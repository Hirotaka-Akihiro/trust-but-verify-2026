"""Build the poster and standee PDFs (and 300 dpi PNGs) from the HTML sources.

Run from the project root: python poster/source/build.py [poster|standee ...]
Needs Microsoft Edge (headless printing) and poppler's pdftoppm.
"""
import re
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
NAME = "23i-2538_23i-2542_23i-2536_Phase-5"
JOBS = {"poster": ("poster.html", f"{NAME}_Poster_A3"), "standee": ("standee.html", f"{NAME}_Standee_2.5x5ft")}


def inline_svg(name: str) -> str:
    s = (SRC / "figs" / f"{name}.svg").read_text(encoding="utf-8")
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    for i in sorted(ids, key=len, reverse=True):          # unique ids when several SVGs share one page
        s = s.replace(f'id="{i}"', f'id="{name}-{i}"').replace(f"url(#{i})", f"url(#{name}-{i})")
        s = s.replace(f'href="#{i}"', f'href="#{name}-{i}"')
    return s


def build(job: str):
    html, stem = JOBS[job]
    page = (SRC / html).read_text(encoding="utf-8")
    page = re.sub(r"\{\{svg:([\w-]+)\}\}", lambda m: inline_svg(m.group(1)), page)
    built = SRC / f"_built_{html}"
    built.write_text(page, encoding="utf-8")
    pdf = OUT / f"{stem}.pdf"
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", built.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dpi = "300" if job == "poster" else "100"
    subprocess.run(["pdftoppm", "-png", "-r", dpi, "-singlefile", str(pdf), str(OUT / stem)], check=True)
    built.unlink()
    print("built", pdf.name)


if __name__ == "__main__":
    for j in (sys.argv[1:] or ["poster"]):
        build(j)
