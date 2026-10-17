---
title: "Key item list: every key item id with its name, sort order, icon and description"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "02EBF090, 02EBF088, 02EBF080, 02EBF078, 0031C5D0, 0031D1B6, 0031D218, 0031D26B, 0031D631, 0031D63E"
---

## What it lists

`key-item-list.tsv` holds one line for each of the 512 key-item ids `8000`<sub>h</sub>-`81FF`<sub>h</sub>, inventory class 13
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)). The class-13 arm of `0031C5D0` splits
the range over three tables of 10-byte rows:

| Ids | Table | Entry | Slot | Rows | Named | Icon frame |
|---|---|---|---|---:|---:|---|
| `8000`<sub>h</sub>-`803F`<sub>h</sub> | m_daiji_data | `+88`<sub>h</sub> | `02EBF090` | 64 | 47 | 112 |
| `8040`<sub>h</sub>-`805F`<sub>h</sub> | g_daiji_data | `+8C`<sub>h</sub> | `02EBF088` | 32 | 27 | 113 |
| `8060`<sub>h</sub>-`81FF`<sub>h</sub> | q_daiji_data | `+90`<sub>h</sub> | `02EBF080` | 416 | 109 | 114, and 49-53 on five rows |

The fourth sub-table the class counts, s_daiji_data (entry `+94`<sub>h</sub>, `02EBF078`), has no rows. The other 329 rows are
named Reserve. The five q_daiji rows with their own icon frame are Dawn Shard, Manufacted Nethicite, Sword of Kings,
Treaty-Blade and Goddess's Magicite.

### How it is built

`Database/Tools/catalogues/keyitems.py`, with the shared readers in `ffxii_text.py`, reads the three `st2e` tables
and decodes each row as the arm does. The m_daiji arm is quoted below; the g_daiji arm (`0031D2C5`-`0031D460`) and
the q_daiji arm (`0031D488`-`0031D61B`, base `8060`<sub>h</sub> at `0031D622`) read the same offsets.

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | b00 | no function reads it: the three tables are loaded only by `0031C5D0`, the validator `00322C50` and the loader `00236C30`, and the arm reads `+02`<sub>h</sub>-`+09`<sub>h</sub> |
| `02`<sub>h</sub> | `u16` | sortOrder | query record `+30`<sub>h</sub> (`0031D631`-`0031D635`), the key Auto-sort `002CFFE0` orders by ([Dialogs](../Menus-And-HUD/dialogs.md)) |
| `04`<sub>h</sub> | `u8` | iconFrame | query record `+2C`<sub>h</sub> (`0031D26B`-`0031D26F`) |
| `05`<sub>h</sub> | `u8` | | 0 on every row |
| `06`<sub>h</sub> | `u16` | textId | the description, through `002F9860` into query record `+10`<sub>h</sub> (`0031D218`-`0031D221`) |
| `08`<sub>h</sub> | `u16` | nameWord | the name (`0031D1B6`) |

The arm sets the record's price `+28`<sub>h</sub> to -1 for every key item (`0031D63E`). Every one-byte text code goes through
the glyph table of the shipped `us` font `font00.dat` ([Fonts](../Menus-And-HUD/fonts.md)). The 47 named m_daiji rows, the
27 named g_daiji rows and q_daiji rows 13-15 ("Available", "Accepted" and "Complete!") have empty description texts:
rows 0-95 of the shipped `listhelp_daijinamono.bin` are empty.

### Checks

- The tables' headers give 64, 32 and 416 rows of 10 bytes, s_daiji_data 0, and the TSV has 512 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts byte `+05`<sub>h</sub> = 0 on every row.
- Rows compared with the arm: id `8000`<sub>h</sub> is row 0 of m_daiji_data, Rabanastre, icon frame 112, text 20000; id
  `8060`<sub>h</sub> is row 0 of q_daiji_data, sort order 73, icon frame 114, text 20096, "This small bottle contains a
  message: ...".
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id` | the key-item id |
| `table`, `row` | the table that holds it and the row in that table |
| `name` | the shipped name |
| `sort_order`, `icon_frame` | `+02`<sub>h</sub>, `+04`<sub>h</sub> |
| `b00` | `+00`<sub>h</sub> |
| `text_id`, `description` | `+06`<sub>h</sub> and its shipped text |
| `explanation` | the table it comes from, and whether its description is empty; "a Reserve row" for the others |

## Related

- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
- [Loot list: every loot id with its name, price, sell price, sort order and description](loot-list.md)
- [Item list: every item with its name, price, sort order, icon, the action it runs and its texts](item-list.md)
