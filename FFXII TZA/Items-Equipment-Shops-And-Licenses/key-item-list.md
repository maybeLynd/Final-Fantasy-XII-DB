---
title: "Key item list: every key item id with its name, sort order, icon and description"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF090, 0x02EBF088, 0x02EBF080, 0x02EBF078, 0x0031C5D0, 0x0031D1B6, 0x0031D218, 0x0031D26B, 0x0031D631, 0x0031D63E"
---

## What it lists

`key-item-list.tsv` holds one line for each of the 512 key-item ids `0x8000`-`0x81FF`, inventory class 13
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)). The class-13 arm of `0x0031C5D0` splits
the range over three tables of 10-byte rows:

| Ids | Table | Entry | Slot | Rows | Named | Icon frame |
|---|---|---|---|---:|---:|---|
| `0x8000`-`0x803F` | m_daiji_data | `+0x88` | `0x02EBF090` | 64 | 47 | 112 |
| `0x8040`-`0x805F` | g_daiji_data | `+0x8C` | `0x02EBF088` | 32 | 27 | 113 |
| `0x8060`-`0x81FF` | q_daiji_data | `+0x90` | `0x02EBF080` | 416 | 109 | 114, and 49-53 on five rows |

The fourth sub-table the class counts, s_daiji_data (entry `+0x94`, `0x02EBF078`), has no rows. The other 329 rows are
named Reserve. The five q_daiji rows with their own icon frame are Dawn Shard, Manufacted Nethicite, Sword of Kings,
Treaty-Blade and Goddess's Magicite. The bounds the validator applies to each of these ranges, and where each one is
compiled in, are on [Item and ability ids](../Engine-Core/item-and-ability-ids.md) ("The thirty-two-class
validator").

### How it is built

`Database/Tools/catalogues/keyitems.py`, with the shared readers in `ffxii_text.py`, reads the three `st2e` tables
and decodes each row as the arm does. The m_daiji arm is quoted below; the g_daiji arm (`0x0031D2C5`-`0x0031D460`) and
the q_daiji arm (`0x0031D488`-`0x0031D61B`, base `0x8060` at `0x0031D622`) read the same offsets.

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u8[2]` | b00 | read and written by no function, so nothing fixes its width: the three table pointers `0x02EBF090`, `0x02EBF088` and `0x02EBF080` are loaded only by `0x0031C5D0`, whose arms read `+0x02`-`+0x09`, by the validator `0x00322C50`, which reads each table's count (`0x00322E3B`-`0x00322E65`), and by the loader `0x00236C30`, which fills each table whole through `0x003845F0` (`0x00236E8C`-`0x00236ECE`) |
| `+0x02` | `u16` | sortOrder | query record `+0x30` (`0x0031D631`-`0x0031D635`), the key Auto-sort `0x002CFFE0` orders by ([Dialogs](../Menus-And-HUD/dialogs.md)) |
| `+0x04` | `u8` | iconFrame | query record `+0x2C` (`0x0031D26B`-`0x0031D26F`) |
| `+0x05` | `u8` | | 0 on every row |
| `+0x06` | `u16` | textId | the description, through `0x002F9860` into query record `+0x10` (`0x0031D218`-`0x0031D221`) |
| `+0x08` | `u16` | nameWord | the name (`0x0031D1B6`) |

The arm sets the record's price `+0x28` to -1 for every key item (`0x0031D63E`). Every one-byte text code goes through
the glyph table of the shipped `us` font `font00.dat` ([Fonts](../Menus-And-HUD/fonts.md)). The 47 named m_daiji rows, the
27 named g_daiji rows and q_daiji rows 13-15 ("Available", "Accepted" and "Complete!") have empty description texts:
rows 0-95 of the shipped `listhelp_daijinamono.bin` are empty.

### Checks

- The tables' headers give 64, 32 and 416 rows of 10 bytes, s_daiji_data 0, and the TSV has 512 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts byte `+0x05` = 0 on every row.
- Rows compared with the arm: id `0x8000` is row 0 of m_daiji_data, Rabanastre, icon frame 112, text 20000; id
  `0x8060` is row 0 of q_daiji_data, sort order 73, icon frame 114, text 20096, "This small bottle contains a
  message: ...".
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id` | the key-item id |
| `table`, `row` | the table that holds it and the row in that table |
| `name` | the shipped name |
| `sort_order`, `icon_frame` | `+0x02`, `+0x04` |
| `b00` | `+0x00` |
| `text_id`, `description` | `+0x06` and its shipped text |
| `explanation` | the table it comes from, and whether its description is empty; "a Reserve row" for the others |

## Related

- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
- [Loot list: every loot id with its name, price, sell price, sort order and description](loot-list.md)
- [Item list: every item with its name, price, sort order, icon, the action it runs and its texts](item-list.md)
