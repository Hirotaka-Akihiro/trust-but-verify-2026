# 6. How AI Detectors Work

## 6.1 Statistical signals

- **Perplexity:** how predictable each word is to a language model, given the words before it. Highly predictable text has low perplexity and is more likely to be flagged. (GPTZero)
- **Burstiness:** how much perplexity and sentence length vary across a document. Human writing alternates short and long, plain and dense; generated text is more even. (GPTZero)
- **Probability curvature (DetectGPT):** generated text sits near a local maximum of the model's log-probability. Slightly rewording a generated passage lowers its probability more than rewording a human passage does. DetectGPT perturbs the text with a second model and compares. It needs no training data and reported AUROC 0.95 on GPT-NeoX 20B news text. (Mitchell et al., ICML 2023)
- **Trained classifiers:** current commercial tools (GPTZero, Pangram) use neural classifiers trained on large sets of human and AI documents. Pangram retrains on human texts it wrongly flagged and on AI text written to imitate specific human samples, and labels each segment Human, AI-assisted or AI-generated.

## 6.2 What raises a detector score

- Even sentence length and structure
- Predictable word choice and stock phrases
- Repeated words and phrases
- Smooth, generic prose without specific detail

GPTZero states that its model is designed to ignore em dashes and semicolons. These remain signs for human readers, but are not scored features of that detector.

## 6.3 Limits and false positives

- No detector is fully accurate; vendors report their own benchmarks (for example, GPTZero cites 1% false positives on the RAID benchmark).
- Scores are probabilities, and the vendors themselves say they should not be the sole basis for a decision.
- Short passages, mixed human/AI text and lightly AI-edited text are harder to classify; many tools cannot tell grammar correction from generation.
- Technical writing has a narrow vocabulary and conventional structure, so it naturally scores as more predictable.
- Most detectors are trained mainly on English; GPTZero reports work on bias against non-native writers.
- Humans detect AI text only slightly better than chance; people who use AI tools heavily do better.

## 6.4 What reads as human

- Mix short and long sentences.
- Use concrete, checkable detail (numbers, names, conditions) instead of general claims.
- Use plain verbs and one consistent name for each thing.
- Keep the author's own voice consistent across sections.
- Keep drafts and version history (the git log serves this purpose here).
