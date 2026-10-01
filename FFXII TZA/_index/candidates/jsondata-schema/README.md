# The `jsondata/` schema: nesting, value types and ranges, and the reader that spells each key (OPUS, 2026-09-25, block 293)

**Why.** S-39's script/data cell is PARTIAL because *"the JSON schema itself is not decoded"*
(L2-VERDICTS, § 'S-39 has a contract'). The seam is already established:
- `JsonData/init.json`, `JsonData/maps/<map>.json` and `JsonData/CutScenes/<scene>.json`;
- the key-name census and the closed 17-function reader population
  (`17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md` §8b–8d).

What was missing was the schema. This package supplies it.

## Instrument

`jsondata_schema_census.py`.
- **Documents.** It walks every document of an extracted `jsondata/` tree (vbfextract of the retail VBF; 830 files).
  For every path it records:
  - the value types seen (int / float / string / bool / null / array<…> / object);
  - how many files carry the path, how many times it occurs, and the numeric min / max.
- **Composed keys.** `Cut N`, `PresetDof N`, `MonsterId N`, `fontclut_N` and bare numerics are folded into
  `<template>` paths.
- **Readers.** For every literal key name, the script finds the NUL-terminated string in the SHA-asserted EXE and
  attributes each rip-relative reference to its containing function. `readers(17-set)` lists the members of §8d's
  reader population that reference it. `any_image_ref` lists up to four references of any kind.
- **Outputs.** `jsondata_schema.tsv` has 564 path rows. `jsondata_schema.out.txt` is the summary.

## The schema

| family | files | shape | paths | read by the 17 (literal) | composed | no literal reader |
|---|---:|---|---:|---:|---:|---:|
| `init.json` | 1 | a flat object of 176 keys: render toggles (`Enable*`, 0/1 ints), float tunables, `ModelsToPreload` (array<string>) | 176 | 165 | 0 | 11 |
| `maps/<map>.json` | 459 | a flat object: a **strict subset of `init.json`'s keys** (§8c); per-area overrides | 175 | 133 | 0 | 42 |
| `cutscenes/<scene>.json` | 337 | **`{ "Common": {…}, "Cut N": {…}, … }`**. `Common` holds 76 distinct keys and occurs in 282 files; `Cut N` holds 43 keys, 3,498 blocks over 281 files. The `Cut N` block names are composed at run time | 121 | 99 | 2 | 20 |
| `fontcluts/*.json` | 28 | a flat object of 10 keys: `mClutIndex` int, font and shadow RGBA floats, `mClutComment` string | 10 | 9 (all by `001C76E0`) | 0 | 1 (`mClutComment`) |
| `monstergallery.json` | 1 | `{ "Common": {37 keys}, "MonsterId N": {38 keys}, … }`, the cutscene shape with per-monster blocks | 77 | 76 | 1 | 0 |
| `monstertoweapon.json` | 1 | `{ "<N>": { "ModelName": string, "<N>": { "ModelName", "WeaponIndex": int } } }` | 5 | 0 | 2 | 3 (no literal reference anywhere in the image; **not claimed unread**, since the names may be composed) |
| `uisize/*.json`, `0.json` | 3 | see the defects below; `0.json` is `{}` | — | — | — | — |

**`Common` is read by `001C3D50`, `001C51D0`, `001C52C0`, `001C5570`, `001C5750` and `001C6320`.** Its per-key types and
ranges, and the same for every `Cut N` key, are rows of `jsondata_schema.tsv`.

**Numbers are written without a type distinction.** 41 map paths mix `int` and `float` for the same key. For example,
`mGlareLuminance` is `int` 413 times and `float` 45 times, and `lightHeight` is 241 / 199. Whole values are emitted as
integers, so a reader must coerce. That this engine's reader does so is implied by the shipped data being used; the
reader's code was not read here.

## Shipped documents that are not strict JSON (30 of 830)

| files | defect |
|---|---|
| 26 × `cutscenes/sum_[a–m]000[02].json` | **zero bytes**, already noted in the ordered-render-command-list page |
| `cutscenes/evt_t0005.json` | a missing `,` between `"Cut 4": {…}` and `"Cut 5"` (line 227) |
| `maps/bhm0201.json` | a missing `,` after `"mUseLinearTonemap": 1` (line 44) |
| `uisize/uisize.json`, `uisize/uisize_sd.json` | a trailing comma before `}` |

How the engine's reader treats these files (rejects them, stops early, or tolerates them) is **not established here**.
It needs the reader body `001FF6B0` or a live load.

## What this does and does not claim

It claims the **on-disk schema of every shipped `jsondata/` document**: nesting, key population, value types and
ranges, and the literal reader of each key. That is the "decoded" half S-39's cell asks for. The per-key **meaning** stays
with the pages (§8b–8d, the render command list's settings commands). The reader's tolerance of malformed files is open.
