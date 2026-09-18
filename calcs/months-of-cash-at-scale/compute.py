#!/usr/bin/env python3
"""Months of operating reserve, computed across every Form 990 e-filed in
calendar year 2024, from the IRS SOI annual extract.

Data: 24eoextract990.csv (IRS SOI, returns filed in CY2024)
https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data

Two versions per the blog's months-of-cash post
(posts/2026-07-06-months-of-cash.md):

  naive  = totnetassetend / (totfuncexpns / 12)
  honest = (unrstrctnetasstsend - lndbldgsequipend + secrdmrtgsend)
           / ((totfuncexpns - deprcatndepletn) / 12)

Field map (24eofinextractdoc.xlsx):
  unrstrctnetasstsend  Pt X-27(B)  net assets without donor restrictions, EOY
  lndbldgsequipend     Pt X-10(B)  land, buildings & equipment (net), EOY
  secrdmrtgsend        Pt X-23(B)  secured mortgages & notes payable, EOY
  totnetassetend       Pt X-33(B)  total net assets, EOY
  totfuncexpns         Pt IX-25(A) total functional expenses
  deprcatndepletn      Pt IX-22(A) depreciation, depletion, amortization
  subseccd             501(c) subsection code
"""

import pandas as pd
import numpy as np

COLS = ["EIN", "tax_pd", "subseccd", "totfuncexpns", "deprcatndepletn",
        "unrstrctnetasstsend", "temprstrctnetasstsend", "permrstrctnetasstsend",
        "lndbldgsequipend", "secrdmrtgsend", "txexmptbndsend",
        "totnetassetend", "nonintcashend", "svngstempinvend"]

df = pd.read_csv("../data/24eoextract990.csv", usecols=COLS)
n_raw = len(df)

# Dedupe: keep the latest tax period per EIN (amended/multiple filings).
df = df.sort_values("tax_pd").drop_duplicates("EIN", keep="last")
n_dedup = len(df)

# FASB check: orgs that don't follow ASC 958 report net assets on Part X
# lines 30-32 and leave 27-29 blank, which would fake a zero/negative
# unrestricted figure. Keep only filers whose 27+28+29 reconciles to
# line 33 (within $1K tolerance or exactly when 33 is 0).
fasb = (df.unrstrctnetasstsend + df.temprstrctnetasstsend
        + df.permrstrctnetasstsend - df.totnetassetend).abs() <= 1000
n_fasb_dropped = (~fasb).sum()

# Cash expenses must be positive to define a runway.
df["cashexp"] = df.totfuncexpns - df.deprcatndepletn
df = df[fasb & (df.cashexp > 0)].copy()
n_pos = len(df)

df["honest"] = (df.unrstrctnetasstsend - df.lndbldgsequipend
                + df.secrdmrtgsend) / (df.cashexp / 12.0)
df["naive"] = df.totnetassetend / (df.totfuncexpns / 12.0)

# Sensitivity: also add back tax-exempt bonds (Pt X line 20) — how large
# orgs finance buildings; the NORI recipe only adds back line 23.
df["honest_bond"] = (df.unrstrctnetasstsend - df.lndbldgsequipend
                     + df.secrdmrtgsend + df.txexmptbndsend) / (df.cashexp / 12.0)

# NFF-comparable metric: months of literal cash on hand (Pt X lines 1+2).
df["cashmonths"] = (df.nonintcashend + df.svngstempinvend) / (df.cashexp / 12.0)

c3 = df[df.subseccd == 3]

def describe(s, label):
    pct = lambda p: np.percentile(s, p)
    print(f"\n== {label} (n={len(s):,}) ==")
    print(f"  p10 {pct(10):8.1f}  p25 {pct(25):8.1f}  median {pct(50):8.1f}"
          f"  p75 {pct(75):8.1f}  p90 {pct(90):8.1f}")
    for thr in [0, 1, 3, 6, 12, 24]:
        print(f"  share <= {thr:>2} months: {(s <= thr).mean()*100:5.1f}%")
    print(f"  share > 24 months: {(s > 24).mean()*100:5.1f}%")

print(f"rows in extract: {n_raw:,}; after EIN dedupe: {n_dedup:,}; "
      f"non-FASB dropped: {n_fasb_dropped:,}; analyzed: {n_pos:,}"
      f"; 501(c)(3): {len(c3):,}")

describe(df.honest, "ALL 990 FILERS - honest (NORI-style)")
describe(df.naive, "ALL 990 FILERS - naive (net assets / expenses)")
describe(c3.honest, "501(c)(3) ONLY - honest")
describe(c3.naive, "501(c)(3) ONLY - naive")
describe(c3.honest_bond, "501(c)(3) ONLY - honest + bond add-back")
describe(c3.cashmonths, "501(c)(3) ONLY - months of cash on hand (NFF-comparable)")

# Size bands (501(c)(3), honest) - the barbell test.
bands = [(0, 5e5, "<$500K"), (5e5, 5e6, "$500K-$5M"),
         (5e6, 5e7, "$5M-$50M"), (5e7, np.inf, ">$50M")]
print("\n== 501(c)(3) honest months, by total-expense band ==")
for lo, hi, name in bands:
    s = c3[(c3.totfuncexpns >= lo) & (c3.totfuncexpns < hi)].honest
    print(f"  {name:>10} (n={len(s):>7,}): median {np.percentile(s,50):6.1f}"
          f"  <=3mo {(s<=3).mean()*100:5.1f}%  <=1mo {(s<=1).mean()*100:5.1f}%"
          f"  >12mo {(s>12).mean()*100:5.1f}%")

# How much does honesty cost? (median naive - honest gap)
gap = (c3.naive - c3.honest)
print(f"\nmedian correction (naive - honest), 501(c)(3): {gap.median():.1f} months")

# Save the per-band and overall histogram data for the figure.
out = c3[["honest", "naive", "honest_bond", "cashmonths", "totfuncexpns"]].copy()
out.to_csv("c3_months.csv.gz", index=False, compression="gzip")
print("\nwrote c3_months.csv.gz")
