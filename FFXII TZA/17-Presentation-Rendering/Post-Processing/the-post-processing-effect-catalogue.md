---
system: The post-processing effect catalogue — TEXSHADERSET::CreateEffect
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: CodeDomain:ThirdParty.Rendering.PPFX — no PrimaryOwner (middleware)
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-post-processing-catalogue-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The post-processing effect catalogue

> `0072A320` is the second-largest uncited function in the executable, 13,547 bytes, and it does
> exactly one thing: it names **every post-processing effect FFXII: The Zodiac Age can run** —
> 325 shader techniques and 36 uniforms — and fetches a handle for each.

## 1. What the player sees

**Every visual effect applied after the scene is drawn, listed by name.**

When the camera pulls focus in a cutscene and the background dissolves into soft round highlights,
that is bokeh depth of field. When you spin the camera quickly and the image smears, that is motion
blur. The star-shaped spikes off water and armour, the haze rising off Dalmasca's sand, the way the
picture darkens toward the corners, the grain that appears as the image is tone-mapped down from
high dynamic range — all of it is post-processing, and **this one function is where the engine
learns the name of every piece of it.**

It runs once, ~~at start-up~~ on the first frame the post-process command runs *(corrected 2026-10-02, OPUS: `00193DA0`+0x31..+0x48 calls create only when `0065E5B0` reports the library absent; UQ-226)*. It loads a compiled shader file, then walks a list of 361 names and asks
the graphics layer for a handle to each. Nothing it does is visible on its own. What it produces is
the index the rest of the post-processing layer uses for the whole session — and what it *tells us*
is the complete inventory, which nobody had written down.

**The headline for a modder is the list itself** (§4). It answers, by name and without guessing:

- **Depth of field** is the largest family by far — 63 techniques *(scope named 2026-10-02, OPUS: §4's Depth list - 53 `tech_DepthOfField`, 8 `tech_DepthFromDofFactor`, 2 `tech_DepthEncode`)* — with a separate **Bokeh** family
  of 40 on top of it. This game spends more shader variety on defocus than on anything else.
- **Motion blur** has 50.
- **Ambient occlusion** is present and it is **Alchemy SSAO**, named outright.
- **Anti-aliasing** is **FXAA 2**.
- **Tone mapping** ships three HDR encodings — `LOGRGB`, `REINHARDRGB`, `RGBALUM`.
- **Glare, bloom, lens ghosts, cross filter, corona, chromatic aberration, heat haze, vignette,
  colour grading by matrix, and temporal accumulation** are all present, each with its own family.

And one direct link to gameplay data: the uniform **`fParam_FocusDistance`** is the shader end of
the **`mDofFocusDistance`** value that
[the cutscene depth-of-field sidecar](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
reads out of `JsonData/CutScenes/<name>.json`. **A number a scene author typed into a text file
arrives here as a shader parameter.**

## 2. Native mechanism

### The function names itself

Four log strings inside the body identify it beyond argument:

```
==== TEXSHADERSET::CreateEffect() ====
TEXSHADERSET::CreateEffect(): IGPUEffect::CreateEffectFromFile() failed (0x%x: %s).
TEXSHADERSET::CreateEffect(): IGPUEffect::CreateEffectFromFile() succeeded.
TEXSHADERSET::CreateEffect(): get parameter handles ...
```

with the source file and build date the middleware was compiled from:

```
..\src\GPU\GPUTextureUtil.cpp(%d) : PPFX:
..\src\GPU\GPUTextureUtil.cpp(%d) : Feb 18 2016 PPFX ERROR:
```

**PPFX is a post-processing library; `TEXSHADERSET` is its shader-set object.** This document does
not need to identify the vendor to be useful, and does not assert one.

### The shape

```c
if (logEnabled && verbose) {
    log("..\\src\\GPU\\GPUTextureUtil.cpp(%d) : PPFX: ", 0x90B);
    log("==== TEXSHADERSET::CreateEffect() ====\n");
}
...
hr = CreateEffectFromFile(device, <name>, "_LUMINANCE_REMAP_S1.pso", 0);
if (hr != 0) {
    log("... failed (0x%x: %s).\n", hr, describe(hr));
    return hr;                       /* the whole post-processing layer is unavailable */
}
log("... succeeded.\n");
log("get parameter handles ...\n");

/* then 332 registrations, in seven shapes */   // <- corrected 2026-10-02, OPUS - 219 of the 332 are string operations (section 8's UQ-225 answer); the registrations are mostly inline
registerHandle (this, &this->slot, "tech_Name");
registerArray  (this, &this->slot, "tech_Name_Tn", count);
...
```

**The gates matter for anyone trying to observe this.** Every log line is behind two globals
(`01F3BA80` plus one of `02EA0B40` / `01F3BA90`), so in a retail run this function is silent — the
strings are present but never printed.

### Seven registration shapes, 332 calls

> **CORRECTED 2026-09-18 (FABLE, UQ-225):** the four most-called rows of this table are the library's string class - destructor, constructor, assignment, concatenation - not registration helpers, and the single-name lookups are inline calls through the effect interface (224 through slot `+0x60`, 33 through `+0x48`). The per-target call counts below stand; the heading's reading of them does not.
>
> **Extended 2026-09-29 (FABLE, adopting OPUS's falsification pass 1, P11):** `00715CC0` (112 B, 8 sites), the string truncate the family helpers call with length − 1 after construction, is a fifth string utility. The string class therefore accounts for **227 of the 332** sites (91 + 48 + 40 + 40 + 8). None of the five reaches the lookup slots; every family helper does (`_index/candidates/ppfx-falsification-pass-1-0929/`).

The body makes **358 direct calls** to **22 real targets** (*corrected 2026-09-12 from 364 / 24 — see the falsification pass*). The ~~registration helpers~~ callees *(corrected 2026-10-02, OPUS: the four most-called are the string class, the correction above)*, by call count:

| helper | body | calls | shape |
|---|---:|---:|---|
| `00715C70` | 70 B | **91** | the smallest and most used |
| `0072DCF0` | 718 B | **65** | takes a count — an array of handles under one name |
| `007157A0` | 256 B | **48** | |
| `007182F0` | 82 B | **40** | |
| `00719380` | 207 B | **40** | |
| `0072EB20` | 215 B | **26** | takes a count |
| `00715CC0` | 112 B | 8 | |
| `0072DFD0` | 716 B | 4 | two-dimensional family (`_TSn_n`) |
| `0072DAC0`, `0072EC00` | 547 / 492 B | 3 each | |
| `0071A380`, `0072E5B0` | 320 / 386 B | 2 each | |

plus `006DF480` (the logger) ×10, `sprintf` ×8, and single calls to ~~the effect loader, `memset`,~~
~~`free` and the stack-cookie check~~ eight targets *(corrected 2026-10-02, OPUS: every direct call of `0072A320` recounted, 358 sites to 22 targets: `0078A530`, `0078A120` the effect loader, `0078A960`, `0071B3C0`, `00861EC0` (`memset`), `00715360`, `0072E940` and `00808C40` the cookie check, once each)*.

**The count argument is the variant multiplier.** A call like

```c
FUN_0072dcf0(this, &this->slot, "tech_DepthOfField_BackgroundLayerMaskT1_Sn", 0x19);
```

registers ~~**25** handles~~ **25 × 22 = 550** handles under one name *(corrected 2026-10-02, OPUS: `0072DCF0` formats `%s%d` for each counted variant (`0072DCF0`+0x90..+0xA4) and registers each one under all 22 suffixes of the table at `02EA2250` (`0072DCF0`+0x1EC `lea rdi, [02EA2250]`, +0x1F3 `lea esi, [rbp + 0x16]`); the handle slots of `ppfx-handle-layout.tsv` step `0x898` bytes from `0xDB60` to `0xE3F8`)* — the `_Sn` suffix is a family of shader variants, and the
literal says how many. Observed counts include 4, 8, 17 (`0x11`) and 25 (`0x19`).

**The complete list (2026-09-29, OPUS's falsification pass 1, P4):** across the two counted helpers' 91 sites, the count is always one of 1, 4, 8, 16, 17, 25, 32, 33 or 64, with 15, 2, 42, 6, 8, 5, 4, 8 and 1 sites respectively. That ~~registers **1,172 handles** in all~~ names 1,172 counted variants; the 640 of them at `0072DCF0`'s 65 sites carry 22 handles each, so the two helpers register 14,612 handles *(corrected 2026-10-02, OPUS: `0072DCF0` formats `%s%d` for each counted variant (`0072DCF0`+0x90..+0xA4) and registers each one under all 22 suffixes of the table at `02EA2250` (`0072DCF0`+0x1EC `lea rdi, [02EA2250]`, +0x1F3 `lea esi, [rbp + 0x16]`))*, and every site's count resolves.

### The suffix grammar

The names are systematic, and the suffix tells you what varies:

| suffix | meaning |
|---|---|
| `_Sn` | *n* sampler/shader variants, count passed as the argument |
| `_Tn` | *n* texture-count variants |
| `_TSn_n` | both, two-dimensional |
| `_T1_Sn`, `_T3_S8`, `_T4_S8` | texture count fixed, sampler count varying |
| `_USNORM` | a variant for unsigned-normalised render targets |
| `_A` / `_R` / `_G` / `_B` | per-channel variants (the `Alpha` family) |

The uniform names carry their type in the prefix: `f` scalar float, `af` float array, `v` vector,
`m44` 4×4 matrix, `am44` matrix array, `asamp2D` / `asamp3D` sampler arrays.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0072A320` | `TEXSHADERSET_CreateEffect` | 13,547 B | **this document**: load the effect, register 325 techniques and 36 uniforms; interior verified 2026-09-17 (SWE2-FRONTIER) — first `006DF480` log call at [`0072A383`](../../_index/ADDRESS-INDEX.md), then `0078A530` (interior read 2026-09-17, SWE2-FRONTIER: 1,057 B, call-free — a `movups` block-copy leaf, descriptor fields staged at [`0078A586`](../../_index/ADDRESS-INDEX.md)) at `0072A3A6` |
| `0072D820` | — | 396 B | its only caller |
| `0078A120` | — | 273 B | ~~`IGPUEffect::CreateEffectFromFile` wrapper~~ `IGPUEffect::CreateEffect` *(corrected 2026-10-02, OPUS: `0078A120`+0xEA logs `IGPUEffect::CreateEffect()`; `0078A240`+0x109 is the `CreateEffectFromFile` string)*; called once |
| `006DF480` | — | 137 B | the PPFX logger; 160 callers image-wide |
| `00715C70` | — | 70 B | ~~registration helper~~ the string destructor *(corrected 2026-10-02, OPUS: UQ-225, 2026-09-18)*, 91 call sites here |
| `0072DCF0` | — | 718 B | registration helper with a count argument, 65 sites |
| `007157A0` | — | 256 B | registration helper, 48 sites |
| `007182F0` | — | 82 B | registration helper, 40 sites |
| `00719380` | — | 207 B | registration helper, 40 sites |
| `0072EB20` | — | 215 B | registration helper with a count argument, 26 sites |
| `0072DFD0` | — | 716 B | two-dimensional family helper, 4 sites |

Addresses are Ghidra image base `0x00120000`.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01F3BA80` | PPFX log master gate | `.data` | non-zero enables any logging from this function |
| `02EA0B40` | PPFX verbose gate | `.data` | gates the informational lines |
| `01F3BA90` | PPFX error gate | `.data` | gates the two error lines |
| `00D9F498` | — | `.rdata` string | `"==== TEXSHADERSET::CreateEffect() ====\n"` |
| `00D9F810` | — | `.rdata` string | the `CreateEffectFromFile() failed` line |
| `00D9FAC0` | — | `.rdata` string | the `succeeded` line |
| `00D9FB40` | — | `.rdata` string | `"...: get parameter handles ...\n"` |

## 4. The catalogue

**325 technique names in 35 families**, every one LEA'd directly from this function's body. This is
the complete list; nothing is elided.

### Depth (63)

```
tech_DepthEncode_RGBA8
tech_DepthEncode_RVALUE
tech_DepthFromDofFactor_A
tech_DepthFromDofFactor_B
tech_DepthFromDofFactor_G
tech_DepthFromDofFactor_R
tech_DepthFromDofFactor_USNORM_A
tech_DepthFromDofFactor_USNORM_B
tech_DepthFromDofFactor_USNORM_G
tech_DepthFromDofFactor_USNORM_R
tech_DepthOfField_BackgroundLayerMaskMakeColorDenseMaskT1_Sn
tech_DepthOfField_BackgroundLayerMaskMakeColorDenseMaskT1_USNORM_Sn
tech_DepthOfField_BackgroundLayerMaskMakeColorDenseT1_Sn
tech_DepthOfField_BackgroundLayerMaskMakeColorDenseT1_USNORM_Sn
tech_DepthOfField_BackgroundLayerMaskMakeColorMaskT1_Sn
tech_DepthOfField_BackgroundLayerMaskMakeColorMaskT1_USNORM_Sn
tech_DepthOfField_BackgroundLayerMaskMakeColorT1_Sn
tech_DepthOfField_BackgroundLayerMaskMakeColorT1_USNORM_Sn
tech_DepthOfField_BackgroundLayerMaskT1_Sn
tech_DepthOfField_BackgroundLayerMaskT1_USNORM_Sn
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCastLutT1_Sn
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCastLut_AVALUE
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCastLut_BVALUE
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCastLut_GVALUE
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCastLut_RGBA8
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCastLut_RVALUE
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCastT1_Sn
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCast_AVALUE
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCast_BVALUE
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCast_GVALUE
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCast_RGBA8
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCast_RVALUE
tech_DepthOfField_BlurFactorAlphaFromDepthTextureTypeCast_USNORM_ABGR8
tech_DepthOfField_CompositeBlurLevelsFrontBlur_TSn_n
tech_DepthOfField_CompositeBlurLevelsFrontBlur_USNORM_TSn_n
tech_DepthOfField_CompositeBlurredLevelsFrontBlur_Tn
tech_DepthOfField_CompositeBlurredLevelsFrontBlur_USNORM_Tn
tech_DepthOfField_CompositeBlurredLevels_Tn
tech_DepthOfField_CompositeBlurredLevels_USNORM_Tn
tech_DepthOfField_CompositeMaskedBlurLevels_TSn_n
tech_DepthOfField_CompositeMaskedBlurLevels_USNORM_TSn_n
tech_DepthOfField_CompositeScatteredLevels
tech_DepthOfField_CompositeScatteredLevels_Blur
tech_DepthOfField_CompositeScatteredLevels_BlurEclipse
tech_DepthOfField_CompositeScatteredLevels_BlurRad
tech_DepthOfField_CompositeScatteredLevels_BlurRadEclipse
tech_DepthOfField_CompositeScatteredLevels_Eclipse
tech_DepthOfField_ForegroundLayerMaskMakeColorDenseMaskT1_Sn
tech_DepthOfField_ForegroundLayerMaskMakeColorDenseMaskT1_USNORM_Sn
tech_DepthOfField_ForegroundLayerMaskMakeColorDenseT1_Sn
tech_DepthOfField_ForegroundLayerMaskMakeColorDenseT1_USNORM_Sn
tech_DepthOfField_ForegroundLayerMaskMakeColorMaskT1_Sn
tech_DepthOfField_ForegroundLayerMaskMakeColorMaskT1_USNORM_Sn
tech_DepthOfField_ForegroundLayerMaskMakeColorT1_Sn
tech_DepthOfField_ForegroundLayerMaskMakeColorT1_USNORM_Sn
tech_DepthOfField_ForegroundLayerMaskT1_Sn
tech_DepthOfField_ForegroundLayerMaskT1_USNORM_Sn
tech_DepthOfField_FrontBlurBlendFactor
tech_DepthOfField_FrontBlurBlendFactorDilation
tech_DepthOfField_FrontBlurBlendFactorDilationMask
tech_DepthOfField_FrontBlurBlendFactorMask
tech_DepthOfField_NormalizeBackgroundBlurFactor
tech_DepthOfField_NormalizeBackgroundBlurFactor_USNORM
```

### Motion (50)

```
tech_MotionBlurCameraRotatePerspectiveFalloffBiLinearT1_Sn
tech_MotionBlurCameraRotatePerspectiveFalloffBiLinear_SM3_T1_Sn
tech_MotionBlurCameraRotatePerspectiveFalloffT1_Sn
tech_MotionBlurCameraRotatePerspectiveFalloff_SM3_T1_Sn
tech_MotionBlurCameraRotatePerspectiveT1_Sn
tech_MotionBlurCameraRotatePerspective_SM3_T1_Sn
tech_MotionBlurMakeCameraVelocityFalloff_A
tech_MotionBlurMakeCameraVelocityFalloff_B
tech_MotionBlurMakeCameraVelocityFalloff_G
tech_MotionBlurMakeCameraVelocityFalloff_R
tech_MotionBlurMakeCameraVelocityFalloff_RGBA8
tech_MotionBlurMakeCameraVelocityOverwriteFalloff_A
tech_MotionBlurMakeCameraVelocityOverwriteFalloff_B
tech_MotionBlurMakeCameraVelocityOverwriteFalloff_G
tech_MotionBlurMakeCameraVelocityOverwriteFalloff_R
tech_MotionBlurMakeCameraVelocityOverwriteFalloff_RGBA8
tech_MotionBlurMakeCameraVelocityOverwrite_A
tech_MotionBlurMakeCameraVelocityOverwrite_B
tech_MotionBlurMakeCameraVelocityOverwrite_G
tech_MotionBlurMakeCameraVelocityOverwrite_R
tech_MotionBlurMakeCameraVelocityOverwrite_RGBA8
tech_MotionBlurMakeCameraVelocity_A
tech_MotionBlurMakeCameraVelocity_B
tech_MotionBlurMakeCameraVelocity_G
tech_MotionBlurMakeCameraVelocity_R
tech_MotionBlurMakeCameraVelocity_RGBA8
tech_MotionBlurVelocityClampT2_Sn
tech_MotionBlurVelocityClamp_SM3_T2_Sn
tech_MotionBlurVelocityDirClampT2_Sn
tech_MotionBlurVelocityDirClamp_SM3_T2_Sn
tech_MotionBlurVelocityDirDepthClampT2_Sn
tech_MotionBlurVelocityDirDepthClamp_SM3_T2_Sn
tech_MotionBlurVelocityDirDepthInnerscreenClampT2_Sn
tech_MotionBlurVelocityDirDepthInnerscreenClamp_SM3_T2_Sn
tech_MotionBlurVelocityDirDepthInnerscreenT2_Sn
tech_MotionBlurVelocityDirDepthInnerscreen_SM3_T2_Sn
tech_MotionBlurVelocityDirDepthT2_Sn
tech_MotionBlurVelocityDirDepth_SM3_T2_Sn
tech_MotionBlurVelocityDirInnerscreenClampT2_Sn
tech_MotionBlurVelocityDirInnerscreenClamp_SM3_T2_Sn
tech_MotionBlurVelocityDirInnerscreenT2_Sn
tech_MotionBlurVelocityDirInnerscreen_SM3_T2_Sn
tech_MotionBlurVelocityDirT2_Sn
tech_MotionBlurVelocityDir_SM3_T2_Sn
tech_MotionBlurVelocityInnerscreenClampT2_Sn
tech_MotionBlurVelocityInnerscreenClamp_SM3_T2_Sn
tech_MotionBlurVelocityInnerscreenT2_Sn
tech_MotionBlurVelocityInnerscreen_SM3_T2_Sn
tech_MotionBlurVelocityT2_Sn
tech_MotionBlurVelocity_SM3_T2_Sn
```

### Bokeh (40)

```
tech_BokehBlurCenterAlpha_EclipseSeparateXY_S
tech_BokehBlurCenterAlpha_Eclipse_S
tech_BokehBlurCenterAlpha_RadEclipseSeparateXY_S
tech_BokehBlurCenterAlpha_RadEclipse_S
tech_BokehBlurCenterAlpha_RadSeparateXY_S
tech_BokehBlurCenterAlpha_Rad_S
tech_BokehBlurCenterAlpha_S
tech_BokehBlurCenterAlpha_SeparateXY_S
tech_BokehBlurConditional_EclipseSeparateXY_S
tech_BokehBlurConditional_Eclipse_S
tech_BokehBlurConditional_RadEclipseSeparateXY_S
tech_BokehBlurConditional_RadEclipse_S
tech_BokehBlurConditional_RadSeparateXY_S
tech_BokehBlurConditional_Rad_S
tech_BokehBlurConditional_S
tech_BokehBlurConditional_SeparateXY_S
tech_BokehBlurSmallAlphaConditional_EclipseSeparateXY_S
tech_BokehBlurSmallAlphaConditional_Eclipse_S
tech_BokehBlurSmallAlphaConditional_RadEclipseSeparateXY_S
tech_BokehBlurSmallAlphaConditional_RadEclipse_S
tech_BokehBlurSmallAlphaConditional_RadSeparateXY_S
tech_BokehBlurSmallAlphaConditional_Rad_S
tech_BokehBlurSmallAlphaConditional_S
tech_BokehBlurSmallAlphaConditional_SeparateXY_S
tech_BokehBlurSmallAlpha_EclipseSeparateXY_S
tech_BokehBlurSmallAlpha_Eclipse_S
tech_BokehBlurSmallAlpha_RadEclipseSeparateXY_S
tech_BokehBlurSmallAlpha_RadEclipse_S
tech_BokehBlurSmallAlpha_RadSeparateXY_S
tech_BokehBlurSmallAlpha_Rad_S
tech_BokehBlurSmallAlpha_S
tech_BokehBlurSmallAlpha_SeparateXY_S
tech_BokehBlur_EclipseSeparateXY_S
tech_BokehBlur_Eclipse_S
tech_BokehBlur_RadEclipseSeparateXY_S
tech_BokehBlur_RadEclipse_S
tech_BokehBlur_RadSeparateXY_S
tech_BokehBlur_Rad_S
tech_BokehBlur_S
tech_BokehBlur_SeparateXY_S
```

### Scatter (32)

```
tech_ScatterCoc
tech_ScatterCocLevel
tech_ScatterCocLevelClamp
tech_ScatterCocLevelClamp_Eclipse
tech_ScatterCocLevelClamp_EclipseSeparateXY
tech_ScatterCocLevelClamp_Rad
tech_ScatterCocLevelClamp_RadEclipse
tech_ScatterCocLevelClamp_RadEclipseSeparateXY
tech_ScatterCocLevelClamp_RadEclipseSeparateXY_Lerp
tech_ScatterCocLevelClamp_RadEclipse_Lerp
tech_ScatterCocLevelClamp_RadSeparateXY
tech_ScatterCocLevelClamp_RadSeparateXY_Lerp
tech_ScatterCocLevelClamp_Rad_Lerp
tech_ScatterCocLevelClamp_SeparateXY
tech_ScatterCocLevel_Eclipse
tech_ScatterCocLevel_EclipseSeparateXY
tech_ScatterCocLevel_Rad
tech_ScatterCocLevel_RadEclipse
tech_ScatterCocLevel_RadEclipseSeparateXY
tech_ScatterCocLevel_RadEclipseSeparateXY_Lerp
tech_ScatterCocLevel_RadEclipse_Lerp
tech_ScatterCocLevel_RadSeparateXY
tech_ScatterCocLevel_RadSeparateXY_Lerp
tech_ScatterCocLevel_Rad_Lerp
tech_ScatterCocLevel_SeparateXY
tech_ScatterCoc_Eclipse
tech_ScatterCoc_EclipseSeparateXY
tech_ScatterCoc_Rad
tech_ScatterCoc_RadEclipse
tech_ScatterCoc_RadEclipseSeparateXY
tech_ScatterCoc_RadSeparateXY
tech_ScatterCoc_SeparateXY
```

### Composite (20)

```
tech_CompositeColorAndAlphaEffectsMask_A
tech_CompositeColorAndAlphaEffectsMask_A_A
tech_CompositeColorAndAlphaEffectsMask_A_B
tech_CompositeColorAndAlphaEffectsMask_A_G
tech_CompositeColorAndAlphaEffectsMask_A_R
tech_CompositeColorAndAlphaEffectsMask_B
tech_CompositeColorAndAlphaEffectsMask_B_A
tech_CompositeColorAndAlphaEffectsMask_B_B
tech_CompositeColorAndAlphaEffectsMask_B_G
tech_CompositeColorAndAlphaEffectsMask_B_R
tech_CompositeColorAndAlphaEffectsMask_G
tech_CompositeColorAndAlphaEffectsMask_G_A
tech_CompositeColorAndAlphaEffectsMask_G_B
tech_CompositeColorAndAlphaEffectsMask_G_G
tech_CompositeColorAndAlphaEffectsMask_G_R
tech_CompositeColorAndAlphaEffectsMask_R
tech_CompositeColorAndAlphaEffectsMask_R_A
tech_CompositeColorAndAlphaEffectsMask_R_B
tech_CompositeColorAndAlphaEffectsMask_R_G
tech_CompositeColorAndAlphaEffectsMask_R_R
```

### Generate (16)

```
tech_GenerateNormalDepth_NormGenMan_DepthA
tech_GenerateNormalDepth_NormGenMan_DepthB
tech_GenerateNormalDepth_NormGenMan_DepthG
tech_GenerateNormalDepth_NormGenMan_DepthR
tech_GenerateNormalDepth_NormGenMan_DepthRGBA8
tech_GenerateNormalDepth_NormGen_DepthA
tech_GenerateNormalDepth_NormGen_DepthB
tech_GenerateNormalDepth_NormGen_DepthG
tech_GenerateNormalDepth_NormGen_DepthR
tech_GenerateNormalDepth_NormGen_DepthRGBA8
tech_GenerateNormalDepth_NormRGB_DepthA
tech_GenerateNormalDepth_NormRGB_DepthB
tech_GenerateNormalDepth_NormRGB_DepthG
tech_GenerateNormalDepth_NormRGB_DepthR
tech_GenerateNormalDepth_NormRGB_DepthRGBA8
tech_GenerateNormalMap
```

### Mad (15)

```
tech_MadAlphaColorT2_A_Sn
tech_MadAlphaColorT2_B_Sn
tech_MadAlphaColorT2_G_Sn
tech_MadAlphaColorT2_R_Sn
tech_MadAlphaT1_Sn
tech_MadCocT2_Sn
tech_MadColorGradingLutT1_Sn
tech_MadLumGammaTn
tech_MadOffsetTn
tech_MadOffsetVignetteSimulateTn
tech_MadOffsetVignetteTn
tech_MadScalarWeightT1_Sn
tech_MadT1_Sn
tech_MadT2_Sn
tech_MadTn
```

### Temporal (14)

```
tech_TemporalAntialias
tech_TemporalAntialias_DynamicPixel
tech_TemporalAntialias_DynamicPixel_DepthA
tech_TemporalAntialias_DynamicPixel_DepthB
tech_TemporalAntialias_DynamicPixel_DepthG
tech_TemporalAntialias_DynamicPixel_DepthR
tech_TemporalAntialias_DynamicPixel_DepthRGBA8
tech_TemporalAntialias_Tonemap
tech_TemporalAntialias_Tonemap_DynamicPixel
tech_TemporalAntialias_Tonemap_DynamicPixel_DepthA
tech_TemporalAntialias_Tonemap_DynamicPixel_DepthB
tech_TemporalAntialias_Tonemap_DynamicPixel_DepthG
tech_TemporalAntialias_Tonemap_DynamicPixel_DepthR
tech_TemporalAntialias_Tonemap_DynamicPixel_DepthRGBA8
```

### Bright (9)

```
tech_BrightPassT1_THRESHOLD_LUMINANCE_REMAP_Sn
tech_BrightPassT1_THRESHOLD_LUMINANCE_Sn
tech_BrightPassT1_THRESHOLD_Sn
tech_BrightPassT1_VignetteSimulate_THRESHOLD_LUMINANCE_REMAP_Sn
tech_BrightPassT1_VignetteSimulate_THRESHOLD_LUMINANCE_Sn
tech_BrightPassT1_VignetteSimulate_THRESHOLD_Sn
tech_BrightPassT1_Vignette_THRESHOLD_LUMINANCE_REMAP_Sn
tech_BrightPassT1_Vignette_THRESHOLD_LUMINANCE_Sn
tech_BrightPassT1_Vignette_THRESHOLD_Sn
```

### Cross (7)

```
tech_CrossBilateralForSsao_MC_A_Sn
tech_CrossBilateralForSsao_MC_B_Sn
tech_CrossBilateralForSsao_MC_G_Sn
tech_CrossBilateralForSsao_MC_RGB_Sn
tech_CrossBilateralForSsao_MC_R_Sn
tech_CrossBilateralForSsao_MC_Sn
tech_CrossBilateralForSsao_Sn
```

### Lens (7)

```
tech_LensDistortion
tech_LensDistortionConv
tech_LensDistortionConv_Noise
tech_LensDistortionConv_Noise_Additive
tech_LensDistortionFalloff
tech_LensDistortion_Noise
tech_LensDistortion_Noise_Additive
```

### Color (5)

```
tech_ColorModulateByChannel_A
tech_ColorModulateByChannel_B
tech_ColorModulateByChannel_G
tech_ColorModulateByChannel_R
tech_ColorModulateByChannel_RGB
```

### Alpha (4)

```
tech_Alpha_A
tech_Alpha_B
tech_Alpha_G
tech_Alpha_R
```

### Feedback (4)

```
tech_Feedback
tech_Feedback_Blend
tech_Feedback_Blend_Matrix
tech_Feedback_Matrix
```

### Fxaa2 (4)

```
tech_Fxaa2
tech_Fxaa2_Falloff
tech_Fxaa2_Tonemap
tech_Fxaa2_Tonemap_Falloff
```

### Heat (4)

```
tech_HeatShimmerParticle_BlendAlpha_Sn
tech_HeatShimmerParticle_SM3_BlendAlpha_Sn
tech_HeatShimmerParticle_SM3_Sn
tech_HeatShimmerParticle_Sn
```

### Render (4)

```
tech_RenderSceneRect
tech_RenderSceneRect_InLinearDepth
tech_RenderSceneRect_InLinearDepth_OutReinhard
tech_RenderSceneRect_OutReinhard
```

### Glare (3)

```
tech_GlareGhost_PointSymmetryDistScaleT4_S8_TrimT1_S8
tech_GlareGhost_PointSymmetryT3_S8
tech_GlareGhost_PointSymmetryT4_S8_TrimT1_S8
```

### Analyze (2)

```
tech_AnalyzeIntensity
tech_AnalyzeIntensityTest
```

### Chromatic (2)

```
tech_ChromaticAberrationWithMask_Noise_Sn
tech_ChromaticAberrationWithMask_Sn
```

### Constant (2)

```
tech_ConstantColor
tech_ConstantColorO4
```

### Image (2)

```
tech_ImageSensorNoise
tech_ImageSensorNoise_Additive
```

### Light (2)

```
tech_LightShaftMask
tech_LightShaftMask_SM3
```

### Max (2)

```
tech_MaxColorLumGammaTn
tech_MaxColorTn
```

### Tex (2)

```
tech_TexCoordMadT1_Sn
tech_TexCoordOffsetMadTn
```

### Alchemy (1)

```
tech_AlchemySsao_T1_Sn
```

### Corona (1)

```
tech_Corona
```

### Dilate (1)

```
tech_DilateScatteredColorT1_S37
```

### Gradient (1)

```
tech_GradientMaskT1_S4
```

### Hybrid (1)

```
tech_HybridLogGamma
```

### Lateral (1)

```
tech_LateralChromaticAberration_Sn
```

### Median (1)

```
tech_MedianFilter_Separablex3x3
```

### Tonemap (1)

```
tech_TonemapHDR
```

### Transform (1)

```
tech_TransformMadT1_Sn
```

### Update (1)

```
tech_UpdateWaterHeight
```

### uniforms
```
afParam_TexCoordScaler8
afRGBA_Constant
afRGBA_Modulate
afRGBA_Offset
afUVWQ_TexCoordScaleOffset
afUV_TexCoordOffsetP32
afUV_TexCoordOffsetV16
afXY_DepthOfFieldLevelBlendFactor16
am44_TransformMatrix
asamp2D_Texture[0]
asamp2D_Texture[1]
asamp2D_Texture[]
asamp2D_VertexTexture[]
asamp3D_Texture[]
fParam_BrightPassRemapFactor
fParam_DepthCastScaleOffset
fParam_DepthOfFieldConvertDepthFactor
fParam_DepthOfFieldFactorScaleOffset
fParam_DepthOfFieldFactorThreshold
fParam_DepthOfFieldLayerMaskThreshold
fParam_DitherOffsetScale
fParam_FocusDistance
fParam_GammaCorrection
fParam_HDRFormatFactor_LOGRGB
fParam_HDRFormatFactor_REINHARDRGB
fParam_HDRFormatFactor_RGBALUM
fParam_PerspectiveFactor
fParam_ScreenSpaceScale
fParam_TonemapMaxMappingLuminance
fParam_VignettePowerOfCosine
fParam_VignetteSimulate
fRGBA_Constant
m44_ColorTransformMatrix
m44_PreTonemapColorTransformMatrix
m44_PreTonemapGlareColorTransformMatrix
vParam_LensDistortion
```

### log and diagnostic
```
'%s\n'
'..\\src\\GPU\\GPUTextureUtil.cpp(%d) : Feb 18 2016 PPFX ERROR: '
'..\\src\\GPU\\GPUTextureUtil.cpp(%d) : PPFX: '
'==== TEXSHADERSET::CreateEffect() ====\n'
'TEXSHADERSET::CreateEffect(): IGPUEffect::CreateEffectFromFile() failed (0x%x: %s).\n'
'TEXSHADERSET::CreateEffect(): IGPUEffect::CreateEffectFromFile() succeeded.\n'
'TEXSHADERSET::CreateEffect(): get parameter handles ...\n'
```
## 5. Call chain

```
start-up / device init   <- corrected 2026-10-02, OPUS - the first post-processed frame: 00193DA0+0x31..+0x48 (UQ-226)
  -> 0072D820                      the sole caller, 396 B
     -> 0072A320                   THIS FUNCTION
        -> 0078A120                CreateEffectFromFile("<base>" + "_LUMINANCE_REMAP_S1.pso")   <- corrected 2026-10-02, OPUS - 0078A120 is IGPUEffect::CreateEffect (its own log string at 0078A120+0xEA)
        -> 00715C70 x88            \   <- corrected 2026-10-02, OPUS - x91, 007157A0 x48, 00719380 x40 (the 2026-09-12 re-census); 332 calls, not ~323, and the first two are string utilities
           0072DCF0 x65             |  ~323 handle registrations
           007157A0 x45             |  across seven helper shapes,
           007182F0 x40             |  each taking a name and a
           00719380 x37             |  destination slot in the object
           0072EB20 x26             |
           ... four more x2-8      /
        -> 006DF480 x10            logging, gated off in retail
```

**Upstream:** one caller. This runs once; there is no per-frame path through it.

**Downstream:** nothing that draws. It fills an object with handles; the drawing code that uses
those handles is elsewhere and was not read here.

**Do not confuse with:** the functions catalogued in
[PPFX function identification](ppfx-function-identification.md). That document identifies PPFX
functions *as a population* by their strings; this one reads a single member and publishes what it
registers. The two do not overlap — that document does not cite `0072A320`.

## 6. Modding notes

- **This is the index, not the effect.** Changing a name here does not change what an effect does;
  it changes which shader technique the handle points at, and a name the effect file does not
  contain will fail to resolve.
- **The effect file is a `.pso` under `TexUtil_D3D11\`**, and the loader appends a variant suffix —
  the one literal present is `_LUMINANCE_REMAP_S1.pso`. Replacing techniques means rebuilding that
  file, not patching this function.
- **If `CreateEffectFromFile` fails the function returns early**, so a malformed effect file costs
  you the *entire* post-processing layer rather than one effect — the failure is all-or-nothing.
- **The logging is compiled in and gated off.** Setting `01F3BA80` and `02EA0B40` non-zero before
  this runs would print the banner, the load result and `get parameter handles ...` — the cheapest
  way to confirm the path is live in a running game.
- **`fParam_FocusDistance` is reachable from authored data** without touching code, through the
  cutscene JSON sidecar. That is the one parameter here with a documented data path.
- **Multiplayer / XIIOnline:** purely local presentation. Nothing here is authoritative state.

## 7. What is not known

- [x] **UQ-223.** **What any individual technique does**, beyond what its name says. 325 names were recovered;
      **zero shader bodies were read** — they are in the `.pso` file, not the executable.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md. See the register row.*
- [x] **UQ-224.** *(answered 2026-09-18, at the end of this item)* **The object layout.** Handles are written to `this + N` on a `longlong *`, so the slots are
      **qword indices, not byte offsets** — the observed range spans indices `0xFC`–`0x1015C`, but
      this document deliberately publishes no byte-offset map because none was verified.
      **ANSWERED 2026-09-18 (FABLE) for the handle slots: they are 32-bit handles at byte offsets, and the map is published.** The decompiler's *qword indices on a `longlong *`* were an artefact: every lookup in the catalogue body ends in `mov dword ptr [base + N], eax`, with `base` one of two registers fixed near the top - `this + 8` (`0072A496`) and, for one run of 35, `this + 0x1AA10` (`0072BA97`). [ppfx_handle_layout.py](members/ppfx_handle_layout.py) walks the body and emits [ppfx-handle-layout.tsv](members/ppfx-handle-layout.tsv): **352 lookups, 337 placed at a `this`-relative byte offset, 271 of those with their literal name, and no offset written twice.** The slots run from `this + 0xA0` to `this + 0x221D8` (`tech_HybridLogGamma`, the last), so the object is at least `0x221DC` bytes. A family call's destination is an array of `count` dwords starting at the listed offset; the body forms most counts as `lea r9d, [r15 + k]` with `r15d` holding 1 throughout, and with that read **92 of the 95 family counts resolve** (1 to 64 handles), none of which overlaps the next placed slot and 17 of which end exactly at it *(artefact corrected later the same day - its first issue printed -1 for 59 of them)*. *Not placed:* 15 lookups whose store is not within three instructions of the call, and the names of 66 lookups whose string is built at run time rather than a literal (all 33 of the slot-`+0x48` lookups among them). What lies between the handle runs was not read. Static, mechanical, reproducible.
- [x] **UQ-225.** **Which of the seven registration helpers means what.** They are distinguished here only by
      call count and by whether they take a count argument; no body was read.
      **ANSWERED 2026-09-18 (FABLE): four of the seven are not registration helpers at all - they are the library's string class - and the registrations themselves are mostly inline.** Bodies read: `00715C70` (70 B, 91 sites) is the string **destructor** - it frees the buffer at `+8` unless it is the shared empty buffer; `007157A0` (256 B, 48) is the **constructor from a C string** - `strlen`, a capacity of `0x40`, `0x80` or about twice the length rounded to 16, an allocation tagged with the source file `..\src\GPU\TinyEffect\TFXString.cpp`, a copy and a terminator; `007182F0` (82 B, 40) is **assignment**; `00719380` (207 B, 40) is **concatenation** returning a new string; and the 112-byte body with 8 sites truncates a string to a given length. The object is `{i32 length, i32 capacity, char *buffer}`. **The three real family helpers:** `0072EB20` (26 sites) takes `(effect holder, out[], name, count)`, drops the name's last character and, for `i = 1 .. count`, formats `"%s%d"`, looks the name up through the effect interface's slot `+0x60`, stores the handle, and zeroes it again if the interface's slot `+0xC8` rejects it; `0072DCF0` (65 sites) does the same over a lazily filled static table of **suffix strings** - `_REINHARDRGB_RGB`, `_REINHARDRGB_RGBFAST`, `_RGB_REINHARDRGB`, the `...LUM` forms, `_LOG...` and `_ALP...` - so one base name yields a tone-map / colour-space family; `0072DFD0` (4 sites, the `_TSn_n` family) was not read. **And the single-name lookups are not calls to any helper:** the catalogue body makes **224** inline indirect calls through the effect interface's slot `+0x60`, 33 through slot `+0x48` and 8 through slot `+0xC8`. So section 2's *332 registrations in seven shapes* counted 219 string operations as registrations; the lookups are 224 + 33 inline plus the 95 family calls, each of which makes several. *Reading, labelled:* look-up-then-validate is the shape of a technique fetch followed by a technique validation, and `+0x48` would then be the parameter fetch the body's own log line announces; the interface's slot names are not in the image. Static.
- [x] **UQ-226.** *(answered 2026-09-18, at the end of this item)* **The sole caller `0072D820`** and where in start-up it sits. **Narrowed 2026-09-14 (FABLE):** it is reached only through a C++ virtual call, from a class whose name the image carries.
      - **Its one caller.** `0072D820` has one raw call site, inside a 4,903-byte method with no direct caller.
      - **The class.** That method's address is slot 0 of the five-slot vtable at `00DA5DA8`. The RTTI locator before the table (`01D3C4B0`) names the class **`PPFX::CTextureUtil`**.
      - **Construction and destruction.** The vtable is installed by a 149-byte constructor and by a second body reached only from slot 4. That shape reads as the destructor path, which is not confirmed here.
      - **Who creates it.** The constructor is called from ten sites in five PPFX functions (4,375 bytes with five sites, 10,104 bytes with two, and 123, 508 and 2,101 bytes).
      - **Not established.** Where slot 0 is invoked on an instance, and therefore when in start-up the techniques are registered, needs the owner's virtual-call site. A direct-call census cannot show it.
      *(Functions are named by size here because they belong to the generated PPFX family on the library's source map. Citing their entries would change that family's measured set.)*
      **ANSWERED 2026-09-18 (FABLE): it is not start-up at all. The catalogue is built lazily, on the first frame the post-process render command runs with the effect library not yet created.** *The object.* `PPFX::CTextureUtil` is a **reference-counted singleton**: pointer at `02EA1590`, count at `02EA1598`. A 123-byte acquire allocates `0x22360` bytes and constructs it when the pointer is null, otherwise bumps the count; a 117-byte release drops the count and, at the last reference, calls slot 4 and frees it. `0x22360` also closes the size left open under UQ-224 (the last handle slot is at `+0x221D8`). *The slot-0 call.* Seven library functions reference the singleton pointer and exactly one makes a slot-0 virtual call on it: the library's 23,568-byte create routine, which acquires the singleton, writes its configuration fields near `+0x222A0`, and calls slot 0 with a pointer from its own parameter block - logging through the library's error path when the result is negative. Slot 0 is the 4,903-byte method that calls the catalogue body. *Who calls create.* One chain, read link by link: `PostProcessObj::Execute` on [the ordered render command list](../Render-Command-List/the-ordered-render-command-list.md) enqueues the callback `00193DA0` when the post-processing switch `01DFE0C4` is on; the callback asks the integration layer *is it created?* (`0065E5B0`) and only when the answer is no calls *create* (`0065E5A0`, `00193DC9`..`00193DE8`), which is a five-byte thunk to the first of the integration client's functions on [the source map](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md); that passes a parameter block (it carries the literal `0x780`) to a library wrapper and so to the create routine. A set byte at the settings object's `+0x99` takes the other arm (`0065E6C0`) instead. **So the 325 techniques are fetched the first time a frame is post-processed, and again after whatever that reset arm tears down** - a cost that lands on a frame, not on the loading screen. Static; library members are named by size and role because they belong to the declared PPFX family. *Not read:* what the reset arm destroys, and who sets `+0x99`.
- [x] **UQ-227.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)* Whether every registered technique is ever used. A name in the table proves the handle is
      fetched, **not that anything draws with it.**

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The function is `TEXSHADERSET::CreateEffect` | four authored log strings inside its body naming it | 2 |
| It is PPFX, built `Feb 18 2016` | `..\src\GPU\GPUTextureUtil.cpp` diagnostic prefixes | 2 |
| 325 technique names and 36 uniforms | every RIP-relative `LEA` in the 13,547-byte body resolved against NUL-terminated strings in `.rdata` | 2 |
| ~~364 call sites to 24 real targets~~ **358 call sites to 22 real targets**, with the per-helper counts | ~~linear `E8` decode of the body~~ **full disassembly of the 13,547-byte body, 2,965 instructions, zero decode gaps** (2026-09-12) | 1 |
| The count argument is a variant multiplier | the decompiled call sites, e.g. `0x19` on `…LayerMaskT1_Sn` | 1 |
| Logging is gated by `01F3BA80` + `02EA0B40` / `01F3BA90` | the decompiled guards | 1 |
| One caller | call graph, and the byte decode agrees | 11 |

### Two instrument limits, stated because both affected numbers above

**1. A printable-only string filter hides log messages, which are the most identifying strings
there are.** The first scan of this function used `[\x20-\x7e]` and returned **364** strings — and
**the five it dropped were the five that name the function**, because each ends in `\n`. Widening
to include `\t\n\r` gives 369. The exclusion was not neutral: it selected against exactly the class
of string that identifies code.

> This is the fourth narrow-matcher defect this session, and it followed the rule that caught the
> other three — the GFZ's own comment on this function quoted `TEXSHADERSET::CreateEffect()` as a
> string it references, my scan did not report it, and **a known positive disagreeing with the scan
> is what sent me to look.** See
> [the cutscene document §14](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md).

**2. A linear `E8` byte scan over-reports call targets.** The decode found 37 apparent targets, of
which **13 are not functions** — negative or absurd addresses produced by an `E8` byte occurring
inside another instruction's operand. They are excluded above; the ~~24~~ 22 real targets *(corrected 2026-10-02, OPUS: the struck row above; 358 sites to 22 targets)* all resolve in
the function list and carry the high call counts. **The per-helper counts are sound; the target
count would not have been if reported raw.**

### How many instances this rests on

- The **suffix grammar** in §2 is read from 325 names and is the best-supported claim here.
- The **count-argument-as-multiplier** reading rests on ~~**four observed literals** (4, 8, 17, 25)~~ the complete list of §2 (nine values over 91 sites) at
  call sites of two of the seven helpers. It is consistent with every one of them ~~and is **not**~~
  ~~established for the five helpers whose bodies were not read~~ *(answered: see §8's UQ-225 answer - the helper bodies are read; 2026-10-02, OPUS)*.
- The **`fParam_FocusDistance` ↔ `mDofFocusDistance` link** rests on **one** parameter name pair and
  the separately documented JSON reader. It is a name correspondence, not a traced dataflow — no
  code path was followed from the JSON value to this uniform.

## 9. Related

- [`ppfx-function-identification.md`](ppfx-function-identification.md) — PPFX as a population; does
  not cite this function.
- [`../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
  — where `mDofFocusDistance` is read from authored data.
- [`../../23-Third-Party-Libraries/third-party-middleware-inventory.md`](../../23-Third-Party-Libraries/third-party-middleware-inventory.md)
  — the middleware census this belongs to.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

§8 states an instrument limit worth taking seriously: *"a linear `E8` byte scan over-reports call
targets — the decode found 37 apparent targets, of which 13 are not functions."* The page corrected
for it by discarding the absurd ones. **The right test is to redo the census with an instrument that
has no such failure mode**, and see whether the corrected numbers survive.

They mostly do not, and the reason is instructive.

| claim | measured |
|---|---|
| the body is **13,547 B** | exact — and it **disassembles completely**: 2,965 instructions, `0072A320`–`0072D80B`, **zero decode gaps**, ending on `ret` |
| the four log strings at `00D9F498`, `00D9F810`, `00D9FAC0`, `00D9FB40` | **all four verbatim**, `\n` and all |
| `0072D820`, 396 B, is its **only** caller | **exactly one caller**, and it is `0072D820` at 396 B |
| `006DF480` has **160** callers image-wide | **exactly 160** |
| §4's family counts sum to **325** | **35 families summing to exactly 325** |
| **364** direct calls to **24** real targets | **358 calls to 22 targets — and every one of the 22 is a listed function** |
| `00715C70` **88** · `007157A0` **45** · `00719380` **37** | **91 · 48 · 40** — each **three** higher |

### A corrected instrument is not a correct one

There are **375 `E8` bytes** in this body and **358 direct calls**. Seventeen `E8`s sit inside other
instructions' operands. §8's filter removed the 13 that produced *"negative or absurd addresses"* —
but **that filter only catches what looks absurd.** The ones that landed on plausible addresses
survived it, and two are still counted among the "24 real targets".

The same misalignment cuts the other way, which is the part a filter can never fix: a byte scan that
mis-frames an instruction can also **miss** a real call. Three helpers are under-reported by
**exactly three each** — 88/45/37 where the image has 91/48/40 — so the registration total is
**332**, not "~323".

**The disassembler was available and has neither failure mode.** It decoded this body end to end with
no gaps, and found no spurious target at all. *A known limitation that has been adjusted for still
biases the number it produced; the fix is a better instrument, not a better correction.*

### What this does not touch

Everything resting on the **string** census is untouched and holds: the 325 technique names, the 36
uniforms, the suffix grammar, the four log strings. §8's other instrument note — the printable-only
filter that dropped exactly the five strings naming the function — was already found and corrected by
the page, and this pass confirms all four surviving log strings byte for byte at their cited
addresses.

**Not claimed:** nothing here was executed or observed live. The helper *bodies* were not read, so
§'s caveat ~~stands~~ *(answered: see §2's complete list and §8's helper bodies; 2026-10-02, OPUS)*: the count-argument-as-multiplier reading ~~still rests on four observed literals at~~
~~two of the seven helpers, and is not established for the five whose bodies are unread~~ rests on nine values at 91 sites.

## The frame half: what the game hands the library every post-processed frame (2026-09-25, FABLE, Claude Opus 5.5)

**Why this section exists.** Everything above describes **creation**: the one-time build of the
catalogue and its handles, which [the creation contract](CONTRACT-ppfx-effect-creation.md) covers.
S-40's verdict row says *"the pass chain is uncovered"*. This is the other half: the per-frame call
the render command makes, and which of its inputs the player controls. Static; read from the image.

**The entry.** `PostProcessObj::Execute` on
[the ordered render command list](../Render-Command-List/the-ordered-render-command-list.md) enqueues
`00193DA0` with the command's context. `00193DA0` takes the command's parameter block from
`[ctx + 0x10]` (called `cfg` below) and works through the library wrapper that `0065E5D0` returns
(a lazily built `0x10`-byte object at `02D38540`). The wrapper functions `0065E5A0`…`0065E6C0` are
one- or two-instruction forwarders into the library; the render command list page, under "the
`00193DA0` thunk family measured", has each forwarder's shape.

**The order, every frame:**

| step | when | call → library | what it passes |
|---|---|---|---|
| 1 | `cfg+0x99` set | `0065E6C0` → `006CC2F0` | nothing from `cfg`: two virtual calls on the library object (slot 1, then slot 0); not named here |
| 1′ | otherwise, library object absent (`0065E5B0` false) | `0065E5A0` → `006CBD20` | `cfg[0]` and the context's first qword: the **lazy create** that builds the catalogue above (`UQ-226`) |
| 2 | library object absent | — | **return: nothing else runs this frame** (`00193DFC`) |
| 3 | always | `0065E6A0` → `006CC1F0` | `&cfg+0x9C`: its contents land in ~~two 16-byte stores at `+0x28`/`+0x38` of an object `006CC1F0` resolves through `006DB900`/`006DB8C0`~~ four 16-byte stores at `+0x28`..`+0x58` of the receiver itself, which also clears byte `+0x24`; `006DB900`/`006DB8C0` run first only while that byte is clear *(corrected 2026-10-02, OPUS: `006CC1F0`+0xA, +0x3D..+0x5C)* |
| 4 | always | `0065E6B0` → `006CC260` | three floats `cfg+0xDC`/`+0xE0`/`+0xE4`, the last halved (`xmm3 × 0.5`) |
| 5 | **Glare option on** | `0065E670` → `006CC1E0` → `006DB9A0` | two floats `cfg+0x18`, `cfg+0x1C` (plus `1.0`, `1`) |
| 5′ | Glare option off | same call | **`1.0` and `0.0`** instead |
| 6 | always | `0065E630` → `006CBD00` → `006CC170` | `cfg+0x98` set: `2.0` and mode `2`; otherwise `1.0` and mode `1` if `cfg+0x9A` else `-1`. `006CBD00` is `mov eax, edx; ret`, so the mode passes through. `006CC170` then calls `006DC820` with `32.0` and `-FLT_MAX` |
| 7 | **DepthofField option on** | `0065E610` → `006CC090` | enable byte `cfg+0x20`, alternative-focus byte `cfg+0x21`, lens **`35.0`**, floats `cfg+0x24`/`+0x28`/`+0x30`/`+0x34` |
| 7′ | DepthofField option off | same call | enable **`0`**, lens `24.0`, `0.0`, `1.0`, `0.5`, `0.5`, alternative byte `0` |
| 8 | always | `0065E5C0` → `006CBEA0` | `cfg[0]`, `cfg[8]`, `cfg[0x10]`: three qwords, the run |

**The two player switches are graphics options, read from the type store.** The gates are dwords of
[`GameSettingConfig`](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
through `[01F82D20]`:
- `+0x34` is **`Glare`** (`enum{Off|On}`, default On) and decides step 5 (`00193E42`);
- `+0x30` is **`DepthofField`** (`enum{Off|On}`, default On) and decides step 7 (`00193EC0`).

Both calls run in either case. **The option changes what is passed, not whether the setter is
called.**

**What step 7 does with it.** `006CC090` is a physical-lens depth-of-field setter:
1. It calls `006DBC20` with the enable byte and, **when the byte is 0, skips every lens setting**
   (`006CC0BD`/`006CC0BF`). That is the path the DepthofField option's "off" takes: it passes enable 0.
2. When enabled and `cfg+0x21` is set, it also sets a `0.1`…`100.0` pair (`006DC700`) and reads
   `006DC650`.
3. It divides the lens value by **1000** (`006CC144`, `008C5F78` = `1000.0`). So `35.0` is a
   **35 mm focal length expressed in metres**, and the `24.0` of the off path never reaches the
   lens at all.

This is where the uniform `fParam_FocusDistance`, and behind it the cutscene sidecar's
`mDofFocusDistance` (§1), would have to enter. ~~**Which `cfg` float carries the focus distance is not~~
~~read here.**~~ *(answered: see CONTRACT-post-processing-subsystem.md - `+0x24` / `+0x28` carry `mDofFocusDistance` / `mDofApertureFnumber`; 2026-10-02, OPUS)*

**What step 5 corroborates, and what it does not.** Glare off passes `(1.0, 0.0)` into the same
setter rather than skipping it. A zero second argument is consistent with a zero intensity, but
~~`006DB9A0`'s body is not read here.~~ *(answered: see CONTRACT-post-processing-subsystem.md - the chain to `00707560` `SetGlareParameters`, read 2026-09-25; 2026-10-02, OPUS)* **So "Glare off disables the glare passes" is an inference; that
the option changes the passed values is not.**

**What this establishes for S-40's pass chain:**
- The library is driven by **one run call per post-processed frame** (step 8), after up to six
  configuration calls.
- **Two of those are under the player's direct control**, through the `GameSettingConfig` Glare and
  DepthofField options.
- The DOF setter provably skips its lens configuration when disabled.

**Not established:**
- which catalogue techniques step 8 executes for a given configuration (`UQ-227`, now PARTIAL: the next section measures which families can never run);
- ~~who fills `cfg`, and in particular which float is the cutscene focus distance;~~ *(answered: see CONTRACT-post-processing-subsystem.md - the post-processing set-up that contract names allocates the `0xF0` block, and `+0x24` is the focus distance; 2026-10-02, OPUS; set-up named by role here, FABLE, so the far-end address stays on the contract)*
- what steps 3, 4 and 6 configure. Their names are not in the image, and nothing here names them.

## Which families can run at all: the feature flags the game initialises with (2026-09-25, FABLE, Claude Opus 5.5)

**The library names its own API.** Its error strings begin `CPostEffect::<method>():`. Mapping each
string to the function that loads it names 62 API functions; the control is that `0070BA00` is
found loading the `ApplyEffects` message, and it is. The artefact is
`Database/Tools/work/FABLE/gg3-scratch/ppfx_api_names.py`. The ones that matter here:

- `006FF900` `Initialize` and `0070BA00` `ApplyEffects`. `ApplyEffects` refuses with `E_FAIL` inside
  a Begin/End scene pair, or when the object was initialised with `PFXINIT_RENDERSCENE_EXTERNAL` and
  no effect source was set.
- `0070B780` `BeginPostEffectScene`.
- One `Set<Feature>Enable` per optional feature.

**Each optional feature is gated twice.** `Initialize` derives a per-feature "initialised with"
byte from one flag word, stored at `+0x20C` (`006FFE56`–`00700080`):

| flag bit | "initialised" bytes it sets | the feature, from its setter's own message |
|---|---|---|
| `0x40000` | `+0x131`, `+0x132`, `+0x133`, `+0x134` (and `+0x135` with `0x200000`), `+0x137`, `+0x138`, `+0x13C` (→ `+0x13D`), `+0x142` | lens distortion, aperture Airy disc, motion blur, geometry blur, Gaussian blur, heat shimmer, chromatic aberration |
| `0x4000000` | `+0x13A`, `+0x13B` | ambient occlusion |
| `0x8000000` | `+0x140`, `+0x141` | post-process antialias and its distance falloff |
| `0x8000` | `+0x143` | not named here |
| `0x400` | `+0x144`, `+0x146` | not named here |

Each `Set<Feature>Enable` refuses unless its byte is set (for example `0070A486 cmp byte ptr
[rcx+0x134], 0`, with the message *"Initialize() with PFXINIT_… flag"*). For motion blur, the byte's
only other readers are `Initialize`'s own resource-allocation gates (`00701128`, `00704AF6`) and two
getters.

**The game initialises the library exactly once, and always with `0x20001`:**
- The one live route to `Initialize` is `00193DA0` → `0065E5A0` → `006CBD20` → `006DAA70` → `006FF900`.
- `006CBD20` passes the constant `0x20001` as the fifth argument (`006CBE02`). `006DAA70` forwards its
  own fifth argument unchanged (`006DAD0A`), and `Initialize` stores it at `+0x20C` (`006FFB8C`).
- Inside `Initialize`, the only bits ever forced are the low `0x0F`/`0x70` group, bit 7, and `0x400`
  (only when `+0x43C` matches).
- The other caller of `Initialize`, `006DE950`, has no route in. There is no E8/E9 call (including
  the unlisted-code arm), no conditional jump, no `lea` and no stored 64- or 32-bit VA. The only hits
  are 32-bit RVAs in the unwind tables.

**So in the shipped game none of the table's first three bits is ever set.** Lens distortion,
aperture Airy disc, motion blur, geometry blur, Gaussian blur, heat shimmer, chromatic aberration,
ambient occlusion and the post-process antialias (FXAA) are **registered in the catalogue above,
never initialised, and their enables always refuse**. That covers the whole Motion family (50),
Alchemy SSAO and Fxaa2 among §4's families. The features the frame half (above) actually drives —
depth of field and glare — are not behind these bits.

**Bounds.**
- Static. The single route and the constant are read from the image, not observed live.
- For motion blur, "never runs" rests on the byte's reader set above (allocation gates, setter,
  getters). For the other features it rests on their setters' refusal. Whether `ApplyEffects`
  reaches any of those passes by another test is not read.
- `UQ-227` asked whether every registered technique is used. The answer is **no**, and the families
  above are the measured part. The rest of the catalogue (depth of field, bokeh, glare, tone map
  and composite) is reachable, but which of its techniques run is not measured.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

**Platform — CLIENT (FABLE, Claude Opus 5.5, 2026-09-25).** The wrapper accessor `0065E5D0` has one caller outside this path: `006253D0`, the platform device set-up that [the ordered render command list](../Render-Command-List/the-ordered-render-command-list.md) calls the NvAPI init. It fetches the same wrapper and calls `0065E580(wrapper, 1)` (`00625493`–`0062549D`), a platform-side switch on the library object that is not read here. The crossing is that shared wrapper. The frame path above does not call into Platform.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-post-processing-effect-catalogue-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `006CC2F0` | 63 B | when qword `+0` of `rcx` is non-null, calls virtual slot 1 (vtable `+8`) on it and stores 0 to qword `+0`; then, when qword `+8` of `rcx` is non-null, calls virtual slot 0 (vtable `+0`) on it with `edx` = 1 and stores 0 to qword `+8` | `006CC2FC`, `006CC304`, `006CC307`, `006CC31F`, `006CC321` |
