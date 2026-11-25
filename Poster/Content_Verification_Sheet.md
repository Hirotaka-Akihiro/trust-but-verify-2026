# Content Verification Sheet: Poster and Standee

**Paper:** *Trust, but Verify the Label: Encrypted-Traffic Misclassification as the Residual Risk of Deterministic Policy Gating* (Phase 4)
**Designs checked:** A3 poster (`23i-2538_23i-2542_23i-2536_Phase-5_Poster_A3.pdf`) and 2.5 × 5 ft standee (`23i-2538_23i-2542_23i-2536_Phase-5_Standee_2.5x5ft.pdf`). Both carry identical text, numbers and figures.
**Authors:** Muhammad Abdullah Aamir (23i-2538), Haider Farooq Toor (23i-2542), Muhammad Ibrahim Kiani (23i-2536)

Every number below was checked against the paper text and against the stored results in `implementation/results/`. All figures were redrawn from those results files by `poster/source/poster_figs.py`, not copied from screenshots.

## 1. Header and research question

| # | Item on the poster | Value | Paper location | Source file | ✓ |
|---|---|---|---|---|---|
| 1 | Title and subtitle | as in the paper | Title | — | ✓ |
| 2 | Authors and roll numbers | 23i-2538, 23i-2542, 23i-2536 | Author block | — | ✓ |
| 3 | Encrypted flows, timing features | 18,758 flows, 23 features | IV, Dataset and preprocessing | `data_manifest.json` | ✓ |
| 4 | Agent scenarios on test flows | 100 scenarios, 50 flows | IV, Scenario suite | `scenarios.json` | ✓ |
| 5 | Policy rules | 3 | III-A, Eq. (1) | `implementation/src/policy.py` | ✓ |

## 2. Problem, gap and contributions (sections 01–03)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 6 | Problem statement | labels inferred from timing; check is only as correct as the prediction | Abstract; I | — | ✓ |
| 7 | Gap | accuracy reported without asking which errors change enforcement; ToolGuard and AgentSpec assume correct facts | I; II | refs [8], [10] | ✓ |
| 8 | Base-protocol gain at every timeout | at least 4.7 points | I (contribution 1); VI; Table V | `cnet_extra.json` | ✓ |
| 9 | Paired gate result | 30 → 6 violations | Abstract; V-B | `metrics.json` | ✓ |
| 10 | Error-direction claim | every remaining violation is a restricted flow predicted as more permissive | III-A; V-C; Table III | `scenario_outcomes.csv` | ✓ |

## 3. Method (section 04, Fig. 1)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 11 | Fig. 1 pipeline (redrawn) | same components and flows as paper Fig. 1 | III-B, Fig. 1 | — | ✓ |
| 12 | Gate checks in order | dispatch → schema/range → identity → policy(ŷ) | III-B, Algorithm 1 | `policy.py` | ✓ |
| 13 | Policy levels | P2P block only; streaming/file transfer block or ≤ 1,024 kbps; others allow/block/≤ 10,000 kbps | III-A, Eq. (1) | `policy.py` | ✓ |
| 14 | Why errors leak | a ∈ Π(ŷ) \ Π(y) only when a restricted flow is predicted as more permissive | III-A, after Eq. (2) | — | ✓ |
| 15 | Dataset setting | ISCXVPN2016 Scenario B, 15 s | IV | `data_manifest.json` | ✓ |
| 16 | Cleaning and split | 17,984 flows; 6,000 / 2,000 / 2,000 | IV | `data_manifest.json` | ✓ |
| 17 | Classifier | Random Forest, 100 trees, depth 16 | III-B | `classifier.joblib` | ✓ |
| 18 | Agent | Llama-3.2-3B (4-bit) on a laptop CPU | III-B; IV Implementation | `implementation/README.md` | ✓ |
| 19 | Statistics | 1,000 paired bootstrap resamples | IV, Metrics | `evaluate.py` | ✓ |

## 4. Key result (section 05, Fig. 2)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 20 | Fig. 2 bars: B0 / B1 / M / M+R / M-oracle | 30 / 27 / 6 / 7 / 0 | V-B; VII; paper Fig. 3 | `metrics.json` | ✓ |
| 21 | Fig. 2 whiskers (95% CI) | B0 24.7–35.2; M 2.0–10.6; M+R 2.7–11.8 | paper Fig. 3 | `metrics.json` (`bootstrap_95ci`) | ✓ |
| 22 | CI of the reduction | 17.7–30.4 points | Abstract; V-B | `metrics.json` | ✓ |
| 23 | Tasks kept | 97.9% (47 of 48) | Abstract; V-B | `metrics.json` | ✓ |
| 24 | Latency | 3.6 µs per gate decision vs 2.96 s per agent call | V-B | `metrics.json` | ✓ |
| 25 | Forbidden requests executed (prompt only) | 25 / 25 | V-B | `scenario_outcomes.csv` | ✓ |
| 26 | Violations with true labels | 0 | V-C; VII Label source | `metrics.json` | ✓ |
| 27 | Headline: all 6 were restricted flows labelled permissive | 6 of 6 | V-C; Table III | `scenario_outcomes.csv` | ✓ |

## 5. Evidence (sections 06–08, Figs. 3–5)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 28 | Weighted precision, base protocol | RF 0.855; +4.7 over rebuilt C4.5 (0.808); +7.2 over reported 0.783 | VI; Table V | `cnet_extra.json` | ✓ |
| 29 | Fig. 3 values by timeout | RF 0.855 / 0.845 / 0.826 / 0.819; reported C4.5 0.783, KNN 0.711 | Table V; paper Fig. 5 | `cnet_extra.json` | ✓ |
| 30 | Test macro-F1 and accuracy | 0.837; 87.7% (0.877) | Abstract; Table II | `classifier_metrics.json` | ✓ |
| 31 | File transfer predicted as chat | 13.6% (0.14 in Fig. 4) | V-A; paper Fig. 2 | `trusted_predictions.csv` | ✓ |
| 32 | Fig. 4 confusion matrix | all cells as in paper Fig. 2 | V-A; paper Fig. 2 | `trusted_predictions.csv` | ✓ |
| 33 | 10% budget | ρ = 0.25: 1 violation, 43 of 50 tasks, 89.6% retention | V-D | `uncertainty_gate.json` | ✓ |
| 34 | 5% budget | ρ = 0.45: no violation removed | V-D | `uncertainty_gate.json` | ✓ |
| 35 | Fig. 5 threshold sweep | same curves as paper Fig. 4 | V-D; paper Fig. 4 | `uncertainty_gate.json` | ✓ |

## 6. Ablation, conclusion and contact (sections 09–10)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 36 | Structural checks alone | remove 3 of 30 violations | VII, Enforcement layers | `metrics.json` | ✓ |
| 37 | Decision tree instead of RF | −0.095 macro-F1 | V-A; VII | `classifier_metrics.json` | ✓ |
| 38 | RF across timeouts | 0.811–0.861 macro-F1 | VII, Classifier and timeout | `cnet_extra.json` | ✓ |
| 39 | Trained without VPN flows | 0.458 macro-F1 on VPN flows | VII; VIII | `cnet_extra.json` | ✓ |
| 40 | Conclusion | gate stops most violations at microsecond cost but is only as correct as its label; recall of restricted vs permissive classes matters | VIII; IX | — | ✓ |
| 41 | Future work | capture-separated splits, stateful rules, policy-aware error costs | IX | — | ✓ |
| 42 | QR code | https://github.com/Hirotaka-Akihiro/trust-but-verify-2026 | Declarations | — | ✓ |

## 7. Design checks

| Check | Poster | Standee |
|---|---|---|
| Size | A3, 297 × 420 mm | 762 × 1524 mm (2.5 × 5 ft) |
| Same template, colours, fonts and figures | ✓ | ✓ |
| Figures redrawn as vector graphics, numbered, captioned and referred to in the text | ✓ | ✓ |
| Reading order numbered 01–10 | ✓ | ✓ |
| No content in the bottom 40 mm of the standee (stand base) | n/a | ✓ |
