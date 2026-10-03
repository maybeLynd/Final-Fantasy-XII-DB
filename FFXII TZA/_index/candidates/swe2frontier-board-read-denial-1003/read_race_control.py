"""read_race_control.py (SWE2-FRONTIER, 2026-10-03, ASTRA-REQ-FRONTIER-BOARD-READ-DENIAL-1003) TEAMPY [MB] [SECS] - readers race team.py's own _write_board_text on a temp board.
Counts read PermissionErrors for plain Path.read_text and for team.read_board_text (when the module has it).
Temp dir only. Exit 1 if the helper exists and failed, or if plain reads never failed (the race was not exercised)."""
import importlib.util, os, sys, tempfile, threading, time, collections
from pathlib import Path
spec = importlib.util.spec_from_file_location("team_ut", sys.argv[1]); team = importlib.util.module_from_spec(spec)
spec.loader.exec_module(team)
mb = float(sys.argv[2]) if len(sys.argv) > 2 else 2
secs = float(sys.argv[3]) if len(sys.argv) > 3 else 20
d = Path(tempfile.mkdtemp(prefix="frontier-readctl-")); target = d / "TEAM.json"
text = "x" * int(mb * 1024 * 1024) + "\n"; target.write_text(text, encoding="utf-8")
stop = time.monotonic() + secs
n = collections.Counter(); err = collections.Counter()
def writer():
    while time.monotonic() < stop:
        try:
            team._write_board_text(target, text); n["write"] += 1
        except PermissionError:
            n["write-fail"] += 1
def reader(kind):
    while time.monotonic() < stop:
        try:
            (target.read_text(encoding="utf-8") if kind == "plain" else team.read_board_text(target)); n[kind] += 1
        except PermissionError:
            err[kind] += 1
        time.sleep(0.004)
kinds = ["plain"] + (["helper"] if hasattr(team, "read_board_text") else [])
ts = [threading.Thread(target=writer)] + [threading.Thread(target=reader, args=(k,)) for k in kinds for _ in range(2)]
[t.start() for t in ts]; [t.join() for t in ts]
print("counts", dict(n), "read errors", dict(err))
bad = (("helper" in kinds and err["helper"] > 0) or err["plain"] == 0)
print("FAILS", int(bad)); sys.exit(1 if bad else 0)
