---
title: "Item list: every item with its name, price, sort order, icon, the action it runs and its texts"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF100, 0x0031C5D0, 0x0031C7F5, 0x0031C81A, 0x0031C83E, 0x0031C845, 0x002CFFE0, 0x0057DAD0"
---

## What it lists

`item-list.tsv` holds one line for each of the 64 rows of the item table that registry slot `0x02EBF100` reaches
(`battle_pack.bin` directory entry `+0x4C`). Row *n* is item id *n*, `0x0000`-`0x003F`: the class-5 arm of
`0x0031C5D0` multiplies the id by the table's row size (`0x0031C7E1`-`0x0031C7F3`).

- 51 rows are usable items. Each row's `+0x07` is its action row, and that row is the one whose kind `+0x1E` is 3
  and whose `+0x22` is the item id, the rule on [Using an item](item-use.md): action rows 82-110 and 124-145.
- Rows 29-41 (ids `0x001D`-`0x0029`) are named Reserve. Their `+0x07` points at action rows 111-123, which have kind
  255, so they are not item actions; their sort order is 255 and their price is 2.

### How it is built

`Database/Tools/catalogues/items.py` reads the `us` `battle_pack.bin`:

1. the `st2e` table at entry `+0x4C`: 64 rows of 12 bytes from the section's `+0x20`;
2. the name word `+0x08` through the word banks at entry `+0xF8`, bank `word >> 11` and row `word & 0x7FF`, as
   `0x0031C5D0` reads it (`0x0031C7F5`-`0x0031C803`);
3. the action row `+0x07` at entry `+0x3C`, decoded as on
   [Action list](../Battle-Actions/action-list.md), with the help and description lines through the text groups;
4. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

The row layout:

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | sortOrder | copied to query record `+0x30` (`0x0031C845`); Auto-sort `0x002CFFE0` orders items by it, then by id ([Dialogs](../Menus-And-HUD/dialogs.md)) |
| `+0x01` | `u8[3]` | | 0 on every row |
| `+0x04` | `u8` | iconFrame | copied to query record `+0x2C` (`0x0031C83E`); the list-row filler `0x0057DAD0` puts it at row `+0x0A`, the icon frame the row painters draw ([Inventory screen](../Menus-And-HUD/inventory-screen.md), [Shop screens](../Menus-And-HUD/shop-screens.md)) |
| `+0x05` | `u8[2]` | | 0 on every row |
| `+0x07` | `u8` | actionRow | the item's action row, `0x52` plus the row number on every row; copied to query record `+0x38` (`0x0031C821`), where the magick and technick arms put their own action row `+0x02` |
| `+0x08` | `u16` | nameWord | the name (`0x0031C7F5`) |
| `+0x0A` | `u16` | price | buy price in gil, query record `+0x28` (`0x0031C81A`); a shop sells for half, rounded down ([Shop screens](../Menus-And-HUD/shop-screens.md), `0x0057DBC2`) |

### Checks

- The table's header gives 64 rows of 12 bytes, and the TSV has 64 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts the zero bytes `+0x01`-`+0x03` and `+0x05`-`+0x06`, `+0x07` = `0x52` + row on every row, that
  no item id is named by two item actions, that each usable item's `+0x07` is its kind-3 action, and that the Reserve
  rows' action rows are not kind 3.
- Rows compared with their readers: row 0, Potion, has price 60 at `+0x0A` (the record `+0x28` that `0x0031C81A`
  writes), sort order 0 and icon frame 37, and action row 82 spends it ("Restore a small amount of HP to one ally.");
  row 6, Phoenix Down, has sort order 8, price 200, and action row 88, which removes KO.
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the item id (the row) and its shipped name |
| `sort_order` | `+0x00`, the Auto-sort key |
| `icon_frame` | `+0x04`, the icon frame of its list rows |
| `action_row` | `+0x07`, the item's action row |
| `price`, `sell_price` | `+0x0A` in gil, and half of it rounded down |
| `action` | the action row that spends the item: `action_row` when that row is an item action, else empty |
| `power`, `hit` | the action's `+0x10` and `+0x12` |
| `element` | the action's element `+0x13` |
| `statuses`, `status_effect` | the action's status bits `+0x18`, and whether it adds or removes them (`+0x36` bits 0 and 1) |
| `area_radius` | the action's `+0x06`; 0 = the target alone |
| `flag_names`, `flag2_names` | the action's `+0x0C` and `+0x2C` bits with a named effect |
| `help`, `description` | the action's shipped help and description lines |
| `explanation` | a one-line summary built from the row and its action |

## Related

- [Using an item: how a Potion is an action that costs an item, when the item is taken, given back or kept, and why enemies never spend items](item-use.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
