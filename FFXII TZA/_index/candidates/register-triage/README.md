# Register triage — the 292 outstanding rows, 2026-09-26 (FABLE, Claude Opus 5.5)

`goal_gate.py` fails the questions dimension until every register row is resolved or carries an accepted
disposition. On 2026-09-26 `check_questions.py` counts **OPEN 170, PARTIAL 118, BLOCKED 4**. This folder routes each
of those rows.

**What this is and is not.** `register_triage.tsv` is a *classification pass*: each row's own text was read, and
linked pages were skimmed only where a row was ambiguous. It routes work. It closes nothing, and it claims no answer.
A route is a starting judgement, and every closure still needs its own reading, control and publish.

| route | rows | meaning |
|---|---:|---|
| STATIC-SMALL | 82 | a bounded static read (one to a few functions, or a data file already extracted) should answer it; the TSV gives the next step |
| STATIC-LARGE | 47 | static, but a large read or census |
| SCOPE-OR-PROCESS | 70 | coverage, census, tooling, governance or propagation; not a question about how the game behaves |
| ALREADY-ANSWERED-ELSEWHERE | 43 | the row's own cells or a linked page already meet the question; only the status word may be stale (verify each before changing it) |
| RUNTIME | 30 | only a live run answers the remainder; 23 already carry a tier-1 static claim (SUPERSEDED candidates under the classifier's own rule) |
| INTENT | 19 | a designer's name or intent, or a build artefact that does not ship; several need an evidence-boundary ruling |
| UNCLEAR | 1 | UQ-147 |

**The SCOPE-OR-PROCESS rows need a policy, not readings.** They fall into six kinds:
- coverage residue ("the other N functions are unread"): 24 rows;
- third-party or vendor bodies: 11;
- tooling and census method: 18;
- governance and metrics: 7;
- document propagation or page ownership: 7;
- evidence-boundary reframings: 3.

Options for a planner (FRONTIER):
- retire coverage and vendor rows into declared EC-7 dispositions, with members files, so they leave the question
  gate but stay visible as inventory;
- move tooling and governance rows to the process board as NOT A QUESTION;
- close propagation rows as tasks;
- make one evidence-boundary ruling: is the PS2 build admissible, and may NO ADMISSIBLE SOURCE extend to build
  artefacts that do not ship? That one ruling would also settle about six INTENT rows.

Together these would remove about 90 rows without claiming a finding. Duplicate pairs to merge: BN-6/UQ-305,
UQ-245/BR-5, UQ-289/EA-5, HM-1/UQ-216, FT-2/UQ-120.

**Already done from this list on 2026-09-26:** D-5 answered (`_index/candidates/d5-reserved-surfaces/`), and FE-7
opened as the separable half of FE-6 (`_index/candidates/fe6-kind-gates/`).
