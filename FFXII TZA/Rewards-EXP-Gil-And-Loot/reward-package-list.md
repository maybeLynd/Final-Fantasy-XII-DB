---
title: "Reward package list: every reward package with its gil and items, and where it is named"
kind: "reference"
category: "Rewards: EXP, LP, gil and loot"
addresses: "02EBF070, 002FD530, 0031C5D0, 0031D683, 00322C50"
---

## What it lists

`reward-package-list.tsv` holds one line for each of the 512 rows of the reward-package table that registry slot
`02EBF070` reaches (`battle_pack.bin` directory entry `+98`<sub>h</sub>). Row *n* is package id `9000`<sub>h</sub> + *n*, inventory
class 14 ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): giving the id gives the
package's gil and items together.

- 300 packages give gil, items or both; 212 are empty (no gil and both items `FFFF`<sub>h</sub>), and no selector or script
  give names an empty one.
- The packages' items are items, equipment and loot only (ids `0XXXh`, `1XXXh`, `2XXXh`).
- 268 of the 300 are named by a package selector or by at least one script give; the other 32 are named by
  neither.

### How it is built

`Database/Tools/catalogues/reward_packages.py` reads the `st2e` table at entry `+98`<sub>h</sub> (512 rows of 12 bytes from
the section's `+20`<sub>h</sub>) and names each item through `ids.py`, which reads the name word of the item's own row as the
matching arm of `0031C5D0` does.

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | gil | added to the party's gil, clamped at 0 (`002FD530`) |
| `04`<sub>h</sub> | `u16` | item1 | an inventory id, `FFFF`<sub>h</sub> for none |
| `06`<sub>h</sub> | `u16` | count1 | given as count × the give's sign |
| `08`<sub>h</sub> | `u16` | item2 | an inventory id, `FFFF`<sub>h</sub> for none |
| `0A`<sub>h</sub> | `u16` | count2 | as `count1` |

The class-14 handler `002FD530` gives the gil and then each item that is not `FFFF`<sub>h</sub> through `003008A0`, and the
class-14 arm of `0031C5D0` copies the five fields to the query record (`0031D683`-`0031D6AB`).

The `selectors` column lists the package selectors ([Reward selector list](reward-selector-list.md)) that name the
package, and `script_gives` counts the rows of [Scene rewards](../Story-Events-And-Hunts/scene-rewards.md)
that may give it (a set row counts for each of its packages).

### Checks

- The table's header gives 512 rows of 12 bytes, and the TSV has 512 data lines.
- Two runs over the same files give byte-identical output.
- Rows compared with the handler: `9003`<sub>h</sub> gives 300 gil, Potion x2 and Teleport Stone x1, and selector `A080`<sub>h</sub>
  names it; `9001`<sub>h</sub> gives Potion x3 and Phoenix Down x2.

## Columns

| Column | Meaning |
|---|---|
| `id` | the package id |
| `gil` | `+00`<sub>h</sub> |
| `item1`, `item1_name`, `count1` | `+04`<sub>h</sub>, its shipped name, `+06`<sub>h</sub>; empty for `FFFF`<sub>h</sub> |
| `item2`, `item2_name`, `count2` | `+08`<sub>h</sub>, its shipped name, `+0A`<sub>h</sub>; empty for `FFFF`<sub>h</sub> |
| `selectors` | the package selectors that name it |
| `script_gives` | the number of scene-reward rows that may give it |
| `explanation` | what the package gives, or that it is empty |

## Related

- [Reward selector list: every package selector and the packages it chooses between](reward-selector-list.md)
- [Scene rewards: every item and gil amount the story scripts give or take, by script and function, and how each item is chosen](../Story-Events-And-Hunts/scene-rewards.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
