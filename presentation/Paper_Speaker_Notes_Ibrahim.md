# Speaker notes: Ibrahim (slides 6–10, about 1.5 minutes)

**6. Tools, data and implementation**
We used the ISCXVPN2016 encrypted-traffic dataset. The Random Forest reaches 87.7% accuracy. The agent is Llama 3.2 3B running on a laptop. The gate is plain Python, checked on all 77,035 combinations of tool, class and rate. We built 100 scenarios: normal requests, forbidden requests and injected notes.

**7. Results: the gate stops most violations**
With only the prompt, 30 actions broke the policy, and the agent obeyed all 25 forbidden requests. With the gate, 6 remain, injections drop to zero, and we keep 97.9% of normal tasks. Each check takes 3.6 microseconds.
*Point at:* the first bar (30), then the "M gate" bar (6).

**8. Retry helps, but label errors remain**
Sending the rejection reason back recovered 4 tasks but created one new violation: the agent found an action the gate accepts but the real rule forbids. All 6 remaining violations come from wrong classifier labels; with correct labels there are none.

**9. Comparison with base papers**
The base papers use different benchmarks, so we compare effect size and cost. Our gate cuts violations by 24 points with no extra model calls, while an AI verifier needs up to 2.2 times as many calls. It works because our policy is a simple lookup.
*Point at:* the orange "This work" row.

**10. Contributions and conclusion**
In short: a prompt is not enforcement; a small code gate is, but it is only as good as the labels it reads. Next we want bigger models, multi-step tasks and better handling of uncertain labels. Thank you, we are happy to take questions.

---
**Numbers to remember:** 87.7% classifier accuracy · 100 scenarios on 50 flows · 4 recovered, 1 new violation on retry · 6 of 6 leftovers are label errors · CI 17.7–30.4 points.
