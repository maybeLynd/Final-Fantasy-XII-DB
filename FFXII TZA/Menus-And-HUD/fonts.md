---
title: "Fonts: the font files a language uses, their kerning pairs and expansion lists, and how digits and glyphs are laid out"
kind: "format"
category: "Menus and HUD"
addresses: "0x001B44A0, 0x001B4D70, 0x001B5230, 0x001FDC10, 0x001FDDD0, 0x001B4C00, 0x002AC2F0, 0x002AE610"
---

## What the player sees

- Menu and dialogue text is drawn in proportional fonts, with tighter spacing for pairs such as "T." and "F,".
- Numbers such as HP, gil and counts line up in columns, because every digit takes the same width.
- The Japanese, Korean and Chinese versions carry extra fonts for subtitles, guides, tutorials, quests and monster
  names.

## Where it comes from

### The font list

Before its list request `0x001B44A0` stores its third argument in the font display's path byte
`[0x01F811F8] + 0x2378` (`0x001E9F30`, `0x001B4544`), and it ends by tail-jumping to `0x001E98A0` (`0x001B4587`), which
loads every palette entry `fontclut_0` to `fontclut_27` not yet loaded through `0x001C5F20`.

`0x001B44A0` picks the language's list and folder from the language id `[0x01E02814]` (`0x00229E40`):

| Language id | Folder |
|---|---|
| 1-6 | `us` (`0x008F8620`) |
| 7 | `kr` (`0x008F8728`) |
| 8 | `ch` (`0x008F8678`) |
| 11 | `cn` (`0x008F86D0`) |
| any other | `jp` (`0x008F8188`) |

The folder is `GameData/D3D11/ArtData/font/<folder>/`, and the list is its `fontlist.ah`. The load runs in this order:

1. `0x001B53F0` requests the list, and its completion reaches `0x001B5140`.
2. `0x001B4930` reads one name at a time with `"%s"`, skipping line ends, and makes each into a path.
3. `0x001B5610` requests `<name>.dat` for each name, and its completion `0x001B5FE0` reaches the font builder `0x001B4D70`.

Each font's atlas is `<name>.dds.phyre` (`0x008F6748`). The builder also names a shadow atlas `<name>_shadow.dds.phyre`
(`0x008F81E0`), which the shipped build never requests and no font folder ships (the manager's list below).

### The font builder

`0x001B4D70` reads the header and every glyph record, builds the font (`0x001FC060`) and files each glyph by its key
(`0x001FDCC0`). A font is known by the header's id, not by its place in the list. The header's flag word (`0x001B4E19`)
then asks for two more files:

| Bit | File | Request | Reader |
|---:|---|---|---|
| `0` | `<name>.ker` | `0x001B5750` (`0x001B5040`) | `0x001B5230`, through `0x001B6080` |
| `1` | `<name>.fex` | `0x001B5480` (`0x001B5061`) | `0x001B4C00`, through `0x001B6030` |

The font object keeps three maps keyed by code: the glyphs at `+0x38`, the kerning pairs at `+0x70` and the
expansion lists at `+0xA8` of the font, each built by the constructor (`0x001FC0E4`, `0x001FC134`, `0x001FC184`). Each map
has its header node at its own `+0x08` and its root at its own `+0x18` (`0x001FC587`, `0x001FC58E`), so the glyph map's
header and root are at the font's `+0x40` and `+0x50`:

- the builder's filer `0x001FDCC0` takes each glyph record from `0x001FC580(font + 0x38, &key)` (`0x001FDCC8`,
  `0x001FDD13`), which returns the record for the key, inserting an empty one for a new key; `0x001E9860` looks glyphs
  up in the same map through `0x001FDEC0(font, key)` (root `+0x50`, header `+0x40`), which returns null for a missing
  key;
- the `.fex` reader `0x001B4C00` adds a list of n entries for a key with `0x001FDB90(font, key, n)`, which returns 0
  when the map at `+0xA8` already holds the key, and writes entry i with `0x001FDB50(font, key, i, v)`; both find
  the key's entry in that map through `0x001FC640`;
- `0x001B4D70` builds three names from the file's name with `0x001B31E0`, each from a suffix pointer:
  - `<name>.dat` at `[rbp - 0x38]` (`0x01DF6E08` to `0x008F81F4`, `0x001B4DA8`);
  - `<name>.dds.phyre` at `[rbp - 0x58]` (`0x01DF6DF8` to `0x008F6748`, `0x001B4DB9`-`0x001B4DC7`);
  - `<name>_shadow.dds.phyre` at `[rbp - 0x78]` (`0x01DF6E00` to `0x008F81E0`, `0x001B4DCD`-`0x001B4DDB`).
- `0x001B4D70` copies `[rbp - 0x58]` (begin `[rbp - 0x58]`, end `[rbp - 0x50]`, `0x001B4F9E`-`0x001B4FAB`) into the font's atlas
  name `+0xE0` with `0x001FE080` (`0x001B4FB8`), and `[rbp - 0x78]` (`0x001B4FD9`-`0x001B4FE6`) into the shadow name `+0x100`
  with `0x001FE020` (`0x001B4FF3`); each of the two frees the string it is given;
- after filing every glyph, the builder tests `0x001FDF80(font)`, whether the glyph map's count `+0x60` (its own
  `+0x28`, which the inserter `0x001FD010` raises at `0x001FD0BB` and `0x001FD14E`) equals the count `+0x18` the
  constructor was given (`0x001FC095`), and asserts on it (`0x001B4F6C`, "Font Info Buffer size Not Equal with Head
  Data!!").

The font manager is the `0x378`-byte object `[0x01F81200]`, built by `0x001B5F10` with the text renderer `[0x01F811F8]`
(`0x2380` bytes, `0x001E71B0`); its constructor `0x001B3940` sets up a name vector, three maps keyed by font id
(`+0x28`, `+0x60`, `+0x98`), two pools (`0x001B36D0`, `0x001B3540`) and 16 slots from `+0x278`.

- `0x001B58E0(manager, id)`, from `0x001B4D70`, requests the font's atlas through the asynchronous loader
  (`0x001A1220`, `0x001A0A90`, `0x001A0BB0`; the path from `0x001FDF10`) with the completion `0x001B6230`, and, unless
  `0x001E9A20([0x01F811F8])` answers non-zero (`0x001B5A3F`-`0x001B5A46`), its shadow atlas (`0x001FDE60`) with `0x001B6110`,
  each request filed in its map by the font id.
- `0x001E9A20` returns the path byte `+0x2378`. Its one writer `0x001E9F30` is called from `0x001B44A0` with the third
  argument, which `0x0017F9E0` passes on from `0x0029CE40`: `[0x01E02818] > 0` (`0x0029CE4A`-`0x0029CE55`). `0x01E02818` holds 1
  in `.data`, and its only rip-relative reference is the read `0x00229E30`, so the byte is 1 and the shadow atlas is
  not requested. None of the 62 shipped atlas files is a `_shadow` one.
- `0x001B6230(font, ...)` finds the texture of the loaded atlas (`0x0019CE20`, `0x0019CA80`, a resource of type
  `0x02CBB900` in its `+0x38` list) and hands it to the font (`0x00213560`).
- `0x001B60D0()` asks for the fonts again: `0x001B5140([0x01F81200])` requests every listed name.
- `0x001B5CC0(manager, id)`, from `0x0017FA70`, frees the slot registered under the key `[manager] x 32 + id`
  (`0x002124C0`, `0x001E9A30`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | fontId | the font's id (lookup `0x001B4E33`, insert `0x0020B5F0`) |
| `+0x04` | `u32` | glyphCount | number of glyph records |
| `+0x08` | `u32` | atlasW | atlas width; copied to font record `+0x24` |
| `+0x0C` | `u32` | atlasH | copied to font record `+0x28` |
| `+0x10` | `u32` | cellW | equal to every glyph record's cellW |
| `+0x14` | `u32` | cellH | equal to every glyph record's cellH |
| `+0x18` | `f32` | scale | divides advances and kerning (`0x001E9C01`) |
| `+0x1C` | `u32` | flags | bit 0 asks for .ker, bit 1 for .fex |
| `+0x20` | `u32` | metricA | copied to font record `+0x1C` |
| `+0x24` | `u32` | metricB | copied to font record `+0x20` |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | key | the glyph's key: a glyph index in font00, fontguide, fontquest, fonttutorial and us fontex_subtitle, a Unicode code point in the others |
| `+0x04` | `u32` | utf8 | the glyph's UTF-8 bytes, packed from the low byte |
| `+0x08` | `u32` | atlasX | left edge in the atlas (`0x002AA5C7`) |
| `+0x0C` | `u32` | atlasY | top edge in the atlas (`0x002AA5E0`) |
| `+0x10` | `u32` | cellW | width in the atlas |
| `+0x14` | `u32` | cellH | height in the atlas |
| `+0x18` | `u32` | advance2 | equal to advance in every record of the 62 listed files |
| `+0x1C` | `u32` | advance | the pen advance (`0x002AC4EC`) |
| `+0x20` | `i32` | kernCp | the glyph's code point for kerning, or -1 for none (`0x002AC527`) |

The atlas fills row by row: `jp/font00` records 0-36 sit on row 0 and record 37 starts the next row at y 55.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | left | code point of the first glyph of the pair |
| `+0x04` | `i32` | right | code point of the second glyph |
| `+0x08` | `i32` | adjust | pen adjustment in font pixels; negative tightens |

A `.ker` is these records to the end of the file. Pairs such as `('T', '.', -3)` and `('F', ',', -1)` show the first
field is the left glyph; no file except `us/fontex_subtitle` has the reverse of such a pair.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | key | the hash of a resource path |
| `+0x04` | `i32` | count | number of u32 values that follow |

A `.fex` is chunks of `{key, count, value[count]}` to the end of the file. The values are glyph keys in first-use order.

### The atlas files

Each of the 62 shipped `<name>.dds.phyre` atlases is a Phyre cluster: the u32 at `+0x00` is `0x50485952` ("PHYR"),
the one at `+0x0C` is `0x44583131` ("DX11"), and the cluster names one `PTexture2D` asset,
`ArtData/font/<folder>/<name>.dds`. The u32 at
`+0x50` is the pixel data size, and the pixels are the last that many bytes of the file, after a header of 2,524 to
2,535 bytes. Every atlas's width and height are the `.dat` header's `atlasW` and `atlasH`:

| Format (class name after `PTexture2D`) | Bytes a pixel | Atlases |
|---|---:|---|
| `A8` | 1 | 45 |
| `ARGB8` | 4 | 17: `font_bookman` in all five folders, the six `font_stf_*` in `jp` and `us` |

The rows are stored bottom row first: a glyph record's `atlasY` counts from the top, and its row *y* is stored row
`atlasH - 1 - y`. Measured over the shipped files:

- read that way, all of an atlas's ink (the A8 value, or the last byte of an ARGB8 pixel) lies inside the glyph
  rectangles in 59 of the 62 files, and 99.85 % in the two `font_stf_as` files and 99.46 % in `us/font_venus`;
- read top row first, 43 files have ink outside them;
- in `us/font00` (2,048 x 1,980), the ink of `.`, `,` and `_` has its centre at rows 38.5 to 44.6 of the 55-row cell,
  and that of `'` and `^` at rows 17.1 to 21.0.

The draw loop `0x002A9F00` passes the glyph's pixel rectangle, `atlasX` to `atlasX + cellW` and `atlasY` to
`atlasY + cellH` (`0x002AA5C7`-`0x002AA647`), to `0x0017F7C0`. The completion `0x001B6230` takes the `PTexture2D` instance
(class `0x02CBB900`) from the loaded cluster's `+0x38` list and hands the font a pointer into the cluster's instance
data for it (`0x001B62A5`-`0x001B6332`).

### The font object

`0x001B4D70` allocates `0x120` bytes (`0x001B4E73`) and builds the font with `0x001FC060` (`0x001B4EC5`), which takes the
header's values as arguments and stores each.

```struct Font base=font size=0x120
+0x00  u32       fontId            header +0x00 (0x001FC089)
+0x04  u8[4]     pad04             not written by the constructor 0x001FC060; 0x00210EC0 allocates the font (0x001B4E73)
+0x08  ptr       atlas             the atlas texture: 0 from the constructor (0x001FC08D), set by 0x00213560 from the
                                   atlas completion 0x001B6230 (0x001B6332)
+0x10  ptr       shadow            the shadow atlas texture: 0 (0x001FC091), set by 0x00213540 from 0x001B6110 (0x001B6212)
+0x18  u32       glyphCount        header +0x04 (0x001FC095); 0x001FDF80 compares it with glyphsCount
+0x1C  u32       metricA           header +0x20 (0x001FC09F); returned by 0x001FDDC0
+0x20  u32       metricB           header +0x24 (0x001FC0A9)
+0x24  u32       atlasW            header +0x08 (0x001FC0AC)
+0x28  u32       atlasH            header +0x0C (0x001FC0B0)
+0x2C  u32       cellW             header +0x10 (0x001FC0B8)
+0x30  u32       cellH             header +0x14 (0x001FC0C2)
+0x34  f32       scale             header +0x18 (0x001FC0CE); returned by 0x001FDDB0, which 0x001E9BF0 calls (0x001E9BFC)
+0x38  u8[8]     glyphsPad         map of the glyph records by key, filed by 0x001FDCC0 and looked up by 0x001FDEC0 (0x001FC0E4); not written by the constructor
+0x40  ptr       glyphsHeadA       header node, first word: 0 (0x001FC0F3), then the header itself (0x001FC111)
+0x48  ptr       glyphsHeadB       header node, second word: 0 (0x001FC0F6), then the header itself (0x001FC114)
+0x50  ptr       glyphsRoot        root node: 0 when empty (0x001FC0FA, 0x001FC118); 0x001FC580 starts here (0x001FC587)
+0x58  u8        glyphsHeadFlag    0 (0x001FC11C)
+0x59  u8[7]     glyphsPad21       zeroed by the qword store at 0x001FC0FE
+0x60  u32       glyphsCount       entries: 0 (0x001FC120); 0x001FD010 raises it (0x001FD0BB, 0x001FD14E)
+0x64  u8[4]     glyphsPad2C       not written by the constructor
+0x68  ptr       glyphsAlloc       the "EASTL map" allocator name (0x008F4120), set by 0x001EDF00 (0x001FC10C)
+0x70  u8[8]     kerningPad        map of the kerning pairs, filed by 0x001FDC10 and looked up by 0x001FDDD0 (0x001FC134); not written by the constructor
+0x78  ptr       kerningHeadA      header node, first word: 0 (0x001FC143), then the header itself (0x001FC161)
+0x80  ptr       kerningHeadB      header node, second word: 0 (0x001FC146), then the header itself (0x001FC164)
+0x88  ptr       kerningRoot       root node: 0 when empty (0x001FC14A, 0x001FC168)
+0x90  u8        kerningHeadFlag   0 (0x001FC16C)
+0x91  u8[7]     kerningPad21      zeroed by the qword store at 0x001FC14E
+0x98  u32       kerningCount      entries: 0 (0x001FC170)
+0x9C  u8[4]     kerningPad2C      not written by the constructor
+0xA0  ptr       kerningAlloc      the "EASTL map" allocator name (0x008F4120), set by 0x001EDF00 (0x001FC15C)
+0xA8  u8[8]     expansionPad      map of the expansion lists by key, filled by 0x001FDB90 and 0x001FDB50 and found by 0x001FDD60 (0x001FC184); not written by the constructor
+0xB0  ptr       expansionHeadA    header node, first word: 0 (0x001FC196), then the header itself (0x001FC1B4)
+0xB8  ptr       expansionHeadB    header node, second word: 0 (0x001FC199), then the header itself (0x001FC1B7)
+0xC0  ptr       expansionRoot     root node: 0 when empty (0x001FC19D, 0x001FC1BB)
+0xC8  u8        expansionHeadFlag 0 (0x001FC1BF)
+0xC9  u8[7]     expansionPad21    zeroed by the qword store at 0x001FC1A1
+0xD0  u32       expansionCount    entries: 0 (0x001FC1C3)
+0xD4  u8[4]     expansionPad2C    not written by the constructor
+0xD8  ptr       expansionAlloc    the "EASTL map" allocator name (0x008F4120), set by 0x001EDF00 (0x001FC1AF)
+0xE0  ptr       atlasNameBegin    atlas name <name>.dds.phyre (0x001FE080, 0x001B4FB8), first character; the empty
                                   string 0x02EBA2E0 from the constructor (0x001FC1F5); 0x001FDF10 copies the name for the request
+0xE8  ptr       atlasNameEnd      end of the characters; 0x02EBA2E0 when empty (0x001FC1FC)
+0xF0  ptr       atlasNameCap      end of the buffer; 0x02EBA2E1 when empty (0x001FC20A)
+0xF8  ptr       atlasNameAlloc    the "EASTL basic_string" allocator name (0x008F6600), set by 0x001EDF00 (0x001FC1E9)
+0x100 ptr       shadowNameBegin   shadow name <name>_shadow.dds.phyre (0x001FE020, 0x001B4FF3), first character;
                                   0x02EBA2E0 when empty (0x001FC239); 0x001FDE60 copies the name for the request
+0x108 ptr       shadowNameEnd     end of the characters; 0x02EBA2E0 when empty (0x001FC240)
+0x110 ptr       shadowNameCap     end of the buffer; 0x02EBA2E1 when empty (0x001FC247)
+0x118 ptr       shadowNameAlloc   the "EASTL basic_string" allocator name (0x008F6600), set by 0x001EDF00 (0x001FC234)
```

### Kerning between two glyphs

`0x001FDC10` files a pair as `kern[right][left] = adjust` in the font's map at `+0x70` (`0x001FDC15`, `0x001FDC45`). While
drawing, `0x002AC2F0` looks a pair up for every glyph that has a kerning code point and follows another glyph
(`0x002AC518`-`0x002AC52F`):

1. `0x001E9780` passes the previous glyph's code point (`0x001E9797`) and the current one to `0x001FDDD0`.
2. `0x001FDDD0` looks up `kern[current][previous]` (`0x001FDDE6`, `0x001FDE24`) and returns the adjustment, or 0.
3. `0x0017F8E0` returns `ceil(adjust / scale)` (`0x001E9C17`, `0x0017F908`).
4. The draw loop `0x002A9F00` adds it to the pen before the glyph (`0x002AA0D2`-`0x002AA0E8`).

So the authored pairs apply as authored. The current glyph then becomes the previous one (`0x0017FAE0`, `0x002AC546`).

### Expansion lists

An expansion list remaps glyph indices for one piece of text. The key of each list is `0x00674A00` of a three-part path,
`event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): a hash starting at `0x1505` that multiplies by 33
and adds each character, with bit 31 cleared (`0x00674A03`-`0x00674A23`).

When text is drawn, `0x001E9D20` binds the
running font and the list for the text's key to the text context (`0x001E9DB9`-`0x001E9DD5`). `0x001FDD60` finds that list in the
font's map at `+0xA8`, the one the `.fex` reader fills, and returns 0 when the key has none (`0x001E9DD0`). `0x001E9860` then reads glyph
`list[index]` instead of `index`; an index at or past the list's end gives a null glyph, as does a context
with no font (`0x001E9866`, `0x001E987E`, `0x001E9890`).

### Glyph advances

For each glyph `0x002AC2F0` computes the advance:

1. `ceil(advance / scale)` from the glyph record (`0x0017F9C0`, `0x001E9BD0`), or the raw advance when the byte `0x01F811E0`
   is set. A glyph with no record uses bits 32-36 of the font sheet's glyph entry (`0x002AC4F6`-`0x002AC504`).
2. Plus the letter spacing `state + 0x4C` (`0x002AC507`).
3. Plus 1.5, or 0.5 when `0x00254A10` returns 0, for glyphs marked by bit 31 of the sheet entry while the float
   `state + 0x40` is non-zero (`0x002AC4B8`-`0x002AC4DF`).

The advance and kerning are then scaled by the text size `state + 0x34` and the x scale `state + 0x38`
(`0x002AC54B`-`0x002AC5A6`). The `0F 4` code overrides the advance of the next glyph only ([Text codes](text-codes.md)).

### Why digits line up

`0x002AE610`, which draws numbers, measures the glyph for `0` once before its loop (`0x002AE7B7`-`0x002AE7EA`). Each
character of the number is drawn at a copy of the pen, and the pen then moves by that one width (`0x002AEA4C`-`0x002AEA59`),
whatever the digit. The shipped fonts agree: every `font00` gives the ten digits one advance, 23 in `us`, 24 in `jp`,
`ch` and `cn`, and 26 in `kr`.

`0x003EFD00` writes the digits, padded on the left with `0` or a space (`0x003EFD59`-`0x003EFD82`). It writes no minus sign:
a negative value gives only the padding (`0x003EFD20`).

### Character mapping

The text code reaches the font sheet through `0x0039C4A0(alt)`, which returns `[0x02AEE808]` when `alt` is non-zero
and that pointer is set, and `[0x02AEE800]` otherwise. `0x0039C4A0` has 24 callers; among them are the character mapping `0x002AC2F0`, the
number writer `0x002B3770`, the encoders `0x002B5AB0` and `0x002B5A20`, the text drawers `0x002AC5F0`, `0x002AE610` and
`0x002B0280`, and the font pack binder `0x0039C150`.

Two more lookups sit beside it: `0x0039C100()` returns entry `[0x02AEE894]` of the 26-entry table `0x02AEE898`, and
`0x0039C120(n)` entry n - 1 with n clamped to 1-26; the battle menu's `0x0027E530` reads both.

`0x002AC2F0` turns a text code into a glyph index:

- A byte `0x20` or above is index `byte - 0x20` (`0x002AC37C`).
- A lead byte `0x10`-`0x1F` and the next byte are index `table[lead & 0xF] + second - 0x20` (`0x002AC38D`-`0x002AC3BC`).
  The table is `0x00916570`, or `0x009165B0` for language ids 7, 8 and 11 (`0x002AB7D0`).

Numbers reach the font through the font sheet's two character maps (`0x002AE77C`, `0x002AE861`): the first maps `0`-`9`
to the `font00` digits and the second to the full-width digits.

The same maps turn plain characters into text codes. Each holds one `u16` code per character from `0x20`; a code of
`0x20`-`0xFF` is written as one byte and any other as two:

- `0x002B5AB0(out, ascii, n)` encodes up to `n` characters with the first map, writing a space as the token `0x04`
  (`0x002B5B2A`); the Brightness row and the title's text consumer use it (`0x0023B5C6`, `0x00393B5B`).
- `0x002B5A20(out, size, plus, fullwidth)` writes the code of `+` (`plus` set) or `-` from the first map, or the second
  with `fullwidth`, and its terminator.

## Shipped data

| Folder | Fonts listed |
|---|---:|
| `jp` | 17 |
| `us` | 12 |
| `ch`, `cn`, `kr` | 11 each |

| | |
|---|---|
| `.dat` files | 63; 62 named by a list (not `us/fontex_expand`) |
| flag word over the 62 | 0 in 26, 1 (kerning) in 24, 2 (expansion) in 11, 3 in 1 |
| `.ker` files | 34, 25 requested |
| `.fex` files | 14, 12 requested |
| glyph records | 22,440 in the 62 listed `.dat` files |
| kerning pairs that can apply | 12,363 of the 26,816 requested, 8,167 of them non-zero |
| font ids | font00 1, fontex_expand 2, fontex_subtitle 3, fontguide 4, fontquest 5, fonttutorial 6, fontmonster 7, font_venus 11, font_bookman 13, font_iwa_g12 14, font_square 15, font_stf 17-22 |

The `fontex_expand` lists are mostly `plan_map` keys (449 of 482 in `jp`) and the `fontex_subtitle` lists mostly
`event` keys (164 in `jp`); the `fontmonster` keys match no path of either family among 1,884,534 candidate strings.

No `us` font asks for a `.fex`, so `us` text always draws glyphs by their own index. The two `us` files that are not
requested, `fontex_expand.fex` and `fontex_subtitle.fex`, are 12-byte `{key, index, value}` triples, 9,032 and 11,481 of
them.

## Loader behaviour

1. Every check message goes to `0x0016D6A0`, which returns at once, so a bad file stops nothing and logs nothing.
2. The `.ker` reader reads a whole record while any byte remains (`0x001B52C6`), so a short last record reads past the
   end.
3. The `.fex` reader refuses a key already loaded and stops there, without freeing the file (`0x001B4CBA`, `0x001B4D03`).
4. The `.fex` reader trusts each count (`0x001B4CA6`). Read this way, the two unrequested `us` files would take their
   first key as a count and run about 2.3 GB past the end.
5. A `.dat` flag bit asks for its file without checking that it exists; no shipped flag asks for a missing file.

## Modding notes

- To kern a new pair, add `{left, right, adjust}` to the font's `.ker` and set bit 0 of the `.dat` flag word.
- A glyph needs a `kernCp` other than -1 to take part in kerning.
- A replacement digit glyph should keep the width of `0`, because every digit is spaced by it.
- The `scale` float divides every advance and kerning value of the font.

## Related

- [Text codes](text-codes.md) - the codes that set size, spacing and the next glyph's advance.
- [Menus](menus.md) - the screens that draw this text.
