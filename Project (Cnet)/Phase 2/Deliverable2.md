# Deliverable 2: Refined research gap

## Existing work and its limits

Network agents perform analysis and prediction [P1]; security studies assess tool-use vulnerabilities [P2] and detect threats in MCP interactions [P3]. Execution controls also exist: ToolGuards checks company policies [P4], CaMeL restricts information flows [P5], and IPIGuard constrains tool sequences [P6]. Traffic classifiers provide application predictions [P10], but prediction accuracy does not establish whether an agent's action respects network policy.

The research opportunity is to evaluate these functions together using uncertain traffic predictions. A gate can apply its rules correctly to a wrong label and still authorize an action that violates policy for the actual traffic. Conservative checks may also prevent legitimate work.

## Three-gap synthesis

| Gap | P1: Adanza et al. | P2: Gasmi et al. | P3: Polat et al. | Our experiment |
|---|---|---|---|---|
| G1: Explicit traffic-policy compliance | Evaluates network analysis/prediction | Evaluates agent attacks | Evaluates MCP threats | Check proposed actions against three application rules, including harmless requests that violate policy. |
| G2: Classification errors affecting authorization | Does not establish this experiment | Uses attack scenarios | Uses generated MCP records | Compare decisions based on predicted labels with decisions based on dataset labels. |
| G3: Security and utility in the same network trial | Does not establish our paired trial | Measures attack susceptibility | Measures threat detection | Replay identical proposals with and without enforcement; measure violations, completion and overhead. |

P4–P6 already study execution defenses. The contribution is a network-domain evaluation of classifier uncertainty, rather than a claim to invent policy gating. The gaps above describe what the reviewed evidence establishes, not an exhaustive absence of related research.

## Refined gap

**How does a lightweight deterministic gate affect policy violations, legitimate task completion and execution cost when an LLM proposes network actions from imperfect statistical flow classifications?**

We will answer this through offline replay, scoring both compliance with the predicted attributes and compliance with the dataset labels. Separate scores will distinguish agent errors, gate defects and classification errors.

## Research questions and hypotheses

| Question | Test |
|---|---|
| RQ1: Does the gate reduce executed policy violations? | H1: Full gating lowers the violation rate for identical proposals. Report the paired difference and 95% confidence interval. |
| RQ2: Does it preserve legitimate work? | H2: It retains at least 95% of ungated completion on ordinary permitted tasks. This is a target to test. |
| RQ3: How do classifier errors affect policy decisions? | Rescore the same cached proposals using dataset labels; identify prediction errors that change the permitted action set. |

RQ1 is the primary comparison. RQ2 tests practical usefulness; RQ3 explains prediction-driven errors. Measuring violations alone would reward a system that blocks everything.

## Scope and approach

The study uses ISCXVPN2016 flow statistics, Decision Tree/Random Forest application classifiers, one small local LLM, three rules and a Python simulator. Generate 100 proposals once, then replay them through prompt-only, structural-check and policy-gate conditions. Each starts from reset state and is scored independently.

The study excludes live deployment, VPN detection, confidence calibration, payload inspection and LLM training. Historical captures and constructed scenarios limit generalization. The full design appears in [Deliverable 3](Deliverable3.md); references are in [Deliverable 1](Deliverable1.md).
