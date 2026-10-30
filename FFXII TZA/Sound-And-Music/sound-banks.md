---
title: "Sound banks: the bank files that hold every sound effect, battle voice and music track, how each is named and found, and how a sound id names a bank and a slot"
kind: "format"
category: "Sound and music"
addresses: "0x007CFF90, 0x007CF6B0, 0x00223AD0, 0x00222DC0, 0x00222740, 0x0036ED50, 0x002E60F0, 0x003A1650, 0x003A1180, 0x002105E0"
---

## What the player sees

- Every sword hit, menu blip, spell and footstep plays from a sound bank; the game ships no loose sound files.
- Battle voices come from 46 banks per language: the party members, guests and summons the model sound tables
  name, and the Imperial soldiers, judges and other enemies whose battle records name one. Each language ships 66
  voice banks and the path arrays name `shout00`-`shout63`. Each bank holds ten lines: three for attacking, three
  for taking damage, two for a critical and two for being knocked out.
- Music plays from much larger bank files, one per track.

## Where it comes from

### The families

All banks are under `ps2data/sound`. The audio manager built by `0x002105E0` holds one controller per family, and
each controller's bank class names the family in its run-time type name.

| Family | Files | Name | Opened by | Manager |
|---|---:|---|---|---|
| block banks, `SebAudioBank` | 248 | `se/sead_data_win/se<n>/se<n>.win.sab`, three digits | `0x00223AD0`, format `"%s/se%03d/se%03d%s"` (`0x00908A38`) | `+0x08` |
| six-digit banks, `SepAudioBank` | 4,097 | `se/sead_data_win/se<id/1000>/se<id>.win.sab`, six digits | `0x00222DC0`, format `"%s/se%03d/se%06d%s"` (`0x009089A8`) | `+0x10` |
| battle voices, `ShoutAudioBank` | 66 per language | `shout/<us or jp>/shoutNN/shoutNN.win.sab` | `0x0036ED50`, by index from the path arrays of kinds 33 and 39 | `+0x20` |
| music, `MusicAudioBank` | 116 | `music/magi_data/win/musicNNN.win.mab` | `0x00222740`, format `"%s%03d%s"` from `PS2Data/sound/music/magi_data/win/music` (`0x009088E0`) | `+0x00` |
| block indexes | 248 | `se/block/se<n>.seb` | `0x002E60F0`, kind 32 | - |

The manager's fifth controller, at `+0x18`, is `StreamAudioController`. The two SE folders' root is
`PS2Data/sound/se/sead_data_win` (`0x00908950`), and `.win.sab` comes from `0x00908998`. Music ids run 7, 15-92,
94-116 and 200-213.

Every shipped bank and index is listed, with its header, contents, loader and what names it, in
[`sound-music-bank-files.tsv`](sound-music-bank-files.tsv), [`sound-se-bank-files.tsv`](sound-se-bank-files.tsv),
[`sound-block-index-files.tsv`](sound-block-index-files.tsv) and [`sound-voice-bank-files.tsv`](sound-voice-bank-files.tsv).
The columns are under Shipped data.

### Block banks and the block index

An actor's sound-effect record names up to three SE blocks as `u16` ids, bit `0x8000` meaning none. `0x002E60F0` turns each id
into an index into the kind-32 path array of 608 `.seb` paths at `0x01E7FCF0` (`0x002E6157`-`0x002E618E`). The array holds
`se000`, `se007`, `se001`-`se006`, then `se200`-`se499` from index 8 and `se700`-`se999` from index 308:

| Block id | Index |
|---|---|
| 0, 1, 2 | 0, 1, 3, which are `se000`, `se007` and `se002` |
| 3-499 | id - 192 |
| 500 and up | id - 392 |

So ids 200-499 and 700 and up name the file with the same number, and ids 192-199 name the first eight entries,
`se000`, `se007` and `se001`-`se006`. 247 of the 248 shipped `.seb` files are reached by
their own number, and `se007` by id 1. The index file is read into a block (`0x002E6277`) and registered by
`0x003A1650`.

### The block registry

`0x003A0C90(block)` keeps 64 records of `0x18` bytes at `0x02AEEDC0`, sorted by block number at `+0x04`:

1. A block already registered adds one to the use count at `+0x0E`, and the new copy of the file is freed.
2. A new block takes a free record, marks it in the bitmap at `0x02AEF3F0`, and is passed to `0x002DEF00(slot & 0x3F,
   file)`, which builds a `SebAudioBank` through `0x001DBD20`, `0x00210B60` and `0x0021B430` (`0x003A1650`).
3. `0x00223AD0` reads the index, stores the registry slot at bank `+0x3C` and the block number at `+0x38`, and opens the
   block's `.win.sab` (`0x00223CB1`-`0x00223D05`).

`0x002DEC10` reads an index's block number, the `i16` at `+0x08`, for `0x003A1650`. A record's handle is its generation
`+0x0A` over its index `+0x08`, and every user compares the whole handle before it trusts a record:

- `0x003A0F80(handle)` counts a use down. At 0, unless the record is permanent (`+0x0D`), it frees the slot's bank
  (`0x002DEEF0`, which hands `0x0021B430` no file), adds one to the generation, unlinks the record (`0x003A1750`) and puts
  it at the head of the free list `0x02AEF3D8`.
- `0x003A1750` takes a record out of its list through the links `+0x00` (next) and `+0x02` (previous) and sets both to
  `0xFFFF`.
- `0x003A0EA0`, run by `0x0036D890`, walks the records marked in the bitmap `0x02AEF3F0`. A record whose `+0x10` is set
  and for which `0x002DEE90` answers 0 gets state 2 at `+0x0C`, `+0x10` = 0 and its bitmap bit (by `+0x08`)
  cleared, and its file handle `+0x14` is released (`0x0036D200`) and freed (`0x00369800`).
- `0x003A1290(handle)` answers the record's byte `+0x0C` for `0x002E60F0`.

`0x003A13F0` loads three blocks once at start-up: blocks 0, 1 and 2, which `0x002ED8C0` maps to `se000`, `se007` and
`se002`. Their callbacks `0x003A1390`, `0x003A1330` and `0x003A12D0` register each one (`0x003A1650`), keep its handle at
`0x02AEF3FC`, `0x02AEF400` or `0x02AEF404`, and mark the record permanent.

The table holds 66 entries of the record layout, `0x02AEEDC0`-`0x02AEF3EF`: the 64 records, then two list heads.

- The start-up loop sets entry *r* to next *r* + 1 (`0x003A1447`), previous *r* - 1 (`0x003A144E`), block -1
  (`0x003A1454`), index *r* (`0x003A1443`) and generation and use count 0 (`0x003A145B`, `0x003A1457`), while *r* is below
  `0x42`, a signed 32-bit compare (`0x003A1463`).
- Entry 64 heads the list of registered records, sorted by block. `0x003A0C90` starts its walk at its `+0x00`
  (`0x003A0CA0`) and, for a block lower than every registered one, links the new record after it, taking its index
  `+0x08`, 64, as the new record's previous link (`0x003A0CB1`, `0x003A0CFF`, `0x003A0D66`).
- Entry 65 heads the free list. Its `+0x00` is `0x02AEF3D8`, and `0x003A0F80` gives a freed record its index `+0x08`,
  65, as the previous link (`0x003A101B`, `0x003A1039`).
- The start-up stores below close both lists, so records 0-63 form the free list and the block list is empty.
- A new block takes the free list's first record. With the free list empty `0x003A0C90` answers -1
  (`0x003A0D2C`-`0x003A0D35`), so at most 64 blocks are registered at once.
- Every link is an `i16` read sign-extended, and a negative link ends a walk.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AEEDC2` | `i16` | 0 | record 0's previous link: 65 at start-up, the free-list head | `0x003A13F0`: -1 (`0x003A144E`), then `0x41` (`0x003A1497`); the link updates, when record 0 is the record or a neighbour: `0x003A0C90` (`0x003A0D96`, `0x003A0DA3`), `0x003A0F80` (`0x003A1039`, `0x003A1047`), `0x003A1750` (`0x003A17AE`, `0x003A17B9`) | `0x003A1750` (`0x003A175C`), when record 0 is unlinked |
| `0x02AEF3A8` | `i16` | 0 | record 63's next link: -1 at start-up, the end of the free list | `0x003A13F0`: 64 (`0x003A1447`), then -1 (`0x003A1468`); the link updates: `0x003A0C90` (`0x003A0D9B`, `0x003A0DA8`), `0x003A0F80` (`0x003A103E`), `0x003A1750` (`0x003A17A5`, `0x003A17B6`) | `0x003A0C90` (`0x003A0CD4`, `0x003A0D63`); `0x003A1750` (`0x003A1764`) |
| `0x02AEF3C0` | `i16` | 0 | the block list's first record, entry 64's next link; -1 while no block is registered | `0x003A13F0`: 65 (`0x003A1447`), then -1 (`0x003A1481`); `0x003A0C90`, a new first record (`0x003A0DA8`); `0x003A1750`, when the first record is unlinked (`0x003A17A5`) | `0x003A0C90` (`0x003A0CA0`, which stops on a negative value at `0x003A0CBA`; `0x003A0D63`) |
| `0x02AEF3C2` | `i16` | 0 | entry 64's previous link: -1 at start-up | `0x003A13F0`: 63 (`0x003A144E`), then -1 (`0x003A1474`) | no instruction names it; `0x003A1750` reads the previous link only of the record it unlinks, the free list's first record (`0x003A0D5E`) or a record named by a handle (`0x003A100E`) |
| `0x02AEF3DA` | `i16` | 0 | entry 65's previous link: -1 at start-up | `0x003A13F0`: 64 (`0x003A144E`), then -1 (`0x003A148B`) | no instruction names it; as for `0x02AEF3C2` |

`0x003A13F0` is called once, by the boot `0x00266D10` (`0x00266DF0`).

### Sound ids

A sound id is `registry slot << 9 + sound slot`. `0x003A1180(slot)` builds it from the current block handle at
`0x02AEF3FC`. It answers -1 when `0x00267330(0)` is non-zero (`0x003A1180`-`0x003A118F`), or when that handle is -1 or its
record does not match (`0x003A11AB`-`0x003A11D1`).

`0x003A11F0(slot)` builds the same id without the `0x00267330` test, for `0x00249CA0`. `0x003A1100` and `0x003A1070` build ids
from the blocks at `0x02AEF400` and `0x02AEF404`. Both answer -1 while `0x02AEF400` is -1 (`0x003A1106`, `0x003A1076`), which
happens when block 1's callback `0x003A1330` stores a failed registration there (`0x003A1344`, `0x003A134A`).

Until that callback runs the word is 0: it is in the zero-filled tail of `.data`, and `0x003A13F0` stores -1 only to
`0x02AEF3FC` and `0x02AEF404` (`0x003A14BE`, `0x003A153D`, `0x003A15BC`). 0 is the handle of record 0 while its generation is 0, as the
start-up loop leaves it (`0x003A1443`, `0x003A145B`), so in that window `0x003A1100` answers the slot itself, an id in
registry slot 0 (`0x003A115E`), unless `0x00267330(0)` is non-zero, and `0x003A1070` passes its test and builds from
`0x02AEF404` once block 2 is loaded.

`0x0021B5B0(id)` finds the bank whose `+0x3C` equals `id / 512` (`0x0021B5DF`-`0x0021B5FA`). An index file has 128 slots,
so slots 128-511 of each id range name nothing.

### Six-digit banks

Effect and sound files carry `SeSep` records that name six-digit banks; 4,318 files hold them (2,304 `.snd`, 1,461
`.efx`, 545 `.mpk`, 7 `.cm`, 1 `.spp`). `0x002DF070` walks the records while each starts with `SeSep` and fits, and
calls `0x001DBE60(id, record + 0x10)` for each. `0x0021A040` skips an id already loaded, and `0x00222DC0` stores the id and
`id / 1000` and copies the record's `u32` and `u8` twice into the bank (`+0x40`/`+0x44`, `+0x45`/`+0x49`).

The sound records of effect files open their banks through the table of 32 entries of `0x84` bytes at `0x02EBBA00`.
The effect loader `0x00504060` adds an entry for a kind-1 record and opens its banks, or adds a reference to it
(`0x003D7CE0`); an entry holds the kind, a reference count `+0x02`, the bank id `+0x04` and up to 30 play handles:

- `0x003D7C50(kind, id, handle)` keeps a handle in the entry's first empty cell.
- `0x003D7E90(entry)` counts the handles that still play (`0x002DEE80`) and clears the rest.
- `0x003D7DC0`, run from `0x00258D70` and `0x00258E40`, empties every kind-1 entry with no reference and no playing
  handle and releases its bank (`0x002DF050`); it leaves kind-3 entries alone.

### Battle voices

`0x0036ED50` loads both languages of one voice bank. The index is the record's `i16` at `+0x14`.

- The kind-33 array at `0x01E127D0` holds the 64 `us` paths and ends there: the cell at `0x01E129D0` is 0.
- The kind-39 array at `0x01ECB7E0` starts with the 64 `jp` paths and goes on to other files: the cell at `0x01ECBBE0` is
  a live pointer.
- Each finished load finds its record by the handle, in `0x022D9AB0` when `handle & 0xF0` is 0 and otherwise in
  `0x022D9AE0`, at `handle & 0xF` times `0x18`. It registers the bank through `0x001DC130` with 1 for `us` (`0x0036EAB0`)
  and 0 for `jp` (`0x0036E9F0`).

`0x0036F000` answers 1 only when no record of either table is in state 1 or 2, so every voice load has finished.

### What names each bank

A music track number reaches the bank loader `0x00222740` only through the four track slots. `0x00361630` is called by
`musicread` (`0x0034174B`), the start of `musicplay` (`0x003427D6`), `0x0035CC57` and `0x0035CC82` with the area's track
from `0x0026DE00`, the two change tasks (`0x00360F3C`, `0x003613DF`) and the game-over task, which asks for track 7
(`0x003EF3D0`, `0x003EF42C`). The change tasks are scheduled by `0x003614E0`, which `0x003614C0` calls for the area's
track (`0x002620A8`) and for `musiccrossplay_22f` (`0x00347367`).

The area's track is the music table's (`0x003EAA70`), the saved override set by `setnowmapmusicno`, or `0x5A` in
chocobo mode and `0x5B` in summon mode ([Music](music.md)).

A block is registered through `0x003A0C90` from two places: `0x003A1650`, for the start-up blocks 0, 1 and 2
(`0x003A13F0`) and for the block ids of a model's `charseinfo` row (`0x002E60F0`), and the developer verb
`debug_registcharsep` `0x206F` (`0x0050CAB2`), which no shipped script calls.

A six-digit bank is opened only by `0x00222DC0`, reached from `0x002DF070` alone (`0x0021A0CB` <- `0x00210C40` <-
`0x001DBE60` <- `0x002DF0B8`). `0x002DF070` walks `SeSep` records for the map binder `0x003635E0` (`0x0036362D`, slot 0 of
the block pack), the event sound slots (`0x003DEC14`, `0x003DF3B7`) and the effect loader `0x00504060` (`0x00504149`).

A voice bank is loaded by `0x0036ED50` from the voice pool `0x0036F0F0` (`0x0036F224`), which the model rebuild calls
(`0x0037B896`) with the bank `0x002ED910` gives: an enemy's battle record word `+0x26` (`0x003212E0`, kind byte 1 at
`0x003212FF`), or else the model's `charseinfo` row
([Character sound tables](../Game-Files-And-Data-Tables/character-se-tables-chse.md)). The verb
`actoriopvoiceread` `0x0341` (`0x003466CB`) also feeds the pool, and no shipped script calls it.

## Layouts

All multi-byte fields are little-endian.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "sabf" in a .sab, "mabf" in a .mab |
| `+0x04` | `u8` | version | 2; below 2 the directory is at +dirDelta |
| `+0x05` | `u8` | flags | bit `0x1`: the bank's sound check `0x007A8CF0` takes sound 0 whatever number it is asked for (`0x007A8D94`-`0x007A8DA5`), and a music bank of version 2 or later answers that any number is present (`0x007A8E28`-`0x007A8E34`); set in every six-digit bank and every `.mab`, clear in the others |
| `+0x06` | `u16` | dirDelta | `0x10` |
| `+0x08` | `u8` | chunkCount | 4 in a .sab, 3 in a .mab |
| `+0x09` | `u8` | nameLength | length of the bank name at `+0x10` |
| `+0x0A` | `u16` | param | 1 makes the voice mixer drop the front-back pan |
| `+0x0C` | `u32` | fileSize | the file's length |

The bank name follows at `+0x10`, `nameLength` bytes and a zero. The chunk directory starts at
`((0x10 + nameLength) & 0xF0) + dirDelta`, which is `0x20` in every shipped file.

In a six-digit bank the name at `+0x10` is the folder, `se<id/1000>`, and the bank's one sound carries the file's
own name, `se<id>`. Block and voice banks carry the file's name, and every music bank carries `music`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | tag | "snd " "seq " "trk " "mtrl" in a .sab; "musc" "inst" "mtrl" in a .mab |
| `+0x04` | `u32` | flags | `0x00100000` |
| `+0x08` | `u32` | offset | from the start of the file |
| `+0x0C` | `u8[4]` | pad | 0; read by no function: `0x007CF6B0` and `0x007D0580` read the tag and the offset, and the five functions that call `0x007CF6B0` (`0x007D0210`, `0x007D0580`, `0x007E3450`, `0x007E3CF0`, `0x007E48D0`) read the offset `+0x08` of the entry it returns and not its `+0x0C`; nothing fixes its width |

The records the game reads in a sound bank's `snd ` chunk:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x02` | `u16` | nameOffset | the sound's name, from the record's start |
| `+0x04` | `u8` | playable | 0 makes `0x007A8CF0` refuse the sound (`0x007A8DE3`); 1 in every playable shipped sound |
| `+0x08` | `u16` | number | the number `0x007A8F40` matches when an id carries bit `0x40000000` (`0x007A8F94`-`0x007A8F9D`); equal to the record's position in every block and voice bank |

The music header fields that name its sections that name its sections (the readers are on [Interactive music](interactive-music.md)):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x02` | `u16` | nameOffset | the music's name, `music<NNN>` in every shipped bank |
| `+0x04` | `u8` | sectionCount | 3 in every shipped bank; section *n* is music version *n* |
| `+0x48` | `u8` | nameLength | the offset table follows the name, at `nameOffset + ((nameLength + 0x10) & 0xF0)` |

A section header gives its name offset at `u16 +0x02` and its name length at byte `+0x04`.

A material record holds its header size at `u16 +0x02`, the channels at byte `+0x04`, the codec at `+0x05`, the
rate at `u32 +0x08` and the loop region at `+0x0C`-`+0x10` (`0x007EBAD0`, [Sound engine](sound-engine.md)). The
codec header's size follows at `u32 +0x14` and the sample data's size at `+0x18`; in every shipped material the
header, the codec header and the data end exactly at the next material or at the file's end.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | magic | "SeBlock " |
| `+0x08` | `i16` | block | the number in the file name |
| `+0x0A` | `i16` | slotCount | 128 |
| `+0x0C` | `u32` | fileSize | the file's length |
| `+0x10` | `i32[128]` | slotOffset from +0x210; -1 for an empty slot |  |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | word | copied as a dword twice into the slot's node by `0x00223AD0`, read by no bank method |
| `+0x04` | `u8` | flags | the slot's start flags, read when the sound starts (`0x00224570`) |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[5]` | magic | "SeSep" |
| `+0x08` | `i32` | id | the six-digit bank id |
| `+0x0C` | `u32` | size | record length in the bits `0x7FFFFFFF` |
| `+0x10` | `u32` | word | copied to bank `+0x40` and `+0x45` |
| `+0x14` | `u8` | flags | copied to bank `+0x44` and `+0x49` |

## Shipped data

Every value below holds in all 4,609 `.sab`, 116 `.mab` and 248 `.seb` files:

| Field | `.sab` | `.mab` |
|---|---|---|
| magic, version, `dirDelta` | `sabf`, 2, `0x10` | `mabf`, 2, `0x10` |
| chunks | `snd `, `seq `, `trk `, `mtrl` | `musc`, `inst`, `mtrl` |
| name length | 5 for `se` banks, 7 for `shout` banks | 5 |
| `+0x05` | 1 in the 4,097 six-digit banks, 0 in the 248 block banks and 264 voice banks | 1 |
| `+0x0A` | 350 values; 1 in 157 banks, starting `se001001` | 10,000 |
| `fileSize` equals the length; chunk offsets rising, the first at the directory's end | yes | yes |

The `.seb` files are `se000`, `se002`, `se007`, `se200`-`se434` and `se700`-`se709`, 708 to 24,968 bytes, with
4,404 slots present. The slot flag byte takes the values 0 (2,647 slots), 128 (1,574), 1 (133), 4 (33), 5 (11), 17
(5) and 8 (1).

### The music banks

Each of the 116 `.mab` banks holds one music of three sections, two-channel HCA at 48,000 Hz. Section 0 is named
for its recording, for example `31_FinalFantasyXII-GameOver` in `music007`; section 1 is `bgm_<NNN>` in most
banks; section 2 `bgm_<NNN>s` in most. The game starts every music in the section of the music version option
([Music](music.md)), which the settings reset sets to 1 (`0x002DF530(1, 1)`,
[Game settings](../Saving-Loading-And-Settings/game-settings.md)). Banks 208, 209, 210 and 212 name their sections `E2NN` and track 211
`bgm_211`.

| Track | Section 0 |
|---|---|
| 7 | the game-over music, `31_FinalFantasyXII-GameOver` |
| 90 | the chocobo music, `59_FinalFantasyXII-Chocobo(FFXIIVersion)` |
| 91 | the summon music, `74_FinalFantasyXII-Esper` |

The other 113 are in [`sound-music-bank-files.tsv`](sound-music-bank-files.tsv). Tracks 102, 106 and 114 carry the
same three section names as 61, 95 and 72.

### The block banks

The 248 block banks hold 6,395 sound records. 4,410 have byte `+0x04` set and can play; 1,985 are empty. The
`.seb` slots name 4,376 of the playable sounds, one slot names an empty sound (`se301` slot 21), and 27 slots lie
past their bank's last sound:

| Block | Slots | Bank sounds | What does not match |
|---|---:|---:|---|
| `se007` (block 1) | 1-4 | 0-3 | slot 4 is past the bank; sound 0 has no slot |
| `se228`, `se241` | 0-18, 32-43 | 0-30 | slots 32-43 are past the bank; sounds 19-30 have no slot |
| `se301` | 0-12, 21, 22 | 0-22 | slot 21 names an empty sound; playable sound 13 has no slot |
| `se330`, `se331` | 0-9, 21, 22 | 0-22 | playable sounds 10-12 have no slot |
| `se353` | 0-12, 21-24 | 0-22 | slots 23 and 24 are past the bank; playable sounds 15 and 16 have no slot |

A slot past the bank or naming an empty sound plays nothing (Loader behaviour), and a sound with no slot cannot be
reached by id. In the 241 other blocks every slot names a playable sound and every playable sound has a slot.

### The six-digit banks

Each six-digit bank holds one sound, named as its file, and one HCA material: 3,251 stereo and 846 mono, 4,080 at
48,000 Hz and 17 at 44,100 Hz, 0.11 to 153.81 seconds long. The folder says what plays them:

| Folders | Banks | Named by |
|---|---:|---|
| `se001` | 157 | map sound lists; ids 1,001-1,999 are the ambiences ([Map sounds](map-sounds.md)) |
| `se010`, `se050` | 502 | map sound lists |
| `se100`, `se101`, `se150`, `se151` | 601 | effect files' sound records |
| `se600`-`se610` | 2,829 | cutscene sound lists in `.snd` packs |
| `se650` | 8 | nothing |

### Battle voice lines

Each language's 66 voice banks hold ten lines per character, named `ve` (English) or `vj` (Japanese), a character
code, a number and an event: 198 `at` (attack), 198 `dm` (damage), 130 `crt` (critical) plus 2 spelt `ctr`, and
132 `dead`. Nine `us` banks, all summons, hold an eleventh line named `vefah_01` and a code.

In five of them, `shout18` (Famfrit), `shout22` (Zodiark), `shout24` (Hashmal), `shout25` (Zalera) and `shout28`
(Mateus), that line is sound 0 and the ten battle lines are sounds 1-10; in the other four and in every `jp` bank
the battle lines are sounds 0-9.

A voice id carries the animation variant, 0-9, as its sound number (`0x002E9F9E`, `0x003A0E30`-`0x003A0E3F`,
`0x00224F5B`). So in English those five summons say the `vefah_01` line where the Japanese voice says the first
attack line, each later variant plays the line before its Japanese counterpart, and no animation sound reaches
`ve<code>_10dead`: the route stops at variant 9 (`0x002E9F79`).

### Files nothing loads

- 132 `.orb.sab` voice banks, 66 per language, each beside a `.win.sab` of the same name; the executable holds no
  `.orb` string.
- `shout64` and `shout65` in both languages: the kind-33 and kind-39 arrays name only `shout00`-`shout63`.
- 18 more voice banks in each language, `shout35`-`shout39`, `shout41`-`shout45`, `shout48`-`shout50`, `shout54`,
  `shout55`, `shout58`, `shout61` and `shout62`: no `charseinfo` row and no battle unit names them.
- Music tracks 24 (`A Small Bargain`), 25 (`A Small Happiness`), 43 (`Battle Drum (Incomplete)`), 106 and 112
  (`Sky Fortress Bahamut (Partial Loop)`): no music-table run, override, mode track, game-over call or script
  argument names them.
- 28 blocks, `.seb` and `.win.sab` both: 206, 216, 220, 228, 330, 375-389, 395, 399-401, 407 and 413-415. No
  `charseinfo` row names them and they are not start-up blocks.
- 59 six-digit banks that no `SeSep` record in any shipped file names, among them all 8 of `se650`; the list is in
  the `used` column of [`sound-se-bank-files.tsv`](sound-se-bank-files.tsv).
- 2 more six-digit banks named only where the game never opens the record: 600173 and 600181, in slot 1 of the
  `sum_a0000` and `sum_c0000` cutscene packs, which their scripts never read.

One record names a bank that does not ship: `600070`, in slot 7 of `sum_a0001.snd`. The scene's script reads slots
0-6 only, in all nine languages, so the record is never opened.

## Loader behaviour

1. `0x007CFF90` accepts a bank only when its first four bytes equal `sabf`, the constant at `0x00D115B4`, and refuses a
   null pointer (`0x007CFF93`-`0x007CFFA0`). `0x007D07A0` is the same test for `mabf` (`0x01CB6FB8`).
2. `0x007CF6B0` finds a chunk by tag: with version 2 or more it starts the directory after the name, rounded down to 16,
   plus `dirDelta` (`0x007CF6B7`-`0x007CF6D4`), and walks `chunkCount` records of 16 bytes (`0x007CF6DC`-`0x007CF704`). A tag
   that is not there gives a null chunk (`0x007CF710`).
3. A chunk's offset is added to the file's base (`0x007D05A9`). Nothing compares an offset or `chunkCount` with
   `fileSize`.
4. The voice path `0x007EDE90` reads `+0x0A` (`0x007EE01D`) and, when it is 1, passes zero as the front-back pan
   (`0x007EE02B`-`0x007EE031`).
5. `0x00223AD0` checks the index's block number against the one asked for only through `_guard_check_icall`
   (`0x00223B53`-`0x00223B5F`), which does not branch.
6. It walks `slotCount` slots (`0x00223B72`), skips an offset of -1,
   and copies each slot's `u32` and `u8` into a 10-byte node at `+0x00`/`+0x04` and again at `+0x05`/`+0x09`. It reads
   nothing past the slot's fifth byte. The `SeBlock` string does not occur in the executable, so no code compares
   the magic.
7. The driver reads every record through small wrapper classes, named by their run-time types. A chunk wrapper skips
   the chunk's name padding (`(byte +0x09 + 0x10) & 0xF0` from version 2) and indexes its offset table at `u16`
   `+0x02`; the record accessors that check the index refuse one at or past the count `u16` `+0x04`:

| Class | Accessor |
|---|---|
| `SoundChunk`, `Sound` | `0x007CFB30`, `0x007CFB00` |
| `SequenceChunk`, `Sequence` | `0x007CFA30`, `0x007CF9E0` |
| `TrackChunk`, `Track` | `0x007CFC70`, `0x007CFC20` |
| `MaterialChunk`, `Material` | `0x007CF8B0`, `0x007CF860`; `0x007CF940` reads a material's offset and `0x007CF960` the offset table's size rounded up to 16 |
| `SoundEffect`, `SoundEffectFlangerParam` | `0x007CF780`, `0x007CF810` |
| `ZeroOne`, `SoundZeroOneParam` | `0x007CFE60`, `0x007CFF40` (from sound version 12, `0x20`-byte records at `u16` `+0x4C`) |

`0x007CF540` and `0x007CF560` build the `AudioBinaryFile` and `SabFile` wrappers, `0x007CF580` drops one, `0x007CF740` gives
the address a version-dependent `u16` of a record points to (`+0x02`, `+0x0E`, `+0x16` or `+0x06` for versions 0, 1, 2
and later), `0x007CF980` a record's zero-one count (2 below version 3, byte `+0x08` after) and `0x007CFD00` a zero-one
curve's value at a point: the input scaled into 0-1 by the curve's range, then a binary search over its 16-byte
points.

In `0x007CFD00`, with the curve header's count `u16 +0x04` (0 gives 0), range `+0x08`..`+0x0C` and points at
`u16 +0x02` past the header, moved on by `(byte +0x01 + 0x10) & 0xF0` when byte `+0x00` is above 3 (`x +0x00`, `y +0x04`, ease byte `+0x08`): `x = clamp((input - min) / (max - min), 0, 1)` when the
header's first byte is non-zero (0 when `max <= min`), the search finds the last point `k` with `x[k] <= x`, and the
value is `y[k] + 0x007A9E50((x - x[k]) / (x[k + 1] - x[k]), ease[k]) x (y[k + 1] - y[k])`, or `y[k]` at the last point
(`0x007CFD00`-`0x007CFE5B`).

8. A six-digit or block bank whose file cannot be read stops the game. The load thread leaves the bank's data
   pointer at 0 when the file gives no length (`0x00212293`-`0x0021229E`), and the completion stores to address 0:
   `0x00222F9E` for a six-digit bank, `0x00223E1E` for a block bank.
9. The six-digit pool holds 256 banks. When every bank is taken and the sweep (`0x00212860`) frees none, the take
   answers 0 (`0x00219A4F`) and `0x0021A0BF` stores through it at address `0x60`.
10. A block sound plays only when its slot is in the index, `id & 0x1FF` (`0x002245D3`, `0x0022462A`), the slot is below
    the bank's sound count (`0x007A8DB8`-`0x007A8DC6`) and the sound's byte `+0x04` is set (`0x007A8DE3`); otherwise
    nothing plays (`0x00224651`).
11. `0x00223AD0` reads the slot count as a signed word (`0x00223B72`, `0x00223BBA`), so a negative count registers no
    slots.
12. Each track number keeps a resume point in two 256-entry tables of the object manager, `+0x3D8` (`f32`) and
    `+0x7D8` (`u8`). Their bound checks only call the empty `0x0016D6A0` (`0x00221737`, `0x00221112`, `0x00220DB2`), so a
    track of 256 or more writes its position over the flag bytes and its flag past the `0x8D8`-byte object
    (`0x00221748`, `0x00221756`).
13. The animation-sound route sends a variant to the voice bank only below 10 (`0x002E9F79`); a higher variant
    plays from the block instead.

## Modding notes

- A block bank is found by its number: `se<n>/se<n>.win.sab`, where `n` is the index file's block number; a
  six-digit bank by `se<id/1000>/se<id>.win.sab`.
- A bank name of 16 characters or more moves the chunk directory unless `dirDelta` grows with it.
- An index with more than 128 slots walks past its offset table; sound slots 128 and up are not reachable by id.
- Block ids 3-191 give a negative index, 192-199 read the array's first eight entries, and 500-699 land on another
  block's file (500 reads `se300`).
- Editing an `.orb.sab` file changes nothing on PC.
- A replacement `.sab` needs the magic `sabf`, version 2, the chunk directory where the name length puts it, and
  the four chunks; their order and `fileSize` are free. A material may use codec 1 (PCM), 2 (MS ADPCM), 3 (Vorbis)
  or 7 (HCA); codec 4, the `.orb` format, is refused ([Sound engine](sound-engine.md)).
- In a block bank, slot *n* of the `.seb` plays sound *n*, which must have byte `+0x04` set. Keep the index's
  block number equal to the file's number: the registry and the `.win.sab` path both use it.
- A six-digit bank plays its sound 0. Every id a loaded map, cutscene or effect record names must have its file,
  or the load stops the game (`0x00222F9E`).
- A voice bank's sound *n* is variant *n*: three attack lines, three damage lines, two critical lines, two
  knock-out lines, in that order.
- A replacement `.mab` needs the magic `mabf` and three sections; a track number must stay below 256.

## Related

- [Escape Mode](../Controls-And-Input/escape.md) - plays block slot `0x52` and `0x2A` through `0x003A1180`.
- [Sound engine configuration](sound-engine-config.md) - the configuration file beside the banks.
