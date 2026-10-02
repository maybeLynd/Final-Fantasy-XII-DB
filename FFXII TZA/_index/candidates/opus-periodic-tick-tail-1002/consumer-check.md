# Consumer check: the periodic tick after its first apply, and its gate structure (OPUS, 2026-10-02)

Board task OPUS-PERIODIC-TICK-TAIL-1002. This closes the 10-Status readiness map's structural gap: `00310DB0` after
`00310FAC`. A read-only reader read it whole (296 instructions), and OPUS byte-checked the anchors
(`tick_tail_check.py`, 17 instructions).

- **Corrects:**
  - "six gates, all of which must pass" on both pages. There are seven gates, and only the first three stop
    everything. The readiness probe `00265680`, the two masks and the `0x1000000000` flag skip to the common tail
    `003112A1` (enmity decay and `002FE950`). A party Esper record can be dismissed before them.
  - The pickup table is `02EC0FA0`.
  - `00469E30` receives the stats record.
- **Adds:** section 14 of the periodic tick page: the order and conditions of the Esper dismiss, the trap applies,
  walk MP, the world pickup and Chain Bonus applies, the common tail, and the exit map.
- **Affected:** 10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md, 10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the periodic tick page §2 and §7, the contract's preconditions | revised-here |
  | where-mp-comes-from.md (walk MP at `003110C3` / `003110D7`) | agrees |
  | the world-loot-pickups page and CONTRACT-world-loot-pickup-pool.md (`02EC0FA0`) | agrees |
  | gambit-evaluation-and-enmity.md (the decay-skipping exits, which omit the Esper exit; no effect in play, since the dismiss needs a party record and the decay a foe record) | agrees |
  | RE repo docs/readiness/10-status.md (its structural gap) | routed-to-OPUS (noted from this commit) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-periodic-tick-tail-1002/tick_tail_check.py, verified at 9e2b8ef7e: 17 instructions decode as cited, FAILS 0 ([`tick_tail_check.out`](tick_tail_check.out)). `apply_tick_tail.py` re-runs as ALREADY, FAILS 0.
