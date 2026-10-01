# Affected-consumer check: the grid-rebuild row (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md (the grid-rebuild row, and the sentence handing the density scale to 003924B0)

The consumer table and the limits are in [README.md](README.md), section "Affected current consumers":
- the unit-definition page: routed-to-FRONTIER. It is an overlay carrier, and `page_edit.py` is its hunk. PENDING PROPAGATION until FRONTIER commits it;
- the corridor contract and the NavGridParams ctor are OPUS's, under `nav-grid-consumers/`;
- the NavGridParams field rows, the RNG page and L2-VERDICTS agree.

Regression: `navgrid_unitdef.py` (G1-G4, control C, arithmetic N). Run verified at 3d95e439c: FAILS 0, output in `navgrid_unitdef.out`.
