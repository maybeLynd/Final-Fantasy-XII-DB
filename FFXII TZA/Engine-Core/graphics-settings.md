---
title: "Graphics settings: the render settings block, its scene-config keys, its defaults and the shader constants it feeds"
kind: "system"
category: "Engine core"
summary: "The static block at 02CB7FD0 that holds the remaster's render settings: the two constructors that write its defaults, the two scene-config loaders that overwrite thirty of them from named keys, the eight shadow-map matrices and the derived shadow scalars written into it every frame, the snapshot the frame builder compares against the last one before it rewrites the shader constant buffer, the post-process and shadow objects the other keys land in, the second run of character-light settings outside the block, the developer-menu rows that step the fields, and the tonemap byte the scene config switches."
addresses: ["02CB7FD0", "00162410", "005DC720", "005DC580", "005DC430", "008AB7C0", "001C7940", "001C3D50", "001FF740", "001C51D0", "00200B50", "00200B80", "00200BE0", "001F0AD0", "001EF6D0", "00187950", "006084B0", "005DEC50", "00604750", "001D1660", "001CD0E0", "001846B0", "001846F0", "00193F70", "00194300", "00194250", "00194290", "001A9930", "0018EEE0", "00193D50", "001C5750"]
---

# Graphics settings: the render settings block, its scene-config keys, its defaults and the shader constants it feeds

## What the player sees

The remaster draws things the PlayStation 2 original could not: depth of field that blurs the
background, ambient occlusion in corners, image-based lighting on skin and metal, cascaded
shadows, water with reflection and refraction, and a post-processing pass over the whole frame.
None of those have a slider in the options menu. Their strengths were chosen by the developers
with a controller in hand and shipped as numbers: each area's scene configuration sets some of
them, a summon scene's own file can override the depth of field, and the rest stay at the
values compiled into the game.

## How it works

### The block and its defaults

The settings live in one C++ static object at `02CB7FD0`. Its initializer `00162410` runs the
constructor `005DC720` on it and registers the destructor `008AB7C0` with `atexit`. The
constructor writes the object out to `+0x1020`: `005DC580` fills `+0x000` to `+0x0C7`,
`005DC430` fills `+0x0D0` to `+0x187`, the constructor itself fills `+0x42C` to `+0x4A8`.

The constructor then runs the first two again on the block images inside the two snapshot slots at `+0x4E0` and
`+0xA78` (a slot is `0x598` bytes and carries the block image at its `+0x110`, so the copies sit
at `+0x5F0` and `+0xB88`), so that the first frame's comparison has something to compare against.
The defaults are immediates in those three bodies; the table
[graphics-settings.tsv](graphics-settings.tsv) carries every one.

The first `0x190` bytes are the tunables the developer menu steps ([debug menu](debug-menu.md)):
`001D1660`'s arms touch 86 addresses in the block, 84 of them below `+0x190`, with `addss` and
`subss` on a float each. The console's row renderer `001CD0E0` reads them back to print the
current value beside the label.

### The scene-config loaders

`001C7940` (an area's scene config) and `001C3D50` (a cutscene's) read settings out of a
string-keyed map. `001FF740(map, "key")` finds the entry, `00200BE0` tests its type tag for 6
("absent"), `00200B50` reads it as a float (tag 2 `cvtpd2ps`, tag 1 `cvtdq2ps`, else 0) or
`00200B80` as an integer, and the value is stored.

The area loader inlines a two-level lookup:
the given map, then the global defaults at `01F813C8` when the tag is 6. The cutscene loader
calls `001C51D0(map, "key")` (its only caller), a three-level chain: the given map, then the
`Common` section of the current scene map (`01F813D8 + 01F813F8 × 0x10` when `01F81418` is set,
else `01DF6E50`'s), then `01F81328`, then `01F813C8`.

Thirty keys land in the block, twenty-nine through the float reader and `mMapEnableShadowFade`
as `value == 1` at `+0x42C` through the integer reader (`001C8F2B`); `mMapShadowFadeRange` at
`+0x43C` is raised to 0.9 when the file gives less (`001C8FAB`):

- the four `chrFresnelSpecular*` at `+0x0D0` to `+0x0DC`;
- `mMapAmbientColorR/G/B` at `+0x0A0` to `+0x0A8`, `mMapAmbientColorCutPercent` at `+0x0B0` and
  `mMapIrrCubemapIntensity` at `+0x09C`;
- `mDebugRefractionFactor` and the seven `mDebugWater*` at `+0x074` to `+0x090`, `mWaterBias` at
  `+0x098`;
- the eye modifiers `mEyeMap*` at `+0x028`, `mEyeAB*` at `+0x104`, `+0x108` and `+0x114`,
  `mEyeA*` at `+0x134` and `mEyeB*` at `+0x158`;
- `mCubemapIntensity` at `+0x168` (`001846F0` parks it in `01F7F53C` and zeroes it, `001846B0`
  restores it, around the work those two bracket) and the four `mMapShadow*Fade*` at `+0x438`
  to `+0x444`.

The same loaders write everything else somewhere other than the block, among others:

- into the post-process parameter object (`0x4A8` bytes, allocated on first use by `00193D50`
  into `01F7F5F0`, and cached again at `01F81300` by the static initializer `0015CAF0`):
  `EnableAO` at `+0x198`, `mGammaValue` at `+0xF0` (`00194300`), the unsharp mask, the glare,
  the colour correction, `EnableYebis` (`00194290`, the post-processing layer's switch at
  `+0xA0`, `+0xA1`, `+0x1F0`) and the motion blur at `+0x334` to `+0x33C`;
- into the same object, the depth of field: `EnableDof`, `mDofApertureFnumber` and
  `mDofFocusDistance` at `+0x110` to `+0x120` through `00194250`; a cutscene with a `PresetDof`
  entry reads the pair from its `Common` section instead;
- into the shadow object (`0xB08` bytes, constructor `001EF2D0`, allocated on first use by
  `001F0850` into `01F82EA8` and cached again at `01F812C8` by `0015CC00`): `ShadowBias` at
  `+0x898`, `ShadowValueR/G/B` at `+0xEC` to `+0xF4`, `mCascadePartition*` at `+0x870`,
  `m_iPCFBlurSize*` at `+0x890` and `+0x894`, `EnableShadow` at `+0`;
- the cutscene loader also sends `mShadowValueLerpMin*` to the shadow object's `+0x140` and
  `+0x144`, where the area loader sends them to `[01F81168]`;
- into `[01F81168]`: `EnableIBL` at `+0x2E4` (and the byte `01DFE190`), the water tiling and
  sampling at `+0x2E8` to `+0x308`, `EnableMapNormalMap` at `+0x3D9`;
- the area loader also reads `lightShaft*`, `lightHeight` and `lightOrientation` 1 to 3,
  `mMapLightColor` R/G/B, `mMapFarPlane`, `m2dBgNpc*`, `mShadowVertexBlend*`, `mShadowAngle*`,
  `mMapObjectShadowFade*`, `mMapShadowDepthBias`, `mMapShadowSlopeOffset`, `earlyAO`,
  `mEarlyWaterDraw` and `mUseSubCameraForShadow`, each into its own subsystem object;
- the second run of thirteen character-light settings: `mMapChrAmbientIntensity` R/G/B at
  `01F82ED8`, `mMapChrAmbientOffset` R/G/B at `01F82EE8`, `mMapChrDirLightColorIntensity` R/G/B at
  `01F82EF8`, `mChrShadowSlopeOffset` at `01F82EF4`, `mChrShadowDepthBias` at `01F82F08`, and
  `mMapChrUpwardDirLight*` at `01DFE198` / `01DFE19C`.

### The shadow matrices

`+0x190` to `+0x38F` is an array of eight 64-byte matrices and `+0x390` to `+0x434` the shadow
scalars beside them. `001F0AD0` is called once per frame by the render pass list `00187950`
inside its `"update shadowmap"` scope, from one of two sites (`00187D56`, `00187D64`) that pass
the camera block at `+0x690` or `+0x358` of the `00189120` object, chosen by that object's byte
`+0xDC5` (the sub-camera-for-shadow switch, cleared after use at `00187D69`).

It copies the matrices out of the shadow object at `[01F82EA8]`: entry n of the block from
`object + 0x1C0 + n × 0xD8`, after `001EF6D0` has retargeted each of the object's eight slot
cameras (`+0x148 + n × 0xD8`, vtable at `+0`, matrix at `+0x78`). `001EF6D0` also writes the
last slot's far plane to `+0x460` (`001F045C`).

The shadow scalars are written in the same pass. `+0x390` to `+0x3AF` is a copy of object
`+0x850` to `+0x86F`; the rest is derived, with h = the map size at object `+0x848`:

| block | value |
|---|---|
| `+0x3B0` to `+0x3B8` | object `+0xFC` to `+0x104` |
| `+0x3D0` to `+0x3D8` | object `+0xEC` to `+0xF4` (`ShadowValue`) |
| `+0x3E4` | the slot count `+0x13C` |
| `+0x3E8`, `+0x3FC` | 1/h |
| `+0x3EC` | (h - 1)/h |
| `+0x3F0`, `+0x414` | object `+0x8A4`, `+0x8A0` |
| `+0x3F4` | object `+0x898` (`ShadowBias`) |
| `+0x3F8` | 1/3 |
| `+0x400` | 1/(3h) |
| `+0x404`, `+0x408` | object `+0x830`, `+0x82C` |
| `+0x40C` | object `+0x138` |
| `+0x410` | object `+0x8B8` != 0 |
| `+0x41C`, `+0x420` | -n/2 and n/2 + 1 for n = the PCF size `+0x890` capped at 7 |
| `+0x424`, `+0x428` | the same of `+0x894` |
| `+0x430`, `+0x434` | object `+0x140`, `+0x144` |

`001F0AD0` also services the map resize request at object `+0xAFE` (`001EE040` with `02CF7480` /
`02CF79C0`) and ends in `001F06D0` when the enable byte `+0` is set. No developer-menu arm touches
this range.

### From the block to the shaders

`006084B0` builds a `0x598`-byte snapshot for the frame: the block's `+0x000` to `+0x18F` sixteen
bytes at a time into snapshot `+0x110`, `+0x190` to `+0x44F` in one `005DEC50` copy into snapshot
`+0x2A0`, and `+0x450` to `+0x470` field by field.

`00604750` builds that snapshot on its stack (the defaults of `005DC580` and `005DC430` first,
then `006084B0` over them), takes the lock at `+0x4B0` (`005CD4F0` / `005CD820`), and compares
the `0x598` bytes against the slot `idx & 1` at `+0x4E0` with `idx` = `+0x4D8`. When they are
equal it returns the previous ring entry and writes nothing. When they differ it advances `idx`
modulo `+0x498`, copies the snapshot into that slot (`005DF3E0`), waits on the ring entry's busy
word (a `Sleep(1)` loop) and rewrites the constant buffer.

The write fills the shipped shaders' `SceneWideParameterConstantBuffer` from the snapshot, field
by field and reordered in places, so every block field below `+0x190`
is one HLSL variable: `mapFresnelRefEnabled` at `+0x000`, `vMapAmbientColor` at `+0x0A0`,
`chrDiffuseIntensity` at `+0x160`, `chrCubemapIntensity` at `+0x168` and so on. The table gives
the constant-buffer offset and variable for all 276 fields the map reaches.

### The tonemap byte

`001C7940` reads `mUseLinearTonemap` as an integer and stores `value == 1` at `+0x4A2` of the
post-process parameter object (`01F7F5F0`). The post-process frame build `0018EEE0` copies that
byte to `+0x9A` of the frame parameters it hands to `005FEA50`, along with the DOF values from
`+0x110`, the byte `+0xEE` as a float at `+0x94` (the loader's `mGammaValue` at `+0xF0` is not
forwarded) and the colour-correction block at `+0xC4`.

## Layouts

```
02CB7FD0  the render settings object, 0x1028 bytes (constructor 005DC720)
  +0x000..+0x18F  console-tunable floats, one shader constant each (graphics-settings.tsv)
  +0x190..+0x38F  8 x 64-byte shadow-map matrices (001F0AD0, per frame)
  +0x390..+0x434  shadow scalars (001F0AD0, per frame); +0x3E4 the live slot count
  +0x42C          u8 mMapEnableShadowFade; +0x438..+0x444 mMapShadowFadeSpeed, FadeRange, FlyingFadeSpeed, FlyingFadeRange
  +0x450..+0x470  copied field by field into the snapshot; +0x460 the last slot's far plane (001EF6D0, per frame)
  +0x478/+0x480   constant-buffer binding list (0x18-byte entries, kind byte at +2, 23 kinds); +0x488 stride
  +0x498          ring length; +0x4B0 lock; +0x4D8 slot index
  +0x4E0, +0xA78  two 0x598-byte snapshot slots; block image at slot +0x110 (= +0x5F0, +0xB88)
01F7F5F0 = 01F81300  post-process parameter object (0x4A8): +0xA0/+0xA1/+0x1F0 EnableYebis, +0xF0 mGammaValue, +0x110..+0x120 DOF, +0x17C contrast, +0x198 EnableAO, +0x1C0 SAO fade, +0x1DC HBAO fade, +0x1E9 AODepthFullRes, +0x334..+0x33C motion blur, +0x4A2 u8 linear tonemap
01F82EA8 = 01F812C8  shadow object (0xB08, ctor 001EF2D0): +0x000 EnableShadow, +0xEC..+0xF4 ShadowValue R/G/B, +0x13C slot count, +0x148 + n*0xD8 slot cameras, +0x1C0 + n*0xD8 matrices, +0x82C/+0x830 decay, +0x848 map size, +0x870.. cascade partitions, +0x890/+0x894 PCF sizes, +0x898 ShadowBias, +0xAFE/+0xB00/+0xB04 resize request
01F82ED8..01F82F08  the second settings run (character light); 01DFE190 EnableIBL byte
snapshot (006084B0): +0x110 <- block +0x000; +0x2A0 <- block +0x190 (704 bytes); then +0x450..+0x470
```

## Shipped data

| Fact | Value |
|---|---|
| block fields with a shader constant | 276, in [graphics-settings.tsv](graphics-settings.tsv) |
| fields with a scene-config key | 30 in the block (21 below `+0x190`), 13 in the second run |
| constructor defaults | 105 fields; `mMapAmbientColor` 1, 1, 1; `chrFresnelSpecularIntensity` 3.9; `mCubemapIntensity` 0.6; `mDebugWaterSpecFactor` 3.59; `+0x0C0` / `+0x0C4` 1920 and 1080 |
| shadow matrices | 8 of 64 bytes, block stride 64, object stride `0xD8` |
| developer-menu arms on the block | 86 addresses, 84 below `+0x190` |

## Operations

At boot: the constructor's defaults. At every area or cutscene load: the loader's keyed stores.
Every frame: `001F0AD0`'s matrix copy, `006084B0`'s snapshot, `00604750`'s comparison with the
last slot and, only when a byte differs, its constant-buffer write; `0018EEE0`'s frame
parameters. On a developer-menu press: one `addss` or `subss` on one field.

## State

The block with its two snapshot slots and ring index, the post-process parameter object
(`01F7F5F0`, also at `01F81300`), the shadow object (`01F82EA8`, also at `01F812C8`), the second
settings run and the frame's snapshot.

## Modding notes

- The defaults are immediates in `005DC580`, `005DC430` and `005DC720`; patching them changes the
  value every area starts from, and a scene config with the key overrides it on load.
- A field below `+0x190` is live: the next frame's snapshot carries whatever is written there,
  and the constant buffer is rewritten because the snapshot changed. A field in `+0x190` to
  `+0x434` is overwritten by `001F0AD0`, and `+0x460` by `001EF6D0`, before the frame uses it;
  `+0x42C` and `+0x438` to `+0x444` hold until the next area load.
- `EnableYebis` is the whole post-processing layer, not one effect; `EnableAO`, `EnableDof`,
  `EnableShadow` and `EnableIBL` each switch one.
- Depth of field has two authors writing the same `+0x110` to `+0x120`: the area's config
  through the loaders, and `JsonData/CutScenes/<name>.json` through `001C5750`, whose one caller
  is the event-slot setter `0020AC30` (from the area load `0032FCA0`), and only for a slot whose
  path contains `sum_`, the summon scenes.

## Related

- [Debug menu](debug-menu.md): the rows that step the block.
- [Debug menu commands](debug-menu-commands.md): which row steps which field.
