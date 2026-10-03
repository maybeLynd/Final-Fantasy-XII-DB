#!/usr/bin/env python3
"""check_execution_coverage.py - controls for the execution-coverage record
(OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R, SWE2-ORACLE).

C1 seal       every file named in SEAL.json hashes to its sealed sha256, and
              the instrument files still match the sealed instrument hashes
C2 receipts   every contributing run's receipt_md5 is the md5 of the sealed
              evidence result.json it claims to have reproduced
C3 stubs      known-answer NOT-EXECUTED controls from the harnesses' own
              disclosures: commit-callees-exec BODYSTUBS 00512F30/0033C9B0
              (entry patched to ret) and auto-status-gates-exec's five
              entry-scripted bodies. v1 recorded all seven `returned`.
C4 executed   known-answer executed controls: mt-twist-simd-exec 00866B90 and
              commit-callees-exec 00808C40 (__security_check_cookie, ends in
              `bnd ret` - v1's mnemonic test missed it) are `returned`
C5 image      blocks outside the image are seen (harness RETQ/stub pages):
              v1's misparsed section table made every block "in image"
C6 aggregate  execution-coverage.tsv agrees with the per-run records: an entry
              is `yes` iff some ok run classes it executed, and run counts match

Prints one line per control and ends `FAILS N`.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
EVID = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments", "evidence")
GFZ = os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts")
EXECUTED = ("returned", "faulted", "returned+faulted")
fails = []


def check(name, ok, detail=""):
    print("%-12s %s %s" % (name, "PASS" if ok else "FAIL", detail))
    if not ok:
        fails.append(name)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run_classes(run):
    p = os.path.join(HERE, "runs", run + ".tsv")
    out = {}
    for ln in open(p).read().splitlines()[1:]:
        f = ln.split("\t")
        out[f[0].upper()] = f[1]
    return out


seal = json.load(open(os.path.join(HERE, "SEAL.json")))
bad = [rel for rel, h in seal["files"].items()
       if not os.path.exists(os.path.join(HERE, rel))
       or sha(os.path.join(HERE, rel)) != h]
inst = {"execution_coverage.py": os.path.join(GFZ, "execution_coverage.py"),
        "execcov/sitecustomize.py": os.path.join(GFZ, "execcov",
                                                 "sitecustomize.py"),
        "execcov/unicorn/__init__.py": os.path.join(GFZ, "execcov", "unicorn",
                                                    "__init__.py")}
ibad = [k for k, p in inst.items() if sha(p) != seal["instrument"][k]]
check("C1 seal", not bad and not ibad,
      "%d files, instrument %s" % (len(seal["files"]),
                                  "matches" if not ibad else "DIFFERS %s" % ibad))

recs = {}
for fn in sorted(os.listdir(os.path.join(HERE, "runs"))):
    if fn.endswith(".json"):
        r = json.load(open(os.path.join(HERE, "runs", fn)))
        recs[r["run"]] = r
ok_runs = [n for n, r in recs.items() if r["status"] == "ok"]
mism = []
for n in ok_runs:
    rp = os.path.join(EVID, n, "result.json")
    if hashlib.md5(open(rp, "rb").read()).hexdigest() != recs[n]["receipt_md5"]:
        mism.append(n)
check("C2 receipts", not mism and len(ok_runs) > 0,
      "%d ok runs of %d, %d receipt mismatches %s" % (
          len(ok_runs), len(recs), len(mism), mism[:5]))

cc = run_classes("commit-callees-exec")
asg = run_classes("auto-status-gates-exec")
stub_ctl = {("commit-callees-exec", "00512F30"): cc,
            ("commit-callees-exec", "0033C9B0"): cc}
for e in ("0031B860", "0030E130", "0030E360", "002FEF30", "0030E060"):
    stub_ctl[("auto-status-gates-exec", e)] = asg
wrong = ["%s:%s=%s" % (r, e, m.get(e)) for (r, e), m in stub_ctl.items()
         if m.get(e) in EXECUTED or m.get(e) is None]
src = open(os.path.join(EVID, "commit-callees-exec", "check.py")).read()
check("C3 stubs", not wrong and "BODYSTUBS = [SINK, MRESET" in src,
      "7 disclosed stubs NOT executed" if not wrong else "wrong %s" % wrong)

mt = run_classes("mt-twist-simd-exec")
check("C4 executed", mt.get("00866B90") == "returned"
      and cc.get("00808C40") == "returned",
      "00866B90=%s 00808C40=%s" % (mt.get("00866B90"), cc.get("00808C40")))

outside = sum(r.get("blocks_outside_image", 0) for r in recs.values())
check("C5 image", outside > 0
      and recs["commit-callees-exec"].get("blocks_outside_image", 0) > 0,
      "%d blocks outside the image across runs" % outside)

agg = {}
lines = open(os.path.join(HERE, "execution-coverage.tsv")).read().splitlines()
hdr = lines[0].split("\t")
for ln in lines[1:]:
    f = dict(zip(hdr, ln.split("\t")))
    agg[f["entry"]] = f
derived = {}
for n in ok_runs:
    for e, c in run_classes(n).items():
        d = derived.setdefault(e, [0, 0])
        d[1] += 1
        d[0] += c in EXECUTED
dis = [e for e in set(agg) | set(derived)
       if e not in agg or e not in derived
       or (agg[e]["executed"] == "yes") != (derived[e][0] > 0)
       or int(agg[e]["runs_executed"]) != derived[e][0]
       or int(agg[e]["runs_observed"]) != derived[e][1]]
nyes = sum(1 for f in agg.values() if f["executed"] == "yes")
check("C6 aggregate", not dis,
      "%d entries, %d executed, %d observed-not-executed, %d disagreements" % (
          len(agg), nyes, len(agg) - nyes, len(dis)))

print("FAILS %d" % len(fails))
sys.exit(1 if fails else 0)
