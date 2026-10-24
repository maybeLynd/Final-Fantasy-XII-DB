---
title: "Key item list: every key item id with its name, sort order, icon and description"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF090, 0x02EBF088, 0x02EBF080, 0x02EBF078, 0x0031C5D0, 0x0031D1B6, 0x0031D218, 0x0031D26B, 0x0031D631, 0x0031D63E"
---

## What it lists

[`key-item-list.tsv`](key-item-list.tsv) holds one line for each of the 512 key-item ids `0x8000`-`0x81FF`, inventory class 13
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

### Where the values come from

Each line is read from one of the three `st2e` tables, and each row is decoded as the arm does. The m_daiji arm is quoted below; the g_daiji arm (`0x0031D2C5`-`0x0031D460`) and
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

### Properties of the shipped rows

- The tables' headers give 64, 32 and 416 rows of 10 bytes and s_daiji_data 0, one TSV line per row.
- Byte `+0x05` is 0 on every row.
- Example rows: id `0x8000` is row 0 of m_daiji_data, Rabanastre, icon frame 112, text 20000; id
  `0x8060` is row 0 of q_daiji_data, sort order 73, icon frame 114, text 20096, "This small bottle contains a
  message: ...".

### Where each key item comes from

`sources` joins tables already in the database by id, and reads the scripts where a table stops short. It holds one part per kind of source, the parts separated by `;`:

- `bazaar:` each bazaar good that gives it, with the good's id ([`bazaar.tsv`](bazaar.tsv)).
- `scene gift (urn):`, `scene gift (talk):`, `scene gift (touch):`, `scene gift (map event):` and `scene gift (event scene):` each map (region) and script whose script gives it, with the reward package when the gift is one ([Scene rewards](../Story-Events-And-Hunts/scene-rewards.md), [Reward package list](../Rewards-EXP-Gil-And-Loot/reward-package-list.md)). The label says how the gift is handed over:
  - urn: the giving actor keeps a treasure flag (`settreasureflag`, `istreasureflag`), so it gives once;
  - talk: the gift comes from the actor's talk slot (slot 2, or a function `sysReqchg` puts in slot 2), or from a function that only such a function requests;
  - touch: the same for the touch slots 3 and 4;
  - map event: the gift comes from a function the map's script runs by itself (`main`, `init` or a function they request);
  - event scene: the gift is in an event script, named by the maps whose scripts play it;
  - gifts in scripts that no map loads are left out.
- `seller:` the map (region) and script of each map seller who sells it, with the price ([Price list](../Rewards-EXP-Gil-And-Loot/price-list.md)). The seller's talk keeps the maps and their prices in two lists, offers the maps the player does not hold, takes the price and gives the chosen map; [Scene rewards](../Story-Events-And-Hunts/scene-rewards.md) lists that gift with its item chosen at run time.
- `first join:` the members whose first join adds it, with the count when it is above 1 ([Party table](../Party/party-table.md)).

A part that names more than 10 places gives its count, the first ones and the table that holds the rest. `-` means that none of these tables names a source. The joined tables do not include treasure chest contents.

### Rows that are not items

`kind` tells the key items from the other named rows:

- `map`: a named row of m_daiji_data, ids `0x8000`-`0x803F`: the area maps, with five Candles among them (Garamsythe, Barheim, Lhusu, Henne and Feywood).
- `teleport destination`: a named row of g_daiji_data, ids `0x8040`-`0x805F`: the key item a gate crystal gives and its teleport list names ([Shared zone-script actors](../Story-Events-And-Hunts/shared-zone-script-actors.md)). Zertinan Caverns and The Feywood are in the table, but no script gives them.
- `status word`: q_daiji rows 13-15, "Available", "Accepted" and "Complete!".
- `key item`: every other named row, and `Reserve` for the Reserve rows.

### What each key item is for

`used_for` lists what takes, tests or reads each key item, one part per kind of use, the parts separated by `;`:

- `map screens:` for an area map, the area whose points and locations the map screens show once the map is owned. `menumap_area.bin` lists one map key item per persistence group, and `0x002543F0` answers whether it is owned ([Map screens](../Menus-And-HUD/map-screens.md), "What is shown"; [Menu map files](../Game-Files-And-Data-Tables/menu-map-files.md)).
- `taken:` each map (region) and script whose script takes it from the player (`subitem`, [Scene rewards](../Story-Events-And-Hunts/scene-rewards.md)).
- `trophy trade:` for the 30 trophies, the three hunters at the Hunters' Camp who take them, and whose counts open the Outfitters' sales ([Equipment list](equipment-list.md), "Where each piece of equipment comes from").
- `tested:` each map (region) and script whose script tests whether the player holds it (`haveitem`, with the id written in the script or stored in a variable by the same function), and what the test decides:
  - that is what the block the test controls does, or the blocks of the conditions that read the stored result;
  - the outcomes named are a map jump, an event scene, taking an item, a gift, a quest step, story progress, a party member, gil, a map exit, the map's passable floors and walls, whether an actor is shown, whether an actor answers the player, and dialogue;
  - "other script steps" means the block does none of these;
  - the map sellers' and trophy hunters' tests of their own lists are left out, since they are the sale and the trade.
- `teleport:` for a teleport destination, the number of map scripts whose gate crystal tests it to build its teleport list ([Shared zone-script actors](../Story-Events-And-Hunts/shared-zone-script-actors.md)).
- `monograph:` for a monograph or the Canopic Jar, the monsters whose monograph slot needs it ([Bestiary](../Enemy-Spawning/bestiary.md)).

A `taken:` or `tested:` part that names more than 10 places gives its count and the first ones. `not yet located` marks a key item for which none of these is found: the five Candles, the teleport destinations Zertinan Caverns and The Feywood, Writ of Transit, Crescent Stone, Rusted Scrap of Armor, Treaty-Blade, Dusty Letter, Time-worn Necklace and Windvane. The status words read `not an item: a status word`, and the Reserve rows `-`.

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
| `kind` | map, teleport destination, status word, key item or Reserve ("Rows that are not items" above) |
| `sources` | where the key item is obtained, one part per kind of source, with how a scene gift is handed over and the map sellers ("Where each key item comes from" above); `-` for none |
| `used_for` | what takes, tests or reads the key item, one part per kind of use ("What each key item is for" above); `not yet located` when none is found |

## Related

- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
- [Loot list: every loot id with its name, price, sell price, sort order and description](loot-list.md)
- [Item list: every item with its name, price, sort order, icon, the action it runs and its texts](item-list.md)
