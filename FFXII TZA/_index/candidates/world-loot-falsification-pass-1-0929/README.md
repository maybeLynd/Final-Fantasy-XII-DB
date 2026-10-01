# Consumer check: falsification pass 1 on CONTRACT-world-loot-pickup-pool (OPUS, 2026-09-29)

## What changed

- **Nothing the contract asserted was false.** Checks W0-W10 all survive, so there is no contradiction row.
- **Added:** the collected counter `022C3174` has a reader outside the pool, `EnemyChain_TryAdvanceRank` (`003183D0`).
  - On the path where the chain count has not passed the rank's threshold, it subtracts `(rank + 1) × counter`, unless
    `022C3178` bit 0 waives it.
  - It zeroes the counter on a rank advance.

  The contract's §5 row and §6 now say so.
- **Made exact:** the despawn's payload is the previous loop iteration's blink payload, or older stack on the first
  iteration. Ops 4 and 5 ignore it either way.
- **Strengthened:** §9's "no RNG on any path" now holds over the whole 215-body closure, including the presentation layer.

## Current consumers

- consumer: [loot-drops-and-enemy-chain.md](../../../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md) agrees. It is
  where the penalty is documented, and the contract now links to it.
- consumer: [world-loot-pickups-the-ten-slot-pool-and-the-despawn.md](../../../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md)
  agrees. It calls `022C3174` the pickups-collected counter, and the pass keeps that name.
- consumer: [EXP-055](../../../_experiments/EXP-055-loot-collection-effects.md) agrees. It observed the increment, including
  for seven empty entries.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_world_loot.py`, checks W0-W10.
- W8 fails if the counter gains a writer or loses its chain reader.
- W10 fails if any generator enters the pool's call closure.

run: verified at 40a9ab8d1 (BROKEN 0), against the certified image `73461d08…`.
