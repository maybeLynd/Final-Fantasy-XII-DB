---
title: "Phyre mesh-instance draws: the segment loop, the bone palette, the per-draw parameter blocks, the light and shadow parameter values and the preprocess ring buffer"
kind: "system"
category: "PhyreEngine"
summary: "How PhyreEngine draws one mesh instance in the executable: 0060B980 walks the mesh's segments, picks each segment's material, technique and shader variant, builds the bone-matrix palette, sizes and fills the per-draw parameter blocks, and the evaluator 00600F30 writes the light, shadow, vertex-stream and LOD values a shader asks for by parameter type; with the 2 MiB PPreprocessRingBuffer that holds large palettes and dynamic-mesh data, and the variant usage counter that never runs."
addresses: "0060B980, 005FF090, 005FF200, 005EB370, 00600B30, 005FECF0, 00600F30, 00670920, 00600BE0, 00606C60, 02CB6360, 006B6410, 006B64F0, 006B6510, 006B6690, 006B64C0, 007A12B0, 02E52270, 005DDAE0, 0060EC30"
---

## What the player sees

A PhyreEngine mesh instance is drawn by the function on this page, which 58 call sites in 27
functions use, among them the bitmap-font text and the FXAA pass. It decides which shader build each
part of the model uses, poses skinned models from their bone matrices, and hands each shader the
colour, position, fall-off and shadow matrices of up to four lights. A part whose effect has no
shader build for the current pass is not drawn.

## How it works

### The mesh-instance draw

`0060B980(renderer, instance, selector, instancing, value, flag)` draws one `PMeshInstance`:

1. It returns `0x16` unless bit `0x1` of the renderer's `+0x08` is set, and `0x15` when the renderer has
   no pass record at `+0x80`.
2. With no `instancing` argument it uses the instance's `m_instanceSegment` (`+0x28`).
3. It builds the matrix palette (below), and stores `value` at the instance's `+0xC0`.
4. It walks the mesh's segments (`0xC0` bytes each; count at mesh `+0x00`, array at `+0x08`) and
   draws each one, as the next sections describe.
5. It releases the palette's ring block, if it took one, by clearing the block's busy word. When an
   exception leaves the function, the unwind action `005DDAE0` does the same.

### Choosing the segment's shader build

For each segment:

1. The selector's slot 0 returns the segment's `PMaterial`; a null material ends the whole draw with 7.
2. The pass type is the renderer's pass record, or the override below. When the material's
   `m_remapFrom` (`+0x18`) is that pass type, its `m_remapTo` (`+0x20`) is used instead.
3. The material's effect variant (`m_effectVariant`, `+0x00`) gives the technique: the entry of its
   pointer array at `+0x30` (count `+0x28`) indexed by the pass type's `+0x18`, or, when that is
   empty, the first `0x50`-byte record at `+0x20` (count `+0x18`) whose `+0x00` is the pass type.
4. The shader build is the `0x40`-byte variant entry at technique `+0x10` + index × `0x40`. The index
   comes from the instance's `0x48`-byte record for the segment (array at `+0x50`) when that record's
   `+0x30` is this effect variant (index at `+0x28`), and otherwise from `00606A20`, which also fills
   the light record (see [Shader variant selection](shader-variant-selection.md)).

A segment with no technique or no variant is skipped.

### Segment overrides

When the instance's word `+0x98` is non-zero, step *i* of the loop reads the instance's
`0x18`-byte record *i* (array `+0x90`, count `+0x88`) instead of segment *i*. Its `+0x00` names the
segment to draw; a missing record or `+0x00` = −1 skips the step. The word selects the override
pass record:

| `+0x98` | Record accepted when | Override pass record |
|---|---|---|
| 1 | `+0x04` is 0 | `+0x08` |
| 3 | always | `+0x10` |
| 4 | `+0x04` is 2 | `+0x08` |
| 5 | `+0x04` is 3 | `+0x08` |
| any other non-zero | always | none |

A null override leaves the renderer's pass record in use.

### The matrix palette

The palette holds one 64-byte matrix per mesh matrix (mesh `+0x30`, bit 31 masked) after one
leading slot. Up to `0x80` entries it lies on the stack; above that it is a block of the preprocess
ring buffer (`006B6410`, `006B64F0`), whose data starts `0x10` bytes in.

- `005FF090(instance, palette)` writes the instance's world matrix into the leading slot (the 64
  bytes before `palette`): `m_localToWorldMatrix` (`+0x08`) expanded from 4×3 to 4×4 as `006045E0`
  does, or the identity when there is none or bit `0x1` of `m_flags` (`+0x58`) is set. It then jumps to
  `005FF200`.
- `005FF200(instance, palette)` fills entry *i* from the instance's matrix array at `+0x18`. With bit
  `0x2` of `m_flags` set it copies the matrices as they are. Otherwise entry *i* is the product
  (`00185100`) of the palette entry named by the mesh's index *i* (an `i32` array at mesh `+0x58`;
  −1 names the world matrix) and the instance's matrix *i*.

A segment's matrix is palette entry `m_matrixIndex` (segment `+0x04`).

### Sizing the draw

`005EB370(&total, &dynamic, &table, flags, parameterBuffer, effectVariant, variantEntry, segment,
dynamicInstance)` adds up what one segment's draw needs. `flags` is the variant entry's first word:

- bit `0x2`: the material's parameter buffer size (its first `u32`), rounded up to 16;
- bit `0x4`: the `u16` at effect variant `+0x62`;
- bit `0x8`: the per-instance block size at variant entry `+0x38`;
- a dynamic mesh instance whose `+0x08` is set adds `dynamic`: `00670E00(that object, segment)` ×
  `0x88`, rounded up to 16, plus `0x80` when the segment's 16-byte record in its `+0x28` array has a
  non-zero `+0x0C`.

`table` is `(n + 1) × 8 + 0x10` bytes rounded up to 16, where `n` is the variant entry's count at
`+0x28`, plus the resource parameters (`005FD5F0`) among the parameter buffer's definitions
(`+0x10` count, `+0x18` data) and among the variant entry's (`+0x18`, `+0x20`), plus 2 with a
dynamic object. `total` includes `table`.

`00600B30(renderer, total, blocks)` returns false when `total` bytes from the renderer's parameter
ring (`+0x28` start, `+0x30` end, `+0x38` cursor) or `blocks` × `0x80` bytes from its render-block
ring (`+0x50`, `+0x58`, `+0x60`) would pass the ring's limit (`+0x40`, `+0x68`). `blocks` is the
variant entry's `+0x08` count. On false, `0060B980` first calls the renderer's slot 2, `00600D20` for
`PRenderer`, which posts the pending blocks to the render thread and moves both limits on
(`0060FA10`).

### The parameter blocks

`005FECF0(renderer, out, flags, parameterBuffer, draw, …)` fills five pointers for the segment:

| `out` | Flag | Source |
|---|---|---|
| `[0]` | `0x1` | the renderer's per-camera block `+0xA0`, built on first use by `00604750` from `+0x98`, the camera `+0xA8` and `+0x20` |
| `[1]` | `0x2` | `00602A40(renderer, parameterBuffer)` |
| `[2]` | `0x4` | `00602EA0(renderer, draw)` |
| `[3]` | `0x8` | the per-instance block from `00600F30`, then passed to `0060A010` (after `00609D80` for a dynamic mesh instance) |
| `[4]` | none | for a dynamic mesh instance whose slot 1 reports a size: a preprocess ring block of that size, filled by its slot 2 |

A non-zero result from `0060A010` is returned. `0060B980` then reserves `table` bytes from the
parameter ring and passes everything to `0060C020`, which writes the segment's render blocks.

### The per-instance shader parameters

`00600F30(renderer, draw, lights, extra)` takes `variant entry +0x38` + `extra` bytes from the
renderer's parameter ring (wrapping to the start when the cursor would pass the end), writes the
block's size (`+0x38`, without `extra`) into its first `u32`, and returns it, or null when it does
not fit. It then walks the variant entry's parameter definitions (`PShaderParameterDefinition`,
`0x18` bytes; count `+0x18`, array `+0x20`) and computes a value for each by its `m_parameterType`
(`+0x02`).

The top three bits of `+0x12` pick the light: entry 0–3 of the light record `lights` (the four
pointers and the count at `+0x20` that `NUM_LIGHTS` fills). The low 13 bits are the size and `+0x10`
the offset. The value is copied to block + offset only when the offset is at least 4 and offset +
size does not pass the block's first `u32`.

### Light values

With the light present (`PLight`; matrix floats taken from its `m_localToWorldMatrix`, `+0x10`):

| Type | Value written |
|---|---|
| `0xC0` | `m_color` (`+0x00`) |
| `0xC1` | `m_intensity` (`+0x30`) in all four floats |
| `0xC2` | `m_color` × `m_intensity` |
| `0xC3` | inner range, outer range, `1/(outer − inner)`, `−inner/(outer − inner)` (`+0x34`, `+0x38`; the difference at least 1e-6); `99999, 100000, 0, −100000` when the outer range is `FLT_MAX` |
| `0xC4`, `0xC5` | `m_innerConeAngle − 1e-6` (`+0x28`), `m_outerConeAngle + 1e-6` (`+0x2C`), in all four floats |
| `0xC6`, `0xC7` | the cosines of those two angles |
| `0xC8` | inner angle, inner + max(outer − inner, 0.001), cos inner, cos inner − max(cos inner − cos outer, 0.001) |
| `0xC9` | the direction (matrix floats 4–6) through the upper 3×3 of the draw record's object matrix (`+0x50`), normalised, w 0 |
| `0xCA` | the position (matrix floats 8–10) through that matrix (`005DFCD0`), w 1 |
| `0xCB`, `0xCC` | the direction normalised and the position, in world space |
| `0xCD`, `0xCE` | the direction and the position through the renderer's view matrix (`+0xF0`) |
| `0xD8` | the four split far planes, `00606BE0` on `m_shadowCaster` (`+0x18`) |

A light without a matrix uses the identity. For any light type not in the table, and for types
`0xC0`–`0xCE` with no light, the copy takes the evaluator's 16-byte scratch vector, which is zero
until a vector-valued parameter has been written.

### Attenuation, shadow and stream values

These do not depend on the record's light slot:

- `0xCF`–`0xD2`: the terms `a`, `b`, `c` and `d` of `005FF5A0` as one vector, one float per light
  0–3. They are computed once per call for each of lights 0–3 that is present and within the light
  record's count, and default to `a = 0`, `b = 1`, `c = 0`, `d = 1`.
- `0xDE`–`0xE1`: the vertex data block holding the stream `Vertex`, `Normal`, `Color` or `ST` of the
  draw's segment (`+0x38`), as a capture record with the block at `+0x10`. When the record's light slot is empty, a
  missing block logs `Could not find data block on mesh instance for shader parameter '%s'.`.
- `0xE2`: the segment's `m_indexData` (`+0x40`); on the same empty-slot path, none logs `Could not
  find index data block on mesh instance for shader parameter '%s'.`.
- `0xE3`: the LOD blend weight, the first float of the element of the instance's `m_lodLevel`
  (`+0x40`) that draw `+0x18` names (`006073D0`), in all four floats; 1.0 without a LOD level.

The shadow types read the light's `m_shadowCaster` and its `PShadowSplit` records (`+0x10` count,
`+0x18` data, `0xE8` bytes each):

- `0xD3`–`0xD6`: the matrix at `+0x80` of split 0–3. With `m_dataType` (`+0x03`) `0x30` it is
  written as 4×3 (the first three floats of each row), otherwise 4×4. A split the caster lacks logs
  `Shadow split transform %d requested by shader; shadow caster only has %d splits.`.
- `0xD7`: the matrices of all splits, up to `m_arrayElementCount` (`+0x00`), written straight into
  the block at the offset, 4×3 or 4×4 the same way.
- `0xD9`–`0xDC`: the shadow map of split 0–3 as a texture capture record `{0x42, map texture +0x0C,
  caster +0x58, texture}`, the map taken from split `+0xC0`. A split with no map logs `Error: shadow
  caster has no shadow map for this split.` once (byte `02CE9D9D`); a map whose byte `+0x08` is set
  gives a null texture.

With no light, `0xD3`–`0xD6` write the identity, `0xD7` writes identity matrices for the whole array,
and `0xD9`–`0xDC` a record with a null texture.

### Finding a stream by data type

`00670920(segment, &block, type)` walks the segment's vertex data blocks (`0x88` bytes; count `+0x30`,
array `+0x38`) and, in each, its `0x18`-byte stream records (count `+0x08`, array `+0x10`), and
returns the first stream whose `m_renderDataType` (`+0x08`) is `type`, with its block in `block`; null
when none matches.

The data types are static objects named before `main`: `Vertex` `02D3AB18`
(`00165E10`), `Normal` `02D3AB30` (`00165B70`), `ST` `02D3AB48` (`00165BA0`) and `Color` `02D3AB78`
(`001659C0`), each built by `00662C00(object, name, 0)`. `00671670` returns whether a segment has a
stream of a type, the test `SKINNING_ENABLED` uses.

`00600BE0(list, type)` returns the first `0x18`-byte record of a list (count `+0x28`, array `+0x30`)
whose `+0x00` is `type`, or null for a null type; `006718B0` uses it to decide which of a segment's
stream groups get a data block of their own.

### The variant usage counter

After choosing a variant entry, `0060B980` and `006007B0` increment a counter for it when the static
`02CB6360` is non-null: `00606C60(tree, technique, entry)` finds the technique in an ordered tree
(key at node `+0x18`) and returns the address of `u32` number `(entry − technique +0x10) / 0x40` of
the node's array at `+0x28`. `02CB6360` is zero in the image and no instruction writes it, so the
counter never runs.

### The preprocess ring buffer

`006B6410` returns the one `PPreprocessRingBuffer`, the static `02E52270`, built on first use. The run
setup `0079F150` gives it the 2 MiB block it allocates (`+0xDF0` of the application): start, end,
capacity `0x200000`, and write and oldest positions at the start; then it creates the lock
(`005CD0A0`).

`006B6510(ring, size)` takes a block of `size` rounded up to 16, plus a 16-byte header:

1. It returns null when that is not below the capacity (`+0x38`) or the ring has no write position.
2. Under the lock (`005CD4F0`, `005CD820`), while the new block would overlap the oldest live block
   (`006B6690`), it moves the oldest position past every block whose busy word is 0, sleeps 1 ms and
   tries again, logging `Trying to make space in PPreprocessRingBuffer, waiting on
   PPreprocessRingBufferBlock %p (size %d) to be not busy` every 1024 waits.
3. A block that would run past the end is turned into a filler up to the end and the write position
   wraps to the start; otherwise the header gets the next block's address, busy 0 and the requested
   size, and the write position moves on.

`006B64F0` calls it and sets the block's busy word to 1; the user clears it when done. `006B6690`
reports an overlap when the oldest block lies ahead of the write position within `size` bytes, or
the block would reach the end while the oldest block is at the start. `PAsyncProcessBuffer`'s
allocator `00684860` uses the same test.

At shutdown, `0079EDD0` calls `007A12B0`, which closes the lock and, until the oldest position
reaches the write position, advances it past free blocks (`006B64C0`), sleeping 1 ms between tries;
then it clears the ring's positions and capacity, so later requests return null.

## Layouts

`DrawRecord` (`0xA0` bytes, offsets from the start of the 0060B980-stack):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | camera | renderer +`0xA8` |
| `08` | `void*` | cameraToWorld | renderer +`0xB0` |
| `10` | `void*` | view | renderer +`0xF0` |
| `18` | `u32` | lodElement | element of the LOD level read for type `0xE3` |
| `20` | `void*` | instance | the PMeshInstance |
| `28` | `void*` | palette | the matrix palette |
| `30` | `void*` | instancing | instancing segment or null |
| `38` | `void*` | segment | the `0xC0`-byte mesh segment |
| `40` | `u32` | segmentIndex |  |
| `48` | `void*` | segmentMatrix | palette entry m_matrixIndex |
| `50` | `f32[16]` | objectMatrix | inverse of the segment matrix (`00187460`) |
| `90` | `void*` | effectVariant |  |
| `98` | `void*` | variantEntry | the `0x40`-byte variant entry |

`VariantEntry` (`0x40` bytes, offsets from the start of the technique+0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | flags | `0x1`, `0x2`, `0x4`, `0x8`: which parameter blocks the draw builds |
| `08` | `u32` | blockCount | render blocks per draw; bit 31 masked |
| `18` | `u32` | parameterCount | bit 31 masked |
| `20` | `void*` | parameters | PShaderParameterDefinition records, `0x18` bytes each |
| `28` | `u32` | extraCount | counted into the table size |
| `38` | `u32` | instanceBlockSize | per-instance parameter block, its first u32 included |

`PShaderParameterDefinition` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16` | m_arrayElementCount |  |
| `02` | `u8` | m_parameterType | selects the value (tables above) |
| `03` | `u8` | m_dataType | `0x30` writes matrices as 4x3 |
| `08` | `void*` | m_name | bit 0 masked off |
| `10` | `u16` | offset | m_bufferLoc: offset in the block |
| `12` | `u16` | sizeAndLight | low 13 bits size, top 3 bits light slot |
| `14` | `u32` | m_constantBufferLocation |  |

`PPreprocessRingBuffer` (`0x58` bytes, offsets from the start of the 02E52270):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8[40]` | lock | `005CC8A0` initialises, `005CD0A0` creates |
| `28` | `void*` | start |  |
| `30` | `void*` | end |  |
| `38` | `u32` | capacity | `0x200000` |
| `40` | `void*` | write | next block; null when not set up |
| `48` | `void*` | oldest | oldest block still counted as live |
| `50` | `void*` | last | the block handed out last |

`PreprocessRingBlock` (`0x10` bytes, offsets from the start of the block):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | next | the following block |
| `08` | `u32` | busy | 1 from `006B64F0` until the user clears it |
| `0C` | `u32` | size | requested size; a filler holds the bytes to the end |

## Operations

- `0060EC30(instance, value)` writes `value` to `+0x28` of every segment of the mesh at the object's
  `+0x00`. The game's `001E5540` calls it for each object in its list at `+0x18`.

## State

| Address | What |
|---|---|
| `02E52270` | the `PPreprocessRingBuffer` (guard `02E522C8`) |
| `02CB6360` | variant usage tree; zero, never written |
| `02CE9D9D` | set once the missing-shadow-map error is logged |
| `02D3AB18`, `02D3AB30`, `02D3AB48`, `02D3AB78` | the `Vertex`, `Normal`, `ST` and `Color` data types |

## Modding notes

- A shader parameter's light slot has three bits, but only slots 0–3 name lights; slot 4 reads the
  light record's count as a pointer.
- Parameters are copied only when they fit inside the block's size; a definition whose offset is below
  4 is never written.
- A mesh with 128 or more matrices takes its palette from the 2 MiB preprocess ring; a block left
  busy stalls every later request in 1 ms steps.
- An effect variant with no variant for the current pass type draws nothing for that segment, without
  a log line.

## Related

- [Shader variant selection](shader-variant-selection.md): the variant key and the light record `00606A20` fills.
- [Phyre frame](the-frame.md): the frame's draw routine and camera snapshot.
- [Phyre post-effect classes](phyre-post-effect-classes.md): the post effects that draw through `0060B980`.
- [Phyre field schema](phyre-field-schema.md): the `PMeshInstance`, `PLight` and `PShaderParameterDefinition` members.
