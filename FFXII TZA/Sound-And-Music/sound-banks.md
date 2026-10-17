---
title: "Sound banks: the bank files that hold every sound effect, battle voice and music track, how each is named and found, and how a sound id names a bank and a slot"
kind: "format"
category: "Sound and music"
addresses: "007CFF90, 007CF6B0, 00223AD0, 00222DC0, 00222740, 0036ED50, 002E60F0, 003A1650, 003A1180, 002105E0"
---

## What the player sees

- Every sword hit, menu blip, spell and footstep plays from a sound bank; the game ships no loose sound files.
- 66 characters call out in battle, each with ten lines: three for attacking, three for taking damage, two for a
  critical and two for being knocked out.
- Music plays from much larger bank files, one per track.

## Where it comes from

### The families

All banks are under `ps2data/sound`. The audio manager built by `002105E0` holds one controller per family, and
each controller's bank class names the family in its run-time type name.

| Family | Files | Name | Opened by | Manager |
|---|---:|---|---|---|
| block banks, `SebAudioBank` | 248 | `se/sead_data_win/se<n>/se<n>.win.sab`, three digits | `00223AD0`, format `"%s/se%03d/se%03d%s"` (`00908A38`) | `+08`<sub>h</sub> |
| six-digit banks, `SepAudioBank` | 4,097 | `se/sead_data_win/se<id/1000>/se<id>.win.sab`, six digits | `00222DC0`, format `"%s/se%03d/se%06d%s"` (`009089A8`) | `+10`<sub>h</sub> |
| battle voices, `ShoutAudioBank` | 66 per language | `shout/<us or jp>/shoutNN/shoutNN.win.sab` | `0036ED50`, by index from the path arrays of kinds 33 and 39 | `+20`<sub>h</sub> |
| music, `MusicAudioBank` | 116 | `music/magi_data/win/musicNNN.win.mab` | `00222740`, format `"%s%03d%s"` from `PS2Data/sound/music/magi_data/win/music` (`009088E0`) | `+00`<sub>h</sub> |
| block indexes | 248 | `se/block/se<n>.seb` | `002E60F0`, kind 32 | - |

The manager's fifth controller, at `+18`<sub>h</sub>, is `StreamAudioController`. The two SE folders' root is
`PS2Data/sound/se/sead_data_win` (`00908950`), and `.win.sab` comes from `00908998`. Music ids run 7, 15-92,
94-116 and 200-213.

### Block banks and the block index

An actor's sound-effect record names up to three SE blocks as `u16` ids, bit 15 meaning none. `002E60F0` turns each id
into an index into the kind-32 path array of 608 `.seb` paths at `01E7FCF0` (`002E6157`-`002E618E`). The array holds
`se000`, `se007`, `se001`-`se006`, then `se200`-`se499` from index 8 and `se700`-`se999` from index 308:

| Block id | Index |
|---|---|
| 0, 1, 2 | 0, 1, 3, which are `se000`, `se007` and `se002` |
| 3-499 | id - 192 |
| 500 and up | id - 392 |

So ids 200-499 and 700 and up name the file with the same number, and ids 192-199 name the first eight entries,
`se000`, `se007` and `se001`-`se006`. 247 of the 248 shipped `.seb` files are reached by
their own number, and `se007` by id 1. The index file is read into a block (`002E6277`) and registered by
`003A1650`.

### The block registry

`003A0C90(block)` keeps 64 records of `18`<sub>h</sub> bytes at `02AEEDC0`, sorted by block number at `+04`<sub>h</sub>:

1. A block already registered adds one to the use count at `+0E`<sub>h</sub>, and the new copy of the file is freed.
2. A new block takes a free record, marks it in the bitmap at `02AEF3F0`, and is passed to `002DEF00(slot & 3Fh,
   file)`, which builds a `SebAudioBank` through `001DBD20`, `00210B60` and `0021B430` (`003A1650`).
3. `00223AD0` reads the index, stores the registry slot at bank `+3C`<sub>h</sub> and the block number at `+38`<sub>h</sub>, and opens the
   block's `.win.sab` (`00223CB1`-`00223D05`).

`002DEC10` reads an index's block number, the `i16` at `+08`<sub>h</sub>, for `003A1650`. A record's handle is its generation
`+0A`<sub>h</sub> over its index `+08`<sub>h</sub>, and every user compares the whole handle before it trusts a record:

- `003A0F80(handle)` counts a use down. At 0, unless the record is permanent (`+0D`<sub>h</sub>), it frees the slot's bank
  (`002DEEF0`, which hands `0021B430` no file), adds one to the generation, unlinks the record (`003A1750`) and puts
  it at the head of the free list `02AEF3D8`.
- `003A1750` takes a record out of its list through the links `+00`<sub>h</sub> (next) and `+02`<sub>h</sub> (previous) and sets both to
  `FFFF`<sub>h</sub>.
- `003A0EA0`, run by `0036D890`, walks the records marked in the bitmap `02AEF3F0`. A record whose `+10`<sub>h</sub> is set
  and for which `002DEE90` answers 0 gets state 2 at `+0C`<sub>h</sub>, `+10`<sub>h</sub> = 0 and its bitmap bit (by `+08`<sub>h</sub>)
  cleared, and its file handle `+14`<sub>h</sub> is released (`0036D200`) and freed (`00369800`).
- `003A1290(handle)` answers the record's byte `+0C`<sub>h</sub> for `002E60F0`.

`003A13F0` loads three blocks once at start-up: blocks 0, 1 and 2, which `002ED8C0` maps to `se000`, `se007` and
`se002`. Their callbacks `003A1390`, `003A1330` and `003A12D0` register each one (`003A1650`), keep its handle at
`02AEF3FC`, `02AEF400` or `02AEF404`, and mark the record permanent.

### Sound ids

A sound id is `registry slot << 9 + sound slot`. `003A1180(slot)` builds it from the current block handle at
`02AEF3FC`. It answers -1 when `00267330(0)` is non-zero (`003A1180`-`003A118F`), or when that handle is -1 or its
record does not match (`003A11AB`-`003A11D1`).

`003A11F0(slot)` builds the same id without the `00267330` test, for `00249CA0`. `003A1100` and `003A1070` build ids
from the blocks at `02AEF400` and `02AEF404`; both answer -1 while `02AEF400` is -1, so `003A1070` gives nothing until
block 1 is loaded even when block 2 is.

`0021B5B0(id)` finds the bank whose `+3C`<sub>h</sub> equals `id / 512` (`0021B5DF`-`0021B5FA`). An index file has 128 slots,
so slots 128-511 of each id range name nothing.

### Six-digit banks

Effect and sound files carry `SeSep` records that name six-digit banks; 4,318 files hold them (2,304 `.snd`, 1,461
`.efx`, 545 `.mpk`, 7 `.cm`, 1 `.spp`). `002DF070` walks the records while each starts with `SeSep` and fits, and
calls `001DBE60(id, record + 10h)` for each. `0021A040` skips an id already loaded, and `00222DC0` stores the id and
`id / 1000` and copies the record's `u32` and `u8` twice into the bank (`+40`<sub>h</sub>/`+44`<sub>h</sub>, `+45`<sub>h</sub>/`+49`<sub>h</sub>).

The sound records of effect files open their banks through the table of 32 entries of `84`<sub>h</sub> bytes at `02EBBA00`.
The effect loader `00504060` adds an entry for a kind-1 record and opens its banks, or adds a reference to it
(`003D7CE0`); an entry holds the kind, a reference count `+02`<sub>h</sub>, the bank id `+04`<sub>h</sub> and up to 30 play handles:

- `003D7C50(kind, id, handle)` keeps a handle in the entry's first empty cell.
- `003D7E90(entry)` counts the handles that still play (`002DEE80`) and clears the rest.
- `003D7DC0`, run from `00258D70` and `00258E40`, empties every kind-1 entry with no reference and no playing
  handle and releases its bank (`002DF050`); it leaves kind-3 entries alone.

### Battle voices

`0036ED50` loads both languages of one voice bank. The index is the record's `i16` at `+14`<sub>h</sub>.

- The kind-33 array at `01E127D0` holds the 64 `us` paths and ends there: the cell at `01E129D0` is 0.
- The kind-39 array at `01ECB7E0` starts with the 64 `jp` paths and goes on to other files: the cell at `01ECBBE0` is
  a live pointer.
- Each finished load finds its record by the handle, in `022D9AB0` when `handle & F0h` is 0 and otherwise in
  `022D9AE0`, at `handle & Fh` times `18`<sub>h</sub>. It registers the bank through `001DC130` with 1 for `us` (`0036EAB0`)
  and 0 for `jp` (`0036E9F0`).

`0036F000` answers 1 only when no record of either table is in state 1 or 2, so every voice load has finished.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | "sabf" in a .sab, "mabf" in a .mab |
| `04`<sub>h</sub> | `u8` | version | 2; below 2 the directory is at +dirDelta |
| `05`<sub>h</sub> | `u8` | flag | 1 in a six-digit bank and in every .mab, 0 in the others |
| `06`<sub>h</sub> | `u16` | dirDelta | `10`<sub>h</sub> |
| `08`<sub>h</sub> | `u8` | chunkCount | 4 in a .sab, 3 in a .mab |
| `09`<sub>h</sub> | `u8` | nameLength | length of the bank name at `+10`<sub>h</sub> |
| `0A`<sub>h</sub> | `u16` | param | 1 makes the voice mixer drop the front-back pan |
| `0C`<sub>h</sub> | `u32` | fileSize | the file's length |

The bank name follows at `+10`<sub>h</sub>, `nameLength` bytes and a zero. The chunk directory starts at
`((10h + nameLength) & F0h) + dirDelta`, which is `20`<sub>h</sub> in every shipped file.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | tag | "snd " "seq " "trk " "mtrl" in a .sab; "musc" "inst" "mtrl" in a .mab |
| `04`<sub>h</sub> | `u32` | flags | `00100000`<sub>h</sub> |
| `08`<sub>h</sub> | `u32` | offset | from the start of the file |
| `0C`<sub>h</sub> | `u32` | pad | 0 |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[8]` | magic | "SeBlock " |
| `08`<sub>h</sub> | `i16` | block | the number in the file name |
| `0A`<sub>h</sub> | `i16` | slotCount | 128 |
| `0C`<sub>h</sub> | `u32` | fileSize | the file's length |
| `10`<sub>h</sub> | `i32[128]` | slotOffset from `+210`<sub>h</sub>; -1 for an empty slot |  |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | word | copied twice into the slot's node, read by no bank method |
| `04`<sub>h</sub> | `u8` | flags | the slot's start flags, read when the sound starts (`00224570`) |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[5]` | magic | "SeSep" |
| `08`<sub>h</sub> | `i32` | id | the six-digit bank id |
| `0C`<sub>h</sub> | `u32` | size | record length in bit 0-30 |
| `10`<sub>h</sub> | `u32` | word | copied to bank `+40`<sub>h</sub> and `+45`<sub>h</sub> |
| `14`<sub>h</sub> | `u8` | flags | copied to bank `+44`<sub>h</sub> and `+49`<sub>h</sub> |

## Shipped data

Every value below holds in all 4,609 `.sab`, 116 `.mab` and 248 `.seb` files:

| Field | `.sab` | `.mab` |
|---|---|---|
| magic, version, `dirDelta` | `sabf`, 2, `10`<sub>h</sub> | `mabf`, 2, `10`<sub>h</sub> |
| chunks | `snd `, `seq `, `trk `, `mtrl` | `musc`, `inst`, `mtrl` |
| name length | 5 for `se` banks, 7 for `shout` banks | 5 |
| `+05`<sub>h</sub> | 1 in the 4,097 six-digit banks, 0 in the 248 block banks and 264 voice banks | 1 |
| `+0A`<sub>h</sub> | 350 values; 1 in 157 banks, starting `se001001` | 10,000 |
| `fileSize` equals the length; chunk offsets rising, the first at the directory's end | yes | yes |

The `.seb` files are `se000`, `se002`, `se007`, `se200`-`se434` and `se700`-`se709`, 708 to 24,968 bytes, with
4,404 slots present. The slot flag byte takes the values 0 (2,647 slots), 128 (1,574), 1 (133), 4 (33), 5 (11), 17
(5) and 8 (1).

### Battle voice lines

Each language's 66 voice banks hold ten lines per character, named `ve` (English) or `vj` (Japanese), a character
code, a number and an event: 198 `at` (attack), 198 `dm` (damage), 130 `crt` (critical) plus 2 spelt `ctr`, and
132 `dead`. Nine `us` banks hold an eleventh line named `vefah_01` and a code, and `shout62` holds a `vjD032` line in
both languages.

### Files the PC build never opens

- 132 `.orb.sab` voice banks, 66 per language, each beside a `.win.sab` of the same name; the executable holds no
  `.orb` string.
- `shout64` and `shout65` in both languages: the kind-33 and kind-39 arrays name only `shout00`-`shout63`.

## Loader behaviour

1. `007CFF90` accepts a bank only when its first four bytes equal `sabf`, the constant at `00D115B4`, and refuses a
   null pointer (`007CFF93`-`007CFFA0`). `007D07A0` is the same test for `mabf` (`01CB6FB8`).
2. `007CF6B0` finds a chunk by tag: with version 2 or more it starts the directory after the name, rounded down to 16,
   plus `dirDelta` (`007CF6B7`-`007CF6D4`), and walks `chunkCount` records of 16 bytes (`007CF6DC`-`007CF704`). A tag
   that is not there gives a null chunk (`007CF710`).
3. A chunk's offset is added to the file's base (`007D05A9`). Nothing compares an offset or `chunkCount` with
   `fileSize`.
4. The voice path `007EDE90` reads `+0A`<sub>h</sub> (`007EE01D`) and, when it is 1, passes zero as the front-back pan
   (`007EE02B`-`007EE031`).
5. `00223AD0` checks the index's block number against the one asked for only through `_guard_check_icall`
   (`00223B53`-`00223B5F`), which does not branch.
6. It walks `slotCount` slots (`00223B72`), skips an offset of -1,
   and copies each slot's `u32` and `u8` into a 10-byte node at `+00`<sub>h</sub>/`+04`<sub>h</sub> and again at `+05`<sub>h</sub>/`+09`<sub>h</sub>. It reads
   nothing past the slot's fifth byte. The `SeBlock` string does not occur in the executable, so no code compares
   the magic.
7. The driver reads every record through small wrapper classes, named by their run-time types. A chunk wrapper skips
   the chunk's name padding (`(byte +09h + 10h) & F0h` from version 2) and indexes its offset table at `u16`
   `+02`<sub>h</sub>; the record accessors that check the index refuse one at or past the count `u16` `+04`<sub>h</sub>:

| Class | Accessor |
|---|---|
| `SoundChunk`, `Sound` | `007CFB30`, `007CFB00` |
| `SequenceChunk`, `Sequence` | `007CFA30`, `007CF9E0` |
| `TrackChunk`, `Track` | `007CFC70`, `007CFC20` |
| `MaterialChunk`, `Material` | `007CF8B0`, `007CF860`; `007CF940` reads a material's offset and `007CF960` the offset table's size rounded up to 16 |
| `SoundEffect`, `SoundEffectFlangerParam` | `007CF780`, `007CF810` |
| `ZeroOne`, `SoundZeroOneParam` | `007CFE60`, `007CFF40` (from sound version 12, `20`<sub>h</sub>-byte records at `u16` `+4C`<sub>h</sub>) |

`007CF540` and `007CF560` build the `AudioBinaryFile` and `SabFile` wrappers, `007CF580` drops one, `007CF740` gives
the address a version-dependent `u16` of a record points to (`+02`<sub>h</sub>, `+0E`<sub>h</sub>, `+16`<sub>h</sub> or `+06`<sub>h</sub> for versions 0, 1, 2
and later), `007CF980` a record's zero-one count (2 below version 3, byte `+08`<sub>h</sub> after) and `007CFD00` a zero-one
curve's value at a point: the input scaled into 0-1 by the curve's range, then a binary search over its 16-byte
points.

## Modding notes

- A block bank is found by its number: `se<n>/se<n>.win.sab`, where `n` is the index file's block number; a
  six-digit bank by `se<id/1000>/se<id>.win.sab`.
- A bank name of 16 characters or more moves the chunk directory unless `dirDelta` grows with it.
- An index with more than 128 slots walks past its offset table; sound slots 128 and up are not reachable by id.
- Block ids 3-191 give a negative index, 192-199 read the array's first eight entries, and 500-699 land on another
  block's file (500 reads `se300`).
- Editing an `.orb.sab` file changes nothing on PC.

## Related

- [Escape Mode](../Controls-And-Input/escape.md) - plays block slot `52`<sub>h</sub> and `2A`<sub>h</sub> through `003A1180`.
- [Sound engine configuration](sound-engine-config.md) - the configuration file beside the banks.
