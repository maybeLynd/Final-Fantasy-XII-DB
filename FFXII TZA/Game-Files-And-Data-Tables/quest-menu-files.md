---
title: "Quest menu files: the menuquest list, petitioner strings and per-group detail tables, how they are read, and what each field shows"
kind: "format"
category: "Game files and data tables"
addresses: "0037F4D0, 0037F440, 0037F3B0, 02AED490, 0037F1F0, 003800D0, 0037FD50, 0037FBA0, 0037FA80, 0037E5B0, 0037EFC0, 0037EE10, 0037EF70, 0037EAA0, 0037E8D0, 00577C30, 005789D0, 00578450, 0037FEA0, 00473D50, 00473DB0, 00473BB0, 00473CC0, 02CA6C68, 02CA6C70, 0037F7C0, 0037FA00, 0037F140"
---

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
| `menuquest.dat` | `128`<sub>h</sub> | the quest list (`qstd`) |
| `menuquest.nfs` | `129`<sub>h</sub> | a TIM2 glyph sheet ([TIM2 images](tim2-images.md)) |
| `menuquest00.bin` to `menuquest02.bin` | `12A`<sub>h</sub> + group | the detail table of one quest group |
| `menuquest.lst` | `13A`<sub>h</sub> | the petitioner lines (`qstl`) |

The `us` kind-7 path array also names `menuquest03.bin` to `menuquest15.bin` (`12D`<sub>h</sub>-`139`<sub>h</sub>), which do
not ship. `menuquest.h`, in the `us`, `cn` and `kr` folders, is a C header with the quest count (66),
the highest quest id (172) and the group count (3); the quest ids `128`<sub>h</sub>-`13A`<sub>h</sub> do not include it. The `questtim2` folders of `ch`
and `in` hold six `q_c00`-`q_c05.tm2` pictures.

## Layouts

### menuquest.dat

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | "qstd"; the readers ignore it |
| `04`<sub>h</sub> | `u32` | version | 100; not read |
| `08`<sub>h</sub> | `u16` | groups | 3; not read |
| `0A`<sub>h</sub> | `u16` | count | records; bounds every index (`0037E5B0`) |
| `0C`<sub>h</sub> | `rec[count]` | 8 bytes each |  |

A record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | text | the quest's name, a message id (`002F9920`) |
| `04`<sub>h</sub> | `u32` | key | bits 0-7 group; bits 8-17 quest id; bits 20-27 row picture; bits 18-19 not read |

A quest's position is its index among the records of its own group; it selects the quest's record in
the group's `.bin` file (`0037FD50`).

### menuquest.lst

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | "qstl"; the readers ignore it |
| `04`<sub>h</sub> | `u32` | version | 100; not read |
| `08`<sub>h</sub> | `u16` | stringsAt | base of the string offsets (`0037F02A`) |
| `0A`<sub>h</sub> | `u16` | zero |  |
| `0C`<sub>h</sub> | `u16` | zero |  |
| `0E`<sub>h</sub> | `u16` | count | directory entries (`0037EFD9`) |
| `10`<sub>h</sub> | `dir[count]` | 8 bytes each |  |

A directory entry:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | quest | quest id; the first entry with the id wins (`0037EFF0`) |
| `02`<sub>h</sub> | `u16` | textAt | offset of the petitioner line from stringsAt; `FFFF`<sub>h</sub> = empty (`0037F01C`) |
| `04`<sub>h</sub> | `u8` | threshold | low nibble: the progress part at which the row picture changes (`0037E6A6`) |
| `05`<sub>h</sub> | `u8[3]` | zero |  |

The strings are the game's encoded text, zero-terminated. A quest with no entry gets an empty line.

### menuquest00.bin to menuquest02.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | sectionAt[6] | offset of each section |
| `0C`<sub>h</sub> | `u16` | pad | `FFFF`<sub>h</sub>; not read |
| `0E`<sub>h</sub> | `u16` | count | records; not read, the records are indexed by position |
| `10`<sub>h</sub> | `rec[count]` | 20 bytes each |  |

A record, at `10h + 20 x position`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | item[6] | offset of the quest's item in each section, from sectionAt[s]; `FFFF`<sub>h</sub> = none |
| `0C`<sub>h</sub> | `u16` | fill[4] | `0FFF`<sub>h</sub>; not read |

No reader uses `item[5]`: the progress row is found by position. The sections:

| Section | Content | Reader |
|---|---|---|
| 0, 1, 2 | zero-terminated text; `FFFF`<sub>h</sub> in `sectionAt` or `item` gives an empty string | `0037E8D0` |
| 3 | a `QHD0` chunk per quest, the map steps | `0037FEA0` → `00473D50` |
| 4 | a `QHT0` chunk per quest, the map labels | `0037FEA0` → `00473DB0` |
| 5 | 28 bytes per quest at `sectionAt[5] + 28 x position` | `0037EF70`, `0037EE10` |

Section 2 holds the parts of the quest record, separated by `03`<sub>h</sub>; within a part `02`<sub>h</sub> breaks the line.
A section-5 row is 52 four-bit values, value `k` in byte `k / 2` (the high nibble for odd `k`), then
two zero bytes. Value `k` is the number of parts shown while the quest's progress byte divided by 5 is
`k` (`0037EF70`).

Both chunks start the same way:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | "QHD0" or "QHT0"; the readers ignore it |
| `04`<sub>h</sub> | `u32` | count | entries; bit 31 is set once the offsets are made addresses |
| `08`<sub>h</sub> | `u32` | entryAt[count] | offset of each entry from the chunk |

A `QHD0` entry, read by `00473BB0(entry, step, progress)`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | steps | step records that follow |
| `01`<sub>h</sub> | `u8` | type | 0 or 1 |
| `02`<sub>h</sub> | `step[steps]` | 18 bytes each: |  |
| `00`<sub>h</sub> | `u8` | a | type 0: returned alone; type 1: returned with b and location |
| `01`<sub>h</sub> | `u8` | b |  |
| `02`<sub>h</sub> | `u16` | location | the location the map marks (type 1) |
| `04`<sub>h</sub> | `u8` | shown[7] | bit n: the step applies while progress / 5 is n (n at most 50) |
| `0B`<sub>h</sub> | `u8` | labelled[7] | bit n: the location carries the step's label then |

A `QHT0` entry, read by `00473CC0(entry, step)`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | count | label pairs; not read |
| `01`<sub>h</sub> | `u8` | value | returned by `00473CC0` |
| `02`<sub>h</sub> | `u16` | zero |  |
| `04`<sub>h</sub> | `{u16 first, u16 second}[]` | per step: offsets of two label strings from the entry; `8000`<sub>h</sub> and up = none |  |

## Shipped data

| Fact | Value |
|---|---|
| languages | `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us`; every folder has all six loaded files |
| `menuquest.dat` | 540 bytes, identical in all nine: 66 quests, group 0 19 (ids 0-22), group 1 45 hunts (ids 128-172), group 2 2 (ids 50, 51) |
| hunt row pictures | bits 20-27 run 19 to 63 for the hunts |
| `menuquest.lst` | 1,684 (`in`) to 2,036 (`es`) bytes; 66 entries naming the same 66 ids, `stringsAt` `220`<sub>h</sub> |
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
| size table | the US table sizes `128`<sub>h</sub>-`12C`<sub>h</sub> and `13A`<sub>h</sub> only |

## Loader behaviour

### The quest data widget

`0037F4D0` is the quest data widget, published at `02AED490` (only one exists: its openers `0037F3B0` and
`0037F440` refuse while the global is set). Bytes passed at creation select what it loads:

| Byte | Bit of `+E0`<sub>h</sub> | Effect |
|---|---|---|
| 0 | `2`<sub>h</sub> | after the first load, request `menuquest.nfs` |
| 2 | `8`<sub>h</sub> | load resource group `15`<sub>h</sub> |
| 3 | `10`<sub>h</sub> | load `menuquest.lst` into `+D0`<sub>h</sub> |

`menuquest.dat` always loads, into `+C8`<sub>h</sub>. The Hunts page opens it with all four bytes 1
(`0037F440` at `00579F1E`); the map-data widget's request `003BC9F0` (`003BCA48`) and `0037E350` open it with all four 0,
and `003F4E70` through `0037F3B0` with byte 2 only. When `menuquest.nfs` arrives `0037F1F0` keeps it at
`+D8`<sub>h</sub> and registers it as a glyph sheet (`0039BEC0`, `0017FBC0(5)`).

Group files load on demand: `0037FD50(index)` finds the quest's group and position and posts a request,
and `003800D0` asks for id `12A`<sub>h</sub> plus the group. Asking for another group releases the other group
files first (`0037FA80`), so one group's table is held at a time.

The widget lists the group files it asked for at `+F0`<sub>h</sub>: `18`<sub>h</sub>-byte entries, count `+EE`<sub>h</sub>, each with a
state byte (1 loaded, 2 loading, 3 dropped on arrival) and the buffer at `+10`<sub>h</sub>.

- `0037F7C0(widget, i, force)` removes entry i and returns 1: a loaded or forced entry has its buffer
  freed (`003697F0`); an entry still loading is marked 3 and kept, returning 0.
- `0037FA00(widget)`, called from the widget procedure `0037F4D0`, frees `menuquest.dat` (`+C8`<sub>h</sub>) and
  every listed buffer and empties the list.
- `0037F340(widget)` sends `{10h, 8}` to the owner's handler at `+C0`<sub>h</sub>, then sets bit `1`<sub>h</sub> of `+E0`<sub>h</sub>
  and `+E5`<sub>h</sub> = 2. `0037F190(owner, entry)` sends `{10h, entry byte 1, its word +4 when that byte is 2}`.
- `0037F050()` answers whether no quest data widget exists, and `0037F160()` returns `+E0`<sub>h</sub> bit 7, or 0
  with none; the map-data widget's `003BBFB0` reads both.
- `0037E4F0(owner)` closes the widget for an owner. While `+E0`<sub>h</sub> bit 7 is set it sends `{10h, 10}` to the
  owner at once. Otherwise it unregisters the glyph sheet (`0037F860`), keeps the owner at `+C0`<sub>h</sub> and sets
  `+E5`<sub>h</sub> to 3 when that returns 0, or to 4 with a close request (`00244F00`) and `{10h, 9}` to the owner.
  With no widget the owner gets `{10h, 9}`. `0037E350`, `003F4E70` and `00579420` call it.
- `0037EDB0(id)` returns the index of the `menuquest.dat` record whose key holds quest id `id`, or -1, and
  `0037E8A0(i)` returns record i's name, or the empty string `01CEB638` past the count.

### Hunt rows

`0037EAA0(row, group)` counts, in record order, the quests of the group that are cleared (`0046B1A0`) or
ordered (`0046B240`). `0037E5B0` then reads the quest: its name, id, picture byte, position and group
from `menuquest.dat`, and its threshold and petitioner line from `menuquest.lst` (`0037EFC0`). The row
builder `00577C30`:

- shows the name, and the petitioner line drawn with the `menuquest.nfs` sheet (`00577D7F`-`00577D95`);
- for group 1, treats the hunt as done when its current progress part (`0037EE10`) is at least the
  `.lst` threshold; for other groups, when the quest is cleared;
- picks picture sheet `2 x (picture / 24)`, plus 1 when done, and cell `picture % 24`; a sheet number of
  6 or more becomes sheet 0.

`0037EE10` needs the group's `.bin` loaded; without it the row counts as not done.

### The detail pane

When the group file has loaded, `0037E8D0` fills the pane's record: quest id, name, the progress part
count from section 5, the section 0, 1 and 2 strings and the `.lst` line. `005789D0` builds two text
panes through `00578450`:

1. Section 0, followed, once the quest is cleared, by an empty line and section 1.
2. Section 2 cut at each `03`<sub>h</sub> into at most 12 parts, of which the first `progress part count` are shown.

The progress byte is the quest's scenario byte, save `+1064h + quest` (`0046B180`; [Quests](../Story-Events-And-Hunts/quests.md)).

### Map markers

Whenever the selected quest's group file is ready (`0037F1F0`, `0037FBA0`), `0037FEA0` takes the quest's
`QHD0` chunk at `sectionAt[3] + item[3]` and its `QHT0` chunk at `sectionAt[4] + item[4]`. `00473D50`
and `00473DB0` publish them at `02CA6C68` and `02CA6C70` and, the first time, add the chunk's address to
each `entryAt` and set bit 31 of `count`. Widget bits `100`<sub>h</sub> and `200`<sub>h</sub> say whether each chunk is set. `0037F140()` returns bit `200`<sub>h</sub>, or 0
when no widget exists; the map-data widget's procedure `003BC4E0` reads it.

- `00473BB0` reads step `j` of entry 0 and tests bit `min(progress / 5, 50)` of `shown` and `labelled`.
- `00473B70(i)` returns the byte that entry `i`'s `entryAt` address (at `+8 + 4i` of the published `QHD0` chunk)
  points at, read as the step count by `0037EB90` (`0037EBE0`), `0037EC70` (`0037ECD1`), `003BC160` (`003BC1C9`)
  and `003BC4E0` (`003BC836`).
- The map-data widget takes the first type-1 step whose `shown` bit is set and looks its `location` up
  among the map's locations (`003BC160`, `003C0380`).
- For the location under the cursor, `003BDB30` finds a type-1 step with both bits set for that location
  and takes its `second` label from `QHT0` (`00473CC0`).
- `0037EB90` returns the location of the first step that applies, and `0037EC70` whether that step is type
  0 or type 1, which `0037E350` hands back to its caller.
- `0037ED80()` returns that type, or 2 when no step applies; `003BC160`, `003C18A0` and `00578F50` call it.
- The map-data widget's `003BCAB0(widget)` turns the quest id at `+CC`<sub>h</sub> into a record index
  (`0037EDB0`), keeps it at `+CE`<sub>h</sub> and loads that quest's group file (`0037FD50`); with no such quest it
  returns 0.

### Address width

The chunk address is formed with a 32-bit addition (`0037FED9`-`0037FEDE`), the rebased offsets are
32-bit and are read back sign-extended (`00473B7A`), and the section-5 row address is 32-bit too
(`0037E9D7`). The group file buffers must therefore lie below 2 GB.

## Modding notes

- Keep `menuquest.dat`, the `.lst` directory and the group files in step: a quest's record in its group
  file is chosen by its position among that group's quests in `menuquest.dat`, and nothing checks the
  group file's `count`.
- Section 2's parts are separated by `03`<sub>h</sub>; a progress row value larger than the part count shows all parts.
  Only 12 parts are read.
- The progress row has 52 values in steps of 5 of the progress byte; values past 50 for the map bits are
  read as step 50.
- The map chunks are rebased in place once per loaded buffer; ship them with bit 31 of `count` clear, or
  their offsets are used as addresses.
- A new group file needs a group number below 16, whose path is already in the array, and an entry in the
  size table ([File size tables](file-size-tables-fst.md)). Group 16 would request `menuquest.lst` (`13A`<sub>h</sub>).
- A `.lst` threshold of 0 marks a hunt done as soon as its group file is loaded.

## Related

- [Clan Primer](../Menus-And-HUD/clan-primer.md): the Hunts page and how hunts are listed and marked read.
- [Quests](../Story-Events-And-Hunts/quests.md): the ordered and cleared bits and the scenario byte the menu reads.
- [Hunts](../Story-Events-And-Hunts/hunts.md): every hunt's name, petitioner, record text and the progress that shows each part.
- [TIM2 images](tim2-images.md): `menuquest.nfs` and the glyph-sheet registry.
- [Map screens](../Menus-And-HUD/map-screens.md): the map-data widget that draws the markers.
- [Text codes](../Menus-And-HUD/text-codes.md): the `02`<sub>h</sub> and `03`<sub>h</sub> codes in the detail text.
- [File size tables](file-size-tables-fst.md): the kind-7 paths and sizes.
