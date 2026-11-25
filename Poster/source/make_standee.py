"""Build standee.html from the poster's content so the two always tell the same story."""
import re
from pathlib import Path
SRC = str(Path(__file__).resolve().parent)
poster = open(SRC + r"\poster.html", encoding="utf-8").read()
body = poster[poster.index('<div class="page">'):poster.rindex("</body>")]

# replace the poster header (top bar + title row) with the standee's dark band + full-width question card
start = body.index('  <div class="top">')
end = body.index('  <div class="three">')
header = '''  <div class="band">
    <div class="kicker">FAST-NUCES Islamabad · Department of Data Science</div>
    <h1>Trust, but Verify <span class="accent">the Label</span></h1>
    <div class="sub">Encrypted-traffic misclassification as the residual risk of deterministic policy gating</div>
    <div class="authors"><b>Muhammad Abdullah Aamir</b> <span>23i-2538</span> &nbsp;·&nbsp; <b>Haider Farooq Toor</b> <span>23i-2542</span> &nbsp;·&nbsp; <b>Muhammad Ibrahim Kiani</b> <span>23i-2536</span></div>
  </div>

  <div class="wrap">
  <div class="card question">
    <div>
      <div class="kicker">Research question</div>
      <p>An AI agent's actions pass a correct policy check. Which violations still get through, and why?</p>
    </div>
    <div class="qstats">
      <div><div class="num">18,758</div><span>encrypted flows</span></div>
      <div><div class="num">100</div><span>agent scenarios</span></div>
      <div><div class="num">3</div><span>policy rules</span></div>
    </div>
  </div>

'''
body = body[:start] + header + body[end:]
# close .wrap before the footer
foot = body.index('  <div class="foot">')
body = body[:foot] + "  </div>\n\n" + body[foot:]

style = poster[poster.index("<style>") + 7:poster.index("</style>")]
# remove poster page geometry and header rules; keep the component styles
style = re.sub(r"  @page \{[^}]*\}\n", "", style)
style = re.sub(r"  html, body \{[^}]*\}\n", "", style)
style = re.sub(r"  \.page \{[^}]*\}\n", "", style)
style = re.sub(r"  \.page > \* \+ \* \{[^}]*\}\n", "", style)
style = re.sub(r"  \.(top|titlerow|title)[^{]*\{[^}]*\}\n", "", style)
style = re.sub(r"  \.question[^{]*\{[^}]*\}\n", "", style)
style = re.sub(r"  \.foot[^{]*\{[^}]*\}\n", "", style)

STANDEE = r"""
  /* Real size 762 x 1524 mm (2.5 x 5 ft): laid out on a 297 x 594 mm canvas and scaled by 762/297. */
  @page { size: 762mm 1524mm; margin: 0; }
  html, body { width: 762mm; height: 1524mm; overflow: hidden; }
  .page { zoom: 2.565657; width: 297mm; height: 594mm; position: relative; }
  .page > * + * { margin-top: 4.4mm; }
  .wrap { padding: 0 11mm; }
  .wrap > * + * { margin-top: 4.4mm; }

  .band { background: var(--deep); color: #fff; padding: 9mm 11mm 8mm; }
  .band .kicker { color: var(--orange-soft); font-size: 8.4pt; }
  .band h1 { font-family: var(--head); font-weight: 700; font-size: 42pt; line-height: 0.98; letter-spacing: -0.025em; margin-top: 3mm; white-space: nowrap; }
  .band h1 .accent { color: var(--orange-soft); }
  .band .sub { font-size: 15pt; font-weight: 500; color: #CFE0F2; line-height: 1.25; margin-top: 3mm; }
  .band .authors { margin-top: 4mm; font-size: 11pt; color: #fff; }
  .band .authors span { font-family: var(--mono); font-size: 8.6pt; color: #A9BCD3; }

  .question { padding: 4mm 5mm; border: 0.5mm solid var(--navy); display: grid; grid-template-columns: 1.5fr 1fr; gap: 6mm; align-items: center; }
  .question .kicker { font-size: 8pt; }
  .question p { font-size: 13.5pt; font-weight: 600; line-height: 1.3; margin-top: 1.6mm; }
  .question .qstats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2mm; border-left: 0.35mm solid var(--line); padding-left: 5mm; }
  .question .num { font-size: 19pt; }
  .question .qstats span { display: block; font-size: 8.4pt; color: var(--muted); }

  /* larger type than the A3 poster: the standee is read standing, from further away */
  .kicker.k { font-size: 8.2pt; }
  h3.h { font-size: 14pt; }
  .txt, ul.clean li { font-size: 10.6pt; line-height: 1.4; }
  .level { font-size: 10.2pt; }
  .methodcard .figsvg { width: 100%; }
  .methodcard .caption { font-size: 9pt; }
  .leak { font-size: 10pt; }
  .formula { font-size: 10pt; }
  .hero h2 { font-size: 18.5pt; }
  .hero .kicker { font-size: 8.4pt; } .hero .tag { font-size: 8pt; }
  .bars .name b { font-size: 10.8pt; } .bars .name span { font-size: 8.6pt; }
  .bars .row { grid-template-columns: 40mm 10mm 1fr; margin-bottom: 1.8mm; }
  .bars .track { height: 7.2mm; }
  .bars .valc { font-size: 13.5pt; }
  .hero .caption { font-size: 8.8pt; }
  .stat .big { font-size: 21pt; } .stat .lbl { font-size: 9.2pt; }
  .evidence { grid-template-columns: 1fr; gap: 4.4mm; }
  .evidence .card { display: grid; grid-template-columns: 0.78fr 1.5fr; column-gap: 6mm; align-content: start; padding: 4mm 4.6mm; }
  .evidence .card > * { grid-column: 1; }
  .evidence .card > .figwrap { grid-column: 2; grid-row: 1 / span 4; }
  .evidence .txt { margin: 1.6mm 0 2mm; }
  .evidence h4 { font-size: 13.5pt; line-height: 1.2; }
  .evidence .caption { font-size: 8.8pt; }
  .bottom { grid-template-columns: 1fr 38mm; }
  .bottom h4 { font-size: 13.5pt; }
  .qr .qrsvg { width: 28mm; } .qr span { font-size: 8.4pt; }

  /* footer stays above the bottom 40 mm (real size) that the stand's base covers */
  .foot { position: absolute; left: 11mm; right: 11mm; bottom: 18mm; display: flex; justify-content: space-between;
    font-size: 8.8pt; color: var(--muted); border-top: 0.35mm solid var(--line); padding-top: 2mm; }
  .foot b { color: var(--ink); font-weight: 600; }
"""
html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<title>Trust, but Verify the Label - 2.5 x 5 ft standee</title>\n<link rel="stylesheet" href="poster.css">\n'
        f'<style>{style}{STANDEE}</style>\n</head>\n<body>\n{body}</body>\n</html>\n')
open(SRC + r"\standee.html", "w", encoding="utf-8").write(html)
print("standee written;", html.count("<div"), "open divs,", html.count("</div>"), "closed")
