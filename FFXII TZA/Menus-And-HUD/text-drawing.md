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
   `[0x01E02818] > 0` (`0x001E9F30`, `0x0029CE4A`-`0x0029CE55`); the shipped value is 1, and the image holds no direct,
   image-base-relative or pointer writer of that cell.
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
  and bits 6-11 of `+0x08` as `+0x66`, `+0x65` and `+0x64`, and `+0x24` as the colour `+0x90` unless bit 18 of the
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
the alternate font (bit 11 of `+0x44`), otherwise `0x0017F8A0` and `0x0017F880`, stored at `0x0209CC70` and `0x0209CC74`. It
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
| `+0x0F8` | `u32[2]` | blendCode | slot 7; decoded by `0x001EE650` |
| `+0x100` | `u32[2]` | stateCode | slot 8; decoded by `0x001EE7C0` |
| `+0x108` | `i32` | viewX | slot 9 |
| `+0x10C` | `i32` | viewY | slot 9 |
| `+0x110` | `i32` | viewW | slot 9; the target width on the offscreen path |
| `+0x114` | `i32` | viewH | slot 9 |
| `+0x118` | `u32` | viewFlag | slot 9 |
| `+0x11C` | `f32[16]` | matrix | slot 3; identity when built |

`Shadow` adds the line origin at `+0x160`/`+0x164` (`0x00214B10`), `ShadowFinal` the target index at `+0x160`
(`0x002147A0`), and `Final` a byte at `+0x168` (`0x0021394D`).

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
