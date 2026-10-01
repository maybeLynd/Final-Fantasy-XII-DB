"""test_build_views.py - the dashboard build over the real database, into a scratch store (OPUS, 2026-09-29; M3 / A19).

  B1  a build commits one generation with all seven required views, each schema-valid (server.check_view) and none FAILED
  B2  an adapter that raises yields a FAILED view carrying the reason - committed, never dropped or zeroed
  B3  a live source edited while the adapters run -> the commit is refused, CURRENT keeps the previous generation, and
      FAILURE.json names the moved input (adapters read the snapshots; the commit re-fingerprints the live sources)
  B5  the executable view's byte classes tile .text exactly, its population equals uc1_band.apply's, and the image is external
  B6  package checks on a fixture: a review item whose linked task is DONE -> LINK-DONE; an accepted item with an open
      linked task -> FALSE-COMPLETE (A02); a package stage that is not its earliest item stage -> STAGE-MISMATCH
  B4  the served views come from that CURRENT: server.State reports the same generation id
  B7  every overview, executable and progress measure of the build declares a direction (up / down / none); register-open
      and pkg-false-complete are "down"; a measure added without a declaration is reported (FABLE's colour rule)
  B8  bytes-overlap counts UNIQUE bytes in two or more population bodies (ASTRA 0d9d9330c): population_cover on disjoint,
      double and triple fixtures and on ASTRA's three real extents 0032E020/0032E030/0032E040 agrees with an independent
      sweep, while the pre-repair formula (sum of the seen flags) over-counts the triple cases; the real build's measure
      equals the sweep over the real population (v4 extents), and the executable view's definition is v4
  B9  a prior generation whose executable view is v1 (overlap 1759) gives bytes-overlap no numeric delta against v4: the
      delta is "N/A - definition changed" and still shows both sides (annotate_deltas' own path)
  B11 the chained-tails extent rule (v4): without the errata extents the same image has >= 16,156 more UNKNOWN bytes, and
      the measures' instrument names the entries grown and the bytes added (a visible denominator change, not a silent one)
  B10 the helper text_intervals calls is bound (ASTRA c7bd09b49): the committed manifest names input uc1_band.py at the
      path of the module actually imported, with that file's sha256; the same helper edited mid-build (a scratch copy the
      input points at) refuses the commit, naming uc1_band.py, and CURRENT keeps the previous generation
  B12 the evidence view is the Evidence & lessons page (definition v3): it carries `page`, its title, the six review
      measure ids unchanged, and all five sections built (none FAILED)
  B13 the question register's status counts equal check_questions.read_table over the same snapshot bytes, and the counts
      the gate printed in that generation (unless the view says the register moved between the two)
  B14 the lessons ledger has exactly one row per CONTRADICTIONS.tsv data row, in order, as contradiction_index.read_ledger
  B15 a failing or erroring checker never reads PASS: run_checks.run_one on exit 1 / crash / silence / exit 3 / timeout /
      a failure marker, classify_captured on INCONSISTENT / empty / crashed / exit-2 gate output, and every run card
      UNMEASURED when the build's check run left no record
It reads the live database read-only; B3 edits only a scratch COPY of one input, pointed at by patching the input table.
"""
import json, os, shutil, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "analysis-kit", "gfz-scripts"))
import build_views as BV  # noqa: E402
import generation as G  # noqa: E402
import server as S  # noqa: E402
fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
T = tempfile.mkdtemp(prefix="bv_"); root = os.path.join(T, "store")
g1 = BV.main(["--root", root])
st = G.Store(root); man, d, probs = st.open_current()
views = {o[5:-5]: json.load(open(os.path.join(d, "outputs", o), encoding="utf-8")) for o in man["outputs"]}
VOC = S.load_vocabulary()
bad = {n: S.check_view(v, VOC) for n, v in views.items() if S.check_view(v, VOC)}
check("B1", not probs and set(S.REQUIRED) <= set(views) == set(BV.ADAPTERS) and not bad and all(v["status"] != "FAILED" for v in views.values()),
      "views %s; malformed %s" % ({n: v["status"] for n, v in views.items()}, bad))
orig = BV.ADAPTERS["types"]
def boom(inp, t): raise RuntimeError("injected adapter failure")
BV.ADAPTERS["types"] = boom
g2 = BV.main(["--root", root]); BV.ADAPTERS["types"] = orig
m2, d2, p2 = st.open_current(); vt = json.load(open(os.path.join(d2, "outputs", "view-types.json"), encoding="utf-8"))
check("B2", g2 != g1 and not p2 and vt["status"] == "FAILED" and "injected adapter failure" in vt["source"]["limits"] and not S.check_view(vt, VOC),
      vt["source"]["limits"])
# B3: point one input at a scratch copy, and edit that copy from inside an adapter (mid-build)
copy = os.path.join(T, "L2-VERDICTS.md"); shutil.copyfile(os.path.join(BV.DB, "_index", "L2-VERDICTS.md"), copy)
real_decl = BV.declare_inputs
def redirected(cap):
    d = real_decl(cap); d["l2"] = {"path": copy}; return d
BV.declare_inputs = redirected
def edit_live(inp, t):
    open(copy, "a", encoding="utf-8").write("\n<!-- edited mid-build -->\n"); return orig(inp, t)
BV.ADAPTERS["types"] = edit_live
try:
    BV.main(["--root", root]); refused = None
except G.GenerationError as e:
    refused = str(e)
BV.declare_inputs = real_decl; BV.ADAPTERS["types"] = orig
fail = json.load(open(os.path.join(root, G.FAILURE), encoding="utf-8")) if os.path.exists(os.path.join(root, G.FAILURE)) else {}
check("B3", refused and "inputs moved" in refused and "l2" in refused and st.current_id() == g2 and fail.get("current_unchanged") == g2, refused)
s = S.State(root).status()
check("B4", s["generation"] == g2 and not s["problems"], "served %s" % s["generation"])
import uc1_band  # noqa: E402
mv, dv, _ = st.open_current(); ex = json.load(open(os.path.join(dv, "outputs", "view-executable.json"), encoding="utf-8"))
mm = {m["id"]: m for m in ex["measures"]}
N = mm["bytes-listed"]["denominator"]
parts = sum(mm["bytes-" + k]["numerator"] for k in ("listed", "frontier", "funclet", "held", "fill", "unknown"))
def _rows():
    for i, line in enumerate(open(os.path.join(BV.TOOLS, "work", "graph", "functions.tsv"), encoding="utf-8", errors="replace")):
        p = line.rstrip("\n").split("\t")
        if i and len(p) > 2 and not p[1].startswith(("Unwind@", "Catch_All@")):
            yield int(p[0], 16), int(p[2])
live = uc1_band.apply(dict(_rows()))[1]
check("B5", parts == N and mm["population"]["numerator"] == live["total"] and 0 < mm["bytes-unknown"]["numerator"] < N and mv["inputs"]["exe"].get("external"),
      ".text %d bytes = sum of classes %d; population %d (uc1_band %d); image external (hashed, not copied)" % (N, parts, mm["population"]["numerator"], live["total"]))
PK = os.path.join(T, "pk"); os.makedirs(PK)
open(os.path.join(PK, "PKG-FIX.md"), "w", encoding="utf-8").write(
    "**stage.** `review` (fixture).\n\n**work items.**\n\n| item | claim | kind | locator | owner | reviewer | stage |\n|---|---|---|---|---|---|---|\n"
    "| F1 | a | claim | x | FABLE | AUDIT-SEM | review (TASK-DONE-ONE) |\n"
    "| F2 | b | claim | x | FABLE | AUDIT-SEM | accepted-and-incorporated (TASK-OPEN-TWO) |\n"
    "| F3 | c | gap | x | FABLE | AUDIT-SEM | research |\n")
fake = {"TASK-DONE-ONE": {"status": "DONE"}, "TASK-OPEN-TWO": {"status": "READY"}}
pc = BV.package_checks(PK, fake)[0]; fl = {i["item"]: i["flags"] for i in pc["items"]}
check("B6", fl == {"F1": ["LINK-DONE"], "F2": ["FALSE-COMPLETE"], "F3": []} and pc["flags"] == ["STAGE-MISMATCH"] and pc["earliest"] == "research",
      "items %s; package %s (recorded review, earliest research)" % (fl, pc["flags"]))
und = BV.undeclared(views)
dirs = {(n, m["id"]): m.get("direction") for n, v in views.items() for m in v.get("measures", [])}
fake_new = BV.undeclared({"overview": {"measures": [{"id": "register-open"}, {"id": "a-new-count"}]}})
check("B7", not und and all(dv in ("up", "down", "none") for dv in dirs.values()) and dirs.get(("overview", "register-open")) == "down"
      and dirs.get(("overview", "pkg-false-complete")) == "down" and dirs.get(("progress", "union")) == "up"
      and dirs.get(("executable", "bytes-listed")) == "none" and fake_new == [("overview", "a-new-count")],
      "undeclared in this build %s; an added measure is caught %s" % (und, fake_new))
def sweep(spans):                      # independent: unique bytes at depth >= 2 and additional covers, from sorted events
    ev = sorted([(a, 1) for a, b in spans] + [(b, -1) for a, b in spans])
    uniq = extra = d = 0; last = None
    for x, k in ev:
        if last is not None and x > last and d >= 2:
            uniq += x - last; extra += (x - last) * (d - 1)
        d += k; last = x
    return uniq, extra
def old_formula(pop, lo, n):           # the pre-repair counting, kept only as the counterexample
    seen = bytearray(n); o = 0
    for e, z in pop.items():
        a, b = max(e - lo, 0), min(e + z - lo, n)
        if a < b: o += sum(seen[a:b]); seen[a:b] = b"\x01" * (b - a)
    return o
fx = {"disjoint": {0: 8, 16: 8}, "double": {0: 16, 8: 16}, "triple": {0: 16, 8: 16, 12: 8},
      "astra-real": {0x0032E020 - 0x0032E000: 0x21, 0x0032E030 - 0x0032E000: 0x21, 0x0032E040 - 0x0032E000: 0x26}}
res = {}
for k, pop in fx.items():
    _c, ov, ex_ = BV.population_cover(pop, set(), 0, 128)
    res[k] = (ov, ex_, sweep([(a, a + z) for a, z in pop.items()]), old_formula(pop, 0, 128))
fx_ok = all(r[:2] == r[2] for r in res.values()) and res["disjoint"][0] == 0 and res["double"][0] == 8 and res["triple"][0] == 12     and res["astra-real"][0] == 0x21 and res["triple"][3] > 12 and res["astra-real"][3] == 0x22
lo = int(mm["bytes-listed"]["scope"].split()[1].split("..")[0], 16)
rpop = uc1_band.apply_extents(uc1_band.apply(dict(_rows()))[0])[0]
rs = sweep([(max(e, lo), min(e + z, lo + N)) for e, z in rpop.items() if max(e, lo) < min(e + z, lo + N)])
check("B8", fx_ok and mm["bytes-overlap"]["numerator"] == rs[0] and ex["definition"] == "v4" and old_formula(rpop, lo, N) > rs[0],
      "fixtures (unique, extra, sweep, pre-repair) %s; real: measure %d, sweep %s, pre-repair %d; definition %s"
      % (res, mm["bytes-overlap"]["numerator"], rs, old_formula(rpop, lo, N), ex["definition"]))
PD = os.path.join(T, "prior"); os.makedirs(os.path.join(PD, "outputs"))
pv = json.loads(json.dumps(ex)); pv["definition"] = "v1"
for m in pv["measures"]:
    if m["id"] == "bytes-overlap": m["numerator"] = 1759
json.dump(pv, open(os.path.join(PD, "outputs", "view-executable.json"), "w", encoding="utf-8"))
cur = {"executable": json.loads(json.dumps(ex))}
BV.annotate_deltas(cur, PD, {"generation": "g-prior-v1"})
dl = {m["id"]: m["delta"] for m in cur["executable"]["measures"] if "delta" in m}["bytes-overlap"]
check("B9", dl.get("na") == "N/A - definition changed" and "pp" not in dl and dl["old"]["numerator"] == 1759 and dl["new"]["numerator"] == mm["bytes-overlap"]["numerator"], dl)
# B11 the chained-tails extent rule (definition v4): the same image without the errata extents (v3) has more UNKNOWN bytes -
# at least the ruling's 16,156 chained-tail bytes - and the view names how many entries grew by how many bytes
v3 = BV.text_intervals(os.path.join(BV.TOOLS, "work", "graph", "functions.tsv"), uc1_band.BAND_TSVS, os.path.join(BV.TOOLS, "work", "exe", "FFXII_TZA.exe"))
moved = v3["bytes"]["unknown"] - mm["bytes-unknown"]["numerator"]
xin = uc1_band.apply_extents(uc1_band.apply(dict(_rows()))[0])[1]
check("B11", moved >= 16156 and xin["grown"] >= 270 and "grown by %d bytes" % xin["bytes_added"] in mm["bytes-unknown"]["instrument"],
      "unknown bytes v3 %d -> v4 %d (%d moved); %s" % (v3["bytes"]["unknown"], mm["bytes-unknown"]["numerator"], moved, uc1_band.describe_extents(xin)))
mc = st.open_current()[0]; ub = mc["inputs"].get("uc1_band.py") or {}
bound = os.path.normcase(ub.get("path") or "") == os.path.normcase(os.path.abspath(uc1_band.__file__)) and ub.get("sha256") == G.sha256_file(uc1_band.__file__)
hcopy = os.path.join(T, "uc1_band.py"); shutil.copyfile(uc1_band.__file__, hcopy)
def redirected_h(cap):
    d = real_decl(cap); d["uc1_band.py"] = {"path": hcopy}; return d
def edit_helper(inp, t):
    open(hcopy, "a", encoding="utf-8").write("\n# edited mid-build\n"); return orig(inp, t)
before = st.current_id()
BV.declare_inputs = redirected_h; BV.ADAPTERS["types"] = edit_helper
try:
    BV.main(["--root", root]); refused_h = None
except G.GenerationError as e:
    refused_h = str(e)
BV.declare_inputs = real_decl; BV.ADAPTERS["types"] = orig
check("B10", bound and refused_h and "inputs moved" in refused_h and "uc1_band.py" in refused_h and st.current_id() == before,
      "bound %s (%s); edited helper -> %s" % (bound, ub.get("sha256", "")[:12], refused_h))
# B12-B15: the Evidence & lessons tab (definition v3), over the first build (g1) of this run
import collections, io, subprocess  # noqa: E402
import check_questions as CQ  # noqa: E402
import contradiction_index as CI  # noqa: E402
import run_checks as RCK  # noqa: E402
dg1 = os.path.join(root, g1)
evv = json.load(open(os.path.join(dg1, "outputs", "view-evidence.json"), encoding="utf-8"))
E = evv.get("evidence") or {}
OLD = {"reviews-done", "reviews-structured", "reviews-accepted", "receipts-intact", "receipts-publishable", "pending-propagation"}
ids = {m["id"] for m in evv.get("measures", [])}
check("B12", evv.get("page") == "evidence" and OLD <= ids and evv.get("definition") == BV.DEFINITIONS["evidence"] == "v3"
      and evv.get("title") == "Evidence & lessons" and os.path.isfile(os.path.join(HERE, "pages", "evidence.html"))
      and all(k in E and not (E[k] or {}).get("failed") for k in ("lessons", "findings", "checks", "formats", "register")),
      "page %s; definition %s; old measures missing %s; sections %s" % (evv.get("page"), evv.get("definition"), sorted(OLD - ids),
      {k: ("FAILED " + E[k]["failed"]) if (E.get(k) or {}).get("failed") else "ok" for k in E}))
# B13: the register's status counts are check_questions' own: read_table over the SAME snapshot bytes, and the counts the
# gate printed in this generation (unless the view itself says the register moved between the two)
QD = os.path.join(T, "qdb"); os.makedirs(os.path.join(QD, "_index"))
shutil.copyfile(G.input_file(dg1, "register"), os.path.join(QD, "_index", "OPEN-QUESTIONS.md"))
tab, _d = CQ.read_table(QD)
reg = E.get("register") or {}
want = dict(collections.Counter(tab.values()))
printed = {k: v for k, v in (reg.get("gate_counts") or {}).items() if k != "rows"}
check("B13", reg.get("counts") == want and reg.get("total") == len(tab) == len(reg.get("rows", []))
      and (reg.get("gate_agrees") and all(want.get(k, 0) == v for k, v in printed.items()) or bool(reg.get("note"))),
      "view %s; check_questions.read_table %s; gate printed %s (agrees %s)" % (reg.get("counts"), want, reg.get("gate_counts"), reg.get("gate_agrees")))
# B14: the lessons ledger has one row per CONTRADICTIONS.tsv data row (comments and the header excluded), and the ledger
# tool's own reader agrees
csnap = G.input_file(dg1, "contradictions")
data_rows = [l for l in io.open(csnap, encoding="utf-8").read().replace("\r\n", "\n").split("\n") if l.strip() and not l.startswith("#")][1:]
les = E.get("lessons") or {}
check("B14", len(les.get("rows", [])) == len(data_rows) == len(CI.read_ledger(csnap)) == les.get("kpis", {}).get("recorded")
      and len(data_rows) > 0 and [r["id"] for r in les["rows"]] == [l.split("\t")[0] for l in data_rows],
      "ledger rows %d; data rows %d; contradiction_index.read_ledger %d" % (len(les.get("rows", [])), len(data_rows), len(CI.read_ledger(csnap))))
# B15: a failing or erroring checker is FAIL / UNMEASURED, never PASS - through run_checks.run_one on real processes, the
# captured-instrument classifier, and the view when the check run left no record
FX = os.path.join(T, "fx"); os.makedirs(FX)
def fx(name, body):
    p = os.path.join(FX, name); open(p, "w", encoding="utf-8").write(body); return {"id": name, "script": p, "args": [], "keys": [("n", r"n=(\d+)")]}
cases = {"exit1": (fx("exit1.py", "print('n=3 findings')\nraise SystemExit(1)\n"), "FAIL"),
         "crash": (fx("crash.py", "print('n=1')\nraise RuntimeError('boom')\n"), "UNMEASURED"),
         "silent": (fx("silent.py", "pass\n"), "UNMEASURED"),
         "exit3": (fx("exit3.py", "print('n=1')\nraise SystemExit(3)\n"), "UNMEASURED"),
         "slow": (fx("slow.py", "import time\ntime.sleep(30)\n"), "UNMEASURED"),
         "marker": (dict(fx("marker.py", "print('n=2')\nprint('FAILS 2')\n"), fail=r"^FAILS [1-9]"), "FAIL"),
         "clean": (fx("clean.py", "print('n=7 all good')\n"), "PASS")}
got = {k: RCK.run_one(s, FX, timeout=3) for k, (s, _w) in cases.items()}
runs_ok = all(got[k]["status"] == w for k, (_s, w) in cases.items()) and got["clean"]["numbers"] == [["n", 7]] and got["crash"]["numbers"] == [["n", None]]
cap = {"cq-inconsistent": BV.classify_captured("check_questions", "QUESTION LEDGER  (_index/OPEN-QUESTIONS.md)\n   rows: 3\nQUESTION LEDGER INCONSISTENT: 2 item(s)\n", 0),
       "cq-empty": BV.classify_captured("check_questions", "", 0),
       "gg-garbage": BV.classify_captured("goal_gate", "Traceback (most recent call last):\n  boom", 2),
       "gg-exit2": BV.classify_captured("goal_gate", '{"verdict": "MET"}', 2),
       "gg-notmet": BV.classify_captured("goal_gate", '{"verdict": "NOT_MET", "remaining": "x"}', 1),
       "pc-stale": BV.classify_captured("progress_check", "STALE: generated x, fp a vs current b\n", 1)}
cap_ok = [cap[k][0] for k in ("cq-inconsistent", "cq-empty", "gg-garbage", "gg-exit2", "gg-notmet", "pc-stale")] == ["FAIL", "UNMEASURED", "UNMEASURED", "UNMEASURED", "FAIL", "FAIL"]
noinp = dict((n, G.input_file(dg1, n)) for n in ("goal_gate", "check_questions", "progress_check", "gate_baseline"))
noinp["checks"] = os.path.join(T, "no-such-checks.json"); noinp["instruments"] = None
nv = BV.ev_checks(noinp)
run_cards = [c for c in nv["cards"] if c.get("captured") == "run at this build"]
none_ok = len(run_cards) == len(RCK.CHECKS) and all(c["status"] == "UNMEASURED" and all(v is None for _k, v in c["numbers"]) for c in run_cards)
check("B15", runs_ok and cap_ok and none_ok,
      "run_one %s; captured %s; no check record -> %s" % ({k: (g["status"], g["reason"][:40]) for k, g in got.items()}, {k: v[0] for k, v in cap.items()},
                                                          collections.Counter(c["status"] for c in run_cards)))
shutil.rmtree(T, ignore_errors=True)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
