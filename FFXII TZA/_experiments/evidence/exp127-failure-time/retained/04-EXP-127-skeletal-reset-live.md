---
experiment: EXP-127
title: Skeletal reset boundary hits followed by a post-trace runtime error
status: INVALID — full session health failed; captured observations retained pending review
contract: none — targeted runtime request; no contract closure from this failed session
tool: evidence/skeletal-reset-live/run_window.py
method: C - ordinary save load followed by labelled hardware-breakpoint intervention
live_game: true
evidence_class: original-process-intervention-provisional
execution_scope: One reference FF12 process, Stepping idle; one 1s positive and one 1s four-slot trace
contract_coverage: No promotion; execution-boundary observations require independent failure-aware review
date_designed: 2026-09-20
date_run: 2026-09-20
---

# EXP-127 — ASTRA skeletal execution observations and failed session health

The trace recorded ordinary loaded-state visits to `003E3C30`, its nonempty
index-reading loop and the return from `00203170`. **The session is INVALID:**
FF12 subsequently displayed a Microsoft Visual C++ Runtime Library termination
dialog. Successful debugger API receipts, cleared registers and continued CPU
activity did not establish healthy gameplay. No normal post-test responsiveness
action completed. The process was closed through the error dialog; original
save/config/reference state is restored. No retry was made.

Player version: while Vaan stood in The Stepping, the bone-reset code was
observed running. The game later failed, so these observations are preserved
for review rather than treated as a clean successful test.

## ASTRA question, hypotheses and method

Request: `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME`. EXP079 already supplies retained
zero-base samples and a successful low-address read. The remaining question is
whether normal loaded-character behavior reaches the skeletal reset entry,
nonempty body and visitor return. H1 predicts those observed boundaries; H2
predicts one or more unobserved boundaries in this selected route. A zero-hit
route would not establish global absence. Method C is necessary for actual
initialization and ordinary reachability; isolated arithmetic cannot supply it.

The decoder-base question is separate. A zero base can coexist with valid
low-address references; it does not imply dead consumers, authored-only storage,
a skeleton allocation extent or an all-time zero invariant. The corresponding
OPUS inference contradiction remains open.

The predeclared bound was one 1-second known-entry control followed, only if
qualified, by one 1-second four-slot window. There was no injected game call,
game-data write, movement or combat. Attaching the debugger, changing thread
debug contexts and requesting the cleanup breakpoint are interventions. They
can affect timing. This is not an unmodified-playback or performance capture.

## ASTRA reference and starting state

PID `31940`, designated Steam `x64/FFXII_TZA.exe`, image base `00120000`:

- EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
- Full mapped `.text`, 7,996,981 bytes: `5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
- Shipping 109-byte reset function: `de32a6a5ea6bdf5c88ee98452efa87981010f7f0646cfd237222e543392b7913`.

[Preflight](evidence/skeletal-reset-live/preflight.json) retains target bytes,
disassembly, Python/Capstone identity, clean reference-directory checks and exact
tool hashes. EXP030 capture/cleanup and EXP031 recovered observer were unchanged.
The existing held-key sender has only three adapter changes: two directory roots
and the current runtime-task guard. Its source and hash are retained. No control
scheme rediscovery or general runtime platform was introduced.

Fresh copies of all 26 save/config files were verified before launch; Cloud was
observed off and left unchanged. Loaded modern save `76561198045890736/FFXII_000`,
5,331 bytes, SHA256 `859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825`.
Three held Enter pulses registered at index49 and were released. Separate images
show the selected Stepping save, Load complete and Vaan standing with HP103/103,
MP33. Those images establish presentation; input receipts establish registration.
No combat command, executed attack or damage/death consequence was tested.

Title, loaded-before and loaded-after snapshots each verified full text before
and after, nonzero LUAC bytes `19930d0a1a0a`, rejected null reads, recorded module
paths and closed the read handle. Module-path inventories do not certify every
DLL byte, heap value or external state. The post snapshot was still readable and
debugger-free even though the later screenshot showed the fatal dialog.

## ASTRA raw observations and normalization

| Boundary | Control window | Skeletal window |
|---|---:|---:|
| `003A1C50` known-entry positive | 202 | 205 |
| `003E3C30` reset entry | not armed | 1,022 |
| `003E3C7A` after index read, before matrix helper call | not armed | 2,113 |
| `003E3C7F` helper returned | not armed | 2,113 |

All recorded hits were on thread30100. Every observed pre-call pairs in order
with a post-call on the same thread and stack depth; none is orphaned in this
window. All 2,113 pre-call frames are 40 bytes below the preceding observed
entry's stack pointer, consistent with the shipping prologue. The 1,022 entry
hits contain 16 distinct RCX values, `6DD2C830..6DF42030`. Pre-call RCX ranges
`6DD26070..6DF41FC0`. These are register observations; no captured pointer was
dereferenced to infer object ownership, extent or lifetime.

The original function skips its loop for count+8C zero. The pre-call boundary is
after `mov ecx,[rbx]` and the stride calculation; entry alone would not establish
that path. A returned helper does not by itself prove all its memory effects.
No frame rate, frequency, object count or ordinary timing follows from hit totals.

Two base-qword samples in each of the three memory captures were zero. They are
sequential samples, **not atomic base reads at the 5,453 trace events**. Together
with EXP079 they make the low-address alternative worth preserving; they do not
prove zero at every intermediate instruction or settle every decoder caller.

Primary artifacts:

- [Control result](evidence/skeletal-reset-live/control/capture/result.json),
  [API receipts](evidence/skeletal-reset-live/control/capture/api.json) and
  [liveness](evidence/skeletal-reset-live/control/liveness.json).
- [Skeletal result](evidence/skeletal-reset-live/skeletal/capture/result.json),
  [API receipts](evidence/skeletal-reset-live/skeletal/capture/api.json) and
  [liveness](evidence/skeletal-reset-live/skeletal/liveness.json).
- [Normalized observations and input hashes](evidence/skeletal-reset-live/normalized.json),
  reproduced offline by `evidence/skeletal-reset-live/assess.py`.
- [Post-trace presentation](evidence/skeletal-reset-live/loaded-after.jpg),
  [fatal dialog](evidence/skeletal-reset-live/runtime-error.jpg) and
  [dialog identity/text](evidence/skeletal-reset-live/runtime-error.json).

## ASTRA failed qualification and affected claims

The control armed/cleared/read back 101 threads; the target window did so for102.
Both detached successfully. The independent observer recorded 1,149/1,147 samples,
no held inputs, FF12 as foreground, debugger absent before/after, and positive
post-detach CPU deltas of4.78125/2.359375 seconds. The target post interval spans
about9.65 seconds. Those narrow receipts remain facts. They are insufficient to
override the visible runtime error. The raw `QUALIFIED_WINDOW` labels are
historical instrument-window outputs, **not the final experiment verdict**.

The error's exact onset and cause were not captured. Context handling, high
breakpoint traffic, later observation or an unrelated native failure have not
been distinguished. No causal claim is made. Repeating this method unchanged is
blocked pending instrument review; no live rerun was performed after the failure.

The immediate problem was contained by closing the instance and restoring state.
`assess.py` adds the smallest final-assessment regression: the actual
CPU-positive/API-positive/error-visible combination must return
`INVALID_POST_TRACE`; missing responsiveness, zero positive hits, failed trace
checks or missing restoration cannot pass. Its synthetic nominal branch is only
a test of that gate, **not a repaired instrument or live qualification**.
[Regression receipt](evidence/skeletal-reset-live/assessment-checks.json).

Affected conclusions: EXP127 healthy-session/reusability, unconditional ordinary
reachability promotion, and consumer closure of the arena/skeleton request remain
withheld. The recorded boundary observations are provisional pending independent
SWE2-AUDIT-SPEC review and OPUS adjudication. No types, executable specifications,
contracts or EC-7 dispositions were promoted from this run. EXP079 read-only and
EXP124 read-only evidence did not depend on this debugger window; they are not
retracted. EXP031's own bounded historical receipts remain, but do not authorize
this higher-event-rate four-slot route as safe or healthy.

## ASTRA cleanup and exact next action

The FF12-owned error dialog was acknowledged; subsequent window/process censuses
show no FF12 or scoped test helpers. PC control was reset and its helper exited.
Both debugger children and read observers had terminated before the dialog was
closed. No game restart, extra trace or experimental save was made.

[Cleanup](evidence/skeletal-reset-live/cleanup.json) verifies all26 files against
the fresh session backup and the original executable hash. Only the account
`GameSetting.ini` adapter LUIDLow changed79439→78748; its changed copy was preserved
in ASTRA scratch before restoring the exact backup. No save bytes changed.
`@runtime` is released. Historical pre-run handoff receipts remain untouched.

**Next action is offline:** auditor re-derives boundary pairing from raw traces,
checks exact original instructions/context/cleanup semantics, and rules what can
be retained despite the failure. OPUS consumes only the accepted scope and keeps
storage/extent separate. Any required instrument repair must name the failure
hypothesis and its small control before a future live rerun. A live rerun, if
still necessary, needs fresh backup/identity and the same identified Stepping
save, with explicit post-test gameplay responsiveness and no fatal dialog; no
reuse of the closed PID, old outputs or a zero-hit counting exercise.

ASTRA is parked for the user's durable usage handoff. Authorization remains
ACTIVE, but a future stop/takeover immediately suspends automation. The queue
continues offline with peer owners; only these specific runtime-dependent claims
wait. Full L1/L2 database completion and its required final reviews remain open.
