---
title: "Technick list: every technick with its name, shop price, sort order, power, statuses and texts"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF0E8, 0x0031C5D0, 0x0031CEEB, 0x0031CF08, 0x00306340"
---

## What it lists

`technick-list.tsv` holds one line for each of the 24 rows of the technick table that registry slot `0x02EBF0E8`
reaches (`battle_pack.bin` directory entry `+0x7C`). Row *n* is technick id `0x4000` + *n*: the class-9 arm of
`0x0031C5D0` subtracts `0x4000` from the id and multiplies by the row size (`0x0031CEB3`-`0x0031CEC8`).

Every row's `+0x02` is its action row, rows 158-181 of the action table, and each of those has kind 2 and `+0x22`
equal to the technick id.

### How it is built

`Database/Tools/catalogues/technicks.py` calls the builder in `magicks.py` for entry `+0x7C`; the rows have the
magick table's layout, as the class-9 arm copies them (`0x0031CEEB`-`0x0031CF08`):

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | price | shop price in gil, query record `+0x28` (`0x0031CEEF`) |
| `+0x02` | `u8` | actionRow | the technick's action row, query record `+0x38` (`0x0031CF04`); `0x00306340` hands it to the test of whether a member holds the technick's license ([Party marks](../Menus-And-HUD/party-marks.md)) |
| `+0x03` | `u8` | iconFrame | query record `+0x2C` (`0x0031CEF6`), 117 on every row |
| `+0x04` | `u16` | nameWord | the name (`0x0031CECA`-`0x0031CED8`) |
| `+0x06` | `u8` | sortOrder | query record `+0x30` (`0x0031CEFD`), the key Auto-sort `0x002CFFE0` orders by ([Dialogs](../Menus-And-HUD/dialogs.md)) |
| `+0x07` | `u8` | | 0 on every row |

Every one-byte text code goes through the glyph table of the shipped `us` font `font00.dat`
([Fonts](../Menus-And-HUD/fonts.md)).

### Checks

- The table's header gives 24 rows of 8 bytes, and the TSV has 24 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts byte `+0x07` = 0 and that every row's action row has `+0x22` = `0x4000` + row.
- Rows compared with their readers: row 0, First Aid, has price 600 and action row 158; row 11, Steal, has price
  1200, sort order 0 and action row 169, the Steal row of [Action list](../Battle-Actions/action-list.md).
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the technick id and its shipped name |
| `sort_order`, `icon_frame`, `price` | `+0x06`, `+0x03`, `+0x00` |
| `action`, `kind_name` | `+0x02`, the action row, and that row's kind |
| `cost`, `charge_base`, `power`, `hit` | the action's `+0x0A`, `+0x09`, `+0x10`, `+0x12` |
| `element` | the action's element `+0x13` |
| `statuses`, `status_effect` | the action's status bits `+0x18`, and whether it adds or removes them (`+0x36` bits 0 and 1) |
| `range_near_tenths`, `reach_tenths`, `area_radius` | the action's `+0x02`, `+0x05`, `+0x06` |
| `flag_names`, `flag2_names` | the action's `+0x0C` and `+0x2C` bits with a named effect |
| `help`, `description` | the action's shipped help and description lines |
| `explanation` | a one-line summary built from the row and its action |

## Related

- [Magick list: every magick with its name, school, shop price, sort order, MP cost, power, element, statuses and texts](magick-list.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
