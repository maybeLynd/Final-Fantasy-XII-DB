---
experiment: EXP-029
title: Requested stopped-event cleanup at a debugger deadline
status: VALIDATED — disposable-process control only; reference-game timeout remains unvalidated
date_designed: 2026-09-11
method: C - ordinary UI input and read-only process observation
live_game: false
contract: none - debugger instrument validation on disposable processes. It tests whether a requested stop can provide a cleanup boundary; the reference game was not its subject.
---

> **`live_game` corrected to `false`, 2026-09-20 (OPUS)**, on `ASTRA-CONTRA-OPUS-EXP030-LIVE-METADATA`. This record's own scope is disposable targets only; the flag was set `true` in bulk by `0a721490b` alongside `method: C`. `live_game` is an evidence class - `check_tier_inflation` reads it as a live-evidence marker and `check_experiment_schema` counts contracts named by a record carrying it - so a true label here would inflate original-game support with a run that never opened the game.

# EXP-029 — deadline cleanup before continuation

EXP-018 validated clearing hardware breakpoint registers at the final two-hit
event. Its timeout path still clears after continuing the target. This private
candidate tests whether a requested debugger stop can provide a stopped cleanup
boundary after a duration-limited capture. Shared hwbp.py is unchanged.

The predicted distinguishing observation is a requested breakpoint event followed
by successful thread-register clear/readback while stopped, then successful
continuation/detach and advancing target heartbeats. A request failure, missing
event, failed clear/readback or failed continuation cannot yield PASS. Fixtures
test those boundaries before any process experiment.

The candidate requires successful attachment, disabled kill-on-debugger-exit and
a serviced initial attach breakpoint. It calls DebugBreakProcess, services the
subsequent CREATE_THREAD event, waits for a breakpoint on a newly observed thread,
clears all enumerated threads, reads DR0–DR3/DR7 back as zero, continues that event
and returns an explicit verdict. DR6 reserved bits are not required to read as
zero. The caller checks detach and target liveness separately. This is a deliberate
debugger intervention, including a remote thread, not a passive observation.
[Microsoft documents](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-debugbreakprocess)
that the call raises a breakpoint and can terminate an undebugged process; the
prepared-attachment precondition is essential.

## Disposable controls

[run.py](evidence/EXP-029-timeout-cleanup/run.py) creates and owns each Python child.
The child allocates two RET bytes and executes the first every 50 ms while appending
a heartbeat. The cold arm breaks on the unused second byte; the positive arm breaks
on the executed first byte. Each capture lasts about two seconds before requested
cleanup. The context helpers are the exact EXP-018 snapshot with SHA256
81a8510288dc5a4e1d93c221659c49926039e66aa277da3f1fea59aa193879f6.

| Control | PID | Hits | Threads cleared/read back | Post-detach heartbeat sizes |
|---|---:|---:|---:|---|
| Cold | 7672 | 0 | 5/5 | 43, 48, 54, 60 |
| Executed RET | 38236 | 40 | 5/5 | 41, 47, 53, 59 |

Both had successful attach/policy, arming, context operations, requested break,
continuation and detach, with no recorded API failures. All context operations
occurred between a received event and its continuation. Four post-detach samples
spanning about 0.9 seconds show the children alive and debugger absent, with three
advancing heartbeat intervals. The owned children were then terminated explicitly.
No FFXII process or save was opened, and no runtime reservation was needed.

The first attempt is retained in the `cold` directory as INCOMPLETE: the Windows
venv executable redirected to a different PID, so the PID equality guard aborted
before opening or attaching. Its original runner is preserved as run-failed.py.
The corrected runner uses the base interpreter directly and checks PID equality.
The failed Popen child was closed; its reported target PID34920 was absent on the
subsequent process inventory. This failure supplies no debugger evidence.

## Boundaries and next step

These are two disposable-process runs, not original-game validation or a general
debugger safety guarantee. The helper's newly-created-thread breakpoint association
is adequate for these controlled children but is not a unique remote-break identity
proof in an arbitrary process with concurrent thread creation or software breaks.
It does not restore pre-attachment register contents, certify all-thread enumeration,
repair failed cleanup, or validate the old after-continue fallback. API readback and
short heartbeat survival do not establish long-term game input responsiveness.

Before reference-game use, integrate a private duration-only candidate with explicit
attach-ready gating, event errors and invalid cleanup propagation; resolve or bound
the requested-break association and test that exact candidate. Then reserve runtime
for matched loaded-state code/input/liveness controls. Handler reachability still
requires a real combat death and its separate positive control.

Raw API receipts, result files, source hashes and fixture output are listed in the
[manifest](evidence/EXP-029-timeout-cleanup/manifest.json).
[seal.py](evidence/EXP-029-timeout-cleanup/seal.py) checks the saved ordering and
identities; [validation.json](evidence/EXP-029-timeout-cleanup/validation.json)
records the bounded verdict and interpreter identity.
