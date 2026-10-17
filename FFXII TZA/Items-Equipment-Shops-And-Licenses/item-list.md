---
title: "Item list: every item with its name, price, sort order, icon, the action it runs and its texts"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "02EBF100, 0031C5D0, 0031C7F5, 0031C81A, 0031C83E, 0031C845, 002CFFE0, 0057DAD0"
---

## What it lists

`item-list.tsv` holds one line for each of the 64 rows of the item table that registry slot `02EBF100` reaches
(`battle_pack.bin` directory entry `+4C`<sub>h</sub>). Row *n* is item id *n*, `0000`<sub>h</sub>-`003F`<sub>h</sub>: the class-5 arm of
`0031C5D0` multiplies the id by the table's row size (`0031C7E1`-`0031C7F3`).

- 51 rows are usable items. Each row's `+07`<sub>h</sub> is its action row, and that row is the one whose kind `+1E`<sub>h</sub> is 3
  and whose `+22`<sub>h</sub> is the item id, the rule on [Using an item](item-use.md): action rows 82-110 and 124-145.
- Rows 29-41 (ids `001D`<sub>h</sub>-`0029`<sub>h</sub>) are named Reserve. Their `+07`<sub>h</sub> points at action rows 111-123, which have kind
  255, so they are not item actions; their sort order is 255 and their price is 2.

### How it is built

`Database/Tools/catalogues/items.py` reads the `us` `battle_pack.bin`:

1. the `st2e` table at entry `+4C`<sub>h</sub>: 64 rows of 12 bytes from the section's `+20`<sub>h</sub>;
2. the name word `+08`<sub>h</sub> through the word banks at entry `+F8`<sub>h</sub>, bank `word >> 11` and row `word & 7FFh`, as
   `0031C5D0` reads it (`0031C7F5`-`0031C803`);
3. the action row `+07`<sub>h</sub> at entry `+3C`<sub>h</sub>, decoded as on
   [Action list](../Battle-Actions/action-list.md), with the help and description lines through the text groups;
4. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

The row layout:

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | sortOrder | copied to query record `+30`<sub>h</sub> (`0031C845`); Auto-sort `002CFFE0` orders items by it, then by id ([Dialogs](../Menus-And-HUD/dialogs.md)) |
| `01`<sub>h</sub> | `u8[3]` | | 0 on every row |
| `04`<sub>h</sub> | `u8` | iconFrame | copied to query record `+2C`<sub>h</sub> (`0031C83E`); the list-row filler `0057DAD0` puts it at row `+0A`<sub>h</sub>, the icon frame the row painters draw (Inventory screen, [Shop screens](../Menus-And-HUD/shop-screens.md)) |
| `05`<sub>h</sub> | `u8[2]` | | 0 on every row |
| `07`<sub>h</sub> | `u8` | actionRow | the item's action row, `52`<sub>h</sub> plus the row number on every row; copied to query record `+38`<sub>h</sub> (`0031C821`), where the magick and technick arms put their own action row `+02`<sub>h</sub> |
| `08`<sub>h</sub> | `u16` | nameWord | the name (`0031C7F5`) |
| `0A`<sub>h</sub> | `u16` | price | buy price in gil, query record `+28`<sub>h</sub> (`0031C81A`); a shop sells for half, rounded down ([Shop screens](../Menus-And-HUD/shop-screens.md), `0057DBC2`) |

### Checks

- The table's header gives 64 rows of 12 bytes, and the TSV has 64 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts the zero bytes `+01`<sub>h</sub>-`+03`<sub>h</sub> and `+05`<sub>h</sub>-`+06`<sub>h</sub>, `+07`<sub>h</sub> = `52`<sub>h</sub> + row on every row, that
  no item id is named by two item actions, that each usable item's `+07`<sub>h</sub> is its kind-3 action, and that the Reserve
  rows' action rows are not kind 3.
- Rows compared with their readers: row 0, Potion, has price 60 at `+0A`<sub>h</sub> (the record `+28`<sub>h</sub> that `0031C81A`
  writes), sort order 0 and icon frame 37, and action row 82 spends it ("Restore a small amount of HP to one ally.");
  row 6, Phoenix Down, has sort order 8, price 200, and action row 88, which removes KO.
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the item id (the row) and its shipped name |
| `sort_order` | `+00`<sub>h</sub>, the Auto-sort key |
| `icon_frame` | `+04`<sub>h</sub>, the icon frame of its list rows |
| `action_row` | `+07`<sub>h</sub>, the item's action row |
| `price`, `sell_price` | `+0A`<sub>h</sub> in gil, and half of it rounded down |
| `action` | the action row that spends the item: `action_row` when that row is an item action, else empty |
| `power`, `hit` | the action's `+10`<sub>h</sub> and `+12`<sub>h</sub> |
| `element` | the action's element `+13`<sub>h</sub> |
| `statuses`, `status_effect` | the action's status bits `+18`<sub>h</sub>, and whether it adds or removes them (`+36`<sub>h</sub> bits 0 and 1) |
| `area_radius` | the action's `+06`<sub>h</sub>; 0 = the target alone |
| `flag_names`, `flag2_names` | the action's `+0C`<sub>h</sub> and `+2C`<sub>h</sub> bits with a named effect |
| `help`, `description` | the action's shipped help and description lines |
| `explanation` | a one-line summary built from the row and its action |

## Related

- [Using an item: how a Potion is an action that costs an item, when the item is taken, given back or kept, and why enemies never spend items](item-use.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
