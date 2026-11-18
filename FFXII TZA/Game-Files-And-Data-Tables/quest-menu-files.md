[Home](../../README.md) / [Game files and data tables](README.md) / Quest menu files

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Quest menu files: the menuquest list, petitioner strings and per-group detail tables, how they are read, and what each field shows | format | Game files and data tables | Menu and map files | The quest-menu files in each language's quest folder: menuquest.dat, the quest list with each quest's name, group and row picture; menuquest.lst, the petitioner line and picture threshold per quest; and menuquest00 to 02.bin, one per group, with each quest's detail text, its progress table and the QHD0 and QHT0 map-marker chunks. Covers the quest data widget that loads them, the Hunts rows, the detail pane and the map-data widget that read them, the shipped files and the rules an edit must keep. | 0x0037F4D0, 0x0037F440, 0x0037F3B0, 0x02AED490, 0x0037F1F0, 0x003800D0, 0x0037FD50, 0x0037FBA0, 0x0037FA80, 0x0037E5B0, 0x0037EFC0, 0x0037EE10, 0x0037EF70, 0x0037EAA0, 0x0037E8D0, 0x00577C30, 0x005789D0, 0x00578450, 0x0037FEA0, 0x00473D50, 0x00473DB0, 0x00473BB0, 0x00473CC0, 0x02CA6C68, 0x02CA6C70, 0x0037F7C0, 0x0037FA00, 0x0037F140 |

## What the player sees

On the Clan Primer's Hunts page each accepted or finished hunt has a row: a picture of the mark, the hunt's
name and a line naming the petitioner and the town, such as "Tomaj (Rabanastre)". The picture changes
once the mark is defeated. Opening a hunt shows its record, which grows as the hunt goes on: the bill,
the accepted hunt and where the mark is, its defeat, the report. The map screens mark where to go next
for the selected hunt and label the place with a name, such as the petitioner's at the tavern or the
mark's where it roams.

## Where it comes from

Each language folder `ps2data/image/ff12/myoshiok/<lang>/quest/` holds the files, requested as kind-7
resources:

| File | Id | Content |
|---|---|---|
| `menuquest.dat` | `0x128` | the quest list (`qstd`) |
| `menuquest.nfs` | `0x129` | a TIM2 glyph sheet ([TIM2 images](tim2-images.md)) |
| `menuquest00.bin` to `menuquest02.bin` | `0x12A` + group | the detail table of one quest group |
| `menuquest.lst` | `0x13A` | the petitioner lines (`qstl`) |

The `us` kind-7 path array also names `menuquest03.bin` to `menuquest15.bin` (`0x12D`-`0x139`), which do
not ship. `menuquest.h`, in the `us`, `cn` and `kr` folders, is a C header with the quest count (66),
the highest quest id (172) and the group count (3); the quest ids `0x128`-`0x13A` do not include it. The `questtim2` folders of `ch`
and `in` hold six `q_c00`-`q_c05.tm2` pictures.

A hunt's record in `menuquest.dat` gives its name, row picture and group. The group picks one of `menuquest00` to
`02.bin`, and the hunt's place within its group picks its record there: its text, map steps and labels, and how many
parts show at each stage of progress. `menuquest.lst` adds the petitioner line and when the row picture changes.

## Layouts

### Queued requests

Each of the 32 queued requests at `+0x3F0` of the quest data widget is `0x10` bytes.

`QuestDataRequest` (`0x10` bytes, offsets from the start of the [questdata+0x3F0]+i*0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | state | 0 in a request; the queue copies requests whole (`0x0037FC55`-`0x0037FC66`) and `0x0037FFD0` moves the first into the list whole (`0x0038003E`), where this byte becomes the list entry's state |
| `+0x01` | `u8` | kind | 2 for a group file (`0x0037FE0E`, `0x0037FE7B`), 4 for menuquest.nfs (`0x0037F56F`); `0x0037FBA0` matches queued and listed entries by it (`0x0037FBD0`-`0x0037FBD4`, `0x0037FC11`-`0x0037FC15`) |
| `+0x02` | `u8` | group | the quest group of a kind-2 request (`0x0037FE13`, `0x0037FE60`), compared only for kind 2 (`0x0037FBE0`-`0x0037FBE4`, `0x0037FC22`-`0x0037FC26`) |
| `+0x03` | `u8[1]` | gap03 | 0 from the qword zero store that starts each request (`0x0037FDF2`, `0x0037FE56`, `0x0037F55E`); copied whole with the request (`0x0037FC55`, `0x0038003E`); read by no function as a field; nothing fixes its width |
| `+0x04` | `u16` | record | the menuquest.dat record index (`0x0037FE18`); `0x0037F190` sends it to the owner for kind 2 (`0x0037F1C6`) |
| `+0x06` | `u16` | questId | the quest id, mask `0x3FF00` of the record's key (dword `+0x04`, file offset `0x10` + 8 x index) (`0x0037FDBC`-`0x0037FDC4`, `0x0037FE06`) |
| `+0x08` | `void*` | owner | the widget to tell when the file is ready (`0x0037FE1E`, `0x0037FE51`, `0x0037F563`); a request equal to a queued one only replaces its owner (`0x0037FD34`-`0x0037FD42`) |

### Listed group files

Each of the 32 listed files at `+0xF0` of the quest data widget is `0x18` bytes; its first `0x10` bytes come whole from the request.

`QuestDataFile` (`0x18` bytes, offsets from the start of the [questdata+0xF0]+i*0x18):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | state | 1 loaded, 2 loading, 3 dropped on arrival; the first eight bytes come whole from the request (`0x0038003E`); `0x0037FBA0` reads it for a matching request and sets a dropped entry (3) back to 2, loading, so that `0x0037F1F0` keeps it when the file arrives (`0x0037FCBB`-`0x0037FCD0`); `0x0037E8D0` and `0x0037EE10` use an entry only at 1 (`0x0037E952`, `0x0037EEF3`); cleared on release (`0x0037FA49`) |
| `+0x01` | `u8` | kind | the request's kind, matched by `0x0037FBA0` (`0x0037FBD0`) and by `0x0037E8D0` and `0x0037EE10` (`0x0037E930`, `0x0037EED1`) |
| `+0x02` | `u8` | group | the request's group, matched for kind 2 (`0x0037FBE4`, `0x0037E936`, `0x0037EED7`) |
| `+0x03` | `u8[5]` | rest03 | the request's bytes `+0x03` to `+0x07`, copied whole with it (`0x0038003E`); `0x0037F190` reads the word `+0x04`, the menuquest.dat record, from a kind-2 entry `0x0037F1F0` hands it (`0x0037F314`, `0x0037F1C6`) |
| `+0x08` | `void*` | owner | the widget to tell: replaced by a matching request's owner (`0x0037FCBE`-`0x0037FCC2`); `0x0037F190` tells it when the entry is ready (`0x0037FD16`-`0x0037FD1D`) |
| `+0x10` | `void*` | buffer | the file's buffer from `0x003800D0`; for kind 2 `0x0037FEA0` publishes the selected quest's chunks from it (`0x0037FCEA`-`0x0037FD11`); `0x0037E8D0` and `0x0037EE10` read the group file through it (`0x0037E957`, `0x0037EEF8`); freed on release (`0x0037FA40`) |

### The quest data widget's fields

The quest data widget is the `0x5F0`-byte widget kept at `0x02AED490` with procedure `0x0037F4D0` (The quest data widget
below).

`QuestDataWidget` (`0x5F0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0037F4D0` |
| `+0x0C0` | `void*` | owner | the widget told when files are ready: 0 on creation, then the creation record's `+0x08` (`0x0037F66C`, `0x0037F6C7`-`0x0037F6CB`); `0x0037E4F0` keeps the closing owner here (`0x0037E53D`); `0x0037F340` sends it {`0x10`, 8} (`0x0037F358`, `0x0037F367`) and `0x0037F1F0`, while `+0xE5` is 0, {`0x10`, 1, 0} from `0x00915BB0` (`0x0037F211`-`0x0037F248`); destroy sends it {`0x10`, 9} (`0x0037F59C`-`0x0037F5CB`); the menuquest.nfs request names it (`0x0037F563`) |
| `+0x0C8` | `void*` | questTable | menuquest.dat, kind-7 resource `0x128`, always requested on creation (`0x0037F72A`-`0x0037F750`); `0x0037FD50` finds a quest's group and position in it (`0x0037FD67`-`0x0037FDC4`); freed by `0x0037FA00` |
| `+0x0D0` | `void*` | questList | menuquest.lst, kind-7 resource `0x13A`, requested when `+0xE0` bit `0x10` is set (`0x0037F745`-`0x0037F778`); `0x0037E5B0` reads the threshold and the petitioner line from it (`0x0037E65F`, `0x0037E6BC`) and `0x0037EFC0` the petitioner line alone (`0x0037EFCB`); `0x0037F860` frees it and clears this (`0x0037F8A9`-`0x0037F8BA`) |
| `+0x0D8` | `void*` | nameSheet | menuquest.nfs, kept by `0x0037F1F0` when it arrives and registered as glyph sheet 5 (`0x0037F2B2`-`0x0037F2C3`); `0x0037EB70` returns it (`0x0037EB7D`); `0x003800D0` tests it (`0x003800F2`); `0x0037F860` unregisters it (`0x0037F8C5`) |
| `+0x0E0` | `u32` | flags | mask `0x39F` cleared on creation (`0x0037F62B`). Bit `0x1`: ready, set by `0x0037F340` with `+0xE5` = 2 (`0x0037F389`). The bits under mask `0x1E`: creation bytes 0-3 (`0x0037F678`-`0x0037F6C1`): bit `0x2` request menuquest.nfs after the first load (`0x0037F54C`-`0x0037F574`), bit `0x4` read by no function, bit `0x8` load resource group `0x15` (`0x0037F70D`-`0x0037F71E`), bit `0x10` load menuquest.lst (`0x0037F745`). Bits `0x20` and `0x40` cleared on creation (`0x0037F6D2`). Bit `0x20`: the first load has arrived (`0x0037F532`-`0x0037F546`). Bit `0x40`: group `0x15` was requested (`0x0037F723`); `0x0037F860` releases it and clears the bit (`0x0037F88D`-`0x0037F8A1`). Bit `0x80`: busy: set while `0x0037E350` works (`0x0037E3BE`, `0x0037E46F`) and by `0x003800A0` (`0x003800AC`-`0x003800BC`); `0x0037F160` returns it and `0x0037E4F0` then answers at once. Bits `0x100` and `0x200`: the selected quest's QHD0 and QHT0 chunks are published (`0x0037FEF5`-`0x0037FF5F`); cleared on creation (`0x0037F6E5`, `0x0037F703`) and by `0x0037F860` (`0x0037F8EC`, `0x0037F902`); `0x0037EB90` and `0x0037EC70` test bit `0x100` (`0x0037EBC3`, `0x0037ECB4`), `0x0037F140` returns bit `0x200` |
| `+0x0E4` | `u8[1]` | gap0E4 | zeroed with the rest of the `0x5F0` bytes by the constructor `0x002465F0` (memset at `0x00246626`); read by no function; nothing fixes its width |
| `+0x0E5` | `u8` | stage | 0 on creation (`0x0037F650`); 1 when the first load arrives (`0x0037F53F`); 2 ready (`0x0037F390`); 3 closing without a close request and 4 closing with one, set by `0x0037E4F0` (`0x0037E594`, `0x0037E548`). At 3 the procedure retries `0x0037F860` and destroys the widget when it succeeds (`0x0037F583`-`0x0037F5D0`); destroy frees the files except at 3 (`0x0037F50B`); `0x0037F1F0`, `0x0037FBA0` and `0x0037FFD0` wait while it is 0 (`0x0037F205`, `0x0037FC75`, `0x0037FFF2`) |
| `+0x0E6` | `u8` | group | the selected quest's group, the low byte of the record's key (file offset `0x10` + 8 x index), stored by `0x0037FD50` (`0x0037FDDD`), or the group `0x0037FE40` is asked for (`0x0037FE64`); `0xFF` on creation (`0x0037F63D`); `0x0037E8D0` finds the group's file by it (`0x0037E90A`) |
| `+0x0E7` | `u8` | position | the quest's position in its group, the number of earlier records of the same group (`0x0037FD93`-`0x0037FDE9`); 0 from `0x0037FE40` (`0x0037FE6D`); `0x0037FBA0`, `0x0037F1F0` and `0x0037E8D0` index the group file's 20-byte items with it (`0x0037FCFE`, `0x0037F2F8`, `0x0037E960`), and `0x0037E8D0` the 28-byte section-5 rows (`0x0037E9D9`) |
| `+0x0E8` | `u16` | record | the selected quest's record index in menuquest.dat (`0x0037FDF7`); 0 from `0x0037FE40` by a dword store with `+0xEA` (`0x0037FE74`); `0x0037E8D0` answers 0 unless it is below menuquest.dat's count `+0x0A` (`0x0037E8F4`-`0x0037E901`) and reads that record's key and name (`0x0037E99D`-`0x0037E9C3`) |
| `+0x0EA` | `u16` | questId | the selected quest's id, mask `0x3FF00` of the record's key (file offset `0x10` + 8 x index) (`0x0037FDBC`-`0x0037FDFF`); 0 from `0x0037FE40` (`0x0037FE74`); `0x0037EB90` and `0x0037EC70` read it (`0x0037EBEE`, `0x0037EC10`, `0x0037ECDF`) |
| `+0x0EC` | `u8[2]` | gap0EC | zeroed with the rest of the `0x5F0` bytes by the constructor `0x002465F0` (memset at `0x00246626`); read by no function; nothing fixes its width |
| `+0x0EE` | `u8` | fileCount | the number of entries in the file list `+0xF0`: 0 on creation with `+0xEF` (`0x0037F647`); `0x0037FBA0` walks it (`0x0037FBAF`), `0x0037FA00` frees that many and sets 0 (`0x0037FA27`, `0x0037FA62`) |
| `+0x0EF` | `u8` | queueCount | the number of queued requests at `+0x3F0`: `0x0037FBA0` walks it and appends at `+0x3F0` + count x `0x10` (`0x0037FBF7`, `0x0037FC4E`-`0x0037FC6A`); `0x0037FFD0` takes the first and lowers it (`0x00380061`); the procedure runs `0x0037FFD0` while it is not 0 (`0x0037F5DA`) |
| `+0x0F0` | `u8[768]` | files | the file list, 32 QuestDataFile entries (above), cleared on creation with the queue (`0x0037F60D`-`0x0037F626`) |
| `+0x3F0` | `u8[512]` | queue | the request queue, 32 QuestDataRequest entries (above) |

### The quest files

The shipped quest files are laid out as follows.

All multi-byte fields are little-endian.

### menuquest.dat

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "qstd"; the readers ignore it |
| `+0x04` | `u32` | version | 100; not read |
| `+0x08` | `u16` | groups | 3; `0x0037EE10` and `0x0037FD50` read its low byte as the group when their record index is -1 (`0x0037EE95`, `0x0037FD93`): `0x0037EE10` for a quest id no record holds, `0x0037FD50` when `0x005789D0` passes it `0x0037EDB0`'s -1 (`0x00578ACE`-`0x00578ADA`); `0x0037FD50` then also takes the quest id from bits `0x3FF00` of the dword at `+0x08` (`0x0037FDBC`) |
| `+0x0A` | `u16` | count | records; bounds every index (`0x0037E5B0`) |
| `+0x0C` | `rec[count]` |  | 8 bytes each |

A record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | text | the quest's name, a message id (`0x002F9920`) |
| `+0x04` | `u32` | key | mask `0xFF` group; mask `0x3FF00` quest id; mask `0xFF00000` row picture; mask `0xC0000` not read |

A quest's position is its index among the records of its own group; it selects the quest's record in
the group's `.bin` file (`0x0037FD50`).

### menuquest.lst

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "qstl"; the readers ignore it |
| `+0x04` | `u32` | version | 100; not read |
| `+0x08` | `u16` | stringsAt | base of the string offsets (`0x0037F02A`) |
| `+0x0A` | `u16` | zero |  |
| `+0x0C` | `u16` | zero |  |
| `+0x0E` | `u16` | count | directory entries (`0x0037EFD9`) |
| `+0x10` | `dir[count]` |  | 8 bytes each |

A directory entry:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | quest | quest id; the first entry with the id wins (`0x0037EFF0`) |
| `+0x02` | `u16` | textAt | offset of the petitioner line from stringsAt; `0xFFFF` = empty (`0x0037F01C`) |
| `+0x04` | `u8` | threshold | low nibble: the progress part at which the row picture changes (`0x0037E6A6`) |
| `+0x05` | `u8[3]` | zero |  |

The strings are the game's encoded text, zero-terminated. A quest with no entry gets an empty line.

### menuquest00.bin to menuquest02.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | sectionAt[6] | offset of each section |
| `+0x0C` | `u8[2]` | pad | `0xFFFF`; read by no function: the readers of a loaded group file, `0x0037E8D0`, `0x0037EE10`, `0x0037EF70` and `0x0037FEA0`, take sectionAt and the records from `+0x10` (`0x0037FD50` reads only menuquest.dat), and the loader `0x003800D0` and the list code `0x0037FFD0`, `0x0037F7C0` and `0x0037FA00` move or free the buffer; nothing fixes its width |
| `+0x0E` | `u16` | count | records, which the readers index by position; read by no function: the readers of a loaded group file, `0x0037E8D0`, `0x0037EE10`, `0x0037EF70` and `0x0037FEA0`, take sectionAt and the records from `+0x10`, and the loader `0x003800D0` and the list code `0x0037FFD0`, `0x0037F7C0` and `0x0037FA00` move or free the buffer; nothing fixes its width |
| `+0x10` | `rec[count]` |  | 20 bytes each |

A record, at `0x10 + 20 x position`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | item[6] | offset of the quest's item in each section, from sectionAt[s]; `0xFFFF` = no item |
| `+0x0C` | `u16` | fill[4] | `0x0FFF`; not read |

No reader uses `item[5]`: the progress row is found by position. The sections:

| Section | Content | Reader |
|---|---|---|
| 0, 1, 2 | zero-terminated text; `0xFFFF` in `sectionAt` or `item` gives an empty string | `0x0037E8D0` |
| 3 | a `QHD0` chunk per quest, the map steps | `0x0037FEA0` → `0x00473D50` |
| 4 | a `QHT0` chunk per quest, the map labels | `0x0037FEA0` → `0x00473DB0` |
| 5 | 28 bytes per quest at `sectionAt[5] + 28 x position` | `0x0037EF70`, `0x0037EE10` |

Section 2 holds the parts of the quest record, separated by `0x03`; within a part `0x02` breaks the line.
A section-5 row is 52 four-bit values, value `k` in byte `k / 2` (the high nibble for odd `k`), then
two zero bytes. Value `k` is the number of parts shown while the quest's progress byte divided by 5 is
`k` (`0x0037EF70`).

Both chunks start the same way:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "QHD0" or "QHT0"; the readers ignore it |
| `+0x04` | `u32` | count | entries; bit `0x80000000` is set once the offsets are made addresses |
| `+0x08` | `u32` | entryAt[count] | offset of each entry from the chunk |

A `QHD0` entry, read by `0x00473BB0(entry, step, progress)`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | steps | step records that follow |
| `+0x01` | `u8` | type | 0 or 1 |
| `+0x02` | `step[steps]` |  | 18 bytes each: |
| `+0x00` | `u8` | a | type 0: returned alone; type 1: returned with b and location |
| `+0x01` | `u8` | b |  |
| `+0x02` | `u16` | location | the location the map marks (type 1) |
| `+0x04` | `u8` | shown[7] | bit n: the step applies while progress / 5 is n (n at most 50) |
| `+0x0B` | `u8` | labelled[7] | bit n: the location carries the step's label then |

A `QHT0` entry, read by `0x00473CC0(entry, step)`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | count | label pairs; not read |
| `+0x01` | `u8` | value | returned by `0x00473CC0` |
| `+0x02` | `u16` | zero |  |
| `+0x04` | `{u16 first, u16 second}[]` |  | per step: offsets of two label strings from the entry; `0x8000` and up = no label |

## Shipped data

| Fact | Value |
|---|---|
| languages | `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us`; every folder has all six loaded files |
| `menuquest.dat` | 540 bytes, identical in all nine: 66 quests, group 0 19 (ids 0-22), group 1 45 hunts (ids 128-172), group 2 2 (ids 50, 51) |
| `menuquest.dat` keys | the bits under mask `0xC0000` are 1 and the bits under mask `0xF0000000` are 4 in group 0's 19 records, both 0 in the other 47; the two group 2 records have text -1; 64 row pictures, picture 0 on three records |
| hunt row pictures | the bits under mask `0xFF00000` run 19 to 63 for the hunts |
| `menuquest.lst` | 1,684 (`in`) to 2,036 (`es`) bytes; 66 entries naming the same 66 ids, `stringsAt` `0x220` |
| `.lst` thresholds | 3 for 44 hunts, 4 for one, 0 for the 21 other quests |
| `.lst` strings | `us`: "not use." for group 0, an empty string for group 2, "petitioner (town)" for the hunts |
| `menuquest00.bin` | 19 records; 2,964 to 3,012 bytes, 10,144 in `in`; sections 0-2 hold placeholder text |
| `menuquest01.bin` | 45 records; 23,564 (`in`) to 39,760 (`de`) bytes; sections 0 and 1 empty, section 2 the hunt record |
| `menuquest02.bin` | 2 records, 224 bytes, no text |
| record counts | equal the `menuquest.dat` group counts in every language; `sectionAt[0] = 16 + 20 x count` and `sectionAt[5] + 28 x count` is the file size in all 27 files |
| hunt records | every hunt's section-2 part count equals the largest value in its progress row, in all languages: 4 parts for 42 hunts, 5 for three (ids 133, 167, 168) |
| progress rows | non-decreasing in every file; every hunt shows its first part from progress 10, the later parts at 20 to 150 by hunt |
| chunks | every record names one `QHD0` and one `QHT0` chunk of one entry; 567 `QHD0` entries of type 1 and 27 of type 0 over all files |
| `menuquest.nfs` | 208 to 29,008 bytes ([TIM2 images](tim2-images.md)) |
| size table | the US table sizes `0x128`-`0x12C` and `0x13A` only |

[`quest-menu-files-dat-rows.tsv`](quest-menu-files-dat-rows.tsv) lists the 66 records of `menuquest.dat`, the
same in all nine folders: offset, text, the key and its fields, and the record's position in its group.

[`quest-menu-files-lst-rows.tsv`](quest-menu-files-lst-rows.tsv) lists the nine `.lst` files, with size,
SHA-256, the locale ids that load each and the header, then their 594 directory entries: quest id,
`menuquest.dat` record and group, `textAt`, the threshold byte and the value `0x0037E5B0` takes from it, the
pad bytes, the string, the line decoded with the language's font, and what the Hunts row shows.

[`quest-menu-files-nfs-rows.tsv`](quest-menu-files-nfs-rows.tsv) lists the nine `.nfs` files and their ten
pictures.

- Locale ids 0, 9 and 10 load the `in` files and ids 1 to 5, 7, 8 and 11 their own folder's. Id 6 loads no
  quest file: its array names `uk/quest/`, which ships nothing, and the UK size table holds -1 for ids
  `0x128` to `0x12C` and `0x13A`, so `0x00249210` files no request for them.
- In every language, 44 hunts have threshold 3 and switch their row picture to the defeated sheet at
  progress part 3; Battle on the Big Bridge (quest 167) has 4. The line under each hunt's name is its
  petitioner and town, such as Tomaj (Rabanastre) for Red & Rotten in the Desert. Every threshold is below
  its hunt's part count.
- The 19 group-0 entries hold `not use.` in eight languages; in `in` they hold Japanese titles such as `DOG
  TEN COMMANDMENTS`, 14 of them starting with expansion glyph 117 of the quest sheet, written `{expansion
  glyph N}` in the TSV with 118 to 120. Quests 50 and 51 of group 2 share one empty string.
- The same rows with those marks read through each language's `fontquest.dat` are in the resolved-text table of
  [Font expansion lists](../Menus-And-HUD/fonts-expansion-lists.md).
- Each file has 66 entries naming the 66 `menuquest.dat` quests once each, its strings start right after the
  directory at `0x220`, the pad bytes and the threshold bytes' high nibbles are 0, and the 99 to 133 bytes
  of the string area that no entry reaches are all zero.
- `menuquest.nfs` holds one 4-bit picture, two in `in`. The block after the first picture's header holds
  8-byte records, of which 121 (`in`), 18 (`kr`) and 26 (`ch`, `cn`) have a non-zero dword at `+2`, the
  record counts of the language's `fontquest.dat`; the `us`, `fr`, `de`, `it` and `es` sheets have one, and
  their font folder has no `fontquest.dat`.
- The second `in` picture, 504 x 23, has header size `0x30`, so `0x0039BF50` fills no block for it. The
  identical `us` and `it` files carry version byte 216, the other seven 4. Every file passes the registry
  test of `0x0039BEC0` (`TIM2` and a low nibble of 1 at `+0x40`).

Every record of the 27 group files, decoded with the layouts above. Each record is listed once per group of folders
whose file has the same bytes, split where those folders draw text with different fonts, so a record that repeats in
files that differ elsewhere has one row per folder; the texts are decoded with the font of each folder's language, in
the notation of the `.lst` table.

| table | rows | one row per |
|---|---:|---|
| [`quest-menu-files-bin-files-rows.tsv`](quest-menu-files-bin-files-rows.tsv) | 27 | group file: folder, size, SHA-256, the folders with the same bytes, `sectionAt`, pad and count |
| [`quest-menu-files-bin-rows.tsv`](quest-menu-files-bin-rows.tsv) | 586 | record: quest id and `menuquest.dat` record, `item[6]`, `fill`, the three texts, the section-2 part count, the 52 progress values, and the `QHD0` and `QHT0` entry headers |
| [`quest-menu-files-bin-steps-rows.tsv`](quest-menu-files-bin-steps-rows.tsv) | 1,063 | `QHD0` step: `a`, `b`, location, the `shown` and `labelled` bits with the values of progress / 5 they cover, and the step's two `QHT0` labels |

## Loader behaviour

### The quest data widget

`0x0037F4D0` is the quest data widget, published at `0x02AED490` (only one exists: its openers `0x0037F3B0` and
`0x0037F440` refuse while the global is set). Bytes passed at creation select what it loads:

| Byte | Bit of `+0xE0` | Effect |
|---|---|---|
| 0 | `0x2` | after the first load, request `menuquest.nfs` |
| 2 | `0x8` | load resource group `0x15` |
| 3 | `0x10` | load `menuquest.lst` into `+0xD0` |

`menuquest.dat` always loads, into `+0xC8`. The Hunts page opens it with all four bytes 1
(`0x0037F440` at `0x00579F1E`); the map-data widget's request `0x003BC9F0` (`0x003BCA48`) and `0x0037E350` open it with all four 0,
and `0x003F4E70` through `0x0037F3B0` with byte 2 only. When `menuquest.nfs` arrives `0x0037F1F0` keeps it at
`+0xD8` and registers it as a glyph sheet (`0x0039BEC0`, `0x0017FBC0(5)`).

`0x0037F3B0(owner)` and `0x0037F440(b0, b1, b2, b3, owner)` return 0 while `0x02AED490` is set (`0x0037F3CB`, `0x0037F45E`).
Otherwise they create the `0x5F0`-byte widget with `0x00244F50` and the procedure `0x0037F4D0`, from a creation record
of the four bytes and the owner at `+0x08`, and return 1 (`0x0037F406`, `0x0037F49F`); `0x0037F3B0` sets byte 2 alone
(`0x0037F3FE`).

`0x0037F1F0(widget)` is the completion of a listed file:

- While `+0xE5` is 0 it sends `{0x10, 1, 0}` to the owner `+0xC0`, when the owner and its handler are set, and
  does nothing else (`0x0037F205`-`0x0037F248`).
- Otherwise it reads the last listed entry (`0x0037F25D`-`0x0037F27A`): at a state other than 2 or 3 it does nothing,
  at 3 it removes the entry with `0x0037F7C0(widget, last, 1)` (`0x0037F298`), and at 2 it sets state 1 (`0x0037F2A3`).
- For a kind-2 entry it then runs `0x0037FEA0(buffer, record)`, the record at `buffer + 0x10 + 20 x position` with
  the published widget's `+0xE7`, or null for a null buffer (`0x0037F2E4`-`0x0037F30B`).
- For kind 4 it also calls `0x0037F340` unless `+0xE0` bit `0x1` is set, or bit `0x8` is set with bit `0x40` clear
  (`0x0037F2C8`-`0x0037F2DD`).
- An entry it set to 1, of any kind, then goes to the entry's owner `+0x08` through `0x0037F190` (`0x0037F317`).

Group files load on demand: `0x0037FD50(index)` finds the quest's group and position and posts a request,
and `0x003800D0` asks for id `0x12A` plus the group. Asking for another group releases the other group
files first (`0x0037FA80`), so one group's table is held at a time.

`0x0037FBA0` queues such a request as a 16-byte entry at `+0x3F0` (count `+0xEF`) unless an equal entry is
already queued, and `0x0037FFD0`, run from there and from the widget procedure `0x0037F4D0`, moves the first
queued entry into the list as a loading entry (state 2, its buffer from `0x003800D0`) and shifts the queue
down. It waits while the published widget's `+0xE5` is 0 or its last listed entry is still loading (2) or
dropped on arrival (3).

- `0x0037FD50(index, owner)` works on the published widget. It reads the record's key before its test, so with
  `+0xC8` null it reads address `0x10 + 8 x index` (`0x0037FDBC`); an index not below the count answers 0
  (`0x0037FD86`, `0x0037FDCA`), and a negative one is not refused and takes position 0.
- Otherwise `0x0037FD50` stores `+0xE6` to `+0xEA` (`0x0037FDDD`-`0x0037FDFF`), posts `{0, 2, group, record, quest id,
  owner}` to `0x0037FBA0` (`0x0037FE23`) and answers 1 whatever that returns.
- `0x003800D0(widget, request)` asks for `0x12A` plus the group for kind 2 (with 3 and 0); for kind 4 it asks for
  `0x129` (with 2 and 1) only while `+0xD8` is null, else answers 0 (`0x003800F2`-`0x003800FB`); another kind asks for
  id 0.
- It takes a menu set (`0x00249580`), files the request through `0x00249210` (`0x00380145`), closes the set
  (`0x00249410`) and answers the record's buffer `+0x08`.
- `0x0037FA80(widget, group)` walks the list from the last entry and releases each kind-2 entry of another group as
  `0x0037F7C0` does without force (`0x0037FAF2`-`0x0037FB9A`). It answers 1 when every such entry went, 0 when one was
  kept because it was at 2 or 3 (`0x0037FB1C`).
- `0x0037FBA0(widget, request)` first looks for a listed entry of the same kind, and group for kind 2. A match
  takes the request's owner and answers 0 (`0x0037FCBB`-`0x0037FCC2`): at 1 it runs `0x0037FEA0` for kind 2 and tells
  the owner through `0x0037F190(owner, request)` (`0x0037FCE4`-`0x0037FD1D`), at 3 it goes back to 2 (`0x0037FCD0`), and
  at another state it stays.
- With no listed match an equal queued request only takes the owner and answers 0 (`0x0037FD34`-`0x0037FD42`).
- Else, for kind 2, `0x0037FBA0` runs `0x0037FA80` on the published widget and ignores its answer (`0x0037FC49`). It
  appends the request with no bound on the 32 places (`0x0037FC4E`-`0x0037FC6A`) and answers 1.
- It runs `0x0037FFD0` when the published widget is null, or its `+0xE5` is not 0 and its last listed entry is
  at neither 2 nor 3 (`0x0037FC70`-`0x0037FCA1`).

The widget lists the group files it asked for at `+0xF0`: `0x18`-byte entries, count `+0xEE`, each with a
state byte (1 loaded, 2 loading, 3 dropped on arrival) and the buffer at `+0x10`.

- `0x0037F7C0(widget, i, force)` removes entry i and returns 1: a loaded or forced entry has its buffer
  freed (`0x003697F0`); an entry still loading is marked 3 and kept, returning 0.
- Without force an entry already at 3 is also kept, returning 0 (`0x0037F801`), and one at state 0 or above 3 is
  removed without a free (`0x0037F803`). An i not below the count returns 0 (`0x0037F7EA`). A freed entry's state is
  cleared (`0x0037F823`); removal lowers `+0xEE` and moves the later entries down (`0x0037F826`-`0x0037F847`).
- `0x0037FA00(widget)`, called from the widget procedure `0x0037F4D0`, frees `menuquest.dat` (`+0xC8`) and
  every listed buffer and empties the list.
- It clears `+0xC8` (`0x0037FA20`) and each entry's state (`0x0037FA49`), frees a listed buffer whatever its state,
  and leaves the queue `+0x3F0` as it is.
- `0x0037F340(widget)` sends `{0x10, 8}` to the owner's handler at `+0xC0`, then sets bit `0x1` of `+0xE0`
  and `+0xE5` = 2. `0x0037F190(owner, entry)` sends `{0x10, entry byte 1, its word +4 when that byte is 2}`.
- `0x0037F050()` answers whether no quest data widget exists, and `0x0037F160()` returns `+0xE0` bit `0x80`, or 0
  with no widget; the map-data widget's `0x003BBFB0` reads both.
- `0x0037E4F0(owner)` closes the widget for an owner. While `+0xE0` bit `0x80` is set it sends `{0x10, 10}` to the
  owner at once. Otherwise it unregisters the glyph sheet (`0x0037F860`), keeps the owner at `+0xC0` and sets
  `+0xE5` to 3 when that returns 0, or to 4 with a close request (`0x00244F00`) and `{0x10, 9}` to the owner.
  With no widget the owner gets `{0x10, 9}`. `0x0037E350`, `0x003BBFB0`, `0x003F4B40`, `0x003F4E70` and `0x00579420` call it.
- `0x0037EDB0(id)` returns the index of the `menuquest.dat` record whose key holds quest id `id`, or -1, and
  `0x0037E8A0(i)` returns record i's name, or the empty string `0x01CEB638` past the count.

### Hunt rows

`0x0037EAA0(row, group)` counts, in record order, the quests of the group that are cleared (`0x0046B1A0`) or
ordered (`0x0046B240`). It returns the record index of the quest numbered `row` in that count, or -1 when fewer
quests qualify or `+0xC8` is null (`0x0037EACA`, `0x0037EB48`); group `0xFF` takes every group (`0x0037EB00`).

`0x0037E5B0` then reads the quest: its name, id, picture byte, position and group from `menuquest.dat`, and its
threshold and petitioner line from `menuquest.lst` (`0x0037E65F`-`0x0037E6AC`, `0x0037E6BC`-`0x0037E746`;
`0x0037EFC0` reads the line alone).

- `0x0037E5B0(index, out)` answers 0 when `+0xC8` is null or the index is outside the records
  (`0x0037E5CE`-`0x0037E5E7`), else 1. It searches the `.lst` directory itself, with the rule of `0x0037EFC0`.
- It writes `+0x00` the name (`0x002F9920`), `+0x08` the quest id, `+0x0A` and `+0x0B` the picture byte, `+0x0C`
  the position, `+0x0E` the threshold, `+0x0F` the group and `+0x10` the line (`0x0037E603`-`0x0037E746`).
- Without `menuquest.lst` or an entry for the quest the threshold is 0 and the line the empty string `0x00D111BA`.

The row builder `0x00577C30(list, layout, row, nodes, sheets)` takes group `list` for lists 0 to 2 and `0xFF`
otherwise (`0x00577C62`-`0x00577C83`), and finds and reads the quest with `0x0037EAA0` and `0x0037E5B0` without testing
either answer (`0x00577C87`-`0x00577C93`). It then:

- shows the name, and the petitioner line drawn with the `menuquest.nfs` sheet (`0x00577D7F`-`0x00577D95`);
- for group 1, treats the hunt as done when its current progress part (`0x0037EE10`) is at least the
  `.lst` threshold; for other groups, when the quest is cleared;
- picks picture sheet `2 x (picture / 24)`, plus 1 when done, and cell `picture % 24`; a sheet number of
  6 or more becomes sheet 0.
- names the chosen sheet `q_img_c%03d` with its `+0x40` when that is not 0 (`0x0017D2E0`, `0x00577D17`), and sets the
  number `row + 1` on `nodes[1]` (`0x00393160`, `0x00577D4F`);
- sets bit `0x1` of `nodes[4]` while the quest is cleared (`0x00577D9D`-`0x00577DBB`), and of `nodes[5]`, on list 1
  only, while the hunt is not fully read (`0x00576D20(6, position)`, `0x00577DC4`-`0x00577DFA`).

`0x0037EE10` needs the group's `.bin` loaded; without it the row counts as not done.

- `0x0037EE10(quest)` finds the quest's first record, its group and position, then the first listed kind-2 file of
  that group. It answers -1 when that file is missing, not at state 1 or has a null buffer
  (`0x0037EEB8`-`0x0037EEFF`), and -1 is below every threshold (`0x00577CB1`).
- Otherwise it answers value `progress / 5` of the section-5 row, as `0x0037EF70` does (`0x0046B180`,
  `0x0037EF01`-`0x0037EF57`).
- An id no record holds takes the byte at `menuquest.dat` `+0x08` as its group and position 0
  (`0x0037EE7F`-`0x0037EE9E`); with `+0xC8` null it looks for group `0xFF` (`0x0037EE75`).

### The detail pane

When the group file has loaded, `0x0037E8D0` fills the pane's record: quest id, name, the progress part
count from section 5, the section 0, 1 and 2 strings and the `.lst` line.

It answers 0 when `+0xC8` is null, the selected record `+0xE8` is not below the count, or the first listed
kind-2 entry of group `+0xE6` is missing, not at state 1 or has a null buffer (`0x0037E8EA`-`0x0037E95E`); else it
fills the record and answers 1 (`0x0037EA88`).

The record: `+0x00` the quest id, `+0x02` the quest's `questbase.bin` value A (`0x00473B90`), `+0x08` the name,
`+0x10` the part count (`0x0037EF70`), `+0x18`, `+0x20` and `+0x28` the section 0, 1 and 2 strings, the empty
string `0x00D111BA` where `sectionAt` or `item` is `0xFFFF`, and `+0x30` the `.lst` line (`0x0037EFC0`, `0x0037EA75`).

`0x005789D0` builds two text
panes through `0x00578450`:

1. Section 0, followed, once the quest is cleared, by an empty line and section 1.
2. Section 2 cut at each `0x03` into at most 12 parts, of which the first `progress part count` are shown.

The progress byte is the quest's scenario flag, save `+0x1064 + quest` (`0x0046B180`;
[Quests](../Story-Events-And-Hunts/quests.md)).

`0x00578450` is the pane's procedure. Message 1 keeps the creation record's `+0x00` at
`+0xC0`, the quest record `+0x10` at `+0xD0`, the mode byte `+0x20` at `+0xF8` and the
byte `+0x21` at `+0xF9` (`0x005784F4`-`0x00578538`). Mode 1 is the first pane: `0x00578120`
lays section 0 out at `+0x100`, and for a cleared quest (`0x0046B1A0`) the empty line
`0x00D237DC` and section 1 follow; the line count goes to `+0xFA` and `+0xFB`
(`0x0057854F`-`0x005785BE`).

Mode 0 is the second pane. After `0x00578120` on section 2 it finds the parts with
`0x002B39A0(text, 3)` and counts each part's lines with `0x002B39A0(text, 2)`: a `0x02`
counts when it lies before the next part and is not the text's last byte, and the last
part counts one more when no `0x02` is left (`0x005785C9`-`0x0057869D`).

The shown count `+0xF4` is the smaller of the record's part count `+0x10` and the parts
found. The twelve bytes from `+0xE8` hold each part's first line, and `+0xFB` the lines
of the shown parts (`0x0057869F`-`0x00578718`).

Both modes then take a pane from `0x003931E0` (kept at `+0xD8`, its `+0xC8` and `+0xD8`
pointing back), give it the line count with `0x002D48C0` and the byte `+0xF9` with
`0x002D47C0`, set its byte `+0xFF` to `0x58`, its handler `+0x120` to `0x00578310` and bits
`0x1000000` of `+0xE4` and `0x800000` of `+0xE0`; a creation dword `+0x08` of 1 also
sets its byte `+0x103` to `0x64` and bit `0x4000000` of `+0xE4` (`0x0057871A`-`0x0057882B`).

Message 10 runs `0x002D3900` on the pane and, like message 12, passes the message to the
function at the first qword of `+0xC0`, answering 0 when that qword is null; message 14
answers 0; any other goes to `0x005C5230` (`0x0057847B`-`0x005784EF`, `0x00578830`).

### Map markers

Whenever the selected quest's group file is ready (`0x0037F1F0`, `0x0037FBA0`), `0x0037FEA0` takes the quest's
`QHD0` chunk at `sectionAt[3] + item[3]` and its `QHT0` chunk at `sectionAt[4] + item[4]`. `0x00473D50`
and `0x00473DB0` publish them at `0x02CA6C68` and `0x02CA6C70` and, the first time, add the chunk's address to
each `entryAt` and set bit `0x80000000` of `count`. Widget bits `0x100` and `0x200` say whether each chunk is
set. `0x0037F140()` returns bit `0x200`, or 0 when no widget exists; the map-data widget's procedure `0x003BC4E0`
reads it.

- `0x0037FEA0(buffer, record)` publishes a chunk only when both are set, neither `sectionAt` nor `item` is `0xFFFF`
  and the 32-bit sum is not 0 (`0x0037FEBA`-`0x0037FEE0`, `0x0037FF11`-`0x0037FF37`). Otherwise it clears that chunk's
  bit of the published widget and leaves `0x02CA6C68` or `0x02CA6C70` as it was (`0x0037FF0B`, `0x0037FF5F`).
- `0x00473D50` and `0x00473DB0` store the chunk first and skip the rebase when bit `0x80000000` is already set
  (`0x00473D62`, `0x00473DC2`). Their loop bound `(int32)(n + n) >> 1` is the count `n` doubled as a signed 32-bit
  value and halved (`sar eax, 1`, `0x00473D97`, `0x00473DF7`), so a count from `0x40000000` up rebases no entry and
  still gets the bit (`0x00473D67`-`0x00473D9E`, `0x00473DC7`-`0x00473DFE`).
- In bytes, with `n` = `chunk[+4]`: `if (n >= 0) { if (n + n > 0) for (i = 0; i < (int32)(n + n) >> 1; i++)
  chunk[+8 + 4 × i] += (u32)chunk; chunk[+4] = n | 0x80000000; }` (`0x00473D60`-`0x00473D9E` for `0x02CA6C68`,
  `0x00473DC0`-`0x00473DFE` for `0x02CA6C70`).
- `0x00473BB0` reads step `j` of entry 0 and tests bit `min(progress / 5, 50)` of `shown` and `labelled`.
- `0x00473BB0`'s fourth argument is a 28-byte record it zeroes first (`0x00473BBA`-`0x00473BC8`): `+0x00` the type, for
  type 0 `+0x04` a, for type 1 `+0x08` a, `+0x0C` location and `+0x10` b, then `+0x14` and `+0x18` the `shown` and
  `labelled` bytes masked to that bit (`0x00473C6C`-`0x00473C80`).
- `0x00473B70(i)` returns the byte that entry `i`'s `entryAt` address (at `+8 + 4i` of the published `QHD0` chunk)
  points at, read as the step count by `0x0037EB90` (`0x0037EBE0`), `0x0037EC70` (`0x0037ECD1`), `0x003BC160` (`0x003BC1C9`)
  and `0x003BC4E0` (`0x003BC836`).
- The map-data widget takes the first type-1 step whose `shown` bit is set and looks its `location` up
  among the map's locations (`0x003BC160`, `0x003C0380`).
- For the location under the cursor, `0x003BDB30` answers 0 unless bits `0x100` and `0x200` of the map-data widget's
  `+0xD0` are set (`0x003BDBA4`-`0x003BDBB2`); it walks entry 0's steps up to the first that is not type 1 and takes the
  one with both bits set for that location whose rank among those is its third argument (`0x003BDBE0`-`0x003BDC3B`).
- While bit `0x400` is set, `0x003BDB30` takes that step's `second` label from `QHT0` (`0x00473CC0`) and answers 0 when
  the entry's `value` is not 1; with the bit clear the label is null. It hands back the step's `b` and the label
  (`0x003BDC43`-`0x003BDC7D`).
- `0x00473CC0(entry, step, first, second)` writes the addresses of the step's two labels to `first` and `second`,
  null for an offset of `0x8000` or more (`0x00473CE4`-`0x00473D14`), and returns the entry's `value` byte.
- `0x0037EB90` returns the location of the first step that applies, and `0x0037EC70` whether that step is type
  0 or type 1, which `0x0037E350` hands back to its caller.
- `0x0037EB90()` answers 0 with no widget at `0x02AED490` or with bit `0x100` of its `+0xE0`
  clear (`0x0037EBA3`-`0x0037EBCD`). Otherwise it asks `0x00473BB0(0, i, progress, record)` for
  each step `i` below `0x00473B70(0)`, the progress being `0x0046B180(word +0xEA)`, and
  answers the dword `+0x0C` of the first record whose dword `+0x14` is not 0, or -1 when
  no step has one (`0x0037EBE0`-`0x0037EC66`).
- `0x0037ED80()` returns that type, or 2 when no step applies; `0x003BC160`, `0x003C18A0` and `0x00578F50` call it.
- The map-data widget's `0x003BCAB0(widget)` turns the quest id at `+0xCC` into a record index
  (`0x0037EDB0`), keeps it at `+0xCE` and loads that quest's group file (`0x0037FD50`); with no such quest it
  returns 0.

### Address width

The chunk address is formed with a 32-bit addition (`0x0037FED9`-`0x0037FEDE`, `0x0037FF30`-`0x0037FF35`), the rebased
offsets are 32-bit (`0x00473D80`, `0x00473DE0`) and are read back sign-extended (`0x00473B7A`, `0x00473BD6`, `0x00473CD0`),
and the section-5 row address is 32-bit too (`0x0037E9D7`, `0x0037EF05`). The group file buffers must therefore lie
below 2 GB.

## Modding notes

- Keep `menuquest.dat`, the `.lst` directory and the group files in step: a quest's record in its group
  file is chosen by its position among that group's quests in `menuquest.dat`, and nothing checks the
  group file's `count`.
- Section 2's parts are separated by `0x03`; a progress row value larger than the part count shows all parts.
  Only 12 parts are read.
- The progress row has 52 values in steps of 5 of the progress byte; values past 50 for the map bits are
  read as step 50.
- The map chunks are rebased in place once per loaded buffer; ship them with bit `0x80000000` of `count` clear, or
  their offsets are used as addresses.
- A new group file needs a group number below 16, whose path is already in the array, and an entry in the
  size table ([File size tables](file-size-tables-fst.md)). Group 16 would request `menuquest.lst` (`0x13A`).
- A `.lst` threshold of 0 marks a hunt done as soon as its group file is loaded.

## Related

- [Clan Primer](../Menus-And-HUD/clan-primer.md): the Hunts page and how hunts are listed and marked read.
- [Quests](../Story-Events-And-Hunts/quests.md): the ordered and cleared bits and the scenario flag the menu reads.
- [Hunts](../Story-Events-And-Hunts/hunts.md): every hunt's name, petitioner, record text and the progress that shows each part.
- [TIM2 images](tim2-images.md): `menuquest.nfs` and the glyph-sheet registry.
- [Map screens](../Menus-And-HUD/map-screens.md): the map-data widget that draws the markers.
- [Text codes](../Menus-And-HUD/text-codes.md): the `0x02` and `0x03` codes in the detail text.
- [File size tables](file-size-tables-fst.md): the kind-7 paths and sizes.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 6 calls with 3 other topics</summary>

**Engine core** (explained on [global state accessors](../Engine-Core/global-state-accessors.md))

| Function | | Functions |
|---|---|---|
| `0x002465F0` | calls | `0x001EDDA0` |

**Saving, loading and settings** (explained on [mrp menu resource packages](mrp-menu-resource-packages.md))

| Function | | Functions |
|---|---|---|
| `0x00249210` | is called by | `0x00582790` |
| `0x00249410` | is called by | `0x00582790` |
| `0x00249580` | is called by | `0x00582790` |

**Controls and input** (explained on [controls](../Controls-And-Input/controls.md))

| Function | | Functions |
|---|---|---|
| `0x002D3900` | calls | `0x001E0A10`, `0x001E0E30` |

</details>
