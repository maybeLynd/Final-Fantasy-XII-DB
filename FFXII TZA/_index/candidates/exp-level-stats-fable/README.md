# The four f32 base stats are Strength, Magick Power, Vitality and Speed, in that order (FABLE, Claude Opus 5.5, 2026-09-29)

**The question.** `PKG-GP-EXP-LEVEL-UP` item E4. Each level grows four f32 base stats at stats-record `+0x10`, `+0x14`, `+0x18` and `+0x1C`. The field map calls them only "f32 stat 1..4", and the level-up page recorded "which stats the six fields are" as not claimed. A developer needs to know which one is Strength.

**Answer (static, `statmap.py` R F S K, FAILS 0).** They become the four attributes in stats-record order. `BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`) is decoded whole from its entry, and:

| check | what it shows |
|---|---|
| **R, the output block** | `rsi` is the caller's block or, when that is null, `rdi + 0x24` (`002FEFAB`). The same block receives max HP at `[rsi]` (clamped to 0x7FFF) and max MP at `[rsi + 4]` (clamped to 999), which are the field map's `+0x24` and `+0x28`. So on the default path `rsi + k` is record `+0x24 + k` |
| **F, the four reads** | `cvttss2si` reads `+0x10` into `r12d`, `+0x14` into `r13d`, `+0x18` into the slot `[rsp + 0x2c]` and `+0x1C` into `[rsp + 0x30]` |
| **S, the four stores** | each value is clamped to 99 (`r15d = 0x63`) and stored in the same order at `[rsi + 6]`, `[rsi + 7]`, `[rsi + 8]` and `[rsi + 9]`, which are `+0x2A`, `+0x2B`, `+0x2C` and `+0x2D`. The next three stores (`+0x2E`–`+0x30`) clamp to 255 instead, the split the attack page describes |
| **K, nothing in between replaces them** | the party arm jumps to `002FF3D0`. From there to the stores the four accumulators are only added to (equipment and licence bonuses, `002FF4D3`–`002FF6D0`), apart from the clamp's own floor |

**So:**
- f32 `+0x10` → `+0x2A` **Strength**;
- `+0x14` → `+0x2B` **Magick Power**;
- `+0x18` → `+0x2C` **Vitality**;
- `+0x1C` → `+0x2D` **Speed**.

Each is recomputed from the float plus bonuses on every rebuild and capped at 99.

**Where the names come from.** [The attack page](../../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) §3 names the effective bytes. Strength (`+0x2A`) and Magick Power (`+0x2B`) are confirmed there by their `Reduce…To70Percent` writers. Vitality (`+0x2C`) and Speed (`+0x2D`) are named from function names only. This record ties the floats to the bytes; for the last two it inherits the page's naming evidence and does not strengthen it.

**Not claimed.** The enemy arm (`002FF0E1`–`002FF3D0`) fills the same accumulators from its definition row with level scaling. It is noted, not decoded here.

**Consumers to update.** The battle-stats field map's rows `+0x010`, `+0x014`, `+0x018` and `+0x01C` ("f32 stat 1..4"), and the level-up page's E2 pointer, which names E4 as open.
