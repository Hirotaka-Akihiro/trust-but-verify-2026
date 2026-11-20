# Signs of AI Writing: Research Notes

Notes collected from public guides and studies on how AI-generated text is recognized, by people and by detection software. They are used to audit the two project papers.

| File | Contents |
|---|---|
| [01_vocabulary.md](01_vocabulary.md) | Words and phrases that language models overuse |
| [02_sentence_patterns.md](02_sentence_patterns.md) | Sentence-level habits: parallelisms, triads, trailing -ing clauses, rhythm |
| [03_content_and_tone.md](03_content_and_tone.md) | Inflated significance, vague attribution, hedging, formulaic sections |
| [04_formatting_and_leftovers.md](04_formatting_and_leftovers.md) | Formatting habits, chatbot phrases, placeholders, Markdown residue |
| [05_citations.md](05_citations.md) | Citation problems typical of generated text |
| [06_how_detectors_work.md](06_how_detectors_work.md) | Perplexity, burstiness, probability curvature, trained classifiers, limits |
| [07_paper_audit_checklist.md](07_paper_audit_checklist.md) | The checklist applied to the papers, with what counts as a real problem |

## Two cautions from every source

1. **Signs are symptoms, not proof.** One or two marker words can be coincidence; what matters is clusters. Perfect grammar, formal register and transition words on their own are not reliable signs.
2. **Detectors make mistakes.** They give probabilities, not verdicts, and they are weaker on short, technical or heavily edited text. The aim of the audit is clear, specific writing, not "beating" a detector.

## Sources

- Wikipedia: Signs of AI writing (WikiProject AI Cleanup advice page, read November 2026). https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- TechCrunch, "The best guide to spotting AI writing comes from Wikipedia" (20 Nov 2025). https://techcrunch.com/2025/11/20/the-best-guide-to-spotting-ai-writing-comes-from-wikipedia/
- D. Kobak, R. González-Márquez, E.-Á. Horvát, J. Lause, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary," arXiv:2406.07016 (v5). https://arxiv.org/abs/2406.07016
- Kumar et al., "Deep dive into language traits of AI-generated Abstracts," arXiv:2312.10617. https://arxiv.org/abs/2312.10617
- E. Mitchell et al., "DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature," ICML 2023, arXiv:2301.11305. https://arxiv.org/abs/2301.11305
- GPTZero, "How AI detectors work." https://gptzero.me/news/how-ai-detectors-work/
- Pangram Labs, "How it works." https://www.pangram.com/research/how-it-works
- Scribbr, "How do AI detectors work?" (found in search; page refused automated reading). https://www.scribbr.com/ai-tools/ai-detector/how-do-ai-detectors-work/
