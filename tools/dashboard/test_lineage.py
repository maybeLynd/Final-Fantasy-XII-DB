"""test_lineage.py - evidence lineage drilldown (improvement addendum section 6; SWE2-FRONTIER, 2026-10-03).
  S1  every system step carries present / not required / not measured / unknown / not yet available and a reason -
      never a blank; a system with no primary page is not "present"
"""
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "analysis-kit", "gfz-scripts"))
import build_views as BV  # noqa: E402

fails = 0


def check(tag, ok, text=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
    fails += (not ok)


tmp = tempfile.mkdtemp(prefix="addendum-test-")
T = "2026-10-03T12:00:00Z"


def jfile(name, obj):
    p = os.path.join(tmp, name)
    json.dump(obj, open(p, "w", encoding="utf-8"))
    return p


# S1
ALLOWED = {"present", "not required", "not measured", "unknown", "not yet available"}
for row, tag in ((["S-99", "00 x", "a system", "core", "../a.md", "../CONTRACT-a.md", ""], "with contract"), (["S-98", "00 x", "bare", "core", "", "", ""], "bare")):
    lin = BV.system_lineage(row, "MET" if tag == "with contract" else None, row[0])
    check("S1 lineage %s" % tag, len(lin) == 9 and all(st in ALLOWED and why for _s, st, why in lin)
          and (lin[0][1] == "present") == (tag == "with contract"), [x[1] for x in lin])

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
