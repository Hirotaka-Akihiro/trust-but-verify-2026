// Paper-defence deck for "Prompts Are Not Policies" (7-minute talk, two presenters).
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const SKILL = process.env.PPTX_SKILL;
const { applyTheme } = require(path.join(SKILL, "scripts", "apply_theme.js"));
const PROJ = process.env.PROJ;
const OUT = process.env.OUT || path.join(PROJ, "presentation", "23i-2538_23i-2536_DS-A_Paper_Presentation.pptx");

const THEME = {
  name: "Gate",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2433", lt1: "FFFFFF", dk2: "0B3C68", lt2: "EEF4FB",
    accent1: "D9822B", accent2: "1F5C99", accent3: "4A86C5", accent4: "9CC1E6",
    accent5: "5B6676", accent6: "B23A3A", hlink: "1F5C99", folHlink: "4A86C5",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";               // 10 x 5.625 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Prompts Are Not Policies";
pres.author = "Muhammad Abdullah Aamir, Muhammad Ibrahim Kiani";
const C = pres.SchemeColor;
const NOTES = require("./notes.json");

// ---------------------------------------------------------------- layouts
pres.defineSlideMaster({
  title: "DARK_TITLE",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.35, w: 8.2, h: 1.1, fontFace: THEME.headFontFace,
        fontSize: 44, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 2.55, w: 8.2, h: 0.9, fontFace: THEME.bodyFontFace,
        fontSize: 18, color: C.accent4, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  margin: [0.4, 0.5, 0.45, 0.5],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.28, w: 9.0, h: 0.72, fontFace: THEME.headFontFace,
        fontSize: 32, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { text: { text: "Prompts Are Not Policies", options: { x: 0.5, y: 5.22, w: 5, h: 0.25, fontSize: 10, color: C.accent5, margin: 0 } } },
  ],
  slideNumber: { x: 9.0, y: 5.22, w: 0.5, h: 0.25, fontSize: 10, color: C.accent5, align: "right" },
});

pres.defineSlideMaster({
  title: "DARK_CLOSE",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 8.8, h: 0.7, fontFace: THEME.headFontFace,
        fontSize: 32, bold: true, color: C.background1, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
});

// ---------------------------------------------------------------- helpers
async function icon(Comp, color = "FFFFFF", size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}
async function iconCircle(slide, Comp, x, y, d, fill, name) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: name + "_circle" });
  const pad = d * 0.24;
  slide.addImage({ data: await icon(Comp), x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad, objectName: name + "_icon" });
}
function card(slide, x, y, w, h, fill, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill },
    objectName: name });
}
const T = (slide, text, opts) => slide.addText(text, { isTextBox: true, margin: 0, ...opts });

(async () => {
  // =============================================================== 1. Title
  pres.addSection({ title: "Introduction" });
  let s = pres.addSlide({ masterName: "DARK_TITLE", sectionTitle: "Introduction" });
  s.addText("Prompts Are Not Policies", { placeholder: "title" });
  s.addText("Deterministic pre-execution gating for language-model agents acting on network traffic", { placeholder: "body" });
  await iconCircle(s, fa.FaShieldAlt, 8.55, 0.55, 0.9, C.accent1, "title");
  T(s, [
    { text: "Muhammad Abdullah Aamir (23i-2538)", options: { breakLine: true } },
    { text: "Muhammad Ibrahim Kiani (23i-2536)", options: { breakLine: true } },
    { text: "Department of Data Science, FAST-NUCES Islamabad", options: { color: C.accent4, fontSize: 12 } },
  ], { x: 0.6, y: 3.85, w: 6.5, h: 1.05, fontSize: 15, color: C.background1, valign: "top", paraSpaceAfter: 3, objectName: "authors" });
  s.addNotes(NOTES[0]);

  // =============================================================== 2. Problem
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Introduction" });
  s.addText("Why this problem matters", { placeholder: "title" });
  const rows = [
    [fa.FaRobot, "Agents now act through tools", "A model emits one JSON tool call, and that call changes real state."],
    [fa.FaFileAlt, "The policy usually lives in the prompt", "Compliance is left to the model, which can follow the operator instead."],
    [fa.FaNetworkWired, "Networks raise the stakes", "One wrong action hits every packet of a flow, and the flow's application is a classifier's guess."],
  ];
  for (let i = 0; i < rows.length; i++) {
    const y = 1.3 + i * 1.22;
    await iconCircle(s, rows[i][0], 0.5, y, 0.62, C.accent2, "prob" + i);
    T(s, rows[i][1], { x: 1.3, y: y - 0.04, w: 4.4, h: 0.36, fontSize: 16, bold: true, color: C.text1, objectName: "prob_h" + i });
    T(s, rows[i][2], { x: 1.3, y: y + 0.32, w: 4.4, h: 0.62, fontSize: 14, color: C.accent5, valign: "top", objectName: "prob_b" + i });
  }
  card(s, 6.1, 1.3, 3.4, 3.45, C.text2, "problem_card");
  T(s, "Research problem", { x: 6.4, y: 1.5, w: 2.9, h: 0.35, fontSize: 14, bold: true, color: C.accent1, objectName: "problem_label" });
  T(s, "Does a policy written in the prompt keep a tool-using agent compliant, and what does a code gate before execution add?",
    { x: 6.4, y: 1.95, w: 2.85, h: 2.6, fontSize: 18, color: C.background1, valign: "top", fontFace: THEME.headFontFace, objectName: "problem_text" });
  s.addNotes(NOTES[1]);

  // =============================================================== 3. Existing work and gap
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Introduction" });
  s.addText("Existing work and the gap", { placeholder: "title" });
  const fam = [
    [fa.FaUserShield, "Model-side defences", "A second model reviews each action",
      "PolicyGuard, ShieldAgent, GuardAgent. The Verifier Tax: up to 94% of bad actions intercepted, but 1.6–2.2× model calls and safe success below 5% in most settings."],
    [fa.FaCode, "Code-side defences", "Rules run before a tool executes",
      "ToolGuard: pass¹ 0.450 → 0.685 on τ-bench airline. AgentSpec: over 90% of unsafe code executions prevented."],
  ];
  for (let i = 0; i < 2; i++) {
    const x = 0.5 + i * 4.6;
    card(s, x, 1.2, 4.4, 2.45, C.background2, "fam_card" + i);
    await iconCircle(s, fam[i][0], x + 0.25, 1.38, 0.55, C.accent2, "fam" + i);
    T(s, fam[i][1], { x: x + 0.95, y: 1.38, w: 3.3, h: 0.3, fontSize: 16, bold: true, color: C.text2, objectName: "fam_h" + i });
    T(s, fam[i][2], { x: x + 0.95, y: 1.68, w: 3.3, h: 0.28, fontSize: 13, italic: true, color: C.accent5, objectName: "fam_s" + i });
    T(s, fam[i][3], { x: x + 0.25, y: 2.1, w: 3.95, h: 1.45, fontSize: 14, color: C.text1, valign: "top", objectName: "fam_b" + i });
  }
  card(s, 0.5, 3.85, 9.0, 1.1, "FBEBDD", "gap_card");
  T(s, [
    { text: "Gap  ", options: { bold: true, color: C.accent1 } },
    { text: "Most tests of both families use customer-service, web or code tasks, and the checks assume the facts they read are correct. " +
            "The network-agent studies reviewed (NetConfEval, Confucius, Adanza et al.) do not let an agent act on single flows, where the deciding fact is a classifier's prediction." },
  ], { x: 0.75, y: 3.95, w: 8.5, h: 0.9, fontSize: 14, color: C.text1, valign: "middle", objectName: "gap_text" });
  s.addNotes(NOTES[2]);

  // =============================================================== 4. Research questions
  pres.addSection({ title: "Method" });
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
  s.addText("Research questions and objectives", { placeholder: "title" });
  const rq = [
    ["RQ1", "Prompt only", "How often does the agent break the rules when the policy is only in its prompt?"],
    ["RQ2", "Gate", "How much does a deterministic pre-execution gate prevent, and what does it cost?"],
    ["RQ3", "Retry", "Does returning the gate's rejection reason help the agent recover?"],
    ["RQ4", "Residual risk", "Which violations remain once the gate is in place, and why?"],
  ];
  for (let i = 0; i < 4; i++) {
    const x = 0.5 + (i % 2) * 4.6, y = 1.2 + Math.floor(i / 2) * 1.45;
    card(s, x, y, 4.4, 1.3, C.background2, "rq_card" + i);
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.3, w: 0.7, h: 0.7, fill: { color: i === 1 ? C.accent1 : C.text2 },
      line: { color: i === 1 ? C.accent1 : C.text2 }, objectName: "rq_dot" + i });
    T(s, rq[i][0], { x: x + 0.2, y: y + 0.3, w: 0.7, h: 0.7, fontSize: 14, bold: true, color: C.background1, align: "center",
      valign: "middle", objectName: "rq_n" + i });
    T(s, rq[i][1], { x: x + 1.1, y: y + 0.15, w: 3.1, h: 0.3, fontSize: 15, bold: true, color: C.text2, objectName: "rq_h" + i });
    T(s, rq[i][2], { x: x + 1.1, y: y + 0.45, w: 3.15, h: 0.8, fontSize: 14, color: C.text1, valign: "top", objectName: "rq_b" + i });
  }
  T(s, [
    { text: "Objective  ", options: { bold: true, color: C.accent1 } },
    { text: "measure enforcement alone: each scenario is answered once and the same stored proposal is replayed under every condition." },
  ], { x: 0.5, y: 4.2, w: 9.0, h: 0.6, fontSize: 14, color: C.text1, valign: "middle", objectName: "objective" });
  s.addNotes(NOTES[3]);

  // =============================================================== 5. Architecture
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
  s.addText("Proposed solution and workflow", { placeholder: "title" });
  s.addImage({ path: path.join(PROJ, "Papers", "figs", "ag_architecture.png"), x: 0.5, y: 1.12, w: 9.0, h: 9.0 * 389 / 1229,
    altText: "Pipeline: flow, Random Forest, trusted record, LLM agent, deterministic gate, simulator", objectName: "arch_img" });
  const checks = ["Dispatch", "Schema and range", "Flow identity", "Policy for ŷ"];
  for (let i = 0; i < 4; i++) {
    const x = 0.5 + i * 2.05;
    card(s, x, 4.15, 1.85, 0.62, i === 3 ? C.accent1 : C.text2, "check" + i);
    T(s, (i + 1) + ". " + checks[i], { x, y: 4.15, w: 1.85, h: 0.62, fontSize: 13, bold: true, color: C.background1, align: "center",
      valign: "middle", objectName: "check_t" + i });
  }
  T(s, "Any failed check:\nthe flow stays held", { x: 8.75 - 0.05, y: 4.1, w: 0.95, h: 0.72, fontSize: 10, color: C.accent5,
    valign: "middle", objectName: "held_note" });
  s.addNotes(NOTES[4]);

  // =============================================================== 6. Implementation
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
  s.addText("Tools, data and implementation", { placeholder: "title" });
  const impl = [
    [fa.FaDatabase, "Dataset", "ISCXVPN2016, 18,758 encrypted flows, 23 timing features, 7 applications"],
    [fa.FaTree, "Classifier", "Random Forest, 100 trees: 0.877 accuracy, 0.837 macro-F1 on 2,000 test flows"],
    [fa.FaRobot, "Agent", "Llama-3.2-3B, 4-bit, llama.cpp on a laptop CPU, temperature 0"],
    [fa.FaShieldAlt, "Gate", "Plain Python; agrees with an independent copy on all 77,035 cases"],
    [fa.FaClipboardList, "Scenarios", "100 on 50 test flows: 50 permitted, 25 conflict, 25 injection"],
    [fa.FaFlask, "Conditions", "B0 prompt only, B1 structural, M gate, M+R retry, M-oracle true labels"],
  ];
  for (let i = 0; i < 6; i++) {
    const x = 0.5 + (i % 3) * 3.05, y = 1.2 + Math.floor(i / 3) * 1.85;
    card(s, x, y, 2.85, 1.7, C.background2, "impl_card" + i);
    await iconCircle(s, impl[i][0], x + 0.2, y + 0.2, 0.5, i === 3 ? C.accent1 : C.accent2, "impl" + i);
    T(s, impl[i][1], { x: x + 0.85, y: y + 0.27, w: 1.9, h: 0.36, fontSize: 16, bold: true, color: C.text2, objectName: "impl_h" + i });
    T(s, impl[i][2], { x: x + 0.2, y: y + 0.8, w: 2.5, h: 0.85, fontSize: 13, color: C.text1, valign: "top", objectName: "impl_b" + i });
  }
  s.addNotes(NOTES[5]);

  // =============================================================== 7. Results 1
  pres.addSection({ title: "Results" });
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
  s.addText("Results: the gate stops most violations", { placeholder: "title" });
  s.addChart(pres.charts.BAR, [{ name: "Executed violations (of 100)", labels: ["B0 prompt", "B1 structural", "M gate", "M+R retry", "M-oracle"],
    values: [30, 27, 6, 7, 0] }], {
    x: 0.45, y: 1.1, w: 4.6, h: 3.85, barDir: "col", chartColors: [HEX.dk2], showValue: true, dataLabelPosition: "outEnd",
    dataLabelFontSize: 13, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt",
    showTitle: true, title: "Executed violations (of 100 scenarios)", titleFontSize: 13, titleColor: HEX.dk2, titleFontFace: "+mn-lt",
    catAxisLabelColor: HEX.accent5, catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt",
    valAxisLabelColor: HEX.accent5, valAxisLabelFontSize: 11, valAxisLabelFontFace: "+mn-lt", valAxisMaxVal: 35,
    valGridLine: { color: "E3E8EF", size: 0.5 }, catGridLine: { style: "none" }, showLegend: false, barGapWidthPct: 60,
    objectName: "violations_chart" });
  const stats = [
    ["30 → 6", "violations; 95% CI of the paired difference 17.7–30.4 points"],
    ["25 / 25", "forbidden operator requests obeyed when the policy was only in the prompt"],
    ["3 → 0", "successful prompt injections"],
    ["97.9%", "of completed tasks kept (47 of 48)"],
    ["3.6 µs", "median gate decision, against 2.96 s per model call"],
  ];
  for (let i = 0; i < stats.length; i++) {
    const y = 1.12 + i * 0.77;
    T(s, stats[i][0], { x: 5.3, y, w: 1.55, h: 0.62, fontSize: 24, bold: true, color: i === 0 ? C.accent1 : C.text2,
      fontFace: THEME.headFontFace, valign: "middle", objectName: "stat_n" + i });
    T(s, stats[i][1], { x: 6.95, y, w: 2.6, h: 0.7, fontSize: 13, color: C.text1, valign: "middle", objectName: "stat_l" + i });
  }
  s.addNotes(NOTES[6]);

  // =============================================================== 8. Results 2
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
  s.addText("Retry helps, but label errors remain", { placeholder: "title" });
  const cols = [
    [fa.FaRedo, "Retry with the gate's reason", C.accent2, [
      ["4 of 25", "rejected tasks recovered (8 Mbps rewritten as 8,000 kbps; 3 injected flows blocked)"],
      ["+1", "new violation: a P2P flow labelled file transfer was limited to 512 kbps"],
      ["Lesson", "retry teaches the agent to pass the gate, not to obey the policy"]]],
    [fa.FaTag, "What the gate cannot see", C.accent1, [
      ["6 of 6", "remaining violations are restricted flows mislabelled as permissive"],
      ["0", "violations with true labels (M-oracle)"],
      ["1 left", "with a probability-aware gate at a 10% budget, but only 43 of 50 tasks done"]]],
  ];
  for (let i = 0; i < 2; i++) {
    const x = 0.5 + i * 4.6;
    card(s, x, 1.15, 4.4, 3.85, C.background2, "res2_card" + i);
    await iconCircle(s, cols[i][0], x + 0.25, 1.32, 0.55, cols[i][2], "res2_" + i);
    T(s, cols[i][1], { x: x + 0.95, y: 1.35, w: 3.3, h: 0.5, fontSize: 16, bold: true, color: C.text2, valign: "middle",
      objectName: "res2_h" + i });
    cols[i][3].forEach((r, j) => {
      const y = 2.05 + j * 0.98;
      T(s, r[0], { x: x + 0.25, y, w: 1.15, h: 0.8, fontSize: 18, bold: true, color: cols[i][2], fontFace: THEME.headFontFace,
        valign: "top", objectName: `res2_n${i}${j}` });
      T(s, r[1], { x: x + 1.45, y, w: 2.8, h: 0.85, fontSize: 13, color: C.text1, valign: "top", objectName: `res2_b${i}${j}` });
    });
  }
  s.addNotes(NOTES[7]);

  // =============================================================== 9. Comparison + interpretation
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
  s.addText("Comparison with base papers", { placeholder: "title" });
  const H = (t) => ({ text: t, options: { bold: true, color: HEX.lt1, fill: { color: HEX.dk2 } } });
  const rowsT = [
    [H("Study"), H("Runtime checker"), H("Reported result*")],
    ["ToolGuard (2025)", "Python guards generated from policy documents", "pass¹ 0.450 → 0.685 on τ-bench airline"],
    ["Verifier Tax (2026)", "LLM verifier (1.6–2.2× model calls)", "Up to 94% intercepted; safe success < 5% in most settings"],
    ["AgentSpec (2026)", "Rule language (millisecond overhead)", "Over 90% of unsafe code executions prevented"],
    ["GuardAgent (2025)", "Second agent plans and writes guard code", "98.7% and 90.0% label accuracy (GPT-4)"],
    [{ text: "This work", options: { bold: true, color: HEX.accent1 } }, { text: "Hand-written lookup (3.6 µs, no model calls)", options: { bold: true } },
      { text: "Violation rate −0.24 (CI 0.177–0.304); 97.9% of tasks kept", options: { bold: true } }],
  ];
  s.addTable(rowsT, { x: 0.5, y: 1.12, w: 9.0, colW: [1.8, 3.35, 3.85], fontSize: 12, color: HEX.dk1, fontFace: THEME.bodyFontFace,
    border: { type: "solid", pt: 0.5, color: "D5DEE9" }, fill: { color: HEX.lt1 }, valign: "middle", rowH: 0.42, margin: [0.04, 0.08, 0.04, 0.08],
    objectName: "comparison_table" });
  T(s, "* Reported in each paper on its own benchmark and model, so effect sizes and costs are compared, not raw scores.",
    { x: 0.5, y: 3.78, w: 9.0, h: 0.28, fontSize: 10, italic: true, color: C.accent5, objectName: "table_note" });
  card(s, 0.5, 4.15, 9.0, 0.85, C.background2, "why_card");
  T(s, [
    { text: "Why it works  ", options: { bold: true, color: C.accent1 } },
    { text: "the policy is a short lookup from application to allowed actions, so code decides it exactly, in microseconds, with no second model." },
  ], { x: 0.75, y: 4.2, w: 8.55, h: 0.75, fontSize: 14, color: C.text1, valign: "middle", objectName: "why_text" });
  s.addNotes(NOTES[8]);

  // =============================================================== 10. Conclusion
  pres.addSection({ title: "Conclusion" });
  s = pres.addSlide({ masterName: "DARK_CLOSE", sectionTitle: "Conclusion" });
  s.addText("Contributions and conclusion", { placeholder: "title" });
  const close = [
    ["Contributions", [
      "Prompt-only failure profile of a 3B agent",
      "Paired test of a gate on identical proposals",
      "Retry analysis with the gate's reason",
      "Residual risk traced to classifier labels"]],
    ["Conclusion", [
      "A prompt is not enforcement: 25 of 25 conflicts obeyed",
      "A code gate is: 30 → 6 violations, 0 injections, 3.6 µs",
      "The gate is only as correct as the labels it reads"]],
    ["Future work", [
      "Larger models and multi-step episodes",
      "Time-of-day windows and per-period limits",
      "Uncertainty handling without a fixed budget"]],
  ];
  for (let i = 0; i < 3; i++) {
    const x = 0.6 + i * 3.0;
    card(s, x, 1.25, 2.8, 3.2, "164B7E", "close_card" + i);
    T(s, close[i][0], { x: x + 0.2, y: 1.4, w: 2.4, h: 0.4, fontSize: 17, bold: true, color: C.accent1, objectName: "close_h" + i });
    T(s, close[i][1].map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < close[i][1].length - 1 } })),
      { x: x + 0.2, y: 1.9, w: 2.45, h: 2.45, fontSize: 14, color: C.background1, valign: "top", paraSpaceAfter: 6,
        objectName: "close_b" + i });
  }
  T(s, "Thank you. Questions?", { x: 0.6, y: 4.65, w: 8.8, h: 0.45, fontSize: 18, bold: true, color: C.accent4, objectName: "thanks" });
  s.addNotes(NOTES[9]);

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})().catch((e) => { console.error(e); process.exit(1); });
