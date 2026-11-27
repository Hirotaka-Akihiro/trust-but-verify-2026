# Phase 6 video: script and recording guide

**Target length:** about 6 minutes (brief allows 5–7). **Deck:** `23i-2538_23i-2542_23i-2536_Phase-6_Presentation.pptx` (the same script is in each slide's speaker notes).

| Part | Speaker | Slides | Time |
|---|---|---|---|
| Hook, problem, gap, objectives | Aamir | 1–3 | ~1:20 |
| Method, policy, setup | Haider | 4–6 | ~1:25 |
| Live demo | Aamir | 7 | ~1:15 |
| Results, findings, conclusion | Ibrahim | 8–11 | ~1:55 |

## Script

**Slide 1 · Aamir (~20 s).** Imagine an AI agent in charge of your network. For every encrypted flow it decides: allow it, block it, or slow it down. Before anything runs, a policy check approves the action. Our project asks one question: what can that check not see?

**Slide 2 · Aamir (~30 s).** Encryption hides what is inside the packets, so the network has to guess the application from timing alone. The agent acts on that guess, and the policy check reads the same guess. So the check can only be as correct as the prediction behind it.

**Slide 3 · Aamir (~30 s).** Classifier papers report overall accuracy, but not which mistakes actually change an enforcement decision. Guard papers assume the facts they check are correct. So we set four objectives: build a strong classifier, test a policy gate on identical agent actions, trace whatever still gets through, and see whether reading probabilities helps. Haider will walk through the method.

**Slide 4 · Haider (~35 s).** Here is the pipeline. A Random Forest labels each encrypted flow from 23 timing statistics and writes the label into a record the agent can read but not change. The agent, Llama 3.2 3B running locally, proposes one JSON action. Our gate checks it in four steps: valid tool, valid arguments, the right flow, and whether the action is allowed for the predicted application. If any check fails, nothing happens.

**Slide 5 · Haider (~25 s).** The policy has three levels: P2P can only be blocked, streaming and file transfer can be blocked or slowed, and everything else can also be allowed. Because the gate trusts the label, a violation can only get through when a restricted flow is predicted as a more permissive class. That is the formula on the right.

**Slide 6 · Haider (~25 s).** We used ISCXVPN2016: about 18,700 encrypted flows, cleaned and split into 6,000, 2,000 and 2,000. We built 100 scenarios on 50 test flows: normal requests, forbidden requests and injected notes. The agent answered each once, and we replayed that answer under five conditions. Abdullah will now show it running.

**Slide 7 · Aamir, live demo (~75 s).** Say each line when that step appears on screen:
- *Tests:* "Now the code. First the gate's unit tests: 60 out of 60 pass."
- *Step 2:* "Our demo script loads the saved Random Forest: 87.7% accuracy, and 13.6% of file-transfer flows read as chat."
- *Step 4:* "Here the operator asks to allow a P2P flow: with only the prompt it executes, with the gate it is held. Here an injected note tries the same thing, and is held. And here a file-transfer flow the classifier called browsing: the gate lets it through, because the label is wrong."
- *Step 5:* "Finally, all 100 scenarios: 30 violations without the gate, 6 with it."
- *Step 6:* "And each check takes a few microseconds. Ibrahim will go through the results."

**Slide 8 · Ibrahim (~30 s).** First the classifier. Using the dataset's original evaluation protocol, our Random Forest reaches 0.855 weighted precision, 4.7 points above the rebuilt C4.5 baseline and 7.2 above the value the original paper reported. It leads at every flow timeout. Its costliest mistake is reading 13.6% of file-transfer flows as chat.

**Slide 9 · Ibrahim (~30 s).** Now the gate. With the policy only in the prompt, 30 of 100 actions broke it, including all 25 forbidden requests. With the gate, 6 remain, the 95% interval of the reduction is 17.7 to 30.4 points, injections drop to zero, and we keep 97.9% of normal tasks. Each check takes microseconds.

**Slide 10 · Ibrahim (~30 s).** All 6 remaining violations were restricted flows the classifier labelled as permissive. With true labels there are none. Reading class probabilities can remove 5 of them, but only at a 10% over-restriction budget, where just 43 of 50 normal tasks complete.

**Slide 11 · Ibrahim (~25 s).** So that is the answer to our question. The gate stops most violations at almost no cost, but it cannot see a wrong label. For an operator, what matters is how often restricted traffic is mistaken for permissive traffic. Next we want newer traffic, stateful rules and classifiers trained with these costs in mind. Thank you.

## Files to collect in `presentation\cn\recordings`

| Who | Files | How |
|---|---|---|
| Aamir | `s01`, `s02`, `s03` | Sound Recorder, one file per slide |
| Aamir | `demo.mp4` | screen + your voice, recorded together (below) |
| Haider | `s04`, `s05`, `s06` | phone voice memo or Sound Recorder |
| Ibrahim | `s08`, `s09`, `s10`, `s11` | phone voice memo or Sound Recorder |

Any audio format is fine (m4a, mp3, wav). Quiet room, phone about 20 cm away, a little slower than normal speech.

## Recording the live demo (Aamir)

1. Open PowerShell in the project's `implementation` folder. Run `cls`, maximise the window and press Ctrl and + until about 20 lines fill it.
2. Practise once: `python src\demo.py --no-pause` (reads saved results only; changes nothing).
3. Start a screen recording **with microphone on**: Snipping Tool → video → New → select the window → Start (turn on the microphone toggle), or Game Bar with Win + Alt + R.
4. Run `python src\gate_tests.py`, say the *Tests* line.
5. Run `python src\demo.py`, press Enter and say each line as its step appears. Step 5 takes about 15 seconds to show up.
6. Stop after *Done.* and save it as `demo.mp4` in `presentation\cn\recordings`.

When all files are in the folder, the slides, audio and demo get assembled into one MP4.

## Upload

1. YouTube → Create → Upload video. Title: *Trust, but Verify the Label – Phase 6 (23i-2538, 23i-2542, 23i-2536)*.
2. Visibility: **Unlisted**.
3. After processing, play it from the link in a private window, then paste the link into Classroom and press *Turn in*.
