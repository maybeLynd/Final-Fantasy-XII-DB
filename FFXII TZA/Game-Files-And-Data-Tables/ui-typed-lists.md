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
  at `[0x0209AC30] + 8 × unit` and prepares it. It always relocates all 23 with no check for an empty
  `0xFFFFFFFF` entry, which the `in_sdver` pack (21 units) has twice; that pack is used only when
  `[0x01E0280C]` is 0, and it ships as 1.

A list file is requested through `0x00249320` (or `0x00249350`), whose completion `0x00249660` prepares the buffer
with `0x002A00F0`. The atlases its sprites name are separate TIM2 images, requested and registered by name
through `0x00249380` or `0x002493D0` (completion `0x00249670` → `0x0024A1D0`). The save and load screen is a typical
user: `0x00582790` requests id 111 through `0x003933F0` and image id 127 (`Tm2_Menu\DataFace_c.tm2`) under the
atlas name `dataface_c` through `0x00393460`.

`0x002432B0` builds one list. It has 113 call sites in 108 functions; each of the six type constructors is called
only by it.

## Layouts

### File header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[3]` | "MRP" |  |
| `+0x03` | `u8` | prepared flag: 0 in the file, set to 1 by 0x002A00F0 |  |
| `+0x04` | `u32` | number of atlas name records |  |
| `+0x08` | `u32` | offset of the atlas name records (file-relative; relocated) |  |
| `+0x10` | `u32` | end of the name records (+0x08 + 16 × count) |  |
| `+0x1C` | `u32` | number of list records |  |
| `+0x20` | `u32` | offset of the list records (file-relative; relocated); 0x30 in every shipped list |  |
| `+0x24` | `u32` | number of file-row atlas registrations |  |
| `+0x28` | `u32` | offset of the row table (file-relative; relocated); rows are 12 bytes |  |

`0x002A00F0` returns at once when byte `+3` is 1. Otherwise it rewrites `+0x08`, `+0x20` (through `0x002A1A80`) and
`+0x28` from file offsets into the engine's 32-bit encoded addresses (`0x0020E620` subtracts the low half of the base
at `0x01F83530`; `0x0020E600` adds the base back), rewrites each list record's `+0x10` and each row's `+0x08`, and
sets byte `+3` to 1. No count or offset is checked against the file size.

A row tagged 1 at `+0x00` registers the name at its relocated `+0x08`, with a TIM2 image 16 bytes after the name,
through `0x0024A440` (the readers are in `0x00406A60`); every shipped list has no rows.

### List record (20 bytes)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | bits 0-9 | item count (at most 1,023) bits 10-27 not read by the decoder bit 28     copied to bit 0 of the built list's header |
| `+0x04` | `i16` | x | the list's rectangle, copied by the widgets that own it |
| `+0x06` | `i16` | y |  |
| `+0x08` | `u16` | width |  |
| `+0x0A` | `u16` | height |  |
| `+0x0C` | `u32` | a value read by the peek reader 0x002BF3D0 (stored in 0x01E0CE88) |  |
| `+0x10` | `u32` | offset of this record's first item, relative to the record itself |  |

### Item header

Items are variable-length and say their own length, so the walk steps over any type.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | item length in bytes |  |
| `+0x01` | `u8` | type, 1-9 |  |
| `+0x02` | `u8` | not read by the decoder |  |
| `+0x03` | `u8` | bit 4 (bit 28 of the first dword): drawn |  |
| `+0x04` | `i16` | x |  |
| `+0x06` | `i16` | y |  |
| `+0x08` | `u16` | width |  |
| `+0x0A` | `u16` | height |  |
| `+0x0C` | `...` | type fields |  |

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
| `+0x00` | `char[14]` | atlas name, NUL-terminated |  |
| `+0x0E` | `u8` | 1 once resolved (0 in the file) |  |
| `+0x0F` | `u8` | the registry slot it resolved to (0 in the file) |  |

### Built list and node

The caller passes a 24-byte list header, usually at widget `+0x50`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | bit 0 = record bit 28, bit 1 = 1, bits 2-17 = item count |  |
| `+0x08` | `void*` | the list record |  |
| `+0x10` | `void*` | the block: count node pointers, then the nodes; null when the size is 0 |  |

Every node starts with the same 0x14 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | the item |  |
| `+0x08` | `u32` | bit 0 = item bit 28 (drawn), bits 2-5 = type & 0xF, bits 6-15 cleared for the constructor |  |
| `+0x0A` | `u16` | 0 (types 2, 9 store the frame here, type 7 a phase) |  |
| `+0x0C` | `i16` | x, y (+0x0E), width (+0x10), height (+0x12), copied from item +0x04..+0x0B |  |

### Atlas registry slot (0x48 bytes, 64 slots at `0x0208F580`)

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[16]` | name |  |
| `+0x10` | `void*` | palette: the file's, or the reordered copy for format 0x14 |  |
| `+0x18` | `void*` | the TIM2 buffer |  |
| `+0x20` | `void*` | the first picture header (buffer + 0x10) |  |
| `+0x28` | `void*` | a replacement palette, or null |  |
| `+0x30` | `u64` | texture descriptor written by the layout pass |  |
| `+0x38` | `u32` | flags: bits 0-3 caller flags, bit 5 occupied, bit 6 image bound, bit 7 in the layout, | bits 8-13 pixel format, bits 14-17 palette format, bits 18+ replacement palette colours |
| `+0x40` | `u32` | number appended to the texture name, 0 for none |  |
| `+0x44` | `u32` | value from 0x00181520 |  |

`0x02090780` counts registrations.

## Shipped data

Measured over every `.mrp` file and every `mrppack_ys.bin` unit in the archive.

| Fact | Value |
|---|---|
| standalone lists | 116 `.mrp` files, 12 names, in 10 locale folders (`us`, `de`, `es`, `fr`, `it`, `in` have all 12; `ch`, `cn`, `kr`, `in_sdver` lack `title_fore3.mrp`) |
| packs | 10 `mrppack_ys.bin`; 23 units in nine, 21 in `in_sdver` (the last two offsets are `0xFFFFFFFF`); 228 units |
| list files in all | 344, every one `MRP\0` with byte `+3` = 0, outer table at file offset `0x30`, no rows |
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

`0x002432B0(list, file, record, parent)` resolves `[file + 0x20]` with `0x0020E600`, takes the record at
`index × 20`, the count from bits 0-9 (`0x002432E3`) and the first item from `[record + 0x10]`. It starts a total at
`count × 8` and walks the items: type `item[1]` (`0x00243340`) picks a size from the jump table `0x00243514`, and the
walk advances by `item[0]` (`0x0024337F`). Types 3, 6 and anything outside 1-9 add 0.

| type | node size | constructor |
|---|---|---|
| 1 | `0x20` | `0x0029ECB0` |
| 2, 9 | `0x40` | `0x0029F4C0` |
| 3, 6 | 0 | none |
| 4 | `0x20` | `0x0029ED40` |
| 5 | `0x30` | `0x0029FEB0` |
| 7 | `0xA0` | `0x0029F130` |
| 8 | `0x20` | `0x0029F930` |

### The single allocation

When the total is 0 the list's block pointer is null and nothing is built (`0x0024338C`). Otherwise `0x002497B0`
allocates the whole total from heap 3 at once (`0x002433A5`): the first `count × 8` bytes are the node pointers and
the nodes follow, packed in walk order. The second walk fills each pointer, writes the shared node fields
(`0x002433E0`-`0x0024342F`), calls the constructor through the table `0x00243538` and advances by the size in the table
`0x0024355C`. The decoder returns the record.

A zero-size item (type 3, 6 or out of range) still gets a pointer slot and its shared fields, written at the
address the next node takes. In the middle of a list its slot therefore points at the following item's node,
which the drawers then visit twice; as the last item it writes `0x14` bytes past the end of the block.
Every shipped type-6 item is the last in its record, so building any of those 46 records writes past
its block.

### What each type builds

- Type 1 (`0x0029ECB0`) creates a 192-byte widget with procedure `0x0029E7D0` through `0x00244F50` and attaches it to
  the parent with `0x00244960`; the node keeps it at `+0x18`. On creation the procedure decodes the record named by
  item `+0x0C` from the same file into its own `+0x50`, with itself as parent, and takes that record's rectangle.
- Types 2 and 9 (`0x0029F4C0`) resolve the atlas (node `+0x18`), find the sub-image record (`+0x20`), store the
  frame at `+0x0A`, the palette selector at `+0x39`, the four vertex colours at `+0x28`-`+0x37`, and set `+0x3A` to the
  first colour's fourth byte and `+0x3B` to `0x80`.
- Type 4 (`0x0029ED40`) stores null at node `+0x18`. Its draw arm `0x0029ED30` jumps to `+0x18` only when it is set,
  so the node is a callback slot that draws nothing until code stores a function there.
- Type 5 (`0x0029FEB0`) stores the colour (`+0x24`), the scale (`+0x28`, a float: byte / 100, or 1.0), the mode
  (`+0x2C`; `0x10` becomes `0x20` and `0x11` becomes `0x21` when the low ten bits of item `+0x12` are not 0) and, unless the id is
  -1, the string from `0x002F9920` at `+0x18`. `0x002F9920` takes the group `id / 10000` (0 to 27) and searches it;
  a missing group or id gives the empty string `0x01CEB638`.
- Type 7 (`0x0029F130`) builds a bar: the atlas at `+0x28`, the six strip pieces unpacked into `+0x4C`-`+0x7F`,
  opacities `+0x44`/`+0x45`, lengths `+0x48`/`+0x4A`, colours `+0x64`/`+0x88`, a value of 0 at `+0x18` against a
  maximum of 100 at `+0x1C`, and, with an overlay atlas, its slot at `+0x90` and `+0x0A` = `rand()` modulo the
  overlay sub-image's width.
- Type 8 (`0x0029F930`) creates a grid widget through `0x002D14E0`: columns × rows cells, each the size of the
  referenced record's width and height, with an inner widget sized to the whole grid. It decodes the referenced
  record into the inner widget with no parent, clears bit 0 of the inner list's header, copies the item
  rectangle onto the grid and attaches the grid to the parent.

### Drawing

`0x002435C0` and `0x00243C00` walk the node pointers, skip nodes whose flag bit 0 is clear, and switch on the type
bits 2-5. Types 1, 3, 6 and 8 have no arm.

- Type 2 nodes are drawn in runs: `0x002D9C40` opens a run, `0x002D9380` emits each sprite with its four vertex
  colours, and the run continues while the next node is also type 2, reopening every 12 sprites; `0x002D9B00`
  closes it.
- Type 9 is drawn alone by `0x0029F5D0` through the float emitter `0x002D8D10`, with the draw context's `+0x5A` set
  to `0x80` for the call (`0x00243651`-`0x00243670`).
- Type 4 goes to `0x0029ED30`; type 5 to `0x0029FBD0` (only in `0x002435C0`), which draws the string at `+0x18` with
  `0x002D8910` and draws nothing when it is null.
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
  destination corners at depth `+0x70`; flag bit 1 is added when the two sizes differ. `0x002D8D40` then hands the
  same quad to the renderer (`0x00181890` with the source box, `0x001813F0`).
- With `+0x20` bit 26 set and an overlay atlas at `+0x90`, `0x0029ED50` then draws the overlay along the fill
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

### Reaching and recolouring nodes

- `0x003931E0(widget, i, j)` returns node i of the widget's list (`+0x60`). When that node is type 1 it
  returns node j of the child widget's list instead (node `+0x18`), or null when there is no child.
- `0x00393240(node, colour)` recolours a node from the menu colour table `0x0215E6C8` (`0x002DD7E0`; grey
  `0x80808080` without the table): colours 0 to 5 take table entries 0, 2, 3, 4, 5 and 6, and any other
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
  sets `+0x0A` to the scaled text width instead and sets `+0x2D` bit 2.
- The on-screen keyboard (`0x00286010`,
  `0x002862A0`, `0x00286500`, `0x00287E60`, `0x002880B0`) and `0x0056C490` use the first, the Graphics Settings rows
  (`0x0023B6F0`) and `0x0023CAF0` the second.
- `0x00393190(list, on)` sets or clears the drawn bit 0 of every node of a list; `0x00393220(node)` returns the
  item's bit 28 for a drawn node, else 0 (`0x00407450`, `0x00407720`).
- `0x00243260(list, i, out)` copies node i's x, y, width and height (`+0x0C`-`+0x12`) into `out` and returns
  1, or returns 0 when i reaches the header's count. The verb `fsmenu_getrectlist` (`0x701D`, through
  `0x005685B0`) and `0x0056C490`, `0x0056D940`, `0x00579230` and `0x0057AC10` use it.
- `0x00243580(list)` clears the drawn bit 0 of every node; the gambit screen (`0x00568BB0`), `0x003FCFE0`, `0x003FDDE0`
  and five other callers use it. `0x00243E90(list)` gives every node its item's bit 28 back as the drawn bit
  (`0x00283E40`, `0x00292390`, `0x002D28E0`).
- `0x00243EE0(list)` puts every node back at its item's x and y (item `+4`, `+6`): types 2, 5 and 9 into node
  `+0x0C`/`+0x0E`, type 8 into its grid widget's position `+0x98`/`+0x9A`; `0x002C4720` calls it.

### Release

`0x002482E0` releases a widget. When bit 1 of the list header at its `+0x50` is set, it clears the bit, frees the
pointer at `+0x80` of each type-7 node (`0x0029F100`) and then frees the block.

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

- `0x0024A4E0(name, flags)` takes the first free slot (bit 5 clear), copies the name to its NUL with no length
  check, zeroes `+0x28` and `+0x40`, sets the flags to `(old & 0x3FF10) | (flags & 0xF) | 0xA0`, counts
  `0x02090780` and returns the slot; with all 64 busy it returns null. `0x0024A660`, run from the menu system's
  start-up `0x00253970`, zeroes the 64 slots and the count.
- When the image arrives, `0x00249670` calls `0x0024A1D0(slot, buffer)`. It stores the buffer at `+0x18` and the
  picture header (buffer `+0x10`) at `+0x20`, copies the pixel format (bits 20-25 of the header's `GsTex0` at
  `+0x18`) into flag bits 8-13 and the palette format (bits 51-54) into bits 14-17, and names the texture `%s` or
  `%s%03d` with `+0x40`.
- Format `0x13` hands the pixels (header + header size) to `0x00181250` and the palette (header + header size +
  image size, or `+0x28` when set) to `0x00181000`. Format `0x14` copies the palette into a new block from
  `0x0036A190` in reordered 16-colour groups, then calls `0x00181190` and `0x00180E70`. Every path sets bit 6.
- `0x0024A440` registers and binds an already loaded image; `0x0024A480` also sets `+0x28` and the colour count.

`0x0024A710(k)` lays out texture memory for slots 0 to 62 whose flags hold bits 5, 6, 7 and bit `k`, writing each
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

- [Resource arenas and relocation](resource-arena-and-relocation.md): the encoded 32-bit addresses `0x0020E600` decodes.
- [File size tables](file-size-tables-fst.md): resource kinds, ids and the path arrays that name the list files.
- [Menu screens](../Menus-And-HUD/menu-screens.md): which screen procedure decodes which pack unit and record.
- [Widgets](../Menus-And-HUD/widgets.md): the widgets that own the lists and the children types 1 and 8 create.
- [Text drawing](../Menus-And-HUD/text-drawing.md): how type-5 text becomes glyphs.
