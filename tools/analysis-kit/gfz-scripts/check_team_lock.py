#!/usr/bin/env python3
"""check_team_lock.py - controls for `team.py`'s board lock.

WHY THIS FILE EXISTS. `locked()` used to `raise` the instant it found a LIVE holder - no wait, no
retry. A peer holds that lock for the length of one JSON rewrite, so losing the race was normal,
and the failure downstream of it is much worse than it looks:

* **2026-09-13**, recorded in `publish_paths.sh`'s own header: an `add` died on a transient lock,
  its output was discarded, the six following claim retries all reported *"unknown task"*, and by
  then nobody held `@publication`, so the guard let the batch through as an unidentified publisher.
* **2026-09-18**, same shape: an `add` lost the race inside an `&&` chain, **forty** subsequent
  claim attempts reported *"unknown task"*, and diagnosing it cost a round - because the message
  names the TASK, while the fault was the LOCK two steps earlier.

Both incidents are the same bug wearing the error text of a different one. Waiting a fraction of a
second is always right here and failing on sight is never right, so `locked()` now waits out a
live holder up to `LOCK_WAIT_SECONDS`.

The two behaviours that must NOT change are controlled below as well: a **dead** holder is still
reaped at once (respecting it would wedge the board forever), and a holder still alive after the
wait still **raises** - at that point it is a wedged process, and silently reaping it would be the
dangerous choice.

    python check_team_lock.py

Runs against a temporary file, never the real board.
"""
import json
import os
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import team

TMP = Path(os.environ["TEMP"]) / "team_lock_control.json"
LOCK = TMP.with_suffix(".lock")
TMP.write_text("{}", encoding="utf-8")
for p in (LOCK,):
    if p.exists():
        p.unlink()

ok = True

# 1. Plain acquisition works.
with team.locked(TMP):
    pass
print("  plain acquire/release                                  ok")

# 2. A DEAD holder is reaped. pid 1 with a mismatched start stamp reads as dead/recycled.
LOCK.write_text(json.dumps({"pid": 999999, "at": "x", "started": 1}), encoding="utf-8")
t0 = time.time()
try:
    with team.locked(TMP):
        pass
    dead_ok = True
except Exception as e:
    dead_ok = False
    print("      raised:", e)
ok = ok and dead_ok
print("  a DEAD holder is still reaped (%.2fs)                  %s"
      % (time.time() - t0, "ok" if dead_ok else "BROKEN"))

# 3. A LIVE holder is WAITED OUT rather than raised on. Hold it from another thread and
#    release after 1s; the old code raised instantly, so a pass here IS the fix.
LOCK.write_text(json.dumps({"pid": os.getpid(), "at": "x",
                            "started": team._proc_start(os.getpid())}), encoding="utf-8")


def release_soon():
    time.sleep(1.0)
    try:
        LOCK.unlink()
    except FileNotFoundError:
        pass


threading.Thread(target=release_soon, daemon=True).start()
t0 = time.time()
try:
    with team.locked(TMP):
        waited = time.time() - t0
    live_ok = waited >= 0.9
except Exception as e:
    live_ok = False
    waited = time.time() - t0
    print("      raised after %.2fs: %s" % (waited, e))
ok = ok and live_ok
print("  a LIVE holder is WAITED OUT, not raised on (%.2fs)     %s"
      % (waited, "ok" if live_ok else "BROKEN"))

# 4. A holder that never releases still raises, with a message naming the wait and the holder.
team.LOCK_WAIT_SECONDS = 1.0
LOCK.write_text(json.dumps({"pid": os.getpid(), "at": "x",
                            "started": team._proc_start(os.getpid())}), encoding="utf-8")
t0 = time.time()
try:
    with team.locked(TMP):
        pass
    wedged_ok = False
    msg = "(no exception)"
except FileExistsError as e:
    msg = str(e)
    wedged_ok = "wedged holder" in msg and "LIVE" in msg
ok = ok and wedged_ok
print("  a WEDGED holder still raises, and says so (%.2fs)      %s"
      % (time.time() - t0, "ok" if wedged_ok else "BROKEN  " + msg[:70]))

try:
    LOCK.unlink()
except FileNotFoundError:
    pass
TMP.unlink()
print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
sys.exit(0 if ok else 2)
