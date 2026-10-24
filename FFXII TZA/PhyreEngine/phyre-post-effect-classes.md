---
title: "Phyre post-effect classes: the PhyreEngine post-effect family the game links, which classes have bodies, and the one it runs"
kind: "system"
category: "PhyreEngine"
addresses: "0x00D61E50, 0x00655DC0, 0x006575E0, 0x00657680, 0x006571C0, 0x00657150, 0x006571A0, 0x00657140, 0x0065B8F0, 0x00653CD0, 0x00653B20, 0x0065B270, 0x00652940, 0x0060CD10, 0x0060B980, 0x00640280, 0x00642F50, 0x0018CD90, 0x00645DB0, 0x0065A630, 0x0065A640, 0x00191DA0, 0x0018FD70, 0x001EE8E0, 0x00649070"
---

## What the player sees

One of the game's anti-aliasing paths runs PhyreEngine's own FXAA effect, which the game builds once
inside one of its own rendering objects. The rest of PhyreEngine's post-effect library
(depth of field, glow, motion blur, MLAA, SSAO, screen-space reflection and others) is linked into the
executable, and no shipped file names any of its classes. The
post-processing the player sees otherwise is the game's own (category 17) and YEBIS
([YEBIS post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md)).

## How it works

### The classes

The image's RTTI names 37 classes in `Phyre::PPostProcessing`. Thirty-six of them have a nine-slot
vtable in one block starting at `PPostEffectBase`'s `0x00D61E50`, spaced `0x50` apart, each with
`0x006571C0` in slot 4; the 37th, `PUtilityPostProcessing`, is a separate three-slot class. The chain is
`PPostEffectBase` → `P<Effect>Base` → `P<Effect>D3D11` → `P<Effect>`, with `PDepthOfFieldLayered` and
`PGlowGPUBase` as extra layers.

Every `Base` and `D3D11` class, and `PMLAA`, `PScreenSpaceAmbientOcclusion` and
`PMeshParticleSystemBase`, overrides only slot 0, its destructor. `PLowResParticles` overrides slot 5
as well. Nine leaf classes override the render slot and have workers:

| Class | Overrides | Slot 6 | Worker | Passes named by the worker |
|---|---|---|---|---|
| `PAtmospherics` | 1 2 6 | `0x0065B270` | `0x00658470` | `RenderTextures`, `RenderAtmosphere`, `RenderAtmosphereInverted` |
| `PCelShading` | 1 2 6 | `0x0065B340` | `0x006587F0` | `Cel`, `CelInverted` |
| `PDeferredLighting` | 1 2 3 5 6 | `0x0065B400` | `0x00659EC0`, `0x0065A960` | `CompositeToScreenTiled`, `CompositeToScreen`; `RenderPointLight`, `RenderSpotLight`, `RenderDirectionalLight` |
| `PDepthOfField` | 1 2 3 6 | `0x0065B4C0` | `0x00658BA0` | `RenderDoFHorizontal`, `RenderDoFVertical`, `RenderDoFComposite` |
| `PFXAA` | 1 2 3 6 | `0x0065B590` | `0x0065A640` | `RenderRGBL`, `RenderFXAA`, `RenderFXAAInverted` |
| `PGlow` | 1 2 3 6 | `0x0065B650` | `0x00652940`, `0x00659080` | `GenerateGlowBuffer`; `RenderGaussianBlurX`, `RenderGaussianBlurY`, `RenderGaussianBlurYComposite`, `RenderGaussianBlurYCompositeCombine` |
| `PMaterialPostEffect` | 2 6 | `0x0065B750` | `0x00659A90` | `MaterialPostEffect`, `MaterialPostEffectInverted` |
| `PMotionBlur` | 1 2 3 6 | `0x0065B820` | `0x00659C20` | `RenderCameraMotionBlur`, `RenderCameraMotionBlurInverted` |
| `PScreenSpaceReflection` | 1 2 3 5 6 | `0x0065B920` | `0x0065BA00` | `ScreenSpaceReflectionPrePass`, `DownsampleScreenSpaceReflectionDepth`, `RenderScreenSpaceReflection`, `CompositeScreenSpaceReflection` |

The pass names are the render-pass records the worker references; each record is registered at start-up
by a CRT initializer calling `0x005DC6F0(record, name, 0)` (60 such registrations in the image).

### The vtable

| Slot | Base body | What it does |
|---|---|---|
| 0 | per class | deleting destructor |
| 1 | `0x00655DC0` | configure at a size: a zero width or height takes `+0x538` / `+0x53C` of the static render context returned by `0x005FD050`; writes `+0x44`, `+0x48` and sets `+0x40` |
| 2 | `0x006575E0` | refresh the cache: `+0x18` = `[+0x10]`, `+0x20` = `[[+0x10]+8]`, `+0x28` = `[[[+0x10]+8]+0x18]`, zero where the chain is null |
| 3 | `0x00657680` | set `+0x44` and `+0x48` directly |
| 4 | `0x006571C0` | ready: `+0x10` non-null, `[+0x10]` non-null and `+0x41` set |
| 5 | `0x00657150` | pass query: when ready, returns the third argument only for the pass record `0x01F2D6E0` (`Transparent`) |
| 6 | `0x0065B8F0` | render: when `+0x40` is clear, calls slot 1 with `+0x28` / `+0x2C` of the fourth argument (0, 0 when null) |
| 7 | `0x00653CD0` | returns `+0x44` |
| 8 | `0x00653B20` | returns `+0x48` |

`0x005FD050` returns the address of the static `0x02CC0410` on every path, and `0x00655DC0` adds `0x520`
before its null test, so its 1280 × 720 fallback never runs. `PScreenSpaceReflection`'s slot 5
(`0x006571A0`) answers for `0x01F2D700` (`DeferredRender`) without the readiness test;
`PDeferredLighting` and `PLowResParticles` use `0x00657140`, which returns 0.

### The render slot

A slot-6 override (`PAtmospherics`'s `0x0065B270` is the shape all nine share):

1. configures through slot 1 as the base does, returning a non-zero result;
2. returns 5 when the fourth argument is null;
3. calls slot 2 when `+0x10`, `[+0x10]+8` or that object's `+0x18` no longer matches the cache;
4. returns `0x15` when `+0x10` or `[+0x10]` is null, else calls its worker.

A worker (for example `0x00652940`, `PGlow`'s first) pushes its parameter records, runs the render-state
helpers `0x0060D4F0`, `0x0060DB50`, `0x005FEFD0` and `0x0060CD70` on the context, stores a pass record at
context `+0x80`, builds a `PMaterialSelectorMaterialSet` on its stack (vtable `0x008C6C98`, items =
effect `+0x30`), calls `0x0060B980`, and ends with `0x00600A60`. The selector's one method, `0x0060CD10`,
returns the item at the index it is given, or null past the end. `0x0060B980` then selects the effect
variant as on [Shader variant selection](shader-variant-selection.md).

### How instances come to exist

Each class's `PClassDescriptorConcrete<T>` vtable carries a construct-in-place factory at slot 10
(`+0x50`); for `PAtmospherics` it is `0x00640280` at `0x00D5B0C0`, which runs the base constructor and stores
the class vtable and descriptor. The 35 descriptor vtables of the family (none exists for
`PDepthOfFieldLayered`) and the manager's have 36 distinct slot-10 bodies, and none has a direct call
site in `.text`; nor does any of the ten slot-6 bodies. They are reached only through the reflection
loader and through vtables.

`PPostEffectManager` has no vtable of its own. Its factory `0x00642F50` (slot 10 of `0x00D5E020`) zeroes a
`0x28`-byte object: a dword and four qwords.

### The PFXAA the game runs

The game constructs one `PFXAA` itself. Its constructor `0x0018CD90` calls `0x00645DB0` on its own `+0x378`
at `0x0018CFD5`; `0x00645DB0` runs the base constructor, zeroes `+0x50`–`+0x68`, and stores the `PFXAA` vtable
`0x00D625D0` and the descriptor `0x02D35FA0`. The same constructor sets `+0x3E8` to 1. `0x0018D850` configures
the member (`0x00654160`, `0x00656B10`: render target, `ColorBuffer`, `InvColorBufferSize`,
`LinearClampSampler`) and then sets `+0x3E9`.

`0x0065A630` jumps to the worker `0x0065A640`; it is called from two places:

- `0x00191DA0`, when `+0x3E8` and `+0x3E9` are set and `+0x4A3` is 0 (when `+0x4A3` is set it runs the
  game's `0x001925D0` instead), with source `[+0x290]`;
- `0x0018FD70`, called from `0x00187950`, with source `[+0x278]`.

Both then call `0x001EE8E0` (`0x0018FDDF`, `0x00191E70`), the game's shared copy pass, which has 17 call
sites in all: it sets `ColorBuffer`, `ColorBufferSampler` and
`ColorBufferOffset` on the material at `[0x01F82E58]+0x20`, picks the `Opaque`, `OpaqueRGB` or another pass
record by the target's format, and submits one draw through `0x0060B980`.

## Layouts

PPostEffectBase (the fields the base slots use):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `void*` | m_effectMaterial | registered at `0x00649101` by `0x00649070` |
| `+0x18` | `void*` | cached | [+`0x10`] |
| `+0x20` | `void*` | cached | [[+`0x10`]+`0x08`] |
| `+0x28` | `void*` | cached | [[[+`0x10`]+`0x08`]+`0x18`] |
| `+0x30` | `...` | material items | the array a worker's selector indexes |
| `+0x40` | `u8` | configured | set by slot 1 |
| `+0x41` | `u8` | m_enabled | registered at `0x00649170` |
| `+0x44` | `u32` | width |  |
| `+0x48` | `u32` | height |  |

The generated class table is
[phyre-post-effect-classes-posteffect-class-family.tsv](phyre-post-effect-classes-posteffect-class-family.tsv). Instruction-level
access tables per class:

| Class | Table |
|---|---|
| `PPostEffectBase` | [phyre-post-effect-classes-p-post-effect-base-accesses.tsv](phyre-post-effect-classes-p-post-effect-base-accesses.tsv) |
| `PPostEffectManager` | [phyre-post-effect-classes-ppost-effect-manager-accesses.tsv](phyre-post-effect-classes-ppost-effect-manager-accesses.tsv) |
| `PAtmosphericsBase` | [phyre-post-effect-classes-patmospherics-base-accesses.tsv](phyre-post-effect-classes-patmospherics-base-accesses.tsv) |
| `PCelShadingBase` | [phyre-post-effect-classes-pcel-shading-base-accesses.tsv](phyre-post-effect-classes-pcel-shading-base-accesses.tsv) |
| `PDeferredLightingBase` | [phyre-post-effect-classes-p-deferred-lighting-base-accesses.tsv](phyre-post-effect-classes-p-deferred-lighting-base-accesses.tsv) |
| `PDeferredLightingD3D11` | [phyre-post-effect-classes-pdeferred-lighting-d3-d11-accesses.tsv](phyre-post-effect-classes-pdeferred-lighting-d3-d11-accesses.tsv) |
| `PDepthOfFieldBase` | [phyre-post-effect-classes-pdepth-of-field-base-accesses.tsv](phyre-post-effect-classes-pdepth-of-field-base-accesses.tsv) |
| `PDepthOfFieldD3D11` | [phyre-post-effect-classes-pdepth-of-field-d3-d11-accesses.tsv](phyre-post-effect-classes-pdepth-of-field-d3-d11-accesses.tsv) |
| `PFXAABase` | [phyre-post-effect-classes-pfxaabase-accesses.tsv](phyre-post-effect-classes-pfxaabase-accesses.tsv) |
| `PGlowBase` | [phyre-post-effect-classes-pglow-base-accesses.tsv](phyre-post-effect-classes-pglow-base-accesses.tsv) |
| `PMaterialPostEffect` | [phyre-post-effect-classes-pmaterial-post-effect-accesses.tsv](phyre-post-effect-classes-pmaterial-post-effect-accesses.tsv) |
| `PMLAABase` | [phyre-post-effect-classes-pmlaabase-accesses.tsv](phyre-post-effect-classes-pmlaabase-accesses.tsv) |
| `PMotionBlurBase` | [phyre-post-effect-classes-pmotion-blur-base-accesses.tsv](phyre-post-effect-classes-pmotion-blur-base-accesses.tsv) |
| `PScreenSpaceAmbientOcclusionBase` | [phyre-post-effect-classes-pscreen-space-ambient-occlusion-base-accesses.tsv](phyre-post-effect-classes-pscreen-space-ambient-occlusion-base-accesses.tsv) |
| `PScreenSpaceReflectionBase` | [phyre-post-effect-classes-pscreen-space-reflection-base-accesses.tsv](phyre-post-effect-classes-pscreen-space-reflection-base-accesses.tsv) |

### The deferred lights

`PDeferredLightingBase` holds 129 light slots of `0x80` bytes: 128 at `+0x50`, drawn in order up to the count `+0x4110`, and one at `+0x4050`, drawn first (`0x0065A46C`-`0x0065A4A4`). The light renderer `0x0065A960` (slot in `r8`) turns a slot into the shader parameters whose handles `0x00656936`-`0x006569D7` and `0x00654C23`-`0x00654C40` look up by name (`DeferredPos`, `DeferredDir`, `DeferredColor`, `DeferredSpotAngles`, `DeferredAttenParams`, `DeferredShadowMask`, `DeferredWorldTransform`). The constructor `0x006458A0` gives every slot the defaults below (`0x006458E0`-`0x00645977`).

`PDeferredLightingSlot0080` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | yAxisX | x of the light's y axis, row 1 of the DeferredWorldTransform the light renderer `0x0065A960` builds (`0x0065AB05`) and scales by the light's width (`0x0065AD47`); 0 from the constructor `0x006458A0` (`0x006458E0`) |
| `+0x04` | `f32` | yAxisY | y of the light's y axis (`0x0065AB0A`, scaled at `0x0065AD42`); 1.0 from the constructor (`0x006458E2`) |
| `+0x08` | `f32` | yAxisZ | z of the light's y axis (`0x0065AB10`, scaled at `0x0065AD3A`); 0 from the constructor (`0x006458E2`) |
| `+0x0C` | `f32` | xAxisX | x of the light's x axis, row 0 of the DeferredWorldTransform (`0x0065AAE6`), scaled by the light's width (`0x0065ADE5`); 1.0 from the constructor (`0x00645906`) |
| `+0x10` | `f32` | directionX | x of the light's direction (its z axis): `0x0065A960` sends +`0x10`/+`0x14`/+`0x18` as the shader parameter DeferredDir (`0x0065AA63`-`0x0065AAC2`) and as row 2 of the DeferredWorldTransform scaled by the range +`0x58` (`0x0065AB2D`, `0x0065ACC2`); 0 from the constructor (`0x006458EA`) |
| `+0x14` | `f32` | directionY | y of the light's direction (`0x0065AA68`, `0x0065AB32`, `0x0065ACBD`); 0 from the constructor (`0x006458EE`) |
| `+0x18` | `f32` | directionZ | z of the light's direction (`0x0065AA63`, `0x0065AB37`, `0x0065ACB5`); 1.0 from the constructor (`0x006458F1`) |
| `+0x1C` | `f32` | xAxisY | y of the light's x axis (`0x0065AAE0`, scaled at `0x0065ADD3`); 0 from the constructor (`0x0064590D`) |
| `+0x20` | `f32` | positionX | x of the light's position: `0x0065A960` sends +`0x20`/+`0x24`/+`0x28` as the shader parameter DeferredPos (`0x0065A9EC`-`0x0065AA46`) and as row 3 of the DeferredWorldTransform (`0x0065AB52`); 0 from the constructor (`0x006458F8`) |
| `+0x24` | `f32` | positionY | y of the light's position (`0x0065A9F2`, `0x0065AB57`); 0 from the constructor (`0x006458F8`) |
| `+0x28` | `f32` | positionZ | z of the light's position (`0x0065A9EC`, `0x0065AB5D`); 0 from the constructor (`0x006458FC`) |
| `+0x2C` | `f32` | xAxisZ | z of the light's x axis (`0x0065AADA`, scaled at `0x0065ADC8`); 0 from the constructor (`0x00645910`, after 1.0 at `0x006458FF`) |
| `+0x30` | `f32[4]` | colour | the light's colour, copied whole into the shader parameter DeferredColor (`0x0065AF27`-`0x0065AF79`); four 1.0 from the constructor (`0x00645913`-`0x00645928`) |
| `+0x40` | `u8[16]` | bytes040 | 16 bytes the constructor sets to 0 (`0x00645928` high half, `0x00645930`, `0x00645934` low half); the light renderer `0x0065A960`, the only reader of the slots in the census of the class's methods, reads none of them (every slot displacement it uses is listed in Project notes); nothing fixes the width |
| `+0x50` | `i32` | kind | the light kind: `0x0065A960` submits the pass `0x02D373C0` with the object at +`0x4120` for 0 (`0x0065B109`-`0x0065B151`), the pass `0x02D373E0` with +`0x4128` for 2 (`0x0065B164`-`0x0065B1AA`) and the pass `0x02D37400` with the class's material items +`0x30` for 1 (`0x0065B1B6`-`0x0065B1EE`); 2 is the spot light, whose transform takes its width from the cone angle +`0x60` (`0x0065ABB5`-`0x0065ABCF`); 0 from the constructor (`0x00645934`) |
| `+0x54` | `f32` | attenuationStart | the first value of the shader parameter DeferredAttenParams (`0x0065B02D`-`0x0065B085`): the distance where the fall-off starts; 50.0 from the constructor (`0x00645938`) |
| `+0x58` | `f32` | range | the light's range: the second value of DeferredAttenParams (`0x0065B028`) and the scale of the transform's direction row and, for kinds other than 2, of its width (`0x0065ABA1`-`0x0065ABAC`); 100.0 from the constructor (`0x0064593F`) |
| `+0x5C` | `f32` | innerConeAngle | the spot light's inner angle: DeferredSpotAngles is (inner - 1e-6, outer + 1e-6, cos of each) (`0x0065AF8E`-`0x0065AFCF`); 0 from the constructor (`0x0064593F` high half) |
| `+0x60` | `f32` | outerConeAngle | the spot light's outer angle: the second and fourth DeferredSpotAngles values (`0x0065AF8E`-`0x0065AFA1`), and for kind 2 the transform's width is tan(angle) * range (`0x0065ABBB`-`0x0065ABCF`); 1.0 from the constructor (`0x00645947`) |
| `+0x64` | `i32` | castsShadow | non-zero when the light casts a shadow: DeferredShadowMask is all 0 when it is 0, otherwise 1.0 in the channel +`0x68` (`0x0065B096`-`0x0065B0B2`); 0 from the constructor (`0x00645947` high half) |
| `+0x68` | `i32` | shadowChannel | the shadow-mask channel, 0 to 3, set to 1.0 in DeferredShadowMask (`0x0065B0A3`-`0x0065B0A6`); 0 from the constructor (`0x0064594F`) |
| `+0x6C` | `f32` | f32One006C | 1.0 from the constructor (`0x00645952`); the light renderer `0x0065A960`, the only reader of the slots in the census of the class's methods, does not read it |
| `+0x70` | `f32` | f32Max0070 | 3.4028235e38 (FLT_MAX, `0x7F7FFFFF`) from the constructor (`0x00645959`); the light renderer `0x0065A960` does not read it |
| `+0x74` | `u8[12]` | tail074 | 12 bytes the constructor sets to 0 (`0x00645959` high half, `0x00645961`); the light renderer `0x0065A960` reads none of them; nothing fixes the width |

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PAtmosphericsBase` (`0x288` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x61` | `u8` | m_renderDebugTextures | m_renderDebugTextures (u8), registered by `0x00648100` (`0x00632960` at `0x006485E4`); no shipped .phyre file declares PAtmosphericsBase; the constructor `0x00645520` clears it with +`0x60` (word store `0x0064554C`) |
| `+0x90` | `f32[4]` | m_betaR | m_betaR (f32[4]), registered by `0x00648100` (`0x00632960` at `0x006482DB`); no shipped .phyre file declares PAtmosphericsBase; the constructor `0x00645520` sets it to (0.0058, 0.0135, 0.0331) (`0x00645571`-`0x00645585`) |
| `+0xA0` | `f32[4]` | m_betaM | m_betaM (f32[4]), registered by `0x00648100` (`0x00632960` at `0x0064834A`); no shipped .phyre file declares PAtmosphericsBase; the constructor `0x00645520` sets it to (0.004, 0.004, 0.004) (`0x0064558F`-`0x006455A3`) |
| `+0xCC` | `f32[4]` | m_sunDir | m_sunDir (f32[4]), registered by `0x00648100` (`0x00632960` at `0x00648506`); no shipped .phyre file declares PAtmosphericsBase; the constructor `0x00645520` sets it to (0, 1, 0): its qword stores write 20.0 to +`0xC8` and 0 to +`0xCC`, then 1.0 to +`0xD0` and 0 to +`0xD4` (`0x006455E9`, `0x006455F4`) |

`PCelShadingBase` (`0xC0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x64` | `f32[4]` | m_lightColor | m_lightColor (f32[4]), registered by `0x00648620` (`0x00632960` at `0x006487FB`); no shipped .phyre file declares PCelShadingBase; the constructor `0x006457E0` sets it to (1, 1, 1, 1) (`0x00645813`-`0x00645828`) |
| `+0x74` | `f32[4]` | m_edgeColor | m_edgeColor (f32[4]), registered by `0x00648620` (`0x00632960` at `0x0064886A`); no shipped .phyre file declares PCelShadingBase; the constructor `0x006457E0` sets it to (0, 0, 0, 1) (`0x00645828`-`0x00645834`) |
| `+0x84` | `u8[60]` | bytes84 | the bytes after m_edgeColor (+`0x74`) up to the end of the `0xC0`-byte class; the constructor `0x006457E0` clears +`0x88` to +`0xBF` (`0x0064583E`-`0x00645868`); no registered member covers it (`0x00644100` registers the `0xC0`-byte class at `0x0064414A`) |

`PDeferredLightingBase` (`0x41D8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x40D0` | `f32[4]` | m_ambientColor | the ambient colour: the composite worker `0x00659EC0` reads its four floats as a parameter value (`0x0065A41F`-`0x0065A43D`) and `0x006515C0` passes its address as one (`0x00652336`); m_ambientColor (f32[4]), registered by `0x006488A0` (`0x00632960` at `0x0064892E`); no shipped .phyre file declares PDeferredLightingBase |
| `+0x40E0` | `f32[4]` | m_fogColor | the fog colour: the composite worker `0x00659EC0` passes its address as a parameter value (`0x0065A26B`); m_fogColor (f32[4]), registered by `0x006488A0` (`0x00632960` at `0x00648C37`); no shipped .phyre file declares PDeferredLightingBase |
| `+0x40F8` | `f32` | m_fogAmount | the fog amount: the composite worker `0x00659EC0` writes it as the fourth float of the fog parameter (`0x0065A1F3`-`0x0065A20A`); m_fogAmount (f32), registered by `0x006488A0` (`0x00632960` at `0x00648BC8`); no shipped .phyre file declares PDeferredLightingBase |
| `+0x40FC` | `f32[3]` | floats40FC | three floats the constructor `0x006458A0` sets to 1.0, 0 and 1.0 (`0x00645A9B`, `0x00645AA6`); no registered member covers it (`0x006442E0` registers the `0x41D8`-byte class at `0x0064432A`) |
| `+0x4114` | `u32` | passState | a state the lighting code steps: 0 from the constructor `0x006458A0` (`0x00645AC5`); `0x006553D0` tests it for 0 (`0x006553DA`) and sets it to 3 (`0x006555AC`); `0x00655690` tests it for 0 (`0x0065569D`); `0x0065C330` reads it (`0x0065C345`); the composite worker `0x00659EC0` compares it with 3 (`0x00659EF8`); no registered member covers it (`0x006442E0` registers the `0x41D8`-byte class at `0x0064432A`) |
| `+0x4118` | `void*` | materialCopy | the lighting pass's own copy of the effect material: `0x00654B00` makes it with `0x00600120` (stored at `0x00654B6E`) and copies m_effectMaterial's parameter buffer into it when the sizes match (`0x00654B79`-`0x00654B95`); the workers `0x00650D40`, `0x006515C0`, `0x006525F0`, `0x00659EC0` and `0x0065A960` read it for every pass parameter they set (for example `0x0065218C`, `0x00659F85`); no registered member covers it (`0x006442E0` registers the `0x41D8`-byte class at `0x0064432A`) |
| `+0x4120` | `void*` | pointer4120 | a pointer `0x00655EC0` sets (`0x00655EE2`) and `0x0065D2A0` releases and clears (`0x0065D2C2`, `0x0065D2D6`); `0x00654B00` returns `0x15` while it is null (`0x00654B0F`) and passes it on (`0x00654BCB`), as does `0x0065A960` (`0x0065B11E`); `0x006568D0` tests it (`0x006568DA`); 0 from the constructor `0x006458A0` (`0x00645AD2`); no registered member covers it (`0x006442E0` registers the `0x41D8`-byte class at `0x0064432A`) |
| `+0x41D1` | `u8[7]` | pad41D1 | the bytes after m_instantLightsEnabled (u8 at +`0x41D0`) up to the end of the `0x41D8`-byte class; no registered member covers it (`0x006442E0` registers the `0x41D8`-byte class at `0x0064432A`) |

`PScreenSpaceReflectionBase` (`0xB0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x50` | `f32` | m_minReflectionDirZ | m_minReflectionDirZ (f32), registered by `0x006496A0` (`0x00632960` at `0x0064972E`); no shipped .phyre file declares PScreenSpaceReflectionBase; the constructor `0x00646250` sets it to 0 (`0x00646271`) |

`PDepthOfFieldBase` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x5C` | `u8[36]` | bytes5C | the bytes after m_focusBlurRange (+`0x58`) up to the end of the `0x80`-byte class; no registered member covers it (`0x006444C0` registers the `0x80`-byte class at `0x0064450A`) |

`PGlowBase` (`0xA0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x68` | `u8[56]` | bytes68 | the bytes after m_glowLuminanceScale (+`0x64`) up to the end of the `0xA0`-byte class; the constructor `0x00645E50` clears them (`0x00645E75`-`0x00645E98`); no registered member covers it (`0x00644880` registers the `0xA0`-byte class at `0x006448CA`) |

`PPostEffectBase` (`0x50` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u8[8]` | bytes08 | cleared by the base constructor `0x006461B0` (`0x006461D2`); no registered member covers it (`0x00645000` registers the `0x50`-byte class at `0x00645050`) |
| `+0x34` | `u8[4]` | bytes34 | the four bytes between the dword at +`0x30` and the pointer at +`0x38`; no registered member covers it (`0x00645000` registers the `0x50`-byte class at `0x00645050`) |
| `+0x42` | `u8[2]` | pad42 | alignment bytes after m_enabled (u8 at +`0x41`) up to width (+`0x44`); no registered member covers it (`0x00645000` registers the `0x50`-byte class at `0x00645050`) |
| `+0x44` | `u32` | width | width: slot 1 `0x00655DC0` writes it (`0x00655E12`), slot 3 `0x00657680` (`0x00657680`), `0x00657690` (`0x006576B6`) and `0x00655AC0` (`0x00655B53`); slot 7 `0x00653CD0` returns it; no registered member covers it (`0x00645000` registers the `0x50`-byte class at `0x00645050`) |
| `+0x48` | `u32` | height | height: slot 1 `0x00655DC0` writes it (`0x00655E08`), slot 3 `0x00657680` (`0x00657685`), `0x00657690` (`0x006576BB`) and `0x00655AC0` (`0x00655B59`); slot 8 `0x00653B20` returns it; no registered member covers it (`0x00645000` registers the `0x50`-byte class at `0x00645050`) |
| `+0x4C` | `u8[4]` | bytes4C | the bytes after height (+`0x48`) up to the end of the `0x50`-byte class; no registered member covers it (`0x00645000` registers the `0x50`-byte class at `0x00645050`) |

## Shipped data

| Fact | Value |
|---|---|
| `.phyre` clusters in the archive | 35,984, all with a decodable packed namespace |
| clusters declaring any `PPostProcessing` class, as a class or a type | 0 |
| clusters declaring `PEffect` | 2,184 |

## State

| Address | What |
|---|---|
| `0x01F2D6E0` | pass record `Transparent`, the base slot 5's answer |
| `0x01F2D700` | pass record `DeferredRender`, `PScreenSpaceReflection`'s answer |
| `0x02CC0410` | the static render context slot 1 reads its default size from |
| game object `+0x378` | the one `PFXAA`, built by `0x0018CD90` |

## Modding notes

- No shipped cluster declares a post-effect class, and the descriptor factories have no direct call
  site; the game's `PFXAA` is built directly by game code at `0x0018CFD5`.
- MLAA and SSAO classes have no render body: an instance would only configure itself.
- The FXAA arm runs only with `+0x3E8` and `+0x3E9` set and `+0x4A3` clear on the game object.

## Related

- [Shader variant selection](shader-variant-selection.md): what `0x0060B980` does with the effect a worker selects.
- [Phyre reflection](phyre-reflection.md): class descriptors and their factory slots.
- [Phyre asset files](phyre-asset-files.md): the packed namespace each cluster carries.
- [YEBIS post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md): the other post-effect library in the executable.
