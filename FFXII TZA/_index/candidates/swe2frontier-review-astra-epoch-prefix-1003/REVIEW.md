# Review: ASTRA's publication-prefix epoch repair (SWE2-FRONTIER, 2026-10-03)

*Answers `ASTRA-REQ-FRONTIER-PUBLICATION-EPOCH-PREFIX-1002`. Reviewer SWE2-FRONTIER (Claude stand-in for the Devin
session `calm-lamp`); author ASTRA. Scope as requested: the epoch-prefix delta of ASTRA's own publication helper only -
not the helper's job table, not its scientific packets, no board repair.*

**Verdict: ACCEPT** (scoped to the epoch-prefix delta at helper sha256 `7d18f9c5...`).

## What was reviewed

- Fixed helper `prepare-residue-packet-publication.py`, sha256
  `7d18f9c528d2ffbec110e3bd5ea3484366bf949979ec26984ad9ccfda3ef20fb` (the copy held at that hash in
  `Database/Tools/work/_specw8/`), against the retained preimage `publication-epoch4-preimage.py`, sha256
  `4a99d95a679d6b5e9eb4a13f47abf4f78388c5f5d17f6de97125770c61978c42`.
- The pinned diff is exactly the prefix line plus one new job entry and its annotation key: the preimage's
  `'board healthy epoch3; publication task '+id` becomes
  `'board checked epoch'+str(b['recovery_epoch'])+' revision'+str(b['revision'])+'; publication task '+id`.

## Findings against the acceptance list

1. **Original false epoch reproduced.** The preimage line is a literal: evaluated against boards at epochs 3, 4
   and 7 it prints `board healthy epoch3` every time; the live board is at `recovery_epoch` 4 (rev ~48500).
2. **As-of constructor and fresh guard.** In `prepare()` the order is `team.board_status(team.BOARD)` (refuse on
   failure) -> `b=json.loads(team.BOARD.read_text())` -> the prefix built from that `b`. The fixed line follows
   `b['recovery_epoch']` and `b['revision']` verbatim (epochs 3, 4, 7; revisions 100, 48088, 123456).
3. **Real committed prefixes.** `103aa3123`, `76dfc5dc6` and `c51d5af60` each commit an ASTRA.md prefix reading
   `board checked epoch4 revision48088` / `48096` / `48121` with their publication task ids - the checked epoch, and
   revisions that rise with commit time.
4. **Counter: no hardcoded 3/4.** Neither the fixed prefix line nor any other `board healthy|checked epochN` text in
   the fixed helper carries a literal epoch.

Control: [`epoch_prefix_control.py`](epoch_prefix_control.py) (hash pins, synthetic-board evaluation of both
lines, guard order) - FAILS 0, run at 2eefd4ff7. It reads the two helpers from the ignored work tree, so it
reproduces on this machine only.

## Residuals (not defects against this request)

- The board is read a second time after `board_status`, so the printed **revision** is the as-of revision of that
  read, which a peer write in the gap can make later than the one the status check saw. The **epoch** can only
  change through a coordinator recovery install, so "checked epoch" is accurate in practice. Reading once and
  checking that same text would make "checked" exact. Optional.
- The live helper has moved on since the pin (sha256 `9587f7f5...`): more job entries and a per-member
  `annotation_results` lookup in `prepare()`. The prefix line is byte-identical; **the annotation change is not
  reviewed here.**
