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
      E = (observed - counterfactual) above   "excess above"
      M = (counterfactual - observed) below   "missing below"
      displacement = E + M

  WHAT DISPLACEMENT IS, AND IS NOT  (corrected 2026-07-15)
    E + M is a TEST STATISTIC, not a count of organisations. If an organisation
    moves from just-below to just-above the line it is counted TWICE: once as
    absent below, once as present above. The post originally reported E+M as
    "about 80 organizations", which overstates the number affected by ~57%.
    The honest quantities are E ~= 29 and M ~= 51 reported separately, and the
    cleanest effect size is M as a share of the mass the counterfactual expects
    below the line: ~15.5%.

    E+M IS defensible as a test statistic, for a specific reason: the
    counterfactual enters E with a minus and M with a plus, so a curve fitted
    too high inflates M and deflates E by the same amount and the sum
    differences that level error out. Across placebos corr(E,M) = -0.445 and
    sd(E+M) = 22.4 against 30.0 if they were independent — that is the variance
    reduction, and it is why E+M has more power than either half.

    The corollary is a caveat the post must carry: neither half is individually
    decisive (z of E = 1.50, z of M = 2.45). What is significant is the JOINT
    asymmetry around the line, not either margin.

  NOT IMPLEMENTED: the integration constraint used in the bunching literature
    (Chetty et al.), which forces the counterfactual to preserve total mass.
    Without it E and M need not balance, and here they do not (29 vs 51). A
    mass-preserving counterfactual would be the more faithful estimator; this
    script does not have one, and the reported figures should be read with that
    in mind.

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


def parts(data, cliff, lo, hi, bw=BW, deg=DEG, w=W):
    """Return (E, M, cf_below, cf_above) against a polynomial counterfactual
    fitted on the region OUTSIDE the +/-w window.
      E = excess mass above the threshold
      M = missing mass below it
    Reported separately because E+M double-counts movers (see module docstring)."""
    bins = np.arange(lo, hi + bw, bw)
    cnt, e = np.histogram(data, bins=bins)
    mid = (e[:-1] + e[1:]) / 2
    excl = (mid > cliff - w) & (mid < cliff + w)
    cf = np.polyval(np.polyfit(mid[~excl], cnt[~excl], deg), mid)
    ab = (mid >= cliff) & (mid < cliff + w)
    be = (mid >= cliff - w) & (mid < cliff)
    return (cnt[ab].sum() - cf[ab].sum(), cf[be].sum() - cnt[be].sum(),
            cf[be].sum(), cf[ab].sum())


def displacement(data, cliff, lo, hi, bw=BW, deg=DEG, w=W):
    """E + M. A TEST STATISTIC, not a count of organisations — see docstring."""
    E, M, _, _ = parts(data, cliff, lo, hi, bw, deg, w)
    return E + M


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
REAL_E, REAL_M, CF_BE, CF_AB = parts(p, CLIFF, LO, HI)
print("\nHEADLINE — reported as E and M separately; E+M is a test statistic only")
check("E  excess above the line", REAL_E, 28.7, 0.1)
check("M  missing below the line", REAL_M, 51.4, 0.1)
check("E + M  (test statistic, NOT a count)", REAL, 80.1, 0.3)
check("mass the counterfactual expects below", CF_BE, 331.4, 0.1)
MISS_PCT = REAL_M / CF_BE * 100
check("M as % of expected below  <-- effect size", MISS_PCT, 15.5, 0.1)

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

# Neither half is individually decisive — the JOINT asymmetry is what the
# placebo test rejects. The post must say so rather than imply that "80
# organisations bunched" was directly observed.
print("\nPLACEBO — each half on its own (the caveat, not the headline)")
pp = [parts(p, float(t), max(10.0, t - 13.0), min(95.0, t + 17.0))
      for t in np.arange(22, 49, 1.0) if abs(t - CLIFF) >= 3]
pE = np.array([x[0] for x in pp])
pM = np.array([x[1] for x in pp])
Z_E = (REAL_E - pE.mean()) / pE.std()
Z_M = (REAL_M - pM.mean()) / pM.std()
check("z of E alone (NOT significant)", Z_E, 1.50, 0.03)
check("placebos >= real E", (pE >= REAL_E).sum(), 2, 0)
check("z of M alone (marginal)", Z_M, 2.45, 0.03)
check("placebos >= real M", (pM >= REAL_M).sum(), 1, 0)

# Why E+M has more power than either half: the counterfactual's level error
# enters with opposite signs and differences out.
CORR_EM = float(np.corrcoef(pE, pM)[0, 1])
check("corr(E,M) across placebos", CORR_EM, -0.445, 0.005)
check("sd(E+M) observed", (pE + pM).std(), 22.4, 0.1)
check("sd(E+M) if independent", float(np.sqrt(pE.var() + pM.var())), 30.0, 0.1)

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

# The near-cliff group is BIMODAL in donor concentration, so its median (53.9%)
# sits in a valley and describes almost nobody — the 40-55% band holds only 6.5%
# of it. Report the decomposition, not the median. (The previous post in this
# series is about exactly this mistake; it nearly got made here.)
print("\nTHE 2% RULE — decomposition (the median is bimodal, do not lean on it)")
NEAR_LT5 = (near.pct_excluded < 5).mean() * 100
NEAR_GE40 = (near.pct_excluded >= 40).mean() * 100
NEAR_5575 = ((near.pct_excluded >= 55) & (near.pct_excluded < 75)).mean() * 100
NEAR_4055 = ((near.pct_excluded >= 40) & (near.pct_excluded < 55)).mean() * 100
TYP_LT5 = (typ.pct_excluded < 5).mean() * 100
check("near-cliff: % with <5% excluded", NEAR_LT5, 29.5, 0.1)
check("near-cliff: % with >=40% excluded", NEAR_GE40, 55.7, 0.1)
check("near-cliff: % in the 55-75% mode", NEAR_5575, 49.2, 0.1)
check("near-cliff: % in the 40-55% VALLEY", NEAR_4055, 6.5, 0.1)
check("typical: % with <5% excluded", TYP_LT5, 86.0, 0.1)

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
               "corr_excluded": float(CORR),
               "near_lt5": float(NEAR_LT5), "near_ge40": float(NEAR_GE40),
               "near_5575": float(NEAR_5575), "near_4055": float(NEAR_4055),
               "typ_lt5": float(TYP_LT5),
               "real_E": float(REAL_E), "real_M": float(REAL_M),
               "cf_below": float(CF_BE), "miss_pct": float(MISS_PCT),
               "z_E": float(Z_E), "z_M": float(Z_M),
               "corr_EM": CORR_EM}, f, indent=2)

print("\nwrote cf.csv.gz, cliff.csv.gz, stats.json")
if FAILURES:
    print(f"\n{len(FAILURES)} SPEC MISMATCH(ES) — the script is wrong, not the spec:")
    for f_ in FAILURES:
        print("  " + f_)
    raise SystemExit(1)
print("\nall spec assertions passed")
