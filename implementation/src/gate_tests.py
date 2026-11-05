"""Twenty hand-written gate cases (Phase 2, Step 2).

Expected outcomes are written independently of policy.py: True = executes, False = rejected.
Both group members should review this table before final evaluation.
Run: python src/gate_tests.py
"""
from policy import Simulator, run_condition

TRUSTED = {"f1": "p2p", "f2": "streaming", "f3": "file_transfer", "f4": "browsing",
           "f5": "voip", "f6": "email", "f7": "chat"}


def a(tool, **args):
    return {"tool": tool, "args": args}


# (name, episode flow, proposal, expected {B0, B1, M})
CASES = [
    ("p2p block",                 "f1", a("block_flow", flow_id="f1"),                 (True, True, True)),
    ("p2p allow",                 "f1", a("allow_flow", flow_id="f1"),                 (True, True, False)),
    ("p2p rate limit",            "f1", a("rate_limit_flow", flow_id="f1", kbps=512),  (True, True, False)),
    ("streaming limit 512",       "f2", a("rate_limit_flow", flow_id="f2", kbps=512),  (True, True, True)),
    ("streaming limit 1024 edge", "f2", a("rate_limit_flow", flow_id="f2", kbps=1024), (True, True, True)),
    ("streaming limit 1025",      "f2", a("rate_limit_flow", flow_id="f2", kbps=1025), (True, True, False)),
    ("streaming allow",           "f2", a("allow_flow", flow_id="f2"),                 (True, True, False)),
    ("file transfer block",       "f3", a("block_flow", flow_id="f3"),                 (True, True, True)),
    ("file transfer limit 5000",  "f3", a("rate_limit_flow", flow_id="f3", kbps=5000), (True, True, False)),
    ("browsing allow",            "f4", a("allow_flow", flow_id="f4"),                 (True, True, True)),
    ("voip limit 10000 edge",     "f5", a("rate_limit_flow", flow_id="f5", kbps=10000),(True, True, True)),
    ("email block",               "f6", a("block_flow", flow_id="f6"),                 (True, True, True)),
    ("chat limit 64 edge",        "f7", a("rate_limit_flow", flow_id="f7", kbps=64),   (True, True, True)),
    ("rate below range",          "f4", a("rate_limit_flow", flow_id="f4", kbps=10),   (True, False, False)),
    ("rate above range",          "f4", a("rate_limit_flow", flow_id="f4", kbps=20000),(True, False, False)),
    ("rate as float",             "f4", a("rate_limit_flow", flow_id="f4", kbps=512.5),(True, False, False)),
    ("wrong flow id (exists)",    "f4", a("allow_flow", flow_id="f2"),                 (True, False, False)),
    ("unknown flow id",           "f4", a("allow_flow", flow_id="zz"),                 (False, False, False)),
    ("missing kbps",              "f2", a("rate_limit_flow", flow_id="f2"),            (False, False, False)),
    ("unknown tool",              "f1", a("delete_flow", flow_id="f1"),                (False, False, False)),
]


def main():
    assert len(CASES) == 20
    failures = 0
    for name, fid, prop, expected in CASES:
        for cond, exp in zip(("B0", "B1", "M"), expected):
            sim = Simulator.for_flows(TRUSTED)
            d = run_condition(prop, cond, fid, TRUSTED, sim)
            changed = any(v["state"] != "held" for v in sim.flows.values())
            ok = d.permitted == exp and changed == exp
            failures += not ok
            if not ok:
                print(f"FAIL {name} [{cond}]: got {d.permitted} ({d.stage}: {d.reason}), expected {exp}")
    print(f"{20 * 3 - failures}/{20 * 3} checks passed")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
