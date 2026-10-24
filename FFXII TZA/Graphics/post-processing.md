---
title: "Post-processing: the game's passes and their shader constants, the post-process command, the PPFX features and effect techniques, and the registries of named render passes"
kind: "system"
category: "Graphics"
addresses: "0x0018D240, 0x0018E4A0, 0x0018F6B0, 0x0018F8F0, 0x0018FE00, 0x00190260, 0x00190760, 0x00191130, 0x00191560, 0x00191E90, 0x001925D0, 0x001930F0, 0x001EE8E0, 0x0018F510, 0x00191DA0, 0x0018EEE0, 0x00193D50, 0x01F7F5F0, 0x00194310, 0x00194250, 0x006FF900, 0x006CBD20, 0x007142F0, 0x007307A0, 0x0072D820, 0x0072A320, 0x0072DCF0, 0x02EA1590, 0x01F2D6A0, 0x02CBF998, 0x005DC6F0, 0x005FDCB0, 0x005DDD60, 0x01F82C80, 0x001D62D0, 0x001D6000"
---

## What the player sees

After the world is drawn the picture goes through full-screen passes: ambient occlusion darkens
creases and contact points (two different methods, with separate strengths for characters and
scenery), edges are smoothed by SMAA or FXAA as the PostAA option says, bright areas bloom, out-of-focus
areas blur, skin is softened by subsurface scattering, the whole image is colour-graded, and menu
text gets its outline. Glare and the cinematic depth of field come from the PPFX library, driven
by values each map and cutscene authors.

## How it works

### The game's twelve passes

Each pass function looks its shader constants up by name and draws with pass records from the static
array at `0x01F2D6A0` ([array](post-processing-named-render-pass-array.tsv)):

| Function | Pass | Pass records | Constants it names | Caller |
|---|---|---|---|---|
| `0x0018E4A0` | AO blur and composite | `SAOBlur`, `SAORender`, `SAOBlendCombine` | `ColorBufferSampler`, `gMainTexTexelSize`, `gAoAxis`, `gMainTex`, `gAoTex` | `0x0018F510` |
| `0x0018F6B0` | bloom | `BrightBlend` | `g_brightPara`, `g_BrightTex` | `0x00187950` |
| `0x0018F8F0` | colour grading | `ColorCorrection` | `apply_MainTex`, `colorR`, `colorG`, `colorB`, `percent`, `gamma`, `resolution` | `0x00187950`, `0x0018EEE0`, `0x001F3090` |
| `0x0018FE00` | single-step pass | `Opaque`, `Transparent` | `ColorBuffer`, `ColorBufferSampler`, `SingleStepOffset` | `0x001F3090` |
| `0x00190260` | font border | `FontBorderWidth`, `FontBorderHeight` | `FontBorderSetting`, `FontBorderColor`, `SingleStepOffset` | `0x00212E70` |
| `0x00190760` | HBAO | `HBAOGenerateAO` | `g_NumSteps`, `g_NumDir`, `g_FocalLen`, `g_HBAOResolution`, `g_RChr`, `g_AngleBiasChr`, `g_ContrastChr`, `g_RSce`, `g_AngleBiasSce`, `g_ContrastSce`, `g_fadeoutScale`, `g_maskBorder`, `tLinDepth`, `tNormal`, `projInfo` | `0x0018F510` |
| `0x00191130` | depth mask | `Opaque`, `Transparent`, `DebugMask` | `MaskDepth` | `0x001F32B0` |
| `0x00191560` | depth of field | `Opaque`, `DOFWriteOnePass` | `materialColor`, `customPosition`, `ColorBuffer`, `MaskBuffer`, `dofShift` | `0x001F3440` |
| `0x00191E90` | scalable AO (SAO) | `SAOGenerateAO` | `projScale`, `radiusChr`, `biasChr`, `intensityChr`, `radiusSce`, `biasSce`, `intensitySce`, `g_fadeoutScale`, `CS_Z_buffer`, `tNormal`, `projInfo`, `widthAO`, `heightAO` | `0x0018F510` |
| `0x001925D0` | SMAA | `ColorEdgeDetection`, `BlendingWeightCalculation`, `NeighborhoodBlending` | `areaTex`, `searchTex`, `edgesTex`, `blendTex`, `colorTex`, `smaa_resolution`, `SMAA_RT_METRICS`, `SMAA_THRESHOLD`, `SMAA_MAX_SEARCH_STEPS`, `SMAA_MAX_SEARCH_STEPS_DIAG`, `SMAA_CORNER_ROUNDING` | `0x00191DA0` |
| `0x001930F0` | subsurface-scattering blur | `SSS` | `useBigKernel`, `blendAmount`, `sssBlur`, `dir`, `SingleStepOffset`, `colorTex`, `depthTex`, `normalTex` | `0x001F3740` |
| `0x001EE8E0` | colour-buffer copy | `Opaque`, `OpaqueRGB` | `ColorBuffer`, `ColorBufferSampler`, `ColorBufferOffset` | 17 sites |

The samplers `LinearSampler`, `PointSampler` and `samNearest` are named too. The shaders are the
`.fx.phyre` assets on [Render parameters and shader assets](render-parameters-and-shader-assets.md).

The copy pass draws a mesh that `0x001EEC80` builds once, from the render-manager installer
`0x00186CD0`. It loads `./GameData/D3D11/ArtData/shaders/CopyBuffer.fx.phyre` (`0x0019CB20`,
`0x0063DA50`, `0x0063B010`), creates a `0xA0`-byte cluster at `0x01F82E60` (`0x00633040`), and builds in it
with `0x00649C20` the same one-triangle full-screen mesh the movie player builds with `0x001B72B0`,
keeping the mesh instance at `0x01F82E58`. The instance's material set (`+0x20`) gets one material
made from the asset's first `PEffectVariant` (`0x02CB6780`, `0x00600120`). `0x001EE8E0` draws that
instance (`0x0060B980`).

### Writing a constant

`0x0018D240(shader, name)` returns the parameter's descriptor or null. A pass then copies its value
into the constant block with `memcpy` (`0x00861EBA`) only when the descriptor's offset (`u16 +0x10`)
plus its size (`u16 +0x12` masked to 13 bits) fits the block's first dword and the offset is at
least 4 (`0x001929A7` to `0x001929E1`). A constant the shader does not declare is skipped silently.

`0x00194540(block, descriptor, sampler)` writes a sampler constant under the same test: the
descriptor's size of the record {`0x47`, sampler, 0} goes to its offset, and a constant that does
not fit returns 3. `0x001EE8E0` uses it for `ColorBufferSampler`, and the passes `0x0018F8F0`,
`0x0018FE00`, `0x00190260`, `0x00191560` and `0x001930F0` call it too.

### Ambient occlusion

`0x0018F510(block, …)` copies the colour buffer first (`0x001EE8E0`) unless the block's `+0x1E9` is set.
It runs AO only when the HDAO option (`+0x28` of the game settings, 1 half resolution, 2 full) is
on and the block's `+0x198` (`EnableAO`) is set:

- with `+0x344` = 1 it runs HBAO (`0x00190760`), after swapping in the targets `+0x2A0` / `+0x2A8` when
  HDAO is at half resolution and `+0x1E8` is clear;
- otherwise it runs SAO (`0x00191E90`);
- either way it then runs the blur and composite `0x0018E4A0`.

Both methods keep a character copy and a scene copy of each value in the render-parameter block:

| Block | Field | Pass constant | Set by |
|---|---|---|---|
| `+0x1A8` / `+0x1AC` / `+0x1B0` | bias, radius, intensity | `biasChr` (divided by 600), `radiusChr`, `intensityChr` | `0x001949C0` |
| `+0x1B4` / `+0x1B8` / `+0x1BC` | the same for the scene | `biasSce` (divided by 600), `radiusSce`, `intensitySce` | `0x001949E0` |
| `+0x1C4` / `+0x1C8` / `+0x1CC` | angle bias, radius, contrast | `g_AngleBiasChr` (degrees x π / 180), `g_RChr`, `g_ContrastChr` | `0x00194330` |
| `+0x1D0` / `+0x1D4` / `+0x1D8` | the same for the scene | `g_AngleBiasSce`, `g_RSce`, `g_ContrastSce` | `0x00194350` |

SAO's `projScale` is the constant 500.0 (`0x008F3140`), the bias divisor 600.0 (`0x008F3144`, divided
at `0x0019204D` and `0x0019210B`), and HBAO's angle conversion uses `0x008F3120` (π) and `0x008F3138`
(180.0) at `0x00190B64` and `0x00190C85`. Both scene loaders call the four setters with the `mSAO*` and
`mHBAO*` keys ([Graphics settings](../Engine-Core/graphics-settings.md)).

### Anti-aliasing

`0x00191DA0` runs when the block's `+0x3E8` and `+0x3E9` are set. With `+0x4A3` set (the PostAA option
on `SMAA_1x`) it runs SMAA `0x001925D0`; otherwise PhyreEngine's FXAA (`0x0065A630`, see
[Phyre post-effect classes](../PhyreEngine/phyre-post-effect-classes.md)) and the copy
`0x001EE8E0`. SMAA takes four constants from the quality integer at `+0x184`:

| `+0x184` | `SMAA_THRESHOLD` | `SMAA_MAX_SEARCH_STEPS` | `SMAA_MAX_SEARCH_STEPS_DIAG` | `SMAA_CORNER_ROUNDING` |
|---|---|---|---|---|
| 1 | 0.15 | 4 | 0 | 0 |
| 2 | 0.10 | 8 | 0 | 0 |
| 3 | 0.10 | 16 | 8 | 25 |
| 4 | 0.05 | 32 | 16 | 25 |
| any other | 0.15 | 4 | 0 | 0 |

The thresholds are `0x008F30F4`, `0x008C5F6C` and `0x008F30E8` (`0x00192975` to `0x0019299A`); the step counts
are immediates (`0x001929FA` to `0x00192A2F`).

### The post-process command

`0x0018EEE0` builds the post-process command each frame: it allocates a `0xF0`-byte block
(`0x001A1470`), fills it from the `0x4A8`-byte render-parameter block (`0x00193D50`, kept at `0x01F7F5F0`)
and enqueues it on the render command list (`0x005FEA50`). [YEBIS post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md)
gives the per-frame library calls its work function `0x00193DA0` makes with it.

| Command | From the block | Meaning |
|---|---|---|
| `+0x00`, `+0x08`, `+0x10` | render targets | the three targets `0x006CBEA0` hands the library |
| `+0x18`, `+0x1C` | `+0xF4`, `+0xF8` | glare luminance and threshold (`0x00194310`) |
| `+0x20` | `+0x110` | depth-of-field enable |
| `+0x21` | `+0x164` | a byte the depth-of-field call also passes |
| `+0x24`, `+0x28` | `+0x114`, `+0x118` | focus distance and aperture f-number (`0x00194250`) |
| `+0x2C` | `+0x120` | the value the cutscene loader sets to 35.0 |
| `+0x30`, `+0x34` | `+0x168`, `+0x16C` | two floats the depth-of-field call also passes |
| `+0x99` | | set when the first argument's `+0x4A1` is set or `+0xDB9` of the object `0x00189120` returns differs from its value last frame (`+0x48C`) |
| `+0x9A` | `+0x4A2` | the linear-tonemap byte |
| `+0xDC` to `+0xE4` | `+0x480` to `+0x488` | three floats |

When the first argument's `+0x124` is 2 the focus distance is its `+0x128`; when it is 1 and `+0x128`
is positive, both the distance and an f-number computed from it (scaled by block `+0x11C`) are used,
eased over ten frames when they change (`0x0018EF94` to `0x0018F2BD`). With `d` the distance and
`c(x, lo, hi)` a clamp, the f-number is `(1 + 0.33 c(4 - d, -2, 3) + 0.7 c(2.9 - d, 0, 2.7) +
0.15 c(d - 4.4, 0, 4) - 0.2 c(d - 6, 0, 3)) x [block +0x11C]`. While easing, each frame moves both values by
`(target - current) / (10 x [0x01DFE0B4] - n)`, `n` counting the frames already eased.

While the block's byte `+0x164` is set, the render pass list `0x00187950` marks the point at `+0x168`
and `+0x16C` (`0x0018D320`) on screen. It maps the point from 0 to 1 into clip space with y flipped
and calls `0x001862B0(manager, x, y)`, which reserves 0x50 bytes of a render-thread callback
(`0x005FEB30` on the manager's device) for `0x001890A0`: four vertices (x ± 0.1, y) and (x, y ± 0.1)
with w = 1.0 and the colour (0, 1, 0, 1), drawn with `0x006215A0` in mode 1 between `0x00628570(ctx,
0, 1)` and `0x00628570(ctx, 1)`.

The depth-of-field pass `0x00191560` works only while the block's byte `+0x349` is set and `+0x110`
is clear. `0x001828C0(on, mode, a, b, c, d, e, f, g)` sets the byte and the pass's values through
`0x001944D0`: `+0x349` = (`on` ≠ 0), the mode at `+0x360` (the pass tests it for 1 and 2) and the
other values at `+0x34C`, `+0x350`, `+0x354`, `+0x358`, `+0x35C`, `+0x364` and `+0x368`. Its caller is `0x00474710`, which
passes 1 and values from its own record each time it runs.

The cutscene loader `0x001C3D50` reads `mGlareThreshold` and `mGlareLuminance` into `0x00194310`
(`0x001C42E4`) and `EnableDof`, `mDofFocusDistance` and `mDofApertureFnumber` into `0x00194250` with
35.0 (`0x001C42A1`); the area loader `0x001C7940` calls both setters with the enable fixed at 1.

### The PPFX features the game leaves off

`0x006CBD20` initialises the library once with the flag word `0x20001` (`0x006CBE02`).
`CPostEffect::Initialize` (`0x006FF900`) stores it at `+0x20C` (`0x006FFB8C`) and derives one byte per
optional feature from it (`0x006FFE56` to `0x00700071`, with `r12` = 1):

| Flag bit | Byte | Feature (from its setter's message) | Setter |
|---|---|---|---|
| `0x40000` | `+0x131` | lens distortion | `0x00709C90` |
| `0x40000` | `+0x133` | aperture Airy disc | `0x0070A060` |
| `0x40000` | `+0x134` | motion blur | `0x0070A480` |
| `0x40000` | `+0x137` | geometry blur | `0x0070A410` |
| `0x40000` | `+0x138` | Gaussian blur | `0x0070A0F0` |
| `0x40000` | `+0x13C`, `+0x13D` | heat shimmer, heat-shimmer particles | `0x0070A350` |
| `0x40000` | `+0x142` | chromatic aberration | `0x00709F40` |
| `0x4000000` | `+0x13A` | ambient occlusion | `0x0070AA80` |
| `0x8000000` | `+0x140`, `+0x141` | post-process antialias, its distance falloff | `0x0070A1F0`, `0x0070A260` |

Each setter first compares its byte with 0 and refuses with "Initialize() with PFXINIT_… flag".
`0x20001` holds none of the three bits, so all of these PPFX features stay off; the game's own AO and
anti-aliasing passes above are separate code. Depth of field and glare are not behind these bits.

### The PPFX effect catalogue

The library's texture utility `CTextureUtil` is a reference-counted singleton (`0x02EA1590`, count
`0x02EA1598`): `0x007142F0` allocates `0x22360` bytes on first use. `Initialize` acquires it
(`0x00700972`) and calls its slot 0, `0x007307A0`, which calls `0x0072D820`, which calls
`TEXSHADERSET::CreateEffect` `0x0072A320` (`0x0072D872`) and abandons the sequence on a non-zero result.

`0x0072A320` (13,547 bytes) loads the compiled effect once through `0x0078A120`, returns the loader's
error unchanged when that fails, and then fetches a handle for each technique and uniform it names. Its body
references 364 distinct strings: 325 `tech_` names and 36 uniforms, among them `fParam_FocusDistance`, three HDR formats
(`fParam_HDRFormatFactor_LOGRGB`, `_REINHARDRGB`, `_RGBALUM`) and the vignette and lens-distortion
parameters. Its ten log calls are gated by `0x01F3BA80` together with `0x02EA0B40` or `0x01F3BA90`.

The largest technique family is `tech_DepthOfField` (53 names), then
`tech_CompositeColorAndAlphaEffectsMask` (20), `tech_GenerateNormalDepth` (15) and
`tech_TemporalAntialias` (14). The helper `0x0072DCF0`, called at 65 sites with a count `n`, drops the
name's last character, appends `1` to `n`, and fetches each of those under 22 suffixes: none, and 21
HDR conversions such as `_REINHARDRGB_RGB` and `_LOGRGBLUM_RGBFAST` (table `0x02EA2250`).

Handles are 32-bit values stored from `this + 8` (`0x0072A496`). One run is addressed from `this + 0x1AA10`
(`0x0072BA97`): a five-pass loop (`0x0072BAB0`-`0x0072C5C3`) fills 25 slots from `+0x1A9C0` to `+0x1AA20`, and
other loops fill arrays of 8 and 4. The last slot is at `+0x221D8`. The placed slots are in
[the handle layout](post-processing-ppfx-handle-layout.tsv): 352 handle stores, fewer than the names, because a
family row fetches several names under one count and suffix table.

### The render-pass registries

Two sets of named pass records exist side by side:

- The static array at `0x01F2D6A0`: 56 records of `0x20` bytes, `{ name, 0, 0, 0xFFFFFFFF }`, the last
  one named `NULL`. It holds `Opaque`, `OpaqueRGB`, `Transparent`, `DeferredRender`, the map passes
  (`DefaultMapRenderPass…`, `AteGequalFbonly…`, `WaterPassFor…`), the character passes
  (`ChrOpaque…`) and the twelve game passes' records above.
- The runtime registry headed at `0x02CBF998`: 60 static initialisers each call
  `0x005DC6F0(record, name, 0)`, which fills the record (name, next 0, flag, `+0x18` = -1) and calls
  `0x005FDCB0`.
  - `0x005FDCB0` returns `0x11` for a null name and `0x12` for a duplicate name; otherwise it pushes
    the record at the head and returns 0. `0x005DDD60` unlinks a record at exit.
  - The 60 names are PhyreEngine's passes, from `ShadowRender` and `RenderFXAA` to the atmosphere
    precompute and `RenderText_*` passes
    ([registry](post-processing-runtime-render-pass-registry.tsv),
    [teardown wrappers](post-processing-render-pass-registry-60.tsv)).
- `0x005F05F0` (`PNamedSemanticDynamic::FindOrCreateDynamic`) returns the registry record of a name. For a name the
  registry lacks it logs "Performance warning - allocating freelist on demand" and creates one: a record from the
  pool `0x02CC0388`, a name buffer from `0x02CC03B0`, the record set to `{name, next 0, flag 1, +0x18 = -1}` and
  registered with `0x005FDCB0`.
- It copies the name with its terminator (`0x005F06E3`) and takes the name's whole length, so a name of 64 bytes or
  more runs past its 64-byte buffer.

### The frame-marker table

`0x001D62D0` allocates the `0xF778`-byte object at `0x01F82C80` at start-up. It is a GPU timing table:
`0x001D5970` creates one timestamp-disjoint query and five rings of 128 timestamp queries
(`0x01F81838`, `0x01F81880`). `0x00187950` queues `0x001D5FD0` on the render command list, and each call
ends the next timestamp query of the current ring (`0x001D6250`). `0x001D6000`, also from `0x00187950`,
stamps an `END` marker (`0x001D6040`), reads back the ring from the frame before
(`0x001D5650`), stores the measured time as a double at `+0xD70` of the object `0x001D50D0` returns, and
clears the marker list (`0x001D6170`).

`0x001D6170` runs `0x001D5970` again while the object's byte `+0x15` is clear. Besides the queries,
`0x001D5970` lays out two rows of bar quads in the object, six vertices of 16 bytes each, after
resetting all `0x324` vertices of each row to `(0, 0, 0, 1)`:

- colours: `0x001D6370(obj, i, r, g, b)` writes colour `i`, divided by 255 with alpha 1.0, to the six
  vertices at `+0x92B8 + i × 0x60` (row 1), and `0x001D6630` at `+0xC4F8` (row 2). Entries 0 and 1 get
  `(0x86, 0x7B, 0x6F)` and `(0x86, 0x64, 0x6D)`, 2 to 4 get `(0xF6, 0xFF, 0x06)`, and 5 to 133 cycle
  through the ten colours at `0x01DFCFC0`: cyan, red, yellow, blue, purple, olive, green, navy, magenta
  and maroon;
- positions: `0x001D64D0(obj, i, x, y, w, h)` (row 1, vertices from `+0x2E38`) and `0x001D6790` (row 2,
  from `+0x6078`) write the two triangles of the rectangle with depth `−0.1 × i`. Quad 0 starts at
  `(+0x04, +0x0C)` (row 2: `+0x10`) with width `1 − +0x00` and height `+0x08`, quad 1 follows it,
  and quads 2 to 4 are ticks 0.01 wide and 0.08 high, 0.04 lower, starting 0.01 left of 0, 1 and 2
  widths from the start.

## Layouts

The post-process command, `0xF0` bytes, that `0x0018EEE0` fills each frame and `0x00193DA0` runs:

`PostProcessFrameParams` (`0xF0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | targetA | the first of the three render targets `0x006CBEA0` hands the library: `0x001867B0` of the render manager (`0x0018EF3E`); passed as the second argument of `0x0065E5C0` (`0x00193F55`) and as the third argument of the context creation `0x0065E5A0` (`0x00193DDF`); with +`0x98` set the builder also runs the colour-grading pass `0x0018F8F0` on it (`0x0018F36D`) and copies it with `0x001EE8E0` (`0x0018F3B0`) |
| `+0x08` | `void*` | targetB | the second of the three render targets: `0x00186660` of the render manager (`0x0018EF4E`); the third argument of `0x0065E5C0` (`0x00193F51`) |
| `+0x10` | `void*` | targetC | the third render target: `0x001868F0`(manager, 0) when +`0x98` and the builder's fifth argument are set, otherwise `0x001867C0`(manager) (`0x0018EF68`-`0x0018EF90`); the fourth argument of `0x0065E5C0` (`0x00193F4A`) |
| `+0x18` | `f32` | glareLuminance | glare luminance, the block's +`0xF4` (`0x0018EFF3`); with the Glare option on (`0x01F82D20` +`0x34`) it is the first float `0x006CC1E0` hands CPostEffect::SetGlareParameters (`0x00193E52`), which stores it at CPostEffect +`0x6E4` |
| `+0x1C` | `f32` | glareThreshold | glare threshold, the block's +`0xF8` (`0x0018EFFC`); the second float of the glare call (`0x00193E4D`), stored at CPostEffect +`0x6E0` |
| `+0x20` | `u8` | dofEnable | depth-of-field enable, the block's +`0x110` (`0x0018F00C`); passed as the enable byte of the depth-of-field call `0x0065E610` while the DepthofField option (`0x01F82D20` +`0x30`) is on (`0x00193EE6`); the builder also copies it into the block's per-slot byte +`0xFC` (`0x0018F2C4`) |
| `+0x21` | `u8` | autoFocus | the auto-focus byte: the block's +`0x164` (`0x0018F30C`), which also makes the render pass list `0x00187950` draw the focus-point marker; passed to the depth-of-field call (`0x00193ED8`), where a set byte turns the library's auto-focus on (`0x0070EC00`), aims it at +`0x30`/+`0x34` (`0x0070F3C0`) over 0.1 to 100 (`0x0070F300`) and takes the auto-focus distance (`0x006DC650`) as the focus distance (`0x006CC0C5`-`0x006CC131`) |
| `+0x22` | `u8[2]` | pad022 | written and read by no function; nothing fixes its width |
| `+0x24` | `f32` | focusDistance | focus distance (`0x00194250`): the block's +`0x128` or +`0x114`, or the eased value, by the mode at +`0x124` of the first argument (`0x0018F19A`, `0x0018F229`, `0x0018F257`); passed at `0x00193EE1` |
| `+0x28` | `f32` | apertureFNumber | aperture f-number, computed with the focus distance (`0x0018F1B7`, `0x0018F22E`, `0x0018F260`); passed at `0x00193EDC` |
| `+0x2C` | `f32` | lens | the block's +`0x120`, the value the cutscene loader sets to 35.0 (`0x0018F2F7`); `0x00193DA0` does not read it and passes the constant 35.0 (`0x008F312C`, `0x00193EF0`) instead |
| `+0x30` | `f32` | focusPointX | the x of the focus point, the block's +`0x168` (`0x0018F300`): the point the marker draws and the auto-focus samples (`0x00193ED3`, `0x006CC0F0`) |
| `+0x34` | `f32` | focusPointY | the y of the focus point, the block's +`0x16C` (`0x0018F309`) (`0x00193ECB`, `0x006CC0E7`) |
| `+0x38` | `u8[12]` | pad038 | written and read by no function; nothing fixes its width |
| `+0x44` | `f32` | flareScreenX | the screen x of the bit-5 lens flare, the block's +`0x36C` (`0x0018F3FB`), stored by `0x00182830` through `0x00194470` from the flare draw `0x00461270`; read by no function in `0x00193DA0` or its callees |
| `+0x48` | `f32` | flareScreenY | the screen y of the same flare, the block's +`0x370` (`0x0018F404`); read by no function in `0x00193DA0` or its callees |
| `+0x4C` | `f32[10]` | lightShaft | the light-shaft values, the block's +`0xC4` to +`0xEB` (`0x0018F407`-`0x0018F445`): colour R, G, B (`lightShaftColorR`/`G`/`B`) and 0 for the alpha, `lightShaftLength`, `lightShaftGlareRatio`, `lightShaftMaskDepthThereshold`, `lightShaftAngleAttenuation`, `lightShaftNoiseMask` and `lightShaftNoiseFrequency` as set by `0x00194400` (`0x001C8AF5`); read by no function in `0x00193DA0` or its callees |
| `+0x74` | `f32[8]` | lightShaftRing | the light-shaft diffraction ring, the block's +`0xA4` to +`0xC3` (`0x0018F448`-`0x0018F476`): `lightShaftDiffractionRing`, `…Radius`, `…Attenuation`, `…SpectrumOrder`, then `…OuterColorR`/`G`/`B`/`A`, as set by `0x00194370` (`0x001C8D33`); read by no function in `0x00193DA0` or its callees |
| `+0x94` | `f32` | lightShaftOn | the block's byte +`0xEE` as a float (`0x0018F3DF`-`0x0018F3ED`); both writers of that byte, `0x001943C0` and `0x0018D640`, end with 0 on every path (`0x001943DA`, `0x0018D65A`), so the value is 0.0; read by no function in `0x00193DA0` or its callees |
| `+0x98` | `u8` | deviceByte | the device byte +`0xD48` of the PhyreEngine application object `0x00796E20`() (`0x0018EF57`); when set the builder runs the colour-grading pass and the copy (`0x0018F323`-`0x0018F3B6`) and `0x00193DA0` passes 2.0 and mode 2 to `0x006CC170` (`0x00193E71`-`0x00193E87`) |
| `+0x99` | `u8` | reinitialise | set when the first argument's +`0x4A1` is set or +`0xDB9` of the object `0x00189120` returns differs from its value last frame (+`0x48C`) (`0x0018EF94`-`0x0018EFAF`); when set `0x00193DA0` calls `0x006CC2F0` on the existing context instead of creating one (`0x00193DB1`) |
| `+0x9A` | `u8` | linearTonemap | the linear-tonemap byte, the block's +`0x4A2` (`0x0018F316`); with +`0x98` clear `0x00193DA0` passes mode 1 when it is set and -1 when it is clear to `0x006CC170` (`0x00193E8F`-`0x00193EAE`) |
| `+0x9B` | `u8[1]` | pad09B | written and read by no function; nothing fixes its width |
| `+0x9C` | `f32[16]` | cameraMatrix | the camera matrix, the block's +`0x440` to +`0x47F` (`0x0018F47D`-`0x0018F4AE`), which `0x00189CE0` copies from the camera `0x001AC950` through `0x001941F0`; its address goes to `0x006CC1F0` (`0x00193E0A`), which hands the previous matrix to `0x00707220` and this one to `0x00706F60` (CPostEffect +`0x654` and +`0x5D4`) |
| `+0xDC` | `f32` | cameraNear | the block's +`0x480` (`0x0018F4BB`), default 0.1 (`0x0018D007`), the camera's +`0xCBC` (`0x00189EA2`); the first float of `0x006CC260` (`0x00193E2E`), which becomes CPostEffect +`0x5A4` |
| `+0xE0` | `f32` | cameraFar | the block's +`0x484` (`0x0018F4C7`), default 1000.0 (`0x0018D011`), the camera's +`0xCC0`; the second float of `0x006CC260` (`0x00193E26`), CPostEffect +`0x5A8` |
| `+0xE4` | `f32` | cameraAngle | the block's +`0x488` (`0x0018F4D3`), default 0.785398 (π / 4, `0x0018D01B`), the camera's +`0xCC4`; the third float of `0x006CC260` (`0x00193E1B`), which halves it (`0x006CC29A`); `0x00706C20` halves it again and stores its tangent at CPostEffect +`0x5B0` (`0x00706C26`-`0x00706C98`) |
| `+0xE8` | `u8[8]` | pad0E8 | written and read by no function; nothing fixes its width |

The render-parameter block fields this page uses (`0x4A8` bytes at `0x01F7F5F0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0F4` | `f32` | glare luminance | +`0x0F8`  f32     glare threshold |
| `+0x110` | `u8` | depth-of-field enable | +`0x114`  f32     focus distance |
| `+0x118` | `f32` | aperture f-number | +`0x11C`  f32     f-number scale |
| `+0x120` | `f32` | lens (35.0) |  |
| `+0x184` | `i32` | SMAA quality |  |
| `+0x198` | `u8` | EnableAO |  |
| `+0x1A8` | `f32[6]` | SAO bias, radius, intensity: Chr, then Sce |  |
| `+0x1C4` | `f32[6]` | HBAO angle bias, radius, contrast: Chr, then Sce |  |
| `+0x344` | `i32` | 1 = HBAO |  |
| `+0x3E8` | `u8` | anti-aliasing built | +`0x3E9`  u8      anti-aliasing configured |
| `+0x4A3` | `u8` | PostAA is SMAA |  |

## Shipped data

| Fact | Value |
|---|---|
| shader-constant names in the twelve passes | 89 calls of `0x0018D240` |
| `0x0072A320` | 379 string references, 325 `tech_` names, 36 uniforms; 358 direct calls to 22 targets |
| static pass array | 56 records, `0x01F2D6A0` to the `NULL` record at `0x01F2DD80` |
| runtime pass registry | 60 registration sites, 60 names, 60 records |
| access tables | [CPostEffect](post-processing-cposteffect-accesses.tsv), [its initialise descriptor](post-processing-ppfx-init-descriptor-accesses.tsv), [the frame-marker object](post-processing-frame-marker-singleton-accesses.tsv) |

## State

| Address | Holds |
|---|---|
| `0x01F7F5F0` | the render-parameter block (also cached at `0x01F81300`) |
| `0x02EA0B70` | the `CPostEffect` object the PPFX calls run on |
| `0x02EA1590`, `0x02EA1598` | the `CTextureUtil` singleton and its reference count |
| `0x02CBF998` | the head of the runtime render-pass registry |
| `0x01F82C80` | the frame-marker table |
| `0x02CC0388` | the pool of `0x20`-byte pass records for passes created at run time: built by `0x00162330` (`0x0067FFB0`: 256 records, alignment 8, named `PSceneRenderPassType`), its free list filled by `0x00680150` when empty, reset by `0x005FDDF0` (`0x006803D0`), destroyed at exit by `0x008AB790` |
| `0x02CC03B0` | the pool of `0x40`-byte name buffers for those records: built by `0x001623D0` (256, alignment 1), filled, reset and destroyed in the same way (`0x008AB7B0` at exit) |

## Modding notes

- AO strength is two independent sets, characters and scenery; change both halves of each pair.
- HBAO angle biases are authored in degrees, SAO biases in units the pass divides by 600.
- Turning on a PPFX feature from the table above needs a different initialise flag word at
  `0x006CBE02`; the setters refuse otherwise.
- A shader that drops a constant name keeps working: the pass skips the missing constant.

## Related

- [YEBIS post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md): the library, its
  start-up and the per-frame calls.
- [Phyre post-effect classes](../PhyreEngine/phyre-post-effect-classes.md): the FXAA
  object and the shared copy pass `0x001EE8E0`.
- [The frame](../PhyreEngine/the-frame.md): where the passes fall in a frame.
- [Graphics settings](../Engine-Core/graphics-settings.md): the scene keys and the block.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the HDAO, PostAA, Glare and
  DepthofField options.
- [Render command list](render-command-list.md): where the command and the markers are queued.
- [Render parameters and shader assets](render-parameters-and-shader-assets.md): the shader files.
