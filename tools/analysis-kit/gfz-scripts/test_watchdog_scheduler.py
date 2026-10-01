"""test_watchdog_scheduler.py - isolated fixtures for the dependency-aware
controller (2026-09-29 incident: OPUS paused on other lanes' work while the
fleet kept waking the wrong lanes and nobody replaced a dead scheduler).

S1  dep_blocked_owners maps a BLOCKED task to the owners of its unfinished
    deps, across lanes; DONE deps and missing ids contribute nothing.
S2  desired_set promotes dep owners ahead of a manually pinned plan; the
    paused owner itself produces no need and is never a candidate.
S3  non-specialist dep owners (OPUS/FABLE/ASTRA) are reported but never
    become a desired wake target.
S4  ensure_decision: no controller -> start; one fresh -> healthy; one stale
    -> restart; two live -> refuse-duplicate; scan failure -> refuse-unknown.
S5  a lane whose only work is BLOCKED emits no need entry (never re-woken
    while its deps stay unchanged) - board_need on a fixture board.
S6  transitions.plan: dep completion emits exactly one AUTO-UNBLOCK nudge to
    the blocked owner; a second plan() run finds it already filed.
S7  eligible(): a lane whose sessions are all NEVER_WAKE is refused; a lane
    at the daily cap is refused with 'daily-cap' and the next candidate
    still wins the slot.
"""
import json
import os
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import swe2_watchdog as W  # noqa: E402
import transitions as TR  # noqa: E402


def _task(tid, status="READY", prio="P2", **kw):
    t = {"id": tid, "kind": kw.pop("kind", "request"), "priority": prio,
         "status": status, "dependencies": kw.pop("dependencies", []),
         "resources": kw.pop("resources", [{"key": "request:" + tid.lower()}]),
         "requester": kw.pop("requester", "SWE2-FRONTIER"),
         "agent": kw.pop("agent", None), "assigned_to": kw.pop("assigned_to", None)}
    t.update(kw)
    return t


_AGENTS = ["SWE2-FRONTIER", "SWE2-EC7", "SWE2-CONTRACT", "SWE2-STRUCT",
           "SWE2-DATA", "SWE2-ORACLE", "SWE2-AUDIT-SEM", "SWE2-AUDIT-SPEC",
           "OPUS", "FABLE", "ASTRA"]


def _board(tasks):
    return {"tasks": tasks, "agents": {a: {
                "agent_id": a, "primary_specialty": "test",
                "current_task": [], "claimed_scope": [], "dependencies": [],
                "blockers": [], "last_checkpoint": "2026-09-29T00:00:00+00:00",
                "status": "READY"} for a in _AGENTS},
            "history": [], "journal": [], "revision": 1, "epoch": 0,
            "schema_version": 1, "phase": "DATABASE"}


class DepOwners(unittest.TestCase):
    def test_blocked_maps_to_dep_owners(self):
        board = _board([
            _task("PKG-HELD", "BLOCKED", "P1", agent="OPUS",
                  dependencies=["DEP-SEM", "DEP-DATA", "DEP-ASTRA", "DEP-DONE"]),
            _task("DEP-SEM", "READY", "P1", assigned_to="SWE2-AUDIT-SEM"),
            _task("DEP-DATA", "READY", "P2", assigned_to="SWE2-DATA"),
            _task("DEP-ASTRA", "READY", "P1", assigned_to="ASTRA"),
            _task("DEP-DONE", "DONE", "P2", assigned_to="SWE2-STRUCT",
                  result_refs=["x"]),
        ])
        dep = W.dep_blocked_owners(board)
        self.assertEqual(dep.get("SWE2-AUDIT-SEM"), {"DEP-SEM"})
        self.assertEqual(dep.get("SWE2-DATA"), {"DEP-DATA"})
        self.assertEqual(dep.get("ASTRA"), {"DEP-ASTRA"})
        self.assertNotIn("SWE2-STRUCT", dep)   # its dep is DONE

    def test_unblocked_board_maps_nothing(self):
        board = _board([_task("T1", "READY", "P2", assigned_to="SWE2-DATA")])
        self.assertEqual(W.dep_blocked_owners(board), {})


class DesiredPromotion(unittest.TestCase):
    def test_dep_owners_beat_pinned_plan(self):
        # A: OPUS paused, deps READY on AUDIT-SEM + DATA; plan had pinned EC7.
        dep = {"SWE2-AUDIT-SEM": {"DEP-SEM"}, "SWE2-DATA": {"DEP-DATA"},
               "ASTRA": {"DEP-ASTRA"}}
        plan = {"desired": ["SWE2-EC7"], "target_active": 3}
        need = {"SWE2-EC7": (2, "P3", "ready-pool:P3:4"),
                "SWE2-AUDIT-SEM": (1, "P1", "ready-targeted:P1:DEP-SEM"),
                "SWE2-DATA": (0, "P2", "active-claim:DEP-DATA")}
        desired, target, source = W.desired_set(plan, need, dep)
        self.assertEqual(desired[0], "SWE2-AUDIT-SEM")
        self.assertEqual(desired[1], "SWE2-DATA")
        self.assertIn("SWE2-EC7", desired)
        self.assertNotIn("ASTRA", desired)          # S3: never a wake target
        self.assertEqual(target, 3)
        self.assertEqual(source, "plan+deps")

    def test_paused_owner_has_no_need(self):
        # C: the blocked side contributes nothing - only dep owners surface.
        dep = {"SWE2-DATA": {"DEP-DATA"}}
        plan = {"desired": ["SWE2-EC7", "SWE2-STRUCT"], "target_active": 3}
        need = {"SWE2-EC7": (2, "P3", "ready-pool"),
                "SWE2-DATA": (0, "P1", "active-claim:DEP-DATA")}
        desired, _, _ = W.desired_set(plan, need, dep)
        self.assertEqual(desired[0], "SWE2-DATA")
        self.assertNotIn("SWE2-FRONTIER", desired)


class EnsureDecision(unittest.TestCase):
    def test_absent_starts(self):
        self.assertEqual(W.ensure_decision([], 30), "start")

    def test_healthy_untouched(self):
        self.assertEqual(W.ensure_decision([1234], 60), "healthy")

    def test_stale_restarts(self):
        self.assertEqual(W.ensure_decision([1234], 99999), "restart")
        self.assertEqual(W.ensure_decision([1234], None), "restart")

    def test_duplicate_fails_closed(self):
        self.assertEqual(W.ensure_decision([1234, 5678], 10),
                         "refuse-duplicate")

    def test_scan_failure_fails_closed(self):
        self.assertEqual(W.ensure_decision(None, 10), "refuse-unknown")


class NeedFromFixtureBoard(unittest.TestCase):
    """C on the real board_need path: a lane holding only a BLOCKED task
    contributes no need, so nothing re-wakes it while deps are unchanged."""

    def _with_board(self, board, fn):
        fd, path = tempfile.mkstemp(suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(board, f)
            old = W.BOARD_FILE
            W.BOARD_FILE = path
            try:
                return fn()
            finally:
                W.BOARD_FILE = old
        finally:
            os.remove(path)

    def test_blocked_only_lane_has_no_need(self):
        board = _board([
            _task("PKG-HELD", "BLOCKED", "P1", agent="SWE2-STRUCT",
                  dependencies=["DEP-SEM"]),
            _task("DEP-SEM", "READY", "P1", assigned_to="SWE2-AUDIT-SEM"),
        ])
        need = self._with_board(board, W.board_need)
        self.assertNotIn("SWE2-STRUCT", need)
        self.assertIn("SWE2-AUDIT-SEM", need)


class UnblockTransition(unittest.TestCase):
    def test_dep_done_nudges_owner_once(self):
        # D: dep completes -> one AUTO-UNBLOCK to the owner, then DONE-ALREADY.
        board = _board([
            _task("PKG-HELD", "BLOCKED", "P1", agent="SWE2-STRUCT",
                  dependencies=["DEP-SEM"]),
            _task("DEP-SEM", "DONE", "P1", assigned_to="SWE2-AUDIT-SEM",
                  result_refs=["x"]),
        ])
        first = TR.plan(board)
        unblocks = [x for x in first if x[0] == "UNBLOCK"]
        self.assertEqual(len(unblocks), 1)
        self.assertEqual(unblocks[0][2], "AUTO-UNBLOCK-PKG-HELD")
        self.assertEqual(unblocks[0][3]["task"]["assigned_to"], "SWE2-STRUCT")
        board["tasks"].append(_task("AUTO-UNBLOCK-PKG-HELD", "READY", "P1",
                                    assigned_to="SWE2-STRUCT"))
        second = TR.plan(board)
        self.assertEqual([x for x in second if x[1] == "PKG-HELD"],
                         [("DONE-ALREADY", "PKG-HELD",
                           "AUTO-UNBLOCK-PKG-HELD", None)])

    def test_dep_unchanged_no_nudge(self):
        # C's other half: deps still open -> nothing is filed at all.
        board = _board([
            _task("PKG-HELD", "BLOCKED", "P1", agent="SWE2-STRUCT",
                  dependencies=["DEP-SEM"]),
            _task("DEP-SEM", "READY", "P1", assigned_to="SWE2-AUDIT-SEM"),
        ])
        self.assertFalse([x for x in TR.plan(board) if x[0] == "UNBLOCK"])


class EligibilityGates(unittest.TestCase):
    def _state(self):
        return {"inflight": {}, "wakes": {}, "failures": {},
                "parked_ineffective": {}, "breaker": {},
                "starvation": {}, "replan": {"events": []}}

    def _fleet_map(self, lane, canonical, current=None):
        return {"identities": {lane: {"canonical": canonical,
                                      "current": current}}}

    def test_never_wake_session_refused(self):
        # E: a lane whose only session is on the never-wake list (the fleet's
        # user-stop equivalent) is never a candidate.
        st = self._state()
        fm = self._fleet_map("SWE2-EC7", "tree-coaster", "tree-coaster")
        ok, reason = W.eligible(st, fm, {"tree-coaster"}, "SWE2-EC7",
                                time.time(), "2026-09-29")
        self.assertFalse(ok)
        self.assertEqual(reason, "no-session")

    def test_daily_cap_refused_next_lane_still_wins(self):
        # F: capped reviewer is skipped, not bypassed; another candidate is
        # chosen from the same desired set. lock_held is host state - a live
        # fleet session holding the fixture's id would read "session-held"
        # before the cap is ever reached - so it is pinned closed here.
        st = self._state()
        today = "2026-09-29"
        st["wakes"]["SWE2-AUDIT-SEM"] = {today: {"count": W.MAX_WAKES_PER_DAY,
                                                "last": 0}}
        fm = {"identities": {
            "SWE2-AUDIT-SEM": {"canonical": "legend-pipe",
                               "current": "legend-pipe"},
            "SWE2-DATA": {"canonical": "holy-rock", "current": "holy-rock"}}}
        sessions = {"legend-pipe", "holy-rock"}
        now = time.time()
        old = W.lock_held
        W.lock_held = lambda _sid: False
        try:
            ok, reason = W.eligible(st, fm, sessions, "SWE2-AUDIT-SEM", now, today)
            self.assertFalse(ok)
            self.assertEqual(reason, "daily-cap")
            st["wakes"]["SWE2-DATA"] = {today: {"count": 0, "last": 0}}
            ok2, reason2 = W.eligible(st, fm, sessions, "SWE2-DATA", now, today)
            self.assertTrue(ok2, reason2)
        finally:
            W.lock_held = old


class ApplyBudget(unittest.TestCase):
    """SWE2-FRONTIER-DEFECT-TRANSITIONS-APPLY-120S: a spent --apply-budget-s
    must defer remaining ops (next cycle picks them up), never write past the
    caller's wall-clock cap."""

    def _review(self, tid):
        # a board-validated DONE review: apply() validates every row, so the
        # fixture needs the full field set a real task carries
        return _task(tid, "DONE", "P2", agent="SWE2-AUDIT-SEM",
                     assigned_to="SWE2-AUDIT-SEM",
                     target="fixture review", scope="fixture",
                     completion="done", checkpoint="landed",
                     updated_at="2026-09-29T00:00:00+00:00",
                     started_at="2026-09-29T00:00:00+00:00",
                     question="q", known_evidence="e", missing_information="m",
                     why_it_matters="w", what_is_blocked="n",
                     reviews={"author": "OPUS", "commit": "abc123"},
                     result_refs=["verdict:REJECT", "commit:abc123"])

    def _apply_board(self, board, *extra):
        fd, path = tempfile.mkstemp(suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(board, f)
            rc = TR.main(["--board", path, "--apply", "--json",
                          "--apply-budget-s"] + list(extra))
            return rc, json.load(open(path, encoding="utf-8"))
        finally:
            os.remove(path)

    def test_zero_budget_defers_without_writing(self):
        board = _board([self._review("REV-1")])
        # A microsecond budget is always spent before the first op, so every
        # op defers and the board is untouched (budget 0 means unbounded).
        rc, after = self._apply_board(board, "0.000001")
        self.assertEqual(rc, 0)
        self.assertEqual({t["id"] for t in after["tasks"]}, {"REV-1"})

    def test_budget_allows_writes(self):
        board = _board([self._review("REV-1")])
        rc, after = self._apply_board(board, "600")
        self.assertEqual(rc, 0)
        self.assertIn("AUTO-REPAIR-REV-1", {t["id"] for t in after["tasks"]})


if __name__ == "__main__":
    unittest.main()
