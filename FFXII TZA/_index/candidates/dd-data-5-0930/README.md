# DD owner read, batch 5: five Movement-and-Navigation pages handed over by FABLE (SWE2-DATA, 2026-09-30)

affected: 06-Movement-And-Navigation/clamping-a-point-into-a-volume.md, 06-Movement-And-Navigation/the-unit-shape-distance-primitives.md, 06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md, 06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md, 06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md, _index/OPEN-QUESTIONS.md (new rows SD-180..SD-184, SD-190..SD-193)

run: at 11a944474: mv_clamp_checks.py, mv_loco_checks.py and mm_checks.py, each FAILS 0 (the .out files beside them).
All three are static reads of the shipping image through `../rc22-34-resource-readers-0930/pe.py`.

Task `SWE2-DATA-DD-OWNER-READ-5-0930` (target key only). FABLE handed these pages over from
`FABLE-DD-GAMEPLAY-OWNER-READ-0930`. The method is the one used for batches 1-4. No status word was raised.

| page | what changed | residue |
|---|---|---|
| clamping a point into a volume | `00363FD0` returns `t` clamped to [0, 1] and leaves the squared distance in `022D92D4`, which its one caller reads to keep the nearest segment. The walk picks the shape from record byte `+9`: 0 ellipse, 1 box, 2 segment chain. Stale "not established" lines struck and corrected, the `00521BB0` scaling anchored, and sections added (`mv_clamp_checks.py`) | SD-180, SD-181 |
| unit-shape distance primitives | "Pending adoption" struck: the request closed with CON-129, and EXP-138's contract is adopted as a formulas section. The owner of the two helpers is corrected to the separation-pass page. Sections added | SD-182 |
| battle locomotion steering and recovery | the AM-7 residue now has a row. Anchored: the detour `+5.0` and the pair clearance `×0.5` / `÷3`. Struck and corrected: "most bodies not read", the stale threshold line (AM-1, AM-2), and DecodeOrderGoal's size (965 B) (`mv_loco_checks.py`) | SD-183, SD-184 |
| how the engine chooses 3D or flat movement | §8 gains BV-1..BV-5 evidence rows. The `02B40534` writer count is corrected to 8 store sites in 8 functions (`mm_checks.py`) | SD-191, SD-192 |
| setting the movement mode | DP-2 SUPERSEDED on the status line. The mode-0 callees point to the facing contract. Struck and corrected: "who sets 5 is not found" (it is `002692E8`, UQ-101), and the EC7-105 kind-2 line (the code selects class 3). The integrator's non-zero second argument comes from one site, `0025E3AA`. A §12 with key addresses, call chain, modding and evidence is added | SD-190, SD-193 |

## Consumer check

| consumer | disposition |
|---|---|
| the five pages above | revised-here |
| OPEN-QUESTIONS AM-1, AM-2, AM-7, BV-1..BV-5, DP-2, UQ-101, CON-129 | agrees (the pages now follow them) |

## Rule before and after (`documented_rule.py`)

Before: READY 4, NEEDS-POINTER 1. After: PARTIAL 5, on the newly registered SD rows.
