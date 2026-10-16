---
title: "Fonts: the font files a language uses, their kerning pairs and expansion lists, and how digits and glyphs are laid out"
kind: "format"
category: "Menus and HUD"
summary: "The PC font files: how a language picks its font list, the font data header and 0x24-byte glyph records with the flag word that asks for kerning and expansion files, the kerning pair and expansion list layouts and their loaders, how a kerning pair is looked up between two glyphs, how a glyph's advance is computed, why every digit of a number takes the width of a zero, and how a text code becomes a glyph index."
addresses: "001B44A0, 001B4D70, 001B5230, 001FDC10, 001FDDD0, 001B4C00, 002AC2F0, 002AE610"
---

## What the player sees

- Menu and dialogue text is drawn in proportional fonts, with tighter spacing for pairs such as "T." and "F,".
- Numbers such as HP, gil and counts line up in columns, because every digit takes the same width.
- The Japanese, Korean and Chinese versions carry extra fonts for subtitles, guides, tutorials, quests and monster
  names.

## Where it comes from

### The font list

`001B44A0` picks the language's list and folder from the language id `[01E02814]` (`00229E40`):

| Language id | Folder |
|---|---|
| 1-6 | `us` (`008F8620`) |
| 7 | `kr` (`008F8728`) |
| 8 | `ch` (`008F8678`) |
| 11 | `cn` (`008F86D0`) |
| any other | `jp` (`008F8188`) |

The folder is `GameData/D3D11/ArtData/font/<folder>/`, and the list is its `fontlist.ah`. The load runs in this order:

1. `001B53F0` requests the list, and its completion reaches `001B5140`.
2. `001B4930` reads one name at a time with `"%s"`, skipping line ends, and makes each into a path.
3. `001B5610` requests `<name>.dat` for each name, and its completion `001B5FE0` reaches the font builder `001B4D70`.

Each font also has an atlas `<name>.dds.phyre` and a shadow atlas `<name>_shadow.dds.phyre` (`008F6748`, `008F81E0`).

### The font builder

`001B4D70` reads the header and every glyph record, builds the font (`001FC060`) and files each glyph by its key
(`001FDCC0`). A font is known by the header's id, not by its place in the list. The header's flag word (`001B4E19`)
then asks for two more files:

| Bit | File | Request | Reader |
|---:|---|---|---|
| 0 | `<name>.ker` | `001B5750` (`001B5040`) | `001B5230`, through `001B6080` |
| 1 | `<name>.fex` | `001B5480` (`001B5061`) | `001B4C00`, through `001B6030` |

## Layouts

`FontDatHeader` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | fontId | the font's id (lookup `001B4E33`, insert `0020B5F0`) |
| `04` | `u32` | glyphCount | number of glyph records |
| `08` | `u32` | atlasW | atlas width; copied to font record +`0x24` |
| `0C` | `u32` | atlasH | copied to font record +`0x28` |
| `10` | `u32` | cellW | equal to every glyph record's cellW |
| `14` | `u32` | cellH | equal to every glyph record's cellH |
| `18` | `f32` | scale | divides advances and kerning (`001E9C01`) |
| `1C` | `u32` | flags | bit 0 asks for .ker, bit 1 for .fex |
| `20` | `u32` | metricA | copied to font record +`0x1C` |
| `24` | `u32` | metricB | copied to font record +`0x20` |

`FontGlyphRecord` (`0x24` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | key | the glyph's key: a glyph index in font00, fontguide, fontquest, fonttutorial and us fontex_subtitle, a Unicode code point in the others |
| `04` | `u32` | utf8 | the glyph's UTF-8 bytes, packed from the low byte |
| `08` | `u32` | atlasX | left edge in the atlas (`002AA5C7`) |
| `0C` | `u32` | atlasY | top edge in the atlas (`002AA5E0`) |
| `10` | `u32` | cellW | width in the atlas |
| `14` | `u32` | cellH | height in the atlas |
| `18` | `u32` | advance2 | equal to advance in every record of the 62 listed files |
| `1C` | `u32` | advance | the pen advance (`002AC4EC`) |
| `20` | `i32` | kernCp | the glyph's code point for kerning, or -1 for none (`002AC527`) |

The atlas fills row by row: `jp/font00` records 0-36 sit on row 0 and record 37 starts the next row at y 55.

`KerPair` (`0xC` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | left | code point of the first glyph of the pair |
| `04` | `i32` | right | code point of the second glyph |
| `08` | `i32` | adjust | pen adjustment in font pixels; negative tightens |

A `.ker` is these records to the end of the file. Pairs such as `('T', '.', -3)` and `('F', ',', -1)` show the first
field is the left glyph; no file except `us/fontex_subtitle` has the reverse of such a pair.

`FexChunk` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | key | the hash of a resource path |
| `04` | `i32` | count | number of u32 values that follow |

A `.fex` is chunks of `{key, count, value[count]}` to the end of the file. The values are glyph keys in first-use order.

### Kerning between two glyphs

`001FDC10` files a pair as `kern[right][left] = adjust` in the font's map at `+0x70` (`001FDC15`, `001FDC45`). While
drawing, `002AC2F0` looks a pair up for every glyph that has a kerning code point and follows another glyph
(`002AC518`-`002AC52F`):

1. `001E9780` passes the previous glyph's code point (`001E9797`) and the current one to `001FDDD0`.
2. `001FDDD0` looks up `kern[current][previous]` (`001FDDE6`, `001FDE24`) and returns the adjustment, or 0.
3. `0017F8E0` returns `ceil(adjust / scale)` (`001E9C17`, `0017F908`).
4. The draw loop `002A9F00` adds it to the pen before the glyph (`002AA0D2`-`002AA0E8`).

So the authored pairs apply as authored. The current glyph then becomes the previous one (`0017FAE0`, `002AC546`).

### Expansion lists

An expansion list remaps glyph indices for one piece of text. The key of each list is `00674A00` of a three-part path,
`event\<folder>\<name>` or `plan_map\<folder>\<name>` (`001B6350`): a hash starting at `0x1505` that multiplies by 33
and adds each character, with bit 31 cleared (`00674A03`-`00674A23`). When text is drawn, `001E9D20` binds the
running font and the list for the text's key to the text context (`001E9DB9`-`001E9DD5`). `001E9860` then reads glyph
`list[index]` instead of `index`; an index past the list's end gives glyph 0.

### Glyph advances

For each glyph `002AC2F0` computes the advance:

1. `ceil(advance / scale)` from the glyph record (`0017F9C0`, `001E9BD0`), or the raw advance when the byte `01F811E0`
   is set. A glyph with no record uses bits 32-36 of the font sheet's glyph entry (`002AC4F6`-`002AC504`).
2. Plus the letter spacing `state + 0x4C` (`002AC507`).
3. Plus 1.5, or 0.5 when `00254A10` returns 0, for glyphs marked by bit 31 of the sheet entry while the float
   `state + 0x40` is non-zero (`002AC4B8`-`002AC4DF`).

The advance and kerning are then scaled by the text size `state + 0x34` and the x scale `state + 0x38`
(`002AC54B`-`002AC5A6`). The `0F 4` code overrides the advance of the next glyph only ([Text codes](text-codes.md)).

### Why digits line up

`002AE610`, which draws numbers, measures the glyph for `0` once before its loop (`002AE7B7`-`002AE7EA`). Each
character of the number is drawn at a copy of the pen, and the pen then moves by that one width (`002AEA4C`-`002AEA59`),
whatever the digit. The shipped fonts agree: every `font00` gives the ten digits one advance, 23 in `us`, 24 in `jp`,
`ch` and `cn`, and 26 in `kr`.

`003EFD00` writes the digits, padded on the left with `0` or a space (`003EFD59`-`003EFD82`). It writes no minus sign:
a negative value gives only the padding (`003EFD20`).

### Character mapping

`002AC2F0` turns a text code into a glyph index:

- A byte `0x20` or above is index `byte - 0x20` (`002AC37C`).
- A lead byte `0x10`-`0x1F` and the next byte are index `table[lead & 0xF] + second - 0x20` (`002AC38D`-`002AC3BC`).
  The table is `00916570`, or `009165B0` for language ids 7, 8 and 11 (`002AB7D0`).

Numbers reach the font through the font sheet's two character maps (`002AE77C`, `002AE861`): the first maps `0`-`9`
to the `font00` digits and the second to the full-width digits.

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

1. Every check message goes to `0016D6A0`, which returns at once, so a bad file stops nothing and logs nothing.
2. The `.ker` reader reads a whole record while any byte remains (`001B52C6`), so a short last record reads past the
   end.
3. The `.fex` reader refuses a key already loaded and stops there, without freeing the file (`001B4CBA`, `001B4D03`).
4. The `.fex` reader trusts each count (`001B4CA6`). Read this way, the two unrequested `us` files would take their
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
