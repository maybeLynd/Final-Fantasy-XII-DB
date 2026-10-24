---
title: "Text drawing: how a line of menu text becomes glyph quads, the drawing classes that draw them, and the border shader that outlines it"
kind: "system"
category: "Menus and HUD"
addresses: "0x001E8070, 0x001E8580, 0x002142A0, 0x00213FE0, 0x00212E70, 0x00213140, 0x00214210, 0x0209D490"
---

## What the player sees

- Menu and dialogue text is drawn with a dark border around each letter, in the colour the text's palette entry gives.
- A line of text can fade from left to right as it appears.
- Text keeps its size and place at any window resolution, because glyph positions are mapped from a fixed
  1920 x 1080 space into clip space (`0x00213D31`-`0x00213D9A`).

## How it works

### From a glyph to a batch

1. The glyph loop `0x002A9F00` ([Fonts](fonts.md)) fills a 0xA0-byte draw record with the glyph's atlas box, its four
   corners, their colours and alpha, and a palette index, and calls `0x0017F7C0` (`0x002AA678`).
2. `0x0017F7C0` hands it to the emitter `0x001E8070([0x01F811F8], record)` (`0x0017F838`).
3. The emitter picks palette entry `index mod 28` (`0x001E94E0`), or the default entry at `+0x1358` for a negative index,
   and writes six 0x3C-byte vertices, corners 0, 1, 2 and 1, 2, 3 (`0x001E8140`-`0x001E8477`).
4. Each vertex carries two colours: the glyph colour from the palette's `+0x14`-`+0x20` and the border colour from
   `+0x04`-`+0x10`. Each red, green and blue is `palette channel x (c / 128) / 255`, with `c` the record's integer at
   `+0x5C`, `+0x6C` or `+0x7C` plus 4 x corner.
   - The border alpha is `+0x10 / 128`; the glyph alpha is `+0x20 / 128`, times `[record +0x8C + 4 x corner] / 128`
     and the corner factor below unless the line's byte `+0x2348` is set (`0x001E81AA`-`0x001E834D`, 1/128 at
     `0x008C5B34`, 255.0 at `0x008C5B40`).
5. The vertices go into the open batch of the current font (`0x001E8361`-`0x001E838C`). `0x001E9D20` picks that batch from
   the font id, one batch per font in each of two groups of 32 (`0x001E9E26`-`0x001E9E46`). The line's box and origin are
   widened to cover the glyph.

The palette entries are named `fontclut_%d` (`0x001E9533`). When a language's font folder is chosen (`0x001B44A0`),
`0x001E98A0` loads every entry from 0 to 27 that is not loaded yet through the reader `0x001C5F20`.

The font display's constructor `0x001E71B0` builds the 64 batches, `0x38` bytes each, with `0x001E7480`, which reserves
room for `0x400` vertices of `0x3C` bytes through `0x001E9AE0`; `0x001E7710` frees a batch's vertices. `0x001E74F0` and
`0x001E76B0` release partly built members when the constructor unwinds (`0x008985CC`, `0x0089866B`).

### The text flush

The next call of `0x0017F850` (the scope "display : draw Font") runs the flush `0x001E8580`. It builds drawing objects
from the arena `[0x01F7F4C0]` at five sites:

| Site | Class | Used for |
|---|---|---|
| `0x001E86BB` | `DynGeoFontTextSpecialShadowInstance` | the glyph mask |
| `0x001E88C4` | `DynGeoFontTextSpecialShadowInstance` | the coloured glyphs |
| `0x001E8A7D` | `DynGeoFontTextSpecialShadowFinalInstance` | the composite quad |
| `0x001E8F84` | `DynGeoFontTextSpecialFinalInstance` | text drawn straight to the screen |
| `0x001E91F3` | `DynGeoFontTextInstance` | text with the pre-drawn shadow atlas |

The flush chooses a path per line record (`0x001E85ED`-`0x001E8659`):

1. Byte `+0x2378` of the font display chooses between the Special classes and `DynGeoFontTextInstance`. It is
   `[0x01E02818] > 0` (`0x001E9F30`, `0x0029CE4A`-`0x0029CE55`); the shipped value is 1, and no instruction writes that
   cell: its only reference is the read in `0x00229E30`.
2. The record's offscreen byte `+0x28` chooses between the offscreen path and `Final`. Every text painter call passes 1
   to the begin call `0x001E9920` through `0x0017FA10` (`0x002AA52A`, `0x002AC801` and seven more), so menu text takes the
   offscreen path.

### The drawing objects

The constructors the flush calls set the objects up before any vertex is added:

- `0x00213A00(obj)` (`0x001E86BB`, `0x001E88C4`) and `0x00213960(obj)` (`0x001E8A7D`) build a `DynGeoFontTextSpecialShadowInstance`
  (vtable `0x00906E50`) and a `DynGeoFontTextSpecialShadowFinalInstance` (`0x00906F20`): each zeroes `+0x08` to `+0xF7`
  (`0x00861EC0`), clears `+0xF8`, `+0x100`, `+0x124`-`+0x12C`, `+0x138`-`+0x140`, `+0x14C`-`+0x154` and `+0x160`, and writes
  the identity matrix at `+0x11C` (1.0 at `+0x11C`, `+0x130`, `+0x144` and `+0x158`).
- `0x002130E0(obj)` (`0x001E91F3`) builds a `DynGeoFontTextInstance` (vtable `0x00906DC8`) and zeroes `+0x08` to `+0x3F`.
- `0x00213870(obj, n)` (`0x001E920A`) stores the vertex count at `+0x28` and takes two arrays of `n x 0x30` bytes from the
  arena `[0x01F7F4C0]` (`0x001A1470`) into `+0x18` and `+0x20`.
- `0x00213570(obj, v)` (`0x001E92CE`, once per `0x3C`-byte vertex) projects the vertex and appends it to both arrays
  while the count `+0x2C` is below `+0x28`. With the 4 x 4 matrix at `+0x54` it computes `w = x m60 + y m70 + m90`,
  `x' = (x m54 + y m64 + m84) / w` and `y' = (x m58 + y m68 + m88) / w`.
- It stores `(x' - 2048) x 2 / W` and `(y' - 2048) x -2 / H` into the vertex's `+0x0C` and `+0x10`, W x H being
  1920 x 1080 when `0x001B1620()` is set and 512 x 448 otherwise (`0x00213628`-`0x00213658` for x,
  `0x0021365D`-`0x00213688` for y).
- Entry `+0x2C` of each array takes the vertex's `+0x00`, `+0x04` at `+0x20`, `+0x24`, its `+0x0C`-`+0x18` at
  `+0x00`-`+0x0C`, and its `+0x1C`-`+0x28` (first array) or `+0x2C`-`+0x38` (second array) at `+0x10`-`+0x1C`; the
  count then moves on.

Text coordinates are centred on 2048 with y growing downward. The factor -2 (`0x008F3148`, `0x00213680`) turns them into
clip space, where y grows upward and both axes run from -1 to 1 across the W x H area. The vertex appender `0x00213D10`
maps its vertices the same way (`0x00213D31`-`0x00213D9A`).

### The drawing classes

The image's run-time type data names eight classes, each with its own vtable:

| Shape | Classes | Vtable slots |
|---|---|---:|
| general geometry | `DynGeoUIInstance` (`0x00906FB0`), `DynGeoTextureInstance` (`0x00904328`), `DynGeo3DInstance` (`0x009043D8`) | 21 |
| text with layers | `DynGeoFontTextSpecialInstance` (`0x00906DE8`) and its `Shadow`, `Final` and `ShadowFinal` (`0x00906E50`, `0x00906EB8`, `0x00906F20`) | 12 |
| text with a shadow atlas | `DynGeoFontTextInstance` (`0x00906DC8`) | 3 |

`DynGeoTextureInstance` and `DynGeo3DInstance` derive from `DynGeoUIInstance`; the three text variants derive from
`DynGeoFontTextSpecialInstance` directly. The general classes are built elsewhere (`0x001B0456`, `0x001B0218`) and draw no
text. The plain `DynGeoFontTextSpecialInstance` is never constructed; only its three variants are.

The 12-slot classes share every slot except 2 (the destructor), 6 (append a vertex), 10 (draw) and 11 (the renderer's
mode):

| Slot | Does |
|---:|---|
| `1` | the draw entry `0x00213FE0`: viewport, blend and state codes, identity matrix, then its own slot 10 (`0x00214191`) |
| `3` | sets the 4 x 4 matrix (`0x00214710`) |
| `4` | sets layer `i`'s texture (`0x00213B30`) |
| `5` | sizes layer `i`'s vertex array (`0x00213F90`) |
| `6` | appends a vertex to layer `i` (`0x00213D10`; `Final` `0x00213B40` applies its matrix first) |
| `10` | draws the layers |
| `11` | renderer mode 0, 1 for `Shadow`, 2 for `Final` and `ShadowFinal` (`0x00214890`, `0x002148B0`, `0x00214860`) |

Slots 4, 5 and 6 refuse a layer index of 10 or more (`0x00213B33`, `0x00213F93`, `0x00213D2B`).

### Layers and the shared draw body

Each Special instance holds ten layers, one per font used in the line: a layer's texture is that font's atlas and its
vertices are that font's glyphs (`0x001E8801`). The flush numbers the fonts without a limit, so the glyphs of an 11th
font in one line are dropped.

The shared body `0x002142A0` walks the ten layers. For each layer with a texture and vertices it binds the texture
(renderer slot 8, `0x0021432A`) and draws the vertices as a triangle list in chunks of at most 480 (`0x0021433A`-`0x0021438E`).
`Final` (`0x00214210`) and `Shadow` (`0x00214540`) run a short prefix and jump into it (`0x00214296`, `0x0021458D`):

- `Shadow` sets blend `(6, 7, 6, 7)` and program 9 (`0x00214550`-`0x0021457A`).
- `Final` would replace row 0 of the matrix with `(height x 16/9 / width, 0, 0, 0)` (`0x0021425C`-`0x0021427B`, `0x00183280`),
  1.0 at 1920 x 1080. Its gate `0x00182F50` needs the display object's first word to be 1; the constructor writes 0
  (`0x001DC5D6`), and no store to it is found at the 72 call sites of `0x001DDAB0`, so the row is left at the identity.
- `ShadowFinal` (`0x002143E0`) does not use the shared body: it draws layer 0 alone as a triangle strip with program 10
  (`0x0021446D`, `0x0021453C`).

Draw types are those of `0x006DA5A0`: 2 a triangle list, 3 a strip, 4 a fan. A strip and a fan of `n` vertices become
`3 x (n - 2)` triangle-list indices from the batch's base vertex word `+0x8010`, through `0x006DA790` (strip, the winding
alternating) and `0x006DA6F0` (fan, every triangle sharing the first vertex), written into the batch's index buffer of
0x4000 words (count `+0x08`); both refuse a draw that would overflow it (`0x006DA61A`, `0x006DA62B`).

### How menu text is drawn

On the offscreen path, each line is drawn in five ordered steps (`0x001E8664`-`0x001E8F49`):

1. A render target from the size ladder is bound: the smallest of ten sizes from 50 x 60 to 1920 x 1080 that holds the
   line (`0x001E97B0`, table `0x009018F0`).
2. A `Shadow` instance draws every glyph in white (`0x00213E30` with flag 1, `0x001E87B6`), a mask of the line.
   `0x002147B0` sets each `Shadow` instance's viewport to the target's width and height, target `+0x28` and `+0x2C`
   (`0x001E86D3`, `0x001E88DC`).
3. A `FontBorderOrderedGaussObject` filters the mask in two passes (`0x00212E70`, `0x00190260`): first across, with
   `SingleStepOffset` one texel wide, from the ladder target into its partner (`0x00186800`, `0x001867E0`), then down, one
   texel high, back again.
4. A second `Shadow` instance draws the glyphs in their own colour over it (flag 0, `0x001E89C6`).
5. A `FontBorderOrderedResetObject` restores the screen target (`0x00213040`), and a `ShadowFinal` instance draws the
   target onto the screen as one quad (`0x00214930`), with the line's first alpha on its left corners and its latest
   alpha on its right ones (`0x00214A67`-`0x00214AA8`). `0x002148F0` makes the target its layer-0 texture (`0x001E8AAF`), and
   `0x002145A0` maps each corner through the matrix `+0x11C` into clip space (`0x00214A62`).

Steps 1 and 5 are the executes (vtable slot 1) of a `FontBorderOrderedObject` (`0x00212F70`, slot
`0x00906D58`) and the `FontBorderOrderedResetObject` (`0x00213040`, slot `0x00906DA8`). `0x00212F70` keeps in
the byte `0x01FD3AC0` whether the context's bit `0x1` bracket was open (`0x00609710`: bit `0x1` of the
context's `+0x08`, stored at `0x00212F92`), closes it when it was (`0x00600A60(ctx, 2)`), binds the ladder
target `[object + 0x18]` (`0x00186800`, `0x0060D4F0`) and opens it (`0x005FEFD0(ctx, 1)`).

`0x00213040` closes it, restores the screen target (`0x001893C0`) and opens it again (`0x005FEFD0(ctx, 0)`) only when
`0x01FD3AC0` is set (`0x00213063`), so the pair leaves the bracket as step 1 found it.

The font display's constructor `0x001E71B0` builds the reset object through `0x00212D60`, which writes its vtable and
clears `+0x18`.

The border shader's parameters are `ColorBuffer`, `SingleStepOffset`, `FontBorderSetting` and `FontBorderColor`
(`0x001902FF`-`0x00190352`). The colour is the palette's border colour, and `FontBorderSetting` is the border width from
the font display, 4.0 when none is set (`0x0017F9A0`, `0x001B5210`). 64 of these objects are kept, one per border colour
and target size (`0x001E96A0`).

The 64 border objects are `0x38` bytes each at font display `+0x1500`. `0x001E96A0` takes the first whose byte `+0x20`
is set, or whose four colour floats `+0x24`-`+0x30` and size `+0x18` already match (`0x00212E30`, `0x001E970E`), and fills
a new one with `0x002130C0` (`0x001E9744`), which stores the four floats and clears `+0x20`. The reset `0x001E9380` runs
`0x00213090` on all 64 (`0x001E9399`), setting `+0x20` and the four floats to 1.0.

So the border is a shader pass over a white mask, and the glyphs are drawn once on top of it.

### The shadow atlas path

Each font also loads `<name>_shadow.dds.phyre` beside its atlas (`0x001B6212`). Only `DynGeoFontTextInstance` uses it:
its draw `0x00213140` draws the line twice through `0x002133D0`, first with the shadow atlas in the border colour, then
with the glyph atlas in the glyph colour. The flush copies the 16 bytes at font display `+0x13A0` into its `+0x40`
(`0x00213520`, `0x001E924E`) and the matrix `+0xE30` into its `+0x54` (`0x002134B0`, `0x001E928A`). With the shipped
`[0x01E02818]` of 1, the flush does not take this path.

### How a draw reaches the renderer

1. The flush submits each instance (`0x001FB810`), which wraps it in a `GeometryInstanceOrderedObject` (`0x001F48B0`,
   `0x001F4950`) on the ordered render list.
2. When the list runs, the wrapper's callback `0x001F4A10` calls the instance's slot 1 with the renderer (`0x001F4A35`).
3. Slot 1 sets the state and calls slot 10, which draws.

### Measuring text

Menu code measures a string without drawing it:

- `0x002B3050(font, text, &w, &h)` sets up a text context on the stack (`0x002AC1E0`) with the font `0x0039BAD0(font)`, and
  the alternate font record when that font is 7 and `0x00254A10` answers 0, and measures it with `0x002B3120`.
- `0x002B3120(context, &w, &h)` lays a copy of the context out with `0x002B24B0` and the terminator `0x009166EC`, and gives 0
  for both when the context has no text (`0x002B313F`).
- `0x0029CD00(text, font, scale, &w, &h)` and `0x0029CD90(text, font, scale, n, &w, &h)` scale the result by `scale` when it
  is above 0; `0x0029CD90` first adds `n` for every character (`0x002B4540`).
- `0x002B3E30(line)`, called from the line layout `0x002AF340`, closes a measured line: it adds the line's height to the
  total, keeps the widest line, and resets the line's values.
- `0x002B3E90(context, text)` measures `text` with `0x002AF340` under the terminator `0x00916544` and moves the context's
  shown count `+0x8C` on by that many, at most what `0x002B43C0` counts ([Message windows](message-windows.md)).

### Drawing text into a widget

A widget draws a string at a point through its draw record ([Menu sprites](menu-sprites.md)). A string that starts
with `ex` is UTF-16 (`0x00364980`), as the credits strings are ([Text codes](text-codes.md)), and takes its own path:

| Call | Ordinary string | UTF-16 string |
|---|---|---|
| `0x002D89E0(record, x, y, text, font, source)`, draw | a text context from `0x002B3400`, then `0x002DD680` | `0x003659F0`, then `0x002DD5D0` |
| `0x002D8B00(&w, &h, text, font, size)`, measure | `0x002B3050` | `0x003656A0` |
| `0x0029CCF0(out, size, plus, x, utf16)`, a sign | the glyph code of `+` or `-` (`0x002B5A20`) | `ex00` and the UTF-16 `+` or `-`, 8 bytes |
| `0x0029CCD0(x, font)`, a blank's width | the width of token 7 (`0x002ABAA0(0)`) | the advance of `0` in UTF-16 font `font - 1` (`0x003655F0`) |

`0x002DD680` hands the record's palette byte `+0x5C`, size `+0x60` and letter spacing `+0x65` to the context, and its
colour to `+0x30` (also kept at record `+0x94`): `rgb = (byte +0x90..+0x92 x s16 +0x5A) >> 7` and
`a = (byte +0x93 x s16 +0x58) >> 7` (`0x002DD6DD`-`0x002DD738`). It places the text at
(x, y) through `0x00397910` and draws it with `0x002B0280`. `0x002D8550` sets up the same and draws through `0x002AF960`, for
the confirm windows and the pause task (`0x0057C92A`, `0x00242373`, `0x00227F39`).

`0x00243860(list, record, dx, dy)` draws the type-5 text nodes of a typed list ([UI typed
lists](../Game-Files-And-Data-Tables/ui-typed-lists.md)) with a draw record; the per-element query `0x002D28E0` runs
it (`0x002D2C3F`, `0x002D2C64`). For each of the header's nodes that has the drawn bit `0x1`, type 5 and a string `+0x18`:

- the record takes the node's scale `+0x28` as the size `+0x60`, `+0x2C` as the palette byte `+0x5C`, `+0x2D`, `+0x2F`
  and bits 6-11 of `+0x08` as `+0x66`, `+0x65` and `+0x64`, and `+0x24` as the colour `+0x90` unless bit `0x40000` of the
  dword at `+0x5C` is set; node flag `0x2` makes the alpha scale `+0x5A` `0x80` for that node;
- with `+0x2D` bit `0x4` the node is clipped to its rectangle (`0x0029FE20`, `0x00249FD0`) and recentred from
  `[0x0208F574] / 4` and its `+0x0A`;
- a string `0x00364980` reports as UTF-16 is skipped; any other gets a context from `0x002B3400`, the colour bytes scaled
  as `0x002DD680` scales them, and `0x002B0280` draws at (dx + x, dy + node `+0x0E`); `0x002D8530(record)` follows a
  clipped node.

### The drawer's VIF packet

`0x002B0280` also fills a VIF1 packet for VU1 in the GS command buffers, as the map screens do
([Legacy PS2 GS layer](../Graphics/legacy-ps2-gs-layer.md)). It counts its glyphs in the painter's
`+0x10D4` (`[0x0209CC40]`) and closes the packet with `0x002B1C90` at 20 (`0x002B0CFA`) and when it ends (`0x002B1B60`):

1. `0x002B1C90` moves the data end `0x0209CC50` back 16 bytes and stores 1 in the last dword before the old end.
2. It writes the header at the cursor `0x0209E5A0`: `n | 0x10000000`, 0, `0x10000000` and the UNPACK code
   `0x6C008150 | n << 16`, with `n` the 16-byte records from the cursor to the data end.
3. After those records it appends `0x10000000`, 0, MSCALF `0x15000000` and FLUSHA `0x13000000`, and moves the
   cursor past them.
4. It moves the cursor `+0x08` of the buffer record `[0x0209CC48]` up to the new cursor, in whole 16 bytes, and flips
   the buffer (`0x003A1DB0`).

### Picking the batch

The interpreter `0x002AC5F0` sets the painter's base size with `0x002B1ED0`: `0x0017F980` and `0x0017F960` for a context with
the alternate font (bit `0x800` of `+0x44`), otherwise `0x0017F8A0` and `0x0017F880`, stored at `0x0209CC70` and `0x0209CC74`. It
opens a font's batch with `0x002AB820(font, group)`, which calls `0x001E9D20` through `0x0017FD30` with the painter
`[0x0209D480]` and keeps the pair at `0x0209CC30` and `0x0209CC34`.

### The font display's setters and base sizes

The text drawers reach the font display `[0x01F811F8]` (`0x001B5FA0`) through small entry points:

| Entry | Body | What the body does |
|---|---|---|
| `0x0017FB00(matrix)` | `0x001E9C80` (157 bytes) | copies the 64-byte 4x4 matrix to `+0xE30`-`+0xE6F`, unless byte `+0x2379` is non-zero (`0x001E9C80`); called from the drawers `0x002B0280`, `0x002AF960`, `0x002AC5F0`, `0x002A9F00`, `0x002AA800`, `0x002AAE40`, `0x002D28E0` and `0x003649A0` |
| `0x0017FC90(a, b, c, d)` | `0x001E9C40` | stores four corner factors for the next glyph: `+0x137C` = b·c, `+0x1380` = a·c, `+0x1384` = b·d, `+0x1388` = a·d (`0x001E9C5A`-`0x001E9C72`); called from `0x002B0280`, `0x002A9F00`, `0x002AA800`, `0x002AAE40`, `0x002AFDC0` and `0x002AEB20` |
| `0x0017F880` | `0x001E93C0` | font 1's `+0x30`, 23.0 when font 1 is not registered |
| `0x0017F8A0` | `0x001E9450` | font 1's `+0x2C`, 20.0 when not registered |
| `0x0017F960` | `0x001E9580` | font 3's `+0x30`, 23.0 when not registered |
| `0x0017F980` | `0x001E9610` | font 3's `+0x2C`, 20.0 when not registered |

The glyph emitter `0x001E8070` multiplies each of the six vertices' alpha by one of the four corner factors
(`+0x137C` + 4·i, unless the line's byte `+0x2348` is set), then sets all four back to 1.0
(`0x001E8563`), so a gradient set with `0x0017FC90` covers one glyph.

The four size bodies find the font in the registry `[0x01F81200]` (`0x001B5FB0`) with `0x001B51C0(registry,
slot)`, an ordered-tree lookup: from the root `+0x40` it walks nodes keyed by the `u32` at `+0x20` and
returns the node's `+0x28` for an exact match, or 0 (the header `+0x30`). The value is returned as it is
while the byte `0x01F811E0` is set (`0x001B1620`, written by `0x001B24B0`), and otherwise divided by the font's
scale `+0x34` (`0x001FDDB0`) and rounded up with `ceilf`. The batch opener `0x001E9D20` uses the same lookup
(`0x001E9DB9`).

### The colour table

Menu colours come from one table of 8-byte entries: a `u32` count, then per entry an RGBA `u32` and a byte. The field
HUD root's load callback `0x0029CED0` requests the file (`0x00249210`, `0x0029CEF6`), and `0x002DD810` keeps it at
`0x0215E6C0`. `0x002DD840`, run from `0x0029CF10` once the root's resources are in, publishes the count at `0x0215E6B8` and the
entries at `0x0215E6C8`.

`0x002DD7E0(n)` returns entry n's colour, or `0x80808080` for an index out of range or before the table is published,
and `0x002DD7B0(n)` its byte.

The battle log's formatter `0x00536410` takes a line's colour and byte for a category 0-7
and a side 0-1 through `0x0035D430` and `0x0035D400`, from the entry numbers at `0x00D10C60`: `0x18`-`0x1B`, `0x14`-`0x17`,
`0x1D`, `0x1D`, `0x1C`, `0x1C`, `0x1E`, `0x1E`, `0x1F`, `0x1F`; a category above 7 reads the first entry. `0x0029CF10` also fills the painter's rows from the two packs `0x0029CB50` and `0x0029CB60`
(`0x002B3480`, through `0x002432B0`). The `fontcolor.bin` copies under `myoshiok` in the extract are 2,108 bytes, 263
entries.

### Where the state is kept

| Object | Where | Holds |
|---|---|---|
| font display | `[0x01F811F8]`, 0x2380 bytes (`0x001B5F6D`) | the current font `+0x00`, the 64 batches `+0x30`, the matrix `+0xE30`, 28 palette entries `+0xF68`, the target ladder `+0x13C0`, the 64 border objects `+0x1500`, the reset object `+0x2300`, the two line records `+0x2320`, the path byte `+0x2378` |
| the display's `+0x28` | `0x0017F940()`, through `0x001B5FA0` and `0x005C52D0` | read by the text interpreter and drawers `0x002AC2F0`, `0x002AC5F0`, `0x002AE610`, `0x002AF340`, `0x002B0280` and `0x002B2150` |
| text painter | `0x0209D490`, 0x1108 bytes, published in `[0x0209CC40]` by `0x002B3550` | the terminator `+0x10C8`, tab stop `+0x10E0`, columns `+0x10EC`, line state `+0x10FC`, justification `+0x1104` ([Text codes](text-codes.md)) |
| text context | the interpreter's argument (`0x002AC5F0`) | size, spacing, colour and pager state |

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32[2]` | vftable | the family's table |
| `+0x008` | `u32[20]` | layerTexture | ten texture pointers (slot 4, read `0x002142D0`) |
| `+0x058` | `u32[20]` | layerVertices | ten pointers to `0x30`-byte vertices (slot 5, read `0x00214332`) |
| `+0x0A8` | `u32[10]` | layerCount | vertex capacity per layer (slot 5) |
| `+0x0D0` | `i32[10]` | layerCursor | next vertex per layer |
| `+0x0F8` | `u32[2]` | blendCode | the alpha-blend code, four 2-bit fields decoded through `0x00902750` by `0x001EE650`: slot 7 `0x002146F0` copies the font display's `+0x1390` (`0x001E874C`, `0x001E895A`, `0x001E8AC1`, `0x001E900C`); the constructors clear it; read only by slot 1 (`0x00214099`) |
| `+0x100` | `u32[2]` | testCode | bit `0x1` and bits `0xE` the alpha test and its method, bit `0x10000` and bits `0x60000` the depth test and its method, decoded through `0x008E2C60` and `0x008E2CE0` by `0x001EE7C0`: slot 8 `0x002148E0` copies the display's `+0x1398` (`0x001E875C`, `0x001E896A`, `0x001E8AD1`, `0x001E901C`); the constructors clear it; read only by slot 1 (`0x00214046`) |
| `+0x108` | `i32` | viewX | the viewport slot 1 hands to the renderer's slot `+0x100` (`0x0021402B`); slot 9 `0x00214830` copies `+0x108`-`+0x11B` from the display's `+0x13A0` for the `ShadowFinal` and `Final` objects (`0x001E8AE1`, `0x001E902C`); the constructors do not write it |
| `+0x10C` | `i32` | viewY | slot 9 |
| `+0x110` | `i32` | viewW | slot 9; for the `Shadow` objects `0x002147B0` sets the viewport to (0, 0, the render target's width `+0x28`, height `+0x2C`, 0) (`0x002147BC`-`0x00214814`, from `0x001E86D3` and `0x001E88DC`), and `0x00213E30` divides their vertices by this width and the height `+0x114` (`0x00213E4D`, `0x00213E8B`) |
| `+0x114` | `i32` | viewH | slot 9 |
| `+0x118` | `u32` | viewFlag | slot 9 |
| `+0x11C` | `f32[16]` | matrix | slot 3; identity when built |

The three subclasses add fields after `+0x15C`:

- `Shadow` adds the line origin at `+0x160`/`+0x164`: cleared by its constructor `0x00213A00` (`0x00213A8D`), set by
  `0x00214B10` from the flush (`0x001E8770`, `0x001E897E`) and subtracted from each vertex by `0x00213E30` (`0x00213E5E`,
  `0x00213E9A`).
- `ShadowFinal` keeps its render target index at `+0x160` (`0x002147A0`, read by `0x002148F0` and `0x00214930`).
- `Final` has a byte at `+0x168` that its constructor sets to 1 (`0x0021394D`) and `0x00214700` overwrites from the
  flush (`0x001E9074`); no instruction reads that byte.
- The plain class's last four bytes `+0x15C`-`+0x15F`, the same bytes of `Shadow` and `Final`, and `Final`'s
  `+0x169`-`+0x16F` are read and written by no function; nothing fixes their width.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | x | clip space; (x - 2048) x 2 / 1920 (`0x00213D31`-`0x00213D61`) |
| `+0x04` | `f32` | y | (y - 2048) x -2 / 1080 |
| `+0x08` | `f32` | z |  |
| `+0x0C` | `f32` | w |  |
| `+0x10` | `f32` | r |  |
| `+0x14` | `f32` | g |  |
| `+0x18` | `f32` | b |  |
| `+0x1C` | `f32` | a |  |
| `+0x20` | `f32` | u |  |
| `+0x24` | `f32` | v |  |

The byte `[0x01F811E0]` is set from `[0x01E0280C]`, shipped 1 (`0x0022A113`-`0x0022A120`, `0x001B24B0`); with it clear the
mapping divides by 512 and 448 instead (`0x001B1620`, `0x00213D38`).

The text painter `0x0209D490` keeps the line state of the text being drawn or measured:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10D0` | `u32` | textColour | the colour a `0F )` code set: the interpreter copies the text context's `+0x30` (`0x002AD46C`); `0x002B5390` seeds it from its record `+0x28` and copies it back after each segment (`0x002B5430`, `0x002B545E`, `0x002B55DB`) |
| `+0x10D4` | `u32` | packetGlyphs | glyphs in the current VIF packet; each drawer adds 1 and closes the packet at 20 (`0x002AA45F`, `0x002AAD5F`, `0x002AB4BA`, `0x002B0CE9`); `0x002B0280` and `0x002AF960` zero it when they start (`0x002B052E`, `0x002AFB2C`) |
| `+0x10D8` | `i32` | shownBudget | glyphs the type-out still lets this draw show: from the context's shown count `+0x8C` (`0x002ABEEB`, `0x002ABF3A`, `0x002AFB19`); each glyph takes one (`0x002AA0B1`, `0x002AA6E2`), a drawn number gives one back per digit (`0x002AE9E2`) |
| `+0x10DC` | `i32` | fadeStart | glyphs left before the type-out fade: from the context's `+0x90` (`0x002AFB26`), 32,000 from `0x002B0280` (`0x002B16FD`); at 0 or less a glyph's alpha is scaled by `+0x10E4` (`0x002AA05C`-`0x002AA086`) |
| `+0x10E0` | `f32` | tabStop | the pen position a `0F 2` with value 0 stores (`0x002ADC94`); a later `0F 2` with value v moves to it plus 2v (`0x002ADCB8`) |
| `+0x10E4` | `f32` | fadeAlpha | the context's byte `+0x9D` x its `+0x50` (`0x002AFB4C`); lowered by the step for each faded glyph (`0x002AA086`, `0x002AA6DA`) |
| `+0x10FD` | `i8` | indent | the last `0F 5` value (`0x002ADD57`), or the negated `0F 6` value (`0x002ADD8B`); returned by the list measure `0x002B24B0` (`0x002B277B`) |
| `+0x10FE` | `u8` | listCursorRoom | 1 when the choice list's fourth byte has bit `0x20` clear (`0x002AC883`); `0x002B24B0` then widens the list by 2 x 16 x the text scale (`0x002B26C4`-`0x002B26FE`) |
| `+0x10FF` | `i8` | measuring | 1 while `0x002B2150` only measures (`0x002B2278`), 0 from the drawers `0x002AF960` and `0x002B2970` (`0x002AFA7A`, `0x002B2A9F`); while it is 0 the choice-list arm counts the shown options (`0x002ACB2D`-`0x002ACB4B`) |
| `+0x1100` | `u8` | columnBeforeList | 1 when a column token `0x05` or `0x0A` comes before any choice list (`0x002ACD5B`, `0x002ACE6B`); returned by `0x002B24B0` (`0x002B270B`) |
| `+0x1101` | `u8` | listSeen | 1 once a choice list token `0x0E` has been read (`0x002AC879`); tested by the column tokens (`0x002ACD52`, `0x002ACE62`) |
| `+0x1103` | `u8` | bufferFlipped | 1 after the menu draw's opener `0x002DD4C0` flips the render buffer through `0x002B4710` (`0x002B4720`); cleared by `0x002B4700` (`0x002B4707`) from the closer `0x002DD420`; `0x002B0280` flips the buffer itself only while it is 0 (`0x002B04D3`-`0x002B04DC`) |

`0x002B24B0`, the choice-list measure, saves `+0x10C8`, `+0x10D8`, `+0x10E8`, `+0x10FC` and `+0x10FF`, stores its own
terminator at `+0x10C8` and clears `+0x10D8`, `+0x10FC`-`+0x10FF`, the column marks `+0x10EC`-`+0x10FB` and
`+0x1100`-`+0x1101` (`0x002B2570`-`0x002B25BC`), and restores the saved ones when it returns (`0x002B278C`-`0x002B27B7`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | loaded | set by `0x001E9515` |
| `+0x04` | `u32` | r2 | border or shadow colour |
| `+0x08` | `u32` | g2 |  |
| `+0x0C` | `u32` | b2 |  |
| `+0x10` | `u32` | a2 | over 128 |
| `+0x14` | `u32` | r1 | glyph colour |
| `+0x18` | `u32` | g1 |  |
| `+0x1C` | `u32` | b1 |  |
| `+0x20` | `u32` | a1 | over 128 |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | ownerKey | `0x001E9E2A` |
| `+0x04` | `u8` | emitted | set by `0x001E83A3` |
| `+0x08` | `f32` | minX | 1920 when reset |
| `+0x0C` | `f32` | minY | 1080 when reset |
| `+0x10` | `f32` | maxX |  |
| `+0x14` | `f32` | maxY |  |
| `+0x18` | `f32` | originX |  |
| `+0x1C` | `f32` | originY |  |
| `+0x20` | `f32` | firstAlpha | `0x001E84F9` |
| `+0x24` | `f32` | latestAlpha | `0x001E8523` |
| `+0x28` | `u8` | offscreen | set by begin `0x001E99AA` |
| `+0x29` | `u8` | firstPending cleared 0x001E84D0 |  |

## State

### The glyph metrics

`0x002AC2F0` reads the next glyph and works out its metrics. It keeps the base width and height `0x0209CC70` and
`0x0209CC74` and the unscaled advance `0x0209CC78`, then multiplies the four floats from `0x0209CC70` by the text size
`+0x34` into `0x0209CC60`-`0x0209CC6C`. When the x or y scale `+0x38`, `+0x3C` is not 1.0, it multiplies all four by the
x scale and the height by the y scale instead (`0x002AC54B`-`0x002AC5A6`).

The drawers read the scaled values to place the glyph's quad and move the pen. These are 0 in the file; the
eight-byte stores in the lists put 0 in two of them at once.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209CC60` | `f32` | 0 | the glyph's width on screen: `0x0209CC70` x size x x scale | `0x002AC2F0` (`0x002AC56A`, `0x002AC59F`); 0: `0x002AAE40` (`0x002AB703`), `0x002AC5F0` (`0x002AC62E`, `0x002AC7AA`), `0x002AE610` (`0x002AE841`, `0x002AEABB`), `0x002AF340` (`0x002AF624`, `0x002AF74A`, `0x002AF8EA`), `0x002AF960` (`0x002AFB73`), `0x002B0280` (`0x002B03F9`), `0x002B2150` (`0x002B2292`); other values: `0x002AE450` (`0x002AE4FD`), `0x002AEB20` (`0x002AECF1`), `0x002B0280` (`0x002B072E`, `0x002B0751`), `0x002B2150` (`0x002B240D`) | `0x002A9F00` (`0x002AA364`, `0x002AA40F`, `0x002AA498`); `0x002AA800` (`0x002AAAC2`, `0x002AAB3E`, `0x002AAB97`); `0x002AAE40` (`0x002AB203`, `0x002AB296`, `0x002AB2F7`); `0x002AF340` (`0x002AF644`, `0x002AF8C3`); `0x002B0280` (`0x002B0993`, `0x002B0A87`, `0x002B0ACF`); `0x002B2150` (`0x002B2262`, `0x002B23D9`) |
| `0x0209CC64` | `f32` | 0 | the glyph's height on screen: `0x0209CC74` x size x y scale | `0x002AC2F0` (`0x002AC56A`, `0x002AC59F`, `0x002AC5A6`); 0: `0x002AAE40` (`0x002AB703`), `0x002AC5F0` (`0x002AC62E`, `0x002AC7AA`), `0x002AE610` (`0x002AE841`, `0x002AEABB`), `0x002AF340` (`0x002AF624`, `0x002AF74A`, `0x002AF8EA`), `0x002AF960` (`0x002AFB73`), `0x002B0280` (`0x002B03F9`), `0x002B2150` (`0x002B2292`); other values: `0x002AC5F0` (`0x002ACB71`, `0x002ACB89`, `0x002ACCD6`, `0x002ACDC8`, `0x002ACEE8`, `0x002ACFAC`, `0x002AD75E`, `0x002ADAD7`, `0x002AE017`), `0x002AE450` (`0x002AE51C`), `0x002AE610` (`0x002AEAD1`), `0x002AEB20` (`0x002AED09`), `0x002B0280` (`0x002B072E`, `0x002B0751`, `0x002B0758`, `0x002B0F40`, `0x002B0FBB`, `0x002B105E`, `0x002B10BC`), `0x002B2150` (`0x002B240D`) | `0x002A9F00` (`0x002AA35C`, `0x002AA4FA`); `0x002AA800` (`0x002AAACA`, `0x002AABB6`); `0x002AAE40` (`0x002AB1FB`, `0x002AB31E`); `0x002AEB20` (`0x002AED45`); `0x002AF340` (`0x002AF7B9`, `0x002AF7F0`); `0x002B0280` (`0x002B098B`, `0x002B0B40`); `0x002B2150` (`0x002B2262`, `0x002B239C`, `0x002B23BD`) |
| `0x0209CC68` | `f32` | 0 | the glyph's advance on screen, which the drawers add to the pen x (`0x002B188B`): `0x0209CC78` x size x x scale, or the one-glyph advance `+0xA9` that `0F 4` sets, which `0x002AC2F0` then clears (`0x002AC5AE`-`0x002AC5CB`) | `0x002AC2F0` (`0x002AC56A`, `0x002AC59F`, `0x002AC5C3`); 0: `0x002AAE40` (`0x002AB70A`), `0x002AC5F0` (`0x002AC638`, `0x002AC7B1`), `0x002AE610` (`0x002AE848`, `0x002AEAC2`), `0x002AF340` (`0x002AF62B`, `0x002AF756`, `0x002AF8F1`), `0x002AF960` (`0x002AFB84`), `0x002B0280` (`0x002B0400`), `0x002B2150` (`0x002B229C`); other values: `0x002AC5F0` (`0x002ACB3A`, `0x002ACCA9`, `0x002ACDB8`, `0x002ACED5`, `0x002ACFA4`, `0x002AD0C7`, `0x002AD144`, `0x002AD756`, `0x002ADACF`, `0x002ADCD0`, `0x002AE009`), `0x002AE450` (`0x002AE529`, `0x002AE5A7`), `0x002AE610` (`0x002AEAC9`), `0x002AEB20` (`0x002AED17`, `0x002AED35`), `0x002B0280` (`0x002B072E`, `0x002B0751`, `0x002B0776`, `0x002B0F1F`, `0x002B0FAC`, `0x002B104A`, `0x002B10D4`, `0x002B11EB`, `0x002B126F`, `0x002B15EC`), `0x002B2150` (`0x002B240D`) | `0x002A9F00` (`0x002AA734`); `0x002AA800` (`0x002AAD9F`); `0x002AAE40` (`0x002AB66A`); `0x002AE610` (`0x002AE7DC`); `0x002AF340` (`0x002AF7A1`, `0x002AF7DC`); `0x002B0280` (`0x002B0D5A`, `0x002B0F5C`, `0x002B0FDE`, `0x002B10F0`, `0x002B188B`); `0x002B2150` (`0x002B2262`, `0x002B23A4`, `0x002B23C5`) |
| `0x0209CC78` | `f32` | 0 | the glyph's unscaled advance: its width (`0x0017F9C0` of the glyph record's `+0x1C`, or bits 32-36 of its character-map entry) plus the letter spacing `+0x4C`, plus 1.5, or 0.5 when `0x00254A10` answers 0, for a glyph marked by bit `0x80000000` of its entry while `+0x40` is not 0 (`0x002AC4B8`-`0x002AC510`) | `0x002AC2F0` (0: `0x002AC316`; `0x002AC510`); `0x002B0280` (0: `0x002B040E`; `0x002B06D3`); 0: `0x002AC5F0` (`0x002AD1D9`), `0x002AF960` (`0x002AFA1F`) | `0x002AC2F0` (`0x002AC55C`); `0x002B0280` (`0x002B0727`) |
| `0x0209CC7C` | `f32` | 0 | the kerning before the glyph, unscaled: `0x0017F8E0` of the glyph's code point `+0x20` ([kerning](fonts.md)), taken when `0x0017F940()` answers non-zero, the glyph record exists and its code point is not -1, and 0 otherwise; the multiply turns it into `0x0209CC6C` | `0x002AC2F0`: 0 with `0x0209CC78` (`0x002AC316`), the kerning (`0x002AC53B`); `0x002B0280`: 0 with `0x0209CC78` (`0x002B040E`), the kerning (`0x002B06FF`) or 0 (`0x002B0709`); 0 with `0x0209CC78`: `0x002AC5F0` (`0x002AD1D9`), `0x002AF960` (`0x002AFA1F`) | `0x002AC2F0` (`0x002AC55C`); `0x002B0280` (`0x002B0727`), the fourth float of the 16-byte multiply |

Nothing else reads or writes these five. The addresses taken near them, `0x0209CC3C` by `0x001AF470` (a `UISize.json` cell, [Screen
layouts](screen-layouts.md)) and `0x0209CC30` by `0x002A84F0` (the end of a loop over `0x0209CC18`-`0x0209CC28`), reach none
of them.

### The screen-width counter

The drawers `0x002A9F00`, `0x002AA800`, `0x002AAE40` and `0x002B0280` split a line's batch every 1920 units of pen travel.
When a glyph's right edge over 1920 passes `0x01E0CDF4` and the context's `+0x20` is set, the drawer:

1. flushes the batch (`0x0017F850`) and begins again with `0x0017FA10(context +0xB8, 0x44, 1)`;
2. reselects the font `0x0209CC30`, `0x0209CC34` (`0x0017FD30`) and the transform `+0x20` (`0x0017FB00`);
3. adds 1.0 to `0x01E0CDF4` (`0x002B0B35`-`0x002B0BA9` in `0x002B0280`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01E0CDF4` | `f32` | 1.0 | the screen width, in units of 1920, at which the next split falls | 1.0: `0x002B0280` at the start of a draw (`0x002B034D`), `0x002AF960` (`0x002AF9E9`); plus 1.0: `0x002A9F00` (`0x002AA583`), `0x002AA800` (`0x002AAC47`), `0x002AAE40` (`0x002AB3BD`), `0x002B0280` (`0x002B0BA9`) | `0x002A9F00` (`0x002AA4EF`, `0x002AA565`); `0x002AA800` (`0x002AABDB`, `0x002AAC33`); `0x002AAE40` (`0x002AB33D`, `0x002AB3A7`); `0x002B0280` (`0x002B0B35`, `0x002B0B9A`) |
| `0x01E0CE0C` | `f32` | 10.0 | `0x0024ABC0()` x 4, 15.0 in the 1920 frame, stored when the text painter is set up and the language test `0x00254A10` answers 0 | `0x002B3550` (`0x002B3587`), from `0x0029CE40` | no instruction |

### Code scratch

A number argument of `0F .` ([Text codes](text-codes.md)) is drawn by `0x002AE610` from a copy of the escape. The
interpreter and the drawer each copy the escape's four bytes from the selector into their own scratch and set byte 1 to
`0xFF`. `0x002AE610` reads bytes 1 and 2 through `0x003FFC60` (`0x002AE760`) and draws the number only when byte 1 & `0x7F`
is `0x7F` (`0x002AE823`). Both scratches hold `2D 80 80 00` in the file, which the copy replaces.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01E0CE04` | `u8[4]` | `2D 80 80 00` | the drawer's copy of a `0F .` escape with a number argument; byte 1, `0x01E0CE05`, is set to `0xFF` | `0x002B0280`: the copy (`0x002B194D`), then `0x01E0CE05` (`0x002B195A`) | `0x002AE610`, called with the address (`0x002B1961`, `0x002B19A2`), through `0x003FFC60` (`0x003FFC68`, `0x003FFC91`, `0x003FFCA9`, `0x003FFCC0`) |
| `0x01E0CE08` | `u8[4]` | `2D 80 80 00` | the interpreter's copy of the same; byte 1, `0x01E0CE09`, is set to `0xFF` | `0x002AC5F0`: the copy (`0x002ADAFA`), then `0x01E0CE09` (`0x002ADB07`) | `0x002AE610`, called with the address (`0x002ADB98`, `0x002ADBC9`), the same way |
| `0x01E0CDFF` | `u8` | `0x80` | the last byte of the static code `0F ? 81 n` at `0x01E0CDFC`: `n` with bit `0x80` set, the argument of `0x002AC2C0(n)` | `0x002AC2C0` (`0x002AC2CA`) | through the address `0x002AC2C0` returns: its one caller `0x003F92B0`, the location text, copies the code into the text with `0x00254F30` (`0x003F92FA`-`0x003F930B`) |

No other instruction reaches these globals. The `UISize.json` cells `0x001AF470` registers near them are separate
globals.

## Modding notes

- A text palette entry's second colour is the border colour.
- The border's look is the `FontBorder` shader's parameters, not the glyph draw; its width is the font display's
  border setting (`0x001B5210`).
- Text using more than ten fonts in one line loses the glyphs of the extra fonts.
- Setting `[0x01E02818]` to 0 switches menu text to the pre-drawn shadow atlas path.

## Related

- [Fonts](fonts.md) - glyph records, kerning and advances.
- [Text codes](text-codes.md) - the codes that set colour, size and layout.
- [Menus](menus.md) - the screens that draw text.
