---
title: "Font glyphs: every glyph record of every shipped font, with its character, atlas rectangle, advance and kerning code point"
kind: "reference"
category: "Menus and HUD"
addresses: "0x001B4D70, 0x001FDCC0, 0x001E9860, 0x002AA5C7, 0x002AC4EC, 0x002AC527"
---

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
