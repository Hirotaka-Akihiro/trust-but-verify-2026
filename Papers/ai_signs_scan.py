"""Scan a LaTeX paper for the AI-writing signs catalogued in Papers/AI_Writing_Signs/.

Run: python Papers/ai_signs_scan.py <paper.tex>
Prints each hit with its line number so it can be reviewed by hand. A hit is a prompt to look,
not a verdict (see AI_Writing_Signs/07_paper_audit_checklist.md).
"""
import re
import statistics
import sys
from pathlib import Path

MARKERS = r"""delve|delves|delving|underscore|underscores|underscoring|showcase|showcases|showcasing|pivotal|crucial|
intricate|intricacies|meticulous|meticulously|tapestry|testament|landscape|realm|garner|foster|fostering|bolster|
leverage|leverages|leveraging|multifaceted|nuanced|groundbreaking|commendable|vibrant|interplay|enduring|boasts|
align with|aligns with|notably|additionally|furthermore|moreover|comprehensive|robust|insights?|enhance|enhances|
enhancing|potential|seamless|seamlessly|paramount|holistic|harness|unlock|unveil|elevate|empower|streamline|
navigate|navigating|ever-evolving|cutting-edge|state-of-the-art|novel|valuable|vital|key role|plays a|serves as|
stands as|sheds light|paves the way|it is worth|it is important|in summary|in conclusion|overall|ultimately|
importantly|significantly|significant|essentially|arguably|remarkably|substantially|utilize|utilizes"""
MARKER_RE = re.compile(r"\b(" + MARKERS.replace("\n", "") + r")\b", re.I)
PATTERNS = {
    "negative parallelism": re.compile(r"\bnot only\b|\bnot just\b|\bnot merely\b|\bnot\b[^.;]{1,60}\bbut\b|\brather than\b", re.I),
    "trailing -ing clause": re.compile(r",\s+(highlighting|underscoring|emphasizing|ensuring|reflecting|demonstrating|"
                                       r"showcasing|illustrating|indicating|suggesting|contributing|making|offering|providing|"
                                       r"revealing|confirming|yielding)\b", re.I),
    "set-up colon": re.compile(r"\b(is simple|is clear|the answer|the reason|the key|the result|the lesson)\s*:", re.I),
    "em/en dash in prose": re.compile(r"---|—"),
    "sentence-initial connector": re.compile(r"(?:^|[.!?]\s+)(Additionally|Moreover|Furthermore|Notably|Importantly|"
                                             r"Overall|Ultimately|Consequently|Thus|Hence|Therefore|Indeed|Crucially)\b"),
    "self-reference": re.compile(r"\b(this (section|paper|work|study) (explores|examines|presents|discusses|shows))\b", re.I),
}


def body(tex):
    t = tex.split(r"\begin{document}", 1)[-1].split(r"\bibliographystyle", 1)[0]
    lines = []
    for i, line in enumerate(t.splitlines(), start=tex[:tex.find(r"\begin{document}")].count("\n") + 1):
        s = line.strip()
        if not s or s.startswith("%") or s.startswith("\\begin{tabular") or "&" in s or s.startswith("\\includegraphics"):
            continue
        lines.append((i, s))
    return lines


def plain(s):
    s = re.sub(r"\$[^$]*\$", "X", s)
    s = re.sub(r"\\(cite|ref|label)\{[^}]*\}", "", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^]]*\])?", "", s)
    return re.sub(r"[{}~]", " ", s)


def main(path):
    tex = Path(path).read_text(encoding="utf-8")
    lines = body(tex)
    hits = 0
    for i, s in lines:
        p = plain(s)
        for m in MARKER_RE.finditer(p):
            print(f"{i:4d} word      {m.group(0)!r:22} ...{p[max(0, m.start()-50):m.end()+40]}...")
            hits += 1
        for name, rx in PATTERNS.items():
            for m in rx.finditer(p if name != "em/en dash in prose" else s):
                print(f"{i:4d} {name:26} ...{p[max(0, m.start()-60):m.end()+50]}...")
                hits += 1
    text = " ".join(plain(s) for _, s in lines)
    sents = [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if len(x.split()) > 3]
    lens = [len(x.split()) for x in sents]
    print(f"\nsentences {len(lens)} | mean {statistics.mean(lens):.1f} | median {statistics.median(lens)} | "
          f"stdev {statistics.pstdev(lens):.1f} | share 8-20 words {sum(8 <= n <= 20 for n in lens)/len(lens):.0%}")
    print(f"semicolons {text.count(';')} | colons {text.count(':')} | flagged items {hits}")


if __name__ == "__main__":
    main(sys.argv[1])
