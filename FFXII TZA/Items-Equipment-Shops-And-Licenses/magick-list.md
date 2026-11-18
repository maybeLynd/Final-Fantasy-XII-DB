[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Magick list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Magick list: every magick with its name, school, shop price, sort order, MP cost, power, element, statuses and texts | reference | Items, equipment, shops and licenses | Magicks and technicks | All 81 rows of the shipped magick table in battle_pack.bin, decoded field by field: the magick id and name, the sort order, the icon frame, the shop price and the action row, and from that action row the school with its shipped name, the MP cost, charge base, power, hit, element, statuses, range, area, named flags, help and description lines, and a one-line explanation. | 0x02EBF0F0, 0x0031C5D0, 0x0031CD4C, 0x0031CD69, 0x0031CDBE, 0x0031CDC5, 0x02EBF110, 0x00306340, 0x00323EC0, 0x002F8FA0 |

## What it lists

[`magick-list.tsv`](magick-list.tsv) holds one line for each of the 81 rows of the magick table that registry slot `0x02EBF0F0` reaches
(`battle_pack.bin` directory entry `+0x78`). Row *n* is magick id `0x3000` + *n*: the class-8 arm of `0x0031C5D0`
subtracts `0x3000` from the id and multiplies by the row size (`0x0031CD0D`-`0x0031CD28`).

Every row's `+0x02` is its action row, rows 0-80 of the action table, and each of those has kind 1 and `+0x22` equal
to the magick id. By school there are 25 White, 25 Black, 20 Time, 6 Green and 5 Arcane magicks.

A magick row holds only its shop price, name, icon and sort order; what the spell does, its MP cost and its school
come from the action row it points to. A member can use the magick only when it is owned and the member holds a
licence square that grants it.

### Where the values come from

Each line is read from the shipped files in these steps, with the action fields as on
[Action list](../Battle-Actions/action-list.md):

1. the `st2e` table at entry `+0x78`: 81 rows of 8 bytes from the section's `+0x20`;
2. the name word `+0x04` through the word banks at entry `+0xF8` (`0x0031CD2B`-`0x0031CD39`);
3. the action row `+0x02` at entry `+0x3C`, with its help and description lines through the text groups;
4. the school: the action row's `+0x2C & 7`, which the arm stores at query record `+0x3C` (`0x0031CDBE`-`0x0031CDC5`),
   named by the row of the same number in the magick-school table (entry `+0x30`, registry slot `0x02EBF110`). That
   table's five rows hold a help text id `+0x00` and a name word `+0x02`, which `0x0031C5D0`'s class-24 arm reads
   (`0x0031DDCF`-`0x0031DE9C`). School *n* takes the name of row *n*;
5. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

The row layout, as the class-8 arm copies it (`0x0031CD4C`-`0x0031CD69`):

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | price | shop price in gil, query record `+0x28` (`0x0031CD50`) |
| `+0x02` | `u8` | actionRow | the magick's action row, query record `+0x38` (`0x0031CD65`); `0x00306340` hands it to `0x003064F0`, the test of whether a member may use the magick: the ownership test `0x003060E0` and the test of whether the member holds the magick's license, `0x00323EC0`, must both pass (`0x0030651F`, `0x00306535`) ([Party marks](../Menus-And-HUD/party-marks.md)) |
| `+0x03` | `u8` | iconFrame | query record `+0x2C` (`0x0031CD57`), the icon frame of its list rows |
| `+0x04` | `u16` | nameWord | the name |
| `+0x06` | `u8` | sortOrder | query record `+0x30` (`0x0031CD5E`), the key Auto-sort `0x002CFFE0` orders by ([Dialogs](../Menus-And-HUD/dialogs.md)) |
| `+0x07` | `u8` | | 0 on every row |

### Properties of the shipped rows

- The table's header gives 81 rows of 8 bytes, one TSV line each.
- Byte `+0x07` is 0 on every row, and every row's action row has `+0x22` = `0x3000` + row.
- Example rows: row 0, Cure, has price 200, action row 0 (8 MP, power 20), school 0, "White
  Magicks"; row 79, Gravity, has price 2300, action row 79 and school 2, "Time Magicks".

### Where each magick comes from

`sources` joins tables already in the database by id, and reads the scripts where a table stops short. It holds one part per kind of source, the parts separated by `;`:

- `shop:` each shop that sells it, by name and number in [`shops.tsv`](shops.tsv), with the map (region) whose script gives an actor that shop (`setshopname`, the `place` column), and when the list that holds it goes on sale:
  - from the start;
  - from a story progress value, with the story point that writes it ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)), or, where no story script writes the value, with the first written value that meets it, which is so for 500: "from story progress 500 (met from 520, After the floating continent)" (below);
  - from a clan rank, with the rank's shipped name;
  - for the Clan Provisioner's last list, from joining Clan Centurio (below).
- `treasure chest (N):` every treasure chest that can give it, N chests in all ([Treasure chests](../World-Areas-And-Travel/treasure-chests.md)). 62 magicks have a chest part, 31 of them no other source.
  - an entry is a map (region) and zone script with the chest numbers (actor `treasure_NN`), and `(once)` for a one-time chest;
  - then the chance that an opening gives it, and in brackets the chance with the Diamond Armlet on the party leader where that differs, as `40% (Diamond Armlet 0%)`;
  - chests of one map with the same chance share an entry; whether a chest is there at all is a separate roll, its presence in the treasure chest list;
  - the 40 chests of `bts_z01`, `pre_a01` and `pre_b01` stand in zone scripts no field loads, and their entries say so.
- `first join:` the members whose first join adds it, with the count when it is above 1 ([Party table](../Party/party-table.md)).

A shop list goes on sale once it or any list above it on the shop's ladder meets its condition, and the last list is always on sale ([Shops](shops.md), "Choosing a list"). The story test is the story counter at least the threshold (`0x002FADF3`-`0x002FAE0D`).

No script writes story progress 500. The values the scripts write go from 490 (After the captive Penelo) to 520 (After the floating continent), so a list that waits on 500 goes on sale at 520.

The Clan Provisioner is a Mysterious Merchant in Muthru Bazaar (Rabanastre) until bit `0x1` of script global byte `0x041D` is set; only then does its actor take the shop's name (`rbn_a02`). Montblanc sets that bit the first time the player talks to him in The Clan Hall (Rabanastre), with the message "You are now a member of Clan Centurio!" (`rbn_a14`).

Every part names every source. A cell that would be longer than 1,000 characters moves its longest parts, longest first, to [`item-sources.tsv`](item-sources.tsv) until it fits, and gives for each moved part its label, its count and the table, as `drop (28): in item-sources.tsv` for the Potion.

That table has one line per entry: `id` and `name` of the row, `part` (the label, or `used_for` and the label for a key item's use) and `entry`. A treasure chest part counts chests, and one entry can hold several. `-` means that none of these tables names a source.

### The licence it needs

`licence` names the licence squares whose node lists the magick's action row (`action`) among its grants ([`license-list.tsv`](license-list.tsv), `grant_ids`), by name and node. Owning any one of them lets a character use it: `0x00323EC0` tests an action through the node mask that `0x002F8FA0` builds ([Licenses](licenses.md), "The test").

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the magick id and its shipped name |
| `sort_order`, `icon_frame`, `price` | `+0x06`, `+0x03`, `+0x00` |
| `action`, `kind_name` | `+0x02`, the action row, and that row's kind |
| `school`, `school_name` | the action row's `+0x2C & 7` and the school's shipped name |
| `cost`, `charge_base`, `power`, `hit` | the action's MP cost `+0x0A`, `+0x09`, `+0x10`, `+0x12` |
| `element` | the action's element `+0x13` |
| `statuses`, `status_effect` | the action's status bits `+0x18`, and whether it adds or removes them (`+0x36` bits `0x1` and `0x2`) |
| `range_near_tenths`, `reach_tenths`, `area_radius` | the action's `+0x02`, `+0x05`, `+0x06` |
| `flag_names`, `flag2_names` | the action's `+0x0C` and `+0x2C` bits with a named effect |
| `help`, `description` | the action's shipped help and description lines |
| `explanation` | a one-line summary built from the row and its action |
| `sources` | where the magick is obtained, one part per kind of source, with each shop's place and opening, clan ranks by name, the treasure chests that hold it with the odds ("Where each magick comes from" above), or for a part moved to [`item-sources.tsv`](item-sources.tsv) its count; `-` when it has no source |
| `licence` | the licence squares that grant it, by name and node ("The licence it needs" above); every magick names at least one, since the action bypass bit (bit `0x2000` of the action row's second flag word, `0x00323F52`) is clear on all 81 magick actions |

## Related

- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
- [Technick list: every technick with its name, shop price, sort order, power, statuses and texts](technick-list.md)
- [Item list: every item with its name, price, sort order, icon, the action it runs and its texts](item-list.md)
- [Treasure chests: where each chest stands, whether it appears and comes back, and what it holds with the odds of each content](../World-Areas-And-Travel/treasure-chests.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat formula: `0x003060E0` calls `0x0031B860`; `0x003064F0` calls `0x00320A40`; those functions are documented on
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
