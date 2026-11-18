[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Item list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Item list: every item with its name, price, sort order, icon, the action it runs and its texts | reference | Items, equipment, shops and licenses | Items and inventory | All 64 rows of the shipped item table in battle_pack.bin, decoded field by field: the item id and name, the Auto-sort order, the icon frame, the buy and sell price, and for the 51 usable items the action row that spends the item, with its power, hit, element, statuses, area, named flags, help and description lines, and a one-line explanation. | 0x02EBF100, 0x0031C5D0, 0x0031C7F5, 0x0031C81A, 0x0031C83E, 0x0031C845, 0x002CFFE0, 0x0057DAD0 |

## What it lists

[`item-list.tsv`](item-list.tsv) holds one line for each of the 64 rows of the item table that registry slot `0x02EBF100` reaches
(`battle_pack.bin` directory entry `+0x4C`). Row *n* is item id *n*, `0x0000`-`0x003F`: the class-5 arm of
`0x0031C5D0` multiplies the id by the table's row size¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031C7E1`-`0x0031C7F3` |

</details>

An item row holds only the item's name, price, sort order and icon. What the item does when used comes from the action
row it points to in the action table, and that action is what takes the item from the inventory.

- 51 rows are usable items. Each row's `+0x07` is its action row, and that row is the one whose kind `+0x1E` is 3
  and whose `+0x22` is the item id, the rule on [Using an item](item-use.md): action rows 82-110 and 124-145.
- Rows 29-41 (ids `0x001D`-`0x0029`) are named Reserve. Their `+0x07` points at action rows 111-123, which have kind
  255, so they are not item actions; their sort order is 255 and their price is 2.

### Where the values come from

Each line is read from the shipped `us` `battle_pack.bin` in these steps:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | the `st2e` table at entry `+0x4C`: 64 rows of 12 bytes from the section's `+0x20`; |   |
| 2 | the name word `+0x08` through the word banks at entry `+0xF8`, bank `word >> 11` and row `word & 0x7FF`, as `0x0031C5D0` reads it; | `0x0031C7F5`-`0x0031C803` |
| 3 | the action row `+0x07` at entry `+0x3C`, decoded as on [Action list](../Battle-Actions/action-list.md), with the help and description lines through the text groups; |   |
| 4 | every one-byte text code through the glyph table of the shipped `us` font `font00.dat` ([Fonts](../Menus-And-HUD/fonts.md)). |   |

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

### Properties of the shipped rows

- The table's header gives 64 rows of 12 bytes, one TSV line each.
- Bytes `+0x01`-`+0x03` and `+0x05`-`+0x06` are 0 and `+0x07` is `0x52` + row on every row. No item id is named by
  two item actions, each usable item's `+0x07` is its kind-3 action, and the Reserve rows' action rows are not kind 3.
- Example rows: row 0, Potion, has price 60 at `+0x0A` (the record `+0x28` that `0x0031C81A`
  writes), sort order 0 and icon frame 37, and action row 82 spends it ("Restore a small amount of HP to one ally.");
  row 6, Phoenix Down, has sort order 8, price 200, and action row 88, which removes KO.

### Where each item comes from

`sources` joins tables already in the database by id, and reads the scripts where a table stops short. It holds one part per kind of source, the parts separated by `;`:

- `shop:` each shop that sells it, by name and number in [`shops.tsv`](shops.tsv), with the map (region) whose script gives an actor that shop (`setshopname`, the `place` column), and when the list that holds it goes on sale:
  - from the start;
  - from a story progress value, with the story point that writes it ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)), or, where no story script writes the value, with the first written value that meets it, which is so for 500: "from story progress 500 (met from 520, After the floating continent)" (below);
  - from a clan rank, with the rank's shipped name;
  - for the Clan Provisioner's last list, from joining Clan Centurio (below).
- `bazaar:` each bazaar good that gives it, with the good's id ([`bazaar.tsv`](bazaar.tsv)).
- `treasure chest (N):` every treasure chest that can give it, N chests in all ([Treasure chests](../World-Areas-And-Travel/treasure-chests.md)). 51 items have a chest part.
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
  - the selector is `0xA000` + the text index of entry n of `questbase.bin`¹, which is n for the 45 hunts, quest ids 128-172 ([Small .bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md));
  - a package that a selector names, that no hunt report opens and that no script gives would be listed as `reward package:` with its selector; no package is.
- `first join:` the members whose first join adds it, with the count when it is above 1 ([Party table](../Party/party-table.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00344C60`, `0x00473C90` |

</details>

A shop list goes on sale once it or any list above it on the shop's ladder meets its condition, and the last list is always on sale ([Shops](shops.md), "Choosing a list"). The story test is the story counter at least the threshold¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FADF3`-`0x002FAE0D` |

</details>

No script writes story progress 500. The values the scripts write go from 490 (After the captive Penelo) to 520 (After the floating continent), so a list that waits on 500 goes on sale at 520.

The Clan Provisioner is a Mysterious Merchant in Muthru Bazaar (Rabanastre) until bit `0x1` of script global byte `0x041D` is set; only then does its actor take the shop's name (`rbn_a02`). Montblanc sets that bit the first time the player talks to him in The Clan Hall (Rabanastre), with the message "You are now a member of Clan Centurio!" (`rbn_a14`).

Every part names every source. A cell that would be longer than 1,000 characters moves its longest parts, longest first, to [`item-sources.tsv`](item-sources.tsv) until it fits, and gives for each moved part its label, its count and the table, as `drop (28): in item-sources.tsv` for the Potion.

That table has one line per entry: `id` and `name` of the row, `part` (the label, or `used_for` and the label for a key item's use) and `entry`. A treasure chest part counts chests, and one entry can hold several. `-` means that none of these tables names a source. The starting inventory table adds nothing ([Starting inventory](../Party/starting-inventory.md)).

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
| `statuses`, `status_effect` | the action's status bits `+0x18`, and whether it adds or removes them (`+0x36` bits `0x1` and `0x2`) |
| `area_radius` | the action's `+0x06`; 0 = the target alone |
| `flag_names`, `flag2_names` | the action's `+0x0C` and `+0x2C` bits with a named effect |
| `help`, `description` | the action's shipped help and description lines |
| `explanation` | a one-line summary built from the row and its action |
| `sources` | where the item is obtained, one part per kind of source, with each shop's place and opening, how a scene gift is handed over and the hunt reward, the treasure chests that hold it with the odds ("Where each item comes from" above), or for a part moved to [`item-sources.tsv`](item-sources.tsv) its count; `-` when the item has no source |

## Related

- [Using an item: how a Potion is an action that costs an item, when the item is taken, given back or kept, and why enemies never spend items](item-use.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
- [Treasure chests: where each chest stands, whether it appears and comes back, and what it holds with the odds of each content](../World-Areas-And-Travel/treasure-chests.md)

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 48 calls with 13 other topics</summary>

**Characters and objects** (explained on [party control modes](../Engine-Core/party-control-modes.md), [frame update order](../Engine-Core/frame-update-order.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [ko and game over](../Status-Effects-And-KO/ko-and-game-over.md), [battle units](../Characters-And-Objects/battle-units.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A3B0`](item-list.md) | calls | [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction)<br>[`0x0031B760`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning) |
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x00236A60`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: reset state for reuse (on battle unit construction)<br>[`0x00322050`](../Characters-And-Objects/battle-unit-construction.md) (on battle unit construction) |
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | is called by | [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) | calls | [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction)<br>[`0x0025AB30`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x002697E0`](../Graphics/effect-file-loading.md) (on effect file loading)<br>[`0x00300FC0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00322050`](../Characters-And-Objects/battle-unit-construction.md) (on battle unit construction) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) | is called by | [`0x00233EA0`](../Characters-And-Objects/battle-units.md) (on battle units)<br>[`0x00233F70`](../Enemy-Spawning/enemy-respawning.md) Battle unit: update lifecycle and combat frame (on enemy respawning)<br>[`0x002348E0`](../Enemy-AI-And-Gambits/enmity.md) (on enmity)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) | calls | [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction)<br>[`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse)<br>[`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) |
| [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) | is called by | [`0x00233CF0`](../Engine-Core/party-control-modes.md) (on party control modes) |
| [`0x00510160`](item-list.md) | calls | [`0x00237650`](../Characters-And-Objects/actor-model-rebuild.md) Actor work: has applied unit definition (on actor model rebuild) |

**Battle actions** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) | calls | [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action (on equipping an item) |
| [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) | calls | [`0x003105D0`](equipping-an-item.md) Battle unit: cancel and reset current action (on equipping an item) |

**Damage and battle formulas** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x0023AC80`](equipment.md) Battle stats: initialize definition record (on equipment) |

**Movement and pathfinding** (explained on [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) | calls | [`0x00311E20`](../Engine-Core/party-control-modes.md) (on party control modes) |

**Party** (explained on [debug menu](../Engine-Core/debug-menu.md), [party control modes](../Engine-Core/party-control-modes.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) | calls | [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list)<br>[`0x00326500`](../Party/party-leader.md) Party focus: select and request default actor (on party leader)<br>[`0x003272F0`](../Party/party-leader.md) (on party leader) |
| [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) | is called by | [`0x003261D0`](../Party/party-members.md) Party configuration: reconcile roster from current selectors (on party members)<br>[`0x003273D0`](../Party/party-members.md) Party configuration: set selectors and reconcile roster (on party members) |

**Graphics** (explained on [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) | calls | [`0x003125E0`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: compute presentation suppression mask (on ko and game over) |

**Scripts and script commands** (explained on [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [force fight mode](../Engine-Core/force-fight-mode.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A3B0`](item-list.md) | is called by | [`0x00510160`](item-list.md) |
| [`0x00344C60`](equipment-list.md) (on equipment list) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00473C90`](equipment-list.md) (on equipment list) | is called by | [`0x00344C60`](equipment-list.md) (on equipment list) |
| [`0x00510160`](item-list.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0037CF50`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) |

**Enemy spawning** (explained on [battle units](../Characters-And-Objects/battle-units.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [enemy respawning](../Enemy-Spawning/enemy-respawning.md), [frame update order](../Engine-Core/frame-update-order.md), [boss fights](../Battle-Actions/boss-fights.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A3B0`](item-list.md) | calls | [`0x002355A0`](../Enemy-Spawning/enemy-spawning.md) Spawn: prepare random candidate for current entry (on enemy spawning) |
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x00236100`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields) |
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | is called by | [`0x0023A3B0`](item-list.md) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) | calls | [`0x00237080`](../Enemy-Spawning/spawn-record-fields.md) Spawn entry: clear selection transient state for teardown (on spawn record fields) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) | is called by | [`0x00234880`](../Battle-Actions/boss-fights.md) Spawn group: teardown all grouped spawn units (on boss fights)<br>[`0x00234990`](../Enemy-Spawning/enemy-respawning.md) Spawn group: teardown units by group mask (on enemy respawning)<br>[`0x002350C0`](../Enemy-Spawning/enemy-spawning.md) Spawn lifecycle: check and retire by native range (on enemy spawning)<br>[`0x00237690`](../Battle-Actions/boss-fights.md) Spawn group: teardown all ungrouped spawn units (on boss fights) |
| [`0x00510160`](item-list.md) | calls | [`0x0023A3B0`](item-list.md) |

**World, areas and travel** (explained on [frame update order](../Engine-Core/frame-update-order.md), [force fight mode](../Engine-Core/force-fight-mode.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) | calls | [`0x00313F60`](equipping-an-item.md) (on equipping an item) |
| [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) | calls | [`0x00313F60`](equipping-an-item.md) (on equipping an item)<br>[`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00377C70`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) |

</details>
