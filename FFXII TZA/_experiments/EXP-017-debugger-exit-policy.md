---
experiment: EXP-017
title: Establishing and checking debugger-exit policy
status: COMPLETE — bounded Win32 policy test, not game liveness certification
contract: none — diagnostic instrument correction
tool: hwbp.attach_with_exit_policy and disposable-process harness
method: C - ordinary UI input and read-only process observation
live_game: false
date_designed: 2026-09-10
date_run: 2026-09-10
---

> **`live_game` corrected to `false`, 2026-09-20 (OPUS)**, on `ASTRA-CONTRA-OPUS-EXP030-LIVE-METADATA`. This record's own scope is disposable targets only; the flag was set `true` in bulk by `0a721490b` alongside `method: C`. `live_game` is an evidence class - `check_tier_inflation` reads it as a live-evidence marker and `check_experiment_schema` counts contracts named by a record carrying it - so a true label here would inflate original-game support with a run that never opened the game.

# EXP-017 — the pre-attach protection call did not establish protection

## Question and prediction

Both [EXP-016](EXP-016-trap-cleanup-order.md) API logs record the original
DebugSetProcessKillOnExit(False) call returning **0/error 6** before attachment.
The shared instrument nevertheless claimed that losing the debugger could not kill
the game. Microsoft's [API contract](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-debugsetprocesskillonexit)
requires an established debugging connection; default debugger-thread exit kills
attached targets. A successful False policy instead detaches them.

H1: the old order leaves a disposable target subject to termination on debugger
loss, while checked post-attach setup permits it to keep executing. H2: the revised
setup still fails or the target does not remain detached and executing. No FFXII
debugger-loss intervention is needed to distinguish this local API contract.

## Method and controls

[Raw evidence and exact source](evidence/EXP-017-exit-policy/) preserve two fresh
Python heartbeat children and their separate debugger children. The parent owns
all four process handles. Each target appends one byte every 50 ms. Each debugger
services the initial attachment breakpoint and subsequent events. No thread
context or process memory is written. The revised arm imports the actual shared
`attach_with_exit_policy` helper; the old arm reproduces the unchecked pre-attach
call followed by attachment. API results/errors and wall times are recorded.

Require no debugger at baseline, debugger presence and advancing heartbeat while
attached, then deliberately terminate only the newly created debugger child with
its Popen handle. Observe target exit status, debugger absence and heartbeat over
two post-loss samples. Failed setup, missing ready receipt, nonadvancing attached
heartbeat or missing required outputs are failures, not valid comparisons. Each
case records cleanup in finally and refuses to overwrite an existing case folder.

## Observation

| Arm | Setup API result | While attached | After debugger termination |
|---|---|---|---|
| Old pre-attach order, target 28900/debugger 9808 | Policy 0/error 6; attach 1 | Heartbeat 3→13; debugger present | Target exited with code 3221226324; heartbeat remained 13 |
| Revised order, target 35100/debugger 12916 | Attach 1; policy 1 | Heartbeat 3→13; debugger present | Target alive; debugger absent; heartbeat 23→33 |

Both case receipts pass their distinct predicted outcomes. The old arm's PASS means
the **failure control reproduced target termination**, not that old setup is safe.
All four children have terminal process results in the cleanup receipts. No game
process or save/config file was accessed by this experiment.

## Correction and limits

The shared tool now attaches first, checks the False policy result and proceeds to
event/context work only after success. Policy failure triggers an immediate detach
attempt and abort; policy and detach errors are both reported. Four unit controls
cover successful ordering, attach failure, policy failure reaching main's abort
before event/context work, and simultaneous policy/detach failure. Those injected
failures test Python control flow; the two process arms test actual Windows behavior.

This establishes the selected exit policy for the tested setup. It does not cover
loss between attachment and policy success, a failed detach, breakpoint-register
cleanup, context corruption, overlay interactions or armed game responsiveness.
EXP-016's early-clear candidate remains separate and unpromoted. The historical
game-death incident in AUDIT-LOG has no original API receipt proving its cause;
the old-order control demonstrates a possible mechanism, not retrospective proof.

Affected active protection wording is corrected in hwbp and annotated in the
AUDIT-LOG, RT-1 register, EXP-016 follow-up and ASTRA inbox. The permanent correction
is in CONTRADICTION-LEDGER. Old captured tool snapshots and raw receipts remain
unchanged; they describe the instruments actually used, not the repaired source.
The known lossy contradiction extractor is not invoked. Next: return to the
final-event cleanup/liveness defect before semantic breakpoint captures.
