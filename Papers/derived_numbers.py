"""Compute every derived number quoted in the papers from implementation/results (no hand arithmetic).

Run: python Papers/derived_numbers.py  ->  Papers/derived_numbers.json
"""
import json
from pathlib import Path

import pandas as pd

R = Path(__file__).resolve().parents[1] / "implementation" / "results"
m = json.loads((R / "metrics.json").read_text())
c = json.loads((R / "classifier_metrics.json").read_text())
x = json.loads((R / "cnet_extra.json").read_text())
u = json.loads((R / "uncertainty_gate.json").read_text())
dm = json.loads((R / "data_manifest.json").read_text())
au = json.loads((R / "audit.json").read_text())
o = pd.read_csv(R / "scenario_outcomes.csv")

bp = x["base_protocol"]["15s"]
rf, c45, nn = (bp[k]["weighted_precision"] for k in ("Random Forest (ours)", "C4.5-style tree", "1-NN (normalised)"))
REP_C45, REP_KNN = 0.783, 0.711
C = m["conditions"]
d = {
    "data": {k: dm[k] for k in ("rows_loaded", "rows_in_conflicting_label_groups", "same_label_duplicates_removed",
                                "rows_after_cleaning", "split_sizes")},
    "classifier": {n: {"val_macro_f1": round(c["models"][n]["val"]["macro_f1"], 3),
                       "test_acc": round(c["models"][n]["test"]["accuracy"], 3),
                       "test_macro_f1": round(c["models"][n]["test"]["macro_f1"], 3),
                       "per_class_f1": {k: round(v, 3) for k, v in c["models"][n]["test"]["per_class_f1"].items()}}
                   for n in ("Majority", "DecisionTree", "RandomForest")},
    "seeds": {n: [round(v["mean"], 3), round(v["std"], 3)] for n, v in c["seed_robustness"].items()},
    "vpn_acc": {k: round(v * 100, 1) for k, v in c["chosen_test_accuracy_by_vpn"].items()},
    "rf_minus_dt_macro_f1_test": round(c["models"]["RandomForest"]["test"]["macro_f1"] - c["models"]["DecisionTree"]["test"]["macro_f1"], 3),
    "base_protocol_15s": {
        "rf": round(rf, 3), "c45": round(c45, 3), "nn": round(nn, 3),
        "macro_f1": {k: round(bp[k]["macro_f1"], 3) for k in bp if isinstance(bp[k], dict)},
        "rf_vs_c45_pts": round((rf - c45) * 100, 1), "rf_vs_c45_rel": round((rf - c45) / c45 * 100, 1),
        "rf_vs_rep_c45_pts": round((rf - REP_C45) * 100, 1), "rf_vs_rep_c45_rel": round((rf - REP_C45) / REP_C45 * 100, 1),
        "rf_vs_nn_pts": round((rf - nn) * 100, 1), "rf_vs_nn_rel": round((rf - nn) / nn * 100, 1),
        "rf_vs_rep_knn_pts": round((rf - REP_KNN) * 100, 1), "rf_vs_rep_knn_rel": round((rf - REP_KNN) / REP_KNN * 100, 1),
        "c45_rebuilt_vs_reported_pts": round((c45 - REP_C45) * 100, 1),
        "rf_minus_c45_macro_f1": round(bp["Random Forest (ours)"]["macro_f1"] - bp["C4.5-style tree"]["macro_f1"], 3),
    },
    "base_protocol_all": {w: {k: round(v["weighted_precision"], 3) for k, v in x["base_protocol"][w].items()
                              if isinstance(v, dict)} for w in x["base_protocol"]},
    "timeout_rf_macro_f1": {w: round(v["Random Forest"]["macro_f1"], 3) for w, v in x["timeout_robustness"].items()},
    "timeout_dt_macro_f1": {w: round(v["Decision Tree"]["macro_f1"], 3) for w, v in x["timeout_robustness"].items()},
    "feature_drop": {g: round(v["drop"], 3) for g, v in x["feature_ablation"]["removed"].items()},
    "vpn_transfer": {k: round(v["macro_f1"], 3) for k, v in x["vpn_transfer"].items()},
    "conditions": {k: {"violations": v["violations"], "permitted_completed": v["permitted_completed"],
                       "conflict_safe": round(v["conflict_safe"] * 25), "inj_success": round(v["injection_success"] * 25),
                       "inj_tasks": round(v["injection_task_completion"] * 25), "incorrect_rej": v["incorrect_rejections"],
                       "executed": v["executed_actions"], "unsafe_neutralised": round(v["unsafe_intercepted"] * 30),
                       "by_family_pct": {f: round(p * 100) for f, p in v["by_family_violation"].items()}}
                   for k, v in C.items()},
    "ci": {k: [round(v["lo"] * 100, 1), round(v["hi"] * 100, 1)] for k, v in m["bootstrap_95ci"].items()},
    "retention_M_pct": round(m["utility_retention_M"] * 100, 1),
    "retention_MR_pct": round(m["utility_retention_MR"] * 100, 1),
    "retry": m["retry"],
    "latency": {"agent_median_s": round(m["agent_latency_s"]["median"], 2), "agent_p95_s": round(m["agent_latency_s"]["p95"], 2),
                "retry_median_s": round(m["agent_latency_s"]["retry_median"], 2),
                "gate_median_us": round(m["gate_latency"]["median_us"], 1), "gate_p95_us": round(m["gate_latency"]["p95_us"], 1),
                "ratio": round(m["agent_latency_s"]["median"] / (m["gate_latency"]["median_us"] * 1e-6))},
    "tools": m["tool_counts"], "unsafe_proposals": m["unsafe_proposals"],
    "audit": {"exhaustive": au["exhaustive_gate_cases"], "disagreements": au["gate_scorer_disagreements"]},
    "misclassified_base_flows": int(o.drop_duplicates("flow_id").eval("true != predicted").sum()),
    "ft_as_chat_pct": round((lambda p: (p[p.true == "file_transfer"].predicted == "chat").mean() * 100)(
        pd.read_csv(R / "trusted_predictions.csv")), 1),
    "uncertainty": {"rules": {k: {"by_budget": v["by_budget"], "test_split": v["test_split_label_rates"]}
                              for k, v in u["rules"].items()},
                    "confidence": u["confidence"], "violating_flows": u["violating_flows"]},
}
d["uncertainty"]["mass_10_retention_pct"] = round(u["rules"]["mass"]["by_budget"]["0.1"]["permitted_completed"] /
                                                  C["B0"]["permitted_completed"] * 100, 1)
Path(__file__).with_name("derived_numbers.json").write_text(json.dumps(d, indent=1, default=float), encoding="utf-8")
print(json.dumps(d, indent=1, default=float)[:6000])
