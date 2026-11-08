---
title: "Shader variant selection: the eight context-switch axes and the variant key a draw uses"
kind: "system"
category: "PhyreEngine"
addresses: "0x00606A20, 0x0060B980, 0x006B8D20, 0x02E522D0, 0x02E522E0, 0x006B9050, 0x006B9120, 0x006B90A0, 0x006B9070, 0x006B93D0, 0x006B9410, 0x006B93A0, 0x006B9450, 0x006B94C0, 0x006B9630, 0x006B9B90, 0x006B89C0, 0x006B8590, 0x005FDD40, 0x01F2EBC8, 0x00D80EA8"
---

## What the player sees

Nothing directly. Before PhyreEngine draws a mesh it picks which compiled build of the effect's shader
to use: with or without skinning, with a given light set, with or without an LOD crossfade. The pick is
made by eight named switches. In this build every shipped effect authors exactly one variant and an
empty context-switch list, so the pick always lands on that one build; the lookup still runs on every [mesh-instance draw](phyre-mesh-instance-draws.md).

## How it works

### The switch objects

A context switch is a `0x28`-byte object of class `Phyre::PRendering::PContextSwitch` or one of eight
subclasses. Each subclass has one static instance in `.data`, starting at `0x01F2EBC8` and spaced
`0x28` apart. The image carries each object with the base vtable `0x00D80EA8`, its name pointer,
`+0x20` = 0 and `+0x24` = 1; the installer in the CRT initializer table (`0x008C43E8`–`0x008C4420`) then:

1. registers it with `0x006B8D20`;
2. only when that returns 0, adds its word count to the image-wide total `0x02E522E0` and stores the
   count at `+0x20` (3 for `NUM_LIGHTS` at `0x001670F0`, 1 for the others);
3. installs its own vtable at `+0x00` and registers an `atexit` teardown.

`LOW_RES_PARTICLES`'s installer (`0x00167140`) also writes 0 to `+0x24`. After static initialization
`0x02E522E0` is 10.

Each switch's count word `+0x20` is stored by its installer in step 2, and its `atexit` teardown subtracts it from
`0x02E522E0` again:

- `NUM_LIGHTS`: `0x01F2EBE8`, stored at `0x0016710B`, teardown `0x008B5930`;
- `LOD_BLEND`: `0x01F2EC10`, `0x001670BA`, `0x008B58B0`;
- `INSTANCING_ENABLED`: `0x01F2EC38`, `0x0016706A`, `0x008B5830`;
- `SHADER_LOD_LEVEL`: `0x01F2EC60`, `0x001671FA`, `0x008B5AB0`;
- `ORTHO_CAMERA`: `0x01F2EC88`, `0x0016724A`, `0x008B5B30`;
- `INDICES_16BIT`: `0x01F2ECB0`, `0x001671AA`, `0x008B5A30`;
- `SKINNING_ENABLED`: `0x01F2ECD8`, `0x0016729A`, `0x008B5BB0`;
- `LOW_RES_PARTICLES`: `0x01F2ED00`, `0x0016715A`, `0x008B59B0`; its `+0x24` is `0x01F2ED04` (`0x0016716B`).

### Registration

`0x006B8D20(switch)` returns `0x11` when `+0x08` (the name) is null, walks the list headed at
`0x02E522D0` through `+0x10` comparing names byte by byte (case-sensitive), returns `0x12` on a match
without linking, and otherwise links the switch at the head and returns 0.

### Building the key

`0x00606A20(effect, a2, a3, out, record)` is called only from `0x0060BDEF` in `0x0060B980`:

1. When the effect's variant count (`+0x58`, bit `0x80000000` masked off) is 0 it returns −1.
2. It reserves `0x02E522E0 × 4` bytes on the stack, rounded up to 16, `(4 * n + 15) & ~15` with the stack probe
   `0x00808F10` (`0x00606A68`-`0x00606A91`), and points a cursor at the start, so the total is the buffer bound, not the
   key length.
3. For each non-null entry of the effect's switch array (`+0x50`, count `+0x48`) it calls vtable
   slot 2 with seven arguments: the switch, the effect, `a2`, `a3`, the cursor, `out` and `record`.
   A non-zero return stops the loop.
4. The key length is how far the cursor moved, in words.
5. It binary-searches the effect's table at `+0x60` (16-byte entries `{u32 count, words}`; one word is
   stored inline, more through a pointer), ordering first by word count and then word by word, and
   returns the matching index or −1. The bounds start at 0 and the variant count less 1, the probe is
   `mid = (lo + hi) >> 1`, and they move by `lo = max(mid, lo + 1)` and `hi = min(mid, hi - 1)`, not past
   `mid`, until `lo > hi` (`0x00606AFF`-`0x00606BA4`).

`0x0060B980` turns a non-negative index into a 64-byte entry (`0x0060BDFA`: `index << 6` plus the table at
`+0x10` of the entry it selected at `0x0060BD84`–`0x0060BDBF`). On −1 the entry stays null and the draw work under
`0x0060BE13` is skipped; no variant is compiled on demand.

### What each switch reads

Every evaluator writes its words at the cursor, advances it by four per word and returns 0.

| Switch | Evaluator | Writes |
|---|---|---|
| `NUM_LIGHTS` | `0x006B9120` | a bit-packed light code (below) |
| `LOD_BLEND` | `0x006B90A0` | 1 when the LOD weight is neither 0.0 nor 1.0 |
| `INSTANCING_ENABLED` | `0x006B9070` | 1 when `record` is non-null and `record+0x30` is non-null |
| `SHADER_LOD_LEVEL` | `0x006B93D0` | the level at `[[a2+0x40]]+0x38` (0 when `a2+0x40` is null, `0x006B93DA`), clamped to effect `+0x74` − 1 (0 when that is 0) as an unsigned minimum, `level < cap ? level : cap` (`0x006B93E5`-`0x006B93F3`) |
| `ORTHO_CAMERA` | `0x006B9410` | 1 when the float at `[record]+0x6C` is at least 0.01, `0.01 <= f`, or is a NaN (`comiss`, `setbe` at `0x006B9429`-`0x006B9435`); 0 when `record` or `[record]` is null (`0x006B9417`-`0x006B9427`) |
| `INDICES_16BIT` | `0x006B93A0` | 1 when the byte `+0x4C` of `[record+0x38]` equals `0x0C` |
| `SKINNING_ENABLED` | `0x006B9450` | 1 when `a2+0x18` is non-null; with `[record+0x38]` present, also needs its count `+0x08` below `0x79` and `0x00671670` to succeed |
| `LOW_RES_PARTICLES` | `0x006B9050` (the base's) | 1 when the byte `+0x24` is non-zero, so always 0 |

`LOD_BLEND` emits 0 when `a2+0x40` or `a3+0x20` is null; otherwise it reads the first float of the
12-byte element `a3+0x30` of the array at `[a2+0x40]` (`+0x20` count, `+0x28` data). Any index is read: an
index at or past a non-zero count reads past the data, and with a count of 0 the data pointer is null, so the
read is at the address `12 * [a3+0x30]` (`0x006B90C7`-`0x006B90DC`). A NaN weight writes 1 (`0x006B90E4`, `0x006B90EF`).

For a `PCamera` (members registered by `0x006784E0`), `+0x6C` is the last float of `m_projectionMatrix`, the 64-byte matrix at
`+0x30`; an orthographic matrix has 1 there and a perspective one 0.

### NUM_LIGHTS

`0x006B9120` walks the light array at `a3` (`+0x10` count with bit `0x80000000` masked, `+0x18` pointers). It
keeps a light when the mask at `+0x18` of its light type (`light+0x20`) meets the effect's word
`+0x00`. For a kept light it takes the shadow-caster type (`[light+0x18]+0x08`) and uses its index
`+0x1C` when that type's mask `+0x18` meets the effect's `+0x04`, else 0, so a shadowless light is
kept with shadow index 0. Each light becomes `(shadowIndex << 5) | lightTypeIndex`.

The count is the smaller of the kept count and the effect's `+0x70`, `kept < [+0x70] ? kept : [+0x70]`
(`0x006B91F3`-`0x006B91FA`). With a count of 0 it writes one zero word, advances the cursor by 4 and leaves `out` as
it was (`0x006B9366`-`0x006B9373`). With a count above 1 it sorts all the kept lights by that code (`0x006B83C0` with
the comparator `0x006B8930`, `0x006B920A`-`0x006B922B`); with a count of 1 it sorts nothing and takes the first kept
light, even when more were kept.

It zeroes `((10 × count + 35) >> 5) << 2` bytes (`0x00861EC0`, `0x006B9252`) and packs a
4-bit count followed by 10 bits per light. It also copies the kept light pointers to `out+0x00`
onward and the count to `out+0x20`; `0x0060B980` reserves four pointer slots there (`0x0060BA9B`–`0x0060BAB7`).

### Defines for the shader compiler

Slot 3 reads the switch's word back off a cursor, moving it on by 4 (`0x006B94E9`-`0x006B94F2`). The base `0x006B94C0`
appends nothing for 0 and otherwise builds `-D<name>=<value>` from `"-D"` (`0x00D81068`), the name at `+0x08` and
`"="` (`0x01CEBB4C`), and the word (`0x0067AEA0`, `0x006B9587`). `NUM_LIGHTS` overrides it (`0x006B9630`) with
`-DLIGHTTYPE_<i>=` and `-DSHADOWTYPE_<i>=` per light; `SHADER_LOD_LEVEL` overrides it with `0x006B9A20`.

The base's output list ends up one entry long. When its count is not 1 the base allocates a new one-entry array,
freeing the old one unless bit `0x80000000` of the count is set (`0x006B94FF`-`0x006B9549`). It copies the string into
a new buffer and stores it as the entry, freeing the entry's previous string unless bit `0x1` of that pointer is
set (`0x006B95B0`-`0x006B95FD`). A failed allocation returns `0xD` (`0x006B95E1`); otherwise it returns 0.

Slot 1 lists the legal values: the base `0x006B9B90` returns two one-word arrays, 0 and 1 (`0x006B9C99`-`0x006B9CAD`),
reusing arrays of the right size and returning `0xD` when an allocation fails (`0x006B9CC8`, `0x006B9CDD`).

### Switches built by name

`0x006B89C0(name)` returns 0 for a null name (`0x006B89CD`, `0x006B89FC`) and otherwise looks the name up in the registry
with `_stricmp`, returning the switch it finds.

On a miss it prints
`PNamedSemanticDynamic::FindOrCreateDynamic : Performance warning - allocating freelist on demand for '%s'.`,
takes an object from the `0x28`-byte pool and a name slot from the `0x40`-byte pool (both named
`PContextSwitch`, declared by `0x00167010` and `0x001672D0`, 256 entries each), copies the name without a
length check, and constructs a base switch with `0x006B8590`: `+0x18` = 1 (pool-owned), one key word,
`+0x24` = 1, registered.

An empty free list is grown with `0x00680150` first (`0x006B8A3E`, `0x006B8A77`). With no object it returns 0, and with
an object but no name slot it returns the object unconstructed (`0x006B8A92`-`0x006B8A9A`). `0x006B8590` stores `+0x20` =
1 at once (`0x006B85B3`) but adds 1 to the total `0x02E522E0` only when `0x006B8D20` returns 0 (`0x006B85C3`-`0x006B85CA`).

`0x006B89C0` is reached through slot 9 of the
`PNamedSemanticDescriptorForDynamicType<PContextSwitch>` vtable (`0x00D81010`, slot `0x006B94B0`) and
through `0x006B8DB0`, which returns `0x13` when nothing comes back. Slot 10 (`0x006B8F70`) copies every
registered switch into an array. At shutdown `0x005FDD40` unlinks only pool-owned switches and frees
both pools.

## Layouts

PContextSwitch, `0x28` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | base `0x00D80EA8`; slot 0 deleting destructor, 1 value list, 2 evaluate, 3 defines |
| `+0x08` | `void*` | name | C string, the registry key |
| `+0x10` | `void*` | next | registry link, head `0x02E522D0` |
| `+0x18` | `u8` | pooled | 1 for a switch built by `0x006B8590` |
| `+0x20` | `u32` | words | key words this switch writes |
| `+0x24` | `u8` | value | read only by the base evaluator `0x006B9050` |

Light output record (caller's stack, `0x0060B980` [rbp+`0x100`]):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*[4]` | lights | kept lights, in code order |
| `+0x20` | `u32` | count |  |

| Object | Name | Class vtable | Evaluator |
|---|---|---|---|
| `0x01F2EBC8` | `NUM_LIGHTS` | `0x00D80ED0` `PContextSwitchLights` | `0x006B9120` |
| `0x01F2EBF0` | `LOD_BLEND` | `0x00D80EF8` `PContextSwitchLODBlend` | `0x006B90A0` |
| `0x01F2EC18` | `INSTANCING_ENABLED` | `0x00D80F20` `PContextSwitchInstancing` | `0x006B9070` |
| `0x01F2EC40` | `SHADER_LOD_LEVEL` | `0x00D80F48` `PContextSwitchShaderLODLevel` | `0x006B93D0` |
| `0x01F2EC68` | `ORTHO_CAMERA` | `0x00D80F70` `PContextSwitchShaderOrthoCamera` | `0x006B9410` |
| `0x01F2EC90` | `INDICES_16BIT` | `0x00D80F98` `PContextSwitchShader16BitIndices` | `0x006B93A0` |
| `0x01F2ECB8` | `SKINNING_ENABLED` | `0x00D80FC0` `PContextSwitchShaderSkinned` | `0x006B9450` |
| `0x01F2ECE0` | `LOW_RES_PARTICLES` | `0x00D80FE8` `PContextSwitchLowResParticles` | `0x006B9050` |

The per-switch installers, teardown stubs and all four slots are in
[shader-variant-selection-context-switch-family.tsv](shader-variant-selection-context-switch-family.tsv).
Instruction-level accesses to the D3D11 shader pass state are in
[shader-variant-selection-p-shader-pass-state-d3d11-accesses.tsv](shader-variant-selection-p-shader-pass-state-d3d11-accesses.tsv).

In a shader file the three program lists (`PShaderVertexProgram`, `PShaderGeometryProgram`,
`PShaderFragmentProgram`) give each program `m_compiledCode`, the byte count of its code,
`m_constantBufferSize` and `m_shaderProfile`, a u32 whose bytes, most significant first, spell the profile:
`vs50`, `vs40`, `vs41`, `gs50`, `ps50` or `ps40`. A list's array area holds the codes back to back in object
order. Each code is a DXBC container whose size word at `+0x18` equals its `m_compiledCode`; 224 of the 266
lists end with 1 to 7 zero bytes after the last code.

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PEffect` (`0x78` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_supportedLightMask | 0 in all 93 shipped effects; m_supportedLightMask (u32), registered by `0x005E3F70` (`0x00632960` at `0x005E3FFA`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffect |
| `+0x04` | `u32` | m_supportedShadowCasterMask | m_supportedShadowCasterMask (u32), registered by `0x005E3F70` (`0x00632960` at `0x005E4069`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffect |
| `+0x08` | `void*` | m_effectFile | m_effectFile (ptr), registered by `0x005E3F70` (`0x00632960` at `0x005E40D7`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffect |
| `+0x10` | `void*` | m_effectFileFromBasePath | m_effectFileFromBasePath (ptr), registered by `0x005E3F70` (`0x00632960` at `0x005E4145`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffect |
| `+0x68` | `void*` | m_effectSource | m_effectSource (ptr), registered by `0x005E3F70` (`0x00632960` at `0x005E41B3`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffect |
| `+0x70` | `u32` | m_maxLightCount | 0 in all 93 shipped effects; m_maxLightCount (u32), registered by `0x005E3F70` (`0x00632960` at `0x005E450B`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffect |
| `+0x74` | `u32` | m_numSupportedShaderLODLevels | 0 in all 93 shipped effects; m_numSupportedShaderLODLevels (u32), registered by `0x005E3F70` (`0x00632960` at `0x005E457A`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffect |

`PEffectVariant` (`0x68` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x38` | `u16` | m_largestShaderPassCount | m_largestShaderPassCount (u16), registered by `0x005E45B0` (`0x00632960` at `0x005E4867`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffectVariant |
| `+0x3A` | `u8[6]` | pad3A | the bytes after m_largestShaderPassCount (u16 at `+0x38`) up to m_tweakableShaderParameterDefinitions at `+0x40`; no registered member covers it (`0x005D9280` registers the `0x68`-byte class at `0x005D92D0`) |
| `+0x60` | `u16` | m_tweakableParameterBufferSize | m_tweakableParameterBufferSize (u16), registered by `0x005E45B0` (`0x00632960` at `0x005E49F3`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffectVariant |
| `+0x62` | `u16` | m_untweakableParameterBufferSize | m_untweakableParameterBufferSize (u16), registered by `0x005E45B0` (`0x00632960` at `0x005E4A62`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PEffectVariant |
| `+0x64` | `u8[4]` | pad64 | the bytes after m_untweakableParameterBufferSize (u16 at `+0x62`) up to the end of the `0x68`-byte class; no registered member covers it (`0x005D9280` registers the `0x68`-byte class at `0x005D92D0`) |

`PMaterialSwitch` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | m_name | m_name (ptr), registered by `0x005E52D0` (`0x00632960` at `0x005E5359`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PMaterialSwitch |
| `+0x08` | `void*` | m_value | m_value (ptr), registered by `0x005E52D0` (`0x00632960` at `0x005E53C7`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PMaterialSwitch |

## Shipped data

Measured over the shader clusters in the archive (`gamedata/d3d11/artdata/shaders/*.phyre`).

| Fact | Value |
|---|---|
| shader clusters | 99 |
| clusters holding a `PEffect` | 93, one `PEffect` each, 44-byte file records |
| clusters declaring a `PContextSwitch` class | 0 (93 name it only as the type of `PArray<PContextSwitch *>`) |
| `m_contextSwitches` count | 0 in all 93 |
| `m_contextVariantSwitches` count | 1 in all 93, a `PNodeContext` whose `m_packedSwitches` is 0 |
| `m_effectVariants` count | 1 in all 93 |
| `m_maxLightCount`, `m_supportedLightMask`, `m_numSupportedShaderLODLevels` | 0 in all 93 |
| switch names as strings | only `SKINNING_ENABLED`, in 12 clusters, as a `PMaterialSwitch` define name |
| compiled variant clusters, named `<shader>.fx#<32 hex digits>.phyre` | 80: `phyredefaultlitshader` 63, `phyrechrshader` 17 |
| model clusters (`.dae.phyre`) that name a variant | 2,091 of 2,112: 1,047 under `chr`, 588 under `chr_shadow`, 456 under `map` |
| variants some model names | 79 of 80; `phyredefaultlitshader.fx#9aa82ed50d0fd3164f55358a7406d2f5` is named by no model |
| most used variants | `phyrechrshader.fx#cb0f9f99…` by 1,591 models and `…#e0c4972f…` by 1,583; `phyredefaultlitshader.fx#5b374ae6…` by all 456 maps |

A model names the compiled shader it draws with as `<shader>.fx#<hash>`, in its own cluster's strings; the archive
ships each such variant as a separate cluster beside the shader, and no other file (`idmaps.txt` included) and no
string in the executable builds or holds those names.

The shader files decode as below; the linked tables hold every value.

| Fact | Value |
|---|---|
| effect files | 93: the 13 effects the executable names and the 80 variants; per file the effect name, render passes, shaders, passes, programs by stage and profile, code bytes, entry points, parameter and sampler counts, parameter names, material defines and what names the file ([effects](shader-variant-selection-effects.tsv)) |
| programs | 5,625: vertex 2,475 (`vs_5_0` 2,431, `vs_4_0` 42, `vs_4_1` 2), geometry 675 (`gs_5_0` 675), fragment 2,475 (`ps_5_0` 2,433, `ps_4_0` 42) ([programs](shader-variant-selection-programs.tsv)) |
| distinct program codes | 335 by SHA-256 (`ps_5_0` 225, `ps_4_0` 41, `vs_5_0` 37, `gs_5_0` 16, `vs_4_0` 15, `vs_4_1` 1), all from `Microsoft (R) HLSL Shader Compiler 6.3.9600.18611`; chunks `RDEF ISGN OSGN SHEX STAT`, with `OSG5` for `OSGN` in the 16 geometry codes and `SHDR` for `SHEX` in the 57 shader model 4 codes; per code the inputs, outputs, constant buffers, bound resources and instruction count ([program codes](shader-variant-selection-program-codes.tsv)) |
| the variant no model names | every program code of `phyredefaultlitshader.fx#9aa82ed5…` is also held by a variant that models name |
| model imports | 4,770 import rows from the 2,091 models that name a variant: `chr` 2,280, `chr_shadow` 1,173, `map` 1,317; each imported variant ships ([imports](shader-variant-selection-imports.tsv)) |
| render passes | 78 names across the 93 effects: 48 are names of records in the static pass array `0x01F2D6A0` and 17 of the runtime pass registry ([Post-processing](../Graphics/post-processing.md)); 13 match a record of neither: `ColorPickingRender`, `DefaultMapRenderPass`, `DefaultMapRenderPassNoAlphaTest`, `DepthEdgeDetection`, `DepthLabelOnePass`, `LumaEdgeDetection`, `Resolve`, `SAOCombine`, `Separate`, `USMApply`, `USMBlur`, `USMDownSample`, `USMDownSampleMS` ([render passes](shader-variant-selection-render-passes.tsv)) |
| effects the executable names | each of the 13 by one path string: `sao` `0x008C66E8`, `unsharpmask` `0x008C6718`, `hbao` `0x008C6750`, `ps2depthoffield` `0x008C6780`, `separablesss` `0x008C67C0`, `gaussianfilter` `0x008C67F8`, `phyrefxaa` `0x008C6830`, `smaa` `0x008C6868`, `depthmask` `0x008C6908`, `brightnessshader` `0x008C6940`, `video` `0x008F8CE0`, `phyretext` `0x0090198F`, `copybuffer` `0x00902DE0` |
| the six textures | `anisolighting`, `areatexdx10` and `searchtex` are named by executable strings (`0x008F9258`, `0x008C68D0`, `0x008C6898`); `beckmannmap`, `mipmaptest` and `shifttex` are named by no executable path string, no `.ah` or prefetch list, no model import and no other shipped file |
| program bindings | each of the 5,625 programs is the target of exactly one `PShaderPass` pointer. In every file `PEffectVariant` `+10` points to the render passes; a `PSceneRenderPass` names its pass at `+0` (a `PSceneRenderPassType` user fixup), its one `PShader` at `+5` and one entry-point record per shader pass at `+10`; `PShader` `+8` points to its shader passes; `PShaderPass` `+0`, `+1`, `+2`, `+3` to the vertex, fragment, geometry and compute program (packed offsets, the same in all 93 files). 1,749 render passes, 2,475 shader passes. `0x00608DD0` (`0x00608EC9`) and `0x00608F20` (`0x0060905B`) hand the pass to `0x00629AA0`, which reads the four program pointers at `+0x0`, `+0x8`, `+0x10`, `+0x18` (`0x00629AB8`-`0x00629AC9`) and sets the vertex, geometry, pixel and compute shaders in that order. 149 programs belong to effects no model imports (the 90 of the 13 effects the executable names and the 59 of `phyredefaultlitshader.fx#9aa82ed5…`); 398 to the 13 render passes no pass record names ([program bindings](shader-variant-selection-programs-binding.tsv)) |
| replacement checks | one row per code: its program objects, files, render passes, entry points, signatures, input-layout formats, constant buffers and bindings, where each bound resource comes from, the meshes, and each check below as passing uses over all uses ([code contract](shader-variant-selection-codes-contract.tsv)) |

## State

| Address | What |
|---|---|
| `0x02E522D0` | registry head, linked through `+0x10` |
| `0x02E522E0` | total key words, 10 after static initialization |
| `0x02E52488` | free list of `0x28`-byte switch objects |
| `0x02E524B0` | free list of `0x40`-byte name slots |

## Modding notes

- An effect can only select a variant it ships; a key with no table entry leaves the draw without one.
- The `NUM_LIGHTS` output holds four light pointers before its count, so an effect authored with
  `m_maxLightCount` above 4 that keeps a fifth light loses that light: its pointer lands on `+0x20`, and the
  count, stored after the pointers (`0x006B92E0`, `0x006B9360`), replaces its low half. A sixth or later light is
  written from `+0x28` on, past the record.
- A switch name the engine does not implement becomes a base switch answering 1; its name must fit
  the 64-byte name slot.
- Material defines such as `SKINNING_ENABLED` in a `PMaterialSwitch` are compile-time names and do not
  go through this registry.

Replacing a program: each program object is bound by one shader pass, and the 5,625 programs hold 335 codes, so a
code is replaced in every program the [code contract](shader-variant-selection-codes-contract.tsv) lists for it. A
replacement keeps:

- Its stage and profile word. The creators refuse `vs50`, `ps50` and `gs50` below feature level `0xB000` and the `41`
  profiles below `0xA100`, and pass `m_compiledCode` with bit `0x80000000` cleared as the code size
  (`0x0061E077`-`0x0061E081`; [Phyre D3D11 draws and state](phyre-d3d11-draws-and-state.md)).
- For a vertex program, the input elements its `m_inputLayout` descs name. `0x0061E0B0` builds one element per desc that
  names a semantic (index `+0x10`, format `+0x14`, slot `+0x18`, offset 0) and hands the program's own code to `CreateInputLayout`
  (`0x0061E1B9`); a failure returns 9, and `0x00629AA0` returns before the geometry, pixel and compute shaders are set
  (`0x00629AF0`).
- Inputs and descs that match. In 52 of the 53 vertex codes every non-system input element has a desc of the same
  semantic and index
  and every desc an element; `FxaaVS` (`0x0070564b…`) reads only `SV_VertexID` and has no desc.
- The slot order of its streams. Desc slot k is vertex buffer k of `IASetVertexBuffers` (`0x00629FA7`), the pass's k-th
  stream location; in every pass the stream locations are the shader's stream definitions in order, and each desc's
  render type is the definition at its slot (53 codes).
- The shipped stream formats. The shipped formats are `R32G32B32_FLOAT` for `Vertex`,
  `Normal`, `Tangent`, `Binormal` and the four `Skinnable` types, `R32G32B32A32_FLOAT` for `Color` and `SkinWeights`,
  `R32G32_FLOAT` for `ST` and the seven two-component `Vertex` descs, `R8G8B8A8_UINT` for `SkinIndices`.
- Only streams the meshes give. The meshes that import a variant give each of its stream definitions a stream of that
  render data type in 12,320 of 12,320 `chr/` segments, 585 of 588 `chr_shadow/` segments and 274,276 of 274,277 map
  segments; the open map segment is `pla0103` mesh 396, drawn only by the instance `pPlane1`, which matches no YM00
  record.
- A new stream in every mesh. A program that reads a new stream needs a new definition and a stream of its type in
  every mesh that imports the variant ([Phyre asset files](phyre-asset-files.md)).
- Its outputs where the next stage reads them. In all 282 pixel and geometry codes every input other than a
  system-generated value is an output of the pass's previous stage with the same semantic, index and register.
- `$Globals` at bind point `m_globalConstantBufferIndex`, of `m_constantBufferSize` bytes. `0x0061F650` creates the
  program's buffer of `[program+0x28]` bytes with bind flag value `0x4`; `0x006231F0`, `0x00623050`, `0x00622F40` and
  `0x00622D90` upload it with `UpdateSubresource` and bind it at slot `+0x2C` unless that is −1.
- The same buffer in every program. All 307 codes that carry
  `$Globals` match in every program that holds them; the other 28 have index `0xFFFFFFFF` and no `$Globals`.
- The offset, size and name of each `$Globals` variable the pass writes. `0x00628B40` copies each 16-byte value record
  (`+0x00` u16 offset in the block, `+0x04` offset in the buffer, `+0x08` size, `+0x0C` type) into the program's copy
  at `[program+0x10]` when the buffer offset is below `m_constantBufferSize` (`0x00628BBB`).
- The value types the copy takes. Type `0x31` is copied as `size >> 6` 4 × 4 matrices transposed, `0x30` as
  `size / 48` 4 × 3 matrices transposed, both stopping at a matrix whose first word is `0xFFFFFFFF`, and any other type
  byte for byte (`0x00628BC5`-`0x00628BEA`). In all 307 codes each record starts at a
  variable, fits it and carries its name, and every variable the code marks used is written.
- Each resource at the slot its record names. `0x0062A0A0` binds the parameter of each resource record at slot `+0x04`
  (−1 skips it) by its parameter type. Every texture, sampler and constant-buffer binding of the 295 codes that have
  them has a record at its bind point.
- The tweakable parameter behind each binding. Each record of block 1 that feeds a binding reads one of the variant's
  tweakable parameters, which carries the binding's name and a parameter type of its kind and dimension (`0x42` 2D,
  `0x43` 3D, `0x44` cube; 267 codes); each such sampler's state is a `PSamplerState` the effect file's material
  parameter buffer points to (265 codes).
- The scene-wide buffer. The only binding fed from block 0 is `SceneWideParameterConstantBuffer`, at
  `b1` in the vertex, pixel and geometry codes and at `b0` in 34 geometry pass uses; a constant-buffer slot above 7 is
  logged `Invalid constant buffer location : %d` (`0x0062A508`).

## Related

- [Phyre post-effect classes](phyre-post-effect-classes.md): the post-effect classes whose render slots reach `0x0060B980`.
- [Phyre reflection](phyre-reflection.md): class descriptors and the `PEffect` member registrations.
- [Phyre asset files](phyre-asset-files.md): the cluster header, packed namespace and instance lists the measurement reads.
- [Phyre field schema](phyre-field-schema.md): file-side against runtime member offsets.
- [Post-processing](../Graphics/post-processing.md): the two render-pass record tables the effects' pass names are matched against.
- [Phyre D3D11 draws and state](phyre-d3d11-draws-and-state.md): the pass switch, stage caches and shader creators a replacement program goes through.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Platform: `0x00622F40` calls `0x0061E340`; `0x0062A0A0` calls `0x006239C0`; those functions are documented on
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [phyre d3d11 device and resources](phyre-d3d11-device-and-resources.md).
- Presentation: `0x00608DD0` calls `0x00629AA0`; `0x00608F20` calls `0x00629AA0`; `0x0061E0B0` is called by `0x0061DFE0`;
  `0x0061F650` is called by `0x0061DBE0`, `0x0061DCA0`, `0x0061DD60`, `0x0061DFE0`; `0x00629AA0` calls `0x0061DBE0`, `0x0061DCA0`,
  `0x0061DD60`, `0x0061DFE0`; `0x0067AEA0` is called by `0x006B9630`.
- Presentation: those functions are documented on [phyre d3d11 draws and state](phyre-d3d11-draws-and-state.md),
  [phyre reflection](phyre-reflection.md).
- Resource: `0x00680150` is called by `0x001F4720`; those functions are documented on
  [bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md).
