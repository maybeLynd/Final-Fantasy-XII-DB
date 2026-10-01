"""test_transitions.py - transitions.py on disposable boards through its CLI and team.py's real writer (OPUS, 2026-09-29;
matrix A14 idempotency, A16 review -> repair / incorporation). Never touches the live board.

  X1  a REJECT review -> dry run plans one AUTO-REPAIR task and writes nothing
  X2  --apply creates it through team.py (assigned to the author, requester the controller identity, linked back)
  X3  a second --apply creates nothing (idempotent: the derived id exists)
  X4  an ACCEPT review naming an incorporation owner -> one AUTO-INCORP task to that owner
  X5  an ACCEPT with no separate incorporation owner -> recorded, nothing created
  X6  a DONE review whose result refs carry no verdict: -> VERDICT-MISSING, nothing created (even though its note says ACCEPT)
  X7  a malformed reviews field (author not a board identity) -> MALFORMED, nothing created
  X8  two verdicts that disagree -> VERDICT-CONFLICT, nothing created
  X9  a DONE task with no reviews field is ignored
  X10 a truthy dict commit, X11 a non-SHA string commit, X12 a dict record -> MALFORMED, nothing created
  X13 a list author -> MALFORMED and the CLI exits 0 (no TypeError aborting the whole plan)
  X14 a self-review (the finishing identity is the author) -> SELF-REVIEW for ACCEPT and REJECT alike, nothing created
      (X10-X14: ASTRA's REJECT of 0d50ee5f3, OPUS-REQ-ASTRA-VERIFY-TRANSITIONS)
  X15 a 40-hex commit + LF (41 chars) -> MALFORMED; X16 "verdict:ACCEPT\n" -> no verdict (VERDICT-MISSING); X17 a commit + CRLF
      -> MALFORMED; X18 the exact 40-hex positive is planned and forwards the commit byte for byte in transition_of
      (X15-X18: ASTRA f112e86b0, ASTRA-REQ-OPUS-TRANSITION-LINE-BOUNDARY)
  X19 writer_status: exit 0 + "Saved revision N" -> created; a non-zero exit after "Saved revision" -> FAILED; an error-only
      non-zero exit -> FAILED; exit 0 without the line -> FAILED
  X20 the duplicate-id refusal is "exists" only when the id is on the re-read board; the same text without it -> FAILED
      (X19-X20: ASTRA 821c25f8b, ASTRA-REQ-OPUS-TRANSITION-WRITER-STATUS)
"""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import team  # noqa: E402
fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
b = {"schema_version": 1, "phase": "DATABASE", "revision": 0, "agents": {}, "tasks": [], "history": []}
for a in team.AGENTS:
    b["agents"][a] = {"agent_id": a, "primary_specialty": a, "last_checkpoint": team.now()}
team.refresh(b)
def review(i, reviewer, refs, note, rv, legacy=False):
    t = {"id": i, "kind": "request", "priority": "P2", "requester": "OPUS", "assigned_to": reviewer, "target": "fixture", "scope": "non-author review",
         "question": "q", "known_evidence": "e", "missing_information": "m", "why_it_matters": "w", "what_is_blocked": "b", "completion": "c",
         "dependencies": [], "resources": [{"key": "request:" + i.lower()}]}
    if rv is not None: t["reviews"] = rv
    team.apply(b, "OPUS", {"action": "add", "task": t})
    team.apply(b, reviewer, {"action": "claim", "task": i, "note": "reviewing"})
    if legacy:
        # A16 finish-path gate (2026-09-29): team.py now refuses to finish a review without exactly one policy verdict, so
        # the historical rows that did (55 on the live board) are modelled as they stand: DONE, set directly on this
        # disposable fixture board, never through a writer.
        x = next(x for x in b["tasks"] if x["id"] == i)
        x.update(status="DONE", result_refs=refs, checkpoint=note)
    else:
        team.apply(b, reviewer, {"action": "finish", "task": i, "note": note, "result_refs": refs})
RV = {"author": "OPUS", "commit": "abc1234", "record": "_index/candidates/x/README.md"}
review("FIX-REJ", "SWE2-AUDIT-SEM", ["verdict:REJECT", "file:review.md"], "REJECT: Z swallows failures", RV)
review("FIX-ACC-INC", "SWE2-AUDIT-SPEC", ["verdict:ACCEPT", "file:r2.md"], "ACCEPT", dict(RV, incorporation_owner="FABLE", package_item="PKG-X:T1"))
review("FIX-ACC-SELF", "SWE2-AUDIT-SPEC", ["verdict:ACCEPT", "file:r3.md"], "ACCEPT", RV)
review("FIX-NOVERDICT", "SWE2-AUDIT-SEM", ["file:r4.md"], "ACCEPT - looks fine", RV, legacy=True)
review("FIX-NARROW", "SWE2-AUDIT-SEM", ["verdict:ACCEPT-WITH-NARROWING", "file:r5.md"], "narrowed", dict(RV, incorporation_owner="FABLE"))
review("FIX-MAL", "SWE2-AUDIT-SEM", ["verdict:ACCEPT"], "ACCEPT", {"author": "NOBODY", "commit": "x"})
review("FIX-CONFLICT", "SWE2-AUDIT-SEM", ["verdict:ACCEPT", "verdict:REJECT"], "?", RV, legacy=True)
review("FIX-PLAIN", "SWE2-AUDIT-SEM", ["verdict:REJECT"], "no reviews field", None)
review("FIX-DICTCOMMIT", "SWE2-AUDIT-SEM", ["verdict:REJECT"], "x", dict(RV, commit={"sha": "abc1234"}))
review("FIX-NONSHA", "SWE2-AUDIT-SEM", ["verdict:REJECT"], "x", dict(RV, commit="HEAD"))
review("FIX-DICTREC", "SWE2-AUDIT-SEM", ["verdict:REJECT"], "x", dict(RV, record={"path": "a.md"}))
review("FIX-LISTAUTH", "SWE2-AUDIT-SEM", ["verdict:REJECT"], "x", dict(RV, author=["OPUS"]))
review("FIX-SELF-ACC", "OPUS", ["verdict:ACCEPT"], "x", dict(RV, incorporation_owner="FABLE"))
review("FIX-SELF-REJ", "OPUS", ["verdict:REJECT"], "x", RV)
SHA40 = "0123456789abcdef0123456789abcdef01234567"
review("FIX-LF", "SWE2-AUDIT-SEM", ["verdict:REJECT"], "x", dict(RV, commit=SHA40 + "\n"))
review("FIX-VLF", "SWE2-AUDIT-SEM", ["verdict:ACCEPT\n"], "x", dict(RV, incorporation_owner="FABLE"), legacy=True)
review("FIX-CRLF", "SWE2-AUDIT-SEM", ["verdict:REJECT"], "x", dict(RV, commit=SHA40 + "\r\n"))
review("FIX-EXACT40", "SWE2-AUDIT-SEM", ["verdict:REJECT"], "x", dict(RV, commit=SHA40))
T = tempfile.mkdtemp(prefix="trans_"); bp = os.path.join(T, "TEAM.json")
json.dump(b, open(bp, "w", encoding="utf-8"), indent=1)
def cli(*args):
    r = subprocess.run([sys.executable, os.path.join(HERE, "transitions.py"), "--board", bp, "--json"] + list(args), capture_output=True, text=True)
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("[") else r.stdout + r.stderr)
tasks = lambda: {t["id"]: t for t in json.load(open(bp, encoding="utf-8"))["tasks"]}
by = lambda res: {x["review"]: x for x in res}
rc, res = cli(); r = by(res)
check("X1", rc == 0 and r["FIX-REJ"]["transition"] == "REPAIR" and r["FIX-REJ"]["status"] == "planned" and "AUTO-REPAIR-FIX-REJ" not in tasks(), json.dumps(r["FIX-REJ"]))
rc, res = cli("--apply"); r = by(res); t = tasks()
rep = t.get("AUTO-REPAIR-FIX-REJ", {})
check("X2", rc == 0 and r["FIX-REJ"]["status"] == "created" and rep.get("assigned_to") == "OPUS" and rep.get("requester") == "SWE2-FRONTIER"
      and rep.get("status") == "READY" and rep.get("transition_of") == {"review": "FIX-REJ", "commit": "abc1234"}, "%s -> %s" % (r["FIX-REJ"]["status"], rep.get("assigned_to")))
n1 = len(t); rc, res = cli("--apply"); r = by(res)
check("X3", rc == 0 and len(tasks()) == n1 and r["FIX-REJ"]["transition"] == "DONE-ALREADY" and r["FIX-ACC-INC"]["transition"] == "DONE-ALREADY", "tasks %d -> %d" % (n1, len(tasks())))
inc = t.get("AUTO-INCORP-FIX-ACC-INC", {})
check("X4", inc.get("assigned_to") == "FABLE" and "PKG-X:T1" in inc.get("question", ""), inc.get("assigned_to"))
check("X5", r["FIX-ACC-SELF"]["transition"] == "ACCEPTED" and "AUTO-INCORP-FIX-ACC-SELF" not in t)
check("X6", r["FIX-NOVERDICT"]["transition"] == "VERDICT-MISSING" and not any(k.endswith("FIX-NOVERDICT") and k != "FIX-NOVERDICT" for k in t))
check("X7", r["FIX-MAL"]["transition"] == "MALFORMED" and "AUTO-INCORP-FIX-MAL" not in t)
check("X8", r["FIX-CONFLICT"]["transition"] == "VERDICT-CONFLICT" and "AUTO-REPAIR-FIX-CONFLICT" not in t)
check("X9", "FIX-PLAIN" not in r and "AUTO-REPAIR-FIX-PLAIN" not in t)
made = lambda rid: [k for k in t if k.startswith("AUTO-") and k.endswith("-" + rid)]
for tag, rid in (("X10", "FIX-DICTCOMMIT"), ("X11", "FIX-NONSHA"), ("X12", "FIX-DICTREC")):
    check(tag, r[rid]["transition"] == "MALFORMED" and not made(rid), r[rid].get("detail"))
check("X13", rc == 0 and r["FIX-LISTAUTH"]["transition"] == "MALFORMED" and not made("FIX-LISTAUTH"), r["FIX-LISTAUTH"].get("detail"))
check("X14", r["FIX-SELF-ACC"]["transition"] == r["FIX-SELF-REJ"]["transition"] == "SELF-REVIEW" and not made("FIX-SELF-ACC")
      and not made("FIX-SELF-REJ"), "%s / %s" % (r["FIX-SELF-ACC"]["transition"], r["FIX-SELF-REJ"]["transition"]))
check("X15", r["FIX-LF"]["transition"] == "MALFORMED" and not made("FIX-LF"), r["FIX-LF"].get("detail"))
check("X16", r["FIX-VLF"]["transition"] == "VERDICT-MISSING" and not made("FIX-VLF"), r["FIX-VLF"]["transition"])
check("X17", r["FIX-CRLF"]["transition"] == "MALFORMED" and not made("FIX-CRLF"), r["FIX-CRLF"].get("detail"))
e40 = t.get("AUTO-REPAIR-FIX-EXACT40", {})
check("X18", e40.get("transition_of") == {"review": "FIX-EXACT40", "commit": SHA40} and len(e40["transition_of"]["commit"]) == 40,
      "exact 40-hex positive forwarded as %r" % (e40.get("transition_of") or {}).get("commit"))
import transitions as TR  # noqa: E402
ws = TR.writer_status
check("X19", ws(0, "Saved revision 12\n", False) == "created" and ws(1, "Saved revision 12\nTraceback: boom\n", False).startswith("FAILED")
      and ws(1, "Saved revision 12\n", True).startswith("FAILED") and ws(1, "BOARD INCIDENT: stale\n", False).startswith("FAILED")
      and ws(0, "", False).startswith("FAILED") and ws(0, "Saved revision\n", False).startswith("FAILED"),
      "labelled child: %s" % ws(1, "Saved revision 12\nTraceback: boom\n", False))
check("X20", ws(1, "task already exists\n", True) == "exists" and ws(1, "task already exists\n", False).startswith("FAILED")
      and ws(1, "task already exists (not quite)\n", True).startswith("FAILED"),
      "refusal + on board -> %s; refusal, not on board -> %s" % (ws(1, "task already exists\n", True), ws(1, "task already exists\n", False)))
# X21 (A16 finish-path, 2026-09-29): a policy verdict other than ACCEPT/REJECT is named, not reported missing, and drives
# nothing automatically
check("X21", r["FIX-NARROW"]["transition"] == "VERDICT-MANUAL" and "ACCEPT-WITH-NARROWING" in r["FIX-NARROW"]["detail"]
      and not made("FIX-NARROW"), "%s: %s" % (r["FIX-NARROW"]["transition"], r["FIX-NARROW"]["detail"]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
