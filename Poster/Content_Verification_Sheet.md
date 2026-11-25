# Content Verification Sheet: Poster and Standee

**Paper:** *Trust, but Verify the Label: Encrypted-Traffic Misclassification as the Residual Risk of Deterministic Policy Gating* (Phase 4)
**Designs checked:** A3 poster (`23i-2538_23i-2542_23i-2536_Phase-5_Poster_A3.pdf`) and 2.5 × 5 ft standee (`23i-2538_23i-2542_23i-2536_Phase-5_Standee_2.5x5ft.pdf`). The standee is generated from the poster's content, so both carry identical text, numbers and figures.
**Authors:** Muhammad Abdullah Aamir (23i-2538), Haider Farooq Toor (23i-2542), Muhammad Ibrahim Kiani (23i-2536)

Every number below was checked against the paper text and against the stored results in `implementation/results/`. All figures were redrawn from those results files by `Poster/source/poster_figs.py`, not copied from screenshots.

## 1. Header and research question

| # | Item on the poster | Value | Paper location | Source file | ✓ |
|---|---|---|---|---|---|
| 1 | Title and subtitle | as in the paper | Title | — | ✓ |
| 2 | Authors and roll numbers | 23i-2538, 23i-2542, 23i-2536 | Author block | — | ✓ |
| 3 | Encrypted flows | 18,758 | IV, Dataset and preprocessing | `data_manifest.json` | ✓ |
| 4 | Agent scenarios | 100 | IV, Scenario suite | `scenarios.json` | ✓ |
| 5 | Policy rules | 3 | III-A, Eq. (1) | `implementation/src/policy.py` | ✓ |

## 2. Problem, gap and policy (sections 01–03)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 6 | 01 Problem | flows labelled from timing; the policy check is only as correct as the prediction | Abstract; I | — | ✓ |
| 7 | 02 Gap | accuracy reported without asking which errors change enforcement; pre-execution guards assume correct inputs | I; II | refs [8], [10] | ✓ |
| 8 | 03 Policy levels | P2P block only; streaming/file transfer block or ≤ 1,024 kbps; browsing/chat/email/VoIP allow, block or ≤ 10,000 kbps | III-A, Eq. (1) | `policy.py` | ✓ |

## 3. Method (section 04, Fig. 1)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 9 | Fig. 1 pipeline (redrawn) | same components and flows as paper Fig. 1 | III-B, Fig. 1 | — | ✓ |
| 10 | Gate checks in order | dispatch → schema/range → identity → policy(ŷ) | III-B, Algorithm 1 | `policy.py` | ✓ |
| 11 | Classifier and agent in Fig. 1 | Random Forest, 7 classes; Llama-3.2-3B (4-bit), one JSON tool call | III-B | `classifier.joblib`; `implementation/README.md` | ✓ |
| 12 | Why errors leak | a ∈ Π(ŷ) \ Π(y): a restricted flow predicted as more permissive | III-A, after Eq. (2) | — | ✓ |

## 4. Key result (section 05, Fig. 2)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 13 | Fig. 2 bars: B0 / B1 / M / M+R / M-oracle | 30 / 27 / 6 / 7 / 0 | V-B; VII; paper Fig. 3 | `metrics.json` | ✓ |
| 14 | Fig. 2 whiskers (95% CI) | B0 24.7–35.2; M 2.0–10.6; M+R 2.7–11.8 | paper Fig. 3 | `metrics.json` (`bootstrap_95ci`) | ✓ |
| 15 | CI of the reduction | 17.7–30.4 points | Abstract; V-B | `metrics.json` | ✓ |
| 16 | Headline: all 6 were restricted flows labelled permissive | 6 of 6 | V-C; Table III | `scenario_outcomes.csv` | ✓ |
| 17 | Tasks kept | 97.9% (47 of 48) | Abstract; V-B | `metrics.json` | ✓ |
| 18 | Latency | 3.6 µs per gate decision vs 2.96 s per agent call | V-B | `metrics.json` | ✓ |
| 19 | Forbidden requests obeyed (prompt only) | 25 / 25 | V-B | `scenario_outcomes.csv` | ✓ |
| 20 | Violations with true labels | 0 | V-C; VII Label source | `metrics.json` | ✓ |

## 5. Evidence (sections 06–07, Figs. 3–4)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 21 | Weighted precision, original protocol | 0.855; 4.7 points above the rebuilt C4.5 (0.808) | VI; Table V | `cnet_extra.json` | ✓ |
| 22 | Costliest error | 13.6% of file-transfer flows read as chat | V-A; paper Fig. 2 | `trusted_predictions.csv` | ✓ |
| 23 | Fig. 3 values by timeout | RF 0.855 / 0.845 / 0.826 / 0.819; reported C4.5 0.783, KNN 0.711 | Table V; paper Fig. 5 | `cnet_extra.json` | ✓ |
| 24 | Probability-aware gate, 10% budget | ρ = 0.25: 5 of 6 violations removed, 43 of 50 permitted tasks complete | V-D | `uncertainty_gate.json` | ✓ |
| 25 | Fig. 4 threshold sweep and budget lines (ρ = 0.25, 0.45) | same curves as paper Fig. 4 | V-D; paper Fig. 4 | `uncertainty_gate.json` | ✓ |

## 6. Conclusion and contact (section 08)

| # | Item | Value | Paper location | Source | ✓ |
|---|---|---|---|---|---|
| 26 | Conclusion | the gate stops most violations at microsecond cost; what gets through comes from classifier errors that move restricted traffic into a permissive class | VIII; IX | — | ✓ |
| 27 | Future work | capture-separated splits, stateful rules, classifiers whose error costs follow the policy | IX | — | ✓ |
| 28 | QR code | https://github.com/Hirotaka-Akihiro/trust-but-verify-2026 | Declarations | — | ✓ |

## 7. Design checks

| Check | Poster | Standee |
|---|---|---|
| Size | A3, 297 × 420 mm | 762 × 1524 mm (2.5 × 5 ft) |
| Same template, colours, fonts, text and figures | ✓ | ✓ |
| Figures redrawn as vector graphics, numbered (Fig. 1–4), captioned and referred to in the text | ✓ | ✓ |
| Reading order numbered 01–08 | ✓ | ✓ |
| No content in the bottom 40 mm of the standee (stand base) | n/a | ✓ |
