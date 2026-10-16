---
title: "Graphics settings: the render settings block, its scene-config keys, its defaults and the shader constants it feeds"
kind: "system"
category: "Engine core"
addresses: "02CB7FD0, 00162410, 005DC720, 005DC580, 005DC430, 008AB7C0, 001C7940, 001C3D50, 001FF740, 001C51D0, 00200B50, 00200B80, 00200BE0, 001F0AD0, 001EF6D0, 00187950, 006084B0, 005DEC50, 00604750, 001D1660, 001CD0E0, 001846B0, 001846F0, 00193F70, 00194300, 00194250, 00194290, 001A9930, 0018EEE0, 00193D50, 001C5750, 001A9AA0, 001A9A70, 001A9AD0, 001A7770, 001A9ED0, 001802E0, 001A9DA0, 001A9D70, 001A9B30, 001A7E40, 001A97F0, 005DDDB0, 00214C30, 00214B90, 001CC800, 001CC920, 001F38B0, 01FD3AE6"
---

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
The destructor loads the block's address and jumps to `005DDDB0`, which frees the callback
vector at `+0x1010` (below) and the arrays at `+0x4A0` and `+0x478`.

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

`mEarlyWaterDraw` lands as `value == 1` (the loader's own `cmp` and `sete`) in the dword `01F7F504` (`00182FE0`, called at
`001C9146`); its getter `0017FE20` is read by the frame-capture routine `0022B0B0`.

### The map-art context's keys

Several area keys land in the map-art context `[01F81168]` (getter `001A9930`) through its own
setters. The three `m2dBgNpcAnimRotation` keys, authored in degrees, are converted with
`v / 180 × π`: `…Speed` by `001A9AA0` to `+0x480`, `…Limit` by `001A9A70` to `+0x484`,
`…SpeedMargin` by `001A9AD0` to `+0x488`. A setter that changes its field calls `001A7770`, which
resets every entry of the map at `+0x498`: angle `+0x30` = 0, limit `+0x28` = `+0x484`, speed
`+0x24` = `+0x480` plus a `rand()` offset inside ±`+0x488`.

The map-art update `001A9ED0` then moves each angle by speed × frame time and reverses the speed
when the angle reaches the limit on either side, but only while both `+0x480` and `+0x484` are
non-zero. The draw-list build `002F5550` reads a model's angle through `001802E0` (`001A7410`:
the entry with that model's index, 0 without one) and multiplies the model's placement by a
rotation of that angle (`00202F00`). The 2D background figures therefore sway back and forth,
each at its own speed.

The three per-slot shadow sets are stored by slot index and applied for the current slot:

- `mShadowValueLerpMinForMap`, `…Map2`, `…Map3` go through `001A9DA0(ctx, i, v)` to `+0x338 + i × 4`,
  and the three `…ForChr` keys through `001A9D70` to `+0x344 + i × 4`;
- `lightHeight` and `lightOrientation` 1 to 3, read only when the area's own file has both, become
  a direction (`001C4F50`, the two angles in degrees) that `001C78D0` hands to `001A9B30(ctx, i, x, y, z)`
  at `+0x374 + i × 0xC`, setting the byte `+0x398`; without them the loader clears `+0x398`;
- the cascade rows of `mCascadePartition%d_%d` sit at `+0x350 + i × 0xC`.

After each of these the setter (or `001AA3B0` after the cascade loop and after each light)
calls `001A7E40(ctx, slot - 1)`, slot being `00265920()`: the developer menu's weather-slot override
`0017D490` when positive, else the area's slot byte `+0x1060` plus 1. `001A7E40` copies that
slot's map and character values to the shadow object's `+0x140` and `+0x144`, its cascade row to
`+0x870` to `+0x878`, and, while `+0x398` is set, its direction through `001F08A0` to the shadow
object's `+0xFC` to `+0x104` (normalised) and the block's `+0x450` to `+0x458`.

The map-art constructor `001A2130` registers `001A97F0` as a callback of the block (`0060B720`
appends it to the vector at `+0x1010`). The callback writes `mapIrrCubeMapFactor` (`+0x0B8`) =
the context's `+0x2DC` while `EnableIBL` (`+0x2E4`) is set and `001AC720(001AD440(), 0)` returns
an object, else 0. It writes `rtWidth` / `rtHeight` (`+0x0C0` / `+0x0C4`) from the render
manager's target (`001867B0`, its `+0x28` and `+0x2C` as floats), and `m_mapFadeHeight` (`+0x448`)
= the context's `+0x32C` while `+0x328` is set, else 1.0.

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

The two use generic matrix helpers: `001854C0` (the product of two affine 4 × 4 matrices, used by
`006084B0`), `00185AF0` (the inverse of an affine matrix through `001871B0`, with `+0x0C`, `+0x1C`
and `+0x2C` set to 0 and `+0x3C` to 1, used by `00604750`) and `00187460` (the same inverse, copied
out).

### The tonemap byte

`001C7940` reads `mUseLinearTonemap` as an integer and stores `value == 1` at `+0x4A2` of the
post-process parameter object (`01F7F5F0`). The post-process frame build `0018EEE0` copies that
byte to `+0x9A` of the frame parameters it hands to `005FEA50`, along with the DOF values from
`+0x110`, the byte `+0xEE` as a float at `+0x94` (the loader's `mGammaValue` at `+0xF0` is not
forwarded) and the colour-correction block at `+0xC4`.

### Scripted depth of field

Event scripts set depth of field through two request slots (0 and 1) that `00214C30` applies:

| Call | Handler | Request |
|---|---|---|
| `0x5C1` | `003513F0` → `00214B80` → `00214B90(kind, focus, aperture, slot)` | a full request; kind 0 replaces focus and aperture with `mDofFocusDistance` and `mDofApertureFnumber` from the map's file `01F81328` (`001C5530`, falling back to `01F813C8`); the enable word becomes 1 |
| `0x5BA` | `0034D870` → `00214B40(enable)` | an enable-only request for slot 0 |
| `0x5C0` | `0034DAF0` → `00214B50(enable, slot)` | an enable-only request for the given slot |

Three more calls read the cutscene's presets. Each first marks the event slot of the calling
script's record (`+0x28` of `002640C0()`) in `01DFE40C`, or -1 for a slot above 4:

| Call | Handler | What it does |
|---|---|---|
| `0x5AE` | `003526F0` → `001EC520(slot, n)` | pushes `mDofFocusDistance` of section `PresetDof n` |
| `0x5AF` | `00352B30` → `001EC540(slot, n)` | pushes `mDofApertureFnumber` of section `PresetDof n` |
| `0x59F` | `0034C7E0` → `001EC620(slot, n, 00358320())` | posts a `ReadPresetDofForCutSceneObj` (`0018C200`, `001F1CB0`) whose execute `001F3500` runs `001C6E20(n, value)` |

`001C5570(n, key)` reads the preset: it builds `"PresetDof "` plus n and looks the key up in that
section of `Common` in scene map 0 (`01F813A8`) for n = 0, else scene map 1 (`01F813D8`), at index
`01F813F8`, or at `01DF6E4C` while `01F81415` is set. `001C5530(map, key)`, used by `0x5C1` with kind
0, looks a key up in the map unless its type is 6 (absent), in which case it looks in `01F813C8`.

Neither `00214B50` nor `00214B90` bounds the slot. `00214B70`, called at the end of `00378BC0`, raises the map-reload
byte, and `00214B30` (from `001EC4B0`) the scene-reset byte.

`00214C30(i)` runs with i = 0 from the main state machine (`0022A5C8`) and with i = 1 from the
capture routine `0022B0B0` (`0022B127`). It refuses an i above 1 (`__report_rangecheckfailure`).
For a pending request of slot i it posts a command on the ordered command list `[01F7F5E8]`
([render command list](../Graphics/render-command-list.md)):

- an enable-only request: `001CC920(enable, i)`, then `0018BC90`, which posts an `EnableDofObj`
  (`001F1940`) whose execute `001F2F50` calls `00194240(post-process object, enable)`;
- a full request: `001CC800(enable, focus, aperture, i)`, then `0018CA50`, which posts a `SetDofObj`
  (`001F1DF0`) whose execute `001F38B0` calls `00194250` with the enable, focus and aperture, the
  object's current `+0x11C` and 35.0.

`001CC920` and `001CC800` also write the values into the running cutscene's data, but only for
slot 0 and only while an event slot is marked with queued events (`01DFE40C` below 5, its count at
`01F832B0` non-zero). They look up the section named by the cut name `01F81358` ("Cut N") in the
current scene map `01F813A8 + [01F813F8] × 0x10` (`001FF6B0`) and set `EnableDof` (`00202820`),
`mDofFocusDistance` and `mDofApertureFnumber` (`002027B0`).

### The crossfade hold

The crossfade that script call `crossfade` (`0x016F`, `00353260`) opens through `002F1A90` lives at
`022BE7C8` until `002F1950` clears it. `001CC600` keeps `01F81280` = that task exists and
`0022A550()` holds, with the previous value in `01F81281`. `00214C30(0)` treats its edges:

1. on the rising edge (`001C53B0`) it saves the live depth of field (`0018D5F0`: the post-process
   object's `+0x110` to `+0x120`) into both saved copies and sets the hold byte `01FD3AE6`;
2. on the falling edge (`001C53D0`) it clears the hold byte;
3. while the hold byte is set and `001EC560()` is 0 (no marked event slot with queued events, or
   `00265680()` non-zero), pending requests of both slots go into the saved copies (and, for
   slot 0, the cut data) instead of the live state, and every call re-posts a `SetDofObj` from saved copy i.

`00214C30` then serves the two bytes: the map-reload byte runs the map document reader `001C61F0`,
and the scene-reset byte runs `001C7290` (when `01F81288` differs from `01F81290`) and `001C5040`.

| Address | Type | Name | Meaning |
|---|---|---|---|
| `01FD3AC8` | `i32` | kind | request kind of slot 0; slot 1 at `01FD3AD4` |
| `01FD3ACC` | `f32` | focus | requested focus distance of slot 0; slot 1 at `01FD3AD8` |
| `01FD3AD0` | `f32` | aperture | requested aperture of slot 0; slot 1 at `01FD3ADC` |
| `01FD3AE0` | `u8[2]` | fullPending | a full request waits, per slot |
| `01FD3AE2` | `u8` | mapReload | run `001C61F0` on the next call |
| `01FD3AE3` | `u8` | sceneReset | run `001C5040` on the next call |
| `01FD3AE4` | `u8[2]` | enablePending | an enable-only request waits, per slot |
| `01FD3AE6` | `u8` | hold | a crossfade holds the depth of field |
| `01FD3AE8` | `i32[2]` | enable | requested enable, per slot |
| `01FD3AF0` | `DofCopy[2]` | saved | the held values, stride `0x14` |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | enable | from post-process `+0x110` |
| `04` | `f32` | focus | from `+0x114` |
| `08` | `f32` | aperture | from `+0x118` |
| `0C` | `f32` | value3 | from `+0x11C` |
| `10` | `f32` | value4 | from `+0x120` |

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

The map-art context at `[01F81168]`, the fields its setters write:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `338` | `f32[3]` | lerpMinMap | `mShadowValueLerpMinForMap`, `…2`, `…3` |
| `344` | `f32[3]` | lerpMinChr | `mShadowValueLerpMinForChr`, `…2`, `…3` |
| `350` | `f32[9]` | cascadeRows | three rows of `mCascadePartition%d_%d` |
| `374` | `f32[9]` | lightDirs | three light directions |
| `398` | `u8` | lightDirSet | the directions apply |
| `480` | `f32` | swaySpeed | radians per second |
| `484` | `f32` | swayLimit | radians |
| `488` | `f32` | swayMargin | radians |
| `498` | `SwayMap` | sway | one entry per model: speed `24`, limit `28`, angle `30` |

The block's `+0x1010` is the vector of callbacks `0060B720` appends to, `001A97F0` among them.


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
- Depth of field has three authors writing the same `+0x110` to `+0x120`: the area's config
  through the loaders, event scripts through the request slots (above), and `JsonData/CutScenes/<name>.json` through `001C5750`, whose one caller
  is the event-slot setter `0020AC30` (from the area load `0032FCA0`), and only for a slot whose
  path contains `sum_`, the summon scenes.

## Related

- [Debug menu](debug-menu.md): the rows that step the block.
- [Debug menu commands](debug-menu-commands.md): which row steps which field.
