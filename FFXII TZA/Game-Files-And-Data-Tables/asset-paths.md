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

### The path array table

The table at `0x0215F000` holds 41 pointers, one per kind, each 0 at load (the zero-filled tail of `.data`).
`0x002DF9A0(languageId, flag)` fills it once at boot from `0x0022A0B0` (`0x0022A159`): first the arrays every language
shares (`0x002DF9C5`-`0x002DFBA8`), then the language's own arrays through an 11-entry jump table on `languageId - 1`
(`0x002DFBAF`-`0x002DFBC9`). That compare is unsigned, so id 0 and every id above 11 take the default arm, and the
entries for ids 9 and 10 point at the default arm too. Every arm ends by storing the kind 7 array at `0x002DFF7F`.

| Global | Kind | Type | Start | Installed array | Set by |
|---|---|---|---|---|---|
| `0x0215F000` | 0 | `void*` | 0 (zero-filled tail) | `0x01E461F0` | `0x002DF9A0` (`0x002DF9C5`) |
| `0x0215F008` | 1 | `void*` | 0 (zero-filled tail) | per language, below | `0x002DF9A0`, by the language's arm |
| `0x0215F010` | 2 | `void*` | 0 (zero-filled tail) | per language, below | `0x002DF9A0`, by the language's arm |
| `0x0215F018` | 3 | `void*` | 0 (zero-filled tail) | `0x0215EFF8`, a zero-filled qword that only this store's `lea` names | `0x002DF9A0` (`0x002DF9DA`) |
| `0x0215F020` | 4 | `void*` | 0 (zero-filled tail) | `0x01E5E500` | `0x002DF9A0` (`0x002DF9E8`) |
| `0x0215F030` | 6 | `void*` | 0 (zero-filled tail) | `0x01EDD690` | `0x002DF9A0` (`0x002DF9F6`) |
| `0x0215F038` | 7 | `void*` | 0 (zero-filled tail) | per language, below | `0x002DF9A0`, by the language's arm |
| `0x0215F040` | 8 | `void*` | 0 (zero-filled tail) | per language, below | `0x002DF9A0`, by the language's arm |
| `0x0215F048` | 9 | `void*` | 0 (zero-filled tail) | per language, below | `0x002DF9A0`, by the language's arm |
| `0x0215F050` | 10 | `void*` | 0 (zero-filled tail) | `0x01E127B8` | `0x002DF9A0` (`0x002DFA04`) |
| `0x0215F058` | 11 | `void*` | 0 (zero-filled tail) | `0x01E18670` | `0x002DF9A0` (`0x002DFA12`) |
| `0x0215F060` | 12 | `void*` | 0 (zero-filled tail) | per language, below | `0x002DF9A0`, by the language's arm |
| `0x0215F068` | 13 | `void*` | 0 (zero-filled tail) | `0x01E7F670` | `0x002DF9A0` (`0x002DFA2E`) |
| `0x0215F070` | 14 | `void*` | 0 (zero-filled tail) | `0x01EAA9A0` | `0x002DF9A0` (`0x002DFA3C`) |
| `0x0215F078` | 15 | `void*` | 0 (zero-filled tail) | `0x01E46280` | `0x002DF9A0` (`0x002DFA4A`) |
| `0x0215F080` | 16 | `void*` | 0 (zero-filled tail) | `0x01E4CDF0` | `0x002DF9A0` (`0x002DFA58`) |
| `0x0215F088` | 17 | `void*` | 0 (zero-filled tail) | `0x0215F148`, a zero-filled qword that only this store's `lea` names | `0x002DF9A0` (`0x002DFA66`) |
| `0x0215F090` | 18 | `void*` | 0 (zero-filled tail) | `0x0215F150`, a zero-filled qword that only this store's `lea` names | `0x002DF9A0` (`0x002DFA74`) |
| `0x0215F098` | 19 | `void*` | 0 (zero-filled tail) | `0x01E94B50` | `0x002DF9A0` (`0x002DFA82`) |
| `0x0215F0A0` | 20 | `void*` | 0 (zero-filled tail) | `0x01ECBA30` | `0x002DF9A0` (`0x002DFA90`) |
| `0x0215F0B0` | 22 | `void*` | 0 (zero-filled tail) | `0x01E8AA00` | `0x002DF9A0` (`0x002DFAAC`) |
| `0x0215F0B8` | 23 | `void*` | 0 (zero-filled tail) | `0x01EA38B0` | `0x002DF9A0` (`0x002DFABA`) |
| `0x0215F0C0` | 24 | `void*` | 0 (zero-filled tail) | `0x01E0E508` | `0x002DF9A0` (`0x002DFAC8`) |
| `0x0215F0C8` | 25 | `void*` | 0 (zero-filled tail) | `0x01E4CD60` | `0x002DF9A0` (`0x002DFAD6`) |
| `0x0215F0D0` | 26 | `void*` | 0 (zero-filled tail) | per language, below | `0x002DF9A0`, by the language's arm |
| `0x0215F0D8` | 27 | `void*` | 0 (zero-filled tail) | `0x01E9D410` | `0x002DF9A0` (`0x002DFAF2`) |
| `0x0215F0E0` | 28 | `void*` | 0 (zero-filled tail) | `0x01ECB4D0` | `0x002DF9A0` (`0x002DFB00`) |
| `0x0215F0E8` | 29 | `void*` | 0 (zero-filled tail) | `0x0215F168`, a zero-filled qword that only this store's `lea` names | `0x002DF9A0` (`0x002DFB0E`) |
| `0x0215F0F0` | 30 | `void*` | 0 (zero-filled tail) | `0x01ED7740` | `0x002DF9A0` (`0x002DFB1C`) |
| `0x0215F0F8` | 31 | `void*` | 0 (zero-filled tail) | `0x01E46400` | `0x002DF9A0` (`0x002DFB2A`) |
| `0x0215F100` | 32 | `void*` | 0 (zero-filled tail) | `0x01E7FCF0` | `0x002DF9A0` (`0x002DFB38`) |
| `0x0215F108` | 33 | `void*` | 0 (zero-filled tail) | `0x01E127D0` | `0x002DF9A0` (`0x002DFB46`) |
| `0x0215F110` | 34 | `void*` | 0 (zero-filled tail) | `0x01E373A0` | `0x002DF9A0` (`0x002DFB54`) |
| `0x0215F118` | 35 | `void*` | 0 (zero-filled tail) | `0x01ECB9E0` | `0x002DF9A0` (`0x002DFB62`) |
| `0x0215F120` | 36 | `void*` | 0 (zero-filled tail) | `0x0215F158`, a zero-filled qword that only this store's `lea` names | `0x002DF9A0` (`0x002DFB70`) |
| `0x0215F128` | 37 | `void*` | 0 (zero-filled tail) | per language, below | `0x002DF9A0`, by the language's arm |
| `0x0215F130` | 38 | `void*` | 0 (zero-filled tail) | `0x01EBE740` | `0x002DF9A0` (`0x002DFB8C`) |
| `0x0215F138` | 39 | `void*` | 0 (zero-filled tail) | `0x01ECB7E0` | `0x002DF9A0` (`0x002DFB9A`) |
| `0x0215F140` | 40 | `void*` | 0 (zero-filled tail) | `0x0215F160`, a zero-filled qword that only this store's `lea` names | `0x002DF9A0` (`0x002DFBA8`) |

| Kind (global) | 1 US | 2 FR | 3 DE | 4 IT | 5 ES | 6 UK | 7 KR | 8 CH | 11 CN | 0, 9, 10 and above 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 (`0x0215F008`) | `0x01ED7630` | `0x01E19670` | `0x01E4C8A0` | `0x01E889F0` | `0x01E659E0` | `0x01EAEAE0` | `0x01E19780` | `0x01E65AF0` | `0x01EAED50` | `0x01E4C9B0` |
| 2 (`0x0215F010`) | `0x01EDBFE0` | `0x01E19890` | `0x01E4CAC0` | `0x01E88B60` | `0x01E6B8A0` | `0x01EAEE60` | `0x01E27430` | `0x01E6BB40` | `0x01EB0D00` | `0x01E4D830` |
| 5 (`0x0215F028`) | `0x01EE23A0` | `0x01E2F8A0` | `0x01E50B70` | `0x01E8D050` | `0x01E6E470` | `0x01EB0FA0` | `0x01E3E6F0` | `0x01E77B70` | `0x01EBF8A0` | `0x01E1F7D0` |
| 7 (`0x0215F038`) | `0x01EC73A0` | `0x01EDFE70` | `0x01E2D370` | `0x01E6BF40` | `0x01E4E640` | `0x01E8AB20` | `0x01E0E530` | `0x01E5A3D0` | `0x01EABBA0` | `0x01EDD7E0` |
| 8 (`0x0215F040`) | `0x01ED1990` | `0x01E129D0` | `0x01E46C00` | `0x01E82D50` | `0x01E5FD40` | `0x01E9DC10` | `0x01E19B30` | `0x01E65C00` | `0x01EB8AA0` | `0x01E276D0` |
| 9 (`0x0215F048`) | `0x01EBF740` | `0x01EDFD10` | `0x01E272D0` | `0x01E6BDE0` | `0x01E4DAD0` | `0x01E80FF0` | `0x01E0E3B0` | `0x01E58670` | `0x01EAEBF0` | `0x01E12660` |
| 12 (`0x0215F060`) | `0x01EC98D0` | `0x01EE9EA0` | `0x01E3CAF0` | `0x01E75F70` | `0x01E587D0` | `0x01EC98D0` | `0x01E10A60` | `0x01E5C900` | `0x01EAF100` | `0x01E88E00` |
| 21 (`0x0215F0A8`) | `0x01EDC280` | `0x01EDC280` | `0x01EDC280` | `0x01EDC280` | `0x01EDC280` | `0x01EDC280` | `0x01E0CFA0` | `0x01E0CFA0` | `0x01E0CFA0` | `0x01EDC280` |
| 26 (`0x0215F0D0`) | `0x01E4DC30` | `0x01E4DC30` | `0x01E4DC30` | `0x01E4DC30` | `0x01E4DC30` | `0x01E4DC30` | `0x01EAE0D0` | `0x01EAE0D0` | `0x01EAE0D0` | `0x01E4DC30` |
| 37 (`0x0215F128`) | `0x01ECBCF0` | `0x01ECBCF0` | `0x01ECBCF0` | `0x01ECBCF0` | `0x01ECBCF0` | `0x01ECBCF0` | `0x01EA4D00` | `0x01EA4D00` | `0x01EA4D00` | `0x01ECBCF0` |

Three functions read the table, each taking the kind as a sign-extended `int` with no bound: the read issuer
`0x002DF780` (`0x002DF7BF`, `0x002DF830`), the path copy `0x002DF880` (`0x002DF893`, which returns -1 for a null entry) and the
path lookup `0x002DF980` (`0x002DF98D`). `0x002DF9A0` itself reads the kind 7 slot back 53 times
(`0x002DFFA3`-`0x002E03E7`) when its second argument is 0: it then replaces 54 entries of the kind 7 array, ids 43 to
216, with `in_sdver` menu paths (`0x002DFF95`-`0x002E03EE`). The word it passes, `[0x01E0280C]`, ships as 1
([MRP menu resource packages](mrp-menu-resource-packages.md)).

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
