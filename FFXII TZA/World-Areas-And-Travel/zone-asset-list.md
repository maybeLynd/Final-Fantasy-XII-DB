---
title: "Zone asset list: every zone the area loader can enter, with the files it loads and the models and foes it brings"
kind: "reference"
category: "World, areas and travel"
addresses: "0x0032FCA0, 0x00264F10, 0x00264F40, 0x00264ED0, 0x003EA820, 0x00379A10, 0x001A7A50, 0x01EF9490, 0x00264FD0, 0x003635E0, 0x00331990, 0x00377B60, 0x003778B0, 0x00264F90, 0x0029C530"
---

## What it lists

[zone-asset-list.tsv](zone-asset-list.tsv) holds one line for each zone: 708 zones, numbered 12 to 1,311, over 215
areas. A zone is the area loader's context *n*. For each it gives the map and region names the player reads in the
menu, the files the loader requests for that zone and the models and foes the zone's script brings in. The 708 are
the zones whose script the US resource-kind 5 array names and the archive ships.

### Where the values come from

The columns come from the path arrays of [Asset paths](../Game-Files-And-Data-Tables/asset-paths.md) and the
archive index:

1. **The zone script.** The area loader `0x0032FCA0` loads manager 0 from kind 5 at index 3*n*: the zone script
   `.ebp`, with its `.mot` at 3*n* + 1 and its `.fpk` at 3*n* + 2
   ([File size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md)).
2. **The map row.** Row *n* of `map_ref.bin` (8 bytes from the header's `+0x04`, [Weather](weather.md)) names the rest:
   - the zone's own map pack, kind 4 at the row's word `+0x00` (`0x00264F10`; [Map pack](mpk-map-pack.md));
   - the block pack, kind 4 at the signed word `+0x00` of the 16-byte block record the row's `+0x02` selects
     (`0x00264F40`). The block record's second word plus 500 is the sound map number (`0x00264FD0`);
   - the area, the row's word `+0x04` (`0x00264ED0`). Its battle data is kind 21 at 2 × area, the `.ard` that
     `0x003EA820` sizes and reads ([Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)).
3. **The remastered map art.** `0x00379A10` cuts `<area>\<map>` out of the zone pack's path and swaps five zones for
   the art they reuse (the table `0x01EF9490`); `0x001A7A50` builds
   `.\GameData\D3D11\ArtData\map\<area>\<map>\<map>_d3d11.ah` ([Map art](map-art.md),
   [Prefetch and asset-header manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)). `art_meshes` and
   `art_textures` count the list's meshes and textures.
4. **The map sounds.** The binder `0x003635E0` keeps the `SPP1` list of the pack loaded in mode 0, the block pack
   (`0x00331990`), and opens the six-digit bank each listed id names ([Map sounds](../Sound-And-Music/map-sounds.md)). The
   block pack's slot 10 holds the list: a `0x20`-byte header with the id count at `+0x04`, then the `u32` ids.
5. **The models,** the bound ids of the zone script's section 12, the actor manifest
   ([Actor manifest](../EBP-Script-Files/ebp-actor-manifest.md)), named through
   [Model asset list](../Graphics/model-asset-list.md).
6. **The foes,** the definitions the zone script places ([Enemy placements](../Enemy-Spawning/enemy-placements.tsv)),
   by their shipped names.
7. **The names,** from the `us` name table `planmapname.bin` as its two indexers return them for field *n*; the
   menu's location line `0x0029C530` calls both, the map name for the current field and the region name for the
   current field, or for the loaded map `0x00314910` while flag `0x5E` is set (`0x0032A8A0`)
   ([Area flags](area-flags-navimapdata.md)):
   - the map name, `0x00377B60(n)`: entry *n* of the offset table at `+0x10`, while *n* is below the area count
     `+0x04` (1,312);
   - the region name, `0x003778B0(n)`: entry `[+0x04]` + group of the same table, while the group is below the region
     count `+0x08` (59). The group is the word `+0x06` of `map_ref.bin` row *n* (`0x00264F90`).

   An empty entry gives an empty name. For the 608 zones below 1,154 the map name is the one
   [area-flags-navimapdata.tsv](area-flags-navimapdata.tsv) lists for that id.

The five swapped zones are `dst0109` (art of `dst0103`), `dst0110` (`dst0105`), `frs0109` (`frs0101`), `frs0110`
(`frs0106`) and `gil0303` (`gil0301`).

### Shipped data

| Fact | Value |
|---|---|
| zones | 708, numbered 12 to 1,311; 47 name prefixes over 215 areas |
| map names | 704 zones, 648 distinct names; the four `ttl` zones have no name. 16 scene-variant zones (`rbn_z01`, `alc_z01` to `alc_z04`, `var_z01` and the like) carry their own code as the name |
| region names | all 708 zones, 51 distinct regions; the largest are Trial Mode (100 zones), The Great Crystal (73) and Draklor Laboratory (71) |
| scripts | all 708 ship, in each of the nine language folders (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`) |
| `.mot` | ships for 188 zones; named but not shipped for 520 |
| `.fpk` | named for all 708, shipped for no zone |
| map packs | 458 distinct zone packs and 88 distinct block packs, all shipped |
| area battle data | 215 distinct `.ard` files named; not shipped for 120 zones |
| remastered map art | 704 zones, 451 distinct lists, each with one mesh; 82,856 textures in all. The four zones `ttl_a01`, `ttl_b01`, `ttl_c01` and `ttl_d01` have no art list |
| map sounds | 704 zones bind a list, from 87 block packs: 1 to 48 ids, 624 distinct, 10,215 in all. The four `ttl` zones' block pack `tst0100` carries no sound id. Sound map numbers 502 to 594, 88 distinct |
| models | 582 zones name models in their manifest, 209 distinct models in all |
| foes | 471 zones place foes. Seven zones (`nal_a01`, `nal_b01`, `rui_a04`, `sav_b01`, `rbn_a01`, `rbn_a03`, `srb_b04`) place definitions whose shipped name is "No name" (21 bestiary rows, NPC models such as `n1020`) and list that name |

The zone scripts have a copy in each language folder, and the table names the US one. The `.ard` files ship in the
`in` and `ch` folders (166 each, byte-identical, [Bestiary](../Enemy-Spawning/bestiary.md)), and the
map packs and the map art sit in folders of their own with no language.

### When each zone opens

[zone-openings.tsv](zone-openings.tsv) gives each of the 708 zones the lowest story counter value (シナリオフラグ,
[Story progress](../Story-Events-And-Hunts/story-progress.md)) at which an open way leads into it from a zone that
is already open, with that way, its condition and what the date rests on. The reading starts from the New Game field,
`naf_a01` (field 274, Aerial Gardens), open at 0.

The 100 Trial Mode stages, `tri_a01` (field 1155) to `tri_t05`, belong to Trial Mode, not to the story, and carry
no date ([Trial Mode scripts](../Story-Events-And-Hunts/trial-mode-scripts.md)).

A way is one of these:

- a map jump in a zone script whose condition holds at that counter
  ([Zone changes and map jumps](zone-changes-and-mapjump.md)). A crystal teleport is not a way in: it leads only to
  a crystal already registered;
- a walk exit, the map jump of an exit group. It counts where the zone's walk mesh joins the entrance the party arrived
  by to the exit's floor, under the floor and map-jump settings the zone's start-up script makes at that counter
  ([Doors, gates and map changes](doors-gates-and-map-changes.md)). The party walks as movement kind 0; an exit the
  mesh joins only for a chocobo rider (kind 5) counts for a ride;
- a Strahl destination chosen on the World Map, under that area's gate in
  [menu-map-files-world-areas.tsv](../Game-Files-And-Data-Tables/menu-map-files-world-areas.tsv): Ridorana Cataract
  (`rwf_a01`) from 5150 and the Bahamut (`bhm_z01`) from 6100;
- an airship flight between aerodromes, no earlier than [airship-routes.tsv](airship-routes.tsv) opens a route to
  that town.

A jump to the map the party came from (`nowmap()` or `lastmap()`), and a way whose condition needs the entrance by
which the party arrived from the way's own destination, take the party back to where it was and are not ways in.

A condition can test saved values. Each starts at its new-game value: 0, or 1 for the boss words that the new-game
set-up `pre_z0000` sets to 1. A value is there from the lowest counter at which a store of it can run in an open zone
under its own condition; a store before the test in the same function counts where its own path holds. A key item a
condition tests is there from the step of the scene or script that gives it.

566 rows are `dated`, from 0 to 7150 over 51 values; the commonest are 105 (99 zones), 4230 (81) and 1475 (80). The
highest is `ttl_b01` at 7150, reached by an event in `bhm_d01`. 50 rows name a battle in `basis`, and without that
battle's store their date moves later: 40 the Zodiark battle (`hne_e01` step 137) and 10 the Firemane battle
(`grm_d01` step 155). The other rows:

- 100 `Trial Mode`;
- 39 `no way in`: 38 Draklor Laboratory rooms (`dor_`) and the title map `ttl_c01`. No way the table reads leads
  into them;
- 2 `title screen map`: `ttl_a01` and `ttl_d01` ([Title scripts](../Story-Events-And-Hunts/titles-scripts.md));
- 1 `not dated`: `grm_f01` (No. 1 Cloaca). Its way in from `grm_e08` needs four saved values, `global_var_2`,
  `global_var_3`, `global_var_5` and `global_var_6`, the sluice gate states, all at 1 (closed). The table names the
  way and gives no counter, because the reading leaves those four values free.

In 105 rows `basis` also names the walls the way's source zone switches on (`setmapidwall` kind 5, value 0) under a
condition that is not false at the date. The date does not take them into account: it counts the way open past
them. Kind 6 writes, which never change where a walking body stops, and writes that switch a wall off are not listed.
In 67 rows the arrival entrance of a way is held in a saved value; the date then counts the exit group reachable from
that arrival.

A `gate_text` or `basis_text` cell names each saved value it tests by a label, `the value of <label> (stored as the
<label> rows of saved-value-stores.tsv give)`. [saved-value-stores.tsv](saved-value-stores.tsv) gives every store of
each label with that store's own condition, in the same words, so each store is written once.

A value tested inside one of those conditions is named by its label and has rows of its own, so every store of every
value the cells name is in the table: 2,351 values, 30,875 stores. Among them are the values the door conditions of
[Script censuses](../Story-Events-And-Hunts/script-censuses.md) test and the values the `set_conditions` cells of
[Story flag ids](../Story-Events-And-Hunts/story-flag-ids.md) test.

A value that no script stores is named by its block, unit and offset, with the scope that was searched: `no line of this
script stores it` for a scratch1 value, `no <region> script stores it` for a scratch2 value, with the stores other areas
make counted, `no line of the us listings stores it` for a global value that no us script stores, and `no story script
stores it` with the developer test scripts' stores named when only those store it.

## Columns

| Column | Meaning |
|---|---|
| `zone`, `name` | the zone number *n* and the zone script's name |
| `map_name`, `region` | the map name `0x00377B60(n)` and the region name `0x003778B0(n)`; empty when the entry is empty |
| `script`, `mot`, `fpk` | the files at kind 5 indices 3*n*, 3*n* + 1 and 3*n* + 2, the US copy; "(not shipped)" when the archive lacks the file |
| `pack`, `block_pack` | the zone's map pack and the block pack |
| `sound_map` | the sound map number, the block record's second word plus 500 |
| `map_sounds` | the ids of the block pack's `SPP1` list, in list order; each names the six-digit bank `se<id / 1000>/se<id>` |
| `area`, `ard` | the area number and its battle data file; "(not shipped)" when the archive lacks it |
| `art`, `art_meshes`, `art_textures` | the remastered `.ah` list and its mesh and texture counts; empty when the zone has no list |
| `models` | the models of the zone script's actor manifest, by name |
| `foes` | the shipped names of the definitions the zone script places |
| `chests` | the zone's chests in [`treasure-chest-list.tsv`](treasure-chest-list.tsv), by zone number |
| `shops` | the shops of [`shops.tsv`](../Items-Equipment-Shops-And-Licenses/shops.tsv) whose `place` ends in the zone script's code, as number and name; `-` when the zone has no shop |
| `music_run` | the run of [`music-table.tsv`](../Sound-And-Music/music-table.tsv) whose field range holds the zone, by its offset, with the run's track |
| `npc_names` | the NPC name rows of [`npc-names-maps.tsv`](../Characters-And-Objects/npc-names-maps.tsv) for the zone |
| `crystals` | the zone's save and teleport crystals in [`save-and-teleport-crystals-list.tsv`](save-and-teleport-crystals-list.tsv), as kind and number; `-` when it has no crystal |
| `explanation` | a one-line summary |

The joined columns place 1,926 of the 1,966 chests, all 267 shops, 1,572 of the 1,575 NPC name rows and 80 of the 81
crystals. The others belong to scripts that no zone-script entry names, so no field loads them: the 40 chests of
`bts_z01`, the NPC name rows of `bts_z01`, `pre_a01` and `pre_b01`, and the crystal of `mic_b07`. Every zone lies in
a music run except field 869, `alc_z04` ([Music table](../Sound-And-Music/music-table.md)); its `music_run` is `-`.

### Columns of zone-openings.tsv

| Column | Meaning |
|---|---|
| `zone`, `name`, `map_name` | the zone number, its script's name and its map name, as in [zone-asset-list.tsv](zone-asset-list.tsv); `map_name` is `-` for the four `ttl` zones |
| `opens` | the story counter value at which the zone opens; `-` when the row is not dated |
| `status` | `dated`, `Trial Mode`, `title screen map`, `no way in`, or `not dated` with the saved values its way in tests |
| `way_in` | the way: the zone it leads from, its kind (`walk` for an exit group's map jump, `event` for a map jump elsewhere in the zone's scripts, `strahl` for a Strahl destination), then the actor, function and step of the map jump in the step tables; `new game start` for `naf_a01` |
| `gate` | the way's condition at that step, in the step tables' notation; `-` for a way with no condition |
| `basis` | what the date rests on, one clause per `; `: how the walk mesh joins the arrival to the exit, an arrival held in a saved value, the battle the date needs and the walls the source zone switches on |
| `gate_text`, `basis_text` | `gate` and `basis` in words: story counter values with their names, saved values by their label in [saved-value-stores.tsv](saved-value-stores.tsv), items by name |

### Columns of saved-value-stores.tsv

| Column | Meaning |
|---|---|
| `flag` | the label a `gate_text`, `basis_text` or `condition` cell, or a `set_conditions` cell of [story-flag-ids.tsv](../Story-Events-And-Hunts/story-flag-ids.tsv), gives the value: an engine-held value by its block, unit and offset (`global byte 0x934`); a scratch1 value, which one script's field holds, by that script, then block, unit and offset (`asp_a01 scratch1 16-bit word 0x4`); a scratch2 value, which the scripts of one area share, by block, unit and offset and the area's script prefix (`scratch2 16-bit word 0x80 of the mic_ scripts`); a script's own variable by the script and the variable's name in the listing; with the element in brackets when the store is to an array element |
| `script` | the script that holds the store |
| `place` | the actor and function of the store and its listing line |
| `store` | the store as the listing writes it, with a bitwise or written `bitor`; a value the game's symbols name, such as `global_flag[2]`, is under that name here |
| `value` | the value stored, or `computed` when the store writes the result of an expression |
| `condition` | when the store runs, in words: `every time the line runs` when nothing before it is tested; a value tested here that has rows of its own is named by its label, and `it` is the row's own `flag` (`it is below 25` tests the value before this store) |

## Related

- [Asset paths: every file the game asks for by resource kind and id, with its path, size and whether the archive ships it](../Game-Files-And-Data-Tables/asset-paths.md)
- [Model asset list: every model the game can bind, with its model file, motion lanes, remastered parts and the tables and scripts that use it](../Graphics/model-asset-list.md)
- [Map art](map-art.md) and [Map pack](mpk-map-pack.md)
- [Enemy placements](../Enemy-Spawning/enemy-placements.tsv)
