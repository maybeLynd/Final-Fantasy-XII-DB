---
title: "Render parameters and shader assets: the post-process shader files and the scene-parameter documents"
kind: "system"
category: "Graphics"
addresses: "0x01DF0910, 0x0018D850, 0x0019CB20, 0x001FF740, 0x001FF6B0, 0x001C51D0, 0x001C3D50, 0x001C7940, 0x001CA600, 0x001C9190, 0x001A9B00, 0x001A9930, 0x008FB2D8"
---

## What the player sees

How each place and each cutscene looks after the geometry is drawn, its shadow softness, ambient
occlusion strength, glare, depth of field, water and eye shine, comes from per-map and per-cutscene
value files, read when the map or scene loads, and from a small set of post-process shader files.
Some values in those files are left over from the tool that wrote them and change nothing.

## How it works

### The shader assets

The executable names 18 `.phyre` assets for the post-process chain, text and video:

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
(and `0x001FF6B0` beneath it); the area loader `0x001C7940` falls back to the defaults when a map omits a
key, and the cutscene loader `0x001C3D50` goes through `0x001C51D0`.
[Graphics settings](../Engine-Core/graphics-settings.md) lists where each key lands.

312 distinct key strings are passed at the call sites of these lookups; the
three largest readers are `0x001C7940`, `0x001CA600` and `0x001C3D50`.

### The cascade keys are composed

`0x001C7940` never spells `mCascadePartition0_1` and its kin. At `0x001C9190` it formats
`"mCascadePartition%d_%d"` (`0x008FB2D8`) for columns 0 to 2 and rows 1 to 3, reads each value (with
the defaults as fallback) and stores it through `0x001A9B00(map-art context, row - 1, column, v)`.
`0x001A9B00` refuses an index of 3 or more and writes `+0x350 + (row x 3 + column) x 4` of the object
`0x001A9930` returns: a 3 x 3 float matrix. No code looks up `mCascadeNumber`, which the files also carry;
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

## Modding notes

- A map's look is changed in its `jsondata/maps/<map>.json`; a key the map omits comes from
  `init.json`.
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
