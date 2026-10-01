---
experiment: EXP-016
title: Does clearing breakpoints before continuing the final event prevent input loss?
status: CHECKPOINT — comparator input control incomplete
contract: none — diagnostic instrument experiment
tool: private hwbp variant in EXP-016-cleanup
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-10
date_run: 2026-09-10
---

# EXP-016 — final-event cleanup ordering

## Question, evidence and prediction

[EXP-015](EXP-015-loaded-state-armed-control.md) preserved the loaded state with a
zero-hit armed site, then lost input after two angle-normalizer entry/ret-site hits.
The old instrument continues the final event before clearing debug registers.
Microsoft documents that [debug events suspend all process threads](https://learn.microsoft.com/en-us/windows/win32/debug/writing-the-debugger-s-main-loop)
and [running-thread contexts are invalid](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getthreadcontext).
That supports testing this ordering; it does not prove the failure's cause.

H1: clearing while the final event still holds the threads stopped prevents the
input failure. H2: input still fails, so this ordering change alone is insufficient.
If any context write/continue/detach fails, or the expected two-hit boundary is not
reached, classify the comparison as invalid for the proposed discriminator.

## Exact intervention and controls

[Evidence and source](evidence/EXP-016-cleanup/) retain the exact old instrument,
hash-guarded variant generator and complete diff. `--cleanup-before-continue` clears
all enumerated threads before the final resume/ContinueDebugEvent; skips the later
clear only if every earlier clear succeeds. The two original resume operations stay
unchanged. API proxy records results, flags, selected contexts and event order in
memory, writing JSON after detach; it changes timing and is a stated confound.
No shared instrument is edited. Legacy printed success is not a scientific verdict.

Two deterministic event fixtures compare order and inject a failed clear. They
exercise the private Python event path, not Win32 or original game execution.

Fresh verified save/config backup; same reference executable and The Stepping
autosave (00:08:42, Vaan level 1), area 227. Require visible field before baseline.
Run 65-second baseline, private positive stage at `003A1C50` / `003A1C8C` capped at
two hits or ten seconds, and separate 65-second post stage. Reuse EXP-015 read-only
observer and held Enter/C controls with explicit screenshots while the menu should
be open. Verify source/executable/live text, full modules, focus, debugger absence,
repeated CPU intervals, input bytes and cleanup. Preserve failures and restore saves.

If the modified order survives, a fresh same-proxy original-order control is needed
before assigning causality to ordering rather than timing. If it fails despite all
API calls succeeding and expected ordering, do not call it a repair; use the result
to select a narrower trap/resume experiment.

## First runtime arm: clear before continue

Reference PID **35004**, area **227**, same named save. The Load complete screen
persisted until explicit Space confirmation; `dismiss-load-input.json` and the
subsequent `loaded-field.jpg` establish the usable recipe. The baseline began only
after that visual field proof. Do not wait indefinitely on the memory classifier.

The positive stage records one entry/ret-site pair on thread **31796**, XMM0
**-3.13068414** at both sites. All 102 enumerated threads were cleared successfully
inside the final event before its continuation; the later clear was skipped.
The API log records 311 successful GetThreadContext, 309 successful SetThreadContext,
208 successful ContinueDebugEvent and successful DebugActiveProcessStop. Inspect
the exact ContextFlags before interpreting individual context fields.

| Window, each 65 s | Five-second CPU fractions of one core | Input and visual response |
|---|---|---|
| Baseline | 0.422–0.519 | Enter/C bytes 49/2; menu opens/closes |
| Modified capture | 0.462–0.632 | Same bytes; menu opens/closes after capture |
| Separate post | 0.401–0.510 | Same bytes; menu opens/closes |

All three windows retain focus on PID 35004 and end with no held byte and no debugger
present. Eight external samples saw the brief positive attachment; the separate
post window saw none. Executable identity and full compared .text bytes match the
EXP-015 reference; full module lists again retain Steam/NVIDIA/Discord overlays.
The original-game capture and sustained responsiveness are live evidence. The
ordering's causal effect remains **unproven until the same-proxy original-order
comparator**, as the proxy and delayed final continuation also affect timing.

## Newly observed protection defect

`positive-api.json` records the pre-attach DebugSetProcessKillOnExit(False) returning
**0, error 6**. The old source's promise that it prevents loss of the debugger from
killing the game is therefore unsupported in this run. The game was not subjected
to a debugger-loss intervention; no actual kill-on-exit behavior is inferred.
All context/continue/detach operations succeeded. The separate contradiction
`ASTRA-CONTRA-KILLONEXIT` routes policy setup verification and claim propagation.
This run does not repair that defect.

## Cleanup and next action

PID 35004 was closed and no reference process remained. Only adapter LUIDLow changed
in one GameSetting.ini (79439 to 78642); its exact backup was restored. `restore.json`
verifies all 26 original save/config hashes match. Runtime ownership is released.

At the first-arm checkpoint, next was a fresh save backup and reference session, same API proxy with the original
continue-then-clear ordering, and the same baseline/post controls. Preserve this
first arm unchanged. No shared instrument change or semantic/parity promotion yet.

## Same-proxy original-order comparator

The separate `control-*` evidence uses fresh PID **19560**, the same Stepping save,
area 227, executable and observed code identity. `control_window.py` retains the
same variant and API proxy, omitting only the early-clear option from the debugger
invocation; filenames are distinct from the first arm. Source hashes are in the
run receipts. The first-arm manifest and its members remain unchanged.

The 65-second baseline had held bytes 49/2, a visibly opening/closing menu, no focus
misses, no debugger and five-second CPU fractions **0.406–0.498** of one core.
The capture then reached one entry/ret-site pair on thread **37136**, with XMM0
**-3.13068414** at both sites. The API receipt places the original clear after the
final continuation. All 311 GetThreadContext, 309 SetThreadContext and 208
ContinueDebugEvent calls succeeded, as did detach. The only reported API failure
was again pre-attach DebugSetProcessKillOnExit(False), result 0/error 6. Successful
API returns alone therefore do not establish a usable post-capture game state.

The game displayed **Not Responding** in `control-positive-menu.jpg`. The positive
window had CPU fractions **0.000–0.284**, 2,645 foreground misses, and no held bytes.
However, **this is not a valid negative input observation**: the Enter helper could
not regain foreground and sent no key-down. It exited with code 3 after about
28.3 seconds; its final key-up was accepted. The wrapper's ten-second child wait
timed out first. `control-positive-run.json` remains **INCOMPLETE**, preserving its
then-live child list. The observer completed separately. No C control or matched
post-capture input window completed, and this failure is not relabeled as success.

A further **65-second read-only** observation (`control-readonly-post-window.json`)
completed with CPU fractions **0.037–0.078**, no debugger samples and no foreground
misses. It sent no input, so neither its empty held array nor regained foreground
demonstrates input recovery. These measurements preserve the liveness difference
without claiming a complete matched behavioral discriminator.

The early-clear candidate has sustained live input evidence in one session; the
same-proxy old-order attempt has a visible hang and failed foreground control.
This supports investigating cleanup ordering, but does not establish causality or
certify a general repair. Overlay/timing variation remains, and the comparator's
required input control is incomplete. Shared hwbp remains unchanged. Next bounded
work is the already-routed kill-on-exit setup defect, followed by a controlled
instrument recovery test before further semantic breakpoint captures.

PID 19560 was closed; `control-process-cleanup.json` confirms no reference process
remained. Only the same GameSetting.ini adapter LUID changed. `control-restore.json`
confirms all **26** save/config files match the fresh pre-session backup. Runtime
ownership is released. No failed receipt or first-arm raw file was overwritten.

Follow-up: [EXP-017](EXP-017-debugger-exit-policy.md) repairs and tests the separate
debugger-exit policy setup. Shared hwbp is subsequently changed for that policy only;
the source snapshots and early-clear variant used here remain unchanged. This
follow-up does not close the incomplete input control or certify cleanup ordering.
