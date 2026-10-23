---
title: "Sound banks: the bank files that hold every sound effect, battle voice and music track, how each is named and found, and how a sound id names a bank and a slot"
kind: "format"
category: "Sound and music"
addresses: "0x007CFF90, 0x007CF6B0, 0x00223AD0, 0x00222DC0, 0x00222740, 0x0036ED50, 0x002E60F0, 0x003A1650, 0x003A1180, 0x002105E0"
---

## What the player sees

- Every sword hit, menu blip, spell and footstep plays from a sound bank; the game ships no loose sound files.
- 64 characters call out in battle (66 banks ship per language; the path arrays name only `shout00`-`shout63`),
  each with ten lines: three for attacking, three for taking damage, two for a
  critical and two for being knocked out.
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

### Block banks and the block index

An actor's sound-effect record names up to three SE blocks as `u16` ids, bit 15 meaning none. `0x002E60F0` turns each id
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

### Sound ids

A sound id is `registry slot << 9 + sound slot`. `0x003A1180(slot)` builds it from the current block handle at
`0x02AEF3FC`. It answers -1 when `0x00267330(0)` is non-zero (`0x003A1180`-`0x003A118F`), or when that handle is -1 or its
record does not match (`0x003A11AB`-`0x003A11D1`).

`0x003A11F0(slot)` builds the same id without the `0x00267330` test, for `0x00249CA0`. `0x003A1100` and `0x003A1070` build ids
from the blocks at `0x02AEF400` and `0x02AEF404`; both answer -1 while `0x02AEF400` is -1, so `0x003A1070` gives nothing until
block 1 is loaded even when block 2 is.

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

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "sabf" in a .sab, "mabf" in a .mab |
| `+0x04` | `u8` | version | 2; below 2 the directory is at +dirDelta |
| `+0x05` | `u8` | flag | 1 in a six-digit bank and in every .mab, 0 in the others |
| `+0x06` | `u16` | dirDelta | `0x10` |
| `+0x08` | `u8` | chunkCount | 4 in a .sab, 3 in a .mab |
| `+0x09` | `u8` | nameLength | length of the bank name at `+0x10` |
| `+0x0A` | `u16` | param | 1 makes the voice mixer drop the front-back pan |
| `+0x0C` | `u32` | fileSize | the file's length |

The bank name follows at `+0x10`, `nameLength` bytes and a zero. The chunk directory starts at
`((0x10 + nameLength) & 0xF0) + dirDelta`, which is `0x20` in every shipped file.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | tag | "snd " "seq " "trk " "mtrl" in a .sab; "musc" "inst" "mtrl" in a .mab |
| `+0x04` | `u32` | flags | `0x00100000` |
| `+0x08` | `u32` | offset | from the start of the file |
| `+0x0C` | `u8[4]` | pad | 0; read by no function: `0x007CF6B0` and `0x007D0580` read the tag and the offset, and the five functions that call `0x007CF6B0` (`0x007D0210`, `0x007D0580`, `0x007E3450`, `0x007E3CF0`, `0x007E48D0`) read the offset `+0x08` of the entry it returns and not its `+0x0C`; nothing fixes its width |

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
| `+0x0C` | `u32` | size | record length in bit 0-30 |
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

## Modding notes

- A block bank is found by its number: `se<n>/se<n>.win.sab`, where `n` is the index file's block number; a
  six-digit bank by `se<id/1000>/se<id>.win.sab`.
- A bank name of 16 characters or more moves the chunk directory unless `dirDelta` grows with it.
- An index with more than 128 slots walks past its offset table; sound slots 128 and up are not reachable by id.
- Block ids 3-191 give a negative index, 192-199 read the array's first eight entries, and 500-699 land on another
  block's file (500 reads `se300`).
- Editing an `.orb.sab` file changes nothing on PC.

## Related

- [Escape Mode](../Controls-And-Input/escape.md) - plays block slot `0x52` and `0x2A` through `0x003A1180`.
- [Sound engine configuration](sound-engine-config.md) - the configuration file beside the banks.
