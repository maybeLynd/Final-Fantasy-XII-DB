---
title: "Category names: the battle command, magick school, element and equipment class name tables"
kind: "reference"
category: "Battle actions"
addresses: "0x02EBF128, 0x02EBF110, 0x02EBF050, 0x02EBF0B0, 0x0031C5D0, 0x00322C50"
---

## What it lists

[`category-names.tsv`](category-names.tsv) holds one line for each row of four tables, 66 in all. Each row only names a number that
other tables use, and is read through the query filler `0x0031C5D0` with an id of its class
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)):

| Table | Slot | Entry | Class | Rows | What the row number is |
|---|---|---|---:|---:|---|
| comac_data | `0x02EBF128` | `+0x48` | 21 | 21 | a battle command, the id in the command lists of [Battle menu](../Menus-And-HUD/battle-menu.md) |
| mgccategory_data | `0x02EBF110` | `+0x30` | 24 | 5 | a magick school, an action row's `+0x2C` & 7 |
| attribute_data | `0x02EBF050` | `+0xA8` | 27 | 8 | an element, in the bit order of [Elements](../Damage-And-Battle-Formulas/elements.md) |
| sobicategory_data | `0x02EBF0B0` | `+0x18` | 28 | 32 | an equipment class, an equipment row's `+0x09` |

The magick schools and equipment classes are the names [Magick list](../Items-Equipment-Shops-And-Licenses/magick-list.md)
and [Equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md) show. The commands numbered 13, 18 and 19
(Gambits, Magicks & Technicks, Mist) are the ones the tutorial groups test on
[Tutorial battle commands](tutorial-battle-commands.md).

### Where the values come from

Each line is a row of one of the four `st2e` tables (rows from each section's `+0x20`), named by its name word
through the word banks and its text id through the text groups, as the arms below do.

| Table | Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|---|
| comac_data | `00` | `u16` | textId | `0x0031DCE4` | help text, through `0x002F9860` to query record `+0x08` |
| comac_data | `02` | `u16` | nameWord | `0x0031DC54`-`0x0031DC9D` | the name, to query record `+0x18` |
| mgccategory_data | `00` | `u16` | textId | `0x0031DCE4` | help text, to query record `+0x08` |
| mgccategory_data | `02` | `u16` | nameWord | `0x0031DE15`-`0x0031DE5E` | the name, to query record `+0x18` |
| attribute_data | `00` | `u16` | nameWord | `0x0031E34F`-`0x0031E389` | the name, to query record `+0x18` |
| sobicategory_data | `00` | `u16` | textId | `0x0031E56A` | 0 on every row; through `0x002F9860` to query record `+0x10` |
| sobicategory_data | `02` | `u16` | nameWord | `0x0031E3EC`-`0x0031E435` | the name, to query record `+0x18` |

Each table is loaded only by `0x0031C5D0`'s arm for its class, the validator `0x00322C50` (the row count) and the
loader `0x00236C30`, and every byte of every row is read by its arm.

### Properties of the shipped rows

- The four headers give 21, 5, 8 and 32 rows of 4, 4, 2 and 4 bytes, one TSV line each.
- Example rows: comac row 0 is Attack, text 3000 "Attack with weapon in hand."; mgccategory row 0
  is White Magicks; attribute row 0 is Fire and row 7 Dark, the bits `0x1` and `0x80` of Elements; sobicategory row 18 is
  Shield, the class of Buckler.
- comac rows 9, 10 and 12 have no name word (0) and no text.

## Columns

| Column | Meaning |
|---|---|
| `table`, `class`, `row` | the table, the id class that reads it, and the row |
| `name_word`, `name` | the name word and its shipped name |
| `text_id`, `text` | the text id and its shipped text; empty for 0 |
| `explanation` | a one-line summary |

## Related

- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
- [Battle menu: the command lists, the party HP and MP list, the help line, the boss and overhead gauges, and how a chosen command is issued](../Menus-And-HUD/battle-menu.md)
- [Magick list: every magick with its name, school, shop price, sort order, MP cost, power, element, statuses and texts](../Items-Equipment-Shops-And-Licenses/magick-list.md)
- [Equipment list: every weapon, shield, armor, accessory and ammunition row with its name, class, price, stats, elements, statuses and bonuses](../Items-Equipment-Shops-And-Licenses/equipment-list.md)
- [Elements: weakness, absorb, half damage, immunity, elemental potency, Oil, and weather and terrain scaling](../Damage-And-Battle-Formulas/elements.md)
