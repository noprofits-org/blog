# Changelog for `blog`

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to the
[Haskell Package Versioning Policy](https://pvp.haskell.org/).

## Unreleased

### Added
- Combined Atom and RSS feeds (`/atom.xml`, `/rss.xml`) with autodiscovery
  `<link>` tags in the site head.
- Custom `404.html` page and `robots.txt`.
- Subresource Integrity (SRI) hash and `crossorigin` on the MathJax CDN
  script, pinned to `mathjax@3.2.2`.

### Changed
- CI now builds on pull requests (verification only) and deploys solely from
  `main`; GitHub Actions bumped to `checkout@v4`, `cache@v4`, and
  `actions-gh-pages@v4`.

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
