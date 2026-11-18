[Home](../../README.md) / [Graphics](README.md) / Model asset list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Model asset list: every model the game can bind, with its model file, motion lanes, remastered parts and the tables and scripts that use it | reference | Graphics | Character models / Model Files | All 1,084 models the eleven bound-id letter classes name: each model's bound id, its PS2-era .cm file and size, the motion lane files that ship and which animation set loads each, its further motion files, the remastered .ah list with its mesh and texture count, and the bestiary definitions, party table rows and script manifests that use it; how 0x002ED6F0, the lane loader 0x002E6EB0 and 0x001BB2B0 turn a bound id into those files. | 0x002ED6F0, 0x002E6EB0, 0x002E6FD1, 0x00320170, 0x003202F0, 0x001BB2B0, 0x002EAD50, 0x0017F000, 0x0032E620 |

## What it lists

[`model-asset-list.tsv`](model-asset-list.tsv) holds one line for each model a bound id can name: 1,084 models over eleven letter
classes. For each it gives the files the game loads for that model and the tables and scripts that name it. A bound
id is a letter class in the bits under mask `0xFF0000` and a number in the bits under mask `0xFFFF` ([Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md));
`c0`¹ is Vaan's model, `chara/c10/c1004/c1004`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00630000` |

</details>

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

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **The model file.** `0x002ED6F0` turns a letter into a resource kind, the number into a file index and gives the model's lane count (the table above). The kind's path array names the `.cm` at that index ([Model files](model-files-cm-ca.md)). |   |
| 2 | **The lane files.** The lane loader `0x002E6EB0` files lane *k* as index + 1 + *k* (index + `0x43` + *k* for kind 1, which no class of the eleven maps to; `0x002E6F99`-`0x002E6FA2`). For class `m` it files lane 0 as index + 1, lanes 1-15 all as index + 2, and lanes from 16 as index + 1 + (*k* − 14), so a monster has one motion set where a character has fifteen. | `0x002E6FD1`-`0x002E6FF6` |

   For each lane bit of the record's `+0x28` whose buffer slot `+0x60 + 4k` is 0, it
   takes the size from `0x002E9920`, a buffer handle from `0x0036B160(size)`, stored in the
   slot, and calls `0x0032E620(kind, file, 0x0036A000(handle), size, request)`; the request
   holds the record's word `+0x20` shifted left 16 with the lane, and the callback
   `0x002E4E50`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6F35`-`0x002E700C` |

</details>

   A lane that got its request, or whose slot was already set, has its bit set in
   `+0x34`; every lane tried has its bit cleared in `+0x28`. A handle of 0 skips the lane
   as a size not above 0 does¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6EED`-`0x002E6EF6`, `0x002E6F52`-`0x002E6F57`, `0x002E7027`-`0x002E703D` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 3 | **The remastered parts.** `0x001BB2B0` names a model's `.ah` list from its `.cm` path: the text after `PS2Data\obj_finish\in\`, less `.cm`, with `\` turned into `/`, as `./GameData/D3D11/ArtData/chr/<name>_d3d11.ah`. The binding's load `0x002EAD50` requests it through `0x0017F000` before the model's own file ([Prefetch and asset-header manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)).<br>• `0x0017F000` requests nothing and returns 0 while the object at `0x01F81240` is null. | `0x0017F010` |
| 4 | **The remastered files.** `pc_meshes` and `pc_textures` count the list's `.dae.phyre` and `.dds.phyre` paths. |   |
| 5 | **Further motions.** Kind 30's motion files are listed with the model whose `.cm` folder holds them. |   |
| 6 | **The sounds.** Row *n* of the model's letter table `charseinfo_<letter>.bin`, which `0x002ED950` returns, names three SE blocks and a battle-voice bank ([Character sound tables](../Game-Files-And-Data-Tables/character-se-tables-chse.md)). `0x002E60F0` turns a block id into a kind-32 `.seb` and its `.win.sab`, and the bank number names `shoutNN` ([Sound banks](../Sound-And-Music/sound-banks.md)). |   |
| 7 | **The users,** joined by bound id: [Bestiary](../Enemy-Spawning/bestiary.md) `model_id`, [Party table](../Party/party-table.md) `model`, and the script manifests of [Actor manifest](../EBP-Script-Files/ebp-actor-manifest.md) (`ebp-actor-manifest-ids.tsv`). |   |

### The motion lanes

A 24-lane model's lane files follow its `.cm` in this order. `0x00320170` gives a unit's lane as its animation set
from `0x003202F0`, which the main-hand weapon's motion class picks unless an enemy record's definition row
byte `+0x13` or the bare-handed Brawler row gives it¹
([Weapon motion list](../Battle-Actions/weapon-motion-list.md)), and an actor that is one of the four
`0x00263750` roster actors its set from `0x00320230`²; without battle flag `0x02089340` bit
`0x10` the lane is −1³:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032031F`-`0x00320389` |
| ² | `0x003201B0`-`0x0032021C` |
| ³ | `0x0032018F`, `0x0032030B` |

</details>

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
function always gives kind 30¹ and looks the model and motion up in three tables, in order
([Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)):

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DCA49` |

</details>

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

`evt_t0020.ebp` is not a script container: it is a bare version-7 script image without the `EBP2` header, so it has no
section 19 and no row counts it.

Replacing a file:

- The tables pick a file by index. A replaced file changes the motion everywhere its index is named; the table lists
  those areas and containers. To change the motion in one area only, point that area's record at another index.
- The file is read whole, with the size the language's `.fst` gives (`0x0032E400`, from `0x003DC8D0`), so a resized file
  needs its new size in every `.fst`. `0x003DC8D0` keeps the size for a model, motion and weapon class in one of
  sixteen entries and does not clear them.
- The cache counts 32 KiB units, `(size + 0x7FFF) >> 15`¹. It files a new entry only while
  the units of the entries in use plus the new ones stay at 4 or below², and returns 0
  otherwise. A file larger than 131,072 bytes therefore never fits; the largest shipped one is 130,208 bytes.
- An index no table names is never read, so a file added at such an index needs a table record that names it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DCE13`-`0x003DCE22` |
| ² | `0x003DCE38`-`0x003DCE3E` |

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 61 calls with 17 other topics</summary>

**Characters and objects** (explained on [party control modes](../Engine-Core/party-control-modes.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [frame update order](../Engine-Core/frame-update-order.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263750`](model-asset-list.md) | is called by | [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots)<br>[`0x0035A8D0`](../Scripts-And-Script-Commands/verb-table.md) (on verb table) |
| [`0x00320170`](model-asset-list.md) | calls | [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x00320170`](model-asset-list.md) | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x0032E400`](effect-file-list.md) (on effect file list) | is called by | [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |
| [`0x0032E620`](effect-file-list.md) (on effect file list) | is called by | [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container) |

**Sound and music** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E60F0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) (on character se tables chse) | calls | [`0x003A1650`](../Sound-And-Music/sound-banks.md) (on sound banks) |

**Battle actions** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00325B40`](model-asset-list.md) | is called by | [`0x0030CBE0`](effect-file-list.md) (on effect file list) |

**Damage and battle formulas** (explained on [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003202F0`](model-asset-list.md) | calls | [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log) |

**Gameplay** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00320230`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list) | calls | [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) |

**Controls and input** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263750`](model-asset-list.md) | is called by | [`0x00226BE0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock) |
| [`0x0032E620`](effect-file-list.md) (on effect file list) | is called by | [`0x00291C80`](effect-file-list.md) (on effect file list) |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263750`](model-asset-list.md) | is called by | [`0x0034A940`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0037CF00`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0037D000`](../Party/party-slots.md) (on party slots) |

**Party** (explained on [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party control modes](../Engine-Core/party-control-modes.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263750`](model-asset-list.md) | is called by | [`0x003261D0`](../Party/party-members.md) Party configuration: reconcile roster from current selectors (on party members)<br>[`0x00326500`](../Party/party-leader.md) Party focus: select and request default actor (on party leader)<br>[`0x003272F0`](../Party/party-leader.md) (on party leader)<br>[`0x003273D0`](../Party/party-members.md) Party configuration: set selectors and reconcile roster (on party members)<br>[`0x0034D4E0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x00350CD0`](../Party/party-members.md) (on party members) |
| [`0x00320170`](model-asset-list.md) | calls | [`0x00263750`](model-asset-list.md) |

**Saving, loading and settings** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E620`](effect-file-list.md) (on effect file list) | is called by | [`0x002EF300`](../Saving-Loading-And-Settings/save-file-format.md) (on save file format) |

**Scripts and script commands** (explained on [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263750`](model-asset-list.md) | is called by | [`0x003415D0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00341CB0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00342250`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00342910`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x00342EC0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003446D0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00344740`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00346EB0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x003473E0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00347970`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x0034AF80`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list)<br>[`0x0034DF40`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list) |
| [`0x00263750`](model-asset-list.md) | is also called by | [`0x0034F060`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x0034F890`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x00350050`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003507B0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003509E0`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list)<br>[`0x00352190`](../Story-Events-And-Hunts/mt-bur-omisace-scripts.md) (on mt bur omisace scripts)<br>[`0x00352FA0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003537D0`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list) |
| [`0x002ED6F0`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings) | is called by | [`0x003580C0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) |
| [`0x0032E400`](effect-file-list.md) (on effect file list) | is called by | [`0x0050DF70`](../Game-Files-And-Data-Tables/resource-lifecycle.md) (on resource lifecycle) |
| [`0x0032E620`](effect-file-list.md) (on effect file list) | is called by | [`0x0050DFE0`](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md) (on file requests and the read queue) |

**World, areas and travel** (explained on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [frame update order](../Engine-Core/frame-update-order.md), [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md), [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](effect-file-list.md) (on effect file list) | is called by | [`0x00378540`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) |
| [`0x0032E620`](effect-file-list.md) (on effect file list) | is called by | [`0x00378540`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) |
| [`0x00325B40`](model-asset-list.md) | calls | [`0x00313F60`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) |
| [`0x0032E400`](effect-file-list.md) (on effect file list) | is called by | [`0x00268750`](../Game-Files-And-Data-Tables/ps2data-bin-families.md) Map ref: begin load resources (on ps2data bin families)<br>[`0x003319D0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x00378030`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x00379A10`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list)<br>[`0x003EA820`](../Game-Files-And-Data-Tables/ard-area-battle-data.md) Area ard: load or unload field resource (on ard area battle data) |
| [`0x0032E620`](effect-file-list.md) (on effect file list) | is called by | [`0x00268750`](../Game-Files-And-Data-Tables/ps2data-bin-families.md) Map ref: begin load resources (on ps2data bin families)<br>[`0x00378030`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x003EA820`](../Game-Files-And-Data-Tables/ard-area-battle-data.md) Area ard: load or unload field resource (on ard area battle data) |

</details>
