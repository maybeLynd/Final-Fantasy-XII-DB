"""transitions.py - the review -> repair / incorporation transition, deterministic and idempotent (OPUS, 2026-09-29).

Workflow migration M2 (FF12-WORKFLOW-MIGRATION-20260928-01 sections 3-5; acceptance matrix A14, A16). A finished review
should start the next step without a person relaying it. This does that with supported board writes only (team.py apply),
from structured data only - it never reads a verdict out of prose.

THE CONVENTION (two fields, both already storable by team.py):
  - a review request carries  "reviews": {"author": <lane>, "commit": <sha>, "record": <repo path>,
                                          "incorporation_owner": <lane, optional>, "package_item": <PKG-...:ID, optional>}
  - the reviewer's finish carries a result ref  "verdict:ACCEPT"  or  "verdict:REJECT"  (plus its receipt refs)

THE TRANSITIONS, for each DONE task that has a "reviews" field:
  verdict:REJECT -> one request AUTO-REPAIR-<review id> to the author: repair at the cause, then re-request review
  verdict:ACCEPT -> one request AUTO-INCORP-<review id> to incorporation_owner, when that owner is named and is not the
                    author; otherwise the acceptance is recorded in the plan only (nothing to hand over)
  no verdict ref  -> reported as VERDICT-MISSING; nothing is created (a verdict is never guessed from the note)
  malformed field -> reported as MALFORMED; nothing is created. Every value is type-checked first (link_problem): the
                    author a board identity string, the commit a 7-40 hex string, the record a non-empty path string
  self-review     -> the finishing identity is the author: reported as SELF-REVIEW; nothing is created
Idempotent: the next task's id is derived from the review's id, so a second run finds it and creates nothing, and two
racing runs cannot both create it (team.py refuses a duplicate id inside its lock).

    python transitions.py [--board PATH] [--agent SWE2-FRONTIER] [--apply] [--json]
Default is a dry run (the shadow check the brief requires before activation). --apply writes through
`team.py apply --agent <agent> --file <op>` - the supported writer, with its lock and journal.
"""
import argparse, json, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import team  # noqa: E402

VERDICT = re.compile(r"^verdict:(ACCEPT|REJECT)$")
SHA = re.compile(r"^[0-9a-f]{7,40}$")


def link_problem(rv):
    """Why a reviews field cannot drive a transition, or None. Every value is checked for its TYPE before it is used, so
    a truthy dict commit, a non-SHA string, a dict record or a list author is reported, never admitted and never a crash
    (ASTRA's REJECT of 0d50ee5f3: commit truthiness and author membership were the only checks)."""
    if not isinstance(rv, dict):
        return "reviews is %s, not an object" % type(rv).__name__
    a = rv.get("author")
    if not isinstance(a, str) or a not in team.AGENTS:
        return "author %r is not a board identity" % (a,)
    c = rv.get("commit")
    if not isinstance(c, str) or not SHA.match(c):
        return "commit %r is not a 7-40 hex commit id" % (c,)
    r = rv.get("record")
    if not isinstance(r, str) or not r.strip():
        return "record %r is not a repository path" % (r,)
    for k in ("incorporation_owner", "package_item"):
        if k in rv and rv[k] is not None and not isinstance(rv[k], str):
            return "%s %r is not a string" % (k, rv[k])
    return None


def plan(board):
    """[(kind, review_id, detail, op_or_None)] for every DONE task carrying a reviews field."""
    ids = {t["id"] for t in board["tasks"]}
    out = []
    # Blocked -> reconsidered: a task parked on dependencies whose deps have
    # all landed gets exactly one AUTO-UNBLOCK nudge to its owner (the owner
    # still performs the `resume` - this pass only files the wakeup, so an
    # unchanged dependency set can never produce a second nudge).
    ids_done = {t["id"] for t in board["tasks"] if t["status"] == "DONE"}
    for t in board["tasks"]:
        if t["status"] != "BLOCKED" or not t.get("dependencies"):
            continue
        if not set(t["dependencies"]) <= ids_done:
            continue
        owner = t.get("agent") or t.get("assigned_to")
        if owner not in team.AGENTS:
            out.append(("UNBLOCK-NO-OWNER", t["id"], "deps done but no owner", None)); continue
        nid = "AUTO-UNBLOCK-" + t["id"]
        if nid in ids:
            out.append(("DONE-ALREADY", t["id"], nid, None)); continue
        q = ("Your BLOCKED task %s is unblocked - every dependency has landed. "
             "Reconsider it: `resume` it if the work is still wanted, or retire/finish "
             "it if the deps made it moot. Dep blockers cleared: %s"
             % (t["id"], t["dependencies"]))
        op = {"action": "add", "task": {
            "id": nid, "kind": "request", "priority": t.get("priority", "P2"),
            "assigned_to": owner,
            "target": "%s <- deps complete" % t["id"],
            "scope": "dependency transition - reconsider a blocked package",
            "question": q,
            "known_evidence": "all dependencies of %s are DONE" % t["id"],
            "missing_information": "owner's disposition",
            "why_it_matters": "a paused package must resume on the dependency transition without a relayed message",
            "what_is_blocked": t["id"], "completion": "resumed or retired with a note",
            "resources": [{"key": "request:" + nid.lower()}], "dependencies": [],
            "transition_of": {"unblocked": t["id"]}}}
        out.append(("UNBLOCK", t["id"], nid, op))
    for t in board["tasks"]:
        rv = t.get("reviews")
        if rv is None or t["status"] != "DONE":
            continue
        why = link_problem(rv)
        if why:
            out.append(("MALFORMED", t["id"], why, None)); continue
        # Independence: the identity that finished the review must not be the author of what it reviewed. A self-review
        # drives nothing - neither a repair nor an incorporation - and is reported so it can be re-requested of a peer.
        reviewer = t.get("agent")
        if not isinstance(reviewer, str) or reviewer not in team.AGENTS:
            out.append(("MALFORMED", t["id"], "reviewer %r is not a board identity" % (reviewer,), None)); continue
        if reviewer == rv["author"]:
            out.append(("SELF-REVIEW", t["id"], "reviewer %s is the author; not an independent review" % reviewer, None)); continue
        verdicts = [m.group(1) for r in (t.get("result_refs") or []) for m in [VERDICT.match(str(r))] if m]
        if len(set(verdicts)) != 1:
            out.append(("VERDICT-MISSING" if not verdicts else "VERDICT-CONFLICT", t["id"], "result refs carry %s" % (verdicts or "no verdict:"), None)); continue
        v = verdicts[0]
        refs = [r for r in t.get("result_refs") or [] if not VERDICT.match(str(r))]
        if v == "REJECT":
            nid = "AUTO-REPAIR-" + t["id"]
            if nid in ids:
                out.append(("DONE-ALREADY", t["id"], nid, None)); continue
            q = ("Review %s REJECTED %s (reviewer %s). Repair at the cause, update affected consumers, and re-request review with a "
                 "`reviews` field naming this task. Reviewer's receipts: %s. Review note: %s"
                 % (t["id"], rv["commit"], t.get("agent"), refs, (t.get("checkpoint") or "")[:600]))
            out.append(("REPAIR", t["id"], nid, _op(nid, rv["author"], "repair after rejected review", q, t, rv)))
        else:
            owner = rv.get("incorporation_owner")
            if not owner or owner == rv["author"]:
                out.append(("ACCEPTED", t["id"], "no separate incorporation owner named", None)); continue
            if owner not in team.AGENTS:
                out.append(("MALFORMED", t["id"], "incorporation_owner %r is not a board identity" % owner, None)); continue
            nid = "AUTO-INCORP-" + t["id"]
            if nid in ids:
                out.append(("DONE-ALREADY", t["id"], nid, None)); continue
            q = ("Review %s ACCEPTED %s (record %s). Incorporate it into your canonical files%s and list the updated consumers. "
                 "Reviewer's receipts: %s" % (t["id"], rv["commit"], rv.get("record"), (" for " + rv["package_item"]) if rv.get("package_item") else "", refs))
            out.append(("INCORPORATE", t["id"], nid, _op(nid, owner, "incorporation after accepted review", q, t, rv)))
    return out


def _op(nid, to, scope, question, review, rv):
    return {"action": "add", "task": {
        "id": nid, "kind": "request", "priority": review.get("priority", "P2"), "assigned_to": to,
        "target": "%s -> %s" % (review["id"], rv.get("record") or rv["commit"]), "scope": scope, "question": question,
        "known_evidence": "review %s (commit %s)" % (review["id"], rv["commit"]), "missing_information": "the next step's result",
        "why_it_matters": "review-to-%s transition without a relayed message (M2, A16)" % scope.split()[0],
        "what_is_blocked": rv.get("package_item") or "the reviewed claim's completion", "completion": "committed, with receipts",
        "resources": [{"key": "request:" + nid.lower()}], "dependencies": [],
        "transition_of": {"review": review["id"], "commit": rv["commit"]}}}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", default=str(team.BOARD)); ap.add_argument("--agent", default="SWE2-FRONTIER")
    ap.add_argument("--apply", action="store_true"); ap.add_argument("--json", action="store_true")
    # The caller's wall-clock cap for board writes. team.py apply serializes under
    # live board contention (measured ~60-240 s per op on 2026-09-29), so an
    # unbounded apply pass can exceed the watchdog's timeout mid-queue. With a
    # budget, ops past the limit are reported "deferred" - not attempted and not
    # failed - and the idempotent rerun next cycle picks them up. 0 = unbounded.
    ap.add_argument("--apply-budget-s", type=float, default=0)
    a = ap.parse_args(argv)
    board = json.load(open(a.board, encoding="utf-8"))
    p = plan(board)
    results = []
    t0 = time.monotonic()
    deferred = False
    for kind, rid, detail, op in p:
        status = "planned" if op else "-"
        if op and a.apply:
            if deferred or (a.apply_budget_s and time.monotonic() - t0 > a.apply_budget_s):
                status, deferred = "deferred", True
            else:
                op["task"]["requester"] = a.agent
                with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
                    json.dump(op, f); fp = f.name
                r = subprocess.run([sys.executable, os.path.join(HERE, "team.py"), "apply", "--agent", a.agent, "--board", a.board, "--file", fp],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace")
                os.remove(fp)
                out = (r.stdout + r.stderr)
                status = "created" if "Saved revision" in out else ("exists" if "already exists" in out else "FAILED: " + out.strip().splitlines()[-1][:160] if out.strip() else "FAILED")
        results.append({"transition": kind, "review": rid, "detail": detail, "status": status})
    if a.json:
        print(json.dumps(results, indent=1))
    else:
        for x in results:
            print("%-16s %-50s %-40s %s" % (x["transition"], x["review"][:50], str(x["detail"])[:40], x["status"]))
        print("%d transition(s); %s%s" % (sum(1 for x in results if x["status"] != "-"),
              "applied" if a.apply else "dry run",
              ", %d deferred" % sum(1 for x in results if x["status"] == "deferred")
              if any(x["status"] == "deferred" for x in results) else ""))
    return 1 if any(x["status"].startswith("FAILED") for x in results) else 0


if __name__ == "__main__":
    sys.exit(main())
