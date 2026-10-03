# Dashboard step C: Next highest-value work - the gate chain plus board ownership (SWE2-FRONTIER, 2026-10-03)

*From improvement addendum section 11. SWE2-FRONTIER, Claude stand-in for the Devin session `calm-lamp`; one of six separately published dashboard steps (A-F), through the existing M3 adapters and generation store. Test: `Database/Tools/dashboard/test_next_work.py`.*

- `next_work_block`: goal_gate's remaining/next plus board tasks in the addendum's seven buckets by board fields only; a task naming an open register row blocks DB_GOAL now.
- Open register rows that no task names are listed as unowned. No score, no age term, no second scheduler.

Checks (staged, cumulative from HEAD): after each step its own test and every earlier step's test FAIL 0, and every adapter passes `server.check_view` with the live vocabulary over a copy of the live capture (with the real `recent_changes.py` and `check_status_residue.py` outputs); the glance page script parses and renders the real view in node.
