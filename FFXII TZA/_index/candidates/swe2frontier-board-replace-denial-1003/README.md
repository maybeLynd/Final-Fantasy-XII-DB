# TEAM.json replace denial: cause and repair (SWE2-FRONTIER, 2026-10-03)

*Answers `ASTRA-REQ-FRONTIER-ATOMIC-BOARD-WRITE-DENIAL-1003`. SWE2-FRONTIER (Claude stand-in for the Devin session
`calm-lamp`). No board restore, no lock reaping, no journal or compare-and-swap change.*

## Cause

`team.py _write_board_text` writes a temp file and `os.replace`s it onto `TEAM.json`. On Windows that replace is
denied (WinError 5) while **any** process holds `TEAM.json` open without `FILE_SHARE_DELETE` - and Python's `open()`
never passes that flag. The writer already retried WinError 5/32, but only eight times with backoff 25 ms << n:
**about 3.2 s in total**.

At 70 MB a reader holds the file for as long as it reads and, for `json.load(open(...))`, for the whole parse too:
measured 0.56-0.67 s per `json.load(open(p))` and 0.24 s per plain `read()` on this machine. Seven readers in the kit
and the dashboard used the parse-while-open form (list below), several of them on timers or on every board change. On
2026-10-03 from about 01:36Z seven more Claude stand-in sessions joined FABLE, ASTRA, OPUS, the watchdog controller
and the dashboard builder in reading the board. ASTRA's two failures (01:40:34Z and 01:44:12Z) are in that window.
SWE2-FRONTIER's own finish op hit the same denial once at 02:16:30Z.

**Reproduced offline** with [`control_replace.py`](control_replace.py): a thread holds a temporary target open with
plain `open()` for 5 s while the writer replaces it. Old `team.py`: `PermissionError winerror=5 after 3.18s`, target
unchanged, no temp file left - ASTRA's receipts exactly. A 1 s hold succeeds on both.

## Repair (this commit)

1. **`team.py`: the retry is bounded by a deadline, `REPLACE_DEADLINE_S = 30.0`, not by eight attempts.** Backoff is
   capped at 0.25 s so a gap between readers is caught promptly. Still fail-closed: when the deadline passes, the
   PermissionError propagates exactly as before, and the journaled intent stays pending for the next transaction to
   reconcile. Same exception classes (WinError 5/32 only). Control after the change: 5 s and 12 s holds succeed,
   and with the deadline forced to 2 s a 5 s hold fails after 2.14 s with the target unchanged.
2. **Readers release the handle before parsing**: `json.loads(open(p, "rb").read().decode("utf-8"))` in
   `transitions.py` (two sites, through a `_read_board_bytes` helper), `publish_paths.sh` (both board checks),
   `check_propagation.py`, `transfer_audit.py`, and the dashboard's `build_views.py`, `requirements.py` and
   `server.py`. Measured hold 0.02 s instead of 0.56 s; the parsed object is identical (compared on the live board).
   `team.py` itself, `swe2_watchdog.py` and ASTRA's helper already read with `read_text()` / `open().read()` first.

Not changed: the dashboard **server** and the watchdog **controller** are long-running processes and keep the old
code until their owners restart them; the controller reads with `open().read()` already.

## Checks

- `control_replace.py` FAILS 0 on the new kit and FAILS 1 on the old one (5 s hold), run on the worktree at HEAD 5cf0bc196 (the new kit uncommitted, the old kit = HEAD).
- Staged copy, before installing: `test_team` + `test_team_rollback` 56/56 OK; `test_transitions.py` FAILS 0;
  `test_watchdog_scheduler` 16/16 OK. `test_publish_paths.sh` fails identically on the staged and the HEAD script
  (byte-identical output, pre-existing). The dashboard tests need the real database tree; `test_server.py`'s one
  staged failure (S11, a missing DASHBOARD-MEANINGS.md) is identical with the original `server.py` in the same staging.
