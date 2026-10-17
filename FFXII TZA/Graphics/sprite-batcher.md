---
title: "Sprite batcher: the 2D vertex batcher, its register mirror and the menu quad emitters"
kind: "system"
category: "Graphics"
addresses: "01F811E8, 001B1C00, 001B1BA0, 001ADD30, 001B06D0, 001B0A20, 001B0CE0, 001B22F0, 001B2410, 001B03D0, 001B0190, 001B0100, 001B1910, 001B1440, 001B1C10, 00181460, 002DAF30, 002DD1E0, 00248EB0, 00248E10, 002DD350, 002DD4C0, 002DD420, 0215E6D0, 002D9DB0, 002DA2D0, 002DA7C0, 002DAC70, 002DBDD0, 002DC7F0, 002DD090, 00392A10"
---

## What the player sees

Menu pictures, icons, gauges, coloured panels and the soft-edged dark windows behind menu text are flat
quads. Each is still written as a PlayStation 2 GS packet, as the original game drew it, and at the same
time as vertices in a batcher that the PC renderer draws. What appears on screen comes from the batcher.

## How it works

### The batcher object

The installer `0017D4C0` calls `001B1BA0`, which allocates 0x4300 bytes (`00210EC0`), builds them with
`001ADD30` and stores the object at `01F811E8`; `001B1C00` returns it. The object holds two texture
registries, 64 vertex batches at `+0x2328` (`0x58` bytes each, built by `001ADD30` through the vector
constructor), the current batch index `+0x3928` (-1 when empty), and from `+0x3930` a block of drawing
state that mirrors the GS registers. The UI layout values bound from `UISize.json` also live in this
object, from `+0x3B00` ([screen layouts](../Menus-And-HUD/screen-layouts.md)).

Each batch is built by `001AE010`: it clears the vector at `+0x38` and reserves 1,024 entries of
`0x30` bytes in it (`001B1A20`).

### Menu textures

There are two registries, both keyed by a name hash:

- `001B1440(batcher, name)` builds `./GameData/D3D11/ArtData/menu/<name>.dds.phyre` (`%s%s%s` with the
  strings at `008F74C0` and `008F6748`), lower-cases A to Z and hashes it with `00674A00` (start `0x1505`,
  times 33 plus each byte sign-extended (`movsx`), `& 0x7FFFFFFF`).
- `001B1C10(name)` registers a menu texture: it hashes the lower-cased path and, when the tree at `+0x28` lacks
  the hash, finds the loaded asset of that path (`0019CE20`, `0019CA80`) and stores its first
  object whose class descriptor is `PTexture2D` (`02CBB900`).
- Indexed pictures from TIM2 files are registered by name in the tree at `+0x2208`, each with a table of
  palettes ([TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md)). `001B11D0` returns a
  registered picture's texture; `001FB720(table, index, half)` finds the palette with key `half + index × 2`.

- A third tree at `+0x2278` maps names to strings. `001B1240(batcher, n)` looks up `shape<n>` and
  returns the string at the entry's `+0x40`, or null; `001814F0(n)` wraps it for `002A3600`, which
  copies the string into the buffer that `0209C518 + 0x20 × i` points to.

### Batches

A batch holds one texture, one clamp region and a vector of 0x30-byte vertices (the `DynGeoVertex` of
[text drawing](../Menus-And-HUD/text-drawing.md)). Every routine below works on the batch at the current index and
moves to the next one when its state no longer matches; an index above 63 drops the vertices.

- `001B06D0(batcher, vertex)` appends one vertex. When the current batch already has a texture, it opens the
  next batch untextured first. The vector grows by doubling (`001AED50`).
- `001B0A20(batcher, vertices, count, width, height, name, clut)` names the texture as given, or
  `%s_clut_%d` with a non-zero `clut`, and looks it up in the `+0x28` tree; an empty name uses the texture at
  `+0x100`. A name that is not registered draws nothing.

- `001B13C0(batcher, name)` is the `+0x28` lookup alone: an empty name returns `+0x100`, an
  unregistered one null. The texture objects' method `00215F80` uses it, with the name or
  `%s_clut_%d`, and keeps the result at its `+0x08`.

- `001B0CE0` does the same through the `+0x2208` registry and a palette, unless `+0x2108` and `+0x2110`
  already hold a texture and palette; a palette argument of -1 takes the default table at `+0x2238`.
- Both continue the current batch when it holds the same texture, give the texture to a batch that has a
  clamp region but no texture yet, and otherwise open the next batch and carry the clamp region over. They
  store the width and height at batch `+0x2C` and `+0x30` and append `count - 2` triangles.
- `001B22F0` sets the clamp region: the mode words `+0x10` and `+0x14` and the bounds `+0x18` to `+0x24`.
  An unset region is filled, an equal one is kept, and a different one opens the next batch.

`00181460(vertices, n)` turns a strip into a list: it appends vertices `i`, `i+1`, `i+2` for each of the
`n - 2` triangles, with no change of winding. `00181350(vertices, n)` appends `n` vertices as they are.

### The register mirror

`001B1910` resets the batches (`001B0100`), zeroes the 0x178-byte state block at `+0x3930`, and sets the
four colour words `+0x3A4C` to `+0x3A58` to `0x80`. The state setters take the GS register values the
emitters also write into their packets:

| Wrapper | Body | Stores |
|---|---|---|
| `00181800`, `00181930`, `001819A0`, `00181A10` | `001B2410` | width `+0x3930`, height `+0x3934`, texture name `+0x3938`, `+0x3AA0`, palette `+0x3A38`, and `+0x3A3C`, `+0x3A40`, `+0x3A44`, `+0x3A48` |
| `001816F0` | `001B1F80` | the colour `+0x3A4C` to `+0x3A58` |
| `00181870` | `001B2490` | `+0x3A60` from the table `008F80F8` (0, 1, 6, 2, 3, 4, 5) |
| `001816B0` | `001B22D0` | the ALPHA_1 value `+0x3A68` |
| `00181910` | `001B22E0` | the TEST_1 value `+0x3A70` |
| `00181740` | `001B1FA0` | `+0x3A8C` |
| `001817A0` | `001B1FE0` | `+0x3A94` |
| `001817D0` | `001B1FF0` | the float `+0x3AFC` |
| `00181890` | `001B22F0` | the clamp region of the current batch |
| `00181390`, `001813F0` | `001B0A20`, `001B0CE0` | a textured strip |

`001B2410` copies the name with `sprintf(+0x3938, name)`, so the name is used as a format string. Each
wrapper fetches the batcher through `001B1C00`.

### The flushes

The 2D flush `001B03D0` is run by `00181330` (25 callers) and the 3D flush `001B0190` by `00181310`
(7 callers). Both walk batches 0 to the current index and, for each, take 0x238 bytes from the command arena
`[01F7F4C0]` and build a drawing object: `DynGeoTextureInstance` (`001FB870`) for 2D,
`DynGeo3DInstance` (`001FBB40`) for 3D ([Gi render commands](gi-render-commands.md)).

1. Slot `+0x90` gets the vertex count.
2. A batch with no texture passes the state block to slot `+0x68`; a textured one calls slot `+0x48`, passes
   its palette to slot `+0x70`, and copies its width and height over `+0x3930` and `+0x3934`.
3. Slot `+0x78` gets the clamp region with the width and height, and slot `+0x88` the state block.
4. The vertices go one by one to slot `+0x80`, and a 4 × 4 matrix to slot `+0xA0`.
5. The object is filed with class key `0x20` (`001FB840`, `001FB810`); the batch is emptied.

The 2D flush also passes `+0x3AE8` to slot `+0x98`. Its matrix is the identity, except that in Super Wide
(`00182F50`) the first element is `00183280()`: the height times `001DD110()` divided by the width, which
keeps the 2D layer at 16:9 ([screen mode and aspect](screen-mode-and-aspect.md)). The 3D flush first copies
the render manager's matrix `+0x6C8` into `+0x3AA8` and rewrites its depth terms from `+0x750` and
`+0x754` (`001B2000`, `00678B50`). Both end with `001B0100`, which restores each batch's defaults and sets
the index to -1.

### Sprite mode and the GS packets

The menu draw `002450B0` (and `00245110`) brackets the widget tree with `002DD4C0` and `002DD420`. The first
closes the current GS command buffer and flips it twice: once directly (`003A1DB0`, `002DD52F`) and once
inside `002B4710` (`002DD534`), which also sets the text painter's byte `+0x1103`. Then it sets
`0215E6D0` to 1.

The second, `002DD420`, also closes the current buffer with the packet word `0x11000000` and flips it
once (`003A1DB0`, `002DD476`), then clears both: the painter byte through `002B4700` (`002DD47B`) and
`0215E6D0` (`002DD485`). `002DD4B0` returns `0215E6D0`, and the emitters that test it
draw nothing outside the bracket. `002DD4A0` clears it alone.

The menu frames reach it through `002529F0`: `GiBeginScene(1)` (`001FBD80`), `002450B0` on `[0208EA48]`,
then `00252500` and `GiEndScene` (`001FBE50`). `00252500` writes one plain packet: TEST_1 `0x2001`, RGBAQ
0, PRIM 6 and two XYZ2 corners covering the screen, a sprite whose pixels all fail the alpha test and
update depth only.

A packet writer is three pointers on the caller's stack: the GS command buffer record, the packet header and
the write cursor ([render command list](render-command-list.md)). The 16-byte records are
`{value, register}`:

- `00248EB0` opens a plain packet with a 0x10-byte header. `00248E10(writer, tag)` closes it, optionally
  with an A+D record `{0x8000, 0xE}`, writing VIF FLUSH and DIRECT with the record count into the header,
  then flips the buffer (`003A1DB0`).
- `002DAF30(writer, widget, gouraud)` opens a sprite packet: it copies the widget's first 0x40 bytes (its
  matrix) to `022D8F30` and into the packet, writes TEX1_1 (`0x14`) from widget `+0x88`, a record of the
  brightness `s16 +0x5A` three times and the alpha `s16 +0x58`, and a GIF tag.
- That tag's register list is A+D then four times RGBAQ, UV, XYZF2, with PRIM `0x15C` (Gouraud) or `0x154`,
  a textured, blended triangle strip with UV coordinates. `002DD1E0` writes the untextured variant: PRIM
  `0x4C`, four times RGBAQ, XYZF2.
- Both openers also reset the register mirror (`00181560`), set its colour to brightness, brightness,
  brightness, alpha (`001816F0`) and select entry 3 (`00181870`).
- `002DD350(writer, code)` closes a sprite packet with `code | 0x14000000` in the header's last dword and
  flips the buffer; `002DD3C0` closes it with zeroed header words.

### The quad emitters

The emitters take the widget as their context: its matrix at `+0x00` (applied by `00202B70`, then divided
by w), depth `+0x70`, ALPHA_1 `+0x78`, TEST_1 `+0x80`, colour bytes `+0x90`. Each writes one packet loop
and the same quad to the batcher as a four-vertex strip (`00181460`).

| Emitter | Draws | Colour | Clamp |
|---|---|---|---|
| `002D9DB0(writer, widget, src, x, y, w, h, flags)` | a textured quad | widget `+0x90` | region from `src` |
| `002DA2D0(writer, widget, colours, src, x, y, w, h, flags)` | a textured quad | four corners | region from `src` |
| `002DA7C0(writer, widget, colours, clamp, src, x, y, w, h, flags)` | a textured quad | four corners | the caller's CLAMP_1 value, decoded into the mirror |
| `002DC7F0(writer, widget, colours, x, y, w, h, flags)` | an untextured patch | four corners | none |

- `src` is `s16` x, y, width, height in texels. When its size differs from the target's, the first three
  set flag `0x2` in each UV record; CLAMP_1 (register 8) is written as region clamp on both axes, `0xA`
  in the low bits.
- Colours are four RGBA dwords in packet order: top left, top right, bottom left, bottom right. The batcher
  strip runs top left, bottom left, top right, bottom right.
- `002DC7F0` with flag `0x8` draws two strips meeting at the patch centre, coloured with the average of the
  four corners; the vertex flags at `+0x28` carry the flags with `0x8` or `0x4` cleared.

`002DD8B0(quad, left, right, top, bottom)` writes the corner positions of a four-vertex quad as floats at
`+0x20`/`+0x24`, `+0x50`/`+0x54`, `+0x80`/`+0x84` and `+0xB0`/`+0xB4`: top left, bottom left, top right,
bottom right. The text icons (`002AEB20`), `002AFDC0` and the HUD billboards (`003F0610`) fill quads with it.

Three more emitters set state around them:

- `002DAC70(writer, widget, picture)` binds a picture. It writes A+D with TEX0_1 (`6`) from the picture's
  `+0x30` with its palette offset from widget `+0x5C` (a 4-bit picture, `+0x38` bits 8-13 = `0x14`,
  adds a TEX2_1 `0x16` record), then TEX1_1, TEST_1 and ALPHA_1, and closes with `0x5D76EC`. It then sets the mirror (`001819A0`, `00181910`, `001816B0`) and runs
  the 2D flush.
- `002DD090(writer, widget)` closes an untextured run: A+D with TEST_1 and ALPHA_1, the close code
  `0x5D76EB`, an untextured 1 × 1 state (`00181930`) and the 2D flush. Either closes an empty packet when
  no quad was added.
- `002DBDD0(widget, rect)` draws a flat colour rectangle alone. Its colour is widget `+0x90` scaled by
  brightness and alpha, kept at `+0x94`: `rgb = (byte +0x90..+0x92 x s16 +0x5A) >> 7` and
  `a = (byte +0x93 x s16 +0x58) >> 7` (`002DBEB4`-`002DBF0E`); it writes TEST_1, ALPHA_1 and RGBAQ, a flat strip of four
  XYZF2, closes with `00248E10`, and draws the same rectangle untextured through the batcher.

### Soft windows

`00392A10(widget, rect, colours)`, entered through `00392A00`, draws a rectangle whose edges fade out. `rect`
is eight `s16`: x, y, width, height, then left, right, top and bottom border sizes. It builds a 4 × 4 grid
of colours: the four given colours on the inner corners and the same colours with alpha 0 on the outer ring.
In sprite mode it opens an untextured packet (`002DD1E0`), draws each non-empty cell of the 3 × 3 grid with
`002DC7F0`, and closes with `002DD090`. Outside sprite mode it calls `00392CE0`, which draws the nine cells
through `002DC290`.

## Layouts

Batcher (`01F811E8`), `0x4300` bytes, built by `001ADD30`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0028` | `map` | menu textures | key: `001B1440` hash; value +`0x28` the texture (`001B1C10`) |
| `+0x0100` | `void*` | texture used by an empty name (001B0A20) |  |
| `+0x2108` | `void*` | override texture | `001B0CE0` |
| `+0x2110` | `void*` | override palette | `001B0CE0` |
| `+0x2140` | `vec` | 256 records of 0x40 (001ADBA0, sized by 001B1B10, trimmed by 001B0640) |  |
| `+0x2208` | `map` | indexed pictures | key: `001B1440` hash (`001B11D0`, `001B0CE0`) |
| `+0x2238` | `...` | default palette table (001B0CE0 with palette -1) |  |
| `+0x2328` | `0x58 x 64` | batches |  |
| `+0x3928` | `i32` | current batch, -1 when empty |  |
| `+0x3930` | `...` | register mirror, 0x178 bytes (001B1910) |  |
| `+0x3AA8` | `f32[16]` | 3D | matrix copied by `001B2000` |
| `+0x3AFC` | `f32` | 1.6 (001ADD30) |  |
| `+0x3B00` | `...` | UISize.json values |  |

Batch, `0x58` bytes (+`0x2328` + `0x58` * i):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | texture | 0: untextured, drawn with the register mirror |
| `+0x08` | `void*` | palette |  |
| `+0x10` | `u32` | clamp word 1 | default 1 |
| `+0x14` | `u32` | clamp mode | default 1; the emitters pass 2 (region) |
| `+0x18` | `u32` | min u | +`0x1C` min v, +`0x20` max u, +`0x24` max v |
| `+0x28` | `u32` | clamp set | `001B22F0` |
| `+0x2C` | `u32` | width | default 1 |
| `+0x30` | `u32` | height | default 1 |
| `+0x38` | `void*` | vertices begin | +`0x40` end, +`0x48` capacity, +`0x50` allocator |

Register mirror (+`0x3930`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x3930` | `u32` | width | +`0x3934` height |
| `+0x3938` | `char[256] texture name` | sprintf'd by 001B2410 |  |
| `+0x3A38` | `u32` | palette | +`0x3A3C` .. +`0x3A48` `001B2410`'s last four |
| `+0x3A4C` | `u32[4] colour` | 0x80 each after 001B1910 |  |
| `+0x3A60` | `u32` | table value | from `008F80F8` |
| `+0x3A68` | `u64` | ALPHA_1 | +`0x3A70` TEST_1 |

## State

| Address | What |
|---|---|
| `01F811E8` | the batcher |
| `0215E6D0` | sprite mode: 1 between `002DD4C0` and `002DD420` |
| `022D8F30` | the last sprite packet's widget matrix |
| `008F80F8` | the table `00181870` indexes |

## Modding notes

- Only 64 batches exist per flush. A run that changes texture or clamp region more often loses the rest of
  its quads until the next flush, with no error.
- A sprite whose texture name is not registered draws nothing; register `.dds.phyre` menu textures through
  `001B1C10` before drawing them by name.
- Texture names reach `sprintf` as the format; a name containing `%` is expanded.
- The GS packet and the batcher are written side by side. A hook that changes what appears must change the
  batcher calls; the packet values alone do not reach the screen.
- Outside the menu draw's sprite-mode bracket, `002DAF30`, `002DD1E0` and `002D0650` emit nothing.

## Related

- [Gi render commands](gi-render-commands.md): the command arena and the filing the flushes use.
- [Text drawing](../Menus-And-HUD/text-drawing.md): the DynGeo classes and the vertex layout.
- [Render command list](render-command-list.md): the GS command buffers the packets go into.
- [Graphics thread handshake](graphics-thread-handshake.md): how a flipped buffer is published.
- [Screen mode and aspect](screen-mode-and-aspect.md): the Super Wide test.
- [Widgets](../Menus-And-HUD/widgets.md): the widgets the emitters draw.
- [TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md): the indexed pictures and palettes.
- [Phyre frame](../PhyreEngine/the-frame.md): the pass that runs the menu draw.
