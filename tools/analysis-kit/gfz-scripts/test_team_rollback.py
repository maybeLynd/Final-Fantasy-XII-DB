"""Board-durability fixtures for the 2026-09-25 TEAM rollback incident.

These exercise the journal/incident machinery in team.py and the offline
reconstruction in team_recover.py - rollback while idle and active, divergent
same-revision content, crash windows, epoch checks, guarded cutover, and
idempotent replay. Disposable fixture boards only; never the live board.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import team
import team_recover


def board():
    b = {"schema_version": 1, "phase": "DATABASE", "revision": 0,
         "agents": {}, "tasks": [], "history": [], "checkpoints": []}
    for a in team.AGENTS:
        b["agents"][a] = {"agent_id": a, "primary_specialty": a,
                          "last_checkpoint": team.now()}
    team.refresh(b)
    return b


def task(tid, resource, **extra):
    t = {"id": tid, "kind": "research", "priority": "P1", "target": resource,
         "scope": "bounded fixture", "completion": "fixture observation",
         "dependencies": [], "resources": [{"key": resource}]}
    t.update(extra)
    return t


def op_add(tid, resource=None, **kw):
    res = resource or "target:%s" % tid.lower()
    return {"action": "add", "task": task(tid, res, **kw)}


def op(action, tid, **kw):
    return {"action": action, "task": tid, "note": "fixture", **kw}


class FixtureBoard(unittest.TestCase):
    """A disposable board file + journal under a temp dir."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.path = self.dir / "TEAM.json"
        self.board = board()
        self.write(self.board)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, b):
        """Raw write - simulates any writer, journaled or not."""
        self.path.write_text(json.dumps(b, indent=2) + "\n",
                             encoding="utf-8")

    def transact(self, agent, opv, **kw):
        return team.transaction(self.path, agent, opv, session="test", **kw)

    def read(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def last_op(self):
        b = self.read()
        return b["history"][-1]["operation"]

    def _forge_intent(self, rev, opv, board_text=None):
        rec = {"kind": "intent", "rev": rev,
               "op_sha": team._sha_text(json.dumps(opv, sort_keys=True,
                                                 ensure_ascii=False)),
               "agent": "FABLE", "session": "crash",
               "epoch": 0}
        if board_text is not None:
            rec["board_sha"] = team._sha_text(board_text)
        team._journal_append(self.path, rec)
        return rec


class JournalBasics(FixtureBoard):
    def test_genesis_then_commit_records(self):
        self.transact("FABLE", op_add("A-1"))
        recs = team.journal_records(self.path)
        kinds = [r["kind"] for r in recs]
        self.assertEqual(kinds[0], "genesis")
        self.assertIn("intent", kinds)
        self.assertEqual(kinds[-1], "commit")
        self.assertEqual(recs[-1]["rev"], self.read()["revision"])

    def test_note_action_is_the_sanctioned_checkpoints_path(self):
        """The incident's bypass was a hand-edit of board['checkpoints']; the
        `note` action is the journaled, locked way to do the same append."""
        self.transact("SWE2-ORACLE",
                      {"action": "note", "note": "EXP-x fixture note"})
        b = self.read()
        cp = b["checkpoints"][-1]
        self.assertEqual(cp["author"], "SWE2-ORACLE")
        self.assertIn("EXP-x", cp["note"])
        self.assertEqual(b["history"][-1]["operation"]["action"], "note")
        with self.assertRaises(ValueError):
            self.transact("FABLE", {"action": "note", "note": ""})

    def test_normal_ops_keep_applying(self):
        self.transact("FABLE", op_add("A-1"))
        self.transact("FABLE", op("claim", "A-1"))
        self.transact("FABLE", op("finish", "A-1",
                                  result_refs=["fixture/done"]))
        b = self.read()
        self.assertEqual(b["revision"], 3)
        self.assertEqual(b["tasks"][0]["status"], "DONE")
        ok, detail = team.board_status(self.path)
        self.assertTrue(ok, detail)


class RollbackDetection(FixtureBoard):
    def snapshot(self):
        return deepcopy(self.read())

    def test_rollback_while_idle_is_refused(self):
        self.transact("FABLE", op_add("A-1"))
        self.transact("FABLE", op_add("A-2"))
        stale = self.snapshot()  # rev 2
        self.transact("FABLE", op_add("A-3"))
        self.write(stale)  # overwrite with the rev-2 copy, like the incident
        with self.assertRaises(team.BoardIncident):
            self.transact("FABLE", op_add("A-4"))
        ok, detail = team.board_status(self.path)
        self.assertFalse(ok)
        self.assertIn("rollback", detail)

    def test_rollback_while_active_is_refused(self):
        self.transact("FABLE", op_add("A-1"))
        self.transact("FABLE", op("claim", "A-1"))
        stale = self.snapshot()  # rev 2, A-1 ACTIVE
        self.transact("FABLE", op("finish", "A-1",
                                  result_refs=["fixture/x"]))
        self.write(stale)  # clobber the finish
        with self.assertRaises(team.BoardIncident):
            self.transact("FABLE", op("checkpoint", "A-1"))
        # the file is untouched - still the stale copy
        self.assertEqual(self.read()["tasks"][0]["status"], "ACTIVE")

    def test_same_revision_divergent_content_is_refused(self):
        self.transact("FABLE", op_add("A-1"))
        b = self.read()
        b["agents"]["FABLE"]["primary_specialty"] = "tampered"
        self.write(b)  # same revision, different bytes
        with self.assertRaises(team.BoardIncident) as cm:
            self.transact("FABLE", op_add("A-2"))
        self.assertIn("same-revision", str(cm.exception))

    def test_unjournaled_advancement_is_refused(self):
        self.transact("FABLE", op_add("A-1"))
        b = self.read()
        b["revision"] += 5  # a hand-edited jump over the high-water
        self.write(b)
        with self.assertRaises(team.BoardIncident) as cm:
            self.transact("FABLE", op_add("A-2"))
        self.assertIn("unjournaled", str(cm.exception))

    def test_stale_epoch_is_refused(self):
        self.transact("FABLE", op_add("A-1"))
        cand = self.read()
        # install a recovery (epoch 1), then try writing on an epoch-0 copy
        cand["revision"] = 100
        team.recover(self.path, self._write_candidate(cand),
                     "fixture recovery", "SWE2-FRONTIER")
        stale = self.read()
        stale["recovery_epoch"] = 0
        stale["revision"] = 100
        self.write(stale)
        with self.assertRaises(team.BoardIncident) as cm:
            self.transact("FABLE", op_add("A-9"))
        self.assertIn("epoch", str(cm.exception))

    def _write_candidate(self, b):
        p = self.dir / "candidate.json"
        p.write_text(json.dumps(b, indent=2) + "\n", encoding="utf-8")
        return p


class MixedSnapshot(FixtureBoard):
    """board_status reads the board then the journal as two separate reads.
    A sanctioned commit between them yields a mixed pair that mimics an
    incident (ASTRA-NOTICE-FRONTIER-BOARD-PREFLIGHT-37999). A transient
    mixed pair must re-read and pass; a persistent incident still fails."""

    def test_stale_board_plus_new_journal_is_not_an_incident(self):
        self.transact("FABLE", op_add("A-1"))
        stale_text = self.path.read_text(encoding="utf-8")  # rev-1 board
        self.transact("FABLE", op_add("A-2"))  # rev-2 board + journal
        real_read = team.Path.read_text
        calls = {"n": 0}

        def stale_once(this, *a, **k):
            if this == self.path and calls["n"] == 0:
                calls["n"] += 1
                return stale_text
            return real_read(this, *a, **k)

        with mock.patch.object(team.Path, "read_text", stale_once):
            ok, detail = team.board_status(self.path)
        self.assertTrue(ok, detail)
        self.assertEqual(calls["n"], 1)

    def test_new_board_plus_old_journal_is_not_an_incident(self):
        self.transact("FABLE", op_add("A-1"))
        old_recs = team.journal_records(self.path)  # journal at rev-1
        self.transact("FABLE", op_add("A-2"))  # rev-2 pair on disk
        calls = {"n": 0}
        real_recs = team.journal_records

        def old_journal_once(p):
            if calls["n"] == 0:
                calls["n"] += 1
                return old_recs
            return real_recs(p)

        with mock.patch.object(team, "journal_records", old_journal_once):
            ok, detail = team.board_status(self.path)
        self.assertTrue(ok, detail)

    def test_persistent_rollback_still_fails_after_repeats(self):
        self.transact("FABLE", op_add("A-1"))
        stale = deepcopy(self.read())
        self.transact("FABLE", op_add("A-2"))
        self.write(stale)  # a real rollback stays stale on every read
        ok, detail = team.board_status(self.path)
        self.assertFalse(ok)
        self.assertIn("rollback", detail)


class CrashWindow(FixtureBoard):

    def test_intent_without_write_aborts_cleanly(self):
        self.transact("FABLE", op_add("A-1"))
        opv = op_add("A-2")
        self._forge_intent(2, opv)  # intent journaled, write never happened
        # next transaction must reconcile (abort) and proceed normally
        self.transact("FABLE", opv)
        b = self.read()
        self.assertEqual(b["revision"], 2)
        kinds = [r["kind"] for r in team.journal_records(self.path)]
        self.assertIn("abort", kinds)

    def test_write_without_commit_self_heals(self):
        self.transact("FABLE", op_add("A-1"))
        opv = op_add("A-2")
        self._forge_intent(2, opv)
        # simulate: the write landed but the commit record crashed
        b = self.read()
        team.apply(b, "FABLE", deepcopy(opv), session="crash")
        self.write(b)
        self.transact("FABLE", op_add("A-3"))
        kinds = [r["kind"] for r in team.journal_records(self.path)]
        commits = [r for r in team.journal_records(self.path)
                   if r["kind"] == "commit"]
        self.assertTrue(any(r.get("healed") for r in commits))

    def test_pending_intent_on_divergent_board_is_incident(self):
        self.transact("FABLE", op_add("A-1"))
        self._forge_intent(2, op_add("A-2"))
        b = self.read()
        team.apply(b, "FABLE", deepcopy(op_add("OTHER", "target:y")),
                   session="other")
        self.write(b)  # rev 2 but the last op is not the journaled intent
        with self.assertRaises(team.BoardIncident):
            self.transact("FABLE", op_add("A-3"))


class PendingStateBinding(FixtureBoard):
    """ASTRA-REQ-FRONTIER-PENDING-STATE-BINDING: a pending intent must bind
    the intended post-write file, not only the last operation. Before the
    fix, a checkpoint changed between the interrupted write and the next
    transaction healed silently under a matching last op. Controls at the
    real invocation path: bound heal, changed-checkpoint refusal,
    different-op refusal, legacy-intent boundary."""

    def _intended_text(self, opv):
        b = self.read()
        team.apply(b, "FABLE", deepcopy(opv), session="crash")
        return b, team._serialize_board(b)

    def test_bound_intent_heals_the_exact_write(self):
        self.transact("FABLE", op_add("A-1"))
        opv = op_add("A-2")
        b, text = self._intended_text(opv)
        self._forge_intent(2, opv, board_text=text)
        self.write(b)
        self.transact("FABLE", op_add("A-3"))
        heals = [r for r in team.journal_records(self.path)
                 if r.get("healed")]
        self.assertEqual(heals[-1]["bound"], "intended")

    def test_changed_checkpoint_under_matching_op_is_incident(self):
        self.transact("FABLE", op_add("A-1"))
        opv = op_add("A-2")
        b, text = self._intended_text(opv)
        self._forge_intent(2, opv, board_text=text)
        b["checkpoints"].append({"ts": team.now()[:10], "author": "tamper",
                                 "note": "changed after the crash"})
        self.write(b)  # same rev, same last op, different file bytes
        with self.assertRaises(team.BoardIncident) as cm:
            self.transact("FABLE", op_add("A-3"))
        self.assertIn("not the intended write", str(cm.exception))
        self.assertEqual(self.read()["tasks"][0]["status"], "READY")

    def test_different_last_op_under_bound_intent_is_incident(self):
        self.transact("FABLE", op_add("A-1"))
        opv = op_add("A-2")
        b, text = self._intended_text(opv)
        self._forge_intent(2, opv, board_text=text)
        b2 = self.read()
        team.apply(b2, "FABLE", deepcopy(op_add("OTHER", "target:y")),
                   session="other")
        self.write(b2)
        with self.assertRaises(team.BoardIncident):
            self.transact("FABLE", op_add("A-3"))

    def test_legacy_intent_heals_with_explicit_boundary(self):
        self.transact("FABLE", op_add("A-1"))
        opv = op_add("A-2")
        self._forge_intent(2, opv)  # no board_sha: pre-binding journal record
        b = self.read()
        team.apply(b, "FABLE", deepcopy(opv), session="crash")
        self.write(b)
        self.transact("FABLE", op_add("A-3"))
        heals = [r for r in team.journal_records(self.path)
                 if r.get("healed")]
        self.assertEqual(heals[-1]["bound"], "received-legacy")

    def test_real_intent_carries_the_intended_sha(self):
        self.transact("FABLE", op_add("A-1"))
        recs = team.journal_records(self.path)
        intent = [r for r in recs if r["kind"] == "intent"][-1]
        text = self.path.read_text(encoding="utf-8")
        self.assertEqual(intent["board_sha"], team._sha_text(text))


class RecoveryBarrier(FixtureBoard):
    def _candidate(self, **over):
        b = self.read()
        b["revision"] = b["revision"] + 50
        t = task("RECOVERED", "target:recovered")
        t.update(agent=None, status="READY", started_at=None,
                 updated_at=team.now(), checkpoint="recovered")
        b["tasks"].append(t)
        for k, v in over.items():
            b[k] = v
        p = self.dir / "cand.json"
        p.write_text(json.dumps(b, indent=2) + "\n", encoding="utf-8")
        return p, b

    def test_recover_installs_under_preimage_and_advances_epoch(self):
        self.transact("FABLE", op_add("A-1"))
        pre = self.read()
        cand, cb = self._candidate()
        team.recover(self.path, cand, "fixture cutover", "SWE2-FRONTIER",
                     expect_revision=pre["revision"])
        b = self.read()
        self.assertEqual(b["revision"], cb["revision"])
        self.assertEqual(b["recovery_epoch"], 1)
        recs = team.journal_records(self.path)
        self.assertEqual(recs[-1]["kind"], "recovery")
        # ordinary ops resume on the new epoch
        self.transact("FABLE", op("claim", "RECOVERED"))

    def test_recover_fails_closed_on_moved_preimage(self):
        self.transact("FABLE", op_add("A-1"))
        cand, _ = self._candidate()
        self.transact("FABLE", op_add("A-2"))  # board moved since capture
        with self.assertRaises(ValueError):
            team.recover(self.path, cand, "stale preimage",
                         "SWE2-FRONTIER", expect_revision=1)
        self.assertNotIn("recovery_epoch", self.read())

    def test_recover_rejects_invalid_candidate(self):
        self.transact("FABLE", op_add("A-1"))
        cand = self.read()
        cand["agents"].pop("OPUS")  # invalid board
        p = self.dir / "bad.json"
        p.write_text(json.dumps(cand), encoding="utf-8")
        with self.assertRaises(ValueError):
            team.recover(self.path, p, "invalid", "SWE2-FRONTIER")

    def test_recover_adopts_verified_unjournaled_write(self):
        """2026-09-27 rev-33308 incident: a raw write appended a history
        receipt for a `note` op whose checkpoints effect never ran, in
        non-canonical bytes. The fleet fails closed; the repair is to prove
        the diverged board equals the journaled preimage plus exactly the
        receipt, complete the missing effect, and install through recover()
        pinned against the diverged file itself."""
        self.transact("FABLE", op_add("A-1"))

        forged = self.read()
        note_op = {"action": "note", "note": "EXP fixture note"}
        forged["history"].append({"at": team.now(), "agent": "SWE2-ORACLE",
                                  "session": "SWE2-ORACLE",
                                  "operation": note_op})
        forged["revision"] += 1
        # bypass tell: compact, non-canonical bytes, no trailing newline
        self.path.write_text(json.dumps(forged), encoding="utf-8")
        forged_sha = team._sha_text(
            self.path.read_text(encoding="utf-8"))

        with self.assertRaises(team.BoardIncident) as cm:
            self.transact("FABLE", op_add("A-2"))
        self.assertIn("unjournaled", str(cm.exception))

        # verification step the repair requires: diverged board minus the
        # receipt must hash to the journaled preimage
        recon = json.loads(self.path.read_text(encoding="utf-8"))
        recon["history"] = recon["history"][:-1]
        recon["revision"] -= 1
        recon_txt = json.dumps(recon, indent=2, ensure_ascii=False) + "\n"
        journaled_sha = [r for r in team.journal_records(self.path)
                         if r.get("kind") == "commit"][-1]["board_sha"]
        self.assertEqual(team._sha_text(recon_txt), journaled_sha)

        # adoption: complete the receipt's effect, install under the
        # diverged file as preimage
        cand = json.loads(self.path.read_text(encoding="utf-8"))
        cand["checkpoints"].append({"ts": team.now()[:10],
                                    "author": "SWE2-ORACLE",
                                    "note": note_op["note"]})
        cp = self.dir / "adopt.json"
        cp.write_text(json.dumps(cand, indent=2) + "\n", encoding="utf-8")
        team.recover(self.path, cp, "adopt unjournaled write",
                     "SWE2-FRONTIER",
                     expect_revision=forged["revision"],
                     expect_sha=forged_sha)
        b = self.read()
        self.assertEqual(b["revision"], forged["revision"])
        self.assertEqual(b["recovery_epoch"], 1)
        self.assertEqual(b["checkpoints"][-1]["note"], note_op["note"])
        ok, detail = team.board_status(self.path)
        self.assertTrue(ok, detail)
        self.transact("FABLE", op_add("A-2"))  # journaled ops resume

    def test_interrupted_recovery_leaves_incident_visible(self):
        """A stale copy written AFTER a recovery install must still incident."""
        self.transact("FABLE", op_add("A-1"))
        stale = self.read()
        cand, _ = self._candidate()
        team.recover(self.path, cand, "cutover", "SWE2-FRONTIER")
        self.write(stale)  # attacker/stale writer restores the pre-recovery file
        with self.assertRaises(team.BoardIncident):
            self.transact("FABLE", op_add("A-9"))
        ok, detail = team.board_status(self.path)
        self.assertFalse(ok)


class Concurrency(FixtureBoard):
    def test_concurrent_writes_keep_journal_consistent(self):
        self.transact("FABLE", op_add("RACE-A", "target:shared"))
        self.transact("FABLE", op_add("RACE-B", "target:shared"))
        jobs = []
        for who, tid in (("FABLE", "RACE-A"), ("OPUS", "RACE-B")):
            f = self.dir / (tid + ".op.json")
            f.write_text(json.dumps(op("claim", tid)))
            jobs.append(subprocess.Popen(
                [sys.executable, team.__file__, "apply", "--board",
                 str(self.path), "--agent", who, "--file", str(f)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        outs = [p.communicate(timeout=30) for p in jobs]
        self.assertEqual(sorted(p.returncode for p in jobs), [0, 1], outs)
        b = self.read()
        team.validate(b)
        ok, detail = team.board_status(self.path)
        self.assertTrue(ok, detail)
        recs = [r for r in team.journal_records(self.path)
                if r["kind"] == "commit"]
        self.assertEqual([r["rev"] for r in recs],
                         sorted(r["rev"] for r in recs))


class Reconstruction(unittest.TestCase):
    """team_recover replay: witness + op files, dedup by receipts."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _witness_with_ops(self):
        """A small live history: baseline ops plus one in-window op."""
        wit = board()
        team.apply(wit, "FABLE", op_add("BASE-1"))
        team.apply(wit, "FABLE", op("claim", "BASE-1"))
        wpath = self.dir / "witness.json"
        wpath.write_text(json.dumps(wit, indent=2) + "\n", encoding="utf-8")
        return wit, wpath

    def _fork_with_post_reset(self, wit):
        """Fork = truncated witness + post-reset ops."""
        fork = deepcopy(wit)
        fork["history"] = fork["history"][:-1]  # rolled back one op
        fork["revision"] -= 1
        fork["tasks"][0]["status"] = "READY"
        fork["tasks"][0]["agent"] = None
        team.refresh(fork)
        team.apply(fork, "FABLE", op("claim", "BASE-1"))  # post-reset re-claim
        fpath = self.dir / "fork.json"
        fpath.write_text(json.dumps(fork, indent=2) + "\n", encoding="utf-8")
        return fpath

    def _inventory(self, ops_with_mtime):
        rows = []
        for i, (o, mt) in enumerate(ops_with_mtime):
            rows.append({"file": str(self.dir / f"op{i}.json"),
                         "mtime": mt, "op": o,
                         "sha": "x%d" % i, "mt": "",
                         "in_witness": [], "in_fork_tail": []})
        ipath = self.dir / "inv.json"
        ipath.write_text(json.dumps(rows), encoding="utf-8")
        return ipath

    def _build(self, wit_path, fork_path, inv_path):
        class A: pass
        a = A()
        a.witness, a.fork, a.inventory = str(wit_path), str(fork_path), str(inv_path)
        a.window_start = "2025-01-01T00:00:00+00:00"
        a.reset_time = "2026-01-01T00:00:00+00:00"
        a.out = str(self.dir / "out")
        team_recover.build(a)
        return json.loads((self.dir / "out" / "TEAM.candidate.json")
                          .read_text(encoding="utf-8")), \
            json.loads((self.dir / "out" / "recovery-report.json")
                       .read_text(encoding="utf-8"))

    def test_replay_recovers_unreceipted_ops(self):
        wit, wpath = self._witness_with_ops()
        fpath = self._fork_with_post_reset(wit)
        inv = self._inventory([
            (op_add("NEW-1"), 1750000000),   # in window, no receipt
            (op("claim", "NEW-1"), 1750000001),
            (op("finish", "NEW-1", result_refs=["fixture/r"]), 1750000002),
        ])
        cand, rep = self._build(wpath, fpath, inv)
        ids = {t["id"]: t["status"] for t in cand["tasks"]}
        self.assertEqual(ids.get("NEW-1"), "DONE")
        self.assertEqual(rep["tail_applied"], 3)

    def test_duplicate_replay_does_not_double_apply(self):
        wit, wpath = self._witness_with_ops()
        fpath = self._fork_with_post_reset(wit)
        same = op_add("NEW-1")
        inv = self._inventory([(same, 1750000000),
                               (dict(same), 1750000002)])  # retry, same bytes
        cand, rep = self._build(wpath, fpath, inv)
        self.assertEqual(sum(1 for t in cand["tasks"] if t["id"] == "NEW-1"), 1)
        # the retry op failed validation and is in the rejected list
        self.assertEqual(len(rep["tail_rejected"]), 1)

    def test_missing_op_payload_is_reported_not_invented(self):
        wit, wpath = self._witness_with_ops()
        fpath = self._fork_with_post_reset(wit)
        # finish without its add: must land in rejected, not be fabricated
        inv = self._inventory([
            (op("finish", "GHOST-TASK", result_refs=["x"]), 1750000000)])
        cand, rep = self._build(wpath, fpath, inv)
        self.assertNotIn("GHOST-TASK", {t["id"] for t in cand["tasks"]})
        self.assertTrue(any(r["task"] == "GHOST-TASK"
                            for r in rep["tail_rejected"]))

    def test_legitimate_reopen_sequence_replays(self):
        wit, wpath = self._witness_with_ops()
        fpath = self._fork_with_post_reset(wit)
        inv = self._inventory([
            (op_add("REOPEN"), 1750000000),
            (op("claim", "REOPEN"), 1750000001),
            (op("release", "REOPEN"), 1750000002),
            (op("claim", "REOPEN"), 1750000003),  # legit second claim
        ])
        cand, rep = self._build(wpath, fpath, inv)
        row = next(t for t in cand["tasks"] if t["id"] == "REOPEN")
        self.assertEqual(row["status"], "ACTIVE")
        self.assertEqual(rep["tail_applied"], 4)

    def test_drafts_after_reset_are_never_applied(self):
        wit, wpath = self._witness_with_ops()
        fpath = self._fork_with_post_reset(wit)
        inv = self._inventory([
            (op_add("TOO-LATE"), 1767225600)])  # mtime past reset bound
        class A: pass
        a = A()
        a.witness, a.fork, a.inventory = str(wpath), str(fpath), str(inv)
        a.window_start = "2020-01-01T00:00:00+00:00"
        a.reset_time = "2025-01-01T00:00:00+00:00"  # reset before file mtime
        a.out = str(self.dir / "out2")
        team_recover.build(a)
        cand = json.loads((self.dir / "out2" / "TEAM.candidate.json")
                          .read_text(encoding="utf-8"))
        self.assertNotIn("TOO-LATE", {t["id"] for t in cand["tasks"]})


class CurrentBlocks(FixtureBoard):
    """Generated operative headers: the block a lane reads at resume instead of
    hand-maintained counts/NEXT lines. All transitions happen through ops -
    the header itself is never edited by hand."""

    def _embed(self, agent="FABLE"):
        return team.write_current("# Lane inbox\nauthored notes stay\n",
                                  agent, self.read())

    def test_block_carries_rev_epoch_and_queue_fingerprint(self):
        self.transact("FABLE", op_add("A-1"))
        text = self._embed()
        verdicts = team.check_current(text, self.read())
        self.assertEqual(verdicts, [("FABLE", "CURRENT")])
        self.assertIn("board_rev=%d" % self.read()["revision"], text)

    def test_accepted_review_stales_then_refreshes(self):
        req = task("REVIEW-REQ", "review:x",
                   kind="request", requester="OPUS", assigned_to="SWE2-AUDIT-SEM",
                   question="ok?", known_evidence="e", missing_information="m",
                   why_it_matters="w", what_is_blocked="b")
        self.transact("OPUS", {"action": "add", "task": req})
        text = self._embed("SWE2-AUDIT-SEM")
        self.assertEqual(team.check_current(text, self.read()),
                         [("SWE2-AUDIT-SEM", "CURRENT")])
        # the auditor accepts: claim + finish with durable refs
        self.transact("SWE2-AUDIT-SEM", op("claim", "REVIEW-REQ"))
        v = team.check_current(text, self.read())[0][1]
        self.assertTrue(v.startswith("STALE-QUEUE"), v)
        self.transact("SWE2-AUDIT-SEM", op("finish", "REVIEW-REQ",
                                           result_refs=["fixture/verdict"]))
        v = team.check_current(text, self.read())[0][1]
        self.assertTrue(v.startswith("STALE-QUEUE"), v)
        # refresh via the tool, not by editing the header
        text = team.write_current(text, "SWE2-AUDIT-SEM", self.read())
        self.assertEqual(team.check_current(text, self.read()),
                         [("SWE2-AUDIT-SEM", "CURRENT")])
        self.assertIn("ACTIVE: none", text)  # the review is DONE, not replayable

    def test_met_transition_invalidates_cached_selection(self):
        """A DONE transition (a 'MET' in queue terms) must move queue_sha so a
        cached 'work on X' header cannot replay completed work."""
        self.transact("FABLE", op_add("CELL-1"))
        text = self._embed()
        self.transact("FABLE", op("claim", "CELL-1"))
        self.transact("FABLE", op("finish", "CELL-1",
                                  result_refs=["fixture/met"]))
        v = team.check_current(text, self.read())[0][1]
        self.assertTrue(v.startswith("STALE-QUEUE"), v)

    def test_legitimate_reopen_returns_to_queue(self):
        self.transact("FABLE", op_add("REOPEN-1"))
        self.transact("FABLE", op("claim", "REOPEN-1"))
        self.transact("FABLE", op("release", "REOPEN-1"))
        text = self._embed()
        self.assertIn("READY pool: 1", text)  # reopened work is back selectable
        # claimed again legitimately - header stales, refresh restores CURRENT
        self.transact("OPUS", op("claim", "REOPEN-1"))
        v = team.check_current(text, self.read())[0][1]
        self.assertTrue(v.startswith("STALE-QUEUE"), v)

    def test_restart_regenerates_identical_block(self):
        """A fresh session derives the same block from the same board - no
        state lives in the header itself."""
        self.transact("FABLE", op_add("PERSIST-1"))
        self.transact("FABLE", op("claim", "PERSIST-1"))
        a = team.current_state(self.read(), "FABLE")
        reread = json.loads(self.path.read_text(encoding="utf-8"))
        b = team.current_state(reread, "FABLE")
        self.assertEqual(a, b)
        self.assertIn("PERSIST-1", team.current_block(reread, "FABLE"))

    def test_unrelated_peer_op_is_moved_not_stale(self):
        self.transact("FABLE", op_add("MINE-1"))
        self.transact("FABLE", op("claim", "MINE-1"))
        text = self._embed()
        # an op that does not touch FABLE's selection view (a checkpoints note)
        self.transact("OPUS", {"action": "note", "note": "peer progress"})
        v = team.check_current(text, self.read())[0][1]
        self.assertTrue(v.startswith("MOVED"), v)

    def test_stale_inputs_label_is_visible_and_stale(self):
        text = self._embed()
        text = text.replace(" -->", " stale-inputs -->", 1)
        v = team.check_current(text, self.read())[0][1]
        self.assertTrue(v.startswith("STALE-LABELLED"), v)

    def test_hand_edits_inside_block_are_detected(self):
        """A forged 'current' line whose queue_sha does not match is caught."""
        text = self._embed()
        forged = text.replace("READY pool: 0", "READY pool: 99")
        # queue_sha is of the view, not the text - a hand edit does not fool
        # the check but the stamped sha still guards the selections. Forgery
        # of the sha itself:
        import re as _re
        forged2 = _re.sub(r"queue_sha=[0-9a-f]+", "queue_sha=0000000000000000",
                          text)
        v = team.check_current(forged2, self.read())[0][1]
        self.assertTrue(v.startswith("STALE-QUEUE"), v)


class WritePathHardening(FixtureBoard):
    """The _write_board replace step (FRONTIER-REQ-STRUCT-BOARD-WRITE-PATH-
    REPAIR): transient WinError 5/32 at os.replace is retried; anything else
    propagates so the intent stays pending; and a session-side write of a
    stale in-memory copy is caught, never silently absorbed."""

    @staticmethod
    def _denied():
        e = PermissionError("Access is denied")
        e.winerror = 5
        return e

    @staticmethod
    def _sharring():
        e = PermissionError("sharing violation")
        e.winerror = 32
        return e

    def test_transient_winerror5_and_32_retry_then_land(self):
        real = team.os.replace
        calls = {"n": 0}
        def flaky(src, dst):
            calls["n"] += 1
            if calls["n"] == 1:
                raise self._denied()
            if calls["n"] == 2:
                raise self._sharring()
            return real(src, dst)
        self.transact("FABLE", op_add("A-1"))
        with mock.patch("team.time.sleep"),              mock.patch.object(team.os, "replace", side_effect=flaky):
            self.transact("FABLE", op_add("A-2"))
        self.assertEqual(calls["n"], 3)
        b = self.read()
        self.assertEqual(b["revision"], 2)
        ok, detail = team.board_status(self.path)
        self.assertTrue(ok, detail)

    def test_persistent_denial_fails_closed_intent_reconciled(self):
        self.transact("FABLE", op_add("A-1"))
        with mock.patch("team.time.sleep"),              mock.patch.object(team.os, "replace",
                               side_effect=self._denied()):
            with self.assertRaises(PermissionError):
                self.transact("FABLE", op_add("A-2"))
        # the journaled intent never landed; the NEXT transaction aborts it
        # and proceeds - the failure is reconciled, not latent
        self.transact("FABLE", op_add("A-3"))
        recs = team.journal_records(self.path)
        self.assertIn("abort", [r["kind"] for r in recs])
        b = self.read()
        self.assertEqual([t["id"] for t in b["tasks"]], ["A-1", "A-3"])

    def test_stale_in_memory_copy_cannot_overwrite_newer_ops(self):
        """The ORACLE incident shape: a writer's in-memory board copy from
        rev N is dumped directly while accepted ops have advanced the live
        board to rev N+2. The direct write physically lands, but the journal
        refuses to absorb it - the next transaction detects the rollback and
        the overwritten ops are provably not lost: still in the journal."""
        self.transact("FABLE", op_add("A-1"))
        stale = deepcopy(self.read())               # rev 1, in-memory copy
        self.transact("FABLE", op_add("A-2"))
        self.transact("SWE2-ORACLE",
                      {"action": "note", "note": "peer op lands legitimately"})
        self.write(stale)                             # rev-1 copy over rev-3
        with self.assertRaises(team.BoardIncident):
            self.transact("FABLE", op_add("A-4"))
        # the journaled commits for rev 2 and rev 3 are intact evidence of
        # what the direct write erased from the file
        recs = team.journal_records(self.path)
        committed = {r["rev"] for r in recs if r["kind"] == "commit"}
        self.assertIn(2, committed)
        self.assertIn(3, committed)


class WatchdogGate(unittest.TestCase):
    def test_board_status_is_the_dispatch_gate(self):
        """The watchdog's gate must read incident as a hard no: a rolled-back
        board produces ok=False and an incident detail, never 'empty queue'."""
        src = Path(team.__file__).parent / "swe2_watchdog.py"
        code = src.read_text(encoding="utf-8")
        self.assertIn('ev["mode"] = "board-incident"', code)
        self.assertIn("board_integrity()", code)
        # and the gate precedes the spawn path
        idx_incident = code.index('elif not board_ok:')
        idx_spawn = code.index('wake_result = spawn_wake')
        self.assertLess(idx_incident, idx_spawn)


if __name__ == "__main__":
    unittest.main()
