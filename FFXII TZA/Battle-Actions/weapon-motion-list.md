---
title: "Weapon motion list: the animation set each weapon's motion class gives a battle unit, from the WepJob_Matrix table"
kind: "reference"
category: "Battle actions"
addresses: "0x02EBF180, 0x003202F0, 0x003203B0, 0x00325A20, 0x00325AD0, 0x00320170, 0x00320230"
---

## What it lists

[`weapon-motion-list.tsv`](weapon-motion-list.tsv) holds one line for each of the 23 rows of the table that registry slot `0x02EBF180` points
at (`battle_pack.bin` directory entry `+0x04`). The table is not an `st2e` table: it is a `u16` stride (1), a `u16`
row count (23), and then one byte per row from `+0x04`. Row *m* is a weapon motion class, the byte `+0x26` of a
main-hand equipment row ([Equipment row](../Items-Equipment-Shops-And-Licenses/equipment-row.md)), and its byte is an
animation set.

### How the set is chosen

`0x003202F0(stats, &set)` gives a unit its animation set (`0x003202F0`-`0x00320443`):

1. An enemy record (stats `+0x05` = 1) whose definition row byte `+0x13` is not `0xFF` takes that byte
   (`0x0032031F`-`0x0032033C`).
2. A record whose main hand `+0x50` is `0x1000`, Unarmed, with no off-hand item (`+0x52` = `0xFFFF`) and Brawler (augment 9)
   in either augment layer (`+0x69` or `+0x79` bit `0x2`) takes row 22 (`0x0032034B`-`0x00320384`).
3. Otherwise `0x003203B0(main hand)` takes the row of the main-hand item's motion class `+0x26` when the id is not
   `0xFFFF` and the item's slot bits `+0x07` are below `0x20`; any other id gives row −1, the high byte of the row
   count, 0 (`0x003203B0`-`0x0032043C`).

Its callers:

- `0x00320170` gives the motion lane of a unit's model ([Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md)).
- `0x00320230` does the same for the member in a seat of slot map 4. It answers 22 itself for the seat `0x00327200`
  returns while `0x00303EC0` holds, and uses the Chocobo's record `[0x02EBF190]` + `0x2E58` for seat 3.
- `0x00325A20` and `0x00325AD0`, the two action caches of [Action phases](action-phases.md), call it only for a unit
  that is not a party unit; a party unit (stats `+0x05` = 0) gets the byte of row 1 there, set 1
  (`0x00325A50`-`0x00325A5A`, `0x00325AD0`).

### Where the values come from

Each line is one of the 23 bytes after the stride and count at entry `+0x04`, with, for its motion class, the names
of the main-hand equipment rows 0-419 (slot bits `+0x07` below `0x20`) whose `+0x26` is that class, leaving out the
rows named Reserve.

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u16` | stride | `0x003202F0`, `0x00325A20`, `0x00325AD0` | the row size, 1 |
| `+0x02` | `u16` | count | no instruction | 23 |
| `+0x04` | `u8[23]` | sets | `0x003202F0`, `0x00325A20`, `0x00325AD0` | the animation set of each motion class |

The slot is loaded by `0x00320376` and `0x0032042D` (`0x003202F0`), `0x00325A50` (`0x00325A20`) and `0x00325AF5` (`0x00325AD0`),
and stored once by the loader (`0x00236C74`); none of them reads the count.

### Properties of the shipped rows

- The header gives stride 1 and 23 rows, one TSV line each.
- Example rows: motion class 3 (the 27 weapons listed in the next item) gives set 3;
  motion class 22, read only by the bare-handed rule, gives set 2; row 1, Unarmed, gives set 1, the set of every party
  unit in the action caches.
- The 27 weapons of motion class 3, in equipment table order: Broadsword, Longsword, Iron Sword, Zwill Blade, Ancient Sword, Blood Sword, Lohengrin, Flametongue, Demonsbane, Icebrand, Platinum Sword, Bastard Sword, Diamond Sword, Runeblade, Deathbringer, Stoneblade, Durandal, Mythril Sword, Hero's Blade, Joyeuse, Chirijiraden, Flimsy Blade, Mythril Blade, Kumbha, Great Trango, Karkata, Simha.
- Motion classes 0, 9, 16, 19 and 22 have no shipped weapon; class 22 is reached only through the bare-handed rule.

## Columns

| Column | Meaning |
|---|---|
| `motion_class` | the row, a weapon motion class |
| `animation_set` | the row's byte |
| `weapons`, `first_weapons` | how many main-hand rows have the class, and the first three by name; the 13 main-hand rows named Reserve are not counted (ten of class 1, rows 179 and 180 of class 13, row 186 of class 18) |
| `explanation` | a one-line summary |

## Related

- [Equipment row: every field of a weapon, shield, armor, accessory or ammunition data row and its bonus record](../Items-Equipment-Shops-And-Licenses/equipment-row.md)
- [Action phases: delay, charge time, approach, execution and the end of a battle action](action-phases.md)
- [Actor model rebuild: the state machine that reloads an actor's model, attachments and body for its current definition, and what runs it](../Characters-And-Objects/actor-model-rebuild.md)
