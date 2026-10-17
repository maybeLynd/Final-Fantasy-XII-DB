---
title: "Magick list: every magick with its name, school, shop price, sort order, MP cost, power, element, statuses and texts"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "02EBF0F0, 0031C5D0, 0031CD4C, 0031CD69, 0031CDBE, 0031CDC5, 02EBF110, 00306340"
---

## What it lists

`magick-list.tsv` holds one line for each of the 81 rows of the magick table that registry slot `02EBF0F0` reaches
(`battle_pack.bin` directory entry `+78`<sub>h</sub>). Row *n* is magick id `3000`<sub>h</sub> + *n*: the class-8 arm of `0031C5D0`
subtracts `3000`<sub>h</sub> from the id and multiplies by the row size (`0031CD0D`-`0031CD28`).

Every row's `+02`<sub>h</sub> is its action row, rows 0-80 of the action table, and each of those has kind 1 and `+22`<sub>h</sub> equal
to the magick id. By school there are 25 White, 25 Black, 20 Time, 6 Green and 5 Arcane magicks.

### How it is built

`Database/Tools/catalogues/magicks.py`, with the shared readers in `ffxii_text.py` and the action fields as on
[Action list](../Battle-Actions/action-list.md):

1. the `st2e` table at entry `+78`<sub>h</sub>: 81 rows of 8 bytes from the section's `+20`<sub>h</sub>;
2. the name word `+04`<sub>h</sub> through the word banks at entry `+F8`<sub>h</sub> (`0031CD2B`-`0031CD39`);
3. the action row `+02`<sub>h</sub> at entry `+3C`<sub>h</sub>, with its help and description lines through the text groups;
4. the school: the action row's `+2Ch & 7`, which the arm stores at query record `+3C`<sub>h</sub> (`0031CDBE`-`0031CDC5`),
   named by the row of the same number in the magick-school table (entry `+30`<sub>h</sub>, registry slot `02EBF110`). That
   table's five rows hold a help text id `+00`<sub>h</sub> and a name word `+02`<sub>h</sub>, which `0031C5D0`'s class-24 arm reads
   (`0031DDCF`-`0031DE9C`). The decoder pairs a school number with the row of the same number;
5. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

The row layout, as the class-8 arm copies it (`0031CD4C`-`0031CD69`):

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | price | shop price in gil, query record `+28`<sub>h</sub> (`0031CD50`) |
| `02`<sub>h</sub> | `u8` | actionRow | the magick's action row, query record `+38`<sub>h</sub> (`0031CD65`); `00306340` hands it to the test of whether a member holds the magick's license ([Party marks](../Menus-And-HUD/party-marks.md)) |
| `03`<sub>h</sub> | `u8` | iconFrame | query record `+2C`<sub>h</sub> (`0031CD57`), the icon frame of its list rows |
| `04`<sub>h</sub> | `u16` | nameWord | the name |
| `06`<sub>h</sub> | `u8` | sortOrder | query record `+30`<sub>h</sub> (`0031CD5E`), the key Auto-sort `002CFFE0` orders by ([Dialogs](../Menus-And-HUD/dialogs.md)) |
| `07`<sub>h</sub> | `u8` | | 0 on every row |

### Checks

- The table's header gives 81 rows of 8 bytes, and the TSV has 81 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts byte `+07`<sub>h</sub> = 0 and that every row's action row has `+22`<sub>h</sub> = `3000`<sub>h</sub> + row.
- Rows compared with their readers: row 0, Cure, has price 200, action row 0 (8 MP, power 20), school 0, "White
  Magicks"; row 79, Gravity, has price 2300, action row 79 and school 2, "Time Magicks".
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the magick id and its shipped name |
| `sort_order`, `icon_frame`, `price` | `+06`<sub>h</sub>, `+03`<sub>h</sub>, `+00`<sub>h</sub> |
| `action`, `kind_name` | `+02`<sub>h</sub>, the action row, and that row's kind |
| `school`, `school_name` | the action row's `+2Ch & 7` and the school's shipped name |
| `cost`, `charge_base`, `power`, `hit` | the action's MP cost `+0A`<sub>h</sub>, `+09`<sub>h</sub>, `+10`<sub>h</sub>, `+12`<sub>h</sub> |
| `element` | the action's element `+13`<sub>h</sub> |
| `statuses`, `status_effect` | the action's status bits `+18`<sub>h</sub>, and whether it adds or removes them (`+36`<sub>h</sub> bits 0 and 1) |
| `range_near_tenths`, `reach_tenths`, `area_radius` | the action's `+02`<sub>h</sub>, `+05`<sub>h</sub>, `+06`<sub>h</sub> |
| `flag_names`, `flag2_names` | the action's `+0C`<sub>h</sub> and `+2C`<sub>h</sub> bits with a named effect |
| `help`, `description` | the action's shipped help and description lines |
| `explanation` | a one-line summary built from the row and its action |

## Related

- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
- [Technick list: every technick with its name, shop price, sort order, power, statuses and texts](technick-list.md)
- [Item list: every item with its name, price, sort order, icon, the action it runs and its texts](item-list.md)
