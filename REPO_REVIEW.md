# Blog Repository Review — Findings & Improvement Recommendations

**Original review:** November 5, 2025
**Last refreshed:** June 15, 2026 (verified against the current tree)
**Reviewer:** Claude (Automated Code Review)
**Repository:** noprofits-org/blog

> **Refresh note (2026-06-15):** The codebase has moved substantially since the
> November 2025 review. The monolithic `site.hs` was split into `app/site.hs` +
> `lib/Blog/{Compilers,Context,Feed,Site,TikZ}.hs`, the TikZ pipeline was
> rewritten (`pdf2svg` → `lualatex` + `dvisvgm`, inline SVG), and feeds, a 404
> page, robots.txt, SRI, and a test stanza were all added. Resolved items are
> marked **✅ RESOLVED** below with what changed; still-open items cross-reference
> the live GitHub issues (#14, #37–#43).

---

## Executive Summary

A **well-architected, sophisticated Hakyll static site** with excellent code
quality and modern features — TikZ diagram rendering, mathematical notation, and
academic citations. The June 2026 refresh found that the majority of the
November 2025 criticals and high-priority items have since been addressed.

**Overall Assessment:** 9/10 (up from 8/10) — most prior findings resolved; the
remaining work is enhancement-grade.

---

## Positive Findings

### 1. Excellent Code Quality
- **Modular Haskell** — logic is split across `lib/Blog/{Compilers,Context,Feed,Site,TikZ}.hs` with a thin `app/site.hs` entry point (the old 198-line monolith is gone).
- **Comprehensive GHC warnings** enabled (`blog.cabal`).
- **Type-safe** compilation; clear separation of concerns.

### 2. Advanced Features
- **TikZ → SVG conversion** via `lualatex` + `dvisvgm` with inline SVG embedding (`lib/Blog/TikZ.hs`) — preserves transparency, gradients, and PostScript specials the old `pdf2svg` path dropped.
- **BibTeX + CSL integration** for academic citations (244 `[@key]` uses, all resolving).
- **MathJax 3** for mathematical notation (now with SRI).
- **RSS + Atom feeds** (`lib/Blog/Feed.hs`, `atom.xml`, `rss.xml`).
- **Code copy buttons** for better UX.

### 3. Good DevOps Practices
- **GitHub Actions CI/CD** (`.github/workflows/deploy.yml`), all actions on v4 / current.
- **Dependency + apt/TeX-Live caching** to speed up builds.
- **Automated deployment** to GitHub Pages with a custom domain (CNAME).

### 4. Theming
- Single consolidated stylesheet `css/default.css` (~18.5 KB) using **CSS custom properties** ("Grey Wolfe" design system), dark by default, with print styles.
- *Note:* this is a change from the Nov-2025 "separate base/mobile/desktop/print files" architecture — now intentionally consolidated.

---

## Status of November 2025 Findings

### ✅ Resolved since November 2025
| # | Finding | Resolution |
|---|---------|------------|
| 1 | `Debug.Trace` in production | Removed — no `Debug.Trace`/`trace` in `lib/` or `app/`. |
| 2 | No SRI on MathJax CDN | SRI `integrity` hash now on the MathJax `<script>` (`templates/default.html:35`). |
| 4 | CHANGELOG placeholder | `CHANGELOG.md` now carries real entries. |
| 5 | No test infrastructure | `test/Spec.hs` + `blog-test` stanza (`blog.cabal:56`) exist (minimal — see #42). |
| 8 | No RSS/Atom feed | Both implemented (`lib/Blog/Site.hs:90-102`, `lib/Blog/Feed.hs`). |
| 9 | Hard crash on TikZ error | Now a graceful `bail` to `stderr` (`lib/Blog/TikZ.hs:143`) instead of `error`. |
| 10 | Verbose TeX dumps in CI | Removed — no source-dumping `putStrLn`. |
| 17 | No robots.txt | `robots.txt` present in root. |
| 18 | Outdated GitHub Actions | `checkout@v4`, `cache@v4`, `actions-gh-pages@v4`. |
| 19 | No 404 page | `404.html` present. |
| 22 | TikZ filter inline in `site.hs` | Extracted to `lib/Blog/TikZ.hs`. |

### 🔶 Still open (tracked as GitHub issues)
| # | Finding | Status / Issue |
|---|---------|----------------|
| 3 | No Content-Security-Policy | Still missing — no CSP meta tag or header. |
| 6 | Hardcoded `bib/` paths | Still inline in source (low priority). |
| 7 | Mixed file extensions | Posts: 25 `.md`, 16 `.markdown`; about page is `.rst`. Not standardized. |
| 11 | Large binary in git | `images/DeepSeekThinkingAndResponse.zip` (2.4 MB) still tracked. |
| 12 | `photonic_radar/` (540 KB) | Unrelated research data still in repo. |
| 13 | No sitemap.xml | Still missing (SEO). |
| 14 | Stack snapshot | Still `lts/23/8` (GHC 9.8.4) — periodic bump advisable. |
| 16 | SVG-only favicon | No PNG/ICO fallback (`templates/default.html:39`). |
| 20 | Accessibility | Skip link still missing → **#39**; broader a11y audit in **#39**. |
| 21 | Image optimization | PNGs unoptimized; SVG/`svgo` work → **#40**. |
| 23 | Analytics | None (optional). |

---

## Open Work — Where It's Tracked

Most remaining enhancement work has been cut into focused issues:

- **#14** — Advanced TikZ→SVG pipeline roadmap (caching, `texlive-fonts-extra`, circuitikz/chemfig/pgfplots in CI, docs). *Note:* the CI package set in `deploy.yml` still does **not** include `circuitikz`/`chemfig`/`pgfplots`/`texlive-fonts-extra`.
- **#37** — Content & metadata (date whitespace fixed; preventative citation check).
- **#38** — Build & CI (pre-commit hooks, TeX-Live caching, lint target).
- **#39** — Accessibility (skip link, empty alts, SVG `<title>`, contrast).
- **#40** — Performance (`svgo`, lazy loading, critical CSS).
- **#41** — Documentation (CONTRIBUTING.md; keep CHANGELOG).
- **#42** — Testing (TikZ property tests, internal link checker).
- **#43** — Mobile (responsive `rem`/`clamp` typography, touch targets; viewport already correct).

---

## Recommended Action Plan (refreshed)

### Cheap wins (sub-hour each)
1. Add a skip-to-content link + fill the 2 empty image alts (**#39**).
2. Add `sitemap.xml` generation and a CSP meta tag.
3. Add a PNG/ICO favicon fallback.

### Repo hygiene
4. Move/remove `photonic_radar/` and `images/DeepSeekThinkingAndResponse.zip` (Git LFS or external host).
5. Standardize post extensions on `.md`; consider converting `about.rst`.

### Quality & enhancement
6. Extend `test/Spec.hs` with TikZ property tests + an internal link checker (**#42**).
7. Land diagram caching and the broader CI package set (**#14**).
8. Add `CONTRIBUTING.md` (**#41**).

---

## Technical Details (current)

### Repository Structure
```
blog/
├── .github/workflows/   # CI/CD (deploy.yml)
├── app/site.hs          # Hakyll entry point
├── lib/Blog/            # Compilers, Context, Feed, Site, TikZ modules
├── bib/                 # bibliography.bib + style.csl
├── css/default.css      # Single consolidated stylesheet (Grey Wolfe)
├── images/              # Blog assets (~15M; includes a 2.4M zip — candidate for removal)
├── js/                  # Client-side scripts
├── photonic_radar/      # Research data (540K) — candidate for removal
├── posts/               # 41 posts (.md / .markdown)
├── templates/           # archive/default/post/post-list HTML
├── test/Spec.hs         # Minimal test suite
├── 404.html, robots.txt # Error page + crawler guidance
├── blog.cabal, stack.yaml
```

### Technology Stack
- **Language / build:** Haskell (GHC 9.8.4), Stack (LTS 23.8)
- **Framework:** Hakyll
- **Content:** Markdown + a little reStructuredText
- **Math:** MathJax 3 (with SRI), LaTeX, mhchem
- **Diagrams:** TikZ → SVG via `lualatex` + `dvisvgm` (inline SVG)
- **Citations:** BibTeX + CSL
- **Feeds:** RSS + Atom
- **Hosting:** GitHub Pages (blog.noprofits.org), GitHub Actions CI/CD

---

**End of Review** — refreshed 2026-06-15.
