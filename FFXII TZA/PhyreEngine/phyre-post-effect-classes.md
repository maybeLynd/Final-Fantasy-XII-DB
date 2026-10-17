---
title: "Phyre post-effect classes: the PhyreEngine post-effect family the game links, which classes have bodies, and the one it runs"
kind: "system"
category: "PhyreEngine"
addresses: "00D61E50, 00655DC0, 006575E0, 00657680, 006571C0, 00657150, 006571A0, 00657140, 0065B8F0, 00653CD0, 00653B20, 0065B270, 00652940, 0060CD10, 0060B980, 00640280, 00642F50, 0018CD90, 00645DB0, 0065A630, 0065A640, 00191DA0, 0018FD70, 001EE8E0, 00649070"
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
vtable in one block starting at `PPostEffectBase`'s `00D61E50`, spaced `50`<sub>h</sub> apart, each with
`006571C0` in slot 4; the 37th, `PUtilityPostProcessing`, is a separate three-slot class. The chain is
`PPostEffectBase` → `P<Effect>Base` → `P<Effect>D3D11` → `P<Effect>`, with `PDepthOfFieldLayered` and
`PGlowGPUBase` as extra layers.

Every `Base` and `D3D11` class, and `PMLAA`, `PScreenSpaceAmbientOcclusion` and
`PMeshParticleSystemBase`, overrides only slot 0, its destructor. `PLowResParticles` overrides slot 5
as well. Nine leaf classes override the render slot and have workers:

| Class | Overrides | Slot 6 | Worker | Passes named by the worker |
|---|---|---|---|---|
| `PAtmospherics` | 1 2 6 | `0065B270` | `00658470` | `RenderTextures`, `RenderAtmosphere`, `RenderAtmosphereInverted` |
| `PCelShading` | 1 2 6 | `0065B340` | `006587F0` | `Cel`, `CelInverted` |
| `PDeferredLighting` | 1 2 3 5 6 | `0065B400` | `00659EC0`, `0065A960` | `CompositeToScreenTiled`, `CompositeToScreen`; `RenderPointLight`, `RenderSpotLight`, `RenderDirectionalLight` |
| `PDepthOfField` | 1 2 3 6 | `0065B4C0` | `00658BA0` | `RenderDoFHorizontal`, `RenderDoFVertical`, `RenderDoFComposite` |
| `PFXAA` | 1 2 3 6 | `0065B590` | `0065A640` | `RenderRGBL`, `RenderFXAA`, `RenderFXAAInverted` |
| `PGlow` | 1 2 3 6 | `0065B650` | `00652940`, `00659080` | `GenerateGlowBuffer`; `RenderGaussianBlurX`, `RenderGaussianBlurY`, `RenderGaussianBlurYComposite`, `RenderGaussianBlurYCompositeCombine` |
| `PMaterialPostEffect` | 2 6 | `0065B750` | `00659A90` | `MaterialPostEffect`, `MaterialPostEffectInverted` |
| `PMotionBlur` | 1 2 3 6 | `0065B820` | `00659C20` | `RenderCameraMotionBlur`, `RenderCameraMotionBlurInverted` |
| `PScreenSpaceReflection` | 1 2 3 5 6 | `0065B920` | `0065BA00` | `ScreenSpaceReflectionPrePass`, `DownsampleScreenSpaceReflectionDepth`, `RenderScreenSpaceReflection`, `CompositeScreenSpaceReflection` |

The pass names are the render-pass records the worker references; each record is registered at start-up
by a CRT initializer calling `005DC6F0(record, name, 0)` (60 such registrations in the image).

### The vtable

| Slot | Base body | What it does |
|---|---|---|
| 0 | per class | deleting destructor |
| 1 | `00655DC0` | configure at a size: a zero width or height takes `+538`<sub>h</sub> / `+53C`<sub>h</sub> of the static render context returned by `005FD050`; writes `+44`<sub>h</sub>, `+48`<sub>h</sub> and sets `+40`<sub>h</sub> |
| 2 | `006575E0` | refresh the cache: `+18`<sub>h</sub> = `[+10h]`, `+20`<sub>h</sub> = `[[+10h]+8]`, `+28`<sub>h</sub> = `[[[+10h]+8]+18h]`, zero where the chain is null |
| 3 | `00657680` | set `+44`<sub>h</sub> and `+48`<sub>h</sub> directly |
| 4 | `006571C0` | ready: `+10`<sub>h</sub> non-null, `[+10h]` non-null and `+41`<sub>h</sub> set |
| 5 | `00657150` | pass query: when ready, returns the third argument only for the pass record `01F2D6E0` (`Transparent`) |
| 6 | `0065B8F0` | render: when `+40`<sub>h</sub> is clear, calls slot 1 with `+28`<sub>h</sub> / `+2C`<sub>h</sub> of the fourth argument (0, 0 when null) |
| 7 | `00653CD0` | returns `+44`<sub>h</sub> |
| 8 | `00653B20` | returns `+48`<sub>h</sub> |

`005FD050` returns the address of the static `02CC0410` on every path, and `00655DC0` adds `520`<sub>h</sub>
before its null test, so its 1280 × 720 fallback never runs. `PScreenSpaceReflection`'s slot 5
(`006571A0`) answers for `01F2D700` (`DeferredRender`) without the readiness test;
`PDeferredLighting` and `PLowResParticles` use `00657140`, which returns 0.

### The render slot

A slot-6 override (`PAtmospherics`'s `0065B270` is the shape all nine share):

1. configures through slot 1 as the base does, returning a non-zero result;
2. returns 5 when the fourth argument is null;
3. calls slot 2 when `+10`<sub>h</sub>, `[+10h]+8` or that object's `+18`<sub>h</sub> no longer matches the cache;
4. returns `15`<sub>h</sub> when `+10`<sub>h</sub> or `[+10h]` is null, else calls its worker.

A worker (for example `00652940`, `PGlow`'s first) pushes its parameter records, runs the render-state
helpers `0060D4F0`, `0060DB50`, `005FEFD0` and `0060CD70` on the context, stores a pass record at
context `+80`<sub>h</sub>, builds a `PMaterialSelectorMaterialSet` on its stack (vtable `008C6C98`, items =
effect `+30`<sub>h</sub>), calls `0060B980`, and ends with `00600A60`. The selector's one method, `0060CD10`,
returns the item at the index it is given, or null past the end. `0060B980` then selects the effect
variant as on [Shader variant selection](shader-variant-selection.md).

### How instances come to exist

Each class's `PClassDescriptorConcrete<T>` vtable carries a construct-in-place factory at slot 10
(`+50`<sub>h</sub>); for `PAtmospherics` it is `00640280` at `00D5B0C0`, which runs the base constructor and stores
the class vtable and descriptor. The 35 descriptor vtables of the family (none exists for
`PDepthOfFieldLayered`) and the manager's have 36 distinct slot-10 bodies, and none has a direct call
site in `.text`; nor does any of the ten slot-6 bodies. They are reached only through the reflection
loader and through vtables.

`PPostEffectManager` has no vtable of its own. Its factory `00642F50` (slot 10 of `00D5E020`) zeroes a
`28`<sub>h</sub>-byte object: a dword and four qwords.

### The PFXAA the game runs

The game constructs one `PFXAA` itself. Its constructor `0018CD90` calls `00645DB0` on its own `+378`<sub>h</sub>
at `0018CFD5`; `00645DB0` runs the base constructor, zeroes `+50`<sub>h</sub>–`+68`<sub>h</sub>, and stores the `PFXAA` vtable
`00D625D0` and the descriptor `02D35FA0`. The same constructor sets `+3E8`<sub>h</sub> to 1. `0018D850` configures
the member (`00654160`, `00656B10`: render target, `ColorBuffer`, `InvColorBufferSize`,
`LinearClampSampler`) and then sets `+3E9`<sub>h</sub>.

`0065A630` jumps to the worker `0065A640`; it is called from two places:

- `00191DA0`, when `+3E8`<sub>h</sub> and `+3E9`<sub>h</sub> are set and `+4A3`<sub>h</sub> is 0 (when `+4A3`<sub>h</sub> is set it runs the
  game's `001925D0` instead), with source `[+290h]`;
- `0018FD70`, called from `00187950`, with source `[+278h]`.

Both then call `001EE8E0` (`0018FDDF`, `00191E70`), the game's shared copy pass, which has 17 call
sites in all: it sets `ColorBuffer`, `ColorBufferSampler` and
`ColorBufferOffset` on the material at `[01F82E58]+20h`, picks the `Opaque`, `OpaqueRGB` or another pass
record by the target's format, and submits one draw through `0060B980`.

## Layouts

PPostEffectBase (the fields the base slots use):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `10`<sub>h</sub> | `void*` | m_effectMaterial | registered at `00649101` by `00649070` |
| `18`<sub>h</sub> | `void*` | cached | [+`10`<sub>h</sub>] |
| `20`<sub>h</sub> | `void*` | cached | [[+`10`<sub>h</sub>]+`08`<sub>h</sub>] |
| `28`<sub>h</sub> | `void*` | cached | [[[+`10`<sub>h</sub>]+`08`<sub>h</sub>]+`18`<sub>h</sub>] |
| `30`<sub>h</sub> | `...` | material items | the array a worker's selector indexes |
| `40`<sub>h</sub> | `u8` | configured | set by slot 1 |
| `41`<sub>h</sub> | `u8` | m_enabled | registered at `00649170` |
| `44`<sub>h</sub> | `u32` | width |  |
| `48`<sub>h</sub> | `u32` | height |  |

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

## Shipped data

| Fact | Value |
|---|---|
| `.phyre` clusters in the archive | 35,984, all with a decodable packed namespace |
| clusters declaring any `PPostProcessing` class, as a class or a type | 0 |
| control: clusters declaring `PEffect` | 2,184 |

## State

| Address | What |
|---|---|
| `01F2D6E0` | pass record `Transparent`, the base slot 5's answer |
| `01F2D700` | pass record `DeferredRender`, `PScreenSpaceReflection`'s answer |
| `02CC0410` | the static render context slot 1 reads its default size from |
| game object `+378`<sub>h</sub> | the one `PFXAA`, built by `0018CD90` |

## Modding notes

- No shipped cluster declares a post-effect class, and the descriptor factories have no direct call
  site; the game's `PFXAA` is built directly by game code at `0018CFD5`.
- MLAA and SSAO classes have no render body: an instance would only configure itself.
- The FXAA arm runs only with `+3E8`<sub>h</sub> and `+3E9`<sub>h</sub> set and `+4A3`<sub>h</sub> clear on the game object.

## Related

- [Shader variant selection](shader-variant-selection.md): what `0060B980` does with the effect a worker selects.
- [Phyre reflection](phyre-reflection.md): class descriptors and their factory slots.
- [Phyre asset files](phyre-asset-files.md): the packed namespace the census reads.
- [YEBIS post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md): the other post-effect library in the executable.
