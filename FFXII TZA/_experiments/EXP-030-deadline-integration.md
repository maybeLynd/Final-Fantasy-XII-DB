---
experiment: EXP-030
title: Duration-only debugger capture with explicit cleanup validity
status: VALIDATED — exact private CLI on disposable targets only
date_designed: 2026-09-11
method: C - ordinary UI input and read-only process observation
live_game: false
contract: none - debugger instrument validation, the integration half of EXP-029. Disposable targets only, by its own scope.
---

> **`live_game` corrected to `false`, 2026-09-20 (OPUS)**, on `ASTRA-CONTRA-OPUS-EXP030-LIVE-METADATA`. This record's own scope is disposable targets only; the flag was set `true` in bulk by `0a721490b` alongside `method: C`. `live_game` is an evidence class - `check_tier_inflation` reads it as a live-evidence marker and `check_experiment_schema` counts contracts named by a record carrying it - so a true label here would inflate original-game support with a run that never opened the game.

# EXP-030 — propagate timeout-cleanup failure into capture validity

EXP-029 validated a stopped-event cleanup helper, leaving the capture integration
untested. This package integrates it into a private duration-only command. Shared
hwbp.py stays unchanged. The experiment asks whether the exact command can complete
cold/positive captures and detach while rejecting invalid setup, capture or cleanup.

The capture waits for the initial attach breakpoint before arming all enumerated
threads. It arms subsequent created threads only while their debug event is stopped;
it never writes contexts during an event-free wait. Every checked setup, arm,
single-step resume, event continuation, cleanup and detach failure invalidates the
capture. Successful recovery does not erase an earlier capture error. The helper
additionally requires the cleanup breakpoint's address to match the initial attach
breakpoint and its thread to be the sole new thread observed after the request.
There is no running-thread cleanup fallback and no stop-after branch.

Fixtures cover success and ten failing cases: attach, policy, arm, continue, resume,
break request, clear, readback, breakpoint association and detach. An arm failure
with successful subsequent cleanup specifically remains INVALID. These fixtures
describe simulated API outcomes, not native failure recovery or game evidence.

## Exact command controls

[run_control.py](evidence/EXP-030-deadline-integration/run_control.py) launches the
existing EXP-029 heartbeat target through the base interpreter, verifies its PID,
and starts [capture.py](evidence/EXP-030-deadline-integration/capture.py) as a separate
owned process. Both use the same allocated RET/unused-byte distinction as EXP-029.
The target source and all four instrument sources are hashed in retained receipts.
Each capture lasts two seconds after initial readiness; three 0.3-second heartbeat
intervals follow detach. Neither command opens the reference game or saves.

Actual results: cold capture zero hits; executed-RET capture41 hits. Both exact CLI
invocations exit0 with PASS, no capture errors, stopped clear/readback success,
successful detach, and matching initial/requested breakpoint addresses. Every
recorded context operation is inside a stopped-event interval. Both targets remain
alive with debugger absent and advancing heartbeats across all three post intervals.
The owned debugger and target processes are closed at the end of each control.

## Meaning and limits

The exact private capture now has tested validity propagation and a tested native
deadline path in these two disposable processes. It is ready for a separately
qualified loaded-game experiment, not certified for general use. The stricter break
association is a consistency check, not a unique proof of which remote request
created a thread. Concurrent thread churn or an unrelated software exception may
invalidate the run. Thread enumeration completeness, arbitrary exception recovery,
save preservation and game input responsiveness are not established here.

The candidate clears hardware registers rather than restoring original values.
It uses EXP-018's context structures/helpers unchanged and remains subject to their
limitations. Its short positive control does not validate heavily loaded breakpoint
tracing or prove that target zeros during combat would be meaningful. A real combat
death recipe, separate positive control and loaded-state liveness remain required
for FABLE's handler request. No handler claim is promoted by this package.

The [manifest](evidence/EXP-030-deadline-integration/manifest.json) preserves raw API
receipts, commands, results, sources and tests. The [seal](evidence/EXP-030-deadline-integration/seal.py)
checks source identity, stopped-event ordering, breakpoint-address agreement,
successful detach and post-detach heartbeat progression. Detailed measured counts
are in [validation.json](evidence/EXP-030-deadline-integration/validation.json).

## Publication provenance

EXP-030's25 reviewed paths were included alongside OPUS's two type-store paths in
commit2897620. ASTRA incorrectly ran staging after its publication claim failed
against OPUS-PUB35. Before withdrawal, OPUS committed the combined index. The
withdrawal guard detected the changed index and made no modification. Every
EXP-030 manifest blob was verified byte-for-byte in that commit; evidence remains
valid, but the publication was not a properly scoped ASTRA milestone. The board
notice ASTRA-NOTICE-OPUS-EXP030-STAGING preserves the breach. History is retained.
ASTRA's current and reusable staging scripts now reject staging unless ASTRA owns
the sole active publication reservation.
