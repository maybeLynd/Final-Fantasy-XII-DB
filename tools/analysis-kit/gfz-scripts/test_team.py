"""Exercise A-G and real competing processes against disposable boards, never live claims."""
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

import team


def board():
    b = {"schema_version": 1, "phase": "DATABASE", "revision": 0,
         "agents": {}, "tasks": [], "history": []}
    for a in team.AGENTS:
        b["agents"][a] = {"agent_id": a, "primary_specialty": a, "last_checkpoint": team.now()}
    team.refresh(b)
    return b


def add(b, key, resource, **extra):
    t = {"id": key, "kind": "research", "priority": "P1", "target": resource,
         "scope": "bounded fixture", "completion": "fixture observation recorded",
         "dependencies": [], "resources": [{"key": resource}]}
    t.update(extra)
    team.apply(b, "FABLE", {"action": "add", "task": t})


def act(b, who, action, task, **extra):
    team.apply(b, who, {"action": action, "task": task, "note": "fixture checkpoint", **extra})


class Scenarios(unittest.TestCase):
    def test_a_claim_is_visible_and_conflicting_work_excluded(self):
        b = board()
        add(b, "SEM-X", "type:actor")
        add(b, "TYPE-X", "type:actor", resources=[{"key": "type:actor", "start": 704, "end": 800}])
        add(b, "TYPE-Y", "type:other")
        act(b, "FABLE", "claim", "SEM-X")
        self.assertEqual([t["id"] for t in team.ready(b, "OPUS")], ["TYPE-Y"])
        with self.assertRaises(ValueError):
            act(b, "OPUS", "claim", "TYPE-X")
        act(b, "OPUS", "claim", "TYPE-Y")

    def test_b_specialized_request_returns_durable_result(self):
        b = board()
        add(b, "STATIC-X", "target:x/static")
        request = {"id": "RUN-X", "kind": "runtime", "priority": "P1", "target": "X live ABI",
                   "scope": "capture args only", "completion": "controlled register capture",
                   "dependencies": [], "resources": [{"key": "@runtime"}],
                   "requester": "OPUS", "assigned_to": "ASTRA", "question": "Is rcx owner X?",
                   "known_evidence": "caller disassembly", "missing_information": "live rcx identity",
                   "why_it_matters": "contract ownership", "what_is_blocked": "ABI-X"}
        team.apply(b, "OPUS", {"action": "add", "task": request})
        add(b, "ABI-X", "target:x/contract", dependencies=["RUN-X"])
        act(b, "OPUS", "claim", "STATIC-X")
        self.assertNotIn("ABI-X", [t["id"] for t in team.ready(b, "OPUS")])
        with self.assertRaises(ValueError):
            act(b, "FABLE", "claim", "RUN-X")
        act(b, "ASTRA", "claim", "RUN-X")
        act(b, "ASTRA", "finish", "RUN-X", result_refs=["fixture/controlled-capture.json"])
        self.assertIn("ABI-X", [t["id"] for t in team.ready(b, "OPUS")])
        self.assertEqual(b["tasks"][1]["known_evidence"], "caller disassembly")

    def test_c_contradiction_preserves_both_sides_and_waits_for_file(self):
        b = board()
        add(b, "SEM-X", "file:database/x.md")
        act(b, "FABLE", "claim", "SEM-X")
        dispute = {"id": "REOPEN-X", "kind": "contradiction", "priority": "P0", "target": "X",
                   "scope": "reopen disputed conclusion", "completion": "evidence resolution and propagation",
                   "dependencies": [], "resources": [{"key": "file:database/x.md"}],
                   "requester": "ASTRA", "assigned_to": "FABLE", "question": "Can X equal 2?",
                   "known_evidence": "static: X always 1", "missing_information": "path explaining X=2",
                   "why_it_matters": "wrong contract", "what_is_blocked": "dependent claims",
                   "original_claim": "X always 1", "counter_evidence": "capture: X=2",
                   "affected_documents": "database/x.md and dependent contracts"}
        team.apply(b, "ASTRA", {"action": "add", "task": dispute})
        self.assertEqual(b["tasks"][1]["counter_evidence"], "capture: X=2")
        self.assertEqual(b["tasks"][0]["status"], "ACTIVE")
        self.assertNotIn("REOPEN-X", [t["id"] for t in team.ready(b, "FABLE")])
        act(b, "FABLE", "release", "SEM-X")
        self.assertEqual(team.ready(b, "FABLE")[0]["id"], "REOPEN-X")
        self.assertEqual(b["history"][-2]["operation"]["task"]["original_claim"], "X always 1")

    def test_d_finished_worker_selects_next_unblocked_priority(self):
        b = board()
        add(b, "FIRST", "target:first")
        add(b, "TAIL", "target:tail", priority="P3")
        add(b, "NEXT", "target:next", priority="P0", dependencies=["FIRST"])
        act(b, "FABLE", "claim", "FIRST")
        act(b, "FABLE", "finish", "FIRST", result_refs=["fixture/handoff.md"])
        self.assertEqual(team.ready(b, "FABLE")[0]["id"], "NEXT")
        act(b, "FABLE", "claim", "NEXT")

    def test_e_shared_publication_and_generated_file_collision(self):
        b = board()
        add(b, "PUB-A", "@publication")
        add(b, "PUB-B", "@publication")
        add(b, "GEN-A", "file:database/index")
        add(b, "GEN-B", "file:database/index/rules.md")
        act(b, "FABLE", "claim", "PUB-A")
        act(b, "FABLE", "claim", "GEN-A")
        for key in ["PUB-B", "GEN-B"]:
            with self.assertRaises(ValueError):
                act(b, "OPUS", "claim", key)
        act(b, "FABLE", "finish", "GEN-A", result_refs=["fixture/generated-output"])
        act(b, "FABLE", "finish", "PUB-A", result_refs=["fixture/commit"])
        act(b, "OPUS", "claim", "PUB-B")
        act(b, "OPUS", "claim", "GEN-B")

    def test_f_blocked_worker_records_reason_and_continues(self):
        b = board()
        add(b, "WAIT", "@runtime")
        add(b, "OFFLINE", "target:offline")
        act(b, "ASTRA", "claim", "WAIT")
        act(b, "ASTRA", "block", "WAIT", resume_when="clean environment available")
        act(b, "ASTRA", "claim", "OFFLINE")
        self.assertEqual(b["agents"]["ASTRA"]["current_task"], ["OFFLINE"])
        self.assertEqual(b["agents"]["ASTRA"]["blockers"][0]["task"], "WAIT")
        act(b, "ASTRA", "resume", "WAIT")
        self.assertEqual(b["tasks"][0]["status"], "READY")

    def test_identity_range_cycle_and_foreign_release_rejected(self):
        b = board()
        add(b, "ONE", "target:x", resources=[{"key": "target:x", "start": 0, "end": 10}])
        add(b, "TWO", "target:x", resources=[{"key": "target:x", "start": 10, "end": 20}])
        act(b, "FABLE", "claim", "ONE")
        act(b, "OPUS", "claim", "TWO")
        with self.assertRaises(ValueError):
            act(b, "ASTRA", "release", "ONE")
        for mutation in [lambda x: x["agents"].update(HELPER={}),
                         lambda x: x["tasks"][0].update(dependencies=["ONE"]),
                         lambda x: x["tasks"][0]["resources"][0].update(key="file:database/types.tsv"),
                         lambda x: x["tasks"][0]["resources"][0].update(key="file:database/./types.tsv"),
                         lambda x: x["tasks"][0]["resources"][0].update(end=0)]:
            invalid = deepcopy(b)
            mutation(invalid)
            with self.assertRaises(ValueError):
                team.validate(invalid)

    def test_real_process_race_and_failed_transaction_leave_valid_board(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TEAM.json"
            b = board()
            add(b, "RACE-A", "target:shared")
            add(b, "RACE-B", "target:shared")
            path.write_text(json.dumps(b), encoding="utf-8")
            jobs = []
            for who, key in [("FABLE", "RACE-A"), ("OPUS", "RACE-B")]:
                op = Path(d) / (key + ".json")
                op.write_text(json.dumps({"action": "claim", "task": key, "note": "race"}))
                jobs.append(subprocess.Popen([sys.executable, team.__file__, "apply", "--board", str(path),
                    "--agent", who, "--file", str(op)], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
            outputs = [p.communicate(timeout=20) for p in jobs]
            self.assertEqual(sorted(p.returncode for p in jobs), [0, 1], outputs)
            b = json.loads(path.read_text())
            team.validate(b)
            self.assertEqual(sum(t["status"] == "ACTIVE" for t in b["tasks"]), 1)
            before = path.read_bytes()
            with self.assertRaises(ValueError):
                team.transaction(path, "ASTRA", {"action": "finish", "task": "RACE-A", "note": "invalid"})
            self.assertEqual(path.read_bytes(), before)
            with team.locked(path):
                with self.assertRaises(FileExistsError):
                    team.transaction(path, "ASTRA", {"action": "claim", "task": "RACE-B", "note": "locked"})
            self.assertFalse(path.with_suffix(".lock").exists())

    def test_lock_liveness_fails_closed_on_unqueryable_holder(self):
        """ASTRA-RETURN-FRONTIER-TEAM-ACCESS-DENIED-LIVENESS, 2026-09-21: OpenProcess
        on a live holder failed with error 5 and _holder_is_live mapped the None to
        dead, reaping a lock under its owner. Only ERROR_INVALID_PARAMETER (87)
        proves the pid does not exist; denied/unknown must read as live."""
        # the mapping itself - the branch that carried the defect
        self.assertTrue(team._open_failed_means_dead(87))
        self.assertFalse(team._open_failed_means_dead(5))
        self.assertFalse(team._open_failed_means_dead(0))
        # live control: our own pid must read as live
        self.assertTrue(team._proc_start(os.getpid()))
        # dead control: a process that ran and exited must read as dead
        p = subprocess.Popen([sys.executable, "-c", "pass"])
        p.wait(timeout=20)
        for _ in range(40):
            if team._proc_start(p.pid) is None:
                break
            time.sleep(0.05)
        self.assertIsNone(team._proc_start(p.pid))
        # end to end: a lock file naming a dead pid is reaped, ours is not
        with tempfile.TemporaryDirectory() as d:
            lock = Path(d) / "TEAM.lock"
            lock.write_text(json.dumps({"pid": p.pid, "started": None}))
            self.assertFalse(team._holder_is_live(lock))
            lock.write_text(json.dumps({"pid": os.getpid(), "started": team._proc_start(os.getpid())}))
            self.assertTrue(team._holder_is_live(lock))


    def test_g_eleven_identities_contend_and_a_swe2_lane_is_a_full_worker(self):
        """The team went from four identities to eleven on 2026-09-13. The claim being tested is
        that NOTHING about contention changed - so this asserts the N-way cases across the whole
        expanded set, not the existence of any one lane."""
        b = board()
        self.assertEqual(len(team.AGENTS), 11)
        self.assertEqual(sorted(b["agents"]), sorted(team.AGENTS))
        # the generic SWE2 is gone; its lane carries the name
        self.assertNotIn("SWE2", team.AGENTS)
        self.assertIn("SWE2-CONTRACT", team.AGENTS)

        mine = "SWE2-CONTRACT"
        others = sorted(team.AGENTS - {mine})

        # one resource, eleven possible claimants, exactly one winner
        add(b, "CONTEND", "file:database/shared/one.md")
        act(b, mine, "claim", "CONTEND")
        for other in others:
            self.assertNotIn("CONTEND", [t["id"] for t in team.ready(b, other)])
        add(b, "CONTEND-SAME", "file:database/shared/one.md")
        for other in others:
            with self.assertRaises(ValueError):
                act(b, other, "claim", "CONTEND-SAME")

        # @publication is exclusive across ALL eleven, not just the original three
        add(b, "PUB-ONE", "@publication")
        act(b, mine, "claim", "PUB-ONE")
        add(b, "PUB-OTHER", "@publication")
        for other in others:
            with self.assertRaises(ValueError):
                act(b, other, "claim", "PUB-OTHER")
        act(b, mine, "finish", "PUB-ONE", result_refs=["fixture/commit"])
        act(b, "OPUS", "claim", "PUB-OTHER")

        # @runtime keeps its behaviour with ten other identities present
        add(b, "RT-A", "@runtime")
        act(b, "ASTRA", "claim", "RT-A")
        add(b, "RT-B", "@runtime")
        for other in others:
            with self.assertRaises(ValueError):
                act(b, other, "claim", "RT-B")

        # a request addressed to one lane is claimable by that lane and by nobody else
        req = {"id": "REQ-LANE", "kind": "request", "priority": "P1",
               "target": "bounded offline closure", "scope": "fixture",
               "completion": "result recorded", "dependencies": [],
               "resources": [{"key": "target:offline/one"}],
               "requester": "OPUS", "assigned_to": mine, "question": "Does the fixture match?",
               "known_evidence": "shipping bytes", "missing_information": "the harness",
               "why_it_matters": "a contract turns on it", "what_is_blocked": "OPUS-X"}
        team.apply(b, "OPUS", {"action": "add", "task": req})
        for other in others:
            self.assertNotIn("REQ-LANE", [t["id"] for t in team.ready(b, other)])
        self.assertIn("REQ-LANE", [t["id"] for t in team.ready(b, mine)])
        with self.assertRaises(ValueError):
            act(b, "OPUS", "claim", "REQ-LANE")
        act(b, mine, "claim", "REQ-LANE")

        # only the owner may close it, and closing still needs durable references
        with self.assertRaises(ValueError):
            act(b, "OPUS", "finish", "REQ-LANE", result_refs=["fixture/x"])
        with self.assertRaises(ValueError):
            act(b, mine, "finish", "REQ-LANE", result_refs=[])
        act(b, mine, "finish", "REQ-LANE", result_refs=["fixture/offline-result.md"])
        team.validate(b)

    def test_h_audit_routing_is_ordinary_request_routing(self):
        """REVIEW-POLICY routes a package to SWE2-AUDIT-SEM or -SPEC. That routing must need NO new
        board machinery: an audit is a request addressed to an auditor, and the existing
        recipient and owner-only-close rules have to carry it unchanged."""
        b = board()
        for producer, auditor in (("SWE2-FRONTIER", "SWE2-AUDIT-SEM"),
                                  ("SWE2-DATA", "SWE2-AUDIT-SEM"),
                                  ("SWE2-STRUCT", "SWE2-AUDIT-SPEC"),
                                  ("SWE2-ORACLE", "SWE2-AUDIT-SPEC")):
            rid = "AUDIT-" + producer.split("-", 1)[1]
            req = {"id": rid, "kind": "request", "priority": "P1",
                   "target": "independent audit of a %s package" % producer,
                   "scope": "the evidence, the original code, the tests and the diff",
                   "completion": "ACCEPT / ACCEPT-WITH-NARROWING / REJECT / ESCALATE-*",
                   "dependencies": [], "resources": [{"key": "review:%s/pkg" % producer.lower()}],
                   "requester": producer, "assigned_to": auditor,
                   "question": "Does the evidence support the claim as written?",
                   "known_evidence": "the package", "missing_information": "the auditor's re-derivation",
                   "why_it_matters": "an unaudited claim propagates",
                   "what_is_blocked": "acceptance"}
            team.apply(b, producer, {"action": "add", "task": req})

            # only the named auditor sees it - the PRODUCER cannot audit its own package
            self.assertIn(rid, [t["id"] for t in team.ready(b, auditor)])
            for other in sorted(team.AGENTS - {auditor}):
                self.assertNotIn(rid, [t["id"] for t in team.ready(b, other)])
            with self.assertRaises(ValueError):
                act(b, producer, "claim", rid)

            act(b, auditor, "claim", rid)
            # the producer cannot close its own audit, and a verdict needs durable evidence
            with self.assertRaises(ValueError):
                act(b, producer, "finish", rid, result_refs=["looks fine"])
            with self.assertRaises(ValueError):
                act(b, auditor, "finish", rid, result_refs=[])
            act(b, auditor, "finish", rid, result_refs=["_inbox/%s.md" % producer])
        team.validate(b)

    def test_i_adjudicated_publication_release_keeps_file_claims(self):
        """TEAM.md's stopped-publisher rule: an adjudicator may lift @publication off a stopped
        holder - and only that key - once all three measurements hold. The file claims stay
        with the holder for a same-identity reclaim."""
        from datetime import timedelta
        b = board()
        add(b, "PUB-DEAD", "file:database/pub", resources=[{"key": "@publication"},
                                                          {"key": "file:database/pub"}])
        add(b, "PUB-WAIT", "@publication", assigned_to="SWE2-EC7")
        req = {"id": "ASK-RELEASE", "kind": "request", "priority": "P1",
               "target": "checkpoint or release", "scope": "the lease",
               "completion": "answer", "dependencies": [], "resources": [{"key": "notice:x"}],
               "requester": "SWE2-EC7", "assigned_to": "OPUS",
               "question": "still publishing?", "known_evidence": "silence",
               "missing_information": "a checkpoint", "why_it_matters": "lease is held",
               "what_is_blocked": "PUB-WAIT"}
        team.apply(b, "SWE2-EC7", {"action": "add", "task": req})
        act(b, "OPUS", "claim", "PUB-DEAD")
        past = lambda h: (team.datetime.now(team.timezone.utc)
                          - timedelta(hours=h)).isoformat(timespec="seconds")

        def rel(actor, **kw):
            act(b, actor, "release_publication", "PUB-DEAD", **kw)

        # every gate refuses on the wrong evidence
        with self.assertRaises(ValueError):  # not an adjudicator
            rel("FABLE", unanswered_request="ASK-RELEASE", no_activity_since=past(3))
        with self.assertRaises(ValueError):  # the holder cannot self-release
            rel("OPUS", unanswered_request="ASK-RELEASE", no_activity_since=past(3))
        # the waiting publisher is the next claimant and may never adjudicate -
        # its queued @publication task is assigned to it and unclaimable while
        # the lease is held
        t = next(x for x in b["tasks"] if x["id"] == "PUB-DEAD")
        t["updated_at"] = past(7)
        r = next(x for x in b["tasks"] if x["id"] == "ASK-RELEASE")
        r["updated_at"] = past(3)
        with self.assertRaises(ValueError):
            rel("SWE2-EC7", unanswered_request="ASK-RELEASE", no_activity_since=past(3))
        # fresh checkpoint / fresh request / fresh activity each refuse alone
        t["updated_at"] = team.now()
        with self.assertRaises(ValueError):
            rel("SWE2-FRONTIER", unanswered_request="ASK-RELEASE", no_activity_since=past(3))
        t["updated_at"] = past(7)
        r["updated_at"] = team.now()
        with self.assertRaises(ValueError):
            rel("SWE2-FRONTIER", unanswered_request="ASK-RELEASE", no_activity_since=past(3))
        r["updated_at"] = past(3)
        with self.assertRaises(ValueError):
            rel("SWE2-FRONTIER", unanswered_request="ASK-RELEASE", no_activity_since=past(1))
        # all three measurements hold: the key lifts, nothing else does
        rel("SWE2-FRONTIER", unanswered_request="ASK-RELEASE", no_activity_since=past(3))
        self.assertEqual(t["status"], "ACTIVE")
        self.assertEqual(t["agent"], "OPUS")
        self.assertEqual(team.hold_set(t), [{"key": "file:database/pub"}])
        self.assertEqual(t["resources"][0]["key"], "@publication")  # declared set untouched
        self.assertEqual(t["history"][-1]["event"], "adjudicated @publication release")
        # the waiter's claim now succeeds
        act(b, "SWE2-EC7", "claim", "PUB-WAIT")
        team.validate(b)

    def test_j_retire_is_adjudicated_hygiene_for_dead_request_rows(self):
        """A request row nobody can claim (dependency on a BLOCKED task it exists to
        inform) would sit READY forever; only FRONTIER or OPUS may retire it."""
        b = board()
        add(b, "BLOCKING", "target:x/core")
        req = {"id": "CIRCULAR", "kind": "request", "priority": "P3",
               "target": "corroborate", "scope": "fixture", "completion": "answered",
               "dependencies": ["BLOCKING"], "resources": [{"key": "notice:x"}],
               "requester": "OPUS", "assigned_to": "SWE2-AUDIT-SPEC",
               "question": "?", "known_evidence": "e", "missing_information": "i",
               "why_it_matters": "m", "what_is_blocked": "n"}
        team.apply(b, "OPUS", {"action": "add", "task": req})
        act(b, "SWE2-AUDIT-SEM", "claim", "BLOCKING")
        act(b, "SWE2-AUDIT-SEM", "block", "BLOCKING", resume_when="never in fixture")
        c = next(x for x in b["tasks"] if x["id"] == "CIRCULAR")
        self.assertEqual(c["status"], "READY")  # dependency open, row unclaimable by design
        with self.assertRaises(ValueError):  # not an adjudicator
            act(b, "SWE2-AUDIT-SPEC", "retire", "CIRCULAR")
        with self.assertRaises(ValueError):  # active claims are never retired
            act(b, "SWE2-FRONTIER", "retire", "BLOCKING")
        add(b, "PLAIN", "target:x/plain")
        with self.assertRaises(ValueError):  # research rows keep the normal lifecycle
            act(b, "SWE2-FRONTIER", "retire", "PLAIN")
        act(b, "SWE2-FRONTIER", "retire", "CIRCULAR",
            result_refs=["fixture/the-answer.md"])
        self.assertEqual(c["status"], "DONE")
        self.assertTrue(c["retired"])
        self.assertEqual(c["result_refs"], ["fixture/the-answer.md"])
        team.validate(b)

        # 2026-09-25 wedge: a DONE row without result_refs refused every subsequent
        # apply. A retire with no refs must not reproduce that - `retired` is the
        # marker the DONE-row check accepts instead.
        req2 = dict(req, id="CIRCULAR-NOREFS")
        team.apply(b, "OPUS", {"action": "add", "task": req2})
        act(b, "SWE2-FRONTIER", "retire", "CIRCULAR-NOREFS")
        c2 = next(x for x in b["tasks"] if x["id"] == "CIRCULAR-NOREFS")
        self.assertEqual(c2["status"], "DONE")
        self.assertTrue(c2["retired"])
        self.assertNotIn("result_refs", c2)
        team.validate(b)

    def test_k_a_review_finishes_only_with_one_policy_verdict(self):
        # A16 finish-path gate (OPUS, 2026-09-29; ASTRA-REQ-OPUS-A16-REVIEW-VERDICT-ADMISSION, reproduction 7068c250a):
        # a task carrying a reviews field may go DONE only with exactly one whole-string verdict:<V> ref.
        b = board()
        rv = {"author": "OPUS", "commit": "abc1234", "record": "_index/candidates/x/README.md"}
        def req(i):
            t = {"id": i, "kind": "request", "priority": "P2", "requester": "OPUS", "assigned_to": "SWE2-AUDIT-SPEC",
                 "target": "t", "scope": "s", "question": "q", "known_evidence": "e", "missing_information": "m",
                 "why_it_matters": "w", "what_is_blocked": "b", "completion": "c", "dependencies": [],
                 "resources": [{"key": "request:" + i.lower()}], "reviews": rv}
            team.apply(b, "OPUS", {"action": "add", "task": t})
            act(b, "SWE2-AUDIT-SPEC", "claim", i)
        for i, refs in (("R-NONE", ["file:review.md"]), ("R-LF", ["verdict:ACCEPT\n", "file:r.md"]),
                        ("R-TWO", ["verdict:ACCEPT", "verdict:REJECT"]), ("R-PARTIAL", ["verdict:PARTIAL", "file:r.md"]),
                        ("R-LOWER", ["verdict:accept"])):
            req(i)
            with self.assertRaises(ValueError, msg=i):
                act(b, "SWE2-AUDIT-SPEC", "finish", i, result_refs=refs)
            self.assertEqual(next(x for x in b["tasks"] if x["id"] == i)["status"], "ACTIVE", i)
        for i, v in (("R-ACC", "ACCEPT"), ("R-NAR", "ACCEPT-WITH-NARROWING"), ("R-REJ", "REJECT"), ("R-ESC", "ESCALATE-OPUS")):
            req(i)
            act(b, "SWE2-AUDIT-SPEC", "finish", i, result_refs=["verdict:" + v, "file:r.md"])
            self.assertEqual(next(x for x in b["tasks"] if x["id"] == i)["status"], "DONE", i)
        # the refusal path leaves an inconclusive review open for checkpoint/block/release, and a task WITHOUT reviews is
        # unaffected (no verdict demanded of ordinary research)
        act(b, "SWE2-AUDIT-SPEC", "release", "R-NONE")
        add(b, "PLAIN", "target:plain")
        act(b, "FABLE", "claim", "PLAIN")
        act(b, "FABLE", "finish", "PLAIN", result_refs=["commit:abc1234"])
        team.validate(b)


if __name__ == "__main__":
    unittest.main(verbosity=2)
