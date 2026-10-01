---
experiment: EXP-044
title: typed runtime check verdicts
status: REPRODUCED - checker verdict defect and repair
contract: none - Runtime-checker verdict reproduction and repair under fake process boundaries; not a game operation.
evidence_class: offline tool reproduction
method: A - offline tool reproduction
live_game: false
execution_scope: Old and repaired checker executed with fake process boundaries; historical printed rows reassessed without new captures.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-044-check-verdict/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-044: typed runtime check verdicts

**Result:** the retained checker falsely returned success for numeric substrings,
unreadable-only checks and empty campaigns. The current checker rejects these cases.
This is offline instrument evidence, not a live game observation.

## Question and method

Can `runtime_probe.py --check` report success without the requested numeric value
or even a readable row? Its previous loop searched the formatted observation for
the expected string, counted FAIL but not unreadable ERROR, and accepted zero rows.

[check.py](evidence/EXP-044-check-verdict/check.py) loads each exact source and calls
its actual `main()` with a temporary TSV. Only process enumeration, open, module
base, memory reader and close boundaries are replaced. Fake base/read controls
pass; every case asserts the fake handle closes. No original game is opened,
attached, read or controlled. Controls qualify verdict logic, not native memory IO.

## Evidence and discriminating results

[Before](evidence/EXP-044-check-verdict/before.json) retains all 14 original runs;
[after](evidence/EXP-044-check-verdict/after.json) retains 22 repaired runs, including
their stdout, return values and fake read/close events.

| Input | Retained source | Repaired source |
|---|---|---|
| u32 expect 81, observe 181 | PASS / exit 0 | FAIL / exit 1 |
| i32 expect 81, observe -81 | PASS / exit 0 | FAIL / exit 1 |
| f32 expect 1, observe 1.5 | PASS / exit 0 | FAIL / exit 1 |
| Unreadable, literal or wildcard | ERROR / exit 0 | ERROR / exit 1 |
| Header with no rows | exit 0 | ERROR / exit 1 |
| Exact values for each of six types | Positive controls retained | exit 0 |

Additional repaired controls reject short reads, unknown kinds, blank expectations,
out-of-range integers, nonfinite float expectations, truncated/extra TSV columns
and multiple unreadable rows. Hex expectations compare numerically regardless of
zero padding. Integer expectations must fit the declared signed/unsigned width.
Float expectations round to binary32 and compare numerically without a tolerance;
signed zero compares equal. A wildcard accepts any complete readable value,
including a nonfinite float, and makes no semantic assertion.

The repair changes only the check path and its helper/import. The type dump, process
selection, base/read controls and other command paths retain their existing scope.
Malformed TSV structure exits 2; row failures/errors and zero rows exit 1.

## Historical consequences and limits

[assessment.json](evidence/EXP-044-check-verdict/assessment.json) records hashes for
all four retained EXP-001 captures and checks their printed C1/E8 literal rows using
numeric equality. Those displayed verdicts agree: C1 matches and E8 differs from 81.
No raw capture was changed. This bounded assessment does not retroactively establish
instrument identity, resolved pointer receipts or the initialization state. EXP-001's
current E8 is observational after the separate initialization correction in bb3d1de.
Its other wildcard PASS rows establish readability only; interpreting them needs the
companion experiment's state and relational checks.

The EXP-042 observer pins the old runtime_probe hash. This repair intentionally
makes that candidate reject the current dependency. A new explicitly qualified
candidate is needed before its next use; old source receipts are not rewritten.
No claim here promotes loaded-game debugger controls or pending handler reachability.

## Reproduction and provenance

Run from the checkout root with the existing Windows Python runtime:

```powershell
$e = 'Database/FFXII TZA/_experiments/evidence/EXP-044-check-verdict'
& '.\Collaboration\Tools\analysis\venv\Scripts\python.exe' "$e/check.py" "$e/runtime-probe-before.py" before
& '.\Collaboration\Tools\analysis\venv\Scripts\python.exe' "$e/check.py" "$e/runtime-probe-after.py" after
```

Exact before/after sources and fixture outputs are sealed by
[manifest.json](evidence/EXP-044-check-verdict/manifest.json). Expected cases are
embedded in the retained harness. Offline fixtures cannot validate Windows API
prototypes, process identity or game semantics. ASTRA, 2026-09-11.
