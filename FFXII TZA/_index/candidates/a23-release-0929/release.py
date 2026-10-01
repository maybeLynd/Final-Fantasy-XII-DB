"""A23 release capture (SWE2-FRONTIER, 2026-09-29). One bounded run; refuses to overwrite a prior run.

status-before -> CURRENT pin -> guarded export (generation.py export, subprocess, exit kept) -> verify-zip (exit kept)
-> served views -> status-after. Then: served view objects vs the ZIP's outputs, manifest source hashes vs Git HEAD
blobs, CURRENT/served/exported generation all equal. Nothing on the server, store or controller is modified; the
only write outside this directory is the export ZIP + sidecar in work/dashboard-exports (the documented release path).
"""
import hashlib, json, os, subprocess, sys, urllib.request, zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
RUN = W / "run"
assert not RUN.exists(), "a prior run exists - inspect it, do not overwrite"
RUN.mkdir()
REPO = Path(r"C:\Users\Kristian\source\repos\XIIOnline")
TOOLS = REPO / "Database" / "Tools"
STORE = TOOLS / "work" / "dashboard"
GEN = TOOLS / "analysis-kit" / "gfz-scripts" / "generation.py"
BASE = "http://127.0.0.1:8765"
now = lambda: datetime.now(timezone.utc).isoformat()
log = {"started": now(), "steps": []}


def get(path, name):
    t = now()
    try:
        with urllib.request.urlopen(BASE + path, timeout=10) as r:
            body, st = r.read(), r.status
    except Exception as e:
        log["steps"].append({"step": name, "path": path, "utc": t, "error": "%s: %s" % (type(e).__name__, e)})
        return None
    (RUN / (name + ".body")).write_bytes(body)
    log["steps"].append({"step": name, "path": path, "utc": t, "status": st, "bytes": len(body),
                         "sha256": hashlib.sha256(body).hexdigest()})
    return body


def run(argv, name):
    t = now()
    p = subprocess.run(argv, capture_output=True, text=True, cwd=str(TOOLS / "dashboard"))
    log["steps"].append({"step": name, "argv": argv, "utc": t, "exit": p.returncode,
                         "stdout": p.stdout.strip()[-2000:], "stderr": p.stderr.strip()[-2000:]})
    return p


sb = json.loads(get("/api/status", "status-before"))
cur = json.loads((STORE / "CURRENT").read_text(encoding="utf-8"))
log["current_pointer"] = cur
gen = cur["generation"]
zip_path = TOOLS / "work" / "dashboard-exports" / (gen + ".zip")
assert not zip_path.exists(), "export already exists for %s" % gen
ex = run([sys.executable, str(GEN), "export", str(STORE), str(zip_path)], "export")
vz = run([sys.executable, str(GEN), "verify-zip", str(zip_path)], "verify-zip")
views = {}
for v in (list(sb.get("views")) if isinstance(sb.get("views"), dict) else [x.get("name") if isinstance(x, dict) else x for x in (sb.get("views") or [])]):
    b = get("/api/view/" + v, "view-" + v)
    if b is not None:
        views[v] = json.loads(b)
get("/", "root")
sa = json.loads(get("/api/status", "status-after"))
cur_after = json.loads((STORE / "CURRENT").read_text(encoding="utf-8"))
log["current_pointer_after"] = cur_after

res = {"generation_status_before": sb.get("generation"), "generation_current_pin": gen,
       "generation_status_after": sa.get("generation"), "current_pointer_after": cur_after.get("generation"),
       "problems_before": sb.get("problems"), "problems_after": sa.get("problems"),
       "reader_stale_before": sb.get("reader_stale"), "reader_stale_after": sa.get("reader_stale"),
       "export_exit": ex.returncode, "verify_zip_exit": vz.returncode, "verify_zip_stdout": vz.stdout.strip()}
res["served_equals_exported"] = sb.get("generation") == gen == sa.get("generation")
if zip_path.exists():
    zb = zip_path.read_bytes()
    res["zip"] = {"path": str(zip_path), "bytes": len(zb), "sha256": hashlib.sha256(zb).hexdigest(),
                  "sidecar": (Path(str(zip_path) + ".sha256")).read_text(encoding="utf-8").strip()}
    res["zip"]["sidecar_matches"] = res["zip"]["sidecar"].split()[0] == res["zip"]["sha256"]
    with zipfile.ZipFile(zip_path) as z:
        man = json.loads(z.read("MANIFEST.json"))
        res["zip"]["members"] = len([i for i in z.infolist() if not i.filename.endswith("/")])
        cmp = {}
        for v, obj in views.items():
            served = obj.get("view", obj)
            cand = [n for n in z.namelist() if n == "outputs/view-%s.json" % v]
            if not cand:
                cmp[v] = "no ZIP output named %s" % v
                continue
            try:
                zobj = json.loads(z.read(cand[0]))
            except ValueError:
                cmp[v] = "ZIP output %s not JSON" % cand[0]
                continue
            cmp[v] = {"zip_member": cand[0], "equal": served == zobj, "served_meta_generation": (obj.get("meta") or {}).get("generation")}
        res["served_view_vs_zip"] = cmp
    # source binding: manifest-recorded hashes vs the Git blobs of the same paths at ONE pinned revision.
    # Repaired 2026-09-30 (ASTRA-REQ-FRONTIER-A23-GIT-LOOKUP-ADMISSION): the first headsha() ignored Git exit codes, so a
    # failed lookup returned SHA256(b"") and an empty commit. source_lookup.bind() keeps every exit/stderr and reports
    # INCOMPLETE (equal=None) for a failed lookup; HEAD is resolved once, checked, and recorded.
    sys.path.insert(0, str(W))
    import source_lookup
    rp = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--verify", "HEAD"], capture_output=True, text=True)
    rev = rp.stdout.strip() if rp.returncode == 0 else None
    res["source_rev"] = {"rev": rev, "exit": rp.returncode, "stderr": rp.stderr.strip()}
    bind = {}
    targets = [(n, r, man["inputs"].get(n, {}).get("sha256")) for n, r in (
        ("build_views.py", "Database/Tools/dashboard/build_views.py"),
        ("requirements.py", "Database/Tools/dashboard/requirements.py"),
        ("uc1_band.py", "Database/Tools/analysis-kit/gfz-scripts/uc1_band.py"))]
    targets.append(("verifier(generation.py)", "Database/Tools/analysis-kit/gfz-scripts/generation.py", man.get("verifier")))
    targets.append(("server.py", "Database/Tools/dashboard/server.py",
                    hashlib.sha256((TOOLS / "dashboard" / "server.py").read_bytes()).hexdigest()))
    for name, rel, recorded in targets:
        bind[name] = source_lookup.bind(REPO, rel, recorded, rev) if rev else {"state": "INCOMPLETE", "equal": None, "why": "HEAD did not resolve"}
    bind["server.py"]["note"] = "recorded = the file on disk; reader_stale=false says the running code equals it"
    res["source_binding"] = bind
    res["manifest_generator"] = man.get("generator")
log["result"] = res
log["finished"] = now()
(RUN / "release-result.json").write_text(json.dumps(log, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
