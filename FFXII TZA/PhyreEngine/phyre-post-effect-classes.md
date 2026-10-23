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
