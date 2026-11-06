# Trust but Verify: Deterministic Gating for LLM Agents Enforcing Network Traffic Policy

Agentic Artificial Intelligence, Section DS-A
M. Abdullah Aamir (23I-2538), M. Ibrahim Kiani (23I-2536)

The report is `23i-2538_23i-2536_Implementation_Report.pdf`.

## Contents

| Path | Contents |
|---|---|
| `src/data_prep.py` | Loads ISCXVPN2016 Scenario B (15 s), cleans, samples 10,000 flows, 60/20/20 split |
| `src/train_classifiers.py` | Majority baseline, Decision Tree, Random Forest; selection on validation; test evaluation; figures |
| `src/policy.py` | Operator policy, deterministic gate (conditions B0, B1, M), flow-state simulator |
| `src/gate_tests.py` | 20 gate test cases checked under B0, B1 and M |
| `src/llm_client.py` | Client for the local llama.cpp server; system prompt and retry message |
| `src/pilot.py` | 10 development queries |
| `src/scenarios.py` | Builds the 100-scenario test suite |
| `src/run_agent.py` | Collects one proposal per scenario and one retry per gate rejection |
| `src/evaluate.py` | Replays proposals through all conditions; metrics, bootstrap intervals, latency, figures |
| `src/audit.py` | Leakage checks and exhaustive gate-versus-scorer check |
| `data/processed/flows.csv` | The 10,000 processed flows with split assignment |
| `results/` | Classifier metrics and model, trusted predictions, scenarios, raw agent replies, per-scenario outcomes, metrics, audit |
| `figures/` | All generated figures; the report uses `architecture.png`, `confusion_matrix.png`, `conditions_violation_completion.png` and `violations_by_family.png` |
| `start_llm_server.ps1` | Starts the local llama.cpp server with the settings below |

## Environment

Windows 11, Intel Core i5-1235U, 16 GB RAM, CPU only. Python 3.11.9 with scikit-learn 1.8.0, pandas 3.0.2, numpy 2.4.6, matplotlib 3.10.9, joblib.

LLM: Llama-3.2-3B-Instruct, `Llama-3.2-3B-Instruct-Q4_K_M.gguf` from `bartowski/Llama-3.2-3B-Instruct-GGUF` (SHA-256 `6c1a2b41161032677be168d354123594c0e6e67d2b9227c84f296ad037c728ff`), served by llama.cpp release `b12128` (Windows CPU x64 build). Settings: context 2048, maximum 128 output tokens, temperature 0, seed 42, 6 threads.

## Reproducing

1. Download the ISCXVPN2016 ARFF files from https://www.unb.ca/cic/datasets/vpn.html and place `Scenario B-ARFF.zip` in `data/raw/`.
2. Place the llama.cpp CPU build in `external/llamacpp/bin/` and the model file in `external/models/`.
3. Run:

```
python src/data_prep.py
python src/train_classifiers.py
python src/gate_tests.py
python src/scenarios.py
powershell -File start_llm_server.ps1      # separate window
python src/run_agent.py
python src/evaluate.py
python src/audit.py
```

Without the model or the raw dataset, `train_classifiers.py` (from `data/processed/flows.csv`), `gate_tests.py`, `evaluate.py` and `audit.py` run directly on the included files and reproduce the reported values; gate latency is re-measured on each run and varies by about ±0.1 µs.
