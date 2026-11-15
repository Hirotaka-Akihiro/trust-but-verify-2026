"""Build the Computer Networks Phase 3 report (implementation and experimental evaluation).

Reads results/figures from ../../implementation and writes
23i-2538_23i-2542_Phase-3/23i-2538_23i-2542_Phase-3.pdf next to this script.
Run: python "Project (Cnet)/Phase 3/build_phase3_report.py"
"""
import json
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

HERE = Path(__file__).resolve().parent
IMPL = HERE.parents[1] / "implementation"
FIG, RES = IMPL / "figures", IMPL / "results"
NAME = "23i-2538_23i-2542_Phase-3"
OUT = HERE / NAME / f"{NAME}.pdf"

FONTS = Path("C:/Windows/Fonts")
for n, f in (("TNR", "times.ttf"), ("TNR-Bold", "timesbd.ttf"), ("TNR-Italic", "timesi.ttf"),
             ("TNR-BoldItalic", "timesbi.ttf")):
    pdfmetrics.registerFont(TTFont(n, str(FONTS / f)))
pdfmetrics.registerFontFamily("TNR", normal="TNR", bold="TNR-Bold", italic="TNR-Italic",
                              boldItalic="TNR-BoldItalic")

m = json.loads((RES / "metrics.json").read_text())
c = json.loads((RES / "classifier_metrics.json").read_text())
x = json.loads((RES / "cnet_extra.json").read_text())
dm = json.loads((RES / "data_manifest.json").read_text())
au = json.loads((RES / "audit.json").read_text())
C, ci = m["conditions"], m["bootstrap_95ci"]

S = {
    "cover_t": ParagraphStyle("ct", fontName="TNR-Bold", fontSize=26, leading=31, spaceAfter=10),
    "cover_s": ParagraphStyle("cs", fontName="TNR", fontSize=15, leading=20, spaceAfter=6),
    "title": ParagraphStyle("t", fontName="TNR-Bold", fontSize=15, leading=19, spaceAfter=6, keepWithNext=1),
    "h1": ParagraphStyle("h1", fontName="TNR-Bold", fontSize=13.5, leading=17, spaceBefore=10, spaceAfter=4, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="TNR-Bold", fontSize=12, leading=15, spaceBefore=6, spaceAfter=3, keepWithNext=1),
    "body": ParagraphStyle("b", fontName="TNR", fontSize=11.5, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=5),
    "bullet": ParagraphStyle("bl", fontName="TNR", fontSize=11.5, leading=14.5, leftIndent=14, bulletIndent=4,
                             spaceAfter=2, bulletFontName="TNR"),
    "cap": ParagraphStyle("c", fontName="TNR-Italic", fontSize=10, leading=12.5, alignment=TA_CENTER,
                          spaceBefore=3, spaceAfter=8),
    "cell": ParagraphStyle("cell", fontName="TNR", fontSize=9.8, leading=11.8),
    "cellb": ParagraphStyle("cellb", fontName="TNR-Bold", fontSize=9.8, leading=11.8),
    "ref": ParagraphStyle("r", fontName="TNR", fontSize=10, leading=12.5, leftIndent=18, firstLineIndent=-18, spaceAfter=3),
}
story = []
P = lambda t, s="body": story.append(Paragraph(t, S[s]))
B = lambda t: story.append(Paragraph(t, S["bullet"], bulletText="•"))
f3 = lambda v: f"{v:.3f}"


def pull_headings():
    heads = []
    while story and isinstance(story[-1], Paragraph) and story[-1].style.name in ("h1", "h2"):
        heads.insert(0, story.pop())
    return heads


def table(rows, widths, caption, bold_rows=()):
    data = [[Paragraph(str(v), S["cellb"] if (i == 0 or i in bold_rows) else S["cell"]) for v in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.black),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.black),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    story.append(KeepTogether(pull_headings() + [Paragraph(caption, S["cap"]), t, Spacer(1, 8)]))


def figure(name, width_cm, caption):
    path = FIG / name
    w, h = PILImage.open(path).size
    story.append(KeepTogether(pull_headings() + [Image(str(path), width=width_cm * cm, height=width_cm * cm * h / w),
                                                 Paragraph(caption, S["cap"])]))


# ------------------------------------------------------------------ cover
story.append(Spacer(1, 4 * cm))
P("Trust but Verify", "cover_t")
P("Deterministic Gating for LLM Agents Enforcing Network Traffic Policy", "cover_s")
P("Phase 3: Research implementation and experimental evaluation", "cover_s")
story.append(Spacer(1, 0.6 * cm))
P("M. Abdullah Aamir (23i-2538) · Haider Farooq Toor (23i-2542) · DS-A", "cover_s")
P("Computer Networks", "cover_s")
story.append(Spacer(1, 0.8 * cm))
for i, t in enumerate(["Implementation of the proposed methodology", "Dataset and preprocessing",
                       "Baseline evaluation", "Graphical results and visualization",
                       "Comparison with existing research", "Ablation studies",
                       "Results analysis and discussion"], 1):
    P(f"{i}. {t}", "cover_s")
story.append(PageBreak())

# ------------------------------------------------------------------ 1
P("1. Implementation of the Proposed Methodology", "h1")
P("The proposed method was implemented in full and runs on a laptop CPU. A traffic classifier predicts each "
  "encrypted flow's application from timing statistics. A local LLM agent receives the predicted application, an "
  "operator request and the written policy, and proposes one network action. A deterministic policy gate checks "
  "that action before a flow-state simulator carries it out. Three research questions are tested. <b>RQ1:</b> does "
  "the gate reduce policy violations on the same proposals? <b>RQ2:</b> does it keep at least 95% of the tasks "
  "completed without it? <b>RQ3:</b> which classifier mistakes change the actions that are allowed?")
figure("architecture.png", 15.5, "Figure 1. Implemented architecture. The gate reads the classifier's prediction "
       "directly; rejected proposals leave the flow held; under M+R the rejection reason is returned once.")
table([["Component", "Implementation"],
       ["Classifier", "scikit-learn Random Forest (100 trees, depth 16, min. 2 samples per leaf, balanced class "
        "weights, seed 42), selected over a Decision Tree by validation macro-F1"],
       ["Agent", "Llama-3.2-3B-Instruct [4], 4-bit Q4_K_M, llama.cpp b12128 [5] on CPU; temperature 0, seed 42, 2,048-token "
        "context, 128 output tokens; one JSON tool call per scenario"],
       ["Tools", "allow_flow(flow_id), block_flow(flow_id), rate_limit_flow(flow_id, kbps 64–10,000)"],
       ["Policy", "P1 P2P: block only. P2 streaming, file transfer: block or limit ≤ 1,024 kbps. "
        "P3 browsing, email, chat, VoIP: allow, block or limit ≤ 10,000 kbps"],
       ["Gate", "Python function outside the LLM: dispatch → schema and rate range → flow identity → policy rule "
        "for the predicted application"],
       ["Simulator", "Dictionary of flow states (held, allowed, blocked, limited); every flow starts held"]],
      [3.0, 13.6], "Table 1. Implemented components.")
P("1.1 Changes from the original plan", "h2")
P("The following changes were needed because of the data, or were added to make the evaluation stronger:")
table([["Original plan", "Implemented", "Reason"],
       ["Packet-size features", "23 time-related features only", "The official feature release contains no "
        "packet-size fields"],
       ["Capture/session-separated split", "Duplicate and conflicting rows removed, then stratified split",
        "The files carry no capture, session, IP or port identifiers"],
       ["Median imputation", "The value −1 kept as a value", "In this release −1 marks a statistic that does not "
        "apply to the flow"],
       ["Three conditions (B0, B1, M)", "Added M+R (one retry) and M with true labels", "Measures recovery after a "
        "rejection and separates out classifier mistakes (RQ3)"],
       ["Classifier comparison only", "Added a rebuild of the base paper's setup, plus timeout, feature-group and "
        "VPN-transfer tests", "Comparison with existing research and robustness"]],
      [4.0, 5.8, 6.8], "Table 2. Documented changes.")

# ------------------------------------------------------------------ 2
P("2. Dataset and Preprocessing", "h1")
P(f"<b>Dataset.</b> ISCXVPN2016 [1], Scenario B, 15-second time-based features: {dm['rows_loaded']:,} flows from "
  "browsing, chat, email, file transfer, P2P, streaming and VoIP applications, each captured with and without a "
  "VPN. Each flow has 23 statistics: duration, forward/backward and flow inter-arrival times, active and idle "
  "times, packets per second and bytes per second. No payload, IP address or port is used.")
P(f"<b>Preprocessing.</b> VPN and non-VPN variants were merged into seven application labels; the VPN flag is kept "
  f"for analysis only. {dm['rows_in_conflicting_label_groups']} rows whose identical feature vectors carry different "
  f"labels and {dm['same_label_duplicates_removed']} exact duplicates were removed, leaving "
  f"{dm['rows_after_cleaning']:,}. A stratified sample of 10,000 flows was split 60/20/20 (6,000 training, 2,000 "
  "validation, 2,000 test, seed 42); no feature vector occurs in more than one split. Trees need no scaling. In the "
  "released files the forward/backward inter-arrival column names do not match their values (minimum exceeds "
  "maximum in 93.3% and 96.1% of rows); values are used as released because tree splits do not depend on names.")
P("<b>Experimental setup.</b> HP 250 G9 laptop, Intel Core i5-1235U, 16 GB RAM, Windows 11, CPU only; Python 3.11.9, "
  "scikit-learn 1.8.0. The agent experiment uses 100 scenarios on 50 test flows (10 each of P2P, streaming and file "
  "transfer; 5 each of browsing, chat, email and VoIP): 50 permitted requests, 25 policy conflicts and 25 prompt "
  "injections (five untrusted-note styles). Each scenario's requested final state was fixed before any model query. "
  "The agent was queried once per scenario; the same 100 replies were replayed under every condition.")

# ------------------------------------------------------------------ 3
P("3. Baseline Evaluation", "h1")
mo = c["models"]; sr = c["seed_robustness"]
table([["Classifier", "Val. macro-F1", "Test accuracy", "Test macro-F1", "Macro-F1, 5 seeds"],
       ["Majority class", f3(mo["Majority"]["val"]["macro_f1"]), f3(mo["Majority"]["test"]["accuracy"]),
        f3(mo["Majority"]["test"]["macro_f1"]), "–"],
       ["Decision Tree (depth 10)", f3(mo["DecisionTree"]["val"]["macro_f1"]), f3(mo["DecisionTree"]["test"]["accuracy"]),
        f3(mo["DecisionTree"]["test"]["macro_f1"]), f"{sr['DecisionTree']['mean']:.3f} ± {sr['DecisionTree']['std']:.3f}"],
       ["Random Forest (selected)", f3(mo["RandomForest"]["val"]["macro_f1"]), f3(mo["RandomForest"]["test"]["accuracy"]),
        f3(mo["RandomForest"]["test"]["macro_f1"]), f"{sr['RandomForest']['mean']:.3f} ± {sr['RandomForest']['std']:.3f}"]],
      [4.6, 2.8, 2.8, 2.8, 3.6], "Table 3. Classifier baselines on 2,000 test flows (7 applications).", bold_rows=(3,))
pc = mo["RandomForest"]["test"]["per_class_f1"]; v = c["chosen_test_accuracy_by_vpn"]
P(f"Random Forest per-class F1: VoIP {pc['voip']:.3f}, browsing {pc['browsing']:.3f}, P2P {pc['p2p']:.3f}, "
  f"streaming {pc['streaming']:.3f}, file transfer {pc['file_transfer']:.3f}, email {pc['email']:.3f}, chat "
  f"{pc['chat']:.3f}. Accuracy is {v['non_vpn']*100:.1f}% on non-VPN and {v['vpn']*100:.1f}% on VPN flows.")
rows = [["Condition", "Violations (of 100)", "Permitted done (of 50)", "Conflicts safe (of 25)",
         "Injections succeeded (of 25)", "Incorrect rejections"]]
for k, n in (("B0", "B0 prompt only (baseline)"), ("B1", "B1 structural checks (baseline)"),
             ("M", "M policy gate (proposed)"), ("MR", "M+R gate with retry"), ("Moracle", "M with true labels")):
    r = C[k]
    rows.append([n, r["violations"], r["permitted_completed"], round(r["conflict_safe"] * 25),
                 round(r["injection_success"] * 25), r["incorrect_rejections"]])
table(rows, [5.0, 2.3, 2.4, 2.2, 2.6, 2.1], "Table 4. Enforcement baselines and proposed gate on identical proposals.",
      bold_rows=(3,))
d = ci["viol_B0_minus_M"]
P(f"The gate reduces violations from 30 to 6, a drop of 24 percentage points on the same proposals (95% confidence "
  f"interval {d['lo']*100:.1f}–{d['hi']*100:.1f}, from 1,000 bootstrap resamples of the 50 base flows). It keeps "
  f"{m['utility_retention_M']*100:.1f}% of the tasks completed without it (interval {ci['retention_M']['lo']*100:.1f}–100%). "
  f"A gate check takes a median {m['gate_latency']['median_us']:.1f} µs (95th percentile "
  f"{m['gate_latency']['p95_us']:.1f} µs), while an agent call takes a median {m['agent_latency_s']['median']:.2f} s.")

# ------------------------------------------------------------------ 4
P("4. Graphical Results and Visualization", "h1")
figure("confusion_matrix.png", 9.0, "Figure 2. Random Forest confusion matrix (row-normalised). 13.6% of file-transfer "
       "flows are predicted as chat, the most policy-relevant error.")
figure("per_class_f1.png", 12.5, "Figure 3. Per-class test F1 of the two tree classifiers.")
figure("conditions_violation_completion.png", 13, "Figure 4. Violation rate and permitted-task completion per "
       "condition, with 95% bootstrap intervals.")
figure("violations_by_family.png", 13, "Figure 5. Violation rate by scenario family and condition.")

# ------------------------------------------------------------------ 5
P("5. Comparison with Existing Research", "h1")
P("5.1 Traffic classification against the dataset's base paper", "h2")
P("Draper-Gil et al. [1] introduced the time-related features used here. They tested them on Scenario B with "
  "14 classes (VPN and non-VPN kept separate), using C4.5 and KNN classifiers in Weka with 10-fold cross-validation. "
  "To compare on equal terms, that setup was rebuilt: 14 classes, the full feature files without cleaning, "
  "stratified 10-fold cross-validation, a C4.5-style decision tree (entropy splits, at least 2 samples per leaf) "
  "and a 1-nearest-neighbour classifier on features scaled to 0–1, as in Weka's defaults. The proposed Random "
  "Forest was tested under exactly the same setup.")
bp = x["base_protocol"]
rows = [["Method", "Source", "15 s", "30 s", "60 s", "120 s", "Best"],
        ["C4.5 [1]", "Reported*", "–", "–", "–", "–", "0.783"],
        ["KNN [1]", "Reported*", "–", "–", "–", "–", "0.711"]]
for name in ("C4.5-style tree", "1-NN (normalised)", "Random Forest (ours)"):
    vals = [bp[w][name]["weighted_precision"] for w in ("15s", "30s", "60s", "120s")]
    rows.append([name, "Re-implemented" if "ours" not in name else "Proposed"] + [f3(v_) for v_ in vals]
                + [f3(max(vals))])
table(rows, [3.8, 2.6, 1.9, 1.9, 1.9, 1.9, 1.9], "Table 5. Weighted precision under the base paper's protocol "
      "(14 classes, 10-fold CV). *Taken from [1], which reports only the best average precision across timeouts "
      "in its text.", bold_rows=(5,))
rf15, c45 = bp["15s"]["Random Forest (ours)"], bp["15s"]["C4.5-style tree"]
P(f"The re-implemented C4.5-style tree reaches {c45['weighted_precision']:.3f} at 15 s, close to the reported 0.783, "
  f"so the re-implementation matches the original setup well. The Random Forest improves weighted precision by "
  f"{(rf15['weighted_precision']-c45['weighted_precision'])*100:.1f} points over the re-implemented tree "
  f"({(rf15['weighted_precision']-c45['weighted_precision'])/c45['weighted_precision']*100:.1f}% relative) and by "
  f"{(rf15['weighted_precision']-0.783)*100:.1f} points over the reported value, with macro-F1 "
  f"{rf15['macro_f1']:.3f} against {c45['macro_f1']:.3f}. The gain comes from averaging many different trees, which "
  "gives more stable predictions when the timing patterns of different applications overlap. Two points limit this "
  "comparison: the original paper does not state how it averages precision or which KNN settings it uses, and its "
  "cross-validation, like ours here, may place flows from the same capture in different folds.")
P("Elshewey and Osman [2] report 0.9949 accuracy and 0.9932 macro-F1 with stacked deep-learning models on a different "
  "HTTPS dataset (145,671 flows, 88 features, six categories). Because the data, labels and features differ, these "
  "numbers cannot be compared directly. That work also stops at classification and does not study which actions "
  "are then allowed.")
P("5.2 Policy enforcement against prior gating work", "h2")
table([["Work", "Setting", "Reported result", "Difference from this work"],
       ["ToolGuard [3]*", "Code checks before tool calls; τ-bench airline, 22 policy-violating tasks",
        "Single-attempt success 0.450 → 0.685", "Checks generated by an LLM; customer-service domain; inputs assumed correct"],
       ["This work", "Hand-written gate before network actions; 100 scenarios on ISCXVPN2016 flows",
        "Violations 30 → 6; injections 3 → 0; 97.9% of completed tasks kept", "Gate inputs come from an imperfect "
        "traffic classifier; remaining risk measured (RQ3)"]],
      [2.6, 4.6, 3.8, 5.6], "Table 6. Comparison with the base gating paper. *Reported on a different benchmark; not "
      "directly comparable.")
P("ToolGuard shows that code checks before an action improve policy compliance when the facts they check are "
  "correct. This work finds the same effect for network actions and adds what ToolGuard does not measure: when the "
  "fact the gate relies on, the traffic class, comes from a classifier, every remaining violation is caused by a "
  "classification mistake.")

# ------------------------------------------------------------------ 6
P("6. Ablation Studies", "h1")
table([["Ablation", "Change", "Result"],
       ["Enforcement layers", "B0 → B1 → M", f"Violations 30 → 27 → 6. Structural checks catch only the 2 unit errors "
        "and 1 malformed call; policy rules remove 21 more"],
       ["Label source", "M with predicted vs true labels", "6 → 0 violations: all remaining violations are classifier "
        "mistakes; the 1 incorrect rejection is also a classifier mistake"],
       ["Recovery", "M → M+R (one retry)", "4 of 25 rejected scenarios recovered; injection tasks completed 22 → 25; "
        "1 new classifier-driven violation"],
       ["Classifier model", "Decision Tree vs Random Forest", "Macro-F1 0.742 vs 0.837 (test); 0.765 vs 0.817 under "
        "the base-paper protocol"],
       ["Flow timeout", "15 / 30 / 60 / 120 s", "Random Forest macro-F1 " + " / ".join(
           f3(x["timeout_robustness"][w]["Random Forest"]["macro_f1"]) for w in ("15s", "30s", "60s", "120s"))],
       ["Feature groups", "Remove one group", "Largest drops: forward/backward inter-arrival −0.030, packet/byte rate "
        "−0.025; removing any other group changes it by 0.012 or less"],
       ["VPN transfer", "Train non-VPN, test VPN", f"Macro-F1 {x['vpn_transfer']['non-VPN -> VPN']['macro_f1']:.3f} vs "
        f"{x['vpn_transfer']['mixed -> VPN (reference)']['macro_f1']:.3f} with mixed training"]],
      [3.2, 4.2, 9.2], "Table 7. Ablation and robustness results.")
figure("timeout_robustness.png", 11.5, "Figure 6. Test macro-F1 by flow timeout (7-class protocol).")
figure("feature_ablation.png", 11.5, "Figure 7. Drop in Random Forest macro-F1 when one feature group is removed.")
P("<b>Validation and reproducibility.</b> 20 hand-written gate tests pass under B0, B1 and M (60 of 60 checks). The "
  f"gate gives the same answer as a separately written policy table on all {au['exhaustive_gate_cases']:,} "
  "combinations of tool, application and rate. The gate only reads test-set predictions, no flow appears in two "
  "splits, and no prompt contains the true label. Running the pipeline again from the stored agent replies gives the "
  "same numbers, apart from timings. The code, data split, model hash and raw agent replies are provided with the "
  "implementation.")

# ------------------------------------------------------------------ 7
P("7. Results Analysis and Discussion", "h1")
P("<b>Research gap and objectives.</b> No earlier study tests an LLM agent that applies a written policy to classified "
  "network flows, or measures how classifier mistakes change which actions are allowed. This work measures both. "
  "RQ1: yes, the gate cuts violations by 24 points, and the confidence interval stays above zero. RQ2: met on "
  "average, since the gate keeps 97.9% of completed tasks (target 95%), although the interval reaches down to 93.5%. "
  "RQ3: every violation that remains is a restricted flow predicted as a more permissive class.")
P("<b>Strengths.</b> All conditions use the same proposals, so any difference comes from the gate alone. The gate is "
  "checked against the policy on every possible action, and it takes microseconds. The classifier beats the dataset's "
  "original paper under that paper's own test setup, and every result can be reproduced from the stored outputs.")
P("<b>Limitations.</b> The study uses one small LLM, one dataset from 2016 without capture identifiers, a simulated "
  "network, 100 scenarios written by the authors, three fixed rules and an agent that makes one decision with at most "
  "one retry. The VPN transfer test also shows that a classifier trained only on non-VPN traffic does not work well "
  "on VPN traffic.")
P("<b>Failure cases.</b> Six violations passed the gate. In each one a restricted flow (file transfer or P2P) was "
  "predicted as chat, browsing or streaming. One retry chose a rate that was allowed for the predicted class but not "
  "for the true one. A natural next step is a gate that becomes stricter when the classifier is unsure.")

P("References", "h1")
for r in [
    "[1] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and VPN "
    "traffic using time-related features,” in <i>Proc. 2nd Int. Conf. Inf. Syst. Secur. Privacy (ICISSP)</i>, 2016, "
    "pp. 407–414, doi: 10.5220/0005740704070414.",
    "[2] A. M. Elshewey and A. M. Osman, “Enhancing encrypted HTTPS traffic classification based on stacked deep "
    "ensembles models,” <i>Scientific Reports</i>, vol. 15, Art. no. 35230, 2025, doi: 10.1038/s41598-025-21261-6.",
    "[3] N. Zwerdling, D. Boaz, E. Rabinovich, G. Uziel, D. Amid, and A. Anaby-Tavor, “Towards enforcing company "
    "policy adherence in agentic workflows,” in <i>Proc. EMNLP 2025: Industry Track</i>, 2025, pp. 595–606, "
    "doi: 10.18653/v1/2025.emnlp-industry.41.",
    "[4] Meta AI, “Llama-3.2-3B-Instruct,” model card, 2024. https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct",
    "[5] ggml-org, “llama.cpp,” release b12128, 2026. https://github.com/ggml-org/llama.cpp",
]:
    P(r, "ref")


def footer(canvas, doc):
    canvas.saveState(); canvas.setFont("TNR", 9); canvas.setFillColor(colors.HexColor("#555"))
    canvas.drawString(2 * cm, A4[1] - 1.2 * cm, "Trust but Verify | Phase 3")
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.2 * cm, str(doc.page))
    canvas.restoreState()


OUT.parent.mkdir(parents=True, exist_ok=True)
SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                  bottomMargin=1.8 * cm, title="Trust but Verify – Phase 3",
                  author="M. Abdullah Aamir, Haider Farooq Toor").build(story, onFirstPage=footer, onLaterPages=footer)
print("built", OUT)
