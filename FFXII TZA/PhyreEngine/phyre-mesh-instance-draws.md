---
title: "Phyre mesh-instance draws: the segment loop, the bone palette, the per-draw parameter blocks, the light and shadow parameter values and the preprocess ring buffer"
kind: "system"
category: "PhyreEngine"
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

1. It returns `16`<sub>h</sub> unless bit `1`<sub>h</sub> of the renderer's `+08`<sub>h</sub> is set, and `15`<sub>h</sub> when the renderer has
   no pass record at `+80`<sub>h</sub>.
2. With no `instancing` argument it uses the instance's `m_instanceSegment` (`+28`<sub>h</sub>).
3. It builds the matrix palette (below), and stores `value` at the instance's `+C0`<sub>h</sub>.
4. It walks the mesh's segments (`C0`<sub>h</sub> bytes each; count at mesh `+00`<sub>h</sub>, array at `+08`<sub>h</sub>) and
   draws each one, as the next sections describe.
5. It releases the palette's ring block, if it took one, by clearing the block's busy word. When an
   exception leaves the function, the unwind action `005DDAE0` does the same.

### Choosing the segment's shader build

For each segment:

1. The selector's slot 0 returns the segment's `PMaterial`; a null material ends the whole draw with 7.
2. The pass type is the renderer's pass record, or the override below. When the material's
   `m_remapFrom` (`+18`<sub>h</sub>) is that pass type, its `m_remapTo` (`+20`<sub>h</sub>) is used instead.
3. The material's effect variant (`m_effectVariant`, `+00`<sub>h</sub>) gives the technique: the entry of its
   pointer array at `+30`<sub>h</sub> (count `+28`<sub>h</sub>) indexed by the pass type's `+18`<sub>h</sub>, or, when that is
   empty, the first `50`<sub>h</sub>-byte record at `+20`<sub>h</sub> (count `+18`<sub>h</sub>) whose `+00`<sub>h</sub> is the pass type.
4. The shader build is the `40`<sub>h</sub>-byte variant entry at technique `+10`<sub>h</sub> + index × `40`<sub>h</sub>. The index
   comes from the instance's `48`<sub>h</sub>-byte record for the segment (array at `+50`<sub>h</sub>) when that record's
   `+30`<sub>h</sub> is this effect variant (index at `+28`<sub>h</sub>), and otherwise from `00606A20`, which also fills
   the light record (see [Shader variant selection](shader-variant-selection.md)).

A segment with no technique or no variant is skipped.

### Segment overrides

When the instance's word `+98`<sub>h</sub> is non-zero, step *i* of the loop reads the instance's
`18`<sub>h</sub>-byte record *i* (array `+90`<sub>h</sub>, count `+88`<sub>h</sub>) instead of segment *i*. Its `+00`<sub>h</sub> names the
segment to draw; a missing record or `+00`<sub>h</sub> = −1 skips the step. The word selects the override
pass record:

| `+98`<sub>h</sub> | Record accepted when | Override pass record |
|---|---|---|
| 1 | `+04`<sub>h</sub> is 0 | `+08`<sub>h</sub> |
| 3 | always | `+10`<sub>h</sub> |
| 4 | `+04`<sub>h</sub> is 2 | `+08`<sub>h</sub> |
| 5 | `+04`<sub>h</sub> is 3 | `+08`<sub>h</sub> |
| any other non-zero | always | none |

A null override leaves the renderer's pass record in use.

### The matrix palette

The palette holds one 64-byte matrix per mesh matrix (mesh `+30`<sub>h</sub>, bit 31 masked) after one
leading slot. Up to `80`<sub>h</sub> entries it lies on the stack; above that it is a block of the preprocess
ring buffer (`006B6410`, `006B64F0`), whose data starts `10`<sub>h</sub> bytes in.

- `005FF090(instance, palette)` writes the instance's world matrix into the leading slot (the 64
  bytes before `palette`): `m_localToWorldMatrix` (`+08`<sub>h</sub>) expanded from 4×3 to 4×4 as `006045E0`
  does, or the identity when there is none or bit `1`<sub>h</sub> of `m_flags` (`+58`<sub>h</sub>) is set. It then jumps to
  `005FF200`.
- `005FF200(instance, palette)` fills entry *i* from the instance's matrix array at `+18`<sub>h</sub>. With bit
  `2`<sub>h</sub> of `m_flags` set it copies the matrices as they are. Otherwise entry *i* is the product
  (`00185100`) of the palette entry named by the mesh's index *i* (an `i32` array at mesh `+58`<sub>h</sub>;
  −1 names the world matrix) and the instance's matrix *i*.

A segment's matrix is palette entry `m_matrixIndex` (segment `+04`<sub>h</sub>).

### Sizing the draw

`005EB370(&total, &dynamic, &table, flags, parameterBuffer, effectVariant, variantEntry, segment,
dynamicInstance)` adds up what one segment's draw needs. `flags` is the variant entry's first word:

- bit `2`<sub>h</sub>: the material's parameter buffer size (its first `u32`), rounded up to 16;
- bit `4`<sub>h</sub>: the `u16` at effect variant `+62`<sub>h</sub>;
- bit `8`<sub>h</sub>: the per-instance block size at variant entry `+38`<sub>h</sub>;
- a dynamic mesh instance whose `+08`<sub>h</sub> is set adds `dynamic`: `00670E00(that object, segment)` ×
  `88`<sub>h</sub>, rounded up to 16, plus `80`<sub>h</sub> when the segment's 16-byte record in its `+28`<sub>h</sub> array has a
  non-zero `+0C`<sub>h</sub>.

`table` is `(n + 1) × 8 + 10h` bytes rounded up to 16, where `n` is the variant entry's count at
`+28`<sub>h</sub>, plus the resource parameters (`005FD5F0`) among the parameter buffer's definitions
(`+10`<sub>h</sub> count, `+18`<sub>h</sub> data) and among the variant entry's (`+18`<sub>h</sub>, `+20`<sub>h</sub>), plus 2 with a
dynamic object. `total` includes `table`.

`00600B30(renderer, total, blocks)` returns false when `total` bytes from the renderer's parameter
ring (`+28`<sub>h</sub> start, `+30`<sub>h</sub> end, `+38`<sub>h</sub> cursor) or `blocks` × `80`<sub>h</sub> bytes from its render-block
ring (`+50`<sub>h</sub>, `+58`<sub>h</sub>, `+60`<sub>h</sub>) would pass the ring's limit (`+40`<sub>h</sub>, `+68`<sub>h</sub>). `blocks` is the
variant entry's `+08`<sub>h</sub> count. On false, `0060B980` first calls the renderer's slot 2, `00600D20` for
`PRenderer`, which posts the pending blocks to the render thread and moves both limits on
(`0060FA10`).

### The parameter blocks

`005FECF0(renderer, out, flags, parameterBuffer, draw, …)` fills five pointers for the segment:

| `out` | Flag | Source |
|---|---|---|
| `[0]` | `1`<sub>h</sub> | the renderer's per-camera block `+A0`<sub>h</sub>, built on first use by `00604750` from `+98`<sub>h</sub>, the camera `+A8`<sub>h</sub> and `+20`<sub>h</sub> |
| `[1]` | `2`<sub>h</sub> | `00602A40(renderer, parameterBuffer)` |
| `[2]` | `4`<sub>h</sub> | `00602EA0(renderer, draw)` |
| `[3]` | `8`<sub>h</sub> | the per-instance block from `00600F30`, then passed to `0060A010` (after `00609D80` for a dynamic mesh instance) |
| `[4]` | none | for a dynamic mesh instance whose slot 1 reports a size: a preprocess ring block of that size, filled by its slot 2 |

A non-zero result from `0060A010` is returned. `0060B980` then reserves `table` bytes from the
parameter ring and passes everything to `0060C020`, which writes the segment's render blocks.

### The per-instance shader parameters

`00600F30(renderer, draw, lights, extra)` takes `variant entry +38h` + `extra` bytes from the
renderer's parameter ring (wrapping to the start when the cursor would pass the end), writes the
block's size (`+38`<sub>h</sub>, without `extra`) into its first `u32`, and returns it, or null when it does
not fit. It then walks the variant entry's parameter definitions (`PShaderParameterDefinition`,
`18`<sub>h</sub> bytes; count `+18`<sub>h</sub>, array `+20`<sub>h</sub>) and computes a value for each by its `m_parameterType`
(`+02`<sub>h</sub>).

The top three bits of `+12`<sub>h</sub> pick the light: entry 0–3 of the light record `lights` (the four
pointers and the count at `+20`<sub>h</sub> that `NUM_LIGHTS` fills). The low 13 bits are the size and `+10`<sub>h</sub>
the offset. The value is copied to block + offset only when the offset is at least 4 and offset +
size does not pass the block's first `u32`.

### Light values

With the light present (`PLight`; matrix floats taken from its `m_localToWorldMatrix`, `+10`<sub>h</sub>):

| Type | Value written |
|---|---|
| `C0`<sub>h</sub> | `m_color` (`+00`<sub>h</sub>) |
| `C1`<sub>h</sub> | `m_intensity` (`+30`<sub>h</sub>) in all four floats |
| `C2`<sub>h</sub> | `m_color` × `m_intensity` |
| `C3`<sub>h</sub> | inner range, outer range, `1/(outer − inner)`, `−inner/(outer − inner)` (`+34`<sub>h</sub>, `+38`<sub>h</sub>; the difference at least 1e-6); `99999, 100000, 0, −100000` when the outer range is `FLT_MAX` |
| `C4`<sub>h</sub>, `C5`<sub>h</sub> | `m_innerConeAngle − 1e-6` (`+28`<sub>h</sub>), `m_outerConeAngle + 1e-6` (`+2C`<sub>h</sub>), in all four floats |
| `C6`<sub>h</sub>, `C7`<sub>h</sub> | the cosines of those two angles |
| `C8`<sub>h</sub> | inner angle, inner + max(outer − inner, 0.001), cos inner, cos inner − max(cos inner − cos outer, 0.001) |
| `C9`<sub>h</sub> | the direction (matrix floats 4–6) through the upper 3×3 of the draw record's object matrix (`+50`<sub>h</sub>), normalised, w 0 |
| `CA`<sub>h</sub> | the position (matrix floats 8–10) through that matrix (`005DFCD0`), w 1 |
| `CB`<sub>h</sub>, `CC`<sub>h</sub> | the direction normalised and the position, in world space |
| `CD`<sub>h</sub>, `CE`<sub>h</sub> | the direction and the position through the renderer's view matrix (`+F0`<sub>h</sub>) |
| `D8`<sub>h</sub> | the four split far planes, `00606BE0` on `m_shadowCaster` (`+18`<sub>h</sub>) |

A light without a matrix uses the identity. For any light type not in the table, and for types
`C0`<sub>h</sub>–`CE`<sub>h</sub> with no light, the copy takes the evaluator's 16-byte scratch vector, which is zero
until a vector-valued parameter has been written.

### Attenuation, shadow and stream values

These do not depend on the record's light slot:

- `CF`<sub>h</sub>–`D2`<sub>h</sub>: the terms `a`, `b`, `c` and `d` of `005FF5A0` as one vector, one float per light
  0–3. They are computed once per call for each of lights 0–3 that is present and within the light
  record's count, and default to `a = 0`, `b = 1`, `c = 0`, `d = 1`.
- `DE`<sub>h</sub>–`E1`<sub>h</sub>: the vertex data block holding the stream `Vertex`, `Normal`, `Color` or `ST` of the
  draw's segment (`+38`<sub>h</sub>), as a capture record with the block at `+10`<sub>h</sub>. When the record's light slot is empty, a
  missing block logs `Could not find data block on mesh instance for shader parameter '%s'.`.
- `E2`<sub>h</sub>: the segment's `m_indexData` (`+40`<sub>h</sub>); on the same empty-slot path, none logs `Could not
  find index data block on mesh instance for shader parameter '%s'.`.
- `E3`<sub>h</sub>: the LOD blend weight, the first float of the element of the instance's `m_lodLevel`
  (`+40`<sub>h</sub>) that draw `+18`<sub>h</sub> names (`006073D0`), in all four floats; 1.0 without a LOD level.

The shadow types read the light's `m_shadowCaster` and its `PShadowSplit` records (`+10`<sub>h</sub> count,
`+18`<sub>h</sub> data, `E8`<sub>h</sub> bytes each):

- `D3`<sub>h</sub>–`D6`<sub>h</sub>: the matrix at `+80`<sub>h</sub> of split 0–3. With `m_dataType` (`+03`<sub>h</sub>) `30`<sub>h</sub> it is
  written as 4×3 (the first three floats of each row), otherwise 4×4. A split the caster lacks logs
  `Shadow split transform %d requested by shader; shadow caster only has %d splits.`.
- `D7`<sub>h</sub>: the matrices of all splits, up to `m_arrayElementCount` (`+00`<sub>h</sub>), written straight into
  the block at the offset, 4×3 or 4×4 the same way.
- `D9`<sub>h</sub>–`DC`<sub>h</sub>: the shadow map of split 0–3 as a texture capture record `{42h, map texture +0Ch,
  caster +58h, texture}`, the map taken from split `+C0`<sub>h</sub>. A split with no map logs `Error: shadow
  caster has no shadow map for this split.` once (byte `02CE9D9D`); a map whose byte `+08`<sub>h</sub> is set
  gives a null texture.

With no light, `D3`<sub>h</sub>–`D6`<sub>h</sub> write the identity, `D7`<sub>h</sub> writes identity matrices for the whole array,
and `D9`<sub>h</sub>–`DC`<sub>h</sub> a record with a null texture.

### Finding a stream by data type

`00670920(segment, &block, type)` walks the segment's vertex data blocks (`88`<sub>h</sub> bytes; count `+30`<sub>h</sub>,
array `+38`<sub>h</sub>) and, in each, its `18`<sub>h</sub>-byte stream records (count `+08`<sub>h</sub>, array `+10`<sub>h</sub>), and
returns the first stream whose `m_renderDataType` (`+08`<sub>h</sub>) is `type`, with its block in `block`; null
when none matches.

The data types are static objects named before `main`: `Vertex` `02D3AB18`
(`00165E10`), `Normal` `02D3AB30` (`00165B70`), `ST` `02D3AB48` (`00165BA0`) and `Color` `02D3AB78`
(`001659C0`), each built by `00662C00(object, name, 0)`. `00671670` returns whether a segment has a
stream of a type, the test `SKINNING_ENABLED` uses.

`00600BE0(list, type)` returns the first `18`<sub>h</sub>-byte record of a list (count `+28`<sub>h</sub>, array `+30`<sub>h</sub>)
whose `+00`<sub>h</sub> is `type`, or null for a null type; `006718B0` uses it to decide which of a segment's
stream groups get a data block of their own.

### The variant usage counter

After choosing a variant entry, `0060B980` and `006007B0` increment a counter for it when the static
`02CB6360` is non-null: `00606C60(tree, technique, entry)` finds the technique in an ordered tree
(key at node `+18`<sub>h</sub>) and returns the address of `u32` number `(entry − technique +10h) / 40h` of
the node's array at `+28`<sub>h</sub>. `02CB6360` is zero in the image and no instruction writes it, so the
counter never runs.

### The preprocess ring buffer

`006B6410` returns the one `PPreprocessRingBuffer`, the static `02E52270`, built on first use. The run
setup `0079F150` gives it the 2 MiB block it allocates (`+DF0`<sub>h</sub> of the application): start, end,
capacity `200000`<sub>h</sub>, and write and oldest positions at the start; then it creates the lock
(`005CD0A0`).

`006B6510(ring, size)` takes a block of `size` rounded up to 16, plus a 16-byte header:

1. It returns null when that is not below the capacity (`+38`<sub>h</sub>) or the ring has no write position.
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

`DrawRecord` (`A0`<sub>h</sub> bytes, offsets from the start of the 0060B980-stack):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | camera | renderer +`A8`<sub>h</sub> |
| `08`<sub>h</sub> | `void*` | cameraToWorld | renderer +`B0`<sub>h</sub> |
| `10`<sub>h</sub> | `void*` | view | renderer +`F0`<sub>h</sub> |
| `18`<sub>h</sub> | `u32` | lodElement | element of the LOD level read for type `E3`<sub>h</sub> |
| `20`<sub>h</sub> | `void*` | instance | the PMeshInstance |
| `28`<sub>h</sub> | `void*` | palette | the matrix palette |
| `30`<sub>h</sub> | `void*` | instancing | instancing segment or null |
| `38`<sub>h</sub> | `void*` | segment | the `C0`<sub>h</sub>-byte mesh segment |
| `40`<sub>h</sub> | `u32` | segmentIndex |  |
| `48`<sub>h</sub> | `void*` | segmentMatrix | palette entry m_matrixIndex |
| `50`<sub>h</sub> | `f32[16]` | objectMatrix | inverse of the segment matrix (`00187460`) |
| `90`<sub>h</sub> | `void*` | effectVariant |  |
| `98`<sub>h</sub> | `void*` | variantEntry | the `40`<sub>h</sub>-byte variant entry |

`VariantEntry` (`40`<sub>h</sub> bytes, offsets from the start of the technique+`10`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | flags | `1`<sub>h</sub>, `2`<sub>h</sub>, `4`<sub>h</sub>, `8`<sub>h</sub>: which parameter blocks the draw builds |
| `08`<sub>h</sub> | `u32` | blockCount | render blocks per draw; bit 31 masked |
| `18`<sub>h</sub> | `u32` | parameterCount | bit 31 masked |
| `20`<sub>h</sub> | `void*` | parameters | PShaderParameterDefinition records, `18`<sub>h</sub> bytes each |
| `28`<sub>h</sub> | `u32` | extraCount | counted into the table size |
| `38`<sub>h</sub> | `u32` | instanceBlockSize | per-instance parameter block, its first u32 included |

`PShaderParameterDefinition` (`18`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | m_arrayElementCount |  |
| `02`<sub>h</sub> | `u8` | m_parameterType | selects the value (tables above) |
| `03`<sub>h</sub> | `u8` | m_dataType | `30`<sub>h</sub> writes matrices as 4x3 |
| `08`<sub>h</sub> | `void*` | m_name | bit 0 masked off |
| `10`<sub>h</sub> | `u16` | offset | m_bufferLoc: offset in the block |
| `12`<sub>h</sub> | `u16` | sizeAndLight | low 13 bits size, top 3 bits light slot |
| `14`<sub>h</sub> | `u32` | m_constantBufferLocation |  |

`PPreprocessRingBuffer` (`58`<sub>h</sub> bytes, offsets from the start of the 02E52270):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8[40]` | lock | `005CC8A0` initialises, `005CD0A0` creates |
| `28`<sub>h</sub> | `void*` | start |  |
| `30`<sub>h</sub> | `void*` | end |  |
| `38`<sub>h</sub> | `u32` | capacity | `200000`<sub>h</sub> |
| `40`<sub>h</sub> | `void*` | write | next block; null when not set up |
| `48`<sub>h</sub> | `void*` | oldest | oldest block still counted as live |
| `50`<sub>h</sub> | `void*` | last | the block handed out last |

`PreprocessRingBlock` (`10`<sub>h</sub> bytes, offsets from the start of the block):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | next | the following block |
| `08`<sub>h</sub> | `u32` | busy | 1 from `006B64F0` until the user clears it |
| `0C`<sub>h</sub> | `u32` | size | requested size; a filler holds the bytes to the end |

## Operations

- `0060EC30(instance, value)` writes `value` to `+28`<sub>h</sub> of every segment of the mesh at the object's
  `+00`<sub>h</sub>. The game's `001E5540` calls it for each object in its list at `+18`<sub>h</sub>.

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
