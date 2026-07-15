# Nobody's Average — Blog Post Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the fourth post in the blog's Form 990 data series — "Nobody's average: who actually pays for the nonprofit sector" — with a reproducible compute script, four figures, one table, and a merged PR.

**Architecture:** Three artifacts in the established sibling pattern. `calcs/who-pays/compute.py` reads the IRS extract, reproduces every number in the approved spec, **asserts each one against the spec value**, and writes gzipped intermediates. `calcs/who-pays/figures.py` reads the intermediates and writes four PNGs. `posts/2026-07-14-nobodys-average.md` is the prose. The assertions in `compute.py` are this plan's test suite: the spec's verified findings are the expected values, so a script that drifts fails loudly instead of quietly publishing wrong numbers.

**Tech Stack:** Python 3 (pandas, numpy, matplotlib), Hakyll + Stack for the site build, `gh` for the PR.

## Global Constraints

Copied verbatim from the spec and `notes/blog-authoring.md`. Every task's requirements implicitly include this section.

- **Spec is authoritative on numbers.** `docs/superpowers/specs/2026-07-14-nobodys-average-design.md` §Verified findings holds values confirmed against the data during design. If a script disagrees with the spec, **the script is wrong** — do not edit the spec to match the script. Escalate to Peter instead.
- **Data source:** `calcs/data/24eoextract990.csv` — IRS SOI annual extract, returns filed CY2024, 345,365 rows. Read-only. Never modify.
- **Two populations, never conflated.** `POP_REV` = 249,668 orgs (`subseccd == 3` and `totrevenue > 0`). `POP_MIX` = 242,348 orgs (`POP_REV` further restricted to contribution share in [0, 100]). Aggregate dollar shares and concentration use `POP_REV`. Three-groups, deciles, `nonpfrea`, and top-1% use `POP_MIX`. The reserve/inverted-U population is `POP_RESERVE` = 195,437.
- **Frontmatter:** `tags: nonprofits, data`. **No `author` field** — the nonprofit series renders without a byline. `og-image` set to the hero. Title contains a colon, so it **must be double-quoted**.
- **Citations:** inline markdown hyperlinks only. **No `[@key]`, no reference list, no footnotes.** Nothing appended to `bib/bibliography.bib`.
- **Links:** site-relative (`/posts/...`), never absolute.
- **Voice:** prose over bullet lists. `##` headers. Bold key terms on first use. No in-body H1, byline, or tags line. End with the series' one-line reader caveat.
- **Captions:** every figure, table, and code block gets a **bold** numbered caption (`**Figure 1.**`, `**Table 1.**`, `**Code 1.**`) as a full sentence, and every one is referenced by number in the prose.
- **Figure text:** lettered callouts only (A, B, C…), defined in the caption. Axis labels, ticks, and legend entries are the only other text allowed in the plot area.
- **Palette:** ink `#143f33`, teal `#2f7da3`, lifted `#5b9fc0`, deep `#1c5572`, cream `#f7f1d7`, page `#f7f4ee`.
- **Three forbidden claims** (spec §Open risks) — these are factual errors, not simplifications:
  1. Never "not a bell curve, therefore not one population." Skew is not mixture evidence.
  2. Never imply the fee/donation piles differ by **size**. Median revenue differs by 1.3× ($614,855 vs $491,463). The split is **business model**.
  3. Never "the IRS already sorts charities into these groups." `nonpfrea` records which test an org **qualifies under**, not how it is **actually funded** (code 09 median is 42.2%, not ~0). It is a strong signal, not a clean partition.
- **Branch:** `post/nobodys-average` (already exists, holds the spec commits). Never commit to `main`.

## File Structure

| File | Responsibility |
| --- | --- |
| `calcs/who-pays/compute.py` | Load extract, build both populations, reproduce + **assert** every spec number, write intermediates. Owns all arithmetic. |
| `calcs/who-pays/mix.csv.gz` | Per-org intermediate (generated): `cs`, `totrevenue`, `npr`, `dec`, `honest`, `band`. |
| `calcs/who-pays/agg.json` | Aggregate dollar totals (generated) — the four revenue categories. |
| `calcs/who-pays/figures.py` | Read intermediates, write four PNGs. Owns all rendering. No arithmetic beyond binning. |
| `posts/2026-07-14-nobodys-average.md` | The prose. |
| `images/2026-07-14-nobodys-average-*.png` | Four figures (generated). |

Arithmetic lives only in `compute.py`; rendering only in `figures.py`. This matches `calcs/below-zero/` and keeps a figure tweak from silently changing a number.

---

### Task 1: compute.py — arithmetic and spec assertions

**Files:**
- Create: `calcs/who-pays/compute.py`
- Create (generated): `calcs/who-pays/mix.csv.gz`, `calcs/who-pays/agg.json`
- Reference: `calcs/below-zero/compute.py` (sibling style), `docs/superpowers/specs/2026-07-14-nobodys-average-design.md`

**Interfaces:**
- Consumes: `calcs/data/24eoextract990.csv`.
- Produces: `mix.csv.gz` with columns `cs` (contribution share, float 0–100), `totrevenue` (float), `npr` (float `nonpfrea` code, `nan` if unparseable), `dec` (int 0–9 revenue decile within `POP_MIX`), `honest` (float honest reserve months, `nan` where the FASB reconciliation fails), `band` (str, one of `0-10`/`10-25`/`25-50`/`50-75`/`75-90`/`90-100`, `nan` where `honest` is). `agg.json` with keys `n_pop_rev`, `total_revenue`, `contrib`, `prgm`, `invst`, `residual`. Task 2 and Task 3 read exactly these names.

- [ ] **Step 1: Write compute.py with the assertions as the test**

The `check()` calls ARE the failing test — they encode the spec's verified findings. Write the file complete:

```python
#!/usr/bin/env python3
"""Who actually pays for the nonprofit sector — revenue mix across the census.

Supports posts/2026-07-14-nobodys-average.md. Every printed number is asserted
against docs/superpowers/specs/2026-07-14-nobodys-average-design.md. If an
assertion fires, THIS SCRIPT is wrong, not the spec.

Data: ../data/24eoextract990.csv (IRS SOI annual extract, returns filed CY2024)
https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data

Two populations, deliberately distinct:
  POP_REV (249,668) = subseccd==3 & totrevenue>0.  Aggregate dollar shares and
                      concentration are computed here.
  POP_MIX (242,348) = POP_REV & contribution share in [0,100].  Three groups,
                      deciles, nonpfrea, and the top 1% are computed here.
  POP_RESERVE (195,437) = POP_REV & FASB reconciliation & cashexp>0.  The
                      inverted U only.

The [0,100] restriction drops ~7,320 orgs whose offsetting negative revenue
lines (investment losses, net rental/sales losses) push the ratio out of range.
"""

import json
import numpy as np
import pandas as pd

SRC = "../data/24eoextract990.csv"

COLS = ["EIN", "tax_pd", "subseccd", "totrevenue", "totcntrbgfts",
        "totprgmrevnue", "invstmntinc", "totfuncexpns", "deprcatndepletn",
        "unrstrctnetasstsend", "temprstrctnetasstsend", "permrstrctnetasstsend",
        "lndbldgsequipend", "secrdmrtgsend", "totnetassetend", "totassetsend",
        "nonpfrea", "operatehosptlcd", "operateschools170cd"]

FAILURES = []


def check(label, got, want, tol):
    """Assert a computed value against the spec. Collect, don't abort, so one
    run reports every drift at once."""
    ok = abs(got - want) <= tol
    print(f"  {'ok  ' if ok else 'FAIL'} {label:52s} got {got:>16,.2f}   spec {want:>16,.2f}")
    if not ok:
        FAILURES.append(f"{label}: got {got:,.4f}, spec says {want:,.4f}")


df = pd.read_csv(SRC, usecols=COLS)
df = df.sort_values("tax_pd").drop_duplicates("EIN", keep="last")

# ---- POP_REV: aggregate dollars and concentration ----------------------
rev = df[(df.subseccd == 3) & (df.totrevenue > 0)].copy()
for c in ("totcntrbgfts", "totprgmrevnue", "invstmntinc"):
    rev[c] = rev[c].fillna(0)

TOT = rev.totrevenue.sum()
contrib, prgm, invst = rev.totcntrbgfts.sum(), rev.totprgmrevnue.sum(), rev.invstmntinc.sum()
residual = TOT - contrib - prgm - invst

print("\nPOP_REV — aggregate, dollar-weighted")
check("n POP_REV", len(rev), 249_668, 0)
check("total revenue $B", TOT / 1e9, 3096.4, 0.5)
check("contributions $B", contrib / 1e9, 754.2, 0.5)
check("contributions % of revenue", contrib / TOT * 100, 24.36, 0.05)
check("program service $B", prgm / 1e9, 2155.2, 0.5)
check("program service % of revenue", prgm / TOT * 100, 69.61, 0.05)
check("investment income $B", invst / 1e9, 73.8, 0.5)
check("investment % of revenue", invst / TOT * 100, 2.38, 0.05)
check("residual $B", residual / 1e9, 113.1, 0.5)
check("residual % of revenue", residual / TOT * 100, 3.65, 0.05)

srt = rev.sort_values("totrevenue")
print("\nPOP_REV — concentration")
check("top 1% share of revenue", srt.totrevenue.tail(len(srt) // 100).sum() / TOT * 100, 69.1, 0.15)
check("top 10% share of revenue", srt.totrevenue.tail(len(srt) // 10).sum() / TOT * 100, 91.8, 0.15)
check("bottom 50% share of revenue", srt.totrevenue.head(len(srt) // 2).sum() / TOT * 100, 0.94, 0.05)

# ---- POP_MIX: per-org distribution -------------------------------------
rev["cs"] = rev.totcntrbgfts / rev.totrevenue * 100
mix = rev[rev.cs.between(0, 100)].copy()
MIXTOT = mix.totrevenue.sum()          # NB: POP_MIX's own revenue, not TOT

print("\nPOP_MIX — per-organization")
check("n POP_MIX", len(mix), 242_348, 0)
check("mean contribution share", mix.cs.mean(), 56.0, 0.1)
check("median contribution share", mix.cs.median(), 65.1, 0.1)
check("p25 contribution share", mix.cs.quantile(.25), 12.5, 0.1)
check("p75 contribution share", mix.cs.quantile(.75), 96.6, 0.1)
check("% >=90 donation-funded", (mix.cs >= 90).mean() * 100, 33.7, 0.1)
check("% <=10 fee-funded", (mix.cs <= 10).mean() * 100, 23.4, 0.1)
check("exactly 0% contributions", (mix.cs == 0).sum(), 26_657, 0)
check("exactly 100% contributions", (mix.cs >= 99.999).sum(), 25_366, 0)

fee, don, mid = mix[mix.cs <= 10], mix[mix.cs >= 90], mix[mix.cs.between(10, 90)]
print("\nPOP_MIX — three groups (revenue shares are WITHIN POP_MIX)")
check("fee n", len(fee), 56_619, 0)
check("don n", len(don), 81_739, 0)
check("mid n", len(mid), 103_990, 0)
check("fee % of orgs", len(fee) / len(mix) * 100, 23.4, 0.1)
check("don % of orgs", len(don) / len(mix) * 100, 33.7, 0.1)
check("mid % of orgs", len(mid) / len(mix) * 100, 42.9, 0.1)
check("fee % of POP_MIX revenue", fee.totrevenue.sum() / MIXTOT * 100, 61.5, 0.15)
check("don % of POP_MIX revenue", don.totrevenue.sum() / MIXTOT * 100, 12.5, 0.15)
check("mid % of POP_MIX revenue", mid.totrevenue.sum() / MIXTOT * 100, 25.9, 0.15)
check("fee median revenue", fee.totrevenue.median(), 614_855, 1)
check("don median revenue", don.totrevenue.median(), 491_463, 1)
check("mid median revenue", mid.totrevenue.median(), 569_737, 1)
check("fee mean revenue", fee.totrevenue.mean(), 33_412_128, 5000)
check("don mean revenue", don.totrevenue.mean(), 4_707_484, 5000)
check("fee median assets", fee.totassetsend.median(), 1_251_203, 1)
check("don median assets", don.totassetsend.median(), 512_764, 1)
check("MECHANISM: fee:don median revenue ratio", fee.totrevenue.median() / don.totrevenue.median(), 1.25, 0.05)

# ---- POP_MIX: deciles ---------------------------------------------------
mix["dec"] = pd.qcut(mix.totrevenue, 10, labels=False)
dec_med = mix.groupby("dec").cs.median()
print("\nPOP_MIX — deciles (flat 1-9, cliff at 10)")
for i, want in enumerate([55.3, 63.0, 73.7, 73.3, 70.2, 71.1, 70.2, 69.9, 65.8, 23.4]):
    check(f"decile {i+1} median contribution share", dec_med.loc[i], want, 0.15)

top1 = mix.nlargest(int(len(mix) * 0.01), "totrevenue")
check("top 1% n", len(top1), 2_423, 0)
check("top 1% median contribution share", top1.cs.median(), 2.0, 0.15)
check("top 1% % fee-funded", (top1.cs <= 10).mean() * 100, 68.9, 0.2)

# ---- POP_MIX: nonpfrea --------------------------------------------------
mix["npr"] = pd.to_numeric(mix.nonpfrea, errors="coerce")
print("\nPOP_MIX — nonpfrea (the distinction already in the file)")
for code, n_want, med_want in [(7, 107_177, 87.0), (9, 92_654, 42.2), (2, 15_473, 17.4),
                               (12, 8_487, 4.0), (1, 4_638, 99.7), (3, 3_546, 1.4),
                               (13, 2_402, 1.2), (14, 2_279, 5.0), (8, 1_692, 80.4),
                               (15, 1_449, 0.0), (6, 1_430, 73.4)]:
    g = mix[mix.npr == code]
    check(f"nonpfrea {code:>2} n", len(g), n_want, 0)
    check(f"nonpfrea {code:>2} median contribution share", g.cs.median(), med_want, 0.15)

hosp = mix[mix.operatehosptlcd == "Y"]
sch = mix[mix.operateschools170cd == "Y"]
check("hospital-flag n", len(hosp), 2_235, 0)
check("hospital-flag median contribution share", hosp.cs.median(), 1.1, 0.15)
check("school-flag n", len(sch), 15_187, 0)
check("school-flag median contribution share", sch.cs.median(), 17.6, 0.15)

# ---- POP_RESERVE: the inverted U ---------------------------------------
fasb = (df.unrstrctnetasstsend + df.temprstrctnetasstsend
        + df.permrstrctnetasstsend - df.totnetassetend).abs() <= 1000
d2 = df[(df.subseccd == 3) & (df.totrevenue > 0)].copy()
d2["cashexp"] = d2.totfuncexpns - d2.deprcatndepletn
d2 = d2[fasb.reindex(d2.index).fillna(False) & (d2.cashexp > 0)].copy()
d2["honest"] = (d2.unrstrctnetasstsend - d2.lndbldgsequipend
                + d2.secrdmrtgsend) / (d2.cashexp / 12.0)
d2["cs"] = d2.totcntrbgfts.fillna(0) / d2.totrevenue * 100
res = d2[d2.cs.between(0, 100)].copy()

# Bands MUST be built with pd.cut exactly as below. pd.cut is RIGHT-closed:
# include_lowest makes the first interval [0,10] and the rest (10,25], (25,50]…
# The spec's band counts were produced this way. A hand-rolled
# `(cs >= lo) & (cs < hi)` is LEFT-closed, lands orgs at the boundaries in the
# wrong band, and will fail these assertions. Do not "simplify" it.
BINS = [0, 10, 25, 50, 75, 90, 100.01]
LABS = ["0-10", "10-25", "25-50", "50-75", "75-90", "90-100"]
res["band"] = pd.cut(res.cs, bins=BINS, labels=LABS, include_lowest=True)

WANT = [("0-10", 43_898, 5.18, 21.5), ("10-25", 16_345, 5.83, 14.9),
        ("25-50", 21_943, 7.38, 12.7), ("50-75", 26_060, 8.90, 11.8),
        ("75-90", 22_350, 9.48, 9.4), ("90-100", 64_841, 5.37, 12.1)]
print("\nPOP_RESERVE — the inverted U")
check("n POP_RESERVE", len(res), 195_437, 0)
for lab, n_want, med_want, bz_want in WANT:
    g = res[res.band == lab]
    check(f"band {lab} n", len(g), n_want, 0)
    check(f"band {lab} median honest months", g.honest.median(), med_want, 0.03)
    check(f"band {lab} % below zero", (g.honest <= 0).mean() * 100, bz_want, 0.1)

# ---- write intermediates ------------------------------------------------
# `band` is written here, not recomputed in figures.py — arithmetic lives in
# exactly one file, so a figure tweak can never move a number.
out = mix[["EIN", "cs", "totrevenue", "npr", "dec"]].copy()
out = out.merge(res[["EIN", "honest", "band"]], on="EIN", how="left")
out = out[["cs", "totrevenue", "npr", "dec", "honest", "band"]]
out.to_csv("mix.csv.gz", index=False, compression="gzip")

with open("agg.json", "w") as f:
    json.dump({"n_pop_rev": int(len(rev)), "total_revenue": float(TOT),
               "contrib": float(contrib), "prgm": float(prgm),
               "invst": float(invst), "residual": float(residual)}, f, indent=2)

print(f"\nwrote mix.csv.gz ({len(out):,} rows) and agg.json")
if FAILURES:
    print(f"\n{len(FAILURES)} SPEC MISMATCH(ES) — the script is wrong, not the spec:")
    for f_ in FAILURES:
        print("  " + f_)
    raise SystemExit(1)
print("\nall spec assertions passed")
```

- [ ] **Step 2: Run it and read every line**

```bash
cd calcs/who-pays && python3 compute.py
```

Expected: every line prefixed `ok`, ending `all spec assertions passed`, exit 0. Takes ~60–90s (247 MB CSV).

**If any assertion FAILS:** the spec is authoritative. Debug the script. Do NOT edit the spec's numbers. The likely culprits, in order: (a) wrong population — check `POP_REV` vs `POP_MIX` vs `POP_RESERVE` denominators; (b) a missing `.fillna(0)`; (c) the FASB `reindex` alignment in the `POP_RESERVE` block. If the script looks right and the number still differs, stop and escalate to Peter — a real data discrepancy is a finding, not a bug to paper over.

- [ ] **Step 3: Verify the intermediates**

```bash
cd calcs/who-pays && python3 -c "
import pandas as pd, json
m = pd.read_csv('mix.csv.gz')
print('rows:', len(m), '(expect 242,348)')
print('cols:', list(m.columns))
print('honest non-null:', m.honest.notna().sum(), '(expect ~195,437)')
print('npr non-null:', m.npr.notna().sum())
print(json.load(open('agg.json')))
"
```

Expected: 242348 rows; columns `['cs','totrevenue','npr','dec','honest']`; `honest` non-null ≈ 195,437.

- [ ] **Step 4: Commit**

```bash
git add calcs/who-pays/compute.py
git commit -m "calcs: who-pays compute script, asserted against the spec

Reproduces every verified finding in the nobodys-average spec and asserts
each one, so drift fails loudly instead of publishing a wrong number.
Keeps POP_REV / POP_MIX / POP_RESERVE denominators distinct.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

Note: `mix.csv.gz` and `agg.json` are generated. Check whether `calcs/below-zero/*.csv.gz` is tracked (`git ls-files calcs/below-zero`) and match that convention — the siblings track theirs, so track these too if so.

---

### Task 2: figures.py scaffold + Figure 1 (hero / OG card)

**Files:**
- Create: `calcs/who-pays/figures.py`
- Create (generated): `images/2026-07-14-nobodys-average-hero.png`
- Reference: `calcs/below-zero/figures.py`

**Interfaces:**
- Consumes: `mix.csv.gz` (`cs`, `totrevenue`, `npr`, `dec`, `honest`, `band`), `agg.json` (`total_revenue`, `contrib`, `prgm`, `invst`, `residual`) from Task 1.
- Produces: the module-level palette constants and `PAGE`/`INK`/`TEAL`/`TEAL_LIFT`/`TEAL_DEEP`/`CREAM` plus the loaded `mix` DataFrame and `agg` dict, reused by Task 3's figures in the same file.

**Hard constraint:** Figure 1 must be **exactly 1200×630** — it is both the in-post hero and the OG/Twitter card. At 150 dpi that is `figsize=(8, 4.2)`.

- [ ] **Step 1: Write figures.py with the scaffold and Figure 1**

```python
#!/usr/bin/env python3
"""Data figures for the nobodys-average post. Brand palette, lettered callouts
only — captions carry the words (notes/blog-authoring.md §5).

Reads mix.csv.gz + agg.json (written by compute.py). Writes:
  images/2026-07-14-nobodys-average-hero.png        Figure 1 (1200x630 hero/OG)
  images/2026-07-14-nobodys-average-bimodal.png     Figure 2
  images/2026-07-14-nobodys-average-by-size.png     Figure 3
  images/2026-07-14-nobodys-average-inverted-u.png  Figure 4
"""

import json
import numpy as np
import pandas as pd
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

OUT = "../../images/2026-07-14-nobodys-average-{}.png"
mix = pd.read_csv("mix.csv.gz")
agg = json.load(open("agg.json"))


def letter(ax, x, y, s):
    """Bold lettered callout — the only prose allowed in a plot area."""
    ax.text(x, y, s, fontsize=13, fontweight="bold", color=INK,
            ha="center", va="center", zorder=10,
            bbox=dict(boxstyle="circle,pad=0.22", fc=CREAM, ec=INK, lw=1.2))


# ---- Figure 1: the two answers, side by side (1200x630 hero/OG) ---------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.2))

# Left: dollar-weighted. One stacked bar, the whole sector's money.
T = agg["total_revenue"]
parts = [("contrib", agg["contrib"], TEAL_DEEP), ("prgm", agg["prgm"], TEAL),
         ("invst", agg["invst"], TEAL_LIFT), ("residual", agg["residual"], CREAM)]
left = 0.0
for _, val, color in parts:
    ax1.barh([0], [val / T * 100], left=left, color=color, edgecolor=INK, lw=1.0, height=0.55)
    left += val / T * 100
ax1.set_xlim(0, 100)
ax1.set_ylim(-0.6, 0.6)
ax1.set_yticks([])
ax1.set_xlabel("percent of sector revenue")
letter(ax1, agg["contrib"] / T * 100 / 2, 0, "A")
letter(ax1, (agg["contrib"] + agg["prgm"] / 2) / T * 100, 0, "B")
ax1.spines["left"].set_visible(False)

# Right: org-weighted. The distribution of the same ratio, per charity.
ax2.hist(mix.cs, bins=np.arange(0, 102, 2), color=TEAL, edgecolor=INK, lw=0.4)
ax2.axvline(mix.cs.median(), color=INK, lw=1.6, ls="--")
ax2.set_xlim(0, 100)
ax2.set_xlabel("contribution share of one charity's revenue (%)")
ax2.set_ylabel("charities")
letter(ax2, 4, ax2.get_ylim()[1] * 0.72, "C")
letter(ax2, 96, ax2.get_ylim()[1] * 0.72, "D")
letter(ax2, mix.cs.median(), ax2.get_ylim()[1] * 0.93, "E")

fig.tight_layout()
fig.savefig(OUT.format("hero"))
plt.close(fig)
print("wrote hero")
```

- [ ] **Step 2: Run it and verify the exact pixel dimensions**

```bash
cd calcs/who-pays && python3 figures.py && python3 -c "
from PIL import Image
im = Image.open('../../images/2026-07-14-nobodys-average-hero.png')
print('size:', im.size)
assert im.size == (1200, 630), f'MUST be exactly 1200x630, got {im.size}'
print('ok — exact OG card dimensions')
"
```

Expected: `size: (1200, 630)` then `ok`. If `tight_layout()` shifts the size, drop it and use `fig.subplots_adjust(...)` instead — `figsize` × `dpi` must land exactly.

If PIL is unavailable, use `python3 -c "import struct;d=open('../../images/2026-07-14-nobodys-average-hero.png','rb').read()[16:24];print(struct.unpack('>II',d))"`.

- [ ] **Step 3: Look at the figure**

Open `images/2026-07-14-nobodys-average-hero.png`. Check: both panels legible at thumbnail size; the left bar reads as one sector's money, the right as a bimodal spread; no text in the plot area except axis labels and the A–E callouts.

**Spec §Open risks names this exact failure:** if two panels cannot be made legible in one 1200×630 frame, the fallback is a single-panel hero on the bimodal distribution, with the dollar/org split moved to Figure 2. Try two-panel first — the divergence *is* the post — but take the fallback rather than shipping an unreadable card, and tell Peter if you do.

- [ ] **Step 4: Commit**

```bash
git add calcs/who-pays/figures.py images/2026-07-14-nobodys-average-hero.png
git commit -m "figures: nobodys-average hero — the two answers side by side

Dollar-weighted sector revenue against the org-weighted distribution of the
same ratio. Exactly 1200x630, so it serves as both hero and OG card.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Figures 2, 3, 4

**Files:**
- Modify: `calcs/who-pays/figures.py` (append)
- Create (generated): `images/2026-07-14-nobodys-average-{bimodal,by-size,inverted-u}.png`

**Interfaces:**
- Consumes: `mix`, `agg`, `letter()`, palette constants from Task 2.
- Produces: three PNGs. No later task depends on their internals.

**Figure 3 is the post's most important figure** (spec §Figures). The flat run across deciles 1–9 matters as much as the cliff at 10, so **the y-axis must start at 0 and must not be scaled to hide the flatness**.

- [ ] **Step 1: Append the three figures to figures.py**

```python
# ---- Figure 2: the bimodal distribution --------------------------------
fig, ax = plt.subplots(figsize=(8, 4.4))
ax.hist(mix.cs, bins=np.arange(0, 102, 2), color=TEAL, edgecolor=INK, lw=0.4)
ax.axvline(mix.cs.mean(), color=INK, lw=1.6, ls="--")
ax.set_xlim(0, 100)
ax.set_xlabel("contribution share of revenue (%)")
ax.set_ylabel("charities")
ymax = ax.get_ylim()[1]
letter(ax, 3, ymax * 0.80, "A")          # the exact-zero pile
letter(ax, 97, ymax * 0.80, "B")         # the exact-100 pile
letter(ax, mix.cs.mean(), ymax * 0.95, "C")   # the mean, describing nobody
fig.tight_layout()
fig.savefig(OUT.format("bimodal"))
plt.close(fig)
print("wrote bimodal")

# ---- Figure 3: flat across deciles 1-9, then the cliff ------------------
dec_med = mix.groupby("dec").cs.median()
top1 = mix.nlargest(int(len(mix) * 0.01), "totrevenue")

fig, ax = plt.subplots(figsize=(8, 4.4))
colors = [TEAL] * 9 + [TEAL_DEEP]
ax.bar(np.arange(1, 11), dec_med.values, color=colors, edgecolor=INK, lw=1.0, width=0.72)
ax.bar([11.4], [top1.cs.median()], color=TEAL_LIFT, edgecolor=INK, lw=1.0, width=0.72)
ax.set_xticks(list(np.arange(1, 11)) + [11.4])
ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "top\n1%"])
ax.set_ylim(0, 100)                      # REQUIRED: never truncate the flat run
ax.set_xlabel("revenue decile (smallest to largest)")
ax.set_ylabel("median contribution share (%)")
letter(ax, 5, 82, "A")                   # the flat run, deciles 1-9
letter(ax, 10, 34, "B")                  # the cliff at decile 10
letter(ax, 11.4, 13, "C")                # the top 1%, a different population
fig.tight_layout()
fig.savefig(OUT.format("by-size"))
plt.close(fig)
print("wrote by-size")

# ---- Figure 4: the inverted U ------------------------------------------
# Group by the `band` compute.py already assigned — never re-derive the bands
# here, or this figure can drift from the asserted numbers.
LABS = ["0-10", "10-25", "25-50", "50-75", "75-90", "90-100"]
res = mix[mix.honest.notna()]
meds = res.groupby("band", observed=True).honest.median().reindex(LABS).tolist()
labs = ["0–10", "10–25", "25–50", "50–75", "75–90", "90–100"]

fig, ax = plt.subplots(figsize=(8, 4.4))
ax.plot(range(len(meds)), meds, color=TEAL_DEEP, lw=2.2, marker="o",
        ms=8, mfc=CREAM, mec=INK, mew=1.4, zorder=5)
ax.set_xticks(range(len(labs)))
ax.set_xticklabels(labs)
ax.set_ylim(0, max(meds) * 1.35)
ax.set_xlabel("contribution share of revenue (%)")
ax.set_ylabel("median honest reserve (months)")
letter(ax, 0, meds[0] + max(meds) * 0.16, "A")        # fee-funded end, fragile
letter(ax, 4, meds[4] + max(meds) * 0.16, "B")        # the resilient middle
letter(ax, 5, meds[5] + max(meds) * 0.16, "C")        # donation-funded end, fragile
fig.tight_layout()
fig.savefig(OUT.format("inverted-u"))
plt.close(fig)
print("wrote inverted-u")
```

- [ ] **Step 2: Run and verify all four exist**

```bash
cd calcs/who-pays && python3 figures.py && ls -la ../../images/2026-07-14-nobodys-average-*.png
```

Expected: four PNGs, all non-trivial size (>20 KB).

- [ ] **Step 3: Verify Figure 4 actually shows the inverted U**

```bash
cd calcs/who-pays && python3 -c "
import pandas as pd
m = pd.read_csv('mix.csv.gz'); r = m[m.honest.notna()]
L = ['0-10','10-25','25-50','50-75','75-90','90-100']
med = r.groupby('band', observed=True).honest.median().reindex(L)
print([round(x,2) for x in med])
assert med['0-10'] < med['75-90'] and med['90-100'] < med['75-90'], 'not an inverted U — investigate'
print('ok — inverted U confirmed: peaks at the 75-90 band, falls at both ends')
"
```

Expected: `[5.18, 5.83, 7.38, 8.9, 9.48, 5.37]` then `ok`.

- [ ] **Step 4: Look at all four figures**

Open each. Check: no sentences in any plot area (lettered callouts only); Figure 3's y-axis runs 0–100 and the flat run across deciles 1–9 is visibly flat; Figure 4 reads as a hump, not a line.

- [ ] **Step 5: Commit**

```bash
git add calcs/who-pays/figures.py images/2026-07-14-nobodys-average-bimodal.png images/2026-07-14-nobodys-average-by-size.png images/2026-07-14-nobodys-average-inverted-u.png
git commit -m "figures: nobodys-average bimodal, by-size, inverted-u

Figure 3 pins y to 0-100 so the flat run across deciles 1-9 reads as flat —
the flatness is half the argument, and autoscaling would hide it.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Write the post

**Files:**
- Create: `posts/2026-07-14-nobodys-average.md`
- Reference: `posts/2026-07-11-below-zero-negative-operating-reserve.md` (voice), `docs/superpowers/specs/2026-07-14-nobodys-average-design.md` (§Structure, §Verified findings), `notes/blog-authoring.md`

**Interfaces:**
- Consumes: the four PNGs from Tasks 2–3; all numbers from the spec's §Verified findings (never recomputed by hand — copy from the spec).
- Produces: the post. Task 5 builds it.

Nine sections per spec §Structure. **Read the spec's §Structure in full before drafting** — it specifies each section's job, and section 5 exists specifically to *refuse* the size explanation.

- [ ] **Step 1: Write the frontmatter**

```yaml
---
title: "Nobody's average: who actually pays for the nonprofit sector"
date: 2026-07-14
tags: nonprofits, data
description: "Donations are 24 percent of the money that moves through American charities. The median charity gets 65 percent of its revenue from donations. Both numbers are right, and what has to be true for both to be right is that 501(c)(3) is not one population — a fact the IRS has been recording on Schedule A the whole time."
og-image: /images/2026-07-14-nobodys-average-hero.png
---
```

No `author` field — the nonprofit series renders without a byline. The title is quoted because it contains a colon.

- [ ] **Step 2: Draft the nine sections**

Follow spec §Structure exactly:

1. **Hook** — the founding sentence, then 24.4%. Establish the contradiction, not the number, as the subject.
2. **The census, not the survey** — method, both filter disclosures (the ~7,320 orgs dropped by the [0,100] restriction; the FASB reconciliation returning for the reserve section only), Code 1.
3. **Two true answers** — 24.4% dollar-weighted vs 65.1% median. Figure 1.
4. **The distribution is bimodal** — 26,657 exact zeros, 25,366 exact hundreds; the mean of 56% describes nobody. Figure 2. Tie back to the at-scale post's sector-average reserve — same failure mode.
5. **It isn't size — it's business model** — kill the intuitive story: 1.3× median revenue gap, piles in every decile. Then the cliff: deciles 1–9 flat ~70%, top 1% at 2.0%. Figure 3.
6. **The inverted U** — both extremes fragile, middle resilient. Figure 4. Correlation-not-causation caveat inline.
7. **The distinction is already in the file** — Table 1, `nonpfrea`. State the qualifies-under vs actually-funded caveat here, in place.
8. **Conclusion: they don't belong in the same bucket** — the two-claim argument; explicitly decline the bell-curve version; the fix is to stop discarding the taxonomy already in the file.
9. **Close** — series cross-links, the noprofits.org tools, one-line reader caveat.

Code 1 (in section 2) is the core arithmetic:

````markdown
```python
cs = totcntrbgfts / totrevenue * 100          # contribution share, per charity
sector = totcntrbgfts.sum() / totrevenue.sum() * 100   # the dollar-weighted answer
```

**Code 1.** The whole disagreement in two lines: the per-charity ratio and the sector ratio are different questions, and the second is not the average of the first.
````

Table 1 (in section 7) ships the eleven `nonpfrea` codes with n ≥ 1,000 from the spec, with a bold caption below it, referenced by number from the prose.

Every figure gets `<figure><img src="/images/..." alt="[a real sentence describing what it argues]"></figure>` followed by `**Figure N.** [full sentence]`, and is referenced by number in the body.

- [ ] **Step 3: Check the post against the three forbidden claims**

```bash
grep -niE "bell curve|normal distribution|hospitals? (and|vs|versus)|food pantr|IRS already sorts|clean(ly)? (sort|partition|separat)" posts/2026-07-14-nobodys-average.md
```

Expected: **no output**, or only hits you can justify. Any sentence claiming the piles differ by size, that the IRS already sorts these groups, or that non-normality implies multiple populations is a factual error per Global Constraints — rewrite it.

- [ ] **Step 4: Check the conventions**

```bash
python3 - <<'PY'
import re, pathlib
t = pathlib.Path("posts/2026-07-14-nobodys-average.md").read_text()
body = t.split("---", 2)[2]
figs = re.findall(r'\*\*Figure (\d+)\.\*\*', body)
tabs = re.findall(r'\*\*Table (\d+)\.\*\*', body)
code = re.findall(r'\*\*Code (\d+)\.\*\*', body)
print("captions — figures:", figs, "tables:", tabs, "code:", code)
for n in figs:
    assert re.search(rf'Figure {n}\b', body.replace(f'**Figure {n}.**','')), f"Figure {n} never referenced in prose"
for n in tabs:
    assert re.search(rf'Table {n}\b', body.replace(f'**Table {n}.**','')), f"Table {n} never referenced in prose"
assert figs == ['1','2','3','4'], f"expected Figures 1-4, got {figs}"
assert not re.search(r'\[@\w+\]', body), "Pandoc citation found — nonprofit series uses inline links only"
assert not re.search(r'\[\^\d+\]', body), "footnote found — matches neither convention"
assert not re.search(r'https://blog\.noprofits\.org', body), "absolute self-link — use site-relative"
assert not re.search(r'^author:', t, re.M), "author field present — nonprofit series omits the byline"
assert '<img' in body and 'alt="' in body, "figure missing alt text"
assert not re.search(r'^# ', body, re.M), "in-body H1 — the template renders the title"
print("ok — conventions pass")
PY
```

Expected: `ok — conventions pass`.

- [ ] **Step 5: Commit**

```bash
git add posts/2026-07-14-nobodys-average.md
git commit -m "post: nobody's average — who actually pays for the nonprofit sector

Fourth in the 990 data series. Donations are 24.4% of sector dollars but
the median charity is 65% donation-funded; both are true because the top 1%
holds most of the money and looks nothing like the other 240,000 orgs.
Concludes that 501(c)(3) is a legal category doing duty as an analytic one —
and that nonpfrea, the Schedule A test each org declares, already records the
distinction the sector averages across.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Build, verify, PR

**Files:**
- No new files. Verifies everything above.

**Interfaces:**
- Consumes: all prior tasks.
- Produces: a PR into `main`.

- [ ] **Step 1: Build the site**

```bash
stack build && stack exec blog build
```

Expected: exit 0. **A YAML frontmatter error aborts the whole build and names the file** — if it fails on `posts/2026-07-14-nobodys-average.md`, the title quoting is the first suspect (§Frontmatter gotchas).

Note: the README says `stack exec blog watch`, so the executable is `blog`. If `stack exec blog build` isn't right, check `blog.cabal` for the executable name.

- [ ] **Step 2: Verify the post rendered**

```bash
ls -la _site/posts/ | grep nobodys
python3 - <<'PY'
import pathlib, re
p = list(pathlib.Path("_site/posts").glob("*nobodys-average*"))
assert p, "post did not render"
h = p[0].read_text()
for name in ("hero", "bimodal", "by-size", "inverted-u"):
    assert f"2026-07-14-nobodys-average-{name}.png" in h, f"{name} figure missing from rendered page"
assert "og:image" in h and "2026-07-14-nobodys-average-hero.png" in h, "OG card meta wrong"
print("ok — rendered with all four figures and the right OG card")
PY
```

Expected: `ok — rendered with all four figures and the right OG card`.

- [ ] **Step 3: Look at the rendered page**

Open `_site/posts/2026-07-14-nobodys-average.html` in a browser. Check: figures load; captions numbered and below their figures; Table 1 renders as a table; no raw `**Figure 1.**` markdown leaking; title and tags render once (from the template, not duplicated in-body).

A green build does **not** prove the page is right — the authoring notes are explicit that failures can be silent. Look at it.

- [ ] **Step 4: Push and open the PR**

```bash
git push -u origin post/nobodys-average
gh pr create --base main --title "Add post: nobody's average — who actually pays for the nonprofit sector" --body "$(cat <<'EOF'
Fourth post in the Form 990 data series, after below-zero.

**The finding.** Donations are 24.4% of the $3.10T that moves through
501(c)(3) public charities, but the median charity is 65% donation-funded.
Both are true: the top 1% of charities hold 69.1% of the revenue, and their
median contribution share is 2.0% against ~70% for deciles 1-9.

**The conclusion.** 501(c)(3) is a legal category doing duty as an analytic
one. The distribution is a mixture of business models (26,657 charities report
exactly 0% contributions, 25,366 exactly 100%, and the piles appear at every
size) plus a detached institutional population at the top. The turn: `nonpfrea`
— the public-charity test each org declares on Schedule A — already separates
them (code 07 median 87.0%, code 09 median 42.2%, hospitals 1.4%). The IRS
collects the distinction; the sector averages across it anyway.

**Reproducibility.** `calcs/who-pays/compute.py` asserts every number in the
post against the approved spec and exits non-zero on drift.

Spec: `docs/superpowers/specs/2026-07-14-nobodys-average-design.md`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 5: Report the PR URL to Peter**

Do not merge without Peter's say-so — merging triggers the Pages deploy to the live blog.

---

## Notes for the executor

- **The spec outranks you on numbers.** Task 1's assertions encode findings verified against the data during design. A failing assertion means the script drifted. Never "fix" it by editing the spec.
- **Two numbers that look wrong but aren't:** the fee pile's *median* revenue is only 1.3× the donation pile's even though its *mean* is 7× — the gap is entirely tail. And code 09's median contribution share is 42.2%, not near zero, because `nonpfrea` records qualification, not realized funding. Both are load-bearing; don't "correct" them.
- **The post's turn is section 7.** Sections 3–6 exist to make the reader accept that these are different populations, so that section 7's reveal — the IRS has been coding it all along — lands. If a draft buries `nonpfrea` in a footnote, the post has no point.
