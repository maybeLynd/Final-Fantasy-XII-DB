---
title: "PhyreEngine asset files: the .phyre cluster header, the packed namespace, the instance data and how the loader reads and fixes up a cluster"
kind: "format"
category: "PhyreEngine"
summary: "The .phyre file that holds every model, texture, shader and animation of the remastered art: the 84-byte cluster header, the packed namespace that names every class and field the file uses, the instance lists, user fixups, header-class tables, packed fixup tables and D3D11 buffers in stream order, the loader that checks the header, binds the file's schema to the engine's registered classes and converts each object to its runtime layout, and a census of all 35,984 shipped files."
addresses: ["0019CB20", "00637C50", "0059E070", "0059A3B0", "0059A6F0", "0059C180", "00686D00", "0069E780", "0059D550", "02CA9D90", "0059AAE0", "0059B430", "00599500", "0059AC00", "0059E300", "0059E780", "0059D6A0", "0059F500", "0059D590", "0059E880", "0059D940", "0059CE30", "0059C700", "0059C250", "00686DE0", "02CAA0A0"]
---

# PhyreEngine asset files: the .phyre cluster header, the packed namespace, the instance data and how the loader reads and fixes up a cluster

## What the player sees

Every character, monster, weapon, map, texture, shader and font of the remastered art is drawn from
`.phyre` files. When one is malformed the game does not crash and does not report it: the asset is
simply missing, or a texture or model part fails to appear.

## Where it comes from

The files sit in the archive under `gamedata/d3d11/artdata/`, as `<name>.dae.phyre` for scenes and
meshes, `<name>.dds.phyre` for textures and `<name>.fx.phyre` for shaders. The `.ah` lists beside them
name, in order, the files each model, map or font loads.

A load request of kind 1 from such a list reaches `0019CB20(manager, path)` through `001A07B0`. It
hashes the path (`00674A00`: 5381, × 33 plus each byte, masked to 31 bits) and looks it up in the
manager's loaded set. A hit raises the entry's reference count and returns the loaded cluster; a miss
loads the file through `00637C50` and records it.

`00637C50` opens the path as a `PStreamReaderFile` (`00597970`),
returns 1 for a null path and 10 when the file does not open, and then calls the cluster reader
`0059E070` repeatedly, one cluster after another, until the stream position reaches the file size.
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

Twenty-one `u32` fields. `005983E0` registers the first eighteen as `PClusterHeaderBase`,
`00598C50` the last three as `PClusterHeaderD3D11`, and `00598DF0` the nine of `PInstanceListHeader`;
the namespace of every file declares the same names in the same places.

```
+0x00  u32  m_phyreMarker              0x50485952, the bytes "RYHP"
+0x04  u32  m_size                     header length, 84
+0x08  u32  m_packedNamespaceSize      bytes of namespace that follow
+0x0C  u32  m_platformID               0x44583131, the bytes "11XD"
+0x10  u32  m_instanceListCount
+0x14  u32  m_arrayFixupSize           packed bytes of the array fixup table
+0x18  u32  m_arrayFixupCount          its decoded entries, the sum over the lists
+0x1C  u32  m_pointerFixupSize
+0x20  u32  m_pointerFixupCount
+0x24  u32  m_pointerArrayFixupSize
+0x28  u32  m_pointerArrayFixupCount
+0x2C  u32  m_pointersInArraysCount    the sum over the lists
+0x30  u32  m_userFixupCount
+0x34  u32  m_userFixupDataSize
+0x38  u32  m_totalDataSize            the sum of the lists' m_size
+0x3C  u32  m_headerClassInstanceCount
+0x40  u32  m_headerClassChildCount
+0x44  u32  m_physicsEngineID          0, or 0x424C4C54 ("TLLB")
+0x48  u32  m_indexBufferSize
+0x4C  u32  m_vertexBufferSize
+0x50  u32  m_maxTextureBufferSize
```

### The instance-list header

```
+0x00  u32  m_classID                  1-based position in the namespace's class table
+0x04  u32  m_count                    objects in the list
+0x08  u32  m_size                     m_objectsSize + m_arraysSize
+0x0C  u32  m_objectsSize
+0x10  u32  m_arraysSize
+0x14  u32  m_pointersInArraysCount
+0x18  u32  m_arrayFixupCount          this list's share of each fixup table
+0x1C  u32  m_pointerFixupCount
+0x20  u32  m_pointerArrayFixupCount
```

### The packed namespace

The namespace is the file's own schema: every type, class and member it uses, by name. Its layout is
the one the byte-swap routine `0059C180` walks (eight header words, then `nTypes` words, `nClasses`
nine-word records and `nMembers` six-word records) and the one the validator `0059E070` checks.

```
+0x00  u32  bom                        0x01020304, stored 04 03 02 01
+0x04  u32  size                       equals m_packedNamespaceSize
+0x08  u32  nTypes
+0x0C  u32  nClasses
+0x10  u32  nMembers
+0x14  u32  poolSize                   bytes of the string pool
+0x18  u32  reserved                   zero
+0x1C  u32  extraSize                  bytes of the block after the pool
+0x20  u32[nTypes]                     pool offsets of the type names
       class record  x nClasses        9 words each
       member record x nMembers        6 words each
       char[poolSize]                  NUL-terminated names
       byte[extraSize]                 indexed by class word 8
```

The loader requires `size == 0x20 + extraSize + 4 × (nTypes + 9 × nClasses + 6 × nMembers) + poolSize`
(`0059E070`), which places the extra block after the pool.

```
class record
+0x00  u32  parent                     1-based class index of the base class, 0 for a root
+0x04  u32  fileSize                   low 28 bits: bytes per object in the file
+0x08  u32  name                       pool offset
+0x0C  u32  memberCount                the class's records, taken in order from the member table
+0x1C  u32  flags                      0x01 dynamic class, 0x04 header class
+0x20  u32  extra                      1-based offset into the extra block, 0 for none

member record
+0x00  u32  name                       pool offset
+0x04  u32  type                       below nTypes: type-table index; else nTypes + 1-based class index
```

The same two-table reference, a type index below `nTypes` and otherwise `nTypes` plus a 1-based class
index, is used by the user-fixup records.

### User-fixup records

```
+0x00  u32  type                       type or class reference, as in a member record
+0x04  u32  size                       bytes of its data
+0x08  u32  offset                     into the user-fixup data
```

The data is usually a name: the class name a `PClassDescriptor` fixup resolves, or the format name of
a texture.

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
| file end | every mesh file ends exactly after its index and vertex buffers, every all-zero file at the end of its array table; in a texture file the image bytes exceed `m_maxTextureBufferSize` in 33,705 and equal it in 89 |

## Loader behaviour

### Preconditions

`0059E070` returns `0x15` when the byte `02CA9D90` is zero and `0xB` when the stream is not open. The
byte is set by `0059D550`, which registers the cluster-header and instance-list classes; it is slot 1
of the module vtable `00D26C40`, a module that static-initialiser code links into the module list
(`0016035C` stores the vtable), and the engine's start-up `005A08E0` calls slot 1 of every listed module before any asset loads.
Slot 2 of the same vtable, the module's shutdown `0059FE20`, clears the byte again at `0059FF14`; after
the shutdown walk `0059E070` returns `0x15` again.

### The header check

`0059A3B0` is the only header reader; its one caller `0059E070` seeds the buffer with `RYHP` and 84,
zeroes the rest and passes platform checking as the constant 1.

1. It reads 84 bytes; fewer returns 9.
2. If the marker is not `RYHP` it byte-swaps the whole header (`0063E2E0` with descriptor
   `02CAA0A0`) and tests again: still wrong returns 6; right sets the swapped flag, so a big-endian
   file is accepted.
3. It calls `00686D00` (`0x44583131`) and `0069E780` (`0x424C4C54`); a different platform, or a physics
   id that is neither Bullet nor 0, returns 6.
4. It gives the namespace buffer `m_packedNamespaceSize` bytes (`0xD` when that fails) and returns 6
   when the buffer is null, which is what a zero-size namespace leaves.
5. With `m_size` 84 it reads the namespace (`0059A6F0`: one read, 9 when short, then `0059C180` when
   the file was swapped). A shorter header takes the surplus already read as the start of the
   namespace (6 when the surplus is larger than the namespace); a longer one is read on into a
   second buffer (`0xD`, 9).

`0059E070` then requires the byte-order mark and the size identity, or returns 6.

### Binding the schema

- `0059AAE0` allocates one table entry per type (`0x18` bytes), class (`0x30`) and member (`0x38`).
- `0059B430` finds each type and class name in the engine's registry (`006373D0`, keyed by a hash of
  1973, × 33 plus the low five bits of each byte), sets each class's parent from word 0, and matches
  each member to the runtime class's member of the same name, walking its bases.
- Names the registry lacks are logged
  (`"Unable to find type '%s' on load"`, `"File refers to compiled class '%s' which does not exist
  in the current runtime"`) and do not stop the load.
- `00599500` finds the class bound to `PClusterHeader` (`0x13` when none), converts the header
  through the file's schema, and checks the platform again (6).
- `0059AC00` builds a dynamic class (`00632E80`) for each class record with flag `0x01` and no
  runtime class, under its parent; one left unbuilt returns `0x13`.

### Reading the instance data

`0059E300` runs the rest in stream order.

- `00686D10` copies the three D3D11 sizes into the load record, and `0059E780` reads the list
  headers (`00596FC0`), returning 6 for a `m_classID` outside the class table.
- `0059D6A0` sizes and allocates each list's objects. A list whose class has no runtime counterpart
  is skipped with a log line, unless its class carries flag `0x04`, which returns 6.
- `0059F500` reads each list's `m_objectsSize` bytes into a scratch buffer and its `m_arraysSize`
  bytes straight into the list's array area, 9 on a short read; a skipped list's `m_size` bytes are
  passed over.
- `0059D590` converts every object: `00599670` fills each with its runtime class's default instance,
  then `0059B090` copies each member present in both the file and the runtime class from its file
  position to its runtime position. A header class (runtime flag bit 2) also keeps the bytes after
  its file size, up to `m_objectsSize`.

### User fixups

`0059E880` reads the user-fixup data and the 12-byte records (`00597130`). Each record's type is a
type-table or class entry; one without a bound descriptor returns `0x13`. A `PAssetReferenceImport`
record (descriptor `02D3E780`) is kept as raw bytes; any other is resolved through its descriptor
(`0063DC30`). A null result is logged (`"Resolving fixup for '%s' returned NULL pointer"`, with a hex
dump of data under 32 bytes) and the load goes on.

### Header classes and the fixup tables

- `0059D940` reads the header-class words and the 16-byte child records (`00597070`) and fixes up
  the header-class objects and their child objects, logging a child whose class has no runtime
  version and a runtime class larger than the file's.
- `0059CE30`, `0059C700` and `0059C250` then read the pointer-array, pointer and array tables. Each
  reads its `*Size` bytes and decodes every list's share into fixed entries (16 bytes for array and
  pointer-array entries, `0x1C` for pointer entries; `00595EF0`, `00596890`, built on the 7-bit
  varint reader `00597400`), so a size is a packed byte length and a count an entry count.
- The entries patch pointers and arrays inside the converted objects. One that names a member the
  runtime lacks is logged (`"Unable to find a data member in class '%s' offset at %d bytes"`).

### D3D11 data and completion

`00686DE0` reads the index buffer into the cluster's `PIndexDataBlockD3D11` and `PMeshSegmentD3D11`
objects, the vertex buffer into its `PDataBlockD3D11` objects, and then texture data for each
`PTexture2D`, `PTexture3D` and `PTextureCubeMap` through a staging buffer sized from
`m_maxTextureBufferSize`. `0059E300` then marks every list loaded (`+0x7D`), calls slot `+0x70` of the
`PAssetReference` and `PClassDescriptorDynamic` descriptors for their lists (a non-zero result ends the
load), and runs `0059F7A0`, which builds the cluster's `PMapPair` records.

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
- The path hash `00674A00` adds each byte as a signed char, so a path byte of `0x80` or above
  subtracts: "× 33 plus each byte" holds for ASCII paths only. Every shipped path is ASCII; a modded
  path with non-ASCII bytes hashes to a different value than an unsigned reading gives.

## Related

- [Prefetch and asset-header manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md): the `.ah` lists that name the `.phyre` files and file their load requests.
- [Texture animation lists](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md): frame lists that bind already loaded `.phyre` textures.
- [File path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md): how an asset path becomes an archive file.
