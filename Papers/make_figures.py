"""Figures for both papers, drawn from the stored results only (no numbers typed by hand).

Palette: one blue family + one orange accent; vector PDF at IEEE column widths
(single 3.5 in, double 7.16 in). Output: Papers/figs/*.pdf
Run: python Papers/make_figures.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
RES, OUT = ROOT / "implementation" / "results", Path(__file__).with_name("figs")
OUT.mkdir(exist_ok=True)
NAVY, BLUE, MID, LIGHT, PALE, TINT = "#0B3C68", "#1F5C99", "#4A86C5", "#9CC1E6", "#D6E6F5", "#EEF4FB"
ORANGE, GRAY = "#D9822B", "#7F7F7F"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7.5,
                     "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5,
                     "axes.edgecolor": "#444444", "axes.linewidth": 0.6, "pdf.fonttype": 42})

m = json.loads((RES / "metrics.json").read_text())
c = json.loads((RES / "classifier_metrics.json").read_text())
x = json.loads((RES / "cnet_extra.json").read_text())
u = json.loads((RES / "uncertainty_gate.json").read_text())
C = m["conditions"]


def clean(ax):
    ax.spines[["top", "right"]].set_visible(False)


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# ------------------------------------------------------------------ architecture (both papers)
def architecture(name, focus):
    fig, ax = plt.subplots(figsize=(7.16, 2.25)); ax.set_xlim(0, 100); ax.set_ylim(0, 31); ax.axis("off")

    def group(x0, y0, w, h, label):
        ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                                    fc=TINT, ec=LIGHT, lw=0.7, ls=(0, (3, 2))))
        ax.text(x0 + 0.8, y0 + h - 1.3, label, fontsize=6.5, color=NAVY, weight="bold", va="center")

    def box(cx, cy, w, h, title, sub, hi=False):
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.7",
                                    fc="white", ec=ORANGE if hi else BLUE, lw=1.3 if hi else 0.9))
        ax.text(cx, cy + 1.3, title, ha="center", va="center", fontsize=6.6, weight="bold",
                color=ORANGE if hi else NAVY)
        ax.text(cx, cy - 1.45, sub, ha="center", va="center", fontsize=5.4, color="#333333", linespacing=1.15)

    def arrow(p, q, label=None, lpos=None, dashed=False, color=GRAY, conn="arc3"):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=7, lw=0.8, color=color,
                                     ls=(0, (3, 2)) if dashed else "-", connectionstyle=conn))
        if label:
            ax.text(*lpos, label, fontsize=5.6, color=color if dashed else "#444444", ha="center", va="center",
                    style="italic")

    group(0.5, 16.8, 47.5, 14.0, "Traffic classification")
    group(0.5, 0.3, 71.8, 15.4, "Decision and enforcement")
    box(11.0, 23.0, 19, 7.5, "ISCXVPN2016 flow", "23 timing statistics\nno payload, IP or port")
    box(35.5, 23.0, 19, 7.5, "Random Forest", "7 application classes\nprobabilities p(c | f)",
        hi=focus == "classifier")
    box(63.0, 23.0, 22, 7.5, "Trusted record", "flow ID → predicted class ŷ\nread-only for the agent")
    box(10.5, 8.2, 18, 7.5, "Operator request", "instruction + optional\nuntrusted note")
    box(34.0, 8.2, 18, 7.5, "LLM agent", "Llama-3.2-3B (4-bit)\none JSON tool call")
    box(60.5, 8.2, 22, 7.5, "Deterministic gate", "dispatch → schema/range →\nflow identity → policy(ŷ)",
        hi=focus == "gate")
    box(88.5, 8.2, 19, 7.5, "Simulator", "flow state: held / allowed /\nblocked / rate-limited")
    arrow((20.5, 23.0), (26.0, 23.0)); arrow((45.0, 23.0), (52.0, 23.0))
    arrow((19.5, 8.2), (25.0, 8.2)); arrow((43.0, 8.2), (49.5, 8.2), "proposal", (46.25, 10.0))
    # labels sit in white space, clear of the dashed group borders
    arrow((71.5, 8.2), (79.0, 8.2), "execute", (75.9, 10.0))
    arrow((65.0, 19.25), (65.0, 11.95), "ŷ", (66.3, 18.0))
    arrow((56.0, 19.25), (42.9, 11.9), "ŷ", (51.2, 18.0))  # ends at the agent's top-right corner
    # retry: gate bottom -> down -> left -> up into the agent; dashed path, solid head
    ax.plot([58.0, 58.0, 36.0, 36.0], [4.45, 2.4, 2.4, 3.4], color=ORANGE, lw=0.8, ls=(0, (3, 2)))
    arrow((36.0, 3.2), (36.0, 4.45), color=ORANGE)
    ax.text(47.0, 1.25, "rejection reason (one retry)", fontsize=5.6, color=ORANGE, ha="center", va="center",
            style="italic")
    save(fig, name)


architecture("cn_architecture", "classifier")
architecture("ag_architecture", "gate")

# ------------------------------------------------------------------ CN: confusion matrix
ORDER = ["browsing", "chat", "email", "file_transfer", "p2p", "streaming", "voip"]
NICE = ["Browsing", "Chat", "Email", "File transfer", "P2P", "Streaming", "VoIP"]
pred = pd.read_csv(RES / "trusted_predictions.csv")
cm = pd.crosstab(pred.true, pred.predicted, normalize="index").reindex(index=ORDER, columns=ORDER, fill_value=0)
fig, ax = plt.subplots(figsize=(3.4, 2.75))
im = ax.imshow(cm.values, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(7), NICE, rotation=40, ha="right"); ax.set_yticks(range(7), NICE)
for i in range(7):
    for j in range(7):
        v = cm.values[i, j]
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=5.6, color="white" if v > 0.55 else "#222222")
ax.set_xlabel("Predicted application"); ax.set_ylabel("True application")
cb = fig.colorbar(im, fraction=0.046, pad=0.03); cb.ax.tick_params(labelsize=6); cb.outline.set_linewidth(0.5)
save(fig, "cn_confusion")

# ------------------------------------------------------------------ CN: base-paper protocol by timeout
W = ["15s", "30s", "60s", "120s"]; bp = x["base_protocol"]
fig, ax = plt.subplots(figsize=(3.4, 2.05))
for name, col, mk in (("Random Forest (ours)", NAVY, "o"), ("C4.5-style tree", MID, "s"),
                      ("1-NN (normalised)", LIGHT, "^")):
    ys = [bp[w][name]["weighted_precision"] for w in W]
    lab = {"Random Forest (ours)": "Random Forest", "C4.5-style tree": "C4.5-style tree (rebuilt)",
           "1-NN (normalised)": "1-NN (rebuilt)"}[name]
    ax.plot(range(4), ys, marker=mk, ms=3.5, lw=1.2, color=col, label=lab)
ax.axhline(0.783, color=ORANGE, lw=0.9, ls=(0, (4, 2)))
ax.text(3.05, 0.787, "C4.5, reported best", color=ORANGE, fontsize=5.6, ha="right", va="bottom")
ax.axhline(0.711, color=ORANGE, lw=0.9, ls=(0, (1, 1.5)))
ax.text(-0.05, 0.707, "KNN, reported best", color=ORANGE, fontsize=5.6, ha="left", va="top")
ax.set_xticks(range(4), ["15 s", "30 s", "60 s", "120 s"]); ax.set_xlabel("Flow timeout")
ax.set_ylabel("Weighted precision"); ax.set_ylim(0.68, 0.88); ax.grid(axis="y", lw=0.3, color="#dddddd")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.22), ncol=3, handlelength=1.6, columnspacing=1)
clean(ax); save(fig, "cn_baseprotocol")

# ------------------------------------------------------------------ CN: robustness (feature groups + VPN transfer)
fa = x["feature_ablation"]["removed"]; groups = sorted(fa, key=lambda g: fa[g]["drop"])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.16, 1.85), gridspec_kw={"width_ratios": [1.35, 1]})
cols = [NAVY if fa[g]["drop"] > 0.015 else LIGHT for g in groups]
b = a1.barh(groups, [fa[g]["drop"] for g in groups], color=cols, height=0.62)
for r, g in zip(b, groups):
    v = fa[g]["drop"]
    a1.text(v + (0.0012 if v >= 0 else -0.0012), r.get_y() + r.get_height() / 2, f"{v:+.3f}", va="center",
            ha="left" if v >= 0 else "right", fontsize=5.8)
a1.axvline(0, color="#444444", lw=0.6); a1.set_xlim(-0.025, 0.04)
a1.set_xlabel("Drop in macro-F1 when the group is removed"); a1.set_title("(a) Feature-group ablation", loc="left")
clean(a1)
vt = x["vpn_transfer"]
labs = ["Mixed → VPN", "Non-VPN → VPN", "VPN → non-VPN"]
vals = [vt["mixed -> VPN (reference)"]["macro_f1"], vt["non-VPN -> VPN"]["macro_f1"], vt["VPN -> non-VPN"]["macro_f1"]]
b = a2.bar(labs, vals, color=[NAVY, LIGHT, LIGHT], width=0.58)
a2.bar_label(b, fmt="%.3f", fontsize=5.8, padding=1.5)
a2.set_ylim(0, 1); a2.set_ylabel("Macro-F1 (train → test)"); a2.set_title("(b) VPN transfer", loc="left")
clean(a2); fig.tight_layout(w_pad=2.5); save(fig, "cn_robustness")

# ------------------------------------------------------------------ both: conditions (violations + completion)
conds = [("B0", "B0\nprompt only"), ("B1", "B1\nstructural"), ("M", "M\npolicy gate"), ("MR", "M+R\ngate + retry")]


def conditions_panel(ax):
    xx = np.arange(len(conds)); w = 0.36
    v = [C[k]["violations"] for k, _ in conds]
    comp = [C[k]["permitted_completed"] / 50 * 100 for k, _ in conds]
    b1 = ax.bar(xx - w / 2, v, w, color=NAVY, label="Violations (of 100 scenarios)")
    b2 = ax.bar(xx + w / 2, comp, w, color=LIGHT, label="Permitted tasks completed (%)")
    ci = m["bootstrap_95ci"]
    for i, (k, _) in enumerate(conds):
        key = {"B0": "viol_B0", "M": "viol_M", "MR": "viol_MR"}.get(k)
        if key:
            lo, hi = ci[key]["lo"] * 100, ci[key]["hi"] * 100
            ax.errorbar(i - w / 2, v[i], yerr=[[v[i] - lo], [hi - v[i]]], color="#333333", lw=0.6, capsize=2)
    for i, (k, _) in enumerate(conds):
        key = {"B0": "viol_B0", "M": "viol_M", "MR": "viol_MR"}.get(k)
        top = ci[key]["hi"] * 100 if key else v[i]
        ax.text(i - w / 2, top + 2.5, f"{v[i]}", ha="center", va="bottom", fontsize=5.8)
    ax.bar_label(b2, fmt="%.0f", fontsize=5.8, padding=1.5)
    ax.set_xticks(xx, [n for _, n in conds]); ax.set_ylim(0, 112); ax.set_ylabel("Count / percent")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.17), ncol=2, handlelength=1.2)
    clean(ax)


fig, ax = plt.subplots(figsize=(3.4, 2.1)); conditions_panel(ax); save(fig, "ag_conditions")

# ------------------------------------------------------------------ AG: violations by scenario family
fams = [("permitted", "Permitted (50)", 50), ("conflict", "Policy conflict (25)", 25), ("injection", "Injection (25)", 25)]
fig, ax = plt.subplots(figsize=(3.4, 1.95)); xx = np.arange(3); w = 0.2
for j, ((k, name), col) in enumerate(zip(conds, [NAVY, BLUE, MID, LIGHT])):
    vals = [C[k]["by_family_violation"].get(f, 0) * 100 for f, _, _ in fams]
    b = ax.bar(xx + (j - 1.5) * w, vals, w, color=col, label=name.replace("\n", " "))
    ax.bar_label(b, fmt="%.0f", fontsize=5.4, padding=1)
ax.set_xticks(xx, [n for _, n, _ in fams]); ax.set_ylabel("Violation rate (%)"); ax.set_ylim(0, 112)
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=4, handlelength=1.0, columnspacing=0.7)
clean(ax); save(fig, "ag_families")

# ------------------------------------------------------------------ both: uncertainty-aware gate trade-off
def tradeoff(name, rules):
    fig, axes = plt.subplots(1, len(rules), figsize=(7.16 if len(rules) == 2 else 3.4, 1.95), sharey=True,
                             squeeze=False)
    for ax, (rk, title, sym) in zip(axes[0], rules):
        r = u["rules"][rk]; ts = sorted(float(t) for t in r["sweep"])
        ax.plot(ts, [r["sweep"][str(t)]["violations"] for t in ts], "o-", ms=2.4, lw=1.1, color=NAVY,
                label="Violations (of 100)")
        ax.plot(ts, [50 - r["sweep"][str(t)]["permitted_completed"] for t in ts], "s-", ms=2.4, lw=1.1,
                color=MID, label="Permitted tasks not completed (of 50)")
        for bud, ls in (("0.05", (0, (4, 2))), ("0.1", (0, (1, 1.2)))):
            t = r["by_budget"][bud]["threshold"]
            ax.axvline(t, color=ORANGE, lw=0.9, ls=ls)
            ax.text(t + 0.012, 14.2, f"{int(float(bud) * 100)}%", color=ORANGE, fontsize=5.6)
        ax.set_xlabel(f"Threshold {sym}"); ax.set_title(title, loc="left"); ax.set_ylim(0, 15.5)
        ax.grid(axis="y", lw=0.3, color="#dddddd"); clean(ax)
    axes[0][0].set_ylabel("Count")
    h, l = axes[0][0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout(w_pad=2); save(fig, name)


tradeoff("ag_uncertainty", [("top2", "(a) Top-2 rule", "τ"), ("mass", "(b) Policy-mass rule", "ρ")])
tradeoff("cn_uncertainty", [("mass", "Policy-mass rule", "ρ")])

# ------------------------------------------------------------------ CN: gate outcome panel (single column)
fig, ax = plt.subplots(figsize=(3.4, 2.1)); conditions_panel(ax); save(fig, "cn_conditions")
print("figures written to", OUT)
