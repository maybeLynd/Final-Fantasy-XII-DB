**How Strength, Magick Power, Vitality and Speed grow: `002F9BD0`, read whole (2026-10-01, OPUS, static plus shipped data).** `002F9BD0` is 41 bytes, `002F9BD0`–`002F9BF8`, followed by `int3` padding. It has **no callees**, so "one level down" is empty. It reads no table, no global state and no generator. Its only memory reads are three float constants.

```asm
002F9BD0  movd     xmm1, edx                 ; growth byte (already zero-extended by the caller)
002F9BD4  cvtdq2ps xmm1, xmm1                ; -> float
002F9BD7  mulss    xmm1, [008C5B34]          ; * 0.0078125  (= 1/128, bytes 00 00 00 3C)
002F9BDF  addss    xmm1, xmm0                ; + current stat value
002F9BE3  comiss   xmm1, [008F3134]          ; compare with 100.0 (00 00 C8 42)
002F9BEA  jbe      002F9BF5
002F9BEC  movss    xmm0, [00D0F97C]          ; > 100.0 -> 99.99999237 (FF FF C7 42, largest float below 100)
002F9BF4  ret
002F9BF5  movaps   xmm0, xmm1                ; <= 100.0 -> the sum
002F9BF8  ret
```

**1. Arguments and callers.** `retool.py callers 002F9BD0` lists four direct call sites, all in `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650`, and no RIP-relative references. Each site passes:
- **arg 1, `xmm0`**: the current f32 stat, loaded from the stats record (`0030C74B`, `0030C76C`, `0030C782`, `0030C798`);
- **arg 2, `edx`**: one growth byte from the party row, zero-extended with `movzx` (`0030C757`, `0030C768`, `0030C77E`, `0030C794`);
- **arg 3, `r8d = 0`**: set by `xor r8d, r8d` (`0030C750`, `0030C765`, `0030C77B`, `0030C791`), but the callee never reads `r8`.

`ecx` is not loaded before any of the four calls, and the callee does not read it, so **there is no level argument**. The return value in `xmm0` is stored back to the same field (`0030C760`, `0030C776`, `0030C78C`, `0030C7A2`).

| stat | record field (read / write) | growth byte | call |
|---|---|---|---|
| Strength | `+0x10` (`0030C74B` / `0030C760`) | row `+0x1F` (`0030C757`) | `0030C75B` |
| Magick Power | `+0x14` (`0030C76C` / `0030C776`) | row `+0x22` (`0030C768`) | `0030C771` |
| Vitality | `+0x18` (`0030C782` / `0030C78C`) | row `+0x25` (`0030C77E`) | `0030C787` |
| Speed | `+0x1C` (`0030C798` / `0030C7A2`) | row `+0x28` (`0030C794`) | `0030C79D` |

The caller `0030C650` itself is reached from `0030C470` (`0030C56E`), `00305960` (`003059CB`), `003112F0` (`003113DF`, `003113FD`) and `00312280` (`003124A3`).

**2. The per-stat computation.**
- **Table.** The row is computed by the caller, not by `002F9BD0`. It is `ImageAddress_ResolveRuntimePointer([02EBF130]+0xC)` (`0020E600`: `ecx + [01F83530]`) plus `u16 [[02EBF130]+8] × byte stats[+4]` (`0030C6FC`–`0030C71D`). This is the party definition table `chr_data`, `battle_pack.bin` directory `+0x44`. In the shipped file it is an `st2e` header at file offset `0x1B6A0` with count 40, record size **128**, and rows starting 0x20 bytes after the header.
- **Columns.** Each stat has a three-byte group: base at `+0x1E`, `+0x21`, `+0x24`, `+0x27`; growth at `+0x1F`, `+0x22`, `+0x25`, `+0x28`; and a third byte at `+0x20`, `+0x23`, `+0x26`, `+0x29`. The third byte is 0 in all 40 shipped rows, and neither `0030C470` nor `0030C650` reads it.
- **Random draw.** There is none. `002F9BD0` makes no call, and therefore never reaches `RNG_MT19937_NextU32_Thunk` `00379CD0`. Only the HP helper `002F9A60` and the MP helper `002F9B20` draw (`002F9AD3`, `002F9B8C`).
- **Arithmetic.** `new = value + (float)g × 2⁻⁷`, so the stat gains g/128 per level (`002F9BD0`–`002F9BDF`).
  - g is an unsigned byte, 0–255, so the per-level gain ranges from 0 to 1.9921875. `cvtdq2ps` is a signed conversion, but a 0–255 input is exact.
  - The multiply is exact. The add rounds to nearest, but every value the walk can produce, below 128 in steps of 1/128, fits in 14 significant bits, so the accumulation is exact fixed-point with 7 fractional bits.
  - There is no lower clamp, because the increment is never negative.
- **Clamp.** If the sum is **strictly greater than 100.0**, the result is 99.99999237 (`002F9BE3`–`002F9BEC`). A sum of exactly 100.0 is kept (`jbe`). A capped value stays capped, because the next add exceeds 100 again.
- **Store.** The result goes back to the f32 field it was read from (table above).
- **Display.** The integer the game shows is produced later. `BattleStats_RebuildEffectiveStatsAndAffinityState` truncates each float with `cvttss2si` (`002FF0C2` Str, `002FF0CD` Mag, `002FF099` Vit, `002FF0B7` Spd). After equipment and licence bonuses it clamps each to 99 and stores the effective bytes `+0x2A`–`+0x2D` (`002FF840`–`002FF88E`).

**The walk around it.**
- `0030C470` zeroes the level byte `+0x1C2` (`0030C496`) and seeds each float with `(float)` of the row's base byte, with no clamp (`0030C50B`–`0030C546`). It then calls `0030C650(rec, target, 2)` (`0030C562`–`0030C56E`).
- `0030C650` runs one iteration per level from the current level to `min(target, 99)` (`0030C67A`–`0030C682`, back-edge `0030C865`). It skips growth when the level is already 99 (`0030C6CC`) or when the record kind `+5` is non-zero (`0030C6D9`).
- So for a party record walked up from 0, **`stat(L) = min-clamp(base + L × g / 128)`**. The level itself never enters the float formula.

**3. One formula or four?** One formula. All four stats call the same function with the same operation; only the f32 field and the row byte differ. The groups are three bytes apart in the row and four bytes apart in the record. HP and MP use different functions: a level-indexed table with a random bonus (`002F9A60`, `002F9B20`).

**4. Worked example: Vaan, party row 0 (shipped `battle_pack.bin`, row bytes `+0x1E`–`+0x29` = `17 48 00 16 43 00 18 30 00 18 12 00`).**

| stat | base | growth g | per level (exact) | level 1 | level 99 | level-ups adding +1 / +0 (levels 2–99) |
|---|---|---|---|---|---|---|
| Strength | 23 | 72 | +0.5625 | 23.5625 → 23 | 78.6875 → 78 | 55 / 43 |
| Magick Power | 22 | 67 | +0.5234375 | 22.52 → 22 | 73.82 → 73 | 51 / 47 |
| Vitality | 24 | 48 | +0.375 | 24.375 → 24 | 61.125 → 61 | 37 / 61 |
| Speed | 24 | 18 | +0.140625 | 24.14 → 24 | 37.92 → 37 | 13 / 85 |

- **Fixed increments.** The float gain per level is fixed, and the displayed base stat rises by 0 or 1 per level. It never rises by 2, because every character row's g is below 128.
- **Other characters.** The other five main characters' g bytes are: Ashe 68/70/44/17, Fran 64/63/47/18, Balthier 67/59/45/19, Basch 69/56/36/16, Penelo 65/72/48/16.
- **When the cap matters.** The cap never fires for the main cast, whose largest level-99 value is 78.69. It does fire for the Esper rows' Magick Power (base 47, g 75–78) and on the first growth of rows 17, 25 and 26. Those rows have base `0xFF` (255) and sit above 100 until `002F9BEC` clamps them.
- **Method.** The level-1 and level-99 values were computed with float32 arithmetic that mirrors `002F9BD7`–`002F9BEC`. None of this was executed in the game.
