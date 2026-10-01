---
experiment: EXP-045
title: observer qualification after checker repair
status: PREPARED - offline controls only
contract: none - Observer dependency qualification under fake memory and time; no native game observation.
evidence_class: offline preparation
method: A - offline instrument preparation
live_game: false
execution_scope: Repaired dependency pin qualified with mocked memory and time; no native process calls.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-045-observer-repaired-dependency/qualify.py
date_designed: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-045: observer qualification after checker repair

**Status:** OFFLINE QUALIFIED; no live game used. ASTRA, 2026-09-11.

[EXP-044](EXP-044-check-verdict.md), commit `bb26093`, repaired runtime check verdicts.
The source change invalidates the dependency receipt of the earlier
[EXP-042 observer](EXP-042-command-source-refresh.md). Its files remain intact.

This [candidate](evidence/EXP-045-observer-repaired-dependency/observe.py) and its
eleven-control test suite are byte-identical to EXP-042. Only the runtime_probe
dependency hash changes. The observer imports process discovery, module base and
read-control constants from that module; it does not execute the repaired `--check`
branch. Its behavior therefore remains the same, with a new explicit source receipt.

[qualify.py](evidence/EXP-045-observer-repaired-dependency/qualify.py) verifies the
single changed pin, exact observer/test equality, the old candidate's rejection of
the current dependency, and the new candidate's receipts before and after tests.
[Qualification](evidence/EXP-045-observer-repaired-dependency/qualification.json),
[raw test output](evidence/EXP-045-observer-repaired-dependency/unit-tests.txt) and
[manifest](evidence/EXP-045-observer-repaired-dependency/manifest.json) retain the result.
Run the qualification script with the repository's existing Windows Python runtime.

The eleven controls cover bounded sampling, health stop, player identity change,
ambiguous/missing observations, invalid duration and empty samples, the sample cap,
exclusive output creation, executable/base/module rejection, changed/short code reads
and dependency rejection. Disk executable bytes are real; process memory and time
are fake. They do not establish native API correctness or original-game behavior.

Use this candidate for the next controlled command-observer run. It still requires
ASTRA's runtime reservation, the intended clean executable and fresh before/after
identity checks. Sampling is limited to five nominal seconds or 100 samples; blocking
reads and qualification remain outside that bound. HP loss stops observation only.
The loaded-state debugger control and handler reachability requests remain unresolved;
game automation remains paused after the physical Escape stop.
