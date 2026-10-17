---
title: "Effect element types: the handlers of every element type, what the verified types draw or change, and the kind-0x54 mesh record"
kind: "system"
category: "Graphics"
addresses: "002F2D60, 002F2530, 00500470, 00442550, 0039C550, 004427D0, 0039C4C0, 0039D890, 0039D970, 0039D5A0, 0039D6C0, 01EFAC20, 02AEE900, 02AEE908, 004490D0, 00501A50, 00502280, 00502EA0, 004434D0, 00444340, 00449AB0, 004355D0, 00377190, 02ADBFE0, 00377230, 004640A0, 003AB960, 0047BE20, 003D7FF0, 00465690, 00465CD0, 003D92C0, 02092628, 00436D00, 003AA280"
---

## What the player sees

Each piece of an effect has a type that decides what it is: a dot of light, a streak, an animated
sprite, a textured ring or dome, a model mesh, a trail of sprites, or something that draws nothing
itself but changes the scene, such as a light on the characters or a colour change on chosen
characters. The type is authored in the effect file, one byte per element definition.

## How it works

### Where the type comes from

An element definition is an `0xA00` record; its header byte `+0x0E` is the type, copied to the
definition's `+0x44` by `003A9A70` and to the element's byte `+0` at birth by `002F2D60`
(`002F30F2`–`002F30F6`). How the five method tables dispatch on it, and when each method runs, is on
[effect element runtime](effect-element-runtime.md); the record grammar is on
[effect files](effect-files-efx-efb.md).

The tables give 65 types an arm, with 248 distinct handlers. Types `0x00`–`0x0A`, `0x40`, `0x41`,
`0x60`–`0x67`, `0x80`–`0x97`, `0xA0`–`0xA2`, `0xA5`, `0xD0` and `0xD1`, except `0x09`, `0x63`, `0x64`
and `0x93`, are main-range types (47);
`0x42`, `0x68`–`0x6B`, `0x70`–`0x74`, `0xA3`, `0xA4` and `0xA6`–`0xAB` are reached only through the
sub-range tables (18); `0x6C`–`0x6F` have no arm in either range (`0043EBF0`, byte map `0043ECC4`). The
full decode is in `effect-element-types-effect-type-methods.tsv`.

Every birth method except `0x70`'s calls the base birth `002F2D60`, and every update method except
`0x70`'s calls the base update `002F2530`. Most updates add a type tail: type 1's `004424E0` is
`002F2530` then `00442600`. Types `0x41` and `0xD0` share `00464F10`, a jump to the base alone. The
tails end in the cull, release and spawn fork of the runtime page. The base setup is `00500470`.

In the tables below "Authored" is the number of `0xA00` definitions of the type over every shipped
stream, then the number of archive files holding them; a sub-range type's handlers are its
sub-range ones.

### The type names

`002FBA60(type)` returns the name of a type from a byte table at `002FBDEC` and a list of strings
from `00D0F9F0`; any other type below 256, and any type above, gives `"NONE TYPE NAME"` (`00D10150`).
The type-1 context builder `002FC4A0` prints these names for the element types of the stream it has
parsed while `022BE950` is set. The prefix is `TsElementType_` unless the row says `Nh`:

| Types | Names |
|---|---|
| `0x00`–`0x08` | NONE, POINT, SPRITE, LINE, CIRCLE, MODEL, COLUMN, SPHERE, BOARD1 |
| `0x0A` | TAIL |
| `0x40`–`0x42` | LIGHT, OBJFOG, CAMERAVIBRATION |
| `0x60`–`0x67` | VTHUNDER, VTHUNDER2, VTHUNDER3, VLASER, VLASER2, VTEXTHUNDER, VTEXTHUNDER2, VAFTERWIND |
| `0x68`–`0x6B` (`Nh`) | VTEXLASER, VEFFAFTERGLOW, VEFFWATER, VAFTERWIND_MULTEX |
| `0x70`–`0x74` (`Nh`) | VEFFMETABALL, VAFTERTHUNDER, VPHYSICALEFFECT1, GLASSBREAK, MODELBREAK |
| `0x80`–`0x8B` | VLINE1, VBEZIER1, VLCYLINDER1, VLCYLINDER2, VGLOBULARANM, VTAIL, VCLROTLINE, VGLROTLINE, VGLROTANM, VCLROTANM, VGLANM2, VCCFITANM |
| `0x8C`–`0x97` | VMODEL02, VMODEL00, VMODEL01, VMODEL03, VMODEL04, VMODEL05, VMODEL06, VMODEL07, VMODEL08, VMODEL09, VGLANM3, VMODEL10 |
| `0xA0`–`0xA2` | 2DSTART, VLENSFLARE, 2DTEX |
| `0xA3`, `0xA4` (`Nh`) | VRAIN2, LOCATIONTITLE |
| `0xA5` | 2DTEX2 |
| `0xA6`–`0xAB` (`Nh`) | 2DTEX2, 2DLINEBLUR, 2DTEX3, 2DCIRCLEPOLY, 2DLINEBLUR2, 2DTEXPOLYREQU |
| `0xD0`, `0xD1` | EXTCTRL, PCAMERA |
| `0xF0`, `0xF1` | PADVIBRATION, SOUND |
| `0xFF` | INVALID |

Type `0xA1`, VLENSFLARE, drives the eight lens-flare slots at `02ADBB40`.

### Types 0x00 to 0x0A

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x00` | `002F2D60` | `002F2530` | - | `00500470` | - | 1,446 / 458 |
| `0x01` | `00442520` | `004424E0` | `00442550` | `00538A60` | - | 476 / 370 |
| `0x02` | `00448DE0` | `00448D70` | `004490D0` | `00538AB0` | - | 7,523 / 1,141 |
| `0x03` | `004427A0` | `00442760` | `004427D0` | `00538B80` | - | none |
| `0x04` | `00445310` | `004452D0` | `004453D0` | `00538C80` | - | 173 / 81 |
| `0x05` | `00449970` | `00449930` | `00449AB0` | `00538DB0` | - | 5,204 / 1,115 |
| `0x06` | `00446F60` | `00446F20` | `00447020` | `00538EB0` | - | 25 / 9 |
| `0x07` | `00447E10` | `00447DD0` | `00447ED0` | `00538EB0` | - | none |
| `0x08` | `0044A5F0` | `0044A5B0` | `0044A620` | `00539030` | - | none |
| `0x0A` | `0044BA80` | `0044BA40` | `0044BAC0` | `00539170` | - | 40 / 39 |

- `0x00` has no draw method: it moves and fires spawn slots only.
- `0x01` is a point. Its draw sets `02AEE908` to the integer track at definition `+0x30` and
  `02AEE900` to definition byte `+0x49 >> 5`, then calls `0039C550` (`004425B2`–`004425E8`), which
  projects the point and emits a one-vertex `GiPrim` (kind 0 in the blended emitter, `0039DA7A`).
- `0x03` is a line: its draw calls `0039C4C0` (`004427D0`), which projects both ends, drops the line
  when either end is rejected, and emits a two-vertex `GiPrim` of kind 1 (`0039C4EB`–`0039C52B`,
  `0039D769`, `0039D83C`).
- `0x02` and `0x0A` draw sprite frames through `00501A50` and `00502280` (`004490D0`, `0044BAC0`).
  Both frame drawers pick a row of a kind-`0x50` record with `00502EA0`.
- `0x04`, `0x06` and `0x07` share the grid emitters `004434D0` and `00444340`, which all three draws
  call.
- `0x05` draws a mesh; see "Type 0x05 and the mesh record" below.
- `0x06` and `0x07` share one setup, `00538EB0`.

### The point and line blend modes

`02AEE900`, definition byte `+0x49` bits 5–7, picks the emitter. Mode 0 builds the primitive and
submits it at once (`0039D890` for a point, `0039D5A0` for a line). Modes 1 to 7 append a draw-list
entry first and set the primitive's blend word: `01EFAC20[mode]`, or in mode 6 the `+0x30` track
value from `02AEE908` (`0039DA89`–`0039DAAC`, `0039D859`–`0039D875`).

| Mode | Blend word |
|---:|---|
| 0 | none: the immediate emitter |
| 1 | `0x48` |
| 2 | `0x42` |
| 3 | `0x44` |
| 4 | `0x49` |
| 5 | `0x46` |
| 6 | the `+0x30` track value |
| 7 | `4` |

### The polygon emitters

Every effect point, line and polygon reaches the renderer through a pair of emitters: one submits
its command at once (blend mode 0, through `0020E630(command, 2)`), the other files it on the draw
list first and sets the blend word as above (modes 1 to 7). The blended ones fill the `0x28`-byte
entry the same way: the smallest of the vertices' 24-bit depths as the key `+8`, the pass nibble
`02AEE910` in bits 28 to 31, and the flag word `+0x20` = `02AEF41C × 4` (`003A2C70`), plus `2` when
`0024E460` returns 1 or `02AEF418` is set (`0039DD60`, `0039EC30`).

Each emitter takes vertices that the translated vector routines have already projected into the GS
form and converts them back with `0039CDC0(points, out, n)`. It reads each vertex as two 16-bit
coordinates in sixteenths of a pixel and a 24-bit depth, clamps the depth to `[02AEEBA0]` ..
`[02AEEBA4]` (`0039CE70`, `0039CE78`), multiplies the vertex by the matrix `02AEEB20` (`00202B70`),
divides by w, and scales x by the 16:9 factor `0017FFD0` when `0024E640` returns 1. `0039CF10` does
the same for vertices that are already floats, without the depth clamp.

Most emitters fill a `GiPrim` (`008642A0`, which returns the command plus 8); the blended textured
quads use a `GiPolyGT4T` (`00864D10`) or a `GiSprite` (`008647C0`) instead.

| Shape | Immediate | Blended | Vertices | Kind | Command | Called from |
|---|---|---|---:|---:|---|---|
| point | `0039D890` | `0039D970` | 1 | 0 | `GiPrim` | `0039C550` |
| line | `0039D5A0` | `0039D6C0` | 2 | 1 | `GiPrim` | `0039C4C0` |
| triangle, vertex colours | `0039E6B0` | `0039E820` | 3 | 3 | `GiPrim` | `004355D0`, `00437130`, `00438860` |
| quad, vertex colours | `0039EA70` | `0039EC30` | 4 | 4 | `GiPrim` | the three above, `004434D0`, `00444340` |
| triangle, textured | `0039F2B0` | `0039F4B0` | 3 | 3 | `GiPrim` | `004355D0`, `00437130`, `00438860` |
| quad, textured | `0039F780` | `0039F9F0` | 4 | 4 | `GiPrim`; blended `GiPolyGT4T` | the five above |
| quad, one colour per row | `0039F140` | `0039EEF0` | 4 | 4 | `GiPrim` | `0039C770` |
| sprite | `0039DAD0` | `0039DD60` | 4 | 4 | `GiPrim` | `0039C5D0` |
| sprite, float path | `0039E420` | `0039E0C0` | 4 | 4 | `GiPrim` | `0039C6B0` |
| sprite, fixed UVs | `003A0870` | `003A0AA0` | 4 | 4 | `GiPrim`; blended `GiSprite` | `0039CCB0` |
| ribbon segment, colour pair | `003A0370` | `0039FD20` | 4 | 4 | `GiPrim`; blended `GiPolyGT4T` | `0039C800` |
| ribbon segment, colour lists | `003A05F0` | `003A0040` | 4 | 4 | `GiPrim`; blended `GiPolyGT4T` | `0039C800` |

"Kind" is the primitive number the `GiPrim` carries; its execute `00863D80` looks it up in the
eight-entry table `01F44D20` (0, 1, 6, 2, 3, 4, 6, 6) and passes the result to the device's draw
slot `+0x20`. The callers `004355D0`, `00437130` and `00438860` are the mesh composers of type
`0x05`, and `004434D0` and `00444340` the grid emitters of types `0x04`, `0x06` and `0x07`. Their
texture coordinates pass through `0039B840` or `0039B860`, both jumps to `0039B880`, which adds the
offset pair its fifth argument points at to each coordinate and multiplies it by the vertex's `q`.

`004355D0` returns 1 without composing anything for a kind-7 effect `0x200`–`0x23F` drawn while the pass id
is 0 (`0024E410`) while the debug console's "Enable VFX Display" row (`+0xAC0` of `[01F81428]`,
`001D50D0`) holds 2: `00180100` answers whether that row is not 2.

### The sprite and ribbon front ends

The sprite drawers `00501A50` and `00502280` (types `0x02` and `0x0A`) reach the quad emitters
through two front ends: while bit 6 of the request's byte `+0x46` is clear, bit 0 picks between
them (`00501A50`).

- `0039C5D0` asks `0024D330` first. For 1 it installs the matrix `02AEECB0` (`0039B550`), projects
  the four corners with `00399B80`, which returns non-zero when a corner falls outside, multiplies
  each texture coordinate by its corner's `q` (`0039B780`), and calls the sprite pair. For 0 it
  hands the call to `0039C6B0`, which projects with the float routine `0039A770` and uses the
  float-path pair.
- `0024D330` returns 0 only when the current context's byte `+0` is 3 and the effect ticket its
  word `+4` names (`02EBCD80`, `0x38` bytes a slot) has effect number `0x34` at `+0x30`. `003B33D0`
  checks the ticket id against the slot and returns that number, or −1 for a stale id.
- `0039CCB0` projects the corners one at a time (`00399B10`, which calls `00399600` per point and
  stops at the first rejected one) and passes the texture coordinates through unchanged.

Type `0x08`'s draw `0044A620` builds a grid of (`+0x270` + 1) × (`+0x274` + 1) points. Untextured,
it draws each cell with `0039C770`, which projects two points from each of two rows with
`00399B10` and colours the quad with one RGBA word per row. Textured, it draws rows through
`00502160` → `0039C800`, the ribbon drawer, which walks a descriptor and draws one quad per
segment between two rails of points:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | first rail, 16-byte points; segment i uses points i and i+1 |  |
| `+0x10` | `void*` | second rail |  |
| `+0x18` | `void*` | two RGBA words (first rail, second rail); with +0x20, one word per segment for the first rail |  |
| `+0x20` | `void*` | one RGBA word per segment for the second rail, or null |  |
| `+0x28` | `void*` | 8-byte texture coordinates per point of the first rail, or null for the rectangle below |  |
| `+0x30` | `void*` | the same for the second rail |  |
| `+0x38` | `f32[4]` | u0, v0, u1, v1 |  |
| `+0x48` | `f32` | added to every u after each segment |  |
| `+0x4C` | `f32` | added to every v after each segment |  |
| `+0x50` | `void*` | texture pair |  |
| `+0x58` | `i32` | segment count |  |
| `+0x5C` | `i32` | segments after which the rectangle starts again from +0x38 |  |

The ribbon drawer skips a segment when either rail's pair of points is rejected by `00399B80`
(`0039C800`).

Element orientations come from `00398480(angles, out, order)`, which builds a rotation matrix from
three angles in one of six axis orders; type `0x08` passes the definition byte `+0x48` as the order
(`0044A7E0`). Orders 1 to 3 multiply three single-axis rotations (`003985B0`, `00398910`,
`00398C50`) in different orders; orders 0, 4 and 5 are written out in `00398DD0`, `00398A90` and `00398730`, which take
sine and cosine from the 32,768-step sine table `01F004E0`, the cosine as the entry a quarter turn on.

The direction helpers `003A2440`, `003A2570` and `003A2690` build an orthonormal matrix whose row 0,
1 or 2 is the normalised direction, with the other rows from cross products with the given up
vector (`003A27C0`, `00398390`), and write the derived up vector back.

### Sprite rows: 00502EA0

`00502EA0(record, index, mode)` returns the index-th row, among the rows of `0x90` bytes from
record `+0x10` whose byte `+0x70` has bit 0 set. Mode 0 first clamps the index to `[+0x3C] − 1`,
mode 1 takes it modulo `[+0x3C]`, mode 2 accepts it up to the row count `+0x38`, and any other mode
returns 0; no match returns 0 (`00502EA0`–`00502F21`).

### Sprite row helpers

A row names its texture and palette in three bytes: `+0x71` indexes the kind-`0x50` record's
texture handles (`+0x28`, kind `0x52`), `+0x72` names the palette source, a kind-`0x53` handle from
`+0x30` when bit 7 is set and the texture itself otherwise, and `+0x73` picks the palette slot.

- `00502F30(record, n, first, count)` finds the `n`-th enabled row and returns its index and the
  number of rows up to the next enabled one; it fails for `n` above the row count `+0x38`.
- `005030F0(record, row, out)` copies the texture's 16-byte register pair (`+0x10`) and, for a
  texture of format 0 to 2 whose row has `+0x72` unlike `+0x71` or a non-zero `+0x73`, replaces
  the high 27 bits of its second word with the palette's address word (`+0x2C + 8 × slot` of a kind-`0x53` record, or
  `+0x24 + 8 × slot` of the texture).
- `00503000(record, colours, count, handle)` returns the palette colours for the record's first
  row: 16 or 256 entries by the source's format, from the kind-`0x53` record's `+0x20` or the
  texture's `+0xB0`, with its handle.
- `00502160(record, draw)` is type `0x08`'s row walk: from the row the draw names, it sets each
  row's texture registers as `005030F0` does, switches to blend mode 6 with the row's word `+0x68`
  when the draw's byte `+0x60` has bits 1–3 equal to `0xC`, and calls `0039C800`, until a row with
  `+0x70` bit 1 or a following row whose `+0x70` byte is non-zero.

### Draw-source blocks

Many types describe what they draw with `0xF0`-byte blocks inside their definition; type `0x04`'s
setup `00538C80` has four of them from `+0x2B0`. A setup prepares each with `00431770(block, base)`,
which rebases the track group at `+0x00` (`00430AF0`), the group at `+0x40` (`0042FCF0`) and the
offsets `+0x90`, `+0x94`, `+0xE0` and `+0xE4`, clears `+0xA9` unless `+0xAA` has bit 4 or 5, binds
the source records (`00431610`) and returns the address after the block. `00431610` binds by the
source kind `+0xA0`; a number of 0 leaves the handle at 0:

| `+0xA0` | Records bound (`003AA280`) |
|---:|---|
| 1 | the kind-`0x54` mesh numbered `+0xA1` into `+0xB0` |
| 2 | the kind-`0x52` texture `+0xA2` into `+0xB4`; the palette `+0xA3` into `+0xB8`, kind `0x53` when bit 7 is set (number in bits 0–6), else kind `0x52` |
| 3 | the kind-`0x50` sprite rows `+0xA5` into `+0xBC` and the kind-`0x51` frame sequence `+0xA6` into `+0xC0` |

The draws read the block back through `00431830`. For source kind 2 it returns the texture's
register word (`+0x10`) with the palette address of slot `+0xA4` in its high half; when the byte
`+0xD0` is set it instead derives a palette from the source palette with `00431B10(block + 0xD0,
…)`, 16 entries when the palette's byte `+0x10` is `0x80` and 256 otherwise, and puts that
palette's address there. For source kind 3
it steps the frame sequence (`005039A0`) and picks the row with `00502EA0`.

### Track values in other units

A track is 16 bytes: two key arrays (offsets `+0x00` and `+0x04`, counts `+0x0C` and `+0x0D`) of
8-byte keys whose value is at `+4`. `004314E0(track, frame)` reads it: 0 for an empty array, the one
key's value for a count of 1, `00431080` otherwise, and with both arrays the two results combined
by `00431350`.

A setup can rescale the stored values once. `00430A60(track, f)` multiplies every key value of
both arrays by `f`, `00431040(group, f)` does so for the three tracks of a group (`+0x00`, `+0x10`,
`+0x20`), and `00431580(track, n)` multiplies integer values by `n`. Type `0x03`'s setup `00538B80`
turns the group at `+0x80` from degrees to radians (`π/180`), divides the groups at `+0x100` and
`+0x140` by 100 and multiplies the integer track at `+0x180` by 100.

### Generated palettes

`00431B10(op, colours, n, frame, texture)` derives a palette from `n` source colours. It unpacks the
colours into the work area `02CA4EE0` (`003CD840`), reads the operation's track `op + 0x10` at
`frame` (`004314E0`), and runs the operation the kind byte `op + 0x00` names; any other kind
returns 0 and the source palette stays:

| Kind | Body | Fields it reads |
|---:|---|---|
| 1 | `0050AC20` | byte `+0x01`, bits 1–2 of `+0x03` |
| 2 | `00506B40` | words `+0x08` to `+0x0E`, bit 0 of `+0x03` |
| 3 | `005080A0` | words `+0x04`, `+0x06`, bit 0 of `+0x03` |
| 5 | `00509BB0` | none besides the track |
| 6 | `00507490` | words `+0x04`, `+0x06` |
| 7 | `00508C90` | bytes `+0x01`, `+0x02`, words `+0x04`, `+0x06` |

With bit 3 of `+0x03` set the operation gets `n − 1` and a flag instead of `n`. `003A9C10(work, n,
texture)` then
reserves room for the palette in the emulated GS memory (`002D81D0`, which can refuse), takes an
`n × 4 + 0x10`-byte block linked on the current record table's list `+0x10`, packs the colours into
it (`003D2B60`), writes them into the palette texture (`00183640`) and returns the GS address.

The draws of types `0x02`, `0x0A`, `0x84`, `0x85`, `0x88`, `0x89`, `0x8A`, `0x8B`, `0x96` and `0xA1`
call `00431B10` themselves; type `0x02`'s draw `004490D0` passes definition `+0x160` and the
palette of its first sprite row (`00503000`).

### Frame sequences: the kind-0x51 record

A kind-`0x51` record holds `+0x10` entries of 16 bytes at `+0x18`. An entry's byte `+8` is its
opcode: 0 shows a frame for byte `+9` ticks, 1 jumps to the entry in word `+0xC`, and 2 ends the
sequence. `005039A0(sequence, time, mode)` returns the frame entry at `time`; at the end, mode 0
keeps the last frame, mode 1 starts over with the time reduced, and mode 2 returns 0.
`00503A80(sequence, cursor)` does the same from a four-byte cursor (entry, time, last frame,
mode) that it updates, for type `0x02`'s draw `004490D0`.

The texture source resolver `00431830` uses `005039A0` with mode bit 6 of the sub-record's word
`+0xAA`, then picks the sprite row from the frame's word `+0xA` with `00502EA0` and its registers
with `005030F0`.

### The mesh and sprite triangle emitters

Four emitters turn projected triangles into `GiPrim` commands of kind 5; the mesh draw and the
sprite frame drawers `00501A50` and `00502280` use them.

| Emitter | Texture | Filing |
|---|---|---|
| `0043D8F0(positions, colours, n)` | none | at once, `0020E630(command, 2)` |
| `0043DB90(positions, uv, q, textures, colours, n)` | `u / q`, `v / q`; texture pair at `+0x38`, `+0x48` | at once |
| `0043E440(positions, colours, n)` | none | draw-list entry |
| `0043DF80(positions, uv, q, textures, colours, n)` | as `0043DB90` | draw-list entry |

The colour bytes become floats. The two list emitters key the entry on the smallest of the three
vertices' 24-bit depth words, OR in the pass nibble, and set the primitive's blend word to
`01EFAC20[02AEE900]`, or to `02AEE908` in mode 6, as the point emitter does
(`0043DFCF`–`0043E012`, `0043E3EC`–`0043E401`; `0043E48E`–`0043E4D0`, `0043E760`–`0043E775`).

### Type 0x05 and the mesh record

`00449AB0` draws one mesh. When definition byte `+0x590` has bit 4 clear, the mesh index `+0x294`
is the integer part of the float track at definition `+0x190`, or 0 when that is not positive or
not below 32 (`00449DA7`–`00449DF9`). It publishes the blend pair as the point does and passes the
handle `[definition + 0x5A0 + index × 4]`, decoded, to the model composer `004355D0`
(`0044A11C`–`0044A15B`). The handles are kind-`0x54` records.

### How the composer prepares a mesh

`004355D0(object, state)` draws nothing for an object without bits 0 and 2 of `+0x18C`. It
first builds the mesh's vertices into the scratch block `[02AEED50]`:

- `00434CD0` when the state's `+0x1E8` is set: it blends each array of the object with the same
  array of the object at state `+0x48`, weights `1 − t` and `t` with `t` the float `+0x1EC`; state
  byte `+0x1F1` bits 4, 5 and 6 copy the 4-byte, 8-byte and vector arrays unblended instead;
- `00435050` otherwise: it copies the arrays unblended.

Both call `00434C50(state, byte +0x1F1 & 7)`, which multiplies the state's matrix by `02AEEC30`
(mode 1), `02AEEC70` (mode 2) or `02AEEA60` (modes 4 and 5); mode 4 first turns the matrix toward
the point `02AEEAD0` from the position `+0x30` (`00434900`), and mode 5 turns it about one axis by
the `atan2` of the same direction (`00434A70`). Then they project the positions; a rejected mesh
draws nothing (`00399B80` at `00434ED9` and `0043526E`).

- With byte `+0x1F1` bit 3 and `0024E410` true, the projection is not tested and the first six
  (`00434CD0`) or four (`00435050`) projected vertices are overwritten with fixed screen values,
  one set for language ids 1–6 (`00229E40`) and another for the rest.
- Byte `+0x1F1` at `0x80` or above hands the mesh to `00438860`; bit 3 hands it to `00437130`.
  Otherwise `004355D0` runs its own loop over the `+0x1F0` layers.

`00437130` is the same per-layer loop without one step: for a layer of mode 4, `004355D0` divides
the first float of the layer's pair at state `+0x50 + 8 × layer` by 1.15 and multiplies the second
by 1.15 (`00435D23`–`00435D49`), and `00437130` does not. In both, a layer of mode 5 emits flat triangles and quads, mode 1 textured
ones whose texture comes from the face's byte at `+0x188`, and any other mode textured ones with
the layer's texture; blend mode 0 files at once and any other mode through the draw list.

The composers share two helpers with the element types at `004434D0`, `00444340`, `004584E0` and
`004595C0`: `00394DA0(matrix, vector, out)` multiplies the vector by the matrix without its
translation, giving four floats, and `00394B70(vertices, indices, out, n)` adds, for each of `n`
indices into the 16-byte projected vertices, the vertex's screen position `x / 16 / 512 − 3.5` and
`y / 16 / 512 − 3.5625` to the next float pair of `out`.

### Types 0x40 to 0x42

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x40` | `00463FF0` | `00463FB0` | `00464090` | `0053AAC0` | `00464050` | 2,254 / 744 |
| `0x41` | `00464B30` | `00464F10` | `00464BC0` | `0053AB10` | `00464B80` | 425 / 310 |
| `0x42` (sub) | `0047BE20` | `0047BDA0` | `0047BFA0` | `0050C450` | `0047BF70` | 613 / 350 |

These types, with `0xD0`, act on the scene instead of drawing. Their births register the element in
the 128-slot registry at `02ADBFE0` (`0x20` bytes a slot, handle `serial << 8 | slot`, element at
`+8`) through `00377190`, whose only callers are those four births. Their draw methods only set a
bit: `00464090` sets bit `0x2` of `+0x248`, `00464BC0` bit `0x1` of `+0x23C`.

The releases `00464050` (`0x40`), `00464B80` (`0x41`), `00465120` (`0xD0`) and `0047BF70` (`0x42`)
free the slot through `00377360(handle)`, which finds it in the registry's live list (head
`02ADBFC8`, tail `02ADBFD0`, links at `+0x10` and `+0x18`), lowers the count `02ADBFC0`, clears the
handle and unlinks it.

`00377230` walks the registry from `MainLoop_Draw` (`0022B268`) and the menu frame (`0022B940`),
checks visibility with the group gate and the per-instance gate (`00377292`–`003772A2`), and calls
the type's apply body: `004640A0` (`0x40`), `00464BD0` (`0x41`), `0047BD30` (`0x42`) and `00465690`
(`0xD0`) (`003772EA`–`00377336`).

- `0x40` makes a light. `004640A0` fills a request and creates it with `003AB960` the first time,
  keeping the handle at `+0x244`, and updates it with `003AC920` afterwards (`00464387`–`004643A0`).
  Definition byte `+0x120` picks the request word: 1 gives `0x8001`, 2 gives `0x8006`, anything else
  `0x8002` (`004640C3`–`0046410A`). The pool is on [character lighting](character-lighting-and-shadows.md).
- `0x41`'s apply keeps a record in the 64-entry pool of `0x60`-byte records at `[02B404E0]` through
  `003B4160`.
- `0x42`'s birth reads three floats at definition `+0x124`, `+0x128` and `+0x12C` and the track group
  at `+0x80`, and takes a slot in the 32-entry, `0x60`-byte pool at `02B4D7D0` through `003D7FF0`
  (`0047BE64`–`0047BF08`).

- The `0x42` pool slots are named by `serial << 8 | slot`, checked at slot `+0x04`. `003D8300(handle)`,
  from the release `0047BF70`, `003E69A0` and `003E7140`, frees a slot: it lowers the count
  `02B4D7A0`, clears the handle and unlinks the slot from the list `02B4D7A8` / `02B4D7B0` (encoded
  links at `+0x08` and `+0x0C`).
- `003D8D70(handle, b)` stores byte `+0x3F` and `003D8DE0(handle, v)` the three floats
  `+0x10`–`+0x18`; the birth, the update and `003E6910` call both. `003D8DA0(mode)`,
  from the field camera's target read `003D9E20`, stores 1.0 for mode 1, 0.6 for mode 2 and 0
  otherwise at `02B4D7B8`, which `003D83A0` and `003D8C30` read.

### Types 0x60 to 0x74

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x60` | `0045BF50` | `0045BF10` | `0045BFB0` | `0053A120` | - | 84 / 22 |
| `0x61` | `0045C920` | `0045C8E0` | `0045C980` | `0053A060` | - | 9 / 7 |
| `0x62` | `0045D290` | `0045D250` | `0045D2F0` | `0053A120` | - | 2 / 2 |
| `0x65` | `0045DCA0` | `0045DC60` | `0045DD10` | `0053A1E0` | - | 169 / 44 |
| `0x66` | `0045E8C0` | `0045E880` | `0045E930` | `0053A3B0` | - | 414 / 123 |
| `0x67` | `0045FD50` | `0045FD10` | `00460170` | `0053A5D0` | `00460120` | 364 / 207 |
| `0x68` (sub) | `00522AB0` | `00522A70` | `00522D80` | `0054EB40` | - | 162 / 83 |
| `0x69` (sub) | `00523C30` | `00523BF0` | `00523D30` | `0054ED10` | - | 58 / 22 |
| `0x6A` (sub) | `00525D50` | `00525D10` | `00526080` | `0054F070` | `00526040` | 395 / 210 |
| `0x6B` (sub) | `00529200` | `005291C0` | `005294F0` | `0054F7C0` | `005294B0` | 258 / 117 |
| `0x70` (sub) | `0053DD10` | `005C5230` | `0016D6A0` | `0054F270` | `0016D6A0` | none |
| `0x71` (sub) | `0052A130` | `0052A0F0` | `0052A360` | `0054F9B0` | `0052A340` | 28 / 12 |
| `0x72` (sub) | `0052ADF0` | `0052ADB0` | `0052B080` | `0054FBE0` | `0052B060` | 89 / 47 |
| `0x73` (sub) | `0052D3B0` | `0052D370` | `0052D920` | `0054FFF0` | `0052D8E0` | 14 / 8 |
| `0x74` (sub) | `0052E430` | `0052E3F0` | `0052EA90` | `00550200` | `0052EA50` | 4 / 3 |

- `0x60` and `0x62` share the setup `0053A120`.
- `0x70` does nothing at run time: its birth `0053DD10` returns 1, its update `005C5230` returns 0,
  and its draw and release are the bare `ret 0` at `0016D6A0`. Only its setup reads the record.
- `0x67`, `0x68`, `0x6A`, `0x6B`, `0x71`, `0x73` and `0x74` update on even frames only in the
  half-rate cadence (the base update's bit set `0x341B`, on the runtime page).
- `0x63`, `0x64` and `0x6C`–`0x6F` have no arm in any table.

### Sub-range draw packets

The sub-range draws build a PS2-style packet in the data arena instead of emitting primitives. Each
one asks a size function for the packet's length in quadwords, gives up when the cursor `02F8F2D0`
plus that length would reach the end `02F8F2D8`, lets a builder write the packet at the cursor and
return the new cursor, and hands the packet to a finaliser (`0052329D`–`0052335F` for type `0x68`).

| Type | Draw | Size | Builder | Templates copied (program) | Finaliser |
|---|---|---|---|---|---|
| `0x68` | `00522D80` | `00541DB0` | `00542100` | `02AEB610` (`004DF440`), `02AEB810` (`004E0F70`), `02AEB820` | `00540F40` |
| `0x69` | `00523D30` | `00543940` | `005439D0` | `02AEB0F0` (`004DCC00`), `02AEB290` (`004DDDF0`), `02AEB2A0` | `00540F40` |
| `0xA3` | `00524A50` | `00544590` | `00544A50` | `02AEA270` (`004DB350`) | `00540F40` |
| `0xA6` | `00524E30` | `00544CE0` | `00544D30` | `02AE9BC0` (`004DA8A0`), `02AE9D50` | `00540F40` |
| `0x6B` | `005294F0` | `00532E80` | `00533250`; `005325D0` with definition word `+0x866` bit `0x2000` | `02AECAC0` (`004E7D90`), `02AECAD0`, `02AECCC0`; `02AEBBB0` (`004E31E0`), `02AEBBC0`, `02AEBDB0` | `00540F40` |
| `0x6A` | `00526080` | `00545EF0` | `005466E0` | `02AE9130` (`004D7BF0`), `02AE9140`, `02AE9290` | `00540DB0` |
| `0xA8` | `005271D0` | `00547350` | `005473A0` | `02AE9BC0` (`004DA8A0`), `02AE9D50`, `02AE9EE0` | `00540F40` |
| `0xA9` | `00528150` | `005479B0` | `00547A00` | `02AE8CF0` (`00479650`), `02AE8D30` | `00540C20` |
| `0x71` | `0052A360` | `00547D80` | `005480E0` | `02AE8620` (`004D40E0`), `02AE87B0`, `02AE8830` | `00540F40` |
| `0x72` | `0052B080` | `0054A980` | `0054AA90` | `02AECD20` (`004D0FA0`), `02AECEB0`, `02AED130` | `00540F40` |
| `0xAB` | `0052C070` | `0054B3A0` | `0054B3E0` | `02AE9BC0` (`004DA8A0`), `02AE9D50`, `02AE9EE0`, `02AEC4B0` (`004CF490`) | `00540F40` |
| `0x73` | `0052D920` | `0054BD40` | `0054BE70` | `02AEBE10` (`004C8320`), `02AEC0A0`, `02AEC110` | `00540F40` |
| `0x74` | `0052EA90` | `0054D610` | `0054D740` | `02AEBE10` (`004C8320`), `02AEC0A0`, `02AEC110` | `00540DB0` |

The templates are the boot-time VIF objects of
[PS2 VIF1 / VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md); a builder copies
their quadwords into the packet and patches in the element's values, and a program in brackets is
the microprogram the template's header installs. `0xA6`, `0xA8` and `0xAB` share the templates of
`02AE9BC0` and `02AE9D50`, and `0x73` and `0x74` share all three of theirs.

- A size function adds a fixed head to a cost per enabled layer slot, the first enabled slot
  costing less: `00541DB0` returns 0 unless byte `+0x38` is set, then `0x230` bytes plus `0xB0` for
  the first and `0xC0` for each further of three slots (`+0x140`, stride `0x50`); `00544CE0`,
  `00547350` and `005479B0` count four slots from a `0x40`-byte head.
- `0054B3A0` never returns 0: its head is `0x4F0` bytes. `00543940` adds `0x190` bytes for each of
  four non-zero words at `+0x740`–`+0x830`; `00544590` adds one quadword per 20 entries to `0x130`.
- `00545EF0` (type `0x6A`) starts from `(+0x1C + 0x17) x 16` bytes and adds, per tile, `0x60` plus
  `w x h x 16` when bit 1 of `+0x64` is set. Tiles start every 21 grid points along `+0x10` and `+0x14`
  while the start is below the count minus 1, and `w = min(22, +0x10 - start)`, `h` likewise; it returns
  the total `>> 4` (`00545EF0`-`00545FAE`).
- `0054BD40` and `0054D610` add the two index blocks
  of every piece and, per enabled layer byte `+0xE0`–`+0xE3`, `0x60` bytes per piece.
- `00540F40(packet, chain, count, key)` computes the flag word, 2 when `0024E460` or `003A3D20`
  returns non-zero, ORed with `003A2C70()`, and passes everything to `00540DB0`, which appends the
  draw-list entry and copies the packet into a command (`00540F65`–`00540F96`).
- `00540C20(packet, chain, count, key)`, used by `0xA9` alone, appends an entry with the packet at
  `+0x00`, the key and pass nibble at `+0x08`, the chain count at `+0x0C` and a null function at
  `+0x10`, and builds no command (`00540C20`–`00540C6B`). `0xA9` sets `02AEF418` around the call
  when its key is `0xFFFE00` or more and `0024E2E0` returns 0 (`005287A6`–`005287C2`).
- The key is the projected depth of the element position for `0x68` and `0x69` (`00202B70` with
  `02AEEBB0`, then z / w); `0xA3` and `0xAB` use `0xFFFFFF` and the rest use 0.

### Type 0x6A: the ripple surface

Type `0x6A` simulates a height field with the damped two-dimensional wave equation. Its birth
`00525D50` copies the definition's time step, wave speed, grid spacing and damping (`+0x3D0`–`+0x3DC`)
and the grid's point counts (`+0x3F0`, `+0x3F4`) into the element block at `+0x230`, allocates
16 bytes per point, and then:

- `00545120` derives the three step coefficients `k1 = (4 − 8c²t²/d²) / (μt + 2)`,
  `k2 = (μt − 2) / (μt + 2)` and `k3 = (2c²t²/d²) / (μt + 2)` into block `+0x30`, `+0x34` and
  `+0x38`, the half extents `(n − 1)d / 2`, and the number of tiles the packet needs;
- `005450E0` zeroes the `n × m` points; `005263F0` then runs once per warm-up frame, the count from
  definition word `+0x3FC` (`00525FDA`–`0052601D`).

`005263F0` is the update tail. Definition byte `+0x3FF` bits 3, 1 and 2 enable three disturbances,
each a strength track (`+0x250`, `+0x260`, `+0x270`) and a position track (`+0x280`, `+0x2C0`,
`+0x300`) in grid units. A disturbance with a non-zero strength stamps the grid; it then runs the
step `00545650` as many times as the integer track `+0x3C0` gives, at most 5.

- `00545310(grid, x, y, h)` sets a 3 × 3 stamp: `h` at the point, `h / 2` at its four neighbours and
  `h / 4` at the corners; `00545490` adds the same stamp. Points within two of the edge are left alone.
- With bit `0x20` of `+0x3FF`, `00546DB0` and `00547060` stamp a line of points instead, each scaled
  by `(1 + cos φ) / 2` with the phase stepping along the line. Definition byte `+0x3F9` picks the
  adding forms.
- `00545650` updates every interior point from itself, its previous height and its four neighbours
  with `k1`, `k2` and `k3`.

### Types 0x73 and 0x74: the flying pieces

Types `0x73` and `0x74` break a mesh into pieces of `0xA0` bytes that fly and spin. `0x73`'s birth
`0052D3B0` copies the authored piece data (`+0x954` bytes from definition `+0x960`), allocates one
record per piece (count at `+0x968`) and randomises its ranges; `0054C6B0` then gives each piece a
start velocity and spin, the direction chosen by the low three bits of block byte `+0x4E`.

Each step, `0054C440` (`0x73`, from the update tail `0052E270`) and `0054DD30` (`0x74`, from
`0052F400`) walk the pieces. The second component `+0x24` of a piece's velocity `+0x20` loses
gravity, its position `+0x70` adds the velocity and its angles `+0x00` add the spin `+0x10`, each
scaled by one of two parameter sets chosen by the piece's time against the block's thresholds;
`0046D560` then rebuilds the piece's rotation at `+0x40`.

In `0054C440` the step is `v.y -= [+0xC0] x [+0x44] x s x k.y`, then per axis `pos += s x k x v` and
`angle += r x spin x q`. Set A is `s` = block `+0x58`, `k` = `+0x80`-`+0x88`, `r` = `+0x70`-`+0x78`,
`q` = `+0x5C`; set B is `+0x90`, `+0xB0`-`+0xB8`, `+0xA0`-`+0xA8` and `+0x94` (`0054C4AE`-`0054C67E`).

Set A applies when piece `+0x0C <= [+0xC4]` or piece `+0x98 <= [+0x3C]`. Otherwise set B applies, unless
piece `+0x0C > (1 - [+0xC4]) x [+0xFC] + [+0xC4]` and piece `+0x98 > (1 - [+0x3C]) x [+0x9C] + [+0x3C]`, which
leaves the piece unmoved that step.

- `0054C440` moves only a piece whose `+0x30` points to itself (`0054C4A4`).
- `0054DD30` rotates the velocity step by the matrix at block `+0x150` when bit 1 of `+0x9C` is set
  (`00202B90`).

### Births of the other sub-range types

- `0x68`'s birth `00522AB0` calls `00541E00`, which draws five random values `r0`-`r4` =
  `003D8E50(1.0) - 0.5` into `+0x00`-`+0x10` and, unless block byte `+0x39` bits 3 or 4 say otherwise,
  sets `+0xA0 = normalise(r0, r1, r2) x L1` and `+0xB0 = normalise(r3, r4, 003D8E50(1.0) - 0.5) x L2`
  (`00380800` normalises; `00541E12`-`00541FCF`).
  - `L1 = [+0xAC] + 003D8E50([+0x120])` and `L2 = [+0xBC] + 003D8E50([+0x124])`, written back to `+0xAC`
    and `+0xBC`.
- The same birth calls `00542060`, which draws six more in `[−0.5, 0.5)`.
- `0x69`'s birth `00523C30` calls `005439A0`, which clears block `+0x04` and `+0x14` and stores
  the float `1 / (count + 1)`, the count being block `+0x00`, at `+0x18`.
- `0x67`'s birth `0045FD50` and `0x6B`'s birth `00529200` call `00532EF0`, which fills each of
  the `+0xB0` strands (`0x440` bytes) with a base plus a random amount for every parameter and a
  direction from a random or stepped angle; `00532E80` sizes `0x6B`'s packet from the strand count
  and three enabled layers (`+0x88`–`+0x90`).
  - Each field is `base + 003D8E50(1.0) x range`, with the strand field, block base and block range:
    `+0x10`, `+0xC8`, `+0xCC`; `+0x14`, `+0xF8`, `+0xFC`; `+0x18`, `+0x100`, `+0x104`; `+0x424`, `+0xD8`,
    `+0xDC`; `+0x434`, `+0xC0`, `+0xC4`; `+0x438`, `+0xE8`, `+0xEC`; `+0x43C`, `+0xF0`, `+0xF4`
    (`00532EF0`-`00533242`).
  - `+0x08` takes `+0xE0`, `+0xE4` the same way when block `+0x140` bit 1 is set, else
    `(+0x14 + +0x18) x 0.5`; `+0x1C` is `003D8E50(1.0) x` block `+0x1C`.
  - The direction is `+0x420 = L sin a`, `+0x428 = L cos a`, `+0x42C = 1.0`, with `L` from `+0xD0`, `+0xD4`
    as above and `a = 003D8E50(6.284)` while block `+0x124` is 0, otherwise `+0x128` plus `+0x12C` for each
    strand before it.
- `0x71`'s birth `0052A130` calls `00547DD0`, which fills each of the `+0x140` records (`0x450`
  bytes) with a base plus a random amount for every parameter, and a direction from a random or
  stepped angle.
  - Each field is `base + 003D8E50(range)`, with the record field, block base and range: `+0x10`, `+0x158`,
    `+0x15C`; `+0x08`, `+0x188`, `+0x18C`; `+0x0C`, `+0x190`, `+0x194`; `+0x434`, `+0x168`, `+0x16C`;
    `+0x444`, `+0x150`, `+0x154`; `+0x448`, `+0x178`, `+0x17C`; `+0x44C`, `+0x180`, `+0x184`
    (`00547DD0`-`005480D7`).
  - `+0x04 = u16 +0x170 + 003A6E60(u16 +0x172)`; `+0x14`-`+0x1C` are each `003D8E50([+0x48])` and
    `+0x20`-`+0x28` each `003D8E50([+0x4C])`.
  - The direction is `+0x430 = L sin a`, `+0x438 = L cos a`, `+0x43C = 1.0`, with
    `L = +0x160 + 003D8E50(+0x164)` and `a = 003D8E50(6.284)` while block byte `+0x67` is 0, otherwise
    `+0x70` plus `+0x74` for each record before it.
- `0x72` keeps a sway chain (see [model oscillators](model-oscillators-and-pose-sequencer.md)).
  `0054B0E0`, called by its birth tail `0052BBD0` and its update tail `0052B5E0`, adds an offset to
  every node and sets the root; `0054A690(section, out, mode)`, called by `0052B5E0`, returns the
  root (mode 0) or walks the segment lengths `+0x38` to the chain's middle (mode 1) or tip (mode 2).

### Types 0x80 to 0x97

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x80` | `0044CC10` | `00450480` | `0044CC50` | `00539320` | - | 875 / 381 |
| `0x81` | `0044D460` | `0044D420` | `0044D4A0` | `00539270` | - | none |
| `0x82` | `0044CC10` | `00450480` | `0044DD00` | `00539320` | - | 617 / 161 |
| `0x83` | `0044CC10` | `00450480` | `0044E530` | `00539320` | - | 80 / 48 |
| `0x84` | `0044ED90` | `0044ED50` | `0044EDD0` | `00539980` | - | 1,972 / 501 |
| `0x85` | `0044F930` | `0044F8F0` | `0044F970` | `005393B0` | - | 78 / 42 |
| `0x86` | `004504C0` | `00450480` | `00450550` | `005394A0` | - | 115 / 87 |
| `0x87` | `00451140` | `00450480` | `00451180` | `00539560` | - | 175 / 54 |
| `0x88` | `00451890` | `00451850` | `004518D0` | `00539610` | - | 41 / 31 |
| `0x89` | `004524C0` | `00452480` | `00452540` | `00539740` | - | 36 / 8 |
| `0x8A` | `00453110` | `004530D0` | `00453150` | `00539870` | - | none |
| `0x8B` | `004548F0` | `004548B0` | `00454930` | `00539A60` | - | 1 / 1 |
| `0x8C` | `00455390` | `0045B260` | `00455540` | `00539B30` | - | 7,509 / 910 |
| `0x8D` | `00455D70` | `00455D30` | `00455DB0` | `00539C10` | - | 1,170 / 553 |
| `0x8E` | `004566E0` | `004566A0` | `00456720` | `00539CF0` | - | 136 / 74 |
| `0x8F` | `00457E10` | `00456EF0` | `00456F30` | `00539DA0` | - | 1,663 / 383 |
| `0x90` | `00457E10` | `00456EF0` | `00457FE0` | `00539DA0` | - | 765 / 313 |
| `0x91` | `00459420` | `004593E0` | `004595C0` | `00539E90` | - | 12 / 7 |
| `0x92` | `0045A050` | `0045A010` | `0045A200` | `00539E90` | - | 84 / 45 |
| `0x94` | `00455390` | `0045B260` | `0045AEE0` | `00539B30` | - | 2,344 / 387 |
| `0x95` | `00455390` | `0045B260` | `0045B2A0` | `00539B30` | - | 456 / 226 |
| `0x96` | `00453CB0` | `00453C70` | `00453CF0` | `00539980` | - | 268 / 75 |
| `0x97` | `00455390` | `0045B260` | `0045BAD0` | `00539F80` | - | none |

The band shares handlers across types, so a type here often selects a variant rather than a class:

- `0x80`, `0x82` and `0x83` share birth, update and setup and differ in their draw.
- `0x86` and `0x87` also use the update `00450480`.
- `0x8C`, `0x94`, `0x95` and `0x97` share birth and update; the first three also share the setup.
- `0x8F` and `0x90` share birth, update and setup; `0x91` and `0x92` share the setup; `0x84` and
  `0x96` share the setup.
- `0x93` and `0x98`–`0x9F` have no arm.

### Types 0xA0 to 0xAB

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0xA0` | `00460B80` | `00460B40` | `00460BC0` | `0053A6F0` | - | none |
| `0xA1` | `00461090` | `00461050` | `00461270` | `0053A790` | `00461250` | 504 / 343 |
| `0xA2` | `00462480` | `00462440` | `00462540` | `0053A840` | - | 6,303 / 2,018 |
| `0xA3` (sub) | `00524800` | `005247C0` | `00524A50` | `0054EE70` | `00524A10` | 447 / 131 |
| `0xA4` (sub) | `005222D0` | `00522290` | `00522300` | `0054EA70` | - | none |
| `0xA5` | `004633A0` | `00463360` | `00463460` | `0053A900` | - | 36 / 20 |
| `0xA6` (sub) | `00524D70` | `00524D30` | `00524E30` | `0054EED0` | - | 359 / 178 |
| `0xA7` (sub) | `005269B0` | `00526970` | `00526A10` | `0054F1B0` | - | 14 / 14 |
| `0xA8` (sub) | `00527110` | `005270D0` | `005271D0` | `0054F350` | - | 367 / 159 |
| `0xA9` (sub) | `00528090` | `00528050` | `00528150` | `0054F520` | - | none |
| `0xAA` (sub) | `00528AF0` | `00528AB0` | `00528B50` | `0054F700` | - | 3 / 3 |
| `0xAB` (sub) | `0052BFB0` | `0052BF70` | `0052C070` | `0054FE00` | - | 7 / 4 |

`0xA1`, `0xA2` and `0xA5` are, with `0x40`, `0x41` and `0xD0`, the definition types whose emitters
are drawn even when the instance's flag byte `+0x36A` bit 0 is clear (the runtime page).

### Types 0xD0 and 0xD1

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0xD0` | `00464F20` | `00464F10` | `00465680` | `0053A9D0` | `00465120` | 1,437 / 544 |
| `0xD1` | `003D9040` | `003D9000` | `0016D6A0` | `0053AA30` | `003D90C0` | 765 / 406 |

- `0xD0` changes how chosen characters look. Its apply `00465690` works from the flag word `+0x232`
  (`004656DB`) and passes each chosen character to `00465CD0`, which it calls from eight sites. `0xD0`
  and `0x41` share the update `00464F10`.
- With bit 0 of `+0x232` set the apply scales the scene colour per channel,
  `020926C0 x= 1 + w x (c / 128 - 1)`: `c` is the four colour bytes of `0042FDB0([+0x20] + 0x80, [+0x44])`
  and `w` the alpha byte of the `002F1F40` fade over 128 while bit 7 is set, else 0; bit 7 is then cleared
  (`004656C6`-`0046578F`).
- `0xD1` draws nothing (its draw is `0016D6A0`). Its update tail `003D92C0` publishes the element at
  `02092628` (`003D9698`); `00258B90`, which the field frame runs with its camera work
  ([frame update order](../Engine-Core/frame-update-order.md)), copies it into the block at
  `02096FA0` and clears the pointer (`00258C3B`–`00258D4D`).

- That copy is then turned into a camera by `003D9150` (from `00258B90`), unless the half-rate
  cadence test and `001EDAD0` hold it back: for the copy's key `+0x330` it takes the eye and target
  (`+0x230` / `+0x240`, 32 bytes a key, swapped when the definition's byte `+0x240` is set) and the
  roll (`+0x320`, 4 bytes a key) and fills the camera `02096ED0` with them through `003CC080`.
- With the definition's byte `+0x241` bit 0 set it uses `003CC970` instead, which first pulls the
  eye out of the map's collision (`0026E500`, `00230B60`). The field of view is the key's `+0x328`,
  with `1 / tan(fov / 2)` at `02096EE0`. It writes the camera into camera record 4, or 6 when `+0x241` bit 2 is set, with mode 3 and its active
  bit raised (`0025A2C0`, `0025A500`, `0025A520`); see [scripted camera](scripted-camera.md).

### The kind-0x54 mesh record

A mesh is an `0xB00` record of kind `0x54`: a `0x190`-byte object built by `004354E0` and loaded by
`00436D00(object, payload)`, which first calls the kind's destroy body `004352C0` (`00436D20`). The loader copies each array into a new block unless the object's `+0x18C` has bit
`0x8`, in which case it keeps a pointer into the stream (`00436D98`–`00436DDE`).

The id bytes name kind-`0x52` texture records: each is resolved through
`003AA280(key, 0x52, id)` with the record's own key word, into the handle array at `+0x184`
(`004370B8`–`004370FE`).

## Layouts

Kind-`0x54` payload (from `00436D00`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | flags: bits 0-2 -> object +0x18C; bit 0 adds the index lists |  |
| `+0x02` | `u16` | triangles | -> +`0x10` |
| `+0x04` | `u16` | quads | -> +`0x12` |
| `+0x06` | `u16` | positions | -> +`0x14`, array +`0x20`, 16 bytes each, w set to 1.0 |
| `+0x08` | `u16` | vectors | -> +`0x16`, array +`0x24`, 16 bytes each |
| `+0x0A` | `u16` | 4-byte entries | -> +`0x18`, array +`0x28` |
| `+0x0C` | `u16` | 8-byte entries | -> +`0x1A`, array +`0x2C` |
| `+0x0E` | `u16` | id bytes | -> +`0x1C`, ids +`0x180`, handles +`0x184` (8 bytes each) |
| `+0x10` | `u16` | 20-byte records | -> +`0x1E`, copied inline to +`0x30` |
| `+0x12` | `positions,` | vectors, | 4-byte, 8-byte and 20-byte arrays in that order; with flags bit 0, two index lists of 6 x triangles + 8 x quads bytes (+`0x170`, +`0x174`); then one byte per triangle and quad (+`0x188`); then the id bytes |

Element fields the verified draws read:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x044` | `i32` | track frame, the time every track is sampled at |  |
| `+0x1F0` | `u32` | colour |  |
| `+0x230` | `vec` | point 1 (types 0x01, 0x03); +0x240 point 2 (0x03) |  |
| `+0x294` | `i32` | mesh index (0x05) |  |

Definition fields the verified draws read:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x030` | `blend` | track | (mode 6) and alpha percent |
| `+0x044` | `u8` | element type |  |
| `+0x049` | `u8` | bits 5-7 blend mode |  |
| `+0x190` | `mesh-index` | track | (`0x05`); +`0x590` u8 bit 4 mesh-index mode; +`0x5A0` u32[32] mesh handles |

## Shipped data

| Fact | Value |
|---|---|
| element definitions | 48,868 `0xA00` records over 4,229 streams, 55 distinct types |
| types with code and no shipped definition | `0x03`, `0x07`, `0x08`, `0x70`, `0x81`, `0x8A`, `0x97`, `0xA0`, `0xA4`, `0xA9` |
| most used | `0x02` 7,523; `0x8C` 7,509; `0xA2` 6,303; `0x05` 5,204; `0x94` 2,344; `0x40` 2,254 |
| used once | `0x8B` |
| kind-`0x54` records | 2,733; flags `0x07` and key 0 in all; slot bytes 1 to 15 and 20 |
| kind-`0x54` sizes | the layout above plus 0 to 15 bytes of padding fills every record's chunk |
| kind-`0x54` arrays | 20-byte count 0 in all; 8-byte count equal to the 4-byte count in all |
| kind-`0x54` id bytes | 0 in 2,275 records, 1 in 444, 2 in 14; all 472 name a kind-`0x52` record of key 0 in the same stream |
| type-`0x05` definitions | 5,204; mesh slots filled at `+0x570`: one in 4,304, two in 898, three in 1, none in 1 |
| type-`0x05` mesh ids | all 6,103 equal the slot byte of a kind-`0x54` record in the same stream |

The per-type counts are in `effect-element-types-type_census.tsv`, which matches this census row
for row. `effect-element-types-effect-type-authored-usage.tsv` is an earlier, smaller census whose
counts this page supersedes. `effect-element-types-effect-mesh-54-records.tsv` (2,252 rows) and
`effect-element-types-effect-mesh-54-element05.tsv` (5,164 rows) list the mesh records and type-`0x05`
definitions of the `.efx` files one per row.

## Operations

One base update and one type tail per live element per simulation step; one draw call per drawn
element per frame; one apply per registered element (`0x40`, `0x41`, `0x42`, `0xD0`) per drawn
frame.

## State

The registry `02ADBFE0` (128 slots), the light pool behind `003AB960`, the pools at `[02B404E0]` and
`02B4D7D0`, the blend pair `02AEE900` / `02AEE908`, and the published element `02092628`.

## Modding notes

- A definition's type byte decides everything; a type without an arm in a table gets no behaviour
  for that method, and a draw arm that is `0016D6A0` draws nothing.
- Point and line blending comes from definition byte `+0x49` bits 5–7; mode 6 takes the blend word
  from the `+0x30` track, so that track then serves as both alpha percent and blend.
- A type-`0x05` mesh index of 32 or more falls back to 0, and its definition holds 32 handles.
- The registry holds 128 elements of types `0x40`, `0x41`, `0x42` and `0xD0`; `00377190` returns 0
  when it is full.

## Related

- [Effect element runtime](effect-element-runtime.md): the method tables, birth, update, release and
  the draw passes.
- [Effect files](effect-files-efx-efb.md): the `0xA00` and `0xB00` records.
- [Character lighting and shadows](character-lighting-and-shadows.md): the light pool `0x40` uses.
- [Authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md): the tracks
  every type samples.
- [PS2 VIF1 / VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the packet path
  many draw methods end in.
