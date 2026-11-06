---
title: "UI typed lists: the authored item lists menus are composed from, their nine item types, the atlas registry their sprites come from, and the one-allocation build"
kind: "format"
category: "Game files and data tables"
addresses: "0x002432B0, 0x00243514, 0x00243538, 0x0024355C, 0x002497B0, 0x0029ECB0, 0x0029E7D0, 0x0029F4C0, 0x0029ED40, 0x0029ED30, 0x0029FEB0, 0x0029FBD0, 0x0029F130, 0x0029ED50, 0x002A0180, 0x0029F930, 0x002D14E0, 0x0029F5D0, 0x002435C0, 0x00243C00, 0x002482E0, 0x002A0060, 0x0024A610, 0x0024A5F0, 0x0024A5A0, 0x0024A4E0, 0x0024A440, 0x0024A480, 0x0024A1D0, 0x0024A710, 0x0208F580, 0x02090780, 0x002A00F0, 0x002A1A80, 0x00249320, 0x00249380, 0x002493D0, 0x00280980, 0x002F9920, 0x0020E600, 0x0020E620, 0x003931E0, 0x00393240, 0x0024A660"
---

## What the player sees

The fixed parts of the menu screens: the title screen and its menu, save and load, the game-over screen, shops,
the quest and Clan Primer screens, location titles and the world-map menu. Every frame piece, icon, caption,
gauge and grid of cells on those screens is an item in an authored list that places a picture cut from a
texture atlas, a line of text from the string tables, a bar, or a child panel at a fixed position. Changing a
list moves, recolours or removes those pieces without touching code.

## Where it comes from

The lists ship in two forms, both starting with the magic `MRP\0`:

- standalone files `ps2data/image/ff12/myoshiok/<locale>/mrp_menu/<name>.mrp`, loaded as resource kind 7 (the
  US path array `0x01EC73A0` names, for example, id 111 `save_load.mrp`); and
- the 23 units of `ps2data/image/ff12/myoshiok/<locale>/packfiles/mrppack_ys.bin` (kind 7 id 211 in the US
  array). The pack begins with 23 `u32` unit offsets from the pack start; `0x00280980` turns each into a pointer
  at `[0x0209AC30] + 8 × unit` and prepares it.
  - It fills and relocates every unit whose slot is still null, with no check for an empty `0xFFFFFFFF` entry,
    which the `in_sdver` pack (21 units) has twice; that pack is used only when `[0x01E0280C]` is 0, and it ships
    as 1. A slot already set is left as it is and not relocated again (`0x002809A8`).
  - With the pack pointer `[0x0209AC30] + 0x3D0` null it fills nothing (`0x00280993`); on both paths it ends by
    jumping to `0x00280AD0` (`0x002809EE`).

A list file is requested through `0x00249320` (or `0x00249350`), whose completion `0x00249660` prepares the buffer
with `0x002A00F0`. The atlases its sprites name are separate TIM2 images, requested and registered by name
through `0x00249380` or `0x002493D0` (completion `0x00249670` → `0x0024A1D0`). The save and load screen is a typical
user: `0x00582790` requests id 111 through `0x003933F0` and image id 127 (`Tm2_Menu\DataFace_c.tm2`) under the
atlas name `dataface_c` through `0x00393460`.

`0x00249380(dest, kind, id, name, flags)` files the request in arena 3 (`0x00249395`), and `0x002493D0` in the arena its
fourth argument names. Both give `0x00249210` a last argument of 1, so the buffer is taken top-down, take a slot
with `0x0024A4E0(name, flags)`, store it at request `+0x18` and the completion at `+0x10` (`0x002493B6`, `0x002493BA`)
and return the slot. Nothing tests the slot: with all 64 busy it is null, and when the image arrives the binder
faults on its read of slot `+0x40` (`0x0024A206`).

`0x002432B0` builds one list. It has 113 call sites in 108 functions; each of the six type constructors is called
only by it.

## Layouts

All multi-byte fields are little-endian.

### File header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[3]` |  | value "MRP" |
| `+0x03` | `u8` |  | prepared flag: 0 in the file, set to 1 by `0x002A00F0` |
| `+0x04` | `u32` |  | number of atlas name records |
| `+0x08` | `u32` |  | offset of the atlas name records (file-relative; relocated) |
| `+0x10` | `u32` |  | end of the name records (`+0x08` + 16 × count) |
| `+0x1C` | `u32` |  | number of list records |
| `+0x20` | `u32` |  | offset of the list records (file-relative; relocated); `0x30` in every shipped list |
| `+0x24` | `u32` |  | number of file-row atlas registrations |
| `+0x28` | `u32` |  | offset of the row table (file-relative; relocated); rows are 12 bytes |

`0x002A00F0` returns at once when byte `+3` is 1. Otherwise it rewrites `+0x08`, `+0x20` (through `0x002A1A80`) and
`+0x28` from file offsets into the engine's 32-bit encoded addresses (`0x0020E620` subtracts the low half of the base
at `0x01F83530`; `0x0020E600` adds the base back), rewrites each list record's `+0x10` and each row's `+0x08`, and
sets byte `+3` to 1 (`0x002A016A`). A row's `+0x08` is an offset from the row table's start: it is added to the
decoded row table address (`0x0020E600`, `0x002A012D`; `0x002A0145`-`0x002A014E`). No count or offset is checked against
the file size.

`0x002A1A80(file)` does the `+0x20` step and the records' `+0x10`: it adds `+0x20` to the low 32 bits of the file's
address and encodes the sum (`0x002A1A96`-`0x002A1A9F`), then, for each of the `+0x1C` records, adds `+0x10` to the low
32 bits of the record's own address and encodes that (`0x002A1AC7`-`0x002A1AD9`).

A row tagged 1 at `+0x00` registers the name at its relocated `+0x08`, with a TIM2 image 16 bytes after the name,
through `0x0024A440` (the readers are in `0x00406A60`); every shipped list has no rows.

### List record (20 bytes)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | mask 0x3FF | item count (at most 1,023) mask `0xFFFFC00` read by no instruction: the decoder takes bits `0x3FF` (`0x002432E3`) and bit `0x10000000` (`0x00243329`), its 113 callers read `+0x04` to `+0x0A` of the returned record, and the peek reader `0x002BF3D0` copies the record whole (`0x002BF456`) into three fields of the menu object (`0x002BE0A0`: `+0x1088`, `+0x109C` and `+0x10B0` of the block at `+0x8FA0`), whose first dwords no instruction reads bit `0x10000000`     copied to bit `0x1` of the built list's header mask `0xE0000000` 0 in all 7,665 records; read by no instruction (the same readers as the bits under mask `0xFFFFC00`: the decoder takes the bits under mask `0x100003FF`, the 113 callers read `+0x04` to `+0x0A`, and `0x002BF3D0`'s whole copy is read by nothing) |
| `+0x04` | `i16` | x | the list's rectangle, copied by the widgets that own it |
| `+0x06` | `i16` | y |  |
| `+0x08` | `u16` | width |  |
| `+0x0A` | `u16` | height |  |
| `+0x0C` | `u32` |  | a value read by the peek reader `0x002BF3D0` (stored in `0x01E0CE88`) |
| `+0x10` | `u32` |  | offset of this record's first item, relative to the record itself |

### Item header

Items are variable-length and say their own length, so the walk steps over any type.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | item length in bytes |
| `+0x01` | `u8` |  | type, 1-9 |
| `+0x02` | `u8` |  | read by no instruction: the decoder reads `+0x00` and `+0x01` (`0x00243379`, `0x00243340`) and bit `0x10` of `+0x03` (`0x00243329`), the six constructors it calls (`0x0029F4C0`, `0x0029FEB0`, `0x0029ED40`, `0x0029F130`, `0x0029F930`, `0x0029ECB0`) read nothing at `+0x02`, and the relocator `0x002A00F0` touches no item |
| `+0x03` | `u8` |  | bit `0x10` (bit `0x10000000` of the first dword): drawn |
| `+0x04` | `i16` | x |  |
| `+0x06` | `i16` | y |  |
| `+0x08` | `u16` | width |  |
| `+0x0A` | `u16` | height |  |
| `+0x0C` | `...` |  | type fields |

### Type fields

Type 1, 16 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u32` | list record | list record to build as a child widget |

Type 2 and 9, 36 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u16` | atlas record | atlas name record index |
| `+0x0E` | `u16` | sub-image | sub-image code |
| `+0x10` | `u16` | frame | record offset from the code's record |
| `+0x12` | `u16` | palette | palette selector; `0xFF` takes byte 7 of the sub-image record |
| `+0x14` | `u32[4]` | vertex colours | one per corner |

A type 4 item is 28 bytes, and nothing past its header is read.

Type 5, 24 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u32` | colour | text colour |
| `+0x10` | `u8` | scale | scale in percent; 0 means 100 |
| `+0x11` | `u8` | text mode | text mode byte |
| `+0x12` | `u16` | node flag bits | stored in the bits under mask `0xFFC0` of the node flags |
| `+0x14` | `i32` | string id | -1 = no text |

Type 7, 72 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u16` | atlas record | atlas name record index |
| `+0x0E` | `u16` | base sub-image | sub-image code of the base record |
| `+0x13` | `u8` | fill palette flag | bit `0x2`: the fill keeps the background's palette and colour |
| `+0x14` | `i16` | background x | x offset |
| `+0x16` | `i16` | background y | y offset |
| `+0x18` | `u16` | background left | left cap, records from the base |
| `+0x1A` | `u16` | background middle | middle, records from the base |
| `+0x1C` | `u16` | background right | right cap, records from the base |
| `+0x1E` | `u16` | background palette | palette selector (`0xFF` = record default) |
| `+0x20` | `u16` | background length | length |
| `+0x22` | `u16` | background height | height |
| `+0x24` | `u32` | background colour | colour |
| `+0x28` | `i16` | fill x | x offset |
| `+0x2A` | `i16` | fill y | y offset |
| `+0x2C` | `u16` | fill left | left cap, records from the base |
| `+0x2E` | `u16` | fill middle | middle, records from the base |
| `+0x30` | `u16` | fill right | right cap, records from the base |
| `+0x32` | `u16` | fill palette | palette selector (`0xFF` = record default) |
| `+0x34` | `u16` | fill length | length at the maximum |
| `+0x36` | `u16` | fill height | height |
| `+0x38` | `u32` | fill colour | colour |
| `+0x3C` | `u32` | overlay colour | colour |
| `+0x40` | `u16` | overlay atlas | atlas name record index; `0xFFFF` = no overlay |
| `+0x42` | `u16` | overlay sub-image | sub-image code |
| `+0x44` | `u8` | overlay palette | palette selector (`0xFF` = record default) |

Type 8, 44 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u16` | list record | list record to show in a grid |
| `+0x0E` | `u8` | columns | columns |
| `+0x0F` | `u8` | rows | rows |

### Atlas name record (16 bytes)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[14]` |  | atlas name, NUL-terminated |
| `+0x0E` | `u8` |  | 1 once resolved (0 in the file) |
| `+0x0F` | `u8` |  | the atlas registry slot it resolved to (0 in the file) |

### Built list and node

The caller passes a 24-byte list header, usually at widget `+0x50`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | bit `0x1` = record bit `0x10000000`, bit `0x2` = 1, mask `0x3FFFC` = item count |
| `+0x08` | `void*` |  | the list record |
| `+0x10` | `void*` |  | the block: count node pointers, then the nodes; null when the size is 0 |

Every node starts with the same 0x14 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` |  | the item |
| `+0x08` | `u32` |  | bit `0x1` = item bit `0x10000000` (drawn), mask `0x3C` = type & `0xF`, mask `0xFFC0` cleared for the constructor |
| `+0x0A` | `u16` |  | 0 (types 2, 9 store the frame here, type 7 a phase) |
| `+0x0C` | `i16` |  | x, y (`+0x0E`), width (`+0x10`), height (`+0x12`), copied from item `+0x04`..+`0x0B` |

### Atlas registry slot (0x48 bytes, 64 slots at `0x0208F580`)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[16]` | name |  |
| `+0x10` | `void*` |  | palette: the file's, or the reordered copy for format `0x14` |
| `+0x18` | `void*` |  | the TIM2 buffer |
| `+0x20` | `void*` |  | the first picture header (buffer + `0x10`) |
| `+0x28` | `void*` |  | a replacement palette, or null |
| `+0x30` | `u64` |  | texture descriptor written by the layout pass |
| `+0x38` | `u32` |  | flags: mask `0xF` caller flags, bit `0x20` occupied, bit `0x40` image bound, bit `0x80` in the layout, mask `0x3F00` pixel format, mask `0x3C000` palette format, bits `0x40000`+ replacement palette colours |
| `+0x40` | `u32` |  | number appended to the texture name, 0 for no number |
| `+0x44` | `u32` |  | value from `0x00181520` |

`0x02090780` counts registrations.

## Shipped data

Measured over every `.mrp` file and every `mrppack_ys.bin` unit in the archive.

| Fact | Value |
|---|---|
| standalone lists | 116 `.mrp` files, 12 names, in 10 locale folders (`us`, `de`, `es`, `fr`, `it`, `in` have all 12; `ch`, `cn`, `kr`, `in_sdver` lack `title_fore3.mrp`) |
| packs | 10 `mrppack_ys.bin`; 23 units in nine, 21 in `in_sdver` (the last two offsets are `0xFFFFFFFF`); 228 units |
| list files in all | 344, every one `MRP\0` with byte `+3` = 0, outer table at file offset `0x30`, no rows |
| list records | 7,665 (1,458 in files, 6,207 in pack units); the largest holds 104 items |
| every list record | one row each in [`ui-typed-lists-records-rows.tsv`](ui-typed-lists-records-rows.tsv), 7,665 rows: carrier file, pack unit, index, item count, mask `0xFFFFC00`, bit `0x10000000`, mask `0xE0000000`, rectangle, the `+0x0C` value and the first item's offset |
| every item | one row each in [`ui-typed-lists-items-rows.tsv`](ui-typed-lists-items-rows.tsv), 30,546 rows: carrier, unit, record, position, length, type, bytes `+2` and `+3`, rectangle and the type fields in hex |
| items | 30,546 (5,223 and 25,323) |
| items by type | 1: 2,661; 2: 20,181; 4: 2,017; 5: 4,484; 6: 46; 7: 278; 8: 879; types 3 and 9: 0 |
| item length by type | 1: 16; 2: 36; 4: 28; 5 and 6: 24; 7: 72; 8: 44; no exceptions |
| item stream | starts at the end of the outer table; each record's items follow the previous record's; 0, 4, 8 or 12 zero bytes pad it to the name records |
| record bits under mask `0xFFFFC00` | equal the record's own index in all 7,665 |
| record bit `0x10000000` | clear in 234 records |
| item byte `+2` | the item's position in its record, in all 30,546 |
| item byte `+3` | `0x10` (drawn) in 27,880, 0 in 2,666 |
| largest block | `0x1040` bytes for one list |
| atlas name records | 1,998; 49 distinct names, 28 of them referenced by items; longest 12 characters; bytes 14 and 15 zero in all |
| atlas indices | no index out of range; 58 type-7 items have no overlay, 220 overlay `battle_4_c` |
| sprite palette | 12,341 of 20,181 type-2 items use the record default (`0xFF`) |
| text | 2,859 type-5 items have no string; 1,625 carry ids 12,034 to 191,536, in groups 1, 2, 18 and 19 |
| type 6 | 46 items, all type-5 text records with string id -1 and colour `0x80808080`, and each the last item of its record |
| child references | every type-1 and type-8 record index is in range; no list reaches itself; records shown by type 8 contain only types 2, 4, 5 and 6 |
| sub-images | 14 of the 28 referenced names have a same-named file in the locale's `tm2_menu` folder; all 1,298 lookups into those land inside the picture header's `eXt` block |
| `tm2_menu` images | 396 files; 366 carry `eXt` at buffer `+0x40`; 390 are 8-bit indexed (`0x13`), 6 are 4-bit (`0x14`) |

## Loader behaviour

### Measuring

`0x002432B0(list, file, record, parent)` resolves `[file + 0x20]` with `0x0020E600`, takes the record at
`index × 20`, the count from bits `0x3FF` (`0x002432E3`) and the first item from `[record + 0x10]`. It starts a total at
`count × 8` and walks the items: type `item[1]` (`0x00243340`) picks a size from the jump table `0x00243514`, and the
walk advances by `item[0]` (`0x0024337F`). Types 3, 6 and anything outside 1-9 add 0.

| type | node size | constructor |
|---|---|---|
| 1 | `0x20` | `0x0029ECB0` |
| 2, 9 | `0x40` | `0x0029F4C0` |
| 3, 6 | 0 | no constructor |
| 4 | `0x20` | `0x0029ED40` |
| 5 | `0x30` | `0x0029FEB0` |
| 7 | `0xA0` | `0x0029F130` |
| 8 | `0x20` | `0x0029F930` |

### The single allocation

When the total is 0 the list's block pointer is null and nothing is built (`0x0024338C`). Otherwise `0x002497B0`
allocates the whole total from heap 3 at once (`0x002433A5`): the first `count × 8` bytes are the node pointers and
the nodes follow, packed in walk order. The second walk fills each pointer, writes the shared node fields
(`0x002433E0`-`0x0024342F`), calls the constructor through the table `0x00243538` and advances by the size in the table
`0x0024355C`. The decoder returns the record, also when it builds nothing (`0x002434FB`).

Nothing tests the block: `0x002497B0` returns what `0x0036A100` gives (`0x002497C7`), and a null block from a full heap
makes the first pointer store fault (`0x002433E4`). Both walks step to the next item with a 32-bit add (`0x0024337F`,
`0x002434E0`), which keeps only the low 32 bits of the item's address. Types 1 and 8 get the parent as a third
argument (`0x0024347F`, `0x0024348F`).

A zero-size item (type 3, 6 or out of range) still gets a pointer slot and its shared fields, written at the
address the next node takes. In the middle of a list its slot therefore points at the following item's node,
which the drawers then visit twice; as the last item it writes `0x14` bytes past the end of the block.
Every shipped type-6 item is the last in its record, so building any of those 46 records writes past
its block.

### What each type builds

- Type 1 (`0x0029ECB0`) creates a 192-byte widget with procedure `0x0029E7D0` through `0x00244F50` and attaches it to
  the parent with `0x00244960`; the node keeps it at `+0x18`. On creation the procedure decodes the record named by
  item `+0x0C` from the same file into its own `+0x50`, with itself as parent, and takes that record's rectangle.
- The creation record carries the file as its low 32 bits only (`0x0029ECC7`) and the index from item `+0x0C`
  (`0x0029ECE9`). On message 1 `0x0029E7D0` decodes (`0x0029E7F7`), stores the rectangle at `+0x98`-`+0x9E`
  (`0x0029E812`-`0x0029E828`), sets `+0x40` bit `0x40000`, which skips the per-tick update (`0x0029E82F`), and answers
  0; every other message goes to `0x005C5230` (`0x0029E7E3`).
- Types 2 and 9 (`0x0029F4C0`) resolve the atlas (node `+0x18`), find the sub-image record (`+0x20`), store the
  frame at `+0x0A`, the palette selector at `+0x39`, the four vertex colours at `+0x28`-`+0x37`, and set `+0x3A`
  to the first colour's fourth byte and `+0x3B` to `0x80`.
- The atlas is `0x002A0060(file, item +0x0C)` (`0x0029F4DA`), used with no test: an index of `0xFFFF` gives null, and
  the read of slot `+0x20` faults (`0x0029F4E7`). `+0x20` is the record of the base code item `+0x0E`. A selector
  `+0x12` of `0x00FF` takes byte 7 of the frame's record, `+0x20 + frame × 8` (`0x0029F528`-`0x0029F531`), any other
  value its low byte; `+0x38` is set to 0 (`0x0029F53F`).
- Type 4 (`0x0029ED40`) stores null at node `+0x18`. Its draw arm `0x0029ED30` jumps to `+0x18` only when it is set,
  so the node is a callback slot that draws nothing until code stores a function there.
- Type 5 (`0x0029FEB0`) stores the colour (`+0x24`), the scale (`+0x28`, a float: byte / 100, or 1.0), the mode
  (`+0x2C`; `0x10` becomes `0x20` and `0x11` becomes `0x21` when the low ten bits of item `+0x12` are not 0) and, unless the id is
  -1, the string from `0x002F9920` at `+0x18`. `0x002F9920` takes the group `id / 10000` (0 to 27) and searches it;
  a missing group or id gives the empty string `0x01CEB638`.
- `0x0029FEB0` first sets `+0x18` to null (`0x0029FEC0`), which an id of -1 leaves, and `+0x20` to the encoded null
  `0x0020E620(0)` (`0x0029FECA`-`0x0029FECF`). It puts the low ten bits of item `+0x12` in node bits `0xFFC0`
  (`0x0029FF08`-`0x0029FF17`), which the mode test reads, and zeroes `+0x2D` and `+0x2F` (`0x0029FF3A`-`0x0029FF3E`).
- Type 7 (`0x0029F130`) builds a bar: the atlas at `+0x28`, the six strip pieces unpacked into `+0x4C`-`+0x7F`,
  opacities `+0x44`/`+0x45`, lengths `+0x48`/`+0x4A`, colours `+0x64`/`+0x88`, a value of 0 at `+0x18` against a
  maximum of 100 at `+0x1C`, and, with an overlay atlas, its slot at `+0x90` and `+0x0A` = `rand()` modulo the
  overlay sub-image's width.
- Type 8 (`0x0029F930`) creates a grid widget through `0x002D14E0`: columns × rows cells, each the size of the
  referenced record's width and height, with an inner widget sized to the whole grid. It decodes the referenced
  record into the inner widget with no parent, clears bit `0x1` of the inner list's header, copies the item
  rectangle onto the grid and attaches the grid to the parent.
- The node keeps the grid at `+0x18` (`0x0029F9B6`). The record `0x0029F930` hands to `0x002D14E0` has flags `0x28`,
  columns × rows items, the columns, the referenced record's width and height as the cell size, no painter and
  the parent as owner (`0x0029F962`-`0x0029F9AC`).

### Drawing

`0x002435C0` and `0x00243C00` walk the node pointers, skip nodes whose flag bit `0x1` is clear, and switch on the type
bits `0x3C`. Types 1, 3, 6 and 8 have no arm.

- Type 2 nodes are drawn in runs: `0x002D9C40` opens a run, `0x002D9380` emits each sprite with its four vertex
  colours, and the run continues while the next node is also type 2, reopening every 12 sprites; `0x002D9B00`
  closes it.
- Type 9 is drawn alone by `0x0029F5D0` through the float emitter `0x002D8D10`, with the draw context's `+0x5A` set
  to `0x80` for the call (`0x00243651`-`0x00243670`), offsets 0, 0 and a fifth argument of 0.0
  (`0x00243655`-`0x00243662`).
- Type 4 goes to `0x0029ED30`; type 5 to `0x0029FBD0` (only in `0x002435C0`), which draws the string at `+0x18` with
  `0x002D8910` at the node's y `+0x0E` (`0x0029FDFD`) and draws nothing when it is null (`0x0029FBEE`).
- `0x0029FBD0` first sets the draw context from the node (`0x0029FBF4`-`0x0029FC39`): `+0x66` from `+0x2D`, the size
  `+0x60` from the scale `+0x28`, `+0x64` from the low byte of the field under mask `0xFFC0` of `+0x08`, `+0x65` from
  `+0x2F`, the palette byte `+0x5C` from the mode `+0x2C`, and the colour `+0x90` from `+0x24` unless the
  context's `+0x5C` bit `0x40000` is set.
- Node bit `0x2` sets the context's alpha scale `+0x5A` to `0x80` for the call (`0x0029FC26`, `0x0029FE02`). The
  text's x is the node's x `+0x0C`, or `+0x0A` when `+0x2D` has a bit of `0x38` (`0x0029FC3C`-`0x0029FC44`).
- With `+0x2D` bit `0x4` it measures the text (`0x002D8B00`, `0x0029FC8C`) and clips the draw to the node's rectangle,
  at least as tall as the scaled text, `h = max(+0x12, (int)(textH × +0x28))`, and cut to the context's clip box
  `+0x48`-`+0x4E` (`0x00249FD0`, `0x0029FD78`); it restores the clip afterwards (`0x002D8530`, `0x0029FE10`).
- The clip rectangle in 16-bit sums, with `c` the draw context and bare offsets the node's:
  `x = max(c[+0x48] + +0x0C, c[+0x48])`, `y = max(c[+0x4A] + +0x0E, c[+0x4A])`, `w = +0x10` and that `h`;
  then `w = c[+0x48] + c[+0x4C] - x` when `x + w > c[+0x48] + c[+0x4C]`, and `h = c[+0x4A] + c[+0x4E] - y` when
  `y + h > c[+0x4A] + c[+0x4E]`. `0x00249FD0` runs only when `w > 0` and `h > 0` (`0x0029FC91`-`0x0029FD78`).
- In that case a text whose scaled width exceeds the node's width `+0x10` scrolls (`cmp ebp, ebx`, `0x0029FD81`):
  with `r = +0x0A - +0x10` (`+0x0A` less that width, `0x0029FD96`-`0x0029FD9A`), the field under mask `0xFFC0`
  becomes the absolute value of `([0x0208F574] / 4) mod 2r - r`, and x is the node's x less it
  (`0x0029FD85`-`0x0029FDC8`). A text that fits is centred in the node's width (`0x0029FDCC`-`0x0029FDDB`).
- Type 7 goes to `0x0029ED50`. It clamps the value into 0 to maximum, draws the background strip at full length,
  then the fill strip at `fill length × value / maximum`, then the overlay over the fill.
- `0x002A0180` draws a strip of length `len` as left cap `L`, middle `len − L − R` and right cap `R` (the pieces' `s16` widths at `+0x04`
  and `+0x14`), the middle only when it is positive; when `len − L − R < 0` it draws only the caps,
  `L × len / (L + R)` and `R × len / (L + R)` wide (`idiv`; `0x002A028D`-`0x002A029B`, `0x002A0351`-`0x002A038C`).
- With a non-zero last argument (`0x002A01B4`) `0x002A0180` draws the left cap `L` at `x`, the middle `len − L` after
  it when `L < len`, and the right cap `R` at `x + len`, past the strip's end, so no cap is shrunk. A strip with
  `len <= 0` draws nothing.
- `0x002A0180` emits each piece with `0x002D8D40(writer, draw, picture, source, x, y, w, h, flags)` (`0x002A0209` to
  `0x002A0410`). Into the VIF packet go the picture bind (TEX0_1 with the palette offset from the draw's `+0x5C`;
  a PSM `0x14` picture is bound as `0x13` with its palette entry in a second record for register `0x16`),
  register `0x14` = 0, CLAMP_1 (register 8) to the source box, and four vertices.
- The vertices carry the draw's colour `+0x90`-`+0x93`, the source corners as texture coordinates and the
  destination corners at depth `+0x70`; flag bit `0x2` is added when the two sizes differ. `0x002D8D40` then hands the
  same quad to the renderer (`0x00181890` with the source box, `0x001813F0`).
- With `+0x20` bit `0x4000000` set and an overlay atlas at `+0x90`, `0x0029ED50` then draws the overlay along the fill
  with `0x002A0440` (`0x0029F0BF`); the bar drawer `0x0029E840` calls it too (`0x0029EC7C`). `0x002A0440` emits each
  vertex with `0x002A1900(vertex, u, v, x, y, alpha, dx, dy, du, dv, draw)`, at twenty sites passing an alpha of
  `0x10` or `0x80`.
- `0x002A1900` takes the colour from the draw's `+0x94`-`+0x96` and the alpha `+0x97 x alpha / 128`. Its texture
  coordinates are `(u + du + 8) / 16` and `(v + dv + 8) / 16`, and the point `(x + dx, y + dy, [+0x70])` goes
  through the draw's matrix (`0x00202B70`, `0x00202CA0`); `0x00181350(vertex, 1)` takes the vertex.

The sprite size and source come from the sub-image record at `+0x20 + frame × 8`: `u16` x, `u16` y, then width
and height as 12-bit fields of the dword at `+4`. The palette selector's high nibble indexes a per-atlas byte table
and the low nibble is added to it; the sum goes to the draw context's `+0x5C` (`0x0029F5D0`, and `0x00243752` for a
type-2 run), which the sprite emitters use as the palette: the palette buffer offset for 8-bit images, and the
palette block and entry for 4-bit ones (`0x002D9380`, `0x002DB8A0`-`0x002DB8D3`).

`0x0029F5D0(node, draw, dx, dy, f)` takes the frame as signed (`0x0029F5DA`) and draws that source box into the node's
own rectangle moved by dx and dy (`0x0029F63B`-`0x0029F675`) with `0x002D8D10(draw, atlas, source, destination, block,
1.0)` (`0x0029F6CD`). The block holds 0, f and the address of the vertex colours `+0x28` (`0x0029F643`, `0x0029F625`,
`0x0029F67E`). Besides the list drawers it is called from six sites from `0x00277481` to `0x002777B2` and from
`0x003C5D02` and `0x003C5D3C`.

### Reaching and recolouring nodes

- `0x003931E0(widget, i, j)` returns node i of the widget's list (`+0x60`). When that node is type 1 it
  returns node j of the child widget's list instead (node `+0x18`), or null when there is no child. Neither
  index is tested against a count, and a null widget faults on the read at address 8 (`0x003931EB`-`0x003931FB`).
- `0x00393240(node, colour)` recolours a node from the menu colour table `0x0215E6C8` (`0x002DD7E0`; grey
  `0x80808080` without the table or for an entry at or above the count `0x0215E6B8`, `0x002DD7E2`-`0x002DD7FE`): colours
  0 to 5 take table entries 0, 2, 3, 4, 5 and 6, and any other
  colour gives 0. A type 2 node gets the value in all four vertex colours (`+0x28`-`+0x34`); a type 5 node
  gets it as its colour `+0x24` (`0x00392F30`).

- `0x00394690(widget, i)` returns node i of the widget's list (`+0x50` count, `+0x60` block) or null past the
  count, and `0x00394660(widget, i)` returns a type 1 node's child widget `+0x18`, or 0. `0x00285F40(widget, i)`
  returns node i of `+0x60` with no count test, or 0 for a null widget; ten on-screen keyboard functions from `0x00286010` to `0x00288A60` and `0x00559E30` call it.
- `0x00394800(widget, i, a, b)` and `0x00394850(widget, i, j, a, b)` write a number (`0x0029F6E0`) into node i, or,
  when node i is type 1, into node 0 or node j of its child widget; the Clan Primer, quest and Save pages call
  them (`0x0056FCB0`, `0x005789D0`, `0x0057EFE0`).
- `0x0029F480(node, colour, which)` writes a colour to `+0x88` and `+0x64` for which 0, `+0x88` alone for 1 and
  `+0x64` alone for 2; the party list (`0x002986E0`), the battle menu (`0x0029A930`) and `0x00570530`, `0x00581490`,
  `0x00581930` use it.
- `0x0029F580(ref, picture)` binds a picture: the picture at `ref + 0x18` and, at `+0x20`, the cell record that
  the frame code at the item's `+0x0E` selects through the picture header's tables (`+0x40`, `+0x44`); the list
  item `0x00292390` calls it.
- `0x0029FA40(node)` centres a text node: it measures the text `+0x18` (`0x002D8B00`) and sets x `+0x0A` to the
  node's left `+0x0C` plus half its width less half the text width times the scale `+0x28`; `0x0029FAD0(node)`
  sets `+0x0A` to the scaled text width instead and sets `+0x2D` bit `0x4`.
- The on-screen keyboard (`0x00286010`,
  `0x002862A0`, `0x00286500`, `0x00287E60`, `0x002880B0`) and `0x0056C490` use the first, the Graphics Settings rows
  (`0x0023B6F0`) and `0x0023CAF0` the second.
- `0x00393190(list, on)` sets or clears the drawn bit `0x1` of every node of a list; `0x00393220(node)` returns the
  item's bit `0x10000000` for a drawn node, else 0 (`0x00407450`, `0x00407720`).
- `0x00243260(list, i, out)` copies node i's x, y, width and height (`+0x0C`-`+0x12`) into `out` and returns
  1, or returns 0 when i reaches the header's count. The verb `fsmenu_getrectlist` (`0x701D`, through
  `0x005685B0`) and `0x0056C490`, `0x0056D940`, `0x00579230` and `0x0057AC10` use it.
- `0x00243580(list)` clears the drawn bit `0x1` of every node; the gambit screen (`0x00568BB0`), `0x003FCFE0`, `0x003FDDE0`
  and five other callers use it. `0x00243E90(list)` gives every node its item's bit `0x10000000` back as the drawn bit
  (`0x00283E40`, `0x00292390`, `0x002D28E0`).
- `0x00243EE0(list)` puts every node back at its item's x and y (item `+4`, `+6`): types 2, 5 and 9 into node
  `+0x0C`/`+0x0E`, type 8 into its grid widget's position `+0x98`/`+0x9A`; `0x002C4720` calls it.

### Release

`0x002482E0` releases a widget ([Widgets](../Menus-And-HUD/widgets.md)): it first releases the children and unlinks the
widget (`0x002482EE`-`0x00248331`). When bit `0x2` of the list header at its `+0x50` is set, it clears the bit
(`0x0024833B`-`0x00248343`) and, when the block at `+0x60` is set, frees the pointer at `+0x80` of each type-7 node
(type bits `0x1C`, `0x0029F100`), then frees the block (`0x003697F0`) and zeroes `+0x60` (`0x0024838E`-`0x00248398`).

A list without bit `0x2` keeps its block. The release then sends message 24, clears the procedure, frees the
storage unless `+0x40` bit `0x4000` marks it borrowed (`0x002483A0`-`0x002483F0`) and jumps to `+0x08` when that is set
(`0x00248405`).

### Atlas lookup

`0x002A0060(file, index)` returns null for index `0xFFFF`. Otherwise it takes the name record at
`[file + 0x08] + index × 16`. When byte `+0x0E` is 1 it checks that the cached slot is occupied and carries the
same name, and returns it.

Otherwise it sets `+0x0E`, scans with `0x0024A610` and caches the slot in `+0x0F`.
`0x0024A610` compares names byte for byte, case included, over the 64 occupied slots and returns 0 when nothing
matches, so a name that is not registered resolves to slot 0. Type 7's overlay repeats the same lookup inline.
The separate find-by-name `0x0024A5A0` returns null on a miss instead.

### Sub-image lookup

With `A` = slot `+0x20` (the picture header) and `T = A + 0x30`, the start of the TIM2 `eXt` block:

```python
page = u16[T + 0x14 + (code >> 8) × 2]
entry = u16[T + 0x14 + (page + (code & 0xFF)) × 2]
record = T + u16[T + 0x10] + entry × 8          8 bytes: x, y, w:12, h:12, byte 7 default palette selector
```

`u16[T + 0x12]` is the offset of the palette byte table. Types 2 and 9 then step `frame` records on; type 7 counts
its six pieces from the base record.

### Registering and filling an atlas

- `0x0024A4E0(name, flags)` takes the first free slot (bit `0x20` clear), copies the name to its NUL with no length
  check, or for a null name zeroes the slot's first 16 bytes (`0x0024A542`, `0x0024A562`-`0x0024A565`), zeroes `+0x28`
  and `+0x40`, sets the flags to `(old & 0x3FF10) | (flags & 0xF) | 0xA0`, counts `0x02090780` and returns the
  slot; with all 64 busy it returns null (`0x0024A53C`).
- `0x0024A660`, run from the menu system's start-up `0x00253970`, zeroes the 64 slots and the count.
- When the image arrives, `0x00249670` calls `0x0024A1D0(slot, buffer)`. It stores the buffer at `+0x18` and the
  picture header (buffer `+0x10`) at `+0x20`, copies the pixel format (mask `0x3F00000` of the header's `GsTex0` at
  `+0x18`) into flag bits under mask `0x3F00` and the palette format (mask `0x78000000000000`) into bits `0x3C000`, and names the texture `%s` or
  `%s%03d` with `+0x40`.
- Format `0x13` hands the pixels (header + header size) to `0x00181250` and the palette (header + header size +
  image size, or `+0x28` when set) to `0x00181000`. Format `0x14` copies the palette into a new block from
  `0x0036A190` in reordered 16-colour groups, then calls `0x00181190` and `0x00180E70`. Every path sets bit `0x40`.
- `0x0024A440(image, name, flags)` registers and binds an already loaded image: it takes a slot with
  `0x0024A4E0(name, flags)`, binds it with `0x0024A1D0(slot, image)` and returns the slot (`0x0024A456`-`0x0024A469`).
  With all 64 slots busy the slot is null, and the binder's first read of entry `+0x40` (`0x0024A206`) faults.
- `0x0024A480` also sets `+0x28` and the colour count, only for a count below `0x4000` (`0x0024A4AA`), and
  returns the slot. It does not test the slot either: with all 64 busy, the null slot faults at its flag
  write (`0x0024A4B1`), or with a larger count in the binder (`0x0024A206`).

`0x0024A710(k)` lays out texture memory for slots 0 to 62 whose flags hold bits `0x20`, `0x40`, `0x80` and bit `k`, writing each
slot's descriptor at `+0x30`; slot 63 is never visited, and clearing bit `0x80` leaves an atlas out of the layout.

## Modding notes

- Keep `item[0]` exact: a wrong length desynchronises every later item in the record.
- Keep each record's item stream where `+0x10` points, relative to the record's own address, and keep the
  item count to 1,023.
- To blank an item, clear item byte `+3` bit `0x10` rather than retyping it to 3 or 6: a zero-size item aliases the
  next node, or writes past the block when it is last.
- A record shown by a type-8 grid is built with no parent, so it must not contain type-1 or type-8 items: the
  attach step reads through the missing parent.
- Atlas names must match the registered name byte for byte, case included, and stay within 13 characters. An
  unregistered name draws from whatever slot 0 holds. A required atlas index of `0xFFFF` makes the type-2, 9 or 7
  constructor read through null.
- Sub-image codes and frame offsets are not bounds-checked against the atlas's `eXt` tables.
- Text ids must exist in a loaded string group, or the item draws the empty string.

## Related

- [Resource arenas and relocation](resource-arena-and-relocation.md): the encoded 32-bit addresses `0x0020E600` decodes.
- [File size tables](file-size-tables-fst.md): resource kinds, ids and the path arrays that name the list files.
- [Menu screens](../Menus-And-HUD/menu-screens.md): which screen procedure decodes which pack unit and record.
- [Widgets](../Menus-And-HUD/widgets.md): the widgets that own the lists and the children types 1 and 8 create.
- [Text drawing](../Menus-And-HUD/text-drawing.md): how type-5 text becomes glyphs.
- [`ui-typed-lists-item-census.tsv`](ui-typed-lists-item-census.tsv): one row per shipped `.mrp` list file: its list
  records, its items and the item types seen (type:count), and where the walk over the items ends beside the
  header's `+0x08`, the start of the atlas name records (116 rows).
- [`ui-typed-lists-item-census-embedded.tsv`](ui-typed-lists-item-census-embedded.tsv): the same for the list units
  embedded in `packfiles/mrppack_ys.bin` of each language folder, one row per unit (228 rows).
- [`ui-typed-lists-atlas-name-census.tsv`](ui-typed-lists-atlas-name-census.tsv): one row per type-2 or type-7 item
  of the shipped `.mrp` files and `mrppack_ys.bin` units, with the atlas name record it selects (20,459 rows).
- [`ui-typed-lists-atlas-name-records.tsv`](ui-typed-lists-atlas-name-records.tsv): one row per distinct name in the
  shipped atlas name records, with how many files declare it and which items use it (49 rows).

In the item table, `file` is the file (`#unitNN` for a unit of `mrppack_ys.bin`), `rec` and `item` the list record
and the item's index in it, `type` the item type, `atlas_idx` the index at `+0x0C` and `name` the name of that
record, and `idx2` and `name2` the same for a type-7 item's overlay index at `+0x40` (`-` for type 2).

In the name table, `declared_files` is the number of files whose name records hold the name, `referenced` `yes` when
an item selects it, `ref_files` the files of those items, and `class` `i` for the 25 names the executable itself
carries (a literal or a registration-table entry), `iv` for the 3 it does not, and `-` for the 21 names no item
selects.
