# Project handoff

**Snapshot:** 5 November 2026. This file records project context and decisions for the next agent. Check the actual repository state before continuing; later user instructions take priority.

## 1. Project identity and purpose

- **Course:** Computer Networks, FAST NUCES.
- **Members:** M. Abdullah Aamir (23i-2538) and Haider Farooq Toor (23i-2542), DS-A.
- **Title:** “Trust but Verify”: Deterministic Gating for LLM Agents Enforcing Network Traffic Policy.
- **Research question:** Does a deterministic check before tool execution reduce policy violations when an LLM proposes network actions from imperfect traffic classifications, while preserving legitimate task completion?

The traffic classifier is a supporting component. The central experiment compares the same proposed actions with and without policy enforcement. A benign action can violate an operator's policy; maliciousness and permission are different questions.

Existing work already implements policy gates. The contribution is a small network-domain evaluation, including how classifier mistakes affect authorization. Do not claim to invent deterministic gating or guarantee universal compliance.

## 2. Current state

Phase 1 and Phase 2 documents are present. Phase 2 has a generated submission PDF, editable Markdown, a paper-eligibility audit and a report/diagram generator. The user repeatedly requested checks against the assignment, shorter writing, a simpler methodology and an aligned diagram. Those revisions are reflected in the current files.

**No experimental implementation or results have been established in this repository.** The Python file under `Phase 2/tools/` generates documents; it is not the classifier, agent or policy-gate implementation. Dataset acquisition, training, model installation, gate implementation and experiment execution remain future work unless new files show otherwise.

The user requested this handoff in place of the newly created `AGENTS.md`. That file has been removed. This is a context document, not an automatically loaded agent-instruction file.

## 3. Repository and Git

**Updated 5 November 2026:** the old `Cnet-Project` git history was removed locally at the user's request; the user is deleting the old GitHub repositories and will create one combined repository for both courses. Layout of the combined directory (`C:\Users\Yurnero\Desktop\Uni Work\Semester 7\Agentic and Cnet Project`):

- `implementation/`: shared experiment code (classifier, gate, simulator, LLM client), used by both courses.
- `Project (Cnet)/`: Computer Networks phase documents (this file lives here).
- `Project (Agentic AI)/`: Agentic AI course documents.

No git repository is initialized yet; do not initialize, commit or push until the user creates the new remote and asks.

## 4. File map and reading order

| File | Purpose |
|---|---|
| [Phase 2/Deliverable3.md](Phase%202/Deliverable3.md) | Current methodology; read first for implementation. |
| [Phase 2/Deliverable2.md](Phase%202/Deliverable2.md) | Research gap, RQ1–RQ3 and hypotheses. |
| [Phase 2/Deliverable4.md](Phase%202/Deliverable4.md) | Diagram explanation, source attribution and step mapping. |
| [Phase 2/Deliverable1.md](Phase%202/Deliverable1.md) | Eleven-paper comparison and bibliography. |
| [Phase 2/Paper-Eligibility.md](Phase%202/Paper-Eligibility.md) | Publication checks, ranking evidence and access limits. |
| [Phase 2/README.md](Phase%202/README.md) | Package summary and requirement checklist. |
| [Phase 2/23i-2538_23i-2542_Phase-2.pdf](Phase%202/23i-2538_23i-2542_Phase-2.pdf) | Current generated submission PDF; last verified at 14 pages. |
| [Phase 2/tools/build_report.py](Phase%202/tools/build_report.py) | Rebuilds the submission PDF and PNG/SVG diagrams. |
| `Phase 2/architecture.png`, `Phase 2/architecture.svg` | Current simplified architecture exports. |
| `Phase 2/Phase 02 - Extended Literature - Research Methdology.pdf` | Instructor's Phase 2 assignment; original filename includes a typo. |
| `Phase 1/Phase 01 - Initial Literature.pdf` | Instructor's Phase 1 assignment. |
| `Phase 1/23i-2538_23i-2542_Phase-1.pdf` | Submitted Phase 1 literature analysis. |
| `Phase 2/Archive/Deliverable1-original-unverified.md` | Superseded comparison table with unverified additions; not reliable evidence. |
| `networks_project_plan.md` | Early classifier-only idea; predates the accepted agent-policy scope. |

Use the current methodology and latest user decisions over the early plan. Preserve original assignment/submission PDFs. Rebuilding the generated Phase 2 PDF is allowed when editing its sources.

## 5. User preferences and hardware constraints

The user explicitly wants a **manageable, low-stress project**, not a large research system. Target laptop: HP 250 G9, 12th-generation Core i5, 16 GB DDR4 RAM and Intel Iris Xe integrated graphics. Exact CPU SKU, available memory and inference speed were not measured. A previous system-information query was unavailable in the tool environment.

Prefer CPU execution, one model instance, sequential runs, few dependencies and short prompts. No dedicated GPU or paid inference is required by the plan. Do not promise a runtime before measuring the pilot.

Keep writing concise and direct, without filler or repeated explanations. The user prefers Times New Roman, no cover date and an easily explained diagram. Do not expand the scope with live networks, complex frameworks or extra experiments merely because they are possible.

## 6. Accepted experiment design

### Data and preprocessing

- Official [ISCXVPN2016 flow CSVs](https://www.unb.ca/cic/datasets/vpn.html); use one consistent feature/timeout variant.
- Use up to **10,000 cleaned flows**. Record source, hashes, selected rows, class counts and capture/session provenance.
- Application labels: browsing, email, chat, streaming, file transfer, VoIP and P2P, where available in the release.
- Merge VPN/non-VPN label variants into application categories. **No separate VPN prediction task.**
- Use numeric flow statistics such as duration, counts, packet sizes and timing. Exclude IPs, ports, IDs, absolute timestamps, filenames and label-derived fields from classifier inputs.
- Clean missing/infinite values and duplicates. Review conflicting-label duplicates. Do not apply the early plan's BlueStacks filter without a sourced, reproducible identification rule.
- Target **60/20/20 train/validation/test**, with capture/session separation where possible. Group separation takes priority over exact ratios. If only duplicate groups are recoverable, disclose the weaker generalization evidence.
- Fit median imputation on training data only. No scaling or confidence calibration is required.

### Classifiers

- Decision Tree: `max_depth=10`.
- Random Forest: 100 trees, `max_depth=16`, `min_samples_leaf=2`.
- Both use balanced class weights and seed 42.
- Include a majority-class sanity baseline. Select the better tree model by validation macro-F1; freeze it before final testing. **Only the selected classifier feeds the agent.**
- No parameter search, deep classifier or repeated training-seed study is required.

### Local LLM

- [Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct), using a [4-bit GGUF release](https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF) with llama.cpp.
- One CPU instance; context limit 2,048 tokens; output limit 128 tokens; temperature zero.
- Input: flow ID, predicted application, operator request and written policy. Optional injected annotations are explicitly marked untrusted.
- Output: one JSON action proposal. No arbitrary generated code executes.
- Ten development-only pilot queries check usability, memory and latency. Record the exact quantization, file hash, runtime and prompt. Select any necessary alternative using development data, before final tests.
- This is inference only; no LLM training or fine-tuning.

### Actions and policy

| Action | Arguments |
|---|---|
| `allow_flow` | `flow_id` |
| `block_flow` | `flow_id` |
| `rate_limit_flow` | `flow_id`, integer `kbps` in 64–10000 |

| Application | Permitted actions |
|---|---|
| P2P | Block only. |
| Streaming or file transfer | Block, or limit to 64–1024 kbps. |
| Browsing, email, chat or VoIP | Allow, block, or limit to 64–10000 kbps. |

These are experimental operator rules, not a dataset annotation. Unknown labels or missing trusted records lead to rejection and a held flow.

### Gate, simulator and conditions

The deterministic gate is a small Python function outside the LLM. It reads the trusted classifier record directly, checks schema, parameter types/ranges, episode flow ID and policy, then permits or rejects the exact proposed action. The LLM cannot rewrite trusted records or bypass the executor.

Use a dictionary simulator storing disposition/rate; every episode starts held. A rejected proposal stays held, with its decision and unchanged state logged. It is not equivalent to executing `block_flow`.

| Condition | Checks |
|---|---|
| B0: Prompt only | Agent sees policy; recognized proposals dispatch without application-policy enforcement. |
| B1: Structural checks | Schema, rate range and flow identity. |
| M: Policy gate | B1 plus application rules. |

Even B0 has a fixed dispatcher; malformed/unknown calls cannot run host commands. Define and log dispatcher failures consistently so B1's contribution is interpretable.

Use **the same cached proposals** and separately reset simulator state for every condition. Ground-truth labels never enter the predicted-label agent or gate. An independently authored decision table scores actual outcomes; it must not reuse the gate's decision function.

### Scenario and query budget

- Select **50 held-out flows**: ten each from P2P, streaming and file transfer, plus twenty from remaining applications where available.
- Create **100 scenarios**: 50 permitted requests, 25 harmless policy conflicts and 25 annotation-injection cases.
- Conflict/injection cases reuse restricted flows. Preserve base-flow and capture IDs for grouped analysis.
- Specify expected outcomes and attacker goals before final querying. Do not exclude classifier mistakes.
- Generate one proposal per scenario: **100 final LLM calls plus ten pilot calls**.
- Replay outputs through all conditions without new inference. No repeated generations, correction loop or separate oracle-context LLM trial.
- Rescore cached actions using true labels to study prediction-driven policy disagreements; this costs no extra LLM calls.
- Write **20 independently reviewed gate-test cases** covering valid actions and schema/identity/policy failures.

If available data cannot support these counts or a pilot shows the model is unusable, document the adjustment before final evaluation. Do not fabricate missing classes or results.

## 7. Research questions and evaluation

- **RQ1/H1:** Does M reduce executed policy violations compared with B0 for identical proposals? Primary effect: paired violation-rate difference in percentage points, with a 95% interval.
- **RQ2/H2:** Does M preserve useful completion? Target: at least 95% of B0's completion rate on permitted scenarios. This is a target, not an achieved result; use N/A if B0 completion is zero.
- **RQ3:** Which classifier mistakes change authorization under the written rules? Rescore existing proposals rather than generating a new trial.

Report classifier accuracy, macro/per-class F1 and confusion matrix; executed policy violations per assigned scenario and per executed action; task completion; utility retention; incorrect rejection; unsafe-action interception; injection success; gate correctness; and median/p95 agent and gate latency. Include numerators/denominators. Blocking or rejecting everything cannot count as completing ordinary allow/limit requests.

The written methodology specifies 1,000 paired bootstrap samples, resampling capture groups where known or base flows otherwise, preserving reused scenarios. Few independent captures make uncertainty exploratory. Gate timing replays cached proposals 30 times without new model calls.

Ablations reuse B0/B1/M: structural validation, then application-policy checks. Inspect every executed violation and incorrect rejection. Separate prediction, agent, argument, identity, gate and execution errors. Preserve refusals, malformed outputs and negative findings; never alter final prompts to force an apparent improvement.

## 8. Literature and evidence limits

Phase 1 requires three 2026 Q1-journal research articles. Phase 2 requires eight to ten additional 2025–2026 research papers, explicitly permitting conferences and book chapters as well as Q1/Q2 journals. The current table has the original three plus **eight additions**, P4–P11.

| IDs | Studies / role |
|---|---|
| P1–P3 | Adanza network agent; Gasmi Function Calling/MCP vulnerability study; Polat MCP monitoring. |
| P4–P6 | ToolGuards, CaMeL and IPIGuard: execution controls and direct prior art. |
| P7–P9 | AgentHarm, BrowserART and AgentAuditor: agent behavior and evaluation methods. |
| P10 | Elshewey/Osman encrypted-flow classification. |
| P11 | Environmental Injection Attack: untrusted-input attack design. |

Official publication references and eligibility findings are in the linked files. Seven additions are conference papers and one is a journal article. Some evidence transfers agent-security methods from non-network domains; do not describe their datasets or reported percentages as our network-policy results.

Q1 evidence for the original journals uses named **2024 SJR snapshots** released in March 2025. Do not relabel these as 2026 quartiles or assign journal quartiles to conferences. P1's journal issue is 2026 despite its DOI containing 2025.

**Full published text was not accessible for P1–P3 or P5 through the sources used.** Their current summaries are limited to publisher abstracts/section snippets. Metadata/eligibility verification is not full-text verification. Do not turn prior submission-readiness assurances into a claim that every experimental detail or instructor interpretation is guaranteed correct. The archived original extended table contains unverified citations and numerical claims; do not restore them as facts.

## 9. Report and diagram workflow

The report is generated from `Deliverable1.md` through `Deliverable4.md`. Edit those sources, then rebuild:

```powershell
python "Phase 2/tools/build_report.py"
```

Required packages: ReportLab and Pillow. The generator loads Windows Times New Roman fonts from `C:/Windows/Fonts`. For inspection, earlier work used pypdf and pypdfium2. If Python/packages are unavailable, use the Codex desktop dependency-discovery tool; the cached runtime path is version-dependent and should not be hard-coded into new instructions.

The script rebuilds the named Phase 2 PDF plus `architecture.png` and `architecture.svg`. Keep **Times New Roman throughout**, **no cover date**, and the student's submission filename. The report contains a landscape cross-paper table and architecture page. Recheck actual page count after changes rather than assuming 14 indefinitely.

The user approved a simplified three-stage diagram:

1. Dataset → cleaning/splitting → selected application classifier.
2. Request and prediction → small local LLM → 100 cached proposals.
3. Identical proposals → ungated/gated simulation → independent evaluation.

Written rules and trusted predictions feed the gate; dataset truth and expected outcomes feed evaluation. B1 is explained in the caption, avoiding another branch. Rejections remain held and are scored. The source attribution is an adaptation of **Zwerdling et al., ToolGuards Figure 1, p. 597**, [official paper](https://aclanthology.org/anthology-files/pdf/emnlp/2025.emnlp-industry.41.pdf#page=3). Our implementation is manual and adds the traffic-classifier/evaluation stages; it does not reproduce automated guard generation.

After edits, check all twelve methodology steps, current counts/model settings, RQ/metric correspondence, diagram/caption consistency, embedded image, fonts, cover and local links. Render changed PDF pages for visual inspection. Keep `README.md` synchronized. A prior pypdfium2 version did not accept negative page indices: use `document[len(document)-1]` for the final page.

## 10. What the next agent should do

Follow the next user request; do not automatically launch the whole experiment merely because implementation is described here. If asked to start implementation, proceed in small working stages:

1. Inspect repository status and any new course instructions or files. The Phase 3 assignment, deadline and rubric are not present in this snapshot.
2. Audit/download the selected CSV variant, verify the real label schema and capture identifiers, and record a reproducible subset/split. The documented category counts are planned, not measured.
3. Train the two small classifiers and freeze selection using validation data. Save the feature mapping and preprocessing with the model.
4. Implement the three rules, action schemas, dictionary simulator and independent expected outcomes. Verify the twenty gate cases.
5. Install/run the small local model and ten-query pilot. Measure memory/runtime and freeze prompt/model settings before final querying.
6. Prepare the reviewed 100-scenario suite, collect proposals once, replay all conditions and compute metrics/uncertainty/failure examples.
7. Write actual findings without converting expectations into achievements. Any methodology change must be reflected in sources, diagram and generated report.

Open practical checks include exact CSV columns/timeouts, capture-group availability, label mapping, usable class counts, exact GGUF quantization, runtime compatibility and pilot speed. The task-success labels also need an explicit reviewed acceptable-state list for each scenario. These are implementation work, not results already obtained.

## 11. Working preferences and repository hygiene

Use clear, brief progress updates. Complete authorized routine work without repeated confirmation questions. Ask only when genuinely missing information blocks the next step; do not silently change the research objective.

Once the combined repository exists, inspect Git status and preserve unrelated user changes. A new document request is not automatically a push request. Do not force-push or rewrite history without explicit authorization.

Keep credentials, downloaded model weights, large raw captures and temporary PDF review images out of commits. Prefer source links, hashes, configuration and reproducible scripts. Report what was verified and any remaining material limit; do not promise perfect accuracy, a grade or unmeasured laptop performance.
