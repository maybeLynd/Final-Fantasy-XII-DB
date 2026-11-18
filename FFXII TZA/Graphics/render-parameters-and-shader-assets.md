[Home](../../README.md) / [Graphics](README.md) / Render parameters and shader assets

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Render parameters and shader assets: the post-process shader files and the scene-parameter documents | system | Graphics | Screen effects and movies | The shader assets the post-process chain loads by path and where their handles are kept, and the scene-parameter JSON documents (the global defaults, one per map, one per cutscene): their shipped shape, the functions that look their keys up, the cascade keys composed at run time, and the authored keys no code reads. | 0x01DF0910, 0x0018D850, 0x0019CB20, 0x001FF740, 0x001FF6B0, 0x001C51D0, 0x001C3D50, 0x001C7940, 0x001CA600, 0x001C9190, 0x001A9B00, 0x001A9930, 0x008FB2D8 |

## What the player sees

How each place and each cutscene looks after the geometry is drawn, its shadow softness, ambient
occlusion strength, glare, depth of field, water and eye shine, comes from per-map and per-cutscene
value files, read when the map or scene loads, and from a small set of post-process shader files.
Some values in those files are left over from the tool that wrote them and change nothing.

## How it works

### The shader assets

The executable names 18 `.phyre` assets by full path: the post-process chain, text, video, the colour-buffer
copy, the anisotropic lighting texture and the map textures:

| Path | Use |
|---|---|
| `/GameData/D3D11/ArtData/shaders/SAO.fx.phyre`, `UnSharpMask`, `HBAO`, `PS2DepthOfField`, `SeparableSSS`, `GaussianFilter`, `PhyreFXAA`, `SMAA` (`.fx`), `searchtex`, `areatexdx10` (`.dds`), `depthmask`, `BrightnessShader` (`.fx`) | the pointer table `0x01DF0910`, in this order |
| `/GameData/D3D11/ArtData/shaders/video.fx.phyre` | `0x001B7850` (`0x001B78E3`) |
| `/GameData/D3D11/ArtData/shaders/PhyreText.fx.phyre`, `/GameData/D3D11/ArtData/font/tuffysdf.fgen.phyre` | the text shader and its distance-field font |
| `/GameData/%s/ArtData/shaders/CopyBuffer.fx.phyre`, `/GameData/%s/ArtData/shaders/anisolighting.dds.phyre` | `%s` is the graphics API folder |
| `/GameData/D3D11/ArtData/map/%s/tex/%s.dds.phyre` | `0x001A6FF0` (`0x001A712D`), the map textures |

`0x0018D850` walks the twelve entries of `0x01DF0910`, requests each path (`0x0019CB20`, `0x0018D8BE`) and
keeps the result at `+0x218 + 8 x i` of the render-parameter block, then configures each
(`0x0018D160`). The twelve entries are ten shaders and the two SMAA lookup textures. The twelve pass
functions on [Post-processing](post-processing.md) draw with them.

`CopyBuffer.fx.phyre` and `anisolighting.dds.phyre` are requested by their users. The
render-manager installer `0x00186CD0` loads the first, with `D3D11` as the folder, through
`0x001EEC80` for the colour-buffer copy pass. The model asset cache's constructor `0x001B9370` loads
the second through `0x001BB190`, which makes the asset ready (`0x0063DA50`, `0x0063B010`), finds its
first object list whose class is `PTexture2D` (`0x02CBB900`) or derives from it, and stores at the
cache's `+0x00` the object address it computes from the list's `+0x60` and the class's `+0xF8`.

### The scene-parameter documents

The values live in JSON inside the archive: `jsondata/init.json` holds the global defaults,
`jsondata/maps/<map>.json` one set per map, and `jsondata/cutscenes/<scene>.json` one set per
cutscene, keyed `Common` and `Cut 1` to `Cut N`. Every key is looked up by name through `0x001FF740`
(and `0x001FF6B0` beneath it); the area loader `0x001C7940` usually falls back to the defaults when a map
omits a key, and the cutscene loader `0x001C3D50` goes through `0x001C51D0`.

The light directions are the
exception: `lightOrientation` and `lightHeight` must both be in the map's own file, or the loader clears
the map-art context's direction flag `+0x398` and applies none of the three pairs (`0x001C7F41`-`0x001C7F6F`,
`0x001C8112`).
[Graphics settings](../Engine-Core/graphics-settings.md) lists where each key lands.

`0x001FF6B0(value, key)` first turns a value whose tag `+0x00` is not 3 into an empty map: it calls
`0x002001F0` on it, stores 3, and keeps a new 0x38-byte map from `0x00210EC0` (constructor `0x001FE510`) at
`+0x08`, or 0 when that allocation fails (`0x001FF6CF`-`0x001FF713`). It then tail-jumps to the find
`0x001FF4F0` with the map and the key (`0x001FF72D`). A key the map lacks gets a new entry of tag 6
(`0x001FF5E1`, `0x001FF647`), so the lookup always returns a value and a missing key becomes an absent entry.

446 distinct key strings are passed as literals at 754 of the 779 call and tail-jump sites of six lookups:
`0x001FF740`, `0x001FF6B0`, `0x001C51D0`, `0x001C52C0`, `0x001C5530` and `0x001C5570`. 439 of the keys reach `0x001FF740`
directly. `0x001C5530(document, key)` repeats the lookup in the document at `0x01F813C8` when the first answer is an
absent entry (tag 6, tested by `0x00200BE0`); `0x001C5570(n, key)` reads the key from the section `PresetDof <n>`.

Of the other 25 sites, 11 pass a composed name and 14 pass on a name their caller gave. 443 of the 446 literal
keys are keys of shipped documents; no document holds `ChangedFileName`, `MapIndex` or `shit`. The three largest
readers are `0x001CA600` (226 keys), `0x001C7940` (157) and `0x001C3D50` (104).

The four composed forms add 486 names: the nine `mCascadePartition<column>_<row>`, and the `Cut <n>` (61),
`PresetDof <n>` (32) and `MonsterId<n>` (384) names the shipped documents hold. Three cascade names are also
passed as literals, by `0x001C3D50` through `0x001C52C0`. Every key, literal or composed, is one row of
[`render-parameters-and-shader-assets-keys.tsv`](render-parameters-and-shader-assets-keys.tsv) with its lookups,
readers and sites.

### The cascade keys are composed

`0x001C7940` never spells `mCascadePartition0_1` and its kin. At `0x001C9190` it formats
`"mCascadePartition%d_%d"` (`0x008FB2D8`) for columns 0 to 2 and rows 1 to 3, reads each value (with
the defaults as fallback) and stores it through `0x001A9B00(map-art context, row - 1, column, v)`.
`0x001A9B00` refuses an index of 3 or more and writes `+0x350 + ((row - 1) x 3 + column) x 4`
of the object `0x001A9930` returns: a 3 x 3 float matrix. No code looks up `mCascadeNumber`, which the files also carry;
the loop is fixed at three.

### Authored keys that nothing reads

Taking every key of `init.json`, the map files and the cutscene files, and setting aside the
section names (`Common`, `Cut N`, `PresetDof N`, `MonsterId N`), gives 218 names. 175 are read,
directly or through the cascade template. The other 43 are:

- 27 `…CheckBoxCheckState` keys and 7 `…Lock` keys (`EnableDofLock`, `EnableYebisLock`,
  `mDofApertureFnumberLock`, `mDofFocusDistanceLock`, `mGammaValueLock`, `mGlareLuminanceLock`,
  `mGlareThresholdLock`): editor state saved with the values;
- `mSAOBias`, `mSAORadius` and `mSAOIntensity`, whose read forms are the `…Chr` and `…Sce` pairs;
- `mCascadeNumber`, `mMapAmbientColorA`, `EnableAutoExposure`, `mWaterParallax`,
  `mDebugWaterExtraFactor` and `DofImageSensorHeight`.

## Shipped data

| Fact | Value |
|---|---|
| post-process shader files | all 16 named `shaders` assets ship under `gamedata/d3d11/artdata/shaders/` (99 files there in all); `tuffysdf.fgen.phyre` ships under `font/` |
| `jsondata/*.json` | 830 files: `maps` 459, `cutscenes` 337, `fontcluts` 28, `uisize` 2, root 4 |
| `jsondata/init.json` | 176 keys |
| map documents | 459, 176 distinct keys |
| empty documents | 26 zero-byte files, all `sum_` cutscenes; 29 more hold only `{}`: 28 cutscenes such as `byu_z9900` and the root `0.json` |
| documents strict JSON rejects | `maps/bhm0201` (line 44) and `cutscenes/evt_t0005` (line 227) miss a comma between two members; `uisize/uisize` (line 232) and `uisize/uisize_sd` (line 165) end an object with a trailing comma |
| authored names, sections set aside | 218: 175 read, 43 never read |
| key names the executable looks up | 929 rows in [`render-parameters-and-shader-assets-keys.tsv`](render-parameters-and-shader-assets-keys.tsv): 446 literal (3 of them also composed), 486 composed |

### Columns of render-parameters-and-shader-assets-keys.tsv

| Column | Holds |
|---|---|
| `key` | the key name; the rows are sorted by it in character-code order |
| `form` | `literal` (443 rows), `composed` (483) or `literal and composed` (3); the 446 literal keys are the rows whose form starts with `literal` |
| `template` | the format a composed name is made from: `mCascadePartition%d_%d`, `Cut %d`, `PresetDof %d` or `MonsterId%d`; empty on the 443 `literal` rows |
| `lookups` | the lookups the sites call or jump to, of `0x001FF740`, `0x001FF6B0`, `0x001C51D0`, `0x001C52C0`, `0x001C5530` and `0x001C5570`, separated by `, ` |
| `readers` | the start of each function that holds a site, separated by `, `; a chained fragment counts under its root function |
| `sites` | the number of sites |
| `site_addresses` | the call or jmp instruction of each site, separated by `, ` |
| `in_shipped_document` | `yes` when at least one of the 830 `jsondata` documents holds the name as a key, `no` otherwise |
| `shipped_documents` | how many of the 830 documents hold the name |

## Modding notes

- A map's look is changed in its `jsondata/maps/<map>.json`; a key the map omits usually comes from
  `init.json`. The light directions apply only when the map's file has both `lightOrientation` and
  `lightHeight`.
- Editing a `…CheckBoxCheckState` or `…Lock` key, `mCascadeNumber`, or the alpha `mMapAmbientColorA`
  changes nothing.
- Shadow cascade splits are the nine keys `mCascadePartition<column>_<row>`, columns 0 to 2 and rows
  1 to 3.
- The twelve post-process assets are replaced as files under `gamedata/d3d11/artdata/shaders/`; the
  pass skips any constant a replacement drops.

## Related

- [Graphics settings](../Engine-Core/graphics-settings.md): the loaders and where each key
  is stored.
- [Post-processing](post-processing.md): the passes that use these shaders and values.
- [Phyre asset files](../PhyreEngine/phyre-asset-files.md): the `.phyre` container.
- [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md): the JSON
  documents as files.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Developer** (explained on [json configs](../Game-Files-And-Data-Tables/json-configs.md))

| Function | | Functions |
|---|---|---|
| `0x00200BE0` | is called by | `0x001C6320` |

</details>
