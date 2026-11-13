"""Collect one LLM proposal per scenario (cached), then one retry for M rejections.

  results/proposals.jsonl  one line per scenario (resumable: finished IDs are skipped)
  results/retries.jsonl    retry condition (M+R): one retry for scenarios rejected under M
Needs the llama.cpp server (start_llm_server.ps1).
Run: python src/run_agent.py            (both passes)
"""
import json
from pathlib import Path

from llm_client import RETRY_TEMPLATE, build_user_prompt, propose, propose_messages
from policy import Simulator, gate

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def load_jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()] if p.exists() else []


def append(p, row):
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def main():
    scen = json.loads((RES / "scenarios.json").read_text())
    trusted = {r["flow_id"]: r["predicted"] for s in scen for r in [s["flow"]]}

    out = RES / "proposals.jsonl"
    done = {r["id"] for r in load_jsonl(out)}
    for i, s in enumerate(scen, 1):
        if s["id"] in done:
            continue
        f = s["flow"]
        prompt = build_user_prompt(f["flow_id"], f["predicted"], s["request"], s["annotation"])
        r = propose(prompt)
        append(out, {"id": s["id"], "prompt": prompt, **r})
        print(f"[{i:3d}/100] {s['id']} {s['family']:9s} {r['latency_s']:5.1f}s {r['raw'][:80]!r}", flush=True)

    # Retry condition (M+R): one retry with the gate's reason, for every M rejection.
    props = {r["id"]: r for r in load_jsonl(out)}
    rout = RES / "retries.jsonl"
    rdone = {r["id"] for r in load_jsonl(rout)}
    for s in scen:
        p = props[s["id"]]
        fid = s["flow"]["flow_id"]
        d = gate(p["proposal"], "M", fid, trusted, Simulator.for_flows(trusted).flows)
        if d.permitted or s["id"] in rdone:
            continue
        turns = [{"role": "user", "content": p["prompt"]},
                 {"role": "assistant", "content": p["raw"]},
                 {"role": "user", "content": RETRY_TEMPLATE.format(reason=d.reason)}]
        r = propose_messages(turns)
        append(rout, {"id": s["id"], "first_reason": d.reason, **r})
        print(f"retry {s['id']} ({d.reason}) -> {r['raw'][:80]!r}", flush=True)
    print("done:", len(load_jsonl(out)), "proposals,", len(load_jsonl(rout)), "retries")


if __name__ == "__main__":
    main()
