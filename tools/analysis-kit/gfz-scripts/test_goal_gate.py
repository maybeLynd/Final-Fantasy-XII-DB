"""Fixtures for the false-/goal-completion fix: the gate, the Stop hook, and
resume classification. Disposable trees only -- no live claims, no real lanes.

Covered: the two observed false completions ("three packages; next RNG
contract", "UQ-289 reframed"), stale acceptance, uncommitted self-certificates,
compaction/resume, user cancellation, hard limits, and a valid terminal
receipt passing.
"""
import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import goal_gate as G          # noqa: E402
import goal_gate_hook as H     # noqa: E402
import goal_resume as R        # noqa: E402

DB_COND = ("GOAL: Complete the whole FF12 knowledge database to the accepted "
           "L1+L2 reconstruction-grade standard.")
OTHER_COND = "The task is complete when fixture_done.txt exists."


def w(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                       text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


class FixtureRepo:
    """A scratch git repo holding only the paths the gate reads."""

    def __init__(self, root):
        self.root = root
        self.db = os.path.join(root, "Database", "FFXII TZA")
        os.makedirs(os.path.join(self.db, "_index"), exist_ok=True)
        git(root, "init", "-q")
        git(root, "config", "user.email", "fixture@x")
        git(root, "config", "user.name", "fixture")
        git(root, "config", "commit.gpgsign", "false")

    def commit_all(self):
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "fixture")
        return git(self.root, "rev-parse", "HEAD")


def hook_in(transcript, session="fixture-1", stop_active=False):
    return json.dumps({"hook_event_name": "Stop", "session_id": session,
                       "transcript_path": transcript,
                       "stop_hook_active": stop_active,
                       "last_assistant_message": "packages published; next: RNG contract",
                       "cwd": "fixture"})


def run_hook(inp):
    import io, contextlib
    buf = io.StringIO()
    stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        with contextlib.redirect_stdout(buf):
            H.main()
    finally:
        sys.stdin = stdin
    return json.loads(buf.getvalue() or "{}")


def transcript_with_goal(path, cond=DB_COND, met=None, failed=None,
                         extra=None):
    """Minimal session transcript: sentinel, optional verdict, optional tail."""
    recs = [{"type": "user", "message": {"role": "user",
             "content": "<command-name>/goal</command-name><command-args>%s</command-args>" % cond},
             "timestamp": "t0"}]
    recs.append({"type": "attachment", "timestamp": "t1",
                 "attachment": {"type": "goal_status", "met": False,
                                "sentinel": True, "condition": cond}})
    if met is not None or failed is not None:
        recs.append({"type": "attachment", "timestamp": "t2",
                     "attachment": {"type": "goal_status",
                                    "met": bool(met), "failed": bool(failed),
                                    "condition": cond,
                                    "reason": "three packages published; "
                                              "next: RNG contract"}})
    if extra:
        recs += extra
    w(path, "\n".join(json.dumps(r) for r in recs))


class GateParsing(unittest.TestCase):
    def test_verdict_rows(self):
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "important-subsystems.tsv"),
              "id\tcategory\nS-01\ta\nS-02\tb\n")
            w(os.path.join(t, "_index", "L2-VERDICTS.md"),
              "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
              "| **S-01** x | MET | MET | MET | MET | MET | **MET** | none |\n"
              "| **S-02** y | MET | PARTIAL | MET | **NOT MET** | MET | **NOT MET** | gap |\n")
            ok, rem, _ = G.check_verdicts(t, t)
            self.assertFalse(ok)
            self.assertIn("S-02", rem)

    def test_verdict_all_met(self):
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "important-subsystems.tsv"),
              "id\tcategory\nS-01\ta\n")
            w(os.path.join(t, "_index", "L2-VERDICTS.md"),
              "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
              "| **S-01** x | MET | MET | MET | MET | MET | **MET** | none |\n")
            ok, rem, _ = G.check_verdicts(t, t)
            self.assertTrue(ok)

    def test_verdict_unscored(self):
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "important-subsystems.tsv"), "id\nS-01\ta\nS-09\tb\n")
            w(os.path.join(t, "_index", "L2-VERDICTS.md"),
              "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
              "| **S-01** x | MET | MET | MET | MET | MET | **MET** | none |\n")
            ok, rem, _ = G.check_verdicts(t, t)
            self.assertFalse(ok)
            self.assertIn("S-09", rem)

    def test_verdict_decoy_table_rows_ignored(self):
        """An S-id row in a narrower table must not overwrite the verdict."""
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "important-subsystems.tsv"),
              "id\tcategory\nS-12\ta\n")
            w(os.path.join(t, "_index", "L2-VERDICTS.md"),
              "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
              "| **S-12** x | MET | PARTIAL | MET | **NOT MET** | MET | **NOT MET** | gap |\n"
              "| S-12 | MET**, subsystem |\n"  # 2-cell decoy after the real row
              "| S-12 | MET |\n")             # 1-cell decoy
            ok, rem, _ = G.check_verdicts(t, t)
            self.assertFalse(ok)
            self.assertIn("S-12", rem)

    def test_verdict_annotated_met_counts(self):
        """A leading MET token counts; the basis lives in the gap cell."""
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "important-subsystems.tsv"),
              "id\tcategory\nS-01\ta\n")
            w(os.path.join(t, "_index", "L2-VERDICTS.md"),
              "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
              "| **S-01** x | MET | MET | MET | MET | MET | **MET** - completed by X | none |\n")
            ok, rem, _ = G.check_verdicts(t, t)
            self.assertTrue(ok)

    def test_verdict_row_with_escaped_pipe_parses(self):
        """GFM escapes a literal pipe in a cell as \\|; the gate must not
        count it as a column separator (FABLE-CONTRA-GOAL-GATE-BITWISE-OR)."""
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "important-subsystems.tsv"),
              "id\tcategory\nS-48\ta\n")
            w(os.path.join(t, "_index", "L2-VERDICTS.md"),
              "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
              "| **S-48** x | MET | MET | MET | MET | MET | **MET** | gate `([+0x41]\\|[02B40524])&1` |\n")
            ok, rem, _ = G.check_verdicts(t, t)
            self.assertTrue(ok)

    def test_verdict_row_with_raw_pipe_fails_closed(self):
        """An UNescaped pipe widens the cell count; the row is dropped and
        the system reports unscored rather than silently accepted."""
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "important-subsystems.tsv"),
              "id\tcategory\nS-48\ta\n")
            w(os.path.join(t, "_index", "L2-VERDICTS.md"),
              "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
              "| **S-48** x | MET | MET | MET | MET | MET | **MET** | gate `a|b` |\n")
            ok, rem, _ = G.check_verdicts(t, t)
            self.assertFalse(ok)
            self.assertIn("S-48", rem)

    def test_contradictions_open_fails(self):
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "CONTRADICTIONS.tsv"),
              "id\tdate\tkind\nCON-1\td\tCORRECTED\nCON-2\td\tOPEN\n")
            ok, rem, _ = G.check_contradictions(t)
            self.assertFalse(ok)
            self.assertIn("CON-2", rem)

    def test_contradictions_resolved_pass(self):
        with tempfile.TemporaryDirectory() as t:
            w(os.path.join(t, "_index", "CONTRADICTIONS.tsv"),
              "id\tdate\tkind\nCON-1\td\tCORRECTED\nCON-2\td\tWITHDRAWN\n")
            ok, _, _ = G.check_contradictions(t)
            self.assertTrue(ok)


class AcceptanceReceipts(unittest.TestCase):
    def test_no_receipt_unmet(self):
        with tempfile.TemporaryDirectory() as t:
            f = FixtureRepo(t)
            w(os.path.join(f.db, "_index", "AUDIT-LOG.md"), "- ordinary entry\n")
            f.commit_all()
            ok, rem, _ = G.check_acceptance(t)
            self.assertFalse(ok)
            self.assertIn("no committed receipt", rem)

    def test_fresh_receipt_met(self):
        with tempfile.TemporaryDirectory() as t:
            f = FixtureRepo(t)
            w(os.path.join(f.db, "_index", "AUDIT-LOG.md"), "- seed\n")
            c1 = f.commit_all()
            w(os.path.join(f.db, "_index", "AUDIT-LOG.md"),
              "- seed\n- 2026-09-22 final audit: complete clean run of all thirty "
              "passes; program state %s\n" % c1)
            f.commit_all()
            ok, rem, _ = G.check_acceptance(t)
            self.assertTrue(ok, rem)

    def test_stale_receipt_unmet(self):
        with tempfile.TemporaryDirectory() as t:
            f = FixtureRepo(t)
            w(os.path.join(f.db, "page.md"), "v1\n")
            w(os.path.join(f.db, "_index", "AUDIT-LOG.md"), "- seed\n")
            c1 = f.commit_all()
            w(os.path.join(f.db, "_index", "AUDIT-LOG.md"),
              "- seed\n- final audit: complete run of all thirty passes; "
              "state %s\n" % c1)
            w(os.path.join(f.db, "page.md"), "v2 -- corpus moved after audit\n")
            f.commit_all()
            ok, rem, _ = G.check_acceptance(t)
            self.assertFalse(ok)
            self.assertIn("stale", rem)

    def test_uncommitted_receipt_unmet(self):
        """A certificate only in the working tree is not accepted evidence."""
        with tempfile.TemporaryDirectory() as t:
            f = FixtureRepo(t)
            w(os.path.join(f.db, "_index", "AUDIT-LOG.md"), "- seed\n")
            c1 = f.commit_all()
            w(os.path.join(f.db, "_index", "AUDIT-LOG.md"),
              "- seed\n- final audit: complete run of all thirty passes; "
              "state %s\n" % c1)  # never committed
            ok, rem, _ = G.check_acceptance(t)
            self.assertFalse(ok)


class TransferDestinations(unittest.TestCase):
    """FRONTIER-TODO-TRANSFER-DESTINATION-AUDIT: a transferred obligation must
    keep a completion-visible destination even when every verdict reads MET."""

    BATCH = ("## Class 1: SUPERSEDED onto the instrument (1)\n\n"
             "| row | population | instrument |\n|---|---|---|\n"
             "| ZZ-1 | 9 things | FixtureZone-99/zz-doc.md |\n\n"
             "## Class 2: NOT A QUESTION, with a carrier (1)\n\n"
             "| row | carrier |\n|---|---|\n"
             "| ZZ-2 | `FABLE-CARRIER-FIXTURE-1` |\n")

    def _mk(self, t, dest=True, carrier=True, verdict_met=True):
        db = os.path.join(t, "Database", "FFXII TZA")
        w(os.path.join(db, "_index", "candidates", "register-triage",
                       "batch-K-scope-rulings.md"), self.BATCH)
        if dest:
            w(os.path.join(db, "FixtureZone-99", "zz-doc.md"), "# dest\n")
        tasks = [{"id": "FABLE-CARRIER-FIXTURE-1", "status": "READY",
                  "assigned_to": "FABLE"}] if carrier else []
        w(os.path.join(db, "_index", "_inbox", "TEAM.json"),
          json.dumps({"tasks": tasks}))
        w(os.path.join(db, "_index", "important-subsystems.tsv"),
          "id\tcategory\nS-01\ta\n")
        w(os.path.join(db, "_index", "L2-VERDICTS.md"),
          "| system | contract | types | relationships | runtime | script/data | **L2** | binding gap |\n"
          "| **S-01** x | MET | MET | MET | MET | MET | **MET** | none |\n")
        return db

    def test_all_destinations_live(self):
        with tempfile.TemporaryDirectory() as t:
            db = self._mk(t)
            ok, rem, _ = G.check_transfers(db)
            self.assertTrue(ok, rem)

    def test_all_met_but_dead_destination_fails(self):
        """The mandated case: every verdict MET, one required unread item's
        destination gone - the goal must still fail."""
        with tempfile.TemporaryDirectory() as t:
            db = self._mk(t, dest=False)
            ok_v, rem_v, _ = G.check_verdicts(db, t)
            self.assertTrue(ok_v, rem_v)  # L2 verdicts are MET
            ok, rem, _ = G.check_transfers(db)
            self.assertFalse(ok)
            self.assertIn("ZZ-1", rem)

    def test_missing_carrier_task_fails(self):
        with tempfile.TemporaryDirectory() as t:
            db = self._mk(t, carrier=False)
            ok, rem, _ = G.check_transfers(db)
            self.assertFalse(ok)
            self.assertIn("FABLE-CARRIER-FIXTURE-1", rem)

    def test_ownerless_carrier_fails(self):
        with tempfile.TemporaryDirectory() as t:
            db = self._mk(t)
            w(os.path.join(db, "_index", "_inbox", "TEAM.json"),
              json.dumps({"tasks": [{"id": "FABLE-CARRIER-FIXTURE-1",
                                     "status": "READY"}]}))
            ok, rem, _ = G.check_transfers(db)
            self.assertFalse(ok)
            self.assertIn("no owner", rem)


class HookBehaviour(unittest.TestCase):
    def setUp(self):
        self._sd, H.STATE_DIR = H.STATE_DIR, tempfile.mkdtemp()
        H.STATE_PATH = os.path.join(H.STATE_DIR, "hook-state.json")

    def tearDown(self):
        H.STATE_DIR = self._sd
        H.STATE_PATH = os.path.join(H.STATE_DIR, "hook-state.json")

    def test_observed_false_completion_blocked(self):
        """'three packages; next RNG contract' stays NOT_MET while the gate is."""
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp, met=True)  # reason names next work -> still block
            out = run_hook(hook_in(tp))
            self.assertEqual(out.get("decision"), "block")
            self.assertIn("DB_GOAL=NOT_MET", out["reason"])
            self.assertIn("remaining=", out["reason"])

    def test_uq289_pattern_blocked(self):
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp, met=True,
                                 extra=[{"type": "assistant", "message": {"content":
                                     "UQ-289 reframed; next nine context-switch variants"}}])
            out = run_hook(hook_in(tp))
            self.assertEqual(out.get("decision"), "block")

    def test_active_goal_blocked(self):
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp)  # sentinel only -> active
            out = run_hook(hook_in(tp))
            self.assertEqual(out.get("decision"), "block")

    def test_other_goal_passes(self):
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp, cond=OTHER_COND, met=True)
            self.assertEqual(run_hook(hook_in(tp)), {})

    def test_failed_goal_honoured(self):
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp, failed=True)
            self.assertEqual(run_hook(hook_in(tp)), {})

    def test_no_goal_passes(self):
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            w(tp, json.dumps({"type": "user", "message": {"content": "hi"}}))
            self.assertEqual(run_hook(hook_in(tp)), {})

    def test_met_gate_allows_stop(self):
        """A valid terminal acceptance passes: when the gate agrees, no veto."""
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp, met=True)
            old = H._run_gate
            H._run_gate = lambda: ({"verdict": "MET"}, None)
            try:
                self.assertEqual(run_hook(hook_in(tp)), {})
            finally:
                H._run_gate = old

    def test_gate_error_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp)
            old = H._run_gate
            H._run_gate = lambda: (None, "fixture gate error")
            try:
                out = run_hook(hook_in(tp))
            finally:
                H._run_gate = old
            self.assertEqual(out.get("decision"), "block")
            self.assertIn("fixture gate error", out["reason"])

    def test_no_progress_pauses_instead_of_storming(self):
        # 2026-09-27 (dd260f6e8): an unchanged tool signature over repeated
        # stops is a bounded pause, not an identical veto. The first flat
        # block still vetoes (and says so); the session then records 'paused'
        # and the hook emits {} - no continuation feedback, verdict intact.
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp, met=True)
            out1 = run_hook(hook_in(tp))
            self.assertEqual(out1.get("decision"), "block")
            run_hook(hook_in(tp))
            out3 = run_hook(hook_in(tp))
            self.assertEqual(out3, {})
            st = json.load(open(H.STATE_PATH))
            self.assertIn("paused", st["fixture-1"])


class ResumeClassification(unittest.TestCase):
    def setUp(self):
        self._ls = R.live_sessions
        R.live_sessions = lambda: set()  # fixture sessions are never live

    def tearDown(self):
        R.live_sessions = self._ls

    def _classify(self, **kw):
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "s.jsonl")
            transcript_with_goal(tp, **kw)
            return R.classify(R.tail_records(tp))

    def test_false_completion_offers_exact_goal(self):
        state, cond, _ = self._classify(met=True)
        self.assertEqual(state, "FALSE_COMPLETION")
        self.assertEqual(cond, DB_COND)

    def test_compaction_resume_keeps_goal(self):
        extra = [{"type": "system", "subtype": "compact",
                  "compact": {"trigger": "auto"}},
                 {"type": "attachment",
                  "attachment": {"type": "goal_status", "met": False,
                                 "sentinel": True, "condition": DB_COND}}]
        state, cond, _ = self._classify(extra=extra)
        self.assertEqual(state, "ORDINARY_STOP")
        self.assertEqual(cond, DB_COND)

    def test_user_cancel_honoured(self):
        extra = [{"type": "user", "message": {"role": "user", "content":
                  "<command-name>/goal</command-name><command-args>clear</command-args>"}}]
        state, _, _ = self._classify(extra=extra)
        self.assertEqual(state, "USER_STOP")

    def test_hard_limit_honoured(self):
        extra = [{"type": "rate_limit_event",
                  "rate_limit_info": {"status": "rate_limited",
                                      "resetsAt": 1}}]
        state, _, _ = self._classify(extra=extra)
        self.assertEqual(state, "USAGE_LIMIT")

    def test_impossible_honoured(self):
        state, _, _ = self._classify(failed=True)
        self.assertEqual(state, "IMPOSSIBLE")


if __name__ == "__main__":
    unittest.main()
