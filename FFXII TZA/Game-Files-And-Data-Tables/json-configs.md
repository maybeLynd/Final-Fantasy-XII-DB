---
title: "JSON configs: every key of the jsondata documents, the code that reads it and what it sets, and the monster viewer's entries"
kind: "reference"
category: "Game files and data tables"
addresses: "0x00200BF0, 0x001FF740, 0x001C7940, 0x001C3D50, 0x001C6320, 0x001C6C00, 0x001CA600, 0x001C76E0, 0x001C3760, 0x00194400, 0x001EBB60, 0x002C530B"
---

## What it lists

[`json-configs.tsv`](json-configs.tsv) holds one line for each of the 717 keys of the 830 documents under `jsondata/`, by family:

| Family | Documents | Keys | Keys the executable names | Read by |
|---|---:|---:|---:|---|
| `maps/` | 459 | 176 | 134 | `0x001C7940`, an area's scene settings |
| `cutscenes/` | 337 | 84 | 70 | `0x001C3D50`, a cutscene's scene settings |
| `init.json` | 1 | 176 | 165 | `0x001C7940` and `0x001C3D50`, as the last fallback; `0x001C3760` reads `ModelsToPreload` and the four `TrackingMapScreen*` keys itself |
| `uisize/` | 2 | 231 | 226 | `0x001CA600`, the UI layout cells |
| `fontcluts/` | 28 | 10 | 9 | `0x001C76E0`, the text palettes |
| `monstergallery.json` | 1 | 38 | 38 | `0x001C6320`, the monster viewer |
| `monstertoweapon.json` | 1 | 2 | 0 | never opened |

`0.json` is `{}` and holds no key. [json-monster-gallery.tsv](json-monster-gallery.tsv) holds the 385 entries of
`monstergallery.json`, `Common` and `MonsterId0` to `MonsterId383`, one column per key.

[json-configs-values.tsv](json-configs-values.tsv) holds every value of every document, 93,715 rows from the 804
documents that are not empty (29 of them, `0.json` among them, are an empty object and give no row). The four
documents that are not strict JSON are read with the trailing comma dropped or the missing commas supplied; no
document repeats a key.

[json-configs-documents.tsv](json-configs-documents.tsv) lists the 832 files under `jsondata/` one by one: the 830
documents and the two struct files `parametersmanageruisizestruct.csv` and `parametersmanagermonstergallerystruct.txt`,
3,242,429 bytes in all. Each row gives the file's size, its SHA-256 and the number of rows [`json-configs-values.tsv`](json-configs-values.tsv)
gives it: 775 documents give rows, 29 are an empty object and 26 are files of 0 bytes.

[json-configs-inputs.tsv](json-configs-inputs.tsv) gives each of the 717 keys as a setting a modder can change: its
types and shipped values, which document wins when several hold it, when the game reads it, what it sets, what the
player sees and when it changes nothing. 65 keys change nothing: no loader reads them from their documents, and
`monstertoweapon.json` is never opened.

One more file under `jsondata/` is text, not JSON: `parametersmanagermonstergallerystruct.txt`, 1,781 bytes, LF line ends, no line end after the last line. No string in the executable holds its name or a setter name in it; the viewer reads `JsonData/MonsterGallery.json`.

- The first line is the column title `#title name, dummy, type, dummy, min, max, default.`
- Each of the 33 lines after it names one monster viewer setting, then `in`, `int` or `float`, a setter name, a minimum, a maximum and a default.
- The settings: `motionIndex` 0 to 80, `motionRepeatFrame` 0 to 300 (default 240), `motionRate` 0.1 to 2.0 (0.5), `modelScale`, `cameraPitch`, `cameraYaw`, `xOffset`, `yOffset`, `cameraFov`, the ambient light's colour and intensity, two directional lights' direction, colour and intensity, the background colour, `drawBgColor` and `eyeVfxZBias` -20000 to 0 (default -7000).
- The setter is `setMotionIndex2` in 27 lines, `setMotionIndex1` in 3, `setMotionIndex` in 1 and `dummy` in 2.

The file formats, the parser and the order in which the loaders look keys up are on
[Standard file formats](standard-file-formats.md) and
[Graphics settings](../Engine-Core/graphics-settings.md); this page is the shipped content.

### How a key is read

`0x00200BF0` parses a document. A loader then asks for each key by its name with `0x001FF740` and reads the value as a
number or a string. 75 keys have no string of their own in the executable, and 63 of them are never asked for,
authored and ignored: among them the 27 `...CheckBoxCheckState` keys of the map files and both keys of
`monstertoweapon.json`, a file whose name no string in the executable holds.

The other twelve are `mCascadePartition<a>_2` and `mCascadePartition<a>_3` of the map and `init.json` documents:
`0x001C7940` builds those names from the format `"mCascadePartition%d_%d"` (`0x001C9199`) and reads them. In cutscene
documents the same keys are never asked for, because `0x001C3D50` reads only the `_1` names.

`0x001C3760` parses `init.json` into the global document `0x01F813C8`, which the area and cutscene loaders fall back
to. A scene setting is looked up in order: an area's in its map document and then in
`init.json`, a cutscene's in its cut section, its `Common` section, the current map document and `init.json`
(`0x001C3D50`).

The monster viewer reads entry `MonsterId<n>` (`0x001C6320`). For nine keys it falls back to `Common`
when the entry lacks them: `eyeVfxZBias`, `lightAmbientA`, `variation`, `clut`, `motionRate`, `bgColorR`, `bgColorG`,
`bgColorB` and `drawBgColor` (`0x001C6563`-`0x001C6B72`). `monsterWeaponIndex2` is read only when the entry has it
(`0x001C6419`), and the other 28 keys are read from the entry alone, so a missing one reads as 0 (`0x001C63E7`,
`0x001C6450`).

### Where the values come from

The columns come from the documents and from the loaders that read them:

1. every `.json` file under `jsondata/` of the extract, sorted; four are not strict JSON (a trailing comma, or a
   missing comma between members): `cutscenes/evt_t0005.json`,
   `maps/bhm0201.json`, `uisize/uisize.json` and `uisize/uisize_sd.json`; 26 cutscene documents are empty;
2. every leaf of every document, keyed by family and the leaf's own name, with the documents that carry it, its
   JSON types and its values;
3. whether the executable holds the name as a string between two zero bytes, and at which file offset;
4. the reader columns, one row per family and key, from the loaders' code;
5. for the gallery, every entry's keys as columns, and the model file and bestiary names that
   [Bestiary](../Enemy-Spawning/bestiary.md) lists for the entry's model id.

## Columns

[`json-configs.tsv`](json-configs.tsv):

| Column | Meaning |
|---|---|
| `family`, `key` | the document family and the key's own name |
| `documents` | how many documents of the family carry the key |
| `types`, `values` | the JSON types (`int`, `float`, `string`, `bool`, `null`) and the values over all documents: each value when there are at most four; else, for numbers, the range and how many values, and for strings how many values with the first three |
| `named_in_exe` | `yes` with the file offset of the name when the executable holds it as a string, else `no` |
| `reader` | the function that asks for the key, and the documents it looks in |
| `destination` | where the value is stored: the object and offset, or the global |
| `conversion` | how the value is converted on the way, `-` when the value is not converted |
| `explanation` | what the value does, with the code that uses it |
| `evidence` | the lookup sites and the pages that describe the use |

[`json-monster-gallery.tsv`](json-monster-gallery.tsv):

| Column | Meaning |
|---|---|
| `entry` | `Common` or `MonsterId<n>`, where `n` is the Bestiary entry number |
| `model`, `names` | the model file of `monsterModelId` and up to three bestiary names that use it |
| `monsterModelId` ... `light2DirZ` | the entry's values, one column per key; an empty cell is a key the entry does not carry: the viewer then takes the `Common` value for the nine keys named above, leaves `monsterWeaponIndex2` unread, and reads 0 for the others |
| `explanation` | a one-line summary: the entry, its model and who uses it |

[`json-configs-values.tsv`](json-configs-values.tsv):

| Column | Meaning |
|---|---|
| `document` | the archive path of the document |
| `key` | the key's path: nested keys joined by `.`, an array element as `[i]` |
| `type` | the JSON type: `int`, `float`, `string`, `bool` or `null` |
| `value` | the value as the document spells it; a tab or line break inside a string is written `\t` or `\n` |

[`json-configs-documents.tsv`](json-configs-documents.tsv):

| Column | Meaning |
|---|---|
| `document` | the archive path of the file |
| `bytes` | the file's size |
| `sha256` | the SHA-256 of the file's bytes |
| `value_rows` | the rows [`json-configs-values.tsv`](json-configs-values.tsv) gives the document; 0 for an empty object, a file of 0 bytes and the two struct files |

## Related

- [Standard file formats: the TGA, CSV, JSON, WebM, C-header and PS2 icon files the game ships, and which of them it reads](standard-file-formats.md)
- [Graphics settings: the render settings block, its scene-config keys, its defaults and the shader constants it feeds](../Engine-Core/graphics-settings.md)
- [Post-processing: the game's passes and their shader constants, the post-process command, the PPFX features and effect techniques, and the registries of named render passes](../Graphics/post-processing.md)
- [Screen layouts: the UISize layout files, every key they set, the loader that binds each key to its cell, and the screens that read them](../Menus-And-HUD/screen-layouts.md)
- [Fonts: the font files a language uses, their kerning pairs and expansion lists, and how digits and glyphs are laid out](../Menus-And-HUD/fonts.md)
- [Clan Primer: the Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages, how entries unlock, and the monster viewer](../Menus-And-HUD/clan-primer.md)
