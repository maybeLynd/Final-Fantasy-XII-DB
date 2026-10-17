---
title: "Effect element types: the handlers of every element type, what the verified types draw or change, and the kind-54ₕ mesh record"
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

An element definition is an `A00`<sub>h</sub> record; its header byte `+0E`<sub>h</sub> is the type, copied to the
definition's `+44`<sub>h</sub> by `003A9A70` and to the element's byte `+0` at birth by `002F2D60`
(`002F30F2`–`002F30F6`). How the five method tables dispatch on it, and when each method runs, is on
[effect element runtime](effect-element-runtime.md); the record grammar is on
[effect files](effect-files-efx-efb.md).

The tables give 65 types an arm, with 248 distinct handlers. Types `00`<sub>h</sub>–`0A`<sub>h</sub>, `40`<sub>h</sub>, `41`<sub>h</sub>,
`60`<sub>h</sub>–`67`<sub>h</sub>, `80`<sub>h</sub>–`97`<sub>h</sub>, `A0`<sub>h</sub>–`A2`<sub>h</sub>, `A5`<sub>h</sub>, `D0`<sub>h</sub> and `D1`<sub>h</sub>, except `09`<sub>h</sub>, `63`<sub>h</sub>, `64`<sub>h</sub>
and `93`<sub>h</sub>, are main-range types (47);
`42`<sub>h</sub>, `68`<sub>h</sub>–`6B`<sub>h</sub>, `70`<sub>h</sub>–`74`<sub>h</sub>, `A3`<sub>h</sub>, `A4`<sub>h</sub> and `A6`<sub>h</sub>–`AB`<sub>h</sub> are reached only through the
sub-range tables (18); `6C`<sub>h</sub>–`6F`<sub>h</sub> have no arm in either range (`0043EBF0`, byte map `0043ECC4`). The
full decode is in `effect-element-types-effect-type-methods.tsv`.

Every birth method except `70`<sub>h</sub>'s calls the base birth `002F2D60`, and every update method except
`70`<sub>h</sub>'s calls the base update `002F2530`. Most updates add a type tail: type 1's `004424E0` is
`002F2530` then `00442600`. Types `41`<sub>h</sub> and `D0`<sub>h</sub> share `00464F10`, a jump to the base alone. The
tails end in the cull, release and spawn fork of the runtime page. The base setup is `00500470`.

In the tables below "Authored" is the number of `A00`<sub>h</sub> definitions of the type over every shipped
stream, then the number of archive files holding them; a sub-range type's handlers are its
sub-range ones.

### The type names

`002FBA60(type)` returns the name of a type from a byte table at `002FBDEC` and a list of strings
from `00D0F9F0`; any other type below 256, and any type above, gives `"NONE TYPE NAME"` (`00D10150`).
The type-1 context builder `002FC4A0` prints these names for the element types of the stream it has
parsed while `022BE950` is set. The prefix is `TsElementType_` unless the row says `Nh`:

| Types | Names |
|---|---|
| `00`<sub>h</sub>–`08`<sub>h</sub> | NONE, POINT, SPRITE, LINE, CIRCLE, MODEL, COLUMN, SPHERE, BOARD1 |
| `0A`<sub>h</sub> | TAIL |
| `40`<sub>h</sub>–`42`<sub>h</sub> | LIGHT, OBJFOG, CAMERAVIBRATION |
| `60`<sub>h</sub>–`67`<sub>h</sub> | VTHUNDER, VTHUNDER2, VTHUNDER3, VLASER, VLASER2, VTEXTHUNDER, VTEXTHUNDER2, VAFTERWIND |
| `68`<sub>h</sub>–`6B`<sub>h</sub> (`Nh`) | VTEXLASER, VEFFAFTERGLOW, VEFFWATER, VAFTERWIND_MULTEX |
| `70`<sub>h</sub>–`74`<sub>h</sub> (`Nh`) | VEFFMETABALL, VAFTERTHUNDER, VPHYSICALEFFECT1, GLASSBREAK, MODELBREAK |
| `80`<sub>h</sub>–`8B`<sub>h</sub> | VLINE1, VBEZIER1, VLCYLINDER1, VLCYLINDER2, VGLOBULARANM, VTAIL, VCLROTLINE, VGLROTLINE, VGLROTANM, VCLROTANM, VGLANM2, VCCFITANM |
| `8C`<sub>h</sub>–`97`<sub>h</sub> | VMODEL02, VMODEL00, VMODEL01, VMODEL03, VMODEL04, VMODEL05, VMODEL06, VMODEL07, VMODEL08, VMODEL09, VGLANM3, VMODEL10 |
| `A0`<sub>h</sub>–`A2`<sub>h</sub> | 2DSTART, VLENSFLARE, 2DTEX |
| `A3`<sub>h</sub>, `A4`<sub>h</sub> (`Nh`) | VRAIN2, LOCATIONTITLE |
| `A5`<sub>h</sub> | 2DTEX2 |
| `A6`<sub>h</sub>–`AB`<sub>h</sub> (`Nh`) | 2DTEX2, 2DLINEBLUR, 2DTEX3, 2DCIRCLEPOLY, 2DLINEBLUR2, 2DTEXPOLYREQU |
| `D0`<sub>h</sub>, `D1`<sub>h</sub> | EXTCTRL, PCAMERA |
| `F0`<sub>h</sub>, `F1`<sub>h</sub> | PADVIBRATION, SOUND |
| `FF`<sub>h</sub> | INVALID |

Type `A1`<sub>h</sub>, VLENSFLARE, drives the eight lens-flare slots at `02ADBB40`.

### Types `00`<sub>h</sub> to `0A`<sub>h</sub>

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `00`<sub>h</sub> | `002F2D60` | `002F2530` | - | `00500470` | - | 1,446 / 458 |
| `01`<sub>h</sub> | `00442520` | `004424E0` | `00442550` | `00538A60` | - | 476 / 370 |
| `02`<sub>h</sub> | `00448DE0` | `00448D70` | `004490D0` | `00538AB0` | - | 7,523 / 1,141 |
| `03`<sub>h</sub> | `004427A0` | `00442760` | `004427D0` | `00538B80` | - | none |
| `04`<sub>h</sub> | `00445310` | `004452D0` | `004453D0` | `00538C80` | - | 173 / 81 |
| `05`<sub>h</sub> | `00449970` | `00449930` | `00449AB0` | `00538DB0` | - | 5,204 / 1,115 |
| `06`<sub>h</sub> | `00446F60` | `00446F20` | `00447020` | `00538EB0` | - | 25 / 9 |
| `07`<sub>h</sub> | `00447E10` | `00447DD0` | `00447ED0` | `00538EB0` | - | none |
| `08`<sub>h</sub> | `0044A5F0` | `0044A5B0` | `0044A620` | `00539030` | - | none |
| `0A`<sub>h</sub> | `0044BA80` | `0044BA40` | `0044BAC0` | `00539170` | - | 40 / 39 |

- `00`<sub>h</sub> has no draw method: it moves and fires spawn slots only.
- `01`<sub>h</sub> is a point. Its draw sets `02AEE908` to the integer track at definition `+30`<sub>h</sub> and
  `02AEE900` to definition byte `+49h >> 5`, then calls `0039C550` (`004425B2`–`004425E8`), which
  projects the point and emits a one-vertex `GiPrim` (kind 0 in the blended emitter, `0039DA7A`).
- `03`<sub>h</sub> is a line: its draw calls `0039C4C0` (`004427D0`), which projects both ends, drops the line
  when either end is rejected, and emits a two-vertex `GiPrim` of kind 1 (`0039C4EB`–`0039C52B`,
  `0039D769`, `0039D83C`).
- `02`<sub>h</sub> and `0A`<sub>h</sub> draw sprite frames through `00501A50` and `00502280` (`004490D0`, `0044BAC0`).
  Both frame drawers pick a row of a kind-`50`<sub>h</sub> record with `00502EA0`.
- `04`<sub>h</sub>, `06`<sub>h</sub> and `07`<sub>h</sub> share the grid emitters `004434D0` and `00444340`, which all three draws
  call.
- `05`<sub>h</sub> draws a mesh; see "Type `05`<sub>h</sub> and the mesh record" below.
- `06`<sub>h</sub> and `07`<sub>h</sub> share one setup, `00538EB0`.

### The point and line blend modes

`02AEE900`, definition byte `+49`<sub>h</sub> bits 5–7, picks the emitter. Mode 0 builds the primitive and
submits it at once (`0039D890` for a point, `0039D5A0` for a line). Modes 1 to 7 append a draw-list
entry first and set the primitive's blend word: `01EFAC20[mode]`, or in mode 6 the `+30`<sub>h</sub> track
value from `02AEE908` (`0039DA89`–`0039DAAC`, `0039D859`–`0039D875`).

| Mode | Blend word |
|---:|---|
| 0 | none: the immediate emitter |
| 1 | `48`<sub>h</sub> |
| 2 | `42`<sub>h</sub> |
| 3 | `44`<sub>h</sub> |
| 4 | `49`<sub>h</sub> |
| 5 | `46`<sub>h</sub> |
| 6 | the `+30`<sub>h</sub> track value |
| 7 | `4` |

### The polygon emitters

Every effect point, line and polygon reaches the renderer through a pair of emitters: one submits
its command at once (blend mode 0, through `0020E630(command, 2)`), the other files it on the draw
list first and sets the blend word as above (modes 1 to 7). The blended ones fill the `28`<sub>h</sub>-byte
entry the same way: the smallest of the vertices' 24-bit depths as the key `+8`, the pass nibble
`02AEE910` in bits 28 to 31, and the flag word `+20`<sub>h</sub> = `02AEF41C × 4` (`003A2C70`), plus `2` when
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
slot `+20`<sub>h</sub>. The callers `004355D0`, `00437130` and `00438860` are the mesh composers of type
`05`<sub>h</sub>, and `004434D0` and `00444340` the grid emitters of types `04`<sub>h</sub>, `06`<sub>h</sub> and `07`<sub>h</sub>. Their
texture coordinates pass through `0039B840` or `0039B860`, both jumps to `0039B880`, which adds the
offset pair its fifth argument points at to each coordinate and multiplies it by the vertex's `q`.

`004355D0` returns 1 without composing anything for a kind-7 effect `200`<sub>h</sub>–`23F`<sub>h</sub> drawn while the pass id
is 0 (`0024E410`) while the debug console's "Enable VFX Display" row (`+AC0`<sub>h</sub> of `[01F81428]`,
`001D50D0`) holds 2: `00180100` answers whether that row is not 2.

### The sprite and ribbon front ends

The sprite drawers `00501A50` and `00502280` (types `02`<sub>h</sub> and `0A`<sub>h</sub>) reach the quad emitters
through two front ends: while bit 6 of the request's byte `+46`<sub>h</sub> is clear, bit 0 picks between
them (`00501A50`).

- `0039C5D0` asks `0024D330` first. For 1 it installs the matrix `02AEECB0` (`0039B550`), projects
  the four corners with `00399B80`, which returns non-zero when a corner falls outside, multiplies
  each texture coordinate by its corner's `q` (`0039B780`), and calls the sprite pair. For 0 it
  hands the call to `0039C6B0`, which projects with the float routine `0039A770` and uses the
  float-path pair.
- `0024D330` returns 0 only when the current context's byte `+0` is 3 and the effect ticket its
  word `+4` names (`02EBCD80`, `38`<sub>h</sub> bytes a slot) has effect number `34`<sub>h</sub> at `+30`<sub>h</sub>. `003B33D0`
  checks the ticket id against the slot and returns that number, or −1 for a stale id.
- `0039CCB0` projects the corners one at a time (`00399B10`, which calls `00399600` per point and
  stops at the first rejected one) and passes the texture coordinates through unchanged.

Type `08`<sub>h</sub>'s draw `0044A620` builds a grid of (`+270`<sub>h</sub> + 1) × (`+274`<sub>h</sub> + 1) points. Untextured,
it draws each cell with `0039C770`, which projects two points from each of two rows with
`00399B10` and colours the quad with one RGBA word per row. Textured, it draws rows through
`00502160` → `0039C800`, the ribbon drawer, which walks a descriptor and draws one quad per
segment between two rails of points:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `08`<sub>h</sub> | `void*` | first rail, 16-byte points; segment i uses points i and i+1 |  |
| `10`<sub>h</sub> | `void*` | second rail |  |
| `18`<sub>h</sub> | `void*` | two RGBA words (first rail, second rail); with `+20`<sub>h</sub>, one word per segment for the first rail |  |
| `20`<sub>h</sub> | `void*` | one RGBA word per segment for the second rail, or null |  |
| `28`<sub>h</sub> | `void*` | 8-byte texture coordinates per point of the first rail, or null for the rectangle below |  |
| `30`<sub>h</sub> | `void*` | the same for the second rail |  |
| `38`<sub>h</sub> | `f32[4]` | u0, v0, u1, v1 |  |
| `48`<sub>h</sub> | `f32` | added to every u after each segment |  |
| `4C`<sub>h</sub> | `f32` | added to every v after each segment |  |
| `50`<sub>h</sub> | `void*` | texture pair |  |
| `58`<sub>h</sub> | `i32` | segment count |  |
| `5C`<sub>h</sub> | `i32` | segments after which the rectangle starts again from `+38`<sub>h</sub> |  |

The ribbon drawer skips a segment when either rail's pair of points is rejected by `00399B80`
(`0039C800`).

Element orientations come from `00398480(angles, out, order)`, which builds a rotation matrix from
three angles in one of six axis orders; type `08`<sub>h</sub> passes the definition byte `+48`<sub>h</sub> as the order
(`0044A7E0`). Orders 1 to 3 multiply three single-axis rotations (`003985B0`, `00398910`,
`00398C50`) in different orders; orders 0, 4 and 5 are written out in `00398DD0`, `00398A90` and `00398730`, which take
sine and cosine from the 32,768-step sine table `01F004E0`, the cosine as the entry a quarter turn on.

The direction helpers `003A2440`, `003A2570` and `003A2690` build an orthonormal matrix whose row 0,
1 or 2 is the normalised direction, with the other rows from cross products with the given up
vector (`003A27C0`, `00398390`), and write the derived up vector back.

### Sprite rows: 00502EA0

`00502EA0(record, index, mode)` returns the index-th row, among the rows of `90`<sub>h</sub> bytes from
record `+10`<sub>h</sub> whose byte `+70`<sub>h</sub> has bit 0 set. Mode 0 first clamps the index to `[+3Ch] − 1`,
mode 1 takes it modulo `[+3Ch]`, mode 2 accepts it up to the row count `+38`<sub>h</sub>, and any other mode
returns 0; no match returns 0 (`00502EA0`–`00502F21`).

### Sprite row helpers

A row names its texture and palette in three bytes: `+71`<sub>h</sub> indexes the kind-`50`<sub>h</sub> record's
texture handles (`+28`<sub>h</sub>, kind `52`<sub>h</sub>), `+72`<sub>h</sub> names the palette source, a kind-`53`<sub>h</sub> handle from
`+30`<sub>h</sub> when bit 7 is set and the texture itself otherwise, and `+73`<sub>h</sub> picks the palette slot.

- `00502F30(record, n, first, count)` finds the `n`-th enabled row and returns its index and the
  number of rows up to the next enabled one; it fails for `n` above the row count `+38`<sub>h</sub>.
- `005030F0(record, row, out)` copies the texture's 16-byte register pair (`+10`<sub>h</sub>) and, for a
  texture of format 0 to 2 whose row has `+72`<sub>h</sub> unlike `+71`<sub>h</sub> or a non-zero `+73`<sub>h</sub>, replaces
  the high 27 bits of its second word with the palette's address word (`+2Ch + 8 × slot` of a kind-`53`<sub>h</sub> record, or
  `+24h + 8 × slot` of the texture).
- `00503000(record, colours, count, handle)` returns the palette colours for the record's first
  row: 16 or 256 entries by the source's format, from the kind-`53`<sub>h</sub> record's `+20`<sub>h</sub> or the
  texture's `+B0`<sub>h</sub>, with its handle.
- `00502160(record, draw)` is type `08`<sub>h</sub>'s row walk: from the row the draw names, it sets each
  row's texture registers as `005030F0` does, switches to blend mode 6 with the row's word `+68`<sub>h</sub>
  when the draw's byte `+60`<sub>h</sub> has bits 1–3 equal to `C`<sub>h</sub>, and calls `0039C800`, until a row with
  `+70`<sub>h</sub> bit 1 or a following row whose `+70`<sub>h</sub> byte is non-zero.

### Draw-source blocks

Many types describe what they draw with `F0`<sub>h</sub>-byte blocks inside their definition; type `04`<sub>h</sub>'s
setup `00538C80` has four of them from `+2B0`<sub>h</sub>. A setup prepares each with `00431770(block, base)`,
which rebases the track group at `+00`<sub>h</sub> (`00430AF0`), the group at `+40`<sub>h</sub> (`0042FCF0`) and the
offsets `+90`<sub>h</sub>, `+94`<sub>h</sub>, `+E0`<sub>h</sub> and `+E4`<sub>h</sub>, clears `+A9`<sub>h</sub> unless `+AA`<sub>h</sub> has bit 4 or 5, binds
the source records (`00431610`) and returns the address after the block. `00431610` binds by the
source kind `+A0`<sub>h</sub>; a number of 0 leaves the handle at 0:

| `+A0`<sub>h</sub> | Records bound (`003AA280`) |
|---:|---|
| 1 | the kind-`54`<sub>h</sub> mesh numbered `+A1`<sub>h</sub> into `+B0`<sub>h</sub> |
| 2 | the kind-`52`<sub>h</sub> texture `+A2`<sub>h</sub> into `+B4`<sub>h</sub>; the palette `+A3`<sub>h</sub> into `+B8`<sub>h</sub>, kind `53`<sub>h</sub> when bit 7 is set (number in bits 0–6), else kind `52`<sub>h</sub> |
| 3 | the kind-`50`<sub>h</sub> sprite rows `+A5`<sub>h</sub> into `+BC`<sub>h</sub> and the kind-`51`<sub>h</sub> frame sequence `+A6`<sub>h</sub> into `+C0`<sub>h</sub> |

The draws read the block back through `00431830`. For source kind 2 it returns the texture's
register word (`+10`<sub>h</sub>) with the palette address of slot `+A4`<sub>h</sub> in its high half; when the byte
`+D0`<sub>h</sub> is set it instead derives a palette from the source palette with `00431B10(block + D0h,
…)`, 16 entries when the palette's byte `+10`<sub>h</sub> is `80`<sub>h</sub> and 256 otherwise, and puts that
palette's address there. For source kind 3
it steps the frame sequence (`005039A0`) and picks the row with `00502EA0`.

### Track values in other units

A track is 16 bytes: two key arrays (offsets `+00`<sub>h</sub> and `+04`<sub>h</sub>, counts `+0C`<sub>h</sub> and `+0D`<sub>h</sub>) of
8-byte keys whose value is at `+4`. `004314E0(track, frame)` reads it: 0 for an empty array, the one
key's value for a count of 1, `00431080` otherwise, and with both arrays the two results combined
by `00431350`.

A setup can rescale the stored values once. `00430A60(track, f)` multiplies every key value of
both arrays by `f`, `00431040(group, f)` does so for the three tracks of a group (`+00`<sub>h</sub>, `+10`<sub>h</sub>,
`+20`<sub>h</sub>), and `00431580(track, n)` multiplies integer values by `n`. Type `03`<sub>h</sub>'s setup `00538B80`
turns the group at `+80`<sub>h</sub> from degrees to radians (`π/180`), divides the groups at `+100`<sub>h</sub> and
`+140`<sub>h</sub> by 100 and multiplies the integer track at `+180`<sub>h</sub> by 100.

### Generated palettes

`00431B10(op, colours, n, frame, texture)` derives a palette from `n` source colours. It unpacks the
colours into the work area `02CA4EE0` (`003CD840`), reads the operation's track `op + 10h` at
`frame` (`004314E0`), and runs the operation the kind byte `op + 00h` names; any other kind
returns 0 and the source palette stays:

| Kind | Body | Fields it reads |
|---:|---|---|
| 1 | `0050AC20` | byte `+01`<sub>h</sub>, bits 1–2 of `+03`<sub>h</sub> |
| 2 | `00506B40` | words `+08`<sub>h</sub> to `+0E`<sub>h</sub>, bit 0 of `+03`<sub>h</sub> |
| 3 | `005080A0` | words `+04`<sub>h</sub>, `+06`<sub>h</sub>, bit 0 of `+03`<sub>h</sub> |
| 5 | `00509BB0` | none besides the track |
| 6 | `00507490` | words `+04`<sub>h</sub>, `+06`<sub>h</sub> |
| 7 | `00508C90` | bytes `+01`<sub>h</sub>, `+02`<sub>h</sub>, words `+04`<sub>h</sub>, `+06`<sub>h</sub> |

With bit 3 of `+03`<sub>h</sub> set the operation gets `n − 1` and a flag instead of `n`. `003A9C10(work, n,
texture)` then
reserves room for the palette in the emulated GS memory (`002D81D0`, which can refuse), takes an
`n × 4 + 10h`-byte block linked on the current record table's list `+10`<sub>h</sub>, packs the colours into
it (`003D2B60`), writes them into the palette texture (`00183640`) and returns the GS address.

The draws of types `02`<sub>h</sub>, `0A`<sub>h</sub>, `84`<sub>h</sub>, `85`<sub>h</sub>, `88`<sub>h</sub>, `89`<sub>h</sub>, `8A`<sub>h</sub>, `8B`<sub>h</sub>, `96`<sub>h</sub> and `A1`<sub>h</sub>
call `00431B10` themselves; type `02`<sub>h</sub>'s draw `004490D0` passes definition `+160`<sub>h</sub> and the
palette of its first sprite row (`00503000`).

### Frame sequences: the kind-`51`<sub>h</sub> record

A kind-`51`<sub>h</sub> record holds `+10`<sub>h</sub> entries of 16 bytes at `+18`<sub>h</sub>. An entry's byte `+8` is its
opcode: 0 shows a frame for byte `+9` ticks, 1 jumps to the entry in word `+C`<sub>h</sub>, and 2 ends the
sequence. `005039A0(sequence, time, mode)` returns the frame entry at `time`; at the end, mode 0
keeps the last frame, mode 1 starts over with the time reduced, and mode 2 returns 0.
`00503A80(sequence, cursor)` does the same from a four-byte cursor (entry, time, last frame,
mode) that it updates, for type `02`<sub>h</sub>'s draw `004490D0`.

The texture source resolver `00431830` uses `005039A0` with mode bit 6 of the sub-record's word
`+AA`<sub>h</sub>, then picks the sprite row from the frame's word `+A`<sub>h</sub> with `00502EA0` and its registers
with `005030F0`.

### The mesh and sprite triangle emitters

Four emitters turn projected triangles into `GiPrim` commands of kind 5; the mesh draw and the
sprite frame drawers `00501A50` and `00502280` use them.

| Emitter | Texture | Filing |
|---|---|---|
| `0043D8F0(positions, colours, n)` | none | at once, `0020E630(command, 2)` |
| `0043DB90(positions, uv, q, textures, colours, n)` | `u / q`, `v / q`; texture pair at `+38`<sub>h</sub>, `+48`<sub>h</sub> | at once |
| `0043E440(positions, colours, n)` | none | draw-list entry |
| `0043DF80(positions, uv, q, textures, colours, n)` | as `0043DB90` | draw-list entry |

The colour bytes become floats. The two list emitters key the entry on the smallest of the three
vertices' 24-bit depth words, OR in the pass nibble, and set the primitive's blend word to
`01EFAC20[02AEE900]`, or to `02AEE908` in mode 6, as the point emitter does
(`0043DFCF`–`0043E012`, `0043E3EC`–`0043E401`; `0043E48E`–`0043E4D0`, `0043E760`–`0043E775`).

### Type `05`<sub>h</sub> and the mesh record

`00449AB0` draws one mesh. When definition byte `+590`<sub>h</sub> has bit 4 clear, the mesh index `+294`<sub>h</sub>
is the integer part of the float track at definition `+190`<sub>h</sub>, or 0 when that is not positive or
not below 32 (`00449DA7`–`00449DF9`). It publishes the blend pair as the point does and passes the
handle `[definition + 5A0h + index × 4]`, decoded, to the model composer `004355D0`
(`0044A11C`–`0044A15B`). The handles are kind-`54`<sub>h</sub> records.

### How the composer prepares a mesh

`004355D0(object, state)` draws nothing for an object without bits 0 and 2 of `+18C`<sub>h</sub>. It
first builds the mesh's vertices into the scratch block `[02AEED50]`:

- `00434CD0` when the state's `+1E8`<sub>h</sub> is set: it blends each array of the object with the same
  array of the object at state `+48`<sub>h</sub>, weights `1 − t` and `t` with `t` the float `+1EC`<sub>h</sub>; state
  byte `+1F1`<sub>h</sub> bits 4, 5 and 6 copy the 4-byte, 8-byte and vector arrays unblended instead;
- `00435050` otherwise: it copies the arrays unblended.

Both call `00434C50(state, byte +1F1h & 7)`, which multiplies the state's matrix by `02AEEC30`
(mode 1), `02AEEC70` (mode 2) or `02AEEA60` (modes 4 and 5); mode 4 first turns the matrix toward
the point `02AEEAD0` from the position `+30`<sub>h</sub> (`00434900`), and mode 5 turns it about one axis by
the `atan2` of the same direction (`00434A70`). Then they project the positions; a rejected mesh
draws nothing (`00399B80` at `00434ED9` and `0043526E`).

- With byte `+1F1`<sub>h</sub> bit 3 and `0024E410` true, the projection is not tested and the first six
  (`00434CD0`) or four (`00435050`) projected vertices are overwritten with fixed screen values,
  one set for language ids 1–6 (`00229E40`) and another for the rest.
- Byte `+1F1`<sub>h</sub> at `80`<sub>h</sub> or above hands the mesh to `00438860`; bit 3 hands it to `00437130`.
  Otherwise `004355D0` runs its own loop over the `+1F0`<sub>h</sub> layers.

`00437130` is the same per-layer loop without one step: for a layer of mode 4, `004355D0` divides
the first float of the layer's pair at state `+50h + 8 × layer` by 1.15 and multiplies the second
by 1.15 (`00435D23`–`00435D49`), and `00437130` does not. In both, a layer of mode 5 emits flat triangles and quads, mode 1 textured
ones whose texture comes from the face's byte at `+188`<sub>h</sub>, and any other mode textured ones with
the layer's texture; blend mode 0 files at once and any other mode through the draw list.

The composers share two helpers with the element types at `004434D0`, `00444340`, `004584E0` and
`004595C0`: `00394DA0(matrix, vector, out)` multiplies the vector by the matrix without its
translation, giving four floats, and `00394B70(vertices, indices, out, n)` adds, for each of `n`
indices into the 16-byte projected vertices, the vertex's screen position `x / 16 / 512 − 3.5` and
`y / 16 / 512 − 3.5625` to the next float pair of `out`.

### Types `40`<sub>h</sub> to `42`<sub>h</sub>

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `40`<sub>h</sub> | `00463FF0` | `00463FB0` | `00464090` | `0053AAC0` | `00464050` | 2,254 / 744 |
| `41`<sub>h</sub> | `00464B30` | `00464F10` | `00464BC0` | `0053AB10` | `00464B80` | 425 / 310 |
| `42`<sub>h</sub> (sub) | `0047BE20` | `0047BDA0` | `0047BFA0` | `0050C450` | `0047BF70` | 613 / 350 |

These types, with `D0`<sub>h</sub>, act on the scene instead of drawing. Their births register the element in
the 128-slot registry at `02ADBFE0` (`20`<sub>h</sub> bytes a slot, handle `serial << 8 | slot`, element at
`+8`) through `00377190`, whose only callers are those four births. Their draw methods only set a
bit: `00464090` sets bit `2`<sub>h</sub> of `+248`<sub>h</sub>, `00464BC0` bit `1`<sub>h</sub> of `+23C`<sub>h</sub>.

The releases `00464050` (`40`<sub>h</sub>), `00464B80` (`41`<sub>h</sub>), `00465120` (`D0`<sub>h</sub>) and `0047BF70` (`42`<sub>h</sub>)
free the slot through `00377360(handle)`, which finds it in the registry's live list (head
`02ADBFC8`, tail `02ADBFD0`, links at `+10`<sub>h</sub> and `+18`<sub>h</sub>), lowers the count `02ADBFC0`, clears the
handle and unlinks it.

`00377230` walks the registry from `MainLoop_Draw` (`0022B268`) and the menu frame (`0022B940`),
checks visibility with the group gate and the per-instance gate (`00377292`–`003772A2`), and calls
the type's apply body: `004640A0` (`40`<sub>h</sub>), `00464BD0` (`41`<sub>h</sub>), `0047BD30` (`42`<sub>h</sub>) and `00465690`
(`D0`<sub>h</sub>) (`003772EA`–`00377336`).

- `40`<sub>h</sub> makes a light. `004640A0` fills a request and creates it with `003AB960` the first time,
  keeping the handle at `+244`<sub>h</sub>, and updates it with `003AC920` afterwards (`00464387`–`004643A0`).
  Definition byte `+120`<sub>h</sub> picks the request word: 1 gives `8001`<sub>h</sub>, 2 gives `8006`<sub>h</sub>, anything else
  `8002`<sub>h</sub> (`004640C3`–`0046410A`). The pool is on [character lighting](character-lighting-and-shadows.md).
- `41`<sub>h</sub>'s apply keeps a record in the 64-entry pool of `60`<sub>h</sub>-byte records at `[02B404E0]` through
  `003B4160`.
- `42`<sub>h</sub>'s birth reads three floats at definition `+124`<sub>h</sub>, `+128`<sub>h</sub> and `+12C`<sub>h</sub> and the track group
  at `+80`<sub>h</sub>, and takes a slot in the 32-entry, `60`<sub>h</sub>-byte pool at `02B4D7D0` through `003D7FF0`
  (`0047BE64`–`0047BF08`).

- The `42`<sub>h</sub> pool slots are named by `serial << 8 | slot`, checked at slot `+04`<sub>h</sub>. `003D8300(handle)`,
  from the release `0047BF70`, `003E69A0` and `003E7140`, frees a slot: it lowers the count
  `02B4D7A0`, clears the handle and unlinks the slot from the list `02B4D7A8` / `02B4D7B0` (encoded
  links at `+08`<sub>h</sub> and `+0C`<sub>h</sub>).
- `003D8D70(handle, b)` stores byte `+3F`<sub>h</sub> and `003D8DE0(handle, v)` the three floats
  `+10`<sub>h</sub>–`+18`<sub>h</sub>; the birth, the update and `003E6910` call both. `003D8DA0(mode)`,
  from the field camera's target read `003D9E20`, stores 1.0 for mode 1, 0.6 for mode 2 and 0
  otherwise at `02B4D7B8`, which `003D83A0` and `003D8C30` read.

### Types `60`<sub>h</sub> to `74`<sub>h</sub>

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `60`<sub>h</sub> | `0045BF50` | `0045BF10` | `0045BFB0` | `0053A120` | - | 84 / 22 |
| `61`<sub>h</sub> | `0045C920` | `0045C8E0` | `0045C980` | `0053A060` | - | 9 / 7 |
| `62`<sub>h</sub> | `0045D290` | `0045D250` | `0045D2F0` | `0053A120` | - | 2 / 2 |
| `65`<sub>h</sub> | `0045DCA0` | `0045DC60` | `0045DD10` | `0053A1E0` | - | 169 / 44 |
| `66`<sub>h</sub> | `0045E8C0` | `0045E880` | `0045E930` | `0053A3B0` | - | 414 / 123 |
| `67`<sub>h</sub> | `0045FD50` | `0045FD10` | `00460170` | `0053A5D0` | `00460120` | 364 / 207 |
| `68`<sub>h</sub> (sub) | `00522AB0` | `00522A70` | `00522D80` | `0054EB40` | - | 162 / 83 |
| `69`<sub>h</sub> (sub) | `00523C30` | `00523BF0` | `00523D30` | `0054ED10` | - | 58 / 22 |
| `6A`<sub>h</sub> (sub) | `00525D50` | `00525D10` | `00526080` | `0054F070` | `00526040` | 395 / 210 |
| `6B`<sub>h</sub> (sub) | `00529200` | `005291C0` | `005294F0` | `0054F7C0` | `005294B0` | 258 / 117 |
| `70`<sub>h</sub> (sub) | `0053DD10` | `005C5230` | `0016D6A0` | `0054F270` | `0016D6A0` | none |
| `71`<sub>h</sub> (sub) | `0052A130` | `0052A0F0` | `0052A360` | `0054F9B0` | `0052A340` | 28 / 12 |
| `72`<sub>h</sub> (sub) | `0052ADF0` | `0052ADB0` | `0052B080` | `0054FBE0` | `0052B060` | 89 / 47 |
| `73`<sub>h</sub> (sub) | `0052D3B0` | `0052D370` | `0052D920` | `0054FFF0` | `0052D8E0` | 14 / 8 |
| `74`<sub>h</sub> (sub) | `0052E430` | `0052E3F0` | `0052EA90` | `00550200` | `0052EA50` | 4 / 3 |

- `60`<sub>h</sub> and `62`<sub>h</sub> share the setup `0053A120`.
- `70`<sub>h</sub> does nothing at run time: its birth `0053DD10` returns 1, its update `005C5230` returns 0,
  and its draw and release are the bare `ret 0` at `0016D6A0`. Only its setup reads the record.
- `67`<sub>h</sub>, `68`<sub>h</sub>, `6A`<sub>h</sub>, `6B`<sub>h</sub>, `71`<sub>h</sub>, `73`<sub>h</sub> and `74`<sub>h</sub> update on even frames only in the
  half-rate cadence (the base update's bit set `341B`<sub>h</sub>, on the runtime page).
- `63`<sub>h</sub>, `64`<sub>h</sub> and `6C`<sub>h</sub>–`6F`<sub>h</sub> have no arm in any table.

### Sub-range draw packets

The sub-range draws build a PS2-style packet in the data arena instead of emitting primitives. Each
one asks a size function for the packet's length in quadwords, gives up when the cursor `02F8F2D0`
plus that length would reach the end `02F8F2D8`, lets a builder write the packet at the cursor and
return the new cursor, and hands the packet to a finaliser (`0052329D`–`0052335F` for type `68`<sub>h</sub>).

| Type | Draw | Size | Builder | Templates copied (program) | Finaliser |
|---|---|---|---|---|---|
| `68`<sub>h</sub> | `00522D80` | `00541DB0` | `00542100` | `02AEB610` (`004DF440`), `02AEB810` (`004E0F70`), `02AEB820` | `00540F40` |
| `69`<sub>h</sub> | `00523D30` | `00543940` | `005439D0` | `02AEB0F0` (`004DCC00`), `02AEB290` (`004DDDF0`), `02AEB2A0` | `00540F40` |
| `A3`<sub>h</sub> | `00524A50` | `00544590` | `00544A50` | `02AEA270` (`004DB350`) | `00540F40` |
| `A6`<sub>h</sub> | `00524E30` | `00544CE0` | `00544D30` | `02AE9BC0` (`004DA8A0`), `02AE9D50` | `00540F40` |
| `6B`<sub>h</sub> | `005294F0` | `00532E80` | `00533250`; `005325D0` with definition word `+866`<sub>h</sub> bit `2000`<sub>h</sub> | `02AECAC0` (`004E7D90`), `02AECAD0`, `02AECCC0`; `02AEBBB0` (`004E31E0`), `02AEBBC0`, `02AEBDB0` | `00540F40` |
| `6A`<sub>h</sub> | `00526080` | `00545EF0` | `005466E0` | `02AE9130` (`004D7BF0`), `02AE9140`, `02AE9290` | `00540DB0` |
| `A8`<sub>h</sub> | `005271D0` | `00547350` | `005473A0` | `02AE9BC0` (`004DA8A0`), `02AE9D50`, `02AE9EE0` | `00540F40` |
| `A9`<sub>h</sub> | `00528150` | `005479B0` | `00547A00` | `02AE8CF0` (`00479650`), `02AE8D30` | `00540C20` |
| `71`<sub>h</sub> | `0052A360` | `00547D80` | `005480E0` | `02AE8620` (`004D40E0`), `02AE87B0`, `02AE8830` | `00540F40` |
| `72`<sub>h</sub> | `0052B080` | `0054A980` | `0054AA90` | `02AECD20` (`004D0FA0`), `02AECEB0`, `02AED130` | `00540F40` |
| `AB`<sub>h</sub> | `0052C070` | `0054B3A0` | `0054B3E0` | `02AE9BC0` (`004DA8A0`), `02AE9D50`, `02AE9EE0`, `02AEC4B0` (`004CF490`) | `00540F40` |
| `73`<sub>h</sub> | `0052D920` | `0054BD40` | `0054BE70` | `02AEBE10` (`004C8320`), `02AEC0A0`, `02AEC110` | `00540F40` |
| `74`<sub>h</sub> | `0052EA90` | `0054D610` | `0054D740` | `02AEBE10` (`004C8320`), `02AEC0A0`, `02AEC110` | `00540DB0` |

The templates are the boot-time VIF objects of
[PS2 VIF1 / VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md); a builder copies
their quadwords into the packet and patches in the element's values, and a program in brackets is
the microprogram the template's header installs. `A6`<sub>h</sub>, `A8`<sub>h</sub> and `AB`<sub>h</sub> share the templates of
`02AE9BC0` and `02AE9D50`, and `73`<sub>h</sub> and `74`<sub>h</sub> share all three of theirs.

- A size function adds a fixed head to a cost per enabled layer slot, the first enabled slot
  costing less: `00541DB0` returns 0 unless byte `+38`<sub>h</sub> is set, then `230`<sub>h</sub> bytes plus `B0`<sub>h</sub> for
  the first and `C0`<sub>h</sub> for each further of three slots (`+140`<sub>h</sub>, stride `50`<sub>h</sub>); `00544CE0`,
  `00547350` and `005479B0` count four slots from a `40`<sub>h</sub>-byte head.
- `0054B3A0` never returns 0: its head is `4F0`<sub>h</sub> bytes. `00543940` adds `190`<sub>h</sub> bytes for each of
  four non-zero words at `+740`<sub>h</sub>–`+830`<sub>h</sub>; `00544590` adds one quadword per 20 entries to `130`<sub>h</sub>.
- `00545EF0` (type `6A`<sub>h</sub>) starts from `(+1Ch + 17h) x 16` bytes and adds, per tile, `60`<sub>h</sub> plus
  `w x h x 16` when bit 1 of `+64`<sub>h</sub> is set. Tiles start every 21 grid points along `+10`<sub>h</sub> and `+14`<sub>h</sub>
  while the start is below the count minus 1, and `w = min(22, +10h - start)`, `h` likewise; it returns
  the total `>> 4` (`00545EF0`-`00545FAE`).
- `0054BD40` and `0054D610` add the two index blocks
  of every piece and, per enabled layer byte `+E0`<sub>h</sub>–`+E3`<sub>h</sub>, `60`<sub>h</sub> bytes per piece.
- `00540F40(packet, chain, count, key)` computes the flag word, 2 when `0024E460` or `003A3D20`
  returns non-zero, ORed with `003A2C70()`, and passes everything to `00540DB0`, which appends the
  draw-list entry and copies the packet into a command (`00540F65`–`00540F96`).
- `00540C20(packet, chain, count, key)`, used by `A9`<sub>h</sub> alone, appends an entry with the packet at
  `+00`<sub>h</sub>, the key and pass nibble at `+08`<sub>h</sub>, the chain count at `+0C`<sub>h</sub> and a null function at
  `+10`<sub>h</sub>, and builds no command (`00540C20`–`00540C6B`). `A9`<sub>h</sub> sets `02AEF418` around the call
  when its key is `FFFE00`<sub>h</sub> or more and `0024E2E0` returns 0 (`005287A6`–`005287C2`).
- The key is the projected depth of the element position for `68`<sub>h</sub> and `69`<sub>h</sub> (`00202B70` with
  `02AEEBB0`, then z / w); `A3`<sub>h</sub> and `AB`<sub>h</sub> use `FFFFFF`<sub>h</sub> and the rest use 0.

### Type `6A`<sub>h</sub>: the ripple surface

Type `6A`<sub>h</sub> simulates a height field with the damped two-dimensional wave equation. Its birth
`00525D50` copies the definition's time step, wave speed, grid spacing and damping (`+3D0`<sub>h</sub>–`+3DC`<sub>h</sub>)
and the grid's point counts (`+3F0`<sub>h</sub>, `+3F4`<sub>h</sub>) into the element block at `+230`<sub>h</sub>, allocates
16 bytes per point, and then:

- `00545120` derives the three step coefficients `k1 = (4 − 8c²t²/d²) / (μt + 2)`,
  `k2 = (μt − 2) / (μt + 2)` and `k3 = (2c²t²/d²) / (μt + 2)` into block `+30`<sub>h</sub>, `+34`<sub>h</sub> and
  `+38`<sub>h</sub>, the half extents `(n − 1)d / 2`, and the number of tiles the packet needs;
- `005450E0` zeroes the `n × m` points; `005263F0` then runs once per warm-up frame, the count from
  definition word `+3FC`<sub>h</sub> (`00525FDA`–`0052601D`).

`005263F0` is the update tail. Definition byte `+3FF`<sub>h</sub> bits 3, 1 and 2 enable three disturbances,
each a strength track (`+250`<sub>h</sub>, `+260`<sub>h</sub>, `+270`<sub>h</sub>) and a position track (`+280`<sub>h</sub>, `+2C0`<sub>h</sub>,
`+300`<sub>h</sub>) in grid units. A disturbance with a non-zero strength stamps the grid; it then runs the
step `00545650` as many times as the integer track `+3C0`<sub>h</sub> gives, at most 5.

- `00545310(grid, x, y, h)` sets a 3 × 3 stamp: `h` at the point, `h / 2` at its four neighbours and
  `h / 4` at the corners; `00545490` adds the same stamp. Points within two of the edge are left alone.
- With bit `20`<sub>h</sub> of `+3FF`<sub>h</sub>, `00546DB0` and `00547060` stamp a line of points instead, each scaled
  by `(1 + cos φ) / 2` with the phase stepping along the line. Definition byte `+3F9`<sub>h</sub> picks the
  adding forms.
- `00545650` updates every interior point from itself, its previous height and its four neighbours
  with `k1`, `k2` and `k3`.

### Types `73`<sub>h</sub> and `74`<sub>h</sub>: the flying pieces

Types `73`<sub>h</sub> and `74`<sub>h</sub> break a mesh into pieces of `A0`<sub>h</sub> bytes that fly and spin. `73`<sub>h</sub>'s birth
`0052D3B0` copies the authored piece data (`+954`<sub>h</sub> bytes from definition `+960`<sub>h</sub>), allocates one
record per piece (count at `+968`<sub>h</sub>) and randomises its ranges; `0054C6B0` then gives each piece a
start velocity and spin, the direction chosen by the low three bits of block byte `+4E`<sub>h</sub>.

Each step, `0054C440` (`73`<sub>h</sub>, from the update tail `0052E270`) and `0054DD30` (`74`<sub>h</sub>, from
`0052F400`) walk the pieces. The second component `+24`<sub>h</sub> of a piece's velocity `+20`<sub>h</sub> loses
gravity, its position `+70`<sub>h</sub> adds the velocity and its angles `+00`<sub>h</sub> add the spin `+10`<sub>h</sub>, each
scaled by one of two parameter sets chosen by the piece's time against the block's thresholds;
`0046D560` then rebuilds the piece's rotation at `+40`<sub>h</sub>.

In `0054C440` the step is `v.y -= [+C0h] x [+44h] x s x k.y`, then per axis `pos += s x k x v` and
`angle += r x spin x q`. Set A is `s` = block `+58`<sub>h</sub>, `k` = `+80`<sub>h</sub>-`+88`<sub>h</sub>, `r` = `+70`<sub>h</sub>-`+78`<sub>h</sub>,
`q` = `+5C`<sub>h</sub>; set B is `+90`<sub>h</sub>, `+B0`<sub>h</sub>-`+B8`<sub>h</sub>, `+A0`<sub>h</sub>-`+A8`<sub>h</sub> and `+94`<sub>h</sub> (`0054C4AE`-`0054C67E`).

Set A applies when piece `+0Ch <= [+C4h]` or piece `+98h <= [+3Ch]`. Otherwise set B applies, unless
piece `+0Ch > (1 - [+C4h]) x [+FCh] + [+C4h]` and piece `+98h > (1 - [+3Ch]) x [+9Ch] + [+3Ch]`, which
leaves the piece unmoved that step.

- `0054C440` moves only a piece whose `+30`<sub>h</sub> points to itself (`0054C4A4`).
- `0054DD30` rotates the velocity step by the matrix at block `+150`<sub>h</sub> when bit 1 of `+9C`<sub>h</sub> is set
  (`00202B90`).

### Births of the other sub-range types

- `68`<sub>h</sub>'s birth `00522AB0` calls `00541E00`, which draws five random values `r0`-`r4` =
  `003D8E50(1.0) - 0.5` into `+00`<sub>h</sub>-`+10`<sub>h</sub> and, unless block byte `+39`<sub>h</sub> bits 3 or 4 say otherwise,
  sets `+A0h = normalise(r0, r1, r2) x L1` and `+B0h = normalise(r3, r4, 003D8E50(1.0) - 0.5) x L2`
  (`00380800` normalises; `00541E12`-`00541FCF`).
  - `L1 = [+ACh] + 003D8E50([+120h])` and `L2 = [+BCh] + 003D8E50([+124h])`, written back to `+AC`<sub>h</sub>
    and `+BC`<sub>h</sub>.
- The same birth calls `00542060`, which draws six more in `[−0.5, 0.5)`.
- `69`<sub>h</sub>'s birth `00523C30` calls `005439A0`, which clears block `+04`<sub>h</sub> and `+14`<sub>h</sub> and stores
  the float `1 / (count + 1)`, the count being block `+00`<sub>h</sub>, at `+18`<sub>h</sub>.
- `67`<sub>h</sub>'s birth `0045FD50` and `6B`<sub>h</sub>'s birth `00529200` call `00532EF0`, which fills each of
  the `+B0`<sub>h</sub> strands (`440`<sub>h</sub> bytes) with a base plus a random amount for every parameter and a
  direction from a random or stepped angle; `00532E80` sizes `6B`<sub>h</sub>'s packet from the strand count
  and three enabled layers (`+88`<sub>h</sub>–`+90`<sub>h</sub>).
  - Each field is `base + 003D8E50(1.0) x range`, with the strand field, block base and block range:
    `+10`<sub>h</sub>, `+C8`<sub>h</sub>, `+CC`<sub>h</sub>; `+14`<sub>h</sub>, `+F8`<sub>h</sub>, `+FC`<sub>h</sub>; `+18`<sub>h</sub>, `+100`<sub>h</sub>, `+104`<sub>h</sub>; `+424`<sub>h</sub>, `+D8`<sub>h</sub>,
    `+DC`<sub>h</sub>; `+434`<sub>h</sub>, `+C0`<sub>h</sub>, `+C4`<sub>h</sub>; `+438`<sub>h</sub>, `+E8`<sub>h</sub>, `+EC`<sub>h</sub>; `+43C`<sub>h</sub>, `+F0`<sub>h</sub>, `+F4`<sub>h</sub>
    (`00532EF0`-`00533242`).
  - `+08`<sub>h</sub> takes `+E0`<sub>h</sub>, `+E4`<sub>h</sub> the same way when block `+140`<sub>h</sub> bit 1 is set, else
    `(+14h + +18h) x 0.5`; `+1C`<sub>h</sub> is `003D8E50(1.0) x` block `+1C`<sub>h</sub>.
  - The direction is `+420h = L sin a`, `+428h = L cos a`, `+42Ch = 1.0`, with `L` from `+D0`<sub>h</sub>, `+D4`<sub>h</sub>
    as above and `a = 003D8E50(6.284)` while block `+124`<sub>h</sub> is 0, otherwise `+128`<sub>h</sub> plus `+12C`<sub>h</sub> for each
    strand before it.
- `71`<sub>h</sub>'s birth `0052A130` calls `00547DD0`, which fills each of the `+140`<sub>h</sub> records (`450`<sub>h</sub>
  bytes) with a base plus a random amount for every parameter, and a direction from a random or
  stepped angle.
  - Each field is `base + 003D8E50(range)`, with the record field, block base and range: `+10`<sub>h</sub>, `+158`<sub>h</sub>,
    `+15C`<sub>h</sub>; `+08`<sub>h</sub>, `+188`<sub>h</sub>, `+18C`<sub>h</sub>; `+0C`<sub>h</sub>, `+190`<sub>h</sub>, `+194`<sub>h</sub>; `+434`<sub>h</sub>, `+168`<sub>h</sub>, `+16C`<sub>h</sub>;
    `+444`<sub>h</sub>, `+150`<sub>h</sub>, `+154`<sub>h</sub>; `+448`<sub>h</sub>, `+178`<sub>h</sub>, `+17C`<sub>h</sub>; `+44C`<sub>h</sub>, `+180`<sub>h</sub>, `+184`<sub>h</sub>
    (`00547DD0`-`005480D7`).
  - `+04h = u16 +170h + 003A6E60(u16 +172h)`; `+14`<sub>h</sub>-`+1C`<sub>h</sub> are each `003D8E50([+48h])` and
    `+20`<sub>h</sub>-`+28`<sub>h</sub> each `003D8E50([+4Ch])`.
  - The direction is `+430h = L sin a`, `+438h = L cos a`, `+43Ch = 1.0`, with
    `L = +160h + 003D8E50(+164h)` and `a = 003D8E50(6.284)` while block byte `+67`<sub>h</sub> is 0, otherwise
    `+70`<sub>h</sub> plus `+74`<sub>h</sub> for each record before it.
- `72`<sub>h</sub> keeps a sway chain (see [model oscillators](model-oscillators-and-pose-sequencer.md)).
  `0054B0E0`, called by its birth tail `0052BBD0` and its update tail `0052B5E0`, adds an offset to
  every node and sets the root; `0054A690(section, out, mode)`, called by `0052B5E0`, returns the
  root (mode 0) or walks the segment lengths `+38`<sub>h</sub> to the chain's middle (mode 1) or tip (mode 2).

### Types `80`<sub>h</sub> to `97`<sub>h</sub>

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `80`<sub>h</sub> | `0044CC10` | `00450480` | `0044CC50` | `00539320` | - | 875 / 381 |
| `81`<sub>h</sub> | `0044D460` | `0044D420` | `0044D4A0` | `00539270` | - | none |
| `82`<sub>h</sub> | `0044CC10` | `00450480` | `0044DD00` | `00539320` | - | 617 / 161 |
| `83`<sub>h</sub> | `0044CC10` | `00450480` | `0044E530` | `00539320` | - | 80 / 48 |
| `84`<sub>h</sub> | `0044ED90` | `0044ED50` | `0044EDD0` | `00539980` | - | 1,972 / 501 |
| `85`<sub>h</sub> | `0044F930` | `0044F8F0` | `0044F970` | `005393B0` | - | 78 / 42 |
| `86`<sub>h</sub> | `004504C0` | `00450480` | `00450550` | `005394A0` | - | 115 / 87 |
| `87`<sub>h</sub> | `00451140` | `00450480` | `00451180` | `00539560` | - | 175 / 54 |
| `88`<sub>h</sub> | `00451890` | `00451850` | `004518D0` | `00539610` | - | 41 / 31 |
| `89`<sub>h</sub> | `004524C0` | `00452480` | `00452540` | `00539740` | - | 36 / 8 |
| `8A`<sub>h</sub> | `00453110` | `004530D0` | `00453150` | `00539870` | - | none |
| `8B`<sub>h</sub> | `004548F0` | `004548B0` | `00454930` | `00539A60` | - | 1 / 1 |
| `8C`<sub>h</sub> | `00455390` | `0045B260` | `00455540` | `00539B30` | - | 7,509 / 910 |
| `8D`<sub>h</sub> | `00455D70` | `00455D30` | `00455DB0` | `00539C10` | - | 1,170 / 553 |
| `8E`<sub>h</sub> | `004566E0` | `004566A0` | `00456720` | `00539CF0` | - | 136 / 74 |
| `8F`<sub>h</sub> | `00457E10` | `00456EF0` | `00456F30` | `00539DA0` | - | 1,663 / 383 |
| `90`<sub>h</sub> | `00457E10` | `00456EF0` | `00457FE0` | `00539DA0` | - | 765 / 313 |
| `91`<sub>h</sub> | `00459420` | `004593E0` | `004595C0` | `00539E90` | - | 12 / 7 |
| `92`<sub>h</sub> | `0045A050` | `0045A010` | `0045A200` | `00539E90` | - | 84 / 45 |
| `94`<sub>h</sub> | `00455390` | `0045B260` | `0045AEE0` | `00539B30` | - | 2,344 / 387 |
| `95`<sub>h</sub> | `00455390` | `0045B260` | `0045B2A0` | `00539B30` | - | 456 / 226 |
| `96`<sub>h</sub> | `00453CB0` | `00453C70` | `00453CF0` | `00539980` | - | 268 / 75 |
| `97`<sub>h</sub> | `00455390` | `0045B260` | `0045BAD0` | `00539F80` | - | none |

The band shares handlers across types, so a type here often selects a variant rather than a class:

- `80`<sub>h</sub>, `82`<sub>h</sub> and `83`<sub>h</sub> share birth, update and setup and differ in their draw.
- `86`<sub>h</sub> and `87`<sub>h</sub> also use the update `00450480`.
- `8C`<sub>h</sub>, `94`<sub>h</sub>, `95`<sub>h</sub> and `97`<sub>h</sub> share birth and update; the first three also share the setup.
- `8F`<sub>h</sub> and `90`<sub>h</sub> share birth, update and setup; `91`<sub>h</sub> and `92`<sub>h</sub> share the setup; `84`<sub>h</sub> and
  `96`<sub>h</sub> share the setup.
- `93`<sub>h</sub> and `98`<sub>h</sub>–`9F`<sub>h</sub> have no arm.

### Types `A0`<sub>h</sub> to `AB`<sub>h</sub>

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `A0`<sub>h</sub> | `00460B80` | `00460B40` | `00460BC0` | `0053A6F0` | - | none |
| `A1`<sub>h</sub> | `00461090` | `00461050` | `00461270` | `0053A790` | `00461250` | 504 / 343 |
| `A2`<sub>h</sub> | `00462480` | `00462440` | `00462540` | `0053A840` | - | 6,303 / 2,018 |
| `A3`<sub>h</sub> (sub) | `00524800` | `005247C0` | `00524A50` | `0054EE70` | `00524A10` | 447 / 131 |
| `A4`<sub>h</sub> (sub) | `005222D0` | `00522290` | `00522300` | `0054EA70` | - | none |
| `A5`<sub>h</sub> | `004633A0` | `00463360` | `00463460` | `0053A900` | - | 36 / 20 |
| `A6`<sub>h</sub> (sub) | `00524D70` | `00524D30` | `00524E30` | `0054EED0` | - | 359 / 178 |
| `A7`<sub>h</sub> (sub) | `005269B0` | `00526970` | `00526A10` | `0054F1B0` | - | 14 / 14 |
| `A8`<sub>h</sub> (sub) | `00527110` | `005270D0` | `005271D0` | `0054F350` | - | 367 / 159 |
| `A9`<sub>h</sub> (sub) | `00528090` | `00528050` | `00528150` | `0054F520` | - | none |
| `AA`<sub>h</sub> (sub) | `00528AF0` | `00528AB0` | `00528B50` | `0054F700` | - | 3 / 3 |
| `AB`<sub>h</sub> (sub) | `0052BFB0` | `0052BF70` | `0052C070` | `0054FE00` | - | 7 / 4 |

`A1`<sub>h</sub>, `A2`<sub>h</sub> and `A5`<sub>h</sub> are, with `40`<sub>h</sub>, `41`<sub>h</sub> and `D0`<sub>h</sub>, the definition types whose emitters
are drawn even when the instance's flag byte `+36A`<sub>h</sub> bit 0 is clear (the runtime page).

### Types `D0`<sub>h</sub> and `D1`<sub>h</sub>

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `D0`<sub>h</sub> | `00464F20` | `00464F10` | `00465680` | `0053A9D0` | `00465120` | 1,437 / 544 |
| `D1`<sub>h</sub> | `003D9040` | `003D9000` | `0016D6A0` | `0053AA30` | `003D90C0` | 765 / 406 |

- `D0`<sub>h</sub> changes how chosen characters look. Its apply `00465690` works from the flag word `+232`<sub>h</sub>
  (`004656DB`) and passes each chosen character to `00465CD0`, which it calls from eight sites. `D0`<sub>h</sub>
  and `41`<sub>h</sub> share the update `00464F10`.
- With bit 0 of `+232`<sub>h</sub> set the apply scales the scene colour per channel,
  `020926C0 x= 1 + w x (c / 128 - 1)`: `c` is the four colour bytes of `0042FDB0([+20h] + 80h, [+44h])`
  and `w` the alpha byte of the `002F1F40` fade over 128 while bit 7 is set, else 0; bit 7 is then cleared
  (`004656C6`-`0046578F`).
- `D1`<sub>h</sub> draws nothing (its draw is `0016D6A0`). Its update tail `003D92C0` publishes the element at
  `02092628` (`003D9698`); `00258B90`, which the field frame runs with its camera work
  ([frame update order](../Engine-Core/frame-update-order.md)), copies it into the block at
  `02096FA0` and clears the pointer (`00258C3B`–`00258D4D`).

- That copy is then turned into a camera by `003D9150` (from `00258B90`), unless the half-rate
  cadence test and `001EDAD0` hold it back: for the copy's key `+330`<sub>h</sub> it takes the eye and target
  (`+230`<sub>h</sub> / `+240`<sub>h</sub>, 32 bytes a key, swapped when the definition's byte `+240`<sub>h</sub> is set) and the
  roll (`+320`<sub>h</sub>, 4 bytes a key) and fills the camera `02096ED0` with them through `003CC080`.
- With the definition's byte `+241`<sub>h</sub> bit 0 set it uses `003CC970` instead, which first pulls the
  eye out of the map's collision (`0026E500`, `00230B60`). The field of view is the key's `+328`<sub>h</sub>,
  with `1 / tan(fov / 2)` at `02096EE0`. It writes the camera into camera record 4, or 6 when `+241`<sub>h</sub> bit 2 is set, with mode 3 and its active
  bit raised (`0025A2C0`, `0025A500`, `0025A520`); see [scripted camera](scripted-camera.md).

### The kind-`54`<sub>h</sub> mesh record

A mesh is an `B00`<sub>h</sub> record of kind `54`<sub>h</sub>: a `190`<sub>h</sub>-byte object built by `004354E0` and loaded by
`00436D00(object, payload)`, which first calls the kind's destroy body `004352C0` (`00436D20`). The loader copies each array into a new block unless the object's `+18C`<sub>h</sub> has bit
`8`<sub>h</sub>, in which case it keeps a pointer into the stream (`00436D98`–`00436DDE`).

The id bytes name kind-`52`<sub>h</sub> texture records: each is resolved through
`003AA280(key, 52h, id)` with the record's own key word, into the handle array at `+184`<sub>h</sub>
(`004370B8`–`004370FE`).

## Layouts

Kind-`54`<sub>h</sub> payload (from `00436D00`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | flags: bits 0-2 -> object `+18C`<sub>h</sub>; bit 0 adds the index lists |  |
| `02`<sub>h</sub> | `u16` | triangles | -> +`10`<sub>h</sub> |
| `04`<sub>h</sub> | `u16` | quads | -> +`12`<sub>h</sub> |
| `06`<sub>h</sub> | `u16` | positions | -> +`14`<sub>h</sub>, array +`20`<sub>h</sub>, 16 bytes each, w set to 1.0 |
| `08`<sub>h</sub> | `u16` | vectors | -> +`16`<sub>h</sub>, array +`24`<sub>h</sub>, 16 bytes each |
| `0A`<sub>h</sub> | `u16` | 4-byte entries | -> +`18`<sub>h</sub>, array +`28`<sub>h</sub> |
| `0C`<sub>h</sub> | `u16` | 8-byte entries | -> +`1A`<sub>h</sub>, array +`2C`<sub>h</sub> |
| `0E`<sub>h</sub> | `u16` | id bytes | -> +`1C`<sub>h</sub>, ids +`180`<sub>h</sub>, handles +`184`<sub>h</sub> (8 bytes each) |
| `10`<sub>h</sub> | `u16` | 20-byte records | -> +`1E`<sub>h</sub>, copied inline to +`30`<sub>h</sub> |
| `12`<sub>h</sub> | `positions,` | vectors, | 4-byte, 8-byte and 20-byte arrays in that order; with flags bit 0, two index lists of 6 x triangles + 8 x quads bytes (+`170`<sub>h</sub>, +`174`<sub>h</sub>); then one byte per triangle and quad (+`188`<sub>h</sub>); then the id bytes |

Element fields the verified draws read:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `044`<sub>h</sub> | `i32` | track frame, the time every track is sampled at |  |
| `1F0`<sub>h</sub> | `u32` | colour |  |
| `230`<sub>h</sub> | `vec` | point 1 (types `01`<sub>h</sub>, `03`<sub>h</sub>); `+240`<sub>h</sub> point 2 (`03`<sub>h</sub>) |  |
| `294`<sub>h</sub> | `i32` | mesh index (`05`<sub>h</sub>) |  |

Definition fields the verified draws read:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `030`<sub>h</sub> | `blend` | track | (mode 6) and alpha percent |
| `044`<sub>h</sub> | `u8` | element type |  |
| `049`<sub>h</sub> | `u8` | bits 5-7 blend mode |  |
| `190`<sub>h</sub> | `mesh-index` | track | (`05`<sub>h</sub>); +`590`<sub>h</sub> u8 bit 4 mesh-index mode; +`5A0`<sub>h</sub> u32[32] mesh handles |

## Shipped data

| Fact | Value |
|---|---|
| element definitions | 48,868 `A00`<sub>h</sub> records over 4,229 streams, 55 distinct types |
| types with code and no shipped definition | `03`<sub>h</sub>, `07`<sub>h</sub>, `08`<sub>h</sub>, `70`<sub>h</sub>, `81`<sub>h</sub>, `8A`<sub>h</sub>, `97`<sub>h</sub>, `A0`<sub>h</sub>, `A4`<sub>h</sub>, `A9`<sub>h</sub> |
| most used | `02`<sub>h</sub> 7,523; `8C`<sub>h</sub> 7,509; `A2`<sub>h</sub> 6,303; `05`<sub>h</sub> 5,204; `94`<sub>h</sub> 2,344; `40`<sub>h</sub> 2,254 |
| used once | `8B`<sub>h</sub> |
| kind-`54`<sub>h</sub> records | 2,733; flags `07`<sub>h</sub> and key 0 in all; slot bytes 1 to 15 and 20 |
| kind-`54`<sub>h</sub> sizes | the layout above plus 0 to 15 bytes of padding fills every record's chunk |
| kind-`54`<sub>h</sub> arrays | 20-byte count 0 in all; 8-byte count equal to the 4-byte count in all |
| kind-`54`<sub>h</sub> id bytes | 0 in 2,275 records, 1 in 444, 2 in 14; all 472 name a kind-`52`<sub>h</sub> record of key 0 in the same stream |
| type-`05`<sub>h</sub> definitions | 5,204; mesh slots filled at `+570`<sub>h</sub>: one in 4,304, two in 898, three in 1, none in 1 |
| type-`05`<sub>h</sub> mesh ids | all 6,103 equal the slot byte of a kind-`54`<sub>h</sub> record in the same stream |

The per-type counts are in `effect-element-types-type_census.tsv`, which matches this census row
for row. `effect-element-types-effect-type-authored-usage.tsv` is an earlier, smaller census whose
counts this page supersedes. `effect-element-types-effect-mesh-54-records.tsv` (2,252 rows) and
`effect-element-types-effect-mesh-54-element05.tsv` (5,164 rows) list the mesh records and type-`05`<sub>h</sub>
definitions of the `.efx` files one per row.

## Operations

One base update and one type tail per live element per simulation step; one draw call per drawn
element per frame; one apply per registered element (`40`<sub>h</sub>, `41`<sub>h</sub>, `42`<sub>h</sub>, `D0`<sub>h</sub>) per drawn
frame.

## State

The registry `02ADBFE0` (128 slots), the light pool behind `003AB960`, the pools at `[02B404E0]` and
`02B4D7D0`, the blend pair `02AEE900` / `02AEE908`, and the published element `02092628`.

## Modding notes

- A definition's type byte decides everything; a type without an arm in a table gets no behaviour
  for that method, and a draw arm that is `0016D6A0` draws nothing.
- Point and line blending comes from definition byte `+49`<sub>h</sub> bits 5–7; mode 6 takes the blend word
  from the `+30`<sub>h</sub> track, so that track then serves as both alpha percent and blend.
- A type-`05`<sub>h</sub> mesh index of 32 or more falls back to 0, and its definition holds 32 handles.
- The registry holds 128 elements of types `40`<sub>h</sub>, `41`<sub>h</sub>, `42`<sub>h</sub> and `D0`<sub>h</sub>; `00377190` returns 0
  when it is full.

## Related

- [Effect element runtime](effect-element-runtime.md): the method tables, birth, update, release and
  the draw passes.
- [Effect files](effect-files-efx-efb.md): the `A00`<sub>h</sub> and `B00`<sub>h</sub> records.
- [Character lighting and shadows](character-lighting-and-shadows.md): the light pool `40`<sub>h</sub> uses.
- [Authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md): the tracks
  every type samples.
- [PS2 VIF1 / VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the packet path
  many draw methods end in.
