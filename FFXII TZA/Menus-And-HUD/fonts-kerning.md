[Home](../../README.md) / [Menus and HUD](README.md) / Font kerning pairs

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Font kerning pairs: every kerning pair of every shipped font, with its two characters and its adjustment | reference | Menus and HUD | Fonts and text drawing | All 39,237 kerning pairs of the 34 shipped .ker font files in file order: each pair's left and right code point with their characters and its pen adjustment, which files the game requests, how many pairs each font carries and how the adjustments are spread. | 0x001B5230, 0x001B6080, 0x001FDC10, 0x001FDDD0, 0x002AC2F0 |

## What it lists

[`fonts-kerning.tsv`](fonts-kerning.tsv) holds one line for each 12-byte pair `{left, right, adjust}` of the 34 `.ker` files: 39,237
pairs, 26,816 of them in the 25 files the game requests. The reader `0x001B5230` (through `0x001B6080`) files each pair
with `0x001FDC10`, and while drawing `0x002AC2F0` looks one up through `0x001FDDD0` by the previous and the current glyph's
kerning code point, as [Fonts](fonts.md) describes. The lines keep each file's pair order.

[Font files](fonts-files.md) says which `.ker` files are requested and how the table rebuilds every `.ker` byte
for byte. A pair applies only between glyphs whose `kernCp` is its code point ([Font glyphs](fonts-glyphs.md)).

### Pairs per font

| Font | Pairs |
|---|---|
| `font00` | 5,034 in `jp` and `us`, 380 in `kr`, 123 in `ch` and `cn` |
| `font_iwa_g12` | 1,046 in `jp` and `us` |
| `font_square` | 51 in each of the five folders |
| `font_stf_a`, `font_stf_as`, `font_stf_b`, `font_stf_bs`, `font_stf_c`, `font_stf_cs` | 1,237 each in `jp` and `us` |
| `font_venus` | 325 in `ch`, `cn`, `jp` and `kr`, 1,111 in `us` |
| `fontex_expand` | 5 in `ch`, `cn` and `kr` |
| `fontex_subtitle` | 39 in `kr`, 8,887 in `us` |

### The adjustments

`adjust` runs from -8 to 16 font pixels. 22,878 pairs adjust by 0, 11,650 of them in requested files.

| Adjust | Pairs |
|---:|---:|
| -8 | 168 |
| -7 | 62 |
| -6 | 290 |
| -5 | 465 |
| -4 | 739 |
| -3 | 614 |
| -2 | 2,793 |
| -1 | 11,142 |
| 0 | 22,878 |
| 1 | 34 |
| 2 | 3 |
| 3 | 33 |
| 4 | 3 |
| 5 | 4 |
| 9 | 1 |
| 13 | 1 |
| 14 | 3 |
| 15 | 3 |
| 16 | 1 |

## Columns

| Column | Meaning |
|---|---|
| `folder`, `file` | the font folder and the `.ker` file |
| `pair` | the pair's 0-based place in the file |
| `left`, `right` | the code points of the first and the second glyph of the pair (`i32`, decimal) |
| `left_char`, `right_char` | the characters of those code points; empty for U+00A0 (12 cells) and U+00AD (171 cells), which are not printable characters |
| `adjust` | the pen adjustment in font pixels (`i32`); negative tightens |

## Related

- [Fonts](fonts.md) - how a pair is filed, looked up and scaled.
- [Font files](fonts-files.md) - which `.ker` files are requested, and the round trip.
- [Font glyphs](fonts-glyphs.md) - each glyph's `kernCp`.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 2 calls with 2 other topics</summary>

**Graphics** (explained on [message windows](message-windows.md))

| Function | | Functions |
|---|---|---|
| `0x002AC2F0` | is called by | `0x002AAE40` |

**Game files and data tables** (explained on [fonts](fonts.md))

| Function | | Functions |
|---|---|---|
| `0x001B5230` | is called by | `0x001B6080` |

</details>
