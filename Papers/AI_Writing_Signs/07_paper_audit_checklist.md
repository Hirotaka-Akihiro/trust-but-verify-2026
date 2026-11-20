# 7. Paper Audit Checklist

How to apply notes 1–6 to an IEEE research paper. Mark an item as a problem only when it is a real pattern, not a single harmless use.

## A. Vocabulary (note 1)

- [ ] No Kobak/Wikipedia marker words: delve, underscore, showcase, pivotal, crucial, intricate, meticulous, tapestry, testament, landscape, realm, garner, foster, bolster, leverage, multifaceted, nuanced, groundbreaking, commendable, vibrant, interplay, enduring, boasts, align with.
- [ ] No more than an occasional *notably, additionally, furthermore, moreover, comprehensive, robust, potential, insights, enhance*, and none as sentence openers in a run.
- [ ] *significant* used only with a statistical meaning.
- [ ] Plain verbs: *use, is, has, show* rather than *utilize, serves as, boasts, showcase*.

## B. Sentence patterns (note 2)

- [ ] No more than one "not X but Y" / "X rather than Y" construction per section, and only where the contrast carries information.
- [ ] Triads only when they list three real items.
- [ ] No evaluative trailing -ing clause ("..., highlighting ...", "..., underscoring ...", "..., ensuring ...").
- [ ] No set-up/payoff colons used for effect ("The reason is simple: ...").
- [ ] Sentence lengths vary (check with `paper_lint.py`; the reference papers average 28–32 words with a wide spread).
- [ ] One name per concept (no elegant variation).
- [ ] No em dashes; semicolons limited to real lists or tightly linked clauses.

## C. Content (note 3)

- [ ] Each claim of importance is backed by a number or a citation.
- [ ] No uncited "prior work shows".
- [ ] No "it is important/worth noting".
- [ ] No paragraph ends with a moral that repeats the paragraph.
- [ ] The conclusion adds the outcome and next steps, not a restatement of every section.

## D. Formatting and leftovers (note 4)

- [ ] No chatbot phrases, placeholders, Markdown, TODOs or tool artefacts (`paper_lint.py` META and ARTIFACT checks).
- [ ] Bold only where the reference papers use it (contribution labels, best results in tables).
- [ ] Headings follow IEEE style as in the reference papers.

## E. Citations (note 5)

- [ ] All references resolve and the metadata matches (`verify_refs.py`).
- [ ] Every number attributed to a paper appears in that paper.

## F. Correctness guard (applies to every rewrite)

- [ ] Every number after a rewrite still matches `derived_numbers.json` and the results files.
- [ ] No claim is made stronger or weaker than the data supports.
- [ ] Page count, figure and table numbering and cross-references are unchanged or still correct.
