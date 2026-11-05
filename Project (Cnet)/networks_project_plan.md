# Machine Learning-Based Classification of Encrypted Network Traffic Using Statistical Flow Features

*Provisional title — Computer Networks Research Project, FAST NUCES*

## Research Question

Can statistical flow-level features (packet size, timing, direction — no payload inspection) reliably classify encrypted network traffic by VPN-usage and/or application category?

## Why This Is Feasible

- **No GPU required.** The approach works on ~80 numeric features per flow, not raw packets — classical ML (Decision Tree, Random Forest, XGBoost) trains on a laptop CPU in minutes.
- **Established, still-active research area.** This is the same core approach used in papers published this year (2026) on the same problem — it's a well-trodden but not "solved" area, especially as more traffic moves to TLS 1.3/QUIC.
- **No custom data collection needed.** Public benchmark datasets already exist with flow features pre-extracted.
- **Scoped to be extendable.** Start with a working baseline; extend toward a more novel "hook" if time allows.

## Dataset

**ISCXVPN2016** (Canadian Institute for Cybersecurity, UNB) — `unb.ca/cic/datasets/vpn.html`
- Ships both raw `.pcap` files and a **pre-extracted CSV of flow features** (the CSV is what we actually use — skips needing to run a flow-extraction tool ourselves)
- 14 traffic labels across VoIP, P2P, Browsing, Chat, Email, File Transfer, Streaming — each with a VPN and non-VPN version
- **Known caveat:** prior research found data-quality issues (a large share of flows come from a BlueStacks emulator and should be filtered; some "VPN" captures leak unencrypted payload). We'll note this filtering step explicitly in the methodology — it strengthens rather than weakens the project.

## Methodology (high level)

1. Acquire dataset CSV; filter known problematic flows (BlueStacks-origin biflows)
2. Choose classification target: binary (VPN vs non-VPN) and/or multi-class (7 application categories)
3. Preprocess: handle missing/infinite values, stratified train/test split
4. Train and compare classical ML models: Decision Tree, Random Forest, XGBoost
5. Evaluate with accuracy, precision/recall, F1, confusion matrix (not accuracy alone — classes are imbalanced)
6. Pick one analytical "hook" to go beyond plain reproduction (pick one, based on time available):
   - **Generalization test** — train on ISCXVPN2016, test on a second dataset (e.g. VNAT) to show real-world robustness (or lack of it)
   - **Feature efficiency** — how few features can we use and still get strong accuracy?
   - **Error analysis** — which categories get confused, and why?

## Differentiation From Similar Class Projects

One classmate group is doing encrypted/malware traffic classification via deep learning on raw traffic. Ours differs on both method (classical ML on flow statistics, not deep learning on raw packets) and target (traffic-type/VPN classification, not malware) — worth a one-line note in the proposal to make this explicit.

## Rough Timeline

| Phase | Focus |
|---|---|
| Weeks 1–2 | Related work, finalize dataset + classification target |
| Weeks 3–4 | Data cleaning, filtering, feature prep |
| Weeks 5–6 | Model training and comparison |
| Weeks 7–8 | Evaluation, chosen "hook" analysis |
| Final weeks | Report writing, results writeup |

## Deliverables

- Proposal (this doc, refined)
- Short related-work summary (3–4 cited papers)
- Working classification pipeline + results (metrics, confusion matrix, feature importance)
- Final report covering methodology, results, and discussion of failure cases
