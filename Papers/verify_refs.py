"""Fetch authoritative metadata for every candidate reference (Crossref for DOIs, arXiv API for preprints).

Run: python Papers/verify_refs.py  ->  Papers/verified_refs.json
"""
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DOIS = {
    "drapergil2016": "10.5220/0005740704070414",
    "elshewey2025": "10.1038/s41598-025-21261-6",
    "zwerdling2025": "10.18653/v1/2025.emnlp-industry.41",
    "wang2026agentspec": "10.1145/3744916.3764546",
    "sah2026verifier": "10.1145/3786335.3813160",
    "wang2024netconfeval": "10.1145/3656296",
    "wang2025confucius": "10.1145/3718958.3750537",
    "adanza2026": "10.1016/j.comnet.2025.111809",
    "greshake2023": "10.1145/3605764.3623985",
    "lotfollahi2020": "10.1007/s00500-019-04030-2",
    "rezaei2019": "10.1109/MCOM.2019.1800819",
    "breiman2001": "10.1023/A:1010933404324",
}
ARXIV = {
    "debenedetti2025camel": "2503.18813",
    "debenedetti2024agentdojo": "2406.13352",
    "andriushchenko2025agentharm": "2410.09024",
    "xiang2025guardagent": "2406.09187",
    "chen2025shieldagent": "2503.22738",
    "yao2023react": "2210.03629",
    "yao2025taubench": "2406.12045",
    "grattafiori2024llama3": "2407.21783",
    "kang2026policyguard": "2606.29225",
    "wu2026policyinvisible": "2604.12177",
    "guo2017calibration": "1706.04599",
    "schick2023toolformer": "2302.04761",
    "sah2026verifier_arxiv": "2603.19328",
}
UA = {"User-Agent": "reference-verifier/1.0 (academic use)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def crossref(doi):
    m = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
    return {"source": "crossref", "doi": doi, "type": m.get("type"),
            "title": " ".join(m.get("title", [])),
            "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in m.get("author", [])],
            "venue": " ".join(m.get("container-title", [])),
            "year": (m.get("published-print") or m.get("published-online") or m.get("issued"))["date-parts"][0][0],
            "volume": m.get("volume"), "issue": m.get("issue"), "pages": m.get("page"),
            "article_number": m.get("article-number"), "publisher": m.get("publisher")}


def arxiv(aid):
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(get(f"http://export.arxiv.org/api/query?id_list={aid}"))
    e = root.find("a:entry", ns)
    jr = e.find("x:journal_ref", ns); cm = e.find("x:comment", ns); doi = e.find("x:doi", ns)
    return {"source": "arxiv", "arxiv": aid,
            "title": " ".join(e.find("a:title", ns).text.split()),
            "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
            "year": int(e.find("a:published", ns).text[:4]),
            "journal_ref": jr.text if jr is not None else None,
            "comment": " ".join(cm.text.split()) if cm is not None else None,
            "doi": doi.text if doi is not None else None}


out = {}
for k, d in DOIS.items():
    try:
        out[k] = crossref(d)
    except Exception as ex:
        out[k] = {"error": str(ex), "doi": d}
    time.sleep(0.4)
for k, a in ARXIV.items():
    try:
        out[k] = arxiv(a)
    except Exception as ex:
        out[k] = {"error": str(ex), "arxiv": a}
    time.sleep(3.2)                      # arXiv API etiquette
Path(__file__).with_name("verified_refs.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
for k, v in out.items():
    if "error" in v:
        print(f"{k}: ERROR {v['error']}")
    else:
        au = v["authors"]
        print(f"{k}: {v['title'][:80]} | {au[:3]}{'...' if len(au) > 3 else ''} ({len(au)}) | "
              f"{v.get('venue') or v.get('journal_ref') or v.get('comment') or ''} | {v['year']} | "
              f"{v.get('volume') or ''} {v.get('pages') or v.get('article_number') or ''}")
