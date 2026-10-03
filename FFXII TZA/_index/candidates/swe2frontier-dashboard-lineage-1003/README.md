# Dashboard step D: evidence lineage drilldown on the systems view (SWE2-FRONTIER, 2026-10-03)

*From improvement addendum section 6. SWE2-FRONTIER, Claude stand-in for the Devin session `calm-lamp`; one of six separately published dashboard steps (A-F), through the existing M3 adapters and generation store. Test: `Database/Tools/dashboard/test_lineage.py`.*

- Each registered system node carries the nine-step lineage (system, claim, contract, static/native, original-code, live, review, consumers, probe/parity), each present / not required / not measured / unknown / not yet available with a reason; the node links its contract and the L2 verdicts.

Checks (staged, cumulative from HEAD): after each step its own test and every earlier step's test FAIL 0, and every adapter passes `server.check_view` with the live vocabulary over a copy of the live capture (with the real `recent_changes.py` and `check_status_residue.py` outputs); the glance page script parses and renders the real view in node.
