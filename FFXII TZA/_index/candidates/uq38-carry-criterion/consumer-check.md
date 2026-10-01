# Affected-consumer check: UQ-38's proposed criterion retired (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md (the UQ-38 box)
run: uq38_carry.py and uq38_example.py at 2155a7bf3, FAILS 0 for the example (E2 control); the carry table is a measurement.

| consumer | what it said | state |
|---|---|---|
| _index/OPEN-QUESTIONS.md UQ-38 | "What the question needs is ... whether x64 registers carry values ACROSS bank stores" | revised-here: the criterion is measured and fails its premise; PARTIAL stays, scoped to the PS2 executable like UQ-36/39 |
| `the-ee-and-vu0-register-bank.md`, UQ-38 box | the same criterion as the next step | revised-here: narrowing note under the box (criterion retired, bracket stands) |
| `members/ee-register-members.tsv`, `ee-member-calls.tsv` | the two instruments' classes | agree; used as the calibration sets |

Regenerated with it: nothing.
