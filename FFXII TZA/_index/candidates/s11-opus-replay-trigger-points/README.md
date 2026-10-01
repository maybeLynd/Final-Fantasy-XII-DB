# S-11: the authored trigger points executed as shipped code; the unit's height is ignored (OPUS, 2026-09-25, block 317)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
- `CONTRACT-authored-trigger-points.md` (`002F8060`) was the one S-11 contract with no execution (block 304's README,
  "Related").
- This narrow OPUS harness runs it.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Allowed set.** The entry's static closure plus the jump target `002E7410` and the MT19937 body (488 functions).
- **Imports.** Every IAT slot is trapped; memset / memcpy / memmove and `sqrtf` (the distance helper `003A1920`'s
  import) are bridged by name.
- **The generator is the image's own.** Every draw is checked against an independent MT19937(5489).
- **Fixtures** are planted data only:
  - the acting unit, its class-3 actor and position block, and the stats block (the TP-6 bytes);
  - the active field id (payload `+0x1044`);
  - the live-mask table at `02EC3EA0`;
  - the authored point list behind `[022BE948]`.
- **Test outcomes are all `>= 0x200`.** The delivery `0046A9D0` → `0046AB10` refuses an outcome index `>= 0x1FF` at its
  entry (`0046AB19`), which is the shipped behaviour and lets the run continue through the notify and the mask store.
  **The item-grant branch for outcomes below `0x1FF` is not covered.**

**All checks pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `TP1_threshold` | TP-1 | the constant at `00901B34` is `1.2999999523162842`. A point at 1.25, and one at exactly that distance, fire; one at the next float (`1.3000000715`) and one at 1.4 do not |
| `TP2_height_is_ignored` | **TP-2 — contradicted** | a unit **1.0 above** a point 1.0 away horizontally **still fires**, the same as a unit level with it. `002F8150 mov [rsp+0x54], edi` (`edi = 0`) **zeroes the unit's height** right after `00265020` returns. Both heights are 0, so the distance is **horizontal** |
| `TP3_75_25_from_the_draw` | TP-3 | 12 fires: each draws once, every draw equals MT19937(5489), and the outcome is `+0x06` when `draw % 100 < 75`, else `+0x08` |
| `TP4_one_point_flag_and_bit` | TP-4 | with two points in range, **only the first fires**. Its flag id is set in Bank512 (payload `+0x14B4`) and **its live bit is cleared** (mask `0b11` → `0b10`) |
| `TP4_flag_FF_sets_none` | TP-4 | flag id `0xFF` sets no Bank512 bit |
| `TP5_32_point_ceiling` | TP-5 | of 40 listed points, only index 35 in range: nothing fires; index 31 in range fires |
| `TP6_eligibility` | TP-6 | status bit 26, either layer's `0x20`, `rec+5 == 1`, or `rec+5 == 0` with `rec+4` in `0x1B..0x27`: no fire; otherwise it fires |
| `field_not_in_live_table` | not in the contract | a field with no row at `02EC3EA0` has live mask 0, and nothing fires |

## What the execution adds to the contract

1. **TP-2 is wrong.** The contract says the unit's height "is spent against the same budget" and that a point is
   "harder to reach from above or below it". The body zeroes the unit's height too (`002F8150`), so the test is a
   **horizontal** 1.3-unit radius. Measured: a unit 1.0 above a point 1.0 away fires.
2. **TP-1's illustration has its direction reversed.** The original fires only when `d <= 1.2999999523`. A copy
   comparing a higher-precision distance against a decimal 1.3 **additionally** fires for `d` in
   `(1.2999999523, 1.3]`. So the boundary case fires in the copy and **not** in the original, the opposite of the
   contract's sentence. With `f32` distances no value lies between the two, so the difference needs a higher-precision
   reimplementation to show.
3. **The point record is at least 11 bytes.** The delivery `002FB8C0` reads byte `+0x0A` (a zero takes its fast path
   `*out = ctx; return 1`); §3's layout ends at `+0x08`.
4. **The live-mask table is a three-slot ring (static).** `002FB3B0`, called only by `002F8060` after a fire, stores
   a missing field at slot `[+0x24]`, increments `[+0x28]` and advances the slot **modulo 3** (`0x55555556`).
   `002FA230` clears the table; `002F82F0` and `002FA740` also reference it (not read here). TP-4's "once-ever
   guarantee" therefore rests on a mask that only three fields' worth of state holds. Whether an evicted field is
   re-armed is decided by those unread bodies, so it is **not concluded here**.

## Not covered

- the item-grant branch (outcomes `< 0x1FF`);
- `002F82F0` / `002FA740` / `002FA230`;
- the callers;
- a live game.
