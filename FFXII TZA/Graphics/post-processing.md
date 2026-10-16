---
title: "Post-processing: the game's passes and their shader constants, the post-process command, the PPFX features and effect techniques, and the registries of named render passes"
kind: "system"
category: "Graphics"
addresses: "0018D240, 0018E4A0, 0018F6B0, 0018F8F0, 0018FE00, 00190260, 00190760, 00191130, 00191560, 00191E90, 001925D0, 001930F0, 001EE8E0, 0018F510, 00191DA0, 0018EEE0, 00193D50, 01F7F5F0, 00194310, 00194250, 006FF900, 006CBD20, 007142F0, 007307A0, 0072D820, 0072A320, 0072DCF0, 02EA1590, 01F2D6A0, 02CBF998, 005DC6F0, 005FDCB0, 005DDD60, 01F82C80, 001D62D0, 001D6000"
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
array at `01F2D6A0` ([array](post-processing-named-render-pass-array.tsv)):

| Function | Pass | Pass records | Constants it names | Caller |
|---|---|---|---|---|
| `0018E4A0` | AO blur and composite | `SAOBlur`, `SAORender`, `SAOBlendCombine` | `ColorBufferSampler`, `gMainTexTexelSize`, `gAoAxis`, `gMainTex`, `gAoTex` | `0018F510` |
| `0018F6B0` | bloom | `BrightBlend` | `g_brightPara`, `g_BrightTex` | `00187950` |
| `0018F8F0` | colour grading | `ColorCorrection` | `apply_MainTex`, `colorR`, `colorG`, `colorB`, `percent`, `gamma`, `resolution` | `00187950`, `0018EEE0`, `001F3090` |
| `0018FE00` | single-step pass | `Opaque`, `Transparent` | `ColorBuffer`, `ColorBufferSampler`, `SingleStepOffset` | `001F3090` |
| `00190260` | font border | `FontBorderWidth`, `FontBorderHeight` | `FontBorderSetting`, `FontBorderColor`, `SingleStepOffset` | `00212E70` |
| `00190760` | HBAO | `HBAOGenerateAO` | `g_NumSteps`, `g_NumDir`, `g_FocalLen`, `g_HBAOResolution`, `g_RChr`, `g_AngleBiasChr`, `g_ContrastChr`, `g_RSce`, `g_AngleBiasSce`, `g_ContrastSce`, `g_fadeoutScale`, `g_maskBorder`, `tLinDepth`, `tNormal`, `projInfo` | `0018F510` |
| `00191130` | depth mask | `Opaque`, `Transparent`, `DebugMask` | `MaskDepth` | `001F32B0` |
| `00191560` | depth of field | `Opaque`, `DOFWriteOnePass` | `materialColor`, `customPosition`, `ColorBuffer`, `MaskBuffer`, `dofShift` | `001F3440` |
| `00191E90` | scalable AO (SAO) | `SAOGenerateAO` | `projScale`, `radiusChr`, `biasChr`, `intensityChr`, `radiusSce`, `biasSce`, `intensitySce`, `g_fadeoutScale`, `CS_Z_buffer`, `tNormal`, `projInfo`, `widthAO`, `heightAO` | `0018F510` |
| `001925D0` | SMAA | `ColorEdgeDetection`, `BlendingWeightCalculation`, `NeighborhoodBlending` | `areaTex`, `searchTex`, `edgesTex`, `blendTex`, `colorTex`, `smaa_resolution`, `SMAA_RT_METRICS`, `SMAA_THRESHOLD`, `SMAA_MAX_SEARCH_STEPS`, `SMAA_MAX_SEARCH_STEPS_DIAG`, `SMAA_CORNER_ROUNDING` | `00191DA0` |
| `001930F0` | subsurface-scattering blur | `SSS` | `useBigKernel`, `blendAmount`, `sssBlur`, `dir`, `SingleStepOffset`, `colorTex`, `depthTex`, `normalTex` | `001F3740` |
| `001EE8E0` | colour-buffer copy | `Opaque`, `OpaqueRGB` | `ColorBuffer`, `ColorBufferSampler`, `ColorBufferOffset` | 17 sites |

The samplers `LinearSampler`, `PointSampler` and `samNearest` are named too. The shaders are the
`.fx.phyre` assets on [Render parameters and shader assets](render-parameters-and-shader-assets.md).

The copy pass draws a mesh that `001EEC80` builds once, from the render-manager installer
`00186CD0`. It loads `./GameData/D3D11/ArtData/shaders/CopyBuffer.fx.phyre` (`0019CB20`,
`0063DA50`, `0063B010`), creates a `0xA0`-byte cluster at `01F82E60` (`00633040`), and builds in it
with `00649C20` the same one-triangle full-screen mesh the movie player builds with `001B72B0`,
keeping the mesh instance at `01F82E58`. The instance's material set (`+0x20`) gets one material
made from the asset's first `PEffectVariant` (`02CB6780`, `00600120`). `001EE8E0` draws that
instance (`0060B980`).

### Writing a constant

`0018D240(shader, name)` returns the parameter's descriptor or null. A pass then copies its value
into the constant block with `memcpy` (`00861EBA`) only when the descriptor's offset (`u16 +0x10`)
plus its size (`u16 +0x12` masked to 13 bits) fits the block's first dword and the offset is at
least 4 (`001929A7` to `001929E1`). A constant the shader does not declare is skipped silently.

`00194540(block, descriptor, sampler)` writes a sampler constant under the same test: the
descriptor's size of the record {`0x47`, sampler, 0} goes to its offset, and a constant that does
not fit returns 3. `001EE8E0` uses it for `ColorBufferSampler`, and the passes `0018F8F0`,
`0018FE00`, `00190260`, `00191560` and `001930F0` call it too.

### Ambient occlusion

`0018F510(block, …)` copies the colour buffer first (`001EE8E0`) unless the block's `+0x1E9` is set.
It runs AO only when the HDAO option (`+0x28` of the game settings, 1 half resolution, 2 full) is
on and the block's `+0x198` (`EnableAO`) is set:

- with `+0x344` = 1 it runs HBAO (`00190760`), after swapping in the targets `+0x2A0` / `+0x2A8` when
  HDAO is at half resolution and `+0x1E8` is clear;
- otherwise it runs SAO (`00191E90`);
- either way it then runs the blur and composite `0018E4A0`.

Both methods keep a character copy and a scene copy of each value in the render-parameter block:

| Block | Field | Pass constant | Set by |
|---|---|---|---|
| `+0x1A8` / `+0x1AC` / `+0x1B0` | bias, radius, intensity | `biasChr` (divided by 600), `radiusChr`, `intensityChr` | `001949C0` |
| `+0x1B4` / `+0x1B8` / `+0x1BC` | the same for the scene | `biasSce` (divided by 600), `radiusSce`, `intensitySce` | `001949E0` |
| `+0x1C4` / `+0x1C8` / `+0x1CC` | angle bias, radius, contrast | `g_AngleBiasChr` (degrees x π / 180), `g_RChr`, `g_ContrastChr` | `00194330` |
| `+0x1D0` / `+0x1D4` / `+0x1D8` | the same for the scene | `g_AngleBiasSce`, `g_RSce`, `g_ContrastSce` | `00194350` |

SAO's `projScale` is the constant 500.0 (`008F3140`), the bias divisor 600.0 (`008F3144`, divided
at `0019204D` and `0019210B`), and HBAO's angle conversion uses `008F3120` (π) and `008F3138`
(180.0) at `00190B64` and `00190C85`. Both scene loaders call the four setters with the `mSAO*` and
`mHBAO*` keys ([Graphics settings](../Engine-Core/graphics-settings.md)).

### Anti-aliasing

`00191DA0` runs when the block's `+0x3E8` and `+0x3E9` are set. With `+0x4A3` set (the PostAA option
on `SMAA_1x`) it runs SMAA `001925D0`; otherwise PhyreEngine's FXAA (`0065A630`, see
[Phyre post-effect classes](../PhyreEngine/phyre-post-effect-classes.md)) and the copy
`001EE8E0`. SMAA takes four constants from the quality integer at `+0x184`:

| `+0x184` | `SMAA_THRESHOLD` | `SMAA_MAX_SEARCH_STEPS` | `SMAA_MAX_SEARCH_STEPS_DIAG` | `SMAA_CORNER_ROUNDING` |
|---|---|---|---|---|
| 1 | 0.15 | 4 | 0 | 0 |
| 2 | 0.10 | 8 | 0 | 0 |
| 3 | 0.10 | 16 | 8 | 25 |
| 4 | 0.05 | 32 | 16 | 25 |
| any other | 0.15 | 4 | 0 | 0 |

The thresholds are `008F30F4`, `008C5F6C` and `008F30E8` (`00192975` to `0019299A`); the step counts
are immediates (`001929FA` to `00192A2F`).

### The post-process command

`0018EEE0` builds the post-process command each frame: it allocates a `0xF0`-byte block
(`001A1470`), fills it from the `0x4A8`-byte render-parameter block (`00193D50`, kept at `01F7F5F0`)
and enqueues it on the render command list (`005FEA50`). [YEBIS post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md)
gives the per-frame library calls its work function `00193DA0` makes with it.

| Command | From the block | Meaning |
|---|---|---|
| `+0x00`, `+0x08`, `+0x10` | render targets | the three targets `006CBEA0` hands the library |
| `+0x18`, `+0x1C` | `+0xF4`, `+0xF8` | glare luminance and threshold (`00194310`) |
| `+0x20` | `+0x110` | depth-of-field enable |
| `+0x21` | `+0x164` | a byte the depth-of-field call also passes |
| `+0x24`, `+0x28` | `+0x114`, `+0x118` | focus distance and aperture f-number (`00194250`) |
| `+0x2C` | `+0x120` | the value the cutscene loader sets to 35.0 |
| `+0x30`, `+0x34` | `+0x168`, `+0x16C` | two floats the depth-of-field call also passes |
| `+0x99` | | set when the first argument's `+0x4A1` is set or `+0xDB9` of the object `00189120` returns differs from its value last frame (`+0x48C`) |
| `+0x9A` | `+0x4A2` | the linear-tonemap byte |
| `+0xDC` to `+0xE4` | `+0x480` to `+0x488` | three floats |

When the first argument's `+0x124` is 2 the focus distance is its `+0x128`; when it is 1 and `+0x128`
is positive, both the distance and an f-number computed from it (scaled by block `+0x11C`) are used,
eased over ten frames when they change (`0018EF95` to `0018F2BD`).

While the block's byte `+0x164` is set, the render pass list `00187950` marks the point at `+0x168`
and `+0x16C` (`0018D320`) on screen. It maps the point from 0 to 1 into clip space with y flipped
and calls `001862B0(manager, x, y)`, which reserves 0x50 bytes of a render-thread callback
(`005FEB30` on the manager's device) for `001890A0`: four vertices (x ± 0.1, y) and (x, y ± 0.1)
with w = 1.0 and the colour (0, 1, 0, 1), drawn with `006215A0` in mode 1 between `00628570(ctx,
0, 1)` and `00628570(ctx, 1)`.

The depth-of-field pass `00191560` works only while the block's byte `+0x349` is set and `+0x110`
is clear. `001828C0(on, mode, a, b, c, d, e, f, g)` sets the byte and the pass's values through
`001944D0`: `+0x349` = (`on` ≠ 0), the mode at `+0x360` (the pass tests it for 1 and 2) and the
other values at `+0x34C`, `+0x350`, `+0x354`, `+0x358`, `+0x35C`, `+0x364` and `+0x368`. Its caller is `00474710`, which
passes 1 and values from its own record each time it runs.

The cutscene loader `001C3D50` reads `mGlareThreshold` and `mGlareLuminance` into `00194310`
(`001C42E4`) and `EnableDof`, `mDofFocusDistance` and `mDofApertureFnumber` into `00194250` with
35.0 (`001C42A1`); the area loader `001C7940` calls both setters with the enable fixed at 1.

### The PPFX features the game leaves off

`006CBD20` initialises the library once with the flag word `0x20001` (`006CBE02`).
`CPostEffect::Initialize` (`006FF900`) stores it at `+0x20C` (`006FFB8C`) and derives one byte per
optional feature from it (`006FFE56` to `00700071`, with `r12` = 1):

| Flag bit | Byte | Feature (from its setter's message) | Setter |
|---|---|---|---|
| `0x40000` | `+0x131` | lens distortion | `00709C90` |
| `0x40000` | `+0x133` | aperture Airy disc | `0070A060` |
| `0x40000` | `+0x134` | motion blur | `0070A480` |
| `0x40000` | `+0x137` | geometry blur | `0070A410` |
| `0x40000` | `+0x138` | Gaussian blur | `0070A0F0` |
| `0x40000` | `+0x13C`, `+0x13D` | heat shimmer, heat-shimmer particles | `0070A350` |
| `0x40000` | `+0x142` | chromatic aberration | `00709F40` |
| `0x4000000` | `+0x13A` | ambient occlusion | `0070AA80` |
| `0x8000000` | `+0x140`, `+0x141` | post-process antialias, its distance falloff | `0070A1F0`, `0070A260` |

Each setter first compares its byte with 0 and refuses with "Initialize() with PFXINIT_… flag".
`0x20001` holds none of the three bits, so all of these PPFX features stay off; the game's own AO and
anti-aliasing passes above are separate code. Depth of field and glare are not behind these bits.

### The PPFX effect catalogue

The library's texture utility `CTextureUtil` is a reference-counted singleton (`02EA1590`, count
`02EA1598`): `007142F0` allocates `0x22360` bytes on first use. `Initialize` acquires it
(`00700972`) and calls its slot 0, `007307A0`, which calls `0072D820`, which calls
`TEXSHADERSET::CreateEffect` `0072A320` (`0072D872`) and abandons the sequence on a non-zero result.

`0072A320` (13,547 bytes) loads the compiled effect once through `0078A120`, returns the loader's
error unchanged when that fails, and then fetches a handle for each technique and uniform it names:
325 `tech_` names and 36 uniforms, among them `fParam_FocusDistance`, three HDR formats
(`fParam_HDRFormatFactor_LOGRGB`, `_REINHARDRGB`, `_RGBALUM`) and the vignette and lens-distortion
parameters. Its ten log calls are gated by `01F3BA80` together with `02EA0B40` or `01F3BA90`.

The largest technique family is `tech_DepthOfField` (53 names), then
`tech_CompositeColorAndAlphaEffectsMask` (20), `tech_GenerateNormalDepth` (15) and
`tech_TemporalAntialias` (14). The helper `0072DCF0`, called at 65 sites with a count `n`, drops the
name's last character, appends `1` to `n`, and fetches each of those under 22 suffixes: none, and 21
HDR conversions such as `_REINHARDRGB_RGB` and `_LOGRGBLUM_RGBFAST` (table `02EA2250`).

Handles are 32-bit values stored from `this + 8` (`0072A496`), with one run from `this + 0x1AA10`
(`0072BA97`); the last is at `+0x221D8`. The placed slots are in
[the handle layout](post-processing-ppfx-handle-layout.tsv).

### The render-pass registries

Two sets of named pass records exist side by side:

- The static array at `01F2D6A0`: 56 records of `0x20` bytes, `{ name, 0, 0, 0xFFFFFFFF }`, the last
  one named `NULL`. It holds `Opaque`, `OpaqueRGB`, `Transparent`, `DeferredRender`, the map passes
  (`DefaultMapRenderPass…`, `AteGequalFbonly…`, `WaterPassFor…`), the character passes
  (`ChrOpaque…`) and the twelve game passes' records above.
- The runtime registry headed at `02CBF998`: 60 static initialisers each call
  `005DC6F0(record, name, 0)`, which fills the record (name, next 0, flag, `+0x18` = -1) and calls
  `005FDCB0`.
  - `005FDCB0` returns `0x11` for a null name and `0x12` for a duplicate name; otherwise it pushes
    the record at the head and returns 0. `005DDD60` unlinks a record at exit.
  - The 60 names are PhyreEngine's passes, from `ShadowRender` and `RenderFXAA` to the atmosphere
    precompute and `RenderText_*` passes
    ([registry](post-processing-runtime-render-pass-registry.tsv),
    [teardown wrappers](post-processing-render-pass-registry-60.tsv)).

### The frame-marker table

`001D62D0` allocates the `0xF778`-byte object at `01F82C80` at start-up. It is a GPU timing table:
`001D5970` creates one timestamp-disjoint query and five rings of 128 timestamp queries
(`01F81838`, `01F81880`). `00187950` queues `001D5FD0` on the render command list, and each call
ends the next timestamp query of the current ring (`001D6250`). `001D6000`, also from `00187950`,
stamps an `END` marker (`001D6040`), reads back the ring from the frame before
(`001D5650`), stores the measured time as a double at `+0xD70` of the object `001D50D0` returns, and
clears the marker list (`001D6170`).

`001D6170` runs `001D5970` again while the object's byte `+0x15` is clear. Besides the queries,
`001D5970` lays out two rows of bar quads in the object, six vertices of 16 bytes each, after
resetting all `0x324` vertices of each row to `(0, 0, 0, 1)`:

- colours: `001D6370(obj, i, r, g, b)` writes colour `i`, divided by 255 with alpha 1.0, to the six
  vertices at `+0x92B8 + i × 0x60` (row 1), and `001D6630` at `+0xC4F8` (row 2). Entries 0 and 1 get
  `(0x86, 0x7B, 0x6F)` and `(0x86, 0x64, 0x6D)`, 2 to 4 get `(0xF6, 0xFF, 0x06)`, and 5 to 133 cycle
  through the ten colours at `01DFCFC0`: cyan, red, yellow, blue, purple, olive, green, navy, magenta
  and maroon;
- positions: `001D64D0(obj, i, x, y, w, h)` (row 1, vertices from `+0x2E38`) and `001D6790` (row 2,
  from `+0x6078`) write the two triangles of the rectangle with depth `−0.1 × i`. Quad 0 starts at
  `(+0x04, +0x0C)` (row 2: `+0x10`) with width `1 − +0x00` and height `+0x08`, quad 1 follows it,
  and quads 2 to 4 are ticks 0.01 wide and 0.08 high, 0.04 lower, starting 0.01 left of 0, 1 and 2
  widths from the start.

## Layouts

The render-parameter block fields this page uses (`0x4A8` bytes at `01F7F5F0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0F4` | `f32` | glare luminance | +`0x0F8`  f32     glare threshold |
| `110` | `u8` | depth-of-field enable | +`0x114`  f32     focus distance |
| `118` | `f32` | aperture f-number | +`0x11C`  f32     f-number scale |
| `120` | `f32` | lens (35.0) |  |
| `184` | `i32` | SMAA quality |  |
| `198` | `u8` | EnableAO |  |
| `1A8` | `f32[6]` | SAO bias, radius, intensity: Chr, then Sce |  |
| `1C4` | `f32[6]` | HBAO angle bias, radius, contrast: Chr, then Sce |  |
| `344` | `i32` | 1 = HBAO |  |
| `3E8` | `u8` | anti-aliasing built | +`0x3E9`  u8      anti-aliasing configured |
| `4A3` | `u8` | PostAA is SMAA |  |

## Shipped data

| Fact | Value |
|---|---|
| shader-constant names in the twelve passes | 89 calls of `0018D240` |
| `0072A320` | 379 string references, 325 `tech_` names, 36 uniforms; 358 direct calls to 22 targets |
| static pass array | 56 records, `01F2D6A0` to the `NULL` record at `01F2DD80` |
| runtime pass registry | 60 registration sites, 60 names, 60 records |
| access tables | [CPostEffect](post-processing-cposteffect-accesses.tsv), [its initialise descriptor](post-processing-ppfx-init-descriptor-accesses.tsv), [the frame-marker object](post-processing-frame-marker-singleton-accesses.tsv) |

## State

| Address | Holds |
|---|---|
| `01F7F5F0` | the render-parameter block (also cached at `01F81300`) |
| `02EA0B70` | the `CPostEffect` object the PPFX calls run on |
| `02EA1590`, `02EA1598` | the `CTextureUtil` singleton and its reference count |
| `02CBF998` | the head of the runtime render-pass registry |
| `01F82C80` | the frame-marker table |

## Modding notes

- AO strength is two independent sets, characters and scenery; change both halves of each pair.
- HBAO angle biases are authored in degrees, SAO biases in units the pass divides by 600.
- Turning on a PPFX feature from the table above needs a different initialise flag word at
  `006CBE02`; the setters refuse otherwise.
- A shader that drops a constant name keeps working: the pass skips the missing constant.

## Related

- [YEBIS post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md): the library, its
  start-up and the per-frame calls.
- [Phyre post-effect classes](../PhyreEngine/phyre-post-effect-classes.md): the FXAA
  object and the shared copy pass `001EE8E0`.
- [The frame](../PhyreEngine/the-frame.md): where the passes fall in a frame.
- [Graphics settings](../Engine-Core/graphics-settings.md): the scene keys and the block.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the HDAO, PostAA, Glare and
  DepthofField options.
- [Render command list](render-command-list.md): where the command and the markers are queued.
- [Render parameters and shader assets](render-parameters-and-shader-assets.md): the shader files.
