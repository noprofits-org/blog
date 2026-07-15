#!/usr/bin/env python3
"""Who actually pays for the nonprofit sector — revenue mix across the census.

Supports posts/2026-07-14-nobodys-average.md. Every printed number is asserted
against docs/superpowers/specs/2026-07-14-nobodys-average-design.md. If an
assertion fires, THIS SCRIPT is wrong, not the spec.

WHAT `totcntrbgfts` IS  (corrected 2026-07-15)
  Form 990 Part VIII line 1h — the TOTAL of the contributions block, which
  includes line 1e, GOVERNMENT GRANTS. This extract publishes only the total, so
  nothing here separates private giving from government money. Call the ratio
  "contribution share", never "donation share": the Tax Foundation's 2019
  decomposition puts private contributions at ~12% of revenue and government
  grants at ~9%, i.e. roughly half of this figure is government.
  https://taxfoundation.org/blog/501c3-nonprofit-revenue/
  The org-vs-sector comparison this script exists for is unaffected — the same
  line is used identically for every filer — but the naming matters.

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
# band_idx is the same cut as an integer 0-5. figures.py runs in an env with
# matplotlib but NO pandas (see its docstring) and reads this file with
# np.genfromtxt, which needs every column numeric — so the band crosses the
# boundary as an index into LABS, not as a string.
res["band_idx"] = pd.cut(res.cs, bins=BINS, labels=False, include_lowest=True)

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
# The band is assigned here, not recomputed in figures.py — arithmetic lives in
# exactly one file, so a figure tweak can never move a number. Every column is
# numeric so np.genfromtxt can read it; see the band_idx note above.
out = mix[["EIN", "cs", "totrevenue", "npr", "dec"]].copy()
out = out.merge(res[["EIN", "honest", "band_idx"]], on="EIN", how="left")
out = out[["cs", "totrevenue", "npr", "dec", "honest", "band_idx"]]
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
