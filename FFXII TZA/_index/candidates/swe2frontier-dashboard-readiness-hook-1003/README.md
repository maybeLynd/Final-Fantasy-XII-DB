# Dashboard step G: system readiness view on the systems view (SWE2-FRONTIER, 2026-10-03)

*Wires SWE2-STRUCT's `readiness_view.py` (HOOK.md in `_index/candidates/swe2struct-design-readiness-views-1003/`;
SWE2STRUCT-REQ-FRONTIER-READINESS-VIEW-HOOK-1003) into the systems view. SWE2-FRONTIER, Claude stand-in for the Devin
session `calm-lamp`. Test: `Database/Tools/dashboard/test_readiness_hook.py`.*

- The build captures `readiness_view.py --out` each run (about 3 s) as the optional input `readiness`. Each registered
  system's counts gain:
  - the previously UNMEASURED "open obligations under this system", from `register_live` / `register_closed`;
  - `maturity` (SPECIFICATION READY or no label, with the withholding conditions), capped at SPECIFICATION READY:
    a later label reads WITHHELD;
  - `parity probes (PROBE, database phase)`;
  - the other columns.
  No sum and no percentage.
- Maturity is shown in counts, not as the node `state`. `server.load_vocabulary` reads node states from DASHBOARD-MEANINGS
  sections 1-2 only. Showing SPECIFICATION READY as a state would need the 6.4 labels added to that loader (routed to
  FABLE / the dashboard owner).
- Limit: the capture reads the live TEAM.json at capture time, not the generation's `team` snapshot (HOOK.md asks for
  the snapshot). Capture runs before `Build.begin()`, so byte-binding would need a build-order change. `board_open` is
  coordination load only.

Checks (staged on top of the committed steps): every dashboard step test FAILS 0 including `test_readiness_hook.py`, and
every adapter passes `server.check_view` with the live vocabulary over the real capture.
