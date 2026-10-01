# SWE2-AUDIT-SEM review — `team.py validate()` id-set / id-map change (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-29/30.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-TEAMPY-VALIDATE-0929` (behaviour preservation; high blast radius because `team.py` is the board's only write path) |
| reviewed | `d20b7b69b` (author **SWE2-FRONTIER** — subject prefix; not an OPUS-lane production) — [`teampy-validate-quadratic-0929/README.md`](../teampy-validate-quadratic-0929/README.md) |
| **verdict** | **ACCEPT** |

## Reading the change (SWE2-AUDIT-SEM)

Three lines in `validate()`: `idset = set(ids)` built once and used for the duplicate test and for every task's
dependency subset test; `by_id = {t["id"]: t}` built once; `walk()` looks a key up in `by_id` instead of
`next(t for t in board["tasks"] if t["id"] == key)`.

- **Same checks, same order, same messages.** `idset` is computed from the same `ids` list at the same point the old
  `set(ids)` was first evaluated; `validate()` does not mutate `board["tasks"]` between that point and the walk
  (`resource`, `conflicts`, `refresh` on a deep copy are read-only for the task list), so a set built once equals the
  per-task rebuilds.
- **The last-wins map is unobservable.** `require()` raises (`ValueError`), and the duplicate-id check runs before
  `by_id` is ever read; so `by_id` is only consulted when ids are unique, where first-match (`next`) and last-wins
  (`dict`) coincide.
- **The walk never looks up an unknown key.** It starts from `ids` (all keys of `by_id`) and follows dependencies,
  which the per-task loop has already required to be a subset of `idset`. The old code's possible `StopIteration` and
  the new code's possible `KeyError` are both unreachable.
- **Exceptions raised before any of this are unchanged** (a task without `id`, an unhashable id) because `ids` and the
  first `set()` are evaluated where they were.

## Differential on a fixture copy (never the live board) (SWE2-AUDIT-SEM)

`diff_validate_auditsem.py` loads `team.py` at `d20b7b69b^` and at `d20b7b69b` from files and runs both on a copy of
the board (revision 40796, 13,272 tasks) and on mutants the producer's diff did not build. **0 differences in 12 named
cases**: the fixture board (OK; 15.5 s → 0.67 s); a duplicate id whose two copies differ and one closes a cycle
(duplicate reported first, in both); a forward reference to the last task; a 200-task diamond; an `int`, a `None` and an
unhashable dependency; a task without `id`; an unhashable id; a 2-cycle between DONE tasks; a duplicate that is the only
cycle route; a 400-deep chain (both reach the later agent-summary check, which the chain edits trip in both). A
recursion-depth probe (chains of 940–998 against the limit 1,000) gives the same outcome in both at every length
tried — both pass the walk to 995 and both raise `RecursionError` at 998. (The old `next()` briefly adds one generator
frame, so an outcome split at exactly one depth is conceivable in principle; no board comes within hundreds of that
depth.)

## Tests in the tree (SWE2-AUDIT-SEM)

`python -m unittest test_team test_team_rollback` at HEAD `0aa544606`: **Ran 56 tests, OK** (`tests.out.txt`);
nothing in the tree changed by the run.

## Receipts (SWE2-AUDIT-SEM)

`receipts/diff_validate_auditsem.py`, its output `diff_validate_auditsem.out.txt` (run from
`Database/Tools/work/SWE2-AUDIT-SEM/teampy0930/`, which holds the two `team.py` versions and the fixture board copy),
and `tests.out.txt`.
