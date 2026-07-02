# Changelog for `blog`

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to the
[Haskell Package Versioning Policy](https://pvp.haskell.org/).

## Unreleased

### Added
- `sitemap.xml` generation (posts plus the static pages) — `robots.txt` was
  already advertising it, but the file was never built.
- On-disk cache for rendered TikZ diagrams (`_cache/tikz`, keyed by a hash of
  the preamble and diagram source), persisted across CI runs, so editing prose
  in a diagram-heavy post no longer re-runs LaTeX for every diagram.
- Combined Atom and RSS feeds (`/atom.xml`, `/rss.xml`) with autodiscovery
  `<link>` tags in the site head.
- Custom `404.html` page and `robots.txt`.
- Subresource Integrity (SRI) hash and `crossorigin` on the MathJax CDN
  script, pinned to `mathjax@3.2.2`.

### Changed
- Draft posts (`draft: true`) are now excluded from the build entirely instead
  of getting an unlisted-but-public page; set `PREVIEW_DRAFTS=1` to build and
  list them locally.
- CI no longer installs an unused GHC (the snapshot's GHC comes from Stack and
  is cached), drops the redundant `stack setup`/`stack update` step, and
  deploys from a separate job so only that job holds `contents: write`.
- CI now builds on pull requests (verification only) and deploys solely from
  `main`; GitHub Actions bumped to `checkout@v4`, `cache@v4`, and
  `actions-gh-pages@v4`.

### Fixed
- The fundamentals-of-quantum-chemistry post's URL slug was misspelled
  (`fundementals`); the source file is renamed, internal links updated, and a
  redirect page keeps the old URL alive (`createRedirects`). The post globs in
  `Blog.Site` are now `posts/*.{md,markdown}` so created redirect pages never
  enter listings, feeds, or the sitemap.
- Pigments post: corrected Figure 1's example gaps (2.8 eV/violet→yellow,
  2.1 eV/orange→blue — the old labels paired energies with the wrong colors),
  and untangled the Laporte-rule discussion — cobalt blue's tetrahedral site is
  noncentrosymmetric, so viridian's octahedral Cr³⁺ now carries the
  strictly-forbidden case and site symmetry is presented as a
  forbidden-to-allowed dial ending at YInMn. Also fixed the iron-earth naming
  (hematite reds, sienna raw vs burnt). Enrichments: chromate's and vanadate's
  band edges noted as O→metal charge transfer, vermilion's blackening and
  chrome yellow's browning added as inorganic lightfastness failures (echoed
  in §8), molecular band vs semiconductor edge contrasted at the same gap
  energy, azo/benzimidazolone workhorses mentioned in §3, and the
  particle-in-a-box gap scaling stated explicitly.
- Mobile horizontal overflow: the post tag list (rendered as a single `.chip`
  on posts and `.post-row-topic` on listings) used `white-space:nowrap`, so a
  long comma-separated tag string ran off-screen and widened the page, clipping
  the title. Tags now wrap; `.post-body` also breaks long words/URLs.

### Removed
- `Debug.Trace` instrumentation and verbose success-path logging from
  `site.hs` (failure diagnostics for the TikZ pipeline retained).

## 0.1.0.0 - 2025-11-05

### Added
- Hakyll-based static site for blog.noprofits.org with modular CSS
  (base/mobile/desktop/print), MathJax math, BibTeX citations, and
  TikZ-to-SVG diagram rendering.
- GitHub Actions workflow building the site and deploying to GitHub Pages.
- Posts on automating IRS Form 990 data extraction, a Google Sheets bound
  web-app script for fetching nonprofit data, network-path analysis,
  PowerShell, DNS analysis, and process diagrams.

### Removed
- Science posts migrated to hyperpolarizability.com (since retired).
