---
title: "Phyre D3D11 draws, state and buffers: the draw and dispatch calls, topology and index formats, the state translation tables, material parameters and the buffer rings behind data blocks"
kind: "system"
category: "PhyreEngine"
addresses: "0060E7A0, 001B81B0, 0062C9A0, 00671B30, 00674610, 0062EBC0, 01F7F5B8, 006BA720, 00622350, 00622450, 006224E0, 006226D0, 006223D0, 006225D0, 00621F80, 00621FA0, 0061ED00, 0061C1C0, 01F2DEF8, 01F2DEF0, 00616F00, 0061BF40, 0061C010, 0061C150, 00627F10, 00628570, 0062A920, 00618740, 006187A0, 0061C8A0, 02CED880, 01F2DE88, 00608DD0, 0060B860, 0060EC80, 00629AA0, 00629C70, 0061D260, 00623180, 006231F0, 00622F40, 00623050, 00622D90, 0061E340, 0062A0A0, 0061DFE0, 0061DCA0, 0061DD60, 0061DBE0, 0061E0B0, 02CEDA20, 02CEE3D0, 02CEED80, 02CEF730, 00621C00"
---

## What the player sees

Every model, menu and effect on screen reaches the graphics card through the eight functions on
this page. A primitive type the table does not know is skipped without a draw, and a triangle fan
is drawn as a strip, which gives a different shape from a fan with more than three vertices.

## How it works

### The render context

All functions here take PhyreEngine's render context, the static object `005FD050` returns, and
reach Direct3D through two of its fields: the device at `+108`<sub>h</sub> and the immediate device context at
`+110`<sub>h</sub>. Each draw first translates the engine's primitive type, then sets the topology, binds an
index buffer where it needs one and calls the context.

### Draw and dispatch calls

| Function | Arguments after the context | Direct3D call (context slot) |
|---|---|---|
| `00622350` | type, first vertex, vertex count | `Draw` (`+68`<sub>h</sub>); nothing for a count of 0 |
| `00622450` | type, first vertex, vertex count, instance count | `DrawInstanced` (`+A8`<sub>h</sub>); nothing when either count is 0 |
| `006224E0` | type, index count, index block, buffer index | `IASetIndexBuffer` (`+98`<sub>h</sub>), `DrawIndexed` (`+60`<sub>h</sub>) |
| `006226D0` | type, index count, index block, buffer index, instance count | `IASetIndexBuffer`, `DrawIndexedInstanced` (`+A0`<sub>h</sub>) |
| `006223D0` | type, argument buffer | `DrawInstancedIndirect` (`+140`<sub>h</sub>) |
| `006225D0` | type, argument buffer, index block, buffer index | `IASetIndexBuffer`, `DrawIndexedInstancedIndirect` (`+138`<sub>h</sub>) |
| `00621F80` | three group counts | `Dispatch` (`+148`<sub>h</sub>) |
| `00621FA0` | argument buffer | `DispatchIndirect` (`+150`<sub>h</sub>) |

The draws return 1, or 0 when the primitive type has no topology; the two dispatches return 0.
The mesh-segment draw `005FDEA0` shows the choice between them: one branch dispatches one group per
64 elements, rounded up; the others draw non-indexed without an index block and indexed with one. The render-thread executor `0060A410` and `00670790`, `00670810` and `0079B850`
also call them.

### Primitive topology

`0061C1C0` turns the engine's primitive type into a `D3D11_PRIMITIVE_TOPOLOGY`. The last value set
is kept in `01F2DEF8`, and a draw calls the setter in `01F2DEF0` only when the value changes; the
setter is `00616F00`, a jump to the context's `IASetPrimitiveTopology` (`+C0`<sub>h</sub>).

| Engine type | Topology |
|---|---|
| 0, 5 | 1, point list |
| 1 | 2, line list |
| 2 | 4, triangle list |
| 3 | 5, triangle strip |
| 4 | 5, triangle strip; logs `FAN_NOT_SUPPORTED` once (byte `02CF6C3C`) |
| any other | 0: the draw returns 0 |

### Index buffers

The indexed draws take an index data block and the number of the buffer to use. The index format is
`R32_UINT` (`2A`<sub>h</sub>) when the block's type byte `+0C`<sub>h</sub> is 8 and `R16_UINT` (`39`<sub>h</sub>) otherwise; the
offset is the block's `m_offsetInIndexBuffer` (`+68`<sub>h</sub>). The buffer is entry *n* of the block's
array of `48`<sub>h</sub>-byte buffer records at `+18`<sub>h</sub>, used only when bit 0 of `+6C`<sub>h</sub> is set; otherwise a
null buffer is bound.

### Indirect arguments

An argument buffer record keeps a source resource at `+10`<sub>h</sub> and the resource the GPU reads at
`+08`<sub>h</sub>. When its byte `+20`<sub>h</sub> is set, the draw first calls `0061ED00`, which copies `+10`<sub>h</sub> into
`+08`<sub>h</sub> with the context's `CopyResource` (`+178`<sub>h</sub>), and clears the byte.

### Blend and depth-stencil state

The context keeps the pending state descriptions in its own body, with dirty bits in the word
`+9C0`<sub>h</sub>: a `D3D11_DEPTH_STENCIL_DESC` at `+9EC`<sub>h</sub> (bit `4`<sub>h</sub>) and a `D3D11_BLEND_DESC` at `+A20`<sub>h</sub>
(bit `2`<sub>h</sub>). The render-block handlers fill them through three translation tables:

- `00627F10` (opcode `1B`<sub>h</sub>) turns blending on or off, translates the source and destination factors
  with `0061BF40`, and sets the alpha factors to `SRC_ALPHA` and `INV_SRC_ALPHA`.
- `00628570` (opcode `21`<sub>h</sub>) enables depth and stores the compare function from `0061C010`, or
  `ALWAYS` (8) when its flag is clear.
- `0062A920` fills the stencil half: enable, read and write masks, and for both faces three
  `0061C150` operations and a `0061C010` function.

### Material parameters

A material keeps its parameter values in one buffer whose first `u32` is its size. `0018D240(effect
variant, name)` finds a parameter record (`18`<sub>h</sub> bytes) by name; the record's byte `+02`<sub>h</sub> is its type,
`+10`<sub>h</sub> its offset in the buffer and the low 13 bits of `+12`<sub>h</sub> its size. Three setters copy a value
in:

- `0060E7A0(buffer, record, value)` takes any type;
- `0060E5A0` only type `44`<sub>h</sub> and `001B81B0` only types `12`<sub>h</sub>, `16`<sub>h</sub>, `42`<sub>h</sub> and `D9`<sub>h</sub>–`DC`<sub>h</sub>,
  returning 5 for any other.

Each returns 1 for a null value and 3 when the offset is below 4 or the value would run past the
buffer's size. `005FD5F0` returns true for a record of type `12`<sub>h</sub>–`16`<sub>h</sub>, `42`<sub>h</sub>–`44`<sub>h</sub>,
`48`<sub>h</sub>–`4E`<sub>h</sub>, `90`<sub>h</sub>, `91`<sub>h</sub>, `D9`<sub>h</sub>–`DC`<sub>h</sub> or `DE`<sub>h</sub>–`E2`<sub>h</sub>.

`00600120(effectVariant, pool)` creates a material for an effect variant: a `PParameterBuffer`
(class `02CB7480`) of the variant's buffer size (`u16 +60h`), zeroed, with the size in its first
`u32`, the variant at `+08`<sub>h</sub> and its definition array (`+10`<sub>h</sub> count, `+18`<sub>h</sub> data) pointed at the
variant's (`+40`<sub>h</sub>, `+48`<sub>h</sub>) without owning it (`0060EFE0`); then a `PMaterial` (class `02CB6B80`)
holding the variant and that buffer.

`0060DEA0(material, effectVariant, parameterBuffer)` stores
`m_effectVariant` (`+00`<sub>h</sub>) and `m_parameterBuffer` (`+08`<sub>h</sub>). The map-art function `001EE1D0`, which
gives a model instance materials of its own, calls it after copying each parameter's value into the
new buffer.

A shader program's constant buffer is created on first use by `0061F650`: when the record has no
buffer and a non-zero size at `+28`<sub>h</sub> it calls the device's `CreateBuffer` (`+18`<sub>h</sub>) with that size,
default usage and bind flag 4 (constant buffer), passes the name `PShaderProgramConstantBuffer` to
`0061C550`, and sizes a main-memory copy at `+08`<sub>h</sub> (`0067B100`). A failed creation returns 5.

### Bind caches

`006238E0` updates three caches of bound pointers in its object, 8, 128 and 16 slots wide (at
`+490`<sub>h</sub>, `+000`<sub>h</sub> and `+408`<sub>h</sub>), each followed by the function that binds them. `0062C9A0`, `0062CA70` and `0062CB40` update one cache each: they skip
the leading and trailing entries that already match, copy the changed run and call the bind function
for that run only, so an unchanged binding costs no Direct3D call.

### Data blocks and their buffer rings

A vertex data block (`PDataBlockD3D11`, `88`<sub>h</sub> bytes) and an index data block hold a ring of
Direct3D buffers, a `PSharray` of `48`<sub>h</sub>-byte records (vertex blocks `+20`<sub>h</sub>, index blocks `+18`<sub>h</sub>)
with the ring position before it. A record holds the buffer at `+00`<sub>h</sub>, a staging buffer at `+18`<sub>h</sub>,
an in-use count at `+20`<sub>h</sub>, a `TAsyncUpdate` record at `+28`<sub>h</sub> (owner `+30`<sub>h</sub>, ring index `+38`<sub>h</sub>) and
a main-memory copy at `+40`<sub>h</sub>. Bit 0 of `+74`<sub>h</sub> (vertex, `00671B10`) or `+6C`<sub>h</sub> (index, `00671B20`)
marks a bound block.

1. Writing takes the next record of the ring and sleeps 1 ms at a time while its in-use count is
   above 0 (`0067BE10`, `0067BEC0`); `00673780` and `006737F0` wait the same way for every record.
2. Mapping a vertex record (`00671B30`) reads the buffer's description. Without CPU write access it
   creates a staging buffer once and maps it for writing; with it, it hands out the main-memory copy,
   allocated at the buffer's size on first use. An index record (`00671D80`) always uses the copy.
   Either way the caller gets the block's offset into the buffer and its data size.
3. Committing a staged vertex record (`00674610`) unmaps the staging buffer and copies it into the
   buffer with `CopyResource`. A record written through the copy is queued instead: its `TAsyncUpdate`
   record goes into the set for the current frame slot (`0062EB90`; `006747D0` for index blocks).

The queue is the `E0`<sub>h</sub>-byte object at `01F7F5B8`, four `38`<sub>h</sub>-byte sets (`0062EA20`, each set
built by `0062EB20`). The game's `00185A50` posts an opcode `2F`<sub>h</sub> render block (`005FEA50`) whose
function `00186610` jumps to `0062EBC0` on the queue, and then advances the slot `01F7F590` modulo 4.
`0062EBC0` calls slot 0 of every record in one slot's set and empties the set.

`006BA720` gives the bytes per element of a data type code (`0C`<sub>h</sub>, the text index type, is 2):

| Bytes | Codes |
|---|---|
| 1 | `10`<sub>h</sub>, `18`<sub>h</sub>, `24`<sub>h</sub>, `2C`<sub>h</sub> |
| 2 | `04`<sub>h</sub>, `0C`<sub>h</sub>, `11`<sub>h</sub>, `14`<sub>h</sub>, `19`<sub>h</sub>, `20`<sub>h</sub>, `25`<sub>h</sub>, `28`<sub>h</sub>, `2D`<sub>h</sub> |
| 3 | `12`<sub>h</sub>, `1A`<sub>h</sub>, `26`<sub>h</sub>, `2E`<sub>h</sub> |
| 4 | `00`<sub>h</sub>, `05`<sub>h</sub>, `08`<sub>h</sub>, `0D`<sub>h</sub>, `13`<sub>h</sub>, `15`<sub>h</sub>, `1B`<sub>h</sub>, `1C`<sub>h</sub>, `21`<sub>h</sub>, `27`<sub>h</sub>, `29`<sub>h</sub>, `2F`<sub>h</sub>, `32`<sub>h</sub> |
| 6 | `06`<sub>h</sub>, `0E`<sub>h</sub>, `16`<sub>h</sub>, `22`<sub>h</sub>, `2A`<sub>h</sub> |
| 8 | `01`<sub>h</sub>, `07`<sub>h</sub>, `09`<sub>h</sub>, `0F`<sub>h</sub>, `17`<sub>h</sub>, `1D`<sub>h</sub>, `23`<sub>h</sub>, `2B`<sub>h</sub> |
| 12 | `02`<sub>h</sub>, `0A`<sub>h</sub>, `1E`<sub>h</sub> |
| 16 | `03`<sub>h</sub>, `0B`<sub>h</sub>, `1F`<sub>h</sub> |
| 48, 64 | `30`<sub>h</sub>, `31`<sub>h</sub> |
| 0 | any other |

### Unbinding

- `0061C8A0(context, n, buffers, strides, offsets)` binds `n` vertex buffers from slot 0 and binds
  null buffers to the slots from `n` up to the count left by the previous call, kept in `02CED880`.
- `006187A0` unbinds all of those slots and sets the count to 0.
- `00618740` unbinds the compute stage's unordered-access views once (byte `01F2DE88`):
  `CSSetUnorderedAccessViews` (`+220`<sub>h</sub>) from slot 0 with null views, 8 slots, or 1 when the feature
  level at context `+168`<sub>h</sub> is below `B000`<sub>h</sub>. The scene begin `006CA7B0` and `006CA8D0` call it.

### Shader objects

A shader program holds four shaders, vertex, pixel, geometry and compute. Each shader keeps its
bytecode as an array at `+18`<sub>h</sub>/`+20`<sub>h</sub>, a profile word at `+70`<sub>h</sub> and its Direct3D shader, which
is created on first use:

| Function | Shader | Device call | Stored at | Refused profiles |
|---|---|---|---|---|
| `0061DFE0` | vertex | `CreateVertexShader` (`+60`<sub>h</sub>) | `+90`<sub>h</sub> | `vs50` below level `B000`<sub>h</sub>, `vs41` below `A100`<sub>h</sub> |
| `0061DCA0` | pixel | `CreatePixelShader` (`+78`<sub>h</sub>) | `+78`<sub>h</sub> | `ps50`, `ps41` likewise |
| `0061DD60` | geometry | `CreateGeometryShader` (`+68`<sub>h</sub>) | `+78`<sub>h</sub> | `gs50`, `gs41` likewise |
| `0061DBE0` | compute | `CreateComputeShader` (`+90`<sub>h</sub>) | `+78`<sub>h</sub> | `cs50`, `cs41` likewise |

A refused profile only logs `Unable to compile … shader - profile not supported.`; a failed creation
returns 9. Each then creates its constant buffer (`0061F650`), and the vertex shader its input layout
with `0061E0B0`: one `D3D11_INPUT_ELEMENT_DESC` per named input of the `20`<sub>h</sub>-byte input array at
`+78`<sub>h</sub>, taking the semantic index, format and input slot from the input's `+10`<sub>h</sub>, `+14`<sub>h</sub> and
`+18`<sub>h</sub>, offset 0, and per-instance data with step rate 1 when byte `+10`<sub>h</sub> of the input's stream
(`+08`<sub>h</sub>) is set. `CreateInputLayout` (`+58`<sub>h</sub>) stores the layout at `+88`<sub>h</sub>; 9 on failure.

### Switching passes

`00608DD0(tracker, pass)` makes a pass current. The pass names its shader program at `+28`<sub>h</sub> and
four parameter blocks at `+38`<sub>h</sub>–`+50`<sub>h</sub>:

1. With no current pass it takes the new one whole. With the same program it marks only the
   parameter blocks that differ, bits 1, 2, 4 and 8 for blocks 0–3; with another program all four.
2. `0060B860` unbinds the old pass's marked blocks through `00627160`, which hands each stage's
   resource records for that block to `006272C0` to clear their pending slots.
3. When the program changes it also clears the old one (`00627140`) and binds the new one:
   `00629AA0` creates the four shaders as needed and sets each through a one-entry cache
   (`01F2DE98`, `01F2DEA8`, `01F2DEB8`, `01F2DEC8`); `00629C70` builds the program's pass state at
   `+30`<sub>h</sub> (`0061DE20`) and applies it with `0061D260`.
4. `0060EC80` binds the marked blocks of the new pass: `00629970` writes the value parameters
   (`00628B40`) and `00629CD0` the resource parameters (`0062A0A0`), stage by stage; block 3 also
   runs `00629CB0`, which calls `00629E50` when a vertex shader is bound.
5. `00623180` applies the shaders, and the pass becomes current.

To drop the current pass, `005DE1D0` calls `0060B750`, which unbinds all four of its blocks and
clears the program (`00627140`), and then clears the tracker's pass.

`005C5230`, called before each block in step 2 and when the program changes, returns 0 and does
nothing.

`0061D260`
sets the rasterizer state at `+168`<sub>h</sub> (`RSSetState`, `+158`<sub>h</sub>; the one at `+170`<sub>h</sub> instead when the
context's word `+9C4`<sub>h</sub> is 2), the blend state at `+180`<sub>h</sub> with a zero blend factor and mask
`FFFFFFFF`<sub>h</sub> (`+118`<sub>h</sub>) and the depth-stencil state at `+178`<sub>h</sub> with the stencil reference byte at
`+188`<sub>h</sub> (`+120`<sub>h</sub>). `0061D180` applies only the states selected by bits 1, 2 and 4 of its mask, and
`0061D320` all three without the alternative rasterizer state. `00629680(state, value)` stores a
byte at `+20`<sub>h</sub> of a pass state and sets dirty bit 1.

### The stage caches

Each shader stage has a `9B0`<sub>h</sub>-byte cache of what is bound and what is pending (layout below):
vertex `02CEDA20`, pixel `02CEE3D0`, geometry `02CEED80` and compute `02CEF730`, with two more at
`02CF00E0` and `02CF0A90`. A program keeps, per stage and per parameter block, a run of 16-byte
parameter records: start and count as `u16` at `+1C0`<sub>h</sub>/`+1C8`<sub>h</sub> (value parameters) and
`+240`<sub>h</sub>/`+248`<sub>h</sub> (resource parameters), `20`<sub>h</sub> apart per stage, with the record arrays at `+1D8`<sub>h</sub>
and `+258`<sub>h</sub>.

`0062A0A0` reads each resource record's slot (`+04`<sub>h</sub>, −1 skips it) and the parameter at its offset
(`+00`<sub>h</sub>) in the pass's block, and fills the pending arrays by parameter type:

| Type | What it binds | Pending array |
|---|---|---|
| `42`<sub>h</sub>, `43`<sub>h</sub>, `44`<sub>h</sub> | 2D, 3D or cube-map shader view (`00623FA0`, `00623FF0`, `00624040`) | views |
| `47`<sub>h</sub> | a sampler state's object at `+20`<sub>h</sub> | samplers |
| `48`<sub>h</sub>, `4B`<sub>h</sub> | structured-buffer view (`00623F50`) or vertex-block view (`00624690`) | views |
| `49`<sub>h</sub>, `4C`<sub>h</sub> | structured-buffer or vertex-block UAV (`00624180`, `00624730`); `4C`<sub>h</sub> also an indirect-arguments buffer's `+18`<sub>h</sub>, marking it for copy | the shader's UAVs at `+30`<sub>h</sub> |
| `4A`<sub>h</sub> | constant buffer: `006239C0` uploads it, `00623EB0` gives it; slots above 7 are logged | constant buffers |
| `4D`<sub>h</sub>, `4E`<sub>h</sub> | 2D texture UAV (`006241D0`) or `00624220` | the shader's UAVs at `+30`<sub>h</sub> |
| `4F`<sub>h</sub>, `DE`<sub>h</sub>–`E1`<sub>h</sub> | vertex data block view (`00624690`) | views |
| `50`<sub>h</sub>, `E2`<sub>h</sub> | index data block view (`006246E0`) | views |

A texture without a view logs `Texture2D (%p) missing Shader Resource View%s` (or the `Texture3D`
and `Cubemap` forms) once per kind (bytes
`02CF6ABC`–`02CF6ABE`), adding ` - read before use as a render target?` for a render-target texture;
a missing data block logs `Unable to provide a data block for data block shader parameter`. Every
write lowers and raises the array's dirty range.

### Applying the shaders

`00623180` applies the vertex (`006231F0`), geometry (`00623050`), pixel (`00622F40`) and compute
(`00622D90`) shaders that are present. Each:

- uploads the shader's own constant buffer from its copy with `UpdateSubresource` (`+180`<sub>h</sub>) and
  puts it in its stage's pending constant-buffer slot, when the shader has a slot (`+2C`<sub>h</sub> not −1);
- sets the shader through its cache and flushes the stage cache with `006238E0`.

The vertex and geometry paths then unbind the compute UAVs once (`01F2DE88`). The pixel path first
binds the shader's UAVs (`+30`<sub>h</sub>) after the render targets with `0061E340`: up to 8 views from the
slot after the last render target (`+6D0`<sub>h</sub>), through `OMSetRenderTargetsAndUnorderedAccessViews`
(`+110`<sub>h</sub>) with the targets at `+648`<sub>h</sub> and depth view `+688`<sub>h</sub>, skipped when nothing changed. The
compute path empties the shader views of all six caches (`0061E6B0`), unbinds the render targets,
sets the compute UAVs from `+30`<sub>h</sub> (8 slots, 1 below level 11.0) and clears `01F2DE88` and `+6D4`<sub>h</sub>.

### Full-screen quads

`00621C00(context, texture, x0, y0, x1, y1, sampler)` draws a texture as a quad with the object at
context `+7D8`<sub>h</sub>, using the default sampler at `+1820`<sub>h</sub> when none is given.

1. `00629580` copies the context's pending state block (`+9C0`<sub>h</sub>, `190`<sub>h</sub> bytes) into
   that object's pass state, turning depth on with `ALWAYS`.
2. It maps the object's vertex buffer (`00626010`, `WRITE_DISCARD`) and writes six `30`<sub>h</sub>-byte
   vertices: positions as two triangles with `0061C690` (0–1 mapped to −1–1), white colours, and with
   `0061C740` the texture coordinates, V flipped for a render-target texture.
3. It unmaps the buffer and draws six vertices as a triangle list (`006227D0`).

## Layouts

Render context (`005FD050`), fields used here:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `108`<sub>h</sub> | `void*` | ID3D11Device |  |
| `110`<sub>h</sub> | `void*` | ID3D11DeviceContext |  |
| `168`<sub>h</sub> | `u32` | feature level |  |
| `9C0`<sub>h</sub> | `u32` | dirty bits: `2`<sub>h</sub> blend, `4`<sub>h</sub> depth-stencil |  |
| `9EC`<sub>h</sub> | `D3D11_DEPTH_STENCIL_DESC` | pending depth-stencil state |  |
| `A20`<sub>h</sub> | `D3D11_BLEND_DESC` | pending blend state |  |

`D3D11_DEPTH_STENCIL_DESC` (`34`<sub>h</sub> bytes, offsets from the start of the context+`9EC`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `08`<sub>h</sub> | `u32` | DepthFunc | compare function (context +`9F4`<sub>h</sub>) |
| `0C`<sub>h</sub> | `u32` | StencilEnable | (context +`9F8`<sub>h</sub>) |
| `14`<sub>h</sub> | `u32[4]` | FrontFace | fail, depth-fail and pass operations, function (context +`A00`<sub>h</sub>) |
| `24`<sub>h</sub> | `u32[4]` | BackFace | the same for back faces (context +`A10`<sub>h</sub>) |

`D3D11_BLEND_DESC` (`108`<sub>h</sub> bytes, offsets from the start of the context+`A20`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `08`<sub>h</sub> | `u32` | BlendEnable | render target 0 (context +`A28`<sub>h</sub>) |
| `0C`<sub>h</sub> | `u32` | SrcBlend | (context +`A2C`<sub>h</sub>) |
| `10`<sub>h</sub> | `u32` | DestBlend | (context +`A30`<sub>h</sub>) |
| `18`<sub>h</sub> | `u32` | SrcBlendAlpha | (context +`A38`<sub>h</sub>) |
| `1C`<sub>h</sub> | `u32` | DestBlendAlpha | (context +`A3C`<sub>h</sub>) |

Index data block, fields used here:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0C`<sub>h</sub> | `u8` | index type: 8 = 32-bit |  |
| `18`<sub>h</sub> | `PSharray` | of | `48`<sub>h</sub>-byte buffer records; +`00`<sub>h</sub> of a record is the ID3D11Buffer |
| `68`<sub>h</sub> | `u32` | m_offsetInIndexBuffer |  |
| `6C`<sub>h</sub> | `u32` | bit 0: buffers bound |  |

`StageCache` (`9B0`<sub>h</sub> bytes, offsets from the start of the 02CEDA20):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `void*[128]` | boundViews | shader-resource views as bound |
| `400`<sub>h</sub> | `void*` | bindViews | binds a run of views |
| `408`<sub>h</sub> | `void*[16]` | boundSamplers | samplers as bound |
| `488`<sub>h</sub> | `void*` | bindSamplers |  |
| `490`<sub>h</sub> | `void*[8]` | boundConstantBuffers | constant buffers as bound |
| `4D0`<sub>h</sub> | `void*` | bindConstantBuffers |  |
| `4D8`<sub>h</sub> | `void*[128]` | views | pending views |
| `8D8`<sub>h</sub> | `i32` | viewsLow | lowest changed slot; `80`<sub>h</sub> when clean |
| `8DC`<sub>h</sub> | `i32` | viewsHigh | highest changed slot |
| `8E0`<sub>h</sub> | `void*[16]` | samplers | pending samplers |
| `960`<sub>h</sub> | `i32` | samplersLow | `10`<sub>h</sub> when clean |
| `964`<sub>h</sub> | `i32` | samplersHigh |  |
| `968`<sub>h</sub> | `void*[8]` | constantBuffers | pending constant buffers |
| `9A8`<sub>h</sub> | `i32` | constantBuffersLow | 8 when clean |
| `9AC`<sub>h</sub> | `i32` | constantBuffersHigh |  |

`ShaderPassState` (`190`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u32` | dirty | the same block as context +`9C0`<sub>h</sub> |
| `168`<sub>h</sub> | `void*` | rasterizer | RSSetState |
| `170`<sub>h</sub> | `void*` | rasterizerAlt | used when context +`9C4`<sub>h</sub> is 2 |
| `178`<sub>h</sub> | `void*` | depthStencil | OMSetDepthStencilState |
| `180`<sub>h</sub> | `void*` | blend | OMSetBlendState |
| `188`<sub>h</sub> | `u8` | stencilRef |  |

Blend factors (`0061BF40`), engine value to `D3D11_BLEND`:

| Engine | D3D11 | Engine | D3D11 |
|---|---|---|---|
| 0 | 1 `ZERO` | 9 | 8 `INV_DEST_ALPHA` |
| 1, 12, 13, others | 2 `ONE` | 10 | 14 `BLEND_FACTOR` |
| 2 | 3 `SRC_COLOR` | 11 | 15 `INV_BLEND_FACTOR` |
| 3 | 4 `INV_SRC_COLOR` | 14 | 11 `SRC_ALPHA_SAT` |
| 4 | 9 `DEST_COLOR` | 15 | 16 `SRC1_COLOR` |
| 5 | 10 `INV_DEST_COLOR` | 16 | 17 `INV_SRC1_COLOR` |
| 6 | 5 `SRC_ALPHA` | 17 | 18 `SRC1_ALPHA` |
| 7 | 6 `INV_SRC_ALPHA` | 18 | 19 `INV_SRC1_ALPHA` |
| 8 | 7 `DEST_ALPHA` | | |

Compare functions (`0061C010`) and stencil operations (`0061C150`):

| Engine | `D3D11_COMPARISON_FUNC` | `D3D11_STENCIL_OP` |
|---|---|---|
| 0 | 1 `NEVER` | 1 `KEEP` |
| 1 | 2 `LESS` | 2 `ZERO` |
| 2 | 4 `LESS_EQUAL` | 3 `REPLACE` |
| 3 | 3 `EQUAL` | 4 `INCR_SAT` |
| 4 | 5 `GREATER` | 5 `DECR_SAT` |
| 5 | 6 `NOT_EQUAL` | 7 `INCR` |
| 6 | 7 `GREATER_EQUAL` | 8 `DECR` |
| 7 | 8 `ALWAYS` | 6 `INVERT` |
| other | 8 `ALWAYS` | 1 `KEEP` |

## State

| Address | What |
|---|---|
| `01F2DEF8` | last primitive topology set |
| `01F2DEF0` | topology setter, `00616F00` |
| `02CED880` | number of vertex-buffer slots bound by `0061C8A0` |
| `02CED890`, `02CED990` | zeroed arrays passed when unbinding |
| `01F2DE88` | set once the unordered-access views are unbound |
| `02CF6C3C` | set once the fan warning is logged |
| `02CEDA20`, `02CEE3D0`, `02CEED80`, `02CEF730` | vertex, pixel, geometry and compute stage caches |
| `02CF00E0`, `02CF0A90` | the two further stage caches, emptied by the compute path |
| `01F2DE98`, `01F2DEA8`, `01F2DEB8`, `01F2DEC8` | the shader last set on each of the four stages |
| `02CF6ABC`–`02CF6ABE` | set once a missing 2D, 3D or cube-map view is logged |

## Modding notes

- Engine primitive type 4 is drawn as a triangle strip, so fan geometry needs converting to lists
  or strips before it reaches the engine.
- The topology cache `01F2DEF8` assumes nothing else sets the topology. Code that calls
  `IASetPrimitiveTopology` directly should store its value there too, or the next draw with the old
  value skips the call.
- An index block's type byte decides the index width for every draw that uses it; any value other
  than 8 is read as 16-bit.
- A shader's constant buffer may only use slots 0-7; a resource parameter with a higher constant-buffer
  slot is logged and not bound.

## Related

- [Render commands](../Graphics/gi-render-commands.md): the render thread and the
  render-block opcodes whose handlers end in these calls.
- [Shader variant selection](shader-variant-selection.md): the context switches applied before a draw.
- [Phyre frame](the-frame.md): the draw routine of a frame.
- [Phyre D3D11 device and resources](phyre-d3d11-device-and-resources.md): the device, texture formats, textures and buffers these calls bind.
