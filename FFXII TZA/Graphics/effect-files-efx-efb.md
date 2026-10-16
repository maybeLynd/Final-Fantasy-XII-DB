---
title: "Effect files (.efx, .efb): the effect containers, their chunk streams, the record kinds and the map effect bank"
kind: "format"
category: "Graphics"
addresses: "003EDAD0, 01EFF3B0, 003EE2D0, 003ED8A0, 003A79C0, 00333C80, 003A7E80, 004FF270, 003A9730, 003A9A70, 003A9EF0, 003AA470, 00500980, 0026FB90, 02F8F29D, 0026F470, 0026FAD0, 00377DC0, 003788F0, 00378230, 02ADD088, 002FC4A0, 003B38B0, 003B29B0, 003B0660, 003B2220, 02EBB738"
---

## What the player sees

Every spell, summon, Quickening, hit flash, event effect and map effect (falling leaves, weather
particles, glowing water) is built from the data in these files. An `.efx` file is one effect
stream; an `.efb` file is a map's effect bank, an effect stream plus a table saying which of its
effects to start. A file the loader refuses is skipped without a message: the effect never appears.

## Where it comes from

- `.efx`: 3,288 files under `ps2data/effect_finish/<locale>/`. The file kinds that name them (the
  common and menu banks, the magic and event effects) are on the
  [size-table page](../Game-Files-And-Data-Tables/file-size-tables-fst.md).
- `.efb`: 410 files under `ps2data/efb/`. The field loader asks for one per map through `00377DC0`
  ([map packs](../World-Areas-And-Travel/mpk-map-pack.md)); see "The map's effect bank" below.
- Streams embedded in other files: 144 `.cm` model files carry one in their `@FEF` section
  ([resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)), and
  387 `.mpk` map packs carry one each. The 531 paths are listed in
  `effect-files-efx-efb-efx-embedded-stream-files.txt`.

Every stream is parsed by `003EDAD0(stream, size)`. Six builders call it, each after making an
effect context from a `890`<sub>h</sub>-byte template whose byte `+0` is the context type (the context
itself is on the [resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)
page). Five pass the stream's own `+0C`<sub>h</sub> as the size; the EFB loader passes the blob size.

| Type | Builder | Call | Template flags `+2` |
|---:|---|---|---|
| 1 | `002FC4A0` | `002FC5D2` | 0 |
| 2 | `0026FB90` (the EFB loader) | `0026FCEE` | `0C`<sub>h</sub> |
| 3 | `003B38B0` (the `@FEF` ticket) | `003B39B3` | `0C`<sub>h</sub> |
| 4 | `003B29B0` | `003B2A75` | 0 |
| 5 | `003B0660` | `003B0745` | 0 |
| 7 | `003B2220` | `003B226D` | 0 |

## Layouts

```
EFX stream (offsets from the magic)
+0x00  char[8]  magic     "EFX0010", "EFX0009" or "EFX0008", NUL-terminated, compared as 8 bytes
+0x08  f32      1.0 in every shipped stream; unused by the loader
+0x0C  u32      stream size, header included; the chunk walk ends here
+0x10  chunks

chunk
+0x00  u32  length   header included; the walk adds it to the cursor
+0x04  u16  flag     0x100 selects the run paths; 0x101, 0x102 and 0x103 select other routes
+0x06  u16  type
+0x08  s32  bias     stored at 02EBB738 before each record handler runs
+0x0C       record header, read by the record handler
+0x10       record payload
```

| Type | Record header at `+0C`<sub>h</sub> | Payload at `+10`<sub>h</sub> | Handler |
|---|---|---|---|
| `600`<sub>h</sub>, `610`<sub>h</sub>, `620`<sub>h</sub> | `+0D`<sub>h</sub> u8 index (`600`<sub>h</sub>) | `600`<sub>h</sub>: an `A0`<sub>h</sub>-byte record | `003A79C0` (`600`<sub>h</sub>) |
| `700`<sub>h</sub> | `+0C`<sub>h</sub> u8 index, `+0E`<sub>h</sub> u8 subtype | a fixed record of `160`<sub>h</sub>, `200`<sub>h</sub>, `280`<sub>h</sub> or `300`<sub>h</sub> bytes by subtype, then variable data | `003A7E80` |
| `800`<sub>h</sub> | `+0C`<sub>h</sub> u16 id, `+0E`<sub>h</sub> u8 subtype (0 to 8) | an emitter record; id and subtype copied to `+280`<sub>h</sub> / `+282`<sub>h</sub> | `003A9730` |
| `A00`<sub>h</sub> | `+0C`<sub>h</sub> u16 id, `+0E`<sub>h</sub> u8 element type | an element definition; id and type copied to `+42`<sub>h</sub> / `+44`<sub>h</sub> | `003A9A70` |
| `B00`<sub>h</sub> | `+0C`<sub>h</sub> u16 key, `+0E`<sub>h</sub> u8 kind (`50`<sub>h</sub>–`59`<sub>h</sub>), `+0F`<sub>h</sub> u8 slot | the record of that kind | `003A9EF0` |

```
0x600 record (payload, 0xA0 bytes, after 00333C80)
+0x00  u8      index, written by the handler from the header byte
+0x0A  u8[11]  eleven bytes
+0x16  u8      high nibble: index of the last non-zero byte of the eleven (0 when none), recomputed at load
+0x2C  u32[29] slots, reset to the encoded null at load

EFB file
+0x00  char[8]  magic     "EFB0001" or "EFB0002"
+0x08  u16      blob count
+0x0A  u16      row count
+0x0C  u32      0 in every shipped file
+0x10  blobs    { u32 size; 12 bytes; EFX stream[size] } x blob count
then   rows     row count rows

EFB row (type 3, 0xA0 bytes)
+0x00  u8   row type: 3 instantiates; 1 is a 0x60-byte row that is stepped over
+0x01  u8   must be 1, or the walk stops
+0x04  u8   channel
+0x05  u8   definition id; in an EFB0002 bank the lookup uses 0 and the instance's +0x373 gets this + 1
+0x07+s u8  enable byte for weather slot s (1 to 3)
```

The `B00`<sub>h</sub> kinds, each built by the record store as `alloc(size)`, then `ctor`, then `loader`:

| Kind | Object | Ctor | Loader |
|---:|---:|---|---|
| `50`<sub>h</sub> | `48`<sub>h</sub> | `005019D0` | `00502CB0` |
| `51`<sub>h</sub> | `1C`<sub>h</sub> | `00503790` | `00503880` |
| `52`<sub>h</sub> | `1D0`<sub>h</sub> | `00500B70` | `00500C00` |
| `53`<sub>h</sub> | `C0`<sub>h</sub> | `005014B0` | `00501520` |
| `54`<sub>h</sub> | `190`<sub>h</sub> | `004354E0` | `00436D00` |
| `55`<sub>h</sub> | `20`<sub>h</sub> | `00503C50` | `00503CD0` |
| `56`<sub>h</sub> | `20`<sub>h</sub> | `00503D50` | `00503E30` |
| `57`<sub>h</sub> | `30`<sub>h</sub> | `00503F50` | `00504060` |
| `58`<sub>h</sub> | `20`<sub>h</sub> | `00504170` | `00504230` |
| `59`<sub>h</sub> | `30`<sub>h</sub> | `005042C0` | `00504350` |

The kind-`54`<sub>h</sub> mesh record's layout is on [effect element types](effect-element-types.md). The
case-by-case load and destroy arms are in `effect-element-runtime-switch-family-record-store-5x.tsv`.

## Shipped data

| Fact | Value |
|---|---|
| `.efx` files | 3,288, 4,579,689,088 bytes, 1,840 to 25,310,800 bytes each, all under `ps2data/effect_finish` |
| `.efb` files | 410, 226,292,720 bytes, 7,584 to 4,444,528 bytes each, all under `ps2data/efb` |
| embedded streams | 144 `.cm` and 387 `.mpk` files, one stream each |
| streams | 4,229; every chunk walk ends exactly at `+0C`<sub>h</sub>; `+08`<sub>h</sub> is 1.0 in all |
| `.efx` magics | `EFX0010` 3,284, `EFX0008` 4 (`l0000.efx` in four locales) |
| stream magics | `EFX0010` 4,221, `EFX0008` 7, `EFX0009` 1 |
| `.efb` | all `EFB0002`; one blob each, its size equal to the stream's `+0C`<sub>h</sub>, its 12 header bytes zero; `+0C`<sub>h</sub> zero |
| `.efb` rows | 2,615, all type 3 with byte `+1` = 1; channels 0 to 63; row count equal to the header word in all 410 |
| chunks | 242,875, all flag `100`<sub>h</sub> |
| chunk types | `620`<sub>h</sub> 62,605; `800`<sub>h</sub> 53,351; `A00`<sub>h</sub> 48,868; `B00`<sub>h</sub> 40,750; `610`<sub>h</sub> 14,937; `700`<sub>h</sub> 13,928; `600`<sub>h</sub> 8,436 |
| `600`<sub>h</sub> | bias `A0`<sub>h</sub> in all |
| `700`<sub>h</sub> subtypes | 0: 13,224; 1: 520; 2: 120; 3: 64; the bias equals the subtype's fixed size in all |
| `800`<sub>h</sub> subtypes | 0: 2,153; 1: 41,058; 2: 1,237; 3: 2,502; 4: 620; 5: 2,810; 6: 26; 7: 2,203; 8: 742 |
| `A00`<sub>h</sub> | 55 distinct element types; payload byte `+0` is 0 in all |
| `B00`<sub>h</sub> kinds | `52`<sub>h</sub> 16,862; `56`<sub>h</sub> 6,746; `50`<sub>h</sub> 5,810; `51`<sub>h</sub> 5,352; `54`<sub>h</sub> 2,733; `57`<sub>h</sub> 1,843; `58`<sub>h</sub> 746; `53`<sub>h</sub> 374; `59`<sub>h</sub> 284; `55`<sub>h</sub> none |
| `B00`<sub>h</sub> keys | key 0 in all; slot byte never 0; no key repeats within a stream |

## Loader behaviour

### The version ladder

`003EDAD0` returns at once for a size of 0 (`003EDAD2`). It compares the first eight bytes with
`EFX0010`, `EFX0009` and `EFX0008` (`003EDAE4`, `003EDB13`, `003EDB43`) and sets the version
global `01EFF3B0` to 10, 9 or 8. No match jumps to `003EE24D`, which stores 10 and returns without
reading a chunk. The successful path ends at the same store, so `01EFF3B0` is 10 whenever the
loader is not running; only the `600`<sub>h</sub> record handler reads it, during the parse.

### The chunk walk

The walk runs from `+10`<sub>h</sub> to `stream + size` (`003EDB7B`, `003EE221`). At entry the loader clears
bit `1`<sub>h</sub> of the current context's byte `+3` and sets it again when the context type is 0, 2, 3, 4,
5, 6, 8 or 9 (mask `37D`<sub>h</sub>, `003EDBA2`–`003EDBB3`). A chunk takes a run path only when its flag
is `100`<sub>h</sub> and that bit is set (`003EDC0C`, `003EDC1D`). Anything else goes, one chunk at a time,
to `003EE2D0(chunk + 4, length − 4)`.

Each run path collects the consecutive chunks of its family, takes one block for them in arena 8
and copies them (`0036C1D0(8, 10)`, `0036A100`, `00861EBA`), then hands each record to its handler
with the chunk's bias in `02EBB738`. The copies truncate lengths to a multiple of 16.

| Family | Block at context | Handler per record |
|---|---|---|
| `600`<sub>h</sub>, `610`<sub>h</sub>, `620`<sub>h</sub> | `+888`<sub>h</sub> | `003A79C0`, `003A7B50`, `003A77F0` |
| `700`<sub>h</sub> | `+880`<sub>h</sub> | `003A7E80` |
| `800`<sub>h</sub> | `+870`<sub>h</sub>, or borrowed | `003A9730` |
| `A00`<sub>h</sub> | `+878`<sub>h</sub>, or borrowed | `003A9A70` |

For `800`<sub>h</sub> and `A00`<sub>h</sub> the loader tests the context's flag byte `+2` bit `4`<sub>h</sub> first (`003EE117`,
`003EE018`); when it is set it stores the input pointer instead of copying (`003EE171`, `003EE078`).
What borrowing implies for the source's lifetime is on the
[resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) page, and
the repair after a moved source is on the
[arena page](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).

### The `600`<sub>h</sub> family

The sizing pass gives a `600`<sub>h</sub> chunk an `B0`<sub>h</sub>-byte slot, a `610`<sub>h</sub> chunk `30h + 4n` bytes with
`n` the byte at chunk `+13`<sub>h</sub> (0 counts as `40`<sub>h</sub>), and a `620`<sub>h</sub> chunk its own length
(`003EDC8D`–`003EDCB1`). A `600`<sub>h</sub> copy is zero-filled to its slot (`003EDD62`–`003EDD79`). Only
the first run in a stream is parsed: the run flag starts at 1 (`003EDAE1`), a later chunk of the
family is stepped over while it is 0 (`003EDC4D`), and the first run clears it (`003EDED5`).

`003A79C0(header)` writes the index byte to the record's `+0`, resets the 29 slots at `+2C`<sub>h</sub> to
the encoded null, registers the record in the table at `[02EBEFA8]` (count at `+0`, entries from
`+8`) and calls `00333C80(record)`, which returns `record + A0h` (`003A79D4`–`003A7A21`).

`00333C80` rewrites an `EFX0009` or `EFX0008` record into the `EFX0010` layout when `01EFF3B0` is
9 or 8 (`00333CA1`, `00333DFE`). In every version it clears bit `2`<sub>h</sub> of `+16`<sub>h</sub> when that byte's
high nibble is `F`<sub>h</sub>, then sets the high nibble to the index of the last non-zero byte among the
eleven at `+0A`<sub>h</sub> (`00333F97`–`00333FD9`). The nibble in the file is therefore not the one used.

### The `700`<sub>h</sub> records

`003A7E80(header, length)` stores the index byte as a word at record `+C0`<sub>h</sub> and the subtype at
`+C2`<sub>h</sub>, registers the record in the table `[[02EBEFA0]]` at the index, and calls
`004FF270(record, low32(record) + bias)` (`003A7E8A`–`003A7EC3`). `004FF270` sends subtypes 0 to 3
to `00537C80`, `00537FA0`, `00538350` and `005387B0` and returns the record unchanged for any
other (`004FF270`–`004FF2A2`).

Each subtype body rebases a fixed list of stored offsets and returns `record + 160h`, `200`<sub>h</sub>,
`280`<sub>h</sub> or `300`<sub>h</sub> (`00537CA7`, `00537FE3`, `005383A1`, `0053880F`). A rebase decodes each dword
with `0020E600`, adds the delta and encodes it again with `0020E620` (`004304F0`, `00430AF0`).

### The `800`<sub>h</sub> and `A00`<sub>h</sub> records

`003A9730` copies the header's id and subtype to payload `+280`<sub>h</sub> / `+282`<sub>h</sub>, publishes the payload
at `[[02EBEF90]] + id × 8` and calls `00442460(payload, low32(payload) + bias)`, which dispatches
on the subtype (`003A973A`–`003A9773`, `00442460`). `003A9A70` copies the id and the element type to
`+42`<sub>h</sub> / `+44`<sub>h</sub>, publishes the payload at `[[02EBEF78]] + id × 8` and calls the setup dispatcher
`005004C0` (`003A9A7A`–`003A9AAD`).

Neither checks the id against the table size; the tables
themselves are on the [resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)
page, and what the records do is on [effect element runtime](effect-element-runtime.md).

### Single chunks and the flag routes

`003EE2D0` stores the chunk's bias in `02EBB738` and switches on the flag (`003EE2DA`–`003EE30B`):

- `100`<sub>h</sub>: clears `02096B40` and `02096BA4` and calls `003ED8A0`, which dispatches on the type.
  It sends `B00`<sub>h</sub> to the record store `003A9EF0` and `A00`<sub>h</sub> to `003A99F0` (`003EDA78`–`003EDAAD`),
  and has arms for types that no shipped stream carries.
- `101`<sub>h</sub> and `102`<sub>h</sub>: make a fixed instance current (`0024ED80`) and go to `003EE3B0` or
  `003EE260`. For a `B00`<sub>h</sub> chunk these write the key word 1 or 2 (`101`<sub>h</sub> also adds 1 to the slot
  byte) and call the second record store `003AA470` (`003EE3E1`–`003EE3EF`, `003EE291`–`003EE29C`).
- `103`<sub>h</sub>: only type `4000`<sub>h</sub> is passed on, to `0016D680`.
- Any other flag: the chunk is dropped.

Type-1 and type-7 contexts never set the run bit, so every chunk of their streams takes this
route.

### The single-chunk arms

`003ED8A0(chunk, length)` switches on the chunk's type word `+2` and hands the body at `+8` to one
arm.

A record arm takes an index (0 means the first free slot), frees whatever already holds that
slot, takes a block for the copy, and copies and rebases the body as the run paths do. The context
tables it fills are allocated with the context by `0024B3A0`: `003A7D00` (`400`<sub>h</sub> bytes, 128 `700`<sub>h</sub>
slots), `003A9560` (`A00`<sub>h</sub> bytes, 320 `800`<sub>h</sub> slots) and `003A9920` (`1800`<sub>h</sub> bytes, 768 `A00`<sub>h</sub>
slots), each zeroed; `003A76F0` empties the `600`<sub>h</sub> table `[02EBEFA8]` (256 pointers from `+8`) and its count.

| Type | Arm | What it does |
|---|---|---|
| `401`<sub>h</sub> | inline | the effect camera: the 64-byte matrix at `+8` goes to `02AEE9E0` through `0039D430`, which then calls `0039AFA0` and copies the workbench matrix to `02AEECB0` (`003970A0`); `003CC0F0` resets the camera record `02096D30` and copies the matrix to its `+60`<sub>h</sub>, the dwords `+48`<sub>h</sub>–`+54`<sub>h</sub> are stored at its `+00`<sub>h</sub>, `+04`<sub>h</sub>, `+08`<sub>h</sub> and `+10`<sub>h</sub>, and the record is submitted with priority `64`<sub>h</sub> (`003829D0`) while `02096887` is set |
| `500`<sub>h</sub> | `003A75B0` | frees every `600`<sub>h</sub> record of `[02EBEFA8]` and zeroes the table; when the context's byte `+3` bit 0 is set (the records sit in the run block) it frees only their 29 slot targets whose byte `+1` is 0, then the context's `+888`<sub>h</sub> block |
| `510`<sub>h</sub> | `003A7CB0` | frees all 128 `700`<sub>h</sub> records |
| `520`<sub>h</sub> | `003A9510` | frees the `800`<sub>h</sub> records |
| `530`<sub>h</sub> | `003A98D0` | frees the `A00`<sub>h</sub> definitions |
| `540`<sub>h</sub> | `003A9E00` | unlinks the record-store node whose key, kind and slot match the body and frees it (`00500850`) |
| `600`<sub>h</sub> | `003A7A50` | gets or creates the `600`<sub>h</sub> record for byte `+1` (`003A78A0`, which allocates `A0`<sub>h</sub> bytes and registers it with `00333BB0` / `00333AC0`), copies the `2C`<sub>h</sub>-byte header into it and calls `00333C80` |
| `601`<sub>h</sub> | `003A7950` | frees the `600`<sub>h</sub> record of byte `+1` |
| `610`<sub>h</sub> | `003A7AE0` | gets or creates the `600`<sub>h</sub> record of byte `+0`, finds its sub-entry byte `+1` (`00334000`) and copies a dword and the entry's own byte count of data into it |
| `611`<sub>h</sub> | `003A7AA0` | passes byte `+2` to `003340C0` for the `600`<sub>h</sub> record of byte `+1` |
| `620`<sub>h</sub> | `003A7730` | as `610`<sub>h</sub>, but takes a new block for the sub-entry (`0046F380`), copies the body from `+10`<sub>h</sub> and rebases it (`004FF320`) |
| `700`<sub>h</sub> | `003A7DC0` | the record through `003A7BE0` and `004FF270`; when it replaced a record, every `700`<sub>h</sub> object of the instance that pointed at the old one (`+E0`<sub>h</sub>) is pointed at the new one |
| `800`<sub>h</sub> | `003A96A0` | the record through `003A9790` and `00442460`; a replaced record is swapped in every emitter (`+100`<sub>h</sub>), every definition link (`+108`<sub>h</sub>) and every element link (`+18`<sub>h</sub>, `+20`<sub>h</sub>) of the current instance (`003A9590`) |
| `900`<sub>h</sub> | `003A92B0` | releases every emitter of the current instance (`003A9160`) |
| `A00`<sub>h</sub> | `003A99F0` | the definition through `003A9AD0` and `005004C0` |
| `B00`<sub>h</sub> | `003A9EF0` | the record store |
| `1000`<sub>h</sub> | `0016D680` | returns its argument and does nothing else |

The `600`<sub>h</sub> arm resets the 29 slots at `+2C`<sub>h</sub> only for a new record (`00333BB0`); an existing
record keeps its slots, where the run-path handler `003A79C0` resets them every time.

Outside the run block, the `500`<sub>h</sub> arm and the `601`<sub>h</sub> arm empty a record before freeing it through
`00333C00`, which releases each of the 29 slots (`0046F370`, `003697F0`) and stores the encoded
null `0020E620(0)` in it.

### The record store

`003A9EF0(header)` looks for a node whose word `+C`<sub>h</sub>, byte `+E`<sub>h</sub> and byte `+F`<sub>h</sub> equal the key,
kind and slot, walking the list at `[02EBEF70]` (the context's `+18`<sub>h</sub>) through `0020E600`
(`003A9EF6`–`003A9F3D`). A match is reloaded in place by `00500980(node, payload)`
(`003A9F42`). Otherwise the kind minus `50`<sub>h</sub>, bounded at 9, selects an arm of the table above
(`003A9F4D`–`003A9F76`).

`003AA470` is the same search with a six-arm table for kinds `50`<sub>h</sub> to `55`<sub>h</sub>
(`003AA47C`, `003AA4C2`, `003AA4DA`). It is reached only from the `101`<sub>h</sub> and `102`<sub>h</sub> routes,
which no shipped chunk takes.

Its arms build each kind with the same constructor as the first store but a loader of its own
(`003AA4FD`–`003AA5E1`), and a match is reloaded through `00500A60`, which dispatches on the kind
byte to the same loaders:

| Kind | Second loader | What it reads |
|---:|---|---|
| `50`<sub>h</sub> | `005032D0` | a row count, texture and palette counts, then `48`<sub>h</sub>-byte rows |
| `51`<sub>h</sub> | `00503BA0` | a `u16` count, then that many 16-byte entries, copied to a new block |
| `52`<sub>h</sub> | `005C5230` | nothing: it returns 0 |
| `53`<sub>h</sub> | `00501750` | a mode byte (`FF`<sub>h</sub> empty), a count and a slot byte, then 64-byte (mode 0) or 1,024-byte (mode 1) palettes |
| `54`<sub>h</sub> | `00436D00` | as the first store |
| `55`<sub>h</sub> | `00503CD0` | as the first store |

- `005032D0` numbers the texture and palette slots 1 to n and expands each `48`<sub>h</sub>-byte row into a
  `90`<sub>h</sub>-byte sprite row: the four corners of its rectangle, rotated by the row's angle in degrees,
  scaled and offset; the last row gets bit 1 of `+70`<sub>h</sub>.
- `00503180(record)` then resolves the kind-`50`<sub>h</sub> record's slot bytes into handles with
  `003AA280(key, 52h, slot)` and `003AA280(key, 53h, slot)`, and turns each row's pixel rectangle
  into texture coordinates by dividing by the texture's width `+A4`<sub>h</sub> and height `+A6`<sub>h</sub>.
- `00501750` ends by running `00503180` again over every kind-`50`<sub>h</sub> record of key 1 (`003AA1F0`,
  `003AA240`), so palettes loaded later still reach the sprites.

### The kind-`52`<sub>h</sub> texture loader

`00500C00(record, data)` reads a texture record. A first byte of `FF`<sub>h</sub> is an empty record. Otherwise
it keeps the byte's low six bits as the format `+A0`<sub>h</sub>, bit 6 as the word `+1C8`<sub>h</sub> and bit 7 as
`+1CA`<sub>h</sub>, the palette count from byte `+2` at `+A2`<sub>h</sub>, a reference size from words `+4` and `+6` at
`+1CC`<sub>h</sub> and `+1CE`<sub>h</sub>, and the width and height from words `+8` and `+0A`<sub>h</sub> at both `+A4`<sub>h</sub>/`+A6`<sub>h</sub> and
`+A8`<sub>h</sub>/`+AA`<sub>h</sub>. The palettes start at `+10`<sub>h</sub>.

Each palette gets two handles: format 0 has 16-colour palettes of `40`<sub>h</sub> bytes and format 1 256-colour
palettes of `400`<sub>h</sub> bytes (`001837A0` and `00183760`); a record with palettes in any other format
makes the loader return null. The palette data is copied to a new block at
`+B0`<sub>h</sub> (`0036A100`), or used in place when bit 3 of byte `+2` of `[02F97340]` is set.

The texture's allocated size is the width and height rounded up to a power of two (`0017FEA0`). With
`+1C8`<sub>h</sub> set it is instead scaled to the reference size: each side is `side / reference ×
pow2(reference)`, and an image whose size and reference size are both 1920 × 1080 keeps that size. The
format picks the builder, and its handle goes to `+C0`<sub>h</sub> with a code at `+B8`<sub>h</sub>:

| Format | Builder | Pixel bytes | `+B8`<sub>h</sub> |
|---:|---|---|---:|
| 0 | `00183EE0`, 4-bit indices | `w × h / 2` | `14`<sub>h</sub> |
| 1 | `00184140`, 8-bit indices | `w × h` | `13`<sub>h</sub> |
| 2 | `00183A00` | `w × h × 2` | 2 |
| 3 | `00183C60` | `w × h × 3` | 1 |
| 4 | `00183EB0`, 32-bit pixels (`0017E8E0`) | `w × h × 4` | 0 |
| `80`<sub>h</sub> | `00184130`, as format 0 | `w × h × 4` | `14`<sub>h</sub> |
| `81`<sub>h</sub> | `00184370`, as format 1 at twice the width and height | `w × h × 4` | `13`<sub>h</sub> |

Format bytes `80`<sub>h</sub> and `81`<sub>h</sub> cannot occur after the six-bit mask; any other format leaves the record
without a texture.

`00183A00` and `00183C60` create an `RGBA8` texture (format object `02CF7480`) of the allocated size,
or of the image size when the allocation is only one larger. They map it (`0017EBD0`), clear it when
the sizes differ, and write one byte per texel, the first of each four: `00183A00` the low four bits
of the first byte of each two-byte source pixel, `00183C60` the first byte of each three-byte pixel.
Then they commit it (`0062C360`).

### Uploading textures and palettes

The group draw `0024D370` calls `003AA2E0(0)` for an instance whose flag byte `+36A`<sub>h</sub> has bit 0
(`0024D448`). Once per record table (the latch word `+1A`<sub>h</sub> of `[02EBEF70]`) it uploads every record of that key:
`005011B0` for a kind-`52`<sub>h</sub> texture and `00501610` for a kind-`53`<sub>h</sub> palette; it then frees the
blocks listed at the table's `+10`<sub>h</sub>.

- `005011B0` fails on a record without image data `+C0`<sub>h</sub>. Each palette of the record (count byte
  `+A2`<sub>h</sub>) goes up through `002D81D0`, with 256 entries for format byte `+A0`<sub>h</sub> 1 and 16 for the
  others; the image goes up through `002D83B0` with the width `+A4`<sub>h</sub> and height `+A6`<sub>h</sub>.
- Its branches for format bytes `80`<sub>h</sub> and `81`<sub>h</sub>, which rebuild the size fields of the register
  word `+10`<sub>h</sub> with `002D8150`, are never taken for a record from `00500C00`, which keeps only the
  low six bits of the format.
- `00500C00` also keeps the header byte's bits 6 and 7 as the words `+1C8`<sub>h</sub> and `+1CA`<sub>h</sub>, which
  `00501190` and `005011A0` return to the draws of types `A2`<sub>h</sub>, `A5`<sub>h</sub>, `A6`<sub>h</sub>, `A8`<sub>h</sub> and `AB`<sub>h</sub>.

### The EFB loader

`0026FB90(file)` selects arena 8 (`0026FBA6`). When a bank is already parsed it first frees
every type-2 context through `0024C550(2)`, which walks `020910A0[2]` with `0024F410`
(`0026FBAE`–`0026FBCE`, `0024C599`–`0024C5B4`). It sets the EFB version
`02F8F29D` to 1 or 2 from the magic (`0026FC13`, `0026FC47`); no match pops the arena selection and
returns 0 (`0026FD75`).

For each blob it fills a zeroed template with type 2 and flags `|= 0Ch` (so the `800`<sub>h</sub> and `A00`<sub>h</sub>
runs are borrowed from the file's block), builds the context with `0024B3A0`, makes it current with
its record tables, and parses the stream (`0026FC4E`–`0026FCEE`). A failed build returns 0. After
the parse it copies the high nibble of the lowest-indexed `600`<sub>h</sub> record's `+16`<sub>h</sub> into the
context's byte `+2` (`0026FD00`–`0026FD26`).

It then publishes the rows: `02F8F228` points past the last blob, `02F8F23A` holds the row count
and `02F8F238` is set (`0026FD3A`–`0026FD56`); it returns 1.

### The rows

`0026FAD0(channel, slot, …)` does nothing until a bank is loaded, or when an instance for the
channel already exists (`0024F680`); otherwise it walks the rows with `0026F470`
(`0026FAED`–`0026FB46`).

`0026FE50(channel)` stops a channel: while a bank is loaded (`02F8F238`) it passes the request
`{kind 2, id channel}` to `0024DB80`, which unlinks and destroys every kind-2 instance in `020910F0[2]`
whose `u16 +04h` equals the id, and it clears bits `4`<sub>h</sub> and `8`<sub>h</sub> of the channel's byte
`02F8F23C[channel]`.

The third argument of `0026FAD0`, the issuing script's manager when `bgeffectplay` (`00342880`)
starts a channel, goes through `0026F470` into the instance's word `+06`<sub>h</sub>, beside the channel at
`+04`<sub>h</sub>. `0026FA80(manager)` passes `{kind 2, +06h manager}`
to `0024E7D0`, the twin of `0024DB80` keyed on `+06`<sub>h</sub>, which unlinks and destroys every bank
instance that manager started. The skip paths `00360710` and `00360A50` call it, and so do
`bgeffectsync` (`003436B0`) and `animesync` (`00355300`) while their manager is skipping
(`00267310`).

`0024F650(instance)` returns the next instance of the same list with the same channel word
`+04`<sub>h</sub>, or 0. Two readers walk a channel with it:

- `0026FDB0(channel)` answers 0 for a channel of `40`<sub>h</sub> or more, 4 with no instance, 2 as soon as
  one instance's state `+370`<sub>h</sub> is neither 0 nor 3, else 3 when one is in state 0 and 4 when all
  are in state 3. `00473620` turns that into 1 for 2 and 0 otherwise, for `bgeffectstatus`
  (`00343050`) and `bgeffectsync`.
- `bgeffecttrigger` (`003438A0`) calls `00270150(channel, n)`, which for `n` of 1 to 10 signals
  every instance of the channel (`0024FE70`, with arena 8 selected) and puts `n` in the low nibble
  of the word `+378`<sub>h</sub> of each one the signal reached.

`0026F470` stops at a row whose byte `+1` is not 1, steps over type-1
rows by `60`<sub>h</sub>, and for a type-3 row of the requested channel (or any channel when the filter is
−1) whose slot enable byte is set, looks up the definition (`0024F610`) and creates an effect
instance of kind 2 (`0024B270`) (`0026F4E3`–`0026F5BE`). Which channels the weather code starts is
on the [weather](../World-Areas-And-Travel/weather.md) page.

The definition byte `+5` is used in both bank versions. `0026FAD0` passes type 2 (`0026FB38`), and
the row builders compare it with the bank version `02F8F29D`, which `0026FC47` sets to 2 for
`EFB0002` and `0026FBCE`, `0026FC13` and `0026FF7A` set to 1:

- when the type and the version are both 2, the `0024F610` lookup uses key 0 instead of byte `+5`
  (`0026F546`–`0026F55B`, `0026F7A8`–`0026F7BD`), and the instance's `+373`<sub>h</sub> is byte `+5` plus 1
  (`0026F731`–`0026F748`, `0026F904`–`0026F91B`);
- otherwise the lookup uses byte `+5` and `+373`<sub>h</sub> is 1.

Scripts drive the channels through `00473640(channel, on, manager)`: with `on` set it runs
`0026FAD0(channel, 00265920(), manager)` for the current weather slot, and otherwise
`0026FE50(channel)`. `bgeffectplay(channel)` (`00C3`<sub>h</sub>, `00342880`) calls it with 0 and then 1, so
a play restarts the channel; `bgeffectstop(channel)` (`00C2`<sub>h</sub>, `00342CB0`) calls it with 0. Both pass
the issuing script's manager byte `+15`<sub>h</sub>.

### The map's effect bank

`00377DC0` builds `PS2Data\efb\<name>.efb` from the map's pack name, takes a fixed block of
`43D170`<sub>h</sub> bytes tagged `EffMapNo` and queues the read (`00377ED0`–`00377FF3`). The block is the
size of the largest shipped `.efb`. One completion, `003788F0`, parses it through `0026FF90` →
`0026FB90` and publishes it at `02ADD088`; a failed read frees the block (`00378975`). The other,
`003789A0`, hands the block to `0053DD10`, which returns 1 without reading it, and publishes it at
`02ADD088` too (`003789EE`, `00378A0B`).

Only the map teardown `00378230` frees `02ADD088`, and it does so after `0026FF50` has disposed of
the type-2 contexts and `0026F420` has run (`003783E0`–`003783FF`). A borrowed bank context never
outlives the block it reads from.

## Modding notes

- The magic must be exactly `EFX0010`, `EFX0009` or `EFX0008` with its NUL; anything else is
  skipped without a message. Write `+0C`<sub>h</sub> as the stream size; the walk stops there.
- Keep every chunk length a multiple of 16, and keep a stream's `600`<sub>h</sub>, `610`<sub>h</sub> and `620`<sub>h</sub>
  chunks in one consecutive run: a second run is ignored.
- The high nibble of a `600`<sub>h</sub> record's `+16`<sub>h</sub> is recomputed at load from the eleven bytes at
  `+0A`<sub>h</sub>; edit those bytes, not the nibble.
- A `700`<sub>h</sub> record's offsets are relative to the record plus the chunk's bias; set the bias to the
  subtype's fixed size, as every shipped chunk does.
- Record ids index fixed tables without a bound check; keep `800`<sub>h</sub> ids below 320 and `A00`<sub>h</sub> ids
  below 768, the table sizes on the resource ownership page.
- In an `EFB0002` bank, the row's definition byte `+5` does not choose the lookup key, which is 0,
  but it still sets the instance's `+373`<sub>h</sub> to byte `+5` plus 1; every shipped bank is `EFB0002`.
- A `.efb` larger than `43D170`<sub>h</sub> bytes overruns its block.

## Related

- [Effect element runtime](effect-element-runtime.md): what the emitter and definition records do
  each frame.
- [Effect element types](effect-element-types.md): the element types and the kind-`54`<sub>h</sub> mesh
  record.
- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md):
  effect tickets, contexts, borrowing and teardown.
- [Resource arenas and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md):
  the repair of borrowed data after its source moves.
- [Authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md): the value
  records the effect data is made of.
- [Map packs](../World-Areas-And-Travel/mpk-map-pack.md) and [weather](../World-Areas-And-Travel/weather.md):
  who loads a map's bank and which rows start.
- [File size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md): the file kinds of
  the `.efx` files.
