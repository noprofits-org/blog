#!/usr/bin/env python3
"""Data figures for the below-zero post. numpy + matplotlib, brand palette
(notes/blog-authoring.md §5). Lettered callouts only; captions carry the words.

Reads neg_c3.csv.gz and all_c3.csv.gz (written by compute.py). Writes:
  images/2026-07-11-below-zero-hero.png          Figure 1  (1200x630 hero/OG)
  images/2026-07-11-below-zero-by-size.png       Figure 2
  images/2026-07-11-below-zero-liquidity.png     Figure 3
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

neg = np.genfromtxt("neg_c3.csv.gz", delimiter=",", names=True)
allc3 = np.genfromtxt("all_c3.csv.gz", delimiter=",", names=True)

honest = neg["honest"]
totNA = neg["totnetassetend"]
unrest = neg["unrstrctnetasstsend"]
cashm = neg["cashmonths"]
exp = neg["totfuncexpns"]
n = len(honest)
N = len(allc3["honest"])

# Mutually exclusive causes.
underwater = totNA < 0
unrest_def = (~underwater) & (unrest < 0)
asset_rich = (~underwater) & (unrest >= 0)
pC = asset_rich.mean() * 100   # 57.9
pA = underwater.mean() * 100   # 32.4
pB = unrest_def.mean() * 100   # 9.7
distress = ((cashm < 1) & (underwater)).sum()

# ---- Figure 1 (HERO, 1200x630): what "below zero" is made of ---------------
fig = plt.figure(figsize=(12, 6.3), dpi=100)
ax = fig.add_axes([0.06, 0.30, 0.88, 0.40])

# A single 100%-wide horizontal bar segmented into the three causes.
segs = [("C", pC, TEAL_LIFT), ("A", pA, TEAL_DEEP), ("B", pB, TEAL)]
left = 0
for letter, w, col in segs:
    ax.barh(0, w, left=left, height=0.6, color=col, edgecolor=PAGE, linewidth=2)
    ax.annotate(letter, xy=(left + w / 2, 0), ha="center", va="center",
                fontsize=22, fontweight="bold", color=PAGE)
    ax.annotate(f"{w:.0f}%", xy=(left + w / 2, -0.46), ha="center", va="center",
                fontsize=13, color=INK)
    left += w

# D: distress subset bracket beneath segment A.
dstart = pC
dpct = distress / n * 100
ax.plot([dstart, dstart + dpct], [-0.72, -0.72], color=INK, linewidth=2.5)
ax.annotate("D", xy=(dstart + dpct / 2, -0.92), ha="center", va="center",
            fontsize=18, fontweight="bold", color=INK)

ax.set_xlim(0, 100)
ax.set_ylim(-1.15, 1.05)
ax.set_yticks([])
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=11)
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(INK)

fig.text(0.06, 0.88, "ONE IN SEVEN CHARITIES SITS AT OR BELOW ZERO RESERVE",
         fontsize=18, fontweight="bold", color=INK)
fig.text(0.06, 0.80, "28,651 of 202,827 U.S. public charities — and most of them are not out of money",
         fontsize=12.5, color=TEAL_DEEP)
fig.text(0.06, 0.12, "Each below-zero charity, sorted by why its expendable reserve is negative",
         fontsize=11, color=INK)
fig.savefig("../../images/2026-07-11-below-zero-hero.png", dpi=100)
plt.close(fig)

# ---- Figure 2: below-zero share by expense band ----------------------------
a_honest = allc3["honest"]
a_exp = allc3["totfuncexpns"]
a_totNA = allc3["totnetassetend"]
bands = [(0, 5e5, "<\\$500K"), (5e5, 5e6, "\\$500K–\\$5M"),
         (5e6, 5e7, "\\$5M–\\$50M"), (5e7, np.inf, ">\\$50M")]
labels, bz, uw = [], [], []
for lo, hi, name in bands:
    m = (a_exp >= lo) & (a_exp < hi)
    labels.append(f"{name}\n(n={m.sum():,})")
    bz.append((a_honest[m] <= 0).mean() * 100)
    uw.append((a_totNA[m] < 0).mean() * 100)

x = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.bar(x, bz, 0.55, color=TEAL, edgecolor=INK, linewidth=0.8,
       label="below zero (honest reserve ≤ 0)")
ax.plot(x, uw, "o-", color=TEAL_DEEP, linewidth=1.8, markersize=6,
        label="fully underwater (total net assets < 0)")
ax.annotate("A", xy=(3, bz[3] + 0.9), ha="center", fontsize=11,
            fontweight="bold", color=INK)
ax.annotate("B", xy=(3, uw[3] + 1.1), ha="center", fontsize=11,
            fontweight="bold", color=TEAL_DEEP)
ax.set_xticks(x, labels)
ax.set_ylabel("Share of charities (%)")
ax.set_xlabel("Total annual expenses")
ax.set_ylim(0, max(bz) + 6)
ax.legend(frameon=False, fontsize=9, loc="upper left")
fig.tight_layout()
fig.savefig("../../images/2026-07-11-below-zero-by-size.png")
plt.close(fig)

# ---- Figure 3: liquidity of the below-zero group ---------------------------
fig, ax = plt.subplots(figsize=(8, 4.6))
LO, HI = -3, 12
interior = cashm[(cashm >= LO) & (cashm <= HI)]
bins = np.arange(LO, HI + 0.5, 0.5)
ax.hist(interior, bins=bins, color=TEAL, edgecolor=PAGE, linewidth=0.4,
        weights=np.full(len(interior), 100.0 / n))
right_pct = (cashm > HI).mean() * 100
ax.bar(HI + 1.0, right_pct, width=0.5, color=TEAL_LIFT, edgecolor=PAGE,
       linewidth=0.4)
ax.annotate("D", xy=(HI + 1.0, right_pct + 0.4), ha="center", fontsize=11,
            fontweight="bold", color=INK)
med = np.median(cashm)
ax.axvline(0, color=INK, linestyle="--", linewidth=1.2)
ax.axvline(med, color=TEAL_DEEP, linewidth=1.5)
ax.axvline(3, color=INK, linestyle=":", linewidth=1.1)
ax.annotate("A", xy=(0, ax.get_ylim()[1] * 0.92), ha="center", fontsize=11,
            fontweight="bold", color=INK)
ax.annotate("B", xy=(med, ax.get_ylim()[1] * 0.82), ha="center", fontsize=11,
            fontweight="bold", color=TEAL_DEEP)
ax.annotate("C", xy=(3, ax.get_ylim()[1] * 0.72), ha="center", fontsize=11,
            fontweight="bold", color=INK)
ticks = list(range(LO, HI + 1, 3)) + [HI + 1.0]
ax.set_xticks(ticks, [str(t) for t in range(LO, HI + 1, 3)] + ["> 12"])
ax.set_xlabel("Months of literal cash on hand (Form 990 Part X lines 1+2)")
ax.set_ylabel("Share of below-zero charities (%)")
fig.tight_layout()
fig.savefig("../../images/2026-07-11-below-zero-liquidity.png")
plt.close(fig)

print("wrote three figures")
print(f"hero decomposition: C={pC:.1f} A={pA:.1f} B={pB:.1f}  distress D={distress:,} ({dpct:.1f}% of neg)")
