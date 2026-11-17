# Paper checklist – Networks paper (CN) and Agentic AI paper (AG)

Tick each box **separately for both papers**. A paper is ready only when every row is ticked for it.
Automated checks: `python Papers/paper_lint.py <CN.pdf> <AG.pdf>` (calibrated on the two reference papers, which score 0 flagged items).

---

## 0. The two papers at a glance

| | CN – Computer Networks | AG – Agentic Artificial Intelligence |
|---|---|---|
| Authors | Muhammad Abdullah Aamir (23i-2538), Haider Farooq Toor (23i-2542), Muhammad Ibrahim Kiani (23i-2536; joined the CN project with instructor permission) | Muhammad Abdullah Aamir (23i-2538), Muhammad Ibrahim Kiani (23i-2536) |
| Must **not** name | (no exclusions: all three are CN authors) | Haider Farooq Toor, 23i-2542 |
| Template | IEEE conference (IEEEtran, two-column), like the reference papers | IEEE conference (IEEEtran, two-column) |
| Length | 6 pages (reference papers); brief allows 6–9 for conferences | 6 pages |
| Lead question | How traffic-classification errors pass through a correct policy gate | Whether a deterministic gate enforces policy where prompting fails |
| Base papers | Draper-Gil et al. (ISCXVPN2016), Elshewey & Osman, ToolGuard | ToolGuard, The Verifier Tax, AgentSpec, GuardAgent |
| Emphasis | Classifier, base-paper rebuild, timeout/feature/VPN robustness, uncertainty-aware gate | Prompt vs gate, injections, retry, uncertainty-aware gate, latency |

---

## 1. Authors, identity and cross-paper mix-ups *(your item 8)*

| # | Check | CN | AG |
|---|---|---|---|
| 1.1 | Author list exactly as in §0, full names written the same way as in the reference papers ("Muhammad Abdullah Aamir") | ☐ | ☐ |
| 1.2 | No name, roll number or email from the other team anywhere (title block, acknowledgements, metadata) | ☐ | ☐ |
| 1.3 | Affiliation line matches the reference papers: "Department of Data Science, FAST-NUCES, Islamabad, Pakistan" | ☐ | ☐ |
| 1.4 | **Decided: students only.** No instructor or other faculty in the author block, footnotes or acknowledgements | ☐ | ☐ |
| 1.5 | Each author block carries that student's university email (i232538@isb.nu.edu.pk, i232542@isb.nu.edu.pk, i232536@isb.nu.edu.pk), correctly spelled | ☐ | ☐ |
| 1.6 | PDF metadata (Title, Author) matches the paper; no tool names or the other paper's title | ☐ | ☐ |
| 1.7 | File name follows the course convention (e.g. `23i-2538_23i-2542_…` for CN, `23i-2538_23i-2536_DS-A_…` for AG) | ☐ | ☐ |
| 1.8 | Title is different between the two papers and states problem, approach and domain | ☐ | ☐ |

## 2. Required sections (Phase 4 brief) and structure

| # | Check | CN | AG |
|---|---|---|---|
| 2.1 | Title and author block | ☐ | ☐ |
| 2.2 | Abstract: one paragraph, 150–250 words (reference papers: ~160), states background, problem, gap, method, dataset, **actual numbers**, conclusion | ☐ | ☐ |
| 2.3 | Index Terms: 4–6 (reference papers: 5) | ☐ | ☐ |
| 2.4 | Introduction: problem → limitations of existing work → gap → contributions as **bold-labelled bullets** → "The remainder of this paper is organized as follows" | ☐ | ☐ |
| 2.5 | Related work organised by theme (not paper by paper) with a summary table of key studies | ☐ | ☐ |
| 2.6 | Methodology: problem formulation, architecture diagram, each module, numbered equations, pseudocode for the gate | ☐ | ☐ |
| 2.7 | Experimental setup: dataset, preprocessing, splits, baselines, metrics, hyperparameters, hardware/software, seeds | ☐ | ☐ |
| 2.8 | Results and analysis with statistical evidence (95% bootstrap CIs, 5-seed mean ± std) | ☐ | ☐ |
| 2.9 | Comparison with base papers: summary table (authors/year, problem, method, dataset, metrics, results, limitations); quantitative table with reported numbers marked *; methodological comparison; absolute and relative improvement; fairness and limitations | ☐ | ☐ |
| 2.10 | Ablation study: what each component contributes | ☐ | ☐ |
| 2.11 | Discussion: why it works, implications, strengths, limitations, failure cases, threats to validity, whether the gap/objectives were met | ☐ | ☐ |
| 2.12 | Conclusion and future work: no new information | ☐ | ☐ |
| 2.13 | Declarations: data and code availability, conflict of interest, funding, **AI-tool usage declaration (required by the brief)** | ☐ | ☐ |
| 2.14 | References in IEEE style; optional appendix | ☐ | ☐ |
| 2.15 | Page count within limit; no section cut short to fit | ☐ | ☐ |
| 2.16 | Editable source (LaTeX) kept alongside the PDF | ☐ | ☐ |

## 3. Results integrity – nothing fabricated *(your item 7)*

Every number in text, tables, figures and captions must trace to a file in `implementation/results/`. No number may be typed from memory.

| # | Check | CN | AG |
|---|---|---|---|
| 3.1 | Each number in the paper appears in the canonical table below or in the named JSON file | ☐ | ☐ |
| 3.2 | Abstract, introduction, results, discussion and conclusion give **the same** value for each result (the corpus review found papers with 2K vs 3K, 11.3% vs 10.2% mismatches) | ☐ | ☐ |
| 3.3 | Every figure is generated by a script in `implementation/src/` from stored results; no figure edited by hand | ☐ | ☐ |
| 3.4 | Figure captions describe what the figure actually shows (counts, conditions, units) | ☐ | ☐ |
| 3.5 | Numbers taken from other papers are marked "reported" (*) and never mixed with our measurements | ☐ | ☐ |
| 3.6 | Claims stay within the evidence: one 3B model, one dataset, 100 scenarios; no "always", "guarantees", "state of the art" | ☐ | ☐ |
| 3.7 | Negative or mixed results reported as they are (top-2 rule removed no violations; policy-mass rule costs 4 tasks; retry added 1 violation) | ☐ | ☐ |
| 3.8 | Rounding consistent (3 decimals for F1/precision, 1 decimal for percentages and CIs) | ☐ | ☐ |
| 3.9 | Timing values quoted as measured (gate median 3.6 µs varies ±0.1 µs between runs; say "about 4 µs" if rounding) | ☐ | ☐ |

**Canonical numbers (source files)**

| Result | Value | Source |
|---|---|---|
| Flows loaded / after cleaning / sampled | 18,758 / 17,984 / 10,000 (6,000 / 2,000 / 2,000) | `data_manifest.json` |
| Conflicting-label rows / duplicates removed | 622 / 152 | `data_manifest.json` |
| Majority / DT / RF test accuracy | 0.282 / 0.803 / 0.877 | `classifier_metrics.json` |
| Majority / DT / RF test macro-F1 | 0.063 / 0.742 / 0.837 | `classifier_metrics.json` |
| 5-seed macro-F1 DT / RF | 0.745 ± 0.002 / 0.845 ± 0.002 | `classifier_metrics.json` |
| RF accuracy non-VPN / VPN | 91.4% / 84.2% | `classifier_metrics.json` |
| File transfer predicted as chat | 13.6% | `trusted_predictions.csv` |
| Base-paper protocol, 15 s weighted precision: C4.5-style / 1-NN / RF | 0.808 / 0.745 / 0.855 (reported: 0.783 / 0.711) | `cnet_extra.json` |
| RF macro-F1 by timeout 15/30/60/120 s | 0.837 / 0.861 / 0.811 / 0.812 | `cnet_extra.json` |
| Feature-group drops | fwd/bwd inter-arrival 0.030; packet/byte rate 0.025; others ≤ 0.012 | `cnet_extra.json` |
| VPN transfer macro-F1 | 0.458 (non-VPN → VPN) vs 0.806 (mixed) | `cnet_extra.json` |
| Violations B0 / B1 / M / M+R / M-oracle | 30 / 27 / 6 / 7 / 0 | `metrics.json` |
| Permitted tasks completed (of 50) | 48 / 48 / 47 / 48 / 48 | `metrics.json` |
| Injection success (of 25) | 3 / 3 / 0 / 0 / 0 | `metrics.json` |
| Injection tasks completed (of 25) | 22 / 22 / 22 / 25 / 22 | `metrics.json` |
| B0 − M violation difference | 24 pp, 95% CI 17.7–30.4 | `metrics.json` |
| Utility retention (M) | 97.9%, CI 93.5–100 | `metrics.json` |
| Retry | 25 retried, 4 recovered, 1 new violation (S062) | `metrics.json` |
| Latency | agent median 2.96 s (p95 3.75 s); gate median 3.6 µs (p95 4.4 µs) | `metrics.json` |
| Gate verification | 60/60 tests; 77,035 exhaustive cases, 0 disagreements | `audit.json` |
| Uncertainty-aware gate, policy-mass rule | 5% budget: ρ = 0.45 → 6 violations, 47 tasks; 10% budget: ρ = 0.25 → 1 violation, 43 tasks | `uncertainty_gate.json` |
| Uncertainty-aware gate, top-2 rule | 5%: τ = 0.40 → 6, 46; 10%: τ = 0.65 → 5, 43 | `uncertainty_gate.json` |
| Confidence | correct predictions median top probability 0.93; violating flows 0.38–0.71 | `uncertainty_gate.json` |

## 4. References – real, correct and matched *(your item 1)*

| # | Check | CN | AG |
|---|---|---|---|
| 4.1 | Every reference opened at its DOI or publisher page; authors, title, venue, year, volume/pages copied from there, not from memory | ☐ | ☐ |
| 4.2 | Every in-text citation is in the list and every listed reference is cited (`paper_lint.py` reports both) | ☐ | ☐ |
| 4.3 | Numbered in order of first citation (IEEE) | ☐ | ☐ |
| 4.4 | Each citation supports the exact sentence it is attached to (reported numbers checked against the source) | ☐ | ☐ |
| 4.5 | Preprints cited as arXiv with ID; published versions preferred when they exist | ☐ | ☐ |
| 4.6 | Sources whose full text was not read are not quoted for details beyond their abstract (Adanza et al.) | ☐ | ☐ |
| 4.7 | Dataset, model (Llama-3.2-3B-Instruct), runtime (llama.cpp) and libraries (scikit-learn) cited | ☐ | ☐ |
| 4.8 | Reference count similar to the reference papers (22–28) without padding | ☐ | ☐ |

**Already verified against publisher/DOI pages in earlier work** (still re-check the final BibTeX entries): Draper-Gil et al. ICISSP 2016 (10.5220/0005740704070414); Elshewey & Osman, Sci. Rep. 2025 (10.1038/s41598-025-21261-6); Zwerdling et al. ToolGuard, EMNLP 2025 Industry (10.18653/v1/2025.emnlp-industry.41); Wang et al. AgentSpec, ICSE 2026 (10.1145/3744916.3764546); Xiang et al. GuardAgent, ICML 2025 (PMLR 267); Chen et al. ShieldAgent, ICML 2025 (PMLR 267); Wang et al. NetConfEval, Proc. ACM Netw. 2024 (10.1145/3656296); Wang et al. Confucius, SIGCOMM 2025 (10.1145/3718958.3750537); Adanza et al., Comput. Netw. 2026 (10.1016/j.comnet.2025.111809); Yao et al. ReAct, ICLR 2023; Yao et al. τ-bench, ICLR 2025.
**Verify before use:** Sah et al. The Verifier Tax (ACM CAIS 2026; DOI seen only in search results); CaMeL (arXiv 2503.18813); AgentDojo (NeurIPS 2024 D&B); AgentHarm (ICLR 2025); PolicyGuard; Wu & Gong "Policy-Invisible Violations"; scikit-learn (Pedregosa et al., JMLR 2011); Breiman, Random Forests (Machine Learning 2001); Efron bootstrap.

## 5. No meta commentary, no fourth-wall breaks *(your items 2 and 3)*

| # | Check | CN | AG |
|---|---|---|---|
| 5.1 | No mention of phases, the course, assignment, instructor, rubric, deadline, submission or grading (`paper_lint.py` [META]) | ☐ | ☐ |
| 5.2 | No mention of the other paper, the other course, or "our earlier report" | ☐ | ☐ |
| 5.3 | No text addressed to a reader or helper ("Here is", "Note that we will", "feel free", "as requested", "I hope") | ☐ | ☐ |
| 5.4 | No description of how the paper was written or what will be added later | ☐ | ☐ |
| 5.5 | Changes to the method are stated as design decisions with reasons, not as "changed after feedback" | ☐ | ☐ |
| 5.6 | Scenario IDs (S054 …) appear only where they help a case study, and are introduced first | ☐ | ☐ |
| 5.7 | The paper reads as a standalone publication to someone who knows nothing about the course | ☐ | ☐ |

## 6. No leftover artifacts *(your item 4)*

| # | Check | CN | AG |
|---|---|---|---|
| 6.1 | LaTeX compiles with no "??" references, no undefined citations, no overfull boxes running into margins | ☐ | ☐ |
| 6.2 | No TODO, TBD, XXX, lorem ipsum, "[citation needed]", template text or IEEE sample text | ☐ | ☐ |
| 6.3 | No Markdown (`**`, `#`, backticks), no raw LaTeX commands visible, no code variable names (`np.float64`, `MU_mass`) in prose | ☐ | ☐ |
| 6.4 | Special characters render (µ, →, ≤, τ, ρ, en dash); no "�" | ☐ | ☐ |
| 6.5 | No widowed single word at the top of a column/page; figures and tables not separated from their first mention by more than a page | ☐ | ☐ |
| 6.6 | Condition names identical everywhere (B0, B1, M, M+R, M-oracle, M-U) and defined before use | ☐ | ☐ |
| 6.7 | Every acronym defined once at first use | ☐ | ☐ |

## 7. Diagrams and figures *(your item 5)*

Reference practice (IEEE figure guidelines; Rougier et al., "Ten Simple Rules for Better Figures"; the two reference papers):

| # | Check | CN | AG |
|---|---|---|---|
| 7.1 | **Palette mostly blue**: one blue family (e.g. #1F4E79 dark, #2F5D9A, #9DB4D3 light) plus at most one accent (orange, as the reference papers use) for the highlighted element; gray for neutral | ☐ | ☐ |
| 7.2 | No red–green contrast; the figure still reads in grayscale (line styles/markers differ, not only colour) | ☐ | ☐ |
| 7.3 | **No overlaps**: no text over lines/bars/boxes, no clipped labels, legends outside the data area; checked at 100% and 200% zoom | ☐ | ☐ |
| 7.4 | Sized for the column (≈3.5 in single, ≈7.16 in double) and created at that size, not shrunk | ☐ | ☐ |
| 7.5 | Text in figures ≥ 7 pt at print size, one font family across all figures (sans-serif as in the reference diagrams) | ☐ | ☐ |
| 7.6 | Vector PDF for diagrams and plots (or ≥ 300 dpi PNG) | ☐ | ☐ |
| 7.7 | Architecture diagram: rounded boxes, light tinted fills, labelled arrows, grouped stages (as in the reference papers); same component names as the text | ☐ | ☐ |
| 7.8 | Axes labelled with units; panel labels (a), (b) for multi-panel figures; no chartjunk (3-D, shadows, heavy gridlines) | ☐ | ☐ |
| 7.9 | Every figure and table is referred to in the text before it appears and its message is stated | ☐ | ☐ |
| 7.10 | Captions are informative (1–3 sentences, as in the reference papers) and state what to conclude | ☐ | ☐ |
| 7.11 | Table captions in IEEE form ("TABLE I", above the table); figure captions below ("Fig. 1.") | ☐ | ☐ |
| 7.12 | The two papers do not reuse an identical figure set; shared figures are re-captioned for the paper's focus | ☐ | ☐ |

## 8. Writing style matches the reference papers *(your item 6)*

Measured from *All Dice, No Slice* and *Take the Hint* (`paper_lint.py` prints the same statistics for our drafts):

| Feature | Reference papers | Target |
|---|---|---|
| Abstract | 161–164 words, one bold paragraph | 150–170 words |
| Index Terms | 5 | 5 |
| Sentence length | mean 28–32 words, median 22–25, wide spread | similar mean and **varied** lengths |
| "we" / "our" per 6 pages | 15–16 / 6–9 | same order |
| Words like *furthermore, notably, crucial* | 0–2 each | 0–2 each |
| Contributions | bullets with **bold labels** | same |
| Roadmap paragraph | "The remainder of this paper is organized as follows" | same |
| Ranges and numbers | en dashes (2.8–3.2×), percentage points, CIs in brackets | same |

| # | Check | CN | AG |
|---|---|---|---|
| 8.1 | Statistics from `paper_lint.py` fall inside the reference ranges above | ☐ | ☐ |
| 8.2 | No words from the over-used AI vocabulary list beyond the reference papers' levels (delve, showcase, underscore, intricate, pivotal, meticulous, realm, tapestry, landscape, seamless, groundbreaking, "plays a crucial role", "paves the way", "a testament to") | ☐ | ☐ |
| 8.3 | Each paragraph carries at least one concrete fact (a number, a dataset, a named method, a scenario) – no paragraph of only general statements | ☐ | ☐ |
| 8.4 | No generic openers ("In today's rapidly evolving…", "In recent years, … has gained significant attention") | ☐ | ☐ |
| 8.5 | No paragraph-closing summaries that restate the paragraph ("Overall, these results highlight…") | ☐ | ☐ |
| 8.6 | No reflexive groups of three ("efficient, scalable, and robust") unless all three are measured | ☐ | ☐ |
| 8.7 | Hedging only where evidence is thin, never stacked ("may potentially suggest") | ☐ | ☐ |
| 8.8 | Sentence openings vary (`paper_lint.py` lists openers used 5+ times) | ☐ | ☐ |
| 8.9 | Tense: present for the method and conclusions, past for what was run and measured | ☐ | ☐ |
| 8.10 | Technical terms specific to our work used precisely (flow, timeout, kbps, gate, proposal) instead of vague ones (framework, solution, system) | ☐ | ☐ |
| 8.11 | All authors read the paper aloud once and rewrite any sentence they would not write themselves | ☐ | ☐ |
| 8.12 | The AI-tool usage declaration required by the brief is present and accurate | ☐ | ☐ |

## 9. Keeping the two papers distinct

| # | Check | CN | AG |
|---|---|---|---|
| 9.1 | `paper_lint.py CN.pdf AG.pdf` shows no shared 8-word sequences beyond the affiliation line and standard terms | ☐ | ☐ |
| 9.2 | Different titles, abstracts, introductions, contribution lists and conclusions | ☐ | ☐ |
| 9.3 | Different emphasis: CN leads with classification and networking robustness; AG leads with agent behaviour, injection and retry | ☐ | ☐ |
| 9.4 | Each paper cites its own base papers in the comparison section (§0) | ☐ | ☐ |
| 9.5 | Data/code statement points to the same repository in both, worded independently | ☐ | ☐ |

## 10. Technical correctness

| # | Check | CN | AG |
|---|---|---|---|
| 10.1 | Notation defined once and used consistently (flow f, true class y, prediction ŷ, action a, policy Π(·), gate G) | ☐ | ☐ |
| 10.2 | Equations numbered and referenced; violation, completion, retention and CI definitions match the code in `evaluate.py` | ☐ | ☐ |
| 10.3 | Pseudocode of the gate matches `policy.py` (dispatch → schema/range → identity → policy) | ☐ | ☐ |
| 10.4 | Policy rules P1–P3 stated identically to `policy.py` | ☐ | ☐ |
| 10.5 | Dataset facts correct: Scenario B, 15 s, 23 features, 7 applications, no payload/IP/port | ☐ | ☐ |
| 10.6 | Known dataset caveats stated (no capture IDs; scrambled fwd/bwd column names) | ☐ | ☐ |
| 10.7 | Reproducibility details: versions, seeds (42), hardware, model hash, temperature 0 | ☐ | ☐ |

## 11. Final pass (run in this order)

1. Compile LaTeX; fix all warnings about references and overfull boxes.
2. `python Papers/paper_lint.py CN.pdf AG.pdf` – fix every [META] and [ARTIFACT] line, citation mismatch and style outlier.
3. Trace every number against §3 (one person reads numbers, the other checks the JSON).
4. Open each reference link (§4).
5. View every page at 100% and 200%; check figures (§7) and layout (§6).
6. All authors read the whole paper once, aloud (§8.11).
7. Re-run step 2 after the last edit; save PDF and LaTeX source together.
