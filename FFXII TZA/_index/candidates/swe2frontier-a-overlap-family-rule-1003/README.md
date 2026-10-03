# A-overlap family rule and the accepted_families() API (SWE2-FRONTIER, 2026-10-03)

*Answers `FABLE-REQ-FRONTIER-A-OVERLAP-FAMILY-RULE-1003` (FABLE's ruling as semantic owner) and
`SWE2DATA-REQ-FRONTIER-ACCEPTED-FAMILIES-API-1003`. SWE2-FRONTIER, Claude stand-in for `calm-lamp`.*

## The rule

"A beats a declaration" means **an A member counts as A**, not that the family is refused. In
`check_dispositions.evaluate()`:
- a family whose **only** defect is that some members are measured as A is **ACCEPTED for its non-A members**;
- the gate **WARNS** that the members file is stale, and names the selector to re-run when the note declares one;
- every other refusal still refuses (bad letter, no note, unreadable or empty or repeating members file, count
  mismatch, non-function members, UC-1 outside an R1 span row, cross-family collision), because each of those is
  tested before the A-overlap test and `continue`s;
- an A member stays in A and is not claimed by the family, so nothing is counted twice. `evaluate()` now also returns
  `a_set`, and the dashboard's `requirements._f` labels an A member of an accepted family A, not with the family's
  letter.

## Before / after (live database, same HEAD)

| | before | after |
|---|---:|---|
| frontier (F) | **8,842** | **2,233** |
| A | 15,896 | 15,896 (unchanged) |
| B / C / D | 2,742 / 7,585 / 0 | 3,224 / 13,712 / 0 |
| families accepted / refused | 288 / 47 | 334 / 1 |
| refused for A-overlap only | 46 | 0 (now 46 warnings) |

The one remaining refusal is a genuine defect: `generated-function-families.md :: NativeAdapter.Gu...` declares 10
members while its file holds 11. `goal_gate.py` reads F from the current dashboard generation's requirement facts, so
its `F=` line moves at the next dashboard build. `check_frontier_shape.py` agrees with the new rule (frontier measured
2,239 = 2,239 per check_dispositions, exit 0; pages moved between the two runs). `check_untouched_runs.py` exit 0.

## accepted_families()

`accepted_families(db, sizes, paths=None, uc1=None)` returns `(declaring doc path, family name, letter,
frozenset(declared members))` for every family `evaluate()` accepts, by the same logic. The members are the declared
set, including any that are now A; the A/B/C accounting uses the non-A part. `--json` omits the key.

## Controls (`check_dispositions.py --self-test`, 26 cases)

- **8**: an A-overlap-only family is accepted for its non-A member, with the stale warning. A = 1, B = 1, explained = 2,
  the A member in `a_set` and not in `claimed_set`, and `accepted_families()` returns the declared pair.
- **8b**: A-overlap plus a count mismatch stays refused ("declared 3"). A = 1, B = 0, no warning.
- **8c**: A-overlap plus a cross-family collision stays refused for the colliding family.
- **13**: `accepted_families()` returns exactly the accepted row, with the full doc path; a refused row is absent.
- `dashboard/test_requirements.py` FAILS 0.
