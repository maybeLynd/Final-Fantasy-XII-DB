# Consumer check: falsification pass 1 on CONTRACT-corridor-query-family (OPUS, 2026-09-29)

corrects: 06-Movement-And-Navigation/CONTRACT-corridor-query-family.md (§4 "writes no global on any path that returns", §5's written row and §15's evidence row; §9's race widened)

## What was corrected

- **The no-global-write headline.**
  - `RDEC` (`0032A6E0`) stores 16 bytes to `022D91B0` (`movdqu`, `0032A735`) and returns normally. The contract's own census
    had found that site.
  - `BMASK` (`003912E0`) memsets the buffer behind the global pointer `[02AEE0B0]` and ORs into it, then returns.
  - Only `__report_gsfailure`'s seven sites are non-returning.
  - What holds is narrower: no verdict reads an earlier call's write. `CON-161`.
- **What `022D91B0` is.** It is the shared transform workbench's `vf1`, with 53 writing and 48 reading functions, so a corridor
  query overwrites it as a side effect. §9's race is with every workbench user, not only another `RDEC`.
- **What survives.** Checks K0 and K2-K7:
  - the 102-body closure, with no generator in it;
  - the literal returns;
  - the mode re-read;
  - `PATHW`'s five `QWALK` calls and `VADD`;
  - the identity byte and the stale-handle null;
  - the NaN tolerance and `GATE`'s early exit.

## Current consumers

- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-161`).
- consumer: [CONTRACT-shared-transform-workbench.md](../../../00-Engine-Core-Runtime/CONTRACT-shared-transform-workbench.md) agrees.
  Its register census (`Shared-Transform-Workbench/members/ee-register-census.tsv`) already lists `0032A6E0` among the bank's
  writers. The corridor contract now links to it.
- consumer: [how-a-unit-finds-its-way-across-the-navigation-mesh.md](../../../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md)
  agrees. It documents the mechanism below the query layer and makes no global-write claim about this family.
- consumer: [battle-locomotion-steering-and-recovery.md](../../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
  agrees. It names `00335B60` and `003357B0` and their polarities, which K3 confirms. It makes no write claim.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_corridor_query.py`, checks K0-K7.
- K1 fails if the closure's RIP-relative writes change, if `RDEC` stops returning after its store, or if `BMASK` stops
  writing through `[02AEE0B0]`. It rejects "no global on any path that returns".
- K2 fails if a closure function reads `022D91B0`, which would make a verdict depend on an earlier call.

run: verified at f2ab6f431 (BROKEN 0), against the certified image `73461d08…`.
