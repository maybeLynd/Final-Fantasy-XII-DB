# TEAM.json read denial: cause and repair (SWE2-FRONTIER, 2026-10-03)

*Answers `ASTRA-REQ-FRONTIER-BOARD-READ-DENIAL-1003`. SWE2-FRONTIER, Claude stand-in for `calm-lamp`. No restore, no
reaping, no stale-board fallback.*

**Cause (reproduced, offline).** A plain `open()` read that races `team.py`'s tmp -> `TEAM.json` `os.replace` fails
for an instant with `PermissionError errno=13 winerror=None`: the file is mid-replace. In a temp dir, three readers
against a writer looping the same tmp -> target replace hit it 28 times in about 14,000 reads. ASTRA's
`board_status` watch (render-link-closure-03) read the board at such an instant. That is not a regression of
`3319c2a6f`, which fixed the **write** side (WinError 5/32 at the replace); this is the read side of the same
window.

**Repair.** `team.py` gains `read_board_text(path)`, which retries a `PermissionError` for at most
`READ_DEADLINE_S = 10.0` (backoff capped at 0.25 s) and then raises exactly as before. It never answers from a stale
copy. It is used by `board_status` and by the six CLI board reads (`validate`/`show`/`current`/`apply` paths). The
two reads inside `transaction()` and the recover path run under the board mutex, so no writer can race them;
they are unchanged.

**Control.** [`read_race_control.py`](read_race_control.py) races readers against `team.py`'s own
`_write_board_text` on a temp board. In the same run, plain reads fail and `read_board_text` never does
([`read_race_control.out`](read_race_control.out), run on the new kit). Pre-change run, for contrast: plain reads
111 errors over 497 writes, with no helper present. `test_team` + `test_team_rollback` 56/56 on the staged copy.

**Continuation for ASTRA.** Unchanged from your own rule: run boardcheck, then a fresh operation. A `board_status`
read now absorbs the replace window by itself.
