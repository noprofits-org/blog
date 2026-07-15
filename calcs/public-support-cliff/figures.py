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
below = (mid >= CLIFF - 1.5) & (mid < CLIFF)
above = (mid >= CLIFF) & (mid < CLIFF + 1.5)

# Colour the bars by region rather than shading behind them: the window's bars
# ARE the finding, and a fill drawn under them is invisible.
colors = np.where(below[sel], CREAM, np.where(above[sel], TEAL_LIFT, TEAL))
ax.bar(mid[sel], obs[sel], width=0.45, color=colors, edgecolor=INK, lw=0.6, zorder=3)
ax.plot(mid[sel], cfv[sel], color=TEAL_DEEP, lw=2.4, ls="--", zorder=4)
ax.axvline(CLIFF, color=INK, lw=1.8, zorder=5)

ymax = obs[sel].max()
ax.set_xlim(24, 44)
ax.set_ylim(0, ymax * 1.18)
ax.set_xlabel("public support (% of total support)")
ax.set_ylabel("charities")
letter(ax, CLIFF, ymax * 1.09, "A")            # the line itself
letter(ax, CLIFF - 0.75, ymax * 0.30, "B")     # short of the counterfactual
letter(ax, CLIFF + 0.75, ymax * 0.30, "C")     # over the counterfactual
letter(ax, 41.0, ymax * 0.72, "D")             # the counterfactual
fig.tight_layout()
fig.savefig(OUT.format("hero"))
plt.close(fig)
print("wrote hero")

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
