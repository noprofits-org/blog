---
title: "How grants.noprofits.org works: tracing federal money through a live graph"
date: 2026-06-26
author: Peter Johnston
tags: usaspending, propublica, d3, graph, federal grants, javascript, data, transparency
description: A walk through the live tool at grants.noprofits.org — pulling a federal grant-flow graph straight from USAspending.gov, enriching it with ProPublica 990 data, and the decisions (sub-agency grouping, name normalization, proximity-first trimming, a fuzzy-match gate, fiscal-year-normalized taxpayer ratios) that keep it honest.
---

The tool at `grants.noprofits.org` answers one question: when the federal
government hands money to an organization, where does it come from, and where
does it go from there? You type an org — a hospital, a university, a state health
department — and it pulls that organization's federal awards live from
[USAspending.gov](https://www.usaspending.gov/), walks outward a couple of hops,
and draws the result as a force-directed money-flow graph. Each recipient node is
then enriched with its IRS Form 990 financials from
[ProPublica](https://projects.propublica.org/nonprofits/api), so the inspector
can show what fraction of an organization's revenue is federal grant money. The
real point isn't the pretty graph — it's making taxpayer money *legible*: you can
see that a sub-agency you've never heard of is the actual funder, and that a
nonprofit you have heard of runs largely on federal dollars.

This post is a tour of how it's built. The source of truth is the
[`noprofits-org/grants`](https://github.com/noprofits-org/grants) repo, and most
of the interesting decisions are recorded there as `(#NN)` comments tied to a real
bug or a wrong first attempt. Those are the parts worth reading, so that's what
I've pulled out here.

## Architecture at a glance

There's no build step and no server. `index.html` loads ES modules directly in
the browser:

```
index.html          # the live tool
├── live-main.js     # app controller: search, render, inspector, state
├── usaspending.js   # USAspending.gov client → {grants, charities, connected}
├── flow-graph.js    # D3 force-directed renderer (the visualization engine)
├── propublica.js    # IRS-990 enrichment (taxpayer rings + inspector)
└── live.css         # design tokens
```

The separation that matters is between **the rendering engine and the data
adapter**. `flow-graph.js` is deliberately data-shape agnostic: it renders *any*
directed, weighted, entity→entity flow graph. It knows nothing about federal
grants. `usaspending.js` is one adapter that happens to feed it federal data; you
could write another adapter against a different source and the renderer wouldn't
change. The contract between them is a single object shape that
`usaspending.js` emits and everything downstream reads:

- **grants** — the edges: `{ filer_ein, grant_ein, grant_amt, tax_year }`
- **charities** — the nodes: `{ filer_ein, filer_name, receipt_amt, govt_amt, … }`,
  where the `filer_ein` field is an id with a type prefix (`A:` for an agency,
  `R:` for a recipient)
- **connected** — the set of node ids that survived trimming and are actually
  rendered

The field names (`filer_ein`, `tax_year`) are a tell: this shape predates the
live tool — it came from an earlier 990-based version where the nodes really were
990 filers with EINs. The live adapter keeps the shape and overloads it, which is
why an "EIN" here is actually a normalized agency or recipient name. Reusing the
contract meant the renderer didn't have to be rewritten when the data source
changed.

## Pulling the graph from USAspending

This is the heart of the tool. `usaspending.js` builds the graph with a bounded
breadth-first search (BFS) outward from the org you searched for. The root goes on
the frontier at depth 0; each hop expands the frontier by querying USAspending for
each node's awards, registers the new endpoints, and stops at a configured depth:

```javascript
let frontier = [{ ...root, depth: 0 }];
const expanded = new Set();

while (frontier.length > 0) {
    const expandable = frontier.filter(n => n.depth < depth && !expanded.has(n.id));
    if (expandable.length === 0) break;

    const batches = await Promise.all(expandable.map(async node => {
        expanded.add(node.id);
        return node.kind === 'recipient'
            ? await this.recipientEdges(node.name, years)
            : await this.agencyEdges(node.name, years, perAgencyFanout, node.tier || 'toptier');
    }));
    // …register endpoints, aggregate edge amounts, build the next frontier…
}
```

Each level's expansions fire concurrently with `Promise.all`. A recipient node
gets expanded by asking "who funded this org?"; an agency node by asking "who did
this agency fund?". Everything past that point is about making the resulting graph
*correct* and *readable*, and each of those is a decision with a story.

### Group by the sub-agency, not the department (#30)

The first instinct is to group a recipient's inbound awards by the awarding
agency. That's wrong, and it's wrong in a way that destroys the whole point of the
tool. If you collapse everything to the top-tier department, every grant from the
National Institutes of Health, the Health Resources and Services Administration,
and the Centers for Medicare & Medicaid Services becomes one undifferentiated
"HHS" arrow. But "HHS" isn't who funded you — NIH did. The sub-agency *is* the
funder:

```javascript
// A recipient's inbound awards, grouped by the funding SUB-agency (NIH,
// HRSA, CMS…). Grouping by the top-tier "Awarding Agency" collapses every
// HHS sub-agency into a single "HHS" inflow, which misrepresents the funding
// picture (see #30); the sub-agency is the real funder. Awards with no
// sub-agency fall back to the top-tier department.
const sub = r['Awarding Sub Agency'];
const agency = sub || r['Awarding Agency'];
const tier = sub ? 'subtier' : 'toptier';
```

Notice the `tier` that rides along. USAspending's filter API distinguishes
`subtier` from `toptier` agencies, and you have to query a node against the tier it
was minted at. If you mint "HRSA" as a sub-tier node and then, on the next BFS hop,
query it against the top-tier filter, USAspending matches nothing and the agency's
fan-out silently vanishes. So the tier is stored on the node and threaded back into
the next query in `agencyEdges`.

### One award group per query, or you get a 422

The query filters on `award_type_codes`, and there's a constraint hiding in that
list:

```javascript
// USAspending splits award types into groups (grants, loans, contracts, ...)
// and ONE spending_by_award query may only use codes from a single group, else
// it 422s. The "grants" group is exactly these four — the natural identity for
// this app. (Block Grant, Formula Grant, Project Grant, Cooperative Agreement.)
const AWARD_TYPE_CODES = ['02', '03', '04', '05'];
```

You can't mix grant codes and contract codes in one `spending_by_award` call —
USAspending returns a 422. Codes `02`–`05` are the entire grants group, which is
exactly what this tool is about, so the constraint and the scope happen to line up.

### Normalize names so one org is one node (#15)

Award data is messy. The same recipient shows up as `"FRED HUTCH "` in one record
and `"Fred Hutch"` in another, and if you key nodes on the raw string you get two
nodes for one organization and the graph fragments. Node ids key on a normalized
name instead:

```javascript
// Node ids key on a NORMALIZED name (case-folded, whitespace-collapsed) so
// the same entity under different spacing/casing — "FRED HUTCH " vs "Fred
// Hutch" — resolves to ONE node instead of fragmenting (#15). The raw name
// still rides on every edge's sourceName/targetName for display. A stable
// id (recipient UEI) would also disambiguate genuinely distinct same-named
// orgs, but that needs the root resolved to a UEI first — deferred.
normKey(name) { return (name || '').trim().toLowerCase().replace(/\s+/g, ' '); }
agencyId(name) { return 'A:' + this.normKey(name); }
recipientId(name) { return 'R:' + this.normKey(name); }
```

The normalized string is only the *id*; the original display name still travels on
every edge, so the graph reads "Fred Hutch" even though both spellings collapse to
the same node. The comment also flags the limitation honestly: case-folding merges
genuinely-distinct orgs that share a name. The real fix is a stable identifier
(USAspending's Unique Entity Identifier), but that requires resolving the root to a
UEI first — deferred, and noted as such.

### Trim by proximity first, then by dollars (#37)

A two-hop BFS over federal data produces far more nodes than you want on screen, so
the graph trims to a `maxOrgs` budget. The obvious ranking — keep the biggest
dollar nodes — turned out to be exactly wrong, and the comment explaining why is my
favorite in the repo:

```javascript
// Trim to maxOrgs, always keeping the root, ranking by PROXIMITY first
// then dollar volume (#37). Volume-only ranking dropped the root's own
// direct funders (e.g. HRSA at depth 1) in favour of billion-dollar
// nodes several hops away, and trimmed small connector nodes — which,
// with the both-endpoints-survive edge rule, stranded whole far clusters
// (a floating CMS->states blob) with no path back to the root. Keeping
// shallower nodes first means a direct funder is never cut for a distant
// one, and the keep-set stays a prefix-by-depth of the BFS.
let keep = new Set(meta.keys());
if (keep.size > maxOrgs) {
    const ranked = Array.from(meta.entries())
        .filter(([id]) => id !== root.id)
        .sort((a, b) => {
            const da = connected.get(a[0]) ?? Infinity, db = connected.get(b[0]) ?? Infinity;
            return da - db || (b[1].inflow + b[1].outflow) - (a[1].inflow + a[1].outflow);
        })
        .slice(0, Math.max(0, maxOrgs - 1))
        .map(([id]) => id);
    keep = new Set([root.id, ...ranked]);
}
```

`connected.get(id)` is the node's BFS depth. The sort compares depth first
(`da - db`) and only breaks ties by total dollar flow. So a depth-1 direct funder
of the org you searched always outranks a depth-2 giant. Ranking by dollars alone
literally dropped the root's own funders — HRSA, sitting right next to the org you
asked about — in favor of a billion-dollar node two hops out that you didn't care
about.

### Never render a floating blob (#37)

Trimming creates a second hazard. An edge survives only if *both* its endpoints
survive the trim. Cut a small connector node and you can sever the only path
between a distant cluster and the root, leaving an island — a "floating CMS→states
blob" with no visible connection to anything. The fix is to prune the kept set down
to the connected component that actually contains the root:

```javascript
// Prune to the root's connected component so no disconnected cluster is
// ever rendered (#37). Undirected walk — a recipient root reaches its
// funder agencies by traversing edges backward.
const adj = new Map();
for (const id of keep) adj.set(id, []);
for (const { src, tgt } of keptEdges) { adj.get(src).push(tgt); adj.get(tgt).push(src); }
const reachable = new Set([root.id]);
const queue = [root.id];
while (queue.length) {
    for (const nb of (adj.get(queue.shift()) || [])) {
        if (!reachable.has(nb)) { reachable.add(nb); queue.push(nb); }
    }
}
keep = reachable;
```

The walk is deliberately *undirected*. Money flows agency→recipient, but the org
you searched for is usually a recipient, and it reaches its funders by traversing
those edges *backward*. A directed walk from a recipient root would reach nothing.
Anything not reachable from the root is dropped before render, so an island is never
drawn.

## Enriching with 990 data and taxpayer rings

Once the graph is on screen, `live-main.js` enriches every recipient in the
background with ProPublica's 990 data. This is what powers the inspector's
financials and the "taxpayer ring" that flags orgs heavily dependent on federal
money. Two disciplines govern this whole layer: *never attach the wrong 990*, and
*never let an enrichment failure break the graph*.

### The match has to be right, or it's misinformation (#23)

ProPublica's search is fuzzy. Search "Fred Hutch" and you'll get the real
organization plus a scattering of similarly-named or chapter/affiliate orgs. If you
naively take the first result, you can attach the wrong organization's financials —
and in a tool whose entire purpose is showing where taxpayer money goes, a wrong
990 isn't a cosmetic bug, it's misinformation. So `bestMatch` gates candidates
before ranking them:

```javascript
// Gate (per candidate, both STOP-stripped): keep only candidates that
//   (a) overlap ≥60% of the smaller token set, AND
//   (b) contain the query's MOST DISTINCTIVE token (longest, as a rare-token
//       proxy) — this kills cross-domain false accepts that share only a common
//       word, which the bare 60% ratio let through.
const Q = new Set(toks(query));
if (!Q.size) return null;
const distinctive = [...Q].reduce((a, b) => (b.length > a.length ? b : a));
```

The 60%-overlap test alone wasn't enough: two names sharing only a common word
("Foundation", "Health") could clear it. The distinctive-token requirement — the
query's longest token, used as a cheap proxy for "rarest" — has to appear in the
candidate, which kills those cross-domain false accepts. Among survivors, the
ranking prefers an exact token-set match, then the most shared tokens, then the
*fewest extra* tokens — that last tiebreak favors the parent organization over a
"…of Anytown Chapter" variant that would otherwise outrank it. The matched name is
returned alongside the EIN so the inspector can flag when it differs from the
recipient's name on the graph.

### The CORS proxy and best-effort-null

ProPublica's API sends no Cross-Origin Resource Sharing (CORS) headers, so the
browser can't call it directly. Every request goes through the org's shared Vercel
proxy. The more important discipline is what happens on failure:

```javascript
async resolveEin(name) {
    const key = name.trim().toLowerCase();
    if (this.einCache.has(key)) return this.einCache.get(key);
    let d;
    try {
        d = await this.proxied(`${BASE}/search.json?q=${encodeURIComponent(name)}`);
    } catch (e) {
        console.warn('propublica search failed', name, e);
        return null; // transient — do not cache
    }
    const result = bestMatch(name, d.organizations || []);
    this.einCache.set(key, result);
    return result;
}
```

Every enrichment is best-effort and resolves to `null` on any failure — an agency
isn't a nonprofit and has no 990, and a network blip is just a `null` too. The
graph is already drawn; enrichment only ever *adds* to it, so a failed 990 lookup
leaves the node exactly as it was rather than breaking the render. There's a subtle
caching rule in there too: a *deterministic* result (a real match, or a clean
"nothing matched") gets cached, but a *transient* failure returns `null` without
caching, so a later interaction retries instead of being stuck on a momentary blip.

### Don't divide multi-year money by one year's revenue (#28)

The taxpayer ratio is the number the whole tool builds toward: what fraction of an
organization's revenue is federal grant money? The naive computation divides the
graph's federal inflow by the org's 990 total revenue — and that can come out over
100%, which reads as a data error and undermines trust in the figure. The bug is a
units mismatch: the graph sums inflow across *all* selected fiscal years, but a 990
reports *one* year's revenue.

```javascript
// Taxpayer ratio normalized to the 990's fiscal year (#28). The graph
// sums federal inflow across ALL selected years, but a 990's revenue is
// one year — dividing the two can exceed 100% and read as a data error.
// Compare only the 990 year's federal inflow to that year's revenue, and
// only when the 990 year is within the selected fiscal years (so it
// stays consistent with what's on screen).
if (!isAgency && profile && profile.revenue && profile.year != null && this.years.includes(profile.year)) {
    ratioYear = profile.year;
    const entry = this.yearInflows.get(n.id);
    if (entry && entry.year === ratioYear) {
        yearInflow = entry.inflow;
        share = yearInflow / profile.revenue;
    }
}
```

The fix restricts the numerator to the *same* fiscal year the 990 covers, and only
computes the ratio when that year is among the years on screen, so the percentage is
consistent with the graph the user is looking at. The graph *ring*, on the other
hand, intentionally uses the coarse all-years signal against a `0.05` threshold —
it's a binary "this org leans on federal money" highlight, not a stated figure:

```javascript
const TAXPAYER_THRESHOLD = 0.05;   // federal grants / total revenue → rust ring + alert
```

The ring and the inspector number deliberately differ: one is a cheap visual flag,
the other is a precise, fiscal-year-normalized percentage you can quote.

### Timeouts so a hung request never strands the UI (#13, #22)

`enrichAll` fires a dozen or two of these concurrently per Visualize. A single
hung proxy connection used to strand that node's ring on "loading" forever (#22),
and on the USAspending side a hung request would leave the loading overlay spinning
(#13). Both sides cap every request with an `AbortController`:

```javascript
async proxied(target, { timeout = 10000 } = {}) {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), timeout);
    try {
        const res = await fetch(`${PROXY}?url=${encodeURIComponent(target)}`, { signal: ctl.signal });
        if (!res.ok) throw new Error('proxy ' + res.status);
        return await res.json();
    } catch (e) {
        if (e.name === 'AbortError') throw new Error('proxy timeout');
        throw e;
    } finally {
        clearTimeout(t);
    }
}
```

A timeout surfaces as an ordinary error, which the best-effort-null discipline
above already handles — so a slow request degrades to a missing enrichment, never a
stuck spinner.

## Rendering

`flow-graph.js` stays small because it's the generic engine. It derives a visual
*role* for each node from the shape alone:

```javascript
roleOf(n) {
    if (n.id === this.focusId) return 'focus';
    return n.kind === 'agency' ? 'govt' : 'grantee';
}
```

The node you searched for is the focus; agencies are `govt`; everyone else is a
grantee. In federal data there's no such thing as a non-government funder, so the
design's neutral "funder" color is unused and agencies read in rust instead — the
color carries the meaning "this is public money."

One small but necessary detail: the colors live in CSS as design tokens, but SVG
`fill` and `stroke` attributes can't take `var(--…)`. So the renderer resolves each
token to a concrete color once, via `getComputedStyle`, and caches the palette:

```javascript
// resolved to concrete colors here because SVG attributes (fill/stroke)
// can't take var() (#18).
function cssToken(name) {
    return getComputedStyle(document.documentElement)
        .getPropertyValue('--' + name).trim();
}
```

That keeps a single source of truth for color across the whole suite — the
stylesheet — while still feeding SVG the literal hex strings it requires. The
renderer also offers two layouts off the same data: a force-directed view and a
depth-columnar hierarchy view, since the BFS depth is already on every node.

## What's deferred, and the point

Two honest limitations. The first is in that normalization comment: case-folding
names merges genuinely-distinct organizations that happen to share a name, and the
real fix — keying nodes on USAspending's stable Unique Entity Identifier — is
deferred because it needs the root resolved to a UEI first. The second is that the
fiscal-year-normalized taxpayer ratio is still an approximation: it lines up the
990's reporting year with the awards in that year, but award timing and 990 fiscal
years don't always align cleanly, so the percentage is a good estimate rather than
an audited figure.

Neither of those changes what the tool is for. Federal money moves through a
structure that's genuinely hard to see: a department contains sub-agencies you've
never heard of, those sub-agencies fund organizations you have, and those
organizations may run largely on the public's money. Every decision above —
grouping by sub-agency, normalizing names, trimming by proximity, gating the 990
match, normalizing the ratio to a fiscal year — exists to make that flow legible
without lying about it. That's the whole job.
