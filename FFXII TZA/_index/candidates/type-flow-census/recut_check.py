"""Generic check for a read-side re-cut of one type (OPUS, 2026-09-27).
Usage: python recut_check.py TYPE KEY=VALUE... [--fields PATH]   (keys as type_flow_census.py: CELLS / STATIC / ENTRIES / GETTERS / POOL / SHIFT / TYPE_SIZE)
Runs the census with those seeds and checks:
  P1 positive control: the census hits at least min(5, all) of the type's already-declared (non-DISCOVERED, not re-cut) rows
     (a type with none: its row starts of any status),
     and at least 95% of the recorded fields lie inside the object
  R1 every row of the type carrying this re-cut's mark is exactly a field of recut.derive's layout (offset, width, type)
  S  no re-cut offset is still DISCOVERED (FAILS on the store before the re-cut)
  S2 no DISCOVERED span of the type is still re-cuttable by the census (a re-cut gone stale after a seed change)
Writes the census rows to a temporary file; with --receipt it writes flow-<TYPE>.tsv beside this file (the tracked receipt).
A re-run for review must NOT pass --receipt: that would rewrite a tracked file in the shared tree (2026-09-27, when
review re-runs overwrote published receipts between a check and a commit).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import recut as R
args = [a for a in sys.argv[1:]]
FIELDS = os.environ.get("FIELDS_PATH") or "FFXII TZA/_types/fields.tsv"
if "--fields" in args:
    i = args.index("--fields"); FIELDS = args[i + 1]; del args[i:i + 2]
RECEIPT = "--receipt" in args
if RECEIPT: args.remove("--receipt")
TYP = args[0]; SEEDS = dict(a.split("=", 1) for a in args[1:])
MARK = "FLOW RE-CUT 2026-09-27"
import tempfile
OUTP = os.path.join(HERE, "flow-%s.tsv" % TYP) if RECEIPT else os.path.join(tempfile.mkdtemp(prefix="recut_"), "flow-%s.tsv" % TYP)
rows = R.run_census("Tools/work/exe/FFXII_TZA.exe", "Tools/work/graph/functions.tsv", OUTP, SEEDS)
print("census written to", OUTP)
size = int(SEEDS["TYPE_SIZE"], 16)
inr = [r for r in rows if 0 <= int(r["field"], 16) < size]
fails = 0


def check(name, ok, det=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, det)); fails += not ok


allrows = R.spans_of(FIELDS, TYP, only_discovered=False)
declared = {o for o, n, c in allrows if c[6] != "DISCOVERED" and MARK not in c[8]}
# a type with no declared row yet (every row DISCOVERED - StickBasis022C7FA0, 2026-09-27) has nothing else to hit: P1 then
# rests on the store's own row starts of any status, still excluding rows this re-cut made
if not declared:
    declared = {o for o, n, c in allrows if MARK not in c[8]}
hit = {int(r["field"], 16) for r in inr} & declared
# an interior type (SHIFT) sees its parent's census, whose other fields fall outside the sub-object by design: there the
# range test is void and P1 rests on the declared-row hits alone (2026-09-27)
inrange_ok = "SHIFT" in SEEDS or len(inr) >= 0.95 * len(rows)
# a type this re-cut covers WHOLE (OwnedObjectPtr022C8058, one 8-byte row) has no other row to hit; P1 then rests on
# the census reaching the object at all, entirely in range (2026-09-27)
whole = not declared and len(inr) > 0
check("P1 the seeds reach the object", (whole or len(hit) >= max(1, min(5, len(declared)))) and inrange_ok,
      "(%d of %d declared rows hit; %d of %d fields in range)" % (len(hit), len(declared), len(inr), len(rows)))
recut = [c for o, n, c in allrows if MARK in c[8] and TYP + " " in c[8]]
old = []
for c in recut:
    for part in c[8].split(" || "):
        if part.startswith("WAS SPAN "):
            o, n = part[len("WAS SPAN "):].split()[0:2]; old.append((int(o, 16), int(n), None))
lay = {f: (w, t) for o, n, cells, fl in R.derive(inr, sorted(set(old))) for f, w, t, s, wd in fl}
def _same(l, w, t):
    # a qword read cannot tell a pointer from an integer, so derive's uint64 matches a declared pointer ctype (2026-09-27)
    return l == (w, t) or (l == (8, "uint64") and w == 8 and t.strip().endswith("*"))
check("R1 every re-cut row matches the census layout", bool(recut) and all(int(c[1], 16) in lay and _same(lay[int(c[1], 16)], int(c[2]), c[4]) for c in recut), "(%d re-cut rows)" % len(recut))
check("S no re-cut offset is still DISCOVERED", bool(recut) and all(c[6] != "DISCOVERED" for c in recut))
# S2 (2026-09-27, OPUS): the census's CURRENT layout is fully applied - no DISCOVERED span of the type is still
# re-cuttable. S alone cannot see a re-cut gone stale: BootSingleton was re-cut before its GETTERS seed was added, and
# five spans the seeded census resolves stayed DISCOVERED while S passed.
stale = R.derive(inr, R.spans_of(FIELDS, TYP))
check("S2 no DISCOVERED span is still re-cuttable by the census", not stale,
      "(%d: %s)" % (len(stale), ", ".join("+0x%X/%d" % (o, n) for o, n, c, f in stale[:8])))
print("FAILS", fails); sys.exit(1 if fails else 0)
