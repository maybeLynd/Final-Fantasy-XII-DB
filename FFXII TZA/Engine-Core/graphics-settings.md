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
constructor writes the object out to `+1020`<sub>h</sub>: `005DC580` fills `+000`<sub>h</sub> to `+0C7`<sub>h</sub>,
`005DC430` fills `+0D0`<sub>h</sub> to `+187`<sub>h</sub>, the constructor itself fills `+42C`<sub>h</sub> to `+4A8`<sub>h</sub>.
The destructor loads the block's address and jumps to `005DDDB0`, which frees the callback
vector at `+1010`<sub>h</sub> (below) and the arrays at `+4A0`<sub>h</sub> and `+478`<sub>h</sub>.

The constructor then runs the first two again on the block images inside the two snapshot slots at `+4E0`<sub>h</sub> and
`+A78`<sub>h</sub> (a slot is `598`<sub>h</sub> bytes and carries the block image at its `+110`<sub>h</sub>, so the copies sit
at `+5F0`<sub>h</sub> and `+B88`<sub>h</sub>), so that the first frame's comparison has something to compare against.
The defaults are immediates in those three bodies; the table
[graphics-settings.tsv](graphics-settings.tsv) carries every one.

The first `190`<sub>h</sub> bytes are the tunables the developer menu steps ([debug menu](debug-menu.md)):
`001D1660`'s arms touch 86 addresses in the block, 84 of them below `+190`<sub>h</sub>, with `addss` and
`subss` on a float each. The console's row renderer `001CD0E0` reads them back to print the
current value beside the label.

### The scene-config loaders

`001C7940` (an area's scene config) and `001C3D50` (a cutscene's) read settings out of a
string-keyed map. `001FF740(map, "key")` finds the entry, `00200BE0` tests its type tag for 6
("absent"), `00200B50` reads it as a float (tag 2 `cvtpd2ps`, tag 1 `cvtdq2ps`, else 0) or
`00200B80` as an integer, and the value is stored. `00200BA0` reads it as a string: the string object at
`+8` for tag 0, otherwise `01F83130`, an empty string that the initialiser `0015D2F0` builds at start-up
on the shared byte `02EBA2E0` ([EASTL strings](../Third-Party-Libraries/eastl-strings-and-containers.md)).

The area loader inlines a two-level lookup:
the given map, then the global defaults at `01F813C8` when the tag is 6. The cutscene loader
calls `001C51D0(map, "key")` (its only caller), a three-level chain: the given map, then the
`Common` section of the current scene map (`01F813D8 + 01F813F8 × 10h` when `01F81418` is set,
else `01DF6E50`'s), then `01F81328`, then `01F813C8`.

`001C52C0(map, section, key)` is the same chain for a
key inside a section, used three times by the cutscene loader (`001C4760`-`001C47BA`).
`001CC9A0(out, n)` makes the decimal string of n (`"%d"`, `008F6D3C`) that `001C5570` and `001CC600` append to
their key names.

Thirty keys land in the block, twenty-nine through the float reader and `mMapEnableShadowFade`
as `value == 1` at `+42C`<sub>h</sub> through the integer reader (`001C8F2B`); `mMapShadowFadeRange` at
`+43C`<sub>h</sub> is raised to 0.9 when the file gives less (`001C8FAB`):

- the four `chrFresnelSpecular*` at `+0D0`<sub>h</sub> to `+0DC`<sub>h</sub>;
- `mMapAmbientColorR/G/B` at `+0A0`<sub>h</sub> to `+0A8`<sub>h</sub>, `mMapAmbientColorCutPercent` at `+0B0`<sub>h</sub> and
  `mMapIrrCubemapIntensity` at `+09C`<sub>h</sub>;
- `mDebugRefractionFactor` and the seven `mDebugWater*` at `+074`<sub>h</sub> to `+090`<sub>h</sub>, `mWaterBias` at
  `+098`<sub>h</sub>;
- the eye modifiers `mEyeMap*` at `+028`<sub>h</sub>, `mEyeAB*` at `+104`<sub>h</sub>, `+108`<sub>h</sub> and `+114`<sub>h</sub>,
  `mEyeA*` at `+134`<sub>h</sub> and `mEyeB*` at `+158`<sub>h</sub>;
- `mCubemapIntensity` at `+168`<sub>h</sub> (`001846F0` parks it in `01F7F53C` and zeroes it, `001846B0`
  restores it, around the work those two bracket) and the four `mMapShadow*Fade*` at `+438`<sub>h</sub>
  to `+444`<sub>h</sub>.

The same loaders write everything else somewhere other than the block, among others:

- into the post-process parameter object (`4A8`<sub>h</sub> bytes, allocated on first use by `00193D50`
  into `01F7F5F0`, and cached again at `01F81300` by the static initializer `0015CAF0`):
  `EnableAO` at `+198`<sub>h</sub>, `mGammaValue` at `+F0`<sub>h</sub> (`00194300`), the unsharp mask, the glare,
  the colour correction, `EnableYebis` (`00194290`, the post-processing layer's switch at
  `+A0`<sub>h</sub>, `+A1`<sub>h</sub>, `+1F0`<sub>h</sub>) and the motion blur at `+334`<sub>h</sub> to `+33C`<sub>h</sub>;
- into the same object, the depth of field: `EnableDof`, `mDofApertureFnumber` and
  `mDofFocusDistance` at `+110`<sub>h</sub> to `+120`<sub>h</sub> through `00194250`; a cutscene with a `PresetDof`
  entry reads the pair from its `Common` section instead;
- into the shadow object (`B08`<sub>h</sub> bytes, constructor `001EF2D0`, allocated on first use by
  `001F0850` into `01F82EA8` and cached again at `01F812C8` by `0015CC00`): `ShadowBias` at
  `+898`<sub>h</sub>, `ShadowValueR/G/B` at `+EC`<sub>h</sub> to `+F4`<sub>h</sub>, `mCascadePartition*` at `+870`<sub>h</sub>,
  `m_iPCFBlurSize*` at `+890`<sub>h</sub> and `+894`<sub>h</sub>, `EnableShadow` at `+0`;
- the cutscene loader also sends `mShadowValueLerpMin*` to the shadow object's `+140`<sub>h</sub> and
  `+144`<sub>h</sub>, where the area loader sends them to `[01F81168]`;
- into `[01F81168]`: `EnableIBL` at `+2E4`<sub>h</sub> (and the byte `01DFE190`), the water tiling and
  sampling at `+2E8`<sub>h</sub> to `+308`<sub>h</sub>, `EnableMapNormalMap` at `+3D9`<sub>h</sub>;
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
`v / 180 × π`: `…Speed` by `001A9AA0` to `+480`<sub>h</sub>, `…Limit` by `001A9A70` to `+484`<sub>h</sub>,
`…SpeedMargin` by `001A9AD0` to `+488`<sub>h</sub>. A setter that changes its field calls `001A7770`, which
resets every entry of the map at `+498`<sub>h</sub>: angle `+30`<sub>h</sub> = 0, limit `+28`<sub>h</sub> = `+484`<sub>h</sub>, speed
`+24`<sub>h</sub> = `+480`<sub>h</sub> plus a `rand()` offset inside ±`+488`<sub>h</sub>.

The map-art update `001A9ED0` then moves each angle by speed × frame time and reverses the speed
when the angle reaches the limit on either side, but only while both `+480`<sub>h</sub> and `+484`<sub>h</sub> are
non-zero. The draw-list build `002F5550` reads a model's angle through `001802E0` (`001A7410`:
the entry with that model's index, 0 without one) and multiplies the model's placement by a
rotation of that angle (`00202F00`). The 2D background figures therefore sway back and forth,
each at its own speed.

The three per-slot shadow sets are stored by slot index and applied for the current slot:

- `mShadowValueLerpMinForMap`, `…Map2`, `…Map3` go through `001A9DA0(ctx, i, v)` to `+338h + i × 4`,
  and the three `…ForChr` keys through `001A9D70` to `+344h + i × 4`;
- `lightHeight` and `lightOrientation` 1 to 3, read only when the area's own file has both, become
  a direction (`001C4F50`, the two angles in degrees) that `001C78D0` hands to `001A9B30(ctx, i, x, y, z)`
  at `+374h + i × Ch`, setting the byte `+398`<sub>h</sub>; without them the loader clears `+398`<sub>h</sub>;
- the cutscene loader's `001C7850(height, orientation)` makes the same direction and passes it, with y negated, straight to
  the shadow object (`001F0850`, `001F08A0`);
- the cascade rows of `mCascadePartition%d_%d` sit at `+350h + i × Ch`.

After each of these the setter (or `001AA3B0` after the cascade loop and after each light)
calls `001A7E40(ctx, slot - 1)`, slot being `00265920()`: the developer menu's weather-slot override
`0017D490` when positive, else the area's slot byte `+1060`<sub>h</sub> plus 1. `001A7E40` copies that
slot's map and character values to the shadow object's `+140`<sub>h</sub> and `+144`<sub>h</sub>, its cascade row to
`+870`<sub>h</sub> to `+878`<sub>h</sub>, and, while `+398`<sub>h</sub> is set, its direction through `001F08A0` to the shadow
object's `+FC`<sub>h</sub> to `+104`<sub>h</sub> (normalised) and the block's `+450`<sub>h</sub> to `+458`<sub>h</sub>.

The map-art constructor `001A2130` registers `001A97F0` as a callback of the block (`0060B720`
appends it to the vector at `+1010`<sub>h</sub>). The callback writes `mapIrrCubeMapFactor` (`+0B8`<sub>h</sub>) =
the context's `+2DC`<sub>h</sub> while `EnableIBL` (`+2E4`<sub>h</sub>) is set and `001AC720(001AD440(), 0)` returns
an object, else 0. It writes `rtWidth` / `rtHeight` (`+0C0`<sub>h</sub> / `+0C4`<sub>h</sub>) from the render
manager's target (`001867B0`, its `+28`<sub>h</sub> and `+2C`<sub>h</sub> as floats), and `m_mapFadeHeight` (`+448`<sub>h</sub>)
= the context's `+32C`<sub>h</sub> while `+328`<sub>h</sub> is set, else 1.0.

The character render-object manager's constructor `001BC9D0` registers `001BD9D0` the same way (`001BCC6C`). It
writes the block's `+184`<sub>h</sub> (`02CB8154`): 0 while byte `+118`<sub>h</sub> of `001EBA40()` is set, otherwise `01DFE194`
when `01DFE190` is set and that value is at least 0.001 in size, else 0.

### The shadow matrices

`+190`<sub>h</sub> to `+38F`<sub>h</sub> is an array of eight 64-byte matrices and `+390`<sub>h</sub> to `+434`<sub>h</sub> the shadow
scalars beside them. `001F0AD0` is called once per frame by the render pass list `00187950`
inside its `"update shadowmap"` scope, from one of two sites (`00187D56`, `00187D64`) that pass
the camera block at `+690`<sub>h</sub> or `+358`<sub>h</sub> of the `00189120` object, chosen by that object's byte
`+DC5`<sub>h</sub> (the sub-camera-for-shadow switch, cleared after use at `00187D69`).

It copies the matrices out of the shadow object at `[01F82EA8]`: entry n of the block from
`object + 1C0h + n × D8h`, after `001EF6D0` has retargeted each of the object's eight slot
cameras (`+148h + n × D8h`, vtable at `+0`, matrix at `+78`<sub>h</sub>). `001EF6D0` also writes the
last slot's far plane to `+460`<sub>h</sub> (`001F045C`).

For a slot camera `001EF6D0` takes the eight corners of its view volume from `001EF560(out, fov, aspect, near,
far)`: four at the depth `-2 x near x far / (near + far)` and four at `-far`, each with y = ±depth / tan(pi/2 -
fov/2), x = ±y x aspect and w = 1. `001F0A00`, from `00169580`, `001EF280` and `006ACEE0`, builds an
orthographic matrix with `001F05B0(out, left, right, bottom, top, near, far)`: scales `2 / (right - left)`,
`2 / (top - bottom)` and `1 / (near - far)`, offsets `-(left + right) / (right - left)`, `-(top + bottom) /
(top - bottom)` and `near / (near - far)`.

At start-up the application set-up `00186CD0` gives the shadow object (`001F0850`) its map size through
`001F0570`: the Shadows setting's pair (`001DE5A0` on `[01F82D20]`) as its high half at `+844`<sub>h</sub> and its low
half at `+848`<sub>h</sub>.

The shadow scalars are written in the same pass. `+390`<sub>h</sub> to `+3AF`<sub>h</sub> is a copy of object
`+850`<sub>h</sub> to `+86F`<sub>h</sub>; the rest is derived, with h = the map size at object `+848`<sub>h</sub>:

| block | value |
|---|---|
| `+3B0`<sub>h</sub> to `+3B8`<sub>h</sub> | object `+FC`<sub>h</sub> to `+104`<sub>h</sub> |
| `+3D0`<sub>h</sub> to `+3D8`<sub>h</sub> | object `+EC`<sub>h</sub> to `+F4`<sub>h</sub> (`ShadowValue`) |
| `+3E4`<sub>h</sub> | the slot count `+13C`<sub>h</sub> |
| `+3E8`<sub>h</sub>, `+3FC`<sub>h</sub> | 1/h |
| `+3EC`<sub>h</sub> | (h - 1)/h |
| `+3F0`<sub>h</sub>, `+414`<sub>h</sub> | object `+8A4`<sub>h</sub>, `+8A0`<sub>h</sub> |
| `+3F4`<sub>h</sub> | object `+898`<sub>h</sub> (`ShadowBias`) |
| `+3F8`<sub>h</sub> | 1/3 |
| `+400`<sub>h</sub> | 1/(3h) |
| `+404`<sub>h</sub>, `+408`<sub>h</sub> | object `+830`<sub>h</sub>, `+82C`<sub>h</sub> |
| `+40C`<sub>h</sub> | object `+138`<sub>h</sub> |
| `+410`<sub>h</sub> | object `+8B8`<sub>h</sub> != 0 |
| `+41C`<sub>h</sub>, `+420`<sub>h</sub> | -n/2 and n/2 + 1 for n = the PCF size `+890`<sub>h</sub> capped at 7 |
| `+424`<sub>h</sub>, `+428`<sub>h</sub> | the same of `+894`<sub>h</sub> |
| `+430`<sub>h</sub>, `+434`<sub>h</sub> | object `+140`<sub>h</sub>, `+144`<sub>h</sub> |

`001F0AD0` also services the map resize request at object `+AFE`<sub>h</sub> (`001EE040` with `02CF7480` /
`02CF79C0`) and ends in `001F06D0` when the enable byte `+0` is set. No developer-menu arm touches
this range.

### From the block to the shaders

`006084B0` builds a `598`<sub>h</sub>-byte snapshot for the frame: the block's `+000`<sub>h</sub> to `+18F`<sub>h</sub> sixteen
bytes at a time into snapshot `+110`<sub>h</sub>, `+190`<sub>h</sub> to `+44F`<sub>h</sub> in one `005DEC50` copy into snapshot
`+2A0`<sub>h</sub>, and `+450`<sub>h</sub> to `+470`<sub>h</sub> field by field.

`00604750` builds that snapshot on its stack (the defaults of `005DC580` and `005DC430` first,
then `006084B0` over them), takes the lock at `+4B0`<sub>h</sub> (`005CD4F0` / `005CD820`), and compares
the `598`<sub>h</sub> bytes against the slot `idx & 1` at `+4E0`<sub>h</sub> with `idx` = `+4D8`<sub>h</sub>. When they are
equal it returns the previous ring entry and writes nothing. When they differ it advances `idx`
modulo `+498`<sub>h</sub>, copies the snapshot into that slot (`005DF3E0`), waits on the ring entry's busy
word (a `Sleep(1)` loop) and rewrites the constant buffer.

The write fills the shipped shaders' `SceneWideParameterConstantBuffer` from the snapshot, field
by field and reordered in places, so every block field below `+190`<sub>h</sub>
is one HLSL variable: `mapFresnelRefEnabled` at `+000`<sub>h</sub>, `vMapAmbientColor` at `+0A0`<sub>h</sub>,
`chrDiffuseIntensity` at `+160`<sub>h</sub>, `chrCubemapIntensity` at `+168`<sub>h</sub> and so on. The table gives
the constant-buffer offset and variable for all 276 fields the map reaches.

The two use generic matrix helpers: `001854C0` (the product of two affine 4 × 4 matrices, used by
`006084B0`), `00185AF0` (the inverse of an affine matrix through `001871B0`, with `+0C`<sub>h</sub>, `+1C`<sub>h</sub>
and `+2C`<sub>h</sub> set to 0 and `+3C`<sub>h</sub> to 1, used by `00604750`) and `00187460` (the same inverse, copied
out).

### The tonemap byte

`001C7940` reads `mUseLinearTonemap` as an integer and stores `value == 1` at `+4A2`<sub>h</sub> of the
post-process parameter object (`01F7F5F0`). The post-process frame build `0018EEE0` copies that
byte to `+9A`<sub>h</sub> of the frame parameters it hands to `005FEA50`, along with the DOF values from
`+110`<sub>h</sub>, the byte `+EE`<sub>h</sub> as a float at `+94`<sub>h</sub> (the loader's `mGammaValue` at `+F0`<sub>h</sub> is not
forwarded) and the colour-correction block at `+C4`<sub>h</sub>.

### Scripted depth of field

Event scripts set depth of field through two request slots (0 and 1) that `00214C30` applies:

| Call | Handler | Request |
|---|---|---|
| `5C1`<sub>h</sub> | `003513F0` → `00214B80` → `00214B90(kind, focus, aperture, slot)` | a full request; kind 0 replaces focus and aperture with `mDofFocusDistance` and `mDofApertureFnumber` from the map's file `01F81328` (`001C5530`, falling back to `01F813C8`); the enable word becomes 1 |
| `5BA`<sub>h</sub> | `0034D870` → `00214B40(enable)` | an enable-only request for slot 0 |
| `5C0`<sub>h</sub> | `0034DAF0` → `00214B50(enable, slot)` | an enable-only request for the given slot |

Three more calls read the cutscene's presets. Each first marks the event slot of the calling
script's record (`+28`<sub>h</sub> of `002640C0()`) in `01DFE40C`, or -1 for a slot above 4:

| Call | Handler | What it does |
|---|---|---|
| `5AE`<sub>h</sub> | `003526F0` → `001EC520(slot, n)` | pushes `mDofFocusDistance` of section `PresetDof n` |
| `5AF`<sub>h</sub> | `00352B30` → `001EC540(slot, n)` | pushes `mDofApertureFnumber` of section `PresetDof n` |
| `59F`<sub>h</sub> | `0034C7E0` → `001EC620(slot, n, 00358320())` | posts a `ReadPresetDofForCutSceneObj` (`0018C200`, `001F1CB0`) whose execute `001F3500` runs `001C6E20(n, value)` |

`001C5570(n, key)` reads the preset: it builds `"PresetDof "` plus n and looks the key up in that
section of `Common` in scene map 0 (`01F813A8`) for n = 0, else scene map 1 (`01F813D8`), at index
`01F813F8`, or at `01DF6E4C` while `01F81415` is set. `001C5530(map, key)`, used by `5C1`<sub>h</sub> with kind
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
  object's current `+11C`<sub>h</sub> and 35.0.

`001CC920` and `001CC800` also write the values into the running cutscene's data, but only for
slot 0 and only while an event slot is marked with queued events (`01DFE40C` below 5, its count at
`01F832B0` non-zero). They look up the section named by the cut name `01F81358` ("Cut N") in the
current scene map `01F813A8 + [01F813F8] × 10h` (`001FF6B0`) and set `EnableDof` (`00202820`),
`mDofFocusDistance` and `mDofApertureFnumber` (`002027B0`).

### The crossfade hold

The crossfade that script call `crossfade` (`016F`<sub>h</sub>, `00353260`) opens through `002F1A90` lives at
`022BE7C8` until `002F1950` clears it. `001CC600` keeps `01F81280` = that task exists and
`0022A550()` holds, with the previous value in `01F81281`. `00214C30(0)` treats its edges:

1. on the rising edge (`001C53B0`) it saves the live depth of field (`0018D5F0`: the post-process
   object's `+110`<sub>h</sub> to `+120`<sub>h</sub>) into both saved copies and sets the hold byte `01FD3AE6`;
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
| `01FD3AF0` | `DofCopy[2]` | saved | the held values, stride `14`<sub>h</sub> |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | enable | from post-process `+110`<sub>h</sub> |
| `04`<sub>h</sub> | `f32` | focus | from `+114`<sub>h</sub> |
| `08`<sub>h</sub> | `f32` | aperture | from `+118`<sub>h</sub> |
| `0C`<sub>h</sub> | `f32` | value3 | from `+11C`<sub>h</sub> |
| `10`<sub>h</sub> | `f32` | value4 | from `+120`<sub>h</sub> |

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
| `338`<sub>h</sub> | `f32[3]` | lerpMinMap | `mShadowValueLerpMinForMap`, `…2`, `…3` |
| `344`<sub>h</sub> | `f32[3]` | lerpMinChr | `mShadowValueLerpMinForChr`, `…2`, `…3` |
| `350`<sub>h</sub> | `f32[9]` | cascadeRows | three rows of `mCascadePartition%d_%d` |
| `374`<sub>h</sub> | `f32[9]` | lightDirs | three light directions |
| `398`<sub>h</sub> | `u8` | lightDirSet | the directions apply |
| `480`<sub>h</sub> | `f32` | swaySpeed | radians per second |
| `484`<sub>h</sub> | `f32` | swayLimit | radians |
| `488`<sub>h</sub> | `f32` | swayMargin | radians |
| `498`<sub>h</sub> | `SwayMap` | sway | one entry per model: speed `24`, limit `28`, angle `30` |

The block's `+1010`<sub>h</sub> is the vector of callbacks `0060B720` appends to, `001A97F0` among them.


## Shipped data

| Fact | Value |
|---|---|
| block fields with a shader constant | 276, in [graphics-settings.tsv](graphics-settings.tsv) |
| fields with a scene-config key | 30 in the block (21 below `+190`<sub>h</sub>), 13 in the second run |
| constructor defaults | 105 fields; `mMapAmbientColor` 1, 1, 1; `chrFresnelSpecularIntensity` 3.9; `mCubemapIntensity` 0.6; `mDebugWaterSpecFactor` 3.59; `+0C0`<sub>h</sub> / `+0C4`<sub>h</sub> 1920 and 1080 |
| shadow matrices | 8 of 64 bytes, block stride 64, object stride `D8`<sub>h</sub> |
| developer-menu arms on the block | 86 addresses, 84 below `+190`<sub>h</sub> |

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
- A field below `+190`<sub>h</sub> is live: the next frame's snapshot carries whatever is written there,
  and the constant buffer is rewritten because the snapshot changed. A field in `+190`<sub>h</sub> to
  `+434`<sub>h</sub> is overwritten by `001F0AD0`, and `+460`<sub>h</sub> by `001EF6D0`, before the frame uses it;
  `+42C`<sub>h</sub> and `+438`<sub>h</sub> to `+444`<sub>h</sub> hold until the next area load.
- `EnableYebis` is the whole post-processing layer, not one effect; `EnableAO`, `EnableDof`,
  `EnableShadow` and `EnableIBL` each switch one.
- Depth of field has three authors writing the same `+110`<sub>h</sub> to `+120`<sub>h</sub>: the area's config
  through the loaders, event scripts through the request slots (above), and `JsonData/CutScenes/<name>.json` through `001C5750`, whose one caller
  is the event-slot setter `0020AC30` (from the area load `0032FCA0`), and only for a slot whose
  path contains `sum_`, the summon scenes.

## Related

- [Debug menu](debug-menu.md): the rows that step the block.
- [Debug menu commands](debug-menu-commands.md): which row steps which field.
