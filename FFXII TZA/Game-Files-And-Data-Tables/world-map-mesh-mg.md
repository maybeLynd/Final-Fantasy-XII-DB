---
title: "World map mesh (.mg): the world-map geometry file, its layout and how the map screen loads and draws it"
kind: "format"
category: "Game files and data tables"
addresses: "00562F90, 00563110, 00274780, 00555A50, 005556A0, 00555400, 00555D10, 00556240, 00555B90, 00555F80, 00552250, 005528C0, 00550540, 00561390, 0055A8A0, 00D231C0, 00D23270, 0024A5A0, 00249210, 002493D0, 002DF9A0, 02CA8F38, 02CA8F40"
---

## What the player sees

The main menu's World Map shows Ivalice as one large picture. That picture is four textures laid side
by side on flat tiles, and the tiles come from this file. The same file also holds a second, finer mesh
that the World Map draws with a soft shading texture, and that the license board screen draws again
without a texture.

## Where it comes from

The file is `ps2data/image/ff12/myoshiok/<tree>/worldmap/meshdata.mg` in the archive, and it is kind 7,
id `0xA8` in the path arrays that `ResourcePath_Init` (`002DF9A0`) installs. The KR, CH and CN arrays
(`01E0E530`, `01E5A3D0`, `01EABBA0`) name the `ch` copy; the arrays of the other languages (one each
for languages 1 to 6, and `01EDD7E0` for the rest) name the `in` copy.

Two screens request it. The World Map set-up `00550540` calls `00562F90` on the World Map host
`02CA8F38` (object `+0xC0`), and the license board screen `00561390` requests it again for its own use
(`0056162B`).

## Layouts

All offsets are little-endian. The file starts with a directory of two `{offset, size}` pairs:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | sub0Offset | offset of sub-mesh 0 from the file start |
| `+0x04` | `u32` | sub0Size | not read |
| `+0x08` | `u32` | sub1Offset | offset of sub-mesh 1 from the file start |
| `+0x0C` | `u32` | sub1Size | not read |

`00274780(buffer, i)` returns `buffer + u32[buffer + 8 × i]` (`00274783`, `00274786`); it is the only
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

`00555A50(sub, i)` returns `sub + s32[sub + 0x10] + 0x20 × i`. A slot is:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[16]` | name | NUL-padded; the binder overwrites +`0x00`..+`0x07` with an image-entry pointer |
| `+0x10` | `i32` | indexStart | first index-stream entry of the slot's run (sub-mesh 1 path) |
| `+0x14` | `i32` | indexCount | entries in the run (sub-mesh 1 path) |
| `+0x18` | `i16[4]` | colour | R, G, B, A; `0x80` = 1.0 |

A sub-mesh 0 vertex and a sub-mesh 1 vertex share the size but not the first half:

Sub-mesh 0 (tiles):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | s | fraction of the bound texture's width |
| `+0x04` | `f32` | t | fraction of the bound texture's height |
| `+0x08` | `f32[2]` | - | 1.0 in every shipped vertex; not read by the draw path |
| `+0x10` | `f32[4]` | x, y, z, w | position |

Sub-mesh 1 (strips):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32[4]` | colour | R, G, B, A |
| `+0x10` | `f32[4]` | x, y, z, w | position |

An index entry is a `u16`: bit 15 (`0x8000`) starts a new strip, and bits 0 to 14 are the vertex index.

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

## Loader behaviour

### Request

`00562F90(meshObject, group)` requests kind 7 id `0xA8` through `00249210` (`00562FB6`) and stores the
returned buffer pointer at `meshObject + 0x10` (`00562FDA`). `00249210` claims a request slot, takes the
size from the file-size table (`0032E400`), allocates a buffer of that size and queues one read of the
whole file.

The loader then walks the eleven `{name, flag}` entries at `00D231C0`:

- entries 0 to 7 (`w_shade_p`, `w_main0` to `w_main3`, `w_icon_p`, `w_line01`, `w_line02`) become named
  images requested as kind 7 id `0xAA + i` through `002493D0` (`0056301F`, the flag 1 for `w_main0` to
  `w_main3` and 2 for the others), stored at `meshObject + 0x20 + 8 × i`;
- entries 8 and 9 (`w_win_c`, `map_gra_c`) are skipped;
- entry 10 is replaced: `+0x70` gets the registered image `cursol_4_p` (`0024A5A0`).

It then requests `w_menu.mrp` (`0xA6`) into `+0x18` and sets `+0x88` to −1.

MeshObject (World Map host + `0xC0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | sub-mesh 0 | set by the binder |
| `+0x08` | `void*` | sub-mesh 1 | set by the binder |
| `+0x10` | `void*` | file buffer |  |
| `+0x18` | `void*` | w_menu.mrp request |  |
| `+0x20` | `void*` | w_shade_p image entry; +0x28..+0x40 w_main0..w_main3; +0x48 w_icon_p, +0x50 w_line01, +0x58 w_line02 |  |
| `+0x70` | `void*` | cursol_4_p image entry |  |
| `+0x78` | `void*` | w_line01 image entry, looked up by the binder |  |

### Binding textures

The World Map host's procedure `00552250` calls `00563110` in its message `0x10` case (`00552362`), the
message `002495C0` posts to a request group's widget once all of its requests have completed.

`00563110` stores both sub-mesh pointers (`00274780` with 0 and 1), then, for every slot of each sub-mesh,
compares the slot name byte for byte with the six names at `00D23270`: `main0.psd` to `main3.psd`,
`upper` and `linetex`. On the first match it looks up the paired image name (`w_main0` to `w_main3`,
`w_shade_p`, `w_line01`) with `0024A5A0`, which searches the 64 named-image entries at `0208F580` (stride
`0x48`, in-use bit `0x20` at `+0x38`) and returns the entry or 0.

It writes that pointer over the slot's
first eight bytes (`005631CA`). A slot whose name matches nothing keeps its name bytes.

### Drawing the tiles (sub-mesh 0)

On its draw message (4), `00552250` calls `00562F30` (`005527D2`), which passes sub-mesh 0 to `005556A0`.
That function builds a matrix with `00555A70` (scale half of `[01F2CAC0]`, a quarter turn about x by
`00202E90`, a translation from the scroll position) and copies the whole vertex array, `vtxCount` entries,
into its packet behind it. It then draws one four-vertex primitive per slot:

- Slot `k` uses vertices `4k` to `4k + 3`, read in order from `vtxOff`; the path ignores the slot's index run
  and the index stream.
- When the slot's first qword is non-zero, it is taken as the image entry: the texture header at
  `[entry + 0x20]` gives the width (`u16 +0x14`) and height (`u16 +0x16`), and `s × width`, `t × height`
  become the texel coordinates (`00555900`, `0055590B`). A zero qword draws the tile untextured.
- Each position (`+0x10`) is transformed by the matrix (`00202B70`, `005558EB`).
- The colour is the slot's R, G and B times the widget's brightness (`s16 +0x5A`), and its A times the
  widget's alpha (`s16 +0x58`), each `>> 7`.
- The vertices are emitted in the order 3, 0, 1, 2.

### Drawing the strip mesh (sub-mesh 1)

The World Map's child widget `005528C0`, created by `00552250`, calls `00562F40` (`005536B7`), which
calls `00555400(meshObject + 0x20 entry, sub-mesh 1, …)`: sub-mesh 1 with the `w_shade_p` image. 
`00555400` sets the view with `00555F80`, which writes the matrix to `02CA8F40` and the texture origin and
extent to `02CA8F80` to `02CA8F8C`, then calls `00555D10` for each slot (`0055567A`).

`00555D10(sub, slot, widget, image)` reads `indexCount` entries from `idxOff + 2 × indexStart`:

- An entry with bit 15 set starts a strip: `00556240` re-emits the GS `PRIM` (`0x5C` textured or `0x4C`
  untextured triangle strip, or `0x0A` line strip when bit 0 of `01F2CAC8` is clear) and `00555B90`
  writes the slot's colour factors.
- After 32 vertices without a restart, it opens a new packet chunk without a new `PRIM`, so the strip
  continues (`00555DB2`).
- The vertex is `vtxOff + 0x20 × (entry & 0x7FFF)`; nothing compares it with `vtxCount`.
- Per channel `c` (R, G, B, A), `00555B90` stores `f[c] = ((widget[+0x94 + c] × slot[+0x18 + 2c]) >> 7) / 128`,
  the widget's colour bytes times the slot's `s16` colours (`00555BB7`-`00555CAA`); each vertex colour then
  becomes `(int)(vertex[c] × f[c])` (`00555E68`-`00555E9A` for R and G, the same for B and A).
- The position is transformed by the matrix at `02CA8F40`. Texture coordinates are not stored: the
  transformed x and y, less the origin at `02CA8F80`/`02CA8F84` and divided by the extent at
  `02CA8F88`/`02CA8F8C`, are the fractions of the image's width and height.

Sub-mesh 1's slot names do not matter to this path; the texture is the one the caller passes.

### The license board

`00561390` requests kind 7 id `0xA8` into its data's `+0x110` (`0056162B`) beside the board images
(`lic_bk`, `lic_8_c`, `lic_8_c2`, `lic_8_c3`), and installs the widget `0055A8A0` through `0055A810`
(`005614FC`) with mode 1. On draw, `0055A8A0` takes sub-mesh 1 with `00274780` (`0055A928`), sets the
widget colour to `0x80000000` (RGB 0, alpha `0x80`) and calls `00555400` with no image and a scale of
1.2 (`0055A967`): the same strip mesh, untextured and black.

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
- Each slot run in sub-mesh 1 must start with an index that has bit 15 set: the path creates its first
  packet only on a restart, and a run that starts without one reads through a null pointer.
- Vertex indices are bits 0 to 14, and nothing compares them with `vtxCount`; keep them inside the array.
- Sub-mesh 1 cannot carry texture coordinates; its texture is spread over the view by screen position.
- The file is read whole into a buffer of the size the file-size table gives for kind 7 id `0xA8`; a
  file of another size needs that entry changed in every language's table.
- KR, CH and CN load the `ch` copy and the other languages the `in` copy; change both.

## Related

- [Map screens](../Menus-And-HUD/map-screens.md): the World Map host and the screens around it.
- [License board screen](../Menus-And-HUD/license-board-screen.md): the board screen that draws sub-mesh 1.
- [File size tables (.fst)](file-size-tables-fst.md): the sizes that bound the read.
- [File requests and the read queue](file-requests-and-the-read-queue.md): `00249210` and the kind 7 reads.
- [File path resolution](file-path-resolution.md): how a kind 7 path becomes an archive entry.
