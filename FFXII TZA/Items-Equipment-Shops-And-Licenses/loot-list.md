---
title: "Loot list: every loot id with its name, price, sell price, sort order and description"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF098, 0x0031C5D0, 0x0031CBA3, 0x0031CBC1, 0x0031CBE0, 0x0031CBE7, 0x0031CBFA, 0x0031CC01, 0x0057DBC2"
---

## What it lists

[`loot-list.tsv`](loot-list.tsv) holds one line for each of the 512 rows of the loot table that registry slot `0x02EBF098` reaches
(`battle_pack.bin` directory entry `+0x84`). Row *n* is loot id `0x2000` + *n*, inventory class 7
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): the class-7 arm of `0x0031C5D0`
subtracts `0x2000` from the id and multiplies by the row size (`0x0031CBA3`-`0x0031CBBE`).

- 235 rows are named loot: rows 0, 32-245, 256-269 and 274-279.
- The other 277 rows are named Reserve, with icon frame 0.
- Two rows, 274 Sandalwood Chop and 275 Pinewood Chop, have price 0, so a shop will not buy them.

### Where the values come from

Each line is read from the `st2e` table at entry
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

### Properties of the shipped rows

- The table's header gives 512 rows of 10 bytes, one TSV line each.
- Byte `+0x05` is 0 on every row.
- Example rows: row 0, Teleport Stone, has price 200 (sells for 100), text 14000 "A stone
  allowing instantaneous transport between two gate crystals." and sort order 0; row 32, Earth Stone, has price 70.

### Where each loot comes from

`sources` joins tables already in the database by id, and reads the scripts where a table stops short. It holds one part per kind of source, the parts separated by `;`:

- `shop:` each shop that sells it, by name and number in [`shops.tsv`](shops.tsv), with the map (region) whose script gives an actor that shop (`setshopname`, the `place` column), and when the list that holds it goes on sale:
  - from the start;
  - from a story progress value, with the story point that writes it ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)), or the value alone where no script writes it, which is so for 500 (below);
  - from a clan rank, with the rank's shipped name;
  - for the Clan Provisioner's last list, from joining Clan Centurio (below).
- `bazaar:` each bazaar good that gives it, with the good's id ([`bazaar.tsv`](bazaar.tsv)).
- `treasure chest (N):` every treasure chest that can give it, N chests in all ([Treasure chests](../World-Areas-And-Travel/treasure-chests.md)). Three loot have a chest part: Teleport Stone, Braid Wool and Gysahl Greens.
  - an entry is a map (region) and zone script with the chest numbers (actor `treasure_NN`), and `(once)` for a one-time chest;
  - then the chance that an opening gives it, and in brackets the chance with the Diamond Armlet on the party leader where that differs, as `40% (Diamond Armlet 0%)`;
  - chests of one map with the same chance share an entry; whether a chest is there at all is a separate roll, its presence in the treasure chest list;
  - the 40 chests of `bts_z01`, `pre_a01` and `pre_b01` stand in zone scripts no field loads, and their entries say so.
- `steal:`, `drop:`, `poach:` and `monograph:` the monsters whose enemy definitions hold its id in those slots, read from the area files ([Bestiary](../Enemy-Spawning/bestiary.md)). No definition is left out:
  - three are placed by no map script, and each is named with its area and row, as `Dead Bones (bog_a row 3: a definition no map script places)`: Dead Bones (`bog_a` row 3), Axebeak (`enw_b` row 8) and Omega Mark XII (`gil_i` row 7), variants of monsters that other definitions place;
  - a unit whose name word reads No name is listed by its definition id, area and row, as `unnamed unit 0x0100 (nal_b row 0)`; the bestiary row's explanation gives the functions that place it.
- `scene gift (urn):`, `scene gift (talk):`, `scene gift (touch):`, `scene gift (map event):` and `scene gift (event scene):` each map (region) and script whose script gives it, with the reward package when the gift is one ([Scene rewards](../Story-Events-And-Hunts/scene-rewards.md), [Reward package list](../Rewards-EXP-Gil-And-Loot/reward-package-list.md)). The label says how the gift is handed over:
  - urn: the giving actor keeps a treasure flag (`settreasureflag`, `istreasureflag`), so it gives once;
  - talk: the gift comes from the actor's talk slot (slot 2, or a function `sysReqchg` puts in slot 2), or from a function that only such a function requests;
  - touch: the same for the touch slots 3 and 4;
  - map event: the gift comes from a function the map's script runs by itself (`main`, `init` or a function they request);
  - event scene: the gift is in an event script, named by the maps whose scripts play it;
  - of the scene-rewards gifts in a zone script that no field loads, every one is a teleport destination in `mic_b07` ([Key item list](key-item-list.md), "Where each key item comes from"); the developer scripts `evt_t*` are not scene-rewards rows ([Scene rewards](../Story-Events-And-Hunts/scene-rewards.md), "Scope") and are not joined.
- `hunt reward:` the hunt whose report gives it, with the package and the map (region) and script that report it ([Hunts](../Story-Events-And-Hunts/hunts.md), [Reward selector list](../Rewards-EXP-Gil-And-Loot/reward-selector-list.md)):
  - the script verb `questresultwindow(n)` opens the reward window for quest n and grants at once the package its selector names ([Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md));
  - the selector is `0xA000` + the text index of entry n of `questbase.bin` (`0x00344C60`, `0x00473C90`), which is n for the 45 hunts, quest ids 128-172 ([Small .bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md));
  - a package that a selector names, that no hunt report opens and that no script gives would be listed as `reward package:` with its selector; none is.

A shop list goes on sale once it or any list above it on the shop's ladder meets its condition, and the last list is always on sale ([Shops](shops.md), "Choosing a list"). The story test is the story counter at least the threshold (`0x002FADF3`-`0x002FAE0D`).

No script writes story progress 500. The values the scripts write go from 490 (After the captive Penelo) to 520 (After the floating continent), so a list that waits on 500 goes on sale at 520.

The Clan Provisioner is a Mysterious Merchant in Muthru Bazaar (Rabanastre) until bit `0x1` of script global byte `0x041D` is set; only then does its actor take the shop's name (`rbn_a02`). Montblanc sets that bit the first time the player talks to him in The Clan Hall (Rabanastre), with the message "You are now a member of Clan Centurio!" (`rbn_a14`).

Every part names every source. A cell that would be longer than 1,000 characters moves its longest parts, longest first, to [`item-sources.tsv`](item-sources.tsv) until it fits, and gives for each moved part its label, its count and the table, as `drop (28): in item-sources.tsv` for the Potion.

That table has one line per entry: `id` and `name` of the row, `part` (the label, or `used_for` and the label for a key item's use) and `entry`. A treasure chest part counts chests, and one entry can hold several. `-` means that none of these tables names a source. The starting inventory table adds nothing ([Starting inventory](../Party/starting-inventory.md)).

The five Tufts (Peach, Green, Orange, Brown and White, `0x2104`-`0x2108`) have no source, and their cells say so with `none:`. No shop list, bazaar good, treasure chest, enemy definition, reward package, hunt reward, starting inventory row or scenario set holds their ids ([Scenario presets](../Party/scenario-presets.md)), and no give call of any `us` script names them, the developer scripts `evt_t*` included.

### What it is used for

`used_in` lists the bazaar goods that need the loot sold before they are offered ([`bazaar.tsv`](bazaar.tsv), `unlocked_by_selling`), with the good's id and the count to sell.

## Columns

| Column | Meaning |
|---|---|
| `id`, `row` | the loot id, `0x2000` + row, and the row |
| `name` | the shipped name |
| `sort_order`, `icon_frame` | `+0x08`, `+0x04` |
| `price`, `sell_price` | `+0x00` in gil, and half of it rounded down |
| `text_id`, `description` | `+0x02` and its shipped text |
| `explanation` | the sell price, or that a shop will not buy it, or "a Reserve row" |
| `sources` | where the loot is obtained, one part per kind of source, with each shop's place and opening, how a scene gift is handed over and the hunt reward, the treasure chests that hold it with the odds ("Where each loot comes from" above), or for a part moved to [`item-sources.tsv`](item-sources.tsv) its count; for the five Tufts, `none:` and the sources that do not hold them; `-` for a Reserve row |
| `used_in` | the bazaar goods that need it sold, with the good's id and the count; `-` for none |

## Related

- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
- [Bazaar: every bazaar good, the loot you must sell to unlock it, its price, what it gives, and how unlocking and buying work](bazaar.md)
- [Item list: every item with its name, price, sort order, icon, the action it runs and its texts](item-list.md)
- [Treasure chests: where each chest stands, whether it appears and comes back, and what it holds with the odds of each content](../World-Areas-And-Travel/treasure-chests.md)
