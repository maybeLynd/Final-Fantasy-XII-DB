---
title: "Font expansion lists: every expansion list of every shipped font, with the script path it belongs to and the glyphs it holds"
kind: "reference"
category: "Menus and HUD"
addresses: "0x001B4C00, 0x001B6030, 0x001FDB90, 0x001FDB50, 0x00674A00, 0x001B6350, 0x001E9860"
---

## What it lists

`fonts-expansion-lists.tsv` holds one line for each value of the 14 `.fex` files: 127,031 values in 127,070 lines,
because each of the 39 lists that hold no value has one line of its own. The reader `0x001B4C00` (through `0x001B6030`)
adds each list for its key with `0x001FDB90` and writes value i with `0x001FDB50`; `0x001E9860` then draws glyph
`list[index]` for text whose key has a list, as [Fonts](fonts.md) describes. The lines keep the file order.

[Font files](fonts-files.md) says which `.fex` files are requested and how the table rebuilds every `.fex` byte
for byte.

### The path of a list

A list's key is `0x00674A00` of a name (`0x001B6350`): for a `fontex_expand` or `fontex_subtitle` list a path
`event\<folder>\<name>` or `plan_map\<folder>\<name>`, and for a `fontmonster` list `handbook_monster<NNN>.txt`.

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
