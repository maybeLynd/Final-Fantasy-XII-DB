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

A zone's number picks its script files directly, and the zone's row in `map_ref.bin` names the rest: its own map pack,
a shared block pack that carries only sounds, and the area whose battle data it loads. The models come from a list
inside the zone's script.

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
     `0x003EA820` sizes and reads ([Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md));
   - the row readers take *n* with no bound (`0x00264F26`, `0x00264F56`, `0x00264FE6`) and answer only while `0x02099D88`
     and `0x02099D90` are both set: otherwise `0x00264F10` gives 0 and `0x00264F40` and `0x00264FD0` give -1 (`0x00264F3D`,
     `0x00264F7E`, `0x0026500F`).
3. **The remastered map art.** `0x00379A10` cuts `<area>\<map>` out of the zone pack's path and swaps five zones for
   the art they reuse (the table `0x01EF9490`); `0x001A7A50` builds
   `.\GameData\D3D11\ArtData\map\<area>\<map>\<map>_D3D11_srm.ah` and requests it when `0x0019EAA0` can open it,
   else `<map>_D3D11.ah` (`0x001A7C02`-`0x001A7C53`; [Map art](map-art.md),
   [Prefetch and asset-header manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)).
   - Every shipped map folder has its `_srm` list, so the game requests that one. `art` names the plain
     `<map>_d3d11.ah` list, and `art_meshes` and `art_textures` count that list's meshes and textures.
   - `0x00379A10(kind, index)` acts only when `0x0032E400(kind, index)` gives a size above 0 (`0x00379A3E`). It copies
     the path `0x002DF980(kind, index)` and keeps the text between the fourth and the second separator (`\` or `/`)
     from the end (`0x00379A5A`-`0x00379B0A`); a cut at or past 260 characters ends in the range-check failure
     `0x00809728` (`0x00379ADD`-`0x00379AE4`).
   - The swap compares that text from its seventh character on with the five names of `0x01EF9490` and, on a
     match, keeps the first six characters and appends the reused map (`0x00379B30`-`0x00379B8A`). The name then
     goes to `0x001805D0` and `0x022BE7E0` is set to 0 (`0x00379B94`, `0x00379B99`; [Map art](map-art.md)).
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
     count `+0x08` (59). The group is the word `+0x06` of `map_ref.bin` row *n* (`0x00264F90`), 0 while that table
     is not bound (`0x00264FBE`). While the name table `[0x02ADD0F8]` is not loaded the region name is empty
     (`0x003778C5`, `0x003778E8`).

   An empty entry gives an empty name. For the 608 zones below 1,154 the map name is the one
   [area-flags-navimapdata.tsv](area-flags-navimapdata.tsv) lists for that id.

The five swapped zones are `dst0109` (art of `dst0103`), `dst0110` (`dst0105`), `frs0109` (`frs0101`), `frs0110`
(`frs0106`) and `gil0303` (`gil0301`).

### Shipped data

| Fact | Value |
|---|---|
| zones | 708, numbered 12 to 1,311; 47 name prefixes over 215 areas |
| map names | 704 zones carry the name the game gives, 648 distinct. The four `ttl` zones, whose entry is empty, carry what they show: title screen (`ttl_a01`), staff roll (`ttl_b01`), second title screen (`ttl_c01`) and Trial Mode completion screen (`ttl_d01`). 16 scene-variant zones (`rbn_z01`, `alc_z01` to `alc_z04`, `var_z01` and the like) carry their own code as the name |
| region names | all 708 zones, 51 distinct regions; the largest are Trial Mode (100 zones), The Great Crystal (73) and Draklor Laboratory (71) |
| scripts | all 708 ship, in each of the nine language folders (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`) |
| `.mot` | ships for 188 zones; named but not shipped for 520 |
| `.fpk` | named for all 708, shipped for no zone |
| map packs | 458 distinct zone packs and 88 distinct block packs, all shipped |
| area battle data | 215 distinct `.ard` files named; not shipped for 120 zones |
| remastered map art | 704 zones, 451 distinct lists, each with one mesh. The 451 shipped lists name 62,089 textures, none twice in one list, 62,087 distinct texture files in all; the `art_textures` column sums to 82,856 because a list that several zones share is counted on each of its rows. The four zones `ttl_a01`, `ttl_b01`, `ttl_c01` and `ttl_d01` have no art list |
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

[`zone-ways-in.tsv`](zone-ways-in.tsv) lists every map change with its trigger, arrival, gate and wall state. A way
is one of these:

- a map jump in a zone script whose condition holds at that counter
  ([Zone changes and map jumps](zone-changes-and-mapjump.md)). A crystal teleport is not a way in: it leads only to
  a crystal already registered;
- a walk exit, the map jump of an exit group. It counts where the zone's walk mesh joins the entrance the party arrived
  by to the exit's floor, under the floor and map-jump settings the zone's start-up script makes at that counter
  ([Doors, gates and map changes](doors-gates-and-map-changes.md)). The party walks as movement kind 0; an exit the
  mesh joins only for a chocobo rider (kind 5) counts for a ride when its condition lets a rider through;
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

567 rows are `dated`, from 0 to 7150 over 79 values; the commonest are 4350 (75 zones), 100 (43) and 3050 (43).
The highest is `ttl_b01` at 7150, reached by an event in `bhm_d01`. 89 rows name a battle in `basis`: 10 the Firemane
battle (`grm_d01` step 155), 75 the Tyrant battle (`gil_c02` `ボス登場.touch` line 795) and 4 the Daedalus battle
(`gil_a02` `ボス登場.touch` line 681). Without the Firemane store the date moves later.

The Tyrant and Daedalus rows lie behind a Giruvegan device that the battle's own store enables first. That store runs
with the party's control off, so these rows take the counter the battle's function stores as it hands control back:
4350 (`gil_c02` `ボス登場.touch` line 969) and 4300 (`gil_a02` `ボス登場.touch` line 854). The developer test script
`evt_t0505` can place a party in some of these zones at its own counter values, and the dates do not count it.

The other rows:

- 100 `Trial Mode`;
- 39 `no way in`: 38 Draklor Laboratory rooms (`dor_`) and the title map `ttl_c01`. No way the table reads leads
  into them;
- 2 `title screen map`: `ttl_a01` and `ttl_d01` ([Title scripts](../Story-Events-And-Hunts/titles-scripts.md)).

`grm_f01` (No. 1 Cloaca) is dated 1540. Its way in from `grm_e08` needs four sluice gate states, saved bytes `0x09E0`,
`0x09E1`, `0x09E3` and `0x09E4`, all at 1 (closed). Entering `grm_e09` stores 1 in `0x09E0`, and entering `grm_e12` stores
1 in `0x09E1`, each from its `Mapdirector.init`. A switch in each room stores the other two: `grm_e09` `0x09E4` and
`grm_e12` `0x09E3`. Those switches are talk actors with no condition. Both rooms open at 1540, so the date is theirs.

`grm_e13`, open from 290, has switches that store 1 or 0 in `0x09E0` and `0x09E1` too, and they do not move the date.
`mic_d01` stores 0 in all four, from `Map_Director.ガラムサイズフラグリセット`.

In 100 rows `basis` also names the walls the way's source zone switches on (`setmapidwall` kind 5, value 0) under a
condition that is not false at the date. The search behind a date counts the way open past them, unless the wall's
switch or door sets the date, as in the 28 rows of Barheim Passage and the Lhusu Mines below. Kind 6 writes, which
never change where a walking body stops, and writes that switch a wall off are not listed.

In 67 rows the arrival entrance of a way is held in a saved value. In 59 of them the source zone's script stores that
value when the zone starts up, in the branch for that map, which `store_conditions` names; in the other 8 it stores
the value in the function that makes the jump. The entrance is fixed per way, and
[`zone-openings-saved-arrivals.tsv`](zone-openings-saved-arrivals.tsv) gives it with its store. In all 67 it reaches
the exit group the date counts, with no walls and with every wall the row names standing.

[`zone-openings-wall-gates.tsv`](zone-openings-wall-gates.tsv) tests those 100 rows on the source zone's walk mesh.
The walls of a row are the wall records of its groups, taken as the unit solids of
[Geometry primitives](../Movement-And-Pathfinding/geometry-primitives.md); no group in these rows holds a type-1
polygon.

`result` says whether the arrival still reaches the exit's floor with the walls standing: the floor that
stands with the row's wall is shut with it, and the verdict rows state the date. The floor is flooded in
steps of 0.1, and a point is blocked inside a solid at 0.05 above the floor:

| `result` | Rows |
|---|---:|
| `joined`: the mesh joins them with the walls standing | 85 |
| `separated`: the walls cut every path on the mesh | 11 |
| `joined from some arrivals`: an arrival held in a saved value, joined from some of the zone's entrances | 1 |
| `no walk-mesh basis`: the row's date does not rest on the walk mesh | 3 |

A `separated` row does not make its date wrong by itself. The wall's condition, in `basis_text`, may be false when
the party arrives, or a lift may run on the arrival side. `result` leaves out the body's radius, and
`result_radius_0.5` repeats it for a radius of 0.5, and no row differs. Six rows also shut the floor groups
that their listing shuts with the walls or at the row's date, as the table `ROW_STATE` in `wall_gates.py` gives.

[`zone-openings-wall-verdicts.tsv`](zone-openings-wall-verdicts.tsv) joins these rows to their cutting wall, its
condition, its lift and the arrival position:

| Verdict | Rows |
|---|---:|
| the date moves | 7 |
| the named way is shut at the date | 2 |
| the date stands | 7 |

The `lus_a04` row there tests arrival entrance 1, the near side; the date rests on entrance 5, which the wall-gates
table tests, so that row is `joined`. [`zone-openings-wall-points.tsv`](zone-openings-wall-points.tsv)
gives the entrances, exit groups and listed points each wall state joins, by the same flood;
`Database/Tools/catalogues/wall_points.py` writes it.

In Barheim Passage the walls follow the power and door switches. `mic_a06` opens at 321, when `0x9C1` can reach 5
(`mic_a01` lines 950, 1495). The rooms on the way to `mic_c02` open at 323, the counter stored on first entering
`mic_a06` (line 292), and so do the zones reached through them: 16 rows in all carry a Barheim date from this.

`mic_e03` follows `mic_e02` at 323. The cart's touch and talk regions are its field sign records, and the
arrival entrances reach both while its wall stands, so the party can take the wall down from the arrival side.
`mic_e04` and `mic_d01` take their date from `mic_e03`.

The far half of the Lhusu Mines opens at 1982, through the Site 3 door in `lus_b02`. The door answers from that
counter and needs the Site 3 Key (`鉱区の扉.main` line 655, `.talk` line 754). The talk regions of the
Transitway and `lus_b02` switches are reached only from the far side of their walls, so those switches do not open
the way in.
`lus_b02` opens at 660, when the near half of `lus_b01` leads to it (below `0x0294` that exit leads to another map).

The Site 3 Key is given at `byu_a17` during quest 165 (lines 1953, 2027). Its speaker tests clan rank 5 or more and
story counter 1982 or more (line 1855), so the door also rests on a clan rank the story counter does not hold.

`lus_b03` opens at 1982, through that door. `lus_d03` opens at 3050: its door needs the Site 11 Key, given at
`fon_b01`, which opens at 3050, and the `lus_d01` switch that takes wall 1 down is on the `lus_d03` side of that
wall. `lus_e01` and `lus_f01` to `lus_f05` follow it. 12 rows carry a Lhusu date from this. A switch's talk
region is its field sign record, tested on the walk mesh with its wall standing and its floor group shut.

The hub door of Henne Mines moves five dates. `hne_c01`, `hne_c02`, `hne_c03`, `hne_d01` and `hne_e01` open at 4400:
floor group 2 of `hne_b01` is shut unless bit `0x2` of `g_com_マップ通行制限フラグ[1]` is set
(`Map_Director.init`, lines 638 to 644), and outside developer scripts only `ガリフ族工芸家03.talk` in `glf_a02`
sets it.

That talk sets it only once the Mine Flayer hunt has been reported to `ガリフ戦士05` (global `0x0313`, the
test at line 6025; the hunt is posted from
story progress 3000 at clan rank 5 or higher), and only with ten of the Espers `0xC012` to `0xC01E` held.
Zodiark lies behind the door, so the tenth of the other twelve fixes the date: Shemhazai, at 4400.

The Golmore barrier moves 22 more. Floor group 1 of `gol_a01` and `gol_a02` is shut, on foot and riding, without
key item `0x80B7`, Lente's Tear. Scene `vic_a0300` gives it, and `イベント管理.姉と妹_再生` in `vic_a01` stores 1950
as it plays, so the zones past the barrier open at 1950: `gol_a03` to `gol_d02`, the `pbc_` zones, `mfr_a01` to
`mfr_a04`, `mrm_a01`, `mrm_a02` and `hne_c04`.

Beyond them, `bul_b02`, `bul_b01`, `bul_a03` and `bul_a01` open at 1976, 1982, 1984 and 1986, one forced store on
each arrival. `mrm_b01` opens at 2050, because `DOOR.talk` is disabled below that value, and ten zones past it
open at 2057, which `mrm_b01` stores on arrival.

Three floors move dates. `alc_b04` opens at 3220: floor group 1 of `ald_a01` is shut below that value, its wall group
holds no solid, and `NPC_JULES.talk` stores 3220 before it takes the party through. The nine zones reached through
`alc_b04` follow it. `lus_a02` opens at 610: floor group 3 of `lus_a01` is shut below that value, and `lus_a03`,
`lus_b01` and `lus_g01` follow it. `grm_c01` opens at 257: floor group 4 of `grm_b02` is shut below 249, and the
touch rect that reopens it leads to the store of 257. `grm_b03`, `grm_b05` and `grm_d01` follow it.

Floors move seven more dates, on rows with no wall. `glf_a02` opens at 1625 and `glf_a03` at 1628, when the events
that store those values reopen floor group 1 of `glf_a01` and `glf_a02`. `nal_c01` opens at 310 and `rsn_b02` at 930,
when the touch rect that reopens floor group 31 leads to the store of that value. `naf_b01` opens at 16, stored just
before the door of `naf_a02` reopens. `mfr_c01` opens at 4200, stored after the battle that reopens floor group 1 of
`mfr_b01`. `vic_a03` opens at 1700, when the hidden passage of `gol_a02` opens.

The zones reached through those ways follow them: `nal_d01`; `rsn_b03`, `rsn_b04`, `rsn_c01`, `rsn_d01` and `rsn_y01`;
`mfr_c02` and `mfr_c03`; `naf_b02` and `naf_b04`; `vic_a01` and `vic_a02`.

The `gil_` rows and `rbl_e01` keep their results with floors their listings open during play: every floor a `gil_`
source shuts is reopened by that listing, `floor_check.main` among them, and in `rbl_d02` the touch rect of
`mfloor_ctrl_finish01` opens floors 10 and 11.

`dor_b01` and `grm_b05` are `joined` with no solid tested: the groups their sources switch on hold no
wall record or wall polygon, so `wall_records` and `edges_met` are 0.

`wall_polygons`, `wall_records` and `edges_met` give what was tested; `edges_met` counts the floor edges a solid
meets 1.0 above the floor. `Database/Tools/catalogues/wall_gates.py` writes the table.

A `gate_text` or `basis_text` cell names each saved value it tests by a label, `the value of <label> (stored as the
<label> rows of saved-value-stores.tsv give)`. [saved-value-stores.tsv](saved-value-stores.tsv) gives every store of
each label with that store's own condition, in the same words, so each store is written once.

A value tested inside one of those conditions is named by its label and has rows of its own, so every store of every
value the cells name is in the table: 3,321 values, 47,948 stores. Among them are the values the door conditions of
[Script calls in every script](../Story-Events-And-Hunts/script-censuses.md) test and the values the
`set_conditions` cells of
[Story flag ids](../Story-Events-And-Hunts/story-flag-ids.md) test.

A value that no script stores is named by its block, unit and offset, with the scope that was searched: `no line of this
script stores it` for a scratch1 value, `no <region> script stores it` for a scratch2 value, with the stores other areas
make counted, `no line of the us listings stores it` for a global value that no us script stores, and `no story script
stores it` with the developer test scripts' stores named when only those store it.

## Columns

| Column | Meaning |
|---|---|
| `zone`, `name` | the zone number *n* and the zone script's name |
| `map_name`, `region` | the map name `0x00377B60(n)` and the region name `0x003778B0(n)`. The four `ttl` zones, whose map name entry is empty, carry what the zone shows instead ([Title scripts](../Story-Events-And-Hunts/titles-scripts.md)); their region, Pharos at Ridorana, is region entry 1, as the `map_ref.bin` rows of these four zones hold group 1 and no other zone in this list holds group 1 |
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

The joined columns place 1,926 of the 1,966 chests, all 267 shops, 1,578 of the 1,583 NPC name rows and 80 of the 81
crystals. The others belong to scripts that no zone-script entry names, so no field loads them: the chests of
`bts_z01` (16), `pre_a01` (12) and `pre_b01` (12), the NPC name rows of `bts_h01`, `bts_y01`, `bts_z01`, `pre_a01`
and `pre_b01`, and the crystal of `mic_b07`. Every zone lies in
a music run except field 869, `alc_z04` ([Music table](../Sound-And-Music/music-table.md)); its `music_run` is `-`.

### Columns of zone-openings.tsv

| Column | Meaning |
|---|---|
| `zone`, `name`, `map_name` | the zone number, its script's name and its map name, as in [zone-asset-list.tsv](zone-asset-list.tsv) |
| `opens` | the story counter value at which the zone opens; `-` when the row is not dated |
| `status` | `dated`, `Trial Mode`, `title screen map` or `no way in` |
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x002DF980` is called by `0x0032FCA0`; `0x0032E400` is called by `0x0032FCA0`, `0x00330310`, `0x003306E0`;
  `0x0032FCA0` calls `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0`.
- Actor entity: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [zone changes and mapjump](zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Audio: `0x003635E0` calls `0x002DF070`, `0x00363750`; those functions are documented on [mpk map pack](mpk-map-pack.md),
  [game over](game-over.md).
- Input: `0x0032A8A0` is called by `0x00253C70`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Presentation: `0x001A7A50` calls `0x001A92C0`; `0x002DF980` is called by `0x001BB2B0`; `0x00314910` is called by `0x001CD0E0`;
  `0x0032E400` is called by `0x003B2310`, `0x003B53C0`; `0x00377B60` is called by `0x002B7B80`, `0x002BAF80`.
- Presentation: those functions are documented on [map art](map-art.md),
  [file size tables fst](../Game-Files-And-Data-Tables/file-size-tables-fst.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md).
- Presentation: and on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Save load settings: `0x00264F90` is called by `0x00583D60`; `0x00314910` calls `0x002EF2B0`; `0x0032A8A0` calls `0x002EF2B0`;
  `0x0032A8A0` is called by `0x00583D60`; those functions are documented on
  [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Script VM: `0x00264F10` is called by `0x0050CDE0`; `0x00264F40` is called by `0x0050CDE0`; `0x00264F90` is called by
  `0x00357450`, `0x0050CDE0`; `0x0032A8A0` is called by `0x0034E0B0`; `0x0032E400` is called by `0x0050DF70`; those functions are
  documented on [archades scripts](../Story-Events-And-Hunts/archades-scripts.md).
- `0x0050CDE0` pops two ints, a and then b, and hands `0x00264F10(a)`, `0x00264F40(a)` and
  `0x00264F90(a)`, each with b, to `0x0016D6A0`, which only returns; the verb
  `debug_replacegmap` therefore changes nothing (`0x0050CDEA`-`0x0050CE36`).
- Story event quest hunt: `0x00314910` is called by `0x001ED240`; those functions are documented on
  [model effects and motion commands](../Graphics/model-effects-and-motion-commands.md).
- Story event quest hunt: `0x0029C530` calls `0x0032A8A0`; `0x0032A8A0` calls `0x00377970`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md),
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md).
- UI: `0x00264F90` is called by `0x0029C530`; `0x00314910` is called by `0x0029C530`; `0x0032A8A0` is called by `0x00281AE0`,
  `0x0029C530`; `0x003778B0` is called by `0x0029C530`; `0x00377B60` is called by `0x0029C530`; those functions are documented
  on [menu screens](../Menus-And-HUD/menu-screens.md), [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md).
