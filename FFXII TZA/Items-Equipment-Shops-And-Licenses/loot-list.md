---
title: "Loot list: every loot id with its name, price, sell price, sort order and description"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF098, 0x0031C5D0, 0x0031CBA3, 0x0031CBC1, 0x0031CBE0, 0x0031CBE7, 0x0031CBFA, 0x0031CC01, 0x0057DBC2"
---

## What it lists

`loot-list.tsv` holds one line for each of the 512 rows of the loot table that registry slot `0x02EBF098` reaches
(`battle_pack.bin` directory entry `+0x84`). Row *n* is loot id `0x2000` + *n*, inventory class 7
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): the class-7 arm of `0x0031C5D0`
subtracts `0x2000` from the id and multiplies by the row size (`0x0031CBA3`-`0x0031CBBE`).

- 235 rows are named loot: rows 0, 32-245, 256-269 and 274-279.
- The other 277 rows are named Reserve, with icon frame 0.
- Two rows, 274 Sandalwood Chop and 275 Pinewood Chop, have price 0, so a shop will not buy them.

### How it is built

`Database/Tools/catalogues/loot.py`, with the shared readers in `ffxii_text.py`, reads the `st2e` table at entry
`+0x84` (512 rows of 10 bytes from the section's `+0x20`), the names through the word banks at entry `+0xF8` and the
descriptions through the text groups. Every one-byte text code goes through the glyph table of the shipped `us`
font `font00.dat` ([Fonts](../Menus-And-HUD/fonts.md)).

The row layout, as the class-7 arm copies it:

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | price | query record `+0x28` (`0x0031CBE0`); a shop pays half, rounded down, and will not buy loot whose half is 0 ([Shop screens](../Menus-And-HUD/shop-screens.md), `0x0057DBC2`) |
| `+0x02` | `u16` | textId | the description, through `0x002F9860` into query record `+0x10` (`0x0031CBE7`-`0x0031CBF6`); `14000` + row on every row |
| `+0x04` | `u8` | iconFrame | query record `+0x2C` (`0x0031CBFA`); 73 on every named row |
| `+0x05` | `u8` | | 0 on every row |
| `+0x06` | `u16` | nameWord | the name (`0x0031CBC1`) |
| `+0x08` | `u16` | sortOrder | query record `+0x30` (`0x0031CC01`), the key Auto-sort `0x002CFFE0` orders by ([Dialogs](../Menus-And-HUD/dialogs.md)); equal to the row on every row |

### Checks

- The table's header gives 512 rows of 10 bytes, and the TSV has 512 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts byte `+0x05` = 0 on every row.
- Rows compared with their readers: row 0, Teleport Stone, has price 200 (sells for 100), text 14000 "A stone
  allowing instantaneous transport between two gate crystals." and sort order 0; row 32, Earth Stone, has price 70.
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id`, `row` | the loot id, `0x2000` + row, and the row |
| `name` | the shipped name |
| `sort_order`, `icon_frame` | `+0x08`, `+0x04` |
| `price`, `sell_price` | `+0x00` in gil, and half of it rounded down |
| `text_id`, `description` | `+0x02` and its shipped text |
| `explanation` | the sell price, or that a shop will not buy it, or "a Reserve row" |

## Related

- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
- [Bazaar: every bazaar good, the loot you must sell to unlock it, its price, what it gives, and how unlocking and buying work](bazaar.md)
- [Item list: every item with its name, price, sort order, icon, the action it runs and its texts](item-list.md)
