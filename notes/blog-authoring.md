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
                            # no author line — the nonprofit series omits it (renders with no byline)
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

## 3. Citations — inline links only

This blog is now nonprofit-sector research exclusively; the science/technical
series has moved to a separate repository. There is one citation convention:

**Inline markdown hyperlinks to the DOI/URL. No `[@key]`, no reference list.**
(`how-to-vet-a-charity` and `501c3-vs-c4-vs-c6` are the template.)

Do **not** use markdown footnotes (`[^1]`) or Pandoc citations (`[@key]`). The
Pandoc citation pipeline (`lib/Blog/Compilers.hs` → `readPandocBiblio`) is still
wired up and still renders the archived science posts, so `[@key]` will silently
work if you use it — that is a trap, not a license. New posts link inline.

## 4. Bibliography (`bib/bibliography.bib`) — append-only, verified entries

Nonprofit posts cite with inline links (§3), so most posts add nothing here. But
you may append entries when a source warrants one — provided the entry is
**verified**: you have seen the actual source and its real metadata, not a
plausible-looking reconstruction. Never invent a DOI, page range, or author list.

1. **Append only.** Add new `@entries` at the end. Never reformat, reorder, or
   rewrite existing entries — the file also serves the archived science posts.
2. **One writer at a time.** If another agent has uncommitted changes to this
   file, don't touch it — coordinate first.
3. **Key scheme:** `AuthorYYYYword` (e.g. `Gregory2009Starvation`,
   `Tinkelman2006Donations`). Before adding, grep for the surname AND the year to
   confirm it isn't already present under a different key — common surnames
   produce false-positive substring matches, so verify the actual entry, not just
   the string.

## 5. Figures & the hero image

**File & embed.** PNG in `/images/`, named with the post slug
(`2026-07-06-the-overhead-myth-hero.png`). Embed as:

```html
<figure>
  <img src="/images/NAME.png" alt="Detailed, meaningful description of what the figure shows and argues.">
</figure>
```

Alt text is a real sentence describing the concept, not "figure 1."

**Figures are charts.** Every figure is a data chart generated by script —
matplotlib, committed as a `figures.py` next to the post's `compute.py` under
`calcs/<slug>/`. No illustration, no generated/vector artwork, no prompt-authored
imagery. If a figure isn't showing data, it probably shouldn't be in the post.
The script is part of the deliverable: it must regenerate every PNG in the post
from the analysis output, deterministically.

Brand palette for chart colors (matches the site and the gear logo):

| Role | Hex |
| --- | --- |
| Outline / ink / text | `#143f33`, `#16221d` |
| Teal / sky (series fills) | `#2f7da3`, lifted `#5b9fc0`, deep `#1c5572` |
| Cream (background / labels) | `#f7f1d7`, page `#f7f4ee` |

House chart style: cream or transparent background, dark-green ink for axes and
text, teal for the primary series and the lifted/deep teals for secondary series
or highlighted bins. Keep chrome minimal — no gridline clutter, no 3D, no
drop shadows, no top/right spines.

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
- [ ] Citations are inline links (§3) — no `[@key]`, no footnotes, nothing added to the bib
- [ ] Figures are script-generated charts; `calcs/<slug>/figures.py` committed and regenerates every PNG
- [ ] Figure 1 authored at 1200×630 in house palette; `<figure>` + alt text
- [ ] Every figure, table, and code block has a numbered caption (Figure/Table/Code N) and is referenced by number in the prose
- [ ] `og-image` set to the hero
- [ ] Cross-links to the rest of the series
- [ ] Handed to Claude Code / Peter for branch, `stack build`, PR, merge
