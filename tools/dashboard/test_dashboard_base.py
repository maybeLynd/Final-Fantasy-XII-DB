"""test_dashboard_base.py - DB_GOAL blocking chain, Depth as a diagnostic, Source/Freshness drawer (the user's context-refresh
package v3 and improvement addendum section 1; SWE2-FRONTIER, 2026-10-03). Fixtures only.
  B1  the DB_GOAL chain is goal_gate.py's own verdict / remaining / next / detail, verbatim
  B2  Depth cannot label DB_GOAL: the title and OVERALL label say "not DB_GOAL", the view carries the diagnostic block,
      and no Depth measure claims readiness
  B3  drawer: the knowledge.sqlite check reads CURRENT only on exit 0 with no STALE line, STALE (with the tables) when
      the check names any, UNMEASURED when there is no capture; the lifecycle hash is absent until that input exists
  B4  the knowledge check is a declared, volatile, optional input
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


tmp = tempfile.mkdtemp(prefix="dashbase-test-")
T = "2026-10-03T12:00:00Z"
# B1
G = {"verdict": "NOT_MET", "remaining": "questions outstanding: OPEN=4", "next": "resolve rows", "detail": ["F=59", "terminal 0/30"]}
db = BV.db_goal_block(G)
check("B1 gate lines verbatim", (db["verdict"], db["remaining"], db["next"], db["detail"]) == ("NOT_MET", G["remaining"], G["next"], G["detail"]))
# B2
pj = os.path.join(tmp, "progress_py.json")
json.dump({"overall": 51.2, "dimensions": [{"id": "engine_explained", "weight": 0.55, "numerator": 1, "denominator": 2}]}, open(pj, "w"))
dv = BV.v_depth({"progress_py": pj, "progress.py": os.path.join(BV.GS, "progress.py")}, T)
labels = " | ".join(m["label"] for m in dv["measures"])
check("B2 depth title", "not DB_GOAL" in dv["title"] and dv.get("diagnostic", {}).get("is_not", "").startswith("DB_GOAL"), dv["title"])
check("B2 no readiness label", "not DB_GOAL" in labels and "READY" not in labels.upper(), labels)


# B3
def drawer(ktext):
    gl = os.path.join(tmp, "gitlog.txt"); open(gl, "w").write("abc1234\t2026-10-03T00:00:00Z\tX: y\n")
    sn = os.path.join(tmp, "snap.json"); json.dump({"freshness": {"state": "CURRENT", "fingerprint": "f" * 64}, "commit_id": "c1"}, open(sn, "w"))
    kc = os.path.join(tmp, "kc.txt")
    if ktext is None:
        kc = os.path.join(tmp, "absent.txt")
    else:
        open(kc, "w").write(ktext)
    inp = {"gitlog": gl, "progress_snapshot": sn, "knowledge_check": kc, "goal_gate.py": os.path.join(BV.GS, "goal_gate.py")}
    return BV.provenance_block(inp, T, {"revision": 7, "recovery_epoch": 4}, G)


p = drawer("index built x\nexit 0\n")
check("B3 CURRENT", p["knowledge"]["state"] == "CURRENT" and p["source_commit"] == "abc1234" and p["board_revision"] == 7
      and p["progress"]["state"] == "CURRENT" and p["lifecycle"] is None, p)
p = drawer("index built x\n  STALE types: changed\nexit 3\n")
check("B3 STALE names the table", p["knowledge"]["state"] == "STALE" and p["knowledge"]["stale"] == ["STALE types: changed"], p["knowledge"])
check("B3 no capture -> UNMEASURED", drawer(None)["knowledge"]["state"] == "UNMEASURED")
# B4
spec = BV.declare_inputs(tmp)["knowledge_check"]
check("B4 declared volatile optional", spec.get("volatile") is True and spec.get("required") is False)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
