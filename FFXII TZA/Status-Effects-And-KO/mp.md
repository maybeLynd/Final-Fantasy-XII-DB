---
title: "MP gain and cost: how MP is gained from walking, from being hit, from hitting and from kills, what an action costs, and what pins MP to zero"
kind: "system"
category: "Status effects and KO"
addresses: "00300CE0, 00307B0D, 002F91A0, 002F9240, 002FB6C0, 002F9400, 00309110, 002F95D0, 00305640"
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

`00300CE0(stats, delta, flags)` changes current MP `+4C`<sub>h</sub> (`00300D69`-`00300E25`):

1. With flags bit 0 clear, the battle and unit eligibility masks of [Gaining and losing
   statuses](status-changes.md) refuse the change on any low bit (`00300D42`-`00300D63`).
2. The new value is floored at 0 and capped at max MP `+28`<sub>h</sub>. With augment 39 in either layer (byte
   `+6C`<sub>h</sub> or `+7C`<sub>h</sub>, bit 7) the cap is 0, so MP stays at 0 (`00300D6D`-`00300D9F`).
3. Unless flags bit 4 is set, `003283D0` shows the change; unless bit 7 is set, `0028F1F0` reports it
   (`00300DA6`-`00300DD3`). `003283D0` posts a battle number through `003BBD00` (`00328462`,
   [Battle numbers](../Menus-And-HUD/battle-numbers.md)); `0028F1F0` finds the member's counter pair with `00296280`
   (`0028F20E`) and starts its roll ([Party list](../Menus-And-HUD/party-list.md)).
4. A loss is refused at this point when the unit mask has a high bit (`00300DD8`-`00300DFE`); otherwise MP is
   stored (`00300E00`).
5. A gain also feeds the Mist charges through `00300BC0` ([Augments](../Damage-And-Battle-Formulas/augments.md)), and
   any loss clears the walking progress (`00300E04`-`00300E25`).

### What gives MP for damage

`00307300` is the only caller of the two gain functions (`00307B0D`-`00307B8C`). It runs them when the
result changed HP by a delta, `+2C`<sub>h</sub> bit 8 set and bit 3 (an absolute HP) clear. The target's gain is written
with flags `10`<sub>h</sub>, then the attacker's.

Both gains need the two units on opposite sides: exactly one of them a party record (`002F91EB`-`002F91FB`,
`002F92A8`-`002F92B8`). Both return 0 for a heal.

### Gain from being hit

`002F91A0(attacker, target, hpDelta)` gives the target the ladder value for the damage when it has Martyr
(augment 21) in either layer, byte `+6A`<sub>h</sub> or `+7A`<sub>h</sub> bit 5 (`002F9204`-`002F921E`).

### Gain from dealing damage

`002F9240(attacker, target, hpDelta, action, killed)` decides the attacker's gain in this order
(`002F9240`-`002F93D6`):

1. A heal (`hpDelta` not below 0) or two units on the same side gives 0.
2. With Inquisitor (augment 86: attacker byte `+72`<sub>h</sub> or `+82`<sub>h</sub>, bit 6) and the action row's `+2C`<sub>h</sub> bit 3
   set, the gain is the ladder value for the damage.
3. Otherwise, with Warmage (augment 20: byte `+6A`<sub>h</sub> or `+7A`<sub>h</sub>, bit 4) and `+2C`<sub>h</sub> bit 4 set, the gain is the
   ladder value; without either pair it is 0 (`002F9329`-`002F9389`).
4. With Headsman (augment 23: byte `+6A`<sub>h</sub> or `+7A`<sub>h</sub>, bit 7) and a kill, it adds `max(target level >> 2, 1)`,
   the level being target byte `+1C2`<sub>h</sub> (`002F938B`-`002F93C0`). A kill here is a target that now has KO,
   Stone or X-Zone without the field's bit 15 (`00307B3F`-`00307B61`).
5. In an area with MP regime 2 or 3 the total is tripled (`002F93C2`-`002F93D6`).

### The damage ladder

`002FB6C0(unit, damage)` reads rows 1 to 19 of the MP table `[02EBF0B8]` (`002FB6E9`-`002FB85B`):

```python
for i = 1 .. 19: if damage < row[i].threshold: return row[i - 1].factor
return row[19].factor
```

The factor is row byte `+03`<sub>h</sub> for a summoned Esper (a party record of type `1B`<sub>h</sub>-`27`<sub>h</sub>) and byte `+02`<sub>h</sub>
for everyone else (`002FB752`-`002FB7FE`). A damage of 0 gives 0.

### Rich areas

Both gain functions triple their result when the area's MP regime `00377BA0` is 2 or 3 (`002F9220`-`002F9234`,
`002F93C2`-`002F93D6`). The regime is bits 12-13 of the area's field word, or a value from the save that
replaces it ([Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

### MP from walking

While a unit is active and has none of KO, Stone and X-Zone (or the field's bit 15 is set), the distance its
actor moves each frame is added to unit `+70`<sub>h</sub>: on the ground plane, or in three dimensions for an actor with
byte `+8` bit 2 (`002E5290`-`002E5337`, `00329A80`).

`002F9400(unit)`, run by the periodic step `00310DB0` (`003110C3`), turns that distance into MP
(`002F9400`-`002F95AE`):

1. It takes the distance from `+70`<sub>h</sub> and compares it with the unit's last stored value, the 32-bit value at
   `+18`<sub>h</sub> of its 64-byte record. When the two are equal it stores the value back and gives nothing. A unit that
   is inactive or has KO, Stone or X-Zone without the field's bit 15 gets 0 and loses its progress
   (`00320450`-`00320492`).
2. It picks the first of rows 20-24 whose MP limit `+04`<sub>h</sub> is at least current MP, or row 24.
3. The row's distance `+00`<sub>h</sub>, divided by 3 in a rich area, is the walk for one point. A longer distance gives
   1 MP and starts again from 0.
4. The remaining distance goes back into `+70`<sub>h</sub>.

`00310DB0` writes the point with flags `90`<sub>h</sub>, so the gain is neither shown nor reported (`003110C8`-`003110D7`).

### What an action costs

`00309110(unit, action)` gives the MP an action costs (`00309110`-`003091A3`):

1. An id above `21E`<sub>h</sub>, or an action of kind 5 or 6 (row `+1E`<sub>h</sub>), costs nothing.
2. Without a unit the cost is the action row's byte `+0A`<sub>h</sub>.
3. A unit on the gil channel pays no MP (`002F9820`): one that is not an enemy-table record and has
   augment 32 in either layer, byte `+6C`<sub>h</sub> / `+7C`<sub>h</sub> bit 0.
4. Otherwise `002F95D0` adjusts row `+0A`<sub>h</sub> (`002F962B`-`002F9808`).

`002F95D0` leaves the cost unchanged for a party record's Quickenings (`D0`<sub>h</sub>-`E1`<sub>h</sub>, `002F9646`-`002F9655`)
and Esper summons (`106`<sub>h</sub>-`112`<sub>h</sub>); the Concurrences (`E2`<sub>h</sub>-`F1`<sub>h</sub>) are adjusted like other actions. For
every other action, in this order:

| Augment | Cost | Sites |
|---|---|---|
| 32 | `10 * trunc(cost * 64 / 50)`, paid in gil | `002F97E4`-`002F9802` |
| 91, 92, 93 (Channeling) | `trunc(cost - cost / 100 * sum)`, the sum of word `+4` of augment rows 91-93 present | `002F9688`-`002F97C1` |
| 51 | 0 | `002F97A3`, `002F97C7` |
| 36 | `cost / 2`, truncated toward 0 | `002F97CD`-`002F97DC` |

Each augment counts in either layer. The action pays when it runs: `00305640` subtracts the cost with
`00300CE0`, its Mist charges with `00300BC0` and its gil (`003056C1`-`0030571A`;
[Action phases](../Battle-Actions/action-phases.md)), the gil through `00253690` and `00254EE0`
(`0030571A`, `0030572B`; [Gil](../Rewards-EXP-Gil-And-Loot/gil.md)).

The battle menu's list builder `0031EB20` runs the same `002F9820` and `002F95D0` for each action it lists and
keeps the adjusted cost in the entry's word `+52`<sub>h</sub>, with entry flag 8 for the gil channel and 2 otherwise
(`0031F00C`-`0031F072`, [Battle menu](../Menus-And-HUD/battle-menu.md)).

## Shipped data

The MP table is `battle_pack.bin` section 3, 25 rows of 8 bytes, bound by `00236C92`. Rows 0-19 are the
damage ladder:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | damage | damage from |
| `02`<sub>h</sub> | `u8` | factor | MP factor |
| `03`<sub>h</sub> | `u8` | esperFactor | Esper MP factor |

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

Rows 20-24 are the walking ladder. The range is fixed in the code, not by the file: `002F9400` reads row
`20 + i` for `i` = 0 to 4 and falls back to row 24, whatever the table's count says:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | distance | distance per point |
| `04`<sub>h</sub> | `i32` | mpLimit | current MP up to |

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
- An action gives MP on a hit only through the two `+2C`<sub>h</sub> bits; setting them on an action row makes it count.
- The cost cuts come from augment rows 91-93's word `+4`, so the percentage is data.

## Related

- [Gaining and losing statuses](status-changes.md) - the eligibility masks.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - the augment layers, max MP and the Mist charges.
- [Action definition row](../Battle-Actions/action-definition-row.md) - `+0A`<sub>h</sub>, `+1E`<sub>h</sub> and `+2C`<sub>h</sub>.
- [Action phases](../Battle-Actions/action-phases.md) - when an action pays.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the MP regime.
