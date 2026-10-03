# Dashboard step F: lifecycle panel - the phase read from PROJECT-LIFECYCLE.json (SWE2-FRONTIER, 2026-10-03)

*From FABLE-REQ-FRONTIER-DASHBOARD-LIFECYCLE-1003; DASHBOARD-MEANINGS section 6. SWE2-FRONTIER, Claude stand-in for the Devin session `calm-lamp`; one of six separately published dashboard steps (A-F), through the existing M3 adapters and generation store. Test: `Database/Tools/dashboard/test_lifecycle.py`.*

- `lifecycle_block`: the phase is PROJECT-LIFECYCLE.json's current_primary_phase, read only, never advanced; the gate verdict and readiness are shown beside it; a file declaring a later phase than DB_GOAL supports shows both and a DISAGREEMENT, never the later phase as current; probes labelled PROBE (database phase); original game = oracle, never the production backend.
- PROJECT-LIFECYCLE.json is a strict generation input (a change makes the generation STALE); absent/malformed/unknown phase -> FAILED panel.
- test_lifecycle.py L1-L9; L9 checks the dashboard labels against DASHBOARD-MEANINGS section 6 (FABLE's consumer-pair table).

Checks (staged, cumulative from HEAD): after each step its own test and every earlier step's test FAIL 0, and every adapter passes `server.check_view` with the live vocabulary over a copy of the live capture (with the real `recent_changes.py` and `check_status_residue.py` outputs); the glance page script parses and renders the real view in node.
