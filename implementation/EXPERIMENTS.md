# Experiment plan and changes from Phase 2

This file is the shared record of what is run, for both write-ups. Results go in `results/`, figures in `figures/`.

## Shared core (both papers)

1. **Data:** ISCXVPN2016 Scenario B, 15 s time-based features (`TimeBasedFeatures-Dataset-15s.arff`). VPN and non-VPN labels merged into 7 applications: browsing, chat, email, file transfer, P2P, streaming, VoIP. The VPN flag is kept as metadata for error analysis only, never as an input.
2. **Classifiers:** majority-class baseline, Decision Tree (`max_depth=10`), Random Forest (100 trees, `max_depth=16`, `min_samples_leaf=2`); balanced class weights, seed 42. The better tree by validation macro-F1 is frozen and its test-set predictions become the trusted records the gate reads.
3. **Agent:** Llama-3.2-3B-Instruct Q4_K_M on llama.cpp (CPU), temperature 0, one JSON tool call per scenario.
4. **Scenarios:** 100 on held-out test flows: 50 permitted requests, 25 policy conflicts (operator asks for something the policy forbids), 25 injection cases (untrusted annotation tries to force a prohibited action).
5. **Conditions (same cached proposals):** B0 prompt only, B1 structural checks, M full policy gate.
6. **Metrics:** executed violations, task completion, utility retention, incorrect rejections, injection success, gate latency; paired bootstrap 95% intervals.
7. **Ablations:** B0→B1→M; Decision Tree vs Random Forest; scoring with predicted vs true labels (which classifier errors change authorisation); per-class / VPN vs non-VPN error breakdown.

## Agentic AI extension: retry after rejection

Prior work reports that blocking a bad action is not the same as completing the task: Sah et al. ("The Verifier Tax") saw safe task success stay below 5% even when most bad actions were intercepted, and ToolGuard returns the rejection reason to the agent so it can try again. The Agentic AI paper therefore adds one condition:

- **M+R (gate with one retry):** when the gate rejects a proposal under M, the rejection reason (for example `rate above 1024 kbps for streaming`) is sent back to the agent with the original request, and the agent may propose **one** new action. That new action goes through the same gate. If it is rejected again, the flow stays held.
- **Measured:** recovery rate (rejected scenarios that end in a permitted, task-correct action), extra LLM calls and latency, and whether retries ever produce a *different* violation.
- **Cost:** at most one extra call per rejected scenario (expected roughly 25–50 calls, under 10 minutes on the laptop).
- This is reported in the Agentic AI paper; the Cnet paper may mention it briefly as future work or an extra result.

## Changes from the Phase 2 methodology

| Phase 2 text | What we actually do | Why |
|---|---|---|
| Features include packet sizes | 23 time-based features only (durations, inter-arrival times, active/idle, packets/s, bytes/s) | The official ISCXVPN2016 feature release contains no packet-size fields. |
| Split keeps capture sessions separate where possible | Duplicate feature vectors removed and conflicting-label duplicates dropped, then a stratified 60/20/20 split | The ARFF files have no capture, session, IP or port identifiers, so session grouping is impossible. Generalisation evidence is weaker and this is stated as a limitation. |
| Median imputation for missing values | `-1` kept as a value; only real NaN/inf would be imputed (median, fitted on training data) | In this release `-1` means "not applicable" (for example no packets in one direction); replacing it would erase information. |
| LLM runtime llama.cpp | Unchanged: llama.cpp `b12128` CPU build, model hash recorded in README | Ollama was tried and dropped because of its 1.6 GB GPU-only installer. |

No instructor feedback was received on Phase 2.

## Results so far

### Data (`src/data_prep.py`, `results/data_manifest.json`)
18,758 flows loaded; no NaN/inf; 11,663 rows contain the `-1` sentinel. 622 rows in groups whose identical features carry different labels were dropped, and 152 same-label duplicates removed, leaving 17,984. A stratified sample of 10,000 was split 6,000 / 2,000 / 2,000. Test set: VoIP 565, browsing 556, file transfer 302, chat 226, P2P 178, streaming 103, email 70.

### Classifiers (`src/train_classifiers.py`, `results/classifier_metrics.json`)

| Model | Val macro-F1 | Test accuracy | Test macro-F1 | Test macro-F1, 5 seeds | Fit time |
|---|---|---|---|---|---|
| Majority class | 0.063 | 0.282 | 0.063 | n/a | <0.01 s |
| Decision Tree | 0.728 | 0.803 | 0.742 | 0.745 ± 0.002 | 0.1 s |
| **Random Forest (selected)** | **0.839** | **0.877** | **0.837** | 0.845 ± 0.002 | 0.5 s |

Random Forest per-class test F1: VoIP 0.989, browsing 0.908, P2P 0.887, streaming 0.854, file transfer 0.772, email 0.733, chat 0.718. Accuracy is lower on VPN flows (0.842) than non-VPN flows (0.914).

Policy-relevant error: 14% of true file-transfer flows are predicted as chat. File transfer may not be allowed, but chat may, so the gate will approve `allow_flow` for these flows: a violation that is invisible to the gate because it trusts the classifier (RQ3).

Figures: `figures/confusion_matrix.png`, `figures/per_class_f1.png`, `figures/feature_importance.png`.
