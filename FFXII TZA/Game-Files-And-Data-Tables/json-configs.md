---
title: "JSON configs: every key of the jsondata documents, the code that reads it and what it sets, and the monster viewer's entries"
kind: "reference"
category: "Game files and data tables"
addresses: "00200BF0, 001FF740, 001C7940, 001C3D50, 001C6320, 001C6C00, 001CA600, 001C76E0, 001C3760, 00194400, 001EBB60, 002C530B"
---

## What it lists

`json-configs.tsv` holds one line for each of the 717 keys of the 830 documents under `jsondata/`, by family:

| Family | Documents | Keys | Keys the executable names | Read by |
|---|---:|---:|---:|---|
| `maps/` | 459 | 176 | 134 | `001C7940`, an area's scene settings |
| `cutscenes/` | 337 | 84 | 70 | `001C3D50`, a cutscene's scene settings |
| `init.json` | 1 | 176 | 165 | `001C7940` and `001C3D50`, as the last fallback; `001C3760` reads `ModelsToPreload` and the four `TrackingMapScreen*` keys itself |
| `uisize/` | 2 | 231 | 226 | `001CA600`, the UI layout cells |
| `fontcluts/` | 28 | 10 | 9 | `001C76E0`, the text palettes |
| `monstergallery.json` | 1 | 38 | 38 | `001C6320`, the monster viewer |
| `monstertoweapon.json` | 1 | 2 | 0 | never opened |

`0.json` is `{}` and holds no key. [json-monster-gallery.tsv](json-monster-gallery.tsv) holds the 385 entries of
`monstergallery.json`, `Common` and `MonsterId0` to `MonsterId383`, one column per key.

The file formats, the parser and the order in which the loaders look keys up are on
[Standard file formats](standard-file-formats.md) and
[Graphics settings](../Engine-Core/graphics-settings.md); this page is the shipped content.

### How a key is read

`00200BF0` parses a document. A loader then asks for each key by its name with `001FF740` and reads the value as a
number or a string. 75 keys have no string of their own in the executable, and 63 of them are never asked for,
authored and ignored: among them the 27 `...CheckBoxCheckState` keys of the map files and both keys of
`monstertoweapon.json`, a file whose name no string in the executable holds.

The other twelve are `mCascadePartition<a>_2` and `mCascadePartition<a>_3` of the map and `init.json` documents:
`001C7940` builds those names from the format `"mCascadePartition%d_%d"` (`001C9199`) and reads them. In cutscene
documents the same keys are never asked for, because `001C3D50` reads only the `_1` names.

`001C3760` parses `init.json` into the global document `01F813C8`, which the area and cutscene loaders fall back
to. A scene setting is looked up in order: an area's in its map document and then in
`init.json`, a cutscene's in its cut section, its `Common` section, the current map document and `init.json`
(`001C3D50`).

The monster viewer reads entry `MonsterId<n>` (`001C6320`). For nine keys it falls back to `Common`
when the entry lacks them: `eyeVfxZBias`, `lightAmbientA`, `variation`, `clut`, `motionRate`, `bgColorR`, `bgColorG`,
`bgColorB` and `drawBgColor` (`001C6563`-`001C6B72`). `monsterWeaponIndex2` is read only when the entry has it
(`001C6419`), and the other 28 keys are read from the entry alone, so a missing one reads as 0 (`001C63E7`,
`001C6450`).

### How it is built

`Database/Tools/catalogues/json_configs.py`:

1. every `.json` file under `jsondata/` of the extract, sorted; four are not strict JSON (a trailing comma, or a
   missing comma between members) and the decoder repairs only those two defects: `cutscenes/evt_t0005.json`,
   `maps/bhm0201.json`, `uisize/uisize.json` and `uisize/uisize_sd.json`; 26 cutscene documents are empty;
2. every leaf of every document, keyed by family and the leaf's own name, with the documents that carry it, its
   JSON types and its values;
3. whether the executable holds the name as a string between two zero bytes, and at which file offset;
4. the reader columns from `json-config-readers.tsv` beside the script, one row per family and key, written from
   the loaders' code; the script refuses to write when that table and the files name different keys;
5. for the gallery, every entry's keys as columns, and the model file and bestiary names that
   [Bestiary](../Enemy-Spawning/bestiary.md) lists for the entry's model id.

### Checks

- The extract holds 830 `.json` files under `jsondata/`: 459 map, 337 cutscene, 28 palette and 2 UI-size documents
  and the four root files. The TSV has 717 data lines, one per family and key, and the reader table names the
  same 717.
- `monstergallery.json` has 385 entries and the gallery TSV 385 data lines.
- Two runs over the same files give byte-identical output.
- `lightShaftColorR`, `G` and `B` compared with the code: `001C7940` reads the three and `lightShaftColorA` into
  four floats and passes them to `00194400` (`001C8AF5`), which stores the first three at `+0xC4`, `+0xC8` and
  `+0xCC` of the post-process parameter object and 0 at `+0xD0`.
- `modelScale` compared with the code: its setter `001EBB60` stores the value at `+0x23C` of the monster viewer.
- `ActionListMistLineOffset` compared with the code: the battle menu adds the global `01E0CEA0` it sets to the
  word it reads at `+0x9E` (`002C5304`, `002C530B`).
- Where a row says a value is only written, the sweep it rests on is named in the row: every access to the field
  in the object's own methods, the functions that load the object's pointer, and the callers of its getter.

## Columns

`json-configs.tsv`:

| Column | Meaning |
|---|---|
| `family`, `key` | the document family and the key's own name |
| `documents` | how many documents of the family carry the key |
| `types`, `values` | the JSON types (`int`, `float`, `string`, `bool`, `null`) and the values over all documents: each value when there are at most four; else, for numbers, the range and how many values, and for strings how many values with the first three |
| `named_in_exe` | `yes` with the file offset of the name when the executable holds it as a string, else `no` |
| `reader` | the function that asks for the key, and the documents it looks in |
| `destination` | where the value is stored: the object and offset, or the global |
| `conversion` | how the value is converted on the way, `-` for none |
| `explanation` | what the value does, with the code that uses it |
| `evidence` | the lookup sites and the pages that describe the use |

`json-monster-gallery.tsv`:

| Column | Meaning |
|---|---|
| `entry` | `Common` or `MonsterId<n>`, where `n` is the Bestiary entry number |
| `model`, `names` | the model file of `monsterModelId` and up to three bestiary names that use it |
| `monsterModelId` ... `light2DirZ` | the entry's values, one column per key; an empty cell is a key the entry does not carry: the viewer then takes the `Common` value for the nine keys named above, leaves `monsterWeaponIndex2` unread, and reads 0 for the others |
| `explanation` | a one-line summary: the entry, its model and who uses it |

## Related

- [Standard file formats: the TGA, CSV, JSON, WebM, C-header and PS2 icon files the game ships, and which of them it reads](standard-file-formats.md)
- [Graphics settings: the render settings block, its scene-config keys, its defaults and the shader constants it feeds](../Engine-Core/graphics-settings.md)
- [Post-processing: the game's passes and their shader constants, the post-process command, the PPFX features and effect techniques, and the registries of named render passes](../Graphics/post-processing.md)
- [Screen layouts: the UISize layout files, every key they set, the loader that binds each key to its cell, and the screens that read them](../Menus-And-HUD/screen-layouts.md)
- [Fonts: the font files a language uses, their kerning pairs and expansion lists, and how digits and glyphs are laid out](../Menus-And-HUD/fonts.md)
- [Clan Primer: the Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages, how entries unlock, and the monster viewer](../Menus-And-HUD/clan-primer.md)
