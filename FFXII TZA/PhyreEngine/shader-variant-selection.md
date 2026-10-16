---
title: "Shader variant selection: the eight context-switch axes and the variant key a draw uses"
kind: "system"
category: "PhyreEngine"
summary: "PhyreEngine's context switches: the eight static switch objects (NUM_LIGHTS, LOD_BLEND, INSTANCING_ENABLED, SHADER_LOD_LEVEL, ORTHO_CAMERA, INDICES_16BIT, SKINNING_ENABLED, LOW_RES_PARTICLES), how each evaluates a draw into words of the variant key, the binary search of the effect's variant table, the -D defines the same objects write, the base switch built by name at run time, and what the 93 shipped effects author."
addresses: ["00606A20", "0060B980", "006B8D20", "02E522D0", "02E522E0", "006B9050", "006B9120", "006B90A0", "006B9070", "006B93D0", "006B9410", "006B93A0", "006B9450", "006B94C0", "006B9630", "006B9B90", "006B89C0", "006B8590", "005FDD40", "01F2EBC8", "00D80EA8"]
---

# Shader variant selection: the eight context-switch axes and the variant key a draw uses

## What the player sees

Nothing directly. Before PhyreEngine draws a mesh it picks which compiled build of the effect's shader
to use: with or without skinning, with a given light set, with or without an LOD crossfade. The pick is
made by eight named switches. In this build every shipped effect authors exactly one variant and an
empty context-switch list; the lookup runs on every draw that goes through `0060B980`.

## How it works

### The switch objects

A context switch is a `0x28`-byte object of class `Phyre::PRendering::PContextSwitch` or one of eight
subclasses. Each subclass has one static instance in `.data`, starting at `01F2EBC8` and spaced
`0x28` apart. The image carries each object with the base vtable `00D80EA8`, its name pointer,
`+0x20` = 0 and `+0x24` = 1; the installer in the CRT initializer table (`008C43E8`–`008C4420`) then:

1. registers it with `006B8D20`;
2. only when that returns 0, adds its word count to the image-wide total `02E522E0` and stores the
   count at `+0x20` (3 for `NUM_LIGHTS` at `001670F0`, 1 for the others);
3. installs its own vtable at `+0x00` and registers an `atexit` teardown.

`LOW_RES_PARTICLES`'s installer (`00167140`) also writes 0 to `+0x24`. After static initialization
`02E522E0` is 10.

### Registration

`006B8D20(switch)` returns `0x11` when `+0x08` (the name) is null, walks the list headed at
`02E522D0` through `+0x10` comparing names byte by byte (case-sensitive), returns `0x12` on a match
without linking, and otherwise links the switch at the head and returns 0.

### Building the key

`00606A20(effect, a2, a3, out, record)` is called only from `0060BDEF` in `0060B980`:

1. When the effect's variant count (`+0x58`, bit 31 masked off) is 0 it returns −1.
2. It reserves `02E522E0 × 4` bytes on the stack and points a cursor at the start, so the total is the
   buffer bound, not the key length.
3. For each non-null entry of the effect's switch array (`+0x50`, count `+0x48`) it calls vtable
   slot 2 with seven arguments: the switch, the effect, `a2`, `a3`, the cursor, `out` and `record`.
   A non-zero return stops the loop.
4. The key length is how far the cursor moved, in words.
5. It binary-searches the effect's table at `+0x60` (16-byte entries `{u32 count, words}`; one word is
   stored inline, more through a pointer), ordering first by word count and then word by word, and
   returns the matching index or −1.

`0060B980` turns a non-negative index into a 64-byte entry (`0060BDFA`: `index << 6` plus the table at
`+0x10` of the entry it selected at `0060BD84`–`0060BDBF`). On −1 the entry stays null and the draw work under
`0060BE13` is skipped; no variant is compiled on demand.

### What each switch reads

Every evaluator writes its words at the cursor, advances it by four per word and returns 0.

| Switch | Evaluator | Writes |
|---|---|---|
| `NUM_LIGHTS` | `006B9120` | a bit-packed light code (below) |
| `LOD_BLEND` | `006B90A0` | 1 when the LOD weight is neither 0.0 nor 1.0 |
| `INSTANCING_ENABLED` | `006B9070` | 1 when `record` is non-null and `record+0x30` is non-null |
| `SHADER_LOD_LEVEL` | `006B93D0` | the level at `[[a2+0x40]]+0x38`, clamped to effect `+0x74` − 1 (0 when that is 0) |
| `ORTHO_CAMERA` | `006B9410` | 1 when the float at `[record]+0x6C` is at least 0.01 |
| `INDICES_16BIT` | `006B93A0` | 1 when the byte `+0x4C` of `[record+0x38]` equals `0x0C` |
| `SKINNING_ENABLED` | `006B9450` | 1 when `a2+0x18` is non-null; with `[record+0x38]` present, also needs its count `+0x08` below `0x79` and `00671670` to succeed |
| `LOW_RES_PARTICLES` | `006B9050` (the base's) | 1 when the byte `+0x24` is non-zero, so always 0 |

`LOD_BLEND` emits 0 when `a2+0x40` or `a3+0x20` is null; otherwise it reads the first float of the
12-byte element `a3+0x30` of the array at `[a2+0x40]` (`+0x20` count, `+0x28` data).

For a `PCamera` (members registered by `006784E0`), `+0x6C` is the last float of `m_projectionMatrix`, the 64-byte matrix at
`+0x30`; an orthographic matrix has 1 there and a perspective one 0.

### NUM_LIGHTS

`006B9120` walks the light array at `a3` (`+0x10` count with bit 31 masked, `+0x18` pointers). It
keeps a light when the mask at `+0x18` of its light type (`light+0x20`) meets the effect's word
`+0x00`. For a kept light it takes the shadow-caster type (`[light+0x18]+0x08`) and uses its index
`+0x1C` when that type's mask `+0x18` meets the effect's `+0x04`, else 0, so a shadowless light is
kept with shadow index 0. Each light becomes `(shadowIndex << 5) | lightTypeIndex`.

When more than one light is kept it sorts them by that code (`006B83C0`). The count is the smaller of
the kept count and the effect's `+0x70`. It zeroes `((10 × count + 35) >> 5) << 2` bytes and packs a
4-bit count followed by 10 bits per light. It also copies the kept light pointers to `out+0x00`
onward and the count to `out+0x20`; `0060B980` reserves four pointer slots there (`0060BA9B`–`0060BAB7`).

### Defines for the shader compiler

Slot 3 reads the switch's word back off a cursor. The base `006B94C0` appends nothing for 0 and
otherwise builds `-D<name>=<value>` from `"-D"` (`00D81068`), the name at `+0x08` and `"="`
(`01CEBB4C`). `NUM_LIGHTS` overrides it (`006B9630`) with `-DLIGHTTYPE_<i>=` and
`-DSHADOWTYPE_<i>=` per light; `SHADER_LOD_LEVEL` overrides it with `006B9A20`. Slot 1 lists the legal
values: the base `006B9B90` returns two one-word arrays, 0 and 1.

### Switches built by name

`006B89C0(name)` looks the name up in the registry with `_stricmp`. On a miss it prints
`PNamedSemanticDynamic::FindOrCreateDynamic : Performance warning - allocating freelist on demand for '%s'.`,
takes an object from the `0x28`-byte pool and a name slot from the `0x40`-byte pool (both named
`PContextSwitch`, declared by `00167010` and `001672D0`, 256 entries each), copies the name without a
length check, and constructs a base switch with `006B8590`: `+0x18` = 1 (pool-owned), one key word,
`+0x24` = 1, registered.

`006B89C0` is reached through slot 9 of the
`PNamedSemanticDescriptorForDynamicType<PContextSwitch>` vtable (`00D81010`, slot `006B94B0`) and
through `006B8DB0`, which returns `0x13` when nothing comes back. Slot 10 (`006B8F70`) copies every
registered switch into an array. At shutdown `005FDD40` unlinks only pool-owned switches and frees
both pools.

## Layouts

```
PContextSwitch, 0x28 bytes
+0x00  ptr   vtable     base 00D80EA8; slot 0 deleting destructor, 1 value list, 2 evaluate, 3 defines
+0x08  ptr   name       C string, the registry key
+0x10  ptr   next       registry link, head 02E522D0
+0x18  u8    pooled     1 for a switch built by 006B8590
+0x20  u32   words      key words this switch writes
+0x24  u8    value      read only by the base evaluator 006B9050
```

```
light output record (caller's stack, 0060B980 [rbp+0x100])
+0x00  ptr[4]  lights   kept lights, in code order
+0x20  u32     count
```

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

## State

| Address | What |
|---|---|
| `02E522D0` | registry head, linked through `+0x10` |
| `02E522E0` | total key words, 10 after static initialization |
| `02E52488` | free list of `0x28`-byte switch objects |
| `02E524B0` | free list of `0x40`-byte name slots |

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
