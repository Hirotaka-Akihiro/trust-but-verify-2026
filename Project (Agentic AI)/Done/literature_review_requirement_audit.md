# Literature Review Requirement Audit

Source reviewed: `C:\Users\Yurnero\Desktop\Uni Work\Semester 7\Agentic AI\Assignments\Project\Literature_Review_Trust_but_Verify.docx`

Date checked: 2026-10-04

## Overall Verdict

The literature review is mostly aligned with the Agentic AI teacher's requirements. The cited works are largely real, relevant, and recent, and the review does more than summarize papers one by one: it includes thematic synthesis, a comparison table, and a clear gap statement.

However, it should be revised before submission. The biggest issues are:

1. The comparison table's reference numbers are shifted after ReAct.
2. The review says it covers "nine peer-reviewed papers" but the reference list contains ten entries, including tau-bench as background.
3. Some claims about results and limitations should be softened where only abstracts or secondary-access pages were available, especially the Elsevier traffic-agent paper.
4. The references should include the DOI for ToolGuard and should be checked for exact author spelling and conference metadata.

## Requirement-by-Requirement Check

| Teacher requirement | Status | Notes |
|---|---|---|
| Review 8-10 related research papers | Meets | The document reviews 9 main papers and cites tau-bench as background. |
| Papers from 2022-2026 | Meets | ReAct is an arXiv 2022 paper but was published at ICLR 2023, so it fits if cited as 2023. |
| Reliable sources | Mostly meets | Sources include ACL, ICLR, PMLR/ICML, ACM, IEEE/ACM ICSE, PACM Networking, SIGCOMM, and Elsevier. PMLR/ICLR/ACL are reliable, even though not named in the teacher's examples. |
| Problem, method, dataset, result, limitation per paper | Meets with minor fixes | The table covers these fields. Add a note where the full text was not available for Adanza et al. |
| Compare and synthesize, not just summaries | Meets | Section 5 compares prompt-only, code gates, LLM verifiers, network-domain work, costs, and gaps. |
| Include comparison table | Meets | Table exists, but citation numbering must be corrected. |
| Identify limitations/gaps | Meets | Section 6 gives clear gaps tied to the proposed project. |
| IEEE-style in-text citations and references | Mostly meets | Numbered citation style is used, but the table numbering mismatch breaks consistency. |
| No fabricated citations | Mostly meets | I verified the main citations as real from publisher or reliable pages. See reference notes below. |
| Avoid plagiarism / write in own words | Likely meets | The prose appears paraphrased and not copied verbatim from the sources I checked. A formal plagiarism checker would still be needed for certainty. |

## Required Fixes Before Submission

### 1. Fix the comparison table reference numbers

The table currently labels papers incorrectly after ReAct:

| Current table label | Paper named in table | Correct reference number |
|---|---|---|
| [4] | Confucius | [5] |
| [5] | AgentSpec | [6] |
| [6] | GuardAgent | [7] |
| [7] | ShieldAgent | [8] |
| [8] | NetConfEval | [9] |
| [9] | Adanza et al. | [10] |

This is the most important formatting/content bug because it makes the table cite the wrong papers.

### 2. Clarify paper count

The introduction says:

> This review covers nine peer-reviewed papers published between 2023 and 2026.

This is defensible if tau-bench is only background, but the reference list has ten entries. To avoid confusion, revise to something like:

> This review focuses on nine main research papers, with tau-bench cited as benchmark background.

### 3. Be careful with "all nine papers are peer reviewed"

Most appear peer-reviewed or formally published, but "The Verifier Tax" should be treated carefully unless you can access the official ACM page/proceedings entry. I found evidence of the DOI and CAIS '26 conference listing, but the safest wording is:

> Most reviewed works are peer-reviewed conference or journal papers; one 2026 work should be rechecked against the official ACM proceedings before final submission.

If your teacher is strict, keep the ACM DOI but verify through your university library or ACM DL.

### 4. Strengthen the Adanza et al. limitation note

The document already says only abstract/highlights/intro were available. Keep that note, and avoid over-specific claims not visible on the publisher page. The verified public information supports:

- Article: Computer Networks, vol. 274, article 111809, January 2026.
- DOI: `10.1016/j.comnet.2025.111809`.
- Dataset/evaluation: subset of 40 intents in a real-case scenario.
- Results: factual accuracy range 70%-100%, with highlighted values of 85% query generation, 90% traffic classification, and 100% prediction process.

### 5. Add missing DOI for ToolGuard

Reference [1] should include:

`doi: 10.18653/v1/2025.emnlp-industry.41`

### 6. Decide whether tau-bench should stay in the reference list

Tau-bench is useful because ToolGuard and Verifier Tax rely on it. It is acceptable as a background citation, but it is not one of the nine reviewed papers in the table. That distinction should be explicit.

## Verified Reference Notes

### [1] ToolGuard

Verified real. ACL Anthology lists:

- Title: "Towards Enforcing Company Policy Adherence in Agentic Workflows"
- Authors: Naama Zwerdling, David Boaz, Ella Rabinovich, Guy Uziel, David Amid, Ateret Anaby Tavor
- Venue: EMNLP 2025 Industry Track
- Pages: 595-606
- DOI: `10.18653/v1/2025.emnlp-industry.41`

The document's summary matches the paper's stated two-phase buildtime/runtime guard design and tau-bench Airlines evaluation.

### [2] The Verifier Tax

Verified as a real 2026 paper/preprint with matching title, authors, and arXiv entry. Search results also showed DOI `10.1145/3786335.3813160` and CAIS '26 metadata, but I could not directly open the official ACM DOI page with the browser tool.

The document's summary matches the publicly visible abstract: tau-bench Airline/Retail, GPT-OSS-20B and GLM-4-9B, up to 94% interception, safe success below 5% in most settings, verifier cost, and identity hallucination/integrity leak behavior.

### [3] ReAct

Verified real. Published as an ICLR 2023 paper. The document's description of interleaved reasoning and acting, and the use of HotpotQA, FEVER, ALFWorld, and WebShop, is consistent with the paper.

### [4] tau-bench

Verified real. Published at ICLR 2025. It is benchmark background rather than one of the main reviewed papers. Keep it if you cite pass^k and tau-bench setup.

### [5] Confucius

Verified real. ACM SIGCOMM 2025 paper:

- Title: "Intent-Driven Network Management with Multi-Agent LLMs: The Confucius Framework"
- DOI: `10.1145/3718958.3750537`

The document's claims about DAG-style workflows, RAG/memory, integration with network tools, validation, and production deployment are consistent with the accessible paper page/PDF metadata. Some numeric claims should be kept tied to the paper rather than overstated as general results.

### [6] AgentSpec

Verified real. Author/public PDF lists:

- Title: "AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents"
- Venue: ICSE 2026
- DOI: `10.1145/3744916.3764546`

The document's summary of trigger/check/enforcement rules and the reported evaluation domains is consistent with the visible abstract.

### [7] GuardAgent

Verified real. PMLR/ICML 2025 lists the paper, authors, pages 68316-68342, and the EICU-AC and Mind2Web-SC benchmarks. The document's summary is accurate at the level needed for a literature review.

### [8] ShieldAgent

Verified real. PMLR/ICML 2025 lists "ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning." The document's claims about ShieldAgent-Bench, 3K instruction/action pairs, 6 web environments, 7 risk categories, 11.3% average improvement, 90.1% recall, and reduced API/time cost match the abstract.

### [9] NetConfEval

Verified real. PACM Networking 2024:

- Title: "NetConfEval: Can LLMs Facilitate Network Configuration?"
- DOI: `10.1145/3656296`
- Article 7, 25 pages

The document's description is broadly accurate. It should cite this as Proceedings of the ACM on Networking, not only "ACM CoNEXT," although the issue is CoNEXT2.

### [10] Adanza et al.

Verified real. Elsevier ScienceDirect lists:

- Title: "A domain-specific autonomous agent for network traffic analysis"
- Journal: Computer Networks
- Volume 274, article 111809, January 2026
- DOI: `10.1016/j.comnet.2025.111809`

The document correctly notes limited access. Keep the summary conservative unless you obtain the full text.

## Accuracy Notes on the Literature Review Text

The introduction and background are aligned with the project idea. The network-traffic-policy framing is clearly separated from the cited papers, which is good because none of the papers directly implements the exact same project.

The synthesis is one of the stronger parts. It correctly argues that:

- Prompt-only policy adherence is unreliable.
- Deterministic/code-based checks are more inspectable and cheaper than LLM verifiers.
- LLM verifiers can detect more context but introduce cost and reliability concerns.
- Existing network papers focus on configuration, operations, or traffic analysis, not traffic-flow policy enforcement driven by classifier labels.
- The proposed project's classifier-error angle is a valid differentiator.

The gap statement is also credible. I did not find evidence in the reviewed papers that directly covers "LLM policy enforcement over classified network flows with deterministic gates and classifier-error separation."

## Suggested Revision Checklist

Before submission:

1. Fix table citation numbers.
2. Add ToolGuard DOI.
3. Clarify "nine reviewed papers plus tau-bench background."
4. Recheck The Verifier Tax official ACM page through ACM DL or university access.
5. Keep Adanza et al. wording limited to abstract/highlights unless you can access the full text.
6. Run a plagiarism checker if your university provides one.
7. Make sure every numeric result in the prose appears either in the source paper or in the comparison table.

## Sources Checked

- ACL Anthology page/PDF for ToolGuard: https://aclanthology.org/2025.emnlp-industry.41/
- PMLR page for GuardAgent: https://proceedings.mlr.press/v267/xiang25a.html
- PMLR page for ShieldAgent: https://proceedings.mlr.press/v267/chen25ae.html
- Public/author PDF metadata for AgentSpec: https://cposkitt.github.io/files/publications/agentspec_llm_enforcement_icse26.pdf
- Public PDF metadata for Confucius: https://minlanyu.seas.harvard.edu/writeup/sigcomm25.pdf
- ACM/PACM metadata and repository citation for NetConfEval: https://github.com/RedHatResearch/conext24-NetConfEval
- ScienceDirect abstract/highlights for Adanza et al.: https://www.sciencedirect.com/science/article/pii/S1389128625007753
- arXiv/ICLR page for ReAct: https://arxiv.org/abs/2210.03629
- OpenReview/ICLR page for tau-bench: https://openreview.net/pdf?id=roNSXZpUDN
- arXiv entry for The Verifier Tax: https://arxiv.org/abs/2603.19328
