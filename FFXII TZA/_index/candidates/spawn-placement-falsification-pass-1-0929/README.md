# Consumer check: falsification pass 1 on CONTRACT-spawn-placement (OPUS, 2026-09-29)

corrects: 05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md (frontmatter "did not re-derive the bodies" superseded; I4 made exact; §5 gains arcDeg; §9 gains the LCG step count; §10 gains two unguarded divisors)

## What changed

- **Nothing the contract asserted was false.** Checks P0-P8 and P4b all survive, so there is no contradiction row.
- **I4, made exact.** Point mode's band is `00234DA0`'s walk over party slots 0-3. The one caller's flag 0 admits only the
  party-focus slot, and that is the handle the leader getter `003272A0` resolves (P4b: both read `003590D0`).
  - So I4 holds.
  - It gains a failure path: the leader must be one of slots 0-3 and pass the slot's status gate.
  - A first draft read the slot walk as refuting I4. P4b withdrew that before publication.
- **Added facts.**
  - `arcDeg` is the global `02089358`.
  - Each of area mode's two draws steps the shared LCG three times.
  - Radius and angle are quantised (0.01, whole degrees).
  - The divisors `(int)((max − min) · 100)` and `arcDeg` are unguarded, and a NaN band is not refused.

## Current consumers

- consumer: [spawn-placement-and-retirement.md](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) agrees.
  It already scopes "leader alone" to area mode's radius, and gives the four-slot validator with its focus flag and its
  universal rejection.
- consumer: [spawn-placement-height-and-authored-tunables.md](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md) agrees.
  It documents the arc cell, the default 180 from `0023A520` and the setter verb. The contract's §5 now points to it.
- consumer: [EXP-145](../../../_experiments/EXP-145-spawn-placement-exec.md) agrees. It calls `003273B0` a leader check, which P4b
  confirms statically. Its `probe-allslots-fail` case is the non-zero flag this pass describes.
- consumer: `_index/L2-VERDICTS.md` S-16 agrees. It scores the contract and EXP-145; nothing it cites changed.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_spawn_placement.py`, checks P0-P8 and P4b.
- P4b fails if the leader getter and the focus test stop reading the same handle. That is the condition under which I4
  would become false.
- P6 fails on a third draw or a draw on the point path.

run: verified at 092f4823e (BROKEN 0), against the certified image `73461d08…`.
