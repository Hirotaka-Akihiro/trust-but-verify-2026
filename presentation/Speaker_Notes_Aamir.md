# Speaker notes – Aamir (slides 1–3)

**Your time: ~1 min 20 s.** Ibrahim takes over at slide 4. Speak at a normal pace; the scripts are about 150 words per minute.

---

## Slide 1 – Trust, but verify · ~20 s

> An LLM agent decides what happens to network traffic: it can allow a flow, block it, or limit its speed. The network operator's policy is written into the agent's prompt. Our question is simple: can a few lines of code stop an LLM agent from breaking that policy?

**Point at:** the green phrase "a few lines of code" – that is the gate.

---

## Slide 2 – The agent obeyed the operator, not the policy · ~30 s

> We gave the policy to Llama-3.2-3B, running locally, and tested it on 100 scenarios built from real encrypted-traffic flows. 30 of its proposals would have broken the policy. In all 25 cases where the operator asked for something forbidden – like "allow this P2P flow for a demo" – the model simply complied. 3 fake "pre-approved" notes changed its action, and twice it turned megabits into a number a thousand times too large. A prompt alone is not enforcement.

**Numbers on screen:** 30 / 100 unsafe · 25 / 25 conflicts obeyed · 3 / 25 injections worked · 2 / 50 unit errors ("8 Mbps" → 8,000,000 kbps).

---

## Slide 3 – The model only proposes; the gate decides · ~30 s

> So we separated proposing from acting. A Random Forest labels each flow's application from timing features only – 87.7 percent accurate. The LLM then proposes one tool call. Before anything reaches the network, a deterministic gate – plain Python – checks the call's format, the flow ID, and three policy rules. If the check fails, the flow stays on hold; in one variant the rejection reason goes back to the agent for a single retry. Ibrahim will show what this changed.

**Rules on screen:** P1 P2P → block only · P2 streaming / file transfer → block or ≤ 1,024 kbps · P3 browsing, email, chat, VoIP → allow, block or ≤ 10,000 kbps.

**Hand over:** "Ibrahim will show what this changed."

---

## If asked (your part)

| Question | Answer |
|---|---|
| Which model, and why so small? | Llama-3.2-3B-Instruct, 4-bit, on a laptop CPU via llama.cpp. Cheap, local, repeatable (temperature 0). |
| Where does the traffic come from? | ISCXVPN2016 – public encrypted / VPN traffic from the University of New Brunswick. 7 applications. |
| Why a Random Forest? | Best of three models on validation data (majority baseline, Decision Tree, Random Forest). |
| Does the classifier see packet contents? | No – only 23 timing statistics per flow. No payload, IPs or ports. |
| What is a "violation"? | An action that breaks the policy for the flow's **true** application, e.g. allowing a P2P flow. |
