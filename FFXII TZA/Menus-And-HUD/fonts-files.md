---
title: "Font files: every shipped font data file with its size, its form, its place in the font list and its .dat header"
kind: "reference"
category: "Menus and HUD"
addresses: "0x001B44A0, 0x001B4930, 0x001B4D70, 0x001B4E19, 0x001B5230, 0x001B4C00, 0x001B58E0, 0x001B6230, 0x001EA3C0, 0x001E8070, 0x001E9D20, 0x001E8580"
---

## What it lists

`fonts-files.tsv` holds one line for each data file in the five font folders `ch`, `cn`, `jp`, `kr` and `us` of
`GameData/D3D11/ArtData/font/`: 5 `fontlist.ah`, 63 `.dat`, 34 `.ker` and 14 `.fex`, 116 files. For a `.dat` the
line also carries the file's header. [Fonts](fonts.md) gives the formats and how `0x001B44A0` picks a folder and loads
its list. The 62 `<name>.dds.phyre` atlases and the two `.fgen.phyre` bitmap fonts are in
[`fonts-files-atlases.tsv`](fonts-files-atlases.tsv), one line each with the texture's size and pixel format
(The atlas files, below).

Three tables hold the rest of the data: the glyph records in [Font glyphs](fonts-glyphs.md), the pairs in
[Font kerning pairs](fonts-kerning.md) and the lists in [Font expansion lists](fonts-expansion-lists.md).

### What each file holds

Every byte of the 116 files is in the four tables, and each file is exactly these parts:

| File | Made of |
|---|---|
| `fontlist.ah` | the names of the folder's `.dat` lines that have a `list_position`, in that order, each followed by CR LF |
| `.dat` | this line's header fields, then the file's lines of `fonts-glyphs.tsv` in `record` order |
| `.ker` | the file's lines of `fonts-kerning.tsv` in `pair` order |
| `.fex` | the file's lines of `fonts-expansion-lists.tsv`, as lists or as triples by `form` |

### The two header sizes

62 `.dat` files have the `0x28`-byte header that the builder `0x001B4D70` reads. The 63rd, `us/fontex_expand.dat`,
which no list names, stops after `flags`: its header is `0x20` bytes, with no `metricA` or `metricB`, and its 810
records start at `+0x20` (`form` `header 0x20`). Its first record's key and UTF-8 bytes sit where the other files
have `metricA` and `metricB`. Its `scale` is 2.4; every other `.dat` has 1.

The game never loads `us/fontex_expand.dat`: a `.dat` name
comes only from the folder's `fontlist.ah` (`0x001B4930`, `0x001B5610`), and `us/fontlist.ah` does not name it. The
builder always reads a `0x28`-byte header and steps past it (`0x001B4E2F`), so loaded, this file's records would be
read 8 bytes late.

### Requested files

A `.dat` is requested when its folder's `fontlist.ah` names it (`0x001B4930`). The builder loads the `.dat` header's
`flags` (`0x001B4E19`) and requests the `.ker` when bit `0x1` is set (`0x001B5024`, request `0x001B5750`, reader `0x001B5230`)
and the `.fex` when bit `0x2` is set (`0x001B5045`, request `0x001B5480`, reader `0x001B4C00`). Those two requests are the
only code in the game that names a `.ker` or a `.fex`. That gives 62 of the 63 `.dat`, 25 of the 34 `.ker` and
12 of the 14 `.fex` files. The ones never requested are:

- `us/fontex_expand.dat`, with its `.fex`;
- `us/fontex_subtitle.fex`: its `.dat` has flags `0x1`;
- `font00.ker` in `ch`, `cn`, `jp` and `us`, and `font_iwa_g12.ker` in `jp` and `us`: those `.dat` files have flags
  `0x0`;
- `fontex_expand.ker` in `ch`, `cn` and `kr`: those `.dat` files have flags `0x2`.

`kr/font00.dat` has flags `0x1`, so `kr/font00.ker` is requested.

### The atlas files

Every `.dat` a list names has its atlas, `<name>.dds.phyre` in the same folder, and every atlas belongs to one:
62 atlases for the 62 listed `.dat` files. `us/fontex_expand.dat`, which no list names, has none. After filing the
glyphs, the font builder requests the atlas for every font it builds, with no test on the flag word
(`0x001B501F`, `0x001B58E0`); the completion `0x001B6230` hands the texture to the font.

Each atlas is a Phyre cluster (`PHYR`, platform `DX11`) holding one `PTexture2D` named
`ArtData/font/<folder>/<name>.dds`. The two words before the class name are the width and height, which equal the
`.dat` header's `atlasW` and `atlasH` in all 62. The pixel data, the last `u32 +0x50` bytes, is width x height x 1
for the 45 `A8` atlases and x 4 for the 17 `ARGB8` ones, in all 62; the header before it is 2,524 to 2,535 bytes.

44 different glyph images fill the 62 atlases. `font_bookman` has the same pixels in all five folders,
`font_square` in all but `cn`, and `font_venus` in all but `us`; the `font_stf_*` atlases are the same in `jp` and
`us`, and `font_stf_a` with `font_stf_b`, `font_stf_bs` with `font_stf_cs`, share one image. The
`same_pixels_as` column names the copies.

### The two bitmap fonts

`tuffysdf.fgen.phyre` and `tuffy.fgen.phyre`, 269,961 bytes each, sit at the top of the font folder. Each is a
Phyre cluster holding a `PBitmapFont` of the 95 characters `0x20` to `0x7E` over a 512 x 512 `L8` texture:

| File | Asset name | `m_isSDF` | `m_fontSize` | `m_lineSpacing` | `m_baselineOffset` |
|---|---|---:|---:|---:|---:|
| `tuffysdf.fgen.phyre` | `Samples/tuffySDF.fgen#BitmapFont` | 1 | 86 | 168.375 | 83.75 |
| `tuffy.fgen.phyre` | `ArtData/font/tuffy.fgen#BitmapFont` | 0 | 88 | 172 | 86 |

`tuffysdf.fgen.phyre` is the debug-information overlay's font: the path `0x009019C8`, through the pointer at
`0x01DFDE08`, is loaded by `0x001EA3C0` for each of the 32 text lines the `MultipleDebugDisplay` constructor
`0x001C1D40` builds at start-up ([Phyre bitmap-font text](../PhyreEngine/phyre-bitmap-font-text.md)).
No string in the executable and no other shipped file names `tuffy.fgen.phyre`, so the game never
loads it.

### Changing an atlas

- An atlas must stay a Phyre cluster holding a `PTexture2D` asset. The completion `0x001B6230` takes the first
  instance of that class from the loaded cluster (`0x001B62A5`-`0x001B62F4`) and hands the font nothing when the cluster
  or the instance is missing (`0x001B629F`, `0x001B62C0`, `0x001B62F4`).
- Glyph records place each glyph in the atlas in pixels, `atlasX` to `atlasX + cellW` and `atlasY` to
  `atlasY + cellH` from the top (`0x002AA5C7`-`0x002AA647`), so a redrawn atlas keeps every glyph at its record's
  rectangle; every shipped atlas has the `.dat` header's `atlasW` x `atlasH`.
- The texture coordinates are fractions of the `.dat` header's `atlasW` and `atlasH` (font `+0x24`, `+0x28`), not of
  the texture's own size: the emitter `0x001E8070` computes u = x / `atlasW` and v = (`atlasH` - y) / `atlasH` for each
  corner (`0x001E8150`-`0x001E81DD`, through `0x00225690` and `0x0079E3C0`). No other code reads the two fields (census in
  the Project notes).
- An atlas may therefore change size in two ways. Scaled by the same factor in width and height with the `.dat`
  unchanged, every coordinate stays the same fraction and samples the same glyph. Any other size, or glyphs moved
  in the image, needs the header's `atlasW` and `atlasH` and every glyph record's rectangle changed to match.
- A missing atlas, or a cluster without a `PTexture2D`, leaves the font's atlas at the constructor's 0 (`0x001FC08D`;
  the completion skips the store at `0x001B629F`, `0x001B62C0`, `0x001B62F4`, `0x001B6310`). The font still lays out and
  measures its text from the `.dat`, but none of its glyphs is drawn (the next bullet): its text is invisible, and
  nothing reads through the null pointer.
- When `0x001E9D20` opens the font's batch it copies the atlas into the batch's `+0x08` (`0x001E9E90`-`0x001E9E99`). All
  four batch loops of the flush `0x001E8580` skip a batch whose `+0x08` is 0 (`0x001E86F2`, `0x001E8900`, `0x001E8FB0`,
  `0x001E9190`), and the shared draw body tests each layer's texture again (`0x002142D3`).
- A font id that the font list does not hold draws nothing either: the lookup `0x001B51C0` returns 0, `0x001E9D20` clears
  the current font (`0x001E9DC4`, `0x001E9ED4`), and the emitter adds no vertex while it is 0 (`0x001E80C9`). An id outside
  1 to 31 is cleared the same way (`0x001E9DD9`-`0x001E9DE3`), because each group has 32 batches indexed by font id.
- A new font in a list needs both `<name>.dat` and `<name>.dds.phyre`: the builder requests the atlas for every
  font it builds (`0x001B501F`).

## Columns

| Column | Meaning |
|---|---|
| `folder` | the font folder: `ch`, `cn`, `jp`, `kr` or `us` |
| `file` | the file name |
| `bytes` | the file's size |
| `form` | `names` for `fontlist.ah`; `header 0x28` or `header 0x20` for a `.dat`; `pairs` for a `.ker`; `lists` (`{key, count, value[count]}` chunks) or `triples` (`{key, index, value}`) for a `.fex` |
| `list_position` | for a `.dat`, the 0-based place of its name in the folder's `fontlist.ah`; empty when the list does not name it |
| `requested` | 1 when the game requests the file (above), 0 otherwise |
| `fontId` to `metricB` | the `.dat` header fields, named as on [Fonts](fonts.md): `fontId`, `glyphCount`, `atlasW`, `atlasH`, `cellW`, `cellH`, `scale` (the shortest decimal that gives the same `f32`), `flags` (hex), `metricA`, `metricB`; empty for other files, and `metricA` and `metricB` empty for a `header 0x20` file |

### fonts-files-atlases.tsv

| Column | Meaning |
|---|---|
| `folder` | the font folder; empty for the two `.fgen.phyre` files at the folder's top level |
| `file` | the file name |
| `bytes` | the file's size |
| `kind` | `atlas` for a `<name>.dds.phyre`, `bitmap font` for a `.fgen.phyre` |
| `asset` | the asset name the cluster gives its texture or font |
| `class` | `PTexture2D` for an atlas, `PBitmapFont` for a bitmap font |
| `format` | the texture's pixel format: `A8`, `ARGB8` or `L8` |
| `width`, `height` | the texture's size in pixels |
| `bytes_per_pixel` | 1 for `A8` and `L8`, 4 for `ARGB8` |
| `pixel_bytes` | the cluster word `+0x50`: the size of the pixel data, which ends the file |
| `header_bytes` | the bytes before the pixel data |
| `pixel_bytes_match` | 1 when `pixel_bytes` is width x height x `bytes_per_pixel` |
| `same_pixels_as` | the other files with byte-identical pixel data |
| `fontId`, `list_position` | for an atlas, from its `.dat` line in `fonts-files.tsv` |
| `dat_size_match` | 1 when `width` and `height` equal the `.dat` header's `atlasW` and `atlasH` |
| `isSDF`, `fontSize`, `lineSpacing`, `baselineOffset`, `characters` | for a bitmap font, the `PBitmapFont` members and its character count |
| `loader` | the function that requests the file |
| `used` | `used`, or `unused` with the reason |

## Related

- [Fonts](fonts.md) - the formats, the loaders and how text reaches a glyph.
- [Font glyphs](fonts-glyphs.md) - every glyph record of every `.dat`.
- [Font kerning pairs](fonts-kerning.md) - every pair of every `.ker`.
- [Font expansion lists](fonts-expansion-lists.md) - every list of every `.fex`.
- [Phyre bitmap-font text](../PhyreEngine/phyre-bitmap-font-text.md) - the overlay that draws with
  `tuffysdf.fgen.phyre`.
