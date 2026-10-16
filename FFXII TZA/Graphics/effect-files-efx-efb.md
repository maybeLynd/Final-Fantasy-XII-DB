---
title: "Effect files (.efx, .efb): the effect containers, their chunk streams, the record kinds and the map effect bank"
kind: "format"
category: "Graphics"
summary: "The .efx effect stream and the .efb map effect bank: the 16-byte stream header and the three accepted versions, the chunk grammar and its seven shipped chunk types, how the loader collects runs of chunks, copies or borrows them, rewrites older 0x600 records and rebases 0x700 records, the 0xB00 record store and its ten record kinds, the EFB blob and row table, the fixed block the map's bank is read into, and the shipped census."
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
effect context from a `0x890`-byte template whose byte `+0` is the context type (the context
itself is on the [resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)
page). Five pass the stream's own `+0x0C` as the size; the EFB loader passes the blob size.

| Type | Builder | Call | Template flags `+2` |
|---:|---|---|---|
| 1 | `002FC4A0` | `002FC5D2` | 0 |
| 2 | `0026FB90` (the EFB loader) | `0026FCEE` | `0x0C` |
| 3 | `003B38B0` (the `@FEF` ticket) | `003B39B3` | `0x0C` |
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

| Type | Record header at `+0x0C` | Payload at `+0x10` | Handler |
|---|---|---|---|
| `0x600`, `0x610`, `0x620` | `+0x0D` u8 index (`0x600`) | `0x600`: an `0xA0`-byte record | `003A79C0` (`0x600`) |
| `0x700` | `+0x0C` u8 index, `+0x0E` u8 subtype | a fixed record of `0x160`, `0x200`, `0x280` or `0x300` bytes by subtype, then variable data | `003A7E80` |
| `0x800` | `+0x0C` u16 id, `+0x0E` u8 subtype (0 to 8) | an emitter record; id and subtype copied to `+0x280` / `+0x282` | `003A9730` |
| `0xA00` | `+0x0C` u16 id, `+0x0E` u8 element type | an element definition; id and type copied to `+0x42` / `+0x44` | `003A9A70` |
| `0xB00` | `+0x0C` u16 key, `+0x0E` u8 kind (`0x50`–`0x59`), `+0x0F` u8 slot | the record of that kind | `003A9EF0` |

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

The `0xB00` kinds, each built by the record store as `alloc(size)`, then `ctor`, then `loader`:

| Kind | Object | Ctor | Loader |
|---:|---:|---|---|
| `0x50` | `0x48` | `005019D0` | `00502CB0` |
| `0x51` | `0x1C` | `00503790` | `00503880` |
| `0x52` | `0x1D0` | `00500B70` | `00500C00` |
| `0x53` | `0xC0` | `005014B0` | `00501520` |
| `0x54` | `0x190` | `004354E0` | `00436D00` |
| `0x55` | `0x20` | `00503C50` | `00503CD0` |
| `0x56` | `0x20` | `00503D50` | `00503E30` |
| `0x57` | `0x30` | `00503F50` | `00504060` |
| `0x58` | `0x20` | `00504170` | `00504230` |
| `0x59` | `0x30` | `005042C0` | `00504350` |

The kind-`0x54` mesh record's layout is on [effect element types](effect-element-types.md). The
case-by-case load and destroy arms are in `effect-element-runtime-switch-family-record-store-5x.tsv`.

## Shipped data

| Fact | Value |
|---|---|
| `.efx` files | 3,288, 4,579,689,088 bytes, 1,840 to 25,310,800 bytes each, all under `ps2data/effect_finish` |
| `.efb` files | 410, 226,292,720 bytes, 7,584 to 4,444,528 bytes each, all under `ps2data/efb` |
| embedded streams | 144 `.cm` and 387 `.mpk` files, one stream each |
| streams | 4,229; every chunk walk ends exactly at `+0x0C`; `+0x08` is 1.0 in all |
| `.efx` magics | `EFX0010` 3,284, `EFX0008` 4 (`l0000.efx` in four locales) |
| stream magics | `EFX0010` 4,221, `EFX0008` 7, `EFX0009` 1 |
| `.efb` | all `EFB0002`; one blob each, its size equal to the stream's `+0x0C`, its 12 header bytes zero; `+0x0C` zero |
| `.efb` rows | 2,615, all type 3 with byte `+1` = 1; channels 0 to 63; row count equal to the header word in all 410 |
| chunks | 242,875, all flag `0x100` |
| chunk types | `0x620` 62,605; `0x800` 53,351; `0xA00` 48,868; `0xB00` 40,750; `0x610` 14,937; `0x700` 13,928; `0x600` 8,436 |
| `0x600` | bias `0xA0` in all |
| `0x700` subtypes | 0: 13,224; 1: 520; 2: 120; 3: 64; the bias equals the subtype's fixed size in all |
| `0x800` subtypes | 0: 2,153; 1: 41,058; 2: 1,237; 3: 2,502; 4: 620; 5: 2,810; 6: 26; 7: 2,203; 8: 742 |
| `0xA00` | 55 distinct element types; payload byte `+0` is 0 in all |
| `0xB00` kinds | `0x52` 16,862; `0x56` 6,746; `0x50` 5,810; `0x51` 5,352; `0x54` 2,733; `0x57` 1,843; `0x58` 746; `0x53` 374; `0x59` 284; `0x55` none |
| `0xB00` keys | key 0 in all; slot byte never 0; no key repeats within a stream |

## Loader behaviour

### The version ladder

`003EDAD0` returns at once for a size of 0 (`003EDAD2`). It compares the first eight bytes with
`EFX0010`, `EFX0009` and `EFX0008` (`003EDAE4`, `003EDB13`, `003EDB43`) and sets the version
global `01EFF3B0` to 10, 9 or 8. No match jumps to `003EE24D`, which stores 10 and returns without
reading a chunk. The successful path ends at the same store, so `01EFF3B0` is 10 whenever the
loader is not running; only the `0x600` record handler reads it, during the parse.

### The chunk walk

The walk runs from `+0x10` to `stream + size` (`003EDB7B`, `003EE221`). At entry the loader clears
bit `0x1` of the current context's byte `+3` and sets it again when the context type is 0, 2, 3, 4,
5, 6, 8 or 9 (mask `0x37D`, `003EDBA2`–`003EDBB3`). A chunk takes a run path only when its flag
is `0x100` and that bit is set (`003EDC0C`, `003EDC1D`). Anything else goes, one chunk at a time,
to `003EE2D0(chunk + 4, length − 4)`.

Each run path collects the consecutive chunks of its family, takes one block for them in arena 8
and copies them (`0036C1D0(8, 10)`, `0036A100`, `00861EBA`), then hands each record to its handler
with the chunk's bias in `02EBB738`. The copies truncate lengths to a multiple of 16.

| Family | Block at context | Handler per record |
|---|---|---|
| `0x600`, `0x610`, `0x620` | `+0x888` | `003A79C0`, `003A7B50`, `003A77F0` |
| `0x700` | `+0x880` | `003A7E80` |
| `0x800` | `+0x870`, or borrowed | `003A9730` |
| `0xA00` | `+0x878`, or borrowed | `003A9A70` |

For `0x800` and `0xA00` the loader tests the context's flag byte `+2` bit `0x4` first (`003EE117`,
`003EE018`); when it is set it stores the input pointer instead of copying (`003EE171`, `003EE078`).
What borrowing implies for the source's lifetime is on the
[resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) page, and
the repair after a moved source is on the
[arena page](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).

### The 0x600 family

The sizing pass gives a `0x600` chunk an `0xB0`-byte slot, a `0x610` chunk `0x30 + 4n` bytes with
`n` the byte at chunk `+0x13` (0 counts as `0x40`), and a `0x620` chunk its own length
(`003EDC8D`–`003EDCB1`). A `0x600` copy is zero-filled to its slot (`003EDD62`–`003EDD79`). Only
the first run in a stream is parsed: the run flag starts at 1 (`003EDAE1`), a later chunk of the
family is stepped over while it is 0 (`003EDC4D`), and the first run clears it (`003EDED5`).

`003A79C0(header)` writes the index byte to the record's `+0`, resets the 29 slots at `+0x2C` to
the encoded null, registers the record in the table at `[02EBEFA8]` (count at `+0`, entries from
`+8`) and calls `00333C80(record)`, which returns `record + 0xA0` (`003A79D4`–`003A7A21`).

`00333C80` rewrites an `EFX0009` or `EFX0008` record into the `EFX0010` layout when `01EFF3B0` is
9 or 8 (`00333CA1`, `00333DFE`). In every version it clears bit `0x2` of `+0x16` when that byte's
high nibble is `0xF`, then sets the high nibble to the index of the last non-zero byte among the
eleven at `+0x0A` (`00333F97`–`00333FD9`). The nibble in the file is therefore not the one used.

### The 0x700 records

`003A7E80(header, length)` stores the index byte as a word at record `+0xC0` and the subtype at
`+0xC2`, registers the record in the table `[[02EBEFA0]]` at the index, and calls
`004FF270(record, low32(record) + bias)` (`003A7E8A`–`003A7EC3`). `004FF270` sends subtypes 0 to 3
to `00537C80`, `00537FA0`, `00538350` and `005387B0` and returns the record unchanged for any
other (`004FF270`–`004FF2A2`).

Each subtype body rebases a fixed list of stored offsets and returns `record + 0x160`, `0x200`,
`0x280` or `0x300` (`00537CA7`, `00537FE3`, `005383A1`, `0053880F`). A rebase decodes each dword
with `0020E600`, adds the delta and encodes it again with `0020E620` (`004304F0`, `00430AF0`).

### The 0x800 and 0xA00 records

`003A9730` copies the header's id and subtype to payload `+0x280` / `+0x282`, publishes the payload
at `[[02EBEF90]] + id × 8` and calls `00442460(payload, low32(payload) + bias)`, which dispatches
on the subtype (`003A973A`–`003A9773`, `00442460`). `003A9A70` copies the id and the element type to
`+0x42` / `+0x44`, publishes the payload at `[[02EBEF78]] + id × 8` and calls the setup dispatcher
`005004C0` (`003A9A7A`–`003A9AAD`).

Neither checks the id against the table size; the tables
themselves are on the [resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)
page, and what the records do is on [effect element runtime](effect-element-runtime.md).

### Single chunks and the flag routes

`003EE2D0` stores the chunk's bias in `02EBB738` and switches on the flag (`003EE2DA`–`003EE30B`):

- `0x100`: clears `02096B40` and `02096BA4` and calls `003ED8A0`, which dispatches on the type.
  It sends `0xB00` to the record store `003A9EF0` and `0xA00` to `003A99F0` (`003EDA78`–`003EDAAD`),
  and has arms for types that no shipped stream carries.
- `0x101` and `0x102`: make a fixed instance current (`0024ED80`) and go to `003EE3B0` or
  `003EE260`. For a `0xB00` chunk these write the key word 1 or 2 (`0x101` also adds 1 to the slot
  byte) and call the second record store `003AA470` (`003EE3E1`–`003EE3EF`, `003EE291`–`003EE29C`).
- `0x103`: only type `0x4000` is passed on, to `0016D680`.
- Any other flag: the chunk is dropped.

Type-1 and type-7 contexts never set the run bit, so every chunk of their streams takes this
route.

### The record store

`003A9EF0(header)` looks for a node whose word `+0xC`, byte `+0xE` and byte `+0xF` equal the key,
kind and slot, walking the list at `[02EBEF70]` (the context's `+0x18`) through `0020E600`
(`003A9EF6`–`003A9F3D`). A match is reloaded in place by `00500980(node, payload)`
(`003A9F42`). Otherwise the kind minus `0x50`, bounded at 9, selects an arm of the table above
(`003A9F4D`–`003A9F76`).

`003AA470` is the same search with a six-arm table for kinds `0x50` to `0x55`
(`003AA47C`, `003AA4C2`, `003AA4DA`). It is reached only from the `0x101` and `0x102` routes,
which no shipped chunk takes.

### The EFB loader

`0026FB90(file)` selects arena 8 (`0026FBA6`). When a bank is already parsed it first frees
every type-2 context through `0024C550(2)`, which walks `020910A0[2]` with `0024F410`
(`0026FBAE`–`0026FBCE`, `0024C599`–`0024C5B4`). It sets the EFB version
`02F8F29D` to 1 or 2 from the magic (`0026FC13`, `0026FC47`); no match pops the arena selection and
returns 0 (`0026FD75`).

For each blob it fills a zeroed template with type 2 and flags `|= 0x0C` (so the `0x800` and `0xA00`
runs are borrowed from the file's block), builds the context with `0024B3A0`, makes it current with
its record tables, and parses the stream (`0026FC4E`–`0026FCEE`). A failed build returns 0. After
the parse it copies the high nibble of the lowest-indexed `0x600` record's `+0x16` into the
context's byte `+2` (`0026FD00`–`0026FD26`).

It then publishes the rows: `02F8F228` points past the last blob, `02F8F23A` holds the row count
and `02F8F238` is set (`0026FD3A`–`0026FD56`); it returns 1.

### The rows

`0026FAD0(channel, slot, …)` does nothing until a bank is loaded, or when an instance for the
channel already exists (`0024F680`); otherwise it walks the rows with `0026F470`
(`0026FAED`–`0026FB46`).

`0026F470` stops at a row whose byte `+1` is not 1, steps over type-1
rows by `0x60`, and for a type-3 row of the requested channel (or any channel when the filter is
−1) whose slot enable byte is set, looks up the definition (`0024F610`) and creates an effect
instance of kind 2 (`0024B270`) (`0026F4E3`–`0026F5BE`). Which channels the weather code starts is
on the [weather](../World-Areas-And-Travel/weather.md) page.

The definition byte `+5` is used in both bank versions. `0026FAD0` passes type 2 (`0026FB38`), and
the row builders compare it with the bank version `02F8F29D`, which `0026FC47` sets to 2 for
`EFB0002` and `0026FBCE`, `0026FC13` and `0026FF7A` set to 1:

- when the type and the version are both 2, the `0024F610` lookup uses key 0 instead of byte `+5`
  (`0026F546`–`0026F55B`, `0026F7A8`–`0026F7BD`), and the instance's `+0x373` is byte `+5` plus 1
  (`0026F731`–`0026F748`, `0026F904`–`0026F91B`);
- otherwise the lookup uses byte `+5` and `+0x373` is 1.

### The map's effect bank

`00377DC0` builds `PS2Data\efb\<name>.efb` from the map's pack name, takes a fixed block of
`0x43D170` bytes tagged `EffMapNo` and queues the read (`00377ED0`–`00377FF3`). The block is the
size of the largest shipped `.efb`. One completion, `003788F0`, parses it through `0026FF90` →
`0026FB90` and publishes it at `02ADD088`; a failed read frees the block (`00378975`). The other,
`003789A0`, hands the block to `0053DD10`, which returns 1 without reading it, and publishes it at
`02ADD088` too (`003789EE`, `00378A0B`).

Only the map teardown `00378230` frees `02ADD088`, and it does so after `0026FF50` has disposed of
the type-2 contexts and `0026F420` has run (`003783E0`–`003783FF`). A borrowed bank context never
outlives the block it reads from.

## Modding notes

- The magic must be exactly `EFX0010`, `EFX0009` or `EFX0008` with its NUL; anything else is
  skipped without a message. Write `+0x0C` as the stream size; the walk stops there.
- Keep every chunk length a multiple of 16, and keep a stream's `0x600`, `0x610` and `0x620`
  chunks in one consecutive run: a second run is ignored.
- The high nibble of a `0x600` record's `+0x16` is recomputed at load from the eleven bytes at
  `+0x0A`; edit those bytes, not the nibble.
- A `0x700` record's offsets are relative to the record plus the chunk's bias; set the bias to the
  subtype's fixed size, as every shipped chunk does.
- Record ids index fixed tables without a bound check; keep `0x800` ids below 320 and `0xA00` ids
  below 768, the table sizes on the resource ownership page.
- In an `EFB0002` bank, the row's definition byte `+5` does not choose the lookup key, which is 0,
  but it still sets the instance's `+0x373` to byte `+5` plus 1; every shipped bank is `EFB0002`.
- A `.efb` larger than `0x43D170` bytes overruns its block.

## Related

- [Effect element runtime](effect-element-runtime.md): what the emitter and definition records do
  each frame.
- [Effect element types](effect-element-types.md): the element types and the kind-`0x54` mesh
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
