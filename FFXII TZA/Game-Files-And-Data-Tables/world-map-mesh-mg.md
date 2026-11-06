---
title: "World map mesh (.mg): the world-map geometry file, its layout and how the map screen loads and draws it"
kind: "format"
category: "Game files and data tables"
addresses: "0x00562F90, 0x00563110, 0x00274780, 0x00555A50, 0x005556A0, 0x00555400, 0x00555D10, 0x00556240, 0x00555B90, 0x00555F80, 0x00552250, 0x005528C0, 0x00550540, 0x00561390, 0x0055A8A0, 0x00D231C0, 0x00D23270, 0x0024A5A0, 0x00249210, 0x002493D0, 0x002DF9A0, 0x02CA8F38, 0x02CA8F40"
---

## What the player sees

The main menu's World Map shows Ivalice as one large picture. That picture is four textures laid side
by side on flat tiles, and the tiles come from this file. The same file also holds a second, finer mesh
that the World Map draws with a soft shading texture, and that the license board screen draws again
without a texture.

## Where it comes from

The file is `ps2data/image/ff12/myoshiok/<tree>/worldmap/meshdata.mg` in the archive, and it is kind 7,
id `0xA8` in the path arrays that `ResourcePath_Init` (`0x002DF9A0`) installs. The KR, CH and CN arrays
(`0x01E0E530`, `0x01E5A3D0`, `0x01EABBA0`) name the `ch` copy; the arrays of the other languages (one each
for languages 1 to 6, and `0x01EDD7E0` for the rest) name the `in` copy.

Two screens request it. The World Map set-up `0x00550540` calls `0x00562F90` on the World Map host kept at
`0x02CA8F38` (the host's `+0xC0`, `0x005505C6`), and the license board screen `0x00561390` requests it again for its own use
(`0x0056162B`).

`0x00550540(record)` returns null at once while `[0x02CA8F38]` is null (`0x00550551`, `0x005505FA`). Otherwise it copies
the record's words `+0x00`, `+0x08` and `+0x0C` and bits `0x1` and `0x2` of `+0x04` into the host
(`0x00550557`-`0x005505B0`, [Map screens](../Menus-And-HUD/map-screens.md)). It then opens a request group (`0x00249580`), runs
`0x00562F90` with it (`0x005505D0`), closes it (`0x00249410`), asks for the map-data widget with the World Map and
location files and the host as owner (`0x003BC440`, `0x005505E4`) and returns the host.

## Layouts

All offsets are little-endian. The file starts with a directory of two `{offset, size}` pairs:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | sub0Offset | offset of sub-mesh 0 from the file start |
| `+0x04` | `u32` | sub0Size | not read |
| `+0x08` | `u32` | sub1Offset | offset of sub-mesh 1 from the file start |
| `+0x0C` | `u32` | sub1Size | not read |

`0x00274780(buffer, i)` returns `buffer + u32[buffer + 8 × i]` (`0x00274783`, `0x00274786`); it is the only
reader of the directory. Each sub-mesh starts with a header whose offsets count from the sub-mesh start:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | idxOff | u16 index stream |
| `+0x04` | `i32` | idxCount | not read |
| `+0x08` | `i32` | vtxOff | vertex array, `0x20` bytes per vertex |
| `+0x0C` | `i32` | vtxCount | read by the tile path (sub-mesh 0) only |
| `+0x10` | `i32` | slotOff | slot array, `0x20` bytes per slot |
| `+0x14` | `i32` | slotCount | slots drawn and bound |
| `+0x18` | `u8[8]` | - | zero in both shipped sub-meshes; not read |

`0x00555A50(sub, i)` returns `sub + s32[sub + 0x10] + 0x20 × i`. A slot is:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[16]` | name | NUL-padded; the binder overwrites `+0x00`..+`0x07` with an image-entry pointer |
| `+0x10` | `i32` | indexStart | first index-stream entry of the slot's run (sub-mesh 1 path) |
| `+0x14` | `i32` | indexCount | entries in the run (sub-mesh 1 path) |
| `+0x18` | `i16[4]` | colour | R, G, B, A; `0x80` = 1.0 |

A sub-mesh 0 vertex and a sub-mesh 1 vertex share the size but not the first half:

Sub-mesh 0 (tiles):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | s | fraction of the bound texture's width |
| `+0x04` | `f32` | t | fraction of the bound texture's height |
| `+0x08` | `f32[2]` | - | 1.0 in every shipped vertex; copied with the whole vertex array into the tile packet's UNPACK chunk (`0x005556A0` at `0x00555786`: V4-32, two 16-byte quads per vertex, so these are the z and w of the first quad), which nothing on this port decodes (Drawing the tiles); the draw that reaches the GPU binds the sprite batcher's `0x30`-byte vertices, built from `+0x00`, `+0x04` and `+0x10` only (`0x005558E0`-`0x00555957`), so the GPU never sees these bytes; no instruction reads them (`0x00274780`'s other callers, `0x00563110` and `0x0055A8A0`, read the slots and sub-mesh 1) |
| `+0x10` | `f32[4]` | x, y, z, w | position |

Sub-mesh 1 (strips):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32[4]` | colour | R, G, B, A |
| `+0x10` | `f32[4]` | x, y, z, w | position |

An index entry is a `u16`: bit `0x8000` starts a new strip, and the bits under mask `0x7FFF` are the vertex index.

## Shipped data

Measured from both archive copies and the twelve file-size tables:

| Fact | Value |
|---|---|
| files | 2, `in/worldmap/meshdata.mg` and `ch/worldmap/meshdata.mg`, byte-identical; no other `.mg` ships |
| size | 13,648 bytes (`0x3550`), the size recorded for kind 7 id `0xA8` in all twelve file-size tables |
| directory | sub-mesh 0 at `0x10`, `0x2C0` bytes; sub-mesh 1 at `0x2D0`, `0x3280` bytes; together they end at the file end |
| sub-mesh 0 header | `idxOff 0x2A0`, 16 indices, `vtxOff 0xA0`, 16 vertices, `slotOff 0x20`, 4 slots |
| sub-mesh 0 slots | `main0.psd`, `main1.psd`, `main2.psd`, `main3.psd`; `indexStart` 0, 4, 8, 12; `indexCount` 4; colour (126, 126, 126, 127) |
| sub-mesh 0 tiles | `main0` x 0 to 1, z 0 to −1; `main1` x 1 to 2, z 0 to −1; `main2` x 0 to 1, z −1 to −1.25; `main3` x 1 to 2, z −1 to −1.25; y 0 and w 1 throughout |
| sub-mesh 0 indices | `0x8002, 0, 1, 3` repeated for each tile (+4 per tile) |
| bound textures | `w_main0.tm2` and `w_main1.tm2` 1024 × 1024, `w_main2.tm2` and `w_main3.tm2` 1024 × 256, `w_shade_p.tm2` 512 × 512 |
| sub-mesh 1 header | `idxOff 0x2B00`, 956 indices, `vtxOff 0x60`, 341 vertices, `slotOff 0x20`, 2 slots, 8 zero bytes after the index stream |
| sub-mesh 1 slots | both unnamed; slot 0 covers indices 0 to 955 with colour (126, 126, 126, 127); slot 1 has 0 indices and colour 0 |
| sub-mesh 1 strips | 174, of 3 to 34 indices; highest vertex index 340 |
| sub-mesh 1 vertices | x −0.1167 to 1.1167, z −1.1167 to 0.1167, y 0, w 1; colour RGB 127 with alpha 0, 11, 58, 90 or 127 |

The tile sizes match the textures: the two upper tiles are square and 1024 × 1024, the two lower
tiles are a quarter as tall and 1024 × 256.

[`world-map-mesh-mg-mg-rows.tsv`](world-map-mesh-mg-mg-rows.tsv) lists both copies with size, SHA-256 and
the locale ids that load each, then every field of each copy in file order: the directory, both sub-mesh
headers, the six slots, the 16 tile vertices, the 341 strip vertices, both index streams, the 174 strips and
the tail, each with the function that reads it and what it shows.

- Tiles 0 to 3 are the four quarters of the Ivalice picture, textured `w_main0` to `w_main3`. Sub-mesh 1 is
  the shading laid over the World Map with `w_shade_p`, and the license board draws the same strips black.
  Locale ids 7, 8 and 11 read the `ch` copy, the others the `in` copy.
- The 174 strips run back to back over entries 0 to 955 of sub-mesh 1's index stream, and together they use
  all 341 of its vertices. No index reaches past the vertex array, so no field is out of range.
- Never read: sub-mesh 0's index stream, which gives each tile as `0x8000 + 4k + 2`, `4k`, `4k + 1`, `4k +
  3`, while `0x005556A0` takes vertices `4k` to `4k + 3` and emits them 3, 0, 1, 2. `0x00555D10`, the only
  reader of index runs, is reached only through `0x00555400`, which `0x00562F40` and `0x0055A8A0` call with
  sub-mesh 1.
- Also never read: the `indexStart` and `indexCount` of sub-mesh 0's slots, both directory sizes, both
  `idxCount` fields and the 8 zero bytes after sub-mesh 1's index stream. Slot 1 of sub-mesh 1 holds 0
  entries, so `0x00555D10` reads nothing for it and it draws nothing.

## Loader behaviour

### Request

`0x00562F90(meshObject, group)` requests kind 7 id `0xA8` through `0x00249210` (`0x00562FB6`) and stores the
returned buffer pointer at `meshObject + 0x10` (`0x00562FDA`). `0x00249210` claims a request slot, takes the
size from the file-size table (`0x0032E400`), allocates a buffer of that size and queues one read of the
whole file.

The buffer comes from arena 3, bottom-up (`0x00562FC2`, `0x00562FB2`). `0x00562F90` sets no completion on this request,
so the record keeps the zero `0x00249210` stores at `+0x10` and `0x002495C0` only counts it on the group. A size
below 1 queues no read and leaves the buffer null, which is then what `+0x10` gets ([Menu resource
packages](mrp-menu-resource-packages.md)).

The loader then walks the eleven `{name, flag}` entries at `0x00D231C0`:

- entries 0 to 7 (`w_shade_p`, `w_main0` to `w_main3`, `w_icon_p`, `w_line01`, `w_line02`) become named
  images requested as kind 7 id `0xAA + i` through `0x002493D0` (`0x0056301F`, the flag 1 for `w_main0` to
  `w_main3` and 2 for the others), stored at `meshObject + 0x20 + 8 × i`;
- entries 8 and 9 (`w_win_c`, `map_gra_c`) are skipped;
- entry 10, `baseicon`, is not requested: `+0x70` gets the registered image named by the pointer at `0x01E0C220`,
  `cursol_4_p`, through `0x0024A5A0` (`0x00562FEA`-`0x00562FF6`).

The eight images come from arena 2 (`0x0056301B`). It then requests `w_menu.mrp` (`0xA6`) into `+0x18`, also in
arena 2 through `0x00249350`, whose completion relocates it (`0x00563044`, `0x00563048`), and sets `+0x88` to −1.

MeshObject (World Map host + `0xC0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | sub-mesh 0 | set by the binder |
| `+0x08` | `void*` | sub-mesh 1 | set by the binder |
| `+0x10` | `void*` |  | file buffer |
| `+0x18` | `void*` |  | w_menu.mrp request |
| `+0x20` | `void*` | w_shade_p | image entry |
| `+0x28-0x40` | `...` |  | w_main0..w_main3 image entries |
| `+0x48` | `...` | w_icon_p | image entry |
| `+0x50` | `...` | w_line01 | image entry |
| `+0x58` | `...` | w_line02 | image entry |
| `+0x70` | `void*` | cursol_4_p | image entry |
| `+0x78` | `void*` | w_line01 | image entry, looked up by the binder |

### Binding textures

The World Map host's procedure `0x00552250` calls `0x00563110` in its message `0x10` case (`0x00552362`), the
message `0x002495C0` posts to a request group's widget once all of its requests have completed, or `0x00249410`
posts when they have all completed before the group is closed (`0x00249434`).

`0x00563110` stores both sub-mesh pointers (`0x00274780` with 0 and 1), then, for every slot of each sub-mesh,
compares the slot name byte for byte with the six names at `0x00D23270`: `main0.psd` to `main3.psd`,
`upper` and `linetex`. On the first match it looks up the paired image name (`w_main0` to `w_main3`,
`w_shade_p`, `w_line01`) with `0x0024A5A0`, which searches the 64 named-image entries at `0x0208F580` (stride
`0x48`, in-use bit `0x20` at `+0x38`) and returns the entry or 0.

It writes that pointer over the slot's
first eight bytes (`0x005631CA`), 0 when the image is not registered. A slot whose name matches nothing keeps its
name bytes. A pair without an image name would be passed over (`0x005631C3`); all six have one.

After both sub-meshes it looks up `w_line01` again into `+0x78` (`0x0056325F`-`0x00563273`), zeroes the eight bytes at
`+0x94` and sets the floats `+0x8C` and `+0x90` to 1.0 (`0x00563277`-`0x0056328C`).

### Drawing the tiles (sub-mesh 0)

On its draw message (4), `0x00552250` calls `0x00562F30` (`0x005527D2`), which passes sub-mesh 0 to `0x005556A0`.
That function builds a matrix with `0x00555A70` (scale half of `[0x01F2CAC0]`, a quarter turn about x by
`0x00202E90`, a translation from the scroll position) and copies the whole vertex array, `vtxCount` entries,
into its packet behind it.

The packet is a VIF chunk in the GS command buffer: an UNPACK header for the block (`0x00271100`, `0x6C008000`: V4-32,
two 16-byte quads per vertex, the count in the bits from `0x10000` up), the block of `vtxCount`, the matrix and the vertices, then
FLUSHE and MSCAL `0x2E95` (`0x005557B9`-`0x005557DD`).

Nothing on this port decodes that buffer
([graphics thread handshake](../Graphics/graphics-thread-handshake.md)); the tiles reach the screen
through the [sprite batcher](../Graphics/sprite-batcher.md), whose `0x00181350` takes the 0x30-byte
vertices the path builds on its stack (`0x005558E0`-`0x00555957`): the position with z forced to 0, the colour, `s x width`
and `t x height`. It draws one four-vertex primitive per slot:

- Slot `k` uses vertices `4k` to `4k + 3`, read in order from `vtxOff`; the path ignores the slot's index run
  and the index stream.
- When the slot's first qword is non-zero, it is taken as the image entry: the texture header at
  `[entry + 0x20]` gives the width (`u16 +0x14`) and height (`u16 +0x16`), and `s × width`, `t × height`
  become the texel coordinates (`0x00555900`, `0x0055590B`). A zero qword draws the tile untextured.
- Each position (`+0x10`) is transformed by the matrix (`0x00202B70`, `0x005558EB`).
- The colour is the slot's R, G and B times the widget's brightness (`s16 +0x5A`), and its A times the
  widget's alpha (`s16 +0x58`), each `>> 7`.
- The vertices are emitted in the order 3, 0, 1, 2.

### Drawing the strip mesh (sub-mesh 1)

The World Map's child widget `0x005528C0`, created by `0x00552250`, calls `0x00562F40` (`0x005536B7`), which
calls `0x00555400(meshObject + 0x20 entry, sub-mesh 1, …)`: sub-mesh 1 with the `w_shade_p` image. 
`0x00555400` sets the view with `0x00555F80`, which writes the matrix to `0x02CA8F40` and the texture origin and
extent to `0x02CA8F80` to `0x02CA8F8C`, then calls `0x00555D10` for each slot (`0x0055567A`).

`0x00555D10(sub, slot, widget, image)` reads `indexCount` entries from `idxOff + 2 × indexStart`:

- An entry with bit `0x8000` set starts a strip: `0x00556240` re-emits the GS `PRIM` (`0x5C` textured or `0x4C`
  untextured triangle strip, or `0x0A` line strip when bit `0x1` of `0x01F2CAC8` is clear) and `0x00555B90`
  writes the slot's colour factors (`0x00555DEF`-`0x00555E24`). Textured means an image was passed (`0x00555D3B`).
- On that restart `0x00556240` writes, under one A+D tag, TEST_1 (`0x47`) = widget `+0x80`, ALPHA_1 (`0x42`) =
  widget `+0x78` and PRMODECONT (`0x1A`) = 1 before the `PRIM` (`0x00556284`-`0x00556319`).
- It then flushes the sprite batcher (`0x00181330`) and sets the batcher's mirror: TEST_1 from `+0x80` (`0x00181910`),
  ALPHA_1 from `+0x78` (`0x001816B0`) and entry 4 (`0x00181870`) (`0x0055632B`-`0x0055634A`).
- Every call of `0x00556240` opens a chunk (`0x00271450`, `0x002714A0`) and reserves `0x20` bytes at its cursor, whose
  address it returns (`0x0055634F`-`0x0055636E`). There `0x00555B90` writes a GIF tag (NLOOP from its second argument,
  0 at both calls, EOP, and the three PACKED registers ST, RGBAQ and XYZF2, `0x412`; `0x00555B96`-`0x00555BA6`), then
  the four factors.
- After 32 vertices without a restart, it opens a new packet chunk without a new `PRIM`, so the strip
  continues (`0x00555DB2`).
- The vertex is `vtxOff + 0x20 × (entry & 0x7FFF)`; nothing compares it with `vtxCount`. Its `0x20` bytes are
  copied into the packet (`0x00271290`, `0x00555E48`).
- Per channel `c` (R, G, B, A), `0x00555B90` stores `f[c] = ((widget[+0x94 + c] × slot[+0x18 + 2c]) >> 7) / 128`,
  the widget's colour bytes times the slot's `s16` colours (`0x00555BB7`-`0x00555CAA`); each vertex colour then
  becomes `(int)(vertex[c] × f[c])` (`0x00555E68`-`0x00555E9A` for R and G, the same for B and A).
- Both calls give `0x00555B90` a fourth argument of 1, which selects that path (`0x00555BAE`). It also stores the
  factors at `0x022D9230`, the same factors before the division by 128 at `0x022D9240`, and 1/128 four times at
  `0x022D9250` (`0x00555C49`-`0x00555CA3`).
- Its path for a fourth argument of 0 (`0x00555CB0`-`0x00555D01`), which neither call takes, stores integers: R, G
  and B times the widget's `s16 +0x5A`, A times its `s16 +0x58`, each `>> 7`.
- The position is transformed by the matrix at `0x02CA8F40` (`0x00202B70`, `0x00555E63`). Texture coordinates are not
  stored: the transformed x and y, less the origin at `0x02CA8F80`/`0x02CA8F84` and divided by the extent at
  `0x02CA8F88`/`0x02CA8F8C`, are the fractions of the image's width and height.
- Those fractions times the image's width and height, `u = (x - [0x02CA8F80]) / [0x02CA8F88] × w` and
  `v = (y - [0x02CA8F84]) / [0x02CA8F8C] × h` (`subss`, `divss`, `mulss`, `0x00555EB2`-`0x00555F0E`), are the texture
  coordinates of the vertex handed to the sprite batcher (`0x00181350`, `0x00555F17`). Here `w` and `h` are the
  `u16` `+0x14` and `+0x16` of the image's `+0x20` record, 0 with no image (`0x00555D4B`-`0x00555D59`).
- After the last entry `0x00555D10` flushes the batcher (`0x00181330`, `0x00555F53`); a slot of 0 entries does only that.

Sub-mesh 1's slot names do not matter to this path; the texture is the one the caller passes.

### The license board

`0x00561390` requests kind 7 id `0xA8` into its data's `+0x110` (`0x0056162B`) beside the board images
(`lic_bk`, `lic_8_c`, `lic_8_c2`, `lic_8_c3`), and installs the widget `0x0055A8A0` through `0x0055A810`
(`0x005614FC`) with mode 1. On draw, `0x0055A8A0` takes sub-mesh 1 with `0x00274780` (`0x0055A928`), sets the
widget colour to `0x80000000` (RGB 0, alpha `0x80`) and calls `0x00555400` with no image and a scale of
1.2 (`0x0055A967`): the same strip mesh, untextured and black.

`0x0055A810(owner, file, mode)` creates the `0xD8`-byte widget only while the owner's `+0xD8 + 8 × mode` is empty,
stores it there and attaches it to `[0x0208EA28]` (`0x0055A82C`-`0x0055A884`). On message 1 `0x0055A8A0` installs the
descriptor `0x00D22FE0` (`0x00247570`), keeps the owner at `+0xC0`, the file at `+0xC8` and the mode at `+0xD0`, and
with mode 1 sets its position to 0, 0, its size to `[0x01E0C1D8]` x `[0x01E0C1DC]` (512 x 448 in the executable) and
its draw priority to `0x72` (`0x0055A97E`-`0x0055A9DE`).

The draw (message 4) does its work only in mode 1 (`0x0055A90B`-`0x0055A916`): sub-mesh 1 comes from the file at
`+0xC8`, `0x00555A10` runs first (`0x0055A930`), and the colour goes to the draw record's `+0x90` (widget `+0x38`,
`0x0055A95D`). Message 18 clears the owner's `+0xD8 + 8 × mode` (`0x0055A8E1`-`0x0055A8F1`); every other message goes
to `0x005C5230` (`0x0055A8DC`).

### What the load checks

Nothing in the file is validated:

- `0x00274780` takes each directory offset as stored and reads no size (`0x00274783`).
- The binder's one test is the slot name against the six names at `0x00D23270`; a slot that matches no name keeps its
  name bytes where the image pointer goes ([binding textures](#binding-textures)).
- No vertex index is compared with `vtxCount`.

## Modding notes

- Only the two directory offsets are read; the size fields, `idxCount`, the header padding and
  sub-mesh 0's index stream can hold anything.
- Every named slot in sub-mesh 0 must carry one of `main0.psd`, `main1.psd`, `main2.psd`, `main3.psd`,
  `upper` or `linetex`, or have all-zero name bytes (drawn untextured). Any other name stays in place of
  the image pointer, and the tile path reads through it.
- A tile's texture follows its slot name, not its position. Slot `k` always uses vertices `4k` to
  `4k + 3`, so sub-mesh 0 needs four vertices per slot.
- Sub-mesh 0's `s` and `t` are fractions of the texture size, so a replacement `w_mainN.tm2` of another
  size keeps the same mapping.
- Each slot run in sub-mesh 1 must start with an index that has bit `0x8000` set: the path creates its first
  packet only on a restart, and a run that starts without one reads through a null pointer.
- Vertex indices are the bits under mask `0x7FFF`, and nothing compares them with `vtxCount`; keep them inside the array.
- Sub-mesh 1 cannot carry texture coordinates; its texture is spread over the view by screen position.
- The file is read whole into a buffer of the size the file-size table gives for kind 7 id `0xA8`; a
  file of another size needs that entry changed in every language's table.
- KR, CH and CN load the `ch` copy and the other languages the `in` copy; change both.

## Related

- [Map screens](../Menus-And-HUD/map-screens.md): the World Map host and the screens around it.
- [License board screen](../Menus-And-HUD/license-board-screen.md): the board screen that draws sub-mesh 1.
- [File size tables (.fst)](file-size-tables-fst.md): the sizes that bound the read.
- [File requests and the read queue](file-requests-and-the-read-queue.md): `0x00249210` and the kind 7 reads.
- [File path resolution](file-path-resolution.md): how a kind 7 path becomes an archive entry.
