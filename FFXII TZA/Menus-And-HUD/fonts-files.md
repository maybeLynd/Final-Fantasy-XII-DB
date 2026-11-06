---
title: "Font files: every shipped font data file with its size, its form, its place in the font list and its .dat header"
kind: "reference"
category: "Menus and HUD"
addresses: "0x001B44A0, 0x001B4930, 0x001B4D70, 0x001B4E19, 0x001B5230, 0x001B4C00, 0x001B58E0, 0x001B6230, 0x001EA3C0, 0x001E8070, 0x001E9D20, 0x001E8580, 0x001FDCC0, 0x003643A0, 0x00365810, 0x003649A0, 0x002D8690, 0x0067D3B0, 0x0055BAC0, 0x0029FEB0, 0x0029FBD0, 0x0029FF60, 0x00365B30, 0x002DD5D0, 0x002D8910, 0x002B3400, 0x0039BAD0, 0x0017FBC0, 0x0017FB90, 0x0039BEC0, 0x0039C150, 0x003BC4E0, 0x0037F1F0, 0x00575710, 0x005599D0"
---

## What it lists

[`fonts-files.tsv`](fonts-files.tsv) holds one line for each data file in the five font folders `ch`, `cn`, `jp`, `kr` and `us` of
`GameData/D3D11/ArtData/font/`: 5 `fontlist.ah`, 63 `.dat`, 34 `.ker` and 14 `.fex`, 116 files. For a `.dat` the
line also carries the file's header. [Fonts](fonts.md) gives the formats and how `0x001B44A0` picks a folder and loads
its list. The 62 `<name>.dds.phyre` atlases and the two `.fgen.phyre` bitmap fonts are in
[`fonts-files-atlases.tsv`](fonts-files-atlases.tsv), one line each with the texture's size and pixel format
(The atlas files, below).

[`fonts-files-hashes.tsv`](fonts-files-hashes.tsv) gives all 180 files of the font folder, one line each, with its
size, its SHA-256 and the other files that have the same bytes: 146 different contents.
[`fonts-files-bitmap-characters.tsv`](fonts-files-bitmap-characters.tsv) gives the 95 character records of each of
the two `.fgen.phyre` bitmap fonts (The two bitmap fonts, below).

Three tables hold the rest of the data: the glyph records in [Font glyphs](fonts-glyphs.md), the pairs in
[Font kerning pairs](fonts-kerning.md) and the lists in [Font expansion lists](fonts-expansion-lists.md).

### What each file holds

Every byte of the 116 files is in the four tables, and each file is exactly these parts:

| File | Made of |
|---|---|
| `fontlist.ah` | the names of the folder's `.dat` lines that have a `list_position`, in that order, each followed by CR LF |
| `.dat` | this line's header fields, then the file's lines of [`fonts-glyphs.tsv`](fonts-glyphs.tsv) in `record` order |
| `.ker` | the file's lines of [`fonts-kerning.tsv`](fonts-kerning.tsv) in `pair` order |
| `.fex` | the file's lines of [`fonts-expansion-lists.tsv`](fonts-expansion-lists.tsv), as lists or as triples by `form` |

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
62 atlases for the 62 listed `.dat` files. `us/fontex_expand.dat`, which no list names, has no atlas. After filing the
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

### The fonts of the ExFont faces and the staff roll

Ten font ids belong to the faces whose glyph tables are in `fontpack_fs.bin`
([ExFont sheets](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md)):

- `font_venus` (11), `font_bookman` (13), `font_iwa_g12` (14) and `font_square` (15) are faces 0, 2, 3 and 4. The
  fontpack binder `0x003643A0` registers ids `0xB`, `0xD`, `0xE` and `0xF` through `0x0017FC00` as it binds those faces'
  sheets (`0x003643FF`-`0x0036449E`). It registers each id even when that face's sheet slot was already set and nothing
  is bound (`0x003643E5`).
- The six `font_stf_*` fonts (17 to 22) are the [staff roll](staff-roll.md)'s faces 6 to 11: `0x00365810` registers
  id slot + 10 for sheet slots 7 to 12 (`0x003658D1`, `0x003658D4`).

The face drawer `0x003649A0` takes each glyph's quad and advance from the font whose id is its face byte `+0x60` plus
11 (`0x00364A50`-`0x00364A58`), and the measure `0x00364530` does the same (`0x003645DD`, `0x00364696`). `0x002D8690`, one of
the drawer's four callers, uses it only for text that starts with `ex` (`0x00364980`, `0x002D8720`-`0x002D8727`); it
sets that byte to its record's byte `+0x64` less 1 when that byte is above 0, and to 0
otherwise, so a record whose byte `+0x64` is 0 draws in face 0, `font_venus` (`0x002D8729`-`0x002D874B`).

### Where faces 2, 3 and 4 are drawn

`0x002D8690`, its twin `0x002D87D0` and `0x002DD5D0` clear the record's byte `+0x64` after each draw (`0x002D8796`,
`0x002D88D6`, `0x002DD66D`); `0x002DD5D0` draws the `ex` text that `0x002D8910` and `0x002D89E0` hand it (`0x002D8994`,
`0x002D8A6E`). `0x002D8910(record, x, y, text, sheet)` first builds that context with `0x003659F0`, giving it the
record's `+0x70` and x and y (`0x002D8954`-`0x002D8982`); for any other text it builds the context with
`0x002B3400(context, text, sheet)` and draws it with `0x002DD680` (`0x002D899B`-`0x002D89B3`).

`0x002DD5D0` sets the context's face `+0x60` from `+0x64` as `0x002D8690` does (`0x002DD651`-`0x002DD665`). It also gives
the context the record's dword `+0x60` at `+0x00`, its byte `+0x5C` at `+0x61` and its byte `+0x66` at `+0x63`
(`0x00365B20`), and the colour `rgb = (byte +0x90..+0x92 x s16 +0x5A) >> 7`, `a = (byte +0x93 x s16 +0x58) >> 7` at
`+0x30`, kept at the record's `+0x94` (`0x002DD5DA`-`0x002DD64E`). It reads neither its x nor its y.

So the face is set by whoever fills `+0x64` just before the draw. The License Board and the menu layouts
set it above 1:

- `0x0055BAC0`, the [Licenses](license-board-screen.md) square drawer, sets it to 3 (`0x0055BE9D`) for a square in
  state 4 while the board is zoomed in, fills text 19257 (`menu_expansion` row 257, a one-number `ex` template)
  with the square's `lpCost` (`0x00365B30`, `0x0055BEDE`) and draws it with `0x002D8910` (`0x0055BF18`). The LP cost on a
  square is face 2, `font_bookman`, whose glyphs are the digits 0 to 9.
- The menu layouts: a type-5 item's `u16` `+0x12` ([UI typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md))
  becomes the bits under mask `0xFFC0` of its node (`0x0029FEB0`). The type-5 drawer `0x0029FBD0` (`0x0029FC01`-`0x0029FC11`) and the
  Licenses list pane `0x005599D0` (`0x00559CBA`-`0x00559CCA`) copy them into `+0x64` and draw the node's text with
  `0x002D8910` (`0x0029FDFD`, `0x00559D18`). An item with `+0x12` = n draws in face n - 1.
- `0x0029FEB0` keeps only the low ten bits of `+0x12` (`0x0029FF08`-`0x0029FF17`). With `+0x2D` bit `0x4` and a text
  wider at its scale than the node, `0x0029FBD0` overwrites those bits with the scroll offset
  (`0x0029FDB1`-`0x0029FDBF`), and its next draw copies that offset into `+0x64` (`0x0029FC01`-`0x0029FC11`).

`0x0029FF60` fills such a node's text with the `ex` formatter `0x00365B30` when the field is above 0 (`0x0029FFE5`).
Its call is `0x0029FF60(node, buffer, size, n, id, p)`. The text id is `id`, or the item's `+0x14` plus 100,000 when
`id` is 0 and `+0x14` is not -1 (`0x0029FF8F`-`0x0029FF9F`); an id from 100,000 up is read with `0x002F9920` (`0x0029FFB8`).
The field counts as above 0 when the bits under `0xFFC0` of the node's dword `+0x08`, moved to the top of the
register, make a positive number (`0x0029FFC9`-`0x0029FFD4`).

With such a field and a buffer of 32 bytes or less, `0x0029CC70` formats instead, with a 32-byte limit
(`0x0029FFF4`). A field at 0 formats with `0x002B4090` (`0x002A0004`). With no buffer the text goes to the next of the
eight rotating buffers through `0x0029CC00`, or `0x0029CB80` for a field at 0 (`0x002A000B`-`0x002A0023`). The node keeps
the text at `+0x18` and `0x0020E620(p)` at `+0x20` (`0x002A0030`-`0x002A0048`).

Over the 4,484 type-5 items of all shipped layout copies, `+0x12` is 0 in 3,182, 1 in 642, 2 in 10, 4 in 330 and
5 in 320:

| `+0x12` | Face | Font | Text | Layouts and screens |
|---:|---:|---|---|---|
| 4 | 3 | `font_iwa_g12` (14) | the headings `STATUS EFFECTS`, `EQUIPMENT`, `NAME`, `EQUIPPED/TOTAL`, `PRICE`, `QUANTITY`, `INVENTORY`, `TOTAL`, `Current` and `New` (`menu_expansion` ids 190300 to 191009) | `shop_new.mrp` records 3 and 7 to 10 (the shops), `mrppack_ys.bin` unit 7 records 2 and 3 and unit 8 records 0, 2 and 11 (the Status and Equip panes), unit 9 records 0 to 3 |
| 5 | 4 | `font_square` (15) | number templates (`menu_expansion` ids 191400 to 191417, `menu_command_template` 180014) | unit 11 records 1 to 3, 7 and 8 (Licenses list and detail panes), unit 6 records 11, 12, 14 and 15 (Quit, the member rows and the Status and Equip rows), unit 7 records 9 and 17, unit 8 records 13 and 14, unit 9 records 20 and 22, `shop_new.mrp` records 3 and 11 to 15, `party_book.mrp` records 50 and 57 (the Clan Primer back panel) |

No item carries 3: the layouts do not ask for face 2, which the License Board's drawer sets. The one item with 2,
`quest.mrp` record 7, has no string. The other callers of the drawer pass the face themselves or leave `+0x64` at 0:
the staff roll's `0x0053E0B0` sets each line's face (staff-roll faces 6 to 11), and `0x005569F0` and the 13 functions
holding the 23 calls of `0x002D8650` (among them `0x0027E530`) and the call of `0x002D8670` (`0x004046AB`) write no `+0x64`.

### Which text fonts 1, 3, 4, 5 and 6 draw

A text context keeps a font index at `+0xA6`. `0x002B3400` and `0x002B32D0` set it to the place of the context's glyph
sheet in the sheet table `0x02AEE810`, 1 to 7, or 0 when the sheet is not there (`0x0039BAD0`, `0x002B3420`-`0x002B3425`).
When the language test `0x00254A10` is false and the index is 7, both also set the context's bit `0x800` and its
sheet `+0x60` to `0x0039C4A0(1)` (`0x002B342B`-`0x002B3452`, `0x002B331F`-`0x002B3341`); `0x002B3400(context, text, sheet)`
takes the sheet from its third argument.

A two-byte code whose lead is at least `[0x01E0CDF8]` is drawn with that index; one-byte codes and lower leads with
index 0 (`0x002B0280`), and in the character mapping `0x002AC2F0` with 7 once the context's bit `0x800` is set
(`0x002AC33E`-`0x002AC34E`). `0x0017FD30` passes the index to
`0x001E9D20`, which finds the record filed under `(group << 32) | index` in the display map `+0xF38` and draws with
the font keyed by the record's `+0x04` (`0x001E9D50`-`0x001E9DB9`, `0x001B51C0`).

The record's index is a slot of the font manager. `0x0017FBC0(id)` files a font in the first empty of the 16 slots
(`0x001B6510`, `0x001B4590`) and `0x0017FB90(id, slot)` in the given one (`0x001B6470`); `0x001E7F90` files the record. A
screen's glyph sheet takes the first empty place of the sheet table from 1 (`0x0039BEC0`). `0x0017FBC0` has four
callers and `0x0017FB90` one, each with its own id:

- font00 (1): the font pack binder `0x0039C150` files it (`0x0039C27C`) in the first empty slot, slot 0 while no other
  font holds one: index 0, that of every text without a sheet of its own.
- fontex_subtitle (3): the same binder files it in slot 7 when the language test `0x00254A10` is 0, locale ids 1 to
  6 and 9 (`0x0039C290`).
- fontguide (4): `0x003BC4E0`, the map screen's map-data widget, registers the guide picture of `menumap_guide<n>.bin`
  as a sheet and then the font (`0x003BC7C3`, `0x003BC7CD`), and releases both together (`0x0039BB60`, `0x0017FA70(4)`).
- fontquest (5): `0x0037F1F0` registers `menuquest.nfs`, the quest menu's name sheet, and then the font (`0x0037F2B9`,
  `0x0037F2C3`).
- fonttutorial (6): `0x00575710` registers a Traveler's Tips text bundle's glyph sheet and then the font (`0x0057576C`,
  `0x005757E5`); only the `ch`, `cn`, `in` and `kr` tutorial bundles carry a sheet
  ([Handbook files](../Game-Files-And-Data-Tables/handbook-files.md)).

### The two bitmap fonts

`tuffysdf.fgen.phyre` and `tuffy.fgen.phyre`, 269,961 bytes each, sit at the top of the font folder. Each is a
Phyre cluster holding a `PBitmapFont` of the 95 characters `0x20` to `0x7E` over a 512 x 512 `L8` texture:

| File | Asset name | `m_isSDF` | `m_fontSize` | `m_lineSpacing` | `m_baselineOffset` |
|---|---|---:|---:|---:|---:|
| `tuffysdf.fgen.phyre` | `Samples/tuffySDF.fgen#BitmapFont` | 1 | 86 | 168.375 | 83.75 |
| `tuffy.fgen.phyre` | `ArtData/font/tuffy.fgen#BitmapFont` | 0 | 88 | 172 | 86 |

After the four members each file holds the character count, 95, seven zero bytes and the 95
`PBitmapFontCharInfo` records, from `0xD7E` to `0x1E31`: 45 bytes each with no padding, in the order the
registration `0x0067D3B0` gives the members, `m_characterCode`, `m_kernPairs`, `m_kernOffset`, `m_uv`, `m_width`,
`m_height`, `m_offset`, `m_advance` and `m_rotated`. The codes run from `0x20` to `0x7E` in order.

Every record's `m_kernPairs` is 0, so neither font kerns. `m_rotated` is set on 85 records of
`tuffysdf.fgen.phyre` and 84 of `tuffy.fgen.phyre`; the builder `0x0067B530` then swaps the glyph's texture
coordinates (`0x0067B818`), and the glyph lies in the texture `m_height` wide and `m_width` high.

`tuffysdf.fgen.phyre` is the debug-information overlay's font: the path `0x009019C8`, through the pointer at
`0x01DFDE08`, is loaded by `0x001EA3C0` for each of the 32 text lines the `MultipleDebugDisplay` constructor
`0x001C1D40` builds at start-up ([Phyre bitmap-font text](../PhyreEngine/phyre-bitmap-font-text.md)).
No string in the executable and no other shipped file names `tuffy.fgen.phyre`, so the game never
loads it.

### Changing a font file

- `fontlist.ah` holds one name per line, each line ended by CR LF or LF, with nothing else on it. `0x001B4930` reads
  a name with `"%s"` (`0x008F4438`, `0x001B49CE`) and steps past exactly the name's length and then only CR and LF
  bytes (`0x001B49E0`-`0x001B4A01`), so a blank before or after a name makes a later read start inside a name. The list
  ends at the first read that finds no name (`0x001B49D3`).
- The folder and a name are joined with `"%s%s"` (`0x008F80F0`) into a 256-byte buffer (`0x001B4A13`-`0x001B4A24`);
  every folder, such as `./GameData/D3D11/ArtData/font/jp/`, is 33 characters, which leaves 222 for the name.
- A `.dat` is the `0x28`-byte header and then `0x24`-byte glyph records to the end of the file ([Fonts](fonts.md)
  Layouts). A key must not repeat: the filer `0x001FDCC0` files a record only when the font has no record of that key
  yet, and returns 0 for a repeated key without storing it (`0x001FDCF7`-`0x001FDD09`, `0x001FDD4C`), so the first
  record of a key is the one drawn.
- A `.ker` is 12-byte pairs and a `.fex` is `{key, count, values}` chunks, each to the end of the file; a `.fex`
  key already loaded stops its reader ([Fonts](fonts.md) Loader behaviour).

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
- `0x001E9D20` opens a batch only when the batch's `+0x00` is not already the font id: it then stores the id there,
  the atlas at `+0x08`, the font's `+0x10` (`0x005C5310`) at `+0x10` and copies the batch's `+0x18` to `+0x20`
  (`0x001E9E80`-`0x001E9EB5`). A batch already holding the id is used as it stands.
- Before that it stores the font's expansion list for the record's `+0x08` at `+0x08` (`0x001FDD60`,
  `0x001E9DCA`-`0x001E9DD5`), and last it copies the record's `+0x00` and `+0x0C` to `+0x18` and `+0x1C`
  (`0x001E9EB9`-`0x001E9EC6`).
- With a font bound, both halves equal to `+0x18` and `+0x1C` (`a == [+0x18] && b == [+0x1C]`) and byte
  `+0x2379` clear, `0x001E9D20` returns at once: `[+0x00] != 0`, the two equalities for its second and third
  arguments `a` and `b`, and `[+0x2379] == 0` (`0x001E9D2A`-`0x001E9D4A`). A key the display map does not hold clears
  `+0x00`-`+0x20` like a missing font
  (`0x001E9D87`-`0x001E9DA4`, `0x001E9ED4`-`0x001E9EEA`).
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

### fonts-files-hashes.tsv

| Column | Meaning |
|---|---|
| `folder` | the font folder; empty for the two `.fgen.phyre` files at the folder's top level |
| `file` | the file name |
| `bytes` | the file's size |
| `sha256` | the SHA-256 of the file |
| `same_bytes_as` | the other files with the same bytes, as `<folder>/<file>`; empty when no other file has them |

### fonts-files-bitmap-characters.tsv

| Column | Meaning |
|---|---|
| `file` | `tuffysdf.fgen.phyre` or `tuffy.fgen.phyre` |
| `record` | the record's place in the character table, from 0 |
| `code`, `char` | `m_characterCode` and its character (`space` for `0x20`, `vertical bar` for `0x7C`) |
| `texelX`, `texelY` | `m_uv`: the glyph's left and top pixel in the 512 x 512 texture |
| `width`, `height` | `m_width` and `m_height`: the quad's size in font pixels |
| `offsetX`, `offsetY` | `m_offset` |
| `advanceX`, `advanceY` | `m_advance` |
| `rotated` | `m_rotated`: 1 when the glyph lies in the texture `height` wide and `width` high |
| `kernPairs`, `kernOffset` | `m_kernPairs` and `m_kernOffset` |
| `file_offset` | where the record starts in the file |

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
| `fontId`, `list_position` | for an atlas, from its `.dat` line in [`fonts-files.tsv`](fonts-files.tsv) |
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
