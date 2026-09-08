#!/usr/bin/env python3
"""Regenerate both article charts from results.json; run compute.py first."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "images"
D = json.loads((HERE / "results.json").read_text())
INK, TEAL, DEEP, LIFT, CREAM = "#143f33", "#2f7da3", "#1c5572", "#5b9fc0", "#f7f1d7"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.parse_math": False,
                     "text.color": INK, "axes.labelcolor": INK,
                     "axes.edgecolor": INK, "xtick.color": INK, "ytick.color": INK})


def style(ax):
    ax.set_facecolor(CREAM)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(length=4)


def main():
    OUT.mkdir(exist_ok=True)
    labels = [b["band"] for b in D["bands"]]
    x = np.arange(4)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor(CREAM)
    for ax, key, label, ylim, letter in [
        (axes[0], "reserve_median", "Median estimated reserve (months)", 8, "A"),
        (axes[1], "reserve_le3_pct", "Recipients at or below 3 reserve months (%)", 55, "B"),
    ]:
        vals = [b[key] for b in D["bands"]]
        ax.bar(x, vals, width=.62, color=[TEAL, TEAL, TEAL, DEEP])
        ax.set_xticks(x, labels)
        ax.set_ylim(0, ylim)
        ax.set_ylabel(label)
        ax.set_xlabel("Government grants / total revenue", labelpad=14)
        ax.text(3, vals[3] + ylim * .035, letter, ha="center", fontweight="bold", fontsize=16)
        style(ax)
    fig.subplots_adjust(left=.08, right=.97, top=.92, bottom=.19, wspace=.30)
    fig.savefig(OUT / "2026-09-08-when-the-funding-stops-hero.png", dpi=100)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor(CREAM)
    colors = [LIFT, TEAL, "#143f33", DEEP]
    markers = ["o", "s", "^", "D"]
    for j, size in enumerate(D["expense_bands"]):
        ax.plot(x, [b["reserve_median"] for b in size["bands"]],
                color=colors[j], marker=markers[j], markersize=8,
                linewidth=2, label=size["size"])
    ax.set_xticks(x, labels)
    ax.set_xlim(-.15, 3.2)
    ax.set_ylim(0, 12)
    ax.set_ylabel("Median estimated reserve (months)")
    ax.set_xlabel("Government grants / total revenue", labelpad=12)
    ax.legend(title="Annual expenses", frameon=False, loc="upper right", ncols=2, fontsize=11)
    for idx, letter in [(0, "A"), (3, "B")]:
        y = D["expense_bands"][idx]["bands"][3]["reserve_median"]
        ax.annotate(letter, (3, y), xytext=(13, 0), textcoords="offset points",
                    va="center", fontweight="bold", fontsize=16)
    style(ax)
    fig.subplots_adjust(left=.085, right=.95, top=.94, bottom=.18)
    fig.savefig(OUT / "2026-09-08-when-the-funding-stops-size.png", dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    main()
