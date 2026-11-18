[Home](../../README.md) / [Menus and HUD](README.md) / Font glyphs

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Font glyphs: every glyph record of every shipped font, with its character, atlas rectangle, advance and kerning code point | reference | Menus and HUD | Fonts and text drawing | All 23,250 glyph records of the 63 shipped .dat font files in file order: each record's key, its character, its UTF-8 word, its rectangle in the atlas, its two advance words and its kerning code point, with the fields named as on the Fonts page; which fonts key their glyphs by index and which by code point. | 0x001B4D70, 0x001FDCC0, 0x001E9860, 0x002AA5C7, 0x002AC4EC, 0x002AC527 |

## What it lists

[`fonts-glyphs.tsv`](fonts-glyphs.tsv) holds one line for each `0x24`-byte glyph record of the 63 `.dat` files: 23,250 records, the
22,440 of the 62 listed files and the 810 of `us/fontex_expand.dat`. The lines keep each file's record order, which
is key order in 23 of the 63 files. The builder `0x001B4D70` files every record by its key (`0x001FDCC0`) and
`0x001E9860` looks glyphs up by key, and no file repeats a key.

The header of each file is in [Font files](fonts-files.md), which also says how the two tables hold every byte of
each `.dat`. [Fonts](fonts.md) gives the record layout and what reads each field.

### What the key is

The key is a glyph index in some fonts and a Unicode code point in the others. Set against the code point of the
record's own character, the key is:

| Font | Records | Key |
|---|---:|---|
| `font00`, `fontguide`, `fontquest`, `fonttutorial` | 8,591, 56, 191, 63 | a glyph index; never the character's code point |
| `fontex_subtitle` in `us` | 1,301 | a glyph index; never the character's code point |
| `fontex_subtitle` in `ch`, `cn`, `jp`, `kr` | 5,805 | the character's code point |
| every other font | 7,243 | the character's code point |

### Properties of the records

- Every record's `utf8` word decodes to one printable character.
- Every record's `cellW` and `cellH` equal its file header's.
- `advance2` equals `advance` in every record.
- `kernCp` is -1 in 22,078 records and the code point of the record's own character in the other 1,172. Those
  1,172 are in `font_square`, `font_venus` and the six `font_stf_*` fonts, `kr/font00` (50) and `fontex_subtitle`
  in `kr` (5) and `us` (148).

## Columns

| Column | Meaning |
|---|---|
| `folder`, `file` | the font folder and the `.dat` file |
| `record` | the record's 0-based place in the file |
| `key` | the glyph's key (above) |
| `char` | the character the `utf8` word spells |
| `utf8` | the record's `+0x04` word in hex: the character's UTF-8 bytes packed from the low byte |
| `atlasX`, `atlasY` | the left and top edge in the atlas, `atlasY` counted from the top (`0x002AA5C7`) |
| `cellW`, `cellH` | the width and height in the atlas |
| `advance2`, `advance` | the two advance words; the pen advance is `advance` (`0x002AC4EC`) |
| `kernCp` | the code point the glyph kerns as, or -1 for no kerning (`0x002AC527`) |

## Related

- [Fonts](fonts.md) - the record layout and how a glyph is drawn and spaced.
- [Font files](fonts-files.md) - each `.dat` header and the round trip.
- [Font kerning pairs](fonts-kerning.md) - the pairs keyed by `kernCp`.
- [Font expansion lists](fonts-expansion-lists.md) - the lists whose values are glyph keys.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 10 calls with 2 other topics</summary>

**Graphics** (explained on [fonts files](fonts-files.md), [fonts](fonts.md))

| Function | | Functions |
|---|---|---|
| `0x001B4D70` | calls | `0x001FC060`, `0x001FDCC0`, `0x001FE020`, `0x001FE080` |

**Game files and data tables** (explained on [fonts files](fonts-files.md), [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md), [fonts](fonts.md))

| Function | | Functions |
|---|---|---|
| `0x001B4D70` | calls | `0x001B5480`, `0x001B5750`, `0x001B58E0`, `0x0020B5F0` |
| `0x001B4D70` | is called by | `0x001B5FE0` |
| `0x001FDCC0` | is called by | `0x001B4D70` |

</details>
