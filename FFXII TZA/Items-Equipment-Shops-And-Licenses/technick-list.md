---
title: "Technick list: every technick with its name, shop price, sort order, power, statuses and texts"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF0E8, 0x0031C5D0, 0x0031CEEB, 0x0031CF08, 0x00306340, 0x00323EC0, 0x002F8FA0"
---

## What it lists

[`technick-list.tsv`](technick-list.tsv) holds one line for each of the 24 rows of the technick table that registry slot `0x02EBF0E8`
reaches (`battle_pack.bin` directory entry `+0x7C`). Row *n* is technick id `0x4000` + *n*: the class-9 arm of
`0x0031C5D0` subtracts `0x4000` from the id and multiplies by the row size (`0x0031CEB3`-`0x0031CEC8`).

Every row's `+0x02` is its action row, rows 158-181 of the action table, and each of those has kind 2 and `+0x22`
equal to the technick id.

### Where the values come from

Each line is read from the `st2e` table at entry `+0x7C`, as [Magick list](magick-list.md) reads its table; the rows
have the magick table's layout, as the class-9 arm copies them (`0x0031CEEB`-`0x0031CF08`):

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

### Properties of the shipped rows

- The table's header gives 24 rows of 8 bytes, one TSV line each.
- Byte `+0x07` is 0 on every row, and every row's action row has `+0x22` = `0x4000` + row.
- Example rows: row 0, First Aid, has price 600 and action row 158; row 11, Steal, has price
  1200, sort order 0 and action row 169, the Steal row of [Action list](../Battle-Actions/action-list.md).

### Where each technick comes from

`sources` joins tables already in the database by id, and reads the scripts where a table stops short. It holds one part per kind of source, the parts separated by `;`:

- `shop:` each shop that sells it, by name and number in [`shops.tsv`](shops.tsv), with the map (region) whose script gives an actor that shop (`setshopname`, the `place` column), and when the list that holds it goes on sale:
  - from the start;
  - from a story progress value, with the story point that writes it ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)), or the value alone where no script writes it, which is so for 500 (below);
  - from a clan rank, with the rank's shipped name;
  - for the Clan Provisioner's last list, from joining Clan Centurio (below).
- `treasure chest (N):` every treasure chest that can give it, N chests in all ([Treasure chests](../World-Areas-And-Travel/treasure-chests.md)). 23 technicks have a chest part, 16 of them no other source.
  - an entry is a map (region) and zone script with the chest numbers (actor `treasure_NN`), and `(once)` for a one-time chest;
  - then the chance that an opening gives it, and in brackets the chance with the Diamond Armlet on the party leader where that differs, as `40% (Diamond Armlet 0%)`;
  - chests of one map with the same chance share an entry; whether a chest is there at all is a separate roll, its presence in the treasure chest list;
  - the 40 chests of `bts_z01`, `pre_a01` and `pre_b01` stand in zone scripts no field loads, and their entries say so.
- `first join:` the members whose first join adds it, with the count when it is above 1 ([Party table](../Party/party-table.md)).

A shop list goes on sale once it or any list above it on the shop's ladder meets its condition, and the last list is always on sale ([Shops](shops.md), "Choosing a list"). The story test is the story counter at least the threshold (`0x002FADF3`-`0x002FAE0D`).

No script writes story progress 500. The values the scripts write go from 490 (After the captive Penelo) to 520 (After the floating continent), so a list that waits on 500 goes on sale at 520.

The Clan Provisioner is a Mysterious Merchant in Muthru Bazaar (Rabanastre) until bit 0 of script global byte `0x041D` is set; only then does its actor take the shop's name (`rbn_a02`). Montblanc sets that bit the first time the player talks to him in The Clan Hall (Rabanastre), with the message "You are now a member of Clan Centurio!" (`rbn_a14`).

Every part names every source. A cell that would be longer than 1,000 characters moves its longest parts, longest first, to [`item-sources.tsv`](item-sources.tsv) until it fits, and gives for each moved part its label, its count and the table, as `drop (28): in item-sources.tsv` for the Potion.

That table has one line per entry: `id` and `name` of the row, `part` (the label, or `used_for` and the label for a key item's use) and `entry`. A treasure chest part counts chests, and one entry can hold several. `-` means that none of these tables names a source.

### The licence it needs

`licence` names the licence squares whose node lists the technick's action row (`action`) among its grants ([`license-list.tsv`](license-list.tsv), `grant_ids`), by name and node. Owning any one of them lets a character use it: `0x00323EC0` tests an action through the node mask that `0x002F8FA0` builds ([Licenses](licenses.md), "The test").

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
| `sources` | where the technick is obtained, one part per kind of source, with each shop's place and opening, clan ranks by name, the treasure chests that hold it with the odds ("Where each technick comes from" above), or for a part moved to [`item-sources.tsv`](item-sources.tsv) its count; `-` for none |
| `licence` | the licence squares that grant it, by name and node ("The licence it needs" above); every technick names at least one, since the action bypass bit (bit 13 of the action row's second flag word, `0x00323F52`) is clear on all 24 technick actions |

## Related

- [Magick list: every magick with its name, school, shop price, sort order, MP cost, power, element, statuses and texts](magick-list.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
- [Treasure chests: where each chest stands, whether it appears and comes back, and what it holds with the odds of each content](../World-Areas-And-Travel/treasure-chests.md)
