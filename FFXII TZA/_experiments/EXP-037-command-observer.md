---
experiment: EXP-037
title: qualified short command/target observer preparation
status: PREPARED - offline controls only
contract: none - Observer preparation with mocked process memory and time; no game-behavior contract observation.
evidence_class: offline preparation
method: A - offline instrument preparation
live_game: false
execution_scope: Mocked observer and component controls; prepared game observer not used live.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-037-command-observer/test_observe.py
date_designed: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-037: qualified short command/target observer preparation

**Status:** OFFLINE PREPARATION. No original-game process was opened, driven or sampled for this package.
**Owner:** ASTRA. **Date:** 2026-09-11. Runtime remains paused after the physical Escape stop in
[EXP-031](EXP-031-loaded-deadline-control.md), pending the user's unanswered resumption preference.

## Question and method

[EXP-027](EXP-027-ordinary-kill-control.md) did not record committed command state, so its stalled
attack observation cannot distinguish cancellation from a retained target or execution delay.
[EXP-035](EXP-035-command-target-binding.md) prepared the command/resolver/census composition.
This package makes that composition callable in a short, qualified read-only observation window.
It adds no interpretation of cancellation, death, action execution or actor lifetime.

The [observer](evidence/EXP-037-command-observer/observe.py) requires ASTRA's active `@runtime`
reservation, the sole intended PID at the designated Steam reference path, certified executable
SHA-256, base `0x120000`, the existing runtime module classification and nonempty module inventory,
the known read control, and exact live/disk `.text` equality against the certified 7,996,981-byte
section. It repeats executable/module/live-code qualification after sampling. These checks do not
prove the absence of all instrumentation or transient modifications between checks.

The CLI retains source hashes before and after. [Dependencies](evidence/EXP-037-command-observer/dependencies.json)
pin EXP-035, EXP-032, EXP-034 and EXP-024 readers plus their local import dependencies. Imports
remain deferred until capture execution. EXP-024 imports input helpers, but this observer invokes
only its read-only Reader; there are no input, process-write or debugger actions in this CLI.

The window accepts `(0,5]` seconds and at most 100 samples, separated by up to 50 ms. This bounds
sampling demand, not the duration of blocking OS reads or the full pre/post qualification work.
EXP-035 scans its filtered census internally; output retains only the selected player and resolved
target rows plus raw command/identity data. Each sample retains frame boundaries and ambiguity.
A stable slot alone is insufficient: player unit/actor identity must also persist across samples.

Unreadable/missing HP, identity changes, ambiguity, exceptions and zero samples yield `INVALID`.
Player HP below the requested positive floor or below the first sample's HP yields `HEALTH_STOP`
immediately after that sample. This stops observation, not the game or combat; a runtime operator
must still perform cleanup. `OBSERVED` means the qualified bounded read window completed; it is
not a semantic PASS. Only `OBSERVED` exits zero; other recorded statuses exit 3. The output file is
created exclusively to preserve earlier evidence.

## Controls and actual results

[Tests](evidence/EXP-037-command-observer/test_observe.py) use fake time, selected-player fixtures
and fake process memory. Qualification's positive control reads the certified executable from disk
and serves its actual section bytes through that fake reader. It is not a live memory observation.
[Raw output](evidence/EXP-037-command-observer/unit-tests.txt): eleven tests passed.

- Positive bounded capture retains the exact selected observation; a stalled clock still caps at 100.
- HP decrease, low initial HP and within-sample HP decrease stop immediately.
- Cross-sample player replacement, ambiguous selection, absent player, missing HP and read/iterator
  failure return `INVALID`, retaining collected samples.
- Invalid/nonfinite duration and zero collected samples cannot report observation success.
- Wrong executable bytes, base, module verdict or empty inventory fail qualification.
- Wrong control, empty live text and a changed live text byte fail qualification.
- Pinned dependency changes are rejected.
- The CLI records an invalid-duration failure without OS imports and refuses to overwrite the receipt.

The seven EXP-035 composition tests also passed again, recorded in
[component output](evidence/EXP-037-command-observer/component-tests.txt).
The command/target decoding itself remains covered by EXP-035's original component fixtures;
these new controls exercise the wrapper boundaries rather than claiming new native behavior.
The sealed [manifest](evidence/EXP-037-command-observer/manifest.json) identifies this package.

## Next live discriminator and limits

After UI resumption, preserve saves, reserve runtime, establish the known named loaded state and
perform a short no-command baseline before the existing bounded attack recipe. Example, with a
fresh verified PID and new output path:

```powershell
python "Database/FFXII TZA/_experiments/evidence/EXP-037-command-observer/observe.py" --pid <PID> --seconds 3 --slot 0 --minimum-hp 35 --out <new-output.json>
```

Compare live/shadow command bytes, context sentinel, action ID, phase and resolver result through
the visible command transition. A retained target alone cannot establish active execution. A
nonzero resolved unit outside the filtered census is not proof of death. Equal before/after reads
do not establish atomicity, exclude ABA reuse, or explain writers. Health and identity failure
receipts must not be relabeled as a successful full window. Live validation and the separate
loaded armed-deadline control remain outstanding; no database semantic claim is promoted here.
