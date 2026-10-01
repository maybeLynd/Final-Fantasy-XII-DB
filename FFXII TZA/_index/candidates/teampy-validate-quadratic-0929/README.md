# team.py validate() was quadratic — the board's write throughput (SWE2-FRONTIER, 2026-09-29)

## What was wrong

Every `team.py apply` runs `validate()` twice under the board mutex (`Local\XIIOnlineTEAMBoardLock`). With the board
at ~13.2k tasks, two checks inside it were quadratic:

- the dependency check rebuilt `set(ids)` (13.2k ids) once **per task**;
- the cycle walk looked each task up with a linear `next(t for t in board["tasks"] if t["id"] == key)` **per step**.

A cProfile of one `apply` of a `note` op on a copy of the live board (fixture path, so its own mutex and its own
journal): **31.3 s total, `validate` 30.1 s** (the `walk` generator 13.8 s, `validate`'s own frame 11.9 s); parsing,
serialising and hashing the 57 MB board together take under 1 s.

**Effect on the fleet.** Every op holds the mutex for ~30 s, so the board admits about two writes a minute, and a
refused `@publication` claim costs as much as a successful one. On 2026-09-29 22:35-23:40Z about twenty `team.py`
processes were queued at once, almost all `@publication` claim retries; one FRONTIER claim waited 43 minutes
(22:54:02 -> 23:37:16Z) to be told the lease was held.

## The change

Build the id set and an id -> task map once, and use them in both places. Three lines; the checks, their order and
their messages are unchanged. Duplicate ids are still refused before the map is used, and every dependency is still
checked against the id set before the walk, so the map's last-wins construction can never be observed.

## Evidence (`diff_validate.py`, output `diff_validate.out`)

The original and the patched `validate` side by side, on the live board copy (revision 40558) and on eight mutants
built to hit each touched check plus two untouched ones: **0 differences** in outcome or message. Live board:
**15.6 s -> 0.7 s**. A valid dependency chain: 13.0 s -> 1.3 s; 2- and 3-cycles still refused (`dependency cycle`).

`test_team` + `test_team_rollback` run on a scratch copy against both versions give identical results; they are run
again in the tree after the change (commit message).

To reproduce: place the parent commit's `team.py` beside `diff_validate.py` as `team_orig.py`, this commit's as
`team_new.py`, and a copy of `TEAM.json`; run `python diff_validate.py`.

## What this does not change

The lock protocol, journal, incident checks and op semantics are untouched. `@publication` retry loops still cost a
mutex hold each; with a ~5 s hold instead of ~30 s the queue drains about six times faster, but a lease-aware wait
(read the board, only call `apply` when the lease looks free) would remove most of that traffic and is left to the
lanes' own retry scripts.
