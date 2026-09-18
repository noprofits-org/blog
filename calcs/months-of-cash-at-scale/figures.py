#!/usr/bin/env python3
"""Data figures for the months-of-cash-at-scale post.

Reads c3_months.csv.gz (written by compute.py) and produces:
  images/2026-07-07-months-of-cash-at-scale-distribution.png  (Figure 2)
  images/2026-07-07-months-of-cash-at-scale-bands.png         (Figure 3)

numpy + matplotlib only (no pandas — the csv is 5 numeric columns).
Brand palette per notes/blog-authoring.md §5.
"""

import numpy as np
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

df = np.genfromtxt("c3_months.csv.gz", delimiter=",", names=True)
honest = df["honest"]
totfuncexpns = df["totfuncexpns"]

# ---- Figure 2: distribution of honest months, 501(c)(3) --------------------
# Lettered callouts only (A-D); the caption in the post explains each letter.
fig, ax = plt.subplots(figsize=(8, 4.6))
LO, HI, GAP = -6, 36, 1.5
interior = honest[(honest >= LO) & (honest <= HI)]
bins = np.arange(LO, HI + 1, 1)
ax.hist(interior, bins=bins, color=TEAL, edgecolor=PAGE, linewidth=0.4,
        weights=np.full(len(interior), 100.0 / len(honest)))

# Overflow bins (A, D): detached, lighter step of the same hue.
left_pct = (honest < LO).mean() * 100
right_pct = (honest > HI).mean() * 100
for x, pct, letter in [(LO - GAP - 0.5, left_pct, "A"),
                       (HI + GAP + 0.5, right_pct, "D")]:
    ax.bar(x, pct, width=1, color=TEAL_LIFT, edgecolor=PAGE, linewidth=0.4)
    ax.annotate(letter, xy=(x, pct + 0.5), ha="center",
                fontsize=11, fontweight="bold", color=INK)

med = np.median(honest)
ax.set_ylim(0, 17)
ax.axvline(3, color=INK, linestyle="--", linewidth=1.2, ymax=0.62)
ax.axvline(med, color=TEAL_DEEP, linestyle="-", linewidth=1.4, ymax=0.55)
ax.annotate("B", xy=(3, 10.9), ha="center",
            fontsize=11, fontweight="bold", color=INK)
ax.annotate("C", xy=(med, 9.7), ha="center",
            fontsize=11, fontweight="bold", color=TEAL_DEEP)

ticks = [LO - GAP - 0.5] + list(range(0, HI + 1, 6)) + [HI + GAP + 0.5]
ax.set_xticks(ticks, ["≤ −6"] + [str(t) for t in range(0, HI + 1, 6)] + ["> 36"])
ax.set_xlabel("Months of operating reserve (honest, NORI-style)")
ax.set_ylabel("Share of organizations (%)")
ax.set_xlim(LO - GAP - 1.2, HI + GAP + 1.2)
fig.tight_layout()
fig.savefig("../../images/2026-07-07-months-of-cash-at-scale-distribution.png")
plt.close(fig)

# ---- Figure 3: months by expense band — the inverted gradient --------------
bands = [(0, 5e5, "<\\$500K"), (5e5, 5e6, "\\$500K–\\$5M"),
         (5e6, 5e7, "\\$5M–\\$50M"), (5e7, np.inf, ">\\$50M")]
labels, medians, p25s, p75s, sh3 = [], [], [], [], []
for lo, hi, name in bands:
    s = honest[(totfuncexpns >= lo) & (totfuncexpns < hi)]
    labels.append(f"{name}\n(n={len(s):,})")
    medians.append(np.median(s))
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
# Lettered callout only (A = the floor line); the caption explains it and
# carries the per-band <=3mo shares (sh3).
ax.axhline(3, color=INK, linestyle="--", linewidth=1.2)
ax.annotate("A", xy=(-0.42, 3.35), fontsize=11, fontweight="bold", color=INK)

ax.set_xticks(x, labels)
ax.set_ylabel("Months of operating reserve")
ax.set_xlabel("Total annual expenses")
ax.set_ylim(0, max(p75s) + 3)
fig.tight_layout()
fig.savefig("../../images/2026-07-07-months-of-cash-at-scale-bands.png")
plt.close(fig)

print("wrote both figures")
