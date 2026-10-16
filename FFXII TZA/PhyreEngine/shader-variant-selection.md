---
title: "Shader variant selection: the eight context-switch axes and the variant key a draw uses"
kind: "system"
category: "PhyreEngine"
addresses: "00606A20, 0060B980, 006B8D20, 02E522D0, 02E522E0, 006B9050, 006B9120, 006B90A0, 006B9070, 006B93D0, 006B9410, 006B93A0, 006B9450, 006B94C0, 006B9630, 006B9B90, 006B89C0, 006B8590, 005FDD40, 01F2EBC8, 00D80EA8"
---

## What the player sees

Nothing directly. Before PhyreEngine draws a mesh it picks which compiled build of the effect's shader
to use: with or without skinning, with a given light set, with or without an LOD crossfade. The pick is
made by eight named switches. In this build every shipped effect authors exactly one variant and an
empty context-switch list; the lookup runs on every draw that goes through `0060B980`.

## How it works

### The switch objects

A context switch is a `28`<sub>h</sub>-byte object of class `Phyre::PRendering::PContextSwitch` or one of eight
subclasses. Each subclass has one static instance in `.data`, starting at `01F2EBC8` and spaced
`28`<sub>h</sub> apart. The image carries each object with the base vtable `00D80EA8`, its name pointer,
`+20`<sub>h</sub> = 0 and `+24`<sub>h</sub> = 1; the installer in the CRT initializer table (`008C43E8`–`008C4420`) then:

1. registers it with `006B8D20`;
2. only when that returns 0, adds its word count to the image-wide total `02E522E0` and stores the
   count at `+20`<sub>h</sub> (3 for `NUM_LIGHTS` at `001670F0`, 1 for the others);
3. installs its own vtable at `+00`<sub>h</sub> and registers an `atexit` teardown.

`LOW_RES_PARTICLES`'s installer (`00167140`) also writes 0 to `+24`<sub>h</sub>. After static initialization
`02E522E0` is 10.

### Registration

`006B8D20(switch)` returns `11`<sub>h</sub> when `+08`<sub>h</sub> (the name) is null, walks the list headed at
`02E522D0` through `+10`<sub>h</sub> comparing names byte by byte (case-sensitive), returns `12`<sub>h</sub> on a match
without linking, and otherwise links the switch at the head and returns 0.

### Building the key

`00606A20(effect, a2, a3, out, record)` is called only from `0060BDEF` in `0060B980`:

1. When the effect's variant count (`+58`<sub>h</sub>, bit 31 masked off) is 0 it returns −1.
2. It reserves `02E522E0 × 4` bytes on the stack and points a cursor at the start, so the total is the
   buffer bound, not the key length.
3. For each non-null entry of the effect's switch array (`+50`<sub>h</sub>, count `+48`<sub>h</sub>) it calls vtable
   slot 2 with seven arguments: the switch, the effect, `a2`, `a3`, the cursor, `out` and `record`.
   A non-zero return stops the loop.
4. The key length is how far the cursor moved, in words.
5. It binary-searches the effect's table at `+60`<sub>h</sub> (16-byte entries `{u32 count, words}`; one word is
   stored inline, more through a pointer), ordering first by word count and then word by word, and
   returns the matching index or −1.

`0060B980` turns a non-negative index into a 64-byte entry (`0060BDFA`: `index << 6` plus the table at
`+10`<sub>h</sub> of the entry it selected at `0060BD84`–`0060BDBF`). On −1 the entry stays null and the draw work under
`0060BE13` is skipped; no variant is compiled on demand.

### What each switch reads

Every evaluator writes its words at the cursor, advances it by four per word and returns 0.

| Switch | Evaluator | Writes |
|---|---|---|
| `NUM_LIGHTS` | `006B9120` | a bit-packed light code (below) |
| `LOD_BLEND` | `006B90A0` | 1 when the LOD weight is neither 0.0 nor 1.0 |
| `INSTANCING_ENABLED` | `006B9070` | 1 when `record` is non-null and `record+30h` is non-null |
| `SHADER_LOD_LEVEL` | `006B93D0` | the level at `[[a2+40h]]+38h`, clamped to effect `+74`<sub>h</sub> − 1 (0 when that is 0) |
| `ORTHO_CAMERA` | `006B9410` | 1 when the float at `[record]+6Ch` is at least 0.01 |
| `INDICES_16BIT` | `006B93A0` | 1 when the byte `+4C`<sub>h</sub> of `[record+38h]` equals `0C`<sub>h</sub> |
| `SKINNING_ENABLED` | `006B9450` | 1 when `a2+18h` is non-null; with `[record+38h]` present, also needs its count `+08`<sub>h</sub> below `79`<sub>h</sub> and `00671670` to succeed |
| `LOW_RES_PARTICLES` | `006B9050` (the base's) | 1 when the byte `+24`<sub>h</sub> is non-zero, so always 0 |

`LOD_BLEND` emits 0 when `a2+40h` or `a3+20h` is null; otherwise it reads the first float of the
12-byte element `a3+30h` of the array at `[a2+40h]` (`+20`<sub>h</sub> count, `+28`<sub>h</sub> data).

For a `PCamera` (members registered by `006784E0`), `+6C`<sub>h</sub> is the last float of `m_projectionMatrix`, the 64-byte matrix at
`+30`<sub>h</sub>; an orthographic matrix has 1 there and a perspective one 0.

### NUM_LIGHTS

`006B9120` walks the light array at `a3` (`+10`<sub>h</sub> count with bit 31 masked, `+18`<sub>h</sub> pointers). It
keeps a light when the mask at `+18`<sub>h</sub> of its light type (`light+20h`) meets the effect's word
`+00`<sub>h</sub>. For a kept light it takes the shadow-caster type (`[light+18h]+08h`) and uses its index
`+1C`<sub>h</sub> when that type's mask `+18`<sub>h</sub> meets the effect's `+04`<sub>h</sub>, else 0, so a shadowless light is
kept with shadow index 0. Each light becomes `(shadowIndex << 5) | lightTypeIndex`.

When more than one light is kept it sorts them by that code (`006B83C0`). The count is the smaller of
the kept count and the effect's `+70`<sub>h</sub>. It zeroes `((10 × count + 35) >> 5) << 2` bytes and packs a
4-bit count followed by 10 bits per light. It also copies the kept light pointers to `out+00h`
onward and the count to `out+20h`; `0060B980` reserves four pointer slots there (`0060BA9B`–`0060BAB7`).

### Defines for the shader compiler

Slot 3 reads the switch's word back off a cursor. The base `006B94C0` appends nothing for 0 and
otherwise builds `-D<name>=<value>` from `"-D"` (`00D81068`), the name at `+08`<sub>h</sub> and `"="`
(`01CEBB4C`). `NUM_LIGHTS` overrides it (`006B9630`) with `-DLIGHTTYPE_<i>=` and
`-DSHADOWTYPE_<i>=` per light; `SHADER_LOD_LEVEL` overrides it with `006B9A20`. Slot 1 lists the legal
values: the base `006B9B90` returns two one-word arrays, 0 and 1.

### Switches built by name

`006B89C0(name)` looks the name up in the registry with `_stricmp`. On a miss it prints
`PNamedSemanticDynamic::FindOrCreateDynamic : Performance warning - allocating freelist on demand for '%s'.`,
takes an object from the `28`<sub>h</sub>-byte pool and a name slot from the `40`<sub>h</sub>-byte pool (both named
`PContextSwitch`, declared by `00167010` and `001672D0`, 256 entries each), copies the name without a
length check, and constructs a base switch with `006B8590`: `+18`<sub>h</sub> = 1 (pool-owned), one key word,
`+24`<sub>h</sub> = 1, registered.

`006B89C0` is reached through slot 9 of the
`PNamedSemanticDescriptorForDynamicType<PContextSwitch>` vtable (`00D81010`, slot `006B94B0`) and
through `006B8DB0`, which returns `13`<sub>h</sub> when nothing comes back. Slot 10 (`006B8F70`) copies every
registered switch into an array. At shutdown `005FDD40` unlinks only pool-owned switches and frees
both pools.

## Layouts

PContextSwitch, `28`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | vtable | base `00D80EA8`; slot 0 deleting destructor, 1 value list, 2 evaluate, 3 defines |
| `08`<sub>h</sub> | `void*` | name | C string, the registry key |
| `10`<sub>h</sub> | `void*` | next | registry link, head `02E522D0` |
| `18`<sub>h</sub> | `u8` | pooled | 1 for a switch built by `006B8590` |
| `20`<sub>h</sub> | `u32` | words | key words this switch writes |
| `24`<sub>h</sub> | `u8` | value | read only by the base evaluator `006B9050` |

Light output record (caller's stack, `0060B980` [rbp+`100`<sub>h</sub>]):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*[4]` | lights | kept lights, in code order |
| `20`<sub>h</sub> | `u32` | count |  |

| Object | Name | Class vtable | Evaluator |
|---|---|---|---|
| `01F2EBC8` | `NUM_LIGHTS` | `00D80ED0` `PContextSwitchLights` | `006B9120` |
| `01F2EBF0` | `LOD_BLEND` | `00D80EF8` `PContextSwitchLODBlend` | `006B90A0` |
| `01F2EC18` | `INSTANCING_ENABLED` | `00D80F20` `PContextSwitchInstancing` | `006B9070` |
| `01F2EC40` | `SHADER_LOD_LEVEL` | `00D80F48` `PContextSwitchShaderLODLevel` | `006B93D0` |
| `01F2EC68` | `ORTHO_CAMERA` | `00D80F70` `PContextSwitchShaderOrthoCamera` | `006B9410` |
| `01F2EC90` | `INDICES_16BIT` | `00D80F98` `PContextSwitchShader16BitIndices` | `006B93A0` |
| `01F2ECB8` | `SKINNING_ENABLED` | `00D80FC0` `PContextSwitchShaderSkinned` | `006B9450` |
| `01F2ECE0` | `LOW_RES_PARTICLES` | `00D80FE8` `PContextSwitchLowResParticles` | `006B9050` |

The per-switch installers, teardown stubs and all four slots are in
[shader-variant-selection-context-switch-family.tsv](shader-variant-selection-context-switch-family.tsv).
Instruction-level accesses to the D3D11 shader pass state are in
[shader-variant-selection-p-shader-pass-state-d3d11-accesses.tsv](shader-variant-selection-p-shader-pass-state-d3d11-accesses.tsv).

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
| variants some model names | 79 of 80; `phyredefaultlitshader.fx#9aa82ed50d0fd3164f55358a7406d2f5` is named by none |
| most used variants | `phyrechrshader.fx#cb0f9f99…` by 1,591 models and `…#e0c4972f…` by 1,583; `phyredefaultlitshader.fx#5b374ae6…` by all 456 maps |

A model names the compiled shader it draws with as `<shader>.fx#<hash>`, in its own cluster's strings; the archive
ships each such variant as a separate cluster beside the shader, and no other file (`idmaps.txt` included) and no
string in the executable builds or holds those names. Measured by `Database/Tools/phyre-census/shader_variant_files.py`.

## State

| Address | What |
|---|---|
| `02E522D0` | registry head, linked through `+10`<sub>h</sub> |
| `02E522E0` | total key words, 10 after static initialization |
| `02E52488` | free list of `28`<sub>h</sub>-byte switch objects |
| `02E524B0` | free list of `40`<sub>h</sub>-byte name slots |

## Modding notes

- An effect can only select a variant it ships; a key with no table entry leaves the draw without one.
- The `NUM_LIGHTS` output holds four light pointers before its count, so an effect authored with
  `m_maxLightCount` above 4 that keeps a fifth light overwrites the count.
- A switch name the engine does not implement becomes a base switch answering 1; its name must fit
  the 64-byte name slot.
- Material defines such as `SKINNING_ENABLED` in a `PMaterialSwitch` are compile-time names and do not
  go through this registry.

## Related

- [Phyre post-effect classes](phyre-post-effect-classes.md): the post-effect classes whose render slots reach `0060B980`.
- [Phyre reflection](phyre-reflection.md): class descriptors and the `PEffect` member registrations.
- [Phyre asset files](phyre-asset-files.md): the cluster header, packed namespace and instance lists the measurement reads.
- [Phyre field schema](phyre-field-schema.md): file-side against runtime member offsets.
