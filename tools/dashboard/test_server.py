"""test_server.py - the dashboard server through its real HTTP entry point (OPUS, 2026-09-29; matrix A17 / A19 at
server scope). A fixture generation store is built with generation.py; the server runs on an ephemeral loopback port.

  S1  it binds 127.0.0.1 only
  S2  a valid generation: status lists the seven required views; the present valid view is OK and served with its
      generation id; absent required views are UNMEASURED (not empty, not OK)
  S3  a view with a measure lacking `limits` -> MALFORMED, no view body served
  S4  a view with numerator > denominator -> MALFORMED
  S5  an output tampered after commit AND after the server verified it -> the next request re-verifies (the cache key
      includes each file's size/mtime); CURRENT is rejected and the last verified generation is served as HISTORICAL (the
      includes each file's size/mtime), every view INVALID, no data served; restoring the file makes it valid again
  S6  a source moved after commit -> status STALE with the input named, data still served (valid as of its inputs)
  S7  a failed later build -> CURRENT unchanged and the failure is reported alongside
  S8  POST / DELETE -> 405; unknown path -> 404
  S10 a VOLATILE input moving after the snapshot is reported separately and does not mark views STALE
  S11 a node state outside DASHBOARD-MEANINGS.md (e.g. 'MET') -> MALFORMED; axis states and package stages pass
  S12 an unreadable vocabulary fails closed for views with node states
  S13 no generation verifies -> INVALID everywhere, "no verified generation is available", nothing served
  S14 a failure older than CURRENT is reported resolved; a newer one is not
  S15 a reader whose code changed on disk since it started reports reader_stale (RESTART REQUIRED)
  S16 an unknown manifest format is UNSUPPORTED, not a guessed verdict
  S18 a progress view claiming DATABASE READY with a terminal requirement other than 30 is refused (ASTRA 037557884)
  S17 a same-length edit with the mtime restored (ASTRA's counterexample, cccd7c04c) is detected on the next warm
      request: the served content is re-hashed every request, and status states the verification scope
  S9  the page is served and polls /api/status (no model call, no scan)
"""
import json, os, shutil, sys, tempfile, threading, urllib.error, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "analysis-kit", "gfz-scripts"))
import generation as G  # noqa: E402
import server as S  # noqa: E402
fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
T = tempfile.mkdtemp(prefix="dash_"); src = os.path.join(T, "board.json"); open(src, "w").write('{"revision": 1}')
M = lambda i, n, d, **k: dict({"id": i, "label": i, "numerator": n, "denominator": d, "scope": "fixture", "instrument": "fixture",
                               "as_of": "2026-09-29", "limits": "fixture"}, **k)
GOOD = {"view": "vbf", "title": "VBF archive", "status": "OK", "source": {"identity": "fixture"},
        "measures": [M("files", 89414, None), M("parsed", 10, 48)], "tree": [{"id": "gamedata", "label": "gamedata", "counts": {"files": 1}}]}
st = G.Store(os.path.join(T, "gens"))
def publish(views):
    b = st.begin({"board": {"path": src}}, {"name": "fixture"})
    for n, v in views.items():
        open(b.output_path("view-%s.json" % n), "w").write(json.dumps(v))
    return st.commit(b, ["view-%s.json" % n for n in views])
g1 = publish({"vbf": GOOD})
srv = S.serve(st.root, 0); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
def get(p, method="GET"):
    req = urllib.request.Request("http://127.0.0.1:%d%s" % (port, p), method=method)
    try:
        r = urllib.request.urlopen(req, timeout=10); return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
J = lambda p: json.loads(get(p)[1])
check("S1", srv.server_address[0] == "127.0.0.1", str(srv.server_address))
s = J("/api/status"); v = J("/api/view/vbf"); u = J("/api/view/systems")
check("S2", s["generation"] == g1 and s["required"] == list(S.REQUIRED) and s["views"]["vbf"] == "OK"
      and all(s["views"][n] == "UNMEASURED" for n in S.REQUIRED if n != "vbf") and v["view"]["measures"][0]["numerator"] == 89414
      and v["meta"]["generation"] == g1 and u["status"] == "UNMEASURED", json.dumps(s["views"]))
bad = dict(GOOD, view="types", measures=[{k: x for k, x in M("m", 1, 2).items() if k != "limits"}])
over = dict(GOOD, view="fleet", measures=[M("m", 5, 2)])
publish({"vbf": GOOD, "types": bad, "fleet": over}); s = J("/api/status"); vt = J("/api/view/types"); vf = J("/api/view/fleet")
check("S3", s["views"]["types"] == "MALFORMED" and vt["status"] == "MALFORMED" and "limits" in vt["why"] and "view" not in vt, vt.get("why"))
check("S4", s["views"]["fleet"] == "MALFORMED" and "exceeds" in vf["why"], vf.get("why"))
man, d, _ = st.open_current(); op = os.path.join(d, "outputs", "view-vbf.json"); keep = open(op, "rb").read()
open(op, "w").write(json.dumps(dict(GOOD, measures=[M("files", 1, None)])))
s2 = J("/api/status"); v2 = J("/api/view/vbf")     # no restart: the file change alone forces re-verification
# 2026-09-29 incident: a rejected CURRENT no longer blanks the page when an earlier generation still verifies - that one is
# served, labelled HISTORICAL, with the reason CURRENT was rejected; the tampered bytes are never served
check("S5", s2["historical"] and s2["generation"] == g1 and s2["current"]["generation"] == man["generation"] and s2["current"]["problems"]
      and s2["views"]["vbf"] == "HISTORICAL" and v2["meta"]["historical"] and v2["view"]["measures"][0]["numerator"] == 89414,
      "CURRENT %s rejected (%s); serving last verified %s" % (man["generation"], "; ".join(s2["current"]["problems"]), s2["generation"]))
# S13: no generation verifies at all -> INVALID everywhere and "no verified generation is available"; nothing served
g1dir = os.path.join(st.root, g1, "outputs", "view-vbf.json"); keep1 = open(g1dir, "rb").read(); open(g1dir, "w").write("{}")
s13 = J("/api/status"); v13 = J("/api/view/vbf"); open(g1dir, "wb").write(keep1)
check("S13", s13["no_verified_generation"] and all(x == "INVALID" for x in s13["views"].values()) and "view" not in v13
      and v13["why"] == "no verified generation is available", v13.get("why"))
open(op, "wb").write(keep)
open(src, "w").write('{"revision": 2}')
s = J("/api/status")
check("S6", s["drift"] == {"board": "changed"} and s["views"]["vbf"] == "STALE" and J("/api/view/vbf")["view"]["status"] == "OK", json.dumps(s["drift"]))
open(src, "w").write('{"revision": 1}')
cur = st.current_id()
try:
    st.commit(st.begin({"board": {"path": src}}), ["view-vbf.json"])
except G.GenerationError:
    pass
s = J("/api/status")
check("S7", st.current_id() == cur and s["generation"] == cur and s["failure"] and "required outputs missing" in s["failure"]["reason"], s["failure"]["reason"] if s["failure"] else None)
vb = os.path.join(T, "vol.json"); open(vb, "w").write("1")
bb = st.begin({"board": {"path": src}, "live": {"path": vb, "volatile": True}}, {"name": "fixture"})
open(bb.output_path("view-vbf.json"), "w").write(json.dumps(GOOD)); st.commit(bb, ["view-vbf.json"])
open(vb, "w").write("2"); s10 = J("/api/status")
check("S10", s10["views"]["vbf"] == "OK" and s10["drift"] == {} and s10["volatile_drift"] == {"live": "changed"},
      "volatile drift %s shown, views not STALE" % s10["volatile_drift"])
bad_state = dict(GOOD, view="systems", tree=[{"id": "S-01", "label": "S-01", "state": "MET"}])
ok_state = dict(GOOD, view="types", tree=[{"id": "t", "label": "t", "state": "TYPE-RESOLVED", "children": [{"id": "p", "label": "p", "state": "research"}]}])
publish({"vbf": GOOD, "systems": bad_state, "types": ok_state}); s11 = J("/api/status"); v11 = J("/api/view/systems")
check("S11", s11["views"]["systems"] == "MALFORMED" and "vocabulary" in v11["why"] and s11["views"]["types"] == "OK", v11.get("why"))
check("S12", S.load_vocabulary(os.path.join(T, "nope.md")) is None and S.check_view(ok_state, None) and not S.check_view(GOOD, None),
      "vocabulary unreadable -> None; a view with node states is then MALFORMED; a view without states is unaffected")
# S14: a failure older than the current generation is reported as resolved; a newer one is not
fp = os.path.join(st.root, G.FAILURE); keepf = open(fp, "rb").read() if os.path.exists(fp) else None
open(fp, "w").write(json.dumps({"generation": "gX", "failed_at": "2000-01-01T00:00:00Z", "reason": "old"})); f_old = J("/api/status")["failure"]
open(fp, "w").write(json.dumps({"generation": "gY", "failed_at": "2999-01-01T00:00:00Z", "reason": "new"})); f_new = J("/api/status")["failure"]
if keepf is not None: open(fp, "wb").write(keepf)
check("S14", f_old["resolved"] is True and f_new["resolved"] is False, "old -> resolved, newer than CURRENT -> not resolved")
# S15: a reader whose code changed on disk since it started says RESTART REQUIRED; S16: an unknown manifest format -> UNSUPPORTED
real = G.VERIFIER_SHA; G.VERIFIER_SHA = "0" * 64; s15 = J("/api/status")["reader_stale"]; G.VERIFIER_SHA = real
check("S15", s15 is True and J("/api/status")["reader_stale"] is False)
m16, d16, _ = st.open_current(); mp16 = os.path.join(d16, G.MANIFEST); k16 = open(mp16, "rb").read()
open(mp16, "wb").write(k16.replace(b'"ff12-generation-2"', b'"ff12-generation-9"')); s16 = J("/api/status")
open(mp16, "wb").write(k16)
check("S16", any(p.startswith("UNSUPPORTED") for p in s16["current"]["problems"]), "; ".join(s16["current"]["problems"])[:120])
# S17: same length, mtime restored - the stat key cannot see it; the per-request content hash must
J("/api/status")                                          # warm the cache on the current generation
m17, d17, _ = st.open_current(); o17 = os.path.join(d17, "outputs", "view-vbf.json"); k17 = open(o17, "rb").read()
t17 = os.stat(o17); i17 = k17.index(b"89414"); edited = k17[:i17] + b"89415" + k17[i17 + 5:]
open(o17, "wb").write(edited); os.utime(o17, ns=(t17.st_atime_ns, t17.st_mtime_ns))
s17 = J("/api/status"); v17 = J("/api/view/vbf")
open(o17, "wb").write(k17); os.utime(o17, ns=(t17.st_atime_ns, t17.st_mtime_ns))
check("S17", len(edited) == len(k17) and any("view-vbf.json" in p for p in s17["current"]["problems"])
      and v17.get("view", {}).get("measures", [{}])[0].get("numerator") != 89415 and "every request" in s17["verification"]
      and s17["verified_at"], "same-stat edit reported: %s" % "; ".join(s17["current"]["problems"])[:90])
check("S8", get("/api/status", "POST")[0] == 405 and get("/api/view/vbf", "DELETE")[0] == 405 and get("/nope")[0] == 404)
code, page = get("/")
check("S9", code == 200 and b"/api/status" in page and b"setInterval(poll,5000)" in page)
srv.shutdown(); shutil.rmtree(T, ignore_errors=True)
# S18 (ASTRA's My Progress REJECT, 037557884) - a view claiming DATABASE READY with a terminal requirement other than 30 is refused
def pview(req, acc):
    one = {"accepted": 1, "total": 1}
    return {"progress": {"version": "MP-2", "measured": True, "scopes": {"union": one, "L1": one, "L2": one}, "categories": [],
                         "reconstruction": {"state": "DATABASE READY - awaiting user authorization"}, "terminal": {"accepted": acc, "required": req}},
            "measures": [{"id": k, "numerator": 1, "denominator": 1} for k in ("union", "L1", "L2")]}
check("S18", S.check_progress(pview(0, 0)) is not None and S.check_progress(pview(30, 30)) is None,
      "required 0 -> %s; required 30 -> accepted" % S.check_progress(pview(0, 0)))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
