---
title: "Equipment list: every weapon, shield, armor, accessory and ammunition row with its name, class, price, stats, elements, statuses and bonuses"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF0F8, 0x0031C5D0, 0x0031C911, 0x0031C981, 0x002FEF30, 0x0031E9F0, 0x00388409, 0x0038BE30, 0x00317B70, 0x00317930, 0x00323C60, 0x002F8FA0"
---

## What it lists

[`equipment-list.tsv`](equipment-list.tsv) holds one line for each of the 557 rows of the equipment table that registry slot `0x02EBF0F8`
reaches (`battle_pack.bin` directory entry `+0x38`). The meaning of every field, and the code that reads it, is on
[Equipment row](equipment-row.md); this page is the shipped content of that table.

- Rows 0-419 are the equipment the party can hold, ids `0x1000`-`0x11A3`, the 420 counts of the inventory's
  equipment class ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): 200 main-hand
  weapons, 52 off-hand items (shields and ammunition), 60 head pieces, 60 body pieces and 48 accessories.
- Thirteen of the main-hand rows, 179-191, are named Reserve: classes 5, 0 and 8 and a price of 1, with weapon
  stats (Attack 61-201, reach, recipe, knockback on three) and element sets of their own, and empty bonus stats. An
  inventory count reaches them, and the party table gives them to the 13 Espers as starting main hands, rows 27-39
  one to one. Their explanation says so and lists their Attack and element sets.
- Rows 420-556, ids `0x11A4`-`0x122C`, are past the inventory's 420 counts, so the party cannot hold them. Their
  names are "NOT USED" (124 rows) or "Reserve" (13 rows). The id check `0x00322C50` still accepts them, since it
  bounds class 6 by the table's own 557 rows (`0x1000` to `0x1000` + 557 - 1).
- The 13 rows named Reserve here, 544-556, are the Espers' starting body pieces. Thirteen `NOT USED` rows, 440,
  444-449, 462-464, 486, 490 and 491, are reserve data: the id check accepts them and nothing shipped names them.
- Enemies are given these ids: 958 of the 1,146 enemy definitions hold one of them in their main-hand word
  `+0x16`, which `0x0023AC80` installs ([Bestiary](../Enemy-Spawning/bestiary.md)).

### Where the values come from

Each line is read from the shipped `us` `battle_pack.bin` in these steps:

1. the `st2e` table at entry `+0x38`: 557 rows of 52 bytes from the section's `+0x20`, and each row's 24-byte bonus
   record at section `+0x7144` plus the row's `+0x28`;
2. the name word `+0x02` through the word banks at entry `+0xF8`, as `0x0031C5D0` does (`0x0031C911`);
3. the class name: the name word (second `u16`) of row *class* of the category table at entry `+0x18`, which
   `0x0031C5D0` reads through id kind 28 (`0x0031E3DB`-`0x0031E435`). Its rows 0-26 carry the names of the classes 0-26
   ("Unarmed", "Sword (1H)", "Shield", "Arrows" and the others), and class *n* takes the name of row *n*. The shipped name
   of row 22 is "NOT USED crown";
4. the element bits by the names on [Elements](../Damage-And-Battle-Formulas/elements.md), and the status bits by the names in
   [Statuses](../Status-Effects-And-KO/statuses.md)' table;
5. every one-byte text code through the glyph table of the shipped `us` font `font00.dat` (records of `0x24` bytes
   from `+0x28`, key = byte - `0x20`, the glyph's UTF-8 at `+0x04`, as [Fonts](../Menus-And-HUD/fonts.md) describes).

Every name word of this table starts with the two zero bytes that `0x002B58B0` skips, so its other branch, for a word
without them, is never taken for this table.

The group of a row's class decides which of `+0x18`, `+0x19` and `+0x1A` fill the weapon, shield or armor columns,
as the stats rebuild `0x002FEF30` reads them ([Equipment row](equipment-row.md), "The class byte and the group").

### Properties of the shipped rows

- The table's own header gives 557 rows of 52 bytes, one TSV line each.
- Example rows: row 1, Broadsword, has `+0x12` = `0x0186` (390 gil, the price `0x0031C981` reads),
  `+0x1A` = 14 (Attack) and `+0x11` = 18 (it takes a shield in the off hand); row 0, Unarmed, has Attack 12 and the
  class name Unarmed.

### Where each piece of equipment comes from

`sources` joins tables already in the database by id, and reads the scripts where a table stops short. It holds one part per kind of source, the parts separated by `;`:

- `shop:` each shop that sells it, by name and number in [`shops.tsv`](shops.tsv), with the map (region) whose script gives an actor that shop (`setshopname`, the `place` column), and when the list that holds it goes on sale:
  - from the start;
  - from a story progress value, with the story point that writes it ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)), or, where no story script writes the value, with the first written value that meets it, which is so for 500: "from story progress 500 (met from 520, After the floating continent)" (below);
  - from a clan rank, with the rank's shipped name;
  - for the Clan Provisioner's last list, from joining Clan Centurio (below).
- `bazaar:` each bazaar good that gives it, with the good's id ([`bazaar.tsv`](bazaar.tsv)).
- `treasure chest (N):` every treasure chest that can give it, N chests in all ([Treasure chests](../World-Areas-And-Travel/treasure-chests.md)). 367 pieces of equipment have a chest part, 6 of them no other source.
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
- `trophy trade:` the Hunters' Camp (Phon Coast) sale, with the price ([Price list](../Rewards-EXP-Gil-And-Loot/price-list.md)), how many trophies each hunter must hold, and the package:
  - the Shifty-Eyed Man, later named Outfitters, sells 31 reward packages for gil, each once;
  - he offers a package only after the player has given enough trophies to the three hunters Atak, Blok and Stok;
  - each hunter takes one trophy at a time, any of the 30 trophy key items `0x80B9`-`0x80D6`, and counts the trophies given to him;
  - the seller opens his menu only once quest 71 has reached progress 70, which the three hunters set (`fon_b01`).
- `hunt reward:` the hunt whose report gives it, with the package and the map (region) and script that report it ([Hunts](../Story-Events-And-Hunts/hunts.md), [Reward selector list](../Rewards-EXP-Gil-And-Loot/reward-selector-list.md)):
  - the script verb `questresultwindow(n)` opens the reward window for quest n and grants at once the package its selector names ([Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md));
  - the selector is `0xA000` + the text index of entry n of `questbase.bin` (`0x00344C60`, `0x00473C90`), which is n for the 45 hunts, quest ids 128-172 ([Small .bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md));
  - a package that a selector names, that no hunt report opens and that no script gives would be listed as `reward package:` with its selector; no package is.
- `starting equipment:` the main characters who wear it when the game begins ([Party table](../Party/party-table.md)).

A shop list goes on sale once it or any list above it on the shop's ladder meets its condition, and the last list is always on sale ([Shops](shops.md), "Choosing a list"). The story test is the story counter at least the threshold (`0x002FADF3`-`0x002FAE0D`).

No script writes story progress 500. The values the scripts write go from 490 (After the captive Penelo) to 520 (After the floating continent), so a list that waits on 500 goes on sale at 520.

The Clan Provisioner is a Mysterious Merchant in Muthru Bazaar (Rabanastre) until bit `0x1` of script global byte `0x041D` is set; only then does its actor take the shop's name (`rbn_a02`). Montblanc sets that bit the first time the player talks to him in The Clan Hall (Rabanastre), with the message "You are now a member of Clan Centurio!" (`rbn_a14`).

Every part names every source. A cell that would be longer than 1,000 characters moves its longest parts, longest first, to [`item-sources.tsv`](item-sources.tsv) until it fits, and gives for each moved part its label, its count and the table, as `drop (28): in item-sources.tsv` for the Potion.

That table has one line per entry: `id` and `name` of the row, `part` (the label, or `used_for` and the label for a key item's use) and `entry`. A treasure chest part counts chests, and one entry can hold several. `-` means that none of these tables names a source. The starting inventory table adds nothing ([Starting inventory](../Party/starting-inventory.md)).

Six weapons have no source for the player. Their cells start `no source for the player:` for the five a guest
wears and `no source:` for the Hero's Blade, which nobody wears. Joyeuse, Chirijiraden, Flimsy Blade and the two Nightmare rows are the main-hand weapons of guests in the party table ([Party table](../Party/party-table.md), word `+0x0A`): Larsa (row 13), Reddas (rows 14 and 16), Basch (row 9) and Vossler (`0x10A6` row 11, `0x10A9` row 12). No party table row wears the Hero's Blade.

None of the six is in a shop, bazaar good, treasure chest, enemy slot, reward package, hunt reward or script give. Scenario sets give or equip them ([Scenario presets](../Party/scenario-presets.md)), but a new game asks for set 0, `naf_b04` for set 1, and the developer script `evt_t0505` for sets 0, 2, 3, 11-13, 15, 17, 18, 20 and 22-49.

### The licence it needs

`licence` names the licence squares whose node lists the equipment id among its grants ([`license-list.tsv`](license-list.tsv), `grant_ids`), by name and node. Owning any one of them answers the licence question.

`0x00317930` also refuses an item whose slot is not the one asked (`0x00317A21`), an off-hand item whose `+9` is not
`0x12` and does not match `+0x11` of the item in the loadout's first word (`0x00317A82`), and an item whose `+9` bit
is set in the character's row of the table at `[0x02EBF130]` (`0x00317AD6`), and it passes a null record or one whose
byte `+5` is not 0 before any of that table or licence test (`0x00317A87`, `0x00317A8F`).

The equip test `0x00317B70` calls `0x00317930`, which asks `0x00323C60` (`0x00317ADE`); that builds the node mask with
`0x002F8FA0` ([Licenses](licenses.md), "The test"). `no licence needed` marks a row whose `+0x07` bit `0x10` is set,
which `0x00323C60` passes without the board (`0x00323CDF`).

`0x00317B70(row, id, slot, flags)` runs `0x00317930` on the party record of row `row`, `[0x02EBF190] + 8 + row × 0x1C8`,
with its slot words `+0x50` as the loadout and with the free-copy test when `flags` bit `0x1` is clear
(`0x00317B7D`-`0x00317BAB`). A row above `0x27` is refused, 0 (`0x00317B78`, `0x00317BB5`).

## Columns

| Column | Meaning |
|---|---|
| `id` | the equipment id, `0x1000` + row |
| `row` | the row number |
| `name` | the item's shipped name |
| `slot` | main hand, off hand, head, body or accessory (mask `0xE0` of `+0x07`) |
| `class`, `class_name` | the class `+0x09` and its shipped category name |
| `sub_type` | `+0x04`, the kind of item copied to the query record `+0x2C` (`0x0031C9C4`) |
| `sort_key` | `+0x06`, the Optimise tie-break (`0x002F7C3C`) |
| `ordinal` | `+0x08`, the row's order inside its class (`0x0031C9CB`) |
| `price` | buy price in gil (`+0x12`) |
| `attack`, `reach_tenths`, `recipe` | weapons and ammunition: Attack Power `+0x1A`; weapons: reach in tenths `+0x18` and the damage recipe `+0x19` ([Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md)) |
| `defense`, `magick_resist`, `augment` | head, body and accessories: Defense `+0x18`, Magick Resist `+0x19`, and the augment `+0x1A` by its term on [Augment list](../Damage-And-Battle-Formulas/augment-list.md) with its id (empty for no augment; [Augments](../Damage-And-Battle-Formulas/augments.md)) |
| `shield_evade`, `magick_evade` | shields: `+0x18` and `+0x19` |
| `knockback`, `combo`, `weapon_evade` | weapons (classes 0-17): `+0x1B`, `+0x1C`, `+0x1D`; empty on ammunition, where all three are 0 |
| `element` | weapons and ammunition: the attack element `+0x1E` (`0x0038BE30`) |
| `status_chance`, `statuses_inflicted` | weapons and ammunition: the on-hit chance `+0x1F` and the statuses `+0x20` |
| `charge_base` | weapons (classes 0-17): the charge time base `+0x27` |
| `charge_weight` | `+0x10`, summed over the equipped items while the battle flag slows the charge |
| `off_hand_class` | `+0x11`, the class the off-hand item must have; -1 for no class |
| `hp`, `mp`, `strength`, `magick_power`, `vitality`, `speed` | the bonus record's stat bonuses |
| `statuses_held`, `status_immune` | the bonus record's statuses the wearer has, and those it cannot get |
| `absorb`, `nullify`, `halve`, `weak`, `potency` | the bonus record's element sets |
| `no_license`, `hits_flying`, `cannot_sell` | `yes` for bits `0x10`, `0x4` and `0x2` of `+0x07` |
| `b24` | weapons (classes 0-17): `+0x24`, one value per weapon kind |
| `reach_kind` | weapons (classes 0-17): `+0x25`, the range pair that sets the near and middle distance (`0x00320D93`) |
| `motion_class` | weapons (classes 0-17): `+0x26`, the attack motion class (`0x0032041E`) |
| `attack_effect` | weapons (classes 0-17): `+0x2C`, the effect a plain Attack shows in its low 15 bits (`0x0030AD56`) |
| `bonus_record` | the bonus record's index: `+0x28` / 24 |
| `model_id` | weapons, ammunition and shields: the held model `+0x30` |
| `explanation` | a one-line summary built from the row's own fields; for the Reserve rows 179-191 and the rows past the inventory's 420, what the row is and who holds it, or that nothing shipped names it |
| `sources` | where the piece of equipment is obtained, one part per kind of source, with each shop's place and opening, how a scene gift is handed over, the trophy trade and the hunt reward, the treasure chests that hold it with the odds ("Where each piece of equipment comes from" above), or for a part moved to [`item-sources.tsv`](item-sources.tsv) its count; for the six guest weapons, `no source for the player` and who wears them; `-` for a row with no source |
| `licence` | the licence squares that grant it, by name and node, or `no licence needed` ("The licence it needs" above) |

## Related

- [Equipment row: every field of a weapon, shield, armor, accessory or ammunition data row and its bonus record](equipment-row.md)
- [Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script](../Damage-And-Battle-Formulas/augments.md)
- [Treasure chests: where each chest stands, whether it appears and comes back, and what it holds with the odds of each content](../World-Areas-And-Travel/treasure-chests.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Script VM: `0x0023A3B0` is called by `0x00510160`; `0x00344C60` calls `0x00267E10`; `0x00473C90` is called by `0x00344C60`;
  `0x00510160` calls `0x00267E10`, `0x0037CF50`; those functions are documented on
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Spawn encounter lifecycle: `0x0023A3B0` calls `0x002355A0`; `0x0023A570` calls `0x00236100`; `0x0023A570` is called by
  `0x0023A3B0`; `0x00300E40` calls `0x00237080`; `0x00300E40` is called by `0x00234880`, `0x00234990`, `0x002350C0`, `0x00237690`;
  `0x00510160` calls `0x0023A3B0`.
- Spawn encounter lifecycle: those functions are documented on [battle units](../Characters-And-Objects/battle-units.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md),
  [enemy respawning](../Enemy-Spawning/enemy-respawning.md).
- Spawn encounter lifecycle: and on [frame update order](../Engine-Core/frame-update-order.md),
  [boss fights](../Battle-Actions/boss-fights.md).
- World area: `0x0023A570` calls `0x00313F60`; `0x003266C0` calls `0x00313F60`, `0x00377C20`, `0x00377C70`; those functions are
  documented on [frame update order](../Engine-Core/frame-update-order.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [party control modes](../Engine-Core/party-control-modes.md).
