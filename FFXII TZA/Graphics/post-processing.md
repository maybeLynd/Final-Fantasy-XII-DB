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
| `0x0018F6B0` | brightness, from the Brightness option (`0x0018F6F1`) | `BrightBlend` | `g_brightPara`, `g_BrightTex` | `0x00187950` |
| `0x0018F8F0` | colour grading | `ColorCorrection` | `apply_MainTex`, `colorR`, `colorG`, `colorB`, `percent`, `gamma`, `resolution` | `0x00187950`, `0x0018EEE0`, `0x001F3090` |
| `0x0018FE00` | single-step pass | `Opaque`, `Transparent` | `ColorBuffer`, `ColorBufferSampler`, `SingleStepOffset` | `0x001F3090` |
| `0x00190260` | font border | `FontBorderWidth`, `FontBorderHeight` | `FontBorderSetting`, `FontBorderColor`, `SingleStepOffset` | `0x00212E70` |
| `0x00190760` | HBAO | `HBAOGenerateAO` | `g_NumSteps`, `g_NumDir`, `g_FocalLen`, `g_HBAOResolution`, `g_RChr`, `g_AngleBiasChr`, `g_ContrastChr`, `g_RSce`, `g_AngleBiasSce`, `g_ContrastSce`, `g_fadeoutScale`, `g_maskBorder`, `tLinDepth`, `tNormal`, `projInfo` | `0x0018F510` |
| `0x00191130` | depth mask | `Opaque`, `Transparent`, `DebugMask` | `MaskDepth` | `0x001F32B0` |
| `0x00191560` | depth of field | `Opaque`, `DOFWriteOnePass` | `materialColor`, `customPosition`, `ColorBuffer`, `MaskBuffer`, `dofShift` | `0x001F3440` |
| `0x00191E90` | scalable AO (SAO) | `SAOGenerateAO` | `projScale`, `radiusChr`, `biasChr`, `intensityChr`, `radiusSce`, `biasSce`, `intensitySce`, `g_fadeoutScale`, `CS_Z_buffer`, `tNormal`, `projInfo`, `widthAO`, `heightAO` | `0x0018F510` |
| `0x001925D0` | SMAA | `ColorEdgeDetection`, `BlendingWeightCalculation`, `NeighborhoodBlending` | `areaTex`, `searchTex`, `edgesTex`, `blendTex`, `colorTex`, `smaa_resolution`, `SMAA_RT_METRICS`, `SMAA_THRESHOLD`, `SMAA_MAX_SEARCH_STEPS`, `SMAA_MAX_SEARCH_STEPS_DIAG`, `SMAA_CORNER_ROUNDING` | `0x00191DA0` |
| `0x001930F0` | subsurface-scattering blur | `SSS` | `useBigKernel`, `blendAmount`, `sssBlur`, `dir`, `SingleStepOffset`, `colorTex`, `depthTex`, `normalTex` | `0x001F3740` |
| `0x001EE8E0` | colour-buffer copy | `Opaque`, `OpaqueRGB`, `OpaqueDepth` (`0x01F82E68`), `OpaqueGray` (`0x01F82E88`) | `ColorBuffer`, `ColorBufferSampler`, `ColorBufferOffset` | 17 sites |

The samplers `LinearSampler`, `PointSampler` and `samNearest` are named too. The shaders are the
`.fx.phyre` assets on [Render parameters and shader assets](render-parameters-and-shader-assets.md).

`0x0018F6B0(block, ctx, texture)` returns 0 at once while the block's byte `+0x1F4` is clear (`0x0018F6DD`).
Otherwise it reads the Brightness option, the dword `+0x10` of the game settings `[0x01F82D20]`, keeps it as
a float `v` at `+0x1F8` (`0x0018F6F1`-`0x0018F6F9`) and writes `g_brightPara = (v - 50.0) / 100.0` (`0x008F3130`,
`0x008F3134`, `0x0018F76A`-`0x0018F772`) under the size test below, returning 3 when it does not fit
(`0x0018F7BF`).

`g_BrightTex` gets the texture `[texture]`, null when the byte at `texture + 8` is set, through
`0x001945B0` (`0x0018F7DD`-`0x0018F80D`): the record's first dword `0xFF` is replaced by the descriptor's type, `0x43`
or `0x44`, else `0x42` (`0x00194643`-`0x00194661`), and a non-zero status from `0x001945B0` (5 for another type, 3 when
it does not fit) ends the pass with that value (`0x0018F812`-`0x0018F814`).

The pass then calls `0x0060D4F0(ctx, 0, 0)`, `0x0060DB50(ctx, 0)`, `0x0060D190(ctx, 0.0, 0.0, 0.0, 0.0)` and
`0x005FEFD0(ctx, 0)`, stores the `BrightBlend` record `0x01F2DD40` at `ctx + 0x80` (`0x0018F86A`), submits with
`0x0060B980` (`0x0018F8AE`) and ends with `0x00600A60(ctx, 0)` (`0x0018F8BD`). The first of these calls to return
non-zero ends the pass with its value (`0x0018F812`-`0x0018F8C4`); otherwise the pass returns 0.

The copy pass draws a mesh that `0x001EEC80` builds once, from the render-manager installer
`0x00186CD0`. It loads `./GameData/D3D11/ArtData/shaders/CopyBuffer.fx.phyre` (`0x0019CB20`,
`0x0063DA50`, `0x0063B010`), creates a `0xA0`-byte cluster at `0x01F82E60` (`0x00633040`), and builds in it
with `0x00649C20` the same one-triangle full-screen mesh the movie player builds with `0x001B72B0`,
keeping the mesh instance at `0x01F82E58`. The instance's material set (`+0x20`) gets one material
made from the asset's first `PEffectVariant` (`0x02CB6780`, `0x00600120`). `0x001EE8E0` draws that
instance (`0x0060B980`).

`0x001EEC80` looks for the variant in the asset's list at `+0x38`: it takes the first entry whose class
`+0x50`, or a class reached from it through `+0x78`, is `0x02CB6780` and whose dword `+0x74` is above 0
(`0x001EECEE`-`0x001EED35`). With no such entry it builds nothing: no cluster, no mesh, and `0x01F82E60`
and `0x01F82E58` are left as they were (`0x001EED08`, `0x001EED3A`, `0x001EED5A`). The variant is the first
object of that entry (`0x001EED40`-`0x001EED70`).

The cluster comes from `0x00584740(0xA0)` and is `0x00633040` of that block, or 0 when the block is null;
the mesh call `0x00649C20` follows with no test of it (`0x001EED74`-`0x001EEDA4`).

The material is the answer of `0x00600120(variant, cluster)` (`0x001EEDAB`-`0x001EEDBA`), and the material
set is the array `0x0063A990(cluster, 1, 0x02D3A440, 0)` answers. When its count is not 1 the body empties it,
freeing its block with `0x00584730` when bit `0x80000000` of the count dword is clear, and stores a
count of 1 (`0x001EEDD2`-`0x001EEE1E`). The material goes to the array's `+0x08` and the array's address
to the instance's `+0x20` (`0x001EEE24`-`0x001EEE4A`).

### Writing a constant

`0x0018D240(shader, name)` returns the parameter's descriptor or null. It returns null for a null name, and
otherwise searches the shader's two tables of `0x18`-byte entries in turn: `[+0x40]` entries at `[+0x48]`, then
`[+0x50]` entries at `[+0x58]` (each count masked with `0x7FFFFFFF`). It compares the name byte by byte with
the entry's name pointer `+0x08` less its bit `0x1`, and the first match is the descriptor (`0x0018D24B`-`0x0018D310`).

A pass then copies its value
into the constant block with `memcpy` (`0x00861EBA`) only when the descriptor's offset (`u16 +0x10`)
plus its size (`u16 +0x12` masked to 13 bits) fits the block's first dword and the offset is at
least 4 (`0x001929A7` to `0x001929E1`). A constant the shader does not declare is skipped silently.

`0x00194540(block, descriptor, sampler)` writes a sampler constant under the same test: the
descriptor's size of the record {`0x47`, sampler, 0} goes to its offset, and a constant that does
not fit returns 3. `0x001EE8E0` uses it for `ColorBufferSampler`, and the passes `0x0018F8F0`,
`0x0018FE00`, `0x00190260`, `0x00191560` and `0x001930F0` call it too.

### Ambient occlusion

`0x0018F510(block, …)` copies the colour buffer first (`0x001EE8E0`) unless the block's `+0x1E9` is set.
The copy takes `[r]` of the target `r = 0x00186660(0x00189120())`, null when the byte at `r + 8` is set, into
`[+0x2B0]` (`0x0018F54F`-`0x0018F578`). On every call the AO targets `+0x2D0` and `+0x2D8` are then reset to
`+0x280` and `+0x288` (`0x0018F57D`-`0x0018F595`), and the function returns 0 on every path (`0x0018F694`).

It runs AO only when the HDAO option (`+0x28` of the game settings, 1 half resolution, 2 full) is
on and the block's `+0x198` (`EnableAO`) is set. The option is read from `[0x01F82D20]`, and any value other
than 1 and 2 leaves AO off (`0x0018F5A3`-`0x0018F5C4`):

- with `+0x344` = 1 it runs HBAO (`0x00190760`), after swapping in the targets `+0x2A0` / `+0x2A8` when
  HDAO is at half resolution and `+0x1E8` is clear; they go into `+0x2D0` / `+0x2D8` (`0x0018F5F7`-`0x0018F60C`);
- otherwise it runs SAO (`0x00191E90`);
- either way it then runs the blur and composite `0x0018E4A0`, with the same first five arguments and 0 in
  place of the sixth (`0x0018F66B`-`0x0018F685`).

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
`0x001EE8E0`. With either of the two bytes clear it returns without drawing (`0x00191DBF`, `0x00191DCC`).

SMAA is a tail jump (`0x00191E0B`): `0x001925D0` gets the render-parameter block `0x00193D50` returns in place of
the first argument, the second and third arguments as they came, and the target `0x001867C0(0x00189120())`
(`0x00191DDB`-`0x00191DF3`). FXAA gets the block's `+0x378`, the second argument, `[+0x290]`, `[arg3]` (null
when the byte at `arg3 + 8` is set) and 1 (`0x00191E17`-`0x00191E38`). The copy then gets `[[+0x290]]` (null when
the byte at `[+0x290] + 8` is set), the third argument, a zeroed record and 0 (`0x00191E3D`-`0x00191E70`).

SMAA takes four constants from the quality integer at `+0x184`:

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
eased over ten frames (`0x0018EF94` to `0x0018F2BD`).

The ease starts when the slot's byte `+0x152` is 0, its byte `+0x150` is set and
the float the slot saved at `+0x138` is below 0 (`0x0018F0FF`-`0x0018F11B`), not on a change of the distance.
Outside mode 1 with a positive distance `0x0018EEE0` also saves `+0x128` at the slot's `+0x138` and the block's `+0x114`
and `+0x118` at `+0x140` and `+0x148`, sets `+0x150` and clears `+0x152`, which ends an ease in progress
(`0x0018F263`-`0x0018F2B5`). On every path it then copies the command's `+0x20`, `+0x24` and `+0x28` to the slot's
`+0xFC`, `+0x100` and `+0x108` (`0x0018F2BD`-`0x0018F2EA`).

With `d` the distance and
`c(x, lo, hi)` a clamp, the f-number is `(1 + 0.33 c(4 - d, -2, 3) + 0.7 c(2.9 - d, 0, 2.7) +
0.15 c(d - 4.4, 0, 4) - 0.2 c(d - 6, 0, 3)) x [block +0x11C]`. While easing, each frame moves both values by
`(target - current) / (10 x [0x01DFE0B4] - n)`, `n` counting the frames already eased.

The script verb `unkCall_5bd` (`0x05BD`, helper `0x002E30D0`; [verb
table](../Scripts-And-Script-Commands/verb-table.md)) holds the focus on one bone of a model.
`0x00382B50(render index, bone, distance)` stores the three at `0x02AEDFA0`, `0x02AEDFA4` and `0x02AEDFA8`
(`0x00382B58`, `0x00382B5E`, `0x00382B50`); `0x00382910` sets `0x02AEDFA0` to -1 at boot (`0x003829A4`), and the
verb's off form and the game-over reset pass -1. Each model's render update `0x0053AB50` calls
`0x00382BF0` with its record index (`0x0053CF85`), which does nothing unless the index is
`0x02AEDFA0`'s (`0x00382C09`).

For the held model, when its render record exists and its `+0x284` is non-zero, `0x00382BF0` takes
the origin of bone `[0x02AEDFA4]` (`0x00421E20(record, bone, 0, matrix)`, `0x00382C4B`), transforms it, with
w = 1.0, by the camera matrix copy `0x02CA7F80` (`0x00202B70`) and requests mode 2 with `[0x02AEDFA8]` minus the
point's camera-space z (`0x00182870(2, distance, 0)`, `0x00382CA7`-`0x00382CBC`).

`0x00182870` hands the
request to the render parameters (`0x00194490`: `+0x124` the mode, `+0x128` the distance), so the
focus follows the bone. When the record is gone or its `+0x284` is 0, it requests mode 0 with
-1.0 and sets `0x02AEDFA0` to -1 (`0x00382CD9`-`0x00382CEB`).

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
passes 1 each time it runs.

It passes its record's `+0x1C` as the mode, its `+0x04`, `+0x08`, `+0x0C`, `+0x14` and `+0x18` as `a`-`e`, and the
working camera's near `[0x02AED560]` and far `[0x02AED564]` as `f` and `g` (`0x00474850`-`0x0047488A`, `0x00474771`, `0x0047477D`,
`0x0047487F`, `0x00474878`, `0x0047489C`). `0x001828C0` calls `0x001944D0`, which puts `f` and `g` at `+0x364` and `+0x368`
(`0x00194506`, `0x0019450E`), only when `0x00193D50` returns the render-parameter block; it returns 0 only when the block's
first allocation fails (`0x001828E6`, `0x00193D69`-`0x00193D7B`).

The cutscene loader `0x001C3D50` reads `mGlareThreshold` and `mGlareLuminance` into `0x00194310`
(`0x001C42E4`) and `EnableDof`, `mDofFocusDistance` and `mDofApertureFnumber` into `0x00194250` with
35.0 (`0x001C42A1`); the area loader `0x001C7940` calls both setters with the enable fixed at 1.

### The PPFX features the game leaves off

`0x006CBD20` initialises the library with the flag word `0x20001` (`0x006CBE02`) on every call, each of which
creates a context; only the allocator and licence set-up behind the flag `0x01F31F70` runs once
(`0x006CBD3F`-`0x006CBD68`).
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
`TEXSHADERSET::CreateEffect` `0x0072A320` (`0x0072D872`) and abandons the sequence on a negative result.

`0x007142F0` returns the instance `[0x02EA1590]` and sets the count to `count + 1` when the count is above 0
(`0x00714307`, `0x00714356`). Otherwise it allocates through `0x006DA880` with the allocator `[0x01F3BA68]`, tagged
`GPUClassUtil.h` line `0x49` (`0x00714314`-`0x00714327`), builds the object with `0x0072F870(object, 0)`
(`0x0071433B`), stores it at `0x02EA1590` and sets the count to 1 (`0x00714345`-`0x0071434E`); a failed allocation
stores null and still sets the count to 1.

`0x0072D820`, `TEXSHADERSET::InitializeDevice()` by its log lines (`0x00DA51D0`), skips `CreateEffect` when the
low byte of its third argument is set (`0x0072D868`). A negative `CreateEffect` result is logged as
"CreateEffect() failed" and returned (`0x0072D87B`-`0x0072D8B8`); a zero or positive one goes on.

`0x0072D820` then calls `m_pEffect->OnResetDevice()`, slot `0x38` of the object at `this + 0` (`0x0072D8D9`),
and returns a negative result from it the same way (`0x0072D8E0`); otherwise it calls slot `0x88` of that
object with `[this + 0xA0]` and the record {1.0, −1.0, 0} (`0x0072D937`-`0x0072D965`). With no object at
`this + 0` it skips both calls (`0x0072D8D0`). It returns 0 on success (`0x0072D99F`).

`0x0072A320` (13,547 bytes) loads the compiled effect once through `0x0078A120`, returns the loader's
error unchanged when that fails, and then fetches a handle for each technique and uniform it names. Its body
references 364 distinct strings: 325 `tech_` names and 36 uniforms, among them `fParam_FocusDistance`, three HDR formats
(`fParam_HDRFormatFactor_LOGRGB`, `_REINHARDRGB`, `_RGBALUM`) and the vignette and lens-distortion
parameters. Its ten log calls are gated by `0x01F3BA80` together with `0x02EA0B40` or `0x01F3BA90`.

The largest technique family is `tech_DepthOfField` (53 names), then
`tech_CompositeColorAndAlphaEffectsMask` (20), `tech_GenerateNormalDepth` (15) and
`tech_TemporalAntialias` (14). The helper `0x0072DCF0`, called at 65 sites with a count `n`, drops the
name's last character, appends `1` to `n`, and fetches each of those under 22 suffixes: the empty suffix, and 21
HDR conversions such as `_REINHARDRGB_RGB` and `_LOGRGBLUM_RGBFAST` (table `0x02EA2250`).

Handles are 32-bit values stored from `this + 8` (`0x0072A496`). One run is addressed from `this + 0x1AA10`
(`0x0072BA97`): a five-pass loop (`0x0072BAB0`-`0x0072C5C3`) fills 25 slots from `+0x1A9C0` to `+0x1AA20`, and
other loops fill arrays of 8 and 4. The last slot is at `+0x221D8`. The placed slots are in
[the handle layout](post-processing-ppfx-handle-layout.tsv): 352 handle stores, fewer than the names, because a
family row fetches several names under one count and suffix table.

### Columns of post-processing-ppfx-handle-layout.tsv

| Column | Holds |
|---|---|
| `this_offset` | where the handle lands, as an offset from the start of the object: the store's displacement plus its base (`r14` = `this + 8`, `rsi` = `this + 0x1AA10`, `rdi` = `this + 0x220E4`); `+ 4*i (i 0-n)` marks an array a loop fills. All 352 offsets are distinct, from `0x8` to `0x221D8`; the 257 inline rows match the `mov` after the call at `site`, and 93 of the 95 family rows match the `lea rdx` before it |

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

### Columns of the two registry tables

| Column | Holds |
|---|---|
| `band` | in post-processing-runtime-render-pass-registry.tsv, the address range the record lies in: `game` for the 10 records from `0x01F81220` to `0x01F83040`, `phyre-post-effect` for the 43 from `0x02D36DA0` to `0x02D38000`, `text` for the 7 `RenderText_*` records from `0x02E5BEA8` to `0x02E5BF68` |
| `node` | in post-processing-render-pass-registry-60.tsv, the record the row's `teardown` unlinks: its first instruction is `lea rcx, [node]` and its second `jmp 0x005DDD60`, on all 60 rows |
| `registration_site` | the static initialiser that registers the record: `xor r8d, r8d`, `lea rdx, [name]`, `lea rcx, [node]`, `call 0x005DC6F0`, then `lea rcx, [teardown]` and a tail jump to the exit registrar `0x00808B90`, on all 60 rows |
| `flag_at_plus10` | the flag the initialiser passes in `r8d`, which `0x005DC6F0` stores at record `+0x10`: 0 on all 60 rows |

### Columns that mark selected pass records

| Column | Holds |
|---|---|
| `selected_by_001E2AF0` | in post-processing-named-render-pass-array.tsv, `yes` on the 19 records, indexes 4 to 22, whose address `0x001E2AF0`, the function `MapOrderedObject`'s execute slot forwards to, stores at `[rsi + 0x80]` (`0x001E3111` to `0x001E3347`). It picks one record from its flag bytes `+0xC1` to `+0xC4` and `+0xB8` and the dword it reads through `+0x78`: the `DefaultMapRenderPass…` records (indexes 4 to 12), the `AteGequalFbonly…` records and `NoBlendWithAlphaClip` (13 to 17), and the `WaterPassFor…` records (18 to 22). Every load of an array record in `0x001E2AF0` is one of these 19 |
| `submitted_by_a_post_effect_worker` | in post-processing-runtime-render-pass-registry.tsv, `yes` on the 29 records that one of the eleven post-effect workers stores at `[ctx + 0x80]` before it submits with `0x0060B980`: the eleven functions from `0x00652940` to `0x0065BA00` that call `0x0060B980`. All 29 are in the `phyre-post-effect` band; 6 of them are the `…Inverted` and `…Combine` variants a worker picks with a conditional jump or `cmov` before the same store. The game-band records `VideoScreen`, `MapShadowRender`, `OpaqueDepth`, `OpaqueGray`, `ShadowRender`, `ShadowRenderWithRef` and `AlphaModeRender` are stored the same way by the game's own functions `0x001B76E0`, `0x001E2AF0`, `0x001EE8E0` and `0x001F5D70`, and are left blank |

### The frame-marker table

`0x001D62D0` allocates the `0xF778`-byte object at `0x01F82C80` at start-up. It is a GPU timing table:
`0x001D5970` creates one timestamp-disjoint query and five rings of 128 timestamp queries
(`0x01F81838`, `0x01F81880`). `0x00187950` queues `0x001D5FD0` on the render command list, and each call
ends the next timestamp query of the current ring (`0x001D6250`). `0x001D6000`, also from `0x00187950`,
stamps an `END` marker (`0x001D6040`).

`0x001D5650` reads back ring `(r + 1) mod 5` while ring `r` takes this frame's timestamps, then advances `r`
(`0x01F81834`, `0x01F81848` under State). Called once a frame, the ring it reads was written four frames earlier,
once all five have been written. `0x001D6000` then stores the measured time as a double at `+0xD70` of the object `0x001D50D0` returns, and
clears the marker list (`0x001D6170`).

`0x001D62D0` allocates only while `0x01F82C80` is null (`0x001D62F0`), through `0x00210EC0`, and leaves null there
when the allocation fails (`0x001D6357`). It sets the layout floats `+0x00` = 0.2, `+0x04` = −0.8, `+0x08` =
0.04, `+0x0C` = 0.8 and `+0x10` = 0.7 (`0x001D6306`-`0x001D6321`): quad 0 starts at `(−0.8, 0.8)` in row 1 and
`(−0.8, 0.7)` in row 2, with width `1 - 0.2` = 0.8 and height 0.04. It clears the word `+0x14`, the byte
`+0x16` and `+0x1C` to `+0x2B`, and sets `+0x2C30` to −1 and `+0x2C34` to 0 (`0x001D6328`-`0x001D6341`).

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
| `+0x00` | `void*` | targetA | the first of the three render targets `0x006CBEA0` hands the library: `0x001867B0` of the render manager (`0x0018EF3E`); passed as the second argument of `0x0065E5C0` (`0x00193F55`) and as the third argument of the context creation `0x0065E5A0` (`0x00193DDF`); with `+0x98` set the builder also runs the colour-grading pass `0x0018F8F0` on it (`0x0018F36D`) and copies it with `0x001EE8E0` (`0x0018F3B0`) |
| `+0x08` | `void*` | targetB | the second of the three render targets: `0x00186660` of the render manager (`0x0018EF4E`); the third argument of `0x0065E5C0` (`0x00193F51`) |
| `+0x10` | `void*` | targetC | the third render target: `0x001868F0`(manager, 0) when `+0x98` and the builder's fifth argument are set, otherwise `0x001867C0`(manager) (`0x0018EF68`-`0x0018EF90`); the fourth argument of `0x0065E5C0` (`0x00193F4A`) |
| `+0x18` | `f32` | glareLuminance | glare luminance, the block's `+0xF4` (`0x0018EFF3`); with the Glare option on (`0x01F82D20` `+0x34`) it is the first float `0x006CC1E0` hands CPostEffect::SetGlareParameters (`0x00193E52`), which stores it at CPostEffect `+0x6E4` |
| `+0x1C` | `f32` | glareThreshold | glare threshold, the block's `+0xF8` (`0x0018EFFC`); the second float of the glare call (`0x00193E4D`), stored at CPostEffect `+0x6E0` |
| `+0x20` | `u8` | dofEnable | depth-of-field enable, the block's `+0x110` (`0x0018F00C`); passed as the enable byte of the depth-of-field call `0x0065E610` while the DepthofField option (`0x01F82D20` `+0x30`) is on (`0x00193EE6`); the builder also copies it into the block's per-slot byte `+0xFC` (`0x0018F2C4`) |
| `+0x21` | `u8` | autoFocus | the auto-focus byte: the block's `+0x164` (`0x0018F30C`), which also makes the render pass list `0x00187950` draw the focus-point marker; passed to the depth-of-field call (`0x00193ED8`), where a set byte turns the library's auto-focus on (`0x0070EC00`), aims it at `+0x30`/`+0x34` (`0x0070F3C0`) over 0.1 to 100 (`0x0070F300`) and takes the auto-focus distance (`0x006DC650`) as the focus distance (`0x006CC0C5`-`0x006CC131`) |
| `+0x22` | `u8[2]` | pad022 | written and read by no function; nothing fixes its width |
| `+0x24` | `f32` | focusDistance | focus distance (`0x00194250`): the block's `+0x128` or `+0x114`, or the eased value, by the mode at `+0x124` of the first argument (`0x0018F19A`, `0x0018F229`, `0x0018F257`); passed at `0x00193EE1` |
| `+0x28` | `f32` | apertureFNumber | aperture f-number: in mode 1 with a positive `+0x128` the f-number computed with the focus distance, or its eased value (`0x0018F22E`, `0x0018F1B7`); otherwise the block's `+0x118` (`0x0018F25A`-`0x0018F260`), mode 2 included; passed at `0x00193EDC` |
| `+0x2C` | `f32` | lens | the block's `+0x120`, the value the cutscene loader sets to 35.0 (`0x0018F2F7`); `0x00193DA0` does not read it and passes the constant 35.0 (`0x008F312C`, `0x00193EF0`) instead |
| `+0x30` | `f32` | focusPointX | the x of the focus point, the block's `+0x168` (`0x0018F300`): the point the marker draws and the auto-focus samples (`0x00193ED3`, `0x006CC0F0`) |
| `+0x34` | `f32` | focusPointY | the y of the focus point, the block's `+0x16C` (`0x0018F309`) (`0x00193ECB`, `0x006CC0E7`) |
| `+0x38` | `u8[12]` | pad038 | written and read by no function; nothing fixes its width |
| `+0x44` | `f32` | flareScreenX | the screen x of the bit `0x20` lens flare, the block's `+0x36C` (`0x0018F3FB`), stored by `0x00182830` through `0x00194470` from the flare draw `0x00461270`; read by no function in `0x00193DA0` or its callees |
| `+0x48` | `f32` | flareScreenY | the screen y of the same flare, the block's `+0x370` (`0x0018F404`); read by no function in `0x00193DA0` or its callees |
| `+0x4C` | `f32[10]` | lightShaft | the light-shaft values, the block's `+0xC4` to `+0xEB` (`0x0018F407`-`0x0018F445`): colour R, G, B (`lightShaftColorR`/`G`/`B`) and 0 for the alpha, `lightShaftLength`, `lightShaftGlareRatio`, `lightShaftMaskDepthThereshold`, `lightShaftAngleAttenuation`, `lightShaftNoiseMask` and `lightShaftNoiseFrequency` as set by `0x00194400` (`0x001C8AF5`); read by no function in `0x00193DA0` or its callees |
| `+0x74` | `f32[8]` | lightShaftRing | the light-shaft diffraction ring, the block's `+0xA4` to `+0xC3` (`0x0018F448`-`0x0018F476`): `lightShaftDiffractionRing`, `…Radius`, `…Attenuation`, `…SpectrumOrder`, then `…OuterColorR`/`G`/`B`/`A`, as set by `0x00194370` (`0x001C8D33`); read by no function in `0x00193DA0` or its callees |
| `+0x94` | `f32` | lightShaftOn | the block's byte `+0xEE` as a float (`0x0018F3DF`-`0x0018F3ED`); both writers of that byte, `0x001943C0` and `0x0018D640`, end with 0 on every path (`0x001943DA`, `0x0018D65A`), so the value is 0.0; read by no function in `0x00193DA0` or its callees |
| `+0x98` | `u8` | deviceByte | the device byte `+0xD48` of the PhyreEngine application object `0x00796E20`() (`0x0018EF57`); when set the builder runs the colour-grading pass and the copy (`0x0018F323`-`0x0018F3B6`) and `0x00193DA0` passes 2.0 and mode 2 to `0x006CC170` (`0x00193E71`-`0x00193E87`) |
| `+0x99` | `u8` | reinitialise | set when the first argument's `+0x4A1` is set or `+0xDB9` of the object `0x00189120` returns differs from its value last frame (`+0x48C`) (`0x0018EF94`-`0x0018EFAF`); when set `0x00193DA0` calls `0x006CC2F0` on the existing context instead of creating one (`0x00193DB1`) |
| `+0x9A` | `u8` | linearTonemap | the linear-tonemap byte, the block's `+0x4A2` (`0x0018F316`); with `+0x98` clear `0x00193DA0` passes mode 1 when it is set and -1 when it is clear to `0x006CC170` (`0x00193E8F`-`0x00193EAE`) |
| `+0x9B` | `u8[1]` | pad09B | written and read by no function; nothing fixes its width |
| `+0x9C` | `f32[16]` | cameraMatrix | the camera matrix, the block's `+0x440` to `+0x47F` (`0x0018F47D`-`0x0018F4AE`), which `0x00189CE0` copies from the camera `0x001AC950` through `0x001941F0`; its address goes to `0x006CC1F0` (`0x00193E0A`), which hands the previous matrix to `0x00707220` and this one to `0x00706F60` (CPostEffect `+0x654` and `+0x5D4`) |
| `+0xDC` | `f32` | cameraNear | the block's `+0x480` (`0x0018F4BB`), default 0.1 (`0x0018D007`), the camera's `+0xCBC` (`0x00189EA2`); the first float of `0x006CC260` (`0x00193E2E`), which becomes CPostEffect `+0x5A4` |
| `+0xE0` | `f32` | cameraFar | the block's `+0x484` (`0x0018F4C7`), default 1000.0 (`0x0018D011`), the camera's `+0xCC0`; the second float of `0x006CC260` (`0x00193E26`), CPostEffect `+0x5A8` |
| `+0xE4` | `f32` | cameraAngle | the block's `+0x488` (`0x0018F4D3`), default 0.785398 (π / 4, `0x0018D01B`), the camera's `+0xCC4`; the third float of `0x006CC260` (`0x00193E1B`), which halves it (`0x006CC29A`); `0x00706C20` halves it again and stores its tangent at CPostEffect `+0x5B0` (`0x00706C26`-`0x00706C98`) |
| `+0xE8` | `u8[8]` | pad0E8 | written and read by no function; nothing fixes its width |

The render-parameter block fields this page uses (`0x4A8` bytes, kept at `0x01F7F5F0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0F4` | `f32` |  | glare luminance |
| `+0x0F8` | `f32` |  | glare threshold |
| `+0x110` | `u8` |  | depth-of-field enable |
| `+0x114` | `f32` |  | focus distance |
| `+0x118` | `f32` |  | aperture f-number |
| `+0x11C` | `f32` |  | f-number scale |
| `+0x120` | `f32` |  | lens (35.0) |
| `+0x184` | `i32` |  | SMAA quality |
| `+0x198` | `u8` | EnableAO |  |
| `+0x1A8` | `f32[6]` |  | SAO bias, radius, intensity: Chr, then Sce |
| `+0x1C4` | `f32[6]` |  | HBAO angle bias, radius, contrast: Chr, then Sce |
| `+0x344` | `i32` |  | 1 = HBAO |
| `+0x3E8` | `u8` |  | anti-aliasing built |
| `+0x3E9` | `u8` |  | anti-aliasing configured |
| `+0x4A3` | `u8` | PostAA | is SMAA |

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

The frame-marker table keeps four words of its own beside the timestamp-disjoint query `0x01F81838` and the query rings
`0x01F81880` (128 queries per ring, `0x400` bytes apart). They are 0 at load (the zero-filled tail of `.data`). The
context `0x01F81840` is called through its slots `0xD8`, `0xE0` and `0xE8` (Begin, End and GetData of a Direct3D 11
device context).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F81830` | `f32` | 0 | the timestamp frequency in ticks per second: `0x001D6040` ends the disjoint query, polls GetData until it answers and stores the frequency it returns as a float (`0x001D60E3`-`0x001D614C`); both this and the Begin in `0x001D6170` run only while the frequency's magnitude is below `1e-6` (`0x001D60BC`-`0x001D60E1`, `0x001D620A`-`0x001D622F`), so it is measured once | `0x001D6040` (`0x001D614C`) | `0x001D6040` (`0x001D60BC`); `0x001D6170` (`0x001D620A`); `0x001D5650`, the divisor of each tick difference (`0x001D5786`, `0x001D5885`) |
| `0x01F81834` | `i32` | 0 | the ring that takes this frame's timestamps, 0 to 4: `0x001D5650` advances it to `(ring + 1) mod 5`, a signed division by 5 (`0x001D58A7`-`0x001D58D4`) | `0x001D5970`, 0 (`0x001D5A77`); `0x001D5650` (`0x001D58D4`) | `0x001D5650` (`0x001D565B`, `0x001D58A7`); `0x001D6250` (`0x001D6264`, `0x001D629B`), which ends the next query of this ring and marks the ring written in the dword at `0x01F81850` + 4 × ring |
| `0x01F81840` | `void*` | 0 | the device context the queries run on: the pointer at `+0x110` of the object `0x00624670` returns (`0x001D5A13`-`0x001D5A1F`) | `0x001D5970` (`0x001D5A1F`) | `0x001D5650` (`0x001D572D`, `0x001D57C7`, `0x001D5822`); `0x001D6040` (`0x001D60E3`, `0x001D6100`); `0x001D6170` (`0x001D6231`); `0x001D6250` (`0x001D628B`) |
| `0x01F81848` | `i32` | 0 | the ring read back this frame, `(0x01F81834 + 1) mod 5`: `0x001D5650` reads that ring only when its written dword at `0x01F81850` is 1 (`0x001D5698`) and gets each query with GetData (`0x001D5720`-`0x001D5751`) | `0x001D5650` (`0x001D5691`) | `0x001D5650` (`0x001D5720`, `0x001D577D`, `0x001D5815`) |

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Developer: `0x00796E20` is called by `0x001C2F50`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Platform online achievements: `0x00796E20` is called by `0x008655A0`; those functions are documented on
  [steam integration](../Steam-And-Achievements/steam-integration.md).
- Script VM: `0x002E30D0` is called by `0x0034DEE0`; `0x00382B50` is called by `0x00356D40`; those functions are documented on
  [debug menu](../Engine-Core/debug-menu.md).
