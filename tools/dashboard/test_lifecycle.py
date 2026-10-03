"""test_lifecycle.py - the dashboard's lifecycle semantics (DASHBOARD-MEANINGS.md section 6;
FABLE-REQ-FRONTIER-DASHBOARD-LIFECYCLE-1003; SWE2-FRONTIER, 2026-10-03). Focused: only the new semantics.
  L1  the phase is READ from PROJECT-LIFECYCLE.json: a MET gate with every requirement ready leaves DATABASE as
      DATABASE IN PROGRESS and only adds the note that the user must authorize; the six phases keep their order and the
      transition chain names user authorization
  L2  parity pilots and board state never set the phase: lifecycle_block takes no parity or board input, and a gate
      detail claiming every pilot certified changes nothing
  L3  no view reaches RECONSTRUCTION AUTHORIZED on its own: against the real lifecycle file, a MET + ready gate still
      shows the file's phase; a file that declares a later phase while DB_GOAL is NOT_MET shows both and the disagreement,
      never the later phase as current (meanings 6.1 rule 3)
  L4  lifecycle source drift -> STALE: the input is declared strict (not volatile), and a generation that snapshotted it
      reports it in drift() once the live file changes
  L5  Depth cannot label DB_GOAL: the Depth view's title and OVERALL label say "not DB_GOAL", it carries the diagnostic
      block, and no Depth measure claims readiness
  L6  the original game is evidence/oracle, never the production backend; wrapper / delegation shapes are listed as not
      reconstruction
  L7  fail closed: a missing, malformed or unknown-phase lifecycle file gives a FAILED panel, never a default phase
  L8  the DB_GOAL chain is the gate's own remaining / next / detail lines, verbatim
  L9  dashboard labels vs DASHBOARD-MEANINGS.md section 6: the phase labels equal the 6.1 axis in order, the probe label,
      the Depth diagnostic, the remaining/next/detail chain and ORIGINAL-BINARY DELEGATION wording
"""
import json, os, shutil, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "analysis-kit", "gfz-scripts"))
import build_views as BV  # noqa: E402
import generation as G  # noqa: E402

REAL = os.path.join(BV.DB, "_index", "workflow", "PROJECT-LIFECYCLE.json")
fails = 0


def check(tag, ok, text=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
    fails += (not ok)


tmp = tempfile.mkdtemp(prefix="lifecycle-test-")


def fixture(phase="DATABASE", drop=None, raw=None):
    p = os.path.join(tmp, "lc-%s-%s.json" % (phase, drop))
    if raw is not None:
        open(p, "w", encoding="utf-8").write(raw); return p
    d = json.load(open(REAL, encoding="utf-8"))
    d["current_primary_phase"] = phase
    if drop:
        d.pop(drop)
    json.dump(d, open(p, "w", encoding="utf-8")); return p


MET = {"verdict": "MET", "remaining": 0, "next": "none", "detail": ["DA=0", "parity pilots 45/45 certified"]}
NOT_MET = {"verdict": "NOT_MET", "remaining": 3, "next": "terminal certification", "detail": ["F=59", "terminal 0/30"]}

# L1
lc = BV.lifecycle_block({"lifecycle": fixture("DATABASE")}, MET, True)
check("L1 phase read", lc["status"] == "OK" and lc["phase"] == "DATABASE" and lc["phase_label"] == "DATABASE IN PROGRESS", lc.get("phase_label"))
check("L1 authorization note", any("user authorizes" in n for n in lc["notes"]), lc["notes"])
check("L1 phase order", [p[0] for p in lc["phases"]] == ["DATABASE", "DATABASE_READY_AWAITING_AUTHORIZATION", "RECONSTRUCTION", "INTEGRATION",
                                                          "PARITY_CERTIFICATION", "HIGH_PARITY_RUNTIME"])
check("L1 chain names authorization", "user authorization" in lc["transition_chain"] and lc["user_authorization_required"] and not lc["automatic_transition"])
# L2
import inspect  # noqa: E402
check("L2 no parity/board input", list(inspect.signature(BV.lifecycle_block).parameters) == ["inp", "gg", "ready"])
check("L2 pilots do not move the phase", BV.lifecycle_block({"lifecycle": fixture("DATABASE")}, MET, True)["phase"] == "DATABASE")
# L3
real = BV.lifecycle_block({"lifecycle": REAL}, MET, True)
check("L3 real file, MET+ready -> file's phase", real["status"] == "OK" and real["phase"] == json.load(open(REAL, encoding="utf-8"))["current_primary_phase"]
      and real["phase_label"] != "RECONSTRUCTION AUTHORIZED", real.get("phase"))
lr = BV.lifecycle_block({"lifecycle": fixture("RECONSTRUCTION")}, NOT_MET, False)
check("L3 disagreement: both shown, later phase never current (meanings 6.1 rule 3)",
      lr["phase"] == "DATABASE" and lr["declared_phase"] == "RECONSTRUCTION" and lr["disagreement"]
      and any(n.startswith("DISAGREEMENT") for n in lr["notes"]) and all(p[3] != "current" or p[0] == "DATABASE" for p in lr["phases"]),
      (lr["phase"], lr.get("declared_phase"), lr["notes"]))
# L4
spec = BV.declare_inputs(tmp)["lifecycle"]
check("L4 declared strict", not spec.get("volatile") and spec["path"].endswith(os.path.join("workflow", "PROJECT-LIFECYCLE.json")))
live = fixture("DATABASE")
st = G.Store(os.path.join(tmp, "store"))
b = st.begin({"lifecycle": {"path": live}})
open(b.output_path("view-x.json"), "w").write("{}")
st.commit(b, ["view-x.json"])
man = st.open_current()[0]
before = st.drift(man)
d = json.load(open(live, encoding="utf-8")); d["contract_version"] = "changed"; json.dump(d, open(live, "w", encoding="utf-8"))
after = st.drift(man)
check("L4 drift -> STALE", before == {} and after.get("lifecycle") == "changed", (before, after))
# L5
pj = os.path.join(tmp, "progress_py.json")
json.dump({"overall": 51.2, "dimensions": [{"id": "engine_explained", "weight": 0.55, "numerator": 1, "denominator": 2}]}, open(pj, "w"))
dv = BV.v_depth({"progress_py": pj, "progress.py": os.path.join(BV.GS, "progress.py")}, "2026-10-03T00:00:00Z")
labels = " | ".join(m["label"] for m in dv["measures"])
check("L5 depth title", "not DB_GOAL" in dv["title"] and dv.get("diagnostic", {}).get("is_not", "").startswith("DB_GOAL"), dv["title"])
check("L5 no readiness label", "not DB_GOAL" in labels and "READY" not in labels.upper().replace("NOT DB_GOAL", ""), labels)
# L6
og = lc["original_game"]
check("L6 oracle, not backend", og["production_backend"] is False and "never the production backend" in og["role"]
      and any("wrapper" in x for x in og["not_reconstruction"]))
# L7
for tag, path in (("missing", os.path.join(tmp, "nope.json")), ("malformed", fixture(raw="{not json")),
                  ("unknown phase", fixture("SOMEWHERE")), ("no phases", fixture("DATABASE", drop="phases"))):
    r = BV.lifecycle_block({"lifecycle": path}, MET, True)
    check("L7 %s -> FAILED" % tag, r["status"] == "FAILED" and "phase" not in r, r.get("why"))
# L9 dashboard labels vs DASHBOARD-MEANINGS.md section 6 (FABLE's consumer-pair table maps this pair to this test)
import re  # noqa: E402
MEAN = os.path.join(BV.DB, "_index", "workflow", "DASHBOARD-MEANINGS.md")
text = open(MEAN, encoding="utf-8").read()
if "## 6." not in text:      # before FABLE's context-refresh publish lands: its staged section text
    text = open(os.path.join(BV.DB, "_index", "candidates", "fable-context-refresh-1003", "meanings_section6.txt"), encoding="utf-8").read()
s6 = re.sub(r"\s+", " ", text[text.index("## 6."):])      # the section wraps inside backticks; compare on single spaces
axis = s6[s6.index("### 6.1"):s6.index("1. **The phase is its own axis")]
want = re.findall(r"`([^`]+)`", axis)
got = [BV.PHASE_LABELS[i] for i in json.load(open(REAL, encoding="utf-8")) and [p["id"] for p in json.load(open(REAL, encoding="utf-8"))["phases"]]]
check("L9 phase labels == meanings 6.1 axis, in order", got == want, (got, want))
check("L9 probe label == meanings 6.1 rule 4", "`PROBE (database phase)`" in s6 and lc["probe_label"] == "PROBE (database phase)")
check("L9 Depth is 'the Depth diagnostic' (6.2)", "**Depth diagnostic**" in s6 and "diagnostic" in BV.DEPTH_TITLE and "not DB_GOAL" in BV.DEPTH_TITLE)
check("L9 DB_GOAL chain = remaining/next/detail (6.2)", all(x in s6 for x in ("`remaining=`", "`next=`", "`detail=`"))
      and set(BV.db_goal_block(NOT_MET)) >= {"verdict", "remaining", "next", "detail"})
check("L9 delegation is not reconstruction (6.4)", "`ORIGINAL-BINARY DELEGATION`" in s6 and lc["original_game"]["production_backend"] is False)
# L8
db = BV.db_goal_block(NOT_MET)
check("L8 gate lines verbatim", (db["verdict"], db["remaining"], db["next"], db["detail"]) == ("NOT_MET", 3, "terminal certification", ["F=59", "terminal 0/30"]))

shutil.rmtree(tmp, ignore_errors=True)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
