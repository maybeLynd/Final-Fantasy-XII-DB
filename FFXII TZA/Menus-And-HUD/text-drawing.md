---
title: "Text drawing: how a line of menu text becomes glyph quads, the drawing classes that draw them, and the border shader that outlines it"
kind: "system"
category: "Menus and HUD"
summary: "How a glyph becomes six vertices in a per-font batch, how the text flush turns the batches into drawing objects, the eight DynGeo drawing classes and their three shapes, the shared ten-layer draw body and its Final and Shadow variants, how menu text is drawn as a white mask, a border shader pass, the coloured glyphs and one composite quad, the pre-drawn shadow atlas path and the aspect row the shipped settings leave off, and where the painter's state is kept."
addresses: ["001E8070", "001E8580", "002142A0", "00213FE0", "00212E70", "00213140", "00214210", "0209D490"]
---

# Text drawing: how a line of menu text becomes glyph quads, the drawing classes that draw them, and the border shader that outlines it

## What the player sees

- Menu and dialogue text is drawn with a dark border around each letter, in the colour the text's palette entry gives.
- A line of text can fade from left to right as it appears.
- Text keeps its size and place at any window resolution, because glyph positions are mapped from a fixed
  1920 x 1080 space into clip space (`00213D31`-`00213D9A`).

## How it works

### From a glyph to a batch

1. The glyph loop `002A9F00` ([Fonts](fonts.md)) fills a 0xA0-byte draw record with the glyph's atlas box, its four
   corners, their colours and alpha, and a palette index, and calls `0017F7C0` (`002AA678`).
2. `0017F7C0` hands it to the emitter `001E8070([01F811F8], record)` (`0017F838`).
3. The emitter picks palette entry `index mod 28` (`001E94E0`), or the default entry at `+0x1358` for a negative index,
   and writes six 0x3C-byte vertices, corners 0, 1, 2 and 1, 2, 3 (`001E8140`-`001E8477`).
4. Each vertex carries two colours: the glyph colour from the palette's `+0x14`-`+0x20` and the border colour from
   `+0x04`-`+0x10`, both scaled by the corner colour (`001E81FC`-`001E834D`).
5. The vertices go into the open batch of the current font (`001E8361`-`001E838C`). `001E9D20` picks that batch from
   the font id, one batch per font in each of two groups of 32 (`001E9E26`-`001E9E46`). The line's box and origin are
   widened to cover the glyph.

The palette entries are named `fontclut_%d` (`001E9533`).

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

1. Byte `+0x2378` of the font display chooses between the Special classes and `DynGeoFontTextInstance`. It is
   `[01E02818] > 0` (`001E9F30`, `0029CE4A`-`0029CE55`); the shipped value is 1, and the image holds no direct,
   image-base-relative or pointer writer of that cell.
2. The record's offscreen byte `+0x28` chooses between the offscreen path and `Final`. Every text painter call passes 1
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
| 1 | the draw entry `00213FE0`: viewport, blend and state codes, identity matrix, then its own slot 10 (`00214191`) |
| 3 | sets the 4 x 4 matrix (`00214710`) |
| 4 | sets layer `i`'s texture (`00213B30`) |
| 5 | sizes layer `i`'s vertex array (`00213F90`) |
| 6 | appends a vertex to layer `i` (`00213D10`; `Final` `00213B40` applies its matrix first) |
| 10 | draws the layers |
| 11 | renderer mode 0, 1 for `Shadow`, 2 for `Final` and `ShadowFinal` (`00214890`, `002148B0`, `00214860`) |

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

Draw types are those of `006DA5A0`: 2 a triangle list, 3 a strip, 4 a fan.

### How menu text is drawn

On the offscreen path, each line is drawn in five ordered steps (`001E8664`-`001E8F49`):

1. A render target from the size ladder is bound: the smallest of ten sizes from 50 x 60 to 1920 x 1080 that holds the
   line (`001E97B0`, table `009018F0`).
2. A `Shadow` instance draws every glyph in white (`00213E30` with flag 1, `001E87B6`), a mask of the line.
3. A `FontBorderOrderedGaussObject` filters the mask in two passes (`00212E70`, `00190260`): first across, with
   `SingleStepOffset` one texel wide, from the ladder target into its partner (`00186800`, `001867E0`), then down, one
   texel high, back again.
4. A second `Shadow` instance draws the glyphs in their own colour over it (flag 0, `001E89C6`).
5. A `FontBorderOrderedResetObject` restores the screen target (`00213040`), and a `ShadowFinal` instance draws the
   target onto the screen as one quad (`00214930`), with the line's first alpha on its left corners and its latest
   alpha on its right ones (`00214A67`-`00214AA8`).

The border shader's parameters are `ColorBuffer`, `SingleStepOffset`, `FontBorderSetting` and `FontBorderColor`
(`001902FF`-`00190352`). The colour is the palette's border colour, and `FontBorderSetting` is the border width from
the font display, 4.0 when none is set (`0017F9A0`, `001B5210`). 64 of these objects are kept, one per border colour
and target size (`001E96A0`).

So the border is a shader pass over a white mask, and the glyphs are drawn once on top of it.

### The shadow atlas path

Each font also loads `<name>_shadow.dds.phyre` beside its atlas (`001B6212`). Only `DynGeoFontTextInstance` uses it:
its draw `00213140` draws the line twice through `002133D0`, first with the shadow atlas in the border colour, then
with the glyph atlas in the glyph colour. With the shipped `[01E02818]` of 1, the flush does not take this path.

### How a draw reaches the renderer

1. The flush submits each instance (`001FB810`), which wraps it in a `GeometryInstanceOrderedObject` (`001F48B0`,
   `001F4950`) on the ordered render list.
2. When the list runs, the wrapper's callback `001F4A10` calls the instance's slot 1 with the renderer (`001F4A35`).
3. Slot 1 sets the state and calls slot 10, which draws.

### Where the state is kept

| Object | Where | Holds |
|---|---|---|
| font display | `[01F811F8]`, 0x2380 bytes (`001B5F6D`) | the current font `+0x00`, the 64 batches `+0x30`, the matrix `+0xE30`, 28 palette entries `+0xF68`, the target ladder `+0x13C0`, the 64 border objects `+0x1500`, the reset object `+0x2300`, the two line records `+0x2320`, the path byte `+0x2378` |
| text painter | `0209D490`, 0x1108 bytes, published in `[0209CC40]` by `002B3550` | the terminator `+0x10C8`, tab stop `+0x10E0`, columns `+0x10EC`, line state `+0x10FC`, justification `+0x1104` ([Text codes](text-codes.md)) |
| text context | the interpreter's argument (`002AC5F0`) | size, spacing, colour and pager state |

## Layouts

```struct DynGeoFontTextSpecialInstance base=record size=0x160
+0x000  u32[2]   vftable        the family's table
+0x008  u32[20]  layerTexture   ten texture pointers (slot 4, read 002142D0)
+0x058  u32[20]  layerVertices  ten pointers to 0x30-byte vertices (slot 5, read 00214332)
+0x0A8  u32[10]  layerCount     vertex capacity per layer (slot 5)
+0x0D0  i32[10]  layerCursor    next vertex per layer
+0x0F8  u32[2]   blendCode      slot 7; decoded by 001EE650
+0x100  u32[2]   stateCode      slot 8; decoded by 001EE7C0
+0x108  i32      viewX          slot 9
+0x10C  i32      viewY          slot 9
+0x110  i32      viewW          slot 9; the target width on the offscreen path
+0x114  i32      viewH          slot 9
+0x118  u32      viewFlag       slot 9
+0x11C  f32[16]  matrix         slot 3; identity when built
```

`Shadow` adds the line origin at `+0x160`/`+0x164` (`00214B10`), `ShadowFinal` the target index at `+0x160`
(`002147A0`), and `Final` a byte at `+0x168` (`0021394D`).

```struct DynGeoVertex base=record size=0x30
+0x00  f32  x  clip space; (x - 2048) x 2 / 1920 (00213D31-00213D61)
+0x04  f32  y  (y - 2048) x -2 / 1080
+0x08  f32  z
+0x0C  f32  w
+0x10  f32  r
+0x14  f32  g
+0x18  f32  b
+0x1C  f32  a
+0x20  f32  u
+0x24  f32  v
```

The byte `[01F811E0]` is set from `[01E0280C]`, shipped 1 (`0022A113`-`0022A120`, `001B24B0`); with it clear the
mapping divides by 512 and 448 instead (`001B1620`, `00213D38`).

```struct FontClutEntry base=record size=0x24
+0x00  u8   loaded  set by 001E9515
+0x04  u32  r2      border or shadow colour
+0x08  u32  g2
+0x0C  u32  b2
+0x10  u32  a2      over 128
+0x14  u32  r1      glyph colour
+0x18  u32  g1
+0x1C  u32  b1
+0x20  u32  a1      over 128
```

```struct FontPaintRecord base=record size=0x2C
+0x00  u32  ownerKey     001E9E2A
+0x04  u8   emitted      set by 001E83A3
+0x08  f32  minX         1920 when reset
+0x0C  f32  minY         1080 when reset
+0x10  f32  maxX
+0x14  f32  maxY
+0x18  f32  originX
+0x1C  f32  originY
+0x20  f32  firstAlpha   001E84F9
+0x24  f32  latestAlpha  001E8523
+0x28  u8   offscreen    set by begin 001E99AA
+0x29  u8   firstPending cleared 001E84D0
```

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
