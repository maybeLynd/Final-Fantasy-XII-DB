---
title: "PhyreEngine asset files: the .phyre cluster header, the packed namespace, the instance data and how the loader reads and fixes up a cluster"
kind: "format"
category: "PhyreEngine"
addresses: "0x0019CB20, 0x00637C50, 0x0059E070, 0x0059A3B0, 0x0059A6F0, 0x0059C180, 0x00686D00, 0x0069E780, 0x0059D550, 0x02CA9D90, 0x0059AAE0, 0x0059B430, 0x00599500, 0x0059AC00, 0x0059E300, 0x0059E780, 0x0059D6A0, 0x0059F500, 0x0059D590, 0x0059E880, 0x0059D940, 0x0059CE30, 0x0059C700, 0x0059C250, 0x00686DE0, 0x02CAA0A0, 0x00676450, 0x00675EF0, 0x00676BD0, 0x006753A0, 0x00675580, 0x006D4CF0, 0x006DA380, 0x005BFF30, 0x005FE350, 0x001605C0, 0x001615C0, 0x00167DB0, 0x001688F0"
---

## What the player sees

Every character, monster, weapon, map, texture, shader and font of the remastered art is drawn from
`.phyre` files. When one is malformed the game does not crash and does not report it: the asset is
simply missing, or a texture or model part fails to appear.

## Where it comes from

The files sit in the archive under `gamedata/d3d11/artdata/`, as `<name>.dae.phyre` for scenes and
meshes, `<name>.dds.phyre` for textures and `<name>.fx.phyre` for shaders. The `.ah` lists beside them
name, in order, the files each model, map or font loads.

A load request of kind 1 from such a list reaches `0x0019CB20(manager, path)` through `0x001A07B0`. It
hashes the path (`0x00674A00`: 5381, × 33 plus each byte, masked to 31 bits) and looks it up in the
manager's loaded set. A hit raises the entry's reference count and returns the loaded cluster; a miss
loads the file through `0x00637C50` and records it.

`0x00637C50` opens the path as a `PStreamReaderFile` (`0x00597970`),
returns 1 for a null path and 10 when the file does not open, and then calls the cluster reader
`0x0059E070` repeatedly, one cluster after another, until the stream position reaches the file size.
Each cluster gets its own `0xA0`-byte container, chained through `+0x98`.

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
| `+0x20` | `u32[nTypes]` | pool offsets of the type names | class record  x nClasses        9 words each member record x nMembers        6 words each char[poolSize]                  NUL-terminated names byte[extraSize]                 indexed by class word 8 |

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
| `+0x20` | `u32` | extra | 1-based offset into the extra block, 0 for none |

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
| `+0x70` | `u32` | m_offsetInVertexBuffer where the block's data starts in the file's vertex buffer: 0x00670070 | creates the block's immutable buffer from the file data at this offset (`0x006700C1`); m_offsetInVertexBuffer (u32), registered by `0x00665870` (`0x00632960` at `0x00665A03`); the cluster loader binds it by name (`0x0059B430`) in the 2,091 shipped .phyre files that declare PDataBlockD3D11 |
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
| `+0x08` | `u32` | m_modifierInstanceCount the number of 0x20-byte modifier-instance records after the codes: | `0x006D4CF0` reads it (`0x006D4D1A`); m_modifierInstanceCount (u32), registered by `0x006D1810` (`0x00632960` at `0x006D198B`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x0C` | `u16` | m_inputCount | counted with m_outputCount for the two-byte buffer entries after the instances: `0x006D4CF0` reads it (`0x006D4D11`); m_inputCount (u16), registered by `0x006D1810` (`0x00632960` at `0x006D19FE`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x0E` | `u16` | m_outputCount | counted with m_inputCount for the two-byte buffer entries: `0x006D4CF0` reads it (`0x006D4D22`); m_outputCount (u16), registered by `0x006D1810` (`0x00632960` at `0x006D1A71`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x14` | `u32` | m_totalPersistentStateSize m_totalPersistentStateSize (u32), registered by 0x006D1810 (0x00632960 | at `0x006D1B56`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x18` | `u32` | m_totalStateBlockSize | m_totalStateBlockSize (u32), registered by `0x006D1810` (`0x00632960` at `0x006D1BC9`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |
| `+0x1C` | `u32` | m_spuModifierCodeSize | m_spuModifierCodeSize (u32), registered by `0x006D1810` (`0x00632960` at `0x006D1C3C`); the cluster loader binds it by name (`0x0059B430`) in the 3 shipped .phyre files that declare PModifierNetworkInfoPacket |

`POccluderGeometryObject` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_planeCount | the plane count: `0x006DA380` hands (count + 3) / 4 Matrix4 records of planes to the visitor (`0x006DA3A0`); m_planeCount (u32), registered by `0x006D9FC0` (`0x00632960` at `0x006DA051`); no shipped .phyre file declares POccluderGeometryObject |
| `+0x04` | `u32` | m_vertexCount | the vertex count: `0x006DA380` hands that many Point3 records to the visitor (`0x006DA3D4`); m_vertexCount (u32), registered by `0x006D9FC0` (`0x00632960` at `0x006DA0C0`); no shipped .phyre file declares POccluderGeometryObject |
| `+0x08` | `u32` | m_edgeCount | the edge count: `0x006DA380` hands that many 4-byte entries to the visitor (`0x006DA3FE`); m_edgeCount (u32), registered by `0x006D9FC0` (`0x00632960` at `0x006DA12F`); no shipped .phyre file declares POccluderGeometryObject |
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
| D3D11 sizes | texture only 33,794; index and vertex, no texture 2,091; all zero 99; none mixes vertex and texture |
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
| `idmaps.txt` | `gamedata/d3d11/artdata/shared/idmaps.txt`: 4,061,418 bytes, 75,624 CRLF lines, 37,812 key and value pairs, every key distinct and none equal to its value; no `#` in any line |
| file end | every mesh file ends exactly after its index and vertex buffers, every all-zero file at the end of its array table; in a texture file the image bytes exceed `m_maxTextureBufferSize` in 33,705 and equal it in 89 |

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

## Loader behaviour

### Preconditions

`0x0059E070` returns `0x15` when the byte `0x02CA9D90` is zero and `0xB` when the stream is not open. The
byte is set by `0x0059D550`, which registers the cluster-header and instance-list classes; it is slot 1
of the module vtable `0x00D26C40`, a module that static-initialiser code links into the module list
(`0x0016035C` stores the vtable), and the engine's start-up `0x005A08E0` calls slot 1 of every listed module before any asset loads.
Slot 2 of the same vtable, the module's shutdown `0x0059FE20`, clears the byte again at `0x0059FF14`; after
the shutdown walk `0x0059E070` returns `0x15` again.

### The header check

`0x0059A3B0` is the only header reader; its one caller `0x0059E070` seeds the buffer with `RYHP` and 84,
zeroes the rest and passes platform checking as the constant 1.

1. It reads 84 bytes; fewer returns 9.
2. If the marker is not `RYHP` it byte-swaps the whole header (`0x0063E2E0` with descriptor
   `0x02CAA0A0`) and tests again: still wrong returns 6; right sets the swapped flag, so a big-endian
   file is accepted.
3. It calls `0x00686D00` (`0x44583131`) and `0x0069E780` (`0x424C4C54`); a different platform, or a physics
   id that is neither Bullet nor 0, returns 6.
4. It gives the namespace buffer `m_packedNamespaceSize` bytes (`0xD` when that fails) and returns 6
   when the buffer is null, which is what a zero-size namespace leaves.
5. With `m_size` 84 it reads the namespace (`0x0059A6F0`: one read, 9 when short, then `0x0059C180` when
   the file was swapped). A shorter header takes the surplus already read as the start of the
   namespace (6 when the surplus is larger than the namespace); a longer one is read on into a
   second buffer (`0xD`, 9).

`0x0059E070` then requires the byte-order mark and the size identity, or returns 6.

`0x0059C180` swaps the namespace of a big-endian file in place: its eight header words, every word of
the type-name table (`0x0059A8B0`), the nine words of every class record (`0x0059A780`) and the six
words of every member record. The string pool is left as it is.

### Binding the schema

- `0x0059AAE0` allocates one table entry per type (`0x18` bytes), class (`0x30`) and member (`0x38`).
- `0x0059B430` finds each type and class name in the engine's registry (`0x006373D0`, keyed by a hash of
  1973, × 33 plus the low five bits of each byte), sets each class's parent from word 0, and matches
  each member to the runtime class's member of the same name, walking its bases. A class name is
  also looked up in the tree passed as its third argument (`0x0059BE00`, by each entry's descriptor
  name).
- Names the registry lacks are logged
  (`"Unable to find type '%s' on load"`, `"File refers to compiled class '%s' which does not exist
  in the current runtime"`) and do not stop the load.
- `0x00599500` finds the class bound to `PClusterHeader` (`0x13` when none), converts the header
  through the file's schema, and checks the platform again (6).
- `0x0059AC00` builds a dynamic class (`0x00632E80`) for each class record with flag `0x01` and no
  runtime class, under its parent; one left unbuilt returns `0x13`.

### Reading the instance data

`0x0059E300` runs the rest in stream order.

- `0x00686D10` copies the three D3D11 sizes into the load record, and `0x0059E780` reads the list
  headers (`0x00596FC0`), returning 6 for a `m_classID` outside the class table.
- `0x0059D6A0` sizes and allocates each list's objects. A list whose class has no runtime counterpart
  is skipped with a log line, unless its class carries flag `0x04`, which returns 6.
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
- `0x006D4CF0` serves `PModifierNetworkInfoPacket` (`0x20` bytes), and does nothing when the visitor's
  slot `+0x18` answers true: `+0x04` modifier codes and `+0x08` modifier instances (`0x20` bytes
  each), then `+0x0C` + `+0x0E` two-byte buffer entries.
- `0x006DA380` serves `POccluderGeometryObject` (`0x30` bytes): `(+0x00 + 3) / 4` `Matrix4`, then
  `+0x04` `Point3`, then `+0x08` × 4 bytes.
- `0x005BFF30` serves `PAnimationClipBinding` (`0x08` bytes), and does nothing when the visitor's slot
  `+0x18` answers true: `(+0x06 + 3) & ~3` two-byte entries at `+0x08` (the type `0x006300A0` returns),
  then `+0x02` + `+0x04` four-byte `PAnimationClipBindingChannelMap` records, both through slot `+0x08`
  (`0x005BFF6B`-`0x005BFFF4`).
- It then hands, from the next 8-byte boundary, `+0x02` `PAnimationClipBindingDataBlockCache` records
  through slot `+0x10`; the second location is the end of the two arrays rounded up to the alignment the
  visitor's `+0x08` object answers for that type (its slot `+0x18`, `0x005BFFF8`-`0x005C0058`).
- `0x005FE350` serves `PParameterBuffer` (`0x20` bytes), and does nothing when slot `+0x18` answers true:
  for each of the `+0x10` (bits 0-30) `PShaderParameterDefinition` records at `+0x18`, `0x18` bytes
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
  and offset plus size (bits 0-12 of `+0x12`) lies within `+0x00`, both as unsigned compares
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
  `+0x38` and `+0x40`, clears `+0x48` and registers the object (`0x00677BA0`).
- For a loaded list, slot `+0x70` (`0x00674B50`) runs `0x00676450`: each reference gets the list's
  cluster at `+0x48`, its name hash (`0x00677350`, seed `0x7B5`) and name in its key, and is inserted
  under the lock `0x02D3E880`. A reference without a name returns `0x15` and a name already
  registered `0x12`, which ends the load.
- The registry orders keys with `0x00675EF0`: by hash, then, when both names contain `#`, by the text
  after the last `#` (case-sensitive) and then by the part before it (length first, then
  case-insensitive), and otherwise by the whole names case-insensitively.

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

## Related

- [Prefetch and asset-header manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md): the `.ah` lists that name the `.phyre` files and file their load requests.
- [Texture animation lists](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md): frame lists that bind already loaded `.phyre` textures.
- [File path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md): how an asset path becomes an archive file.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the asset-name registry at `0x01F2EA70` that holds the asset references.
- [Phyre entities and components](phyre-entities-and-components.md): the entity and component hooks behind slot `+0x70`.
