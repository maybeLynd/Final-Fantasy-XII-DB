# Dashboard step E: Production system status residue view from check_status_residue.py (SWE2-FRONTIER, 2026-10-03)

*From the user's FFXII_INDEPENDENT_CORPUS_AUDIT_FOLLOWUP_2026-10-03 section 9. SWE2-FRONTIER, Claude stand-in for the Devin session `calm-lamp`; one of six separately published dashboard steps (A-F), through the existing M3 adapters and generation store. Test: `Database/Tools/dashboard/test_status_residue.py`.*

- New view `residue` (tab 'Status residue') from FABLE's `check_status_residue.py --json`, captured every build: system pages by status word, then the PARTIAL/REOPENED pages split into live register row / process-only / no mapped obligation, UNMAPPED first. No score.

Checks (staged, cumulative from HEAD): after each step its own test and every earlier step's test FAIL 0, and every adapter passes `server.check_view` with the live vocabulary over a copy of the live capture (with the real `recent_changes.py` and `check_status_residue.py` outputs); the glance page script parses and renders the real view in node.
