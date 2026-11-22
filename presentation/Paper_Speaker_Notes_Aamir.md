# Speaker notes: Aamir (slides 1–5, about 1.5 minutes)

**1. Title**
Assalam-o-Alaikum. Our paper is *Prompts Are Not Policies*. An AI agent manages network traffic: it can allow, block or slow down a flow. We test whether rules written in its prompt are enough, or whether it needs a small code check before every action.

**2. Why this problem matters**
Agents now act through tools, and their rules usually sit in the prompt, so obeying them is the model's choice. In a network, one wrong action hits every packet of a flow, and the flow's type comes from a classifier that can be wrong. That is our research problem, on the right.
*Point at:* the dark "Research problem" box.

**3. Existing work and the gap**
Earlier work either adds a second model to review each action, which costs extra calls, or runs code rules before a tool executes. Both are mostly tested on customer service, web and code tasks, and both trust their input facts. The network-agent studies we reviewed do not let an agent act on single flows.
*Point at:* the orange "Gap" box.

**4. Research questions**
We ask four questions: how often the agent breaks the rules with only a prompt, how much a gate prevents, whether telling it why it failed helps, and what still gets through. The agent answers each scenario once, and we replay that same answer under every condition.

**5. Architecture and workflow**
A Random Forest labels each flow. The agent sees that label and the request, and proposes one JSON action. The gate runs the four checks at the bottom; if any fails, nothing is executed. Ibrahim will cover the setup and results.
*Point at:* the four boxes at the bottom, left to right. Hand over to Ibrahim.

---
**Numbers to remember:** 30 → 6 violations · 25 of 25 forbidden requests obeyed · 3 → 0 injections · 97.9% of tasks kept · 3.6 µs per check.
