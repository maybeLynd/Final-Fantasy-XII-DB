---
experiment: EXP-042
title: command observer source qualification refresh
status: PREPARED - offline controls only
contract: none - Observer source-pin refresh and mocked controls; no new game-behavior observation.
evidence_class: offline preparation
method: A - offline instrument preparation
live_game: false
execution_scope: Dependency hash refresh and mocked observer controls; no game process.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-042-command-source-refresh/test_observe.py
date_designed: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-042: command observer source qualification refresh

**Status:** OFFLINE PREPARATION, eleven controls passed; no live game used.
**Owner:** ASTRA. **Date:** 2026-09-11.

[EXP-041](EXP-041-config-pointer-closure.md), commit `ce1a28d`, corrected the runtime probe's
GameSettingConfig usage example without changing its implementation. The source hash changed,
so [EXP-037](EXP-037-command-observer.md) correctly refuses that dependency. Its original source,
manifest and test receipts remain untouched.

This explicitly versioned [observer](evidence/EXP-042-command-source-refresh/observe.py) and
[test suite](evidence/EXP-042-command-source-refresh/test_observe.py) are byte-identical to EXP-037
at `c16fa6a`. The only dependency change is the runtime probe hash, recorded with its prior value
in [refresh.json](evidence/EXP-042-command-source-refresh/refresh.json). All other dependency pins
are unchanged. The eleven offline controls passed again against the corrected source, including
dependency rejection, executable/live-text checks using fake memory, HP-stop and identity boundaries,
bounded sample count, invalid-duration failure receipts and exclusive output creation.
[Raw output](evidence/EXP-042-command-source-refresh/unit-tests.txt) and the
[manifest](evidence/EXP-042-command-source-refresh/manifest.json) identify this preparation.

For future controlled runs use this candidate's `observe.py`, with the same CLI arguments as
EXP-037. It still requires ASTRA's active runtime reservation and fresh reference identity checks.
The nominal sampling limit remains five seconds/100 samples; blocking reads and qualification work
are outside that duration bound. HP loss stops the observer, not combat. Original-game responsiveness,
command transitions and semantic interpretations remain unvalidated. UI automation remains paused.
