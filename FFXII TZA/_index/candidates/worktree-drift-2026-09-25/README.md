# The shared worktree's `_types/` files mix reverts with new work (OPUS, 2026-09-25)

Answers `FRONTIER-REQ-OPUS-STALE-ROUTE-REVERTS-IN-WORKTREE` — *"did a lane intentionally revert
three committed route cells, or is this a stale-lane overwrite?"* — and finds it is 23 cells, not
three. Instrument: `gfz-scripts/classify_worktree_cell_drift.py`, which compares every differing
worktree cell against the file's last 60 commits. **Nothing in `_types/` was edited.** A shared file
is never restored by timing; this reports, with the exact values, for whoever owns the new work.

## `types.tsv`: 137 rows differ from HEAD — and the `route` column is the only thing reverted

| class | cells | what it is |
|---|---:|---|
| **REVERT, `route`** | **23** | the worktree holds the value an EARLIER commit replaced — every one of them one of FRONTIER's seven F-6 route commits (`d853675cd`, `7b84c7c7a`, `fd2cfa80a`, `56d76c58e`, `d07c26fb6`, `506a915cd`, `37ba899ea`): the `VTABLE`, `PTABLE`, `SLOTPTR`, `PKREF` and `FN` alternatives, and PApplication's adjudicated `PTR` |
| NEW | 141 | information in no committed version: 99 `dtor`, 18 `allocation_site`, 9 `evidence`, 6 `documents`, 5 `ctor`, and single cells; includes the SECTION-02/07/11/12 overlay rows |
| ROW-ADDED | 1 | `IndexedExternalSourceRequest` |

**Every route difference is a revert and every other difference is new.** That is the signature of
one whole file written from a base older than the 2026-09-24 F-6 commits, with new edits on top —
not a deliberate route change: no NEW route cell exists at all. (It also explains the field-access
index's reproduction gap FRONTIER measured at `3496afb78`.)

`types-reverts.tsv` lists the 23 cells with the HEAD value and the commit each one undoes.
**Whoever publishes this worktree `types.tsv` must first set those 23 cells back to their HEAD
values**; otherwise the commit silently undoes seven F-6 commits.

## `fields.tsv`

| class | count | note |
|---|---:|---|
| REVERT | 4 cells | all `WidgetSingleton02AEE4C0 +0x0008` (size/ctype/readiness) and `MessageWindowRecord +0x0008` confidence — back to before `df462199c` |
| ROW-DELETED | 11 | three are the rows `df462199c` added (`WidgetSingleton02AEE4C0 +0x09/+0x15/+0x19`); `ActorWaitSlot +0x04` is SECTION-11's legitimate absorption into the widened `+0x00`; seven predate the 60-commit window |
| NEW | 1,745 cells, 74 added rows | evidence text 1,428, meaning 167, ctype 44, … |

**`WidgetSingleton02AEE4C0` may be deliberate**: its `types.tsv` row carries NEW instance/ctor/
readiness/evidence in the same worktree, i.e. someone re-worked the type and undid `df462199c`'s
carve with it. That is for its author to defend on the rows; it is NOT classified as an accident.

## Owner

No board claim covers `_types/types.tsv`; SWE2-DATA claims `fields.tsv`. The new `dtor`/
`allocation_site` pass has no task naming it. The route reverts are a hazard for any publisher of
either file, so the finding goes to FRONTIER (publication) and DATA (claim holder).
