"""Automated checks for the two papers (run on the compiled PDFs).

Usage:
  python Papers/paper_lint.py <paper.pdf> [<other_paper.pdf>]

Checks: banned meta / fourth-wall phrases, leftover artifacts, over-used "AI" vocabulary,
abstract length, Index Terms count, sentence-length statistics, use of "we", citation
numbering (every [n] cited and listed, none missing), figure/table references, PDF metadata,
and - when two PDFs are given - long verbatim overlaps between the papers.
Thresholds are calibrated on the two reference papers (All Dice, No Slice; Take the Hint).
"""
import re
import statistics
import sys

import pypdf

META = [r"\bphase\s*[1-4]\b", r"\b(this|the|our) assignment\b", r"\binstructor\b", r"\bteacher\b",
        r"\bsubmission\b", r"\bcourse\b", r"\bsemester\b", r"\brubric\b", r"\bdeadline\b", r"\b(our|the) grade\b",
        r"\bas requested\b", r"\bthis report\b", r"\bin this document\b", r"\bthe other paper\b",
        r"\bcnet\b", r"\bagentic ai (course|paper)\b", r"\bcomputer networks (course|paper)\b",
        r"\bas an ai\b", r"\blanguage model,? I\b", r"\bhere is\b", r"\bI hope\b", r"\bcertainly\b",
        r"\bfeel free\b", r"\blet me\b", r"\bnote to\b", r"\bplaceholder\b", r"\bwill be (added|updated)\b"]
ARTIFACTS = [r"\?\?", r"\bTODO\b", r"\bTBD\b", r"\bXXX\b", r"lorem ipsum", r"\[citation needed\]", r"\*\*",
             r"(?m)^#+ ", r"`", r"\\[a-zA-Z]+\{", r"Figure \?", r"Table \?", r"\bundefined\b", r"\bNaN\b",
             r"\bnp\.float", r"�", r"\{\}", r"\bS0\d\d\b(?!\))"]
# Words with large post-ChatGPT excess frequency in academic text (Kobak et al., 2024-25) and similar lists.
AI_WORDS = ["delve", "delves", "delving", "showcase", "showcasing", "underscore", "underscores", "intricate",
            "notably", "crucial", "pivotal", "meticulous", "meticulously", "commendable", "realm", "tapestry",
            "landscape", "seamless", "seamlessly", "invaluable", "groundbreaking", "unwavering", "multifaceted",
            "furthermore", "moreover", "additionally", "in conclusion", "it is worth noting", "plays a crucial role",
            "paving the way", "shed light", "a testament", "navigate the", "ever-evolving", "rapidly evolving",
            "holistic", "synergy", "harness", "unlock", "elevate", "embark", "boast"]


def text_of(path):
    r = pypdf.PdfReader(path)
    raw = "\n".join(p.extract_text() or "" for p in r.pages)
    raw = re.sub(r"-\n(?=[a-z])", "", raw)              # undo end-of-line hyphenation
    return r, raw, " ".join(raw.split())


def check(path):
    r, raw, t = text_of(path)
    body = t[:t.rfind("REFERENCES")] if "REFERENCES" in t else t
    refs = t[t.rfind("REFERENCES"):] if "REFERENCES" in t else ""
    low = body.lower()
    print(f"\n=== {path}\npages: {len(r.pages)} | words: {len(t.split())}")
    md = r.metadata or {}
    print("PDF metadata:", {k: md.get(k) for k in ("/Title", "/Author", "/Producer", "/Creator")})

    issues = 0
    for pat in META:
        for m in re.finditer(pat, body, re.I):
            issues += 1; print(f"  [META] {pat!r}: ...{body[max(0, m.start()-50):m.end()+50]}...")
    for pat in ARTIFACTS:
        for m in re.finditer(pat, body):
            issues += 1; print(f"  [ARTIFACT] {pat!r}: ...{body[max(0, m.start()-40):m.end()+40]}...")

    ab = t[t.find("Abstract"):t.find("Index Terms")] if "Index Terms" in t else ""
    it = re.search(r"Index Terms\s*[—-]+\s*(.*?)\.", t)
    n_terms = len(it.group(1).split(",")) if it else 0
    print(f"abstract words: {len(ab.split())} (reference papers: 162-164) | index terms: {n_terms} (reference: 5)")

    sents = [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", body) if len(s.split()) > 3]
    lens = [len(s.split()) for s in sents]
    if lens:
        print(f"sentences: {len(lens)} | mean {statistics.mean(lens):.1f} | median {statistics.median(lens)} | "
              f"stdev {statistics.pstdev(lens):.1f} (reference: mean 28-32, median 23-25)")
    n_we, n_our = len(re.findall(r"\bwe\b", low)), len(re.findall(r"\bour\b", low))
    print(f"'we': {n_we} | 'our': {n_our} (reference: 15-17 / 6-9 per 6 pages)")
    hits = {w: len(re.findall(r'\b' + re.escape(w) + r'\b', low)) for w in AI_WORDS}
    hits = {k: v for k, v in hits.items() if v}
    print("AI-flavoured words:", hits or "none", "(reference papers: furthermore 2, notably 1, crucial 1, robust 2-4)")
    starts = [s.split()[0].strip(",") for s in sents]
    common = {w: starts.count(w) for w in set(starts) if starts.count(w) >= 5 and w not in ("The", "This", "A", "In")}
    if common:
        print("repeated sentence openers (>=5):", common)

    listed = {int(n) for n in re.findall(r"\[(\d+)\]\s", refs)}
    top = max(listed) if listed else 999
    cited = set()
    for a_, b_ in re.findall(r"\[(\d+)\]\s*[–-]\s*\[(\d+)\]", body):      # "[1]–[4]" ranges
        cited |= set(range(int(a_), int(b_) + 1))
    for grp in re.findall(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]", body):
        nums = [int(x) for x in re.findall(r"\d+", grp)]
        if min(nums) < 1 or max(nums) > top:                              # a math interval, not a citation
            continue
        for part in re.split(r"\s*,\s*", grp):
            if re.search(r"[–-]", part):
                a, b = map(int, re.split(r"\s*[–-]\s*", part)); cited |= set(range(a, b + 1))
            else:
                cited.add(int(part))
    if listed:
        miss_list = sorted(cited - listed); never = sorted(listed - cited)
        gaps = sorted(set(range(1, max(listed) + 1)) - listed)
        print(f"references listed: {len(listed)} | cited but not listed: {miss_list} | listed but never cited: "
              f"{never} | numbering gaps: {gaps}")
        order = []
        expanded = re.sub(r"\[(\d+)\]\s*[–-]\s*\[(\d+)\]",
                          lambda m: "[" + ",".join(map(str, range(int(m[1]), int(m[2]) + 1))) + "]", body)
        expanded = re.sub(r"\[(\d+)\s*[–-]\s*(\d+)\]",
                          lambda m: "[" + ",".join(map(str, range(int(m[1]), int(m[2]) + 1))) + "]", expanded)
        for grp in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", expanded):
            for n in map(int, re.findall(r"\d+", grp)):
                if n in cited and n not in order: order.append(n)
        if order != sorted(order):
            print("  [STYLE] references are not numbered in order of first citation (IEEE expects first-use order)")
        issues += len(miss_list) + len(never) + len(gaps)
    for kind in ("Fig.", "TABLE"):
        nums = sorted({int(x) if x.isdigit() else x for x in re.findall(rf"{re.escape(kind)}\s+([0-9IVX]+)", t)},
                      key=str)
        print(f"{kind} labels found: {nums}")
    print(f"TOTAL flagged items: {issues}")
    return set(re.findall(r"\w+", body.lower())), body


def overlap(b1, b2, n=8):
    tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
    g = lambda w: {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
    s1, s2 = g(tok(b1)), g(tok(b2))
    common = s1 & s2
    share = len(common) / max(1, min(len(s1), len(s2)))
    print(f"\n=== cross-paper overlap: {len(common)} shared {n}-word sequences ({share:.1%} of the shorter paper)")
    for c in sorted(common)[:25]:
        print("   ", c)


if __name__ == "__main__":
    bodies = [check(p)[1] for p in sys.argv[1:]]
    if len(bodies) == 2:
        overlap(*bodies)
