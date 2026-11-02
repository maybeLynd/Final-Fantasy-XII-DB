---
title: "Effect files (.efx, .efb): the effect containers, their chunk streams, the record kinds and the map effect bank"
kind: "format"
category: "Graphics"
addresses: "0x003EDAD0, 0x01EFF3B0, 0x003EE2D0, 0x003ED8A0, 0x003A79C0, 0x00333C80, 0x003A7E80, 0x004FF270, 0x003A9730, 0x003A9A70, 0x003A9EF0, 0x003AA470, 0x00500980, 0x0026FB90, 0x02F8F29D, 0x0026F470, 0x0026FAD0, 0x00377DC0, 0x003788F0, 0x00378230, 0x02ADD088, 0x002FC4A0, 0x003B38B0, 0x003B29B0, 0x003B0660, 0x003B2220, 0x02EBB738"
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
- `.efb`: 410 files under `ps2data/efb/`. The field loader asks for one per map through `0x00377DC0`
  ([map packs](../World-Areas-And-Travel/mpk-map-pack.md)); see "The map's effect bank" below.
- Streams embedded in other files: 144 `.cm` model files carry one in their `@FEF` section
  ([resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)), and
  387 `.mpk` map packs carry one each. The 531 paths are listed in
  `effect-files-efx-efb-efx-embedded-stream-files.txt`.

Every stream is parsed by `0x003EDAD0(stream, size)`. Six builders call it, each after making an
effect context from a `0x890`-byte template whose byte `+0` is the context type (the context
itself is on the [resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)
page). Five pass the stream's own `+0x0C` as the size; the EFB loader passes the blob size.

| Type | Builder | Call | Template flags `+2` |
|---:|---|---|---|
| 1 | `0x002FC4A0` | `0x002FC5D2` | 0 |
| 2 | `0x0026FB90` (the EFB loader) | `0x0026FCEE` | `0x0C` |
| 3 | `0x003B38B0` (the `@FEF` ticket) | `0x003B39B3` | `0x0C` |
| 4 | `0x003B29B0` | `0x003B2A75` | 0 |
| 5 | `0x003B0660` | `0x003B0745` | 0 |
| 7 | `0x003B2220` | `0x003B226D` | 0 |

## Layouts

All multi-byte fields are little-endian.

EFX stream (offsets from the magic):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | magic | "EFX0010", "EFX0009" or "EFX0008", NUL-terminated, compared as 8 bytes |
| `+0x08` | `f32` |  | 1.0 in every shipped stream; unused by the loader |
| `+0x0C` | `u32` |  | stream size, header included; the chunk walk ends here |

```
+0x10  chunks
```

Chunk:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | length | header included; the walk adds it to the cursor |
| `+0x04` | `u16` | flag | `0x100` selects the run paths; `0x101`, `0x102` and `0x103` select other routes |
| `+0x06` | `u16` | type |  |
| `+0x08` | `i32` | bias | stored at `0x02EBB738` before each record handler runs |
| `+0x0C` | `...` |  | record header, read by the record handler |
| `+0x10` | `...` |  | record payload |

| Type | Record header at `+0x0C` | Payload at `+0x10` | Handler |
|---|---|---|---|
| `0x600`, `0x610`, `0x620` | `+0x0D` u8 index (`0x600`) | `0x600`: an `0xA0`-byte record | `0x003A79C0` (`0x600`) |
| `0x700` | `+0x0C` u8 index, `+0x0E` u8 subtype | a fixed record of `0x160`, `0x200`, `0x280` or `0x300` bytes by subtype, then variable data | `0x003A7E80` |
| `0x800` | `+0x0C` u16 id, `+0x0E` u8 subtype (0 to 8) | an emitter record; id and subtype copied to `+0x280` / `+0x282` | `0x003A9730` |
| `0xA00` | `+0x0C` u16 id, `+0x0E` u8 element type | an element definition; id and type copied to `+0x42` / `+0x44` | `0x003A9A70` |
| `0xB00` | `+0x0C` u16 key, `+0x0E` u8 kind (`0x50`–`0x59`), `+0x0F` u8 slot | the record of that kind | `0x003A9EF0` |

`0x600` record (payload, `0xA0` bytes, after `0x00333C80`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | index, written by the handler from the header byte |
| `+0x0A` | `u8[11]` |  | eleven bytes |
| `+0x16` | `u8` |  | high nibble: index of the last non-zero byte of the eleven (0 when all are 0), recomputed at load |
| `+0x2C` | `u32[29]` |  | slots, reset to the encoded null at load |

EFB file:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | magic | "EFB0001" or "EFB0002" |
| `+0x08` | `u16` |  | blob count |
| `+0x0A` | `u16` |  | row count |
| `+0x0C` | `u32` |  | 0 in every shipped file |
| `+0x10` | `blobs` |  | { u32 size; 12 bytes; EFX stream[size] } x blob count |

```
then   rows     row count rows
```

EFB row (type 3, `0xA0` bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | row type: 3 instantiates; 1 is a `0x60`-byte row that is stepped over |
| `+0x01` | `u8` |  | must be 1, or the walk stops |
| `+0x04` | `u8` | channel |  |
| `+0x05` | `u8` |  | definition id; in an EFB0002 bank the lookup uses 0 and the instance's `+0x373` gets this + 1 |

```
+0x07+s u8  enable byte for weather slot s (1 to 3)
```

The `0xB00` kinds, each built by the record store as `alloc(size)`, then `ctor`, then `loader`:

| Kind | Object | Ctor | Loader |
|---:|---:|---|---|
| `0x50` | `0x48` | `0x005019D0` | `0x00502CB0` |
| `0x51` | `0x1C` | `0x00503790` | `0x00503880` |
| `0x52` | `0x1D0` | `0x00500B70` | `0x00500C00` |
| `0x53` | `0xC0` | `0x005014B0` | `0x00501520` |
| `0x54` | `0x190` | `0x004354E0` | `0x00436D00` |
| `0x55` | `0x20` | `0x00503C50` | `0x00503CD0` |
| `0x56` | `0x20` | `0x00503D50` | `0x00503E30` |
| `0x57` | `0x30` | `0x00503F50` | `0x00504060` |
| `0x58` | `0x20` | `0x00504170` | `0x00504230` |
| `0x59` | `0x30` | `0x005042C0` | `0x00504350` |

The kind-`0x54` mesh record's layout is on [effect element types](effect-element-types.md). The
case-by-case load and destroy arms are in [`effect-element-runtime-switch-family-record-store-5x.tsv`](effect-element-runtime-switch-family-record-store-5x.tsv).

### Columns of effect-element-runtime-switch-family-record-store-5x.tsv

One row per `0xB00` kind, 10 rows, `0x50` to `0x59`.

| Column | Holds |
|---|---|
| `case_value` | the kind byte, `0x50` to `0x59` |
| `selector_byte` | the record byte the three dispatchers switch on: `+0xE`, the kind byte, on all 10 rows |
| `load_handler` | the loader for the kind, the arm `0x00500980` jumps to for case kind minus `0x50`; the same as the Loader column above |
| `destroy_handler` | the function the destroy dispatcher `0x00500850` reaches for the kind; `(via thunk ...)` when its arm jumps to a one-jump thunk first (kinds `0x50` and `0x52` to `0x54`) |
| `load_role` | what the loader reads from the stream and where it stores it in the node, with the functions it calls and their addresses |
| `destroy_role` | what the destroy body frees or clears, field by field, and for kinds `0x50` and `0x52` to `0x54` that the loader runs it first as a reset |
| `evidence` | the instruction addresses and ranges read for the load and destroy bodies, with a destroy body's size in bytes (`B`) |
| `node_size` | the bytes the arm of `0x003A9EF0` allocates for a new node (`mov ecx, size` before `call 0x0036A100`), the Object column above |
| `find_or_create_arm` | the address of that arm in `0x003A9EF0`'s jump table (kind minus `0x50`); each allocates `node_size` bytes, calls `ctor` and then the loader |

## Shipped data

| Fact | Value |
|---|---|
| `.efx` files | 3,288, 4,579,689,088 bytes, 1,840 to 25,310,800 bytes each, all under `ps2data/effect_finish` |
| `.efb` files | 410, 226,292,720 bytes, 7,584 to 4,444,528 bytes each, all under `ps2data/efb` |
| banks a zone can load | 388: `0x00377DC0` is called with kind 4 (`0x00378B1A`) and keeps the zone pack's file name without its extension (`0x00377E64`-`0x00377E83`), so of the 550 zone packs 388 name a shipped bank and 162 name no shipped bank (that read fails and frees its block). The other 22 banks match no zone pack: `alc0201`, `alc0202`, `alc0204`, `bds0102`, `bds0105`, `bds0106`, `bds0108`, `bul0103`, `rbl0102`, `rbl0114`, `rbl0118`, `rbl0120`, `rbl0123`, `rbn0105`, `rbn0106`, `rdl0105`, `rdl0110`, `rwf0102`, `rwf0104`, `rwf0108`, `vic0103` and `vic0104`. No other path requests a bank: the folder string `PS2Data\efb\` (`0x00D11110`) is read only by `0x00377DC0` (`0x00377E8A`-`0x00377EA3`), whose one caller is `0x00378A60` (`0x00378B2B`), so those 22 are never loaded |
| embedded streams | 144 `.cm` and 387 `.mpk` files, one stream each |
| streams | 4,229; every chunk walk ends exactly at `+0x0C`; `+0x08` is 1.0 in all |
| `.efx` magics | `EFX0010` 3,284, `EFX0008` 4 (`l0000.efx` in four locales) |
| stream magics | `EFX0010` 4,221, `EFX0008` 7, `EFX0009` 1 |
| `.efb` | all `EFB0002`; one blob each, its size equal to the stream's `+0x0C`, its 12 header bytes zero; `+0x0C` zero |
| `.efb` rows | 2,615, all type 3 with byte `+1` = 1; channels 0 to 63; row count equal to the header word in all 410 |
| every `.efb` | one row each in [`effect-banks-efb-files-rows.tsv`](effect-banks-efb-files-rows.tsv), 410 rows: size, SHA-256 prefix, magic, blob and row counts, the stream's magic and size, its chunks by type, that the rows end at the file end (all 410), the zone pack whose name it shares, and the fields that load it |
| which fields load a bank | `0x00331990(field)` requests the field's block pack (mode 0, `0x003319A4`) and its own pack (mode 1, `0x003319BF`), and each request asks for the bank of that pack's name (`0x00378B2B`), so a bank is the effects of the fields whose `map_ref.bin` row names its pack. The table gives those fields under `fields_own` and `fields_block`: all 388 banks with a zone pack are loaded by at least one field |
| every bank row | one row each in [`effect-banks-efb-rows.tsv`](effect-banks-efb-rows.tsv), 2,615 rows: bank, index, type, byte `+1`, channel, definition id, the three weather enable bytes and the row's 160 bytes in hex |
| chunks | 242,875, all flag `0x100` |
| chunk types | `0x620` 62,605; `0x800` 53,351; `0xA00` 48,868; `0xB00` 40,750; `0x610` 14,937; `0x700` 13,928; `0x600` 8,436 |
| `0x600` | bias `0xA0` in all |
| `0x700` subtypes | 0: 13,224; 1: 520; 2: 120; 3: 64; the bias equals the subtype's fixed size in all |
| `0x800` subtypes | 0: 2,153; 1: 41,058; 2: 1,237; 3: 2,502; 4: 620; 5: 2,810; 6: 26; 7: 2,203; 8: 742 |
| `0xA00` | 55 distinct element types; payload byte `+0` is 0 in all |
| `0xB00` kinds | `0x52` 16,862; `0x56` 6,746; `0x50` 5,810; `0x51` 5,352; `0x54` 2,733; `0x57` 1,843; `0x58` 746; `0x53` 374; `0x59` 284; `0x55` 0 |
| `0xB00` keys | key 0 in all; slot byte never 0; no key repeats within a stream |

Every shipped `.efx` file and every chunk of its stream, read with the layouts above. Each file is one stream with no second `EFX` magic inside it, its size equals its `+0x0C`, and its walk ends there. The `.efx` files hold 157,819 of the 242,875 chunks. For the 1,394 entries of [`effect-file-list.tsv`](effect-file-list.tsv) whose file ships, the `chunks`, `elements` and `textures` cells match these rows.

| table | rows | one row per |
|---|---:|---|
| [`effect-files-efx-files.tsv`](effect-files-efx-files.tsv) | 3,288 | `.efx` file |
| [`effect-files-efx-chunks-ch.tsv`](effect-files-efx-chunks-ch.tsv) | 8,603 | chunk of a file in the `ch` folder |
| [`effect-files-efx-chunks-cn.tsv`](effect-files-efx-chunks-cn.tsv) | 8,603 | chunk of a file in the `cn` folder |
| [`effect-files-efx-chunks-de.tsv`](effect-files-efx-chunks-de.tsv) | 6,900 | chunk of a file in the `de` folder |
| [`effect-files-efx-chunks-es.tsv`](effect-files-efx-chunks-es.tsv) | 6,899 | chunk of a file in the `es` folder |
| [`effect-files-efx-chunks-fr.tsv`](effect-files-efx-chunks-fr.tsv) | 6,822 | chunk of a file in the `fr` folder |
| [`effect-files-efx-chunks-in.tsv`](effect-files-efx-chunks-in.tsv) | 1,511 | chunk of a file in the `in` folder |
| [`effect-files-efx-chunks-it.tsv`](effect-files-efx-chunks-it.tsv) | 6,818 | chunk of a file in the `it` folder |
| [`effect-files-efx-chunks-jp.tsv`](effect-files-efx-chunks-jp.tsv) | 81,506 | chunk of a file in the `jp` folder |
| [`effect-files-efx-chunks-kr.tsv`](effect-files-efx-chunks-kr.tsv) | 8,603 | chunk of a file in the `kr` folder |
| [`effect-files-efx-chunks-uk.tsv`](effect-files-efx-chunks-uk.tsv) | 2,554 | chunk of a file in the `uk` folder |
| [`effect-files-efx-chunks-us.tsv`](effect-files-efx-chunks-us.tsv) | 19,000 | chunk of a file in the `us` folder |

The file table's columns:

| Column | Meaning |
|---|---|
| `path`, `folder`, `group` | the path, its language folder and its sub-folder (`chara`, `common`, `event`, `magic`, `menu`) |
| `bytes`, `sha256` | the file size and its SHA-256 |
| `magic`, `version` | the magic and the version `0x003EDAD0` sets for it: 10 for `EFX0010`, 8 for `EFX0008` |
| `float_0x08`, `stream_size` | the header's `+0x08` as an `f32`, and its `+0x0C` |
| `walk_ends_at_stream_size`, `trailing_bytes` | `yes` when the chunk walk ends exactly at `+0x0C` (all 3,288), and the bytes after `+0x0C` (0 in all) |
| `chunks`, `chunks_0x600`, `chunks_0x610`, `chunks_0x620`, `chunks_0x700`, `chunks_0x800`, `chunks_0xA00`, `chunks_0xB00` | the chunk count, then the count of each of the seven chunk types, by the type word `+0x06` of each chunk in the walk |
| `kinds_0xB00` | the `0xB00` records by kind byte `+0x0E` |
| `embedded_streams` | the offset of each further `EFX` magic inside the file; 0 in all |
| `named_by` | each resource kind and id whose path array, in any of the twelve languages, names the file, or `chara` and the lowest slot of the character table; `-` for the 43 files no entry names |

The chunk tables' columns (a column that does not apply to the chunk's type is empty):

| Column | Meaning |
|---|---|
| `path`, `chunk`, `offset` | the file, the chunk's position in the walk from 0, and its offset from the magic |
| `length`, `flag`, `type`, `bias` | the chunk header's `+0x00`, `+0x04`, `+0x06` and `+0x08` |
| `header_0x0C` | the four record-header bytes `+0x0C` to `+0x0F` in file order |
| `index` | `0x600`: byte `+0x0D`; `0x700`: byte `+0x0C` |
| `id` | `0x800` and `0xA00`: the `u16` at `+0x0C` |
| `key`, `kind`, `slot` | `0xB00`: the `u16` at `+0x0C`, byte `+0x0E` and byte `+0x0F` |
| `subtype` | `0x700` and `0x800`: byte `+0x0E` |
| `element_type` | `0xA00`: byte `+0x0E` |
| `entries_0x13` | `0x610`: byte `+0x13`, the `n` of its `0x30 + 4n`-byte slot (0 counts as `0x40`) |
| `record_0x00` | `0x600` and `0xA00`: payload byte `+0` |
| `record_0x0A`, `record_0x16` | `0x600`: the eleven payload bytes at `+0x0A`, and payload byte `+0x16` as the file holds it (the loader recomputes its high nibble) |
| `tex_format`, `tex_bit_0x40`, `tex_bit_0x80` | kind-`0x52` `0xB00`: the low six bits of payload byte `+0`, and 1 when its bit `0x40` or bit `0x80` is set |
| `tex_palettes`, `tex_reference`, `tex_size` | kind-`0x52` `0xB00`: the palette count byte `+2`, the reference size words `+4` and `+6`, and the width and height words `+8` and `+0x0A` |

### Columns of effect-banks-efb-files-rows.tsv and effect-banks-efb-rows.tsv

Every value below was checked against the 410 shipped `.efb` files; each holds one blob.

| Column | Holds |
|---|---|
| `sha256_16` | in the file table, the first 16 hex digits of the file's SHA-256 |
| `stream_magic` | the first seven bytes of the blob's `EFX` stream: `EFX0010` in 408 files, `EFX0008` in 2 |
| `stream_bytes` | the stream's size, its `+0x0C`, equal to the blob's size word in all 410 |
| `rows_end_at_file_end` | `yes` when the rows, read from the end of the last blob at `0xA0` bytes per type-3 row and `0x60` per type-1 row, end exactly at the file's end; `yes` in all 410 |
| `weather_1`, `weather_2`, `weather_3` | in the row table, the row's enable bytes for weather slots 1 to 3, row bytes `+0x08`, `+0x09` and `+0x0A`: 1 runs the row in that slot, 0 skips it (slot 1: 2,374 rows 1, 241 rows 0; slot 2: 2,268 and 347; slot 3: 2,171 and 444) |
| `row_hex` | the row's `0xA0` (160) bytes in file order as 320 hex digits |

## Loader behaviour

### The version ladder

`0x003EDAD0` returns at once for a size of 0 (`0x003EDAD2`). It compares the first eight bytes with
`EFX0010`, `EFX0009` and `EFX0008` (`0x003EDAE4`, `0x003EDB13`, `0x003EDB43`) and sets the version
global `0x01EFF3B0` to 10, 9 or 8. No match jumps to `0x003EE24D`, which stores 10 and returns without
reading a chunk. The successful path ends at the same store, so `0x01EFF3B0` is 10 whenever the
loader is not running; only the `0x600` record handler reads it, during the parse.

### The chunk walk

The walk runs from `+0x10` to `stream + size` (`0x003EDB7B`, `0x003EE221`). At entry the loader clears
bit `0x1` of the current context's byte `+3` and sets it again when the context type is 0, 2, 3, 4,
5, 6, 8 or 9 (mask `0x37D`, `0x003EDBA2`–`0x003EDBB3`). A chunk takes a run path only when its flag
is `0x100` and that bit is set (`0x003EDC0C`, `0x003EDC1D`). Anything else goes, one chunk at a time,
to `0x003EE2D0(chunk + 4, length − 4)`.

Each run path collects the consecutive chunks of its family, takes one block for them in arena 8
and copies them (`0x0036C1D0(8, 10)`, `0x0036A100`, `0x00861EBA`), then hands each record to its handler
with the chunk's bias in `0x02EBB738`. The copies truncate lengths to a multiple of 16.

| Family | Block at context | Handler per record |
|---|---|---|
| `0x600`, `0x610`, `0x620` | `+0x888` | `0x003A79C0`, `0x003A7B50`, `0x003A77F0` |
| `0x700` | `+0x880` | `0x003A7E80` |
| `0x800` | `+0x870`, or borrowed | `0x003A9730` |
| `0xA00` | `+0x878`, or borrowed | `0x003A9A70` |

For `0x800` and `0xA00` the loader tests the context's flag byte `+2` bit `0x4` first (`0x003EE117`,
`0x003EE018`); when it is set it stores the input pointer instead of copying (`0x003EE171`, `0x003EE078`).
What borrowing implies for the source's lifetime is on the
[resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) page, and
the repair after a moved source is on the
[arena page](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).

### The 0x600 family

The sizing pass gives a `0x600` chunk an `0xB0`-byte slot, a `0x610` chunk `0x30 + 4n` bytes with
`n` the byte at chunk `+0x13` (0 counts as `0x40`), and a `0x620` chunk its own length
(`0x003EDC8D`–`0x003EDCB1`). A `0x600` copy is zero-filled to its slot (`0x003EDD62`–`0x003EDD79`). Only
the first run in a stream is parsed: the run flag starts at 1 (`0x003EDAE1`), a later chunk of the
family is stepped over while it is 0 (`0x003EDC4D`), and the first run clears it (`0x003EDED5`).

`0x003A79C0(header)` writes the index byte to the record's `+0`, resets the 29 slots at `+0x2C` to
the encoded null, registers the record in the table at `[0x02EBEFA8]` (count at `+0`, entries from
`+8`) and calls `0x00333C80(record)`, which returns `record + 0xA0` (`0x003A79D4`–`0x003A7A21`).

`0x00333C80` rewrites an `EFX0009` or `EFX0008` record into the `EFX0010` layout when `0x01EFF3B0` is
9 or 8 (`0x00333CA1`, `0x00333DFE`). In every version it clears bit `0x2` of `+0x16` when that byte's
high nibble is `0xF`, then sets the high nibble to the index of the last non-zero byte among the
eleven at `+0x0A` (`0x00333F97`–`0x00333FD9`). The nibble in the file is therefore not the one used.

### The 0x700 records

`0x003A7E80(header, length)` stores the index byte as a word at record `+0xC0` and the subtype at
`+0xC2`, registers the record in the table `[[0x02EBEFA0]]` at the index, and calls
`0x004FF270(record, low32(record) + bias)` (`0x003A7E8A`–`0x003A7EC3`). `0x004FF270` sends subtypes 0 to 3
to `0x00537C80`, `0x00537FA0`, `0x00538350` and `0x005387B0` and returns the record unchanged for any
other (`0x004FF270`–`0x004FF2A2`).

Each subtype body rebases a fixed list of stored offsets and returns `record + 0x160`, `0x200`,
`0x280` or `0x300` (`0x00537CA7`, `0x00537FE3`, `0x005383A1`, `0x0053880F`). A rebase decodes each dword
with `0x0020E600`, adds the delta and encodes it again with `0x0020E620` (`0x004304F0`, `0x00430AF0`).

### The 0x800 and 0xA00 records

`0x003A9730` copies the header's id and subtype to payload `+0x280` / `+0x282`, publishes the payload
at `[[0x02EBEF90]] + id × 8` and calls `0x00442460(payload, low32(payload) + bias)`, which dispatches
on the subtype (`0x003A973A`–`0x003A9773`, `0x00442460`). `0x003A9A70` copies the id and the element type to
`+0x42` / `+0x44`, publishes the payload at `[[0x02EBEF78]] + id × 8` and calls the setup dispatcher
`0x005004C0` (`0x003A9A7A`–`0x003A9AAD`).

Neither checks the id against the table size; the tables
themselves are on the [resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)
page, and what the records do is on [effect element runtime](effect-element-runtime.md).

### Single chunks and the flag routes

`0x003EE2D0` stores the chunk's bias in `0x02EBB738` and switches on the flag (`0x003EE2DA`–`0x003EE30B`):

- `0x100`: clears `0x02096B40` and `0x02096BA4` and calls `0x003ED8A0`, which dispatches on the type.
  It sends `0xB00` to the record store `0x003A9EF0` and `0xA00` to `0x003A99F0` (`0x003EDA78`–`0x003EDAAD`),
  and has arms for types that no shipped stream carries.
- `0x101` and `0x102`: make a fixed instance current (`0x0024ED80`) and go to `0x003EE3B0` or
  `0x003EE260`. For a `0xB00` chunk these write the key word 1 or 2 (`0x101` also adds 1 to the slot
  byte) and call the second record store `0x003AA470` (`0x003EE3E1`–`0x003EE3EF`, `0x003EE291`–`0x003EE29C`).
- `0x103`: only type `0x4000` is passed on, to `0x0016D680`.
- Any other flag: the chunk is dropped.

Type-1 and type-7 contexts never set the run bit, so every chunk of their streams takes this
route.

### The single-chunk arms

`0x003ED8A0(chunk, length)` switches on the chunk's type word `+2` and hands the body at `+8` to one
arm.

A record arm takes an index (0 means the first free slot), frees whatever already holds that
slot, takes a block for the copy, and copies and rebases the body as the run paths do. The context
tables it fills are allocated with the context by `0x0024B3A0`: `0x003A7D00` (`0x400` bytes, 128 `0x700`
slots), `0x003A9560` (`0xA00` bytes, 320 `0x800` slots) and `0x003A9920` (`0x1800` bytes, 768 `0xA00`
slots), each zeroed; `0x003A76F0` empties the `0x600` table `[0x02EBEFA8]` (256 pointers from `+8`) and its count.

| Type | Arm | What it does |
|---|---|---|
| `0x401` | inline | the effect camera: the 64-byte matrix at `+8` goes to `0x02AEE9E0` through `0x0039D430`, which then calls `0x0039AFA0` and copies the workbench matrix to `0x02AEECB0` (`0x003970A0`); `0x003CC0F0` resets the camera record `0x02096D30` and copies the matrix to its `+0x60`, the dwords `+0x48`–`+0x54` are stored at its `+0x00`, `+0x04`, `+0x08` and `+0x10` (`0x02096D30`, `0x02096D34`, `0x02096D38`, `0x02096D40`; `0x003ED96F`-`0x003ED98A`), and the record is submitted with priority `0x64` (`0x003829D0`) while `0x02096887` is set |
| `0x500` | `0x003A75B0` | frees every `0x600` record of `[0x02EBEFA8]` and zeroes the table; when the context's byte `+3` bit `0x1` is set (the records sit in the run block) it frees only their 29 slot targets whose byte `+1` is 0, then the context's `+0x888` block |
| `0x510` | `0x003A7CB0` | frees all 128 `0x700` records |
| `0x520` | `0x003A9510` | frees the `0x800` records |
| `0x530` | `0x003A98D0` | frees the `0xA00` definitions |
| `0x540` | `0x003A9E00` | unlinks the record-store node whose key, kind and slot match the body and frees it (`0x00500850`) |
| `0x600` | `0x003A7A50` | gets or creates the `0x600` record for byte `+1` (`0x003A78A0`, which allocates `0xA0` bytes and registers it with `0x00333BB0` / `0x00333AC0`), copies the `0x2C`-byte header into it and calls `0x00333C80` |
| `0x601` | `0x003A7950` | frees the `0x600` record of byte `+1` |
| `0x610` | `0x003A7AE0` | gets or creates the `0x600` record of byte `+0`, finds its sub-entry byte `+1` (`0x00334000`) and copies a dword and the entry's own byte count of data into it |
| `0x611` | `0x003A7AA0` | passes byte `+2` to `0x003340C0` for the `0x600` record of byte `+1` |
| `0x620` | `0x003A7730` | as `0x610`, but takes a new block for the sub-entry (`0x0046F380`), copies the body from `+0x10` and rebases it (`0x004FF320`) |
| `0x700` | `0x003A7DC0` | the record through `0x003A7BE0` and `0x004FF270`; when it replaced a record, every `0x700` object of the instance that pointed at the old one (`+0xE0`) is pointed at the new one |
| `0x800` | `0x003A96A0` | the record through `0x003A9790` and `0x00442460`; a replaced record is swapped in every emitter (`+0x100`), every definition link (`+0x108`) and every element link (`+0x18`, `+0x20`) of the current instance (`0x003A9590`) |
| `0x900` | `0x003A92B0` | releases every emitter of the current instance (`0x003A9160`) |
| `0xA00` | `0x003A99F0` | the definition through `0x003A9AD0` and `0x005004C0` |
| `0xB00` | `0x003A9EF0` | the record store |
| `0x1000` | `0x0016D680` | returns its argument and does nothing else |

The `0x600` arm resets the 29 slots at `+0x2C` only for a new record (`0x00333BB0`); an existing
record keeps its slots, where the run-path handler `0x003A79C0` resets them every time.

Outside the run block, the `0x500` arm and the `0x601` arm empty a record before freeing it through
`0x00333C00`, which releases each of the 29 slots (`0x0046F370`, `0x003697F0`) and stores the encoded
null `0x0020E620(0)` in it.

### The record store

`0x003A9EF0(header)` looks for a node whose word `+0xC`, byte `+0xE` and byte `+0xF` equal the key,
kind and slot, walking the list at `[0x02EBEF70]` (the context's `+0x18`) through `0x0020E600`
(`0x003A9EF6`–`0x003A9F3D`). A match is reloaded in place by `0x00500980(node, payload)`
(`0x003A9F42`). Otherwise the kind minus `0x50`, bounded at 9, selects an arm of the table above
(`0x003A9F4D`–`0x003A9F76`).

`0x003AA470` is the same search with a six-arm table for kinds `0x50` to `0x55`
(`0x003AA47C`, `0x003AA4C2`, `0x003AA4DA`). It is reached only from the `0x101` and `0x102` routes,
which no shipped chunk takes.

Its arms build each kind with the same constructor as the first store but a loader of its own
(`0x003AA4FD`–`0x003AA5E1`), and a match is reloaded through `0x00500A60`, which dispatches on the kind
byte to the same loaders:

| Kind | Second loader | What it reads |
|---:|---|---|
| `0x50` | `0x005032D0` | a row count, texture and palette counts, then `0x48`-byte rows |
| `0x51` | `0x00503BA0` | a `u16` count, then that many 16-byte entries, copied to a new block |
| `0x52` | `0x005C5230` | nothing: it returns 0 |
| `0x53` | `0x00501750` | a mode byte (`0xFF` empty), a count and a slot byte, then 64-byte (mode 0) or 1,024-byte (mode 1) palettes |
| `0x54` | `0x00436D00` | as the first store |
| `0x55` | `0x00503CD0` | as the first store |

- `0x005032D0` numbers the texture and palette slots 1 to n and expands each `0x48`-byte row into a
  `0x90`-byte sprite row: the four corners `(±0.5 x abs(w) x sx, ±0.5 x abs(h) x sy)` of its rectangle (row
  `+0x08`, `+0x0C` the size `w`, `h`; `+0x18`, `+0x1C` the scales), rotated about z by the row's angle
  `+0x20 x 2π / 360` and offset by `+0x10`, `+0x14`; the last row gets bit `0x2` of `+0x70`
  (`0x005032D0`-`0x0050378D`).
- `0x00503180(record)` then resolves the kind-`0x50` record's slot bytes into handles with
  `0x003AA280(key, 0x52, slot)` and `0x003AA280(key, 0x53, slot)`, and turns each row's pixel rectangle
  into texture coordinates by dividing by the texture's width `+0xA4` and height `+0xA6`.
- `0x00501750` ends by running `0x00503180` again over every kind-`0x50` record of key 1 (`0x003AA1F0`,
  `0x003AA240`), so palettes loaded later still reach the sprites.

### The kind-0x52 texture loader

`0x00500C00(record, data)` reads a texture record. A first byte of `0xFF` is an empty record. Otherwise
it keeps the byte's low six bits as the format `+0xA0`, bit `0x40` as the word `+0x1C8` and bit `0x80` as
`+0x1CA`, the palette count from byte `+2` at `+0xA2`, a reference size from words `+4` and `+6` at
`+0x1CC` and `+0x1CE`, and the width and height from words `+8` and `+0x0A` at both `+0xA4`/`+0xA6` and
`+0xA8`/`+0xAA`. The palettes start at `+0x10`.

Each palette gets two handles: format 0 has 16-colour palettes of `0x40` bytes and format 1 256-colour
palettes of `0x400` bytes (`0x001837A0` and `0x00183760`); a record with palettes in any other format
makes the loader return null. The palette data is copied to a new block at
`+0xB0` (`0x0036A100`), or used in place when bit `0x8` of byte `+2` of `[0x02F97340]` is set.

The texture's allocated size is the width and height rounded up to a power of two (`0x0017FEA0`). With
`+0x1C8` set it is instead scaled to the reference size: each side is `side / reference ×
pow2(reference)`, and an image whose size and reference size are both 1920 × 1080 keeps that size. The
format picks the builder, and its handle goes to `+0xC0` with a code at `+0xB8`:

| Format | Builder | Pixel bytes | `+0xB8` |
|---:|---|---|---:|
| 0 | `0x00183EE0`, 4-bit indices | `w × h / 2` | `0x14` |
| 1 | `0x00184140`, 8-bit indices | `w × h` | `0x13` |
| 2 | `0x00183A00` | `w × h × 2` | 2 |
| 3 | `0x00183C60` | `w × h × 3` | 1 |
| 4 | `0x00183EB0`, 32-bit pixels (`0x0017E8E0`) | `w × h × 4` | 0 |
| `0x80` | `0x00184130`, as format 0 | `w × h × 4` | `0x14` |
| `0x81` | `0x00184370`, as format 1 at twice the width and height | `w × h × 4` | `0x13` |

Format bytes `0x80` and `0x81` cannot occur after the six-bit mask; any other format leaves the record
without a texture.

`0x00183A00` and `0x00183C60` create an `RGBA8` texture (format object `0x02CF7480`) of the allocated size,
or of the image size when the allocation is only one larger. They map it (`0x0017EBD0`), clear it when
the sizes differ, and write one byte per texel, the first of each four: `0x00183A00` the low four bits
of the first byte of each two-byte source pixel, `0x00183C60` the first byte of each three-byte pixel.
Then they commit it (`0x0062C360`).

### Uploading textures and palettes

The group draw `0x0024D370` calls `0x003AA2E0(0)` for an instance whose flag byte `+0x36A` has bit `0x1`
(`0x0024D448`). Once per record table (the latch word `+0x1A` of `[0x02EBEF70]`) it uploads every record of that key:
`0x005011B0` for a kind-`0x52` texture and `0x00501610` for a kind-`0x53` palette; it then frees the
blocks listed at the table's `+0x10`.

- `0x005011B0` fails on a record without image data `+0xC0`. Each palette of the record (count byte
  `+0xA2`) goes up through `0x002D81D0`, with 256 entries for format byte `+0xA0` 1 and 16 for the
  others; the image goes up through `0x002D83B0` with the width `+0xA4` and height `+0xA6`.
- Its branches for format bytes `0x80` and `0x81`, which rebuild the size fields of the register
  word `+0x10` with `0x002D8150`, are never taken for a record from `0x00500C00`, which keeps only the
  low six bits of the format.
- `0x00500C00` also keeps the header byte's bits `0x40` and `0x80` as the words `+0x1C8` and `+0x1CA`, which
  `0x00501190` and `0x005011A0` return to the draws of types `0xA2`, `0xA5`, `0xA6`, `0xA8` and `0xAB`.

### The EFB loader

`0x0026FB90(file)` selects arena 8 (`0x0026FBA6`). When a bank is already parsed it first frees
every type-2 context through `0x0024C550(2)`, which walks `0x020910A0[2]` with `0x0024F410`
(`0x0026FBAE`–`0x0026FBCE`, `0x0024C599`–`0x0024C5B4`). It sets the EFB version
`0x02F8F29D` to 1 or 2 from the magic (`0x0026FC13`, `0x0026FC47`); no match pops the arena selection and
returns 0 (`0x0026FD75`).

For each blob it fills a zeroed template with type 2 and flags `|= 0x0C` (so the `0x800` and `0xA00`
runs are borrowed from the file's block), builds the context with `0x0024B3A0`, makes it current with
its record tables, and parses the stream (`0x0026FC4E`–`0x0026FCEE`). A failed build returns 0. After
the parse it copies the high nibble of the lowest-indexed `0x600` record's `+0x16` into the
context's byte `+2` (`0x0026FD00`–`0x0026FD26`).

It then publishes the rows: `0x02F8F228` points past the last blob, `0x02F8F23A` holds the row count
and `0x02F8F238` is set (`0x0026FD3A`–`0x0026FD56`); it returns 1.

The loader also copies the low byte of the file's `u16` blob count `+0x08` into `0x02F8F239` (`0x0026FD3A`-`0x0026FD3E`)
and stores 0 in `0x02F8F220` (`0x0026FD5D`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02F8F220` | `u32` | 0 (zero-filled tail of `.data`) | a word of the bank's state that every store sets to 0 | the bank reset `0x0026F9F0` (`0x0026F9F9`); `0x0026FB90` (`0x0026FD5D`, from `r15d`, zeroed at `0x0026FBAB` and not written after) | no read: the bases that `0x0026FFA0` (`0x0026FFA8`) and `0x002700F0` (`0x002700F8`) form at this address reach only the channel bytes from `+0x1C`, `0x02F8F23C` (`0x0026FFE0`, `0x00270102`), and no other RIP-relative, image-base-relative or address-forming reference names it |
| `0x02F8F239` | `u8` | 0 (zero-filled tail of `.data`) | the low byte of the loaded file's blob count | `0x0026FB90` (`0x0026FD3E`); cleared by the 4-byte stores at `0x02F8F238`: `0x0026F9F0` (`0x0026FA02`), `0x0026FB90` before a reload (`0x0026FBC0`) and the bank disposal `0x0026FF50` (`0x0026FF69`) | no read: every RIP-relative read of `0x02F8F238` is a 1-byte compare, the word read of `0x02F8F23A` (`0x0026FB27`) starts after it, and no other RIP-relative, image-base-relative or address-forming reference names it; the compares are (`0x0026F9D0`, `0x0026FA99`, `0x0026FAED`, `0x0026FBAE`, `0x0026FE6B`, `0x0026FF54`, `0x0027016B`) |

### The rows

`0x0026FAD0(channel, slot, …)` does nothing until a bank is loaded, or when an instance for the
channel already exists (`0x0024F680`); otherwise it walks the rows with `0x0026F470`
(`0x0026FAED`–`0x0026FB46`).

`0x0026FE50(channel)` stops a channel: while a bank is loaded (`0x02F8F238`) it passes the request
`{kind 2, id channel}` to `0x0024DB80`, which unlinks and destroys every kind-2 instance in `0x020910F0[2]`
whose `u16 +0x04` equals the id, and it clears bits `0x4` and `0x8` of the channel's byte
`0x02F8F23C[channel]`.

The channel bytes are 64 flag bytes at `0x02F8F23C`, one per channel (an instance's word `+0x04`), followed by 32 at
`0x02F8F27C`, one per issuing manager (the instance's word `+0x06`). The bank reset `0x0026F9F0` (called from `0x00259180`
at `0x002591E1`) sets all 96 to 3 with twelve 8-byte stores, from `0x02F8F23C` to `0x02F8F294` (`0x0026FA12`-`0x0026FA5F`).

The twelve stores are seven bytes apart, from `0x0026FA12`. `0x02F8F23C`, `0x02F8F244`, `0x02F8F24C`, `0x02F8F254`,
`0x02F8F25C`, `0x02F8F264`, `0x02F8F26C` and `0x02F8F274` take the channel bytes 0-63 eight at a time; `0x02F8F27C`,
`0x02F8F284`, `0x02F8F28C` and `0x02F8F294` take the manager bytes 0-31.

The update pass holds a bank instance (state 1 then runs only `0x003A7EE0` and `0x003A93F0`) when its channel byte or
its manager byte has neither bit `0x1` nor bit `0x4` (`0x0024BB2B`-`0x0024BB51`), and the draw gate `0x0024D770` refuses one
unless both bytes have bit `0x2` (`0x0024D7CD`-`0x0024D7E9`):

| Bit | Meaning | Written by | Read by |
|---|---|---|---|
| 0 (1) | the channel runs | `0x002700F0(channel, on)` (`0x0027011D` sets it, `0x0027010C` clears it); `0x0026FFA0(on)` for all 64 (`0x00270092`-`0x002700A6` set, `0x0026FFE0`-`0x00270046` clear); the update pass's rewrite below | `0x0024B9B0` (`0x0024BB36` channel, `0x0024BB49` manager); `0x0026FAD0` (`0x0026FB63`) |
| 1 (2) | the channel is drawn | `0x00270130(channel, on)` (`0x00270144`, `0x00270148`); `0x002700C0(on)` for all 64 (`0x002700D0`-`0x002700DD`) | `0x0024D770` (`0x0024D7D1` channel, `0x0024D7E0` manager) |
| 2 (4) | run one more step | `0x0026FAD0` (`0x0026FB69`, when bit `0x1` is clear); `0x002700F0(channel, 0)` and `0x0026FFA0(0)`, when bit `0x8` is set (`0x00270115`; `0x0026FFE0`-`0x00270046`); cleared by `0x0026FE50` (`0x0026FE92`), by `0x002700F0(channel, 1)` (`0x00270119`-`0x0027011D`), by `0x0026FFA0(1)` and by the rewrite | `0x0024B9B0` (`0x0024BB36`, `0x0024BB49`, and in the rewrite `0x0024BEBA`, `0x0024BF13`) |
| 3 (8) | started since the last update pass | `0x0026FAD0` (`0x0026FB5D`); cleared by `0x0026FE50` (`0x0026FE92`), by the map teardown's `0x0026F420` (`0x0026F440`-`0x0026F459`) and by the rewrite | `0x002700F0` (`0x0027010F`); `0x0026FFA0` (`0x0026FFF2`, `0x0027002A`) |

After the kind-2 update pass has walked a non-empty list, `0x0024B9B0` rewrites the 64 channel bytes
(`0x0024BE75`-`0x0024BF5A`): every byte loses bit `0x8`, and a byte that had bit `0x4` also loses bits `0x4` and `0x1`.

`0x0026FFA0` and
`0x002700C0` are called with 1 from `0x0026C8C0` (`0x0026CA61`, `0x0026CA6B`). `0x002700F0` is called by `0x003E8440`
(`0x003E855B`), `0x003E85B0` (`0x003E8656`), `0x003E8690` (`0x003E87B3`) and `0x003E8C50` (`0x003E8D0F`), and `0x00270130` by
`0x003E8690` (`0x003E87C0`) and `0x003E8C50` (`0x003E8D18`) ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)). The
reset stores the 32 manager bytes, and `0x0024BB49` and `0x0024D7E0` read them.

The third argument of `0x0026FAD0`, the issuing script's manager when `bgeffectplay` (`0x00342880`)
starts a channel, goes through `0x0026F470` into the instance's word `+0x06`, beside the channel at
`+0x04`. `0x0026FA80(manager)` passes `{kind 2, +0x06 manager}`
to `0x0024E7D0`, the twin of `0x0024DB80` keyed on `+0x06`, which unlinks and destroys every bank
instance that manager started. The skip paths `0x00360710` and `0x00360A50` call it, and so do
`bgeffectsync` (`0x003436B0`) and `animesync` (`0x00355300`) while their manager is skipping
(`0x00267310`).

`0x0024F650(instance)` returns the next instance of the same list with the same channel word
`+0x04`, or 0. Two readers walk a channel with it:

- `0x0026FDB0(channel)` answers 0 for a channel of `0x40` or more, 4 with no instance, 2 as soon as
  one instance's state `+0x370` is neither 0 nor 3, else 3 when one is in state 0 and 4 when all
  are in state 3. `0x00473620` turns that into 1 for 2 and 0 otherwise, for `bgeffectstatus`
  (`0x00343050`) and `bgeffectsync`.
- `bgeffecttrigger` (`0x003438A0`) calls `0x00270150(channel, n)` through the one-jump stub `0x00473610`, which for `n` of
  1 to 10 signals
  every instance of the channel (`0x0024FE70`, with arena 8 selected) and puts `n` in the low nibble
  of the word `+0x378` of each one the signal reached.

`0x0026F470` stops at a row whose byte `+1` is not 1, steps over type-1
rows by `0x60`, and for a type-3 row of the requested channel (or any channel when the filter is
−1) whose slot enable byte is set, looks up the definition (`0x0024F610`) and creates an effect
instance of kind 2 (`0x0024B270`) (`0x0026F4E3`–`0x0026F5BE`). Which channels the weather code starts is
on the [weather](../World-Areas-And-Travel/weather.md) page.

The definition byte `+5` is used in both bank versions. `0x0026FAD0` passes type 2 (`0x0026FB38`), and
the row builders compare it with the bank version `0x02F8F29D`, which `0x0026FC47` sets to 2 for
`EFB0002` and `0x0026FBCE`, `0x0026FC13` and `0x0026FF7A` set to 1:

- when the type and the version are both 2, the `0x0024F610` lookup uses key 0 instead of byte `+5`
  (`0x0026F546`–`0x0026F55B`, `0x0026F7A8`–`0x0026F7BD`), and the instance's `+0x373` is byte `+5` plus 1
  (`0x0026F731`–`0x0026F748`, `0x0026F904`–`0x0026F91B`);
- otherwise the lookup uses byte `+5` and `+0x373` is 1.

Scripts drive the channels through `0x00473640(channel, on, manager)`: with `on` set it runs
`0x0026FAD0(channel, 0x00265920(), manager)` for the current weather slot, and otherwise
`0x0026FE50(channel)`. `bgeffectplay(channel)` (`0x00C3`, `0x00342880`) calls it with 0 and then 1, so
a play restarts the channel; `bgeffectstop(channel)` (`0x00C2`, `0x00342CB0`) calls it with 0. Both pass
the issuing script's manager byte `+0x15`.

### The map's effect bank

`0x00377DC0` builds `PS2Data\efb\<name>.efb` from the map's pack name, takes a fixed block of
`0x43D170` bytes tagged `EffMapNo` and queues the read (`0x00377ED0`–`0x00377FF3`). The block is the
size of the largest shipped `.efb`. One completion, `0x003788F0`, parses it through `0x0026FF90` →
`0x0026FB90` and publishes it at `0x02ADD088`; a failed read frees the block (`0x00378975`). The other,
`0x003789A0`, hands the block to `0x0053DD10`, which returns 1 without reading it, and publishes it at
`0x02ADD088` too (`0x003789EE`, `0x00378A0B`).

Only the map teardown `0x00378230` frees `0x02ADD088`, and it does so after `0x0026FF50` has disposed of
the type-2 contexts and `0x0026F420` has run (`0x003783E0`–`0x003783FF`). A borrowed bank context never
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
