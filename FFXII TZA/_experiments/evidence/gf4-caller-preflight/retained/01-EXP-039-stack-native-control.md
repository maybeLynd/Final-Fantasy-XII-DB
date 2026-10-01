---
experiment: EXP-039
title: native known-return control for stopped stack capture
status: COMPLETE - instrument control only
contract: none - Disposable generated native fixture validates instrumentation; it executes no shipping FF12 instructions.
evidence_class: native instrument control
method: Native instrument control - generated disposable fixture
live_game: false
execution_scope: Disposable generated native target, cold and positive stack controls, detach and heartbeat receipts; no FF12 code.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-039-stack-native-control/run_control.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-039: native known-return control for stopped stack capture

**Status:** PASS for the bounded disposable native control; **not original-game validation**.
**Owner:** ASTRA. **Date:** 2026-09-11.

## Question and hypotheses

Does the exact [EXP-038](EXP-038-handler-stack.md) candidate obtain the stack's top qword while
the recognized entry event is stopped, and does it match a known native call-return address?
Mocks alone could miss API declaration, pointer truncation or event-timing defects. A positive
entry with a return location inside controlled native code distinguishes those failures; an
adjacent unexecuted entry supplies a cold control. Neither establishes FFXII handler execution.

## Initial state, instrumentation and action

[target.py](evidence/EXP-039-stack-native-control/target.py) creates only its own executable page.
Its 34-byte fixture is `sub rsp,0x28; call entry; add rsp,0x28; ret`, padding, an executed `ret`
at allocation+32 and an unexecuted `ret` at +33. The call at +4 ends at +9, making the entry's
expected stack-top return address allocation+9. It calls this native wrapper every 50 ms and
appends a heartbeat byte after return. This is native fixture execution, not emulated or game code.

[run_control.py](evidence/EXP-039-stack-native-control/run_control.py), derived from EXP-030's
owned-child control, launches a fresh base-interpreter child for each arm and verifies the ready
PID equals the owned Popen PID. It reads and compares all 34 allocated code bytes before and
after capture. Each arm invokes EXP-038's exact CLI for two seconds, then records four post-detach
snapshots across three intervals, including debugger absence and heartbeat growth. The harness
finally terminates and waits for only its own children. No game process or UI was used.

The candidate source hashes recorded by each CLI result match commit `ea38079`, including its
stack reader and inherited cleanup/event helpers. No source changes occurred between that
candidate's offline tests and these native runs. Hardware breakpoints and the requested cleanup
breakpoint are interventions; this is not a claim of negligible debugger effects.

## Actual observations

| Arm | Owned target PID | Entry hits | Expected top qword | Threads cleared/read back | Post heartbeat increases |
|---|---:|---:|---|---:|---|
| Cold | 37120 | 0 | `0x1BF619C0009` (no hit expected) | 5 | 6, 6, 5 |
| Positive | 17992 | 41 | `0x21ADA790009` | 5 | 6, 6, 6 |

All 41 positive hits returned exactly 64 stack bytes and the expected top qword, preserving
the raw bytes and all eight qwords. The audit has exactly 41 corresponding stopped-stack receipts,
each after the matching single-step event and before its `ContinueDebugEvent`; there are no
unpaired hits or receipts. The cold trace has zero hits and zero stack receipts.

Both capture CLIs returned zero with `PASS`, no recorded errors, successful cleanup and detach.
All four post snapshots per arm showed a live target and no debugger; all three heartbeat deltas
were positive. Final exits `[0,1]` mean the debugger exited normally and the harness subsequently
terminated the still-live owned target. The target exit 1 is expected cleanup, not spontaneous
failure. Both runs completed and both owned processes were waited on.

## Evidence, falsification and limits

- [Cold control](evidence/EXP-039-stack-native-control/cold/control.json),
  [capture](evidence/EXP-039-stack-native-control/cold/capture/result.json),
  [API log](evidence/EXP-039-stack-native-control/cold/capture/api.json).
- [Positive control](evidence/EXP-039-stack-native-control/positive/control.json),
  [capture](evidence/EXP-039-stack-native-control/positive/capture/result.json),
  [API log](evidence/EXP-039-stack-native-control/positive/capture/api.json).
- [Seal](evidence/EXP-039-stack-native-control/seal.py) checks the exact output census, source
  identities, code identity, qword decoding/expected return, event ordering, cleanup and liveness.
  [Summary](evidence/EXP-039-stack-native-control/summary.json) and
  [manifest](evidence/EXP-039-stack-native-control/manifest.json) preserve the result and bytes.

An incorrect return value, short stack read, unpaired event, failed cleanup, debugger retention or
stalled post heartbeat would reject this control. None was observed in these two runs. The
positive proves detection for this controlled entry; it does not turn a future game zero-hit window
into proof of handler absence. The remaining seven stack qwords are raw context, not unwound
callers or identified arguments. Their contents are deliberately not interpreted.

`FABLE-REQ-ASTRA-HANDLERS` remains open. The next reference-game step requires UI resumption,
a fresh runtime reservation and save-preserved loaded-state armed-deadline control, followed by
a verified ordinary fight with an actual enemy death. These disposable results cannot substitute
for that state or its liveness evidence. Game automation remains paused.
