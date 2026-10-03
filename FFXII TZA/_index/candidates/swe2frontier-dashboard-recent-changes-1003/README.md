# Dashboard step B: Recent meaningful changes - knowledge versus activity from recent_changes.py (SWE2-FRONTIER, 2026-10-03)

*From improvement addendum section 2; DASHBOARD-MEANINGS 6.3. SWE2-FRONTIER, Claude stand-in for the Devin session `calm-lamp`; one of six separately published dashboard steps (A-F), through the existing M3 adapters and generation store. Test: `Database/Tools/dashboard/test_recent_changes.py`.*

- Renders FABLE's `recent_changes.py --json` (a065b24fa), captured every build as a volatile input, under the contract agreed with FABLE.
- Knowledge, activity and unclassified are separate counts per window (24h, 7d) and are never summed; knowledge events are listed with their canonical evidence.
- The adapter never classifies; an unknown class string is named (PARTIAL); absent output is UNMEASURED. On live data at build time, 24h: 376 knowledge / 412 activity / 79 unclassified.
- recent_changes.py takes about 133 s per build (within the 900 s instrument limit).

Checks (staged, cumulative from HEAD): after each step its own test and every earlier step's test FAIL 0, and every adapter passes `server.check_view` with the live vocabulary over a copy of the live capture (with the real `recent_changes.py` and `check_status_residue.py` outputs); the glance page script parses and renders the real view in node.
