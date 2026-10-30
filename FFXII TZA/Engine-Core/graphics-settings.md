---
title: "Graphics settings: the render settings block, its scene-config keys, its defaults and the shader constants it feeds"
kind: "system"
category: "Engine core"
addresses: "0x02CB7FD0, 0x00162410, 0x005DC720, 0x005DC580, 0x005DC430, 0x008AB7C0, 0x001C7940, 0x001C3D50, 0x001FF740, 0x001C51D0, 0x00200B50, 0x00200B80, 0x00200BE0, 0x001F0AD0, 0x001EF6D0, 0x00187950, 0x006084B0, 0x005DEC50, 0x00604750, 0x001D1660, 0x001CD0E0, 0x001846B0, 0x001846F0, 0x00193F70, 0x00194300, 0x00194250, 0x00194290, 0x001A9930, 0x0018EEE0, 0x00193D50, 0x001C5750, 0x001A9AA0, 0x001A9A70, 0x001A9AD0, 0x001A7770, 0x001A9ED0, 0x001802E0, 0x001A9DA0, 0x001A9D70, 0x001A9B30, 0x001A7E40, 0x001A97F0, 0x005DDDB0, 0x00214C30, 0x00214B90, 0x001CC800, 0x001CC920, 0x001F38B0, 0x01FD3AE6"
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

The settings live in one C++ static object at `0x02CB7FD0`. Its initializer `0x00162410` runs the
constructor `0x005DC720` on it and registers the destructor `0x008AB7C0` with `atexit`. The
constructor writes the object out to `+0x1020`: `0x005DC580` fills `+0x000` to `+0x0C7`,
`0x005DC430` fills `+0x0D0` to `+0x187`, the constructor itself fills `+0x42C` to `+0x4A8`.
The destructor loads the block's address and jumps to `0x005DDDB0`, which frees the callback
vector at `+0x1010` (below) and the arrays at `+0x4A0` and `+0x478`.

The constructor then runs the first two again on the block images inside the two snapshot slots at `+0x4E0` and
`+0xA78` (a slot is `0x598` bytes and carries the block image at its `+0x110`, so the copies sit
at `+0x5F0` and `+0xB88`), so that the first frame's comparison has something to compare against.
The defaults are immediates in those three bodies; the table
[graphics-settings.tsv](graphics-settings.tsv) carries every one.

The first `0x190` bytes are the tunables the developer menu steps ([debug menu](debug-menu.md)):
`0x001D1660`'s arms touch 86 addresses in the block, 84 of them below `+0x190`, with `addss` and
`subss` on a float each. The console's row renderer `0x001CD0E0` reads them back to print the
current value beside the label.

### The scene-config loaders

`0x001C7940` (an area's scene config) and `0x001C3D50` (a cutscene's) read settings out of a
string-keyed map. `0x001FF740(map, "key")` finds the entry, `0x00200BE0` tests its type tag for 6
("absent"), `0x00200B50` reads it as a float (tag 2 `cvtpd2ps`, tag 1 `cvtdq2ps`, else 0) or
`0x00200B80` as an integer, and the value is stored. `0x00200BA0` reads it as a string: the string object at
`+8` for tag 0, otherwise `0x01F83130`, an empty string that the initialiser `0x0015D2F0` builds at start-up
on the shared byte `0x02EBA2E0` ([EASTL strings](../Third-Party-Libraries/eastl-strings-and-containers.md)).

The area loader inlines a two-level lookup:
the given map, then the global defaults at `0x01F813C8` when the tag is 6. The cutscene loader
calls `0x001C51D0(map, "key")` (its only caller), a three-level chain: the given map, then the
`Common` section of the current scene map (`0x01F813D8 + 0x01F813F8 × 0x10` when `0x01F81418` is set,
else `0x01DF6E50`'s), then `0x01F81328`, then `0x01F813C8`.

`0x001C3D50(mode)` keeps the mode in `0x01F81418` and picks the document whose cut section it reads.
- In mode 0 that is `0x01DF6E50`.
- In mode 1, the second-screen run, it is `0x01DF6E58`. The cut section comes from `0x001FF6B0(document, name)`
  (`0x001C3E9F`-`0x001C3EBB`).
- `0x001C3D50` sets `0x01DF6E58` on every call that gets past its first tests. Normally it holds the slot's `_2ndScreen`
  document, `0x01F813D8 + slot × 0x10` (`0x001C3E78`). In mode 1, while the crossfade byte `0x01F81280` is set and that
  document is absent (`0x00200BE0`), it holds the slot's main document `0x01F813A8 + slot × 0x10` instead (`0x001C3E5A`).
  When the document it picked is also absent, the call returns 0 (`0x001C3E84`-`0x001C3E8B`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01DF6E58` | `void*` | `0x01F813D8`, slot 0's second-screen document | the document a second-screen (mode 1) cutscene settings run reads its cut section from | `0x001C3D50` (`0x001C3E5A`, `0x001C3E78`) | `0x001C3D50` (`0x001C3E98`, in mode 1 only; in mode 0 `rcx` is replaced by `0x01DF6E50`'s value at `0x001C3EB8`) |

`0x001C52C0(map, section, key)` is the same chain for a
key inside a section, used three times by the cutscene loader (`0x001C4760`-`0x001C47BA`).
`0x001CC9A0(out, n)` makes the decimal string of n (`"%d"`, `0x008F6D3C`) that `0x001C5570` and `0x001CC600` append to
their key names.

Thirty keys land in the block, twenty-nine through the float reader and `mMapEnableShadowFade`
as `value == 1` at `+0x42C` through the integer reader (`0x001C8F2B`); `mMapShadowFadeRange` at
`+0x43C` is raised to 0.9 when the file gives less (`0x001C8FAB`):

- the four `chrFresnelSpecular*` at `+0x0D0` to `+0x0DC`;
- `mMapAmbientColorR/G/B` at `+0x0A0` to `+0x0A8`, `mMapAmbientColorCutPercent` at `+0x0B0` and
  `mMapIrrCubemapIntensity` at `+0x09C`;
- `mDebugRefractionFactor` and the seven `mDebugWater*` at `+0x074` to `+0x090`, `mWaterBias` at
  `+0x098`;
- the eye modifiers `mEyeMap*` at `+0x028`, `mEyeAB*` at `+0x104`, `+0x108` and `+0x114`,
  `mEyeA*` at `+0x134` and `mEyeB*` at `+0x158`;
- `mCubemapIntensity` at `+0x168` (`0x001846F0` parks it in `0x01F7F53C` and zeroes it, `0x001846B0`
  restores it, around the work those two bracket) and the four `mMapShadow*Fade*` at `+0x438`
  to `+0x444`.

The same loaders write everything else somewhere other than the block, among others:

- into the post-process parameter object (`0x4A8` bytes, allocated on first use by `0x00193D50`
  into `0x01F7F5F0`, and cached again at `0x01F81300` by the static initializer `0x0015CAF0`):
  `EnableAO` at `+0x198`, `mGammaValue` at `+0xF0` (`0x00194300`), the unsharp mask, the glare,
  the colour correction, `EnableYebis` (`0x00194290`, the post-processing layer's switch at
  `+0xA0`, `+0xA1`, `+0x1F0`) and the motion blur at `+0x334` to `+0x33C`;
- into the same object, the depth of field: `EnableDof`, `mDofApertureFnumber` and
  `mDofFocusDistance` at `+0x110` to `+0x120` through `0x00194250`; a cutscene with a `PresetDof`
  entry reads the pair from its `Common` section instead;
- into the shadow object (`0xB08` bytes, constructor `0x001EF2D0`, allocated on first use by
  `0x001F0850` into `0x01F82EA8` and cached again at `0x01F812C8` by `0x0015CC00`): `ShadowBias` at
  `+0x898`, `ShadowValueR/G/B` at `+0xEC` to `+0xF4`, `mCascadePartition*` at `+0x870`,
  `m_iPCFBlurSize*` at `+0x890` and `+0x894`, `EnableShadow` at `+0`;
- the cutscene loader also sends `mShadowValueLerpMin*` to the shadow object's `+0x140` and
  `+0x144`, where the area loader sends them to `[0x01F81168]`;
- into `[0x01F81168]`: `EnableIBL` at `+0x2E4` (and the byte `0x01DFE190`), the water tiling and
  sampling at `+0x2E8` to `+0x308`, `EnableMapNormalMap` at `+0x3D9`;
- the area loader also reads `lightShaft*`, `lightHeight` and `lightOrientation` 1 to 3,
  `mMapLightColor` R/G/B, `mMapFarPlane`, `m2dBgNpc*`, `mShadowVertexBlend*`, `mShadowAngle*`,
  `mMapObjectShadowFade*`, `mMapShadowDepthBias`, `mMapShadowSlopeOffset`, `earlyAO`,
  `mEarlyWaterDraw` and `mUseSubCameraForShadow`, each into its own subsystem object;
- the second run of thirteen character-light settings: `mMapChrAmbientIntensity` R/G/B at
  `0x01F82ED8`, `mMapChrAmbientOffset` R/G/B at `0x01F82EE8`, `mMapChrDirLightColorIntensity` R/G/B at
  `0x01F82EF8`, `mChrShadowSlopeOffset` at `0x01F82EF4`, `mChrShadowDepthBias` at `0x01F82F08`, and
  `mMapChrUpwardDirLight*` at `0x01DFE198` / `0x01DFE19C`.

`mEarlyWaterDraw` lands as `value == 1` (the loader's own `cmp` and `sete`) in the dword `0x01F7F504` (`0x00182FE0`, called at
`0x001C9146`); its getter `0x0017FE20` is read by the frame-capture routine `0x0022B0B0`.

### The map-art context's keys

Several area keys land in the map-art context `[0x01F81168]` (getter `0x001A9930`) through its own
setters. The three `m2dBgNpcAnimRotation` keys, authored in degrees, are converted with
`v / 180 × π`: `…Speed` by `0x001A9AA0` to `+0x480`, `…Limit` by `0x001A9A70` to `+0x484`,
`…SpeedMargin` by `0x001A9AD0` to `+0x488`. A setter that changes its field calls `0x001A7770`, which
resets every entry of the map at `+0x498`: angle `+0x30` = 0, limit `+0x28` = `+0x484`, speed
`+0x24` = `+0x480` plus a `rand()` offset inside ±`+0x488`.

The map-art update `0x001A9ED0` then moves each angle by speed × frame time and reverses the speed
when the angle reaches the limit on either side, but only while both `+0x480` and `+0x484` are
non-zero. The draw-list build `0x002F5550` reads a model's angle through `0x001802E0` (`0x001A7410`:
the entry with that model's index, 0 without one) and multiplies the model's placement by a
rotation of that angle (`0x00202F00`). The 2D background figures therefore sway back and forth,
each at its own speed.

The three per-slot shadow sets are stored by slot index and applied for the current slot:

- `mShadowValueLerpMinForMap`, `…Map2`, `…Map3` go through `0x001A9DA0(ctx, i, v)` to `+0x338 + i × 4`,
  and the three `…ForChr` keys through `0x001A9D70` to `+0x344 + i × 4`;
- `lightHeight` and `lightOrientation` 1 to 3, read only when the area's own file has both, become
  a direction (`0x001C4F50`, the two angles in degrees) that `0x001C78D0` hands to `0x001A9B30(ctx, i, x, y, z)`
  at `+0x374 + i × 0xC`, setting the byte `+0x398`; without them the loader clears `+0x398`;
- the cutscene loader's `0x001C7850(height, orientation)` makes the same direction and passes it, with y negated, straight to
  the shadow object (`0x001F0850`, `0x001F08A0`);
- the cascade rows of `mCascadePartition%d_%d` sit at `+0x350 + i × 0xC`.

After each of these the setter (or `0x001AA3B0` after the cascade loop and after each light)
calls `0x001A7E40(ctx, slot - 1)`, slot being `0x00265920()`: the developer menu's weather-slot override
`0x0017D490` when positive, else the area's slot byte `+0x1060` plus 1. `0x001A7E40` copies that
slot's map and character values to the shadow object's `+0x140` and `+0x144`, its cascade row to
`+0x870` to `+0x878`, and, while `+0x398` is set, its direction through `0x001F08A0` to the shadow
object's `+0xFC` to `+0x104` (normalised) and the block's `+0x450` to `+0x458`.

The map-art constructor `0x001A2130` registers `0x001A97F0` as a callback of the block (`0x0060B720`
appends it to the vector at `+0x1010`). The callback writes `mapIrrCubeMapFactor` (`+0x0B8`) =
the context's `+0x2DC` while `EnableIBL` (`+0x2E4`) is set and `0x001AC720(0x001AD440(), 0)` returns
an object, else 0. It writes `rtWidth` / `rtHeight` (`+0x0C0` / `+0x0C4`) from the render
manager's target (`0x001867B0`, its `+0x28` and `+0x2C` as floats), and `m_mapFadeHeight` (`+0x448`)
= the context's `+0x32C` while `+0x328` is set, else 1.0.

The character render-object manager's constructor `0x001BC9D0` registers `0x001BD9D0` the same way (`0x001BCC6C`). It
writes the block's `+0x184` (`0x02CB8154`): 0 while byte `+0x118` of `0x001EBA40()` is set, otherwise `0x01DFE194`
when `0x01DFE190` is set and that value is at least 0.001 in size, else 0.

Two more fields follow the light direction and the far plane. The byte `+0x464` (`0x02CB8434`) switches subsurface
scattering: its execute `0x001F3740` does nothing unless both it and `0x01DFE0C4` are set (`0x001F3749`, `0x001F3759`), and
the developer menu `0x001D1660` flips it (`0x001D298A`). The float `+0x468` (`0x02CB8438`) is a tunable that the developer
menu steps (`0x001D29AA`, `0x001D29BF`) and the console prints (`0x001CE8BD`); the snapshot copies both (`0x006089F2`,
`0x006089FF`).

### The shadow matrices

`+0x190` to `+0x38F` is an array of eight 64-byte matrices and `+0x390` to `+0x434` the shadow
scalars beside them. `0x001F0AD0` is called once per frame by the render pass list `0x00187950`
inside its `"update shadowmap"` scope, from one of two sites (`0x00187D56`, `0x00187D64`) that pass
the camera block at `+0x690` or `+0x358` of the `0x00189120` object, chosen by that object's byte
`+0xDC5` (the sub-camera-for-shadow switch, cleared after use at `0x00187D69`).

It copies the matrices out of the shadow object at `[0x01F82EA8]`: entry n of the block from
`object + 0x1C0 + n × 0xD8`, after `0x001EF6D0` has retargeted each of the object's eight slot
cameras (`+0x148 + n × 0xD8`, vtable at `+0`, matrix at `+0x78`). `0x001EF6D0` also writes the
last slot's far plane to `+0x460` (`0x001F045C`).

For a slot camera `0x001EF6D0` takes the eight corners of its view volume from `0x001EF560(out, fov, aspect, near,
far)`: four at the depth `-2 x near x far / (near + far)` and four at `-far`, each with y = ±depth / tan(pi/2 -
fov/2), x = ±y x aspect and w = 1. `0x001F0A00`, from `0x00169580`, `0x001EF280` and `0x006ACEE0`, builds an
orthographic matrix with `0x001F05B0(out, left, right, bottom, top, near, far)`: scales `2 / (right - left)`,
`2 / (top - bottom)` and `1 / (near - far)`, offsets `-(left + right) / (right - left)`, `-(top + bottom) /
(top - bottom)` and `near / (near - far)`.

At start-up the application set-up `0x00186CD0` gives the shadow object (`0x001F0850`) its map size through
`0x001F0570`: the Shadows setting's pair (`0x001DE5A0` on `[0x01F82D20]`) as its high half at `+0x844` and its low
half at `+0x848`.

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

`0x001F0AD0` also services the map resize request at object `+0xAFE` (`0x001EE040` with `0x02CF7480` /
`0x02CF79C0`) and ends in `0x001F06D0` when the enable byte `+0` is set. No developer-menu arm touches
this range.

### From the block to the shaders

`0x006084B0` builds a `0x598`-byte snapshot for the frame: the block's `+0x000` to `+0x18F` sixteen
bytes at a time into snapshot `+0x110`, `+0x190` to `+0x44F` in one `0x005DEC50` copy into snapshot
`+0x2A0`, and `+0x450` to `+0x470` field by field.

`0x00604750` builds that snapshot on its stack (the defaults of `0x005DC580` and `0x005DC430` first,
then `0x006084B0` over them), takes the lock at `+0x4B0` (`0x005CD4F0` / `0x005CD820`), and compares
the `0x598` bytes against the slot `idx & 1` at `+0x4E0` with `idx` = `+0x4D8`. When they are
equal it returns the previous ring entry and writes nothing. When they differ it sets
`idx = (idx + 1 == [+0x498]) ? 0 : idx + 1` (`0x006048E1`-`0x006048EE`), copies the snapshot into that slot (`0x005DF3E0`), waits on the ring entry's busy
word (a `Sleep(1)` loop) and rewrites the constant buffer.

The write fills the shipped shaders' `SceneWideParameterConstantBuffer` from the snapshot, field
by field and reordered in places, so every block field below `+0x190`
is one HLSL variable: `mapFresnelRefEnabled` at `+0x000`, `vMapAmbientColor` at `+0x0A0`,
`chrDiffuseIntensity` at `+0x160`, `chrCubemapIntensity` at `+0x168` and so on. The table gives
the constant-buffer offset and variable for all 276 fields the map reaches.

[The render settings inputs](graphics-settings-inputs.tsv) table gives each of the 276 fields as a setting: its
values and who writes them, which write lands last, when it takes effect, the shipped programs that read it, what
the player sees where this page states it, and when it changes nothing.

- 162 fields are rewritten every frame from the shadow object (`0x001F0AD0`), 30 by the scene-config loaders on each
  area or cutscene load, and 15 by other code; the other 69 keep the value the constructors or the zero-filled block
  give them; no instruction outside the developer menu names one of them in a store, and that menu, which the shipped game
  never opens, steps 65 of them.
- The reflection data of the shipped programs marks 272 of the fields as read. `m_iChrPCFBlurForLoopStart`,
  `m_iMapPCFBlurForLoopStart`, `mChrEnableHeightFade` and `sssFarPlane` are declared by all 228 program codes that
  carry `SceneWideParameterConstantBuffer`, and every one of them marks the four as unread.

The two use generic matrix helpers: `0x001854C0` (the product of two affine 4 × 4 matrices, used by
`0x006084B0`), `0x00185AF0` (the inverse of an affine matrix through `0x001871B0`, with `+0x0C`, `+0x1C`
and `+0x2C` set to 0 and `+0x3C` to 1, used by `0x00604750`) and `0x00187460` (the same inverse, copied
out).

### The tonemap byte

`0x001C7940` reads `mUseLinearTonemap` as an integer and stores `value == 1` at `+0x4A2` of the
post-process parameter object (`0x01F7F5F0`). The post-process frame build `0x0018EEE0` copies that
byte to `+0x9A` of the frame parameters it hands to `0x005FEA50`, along with the DOF values from
`+0x110`, the byte `+0xEE` as a float at `+0x94` (the loader's `mGammaValue` at `+0xF0` is not
forwarded) and the light-shaft values at `+0xC4` to `+0xE8`, which `0x001C7940` reads from the
`lightShaft*` keys and sets with `0x00194400` (`0x001C8AF5`; the alpha is not stored, `+0xD0` is set to 0).

### Scripted depth of field

Event scripts set depth of field through two request slots (0 and 1) that `0x00214C30` applies:

| Call | Handler | Request |
|---|---|---|
| `0x5C1` | `0x003513F0` → `0x00214B80` → `0x00214B90(kind, focus, aperture, slot)` | a full request; kind 0 replaces focus and aperture with `mDofFocusDistance` and `mDofApertureFnumber` from the map's file `0x01F81328` (`0x001C5530`, falling back to `0x01F813C8`); the enable word becomes 1 |
| `0x5BA` | `0x0034D870` → `0x00214B40(enable)` | an enable-only request for slot 0 |
| `0x5C0` | `0x0034DAF0` → `0x00214B50(enable, slot)` | an enable-only request for the given slot |

Three more calls read the cutscene's presets. Each first marks the event slot of the calling
script's record (`+0x28` of `0x002640C0()`) in `0x01DFE40C`, or -1 for a slot above 4:

| Call | Handler | What it does |
|---|---|---|
| `0x5AE` | `0x003526F0` → `0x001EC520(slot, n)` | pushes `mDofFocusDistance` of section `PresetDof n` |
| `0x5AF` | `0x00352B30` → `0x001EC540(slot, n)` | pushes `mDofApertureFnumber` of section `PresetDof n` |
| `0x59F` | `0x0034C7E0` → `0x001EC620(slot, n, 0x00358320())` | posts a `ReadPresetDofForCutSceneObj` (`0x0018C200`, `0x001F1CB0`) whose execute `0x001F3500` runs `0x001C6E20(n, value)` |

`0x001C5570(n, key)` reads the preset: it builds `"PresetDof "` plus n and looks the key up in that
section of `Common` in scene map 0 (`0x01F813A8`) for n = 0, else scene map 1 (`0x01F813D8`), at index
`0x01F813F8`, or at `0x01DF6E4C` while `0x01F81415` is set. `0x001C5530(map, key)`, used by `0x5C1` with kind
0, looks a key up in the map unless its type is 6 (absent), in which case it looks in `0x01F813C8`.

Neither `0x00214B50` nor `0x00214B90` bounds the slot. `0x00214B70`, called at the end of `0x00378BC0`, raises the map-reload
byte, and `0x00214B30` (from `0x001EC4B0`) the scene-reset byte.

`0x00214C30(i)` runs with i = 0 from the main state machine (`0x0022A5C8`) and with i = 1 from the
capture routine `0x0022B0B0` (`0x0022B127`). It refuses an i above 1 (`__report_rangecheckfailure`).
For a pending request of slot i it posts a command on the ordered command list `[0x01F7F5E8]`
([render command list](../Graphics/render-command-list.md)):

- an enable-only request: `0x001CC920(enable, i)`, then `0x0018BC90`, which posts an `EnableDofObj`
  (`0x001F1940`) whose execute `0x001F2F50` calls `0x00194240(post-process object, enable)`;
- a full request: `0x001CC800(enable, focus, aperture, i)`, then `0x0018CA50`, which posts a `SetDofObj`
  (`0x001F1DF0`) whose execute `0x001F38B0` calls `0x00194250` with the enable, focus and aperture, the
  object's current `+0x11C` and 35.0.

`0x001CC920` and `0x001CC800` also write the values into the running cutscene's data, but only for
slot 0 and only while an event slot is marked with queued events (`0x01DFE40C` below 5, its count at
`0x01F832B0` non-zero). They look up the section named by the cut name `0x01F81358` ("Cut N") in the
current scene map `0x01F813A8 + [0x01F813F8] × 0x10` (`0x001FF6B0`) and set `EnableDof` (`0x00202820`),
`mDofFocusDistance` and `mDofApertureFnumber` (`0x002027B0`).

### The crossfade hold

The crossfade that script call `crossfade` (`0x016F`, `0x00353260`) opens through `0x002F1A90` lives at
`0x022BE7C8` until `0x002F1950` clears it. `0x001CC600` keeps `0x01F81280` = that task exists and
`0x0022A550()` holds, with the previous value in `0x01F81281`. `0x00214C30(0)` treats its edges:

1. on the rising edge (`0x001C53B0`) it saves the live depth of field (`0x0018D5F0`: the post-process
   object's `+0x110` to `+0x120`) into both saved copies and sets the hold byte `0x01FD3AE6`;
2. on the falling edge (`0x001C53D0`) it clears the hold byte;
3. while the hold byte is set and `0x001EC560()` is 0 (no marked event slot with queued events, or
   `0x00265680()` non-zero), pending requests of both slots go into the saved copies (and, for
   slot 0, the cut data) instead of the live state, and every call re-posts a `SetDofObj` from saved copy i.

`0x00214C30` then serves the two bytes: the map-reload byte runs the map document reader `0x001C61F0`,
and the scene-reset byte runs `0x001C7290` (when `0x01F81288` differs from `0x01F81290`) and `0x001C5040`.

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01FD3AC8` | `i32` | kind | request kind of slot 0; slot 1 at `0x01FD3AD4` |
| `0x01FD3ACC` | `f32` | focus | requested focus distance of slot 0; slot 1 at `0x01FD3AD8` |
| `0x01FD3AD0` | `f32` | aperture | requested aperture of slot 0; slot 1 at `0x01FD3ADC` |
| `0x01FD3AE0` | `u8[2]` | fullPending | a full request waits, per slot |
| `0x01FD3AE2` | `u8` | mapReload | run `0x001C61F0` on the next call |
| `0x01FD3AE3` | `u8` | sceneReset | run `0x001C5040` on the next call |
| `0x01FD3AE4` | `u8[2]` | enablePending | an enable-only request waits, per slot |
| `0x01FD3AE6` | `u8` | hold | a crossfade holds the depth of field |
| `0x01FD3AE8` | `i32[2]` | enable | requested enable, per slot |
| `0x01FD3AF0` | `DofCopy[2]` | saved | the held values, stride `0x14` |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | enable | from post-process `+0x110` |
| `+0x04` | `f32` | focus | from `+0x114` |
| `+0x08` | `f32` | aperture | from `+0x118` |
| `+0x0C` | `f32` | value3 | from `+0x11C` |
| `+0x10` | `f32` | value4 | from `+0x120` |

Slot 0's saved copy is `0x01FD3AF0` (enable), `0x01FD3AF4` (focus), `0x01FD3AF8` (aperture), `0x01FD3AFC` and `0x01FD3B00`;
slot 1's is `0x01FD3B04`, `0x01FD3B08`, `0x01FD3B0C`, `0x01FD3B10` and `0x01FD3B14`. The crossfade's rising edge copies
`+0x110` to `+0x120` into both: `0x00214C75` and `0x00214C7F` for slot 0, `0x00214C88` and `0x00214C92` for slot 1. A held
request stores its enable with `setne` and its focus or aperture with `movss` (`0x00214D9E` and `0x00214D96` for slot 0,
`0x00214E01` and `0x00214DF9` for slot 1). Slot 1's pending bytes are `0x01FD3AE1` (full request) and `0x01FD3AE5`
(enable-only request).

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02CB7FD0` | `...` | the render settings object, 0x1028 bytes (constructor 0x005DC720) |  |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000-0x18F` | `...` | console-tunable floats, one shader constant each (graphics-settings.tsv) |  |
| `+0x190-0x38F` | `...` | 8 x 64-byte shadow-map matrices (0x001F0AD0, per frame) |  |
| `+0x390-0x434` | `...` | shadow scalars (0x001F0AD0, per frame); +0x3E4 the live slot count |  |
| `+0x42C` | `u8` | mMapEnableShadowFade |  |
| `+0x438-0x444` | `...` | mMapShadowFadeSpeed, FadeRange, FlyingFadeSpeed, FlyingFadeRange |  |
| `+0x450-0x470` | `...` | copied field by field into the snapshot; +0x460 the last slot's far plane (0x001EF6D0, per frame) |  |
| `+0x478` | `...` | constant-buffer binding list (0x18-byte entries, kind byte at +2, 23 kinds) | with `+0x480` |
| `+0x480` | `...` | constant-buffer binding list (0x18-byte entries, kind byte at +2, 23 kinds) | with `+0x478` |
| `+0x488` | `...` | stride |  |
| `+0x498` | `...` | ring length |  |
| `+0x4B0` | `...` | lock |  |
| `+0x4D8` | `...` | slot index |  |
| `+0x4E0` | `...` | two 0x598-byte snapshot slots; block image at slot +0x110 (= +0x5F0, +0xB88) | with `+0xA78` |
| `+0xA78` | `...` | two 0x598-byte snapshot slots; block image at slot +0x110 (= +0x5F0, +0xB88) | with `+0x4E0` |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01F7F5F0` | `void*` | post-process parameter object = 0x01F81300 (0x4A8 bytes) |  |
| `0x01F82EA8` | `void*` | shadow object = 0x01F812C8 (0xB08 bytes, ctor 0x001EF2D0) |  |

Post-process parameter object (`0x01F81300`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A0` | `...` | EnableYebis | with `+0xA1` and `+0x1F0` |
| `+0x0A1` | `...` | EnableYebis | with `+0xA0` and `+0x1F0` |
| `+0x1F0` | `...` | EnableYebis | with `+0xA0` and `+0xA1` |
| `+0x0F0` | `...` | mGammaValue |  |
| `+0x110-0x120` | `...` | DOF |  |
| `+0x17C` | `...` | contrast |  |
| `+0x198` | `...` | EnableAO |  |
| `+0x1C0` | `...` | SAO fade |  |
| `+0x1DC` | `...` | HBAO fade |  |
| `+0x1E9` | `...` | AODepthFullRes |  |
| `+0x334-0x33C` | `...` | motion blur |  |
| `+0x4A2` | `u8` | linear tonemap |  |

Shadow object (`0x01F812C8`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `...` | EnableShadow |  |
| `+0x0EC-0x0F4` | `...` | ShadowValue R/G/B |  |
| `+0x13C` | `...` | slot count |  |
| `+0x148` | `...` | slot cameras, + n*0xD8 |  |
| `+0x1C0` | `...` | matrices, + n*0xD8 |  |
| `+0x82C` | `...` | decay | with `+0x830` |
| `+0x830` | `...` | decay | with `+0x82C` |
| `+0x848` | `...` | map size |  |
| `+0x870` | `...` | cascade partitions, from here |  |
| `+0x890` | `...` | PCF sizes | with `+0x894` |
| `+0x894` | `...` | PCF sizes | with `+0x890` |
| `+0x898` | `...` | ShadowBias |  |
| `+0xAFE` | `...` | resize request | with `+0xB00` and `+0xB04` |
| `+0xB00` | `...` | resize request | with `+0xAFE` and `+0xB04` |
| `+0xB04` | `...` | resize request | with `+0xAFE` and `+0xB00` |

```
0x01F82ED8..0x01F82F08  the second settings run (character light); 0x01DFE190 EnableIBL byte
snapshot (0x006084B0): +0x110 <- block +0x000; +0x2A0 <- block +0x190 (704 bytes); then +0x450..+0x470
```

The map-art context at `[0x01F81168]`, the fields its setters write:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x338` | `f32[3]` | lerpMinMap | `mShadowValueLerpMinForMap`, `…2`, `…3` |
| `+0x344` | `f32[3]` | lerpMinChr | `mShadowValueLerpMinForChr`, `…2`, `…3` |
| `+0x350` | `f32[9]` | cascadeRows | three rows of `mCascadePartition%d_%d` |
| `+0x374` | `f32[9]` | lightDirs | three light directions |
| `+0x398` | `u8` | lightDirSet | the directions apply |
| `+0x480` | `f32` | swaySpeed | radians per second |
| `+0x484` | `f32` | swayLimit | radians |
| `+0x488` | `f32` | swayMargin | radians |
| `+0x498` | `SwayMap` | sway | one entry per model: speed `24`, limit `28`, angle `30` |

The block's `+0x1010` is the vector of callbacks `0x0060B720` appends to, `0x001A97F0` among them.


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
Every frame: `0x001F0AD0`'s matrix copy, `0x006084B0`'s snapshot, `0x00604750`'s comparison with the
last slot and, only when a byte differs, its constant-buffer write; `0x0018EEE0`'s frame
parameters. On a developer-menu press: one `addss` or `subss` on one field.

## State

The block with its two snapshot slots and ring index, the post-process parameter object
(`0x01F7F5F0`, also at `0x01F81300`), the shadow object (`0x01F82EA8`, also at `0x01F812C8`), the second
settings run and the frame's snapshot.

### The previous-cut name copy

`0x01F812E0` is a static EASTL string (`+0x00` begin, `+0x08` end, `+0x10` capacity end) that the initialiser
`0x0015C650` builds empty and the destructor `0x008A6A40` frees. `0x001C3C30` copies the previous cut name `0x01F81338` into
it through `0x001A5760` (`0x001C3C80`), and the cutscene scene-config reader `0x001C3D50` passes it, with the current cut
name `0x01F81358`, to the scene-map lookup `0x001FF6B0` (`0x001C3EA6`), which compares names in `0x001FF4F0`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F812E0` | `void*` | 0 (zero-filled tail of `.data`) | `+0x00` begin of the copy | `0x0015C650` (`0x0015C683`, `0x0015C6C2`, `0x0015C6F0`); `0x001A52A0` (`0x001A5386`) | `0x001A52A0` (`0x001A52BE`, `0x001A52C5`, `0x001A5312`, `0x001A5349`); `0x001A5760` (`0x001A577A`, `0x001A5782`, `0x001A579C`, `0x001A57D5`); `0x001FF4F0` (`0x001FF534`, `0x001FF5A2`, `0x001FF611`); `0x008A6A40` (`0x008A6A57`) |
| `0x01F812E8` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08` end of the copy | `0x0015C650` (`0x0015C683`, `0x0015C6C9`, `0x0015C6F7`, `0x0015C714`); `0x001A52A0` (`0x001A538E`, `0x001A53D3`); `0x001A5760` (`0x001A57BC`) | `0x001A52A0` (`0x001A52C0`, `0x001A5318`, `0x001A53A0`, `0x001A53B7`, `0x001A53C5`, `0x001A53D3`); `0x001A5760` (`0x001A5774`, `0x001A5798`, `0x001A57BC`, `0x001A57C2`, `0x001A57CF`); `0x001FF4F0` (`0x001FF530`, `0x001FF59E`, `0x001FF60D`) |
| `0x01F812F0` | `void*` | 0 (zero-filled tail of `.data`) | `+0x10` capacity end of the copy | `0x0015C650` (`0x0015C66E`, `0x0015C6D9`, `0x0015C6FE`); `0x001A52A0` (`0x001A537F`) | `0x001A52A0` (`0x001A52BB`, `0x001A534C`, `0x001A535E`); `0x008A6A40` (`0x008A6A4D`) |

The previous cut name is the same kind of string: `0x01F81338` its begin, `0x01F81340` its end and `0x01F81348` its
capacity end. The initialiser `0x0015CB10` builds it, storing the end at `0x0015CB89` or, for an empty name, `0x0015CBB7`,
and again after the copy (`0x0015CBD4`). `0x001C3C30` passes the end to the copy `0x001A5760` (`0x001C3C79`), and `0x001C7290`
empties the string: it loads the end (`0x001C72B1`), moves the terminator to the begin and sets the end back to the
begin (`0x001C72DC`).

`0x001C3C30(mode)` also keeps three words of its own, in the zero-filled tail of `.data`:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F813FC` | `i32` | 0 | the mode of the last cutscene settings run that `0x001C3D50` reported done; a call with the same mode and no swap pending returns at once (`0x001C3CE8`-`0x001C3CF2`) | `0x001C3C30` (`0x001C3D3E`) | `0x001C3C30` (`0x001C3CE8`, `0x001C3D33`) |
| `0x01F81410` | `i32` | 0 | the scene-map swaps still to make: a mode-0 call with the swap byte set takes one and flips the scene-map index `0x01F813F8` between 0 and 1 (`0x001C3CFC`-`0x001C3D20`) | `0x001C5930` (`0x001C5EB1` 2; `0x001C5ECB` 1, or 2 while `0x01F81414` is set); `0x001C6E20` (`0x001C71D0` 2; `0x001C71EA` the same 1 or 2); `0x001C7290` (`0x001C72EB` 0); `0x001C3C30` (`0x001C3D20`) | `0x001C3C30` (`0x001C3CFC`) |
| `0x01F81414` | `u8` | 0 | the swap byte: set by a mode-0 call that finds the countdown `0x01F81284` at 1, as it steps it to 0 (`0x001C3CB4`-`0x001C3CD9`); cleared when the last pending swap is taken (`0x001C3D26`) | `0x001C3C30` (`0x001C3CD9`, `0x001C3D26`); `0x001C7290` (`0x001C72F1` 0) | `0x001C3C30` (`0x001C3CC8`, `0x001C3CE1`); `0x001C5930` (`0x001C5EBD`); `0x001C6E20` (`0x001C71DC`) |

No other instruction reaches the string's words: no other RIP-relative, image-base-relative or disp32 reference names them,
and the string's address is taken only at `0x001C3C80` and `0x001C3EA6`.

## Modding notes

- The defaults are immediates in `0x005DC580`, `0x005DC430` and `0x005DC720`; patching them changes the
  value every area starts from, and a scene config with the key overrides it on load.
- A field below `+0x190` is live: the next frame's snapshot carries whatever is written there,
  and the constant buffer is rewritten because the snapshot changed. A field in `+0x190` to
  `+0x434` is overwritten by `0x001F0AD0`, and `+0x460` by `0x001EF6D0`, before the frame uses it;
  `+0x42C` and `+0x438` to `+0x444` hold until the next area load.
- `EnableYebis` is the whole post-processing layer, not one effect; `EnableAO`, `EnableDof`,
  `EnableShadow` and `EnableIBL` each switch one.
- Depth of field has three authors writing the same `+0x110` to `+0x120`: the area's config
  through the loaders, event scripts through the request slots (above), and `JsonData/CutScenes/<name>.json` through `0x001C5750`, whose one caller
  is the event-slot setter `0x0020AC30` (from the area load `0x0032FCA0`), and only for a slot whose
  path contains `sum_`, the summon scenes.

## Related

- [Debug menu](debug-menu.md): the rows that step the block.
- [Debug menu commands](debug-menu-commands.md): which row steps which field.
