---
title: "MP gain and cost: how MP is gained from walking, from being hit, from hitting and from kills, what an action costs, and what pins MP to zero"
kind: "system"
category: "Status effects and KO"
addresses: "0x00300CE0, 0x00307B0D, 0x002F91A0, 0x002F9240, 0x002FB6C0, 0x002F9400, 0x00309110, 0x002F95D0, 0x00305640"
---

## What the player sees

- **Walking** refills MP a point at a time. The lower the MP, the shorter the walk to the next point, and
  any MP loss, spending included, clears the distance already walked toward it.
- **Being hit** gives MP to a character with the Martyr license (augment 21), more for a bigger hit.
- **Hitting** a foe gives MP with Inquisitor (augment 86) or Warmage (augment 20), each only for actions whose
  row carries that augment's mark.
- **Defeating** a foe gives a quarter of its level in MP with Headsman (augment 23).
- In the areas whose `navimapdata.bin` record sets MP regime 2 or 3 (Terminus No. 7, the Necrohol of Nabudis,
  the Great Crystal, the Pharos, the Henne Mines' Site 7 and Giruvegan; [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)),
  the MP from damage and kills is tripled and walking recovery runs three times as fast.
- The Channeling licenses (augments 91-93) lower what an action costs.

Healing gives no MP, and neither does damage between two units on the same side.

## How it works

### The MP write

`0x00300CE0(stats, delta, flags)` changes current MP `+0x4C` (`0x00300D69`-`0x00300E25`):

1. With flags bit `0x1` clear, the battle and unit eligibility masks of [Gaining and losing
   statuses](status-changes.md) refuse the change on any low bit (`0x00300D42`-`0x00300D63`).
2. The new value is floored at 0 and capped at max MP `+0x28`. With augment 39 in either layer (byte
   `+0x6C` or `+0x7C`, bit `0x80`) the cap is 0, so MP stays at 0 (`0x00300D6D`-`0x00300D9F`).
3. Unless flags bit `0x10` is set, `0x003283D0` shows the change; unless bit `0x80` is set, `0x0028F1F0` reports it
   (`0x00300DA6`-`0x00300DD3`). `0x003283D0` posts a battle number through `0x003BBD00` (`0x00328462`,
   [Battle numbers](../Menus-And-HUD/battle-numbers.md)); `0x0028F1F0` finds the member's counter pair with `0x00296280`
   (`0x0028F20E`) and starts its roll ([Party list](../Menus-And-HUD/party-list.md)).
4. A loss is refused at this point when the unit mask has a high bit (`0x00300DD8`-`0x00300DFE`); otherwise MP is
   stored (`0x00300E00`).
5. A gain also feeds the Mist charges through `0x00300BC0` ([Augments](../Damage-And-Battle-Formulas/augments.md)), and
   any loss clears the walking progress (`0x00300E04`-`0x00300E25`).

Current and max MP are signed 16-bit reads (`0x00300D69`, `0x00300D83`). The show and the report need the unit
`0x0031B860` gives for the stats record (`0x00300D02`, `0x00300DA1`-`0x00300DA4`): `0x003283D0(unit, delta, gain, 1)` gets
`gain` 1 for a positive delta and 0 for a negative one, and for a delta of 0 the flags' bit `0x20`
(`0x00300D1F`-`0x00300D31`); `0x0028F1F0([unit + 8], old, new, 1)` gets the old and the new MP (`0x00300DC4`-`0x00300DD3`).

The walking progress is cleared only with a unit and when the stored MP is below the old (`0x00300E19`-`0x00300E20`):
`0x002FA540(unit)` takes `+0x70` with `0x00320450`, which zeroes it (`0x00320492`), and adds 0 back with `0x00329A20`
(`0x002FA549`-`0x002FA559`).

### What gives MP for damage

`0x00307300` is the only caller of the two gain functions (`0x00307B0D`-`0x00307B8C`). It runs them when the
result changed HP by a delta, `+0x2C` bit `0x100` set and bit `0x8` (an absolute HP) clear. The target's gain is written
with flags `0x10`, then the attacker's.

Both gains need the two units on opposite sides: exactly one of them a party record (`0x002F91EB`-`0x002F91FB`,
`0x002F92A8`-`0x002F92B8`). Both return 0 for a heal.

### Gain from being hit

`0x002F91A0(attacker, target, hpDelta)` gives 0 for a heal (`hpDelta` not below 0) or two units on the same side
(`0x002F91AB`-`0x002F91FB`); otherwise it gives the target the ladder value for the damage when it has Martyr
(augment 21) in either layer, byte `+0x6A` or `+0x7A` bit `0x20` (`0x002F9204`-`0x002F921E`), tripled in an area with MP
regime 2 or 3 (`0x00320160`, `0x002F9220`-`0x002F9234`).

### Gain from dealing damage

`0x002F9240(attacker, target, hpDelta, action, killed)` decides the attacker's gain in this order
(`0x002F9240`-`0x002F93D6`):

1. A heal (`hpDelta` not below 0) or two units on the same side gives 0.
2. With Inquisitor (augment 86: attacker byte `+0x72` or `+0x82`, bit `0x40`) and the action row's `+0x2C` bit `0x8`
   set, the gain is the ladder value for the damage.
3. Otherwise, with Warmage (augment 20: byte `+0x6A` or `+0x7A`, bit `0x10`) and `+0x2C` bit `0x10` set, the gain is the
   ladder value; without either pair it is 0 (`0x002F9329`-`0x002F9389`).
4. With Headsman (augment 23: byte `+0x6A` or `+0x7A`, bit `0x80`) and a kill, it adds `max(target level >> 2, 1)`,
   the level being target byte `+0x1C2` (`0x002F938B`-`0x002F93C0`). A kill here is a target that now has KO,
   Stone or X-Zone without the field's bit `0x8000` (`0x00307B3F`-`0x00307B61`).
5. In an area with MP regime 2 or 3 the total is tripled (`0x002F93C2`-`0x002F93D6`).

The action row is `0x0020E600([[0x02EBF138] + 0x0C]) + action × u16 [[0x02EBF138] + 8]`, summed in 32 bits
(`0x002F9309`-`0x002F9315`, `0x002F9365`-`0x002F9370`). With `[0x02EBF138]` null or that base 0 the row address is 0, and the
bit test reads address `0x2C` and faults (`0x002F92E3`, `0x002F92F1`, `0x002F9323`; `0x002F933F`, `0x002F934D`, `0x002F9377`).

### The damage ladder

`0x002FB6C0(unit, damage)` reads rows 1 to 19 of the MP table `[0x02EBF0B8]` (`0x002FB6E9`-`0x002FB85B`):

```python
for i = 1 .. 19: if damage < row[i].threshold: return row[i - 1].factor
return row[19].factor
```

The factor is row byte `+0x03` for a summoned Esper (a party record of type `0x1B`-`0x27`) and byte `+0x02`
for everyone else (`0x002FB752`-`0x002FB7FE`). A damage of 0 gives 0, as does a negative one (`0x002FB6DE`-`0x002FB6E4`).
The thresholds are the rows' 16-bit words `+0x00` (`0x002FB73F`), and the Esper test needs a stats record with byte
`+0x05` = 0 and type `+0x04` from `0x1B` to `0x27` (`0x002FB752`-`0x002FB76E`).

### Rich areas

Both gain functions triple their result when the area's MP regime `0x00377BA0` is 2 or 3 (`0x002F9220`-`0x002F9234`,
`0x002F93C2`-`0x002F93D6`). The regime is the field `0x3000` of the area's field word, or a value from the save that
replaces it ([Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

### MP from walking

While a unit is active and has none of KO, Stone and X-Zone (or the field's bit `0x8000` is set), the distance its
actor moves each frame is added to unit `+0x70`: on the ground plane, or in three dimensions for an actor with
byte `+8` bit `0x4` (`0x002E5290`-`0x002E5337`, `0x00329A80`).

`0x002F9400(unit)`, run by the periodic step `0x00310DB0` (`0x003110C3`), turns that distance into MP
(`0x002F9400`-`0x002F95AE`):

1. It takes the distance from `+0x70` and compares it with the unit's last stored value, the 32-bit value at
   `+0x18` of its 64-byte record. When the two are equal it stores the value back and gives nothing. A unit that
   is inactive or has KO, Stone or X-Zone without the field's bit `0x8000` gets 0 and loses its progress
   (`0x00320450`-`0x00320492`).
2. It picks the first of rows 20-24 whose MP limit `+0x04` is at least current MP, or row 24.
3. The row's distance `+0x00`, divided by 3 in a rich area, is the walk for one point. A longer distance gives
   1 MP and starts again from 0.
4. The remaining distance goes back into `+0x70`.

The 64-byte record is `0x0208D480 + 64 * type` for a party record (stats `+0x04`), else `0x0208DE80 + 64 *` byte
`+0xEA9` of the unit `0x0031B860` gives, which is kept in `0x02EBF188` (`0x002F941E`-`0x002F9471`). Current MP is a signed
16-bit read against the row's 32-bit limit (`0x002F94FD`-`0x002F9501`); the row's distance is a 32-bit integer made a
float, divided by 3.0 in a rich area, `d = (float)[row + 0x00] / 3.0` when `0x00320160()` returns 2 or 3
(`0x002F9563`-`0x002F957E`). Only a distance above it gives the point, `distance > d` (`0x002F9586`-`0x002F9590`).

The distance left is stored at record `+0x18` and added back to `+0x70` by `0x00329A20(unit, distance)`
(`0x002F95A6`-`0x002F95AE`). On the equal path it is the same value (`0x002F947E`).

`0x00310DB0` writes the point with flags `0x90`, so the gain is neither shown nor reported (`0x003110C8`-`0x003110D7`).

### What an action costs

`0x00309110(unit, action)` gives the MP an action costs (`0x00309110`-`0x003091A3`):

1. An id above `0x21E`, or an action of kind 5 or 6 (row `+0x1E`), costs nothing.
2. Without a unit the cost is the action row's byte `+0x0A`.
3. A unit on the gil channel pays no MP (`0x002F9820`): one that is not an enemy-table record and has
   augment 32 in either layer, byte `+0x6C` / `+0x7C` bit `0x1`.
4. Otherwise `0x002F95D0` adjusts row `+0x0A` (`0x002F962B`-`0x002F9808`).

`0x002F95D0` leaves the cost unchanged for a party record's Quickenings (`0xD0`-`0xE1`, `0x002F9646`-`0x002F9655`)
and Esper summons (`0x106`-`0x112`); the Concurrences (`0xE2`-`0xF1`) are adjusted like other actions. For
every other action, in this order:

| Augment | Cost | Sites |
|---|---|---|
| 32 | `10 * trunc(cost * 64 / 50)`, paid in gil | `0x002F97E4`-`0x002F9802` |
| 91, 92, 93 (Channeling) | `trunc(cost - cost / 100 * sum)`, the sum of word `+4` of augment rows 91-93 present | `0x002F9688`-`0x002F97C1` |
| 51 | 0 | `0x002F97A3`, `0x002F97C7` |
| 36 | `cost / 2`, truncated toward 0 | `0x002F97CD`-`0x002F97DC` |

Each augment counts in either layer. The action pays when it runs: `0x00305640` subtracts the cost with
`0x00300CE0`, its Mist charges with `0x00300BC0` and its gil (`0x003056C1`-`0x0030571A`;
[Action phases](../Battle-Actions/action-phases.md)), the gil through `0x00253690` and `0x00254EE0`
(`0x0030571A`, `0x0030572B`; [Gil](../Rewards-EXP-Gil-And-Loot/gil.md)).

`0x00305640` passes `0x10` as the flags of both calls, plus 1 when its `flag` is non-zero (`0x003056E3`-`0x00305700`):
the MP loss is not shown, and with `flag` the eligibility masks are skipped. The Mist argument is
`-(max MP * 0x00308FF0(unit, id))`, with max MP the signed 16-bit `+0x28` (`0x003056D4`, `0x00305704`-`0x0030570D`), and
the action id is the row's index in `[0x02EBF138]` (`0x0030565E`-`0x00305693`).

The battle menu's list builder `0x0031EB20` runs the same `0x002F9820` and `0x002F95D0` for each action it lists and
keeps the adjusted cost in the entry's word `+0x52`, with entry flag 8 for the gil channel and 2 otherwise
(`0x0031F00C`-`0x0031F072`, [Battle menu](../Menus-And-HUD/battle-menu.md)).

## Shipped data

The MP table is `battle_pack.bin` section 3, 25 rows of 8 bytes, bound by `0x00236C92`. Rows 0-19 are the
damage ladder:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | damage | damage from |
| `+0x02` | `u8` | factor | MP factor |
| `+0x03` | `u8` | esperFactor | Esper MP factor |

The shipped rows:

| Damage from | MP | Esper MP |
|---:|---:|---:|
| 1 | 1 | 6 |
| 50 | 1 | 6 |
| 100 | 1 | 6 |
| 300 | 1 | 6 |
| 500 | 2 | 12 |
| 750 | 2 | 12 |
| 1,000 | 2 | 12 |
| 1,250 | 2 | 12 |
| 1,500 | 3 | 18 |
| 2,000 | 3 | 18 |
| 2,500 | 3 | 18 |
| 3,000 | 4 | 24 |
| 3,500 | 4 | 24 |
| 4,000 | 4 | 24 |
| 5,000 | 5 | 30 |
| 6,000 | 6 | 36 |
| 7,000 | 8 | 48 |
| 8,000 | 10 | 60 |
| 9,000 | 15 | 90 |
| 9,999 | 30 | 180 |

Rows 20-24 are the walking ladder. The range is fixed in the code, not by the file: `0x002F9400` reads row
`20 + i` for `i` = 0 to 4 and falls back to row 24, whatever the table's count says:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | distance | distance per point |
| `+0x04` | `i32` | mpLimit | current MP up to |

The shipped rows:

| Current MP up to | Distance per point |
|---:|---:|
| 25 | 9 |
| 50 | 13 |
| 100 | 18 |
| 200 | 22 |
| above 200 | 27 |

Augment rows 91, 92 and 93 each carry 10 in word `+4`, so the three together cut a cost by 30 %.

## Modding notes

- Both ladders are data in section 3; the code reads exactly 20 damage rows and 5 walking rows, whatever the
  table's count says.
- An action gives MP on a hit only through the two `+0x2C` bits; setting them on an action row makes it count.
- The cost cuts come from augment rows 91-93's word `+4`, so the percentage is data.

## Related

- [Gaining and losing statuses](status-changes.md) - the eligibility masks.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - the augment layers, max MP and the Mist charges.
- [Action definition row](../Battle-Actions/action-definition-row.md) - `+0x0A`, `+0x1E` and `+0x2C`.
- [Action phases](../Battle-Actions/action-phases.md) - when an action pays.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the MP regime.
