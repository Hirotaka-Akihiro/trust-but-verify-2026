"""Render Content_Verification_Sheet.md to an A4 PDF in the poster's style (headings, paragraphs and tables only)."""
import html, re, subprocess
from pathlib import Path

SRC = Path(__file__).resolve().parent
md = (SRC.parent / "Content_Verification_Sheet.md").read_text(encoding="utf-8")


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", t)


out, rows = [], []
def flush():
    global rows
    if rows:
        head, body = rows[0], [r for r in rows[2:]]
        out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>" +
                   "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table>")
        rows = []

for line in md.splitlines():
    if line.startswith("|"):
        rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        continue
    flush()
    if line.startswith("# "):
        out.append(f"<h1>{inline(line[2:])}</h1>")
    elif line.startswith("## "):
        out.append(f"<h2>{inline(line[3:])}</h2>")
    elif line.strip():
        out.append(f"<p>{inline(line)}</p>")
flush()

page = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="poster.css"><style>
@page {{ size: A4; margin: 14mm 13mm; }}
html, body {{ background: #fff; }}
body {{ font-size: 9pt; line-height: 1.4; }}
h1 {{ font-family: var(--head); color: var(--navy); font-size: 18pt; margin-bottom: 3mm; }}
h2 {{ font-family: var(--head); color: var(--navy); font-size: 12pt; margin: 5mm 0 2mm; }}
p {{ margin-bottom: 1.4mm; }}
table {{ width: 100%; border-collapse: collapse; font-size: 8pt; }}
th {{ background: var(--deep); color: #fff; text-align: left; padding: 1.4mm 1.8mm; font-weight: 600; }}
td {{ border-bottom: 0.3mm solid var(--line); padding: 1.3mm 1.8mm; vertical-align: top; }}
tr {{ break-inside: avoid; }}
code {{ font-family: var(--mono); font-size: 7.4pt; color: var(--navy); }}
</style></head><body>{''.join(out)}</body></html>"""
tmp = SRC / "_sheet.html"
tmp.write_text(page, encoding="utf-8")
pdf = SRC.parent / "23i-2538_23i-2542_23i-2536_Phase-5_Content_Verification_Sheet.pdf"
subprocess.run([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "--headless=new", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=6000", f"--print-to-pdf={pdf}", tmp.as_uri()],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
tmp.unlink()
print("written", pdf.name)
