[Home](../../README.md) / [PhyreEngine](README.md) / PhyreEngine asset files

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| PhyreEngine asset files: the .phyre cluster header, the packed namespace, the instance data and how the loader reads and fixes up a cluster | format | PhyreEngine | Asset files and animation | The .phyre file that holds every model, texture, shader and animation of the remastered art: the 84-byte cluster header, the packed namespace that names every class and field the file uses, the instance lists, user fixups, header-class tables, packed fixup tables and D3D11 buffers in stream order, the loader that checks the header, binds the file's schema to the engine's registered classes and converts each object to its runtime layout, and counts over all 35,984 shipped files. | 0x0019CB20, 0x00637C50, 0x0059E070, 0x0059A3B0, 0x0059A6F0, 0x0059C180, 0x00686D00, 0x0069E780, 0x0059D550, 0x02CA9D90, 0x0059AAE0, 0x0059B430, 0x00599500, 0x0059AC00, 0x0059E300, 0x0059E780, 0x0059D6A0, 0x0059F500, 0x0059D590, 0x0059E880, 0x0059D940, 0x0059CE30, 0x0059C700, 0x0059C250, 0x00686DE0, 0x02CAA0A0, 0x00676450, 0x00675EF0, 0x00676BD0, 0x006753A0, 0x00675580, 0x006D4CF0, 0x006DA380, 0x005BFF30, 0x005FE350, 0x001605C0, 0x001615C0, 0x00167DB0, 0x001688F0 |

## What the player sees

Every character, monster, weapon, map, texture, shader and font of the remastered art is drawn from
`.phyre` files. When one is malformed the game does not crash and does not report it: the asset is
simply missing, or a texture or model part fails to appear.

## Where it comes from

The files sit in the archive under `gamedata/d3d11/artdata/`, as `<name>.dae.phyre` for scenes and
meshes, `<name>.dds.phyre` for textures and `<name>.fx.phyre` for shaders. The `.ah` lists beside them
name, in order, the files each model, map or font loads.

Each file named in an `.ah` list is loaded only once and then shared: a second request for the same path raises a use
count instead. Inside the file, a table of names describes every class and field it holds, and the game matches those
names to its own classes to rebuild each object; a name it does not know is dropped with a log line.

A load request of kind 1 from such a list reaches `0x0019CB20(manager, path)` through `0x001A07B0`. It
hashes the path (`0x00674A00`: 5381, × 33 plus each byte as a signed value, `0x00674A17`, masked to 31 bits) and
looks it up in the manager's loaded set. A hit raises the entry's reference count and returns the loaded
cluster; a miss loads the file through `0x00637C50` and records it.

The loaded set is a tree whose root is the manager's `+0x40`: the lookup takes the first node whose dword
key `+0x20` is not below the hash and keeps it only when that key equals the hash (`0x0019CB59`-`0x0019CB92`).
It runs between `0x005CD4F0(manager)` and `0x005CD820(manager)`. A hit increments the entry's count `+0x04`
and returns the entry's `+0x08` (`0x0019CBA1`-`0x0019CBB5`).

A miss takes an entry from the manager's pool `+0x60` (`0x001BA860`, `0x0019CBC3`) and sets its byte `+0x00`
to 1, its `+0x10` to the third argument, which all six callers give as 0, and its count `+0x04` to 1
(`0x0019CBCB`-`0x0019CBD1`). It loads into the entry with `0x00637C50(entry + 8, path)` (`0x0019CBDF`).

When that returns non-zero or leaves `+0x08` null (`0x0019CBE4`-`0x0019CBED`), it clears the byte `+0x00` and
the count, gives the entry back to the pool with `0x002124C0` and returns 0 (`0x0019CC20`-`0x0019CC36`).
Otherwise it stores the entry under the hash in the map at `+0x28` (`0x0020B5F0`, `0x0019CC06`, `0x0019CC0B`),
again between `0x005CD4F0` and `0x005CD820`, and returns the entry's `+0x08` (`0x0019CC0E`-`0x0019CC1B`).

`0x00637C50` opens the path as a `PStreamReaderFile` (`0x00597970`),
returns 1 for a null path and 10 when the file does not open, and then calls the cluster reader
`0x0059E070` repeatedly, one cluster after another, until the stream position reaches the file size.
Each cluster gets its own `0xA0`-byte container, chained through `+0x98`.

`0x00637C50(out, path)` builds each container with `0x00633070`, points its list at `+0x88` at itself and
clears `+0x98`, and stores the first one at `out` (`0x00637CA4`-`0x00637CE3`); a failed allocation gives
`0xD` (`0x00637CF5`, `0x00637DAF`). A new container is made only after a cluster reads without error while
the stream position `+0x18` has not reached the size `+0x1C`, and goes on the end of the chain
(`0x00637D29`-`0x00637DA0`); a size of `0xFFFFFFFF` skips that end test (`0x00637D03`, `0x00637D2D`).

Every exit once the stream is open calls `0x0059BD40` on it (`0x00637CF0`, `0x00637DB9`) and then `0x00598100`
(`0x00637DE8`); the exit for a file that does not open calls `0x00598100` alone (`0x00637C9A`, `0x00637DE3`). On an
error the first container is destroyed (`0x006336E0`, then `0x00584730`), `out` is cleared and the error is
returned (`0x00637DBE`-`0x00637DDC`); a full read returns 0 (`0x00637DE1`).

## Layouts

### File order

A cluster is read front to back with no seeks; this is the order the loader consumes it in.

```
header                     84 bytes (m_size)
packed namespace           m_packedNamespaceSize bytes
instance-list headers      m_instanceListCount x 36 bytes
instance data              per list: m_objectsSize bytes of objects, then m_arraysSize bytes of arrays
user-fixup data            m_userFixupDataSize bytes
user-fixup records         m_userFixupCount x 12 bytes
header-class words         m_headerClassInstanceCount x 4 bytes
header-class child records m_headerClassChildCount x 16 bytes
pointer-array fixup table  m_pointerArrayFixupSize bytes, packed
pointer fixup table        m_pointerFixupSize bytes, packed
array fixup table          m_arrayFixupSize bytes, packed
D3D11 data                 index buffer, vertex buffer, then texture images
```

### The cluster header

Twenty-one `u32` fields. `0x005983E0` registers the first eighteen as `PClusterHeaderBase`,
`0x00598C50` the last three as `PClusterHeaderD3D11`, and `0x00598DF0` the nine of `PInstanceListHeader`;
the namespace of every file declares the same names in the same places.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_phyreMarker | `0x50485952`, the bytes "RYHP" |
| `+0x04` | `u32` | m_size | header length, 84 |
| `+0x08` | `u32` | m_packedNamespaceSize | bytes of namespace that follow |
| `+0x0C` | `u32` | m_platformID | `0x44583131`, the bytes "11XD" |
| `+0x10` | `u32` | m_instanceListCount |  |
| `+0x14` | `u32` | m_arrayFixupSize | packed bytes of the array fixup table |
| `+0x18` | `u32` | m_arrayFixupCount | its decoded entries, the sum over the lists |
| `+0x1C` | `u32` | m_pointerFixupSize |  |
| `+0x20` | `u32` | m_pointerFixupCount |  |
| `+0x24` | `u32` | m_pointerArrayFixupSize |  |
| `+0x28` | `u32` | m_pointerArrayFixupCount |  |
| `+0x2C` | `u32` | m_pointersInArraysCount | the sum over the lists |
| `+0x30` | `u32` | m_userFixupCount |  |
| `+0x34` | `u32` | m_userFixupDataSize |  |
| `+0x38` | `u32` | m_totalDataSize | the sum of the lists' m_size |
| `+0x3C` | `u32` | m_headerClassInstanceCount |  |
| `+0x40` | `u32` | m_headerClassChildCount |  |
| `+0x44` | `u32` | m_physicsEngineID | 0, or `0x424C4C54` ("TLLB") |
| `+0x48` | `u32` | m_indexBufferSize |  |
| `+0x4C` | `u32` | m_vertexBufferSize |  |
| `+0x50` | `u32` | m_maxTextureBufferSize |  |

### The instance-list header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_classID | 1-based position in the namespace's class table |
| `+0x04` | `u32` | m_count | objects in the list |
| `+0x08` | `u32` | m_size | m_objectsSize + m_arraysSize |
| `+0x0C` | `u32` | m_objectsSize |  |
| `+0x10` | `u32` | m_arraysSize |  |
| `+0x14` | `u32` | m_pointersInArraysCount |  |
| `+0x18` | `u32` | m_arrayFixupCount | this list's share of each fixup table |
| `+0x1C` | `u32` | m_pointerFixupCount |  |
| `+0x20` | `u32` | m_pointerArrayFixupCount |  |

### The packed namespace

The namespace is the file's own schema: every type, class and member it uses, by name. Its layout is
the one the byte-swap routine `0x0059C180` walks (eight header words, then `nTypes` words, `nClasses`
nine-word records and `nMembers` six-word records) and the one the validator `0x0059E070` checks.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | bom | `0x01020304`, stored 04 03 02 01 |
| `+0x04` | `u32` | size | equals m_packedNamespaceSize |
| `+0x08` | `u32` | nTypes |  |
| `+0x0C` | `u32` | nClasses |  |
| `+0x10` | `u32` | nMembers |  |
| `+0x14` | `u32` | poolSize | bytes of the string pool |
| `+0x18` | `u8[4]` | reserved | 0 in every shipped file; read by no function on a shipped file: the validator `0x0059E070` sums `+0x08`, `+0x0C`, `+0x10`, `+0x14` and `+0x1C` against `+0x04` (`0x0059E173`-`0x0059E191`), checks the byte-order mark `+0x00` (`0x0059E167` cmp dword [rdi], `0x1020304`) and reads nothing else of the header, the binders take the counts and the records, and the byte swap `0x0059C180` (`0x0059C1B7`-`0x0059C1BC`) runs only when `0x0059A3B0` finds the cluster marker byte-reversed (`0x0059A3FF`-`0x0059A437`), which no shipped file is; nothing fixes its width |
| `+0x1C` | `u32` | extraSize | bytes of the block after the pool |
| `+0x20` | `u32[nTypes]` |  | pool offsets of the type names class record  x nClasses        9 words each member record x nMembers        6 words each char[poolSize]                  NUL-terminated names byte[extraSize]                 indexed by class word 8 |

The loader requires `size == 0x20 + extraSize + 4 × (nTypes + 9 × nClasses + 6 × nMembers) + poolSize`
(`0x0059E070`), which places the extra block after the pool.

Class record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | parent | 1-based class index of the base class, 0 for a root |
| `+0x04` | `u32` | fileSize | low 28 bits: bytes per object in the file |
| `+0x08` | `u32` | name | pool offset |
| `+0x0C` | `u32` | memberCount | the class's records, taken in order from the member table |
| `+0x1C` | `u32` | flags | `0x01` dynamic class, `0x04` header class |
| `+0x20` | `u32` | extra | 1-based offset into the extra block, 0 for no extra data |

Member record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | name | pool offset |
| `+0x04` | `u32` | type | below nTypes: type-table index; else nTypes + 1-based class index |

The same two-table reference, a type index below `nTypes` and otherwise `nTypes` plus a 1-based class
index, is used by the user-fixup records.

### User-fixup records

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | type | type or class reference, as in a member record |
| `+0x04` | `u32` | size | bytes of its data |
| `+0x08` | `u32` | offset | into the user-fixup data |

The data is usually a name: the class name a `PClassDescriptor` fixup resolves, or the format name of
a texture.

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PAssetReference` (`0x50` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `void*` | m_id | the asset's id; m_id (ptr), registered by `0x00675740` (`0x00632960` at `0x006757D9`); the cluster loader binds it by name (`0x0059B430`) in the 35,984 shipped .phyre files that declare PAssetReference; the script method getID (registered at `0x00675999`) returns its address through `0x005C4D20` |
| `+0x48` | `void*` | cluster | the cluster the reference belongs to: when one cluster absorbs another, `0x00677550` sets it on every object of a list whose class derives from PAssetReference (`0x0067757A`, `0x00677590`); no registered member covers it (`0x006751A0` registers the `0x50`-byte class at `0x006751F0`) |

`PAssetReferenceImport` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | m_id | the id an asset import names; the user-fixup reader `0x0059E880` keeps a PAssetReferenceImport record as raw bytes; m_id (ptr), registered by `0x00675DA0` (`0x00632960` at `0x00675E4B`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PAssetReferenceImport; the placement constructor `0x00674E50` clears it (`0x00674E7A`) |

`PDataBlockD3D11` (`0x88` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x70` | `u32` | m_offsetInVertexBuffer | where the block's data starts in the file's vertex buffer: `0x00670070` creates the block's immutable buffer from the file data at this offset (`0x006700C1`); m_offsetInVertexBuffer (u32), registered by `0x00665870` (`0x00632960` at `0x00665A03`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDataBlockD3D11 |
| `+0x78` | `u32` | m_dataSize | the size of the block's data: `0x00670070` creates the block's buffer with this byte width (`0x006700B1`); m_dataSize (u32), registered by `0x00665870` (`0x00632960` at `0x00665990`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDataBlockD3D11 |
| `+0x7C` | `u8[4]` | bytes7C | the bytes after m_dataSize (`+0x78`), before `+0x80`; no registered member covers it (`0x00661D30` registers the `0x88`-byte class at `0x00661D7A`) |

`PIndexDataBlockD3D11` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x68` | `u32` | m_offsetInIndexBuffer | the offset of the block's indices in the index buffer: the indexed draw `0x006224E0` passes it as the binding offset (`0x00622539`); m_offsetInIndexBuffer (u32), registered by `0x00666380` (`0x00632960` at `0x00666513`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PIndexDataBlockD3D11 |
| `+0x70` | `u32` | m_dataSize | the size of the block's index data; m_dataSize (u32), registered by `0x00666380` (`0x00632960` at `0x006664A0`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PIndexDataBlockD3D11 |
| `+0x74` | `u8[4]` | bytes74 | the bytes after m_dataSize (`+0x70`), before `+0x78`; no registered member covers it (`0x006621E0` registers the `0x80`-byte class at `0x0066222A`) |

`PMaterial` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `u32` | m_flag | m_flag (u32), registered by `0x005E4AA0` (`0x00632960` at `0x005E4C18`); the cluster loader binds it by name (`0x0059B430`) in the 2,184 shipped .phyre files that declare PMaterial |
| `+0x14` | `u8[4]` | bytes14 | the bytes after m_flag (`+0x10`), before `+0x18`; no registered member covers it (`0x005D9520` registers the `0x28`-byte class at `0x005D9570`) |

`PModifierNetworkInfoPacket` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_size | m_size (u32), registered by `0x006D1810` (`0x00632960` at `0x006D18A5`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x04` | `u32` | m_modifierCodeCount | the number of `0x20`-byte modifier-code records that follow the packet: `0x006D4CF0` reads it to hand them to the visitor (`0x006D4D0E`); m_modifierCodeCount (u32), registered by `0x006D1810` (`0x00632960` at `0x006D1918`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x08` | `u32` | m_modifierInstanceCount | the number of `0x20`-byte modifier-instance records after the codes: `0x006D4CF0` reads it (`0x006D4D1A`); m_modifierInstanceCount (u32), registered by `0x006D1810` (`0x00632960` at `0x006D198B`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x0C` | `u16` | m_inputCount | counted with m_outputCount for the two-byte buffer entries after the instances: `0x006D4CF0` reads it (`0x006D4D11`); m_inputCount (u16), registered by `0x006D1810` (`0x00632960` at `0x006D19FE`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x0E` | `u16` | m_outputCount | counted with m_inputCount for the two-byte buffer entries: `0x006D4CF0` reads it (`0x006D4D22`); m_outputCount (u16), registered by `0x006D1810` (`0x00632960` at `0x006D1A71`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x14` | `u32` | m_totalPersistentStateSize | m_totalPersistentStateSize (u32), registered by `0x006D1810` (`0x00632960` at `0x006D1B56`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x18` | `u32` | m_totalStateBlockSize | m_totalStateBlockSize (u32), registered by `0x006D1810` (`0x00632960` at `0x006D1BC9`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x1C` | `u32` | m_spuModifierCodeSize | m_spuModifierCodeSize (u32), registered by `0x006D1810` (`0x00632960` at `0x006D1C3C`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |

`POccluderGeometryObject` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_planeCount | the plane count: `0x006DA380` hands (count + 3) / 4 Matrix4 records of planes to the visitor (`0x006DA3A0`); m_planeCount (u32), registered by `0x006D9FC0` (`0x00632960` at `0x006DA051`); no shipped .phyre file declares POccluderGeometryObject |
| `+0x04` | `u32` | m_vertexCount | the vertex count: `0x006DA380` hands that many Point3 records to the visitor (`0x006DA3D4`); m_vertexCount (u32), registered by `0x006D9FC0` (`0x00632960` at `0x006DA0C0`); no shipped .phyre file declares POccluderGeometryObject |
| `+0x08` | `u32` | m_edgeCount | the edge count: `0x006DA380` hands count × 4 one-byte PUInt8 entries (4 bytes per edge) to the visitor (`0x006DA3FE`, `0x006DA427`); m_edgeCount (u32), registered by `0x006D9FC0` (`0x00632960` at `0x006DA12F`); no shipped .phyre file declares POccluderGeometryObject |
| `+0x0C` | `u8[4]` | pad0C | alignment bytes between m_edgeCount (`+0x08`) and m_minBounds (16-byte vector at `+0x10`); no registered member covers it (`0x006D9F00` registers the `0x30`-byte class at `0x006D9F50`) |
| `+0x10` | `f32[4]` | m_minBounds | m_minBounds (f32[4]), registered by `0x006D9FC0` (`0x00632960` at `0x006DA19E`); no shipped .phyre file declares POccluderGeometryObject |
| `+0x20` | `f32[4]` | m_maxBounds | m_maxBounds (f32[4]), registered by `0x006D9FC0` (`0x00632960` at `0x006DA20D`); no shipped .phyre file declares POccluderGeometryObject |

## Shipped data

Measured over the whole archive, reading each `.phyre` file in the loader's stream order.

| Fact | Value |
|---|---|
| `.phyre` files | 35,984 of 89,414 archive files; 27,154,292,432 of 58,894,815,547 bytes |
| neighbours in `gamedata/d3d11` | `.ah` 2,564 files, 12,235,216 bytes; `.ta` 45, 46,885; `.ker` 34, 470,844; `.fex` 14, 692,292 |
| header | `RYHP`, `m_size` 84, platform `11XD`, physics 0 in all 35,984 |
| D3D11 sizes | texture only 33,794; index and vertex, no texture 2,091; all zero 99; no file mixes vertex and texture |
| namespace | byte-order mark, repeated size and size identity hold in all 35,984; largest 24,999 bytes |
| namespace words `+0x18`, `+0x1C` | zero in every file, so no file has an extra block |
| class records | 684,244; words 4, 5, 6 and 8 zero in all |
| class flags | 0 ×523,918, 8 ×66,379, 32 ×49,068, 2 ×38,322, 12, 34 and 40 ×2,184 each, 20 ×5; bit 0x01 never set |
| distinct names | 19 type, 177 class, 349 member |
| instance lists | 212,329, all `m_classID` in range, 59 distinct classes |
| commonest list classes | `PParameterBuffer` 106,256; `PAssetReference` 35,984 (one per file); `PTexture2D` 29,184; `PTextureCubeMap` 4,610; `PMaterial`, `PSamplerState`, `PShaderParameterDefinition` 2,184 each; `PNode`, `PWorldMatrix` 2,097 each; `PMesh` 2,091 |
| list sizes | `m_size = m_objectsSize + m_arraysSize` in all 212,329 lists; `m_totalDataSize` is their sum in every file |
| fixup counts | the header's four counts are the sums of the list counts in every file |
| user fixups | present in every file; 131,488 records: `PClassDescriptor` 47,020, `PTextureFormatBase` 33,794, `PAssetReferenceImport` 28,037, `PRenderDataType` 16,695, `PSceneRenderPassType` 5,931, `PAnimationKeyDataType` 8, `PModifier` 3 |
| a texture's fixups | exactly one `PClassDescriptor` and one `PTextureFormatBase`, in all 33,794 |
| `idmaps.txt` | `gamedata/d3d11/artdata/shared/idmaps.txt`: 4,061,418 bytes, 75,624 CRLF lines, 37,812 key and value pairs, every key distinct and no key equal to its value; no `#` in any line |
| file end | every mesh file ends exactly after its index and vertex buffers, every all-zero file at the end of its array table; in a texture file the image bytes exceed `m_maxTextureBufferSize` in 33,705 and equal it in 89 |
| texture files | the 33,792 `.dds.phyre` files and the two font generator files `font/tuffy.fgen.phyre` and `font/tuffysdf.fgen.phyre`, one texture object each |
| texture formats | `ARGB8` 12,913, `BC5` 9,149, `DXT5` 7,039, `RGBA16F` 4,610 (every cube map), `A8` 45, `DXT1` 26, `L8` 9, `DXT3` 3 |
| texture images | in every texture file the image bytes are exactly the texture's levels: `m_mipmapCount` + 1 levels, each half the size of the one before (at least 1 pixel, or one 4 x 4 block for the `BC`/`DXT` formats), times 6 faces for a cube map; `m_memoryType` is 3 and the `m_format` byte 0 in all 33,794 |
| texture flags | `m_textureFlags` is 2 in the 89 single-level textures (the 89 whose image equals `m_maxTextureBufferSize`) and 0 in the rest |
| textures by list | every `shared/` and `chr_shadow/` texture and all but 10 `map/` and 554 `chr/` textures are named by a `.ah` list; those 564 are named by no `.ah` list and no prefetch list; the `font/`, `menu/` and `shaders/` textures are named by none of the `.ah` path tokens |

Every texture, one row each, with the members its own namespace gives:

| table | rows | folder |
|---|---:|---|
| [`phyre-asset-files-textures-map.tsv`](phyre-asset-files-textures-map.tsv) | 15,028 | `artdata/map/` |
| [`phyre-asset-files-textures-shared.tsv`](phyre-asset-files-textures-shared.tsv) | 9,529 | `artdata/shared/` |
| [`phyre-asset-files-textures-chr.tsv`](phyre-asset-files-textures-chr.tsv) | 8,644 | `artdata/chr/` |
| [`phyre-asset-files-textures-chr_shadow.tsv`](phyre-asset-files-textures-chr_shadow.tsv) | 512 | `artdata/chr_shadow/` |
| [`phyre-asset-files-textures-font.tsv`](phyre-asset-files-textures-font.tsv) | 64 | `artdata/font/` |
| [`phyre-asset-files-textures-menu.tsv`](phyre-asset-files-textures-menu.tsv) | 11 | `artdata/menu/` |
| [`phyre-asset-files-textures-shaders.tsv`](phyre-asset-files-textures-shaders.tsv) | 6 | `artdata/shaders/` |

| Column | Meaning |
|---|---|
| `path` | the file in the archive |
| `class` | `Texture2D` or `TextureCubeMap` |
| `format` | the name the `PTextureFormatBase` user fixup holds |
| `width`, `height` | `m_width` and `m_height`; for a cube map both are `m_size`, the edge of each face |
| `faces` | 1, or 6 for a cube map |
| `mip_levels` | `m_mipmapCount` + 1, the levels the image holds |
| `max_mip_level` | `m_maxMipLevel` |
| `texture_flags` | `m_textureFlags` |
| `image_bytes` | the bytes after the fixup tables, the texture image |
| `max_texture_buffer` | the header's `m_maxTextureBufferSize` |
| `file_bytes`, `sha256` | the file's size and SHA-256 |
| `ah_lists` | the `.ah` lists that name the texture, by its own path or by a map path `shared/phyremaps.txt` maps to it ([Prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)) |
| `prefetch_lists` | the prefetch files that name it |

Every `.phyre` file without a texture, one row each: the 2,091 mesh files and the 99 with no buffers (the 93 shader
files under `shaders/` and six `chr/weapon/mws` files that hold only an asset reference, four nodes and a world
matrix).

| table | rows | folder |
|---|---:|---|
| [`phyre-asset-files-models-chr.tsv`](phyre-asset-files-models-chr.tsv) | 1,053 | `artdata/chr/` |
| [`phyre-asset-files-models-chr_shadow.tsv`](phyre-asset-files-models-chr_shadow.tsv) | 588 | `artdata/chr_shadow/` |
| [`phyre-asset-files-models-map.tsv`](phyre-asset-files-models-map.tsv) | 456 | `artdata/map/` |
| [`phyre-asset-files-models-shaders.tsv`](phyre-asset-files-models-shaders.tsv) | 93 | `artdata/shaders/` |

| Column | Meaning |
|---|---|
| `path` | the file in the archive |
| `kind` | `mesh` (index and vertex buffers) or `no buffers` |
| `Mesh` to `DataBlock` | the objects of that class in the file's instance lists |
| `lists` | the file's instance lists |
| `objects_by_class` | every class of the file's lists with its objects, in list order |
| `index_buffer_bytes`, `vertex_buffer_bytes` | the header's `m_indexBufferSize` and `m_vertexBufferSize` |
| `file_bytes`, `sha256` | the file's size and SHA-256 |

Every `chr/` and `chr_shadow/` mesh file decoded: each object's members as its file's namespace gives them, read at their offsets in the packed object (a pointer member is one byte there and is not given).

| table | rows | one row per |
|---|---:|---|
| [`phyre-asset-files-meshes-chr.tsv`](phyre-asset-files-meshes-chr.tsv) | 1,053 | `chr/` `.dae.phyre` file |
| [`phyre-asset-files-mesh-segments-chr.tsv`](phyre-asset-files-mesh-segments-chr.tsv) | 12,320 | mesh segment |
| [`phyre-asset-files-mesh-vertex-blocks-chr.tsv`](phyre-asset-files-mesh-vertex-blocks-chr.tsv) | 98,528 | vertex data block |
| [`phyre-asset-files-meshes-chr_shadow.tsv`](phyre-asset-files-meshes-chr_shadow.tsv) | 588 | `chr_shadow/` `.dae.phyre` file |
| [`phyre-asset-files-mesh-segments-chr_shadow.tsv`](phyre-asset-files-mesh-segments-chr_shadow.tsv) | 588 | mesh segment |
| [`phyre-asset-files-mesh-vertex-blocks-chr_shadow.tsv`](phyre-asset-files-mesh-vertex-blocks-chr_shadow.tsv) | 4,704 | vertex data block |

| Column | Meaning |
|---|---|
| `path`, `file_bytes`, `sha256` | the file, its size and SHA-256 |
| `meshes`, `segments`, `skeleton_matrices`, `default_pose`, `default_materials`, `ps2_dl_indices` | the `PMesh` objects and, per mesh, the element counts of `m_meshSegments`, `m_skeletonMatrices`, `m_defaultPose`, `m_defaultMaterials` and `m_ps2DLIndices` |
| `instances`, `instance_values`, `bounds` | the `PMeshInstance` objects with their flags and numbers, and each `PMeshInstanceBounds` minimum and size |
| `materials`, `material_flags`, `render_pass_names` | the `PMaterial` objects, each `m_flag`, and the file's `PSceneRenderPassType` names |
| `nodes`, `joint_bounds`, `names` | the `PNode` and `PSkeletonJointBounds` objects, and every `PString` of the file in list order (the node and joint names) |
| `skin_bone_remaps` | each `PSkinBoneRemap` as hierarchy matrix index:skeleton matrix index, in list order |
| `dynamic_blocks` | each `PDynamicDataBlock` as stride:elements:streams |
| `vertex_streams`, `stream_values`, `render_data_types` | the `PVertexStream` objects, their offset:type:stream set values with how many streams have each, and the file's `PRenderDataType` names |
| `exports`, `imports` | the ids of the file's asset references and of its asset imports: the shader variants and textures it binds by name |
| `index_buffer_bytes`, `vertex_buffer_bytes` | the header's buffer sizes |
| `ah_lists` | the `.ah` lists that name the file ([Prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md), all four token tables) |
| `requested` | when the game requests one of those lists (`prefetch-manifests-ah-lists-chr.tsv` and [`prefetch-manifests-ah-lists-chr_shadow.tsv`](../Game-Files-And-Data-Tables/prefetch-manifests-ah-lists-chr_shadow.tsv)), `-` when it requests no list that names the file |
| `segment`, `material_index`, `matrix_index`, `skin_bones`, `primitive_type`, `lod_index`, `shape_index`, `gather_index`, `vertex_blocks` | a segment's place in its list and its `PMeshSegmentBase` and `PMeshSegmentD3D11` members (`vertex_blocks`: the element count of `m_vertexData`) |
| `index_count`, `index_type`, `index_min`, `index_max`, `index_bytes`, `index_offset` | its index block: `m_elementCount`, `m_type`, `m_minimumIndex`, `m_maximumIndex`, `m_dataSize`, `m_offsetInIndexBuffer` |
| `block`, `stride`, `element_count`, `streams`, `memory_type`, `offset`, `bytes` | a vertex block's place in its list and its `m_stride`, `m_elementCount`, `m_streams` count, `m_memoryType`, `m_offsetInVertexBuffer` and `m_dataSize` |

- In all 1,641 files the vertex blocks fill the vertex buffer: each block's bytes are its stride times its element count, the first starts at 0, each next where the one before ends, and the last ends at `m_vertexBufferSize`.
- The index blocks fill the index buffer the same way, each starting on a 4-byte boundary. All 12,908 index blocks have type 12, two bytes per index, and all 12,908 segments primitive type 2.
- In every file the segments' `vertex_blocks` sum to its `PDataBlock` objects and their `skin_bones` to its `PSkinBoneRemap` objects. In the 1,638 files without a dynamic mesh the blocks' stream counts sum to the file's `PVertexStream` objects; the other three (`chr_shadow` `hn1017_33`, `hn1017_43` and `m1134`) also hold five `PDynamicDataBlock` objects.
- Six `chr/weapon/mws/` files hold no mesh: `w1000`, `w1003`, `w1005`, `w1009`, `w1016` and `w5020`. Of the 1,047 `chr/` meshes, 1,046 name the vertex data `SkinnableVertex`, `SkinnableNormal`, `ST`, `SkinnableTangent`, `SkinnableBinormal`, `Color`, `SkinWeights` and `SkinIndices`, and `global/materialsphere` names `Vertex`, `Normal`, `ST`, `Tangent`, `Binormal` and `Color`.
- All 588 `chr_shadow/` meshes name the eight skinnable types, the three dynamic ones `Vertex`, `Normal` and `Tangent` as well.
- Every mesh names the render passes `Opaque` and `MayaRenderPass`. Every `chr_shadow/` mesh has one segment and two materials and imports its folder's `for_shadow.dds` and the `PhyreChrShader.fx` variant `CB0F9F994888730E82AD01521483E596`, 585 of them also `E0C4972F01FD4520BF3F1330C4E1C44D`.
- A list the game requests names every mesh file except the heads `hn1021_01` and `hn1081_01` in `chr/` and in `chr_shadow/`: each is named by its own list alone, which no model's path builds. Of the 512 `chr_shadow/` textures ([`phyre-asset-files-textures-chr_shadow.tsv`](phyre-asset-files-textures-chr_shadow.tsv)), 511 are named by a requested list, and `high/n10/n1081/tex/for_shadow.dds.phyre` only by the `hn1081_01` shadow list.

Each `chr/` and `chr_shadow/` segment joined to the shader variant it draws with, pass by pass:

| table | rows | one row per |
|---|---:|---|
| [`phyre-asset-files-mesh-segment-variants-chr.tsv`](phyre-asset-files-mesh-segment-variants-chr.tsv) | 12,908 | mesh segment: its material and the name the file exports it under, the variant the material imports, the render data types of its vertex blocks and of the file's dynamic streams, the variant's render passes, how many of them its streams satisfy, and each pass and type left open |
| [`phyre-asset-files-mesh-materials-chr.tsv`](phyre-asset-files-mesh-materials-chr.tsv) | 29,538 | `PMaterial`: exported name, variant, and the mesh default-set slots that hold it |
| [`phyre-asset-files-mesh-material-bindings-chr.tsv`](phyre-asset-files-mesh-material-bindings-chr.tsv) | 29,538 | `PMaterial`: its parameter buffer object, and the sets of values and samplers it holds |
| [`phyre-asset-files-mesh-material-textures-chr.tsv`](phyre-asset-files-mesh-material-textures-chr.tsv) | 29,508 | texture slot of a parameter buffer that names a file |
| [`phyre-asset-files-mesh-parameter-sets-chr.tsv`](phyre-asset-files-mesh-parameter-sets-chr.tsv) | 5 | distinct list of numeric parameter values |
| [`phyre-asset-files-mesh-sampler-sets-chr.tsv`](phyre-asset-files-mesh-sampler-sets-chr.tsv) | 2 | distinct list of sampler states |
| [`phyre-asset-files-mesh-parameter-definitions-chr.tsv`](phyre-asset-files-mesh-parameter-definitions-chr.tsv) | 214 | distinct parameter definition in the buffers |
| [`phyre-asset-files-mesh-vertex-streams-chr.tsv`](phyre-asset-files-mesh-vertex-streams-chr.tsv) | 103,232 | stream of a vertex data block |
| [`phyre-asset-files-mesh-block-digests-chr.tsv`](phyre-asset-files-mesh-block-digests-chr.tsv) | 103,232 | vertex data block: the digest of its bytes |
| [`phyre-asset-files-mesh-segment-indices-chr.tsv`](phyre-asset-files-mesh-segment-indices-chr.tsv) | 12,908 | mesh segment: its index count, the lowest and highest index, and the digest of its index bytes |
| [`phyre-asset-files-mesh-vertex-data-chr-01-b0001-to-hc1042_02.tsv`](phyre-asset-files-mesh-vertex-data-chr-01-b0001-to-hc1042_02.tsv) | 20,032 | vertex data block of a `chr/` file: its bytes, assets `b0001` to `hc1042_02` |
| [`phyre-asset-files-mesh-vertex-data-chr-02-hc1042_03-to-m1049.tsv`](phyre-asset-files-mesh-vertex-data-chr-02-hc1042_03-to-m1049.tsv) | 24,280 | the same, assets `hc1042_03` to `m1049` |
| [`phyre-asset-files-mesh-vertex-data-chr-03-m1050-to-m1189.tsv`](phyre-asset-files-mesh-vertex-data-chr-03-m1050-to-m1189.tsv) | 9,232 | the same, assets `m1050` to `m1189` |
| [`phyre-asset-files-mesh-vertex-data-chr-04-m1190-to-n1044.tsv`](phyre-asset-files-mesh-vertex-data-chr-04-m1190-to-n1044.tsv) | 11,688 | the same, assets `m1190` to `n1044` |
| [`phyre-asset-files-mesh-vertex-data-chr-05-n1045-to-n1208.tsv`](phyre-asset-files-mesh-vertex-data-chr-05-n1045-to-n1208.tsv) | 20,944 | the same, assets `n1045` to `n1208` |
| [`phyre-asset-files-mesh-vertex-data-chr-06-n1209-to-w8308.tsv`](phyre-asset-files-mesh-vertex-data-chr-06-n1209-to-w8308.tsv) | 12,352 | the same, assets `n1209` to `w8308` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-01-c1004-to-hc1025_02.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-01-c1004-to-hc1025_02.tsv) | 384 | vertex data block of a `chr_shadow/` file: its bytes, assets `c1004` to `hc1025_02` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-02-hc1026_01-to-hn1061_02.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-02-hc1026_01-to-hn1061_02.tsv) | 336 | the same, assets `hc1026_01` to `hn1061_02` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-03-hn1061_03-to-hn1172_02.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-03-hn1061_03-to-hn1172_02.tsv) | 368 | the same, assets `hn1061_03` to `hn1172_02` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-04-hn1172_03-to-m1050.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-04-hn1172_03-to-m1050.tsv) | 408 | the same, assets `hn1172_03` to `m1050` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-05-m1053-to-m1106.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-05-m1053-to-m1106.tsv) | 360 | the same, assets `m1053` to `m1106` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-06-m1107-to-m1180.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-06-m1107-to-m1180.tsv) | 536 | the same, assets `m1107` to `m1180` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-07-m1181-to-m1207.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-07-m1181-to-m1207.tsv) | 208 | the same, assets `m1181` to `m1207` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-08-m1208-to-m1251.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-08-m1208-to-m1251.tsv) | 352 | the same, assets `m1208` to `m1251` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-09-m1252-to-n1048.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-09-m1252-to-n1048.tsv) | 424 | the same, assets `m1252` to `n1048` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-10-n1053-to-n1109.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-10-n1053-to-n1109.tsv) | 400 | the same, assets `n1053` to `n1109` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-11-n1110-to-n1176.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-11-n1110-to-n1176.tsv) | 432 | the same, assets `n1110` to `n1176` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-12-n1177-to-s0009.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-12-n1177-to-s0009.tsv) | 392 | the same, assets `n1177` to `s0009` |
| [`phyre-asset-files-mesh-vertex-data-chr_shadow-13-s0014-to-s0031.tsv`](phyre-asset-files-mesh-vertex-data-chr_shadow-13-s0014-to-s0031.tsv) | 104 | the same, assets `s0014` to `s0031` |
| [`phyre-asset-files-mesh-index-data-chr.tsv`](phyre-asset-files-mesh-index-data-chr.tsv) | 12,320 | mesh segment of a `chr/` file: its index bytes in stored order |
| [`phyre-asset-files-mesh-index-data-chr_shadow.tsv`](phyre-asset-files-mesh-index-data-chr_shadow.tsv) | 588 | mesh segment of a `chr_shadow/` file: its index bytes in stored order |
| [`phyre-asset-files-mesh-dynamic-blocks-chr.tsv`](phyre-asset-files-mesh-dynamic-blocks-chr.tsv) | 24 | dynamic data block with its stream, or dynamic stream, of the three `chr_shadow/` dynamic meshes, with their modifier |
| [`phyre-asset-files-shader-pass-streams-chr.tsv`](phyre-asset-files-shader-pass-streams-chr.tsv) | 150 | render pass of the ten variants the segments draw with: its shader's stream definitions, in order |

| Column | Tables | Meaning |
|---|---|---|
| `parameter_buffer` | material-bindings, material-textures | the `PParameterBuffer` object as list and element, so two materials sharing a block of buffers stay apart |
| `parameter_set`, `sampler_set` | material-bindings | the row of the two set tables |
| `slot`, `type`, `texture` | material-textures | the sampler parameter's name, its texture type, and the file it imports |
| `sampler` | material-textures | the slot's sampler state as min filter/mag filter/wrap S/wrap T/wrap R/LOD bias/max anisotropy/border colour/base level/max level/flags; `-` for none |
| `values` | parameter-sets | `name=value` for each parameter; a value whose size has no typed form is `#` and its bytes as hex |
| `samplers` | sampler-sets | `name:state`, the state as in `sampler` |
| `name`, `parameter_type`, `data_type`, `size`, `count`, `uses` | parameter-definitions | the definition's fields, and how many buffers hold it |
| `block`, `stream`, `offset`, `type`, `render_data_type`, `stream_set` | vertex-streams | the data block, the stream's place in it and its `PVertexStream` fields |
| `sha1` | block-digests, segment-indices | digest of the block's bytes, or of the segment's index bytes in stored order |
| `render_data_type`, `type`, `format`, `vertices`, `stride`, `source_offset`, `data` | vertex-data | the stream's fields, its little-endian element format, the vertex count, the bytes of one vertex, the block's offset in the file, and its bytes as hexadecimal |
| `indices`, `index_width`, `source_offset`, `data` | index-data | the index count, the bytes of one index (2 or 4), the offset in the file, and the index bytes as hexadecimal |

A file's bytes after the scene data are the index data and then the vertex data, each at the offsets its
records store. All 12,908 segments' index ranges equal their stored bounds. The vertex and index bytes of all 1,635
meshes, 1,047 in `chr/` and 588 in `chr_shadow/`, are in the data tables above, and they hash to the digest tables.

A segment's blocks are the next `vertex_blocks` of its file in block order: eight for a skinned segment, six for the
16 of `global/materialsphere`. A block's `render_data_type` names its stream. In a skinned segment `SkinIndices`
holds four `uint8` and `SkinWeights` four `float32` per vertex. In `chr/` an index is a `position` in the segment's
list in the skin-bones table. That table holds `chr/` segments only; in `chr_shadow/` every index is below the
segment's `skin_bones`.

The bindings are the values a file stores. Of 945,216 texture slots in the buffers, 29,508 name a file, 29,506 of
them `TextureSampler` and 2 `irrCubeMap0`; the slots with no file are named in the definitions table. Six files hold
no material. A value the renderer sets at draw time is not a stored value and is not in these tables.

- A segment draws with the material at its `m_materialIndex` in its mesh's default set, and every instance's `m_materialSet` is its own mesh's set. Those materials are named `<name>-Skinned-VertexColor` (12,304 in `chr/`, 585 in `chr_shadow/`) or `<name>-VertexColor` (the 16 of `chr/global/materialsphere` and the three dynamic `chr_shadow/` meshes).
- Each file also exports a material under the base name, which no mesh's set holds: 16,042 in `chr/` and 588 in `chr_shadow/`. Each of them imports a variant that declares the rigid types `Color`, `Vertex`, `Normal`, `ST`, `Tangent` and `Binormal`, so a skinned mesh's streams match the variant of its `-Skinned-` material and not the one its base material imports.
- For each pass, `0x00609D80` first gives the pass shader's stream definitions the dynamic mesh's streams of their render data type, then `0x0060A010` the first vertex block stream of each type still open. A definition left open logs `Failed to find data block/vertex stream to satisfy RDT %s for stream %d`, `0x0060A010` returns `0x13`, and `0x0060B980` returns at `0x0060BF33` without drawing that segment or the instance's later ones.
- The ten variants the segments draw with give 150 passes: the 120 skinned ones define `Color`, `SkinnableVertex`, `SkinnableNormal`, `SkinIndices`, `SkinWeights`, `ST`, `SkinnableTangent` and `SkinnableBinormal`, the 30 of the two rigid variants `Color`, `Vertex`, `Normal`, `ST`, `Tangent` and `Binormal`. All 12,320 `chr/` segments and 585 of the 588 `chr_shadow/` segments satisfy every pass.
- The other three, `high/n10/n1017/mws/hn1017_33`, `hn1017_43` and `monster/m11/m1134/mws/m1134`, draw with the rigid variant `CB0F9F994888730E82AD01521483E596`. Their modifier `SkinLocalTangent` writes `Vertex`, `Normal` and `Tangent` from five dynamic data blocks, and their vertex blocks carry the eight skinnable types.
- So no stream of those three has the type `Binormal` that all 15 passes of that variant define: the match returns `0x13` in every pass, the shadow draw at `0x001F5F38` included, and the three meshes are not drawn: a character whose shadow model is one of them casts no shadow.

The 93 `shaders/` model files ([`phyre-asset-files-models-shaders.tsv`](phyre-asset-files-models-shaders.tsv)) decoded
with the `chr/` material walk, `shader_materials.py`:

| table | rows | one row per |
|---|---:|---|
| [`phyre-asset-files-shader-material-bindings.tsv`](phyre-asset-files-shader-material-bindings.tsv) | 93 | `PMaterial` (one per file): its parameter buffer object, how many definitions the buffer holds, and the sets of values and samplers it holds |
| [`phyre-asset-files-shader-parameters.tsv`](phyre-asset-files-shader-parameters.tsv) | 8,267 | `PShaderParameterDefinition` of a file, with its place in the material's parameter buffer |
| [`phyre-asset-files-shader-material-textures.tsv`](phyre-asset-files-shader-material-textures.tsv) | 1,993 | texture slot of a material's parameter buffer |
| [`phyre-asset-files-shader-parameter-sets.tsv`](phyre-asset-files-shader-parameter-sets.tsv) | 21 | distinct list of numeric parameter values |
| [`phyre-asset-files-shader-sampler-sets.tsv`](phyre-asset-files-shader-sampler-sets.tsv) | 12 | distinct list of sampler states |
| [`phyre-asset-files-shader-parameter-definitions.tsv`](phyre-asset-files-shader-parameter-definitions.tsv) | 297 | distinct parameter definition in the buffers |
| [`phyre-asset-files-shader-stream-definitions.tsv`](phyre-asset-files-shader-stream-definitions.tsv) | 13,356 | `PShaderStreamDefinition` of a file |

| Column | Tables | Meaning |
|---|---|---|
| `parameters` | material-bindings | how many definitions the material's parameter buffer holds |
| `definition`, `name`, `parameter_type`, `data_type`, `array_count`, `size`, `buffer_offset` | parameters | the definition's place in its list and its `m_parameterType`, `m_dataType`, `m_arrayElementCount` and `m_bufferLoc` size and offset |
| `constant_buffer_location` | parameters | `m_constantBufferLocation`, `-` for `0xFFFFFFFF` |
| `material_slot` | parameters | the definition's place in the run of definitions the material's parameter buffer points at (`+0x14`, with the count at `+0x10`), `-` when the run does not hold it |
| `stream`, `name`, `data_type`, `size`, `buffer_offset`, `name_hash`, `index` | stream-definitions | the definition's place in its list and its `m_dataType`, `m_bufferLoc` size and offset, `m_nameHash` and `m_index` |

The other columns are those of the `chr/` tables above.

- In all 93 files the definitions are, name for name, the `parameter_names` of
  [`shader-variant-selection-effects.tsv`](shader-variant-selection-effects.tsv), and their count its `parameters`.
- 7,768 definitions have a slot in their file's material buffer. The other 499, in 82 files, have none: `World` (82),
  `WorldViewProjection`, `WorldViewInverse`, `WorldView`, `WorldInverse` and `BoneTransformConstantBuffer` (81 each)
  and `BoneTransforms` (12).
- The 1,993 texture slots, 1,353 `Texture2D` and 640 `TextureCubeMap`, name no file and no sampler state; the sampler
  states are in the sampler sets. No parameter value is kept as hex.
- `phyrefxaa.fx.phyre` holds no stream definition; the other 92 hold 13,356.

Every map scene, `map/<area>/<map>/<map>.dae.phyre` (456 files), decoded object by object the same way, with each pointer member followed through the file's pointer fixup table to the object, import or user fixup it names:

| table | rows | one row per |
|---|---:|---|
| [`phyre-asset-files-scenes-map.tsv`](phyre-asset-files-scenes-map.tsv) | 456 | scene: its `.ah` lists, the packs that draw it and their tag-30 record counts, the instances matched and the records no instance names, object counts by class, imports by class, the variants and the checks |
| [`phyre-asset-files-scene-instances-map.tsv`](phyre-asset-files-scene-instances-map.tsv) | 274,258 | `PMeshInstance`: name, the record number the name gives, mesh, materials, flags and numbers, bounds and world matrix |
| [`phyre-asset-files-scene-meshes-map.tsv`](phyre-asset-files-scene-meshes-map.tsv) | 274,255 | `PMesh`: name, segment run, default materials and the element counts of its arrays |
| [`phyre-asset-files-scene-segments-map.tsv`](phyre-asset-files-scene-segments-map.tsv) | 274,277 | `PMeshSegment`: mesh, material, vertex block run and index block |
| [`phyre-asset-files-scene-vertex-blocks-map-1.tsv`](phyre-asset-files-scene-vertex-blocks-map-1.tsv) [`phyre-asset-files-scene-vertex-blocks-map-2.tsv`](phyre-asset-files-scene-vertex-blocks-map-2.tsv) | 1,805,837 | `PDataBlock`: stride, elements, streams, memory type, offset, bytes and stream layout |
| [`phyre-asset-files-scene-stream-layouts-map.tsv`](phyre-asset-files-scene-stream-layouts-map.tsv) | 2,190 | distinct block stride and stream list, each stream as offset:type:render data type:stream set, with the blocks that have it |
| [`phyre-asset-files-scene-materials-map.tsv`](phyre-asset-files-scene-materials-map.tsv) | 76,625 | `PMaterial`: name, shader variant, flag, render-pass remap, bound textures, parameter set and sampler set |
| [`phyre-asset-files-scene-parameter-sets-map.tsv`](phyre-asset-files-scene-parameter-sets-map.tsv) | 21 | distinct set of a material's parameter values, by parameter name |
| [`phyre-asset-files-scene-sampler-sets-map.tsv`](phyre-asset-files-scene-sampler-sets-map.tsv) | 2 | distinct set of a material's sampler states, by sampler name: minify and magnify filter, wrap S, T and R, LOD bias, anisotropy, border colour, base and max level, flags |
| [`phyre-asset-files-scene-nodes-map.tsv`](phyre-asset-files-scene-nodes-map.tsv) | 312,172 | `PNode`: name, parent and local matrix |
| [`phyre-asset-files-scene-cameras-map.tsv`](phyre-asset-files-scene-cameras-map.tsv) | 825 | `PCameraPerspective` or `PCameraOrthographic`: field of view or height, aspect, near and far planes, world matrix |
| [`phyre-asset-files-scene-skins-map.tsv`](phyre-asset-files-scene-skins-map.tsv) | 32,850 | `PSkinBoneRemap` with the `PSkeletonJointBounds` of the same index |
| [`phyre-asset-files-scene-pose-matrices-map.tsv`](phyre-asset-files-scene-pose-matrices-map.tsv) | 104,550 | `PMatrix4` |
| [`phyre-asset-files-scene-stream-bindings-map.tsv`](phyre-asset-files-scene-stream-bindings-map.tsv) | 51,390 | `PMeshInstanceSegmentStreamBinding`: render data type, name, name hash, index, input set |
| [`phyre-asset-files-scene-imports-map.tsv`](phyre-asset-files-scene-imports-map.tsv) | 22,026 | `PAssetReferenceImport`: id and target class |
| [`phyre-asset-files-scene-unmatched-instances-map.tsv`](phyre-asset-files-scene-unmatched-instances-map.tsv) | 5,983 | instance that matches no YM00 record, and why |
| [`phyre-asset-files-scene-procedural-records-map.tsv`](phyre-asset-files-scene-procedural-records-map.tsv) | 10,477 | `proceduralTextureConfigs.txt` record: whether its map's scene imports the texture, the materials that bind it as `TextureSampler`, and the matched instances whose first material does |

- In all 456 scenes the vertex blocks fill the vertex buffer and the index blocks the index buffer as in the character files. 274,272 index blocks have type 12 and five type 8, four bytes per index, with 73,500 to 139,767 indices (`byu0101`, `byu0102`, `byu0105` and two in `gil5001`). Every segment has primitive type 2.
- Each mesh's segment run, each segment's vertex block run and each block's stream run cover their lists once over. The 274,255 meshes hold 274,277 segments (19 meshes have two and one has four), and the 1,805,837 blocks hold 1,857,389 streams in 2,190 layouts. Three meshes are drawn by two instances.
- Every material remaps the render pass `Opaque` to `MayaRenderPass`; 76,031 bind a `TextureSampler` texture and 594 bind no texture. The 76,625 materials hold 21 distinct parameter value sets and 2 sampler state sets. Each scene's nodes, 312,172 in all, form one tree under one root.
- Cameras sit in 212 scenes (221 perspective, 604 orthographic), skin data in 58 (3,000 skinned segments, 32,850 bone remaps, 104,550 pose matrices) and stream bindings in 157; animation objects only in `bds0109` and `gil0102` ([Animation channel binding](phyre-animation-binding.md)).
- The 22,026 imports are 20,709 textures and 1,317 shader variants. Each scene is named by its own two lists, `<map>_d3d11.ah` and `<map>_d3d11_srm.ah`, and by no other `.ah` list.
- The 459 pack and scene pairs are 454 packs drawing their own scene and five drawing another map's ([Map art](../World-Areas-And-Travel/map-art.md#naming-the-map)). Of the 274,258 instances, 268,275 carry a number below the record count of the pack that draws their scene and are matched ([matching models to instances](../World-Areas-And-Travel/map-art.md#matching-models-to-instances)); the other 5,983 are matched to no record:
  - `alc0201` (2,927) and `frs0109` (2,510): no pack draws the scene.
  - `mic0108`: 539 instances named `mic0108_nodename<N>`, beside its 539 `nodename<N>` instances that match; their ninth character is not a digit.
  - `pla0103`: one instance named `pPlane1`, seven characters.
  - Six whose number is not below their pack's record count: `dor0104` 747 (747 records), `dor0105` 232 (232 records), `rsn0104` 1292 and 1293 (1,292 records), `rsn0107` 1123 and 1124 (1,123 records).

`gamedata/d3d11/artdata/shared/phyremaps.txt` beside it (8,492,839 bytes, 94,682 CRLF lines) holds 47,341 pairs: a
map texture's path under `/GameData/D3D11/ArtData/map/` and the file under `/GameData/D3D11/ArtData/shared/map/`
that holds it. The values are exactly the 9,529 files of `shared/map/`. No key is a shipped file, and each key is
named by at least one of the 914 map asset lists. `0x001A9940` reads it for the map art
([Map art](../World-Areas-And-Travel/map-art.md)).

- Each shared file carries one asset id, an `ArtData/...dds` string in its first 64 KiB. For 9,529 pairs the key is
  that id's own path; the other 37,812 keys are exactly the `idmaps.txt` keys.
- For every `idmaps.txt` pair both ids reach the same shared file, and that file carries the pair's value. No value
  is also a key.
- The remaster thus stores each distinct map texture once: up to 338 map texture paths share one file, and
  `idmaps.txt` sends an import of any of their ids to the id the file carries.
- The longest key is 91 characters and the longest value 119; the longest `idmaps.txt` id is 69.
- [`phyre-asset-files-shared-maps-rows.tsv`](phyre-asset-files-shared-maps-rows.tsv) gives every `phyremaps.txt`
  pair with its line, whether its key is the carried id or an `idmaps.txt` key (with that line), the row of the
  carried id's own pair, and how many map asset lists name the path.

### Bones and skin weights of the `chr/` meshes

| Table | Rows | One row per |
|---|---:|---|
| [`phyre-asset-files-mesh-bones-chr.tsv`](phyre-asset-files-mesh-bones-chr.tsv) | 27,612 | bone of a mesh (26,593), or `@FTR` node its mesh does not hold (1,019) |
| [`phyre-asset-files-mesh-skin-bones-chr.tsv`](phyre-asset-files-mesh-skin-bones-chr.tsv) | 67,532 | `PSkinBoneRemap`, in the order of its segment's list |

| Column | Tables | Meaning |
|---|---|---|
| `path`, `cm` | bones | the `.dae.phyre` file and the `.cm` of the same name under `obj_finish`, `-` when there is none |
| `mesh`, `bone` | both | the mesh's place in the file, and the bone's place in `m_matrixNames`; `-` for a node only the `.cm` holds |
| `name`, `parent`, `parent_name` | both, bones | the bone's name, and the bone `m_matrixParents` gives, `-` for the root |
| `ftr_node`, `ftr_key` | both, bones | the `@FTR` node number in the bone's `s<N>_` name, and that node's key |
| `parent_agrees` | bones | whether node N's parent is the node of the mesh parent |
| `skeleton_matrix` | both | the bone's place in `m_skeletonMatrices`, `-` for a bone without one |
| `default_pose`, `skeleton_values` | bones | the bone's matrix relative to its parent, and its skeleton matrix, 16 values each |
| `bounds_min`, `bounds_size` | bones | the `PSkeletonJointBounds` of the bone |
| `cm_matrix` | bones | what the node's stored matrix equals within 0.005: `skeleton`, `chain` (the inverse of the default poses multiplied up to the root), `both` |
| `segment`, `position` | skin-bones | the mesh segment, and the place in its list that a vertex's `SkinIndices` value names |
| `vertices` | skin-bones | the vertices of the segment |
| `weighted_vertices`, `weight_sum` | skin-bones | how many of them give this position a weight above 0, and the sum of those weights |

A bone named `s<N>_...` is node N of the `@FTR` of the `.cm` of the same name. All 26,439 such bones have the
parent that node has, or for 10 of them a `fosterParent` bone where the node is a root. The node's stored matrix is
the bone's inverse bind matrix:

- All 24,372 bones with a skeleton matrix have a stored matrix equal to it.
- The 2,067 others, which no vertex is skinned to, equal the inverse of their chained default poses.
- That chain also equals the stored matrix for 24,343 of the 24,372. In the other 29, in 10 files, the default pose
  differs from the bind pose. `cm_matrix` is `skeleton` for those.

The other bones are 144 in the six files with no `.cm` of their name (`c1014` to `c1017`, `hn1021_01`, `hn1081_01`)
and 10 named `__UNKNOWN_REF_NODE_fosterParent1` or `_UNKNOWN_REF_NODE_fosterParent1`, one a file. Of the `.cm` nodes,
1,019 in 512 files have no bone in the mesh, and none of them is the parent of one that does.

Each `PSkinBoneRemap` names a bone and a skeleton matrix, and that matrix's `PSkeletonJointBounds` names the same bone
in all 67,532. Each of the 1,341,188 vertices has `SkinWeights` that sum to 1, every position with a weight is inside
its segment's list, and every position has a weighted vertex.

## Loader behaviour

### Preconditions

`0x0059E070` returns `0x15` when the byte `0x02CA9D90` is zero and `0xB` when the stream is not open. The
byte is set by `0x0059D550`, which registers the cluster-header and instance-list classes: it calls
`0x005983E0` and `0x00598C50`, registers the `PClusterHeader` descriptor `0x02CAA0A0` by name with `0x006388C0`
and its members with `0x00639450`, calls `0x00598DF0`, and then sets the byte (`0x0059D57D`) and returns 0.

`0x0059D550` is slot 1 of the module vtable `0x00D26C40`, a module that static-initialiser code links into
the module list (`0x0016035C` stores the vtable), and the engine's start-up `0x005A08E0` calls slot 1 of
every listed module before any asset loads. Slot 2 of the same vtable, the module's shutdown
`0x0059FE20`, clears the byte again at `0x0059FF14`; after the shutdown walk `0x0059E070` returns `0x15` again.

### The header check

`0x0059A3B0` is the only header reader; its one caller `0x0059E070` seeds the buffer with `RYHP` and 84,
zeroes the rest and passes platform checking as the constant 1.

1. It reads 84 bytes; fewer returns 9.
2. If the marker is not `RYHP` it byte-swaps the whole header (`0x0063E2E0` with descriptor
   `0x02CAA0A0`) and tests again: still wrong returns 6; right sets the swapped flag, so a big-endian
   file is accepted.
3. It calls `0x00686D00` (`0x44583131`) and `0x0069E780` (`0x424C4C54`); a different platform, or a physics
   id that is neither Bullet nor 0, returns 6. Both compares are skipped when the platform-check
   argument is 0 (`0x0059A44D`, `0x0059A45C`).
4. It gives the namespace buffer `m_packedNamespaceSize` bytes (`0xD` when that fails) and returns 6
   when the buffer is null, which is what a zero-size namespace leaves. A buffer whose size word already
   equals that size is kept (`0x0059A479`); otherwise the new one comes from `0x0017D260(size, 4)` and the old
   one is released through `0x00584730` unless bit `0x80000000` of its size word is set (`0x0059A484`-`0x0059A4C8`).
5. With `m_size` 84 it reads the namespace (`0x0059A6F0`: one read, 9 when short, then `0x0059C180` when
   the file was swapped). A shorter header takes the surplus already read as the start of the
   namespace (6 when the surplus is larger than the namespace); a longer one is read on into a
   second buffer (`0xD`, 9).
6. It writes `m_size` to its sixth argument (`0x0059A4E4`). For an `m_size` other than 84 in a swapped
   file it first swaps the header back to file order (`0x0059A501`), and a longer header's second buffer
   (`0x0067B100`) gets all `m_size` bytes, the 84 already read first (`0x0059A52E`-`0x0059A56F`).
7. After a shorter header, `0x0059A6F0` reads the rest of the namespace and is given
   `namespace + surplus` (`0x0059A5B1`), which is the address it hands to `0x0059C180` (`0x0059A748`).
8. `0x0059A6F0` skips its read when the size is 0 or the buffer null, and swaps after a short read too
   (`0x0059A710`-`0x0059A748`); `0x0059A3B0` returns 0 when the namespace is read in full (`0x0059A5E0`).

`0x0059E070` then requires the byte-order mark and the size identity, or returns 6.

`0x0059C180` swaps the namespace of a big-endian file in place: its eight header words, every word of
the type-name table (`0x0059A8B0`), the nine words of every class record (`0x0059A780`) and the six
words of every member record. The string pool is left as it is.
The `extraSize` block after the pool is left as it is too. The eight header words are swapped first
(`0x0059C186`-`0x0059C1C4`), so the counts it then reads are in host order, and the type-name table is
swapped last, by a tail jump (`0x0059C245`).

### Binding the schema

- `0x0059AAE0` allocates one table entry per type (`0x18` bytes), class (`0x30`) and member (`0x38`).
  The three tables share one block, each part `(count × size + 0xF) & ~0xF` bytes long
  (`0x0059AB04`-`0x0059AB30`).
- A block whose size word already equals the total is reused; otherwise the new one comes from
  `0x0017D260(total, 0x10)`, `0xD` when that fails (`0x0059ABEC`), and the old one is released through
  `0x00584730` unless bit `0x80000000` of its size word is set (`0x0059AB3E`-`0x0059AB7C`).
- `0x0059AAE0` then zero-fills the block (`0x00861EC0`), hands the type, class and member parts with their
  counts to `0x0059FCA0` for the views at `+0x18`, `+0x28` and `+0x38` (`0x0059ABA2`-`0x0059ABCA`) and returns 0.
- `0x0059B430` finds each type and class name in the engine's registry (`0x006373D0`, keyed by a hash of
  1973, × 33 plus the low five bits of each byte), sets each class's parent from word 0, and matches
  each member to the runtime class's member of the same name, walking its bases. A class name is
  also looked up in the tree passed as its third argument (`0x0059BE00`, by each entry's descriptor
  name).
- Names the registry lacks are logged
  (`"Unable to find type '%s' on load"`, `"File refers to compiled class '%s' which does not exist
  in the current runtime"`) and do not stop the load.
- `0x00599500` finds the class bound to `PClusterHeader` (`0x13` when no class is bound), converts the header
  through the file's schema, and checks the platform again (6).
- That class is the `0x30`-byte table entry whose `+0x10` is the descriptor `0x02CAA0A0` (`0x00599543`). The
  conversion `0x00599670(entry, source, header, 1)` (`0x0059962A`) reads from a local copy of the 84 bytes
  (`0x005995E6`-`0x00599619`), or, when `m_size` is above 84, from the second buffer whose pointer is at `+0x08` of
  `0x00599500`'s own third argument (`0x0059951B`, `0x005995E0`), and writes into the header.
- `0x00599500`'s only caller `0x0059E070` passes as that third argument the pair it also passes to `0x0059A3B0` as the
  fourth argument (`0x0059E142`, `0x0059E200`).
- For a swapped file it swaps an 84-byte header back to file order before the copy (`0x00599592`) and
  swaps the converted header after it (`0x00599642`). The platform check compares `m_platformID` with
  `0x00686D00` (`0x00599647`-`0x00599656`); a match returns 0.
- `0x0059AC00` builds a dynamic class (`0x00632E80`) for each class record with flag `0x01` and no
  runtime class, under its parent; one left unbuilt returns `0x13`.

### Reading the instance data

`0x0059E300` runs the rest in stream order.

- `0x00686D10` copies the three D3D11 sizes into the `0x28`-byte local that `0x00686C20` has just zeroed
  (`0x0059E343`; the header's dwords `+0x48`, `+0x4C` and `+0x50` to its `+0x20`, `+0x1C` and `+0x24`),
  and `0x0059E780` reads the list
  headers (`0x00596FC0`), returning 6 for a `m_classID` outside the class table.
- `0x0059E780` returns the result of `0x00596FC0` when it is not 0 (`0x0059E7CD`). For each list it stores the
  class entry in the load record's per-list array at `+0x58` (`0x0059E801`). When the entry's runtime
  descriptor has a non-zero word `+0xE0`, the total its third argument points at first becomes
  `(t + a - 1) & ~(a - 1)` for a non-zero alignment a, the word `+0xE4` (`0x0059E81F`-`0x0059E830`).
- The total then grows by `m_count × [+0xE0]` (`0x0059E83C`-`0x0059E843`), and its fourth argument keeps the
  largest such a (`0x0059E832`-`0x0059E839`). It returns 0 after the last list (`0x0059E852`).
- `0x0059D6A0` sizes and allocates each list's objects. A list whose class has no runtime counterpart
  is skipped with a log line (`0x005CDAA0`, level 2, the format at `0x00D26D50`, which names the class and
  says it is skipped, `0x0059D74C`), written in the sizing walk for every such list; when its class carries
  flag `0x04`, the allocation walk then returns 6 (`0x0059D836`-`0x0059D840`).
- For a list with runtime descriptor D it takes `o = m_count × s`, s being D's instance size `+0x38`, and
  `p = ((m_arraysSize + 0x17) & ~7) + h + 8 × m_pointersInArraysCount`, where h is `m_objectsSize - o`
  for a header class (D `+0xFC` bit `0x4`) and 0 for any other (`0x0059D753`-`0x0059D781`).
- When D's word `+0xE0` is not 0, p becomes `(p + a - 1) & ~(a - 1)` for a non-zero a, D's word `+0xE4`,
  and then `p + m_count × [+0xE0]` (`0x0059D784`-`0x0059D7A8`).
- The block size is built list by list as `t = ((t + b - 1) & ~(b - 1)) + p + o`, b being D's alignment
  `+0x3C` (`0x0059D7AB`-`0x0059D7BB`); `0x0063DD30(cluster, t, t, m_instanceListCount)` is called only when t
  is not 0 (`0x0059D7D1`-`0x0059D7E5`).
- The allocation walk takes each list's record from `0x006394E0(cluster, m_count, D, p)`, `0xD` when that
  gives null, clears the record's byte `+0x7D` and stores the record in the list's slot of the array at
  `+0x48`; a skipped list's slot gets null (`0x0059D8AB`-`0x0059D8C2`). It returns 0 (`0x0059D8D6`).
- `0x0063DD30` allocates the cluster's one block (alignment `0x20`): a `0x20`-byte header, the objects' size
  rounded up to 8 and one `0x80`-byte list record per list. It links the block on the cluster's
  chain at `+0x48` and gives the records to its pool at `+0x50` (`0x00680100`); a second block gets
  `0x16`.
- `0x0059F500` reads each list's `m_objectsSize` bytes into a scratch buffer and its `m_arraysSize`
  bytes straight into the list's array area, 9 on a short read; a skipped list's `m_size` bytes are
  passed over.
- `0x0059D590` converts every object: `0x00599670` fills each with its runtime class's default instance,
  then `0x0059B090` copies each member present in both the file and the runtime class from its file
  position to its runtime position. A header class (runtime flag bit `0x4`) also keeps the bytes after
  its file size, up to `m_objectsSize`.
  - When the load context's byte `+0x18` is set it then runs the runtime
  class's descriptor slot `+0x00` forwards over every object (`0x0059FDB0(descriptor, objects, count, 1)` at
  `0x0059D674`), the byte-order walk of [reflection](phyre-reflection.md). It returns `0x13` for an out-of-range or
  unbound class and `0x11` when the list has no object area.
  - The objects handed to `0x0059FDB0` start at `objects + [D+0xF8] - [D+0xF4]` (`0x0059D659`-`0x0059D671`). A
    class is unbound when its table entry's file record `+0x08` or runtime descriptor `+0x10` is null
    (`0x0059D5D9`-`0x0059D5ED`). A header class's tail is copied with `0x00861EBA` from the file size
    `[record+4] & 0x0FFFFFFF` on (`0x0059D631`-`0x0059D64E`). Every other path returns 0 (`0x0059D67E`).

### User fixups

`0x0059E880` reads the user-fixup data and the 12-byte records (`0x00597130`). Each record's type is a
type-table or class entry; one without a bound descriptor returns `0x13`. A `PAssetReferenceImport`
record (descriptor `0x02D3E780`) is kept as raw bytes; any other is resolved through its descriptor
(`0x0063DC30`). A null result is logged (`"Resolving fixup for '%s' returned NULL pointer"`, with a hex
dump of data under 32 bytes) and the load goes on.

### Header classes and the fixup tables

- `0x0059D940` reads the header-class words and the 16-byte child records (`0x00597070`) and fixes up
  the header-class objects and their child objects, logging a child whose class has no runtime
  version and a runtime class larger than the file's.
- Four header classes carry arrays after their fixed part, and their static initialisers (`0x001605C0`,
  `0x001615C0`, `0x00167DB0`, `0x001688F0`) clear flag `0x2` and set `0x4` at `+0xFC` (`0x001615C0` sets `0x8` as
  well; the other three clear it) and store a function at descriptor `+0x100` that hands each array to
  the visitor with its element type: through its slot `+0x08`, or through `+0x10` with a second location.
- Each initialiser first calls a builder on its descriptor, then stores the descriptor's vtable, the
  function and the flags, and ends with a tail jump to `0x00808B90` that hands over an exit routine:
  `0x001605C0` builds `0x02CADB40` with `0x005A8400`, vtable `0x00D2B768`, function `0x005BFF30`, exit `0x008A8F20`;
  `0x001615C0` builds `0x02CB7480` with `0x005D9B30`, vtable `0x00D3BC30`, function `0x005FE350`, exit `0x008AB0B0`.
- `0x00167DB0` builds `0x02E5E430` with `0x006CFDB0`, vtable `0x00D8B050`, function `0x006D4CF0`, exit `0x008B7150`;
  `0x001688F0` builds `0x02EA0850` with `0x006D9F00`, vtable `0x00D8DFA8`, function `0x006DA380`, exit `0x008B78B0`.
  Each exit routine stores another vtable at the descriptor (`0x00D2B298`, `0x00D3ADA8`, `0x00D8AE20`,
  `0x00D8DE98`) and jumps to `0x00633390`.
- `0x006D4CF0` serves `PModifierNetworkInfoPacket` (`0x20` bytes), and does nothing when the visitor's
  slot `+0x18` answers true: `+0x04` modifier codes and `+0x08` modifier instances (`0x20` bytes
  each), then `+0x0C` + `+0x0E` two-byte buffer entries.
- All three go through slot `+0x08` with the types `0x02E5E130`, `0x02E5E230` and `0x02E5E330`, starting at
  `0x20`, `0x20 × (1 + c)` and `0x20 × (1 + c + i)` from the packet for c codes and i instances; an
  array whose count is 0 is not handed over (`0x006D4D32`-`0x006D4DB9`).
- `0x006DA380` serves `POccluderGeometryObject` (`0x30` bytes): `(+0x00 + 3) / 4` `Matrix4`, then
  `+0x04` `Point3`, then `+0x08` × 4 bytes.
- It does not call the visitor's slot `+0x18` and hands all three through slot `+0x08` whatever the
  counts: q = `(+0x00 + 3) / 4` records of the type `0x006B08A0` returns at `0x30`, then `+0x04` of the
  type `0x006B0B20` returns at `0x30 + 64 × q`, then `+0x08 × 4` entries of `PUInt8` (`0x01F2E460`, size 1,
  from `0x0062FFC0`) at `16 × (3 + 4 × q + n)` for n = `+0x04`, all from the object (`0x006DA39B`-`0x006DA435`).
- On its first call, under the guard `0x02CF94FC`, `0x0062FFC0` only registers the exit
  teardown `0x008AFE10` with `0x00808B90`; every call answers the address `0x01F2E460`
  (`0x0062FFDF`-`0x00630020`).
- `0x005BFF30` serves `PAnimationClipBinding` (`0x08` bytes), and does nothing when the visitor's slot
  `+0x18` answers true: `(+0x06 + 3) & ~3` two-byte entries at `+0x08` (the type `0x006300A0` returns),
  then `+0x02` + `+0x04` four-byte `PAnimationClipBindingChannelMap` records, both through slot `+0x08`
  (`0x005BFF6B`-`0x005BFFF4`).
- It then hands, from the next 8-byte boundary, `+0x02` `PAnimationClipBindingDataBlockCache` records
  through slot `+0x10`; the second location is `(e + a - 1) & ~(a - 1)`, the end of the two arrays rounded up to
  the alignment a the visitor's `+0x08` object answers for that type (its slot `+0x18`, `0x005BFFF8`-`0x005C0058`),
  with e = `8 + 2 × ((+0x06 + 3) & ~3) + 4 × (+0x02 + +0x04)`.
- The first location is an address rounded up to 8 (`0x005C002F`-`0x005C0041`); the second is an offset rounded up and
  added to the record (`0x005C002C`-`0x005C0049`).
- `0x005FE350` serves `PParameterBuffer` (`0x20` bytes), and does nothing when slot `+0x18` answers true:
  for each of the `+0x10` (mask `0x7FFFFFFF`) `PShaderParameterDefinition` records at `+0x18`, `0x18` bytes
  each, it hands one parameter to slot `+0x10` at the record's `+0x10` offset into the buffer
  (`0x005FE3C7`-`0x005FE40A`).
- A parameter type `+0x02` of `0x42`-`0x44`, `0x47`-`0x49` or `0x4B`-`0x50` is one `PShaderParameterCaptureBuffer`
  record: `0x42` Texture2D, `0x43` Texture3D, `0x44` TextureCubeMap, `0x47` Sampler, `0x48`
  StructuredBuffer, `0x49` RWStructuredBuffer, `0x4B` ByteAddressBuffer, `0x4C` RWByteAddressBuffer, `0x4D`
  RWTexture2D, `0x4E` RWTexture3D, `0x4F` DataBlock, `0x50` IndexDataBlock (`0x005FE40D`-`0x005FE651`).
- `0x4A` is one `PShaderParameterCaptureConstantBuffer` (`0x005FE575`-`0x005FE59A`).
- Any other parameter is `+0x00` (or 1) times the 1, 2, 3, 4, 12 or 16 elements of the basic type its
  data type `+0x03` selects through the type getters `0x0062FF50`-`0x006301F0`, each behind a thread-safe static
  (`0x005FE656`-`0x005FE7E5`);
  a data type with no descriptor is logged by name through `0x005CDAA0` with the format at `0x00D4A688`
  (`0x005FE802`-`0x005FE81C`).
- The second location is the same record's `+0x10` offset in the array the visitor's `+0x08` object
  returns for `+0x18` through its slot `+0x20`, when that array's class is or derives from
  `PShaderParameterDefinition` (`0x005D8EB0`).
- Without that array the second location is the first, and both are null unless the offset is at least 4
  and offset plus size (mask `0x1FFF` of `+0x12`) lies within `+0x00`, both as unsigned compares
  (`0x005FE36F`-`0x005FE40A`).
- `0x0059CE30`, `0x0059C700` and `0x0059C250` then read the pointer-array, pointer and array tables. Each
  reads its `*Size` bytes and decodes every list's share into fixed entries (16 bytes for array and
  pointer-array entries, `0x1C` for pointer entries; `0x00595EF0`, `0x00596890`, built on the 7-bit
  varint reader `0x00597400`), so a size is a packed byte length and a count an entry count.
- `0x0059FF40` reads an entry's two varints; the first has its low bit moved to bit `0x80000000`.
- The entries patch pointers and arrays inside the converted objects. One that names a member the
  runtime lacks is logged (`"Unable to find a data member in class '%s' offset at %d bytes"`).
- An entry names an object by instance list and index. `0x0063BFA0` turns that into the object's
  address plus the class's layout base `+0xF8`, or null when the index is not below the list's
  count (`+0x70`) or the slot lies on the list's chain at `+0x10`.

### D3D11 data and completion

`0x00686DE0` reads the index buffer into the cluster's `PIndexDataBlockD3D11` and `PMeshSegmentD3D11`
objects, the vertex buffer into its `PDataBlockD3D11` objects, and then texture data for each
`PTexture2D`, `PTexture3D` and `PTextureCubeMap` through a staging buffer sized from
`m_maxTextureBufferSize`. `0x0059E300` then marks every list loaded (`+0x7D`), calls slot `+0x70` of the
`PAssetReference` and `PClassDescriptorDynamic` descriptors for their lists (a non-zero result ends the
load), and runs `0x0059F7A0`, which builds the cluster's `PMapPair` records.

`0x0059F7A0` keeps those records in a local ordered map: a tree head with a `PMapPair` pool of
`0x28`-byte nodes `0x30` bytes after it (`0x0067FFB0`). It clears the map on return; when an exception
leaves it, the unwind action `0x00597F30` does the same: it resets the head's links (`0x0067F6F0`),
frees the pool's blocks (`0x006803D0`, `0x00680030`) and calls `0x0067F580` on the head twice.

For the `PClassDescriptorDynamic` lists, `0x0059BDC0` finds the `0x30`-byte class entry whose `+0x10`
is a given descriptor. `0x00686DE0` steps through the objects with `0x00686D40`, which skips the slots on a list's chain at
`+0x10` and moves to the next list when one is used up. `0x00670070` creates each ring buffer of a
loaded `PDataBlockD3D11` as an immutable buffer (bind flags 9, misc flags `0x20`) of the block's data
size, initialised from the file data at the block's offset; 9 when creation fails.

`0x0059E300` starts by zeroing its `0x28`-byte list cursor (`0x00686C20`). When it returns, `0x0059E070` frees the four arrays at `+0x20`–`+0x58` of the load record it passed
(`0x00597F80`). `0x0059FC20` copies the text between two pointers into new memory with `0x005994A0`
(alignment 2) and terminates it; 5 when the end lies before the start, `0xD` without memory.

### Asset references and idmaps.txt

Every `.phyre` file has a `PAssetReference` list; a reference names the file's contents by an id string at
`+0x30`. These objects are kept in the asset-name registry at `0x01F2EA70` (see the memory page under
Related).

- The constructor `0x006753A0(reference, name, a, b)`, called by the descriptor's construct slot
  `0x00674BE0`, sets up the node at `+0x08`, copies the name (`0x001C26B0`), stores `a` and `b` at
  `+0x38` and `+0x40`, clears `+0x48` and calls the registration `0x00677BA0`, whose result it drops
  (`0x00675403`-`0x00675409`).
- `0x00677BA0` registers a named reference only: with `+0x30` at 0 it returns `0x15` before it touches the
  node, the hash or the registry (`0x00677BBF`-`0x00677BD2`). The one call of the constructor (`0x00674C2A`)
  passes a null name (`0x00674C25`), which `0x001C26B0` answers with 0 (`0x001C26B9`-`0x001C2713`), so that
  reference is not registered.
- It points the node's three links at `+0x08` itself, clears the key's 32-bit hash `+0x20` and name
  `+0x28`, keeps the copy at `+0x30` and returns the reference (`0x006753C6`-`0x00675409`).
- For a loaded list, slot `+0x70` (`0x00674B50`) runs `0x00676450`: each reference gets the list's
  cluster at `+0x48`, its name hash (`0x00677350`, seed `0x7B5`) and name in its key, and is inserted
  under the lock `0x02D3E880`. A reference without a name returns `0x15` and a name already
  registered `0x12`, which ends the load.
- `0x00676450` steps through the list's `+0x70` objects from `+0x58` by the instance size `+0x38` of the
  descriptor at `+0x50` (`0x00676476`-`0x00676486`). The name is the pointer at `+0x30` with bit `0x1`
  cleared (`0x006764B4`-`0x006764BF`); the cluster is stored before that test (`0x006764B0`).
- The key is the hash at `+0x20` and the name at `+0x28`, after the node at `+0x08` is pointed at itself
  again (`0x006764C8`-`0x006764E7`). On first use, under the guard `0x02D3EC9C`, the registry anchor
  `0x01F2EA70` gets its six links pointed at itself and the exit routine `0x008B1C00` goes to `0x00808B90`
  (`0x0067650C`-`0x0067656D`).
- Under the lock (`0x005CD4F0`, released by `0x005CD820`), `0x006750C0` looks the reference up, a hit giving
  `0x12`; on a miss `0x006750C0` itself links the node at the end of its walk (`0x0067516D`-`0x0067517F`) and
  `0x0067F700` rebalances the tree (`0x006764FA`-`0x006765A4`). After the last reference it returns 0
  (`0x006765D2`).
- The registry orders keys with `0x00675EF0`: by hash, then, when both names contain `#`, by the text
  after the last `#` (case-sensitive) and then by the part before it (length first, then
  case-insensitive), and otherwise by the whole names case-insensitively.
- `0x00675EF0` compares the hashes unsigned (`0x00675F05`-`0x00675F1A`), finds the last `#` with `strrchr`
  (`0x00675F38`, `0x00675F4A`) and compares the suffixes byte by byte (`0x00675F70`-`0x00675F86`). It calls
  `_strnicmp` for equal-length prefixes and `_stricmp` for whole names with the second key's name first
  (`0x00675F8D`-`0x00675FB2`, `0x00675FD7`-`0x00675FDF`), so those two return the reverse of a first-key compare.

`0x00676BD0(id)` finds a reference by id. On first use it loads
`/GameData/D3D11/ArtData/shared/idmaps.txt` into a map of id pairs with `0x00677030` (alternate CRLF
lines as key and value) and registers its teardown `0x008B1B10`. An id found as a key is replaced by
its value; the result is hashed and looked up in the registry (`0x00674F60`) under the same lock.
`0x0063B040`, which works through a cluster's `PAssetReferenceImport` lists, and `0x00677CE0` call it.

The map is a guarded local static of `0x00676BD0` at `0x02D3ECA8` (guard `0x02D3ECE0`, `_Init_thread_header` at
`0x00676C44`), laid out like the thread-name map of [runtime services](../Compiler-And-C-Runtime/runtime-services.md):

- `+0x08`, `0x02D3ECB0`, and `+0x10`, `0x02D3ECB8`: the anchor's two links, both set to the anchor.
- `+0x18`, `0x02D3ECC0`: the root, set to 0.
- `+0x20`, `0x02D3ECC8`: the colour byte, set to 0 (`0x00676C54`, an 8-byte store, then `0x00676C7E`, one byte).
- `+0x28`, `0x02D3ECD0`: the count, set to 0 (`0x00676C84`).
- `+0x30`, `0x02D3ECD8`: the plain EASTL allocator vtable `0x008F6500`.

The byte `0x02D3ECA0` records that `idmaps.txt` has been loaded (`0x00676CA2`-`0x00676CAA`). The search walks from the
root and treats the anchor as "not found":

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02D3ECB0` | `void*` | 0 (zero-filled tail of `.data`) | the map anchor's first link, which the constructor points at the anchor itself | `0x00676BD0` (`0x00676C69`); the tree code through the map's address (`0x00676CB1` to `0x00677030`, which hands it to `0x00675580`) | `0x00676BD0` forms its address as the search's end (`0x00676C28`, `0x00676D85`); the tree code, as for its stores |
| `0x02D3ECC0` | `void*` | 0 (zero-filled tail of `.data`) | the map's root node, 0 while empty | `0x00676BD0`, 0 (`0x00676C77`); the tree code, as for `0x02D3ECB0` | `0x00676BD0` (`0x00676CF9`), where the search starts; the teardown `0x008B1B10` (`0x008B1B1D`), which hands it to `0x001A49C0` |
| `0x02D3ECD8` | `void*` | 0 (zero-filled tail of `.data`) | the map's allocator, the plain vtable `0x008F6500` | `0x00676BD0` (`0x00676C62`) | the node allocation in the tree code, through the map's address (`0x00676CB1` to `0x00677030`, which hands it to `0x00675580`) |

The map is a tree of `std::string` pairs: `0x00675580` returns the value for a key, inserting an empty
one when the key is missing; `0x00677AD0` finds the first node not below a key; `0x00675300` copies a
pair and `0x00675440` destroys one.


## Modding notes

- Keep the header little-endian with `RYHP`, 84, `11XD` and physics 0. A header taken from another
  platform's release is refused at the platform check.
- Every size and count must match the bytes that follow: the loader reads straight through and a
  wrong size shifts everything after it. Recompute `m_totalDataSize`, each list's `m_size`, and the
  header's fixup counts as the sums over the lists.
- The namespace must satisfy the size identity, with `+0x18` and `+0x1C` zero.
- A class or member the file declares and the game does not register is dropped with a log line;
  data in it is lost silently. Flag `0x04` on such a class turns the drop into a refusal.
- Edit fixup tables only with a decoder for the packed form; their sizes are byte lengths, not entry
  counts.
- A texture's two user fixups name its class and its format by string; the format name decides how
  the image bytes are read.
- An asset id listed as a key in `idmaps.txt` is looked up under its value instead, so one line pair
  redirects every import of that id; a later pair with the same key replaces an earlier one. The id and its value are copied into a
  256-byte buffer without a bound, so both must stay under 256 bytes.
- The path hash `0x00674A00` adds each byte as a signed char, so a path byte of `0x80` or above
  subtracts: "× 33 plus each byte" holds for ASCII paths only. Every shipped path is ASCII; a modded
  path with non-ASCII bytes hashes to a different value than an unsigned reading gives.
- A map scene's mesh instance is matched to a YM00 record, and given its draw objects, only when its name
  `m_name` (`+0x80`) is longer than eight characters, its ninth character starts a decimal number and that
  number is below the pack's record count (`0x001A624C`-`0x001A630A`; [Map art](../World-Areas-And-Travel/map-art.md#matching-models-to-instances)).
  The number picks the record, so a replacement scene keeps each instance's `nodename<N>` name.
- A replacement `chr/` or `chr_shadow/` mesh needs, for each segment, a stream of every render data type
  that the passes of its material's variant define, in its vertex blocks or its dynamic mesh's streams
  ([`phyre-asset-files-shader-pass-streams-chr.tsv`](phyre-asset-files-shader-pass-streams-chr.tsv)); a type
  left open stops that segment's draw and the instance's later ones (`0x0060A010`, `0x0060BF33`).
- The match compares render data types only, and the input layout takes each element's format from the
  variant's vertex program (`0x0061E0B0`), so each stream keeps the format of the shipped stream of its type.
  Keep one stream per block, as every shipped block has: when the segment's word `+0x28`, cleared at
  construction (`0x0065EA5D`), is below a block's stream count, the match tries only the stream at that index.

## Related

- [Prefetch and asset-header manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md): the `.ah` lists that name the `.phyre` files and file their load requests.
- [Texture animation lists](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md): frame lists that bind already loaded `.phyre` textures.
- [File path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md): how an asset path becomes an archive file.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the asset-name registry at `0x01F2EA70` that holds the asset references.
- [Phyre entities and components](phyre-entities-and-components.md): the entity and component hooks behind slot `+0x70`.
- [`phyre-asset-files-user-fixup-census.tsv`](phyre-asset-files-user-fixup-census.tsv): how many shipped `.phyre`
  files have each pair of user-fixup record count and user-fixup data size, by kind of file (`mesh`, `texture` or
  `neither`), with one example path (239 rows).

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 25 calls with 2 other topics</summary>

**Sound and music**

| Function | | Functions |
|---|---|---|
| `0x001BA860` | is called by | `0x002120E0` |
| `0x002124C0` | is called by | `0x00212050`, `0x00212300` |
| `0x005CD4F0` | is called by | `0x00212050`, `0x002120E0`, `0x00212300`, `0x00219C40`, `0x0021B290`, `0x00220C70`, `0x00220CE0`, `0x00220D40`, `0x00221140`, `0x002211B0`, `0x00221220` |

**Sound and music** (explained on [audio manager](../Sound-And-Music/audio-manager.md))

| Function | | Functions |
|---|---|---|
| `0x005CD820` | is called by | `0x00212050`, `0x002120E0`, `0x00212300`, `0x00219C40`, `0x0021B290`, `0x00220C70`, `0x00220CE0`, `0x00220D40`, `0x00221140`, `0x002211B0`, `0x00221220` |

</details>
