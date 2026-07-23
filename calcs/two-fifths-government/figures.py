"""
Figures for the two-fifths-government post. Run compute.py first (writes
results.json), then this. Regenerates every PNG in the post deterministically.

  Figure 1  /images/2026-07-22-two-fifths-government-hero.png   1200x630
  Figure 2  /images/2026-07-22-two-fifths-government-mix.png
"""

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
IMAGES = HERE.parent.parent / "images"
D = json.loads((HERE / "results.json").read_text())

INK = "#143f33"
DEEP = "#1c5572"
TEAL = "#2f7da3"
LIFT = "#5b9fc0"
CREAM = "#f7f1d7"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.edgecolor": INK,
})


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)


LABELS = D["size_labels"][1:]          # six asset-size classes
X = range(6)

# ------------------------------------------------------------- Figure 1 -----
# Hero, 1200x630. Left: government grants as a share of each class's
# contributions (dashed line = all-size 40.3%). Right: as a share of each
# class's total revenue (dashed line = all-size 10.1%).

fig, (axl, axr) = plt.subplots(1, 2, figsize=(12, 6.3), dpi=100)
fig.patch.set_facecolor(CREAM)

pc = D["pct_contrib"][1:]
pr = D["pct_rev"][1:]

for ax, vals, ref, ylab in (
    (axl, pc, D["pct_contrib"][0], "Government grants, % of the class's contributions"),
    (axr, pr, D["pct_rev"][0], "Government grants, % of the class's total revenue"),
):
    ax.set_facecolor(CREAM)
    ax.bar(X, vals, color=TEAL, width=0.62, zorder=3)
    ax.axhline(ref, color=INK, linewidth=1.4, linestyle=(0, (5, 3)), zorder=2)
    ax.axhline(0, color=INK, linewidth=1.2)
    ax.set_xticks(X)
    ax.set_xticklabels(LABELS, fontsize=9.5, rotation=20, ha="right")
    ax.set_ylabel(ylab, fontsize=11)
    ax.set_xlabel("Total assets", fontsize=11)
    ax.tick_params(axis="y", labelsize=10)
    style(ax)

axl.set_ylim(0, 60)
axr.set_ylim(0, 60)

# Highlight the two bars the captions letter: the majority-government class
# and the giants' collapse.
axl.patches[4].set_facecolor(DEEP)      # $10M-50M, 51.6%
axr.patches[5].set_facecolor(LIFT)      # >=$50M, 7.0%

axl.annotate("A", (4, pc[4]), xytext=(0, 8), textcoords="offset points",
             ha="center", fontsize=14, fontweight="bold", color=INK)
axl.annotate("B", (5, pc[5]), xytext=(0, 8), textcoords="offset points",
             ha="center", fontsize=14, fontweight="bold", color=INK)
axr.annotate("C", (5, pr[5]), xytext=(0, 8), textcoords="offset points",
             ha="center", fontsize=14, fontweight="bold", color=INK)
axl.annotate("D", (0.20, D["pct_contrib"][0]), xytext=(0, 6),
             textcoords="offset points", ha="center", fontsize=14,
             fontweight="bold", color=INK)
axr.annotate("D", (2.5, D["pct_rev"][0]), xytext=(0, 6),
             textcoords="offset points", ha="center", fontsize=14,
             fontweight="bold", color=INK)

fig.tight_layout(pad=1.6)
fig.savefig(IMAGES / "2026-07-22-two-fifths-government-hero.png",
            facecolor=CREAM, dpi=100)
plt.close(fig)

# ------------------------------------------------------------- Figure 2 -----
# Revenue composition, 100%-stacked horizontal bars: Total + six classes.
# Segments: government grants / other contributions / program service (payer
# not identifiable in IRS data) / everything else.

ORDER = list(range(7))                  # Total first, then ascending size
names = D["size_labels"]
gov = D["pct_rev"]
priv = D["priv_pct"]
prg = D["prg_pct"]
oth = D["oth_pct"]

fig, ax = plt.subplots(figsize=(12, 6.0), dpi=100)
fig.patch.set_facecolor(CREAM)
ax.set_facecolor(CREAM)

ys = range(len(ORDER))[::-1]            # Total at the top
segs = [
    ("Government grants", gov, DEEP),
    ("Other contributions, gifts, and grants", priv, TEAL),
    ("Program service revenue", prg, LIFT),
    ("Everything else", oth, "#8aa398"),
]
for y, i in zip(ys, ORDER):
    left = 0.0
    for _, vals, colour in segs:
        ax.barh(y, vals[i], left=left, color=colour, height=0.62,
                edgecolor=CREAM, linewidth=1.2, zorder=3)
        left += vals[i]

ax.set_yticks(list(ys))
ax.set_yticklabels(names, fontsize=10.5)
ax.set_xlim(0, 100)
ax.set_xlabel("Share of the class's total revenue (%)", fontsize=11)
ax.tick_params(axis="x", labelsize=10)
style(ax)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)

handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in segs]
ax.legend(handles, [s[0] for s in segs], loc="upper center",
          bbox_to_anchor=(0.5, 1.14), ncol=4, frameon=False, fontsize=9.5)

# Letters: A = giants' program-service block; B = $10M-50M government block;
# C = the sector-total government block.
y_of = {i: y for y, i in zip(ys, ORDER)}
ax.annotate("A", (gov[6] + priv[6] + prg[6] / 2, y_of[6]), ha="center",
            va="center", fontsize=14, fontweight="bold", color=INK)
ax.annotate("B", (gov[5] / 2, y_of[5]), ha="center", va="center",
            fontsize=14, fontweight="bold", color=CREAM)
ax.annotate("C", (gov[0] / 2, y_of[0]), ha="center", va="center",
            fontsize=14, fontweight="bold", color=CREAM)

fig.tight_layout(pad=1.4)
fig.savefig(IMAGES / "2026-07-22-two-fifths-government-mix.png",
            facecolor=CREAM, dpi=100)
plt.close(fig)

print("wrote hero (1200x630) and mix figures to /images/")
