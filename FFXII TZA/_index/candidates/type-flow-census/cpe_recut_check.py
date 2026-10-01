"""Check for the CPostEffect re-cut (OPUS, 2026-09-27). Runs type_flow_census.py with CPostEffect's seeds (cell 02EA0B70,
constructor 006FF5D0 argument 0, size 0xD40) and checks:
  P1 positive control: the census finds the established glareParam0 readers at +0x6E4 (006FA9E7, 006FAB37) and every
     field it records lies inside the 0xD40-byte object
  R1 every re-cut row in the store is exactly a field of cpe_recut.derive's layout (offset, width, type)
  S  none of the re-cut offsets is still DISCOVERED (FAILS on the store before the re-cut)
Writes the census rows to a temporary file; with --receipt, to cpe-flow-accesses.tsv beside this file (review re-runs
must not pass it: it rewrites a tracked file).
Usage: python cpe_recut_check.py [exe] [functions.tsv] [fields.tsv]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cpe_recut as R
RECEIPT = "--receipt" in sys.argv
sys.argv = [a for a in sys.argv if a != "--receipt"]
EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUN = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/graph/functions.tsv"
FIELDS = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("FIELDS_PATH") or "FFXII TZA/_types/fields.tsv"
import tempfile
OUTP = os.path.join(HERE, "cpe-flow-accesses.tsv") if RECEIPT else os.path.join(tempfile.mkdtemp(prefix="cpe_"), "cpe-flow-accesses.tsv")
rows = R.run_census(EXE, FUN, OUTP)
fails = 0


def check(name, ok, det=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, det)); fails += not ok


sites = {(r["site"], r["field"]) for r in rows}
check("P1 positive control and range", ("006FA9E7", "0x6E4") in sites and ("006FAB37", "0x6E4") in sites
      and all(0 <= int(r["field"], 16) < 0xD40 for r in rows), "(%d rows)" % len(rows))
store = {o: c for o, n, c in R.spans_of(FIELDS, only_discovered=False)}
recut = [c for o, c in store.items() if "CPOSTEFFECT FLOW RE-CUT 2026-09-27" in c[8]]
# the layout the census supports, derived from the rows' recorded old spans
old_spans = []
for c in recut:
    for part in c[8].split(" || "):
        if part.startswith("WAS SPAN "):
            o, n = part[len("WAS SPAN "):].split()[0:2]; old_spans.append((int(o, 16), int(n), None))
lay = {f: (w, t) for o, n, cells, fl in R.derive(rows, sorted(set(old_spans))) for f, w, t, s, wd in fl}
check("R1 every re-cut row matches the census layout", recut and all(int(c[1], 16) in lay and lay[int(c[1], 16)] == (int(c[2]), c[4]) for c in recut),
      "(%d re-cut rows)" % len(recut))
check("S no re-cut offset is still DISCOVERED", len(recut) > 150 and all(c[6] != "DISCOVERED" for c in recut), "(%d)" % len(recut))
print("FAILS", fails); sys.exit(1 if fails else 0)
