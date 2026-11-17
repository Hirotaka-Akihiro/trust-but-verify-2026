# Agentic AI paper – writing plan

**Deliverable:** "PDF paper written in LaTeX or Word in the same format as the targeted conference or journal" (Classroom post "Final Results and Paper Writeup"; the screenshot in this folder shows **due 18 Nov**, plan below finishes by **Sun 15 Nov** to be safe).
**Authors:** M. Abdullah Aamir (23I-2538), M. Ibrahim Kiani (23I-2536).
**Quality bar:** the Computer Networks Phase 4 brief (same sections and comparison rules) – it is the most detailed written requirement either course has given.

---

## 1. Target venue and template

> **Update (17 Nov):** use the **IEEE conference template (IEEEtran, two-column, ~6 pages)** for both papers, matching the authors' earlier papers *All Dice, No Slice* and *Take the Hint*. The ACL choice below is superseded. Full verification list: `Papers/Paper_Checklist.md`.

| Decision | Choice | Why |
|---|---|---|
| Venue style | **ACL / EMNLP long paper** (ACL ARR template) | Closest peer work is ACL-family: ToolGuard (EMNLP 2025 Industry). Policy adherence of LLM agents is an NLP/agents topic. |
| Length | 8 pages main text + unlimited references, Limitations, Ethics, appendix | ACL rule; Limitations section is **mandatory** and does not count toward the 8 pages. |
| Tooling | LaTeX (MiKTeX is installed) with the official `acl-style-files` template | The brief prefers LaTeX source; ACL template handles citations (natbib, author–year). |
| Keep distinct from the Networks paper | Networks paper → IEEE two-column conference format, networking framing (classifier, ISCXVPN2016 base-paper comparison). Agentic paper → ACL format, agent-safety framing (prompt vs gate, injection, retry). | Two course papers, two framings, one shared experiment; avoids duplicate-submission concerns. |

---

## 2. What published papers like ours do (9 papers analysed)

| Paper | Venue / database | Abstract | Contributions | RQs | Results presentation | Limitations |
|---|---|---|---|---|---|---|
| ToolGuard (Zwerdling et al.) | EMNLP 2025 Industry, ACL Anthology | 112 words, 4 moves | In prose | No | Per-stage evaluation subsections; pass^k | Separate **Limitations** + **Ethical Considerations** |
| AgentSpec (Wang et al.) | ICSE 2026, ACM | ~260 words, ~10 sentences, numbers-dense | 4 bullets, each with a number | **4 explicit RQs** | Tables per RQ; overhead in ms | Threats to validity + Limitations |
| GuardAgent (Xiang et al.) | ICML 2025, PMLR | ~200 words, ends on accuracies | 4 bullets ("We propose / We create") | No | One main table + ablation tables + case studies | Only future work |
| ShieldAgent (Chen et al.) | ICML 2025, PMLR | ~230 words | In prose | No | Large tables by category; cost columns | Impact statement only |
| The Verifier Tax (Sah et al.) | CAIS 2026, ACM / arXiv | ~200 words | Inline (i)–(iv) | Implicit | 6 tables, mean ± SE; **no CIs** | Strong, specific Limitations |
| CaMeL (Debenedetti et al.) | arXiv (security) | ~160 words | 3 bullets | No | Bar charts + full tables; overhead multipliers | Explicit; "are prompt injections solved?" |
| AgentDojo (Debenedetti et al.) | NeurIPS 2024 D&B | ~190 words | In intro | No | **Utility and attack success side by side, with 95% CIs**; Pareto plots | Future work + checklist |
| AgentHarm (Andriushchenko et al.) | ICLR 2025 | ~200 words, findings (1)–(3) | 2 bullet blocks (properties, findings) | No | Tables + one multi-panel figure; no CIs | Limitations + ethics appendix |
| Intent management (Dinh et al.) | IFIP Networking 2025, IEEE style | ~175 words | 3 bullets (First/Second/Finally) | No | Tables of metrics; no variance | Brief |

**Patterns to adopt**
1. **Abstract** of ~180–220 words in one paragraph: context → gap → method → setup → 3–4 numbers → implication. Every accepted paper above puts concrete numbers in the abstract.
2. **Introduction as a funnel** ending in **3–4 bulleted contributions**, each with a measured result, then a one-paragraph roadmap (AgentSpec, GuardAgent, CaMeL).
3. **Related work by theme**, 3–4 paragraphs, each ending with a sentence positioning our work.
4. **Problem formulation / threat model** before the method, with a concrete example and formal definitions (CaMeL's security game, AgentSpec's definitions).
5. **Explicit research questions** structuring the results (AgentSpec). Most peers lack them – having them is a strength.
6. **Report utility and safety together**, with confidence intervals (AgentDojo). Our bootstrap CIs exceed what most peers report (Verifier Tax: SE only; AgentHarm, GuardAgent, intent paper: none).
7. **Case studies** of concrete failures (GuardAgent, CaMeL) – we have S055, S083, S035, S062, S043.
8. **A substantive Limitations section** (ToolGuard, Verifier Tax, CaMeL); mandatory in ACL.

**Pitfalls seen in the corpus – avoid**
- Numbers that disagree between abstract, intro and tables (ShieldAgent 2K vs 3K pairs, 11.3% vs 10.2%; AgentDojo "<25%" vs 47.69%). → Generate every number from `results/*.json`; check abstract/intro/tables against one source.
- Terms used without definition (Verifier Tax: "marathon configuration") and drifting terminology ("safety tax" vs "verifier tax"). → Keep a terminology table (Section 6) and use it verbatim.
- Typos in headings (ShieldAgent "Ovewview", GuardAgent). → Final spell-check pass.

**Style rules (common to all nine)**
- First-person plural "we"; present tense for the system and claims, past tense for what was run.
- Hedge only where the evidence is thin ("suggests", "in our setting"); state measured results plainly.
- Signpost: refer to every figure and table in the text; captions say what to conclude.
- Numbered equations and definitions; define each symbol at first use.

---

## 3. Paper outline (8 pages, ACL)

**Title options**
1. *Trust, but Verify: A Deterministic Gate for LLM Agents Enforcing Network Traffic Policy*
2. *Prompts Are Not Policies: Deterministic Gating of LLM Agents over Classified Network Traffic*

| § | Section | Content | Assets (already built) | Budget |
|---|---|---|---|---|
| – | Abstract | Context (LLM agents acting on networks) → gap (prompt-only policy; gates assume correct inputs) → method (Random Forest labels + Llama-3.2-3B + deterministic gate; replayed identical proposals) → setup (ISCXVPN2016, 100 scenarios, 5 conditions) → numbers (25/25 conflicts obeyed; 30 → 6 violations, CI 17.7–30.4; injections 3 → 0; 97.9% utility; 3.6 µs vs 2.96 s) → implication (residual risk = labels) | metrics.json | 200 words |
| 1 | Introduction | Agents act on infrastructure; policy in prompt is best-effort; gates exist (ToolGuard, AgentSpec) but assume correct facts; network traffic class comes from an imperfect classifier. RQ1–RQ3. Contributions (below). Roadmap. | – | 0.9 p |
| 2 | Related work | (a) runtime guards and policy enforcement (ToolGuard, AgentSpec, GuardAgent, ShieldAgent, PolicyGuard); (b) cost/recovery of verification (Verifier Tax); (c) prompt injection and defences (CaMeL, AgentDojo, AgentHarm, Wu & Gong policy-invisible violations); (d) LLMs in network operations (NetConfEval, Confucius, Adanza et al.). Close each with how we differ. | lit review [1]–[10] | 0.8 p |
| 3 | Problem formulation | Flow f with true class y and predicted ŷ; action a ∈ {allow, block, limit(k)}; policy Π(c) = permitted actions for class c; gate G(a, ŷ) ∈ {execute, hold}; **violation** ⇔ a executed ∧ a ∉ Π(y). Threat model: operator requests may conflict with policy; tool outputs/notes may carry injections; classifier may err. Running example S055. | policy.py | 0.6 p |
| 4 | Method | Architecture figure; classifier; agent prompt and tools; gate's 4 checks as **Algorithm 1**; retry condition M+R; why replay identical proposals (paired design). | architecture.png | 1.0 p |
| 5 | Experimental setup | Dataset and cleaning; 100-scenario suite (3 families); conditions B0/B1/M/M+R/M-oracle; metrics with formulas (violation rate, completion, retention, injection success, incorrect rejection); bootstrap; hardware, versions, seeds. | data_manifest, scenarios | 0.9 p |
| 6 | Results | **RQ1** violations table + Fig (conditions); **RQ2** completion/retention with CI; **RQ3** label-source ablation (6 → 0) + table of 6 cases; retry analysis; latency. | Tables 6–7 of report; conditions & family figures | 1.6 p |
| 7 | Comparison with base papers | Summary table (ToolGuard, Verifier Tax, AgentSpec, GuardAgent: problem, method, data, metric, reported result*, limitation); quantitative table marked *reported, different benchmark*; methodological comparison; where our gain comes from; fairness caveats. | Phase 4 brief requirement | 0.8 p |
| 8 | Ablation study | B0 → B1 → M (structural vs policy checks); predicted vs true labels; M vs M+R; Decision Tree vs Random Forest labels; VPN-transfer (classifier side). | cnet_extra.json | 0.5 p |
| 9 | Discussion | Why the gate works (policy is a lookup table); agent obeys operator (25/25, no refusal tool); gate moves risk to labels; retry satisfies the gate, not the policy (S062); practical implication: uncertainty-aware gating. | – | 0.5 p |
| 10 | Conclusion | 1 paragraph, no new facts; future work (uncertainty-aware gate, larger models, stateful rules, multi-step agents). | – | 0.2 p |
| – | Limitations (unnumbered, mandatory) | One 3B model; one 2016 dataset without capture IDs; simulated network; 100 author-written scenarios; static rules; single-step agent. | – | 0.3 p |
| – | Ethics + Declarations | Data/code availability (repo), no human subjects, AI-tool usage declaration, conflict of interest, funding: none. | – | 0.2 p |
| – | Appendix | Prompt templates, full scenario examples, gate test list, per-class F1, reproducibility commands. | src/, results/ | – |

**Contribution bullets (draft)**
- A paired evaluation of prompt-only versus deterministic gating for an LLM agent acting on classified encrypted network flows, replaying identical proposals across five conditions.
- Evidence that prompting does not enforce policy (25/25 forbidden requests executed) and that a 3.6 µs code gate cuts violations from 30 to 6 and injections from 3 to 0 while retaining 97.9% of legitimate task completion.
- An ablation isolating classifier error as the sole source of residual violations (6 → 0 with true labels), and an analysis of retry-after-rejection showing it recovers tasks but can find gate-approved unsafe actions.
- A reproducible CPU-only pipeline (code, scenarios, raw model replies) with an exhaustive gate-versus-policy check over 77,035 actions.

**Equations / algorithm to include**
- Violation rate V = (1/N) Σ 1[a_i executed ∧ a_i ∉ Π(y_i)].
- Completion C = (1/|P|) Σ_{i∈P} 1[s_i = s_i*]; retention R = C_M / C_B0.
- Paired bootstrap: resample base flows with replacement, B = 1,000; CI = 2.5th–97.5th percentiles of V_B0 − V_M.
- Algorithm 1: Gate(a, f, ŷ): dispatch → schema/range → identity → policy → execute or hold.

---

## 4. Terminology (use exactly these words)

| Term | Meaning |
|---|---|
| proposal | the agent's single JSON tool call for a scenario |
| gate | the deterministic Python checker; never "verifier" or "guard" in our own system |
| violation | an executed action not permitted for the flow's **true** class |
| held | flow state when no action executes |
| B0 / B1 / M / M+R / M-oracle | prompt only / structural checks / policy gate / gate with one retry / gate with true labels |
| permitted / conflict / injection | the three scenario families |
| completion | permitted scenario ends in exactly the requested state |
| incorrect rejection | a correct, policy-compliant first proposal rejected by the gate |

---

## 5. Schedule and split

| Day | Aamir | Ibrahim |
|---|---|---|
| Fri 13 Nov | Set up ACL LaTeX project; write §3 Problem formulation + §4 Method | Collect citations (BibTeX) for all related work; write §2 Related work |
| Sat 14 Nov | Write §5 Setup + §6 Results (tables from results JSON) | Write §7 Base-paper comparison + §8 Ablation; prepare appendix |
| Sun 15 Nov | Abstract, Introduction, Conclusion; number-consistency pass | Discussion, Limitations, Ethics/Declarations; spell-check |
| Sun 15 Nov (evening) | Joint: compile PDF, check 8-page limit, every figure/table referenced, every citation in the bibliography and vice versa | |

**Final checklist (from the Phase 4 brief)**
- [ ] Abstract 150–250 words with actual numbers
- [ ] 4–6 keywords
- [ ] Contributions as a bulleted list; roadmap paragraph
- [ ] Related work by theme with a summary table
- [ ] Problem formulation, equations, pseudocode, architecture figure
- [ ] Setup: dataset, splits, baselines, metrics, hyperparameters, hardware/software, seeds
- [ ] Results with CIs; every figure/table discussed
- [ ] Base-paper summary table, quantitative table (reported numbers marked *), improvement analysis, fairness discussion
- [ ] Ablation section; discussion with failure cases and threats to validity
- [ ] Data/code availability, conflict of interest, funding, AI-tool usage declaration
- [ ] Consistent citation style; every in-text citation in the reference list and vice versa
- [ ] All numbers traced to `implementation/results/*.json`
