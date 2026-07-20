# Blog authoring conventions

The single source of truth for producing a post on blog.noprofits.org. Both the
Cowork assistant and Claude Code should read this before drafting, and follow it
exactly so every post comes out consistent. Pipeline order: **research → draft →
bib → figures → hero/OG → branch → verify → PR → merge → auto-deploy.**

---

## The stance — analysis in the open, held loosely

This is the governing voice of the blog; every rule below serves it. We publish
public-data analysis as people who might be wrong, and the writing has to show
it.

**We are working through public data in the open, not delivering verdicts.** The
honest description of most posts is: *we had a question about the nonprofit or
economic world, we pulled public data — IRS 990s, ProPublica, USAspending, grant
records — analyzed it, and here is what we found, how we cut it, and where our
read could be off.* We are not credentialed authorities on the sector; we are
careful readers of open data, writing for people who often know a corner of it
better than we do. A post invites correction; it does not close a case.

**Our numbers are our data cut — say so.** The thing most likely to be wrong is
on our side: which fiscal years we pulled, how we defined a category, which
organizations the filter caught or dropped, how we handled missing filings, a
join that double-counted. State those choices where a reader can check them, and
treat a surprising result as *"this is what our cut shows"* — an invitation to be
corrected on the data — not a finding we are certain of. A different, equally
defensible definition often moves the number. (The most recent correction to
this blog was exactly this kind: a headline that read as a count of
organizations when the data did not support it.)

**We describe organizations; we do not indict them.** This is the reputation
line that matters most here. Public data about a *named* nonprofit or person is
easy to turn into an accusation, and we do not. A high overhead ratio is not
proof of waste; a low one is not proof of virtue — that is the overhead myth we
write *against*, not with. A single filing anomaly is not fraud. When a point
needs a specific organization as an example, make sure the public record fully
and fairly supports exactly what is said, prefer aggregates over singling out a
small charity, and never imply wrongdoing the data cannot establish. When in
doubt, describe the pattern, not the party.

**Observational data shows association, not cause.** Almost everything here is
observational: two lines moving together in a 990 panel is not one causing the
other. Say "associated with," "consistent with," "we cannot separate X from Y
here" — and reserve causal language for a design that actually earns it.

**Novelty is "new to us," not "what the sector hides."** Report plainly what the
public data shows; do not frame it as an exposé of concealed truth or claim it is
unknown to people who work in the field. "New to us; tell us if this is already
known or if we read it wrong" is the honest register.

**Concretely — banned and required framings:**

| Don't write | Write instead |
| --- | --- |
| "Charity X is a scam / wasteful / a fraud" | "In [year] filings, X reports [figure]; here is what that does and does not tell you" |
| "The data proves X causes Y" | "X and Y move together in this data; we can't establish cause here" |
| "We exposed / uncovered what they hide" | "We pulled the public filings, and here is what we found" |
| "Obviously / clearly / everyone knows" | say it plainly, or show it |
| any claim the finding is new to the sector | "new to us; corrections welcome if this is known" |
| singling out one small org to stand for a problem | show the aggregate; name a specific org only when the record fully backs the exact claim |

A slightly contrarian hook (§2) is still house voice — but it frames a *question*
or a common misconception, never an indictment of an organization, and the claim
underneath it must be exactly what the data supports. Keep the closing
caveat/disclaimer line (§2); it is part of this stance, not decoration.

---

## 1. Front matter

YAML only. The template renders the title, date, byline, and tags — do **not**
repeat them as an in-body `# H1`, byline line, or tags line.

```yaml
---
title: "Colon-bearing titles must be quoted"
date: 2026-07-06
author: Peter Johnston      # science posts include this; the nonprofit series omits it (renders with no byline). Match the sibling posts.
tags: nonprofits, data      # comma-separated, lowercase
description: One or two sentences. Used for meta description and social cards.
og-image: /images/2026-07-06-the-overhead-myth-hero.png   # optional; see §5
---
```

- **Title:** quote if it contains a colon or other YAML-significant punctuation.
- **Links:** always site-relative — `/posts/2026-07-05-how-to-vet-a-charity.html`,
  never the absolute `https://blog.noprofits.org/...`.

## 2. Voice

Prose, not bullet lists. Section headers with `##`. Bold key terms on first use.
Em-dashes are fine and characteristic. Lead with a concrete, slightly
contrarian hook. Close by tying back to the series and, where relevant, to the
noprofits.org tools (search.noprofits.org, grants.noprofits.org, ProPublica
Nonprofit Explorer). End reader-facing posts with a one-line caveat/disclaimer
(the nonprofit series does this consistently).

## 3. Citations — two conventions, pick by series

Every post is compiled through the Pandoc citation pipeline
(`lib/Blog/Compilers.hs` → `readPandocBiblio` with `bib/style.csl` +
`bib/bibliography.bib`), so `[@key]` works anywhere. But the two active series
cite differently, and a post must match its siblings:

- **Science / technical series** — Pandoc citations: `[@Halkier1999]`, rendered
  into a numbered reference list via the shared bib. Use for physics/chemistry
  posts.
- **Nonprofit series** — inline markdown hyperlinks to the DOI/URL, **no**
  `[@key]`, **no** reference list. (`how-to-vet-a-charity` and `501c3-vs-c4-vs-c6`
  are the template.) Use for donor/operator/data posts.

Do **not** use markdown footnotes (`[^1]`) — that matches neither.

## 4. Bibliography (`bib/bibliography.bib`) — append-only

Shared 200 KB+ file, and often edited by another session at the same time.
Rules:

1. **Append only.** Add new `@entries` at the end. Never reformat, reorder, or
   rewrite existing entries.
2. **One writer at a time.** If another agent has uncommitted changes to this
   file, don't touch it — coordinate first.
3. **Key scheme:** `AuthorYYYYword` (e.g. `Gregory2009Starvation`,
   `Tinkelman2006Donations`). Before adding, grep the file for the surname AND
   the year to confirm it isn't already present under a different key — common
   surnames produce false-positive substring matches, so verify the actual
   entry, not just the string.
4. Only add entries for the science-series `[@key]` convention. Nonprofit posts
   use inline links and add nothing to the bib.

## 5. Figures & the hero image

**File & embed.** PNG in `/images/`, named with the post slug
(`2026-07-06-the-overhead-myth-hero.png`). Embed as:

```html
<figure>
  <img src="/images/NAME.png" alt="Detailed, meaningful description of what the figure shows and argues.">
</figure>
```

Alt text is a real sentence describing the concept, not "figure 1."

**House illustration style.** Flat vector, bold uniform dark-green outlines,
limited palette, baked-in UPPERCASE condensed-sans labels (the generator drops
free text, so add captions in a type layer afterward). Two proven layouts: a
node-cycle (icons in outlined circles joined by a clockwise arrow ring) or a
two-panel / side-by-side scene with a heading. Brand palette (also on the gear
logo used as the Illustrator color source):

| Role | Hex |
| --- | --- |
| Outline / ink | `#143f33`, `#16221d` |
| Teal / sky (fills) | `#2f7da3`, lifted `#5b9fc0`, deep `#1c5572` |
| Cream (fills / labels) | `#f7f1d7`, page `#f7f4ee` |

Workflow: open the **gear logo** in Illustrator as the color source, run Text to
Vector Graphic with the concept prompt, then add uppercase caption text.

**Text inside data figures: lettered callouts only, never sentences.** Mark
each feature worth explaining with a bold letter (A, B, C…) placed at the
feature, and define every letter in the numbered caption (§6) — ACS style.
Axis labels, tick text, and legend entries are the only other text allowed in
the plot area; values, names, and explanations all go to the caption. If a
chart clips or piles a heavy tail, mark the overflow bins visually (detached
bars in the lifted teal, tick labels like "≤ −6" / "> 36"), letter them, and
let the caption say what they collect.

**Hero = Figure 1 = the social card.** Author Figure 1 at **1200×630 (1.91:1
landscape)** so the same asset serves as both the in-post hero and the OG/Twitter
card — no separate variant, no crop. Compose horizontally (e.g. a left-to-right
loop, or side-by-side panels) rather than square. Then set `og-image` in front
matter to that file. Posts without `og-image` fall back to the generic branded
card (`/images/og-image.png`), so always set it going forward. (Backfill older
posts by setting `og-image` to a 1200×630 crop/reframe of their existing figure.)

## 6. Captions & numbering (required)

**Every figure, table, and code block gets a numbered caption, and every one is
referenced by number somewhere in the prose.** No exceptions — an uncaptioned or
unreferenced element is a bug.

- **Numbering** runs independently per type, in document order: Figure 1, 2, 3…;
  Table 1, 2…; Code 1, 2…. A post can have Figure 1 and Table 1 and Code 1.
- **Format:** the caption label is **bold** for all three types, followed by a
  full sentence (not a bare label):
  - Figures — `**Figure 1.** Sentence describing what it shows.` directly
    **below** the `<figure>`.
  - Tables — `**Table 1.** Sentence describing the table.` directly **below**
    the table.
  - Code blocks — `**Code 1.** Sentence describing what the code does.` directly
    **below** the fenced block.
  - (Older posts used italic `*Figure N.*` / `*Table N.*` — that was a mistake;
    bold is the standard. Normalize when touching an old post.)
- **Cross-reference:** point to each numbered element at least once in the body
  by its number — "(Figure 1)", "as Table 2 shows", "the loop in Code 1". If
  there's no natural place to reference it, it probably doesn't belong in the
  post.
- Figure 1 is still the hero / OG card (§5).

## 7. Deploy flow

`.github/workflows/deploy.yml` builds the Hakyll site with Stack and publishes to
GitHub Pages on **push to `main`** (also PR-to-main and manual dispatch). So:

1. Work on a feature branch (`post/<slug>`), never commit straight to `main`.
2. **Verify before merge:** `stack build && stack exec site build` must succeed;
   check the post renders, citations resolve, figures load, and the card meta is
   right.
3. Open a PR into `main`; merge triggers the deploy.

**Credentials:** the Cowork sandbox has no push credentials and no `gh`, and it
shares the live working tree with Claude Code. So the Cowork assistant authors
files only; **git add/commit/push/PR and the Stack build are done by Claude Code
(runs in the real environment with gh auth) or by Peter.** Never run git in the
shared tree while another session has uncommitted changes.

## 8. Per-post checklist

- [ ] Front matter complete; title quoted if needed; links relative
- [ ] Voice matches the series; disclaimer line if reader-facing
- [ ] **Stance check:** numbers presented as our data cut (years/definitions/filters stated); no organization indicted beyond what the public record fully supports; no causal claim from observational data; no exposé / "new to the sector" framing; post invites correction (stance section)
- [ ] Citations in the correct convention for the series
- [ ] New bib entries appended (science posts only), keys unique & de-duped
- [ ] Figure 1 authored at 1200×630 in house style; `<figure>` + alt text
- [ ] Every figure, table, and code block has a numbered caption (Figure/Table/Code N) and is referenced by number in the prose
- [ ] `og-image` set to the hero
- [ ] Cross-links to the rest of the series
- [ ] Handed to Claude Code / Peter for branch, `stack build`, PR, merge
