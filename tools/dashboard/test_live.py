"""test_live.py - Agent Activity, percentage-point deltas and the full-refresh countdown (OPUS, 2026-09-29). Fixtures only.

  A1  one agent working in one category -> that category's label is one span in that agent's colour
  A2  two agents share a category -> the label splits into two contiguous spans, deterministic order
  A3  three agents -> thirds
  A4  one active agent + one queued reviewer -> the active one colours the label, the reviewer is muted (outlined), not working
  A5  a stale controller feed -> the lane's liveness is UNKNOWN and its ACTIVE claim is 'claimed', never 'working'
  A6  an agent moving between categories -> the colour follows the claim to the new category, the old one goes neutral
  A7  colours are stable across refreshes and input order, and never repeat among visible lanes (incl. a new unknown lane)
  A8  a review another lane queues for OPUS (fresh task timestamp) does not make OPUS 'recent', with no feed or an UNKNOWN
      Claude classification: OPUS's two-hour-old claim stays 'claimed', the review 'waiting'; the issuer is the one credited
  A9  a fresh OPUS note (history only, no task timestamp change) makes OPUS 'recent' and its claim 'working'; 61 min -> UNKNOWN
  D1  + / - / 0 percentage-point deltas, as points (not relative growth)
  D2  a denominator change -> 'scope changed', never a numeric delta
  D3  a definition-version change -> 'N/A - definition changed'
  D4  the overall figure UNMEASURED: the known-scope union measure still carries its numeric delta
  D5  a tampered prior generation is not used as the comparison basis (the older verified one is)
  D6  one basis: a newer verified generation without a progress view gives NO progress prior, never an older one
      (ASTRA 9e84de620); delta_basis names the compared generation and the measure delta says "no prior"
  D7  control: when the basis carries a progress view, prior_progress comes from that same generation
  T1  healthy controller -> OK with next_at = last_run + the controller's configured interval (read from its source)
  T2  a build in progress -> REFRESHING
  T3  the last full refresh failed -> FAILED (the countdown becomes the retry)
  T4  controller stopped / state unreadable / no build recorded -> UNKNOWN with the reason, never a guessed countdown
  T5  past the deadline by more than two polls -> OVERDUE
  J1  the page's delta renders text only, coloured by class (no dots, badges, arrows or icons)
  D10 an empty scope counts as complete: 0 of 0 -> 0 of 10 is -100 points
  J2  the countdown runs one tick interval and one live poll, cleared before re-creation on reload
  J5  a count delta renders '+N (+x.x%)' coloured by direction; a moved denominator renders '+a of +b', muted
  D8  a count measure carries its signed and relative change; D9 a moved denominator carries both sides' changes
  J4  colour follows the measure's direction: register-open ("down") rising is red, a "down" fall green; "none", an
      undeclared direction and an unknown word are muted whatever the sign (FABLE-REQ-OPUS-DELTA-COLOUR-DIRECTION)
"""
import json, os, shutil, subprocess, sys, tempfile, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "analysis-kit", "gfz-scripts"))
import activity as A  # noqa: E402
import build_views as BV  # noqa: E402
import generation as G  # noqa: E402
import requirements as R  # noqa: E402
import server as S  # noqa: E402

fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

T = tempfile.mkdtemp(prefix="live_")
NOW = time.time()
iso = lambda s_ago: time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(NOW - s_ago))
cmap = R.load_map(os.path.join(HERE, "..", "..", "FFXII TZA", "_index", "workflow", "my-progress", "category-map.tsv"))
placer = A.Placer(cmap, {"facts": []}, {})
def task(i, st, agent=None, to=None, target="", upd=60):
    return {"id": i, "status": st, "agent": agent, "assigned_to": to, "target": target, "scope": "", "question": "", "updated_at": iso(upd)}
POLL = {"ts": iso(30), "lane_state": {"SWE2-DATA": "busy-active", "SWE2-ORACLE": "busy-wake", "SWE2-EC7": "busy-active", "SWE2-AUDIT-SEM": "free"}}
def run(tasks, poll=POLL, claude=None, history=None):
    return A.compute({"tasks": tasks, "revision": 1, "history": history or []}, poll, claude or {}, placer, NOW)
cat = lambda r, code: next(c for c in r["categories"] if c["code"] == code)
W = "07-Combat-Action/x.md"

r1 = run([task("DATA-1", "ACTIVE", "SWE2-DATA", target=W)])
check("A1", cat(r1, "C")["working"] == ["SWE2-DATA"] and cat(r1, "W")["working"] == [], "Combat working %s" % cat(r1, "C")["working"])
r2 = run([task("DATA-1", "ACTIVE", "SWE2-DATA", target=W), task("OR-1", "ACTIVE", "SWE2-ORACLE", target=W)])
r2b = run([task("OR-1", "ACTIVE", "SWE2-ORACLE", target=W), task("DATA-1", "ACTIVE", "SWE2-DATA", target=W)])
check("A2", cat(r2, "C")["working"] == ["SWE2-DATA", "SWE2-ORACLE"] == cat(r2b, "C")["working"], "order %s (input order ignored)" % cat(r2, "C")["working"])
r3 = run([task("DATA-1", "ACTIVE", "SWE2-DATA", target=W), task("OR-1", "ACTIVE", "SWE2-ORACLE", target=W), task("EC-1", "ACTIVE", "SWE2-EC7", target=W)])
check("A3", len(cat(r3, "C")["working"]) == 3, "three working %s" % cat(r3, "C")["working"])
r4 = run([task("DATA-1", "ACTIVE", "SWE2-DATA", target=W), task("X-REVIEW-1", "READY", to="SWE2-AUDIT-SEM", target=W)])
check("A4", cat(r4, "C")["working"] == ["SWE2-DATA"] and cat(r4, "C")["muted"] == ["SWE2-AUDIT-SEM"]
      and any(i["kind"] == "waiting" for i in cat(r4, "C")["items"]), "working %s, muted %s" % (cat(r4, "C")["working"], cat(r4, "C")["muted"]))
stale = dict(POLL, ts=iso(4000))
r5 = run([task("DATA-1", "ACTIVE", "SWE2-DATA", target=W, upd=7200)], poll=stale)
check("A5", r5["liveness"]["SWE2-DATA"][0] == "UNKNOWN" and cat(r5, "C")["working"] == [] and cat(r5, "C")["muted"] == ["SWE2-DATA"]
      and r5["liveness"]["ASTRA"][0] == "UNKNOWN", "stale feed -> %s; ASTRA without feed or recent write -> %s" % (r5["liveness"]["SWE2-DATA"], r5["liveness"]["ASTRA"][0]))
r6a = run([task("DATA-1", "ACTIVE", "SWE2-DATA", target=W)]); r6b = run([task("DATA-2", "ACTIVE", "SWE2-DATA", target="03-World-Area-Field/y.md")])
check("A6", cat(r6a, "C")["working"] == ["SWE2-DATA"] and cat(r6b, "C")["working"] == [] and cat(r6b, "W")["working"] == ["SWE2-DATA"], "moved Combat -> World")
c1 = A.colors({"OPUS", "SWE2-DATA", "SWE2-NEW-LANE"}); c2 = A.colors({"SWE2-NEW-LANE", "OPUS", "SWE2-DATA"})
allc = A.colors(set(A.PALETTE) | {"SWE2-NEW-LANE", "ZETA"})
check("A7", c1 == c2 and c1["OPUS"] == A.PALETTE["OPUS"] and len(set(allc.values())) == len(allc), "stable; %d visible lanes, %d distinct colours" % (len(allc), len(set(allc.values()))))
# A8/A9: ASTRA's discriminators for 8ddc8c7e8 (00fd54fda). Writes are attributed to the lane that ISSUED the operation.
hop = lambda agent, action, tid, s_ago: {"at": iso(s_ago), "agent": agent, "operation": {"action": action, "task": {"id": tid}}}
old_claim = task("OPUS-OLD", "ACTIVE", "OPUS", target=W, upd=7200)
foreign = task("FABLE-REVIEW-X", "READY", to="OPUS", target=W, upd=60)
hist8 = [hop("OPUS", "claim", "OPUS-OLD", 7200), hop("FABLE", "add", "FABLE-REVIEW-X", 60)]
r8 = run([old_claim, foreign], history=hist8)
r8u = run([old_claim, foreign], history=hist8, claude={"OPUS": {"classification": "UNKNOWN"}})
k8 = lambda r: {i["task"]: i["kind"] for i in cat(r, "C")["items"]}
check("A8", all(r["liveness"]["OPUS"][0] == "UNKNOWN" and "OPUS" not in cat(r, "C")["working"] and k8(r) == {"OPUS-OLD": "claimed", "FABLE-REVIEW-X": "waiting"}
                and r["liveness"]["FABLE"][0] == "recent" for r in (r8, r8u)),
      "a review FABLE queued for OPUS credits FABLE, not OPUS: OPUS %s, kinds %s" % (r8["liveness"]["OPUS"], k8(r8)))
r9 = run([old_claim], history=[hop("OPUS", "claim", "OPUS-OLD", 7200), hop("OPUS", "note", "OPUS-OLD", 300)])
r9x = run([old_claim], history=[hop("OPUS", "claim", "OPUS-OLD", 7200), hop("OPUS", "note", "OPUS-OLD", 3700)])
check("A9", r9["liveness"]["OPUS"][0] == "recent" and k8(r9) == {"OPUS-OLD": "working"} and r9x["liveness"]["OPUS"][0] == "UNKNOWN"
      and k8(r9x) == {"OPUS-OLD": "claimed"} and run([old_claim])["liveness"]["OPUS"][0] == "UNKNOWN",
      "an OPUS note 5 min ago with no task timestamp change -> %s/%s; 61 min ago -> %s; no history -> UNKNOWN"
      % (r9["liveness"]["OPUS"][0], k8(r9), r9x["liveness"]["OPUS"][0]))

# deltas
def view(name, defn, ms):
    return {"view": name, "definition": defn, "measures": [{"id": i, "numerator": n, "denominator": d, "scope": sc} for i, n, d, sc in ms]}
pd = os.path.join(T, "prior"); os.makedirs(os.path.join(pd, "outputs"))
json.dump(view("progress", "MP-2", [("union", 500, 1000, "u"), ("L1", 40, 100, "l1"), ("L2", 50, 100, "l2"), ("cat-C", 10, 20, "c")]),
          open(os.path.join(pd, "outputs", "view-progress.json"), "w"))
json.dump(view("types", "v1", [("fields", 10, 100, "t")]), open(os.path.join(pd, "outputs", "view-types.json"), "w"))
now_v = {"progress": view("progress", "MP-2", [("union", 520, 1000, "u"), ("L1", 39, 100, "l1"), ("L2", 50, 100, "l2"), ("cat-C", 10, 25, "c")]),
         "types": view("types", "v2", [("fields", 12, 100, "t")])}
now_v["progress"]["progress"] = {"measured": False}
BV.annotate_deltas(now_v, pd, {"generation": "gPRIOR"})
dm = {m["id"]: m["delta"] for m in now_v["progress"]["measures"]}
check("D1", dm["union"]["pp"] == 2.0 and dm["L1"]["pp"] == -1.0 and dm["L2"]["pp"] == 0.0, "union %+.1f, L1 %+.1f, L2 %+.1f (points)" % (dm["union"]["pp"], dm["L1"]["pp"], dm["L2"]["pp"]))
_pc = {m["id"]: m for m in json.load(open(os.path.join(pd, "outputs", "view-progress.json")))["measures"]}["cat-C"]
check("D2", dm["cat-C"].get("na") == "scope changed" and dm["cat-C"].get("pp") == round(100.0 * 10 / 25 - 100.0 * _pc["numerator"] / _pc["denominator"], 3),
      "moved denominator still carries the completion-%% change (user directive 2026-09-30): %s; %s" % (dm["cat-C"].get("pp"), dm["cat-C"].get("why")))
check("D3", now_v["types"]["measures"][0]["delta"].get("na") == "N/A - definition changed", now_v["types"]["measures"][0]["delta"].get("why"))
check("D4", now_v["progress"]["progress"]["measured"] is False and "pp" in dm["union"], "UNMEASURED overall, known-scope delta %+.1f" % dm["union"]["pp"])
st = G.Store(os.path.join(T, "gens")); src = os.path.join(T, "s.txt"); open(src, "w").write("1")

# D8/D9 (2026-09-29, user request: a change on every tile): a count with no denominator carries its signed and relative
# change; a moved denominator carries both sides' changes (still no percentage-point delta)
pdc = os.path.join(T, "prior_c"); os.makedirs(os.path.join(pdc, "outputs"))
json.dump(view("vbf", "v1", [("files", 100, None, "a"), ("bytes", 0, None, "a"), ("fmt", 40, 48, "x")]), open(os.path.join(pdc, "outputs", "view-vbf.json"), "w"))
nowc = {"vbf": view("vbf", "v1", [("files", 112, None, "a"), ("bytes", 5, None, "a"), ("fmt", 45, 51, "x"), ("new", 3, None, "a")])}
BV.annotate_deltas(nowc, pdc, {"generation": "gP"})
dc = {m["id"]: m["delta"] for m in nowc["vbf"]["measures"]}
check("D8", dc["files"].get("count") == 12 and dc["files"].get("rel") == 12.0 and dc["bytes"].get("count") == 5 and dc["bytes"].get("rel") is None
      and dc["new"].get("na") == "no prior", "files %s, bytes %s, new %s" % (dc["files"], dc["bytes"].get("count"), dc["new"].get("na")))
check("D9", dc["fmt"].get("na") == "scope changed" and dc["fmt"].get("dnum") == 5 and dc["fmt"].get("dden") == 3
      and dc["fmt"].get("pp") == round(100.0 * 45 / 51 - 100.0 * 40 / 48, 3),
      "moved denominator -> pp %s with %s of %s kept for the tooltip" % (dc["fmt"].get("pp"), dc["fmt"].get("dnum"), dc["fmt"].get("dden")))
# D10 (user, 2026-09-30): an empty scope counts as 100 % complete, so 0 of 0 -> 0 of 10 is a 100-point fall, not "0 of +10"
pdz = os.path.join(T, "prior_z"); os.makedirs(os.path.join(pdz, "outputs"))
json.dump(view("vbf", "v1", [("z", 0, 0, "x")]), open(os.path.join(pdz, "outputs", "view-vbf.json"), "w"))
nowz = {"vbf": view("vbf", "v1", [("z", 0, 10, "x")])}
BV.annotate_deltas(nowz, pdz, {"generation": "gZ"})
dz_ = nowz["vbf"]["measures"][0]["delta"]
check("D10", dz_.get("pp") == -100.0 and dz_.get("dden") == 10, "0 of 0 -> 0 of 10: %s" % dz_)
def commit(v):
    b = st.begin({"s": {"path": src}}, {"name": "fixture"}); json.dump(v, open(b.output_path("view-types.json"), "w")); return st.commit(b, ["view-types.json"])
g_old = commit(view("types", "v1", [("fields", 1, 10, "t")])); time.sleep(1.1); g_new = commit(view("types", "v1", [("fields", 2, 10, "t")]))
man, d, _ = st.open_current(); tp = os.path.join(d, "outputs", "view-types.json"); open(tp, "w").write("{}")      # tamper the newest
pm, pdir = BV.prior_generation(st)
check("D5", pm is not None and pm["generation"] == g_old, "tampered %s skipped; basis %s" % (g_new, pm and pm["generation"]))
# D6/D7: ONE basis. ASTRA 9e84de620: a newer verified generation WITHOUT a progress view made the change block come from an
# older generation while delta_basis named the newer one.
st2 = G.Store(os.path.join(T, "gens2"))
PROG = {"version": R.VERSION, "scopes": {"L1": {"accepted": 20, "total": 100}}, "categories": [{"code": "C", "accepted": 20, "total": 100}]}
def commit2(views):
    b = st2.begin({"s": {"path": src}}, {"name": "fixture"})
    for n, v in views.items():
        json.dump(v, open(b.output_path("view-%s.json" % n), "w"))
    return st2.commit(b, ["view-%s.json" % n for n in views])
g_a = commit2({"progress": dict(view("progress", "MP-2", [("L1", 20, 100, "l1")]), progress=PROG)}); time.sleep(1.1)
g_b = commit2({"types": view("types", "v1", [("fields", 2, 10, "t")])})
pm6, pd6 = BV.prior_generation(st2); pp6 = BV.prior_progress(pm6, pd6)
cur6 = {"progress": view("progress", "MP-2", [("L1", 40, 100, "l1")])}; BV.annotate_deltas(cur6, pd6, pm6)
check("D6", pm6["generation"] == g_b and pp6 is None and cur6["progress"]["delta_basis"]["generation"] == g_b
      and cur6["progress"]["measures"][0]["delta"].get("na") == "no prior",
      "basis %s (no progress view) -> prior_progress %s, measure delta %s; the older %s is not used"
      % (g_b, pp6, cur6["progress"]["measures"][0]["delta"].get("na"), g_a))
time.sleep(1.1); g_c = commit2({"progress": dict(view("progress", "MP-2", [("L1", 30, 100, "l1")]), progress=PROG)})
pm7, pd7 = BV.prior_generation(st2); pp7 = BV.prior_progress(pm7, pd7)
check("D7", pm7["generation"] == g_c and pp7 is not None and pp7["generation"] == g_c and pp7["categories"] == {"C": {"accepted": 20, "total": 100}},
      "control: basis %s carries a progress view -> prior_progress from the same generation" % g_c)

# countdown
fleet = os.path.join(T, "fleet"); os.makedirs(fleet)
cfg = S.controller_config()
def state(**kw):
    json.dump(dict({"heartbeat": NOW - 30, "dashboard": {"last_run": NOW - 600, "last_rc": 0}}, **kw), open(os.path.join(fleet, "watchdog-state.json"), "w"))
state(); s1 = S.schedule(fleet, T, NOW, cfg)
src_cfg = S.controller_config(os.path.join(HERE, "..", "analysis-kit", "gfz-scripts", "swe2_watchdog.py"))
fake = os.path.join(T, "wd.py"); open(fake, "w").write("DASH_INTERVAL = 900\nPOLL_INTERVAL = 60\n")
s1b = S.schedule(fleet, T, NOW, S.controller_config(fake))
check("T1", s1["state"] == "OK" and s1["next_at"] == NOW - 600 + src_cfg["dash_interval"] and s1b["next_at"] == NOW - 600 + 900,
      "interval %s from the controller source (a 900 s configuration gives %s s left)" % (s1["interval"], round(s1b["next_at"] - NOW)))
open(os.path.join(T, "building.json"), "w").write(json.dumps({"started": NOW - 20})); s2 = S.schedule(fleet, T, NOW, cfg); os.remove(os.path.join(T, "building.json"))
check("T2", s2["state"] == "REFRESHING")
state(dashboard={"last_run": NOW - 600, "last_rc": 1}); s3 = S.schedule(fleet, T, NOW, cfg)
check("T3", s3["state"] == "FAILED" and s3["next_at"] > NOW, s3.get("why"))
state(heartbeat=NOW - 3600); s4a = S.schedule(fleet, T, NOW, cfg)
os.remove(os.path.join(fleet, "watchdog-state.json")); s4b = S.schedule(fleet, T, NOW, cfg)
state(dashboard={}); s4c = S.schedule(fleet, T, NOW, cfg)
check("T4", s4a["state"] == s4b["state"] == s4c["state"] == "UNKNOWN" and "next_at" not in s4a, "%s | %s | %s" % (s4a["why"], s4b["why"], s4c["why"]))
state(dashboard={"last_run": NOW - cfg["dash_interval"] - 3 * cfg["poll_interval"], "last_rc": 0}); s5 = S.schedule(fleet, T, NOW, cfg)
check("T5", s5["state"] == "OVERDUE", s5.get("why"))

# the page's JavaScript, executed
js = S.PAGE.split("<script>")[1].split("</script>")[0]
def grab(name):
    i = js.index("function %s(" % name); depth = 0
    for j in range(js.index("{", i), len(js)):
        depth += {"{": 1, "}": -1}.get(js[j], 0)
        if depth == 0:
            return js[i:j + 1]
prog = ("const esc=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));"
        + grab("dtip") + grab("dcol") + grab("sgn") + grab("delta") +
        "const out=[delta({direction:'up',delta:{pp:1.44,old:{numerator:1,denominator:2},new:{numerator:1,denominator:2}}}),delta({direction:'up',delta:{pp:-0.3}}),"
        "delta({delta:{pp:0}}),delta({delta:{na:'scope changed',why:'x'}}),"
        "delta({id:'register-open',direction:'down',delta:{pp:2}}),delta({direction:'down',delta:{pp:-2}}),"
        "delta({direction:'none',delta:{pp:3}}),delta({delta:{pp:3}}),delta({direction:'sideways',delta:{pp:-3}})];console.log(JSON.stringify(out));")
jp = os.path.join(T, "d.js"); open(jp, "w", encoding="utf-8").write(prog)
o = subprocess.run(["node", jp], capture_output=True, text=True)
got = json.loads(o.stdout) if o.returncode == 0 else []
plain = lambda h: h.split(">", 1)[1].rsplit("<", 1)[0] if h else ""
icons = any(ch in "".join(got) for ch in "●•▲▼↑↓⬤⚫")
check("J4", len(got) == 9 and "dneg" in got[4] and plain(got[4]) == "+2.00%" and "dpos" in got[5] and plain(got[5]) == "-2.00%"
      and all("dmut" in g and "dpos" not in g and "dneg" not in g for g in got[6:9]),
      "register-open +2 -> %s; down -2 -> %s; none/undeclared/unknown -> %s" % (
          got[4].split("'")[1] if got else "", got[5].split("'")[1] if got else "", [g.split("'")[1] for g in got[6:9]] if got else ""))
check("J1", len(got) >= 4 and "dpos" in got[0] and plain(got[0]) == "+1.44%" and "dneg" in got[1] and plain(got[1]) == "-0.30%"
      and "dz" in got[2] and plain(got[2]) == "0.00%" and "dna" in got[3] and plain(got[3]) == "new" and not icons
      and "background" not in "".join(got), "%s" % [plain(g) for g in got] if got else o.stderr[-200:])
prog5 = ("const esc=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));"
         + grab("dtip") + grab("dcol") + grab("sgn") + grab("delta") +
         "console.log(JSON.stringify([delta({direction:'up',delta:{count:12,rel:12,old:{numerator:100},new:{numerator:112}}}),"
         "delta({direction:'down',delta:{count:3,rel:null,old:{numerator:0},new:{numerator:3}}}),"
         "delta({direction:'up',delta:{na:'scope changed',why:'x',dnum:5,dden:3,old:{numerator:40,denominator:48},new:{numerator:45,denominator:51}}}),"
         "delta({direction:'up',delta:{na:'scope changed',why:'x',pp:4.902,dnum:5,dden:3,old:{numerator:40,denominator:48},new:{numerator:45,denominator:51}}})]));")
jp5 = os.path.join(T, "d5.js"); open(jp5, "w", encoding="utf-8").write(prog5)
o5 = subprocess.run(["node", jp5], capture_output=True, text=True)
g5 = json.loads(o5.stdout) if o5.returncode == 0 else []
check("J5", len(g5) == 4 and plain(g5[0]) == "+12 (+12.0%)" and "dpos" in g5[0] and plain(g5[1]) == "+3" and "dneg" in g5[1]
      and plain(g5[2]) == "new" and "dna" in g5[2] and plain(g5[3]) == "+4.90%" and "dpos" in g5[3] and " of " not in "".join(plain(g) for g in g5), "%s" % [plain(g) for g in g5] if g5 else o5.stderr[-300:])
check("J2", js.count("setInterval(") == 3 and "window.__ff12.forEach(clearInterval)" in js and "Next full refresh" in js
      and "Refreshing" in js and "Refresh failed · retry in" in js, "three intervals, cleared before re-creation")

prog3 = ("const esc=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));const DARK=false;"
         + grab("lc") + grab("split") +
         "const a={colors:{X:['#111111','#eeeeee'],Y:['#222222','#dddddd'],Z:['#333333','#cccccc']}};"
         "console.log(JSON.stringify([split('Combat & damage',['X'],a),split('Combat & damage',['X','Y'],a),split('Combat & damage',['X','Y','Z'],a),split('Combat & damage',[],a)]));")
jp3 = os.path.join(T, "s.js"); open(jp3, "w", encoding="utf-8").write(prog3)
o3 = subprocess.run(["node", jp3], capture_output=True, text=True)
sp = json.loads(o3.stdout) if o3.returncode == 0 else []
import re as _re
parts = lambda h: _re.findall(r"<span style='color:(#[0-9a-f]{6})'>([^<]*)</span>", h)
ok3 = False
if len(sp) == 4:
    p1, p2, p3 = parts(sp[0]), parts(sp[1]), parts(sp[2])
    joined = lambda ps: "".join(t for _c, t in ps).replace("&amp;", "&")
    lens = [len(t.replace("&amp;", "&")) for _c, t in p3]
    ok3 = (len(p1) == 1 and len(p2) == 2 and len(p3) == 3 and all(joined(x) == "Combat & damage" for x in (p1, p2, p3))
           and [c for c, _t in p2] == ["#111111", "#222222"] and max(lens) - min(lens) <= 1 and "<span" not in sp[3])
check("J3", ok3, "1 -> %d span, 2 -> %d, 3 -> %d (lengths %s); nobody -> neutral" % (len(parts(sp[0])), len(parts(sp[1])), len(parts(sp[2])),
      [len(t.replace("&amp;", "&")) for _c, t in parts(sp[2])]) if len(sp) == 4 else o3.stderr[-200:])

shutil.rmtree(T, ignore_errors=True)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
