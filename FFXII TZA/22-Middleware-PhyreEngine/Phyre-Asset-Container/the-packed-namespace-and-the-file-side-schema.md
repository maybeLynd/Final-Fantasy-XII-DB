---
system: The packed namespace — every .phyre file carries its own schema
category: 22-Middleware-PhyreEngine
status: AUDITED
owner_layer: CodeDomain:Phyre.AssetContainer; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  project: work/headless_gn160/GFZ_GN160, CHECKPOINT VERIFIED 2026-09-07
corpus_validated: "169 / 169 extracted .phyre files — 0.47 % of the 35,984 shipped"
last_reviewed: 2026-09-07
audit:
  passes: 1
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-self-attack
  last_pass_kind: attack
  crossref_clean: true
  reopened_count: 0
---

# The packed namespace — every `.phyre` file carries its own schema

> **Open any asset file in the game in a hex editor, skip 84 bytes, and it will tell you — in plain
> ASCII — every class and every field it contains.** A texture names `PTexture2D` and
> `m_maxTextureBufferSize`; a mesh names `m_skeletonMatrices` and `m_vertexData`.
>
> **The schema is not something you have to reverse. It is shipped inside every one of the 35,984
> files.**

## 1. What the player sees

Nothing directly — but this is the difference between guessing at a model format and reading it.

Phyre stores its data the way a program stores objects, and it writes down what those objects are
called. **Every asset file begins with its header, and immediately after the header comes a block
that lists the names of every class in that file and every field of every class**, as ordinary text.

For anyone editing FFXII's models, textures or animations, that means **the file tells you what it
is**. A character mesh declares that it has a skeleton, a default pose, skin bones, mesh segments and
vertex data — by those names — before you have decoded a single byte of the data itself.

And it is a **checkable** list. If your rebuilt file no longer declares what it used to declare,
something is wrong long before the game refuses it.

## 2. Native mechanism

### Where it is, and how the game reads it

The packed namespace occupies **bytes `[m_size, m_size + m_packedNamespaceSize)`** — immediately
after the cluster header documented in
[`the-cluster-header-and-what-the-loader-rejects.md`](the-cluster-header-and-what-the-loader-rejects.md).
In every shipped file `m_size` is 84, so it starts at byte 84.

`FUN_0059A6F0` (116 B) is the whole reader:

```c
if (namespaceSize == 0 || buffer == NULL) return 0;

n = stream->vtbl[0x28](stream, buffer, namespaceSize);   /* one bulk read */
stream->bytesConsumed += n;
result = (n == namespaceSize) ? 0 : 9;                   /* 9 = truncated */

if (buffer && wasByteSwapped) FUN_0059C180(buffer);      /* fix up if big-endian */
return result;
```

> **It is a single bulk read of a self-describing blob** — no parsing, no validation, no bounds
> check beyond the length. The only failure it can report is a short read, with the same code `9`
> the header read uses. **Whatever the namespace contains, the loader has already accepted it by the
> time anything looks at it.**

The byte-swap call is the same `wasByteSwapped` flag the header validation set — so a big-endian
`.phyre` gets its namespace corrected in one pass, by `FUN_0059C180` — **read in §8, where it turns out to be the description of the table's layout.**

### The layout

```
+0x00  u32   0x01020304      byte-order mark, stored 04 03 02 01
+0x04  u32   namespaceSize   repeats m_packedNamespaceSize from the header
+0x08  ...   counts, then three regions and a string pool   -- DECODED IN SECTION 8
 tail  ...   a NUL-separated ASCII string pool
```

**Verified across the whole extracted corpus:**

| check | result |
|---|---|
| namespace begins `04 03 02 01` | **169 / 169** |
| word at `+0x04` equals `m_packedNamespaceSize` | **169 / 169** |

> **The byte-order mark is the namespace's own, separate from the header's `RYHP` marker.** Two
> independent endianness statements in the same file, four bytes and eighty bytes apart.

The string pool sits at the **end** of the block — in the sample texture, the first string begins at
offset `0x5BC` of a `0x8D7`-byte namespace, so **roughly the first two thirds are the table** and the
last third is text. **Section 8 decodes that table**; the mapping from a class to the `m_classID` an
instance list names ~~is the one part that remains open~~ is the class's 1-based position in that
table (`CX-2`, answered 2026-09-12 — see the open-questions list below).

### What the names are

The pool holds three kinds of token, in groups:

- **type names** — `PChar`, `PInt32`, `PUInt8`, `PUInt32`, `PString`, `PArray`, `PSharray`
- **class names**, alphabetically ordered — `PAssetReference`, `PBase`, `PClassDescriptor`,
  `PClusterHeader`, `PClusterHeaderBase`, `PClusterHeaderD3D11`, `PInstanceListHeader`,
  `PTexture2D`, `PTexture2DBase`, `PTexture2DD3D11`, `PTextureCommonBase`, `PTextureFormatBase`
- **field names**, in declaration order — `m_id`, `m_asset`, `m_assetType`, then the header's own
  fields

Census over 169 files: **107 distinct type/class names, 236 distinct field names, 42 other tokens.**

**Seventeen names appear in all 169 files** — the cluster-header trio, `PInstanceListHeader`,
`PClassDescriptor`, `PBase`, `PAssetReference`, `PString`, the five primitives, and the texture core
(`PTexture2D`, `PTexture2DBase`, `PTexture2DD3D11`, `PTextureCommonBase`, `PTextureFormatBase`).

The 42 "other" tokens are **not Phyre names at all** — `CD3D11_BLEND_DESC`,
`D3D11_RENDER_TARGET_BLEND_DESC`, `DepthWriteMask`, `StencilReadMask`, `CullMode`, `FillMode`,
`bool`, `float`. **Direct3D 11 state-description structures, by their Windows SDK names**, in 99 of
the 169 files.

> *Corpus census 2026-09-12 (FABLE, all 35,984 files):* **19 type-table names, 177 class names, 349
> field names** — the 169-file numbers above were a sample of about half the classes (`CW-4`). The
> "other" tokens are five D3D11 structures **reflected as classes with their SDK fields**, `float` /
> `bool` in the type table, and `Vector3` / `Matrix4` (`CW-5`); they appear in the 2,184 shader and
> mesh clusters.

### ⚠ The file's own schema confirms the header layout independently

The namespace of every shipped file lists, as plain text:

```
m_phyreMarker  m_size  m_packedNamespaceSize  m_platformID  m_instanceListCount
m_arrayFixupSize  m_arrayFixupCount  m_pointerFixupSize  m_pointerFixupCount
m_pointerArrayFixupSize  m_pointerArrayFixupCount  m_pointersInArraysCount
m_userFixupCount  m_userFixupDataSize  m_totalDataSize
m_headerClassInstanceCount  m_headerClassChildCount
```

> **That is the same field set recovered from the binary's reflection registrations at `005983E0`,
> from a completely independent source.** One list comes from the code that registers the fields; the
> other from the data files that use them. **Neither was derived from the other, and they agree.**

### The file schema against the runtime schema — a static join

[`../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md`](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
matches what the *binary registers* against what *files declare*. This is the same join taken from
the file side, over the namespace rather than over image strings:

| | count |
|---|---:|
| type/class names declared by the 169 files | **107** |
| of those, with at least one field registration in the binary | **68** |
| **declared by files, never registered** | **39** |
| — of which primitives, containers and base types | 10 |
| — of which enum-shaped (`*Type`, `*Switch`) | 7 |
| — **structural classes with no registered fields** | **22** |
| field names declared by the 169 files | **236** |
| of those, registered in the binary | **189** |
| **declared by files, never registered** | **47** |

**The 22 and the 47 are not scattered. They are one region of the engine:**

```
PDataBlock  PIndexDataBlock  PMaterialSet  PMeshSegmentContext  PSamplerState
PSamplerStateD3D11  PShaderComputeProgram  PShaderFragmentProgram(D3D11)
PShaderGeometryProgram(D3D11)  PShaderProgramBase  PShaderVertexProgram
PStreamInputLayoutD3D11  PTexture2D(D3D11)  PTextureCubeMap(D3D11)  PTextureFormatBase
```

```
m_vertexData  m_streams  m_streamBindings  m_meshSegments  m_meshInstances
m_skeletonMatrices  m_skinBones  m_skeletonBounds  m_currentPose  m_defaultPose
m_compiledCode  m_shaders  m_passes  m_entryPoints  m_parameterLocations  ...
```

> **Every one is mesh, skeleton, shader or D3D11 resource.** That document's §7 asks *"why the
> recovery's coverage falls off precisely at the shader and D3D11-resource boundary."* **This is the
> same boundary seen from the other side**: those classes' fields are declared in the files and are
> absent from the binary's reflection registrations.
>
> **The obvious reading — that platform resource classes are built by hand-written D3D11 code rather
> than by reflection-driven deserialisation — is a reading, not a result.** ~~No constructor for any of
> the 22 has been read.~~ What is established is the *correspondence*, not its cause.
>
> **Answered 2026-09-26 (FABLE, Claude Opus 5.5) (`CW-3`): the obvious reading is wrong, and "never registered" was a property
> of the census, not of the engine.**
> - **Why the census missed them.** The recovered field schema counts the call sites of one member registrar
>   only. The engine registers members through three more: the array-member form, which also installs the
>   array vtable, and two variants that build the member record through the same shared base. *((FABLE, Claude Opus 5.5, 2026-09-26): and
>   a fourth, `00632B30` (`PClassDataMemberDynamic`), used only at load time by the cluster loader `0059AC00`
>   through `006393A0` — see the CL-1 correction on
>   [the file schema against the runtime schema](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md).)*
> - **The fields.** Across all 35,984 files, the schema misses 85 of the 349 field names the files declare.
>   Every one of the 85 is registered at a site of those three: 64 array members (`m_vertexData`,
>   `m_meshSegments`, `m_skeletonMatrices` …), 5 by the second variant, and 16 by the third. The 16 include the
>   D3D11 state fields `DepthWriteMask`, `FillMode`, `CullMode`, the `Stencil*` and `*Blend*` fields, and
>   `m_primitiveType`.
> - **The classes.** They were answered on the image side: `CL-1`/`CL-2` on
>   [the file schema against the runtime schema](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
>   found 21 of the 22 with their own descriptors, and `PContextSwitch` a type-table entry.
> - **So these classes' members are reflected.** What the engine does with them after deserialisation, such as
>   creating the D3D11 resources, is a separate matter this does not address.
> - Control: [`cw3_field_registrars.py`](../../_index/candidates/cw3-field-registrars/cw3_field_registrars.py) (4 checks, FAILS 0).

**And the 47 unregistered field names are exactly what a model modder wants**: `m_vertexData`,
`m_skeletonMatrices`, `m_skinBones`, `m_defaultPose`, `m_meshSegments`. **The names are in the files
~~even though the engine's reflection never registers them~~.** *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5): the engine does
register them, as array members; the census counted one registrar. See the answer above.)*

## 3. Key addresses

| address | what | size |
|---|---|---:|
| `0059A6F0` | the packed-namespace reader — one bulk read | 116 B |
| `0059C180` | the namespace byte-swap fixup — **not read** | — |
| `0059A3B0` | the header validation that precedes it | 589 B |
| `005983E0` | registers the 18 `PClusterHeaderBase` fields the namespace also names | — |

## 4. Modding notes

- **The namespace is at byte 84 of every shipped `.phyre`**, and it is `m_packedNamespaceSize` bytes
  long. `04 03 02 01` then the size repeated is how you know you are in the right place.
- **The string pool is at the end of the block, not the start.** Roughly the last third.
- **Read the pool to identify a file** without decoding anything: a texture names `PTexture2D`, a
  mesh names `m_meshSegments` and `m_vertexData`, a shader names `m_compiledCode` and `m_passes`.
- **99 of 169 files name Direct3D state structures by their SDK names** — `CD3D11_BLEND_DESC`,
  `CullMode`, `DepthWriteMask`. If your file declares those, it carries render state.
- **The reader validates nothing but the length.** A corrupt namespace is not rejected here; it will
  fail later, somewhere less informative. **If a rebuilt asset fails mysteriously, check that
  `m_packedNamespaceSize` still matches the block you wrote.**
- **The byte-order mark is separate from the header's.** Both must agree with the data or the
  swap-fixup will run on already-correct bytes.

## 5. What is not known

- [x] ~~The table between `+0x08` and the string pool.~~ **DECODED — section 8.** Eight header words,
  then `nTypes` pool offsets, `nClasses` records of 9 words, `nMembers` records of 6 words, then the
  pool; the arithmetic closes to the byte in 169/169 files.
- [x] ~~`FUN_0059C180`, the byte-swap fixup — not read.~~ **READ — section 8, and it was the way in,
  exactly as `CW-2` predicted:** a routine that swaps a structure has to describe it.
- [x] ~~**The class→`m_classID` link.** The schema is fully reconstructable, but the number an instance
  list uses to name its class is still not tied to a class record. Two unidentified class words
  remain (`w0`, `w7`), and **`w0` is not a type-table index** — in range for only 6,199 of 9,203.~~
  **`CX-2` ANSWERED 2026-09-12 (FABLE): `m_classID` is the 1-based position of the class in the
  file's own class table, and `w0` is the 1-based position of the class's parent in the same table
  (0 = no parent).** On the `aircon_00…` texture the class table in file order is 1 `PAssetReference`,
  2 `PBase`, 3 `PClassDescriptor`, 4 `PClusterHeader`, 5 `PClusterHeaderD3D11`, 6 `PClusterHeaderBase`,
  7 `PInstanceListHeader`, 8 `PString`, 9 `PTexture2DD3D11`, 10 `PTexture2D`, 11 `PTexture2DBase`,
  12 `PTextureCommonBase`; the two instance-list headers that follow the namespace (file offset
  `0x92B`) carry `m_classID` **1** and **10** — the asset reference and the texture, the only two
  objects a texture cluster holds — and `w0` reads `PTexture2D` 9 → `PTexture2DD3D11` 11 →
  `PTexture2DBase` 12 → `PTextureCommonBase` 2 → `PBase` 0, and `PClusterHeader` 5 → `…D3D11` 6 →
  `…Base` 2 → `PBase` 0, which is PhyreEngine's real inheritance. **Over the whole archive** (35,984
  clusters, **212,329** instance lists, `tools/cx2_census.py`): every `m_classID` lies in
  `1..nClasses` and **none is 0** (so the numbering is 1-based, not 0-based — a 0-based reading would
  make the sample's ids `PBase`, an abstract root, and `PTexture2DBase`); every `w0` lies in
  `0..nClasses`, none is its own parent and no chain cycles; the ids name **59 distinct classes**, all
  concrete (`PParameterBuffer` 106,256 lists, `PAssetReference` exactly one per file = 35,984,
  `PTexture2D` 29,184, `PTextureCubeMap` 4,610, `PMaterial` / `PSamplerState` /
  `PShaderParameterDefinition` 2,184, `PMesh` and its seven companions 2,091, …); and the roots
  (`w0` = 0) are `PBase` in every file plus the value types that do not derive from it
  (`CD3D11_BLEND_DESC`, `CD3D11_DEPTH_STENCIL_DESC`, `CD3D11_RASTERIZER_DESC`, `D3D11_DEPTH_STENCILOP_DESC`,
  `D3D11_RENDER_TARGET_BLEND_DESC`, `PMatrix4`, `PMatrix4x3`, `Vector3`, `Matrix4`). The earlier
  "in range for only 6,199 of 9,203" was the type table's range, not the class table's. `w7` (0, 2, 8,
  12, 20, 32, 34, 40 — 20 added 2026-09-30, found in 5 records) is the one partly-identified class word:
  **bit 0 is the loader's dynamic-class flag, set on 0 shipped records** (`SD-65`); bits 1–5 stay
  unexplained.
- [x] ~~`PInstanceListHeader` is registered with ten fields and declared with nine.~~ **REFUTED the
  same day — the "tenth field" was my own grep artifact. Both sides say nine.** See the section above.
- [x] ~~**Member word 1**, the type reference. It indexes the type table correctly for primitives
  (`m_format`→`PTextureFormatBase`, `m_buffer`→`PChar`) and is out of range for others, so the
  encoding is **not** a plain index.~~ **`CX-3` ANSWERED 2026-09-12 (FABLE): one number over two
  tables.** A value below `nTypes` is a **0-based index into the type table**; a value at or above
  it is **`nTypes` + the class's 1-based `m_classID`** (the numbering `CX-2` established). On the
  sample (`nTypes` 5): `m_id` 13 → class 8 `PString`, `m_asset` 7 → class 2 `PBase`, `m_assetType` 8 →
  class 3 `PClassDescriptor`; `m_format` 2 → `PTextureFormatBase`, `m_memoryType` 3 → `PUInt8`,
  `m_textureFlags` 4 → `PInt32`, the eighteen header fields 0 → `PUInt32`. Over the archive
  (2,192,621 member records) **1,781,255 resolve to a type and 411,366 to a class; none equals
  `nTypes` and none is out of range**, and the resolved pairs are PhyreEngine's real field types —
  `PNode.m_parent` → `PNode`, `PMesh.m_meshSegments` → `PArray<PMeshSegment>`,
  `PArray<PMeshSegment>.m_els` → `PMeshSegment`, `PMaterial.m_parameterBuffer` → `PParameterBuffer`,
  `PShaderPassStateD3D11.m_blendDesc` → `CD3D11_BLEND_DESC`. So the "out of range" reading was the
  type table alone; the reference space is the type table followed by the class table.
- [x] ~~Four of the nine class words (`w4`, `w5`, `w6`, `w8`) are **zero in all 9,203 records**. Unused
  in this corpus, purpose unknown.~~ **CX-4 ANSWERED 2026-09-12 (FABLE) over the whole archive — and
  `w1` corrected.** Every shipped cluster's namespace was parsed from the VBF (35,984 files, all
  namespaces inside the first block; **684,244** class records; alignment proven by decoding the
  names through `w2` — `PAssetReference`, `PBase`, `PClassDescriptor`, `PClusterHeader`, … — and by the
  page's own `0x5BC` string-pool offset reproducing on the `aircon_00…` texture). **`w4`, `w5`, `w6`,
  `w8` are zero in 684,244 / 684,244**: the corpus cannot say whether the format reserves them or
  the exporter never fills them, but "unused in this title" is now a whole-archive fact. **`w1` is
  not "always 0"**: it is non-zero in **646,076** records (textures 371,742 / 33,794, meshes 266,880 /
  4,182, neither 7,454 / 192), and it is zero exactly where the class is a root or a descriptor — the
  sample's `PBase` carries 0, `PClassDescriptor` `0x40000000`. The value is packed: a kind in the top
  nibble (`0x2`, `0x3`, `0x4`) over a small number, and for the `0x2` family that number is **the
  class's instance size in bytes** — `PClusterHeader` `0x20000054` = 84 (the header), `PClusterHeaderBase`
  `0x20000048` = 72 (its 18 `u32`s), `PInstanceListHeader` `0x20000024` = 36 (its nine) — while the
  `0x3` family carries 1 (`PString`), 3 (`PAssetReference`), 5, 14, 22 (top corpus values
  `0x30000016` ×100,656, `0x30000005` ×79,270, `0x20000054` ×71,968, `0x3000000E` ×42,347). The
  member-record `w1` reading in the table below (a type reference) is a different column and
  unaffected. `w0`'s corpus values are small integers (2 ×207,185, 3 ×175,785, 0 ×53,436, 6, 11, 12,
  5, 9 …) and `w7`'s are 0, 8, 32, 2, 12, 34, 40 — recorded for `CX-2`.
- [x] **UQ-288.** *(SUPERSEDED in the register 2026-09-26, FABLE, Claude Opus 5.5: a duplicate; the open residue is carried by **CW-3**)* **Why 22 structural classes and 47 field names are declared by files and never registered.**
  The correspondence with the shader/D3D11 boundary is established; the cause is not. `CW-3`.
- [x] ~~Whether the 169-file name sets are representative of the 35,984. The namespace is cheap to read
  from an archive entry — 84 bytes plus one length — so this is answerable without extraction.~~
  **`CW-4` ANSWERED 2026-09-12 (FABLE): they were not.** Every namespace in the archive parsed
  (`ns_corpus.py`): **19 type-table names, 177 class names, 349 field names** against the sample's
  107 type/class and 236 field names — the sample held about half the classes and two thirds of
  the fields, because 169 files under-sampled meshes, shaders, animation and fonts. Joined against
  `phyre-field-schema.tsv`, **138 of 177 classes and 262 of 349 field names are in the recovered
  registration**; the 39 classes outside it are mostly classes that declare no fields of their own
  in the file (`PBase`, `PString`, `PTexture2D`, `PShaderPass`, `PMeshSegment`, …) plus the D3D11
  structures and the array/element holders, and the 87 fields outside it are dominated by array
  members (`m_els`, `m_u`, `m_meshSegments`, `m_skeletonMatrices`, …) and the D3D11 structure fields.
  **All 545 names are present in the binary as NUL-terminated strings** (`FFXII_TZA.exe`, 545 / 545),
  so no file declares a class or field the build does not know by name. Same question as `CU-4`.
- [x] ~~What the 42 non-Phyre tokens are doing in a Phyre namespace — whether D3D11 state structures
  are reflected as if they were Phyre classes, or merely named.~~ **`CW-5` ANSWERED 2026-09-12
  (FABLE): reflected as classes, with their real SDK members.** In the 2,184 shader and mesh
  clusters that carry a `PShaderPassStateD3D11`, `CD3D11_RASTERIZER_DESC`, `CD3D11_DEPTH_STENCIL_DESC`
  and `CD3D11_BLEND_DESC` are **class records** (root classes, `w0` = 0) with member records
  `FillMode`, `CullMode`, `FrontCounterClockwise`, `DepthBias`, `DepthBiasClamp`, `SlopeScaledDepthBias`,
  `DepthClipEnable`, `ScissorEnable`, `MultisampleEnable`, `AntialiasedLineEnable` (10);
  `DepthEnable`, `DepthWriteMask`, `DepthFunc`, `StencilEnable`, `StencilReadMask`, `StencilWriteMask`,
  `FrontFace`, `BackFace` (8); `AlphaToCoverageEnable`, `IndependentBlendEnable`, `RenderTarget` (3) —
  and `FrontFace` / `BackFace` reference a fourth class `D3D11_DEPTH_STENCILOP_DESC` (`StencilFailOp`,
  `StencilDepthFailOp`, `StencilPassOp`, `StencilFunc`), `RenderTarget` a fifth,
  `D3D11_RENDER_TARGET_BLEND_DESC` (`BlendEnable`, `SrcBlend`, `DestBlend`, `BlendOp`, `SrcBlendAlpha`,
  `DestBlendAlpha`, `BlendOpAlpha`, `RenderTargetWriteMask`). `PShaderPassStateD3D11.m_rasterDesc` /
  `m_depthDesc` / `m_blendDesc` point at the first three. `float` and `bool` sit in the **type
  table** beside `PUInt32`. That is the whole 42: five structure names, 33 field names, two primitive
  names, and the two non-`P` maths classes `Vector3` / `Matrix4` (each with one `m_elements`
  field). The exporter serialises the D3D11 state descriptions through the same reflection as
  everything else.

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| Namespace location and single bulk read | complete body of `0059A6F0` | 1 |
| Error 9 on short read; byte-swap on the header's flag | the same body | 1 |
| BOM `04 03 02 01`, self-size at `+0x04` | 169 / 169 shipped files | 1 |
| String pool at the tail, three token groups | the parsed pools of all 169 files | 1 |
| 107 type names / 236 field names / 42 other | per-file distinct-name census | 1 |
| 17 names in all 169 files | the same census | 1 |
| **The file's own schema names the 18 header fields** | the namespace string pool, against the registration bodies at `005983E0` — **two independent sources** | 1 |
| 68/107 and 189/236 registered | set join against the recovered member-registration dataset | 1 |
| The 22 and 47 cluster in shader/mesh/D3D11 | enumerated in full above | 1 |
| **Why they cluster there** | **not established — a reading, no constructor read** | 8 |
| Corpus is 0.47 % of shipped | the archive census's 35,984 `.phyre` entries | 3 |

## 7. Related

- [`the-cluster-header-and-what-the-loader-rejects.md`](the-cluster-header-and-what-the-loader-rejects.md)
  — the 84 bytes that precede this block, and the validation that runs first.
- [`../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md`](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
  — the same join from the image side; **its §7 shader/D3D11 question is answered here from the file
  side, as a correspondence.**
- [`../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`](../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md)
  — the registration mechanism the join compares against.
- [`README.md`](README.md) — the folder's `external`-disposition obligation.

## 8. The table decoded — 2026-09-07, later the same day

**`CW-1` and `CW-2` answered together, and `CW-2` predicted the method.** The byte-swap fixup
`FUN_0059C180` (202 B) has to know the table's layout to swap it, so **the swap routine is the
structure description written as code.** It is 202 bytes and it gives up everything.

### What the swap routine says

```asm
0059C186..0059C1C4   bswap the first EIGHT u32 individually        -> the header is 8 words
0059C1C7  mov eax,[rcx+8]      ; A
0059C1CA  add rax,8
0059C1CE  lea rdx,[rcx+rax*4]  ; &ns[8 + A]
0059C1D2  mov ecx,[rcx+0xc]    ; B
0059C1D5  call 0x59A780        ; swap B records there
0059C1DD  lea rcx,[rax+rax*8]  ; B * 9                 -> class records are NINE words
0059C1EB  lea rax,[rbx+rcx*4]  ; &ns[8 + A + 9B]
0059C1EF  mov ecx,[rbx+0x10]   ; C
0059C200..0059C230              ; loop C times, bswap SIX u32, rax += 0x18
0059C239  mov ecx,[rbx+8]      ; A
0059C23C  lea rdx,[rbx+0x20]   ; &ns[8]
0059C245  jmp 0x59A8B0         ; process A entries
```

### The layout

```
+0x00  u32       0x01020304                byte-order mark
+0x04  u32       namespaceSize             repeats m_packedNamespaceSize
+0x08  u32       nTypes
+0x0C  u32       nClasses
+0x10  u32       nMembers
+0x14  u32       stringPoolSize
+0x18  u32       0 in ALL 35,984 shipped files - no consumer at all (CX-5)
+0x1C  u32       0 in ALL 35,984 - sizes an optional block that never occurs (CX-5)
+0x20  u32[nTypes]                          string-pool offsets of type names
       class [9 words] x nClasses
       member[6 words] x nMembers
       char[stringPoolSize]                 NUL-separated names
```

> **`+0x1C` is a byte count the loader adds into this equation (2026-09-14, FABLE, narrows `CX-5`).** The
> namespace consumer `0059E070` accepts a namespace only when the byte-order mark matches (`0059E167`) and **`+0x04` ==
> `0x20` + `[+0x1C]` + 4 × (`nTypes` + 9 × `nClasses` + 6 × `nMembers`) + `stringPoolSize`** (`0059E173`–`0059E191`).
> So `+0x1C` is the size in bytes of one more optional block, zero in every shipped file. **`+0x18` takes no part in the
> check**: that consumer does not read it, and nothing else seen reads it beyond the byte swap. What the `+0x1C` block holds,
> and where in the layout it sits, is still open.

> **Confirmed by arithmetic, not by assertion:**
> `0x20 + 4*nTypes + 36*nClasses + 24*nMembers + stringPoolSize == m_packedNamespaceSize`
> holds in **169 / 169 files**, to the byte. Corpus totals: **1,649 type entries, 9,203 class
> records, 27,543 member records.**


## `CX-5` answered — the optional block never occurs, and `+0x18` has no consumer (FABLE, 2026-09-22)

**This page's layout above said *“0 in every file sampled”* for both words, and that wording was
stale against this subsystem's own contract.**
[`CONTRACT-phyre-packed-namespace.md`](CONTRACT-phyre-packed-namespace.md) §15 already carries the
full-archive census — *“BOM `0x01020304` in 35,984/35,984; `+0x18` = `+0x1C` = 0 in 35,984/35,984”*,
which is what closed `NS-2`. **The sample became the whole archive and this page never heard.**

### Reproduced independently, by a different route (FABLE, 2026-09-22)

The contract's census ran over every `.phyre` member of `FFXII_TZA.vbf` through `vbfextract.py`.
This one walks the **extracted tree** on disk instead and reads each cluster's namespace directly:

| | |
|---|--:|
| clusters read with **both** controls passing | **35,984** |
| rejected | **0** |
| files with `+0x18` non-zero | **0** |
| files with `+0x1C` non-zero | **0** |

*The two controls are per file and mandatory:* the BOM at `+0x00` must be `0x01020304` **and** the
size word at `+0x04` must equal the cluster header's `m_packedNamespaceSize`; a file failing either
is counted as unreadable rather than as a zero. **Two independent extraction routes agreeing to the
file is worth more than either alone**, and this is published as corroboration of the contract's
figure, not as a new one.

### What is new: `+0x18` is not read by anything (FABLE, 2026-09-22)

The contract establishes the *values*; it does not say who consumes them. **An image-wide scan for
the dword `0x01020304` finds exactly ONE site in `.text` — `0059E169`** — and it is the immediate
inside `0059E070`'s BOM test, the validator this page already documents. That body reads `+0x08`,
`+0x0C`, `+0x10`, `+0x14` and `+0x1C` in its size identity, and **never touches `+0x18`**.
`0059C180` byte-swaps it as one of the first eight words — but byte-ordering a word is not
consuming it.

> **So `CX-5` resolves in two halves.** **`+0x1C`** is the byte count of an optional block, and that
> block **never occurs**: it is 0 in all 35,984 shipped files, so *its contents and placement are
> not observable from this corpus at all* — the question's residue is unanswerable from shipped data
> rather than merely unanswered. **`+0x18`** is a reserved word with **no reader in the image**:
> swapped, never consumed, universally zero.

> **Scope, and the limit of the reader sweep.** The sweep finds every site carrying the BOM
> *constant*, so it enumerates the code that **validates** a namespace. **A body that reads the
> block without checking its BOM would not appear**, and nothing here excludes one; what is shown
> is that the only validating consumer ignores `+0x18`. **NATIVE/STATIC — image and shipped assets,
> nothing executed.**

### The records

Every column was tested by asking whether it lands on the **first byte of a NUL-terminated name**, in
every record of every file. One counter-example disqualifies a column.

| | class record (9 words) | member record (6 words) |
|---|---|---|
| **w0** | ~~not established — *not* simply an index into the type table (in range for only 6,199 of 9,203)~~ **1-based index of the parent class in this class table, 0 for a root (2026-09-12, `CX-2`)** — in range and acyclic in all 684,244 shipped records; `PTexture2D` → `PTexture2DD3D11` → `PTexture2DBase` → `PTextureCommonBase` → `PBase` | **name**, pool offset — 27,543 / 27,543 |
| **w1** | ~~always 0~~ **non-zero in 646,076 of 684,244 shipped records (2026-09-12)** — a packed word: kind nibble `0x2`/`0x3`/`0x4` over the class's instance size in bytes for the `0x2` family (84 / 72 / 36 for the three header classes); 0 for `PBase` | ~~a type reference; **region-A index for primitives** (`m_format`→`PTextureFormatBase`, `m_buffer`→`PChar`) but out of range for some records, **so not established**~~ **0-based type-table index when < `nTypes`, else `nTypes` + the class's 1-based `m_classID` (2026-09-12, `CX-3`)** — 2,192,621 / 2,192,621 resolve |
| **w2** | **name**, pool offset — 9,203 / 9,203 | ~~**byte offset of the field within the class**~~ **the byte offset in the class's file-side layout**. That layout is packed for 147 of 154 classes, so this is not the runtime offset (corrected 2026-09-26, FABLE; [contract §3](CONTRACT-phyre-packed-namespace.md), `members/w3_census.py`) |
| **w3** | **member count** | ~~element size in bytes (4 for a `u32`, 1 for a byte)~~ **the member's width in that layout**: 1 for an object pointer and 5 for a `PArray` in a packed class, 8 and 16 in the 6 native ones (corrected 2026-09-26, FABLE) |
| **w4** | always 0 | attribute word — ~~**bit 31 marks a pointer** (2,239 records set it)~~ **the reflection attribute word: bit 1 marks an object pointer, and bit 31 (2,239 records) marks the three counted-buffer members** *(corrected 2026-09-26, below)* |
| **w5** | always 0 | 0 in all but 342 records |
| w6, w7, w8 | w6 and w8 always 0; ~~w7 not established~~ **w7 bit 0 is the loader's dynamic-class flag** — set on 0 of 684,244 shipped class records (corrected 2026-09-30, `SD-65`); bits 1–5 not established (values 0, 2, 8, 12, 20, 32, 34, 40 corpus-wide — 20 found in 5 records, earlier list missed it) | — |

> **`sum(class[w3]) == nMembers` in 169 / 169 files.** Members are stored **contiguously in class
> order**, so class *i* owns the next `class[i].w3` member records. **That is the whole mapping**: the
> file's complete schema — every class, its fields, their offsets, sizes and pointer-ness — is
> reconstructable from the namespace alone.
> **Corrected 2026-09-26 (FABLE, Claude Opus 5.5): `w4` is the reflection attribute word, and bit 31 marks
> only the counted-buffer members.** Over the same 169 files, `w4` takes thirteen values:
>
> | `w4` | records | on |
> |---|---|---|
> | `0x00` | 8,529 | plain values (`Matrix4::m_elements`) |
> | `0x02` | 723 | object pointers (`PMaterial::m_effectVariant`) |
> | `0x08` | 4,896 | (`PClusterHeaderBase::m_phyreMarker`) |
> | `0x0A` | 60 | object pointers (`PMeshInstance::m_mesh`) |
> | `0x10` | 8,181 | (`PAssetReference::m_id`) |
> | `0x12` | 1,354 | object pointers (`PAssetReference::m_assetType`) |
> | `0x16` | 169 | `PAssetReference::m_asset` only |
> | `0x30` | 1,392 | enum-typed fields only: the fourteen D3D11 state enums (`FillMode`, `CullMode`, `DepthFunc`, the blend and stencil ops) and `PMeshSegmentBase::m_primitiveType` |
> | `0x80000000` | 1,446 | `PArray::m_els` |
> | `0x80000002` | 495 | `PArray::m_els` over pointer elements (`PArray<PSceneRenderPass *>`) |
> | `0x80000010` | 169 | `PString::m_buffer` |
> | `0x80000040` | 111 | `PSharray::m_u` |
> | `0x80000042` | 18 | `PSharray::m_u` over pointer elements (`PSharray<PMaterial *>`) |
>
> - **Bit 31 is set on exactly three members:** `PArray::m_els` (1,941), `PString::m_buffer` (169) and
>   `PSharray::m_u` (129). They total 2,239, the figure the table gives. Each is the pointer to a counted buffer.
> - **An object pointer carries bit 1, not bit 31.** 2,306 records set bit 1 without bit 31. On a bit-31 member,
>   bit 1 says the buffer's elements are pointers (513 records).
> - So *"bit 31 marks a pointer"* was true of every record that has it, but it cannot be used as the test for a
>   pointer. A walker that tested bit 31 would treat `m_effectVariant`, `m_mesh` and `m_asset` as inline values.
> - **The low bits are the runtime registration's attribute word, carried over.** Joining each member to
>   [the recovered field schema](../Reflection-And-Class-Metadata/phyre-field-schema.tsv) by class and member name
>   pairs 19,301 records over 248 fields. 18,934 carry exactly the runtime value, including every bits-3–4 value
>   (`0x08`, `0x0A`, `0x10`, `0x12`).
> - The 367 that differ are three fields. `PAssetReference::m_asset` adds bit 2 (runtime `0x12`, file `0x16`), and
>   `PShaderPassParameterLocationTypesBase::m_parameterStart` and `m_parameterCount` are `0x00` at runtime but
>   `0x10` in the file (99 each).
> - **Bits 5 and 6 appear only in files.** Bit 5, always with bit 4, is on enum-typed fields; bit 6 is only on
>   `PSharray::m_u`. The runtime census never sees either, because no resolved registration sets them. The enum
>   fields have no joined runtime row.
>
> The census is `members/bl1_file_vs_runtime.py`, beside this page (the join, with the `w4` vocabulary above
> recounted inline). It serves `BL-1` on the member-registration page: bits 3–4 are persisted into every shipped
> file's schema, not only held at run time.
>
> **Four of the nine class words are always zero across all 9,203 records.** Whatever they are for,
> this corpus does not use them.

### ⚠ A third independent confirmation of the header layout

`m_phyreMarker` 0, `m_size` 4, `m_packedNamespaceSize` 8, `m_platformID` 12, `m_instanceListCount`
16, … `m_physicsEngineID` 68 — **the member records' `w2` reproduces the byte offsets recovered from
the binary's reflection registrations at `005983E0`.**

> **3,042 offset checks over 169 files. Zero mismatches.**
>
> The header layout now rests on **three sources that could each have been wrong alone**: the code
> that registers the fields, the code that reads the file, and the files themselves.

### ⚠ A discrepancy this document reported, and then refuted the same day

**Published here hours earlier:** *"`PInstanceListHeader` is registered with ten fields and every one
of the 169 shipped files declares nine"* — filed as `CX-1`, with the practical warning that a tool
trusting the runtime layout would read four bytes that are not there.

**There is no discrepancy. Both sides say nine.** The registration site `00598DF0` has **nine** rows,
and the 169 files declare nine.

> **The tenth field was manufactured by my own grep.** The class's registrations were pulled with a
> case-insensitive search for `InstanceList`, which also matches **`m_instanceListCount` — a field of
> `PClusterHeaderBase`** — and that row was counted into this class's list.
>
> **This is worse than a miscount: it invented a finding.** A miscount makes a true statement
> imprecise; this created a conflict between two sources that agree, gave it a plausible cause
> ("the exporter predates the field"), and attached a warning to it. **Nothing downstream would have
> flagged it** — the number was self-consistent, the story was reasonable, and both documents
> repeated it.
>
> **The rule it earns: a class's field list must come from a search anchored on the class, not on a
> substring of its name.** `m_instanceListCount` and `PInstanceListHeader` share eleven characters
> and nothing else.

### A rebuilt schema, in full

The complete namespace of a shipped texture, reconstructed by the rules above — 12 classes, 41
members, all consumed exactly:

```
types: PUInt32 PChar PTextureFormatBase PUInt8 PInt32

PAssetReference       3   m_id +0  m_asset +1  m_assetType +2
PBase                 0
PClassDescriptor      0
PClusterHeader        0
PClusterHeaderD3D11   3   m_indexBufferSize +72  m_vertexBufferSize +76  m_maxTextureBufferSize +80
PClusterHeaderBase   18   m_phyreMarker +0 ... m_physicsEngineID +68
PInstanceListHeader   9   m_classID +0 ... m_pointerArrayFixupCount +32
PString               1   m_buffer +0        (attribute 0x80000010 - the pointer bit)
PTexture2DD3D11       0
PTexture2D            0
PTexture2DBase        2   m_width +14  m_height +18
PTextureCommonBase    5   m_format +0  m_memoryType +1  m_mipmapCount +2  m_maxMipLevel +6  m_textureFlags +10
```

**`m_buffer` is the only field in the file with attribute bit 31 set, and it is the one field that is
a pointer** — `PString`'s character buffer.

### Modding consequence

**A `.phyre` file can now be read without the game.** Parse the 84-byte header, take the namespace,
and you have every class in the file with every field's name, byte offset, size and pointer-ness —
which is the description you need to walk the instance lists that follow.

~~**What is still missing is the link from a class to the `m_classID` an instance list names.** The
class records carry two unidentified words (`w0`, `w7`); one of them is the likely candidate, and
`w0` is *not* a type-table index.~~ **Answered 2026-09-12 (`CX-2`): `m_classID` is the 1-based index
of the class in the file's class table, and `w0` is the same 1-based index for the class's parent
(0 for a root)** — so the instance list at `m_size + m_packedNamespaceSize` names its class by
counting class records, and the parent link gives each class its inherited members. Only `w7` is
still unidentified.

## Falsification pass — 2026-09-07, `xiionline-61`

**Self-attack, same day as authorship.** The session that wrote this document had a demonstrated
error rate, so its own claims were re-derived rather than re-read.

**The systematic attack:** every "only caller" / "N callers" statement in the day's four documents was
made with a scan that matched `E8 call rel32` only. **The CRT block later established that this
binary reaches things through `E9 jmp rel32` tail calls and import thunks**, so every one of those
claims was re-run against **both** instruction forms, and against `data_xref_scan.py` for
address-taken references (vtables, pointer tables) with a passing control.

### Result for this document — **one invented finding withdrawn**

| claim re-tested | result |
|---|---|
| `0059C180` has one caller (`0059A6F0`) | **stands** — 1 `call`, 0 `jmp`. |
| `0059A6F0` is called from the header validator | **stands** — 2 sites, matching the fast path and the version-shim path. |
| the layout arithmetic closes in 169/169 | **stands** |
| **"the binary registers ten `PInstanceListHeader` fields, files declare nine"** | **REFUTED — the registration site has nine.** The tenth came from a case-insensitive grep for `InstanceList` that also matched `m_instanceListCount`, a field of `PClusterHeaderBase`. **The "discrepancy" never existed.** Withdrawn in §8 and in `CX-1`. |

> **This was the worst error of the day because it did not make a true statement imprecise — it
> created a conflict between two sources that agree**, gave it a plausible cause and a practical
> warning, and put it in two documents. Nothing downstream would have caught it: the number was
> self-consistent and the story was reasonable.

**Not attacked:** the class→`m_classID` question (`CX-2`), the member type reference (`CX-3`), and the
representativeness of the 169-file corpus, all of which remain open exactly as §5 states.

`00598040` (172 B) is the four-vector teardown `005980F0`/`0059E070`/`0059FE20` call for the packed-file record: walks the `+0x38/+0x40`, `+0x28/+0x30`, `+0x18/+0x20`, `+0x08/+0x10` count/pointer pairs in that order; for each, when the count's high bit is clear (`shr 0x1f; not al; test 1` passes) and the pointer non-null it calls `00584730` (the dealloc), then clears both fields — so the high bit marks inline storage that is skipped.

Interior anchor `00598057` (function `00598040`).

`00597F80` (183 B) is the four-vector teardown sibling covering the upper half of the same record: `+0x50/+0x58`, `+0x40/+0x48` (this pair additionally requires the `btr 0x1f` count to exceed `1` before deallocating), `+0x30/+0x38`, `+0x20/+0x28`; identical `00584730` dealloc-and-clear pattern. Together with `00598040` it spans `+0x08..+0x58` — eight counted buffers.

Interior anchor `00597F97` (function `00597F80`).
