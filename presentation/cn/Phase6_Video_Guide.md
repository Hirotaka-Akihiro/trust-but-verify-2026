# Phase 6 video: script and recording guide

**Target length:** about 6 minutes (brief allows 5–7). **Deck:** `23i-2538_23i-2542_23i-2536_Phase-6_Presentation.pptx` (the script is also in each slide's speaker notes).

| Part | Speaker | Slides | Time |
|---|---|---|---|
| Problem, gap, objectives | Aamir | 1–3 | ~1:20 |
| Method, setup, live demo | Haider | 4–7 | ~2:40 |
| Results, findings, conclusion | Ibrahim | 8–11 | ~1:55 |

## Script

**Slide 1 · Aamir (~20 s).** Assalam-o-Alaikum. We are Abdullah Aamir, Haider Toor and Ibrahim Kiani. Our project is *Trust, but Verify the Label*: what happens when an AI agent manages encrypted network traffic using a classifier's label.

**Slide 2 · Aamir (~30 s).** Encryption hides packet contents, so networks guess the application from flow timing instead. AI agents are now proposed to act on those guesses: allow, block or slow down a flow. A policy check before the action reads the same label, so it can only be as correct as the prediction.

**Slide 3 · Aamir (~30 s).** Classifier papers report overall accuracy, but not which mistakes change an enforcement decision. Guard papers assume the facts they check are correct. So our objectives were to build a strong classifier, measure a policy gate on identical agent actions, trace what still gets through, and test whether reading probabilities helps. Haider will explain the method.

**Slide 4 · Haider (~35 s).** Here is the pipeline. A Random Forest labels each encrypted flow from 23 timing statistics and writes the label into a record the agent can read but not change. The agent, Llama 3.2 3B running locally, proposes one JSON action. Our gate checks it in four steps: valid tool, valid arguments, the right flow, and whether the action is allowed for the predicted application. If any check fails, nothing happens.

**Slide 5 · Haider (~25 s).** The policy has three levels: P2P can only be blocked, streaming and file transfer can be blocked or slowed, and everything else can also be allowed. Because the gate trusts the label, a violation can only get through when a restricted flow is predicted as a more permissive class. That is the formula on the right.

**Slide 6 · Haider (~25 s).** We used ISCXVPN2016: about 18,700 encrypted flows, cleaned and split into 6,000, 2,000 and 2,000. We built 100 scenarios on 50 test flows: normal requests, forbidden requests and injected notes. The agent answered each once, and we replayed that answer under five conditions.

**Slide 7 · Haider, live demo (~75 s).** Switch to the terminal (see *Demo* below) and talk over each step:
- `python src/gate_tests.py`: "First the gate's unit tests: 60 out of 60 pass."
- `python src/demo.py`, then press Enter through the steps:
  - step 2: "It loads the saved Random Forest: 87.7% accuracy, and 13.6% of file-transfer flows read as chat."
  - step 4: "Here the operator asks to allow a P2P flow: with only the prompt it executes, with the gate it is held. Here an injected note tries the same, and is held. And here a file-transfer flow the classifier called browsing: the gate lets it through, because the label is wrong."
  - step 5: "All 100 scenarios: 30 violations without the gate, 6 with it."
  - step 6: "And each gate decision takes a few microseconds."
- Switch back to the slides: "Ibrahim will go through the results."

**Slide 8 · Ibrahim (~30 s).** First the classifier. Using the dataset's original evaluation protocol, our Random Forest reaches 0.855 weighted precision, 4.7 points above the rebuilt C4.5 baseline and 7.2 above the value the original paper reported. It leads at every flow timeout. Its costliest mistake is reading 13.6% of file-transfer flows as chat.

**Slide 9 · Ibrahim (~30 s).** Now the gate. With the policy only in the prompt, 30 of 100 actions broke it, including all 25 forbidden requests. With the gate, 6 remain, the 95% interval of the reduction is 17.7 to 30.4 points, injections drop to zero, and we keep 97.9% of normal tasks. Each check takes microseconds.

**Slide 10 · Ibrahim (~30 s).** All 6 remaining violations were restricted flows the classifier labelled as permissive. With true labels there are none. Reading class probabilities can remove 5 of them, but only at a 10% over-restriction budget, where just 43 of 50 normal tasks complete.

**Slide 11 · Ibrahim (~25 s).** So a deterministic gate stops most violations at almost no cost, but it is only as correct as the label it reads. For an operator, what matters is how often restricted traffic is mistaken for permissive traffic. Next we want newer traffic, stateful rules and classifiers trained with these costs in mind. Thank you.

## Demo setup (on the laptop that has the project)

1. Open PowerShell, then `cd` into the project's `implementation` folder.
2. Make the text large: Ctrl + scroll up until about 20 lines fill the screen.
3. Do one dry run first: `python src/demo.py --no-pause`. It reads the saved results only and changes nothing. Step 5 takes about 15 seconds.
4. During recording run `python src/gate_tests.py`, then `python src/demo.py` and press Enter between steps.

## Easiest way to record with three people

**Option A: one call, recorded (recommended).** Start a Google Meet / Zoom / Teams call, the person with the project shares the screen (slides, then terminal), each of you unmutes for your part, and record the meeting (or record the screen with OBS / Windows Game Bar, Win + Alt + R). Everyone's voice is captured in one take.

**Option B: one laptop.** Sit together, record the screen with OBS or Game Bar (Win + Alt + R, microphone on) and pass the laptop between parts.

Tips: speak a little slower than normal; close notifications (Windows Focus mode); check the first 10 seconds for audio before doing the full take; aim for 5:30–6:30.

## Upload

1. YouTube → Create → Upload video. Title: *Trust, but Verify the Label – Phase 6 (23i-2538, 23i-2542, 23i-2536)*.
2. Visibility: **Unlisted** (anyone with the link can watch; it does not show in search).
3. Wait until processing finishes, play it once from the link in a private window, then paste the link into Classroom and press *Turn in*.
