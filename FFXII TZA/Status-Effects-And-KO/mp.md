---
title: "MP gain and cost: how MP is gained from walking, from being hit, from hitting and from kills, what an action costs, and what pins MP to zero"
kind: "system"
category: "Status effects and KO"
summary: "Where MP comes from and where it goes: the walking recovery ladder keyed on current MP, the damage ladder for being hit and for hitting, the three augments each gain needs, the kill bonus from the foe's level, the rules every gain obeys, the areas that triple MP gains, the cap and the augment that pins MP to zero, the MP cost of an action with its halving, freeing and percentage cuts, and the gil channel that pays an action in gil."
addresses: "00300CE0, 00307B0D, 002F91A0, 002F9240, 002FB6C0, 002F9400, 00309110, 002F95D0, 00305640"
---

## What the player sees

- **Walking** refills MP a point at a time. The lower the MP, the shorter the walk to the next point, and
  spending MP throws away the progress toward it.
- **Being hit** gives MP to a character with "Gain MP after taking damage", more for a bigger hit.
- **Hitting** a foe gives MP with "Gain MP after dealing damage", or for magick with "Gain MP after dealing
  magick damage", but only for actions marked to give it.
- **Defeating** a foe gives a quarter of its level in MP with "Gain MP after defeating a foe".
- In some areas every MP gain is tripled and walking recovery runs three times as fast.
- "Reduces magick MP cost by 10%" lowers what an action costs.

Healing gives no MP, and neither does damage between two units on the same side.

## How it works

### The MP write

`00300CE0(stats, delta, flags)` changes current MP `+0x4C` (`00300D69`-`00300E25`):

1. With flags bit 0 clear, the battle and unit eligibility masks of [Gaining and losing
   statuses](status-changes.md) refuse the change on any low bit (`00300D42`-`00300D63`).
2. The new value is floored at 0 and capped at max MP `+0x28`. With augment 39 in either layer (byte
   `+0x6C` or `+0x7C`, bit 7) the cap is 0, so MP stays at 0 (`00300D6D`-`00300D9F`).
3. Unless flags bit 4 is set, `003283D0` shows the change; unless bit 7 is set, `0028F1F0` reports it
   (`00300DA6`-`00300DD3`).
4. A loss is refused at this point when the unit mask has a high bit (`00300DD8`-`00300DFE`); otherwise MP is
   stored (`00300E00`).
5. A gain also feeds the Mist charges through `00300BC0` ([Augments](../Damage-And-Battle-Formulas/augments.md)), and
   any loss clears the walking progress (`00300E04`-`00300E25`).

### What gives MP for damage

`00307300` is the only caller of the two gain functions (`00307B0D`-`00307B8C`). It runs them when the
result changed HP by a delta, `+0x2C` bit 8 set and bit 3 (an absolute HP) clear. The target's gain is written
with flags `0x10`, then the attacker's.

Both gains need the two units on opposite sides: exactly one of them a party record (`002F91EB`-`002F91FB`,
`002F92A8`-`002F92B8`). Both return 0 for a heal.

### Gain from being hit

`002F91A0(attacker, target, hpDelta)` gives the target the ladder value for the damage when it has augment 21
in either layer, byte `+0x6A` or `+0x7A` bit 5 (`002F9204`-`002F921E`).

### Gain from dealing damage

`002F9240(attacker, target, hpDelta, action, killed)` gives the attacker the ladder value for the damage through
either of two routes (`002F92BA`-`002F9389`):

| Route | Augment | Action row `+0x2C` |
|---|---|---|
| tried first | 86 "Gain MP after dealing damage", byte `+0x72` / `+0x82` bit 6 | bit 3 |
| then | 20 "Gain MP after dealing magick damage", byte `+0x6A` / `+0x7A` bit 4 | bit 4 |

When route A's action bit is clear the code tries route B. With augment 23 "Gain MP after defeating a foe"
(byte `+0x6A` / `+0x7A` bit 7) and a kill, it adds `max(target level >> 2, 1)` (`002F938B`-`002F93C0`). A kill
here is a target that now has KO, Stone or X-Zone without the field's bit 15 (`00307B3F`-`00307B61`).

### The damage ladder

`002FB6C0(unit, damage)` reads rows 1 to 19 of the MP table `[02EBF0B8]` (`002FB6E9`-`002FB85B`):

```
for i = 1 .. 19: if damage < row[i].threshold: return row[i - 1].factor
return row[19].factor
```

The factor is row byte `+0x03` for a summoned Esper (a party record of type `0x1B`-`0x27`) and byte `+0x02`
for everyone else (`002FB752`-`002FB7FE`). A damage of 0 gives 0.

### Rich areas

Both gain functions triple their result when the area's MP regime `00377BA0` is 2 or 3 (`002F9220`-`002F9234`,
`002F93C2`-`002F93D6`). The regime is bits 12-13 of the area's field word, or a value from the save that
replaces it ([Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

### MP from walking

While a unit is active and has none of KO, Stone and X-Zone (or the field's bit 15 is set), the distance its
actor moves each frame is added to unit `+0x70`: on the ground plane, or in three dimensions for an actor with
byte `+8` bit 2 (`002E5290`-`002E5337`, `00329A80`).

`002F9400(unit)`, run by the periodic step `00310DB0` (`003110C3`), turns that distance into MP
(`002F9400`-`002F95AE`):

1. It takes the distance from `+0x70` and compares it with the unit's last stored value, the 32-bit value at
   `+0x18` of its 64-byte record. When the two are equal it stores the value back and gives nothing. A unit that
   is inactive or has KO, Stone or X-Zone without the field's bit 15 gets 0 and loses its progress
   (`00320450`-`00320492`).
2. It picks the first of rows 20-24 whose MP limit `+0x04` is at least current MP, or row 24.
3. The row's distance `+0x00`, divided by 3 in a rich area, is the walk for one point. A longer distance gives
   1 MP and starts again from 0.
4. The remaining distance goes back into `+0x70`.

`00310DB0` writes the point with flags `0x90`, so the gain is neither shown nor reported (`003110C8`-`003110D7`).

### What an action costs

`00309110(unit, action)` gives the MP an action costs (`00309110`-`003091A3`):

1. An id above `0x21E`, or an action of kind 5 or 6 (row `+0x1E`), costs nothing.
2. Without a unit the cost is the action row's byte `+0x0A`.
3. A unit on the gil channel pays no MP (`002F9820`): one that is not an enemy-table record and has
   augment 32 in either layer, byte `+0x6C` / `+0x7C` bit 0.
4. Otherwise `002F95D0` adjusts row `+0x0A` (`002F962B`-`002F9808`).

`002F95D0` leaves the cost unchanged for a party record's Quickenings and Concurrences (`0xD0`-`0xE1`) and Esper
summons (`0x106`-`0x112`). For every other action, in this order:

| Augment | Cost | Sites |
|---|---|---|
| 32 | `10 * trunc(cost * 64 / 50)`, paid in gil | `002F97E4`-`002F9802` |
| 91, 92, 93 "Reduces magick MP cost by 10%" | `trunc(cost - cost / 100 * sum)`, the sum of word `+4` of augment rows 91-93 present | `002F9688`-`002F97C1` |
| 51 | 0 | `002F97A3`, `002F97C7` |
| 36 | halved | `002F97CD`-`002F97DC` |

Each augment counts in either layer. The action pays when it runs: `00305640` subtracts the cost with
`00300CE0`, its Mist charges with `00300BC0` and its gil (`003056C1`-`0030571A`;
[Action phases](../Battle-Actions/action-phases.md)).

## Shipped data

The MP table is `battle_pack.bin` section 3, 25 rows of 8 bytes, bound by `00236C92`. Rows 0-19 are the
damage ladder:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16` | damage | damage from |
| `02` | `u8` | factor | MP factor |
| `03` | `u8` | esperFactor | Esper MP factor |

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

Rows 20-24 are the walking ladder:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | distance | distance per point |
| `04` | `i32` | mpLimit | current MP up to |

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
