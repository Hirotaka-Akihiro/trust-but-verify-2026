"""Integrity checks on the finished experiment (reads existing outputs; no LLM calls).

1. Trusted records come only from the test split.
2. No identical feature vector is shared between train and val/test.
3. Every prompt shows the predicted label, and no prompt leaks a different true label.
4. Exhaustive check: gate M (true labels) == independent scorer on every tool x app x integer rate.
5. Column-order check on the ISCX feature names (min must not exceed max).
Run: python src/audit.py
"""
import json
from pathlib import Path

import pandas as pd

from evaluate import compliant
from policy import TOOLS, Simulator, gate

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "results"
APPS = ["browsing", "chat", "email", "file_transfer", "p2p", "streaming", "voip"]
STATE = {"allow_flow": "allowed", "block_flow": "blocked", "rate_limit_flow": "limited"}


def main():
    f = pd.read_csv(ROOT / "data" / "processed" / "flows.csv")
    feats = [c for c in f.columns if c not in ("flow_id", "split", "label", "vpn")]
    t = pd.read_csv(R / "trusted_predictions.csv")
    out = {"trusted_records_test_only": set(f.set_index("flow_id").loc[t.flow_id, "split"]) == {"test"}}

    key = lambda d: set(map(tuple, d[feats].round(9).values))
    tr = key(f[f.split == "train"])
    out["shared_vectors_train_val"] = len(tr & key(f[f.split == "val"]))
    out["shared_vectors_train_test"] = len(tr & key(f[f.split == "test"]))

    sc = {s["id"]: s for s in json.loads((R / "scenarios.json").read_text())}
    shown = leaked = 0
    for line in (R / "proposals.jsonl").read_text(encoding="utf-8").splitlines():
        p = json.loads(line); fl = sc[p["id"]]["flow"]
        shown += f"Classifier prediction: {fl['predicted']}\n" in p["prompt"]
        leaked += fl["true"] != fl["predicted"] and fl["true"] in p["prompt"]
    out["prompts_with_predicted_label"], out["prompts_leaking_true_label"] = shown, leaked

    n = dis = 0
    for app in APPS:
        for tool in TOOLS:
            for k in ([None] if tool != "rate_limit_flow" else [*range(0, 11001), -5, 20000]):
                args = {"flow_id": "x"} if k is None else {"flow_id": "x", "kbps": k}
                d = gate({"tool": tool, "args": args}, "M", "x", {"x": app}, Simulator.for_flows(["x"]).flows)
                n += 1; dis += d.permitted != compliant(app, {"state": STATE[tool], "kbps": k})
    out["exhaustive_gate_cases"], out["gate_scorer_disagreements"] = n, dis

    pairs = [("min_fiat", "max_fiat"), ("min_biat", "max_biat"), ("min_flowiat", "max_flowiat"),
             ("min_active", "max_active"), ("min_idle", "max_idle")]
    out["share_min_exceeds_max"] = {}
    for a, b in pairs:
        v = f[(f[a] >= 0) & (f[b] >= 0)]
        out["share_min_exceeds_max"][f"{a}>{b}"] = round(float((v[a] > v[b]).mean()), 3)

    (R / "audit.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
