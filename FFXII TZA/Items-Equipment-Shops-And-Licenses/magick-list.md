---
title: "Magick list: every magick with its name, school, shop price, sort order, MP cost, power, element, statuses and texts"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "02EBF0F0, 0031C5D0, 0031CD4C, 0031CD69, 0031CDBE, 0031CDC5, 02EBF110, 00306340"
---

## What it lists

`magick-list.tsv` holds one line for each of the 81 rows of the magick table that registry slot `02EBF0F0` reaches
(`battle_pack.bin` directory entry `+0x78`). Row *n* is magick id `0x3000` + *n*: the class-8 arm of `0031C5D0`
subtracts `0x3000` from the id and multiplies by the row size (`0031CD0D`-`0031CD28`).

Every row's `+0x02` is its action row, rows 0-80 of the action table, and each of those has kind 1 and `+0x22` equal
to the magick id. By school there are 25 White, 25 Black, 20 Time, 6 Green and 5 Arcane magicks.

### How it is built

`Database/Tools/catalogues/magicks.py`, with the shared readers in `ffxii_text.py` and the action fields as on
[Action list](../Battle-Actions/action-list.md):

1. the `st2e` table at entry `+0x78`: 81 rows of 8 bytes from the section's `+0x20`;
2. the name word `+0x04` through the word banks at entry `+0xF8` (`0031CD2B`-`0031CD39`);
3. the action row `+0x02` at entry `+0x3C`, with its help and description lines through the text groups;
4. the school: the action row's `+0x2C & 7`, which the arm stores at query record `+0x3C` (`0031CDBE`-`0031CDC5`),
   named by the row of the same number in the magick-school table (entry `+0x30`, registry slot `02EBF110`). That
   table's five rows hold a help text id `+0x00` and a name word `+0x02`, which `0031C5D0`'s class-24 arm reads
   (`0031DDCF`-`0031DE9C`). The decoder pairs a school number with the row of the same number;
5. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

The row layout, as the class-8 arm copies it (`0031CD4C`-`0031CD69`):

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | price | shop price in gil, query record `+0x28` (`0031CD50`) |
| `+0x02` | `u8` | actionRow | the magick's action row, query record `+0x38` (`0031CD65`); `00306340` hands it to the test of whether a member holds the magick's license ([Party marks](../Menus-And-HUD/party-marks.md)) |
| `+0x03` | `u8` | iconFrame | query record `+0x2C` (`0031CD57`), the icon frame of its list rows |
| `+0x04` | `u16` | nameWord | the name |
| `+0x06` | `u8` | sortOrder | query record `+0x30` (`0031CD5E`), the key Auto-sort `002CFFE0` orders by ([Dialogs](../Menus-And-HUD/dialogs.md)) |
| `+0x07` | `u8` | | 0 on every row |

### Checks

- The table's header gives 81 rows of 8 bytes, and the TSV has 81 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts byte `+0x07` = 0 and that every row's action row has `+0x22` = `0x3000` + row.
- Rows compared with their readers: row 0, Cure, has price 200, action row 0 (8 MP, power 20), school 0, "White
  Magicks"; row 79, Gravity, has price 2300, action row 79 and school 2, "Time Magicks".
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the magick id and its shipped name |
| `sort_order`, `icon_frame`, `price` | `+0x06`, `+0x03`, `+0x00` |
| `action`, `kind_name` | `+0x02`, the action row, and that row's kind |
| `school`, `school_name` | the action row's `+0x2C & 7` and the school's shipped name |
| `cost`, `charge_base`, `power`, `hit` | the action's MP cost `+0x0A`, `+0x09`, `+0x10`, `+0x12` |
| `element` | the action's element `+0x13` |
| `statuses`, `status_effect` | the action's status bits `+0x18`, and whether it adds or removes them (`+0x36` bits 0 and 1) |
| `range_near_tenths`, `reach_tenths`, `area_radius` | the action's `+0x02`, `+0x05`, `+0x06` |
| `flag_names`, `flag2_names` | the action's `+0x0C` and `+0x2C` bits with a named effect |
| `help`, `description` | the action's shipped help and description lines |
| `explanation` | a one-line summary built from the row and its action |

## Related

- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
- [Technick list: every technick with its name, shop price, sort order, power, statuses and texts](technick-list.md)
- [Item list: every item with its name, price, sort order, icon, the action it runs and its texts](item-list.md)
