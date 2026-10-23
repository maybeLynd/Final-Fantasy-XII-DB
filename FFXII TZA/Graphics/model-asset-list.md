---
title: "Model asset list: every model the game can bind, with its model file, motion lanes, remastered parts and the tables and scripts that use it"
kind: "reference"
category: "Graphics"
addresses: "0x002ED6F0, 0x002E6EB0, 0x002E6FD1, 0x00320170, 0x003202F0, 0x001BB2B0, 0x002EAD50, 0x0017F000, 0x0032E620"
---

## What it lists

`model-asset-list.tsv` holds one line for each model a bound id can name: 1,084 models over eleven letter
classes. For each it gives the files the game loads for that model and the tables and scripts that name it. A bound
id is a letter class in bits 16-23 and a number in bits 0-15 ([Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md));
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

### How it is built

`Database/Tools/catalogues/model_assets.py`, on the path arrays of [Asset paths](../Game-Files-And-Data-Tables/asset-paths.md)
and the archive reader `vbflib.py`:

1. **The model file.** `0x002ED6F0` turns a letter into a resource kind, the number into a file index and gives the
   model's lane count (the table above). The kind's path array names the `.cm` at that index
   ([Model files](model-files-cm-ca.md)).
2. **The lane files.** The lane loader `0x002E6EB0` files lane *k* as index + 1 + *k*. For class `m` it files lane 0 as
   index + 1, lanes 1-15 all as index + 2, and lanes from 16 as index + 1 + (*k* − 14) (`0x002E6FD1`-`0x002E6FF6`), so a
   monster has one motion set where a character has fifteen.
3. **The remastered parts.** `0x001BB2B0` names a model's `.ah` list from its `.cm` path: the text after
   `PS2Data\obj_finish\in\`, less `.cm`, with `\` turned into `/`, as `./GameData/D3D11/ArtData/chr/<name>_d3d11.ah`.
   The binding's load `0x002EAD50` requests it through `0x0017F000` before the model's own file
   ([Prefetch and asset-header manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)).
4. **The remastered files.** The decoder reads each list from the archive and counts its `.dae.phyre` and
   `.dds.phyre` paths.
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
from `0x003202F0`, which the main-hand weapon's motion class picks ([Weapon motion list](../Battle-Actions/weapon-motion-list.md)):

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

### Shipped data

| Fact | Value |
|---|---|
| models | 1,084; their `.cm` ships for 1,066, the count [Model files](model-files-cm-ca.md) gives |
| `.cm` named but not shipped | 18, among them `c1010` and `c1014`-`c1018`, `n1037`, `g0054` and `w2123` |
| remastered `.ah` lists | 1,050 models, 4 of them with no shipped `.cm`; each list names one `.dae.phyre` mesh, and 8,418 textures in all |
| shipped `.cm` with no `.ah` | 20: 18 weapons and the NPCs `n1027` and `n1174` |
| lane files that ship | 1,195 on 449 models |
| further motions | 1,954 of kind 30's 1,969 files, on 344 models |
| sounds | 673 models name SE blocks (252 weapons in slot 0; characters, monsters, NPCs and summons in slots 1 and 2), 217 distinct blocks; 39 name a battle-voice bank. A battle unit's definition can name its own voice bank, which takes precedence ([Bestiary](../Enemy-Spawning/bestiary.md) `voice_bank`) |
| users | 347 models in the bestiary, 28 in the party table, 482 in script manifests; 342 in none of the three |

### Checks

- Every `.cm` in the archive's `obj_finish` folders is reached by exactly one bound id (1,066 of 1,066).
- Rows compared with their sources: `c0` is `c1004` and the party table's Vaan; `m1`, `m1015`, is the bestiary's
  Wolf, Wary Wolf and Alpha Wolf (bound id `0x006D0001`); `n4`, `n1020`, has bound id `0x006E0004`, the value the
  bestiary gives its rows.
- Two runs over the same files give byte-identical output.

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
| `voice_bank` | the battle-voice bank the row names, `shoutNN`; empty for none |
| `bestiary`, `party`, `script_containers` | the bestiary names, party table rows and number of script manifests that use the model |
| `explanation` | a one-line summary |

## Related

- [Model files (.cm, .ca): the @FRP container and its FCP, FDM, FOR, FTE, FCT and FTR entries](model-files-cm-ca.md)
- [Asset paths: every file the game asks for by resource kind and id, with its path, size and whether the archive ships it](../Game-Files-And-Data-Tables/asset-paths.md)
- [Prefetch and asset-header manifests: the text lists that preload files into the file cache, and the .ah lists that name the parts of a model, map or font](../Game-Files-And-Data-Tables/prefetch-manifests.md)
- [Weapon motion list: the animation set each weapon's motion class gives a battle unit, from the WepJob_Matrix table](../Battle-Actions/weapon-motion-list.md)
