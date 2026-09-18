"""
Figures for the SOI reconciliation post. Run compute.py first (writes
reconciliation.json), then this. Regenerates every PNG in the post
deterministically.

  Figure 1  /images/2026-07-21-checking-our-work-hero.png   1200x630
  Figure 2  /images/2026-07-21-checking-our-work-contrib.png
"""

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
IMAGES = HERE.parent.parent / "images"
D = json.loads((HERE / "reconciliation.json").read_text())

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


# ------------------------------------------------------------- Figure 1 -----
# Gap from the published table, three cuts, seven line items. Zero = published.

ITEMS = [("n", "Number of returns"), ("rev", "Total revenue"),
         ("contrib", "Contributions"), ("assets", "Total assets"),
         ("liab", "Total liabilities"), ("netassets", "Total net assets"),
         ("exp", "Total expenses")]
SERIES = [("ty2022", "Tax year 2022 only", LIFT, "o"),
          ("dedup", "One return per EIN", TEAL, "s"),
          ("pooled", "All CY2023 filings", DEEP, "D")]

fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100)
fig.patch.set_facecolor(CREAM)
ax.set_facecolor(CREAM)

ys = range(len(ITEMS))
for key, label, colour, marker in SERIES:
    ax.scatter([D["gaps"][key][k] for k, _ in ITEMS], list(ys),
               s=110, color=colour, marker=marker, label=label,
               zorder=3, edgecolor=CREAM, linewidth=0.8)

ax.axvline(0, color=INK, linewidth=1.6, zorder=2)
for y in ys:
    ax.axhline(y, color=INK, alpha=0.10, linewidth=0.8, zorder=1)

ax.set_yticks(list(ys))
ax.set_yticklabels([lab for _, lab in ITEMS], fontsize=11)
ax.invert_yaxis()
ax.set_xlabel("Difference from the IRS published figure (percent)", fontsize=11)
ax.set_xlim(-15, 8)
ax.tick_params(axis="x", labelsize=10)
ax.legend(loc="lower left", frameon=False, fontsize=10)
style(ax)

# Lettered callouts, defined in the caption.
ax.annotate("A", (D["gaps"]["pooled"]["rev"], 1), textcoords="offset points",
            xytext=(0, 16), ha="center", fontsize=13, fontweight="bold", color=INK)
ax.annotate("B", (D["gaps"]["ty2022"]["liab"], 4), textcoords="offset points",
            xytext=(-2, 16), ha="center", fontsize=13, fontweight="bold", color=INK)
ax.annotate("C", (D["gaps"]["pooled"]["n"], 0), textcoords="offset points",
            xytext=(2, 16), ha="center", fontsize=13, fontweight="bold", color=INK)

fig.tight_layout()
fig.savefig(IMAGES / "2026-07-21-checking-our-work-hero.png",
            facecolor=CREAM, dpi=100)
plt.close(fig)

# ------------------------------------------------------------- Figure 2 -----
# What the published table can see that the extract cannot: contributions split
# into government grants and everything else. In billions of dollars.

CB = D["components_billions"]
PARTS = [("Government grants",
          CB["Government grants (contributions)"], DEEP),
         ("All other contributions,\ngifts and grants",
          CB["All other contributions, gifts, grants, etc."], TEAL),
         ("Related organizations", CB["Related organizations"], LIFT),
         ("Fundraising events", CB["Fundraising events"], "#8fbdd4"),
         ("Membership dues", CB["Membership dues"], "#b3d4e3"),
         ("Federated campaigns", CB["Federated campaigns"], "#d6e8ef")]

fig, ax = plt.subplots(figsize=(10, 3.4), dpi=100)
fig.patch.set_facecolor(CREAM)
ax.set_facecolor(CREAM)

left = 0.0
for label, value, colour in PARTS:
    ax.barh(0, value, left=left, height=0.5, color=colour,
            edgecolor=CREAM, linewidth=1.2)
    left += value

gov, other = PARTS[0][1], PARTS[1][1]
ax.annotate("A", (gov / 2, 0.34), ha="center", fontsize=13,
            fontweight="bold", color=INK)
ax.annotate("B", (gov + other / 2, 0.34), ha="center", fontsize=13,
            fontweight="bold", color=INK)

ax.set_xlim(0, 760)
ax.set_ylim(-0.5, 0.6)
ax.set_yticks([])
ax.set_xlabel("Billions of dollars, tax year 2022", fontsize=11)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(INK)

fig.tight_layout()
fig.savefig(IMAGES / "2026-07-21-checking-our-work-contrib.png",
            facecolor=CREAM, dpi=100)
plt.close(fig)

print("wrote both figures to", IMAGES)
