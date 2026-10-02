# Consumer check: the four float stats' growth formula 002F9BD0 (OPUS, 2026-10-02)

Board task OPUS-GROWTH-FORMULA-1002. This closes the 13-Rewards readiness map's structural gap. A read-only reader read
`002F9BD0` and its four call sites, and replayed the shipped rows; OPUS byte-checked the code and constants
(`growth_check.py`, 12 instructions and 3 constants).

- **Corrects:**
  - the level-up page's `002F9BD0(level, growth, 0, value)`: there is no level argument;
  - the unit-definition page's "456-byte rows" for the party definition table: rows are the descriptor's word `+8`
    long, 128 in the shipped data, and 456 is the spacing of the party stats records.
- **Adds:**
  - section 4a of the level-up page: `stat(L) = base + L * g / 128`, clamped to `99.99999237` above `100.0`,
    one formula for Strength, Magick Power, Vitality and Speed, no draw, and a worked example for Vaan;
  - the formula note on the contract.
- **Affected:** 13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md, 13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md, 04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the level-up page section 4 table and new section 4a; the contract's determinism note | revised-here |
  | the unit-definition page's `02EBF130` row | revised-here |
  | the stat rebuild `002FF0C2`-`002FF88E` (truncation, bonuses, cap 99) as documented on the level-up and battle-unit pages | agrees |
  | RE repo docs/readiness/13-rewards.md (its structural gap) | routed-to-OPUS (noted from this commit) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-growth-formula-1002/growth_check.py, verified at 1305be85a: 12 instructions and 3 float constants as cited, FAILS 0 ([`growth_check.out`](growth_check.out)). `apply_growth.py` re-runs as ALREADY, FAILS 0.
