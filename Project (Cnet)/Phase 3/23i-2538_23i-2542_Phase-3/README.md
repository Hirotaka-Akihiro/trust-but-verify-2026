# Trust but Verify – Phase 3: Implementation and Experimental Evaluation

Computer Networks, Section DS-A
M. Abdullah Aamir (23i-2538), Haider Farooq Toor (23i-2542)

The report is `23i-2538_23i-2542_Phase-3.pdf`.

## Contents

| Path | Contents |
|---|---|
| `src/data_prep.py` | Loads ISCXVPN2016 Scenario B (15 s), cleans, samples 10,000 flows, 60/20/20 split |
| `src/train_classifiers.py` | Majority baseline, Decision Tree, Random Forest; validation selection; test evaluation; figures |
| `src/cnet_extra.py` | Base-paper re-implementation (14 classes, 10-fold CV), timeout robustness, feature-group ablation, VPN transfer |
| `src/policy.py` | Operator policy, deterministic gate (B0, B1, M), flow-state simulator |
| `src/gate_tests.py` | 20 gate test cases under B0, B1 and M |
| `src/llm_client.py`, `src/pilot.py` | Local llama.cpp client and 10 development queries |
| `src/scenarios.py`, `src/run_agent.py` | 100-scenario suite; one proposal per scenario and one retry per rejection |
| `src/evaluate.py` | Replays proposals under all conditions; metrics, bootstrap intervals, latency, figures |
| `src/audit.py` | Leakage checks and exhaustive gate-versus-scorer check |
| `data/processed/flows.csv` | The 10,000 processed flows with split assignment |
| `results/` | All metrics, the trained classifier, scenarios, raw agent replies, per-scenario outcomes, audit |
| `figures/` | All figures |

## Environment

Windows 11, Intel Core i5-1235U, 16 GB RAM, CPU only. Python 3.11.9 with scikit-learn 1.8.0, pandas 3.0.2, numpy 2.4.6, matplotlib 3.10.9.

LLM: Llama-3.2-3B-Instruct, `Llama-3.2-3B-Instruct-Q4_K_M.gguf` from `bartowski/Llama-3.2-3B-Instruct-GGUF` (SHA-256 `6c1a2b41161032677be168d354123594c0e6e67d2b9227c84f296ad037c728ff`), llama.cpp release `b12128` (Windows CPU x64). Context 2048, maximum 128 output tokens, temperature 0, seed 42, 6 threads.

## Reproducing

1. Download the ISCXVPN2016 ARFF files from https://www.unb.ca/cic/datasets/vpn.html and place `Scenario B-ARFF.zip` in `data/raw/`.
2. Place the llama.cpp CPU build in `external/llamacpp/bin/` and the model file in `external/models/`.
3. Run:

```
python src/data_prep.py
python src/train_classifiers.py
python src/cnet_extra.py
python src/gate_tests.py
python src/scenarios.py
powershell -File start_llm_server.ps1      # separate window
python src/run_agent.py
python src/evaluate.py
python src/audit.py
```

Without the model, `train_classifiers.py`, `gate_tests.py`, `evaluate.py` and `audit.py` run on the included files; `cnet_extra.py` needs the raw ARFF files. Gate latency is re-measured on each run and varies by about ±0.1 µs.
