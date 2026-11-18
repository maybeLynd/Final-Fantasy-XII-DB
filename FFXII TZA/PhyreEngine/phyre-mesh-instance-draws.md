[Home](../../README.md) / [PhyreEngine](README.md) / Phyre mesh-instance draws

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Phyre mesh-instance draws: the segment loop, the bone palette, the per-draw parameter blocks, the light and shadow parameter values and the preprocess ring buffer | system | PhyreEngine | Drawing and shaders | How PhyreEngine draws one mesh instance in the executable: 0x0060B980 walks the mesh's segments, picks each segment's material, technique and shader variant, builds the bone-matrix palette, sizes and fills the per-draw parameter blocks, and the evaluator 0x00600F30 writes the light, shadow, vertex-stream and LOD values a shader asks for by parameter type; with the 2 MiB PPreprocessRingBuffer that holds large palettes and dynamic-mesh data, and the variant usage counter that never runs. | 0x0060B980, 0x005FF090, 0x005FF200, 0x005EB370, 0x00600B30, 0x005FECF0, 0x00600F30, 0x00670920, 0x00600BE0, 0x00606C60, 0x02CB6360, 0x006B6410, 0x006B64F0, 0x006B6510, 0x006B6690, 0x006B64C0, 0x007A12B0, 0x02E52270, 0x005DDAE0, 0x0060EC30 |

## What the player sees

A PhyreEngine mesh instance is drawn by the routine on this page; 27 routines of the game draw
through it, among them the bitmap-font text and the FXAA pass. It decides which shader build each
part of the model uses, poses skinned models from their bone matrices, and hands each shader the
colour, position, fall-off and shadow matrices of up to four lights. A part whose effect has no
shader build for the current pass is not drawn.

Each part of a model has a material. The material's effect holds one technique per render pass, and each technique
holds a list of shader builds; the game takes the technique for the current pass and then one build from its list for
that part.

## How it works

### The mesh-instance draw

`0x0060B980(renderer, instance, selector, instancing, value, flag)` draws one `PMeshInstance`. 58 call
sites in 27 functions call it, among them the bitmap-font text and the FXAA pass. In order:

1. It returns `0x16` unless bit `0x1` of the renderer's `+0x08` is set, and `0x15` when the renderer has
   no pass record at `+0x80`.
2. With no `instancing` argument it uses the instance's `m_instanceSegment` (`+0x28`).
3. It builds the matrix palette (below), and stores `value` at the instance's `+0xC0`.
4. It walks the mesh's segments (`0xC0` bytes each; count at mesh `+0x00`, array at `+0x08`) and
   draws each one, as the next sections describe.
5. It releases the palette's ring block, if it took one, by clearing the block's busy word. When an
   exception leaves the function, the unwind action `0x005DDAE0` does the same.

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
   `+0x30` is this effect variant (index at `+0x28`), and otherwise from `0x00606A20`, which also fills
   the light record (see [Shader variant selection](shader-variant-selection.md)).

A segment with no technique or no variant is skipped.

The `0x48`-byte record is a `PMeshInstanceSegmentContext`. `PMeshInstance` (descriptor `0x02CB6E80`) registers the
array of them as its member `m_segmentContext` at `+0x48`¹, with the type name
`PArray<PMeshInstanceSegmentContext>`²: the count at `+0x48` and the records at `+0x50`, one per
segment. The draw takes segment i's record at `+0x50` plus i × `0x48`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005E5865` |
| ² | `0x005E5806` |
| ³ | `0x0060BC0A`, `0x0060BC0E`, `0x0060BC13` |

</details>

In the record, `+0x28` is the variant entry's index and `+0x30` the effect variant it belongs to¹, and the reflected member `m_streamBindings` at `+0x38` is a
`PSharray<PMeshInstanceSegmentStreamBinding *>` (count `+0x38`, array `+0x40`; `0x005E6860`). The descriptor's
construct slot `0x005CF520` clears `+0x00` to `+0x23`, sets `+0x28` to -1² and clears `+0x30` and the
bindings³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0060BD44`, `0x0060BDCF` |
| ² | `0x005CF53B` |
| ³ | `0x005CF542`, `0x005CF546`, `0x005CF549` |

</details>

Its copy slot `0x005CF610` copies the record field by field¹ and the bindings through
`0x00646C00`. Its destroy slot `0x005CEBA0` frees the bindings' array when bit `0x80000000` of the count is clear
and the count is above 1² and zeroes the pair³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005CF628`, `0x005CF62F`, `0x005CF638`, `0x005CF640`, `0x005CF647` |
| ² | `0x005CEBC7`, `0x005CEBD2` |
| ³ | `0x005CEBD9`, `0x005CEBDD` |

</details>

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
| any other non-zero | always | no override |

A null override leaves the renderer's pass record in use.

### The matrix palette

The palette holds one 64-byte matrix per mesh matrix (mesh `+0x30`, bit `0x80000000` masked) after one
leading slot. Up to `0x80` entries it lies on the stack; above that it is a block of the preprocess
ring buffer¹, whose data starts `0x10` bytes in.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006B6410`, `0x006B64F0` |

</details>

- `0x005FF090(instance, palette)` writes the instance's world matrix into the leading slot (the 64
  bytes before `palette`): `m_localToWorldMatrix` (`+0x08`) expanded from 4×3 to 4×4 as `0x006045E0`
  does, or the identity when there is no world matrix or bit `0x1` of `m_flags` (`+0x58`) is set. It then jumps to
  `0x005FF200`.
- `0x005FF200(instance, palette)` fills entry *i* from the instance's matrix array at `+0x18`. With bit
  `0x2` of `m_flags` set it copies the matrices as they are. Otherwise entry *i* is the product
 ¹ of the palette entry named by the mesh's index *i* (an `i32` array at mesh `+0x58`;
  −1 names the world matrix) and the instance's matrix *i*.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00185100` |

</details>

A segment's matrix is palette entry `m_matrixIndex` (segment `+0x04`).

### Sizing the draw

`0x005EB370(&total, &dynamic, &table, flags, parameterBuffer, effectVariant, variantEntry, segment,
dynamicInstance)` adds up what one segment's draw needs. `flags` is the variant entry's first word:

- bit `0x2`: the material's parameter buffer size (its first `u32`), rounded up to 16;
- bit `0x4`: the `u16` at effect variant `+0x62`;
- bit `0x8`: the per-instance block size at variant entry `+0x38`;
- a dynamic mesh instance whose `+0x08` is set adds `dynamic`: `0x00670E00(that object, segment)` ×
  `0x88`, rounded up to 16, plus `0x80` when the segment's 16-byte record in its `+0x28` array has a
  non-zero `+0x0C`.

`table` is `(n + 1) × 8 + 0x10` bytes rounded up to 16, where `n` is the variant entry's count at
`+0x28`, plus the resource parameters¹ among the parameter buffer's definitions
(`+0x10` count, `+0x18` data) and among the variant entry's (`+0x18`, `+0x20`), plus 2 with a
dynamic object. `total` includes `table`. All three counts have bit `0x80000000` masked².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005FD5F0` |
| ² | `0x005EB431`, `0x005EB436`, `0x005EB46A` |

</details>

`0x005EB370` zeroes `total` and `dynamic` first¹, so `dynamic` stays 0 without a
dynamic object. It stores `table` last² and adds it to `total`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005EB3B2`, `0x005EB3B4` |
| ² | `0x005EB4CD` |
| ³ | `0x005EB4D1` |

</details>

`0x00600B30(renderer, total, blocks)` tests the renderer's parameter ring (`+0x28` start, `+0x30` end,
`+0x38` cursor, `+0x40` limit) for `total` bytes and its render-block ring (`+0x50`, `+0x58`, `+0x60`,
limit `+0x68`) for `blocks` × `0x80` bytes, and stores nothing. `blocks` is the variant entry's `+0x08`
count. It returns false when either ring fails, and true otherwise:

- A request that fits before the ring's end fails when the cursor is at or before the limit and
  cursor + size passes it¹.
- A request that has to wrap to the start, or is larger than the whole ring, fails whenever the cursor
  is at or before the limit². With the limit behind the cursor it passes,
  whatever start + size is, so the wrapped block can run past the limit.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00600BB7`-`0x00600BBF`, `0x00600BC9`-`0x00600BD1` |
| ² | `0x00600B72`, `0x00600BA8` |

</details>

On false, `0x0060B980` first calls the renderer's slot 2, `0x00600D20` for
`PRenderer`, which posts the pending blocks to the render thread and moves both limits on¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0060FA10` |

</details>

### The parameter blocks

`0x005FECF0(renderer, out, flags, parameterBuffer, draw, …)` fills five pointers for the segment:

| `out` | Flag | Source |
|---|---|---|
| `[0]` | `0x1` | the renderer's per-camera block `+0xA0`, built on first use by `0x00604750` from `+0x98`, the camera `+0xA8` and `+0x20`; null, with nothing built, while `+0x98` or the camera is null (`0x005FED2F`, `0x005FED3F`) |
| `[1]` | `0x2` | `0x00602A40(renderer, parameterBuffer)` |
| `[2]` | `0x4` | `0x00602EA0(renderer, draw)` |
| `[3]` | `0x8` | the per-instance block from `0x00600F30`, then passed to `0x0060A010` (after `0x00609D80` for a dynamic mesh instance); null when `0x00600F30` returns null, and then neither is called (`0x005FEDC4`, `0x005FEE18`) |
| `[4]` | no flag | for a dynamic mesh instance whose slot 1 reports a size: a preprocess ring block of that size (`0x006B64F0`), filled by its slot 2, which is called even when the ring returns null (`0x005FEE51`); null otherwise (`0x005FEE55`) |

A slot whose flag is clear is left as it is. For a dynamic mesh instance, `0x00609D80` also receives
`out` + `0x28` and `out` + `0x30` and writes them: the first when `0x00670E00` returns non-zero and the
segment's 16-byte record has a non-zero `+0x08`¹, the second when that record's `+0x0C` is
non-zero². Its result is `0x0060A010`'s fifth argument³, 0 without a dynamic
mesh instance.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00609E34` |
| ² | `0x00609F93` |
| ³ | `0x005FEE08` |

</details>

For each parameter it walks, `0x00602EA0` reads the type byte `+0x03`¹ and handles types `0x30` and
`0x31`. Any other type prints the type-id message at `0x00D4B3C8`² once,
setting the byte `0x02CE9D9C`³, and the walk goes on to the next parameter⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00603356` |
| ² | `0x005CDAA0` |
| ³ | `0x00603382`-`0x00603396` |
| ⁴ | `0x00603717` |

</details>

A non-zero result from `0x0060A010` is returned before `out[3]` and `out[4]` are written¹;
every other path returns 0². `0x0060B980` then reserves `table` bytes from the
parameter ring and passes everything to `0x0060C020`, which writes the segment's render blocks.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005FEE16` |
| ² | `0x005FEE59` |

</details>

### The per-instance shader parameters

`0x00600F30(renderer, draw, lights, extra)` takes `variant entry +0x38` + `extra` bytes from the
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
| `0xCA` | the position (matrix floats 8–10) through that matrix (`0x005DFCD0`), w 1 |
| `0xCB`, `0xCC` | the direction normalised and the position, in world space |
| `0xCD`, `0xCE` | the direction and the position through the renderer's view matrix (`+0xF0`) |
| `0xD8` | the four split far planes, `0x00606BE0` on `m_shadowCaster` (`+0x18`) |

A light without a matrix uses the identity. For any light type not in the table, and for types
`0xC0`–`0xCE` with no light, the copy takes the evaluator's 16-byte scratch vector, which is zero
until a vector-valued parameter has been written.

### Attenuation, shadow and stream values

These do not depend on the record's light slot:

- `0xCF`–`0xD2`: the terms `a`, `b`, `c` and `d` of `0x005FF5A0` as one vector, one float per light
  0–3. They are computed once per call for each of lights 0–3 that is present and within the light
  record's count, and default to `a = 0`, `b = 1`, `c = 0`, `d = 1`.
- `0xDE`–`0xE1`: the vertex data block holding the stream `Vertex`, `Normal`, `Color` or `ST` of the
  draw's segment (`+0x38`), as a capture record with the block at `+0x10`. When the record's light slot is empty, a
  missing block logs `Could not find data block on mesh instance for shader parameter '%s'.`.
- `0xE2`: the segment's `m_indexData` (`+0x40`); on the same empty-slot path, a missing one logs `Could not
  find index data block on mesh instance for shader parameter '%s'.`.
- `0xE3`: the LOD blend weight, the first float of the element of the instance's `m_lodLevel`
  (`+0x40`) that draw `+0x18` names¹, in all four floats; 1.0 without a LOD level.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006073D0` |

</details>

The shadow types read the light's `m_shadowCaster` and its `PShadowSplit` records (`+0x10` count,
`+0x18` data, `0xE8` bytes each):

- `0xD3`–`0xD6`: the matrix at `+0x80` of split 0–3. With `m_dataType` (`+0x03`) `0x30` it is
  written as 4×3 (the first three floats of each row), otherwise 4×4. A split the caster lacks logs
  `Shadow split transform %d requested by shader; shadow caster only has %d splits.`.
- `0xD7`: the matrices of all splits, up to `m_arrayElementCount` (`+0x00`), written straight into
  the block at the offset, 4×3 or 4×4 the same way.
- `0xD9`–`0xDC`: the shadow map of split 0–3 as a texture capture record `{0x42, map texture +0x0C,
  caster +0x58, texture}`, the map taken from split `+0xC0`. A split with no map logs `Error: shadow
  caster has no shadow map for this split.` once (byte `0x02CE9D9D`); a map whose byte `+0x08` is set
  gives a null texture.

With no light, `0xD3`–`0xD6` write the identity, `0xD7` writes identity matrices for the whole array,
and `0xD9`–`0xDC` a record with a null texture.

### Finding a stream by data type

`0x00670920(segment, &block, type)` walks the segment's vertex data blocks (`0x88` bytes; count `+0x30`,
array `+0x38`) and, in each, its `0x18`-byte stream records (count `+0x08`, array `+0x10`), and
returns the first stream whose `m_renderDataType` (`+0x08`) is `type`, with its block in `block`; null
when no stream matches. It sets `block` to null on entry¹, so `block` is null too when no
stream matches, and both counts have bit `0x80000000` masked².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00670934` |
| ² | `0x0067094A`, `0x00670976` |

</details>

The data types are static objects named before `main`: `Vertex` `0x02D3AB18`¹, `Normal` `0x02D3AB30`², `ST` `0x02D3AB48`³ and `Color` `0x02D3AB78`⁴, each built by `0x00662C00(object, name, 0)`. `0x00671670` returns whether a segment has a
stream of a type, the test `SKINNING_ENABLED` uses.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00165E10` |
| ² | `0x00165B70` |
| ³ | `0x00165BA0` |
| ⁴ | `0x001659C0` |

</details>

`0x00600BE0(list, type)` returns the first `0x18`-byte record of a list (count `+0x28`, array `+0x30`)
whose `+0x00` is `type`, or null for a null type; `0x006718B0` uses it to decide which of a segment's
stream groups get a data block of their own. It also returns null when no record matches¹, and masks bit `0x80000000` of the count².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00600C0E` |
| ² | `0x00600BEC` |

</details>

### The variant usage counter

After choosing a variant entry, `0x0060B980` and `0x006007B0` increment a counter for it when the static
`0x02CB6360` is non-null: `0x00606C60(tree, technique, entry)` finds the technique in an ordered tree
(key at node `+0x18`) and returns the address of `u32` number `(entry − technique +0x10) / 0x40` of
the node's array at `+0x28`. `0x02CB6360` is zero in the image and no instruction writes it, so the
counter never runs.

The walk in `0x00606C60` starts at the tree's `+0x18` and ends on reaching the tree object itself¹; a node whose key is above the technique leads to its `+0x00`, one below to
its `+0x08`. With no node for the technique it returns null².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00606C67`, `0x00606C8F` |
| ² | `0x00606C94`, `0x00606C9E` |

</details>

### The preprocess ring buffer

`0x006B6410` returns the one `PPreprocessRingBuffer`, the static `0x02E52270`, built on first use. The run
setup `0x0079F150` gives it the 2 MiB block it allocates (`+0xDF0` of the application): start, end,
capacity `0x200000`, and write and oldest positions at the start; then it creates the lock¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005CD0A0` |

</details>

The first use, behind the guard `0x02E522C8`¹, builds the lock² and zeroes the
rest³: the start `0x02E52298`, the end `0x02E522A0`, the capacity `0x02E522A8`, the write and
oldest positions `0x02E522B0` and `0x02E522B8` (one 16-byte store) and the last block `0x02E522C0`. It registers its
teardown with `atexit`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008092FC`, `0x0080929C` |
| ² | `0x005CC8A0` |
| ³ | `0x006B6468`-`0x006B6487` |
| ⁴ | `0x006B648E` |

</details>

`0x006B6510(ring, size)` takes a block of `size` rounded up to 16, plus a 16-byte header:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It returns null when that is not below the capacity (`+0x38`) or the ring has no write position. |   |
| 2 | Under the lock, while the new block would overlap the oldest live block, it moves the oldest position past every block whose busy word is 0, sleeps 1 ms and tries again, logging `Trying to make space in PPreprocessRingBuffer, waiting on PPreprocessRingBufferBlock %p (size %d) to be not busy` every 1024 waits. | `0x005CD4F0`, `0x005CD820`<br>`0x006B6690` |
| 3 | Each move stops at the first block whose busy word is not 0, or at the write position. | `0x006B6582`-`0x006B659B`, `0x006B65F0`-`0x006B6609` |
| 4 | A block that would run past the end is turned into a filler up to the end and the write position wraps to the start; otherwise the header gets the next block's address, busy 0 and the requested size, and the write position moves on. |   |
| 5 | The filler's size word holds the bytes to the end and its next address is the start; the body then repeats the overlap test from the start. A block that ends exactly at the end makes the start both its next address and the write position. | `0x006B6632`-`0x006B663A`<br>`0x006B6661`<br>`0x006B6646`-`0x006B664F` |
| 6 | The block is recorded as the last one (`+0x50`, `0x006B6667`), the lock is released and the block's header is returned. | `0x006B6674` |

`0x006B64F0` calls it and sets the block's busy word to 1; the user clears it when done. `0x006B6690`
reports an overlap when the oldest block lies ahead of the write position within `size` bytes, or
the block would reach the end while the oldest block is at the start. `PAsyncProcessBuffer`'s
allocator `0x00684860` uses the same test.

At shutdown, `0x0079EDD0` calls `0x007A12B0`, which closes the lock and, until the oldest position
reaches the write position, advances it past free blocks¹, sleeping 1 ms between tries;
then it clears the ring's positions and capacity, so later requests return null.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006B64C0` |

</details>

The lock is closed by `0x005CD6D0`, which acts only when the lock's first byte is set¹.
`0x006B64C0` returns 0 on every path², so only reaching the write position ends the wait,
and a block left busy keeps it waiting. The clearing also zeroes the start and end³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005CD6D6` |
| ² | `0x006B64EA` |
| ³ | `0x007A12FA`-`0x007A130A` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PLight` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | m_color | the light colour, written as parameter type `0xC0` and, times m_intensity, as `0xC2`; m_color (f32[4]), registered by `0x006BED60` (`0x00632960` at `0x006BEDFA`); no shipped .phyre file declares PLight; the script method setColorRGBA (registered at `0x006BF329`) stores red, green, blue and alpha at `+0x00`, `+0x04`, `+0x08` and `+0x0C` through `0x006C0520` |
| `+0x28` | `f32` | m_innerConeAngle | the inner cone angle, written as parameter types `0xC4` and `0xC5`; m_innerConeAngle (f32), registered by `0x006BED60` (`0x00632960` at `0x006BEFC4`); no shipped .phyre file declares PLight; the script method setInnerConeAngle (registered at `0x006BF3F3`) stores it through `0x006C05C0` |
| `+0x34` | `f32` | m_innerRange | the inner range of parameter type `0xC3`; m_innerRange (f32), registered by `0x006BED60` (`0x00632960` at `0x006BF11D`); no shipped .phyre file declares PLight; the script method setRange (registered at `0x006BF70D`) stores the inner range here and the outer range at `+0x38` through `0x006C05F0` |
| `+0x3C` | `f32` | m_scatteringIntensity | the scattering intensity; m_scatteringIntensity (f32), registered by `0x006BED60` (`0x00632960` at `0x006BF203`); no shipped .phyre file declares PLight; the script method setScatteringIntensity (registered at `0x006BF89A`) stores it through `0x006C0600` |

Bytes `+0x04` to `+0x07` of `PShaderParameterDefinition` lie between `m_dataType` (`+0x03`) and `m_name` (`+0x08`); no registered member covers them (`0x005DAF10` registers the `0x18`-byte class at `0x005DAF60`).

### Draw records

The structures below are the ones the mechanisms above use.

`DrawRecord` (`0xA0` bytes, offsets from the start of the 0x0060B980-stack):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | camera | renderer `+0xA8` |
| `+0x08` | `void*` | cameraToWorld | renderer `+0xB0` |
| `+0x10` | `void*` | view | renderer `+0xF0` |
| `+0x18` | `u32` | lodElement | element of the LOD level read for type `0xE3` |
| `+0x20` | `void*` | instance | the PMeshInstance |
| `+0x28` | `void*` | palette | the matrix palette |
| `+0x30` | `void*` | instancing | instancing segment or null |
| `+0x38` | `void*` | segment | the `0xC0`-byte mesh segment |
| `+0x40` | `u32` | segmentIndex |  |
| `+0x48` | `void*` | segmentMatrix | palette entry m_matrixIndex |
| `+0x50` | `f32[16]` | objectMatrix | inverse of the segment matrix (`0x00187460`) |
| `+0x90` | `void*` | effectVariant |  |
| `+0x98` | `void*` | variantEntry | the `0x40`-byte variant entry |

`VariantEntry` (`0x40` bytes, offsets from the start of the technique+0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | flags | `0x1`, `0x2`, `0x4`, `0x8`: which parameter blocks the draw builds |
| `+0x08` | `u32` | blockCount | render blocks per draw; bit `0x80000000` masked |
| `+0x18` | `u32` | parameterCount | bit `0x80000000` masked |
| `+0x20` | `void*` | parameters | PShaderParameterDefinition records, `0x18` bytes each |
| `+0x28` | `u32` | extraCount | counted into the table size |
| `+0x38` | `u32` | instanceBlockSize | per-instance parameter block, its first u32 included |

`PShaderParameterDefinition` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | m_arrayElementCount |  |
| `+0x02` | `u8` | m_parameterType | selects the value (tables above) |
| `+0x03` | `u8` | m_dataType | `0x30` writes matrices as 4x3 |
| `+0x08` | `void*` | m_name | bit `0x1` masked off |
| `+0x10` | `u16` | offset | m_bufferLoc: offset in the block |
| `+0x12` | `u16` | sizeAndLight | low 13 bits size, top 3 bits light slot |
| `+0x14` | `u32` | m_constantBufferLocation |  |

`PPreprocessRingBuffer` (`0x58` bytes, offsets from the start of the 0x02E52270):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[40]` | lock | `0x005CC8A0` initialises, `0x005CD0A0` creates |
| `+0x28` | `void*` | start |  |
| `+0x30` | `void*` | end |  |
| `+0x38` | `u32` | capacity | `0x200000` |
| `+0x40` | `void*` | write | next block; null when not set up |
| `+0x48` | `void*` | oldest | oldest block still counted as live |
| `+0x50` | `void*` | last | the block handed out last |

`PreprocessRingBlock` (`0x10` bytes, offsets from the start of the block):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | next | the following block |
| `+0x08` | `u32` | busy | 1 from `0x006B64F0` until the user clears it |
| `+0x0C` | `u32` | size | requested size; a filler holds the bytes to the end |

</details>

## Operations

- `0x0060EC30(instance, value)` writes `value` to `+0x28` of every segment of the mesh at the object's
  `+0x00`. The game's `0x001E5540` calls it for each object in its list at `+0x18`.

## State

<details>
<summary>Show the state it keeps</summary>

| Address | What |
|---|---|
| `0x02E52270` | the `PPreprocessRingBuffer` (guard `0x02E522C8`) |
| `0x02CB6360` | variant usage tree; zero, never written |
| `0x02CE9D9D` | set once the missing-shadow-map error is logged |
| `0x02D3AB18`, `0x02D3AB30`, `0x02D3AB48`, `0x02D3AB78` | the `Vertex`, `Normal`, `ST` and `Color` data types |

</details>

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

- [Shader variant selection](shader-variant-selection.md): the variant key and the light record `0x00606A20` fills.
- [Phyre frame](the-frame.md): the frame's draw routine and camera snapshot.
- [Phyre post-effect classes](phyre-post-effect-classes.md): the post effects that draw through `0x0060B980`.
- [Phyre field schema](phyre-field-schema.md): the `PMeshInstance`, `PLight` and `PShaderParameterDefinition` members.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Movement and pathfinding** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x006C0520`](phyre-mesh-instance-draws.md) | is called by | [`0x00268380`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |

</details>

---

[← Phyre frame](the-frame.md) | [Shader variant selection →](shader-variant-selection.md)
