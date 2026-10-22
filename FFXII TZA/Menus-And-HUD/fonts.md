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

Each font also has an atlas `<name>.dds.phyre` and a shadow atlas `<name>_shadow.dds.phyre` (`0x008F6748`, `0x008F81E0`).

### The font builder

`0x001B4D70` reads the header and every glyph record, builds the font (`0x001FC060`) and files each glyph by its key
(`0x001FDCC0`). A font is known by the header's id, not by its place in the list. The header's flag word (`0x001B4E19`)
then asks for two more files:

| Bit | File | Request | Reader |
|---:|---|---|---|
| `0` | `<name>.ker` | `0x001B5750` (`0x001B5040`) | `0x001B5230`, through `0x001B6080` |
| `1` | `<name>.fex` | `0x001B5480` (`0x001B5061`) | `0x001B4C00`, through `0x001B6030` |

The font object keeps its tables in maps keyed by code:

- the builder's filer `0x001FDCC0` takes each glyph record from `0x001FC580(font, key)`, which returns the record in
  the map at `+0x08`, inserting an empty one for a new key; `0x001E9860` looks glyphs up through `0x001FDEC0(font,
  key)` in the map at `+0x40`, which returns null for a missing key;
- the `.fex` reader `0x001B4C00` adds a list of n entries for a key with `0x001FDB90(font, key, n)`, which returns 0
  when the map at `+0xA8` already holds the key, and writes entry i with `0x001FDB50(font, key, i, v)`;
- `0x001B4D70` stores the atlas and shadow names at `+0x100` and `+0xE0` with `0x001FE020` and `0x001FE080`, which
  free the string they are given, and tests `0x001FDF80(font)`, whether `+0x60` equals `+0x18`.

The font manager is the `0x378`-byte object `[0x01F81200]`, built by `0x001B5F10` with the text renderer `[0x01F811F8]`
(`0x2380` bytes, `0x001E71B0`); its constructor `0x001B3940` sets up a name vector, three maps keyed by font id
(`+0x28`, `+0x60`, `+0x98`), two pools (`0x001B36D0`, `0x001B3540`) and 16 slots from `+0x278`.

- `0x001B58E0(manager, id)`, from `0x001B4D70`, requests the font's atlas through the asynchronous loader
  (`0x001A1220`, `0x001A0A90`, `0x001A0BB0`; the path from `0x001FDF10`) with the completion `0x001B6230`, and, unless
  `0x001E9A20([0x01F811F8])` answers non-zero, its shadow atlas (`0x001FDE60`) with `0x001B6110`, each request filed
  in its map by the font id.
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
font's map at `+0xB0` and returns 0 when the key has none (`0x001E9DD0`). `0x001E9860` then reads glyph
`list[index]` instead of `index`; an index past the list's end gives glyph 0.

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
