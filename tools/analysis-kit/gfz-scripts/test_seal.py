"""test_seal.py - seal.py against the six defect shapes FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING names, plus the valid
path (OPUS, 2026-09-29; matrix A04). Disposable fixtures; the CLI is exercised as a subprocess.

  V   a valid run seals; verify and publishable are clean; sealing identical content again returns the same run_id
  S1  shared-result overwrite: another run rewrites the shared result.json -> the first receipt still verifies from its
      sealed copy, the live path reads MOVED, and the second run gets a different run_id
  S2  missing case: the result lacks a declared case -> not publishable
  S3  truncated driver: the driver cut mid-function at a point that STILL PARSES -> not publishable (not a committed
      source); parsing alone would have passed it
  S4  changed input, same count: the same number of cases over a changed input -> a new run_id; the old receipt unchanged
  S5  interrupted publication: a crash leaves a .partial directory -> no receipt appears under the run_id, and a later
      seal of the same content succeeds
  S6  valid cumulative reuse: a new receipt crediting cases from an earlier publishable receipt -> publishable; crediting
      a case the source lacks, a case twice, or a case from a WIP source -> refused
  W   a WIP draft is sealed but never publishable (no execution credit)
  T   a stored copy tampered after sealing -> verify reports it
  C   CLI: `publishable` exits 0 on V and 1 on S2
  R1  a stored result edited and its sha256 re-stamped in RECEIPT.json -> verify reports that the run id does not derive
  R2  a hand-set `committed` flag on an uncommitted driver -> publishable still refuses it
"""
import json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import seal as SL  # noqa: E402
fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
T = tempfile.mkdtemp(prefix="seal_"); W = os.path.join(T, "work"); os.makedirs(W); store = os.path.join(T, "receipts")
def w(n, s): p = os.path.join(W, n); open(p, "w", encoding="utf-8").write(s); return p
drv = w("driver.py", "import json\ndef run(x):\n    return x * 2\nprint(json.dumps(run(1)))\n")
G = lambda *a: subprocess.run(["git", "-C", W] + list(a), capture_output=True, text=True)
G("init", "-q"); G("config", "user.email", "f@x"); G("config", "user.name", "fixture"); G("config", "commit.gpgsign", "false")
G("add", "driver.py"); G("commit", "-qm", "driver")          # the driver is a committed source
inp = w("input.bin", "input-v1")
res = w("result.json", json.dumps({"cases": {"c1": 1, "c2": 2, "c3": 3}}))
ENV = {"python": "fixture"}
r1 = SL.seal(store, [drv], [inp], res, ["c1", "c2", "c3"], "fixture limits", ENV)
check("V", not SL.verify(store, r1) and not SL.publishable(store, r1) and SL.seal(store, [drv], [inp], res, ["c1", "c2", "c3"], "fixture limits", ENV) == r1,
      "sealed %s; re-seal returns the same id" % r1)
w("result.json", json.dumps({"cases": {"c1": 1, "c2": 2, "c3": 4}}))
r2 = SL.seal(store, [drv], [inp], res, ["c1", "c2", "c3"], "second run", ENV)
mv = SL.verify(store, r1, live={"result": res})
check("S1", r2 != r1 and not SL.verify(store, r1) and any(p.startswith("MOVED") for p in mv) and not SL.publishable(store, r1),
      "old %s intact, live result MOVED; new run %s" % (r1, r2))
w("result.json", json.dumps({"cases": {"c1": 1, "c2": 2}}))
r3 = SL.seal(store, [drv], [inp], res, ["c1", "c2", "c3"], "missing case", ENV)
p3 = SL.publishable(store, r3)
check("S2", any("case map mismatch" in p and "c3" in p for p in p3), "; ".join(p3))
w("result.json", json.dumps({"cases": {"c1": 1, "c2": 2, "c3": 3}}))
trunc = w("driver_cut.py", open(drv).read()[:30])
r4 = SL.seal(store, {"driver.py": trunc}, [inp], res, ["c1", "c2", "c3"], "truncated", ENV)
p4 = SL.publishable(store, r4)
import ast as _ast; _ast.parse(open(trunc).read())          # the cut really does parse
check("S3", r4 != r1 and any("not a committed source" in p for p in p4), "; ".join(p4))
w("input.bin", "input-v2")
r5 = SL.seal(store, [drv], [inp], res, ["c1", "c2", "c3"], "changed input", ENV)
check("S4", r5 != r1 and len(SL.load(store, r5)["cases"]) == len(SL.load(store, r1)["cases"]) and not SL.verify(store, r1) and not SL.publishable(store, r5),
      "same 3 cases, new id %s; %s untouched" % (r5, r1))
w("input.bin", "input-v3")
orig_copy = SL.shutil.copyfile
calls = {"n": 0}
def crash_copy(a, b):
    calls["n"] += 1
    if calls["n"] == 2: raise KeyboardInterrupt("crash mid-seal")
    return orig_copy(a, b)
SL.shutil.copyfile = crash_copy
try:
    SL.seal(store, [drv], [inp], res, ["c1", "c2", "c3"], "interrupted", ENV); crashed = False
except KeyboardInterrupt:
    crashed = True
SL.shutil.copyfile = orig_copy
partials = [x for x in os.listdir(store) if x.endswith(".partial")]
visible = [x for x in os.listdir(store) if not x.startswith(".")]
r6 = SL.seal(store, [drv], [inp], res, ["c1", "c2", "c3"], "interrupted", ENV)
check("S5", crashed and partials and r6 not in visible and not SL.publishable(store, r6), "partial %s left invisible; re-seal gives %s" % (partials[:1], r6))
w("result.json", json.dumps({"cases": {"c4": 4}}))
r7 = SL.seal(store, [drv], [inp], res, ["c1", "c4"], "cumulative", ENV, case_sources={"c1": r1})
bad_src = SL.seal(store, [drv], [inp], res, ["c9", "c4"], "cumulative bad", ENV, case_sources={"c9": r1})
wip = SL.seal(store, [drv], [inp], w("r_wip.json", json.dumps({"cases": {"c5": 5}})), ["c5"], "draft", ENV, wip=True)
from_wip = SL.seal(store, [drv], [inp], res, ["c5", "c4"], "from wip", ENV, case_sources={"c5": wip})
p7, pb, pw = SL.publishable(store, r7), SL.publishable(store, bad_src), SL.publishable(store, from_wip)
twice = SL.publishable(store, r7, _seen={"c1"})
check("S6", not p7 and any("does not carry" in p for p in pb) and any("not publishable" in p for p in pw) and any("credited twice" in p for p in twice),
      "valid reuse ok; missing source case / WIP source / double credit refused")
check("W", wip.startswith("wip-") and not SL.verify(store, wip) and any("WIP" in p for p in SL.publishable(store, wip)))
sp = os.path.join(store, r1, "drivers", "driver.py"); keep = open(sp, "rb").read(); open(sp, "ab").write(b"# edit\n")
tv = SL.verify(store, r1); open(sp, "wb").write(keep)
check("T", any("does not match" in p for p in tv), "; ".join(tv))
cli = lambda *a: subprocess.run([sys.executable, os.path.join(HERE, "seal.py")] + list(a), capture_output=True, text=True).returncode
check("C", cli("publishable", store, r1) == 0 and cli("publishable", store, r3) == 1)
# F (2026-09-29): the house harness's FLAT case map {id: {record}} is a case list (all three EXP-201 receipts were refused
# as "no cases" before); the exact-case rule still refuses an extra case, and a flat dict with a non-record value is no case map
fr = w("flat.json", json.dumps({"k1": {"ok": True}, "k2": {"ok": False}}))
rf = SL.seal(store, [drv], [inp], fr, ["k1", "k2"], "flat map", ENV)
fx = w("flat_extra.json", json.dumps({"k1": {"ok": True}, "k2": {"ok": False}, "k9": {"ok": True}}))
rx = SL.seal(store, [drv], [inp], fx, ["k1", "k2"], "flat map, extra case", ENV)
fn = w("flat_scalar.json", json.dumps({"k1": {"ok": True}, "k2": 3}))
rn = SL.seal(store, [drv], [inp], fn, ["k1", "k2"], "not a case map", ENV)
check("F", not SL.publishable(store, rf) and SL.publishable(store, rx) and any("parseable case list" in p for p in SL.publishable(store, rn)),
      "flat map publishable; extra case -> %s; scalar value -> %s" % (SL.publishable(store, rx)[:1], SL.publishable(store, rn)[:1]))
# R1/R2 (2026-09-30, AUDITSPEC-REQ-OPUS-SEAL-RUNID-REDERIVE-0929, the reviewer's mutants M2a/M2b): the run id is
# re-derived from the receipt's content, and `committed` is re-checked against the stored copy, not trusted
rm = SL.seal(store, [drv], [inp], w("r1.json", json.dumps({"cases": {"c1": 1}})), ["c1"], "mutant base", ENV)
rd = os.path.join(store, rm)
open(os.path.join(rd, "result"), "w", encoding="utf-8").write(json.dumps({"cases": {"c1": 99}}))
rec = json.load(open(os.path.join(rd, "RECEIPT.json"), encoding="utf-8"))
rec["result"]["sha256"] = SL.sha(os.path.join(rd, "result")); rec["result"]["size"] = os.path.getsize(os.path.join(rd, "result"))
json.dump(rec, open(os.path.join(rd, "RECEIPT.json"), "w", encoding="utf-8"), indent=1, sort_keys=True)
v1 = SL.verify(store, rm)
check("R1", any("does not derive" in p for p in v1) and SL.publishable(store, rm), "; ".join(v1))
rec4 = json.load(open(os.path.join(store, r4, "RECEIPT.json"), encoding="utf-8"))
for v in rec4["drivers"].values():
    v["committed"] = True
json.dump(rec4, open(os.path.join(store, r4, "RECEIPT.json"), "w", encoding="utf-8"), indent=1, sort_keys=True)
p4b = SL.publishable(store, r4)
check("R2", any("not a committed source" in p for p in p4b), "; ".join(p4b))
shutil.rmtree(T, ignore_errors=True)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
