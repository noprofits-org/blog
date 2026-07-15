# Public Support Cliff — Blog Post Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the fifth post in the Form 990 data series — the bunching finding at the 33⅓% public support cliff — with a downloadable, self-asserting analysis script, four figures, two tables, and a merged PR.

**Architecture:** Same sibling pattern as `calcs/who-pays/`. `compute.py` (pandas env) does all arithmetic, asserts every spec number, and writes all-numeric intermediates plus a `stats.json`. `figures.py` (matplotlib env, numpy-only) renders. One new Hakyll rule publishes the analysis scripts so readers can download the exact code. The post links to that code directly.

**Tech Stack:** Python 3 (pandas, numpy, matplotlib), Hakyll + Stack, `gh`.

## Global Constraints

Copied from `docs/superpowers/specs/2026-07-15-public-support-cliff-design.md` and `notes/blog-authoring.md`. Every task implicitly includes this section.

- **Spec is authoritative on numbers.** If a script disagrees with the spec, **the script is wrong**. Do not edit the spec to match. Escalate to Peter.
- **Data:** `calcs/data/24eoextract990.csv` (IRS SOI extract, returns filed CY2024). Read-only.
- **Population:** `subseccd == 3` AND `totsupp170 > 0` AND `nonpfrea == 7` AND support pct in [0,100] → **111,991** orgs. Support pct = `pubsupplesspct170 / totsupp170 * 100`.
- **Two environments — no interpreter has both pandas and matplotlib:**
  - `compute.py` → `python3` (gwc venv: pandas + numpy, **no** matplotlib)
  - `figures.py` → `/opt/homebrew/Caskroom/miniforge/base/envs/qchem/bin/python` (matplotlib + numpy, **no** pandas). Reads via `np.genfromtxt` → **every intermediate column must be numeric.**
- **Intermediates stay untracked** (match `calcs/below-zero/`, `calcs/who-pays/` — scripts only).
- **Bootstrap must pin `np.random.default_rng(7)` and 400 resamples.** The post publishes this script; a reader who reruns it must get the post's numbers. An unseeded bootstrap silently breaks the transparency claim.
- **The specification was frozen before the placebo test:** bw=0.5, degree=5, W=1.5. Do not "improve" it. Raising the number by respecifying is p-hacking; the spec's values stand.
- **Frontmatter:** `tags: nonprofits, data`; **no `author` field**; `og-image` → hero; quote the title if it has a colon.
- **Citations:** inline markdown links only. No `[@key]`, no reference list, no footnotes, nothing appended to `bib/bibliography.bib`.
- **Captions:** every figure/table/code block gets a **bold** numbered caption and a by-number prose reference.
- **Figure text:** lettered callouts only; axis/tick/legend text is the only other plot-area text.
- **Palette:** ink `#143f33`, teal `#2f7da3`, lifted `#5b9fc0`, deep `#1c5572`, cream `#f7f1d7`, page `#f7f4ee`.
- **Honesty constraints (spec §Honesty and inference) — violations are factual errors:**
  1. **Never assert the mechanism.** Four processes produce this signature (donor-broadening, classification judgment, timing, misreporting); this data distinguishes none of them. Never imply fraud — and never imply benignity either ("the rule working as designed" is equally unsupported). State the displacement; leave the mechanism open; name what would resolve it (panel data, Schedule B).
  2. **Verbs:** *steer*, *respond to*, *manage*. Never *dodge*, *game*, *cook*, *cheat*.
  3. **The 10% result is a null**, not a finding: "cannot be distinguished from the placebos," never "we showed they don't respond."
  4. **One year of filings; a multi-year rule.** Never imply we observed an org lose public charity status.
- **Legal claims:** verify against an IRS source and carry an inline link. **Do not assert tax mechanics from memory.** If it can't be sourced, cut it — the finding doesn't depend on it.
- **Branch:** `post/public-support-cliff` (exists, holds the spec). Never commit to `main`. Do not merge without Peter.

## File Structure

| File | Responsibility |
| --- | --- |
| `calcs/public-support-cliff/compute.py` | All arithmetic: population, estimator, placebo, bootstrap, spec grid, 2% rule. Asserts every spec value. Writes intermediates. **Published for download — must run standalone and document itself.** |
| `calcs/public-support-cliff/cf.csv.gz` | Generated: `mid`, `obs`, `cf` — binned density + counterfactual (Figure 1). |
| `calcs/public-support-cliff/cliff.csv.gz` | Generated: `pct`, `pct_excluded` (Figures 2, 4). |
| `calcs/public-support-cliff/stats.json` | Generated: scalars + placebo list + spec grid (Figure 3, prose). |
| `calcs/public-support-cliff/figures.py` | All rendering, numpy-only. No arithmetic beyond binning. **Published for download.** |
| `lib/Blog/Site.hs` | One new rule publishing `calcs/*/*.py`. |
| `posts/2026-07-15-public-support-cliff.md` | The prose. |

---

### Task 1: compute.py — estimator, placebo, bootstrap, assertions

**Files:**
- Create: `calcs/public-support-cliff/compute.py`
- Create (generated): `cf.csv.gz`, `cliff.csv.gz`, `stats.json`
- Reference: `calcs/who-pays/compute.py` (sibling style), the spec

**Interfaces:**
- Consumes: `../data/24eoextract990.csv`
- Produces: `cf.csv.gz` (cols `mid`, `obs`, `cf`); `cliff.csv.gz` (cols `pct`, `pct_excluded`); `stats.json` with keys `n`, `median_pct`, `n_below`, `pct_below`, `n_near`, `pct_near`, `real_displacement`, `placebos` (list of `[threshold, displacement]`), `placebo_mean`, `placebo_sd`, `z`, `n_placebos_ge_real`, `boot_lo`, `boot_hi`, `grid` (list of `[bw, deg, displacement]`), `ten_displacement`, `ten_z`, `near_excluded_median`, `typ_excluded_median`, `corr_excluded`. Tasks 3–4 read exactly these names.

- [ ] **Step 1: Write compute.py**

The `check()` calls are the test — they encode the spec's verified findings.

```python
#!/usr/bin/env python3
"""Bunching at the 33-1/3% public support cliff — 501(c)(3) public charities.

Supports posts/2026-07-15-public-support-cliff.md on blog.noprofits.org.
This script is published for download alongside the post; it is meant to be
read, disagreed with, and rerun.

WHAT IT DOES
  A charity relying on the IRC 170(b)(1)(A)(vi) support test must draw at least
  one-third of its support from the public. This script asks whether the
  distribution of that ratio shows *bunching* just above the line: a deficit of
  organizations below it and an excess above.

  Estimator: fit a counterfactual density (degree-5 polynomial, 0.5-point bins)
  over [20,50] EXCLUDING a +/-1.5-point window around 33.333, then compare
  observed to counterfactual inside the window.
      displacement = (observed - counterfactual) above
                   + (counterfactual - observed) below

  The specification (bw=0.5, degree=5, W=1.5) was FIXED BEFORE the placebo test.
  Section GRID reports all 12 bandwidth/degree combinations, including the ones
  that attenuate the estimate, so the reader sees the whole pile rather than a
  flattering pick.

WHAT IT CANNOT DO
  It cannot identify the mechanism. Donor-broadening, classification judgment,
  timing across the 5-year window, and misreporting all produce the same
  signature. One year of as-filed aggregates separates none of them.

DATA
  ../data/24eoextract990.csv — IRS SOI annual extract of tax-exempt organization
  financial data, returns filed CY2024 (mostly fiscal 2023).
  https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data

  The support ratio is a FIVE-YEAR measure (Schedule A Part II), not annual.

RUN
  python3 compute.py          # needs pandas + numpy
"""

import json
import numpy as np
import pandas as pd

SRC = "../data/24eoextract990.csv"
CLIFF = 100.0 / 3.0
BW, DEG, W = 0.5, 5, 1.5           # frozen before the placebo test
LO, HI = 20.0, 50.0                # fitting region for the real cliff
BOOT_SEED, BOOT_N = 7, 400         # pinned so a reader reproduces the CI

FAILURES = []


def check(label, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'ok  ' if ok else 'FAIL'} {label:46s} got {got:>12,.3f}   spec {want:>12,.3f}")
    if not ok:
        FAILURES.append(f"{label}: got {got:,.4f}, spec says {want:,.4f}")


def displacement(data, cliff, lo, hi, bw=BW, deg=DEG, w=W):
    """Excess mass above the threshold plus missing mass below it, against a
    polynomial counterfactual fitted on the region OUTSIDE the +/-w window."""
    bins = np.arange(lo, hi + bw, bw)
    cnt, e = np.histogram(data, bins=bins)
    mid = (e[:-1] + e[1:]) / 2
    excl = (mid > cliff - w) & (mid < cliff + w)
    cf = np.polyval(np.polyfit(mid[~excl], cnt[~excl], deg), mid)
    ab = (mid >= cliff) & (mid < cliff + w)
    be = (mid >= cliff - w) & (mid < cliff)
    return (cnt[ab].sum() - cf[ab].sum()) + (cf[be].sum() - cnt[be].sum())


COLS = ["EIN", "tax_pd", "subseccd", "pubsupplesspct170", "totsupp170",
        "nonpfrea", "exceeds2pct170", "totrevenue", "totassetsend"]
df = pd.read_csv(SRC, usecols=COLS)
df = df.sort_values("tax_pd").drop_duplicates("EIN", keep="last")
d = df[(df.subseccd == 3) & (df.totsupp170 > 0)].copy()
d["npr"] = pd.to_numeric(d.nonpfrea, errors="coerce")
d["pct"] = d.pubsupplesspct170 / d.totsupp170 * 100
d = d[(d.npr == 7) & (d.pct.between(0, 100))].copy()
d["pct_excluded"] = d.exceeds2pct170.fillna(0) / d.totsupp170 * 100
p = d.pct.values

print("\nPOPULATION")
check("n (subsec 3, nonpfrea 7, pct in [0,100])", len(d), 111_991, 0)
check("median public support %", np.median(p), 95.7, 0.05)
check("n below the 33-1/3 line", (p < CLIFF).sum(), 4_323, 0)
check("% below the line", (p < CLIFF).mean() * 100, 3.86, 0.02)
check("n within 1.5pt of the line", ((p > CLIFF - 1.5) & (p < CLIFF + 1.5)).sum(), 670, 0)
check("% within 1.5pt", ((p > CLIFF - 1.5) & (p < CLIFF + 1.5)).mean() * 100, 0.60, 0.02)

# The ratio is a five-year measure, not annual — this is why.
r = (d.totsupp170 / d.totrevenue)[d.totrevenue > 0]
check("median totsupp170 / one yr revenue", r.median(), 3.70, 0.02)

print("\nWINDOWS (observed vs counterfactual)")
for w_, ab_want, cf_ab_want, be_want, cf_be_want in [
        (1.0, 267, 241.0, 187, 223.4),
        (1.5, 399, 370.3, 280, 331.4),
        (2.0, 536, 502.0, 379, 433.6)]:
    bins = np.arange(LO, HI + BW, BW)
    cnt, e = np.histogram(p, bins=bins)
    mid = (e[:-1] + e[1:]) / 2
    excl = (mid > CLIFF - w_) & (mid < CLIFF + w_)
    cf = np.polyval(np.polyfit(mid[~excl], cnt[~excl], DEG), mid)
    ab = (mid >= CLIFF) & (mid < CLIFF + w_)
    be = (mid >= CLIFF - w_) & (mid < CLIFF)
    check(f"W={w_} observed above", cnt[ab].sum(), ab_want, 0)
    check(f"W={w_} counterfactual above", cf[ab].sum(), cf_ab_want, 0.3)
    check(f"W={w_} observed below", cnt[be].sum(), be_want, 0)
    check(f"W={w_} counterfactual below", cf[be].sum(), cf_be_want, 0.3)

REAL = displacement(p, CLIFF, LO, HI)
print("\nHEADLINE")
check("real displacement (bw=.5 deg=5 W=1.5)", REAL, 80.1, 0.3)

# ---- placebo: identical estimator at thresholds with no rule -------------
# Window geometry mirrors the real one: [cliff-13.33, cliff+16.67] -> [20,50].
print("\nPLACEBO (21 fake thresholds)")
placebos = []
for t in np.arange(22, 49, 1.0):
    if abs(t - CLIFF) < 3:
        continue
    s = displacement(p, float(t), max(10.0, t - 13.0), min(95.0, t + 17.0))
    placebos.append([float(t), float(s)])
pl = np.array([s for _, s in placebos])
check("n placebos", len(pl), 21, 0)
check("placebo mean", pl.mean(), -4.2, 0.3)
check("placebo sd", pl.std(), 22.4, 0.3)
Z = (REAL - pl.mean()) / pl.std()
check("z vs placebo distribution", Z, 3.77, 0.05)
check("placebos >= real", (pl >= REAL).sum(), 0, 0)
check("largest placebo", pl.max(), 35.0, 0.5)

# ---- bootstrap ----------------------------------------------------------
rng = np.random.default_rng(BOOT_SEED)
b = np.array([displacement(rng.choice(p, len(p), replace=True), CLIFF, LO, HI)
              for _ in range(BOOT_N)])
BLO, BHI = np.percentile(b, 2.5), np.percentile(b, 97.5)
print(f"\nBOOTSTRAP (seed={BOOT_SEED}, {BOOT_N} resamples)")
check("bootstrap 2.5th pct", BLO, 28.1, 8.0)
check("bootstrap 97.5th pct", BHI, 129.0, 12.0)
check("bootstraps <= 0", (b <= 0).sum(), 0, 0)
assert BLO > 0, "bootstrap CI must exclude zero"

# ---- specification grid: publish the whole pile -------------------------
print("\nGRID (all 12 specifications)")
grid = []
for bw in (0.25, 0.5, 1.0):
    for deg in (3, 4, 5, 6):
        s = displacement(p, CLIFF, LO, HI, bw=bw, deg=deg)
        grid.append([bw, deg, float(s)])
        print(f"    bw={bw:<5} deg={deg}  displacement {s:+7.1f}")
g = np.array([s for _, _, s in grid])
check("grid min", g.min(), 46.9, 0.5)
check("grid max", g.max(), 95.4, 0.5)
check("grid cells positive", (g > 0).sum(), 12, 0)

# ---- the 10% facts-and-circumstances floor: a NULL ----------------------
print("\nTEN PERCENT FLOOR (reported as a null)")
TEN = displacement(p, 10.0, 2.0, 25.0)
tp = np.array([displacement(p, float(t), max(1.0, t - 7.0), t + 11.0)
               for t in (5, 6, 7, 8, 13, 14, 15, 16, 17, 18)])
TENZ = (TEN - tp.mean()) / tp.std()
check("10% displacement", TEN, 44.6, 0.3)
check("10% z (NOT significant)", TENZ, 1.73, 0.05)
check("placebo at 5% (as large as the real 10%)", tp[0], 45.5, 0.5)

# ---- the 2% rule: the mechanism behind who stands near the cliff ---------
near = d[(d.pct > CLIFF - 5) & (d.pct < CLIFF + 5)]
typ = d[d.pct >= 80]
print("\nTHE 2% RULE")
check("near-cliff n", len(near), 2_308, 0)
check("typical n", len(typ), 80_940, 0)
check("near-cliff median % excluded", near.pct_excluded.median(), 53.9, 0.05)
check("typical median % excluded", typ.pct_excluded.median(), 0.0, 0.01)
check("near-cliff median revenue", near.totrevenue.median(), 387_204, 1)
check("typical median revenue", typ.totrevenue.median(), 662_907, 1)
check("near-cliff median assets", near.totassetsend.median(), 1_266_282, 1)
check("typical median assets", typ.totassetsend.median(), 829_810, 1)
CORR = d.pct.corr(d.pct_excluded)
check("corr(support %, % excluded)", CORR, -0.744, 0.005)

# ---- intermediates (all-numeric; figures.py has no pandas) ---------------
bins = np.arange(LO, HI + BW, BW)
cnt, e = np.histogram(p, bins=bins)
mid = (e[:-1] + e[1:]) / 2
excl = (mid > CLIFF - W) & (mid < CLIFF + W)
cf = np.polyval(np.polyfit(mid[~excl], cnt[~excl], DEG), mid)
pd.DataFrame({"mid": mid, "obs": cnt, "cf": cf}).to_csv(
    "cf.csv.gz", index=False, compression="gzip")
d[["pct", "pct_excluded"]].to_csv("cliff.csv.gz", index=False, compression="gzip")

with open("stats.json", "w") as f:
    json.dump({"n": int(len(d)), "median_pct": float(np.median(p)),
               "n_below": int((p < CLIFF).sum()),
               "pct_below": float((p < CLIFF).mean() * 100),
               "n_near": int(((p > CLIFF - 1.5) & (p < CLIFF + 1.5)).sum()),
               "pct_near": float(((p > CLIFF - 1.5) & (p < CLIFF + 1.5)).mean() * 100),
               "real_displacement": float(REAL), "placebos": placebos,
               "placebo_mean": float(pl.mean()), "placebo_sd": float(pl.std()),
               "z": float(Z), "n_placebos_ge_real": int((pl >= REAL).sum()),
               "boot_lo": float(BLO), "boot_hi": float(BHI), "grid": grid,
               "ten_displacement": float(TEN), "ten_z": float(TENZ),
               "near_excluded_median": float(near.pct_excluded.median()),
               "typ_excluded_median": float(typ.pct_excluded.median()),
               "corr_excluded": float(CORR)}, f, indent=2)

print("\nwrote cf.csv.gz, cliff.csv.gz, stats.json")
if FAILURES:
    print(f"\n{len(FAILURES)} SPEC MISMATCH(ES) — the script is wrong, not the spec:")
    for f_ in FAILURES:
        print("  " + f_)
    raise SystemExit(1)
print("\nall spec assertions passed")
```

- [ ] **Step 2: Run it**

```bash
cd calcs/public-support-cliff && python3 compute.py
```

Expected: every line `ok`, ending `all spec assertions passed`, exit 0. Takes ~90s (the bootstrap does 400 refits).

**If an assertion FAILS:** the spec is authoritative — debug the script. Do NOT edit the spec, and do NOT change `BW`/`DEG`/`W` to make a number match; the specification is frozen. Likely culprits: a missing `nonpfrea == 7` filter, the `[0,100]` restriction, or placebo window geometry (`t-13` / `t+17`). If the bootstrap CI is outside tolerance but the point estimate is exact, that is a numpy-version RNG difference — report it to Peter rather than widening the tolerance silently.

- [ ] **Step 3: Verify the intermediates are all-numeric**

```bash
cd calcs/public-support-cliff && python3 -c "
import pandas as pd, json
cf = pd.read_csv('cf.csv.gz'); cl = pd.read_csv('cliff.csv.gz')
print('cf cols:', list(cf.columns), 'rows:', len(cf))
print('cliff cols:', list(cl.columns), 'rows:', len(cl), '(expect 111,991)')
assert all(str(t).startswith(('int','float')) for t in cf.dtypes), 'cf.csv.gz not all-numeric'
assert all(str(t).startswith(('int','float')) for t in cl.dtypes), 'cliff.csv.gz not all-numeric'
s = json.load(open('stats.json'))
print('stats keys:', sorted(s.keys()))
print('placebos:', len(s['placebos']), '| grid:', len(s['grid']))
print('ok — numeric intermediates, np.genfromtxt can read them')
"
```

Expected: `cliff.csv.gz` 111,991 rows; 21 placebos; 12 grid cells; `ok`.

- [ ] **Step 4: Commit**

```bash
git add calcs/public-support-cliff/compute.py
git commit -m "calcs: public-support-cliff — bunching estimator, asserted against spec

Displacement +80.1 orgs at the 33-1/3 line; placebo z=+3.77 with 0 of 21 fake
thresholds matching; bootstrap CI excludes zero; all 12 specifications positive.
Bootstrap seed pinned (7/400) so a reader who downloads the script reproduces
the post's CI. Specification frozen before the placebo test.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

Intermediates stay untracked, matching the siblings.

---

### Task 2: Publish the analysis code for download

**Files:**
- Modify: `lib/Blog/Site.hs` (add one rule near the `images/*` rule, ~line 51)

**Interfaces:**
- Consumes: nothing.
- Produces: `_site/calcs/<dir>/*.py` served at `/calcs/<dir>/<script>.py`. Task 5's post links to these URLs; Task 6 verifies them.

Peter's requirement: the code must be downloadable. For a post whose claim rests on a specification invisible from the prose, publishing the script *is* the argument.

- [ ] **Step 1: Read the existing static rules**

```bash
sed -n '45,70p' lib/Blog/Site.hs
```

You should see the `match "images/*"` block using `route idRoute` and `compile copyFileCompiler`. Match that style exactly.

- [ ] **Step 2: Add the rule**

Insert immediately after the `match "images/*"` block:

```haskell
    match "calcs/*/*.py" $ do
        route   idRoute
        compile copyFileCompiler
```

**The glob must be `calcs/*/*.py` — NOT `calcs/**`.** `calcs/**` would sweep in `calcs/data/24eoextract990.csv` (247 MB) and every `.csv.gz` intermediate, bloating the deploy and publishing derived data that is deliberately untracked. `calcs/*/*.py` matches only Python scripts exactly one directory deep (verified: 8 scripts, 0 data files).

- [ ] **Step 3: Build and verify exactly what got published**

```bash
stack build && stack exec blog build 2>&1 | tail -2
echo "--- published scripts ---"; find _site/calcs -type f | sort
echo "--- MUST be empty (no data published) ---"; find _site/calcs \( -name '*.csv' -o -name '*.csv.gz' -o -name '*.json' \) -print
echo "--- deploy size sanity ---"; du -sh _site/calcs
```

Expected: 8 `.py` files under `_site/calcs/`; the data check prints **nothing**; `_site/calcs` is a few tens of KB, not megabytes.

- [ ] **Step 4: Verify a script is actually fetchable**

```bash
cd _site && (python3 -m http.server 8899 >/dev/null 2>&1 &) ; sleep 1
curl -s -o /dev/null -w "who-pays compute.py -> %{http_code}\n" http://localhost:8899/calcs/who-pays/compute.py
curl -s -o /dev/null -w "247MB extract      -> %{http_code} (MUST be 404)\n" http://localhost:8899/calcs/data/24eoextract990.csv
pkill -f "http.server 8899"
```

Expected: `200` for the script, `404` for the extract. If the extract returns 200, the glob is wrong — stop and fix it before going further.

- [ ] **Step 5: Commit**

```bash
git add lib/Blog/Site.hs
git commit -m "site: publish analysis scripts for download

Adds match \"calcs/*/*.py\" + copyFileCompiler so every post's analysis code is
fetchable at /calcs/<post>/compute.py. Scoped to *.py one directory deep so it
cannot publish calcs/data/24eoextract990.csv (247MB) or the .csv.gz
intermediates. Retroactively publishes the scripts behind the earlier posts.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: figures.py scaffold + Figure 1 (hero)

**Files:**
- Create: `calcs/public-support-cliff/figures.py`
- Create (generated): `images/2026-07-15-public-support-cliff-hero.png`
- Reference: `calcs/who-pays/figures.py`

**Interfaces:**
- Consumes: `cf.csv.gz` (`mid`, `obs`, `cf`), `cliff.csv.gz` (`pct`, `pct_excluded`), `stats.json` from Task 1.
- Produces: palette constants, `letter()`, loaded `cf`/`cl`/`stats`, reused by Task 4 in the same file.

**Hard constraint:** exactly **1200×630** — hero and OG card. At 150 dpi that is `figsize=(8, 4.2)`.

- [ ] **Step 1: Write figures.py**

```python
#!/usr/bin/env python3
"""Figures for the public-support-cliff post. numpy + matplotlib, brand palette
(notes/blog-authoring.md §5). Lettered callouts only; captions carry the words.

NO PANDAS — deliberately. compute.py runs under an env with pandas; this runs
under one with matplotlib, and on this machine no interpreter has both (same as
the below-zero and who-pays siblings). Hence np.genfromtxt and all-numeric
intermediates.

Run:
  /opt/homebrew/Caskroom/miniforge/base/envs/qchem/bin/python figures.py

Reads cf.csv.gz, cliff.csv.gz, stats.json (written by compute.py). Writes:
  images/2026-07-15-public-support-cliff-hero.png          Figure 1 (1200x630)
  images/2026-07-15-public-support-cliff-distribution.png  Figure 2
  images/2026-07-15-public-support-cliff-placebo.png       Figure 3
  images/2026-07-15-public-support-cliff-concentration.png Figure 4
"""

import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

INK = "#143f33"
TEAL = "#2f7da3"
TEAL_LIFT = "#5b9fc0"
TEAL_DEEP = "#1c5572"
CREAM = "#f7f1d7"
PAGE = "#f7f4ee"

mpl.rcParams.update({
    "figure.facecolor": PAGE, "axes.facecolor": PAGE,
    "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "text.color": INK,
    "font.family": "DejaVu Sans", "axes.spines.top": False,
    "axes.spines.right": False, "savefig.dpi": 150,
})

OUT = "../../images/2026-07-15-public-support-cliff-{}.png"
CLIFF = 100.0 / 3.0

cf = np.genfromtxt("cf.csv.gz", delimiter=",", names=True)
cl = np.genfromtxt("cliff.csv.gz", delimiter=",", names=True)
stats = json.load(open("stats.json"))

mid, obs, cfv = cf["mid"], cf["obs"], cf["cf"]
pct, pct_excl = cl["pct"], cl["pct_excluded"]


def letter(ax, x, y, s):
    """Bold lettered callout — the only prose allowed in a plot area."""
    ax.text(x, y, s, fontsize=13, fontweight="bold", color=INK,
            ha="center", va="center", zorder=10,
            bbox=dict(boxstyle="circle,pad=0.22", fc=CREAM, ec=INK, lw=1.2))


# ---- Figure 1: observed vs counterfactual around the cliff (1200x630) ----
fig, ax = plt.subplots(figsize=(8, 4.2))
sel = (mid >= 24) & (mid <= 44)
ax.bar(mid[sel], obs[sel], width=0.45, color=TEAL, edgecolor=INK, lw=0.5, zorder=3)
ax.plot(mid[sel], cfv[sel], color=TEAL_DEEP, lw=2.2, ls="--", zorder=4)
ax.axvline(CLIFF, color=INK, lw=1.8, zorder=5)

below = sel & (mid >= CLIFF - 1.5) & (mid < CLIFF)
above = sel & (mid >= CLIFF) & (mid < CLIFF + 1.5)
ax.fill_between(mid[below], obs[below], cfv[below], step=None,
                color=CREAM, ec=INK, lw=0.6, alpha=0.95, zorder=2)
ax.fill_between(mid[above], cfv[above], obs[above], step=None,
                color=TEAL_LIFT, ec=INK, lw=0.6, alpha=0.95, zorder=2)

ax.set_xlim(24, 44)
ax.set_ylim(0, obs[sel].max() * 1.25)
ax.set_xlabel("public support (% of total support)")
ax.set_ylabel("charities")
letter(ax, CLIFF - 2.6, obs[sel].max() * 1.06, "A")   # the line itself
letter(ax, CLIFF - 0.75, obs[sel].max() * 0.42, "B")  # missing mass below
letter(ax, CLIFF + 0.75, obs[sel].max() * 0.42, "C")  # excess mass above
letter(ax, 40.5, obs[sel].max() * 0.92, "D")          # the counterfactual
fig.tight_layout()
fig.savefig(OUT.format("hero"))
plt.close(fig)
print("wrote hero")
```

- [ ] **Step 2: Render and verify exact dimensions**

```bash
cd calcs/public-support-cliff && /opt/homebrew/Caskroom/miniforge/base/envs/qchem/bin/python figures.py && python3 -c "
import struct
size = struct.unpack('>II', open('../../images/2026-07-15-public-support-cliff-hero.png','rb').read()[16:24])
print('size:', size)
assert size == (1200,630), f'MUST be exactly 1200x630, got {size}'
print('ok — exact OG card dimensions')
"
```

Expected: `(1200, 630)` then `ok`. If `tight_layout()` shifts it, drop it for `fig.subplots_adjust(...)`.

- [ ] **Step 3: Look at it**

Open `images/2026-07-15-public-support-cliff-hero.png`. The deficit below the line and the excess above must be *visible* — this figure is the finding. If the shaded regions are too subtle to see at thumbnail size, raise contrast (`TEAL_LIFT` vs `CREAM`) rather than exaggerating the y-range. **Never truncate the y-axis to inflate the effect** — the honest picture is a modest bump, and the placebo test is what makes it credible, not the drama of the chart.

- [ ] **Step 4: Commit**

```bash
git add calcs/public-support-cliff/figures.py images/2026-07-15-public-support-cliff-hero.png
git commit -m "figures: public-support-cliff hero — observed vs counterfactual

The finding in one image: deficit below the 33-1/3 line, excess above, against
the polynomial counterfactual. Exactly 1200x630 (hero + OG card). Y-axis starts
at zero — the effect is modest and the chart must not oversell it.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Figures 2, 3, 4

**Files:**
- Modify: `calcs/public-support-cliff/figures.py` (append)
- Create (generated): `images/2026-07-15-public-support-cliff-{distribution,placebo,concentration}.png`

**Interfaces:**
- Consumes: `mid`/`obs`/`cfv`/`pct`/`pct_excl`/`stats`/`letter()`/palette from Task 3.
- Produces: three PNGs.

**Figure 3 is the credibility figure** — it is what earns the claim. It must show the real estimate against all 21 placebos.

- [ ] **Step 1: Append to figures.py**

```python
# ---- Figure 2: the cliff is invisible to almost everyone ---------------
fig, ax = plt.subplots(figsize=(8, 4.4))
ax.hist(pct, bins=np.arange(0, 102, 2), color=TEAL, edgecolor=INK, lw=0.4)
ax.axvline(CLIFF, color=INK, lw=2.0)
ax.axvline(np.median(pct), color=TEAL_DEEP, lw=1.6, ls="--")
ax.set_xlim(0, 100)
ax.set_xlabel("public support (% of total support)")
ax.set_ylabel("charities")
ymax = ax.get_ylim()[1]
letter(ax, CLIFF, ymax * 0.88, "A")               # the cliff
letter(ax, np.median(pct), ymax * 0.60, "B")      # the median, far away
fig.tight_layout()
fig.savefig(OUT.format("distribution"))
plt.close(fig)
print("wrote distribution")

# ---- Figure 3: placebo — the credibility figure ------------------------
plac = np.array([s for _, s in stats["placebos"]])
thr = np.array([t for t, _ in stats["placebos"]])
real = stats["real_displacement"]

fig, ax = plt.subplots(figsize=(8, 4.4))
ax.axhline(0, color=INK, lw=0.8, zorder=1)
ax.scatter(thr, plac, s=55, color=TEAL, edgecolor=INK, lw=1.0, zorder=3)
ax.scatter([CLIFF], [real], s=190, marker="D", color=TEAL_LIFT,
           edgecolor=INK, lw=1.6, zorder=5)
ax.set_xlabel("threshold tested (% public support)")
ax.set_ylabel("displacement (organizations)")
ax.set_xlim(20, 50)
letter(ax, CLIFF, real + 16, "A")        # the real cliff
letter(ax, 45.5, plac.max() + 16, "B")   # the largest placebo
fig.tight_layout()
fig.savefig(OUT.format("placebo"))
plt.close(fig)
print("wrote placebo")

# ---- Figure 4: donor concentration -------------------------------------
near = (pct > CLIFF - 5) & (pct < CLIFF + 5)
typ = pct >= 80
fig, ax = plt.subplots(figsize=(8, 4.4))
bins = np.arange(0, 102, 4)
ax.hist(pct_excl[typ], bins=bins, color=TEAL, edgecolor=INK, lw=0.4,
        alpha=0.85, density=True, label="typical (support ≥ 80%)")
ax.hist(pct_excl[near], bins=bins, color=TEAL_LIFT, edgecolor=INK, lw=0.4,
        alpha=0.7, density=True, label="near the cliff (±5 points)")
ax.set_xlim(0, 100)
ax.set_xlabel("share of support excluded by the 2% rule (%)")
ax.set_ylabel("density of charities")
ax.legend(frameon=False)
ymax = ax.get_ylim()[1]
letter(ax, 4, ymax * 0.72, "A")     # typical: nothing excluded
letter(ax, 60, ymax * 0.22, "B")    # near-cliff: half excluded
fig.tight_layout()
fig.savefig(OUT.format("concentration"))
plt.close(fig)
print("wrote concentration")
```

- [ ] **Step 2: Render all four**

```bash
cd calcs/public-support-cliff && /opt/homebrew/Caskroom/miniforge/base/envs/qchem/bin/python figures.py && ls -la ../../images/2026-07-15-public-support-cliff-*.png
```

Expected: four PNGs, each > 15 KB.

- [ ] **Step 3: Verify Figure 3 shows what it claims**

```bash
cd calcs/public-support-cliff && python3 -c "
import json, numpy as np
s = json.load(open('stats.json'))
pl = np.array([x for _, x in s['placebos']]); r = s['real_displacement']
print('real', round(r,1), '| placebo max', round(pl.max(),1), '| n >= real:', int((pl>=r).sum()))
assert (pl >= r).sum() == 0, 'a placebo matched the real cliff — the claim fails'
assert r > pl.max(), 'real must exceed every placebo'
print('ok — the real cliff stands clear of all 21 placebos')
"
```

Expected: `n >= real: 0` then `ok`.

- [ ] **Step 4: Look at all four**

Open each. Figure 3 must make the real estimate obviously separate from the placebo cloud without any axis trickery. Figure 2 must show the cliff sitting far from where charities live. Figure 4's two distributions must be distinguishable.

- [ ] **Step 5: Commit**

```bash
git add calcs/public-support-cliff/figures.py images/2026-07-15-public-support-cliff-distribution.png images/2026-07-15-public-support-cliff-placebo.png images/2026-07-15-public-support-cliff-concentration.png
git commit -m "figures: public-support-cliff distribution, placebo, concentration

Figure 3 is the credibility figure: the real +80.1 against all 21 placebo
thresholds, no axis trickery.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Write the post

**Files:**
- Create: `posts/2026-07-15-public-support-cliff.md`
- Reference: the spec (§Structure, §Honesty and inference, §Verified findings), `posts/2026-07-14-nobodys-average.md` (voice)

**Interfaces:**
- Consumes: the four PNGs; all numbers from the spec's §Verified findings (copy them; never recompute by hand).
- Produces: the post. Task 6 builds it.

**Read the spec's §Honesty and inference in full before drafting.** It is the governing standard and it is not optional.

- [ ] **Step 1: Verify the legal claims before writing them**

The post makes claims about the support test, reclassification, the 2% rule, and the facts-and-circumstances test. **Do not write these from memory.** Check each against an IRS source and carry an inline link:

- [IRS Publication 557](https://www.irs.gov/publications/p557)
- [Public charity support tests / Schedules A and B](https://www.irs.gov/charities-non-profits/exempt-organizations-annual-reporting-requirements-form-990-schedules-a-and-b-public-charity-support-test)

If a claim cannot be sourced, **cut it** — the finding does not depend on any of them. Prefer "risks being reclassified" over a precise mechanism you cannot cite.

- [ ] **Step 2: Write the frontmatter**

```yaml
---
title: "One-third: the cliff a few hundred charities steer around"
date: 2026-07-15
tags: nonprofits, data
description: "There is a bright line in the tax code: draw less than a third of your support from the public and you risk ceasing to be a public charity. Almost no charity can see it — the median sits at 96 percent. But among the few hundred close enough to see it, the distribution bends, and it bends at the number they can compute."
og-image: /images/2026-07-15-public-support-cliff-hero.png
---
```

No `author` field. Title quoted (contains a colon).

- [ ] **Step 3: Draft the seven sections**

Per spec §Structure:

1. **The rule** — the bright line, sourced and linked.
2. **Almost nobody can see it** — median 95.7%; 3.86% below; 670 within 1.5 points. Figure 2.
3. **It isn't about being unpopular — it's the 2% rule** — the payoff. 53.9% vs 0.0% excluded; correlation −0.744; near-cliff orgs are *not* smaller (revenue $387,204 vs $662,907, and they hold *more* assets). Table 1, Figure 4.
4. **Do they steer?** — the estimator explained plainly; missing below (−15.5%), excess above (+7.8%). Figure 1, Code 1. Show bw/degree/window and say they were frozen before the placebo test.

   **Two method facts that belong in the prose here, not in a footnote:**

   - **The ratio is a five-year measure, not an annual one.** Total support spans the Schedule A Part II measuring period — it runs a median **3.70×** a single year's revenue. So the quantity that bends is a *five-year aggregate*, which is considerably harder to nudge than one year's books. This makes the displacement **more** notable, not less, and the reader deserves to know it rather than assuming we found charities tweaking a single year.
   - **The population restriction bought nothing, and say so.** Limiting to `nonpfrea == 7` (the orgs the rule actually binds) barely moves the estimate versus all 501(c)(3)s with a computable ratio (111,991 of 116,894), because the §170 support fields are only populated by organizations using that test. Restrict anyway — it is the right population — but **do not claim the restriction sharpened anything.** It didn't, and an earlier version of this analysis wrongly expected it would.
5. **Is it real?** — placebo 0/21, z = +3.77, bootstrap [+28, +129], 12 specs +47 to +95 (Table 2). Figure 3. **Link the downloadable script here.**
6. **How big? Depends what you divide by** — 80 orgs: 0.072% of all, ~12% of the 670. Cross-link [nobody's average](/posts/2026-07-14-nobodys-average.html).
7. **What this does and does not show** — the 10% null; the inference (response at the computable line, undetectable at the discretionary one); the limit (four mechanisms, indistinguishable here); what would resolve it (panel data, Schedule B). Close + caveat.

Code 1 (section 4) — show the choices, don't bury them:

````markdown
```python
# Frozen before the placebo test: 0.5-point bins, degree-5 fit, ±1.5-point window.
BW, DEG, W = 0.5, 5, 1.5

# Counterfactual: fit the density OUTSIDE a window around the line, then ask
# what the window would have held if the line weren't there.
excl = (mid > CLIFF - W) & (mid < CLIFF + W)
cf = np.polyval(np.polyfit(mid[~excl], cnt[~excl], DEG), mid)

displacement = (observed_above - cf_above) + (cf_below - observed_below)
```

**Code 1.** The estimator, with its three arbitrary choices made in public: bin width, polynomial degree, and window. The [full script](/calcs/public-support-cliff/compute.py) is downloadable, and Table 2 reports what happens when the first two are changed.
````

Table 2 (section 5) is the 12-cell grid **including the coarse bins that attenuate the estimate to +47**. Do not report only the favourable cells — publishing the whole pile is the point.

**The mechanism paragraph in section 7 is the hardest thing in this post.** It must state the inference the analysis licenses and its limit in the same breath, accuse no one, and leave the reader to decide. Neither "they're gaming it" nor "it's the rule working as designed" is supported.

- [ ] **Step 4: Check the honesty constraints**

```bash
grep -niE "\b(gam(e|ing|ed)|dodg|cook(ing|ed)?|cheat|fraud|evad|abus)" posts/2026-07-15-public-support-cliff.md
```

Expected: **no output**, or only hits inside an explicit disclaimer of that reading. Any sentence asserting a mechanism — accusatory *or* benign — violates Global Constraints. Also check by eye that "working as designed" and equivalents do not appear as claims.

- [ ] **Step 5: Check the conventions**

```bash
python3 - <<'PY'
import re, pathlib
t = pathlib.Path("posts/2026-07-15-public-support-cliff.md").read_text()
body = t.split("---", 2)[2]
figs = re.findall(r'\*\*Figure (\d+)\.\*\*', body)
tabs = re.findall(r'\*\*Table (\d+)\.\*\*', body)
code = re.findall(r'\*\*Code (\d+)\.\*\*', body)
print("figures:", figs, "tables:", tabs, "code:", code)
for kind, ns in (("Figure", figs), ("Table", tabs), ("Code", code)):
    for n in ns:
        assert re.search(rf'{kind} {n}\b', body.replace(f'**{kind} {n}.**','')), f"{kind} {n} never referenced in prose"
assert figs == ['1','2','3','4'], f"expected Figures 1-4, got {figs}"
assert tabs == ['1','2'], f"expected Tables 1-2, got {tabs}"
assert "/calcs/public-support-cliff/compute.py" in body, "post must link the downloadable script"
assert not re.search(r'\[@\w+\]', body), "Pandoc citation found"
assert not re.search(r'\[\^\d+\]', body), "footnote found"
assert not re.search(r'https://blog\.noprofits\.org', body), "absolute self-link"
assert not re.search(r'^author:', t, re.M), "author field present"
assert not re.search(r'^# ', body, re.M), "in-body H1"
assert 'irs.gov' in body, "no IRS source linked for the legal claims"
print("ok — conventions pass")
PY
```

Expected: `ok — conventions pass`.

- [ ] **Step 6: Commit**

```bash
git add posts/2026-07-15-public-support-cliff.md
git commit -m "post: one-third — the cliff a few hundred charities steer around

Fifth in the 990 data series. Displacement of ~80 organizations across the
33-1/3% public support line: placebo z=+3.77, 0 of 21 fake thresholds match,
bootstrap CI excludes zero, all 12 specifications positive. The payoff is the
2% rule — near-cliff charities have 53.9% of their support excluded vs 0.0%
for typical ones, so the test measures breadth, not amount.

States the inference and its limit together: the response sits at the
computable threshold and is undetectable at the discretionary one, consistent
with deliberate management of a calculable number — but four mechanisms
produce that signature and this data separates none of them. No accusation.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Build, verify, PR

**Files:** none new.

**Interfaces:**
- Consumes: everything above.
- Produces: a PR into `main`.

- [ ] **Step 1: Build**

```bash
stack build && stack exec blog build 2>&1 | tail -3
```

Expected: `Success`. A YAML error aborts the build and names the file — check title quoting first.

- [ ] **Step 2: Verify the rendered page and the published code**

```bash
python3 - <<'PY'
import pathlib
p = list(pathlib.Path("_site/posts").glob("*public-support-cliff*"))
assert p, "post did not render"
h = p[0].read_text()
for n in ("hero", "distribution", "placebo", "concentration"):
    assert f"2026-07-15-public-support-cliff-{n}.png" in h, f"{n} figure missing"
assert "og:image" in h and "public-support-cliff-hero.png" in h, "OG meta wrong"
assert h.count("<figure") == 4, f"expected 4 figures, got {h.count('<figure')}"
assert h.count("<table") >= 2, "expected Tables 1 and 2 to render"
assert "**Figure" not in h, "raw markdown caption leaked"
assert "/calcs/public-support-cliff/compute.py" in h, "script link missing from rendered page"
print("ok — page, figures, tables, OG card, script link")
PY
echo "--- published code ---"; find _site/calcs -name '*.py' | sort
echo "--- MUST be empty ---"; find _site/calcs \( -name '*.csv' -o -name '*.csv.gz' \) -print
```

Expected: `ok`; the cliff scripts listed; the data check prints nothing.

- [ ] **Step 3: Look at the page, and click the code link**

```bash
cd _site && (python3 -m http.server 8899 >/dev/null 2>&1 &) ; sleep 1
curl -s -o /dev/null -w "post   -> %{http_code}\n" http://localhost:8899/posts/2026-07-15-public-support-cliff.html
curl -s -o /dev/null -w "script -> %{http_code}\n" http://localhost:8899/calcs/public-support-cliff/compute.py
```

Then open `http://localhost:8899/posts/2026-07-15-public-support-cliff.html` in a browser. Check: figures load; captions numbered below their figures; **Tables 1 and 2 render as tables**; **Code 1 does not overflow its container** (the last post shipped that bug past a green build — look at it); the script link resolves. Kill the server when done: `pkill -f "http.server 8899"`.

- [ ] **Step 4: Push and open the PR**

```bash
git push -u origin post/public-support-cliff
gh pr create --base main --title "Add post: one-third — the cliff a few hundred charities steer around" --body "$(cat <<'EOF'
Fifth post in the Form 990 data series, after nobody's average.

**The finding.** Charities relying on the §170(b)(1)(A)(vi) support test must
draw a third of their support from the public. The distribution of that ratio
shows a deficit just below the line and an excess just above — a displacement
of ~80 organizations.

**Why it's credible.** Placebo test at 21 fake thresholds: real z=+3.77, and
0 of 21 placebos reach it (largest +35.0 vs real +80.1). Bootstrap 95% CI
[+28, +129], 0/400 resamples ≤ 0. All 12 bandwidth/degree specifications
positive (+47 to +95) — Table 2 in the post publishes the whole grid, including
the coarse bins that attenuate it.

**The payoff.** The 2% rule: any one donor's support above 2% of the total
doesn't count toward the public's share. Near-cliff charities have 53.9% of
their support excluded against 0.0% for typical ones (corr −0.744), and they
are *not* smaller. They're narrowly funded. The test measures breadth, not
amount.

**What it does not show.** The mechanism. Donor-broadening, classification
judgment, timing across the five-year window, and misreporting all produce this
signature, and one year of as-filed aggregates separates none of them. The post
states that alongside the finding and makes no accusation.

**Reproducibility.** The analysis script is published for download at
/calcs/public-support-cliff/compute.py (new Hakyll rule, scoped to `calcs/*/*.py`
so it cannot publish the 247MB extract). It asserts every number in the post and
pins the bootstrap seed so a reader reproduces the CI.

Spec: `docs/superpowers/specs/2026-07-15-public-support-cliff-design.md`
Plan: `docs/superpowers/plans/2026-07-15-public-support-cliff.md`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 5: Report the PR URL to Peter. Do not merge** — merging deploys to the live blog.

---

## Notes for the executor

- **The spec outranks you on numbers, and the specification is frozen.** bw=0.5, degree=5, W=1.5 were fixed before the placebo test. If you find a specification that produces a bigger number, that is not an improvement — it is p-hacking, and the placebo test's credibility depends on not doing it.
- **Two numbers that look wrong but aren't:** the 10% floor's displacement is *positive* (+44.6) and still a null, because placebos at 5% and 6% are just as large. And coarse bins (bw=1.0) attenuate the estimate to ~+47 — that is expected when a 1.5-point window is smeared across 1-point bins, not instability.
- **The hardest paragraph is the mechanism one in section 7.** Both the accusatory reading and the comfortable one are unsupported. State the displacement, state the inference the bright-line/judgment-call contrast licenses, state that four mechanisms produce it and this data separates none, name what would (panel data, Schedule B), stop.
- **The code is part of the argument now.** It ships at a public URL. It must run standalone, assert its own numbers, and explain its choices in its docstring.
