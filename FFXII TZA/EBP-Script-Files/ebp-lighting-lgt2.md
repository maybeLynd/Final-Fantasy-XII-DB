---
title: "LGT2 light sets: the 0x70-byte light records and chunk tables of an event script's lighting, how they are bound into a light group and how the renderer picks them"
kind: "format"
category: "EBP script files"
addresses: "0x0037AA90, 0x02EBF420, 0x01EF94E4, 0x01EF94E0, 0x00330110, 0x0032F1B0, 0x0037B230, 0x0037A9B0, 0x0037AD40, 0x0037A5B0, 0x0037A450, 0x003ACC10, 0x003DEA00, 0x003DEA10, 0x0037B030, 0x0037B0F0, 0x0037B190, 0x003DE9A0, 0x0037A880, 0x0037A7F0, 0x003E8A40"
---

## What the player sees

The lamps, fires and coloured fill lights of a cutscene, and the lights a scene switches on and off
as it plays. Each record is one light that tints the characters and objects near it; the chunk
tables decide which records are lit at a given moment. Field maps carry the same format in their
map pack ([map pack](../World-Areas-And-Travel/mpk-map-pack.md), slot 17), bound into group 0.

## Where it comes from

Slot 14 of the [EBP script container](ebp-script-container.md) directory, present only in event
scripts. The walker `0x003304A0` passes it to `0x00330110` only for actor managers 1 to 4 (`0x0033066B`
skips manager 0). `0x00330110` stores the pointer at `0x022C6E20 + manager × 8` (`0x00330140`) and clears
pending bit `0x10000`; when the manager's pending word empties, the finaliser `0x0032F1B0` binds it with
`0x0037AA90(section, manager)` (`0x0032F1F9`). The manager index is the light group.

## Layouts

All multi-byte fields are little-endian.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "LGT2", compared as the dword `0x3254474C` |
| `+0x04` | `u16` | listOffset | start of the chunk chain, from the section start |
| `+0x06` | `u16` |  | value 0 |
| `+0x08` | `u16` |  | 1 or 2, not read |
| `+0x0A` | `u16` | lightCount | light records |
| `+0x0C` | `u32` |  | value 0 |
| `+0x10` | `record[lightCount]` |  | `0x70` bytes each |

```
[listOffset] chunk chain, each chunk {u16 size; u16 type; ...}; size 0 ends the chain
```

Light record, as its readers use it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x02` | `u8` | kind | 1 interpolate, 2 curves, other values static |
| `+0x03` | `u8` | state | bit `0x1` off, bit `0x2` animated, bit `0x4` loop the clock |
| `+0x04` | `i16[4]` |  | kind 1: three start values; kind 2: four curve indices into the type-5 table |
| `+0x18` | `...` |  | kind 1: s16[3], the three end values; kind 2: f32, the duration |
| `+0x1C` | `f32` |  | kind 2: the clock |
| `+0x20` | `request` |  | the `0x50` bytes handed to the renderer |
| `+0x20` | `u8` | lightKind | 6 is folded into the object's colour; any other kind is passed on in the light list |
| `+0x21` | `u8` | priority | 0 to 5 remapped at bind; the highest kind-6 light becomes the object's key light |
| `+0x22` | `u8` |  | 5 on a kind-6 light makes `+0x30`..+`0x38` multipliers |
| `+0x23` | `u8` | filter | 1 with `+0x24` = 2: `+0x28` must equal the object's id; 3: `+0x28` is a mask (`+0x24` 7 include, 6 exclude) |
| `+0x24` | `u8` | test |  |
| `+0x25` | `u8` |  | bit `0x10` exempts the light from the object's blend |
| `+0x27` | `u8` | flags | bit `0x1` not added to the summed colour; mask `0xFC` an exclusion mask (bit `0x20` set on group 0) |
| `+0x28` | `u32` | id | the value the filter tests |
| `+0x30` | `f32[4]` |  | values written by kind 1 and kind 2 animation |

Chunks, by type:

```python
type 0  +0x08 u16 first, +0x0A u16 count          a contiguous range of records
type 1  bound to group +0x10                       no shipped file carries one
type 2  +0x04 u32 n, entries at +0x10, 8 bytes:    cut list
          +0x00 u16 cutId, +0x02 u8 status, +0x04 u16 first, +0x06 u16 count
type 3  +0x04 s32 n, +0x08 u16 record[n]           light index table
type 4  skipped
type 5  +0x04 s32 n, +0x08 u32 slot[n], then n sub-entries each led by its s32 size   curve table
type 6  +0x04 s32 n, +0x08 {u16 type3Index; u16 id}[n]   id lookup into the type-3 table
type 7  +0x04 + selector × 8: u16[4] record indices   selector-driven set; 0xFFFF in the first is skipped, in the others it ends the set
```

A type-5 sub-entry is a curve with the ease-curve layout of the camera tables and SHK1 (`+0x00` length
`0x18 + 0x24 * keys`, `+0x04` keys, start and end time and value, then the keys): the animation hands each one to
the same evaluator, `0x003CC5F0` ([EBP camera tables](ebp-camera-tables.md) has the layout in full).

A light group is `0x50` bytes; the five groups sit at `0x02EBF420 + 0x50 x g`. The bind `0x0037AA90` stores each chunk by
its type through the jump table `0x0037AC7C`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8*` | section | the bound LGT2 section |
| `+0x08` | `u8*` | range | type 0 chunk (`0x0037AB2A`) |
| `+0x10` | `u8*` | bound | type 1 chunk (`0x0037AB33`) |
| `+0x18` | `u8*` | cuts | type 2 chunk (`0x0037AB43`) |
| `+0x20` | `u8*` | index | type 3 chunk (`0x0037AB8B`) |
| `+0x28` | `u8*` | ids | type 6 chunk (`0x0037AB91`) |
| `+0x30` | `u8*` | sets | type 7 chunk (`0x0037ABE0`) |
| `+0x38` | `u32*` | curves | type 5 slot table, the chunk + 8 (`0x0037AB9E`) |
| `+0x40` | `f32[3]` | colour | 1.0 after a reset |
| `+0x4C` | `u8` | ready |  |

| Group | `+0x00` | `+0x10` | `+0x20` | `+0x30` | `+0x40` | `+0x44` | `+0x48` | `+0x4C` |
|---|---|---|---|---|---|---|---|---|
| 0 | `0x02EBF420` | `0x02EBF430` | `0x02EBF440` | `0x02EBF450` | `0x02EBF460` | `0x02EBF464` | `0x02EBF468` | `0x02EBF46C` |
| 1 | `0x02EBF470` | `0x02EBF480` | `0x02EBF490` | `0x02EBF4A0` | `0x02EBF4B0` | `0x02EBF4B4` | `0x02EBF4B8` | `0x02EBF4BC` |
| 2 | `0x02EBF4C0` | `0x02EBF4D0` | `0x02EBF4E0` | `0x02EBF4F0` | `0x02EBF500` | `0x02EBF504` | `0x02EBF508` | `0x02EBF50C` |
| 3 | `0x02EBF510` | `0x02EBF520` | `0x02EBF530` | `0x02EBF540` | `0x02EBF550` | `0x02EBF554` | `0x02EBF558` | `0x02EBF55C` |
| 4 | `0x02EBF560` | `0x02EBF570` | `0x02EBF580` | `0x02EBF590` | `0x02EBF5A0` | `0x02EBF5A4` | `0x02EBF5A8` | `0x02EBF5AC` |

`0x00379F70`, from the boot `0x00266D10` and from `0x00379D00`, resets all five groups: 16-byte zero stores over `+0x00`
to `+0x3F`, 1.0 into the three colour floats and 0 into `+0x4C` (group 0: `0x00379FA8`, `0x00379FC8`, `0x00379FDA`,
`0x00379FE9`, `0x00379F90`, `0x00379F84`, `0x00379F77`, `0x00379FA1`). `0x0037B230` resets one group the same way.

`0x00379F70` also rebuilds the default request `0x02ADD8E0`. It zeroes its `0x50` bytes (`0x0037A0EA`) and stores the
dword `0x01050006` at `+0x00`, kind 6 with `+0x02` 5 and the filter byte 1 (`0x0037A101`), the test byte `0x02ADD8E4` = 1
(`0x0037A10D`), the flags `0x02ADD8E7` = `0x20`, the exclusion bit that group 0's records get (`0x0037A0EF`, `0x0037A114`),
and four 1.0 at `+0x10` (`0x0037A11A`).

## Shipped data

Measured over all 10,036 EBP2 containers in the nine language trees.

| Fact | Value |
|---|---|
| containers with section 14 | 1,260, 140 per language, all event scripts; each also carries sections 8 and 9 |
| languages | the 140 light sets are byte-identical in all nine trees |
| section length | 64 to 34,304 bytes, median 3,680 |
| `listOffset` | `0x10 + 0x70 × lightCount` in every file |
| header | `+0x06` and `+0x0C` 0 in all; `+0x08` 1 (1,251) or 2 (9) |
| `lightCount` | 0 to 287, median 30; 51,723 records |
| chunks per file | 4 (1,233), 5 (18), 3 (9); every chain ends inside the section |
| chunk types | 3, 5 and 6 in all 1,260; 2 in 1,251; 0 in 18; never 1, 4 or 7 |
| type 5 | `n` = 0 in every file |
| type 2 | size `0x10 + 8n` in all; record ranges in bounds; status byte 0 (14,742) or 1 (135); 135 lists contain cut 0 |
| type 3 and 6 | every index in bounds; equal counts in 1,089 files |
| record `kind` | 0 in all 51,723; `state` 2 (51,606) or 6 (117) |
| request `lightKind` | 1 (38,754), 6 (8,271), 2 (4,626), 4 (72) |
| request `priority` | 0 (51,624), 1 (90), 255 (9) |
| request `filter` / `test` | 1/1 (43,803), 3/7 (4,905), 3/6 (3,015) |
| request `flags` | 0 (51,327), 1 (396) |

The rows, once per light set (the nine trees carry the same bytes):

- [`ebp-lighting-lgt2-sets.tsv`](ebp-lighting-lgt2-sets.tsv) has the 140 sets: the script path under each language's
  `plan_master`, the languages, the section's SHA-256 and length, `listOffset`, `+0x08`, `lightCount`, and the chunk
  count and types in chain order.
- [`ebp-lighting-lgt2-lights.tsv`](ebp-lighting-lgt2-lights.tsv) has the 5,747 light records with their fields by the
  layout above and their 0x70 bytes. The record's `s16` words at `+0x04` and `+0x0C` and its floats at `+0x18` and
  `+0x1C` are given as stored, whichever kind reads them.
- [`ebp-lighting-lgt2-chunks.tsv`](ebp-lighting-lgt2-chunks.tsv) has the 561 chunks, each with its offset, size, type,
  `n` and entries:
  - type 0: `first` and `count`;
  - type 2: `cutId:status:first+count`;
  - type 3: the record indices;
  - type 6: `type3Index:id`.

Map packs carry the same section as their slot 17 ([map_ctrl pack](../World-Areas-And-Travel/mpk-map-pack.md)): 212 light
sets with `+0x08` 0 in all, chunk type 7 in 20 of them, and their own rows beside that page.

Each of the 20 type-7 chunks is 28 bytes, three sets for the selectors 0 to 2. The sets are listed only when the section
has no type-0 range (Which records are lit, below), and 16 of the 20 have one, so only the map light sets of `gil0102`,
`mfr0105`, `mnt0109` and `wdl0107` change their lights with the weather.
[`mpk-map-pack-lgt2-lit-by-slot.tsv`](../World-Areas-And-Travel/mpk-map-pack-lgt2-lit-by-slot.tsv) gives the records group 0
lists on entry for each map and weather slot.

### Columns of the light set tables

Offsets are from the start of the LGT2 section and written in hexadecimal.

| Column | Holds |
|---|---|
| `sha256` | in ebp-lighting-lgt2-sets.tsv, the SHA-256 of the section's bytes, 64 hexadecimal digits; `gil_d0102` and `rbl_f0101` carry the same section, so 139 values occur on the 140 rows |
| `section_bytes` | the section's length in bytes, 64 to 34,304 |
| `list_offset` | the header's `listOffset` (`+0x04`), where the chunk chain starts; `0x10 + 0x70 × light_count` on every row |
| `light_count` | the header's `lightCount` (`+0x0A`), 0 to 287; the 140 values add up to the 5,747 rows of the lights table |
| `record_offset` | in ebp-lighting-lgt2-lights.tsv, where the record starts: `0x10 + 0x70 × record` |
| `light_kind` | the request's `lightKind`, the byte at record `+0x20`: 1 (4,306 rows), 6 (919), 2 (514) or 4 (8) |
| `f34` | the second of the four floats at record `+0x30`, the one at `+0x34`, as stored: -1.2468749284744263 to 8.4375 |
| `record_hex` | the record's `0x70` bytes in file order, 224 hexadecimal digits |
| `chunk_offset` | in ebp-lighting-lgt2-chunks.tsv, where the chunk starts: chunk 0 at the set's `list_offset`, each next chunk at the previous one's offset plus its `size` |

## Loader behaviour

### The bind

`0x0037AA90(section, group)`:

1. returns at once for a group above 4 (`0x0037AA9E`), and for a negative one too, as the compare is unsigned
   (`0x0037AAA2`); the section's magic is read with no null test (`0x0037AABF`);
2. on a magic mismatch jumps straight to setting the group's ready byte `+0x4C` (`0x0037AAC5` →
   `0x0037AC69`);
3. otherwise resets the group with `0x0037B230` (pointers `+0x00` to `+0x38` zeroed, `+0x40` to `+0x48`
   set to 1.0, `+0x4C` cleared), stores the section at `+0x00`, and walks the chain from `+0x04` (a `u16`,
   `0x0037AAE7`) through the jump table at `0x0037AC7C`: type 0 to `+0x08`, 1 to `+0x10`, 2 to `+0x18`,
   3 to `+0x20`, 6 to `+0x28`, 7 to `+0x30`, type 5's `+0x08` to `+0x38`; type 4 and types above 7 are
   skipped by their size;
4. for type 2, when `0x01EF94E0` is non-zero, clears every entry's status (`0x0037AB4D`-`0x0037AB76`) and turns on the
   first entry whose cut id is 0 (`0x0037A9B0(group, 0)`, which stops at the first match, `0x0037A9E6`);
5. for type 5, replaces each `slot[i]` with the encoded address of sub-entry `i` (`0x0020E620`);
6. replaces each record's `+0x21` below 6 with `0x01EF94E4[value]` (`0x0037AC20`): the table holds
   `0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0`; values of 6 and above stay;
7. on group 0 only, ORs `0x20` into each record's `+0x27` (`0x0037AC50`);
8. sets `+0x4C` to 1.

`0x01EF94E0` is 1 in the image and is set only by `0x0037AA80`, the debug verb `debug_lightdatamustinit`
(`0x0050D340`). Every pointer refers into the loaded file, and steps 4 to 7 rewrite that file in memory.

On the container route the finaliser, for a manager above 0 (`0x0032F1BB`), resets the group (`0x0032F1D4`) and
clears its ready byte (`0x003DE920(group, 0)` → `0x0037ACA0`, which also clears bit `1 << group` of `0x02B59350`,
`0x003DE953`) before the bind, sets it again after (`0x003DE920(group, 1)` →
`0x0037ACD0`, which sets `+0x4C` only when `+0x00` is non-null, and sets bit `1 << group` of `0x02B59350`, `0x003DE938`),
and stores the first cut id plus 1 at manager record `+0x1FC` (`0x0037B290`).

That id is word `+0x10` of the cuts chunk `+0x18`; when that pointer is null or the chunk's `+0x04` is 0,
`0x0037B290` returns -1 and 0 is stored (`0x0037B2A9`, `0x0037B2AF`). A section with a bad magic therefore leaves a ready
group with no chunks, which lights nothing.

When the manager's slot `0x022C6E20` is null (`0x0032F1F2`), the finaliser stops after the reset and the cleared ready
byte: it binds nothing, leaves the group not ready and leaves `+0x1FC` as it was.

### Which records are lit

The collector `0x0037AD40` runs over the five groups and skips any whose `+0x4C` is 0. For each it
adds every record whose state bit `0x1` is clear, first running `0x0037A5B0` on it, and lists the
record's request (`record + 0x20`):

- the type-0 range, when present (`0x0037ADCB`); after it the collector goes straight to the cuts (`0x0037AE2E`);
- otherwise the type-7 set for the selector `0x02EBF408`: the `u16` at `+0x04 + selector × 8`, skipped when it is
  `0xFFFF` (`0x0037AE47`-`0x0037AE50`), then the next three, up to the first `0xFFFF` (`0x0037AEA0`-`0x0037AEF6`);
- then the range of every type-2 cut whose status is non-zero.

The selector is the weather slot minus 1. `0x00379860(slot)` jumps to `0x00379F50` when a map light set is loaded
(`0x02ADD090`), and `0x00379F50` stores `slot - 1` at `0x02EBF408` for slots 1 to 3 (`0x00379F5B`); the weather roll calls
`0x00379860` on every zone start ([Weather](../World-Areas-And-Travel/weather.md)). `0x00379F70` resets the selector to 0
(`0x0037A0C0`).

The list starts with a default request at `0x02ADD8E0`. Each frame the collector first copies group 0's
`+0x40`, `+0x44` and `+0x48` (1.0 after a reset, read at `0x02EBF460`, `0x02EBF464` and `0x02EBF468`) into that
request's `0x02ADD8F0`, `0x02ADD8F4` and `0x02ADD8F8` (`0x0037AD78`, `0x0037ADA1`, `0x0037AD99`). When a group
has a type-1 chunk (`+0x10`), the collector calls `0x00265020` for it each frame and discards the
results; no shipped file has one.

The collector writes every listed request into the array at `0x02EBF5C0` and applies the 128 cap only
at the end, so a frame that lists more than 128 records writes past slot 128 before the count
returned is cut to 128. With one cut on, a shipped light set lists at most 11 records.
`setlightallcutstatus` on would list 287 in `alc_z0104`, 259 in `gil_z0100` (256 cut records and a
type-0 range of 3) and 204 in `bhm_c0102`.

The object light pass
`0x003ACC10` reaches the collector when it meets a kind-7 request. For each listed request it skips the
light when `(0x02B3F520 | 0x02B3F501) & (+0x27 >> 2)` is non-zero, applies the `+0x23`/`+0x24` filter,
folds kind-6 lights into the object's colour (choosing the key light by `+0x21`, then by strength)
and passes every other kind on.

### Animation

`0x0037A5B0` acts on records with state bit `0x2`: kind 1 interpolates the three start and end values
by the current fraction (`0x00466BF0`) into `+0x30` to `+0x38`, scaled by 1/128; kind 2 evaluates the
four type-5 curves (`0x003CC5F0`) and clamps each result to -1..1 into `+0x30` to `+0x3C`. Each frame
`0x0037A450` advances a kind-2 clock `+0x1C` by `0x01DFE0BC` and, past the duration `+0x18`, wraps it to
0 (state bit `0x4`) or holds it at the duration.

`0x0037A450` walks every record of the five groups whose section pointer `+0x00` is set (`0x02EBF420` to
`0x02EBF5B0` in steps of `0x50`, `0x0037A464`, `0x0037A4E3`) and skips a record with state bit `0x1` or without bit
`0x2` (`0x0037A488`, `0x0037A490`). Only the clock step tests the kind (`0x0037A492`); the duration test and the
wrap or hold run on every animated record (`0x0037A4AD`-`0x0037A4CA`).

### Script and map control

| Caller | Effect |
|---|---|
| `setlightcutstatus` (`0x00351210`), `setlightcutstatus_21c` (`0x00351D90`) | `0x003DEA00`: a cut's status on (`0x0037A9B0`) or off (`0x0037A910`) |
| `setlightallcutstatus` (`0x00351850`) | `0x003DEA10`: every cut on (`0x0037AA00`) or off (`0x0037A960`) |
| `setlightcutanimestatus` (`0x00352130`), `setlightcutanimestatus_21e` (`0x00352780`) | `0x003DE9A0(group, cut, status)`: state bit `0x2` set on every record of the cut's range (`0x0037A880`) or cleared (`0x0037A7F0`); the group is the caller's actor manager `+0x28` |
| `0x003E8440`, `0x003E8690`, `0x003E8A10`, `0x003E8A70`, `0x003E8C50` | by id through types 6 and 3: off and on (`0x0037B0F0`, `0x0037B190`), animation start and stop (`0x0037A1D0`, `0x0037A130`), loop on and off (`0x0037A3B0`, `0x0037A310`), clock reset (`0x0037A270`, `0x0037A500`), the still-running test (`0x0037B030`: 1 while an on kind 2 record's clock is below its duration, `0x0037B0BE`) |

Animation start and stop by id go through `0x003E8A40(id, start)`, which calls `0x0037A1D0(0, id)` when
`start` is non-zero and `0x0037A130(0, id)` otherwise; `0x003E8440`, `0x003E85B0`, `0x003E8690` and
`0x003E8C50` call it. Both look the id up in the type-6 table, map it through the type-3 table and set
or clear state bit `0x2` of that one record in group 0. An id missing from the type-6 table selects
entry 0 of the type-3 table.

The other by-id routines use the same lookup. `0x0037B0F0` sets state bit `0x1`, turning the light off
(`0x0037B171`), and `0x0037B190` clears it (`0x0037B211`); a type-3 index at or past the table's count changes
nothing (`0x0037B15C`, `0x0037B1FC`). `0x0037B030(group, id)` returns 1 only while the record is on, is of kind 2
and its clock `+0x1C` is below the duration `+0x18` (`0x0037B0A5`-`0x0037B0BE`), and 0 otherwise. For an id
without bit `0x4000`, `0x003E8440` resets the clock (`0x0037A270`) and starts the animation (`0x0037A1D0`) when
it returns 0 (`0x003E84D3`-`0x003E851B`).

`0x0037A880` and `0x0037A7F0` act on every type-2 entry that carries the cut id, not only the first: the walk
goes on after a match (`0x0037A8F1`, `0x0037A861`). Both return at once when the group has no cuts chunk
(`0x0037A8A0`, `0x0037A810`).

## Modding notes

- Keep `listOffset = 0x10 + 0x70 × lightCount` and end the chain with a zero size word; the loader
  trusts both and reads `listOffset` as 16 bits.
- A light is lit only through a type-0 range, a type-2 cut that is on, or a type-7 set; a record no
  chunk covers never reaches the renderer.
- Cut 0 is the one turned on at load. Other cuts start off unless a script turns them on.
- Priority values 0 to 5 become `0x20` to `0xC0`; write 6 or more to set the byte directly.
- Light sets in group 0 (the map pack's) get `+0x27` bit `0x20` added at bind; edit the other bits
  only.
- The bytes in memory differ from the file after binding (priorities, flags, cut status, curve slots).

## Related

- [EBP script container](ebp-script-container.md): the directory, the walker and the pending word.
- [Map pack](../World-Areas-And-Travel/mpk-map-pack.md): the field light set in slot 17, bound into group 0.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the manager record and its `+0x1FC` field.
- [Script verb table](../Scripts-And-Script-Commands/verb-table.md): the light verbs and their use counts.
- [Resource arenas and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md): the 32-bit address encoding the type-5 slots use.
