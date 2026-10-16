---
title: "UI typed lists: the authored item lists menus are composed from, their nine item types, the atlas registry their sprites come from, and the one-allocation build"
kind: "format"
category: "Game files and data tables"
addresses: "002432B0, 00243514, 00243538, 0024355C, 002497B0, 0029ECB0, 0029E7D0, 0029F4C0, 0029ED40, 0029ED30, 0029FEB0, 0029FBD0, 0029F130, 0029ED50, 002A0180, 0029F930, 002D14E0, 0029F5D0, 002435C0, 00243C00, 002482E0, 002A0060, 0024A610, 0024A5F0, 0024A5A0, 0024A4E0, 0024A440, 0024A480, 0024A1D0, 0024A710, 0208F580, 02090780, 002A00F0, 002A1A80, 00249320, 00249380, 002493D0, 00280980, 002F9920, 0020E600, 0020E620, 003931E0, 00393240, 0024A660"
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
  US path array `01EC73A0` names, for example, id 111 `save_load.mrp`); and
- the 23 units of `ps2data/image/ff12/myoshiok/<locale>/packfiles/mrppack_ys.bin` (kind 7 id 211 in the US
  array). The pack begins with 23 `u32` unit offsets from the pack start; `00280980` turns each into a pointer
  at `[0209AC30] + 8 × unit` and prepares it. It always relocates all 23 with no check for an empty
  `0xFFFFFFFF` entry, which the `in_sdver` pack (21 units) has twice; that pack is used only when
  `[01E0280C]` is 0, and it ships as 1.

A list file is requested through `00249320` (or `00249350`), whose completion `00249660` prepares the buffer
with `002A00F0`. The atlases its sprites name are separate TIM2 images, requested and registered by name
through `00249380` or `002493D0` (completion `00249670` → `0024A1D0`). The save and load screen is a typical
user: `00582790` requests id 111 through `003933F0` and image id 127 (`Tm2_Menu\DataFace_c.tm2`) under the
atlas name `dataface_c` through `00393460`.

`002432B0` builds one list. It has 113 call sites in 108 functions; each of the six type constructors is called
only by it.

## Layouts

### File header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[3]` | "MRP" |  |
| `03` | `u8` | prepared flag: 0 in the file, set to 1 by 002A00F0 |  |
| `04` | `u32` | number of atlas name records |  |
| `08` | `u32` | offset of the atlas name records (file-relative; relocated) |  |
| `10` | `u32` | end of the name records (+0x08 + 16 × count) |  |
| `1C` | `u32` | number of list records |  |
| `20` | `u32` | offset of the list records (file-relative; relocated); 0x30 in every shipped list |  |
| `24` | `u32` | number of file-row atlas registrations |  |
| `28` | `u32` | offset of the row table (file-relative; relocated); rows are 12 bytes |  |

`002A00F0` returns at once when byte `+3` is 1. Otherwise it rewrites `+0x08`, `+0x20` (through `002A1A80`) and
`+0x28` from file offsets into the engine's 32-bit encoded addresses (`0020E620` subtracts the low half of the base
at `01F83530`; `0020E600` adds the base back), rewrites each list record's `+0x10` and each row's `+0x08`, and
sets byte `+3` to 1. No count or offset is checked against the file size.

A row tagged 1 at `+0x00` registers the name at its relocated `+0x08`, with a TIM2 image 16 bytes after the name,
through `0024A440` (the readers are in `00406A60`); every shipped list has no rows.

### List record (20 bytes)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | bits 0-9 | item count (at most 1,023) bits 10-27 not read by the decoder bit 28     copied to bit 0 of the built list's header |
| `04` | `i16` | x | the list's rectangle, copied by the widgets that own it |
| `06` | `i16` | y |  |
| `08` | `u16` | width |  |
| `0A` | `u16` | height |  |
| `0C` | `u32` | a value read by the peek reader 002BF3D0 (stored in 01E0CE88) |  |
| `10` | `u32` | offset of this record's first item, relative to the record itself |  |

### Item header

Items are variable-length and say their own length, so the walk steps over any type.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | item length in bytes |  |
| `01` | `u8` | type, 1-9 |  |
| `02` | `u8` | not read by the decoder |  |
| `03` | `u8` | bit 4 (bit 28 of the first dword): drawn |  |
| `04` | `i16` | x |  |
| `06` | `i16` | y |  |
| `08` | `u16` | width |  |
| `0A` | `u16` | height |  |
| `0C` | `...` | type fields |  |

### Type fields

```
type 1, 16 bytes      +0x0C u32  list record to build as a child widget
type 2 and 9, 36 bytes
                      +0x0C u16  atlas name record index
                      +0x0E u16  sub-image code
                      +0x10 u16  record offset from the code's record (frame)
                      +0x12 u16  palette selector; 0xFF takes byte 7 of the sub-image record
                      +0x14 u32[4] vertex colours, one per corner
type 4, 28 bytes      nothing past the header is read
type 5, 24 bytes      +0x0C u32  colour
                      +0x10 u8   scale in percent; 0 means 100
                      +0x11 u8   text mode byte
                      +0x12 u16  stored in bits 6-15 of the node flags
                      +0x14 s32  string id; -1 = no text
type 7, 72 bytes      +0x0C u16  atlas name record index
                      +0x0E u16  sub-image code of the base record
                      +0x13 u8   bit 1: the fill keeps the background's palette and colour
                      +0x14 s16  background x, y offset (+0x16)
                      +0x18 u16  background left cap, middle, right cap (+0x1A, +0x1C), records from the base
                      +0x1E u16  background palette selector (0xFF = record default)
                      +0x20 u16  background length
                      +0x22 u16  background height
                      +0x24 u32  background colour
                      +0x28 s16  fill x, y offset (+0x2A)
                      +0x2C u16  fill left cap, middle, right cap (+0x2E, +0x30)
                      +0x32 u16  fill palette selector (0xFF = record default)
                      +0x34 u16  fill length at the maximum
                      +0x36 u16  fill height
                      +0x38 u32  fill colour
                      +0x3C u32  overlay colour
                      +0x40 u16  overlay atlas name record index; 0xFFFF = no overlay
                      +0x42 u16  overlay sub-image code
                      +0x44 u8   overlay palette selector (0xFF = record default)
type 8, 44 bytes      +0x0C u16  list record to show in a grid
                      +0x0E u8   columns
                      +0x0F u8   rows
```

### Atlas name record (16 bytes)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[14]` | atlas name, NUL-terminated |  |
| `0E` | `u8` | 1 once resolved (0 in the file) |  |
| `0F` | `u8` | the registry slot it resolved to (0 in the file) |  |

### Built list and node

The caller passes a 24-byte list header, usually at widget `+0x50`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | bit 0 = record bit 28, bit 1 = 1, bits 2-17 = item count |  |
| `08` | `void*` | the list record |  |
| `10` | `void*` | the block: count node pointers, then the nodes; null when the size is 0 |  |

Every node starts with the same 0x14 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | the item |  |
| `08` | `u32` | bit 0 = item bit 28 (drawn), bits 2-5 = type & 0xF, bits 6-15 cleared for the constructor |  |
| `0A` | `u16` | 0 (types 2, 9 store the frame here, type 7 a phase) |  |
| `0C` | `i16` | x, y (+0x0E), width (+0x10), height (+0x12), copied from item +0x04..+0x0B |  |

### Atlas registry slot (0x48 bytes, 64 slots at `0208F580`)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[16]` | name |  |
| `10` | `void*` | palette: the file's, or the reordered copy for format 0x14 |  |
| `18` | `void*` | the TIM2 buffer |  |
| `20` | `void*` | the first picture header (buffer + 0x10) |  |
| `28` | `void*` | a replacement palette, or null |  |
| `30` | `u64` | texture descriptor written by the layout pass |  |
| `38` | `u32` | flags: bits 0-3 caller flags, bit 5 occupied, bit 6 image bound, bit 7 in the layout, | bits 8-13 pixel format, bits 14-17 palette format, bits 18+ replacement palette colours |
| `40` | `u32` | number appended to the texture name, 0 for none |  |
| `44` | `u32` | value from 00181520 |  |

`02090780` counts registrations.

## Shipped data

Measured over every `.mrp` file and every `mrppack_ys.bin` unit in the archive.

| Fact | Value |
|---|---|
| standalone lists | 116 `.mrp` files, 12 names, in 10 locale folders (`us`, `de`, `es`, `fr`, `it`, `in` have all 12; `ch`, `cn`, `kr`, `in_sdver` lack `title_fore3.mrp`) |
| packs | 10 `mrppack_ys.bin`; 23 units in nine, 21 in `in_sdver` (the last two offsets are `0xFFFFFFFF`); 228 units |
| list files in all | 344, every one `MRP\0` with byte `+3` = 0, outer table at `0x30`, no rows |
| list records | 7,665 (1,458 in files, 6,207 in pack units); the largest holds 104 items |
| items | 30,546 (5,223 and 25,323) |
| items by type | 1: 2,661; 2: 20,181; 4: 2,017; 5: 4,484; 6: 46; 7: 278; 8: 879; types 3 and 9: none |
| item length by type | 1: 16; 2: 36; 4: 28; 5 and 6: 24; 7: 72; 8: 44; no exceptions |
| item stream | starts at the end of the outer table; each record's items follow the previous record's; 0, 4, 8 or 12 zero bytes pad it to the name records |
| record bits 10-27 | equal the record's own index in all 7,665 |
| record bit 28 | clear in 234 records |
| item byte `+2` | the item's position in its record, in all 30,546 |
| item byte `+3` | `0x10` (drawn) in 27,880, 0 in 2,666 |
| largest block | `0x1040` bytes for one list |
| atlas name records | 1,998; 49 distinct names, 28 of them referenced by items; longest 12 characters; bytes 14 and 15 zero in all |
| atlas indices | none out of range; 58 type-7 items have no overlay, 220 overlay `battle_4_c` |
| sprite palette | 12,341 of 20,181 type-2 items use the record default (`0xFF`) |
| text | 2,859 type-5 items have no string; 1,625 carry ids 12,034 to 191,536, in groups 1, 2, 18 and 19 |
| type 6 | 46 items, all type-5 text records with string id -1 and colour `0x80808080`, and each the last item of its record |
| child references | every type-1 and type-8 record index is in range; no list reaches itself; records shown by type 8 contain only types 2, 4, 5 and 6 |
| sub-images | 14 of the 28 referenced names have a same-named file in the locale's `tm2_menu` folder; all 1,298 lookups into those land inside the picture header's `eXt` block |
| `tm2_menu` images | 396 files; 366 carry `eXt` at buffer `+0x40`; 390 are 8-bit indexed (`0x13`), 6 are 4-bit (`0x14`) |

## Loader behaviour

### Measuring

`002432B0(list, file, record, parent)` resolves `[file + 0x20]` with `0020E600`, takes the record at
`index × 20`, the count from bits 0-9 (`002432E3`) and the first item from `[record + 0x10]`. It starts a total at
`count × 8` and walks the items: type `item[1]` (`00243340`) picks a size from the jump table `00243514`, and the
walk advances by `item[0]` (`0024337F`). Types 3, 6 and anything outside 1-9 add 0.

| type | node size | constructor |
|---|---|---|
| 1 | `0x20` | `0029ECB0` |
| 2, 9 | `0x40` | `0029F4C0` |
| 3, 6 | 0 | none |
| 4 | `0x20` | `0029ED40` |
| 5 | `0x30` | `0029FEB0` |
| 7 | `0xA0` | `0029F130` |
| 8 | `0x20` | `0029F930` |

### The single allocation

When the total is 0 the list's block pointer is null and nothing is built (`0024338C`). Otherwise `002497B0`
allocates the whole total from heap 3 at once (`002433A5`): the first `count × 8` bytes are the node pointers and
the nodes follow, packed in walk order. The second walk fills each pointer, writes the shared node fields
(`002433E0`-`0024342F`), calls the constructor through the table `00243538` and advances by the size in the table
`0024355C`. The decoder returns the record.

A zero-size item (type 3, 6 or out of range) still gets a pointer slot and its shared fields, written at the
address the next node takes. In the middle of a list its slot therefore points at the following item's node,
which the drawers then visit twice; as the last item it writes `0x14` bytes past the end of the block.
Every shipped type-6 item is the last in its record, so building any of those 46 records writes past
its block.

### What each type builds

- Type 1 (`0029ECB0`) creates a 192-byte widget with procedure `0029E7D0` through `00244F50` and attaches it to
  the parent with `00244960`; the node keeps it at `+0x18`. On creation the procedure decodes the record named by
  item `+0x0C` from the same file into its own `+0x50`, with itself as parent, and takes that record's rectangle.
- Types 2 and 9 (`0029F4C0`) resolve the atlas (node `+0x18`), find the sub-image record (`+0x20`), store the
  frame at `+0x0A`, the palette selector at `+0x39`, the four vertex colours at `+0x28`-`+0x37`, and set `+0x3A` to the
  first colour's fourth byte and `+0x3B` to `0x80`.
- Type 4 (`0029ED40`) stores null at node `+0x18`. Its draw arm `0029ED30` jumps to `+0x18` only when it is set,
  so the node is a callback slot that draws nothing until code stores a function there.
- Type 5 (`0029FEB0`) stores the colour (`+0x24`), the scale (`+0x28`, a float: byte / 100, or 1.0), the mode
  (`+0x2C`; `0x10` becomes `0x20` and `0x11` becomes `0x21` when the low ten bits of item `+0x12` are not 0) and, unless the id is
  -1, the string from `002F9920` at `+0x18`. `002F9920` takes the group `id / 10000` (0 to 27) and searches it;
  a missing group or id gives the empty string `01CEB638`.
- Type 7 (`0029F130`) builds a bar: the atlas at `+0x28`, the six strip pieces unpacked into `+0x4C`-`+0x7F`,
  opacities `+0x44`/`+0x45`, lengths `+0x48`/`+0x4A`, colours `+0x64`/`+0x88`, a value of 0 at `+0x18` against a
  maximum of 100 at `+0x1C`, and, with an overlay atlas, its slot at `+0x90` and `+0x0A` = `rand()` modulo the
  overlay sub-image's width.
- Type 8 (`0029F930`) creates a grid widget through `002D14E0`: columns × rows cells, each the size of the
  referenced record's width and height, with an inner widget sized to the whole grid. It decodes the referenced
  record into the inner widget with no parent, clears bit 0 of the inner list's header, copies the item
  rectangle onto the grid and attaches the grid to the parent.

### Drawing

`002435C0` and `00243C00` walk the node pointers, skip nodes whose flag bit 0 is clear, and switch on the type
bits 2-5. Types 1, 3, 6 and 8 have no arm.

- Type 2 nodes are drawn in runs: `002D9C40` opens a run, `002D9380` emits each sprite with its four vertex
  colours, and the run continues while the next node is also type 2, reopening every 12 sprites; `002D9B00`
  closes it.
- Type 9 is drawn alone by `0029F5D0` through the float emitter `002D8D10`, with the draw context's `+0x5A` set
  to `0x80` for the call (`00243651`-`00243670`).
- Type 4 goes to `0029ED30`; type 5 to `0029FBD0` (only in `002435C0`), which draws the string at `+0x18` with
  `002D8910` and draws nothing when it is null.
- Type 7 goes to `0029ED50`. It clamps the value into 0 to maximum, draws the background strip at full length,
  then the fill strip at `fill length × value / maximum`, then the overlay over the fill. `002A0180` draws a strip
  as left cap, middle stretched to the remaining length, and right cap; when the length is shorter than both
  caps it shrinks the caps in proportion.

The sprite size and source come from the sub-image record at `+0x20 + frame × 8`: `u16` x, `u16` y, then width
and height as 12-bit fields of the dword at `+4`. The palette selector's high nibble indexes a per-atlas byte table
and the low nibble is added to it; the sum goes to the draw context's `+0x5C` (`0029F5D0`, and `00243752` for a
type-2 run), which the sprite emitters use as the palette: the palette buffer offset for 8-bit images, and the
palette block and entry for 4-bit ones (`002D9380`, `002DB8A0`-`002DB8D3`).

### Reaching and recolouring nodes

- `003931E0(widget, i, j)` returns node i of the widget's list (`+0x60`). When that node is type 1 it
  returns node j of the child widget's list instead (node `+0x18`), or null when there is no child.
- `00393240(node, colour)` recolours a node from the menu colour table `0215E6C8` (`002DD7E0`; grey
  `0x80808080` without the table): colours 0 to 5 take table entries 0, 2, 3, 4, 5 and 6, and any other
  colour gives 0. A type 2 node gets the value in all four vertex colours (`+0x28`-`+0x34`); a type 5 node
  gets it as its colour `+0x24` (`00392F30`).

### Release

`002482E0` releases a widget. When bit 1 of the list header at its `+0x50` is set, it clears the bit, frees the
pointer at `+0x80` of each type-7 node (`0029F100`) and then frees the block.

### Atlas lookup

`002A0060(file, index)` returns null for index `0xFFFF`. Otherwise it takes the name record at
`[file + 0x08] + index × 16`. When byte `+0x0E` is 1 it checks that the cached slot is occupied and carries the
same name, and returns it.

Otherwise it sets `+0x0E`, scans with `0024A610` and caches the slot in `+0x0F`.
`0024A610` compares names byte for byte, case included, over the 64 occupied slots and returns 0 when nothing
matches, so a name that is not registered resolves to slot 0. Type 7's overlay repeats the same lookup inline.
The separate find-by-name `0024A5A0` returns null on a miss instead.

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

- `0024A4E0(name, flags)` takes the first free slot (bit 5 clear), copies the name to its NUL with no length
  check, zeroes `+0x28` and `+0x40`, sets the flags to `(old & 0x3FF10) | (flags & 0xF) | 0xA0`, counts
  `02090780` and returns the slot; with all 64 busy it returns null. `0024A660`, run from the menu system's
  start-up `00253970`, zeroes the 64 slots and the count.
- When the image arrives, `00249670` calls `0024A1D0(slot, buffer)`. It stores the buffer at `+0x18` and the
  picture header (buffer `+0x10`) at `+0x20`, copies the pixel format (bits 20-25 of the header's `GsTex0` at
  `+0x18`) into flag bits 8-13 and the palette format (bits 51-54) into bits 14-17, and names the texture `%s` or
  `%s%03d` with `+0x40`.
- Format `0x13` hands the pixels (header + header size) to `00181250` and the palette (header + header size +
  image size, or `+0x28` when set) to `00181000`. Format `0x14` copies the palette into a new block from
  `0036A190` in reordered 16-colour groups, then calls `00181190` and `00180E70`. Every path sets bit 6.
- `0024A440` registers and binds an already loaded image; `0024A480` also sets `+0x28` and the colour count.

`0024A710(k)` lays out texture memory for slots 0 to 62 whose flags hold bits 5, 6, 7 and bit `k`, writing each
slot's descriptor at `+0x30`; slot 63 is never visited, and clearing bit 7 leaves an atlas out of the layout.

## Modding notes

- Keep `item[0]` exact: a wrong length desynchronises every later item in the record.
- Keep each record's item stream where `+0x10` points, relative to the record's own address, and keep the
  item count to 1,023.
- To blank an item, clear item byte `+3` bit 4 rather than retyping it to 3 or 6: a zero-size item aliases the
  next node, or writes past the block when it is last.
- A record shown by a type-8 grid is built with no parent, so it must not contain type-1 or type-8 items: the
  attach step reads through the missing parent.
- Atlas names must match the registered name byte for byte, case included, and stay within 13 characters. An
  unregistered name draws from whatever slot 0 holds. A required atlas index of `0xFFFF` makes the type-2, 9 or 7
  constructor read through null.
- Sub-image codes and frame offsets are not bounds-checked against the atlas's `eXt` tables.
- Text ids must exist in a loaded string group, or the item draws the empty string.

## Related

- [Resource arenas and relocation](resource-arena-and-relocation.md): the encoded 32-bit addresses `0020E600` decodes.
- [File size tables](file-size-tables-fst.md): resource kinds, ids and the path arrays that name the list files.
- [Menu screens](../Menus-And-HUD/menu-screens.md): which screen procedure decodes which pack unit and record.
- [Widgets](../Menus-And-HUD/widgets.md): the widgets that own the lists and the children types 1 and 8 create.
- [Text drawing](../Menus-And-HUD/text-drawing.md): how type-5 text becomes glyphs.
