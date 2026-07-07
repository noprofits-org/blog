#!/usr/bin/env python3
"""Data figures for the months-of-cash-at-scale post.

Reads c3_months.csv.gz (written by compute.py) and produces:
  images/2026-07-07-months-of-cash-at-scale-distribution.png  (Figure 2)
  images/2026-07-07-months-of-cash-at-scale-bands.png         (Figure 3)

Brand palette per notes/blog-authoring.md §5.
"""

import gzip
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

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

df = pd.read_csv("c3_months.csv.gz")

# ---- Figure 2: distribution of honest months, 501(c)(3) --------------------
fig, ax = plt.subplots(figsize=(8, 4.6))
clipped = df.honest.clip(-6, 36)
bins = np.arange(-6, 36.5, 1)
ax.hist(clipped, bins=bins, color=TEAL, edgecolor=PAGE, linewidth=0.4,
        weights=np.full(len(clipped), 100.0 / len(clipped)))

med = df.honest.median()
ymax = 17
ax.set_ylim(0, ymax)
ax.axvline(3, color=INK, linestyle="--", linewidth=1.2, ymax=0.62)
ax.axvline(med, color=TEAL_DEEP, linestyle="-", linewidth=1.4, ymax=0.55)
ax.annotate("3-month floor (NORI)", xy=(3, 10.8), ha="center",
            fontsize=9, color=INK)
ax.annotate(f"median {med:.1f} mo", xy=(med, 9.7), ha="left",
            xytext=(med + 0.5, 9.7), fontsize=9, color=TEAL_DEEP)

share3 = (df.honest <= 3).mean() * 100
share0 = (df.honest <= 0).mean() * 100
share36 = (df.honest > 36).mean() * 100
ax.annotate(f"{share3:.0f}% of 501(c)(3)s sit at or below\n"
            f"three months ({share0:.0f}% at zero or below)",
            xy=(12, 13.5), fontsize=10, color=INK)
ax.annotate(f"all orgs below −6 months\npiled here →", xy=(-6.0, 7.2),
            fontsize=8, color=INK, alpha=0.75)
ax.annotate(f"← {share36:.0f}% hold more than\n     36 months, piled here",
            xy=(24.5, 15.2), fontsize=8, color=INK, alpha=0.75)

ax.set_xlabel("Months of operating reserve (honest, NORI-style)")
ax.set_ylabel("Share of organizations (%)")
ax.set_xlim(-6.2, 36.2)
fig.tight_layout()
fig.savefig("../../images/2026-07-07-months-of-cash-at-scale-distribution.png")
plt.close(fig)

# ---- Figure 3: months by expense band — the inverted gradient --------------
bands = [(0, 5e5, "<\\$500K"), (5e5, 5e6, "\\$500K–\\$5M"),
         (5e6, 5e7, "\\$5M–\\$50M"), (5e7, np.inf, ">\\$50M")]
labels, medians, p25s, p75s, sh3 = [], [], [], [], []
for lo, hi, name in bands:
    s = df[(df.totfuncexpns >= lo) & (df.totfuncexpns < hi)].honest
    labels.append(f"{name}\n(n={len(s):,})")
    medians.append(s.median())
    p25s.append(np.percentile(s, 25))
    p75s.append(np.percentile(s, 75))
    sh3.append((s <= 3).mean() * 100)

x = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.bar(x, medians, 0.55, color=TEAL, edgecolor=INK, linewidth=0.8,
       label="median months (honest)")
err_lo = np.array(medians) - np.array(p25s)
err_hi = np.array(p75s) - np.array(medians)
ax.errorbar(x, medians, yerr=[err_lo, err_hi], fmt="none", ecolor=INK,
            elinewidth=1.1, capsize=4, alpha=0.8)
ax.axhline(3, color=INK, linestyle="--", linewidth=1.2)
ax.annotate("3-month floor", xy=(-0.42, 3.35), fontsize=9, color=INK)
for xi, (m, p75, s3) in enumerate(zip(medians, p75s, sh3)):
    ax.annotate(f"{s3:.0f}% ≤ 3 mo", xy=(xi + 0.32, p75 + 1.2),
                ha="left", fontsize=9, color=TEAL_DEEP, fontweight="bold")

ax.set_xticks(x, labels)
ax.set_ylabel("Months of operating reserve")
ax.set_xlabel("Total annual expenses")
ax.set_ylim(0, max(p75s) + 3)
fig.tight_layout()
fig.savefig("../../images/2026-07-07-months-of-cash-at-scale-bands.png")
plt.close(fig)

print("wrote both figures")
