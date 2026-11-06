---
title: "Model asset list: every model the game can bind, with its model file, motion lanes, remastered parts and the tables and scripts that use it"
kind: "reference"
category: "Graphics"
addresses: "0x002ED6F0, 0x002E6EB0, 0x002E6FD1, 0x00320170, 0x003202F0, 0x001BB2B0, 0x002EAD50, 0x0017F000, 0x0032E620"
---

## What it lists

[`model-asset-list.tsv`](model-asset-list.tsv) holds one line for each model a bound id can name: 1,084 models over eleven letter
classes. For each it gives the files the game loads for that model and the tables and scripts that name it. A bound
id is a letter class in the bits under mask `0xFF0000` and a number in the bits under mask `0xFFFF` ([Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md));
`c0` (`0x00630000`) is Vaan's model, `chara/c10/c1004/c1004`.

| Class | Models | Folder | Kind | Index | Lanes |
|---|---:|---|---:|---|---:|
| `b` | 18 | `bg_obj` | 22 | n × 2 | 1 |
| `C` | 48 | `high` (`hc*`) | 15 | n | 0 |
| `c` | 23 | `chara` | 14 | n × 25 | 24 |
| `g` | 104 | `gadget` | 13 | n × 2 | 1 |
| `m` | 254 | `monster` | 34 | n × 11 | 10 |
| `N` | 87 | `high` (`hn*`) | 20 | n | 0 |
| `n` | 175 | `npc` | 19 | n × 25 | 24 |
| `S` | 5 | `high` (`hs*`) | 24 | n | 0 |
| `s` | 26 | `summon` | 23 | n × 25 | 24 |
| `t` | 17 | `treasure` | 25 | n | 0 |
| `w` | 327 | `weapon` | 16 | n | 0 |

Class `M` maps to kind `0x12`, a runtime slot with no path array, so it names no shipped model.

### Where the values come from

The columns come from the path arrays of [Asset paths](../Game-Files-And-Data-Tables/asset-paths.md) and the
archive index:

1. **The model file.** `0x002ED6F0` turns a letter into a resource kind, the number into a file index and gives the
   model's lane count (the table above). The kind's path array names the `.cm` at that index
   ([Model files](model-files-cm-ca.md)).
2. **The lane files.** The lane loader `0x002E6EB0` files lane *k* as index + 1 + *k* (index + `0x43` + *k* for kind
   1, which no class of the eleven maps to; `0x002E6F99`-`0x002E6FA2`). For class `m` it files lane 0 as
   index + 1, lanes 1-15 all as index + 2, and lanes from 16 as index + 1 + (*k* − 14) (`0x002E6FD1`-`0x002E6FF6`), so a
   monster has one motion set where a character has fifteen.
3. **The remastered parts.** `0x001BB2B0` names a model's `.ah` list from its `.cm` path: the text after
   `PS2Data\obj_finish\in\`, less `.cm`, with `\` turned into `/`, as `./GameData/D3D11/ArtData/chr/<name>_d3d11.ah`.
   The binding's load `0x002EAD50` requests it through `0x0017F000` before the model's own file
   ([Prefetch and asset-header manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)).
   - `0x0017F000` requests nothing and returns 0 while the object at `0x01F81240` is null (`0x0017F010`).
4. **The remastered files.** `pc_meshes` and `pc_textures` count the list's `.dae.phyre` and `.dds.phyre` paths.
5. **Further motions.** Kind 30's motion files are listed with the model whose `.cm` folder holds them.
6. **The sounds.** Row *n* of the model's letter table `charseinfo_<letter>.bin`, which `0x002ED950` returns, names
   three SE blocks and a battle-voice bank ([Character sound tables](../Game-Files-And-Data-Tables/character-se-tables-chse.md)).
   `0x002E60F0` turns a block id into a kind-32 `.seb` and its `.win.sab`, and the bank number names `shoutNN`
   ([Sound banks](../Sound-And-Music/sound-banks.md)).
7. **The users,** joined by bound id: [Bestiary](../Enemy-Spawning/bestiary.md) `model_id`,
   [Party table](../Party/party-table.md) `model`, and the script manifests of
   [Actor manifest](../EBP-Script-Files/ebp-actor-manifest.md) (`ebp-actor-manifest-ids.tsv`).

### The motion lanes

A 24-lane model's lane files follow its `.cm` in this order. `0x00320170` gives a unit's lane as its animation set
from `0x003202F0`, which the main-hand weapon's motion class picks unless an enemy record's definition row
byte `+0x13` or the bare-handed Brawler row gives it (`0x0032031F`-`0x00320389`)
([Weapon motion list](../Battle-Actions/weapon-motion-list.md)), and an actor that is one of the four
`0x00263750` roster actors its set from `0x00320230` (`0x003201B0`-`0x0032021C`); without battle flag `0x02089340` bit
`0x10` the lane is −1 (`0x0032018F`, `0x0032030B`):

| Lane | File | Animation set: the equipment categories of its weapons |
|---:|---|---|
| 0 | `_00` | set 0, no shipped weapon |
| 1 | `_10` | Unarmed |
| 2 | `_11` | bare hands with Brawler (augment 9) |
| 3 | `_20` | Sword (1H) |
| 4 | `_21` | Dagger (1H) |
| 5 | `_22` | Hand-bomb (2H) |
| 6 | `_23` | Ninja Sword (2H) |
| 7 | `_24` | Axe (1H), Hammer (1H) |
| 8 | `_25` | Mace (1H), Measure (1H) |
| 9 | `_30` | Rod (2H), Staff (2H) |
| 10 | `_31` | Pole (2H) |
| 11 | `_32` | Spear (2H) |
| 12 | `_40` | Sword (2H) |
| 13 | `_41` | Katana (2H) |
| 14 | `_50` | Bow (2H) |
| 15 | `_60` | Crossbow (2H), Gun (2H) |
| 16-21 | `_e1`-`_e6` | |
| 22, 23 | `_t1`, `_t2` | |

The motion class belongs to the weapon, so a few weapons share another category's set: four maces and a gun use
set 3, four spears set 9, a pole set 12 and a gun set 1 ([Equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md)).
A 10-lane monster's files are `_00`, `_10`, `_e1`-`_e6`, `_t1` and `_t2`, in that order.

### The action motions (kind 30)

Kind 30's path array `0x01ED7740` names 2,324 `.ca` files, each `<model>_<lane>_<number>.ca`, and 1,969 of them ship.
They are the motions a unit plays for an action, outside its lanes.

The battle code asks the skill-motion cache for a
model, a motion number and a weapon class (`0x00325B40`, [Character render records](character-render-records.md)). The
cache sizes the file with `0x003DC8D0` and reads it with `0x003DC5B0`, and both take the file from `0x003DCA30`. That
function always gives kind 30 (`0x003DCA49`) and looks the model and motion up in three tables, in order
([Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)):

| Table | Records | Files named | Of them shipped |
|---|---:|---:|---:|
| `pc_skillmotion.bin` (global) | 33 | 33 | 18 |
| the areas' `.ard` slot 7 | 1,773 in 136 areas | 1,043 | 1,025 |
| the script containers' section 19, slot 7 | 2,116 in 271 containers | 1,161 | 1,130 |

`0x003DCA30` is the only code that gives kind 30. Every other read request passes another kind
([File requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md)), and
`0x003DCA49` is the only store of 30 as a kind. So a kind 30 file is read only when one of the three tables names its
index. [`model-asset-list-action-motions.tsv`](model-asset-list-action-motions.tsv) gives, for each of the 2,324 ids,
the tables, areas, script containers, motions, weapon classes and models that name it:

| Ids | Count |
|---|---:|
| shipped, named by one table | 631 |
| shipped, named by two tables | 771 |
| shipped, named by no table, so never read | 567: 495 NPC files (`n10` 134, `n11` 276, `n12` 85), 63 monster files (`m10` 20, `m11` 21, `m12` 22) and 9 summon files |
| not shipped, named by a table | 47; every size table gives them −1, and the cache refuses a failed size (`0x003DCD00` returns `0x80000001`) |
| not shipped and named by no table | 308 |

### Columns of model-asset-list-action-motions.tsv

| Column | Holds |
|---|---|
| `global_records` | how many records of `pc_skillmotion.bin` name the id: 1 for 33 ids, 0 for the rest; the column sums to the table's 33 records |
| `area_records` | how many records of the areas' `.ard` slot 7 name the id, 0 to 9; the areas are listed in `areas`, and the column sums to 1,773 |
| `script_records` | how many records of the script containers' section 19, slot 7, name the id, 0 to 7; the containers are listed in `scripts`, and the column sums to 2,116 |

One script container's section 19 is not an area block: `evt_t0020.ebp` holds 8 zero bytes and then `03 21 21 21`
where the `FF12AR03` tag would be.

Replacing a file:

- The tables pick a file by index. A replaced file changes the motion everywhere its index is named; the table lists
  those areas and containers. To change the motion in one area only, point that area's record at another index.
- The file is read whole, with the size the language's `.fst` gives (`0x0032E400`, from `0x003DC8D0`), so a resized file
  needs its new size in every `.fst`. `0x003DC8D0` keeps the size for a model, motion and weapon class in one of
  sixteen entries and does not clear them.
- The cache counts 32 KiB units, `(size + 0x7FFF) >> 15` (`0x003DCE13`-`0x003DCE22`). It files a new entry only while
  the units of the entries in use plus the new ones stay at 4 or below (`0x003DCE38`-`0x003DCE3E`), and returns 0
  otherwise. A file larger than 131,072 bytes therefore never fits; the largest shipped one is 130,208 bytes.
- An index no table names is never read, so a file added at such an index needs a table record that names it.

### Shipped data

| Fact | Value |
|---|---|
| models | 1,084; their `.cm` ships for 1,066, the count [Model files](model-files-cm-ca.md) gives |
| `.cm` named but not shipped | 18, among them `c1010` and `c1014`-`c1018`, `n1037`, `g0054` and `w2123` |
| a model whose `.cm` is not shipped | all twelve size tables give its id −1 (18 of 18). The binding's load `0x002EAD50` sizes the file with `0x0032E400` and requests it with that size (`0x002EADEA`, `0x002EAE08`), but a binding of such a model never reaches it: the request pump `0x002E6700` gets the same −1 first (`0x002E6776`) and, for a size of 0 or less, takes no buffer and files no load (`0x002E6789`-`0x002E678B`), so the entry moves to the live list with `+0x10` = 0 and no completion runs for it. The read issuer refuses a −1 request and the queue reports it delivered with nothing read ([File size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md)); the binding files no such request. No table or manifest names those 18 ids |
| a motion file that is not shipped | 7,198 path-array entries name a `.ca` the archive lacks: 6,843 lanes and 355 of kind 30, and all twelve size tables give each −1. The lane loader `0x002E6EB0` takes a lane's size from `0x002E9920`, which returns `0x0032E400`'s answer, and skips the lane with no buffer and no request when it is not above 0 (`0x002E6F43`-`0x002E6F45`) |
| every shipped `.cm` and `.ca` is named | each `.cm` by its bound id's kind (1,066 of 1,066); 1,195 `.ca` by a lane of their model and the other 1,969 by kind 30's array (3,164 of 3,164) |
| remastered `.ah` lists | 1,050 models, 4 of them with no shipped `.cm`; each list names one `.dae.phyre` mesh, and 8,418 textures in all |
| `chr/` lists no model's path builds | 6: the `mws/` lists of `m1022`, `m1025`, `m1084` and `m1085`, each naming the same files as the model's own list, and the heads `hn1021_01` and `hn1081_01` ([Prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md) [`prefetch-manifests-ah-lists-chr.tsv`](../Game-Files-And-Data-Tables/prefetch-manifests-ah-lists-chr.tsv)) |
| heads `hn1021_01`, `hn1081_01` | each list names one mesh with face joints (`j_kao`, `j_eye_r`, `j_mayu_r`, `j_ago`) and two face textures (`f0019_face` and `f0019_etc`; `f0062_face` and `f0062_hair`). The 26 names of `hn1021_01.dae.phyre` are all in the bound `hn1021_02` (model N12), which adds 24 arm and hand joints and imports the same files and one more texture. No model's path names `hn1021_01` or `hn1081_01`, so no binding requests their lists, and in the four `.ah` token tables each head's mesh is named by its own list alone |
| mesh imports | each mesh names the shader variants and base textures it binds as asset imports: 2,280 variant and 1,969 texture imports in the 1,053 `chr/` mesh files ([PhyreEngine asset files](../PhyreEngine/phyre-asset-files.md) [`phyre-asset-files-meshes-chr.tsv`](../PhyreEngine/phyre-asset-files-meshes-chr.tsv) `imports`) |
| shipped `.cm` with no `.ah` | 20: 18 weapons and the NPCs `n1027` and `n1174` |
| lane files that ship | 1,195 on 449 models |
| further motions | 1,954 of kind 30's 1,969 files, on 344 models |
| sounds | 673 models name SE blocks (252 weapons in slot 0; characters, monsters, NPCs and summons in slots 1 and 2), 217 distinct blocks; 39 name a battle-voice bank. A battle unit's definition can name its own voice bank, which takes precedence ([Bestiary](../Enemy-Spawning/bestiary.md) `voice_bank`) |
| users | 347 models in the bestiary, 28 in the party table, 482 in script manifests; 342 in none of the three |

## Columns

| Column | Meaning |
|---|---|
| `bound_id`, `class`, `number` | the bound id and its letter class and number |
| `name` | the model's name: its `.cm` path under `obj_finish/in/`, without `.cm` |
| `kind`, `index` | the resource kind and file index `0x002ED6F0` gives |
| `cm`, `cm_bytes` | the `.cm` path and its archived size; "(not shipped)" when the archive lacks it |
| `lanes`, `lane_files` | the lane count, and each lane file that ships with the lane or lanes that load it |
| `extra_motions` | the number of kind 30 motion files in the model's folder |
| `ah`, `pc_meshes`, `pc_textures` | the remastered `.ah` list, its mesh and its number of textures; empty when the archive has no list |
| `se_blocks` | the SE blocks of the model's `charseinfo` row, slot by slot, as the `.seb` files they load: slot 0 is sound group 0, played through the weapon model a character holds; slot 1 group 1, the footsteps; slot 2 group 2 ([Animation sounds](../Sound-And-Music/animation-sounds.md)) |
| `voice_bank` | the battle-voice bank the row names, `shoutNN`; empty when the row names no bank |
| `bestiary`, `party`, `script_containers` | the bestiary names, party table rows and number of script manifests that use the model |
| `explanation` | a one-line summary |

## Related

- [Model files (.cm, .ca): the @FRP container and its FCP, FDM, FOR, FTE, FCT and FTR entries](model-files-cm-ca.md)
- [Asset paths: every file the game asks for by resource kind and id, with its path, size and whether the archive ships it](../Game-Files-And-Data-Tables/asset-paths.md)
- [Prefetch and asset-header manifests: the text lists that preload files into the file cache, and the .ah lists that name the parts of a model, map or font](../Game-Files-And-Data-Tables/prefetch-manifests.md)
- [Weapon motion list: the animation set each weapon's motion class gives a battle unit, from the WepJob_Matrix table](../Battle-Actions/weapon-motion-list.md)
