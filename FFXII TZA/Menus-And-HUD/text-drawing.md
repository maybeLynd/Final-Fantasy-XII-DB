---
title: "Text drawing: how a line of menu text becomes glyph quads, the drawing classes that draw them, and the border shader that outlines it"
kind: "system"
category: "Menus and HUD"
addresses: "001E8070, 001E8580, 002142A0, 00213FE0, 00212E70, 00213140, 00214210, 0209D490"
---

## What the player sees

- Menu and dialogue text is drawn with a dark border around each letter, in the colour the text's palette entry gives.
- A line of text can fade from left to right as it appears.
- Text keeps its size and place at any window resolution, because glyph positions are mapped from a fixed
  1920 x 1080 space into clip space (`00213D31`-`00213D9A`).

## How it works

### From a glyph to a batch

1. The glyph loop `002A9F00` ([Fonts](fonts.md)) fills a `A0`<sub>h</sub>-byte draw record with the glyph's atlas box, its four
   corners, their colours and alpha, and a palette index, and calls `0017F7C0` (`002AA678`).
2. `0017F7C0` hands it to the emitter `001E8070([01F811F8], record)` (`0017F838`).
3. The emitter picks palette entry `index mod 28` (`001E94E0`), or the default entry at `+1358`<sub>h</sub> for a negative index,
   and writes six `3C`<sub>h</sub>-byte vertices, corners 0, 1, 2 and 1, 2, 3 (`001E8140`-`001E8477`).
4. Each vertex carries two colours: the glyph colour from the palette's `+14`<sub>h</sub>-`+20`<sub>h</sub> and the border colour from
   `+04`<sub>h</sub>-`+10`<sub>h</sub>, both scaled by the corner colour (`001E81FC`-`001E834D`).
5. The vertices go into the open batch of the current font (`001E8361`-`001E838C`). `001E9D20` picks that batch from
   the font id, one batch per font in each of two groups of 32 (`001E9E26`-`001E9E46`). The line's box and origin are
   widened to cover the glyph.

The palette entries are named `fontclut_%d` (`001E9533`). When a language's font folder is chosen (`001B44A0`),
`001E98A0` loads every entry from 0 to 27 that is not loaded yet through the reader `001C5F20`.

The font display's constructor `001E71B0` builds the 64 batches, `38`<sub>h</sub> bytes each, with `001E7480`, which reserves
room for `400`<sub>h</sub> vertices of `3C`<sub>h</sub> bytes through `001E9AE0`; `001E7710` frees a batch's vertices. `001E74F0` and
`001E76B0` release partly built members when the constructor unwinds (`008985CC`, `0089866B`).

### The text flush

The next call of `0017F850` (the scope "display : draw Font") runs the flush `001E8580`. It builds drawing objects
from the arena `[01F7F4C0]` at five sites:

| Site | Class | Used for |
|---|---|---|
| `001E86BB` | `DynGeoFontTextSpecialShadowInstance` | the glyph mask |
| `001E88C4` | `DynGeoFontTextSpecialShadowInstance` | the coloured glyphs |
| `001E8A7D` | `DynGeoFontTextSpecialShadowFinalInstance` | the composite quad |
| `001E8F84` | `DynGeoFontTextSpecialFinalInstance` | text drawn straight to the screen |
| `001E91F3` | `DynGeoFontTextInstance` | text with the pre-drawn shadow atlas |

The flush chooses a path per line record (`001E85ED`-`001E8659`):

1. Byte `+2378`<sub>h</sub> of the font display chooses between the Special classes and `DynGeoFontTextInstance`. It is
   `[01E02818] > 0` (`001E9F30`, `0029CE4A`-`0029CE55`); the shipped value is 1, and the image holds no direct,
   image-base-relative or pointer writer of that cell.
2. The record's offscreen byte `+28`<sub>h</sub> chooses between the offscreen path and `Final`. Every text painter call passes 1
   to the begin call `001E9920` through `0017FA10` (`002AA52A`, `002AC801` and seven more), so menu text takes the
   offscreen path.

### The drawing classes

The image's run-time type data names eight classes, each with its own vtable:

| Shape | Classes | Vtable slots |
|---|---|---:|
| general geometry | `DynGeoUIInstance` (`00906FB0`), `DynGeoTextureInstance` (`00904328`), `DynGeo3DInstance` (`009043D8`) | 21 |
| text with layers | `DynGeoFontTextSpecialInstance` (`00906DE8`) and its `Shadow`, `Final` and `ShadowFinal` (`00906E50`, `00906EB8`, `00906F20`) | 12 |
| text with a shadow atlas | `DynGeoFontTextInstance` (`00906DC8`) | 3 |

`DynGeoTextureInstance` and `DynGeo3DInstance` derive from `DynGeoUIInstance`; the three text variants derive from
`DynGeoFontTextSpecialInstance` directly. The general classes are built elsewhere (`001B0456`, `001B0218`) and draw no
text. The plain `DynGeoFontTextSpecialInstance` is never constructed; only its three variants are.

The 12-slot classes share every slot except 2 (the destructor), 6 (append a vertex), 10 (draw) and 11 (the renderer's
mode):

| Slot | Does |
|---:|---|
| `1` | the draw entry `00213FE0`: viewport, blend and state codes, identity matrix, then its own slot 10 (`00214191`) |
| `3` | sets the 4 x 4 matrix (`00214710`) |
| `4` | sets layer `i`'s texture (`00213B30`) |
| `5` | sizes layer `i`'s vertex array (`00213F90`) |
| `6` | appends a vertex to layer `i` (`00213D10`; `Final` `00213B40` applies its matrix first) |
| `10` | draws the layers |
| `11` | renderer mode 0, 1 for `Shadow`, 2 for `Final` and `ShadowFinal` (`00214890`, `002148B0`, `00214860`) |

Slots 4, 5 and 6 refuse a layer index of 10 or more (`00213B33`, `00213F93`, `00213D2B`).

### Layers and the shared draw body

Each Special instance holds ten layers, one per font used in the line: a layer's texture is that font's atlas and its
vertices are that font's glyphs (`001E8801`). The flush numbers the fonts without a limit, so the glyphs of an 11th
font in one line are dropped.

The shared body `002142A0` walks the ten layers. For each layer with a texture and vertices it binds the texture
(renderer slot 8, `0021432A`) and draws the vertices as a triangle list in chunks of at most 480 (`0021433A`-`0021438E`).
`Final` (`00214210`) and `Shadow` (`00214540`) run a short prefix and jump into it (`00214296`, `0021458D`):

- `Shadow` sets blend `(6, 7, 6, 7)` and program 9 (`00214550`-`0021457A`).
- `Final` would replace row 0 of the matrix with `(height x 16/9 / width, 0, 0, 0)` (`0021425C`-`0021427B`, `00183280`),
  1.0 at 1920 x 1080. Its gate `00182F50` needs the display object's first word to be 1; the constructor writes 0
  (`001DC5D6`), and no store to it is found at the 72 call sites of `001DDAB0`, so the row is left at the identity.
- `ShadowFinal` (`002143E0`) does not use the shared body: it draws layer 0 alone as a triangle strip with program 10
  (`0021446D`, `0021453C`).

Draw types are those of `006DA5A0`: 2 a triangle list, 3 a strip, 4 a fan. A strip and a fan of `n` vertices become
`3 x (n - 2)` triangle-list indices from the batch's base vertex word `+8010`<sub>h</sub>, through `006DA790` (strip, the winding
alternating) and `006DA6F0` (fan, every triangle sharing the first vertex), written into the batch's index buffer of
`4000`<sub>h</sub> words (count `+08`<sub>h</sub>); both refuse a draw that would overflow it (`006DA61A`, `006DA62B`).

### How menu text is drawn

On the offscreen path, each line is drawn in five ordered steps (`001E8664`-`001E8F49`):

1. A render target from the size ladder is bound: the smallest of ten sizes from 50 x 60 to 1920 x 1080 that holds the
   line (`001E97B0`, table `009018F0`).
2. A `Shadow` instance draws every glyph in white (`00213E30` with flag 1, `001E87B6`), a mask of the line.
   `002147B0` sets each `Shadow` instance's viewport to the target's width and height, target `+28`<sub>h</sub> and `+2C`<sub>h</sub>
   (`001E86D3`, `001E88DC`).
3. A `FontBorderOrderedGaussObject` filters the mask in two passes (`00212E70`, `00190260`): first across, with
   `SingleStepOffset` one texel wide, from the ladder target into its partner (`00186800`, `001867E0`), then down, one
   texel high, back again.
4. A second `Shadow` instance draws the glyphs in their own colour over it (flag 0, `001E89C6`).
5. A `FontBorderOrderedResetObject` restores the screen target (`00213040`), and a `ShadowFinal` instance draws the
   target onto the screen as one quad (`00214930`), with the line's first alpha on its left corners and its latest
   alpha on its right ones (`00214A67`-`00214AA8`). `002148F0` makes the target its layer-0 texture (`001E8AAF`), and
   `002145A0` maps each corner through the matrix `+11C`<sub>h</sub> into clip space (`00214A62`).

The font display's constructor `001E71B0` builds the reset object through `00212D60`, which writes its vtable and
clears `+18`<sub>h</sub>.

The border shader's parameters are `ColorBuffer`, `SingleStepOffset`, `FontBorderSetting` and `FontBorderColor`
(`001902FF`-`00190352`). The colour is the palette's border colour, and `FontBorderSetting` is the border width from
the font display, 4.0 when none is set (`0017F9A0`, `001B5210`). 64 of these objects are kept, one per border colour
and target size (`001E96A0`).

So the border is a shader pass over a white mask, and the glyphs are drawn once on top of it.

### The shadow atlas path

Each font also loads `<name>_shadow.dds.phyre` beside its atlas (`001B6212`). Only `DynGeoFontTextInstance` uses it:
its draw `00213140` draws the line twice through `002133D0`, first with the shadow atlas in the border colour, then
with the glyph atlas in the glyph colour. The flush copies the 16 bytes at font display `+13A0`<sub>h</sub> into its `+40`<sub>h</sub>
(`00213520`, `001E924E`) and the matrix `+E30`<sub>h</sub> into its `+54`<sub>h</sub> (`002134B0`, `001E928A`). With the shipped
`[01E02818]` of 1, the flush does not take this path.

### How a draw reaches the renderer

1. The flush submits each instance (`001FB810`), which wraps it in a `GeometryInstanceOrderedObject` (`001F48B0`,
   `001F4950`) on the ordered render list.
2. When the list runs, the wrapper's callback `001F4A10` calls the instance's slot 1 with the renderer (`001F4A35`).
3. Slot 1 sets the state and calls slot 10, which draws.

### Measuring text

Menu code measures a string without drawing it:

- `002B3050(font, text, &w, &h)` sets up a text context on the stack (`002AC1E0`) with the font `0039BAD0(font)`, and
  the alternate font record when that font is 7 and `00254A10` answers 0, and measures it with `002B3120`.
- `002B3120(context, &w, &h)` lays a copy of the context out with `002B24B0` and the terminator `009166EC`, and gives 0
  for both when the context has no text (`002B313F`).
- `0029CD00(text, font, scale, &w, &h)` and `0029CD90(text, font, scale, n, &w, &h)` scale the result by `scale` when it
  is above 0; `0029CD90` first adds `n` for every character (`002B4540`).
- `002B3E30(line)`, called from the line layout `002AF340`, closes a measured line: it adds the line's height to the
  total, keeps the widest line, and resets the line's values.
- `002B3E90(context, text)` measures `text` with `002AF340` under the terminator `00916544` and moves the context's
  shown count `+8C`<sub>h</sub> on by that many, at most what `002B43C0` counts ([Message windows](message-windows.md)).

### Drawing text into a widget

A widget draws a string at a point through its draw record ([Menu sprites](menu-sprites.md)). A string that starts
with `ex` is UTF-16 (`00364980`), as the credits strings are ([Text codes](text-codes.md)), and takes its own path:

| Call | Ordinary string | UTF-16 string |
|---|---|---|
| `002D89E0(record, x, y, text, font, source)`, draw | a text context from `002B3400`, then `002DD680` | `003659F0`, then `002DD5D0` |
| `002D8B00(&w, &h, text, font, size)`, measure | `002B3050` | `003656A0` |
| `0029CCF0(out, size, plus, x, utf16)`, a sign | the glyph code of `+` or `-` (`002B5A20`) | `ex00` and the UTF-16 `+` or `-`, 8 bytes |
| `0029CCD0(x, font)`, a blank's width | the width of token 7 (`002ABAA0(0)`) | the advance of `0` in UTF-16 font `font - 1` (`003655F0`) |

`002DD680` hands the record's palette byte `+5C`<sub>h</sub>, size `+60`<sub>h</sub> and letter spacing `+65`<sub>h</sub> to the context, and its
colour `+90`<sub>h</sub> scaled by the alpha `+5A`<sub>h</sub> (and `+58`<sub>h</sub> for the alpha byte) to `+30`<sub>h</sub>. It places the text at
(x, y) through `00397910` and draws it with `002B0280`. `002D8550` sets up the same and draws through `002AF960`, for
the confirm windows and the pause task (`0057C92A`, `00242373`, `00227F39`).

### Picking the batch

The interpreter `002AC5F0` sets the painter's base size with `002B1ED0`: `0017F980` and `0017F960` for a context with
the alternate font (bit 11 of `+44`<sub>h</sub>), otherwise `0017F8A0` and `0017F880`, stored at `0209CC70` and `0209CC74`. It
opens a font's batch with `002AB820(font, group)`, which calls `001E9D20` through `0017FD30` with the painter
`[0209D480]` and keeps the pair at `0209CC30` and `0209CC34`.

### The colour table

Menu colours come from one table of 8-byte entries: a `u32` count, then per entry an RGBA `u32` and a byte. The field
HUD root's load callback `0029CED0` requests the file (`00249210`, `0029CEF6`), and `002DD810` keeps it at
`0215E6C0`. `002DD840`, run from `0029CF10` once the root's resources are in, publishes the count at `0215E6B8` and the
entries at `0215E6C8`.

`002DD7E0(n)` returns entry n's colour, or `80808080`<sub>h</sub> for an index out of range or before the table is published,
and `002DD7B0(n)` its byte.

The battle log's formatter `00536410` takes a line's colour and byte for a category 0-7
and a side 0-1 through `0035D430` and `0035D400`, from the entry numbers at `00D10C60`: `18`<sub>h</sub>-`1B`<sub>h</sub>, `14`<sub>h</sub>-`17`<sub>h</sub>,
`1D`<sub>h</sub>, `1D`<sub>h</sub>, `1C`<sub>h</sub>, `1C`<sub>h</sub>, `1E`<sub>h</sub>, `1E`<sub>h</sub>, `1F`<sub>h</sub>, `1F`<sub>h</sub>; a category above 7 reads the first entry. `0029CF10` also fills the painter's rows from the two packs `0029CB50` and `0029CB60`
(`002B3480`, through `002432B0`). The `fontcolor.bin` copies under `myoshiok` in the extract are 2,108 bytes, 263
entries.

### Where the state is kept

| Object | Where | Holds |
|---|---|---|
| font display | `[01F811F8]`, `2380`<sub>h</sub> bytes (`001B5F6D`) | the current font `+00`<sub>h</sub>, the 64 batches `+30`<sub>h</sub>, the matrix `+E30`<sub>h</sub>, 28 palette entries `+F68`<sub>h</sub>, the target ladder `+13C0`<sub>h</sub>, the 64 border objects `+1500`<sub>h</sub>, the reset object `+2300`<sub>h</sub>, the two line records `+2320`<sub>h</sub>, the path byte `+2378`<sub>h</sub> |
| the display's `+28`<sub>h</sub> | `0017F940()`, through `001B5FA0` and `005C52D0` | read by the text interpreter and drawers `002AC2F0`, `002AC5F0`, `002AE610`, `002AF340`, `002B0280` and `002B2150` |
| text painter | `0209D490`, `1108`<sub>h</sub> bytes, published in `[0209CC40]` by `002B3550` | the terminator `+10C8`<sub>h</sub>, tab stop `+10E0`<sub>h</sub>, columns `+10EC`<sub>h</sub>, line state `+10FC`<sub>h</sub>, justification `+1104`<sub>h</sub> ([Text codes](text-codes.md)) |
| text context | the interpreter's argument (`002AC5F0`) | size, spacing, colour and pager state |

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u32[2]` | vftable | the family's table |
| `008`<sub>h</sub> | `u32[20]` | layerTexture | ten texture pointers (slot 4, read `002142D0`) |
| `058`<sub>h</sub> | `u32[20]` | layerVertices | ten pointers to `30`<sub>h</sub>-byte vertices (slot 5, read `00214332`) |
| `0A8`<sub>h</sub> | `u32[10]` | layerCount | vertex capacity per layer (slot 5) |
| `0D0`<sub>h</sub> | `i32[10]` | layerCursor | next vertex per layer |
| `0F8`<sub>h</sub> | `u32[2]` | blendCode | slot 7; decoded by `001EE650` |
| `100`<sub>h</sub> | `u32[2]` | stateCode | slot 8; decoded by `001EE7C0` |
| `108`<sub>h</sub> | `i32` | viewX | slot 9 |
| `10C`<sub>h</sub> | `i32` | viewY | slot 9 |
| `110`<sub>h</sub> | `i32` | viewW | slot 9; the target width on the offscreen path |
| `114`<sub>h</sub> | `i32` | viewH | slot 9 |
| `118`<sub>h</sub> | `u32` | viewFlag | slot 9 |
| `11C`<sub>h</sub> | `f32[16]` | matrix | slot 3; identity when built |

`Shadow` adds the line origin at `+160`<sub>h</sub>/`+164`<sub>h</sub> (`00214B10`), `ShadowFinal` the target index at `+160`<sub>h</sub>
(`002147A0`), and `Final` a byte at `+168`<sub>h</sub> (`0021394D`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `f32` | x | clip space; (x - 2048) x 2 / 1920 (`00213D31`-`00213D61`) |
| `04`<sub>h</sub> | `f32` | y | (y - 2048) x -2 / 1080 |
| `08`<sub>h</sub> | `f32` | z |  |
| `0C`<sub>h</sub> | `f32` | w |  |
| `10`<sub>h</sub> | `f32` | r |  |
| `14`<sub>h</sub> | `f32` | g |  |
| `18`<sub>h</sub> | `f32` | b |  |
| `1C`<sub>h</sub> | `f32` | a |  |
| `20`<sub>h</sub> | `f32` | u |  |
| `24`<sub>h</sub> | `f32` | v |  |

The byte `[01F811E0]` is set from `[01E0280C]`, shipped 1 (`0022A113`-`0022A120`, `001B24B0`); with it clear the
mapping divides by 512 and 448 instead (`001B1620`, `00213D38`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | loaded | set by `001E9515` |
| `04`<sub>h</sub> | `u32` | r2 | border or shadow colour |
| `08`<sub>h</sub> | `u32` | g2 |  |
| `0C`<sub>h</sub> | `u32` | b2 |  |
| `10`<sub>h</sub> | `u32` | a2 | over 128 |
| `14`<sub>h</sub> | `u32` | r1 | glyph colour |
| `18`<sub>h</sub> | `u32` | g1 |  |
| `1C`<sub>h</sub> | `u32` | b1 |  |
| `20`<sub>h</sub> | `u32` | a1 | over 128 |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | ownerKey | `001E9E2A` |
| `04`<sub>h</sub> | `u8` | emitted | set by `001E83A3` |
| `08`<sub>h</sub> | `f32` | minX | 1920 when reset |
| `0C`<sub>h</sub> | `f32` | minY | 1080 when reset |
| `10`<sub>h</sub> | `f32` | maxX |  |
| `14`<sub>h</sub> | `f32` | maxY |  |
| `18`<sub>h</sub> | `f32` | originX |  |
| `1C`<sub>h</sub> | `f32` | originY |  |
| `20`<sub>h</sub> | `f32` | firstAlpha | `001E84F9` |
| `24`<sub>h</sub> | `f32` | latestAlpha | `001E8523` |
| `28`<sub>h</sub> | `u8` | offscreen | set by begin `001E99AA` |
| `29`<sub>h</sub> | `u8` | firstPending cleared 001E84D0 |  |

## Modding notes

- A text palette entry's second colour is the border colour.
- The border's look is the `FontBorder` shader's parameters, not the glyph draw; its width is the font display's
  border setting (`001B5210`).
- Text using more than ten fonts in one line loses the glyphs of the extra fonts.
- Setting `[01E02818]` to 0 switches menu text to the pre-drawn shadow atlas path.

## Related

- [Fonts](fonts.md) - glyph records, kerning and advances.
- [Text codes](text-codes.md) - the codes that set colour, size and layout.
- [Menus](menus.md) - the screens that draw text.
