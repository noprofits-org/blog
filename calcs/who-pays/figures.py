#!/usr/bin/env python3
"""Data figures for the nobodys-average post. numpy + matplotlib, brand palette
(notes/blog-authoring.md §5). Lettered callouts only; captions carry the words.

NO PANDAS — deliberately. compute.py runs under an env with pandas; this runs
under one with matplotlib (the two are not the same env on this machine, same
as the below-zero sibling). Hence np.genfromtxt and an all-numeric mix.csv.gz.

Run with an interpreter that has matplotlib, e.g.
  /opt/homebrew/Caskroom/miniforge/base/envs/qchem/bin/python figures.py

Reads mix.csv.gz + agg.json (written by compute.py). Writes:
  images/2026-07-14-nobodys-average-hero.png        Figure 1 (1200x630 hero/OG)
  images/2026-07-14-nobodys-average-bimodal.png     Figure 2
  images/2026-07-14-nobodys-average-by-size.png     Figure 3
  images/2026-07-14-nobodys-average-inverted-u.png  Figure 4
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

OUT = "../../images/2026-07-14-nobodys-average-{}.png"

mix = np.genfromtxt("mix.csv.gz", delimiter=",", names=True)
agg = json.load(open("agg.json"))

cs = mix["cs"]
band_idx = mix["band_idx"]
honest = mix["honest"]
dec = mix["dec"]
totrev = mix["totrevenue"]

MEDIAN_CS = np.median(cs)


def letter(ax, x, y, s):
    """Bold lettered callout — the only prose allowed in a plot area."""
    ax.text(x, y, s, fontsize=13, fontweight="bold", color=INK,
            ha="center", va="center", zorder=10,
            bbox=dict(boxstyle="circle,pad=0.22", fc=CREAM, ec=INK, lw=1.2))


# ---- Figure 1: the two answers, side by side (1200x630 hero/OG) ---------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.2))

# Left: dollar-weighted. One stacked bar, the whole sector's money.
T = agg["total_revenue"]
parts = [agg["contrib"], agg["prgm"], agg["invst"], agg["residual"]]
colors = [TEAL_DEEP, TEAL, TEAL_LIFT, CREAM]
left = 0.0
for val, color in zip(parts, colors):
    ax1.barh([0], [val / T * 100], left=left, color=color, edgecolor=INK, lw=1.0, height=0.92)
    left += val / T * 100
ax1.set_xlim(0, 100)
ax1.set_ylim(-0.5, 0.5)
ax1.set_yticks([])
ax1.set_xlabel("percent of sector revenue")
letter(ax1, agg["contrib"] / T * 100 / 2, 0, "A")
letter(ax1, (agg["contrib"] + agg["prgm"] / 2) / T * 100, 0, "B")
ax1.spines["left"].set_visible(False)

# Right: org-weighted. The distribution of the same ratio, per charity.
ax2.hist(cs, bins=np.arange(0, 102, 2), color=TEAL, edgecolor=INK, lw=0.4)
ax2.axvline(MEDIAN_CS, color=INK, lw=1.6, ls="--")
ax2.set_xlim(0, 100)
ax2.set_xlabel("contribution share of one charity's revenue (%)")
ax2.set_ylabel("charities")
letter(ax2, 5, ax2.get_ylim()[1] * 0.72, "C")
letter(ax2, 95, ax2.get_ylim()[1] * 0.72, "D")
letter(ax2, MEDIAN_CS, ax2.get_ylim()[1] * 0.93, "E")

fig.tight_layout()
fig.savefig(OUT.format("hero"))
plt.close(fig)
print("wrote hero")
