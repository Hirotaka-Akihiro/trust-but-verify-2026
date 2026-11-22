"""Turn the IEEE two-column Agentic paper into a plain single-column article with identical content."""
import sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
s = src.read_text(encoding="utf-8")
b = chr(92)

def rep(a, c):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, c)

rep(b + "documentclass[conference,a4paper]{IEEEtran}",
    b + "documentclass[11pt,a4paper]{article}\n" + b + "usepackage[margin=2.5cm]{geometry}")
rep(b + "graphicspath{{../figs/}}", b + "graphicspath{{../../figs/}}")
rep(b + "bibliography{../refs}", b + "bibliography{../../refs}")
rep(b + "IEEEtriggeratref{12}\n", "")

start = s.index(b + "author{")
end = s.index(b + "maketitle")
s = s[:start] + (
    b + "author{Muhammad Abdullah Aamir" + b + b + " Department of Data Science, FAST-NUCES, Islamabad, Pakistan" + b + b +
    " i232538@isb.nu.edu.pk" + b + "and Muhammad Ibrahim Kiani" + b + b +
    " Department of Data Science, FAST-NUCES, Islamabad, Pakistan" + b + b + " i232536@isb.nu.edu.pk}\n" +
    b + "date{}\n\n") + s[end:]

rep(b + "begin{IEEEkeywords}\n", b + "noindent" + b + "textbf{Keywords:} ")
rep("\n" + b + "end{IEEEkeywords}", "")
# Tables sized for two IEEE columns: give them the single column's width.
rep(b + "setlength{" + b + "tabcolsep}{4pt}\n" + b + "begin{tabular}{@{}L{2.2cm}L{2.3cm}L{2.6cm}L{2.3cm}L{1.7cm}L{2.6cm}L{2.3cm}@{}}",
    b + "setlength{" + b + "tabcolsep}{2pt}\n" + b + "begin{tabular}{@{}L{2.0cm}L{2.0cm}L{2.5cm}L{2.1cm}L{1.6cm}L{2.5cm}L{2.1cm}@{}}")
rep(b + "begin{tabular}{@{}L{1.2cm}cL{3.6cm}L{1.95cm}@{}}", b + "begin{tabular}{@{}L{2.0cm}cL{8.6cm}L{3.6cm}@{}}")
rep(b + "begin{tabular}{@{}L{1.05cm}L{1.95cm}L{2.0cm}L{2.65cm}@{}}", b + "begin{tabular}{@{}L{1.4cm}L{4.0cm}L{4.4cm}L{5.4cm}@{}}")
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(s, encoding="utf-8")
print("written", dst)
