"""Train majority baseline, Decision Tree and Random Forest; select on validation; test once.

Outputs:
  results/classifier_metrics.json   val/test metrics, selection, seed-robustness study
  results/trusted_predictions.csv   frozen model's test predictions (the gate's trusted records)
  results/classifier.joblib         frozen model + feature list + imputer
  figures/confusion_matrix.png, figures/per_class_f1.png, figures/feature_importance.png
Run: python src/train_classifiers.py
"""
import json
import time
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parents[1]
SEED = 42
ORDER = ["browsing", "chat", "email", "file_transfer", "p2p", "streaming", "voip"]
NICE = {"browsing": "Browsing", "chat": "Chat", "email": "Email", "file_transfer": "File transfer",
        "p2p": "P2P", "streaming": "Streaming", "voip": "VoIP"}
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 10, "figure.dpi": 150})


def models(seed):
    return {
        "Majority": DummyClassifier(strategy="most_frequent"),
        "DecisionTree": DecisionTreeClassifier(max_depth=10, class_weight="balanced", random_state=seed),
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=16, min_samples_leaf=2,
                                               class_weight="balanced", random_state=seed, n_jobs=4),
    }


def metrics(y, p):
    return {"accuracy": accuracy_score(y, p),
            "macro_precision": precision_score(y, p, average="macro", zero_division=0),
            "macro_recall": recall_score(y, p, average="macro", zero_division=0),
            "macro_f1": f1_score(y, p, average="macro", zero_division=0),
            "weighted_f1": f1_score(y, p, average="weighted", zero_division=0),
            "per_class_f1": dict(zip(ORDER, f1_score(y, p, labels=ORDER, average=None, zero_division=0)))}


def main():
    df = pd.read_csv(ROOT / "data" / "processed" / "flows.csv")
    feats = [c for c in df.columns if c not in ("flow_id", "split", "label", "vpn")]
    tr, va, te = (df[df.split == s] for s in ("train", "val", "test"))
    imp = SimpleImputer(strategy="median").fit(tr[feats])
    Xtr, Xva, Xte = (imp.transform(d[feats]) for d in (tr, va, te))

    res, fitted = {}, {}
    for name, m in models(SEED).items():
        t0 = time.perf_counter(); m.fit(Xtr, tr.label); fit_s = time.perf_counter() - t0
        fitted[name] = m
        res[name] = {"fit_seconds": round(fit_s, 3), "val": metrics(va.label, m.predict(Xva))}
    chosen = max(("DecisionTree", "RandomForest"), key=lambda n: res[n]["val"]["macro_f1"])

    # Test once, after selection is frozen.
    preds = {}
    for name, m in fitted.items():
        t0 = time.perf_counter(); preds[name] = m.predict(Xte)
        res[name]["predict_ms_per_flow"] = round((time.perf_counter() - t0) / len(te) * 1000, 4)
        res[name]["test"] = metrics(te.label, preds[name])
    best = fitted[chosen]

    # Robustness: training-seed variation (cheap; frozen model stays seed 42).
    seeds = {}
    for name in ("DecisionTree", "RandomForest"):
        scores = [f1_score(te.label, models(s)[name].fit(Xtr, tr.label).predict(Xte), average="macro")
                  for s in range(5)]
        seeds[name] = {"seeds": list(range(5)), "test_macro_f1": scores,
                       "mean": float(np.mean(scores)), "std": float(np.std(scores, ddof=1))}

    # VPN vs non-VPN accuracy of the chosen model (VPN flag never used as a feature).
    vpn = {("vpn" if v else "non_vpn"): float(accuracy_score(te.label[te.vpn == v], preds[chosen][te.vpn == v]))
           for v in (True, False)}

    out = {"selected_by_val_macro_f1": chosen, "models": res, "seed_robustness": seeds,
           "chosen_test_accuracy_by_vpn": vpn,
           "chosen_report": classification_report(te.label, preds[chosen], labels=ORDER,
                                                  output_dict=True, zero_division=0)}
    (ROOT / "results" / "classifier_metrics.json").write_text(json.dumps(out, indent=2))
    pd.DataFrame({"flow_id": te.flow_id, "predicted": preds[chosen], "true": te.label, "vpn": te.vpn}
                 ).to_csv(ROOT / "results" / "trusted_predictions.csv", index=False)
    joblib.dump({"model": best, "imputer": imp, "features": feats, "name": chosen},
                ROOT / "results" / "classifier.joblib", compress=3)

    figs = ROOT / "figures"
    # Confusion matrix (row-normalised).
    cm = confusion_matrix(te.label, preds[chosen], labels=ORDER, normalize="true")
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(7), [NICE[c] for c in ORDER], rotation=40, ha="right")
    ax.set_yticks(range(7), [NICE[c] for c in ORDER])
    for i in range(7):
        for j in range(7):
            ax.text(j, i, f"{cm[i, j]:.2f}", ha="center", va="center", fontsize=8,
                    color="white" if cm[i, j] > 0.6 else "black")
    ax.set_xlabel("Predicted application"); ax.set_ylabel("True application")
    fig.colorbar(im, fraction=0.046); fig.tight_layout()
    fig.savefig(figs / "confusion_matrix.png", dpi=300); plt.close(fig)

    # Per-class F1 for the two trees.
    fig, ax = plt.subplots(figsize=(6, 3.2)); w = 0.38; x = np.arange(7)
    for k, (name, col) in enumerate((("DecisionTree", "#9db4d3"), ("RandomForest", "#2f5d9a"))):
        ax.bar(x + (k - 0.5) * w, [res[name]["test"]["per_class_f1"][c] for c in ORDER], w,
               label=name.replace("Tree", " Tree").replace("Forest", " Forest"), color=col)
    ax.set_xticks(x, [NICE[c] for c in ORDER], rotation=20); ax.set_ylim(0, 1)
    ax.set_ylabel("Test F1"); ax.legend(frameon=False, ncol=2, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False); fig.tight_layout()
    fig.savefig(figs / "per_class_f1.png", dpi=300); plt.close(fig)

    # Feature importance of the chosen model (top 12).
    imp_s = pd.Series(best.feature_importances_, index=feats).sort_values().tail(12)
    fig, ax = plt.subplots(figsize=(5, 3.6))
    ax.barh(imp_s.index, imp_s.values, color="#2f5d9a"); ax.set_xlabel("Impurity-based importance")
    ax.spines[["top", "right"]].set_visible(False); fig.tight_layout()
    fig.savefig(figs / "feature_importance.png", dpi=300); plt.close(fig)

    print(f"selected: {chosen}")
    for n in res:
        print(f"{n:13s} val F1 {res[n]['val']['macro_f1']:.3f} | test acc {res[n]['test']['accuracy']:.3f} "
              f"macroF1 {res[n]['test']['macro_f1']:.3f} | fit {res[n]['fit_seconds']}s")
    for n, s in seeds.items():
        print(f"{n} test macro-F1 over 5 seeds: {s['mean']:.3f} ± {s['std']:.3f}")
    print("per-class F1 (chosen):", {c: round(v, 3) for c, v in res[chosen]['test']['per_class_f1'].items()})
    print("accuracy by VPN:", {k: round(v, 3) for k, v in vpn.items()})


if __name__ == "__main__":
    main()
