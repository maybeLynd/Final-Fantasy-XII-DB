"""control_replace.py (SWE2-FRONTIER, 2026-10-03, ASTRA-REQ-FRONTIER-ATOMIC-BOARD-WRITE-DENIAL-1003) - does _write_board_text survive a reader that holds the target open past the old ~3.2 s window?

A reader thread opens the target with Python's open() (no FILE_SHARE_DELETE) and holds it HOLD seconds while the
writer replaces it. Run against a team.py given as argv[1] (default: the kit's), then hold times in seconds (default 1 5). Expected: the pre-fix team.py raises PermissionError for
HOLD=5; the fixed one succeeds and the target carries the new text. HOLD=1 must succeed on both (no regression).
"""
import importlib.util, os, sys, tempfile, threading, time
KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts", "team.py"))
ARGS = sys.argv[1:] or [KIT, "1", "5"]
spec = importlib.util.spec_from_file_location("team_under_test", ARGS[0]); team = importlib.util.module_from_spec(spec)
spec.loader.exec_module(team)
def trial(hold):
    d = tempfile.mkdtemp(prefix="frontier-replace-")
    from pathlib import Path
    target = Path(d) / "TEAM.json"; target.write_text("old\n", encoding="utf-8")
    opened = threading.Event()
    def reader():
        with open(target, encoding="utf-8") as f:
            opened.set(); time.sleep(hold); f.read()
    th = threading.Thread(target=reader); th.start(); opened.wait()
    t0 = time.monotonic()
    try:
        team._write_board_text(target, "new\n"); res = "ok"
    except PermissionError as e:
        res = "PermissionError winerror=%s" % getattr(e, "winerror", None)
    el = time.monotonic() - t0; th.join()
    content = target.read_text(encoding="utf-8").strip()
    left = [p for p in os.listdir(d) if p != "TEAM.json"]
    print("hold %.1fs: %s after %.2fs, target=%r, leftover tmp=%s" % (hold, res, el, content, left))
    return res, content, left
fails = 0
for h in [float(x) for x in ARGS[1:]]:
    res, content, left = trial(h)
    fails += (res != "ok" or content != "new" or bool(left))
print("FAILS", fails)
sys.exit(1 if fails else 0)
