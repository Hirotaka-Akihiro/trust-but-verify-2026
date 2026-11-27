// Phase 6 video deck for "Trust, but Verify the Label" (Computer Networks, three presenters).
// Run: NODE_PATH=<node_modules> PPTX_SKILL=<pptx skill dir> PROJ=<project root> node build_cn_deck.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const { applyTheme } = require(path.join(process.env.PPTX_SKILL, "scripts", "apply_theme.js"));
const PROJ = process.env.PROJ;
const OUT = process.env.OUT || path.join(PROJ, "presentation", "cn", "23i-2538_23i-2542_23i-2536_Phase-6_Presentation.pptx");
const NOTES = require("./cn_notes.json");

const THEME = {
  name: "TrustLabel", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "1B2433", lt1: "FFFFFF", dk2: "0A2F52", lt2: "EEF4FB", accent1: "D9822B", accent2: "1F5C99",
            accent3: "4A86C5", accent4: "9CC1E6", accent5: "5B6676", accent6: "B8661A", hlink: "1F5C99", folHlink: "4A86C5" },
};
const HEX = THEME.colors;
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Trust, but Verify the Label";
pres.author = "Muhammad Abdullah Aamir, Haider Farooq Toor, Muhammad Ibrahim Kiani";
const C = pres.SchemeColor;

pres.defineSlideMaster({ title: "DARK_TITLE", background: { color: C.text2 }, objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.2, w: 8.4, h: 1.1, fontFace: THEME.headFontFace,
      fontSize: 44, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
  { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 2.4, w: 8.4, h: 0.9, fontFace: THEME.bodyFontFace,
      fontSize: 18, color: C.accent4, valign: "top", margin: 0 }, text: "" } } ] });
pres.defineSlideMaster({ title: "CONTENT", background: { color: C.background1 }, margin: [0.4, 0.5, 0.45, 0.5], objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.28, w: 9.0, h: 0.72, fontFace: THEME.headFontFace,
      fontSize: 30, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
  { text: { text: "Trust, but Verify the Label", options: { x: 0.5, y: 5.22, w: 5, h: 0.25, fontSize: 10, color: C.accent5, margin: 0 } } } ],
  slideNumber: { x: 9.0, y: 5.22, w: 0.5, h: 0.25, fontSize: 10, color: C.accent5, align: "right" } });
pres.defineSlideMaster({ title: "DARK_CLOSE", background: { color: C.text2 }, objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 8.8, h: 0.7, fontFace: THEME.headFontFace,
      fontSize: 30, bold: true, color: C.background1, valign: "middle", align: "left", margin: 0 }, text: "" } } ] });

async function icon(Comp) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#FFFFFF", size: "256" }));
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}
async function iconCircle(slide, Comp, x, y, d, fill, name) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: name + "_c" });
  const pad = d * 0.24;
  slide.addImage({ data: await icon(Comp), x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad, objectName: name + "_i" });
}
const card = (s, x, y, w, h, fill, name) => s.addShape(pres.shapes.ROUNDED_RECTANGLE,
  { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill }, objectName: name });
const T = (s, text, opts) => s.addText(text, { isTextBox: true, margin: 0, ...opts });
const chartText = { catAxisLabelColor: HEX.accent5, valAxisLabelColor: HEX.accent5, catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", titleFontFace: "+mn-lt", titleFontSize: 13, titleColor: HEX.dk2,
  valGridLine: { color: "E3E8EF", size: 0.5 }, catGridLine: { style: "none" } };

(async () => {
  // 1 Title
  pres.addSection({ title: "Introduction" });
  let s = pres.addSlide({ masterName: "DARK_TITLE", sectionTitle: "Introduction" });
  s.addText("Trust, but Verify the Label", { placeholder: "title" });
  s.addText("Encrypted-traffic misclassification as the residual risk of deterministic policy gating", { placeholder: "body" });
  await iconCircle(s, fa.FaShieldAlt, 8.6, 0.5, 0.85, C.accent1, "t");
  T(s, [
    { text: "Muhammad Abdullah Aamir (23i-2538)", options: { breakLine: true } },
    { text: "Haider Farooq Toor (23i-2542)", options: { breakLine: true } },
    { text: "Muhammad Ibrahim Kiani (23i-2536)", options: { breakLine: true } },
    { text: "Department of Data Science, FAST-NUCES Islamabad", options: { color: C.accent4, fontSize: 12 } },
  ], { x: 0.6, y: 3.55, w: 7, h: 1.4, fontSize: 15, color: C.background1, valign: "top", paraSpaceAfter: 3, objectName: "authors" });
  s.addNotes(NOTES[0]);

  // 2 Problem
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Introduction" });
  s.addText("Why this problem matters", { placeholder: "title" });
  const rows = [
    [fa.FaLock, "Encryption hides the payload", "Networks infer the application from flow timing instead."],
    [fa.FaRobot, "AI agents act on that label", "An agent can allow, block or rate-limit a flow by calling a tool."],
    [fa.FaTag, "The label is a prediction", "A policy check reads the same label, so it is only as correct as the classifier."],
  ];
  for (let i = 0; i < 3; i++) {
    const y = 1.3 + i * 1.22;
    await iconCircle(s, rows[i][0], 0.5, y, 0.62, C.accent2, "p" + i);
    T(s, rows[i][1], { x: 1.3, y: y - 0.04, w: 4.4, h: 0.36, fontSize: 16, bold: true, color: C.text1, objectName: "ph" + i });
    T(s, rows[i][2], { x: 1.3, y: y + 0.32, w: 4.4, h: 0.62, fontSize: 14, color: C.accent5, valign: "top", objectName: "pb" + i });
  }
  card(s, 6.1, 1.3, 3.4, 3.45, C.text2, "rq");
  T(s, "Research question", { x: 6.4, y: 1.5, w: 2.9, h: 0.35, fontSize: 14, bold: true, color: C.accent1, objectName: "rqk" });
  T(s, "An AI agent's actions pass a correct policy check. Which violations still get through, and why?",
    { x: 6.4, y: 1.95, w: 2.85, h: 2.6, fontSize: 18, color: C.background1, valign: "top", fontFace: THEME.headFontFace, objectName: "rqt" });
  s.addNotes(NOTES[1]);

  // 3 Gap and objectives
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Introduction" });
  s.addText("Research gap and objectives", { placeholder: "title" });
  const gaps = [[fa.FaChartBar, "Classifier studies", "report overall accuracy, not which errors change an enforcement decision"],
                [fa.FaUserShield, "Pre-execution guards", "such as ToolGuard and AgentSpec assume the facts they read are correct"]];
  for (let i = 0; i < 2; i++) {
    const x = 0.5 + i * 4.6;
    card(s, x, 1.15, 4.4, 1.3, C.background2, "g" + i);
    await iconCircle(s, gaps[i][0], x + 0.22, 1.37, 0.55, C.accent2, "gi" + i);
    T(s, gaps[i][1], { x: x + 0.95, y: 1.3, w: 3.3, h: 0.32, fontSize: 15, bold: true, color: C.text2, objectName: "gh" + i });
    T(s, gaps[i][2], { x: x + 0.95, y: 1.64, w: 3.3, h: 0.7, fontSize: 13, color: C.text1, valign: "top", objectName: "gb" + i });
  }
  const objs = ["Build a classifier that beats the dataset's original baseline",
                "Measure a policy gate on identical agent actions",
                "Trace every violation that still gets through",
                "Test whether reading class probabilities helps"];
  for (let i = 0; i < 4; i++) {
    const x = 0.5 + (i % 2) * 4.6, y = 2.75 + Math.floor(i / 2) * 1.12;
    card(s, x, y, 4.4, 0.95, "FFFFFF", "oc" + i);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 4.4, h: 0.95, rectRadius: 0.08, fill: { color: "FFFFFF" },
      line: { color: "D5DEE9", width: 1 }, objectName: "ob" + i });
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.2, w: 0.55, h: 0.55, fill: { color: i === 1 ? C.accent1 : C.text2 },
      line: { color: i === 1 ? C.accent1 : C.text2 }, objectName: "od" + i });
    T(s, "O" + (i + 1), { x: x + 0.2, y: y + 0.2, w: 0.55, h: 0.55, fontSize: 13, bold: true, color: C.background1, align: "center", valign: "middle", objectName: "on" + i });
    T(s, objs[i], { x: x + 0.95, y: y + 0.12, w: 3.3, h: 0.72, fontSize: 14, color: C.text1, valign: "middle", objectName: "ot" + i });
  }
  s.addNotes(NOTES[2]);

  // 4 Pipeline
  pres.addSection({ title: "Method" });
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
  s.addText("Proposed method: the pipeline", { placeholder: "title" });
  s.addImage({ path: path.join(PROJ, "Papers", "figs", "cn_architecture.png"), x: 0.5, y: 1.1, w: 9.0, h: 9.0 * 389 / 1229,
    altText: "Pipeline: flow, Random Forest, trusted record, agent, deterministic gate, simulator", objectName: "arch" });
  const chk = ["Dispatch", "Schema and range", "Flow identity", "Policy for ŷ"];
  for (let i = 0; i < 4; i++) {
    const x = 0.5 + i * 2.05;
    card(s, x, 4.15, 1.85, 0.62, i === 3 ? C.accent1 : C.text2, "ck" + i);
    T(s, (i + 1) + ". " + chk[i], { x, y: 4.15, w: 1.85, h: 0.62, fontSize: 13, bold: true, color: C.background1, align: "center", valign: "middle", objectName: "ct" + i });
  }
  T(s, "Any failed check:\nthe flow stays held", { x: 8.7, y: 4.1, w: 0.95, h: 0.72, fontSize: 10, color: C.accent5, valign: "middle", objectName: "held" });
  s.addNotes(NOTES[3]);

  // 5 Policy and why errors leak
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
  s.addText("The policy, and why errors still leak", { placeholder: "title" });
  card(s, 0.5, 1.15, 4.4, 3.7, C.background2, "pol");
  T(s, "Three permission levels", { x: 0.75, y: 1.3, w: 4, h: 0.35, fontSize: 15, bold: true, color: C.text2, objectName: "polh" });
  const lv = [["P2P", "block only", C.text2], ["Streaming, file transfer", "block, or limit ≤ 1,024 kbps", C.accent3],
              ["Browsing, chat, email, VoIP", "allow, block, or limit ≤ 10,000 kbps", C.accent4]];
  for (let i = 0; i < 3; i++) {
    const y = 1.9 + i * 0.95;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y: y + 0.08, w: 0.28, h: 0.28, fill: { color: lv[i][2] }, line: { color: lv[i][2] }, objectName: "ld" + i });
    T(s, [{ text: lv[i][0], options: { bold: true, color: C.text2, breakLine: true } }, { text: lv[i][1], options: { color: C.text1 } }],
      { x: 1.25, y, w: 3.5, h: 0.8, fontSize: 14, valign: "top", objectName: "lt" + i });
  }
  card(s, 5.1, 1.15, 4.4, 3.7, C.text2, "leak");
  T(s, "Why errors still leak", { x: 5.35, y: 1.3, w: 4, h: 0.35, fontSize: 15, bold: true, color: C.accent1, objectName: "lkh" });
  T(s, "The gate only executes actions allowed for the predicted class ŷ. A violation therefore needs",
    { x: 5.35, y: 1.8, w: 3.9, h: 0.8, fontSize: 14, color: C.background1, valign: "top", objectName: "lk1" });
  card(s, 5.35, 2.65, 3.9, 0.6, "164B7E", "fm");
  T(s, "a ∈ Π(ŷ) \\ Π(y)", { x: 5.35, y: 2.65, w: 3.9, h: 0.6, fontSize: 20, color: C.background1, align: "center", valign: "middle", fontFace: "Cambria Math", objectName: "fmt" });
  T(s, "which happens only when a restricted flow is predicted as a more permissive class.",
    { x: 5.35, y: 3.45, w: 3.9, h: 1.2, fontSize: 14, color: C.background1, valign: "top", objectName: "lk2" });
  s.addNotes(NOTES[4]);

  // 6 Implementation
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
  s.addText("Implementation and experimental setup", { placeholder: "title" });
  const impl = [
    [fa.FaDatabase, "Dataset", "ISCXVPN2016, 18,758 flows, 23 timing features, 7 applications"],
    [fa.FaFilter, "Cleaning and split", "17,984 flows after cleaning; 6,000 / 2,000 / 2,000 split"],
    [fa.FaTree, "Classifier", "Random Forest, 100 trees, depth 16, chosen on validation"],
    [fa.FaRobot, "Agent", "Llama-3.2-3B (4-bit) via llama.cpp on a laptop CPU"],
    [fa.FaClipboardList, "Scenarios", "100 on 50 test flows: 50 normal, 25 forbidden, 25 injected"],
    [fa.FaFlask, "Conditions", "B0 prompt only, B1 structural, M gate, M+R retry, true labels"],
  ];
  for (let i = 0; i < 6; i++) {
    const x = 0.5 + (i % 3) * 3.05, y = 1.2 + Math.floor(i / 3) * 1.85;
    card(s, x, y, 2.85, 1.7, C.background2, "ic" + i);
    await iconCircle(s, impl[i][0], x + 0.2, y + 0.2, 0.5, i === 2 ? C.accent1 : C.accent2, "ii" + i);
    T(s, impl[i][1], { x: x + 0.85, y: y + 0.27, w: 1.9, h: 0.36, fontSize: 15, bold: true, color: C.text2, objectName: "ih" + i });
    T(s, impl[i][2], { x: x + 0.2, y: y + 0.8, w: 2.5, h: 0.85, fontSize: 13, color: C.text1, valign: "top", objectName: "ib" + i });
  }
  s.addNotes(NOTES[5]);

  // 7 Demo
  s = pres.addSlide({ masterName: "DARK_CLOSE", sectionTitle: "Method" });
  s.addText("Live demo: code and experiments", { placeholder: "title" });
  const dm = [["1", "Gate unit tests", "python src/gate_tests.py", "60 / 60 checks pass"],
              ["2", "Classifier", "python src/demo.py", "data, saved model, 87.7% accuracy"],
              ["3", "Three real scenarios", "same script", "forbidden request, injected note, wrong label"],
              ["4", "All 100 scenarios", "same script", "30 → 6 violations, gate in microseconds"]];
  for (let i = 0; i < 4; i++) {
    const y = 1.3 + i * 0.92;
    card(s, 0.6, y, 8.8, 0.78, "164B7E", "dc" + i);
    s.addShape(pres.shapes.OVAL, { x: 0.8, y: y + 0.14, w: 0.5, h: 0.5, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "dn" + i });
    T(s, dm[i][0], { x: 0.8, y: y + 0.14, w: 0.5, h: 0.5, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle", objectName: "dnt" + i });
    T(s, dm[i][1], { x: 1.5, y: y + 0.1, w: 2.6, h: 0.58, fontSize: 15, bold: true, color: C.background1, valign: "middle", objectName: "dh" + i });
    T(s, dm[i][2], { x: 4.1, y: y + 0.1, w: 2.5, h: 0.58, fontSize: 12, color: "F6A75A", fontFace: "Consolas", valign: "middle", objectName: "dcmd" + i });
    T(s, dm[i][3], { x: 6.6, y: y + 0.1, w: 2.7, h: 0.58, fontSize: 12, color: C.accent4, valign: "middle", objectName: "dr" + i });
  }
  s.addNotes(NOTES[6]);

  // 8 Classifier results
  pres.addSection({ title: "Results" });
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
  s.addText("Result 1: a stronger classifier", { placeholder: "title" });
  s.addChart(pres.charts.LINE, [
    { name: "Random Forest", labels: ["15 s", "30 s", "60 s", "120 s"], values: [0.855, 0.845, 0.826, 0.819] },
    { name: "C4.5-style tree (rebuilt)", labels: ["15 s", "30 s", "60 s", "120 s"], values: [0.808, 0.789, 0.773, 0.767] },
    { name: "1-NN (rebuilt)", labels: ["15 s", "30 s", "60 s", "120 s"], values: [0.745, 0.743, 0.724, 0.728] },
    { name: "C4.5 reported (0.783)", labels: ["15 s", "30 s", "60 s", "120 s"], values: [0.783, 0.783, 0.783, 0.783] },
  ], { x: 0.45, y: 1.1, w: 5.4, h: 3.9, chartColors: [HEX.dk2, HEX.accent3, HEX.accent4, HEX.accent1], lineSize: 2, lineDataSymbolSize: 7,
       showTitle: true, title: "Weighted precision by flow timeout (14 classes, 10-fold CV)", valAxisMinVal: 0.68, valAxisMaxVal: 0.88,
       valAxisLabelFormatCode: "0.00", showLegend: true, legendPos: "b", legendFontSize: 10, legendFontFace: "+mn-lt", legendColor: HEX.dk1,
       ...chartText, objectName: "c1" });
  const st1 = [["0.855", "weighted precision under the original protocol"], ["+4.7 pts", "over the rebuilt C4.5 (+7.2 over the reported 0.783)"],
               ["0.837", "macro-F1 on our 2,000 test flows"], ["13.6%", "of file-transfer flows read as chat: the costliest error"]];
  for (let i = 0; i < 4; i++) {
    const y = 1.15 + i * 0.95;
    T(s, st1[i][0], { x: 6.1, y, w: 1.55, h: 0.7, fontSize: 22, bold: true, color: i === 3 ? C.accent1 : C.text2, fontFace: THEME.headFontFace, valign: "middle", objectName: "s1n" + i });
    T(s, st1[i][1], { x: 7.7, y, w: 1.85, h: 0.75, fontSize: 12, color: C.text1, valign: "middle", objectName: "s1l" + i });
  }
  s.addNotes(NOTES[7]);

  // 9 Gate results
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
  s.addText("Result 2: the gate stops most violations", { placeholder: "title" });
  s.addChart(pres.charts.BAR, [{ name: "Executed violations", labels: ["B0 prompt", "B1 structural", "M gate", "M+R retry", "True labels"],
    values: [30, 27, 6, 7, 0] }], { x: 0.45, y: 1.1, w: 4.8, h: 3.9, barDir: "col", chartColors: [HEX.dk2], showValue: true,
    dataLabelPosition: "outEnd", dataLabelFontSize: 13, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt", showTitle: true,
    title: "Executed violations (of 100 scenarios)", valAxisMaxVal: 35, showLegend: false, barGapWidthPct: 60, ...chartText, objectName: "c2" });
  const st2 = [["30 → 6", "violations; 95% CI of the reduction 17.7–30.4 points"],
               ["25 / 25", "forbidden requests obeyed with the policy only in the prompt"],
               ["3 → 0", "successful injected notes"],
               ["97.9%", "of completed tasks kept (47 vs 48 of 50)"],
               ["3.6 µs", "per gate decision, vs 2.96 s per agent call"]];
  for (let i = 0; i < 5; i++) {
    const y = 1.12 + i * 0.77;
    T(s, st2[i][0], { x: 5.45, y, w: 1.6, h: 0.62, fontSize: 22, bold: true, color: i === 0 ? C.accent1 : C.text2, fontFace: THEME.headFontFace, valign: "middle", objectName: "s2n" + i });
    T(s, st2[i][1], { x: 7.1, y, w: 2.45, h: 0.7, fontSize: 12, color: C.text1, valign: "middle", objectName: "s2l" + i });
  }
  s.addNotes(NOTES[8]);

  // 10 Key findings
  s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
  s.addText("Key findings: the label is the weak link", { placeholder: "title" });
  const kf = [[fa.FaTag, "6 of 6", "remaining violations are restricted flows labelled as permissive (4 file transfer, 2 P2P)"],
              [fa.FaCheckCircle, "0", "violations when the gate reads the true labels"],
              [fa.FaBalanceScale, "1 left, 43 / 50", "reading probabilities at a 10% over-restriction budget removes 5 of 6, but blocks legitimate work"]];
  for (let i = 0; i < 3; i++) {
    const x = 0.5 + i * 3.05;
    card(s, x, 1.2, 2.85, 3.6, C.background2, "k" + i);
    await iconCircle(s, kf[i][0], x + 0.25, 1.4, 0.6, i === 0 ? C.accent1 : C.accent2, "ki" + i);
    T(s, kf[i][1], { x: x + 0.25, y: 2.2, w: 2.4, h: 0.6, fontSize: 24, bold: true, color: i === 0 ? C.accent1 : C.text2, fontFace: THEME.headFontFace, objectName: "kn" + i });
    T(s, kf[i][2], { x: x + 0.25, y: 2.9, w: 2.4, h: 1.8, fontSize: 14, color: C.text1, valign: "top", objectName: "kt" + i });
  }
  s.addNotes(NOTES[9]);

  // 11 Conclusion
  pres.addSection({ title: "Conclusion" });
  s = pres.addSlide({ masterName: "DARK_CLOSE", sectionTitle: "Conclusion" });
  s.addText("Conclusion and future work", { placeholder: "title" });
  const cl = [["What we showed", ["Random Forest beats the original baseline by ≥ 4.7 points", "A policy gate cuts violations from 30 to 6 at microsecond cost", "Every remaining violation comes from a wrong label"]],
              ["Takeaway", ["A gate is only as correct as the label it reads", "For operators, what matters is how often restricted traffic is read as permissive"]],
              ["Future work", ["Newer traffic with capture-separated splits", "Stateful rules such as bandwidth budgets", "Classifiers trained with policy-aware error costs"]]];
  for (let i = 0; i < 3; i++) {
    const x = 0.6 + i * 3.0;
    card(s, x, 1.25, 2.8, 3.25, "164B7E", "cc" + i);
    T(s, cl[i][0], { x: x + 0.2, y: 1.4, w: 2.4, h: 0.4, fontSize: 16, bold: true, color: C.accent1, objectName: "ch" + i });
    T(s, cl[i][1].map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < cl[i][1].length - 1 } })),
      { x: x + 0.2, y: 1.9, w: 2.45, h: 2.5, fontSize: 13, color: C.background1, valign: "top", paraSpaceAfter: 6, objectName: "cb" + i });
  }
  T(s, "Thank you. Code and results: github.com/Hirotaka-Akihiro/trust-but-verify-2026", { x: 0.6, y: 4.7, w: 8.8, h: 0.4, fontSize: 14, bold: true, color: C.accent4, objectName: "thanks" });
  s.addNotes(NOTES[10]);

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})().catch((e) => { console.error(e); process.exit(1); });
