# Consumer check: 13-Rewards contradictions from a local reconstruction-readiness pass settled on the pages (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-REWARDS-1002: stream R run locally, with no cloud credit. A read-only reader mapped
`13-Rewards-Progression-Economy/` (rated MOSTLY; the map is filed in the RE repo as `docs/readiness/13-rewards.md`).
It found 43 contradictions, 15 of them value-changing, plus two claims every page shares that the bytes refute:
- the chain's rank advance runs before the coin draw, and never on a break;
- the quantity tier's all-admitted edge case.

A second read-only pass drafted the strike edits (`apply_13rewards.py`, 82 edits; only disfavoured sides; strikes
open and close on one line). OPUS re-checked the value-changing items at the bytes (`rewards_check.py`):
- the LP gate;
- the profile row `+0x05` read;
- the weighted pick on a chain break;
- the extra-item gate's condition item;
- counter 11 = LP;
- the `+0x18C` experience cap;
- the level-up event;
- the kind-byte gate;
- the pool init;
- the HUD flags.

- **Affected:** 13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md, 13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md, 13-Rewards-Progression-Economy/CONTRACT-gil-storage-and-movement.md, 13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md, 13-Rewards-Progression-Economy/CONTRACT-loot-rolls-and-the-chain.md, 13-Rewards-Progression-Economy/CONTRACT-world-loot-pickup-pool.md, 13-Rewards-Progression-Economy/README.md, 13-Rewards-Progression-Economy/experience-and-license-point-award.md, 13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md, 13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md, 13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md, 13-Rewards-Progression-Economy/the-chain-and-its-sticky-coin.md, 13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md, 13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md, 13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the fifteen 13-Rewards pages (each disfavoured side; README labels) | revised-here |
  | OPEN-QUESTIONS GR-18 / GR-19 rows (cited, unchanged) | agrees |
  | how-experience-is-computed-and-divided.md front matter, REOPENED by FABLE (owner re-status left) | routed-to-FABLE (a notice) |
  | RE repo `docs/readiness/13-rewards.md` | routed-to-OPUS (filed from this commit) |
  | the growth formula for Strength / Magick Power / Vitality / Speed (`002F9BD0`, the map's structural gap) | routed-to-OPUS (left for a later read) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-rewards-readiness-fixes-1002/rewards_check.py, verified at f1e54ee6b: 18 instructions decode as cited, FAILS 0 ([`rewards_check.out`](rewards_check.out)). `apply_13rewards.py` re-runs as ALREADY (82), FAILS 0.
