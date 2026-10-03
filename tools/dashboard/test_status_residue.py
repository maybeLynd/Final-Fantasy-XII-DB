"""test_status_residue.py - Production system status residue view (FFXII_INDEPENDENT_CORPUS_AUDIT_FOLLOWUP_2026-10-03
section 9; SWE2-FRONTIER, 2026-10-03). Fixtures only.
  R1  no census -> UNMEASURED; a census -> status counts and the PARTIAL/REOPENED split by class, UNMAPPED first; no
      score-like measure
  R2  the view is registered (adapter, definition, directions) and its census is a declared input
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


# R1 / R2
inp = {"status_residue": os.path.join(tmp, "absent.json"), "check_status_residue.py": ""}
check("R1 absent -> UNMEASURED", BV.v_residue(inp, T)["status"] == "UNMEASURED" and BV.v_residue(inp, T)["measures"] == [])
cen = {"db": "x", "counts": {"AUDITED": 10, "DOCUMENTED": 5, "PARTIAL": 2, "REOPENED": 1},
       "pages": [{"page": "b.md", "status": "PARTIAL", "class": "LIVE-ROW", "rows": {"OV-1": "PARTIAL"}, "line": "PARTIAL - OV-1"},
                 {"page": "c.md", "status": "REOPENED", "class": "PROCESS-ONLY", "rows": {}, "line": "REOPENED - review pending"},
                 {"page": "a.md", "status": "PARTIAL", "class": "UNMAPPED", "rows": {"SD-1": "ANSWERED"}, "line": "PARTIAL - SD-1"},
                 {"page": "z.md", "status": "AUDITED", "class": None, "rows": {}, "line": "AUDITED"}]}
v = BV.v_residue({"status_residue": jfile("res.json", cen), "check_status_residue.py": ""}, T)
mm = {m["id"]: (m["numerator"], m["denominator"]) for m in v["measures"]}
check("R1 status counts", (mm["st-audited"], mm["st-partial"], mm["st-reopened"]) == ((10, 18), (2, 18), (1, 18)), mm)
check("R1 class split", (mm["cls-live-row"], mm["cls-process-only"], mm["cls-unmapped"]) == ((1, 3), (1, 3), (1, 3)), mm)
check("R1 UNMAPPED first, only PARTIAL/REOPENED rows", [r_[0] for r_ in v["rows"]["data"]] == ["a.md", "c.md", "b.md"])
check("R1 no score-like measure", not any(k in m for m in mm for k in ("overall", "score", "percent")))
check("R2 registered", "residue" in BV.ADAPTERS and BV.DEFINITIONS.get("residue") and set(BV.DIRECTIONS["residue"]) >= set(mm)
      and BV.declare_inputs(tmp)["status_residue"]["path"].endswith("status_residue.json"))


print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
