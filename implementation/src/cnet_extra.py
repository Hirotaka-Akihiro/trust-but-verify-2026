"""Networks-specific evaluation (no LLM calls).

1. Base-paper comparison: re-implements Draper-Gil et al. (ICISSP 2016), Scenario B --
   14 classes (VPN and non-VPN kept separate), 10-fold cross-validation, a C4.5-style
   decision tree and 1-NN on min-max normalised features (Weka J48 / IBk defaults) --
   and runs our Random Forest under the same protocol, for all four flow timeouts.
2. Timeout robustness: our 7-class protocol (clean, sample 10,000, 60/20/20) on the
   15/30/60/120 s feature files.
3. Feature-group ablation: Random Forest with one feature group removed.
4. VPN transfer: train on non-VPN flows, test on VPN flows (and the reverse).

Outputs: results/cnet_extra.json, figures/timeout_robustness.png, figures/feature_ablation.png
Run: python src/cnet_extra.py
"""
import json
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

from data_prep import LABELS, load_arff

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "data" / "raw" / "Scenario B-ARFF.zip"
SEED = 42
WINDOWS = ["15s", "30s", "60s", "120s"]
GROUPS = {
    "Flow duration": ["duration"],
    "Fwd/bwd inter-arrival": ["total_fiat", "total_biat", "min_fiat", "min_biat",
                              "max_fiat", "max_biat", "mean_fiat", "mean_biat"],
    "Flow inter-arrival": ["min_flowiat", "max_flowiat", "mean_flowiat", "std_flowiat"],
    "Packet / byte rate": ["flowPktsPerSecond", "flowBytesPerSecond"],
    "Active time": ["min_active", "mean_active", "max_active", "std_active"],
    "Idle time": ["min_idle", "mean_idle", "max_idle", "std_idle"],
}
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 10, "figure.dpi": 150})


def rf():
    return RandomForestClassifier(n_estimators=100, max_depth=16, min_samples_leaf=2,
                                  class_weight="balanced", random_state=SEED, n_jobs=4)


def load(window):
    with zipfile.ZipFile(ZIP) as z:
        df = load_arff(z.read(f"Scenario B-ARFF/TimeBasedFeatures-Dataset-{window}.arff").decode("latin-1"))
    feats = [c for c in df.columns if c != "raw_label"]
    df["vpn"] = df["raw_label"].str.startswith("VPN-")
    df["label"] = df["raw_label"].str.replace("VPN-", "", regex=False).map(LABELS)
    df[feats] = df[feats].replace([np.inf, -np.inf], np.nan).fillna(-1)
    return df, feats


def clean_split(df, feats):
    """Same protocol as data_prep.py: drop conflicting/duplicate rows, sample 10,000, 60/20/20."""
    n = df.groupby(feats, dropna=False)["label"].transform("nunique")
    df = df[n == 1].drop_duplicates(subset=feats + ["label"])
    if len(df) > 10_000:
        df, _ = train_test_split(df, train_size=10_000, stratify=df["label"], random_state=SEED)
    tr, rest = train_test_split(df, test_size=0.4, stratify=df["label"], random_state=SEED)
    va, te = train_test_split(rest, test_size=0.5, stratify=rest["label"], random_state=SEED)
    return tr, va, te


def scores(y, p):
    return {"accuracy": accuracy_score(y, p),
            "weighted_precision": precision_score(y, p, average="weighted", zero_division=0),
            "weighted_recall": recall_score(y, p, average="weighted", zero_division=0),
            "macro_f1": f1_score(y, p, average="macro", zero_division=0)}


def main():
    out = {"base_paper_reported": {
        "source": "Draper-Gil et al., ICISSP 2016, Scenario B (14 classes, Weka, 10-fold CV)",
        "best_average_precision": {"C4.5": 0.783, "KNN": 0.711},
        "note": "Best average precision across timeouts, as reported in the paper text; "
                "per-timeout values appear only in its Figure 3."}}

    # 1. base-paper protocol, all windows
    out["base_protocol"] = {}
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)
    for w in WINDOWS:
        df, feats = load(w)
        X = df[feats].to_numpy(dtype=float)
        y = np.asarray(df["raw_label"].astype(str).tolist(), dtype=object)
        models = {"C4.5-style tree": DecisionTreeClassifier(criterion="entropy", min_samples_leaf=2,
                                                             random_state=SEED),
                  "1-NN (normalised)": make_pipeline(MinMaxScaler(), KNeighborsClassifier(n_neighbors=1)),
                  "Random Forest (ours)": rf()}
        out["base_protocol"][w] = {"n_flows": len(df), "n_classes": int(pd.Series(y).nunique())}
        for name, m in models.items():
            out["base_protocol"][w][name] = scores(y, cross_val_predict(m, X, y, cv=cv, n_jobs=1))
        print(w, {k: round(v["weighted_precision"], 3) for k, v in out["base_protocol"][w].items()
                  if isinstance(v, dict)})

    # 2. timeout robustness, our protocol
    out["timeout_robustness"] = {}
    splits15 = None
    for w in WINDOWS:
        df, feats = load(w)
        tr, va, te = clean_split(df, feats)
        if w == "15s":
            splits15 = (tr, va, te, feats)
        row = {"n_after_cleaning_and_sampling": len(tr) + len(va) + len(te)}
        for name, m in (("Decision Tree", DecisionTreeClassifier(max_depth=10, class_weight="balanced",
                                                                 random_state=SEED)),
                        ("Random Forest", rf())):
            m.fit(tr[feats], tr.label)
            row[name] = scores(te.label, m.predict(te[feats]))
        out["timeout_robustness"][w] = row
        print(w, "RF macro-F1", round(row["Random Forest"]["macro_f1"], 3))

    # 3. feature-group ablation (15 s, our split)
    tr, va, te, feats = splits15
    base = rf().fit(tr[feats], tr.label)
    full = f1_score(te.label, base.predict(te[feats]), average="macro")
    out["feature_ablation"] = {"all_features_macro_f1": full, "removed": {}}
    for g, cols in GROUPS.items():
        keep = [c for c in feats if c not in cols]
        m = rf().fit(tr[keep], tr.label)
        f = f1_score(te.label, m.predict(te[keep]), average="macro")
        out["feature_ablation"]["removed"][g] = {"n_removed": len(cols), "macro_f1": f, "drop": full - f}
    print("ablation", {g: round(v["drop"], 3) for g, v in out["feature_ablation"]["removed"].items()})

    # 4. VPN transfer (15 s, our split)
    out["vpn_transfer"] = {}
    for name, trm, tem in (("non-VPN -> VPN", ~tr.vpn, te.vpn), ("VPN -> non-VPN", tr.vpn, ~te.vpn),
                           ("mixed -> VPN (reference)", tr.vpn | ~tr.vpn, te.vpn)):
        m = rf().fit(tr[trm][feats], tr[trm].label)
        out["vpn_transfer"][name] = scores(te[tem].label, m.predict(te[tem][feats]))
    print("transfer", {k: round(v["macro_f1"], 3) for k, v in out["vpn_transfer"].items()})

    (ROOT / "results" / "cnet_extra.json").write_text(json.dumps(out, indent=2))

    # figures
    fig, ax = plt.subplots(figsize=(5.6, 3.0)); x = np.arange(4); w_ = 0.36
    for k, (name, col) in enumerate((("Decision Tree", "#9db4d3"), ("Random Forest", "#2f5d9a"))):
        v = [out["timeout_robustness"][w][name]["macro_f1"] for w in WINDOWS]
        b = ax.bar(x + (k - 0.5) * w_, v, w_, label=name, color=col)
        ax.bar_label(b, fmt="%.2f", fontsize=8)
    ax.set_xticks(x, [f"{w[:-1]} s" for w in WINDOWS]); ax.set_xlabel("Flow timeout")
    ax.set_ylabel("Test macro-F1"); ax.set_ylim(0, 1)
    ax.legend(frameon=False, ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    ax.spines[["top", "right"]].set_visible(False); fig.tight_layout()
    fig.savefig(ROOT / "figures" / "timeout_robustness.png", dpi=300); plt.close(fig)

    ab = out["feature_ablation"]["removed"]
    names = sorted(ab, key=lambda g: ab[g]["drop"])
    fig, ax = plt.subplots(figsize=(5.6, 2.8))
    b = ax.barh(names, [ab[g]["drop"] for g in names], color="#2f5d9a")
    ax.bar_label(b, fmt="%.3f", fontsize=8, padding=2)
    ax.set_xlim(-0.03, 0.04); ax.axvline(0, color="#555", lw=0.6)
    ax.set_xlabel("Drop in Random Forest test macro-F1 when the group is removed")
    ax.spines[["top", "right"]].set_visible(False); fig.tight_layout()
    fig.savefig(ROOT / "figures" / "feature_ablation.png", dpi=300); plt.close(fig)


if __name__ == "__main__":
    main()
