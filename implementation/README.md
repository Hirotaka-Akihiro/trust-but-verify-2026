# Implementation: "Trust but Verify"

Shared experiment code for the Computer Networks (Phase 3/4) and Agentic AI projects.

## Environment (recorded 5 Nov 2026)

| Item | Value |
|---|---|
| Laptop | HP 250 G9, Intel Core i5-1235U (10 cores / 12 threads), 15.7 GB RAM, Iris Xe (unused) |
| OS / Python | Windows 11 Home 10.0.26200 / Python 3.11.9 |
| Python packages | scikit-learn 1.8.0, pandas 3.0.2, numpy 2.4.6, scipy 1.17.1, matplotlib 3.10.9 |
| LLM runtime | llama.cpp release `b12128`, Windows CPU x64 build; zip SHA-256 `2864bc950fe1681f1867ebc1bf0d6a66d18cc5561b29c285b4504787145bd7b7` (matches GitHub digest) |
| LLM | Llama-3.2-3B-Instruct, `Llama-3.2-3B-Instruct-Q4_K_M.gguf` from `bartowski/Llama-3.2-3B-Instruct-GGUF`; 2,019,377,696 bytes, SHA-256 `6c1a2b41161032677be168d354123594c0e6e67d2b9227c84f296ad037c728ff` (matches Hugging Face LFS oid) |
| LLM settings | CPU only, 6 threads, context 2048, max output 128 tokens, temperature 0, seed 42, one request at a time |

**Pilot (10 development-only queries, 5 Nov 2026):** 10/10 replies parsed as JSON; latency median 5.5 s, max 10.6 s; llama-server memory 2.6 GB (peak 3.5 GB). With Brave and Discord open, free RAM dropped to 0.9 GB, so close other apps before the final run. Pilot outputs are in `results/pilot.jsonl`; they are development data only and not reported as results.

Ollama was considered and dropped: its Windows installer is 1.6 GB of GPU libraries the integrated GPU cannot use. llama.cpp is the runtime named in the Phase 2 methodology, so no methodology change follows.

## Layout

```
src/policy.py        operator rules P1-P3, deterministic gate (B0/B1/M), dictionary simulator
src/gate_tests.py    20 hand-written gate cases, checked under all three conditions
src/llm_client.py    client for the local llama.cpp server (no JSON grammar: malformed output is measured)
src/pilot.py         10 development-only pilot queries -> results/pilot.jsonl
start_llm_server.ps1 starts llama-server on 127.0.0.1:8080
external/            llama.cpp binaries and model weights (git-ignored)
data/raw/            ISCXVPN2016 files (git-ignored; registration required at UNB CIC)
```

## Run

See [EXPERIMENTS.md](EXPERIMENTS.md) for the experiment plan, the Agentic AI retry-after-rejection extension, changes from Phase 2 and results so far.

Put the three ISCXVPN2016 `Scenario *-ARFF.zip` files in `data/raw/` (registration at https://www.unb.ca/cic/datasets/vpn.html).

```powershell
python src/data_prep.py           # clean, sample 10,000 flows, 60/20/20 split
python src/train_classifiers.py   # baseline, Decision Tree, Random Forest + figures
python src/gate_tests.py
powershell -File start_llm_server.ps1     # separate window; ~2.5-3 GB RAM
python src/pilot.py
```
