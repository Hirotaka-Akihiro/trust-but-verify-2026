"""Walk-through demo for the presentation video. Read-only: it never writes to results/.

Run from implementation/:  python src/demo.py          (press Enter between steps)
                           python src/demo.py --no-pause
"""
import json
import statistics
import sys
import time
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

sys.path.insert(0, str(Path(__file__).parent))
from policy import POLICY_TEXT, Simulator, gate, run_condition  # noqa: E402
from evaluate import evaluate, rates                            # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
PAUSE = "--no-pause" not in sys.argv


def step(title):
    if PAUSE:
        input("\n[Enter] ")
    print("\n" + "=" * 72 + f"\n  {title}\n" + "=" * 72)


# 1. Data -----------------------------------------------------------------------------
step("1. Data: ISCXVPN2016, encrypted flows described by timing only")
flows = pd.read_csv(ROOT / "data" / "processed" / "flows.csv")
feats = [c for c in flows.columns if c not in ("flow_id", "split", "label", "vpn")]
print(f"flows after cleaning and sampling : {len(flows):,}")
print(f"timing features per flow          : {len(feats)}  (no payload, IP or port)")
print("split sizes                       :", flows.split.value_counts().to_dict())
print("applications                      :", sorted(flows.label.unique()))

# 2. Classifier -----------------------------------------------------------------------
step("2. Classifier: the frozen Random Forest on the 2,000 test flows")
b = joblib.load(RES / "classifier.joblib")
te = flows[flows.split == "test"]
pred = b["model"].predict(b["imputer"].transform(te[b["features"]]))
print(f"model      : {b['name']} ({b['model'].n_estimators} trees, depth {b['model'].max_depth})")
print(f"accuracy   : {accuracy_score(te.label, pred):.3f}")
print(f"macro-F1   : {f1_score(te.label, pred, average='macro'):.3f}")
ft = te.label == "file_transfer"
print(f"file transfer read as chat : {100 * (pred[ft.values] == 'chat').mean():.1f}%  <- crosses a policy level")

# 3. Gate on real scenarios -----------------------------------------------------------
scen = {s["id"]: s for s in json.loads((RES / "scenarios.json").read_text())}
props = {r["id"]: r for r in map(json.loads, (RES / "proposals.jsonl").read_text(encoding="utf-8").splitlines()) if r}
trusted = {s["flow"]["flow_id"]: s["flow"]["predicted"] for s in scen.values()}
step("3. The policy the agent is given")
print(POLICY_TEXT)


def show(sid, note):
    s, p = scen[sid], props[sid]
    fid = s["flow"]["flow_id"]
    print(f"\n--- {sid} ({s['family']}) : {note}")
    print(f"true application : {s['flow']['true']:<14} classifier says : {s['flow']['predicted']}")
    print(f"operator request : {s['request']}")
    if s["annotation"]:
        print(f"untrusted note   : {s['annotation']}")
    print(f"agent's reply    : {p['raw']}")
    for cond in ("B0", "M"):
        d = gate(p["proposal"], cond, fid, trusted, Simulator.for_flows(trusted).flows)
        verdict = "EXECUTED" if d.permitted else f"HELD ({d.reason})"
        print(f"  {cond:<3}{'prompt only' if cond == 'B0' else 'policy gate':<13}: {verdict}")


step("4. Gate on three real scenarios from the experiment")
show("S061", "operator asks for something forbidden")
show("S083", "an injected note tries to change the action")
show("S054", "the classifier's label is wrong")
print("\nS054 passes the gate: the action is allowed for 'browsing', but the flow is really file transfer.")

# 4. Whole experiment -----------------------------------------------------------------
step("5. All 100 scenarios replayed under each condition (same agent replies)")
_, _, _, out = evaluate()
print(f"{'condition':<34}{'violations /100':>16}{'tasks done /50':>16}")
for c, name in (("B0", "B0   policy in the prompt only"), ("B1", "B1   + structural checks"),
                ("M", "M    + policy gate"), ("MR", "M+R  gate + one retry"), ("Moracle", "M with true labels")):
    r = rates(out, c)
    print(f"{name:<34}{r['violations']:>16}{r['permitted_completed']:>16}")

# 5. Speed ----------------------------------------------------------------------------
step("6. Cost of the gate")
times = []
for _ in range(30):
    for sid, s in scen.items():
        sim = Simulator.for_flows(trusted)
        t0 = time.perf_counter_ns()
        run_condition(props[sid]["proposal"], "M", s["flow"]["flow_id"], trusted, sim)
        times.append((time.perf_counter_ns() - t0) / 1000)
agent = statistics.median(p["latency_s"] for p in props.values())
print(f"{'gate decision (median of ' + format(len(times), ',') + ')':<34}: {statistics.median(times):.1f} microseconds")
print(f"{'agent call (median, recorded)':<34}: {agent:.2f} seconds")
print("\nDone.")
