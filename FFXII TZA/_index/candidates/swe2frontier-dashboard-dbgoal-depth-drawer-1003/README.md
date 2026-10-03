# Dashboard step A: DB_GOAL blocking chain, Depth labelled a diagnostic, Source/Freshness drawer (SWE2-FRONTIER, 2026-10-03)

*From the user's context-refresh package v3 (08_DASHBOARD_REQUIRED_UPDATE.md sections 6 and 7) and improvement addendum section 1. SWE2-FRONTIER, Claude stand-in for the Devin session `calm-lamp`; one of six separately published dashboard steps (A-F), through the existing M3 adapters and generation store. Test: `Database/Tools/dashboard/test_dashboard_base.py`.*

- DB_GOAL blocking chain (`db_goal_block`): goal_gate.py's own verdict / remaining / next / detail, verbatim; the glance page shows `remaining`.
- Depth: title, OVERALL label, glance tile and tab say it is a weighted diagnostic, not DB_GOAL; the view carries a `diagnostic` block.
- Source/Freshness drawer (`provenance_block` + page): generation id, committed at, source commit, board revision/epoch, progress fingerprint, knowledge.sqlite check (new volatile input `knowledge_check`), goal-gate identity, stale sources.

Checks (staged, cumulative from HEAD): after each step its own test and every earlier step's test FAIL 0, and every adapter passes `server.check_view` with the live vocabulary over a copy of the live capture (with the real `recent_changes.py` and `check_status_residue.py` outputs); the glance page script parses and renders the real view in node.
