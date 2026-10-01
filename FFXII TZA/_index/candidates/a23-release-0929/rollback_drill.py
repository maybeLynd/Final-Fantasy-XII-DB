"""A23 rollback drill (SWE2-FRONTIER). Materialise an earlier release's reader outside the working tree (git archive, the
same effect as the record's `git worktree add --detach` step without a full checkout), start it on a SPARE port against
the live store (read-only), read /api/status and one view, then stop ONLY the child this script started (by its handle).
The live server on 8765, the controller and the store are not touched."""
import hashlib, io, json, subprocess, sys, tarfile, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(r"C:\Users\Kristian\source\repos\XIIOnline")
STORE = REPO / "Database" / "Tools" / "work" / "dashboard"
W = Path(__file__).resolve().parent
OUT = W / "run" / "rollback"
assert not OUT.exists(), "prior drill exists"
OUT.mkdir(parents=True)
TARGET = sys.argv[1] if len(sys.argv) > 1 else "763d466d6"
PORT = 8766
SCR = Path(r"C:\Users\Kristian\AppData\Local\Temp\claude\C--Users-Kristian-source-repos\73162e75-93f2-44be-9de2-25044eacdc46\scratchpad\SWE2-FRONTIER\rb")
assert not SCR.exists(), "scratch materialisation exists"
paths = ["Database/Tools/dashboard", "Database/Tools/analysis-kit/gfz-scripts/generation.py"]
tar = subprocess.run(["git", "-C", str(REPO), "archive", "--format=tar", TARGET] + paths, capture_output=True, check=True).stdout
tarfile.open(fileobj=io.BytesIO(tar)).extractall(SCR)
srv = SCR / "Database" / "Tools" / "dashboard" / "server.py"
rec = {"target": TARGET, "target_full": subprocess.run(["git", "-C", str(REPO), "rev-parse", TARGET], capture_output=True, text=True).stdout.strip(),
       "materialised": str(SCR), "server_sha256": hashlib.sha256(srv.read_bytes()).hexdigest(),
       "generation_py_sha256": hashlib.sha256((SCR / "Database/Tools/analysis-kit/gfz-scripts/generation.py").read_bytes()).hexdigest(),
       "port": PORT, "started": datetime.now(timezone.utc).isoformat()}
p = subprocess.Popen([sys.executable, str(srv), "--root", str(STORE), "--port", str(PORT)],
                     stdout=open(OUT / "server.out", "wb"), stderr=subprocess.STDOUT)
rec["child_pid"] = p.pid
try:
    body = None
    for _ in range(40):
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/api/status" % PORT, timeout=5) as r:
                body = r.read(); rec["status_http"] = r.status
            break
        except Exception as e:
            rec["last_wait_error"] = "%s: %s" % (type(e).__name__, e)
            time.sleep(0.5)
    if body is not None:
        (OUT / "status.body").write_bytes(body)
        s = json.loads(body)
        rec.update({"generation": s.get("generation"), "problems": s.get("problems"), "reader_stale": s.get("reader_stale"),
                    "drift": s.get("drift")})
        with urllib.request.urlopen("http://127.0.0.1:%d/api/view/progress" % PORT, timeout=10) as r:
            vb = r.read(); rec["view_progress_http"] = r.status
        (OUT / "view-progress.body").write_bytes(vb)
        v = json.loads(vb)
        g = s.get("generation")
        f = STORE / g / "outputs" / "view-progress.json"
        rec["view_progress_equals_store_output"] = v.get("view") == json.loads(f.read_bytes()) if f.exists() else "store output missing"
    live = json.loads(urllib.request.urlopen("http://127.0.0.1:8765/api/status", timeout=10).read())
    rec["live_8765_generation_during_drill"] = live.get("generation")
finally:
    p.terminate()
    try:
        p.wait(timeout=10)
    except subprocess.TimeoutExpired:
        p.kill(); p.wait(timeout=10)
    rec["child_exit"] = p.returncode
    rec["stopped"] = datetime.now(timezone.utc).isoformat()
    try:
        urllib.request.urlopen("http://127.0.0.1:%d/api/status" % PORT, timeout=3)
        rec["port_after_stop"] = "STILL ANSWERING"
    except Exception as e:
        rec["port_after_stop"] = "closed (%s)" % type(e).__name__
(OUT / "rollback-result.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
print(json.dumps(rec, indent=1))
