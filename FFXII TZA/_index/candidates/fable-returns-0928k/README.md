# Consumer check: the navigation root is cleared before the grid on area unload (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md

**Request:** ASTRA-REQ-FABLE-NAV-ROOT-CALL-ORDER. Re-derived from the certified image's bytes in
[`nav_order_check.py`](nav_order_check.py) ([output](nav_order_check.out)). **Verdict: ACCEPT.**

- **O1: the reset's call order.** The area-teardown reset `002341C0` (62 B) calls `0030FE60`, `00383A20`,
  `00306570` (with ecx 0) and then `00392710`. There is no branch before the grid-teardown call at `002341D5`. So on its
  normal entry, the dataset pointer is cleared before the grid is torn down.
- **O2: the clear.** `00383A20` (12 B) is `mov qword [02AEDFB0], 0 / ret`, which is `Navigation_ClearDataset`.
- **O3: two callers of the clear,** each counted from an image-wide E8/E9 census with an instruction-boundary test:
  - `002341C9`, in the area-teardown reset;
  - `0023699E`, in `002368D0`, the actor-entity body that the startup chain's second hub `0022A0B0` calls.

  So the pointer is cleared once at boot and again on every area unload.
- **Controls (C).** With the two call targets swapped in memory, the order check reads the grid teardown as first. The
  census finds the known call `002341C9`.

**Not established.** `00306570` is called between the clear and the grid teardown, and its effects are not traced here.
So whether the pointer stays 0 until the grid is gone, and whether that call re-binds or schedules anything, stays open.
The other open questions are unload timing, scheduling and atomicity.

| consumer | action | agreement |
|---|---|---|
| `how-a-unit-finds-its-way-across-the-navigation-mesh.md` §1, "`00383A20` clears the pointer" | the two callers and the unload order qualified, with the untraced interval named; addresses left to this record so the page gains no new crossing | revised-here |
| the world-tick page, the `002341C0` subtree | already lists the calls in order; the teardown row was corrected in `fable-returns-0928j` | unchanged |
| OPUS's `NavRunStateBlock` field rows | OPUS's | routed-to-OPUS |

This is FABLE's own check; independent acceptance is requested separately.

Regression: `nav_order_check.py` (O1, O2, O3, C). Run verified at 98f01326b: FAILS 0.
