"""test_next_work.py - Next highest-value work (improvement addendum section 11; SWE2-FRONTIER, 2026-10-03). Fixtures only.
  N1  a task naming an open register row is BLOCKS DB_GOAL NOW and lists the row; an open row no task names is unowned
  N2  buckets follow board fields only (review, incorporation, runtime, P0/P1 tooling, P0/P1 other); P2/P3 not promoted
  N3  age never raises priority: equal priority and state order by id, whatever the updated_at
  N4  the buckets come in the addendum's order
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


# N1-N4
def task(i, st="READY", pr="P2", **kw):
    d = {"id": i, "status": st, "priority": pr, "assigned_to": "LANE", "agent": "LANE" if st == "ACTIVE" else None, "target": kw.pop("target", "t"),
         "resources": kw.pop("resources", []), "updated_at": kw.pop("updated_at", "2026-10-03T00:00:00Z")}
    d.update(kw)
    return d


tasks = [task("FIX-OV-5-ROW", target="close OV-5 with the census"), task("X-REVIEW-1", reviews={"author": "OPUS"}),
         task("AUTO-INCORP-REV-2"), task("ASTRA-RT-1", kind="runtime"), task("KIT-1", pr="P1", resources=[{"key": "file:database/tools/dashboard/x.py"}]),
         task("RES-B", pr="P1", updated_at="2026-09-01T00:00:00Z"), task("RES-A", pr="P1", updated_at="2026-10-03T00:00:00Z"),
         task("ORDINARY-P3", pr="P3"), task("DONE-1", st="DONE", target="OV-9")]
nw = BV.next_work_block({"verdict": "NOT_MET", "remaining": "OPEN=2", "next": "rows"}, tasks, ["OV-5", "OV-9"])
B = {b: items for b, items, _n in nw["buckets"]}
check("N1 row-naming task blocks DB_GOAL", [i[0] for i in B["BLOCKS DB_GOAL NOW"]] == ["FIX-OV-5-ROW"] and B["BLOCKS DB_GOAL NOW"][0][5] == ["OV-5"])
check("N1 unowned open row", nw["unowned_blockers"] == ["OV-9"], nw["unowned_blockers"])
check("N2 buckets from board fields", ([i[0] for i in B["AWAITING INDEPENDENT REVIEW"]], [i[0] for i in B["AWAITING INTEGRATION"]],
      [i[0] for i in B["RUNTIME / LIVE AUTHORIZATION NEEDED"]], [i[0] for i in B["TOOLING BLOCKER"]]) ==
      (["X-REVIEW-1"], ["AUTO-INCORP-REV-2"], ["ASTRA-RT-1"], ["KIT-1"]))
check("N2 ordinary P3 not promoted", all("ORDINARY-P3" not in [i[0] for i in items] for items in B.values()))
check("N3 age never raises priority", [i[0] for i in B["HIGH-VALUE NONBLOCKING KNOWLEDGE"]] == ["RES-A", "RES-B"], B["HIGH-VALUE NONBLOCKING KNOWLEDGE"])
check("N4 addendum order", [b for b, _i, _n in nw["buckets"]] == BV.NEXT_BUCKETS == ["BLOCKS DB_GOAL NOW", "AWAITING INDEPENDENT REVIEW",
      "AWAITING INTEGRATION", "RUNTIME / LIVE AUTHORIZATION NEEDED", "TOOLING BLOCKER", "HIGH-VALUE NONBLOCKING KNOWLEDGE", "POST-DB / DEFERRED"])

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
