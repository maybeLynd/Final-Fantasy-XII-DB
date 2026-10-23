---
title: "Asset paths: every file the game asks for by resource kind and id, with its path, size and whether the archive ships it"
kind: "reference"
category: "Game files and data tables"
addresses: "0x002DF9A0, 0x0215F000, 0x0032E620, 0x002DF960, 0x002DF980, 0x002ED6F0, 0x01ED7630, 0x01ED7740, 0x001F4340"
---

## What it lists

`asset-paths.tsv` holds one line for each entry of the path arrays the executable installs for the US build: every
file the game can request by a resource kind and an id, the way `0x0032E620(kind, index, ...)` requests it
([File requests](file-requests-and-the-read-queue.md)). Each line gives the archive path the game uses for that
kind and id, the size the US size table gives it ([File size tables](file-size-tables-fst.md)), and whether the
shipped archive holds the file ([Bigfile archive](bigfile-archive.md)).

Most of the game's files go through these arrays: area files, zone and event scripts, map packs, menu files, every
PS2-era model and motion file, effect files, sound banks, voice files and movies. The remastered `.phyre` art
under `gamedata/` is reached by name instead, through the `.ah` lists
([Prefetch and asset-header manifests](prefetch-manifests.md)), and is not in this table.

### Where the values come from

The columns come from the executable's path arrays, the US size table and the archive index:

1. **The arrays.** `ResourcePath_Init` `0x002DF9A0` stores one array pointer per kind at `0x0215F000` + kind × 8, then
   switches on the language id − 1 and replaces the language's own arrays; the arrays listed are those the US arm
   installs.
2. **The entries.** An array is a run of 8-byte pointers to NUL-terminated paths, or 0; id *n* is entry *n*. Six
   kinds (3, 17, 18, 29, 36 and 40) point at runtime slots near `0x0215F000` instead of an array and have no entries.
3. **Where an array ends.** The arrays sit back to back in `.rdata`, so each one ends where the next array that any
   language installs begins. Past that point an id is listed only when the size table sizes it, with no path
   (below).
4. **The size.** `0x002DF960(kind, id)` returns the dword at `kind × 5000 + id` of the language's
   `FileSizeTable_<lang>.fst`; `0xFFFFFFFF` is no file. The size column is the US table's value.
5. **Shipping.** The path, less its `PS2Data\` prefix and in lower case, is looked up among the 89,414 names of
   the shipped `FFXII_TZA.vbf` index that `0x001F4340` reads; the archive record's size is
   written beside it.

### Shipped data

| Fact | Value |
|---|---|
| entries | 21,834 over 35 kinds with arrays; 21,812 name a path |
| sized by the US table | 10,521, the table's own count of entries that are not `0xFFFFFFFF` |
| sized and shipped | 10,499: every sized entry whose array names a path is in the archive |
| sized with no path | 22, all kind 1 (below) |
| named but not sized | 11,313: paths the game could build that no US file answers, such as model lane slots with no motion file |
| size differs from the archive | 144 `.cm` model files (kind 34: 82, 19: 27, 23: 26, 13: 9); the size table's value is the larger in all 144 |

Per kind, for the US build:

| Kind | Named | Sized | Shipped | First shipped file |
|---:|---:|---:|---:|---|
| 0 | 12 | 1 | 1 | `cdi\in\system.cnf` |
| 1 | 7 | 24 | 2 | `sound\se\map\position_map\spp\env\env99.spp` |
| 2 | 82 | 81 | 81 | `image\FF12\test_battle\in\BinaryFile\WepJob_Matrix.bin` |
| 4 | 550 | 550 | 550 | `plan_master\map_ctrl\ous01\ous0100\bin\ous0100.mpk` |
| 5 | 2,127 | 896 | 896 | `plan_master\us\plan_map\ttl_a\ttl_a01\global\ttl_a01.ebp` |
| 6 | 42 | 0 | 0 | |
| 7 | 865 | 536 | 536 | `image\FF12\myoshiok\in\Bin_Menu\fontcolor.bin` |
| 8 | 1,316 | 1,080 | 1,080 | `plan_master\us\event\nal_a\nal_a0100\nal_a0100.ebp` |
| 9 | 29 | 26 | 26 | `image\ff12\common\test_map_ref.bin` |
| 10 | 3 | 2 | 2 | `effect_finish\jp\common\c_all.efx` |
| 11 | 512 | 366 | 366 | `effect_finish\jp\magic\m0000.efx` |
| 12 | 894 | 532 | 532 | `effect_finish\jp\event\e0000.efx` |
| 13 | 208 | 103 | 103 | `obj_finish\in\gadget\g0001.cm` |
| 14 | 575 | 143 | 143 | `obj_finish\in\chara\c10\c1004\c1004.cm` |
| 15 | 48 | 47 | 47 | `obj_finish\in\high\c10\c1004\hc1004_01.cm` |
| 16 | 327 | 326 | 326 | `obj_finish\in\weapon\w2002.cm` |
| 19 | 4,375 | 691 | 691 | `obj_finish\in\npc\n10\n1059\n1059.cm` |
| 20 | 87 | 80 | 80 | `obj_finish\in\high\n10\n1018\hn1018_11.cm` |
| 21 | 430 | 166 | 166 | `plan_master\in\plan_map\nal_a\area\nal_a.ard` |
| 22 | 36 | 17 | 17 | `obj_finish\in\bg_obj\b00\b0001\b0001.cm` |
| 23 | 650 | 78 | 78 | `obj_finish\in\summon\s0002\s0002.cm` |
| 24 | 5 | 5 | 5 | `obj_finish\in\high\s00\s0003\hs0003_01.cm` |
| 25 | 17 | 17 | 17 | `obj_finish\in\treasure\t0004.cm` |
| 26 | 321 | 166 | 166 | `plan_master\in\plan_map\nal_a\area\nal_a.nmb` |
| 27 | 256 | 0 | 0 | |
| 28 | 90 | 43 | 43 | `movie_finish\us\OPN.mh` |
| 30 | 2,324 | 1,969 | 1,969 | `obj_finish\in\chara\c10\c1004\c1004_10_3000.ca` |
| 31 | 256 | 0 | 0 | |
| 32 | 608 | 248 | 248 | `sound\se\block\se000.seb` |
| 33 | 64 | 64 | 64 | `sound\shout\us\shout00\shout00.win.sab` |
| 34 | 2,794 | 754 | 754 | `obj_finish\in\monster\m10\m1002\m1002.cm` |
| 35 | 10 | 0 | 0 | |
| 37 | 1,316 | 1,080 | 1,080 | `plan_master\in\event\nal_a\nal_a0100\nal_a0100.ebp` |
| 38 | 512 | 366 | 366 | `effect_finish\jp\magic\m0000.efx` |
| 39 | 64 | 64 | 64 | `sound\shout\jp\shout00\shout00.win.sab` |

The model kinds (13 to 16, 19 to 25 and 34) hold each model's `.cm` followed by its motion lane files, in blocks
whose size is the model class's index multiplier; [Model asset list](../Graphics/model-asset-list.md)
lists every model with its files.

### The kind 1 array

The US kind 1 array `0x01ED7630` names ids 4 to 8 (the `wave0480`-`wave0483` and `wave0000` banks), 24
(`env99.spp`) and 32 (`planmapname.bin`), and ends at id 34, where the kind 30 array `0x01ED7740` begins. The US
size table sizes 24 kind 1 ids: 24 and 32, whose files ship; 1 and 2, which the array leaves null; and the 20 ids
109 to 132, which lie past its end, so the US array names no kind 1 file for them.

`0x002ED6F0` gives kind 1 to every bound id whose letter is none of its twelve (`0x002ED840`: index = number, one
lane); `0x002E98F0` adds `0x33` to that index and the lane loader `0x002E6EB0` adds `0x43` (`0x002E6F99`-`0x002E6FA2`,
[Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)). The bestiary, the party table and
the actor manifests name only the twelve letters, so no shipped bound id reaches kind 1.

## Columns

| Column | Meaning |
|---|---|
| `kind`, `id` | the resource kind and id, as `0x0032E620` takes them |
| `path` | the path the kind's array names, as the executable writes it; empty for a null entry or an id past the array's end |
| `size` | the US size table's value in bytes; empty for `0xFFFFFFFF` |
| `ships` | 1 when the archive index names the file, 0 otherwise |
| `archive_size`, `archive_name` | the archive record's size and the name its index gives the file |

## Related

- [File size tables: the per-language .fst that sizes every file by resource kind and id](file-size-tables-fst.md)
- [File requests and the read queue: the request slots, how a load is queued, sized, read in parts and completed, and how a caller waits, asks or cancels](file-requests-and-the-read-queue.md)
- [Bigfile archive: the VBF container, how its index loads and is checked, and how a read reaches the file](bigfile-archive.md)
- [Model asset list: every model with its model file, motion lanes, remastered parts and users](../Graphics/model-asset-list.md)
