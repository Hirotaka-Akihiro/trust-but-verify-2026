# Speaker notes – Ibrahim (slides 4–6)

**Your time: ~1 min 30 s.** You start after Aamir says "Ibrahim will show what this changed." The scripts are about 150 words per minute.

---

## Slide 4 – Same 100 proposals: violations fall from 30 to 6 · ~30 s

> We replayed the exact same 100 proposals with and without the gate, so the only difference is the gate itself. Basic format checks catch only the unit errors: 30 violations become 27. The full policy gate cuts them to 6 – a drop of 24 points, and the 95 percent confidence interval stays well above zero. Every injection is stopped. Legitimate work barely changes: 96 percent of legitimate tasks completed without the gate, 94 with it, and back to 96 with one retry.

**Numbers on screen:** 30 → 27 → 6 → 7 violations · −24 pts (95% CI 17.7–30.4) · injections 3 → 0 · tasks 96% → 94% (96% with retry).

---

## Slide 5 – All 6 remaining violations were labelling errors · ~30 s

> Six violations still got through, and all six have the same cause. A restricted flow – file transfer or P2P – was predicted as a permissive class like chat or browsing, so the gate approved an action that was legal for the wrong label. When we give the gate the true labels, violations drop to zero. The gate made no mistakes of its own; the remaining risk sits in the classifier it trusts.

**Example to name if time allows:** S054 – a file-transfer flow predicted as browsing, so "allow" passed.

---

## Slide 6 – Takeaways · ~30 s

> Three takeaways. First, a prompt is not a policy: without the gate, the agent obeyed all 25 forbidden requests. Second, a code gate is cheap and exact: 30 violations down to 6, no injections, at 3.6 microseconds per check against about 3 seconds per LLM call. Third, the gate is only as safe as its labels: every remaining violation came from a misclassified flow, and letting the agent retry recovered 4 tasks but also found 1 new violation. Thank you.

---

## If asked (your part)

| Question | Answer |
|---|---|
| Why is gate + retry 7, not 6? | One retry (S062) picked a 512 kbps limit – legal for the predicted class (file transfer) but not the true one (P2P). |
| What did retry recover? | 4 tasks: the "8 Mbps" request fixed to 8,000 kbps, and 3 injection cases changed from "allow" to the requested "block". |
| Is the 24-point drop real? | Yes. 1,000 bootstrap resamples of the 50 base flows give 17.7–30.4 points; the interval excludes zero. |
| How fast is the gate? | Median 3.6 µs (95th percentile 4.4 µs) over 3,000 timed checks; an LLM call takes a median 2.96 s. |
| How do you know the gate is correct? | It matches an independently written policy table on all 77,035 possible actions, and passes 20 hand-written test cases. |
| What would you do next? | Make the gate cautious when the classifier is unsure; test bigger models; add time-of-day and bandwidth-budget rules. |
