"""Fixtures for goal_gate_hook.py -- the 2026-09-27 OPUS veto-storm incident.

Session 7af7f6f5 exhausted context (after 15 successful auto-compactions),
checkpointed honestly, and tried to stop; the Stop hook vetoed 306 times --
the last 8 with zero tool-record growth -- until the host's block cap paused
the session. These fixtures pin the repair: an already-triggered continuation
that produced no tool work must be allowed a bounded pause, never vetoed
again with an identical reason.

The real gate is stubbed: the hook calls GATE as a subprocess, so a fixture
script emitting a canned verdict keeps tests fast and deterministic. The
state file is likewise redirected into a temp dir.
"""
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import goal_gate_hook as hook

FIXTURE_HOOK = (Path(r"C:/Users/Kristian/source/repos/goalgate-fixture")
                / "stop_hook.py")

DB_CONDITION = ("GOAL: Complete the FF12 knowledge database to the existing "
                "accepted L1+L2 reconstruction-grade standard.")


def _goal_line(met=False, failed=False, condition=DB_CONDITION):
    return json.dumps({"timestamp": "2026-09-27T00:00:00Z",
                       "attachment": {"type": "goal_status", "met": met,
                                      "failed": failed,
                                      "condition": condition}})


def _tool_line():
    return json.dumps({"type": "tool_use", "name": "read"})


def _prose_line(text="assistant restates status"):
    return json.dumps({"type": "assistant",
                       "message": {"content": [{"type": "text",
                                                "text": text}]}})


GATE_STUB = """import json, os, sys
verdict = os.environ.get("STUB_VERDICT", "NOT_MET")
if verdict == "ERROR":
    sys.stderr.write("stub gate blew up")
    sys.exit(3)
print(json.dumps({"verdict": verdict,
                  "remaining": "OPEN=37", "next": "resolve register rows"}))
"""


class HookFixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.transcript = self.dir / "t.jsonl"
        self.stub = self.dir / "gate_stub.py"
        self.stub.write_text(GATE_STUB, encoding="utf-8")
        self._env = mock.patch.dict(os.environ, {"STUB_VERDICT": "NOT_MET"})
        self._env.start()
        self._patches = [
            mock.patch.object(hook, "GATE", str(self.stub)),
            mock.patch.object(hook, "STATE_PATH", str(self.dir / "hs.json")),
            mock.patch.object(hook, "STATE_DIR", str(self.dir)),
        ]
        for p in self._patches:
            p.start()
        self.write_transcript(goal=True, tools=5)

    def tearDown(self):
        for p in self._patches:
            p.stop()
        self._env.stop()
        self._tmp.cleanup()

    def write_transcript(self, goal=True, tools=0, prose=0,
                         met=False, failed=False,
                         condition=DB_CONDITION):
        lines = []
        if goal:
            lines.append(_goal_line(met=met, failed=failed,
                                    condition=condition))
        lines += [_tool_line() for _ in range(tools)]
        lines += [_prose_line() for _ in range(prose)]
        self.transcript.write_text("\n".join(lines) + "\n",
                                   encoding="utf-8")

    def run_hook(self, session="sess-1", stop_active=False, event="Stop",
                 last_msg=""):
        inp = {"hook_event_name": event, "session_id": session,
               "transcript_path": str(self.transcript),
               "stop_hook_active": stop_active,
               "last_assistant_message": last_msg,
               "cwd": str(self.dir)}
        buf = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO(json.dumps(inp))):
            with mock.patch("sys.stdout", buf):
                hook.main()
        out = buf.getvalue()
        return json.loads(out) if out.strip() else {}

    def state(self, session="sess-1"):
        try:
            return json.loads(Path(hook.STATE_PATH)
                              .read_text(encoding="utf-8"))[session]
        except Exception:
            return {}

    # ---- gating basics ---------------------------------------------------

    def test_non_stop_event_passes(self):
        self.assertEqual(self.run_hook(event="PostToolUse"), {})

    def test_no_goal_passes(self):
        self.write_transcript(goal=False, tools=3)
        self.assertEqual(self.run_hook(), {})

    def test_non_db_goal_passes(self):
        self.write_transcript(condition="GOAL: polish the hud colours")
        self.assertEqual(self.run_hook(), {})

    def test_failed_goal_passes(self):
        self.write_transcript(failed=True)
        self.assertEqual(self.run_hook(), {})

    def test_met_verdict_allows_and_records(self):
        os.environ["STUB_VERDICT"] = "MET"
        self.assertEqual(self.run_hook(), {})
        self.assertEqual(self.state()["last_verdict"], "MET")
        self.assertNotIn("paused", self.state())

    # ---- the storm --------------------------------------------------------

    def test_first_stop_blocks_with_gate_reason(self):
        out = self.run_hook()
        self.assertEqual(out.get("decision"), "block")
        self.assertIn("OPEN=37", out.get("reason", ""))

    def test_repeat_stop_without_progress_allows_pause(self):
        """The incident shape: block once, then an already-triggered
        continuation with an unchanged tool sig must be ALLOWED - and must
        carry no continuation feedback."""
        self.assertEqual(self.run_hook(stop_active=False).get("decision"),
                         "block")
        out = self.run_hook(stop_active=True)   # unchanged transcript
        self.assertEqual(out, {})               # allow, no feedback
        st = self.state()
        self.assertEqual(st["paused"]["reason"], "no-progress")
        self.assertEqual(st["paused"]["verdict"], "NOT_MET")

    def test_pause_without_stop_hook_active_after_two_flat_blocks(self):
        """Hosts that never set stop_hook_active still bound the storm."""
        self.assertEqual(self.run_hook().get("decision"), "block")
        self.assertEqual(self.run_hook().get("decision"), "block")
        self.assertEqual(self.run_hook(), {})

    def test_progress_resets_and_keeps_blocking(self):
        """Real work between stop attempts resets the no-progress counter."""
        self.assertEqual(self.run_hook().get("decision"), "block")
        self.assertEqual(self.run_hook(stop_active=True), {})   # pause window
        # a later attempt after tool growth blocks again
        self.write_transcript(tools=9)
        self.assertEqual(self.run_hook(stop_active=True).get("decision"),
                         "block")

    def test_unverified_context_claim_alone_never_pauses(self):
        """A prose claim of exhaustion is not progress state: the session
        kept calling tools, so the sig moved and the gate still vetoes."""
        self.run_hook()                                  # block, sig=5
        self.write_transcript(tools=8)                   # real work landed
        out = self.run_hook(stop_active=True,
                            last_msg="I am out of context")
        self.assertEqual(out.get("decision"), "block")

    # ---- failure shapes ---------------------------------------------------

    def test_gate_error_blocks_then_pauses_on_no_progress(self):
        os.environ["STUB_VERDICT"] = "ERROR"
        out = self.run_hook()
        self.assertEqual(out.get("decision"), "block")
        self.assertIn("goal_gate.py", out.get("reason", ""))
        out = self.run_hook(stop_active=True)
        self.assertEqual(out, {})
        self.assertTrue(self.state()["paused"]["gate_error"])

    def test_corrupt_state_file_tolerated(self):
        Path(hook.STATE_PATH).write_text("{not json", encoding="utf-8")
        self.assertEqual(self.run_hook().get("decision"), "block")

    def test_duplicate_wakeup_idempotent(self):
        """Two Stop deliveries of the same attempt: the second sees the
        first's counters; the storm rule still bounds it."""
        self.assertEqual(self.run_hook().get("decision"), "block")
        self.assertEqual(self.run_hook(stop_active=True), {})
        # third duplicate delivery stays allowed - no re-block
        self.assertEqual(self.run_hook(stop_active=True), {})

    # ---- both hooks together ----------------------------------------------

    @unittest.skipUnless(FIXTURE_HOOK.exists(), "fixture hook not installed")
    def test_other_hook_does_not_restart_the_loop(self):
        """With the goal hook allowing after no-progress, the probe fixture's
        Stop hook (block-once) emits {} on the same continuation - nothing
        re-blocks, so the session actually exits."""
        import subprocess
        inp = {"hook_event_name": "Stop", "session_id": "sess-1",
               "transcript_path": str(self.transcript),
               "stop_hook_active": True}
        self.run_hook()                       # goal hook blocks once
        self.assertEqual(self.run_hook(stop_active=True), {})
        r = subprocess.run([sys.executable, str(FIXTURE_HOOK)],
                           input=json.dumps(inp), capture_output=True,
                           text=True, timeout=30)
        self.assertEqual(json.loads(r.stdout), {})


if __name__ == "__main__":
    unittest.main()
