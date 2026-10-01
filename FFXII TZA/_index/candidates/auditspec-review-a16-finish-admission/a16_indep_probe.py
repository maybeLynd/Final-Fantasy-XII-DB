"""SWE2-AUDIT-SPEC independent A16 finish-admission probe (not ASTRA's probe.py).

Differences from ASTRA's probe: the disposable task is REQUEST-shaped (kind request,
requester, assigned_to = reviewer), as real review requests are; more verdict shapes are
tried (conflict, lowercase, leading space, CR, duplicate); and the real live board is
scanned for DONE reviews-bearing tasks to show the gap end to end through the CLI path.
Deep copies only; live board bytes compared before/after.
"""
import copy, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
TOOLS = Path(r"Database/Tools/analysis-kit/gfz-scripts")
sys.path.insert(0, str(TOOLS))
import team, transitions

pre = team.BOARD.read_bytes()
base = json.loads(pre)
team.validate(base)
TID = "AUDITSPEC-A16-INDEP-CONTROL"
task = {"id": TID, "kind": "request", "priority": "P2", "requester": "ASTRA",
        "assigned_to": "SWE2-AUDIT-SPEC", "target": "x", "scope": "x", "completion": "x",
        "question": "q", "known_evidence": "k", "missing_information": "m",
        "why_it_matters": "w", "what_is_blocked": "b", "dependencies": [],
        "resources": [{"key": "request:auditspec-a16-indep-control"}],
        "reviews": {"author": "ASTRA", "commit": "c9278cb", "record": "R.md",
                    "incorporation_owner": "OPUS"}}

def run(label, refs, reviewer="SWE2-AUDIT-SPEC", t=task):
    b = copy.deepcopy(base)
    team.apply(b, t["requester"], {"action": "add", "task": t}, "probe")
    team.apply(b, reviewer, {"action": "claim", "task": TID, "note": "n"}, "probe")
    err = None
    try:
        team.apply(b, reviewer, {"action": "finish", "task": TID, "note": "n", "result_refs": refs}, "probe")
    except Exception as e:
        err = "%s: %s" % (type(e).__name__, e)
    row = next(x for x in b["tasks"] if x["id"] == TID)
    pl = [(k, d, op is not None) for (k, i, d, op) in transitions.plan(b) if i == TID]
    print("%-22s finish_err=%-6s status=%-5s plan=%s" % (label, bool(err), row["status"], pl))

run("missing", ["receipt:x"])
run("exact-accept", ["receipt:x", "verdict:ACCEPT"])
run("exact-reject", ["receipt:x", "verdict:REJECT"])
run("lf", ["verdict:ACCEPT\n"])
run("cr", ["verdict:ACCEPT\r"])
run("lower", ["verdict:accept"])
run("lead-space", [" verdict:ACCEPT"])
run("conflict", ["verdict:ACCEPT", "verdict:REJECT"])
run("duplicate-same", ["verdict:ACCEPT", "verdict:ACCEPT"])
run("prose-only", ["verdict ACCEPT (see record)"])
# positive control for the self-review guard, to show plan() is sensitive
t2 = dict(task, requester="SWE2-AUDIT-SPEC", assigned_to="ASTRA", resources=[{"key": "request:auditspec-a16-indep-control"}])
t2["reviews"] = dict(task["reviews"], author="ASTRA")
run("self-review", ["verdict:ACCEPT"], reviewer="ASTRA", t=t2)

# live end-to-end: DONE tasks carrying reviews whose refs have no exact verdict
print("\nlive board rev", base["revision"])
for t in base["tasks"]:
    if t.get("reviews") is not None and t["status"] == "DONE":
        v = [r for r in t.get("result_refs") or [] if transitions.VERDICT.fullmatch(str(r))]
        if not v:
            print("  DONE reviews w/o exact verdict:", t["id"], "agent=", t.get("agent"))
missing_plan = [(k, i) for (k, i, d, op) in transitions.plan(base) if k in ("VERDICT-MISSING", "VERDICT-CONFLICT")]
print("  plan VERDICT-MISSING/CONFLICT on live copy:", missing_plan)
assert team.BOARD.read_bytes() == pre or print("NOTE: live board moved during probe (peer write), not ours")
print("source sha256 team.py", hashlib.sha256((TOOLS / "team.py").read_bytes()).hexdigest()[:16],
      "transitions.py", hashlib.sha256((TOOLS / "transitions.py").read_bytes()).hexdigest()[:16])
