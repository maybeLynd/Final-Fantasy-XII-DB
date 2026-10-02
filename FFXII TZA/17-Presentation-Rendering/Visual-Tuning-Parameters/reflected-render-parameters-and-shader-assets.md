---
system: Reflected render parameters and shader assets
category: 17-Presentation-Rendering
status: PARTIAL — OV-42 (live, ASTRA) stays open in the F4 section; the SD-141 reopening is resolved 2026-10-01 (OPUS; SWE2-AUDIT-SPEC's REJECT was the non-author CORRECTED pass); every other register row is closed: W-7 SUPERSEDED 2026-09-26 (class-1 ruling: the section-3 bodies are a declared population, not read); W-5 answered 2026-09-27 (no Inverted pass draws in this build); which class owns each parameter group (W-3) answered 2026-09-18: none, the groups are three JSON documents and their value stores; W-1, W-2, W-6, W-8, W-9 answered; who reads the flying-fade pair (SD-141) answered 2026-10-01: the GPU - 517 default lit shader variants read it from the scene-wide constant buffer
owner_layer: CodeDomain:Phyre.PostProcessing + Phyre.Rendering
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 22 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
audit:
  passes: 2
  last_pass: 2026-09-30
  last_pass_state: swe2auditspec-sd141-reject-corrected-pass-2
  crossref_clean: true
  reopened_count: 2
  last_pass_kind: falsification
---

# Reflected render parameters and shader assets

> **The people who made FFXII left the names of roughly 150 tuning knobs in the executable** —
> shadow softness per character, ambient occlusion radius for scenery, the *aperture f-number* of
> the depth-of-field blur — along with the paths of the ~~15 shader files~~ 18 `.phyre` assets *(corrected 2026-10-02, OPUS: 16 under `shaders`, the font `tuffysdf.fgen` and the map-texture template - §2's count)* that consume them.

**PARTIAL.** The names and asset paths are authored strings read directly from the shipping EXE
(tier 2) and are exact. ~~What each parameter numerically does, and where the values live, is not
yet read.~~ *(Corrected 2026-09-30, SWE2-DATA: where the values live is answered (W-1, W-2, §8b / §8c), and which
authored names the build reads is censused (§8d); the section-3 bodies are W-7, SUPERSEDED as a declared population.)*

## 1. What the player sees

Everything about how FFXII *looks* that isn't geometry or texture.

The soft edge on a character's shadow. The way distant scenery loses contrast. The blur when the
camera whips around. The bloom around a bright sky. Whether Vaan's eyes catch a highlight. How
water refracts.

None of that is hardcoded. Each is a named number, and the names are still in the game. A modder
who wants FFXII to look different is looking for this list — the game is asking for these values
by name, so they exist somewhere to be found and changed.

The naming even carries the game's history: the depth-of-field shader is called
**`PS2DepthOfField.fx`** — a PlayStation 2 heritage name surviving into a 2017 remaster.

## 2. Native mechanism

### The shader asset set — 18 files, one convention

Authored paths, verbatim from the binary:

```
/GameData/D3D11/ArtData/shaders/SAO.fx.phyre
/GameData/D3D11/ArtData/shaders/HBAO.fx.phyre
/GameData/D3D11/ArtData/shaders/PS2DepthOfField.fx.phyre
/GameData/D3D11/ArtData/shaders/SeparableSSS.fx.phyre
/GameData/D3D11/ArtData/shaders/GaussianFilter.fx.phyre
/GameData/D3D11/ArtData/shaders/UnSharpMask.fx.phyre
/GameData/D3D11/ArtData/shaders/PhyreFXAA.fx.phyre
/GameData/D3D11/ArtData/shaders/SMAA.fx.phyre
/GameData/D3D11/ArtData/shaders/searchtex.dds.phyre
/GameData/D3D11/ArtData/shaders/areatexdx10.dds.phyre
/GameData/D3D11/ArtData/shaders/depthmask.fx.phyre
/GameData/D3D11/ArtData/shaders/BrightnessShader.fx.phyre
/GameData/D3D11/ArtData/shaders/video.fx.phyre
/GameData/D3D11/ArtData/shaders/PhyreText.fx.phyre
/GameData/D3D11/ArtData/font/tuffysdf.fgen.phyre
```

> **Corrected 2026-09-02 (§9).** Three further `.phyre` paths exist and were missed, because they
> spell the API element as a **`%s` format placeholder** rather than the literal `D3D11` the
> enumeration filtered on:
>
> ```
> /GameData/%s/ArtData/shaders/CopyBuffer.fx.phyre
> /GameData/%s/ArtData/shaders/anisolighting.dds.phyre
> /GameData/D3D11/ArtData/map/%s/tex/%s.dds.phyre
> ```
>
> The count is **18**, and **three** directories carry `.phyre` assets — `shaders`, `font` and
> `map/<mapcode>/tex`. The claim below that only two appear is superseded.

The original reading: only **two directories** appear: `shaders` and `font`. The convention is
`/GameData/<API>/ArtData/<kind>/<name>.<type>.phyre` — the `D3D11` element implies the tree is
per-graphics-API.

What the set establishes:

- **Two ambient occlusion implementations ship**: `SAO` (Scalable Ambient Obscurance) and `HBAO`
  (Horizon-Based). Both have parameters (below), so both are wired, not vestigial.
- **Two antialiasing implementations ship**: `PhyreFXAA` and `SMAA`. `searchtex.dds` and
  `areatexdx10.dds` are SMAA's two required precomputed lookup textures — their presence is
  independent confirmation that SMAA is a real path, not just a filename.
- **`SeparableSSS`** is separable subsurface scattering — skin shading.
- **`tuffysdf.fgen`** is the Tuffy typeface as a signed-distance field, which is what
  `RenderText_SoftEdgesAndGlow` consumes.

### The class hierarchy, from mangled names

```
PGlow           <- PGlowBase        <- PGlowGPUBase       <- PGlowD3D11
PMotionBlur     <- PMotionBlurBase                        <- PMotionBlurD3D11
PDepthOfField   <- PDepthOfFieldBase                      <- PDepthOfFieldD3D11
```

All under `Phyre::PPostProcessing::`. The `Base` / `GPUBase` / `D3D11` layering is the standard
Phyre pattern: abstract interface, GPU-generic, API-specific.

Named render entry points also appear as strings: `RenderAtmosphere`,
`RenderAtmosphereInverted`, `RenderCameraMotionBlur`, `RenderCameraMotionBlurInverted`,
`GenerateGlowBuffer`, `GlowBuffer`, `RenderText_SoftEdgesAndGlow`. The `Inverted` variants are
consistent with a mirrored pass — a reflection or an inverted-projection render.

### The parameter surface

These follow the `m<Name>` member convention and are ~~**the embedded strings that Phyre~~
~~reflection's `PClassDataMember` holds**~~ JSON keys: the strings checked are reached only by code `lea`s into the scene loaders' key lookups *(corrected 2026-10-02, OPUS: `001C3D50`+0x556 `lea rdx, [008FA4D0]` then +0x560 `call 001C51D0`; W-3 below)* — the reflection document establishes that each member
descriptor carries its field name as an embedded string, and this is that data.

**Shadow — ~~28~~ 32 parameters.** *(corrected 2026-10-02, OPUS: the names listed below; 31 occur as strings, `mCascadePartition` only as a stem)* Separately tunable for maps and characters:

```
mShadowValueLerpMinForMap / Map2 / Map3        mShadowValueLerpMinForChr / Chr2 / Chr3
mShadowVertexBlendLowerLimit / UpperLimit      mShadowAngleLowerLimit / UpperLimit
mMapShadowDepthBias / mMapShadowSlopeOffset    mChrShadowDepthBias / mChrShadowSlopeOffset
mMapEnableShadowFade                           mMapShadowFadeSpeed / FadeRange
mMapShadowFlyingFadeRange / FlyingFadeSpeed    mMapObjectShadowFadeEnabled / FadeRange
mShadowRed / Green / Blue / Alpha              mUseSubCameraForShadow
mEyeABSpecularShadowModifier                   mSpecialShadowFlag
mCascadePartition / mCascadePartition0 / 1 / 2
```

The `Map` / `Chr` split runs through the whole set — **scenery and characters are lit and shadowed
by separate parameter groups.** `mCascadePartition0..2` confirms a 3-split cascaded shadow map.
`mMapShadowFlyingFade*` is its own case~~, presumably for airborne viewpoints~~. *(Corrected 2026-09-30, SWE2-DATA:
the guess is unsupported. What is read: `001C7940` looks up `mMapShadowFlyingFadeRange` and `...Speed`, falling back to
the defaults document when a map omits them, and stores the two floats into two globals that no rip-relative
instruction reads ([`rrp_checks.py`](../../_index/candidates/dd-data-4-0930/rrp_checks.py) F1, F2). Who consumes them is `SD-141`.)* ~~*(`SD-141` answered 2026-09-30, OPUS, [record](../../_index/candidates/sd141-flying-fade-readers-0930/README.md): nothing reads the pair; the two floats are stored and never used.)*~~ *(Reopened 2026-10-01, OPUS, on SWE2-AUDIT-SPEC's REJECT, [review](../../_index/candidates/auditspec-review-sd141-0930/REVIEW.md): the pair is read by `005DEC50`'s struct copy, handed `02CB8160` by `006084B0`; its consumers are open, SD-141.)* *(Answered 2026-10-01, OPUS: the GPU reads it - SceneWideParameterConstantBuffer +0x5D4 / +0x5DC, used by 517 phyredefaultlitshader.fx blobs; SD-141.)*

**Lighting and colour — 21 parameters**, all `Map`-prefixed or character-specific:

```
mMapAmbientColorR / G / B / mMapAmbientColorCutPercent
mMapLightColorR / G / B
mMapChrAmbientIntensityR / G / B      mMapChrAmbientOffsetR / G / B
mMapChrDirLightColorIntensityR / G / B
mMapChrUpwardDirLightAngleThres       mMapChrUpwardDirLightColorIntensity
mColorR / G / B
```

**Ambient occlusion — ~~12~~ 14 parameters** *(corrected 2026-10-02, OPUS: the fourteen below, 2 x 2 x 3 + 2)*, and the structure is the informative part:

```
mSAOBiasChr   mSAORadiusChr   mSAOIntensityChr     mSAOFadeoutScale
mSAOBiasSce   mSAORadiusSce   mSAOIntensitySce
mHBAOBiasChr  mHBAORadiusChr  mHBAOIntensityChr    mHBAOFadeoutScale
mHBAOBiasSce  mHBAORadiusSce  mHBAOIntensitySce
```

A perfect 2 x 2 x 3: **two algorithms** (SAO, HBAO) x **two subjects** (`Chr` character, `Sce`
scene) x **three knobs** (bias, radius, intensity), plus one fadeout scale each.

**Depth of field, blur and glare:**

```
mDofFocusDistance    mDofApertureFnumber    mDofSpecialApertureFnumber
mMotionBlurEnabled   mBlurFactor
mUSMBlur             mUSMIntensity          mUSMThreshold      (unsharp mask)
mGlareLuminance      mGlareThreshold
mGammaValue          mUseLinearTonemap
```

**`mDofApertureFnumber` is a photographic f-number** — the depth of field is parameterised the way
a real lens is, not as an arbitrary blur radius.

**Water — ~~16~~ 18 parameters** *(corrected 2026-10-02, OPUS: the eighteen below, each a string in the image)*, all shipped with `Debug` in the name:

```
mDebugRefractionFactor      mDebugWaterSpecFactor        mDebugWaterTexBlendFactor
mDebugWaterCubemapFactor    mDebugWaterRoughnessFactor   mDebugWaterParallaxFactor
mDebugWaterFresnelFactor    mDebugWaterUFactor / VFactor mDebugWaterMinZ
mDebugWaterStepSize         mDebugWaterTotalNumPix       mDebugWaterRefBldFactor
mDebugWaterRefFactor        mDebugWaterStepInrSpeed      mDebugWaterExtraFactorTwo
mWaterBias                  mEarlyWaterDraw
```

`StepSize`, `MinZ`, `TotalNumPix` and `StepInrSpeed` together describe a **ray-marched screen-space
refraction** — a per-pixel stepping loop. The `Debug` prefix survived into the retail build.

**Eye rendering has its own group** — an unusual amount of dedicated machinery:

```
mEyeABCubeMapBlendFactor     mEyeABSpecularBlendModifier
mEyeASpecularIntensityAfterClampModifier      mEyeBSpecularIntensityAfterClampModifier
mEyeMapSpecularIntensityAfterClampModifier
```

**Environment and range:**

```
mMapFarPlane   mNearRatio   mFarRatio   mEnableMapHeightRange   mMapHeightMin / Max
mEnableDecay   mDecayDistance           mCubemapIntensity
mMapIrrCubemapFactor / Limit / Intensity          mClutIndex   mDisableCutFov
```

`mMapIrrCubemap*` is an **irradiance cubemap** — image-based ambient lighting.

### The same mechanism drives the UI

The extraction also returned a large group that is plainly not rendering:

```
mGambitPositionOffsetX / Y        mBtlCommandScrollTableOffsetY
mCommandMenuStrHeight / OffsetY   mCommandTitleFontHeight    mScrollListHeight
mCursorRightX / Y  mCursorDownX / Y  mCursorLeftX / Y  mCursorUpX / Y  mCursorOpenX / Y
mGeneralFrameFrontOffset / BackOffset      mCPCWindowHeight
mPauseMenuOffsetX / Y             mNumEffectOffsetX1 / X2    mExpEffectOffsetY
mHelpMessageFontCount             mTriangleHelpMessageFontCount
mFontRed / Green / Blue / Alpha
mBattleCommandItalicRevJp         mBattleCommandItalicRevUs
```

**FFXII's menu layout is data-driven through the same reflection system**, down to individual
cursor positions. And `mBattleCommandItalicRevJp` / `...Us` are **per-region layout corrections** —
the Japanese and US builds needed different italic handling for battle commands.

This belongs to UI, and is recorded here only because it came out of the same extraction. See §9.

## 3. Key addresses

| Address | Role | Verified |
|---|---|---|
| `0059E070` | `PostProcessing.Vignette` (656 B) | ⚠ read, blocks elided |
| `00656B20` | `PostProcessing.GlowParameters` (635 B) | not read |
| `00655180` | `PostProcessing.MotionBlurParameters` (579 B) | not read |
| `00656F20` | `PostProcessing.ReflectionParameters` (542 B) | not read |
| `00648100` / `006561D0` | `PostProcessing.AtmosphereParameters` | not read |
| `006C0540` / `006C0580` / `006C05F0` | `Rendering.LightReflectedMethod` | not read |
| `0062E5A0` | `SceneCamera.PWorldMatrixFlyController.OrientationTransformUpdate` | not read |
| `01F44830` | security cookie (seen again in `0059E070`) | ✅ cross-confirmed |

*(Note 2026-09-30, SWE2-DATA: the "not read" cells above are the W-7 population, SUPERSEDED 2026-09-26 under the
class-1 ruling; they are declared unread, not pending.)*

**Family sizes** from the GFZ tag census: `PostProcessing.NativeQualified` 66,
`Rendering.NativeQualified` 64, `Rendering.RegistryStaticTeardown` 171,
`Rendering.ReflectedMethod` 16, `Animation.NativeQualified` 50, `Physics.NativeQualified` 55.

## 4. Data structures and formulas

```
Asset path convention
  /GameData/<GraphicsAPI>/ArtData/<kind>/<name>.<type>.phyre
  observed: GraphicsAPI = D3D11 ; kind = shaders | font   <- corrected 2026-10-02, OPUS - and map/<mapcode>/tex - three directories, section 2

Ambient occlusion parameter grid           2 x 2 x 3 + 2
  algorithm : { SAO, HBAO }
  subject   : { Chr, Sce }
  knob      : { Bias, Radius, Intensity }
  name      = "m" + algorithm + knob + subject
  plus        mSAOFadeoutScale, mHBAOFadeoutScale

Shadow map cascades
  mCascadePartition0, mCascadePartition1, mCascadePartition2      -> 3 splits

Depth of field
  mDofFocusDistance          focus plane distance
  mDofApertureFnumber        photographic f-number
  mDofSpecialApertureFnumber alternate aperture (cutscene?)   <- corrected 2026-10-02, OPUS - a map key: its only readers are 001C7940+0x171 and +0x188, the map loader

Reflected member naming convention
  m<Name>       where Map = scenery, Chr = character, Sce = scene, USM = unsharp mask
```

**No numeric formula is asserted.** These are names and their organisation; the arithmetic that
consumes them has not been read. ~~Recorded as **W-1**.~~ *(corrected 2026-10-02, OPUS: W-1 is where the values live, answered in §8b; this arithmetic is not a register row)*

## 5. Call chain

```
process start
  -> Phyre reflection static initializers
     -> PClassDataMember descriptors constructed, each holding its name as an embedded string
        -> these ~150 names

render frame
  -> RenderAtmosphere / RenderAtmosphereInverted
  -> GenerateGlowBuffer -> GlowBuffer
  -> RenderCameraMotionBlur / ...Inverted
  -> AO pass  (SAO.fx.phyre or HBAO.fx.phyre)
  -> DOF pass (PS2DepthOfField.fx.phyre)
  -> AA pass  (PhyreFXAA.fx.phyre or SMAA.fx.phyre + searchtex/areatexdx10)
  -> UnSharpMask.fx.phyre, BrightnessShader.fx.phyre
  -> RenderText_SoftEdgesAndGlow (PhyreText.fx.phyre + tuffysdf.fgen.phyre)
```

**Upstream:** the reflection layer that names these fields; the asset pipeline that loads
`.phyre` files.
**Downstream:** the D3D11 device.

**Do not confuse with:** `ThirdParty.Rendering.PPFX` (345 functions), which is a separate
post-processing framework in the same binary.

## 6. Modding notes

- **The look of FFXII is data, not code.** ~150 named parameters govern shadows, AO, DOF, water,
  eyes and tonemapping. Find where the values live and the game can be re-graded without patching
  code.
- **Scenery and characters are separate everywhere.** `Map`/`Sce` vs `Chr`. Changing scene AO does
  not touch characters.
- **Both AO and both AA implementations are present and parameterised.** Switching between SAO and
  HBAO, or FXAA and SMAA, is plausibly a configuration change.
- **`mDofApertureFnumber` is a real f-number** — treat it photographically, not as a blur radius.
- **Water is ray-marched** — `mDebugWaterStepSize` and `mDebugWaterTotalNumPix` are loop controls.
  Raising them costs frame time directly.
- **Shader assets live at `/GameData/D3D11/ArtData/shaders/`** inside the VBF archives, as
  `.fx.phyre`. The `D3D11` element suggests the path is API-parameterised.
- **The UI is data-driven too**, down to cursor coordinates and per-region italic corrections.
- **XIIOnline:** all of this is local presentation. None of it should ever cross the wire, and two
  clients rendering with different values is harmless — unlike the state hubs, disagreement here
  has no gameplay consequence.

## 7. What is not known

- [x] ~~Where the parameter values live.~~ **W-1 ANSWERED in section 8b** - `JsonData/*.json`
      inside the VBF archive, plus loose `ConfigData/*.ini`.
- [x] ~~Whether more parameters exist that this extraction missed.~~ **W-8 ANSWERED - yes**, a whole
      non-`m` vocabulary (`lightShaft*`, `chr*`, `Enable*`, `m_i`/`m_f`).
- [x] ~~Whether the values are per-area.~~ **W-2 ANSWERED in section 8c - yes.** `jsondata/init.json`
      holds 176 defaults; **459** `jsondata/maps/<mapcode>.json` files hold per-area overrides.
- [x] Which class owns each parameter group. **W-3.**
  *Bounded 2026-09-15 (FABLE), not answered — §8d.* The reader population is **seventeen** functions and
  the vocabulary they spell is **452** names; `001CA600` (226) and `001C7940` (155) account for 381 of
  them, so the group-to-class map is mostly a question about those two bodies. Which *function* spells
  each name is now known; which *class* owns each group is not.
  ***ANSWERED 2026-09-18 (FABLE) — no class owns them: each group is a JSON document and the value store it is read into, and the three spellers are the readers.** `001CA600` (8,186 B, the 226 `m*` UI names) is the reader of the UI-size document `01F81318`: every name goes through `001FF740(01F81318, "name")` and the value into the settings block `001B1C00() + 0x3B00` (`001CA60B`..`001CA65D`); its only caller `001C6C00` loads that document from `JsonData/UISize/UISize.json` or `UISize_sd.json`. `001C7940` (11,445 B, the map-lighting names `AODepthFullRes`, `EnableAO`, `mGammaValue`, the DoF and tonemap keys) is called by `001C61F0`, which builds `JsonData/Maps/` + the map name (prefix `008F9E60`, `001C6285`), parses it into the per-map store `01F81328` (`001C62A1`) and then runs the reader over it (`001C62DA`) with the boot defaults `01F813C8` (`init.json`) as the document its lookups fall back to (`001C79F2`); `001C7290` re-applies it after resetting the banks. `001C3D50` (4,607 B, the DoF / SAO / cascade / `EnableDof` / `EnableShadow` names) reads the cut-scene banks `01F813A8` (main screen) and `01F813D8` (second screen) that `001C5930` builds from `JsonData/CutScenes/<scene>.json`, through the four-step fallback *Cut N* → `Common` → `01F81328` → `01F813C8`, into the record `01F812D0` — the machinery [the console page](../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md) and [the render-command-list page](../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md) already read. So the group-to-owner map is: UI names → `UISize.json` → settings `+0x3B00`; map-lighting names → `Maps/<map>.json` → `01F81328` (defaults `01F813C8`); render / cut-scene names → `CutScenes/<scene>.json` → `01F812D0`. None of the three is a reflection class; the names are JSON keys, which is why the reflection static-init region never spells them. Static: the three bodies, their callers and the strings they load.*
- [x] ~~**W-9.** **Why `mCascadeNumber` and the `_2` / `_3` cascade columns are authored but never read.**~~
  **W-9 ANSWERED 2026-09-15 (FABLE), and its premise was my own error — §8d.** The `_2` and `_3` columns
  **are** read: `001C7940` formats the template `"mCascadePartition%d_%d"` at run time
  (`001C9190`–`001C9209`, `c ∈ {0,1,2}`, `q ∈ {1,2,3}`) into a 3 × 3 float matrix at `+0x350` whose sink
  `001A9B00` bounds-checks both indices against `3`. Only `mCascadeNumber` has no reader, and it is
  **`3` in all 284 sections that author it** — invariant, and equal to the hardcoded bound.
- [x] What the `Inverted` render passes are for — water reflection is the obvious guess and is not
      proven. **W-5.**
      ***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static and data: no `Inverted` pass draws in this build, so it is not a
      water reflection.*** The five names are variants inside PhyreEngine's stock post-effect classes (`PAtmospherics`,
      `PCelShading`, `PMaterialPostEffect`, `PMotionBlur`, `PFXAA`), each chosen when the bound target carries bit 1 of its
      `+0xC` word. Only FXAA is built by game code, and its one effect file has no `Inverted` technique. The other four are
      reachable only through their reflection descriptors, and no shipped file names them. No file in the extract contains
      `Inverted`. [The W-5 record](../../_index/candidates/w5-inverted-passes/README.md), control `w5_inverted.py`, 6 checks.
      ***NARROWED 2026-09-17 (FABLE): the `Inverted` variant is chosen per pass by a flag on the render target, not by a reflection pass of its own; what sets the flag is not in code.** The five names are PhyreEngine string objects built at start-up (`CelInverted` `00164BB0`, `MaterialPostEffectInverted` `00164DF0`, `RenderAtmosphereInverted` `00164F70`, `RenderCameraMotionBlurInverted` `00164FD0`, `RenderFXAAInverted` `001650F0`, each `005DC6F0(object, text, 0)` with a destructor registered through `00808B90`), and each pass has one selector that picks between the plain and the Inverted object. The atmosphere selector `00658470` (`00658707`..`00658732`) takes `RenderTextures` when byte `+0x61` of the pipeline object is set, else the Inverted name when its third argument, a target descriptor, has **bit 1 of its dword `+0xC`** set, else the plain name, and stores the choice at `+0x80` of the pass; the cel selector `006587F0` (`00658AC2`) and the material post-effect selector `00659A90` (`00659B4B`) test the same bit of the same word, ~~while the FXAA and motion-blur selectors `0065A640` and `00659C20` branch on a byte argument and a call result instead.~~ *(Corrected 2026-09-27, FABLE, Claude Opus 5.5: they test the same bit of the same word, at `0065A888` and `00659DE4`.)* No instruction in `005C0000`..`006C0000` sets or clears bit 1 of a `+0xC` word with an immediate, so the flag arrives with the target's own data. A reflection pass would set it; so would any target rendered with a flipped projection. Which targets carry it is the residue.*
      **Narrowed again 2026-09-25 (FABLE, Claude Opus 5.5): no immediate store anywhere in the image sets the flag on
      the descriptor type; it is copied in.**
      - **The census.** Every `or` of bit 1 into a `+0xC` field, at byte, word or dword width, and every `bts ..., 1` on
        one, was swept over the whole image. It finds **18 sites in 14 functions**, and each writes a different
        structure:
        - an `ActorEntity` pair in the `0025Bxxx`–`0025Cxxx` range, byte-width;
        - a `Presentation` cluster `00422E50`–`00425510`, whose receiver, where read (`00422E50`), is a presentation entry resolved by id through
          the entry-reference container (for example `00422E7F` → `00422E89`);
        - one `Presentation` body in the `00532xxx` range, a word-width field in `0x440`-stride records.
      - **How the descriptor arrives.** The atmosphere selector's one caller, `0065B270`, is itself a vtable method: its
        only reference is a slot in `.rdata`. It forwards its own third argument, the descriptor, and its fourth, whose
        `+0x28` / `+0x2C` read as a width and height.

      So bit 1 reaches the descriptor through the object's own data, from whoever builds it, and not from a store
      that names the bit. ~~*Next step:* the class behind that vtable slot, through the RTTI index, and the creator of
      the descriptor it is handed.~~ *(Corrected 2026-09-30, SWE2-DATA: no next step is pending; the 2026-09-27
      answer above closes W-5 without it.)*
- [x] `mClutIndex` — a colour lookup table index? Would imply LUT grading. **W-6.**
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (W-6): no grading. It is the index of a text
  colour palette, one of the 28 `fontclut_%d` entries.*
  - **The handler.** `001C76E0` is the only code that names `mClutIndex` (`008FB668`; references at `001C76E4` and
    `001C7707`).
    - It returns at once when that parameter's type dword is 6 (`00200BE0`), taken here as "absent".
    - Otherwise it reads the index and fetches entry `mClutIndex` of the font painter's table through
      `001E94E0(painter, index)` (painter = `001B5FA0()` = `[01F811F8]`).
    - It overwrites the entry's `+0x04`–`+0x10` from `mShadowRed` / `mShadowGreen` / `mShadowBlue` / `mShadowAlpha`
      and `+0x14`–`+0x20` from `mFontRed` / `mFontGreen` / `mFontBlue` / `mFontAlpha` (`001C7738`–`001C782F`).
  - **The table.** `001E94E0` bounds the index to `0x1B` and returns `painter + 0xF68 + 36·index`. On first use it sets
    the entry's loaded byte and loads it by formatting **`fontclut_%d`** (`00901978`) and calling `001C5F20` with that
    name, which reaches `001C76E0` (`001C61CD`).
  - **The consumer.** The glyph painter fetches `001E94E0(painter, [glyph + 0x9C] % 0x1C)` for every glyph and
    multiplies the entry's channels into the vertex colour
    ([painting a line of text](../../99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md) §6).
  - **So `mClutIndex` lives in the `fontclut_N` parameter sets, not in the render-tuning vocabulary around it.** "CLUT"
    here keeps its PS2 meaning: a small fixed palette selected per text run. The name sits next to UI layout keys
    (`monsterModelId`, `mScrollListHeight`) in the string pool, which fits.
- [x] The bodies of every function in §3. **W-7.**
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md. See the register row.*
- [x] Whether more parameters exist that this extraction missed. **W-8.**
- [x] **Who consumes the flying-fade pair.** `001C7940` stores `mMapShadowFlyingFadeRange` and `...Speed` into two
      globals, and no rip-relative instruction reads them; a reader through a base register, and so what "flying"
      fades, is not found. **SD-141** (SWE2-DATA, 2026-09-30). ~~*(SD-141 answered 2026-09-30 by OPUS `940b5ffcf`, [record](../../_index/candidates/sd141-flying-fade-readers-0930/README.md).)*~~ *(Reopened 2026-10-01, OPUS: SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-sd141-0930/REVIEW.md) finds the read through a handed-on base; who reads the copy's `+0x550` / `+0x554` and `[r14 + 0x5D4]` / `[r14 + 0x5DC]` is open.)* *(SD-141 answered 2026-10-01 by OPUS, [record](../../_index/candidates/sd141-gpu-consumers-1001/README.md): the pair is consumed on the GPU: 005DEC50's copy feeds 00604750's snapshot, which 00604750 writes through a mapped D3D11 buffer (006097B0 -> 00626060) into SceneWideParameterConstantBuffer +0x5D4 mShadowFlyingFadeSpeed and +0x5DC mShadowFlyingFadeRange, and 517 of the 4,799 shipped DXBC blobs, all phyredefaultlitshader.fx, read both (D3D_SVF_USED), as many as read the ordinary shadow-fade pair; the fade arithmetic is not decompiled.)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The ~~15~~ 18 asset paths *(corrected 2026-10-02, OPUS: §2)* | authored strings in the authorized EXE, extracted verbatim | 2 |
| Post-processing class hierarchy | mangled RTTI names `PGlow`/`PGlowBase`/`PGlowGPUBase`/`PGlowD3D11` etc. | 4 |
| Render entry-point names | authored strings | 2 |
| ~150 reflected member names | authored strings, `m<Name>` convention | 2 |
| These are `PClassDataMember` names | the reflection document proves each member descriptor holds its name as an embedded string | 1 |
| SMAA is genuinely wired | `searchtex.dds` + `areatexdx10.dds` are SMAA's two required lookup textures | 2 |
| 3-split cascaded shadows | `mCascadePartition0/1/2` | 2 |
| AO grid is 2 x 2 x 3 | the twelve names enumerate exactly | 2 |
| Family sizes | GFZ `CodeDomain` tag census | 3 |

### Extraction artifacts, counted and excluded

The regex `\bm[A-Z][A-Za-z0-9]{3,40}\b` over ASCII runs returned **160 matches**. Ten are not
member names — they are the pattern firing on non-string binary data:

```
mVujnXtVl   mMzwsT   mEHOB
mBBCoBBCpBBCrBBCsBBCuBBBvBBCxBBCyBBC     mBBCoBBCpBBCsBBCtBBCuBBCvBBCyBBCzBBC
mBBCoBBCpBBCrBBCsBBCuBBCvBBCxBBByBBC     mCCDoBBCqBBCrBBCtCCDvBBCwBBCxBBCyCCC
mFFGoEEFpFFGrEEFsFFGuEEFvFFGxEEFyEEF     mFFGoEEGpFFGsEEFtFFGuEEFvFFGyEEFzEFF
mFFGoEEFpFFGrEEFsFFGuEEFvEEFxEEFyEEF
```

The repeating `BBC`/`EEF`/`FFG` triplets are the tell — that is structured binary, not English.
**So the real count is ~150, and this document says "roughly 150" rather than "160".**

A string scan over a 32 MB binary will always produce some of these. Reporting the raw match count
as a finding would have inflated it by 7 %, and the artifacts are listed here so the number can be
checked rather than trusted.

### Why the tier is 2, not 1

Almost everything here is an **authored string**, which is tier 2 — strong, and in some ways more
trustworthy than a decompilation, since these names were typed by the developers. But a name is
not a behaviour. `mDofApertureFnumber` tells us the parameter is an f-number; it does not tell us
the blur kernel. Nothing in §2 claims what any parameter numerically does, and §4 deliberately
contains no formula.

`0059E070` (Vignette) was decompiled and is recorded as elided rather than summarised, for the
same empty-block reason as elsewhere in this database.

## 8b. Reopened 2026-09-02 - W-1 answered: the values are JSON and INI

**The parameter values live in data files, and some of them are loose on disk right now.**

### JSON

The string `.json` sits inside the same `.rdata` window as the parameter names
(`0x8FA000`-`0x8FC400`). The full set of JSON paths in the binary:

```
JsonData/init.json
JsonData/UISize/UISize.json
JsonData/UISize/UISize_sd.json
JsonData/debugMenuSettings.json
JsonData/MonsterGallery.json
JsonData/0.json
/Tools/AutoTest/MapIndex.json
_2ndScreen.json
```

`JsonData/UISize/UISize.json` is where the UI group belongs - `mGambitPositionOffsetX`,
`mCursorRightX`, `mCommandMenuOffsetY`. The `_sd` variant is a standard-definition layout.
`JsonBox` (4 functions) is the linked JSON parser.

The three registration functions that reference these names are the game's own code, not the
reflection static-init region:

| Function | Size | References |
|---|---:|---|
| `001C3D50` | 4,607 B | `mDofApertureFnumber`, `mSAORadiusChr`, `mCascadePartition0` - render |
| `001C7940` | 11,445 B | `mMapAmbientColorR`, `mUseLinearTonemap` - map lighting |
| `001CA600` | 8,186 B | `mGambitPositionOffsetX` - UI |

### A second parameter vocabulary

The same `.rdata` window holds names that do **not** use the `m` prefix, so the earlier extraction
missed them - answering **W-8** in the affirmative:

```
lightShaftColorR/G/B/A   lightShaftLength        lightShaftGlareRatio
lightShaftEnable         lightShaftNoiseMask     lightShaftNoiseFrequency
lightShaftAngleAttenuation                       lightShaftMaskDepthThereshold   [sic]
lightShaftDiffractionRing / Radius / Attenuation / SpectrumOrder / OuterColorR/G/B/A
chrCameraLightEnabled    chrFresnelSpecularIntensity / Power / ClampValue / SkinIntensity
lightOrientation / lightHeight  (and 2, 3 variants)
EnableDof  EnableAO  EnableUSM  EnableIBL  EnableYebis  EnableMapNormalMap
ShadowValueR/G/B  ShadowBias  earlyAO  AODepthFullRes
m_iPCFBlurSize  m_iBlurBetweenCascades  m_fBlurBetweenCascadesAmount  m_iPCFBlurSizeForMap
ModelsToPreload  ChangedFileName  TrackingMapScreenRateX/Y  2ndScreen
```

`lightShaftDiffractionRingSpectrumOrder` is a **spectral diffraction ring** - a physically-modelled
lens artifact. The `m_i` / `m_f` Hungarian prefixes mark the PCF shadow-blur group as a third
convention. `EnableYebis` identifies the owner of that machinery.

`mMapShadowFadeRange` and `lightShaftMaskDepthThereshold` are reproduced with the developers own
spelling.

### INI, loose on disk and editable today

`ConfigData/` in the game install is **not** archived. Two files sit there in plain text:

**`GaussianFilterSetting.ini`** - resolution-tiered blur:

| Tier | Resolution range | Kernel |
|---|---|---|
| Custom1 | 0-800 x 0-600 | **15x15** |
| Custom2 | 800-1280 x 600-720 | 7x7 |
| Custom3 | 1280-1600 x 720-900 | 5x5 |
| Custom4 | 1600-1920 x 900-1080 | 3x3 |
| Custom5 | 1920-32767 x 1080-2160 | 3x3 |

`Factor=0.91` and `BlendAmount=0.5` are constant across all five tiers.

**The game blurs harder at lower resolutions** - a 15x15 kernel at 800x600 against 3x3 at 1080p.
That is a deliberate, player-visible softening, and it is editable without touching the archive.

**`keymap.ini`** - 16 buttons, 8 analog axes, 3 key functions, and mouse Left/Middle/Right, all as
numeric codes. *(Anchored 2026-09-30, SWE2-DATA: its `[Setting]` section declares `ButtonCount=16`, `AnalogCount=8`,
`KeyCount=3`, and the `[Button]`, `[Analog]`, `[KeyFunction]` and `[Mouse]` sections hold 16, 8, 3 and 3 entries;
[`rrp_checks.py`](../../_index/candidates/dd-data-4-0930/rrp_checks.py) K1, read from an installed copy's `ConfigData`.)*

### What this changes

W-1 is answered: **values are data, in `JsonData/*.json` inside the VBF archive and in loose
`ConfigData/*.ini`.** The 31 GB `FFXII_TZA.vbf` holds the JSON; `vbfextract.py` is the tool.

~~**W-2 remains open** - the `Map` prefix still suggests per-area values, and nothing here proves
whether `JsonData/0.json` is one area or a global.~~ *(Corrected 2026-09-30, SWE2-DATA: W-2 is answered in §8c — per
area, 459 map files over 176 global defaults.)*

## 8c. Reopened 2026-09-02 - W-2 answered: the values, extracted

The data files were pulled out of the retail `FFXII_TZA.vbf` (31,196,932,183 bytes) with
`vbfextract.py`. **W-2 is answered: the values ARE per-area.**

### The layout

| Path | Count / size | Role |
|---|---|---|
| `jsondata/init.json` | **176 keys** | global defaults |
| `jsondata/maps/<mapcode>.json` | **459 files** | per-area overrides |
| `jsondata/uisize/uisize.json` | 231 keys | UI layout (separate document) |

**The per-map files are strict overrides.** `alc0101.json` holds 39 keys and **every one of them
also exists in `init.json`** - zero keys appear in a map file that are not in the defaults. That
was checked, not assumed.

### Real values, from `jsondata/maps/alc0101.json`

```json
{
  "mDofFocusDistance": 2.358,
  "mDofApertureFnumber": 100.0,
  "mDofSpecialApertureFnumber": 10.3,
  "mGlareLuminance": 2,
  "mGlareThreshold": 0.2,
  "mShadowValueLerpMinForMap": 0.65,
  "mShadowValueLerpMinForChr": 0.9,
  "m_iPCFBlurSizeForMap": 7,
  "mCascadePartition0_1": 0.006,
  "lightHeight": 80.06,
  "lightOrientation": -45,
  "mSAOBiasSce": 10,   "mSAORadiusSce": 1,
  "mHBAOBiasSce": 30,  "mHBAORadiusSce": 1.25,
  "mSAOFadeoutScale": 3, "mHBAOFadeoutScale": 5,
  "mMapLightColorR": 0.9, "mMapLightColorG": 0.9, "mMapLightColorB": 0.9
}
```

### Global switches, from `jsondata/init.json`

```json
"EnableAO": 1,   "EnableAutoExposure": 1,  "EnableDof": 1,   "EnableIBL": 1,
"EnableMapNormalMap": 1,  "EnableShadow": 1,  "EnableUSM": 0,  "EnableYebis": 1
```

**`EnableYebis` is a JSON key and it is on** - which answers **X-3** in the third-party inventory.
`EnableUSM` is **0**: the unsharp-mask pass ships disabled. `EnableAutoExposure` is a parameter the
string extraction had not surfaced.

`mCascadeNumber` is **3**, confirming the three-split cascade read from `mCascadePartition0/1/2`.
The partitions carry a second index (`mCascadePartition0_1`, `_2`, `_3`) matching
`lightHeight2/3` and `lightOrientation2/3` - **three light setups per map**, each with its own
cascade splits. Values in `init.json`: 0.008, 0.016, 0.035.

`ModelsToPreload` is a real asset list:

```
chara/c10/c1004/c1004   chara/c10/c1005/c1005   chara/c10/c1006/c1006
chara/c10/c1019/c1019   chara/c10/c1021/c1021   chara/c10/c1023/c1023
```

### Two data defects that ship in retail

**1. String where a number belongs.** In `init.json`:

```json
"lightShaftColorA": "null",
"lightShaftDiffractionRingOuterColorA": "null",
```

Both are the **string** `"null"`, not JSON `null` and not a float. Both are alpha channels. Every
other one of the 176 values is a float, int or list.

**2. `uisize.json` is not strict-JSON valid** - a trailing comma at line 232. `JsonBox` accepts it;
a strict parser refuses. Detailed in the UI document.

Neither is speculation: the first is visible in the file, the second was reproduced by a strict
parse failing and a lenient parse succeeding on the same bytes.

### What this changes for a modder

The render-parameter list in section 2 stops being a list of names and becomes an editable surface:
**`init.json` for defaults, one of 459 `jsondata/maps/*.json` for a specific area.** Extract with
`vbfextract.py`, edit, repack.

## 8d. Reopened 2026-09-15 — which authored parameters the shipped build actually reads

§8b and §8c established **where** the values live and **that** they are per-area. This asks the next
question: of the names authored in those files, which ones does the executable ever look up? The answer
needed the **complete reader population**, not a sample, so it was derived rather than assumed.

### The reader population is seventeen functions, and it is closed by construction

Every JSON key read in this engine goes through one member lookup, `001FF740` (which wraps `001FF6B0`).
A byte-level `rel32` decode of every call to those two names gives the whole set:

| function | size | key names it spells |
|---|---:|---:|
| `001CA600` | 8,186 B | 226 |
| `001C7940` | 11,445 B | 155 |
| `001C3D50` | 4,607 B | 103 |
| `001C6320` | 2,261 B | 39 |
| `001C76E0` | 357 B | 9 |
| `001C3760` | 1,220 B | 7 |
| `001C6E20` | 1,130 B | 4 |
| `001C5750` / `001C7360` / `001C7520` / `001CC800` | 467 / 446 / 446 / 277 B | 3 each |
| `001C2F50` / `001CC920` | 1,046 / 117 B | 1 each |
| `001C51D0` / `001C52C0` / `001C5530` / `001C5570` | 232 / 227 / 61 / 472 B | 0 — they take the name as an argument |

**Union: 452 distinct key names.** The set is closed in the sense that a key the image never spells
cannot be looked up by a literal — but it can still be **composed at run time**, and this engine does
that (`"PresetDof " + n`, `"MonsterId%d"`, `"fontclut_%d"`). Composed families are therefore excluded
from **both** sides of the comparison below rather than counted as unread.

### The census

Corpus: `jsondata/init.json` + `jsondata/maps/` + `jsondata/cutscenes/` + `jsondata/fontcluts/`,
**797 files parsed**, every key at every depth, with `Cut N`, `PresetDof N`, `MonsterId N` and bare
numeric keys excluded as run-time-composed.

| | count |
|---|---:|
| authored key names, composed families resolved | **260** |
| of those, **read** — as a literal or through a resolved template | **216** |
| authored with **no reader** | **44** |

~~The 50~~ The 44 *(corrected 2026-09-30, SWE2-DATA: the table above counts 44, and the three families below sum to
27 + 7 + 10 = 44)* are not a ragged tail. They are three families:

- **27 × `*CheckBoxCheckState`** — editor widget state, three per parameter (plain, `Lock`, `UseState`).
- **7 × `*Lock`** — editor lock flags: `EnableDofLock`, `EnableYebisLock`, `mDofApertureFnumberLock`,
  `mDofFocusDistanceLock`, `mGammaValueLock`, `mGlareLuminanceLock`, `mGlareThresholdLock`.
- **10 others**, which split again — and the split is the interesting part.

### Nine of the ten are a superseded generation of names, and the files prove it

`mSAOBias`, `mSAORadius` and `mSAOIntensity` have no reader; `mSAOBias**Chr**` / `mSAOBias**Sce**` and
their `Radius` / `Intensity` twins do. If the unsuffixed names were simply dead, old and new would
appear together. They do not:

| old name | files | files that ALSO carry the `Chr` twin | new name | files |
|---|---:|---:|---|---:|
| `mSAOBias` | 21 | **1** | `mSAOBiasChr` / `Sce` | 287 / 741 |
| `mSAORadius` | 20 | **1** | `mSAORadiusChr` / `Sce` | 286 / 741 |
| `mSAOIntensity` | 1 | **0** | `mSAOIntensityChr` / `Sce` | 283 / 283 |

**The old and the new spellings are almost perfectly disjoint**, which is the signature of a rename
that split one value into a character and a scene value, leaving files authored before the split
untouched. `mMapAmbientColorA` (19), `EnableAutoExposure` (4), `mWaterParallax` (3),
`mDebugWaterExtraFactor` (3), `DofImageSensorHeight` (1) and `mClutComment` (28, an authoring comment
beside `mClutIndex`) sit in the same low-count band.

### The cascade group — CORRECTED the same day, 2026-09-15 (FABLE)

**What this section said first, and why it was wrong.** The first version of §8d claimed the `_2` and
`_3` cascade columns were *"current, heavily authored and still unread"* and opened `W-9` to ask why.
**They are read.** `001C7940` does not spell them as literals — it spells the **template**
`"mCascadePartition%d_%d"` (`008FB2D8`) and formats the key at run time, exactly the way `001C3D50`
builds `"PresetDof " + n`. The census that produced the claim compared authored names against
*literals*, so a composed name looked like a dead key. **That is the same error this project caught in
`UQ-339`**, committed here after excluding composed families from the authored side and forgetting the
reader side. The numbers above are the corrected ones.

**The loop, read from the bytes.** `001C9190`–`001C9209`:

```
ebp = 1                                    ; 001C7DE7
outer:  esi = 0
inner:    snprintf(buf, 0x40, "mCascadePartition%d_%d", esi, ebp)   ; 001C91AA, r9d = esi, [rsp+0x20] = ebp
          v = doc[buf]  (fallback 01F813C8)                         ; 001C91B7 - 001C91DF
          001A9B00(obj, ebp - 1, esi, v)                            ; 001C91F8
          esi++ ; while (esi < 3)                                   ; 001C91FF
        ebp++ ; while (ebp <= 3)                                    ; 001C9206
```

**The sink proves the shape.** `001A9B00` (34 B) rejects either index `>= 3` and otherwise stores at
`obj + 0x350 + (row*3 + col)*4` — a **3 × 3 float matrix**. So the shipped build reads **all nine**
`mCascadePartition<c>_<q>` for `c ∈ {0,1,2}`, `q ∈ {1,2,3}`, and the `_1` / `_2` / `_3` suffix is the
matrix's **row**, not an override rank.

**Two corpora, two spellings, and one reader that serves both.** The base name and the suffixed names
almost never share a section:

| where | base `mCascadePartition0` | `_1` | `_2` | `_3` | `mCascadeNumber` |
|---|---:|---:|---:|---:|---:|
| cutscene sidecar `Common` | 281 | 2 | 2 | 2 | 282 |
| flat `maps/*.json` | — | 198 | 244 | 244 | 1 |

`001C3D50` serves the cutscene corpus through `001C52C0`, which takes **two** names and prefers the
second: `mCascadePartition<c>_1` first, the plain name as the fallback (`001C52DB`–`001C5389`). That is
not a quality rank — it is a reader that must find `_1` in a map file and the bare name in a sidecar.

**`mCascadeNumber` is the one cascade key with no reader, and that is explained rather than open.**
It is authored in 284 sections and its value is **`3` in every one of them**. The loop above is
hardcoded to three columns and three rows, and `001A9B00` bounds-checks both indices against `3`. A
count that is invariant and matches a hardcoded bound does not need to be read. **`W-9` is answered on
that basis**, not left open — with the bound that "invariant across the shipped data" is a statement
about the data, not a guarantee about a modified file: authoring `mCascadeNumber: 4` would change
nothing, because nothing reads it.

**The defaults are in the image.** `001EF2D0` writes three immediate floats to a different object's
`+0x870` / `+0x874` / `+0x878` — `0x3C03126F` = 0.008, `0x3C83126F` = 0.016, `0x3D0F5C29` = 0.035 —
and `0.008` is exactly what the base `mCascadePartition0` carries in the sidecars.

### What this does and does not settle

- ~~**`W-3` is bounded, not answered.**~~ *(Corrected 2026-09-30, SWE2-DATA: W-3 was answered 2026-09-18 — no class
  owns the groups, §7.)* The census says which names have a reader and which function
  spells each one; it does not say which *class* owns a group. `001CA600` and `001C7940` between them
  spell 381 of the 452, so the group-to-class map is mostly a question about those two bodies.
- **No claim is made that an unread key is inert.** The bound is explicit: a name composed at run time
  leaves no literal, and this engine composes names. The three excluded families are the ones found;
  a fourth would move keys out of the ~~50~~ 44 *(corrected 2026-09-30, SWE2-DATA)*.
- ~~**`W-9` opens** for the cascade group, which is the only unread family that is current and heavily
  authored.~~ *(Corrected 2026-09-30, SWE2-DATA: W-9 was answered the same day — the `_2` / `_3` columns are read
  through a composed name, and only `mCascadeNumber` has no reader, §7.)*

## 8e. 2026-09-30 - the `softEdges` parameter binding (FABLE, from ASTRA, independently reviewed)

*Consumed from four ASTRA packets after SWE2-AUDIT-SPEC's reviews ([field extent](../../_index/candidates/auditspec-review-astra-softedges-field-extent-0930/REVIEW.md), ACCEPT;
[member boundaries](../../_index/candidates/auditspec-review-astra-softedges-member-boundaries-0930/REVIEW.md), ACCEPT; [pointer keys](../../_index/candidates/auditspec-review-astra-softedges-pointer-keys-0930/REVIEW.md), ACCEPT-WITH-NARROWING;
[preassignment](../../_index/candidates/auditspec-review-astra-softedges-preassignment-0930/REVIEW.md), ACCEPT); FABLE record [`astra-returns-softedges-fable-0930`](../../_index/candidates/astra-returns-softedges-fable-0930/README.md). Static only
(Method A): no native or live run, and nothing here shows a successful load.*

- **What the shipped asset declares.** `PhyreText.fx.phyre` (44,634 bytes, SHA-256 `f67d4492...a767a4cf`) lists its 12
  shader parameter definitions (class 43, `PShaderParameterDefinition`) in list 12. `softEdges` is definition 8: capture
  offset 160, size 8 (the record at file offset 29328). Packed, a definition is 13 bytes; the native copy is 24 bytes,
  with `m_bufferLoc` at native `+0x10` (offset word) and `+0x12` (size word), so the two layouts are not interchangeable.
- **Where the copy lands.** One owner's constructor passes its object `+8` to the binder (`001D03C6`, call at `001D03CA`).
  The binder finds the definition named `softEdges` and copies its bytes to receiver `+0x118` with `memcpy`, after
  masking the size word with `0x1FFF` and refusing unless offset + size fits the capture buffer and offset >= 4. For the
  shipped definition the destination is the owner's `+0x120`..`+0x127`, 8 bytes. No definition in this asset is larger
  than 64 bytes, so this route cannot reach the owner's `+0xAE0` (that would need a size above `0x9C0`).
  **Scope:** the binder has two other callers with other receivers (object `+0x118` in `001C1D40`, and a `0x230`-stride
  element `+0x108` in `001C2980`). The bound covers only the constructor's route.
- **How the parameter object is bound.** Keys 22 and 27 of the asset's pointer fixups resolve to list 12's objects 0..10
  and object 11. The inner array member is `m_els` (native registration string at `00D32DC0`). Its set callback goes through
  a 33-byte dispatcher that answers 21 when its slot is empty. The setter it reaches answers 5 for a negative count and
  writes nothing; otherwise it stores the pointer and `count | 0x80000000`. The callback then overwrites the setter's status
  with 0.
- **The resolver's guard, corrected.** In `0059EC40`, flag bit `0x40` runs an optional query, and a result of **1 allows**
  recursion into a kind-2 member; any other result stops. Bit `0x02` always stops. The address it returns is
  `object + zext32(member offset + child F4 - parent F4)`, modulo 2^64: the sum is 32-bit and zero-extended
  ([the loader page](../../22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md)
  carries the correction).
- **Before the set: a preclear.** The load path writes 0 to `object + sext32(8 - F4)` (`0059CD14`) before the callback, and
  skips that only when bit 6 is set and the count is 1. When the class F4 dword is 0, that is the same `object + 8` the setter
  reads. With a NULL source the setter's cleanup is skipped, so the preclear does not release an old pointer. The parent
  attribution: the descriptor's `+0x78` gets the root `02CF8270` (arg 6) and `+0x70` gets `01F2E330` (arg 2).

**Kept open, all under OV-42.** F4 stays symbolic: "F4 = 0 now, and nothing rebinds it later" is a premise, not a proof.
The actual loaded-list identity, whether the resource loads, the pointers, their lifetime and aliasing, and the other two
binder routes are not established. The pointer-keys review narrows the checker, not the answer: the reducer does not pin
the guard's polarity instructions, and the review re-derived the polarity from the bytes.

## 9. Related

- [`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) — the system that holds these names as `PClassDataMember` embedded strings
- [`../../16-UI/`](../../16-UI/) — the UI layout parameters found by the same extraction belong there
- [`../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md`](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) — how `.phyre` assets are located and loaded
- [`../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md) — when the descriptors carrying these names are built

## 9. Falsification pass 2026-09-02

**Attack chosen.** This document's load-bearing claims are **counts** produced by scanning the
binary for strings: *"15 shader files"* and *"roughly 150"* tuning parameters. Counts from a scan
are falsified by re-running the scan with a differently-shaped filter, so both were recomputed
independently and printed in full rather than sampled.

### SURVIVED: the parameter count

An independent scan applying this document's own regex — `\bm[A-Z][A-Za-z0-9]{3,40}\b` — over
printable runs in the image yields **153** distinct names. The document claims *"roughly 150"*,
derived as 160 raw minus 10 extraction artifacts. **153 sits inside "roughly 150", so the claim
holds.**

The two scans disagree on the raw figure (153 vs 160) and on artifacts (0 vs 10) because they
define a "string" differently — this one extracts printable runs of length ≥ 4 and applies the regex
within each run, which does not reproduce the `mBBCoBBCp…` triplet garbage the document lists. **That
is a difference of instrument, not evidence of an error**, and it is recorded rather than resolved:
the document's decision to enumerate and exclude its artifacts is what makes the disagreement
checkable at all. Both instruments land at ~150.

### OVERTURNED: the asset count is 18, not 15

A scan for every `/GameData/…\.phyre` string in the image returns **18** paths. The three the
document does not list are:

```
/GameData/%s/ArtData/shaders/CopyBuffer.fx.phyre
/GameData/%s/ArtData/shaders/anisolighting.dds.phyre
/GameData/D3D11/ArtData/map/%s/tex/%s.dds.phyre
```

**Why they were missed, and why it matters.** The document's enumeration is of paths containing the
literal `D3D11`. These three spell the API element as **`%s`** — they are `printf` templates filled
in at load time. So the filter excluded exactly the paths that prove the point the document was
making. Section 2 argues that *"the `D3D11` element implies the tree is API-keyed"*; the `%s` paths
are that inference's **direct evidence**, and they were invisible to the scan that produced the
claim.

**The named blind spot: filtering on a literal that the code itself parameterises.** Added to
[`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md).

**The "two directories" claim also falls.** Three directories carry `.phyre` assets — `shaders`,
`font`, and `map/<mapcode>/tex`. Widening the scan to every `/GameData/` string, `.phyre` or not,
returns 23 more and shows the tree is much broader than the shader set:

```
/GameData/%s/ArtData/chr/%s_%s.ah
/GameData/%s/ArtData/chr_shadow/%s%s/%s_%s.ah
/GameData/%s/ArtData/map/proceduralTexture/proceduralTexture_%s.ah
/GameData/D3D11/ArtData/font/{us,jp,ch,cn,kr}/fontlist.ah
/GameData/D3D11/ArtData/map/%s/cubeMapConfigs.txt
/GameData/D3D11/ArtData/map/%s/proceduralTextureConfigs.txt
/GameData/D3D11/ArtData/shared/idmaps.txt
/GameData/D3D11/ArtData/shared/phyremaps.txt
/GameData/D3D11/ArtData/menu/localmap/
```

**For a modder this is the useful part.** The convention is confirmed and wider than documented:
`ArtData` holds at least `shaders`, `font` (with a per-language `fontlist.ah` under `us`, `jp`,
`ch`, `cn`, `kr`), `chr`, `chr_shadow`, `map` (per-map `tex`, `cubeMapConfigs.txt`,
`proceduralTextureConfigs.txt`), `menu/localmap`, and `shared` (`idmaps.txt`, `phyremaps.txt`).
Two of those — `idmaps.txt` and `phyremaps.txt` — are plain-text index files, which is a promising
starting point for anyone mapping asset ids to files.

**Tier unchanged at 2.** Everything above is an authored string. A path proves a file is named, not
what it contains.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — DRIVER (1 edge).** §8d names `001C2F50`, whose caller `0017D6E0` is owned by that layer. `0017D6E0` is a per-frame body that calls it at `0017D831`, having already called `001CC600` at `0017D7CC` — the routine that raises the apply gate `01F81280`. `001C2F50` spells exactly one key, `"MapIndex"` (`008F9E20`, loaded at `001C309A`, `001C3203` and `001C331B` — the only literal in its 1,046 bytes besides the allocator name), so the crossing is the frame **driving** this subsystem once per frame, not sharing a responsibility with it. Nothing on this page reaches back into scheduling. Read from the shipping bytes 2026-09-15 (FABLE).

**Developer — CLIENT (1 edges, one fan-in).** All 1 edges are Developer bodies reaching `00200BE0` on this page. `FUN_001c6320` is the worked example - it is a 2,261-byte routine that opens by zeroing a **`0xD0`-byte** stack block inside a `0x300`-byte frame with a stack cookie. The crossing is **one shared subject with 1 callers on that layer**, not 1 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
- **Resource - CLIENT and SERVICE (4 edges).** `001C5750`, `0059E070` are called by bodies filed to Resource: `0020AC30`, `00637C50`; `0017D6E0`, `0059E070` reach bodies filed to Resource: `001A1220`, `00598040` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (3 edges).** `SaveloadManager_RequestDisableAutosaveList` (`001C1810`) calls `001A1220`; `0017D6E0` reaches `SaveloadManager_GetSingleton` (`001C18E0`) and `SaveloadManager_ProcessPendingCaptureCopy` (`001C1910`).

