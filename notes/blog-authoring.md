# Blog authoring conventions

The single source of truth for producing a post on blog.noprofits.org. Both the
Cowork assistant and Claude Code should read this before drafting, and follow it
exactly so every post comes out consistent. Pipeline order: **research → draft →
bib → figures → hero/OG → branch → verify → PR → merge → auto-deploy.**

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
- [ ] Citations in the correct convention for the series
- [ ] New bib entries appended (science posts only), keys unique & de-duped
- [ ] Figure 1 authored at 1200×630 in house style; `<figure>` + alt text
- [ ] Every figure, table, and code block has a numbered caption (Figure/Table/Code N) and is referenced by number in the prose
- [ ] `og-image` set to the hero
- [ ] Cross-links to the rest of the series
- [ ] Handed to Claude Code / Peter for branch, `stack build`, PR, merge
