---
title: "Font files: every shipped font data file with its size, its form, its place in the font list and its .dat header"
kind: "reference"
category: "Menus and HUD"
addresses: "0x001B44A0, 0x001B4930, 0x001B4D70, 0x001B4E19, 0x001B5230, 0x001B4C00"
---

## What it lists

`fonts-files.tsv` holds one line for each data file in the five font folders `ch`, `cn`, `jp`, `kr` and `us` of
`GameData/D3D11/ArtData/font/`: 5 `fontlist.ah`, 63 `.dat`, 34 `.ker` and 14 `.fex`, 116 files. For a `.dat` the
line also carries the file's header. [Fonts](fonts.md) gives the formats and how `0x001B44A0` picks a folder and loads
its list. The `<name>.dds.phyre` atlases are textures and are in no table.

Three tables hold the rest of the data: the glyph records in [Font glyphs](fonts-glyphs.md), the pairs in
[Font kerning pairs](fonts-kerning.md) and the lists in [Font expansion lists](fonts-expansion-lists.md).

### How the tables rebuild the files

`Database/Tools/catalogues/font_tables.py write` decodes every data file into the four tables.
`font_tables.py check` reads the four tables back, rebuilds each file from them alone and compares it with the
shipped file. All 116 files rebuild byte for byte:

| File | Rebuilt from |
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

A `.dat` is requested when its folder's `fontlist.ah` names it (`0x001B4930`), and a `.ker` or `.fex` when its
`.dat` is requested and has flag bit 0 or 1 set (`0x001B4E19`; readers `0x001B5230` and `0x001B4C00`). That gives 62 of
the 63 `.dat`, 25 of the 34 `.ker` and 12 of the 14 `.fex` files. The ones never requested are:

- `us/fontex_expand.dat`, with its `.fex`;
- `us/fontex_subtitle.fex`: its `.dat` has flags `0x1`;
- `font00.ker` in all five folders and `font_iwa_g12.ker` in `jp` and `us`: those `.dat` files have flags `0x0`;
- `fontex_expand.ker` in `ch`, `cn` and `kr`: those `.dat` files have flags `0x2`.

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

## Related

- [Fonts](fonts.md) - the formats, the loaders and how text reaches a glyph.
- [Font glyphs](fonts-glyphs.md) - every glyph record of every `.dat`.
- [Font kerning pairs](fonts-kerning.md) - every pair of every `.ker`.
- [Font expansion lists](fonts-expansion-lists.md) - every list of every `.fex`.
