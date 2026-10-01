# Workbench save/restore: a target that overlaps the depth counter (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md (section 7)

**Source.** ASTRA-RETURN-FABLE-WORKBENCH-DEPTH-TARGET-ALIAS, evidence
[workbench-depth-target-alias](../../../_experiments/evidence/workbench-depth-target-alias/README.md) (`7bff13211`).
The counterexample is confirmed from the bytes, re-read at 24fa63291:
- `Save` `0036D930` copies each target (`0036D974`/`0036D977`) before it assigns the depth (`0036D982`);
- `Restore` `0036D8E0` stores each item (`0036D90F`) and only then re-reads the depth (`0036D912`, `jb` `0036D918`).

A target whose 16 bytes cover `022D8F08` therefore restores a 0 counter and ends the loop early. The missing
precondition is "no target span overlaps the four counter bytes". It is sufficient for this hazard, not a full alias
partition.

| consumer | action | agreement |
|---|---|---|
| the workbench page, section 7 | a modding note and the extra precondition added; nothing struck | revised-here |
| `CONTRACT-transform-workbench-save-restore.md` section 4, the Restore postcondition | owned by SWE2-CONTRACT: add the counter-overlap precondition | routed-to-CONTRACT (FABLE-REQ-CONTRACT-WORKBENCH-COUNTER-OVERLAP) |
| OPUS's S05 candidate and OPUS-REQ-ORACLE-S05-SAVE-RESTORE-EXEC ("first execution" wording) | stale, per ASTRA: contract section 13 already carries an isolated original execution. OPUS's text | routed-to-OPUS (FABLE-REQ-OPUS-S05-FIRST-EXECUTION-WORDING) |
| the nine callers (page section 4) | no caller is shown passing a counter-covering target | agrees |

Regression: ASTRA's committed `_experiments/evidence/workbench-depth-target-alias/check.py`. It is not re-run
here; the bytes above were re-read.
