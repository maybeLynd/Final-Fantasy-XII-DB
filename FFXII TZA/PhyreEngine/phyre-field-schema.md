[Home](../../README.md) / [PhyreEngine](README.md) / Phyre field schema

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Phyre field schema: the class and member tables in every .phyre file and how the loader matches them to registered members | format | PhyreEngine | Asset files and animation | The packed namespace each .phyre file carries after its 84-byte header: the type table, the nine-word class records and six-word member records with their names, file offsets, widths and attribute words; how the loader checks it, finds each class and member by name in the run-time reflection data, reports differences and picks a copy routine per member; and the shipped figures, in which every class and member a file declares is registered by the executable. | 0x0059E070, 0x0059A3B0, 0x0059B430, 0x0059BA40, 0x0059D2D0, 0x0059AC00, 0x006393A0, 0x00632B30, 0x00632E80, 0x0063BA10, 0x00597220, 0x00632960, 0x00632A10, 0x00632A70, 0x00632BE0, 0x0062EFD0, 0x00633100, 0x006318A0, 0x00631C40, 0x00599390, 0x00595E70, 0x0059A030, 0x0016D6A0, 0x005CDAA0 |

## What the player sees

Nothing directly. Each model, texture, shader and scene file states which classes and fields its
data was written with, and the game lines that list up with the fields the executable registers
before it copies any data. Because the shipped files and the executable agree on every class and
field name, every asset loads through the plain path.

## Where it comes from

Every `.phyre` file starts with a cluster header whose marker is `RYHP` and whose size `m_size` is
84 in every shipped file; the packed namespace follows at byte 84 and is `m_packedNamespaceSize`
bytes long. `0x0059E070` reads the header through `0x0059A3B0`, then the namespace; `0x0059A3B0` reads both,
the namespace through `0x0059A6F0` (`0x0059A5BF`, `0x0059A5D7`), and `0x0059E070` reads neither itself.

The other half is the executable's own registrations: every reflected member is registered by one
of four constructors (`0x00632960` plain, `0x00632A10` array, `0x00632A70` fixed-size array, `0x00632BE0`
enum), each passing the class descriptor, the member's type, name, byte offset and attribute word.

## Layouts

All multi-byte fields are little-endian.

Packed namespace (at m_size):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | `0x01020304`, byte-order mark |
| `+0x04` | `u32` |  | namespace size (equals m_packedNamespaceSize) |
| `+0x08` | `u32` | nTypes |  |
| `+0x0C` | `u32` | nClasses |  |
| `+0x10` | `u32` | nMembers |  |
| `+0x14` | `u32` | stringPoolSize |  |
| `+0x18` | `u8[4]` |  | 0 in every shipped file; read by no function on a shipped file: the validator `0x0059E070` sums `+0x08`, `+0x0C`, `+0x10`, `+0x14` and `+0x1C` against `+0x04` (`0x0059E173`-`0x0059E191`) and reads nothing else of the header, the binders take the counts and the records, and the byte swap `0x0059C180` (`0x0059C1B7`-`0x0059C1BC`) runs only when `0x0059A3B0` finds the cluster marker byte-reversed (`0x0059A3FF`-`0x0059A437`), which no shipped file is; nothing fixes its width |
| `+0x1C` | `u32` |  | size of an optional block, 0 in every shipped file |
| `+0x20` | `u32` |  | string-pool offset of each type name [nTypes] ...  class records, 9 u32 each [nClasses] ...  member records, 6 u32 each [nMembers] ...  NUL-separated string pool [stringPoolSize] |

```
class record (9 u32)
w0  parent: 1-based index of the parent class record, 0 for no parent
w1  top 4 bits (mask 0xF0000000) a value 0..4; low 28 bits the size of one record of the class in the file layout
w2  name, string-pool offset
w3  number of member records that follow for this class
w4  0
w5  0
w6  0
w7  flags; bit 0x1 asks for a dynamic class when no registered class matches
w8  0
```

Members are stored in class order: class *i* owns the next `w3` member records, and the sum of
`w3` over the classes is `nMembers` in every shipped file.

```
member record (6 u32)
w0  name, string-pool offset
w1  type: a type-table index when below nTypes, else nTypes + 1-based class index
w2  offset in the file layout of the class
w3  width in the file layout (one element for a fixed-size array)
w4  attribute word; bit 0x80000000 marks a counted buffer (PArray<T>::m_els, PSharray<T>::m_u, PString::m_buffer)
w5  element count of a fixed-size array, otherwise 0
```

The attribute word in `w4`, with bit `0x80000000` masked off, is the run-time member's attribute word: bit
`0x2` a pointer, `0x4` a dynamic-type helper, `0x20` an enum, `0x40` an inline counted buffer, and
the per-class bits `0x08` and `0x10`.

Every name (a type-table entry, class `w2`, member `w0`) is an offset from the start of the string pool, the
namespace's last `stringPoolSize` bytes.

```python
registration call (0x00632960), Win64 arguments
rcx         record
rdx         class descriptor
r8          type (a PType or class descriptor)
r9          member name
[rsp+0x20]  byte offset in the run-time layout
[rsp+0x28]  attribute word
[rsp+0x30]  0 at every static site
[rsp+0x38]  context passed to the attach slot
```

`0x00632A10` adds the array kind and the element type's alignment as arguments 7 and 8, `0x00632A70` the element count
as argument 7, and `0x00632BE0` ORs `0x20` into the attribute word. A registering function may OR
`0x08`, `0x10` or `0x40` into the record afterwards, and `0x00633100` adds `0x4`.

### File layout against run-time layout

The file offset is not the run-time offset. Of the 527 class and member pairs shipped files declare,
250 have the same offset in both; of the 154 classes with members, 41 have every member at its
run-time offset, for example `PClusterHeaderBase`, whose 18 fields sit at 0 to 68 in both. The other
113 are packed: in `PAssetReference`, `m_id`, `m_asset` and `m_assetType` sit at file offsets 0, 1
and 2 with width 1, against run-time offsets inside a `0x50`-byte object. An object pointer has
width 1 and a `PArray` member width 5 in a packed class.

So no instance is used in place. `0x0059E300` reads the instances, and each file member is copied from its file
offset to its run-time member's offset by the routine `0x0059D2D0` chose, or skipped
([choosing a copy routine](#choosing-a-copy-routine)); the objects in memory have the run-time layout.

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960, or 0x00632A10 for an array, 0x00632A70 for a fixed-size array and 0x00632BE0 for an enum), and each class fence covers only those members.

`CD3D11_BLEND_DESC` (`0x108` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | AlphaToCoverageEnable | D3D11_BLEND_DESC AlphaToCoverageEnable of a pass state's m_blendDesc, which the pass-state builder `0x0061DE20` passes to ID3D11Device::CreateBlendState (slot `+0xA0`, `0x0061DF2F`); AlphaToCoverageEnable (i32), registered by `0x00613800` (`0x00632960` at `0x00613902`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_BLEND_DESC |
| `+0x04` | `i32` | IndependentBlendEnable | D3D11_BLEND_DESC IndependentBlendEnable of a pass state's m_blendDesc, passed to CreateBlendState by `0x0061DE20` (`0x0061DF2F`); IndependentBlendEnable (i32), registered by `0x00613800` (`0x00632960` at `0x00613971`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_BLEND_DESC |
| `+0x08` | `byte[256]` | RenderTarget | eight D3D11_RENDER_TARGET_BLEND_DESC records of `0x20` bytes, one per render target; RenderTarget (D3D11_RENDER_TARGET_BLEND_DESC[8], a fixed-size array), registered by `0x00613800` (`0x00632A70` at `0x006139DB`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_BLEND_DESC |

`CD3D11_DEPTH_STENCIL_DESC` (`0x34` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | DepthEnable | D3D11_DEPTH_STENCIL_DESC DepthEnable of a pass state's m_depthDesc, which `0x0061DE20` passes to ID3D11Device::CreateDepthStencilState (slot `+0xA8`, `0x0061DF88`); DepthEnable (i32), registered by `0x00613A30` (`0x00632960` at `0x00613B32`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_DEPTH_STENCIL_DESC |
| `+0x0C` | `i32` | StencilEnable | D3D11_DEPTH_STENCIL_DESC StencilEnable, passed to CreateDepthStencilState by `0x0061DE20` (`0x0061DF88`); StencilEnable (i32), registered by `0x00613A30` (`0x00632960` at `0x00613C7D`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_DEPTH_STENCIL_DESC |
| `+0x10` | `u8` | StencilReadMask | D3D11_DEPTH_STENCIL_DESC StencilReadMask, passed to CreateDepthStencilState by `0x0061DE20` (`0x0061DF88`); StencilReadMask (u8), registered by `0x00613A30` (`0x00632960` at `0x00613CEC`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_DEPTH_STENCIL_DESC |
| `+0x11` | `u8` | StencilWriteMask | D3D11_DEPTH_STENCIL_DESC StencilWriteMask, passed to CreateDepthStencilState by `0x0061DE20` (`0x0061DF88`); StencilWriteMask (u8), registered by `0x00613A30` (`0x00632960` at `0x00613D5B`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_DEPTH_STENCIL_DESC |
| `+0x12` | `u8[2]` | pad12 | alignment bytes after StencilWriteMask (u8 at `+0x11`) up to FrontFace at `+0x14`; no registered member covers it (`0x00613A30` registers the `0x34`-byte class at `0x00613AAA`) |
| `+0x14` | `u32[4]` | FrontFace | D3D11_DEPTH_STENCIL_DESC FrontFace: the stencil fail, depth-fail and pass operations and the stencil function for front faces, passed to CreateDepthStencilState by `0x0061DE20` (`0x0061DF88`); FrontFace (u32[4]), registered by `0x00613A30` (`0x00632960` at `0x00613DCA`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_DEPTH_STENCIL_DESC |
| `+0x24` | `u32[4]` | BackFace | D3D11_DEPTH_STENCIL_DESC BackFace: the same four values for back faces, passed to CreateDepthStencilState by `0x0061DE20` (`0x0061DF88`); BackFace (u32[4]), registered by `0x00613A30` (`0x00632960` at `0x00613E39`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_DEPTH_STENCIL_DESC |

`CD3D11_RASTERIZER_DESC` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `i32` | FrontCounterClockwise | D3D11_RASTERIZER_DESC FrontCounterClockwise of a pass state's m_rasterDesc, which `0x0061DE20` passes to ID3D11Device::CreateRasterizerState (slot `+0xB0`, `0x0061DE70`) and again in a copy with FillMode 2, wireframe (`0x0061DEB6`, `0x0061DEE9`); FrontCounterClockwise (i32), registered by `0x00613E80` (`0x00632960` at `0x0061405E`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_RASTERIZER_DESC |
| `+0x0C` | `i32` | DepthBias | D3D11_RASTERIZER_DESC DepthBias, passed to CreateRasterizerState by `0x0061DE20` (`0x0061DE70`, `0x0061DEE9`); DepthBias (i32), registered by `0x00613E80` (`0x00632960` at `0x006140CD`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_RASTERIZER_DESC |
| `+0x10` | `f32` | DepthBiasClamp | D3D11_RASTERIZER_DESC DepthBiasClamp, passed to CreateRasterizerState by `0x0061DE20` (`0x0061DE70`, `0x0061DEE9`); DepthBiasClamp (f32), registered by `0x00613E80` (`0x00632960` at `0x0061413C`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_RASTERIZER_DESC |
| `+0x14` | `f32` | SlopeScaledDepthBias | D3D11_RASTERIZER_DESC SlopeScaledDepthBias, passed to CreateRasterizerState by `0x0061DE20` (`0x0061DE70`, `0x0061DEE9`); SlopeScaledDepthBias (f32), registered by `0x00613E80` (`0x00632960` at `0x006141AB`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_RASTERIZER_DESC |
| `+0x18` | `i32` | DepthClipEnable | D3D11_RASTERIZER_DESC DepthClipEnable, passed to CreateRasterizerState by `0x0061DE20` (`0x0061DE70`, `0x0061DEE9`); DepthClipEnable (i32), registered by `0x00613E80` (`0x00632960` at `0x0061421A`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_RASTERIZER_DESC |
| `+0x1C` | `i32` | ScissorEnable | D3D11_RASTERIZER_DESC ScissorEnable, passed to CreateRasterizerState by `0x0061DE20` (`0x0061DE70`, `0x0061DEE9`); ScissorEnable (i32), registered by `0x00613E80` (`0x00632960` at `0x00614289`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_RASTERIZER_DESC |
| `+0x20` | `i32` | MultisampleEnable | D3D11_RASTERIZER_DESC MultisampleEnable, passed to CreateRasterizerState by `0x0061DE20` (`0x0061DE70`, `0x0061DEE9`); MultisampleEnable (i32), registered by `0x00613E80` (`0x00632960` at `0x006142F8`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_RASTERIZER_DESC |
| `+0x24` | `i32` | AntialiasedLineEnable | D3D11_RASTERIZER_DESC AntialiasedLineEnable, passed to CreateRasterizerState by `0x0061DE20` (`0x0061DE70`, `0x0061DEE9`); AntialiasedLineEnable (i32), registered by `0x00613E80` (`0x00632960` at `0x00614367`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare CD3D11_RASTERIZER_DESC |

`D3D11_RENDER_TARGET_BLEND_DESC` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | BlendEnable | D3D11_RENDER_TARGET_BLEND_DESC BlendEnable of one of the eight RenderTarget entries of a CD3D11_BLEND_DESC, passed to CreateBlendState by `0x0061DE20` (`0x0061DF2F`); BlendEnable (i32), registered by `0x00614640` (`0x00632960` at `0x00614742`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare D3D11_RENDER_TARGET_BLEND_DESC |
| `+0x1C` | `u8` | RenderTargetWriteMask | D3D11_RENDER_TARGET_BLEND_DESC RenderTargetWriteMask, passed to CreateBlendState by `0x0061DE20` (`0x0061DF2F`); RenderTargetWriteMask (u8), registered by `0x00614640` (`0x00632960` at `0x00614A45`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare D3D11_RENDER_TARGET_BLEND_DESC |
| `+0x1D` | `u8[3]` | pad1D | the bytes after RenderTargetWriteMask (u8 at `+0x1C`) up to the `0x20`-byte stride of the RenderTarget array (eight entries from `+0x08` of the `0x108`-byte CD3D11_BLEND_DESC); no registered member covers it (`0x00614640` registers the `0x20`-byte class at `0x006146BA`) |

`PAnimationClipBindingChannelMap` (`0x4` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | m_destSlotArrayIndex | m_destSlotArrayIndex (i16), registered by `0x005B0930` (`0x00632960` at `0x005B09C5`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClipBindingChannelMap |
| `+0x02` | `u16` | m_interp | m_interp (u16), registered by `0x005B0930` (`0x00632960` at `0x005B0A38`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClipBindingChannelMap |

`PAnimationDataSourceListEntry` (`0x98` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u32` | m_inputCount | m_inputCount (u32), registered by `0x005B0E70` (`0x00632960` at `0x005B0F70`); no shipped .phyre file declares PAnimationDataSourceListEntry |
| `+0x0C` | `u32[32]` | m_inputIndex | m_inputIndex (u32[32], a fixed-size array), registered by `0x005B0E70` (`0x00632A70` at `0x005B0FDE`); no shipped .phyre file declares PAnimationDataSourceListEntry |
| `+0x8C` | `u32` | m_destSlotArray | m_destSlotArray (u32), registered by `0x005B0E70` (`0x00632960` at `0x005B1058`); no shipped .phyre file declares PAnimationDataSourceListEntry |
| `+0x90` | `u32` | m_persistentBufferOffset | m_persistentBufferOffset (u32), registered by `0x005B0E70` (`0x00632960` at `0x005B10CB`); no shipped .phyre file declares PAnimationDataSourceListEntry |
| `+0x94` | `u32` | m_preprocessBufferOffset | m_preprocessBufferOffset (u32), registered by `0x005B0E70` (`0x00632960` at `0x005B113E`); no shipped .phyre file declares PAnimationDataSourceListEntry |

`PAnimationEvent` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | m_time | m_time (f32), registered by `0x005B1180` (`0x00632960` at `0x005B120E`); no shipped .phyre file declares PAnimationEvent |
| `+0x04` | `u32` | m_id | m_id (u32), registered by `0x005B1180` (`0x00632960` at `0x005B1281`); no shipped .phyre file declares PAnimationEvent |

`PAnimationSlotFilterDeferredLoad` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | m_nodeName | m_nodeName (ptr), registered by `0x005B1F90` (`0x00632960` at `0x005B2090`); no shipped .phyre file declares PAnimationSlotFilterDeferredLoad |

`PContextVariantFoldingTable` (`0x14` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_contextVariantIndex | m_contextVariantIndex (u32), registered by `0x005E3C30` (`0x00632960` at `0x005E3CBA`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PContextVariantFoldingTable |
| `+0x04` | `u32` | m_contextVariantVpIndex | m_contextVariantVpIndex (u32), registered by `0x005E3C30` (`0x00632960` at `0x005E3D29`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PContextVariantFoldingTable |
| `+0x08` | `u32` | m_contextVariantFpIndex | m_contextVariantFpIndex (u32), registered by `0x005E3C30` (`0x00632960` at `0x005E3D98`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PContextVariantFoldingTable |
| `+0x0C` | `u32` | m_contextVariantGsIndex | m_contextVariantGsIndex (u32), registered by `0x005E3C30` (`0x00632960` at `0x005E3E07`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PContextVariantFoldingTable |
| `+0x10` | `u32` | m_contextVariantCsIndex | m_contextVariantCsIndex (u32), registered by `0x005E3C30` (`0x00632960` at `0x005E3E76`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PContextVariantFoldingTable |

`PDynamicDataBlock` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_stride | m_stride (u32), registered by `0x00665A40` (`0x00632960` at `0x00665ACE`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PDynamicDataBlock |
| `+0x04` | `u32` | m_elementCount | m_elementCount (u32), registered by `0x00665A40` (`0x00632960` at `0x00665B41`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PDynamicDataBlock |

`PDynamicSegmentDesc` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_startStreamIndex | m_startStreamIndex (u32), registered by `0x00665EB0` (`0x00632960` at `0x00665F3E`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDynamicSegmentDesc |
| `+0x04` | `u32` | m_streamCount | m_streamCount (u32), registered by `0x00665EB0` (`0x00632960` at `0x00665FB1`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDynamicSegmentDesc |
| `+0x08` | `u32` | m_elementCount | m_elementCount (u32), registered by `0x00665EB0` (`0x00632960` at `0x00666024`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDynamicSegmentDesc |
| `+0x0C` | `i32` | m_indexCount | m_indexCount (i32), registered by `0x00665EB0` (`0x00632960` at `0x00666097`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDynamicSegmentDesc |

`PMeshInstanceAttachPoint` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `u32` | m_sourceMatrixIndex | m_sourceMatrixIndex (u32), registered by `0x005E6400` (`0x00632960` at `0x005E656E`); no shipped .phyre file declares PMeshInstanceAttachPoint |
| `+0x14` | `u8[4]` | bytes14 | the bytes after m_sourceMatrixIndex (`+0x10`) up to the end of the `0x18`-byte class; no registered member covers it (`0x005D9730` registers the `0x18`-byte class at `0x005D9780`) |

`PModifierAndInputs` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u32` | m_persistentStateOffset | m_persistentStateOffset (u32), registered by `0x006D0D50` (`0x00632960` at `0x006D0E51`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierAndInputs |
| `+0x0C` | `u32` | m_stateBlockOffset | m_stateBlockOffset (u32), registered by `0x006D0D50` (`0x00632960` at `0x006D0EC4`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierAndInputs |

`PModifierNetworkBuffer` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u32` | m_modifier | m_modifier (u32), registered by `0x006D1580` (`0x00632960` at `0x006D1681`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkBuffer |
| `+0x0C` | `u32` | m_stream | m_stream (u32), registered by `0x006D1580` (`0x00632960` at `0x006D16F4`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkBuffer |
| `+0x10` | `u32` | m_elementSize | m_elementSize (u32), registered by `0x006D1580` (`0x00632960` at `0x006D1767`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkBuffer |
| `+0x14` | `u32` | m_info | m_info (u32), registered by `0x006D1580` (`0x00632960` at `0x006D17DA`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkBuffer |

`PModifierNetworkInfoPacket_Buffer` (`0x2` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | m_elementSize | m_elementSize (u16), registered by `0x006D1C70` (`0x00632960` at `0x006D1CFC`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket_Buffer |

`PModifierNetworkInfoPacket_ModifierCode` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u32` | m_inputCount | m_inputCount (u32), registered by `0x006D1D30` (`0x00632960` at `0x006D1E38`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket_ModifierCode |
| `+0x0C` | `u32` | m_outputCount | m_outputCount (u32), registered by `0x006D1D30` (`0x00632960` at `0x006D1EAB`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket_ModifierCode |

`PModifierNetworkInfoPacket_ModifierInstance` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_persistentStateOffset | m_persistentStateOffset (u32), registered by `0x006D1EE0` (`0x00632960` at `0x006D1F75`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket_ModifierInstance |
| `+0x04` | `u32` | m_stateBlockOffset | m_stateBlockOffset (u32), registered by `0x006D1EE0` (`0x00632960` at `0x006D1FE8`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket_ModifierInstance |
| `+0x08` | `u8` | m_codeIndex | m_codeIndex (u8), registered by `0x006D1EE0` (`0x00632960` at `0x006D205B`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket_ModifierInstance |
| `+0x09` | `u8[23]` | m_inputOutputIndices | m_inputOutputIndices (u8[23], a fixed-size array), registered by `0x006D1EE0` (`0x00632A70` at `0x006D20C9`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket_ModifierInstance |

`PModifierNetworkInstancePacketInput` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_source | m_source (u32), registered by `0x006C36C0` (`0x00632960` at `0x006C374E`); no shipped .phyre file declares PModifierNetworkInstancePacketInput |
| `+0x04` | `u32` | m_list | m_list (u32), registered by `0x006C36C0` (`0x00632960` at `0x006C37C1`); no shipped .phyre file declares PModifierNetworkInstancePacketInput |

`POctreeData` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `f32[4]` | m_cachedPosition | m_cachedPosition (f32[4]), registered by `0x008786F0` (`0x00632960` at `0x008787F0`); no shipped .phyre file declares POctreeData |
| `+0x30` | `u8[8]` | bytes30 | the bytes after m_prev (`+0x28`) up to the end of the `0x38`-byte class; no registered member covers it (`0x00877D40` registers the `0x38`-byte class at `0x00877D90`) |

`PParameterBufferBase` (`0x4` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_parameterBufferSize | m_parameterBufferSize (u32), registered by `0x005E6E70` (`0x00632960` at `0x005E6EF8`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PParameterBufferBase |

`PPhysicsBoxBase` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x70` | `f32[4]` | m_halfExtents | the box's half extents; m_halfExtents (f32[4]), registered by `0x00693EC0` (`0x00632960` at `0x00693F49`); no shipped .phyre file declares PPhysicsBoxBase; the placement constructor `0x0068D190`, which stores the class vtable `0x00D79880` (`0x0068D199`), sets it to (1, 1, 1) (`0x0068D1FB`-`0x0068D209`); PPhysicsBoxBullet's build `0x0069F770`, slot 0 of its vtable `0x00D798A8`, reads it (`0x0069F7BF`-`0x0069F7CA`) into a `0x50`-byte Bullet btBoxShape (vtable `0x00D7A838` stored at `0x0069F7DE`, shape type 0 at `0x0069F7E1`) and keeps the shape at `+0x80` (`0x0069F834`); its slot `+0x08`, `0x006A0540`, runs that build (`0x006A0565`) and adds the shape to the rigid body's compound shape `+0x120` through `0x00832590` (`0x006A05D0`) |

`PPhysicsCallbackData` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x20` | `f32` | m_amount | m_amount (f32), registered by `0x00693F80` (`0x00632960` at `0x006940E6`); no shipped .phyre file declares PPhysicsCallbackData |
| `+0x24` | `u8[4]` | bytes24 | the bytes after m_amount (`+0x20`) up to the end of the `0x28`-byte class; no registered member covers it (`0x0068F430` registers the `0x28`-byte class at `0x0068F480`) |

`PPhysicsCharacterControllerBase` (`0x130` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x018` | `f32[4]` | m_scale | m_scale (f32[4]), registered by `0x006949A0` (`0x00632960` at `0x00694F99`); no shipped .phyre file declares PPhysicsCharacterControllerBase; the constructor `0x00690FC0` sets it to (1, 1, 1) (`0x00690FD5`-`0x00690FE3`) |
| `+0x028` | `f32[4]` | m_gravity | m_gravity (f32[4]), registered by `0x006949A0` (`0x00632960` at `0x00694A3C`); no shipped .phyre file declares PPhysicsCharacterControllerBase; the constructor `0x00690FC0` sets it to (0, -19.6, 0) (`0x00690FEA`-`0x00690FF4`) |
| `+0x044` | `u8[4]` | bytes44 | the bytes at `+0x44`, after `+0x40` and before `+0x48`; no registered member covers it (`0x0068F810` registers the `0x130`-byte class at `0x0068F860`) |
| `+0x0E0` | `f32` | m_rotate | m_rotate (f32), registered by `0x006949A0` (`0x00632960` at `0x00694B93`); no shipped .phyre file declares PPhysicsCharacterControllerBase; the constructor `0x00690FC0` clears it with m_right (qword store `0x0069109F`) |
| `+0x0E4` | `f32` | m_right | m_right (f32), registered by `0x006949A0` (`0x00632960` at `0x00694C06`); no shipped .phyre file declares PPhysicsCharacterControllerBase; the constructor `0x00690FC0` clears it with m_rotate (`0x0069109F`) |
| `+0x0E8` | `f32` | m_forward | m_forward (f32), registered by `0x006949A0` (`0x00632960` at `0x00694C79`); no shipped .phyre file declares PPhysicsCharacterControllerBase; the constructor `0x00690FC0` clears it (`0x006910A6`) |
| `+0x104` | `u8` | m_jump | m_jump (u8), registered by `0x006949A0` (`0x00632960` at `0x00694D5F`); no shipped .phyre file declares PPhysicsCharacterControllerBase; the constructor `0x00690FC0` clears it with m_isOnGround (word store `0x006910E8`) |
| `+0x105` | `u8` | m_isOnGround | whether the character stands on the ground; m_isOnGround (u8), registered by `0x006949A0` (`0x00632960` at `0x00694DD2`); no shipped .phyre file declares PPhysicsCharacterControllerBase; the script method getIsOnGround (registered at `0x006953E2`) returns it through `0x006A3A90`; the constructor `0x00690FC0` clears it (`0x006910E8`) |
| `+0x107` | `u8[1]` | pad107 | the byte after `+0x106`, before `+0x108`; no registered member covers it (`0x0068F810` registers the `0x130`-byte class at `0x0068F860`) |

`PPhysicsMaterial` (`0xC` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | m_dynamicFriction | m_dynamicFriction (f32), registered by `0x006955D0` (`0x00632960` at `0x0069565E`); no shipped .phyre file declares PPhysicsMaterial; the placement constructor `0x0068E4C0` clears it with m_staticFriction (qword store `0x0068E4C7`) |
| `+0x04` | `f32` | m_staticFriction | the friction a rigid body is built with; m_staticFriction (f32), registered by `0x006955D0` (`0x00632960` at `0x006956D1`); no shipped .phyre file declares PPhysicsMaterial; the placement constructor `0x0068E4C0` clears it (`0x0068E4C7`); the rigid-body build `0x0069FB10` takes the body's material m_material `+0x98` (`0x006A0111`), or else that of the first child shape whose m_material `+0x18` is set (`0x006A0133`-`0x006A0167`), returns 9 with neither (`0x006A0169`), and copies this member into the Bullet construction info as the body's friction (`0x006A017D`-`0x006A0182`) |
| `+0x08` | `f32` | m_restitution | the restitution a rigid body is built with; m_restitution (f32), registered by `0x006955D0` (`0x00632960` at `0x00695744`); no shipped .phyre file declares PPhysicsMaterial; the placement constructor `0x0068E4C0` clears it (`0x0068E4CA`); `0x0069FB10` copies it from the chosen material into the Bullet construction info as the body's restitution (`0x006A0173`-`0x006A0178`) |

`PPhysicsPlaneBase` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x70` | `f32[4]` | m_equationCoefficient | the plane equation, the normal's x, y and z at `+0x70` to `+0x78` and the constant at `+0x7C`; m_equationCoefficient (f32[4]), registered by `0x006959F0` (`0x00632960` at `0x00695A79`); no shipped .phyre file declares PPhysicsPlaneBase; the placement constructor `0x00689D50`, which stores the class vtable `0x00D79A60` (`0x00689DB5`), sets it to (1, 1, 1, 1) (`0x00689DBF`-`0x00689DD4`); PPhysicsPlaneBullet's slot `+0x08`, `0x0068A1D0` in its vtable `0x00D79A88`, reads it (`0x0068A246`-`0x0068A270`) into a Bullet btStaticPlaneShape through `0x00837700` (`0x0068A27D`; vtable `0x01CCE008` at `0x0083772F`), which scales the normal to unit length (`0x00837767`-`0x008377A5`), keeps the constant at `+0x50` (`0x008377AF`) and sets shape type `0x1C` (`0x008377C6`); `0x0068A1D0` keeps the shape at `+0x80` (`0x0068A283`) and adds it to the rigid body's compound shape `+0x120` through `0x00832590` (`0x0068A2C8`) only when the body's motion type `+0xE8` is not 1, dynamic (`0x0068A2A0`), and otherwise returns 9 (`0x0068A2D1`) |

`PPhysicsRigidBodyBase` (`0x118` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x38` | `f32[4]` | m_initialPosition | m_initialPosition (f32[4]), registered by `0x00696470` (`0x00632960` at `0x00696665`); no shipped .phyre file declares PPhysicsRigidBodyBase; the script method setInitialPosition (registered at `0x00696F49`) writes it through `0x006A5790`; the constructor `0x006912F0` clears `+0x38` to `+0x43` (`0x0069133D`, `0x00691341`) |
| `+0x58` | `f32[4]` | m_inertiaTensor | m_inertiaTensor (f32[4]), registered by `0x00696470` (`0x00632960` at `0x0069674B`); no shipped .phyre file declares PPhysicsRigidBodyBase; the constructor `0x006912F0` clears `+0x58` to `+0x63` (`0x0069134C`, `0x00691354`) |
| `+0x68` | `f32[4]` | m_initialLinearVelocity | m_initialLinearVelocity (f32[4]), registered by `0x00696470` (`0x00632960` at `0x006967BE`); no shipped .phyre file declares PPhysicsRigidBodyBase; the constructor `0x006912F0` clears it (`0x00691358`, `0x0069135C`) |
| `+0x78` | `f32[4]` | m_initialAngularVelocity | m_initialAngularVelocity (f32[4]), registered by `0x00696470` (`0x00632960` at `0x00696831`); no shipped .phyre file declares PPhysicsRigidBodyBase; the constructor `0x006912F0` clears it (`0x0069135F`, `0x00691363`) |
| `+0x88` | `f32[4]` | m_scale | m_scale (f32[4]), registered by `0x00696470` (`0x00632960` at `0x00696A93`); no shipped .phyre file declares PPhysicsRigidBodyBase; the constructor `0x006912F0` sets it to (1, 1, 1) (`0x00691369`-`0x0069137D`) |
| `+0xE1` | `u8[3]` | bytesE1 | the bytes after m_collisionGroup (u8 at `+0xE0`, registered by `0x00696470` at `0x00696D3E`; the constructor `0x006912F0` sets it to `0xF` at `0x006913D2`) up to m_mass (`+0xE4`); no registered member covers it (`0x006902F0` registers the `0x118`-byte class at `0x00690340`) |
| `+0xE4` | `f32` | m_mass | m_mass (f32), registered by `0x00696470` (`0x00632960` at `0x0069650C`); no shipped .phyre file declares PPhysicsRigidBodyBase; the script method getMass (registered at `0x006970DD`) returns it through `0x006A3B00`; the constructor `0x006912F0` clears it (`0x006913D9`) |
| `+0xE8` | `u8` | m_rigidBodyType | m_rigidBodyType (u8), registered by `0x00696470` (`0x00632960` at `0x0069657F`); no shipped .phyre file declares PPhysicsRigidBodyBase; the constructor `0x006912F0` clears it with a word store that sets `+0xE9` to 1 (`0x006913DF`) |
| `+0xEA` | `u8[6]` | bytesEA | the bytes after m_enabled (bool at `+0xE9`, registered by `0x00696470` at `0x00696DB1`; the constructor `0x006912F0` sets it to 1 with the word store at `0x006913DF`) up to `+0xF0`; no registered member covers it (`0x006902F0` registers the `0x118`-byte class at `0x00690340`) |

`PPhysicsShapeBase` (`0x68` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u8` | m_hollow | m_hollow (u8), registered by `0x00697320` (`0x00632960` at `0x006973B2`); no shipped .phyre file declares PPhysicsShapeBase |
| `+0x09` | `u8[3]` | pad09 | alignment bytes after m_hollow (u8 at `+0x08`) up to m_mass (f32 at `+0x0C`); no registered member covers it (`0x006904E0` registers the `0x68`-byte class at `0x00690530`) |
| `+0x0C` | `f32` | m_mass | m_mass (f32), registered by `0x00697320` (`0x00632960` at `0x00697425`); no shipped .phyre file declares PPhysicsShapeBase |
| `+0x10` | `f32` | m_density | m_density (f32), registered by `0x00697320` (`0x00632960` at `0x00697498`); no shipped .phyre file declares PPhysicsShapeBase |
| `+0x14` | `u8[4]` | bytes14 | the bytes after m_density (`+0x10`), before `+0x18`; no registered member covers it (`0x006904E0` registers the `0x68`-byte class at `0x00690530`) |
| `+0x50` | `f32[4]` | m_scale | m_scale (f32[4]), registered by `0x00697320` (`0x00632960` at `0x006975F0`); no shipped .phyre file declares PPhysicsShapeBase |

`PPhysicsWorldBase` (`0x60` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | m_gravity | m_gravity (f32[4]), registered by `0x00698180` (`0x00632960` at `0x00698280`); no shipped .phyre file declares PPhysicsWorldBase; the placement constructor `0x0068B9E0` sets it to (0, -9.8, 0) (`0x0068B9E5`-`0x0068B9F0`) |
| `+0x14` | `f32[4]` | m_worldMin | m_worldMin (f32[4]), registered by `0x00698180` (`0x00632960` at `0x00698366`); no shipped .phyre file declares PPhysicsWorldBase; the placement constructor `0x0068B9E0` sets it to (-5000, -5000, -5000) (`0x0068B9FA`-`0x0068BA08`) |
| `+0x24` | `f32[4]` | m_worldMax | m_worldMax (f32[4]), registered by `0x00698180` (`0x00632960` at `0x006983D9`); no shipped .phyre file declares PPhysicsWorldBase; the placement constructor `0x0068B9E0` sets it to (5000, 5000, 5000) (`0x0068BA0F`-`0x0068BA1D`) |

`PRaycastResult` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | m_contactPoint | the point the ray hit, w 1.0; m_contactPoint (f32[4]), registered by `0x00698500` (`0x00632960` at `0x0069858E`); no shipped .phyre file declares PRaycastResult; the world raycast `0x006A1A70`, which the script methods castRayFromScript (`0x006A1C70`) and castRayFromScriptWithCollisionGroup (`0x006A1D20`) call and `0x00697AC0` registers (`0x00697BBB`, `0x00697E19`), runs a Bullet ClosestRayResultCallback (vtable `0x00D7AB10`, `0x006A1B23`) through slot `+0x30` of the Bullet world (`0x006A1B79`) and, on a hit, writes the hit point into a `0x30`-byte result of this layout (`0x006A1BF3`-`0x006A1C06`) with w 1.0 (`0x006A1C0B`) |
| `+0x10` | `f32[4]` | m_contactNormal | the hit normal at unit length, w 0; m_contactNormal (f32[4]), registered by `0x00698500` (`0x00632960` at `0x00698601`); no shipped .phyre file declares PRaycastResult; `0x006A1A70` scales the callback's normal to unit length (`0x006A1BB9`-`0x006A1BDD`) and writes it here (`0x006A1C17`-`0x006A1C30`) |
| `+0x20` | `void*` | m_collisionObject | the object the ray hit; m_collisionObject (ptr), registered by `0x00698500` (`0x00632960` at `0x00698674`); no shipped .phyre file declares PRaycastResult; the placement constructor `0x0068A4B0` clears it (`0x0068A4B7`); `0x006A1A70` fills it through `0x0069ECE0` (`0x006A1BE9`), which stores the gameplay object behind the Bullet collision object (`0x0069ED14`, `0x0069ED42`) |
| `+0x28` | `void*` | m_collisionObjectClassDescriptor | the hit object's class; m_collisionObjectClassDescriptor (ptr), registered by `0x00698500` (`0x00632960` at `0x006986E6`); no shipped .phyre file declares PRaycastResult; `0x0068A4B0` clears it (`0x0068A4BB`); `0x0069ECE0` stores PPhysicsRigidBody's descriptor `0x02E48BD0` or PPhysicsCharacterController's `0x02E47ED0` (`0x0069ED1C`, `0x0069ED4A`); the script method getAsyncRaycastResultFromScript (`0x006A3770`, registered at `0x00697FAD`) reads entries of this layout, `0x30` bytes apart, from the world's array at `+0xB0` (`0x006A3797`), returns this object and class when entry `+0x0C` and both pointers are set (`0x006A37A1`-`0x006A37EA`), and copies out the point with w 1.0 and the normal with w 0 (`0x006A37F1`-`0x006A3818`) |

`PRenderTargetBase` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x09` | `u8` | m_msaaType | m_msaaType (u8), registered by `0x005E6F30` (`0x00632960` at `0x005E6FC2`); no shipped .phyre file declares PRenderTargetBase |
| `+0x0A` | `u8[2]` | pad0A | alignment bytes after m_msaaType (u8 at `+0x09`) up to m_renderTargetFlags (`+0x0C`); no registered member covers it (`0x005D9D20` registers the `0x10`-byte class at `0x005D9D70`) |
| `+0x0C` | `i32` | m_renderTargetFlags | m_renderTargetFlags (i32), registered by `0x005E6F30` (`0x00632960` at `0x005E7035`); no shipped .phyre file declares PRenderTargetBase |

`PShaderComputeProgramD3D11` (`0x90` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x80` | `u32` | m_dimX | m_dimX (u32), registered by `0x00617810` (`0x00632960` at `0x006178A2`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderComputeProgramD3D11 |
| `+0x84` | `u32` | m_dimY | m_dimY (u32), registered by `0x00617810` (`0x00632960` at `0x00617915`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderComputeProgramD3D11 |
| `+0x88` | `u32` | m_dimZ | m_dimZ (u32), registered by `0x00617810` (`0x00632960` at `0x00617988`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderComputeProgramD3D11 |
| `+0x8C` | `u8[4]` | bytes8C | the bytes after m_dimZ (`+0x88`) up to the end of the `0x90`-byte class; no registered member covers it (`0x00614D10` registers the `0x90`-byte class at `0x00614D5A`) |

`PShaderParameterCaptureBufferLocation` (`0x2` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | m_offset | m_offset (u16), registered by `0x005E8790` (`0x00632960` at `0x005E8811`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderParameterCaptureBufferLocation |

`PShaderParameterCaptureBufferTextureBase` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | m_textureBufferIndex | m_textureBufferIndex (u32), registered by `0x005E9350` (`0x00632960` at `0x005E94CA`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderParameterCaptureBufferTextureBase |

The per-draw block builder `0x00602A40` fills one record per capture-buffer entry and supplies a default for an empty
reference. It loads three defaults before the loop: the default 2D texture `0x02CBBE00` (`0x00602AB9`), the default
object `0x02CBC018` (`0x00602AD1`) and the default sampler state `0x02CBC368` (`0x00602ADB`).

- A `PShaderParameterCaptureBufferTexture2D` record with a null `m_texture` (`+0x10`) receives `0x02CBBE00`
  (`0x00602B7F`).
- A `PShaderParameterCaptureBufferTextureCubeMap` record with a null `m_texture` receives `0x02CBC018` (`0x00602B99`).
- Otherwise both read the texture's `+0x0C` (`0x00602B77`, `0x00602B91`), which the builder stores into
  `m_textureBufferIndex` (`0x00602CA3`).
- A `PShaderParameterCaptureBufferSampler` record with a null `m_samplerState` (`+0x08`) receives `0x02CBC368`
  (`0x00602BA2`, `0x00602BAC`).

`PShaderPassInfo` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | m_vertexEntryPoint | m_vertexEntryPoint (ptr), registered by `0x005E9C20` (`0x00632960` at `0x005E9CA9`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassInfo |
| `+0x08` | `void*` | m_fragmentEntryPoint | m_fragmentEntryPoint (ptr), registered by `0x005E9C20` (`0x00632960` at `0x005E9D86`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassInfo |
| `+0x10` | `void*` | m_geometryEntryPoint | m_geometryEntryPoint (ptr), registered by `0x005E9C20` (`0x00632960` at `0x005E9E63`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassInfo |
| `+0x18` | `void*` | m_computeEntryPoint | m_computeEntryPoint (ptr), registered by `0x005E9C20` (`0x00632960` at `0x005E9F40`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassInfo |
| `+0x20` | `u32` | m_vertexProfile | m_vertexProfile (u32), registered by `0x005E9C20` (`0x00632960` at `0x005E9D18`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassInfo |
| `+0x24` | `u32` | m_fragmentProfile | m_fragmentProfile (u32), registered by `0x005E9C20` (`0x00632960` at `0x005E9DF5`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassInfo |
| `+0x28` | `u32` | m_geometryProfile | m_geometryProfile (u32), registered by `0x005E9C20` (`0x00632960` at `0x005E9ED2`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassInfo |
| `+0x2C` | `u32` | m_computeProfile | m_computeProfile (u32), registered by `0x005E9C20` (`0x00632960` at `0x005E9FAF`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassInfo |

`PShaderPassStateBase` (`0x4` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_importantState | m_importantState (u32), registered by `0x005EA310` (`0x00632960` at `0x005EA395`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassStateBase |

`PShaderPassStateD3D11` (`0x190` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x004` | `u8[40]` | m_rasterDesc | the rasterizer description: the pass-state builder `0x0061DE20` creates the rasterizer state at `+0x168` from it (`0x0061DE5B`-`0x0061DE70`) and a wireframe copy at `+0x170` (`0x0061DEA9`-`0x0061DEE9`); m_rasterDesc (CD3D11_RASTERIZER_DESC), registered by `0x00617E60` (`0x00632960` at `0x00617EF2`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassStateD3D11 |
| `+0x02C` | `u8[52]` | m_depthDesc | the depth-stencil description: `0x0061DE20` creates the depth-stencil state at `+0x178` from it (`0x0061DF73`-`0x0061DF88`); m_depthDesc (CD3D11_DEPTH_STENCIL_DESC), registered by `0x00617E60` (`0x00632960` at `0x00617F65`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassStateD3D11 |
| `+0x168` | `void*[4]` | stateObjects | the four D3D11 state objects `0x0061DE20` creates: rasterizer `+0x168` (RSSetState), rasterizerAlt `+0x170` (the wireframe copy, used when context `+0x9C4` is 2), depthStencil `+0x178` (OMSetDepthStencilState), blend `+0x180` (OMSetBlendState); `0x0061DE20` builds each only while its slot is null (`0x0061DE4C`, `0x0061DE9F`, `0x0061DF05`, `0x0061DF5E`); no registered member covers it (`0x00614F90` registers the `0x190`-byte class at `0x00614FDA`) |
| `+0x188` | `u8` | m_stencilRef | stencilRef, passed with the depth-stencil state by `0x0061D260`; m_stencilRef (u8), registered by `0x00617E60` (`0x00632960` at `0x0061804B`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderPassStateD3D11 |
| `+0x189` | `u8[7]` | pad189 | the bytes after m_stencilRef (u8 at `+0x188`) up to the end of the `0x190`-byte class; no registered member covers it (`0x00614F90` registers the `0x190`-byte class at `0x00614FDA`) |

`PShaderProgramD3D11` (`0x78` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x28` | `u32` | m_constantBufferSize | m_constantBufferSize (u32), registered by `0x00618080` (`0x00632960` at `0x006181B0`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderProgramD3D11 |
| `+0x2C` | `u32` | m_globalConstantBufferIndex | m_globalConstantBufferIndex (u32), registered by `0x00618080` (`0x00632960` at `0x00618223`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderProgramD3D11 |
| `+0x30` | `u8[64]` | bytes30 | the bytes after m_globalConstantBufferIndex (`+0x2C`), before m_shaderProfile (`+0x70`); no registered member covers it (`0x00615030` registers the `0x78`-byte class at `0x0061507A`) |
| `+0x70` | `u32` | m_shaderProfile | m_shaderProfile (u32), registered by `0x00618080` (`0x00632960` at `0x00618296`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderProgramD3D11 |
| `+0x74` | `u8[4]` | bytes74 | the bytes after m_shaderProfile (`+0x70`) up to the end of the `0x78`-byte class; no registered member covers it (`0x00615030` registers the `0x78`-byte class at `0x0061507A`) |

`PShaderSource` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | m_entry | m_entry (ptr), registered by `0x005EA560` (`0x00632960` at `0x005EA65F`); no shipped .phyre file declares PShaderSource |
| `+0x20` | `u32` | m_profile | m_profile (u32), registered by `0x005EA560` (`0x00632960` at `0x005EA76B`); no shipped .phyre file declares PShaderSource |
| `+0x24` | `u8[4]` | bytes24 | the bytes after m_profile (`+0x20`) up to the end of the `0x28`-byte class; no registered member covers it (`0x005DB5C0` registers the `0x28`-byte class at `0x005DB610`) |

`PShaderStreamDefinition` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | m_name | m_name (ptr), registered by `0x005EA7A0` (`0x00632960` at `0x005EA831`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderStreamDefinition |
| `+0x14` | `u16` | m_nameHash | m_nameHash (u16), registered by `0x005EA7A0` (`0x00632960` at `0x005EA9F8`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderStreamDefinition |
| `+0x17` | `u8` | m_index | m_index (u8), registered by `0x005EA7A0` (`0x00632960` at `0x005EAA6B`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PShaderStreamDefinition |

`PSkeletonJointBounds` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | m_min | m_min (f32[3], a fixed-size array), registered by `0x00667700` (`0x00632A70` at `0x00667789`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PSkeletonJointBounds |
| `+0x0C` | `u32` | m_hierarchyMatrixIndex | m_hierarchyMatrixIndex (u32), registered by `0x00667700` (`0x00632960` at `0x00667878`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PSkeletonJointBounds |
| `+0x10` | `f32[3]` | m_size | m_size (f32[3], a fixed-size array), registered by `0x00667700` (`0x00632A70` at `0x006677FE`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PSkeletonJointBounds |

`PSkinBoneRemap` (`0x4` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | m_hierarchyMatrixIndex | m_hierarchyMatrixIndex (u16), registered by `0x00667920` (`0x00632960` at `0x006679AE`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PSkinBoneRemap |
| `+0x02` | `u16` | m_skeletonMatrixIndex | m_skeletonMatrixIndex (u16), registered by `0x00667920` (`0x00632960` at `0x00667A21`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PSkinBoneRemap |

`PTexture2DBase` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x28` | `u32` | m_width | m_width (u32), registered by `0x005EAC50` (`0x00632960` at `0x005EACE2`); the cluster loader binds it by name (`0x0059B430`) in the 31,368 shipped .phyre files that declare PTexture2DBase |
| `+0x2C` | `u32` | m_height | m_height (u32), registered by `0x005EAC50` (`0x00632960` at `0x005EAD55`); the cluster loader binds it by name (`0x0059B430`) in the 31,368 shipped .phyre files that declare PTexture2DBase |

`PTriggerReceiverTypeCallbackData` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x20` | `u32` | m_entryCount | m_entryCount (u32), registered by `0x006CD960` (`0x00632960` at `0x006CDB3C`); no shipped .phyre file declares PTriggerReceiverTypeCallbackData |
| `+0x24` | `u8[4]` | bytes24 | the bytes after m_entryCount (`+0x20`) up to the end of the `0x28`-byte class; no registered member covers it (`0x006CD8A0` registers the `0x28`-byte class at `0x006CD8F0`) |

`PPhysicsCapsuleBase` (`0x88` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x70` | `f32[2]` | m_radiusArray | the capsule's radius in the first element; m_radiusArray (f32[2], a fixed-size array), registered by `0x00694120` (`0x00632A70` at `0x006941AA`); no shipped .phyre file declares PPhysicsCapsuleBase; the placement constructor `0x0068D220`, which stores the class vtable `0x00D799E8` (`0x0068D2A1`), sets both elements to 1.0 (`0x0068D293`, `0x0068D28C`); PPhysicsCapsuleBullet's build `0x0069F870`, slot 0 of its vtable `0x00D79A10`, passes the first element (`0x0069F8A8`) as the radius to Bullet's btCapsuleShape constructor `0x008348A0` (`0x0069F8B0`; vtable `0x01CCDB68` at `0x008348C6`, shape type `0xA` at `0x008348D3`) and keeps the shape at `+0x88` (`0x0069F8B6`) |
| `+0x78` | `f32` | m_height | the capsule's height; m_height (f32), registered by `0x00694120` (`0x00632960` at `0x0069422C`); no shipped .phyre file declares PPhysicsCapsuleBase; the placement constructor `0x0068D220` sets it to 2.0 (`0x0068D285`); `0x0069F870` passes it (`0x0069F8A3`) to `0x008348A0`, which keeps half of it as the capsule's half height (`0x008348BE`, `0x008348E1`) |
| `+0x7C` | `u8[4]` | bytes7C | the bytes at `+0x7C`, before `+0x80`; no registered member covers it (`0x0068F580` registers the `0x88`-byte class at `0x0068F5CA`) |

`PPhysicsCharacterCamera` (`0x208` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u8[8]` | bytes08 | cleared by the constructor `0x00690F00` (`0x00690F13`); no registered member covers it (`0x0068F6C0` registers the `0x208`-byte class at `0x0068F710`) |
| `+0x28` | `u8[8]` | bytes28 | the constructor `0x00690F00` writes 1.0 to `+0x28` and 0 to `+0x2C` with one qword store (`0x00690F3A`); no registered member covers it (`0x0068F6C0` registers the `0x208`-byte class at `0x0068F710`) |
| `+0x38` | `u8[16]` | bytes38 | the constructor `0x00690F00` writes 0 to `+0x38`, 0.3 to `+0x3C` and 0 to `+0x40` (qword stores `0x00690F49`, `0x00690F51`); the camera position the script method getCameraPosition returns starts at `+0x48` (`0x006A3960`); no registered member covers it (`0x0068F6C0` registers the `0x208`-byte class at `0x0068F710`) |

`PPhysicsCylinderBase` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x70` | `f32[2]` | m_radiusArray | the cylinder's radius in the first element; m_radiusArray (f32[2], a fixed-size array), registered by `0x00695490` (`0x00632A70` at `0x0069551A`); no shipped .phyre file declares PPhysicsCylinderBase; the placement constructor `0x0068AEB0`, which stores the class vtable `0x00D79970` (`0x0068AF15`), sets both elements to 1.0 (`0x0068AF2D`, `0x0068AF26`); PPhysicsCylinderBullet's build `0x0069F8E0`, slot 0 of its vtable `0x00D79998`, passes the half extents (radius, half the height, radius) from the first element (`0x0069F920`) and m_height (`0x0069F913`) to Bullet's btCylinderShape constructor `0x008353F0` (`0x0069F948`; vtable `0x01CCDC60` at `0x0083540A`, shape type `0xD` at `0x00835454`) and keeps the shape at `+0x80` (`0x0069F94E`) |
| `+0x78` | `f32` | m_height | the cylinder's height; m_height (f32), registered by `0x00695490` (`0x00632960` at `0x0069559C`); no shipped .phyre file declares PPhysicsCylinderBase; the placement constructor `0x0068AEB0` sets it to 2.0 (`0x0068AF1F`); `0x0069F8E0` multiplies it by 0.5 (`0x01CEBB70`, `0x0069F918`) for the y half extent |
| `+0x7C` | `u8[4]` | bytes7C | the bytes at `+0x7C`, before `+0x80`; no registered member covers it (`0x0068FA00` registers the `0x80`-byte class at `0x0068FA4A`) |

`PPhysicsSphereBase` (`0x78` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x70` | `f32` | m_radius | the sphere's radius; m_radius (f32), registered by `0x006976A0` (`0x00632960` at `0x00697729`); no shipped .phyre file declares PPhysicsSphereBase; the placement constructor `0x0068AC60`, which stores the class vtable `0x00D79808` (`0x0068ACC1`), sets it to 1.0 (`0x0068ACCB`); PPhysicsSphereBullet's build `0x006A0280`, slot 0 of its vtable `0x00D79830`, reads it (`0x006A02BD`) into a `0x50`-byte Bullet btSphereShape (vtable `0x00D7AA18` stored at `0x006A02D1`, shape type 8 at `0x006A02D4`) as both its radius and its margin (`0x006A02DB`, `0x006A02E0`) and keeps the shape at `+0x78` (`0x006A02E9`) |
| `+0x74` | `u8[4]` | bytes74 | the bytes at `+0x74`, up to the end of the `0x78`-byte class; no registered member covers it (`0x006906D0` registers the `0x78`-byte class at `0x0069071A`) |

`PPhysicsTaperedCapsule` (`0x88` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x70` | `f32[2]` | m_upperRadiusArray | m_upperRadiusArray (f32[2], a fixed-size array), registered by `0x00697760` (`0x00632A70` at `0x006977ED`); no shipped .phyre file declares PPhysicsTaperedCapsule; the placement constructor `0x00688ED0`, which stores the class vtable `0x00D709F8` (`0x00688F35`), sets both elements to 1.0 (`0x00688F4D`, `0x00688F46`) |
| `+0x78` | `f32[2]` | m_lowerRadiusArray | m_lowerRadiusArray (f32[2], a fixed-size array), registered by `0x00697760` (`0x00632A70` at `0x00697862`); no shipped .phyre file declares PPhysicsTaperedCapsule; the placement constructor `0x00688ED0` sets both elements to 2.0 (`0x00688F5B`, `0x00688F54`) |
| `+0x80` | `f32` | m_height | the tapered capsule's height; m_height (f32), registered by `0x00697760` (`0x00632960` at `0x006978DC`); no shipped .phyre file declares PPhysicsTaperedCapsule; the placement constructor `0x00688ED0` sets it to 3.0 (`0x00688F3C`); slot 0 of the class's vtable `0x00D709F8` is `0x0068EA90`, which logs "WARNING: This shape is currently not supported by the physics engine." (`0x00D7A4F0`, through `0x005CDAA0` at `0x0068EAA0`) and returns `0x17` (`0x0068EAA5`), and slot `+0x08` is `0x0068EB70`, which calls slot 0 and returns its result when that is not 0 and `0x17` otherwise (`0x0068EB77`-`0x0068EB83`); the rigid-body build `0x0069FB10` calls each child shape's slot `+0x08` (`0x0069FC6D`) and returns the first failure (`0x0069FC72`) before it allocates the Bullet body, so a rigid body holding a tapered capsule gets no Bullet body |
| `+0x84` | `u8[4]` | bytes84 | the bytes after `+0x80` up to the end of the `0x88`-byte class; no registered member covers it (`0x00690810` registers the `0x88`-byte class at `0x0069085A`) |

`PPhysicsTaperedCylinder` (`0x88` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x70` | `f32[2]` | m_upperRadiusArray | m_upperRadiusArray (f32[2], a fixed-size array), registered by `0x00697910` (`0x00632A70` at `0x0069799D`); no shipped .phyre file declares PPhysicsTaperedCylinder; the placement constructor `0x00687DC0`, which stores the class vtable `0x00D76218` (`0x00687E25`), sets both elements to 1.0 (`0x00687E47`, `0x00687E40`) |
| `+0x78` | `f32[2]` | m_lowerRadiusArray | m_lowerRadiusArray (f32[2], a fixed-size array), registered by `0x00697910` (`0x00632A70` at `0x00697A12`); no shipped .phyre file declares PPhysicsTaperedCylinder; the placement constructor `0x00687DC0` sets both elements to 2.0 (`0x00687E55`, `0x00687E4E`) |
| `+0x80` | `f32` | m_height | the tapered cylinder's height; m_height (f32), registered by `0x00697910` (`0x00632960` at `0x00697A8C`); no shipped .phyre file declares PPhysicsTaperedCylinder; the placement constructor `0x00687DC0` sets it to 3.0 (`0x00687E2F`); slot 0 of the class's vtable `0x00D76218` is `0x0068EA90`, which logs "WARNING: This shape is currently not supported by the physics engine." (`0x00D7A4F0`, through `0x005CDAA0` at `0x0068EAA0`) and returns `0x17` (`0x0068EAA5`), and slot `+0x08` is `0x0068EB70`, which calls slot 0 and returns its result when that is not 0 and `0x17` otherwise (`0x0068EB77`-`0x0068EB83`); the rigid-body build `0x0069FB10` calls each child shape's slot `+0x08` (`0x0069FC6D`) and returns the first failure (`0x0069FC72`) before it allocates the Bullet body, so a rigid body holding a tapered cylinder gets no Bullet body |
| `+0x84` | `u8[4]` | bytes84 | the bytes after `+0x80` up to the end of the `0x88`-byte class; no registered member covers it (`0x006908B0` registers the `0x88`-byte class at `0x006908FA`) |

`PStreamInputLayoutD3D11` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `void*` | inputLayout10 | the Direct3D input layout built from m_streams: `0x0061E0B0` passes one input element per named stream and the program's m_compiledCode to the device's CreateInputLayout (slot `+0x58`) and stores the result here (`0x0061E1D2`); no registered member covers it (`0x00615220` registers the `0x18`-byte class at `0x00615270`) |

## Shipped data

| Fact | Value |
|---|---|
| `.phyre` files | 35,984; `m_size` 84 in all |
| namespaces passing the byte-order mark and the size identity | 35,984 |
| `+0x18` and `+0x1C` | 0 in every file |
| records | 201,576 type entries, 684,244 class records, 2,192,621 member records |
| distinct names | 19 type-table names, 177 class names, 349 member names, 527 class and member pairs |
| type-table names | `PAnimationKeyDataType`, `PChar`, `PContextSwitch`, `PInt16`, `PInt32`, `PLODBlendType`, `PLODMetricType`, `PLightType`, `PModifier`, `PRenderDataType`, `PSceneRenderPassType`, `PShadowCasterType`, `PTextureFormatBase`, `PUInt128`, `PUInt16`, `PUInt32`, `PUInt8`, `bool`, `float` |
| class records with `w7` bit `0x1` | 0 |
| `w7` values | 0 (523,918), 8 (66,379), 32 (49,068), 2 (38,322), 12, 34 and 40 (2,184 each), 20 (5) |
| fixed-size arrays (`w5` non-zero) | 16 pairs, counts 2 to 23 |
| class names with a registered descriptor of that name | 177 of 177 (`PBase` and `PClassDescriptor` from `0x006318A0` and `0x00631C40`: `0x006318A0` builds `PBase` at `0x02CF8270` with size 1, alignment 1 and no parent (`0x00631913`-`0x0063194A`); `0x00631C40` builds `PClassDescriptor` at `0x02CF8470` with size `0x100`, alignment `0x10`, the parent and adjustment its initialiser `0x00163E30` gives, `PBase` and `0x30`; both store the name, the default namespace `0x01F2E330` at `+0x70` and the next index from `0x02CF8260`, building that namespace first when its guard `0x02CF94EC` shows it unbuilt (`0x006319E4`, `0x00631DA6`)) |
| pairs registered statically under that class | 527 of 527 |
| member records whose `w4` & `0x7FFFFFFF` equals the run-time attribute word | 2,192,621 of 2,192,621 |
| static member registrations in the executable | 895 (680 plain, 165 array, 29 fixed-size, 21 enum) over 278 descriptors |

`PArray<T>` and `PSharray<T>` appear in files under their full instantiation names
(`PArray<PAnimationChannel *>`); each is registered by its own template descriptor.

### Data files

| File | Rows | What it lists |
|---|---:|---|
| [phyre-field-schema-field-schema.tsv](phyre-field-schema-field-schema.tsv) | 897 | registered members: class, member, offset, type, attribute word, registration site; 895 rows are the static registrations, and two give only the site and caller of the calls the array constructor `0x00632A10` (`0x00632A41`) and the dynamic-member builder `0x00632B30` (`0x00632B89`) make on `0x00632960` |
| [phyre-field-schema-accessor-fields.tsv](phyre-field-schema-accessor-fields.tsv) | 73 | member offsets and widths read from script-accessor adapters |

## Loader behaviour

### Checking the namespace

`0x0059E070` returns `0x15` when the byte at `0x02CA9D90` is clear and `0xB` when the stream's slot
`+0x10` check fails. After the header it accepts the namespace only when it starts with `0x01020304` and
`+0x04 == +0x1C + 0x20 + 4 × (nTypes + 9 × nClasses + 6 × nMembers) + stringPoolSize`; otherwise it
returns 6. It then matches the tables (`0x0059B430`), handles dynamic classes (`0x0059AC00`) and reads
the instances (`0x0059E300`).

### Matching by name

`0x0059B430` resolves everything by name:

- **Types.** Each type-table name is hashed and looked up in the global type tree; a miss logs
  "Unable to find type".
- **Classes.** Each class name is looked up in the type tree and must belong to the target
  namespace, then in the namespace itself (`0x0063BA10`). A miss with `w7` bit `0x1` clear logs "File
  refers to compiled class … which does not exist in the current runtime".
- **Members.** Each member name is searched in the matched class's member list and then its
  ancestors', with an exact comparison, so a file member can land on a base-class member.
- **Member types.** `w1` selects a type-table entry or a class record, and the entry's matched type
  becomes the member's file type.

### Reporting differences

`0x0059BA40` compares each matched class with its file record and logs, through `0x005CDAA0`:

- a parent that was added, removed or changed;
- a member in the file but not in the executable, or the reverse;
- a member whose type changed;
- a member whose attribute word differs (run-time word without bit `0x1` against `w4` without bit
  `0x80000000`);
- a fixed-size array whose element count differs from `w5`.

None of these stops the load.

### Choosing a copy routine

`0x0059D2D0` gives every file member a routine, walking the parent records first. A class whose file record is
missing or declares no members gets no routine (`0x0059D2F4`, `0x0059D303`):

- no matching run-time member: the empty `0x0016D6A0`, so the bytes are skipped;
- same type, and the run-time width (the type's size, or 8 for a pointer or for a kind-2 counted buffer without
  attribute bit `0x40`, `0x0059D3D2`-`0x0059D418`) equals `w3`: `0x00599390`,
  or `0x00595E70` for a one-byte member that is not an array (the record's slot `+0x08` gives 0, `0x0059D46A`);
- same type with a different width, or a fixed-size array whose count differs while offset and
  attribute word match: skipped;
- different type: the conversion `0x0059A030` returns, or skipped when there is no conversion. `0x0059A030` runs the 144
  conversion registrars `0x005850F0`-`0x00592770` once (guard byte `0x02CA9D91`), then looks the `(source, destination)`
  pair up in the tree they fill ([Image hardening](../Compiler-And-C-Runtime/image-hardening.md)).

The byte argument of `0x0059D2D0` orders that pair: 0 gives (run-time type, file type), any other value (file type,
run-time type) (`0x0059D39C`-`0x0059D3B2`). Both callers give 1, which `0x0059E070` sets (`0x0059E1DC`, `0x0059E218`).

`0x00599390` and `0x00595E70` take (source base, destination base, desc, context), where `desc` holds the element
count, the source stride, the destination stride and a byte at `+0xC`. With that byte clear, the source is read at
the run-time offset `+0x48` and the destination written at `w2`; with it set, the other way round. Each routine runs
`desc` count times, stepping the two bases by the two strides.

`0x00595E70` copies one byte each time. `0x00599390` copies `w3` bytes with `memcpy` (`0x00861EBA`), and for a fixed-size
array `w3` times the larger of `w5` and the run-time count `+0x60` (`0x005993F3`-`0x0059940D`). A fixed-size array whose
count differs while its offset or attribute word also differs is therefore copied at the larger count.

### Dynamic classes

For a class record with `w7` bit `0x1` and no registered match, `0x0059AC00` takes the parent from
`w0`, refuses an abstract parent or one without a default constructor, and builds a
`PClassDescriptorDynamic` (`0x00632E80`). Its file members become `PClassDataMemberDynamic` records
through `0x006393A0` and `0x00632B30`. A flagged class still without a descriptor returns `0x13`. No
shipped file sets the flag.

`0x006393A0(descriptor, name, type, attributes, context)` adds one member and returns its record; `0x0059AC00` gives
it the file member's `w4` bit `0x2` alone as the attributes and context 0 (`0x0059AE57`, `0x0059AE9B`). It returns 0
when `0x0063A4C0` refuses the member: a null name, a name `0x00597220` already finds in the class or an ancestor, or a
member without attribute bit `0x2` whose type gives, through its slot `+0x08`, a class descriptor that is abstract
(flag bit `0x2`) or is this class or derives from it (`0x0063A4D8`-`0x0063A525`).

Otherwise `0x006393A0` takes the offset from `0x0063C630`, allocates `0x60` bytes (`0x00584740`), returning 0 when that
fails, and builds the record with `0x00632B30`, giving it the attributes with bit `0x1` set and flag 0.

`0x00632B30` builds the record through `0x00632960` with attribute bit `0x1` cleared (`0x00632B5D`), so `0x00632FB0` keeps
the given name pointer. It then installs its vtable `0x00D58358`, stores a copy of the name (`0x001C26B0`) at `+0x58`
and ORs bit `0x1` back into `+0x28`. Unless the name is the pointer held at `0x01F2DF28`, it also points the name
`+0x20` at the copy with bit `0x1` cleared (`0x00632BB5`-`0x00632BC7`); for that name the copy is made from a null
pointer, so `+0x58` is 0 (`0x00632B99`-`0x00632BAB`). It returns the record.

## Modding notes

- A file's class and member names must match registered names exactly. A renamed member is skipped
  and only logged, and the log is never shown in the shipped game.
- File offsets need not match run-time offsets; the loader copies member by member. Keep each
  member's type and width (`w3`) equal to the registered ones, or its data is dropped.
- Setting `w7` bit `0x1` on a class the executable does not have makes the loader build it from the
  file's members, under a parent that is concrete and has a default constructor.
- The attribute word in a file must equal the registered one apart from bit `0x80000000`; a different word
  only logs a message.

## Related

- [Bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md): where the 35,984 `.phyre` files are stored.
- [Debug logging](../Engine-Core/debug-logging.md): the log call that carries the loader's messages.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI names of the descriptor templates.
- [Bullet physics](../Third-Party-Libraries/bullet-physics.md): the physics classes, which no shipped file declares.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 8 calls with 4 other topics</summary>

**Application** (explained on [game application](../Engine-Core/game-application.md))

| Function | | Functions |
|---|---|---|
| `0x00584740` | is called by | `0x001A98B0` |

**Sound and music** (explained on [audio manager](../Sound-And-Music/audio-manager.md), [sound engine](../Sound-And-Music/sound-engine.md))

| Function | | Functions |
|---|---|---|
| `0x00584740` | is called by | `0x002125A0`, `0x00225C40`, `0x006794D0` |

**Controls and input** (explained on [controllers](../Controls-And-Input/controllers.md))

| Function | | Functions |
|---|---|---|
| `0x00584740` | is called by | `0x007973D0`, `0x00797460`, `0x00797690` |

**Platform** (explained on [phyre post effect classes](phyre-post-effect-classes.md))

| Function | | Functions |
|---|---|---|
| `0x00584740` | is called by | `0x00650D40` |

</details>
