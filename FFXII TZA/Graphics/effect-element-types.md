---
title: "Effect element types: the handlers of every element type, what the verified types draw or change, and the kind-0x54 mesh record"
kind: "system"
category: "Graphics"
addresses: "0x002F2D60, 0x002F2530, 0x00500470, 0x00442550, 0x0039C550, 0x004427D0, 0x0039C4C0, 0x0039D890, 0x0039D970, 0x0039D5A0, 0x0039D6C0, 0x01EFAC20, 0x02AEE900, 0x02AEE908, 0x004490D0, 0x00501A50, 0x00502280, 0x00502EA0, 0x004434D0, 0x00444340, 0x00449AB0, 0x004355D0, 0x00377190, 0x02ADBFE0, 0x00377230, 0x004640A0, 0x003AB960, 0x0047BE20, 0x003D7FF0, 0x00465690, 0x00465CD0, 0x003D92C0, 0x02092628, 0x00436D00, 0x003AA280"
---

## What the player sees

Each piece of an effect has a type that decides what it is: a dot of light, a streak, an animated
sprite, a textured ring or dome, a model mesh, a trail of sprites, or something that draws nothing
itself but changes the scene, such as a light on the characters or a colour change on chosen
characters. The type is authored in the effect file, one byte per element definition.

## How it works

### Where the type comes from

An element definition is an `0xA00` record; its header byte `+0x0E` is the type, copied to the
definition's `+0x44` by `0x003A9A70` and to the element's byte `+0` at birth by `0x002F2D60`
(`0x002F30F2`–`0x002F30F6`). How the five method tables dispatch on it, and when each method runs, is on
[effect element runtime](effect-element-runtime.md); the record grammar is on
[effect files](effect-files-efx-efb.md).

The tables give 65 types an arm, with 248 distinct handlers. Types `0x00`–`0x0A`, `0x40`, `0x41`,
`0x60`–`0x67`, `0x80`–`0x97`, `0xA0`–`0xA2`, `0xA5`, `0xD0` and `0xD1`, except `0x09`, `0x63`, `0x64`
and `0x93`, are main-range types (47);
`0x42`, `0x68`–`0x6B`, `0x70`–`0x74`, `0xA3`, `0xA4` and `0xA6`–`0xAB` are reached only through the
sub-range tables (18); `0x6C`–`0x6F` have no arm in either range (`0x0043EBF0`, byte map `0x0043ECC4`). The
full decode is in [`effect-element-types-effect-type-methods.tsv`](effect-element-types-effect-type-methods.tsv).

### Columns of effect-element-types-effect-type-methods.tsv

One row per type `0x00` to `0xD1`, 210 rows; each other column is one dispatcher, named by its role and address.
The type is the element's byte `+0`, or the definition's byte `+0x44` where the name says `(+0x44)`; `walk` indexes
its table with the type minus 1, the `sub-` dispatchers start at `0x42` and `seventh` at `0x40`.

| Column | Holds |
|---|---|
| `step 0x002F3BC0`, `update 0x002F3910`, `walk 0x002F4020 (type - 1)`, `setup 0x005004C0 (+0x44)` | the main-range handlers: the function the type's arm reaches with its first direct call or jump to another function; `default` when the type takes the table's most common arm; `-` when the type is outside the table |
| `sub-step 0x0043EBF0`, `sub-setup 0x00538910 (+0x44)`, `sub-update 0x0043EAB0`, `sub-walk 0x0043ED30` | the same for the sub-range dispatchers, whose tables start at type `0x42`; `-` on the 104 types below `0x42` or above the table |
| `seventh 0x002F31C0`, `sub-seventh 0x0043E9C0` | the same for the seventh method and its sub-range twin |

Every birth method except `0x70`'s calls the base birth `0x002F2D60`, and every update method except
`0x70`'s calls the base update `0x002F2530`. Most updates add a type tail: type 1's `0x004424E0` is
`0x002F2530` then `0x00442600`. Types `0x41` and `0xD0` share `0x00464F10`, a jump to the base alone. The
tails end in the cull, release and spawn fork of the runtime page.

The base setup is `0x00500470(definition, delta)`: it rebases the two encoded dwords at each of `+0x00`,
`+0x10`, `+0x20` and `+0x30` of the definition with `0x004304F0` and returns `definition + 0x80`
(`0x0050047F`-`0x005004AA`).

In the tables below "Authored" is the number of `0xA00` definitions of the type over every shipped
stream, then the number of archive files holding them; a sub-range type's handlers are its
sub-range ones.

### The type names

`0x002FBA60(type)` returns the name of a type from a byte table at `0x002FBDEC` and a list of strings
from `0x00D0F9F0`; any other type below 256, and any type above, gives `"NONE TYPE NAME"` (`0x00D10150`).
The type-1 context builder `0x002FC4A0` prints these names for the element types of the stream it has
parsed while `0x022BE950` is set. The prefix is `TsElementType_` unless the row says `Nh`:

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

Type `0xA1`, VLENSFLARE, drives the eight lens-flare slots at `0x02ADBB40`.

While it parses a type-1 stream, `0x002FC4A0` records every definition's type. It clears `0x914` bytes from `0x02EC29C0`
(`0x002FC570`), sets `0x02EC32C4` and `0x02EC32CC` to 1 (`0x002FC5BC`, `0x002FC5C7`), runs the parse `0x003EDAD0` (`0x002FC5D2`)
and then clears `0x02EC32C4` (`0x002FC5E7`).

While both words are set, the setup dispatcher `0x005004C0` appends the
definition's type byte `+0x44` to the 512 dwords at `0x02EC29C0` and adds 1 to the count `0x02EC32D0`. When 512 are
recorded it clears `0x02EC32CC` instead (`0x005004C0`-`0x00500501`). With `0x022BE950` set, `0x002FC4A0` then prints the
count, each recorded type with its name (`0x002FBA60`) and each distinct type once (`0x002FC5F5`-`0x002FC7E7`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EC32D0` | `u32` | 0 (zero-filled tail) | the number of definition types recorded at `0x02EC29C0` during the last type-1 parse, at most 512 | `0x002FC4A0`, 0 (its clear from `0x02EC29C0`, `0x002FC570`; the 8-byte store at `0x02EC32CC`, `0x002FC5C7`); `0x005004C0`, +1 (`0x005004F9`) | `0x005004C0` (`0x005004DC`, `0x005004F9`); `0x002FC4A0` (`0x002FC667`, `0x002FC6A3`, `0x002FC70D`, `0x002FC751`, `0x002FC7B7`) |
| `0x02EC32C0` | `u32` | 0 (zero-filled tail) | the id word `+0x20` of the type-1 context being parsed | `0x002FC4A0`, 0 (its clear from `0x02EC29C0`, `0x002FC570`), then the id (`0x002FC57A`) | no RIP-relative instruction reads it |
| `0x02EC32C8` | `u32` | 0 (zero-filled tail) | 1 once a type-1 parse has run | `0x002FC4A0`, 0 (its clear, `0x002FC570`), then 1 after the parse (`0x002FC5DD`) | no RIP-relative instruction reads it |

### Types 0x00 to 0x0A

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x00` | `0x002F2D60` | `0x002F2530` | - | `0x00500470` | - | 1,446 / 458 |
| `0x01` | `0x00442520` | `0x004424E0` | `0x00442550` | `0x00538A60` | - | 476 / 370 |
| `0x02` | `0x00448DE0` | `0x00448D70` | `0x004490D0` | `0x00538AB0` | - | 7,523 / 1,141 |
| `0x03` | `0x004427A0` | `0x00442760` | `0x004427D0` | `0x00538B80` | - | 0 / 0 |
| `0x04` | `0x00445310` | `0x004452D0` | `0x004453D0` | `0x00538C80` | - | 173 / 81 |
| `0x05` | `0x00449970` | `0x00449930` | `0x00449AB0` | `0x00538DB0` | - | 5,204 / 1,115 |
| `0x06` | `0x00446F60` | `0x00446F20` | `0x00447020` | `0x00538EB0` | - | 25 / 9 |
| `0x07` | `0x00447E10` | `0x00447DD0` | `0x00447ED0` | `0x00538EB0` | - | 0 / 0 |
| `0x08` | `0x0044A5F0` | `0x0044A5B0` | `0x0044A620` | `0x00539030` | - | 0 / 0 |
| `0x0A` | `0x0044BA80` | `0x0044BA40` | `0x0044BAC0` | `0x00539170` | - | 40 / 39 |

- `0x00` has no draw method: it moves and fires spawn slots only.
- `0x01` is a point. Its draw sets `0x02AEE908` to the integer track at definition `+0x30` and
  `0x02AEE900` to definition byte `+0x49 >> 5`, then calls `0x0039C550` (`0x004425B2`–`0x004425E8`), which
  projects the point and emits a one-vertex `GiPrim` (kind 0 in the blended emitter, `0x0039DA7A`).
- Before that, the point's draw `0x00442550` hands the element's `+0x244` to `0x0039B620`, which adds the
  instance's depth offset and stores the sum at `0x02AEE7F0`. It sets w `+0x23C` to 1.0 and takes the colour
  as `0x002F1F40` of the position `+0x230` times the colour `+0x240` (`0x0026EE00`, `0x00442567`–`0x004425AA`). The
  track is sampled at the element's `+0x44` and stored sign-extended to 64 bits (`0x004425B6`–`0x004425C6`).
- `0x0039C550(point, colour)` installs `0x02AEECB0` (`0x0039B550`) and draws nothing when `0x00399600` rejects the
  point (`0x0039C589`). The draw's test of the type byte `+0` against 0 (`0x00442556`) is never met: its one
  caller, the draw dispatcher `0x002F4020` (`0x002F4129`), calls `0x00442550` for type 1 only.
- `0x03` is a line: its draw calls `0x0039C4C0` (`0x004427D0`), which projects both ends, drops the line
  when either end is rejected, and emits a two-vertex `GiPrim` of kind 1 (`0x0039C4EB`–`0x0039C52B`,
  `0x0039D769`, `0x0039D83C`).
- The line's draw `0x004427D0` works like the point's with two ends: the depth from `+0x258` (`0x0039B620`),
  w 1.0 at `+0x23C` and `+0x24C`, the same blend pair from definition `+0x30` and `+0x49`, and one colour
  per end, `0x002F1F40` of `+0x230` times `+0x250` and of `+0x240` times `+0x254` (`0x004427F6`–`0x00442890`).
- It calls `0x0039C4C0(+0x230, +0x240, colour 1, colour 2)` (`0x004428C3`), which installs `0x02AEECB0`
  (`0x0039B550`) before projecting. Its test of the type byte `+0` (`0x004427E5`) is never met either: the
  dispatcher calls it for type 3 only (`0x002F4146`).
- `0x02` and `0x0A` draw sprite frames through `0x00501A50` and `0x00502280` (`0x004490D0`, `0x0044BAC0`).
  Both frame drawers pick a row of a kind-`0x50` record with `0x00502EA0`.
- `0x04`, `0x06` and `0x07` share the grid emitters `0x004434D0` and `0x00444340`, which all three draws
  call.
- `0x05` draws a mesh; see "Type 0x05 and the mesh record" below.
- `0x06` and `0x07` share one setup, `0x00538EB0`.

### The point and line blend modes

`0x02AEE900`, definition byte `+0x49` bits under mask `0xE0`, picks the emitter. Mode 0 builds the primitive and
submits it at once (`0x0039D890` for a point, `0x0039D5A0` for a line). Modes 1 to 7 append a draw-list
entry first and set the primitive's blend word: `0x01EFAC20[mode]`, or in mode 6 the `+0x30` track
value from `0x02AEE908` (`0x0039DA89`–`0x0039DAAC`, `0x0039D859`–`0x0039D875`).

| Mode | Blend word |
|---:|---|
| 0 | no blend word: the immediate emitter |
| 1 | `0x48` |
| 2 | `0x42` |
| 3 | `0x44` |
| 4 | `0x49` |
| 5 | `0x46` |
| 6 | the `+0x30` track value |
| 7 | `4` |

### The polygon emitters

Every effect point, line and polygon reaches the renderer through a pair of emitters: one submits
its command at once (blend mode 0, through `0x0020E630(command, 2)`), the other files it on the draw
list first and sets the blend word as above (modes 1 to 7). The blended ones fill the `0x28`-byte
entry the same way: the smallest of the vertices' 24-bit depths as the key `+8`, the pass nibble
`0x02AEE910` in the bits under mask `0xF0000000`, and the flag word `+0x20` = `0x02AEF41C × 4` (`0x003A2C70`), plus `2` when
`0x0024E460` returns 1 or `0x02AEF418` is set (`0x0039DD60`, `0x0039EC30`).

The point emitter `0x0039D970` is the exception for the key: it takes only the 16-bit word at the
vertex's `+4`, the low 16 bits of the depth (`0x0039D9B5`), where the line emitter `0x0039D6C0` keeps 24 bits
of each end and the smaller one (`0x0039D6FD`-`0x0039D724`). The blended point and line emitters clear the
entry's `+0x00` and `+0x10` and store the command at `+0x18`; `+0xC` is 0 for the point and 1 for the line and quad
emitters (`0x0039D9CC`, `0x0039D736`, `0x0039ECD6`). The point and line emitters append without comparing the
count `0x02F8F2C6` with the list's size (`0x0039DA05`, `0x0039D775`).

Each emitter takes vertices that the translated vector routines have already projected into the GS
form and converts them back with `0x0039CDC0(points, out, n)`. It reads each vertex as two 16-bit
coordinates in sixteenths of a pixel and a 24-bit depth, clamps the depth to `[0x02AEEBA0]` ..
`[0x02AEEBA4]` (`0x0039CE70`, `0x0039CE78`), multiplies the vertex by the matrix `0x02AEEB20` (`0x00202B70`),
divides by w, and scales x by the 16:9 factor `0x0017FFD0` when `0x0024E640` returns 1. `0x0039CF10` does
the same for vertices that are already floats, without the depth clamp.

Most emitters fill a `GiPrim` (`0x008642A0`, which returns the command plus 8); the blended textured
quads use a `GiPolyGT4T` (`0x00864D10`) or a `GiSprite` (`0x008647C0`) instead.

| Shape | Immediate | Blended | Vertices | Kind | Command | Called from |
|---|---|---|---:|---:|---|---|
| point | `0x0039D890` | `0x0039D970` | 1 | 0 | `GiPrim` | `0x0039C550` |
| line | `0x0039D5A0` | `0x0039D6C0` | 2 | 1 | `GiPrim` | `0x0039C4C0` |
| triangle, vertex colours | `0x0039E6B0` | `0x0039E820` | 3 | 3 | `GiPrim` | `0x004355D0`, `0x00437130`, `0x00438860` |
| quad, vertex colours | `0x0039EA70` | `0x0039EC30` | 4 | 4 | `GiPrim` | the three above, `0x004434D0`, `0x00444340` |
| triangle, textured | `0x0039F2B0` | `0x0039F4B0` | 3 | 3 | `GiPrim` | `0x004355D0`, `0x00437130`, `0x00438860` |
| quad, textured | `0x0039F780` | `0x0039F9F0` | 4 | 4 | `GiPrim`; blended `GiPolyGT4T` | the five above |
| quad, one colour per row | `0x0039F140` | `0x0039EEF0` | 4 | 4 | `GiPrim` | `0x0039C770` |
| sprite | `0x0039DAD0` | `0x0039DD60` | 4 | 4 | `GiPrim` | `0x0039C5D0` |
| sprite, float path | `0x0039E420` | `0x0039E0C0` | 4 | 4 | `GiPrim` | `0x0039C6B0` |
| sprite, fixed UVs | `0x003A0870` | `0x003A0AA0` | 4 | 4 | `GiPrim`; blended `GiSprite` | `0x0039CCB0` |
| ribbon segment, colour pair | `0x003A0370` | `0x0039FD20` | 4 | 4 | `GiPrim`; blended `GiPolyGT4T` | `0x0039C800` |
| ribbon segment, colour lists | `0x003A05F0` | `0x003A0040` | 4 | 4 | `GiPrim`; blended `GiPolyGT4T` | `0x0039C800` |

The four point and line emitters write each vertex colour as four floats from the colour word's bytes,
in byte order, at `[+0x10]` of the pointer `0x008642A0` returns (`0x0039D8E7`-`0x0039D936`,
`0x0039D5E4`-`0x0039D689`). They set `+0x40` to the kind and `+0x48` to 0, and `+0x44` to 1 in the blended
emitters and 0 in the immediate ones. The point emitters also set the dword `+0x50` to 0 (`0x0039D8DF`,
`0x0039DA20`), which `0x008642A0` sets to 1 (`0x008642FC`); the line emitters leave it at 1.

"Kind" is the primitive number the `GiPrim` carries; its execute `0x00863D80` looks it up in the
eight-entry table `0x01F44D20` (0, 1, 6, 2, 3, 4, 6, 6) and passes the result to the device's draw
slot `+0x20`. The callers `0x004355D0`, `0x00437130` and `0x00438860` are the mesh composers of type
`0x05`, and `0x004434D0` and `0x00444340` the grid emitters of types `0x04`, `0x06` and `0x07`. Their
texture coordinates pass through `0x0039B840` or `0x0039B860`, both jumps to `0x0039B880`, which adds the
offset pair its fifth argument points at to each coordinate and multiplies it by the vertex's `q`.

`0x004355D0` returns 1 without composing anything for a kind-7 effect `0x200`–`0x23F` drawn while the pass id
is 0 (`0x0024E410`) while the debug console's "Enable VFX Display" row (`+0xAC0` of `[0x01F81428]`,
`0x001D50D0`) holds 2: `0x00180100` answers whether that row is not 2.

### The sprite and ribbon front ends

The sprite drawers `0x00501A50` and `0x00502280` (types `0x02` and `0x0A`) reach the quad emitters
through two front ends: while bit `0x40` of the request's byte `+0x46` is clear, bit `0x1` picks between
them (`0x00501A50`).

- `0x0039C5D0` asks `0x0024D330` first. For 1 it installs the matrix `0x02AEECB0` (`0x0039B550`), projects
  the four corners with `0x00399B80`, which returns non-zero when a corner falls outside, multiplies
  each texture coordinate by its corner's `q` (`0x0039B780`), and calls the sprite pair. For 0 it
  hands the call to `0x0039C6B0`, which projects with the float routine `0x0039A770` and uses the
  float-path pair.
- `0x0024D330` returns 0 only when the current context's byte `+0` is 3 and the effect ticket its
  word `+4` names (`0x02EBCD80`, `0x38` bytes a slot) has effect number `0x34` at `+0x30`. `0x003B33D0`
  checks the ticket id against the slot and returns that number, or −1 for a stale id.
- `0x0039CCB0` projects the corners one at a time (`0x00399B10`, which calls `0x00399600` per point and
  stops at the first rejected one) and passes the texture coordinates through unchanged.

Type `0x08`'s draw `0x0044A620` builds a grid of (`+0x270` + 1) × (`+0x274` + 1) points. Untextured,
it draws each cell with `0x0039C770`, which projects two points from each of two rows with
`0x00399B10` and colours the quad with one RGBA word per row. Textured, it draws rows through
`0x00502160` → `0x0039C800`, the ribbon drawer, which walks a descriptor and draws one quad per
segment between two rails of points:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` |  | first rail, 16-byte points; segment i uses points i and i+1 |
| `+0x10` | `void*` |  | second rail |
| `+0x18` | `void*` |  | two RGBA words (first rail, second rail); with `+0x20`, one word per segment for the first rail |
| `+0x20` | `void*` |  | one RGBA word per segment for the second rail, or null |
| `+0x28` | `void*` |  | 8-byte texture coordinates per point of the first rail, or null for the rectangle below |
| `+0x30` | `void*` |  | the same for the second rail |
| `+0x38` | `f32[4]` |  | u0, v0, u1, v1 |
| `+0x48` | `f32` |  | added to every u after each segment |
| `+0x4C` | `f32` |  | added to every v after each segment |
| `+0x50` | `void*` |  | texture pair |
| `+0x58` | `i32` |  | segment count |
| `+0x5C` | `i32` |  | segments after which the rectangle starts again from `+0x38` |

The ribbon drawer skips a segment when either rail's pair of points is rejected by `0x00399B80`
(`0x0039C800`).

Element orientations come from `0x00398480(angles, out, order)`, which builds a rotation matrix from
three angles in one of six axis orders; type `0x08` passes the definition byte `+0x48` as the order
(`0x0044A7E0`). Orders 1 to 3 multiply three single-axis rotations (`0x003985B0`, `0x00398910`,
`0x00398C50`) in different orders; orders 0, 4 and 5 are written out in `0x00398DD0`, `0x00398A90` and `0x00398730`, which take
sine and cosine from the 32,768-step sine table `0x01F004E0`, the cosine as the entry a quarter turn on.

The direction helpers `0x003A2440`, `0x003A2570` and `0x003A2690` build an orthonormal matrix whose row 0,
1 or 2 is the normalised direction, with the other rows from cross products with the given up
vector (`0x003A27C0`, `0x00398390`), and write the derived up vector back.

### Sprite rows: 0x00502EA0

`0x00502EA0(record, index, mode)` returns the index-th row, among the rows of `0x90` bytes from
record `+0x10` whose byte `+0x70` has bit `0x1` set. Mode 0 first clamps the index to `[+0x3C] − 1`,
mode 1 takes it modulo `[+0x3C]`, mode 2 accepts it up to the row count `+0x38`, and any other mode
returns 0; no match returns 0 (`0x00502EA0`–`0x00502F21`).

### Sprite row helpers

A row names its texture and palette in three bytes: `+0x71` indexes the kind-`0x50` record's
texture handles (`+0x28`, kind `0x52`), `+0x72` names the palette source, a kind-`0x53` handle from
`+0x30` when bit `0x80` is set and the texture itself otherwise, and `+0x73` picks the palette slot.

The record in the file is read by `0x00502CB0`: a `u16` row count, the `u8` texture and palette counts, a `u32`, then
`0x70`-byte rows, then one slot byte per texture and per palette. The `u32` is the number of rows with bit `0x1`, in
all 4,321 records. The slot bytes name kind-`0x52` and kind-`0x53` records of key 0, all in the same stream.

A file row's last four bytes, `+0x6C` to `+0x6F`, land at `+0x70` to `+0x73`. Bit `0x1` of the flags makes the row
selectable by `0x00502EA0` (`0x00502EF3`). Bit `0x2` stops the row walks (`0x0050223A`, `0x00502BDE`) and is on the final
row of every record. The palette slot is 0 on all 6,998 rows, and a row without bit `0x80` has its texture index as
its source byte, so `0x005030F0` replaces the palette word only for the 1,234 rows with a palette source.

[`effect-sprite-records.tsv`](effect-sprite-records.tsv) has one row per record and
[`effect-sprite-rows.tsv`](effect-sprite-rows.tsv) one per row of each distinct content, with the selectors.
[`effect-sprite-row-values.tsv`](effect-sprite-row-values.tsv) has the same rows' other stored values.

`0x00502CB0` copies file bytes `+0x00` to `+0x63` to the same offsets and file `+0x64` to `+0x6B` to row `+0x68` to
`+0x6F` (`0x00502D68`), and does not write row `+0x64` to `+0x67`.

| Row bytes | Holds | Read at |
|---|---|---|
| `+0x00` to `+0x3F` | four corners, each x, y, z and w | copied whole (`0x00501C00`-`0x00501CD1`); the frame offsets are added to x and y, and bits `0x10` and `0x20` of the draw's byte `+0x46` negate every x and every y (`0x00501D20`-`0x00501D8A`) |
| `+0x40` to `+0x5F` | four texture coordinate pairs | the sprite drawer `0x0039CCB0` (`0x0050207F`); `0x00431830` subtracts the first pair from the last (`0x0043197E`-`0x00431993`) |
| `+0x60` to `+0x63` | a colour | passed to `0x0026EE00` (`0x00501DB7`, `0x00502866`) |
| `+0x68` to `+0x6F` | a blend word | stored in `0x02AEE908` with blend mode 6 when bits `0xE` of a mode byte are `0xC`: the draw's `+0x46` (`0x00501D8F`, `0x0050283F`) or the caller's record `+0x60` in `0x00502160` (`0x00502194`) |

On all 6,998 rows z is 0 and w is 1. The blend word is an entry of `0x01EFAC20` on every row: `0x80000000A8` on 3,512
rows, `0x48` on 2,553, `0x44` on 894, `0x42` on 37 and `0x49` on 2.

- `0x00502F30(record, n, first, count)` finds the `n`-th enabled row and returns its index and the
  number of rows up to the next enabled one; it fails for `n` above the row count `+0x38`.
- `0x005030F0(record, row, out)` copies the texture's 16-byte register pair (`+0x10`) and, for a
  texture of format 0 to 2 whose row has `+0x72` unlike `+0x71` or a non-zero `+0x73`, replaces
  the high 27 bits of its second word with the palette's address word (`+0x2C + 8 × slot` of a kind-`0x53` record, or
  `+0x24 + 8 × slot` of the texture).
- `0x00503000(record, colours, count, handle)` returns the palette colours for the record's first
  row: 16 or 256 entries by the source's format, from the kind-`0x53` record's `+0x20` or the
  texture's `+0xB0`, with its handle.
- `0x00502160(record, draw)` is type `0x08`'s row walk: from the row the draw names, it sets each
  row's texture registers as `0x005030F0` does, switches to blend mode 6 with the row's word `+0x68`
  when the draw's byte `+0x60` has the bits under mask `0xE` equal to `0xC`, and calls `0x0039C800`, until a row with
  `+0x70` bit `0x2` or a following row whose `+0x70` byte is non-zero.

### Draw-source blocks

Many types describe what they draw with `0xF0`-byte blocks inside their definition; type `0x04`'s
setup `0x00538C80` has four of them from `+0x2B0`. A setup prepares each with `0x00431770(block, base)`,
which rebases the track group at `+0x00` (`0x00430AF0`), the group at `+0x40` (`0x0042FCF0`) and the
offsets `+0x90`, `+0x94`, `+0xE0` and `+0xE4`, clears `+0xA9` unless `+0xAA` has bit `0x10` or `0x20`, binds
the source records (`0x00431610`) and returns the address after the block. `0x00431610` binds by the
source kind `+0xA0`; a number of 0 leaves the handle at 0:

| `+0xA0` | Records bound (`0x003AA280`) |
|---:|---|
| 1 | the kind-`0x54` mesh numbered `+0xA1` into `+0xB0` |
| 2 | the kind-`0x52` texture `+0xA2` into `+0xB4`; the palette `+0xA3` into `+0xB8`, kind `0x53` when bit `0x80` is set (number in the bits under mask `0x7F`), else kind `0x52` |
| 3 | the kind-`0x50` sprite rows `+0xA5` into `+0xBC` and the kind-`0x51` frame sequence `+0xA6` into `+0xC0` |

`0x003AA280(key, kind, number)` returns the first node of the record store `[0x02EBEF70]`, walked from the
head `+0` along the encoded links (`0x0020E600`), whose word `+0xC`, byte `+0xE` and byte `+0xF`, each
sign-extended, equal the three arguments, or 0 at the end of the list (`0x003AA28F`-`0x003AA2CD`).

The draws read the block back through `0x00431830`. For source kind 2 it returns the texture's
register word (`+0x10`) with the palette address of slot `+0xA4` in its high half; when the byte
`+0xD0` is set it instead derives a palette from the source palette with `0x00431B10(block + 0xD0,
…)`, 16 entries when the palette's byte `+0x10` is `0x80` and 256 otherwise, and puts that
palette's address there. For source kind 3
it steps the frame sequence (`0x005039A0`) and picks the row with `0x00502EA0`.

### Track values in other units

A track is 16 bytes: two key arrays (offsets `+0x00` and `+0x04`, counts `+0x0C` and `+0x0D`) of
8-byte keys whose value is at `+4`. `0x004314E0(track, frame)` reads it: 0 for an empty array, the one
key's value for a count of 1, `0x00431080` otherwise, and with both arrays the two results combined
by `0x00431350`.

A setup can rescale the stored values once. `0x00430A60(track, f)` multiplies every key value of
both arrays by `f`, `0x00431040(group, f)` does so for the three tracks of a group (`+0x00`, `+0x10`,
`+0x20`), and `0x00431580(track, n)` multiplies integer values by `n`. Type `0x03`'s setup `0x00538B80`
turns the group at `+0x80` from degrees to radians (`π/180`), divides the groups at `+0x100` and
`+0x140` by 100 and multiplies the integer track at `+0x180` by 100.

### Generated palettes

`0x00431B10(op, colours, n, frame, texture)` derives a palette from `n` source colours. It unpacks the
colours into the work area `0x02CA4EE0` (`0x003CD840`), reads the operation's track `op + 0x10` at
`frame` (`0x004314E0`), and runs the operation the kind byte `op + 0x00` names; any other kind
returns 0 and the source palette stays:

| Kind | Body | Fields it reads |
|---:|---|---|
| 1 | `0x0050AC20` | byte `+0x01`, mask `0x6` of `+0x03` |
| 2 | `0x00506B40` | words `+0x08` to `+0x0E`, bit `0x1` of `+0x03` |
| 3 | `0x005080A0` | words `+0x04`, `+0x06`, bit `0x1` of `+0x03` |
| 5 | `0x00509BB0` | only the track |
| 6 | `0x00507490` | words `+0x04`, `+0x06` |
| 7 | `0x00508C90` | bytes `+0x01`, `+0x02`, words `+0x04`, `+0x06` |

With bit `0x8` of `+0x03` set the operation gets `n − 1` and a flag instead of `n`. `0x003A9C10(work, n,
texture)` then
reserves room for the palette in the emulated GS memory (`0x002D81D0`, which can refuse), takes an
`n × 4 + 0x10`-byte block linked on the current record table's list `+0x10`, packs the colours into
it (`0x003D2B60`), writes them into the palette texture (`0x00183640`) and returns the GS address.

The draws of types `0x02`, `0x0A`, `0x84`, `0x85`, `0x88`, `0x89`, `0x8A`, `0x8B`, `0x96` and `0xA1`
call `0x00431B10` themselves; type `0x02`'s draw `0x004490D0` passes definition `+0x160` and the
palette of its first sprite row (`0x00503000`).

### Frame sequences: the kind-0x51 record

A kind-`0x51` record holds `+0x10` entries of 16 bytes at `+0x18`, read by `0x00503880` from a `u16` count and the
entries after it. An entry's byte `+8` is its opcode: 0 shows a frame for byte `+9` ticks, 1 jumps to the entry in
word `+0xC`, and 2 ends the sequence. Word `+0xA` is the sprite row. The floats at `+0` and `+4` are stored at the
draw's `+0x30` and `+0x34` and added to each corner's x and y (`0x004494DB`, `0x00501C18`, `0x00501C27`). No reader of
word `+0xE` is located yet.

The shipped entries have 939 shows and 2 jumps, each back to entry 0, and no opcode 2. Their floats and word `+0xE`
are 0. 109 of the 111 distinct contents end on a show, so the end of the list stops them. In 34 of the 6,208 pairs
of a sequence with the sprite record its owner names beside it, the sequence's largest row is at or above
`selectable_rows`, and there `0x00502EA0` applies its mode.

[`effect-frame-sequences.tsv`](effect-frame-sequences.tsv) has one row per record and
[`effect-frame-entries.tsv`](effect-frame-entries.tsv) one per entry of each distinct content.

`0x005039A0(sequence, time, mode)` returns the frame entry at `time`; at the end, mode 0
keeps the last frame, mode 1 starts over with the time reduced, and mode 2 returns 0.
`0x00503A80(sequence, cursor)` does the same from a four-byte cursor (entry, time, last frame,
mode) that it updates, for type `0x02`'s draw `0x004490D0`.

The texture source resolver `0x00431830` uses `0x005039A0` with mode bit `0x40` of the sub-record's word
`+0xAA`, then picks the sprite row from the frame's word `+0xA` with `0x00502EA0` and its registers
with `0x005030F0`.

### The mesh and sprite triangle emitters

Four emitters turn projected triangles into `GiPrim` commands of kind 5; the mesh draw and the
sprite frame drawers `0x00501A50` and `0x00502280` use them.

| Emitter | Texture | Filing |
|---|---|---|
| `0x0043D8F0(positions, colours, n)` | no texture | at once, `0x0020E630(command, 2)` |
| `0x0043DB90(positions, uv, q, textures, colours, n)` | `u / q`, `v / q`; texture pair at `+0x38`, `+0x48` | at once |
| `0x0043E440(positions, colours, n)` | no texture | draw-list entry |
| `0x0043DF80(positions, uv, q, textures, colours, n)` | as `0x0043DB90` | draw-list entry |

The colour bytes become floats. The two list emitters key the entry on the smallest of the three
vertices' 24-bit depth words, OR in the pass nibble, and set the primitive's blend word to
`0x01EFAC20[0x02AEE900]`, or to `0x02AEE908` in mode 6, as the point emitter does
(`0x0043DFCF`–`0x0043E012`, `0x0043E3EC`–`0x0043E401`; `0x0043E48E`–`0x0043E4D0`, `0x0043E760`–`0x0043E775`).

### Type 0x05 and the mesh record

`0x00449AB0` draws one mesh. When definition byte `+0x590` has bit `0x10` clear, the mesh index `+0x294`
is the integer part of the float track at definition `+0x190`, or 0 when that is not positive or
not below 32 (`0x00449DA7`–`0x00449DF9`). It publishes the blend pair as the point does and passes the
handle `[definition + 0x5A0 + index × 4]`, decoded, to the model composer `0x004355D0`
(`0x0044A11C`–`0x0044A15B`). The handles are kind-`0x54` records.

### How the composer prepares a mesh

`0x004355D0(object, state)` draws nothing for an object without bits `0x1` and `0x4` of `+0x18C`. It
first builds the mesh's vertices into the scratch block `[0x02AEED50]`:

- `0x00434CD0` when the state's `+0x1E8` is set: it blends each array of the object with the same
  array of the object at state `+0x48`, weights `1 − t` and `t` with `t` the float `+0x1EC`; state
  byte `+0x1F1` bits `0x10`, `0x20` and `0x40` copy the 4-byte, 8-byte and vector arrays unblended instead;
- `0x00435050` otherwise: it copies the arrays unblended.

Both call `0x00434C50(state, byte +0x1F1 & 7)`, which multiplies the state's matrix by `0x02AEEC30`
(mode 1), `0x02AEEC70` (mode 2) or `0x02AEEA60` (modes 4 and 5); mode 4 first turns the matrix toward
the point `0x02AEEAD0` from the position `+0x30` (`0x00434900`), and mode 5 turns it about one axis by
the `atan2` of the same direction (`0x00434A70`). Then they project the positions; a rejected mesh
draws nothing (`0x00399B80` at `0x00434ED9` and `0x0043526E`).

- With byte `+0x1F1` bit `0x8` and `0x0024E410` true, the projection is not tested and the first six
  (`0x00434CD0`) or four (`0x00435050`) projected vertices are overwritten with fixed screen values,
  one set for locale ids 1–6 (`0x00229E40`) and another for the rest.
- Byte `+0x1F1` at `0x80` or above hands the mesh to `0x00438860`; bit `0x8` hands it to `0x00437130`.
  Otherwise `0x004355D0` runs its own loop over the `+0x1F0` layers.

`0x00437130` is the same per-layer loop without one step: for a layer of mode 4, `0x004355D0` divides
the first float of the layer's pair at state `+0x50 + 8 × layer` by 1.15 and multiplies the second
by 1.15 (`0x00435D23`–`0x00435D49`), and `0x00437130` does not. In both, a layer of mode 5 emits flat triangles and quads, mode 1 textured
ones whose texture comes from the face's byte at `+0x188`, and any other mode textured ones with
the layer's texture; blend mode 0 files at once and any other mode through the draw list.

The composers share two helpers with the element types at `0x004434D0`, `0x00444340`, `0x004584E0` and
`0x004595C0`: `0x00394DA0(matrix, vector, out)` multiplies the vector by the matrix without its
translation, giving four floats, and `0x00394B70(vertices, indices, out, n)` adds, for each of `n`
indices into the 16-byte projected vertices, the vertex's screen position `x / 16 / 512 − 3.5` and
`y / 16 / 512 − 3.5625` to the next float pair of `out`.

### Types 0x40 to 0x42

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x40` | `0x00463FF0` | `0x00463FB0` | `0x00464090` | `0x0053AAC0` | `0x00464050` | 2,254 / 744 |
| `0x41` | `0x00464B30` | `0x00464F10` | `0x00464BC0` | `0x0053AB10` | `0x00464B80` | 425 / 310 |
| `0x42` (sub) | `0x0047BE20` | `0x0047BDA0` | `0x0047BFA0` | `0x0050C450` | `0x0047BF70` | 613 / 350 |

These types, with `0xD0`, act on the scene instead of drawing. Their births register the element in
the 128-slot registry at `0x02ADBFE0` (`0x20` bytes a slot, handle `serial << 8 | slot`, element at
`+8`) through `0x00377190`, whose only callers are those four births. Their draw methods only set a
bit: `0x00464090` sets bit `0x2` of `+0x248`, `0x00464BC0` bit `0x1` of `+0x23C`.

`0x00377190(element)` takes the first slot whose handle dword `+0x00` is 0 and returns 0 when all 128 are taken
(`0x003771A0`-`0x003771B5`). Otherwise it raises the count `0x02ADBFC0`, stores the element at `+8` and the handle at
`+0x00`, appends the slot at the tail of the live list (`0x02ADBFC8` and `0x02ADBFD0`, links `+0x10` and `+0x18`) and
returns the handle (`0x003771B6`-`0x00377223`).

The releases `0x00464050` (`0x40`), `0x00464B80` (`0x41`), `0x00465120` (`0xD0`) and `0x0047BF70` (`0x42`)
free the slot through `0x00377360(handle)`, which finds it in the registry's live list (head
`0x02ADBFC8`, tail `0x02ADBFD0`, links at `+0x10` and `+0x18`), lowers the count `0x02ADBFC0`, clears the
handle and unlinks it.

`0x00377230` walks the registry from `MainLoop_Draw` (`0x0022B268`) and the menu frame (`0x0022B940`),
checks visibility with the group gate and the per-instance gate (`0x00377292`–`0x003772A2`), and calls
the type's apply body: `0x004640A0` (`0x40`), `0x00464BD0` (`0x41`), `0x0047BD30` (`0x42`) and `0x00465690`
(`0xD0`) (`0x003772EA`–`0x00377336`).

The walk runs from the head `0x02ADBFC8` through `+0x18` (`0x00377236`, `0x0037733B`). It skips an element
whose `+0x224` is set while the cadence test returns 0 (`0x00377264`–`0x00377275`). Otherwise it makes the
element's instance current with `0x002F3860`, which takes the emitter's `+0x10`, or the element's `+0x18`
for type `0xF0`, and runs `0x0024ED80`. It then runs `0x0024C060` and ANDs the gates `0x0024D4E0(kind)` and
`0x0024D770(instance, 0)` (`0x0037727E`–`0x003772A7`).

Before each apply the walk stores that result: bit `0x2` of `+0x248` for `0x40`, bit `0x1` of `+0x23C`
for `0x41`, the whole byte `+0x238` for `0x42`, and bit `0x80` of the word `+0x232` for `0xD0`
(`0x003772D1`–`0x0037732F`). A type-`0xF0` arm calls `0x0046EDD0`, the vibration refresh in
[Timeline tracks](effect-element-runtime.md#timeline-tracks), without a store (`0x003772C2`–`0x003772CA`); the
registry never holds one, as its only filler `0x00377190` is called by the four births alone. Any other
type gets no call.

- `0x40` makes a light. `0x004640A0` fills a request and creates it with `0x003AB960` the first time,
  keeping the handle at `+0x244`, and updates it with `0x003AC920` afterwards (`0x00464387`–`0x004643A0`).
  Definition byte `+0x120` picks the request word: 1 gives `0x8001`, 2 gives `0x8006`, anything else
  `0x8002` (`0x004640C3`–`0x0046410A`). The pool is on [character lighting](character-lighting-and-shadows.md).
- `0x40`'s create test is `+0x244` = 0 (`0x00464387`), so when the pool is full and `0x003AB960` answers 0
  (`0x003AB985`), the next apply calls `0x003AB960` again.
- `0x41`'s apply keeps a record in the 64-entry pool of `0x60`-byte records at `[0x02B404E0]` through
  `0x003B4160`.
- `0x42`'s birth reads three floats at definition `+0x124`, `+0x128` and `+0x12C` and the track group
  at `+0x80`, and takes a slot in the 32-entry, `0x60`-byte pool at `0x02B4D7D0` through `0x003D7FF0`
  (`0x0047BE64`–`0x0047BF08`).
- The birth `0x0047BE20` returns 0 when the base birth `0x002F2D60` does (`0x0047BE38`). It reads the floats only
  when the current instance's kind byte is 10 or more; below that it uses 1.0, `[0x01DFE0BC]` and 1.0
  (`0x0047BE5F`–`0x0047BEA6`).
- The request holds the floats at `+0`, `+4` and `+8`, definition byte `+0x122` at `+0x0C`, the low seven
  bits of byte `+0x123` in `+0x0D` (bit `0x80` of `+0x0D` is not written), 1 at `+0x0E` and the image
  offset of `+0x80` (`0x0020E620`) at `+0x10` (`0x0047BEAE`–`0x0047BF04`).
- It keeps the pool handle at `+0x230` and the registry handle `0x00377190` at `+0x234`, calls
  `0x003D8D70(pool handle, 0)`, sets `+0x238` to 1, and calls `0x003D8DE0` with the parent's `+0x30`, or its own
  `+0x70` without a parent `+0x10`. It returns 1 (`0x0047BF10`–`0x0047BF53`).

- The `0x42` pool slots are named by `serial << 8 | slot`, checked at slot `+0x04`. `0x003D8300(handle)`,
  from the release `0x0047BF70`, `0x003E69A0` and `0x003E7140`, frees a slot: it lowers the count
  `0x02B4D7A0`, clears the handle and unlinks the slot from the list `0x02B4D7A8` / `0x02B4D7B0` (encoded
  links at `+0x08` and `+0x0C`).
- `0x003D8D70(handle, b)` stores byte `+0x3F` and `0x003D8DE0(handle, v)` the three floats
  `+0x10`–`+0x18`; the birth, the update and `0x003E6910` call both. `0x003D8DA0(mode)`,
  from the field camera's target read `0x003D9E20`, stores 1.0 for mode 1, 0.6 for mode 2 and 0
  otherwise at `0x02B4D7B8`; `0x003D8C30` also writes 1.0 there (`0x003D8D12`), and `0x003D83A0` is its only reader
  (`0x003D8BC3`).

### Types 0x60 to 0x74

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x60` | `0x0045BF50` | `0x0045BF10` | `0x0045BFB0` | `0x0053A120` | - | 84 / 22 |
| `0x61` | `0x0045C920` | `0x0045C8E0` | `0x0045C980` | `0x0053A060` | - | 9 / 7 |
| `0x62` | `0x0045D290` | `0x0045D250` | `0x0045D2F0` | `0x0053A120` | - | 2 / 2 |
| `0x65` | `0x0045DCA0` | `0x0045DC60` | `0x0045DD10` | `0x0053A1E0` | - | 169 / 44 |
| `0x66` | `0x0045E8C0` | `0x0045E880` | `0x0045E930` | `0x0053A3B0` | - | 414 / 123 |
| `0x67` | `0x0045FD50` | `0x0045FD10` | `0x00460170` | `0x0053A5D0` | `0x00460120` | 364 / 207 |
| `0x68` (sub) | `0x00522AB0` | `0x00522A70` | `0x00522D80` | `0x0054EB40` | - | 162 / 83 |
| `0x69` (sub) | `0x00523C30` | `0x00523BF0` | `0x00523D30` | `0x0054ED10` | - | 58 / 22 |
| `0x6A` (sub) | `0x00525D50` | `0x00525D10` | `0x00526080` | `0x0054F070` | `0x00526040` | 395 / 210 |
| `0x6B` (sub) | `0x00529200` | `0x005291C0` | `0x005294F0` | `0x0054F7C0` | `0x005294B0` | 258 / 117 |
| `0x70` (sub) | `0x0053DD10` | `0x005C5230` | `0x0016D6A0` | `0x0054F270` | `0x0016D6A0` | 0 / 0 |
| `0x71` (sub) | `0x0052A130` | `0x0052A0F0` | `0x0052A360` | `0x0054F9B0` | `0x0052A340` | 28 / 12 |
| `0x72` (sub) | `0x0052ADF0` | `0x0052ADB0` | `0x0052B080` | `0x0054FBE0` | `0x0052B060` | 89 / 47 |
| `0x73` (sub) | `0x0052D3B0` | `0x0052D370` | `0x0052D920` | `0x0054FFF0` | `0x0052D8E0` | 14 / 8 |
| `0x74` (sub) | `0x0052E430` | `0x0052E3F0` | `0x0052EA90` | `0x00550200` | `0x0052EA50` | 4 / 3 |

- `0x60` and `0x62` share the setup `0x0053A120`.
- `0x70` does nothing at run time: its birth `0x0053DD10` returns 1, its update `0x005C5230` returns 0,
  and its draw and release are the bare `ret 0` at `0x0016D6A0`. Only its setup reads the record.
- `0x67`, `0x68`, `0x6A`, `0x6B`, `0x71`, `0x73` and `0x74` update on even frames only in the
  half-rate cadence (the base update's bit set `0x341B`, on the runtime page).
- `0x63`, `0x64` and `0x6C`–`0x6F` have no arm in any table.

### Sub-range draw packets

The sub-range draws build a PS2-style packet in the packet arena instead of emitting primitives. Each
one asks a size function for the packet's length in quadwords, gives up when the cursor `0x02F8F2D0`
plus that length would reach the end `0x02F8F2D8`, lets a builder write the packet at the cursor and
return the new cursor, and hands the packet to a finaliser (`0x0052329D`–`0x0052335F` for type `0x68`).

| Type | Draw | Size | Builder | Templates copied (program) | Finaliser |
|---|---|---|---|---|---|
| `0x68` | `0x00522D80` | `0x00541DB0` | `0x00542100` | `0x02AEB610` (`0x004DF440`), `0x02AEB810` (`0x004E0F70`), `0x02AEB820` | `0x00540F40` |
| `0x69` | `0x00523D30` | `0x00543940` | `0x005439D0` | `0x02AEB0F0` (`0x004DCC00`), `0x02AEB290` (`0x004DDDF0`), `0x02AEB2A0` | `0x00540F40` |
| `0xA3` | `0x00524A50` | `0x00544590` | `0x00544A50` | `0x02AEA270` (`0x004DB350`) | `0x00540F40` |
| `0xA6` | `0x00524E30` | `0x00544CE0` | `0x00544D30` | `0x02AE9BC0` (`0x004DA8A0`), `0x02AE9D50` | `0x00540F40` |
| `0x6B` | `0x005294F0` | `0x00532E80` | `0x00533250`; `0x005325D0` with definition word `+0x866` bit `0x2000` | `0x02AECAC0` (`0x004E7D90`), `0x02AECAD0`, `0x02AECCC0`; `0x02AEBBB0` (`0x004E31E0`), `0x02AEBBC0`, `0x02AEBDB0` | `0x00540F40` |
| `0x6A` | `0x00526080` | `0x00545EF0` | `0x005466E0` | `0x02AE9130` (`0x004D7BF0`), `0x02AE9140`, `0x02AE9290` | `0x00540DB0` |
| `0xA8` | `0x005271D0` | `0x00547350` | `0x005473A0` | `0x02AE9BC0` (`0x004DA8A0`), `0x02AE9D50`, `0x02AE9EE0` | `0x00540F40` |
| `0xA9` | `0x00528150` | `0x005479B0` | `0x00547A00` | `0x02AE8CF0` (`0x00479650`), `0x02AE8D30` | `0x00540C20` |
| `0x71` | `0x0052A360` | `0x00547D80` | `0x005480E0` | `0x02AE8620` (`0x004D40E0`), `0x02AE87B0`, `0x02AE8830` | `0x00540F40` |
| `0x72` | `0x0052B080` | `0x0054A980` | `0x0054AA90` | `0x02AECD20` (`0x004D0FA0`), `0x02AECEB0`, `0x02AED130` | `0x00540F40` |
| `0xAB` | `0x0052C070` | `0x0054B3A0` | `0x0054B3E0` | `0x02AE9BC0` (`0x004DA8A0`), `0x02AE9D50`, `0x02AE9EE0`, `0x02AEC4B0` (`0x004CF490`) | `0x00540F40` |
| `0x73` | `0x0052D920` | `0x0054BD40` | `0x0054BE70` | `0x02AEBE10` (`0x004C8320`), `0x02AEC0A0`, `0x02AEC110` | `0x00540F40` |
| `0x74` | `0x0052EA90` | `0x0054D610` | `0x0054D740` | `0x02AEBE10` (`0x004C8320`), `0x02AEC0A0`, `0x02AEC110` | `0x00540DB0` |

The templates are the boot-time VIF objects of
[PS2 VIF1 / VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md); a builder copies
their quadwords into the packet and patches in the element's values, and a program in brackets is
the microprogram the template's header installs. `0xA6`, `0xA8` and `0xAB` share the templates of
`0x02AE9BC0` and `0x02AE9D50`, and `0x73` and `0x74` share all three of theirs.

- A size function adds a fixed head to a cost per enabled layer slot, the first enabled slot
  costing less: `0x00541DB0` returns 0 unless byte `+0x38` is set, then `0x230` bytes plus `0xB0` for
  the first and `0xC0` for each further of three slots (`+0x140`, stride `0x50`); `0x00544CE0`,
  `0x00547350` and `0x005479B0` count four slots from a `0x40`-byte head.
- `0x0054B3A0` never returns 0: its head is `0x4F0` bytes, plus `0x2D0` for the first and `0x2E0` for each further
  of four slots whose word is not zero (`+0x30`, stride `0x110`; `0x0054B3A3`-`0x0054B3DC`). `0x00543940` adds `0x190`
  bytes for each of four non-zero words at `+0x740`–`+0x830`; `0x00544590` adds one quadword per 20 entries to `0x130`.
- `0x00545EF0` (type `0x6A`) starts from `(+0x1C + 0x17) x 16` bytes and adds, per tile, `0x60` plus
  `w x h x 16` when bit `0x2` of `+0x64` is set. Tiles start every 21 grid points along `+0x10` and `+0x14`
  while the start is below the count minus 1, and `w = min(22, +0x10 - start)`, `h` likewise; it returns
  the total `>> 4` (`0x00545EF0`-`0x00545FAE`).
- `0x0054BD40` and `0x0054D610` add the two index blocks
  of every piece and, per enabled layer byte `+0xE0`–`+0xE3`, `0x60` bytes per piece.
- `0x00540F40(packet, chain, count, key)` computes the flag word, 2 when `0x0024E460` or `0x003A3D20`
  returns non-zero, ORed with `0x003A2C70()`, and passes everything to `0x00540DB0`, which appends the
  draw-list entry and copies the packet into a command (`0x00540F65`–`0x00540F96`).
- `0x00540C20(packet, chain, count, key)`, used by `0xA9` alone, appends an entry with the packet at
  `+0x00`, the key and pass nibble at `+0x08`, the chain count at `+0x0C` and a null function at
  `+0x10`, and builds no command (`0x00540C20`–`0x00540C6B`). `0xA9` sets `0x02AEF418` around the call
  when its key is `0xFFFE00` or more and `0x0024E2E0` returns 0 (`0x005287A6`–`0x005287C2`).
- The key is the projected depth of the element position for `0x68` and `0x69` (`0x00202B70` with
  `0x02AEEBB0`, then z / w); `0xA3` and `0xAB` use `0xFFFFFF` and the rest use 0.

### Type 0x6A: the ripple surface

Type `0x6A` simulates a height field with the damped two-dimensional wave equation. Its birth
`0x00525D50` copies the definition's time step, wave speed, grid spacing and damping (`+0x3D0`–`+0x3DC`)
and the grid's point counts (`+0x3F0`, `+0x3F4`) into the element block at `+0x230`, allocates
16 bytes per point, and then:

- `0x00545120` derives the three step coefficients `k1 = (4 − 8c²t²/d²) / (μt + 2)`,
  `k2 = (μt − 2) / (μt + 2)` and `k3 = (2c²t²/d²) / (μt + 2)` into block `+0x30`, `+0x34` and
  `+0x38`, the half extents `(n − 1)d / 2`, and the number of tiles the packet needs;
- `0x005450E0` zeroes the `n × m` points; `0x005263F0` then runs once per warm-up frame, the count from
  definition word `+0x3FC` (`0x00525FDA`–`0x0052601D`).

`0x005263F0` is the update tail. Definition byte `+0x3FF` bits `0x8`, `0x2` and `0x4` enable three disturbances,
each a strength track (`+0x250`, `+0x260`, `+0x270`) and a position track (`+0x280`, `+0x2C0`,
`+0x300`) in grid units. A disturbance with a non-zero strength stamps the grid; it then runs the
step `0x00545650` as many times as the integer track `+0x3C0` gives, at most 5.

- `0x00545310(grid, x, y, h)` sets a 3 × 3 stamp: `h` at the point, `h / 2` at its four neighbours and
  `h / 4` at the corners; `0x00545490` adds the same stamp. Points within two of the edge are left alone.
- With bit `0x20` of `+0x3FF`, `0x00546DB0` and `0x00547060` stamp a line of points instead, each scaled
  by `(1 + cos φ) / 2` with the phase stepping along the line. Definition byte `+0x3F9` picks the
  adding forms.
- `0x00545650` updates every interior point from itself, its previous height and its four neighbours
  with `k1`, `k2` and `k3`.

### Types 0x73 and 0x74: the flying pieces

Types `0x73` and `0x74` break a mesh into pieces of `0xA0` bytes that fly and spin. `0x73`'s birth
`0x0052D3B0` copies the authored piece data (`+0x954` bytes from definition `+0x960`), allocates one
record per piece (count at `+0x968`) and randomises its ranges; `0x0054C6B0` then gives each piece a
start velocity and spin, the direction chosen by the low three bits of block byte `+0x4E`.

Each step, `0x0054C440` (`0x73`, from the update tail `0x0052E270`) and `0x0054DD30` (`0x74`, from
`0x0052F400`) walk the pieces. The second component `+0x24` of a piece's velocity `+0x20` loses
gravity, its position `+0x70` adds the velocity and its angles `+0x00` add the spin `+0x10`, each
scaled by one of two parameter sets chosen by the piece's time against the block's thresholds;
`0x0046D560` then rebuilds the piece's rotation at `+0x40`.

In `0x0054C440` the step is `v.y -= [+0xC0] x [+0x44] x s x k.y`, then per axis `pos += s x k x v` and
`angle += r x spin x q`. Set A is `s` = block `+0x58`, `k` = `+0x80`-`+0x88`, `r` = `+0x70`-`+0x78`,
`q` = `+0x5C`; set B is `+0x90`, `+0xB0`-`+0xB8`, `+0xA0`-`+0xA8` and `+0x94` (`0x0054C4AE`-`0x0054C67E`).

Set A applies when piece `+0x0C <= [+0xC4]` or piece `+0x98 <= [+0x3C]`. Otherwise set B applies, unless
piece `+0x0C > (1 - [+0xC4]) x [+0xFC] + [+0xC4]` and piece `+0x98 > (1 - [+0x3C]) x [+0x9C] + [+0x3C]`, which
leaves the piece unmoved that step.

- `0x0054C440` moves only a piece whose `+0x30` points to itself (`0x0054C4A4`).
- `0x0054DD30` rotates the velocity step by the matrix at block `+0x150` when bit `0x2` of `+0x9C` is set
  (`0x00202B90`).

### Births of the other sub-range types

- `0x68`'s birth `0x00522AB0` calls `0x00541E00`, which draws five random values `r0`-`r4` =
  `0x003D8E50(1.0) - 0.5` into `+0x00`-`+0x10` and, unless block byte `+0x39` bits `0x8` or `0x10` say otherwise,
  sets `+0xA0 = normalise(r0, r1, r2) x L1` and `+0xB0 = normalise(r3, r4, 0x003D8E50(1.0) - 0.5) x L2`
  (`0x00380800` normalises; `0x00541E12`-`0x00541FCF`).
  - `L1 = [+0xAC] + 0x003D8E50([+0x120])` and `L2 = [+0xBC] + 0x003D8E50([+0x124])`, written back to `+0xAC`
    and `+0xBC`.
- The same birth calls `0x00542060`, which draws six more in `[−0.5, 0.5)`.
- `0x69`'s birth `0x00523C30` calls `0x005439A0`, which clears block `+0x04` and `+0x14` and stores
  the float `1 / (count + 1)`, the count being block `+0x00`, at `+0x18`.
- `0x67`'s birth `0x0045FD50` and `0x6B`'s birth `0x00529200` call `0x00532EF0`, which fills each of
  the `+0xB0` strands (`0x440` bytes) with a base plus a random amount for every parameter and a
  direction from a random or stepped angle; `0x00532E80` sizes `0x6B`'s packet from the strand count
  and three enabled layers (`+0x88`–`+0x90`).
  - Each field is `base + 0x003D8E50(1.0) x range`, with the strand field, block base and block range:
    `+0x10`, `+0xC8`, `+0xCC`; `+0x14`, `+0xF8`, `+0xFC`; `+0x18`, `+0x100`, `+0x104`; `+0x424`, `+0xD8`,
    `+0xDC`; `+0x434`, `+0xC0`, `+0xC4`; `+0x438`, `+0xE8`, `+0xEC`; `+0x43C`, `+0xF0`, `+0xF4`
    (`0x00532EF0`-`0x00533242`).
  - `+0x08` takes `+0xE0`, `+0xE4` the same way when block `+0x140` bit `0x2` is set, else
    `(+0x14 + +0x18) x 0.5`; `+0x1C` is `0x003D8E50(1.0) x` block `+0x1C`.
  - The direction is `+0x420 = L sin a`, `+0x428 = L cos a`, `+0x42C = 1.0`, with `L` from `+0xD0`, `+0xD4`
    as above and `a = 0x003D8E50(6.284)` while block `+0x124` is 0, otherwise `+0x128` plus `+0x12C` for each
    strand before it.
- `0x71`'s birth `0x0052A130` calls `0x00547DD0`, which fills each of the `+0x140` records (`0x450`
  bytes) with a base plus a random amount for every parameter, and a direction from a random or
  stepped angle.
  - Each field is `base + 0x003D8E50(range)`, with the record field, block base and range: `+0x10`, `+0x158`,
    `+0x15C`; `+0x08`, `+0x188`, `+0x18C`; `+0x0C`, `+0x190`, `+0x194`; `+0x434`, `+0x168`, `+0x16C`;
    `+0x444`, `+0x150`, `+0x154`; `+0x448`, `+0x178`, `+0x17C`; `+0x44C`, `+0x180`, `+0x184`
    (`0x00547DD0`-`0x005480D7`).
  - `+0x04 = u16 +0x170 + 0x003A6E60(u16 +0x172)`; `+0x14`-`+0x1C` are each `0x003D8E50([+0x48])` and
    `+0x20`-`+0x28` each `0x003D8E50([+0x4C])`.
  - The direction is `+0x430 = L sin a`, `+0x438 = L cos a`, `+0x43C = 1.0`, with
    `L = +0x160 + 0x003D8E50(+0x164)` and `a = 0x003D8E50(6.284)` while block byte `+0x67` is 0, otherwise
    `+0x70` plus `+0x74` for each record before it.
- `0x72` keeps a sway chain (see [model oscillators](model-oscillators-and-pose-sequencer.md)).
  `0x0054B0E0`, called by its birth tail `0x0052BBD0` and its update tail `0x0052B5E0`, adds an offset to
  every node and sets the root; `0x0054A690(section, out, mode)`, called by `0x0052B5E0`, returns the
  root (mode 0) or walks the segment lengths `+0x38` to the chain's middle (mode 1) or tip (mode 2).

### Types 0x80 to 0x97

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x80` | `0x0044CC10` | `0x00450480` | `0x0044CC50` | `0x00539320` | - | 875 / 381 |
| `0x81` | `0x0044D460` | `0x0044D420` | `0x0044D4A0` | `0x00539270` | - | 0 / 0 |
| `0x82` | `0x0044CC10` | `0x00450480` | `0x0044DD00` | `0x00539320` | - | 617 / 161 |
| `0x83` | `0x0044CC10` | `0x00450480` | `0x0044E530` | `0x00539320` | - | 80 / 48 |
| `0x84` | `0x0044ED90` | `0x0044ED50` | `0x0044EDD0` | `0x00539980` | - | 1,972 / 501 |
| `0x85` | `0x0044F930` | `0x0044F8F0` | `0x0044F970` | `0x005393B0` | - | 78 / 42 |
| `0x86` | `0x004504C0` | `0x00450480` | `0x00450550` | `0x005394A0` | - | 115 / 87 |
| `0x87` | `0x00451140` | `0x00450480` | `0x00451180` | `0x00539560` | - | 175 / 54 |
| `0x88` | `0x00451890` | `0x00451850` | `0x004518D0` | `0x00539610` | - | 41 / 31 |
| `0x89` | `0x004524C0` | `0x00452480` | `0x00452540` | `0x00539740` | - | 36 / 8 |
| `0x8A` | `0x00453110` | `0x004530D0` | `0x00453150` | `0x00539870` | - | 0 / 0 |
| `0x8B` | `0x004548F0` | `0x004548B0` | `0x00454930` | `0x00539A60` | - | 1 / 1 |
| `0x8C` | `0x00455390` | `0x0045B260` | `0x00455540` | `0x00539B30` | - | 7,509 / 910 |
| `0x8D` | `0x00455D70` | `0x00455D30` | `0x00455DB0` | `0x00539C10` | - | 1,170 / 553 |
| `0x8E` | `0x004566E0` | `0x004566A0` | `0x00456720` | `0x00539CF0` | - | 136 / 74 |
| `0x8F` | `0x00457E10` | `0x00456EF0` | `0x00456F30` | `0x00539DA0` | - | 1,663 / 383 |
| `0x90` | `0x00457E10` | `0x00456EF0` | `0x00457FE0` | `0x00539DA0` | - | 765 / 313 |
| `0x91` | `0x00459420` | `0x004593E0` | `0x004595C0` | `0x00539E90` | - | 12 / 7 |
| `0x92` | `0x0045A050` | `0x0045A010` | `0x0045A200` | `0x00539E90` | - | 84 / 45 |
| `0x94` | `0x00455390` | `0x0045B260` | `0x0045AEE0` | `0x00539B30` | - | 2,344 / 387 |
| `0x95` | `0x00455390` | `0x0045B260` | `0x0045B2A0` | `0x00539B30` | - | 456 / 226 |
| `0x96` | `0x00453CB0` | `0x00453C70` | `0x00453CF0` | `0x00539980` | - | 268 / 75 |
| `0x97` | `0x00455390` | `0x0045B260` | `0x0045BAD0` | `0x00539F80` | - | 0 / 0 |

The band shares handlers across types, so a type here often selects a variant rather than a class:

- `0x80`, `0x82` and `0x83` share birth, update and setup and differ in their draw.
- `0x86` and `0x87` also use the update `0x00450480`.
- `0x8C`, `0x94`, `0x95` and `0x97` share birth and update; the first three also share the setup.
- `0x8F` and `0x90` share birth, update and setup; `0x91` and `0x92` share the setup; `0x84` and
  `0x96` share the setup.
- `0x93` and `0x98`–`0x9F` have no arm.

### Types 0xA0 to 0xAB

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0xA0` | `0x00460B80` | `0x00460B40` | `0x00460BC0` | `0x0053A6F0` | - | 0 / 0 |
| `0xA1` | `0x00461090` | `0x00461050` | `0x00461270` | `0x0053A790` | `0x00461250` | 504 / 343 |
| `0xA2` | `0x00462480` | `0x00462440` | `0x00462540` | `0x0053A840` | - | 6,303 / 2,018 |
| `0xA3` (sub) | `0x00524800` | `0x005247C0` | `0x00524A50` | `0x0054EE70` | `0x00524A10` | 447 / 131 |
| `0xA4` (sub) | `0x005222D0` | `0x00522290` | `0x00522300` | `0x0054EA70` | - | 0 / 0 |
| `0xA5` | `0x004633A0` | `0x00463360` | `0x00463460` | `0x0053A900` | - | 36 / 20 |
| `0xA6` (sub) | `0x00524D70` | `0x00524D30` | `0x00524E30` | `0x0054EED0` | - | 359 / 178 |
| `0xA7` (sub) | `0x005269B0` | `0x00526970` | `0x00526A10` | `0x0054F1B0` | - | 14 / 14 |
| `0xA8` (sub) | `0x00527110` | `0x005270D0` | `0x005271D0` | `0x0054F350` | - | 367 / 159 |
| `0xA9` (sub) | `0x00528090` | `0x00528050` | `0x00528150` | `0x0054F520` | - | 0 / 0 |
| `0xAA` (sub) | `0x00528AF0` | `0x00528AB0` | `0x00528B50` | `0x0054F700` | - | 3 / 3 |
| `0xAB` (sub) | `0x0052BFB0` | `0x0052BF70` | `0x0052C070` | `0x0054FE00` | - | 7 / 4 |

`0xA1`, `0xA2` and `0xA5` are, with `0x40`, `0x41` and `0xD0`, the definition types whose emitters
are drawn even when the instance's flag byte `+0x36A` bit `0x1` is clear (the runtime page).

### Types 0xD0 and 0xD1

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0xD0` | `0x00464F20` | `0x00464F10` | `0x00465680` | `0x0053A9D0` | `0x00465120` | 1,437 / 544 |
| `0xD1` | `0x003D9040` | `0x003D9000` | `0x0016D6A0` | `0x0053AA30` | `0x003D90C0` | 765 / 406 |

- `0xD0` changes how chosen characters look. Its apply `0x00465690` works from the flag word `+0x232`
  (`0x004656DB`) and passes each chosen character to `0x00465CD0`, which it calls from eight sites. `0xD0`
  and `0x41` share the update `0x00464F10`.
- With bit `0x1` of `+0x232` set the apply scales the scene colour per channel,
  `0x020926C0 x= 1 + w x (c / 128 - 1)`: `c` is the four colour bytes of `0x0042FDB0([+0x20] + 0x80, [+0x44])`
  and `w` the alpha byte of the `0x002F1F40` fade over 128 while bit `0x80` is set, else 0; bit `0x80` is then cleared
  (`0x004656C6`-`0x0046578F`).
- `0xD1` draws nothing (its draw is `0x0016D6A0`). Its update tail `0x003D92C0` publishes the element at
  `0x02092628` (`0x003D9698`); `0x00258B90`, which the field frame runs with its camera work
  ([frame update order](../Engine-Core/frame-update-order.md)), copies it into the block at
  `0x02096FA0` and clears the pointer (`0x00258C3B`–`0x00258D4D`).

- That copy is then turned into a camera by `0x003D9150` (from `0x00258B90`), unless the half-rate
  cadence test and `0x001EDAD0` hold it back: for the copy's key `+0x330` it takes the eye and target
  (`+0x230` / `+0x240`, 32 bytes a key, swapped when the definition's byte `+0x240` is set) and the
  roll (`+0x320`, 4 bytes a key) and fills the camera `0x02096ED0` with them through `0x003CC080`.
- With the definition's byte `+0x241` bit `0x1` set it uses `0x003CC970` instead, which first pulls the
  eye out of the map's collision (`0x0026E500`, `0x00230B60`). The field of view is the key's `+0x328`,
  with `1 / tan(fov / 2)` at `0x02096EE0`. It writes the camera into camera record 4, or 6 when `+0x241` bit `0x4` is set, with mode 3 and its active
  bit raised (`0x0025A2C0`, `0x0025A500`, `0x0025A520`); see [scripted camera](scripted-camera.md).

### The kind-0x54 mesh record

A mesh is an `0xB00` record of kind `0x54`: a `0x190`-byte object built by `0x004354E0` and loaded by
`0x00436D00(object, payload)`, which first calls the kind's destroy body `0x004352C0` (`0x00436D20`). The loader copies each array into a new block unless the object's `+0x18C` has bit
`0x8`, in which case it keeps a pointer into the stream (`0x00436D98`–`0x00436DDE`).

The id bytes name kind-`0x52` texture records: each is resolved through
`0x003AA280(key, 0x52, id)` with the record's own key word, into the handle array at `+0x184`
(`0x004370B8`–`0x004370FE`).

## Layouts

Kind-`0x54` payload (from `0x00436D00`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | flags: bits `0x7` -> object `+0x18C`; bit `0x1` adds the index lists |
| `+0x02` | `u16` | triangles | -> `+0x10` |
| `+0x04` | `u16` | quads | -> `+0x12` |
| `+0x06` | `u16` | positions | -> `+0x14`, array `+0x20`, 16 bytes each, w set to 1.0 |
| `+0x08` | `u16` | vectors | -> `+0x16`, array `+0x24`, 16 bytes each |
| `+0x0A` | `u16` | 4-byte entries | -> `+0x18`, array `+0x28` |
| `+0x0C` | `u16` | 8-byte entries | -> `+0x1A`, array `+0x2C` |
| `+0x0E` | `u16` | id bytes | -> `+0x1C`, ids `+0x180`, handles `+0x184` (8 bytes each) |
| `+0x10` | `u16` | 20-byte records | -> `+0x1E`, copied inline to `+0x30` |
| `+0x12` | `...` |  | positions, vectors, 4-byte, 8-byte and 20-byte arrays in that order; with flags bit `0x1`, two index lists of 6 x triangles + 8 x quads bytes (`+0x170`, `+0x174`); then one byte per triangle and quad (`+0x188`); then the id bytes |

Element fields the verified draws read:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x044` | `i32` |  | track frame, the time every track is sampled at |
| `+0x1F0` | `u32` | colour |  |
| `+0x230` | `vec` |  | point 1 (types `0x01`, `0x03`); `+0x240` point 2 (`0x03`) |
| `+0x294` | `i32` |  | mesh index (`0x05`) |

Definition fields the verified draws read:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x030` | `...` |  | blend track (mode 6) and alpha percent |
| `+0x044` | `u8` |  | element type |
| `+0x049` | `u8` |  | mask `0xE0` blend mode |
| `+0x190` | `...` |  | mesh-index track (`0x05`) |
| `+0x590` | `u8` |  | bit `0x10` mesh-index mode |
| `+0x5A0` | `u32[32]` |  | mesh handles |

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
| type-`0x05` definitions | 5,204; mesh slots filled at `+0x570`: one in 4,304, two in 898, three in 1, no slot in 1 |
| type-`0x05` mesh ids | all 6,103 equal the slot byte of a kind-`0x54` record in the same stream |

The tables beside this page:

- [`effect-element-types-type_census.tsv`](effect-element-types-type_census.tsv): the per-type counts, matching
  the counts above row for row;
- [`effect-element-types-effect-type-authored-usage.tsv`](effect-element-types-effect-type-authored-usage.tsv): an
  earlier, smaller count whose numbers the counts on this page replace;
- [`effect-element-types-effect-mesh-54-records.tsv`](effect-element-types-effect-mesh-54-records.tsv) (2,733
  rows): the mesh records of every EFX stream (the `.efx` and `.efb` files and the streams embedded in
  `.cm` models and `.mpk` map packs), one per row;
- [`effect-element-types-effect-mesh-54-element05.tsv`](effect-element-types-effect-mesh-54-element05.tsv) (5,204
  rows): the type-`0x05` definitions of every EFX stream, one per row.

### Columns of the `type_census` and mesh tables

Every row of the two mesh tables matches the shipped file it names.

| Column | Holds |
|---|---|
| `chunks_efx_efb`, `files_efx_efb` | in effect-element-types-type_census.tsv, the type's `0xA00` records in the streams of the 3,288 `.efx` and 410 `.efb` files, and how many of those files hold one |
| `chunks_embedded`, `files_embedded` | the same for the 531 streams embedded in `.cm` models (144) and `.mpk` map packs (387); 0 for 14 types; `chunks` and `files` are the two sums on all 55 rows |
| `distinct_assets` | how many different assets hold the type: an `.efx` counts once for all language folders (its sub-folder and name), any other file by its name |
| `tri` | in effect-element-types-effect-mesh-54-records.tsv, payload `u16 +0x02`, the triangle count; 0 in 2,081 of the 2,733 records |
| `c14`, `c16`, `c18`, `c1A`, `c1C`, `c1E` | the payload's six further `u16` counts, `+0x06` to `+0x10`, named by the object field they are copied to: positions (`+0x14`), vectors (`+0x16`), 4-byte entries (`+0x18`), 8-byte entries (`+0x1A`), id bytes (`+0x1C`, 0 to 2) and 20-byte records (`+0x1E`, 0 in all) |
| `avail` | the payload's length, the chunk's length minus `0x10` |
| `ok` | 1 when `avail` is `size` plus 0 to 15 bytes and a multiple of 16; 1 in all 2,733 |
| `chunk_off` | in effect-element-types-effect-mesh-54-element05.tsv, the `0xA00` chunk's offset in the file, in hex |
| `chunk_type` | the chunk's type word, `0xa00` in all 5,204 |
| `mode_0x590` | the definition's byte `+0x590` (chunk `+0x10 + 0x590`), in hex; bit `0x10`, which must be clear for the mesh index to come from the track, is set only in `0x1f`, 2 rows; `0x0e` in 2,853 rows and `0x0d` in 1,724 |

## Operations

One base update and one type tail per live element per simulation step; one draw call per drawn
element per frame; one apply per registered element (`0x40`, `0x41`, `0x42`, `0xD0`) per drawn
frame.

## State

The registry `0x02ADBFE0` (128 slots), the light pool behind `0x003AB960`, the pools at `[0x02B404E0]` and
`0x02B4D7D0`, the blend pair `0x02AEE900` / `0x02AEE908`, and the published element `0x02092628`.

### The draw packets

Many draws hand their values to a vector-unit microprogram instead of emitting primitives themselves. They write
the values into words of a `.data` packet and pass the packet on. The packets are zero on disk. Every row of
[effect-element-types-state.tsv](effect-element-types-state.tsv) is one word, or one 8- or 16-byte store, of such
a packet: its place in the packet, the template value after boot, what each store writes, and every instruction
that writes or reads it.

### Templates the draws patch in place

708 rows. The packet is a boot template of
[PS2 VIF1 / VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md). Its builder fills it once, from
`0x0037DF90` or `0x0037E0F0`. Each draw then does three things:

1. It stores the element's values into the template's payload words.
2. It passes the template `+0x18`, and the length to the template's end, to a registrar: `0x003A34D0`, `0x003A35E0`,
   `0x003A33B0` or `0x003A2F70`.
3. The registrar builds the command through `0x001DB840`. That function keeps only the pointer and the length
   (`0x001DB340`, `0x001DB3B4`).

The words are therefore read from the template itself when the command runs. `0x001DB550` passes each chunk to
`0x0022C940` (`0x001DB5E0`). The decoder `0x0022C970` reads each command word at `0x0022C9D6`. For UNPACK V4-32,
`0x0022BFF0` copies element `j` of the payload into VU cell `addr + j`. It reads lane x at `0x0022C650`, y at
`0x0022C658`, z at `0x0022C65E` and w at `0x0022C666`. The "place" column gives the cell and lane each row lands in.

| Type | Draw | Template (builder) | Chunk | Rows |
|---|---|---|---|---:|
| `0x60` | `0x0045BFB0` | `0x02AE4F20` (`0x004B8F20`) | `0x02AE4F38`, `0xC58` bytes | 30 |
| `0x61` | `0x0045C980` | `0x02AE6950` (`0x004BC120`) | `0x02AE6968`, `0x138` | 23 |
| `0x62` | `0x0045D2F0` | `0x02AE6AA0` (`0x004BF2C0`) | `0x02AE6AB8`, `0x138` | 32 |
| `0x65` | `0x0045DD10` | `0x02AE8900` (`0x004F4F80`) | `0x02AE8918`, `0x2C8` | 50 |
| `0x66` | `0x0045E930` | `0x02AE8E30` (`0x004FD060`) | `0x02AE8E48`, `0x2E8` | 61 |
| `0x80` | `0x0044CC50` | `0x02ADFFE0` (`0x004978F0`) | `0x02ADFFF8`, `0x138` | 33 |
| `0x82` | `0x0044DD00` | `0x02AE1A70` (`0x004802F0`) | `0x02AE1A88`, `0x138` | 35 |
| `0x83` | `0x0044E530` | `0x02AE1DA0` (`0x00482410`) | `0x02AE1DB8`, `0x138` | 34 |
| `0x84` | `0x0044EDD0` | `0x02AE4160` (`0x0048CE70`) | `0x02AE4178`, `0xDA8` | 39 |
| `0x85` | `0x0044F970` | `0x02AE3620` (`0x0048AB40`) | `0x02AE3638`, `0xB28` | 35 |
| `0x86` | `0x00450550` | `0x02AE30A0` (`0x00487BA0`) | `0x02AE30B8`, `0x138` | 27 |
| `0x87` | `0x00451180` | `0x02ADFE90` (`0x004956A0`) | `0x02ADFEA8`, `0x138` | 23 |
| `0x88` | `0x004518D0` | `0x02ADEF40` (`0x00492D40`) | `0x02ADEF58`, `0xDA8` | 46 |
| `0x89` | `0x00452540` | `0x02AE21B0` (`0x00485390`) | `0x02AE21C8`, `0xDA8` | 47 |
| `0x8B` | `0x00454930` | `0x02AE0B60` (`0x0047E140`) | `0x02AE0B78`, `0xD98` | 30 |
| `0x8D` | `0x00455DB0` | `0x02ADFD00` (`0x004C0C70`) | `0x02ADFD18`, `0x178` | 24 |
| `0x8E` | `0x00456720` | `0x02AE0390` (`0x0049D310`) | `0x02AE03A8`, `0x178` | 21 |
| `0x8F` | `0x00456F30` | `0x02AE0520` (`0x0049FE90`) | `0x02AE0538`, `0x178` | 21 |
| `0x91` | `0x004595C0` | `0x02AE1EF0` (`0x004A8860`) | `0x02AE1F08`, `0x178` | 20 |
| `0x96` | `0x00453CF0` | `0x02AE6BF0` (`0x0048F410`) | `0x02AE6C08`, `0x1A18` | 40 |
| `0xA7` | `0x00526A10` | `0x02AED330` (`0x004ED960`) | `0x02AED348`, `0x118` | 17 |
| `0xAA` | `0x00528B50` | `0x02AED200` (`0x004EC960`) | `0x02AED218`, `0x118` | 20 |

No other function writes these words, with one exception. `0x0045E930` passes `0x02AE9020` to `0x0039ADE0`, which
scales four rows in place (`0x0039ADF0`-`0x0039AEB9`): `[0x02AE9020 + 16i + 4j] × [s + 4i]` for row i and lane j, with
`s` the value `0x0017FFD0` returns followed by 1.0, 1.0 and 1.0, when `0x0024E640()` answers non-zero
(`0x0045F048`-`0x0045F07B`). A few draws read a word back before storing it again; the table lists those reads with the
draw.

### Packets copied with memcpy

133 rows. Four draws fill a packet that no builder touches. They pass the
packet's address and length to `0x003A3010`, which copies it into the draw list at the arena cursor `+0x40` with
`memcpy` (import thunk `0x00861EBA`, `0x003A3150`). The draws of `0xA0`, `0x81` and `0x8A` call `0x003A2D80` instead on
their other path, which copies with `memcpy` at `0x003A2DA9`.

| Type | Draw | Packet | Length | Calls | Rows |
|---|---|---|---|---|---:|
| `0xA0` | `0x00460BC0` | `0x02ADEDF0` | `0x150` | `0x003A3010` (`0x00460EF5`), `0x003A2D80` (`0x00460F08`) | 35 |
| `0x81` | `0x0044D4A0` | `0x02AE0850` | `0x150` | `0x003A3010` (`0x0044D7F9`), `0x003A2D80` (`0x0044D80C`) | 31 |
| `0x8A` | `0x00453150` | `0x02AE5B90` | `0xDC0` | `0x003A3010` (`0x004537A8`, `0x004537BF`), `0x003A2D80` (`0x004537CE`) | 48 |
| `0xA4` | `0x00522300` | `0x02AE9300` | `0x210` | `0x003A3010` (`0x005227C5`) | 19 |

### Sub-range templates the builders patch

75 rows. The builders of the sub-range draw packets store into these
templates before copying them into the packet at the cursor. The copies are 16-byte loads in a loop of `0x80`
bytes, and the table names the load for each word.

| Builder | Templates | Rows |
|---|---|---:|
| `0x72`'s `0x0054AA90` | `0x02AECD20` (copy `0x0054AC07`-`0x0054AC89`), `0x02AECEB0` (`0x0054AE27`-`0x0054AED5`), `0x02AED130` (`0x0054AFDA`-`0x0054B02C`, once per strand) | 40 |
| `0x73`'s `0x0054BE70` and `0x74`'s `0x0054D740` | `0x02AEBE10` (`0x0054BFF7`-`0x0054C088`, `0x0054D8D7`-`0x0054D968`), `0x02AEC0A0` (`0x0054C1EE`-`0x0054C224`, `0x0054DAD8`-`0x0054DB03`), `0x02AEC110` (`0x0054C33E`-`0x0054C383`, `0x0054DC2E`-`0x0054DC61`) | 35 |

### Type 0x67's draw frame

`0x67`'s draw `0x00460170` keeps its working values in `.data`, not on the stack. It fills the template `0x02AEC660`
through a pointer and submits it with `0x003A33B0` (`0x004607A2`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA5EE0` | `void*` | 0 (zero-filled tail of `.data`) | the element being drawn | `0x00460170` (`0x0046017C`) | `0x00460170` (`0x004601EC`, `0x00460215`, `0x0046023E`, `0x00460267`, `0x00460290`, `0x004602C0`, `0x004602EB`, `0x00460305`, `0x0046032F`, `0x004603A0`, `0x0046044C`, `0x00460575`) |
| `0x02CA5EE8` | `void*` | 0 (zero-filled tail of `.data`) | its definition, element `+0x20` | `0x00460170` (`0x004601AA`) | `0x00460170` (`0x004601D9`, `0x00460202`, `0x0046022B`, `0x00460254`, `0x0046027D`, `0x004602AB`, `0x00460336`, `0x00460373`, `0x00460434`, `0x0046048B`, `0x0046057C`, `0x00460724`) |
| `0x02CA5EF0` | `void*` | 0 (zero-filled tail of `.data`) | the template `0x02AEC660` the draw fills | `0x00460170` (`0x004601B1`) | `0x00460170` (`0x004601D2`, `0x004601FB`, `0x00460224`, `0x0046024D`, `0x00460276`, `0x0046029F`, `0x004602D6`, `0x0046037A`, `0x00460476`, `0x004605AB`, `0x0046076D`) |
| `0x02CA5EF8` | `void*` | 0 (zero-filled tail of `.data`) | the strand copy's destination: the pointer at element `+0x3D0`, plus `0x260` per strand copied | `0x00460170` (`0x00460660`, `0x00460716`) | no function |
| `0x02CA5F00` | `void*` | 0 (zero-filled tail of `.data`) | the strand copy's source: the pointer at element `+0x338`, plus `0x440` per strand copied | `0x00460170` (`0x00460667`, `0x0046071D`) | no function |
| `0x02CA5F08` | `u32` | 0 (zero-filled tail of `.data`) | the current colour: `0x0042FDB0` of the colour track at `[0x02CA5F78]`, multiplied in place by the fade colour `0x02CA5F0C` (`0x0026EE00`); its four bytes go to `[0x02CA5F80]` as four dwords | `0x00460170` (`0x004603B9`); `0x0026EE00` (`0x0026F3FD`) | `0x0026EE00` (`0x0026EE31`); `0x00460170` (`0x004603D9`, `0x004603ED`, `0x004603F7`, `0x00460401`) |
| `0x02CA5F14` | `u32` | 0 (zero-filled tail of `.data`) | the draw-list key passed to `0x003A33B0`: 0 at entry, then the high half of the qword `0x00399600` writes to its output `0x02CA5F10` (`0x00399AE1` or `0x00399AED`) | `0x00460170` (`0x00460183`); `0x00399600` (`0x00399AE1`, `0x00399AED`) | `0x00460170` (`0x0046079C`) |
| `0x02CA5F20` | `vec` | 0 (zero-filled tail of `.data`) | row 0 of a copy of the element's `+0x240` matrix, which `0x00398030` multiplies by `0x02AEEC30`, `0x02AEEC70` or `0x02AEEA60` for definition byte `+0x4A` bits `0x1C` of 1, 2, or 4 and 5 (`0x00460511`-`0x00460570`) | `0x00460170` (`0x004604E0`); `0x00398030` (`0x00398359`) | `0x00398030` (`0x0039809B`) |
| `0x02CA5F30` | `vec` | 0 (zero-filled tail of `.data`) | row 1 of that matrix | `0x00460170` (`0x004604EE`); `0x00398030` (`0x00398363`) | `0x00398030` (`0x003980AE`) |
| `0x02CA5F40` | `vec` | 0 (zero-filled tail of `.data`) | row 2 of that matrix | `0x00460170` (`0x004604FC`); `0x00398030` (`0x0039836E`) | `0x00398030` (`0x003980DE`) |
| `0x02CA5F50` | `vec` | 0 (zero-filled tail of `.data`) | row 3 of that matrix, the position the turn modes 4 and 5 start from | `0x00460170` (`0x0046050A`) | `0x00434900` (`0x00434939`); `0x00434A70` (`0x00434A97`) |
| `0x02CA5F70` | `i32` | 0 (zero-filled tail of `.data`) | the integer track at definition `+0x1B0`; its sum with the dword `[[0x02F97348] + 0x338]`, as a float, is added to the template word `+0x168` (`0x0046062F`-`0x0046064A`) | `0x00460170` (`0x00460594`) | `0x00460170` (`0x00460635`) |
| `0x02CA5F74` | `u32` | 0 (zero-filled tail of `.data`) | `0x0039A9B0`'s result on the path where definition byte `+0x4B` bit `0x1` is set | `0x00460170` (`0x0046074F`) | no function |
| `0x02CA5F78` | `void*` | 0 (zero-filled tail of `.data`) | the colour track cursor: 0 at entry, then definition `+0x1C0` plus `0x50` per colour | `0x00460170` (`0x0046018C`, `0x0046038C`, `0x00460417`) | `0x00460170` (`0x004603E0`) |
| `0x02CA5F80` | `void*` | 0 (zero-filled tail of `.data`) | the colour output cursor: template `+0x60` plus `0x10` per colour | `0x00460170` (`0x00460393`, `0x0046041E`) | `0x00460170` (`0x004603D2`) |
| `0x02CA5F88` | `u32` | 0 (zero-filled tail of `.data`) | `0x0042FDB0` of the colour track at definition `+0x4D0`, which multiplies the fade colour when it is not `0x80808080` | `0x00460170` (`0x0046034C`) | `0x0026EE00` (`0x0026EE49`) |
| `0x02CA5F8C` | `i32` | 0 (zero-filled tail of `.data`) | the loop count: the nine colours (`0x0046039A`-`0x0046042E`), then the strands of element `+0x330` | `0x00460170` (`0x0046039A`, `0x00460425`, `0x004605B9`, `0x004606F6`) | `0x00460170` (`0x0046040F`) |

No instruction reads `0x02CA5F20`-`0x02CA5F4F` after `0x00398030` writes them (`0x00460570`).

### Type 0xAB's draw frame

`0xAB`'s draw `0x0052C070` also keeps its working values in `.data`. It draws up to four layers, one for each
draw-source block of the definition (`+0x690`, `0xF0` apart). A layer is a polygon of nine points in a 3 × 3
grid: the builder `0x0054B3E0` lists their colours centre first and then round the edge, points 4, 0, 1, 2, 5, 8,
7, 6, 3 and 0 again (`0x0054B994`-`0x0054BA16`). Each layer has a `0x110`-byte block in the request at `0x02CA8530`,
from `0x02CA8560`; `0x0054B3A0` sizes the packet from the layers whose word `+0` is set, and `0x0054B3E0` builds it.

The source kind of the layer's block, byte `+0xA0` (definition `+0x730` + `0xF0` × layer), picks the arm
through the table `0x0052CF40` (`0x0052C452`-`0x0052C474`):

| Kind | Arm | The layer |
|---:|---|---|
| 0 | `0x0052C476` | off: word `+0` is 0 |
| 1 | `0x0052CB7C` | the draw returns at once, with no packet for any layer |
| 2 | `0x0052CBBC` | the block's texture (`0x00431830` at `0x0052CBDB`); its size in pixels from the texture record |
| 3 | `0x0052CD79` | a sprite-row frame (`0x00431830` at `0x0052CDA0`); off when there is no frame |
| 4 | `0x0052CE86` | the block's texture over 256 × 224, texture rectangle (0.001, 0.002)-(1.0, 0.875) |
| 5 | `0x0052C47E` | untextured, 256 × 224 |

A layer of kind 2 to 5 that is ready gets word `+0x100` = `0x5D` (`0x4D` for kind 5) and the blend word
`0x01EFAC20[block word +0xAA & 7]` (for kind 3 with mode 6, `0x01EFAC20` indexed by the sprite row's word `+0x68`,
`0x0052CE64`), and sets `0x02CA8A54`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA8520` | `void*` | 0 (zero-filled tail of `.data`) | the element being drawn | `0x0052C070` (`0x0052C08F`) | `0x0052C070` (`0x0052C144`, `0x0052C168`, `0x0052C192`, `0x0052C1B5`, `0x0052C1DF`, `0x0052C202`, `0x0052C22C`, `0x0052C24F`, `0x0052C279`, `0x0052C29C`, `0x0052C2C6`, `0x0052C2E9`, `0x0052C313`, `0x0052C336`, `0x0052C360`, `0x0052C383`, `0x0052C3AD`, `0x0052C3CA`, `0x0052C4CB`, `0x0052C543`, `0x0052C59B`, `0x0052C5EC`, `0x0052C6F4`, `0x0052C703`, `0x0052C9F7`, `0x0052CAA3`, `0x0052CBBC`, `0x0052CD84`, `0x0052CE86`) |
| `0x02CA8528` | `void*` | 0 (zero-filled tail of `.data`) | its definition, element `+0x20` | `0x0052C070` (`0x0052C0BF`) | `0x0052C070` (`0x0052C104`, `0x0052C199`, `0x0052C1E6`, `0x0052C233`, `0x0052C280`, `0x0052C2CD`, `0x0052C31A`, `0x0052C367`, `0x0052C3B4`, `0x0052C42E`, `0x0052C4F5`, `0x0052C5AA`, `0x0052C5CF`, `0x0052C6E4`, `0x0052C9FE`, `0x0052CA15`, `0x0052CAC1`, `0x0052CBF7`, `0x0052CD0B`, `0x0052CDA5`, `0x0052CEB6`, `0x0052CF2C`) |
| `0x02CA8530` | `vec` | 0 (zero-filled tail of `.data`) | request `+0x00`: the vector track at definition `+0xB50` at the element's frame (a copy of `0x02CA8A00`); the builder puts it at `+0x50` of its copy of the template `0x02AEC4B0` (`0x0054B865`) | `0x0052C070` (`0x0052C153`) | `0x0054B3E0` (`0x0054B856`, called from `0x0052C070` at `0x0052CB4D`) |
| `0x02CA8540` | `f32` | 0 (zero-filled tail of `.data`) | request `+0x10`: the float at definition `+0xBEC`; the builder puts it at template `+0x40` (`0x0054B85A`) | `0x0052C070` (`0x0052C14B`) | `0x0054B3E0` (`0x0054B850`, called from `0x0052C070` at `0x0052CB4D`) |
| `0x02CA8548` | `void*` | 0 (zero-filled tail of `.data`) | request `+0x18`: the address of `0x02CA8A10`, the element's matrix `+0x240` combined with the effect-to-screen matrix `0x02AEEBB0` (`0x00202D70` at `0x0052C0FF`); the builder copies its 64 bytes to template `+0x60` (`0x0054B862`-`0x0054B891`) | `0x0052C070` (`0x0052C112`) | `0x0054B3E0` (`0x0054B84C`, called from `0x0052C070` at `0x0052CB4D`) |
| `0x02CA8554` | `u8` | 0 (zero-filled tail of `.data`) | request `+0x24`: definition byte `+0xBE3` bits `0xF`; read by no function | `0x0052C070` (`0x0052C122`) | no function |
| `0x02CA8555` | `u8` | 0 (zero-filled tail of `.data`) | request `+0x25`: definition byte `+0xBE3` bits under mask `0xF0`; read by no function | `0x0052C070` (`0x0052C132`) | no function |
| `0x02CA89A0` | `void*` | 0 (zero-filled tail of `.data`) | the current layer's block: `0x02CA8560` + `0x110` × layer | `0x0052C070` (`0x0052C45E`) | `0x0052C070` (`0x0052C50D`, `0x0052C55B`, `0x0052C5C1`, `0x0052C604`, `0x0052C66B`, `0x0052C778`, `0x0052C7C1`, `0x0052C80A`, `0x0052C853`, `0x0052C89C`, `0x0052C8E5`, `0x0052C92E`, `0x0052C97A`, `0x0052C9C6`, `0x0052CA26`, `0x0052CAB3`, `0x0052CC0A`, `0x0052CC38`, `0x0052CCA4`, `0x0052CDB4`, `0x0052CDC8`, `0x0052CEAF`) |
| `0x02CA89A8` | `u32` | 0 (zero-filled tail of `.data`) | the colour of grid point 0: the colour track at definition `+0x80` at the element's frame (`0x0042FDB0`), times the element's colour `+0x1F0` when that is not `0x80808080` (`0x0026EE00`). Every layer multiplies its own colour by it for point 0 | `0x0052C070` (`0x0052C162`); `0x0026EE00` (`0x0026F3FD`, called from `0x0052C070` at `0x0052C18D`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C18D`; `0x0026EE49`, called at `0x0052C773`); `0x0052C070` (`0x0052C746`) |
| `0x02CA89AC` | `u32` | 0 (zero-filled tail of `.data`) | the colour of grid point 1, from the colour track at definition `+0xD0`, made the same way | `0x0052C070` (`0x0052C1AF`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C1DA`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C1DA`; `0x0026EE49`, called at `0x0052C7BC`); `0x0052C070` (`0x0052C78F`) |
| `0x02CA89B0` | `u32` | 0 (zero-filled tail of `.data`) | point 2, colour track `+0x120` | `0x0052C070` (`0x0052C1FC`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C227`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C227`; `0x0026EE49`, called at `0x0052C805`); `0x0052C070` (`0x0052C7D8`) |
| `0x02CA89B4` | `u32` | 0 (zero-filled tail of `.data`) | point 3, colour track `+0x170` | `0x0052C070` (`0x0052C249`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C274`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C274`; `0x0026EE49`, called at `0x0052C84E`); `0x0052C070` (`0x0052C821`) |
| `0x02CA89B8` | `u32` | 0 (zero-filled tail of `.data`) | point 4, the centre, colour track `+0x1C0` | `0x0052C070` (`0x0052C296`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C2C1`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C2C1`; `0x0026EE49`, called at `0x0052C897`); `0x0052C070` (`0x0052C86A`) |
| `0x02CA89BC` | `u32` | 0 (zero-filled tail of `.data`) | point 5, colour track `+0x210` | `0x0052C070` (`0x0052C2E3`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C30E`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C30E`; `0x0026EE49`, called at `0x0052C8E0`); `0x0052C070` (`0x0052C8B3`) |
| `0x02CA89C0` | `u32` | 0 (zero-filled tail of `.data`) | point 6, colour track `+0x260` | `0x0052C070` (`0x0052C330`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C35B`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C35B`; `0x0026EE49`, called at `0x0052C929`); `0x0052C070` (`0x0052C8FC`) |
| `0x02CA89C4` | `u32` | 0 (zero-filled tail of `.data`) | point 7, colour track `+0x2B0` | `0x0052C070` (`0x0052C37D`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C3A8`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C3A8`; `0x0026EE49`, called at `0x0052C975`); `0x0052C070` (`0x0052C948`) |
| `0x02CA89C8` | `u32` | 0 (zero-filled tail of `.data`) | point 8, colour track `+0x300` | `0x0052C070` (`0x0052C3D8`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C3F5`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C3F5`; `0x0026EE49`, called at `0x0052C9C1`); `0x0052C070` (`0x0052C994`) |
| `0x02CA89CC` | `u32` | 0 (zero-filled tail of `.data`) | the working colour of a layer. First the element's fade colour, which `0x002F1F40(element, element + 0x70, 0x02CA89CC)` writes (`0x0052C71B`); then, for each grid point, the layer colour `0x02CA89E0` times the point's colour, which `0x00462260` unpacks into four words at layer block `+0x30` + `0x10` × point (calls at `0x0052C78A`, `0x0052C7D3`, `0x0052C81C`, `0x0052C865`, `0x0052C8AE`, `0x0052C8F7`, `0x0052C943`, `0x0052C98F`, `0x0052C9DB`) | `0x002F1F40` (`0x002F1F98`, `0x002F211D`, `0x002F216D`, `0x002F217C`, `0x002F222C`, `0x002F229D`, `0x002F22FA`, `0x002F2380`, `0x002F23CD`, `0x002F241A`, `0x002F2496`, `0x002F24A2`, `0x002F24A7`, `0x002F24D1`, `0x002F2509`, called at `0x0052C71B`); `0x0026EE00` (`0x0026F3FD`, called from `0x002F1F40` at `0x002F232D` and from `0x0052C070` at `0x0052C773`, `0x0052C7BC`, `0x0052C805`, `0x0052C84E`, `0x0052C897`, `0x0052C8E0`, `0x0052C929`, `0x0052C975`, `0x0052C9C1`); `0x0052C070` (`0x0052C756`, `0x0052C79F`, `0x0052C7E8`, `0x0052C831`, `0x0052C87A`, `0x0052C8C3`, `0x0052C90C`, `0x0052C958`, `0x0052C9A4`) | `0x0026EE00` (`0x0026EE31`, called from `0x002F1F40` at `0x002F232D` and from `0x0052C070` at `0x0052C773`, `0x0052C7BC`, `0x0052C805`, `0x0052C84E`, `0x0052C897`, `0x0052C8E0`, `0x0052C929`, `0x0052C975`, `0x0052C9C1`; `0x0026EE49`, called at `0x0052C741`); `0x002F1F40` (`0x002F2170`, `0x002F234F`, `0x002F23A7`, `0x002F23F4`, `0x002F2475`, `0x002F24E5`, called at `0x0052C71B`); `0x00462260` (`0x00462281`, called at the nine sites above); `0x0052C070` (`0x0052C720`) |
| `0x02CA89E0` | `u32` | 0 (zero-filled tail of `.data`) | the layer colour: the colour track of the layer's block (definition `+0x6D0` + `0xF0` × layer) at the element's frame (`0x0042FDB0` at `0x0052C6FE`), times the fade colour `0x02CA89CC` when that is not `0x80808080` | `0x0052C070` (`0x0052C711`); `0x0026EE00` (`0x0026F3FD`, called at `0x0052C741`) | `0x0026EE00` (`0x0026EE31`, called at `0x0052C741`); `0x0052C070` (`0x0052C750`, `0x0052C799`, `0x0052C7E2`, `0x0052C82B`, `0x0052C874`, `0x0052C8BD`, `0x0052C906`, `0x0052C952`, `0x0052C99E`) |
| `0x02CA89E4` | `i32` | 0 (zero-filled tail of `.data`) | the layer number, 0 to 3 (`0x0052CB04`) | `0x0052C070` (`0x0052C435`, `0x0052CAFE`) | `0x0052C070` (`0x0052C4EE`, `0x0052C594`, `0x0052C5C8`, `0x0052C6D6`, `0x0052C9E0`, `0x0052CA0E`, `0x0052CABA`, `0x0052CBE9`, `0x0052CD04`, `0x0052CDBB`, `0x0052CDCF`, `0x0052CEBD`, `0x0052CF33`) |
| `0x02CA89E8` | `void*` | 0 (zero-filled tail of `.data`) | a kind-2 layer's texture record, `0x0020E600` of the block's texture handle `+0xB4` (definition `+0x744` + `0xF0` × layer). Its size words `+0xA8` and `+0xAA` (or `+0x1CC` and `+0x1CE` when `0x005011A0` and `0x00501190` return 0) give the layer's width and height in pixels at block `+0xC8` and `+0xCC` | `0x0052C070` (`0x0052CC11`) | `0x0052C070` (`0x0052CC26`, `0x0052CC9D`) |
| `0x02CA8A00` | `vec` | 0 (zero-filled tail of `.data`) | the vector track at definition `+0xB50` at the element's frame (`0x00430B90` at `0x0052C0D7`), copied to `0x02CA8530` | `0x0052C070` (`0x0052C0F7`) | `0x0052C070` (`0x0052C10B`) |
| `0x02CA8A54` | `u32` | 0 (zero-filled tail of `.data`) | 1 when at least one layer is ready to draw (kinds 2 to 5); with 0 the draw builds no packet (`0x0052CB0D`) | `0x0052C070` (`0x0052C43B`, 0; `0x0052C4C1`, 1) | `0x0052C070` (`0x0052CB0D`) |
| `0x02CA8A58` | `void*` | 0 (zero-filled tail of `.data`) | the packet cursor `0x02F8F2D0` at entry: where the builder writes the packet and what the finaliser `0x00540F40` gets (`0x0052CB77`) | `0x0052C070` (`0x0052C088`) | `0x0052C070` (`0x0052CB38`, `0x0052CB65`) |
| `0x02CA8A60` | `vec` | 0 (zero-filled tail of `.data`) | the last per-layer vector track value the draw read; its x is stored again on its own. In turn: the track at definition `+0x350` + `0x40` × layer (to layer `+0xC0`), `+0x490` (to `+0xD0`), `+0x590` (to `+0x08`), the block's track `+0x00` (added to the texture rectangle `+0x10`-`+0x1C` with the element's offset `+0x280` + 8 × layer) and `+0xA50` (to `+0x20`) | `0x0052C070` (`0x0052C519`, `0x0052C520`, `0x0052C54A`, `0x0052C56D`, `0x0052C574`, `0x0052C5B1`, `0x0052C60B`, `0x0052C612`, `0x0052C623`, `0x0052CA2D`, `0x0052CA60`, `0x0052CA75`, `0x0052CACB`, `0x0052CAD7`, `0x0052CAF4`) | `0x0052C070` (`0x0052CA3D`, its y) |
| `0x02CA8A64` | `f32` | 0 (zero-filled tail of `.data`) | the y of that value; for the block's track, plus the element's offset `+0x284` + 8 × layer | `0x0052C070` (`0x0052C519`, `0x0052C54A`, `0x0052C56D`, `0x0052C5B1`, `0x0052C60B`, `0x0052C623`, `0x0052CA2D`, `0x0052CA75`, `0x0052CACB`, `0x0052CAF4`) | `0x0052C070` (`0x0052CA3D`) |

### The grid emitters' block

The draws of types `0x04` (`0x004453D0`), `0x06` (`0x00447020`) and `0x07` (`0x00447ED0`) describe their surface to the
grid emitters `0x004434D0` and `0x00444340` through eight array pointers and seven counts at `0x02AEED58`-`0x02AEEDB3`.
The surface is a grid of rows of points, the rows running round the shape.

1. Each draw carves the arrays out of the `0x20000`-byte scratch block at `[0x02AEED50]`, one after the other, and
   fills the counts.
2. It calls `0x00444340` when definition byte `+0x672` (type `0x04`) or `+0x6D2` (`0x06`, `0x07`) has bit `0x1` set,
   and `0x004434D0` otherwise (`0x00445AEC`-`0x00445AFF`, `0x004477CD`-`0x004477E0`, `0x00448797`-`0x004487A8`).
3. The emitters draw one quad per grid cell and layer with the quad emitters (`0x0039EA70`, `0x0039EC30`,
   `0x0039F780`, `0x0039F9F0`).

Their argument is a layer list the draw fills at `[0x01FD4A78]` + `0x800`, one layer for each draw-source block that
has a source (`0x004458D0`-`0x00445A91` for `0x04`). Its count is byte `+0x1F0`. Per layer it holds:

- the blend mode, byte `+0x134` + layer (block word `+0xAA` bits under mask `0x7`), copied to `0x02AEE900` at `0x00443581`;
- the layer colour, word `+0x138` + 4 × layer, from the block's colour track;
- the lighting byte `+0x1A4` (block byte `+0xA9`), the mapping mode `+0x1B0` (block byte `+0xA7`) and the
  scrolling mode `+0x1AC`.

In the table, `n` is the number of points, (`0x02AEEDA4` + 1) × (`0x02AEEDA8` + 1), and `m` the number of texture
points, (`0x02AEEDA4` + 1 + `0x02AEEDAC`) × (`0x02AEEDA8` + 1).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AEED58` | `void*` | 0 (zero-filled tail of `.data`) | the points, `n` × 16 bytes at the start of the scratch block: the draw builds them in the element's space (type `0x04`: three rings of `+0x254` + 1 points, `0x00445600`-`0x00445665`), and the projection `0x00399B80` (or `0x0039A150`) turns them in place into screen points; the emitters take each quad's four corners from them (`0x00443CB0`-`0x00443CEF`). `0x00434CD0` also stores a pointer into the block here; every reader runs inside one of the three draws after the draw's own store | `0x00434CD0` (`0x00434D62`); `0x004453D0` (`0x004454FD`); `0x00447020` (`0x004471BF`); `0x00447ED0` (`0x00448073`) | `0x004434D0` (`0x004434F8`); `0x00444340` (`0x00444366`); `0x004453D0` (`0x00445667`, `0x00445749`, `0x00445777`); `0x00447020` (`0x00447319`, `0x004473E6`, `0x00447409`); `0x00447ED0` (`0x004482D3`, `0x004483B2`, `0x004483D5`) |
| `0x02AEED60` | `void*` | 0 (zero-filled tail of `.data`) | the point normals, `n` × 16 bytes: `0x00442F30` gives each point the unit cross product of the edges to its neighbours (type `0x04`: `0x00445750`) | `0x004453D0` (`0x00445518`); `0x00447020` (`0x004471FB`); `0x00447ED0` (`0x004480A0`) | `0x004434D0` (`0x00443619`, `0x00443959`, `0x0044399C`, `0x00443B74`); `0x00444340` (`0x00444499`, `0x00444806`, `0x00444852`, `0x00444A2C`); `0x004453D0` (`0x00445742`); `0x00447020` (`0x004473DF`); `0x00447ED0` (`0x004483AB`) |
| `0x02AEED68` | `void*` | 0 (zero-filled tail of `.data`) | the normals turned for one layer, `n` × 16 bytes. For the layer's colour, when its lighting byte is set: `0x003952D0`, `0x00394E50`, `0x003954E0` or `0x00395050`, then `0x004332B0` combines them with the colours (`0x004435F9`-`0x00443770`). For its texture coordinates, by mapping mode: 1, `0x00395CF0` or `0x00395780` after the effect matrix `0x02AEEA20`; 2, `0x003962F0` after the effect-to-camera matrix `0x02AEEBF0`; 3, `0x00396A30` or `0x00396560` after `0x02AEEA20`; 4, the same after `0x02AEEBF0`; `0x00396FD0` then copies each turned normal's x and y into `0x02AEED88` (`0x00443865`-`0x00443BAF`) | `0x004453D0` (`0x00445523`); `0x00447020` (`0x00447206`); `0x00447ED0` (`0x004480AB`) | `0x004434D0` (`0x00443612`, `0x00443769`, `0x00443952`, `0x00443995`, `0x004439CE`, `0x00443B6D`, `0x00443BA4`); `0x00444340` (`0x00444492`, `0x004445E9`, `0x004447FF`, `0x0044484B`, `0x00444884`, `0x00444A25`, `0x00444A65`) |
| `0x02AEED70` | `void*` | 0 (zero-filled tail of `.data`) | the point colours, `n` RGBA words; type `0x04` gives each ring one of the element's colours `+0x25C`, `+0x260` and `+0x264` times its fade colour (`0x0044568B`-`0x0044572B`) | `0x004453D0` (`0x0044552A`); `0x00447020` (`0x00447211`); `0x00447ED0` (`0x004480B6`) | `0x004434D0` (`0x004436A4`, `0x0044372F`, `0x004437B1`, `0x00443838`, `0x0044385E`); `0x00444340` (`0x00444524`, `0x004445AF`, `0x0044463F`, `0x004446D6`, `0x0044470A`); `0x004453D0` (`0x00445710`); `0x00447020` (`0x004473BF`); `0x00447ED0` (`0x0044838B`) |
| `0x02AEED78` | `void*` | 0 (zero-filled tail of `.data`) | the layer's colours, `n` RGBA words: the point colours times the layer colour through `0x00432300`, or `0x80808080` for every point when the layer colour is `0x80808080`; the quads take their corner colours from here or from `0x02AEED70` | `0x004453D0` (`0x00445539`); `0x00447020` (`0x0044721C`); `0x00447ED0` (`0x004480C1`) | `0x004434D0` (`0x00443697`, `0x004436BD`, `0x004436F0`, `0x00443710`, `0x00443738`, `0x0044374F`, `0x00443762`, `0x0044377B`, `0x004437A4`, `0x004437CA`, `0x004437F0`, `0x0044380D`, `0x00443831`, `0x00443855`); `0x00444340` (`0x00444517`, `0x0044453D`, `0x00444570`, `0x00444590`, `0x004445B8`, `0x004445CF`, `0x004445E2`, `0x00444609`, `0x00444632`, `0x00444658`, `0x00444680`, `0x0044469D`, `0x004446CF`, `0x00444701`) |
| `0x02AEED80` | `void*` | 0 (zero-filled tail of `.data`) | the laid-out texture coordinates, `m` pairs of floats: `u` steps by 1 / `0x02AEEDB0` along each texture repeat, `v` is one value per row (type `0x04`: `0x004457A4`-`0x00445845`); a layer with mapping mode 0 uses them | `0x004453D0` (`0x00445543`); `0x00447020` (`0x00447227`); `0x00447ED0` (`0x004480CC`) | `0x004434D0` (`0x0044388A`); `0x00444340` (`0x00444736`); `0x004453D0` (`0x004457CC`); `0x00447020` (`0x0044749A`); `0x00447ED0` (`0x00448226`, `0x00448254`, `0x0044846B`) |
| `0x02AEED88` | `void*` | 0 (zero-filled tail of `.data`) | the layer's texture coordinates, `m` pairs: the mapped ones from `0x02AEED68`, with mapping mode 2 plus an offset from each point's screen position (`0x00443A00`-`0x00443AB0`); a layer with scrolling mode 1 to 3 moves them with `0x0043E7B0`, `0x00434630` or `0x00434760` | `0x004453D0` (`0x0044554E`); `0x00447020` (`0x00447235`); `0x00447ED0` (`0x004480DA`) | `0x004434D0` (`0x004438B3`, `0x0044390D`, `0x00443976`, `0x004439C7`, `0x00443A29`, `0x00443A6F`, `0x00443AE6`, `0x00443B9D`, `0x00443BDC`, `0x00443C02`, `0x00443C1C`, `0x00443C3A`); `0x00444340` (`0x00444764`, `0x004447BE`, `0x0044482C`, `0x0044487D`, `0x004448E8`, `0x0044492E`, `0x004449A2`, `0x00444A5E`, `0x00444AB2`, `0x00444AD8`, `0x00444AFE`, `0x00444B0A`) |
| `0x02AEED90` | `void*` | 0 (zero-filled tail of `.data`) | the perspective factor `q` of each point, one float each, which the projection writes and the textured quads multiply into each texture coordinate (`0x0039B860` at `0x00443FE9`). `0x00434CD0` also stores a pointer here (`0x00434D8D`); every reader runs inside one of the three draws after the draw's own store | `0x00434CD0` (`0x00434D8D`); `0x004453D0` (`0x00445559`); `0x00447020` (`0x00447240`); `0x00447ED0` (`0x004480E5`) | `0x004434D0` (`0x00443F4D`, `0x0044415D`); `0x00444340` (`0x00444E74`, `0x004450C4`); `0x004453D0` (`0x0044577E`); `0x00447020` (`0x0044745A`); `0x00447ED0` (`0x0044841D`) |
| `0x02AEED98` | `i32` | 0 (zero-filled tail of `.data`) | `n`, the number of normals to turn | `0x004453D0` (`0x00445AAD`); `0x00447020` (`0x0044778C`); `0x00447ED0` (`0x00448759`) | `0x004434D0` (`0x0044360B`, `0x0044394B`, `0x0044398E`, `0x00443B66`); `0x00444340` (`0x0044448B`, `0x004447F8`, `0x00444844`, `0x00444A1E`) |
| `0x02AEED9C` | `i32` | 0 (zero-filled tail of `.data`) | `n`, the number of colours | `0x004453D0` (`0x00445AB3`); `0x00447020` (`0x00447792`); `0x00447ED0` (`0x0044875F`) | `0x004434D0` (`0x004436CA`, `0x00443704`, `0x00443728`, `0x00443756`, `0x004437DD`, `0x00443804`, `0x0044382A`); `0x00444340` (`0x0044454A`, `0x00444584`, `0x004445A8`, `0x004445D6`, `0x0044466B`, `0x00444694`, `0x004446C8`) |
| `0x02AEEDA0` | `i32` | 0 (zero-filled tail of `.data`) | `m`, the number of texture points the scrolling moves | `0x004453D0` (`0x00445ABD`); `0x00447020` (`0x0044779C`); `0x00447ED0` (`0x00448769`) | `0x004434D0` (`0x00443BD2`, `0x00443BF8`, `0x00443C30`); `0x00444340` (`0x00444AA8`, `0x00444ACE`, `0x00444AF4`) |
| `0x02AEEDA4` | `i32` | 0 (zero-filled tail of `.data`) | the segments in a row (points per row less 1): element `+0x254` (`0x04`), `+0x268` (`0x06`) or `+0x274` (`0x07`) | `0x004453D0` (`0x00445AC9`); `0x00447020` (`0x004477A8`); `0x00447ED0` (`0x00448775`) | `0x004434D0` (`0x00443CB4`, `0x00443DB4`, `0x00443F04`, `0x00444114`); `0x00444340` (`0x00444393`, `0x004445FB`, `0x004446AA`, `0x004446F3`, `0x00444A82`, `0x00444B17`, `0x00444C1F`, `0x00444D3F`, `0x00444F66`, `0x004451B6`) |
| `0x02AEEDA8` | `i32` | 0 (zero-filled tail of `.data`) | the rows of quads (rows of points less 1): 2 (`0x04`), element `+0x26C` (`0x06`) or `+0x270` (`0x07`) | `0x004453D0` (`0x00445ACF`); `0x00447020` (`0x004477B4`); `0x00447ED0` (`0x00448781`) | `0x004434D0` (`0x004439B9`, `0x004439ED`, `0x00443AA9`, `0x00443B8F`, `0x00443C72`, `0x00443D5C`, `0x00443D72`, `0x00443E5C`, `0x00443E89`, `0x0044408F`, `0x004440A0`, `0x0044429F`); `0x00444340` (`0x0044486F`, `0x004448A9`, `0x0044496B`, `0x00444A50`, `0x00444B4F`, `0x00444C5D`, `0x00444C6E`, `0x00444D7D`, `0x00444DA7`, `0x00444FDA`, `0x00444FEC`, `0x0044522A`) |
| `0x02AEEDAC` | `i32` | 0 (zero-filled tail of `.data`) | how many times the texture repeats along a row: definition word `+0x670` (`0x04`) or `+0x6D0` (`0x06`; `0x07`, where bit `0x4` of `+0x6D2` makes it 1) | `0x004453D0` (`0x00445AE0`); `0x00447020` (`0x004477C1`); `0x00447ED0` (`0x0044878B`) | `0x004434D0` (`0x004439C0`, `0x00443A02`, `0x00443A97`, `0x00443B96`, `0x00443C83`, `0x00443D40`, `0x00443D83`, `0x00443E40`, `0x00443EA3`, `0x00443F25`, `0x0044406A`, `0x004440B3`, `0x00444135`, `0x0044427A`); `0x00444340` (`0x0044439A`, `0x00444602`, `0x004446B1`, `0x004446FA`, `0x00444876`, `0x0044489D`, `0x00444951`, `0x00444A57`, `0x00444A75`, `0x00444B1E`, `0x00444C3B`, `0x00444D5B`, `0x00444DB8`, `0x00444EAE`, `0x00444FA5`, `0x00444FFD`, `0x004450FE`, `0x004451F5`, `0x00445237`) |
| `0x02AEEDB0` | `i32` | 0 (zero-filled tail of `.data`) | the segments under one texture repeat: `0x02AEEDA4` / `0x02AEEDAC` (`0x004457D3`, `0x00447497`, `0x00448468`) | `0x004453D0` (`0x00445AE6`); `0x00447020` (`0x004477C7`); `0x00447ED0` (`0x00448791`) | `0x004434D0` (`0x00443519`, `0x00443775`, `0x00443814`, `0x0044384F`, `0x004439B3`, `0x004439DE`, `0x00443A87`, `0x00443B89`, `0x00443BB4`, `0x00443C23`, `0x00443D22`, `0x00443E22`, `0x00444020`, `0x00444230`); `0x00444340` (`0x0044438D`, `0x004445F5`, `0x004446A4`, `0x004446ED`, `0x00444869`, `0x00444894`, `0x00444946`, `0x00444A4A`, `0x00444A7C`, `0x00444B11`, `0x00444C19`, `0x00444D39`, `0x00444F60`, `0x004451B0`) |

### The effect matrices

`0x0024C060` rebuilds the effect matrices before the states that update an instance and before the group draw
([effect element runtime](effect-element-runtime.md)). Rows that no other row of the page covers:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AEE960` | `vec` | 0 (zero-filled tail of `.data`) | row 0 of the projection the effects draw with: a copy of the camera projection `0x02AEDD30` (`0x0024C0C9`-`0x0024C101`), or for a menu effect (instance kind 4, `[0x02F97348]` byte 0 = 4) the matrix `0x0057A1F0` returns, with the view `0x02AEE9E0` then the identity (`0x0024C07F`-`0x0024C0C2`). `0x0024C060` multiplies it into the effect-to-screen matrix `0x02AEEBB0` (`0x0024C2FD`); sixteen draws load it for their packets, and type `0x6A` with definition byte `+0x3FB` set takes it instead of `0x02AEEBB0` (`0x00526254`-`0x00526318`) | `0x0024C060` (`0x0024C08E`, `0x0024C0DE`) | `0x00397910` (`0x00397966`, called from `0x0024C060` at `0x0024C2FD`); `0x00217150` (`0x002171DE`, reached through `0x00202D70` from `0x00526080` at `0x00526318`); `0x0044EDD0` (`0x0044F2FA`); `0x0044F970` (`0x0044FED9`); `0x004518D0` (`0x00451E5C`); `0x00452540` (`0x00452AB1`); `0x00453150` (`0x004536B7`); `0x00453CF0` (`0x004542C1`); `0x00454930` (`0x00454DBA`); `0x0045DD10` (`0x0045E2BF`); `0x0045E930` (`0x0045EFF8`); `0x00460170` (`0x004605F0`); `0x00522D80` (`0x0052306E`); `0x005294F0` (`0x00529C5C`); `0x0052A360` (`0x0052A7A6`); `0x0052B080` (`0x0052B4D3`); `0x0052D920` (`0x0052DF83`); `0x0052EA90` (`0x0052F0EC`) |
| `0x02AEE970` | `vec` | 0 (zero-filled tail of `.data`) | row 1 of that projection | `0x0024C060` (`0x0024C099`, `0x0024C0EC`) | `0x00397910` (`0x0039796E`, called from `0x0024C060` at `0x0024C2FD`); `0x00217150` (`0x0021716D`, reached through `0x00202D70` from `0x00526080` at `0x00526318`); `0x0044EDD0` (`0x0044F308`); `0x0044F970` (`0x0044FED2`); `0x004518D0` (`0x00451E6A`); `0x00452540` (`0x00452ABF`); `0x00453150` (`0x004536C5`); `0x00453CF0` (`0x004542CF`); `0x00454930` (`0x00454DC8`); `0x0045DD10` (`0x0045E2B1`); `0x0045E930` (`0x0045EFEA`); `0x00460170` (`0x004605FE`); `0x00522D80` (`0x00523079`); `0x005294F0` (`0x00529C67`); `0x0052A360` (`0x0052A7B1`); `0x0052B080` (`0x0052B4DE`); `0x0052D920` (`0x0052DF8A`); `0x0052EA90` (`0x0052F0F3`) |
| `0x02AEE980` | `vec` | 0 (zero-filled tail of `.data`) | row 2 of that projection | `0x0024C060` (`0x0024C0A4`, `0x0024C0FA`) | `0x00397910` (`0x0039797F`, called from `0x0024C060` at `0x0024C2FD`); `0x00217150` (`0x00217182`, reached through `0x00202D70` from `0x00526080` at `0x00526318`); `0x0044EDD0` (`0x0044F316`); `0x0044F970` (`0x0044FF14`); `0x004518D0` (`0x00451E78`); `0x00452540` (`0x00452ACD`); `0x00453150` (`0x004536D3`); `0x00453CF0` (`0x004542DD`); `0x00454930` (`0x00454DD6`); `0x0045DD10` (`0x0045E2DB`); `0x0045E930` (`0x0045F014`); `0x00460170` (`0x0046060C`); `0x00522D80` (`0x00523084`); `0x005294F0` (`0x00529C72`); `0x0052A360` (`0x0052A7BC`); `0x0052B080` (`0x0052B4E9`); `0x0052D920` (`0x0052DF95`); `0x0052EA90` (`0x0052F0FE`) |
| `0x02AEE990` | `vec` | 0 (zero-filled tail of `.data`) | row 3 of that projection | `0x0024C060` (`0x0024C0AF`, `0x0024C101`) | `0x00397910` (`0x0039798E`, called from `0x0024C060` at `0x0024C2FD`); `0x00217150` (`0x0021744C`, reached through `0x00202D70` from `0x00526080` at `0x00526318`); `0x0044EDD0` (`0x0044F324`); `0x0044F970` (`0x0044FF06`); `0x004518D0` (`0x00451E86`); `0x00452540` (`0x00452ADB`); `0x00453150` (`0x004536E1`); `0x00453CF0` (`0x004542EB`); `0x00454930` (`0x00454DE4`); `0x0045DD10` (`0x0045E2CD`); `0x0045E930` (`0x0045F006`); `0x00460170` (`0x0046061A`); `0x00522D80` (`0x0052308F`); `0x005294F0` (`0x00529C7D`); `0x0052A360` (`0x0052A7C7`); `0x0052B080` (`0x0052B4F4`); `0x0052D920` (`0x0052DFA0`); `0x0052EA90` (`0x0052F109`) |
| `0x02AEEA50` | `vec` | 0 (zero-filled tail of `.data`) | row 3 of the effect matrix `0x02AEEA20`, which maps the effect instance's own space into the world: the rotation `0x00398480` builds from the angles `0x02096820` in the axis order `0x02096800` leaves (0, 0, 0, 1) here, `0x0039ADE0` scales the rows by `0x02096810` (w 1.0, `0x0024C212`), and `0x0024C060` adds the instance position `0x02096830` (instance `+0x300`) and stores the sum (`0x0024C21F`-`0x0024C2AA`). So x, y and z are the effect's position | `0x0024C060` (`0x0024C2AA`); `0x00398480` (called from `0x0024C060` at `0x0024C15B`) through its order body: `0x00398DD0` (`0x00398EBA`, `0x00398F57`, `0x00398F7E`, order 0), `0x00398A90` (`0x00398B8E`, `0x00398C09`, `0x00398C3D`, order 4), `0x00398730` (`0x0039883F`, `0x003988B6`, `0x003988F2`, order 5), or for orders 1 to 3 `0x00250010` (`0x002500C4`) and then `0x00397ED0` (`0x00397F6F`, `0x00397FA1`, `0x00397FCB`, `0x00397FF2`, called from `0x003985B0` at `0x0039870C`, `0x00398910` at `0x00398A69` and `0x00398C50` at `0x00398DAC`); `0x0039ADE0` (`0x0039AE9B`, `0x0039AEAA`, `0x0039AEB9`, `0x0039AEC8`, called from `0x0024C060` at `0x0024C21A`) | `0x0024C060` (`0x0024C22D`); `0x004434D0` (`0x00443929`, `0x00443B02`); `0x00444340` (`0x004447DA`, `0x004449BE`); `0x0039ADE0` (`0x0039AE96`, `0x0039AEA5`, `0x0039AEB4`, `0x0039AEC3`, called from `0x0024C060` at `0x0024C21A`); `0x00397910` (`0x003979D5`, called from `0x0024C060` at `0x0024C2E3`; `0x0039798E`, called from `0x004355D0` at `0x00435A2C` and `0x00435B52`, `0x00437130` at `0x004374DE` and `0x00437627`, `0x00438860` at `0x0043892D`, `0x00438CC4` and `0x00438E01`, `0x0045AEF0` at `0x0045AFDF`); `0x0039AF70` (`0x0039AF90`, called from `0x002F1F40` at `0x002F1FFD` and `0x002F2032`, `0x00434900` at `0x00434934`, `0x00434A70` at `0x00434A92`, `0x0043F2B0` at `0x0043F326` and `0x0043F388`, `0x004640A0` at `0x004641FB`, `0x005002E0` at `0x00500348` and `0x005003A6`); `0x00397ED0` (`0x00397F5C`, `0x00397F8E`, `0x00397FBE`, `0x00397FE1`, called from `0x004428F0` at `0x00442AED`) |
| `0x02AEEA64` | `f32` | 0 (zero-filled tail of `.data`) | row 0, lane 1 of the effect rotation `0x02AEEA60`: lane 0 of the effect matrix's row 1, `0x02AEEA30`, so the rotation is that matrix's 3 x 3 part with rows and columns swapped | `0x0024C060` (`0x0024C19A`), after `0x00250010` sets `0x02AEEA60` to the identity (`0x002500E5`, through `0x0024C160`) | `0x00398030` (`0x00398069`), through the 78 sites in 39 functions that pick `0x02AEEA60` for modes 4 and 5 (Project notes); `0x00397910` (`0x00397966`, through `0x0024C345` and `0x0024C35F`) |
| `0x02AEEA68` | `f32` | 0 (zero-filled tail of `.data`) | row 0, lane 2 of the effect rotation `0x02AEEA60`: lane 0 of the effect matrix's row 2, `0x02AEEA40`, so the rotation is that matrix's 3 x 3 part with rows and columns swapped | `0x0024C060` (`0x0024C1AA`), after `0x00250010` sets `0x02AEEA60` to the identity (`0x002500E5`, through `0x0024C160`) | `0x00398030` (`0x00398069`), through the 78 sites in 39 functions that pick `0x02AEEA60` for modes 4 and 5 (Project notes); `0x00397910` (`0x00397966`, through `0x0024C345` and `0x0024C35F`) |
| `0x02AEEA70` | `f32` | 0 (zero-filled tail of `.data`) | row 1, lane 0 of the effect rotation `0x02AEEA60`: lane 1 of the effect matrix's row 0, `0x02AEEA24`, so the rotation is that matrix's 3 x 3 part with rows and columns swapped | `0x0024C060` (`0x0024C1BA`), after `0x00250010` sets `0x02AEEA60` to the identity (`0x002500DA`, through `0x0024C160`) | `0x00398030` (`0x0039807B`), through the 78 sites in 39 functions that pick `0x02AEEA60` for modes 4 and 5 (Project notes); `0x00397910` (`0x0039796E`, through `0x0024C345` and `0x0024C35F`) |
| `0x02AEEA74` | `f32` | 0 (zero-filled tail of `.data`) | row 1, lane 1 of the effect rotation `0x02AEEA60`: lane 1 of the effect matrix's row 1, `0x02AEEA34`, so the rotation is that matrix's 3 x 3 part with rows and columns swapped | `0x0024C060` (`0x0024C1CA`), after `0x00250010` sets `0x02AEEA60` to the identity (`0x002500DA`, through `0x0024C160`) | `0x00398030` (`0x0039807B`), through the 78 sites in 39 functions that pick `0x02AEEA60` for modes 4 and 5 (Project notes); `0x00397910` (`0x0039796E`, through `0x0024C345` and `0x0024C35F`) |
| `0x02AEEA78` | `f32` | 0 (zero-filled tail of `.data`) | row 1, lane 2 of the effect rotation `0x02AEEA60`: lane 1 of the effect matrix's row 2, `0x02AEEA44`, so the rotation is that matrix's 3 x 3 part with rows and columns swapped | `0x0024C060` (`0x0024C1DA`), after `0x00250010` sets `0x02AEEA60` to the identity (`0x002500DA`, through `0x0024C160`) | `0x00398030` (`0x0039807B`), through the 78 sites in 39 functions that pick `0x02AEEA60` for modes 4 and 5 (Project notes); `0x00397910` (`0x0039796E`, through `0x0024C345` and `0x0024C35F`) |
| `0x02AEEA80` | `f32` | 0 (zero-filled tail of `.data`) | row 2, lane 0 of the effect rotation `0x02AEEA60`: lane 2 of the effect matrix's row 0, `0x02AEEA28`, so the rotation is that matrix's 3 x 3 part with rows and columns swapped | `0x0024C060` (`0x0024C1EA`), after `0x00250010` sets `0x02AEEA60` to the identity (`0x002500CF`, through `0x0024C160`) | `0x00398030` (`0x00398088`), through the 78 sites in 39 functions that pick `0x02AEEA60` for modes 4 and 5 (Project notes); `0x00397910` (`0x0039797F`, through `0x0024C345` and `0x0024C35F`) |
| `0x02AEEA84` | `f32` | 0 (zero-filled tail of `.data`) | row 2, lane 1 of the effect rotation `0x02AEEA60`: lane 2 of the effect matrix's row 1, `0x02AEEA38`, so the rotation is that matrix's 3 x 3 part with rows and columns swapped | `0x0024C060` (`0x0024C1FA`), after `0x00250010` sets `0x02AEEA60` to the identity (`0x002500CF`, through `0x0024C160`) | `0x00398030` (`0x00398088`), through the 78 sites in 39 functions that pick `0x02AEEA60` for modes 4 and 5 (Project notes); `0x00397910` (`0x0039797F`, through `0x0024C345` and `0x0024C35F`) |
| `0x02AEEA88` | `f32` | 0 (zero-filled tail of `.data`) | row 2, lane 2 of the effect rotation `0x02AEEA60`: lane 2 of the effect matrix's row 2, `0x02AEEA48`, so the rotation is that matrix's 3 x 3 part with rows and columns swapped | `0x0024C060` (`0x0024C20A`), after `0x00250010` sets `0x02AEEA60` to the identity (`0x002500CF`, through `0x0024C160`) | `0x00398030` (`0x00398088`), through the 78 sites in 39 functions that pick `0x02AEEA60` for modes 4 and 5 (Project notes); `0x00397910` (`0x0039797F`, through `0x0024C345` and `0x0024C35F`) |
| `0x02AEEC60` | `vec` | 0 (zero-filled tail of `.data`) | row 3 of the camera-facing matrix `0x02AEEC30`, the camera rotation kept at `0x02AEEAA0`-`0x02AEEAC0` multiplied by the effect rotation `0x02AEEA60`, itself the transposed 3 x 3 of the effect matrix (`0x00397910` at `0x0024C345`, out = camera x `0x02AEEA60`): (0, 0, 0) with w 1.0 after each rebuild. The sprite drawers `0x00501A50` and `0x00502280` overwrite it with the sprite's position, request `+0x00`, before they turn the sprite to face the camera (`0x00397ED0` at `0x00501B66`, `0x005023A5`); nothing restores it. `0x00398030`, which the other 47 users of `0x02AEEC30` call, reads rows 0 to 2 only (`0x00398069`, `0x0039807B`, `0x00398088`) | `0x00397910` (`0x00397AE0`, called from `0x0024C060` at `0x0024C345`); `0x00501A50` (`0x00501B56`); `0x00502280` (`0x00502395`) | `0x00397ED0` (`0x00397F5C`, `0x00397F8E`, `0x00397FBE`, called from `0x00501A50` at `0x00501B66` and `0x00502280` at `0x005023A5`) |
| `0x02AEEC6C` | `f32` | 0 (zero-filled tail of `.data`) | the w of that row: 1.0 after the rebuild, and 1.0 again from the sprite drawers | `0x00397910` (`0x00397AE0`, called from `0x0024C060` at `0x0024C345`); `0x00501A50` (`0x00501B56`, `0x00501B5E`); `0x00502280` (`0x00502395`, `0x0050239D`) | `0x00397ED0` (`0x00397FE1`, called from `0x00501A50` at `0x00501B66` and `0x00502280` at `0x005023A5`) |
| `0x02AEECC0` | `vec` | 0 (zero-filled tail of `.data`) | row 1 of the effect-to-screen matrix `0x02AEECB0`: the projection `0x02AEE960` times the view `0x02AEE9E0` times the effect matrix `0x02AEEA20` (`0x02AEEBB0`, copied at `0x0024C364`-`0x0024C3A0`), so it maps the effect instance's space onto the screen. The effect-file camera `0x003ED8A0` replaces it through `0x0039D430` (the view it is given, combined with `0x02AEE5A0` by `0x0039AFA0`). `0x0039B550` loads it into the vector unit for the projections of 62 functions; the mesh and sprite drawers `0x00434CD0`, `0x00435050`, `0x00438860`, `0x00501A50` and `0x00502280` fold the element's matrix into it for their draw and put the saved rows back | `0x0024C060` (`0x0024C387`); `0x003977B0` (`0x0039788F`, called from `0x00434CD0` at `0x00434DAD`, `0x00435050` at `0x004350EB` and `0x00438860` at `0x0043890E`); `0x00397910` (`0x00397AB6`, called from `0x00501A50` at `0x00501B83` and `0x00502280` at `0x005023C2`); `0x003970A0` (`0x003970B1`, reached by the tail jump of `0x0039D430` at `0x0039D46F`, which `0x003ED8A0` calls at `0x003ED94F`); `0x00434CD0` (`0x00434E7F`, `0x00434EEC`); `0x00435050` (`0x0043517D`, `0x00435293`); `0x00438860` (`0x0043D882`); `0x00501A50` (`0x005020FE`); `0x00502280` (`0x00502C53`) | `0x003977B0` (`0x003977D5`, called at `0x00434DAD`, `0x004350EB`, `0x0043890E`); `0x00397910` (`0x0039796E`, called at `0x00501B83`, `0x005023C2`); `0x0039B550` (`0x0039B573`), called with this matrix at every one of its 82 call sites: `0x002F1F40` (`0x002F205D`, `0x002F21E3`); `0x0039C4C0` (`0x0039C4EB`); `0x0039C550` (`0x0039C575`); `0x0039C5D0` (`0x0039C620`); `0x0039C6B0` (`0x0039C6E4`); `0x0039C770` (`0x0039C79B`); `0x0039C800` (`0x0039C83C`); `0x0039CCB0` (`0x0039CCE5`); `0x00434CD0` (`0x00434DEC`); `0x00435050` (`0x004350F7`); `0x00438860` (`0x0043891A`); `0x0043F2B0` (`0x0043F3DA`); `0x004453D0` (`0x00445767`); `0x00447020` (`0x004473F9`); `0x00447ED0` (`0x004483C5`); `0x004490D0` (`0x004491CA`); `0x0044CC50` (`0x0044CF79`); `0x0044D080` (`0x0044D306`); `0x0044D4A0` (`0x0044D79D`); `0x0044DD00` (`0x0044E04C`); `0x0044E160` (`0x0044E41D`); `0x0044E530` (`0x0044E86B`); `0x0044E980` (`0x0044EC41`); `0x0044EDD0` (`0x0044F396`); `0x0044F970` (`0x0044FFE1`); `0x00450550` (`0x00450839`); `0x00450940` (`0x00450BC9`); `0x00451180` (`0x00451424`); `0x00451530` (`0x0045173C`); `0x004518D0` (`0x00451EF8`); `0x00452540` (`0x00452B4D`); `0x00453150` (`0x00453753`); `0x00453CF0` (`0x0045435D`); `0x00454930` (`0x00454E56`); `0x00455560` (`0x00455625`, `0x004557AD`); `0x004559C0` (`0x00455A7E`, `0x00455C61`); `0x00455DB0` (`0x00455EE2`, `0x00456201`); `0x00456720` (`0x004567F1`, `0x00456A53`); `0x00456F30` (`0x00457010`, `0x00457349`); `0x004574B0` (`0x00457583`, `0x004578B5`); `0x00458010` (`0x00458140`, `0x004583AA`); `0x004584E0` (`0x00458631`, `0x00458B66`); `0x00458CA0` (`0x00458DD0`, `0x00459291`); `0x004595C0` (`0x004596EF`, `0x00459AA5`); `0x0045A220` (`0x0045A2F1`, `0x0045A490`); `0x0045A6A0` (`0x0045A773`, `0x0045A9B1`); `0x0045AEF0` (`0x0045AFAE`, `0x0045B1AF`); `0x0045B2B0` (`0x0045B3D0`, `0x0045B592`); `0x0045BAE0` (`0x0045BBA4`, `0x0045BE81`); `0x0045BFB0` (`0x0045C336`, `0x0045C369`); `0x0045C980` (`0x0045CCA6`, `0x0045CCD9`); `0x0045D2F0` (`0x0045D6B8`, `0x0045D6EB`); `0x0045DD10` (`0x0045E26D`); `0x0045E930` (`0x0045EFAD`); `0x00460170` (`0x004605A6`); `0x00460BC0` (`0x00460EE1`); `0x00461090` (`0x00461181`); `0x00461270` (`0x004612E8`, `0x00461494`); `0x005002E0` (`0x005003F4`); `0x005294F0` (`0x00529B1E`); `0x0052A360` (`0x0052A772`); `0x0052B080` (`0x0052B49F`); `0x00434CD0` (`0x00434D39`); `0x00435050` (`0x004350C7`); `0x00438860` (`0x004388ED`); `0x00460BC0` (`0x00460E4F`); `0x00501A50` (`0x00501AC0`); `0x00502280` (`0x00502304`) |
| `0x02AEECD0` | `vec` | 0 (zero-filled tail of `.data`) | row 2 of `0x02AEECB0` | `0x0024C060` (`0x0024C380`); `0x003977B0` (`0x003978B7`, called from `0x00434CD0` at `0x00434DAD`, `0x00435050` at `0x004350EB` and `0x00438860` at `0x0043890E`); `0x00397910` (`0x00397ADC`, called from `0x00501A50` at `0x00501B83` and `0x00502280` at `0x005023C2`); `0x003970A0` (`0x003970BC`, reached by the tail jump of `0x0039D430` at `0x0039D46F`, which `0x003ED8A0` calls at `0x003ED94F`); `0x00434CD0` (`0x00434E87`, `0x00434EF4`); `0x00435050` (`0x00435189`, `0x0043529F`); `0x00438860` (`0x0043D88A`); `0x00501A50` (`0x00502110`); `0x00502280` (`0x00502C63`) | `0x003977B0` (`0x003977E6`, called at `0x00434DAD`, `0x004350EB`, `0x0043890E`); `0x00397910` (`0x0039797F`, called at `0x00501B83`, `0x005023C2`); `0x0039B550` (`0x0039B57E`), called with this matrix at every one of its 82 call sites: `0x002F1F40` (`0x002F205D`, `0x002F21E3`); `0x0039C4C0` (`0x0039C4EB`); `0x0039C550` (`0x0039C575`); `0x0039C5D0` (`0x0039C620`); `0x0039C6B0` (`0x0039C6E4`); `0x0039C770` (`0x0039C79B`); `0x0039C800` (`0x0039C83C`); `0x0039CCB0` (`0x0039CCE5`); `0x00434CD0` (`0x00434DEC`); `0x00435050` (`0x004350F7`); `0x00438860` (`0x0043891A`); `0x0043F2B0` (`0x0043F3DA`); `0x004453D0` (`0x00445767`); `0x00447020` (`0x004473F9`); `0x00447ED0` (`0x004483C5`); `0x004490D0` (`0x004491CA`); `0x0044CC50` (`0x0044CF79`); `0x0044D080` (`0x0044D306`); `0x0044D4A0` (`0x0044D79D`); `0x0044DD00` (`0x0044E04C`); `0x0044E160` (`0x0044E41D`); `0x0044E530` (`0x0044E86B`); `0x0044E980` (`0x0044EC41`); `0x0044EDD0` (`0x0044F396`); `0x0044F970` (`0x0044FFE1`); `0x00450550` (`0x00450839`); `0x00450940` (`0x00450BC9`); `0x00451180` (`0x00451424`); `0x00451530` (`0x0045173C`); `0x004518D0` (`0x00451EF8`); `0x00452540` (`0x00452B4D`); `0x00453150` (`0x00453753`); `0x00453CF0` (`0x0045435D`); `0x00454930` (`0x00454E56`); `0x00455560` (`0x00455625`, `0x004557AD`); `0x004559C0` (`0x00455A7E`, `0x00455C61`); `0x00455DB0` (`0x00455EE2`, `0x00456201`); `0x00456720` (`0x004567F1`, `0x00456A53`); `0x00456F30` (`0x00457010`, `0x00457349`); `0x004574B0` (`0x00457583`, `0x004578B5`); `0x00458010` (`0x00458140`, `0x004583AA`); `0x004584E0` (`0x00458631`, `0x00458B66`); `0x00458CA0` (`0x00458DD0`, `0x00459291`); `0x004595C0` (`0x004596EF`, `0x00459AA5`); `0x0045A220` (`0x0045A2F1`, `0x0045A490`); `0x0045A6A0` (`0x0045A773`, `0x0045A9B1`); `0x0045AEF0` (`0x0045AFAE`, `0x0045B1AF`); `0x0045B2B0` (`0x0045B3D0`, `0x0045B592`); `0x0045BAE0` (`0x0045BBA4`, `0x0045BE81`); `0x0045BFB0` (`0x0045C336`, `0x0045C369`); `0x0045C980` (`0x0045CCA6`, `0x0045CCD9`); `0x0045D2F0` (`0x0045D6B8`, `0x0045D6EB`); `0x0045DD10` (`0x0045E26D`); `0x0045E930` (`0x0045EFAD`); `0x00460170` (`0x004605A6`); `0x00460BC0` (`0x00460EE1`); `0x00461090` (`0x00461181`); `0x00461270` (`0x004612E8`, `0x00461494`); `0x005002E0` (`0x005003F4`); `0x005294F0` (`0x00529B1E`); `0x0052A360` (`0x0052A772`); `0x0052B080` (`0x0052B49F`); `0x00434CD0` (`0x00434D4F`); `0x00435050` (`0x004350D3`); `0x00438860` (`0x004388F5`); `0x00460BC0` (`0x00460EA9`); `0x00501A50` (`0x00501AD1`); `0x00502280` (`0x00502314`) |
| `0x02AEECE0` | `vec` | 0 (zero-filled tail of `.data`) | row 3 of `0x02AEECB0` | `0x0024C060` (`0x0024C3A0`); `0x003977B0` (`0x003978DB`, called from `0x00434CD0` at `0x00434DAD`, `0x00435050` at `0x004350EB` and `0x00438860` at `0x0043890E`); `0x00397910` (`0x00397AE0`, called from `0x00501A50` at `0x00501B83` and `0x00502280` at `0x005023C2`); `0x003970A0` (`0x003970C7`, reached by the tail jump of `0x0039D430` at `0x0039D46F`, which `0x003ED8A0` calls at `0x003ED94F`); `0x00434CD0` (`0x00434E8F`, `0x00434EFC`); `0x00435050` (`0x00435190`, `0x004352A6`); `0x00438860` (`0x0043D892`); `0x00501A50` (`0x00502122`); `0x00502280` (`0x00502C75`) | `0x003977B0` (`0x003977F6`, called at `0x00434DAD`, `0x004350EB`, `0x0043890E`); `0x00397910` (`0x0039798E`, called at `0x00501B83`, `0x005023C2`); `0x0039B550` (`0x0039B590`), called with this matrix at every one of its 82 call sites: `0x002F1F40` (`0x002F205D`, `0x002F21E3`); `0x0039C4C0` (`0x0039C4EB`); `0x0039C550` (`0x0039C575`); `0x0039C5D0` (`0x0039C620`); `0x0039C6B0` (`0x0039C6E4`); `0x0039C770` (`0x0039C79B`); `0x0039C800` (`0x0039C83C`); `0x0039CCB0` (`0x0039CCE5`); `0x00434CD0` (`0x00434DEC`); `0x00435050` (`0x004350F7`); `0x00438860` (`0x0043891A`); `0x0043F2B0` (`0x0043F3DA`); `0x004453D0` (`0x00445767`); `0x00447020` (`0x004473F9`); `0x00447ED0` (`0x004483C5`); `0x004490D0` (`0x004491CA`); `0x0044CC50` (`0x0044CF79`); `0x0044D080` (`0x0044D306`); `0x0044D4A0` (`0x0044D79D`); `0x0044DD00` (`0x0044E04C`); `0x0044E160` (`0x0044E41D`); `0x0044E530` (`0x0044E86B`); `0x0044E980` (`0x0044EC41`); `0x0044EDD0` (`0x0044F396`); `0x0044F970` (`0x0044FFE1`); `0x00450550` (`0x00450839`); `0x00450940` (`0x00450BC9`); `0x00451180` (`0x00451424`); `0x00451530` (`0x0045173C`); `0x004518D0` (`0x00451EF8`); `0x00452540` (`0x00452B4D`); `0x00453150` (`0x00453753`); `0x00453CF0` (`0x0045435D`); `0x00454930` (`0x00454E56`); `0x00455560` (`0x00455625`, `0x004557AD`); `0x004559C0` (`0x00455A7E`, `0x00455C61`); `0x00455DB0` (`0x00455EE2`, `0x00456201`); `0x00456720` (`0x004567F1`, `0x00456A53`); `0x00456F30` (`0x00457010`, `0x00457349`); `0x004574B0` (`0x00457583`, `0x004578B5`); `0x00458010` (`0x00458140`, `0x004583AA`); `0x004584E0` (`0x00458631`, `0x00458B66`); `0x00458CA0` (`0x00458DD0`, `0x00459291`); `0x004595C0` (`0x004596EF`, `0x00459AA5`); `0x0045A220` (`0x0045A2F1`, `0x0045A490`); `0x0045A6A0` (`0x0045A773`, `0x0045A9B1`); `0x0045AEF0` (`0x0045AFAE`, `0x0045B1AF`); `0x0045B2B0` (`0x0045B3D0`, `0x0045B592`); `0x0045BAE0` (`0x0045BBA4`, `0x0045BE81`); `0x0045BFB0` (`0x0045C336`, `0x0045C369`); `0x0045C980` (`0x0045CCA6`, `0x0045CCD9`); `0x0045D2F0` (`0x0045D6B8`, `0x0045D6EB`); `0x0045DD10` (`0x0045E26D`); `0x0045E930` (`0x0045EFAD`); `0x00460170` (`0x004605A6`); `0x00460BC0` (`0x00460EE1`); `0x00461090` (`0x00461181`); `0x00461270` (`0x004612E8`, `0x00461494`); `0x005002E0` (`0x005003F4`); `0x005294F0` (`0x00529B1E`); `0x0052A360` (`0x0052A772`); `0x0052B080` (`0x0052B49F`); `0x00434CD0` (`0x00434D72`); `0x00435050` (`0x004350DF`); `0x00438860` (`0x004388FD`); `0x00460BC0` (`0x00460EB7`); `0x00501A50` (`0x00501AE2`); `0x00502280` (`0x00502325`) |
| `0x02AEE904` | `f32` | 0 (zero-filled tail of `.data`) | the word after the blend selector `0x02AEE900`: `0x0024C060` stores 0.0 there at the end of each rebuild of the effect matrices | `0x0024C060` (`0x0024C398`) | no instruction names it |

### The view

The view `0x02AEE9E0` holds four rows. `0x0024C060` copies them from the camera view `0x02AEDE70`-`0x02AEDEAF`
(`0x0024C10D`-`0x0024C13E`), or for a menu effect (instance kind 4, `[0x02F97348]` byte 0 = 4) sets the identity through
`0x00250010` (`0x0024C0BB`, `0x0024C0C2`). `0x0039D430`, called from `0x003ED8A0` (`0x003ED94F`), copies all four from the matrix it
is given. Every access below is 16 bytes.

`0x0024C060` passes the view's address to two functions. `0x00397910` multiplies it, `0x02AEEBF0 = 0x02AEEA20 × 0x02AEE9E0`
(`0x00397910(a, b, out)` forms `b × a`), by the effect matrix `0x02AEEA20` into `0x02AEEBF0` (`0x0024C2CE`-`0x0024C2E3`).

For a menu effect `0x0039D480` copies the view to the camera rotation `0x02AEEAA0`-`0x02AEEADF`
(`0x0024C226`, `0x0024C2B1`-`0x0024C2BD`). Its rows are `0x02AEEAA0`, `0x02AEEAB0`, `0x02AEEAC0` and `0x02AEEAD0` (`0x0039D4AB`, `0x0039D4BB`,
`0x0039D4C6`, `0x0039D4D1`); `0x0024C060` reads the first three for the camera-facing matrix (`0x0024C302`, `0x0024C310`, `0x0024C328`),
and `0x00460BC0` reads `0x02AEEAB0` at `0x00460DAA`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AEE9F0` | `vec` | 0 (zero-filled tail of `.data`) | row 1 of the view: the camera view's row `0x02AEDE80`, or the identity's for a menu effect | `0x0024C060` (`0x0024C129`); `0x00250010` (`0x002500DA`, through `0x0024C0BB`); `0x0039D430` (`0x0039D442`) | `0x0052D920` (`0x0052E196`); `0x00397910` (`0x0039796E`, through `0x0024C2DC`); `0x0039D480` (`0x0039D4B7`, `0x0039D4DB`, through `0x0024C226`, for a menu effect) |
| `0x02AEEA00` | `vec` | 0 (zero-filled tail of `.data`) | row 2 of the view: the camera view's row `0x02AEDE90`, or the identity's | `0x0024C060` (`0x0024C137`); `0x00250010` (`0x002500CF`, through `0x0024C0BB`); `0x0039D430` (`0x0039D44D`) | `0x0052D920` (`0x0052E1A5`); `0x00397910` (`0x0039797F`, through `0x0024C2DC`); `0x0039D480` (`0x0039D4C2`, `0x0039D4E4`, through `0x0024C226`, for a menu effect) |
| `0x02AEEA10` | `vec` | 0 (zero-filled tail of `.data`) | row 3 of the view: the camera view's row `0x02AEDEA0`, or the identity's | `0x0024C060` (`0x0024C13E`); `0x00250010` (`0x002500C4`, through `0x0024C0BB`); `0x0039D430` (`0x0039D458`) | `0x0052D920` (`0x0052E1B0`); `0x00397910` (`0x0039798E`, through `0x0024C2DC`); `0x0039D480` (`0x0039D4CD`, through `0x0024C226`, for a menu effect) |

### Other state

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02ADBFC4` | `u32` | 0 (zero-filled tail of `.data`) | the registry's serial: `0x00377190` adds 1, and above `0xFFFFFF` it becomes 1 (`0x003771B6`-`0x003771D8`); the handle is `serial << 8 \| slot` | `0x00377190` (`0x003771D8`); `0x003773C0` (`0x003773C9`, 0; called from `0x00259180` at `0x002591B4`) | `0x00377190` (`0x003771B6`) |
| `0x02B4D7A4` | `u32` | 0 (zero-filled tail of `.data`) | the `0x42` pool's serial, kept the same way (`0x003D8059`-`0x003D8069`); the handle `serial << 8 \| slot` goes to slot `+0x04` (`0x003D8074`) | `0x003D7FF0` (`0x003D8069`); `0x003D8C30` (`0x003D8D4F`, 0; called from `0x00259180` at `0x002591AF`) | `0x003D7FF0` (`0x003D8059`) |
| `0x02B4D7A1` | `u8` | 0 (zero-filled tail of `.data`) | a mask that `0x003D83A0` ands with slot byte `+0x3C`: any of bits `0x7F` then set would send it to `0x003D8B4A` (`0x003D84D5`-`0x003D84F0`); the only store writes 0, so that branch is never taken | `0x003D8C30` (`0x003D8D1F`, a `u16` store of 0 over `0x02B4D7A1`-`0x02B4D7A2`) | `0x003D83A0` (`0x003D84D5`) |
| `0x02B4D7A2` | `u8` | 0 (zero-filled tail of `.data`) | a switch on kind-2 requests: while it is not 0, `0x003D7FF0` takes no slot for a request whose byte `+0x0E` is 2 and returns 0 (`0x003D7FF6`-`0x003D8008`) | `0x003D8D60` (`0x003D8D60`, the low byte of its argument), reached through `0x002EA880` from `deny_char_camerashake` (`0x4A0`, `0x003517C0`, the popped integer) and from `0x002628B0` (`0x00262A51`, 0); `0x003D8C30` (`0x003D8D1F`, the second byte of its `u16` store of 0) | `0x003D7FF0` (`0x003D7FFF`) |
| `0x02092630` | `u8` | 0 (zero-filled tail of `.data`) | a mode byte for `0xD1`'s copy. `0x00258B90` switches on it (`0x00258C68`): with 0 it skips the camera step when its argument is 1, with 1 it tests the scene flags at `[0x02096A18]` `+0x366`, `+0x367` and `+0x370`, and any other value runs `0x003D9150`. Every store writes 0, so only the 0 arm runs | `memset` (import thunk `0x00861EC0`) from `0x0024C970` (`0x0024C983`, `0x1670` bytes from `0x020910A0`); `0x0024C970` (`0x0024CAF1`); `0x003D92C0` (`0x003D96A3`) | `0x00258B90` (`0x00258C68`) |
| `0x02092631` | `u8` | 0 (zero-filled tail of `.data`) | camera records to release in the field: `0xD1`'s release `0x003D90C0` ors in 1 when definition byte `+0x241` has bit `0x4` set and 2 otherwise, while the byte at `[0x02F97348]` is below `0xA` (`0x003D90E0`-`0x003D9104`). Unless its argument is 1, `0x00258B90` calls `0x0025A520(6, 0)` for bit `0x1` and `0x0025A520(4, 0)` for bit `0x2`, then clears the byte | `memset` from `0x0024C970` (`0x0024C983`); `0x0024C970` (`0x0024CAF1`); `0x003D90C0` (`0x003D9104`); `0x00258B90` (`0x00258BD8`) | `0x003D90C0` (`0x003D9104`); `0x00258B90` (`0x00258B9F`, `0x00258BC3`) |
| `0x02092632` | `u8` | 0 (zero-filled tail of `.data`) | the same while the byte at `[0x02F97348]` is `0xA` or more (`0x003D90FC`). `0x00258B90` handles it when `[0x02096A18]` `+0x370` is set and `+0x366` is 0 or not above `+0x367` (`0x00258BDF`-`0x00258C2F`) | `memset` from `0x0024C970` (`0x0024C983`); `0x0024C970` (`0x0024CAF8`); `0x003D90C0` (`0x003D90FC`); `0x00258B90` (`0x00258C2F`) | `0x003D90C0` (`0x003D90FC`); `0x00258B90` (`0x00258BDF`, `0x00258C1A`) |
| `0x02096ED8` | `f32` | 0 (zero-filled tail of `.data`) | the field of view of the camera `0x02096ED0`: the key's `+0x328` from `0x003D9150`, or π/4 (`0x3F490FDB`) from the camera set-ups | `0x003D9150` (`0x003D922D`); `0x003CBAD0` (`0x003CBAE1`, reached from `0x00259360` by its jump); `0x003CBBE0` (`0x003CBBF1`, reached from `0x00259180` through `0x003CBFF0`) | `0x0025A2C0` (`0x0025A2C6`, its 16-byte load of `0x02096ED0`, called from `0x003D9150` at `0x003D929F`) |

The four built-in type-`0x42` definitions and the projection copy the effect camera starts from:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B4E3D8` | `void*` | 0 (zero-filled tail of `.data`) | entry 1 of the four definition pointers at `0x02B4E3D0`: the body `0x01EFE520` of the built-in record at `0x01EFE510` (its `+0x08` holds the body length, `0x130`), after `0x0050C450` has set it up over that length | `0x003D8C30` (`0x003D8C42`, the record; `0x003D8CA9`, its body; called from `0x00259180` at `0x002591AF`) | `0x003D8C30` (`0x003D8C8E`); `0x003D7FF0` (`0x003D80A0`-`0x003D80A7`) |
| `0x02B4E3E0` | `void*` | 0 (zero-filled tail of `.data`) | entry 2: the body `0x01EFE6A0` of the record at `0x01EFE690`, set up the same way | `0x003D8C30` (`0x003D8C57`, `0x003D8CD0`) | `0x003D8C30` (`0x003D8CB5`); `0x003D7FF0` (`0x003D80A0`-`0x003D80A7`) |
| `0x02AEE5B0` | `vec` | 0 (zero-filled tail of `.data`) | row 1 of `0x02AEE5A0`, a copy of the camera projection `0x02AEDD30` taken by `0x0039AED0` and `0x0039AF20`, which `0x0039CD50` runs in the field reset | `0x0039AED0` (`0x0039AEFC`); `0x0039AF20` (`0x0039AF44`) | `0x0039AFA0` (`0x0039B059`, copied to `0x022D9310` at `0x0039B060`; called from `0x0039D430` at `0x0039D45F`) |
| `0x02AEE5C0` | `vec` | 0 (zero-filled tail of `.data`) | row 2 of that copy | `0x0039AED0` (`0x0039AF0A`); `0x0039AF20` (`0x0039AF52`) | `0x0039AFA0` (`0x0039B067`, copied to `0x022D9320` at `0x0039B082`) |
| `0x02AEE5D0` | `vec` | 0 (zero-filled tail of `.data`) | row 3 of that copy | `0x0039AED0` (`0x0039AF11`); `0x0039AF20` (`0x0039AF59`) | `0x0039AFA0` (`0x0039B08A`, copied to `0x022D9330` at `0x0039B09A`) |

`0x003D7FF0`, the `0x42` pool's slot taker, first refuses a request whose byte `+0x0E` is 2 while `0x02B4D7A2` is not 0: it
returns 0 (`0x003D7FF6`-`0x003D8008`). Otherwise it copies the request's 32 bytes to slot `+0x30`. When the slot byte `+0x3E` is 2 it
holds slot `+0x40` to at most 3, takes that entry of `0x02B4E3D0`, adds `0x80` (the definition's track group) and
stores its image offset (`0x0020E620`) back at `+0x40` (`0x003D8086`-`0x003D80B4`). Entry 0, `0x02B4E3D0`, is `0x01EFE3A0`, the body
of the record at `0x01EFE390`, and entry 3, `0x02B4E3E8`, the body `0x01EFE820` of the record at `0x01EFE810`.

Before the copy, `0x003D7FF0` takes the first slot whose handle `+0x04` is 0 and returns 0 when all 32
are taken (`0x003D8015`-`0x003D8045`). It stamps the slot's `+0x50` with `0x00181DD0()`, raises the byte count
`0x02B4D7A0` and stores the handle (`0x003D8046`-`0x003D8074`); after the copy it clears `+0x3F` (`0x003D808A`).

After the `+0x40` step it clears `+0x00` and `+0x20`, copies the dwords `+0x98` and `+0x9C` of the block
`+0x40` names (`0x0020E600`) to `+0x28` and `+0x2C`, and sets `+0x44` to that block's `+0x90` times `+0x38`,
`+0x48` to 1.2 and `+0x4C` to 1 / `+0x44` (`0x003D80B7`-`0x003D811C`). It appends the slot at the tail of the
list `0x02B4D7A8` / `0x02B4D7B0`, with the links `+0x08` and `+0x0C` encoded by `0x0020E620`, and returns the
handle (`0x003D80EF`-`0x003D8174`).

### Templates the type arms patch

265 rows. Several draws of types `0x80` to `0x95` hand the element to an arm, a function of its own, chosen by a
definition byte. Each arm patches a boot template of its own in the same way as the draws above, and passes the
template `+0x18` and its length to a registrar. The rows of
[effect-element-types-state.tsv](effect-element-types-state.tsv) name the draw and the arm.

| Type | Draw | Arm, and when | Template (builder) | Chunk | Registrar calls | Rows |
|---|---|---|---|---|---|---:|
| `0x80` | `0x0044CC50` | `0x0044D080`, definition byte `+0x250` bit `0x4` set (`0x0044CCAB`) | `0x02AEBA50` (`0x004C7CF0`) | `0x02AEBA68`, `0x148` | `0x003A34D0` (`0x0044D386`, `0x0044D3BC`), `0x003A35E0` (`0x0044D3E5`) | 24 |
| `0x82` | `0x0044DD00` | `0x0044E160`, byte `+0x25E` bit `0x1` set (`0x0044DD5B`) | `0x02AEB8E0` (`0x004C6BB0`) | `0x02AEB8F8`, `0x158` | `0x003A34D0` (`0x0044E49D`, `0x0044E4D3`), `0x003A35E0` (`0x0044E4FC`) | 25 |
| `0x83` | `0x0044E530` | `0x0044E980`, byte `+0x254` bit `0x2` set (`0x0044E58B`) | `0x02AEB4B0` (`0x004C5BD0`) | `0x02AEB4C8`, `0x148` | `0x003A34D0` (`0x0044ECC1`, `0x0044ECF7`), `0x003A35E0` (`0x0044ED20`) | 26 |
| `0x86` | `0x00450550` | `0x00450940`, byte `+0x25C` bit `0x1` set (`0x004505AB`) | `0x02AEB360` (`0x004C4A50`) | `0x02AEB378`, `0x138` | `0x003A34D0` (`0x00450C49`, `0x00450C7F`), `0x003A35E0` (`0x00450CA8`) | 21 |
| `0x87` | `0x00451180` | `0x00451530`, byte `+0x244` bit `0x1` set (`0x004511DB`) | `0x02AEAFC0` (`0x004C3610`) | `0x02AEAFD8`, `0x118` | `0x003A34D0` (`0x004517BC`, `0x004517F2`), `0x003A35E0` (`0x0045181B`) | 15 |
| `0x8C` | `0x00455540` | `0x004559C0`, byte `+0x294` bits `0x6` clear (`0x00455549`) | `0x02AE0130` (`0x00499850`) | `0x02AE0148`, `0x118` | `0x003A2F70` (`0x00455C50`), `0x003A33B0` (`0x00455CF3`) | 8 |
| `0x8C` | `0x00455540` | `0x00455560`, those bits not clear | `0x02AE0260` (`0x0049B850`) | `0x02AE0278`, `0x118` | `0x003A2F70` (`0x00455825`, `0x00455923`), `0x003A33B0` (`0x004558B2`, `0x0045598A`) | 9 |
| `0x8F` | `0x00456F30` | `0x004574B0`, byte `+0x384` bits `0x6` clear (`0x00456F65`) | `0x02AE06B0` (`0x004A1C10`) | `0x02AE06C8`, `0x188` | `0x003A33B0` (`0x00457928`) | 20 |
| `0x90` | `0x00457FE0` | `0x004584E0`, byte `+0x337` not 0 (`0x00457FE9`) | `0x02AE1BC0` (`0x004A6490`) | `0x02AE1BD8`, `0x1C8` | `0x003A33B0` (`0x00458BF6`, `0x00458C54`) | 35 |
| `0x90` | `0x00457FE0` | `0x00458010`, `+0x337` and `+0x330` both 0 (`0x00457FF6`) | `0x02AE1910` (`0x004A4220`) | `0x02AE1928`, `0x148` | `0x003A33B0` (`0x0045843D`, `0x004584A4`) | 15 |
| `0x90` | `0x00457FE0` | `0x00458CA0`, `+0x337` 0 and `+0x330` not 0 | `0x02AE09A0` (`0x004A3150`) | `0x02AE09B8`, `0x1A8` | `0x003A33B0` (`0x00459324`, `0x00459391`) | 30 |
| `0x92` | `0x0045A200` | `0x0045A6A0`, byte `+0x2A4` bits `0x6` clear (`0x0045A209`) | `0x02AE2080` (`0x004AAE20`) | `0x02AE2098`, `0x118` | `0x003A2F70` (`0x0045A9A3`), `0x003A33B0` (`0x0045AA16`) | 9 |
| `0x92` | `0x0045A200` | `0x0045A220`, those bits not clear | `0x02AE2F70` (`0x004AD840`) | `0x02AE2F88`, `0x118` | `0x003A2F70` (`0x0045A509`, `0x0045A607`), `0x003A33B0` (`0x0045A596`, `0x0045A66E`) | 10 |
| `0x94` | `0x0045AEE0` | `0x0045AEF0`, always | `0x02AE31F0` (`0x004B0000`) | `0x02AE3208`, `0x128` | `0x003A2F70` (`0x0045B19E`), `0x003A33B0` (`0x0045B227`) | 8 |
| `0x95` | `0x0045B2A0` | `0x0045B2B0`, always | `0x02AE3330` (`0x004B0B70`) | `0x02AE3348`, `0x118` | `0x003A2F70` (`0x0045B581`), `0x003A33B0` (`0x0045B60A`) | 10 |

The arms of `0x8C`, `0x92`, `0x94` and `0x95` call `0x003A2F70` when the blend mode of the draw-source block at
definition `+0x1A0` (`0x8C`, `0x94`, `0x95`) or `+0x1B0` (`0x92`) is 0, and `0x003A33B0` with a draw-list key
otherwise (`0x00455C04`, `0x0045A964`, `0x0045B15F`, `0x0045B542`).

Some arms submit their chunk twice. They read the two-bit field `(byte >> 1) & 3` of a definition byte: `+0x294`
for `0x8C` and `+0x2A4` for `0x92`, the bytes that chose the arm (`0x004557B2`, `0x0045A495`), and `+0x384` for the three
arms of `0x90` (`0x004583D5`, `0x00458B91`, `0x004592BC`). With 3 they store 2 in a pass word before the first submission
and 0 before the second. With 2 they submit once with 2, and with 1 or 0 once with 0. The pass words are `0x02AE0280`
(`0x8C`), `0x02AE09D0` and `0x02AE1940` (`0x90`), `0x02AE2F90` (`0x92`), and bit `0x2` of `0x02AE1BF8` (`0x90`).

No other function writes these words. The only boot writers are each template's builder and its `memset`.

### Type 0x97's packet

9 rows. `0x97`'s draw `0x0045BAD0` hands the element to `0x0045BAE0`, which fills the `.data` packet `0x02AE3460`
(`0x1C0` bytes) that no builder touches. It copies the packet in one of two ways (`0x0045BE4F`):

- when the blend mode of the draw-source block at definition `+0x1A0` is 0, with `0x003A2E30`, which copies it with
  `memcpy` at `0x003A2E71`;
- otherwise with `0x003A31A0`, which moves the first `0x20` bytes itself (`0x003A32D2`-`0x003A32DE`) and copies the rest
  with `memcpy` at `0x003A3305`.

Packet `+0x60`, `0x02AE34C0`, holds a six-light block of [character lighting](character-lighting-and-shadows.md).
`0x003AC110` builds it (`0x0045BCCD`): it clears `0xE0` bytes with `memset` (`0x003AC190`), stores the light directions by
component at `+0x00`-`+0x5F` and each light's colour at `+0x60` + 16 × light (`0x003AC5AC`).

The draw then takes the two direction blocks, at `+0x00` and `+0x30`, into the element's space. `0x00202D50` is a rigid
inverse: it writes the transposed rotation and minus the turned translation, with w 1.0 (`0x00217610`-`0x00217780`).

The draw inverts each block, multiplies it by the inverse of the element's matrix, `inv(block) × inv(E)`
(`0x00397910` at `0x0045BD63`, `0x0045BD74`), and writes the inverse back (`0x0045BD91`, `0x0045BDA1`), so
`block = inv(inv(block) × inv(E))`, with `inv` the rigid inverse `0x00202D50`, `E` the element's matrix
(`0x0045BCFF`-`0x0045BD08`) and `×` the product `b × a` that `0x00397910(a, b, out)` forms. The write-back of the `+0x30`
block also covers block `+0x60`, the colour of light 0, so the draw saves those 16 bytes first (`0x0045BD79`) and
restores them after (`0x0045BDB7`).

### Type 0x71's sub-range templates

41 rows. `0x71`'s draw `0x0052A360` calls its builder `0x005480E0` with the request at element `+0x280`
(`0x0052A389`, `0x0052A83A`) and a block of its own as fifth argument (`0x0052A830`). Before the call the draw fills:

1. request `+0xB0` to `+0x130`: the nine colours, the colour tracks at definition `+0x180` + `0x50` × colour at the
   element's frame, each as four words (`0x00462260`, `0x0052A4BB`-`0x0052A567`);
2. per layer L 0 to 2, from the draw-source block at definition `+0x570` + `0xF0` × L: the enable byte `+0x78` + L,
   the kind byte `+0x60` + L, the layer colour at `+0x80` + `0x10` × L, and in the block its two texture register
   words, blend word and blend flags (`0x0052A5B2`-`0x0052A6A5`);
3. block `+0x00`-`+0x7F`: the effect-to-camera matrix `0x02AEEBF0` and the projection `0x02AEE960`, with the depth offset
   added to the projection's z (`0x0052A777`-`0x0052A7F0`).

The builder stores into three templates and copies each into the packet:

| Template (boot builder) | Patched by | Copied by |
|---|---|---|
| `0x02AE8620` (`0x004D3E20`) | the nine colours and the two matrices, once (`0x00548110`-`0x005481E9`) | `0x0054857E`-`0x00548656`: two passes of `0x80` bytes from `0x02AE8640`, then `0x70` bytes |
| `0x02AE87B0` (`0x004D3D60`) | one strand record's values, for each of the request's `+0x140` strands (`0x005486B4`-`0x00548747`) | `0x00548738`-`0x005487BD` |
| `0x02AE8830` (`0x004D3FE0`) | one layer's values, for each enabled layer (`0x005487F5`-`0x0054888C`) | `0x00548865`-`0x005488EE` |

The request's floats come from `0x0052A8B0`, which the update `0x0052A0F0` and the birth `0x0052A130` call: it samples the
definition's float tracks at the element's frame into them (`0x0052AB62`-`0x0052AD23`). The birth copies the rest from
the definition (`0x0052A159`-`0x0052A2E7`).

### The position helpers' working values

The update and the birth of six types each call a helper that keeps its working values in `.data`:

| Type | Update (call) | Birth (call) | Helper | Words | Flag, limit, factor | Result |
|---|---|---|---|---|---|---|
| `0xA2` | `0x00462440` (`0x00462466`) | `0x00462480` (`0x004624AF`) | `0x004630D0` | `0x02CA5F90`-`0x02CA5FBF` | definition `+0x7D1`, `+0x7D4`, `+0x7D8` | element `+0x2B0` |
| `0xA5` | `0x00463360` (`0x00463386`) | `0x004633A0` (`0x004633CF`) | `0x00463D20` | `0x02CA5FC0`-`0x02CA5FEF` | `+0x8C1`, `+0x8C4`, `+0x8C8` | `+0x2B0` |
| `0xA6` | `0x00524D30` (`0x00524D56`) | `0x00524D70` (`0x00524DA3`) | `0x005259E0` | `0x02CA8460`-`0x02CA848F` | `+0xA51`, `+0xA54`, `+0xA58` | `+0x250` |
| `0xA8` | `0x005270D0` (`0x005270F6`) | `0x00527110` (`0x00527143`) | `0x00527DC0` | `0x02CA8490`-`0x02CA84BF` | `+0xB61`, `+0xB64`, `+0xB68` | `+0x250` |
| `0xA9` | `0x00528050` (`0x00528076`) | `0x00528090` (`0x005280BF`) | `0x00528820` | `0x02CA84C0`-`0x02CA84EF` | `+0x851`, `+0x854`, `+0x858` | `+0x250` |
| `0xAB` | `0x0052BF70` (`0x0052BF96`) | `0x0052BFB0` (`0x0052BFE3`) | `0x0052CF60` | `0x02CA84F0`-`0x02CA851F` | `+0xBE1`, `+0xBE4`, `+0xBE8` | `+0x2A0` |

Each helper does the same steps (`0x004630D0` for `0xA2`):

1. It keeps the element and its definition, element `+0x20` (`0x004630EE`, `0x004630F9`).
2. It adds the element's position `+0x60` to its position word, turns the sum by the parent's matrix when element
   `+0x10` is set (`0x0039AF70`, then `0x00398F90` in place), and stores it as the world position `+0x70`
   (`0x004630DD`-`0x004631A5`).
3. When the flag byte is set it stores `1 − factor × min(d, limit)` in the result field, with `d` the distance from
   the position word to the camera position `0x02AEDF20` (`0x004631AA`-`0x00463336`). Otherwise it stores 1.0
   (`0x00463344`).

The sum in step 2 starts from the position word's value after the previous call of the same helper, for any
element, not from 0. The common step `0x002F3890` of [effect element runtime](effect-element-runtime.md) takes `+0x60`
alone (`0x002F38BD`, `0x002F38E2`).

`0x005259E0` (`0xA6`) measures `d` from a second sum: it adds `+0x60` to the position word again and turns it again
(`0x00525AC7`-`0x00525B69`), without storing that sum in the element. `0x0052CF60` (`0xAB`) afterwards replaces `+0x70`
with element `+0x230`: the vector track at definition `+0xB90` at the element's frame plus `+0x60`, turned by the
parent's matrix (`0x0052D1F1`-`0x0052D31F`). It first moves the old `+0x70` into `+0x80` (`0x0052D314`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA5F90` | `void*` | 0 (zero-filled tail of `.data`) | the element `0x004630D0` works on | `0x004630D0` (`0x004630EE`) | `0x004630D0` (`0x00463190`) |
| `0x02CA5F98` | `void*` | 0 (zero-filled tail of `.data`) | its definition, element `+0x20` | `0x004630D0` (`0x004630F9`) | `0x004630D0` (`0x00463197`) |
| `0x02CA5FA0` | `vec` | 0 (zero-filled tail of `.data`) | the position word: its previous value plus element `+0x60`, turned by the parent's matrix; the element's `+0x70` | `0x004630D0` (`0x00463168`); `0x00398F90` (`0x00399101`, called from `0x004630D0` at `0x0046318B`) | `0x004630D0` (`0x004630DD`, `0x0046319E`, `0x004631C6`, `0x004631ED`, `0x0046321F`, `0x0046323A`); `0x00398F90` (`0x00398FA8`, called at `0x0046318B`) |
| `0x02CA5FB0` | `vec` | 0 (zero-filled tail of `.data`) | x: first the limit, definition `+0x7D4` (`0x004631CE`), read back with the factor as one vector (`0x004631E6`); then the result vector (`0x0046332F`): x `1 − factor × min(d, limit)`, the value stored at element `+0x2B0`, y `dy²`, z `dz²`, w `d²` | `0x004630D0` (`0x004631CE`, `0x004631DE`, `0x0046332F`) | `0x004630D0` (`0x004631E6`) |
| `0x02CA5FB4` | `f32` | 0 (zero-filled tail of `.data`) | the factor, definition `+0x7D8` (`0x004631DE`); after the result store, `dy²` | `0x004630D0` (`0x004631DE`, `0x0046332F`) | `0x004630D0` (`0x004631E6`) |
| `0x02CA5FC0` | `void*` | 0 (zero-filled tail of `.data`) | the element `0x00463D20` works on | `0x00463D20` (`0x00463D3E`) | `0x00463D20` (`0x00463DE0`) |
| `0x02CA5FC8` | `void*` | 0 (zero-filled tail of `.data`) | its definition | `0x00463D20` (`0x00463D49`) | `0x00463D20` (`0x00463DE7`) |
| `0x02CA5FD0` | `vec` | 0 (zero-filled tail of `.data`) | the position word, as for `0xA2` | `0x00463D20` (`0x00463DB8`); `0x00398F90` (`0x00399101`, called from `0x00463D20` at `0x00463DDB`) | `0x00463D20` (`0x00463D2D`, `0x00463DEE`, `0x00463E16`, `0x00463E3D`, `0x00463E6F`, `0x00463E8A`); `0x00398F90` (`0x00398FA8`, called at `0x00463DDB`) |
| `0x02CA5FE0` | `vec` | 0 (zero-filled tail of `.data`) | the limit, definition `+0x8C4`, then the result vector, as for `0xA2`; x goes to element `+0x2B0` | `0x00463D20` (`0x00463E1E`, `0x00463E2E`, `0x00463F7F`) | `0x00463D20` (`0x00463E36`) |
| `0x02CA5FE4` | `f32` | 0 (zero-filled tail of `.data`) | the factor, definition `+0x8C8`; then `dy²` | `0x00463D20` (`0x00463E2E`, `0x00463F7F`) | `0x00463D20` (`0x00463E36`) |
| `0x02CA8460` | `void*` | 0 (zero-filled tail of `.data`) | the element `0x005259E0` works on | `0x005259E0` (`0x005259FE`) | `0x005259E0` (`0x00525AA0`) |
| `0x02CA8468` | `void*` | 0 (zero-filled tail of `.data`) | its definition | `0x005259E0` (`0x00525A09`) | `0x005259E0` (`0x00525AA7`, `0x00525B6E`) |
| `0x02CA8470` | `vec` | 0 (zero-filled tail of `.data`) | the position word, as for `0xA2` (`0x00525A78`); then the second sum `d` is measured from (`0x00525B46`) | `0x005259E0` (`0x00525A78`, `0x00525B46`); `0x00398F90` (`0x00399101`, called from `0x005259E0` at `0x00525A9B` and `0x00525B69`) | `0x005259E0` (`0x005259ED`, `0x00525AAE`, `0x00525AC7`, `0x00525B84`, `0x00525BAB`, `0x00525BDF`, `0x00525BF3`); `0x00398F90` (`0x00398FA8`, called at `0x00525A9B` and `0x00525B69`) |
| `0x02CA8480` | `vec` | 0 (zero-filled tail of `.data`) | the limit, definition `+0xA54`, then the result vector; x goes to element `+0x250` | `0x005259E0` (`0x00525B8C`, `0x00525B9C`, `0x00525CE8`) | `0x005259E0` (`0x00525BA4`) |
| `0x02CA8484` | `f32` | 0 (zero-filled tail of `.data`) | the factor, definition `+0xA58`; then `dy²` | `0x005259E0` (`0x00525B9C`, `0x00525CE8`) | `0x005259E0` (`0x00525BA4`) |
| `0x02CA8490` | `void*` | 0 (zero-filled tail of `.data`) | the element `0x00527DC0` works on | `0x00527DC0` (`0x00527DDE`) | `0x00527DC0` (`0x00527E80`) |
| `0x02CA8498` | `void*` | 0 (zero-filled tail of `.data`) | its definition | `0x00527DC0` (`0x00527DE9`) | `0x00527DC0` (`0x00527E87`) |
| `0x02CA84A0` | `vec` | 0 (zero-filled tail of `.data`) | the position word, as for `0xA2` | `0x00527DC0` (`0x00527E58`); `0x00398F90` (`0x00399101`, called from `0x00527DC0` at `0x00527E7B`) | `0x00527DC0` (`0x00527DCD`, `0x00527E8E`, `0x00527EB6`, `0x00527EDD`, `0x00527F0F`, `0x00527F2A`); `0x00398F90` (`0x00398FA8`, called at `0x00527E7B`) |
| `0x02CA84B0` | `vec` | 0 (zero-filled tail of `.data`) | the limit, definition `+0xB64`, then the result vector; x goes to element `+0x250` | `0x00527DC0` (`0x00527EBE`, `0x00527ECE`, `0x0052801F`) | `0x00527DC0` (`0x00527ED6`) |
| `0x02CA84B4` | `f32` | 0 (zero-filled tail of `.data`) | the factor, definition `+0xB68`; then `dy²` | `0x00527DC0` (`0x00527ECE`, `0x0052801F`) | `0x00527DC0` (`0x00527ED6`) |
| `0x02CA84C0` | `void*` | 0 (zero-filled tail of `.data`) | the element `0x00528820` works on | `0x00528820` (`0x0052883E`) | `0x00528820` (`0x005288E0`) |
| `0x02CA84C8` | `void*` | 0 (zero-filled tail of `.data`) | its definition | `0x00528820` (`0x00528849`) | `0x00528820` (`0x005288E7`) |
| `0x02CA84D0` | `vec` | 0 (zero-filled tail of `.data`) | the position word, as for `0xA2` | `0x00528820` (`0x005288B8`); `0x00398F90` (`0x00399101`, called from `0x00528820` at `0x005288DB`) | `0x00528820` (`0x0052882D`, `0x005288EE`, `0x00528916`, `0x0052893D`, `0x0052896F`, `0x0052898A`); `0x00398F90` (`0x00398FA8`, called at `0x005288DB`) |
| `0x02CA84E0` | `vec` | 0 (zero-filled tail of `.data`) | the limit, definition `+0x854`, then the result vector; x goes to element `+0x250` | `0x00528820` (`0x0052891E`, `0x0052892E`, `0x00528A7F`) | `0x00528820` (`0x00528936`) |
| `0x02CA84E4` | `f32` | 0 (zero-filled tail of `.data`) | the factor, definition `+0x858`; then `dy²` | `0x00528820` (`0x0052892E`, `0x00528A7F`) | `0x00528820` (`0x00528936`) |
| `0x02CA84F0` | `void*` | 0 (zero-filled tail of `.data`) | the element `0x0052CF60` works on | `0x0052CF60` (`0x0052CF87`) | `0x0052CF60` (`0x0052D029`, `0x0052D1AC`, `0x0052D206`, `0x0052D23D`, `0x0052D2E0`, `0x0052D2FB`) |
| `0x02CA84F8` | `void*` | 0 (zero-filled tail of `.data`) | its definition | `0x0052CF60` (`0x0052CF92`) | `0x0052CF60` (`0x0052D030`, `0x0052D1B3`, `0x0052D225`, `0x0052D2D3`, `0x0052D30D`) |
| `0x02CA8500` | `vec` | 0 (zero-filled tail of `.data`) | the position word, as for `0xA2`; `0x0052CF60` later replaces element `+0x70` | `0x0052CF60` (`0x0052D001`); `0x00398F90` (`0x00399101`, called from `0x0052CF60` at `0x0052D024`) | `0x0052CF60` (`0x0052CF76`, `0x0052D037`, `0x0052D05F`, `0x0052D086`, `0x0052D0B8`, `0x0052D0D3`); `0x00398F90` (`0x00398FA8`, called at `0x0052D024`) |
| `0x02CA8510` | `vec` | 0 (zero-filled tail of `.data`) | the limit, definition `+0xBE4`, then the result vector; x goes to element `+0x2A0` | `0x0052CF60` (`0x0052D067`, `0x0052D077`, `0x0052D1D6`) | `0x0052CF60` (`0x0052D07F`) |
| `0x02CA8514` | `f32` | 0 (zero-filled tail of `.data`) | the factor, definition `+0xBE8`; then `dy²` | `0x0052CF60` (`0x0052D077`, `0x0052D1D6`) | `0x0052CF60` (`0x0052D07F`) |

## Modding notes

- A definition's type byte decides everything; a type without an arm in a table gets no behaviour
  for that method, and a draw arm that is `0x0016D6A0` draws nothing.
- Point and line blending comes from definition byte `+0x49` bits under mask `0xE0`; mode 6 takes the blend word
  from the `+0x30` track, so that track then serves as both alpha percent and blend.
- A type-`0x05` mesh index of 32 or more falls back to 0, and its definition holds 32 handles.
- The registry holds 128 elements of types `0x40`, `0x41`, `0x42` and `0xD0`; `0x00377190` returns 0
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x00181DD0` is called by `0x00332C40`, `0x003B99D0`, `0x003D7CE0`, `0x003D7DC0`, `0x003D7E90`; `0x002628B0` calls
  `0x00360B50`, `0x00360DD0`, `0x003636A0`.
- Audio: those functions are documented on [animation sounds](../Sound-And-Music/animation-sounds.md),
  [effect anchors and targets](effect-anchors-and-targets.md), [sound banks](../Sound-And-Music/sound-banks.md),
  [effect element runtime](effect-element-runtime.md), [music](../Sound-And-Music/music.md),
  [game over](../World-Areas-And-Travel/game-over.md).
- Save load settings: `0x002628B0` calls `0x002EF2B0`; those functions are documented on
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
