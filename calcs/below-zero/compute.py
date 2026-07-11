#!/usr/bin/env python3
"""Characterize the below-zero 501(c)(3) population — charities whose HONEST
months of operating reserve are at or below zero.

Builds on posts/2026-07-07-months-of-cash-at-scale.md, which found that 14% of
501(c)(3)s (one in seven) sit at or below zero honest reserve. This script asks
what that number is made of.

Data: ../data/24eoextract990.csv (IRS SOI annual extract, returns filed CY2024)
https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data

Same filters as the parent post: latest tax period per EIN; FASB reconciliation
(Part X lines 27+28+29 == line 33 within $1K); positive cash expenses.

  honest      = (line27 - line10c + line23) / (cash expenses / 12)
  honest_bond =  honest with line20 (tax-exempt bonds) added back
  cashmonths  = (line1 + line2) / (cash expenses / 12)   # literal cash on hand
"""

import pandas as pd
import numpy as np

COLS = ["EIN", "tax_pd", "subseccd", "totfuncexpns", "deprcatndepletn",
        "unrstrctnetasstsend", "temprstrctnetasstsend", "permrstrctnetasstsend",
        "lndbldgsequipend", "secrdmrtgsend", "txexmptbndsend", "totnetassetend",
        "nonintcashend", "svngstempinvend"]

df = pd.read_csv("../data/24eoextract990.csv", usecols=COLS)
df = df.sort_values("tax_pd").drop_duplicates("EIN", keep="last")
fasb = (df.unrstrctnetasstsend + df.temprstrctnetasstsend
        + df.permrstrctnetasstsend - df.totnetassetend).abs() <= 1000
df["cashexp"] = df.totfuncexpns - df.deprcatndepletn
df = df[fasb & (df.cashexp > 0)].copy()

df["honest"] = (df.unrstrctnetasstsend - df.lndbldgsequipend
                + df.secrdmrtgsend) / (df.cashexp / 12.0)
df["honest_bond"] = (df.unrstrctnetasstsend - df.lndbldgsequipend
                     + df.secrdmrtgsend + df.txexmptbndsend) / (df.cashexp / 12.0)
df["cashmonths"] = (df.nonintcashend + df.svngstempinvend) / (df.cashexp / 12.0)

c3 = df[df.subseccd == 3].copy()
N = len(c3)
neg = c3[c3.honest <= 0].copy()
n = len(neg)

print(f"501(c)(3) analyzed: {N:,}")
print(f"below zero (honest <= 0): {n:,} = {n/N*100:.1f}%  (1 in {N/n:.1f})")
print(f"depth: median {neg.honest.median():.1f}  p25 {neg.honest.quantile(.25):.1f}"
      f"  p10 {neg.honest.quantile(.10):.1f}")
print(f"only mildly under (>= -1 mo, incl 0): {(neg.honest >= -1).mean()*100:.1f}%")
print(f"deep (< -12 mo): {(neg.honest < -12).mean()*100:.1f}%")

# Three mutually exclusive causes.
underwater = neg.totnetassetend < 0                                  # A
unrest_def = (~underwater) & (neg.unrstrctnetasstsend < 0)           # B
asset_rich = (~underwater) & (neg.unrstrctnetasstsend >= 0)          # C
print("\ncauses (mutually exclusive):")
print(f"  A fully underwater (total NA < 0):        {underwater.mean()*100:5.1f}%  ({underwater.sum():,})")
print(f"  B unrestricted deficit, total NA >= 0:    {unrest_def.mean()*100:5.1f}%  ({unrest_def.sum():,})")
print(f"  C asset-rich, reserve-poor (line27>=0):   {asset_rich.mean()*100:5.1f}%  ({asset_rich.sum():,})")

print("\nliquidity:")
print(f"  positive cash on hand:      {(neg.cashmonths > 0).mean()*100:.1f}%")
print(f"  median cash-on-hand months: {neg.cashmonths.median():.1f}")
print(f"  >= 3 months literal cash:   {(neg.cashmonths >= 3).mean()*100:.1f}%")

print("\nbelow-zero share by expense band:")
bands = [(0, 5e5, "<$500K"), (5e5, 5e6, "$500K-5M"),
         (5e6, 5e7, "$5M-50M"), (5e7, np.inf, ">$50M")]
for lo, hi, name in bands:
    s = c3[(c3.totfuncexpns >= lo) & (c3.totfuncexpns < hi)]
    print(f"  {name:>10} (n={len(s):>7,}): below-zero {(s.honest<=0).mean()*100:5.1f}%"
          f"   underwater {(s.totnetassetend<0).mean()*100:4.1f}%")

distress = neg[(neg.cashmonths < 1) & (neg.totnetassetend < 0)]
print(f"\ndistress cluster (total NA < 0 AND < 1 mo cash): "
      f"{len(distress):,} = {len(distress)/N*100:.2f}% of all 501(c)(3)")
print(f"footprint: below-zero orgs run ${neg.totfuncexpns.sum()/1e9:.0f}B "
      f"= {neg.totfuncexpns.sum()/c3.totfuncexpns.sum()*100:.0f}% of sector expenses")

neg[["honest", "honest_bond", "cashmonths", "totfuncexpns",
     "unrstrctnetasstsend", "totnetassetend", "lndbldgsequipend",
     "txexmptbndsend"]].to_csv("neg_c3.csv.gz", index=False, compression="gzip")
c3[["honest", "cashmonths", "totfuncexpns", "totnetassetend"]].to_csv(
    "all_c3.csv.gz", index=False, compression="gzip")
print("\nwrote neg_c3.csv.gz, all_c3.csv.gz")
