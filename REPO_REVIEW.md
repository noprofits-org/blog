# Blog Repository Review - Findings & Improvement Recommendations

**Review Date:** November 5, 2025
**Reviewer:** Claude (Automated Code Review)
**Repository:** noprofits-org/blog
**Branch:** claude/repo-review-findings-011CUpBsetzBaxfS5UCLXo1d

---

## Executive Summary

Your Hakyll-based blog is a **well-architected, sophisticated static site** with excellent code quality and modern features. The use of Haskell/Hakyll for a technical blog demonstrates strong technical expertise. The site successfully handles complex requirements like TikZ diagram rendering, mathematical notation, and academic citations.

**Overall Assessment:** 8/10
- Strong technical implementation
- Good code organization
- Several opportunities for enhancement

---

## Positive Findings

### 1. **Excellent Code Quality**
- **Clean Haskell code** with modern language extensions (site.hs:1-8)
- **Comprehensive GHC warnings** enabled (blog.cabal:35-43)
- **Well-structured** with clear separation of concerns
- **Type-safe** compilation with Haskell's strong type system

### 2. **Advanced Features**
- **TikZ to SVG conversion** - Unique and impressive (site.hs:98-162)
- **BibTeX integration** for academic citations
- **MathJax support** for mathematical notation
- **Responsive design** with separate mobile/desktop/print CSS
- **Code copy buttons** for better UX

### 3. **Good DevOps Practices**
- **GitHub Actions CI/CD** pipeline (deploy.yml)
- **Dependency caching** to speed up builds
- **Automated deployment** to GitHub Pages
- **Custom domain** with CNAME configuration

### 4. **Modern CSS Architecture**
- **Modular CSS** with separate files (base, mobile, desktop, print)
- **CSS custom properties** for theming
- **Dark theme** by default
- **Print-friendly styles**

---

## Areas for Improvement

### **CRITICAL ISSUES**

#### 1. **Security: Debug Trace Functions Left in Production Code**
**Location:** `site.hs:20, 34, 38`
```haskell
import Debug.Trace  -- Line 20
trace "Compiling CSL..." $ return ()  -- Line 34
trace "Compiling bibliography..." $ return ()  -- Line 38
```
**Issue:** Debug.Trace is imported and used, which is typically for debugging only.

**Recommendation:** Remove trace statements or use conditional compilation.

#### 2. **Security: External CDN Dependencies Without SRI**
**Location:** `templates/default.html:13`
```html
<script defer id="MathJax-script" src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```
**Issue:** No Subresource Integrity (SRI) hashes to verify CDN resources.

**Risk:** CDN compromise could inject malicious code.

**Recommendation:** Add SRI attributes:
```html
<script defer id="MathJax-script"
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
    integrity="sha384-[hash]"
    crossorigin="anonymous"></script>
```

#### 3. **Missing Content Security Policy (CSP)**
**Issue:** No CSP headers defined for the site.

**Recommendation:** Add CSP meta tag to `templates/default.html` or configure via GitHub Pages.

---

### **HIGH PRIORITY**

#### 4. **CHANGELOG Never Updated**
**Location:** `CHANGELOG.md:10-11`
```markdown
## 0.1.0.0 - YYYY-MM-DD
```
**Issue:** Placeholder content since project inception, despite active development.

**Recommendation:** Either maintain it properly or remove it. Based on git log, the project has had significant changes (removed 19 posts, added new features).

#### 5. **No Testing Infrastructure**
**Issue:** VSCode tasks include `stack test` (tasks.json), but no test files exist.

**Recommendation:**
- Add property-based tests for TikZ conversion pipeline
- Add tests for Pandoc filters
- Consider snapshot testing for HTML output

#### 6. **Hardcoded Paths and Configuration**
**Location:** `site.hs:61, 165-167`
```haskell
bibtexMathCompiler "bib/style.csl" "bib/bibliography.bib"
```
**Issue:** Configuration values hardcoded in Haskell source.

**Recommendation:** Move to configuration file (YAML or similar) for easier maintenance.

#### 7. **Mixed Content File Extensions**
**Issue:** Posts use `.md`, `.markdown` inconsistently. About page uses `.rst`.

**Recommendation:** Standardize on one extension (`.md` is most common). Convert `.rst` to Markdown for consistency.

#### 8. **No RSS/Atom Feed**
**Issue:** Blog lacks RSS/Atom feed for subscribers.

**Recommendation:** Add feed generation (Hakyll has built-in support):
```haskell
create ["atom.xml"] $ do
    route idRoute
    compile $ do
        let feedCtx = postCtx `mappend` bodyField "description"
        posts <- fmap (take 10) . recentFirst =<< loadAllSnapshots "posts/*" "content"
        renderAtom myFeedConfiguration feedCtx posts
```

---

### **MEDIUM PRIORITY**

#### 9. **Error Handling in TikZ Conversion**
**Location:** `site.hs:156, 162`
```haskell
error $ "pdf2svg failed:\nStdout: " ++ stdout2 ++ "\nStderr: " ++ stderr2
```
**Issue:** Hard crashes on TikZ compilation errors. Build fails completely.

**Recommendation:** Graceful degradation - log error, insert placeholder image, continue build.

#### 10. **Verbose Debug Output in Production**
**Location:** `site.hs:138-140`
```haskell
putStrLn $ "Compiling TeX file at: " ++ texFile
putStrLn "TeX content:"
putStrLn =<< readFile texFile
```
**Issue:** Prints all TikZ source to build logs, cluttering CI output.

**Recommendation:** Make conditional or remove for production builds.

#### 11. **Large Binary Files in Git**
**Issue:** `images/DeepSeekThinkingAndResponse.zip` (2.4M) tracked in git.

**Recommendation:** Use Git LFS for large binary files, or host externally.

#### 12. **photonic_radar Directory**
**Location:** `/home/user/blog/photonic_radar/` (479K)
**Issue:** Research data unrelated to blog content in repository.

**Recommendation:** Move to separate repository or remove if obsolete.

#### 13. **No Sitemap.xml**
**Issue:** Missing sitemap for SEO.

**Recommendation:** Generate sitemap.xml with Hakyll for better search engine indexing.

#### 14. **Stack Snapshot Could Be Newer**
**Location:** `stack.yaml:21`
```yaml
snapshot: lts/23/8.yaml  # GHC 9.4.8
```
**Current:** LTS 23.8 (December 2024)
**Latest:** Check for newer LTS versions

**Recommendation:** Periodically update to latest LTS for security patches.

---

### **LOW PRIORITY / ENHANCEMENTS**

#### 15. **No Mobile-Specific Viewport Tests**
**Issue:** Responsive CSS exists but no documented testing on actual devices.

**Recommendation:** Document tested viewport sizes in README.

#### 16. **Missing Favicon Fallbacks**
**Location:** `templates/default.html:16`
```html
<link rel="icon" type="image/svg+xml" href="/images/favicon.svg">
```
**Issue:** Only SVG favicon (not supported by older browsers).

**Recommendation:** Add PNG fallbacks.

#### 17. **No robots.txt**
**Issue:** Missing robots.txt for crawler guidance.

**Recommendation:** Add robots.txt with sitemap reference.

#### 18. **GitHub Actions: Outdated Actions Versions**
**Location:** `.github/workflows/deploy.yml`
- `actions/checkout@v3` (v4 available)
- `actions/cache@v3` (v4 available)
- `peaceiris/actions-gh-pages@v3` (v4 available)

**Recommendation:** Update to latest versions for security and features.

#### 19. **No 404 Page**
**Issue:** No custom 404.html for broken links.

**Recommendation:** Add custom 404 page for better UX.

#### 20. **Accessibility (a11y) Considerations**
**Issues:**
- No skip-to-content link
- Print button lacks aria-label
- No focus indicators visible in CSS

**Recommendation:** Add accessibility improvements:
```html
<a href="#main" class="skip-link">Skip to content</a>
<button onclick="window.print();" aria-label="Print page or save as PDF">
```

#### 21. **Performance: No Image Optimization**
**Issue:** PNG images (e.g., 186K metrics images) could be optimized.

**Recommendation:** Compress images or convert to WebP with PNG fallback.

#### 22. **Code Organization: TikZ Filter Could Be Separate Module**
**Location:** `site.hs:97-162`
**Issue:** 65 lines of TikZ processing in main site.hs.

**Recommendation:** Extract to `lib/TikZ.hs` for modularity and reusability.

#### 23. **No Analytics**
**Issue:** No privacy-respecting analytics (Plausible, Goatcounter, etc.).

**Recommendation:** Consider lightweight analytics if you want usage insights.

---

## Repository Metrics

| Metric | Value |
|--------|-------|
| Total Size | 20 MB |
| Code Quality | Excellent (Haskell type safety + comprehensive GHC warnings) |
| Documentation | Good (README clear, but CHANGELOG unused) |
| Testing | None (opportunity for improvement) |
| Security | Good (some CDN/CSP improvements needed) |
| Maintenance | Active (recent commits Nov 2025) |
| Dependencies | Stable (LTS 23.8, no known CVEs) |

---

## Recommended Action Plan

### **Phase 1: Security & Critical (1-2 hours)**
1. Remove Debug.Trace import and trace calls
2. Add SRI hashes to CDN resources
3. Add basic CSP meta tag
4. Update CHANGELOG or remove it

### **Phase 2: Testing & Quality (4-6 hours)**
5. Set up basic test suite (TikZ conversion tests)
6. Add RSS/Atom feed
7. Improve error handling in TikZ pipeline
8. Standardize file extensions

### **Phase 3: SEO & Discoverability (2-3 hours)**
9. Generate sitemap.xml
10. Add robots.txt
11. Create custom 404 page
12. Add favicon fallbacks

### **Phase 4: Enhancements (ongoing)**
13. Update GitHub Actions to v4
14. Refactor TikZ code to separate module
15. Add accessibility improvements
16. Optimize images
17. Consider analytics

---

## Conclusion

Your blog demonstrates **excellent technical skills** and thoughtful architecture. The TikZ integration is particularly impressive and unique. The main opportunities are in **testing, security hardening, and SEO optimization**. None of the issues are critical blockers, but addressing the security recommendations would strengthen the site's resilience.

The codebase is maintainable, well-structured, and demonstrates good software engineering practices. With the suggested improvements, this could serve as a **reference implementation** for academic/technical Hakyll blogs.

**Strengths:**
- Sophisticated static site architecture
- Excellent code quality
- Modern CI/CD pipeline
- Unique TikZ rendering capability

**Key Areas to Address:**
- Remove debug code
- Add SRI for CDN resources
- Implement testing
- Update/remove CHANGELOG
- Add RSS feed

---

## Technical Details

### Repository Structure
```
blog/
├── .github/workflows/     # CI/CD automation
├── bib/                   # Bibliography and citation styles (202K)
├── css/                   # Modular stylesheets (27K)
├── images/                # Blog assets (7.4M)
├── js/                    # Client-side scripts (6.5K)
├── photonic_radar/        # Research data (479K) - candidate for removal
├── posts/                 # Blog content (14 posts, ~4,700 lines)
├── templates/             # HTML templates (15K)
├── blog.cabal            # Haskell package definition
├── site.hs               # Hakyll site generator (198 lines)
└── stack.yaml            # Stack build configuration
```

### Technology Stack
- **Language:** Haskell (GHC 9.4.8)
- **Framework:** Hakyll 4.15+
- **Build Tool:** Stack (LTS 23.8)
- **Content:** Markdown, reStructuredText
- **Math:** MathJax 3, LaTeX, mhchem
- **Diagrams:** TikZ → SVG conversion
- **Citations:** BibTeX + CSL
- **Hosting:** GitHub Pages (blog.noprofits.org)
- **CI/CD:** GitHub Actions

### Content Focus
The blog focuses on:
- Non-profit financial transparency
- IRS Form 990 data analysis
- Office process optimization
- Technical automation with Python, Google Apps Script
- Network diagnostics

### Build Pipeline
1. Haskell compilation (Stack)
2. LaTeX ecosystem installation
3. Hakyll site generation
   - CSS compression
   - TikZ → SVG conversion
   - Pandoc markdown processing
   - BibTeX citation resolution
   - Template application
4. GitHub Pages deployment

---

**End of Review**
