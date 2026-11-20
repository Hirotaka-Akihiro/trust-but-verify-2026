# 5. Citations

The citation checks are the most concrete of all the signs, because they can be verified.

- **Hallucinated references:** papers that do not exist, or real authors attached to invented titles.
- **Invalid DOIs or ISBNs:** a DOI that does not resolve, or an ISBN with a bad checksum.
- **DOIs that resolve to a different paper** from the one described.
- **Wrong metadata:** a correct title with the wrong year, venue, volume or pages.
- **Book citations without page numbers** that the claim cannot be traced to.
- **Claims the source does not make:** the cited paper exists but does not report the number or finding attributed to it.
- **Broken links** that are not in any web archive.
- **Tracking parameters** (`utm_source=chatgpt.com`) or exposed citation tokens.
- **Defined but unused, or used but undefined,** references.

## How the papers were checked

Every DOI was resolved through Crossref, every arXiv ID through the arXiv API, and every conference paper against its proceedings page (PMLR, ICLR, ACL Anthology). Every number quoted from another paper was found in that paper's own text. See `../verify_refs.py`, `../verified_refs.json` and `../paper_lint.py` (cited-but-not-listed check).
