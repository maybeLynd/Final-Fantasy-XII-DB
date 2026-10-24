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
| map names | 704 zones, 648 distinct names; the four `ttl` zones have none. 16 scene-variant zones (`rbn_z01`, `alc_z01` to `alc_z04`, `var_z01` and the like) carry their own code as the name |
| region names | all 708 zones, 51 distinct regions; the largest are Trial Mode (100 zones), The Great Crystal (73) and Draklor Laboratory (71) |
| scripts | all 708 ship, in each of the nine language folders (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`) |
| `.mot` | ships for 188 zones; named but not shipped for 520 |
| `.fpk` | named for all 708, shipped for none |
| map packs | 458 distinct zone packs and 88 distinct block packs, all shipped |
| area battle data | 215 distinct `.ard` files named; not shipped for 120 zones |
| remastered map art | 704 zones, 451 distinct lists, each with one mesh; 82,856 textures in all. The four zones `ttl_a01`, `ttl_b01`, `ttl_c01` and `ttl_d01` have none |
| map sounds | 704 zones bind a list, from 87 block packs: 1 to 48 ids, 624 distinct, 10,215 in all. The four `ttl` zones' block pack `tst0100` carries none. Sound map numbers 502 to 594, 88 distinct |
| models | 582 zones name models in their manifest, 209 distinct models in all |
| foes | 471 zones place foes. Seven zones (`nal_a01`, `nal_b01`, `rui_a04`, `sav_b01`, `rbn_a01`, `rbn_a03`, `srb_b04`) place definitions whose shipped name is "No name" (21 bestiary rows, NPC models such as `n1020`) and list that name |

The zone scripts have a copy in each language folder, and the table names the US one. The `.ard` files ship in the
`in` and `ch` folders (166 each, byte-identical, [Bestiary](../Enemy-Spawning/bestiary.md)), and the
map packs and the map art sit in folders of their own with no language.

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
| `art`, `art_meshes`, `art_textures` | the remastered `.ah` list and its mesh and texture counts; empty when the zone has none |
| `models` | the models of the zone script's actor manifest, by name |
| `foes` | the shipped names of the definitions the zone script places |
| `explanation` | a one-line summary |

## Related

- [Asset paths: every file the game asks for by resource kind and id, with its path, size and whether the archive ships it](../Game-Files-And-Data-Tables/asset-paths.md)
- [Model asset list: every model the game can bind, with its model file, motion lanes, remastered parts and the tables and scripts that use it](../Graphics/model-asset-list.md)
- [Map art](map-art.md) and [Map pack](mpk-map-pack.md)
- [Enemy placements](../Enemy-Spawning/enemy-placements.tsv)
