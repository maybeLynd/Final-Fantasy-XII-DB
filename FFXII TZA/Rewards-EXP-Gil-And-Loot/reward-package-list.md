[Home](../../README.md) / [Rewards: EXP, LP, gil and loot](README.md) / Reward package list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Reward package list: every reward package with its gil and items, and where it is named | reference | Rewards: EXP, LP, gil and loot | Gil, prices and reward packages | All 512 reward packages (eis_data, ids 0x9000-0x91FF) of the shipped battle_pack.bin: the gil, the two items with their shipped names and counts, the package selectors and the number of script gives that name each package, and a one-line explanation; 300 packages give something and 212 are empty. | 0x02EBF070, 0x002FD530, 0x0031C5D0, 0x0031D683, 0x00322C50 |

## What it lists

[`reward-package-list.tsv`](reward-package-list.tsv) holds one line for each of the 512 rows of the reward-package table that registry slot
`0x02EBF070` reaches (`battle_pack.bin` directory entry `+0x98`). Row *n* is package id `0x9000` + *n*, inventory
class 14 ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): giving the id gives the
package's gil and items together.

- 300 packages give gil, items or both; 212 are empty (no gil and both items `0xFFFF`), and no selector or script
  give names an empty one.
- The packages' items are items, equipment and loot only (ids `0x0xxx`, `0x1xxx`, `0x2xxx`).
- 299 of the 300 are named by a package selector or by at least one script give; the other one, `0x9001`, is
  named by neither.

### Who gives each package

[`package-givers.tsv`](package-givers.tsv) has one row per package with every giver the tables record:

- 211 packages are given by scene steps alone, 12 by a clan rank and scene steps, and 31 by a trophy trade and
  scene steps;
- 45 are the rewards of the 45 hunts: `questresultwindow(q)` pays selector `0xA000` + q, so no scene step names
  them. `0x902E`, 30,000 gil and the Godslayer's Badge, is selector `0xA0AB`, hunt 171 Farewell to a Legend,
  reported in The Clan Hall;
- the 212 empty packages have no giver, and neither has `0x9001`.

| Column | Meaning |
|---|---|
| `id`, `gives` | the package and what it gives, as in `reward-package-list.tsv` |
| `giver_kinds` | scene, hunt, clan rank and trophy trade, those that apply; `empty` for an empty package |
| `hunt` | the selector, the hunt quest and its name, and where the hunt is reported ([hunts](../Story-Events-And-Hunts/hunts.md)) |
| `clan_rank` | the clan rank whose reward it is |
| `trophy_trade` | the trade's price id, its gil and the map of the trade |
| `scene_gives` | the number of scene-reward rows that give it, and each script with the actor and function; an actor whose copies carry several names is given with all of them, and the step's own tests pick the copy ([scene rewards](../Story-Events-And-Hunts/scene-rewards.md)) |

### Where the values come from

The package table is the `st2e` table at entry `+0x98` (512 rows of 12 bytes from the section's `+0x20`); each
item's name is the name word of the item's own row, as the matching arm of `0x0031C5D0` reads it.

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | gil | times the give's count, added to the party's gil and floored at 0 (`0x002FD530`) |
| `+0x04` | `u16` | item1 | an inventory id, `0xFFFF` for no item |
| `+0x06` | `u16` | count1 | given as count1 times the give's count (negative for a take) |
| `+0x08` | `u16` | item2 | an inventory id, `0xFFFF` for no item |
| `+0x0A` | `u16` | count2 | as `count1` |

The class-14 handler `0x002FD530` acts only on a relative give on channel 1 and otherwise returns 0 at once
(`0x002FD53F`-`0x002FD54C`); it gives the gil and then each item that is not `0xFFFF` through
`0x003008A0(item, count × give's count, 0, 1, flags)`, and returns 0.

The row is the decoded row base plus `(id - 0x9000)` times the stride, added in 32 bits
(`0x002FD586`-`0x002FD5A2`). Nothing guards it: when the slot `0x02EBF070` is null or its decoded row base is 0, the row
address is 0 (`0x002FD56A`-`0x002FD5A6`) and the gil read at `0x002FD5A9` faults, because the first 64 KB of a Windows
x64 process are never mapped. The class-14 arm of `0x0031C5D0` copies the five fields to the query record
(`0x0031D683`-`0x0031D6AB`).

The `selectors` column lists the package selectors ([Reward selector list](reward-selector-list.md)) that name the
package, and `script_gives` counts the rows of [Scene rewards](../Story-Events-And-Hunts/scene-rewards.md)
that may give it (a set row counts for each of its packages; a row that reads "Never given from this script",
whose call runs only when another script's field is loaded, is not counted).

## Columns

| Column | Meaning |
|---|---|
| `id` | the package id |
| `gil` | `+0x00` |
| `item1`, `item1_name`, `count1` | `+0x04`, its shipped name, `+0x06`; empty for `0xFFFF` |
| `item2`, `item2_name`, `count2` | `+0x08`, its shipped name, `+0x0A`; empty for `0xFFFF` |
| `selectors` | the package selectors that name it |
| `script_gives` | the number of scene-reward rows that may give it |
| `explanation` | what the package gives, or that it is empty |

## Related

- [Reward selector list: every package selector and the packages it chooses between](reward-selector-list.md)
- [Scene rewards: every item and gil amount the story scripts give or take, by script and function, and how each item is chosen](../Story-Events-And-Hunts/scene-rewards.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
