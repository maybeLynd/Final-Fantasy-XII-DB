---
title: "Font expansion lists: every expansion list of every shipped font, with the script path it belongs to and the glyphs it holds"
kind: "reference"
category: "Menus and HUD"
addresses: "0x001B4C00, 0x001B6030, 0x001FDB90, 0x001FDB50, 0x00674A00, 0x001B6350, 0x001E9860"
---

## What it lists

[`fonts-expansion-lists.tsv`](fonts-expansion-lists.tsv) holds one line for each value of the 14 `.fex` files: 127,031 values in 127,070 lines,
because each of the 39 lists that hold no value has one line of its own. The reader `0x001B4C00` (through `0x001B6030`,
which runs it only while the font manager `[0x01F81200]` exists, `0x001B604A`-`0x001B606D`)
adds each list for its key with `0x001FDB90` and writes value i with `0x001FDB50`; `0x001E9860` then returns the record
of glyph `list[index]` for text whose key has a list (`0x001E9880`-`0x001E988B`), as [Fonts](fonts.md) describes. The
lines keep the file order.

[Font files](fonts-files.md) says which `.fex` files are requested and how the table rebuilds every `.fex` byte
for byte.

Each list belongs to one scene or map folder, or to one Bestiary text bundle. While text from that place is drawn,
each character number in the text picks an entry of the list, and that entry names the glyph to draw from the font's
`.dat` of the same name.

### Text read through a screen's font

The guide and quest screens draw expansion glyphs from their own fonts, not from a list. Their tables keep each
glyph as `{expansion glyph N}`, because N means a different character in each font.
[`fonts-resolved-text.tsv`](fonts-resolved-text.tsv) keeps that text and gives the readable text beside it.

| Column | Meaning |
|---|---|
| `table`, `file`, `folder`, `row`, `column` | where the text is: the table, the game file, the language folder, the row's own fields, and the column |
| `font` | the font used, `fontguide.dat` or `fontquest.dat`; `-` when no font applies |
| `tokens`, `kept` | how many marks the text holds, and how many stay as written |
| `text`, `resolved` | the text as the source table has it, and with each joined mark replaced by its character |

The `kr`, `ch` and `cn` folders use the font folder of their own name, and `in` uses `jp`, whose `fontquest.dat` has
the 121 records of the `in` sheet. `de`, `es`, `fr`, `it` and `us` use `us` (`0x001B44A0`). A mark joins on the record
whose key is N.

Every mark in `menumap_guide00.bin` and in the quest files joins. Marks in `menumap_guide01.bin` to `04` stay as
written: the schedule never requests those files, so no font is bound to their pictures, and the `us` font
folder, which `es`, `fr`, `it` and `us` read, has no `fontguide.dat`.

`Database/Tools/catalogues/expansion_text.py` writes this table.

### The path of a list

A list's key is `0x00674A00` of a name (`0x001B6350`): for a `fontex_expand` or `fontex_subtitle` list a path
`event\<folder>\<name>` or `plan_map\<folder>\<name>`, and for a `fontmonster` list `handbook_monster<NNN>.txt`.

`0x001B6350(manager, id, kind, name, value)`, called only from `0x0017FA90` (`0x0017FAC4`), files a request for such a
font on the font manager. It takes a record from the pool at the manager's `+0x190` (`0x001BA860`), stores 1 at
`+0x00`, 0 at `+0x08`, the id at `+0x04`, the kind byte at `+0x10`, the name's hash at `+0x14` and the value at
`+0x18` (`0x001B63A4`-`0x001B63D2`), and appends the record to the pending vector at `+0x250` (`0x001B63D5`-`0x001B63EC`),
through `0x001AB570` when the vector is full (`0x001B640C`-`0x001B6414`).

A request whose id and kind match a pending record is dropped before a record is taken: `0x001B6350` then only calls
the empty stub `0x0016D6A0` (`0x001B6380`-`0x001B638D`, `0x001B63F1`-`0x001B6407`).

The `path` column gives the path that hashes to the key among 1,281 candidates: every `<folder>\<name>` pair of
folder names under `plan_master/<lang>/event/` and `plan_master/<lang>/plan_map/` of the nine language trees, 346 of
them `event`. No two candidates share a hash.

The `fontmonster` keys are the hashes of `handbook_monster000.txt` onward, the font names of the Bestiary text
bundles ([Handbook files](../Game-Files-And-Data-Tables/handbook-files.md)): 000 to 013 in `jp`, 000 to 006 in
`kr` and `cn` and 000 to 005 in `ch`. The trees that use these fonts ship text bundles 000 to 010 (`in`), 000 to 003
(`kr`) and 000 to 004 (`cn` and `ch`), so lists 011 to 013 of `jp`, 004 to 006 of `kr`, 005 and 006 of `cn` and 005
of `ch` belong to no shipped bundle.

| File | Lists | With no value | `event` path | `plan_map` path | No path |
|---|---:|---:|---:|---:|---:|
| `ch/fontex_expand.fex` | 465 | 3 | 69 | 396 | 0 |
| `ch/fontex_subtitle.fex` | 171 | 5 | 162 | 9 | 0 |
| `ch/fontmonster.fex` | 6 | 0 | 0 | 0 | 6 |
| `cn/fontex_expand.fex` | 447 | 3 | 68 | 379 | 0 |
| `cn/fontex_subtitle.fex` | 171 | 5 | 162 | 9 | 0 |
| `cn/fontmonster.fex` | 7 | 0 | 0 | 0 | 7 |
| `jp/fontex_expand.fex` | 482 | 3 | 33 | 449 | 0 |
| `jp/fontex_subtitle.fex` | 172 | 6 | 164 | 8 | 0 |
| `jp/fontmonster.fex` | 14 | 0 | 0 | 0 | 14 |
| `kr/fontex_expand.fex` | 389 | 3 | 38 | 351 | 0 |
| `kr/fontex_subtitle.fex` | 177 | 11 | 162 | 15 | 0 |
| `kr/fontmonster.fex` | 7 | 0 | 0 | 0 | 7 |
| `us/fontex_expand.fex` | 483 | 0 | 32 | 451 | 0 |
| `us/fontex_subtitle.fex` | 217 | 0 | 217 | 0 | 0 |

### The two us files

`us/fontex_expand.fex` and `us/fontex_subtitle.fex` are 12-byte triples `{key, index, value}`, 9,032 and 11,481 of
them, and no flag requests them. Each of their lines is one triple, with `list` empty and `ordinal` the stored index.
The triples of one key stand together with indices 0, 1, 2 and on, so they hold the same lists the chunk form would.

### The glyph of a value

A value is a glyph key of the `.dat` with the same name. The `char` column gives that glyph's character. It is
empty for 3,249 values of `us/fontex_subtitle.fex`, which are no key of `us/fontex_subtitle.dat`: that file keys
its 1,301 glyphs by index, 0 to 1,300, and those values run from 8,213 to 65,374. Every other value names a glyph.

## Columns

| Column | Meaning |
|---|---|
| `folder`, `file` | the font folder and the `.fex` file |
| `list` | the list's 0-based place in the file; empty in the two triple files |
| `key_hash` | the list's key, the `0x00674A00` hash, in hex |
| `path` | the path that hashes to the key (above); empty when no candidate does |
| `ordinal` | the value's place in its list, the index `0x001E9860` reads; empty on the one line of a list with no values |
| `value` | the glyph key the ordinal draws |
| `char` | the character of that glyph in the same-named `.dat` (above) |

## Related

- [Fonts](fonts.md) - the list format, the reader and how text binds a list.
- [Font files](fonts-files.md) - which `.fex` files are requested, and the round trip.
- [Font glyphs](fonts-glyphs.md) - the glyph records the values name.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x001BA860` is called by `0x002120E0`; those functions are documented on
  [audio manager](../Sound-And-Music/audio-manager.md).
- Presentation: `0x001AB570` is called by `0x001BD4A0`, `0x001BDD20`; `0x001BA860` is called by `0x001BB2B0`, `0x001BB920`; those
  functions are documented on [character render object](../Graphics/character-render-object.md),
  [add motion tables](../Graphics/add-motion-tables.md),
  [file size tables fst](../Game-Files-And-Data-Tables/file-size-tables-fst.md).
- Presentation: and on [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md).
- Resource: `0x001AB570` is called by `0x0019E7B0`; `0x001B4C00` is called by `0x001B6030`; `0x001BA860` is called by
  `0x0019E7B0`, `0x0019EB60`, `0x001A0A90`, `0x001B5480`, `0x001B5610`, `0x001B5750`, `0x0020B680`; `0x00674A00` is called by
  `0x001A7A50`, `0x001A9050`, `0x001B1440`, `0x001B1C10`, `0x0020BE50`, `0x0020C1B0`.
- Resource: those functions are documented on
  [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md), [fonts](fonts.md),
  [async load manager](../Game-Files-And-Data-Tables/async-load-manager.md), [fonts files](fonts-files.md),
  [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md).
- Resource: and on [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
  [sprite batcher](../Graphics/sprite-batcher.md).
