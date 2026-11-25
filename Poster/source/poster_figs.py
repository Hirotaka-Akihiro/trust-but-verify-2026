"""Poster figures, drawn from the stored results only (no numbers typed by hand).

Writes SVG files to poster/source/figs/. Text stays as text so the poster's own font (Inter) renders it.
Run from the project root: python poster/source/poster_figs.py
"""
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "implementation" / "results"
OUT = Path(__file__).with_name("figs")
OUT.mkdir(exist_ok=True)

NAVY, BLUE, MID, LIGHT, PALE = "#0B3C68", "#1F5C99", "#4A86C5", "#9CC1E6", "#D6E6F5"
ORANGE, INK, MUTED, GRID = "#D9822B", "#1B2433", "#5B6676", "#E3E8EF"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8.5,
                     "ytick.labelsize": 8.5, "legend.fontsize": 8.5, "axes.edgecolor": "#8A94A3", "axes.linewidth": 0.7,
                     "svg.fonttype": "none", "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED})

x = json.loads((RES / "cnet_extra.json").read_text())
u = json.loads((RES / "uncertainty_gate.json").read_text())


def clean(ax):
    ax.spines[["top", "right"]].set_visible(False)


def save(fig, name):
    p = OUT / f"{name}.svg"
    fig.savefig(p, bbox_inches="tight", pad_inches=0.03, transparent=True)
    plt.close(fig)
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"font-family:\s*'?[^;'\"]*'?", "font-family: Inter, sans-serif", s)
    s = re.sub(r"font-family=\"[^\"]*\"", "font-family=\"Inter, sans-serif\"", s)
    s = re.sub(r'<svg([^>]*?) width="[^"]*" height="[^"]*"', r'<svg\1 class="figsvg"', s, count=1)
    s = re.sub(r"<\?xml[^>]*>\s*", "", s)
    s = re.sub(r"<!DOCTYPE[^>]*>\s*", "", s)
    p.write_text(s, encoding="utf-8")


# ---- Fig. 3: weighted precision under the base-paper protocol, by flow timeout
W = ["15s", "30s", "60s", "120s"]
bp = x["base_protocol"]
fig, ax = plt.subplots(figsize=(4.6, 1.9))
for name, col, mk, lab in (("Random Forest (ours)", NAVY, "o", "Random Forest"),
                           ("C4.5-style tree", MID, "s", "C4.5-style tree (rebuilt)"),
                           ("1-NN (normalised)", LIGHT, "^", "1-NN (rebuilt)")):
    ys = [bp[w][name]["weighted_precision"] for w in W]
    ax.plot(range(4), ys, marker=mk, ms=5, lw=1.8, color=col, label=lab)
    if name == "Random Forest (ours)":
        for i, v in enumerate(ys):
            ax.text(i, v + 0.008, f"{v:.3f}", ha="center", va="bottom", fontsize=8, color=NAVY, fontweight="bold")
rep = x["base_paper_reported"]["best_average_precision"]
ax.axhline(rep["C4.5"], color=ORANGE, lw=1.2, ls=(0, (5, 3)))
ax.text(3.12, rep["C4.5"] + 0.004, f"C4.5 reported {rep['C4.5']:.3f}", color=ORANGE, fontsize=8, ha="right", va="bottom")
ax.axhline(rep["KNN"], color=ORANGE, lw=1.2, ls=(0, (1.5, 2)))
ax.text(-0.1, rep["KNN"] - 0.005, f"KNN reported {rep['KNN']:.3f}", color=ORANGE, fontsize=8, ha="left", va="top")
ax.set_xticks(range(4), ["15 s", "30 s", "60 s", "120 s"])
ax.set_xlabel("Flow timeout"); ax.set_ylabel("Weighted precision")
ax.set_ylim(0.68, 0.89); ax.set_xlim(-0.2, 3.2)
ax.grid(axis="y", lw=0.5, color=GRID)
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, handlelength=1.6, columnspacing=1.0)
clean(ax); save(fig, "fig3_baseprotocol")

# ---- Fig. 4: row-normalised confusion matrix of the Random Forest (test split)
ORDER = ["browsing", "chat", "email", "file_transfer", "p2p", "streaming", "voip"]
NICE = ["Browsing", "Chat", "Email", "File transfer", "P2P", "Streaming", "VoIP"]
pred = pd.read_csv(RES / "trusted_predictions.csv")
cm = pd.crosstab(pred.true, pred.predicted, normalize="index").reindex(index=ORDER, columns=ORDER, fill_value=0)
fig, ax = plt.subplots(figsize=(3.4, 2.55))
ax.imshow(cm.values, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(7), NICE, rotation=35, ha="right"); ax.set_yticks(range(7), NICE)
ft, ch = ORDER.index("file_transfer"), ORDER.index("chat")
for i in range(7):
    for j in range(7):
        v = cm.values[i, j]
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7.6,
                color="white" if v > 0.55 else INK, fontweight="bold" if (i, j) == (ft, ch) else "normal")
ax.add_patch(plt.Rectangle((ch - 0.5, ft - 0.5), 1, 1, fill=False, ec=ORANGE, lw=2.2))
ax.set_xlabel("Predicted application"); ax.set_ylabel("True application")
for s_ in ax.spines.values():
    s_.set_visible(False)
ax.tick_params(length=0)
save(fig, "fig4_confusion")

# ---- Fig. 5: policy-mass rule trade-off as the threshold rho varies
r = u["rules"]["mass"]; ts = sorted(float(t) for t in r["sweep"])
fig, ax = plt.subplots(figsize=(4.6, 1.9))
ax.plot(ts, [r["sweep"][str(t)]["violations"] for t in ts], "o-", ms=3.6, lw=1.8, color=NAVY, label="Violations (of 100)")
ax.plot(ts, [50 - r["sweep"][str(t)]["permitted_completed"] for t in ts], "s-", ms=3.6, lw=1.8, color=MID,
        label="Permitted tasks not completed (of 50)")
for bud, ls in (("0.05", (0, (5, 3))), ("0.1", (0, (1.5, 2)))):
    t = r["by_budget"][bud]["threshold"]
    ax.axvline(t, color=ORANGE, lw=1.2, ls=ls)
    ax.text(t + 0.015, 14.3, f"{int(float(bud) * 100)}% budget\nρ = {t:.2f}", color=ORANGE, fontsize=7.8, va="top")
ax.set_xlabel("Threshold ρ"); ax.set_ylabel("Count")
ax.set_ylim(0, 15.5); ax.grid(axis="y", lw=0.5, color=GRID)
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, handlelength=1.6, columnspacing=1.0)
clean(ax); save(fig, "fig5_tradeoff")
print("figures written to", OUT)
