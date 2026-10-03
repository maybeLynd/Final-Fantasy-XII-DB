---
system: The .phyre cluster header, and what this build's loader rejects
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

# The `.phyre` cluster header, and what this build's loader rejects

> **Every model, texture, animation, shader and font in FFXII: The Zodiac Age is a `.phyre` file** —
> 35,984 of them, 72 % of the archive by size. This is the 84-byte header every one of them starts
> with, field by field, and the exact ladder of checks the game runs before it will touch the rest.
>
> **`AQ-1` said no Phyre function body had ever been read.** Four have now been read in full.

## 1. What the player sees

Nothing — until a mod is wrong, and then the asset simply does not appear. **The game does not
crash on a bad `.phyre` file and it does not say why.** It gives up at one of four checks and returns
a number nobody displays.

The four things it insists on:

- **The file must start with the four letters `RYHP`.** If it starts with `PHYR` instead — the same
  four letters the other way round — **the game does not reject it. It flips the whole header round
  and carries on.** That is a file built for a big-endian console, and this build reads it.
- **It must be built for DirectX 11.** The header names its platform, and a file built for the
  PlayStation version is refused here.
- **Its physics must be Bullet, or nothing at all.** Almost every shipped file says "nothing".
- **It must not be truncated.** A file that ends early fails on the read, not on the contents.

**A header from a different PhyreEngine version is *not* an automatic rejection.** The loader is
written to cope with headers both shorter and longer than the one it expects, which is why an asset
from another Phyre title may get further than you would guess before failing somewhere else.

## 2. Native mechanism

### The header — 21 unsigned 32-bit fields, 84 bytes

Recovered from the engine's **own reflection registrations**, which record a field's name, byte
offset and type for every serialized class — the mechanism documented in
[`../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`](../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md).
The registering functions are `005983E0` (`PClusterHeaderBase`, 18 fields) and `00598C50`
(`PClusterHeaderD3D11`, 3 more).

| offset | field | meaning |
|---|---|---|
| `+0x00` | `m_phyreMarker` | `0x50485952` — the bytes `R Y H P` |
| `+0x04` | `m_size` | size of this header; **84** in every shipped file |
| `+0x08` | `m_packedNamespaceSize` | bytes of the class-name namespace that follows |
| `+0x0C` | `m_platformID` | `0x44583131` — the bytes `1 1 X D` |
| `+0x10` | `m_instanceListCount` | how many instance lists the cluster holds |
| `+0x14` | `m_arrayFixupSize` | |
| `+0x18` | `m_arrayFixupCount` | |
| `+0x1C` | `m_pointerFixupSize` | |
| `+0x20` | `m_pointerFixupCount` | |
| `+0x24` | `m_pointerArrayFixupSize` | |
| `+0x28` | `m_pointerArrayFixupCount` | |
| `+0x2C` | `m_pointersInArraysCount` | |
| `+0x30` | `m_userFixupCount` | |
| `+0x34` | `m_userFixupDataSize` | |
| `+0x38` | `m_totalDataSize` | the object payload, excluding header and namespace |
| `+0x3C` | `m_headerClassInstanceCount` | |
| `+0x40` | `m_headerClassChildCount` | |
| `+0x44` | `m_physicsEngineID` | `0x424C4C54` (`T L L B`) or **0** |
| `+0x48` | `m_indexBufferSize` | **D3D11 subclass** — non-zero only for meshes |
| `+0x4C` | `m_vertexBufferSize` | **D3D11 subclass** — non-zero only for meshes |
| `+0x50` | `m_maxTextureBufferSize` | **D3D11 subclass** — non-zero only for textures |

**Every field is `unsigned int`** — each registration passes the same `PTypeDefault<unsigned int>`
singleton at `01F2E5A0`. The base class's 18 fields carry attribute word `8`; the three D3D11 fields
carry `0`.

> **`m_size` is the header's own length, and the shipped value is 84 — exactly `0x48` of base plus
> `0x0C` of D3D11 extension.** The schema predicts the number and the files state it. Neither was
> derived from the other.

### Each instance list then carries its own 36-byte header

`PInstanceListHeader`, registered at `00598DF0`, **nine** `unsigned int` fields — so the instance-list
header is **36 bytes**:

| offset | field |
|---|---|
| `+0x00` | `m_classID` |
| `+0x04` | `m_count` |
| `+0x08` | `m_size` |
| `+0x0C` | `m_objectsSize` |
| `+0x10` | `m_arraysSize` |
| `+0x14` | `m_pointersInArraysCount` |
| `+0x18` | `m_arrayFixupCount` |
| `+0x1C` | `m_pointerFixupCount` |
| `+0x20` | `m_pointerArrayFixupCount` |

> **Corrected 2026-09-07 (same day, audit pass).** This table first listed a tenth field,
> `m_pointerArrayFixupSize` at `+0x24`, and the heading said "40-byte header". **There is no such
> field.** It came from a case-insensitive grep for `InstanceList`, which also matched
> **`m_instanceListCount` — a field of `PClusterHeaderBase`** — and it was counted into this class's
> list. The registration site has **nine** rows. The 169 shipped files declare nine. See §8 of
> [`the-packed-namespace-and-the-file-side-schema.md`](the-packed-namespace-and-the-file-side-schema.md).

### The validation ladder — `0059A3B0`, read in full

```c
n = stream->vtbl[0x28](stream, hdr, 0x54);        /* read exactly 84 bytes */
stream->bytesConsumed += n;
if (n != 0x54) return 9;                          /* TRUNCATED */

*outWasByteSwapped = 0;
if (hdr->m_phyreMarker != 0x50485952) {           /* not 'RYHP' */
    ByteSwapBlock(&DAT_02CAA0A0, hdr, 1);         /* flip the whole header */
    if (hdr->m_phyreMarker != 0x50485952) return 6;   /* NOT A PHYRE FILE */
    *outWasByteSwapped = 1;                       /* it was big-endian; remember it */
}

if (checkPlatform && hdr->m_platformID != GetPlatformID())        return 6;   /* 0x44583131 */   // <- corrected 2026-10-02, OPUS - both GetPlatformID (0059A440) and GetPhysicsEngineID (0059A457) are called whatever checkPlatform says; only the compares are guarded (0059A44D, 0059A45C)
if (checkPlatform && hdr->m_physicsEngineID != GetPhysicsEngineID()
                  && hdr->m_physicsEngineID != 0)                 return 6;   /* 0x424C4C54 or 0 */

/* allocate m_packedNamespaceSize bytes; on failure: */
                                                                  return 0xD; /* OUT OF MEMORY */
```

~~**Four rejections, three distinct codes: `6` refuse, `9` truncated, `0xD` allocation failed.**~~ **Three distinct codes over nine rejection causes: `6` refuse, `9` truncated, `0xD` allocation failed.** *(corrected 2026-10-02, OPUS: in `0059A3B0` code `9` leaves at `0059A3E2` (short header read) and `0059A57A` (short tail read), `0xD` at `0059A524` and `0059A51A`, and `6` for five causes - bad magic `0059A421`, platform or physics mismatch `0059A46C`, null namespace buffer or short-header size mismatch `0059A598`; CONTRACT-phyre-cluster-header.md's return table)* Zero
is success. The enum is `Phyre::PResult` — a name this database already isolated under `AZ-3` — but
its symbolic values are not established, so the numbers are reported as numbers.
*(Checked 2026-09-14, FABLE, against the answered `AZ-3`: still true, and that answer explains why.)* `AZ-3`
identified `005A6670` as a lazy type descriptor that reflects `PResult` as `PTypeDefault<unsigned int>` (vtable
`00D311B0`): a name, a size and an alignment, no value names. A whole-file byte search finds no `PE_RESULT` string
(0 matches), so the symbolic names are not in the shipped binary to recover, and the numbers stay numbers.

> **The byte-swap branch is why searching the image for a second, byte-reversed marker finds nothing.**
> `0x52594850` (`PHYR`) occurs **zero** times in `.text`. There is no second constant because the
> loader **transforms the data and re-tests the same one.** A constant census would have concluded
> that this build refuses big-endian files; the body says it accepts them and sets a flag that rides
> along with the rest of the load.

**`GetPlatformID` (`00686D00`) and `GetPhysicsEngineID` (`0069E780`) are two-instruction constant
leaves:**

```asm
00686D00  b8 31 31 58 44   mov eax, 0x44583131   ; '11XD'  -> "DX11" read the other way
0069E780  b8 54 4c 4c 42   mov eax, 0x424c4c54   ; 'TLLB'  -> "BLLT" — Bullet
```

**The physics id is Bullet**, which is the physics engine this database's third-party inventory
already places in the build. `m_physicsEngineID == 0` is the explicit wildcard for a file that
carries no physics.

### The platform check is live, not vestigial

`0059A3B0` has exactly **one** caller, `0059E070` at `0059E153`, and it passes the `checkPlatform`
argument as a literal:

```asm
0059E0D7  mov  dword ptr [rbp - 0x40], 0x50485952   ; pre-seed marker  'RYHP'
0059E0DE  mov  dword ptr [rbp - 0x3c], 0x54         ; pre-seed m_size  84
0059E0E5  xor  r12d, r12d                           ; ...and zero the other 19 fields
0059E129  mov  byte ptr [rsp + 0x30], 1             ; checkPlatform = TRUE
0059E153  call 0x59a3b0
```

> **The caller fills the header buffer with a valid default before reading over it**, so a failed
> read leaves `RYHP`/84 rather than stack garbage. And **`checkPlatform` is the immediate `1`** —
> there is no configuration, no debug flag, and no second call site that passes `0`. **The platform
> and physics-engine checks always run.**

### Version tolerance, in both directions

When `m_size != 84` the loader does **not** give up:

- **`m_size < 84`** — the header is shorter than the 84 bytes already read, so the surplus is the
  start of the packed namespace. It is `memcpy`d out of the tail of the header buffer:
  `take = min(84 - m_size, m_packedNamespaceSize)`, and if `84 - m_size` exceeds the namespace size
  the file is refused with `6`.
- **`m_size > 84`** — a bigger buffer is allocated (`0xD` on failure), the 84 bytes already read are
  copied in ~~as 21 dwords~~ inline as ten `movups` (five 16-byte loads and stores) plus one dword *(corrected 2026-10-02, OPUS: `0059A536`-`0059A55F`; 84 bytes, no `memcpy` call)*, and `m_size - 84` further bytes are read; a short read returns `9`.
- **If the file was byte-swapped, the header is swapped *back*** before either path runs.

**Both paths are dead against shipped data** — all 169 files sampled report `m_size == 84`. They
exist for assets built by a different PhyreEngine version.

### The corpus

Every extracted `.phyre` file was checked against the recovered layout:

| field | value | files |
|---|---|---|
| `m_phyreMarker` | `RYHP` | **169 / 169** |
| `m_size` | 84 | **169 / 169** |
| `m_platformID` | `11XD` | **169 / 169** |
| `m_physicsEngineID` | 0 | **169 / 169** |

and the three D3D11 fields partition the corpus exactly as their names say:

| shape | files | reading |
|---|---:|---|
| index + vertex buffers, no texture | **6** | meshes |
| texture buffer only | **70** | textures |
| all three zero | **93** | everything else — shaders, animation, fonts, scene data |

> **No file has both a vertex buffer and a texture buffer.** The three sizes are not a generic
> capacity triple; they discriminate what kind of asset the cluster is.

> **CU-4 answered 2026-09-12 (FABLE): the uniformity holds over all 35,984, and the sample's
> proportions did not.** Every `.phyre` entry in `FFXII_TZA.vbf` was checked from its first
> compressed block alone (84 bytes each, no extraction): `m_phyreMarker` = `RYHP`, `m_size` = 84,
> `m_platformID` = `11XD` and `m_physicsEngineID` = 0 in **35,984 / 35,984**. The three D3D11 sizes
> partition the whole corpus as the sample said — **no file has both a vertex and a texture buffer**
> — but in shipped proportions the extracted 169 badly under-sampled textures: **33,794** texture-only
> (94 %), **2,091** meshes (index + vertex, no texture), **99** with all three zero (shaders, animation,
> fonts, scene data), 0 both. So the 93 "everything else" files of the sample are 99 in the whole
> archive — the sample held nearly all of them — while textures are 200× the sample's 70.

**The denominator matters: 169 files is 0.47 % of the 35,984 shipped**, and it is the same extracted
corpus [`../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md`](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
already warns is small and unrepresentative — 6 meshes against ~~2,097~~ 2,091 *(corrected 2026-10-02, OPUS: the mesh rows of `members/user-fixup-census.tsv` sum to 2,091 of 35,984, CU-4)* in the archive. **The uniformity
above is a property of the sample, not a proven property of the shipping data.**
*Superseded 2026-09-12 by the CU-4 answer directly above, which checked all 35,984 entries and found the uniformity
holds; noted 2026-09-26 (FABLE, Claude Opus 5.5), `PH-4`. The warning stands for the sample's PROPORTIONS, which
CU-4 shows it misjudged: textures are 94 % of the archive, not 41 % of the sample.*

## 3. Key addresses

| address | what | size |
|---|---|---:|
| `0059A3B0` | the header read and validation ladder | 589 B |
| `0059E070` | its only caller; sets `checkPlatform = 1` | 656 B |
| `0059A6F0` | reads the packed namespace — ~~**not read here**~~ *(answered: see CONTRACT-phyre-cluster-header.md, 0059A6F0 read in full; 2026-10-02, OPUS)* | 116 B |
| `00686D00` | `GetPlatformID` → `0x44583131` | 6 B |
| `0069E780` | `GetPhysicsEngineID` → `0x424C4C54` | 6 B |
| `005983E0` | registers the 18 `PClusterHeaderBase` fields | — |
| `00598C50` | registers the 3 `PClusterHeaderD3D11` fields | — |
| `00598DF0` | registers the ~~10~~ nine *(corrected 2026-10-02, OPUS: nine `00632960` calls, `0059904A` to `00599216`; the same row's nine-element battery)* `PInstanceListHeader` fields — interior verified 2026-09-17 (SWE2-FRONTIER): `006388C0` first at [`00598E0B`](../../_index/ADDRESS-INDEX.md), `008092FC`/`0080929C`/`00808B90`/`00632960` ×9 each — a nine-element registration battery | — |
| `00632960` | the one field-registration call every one of them uses | — |
| `01F2E5A0` | `PTypeDefault<unsigned int>` — the type of all 21 fields | — |
| `02CAA0A0` | byte-swap descriptor for the header | — |

## 4. Modding notes

- **The header is 21 little-endian `uint32`s, 84 bytes, then the packed namespace, then the data.**
  `m_packedNamespaceSize` is the namespace length; `m_totalDataSize` the payload.
- **`m_size` must be 84** for the fast path. Any other value sends the loader down a version-shim
  branch that no shipped file exercises — so it is the least-tested code you can reach.
- **Do not rewrite the marker.** `RYHP` is right for this build. Writing `PHYR` will *work*, via the
  byte-swap path, but every field then has to be big-endian too — the loader swaps the whole header
  and sets a flag that changes how the rest of the file is read.
- **`m_platformID` must be `11XD`.** A `.phyre` lifted from the PS4 or Vita release is refused at the
  header, before anything else is examined. This is the single most likely reason a cross-platform
  asset silently fails.
- **`m_physicsEngineID` should be 0** unless the cluster really carries Bullet data. `0` is a
  wildcard the loader accepts unconditionally; every shipped file uses it.
- **A truncated file fails differently from a malformed one** — `9` against `6` — but neither is
  shown, so from the outside both look like "the asset didn't load".
- **The three D3D11 sizes tell the loader how much ~~GPU~~ memory to reserve.** *(corrected 2026-10-02, OPUS: `00686D10` copies them into the load record and `00686DE0` allocates that many bytes (`00686E2C`-`00686E32`, `0017D260`) and reads them from the file (`00686E44`, `0059D510`); what the D3D11 side does with the buffers is not read here)* Get them wrong on a mesh
  or texture you have rebuilt and the failure will be downstream of every check documented here.

## 5. What is not known

- [x] **UQ-285.** **The packed namespace format.** `0059A6F0` (116 B) reads it and is **not read**. It is the
  bridge between a cluster's `m_classID` values and the class descriptors, so it is the next thing
  worth reading. `CU-1`. *(2026-09-14, FABLE: stale as worded. `0059A6F0` was read in full on
  [the packed namespace page](the-packed-namespace-and-the-file-side-schema.md) §2 ("the whole reader"), and the register
  records `CU-1` as answered in part; the remaining format questions are that page's.)*
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5), by three answers that were already on record.** The reader is read in
  full (`CU-1`, the namespace page §2). The table is decoded (`CW-1`, 2026-09-07): 8 header words, the type
  offsets, 9-word class records, 6-word member records and the pool, exact in 169 of 169 files. The bridge this box
  asks for is `CX-2` (2026-09-12): an instance list's `m_classID` is the 1-based position of its class in the file's own
  class table. What stays open about the format is the class word `w7`'s bit names, which is
  [the namespace contract](CONTRACT-phyre-packed-namespace.md)'s `NS-1`.
- [x] **UQ-286.** *(closed 2026-09-18, at the end of this item)* **`Phyre::PResult`'s symbolic values.** `0`, `6`, `9` and `0xD` are observed; the enum name is
  known from `AZ-3`; no mapping from name to number is established.
  **ANSWERED 2026-09-18 (FABLE) as NO ADMISSIBLE SOURCE for the names; the meanings stand as read.** The question asks for source-level identifiers, and nothing this project admits as evidence contains them: the executable reflects `PResult` as `PTypeDefault<unsigned int>` - a name, a size and an alignment, no enumerators (`AZ-3`); the string `PE_RESULT` occurs 0 times in the executable, 0 times in the `.dll` / `.exe` files of the installed game, and 0 times in the text-like files (`.txt`, `.xml`, `.json`, `.h`, `.ini`, `.cfg`, `.fx`, `.cgfx`) of the full archive extract; and `PResult` itself occurs only inside RTTI type strings and once as the reflected type name `Phyre::PResult`. An SDK header would settle it and is not a source this database holds or may quote. **What a reimplementation needs is already on this page and does not depend on the names**: `0` success, `6` the header is refused, `9` the read came up short, `0xD` an allocation failed - each read from the `return` it comes from. If a header is ever admitted, this row reopens with a one-line table; until then the numbers are the identifiers.
- [x] ~~**What `m_headerClassInstanceCount` and `m_headerClassChildCount` count**, as distinct from
  `m_instanceListCount`. The mesh sample gives 76 and 9,196 against 96 instance lists; the texture
  gives 0 and 0 against 2.~~ **`CU-2` ANSWERED 2026-09-12 (FABLE) over the archive.** A "header
  class" is a class whose namespace record carries **~~bit 4~~ the `0x04` bit of class word `w7`** *(corrected 2026-10-02, OPUS: `0x04` is the header flag, CONTRACT-phyre-packed-namespace.md NS-1; 12 and 20 both carry it, and 12 has no `0x10`)* — in this title
  exactly three: `PParameterBuffer` (`w7` = 12), `PAnimationClipBinding` and
  `PModifierNetworkInfoPacket` (`w7` = 20); `w7` is a per-class constant (no class carries two
  values in 684,244 records; `PBase` 32, `PAssetReference` 8, `PClassDescriptor` 2, `PParameterBufferBase`
  34, …). **`m_headerClassInstanceCount` = the number of instances of those classes** — equal in
  all 2,184 files that hold any (the shader and mesh clusters) and 0 in the other 33,800, which hold
  none. **`m_headerClassChildCount` = the sum of their children**: for a `PParameterBuffer` the
  `m_count` of its `m_tweakableShaderParameterDefinitions` array (read from the object at `+0x10`),
  for a `PAnimationClipBinding` 1 and for a `PModifierNetworkInfoPacket` 3 (its `_Buffer`,
  `_ModifierCode`, `_ModifierInstance` sub-blocks) — **2,184 / 2,184**, the five files with the
  latter two being the ones the parameter-array sum alone missed by exactly 1 and 3. The reading
  the name implies holds: these are the objects that carry trailing data after the reflected
  fields (`n × instanceSize ≠ m_objectsSize` for every header-class list; `brightnessshader.fx`'s
  one buffer is 32 reflected bytes then 132 of constants), and the counts tell the loader how many
  such headers and sub-blocks to expect. The earlier mesh sample's 76 / 9,196 are its parameter
  buffers and their parameter total.
- [x] **CU-3.** **The fixup tables themselves** — six of the header's fields size and count them, and none of
  the six has been followed into the data. That is where a modder who wants to *edit* rather than
  read a cluster has to go. `CU-3`.
  > *Narrowed 2026-09-12 (FABLE):* over all 35,984 files, `m_totalDataSize` **equals the sum of the
  > instance lists' `m_size`** and each of `m_arrayFixupCount`, `m_pointerFixupCount`,
  > `m_pointerArrayFixupCount` and `m_pointersInArraysCount` **equals the sum of the same field
  > over the list headers** (35,984 / 35,984), so the header's counts are totals of the per-list
  > counts and the instance data is one contiguous run in list order (walked that way to read
  > the parameter buffers for `CU-2`). The file is **not** header + namespace + lists + data + the
  > four fixup sizes + the three buffer sizes (0 / 35,984) — the buffer sizes are maxima, not totals
  > — so the tables' positions still need the loader.
  >
  > *Narrowed further 2026-09-22 (FABLE) — **the obvious reading is refuted, over all 35,984
  > clusters, 0 unreadable.*** **A fixup table is NOT `count` fixed-width entries filling `size`
  > bytes.**
  >
  > | | |
  > |---|--:|
  > | files where `m_arrayFixupSize` **< `m_arrayFixupCount`** | **18** |
  > | … the extreme (`phyredefaultlitshader.fx#176bb7aa…`) | **755 bytes declared for 955 entries — 0.79 B/entry** |
  > | files where `m_arrayFixupSize % m_arrayFixupCount != 0` | **2,190** |
  > | files where `m_pointerFixupSize % m_pointerFixupCount != 0` | **35,970 of 35,984** |
  >
  > **The 18 files are the ones that settle it**: no table of 955 entries fits in 755 bytes at one
  > byte an entry, so either the entries are **bit-packed or otherwise compressed**, or **`size`
  > does not measure a table of `count` things at all.** *This narrowing does not choose between
  > those two* — it removes the reading that a reader arrives with, which is the flat array. The
  > pointer table's 35,970 / 35,984 non-divisibility says the same thing without needing the
  > extreme case; the 14 that do divide are what coincidence produces at this corpus size.
  >
  > **And the pointer-array channel is mostly unused:** `(m_pointerArrayFixupSize,
  > m_pointerArrayFixupCount)` is `(0, 0)` in **34,859** of 35,984 clusters, `(4, 1)` in **960**,
  > and a long tail otherwise.
  >
  > > **A caution recorded against my own first pass.** On the eight `artdata/shaders/*.fx`
  > > clusters I looked at first, that pair was `(4, 1)` in **every one**, and it read like a
  > > structural constant. **It dissolved at corpus scale** — those eight are 0.02 % of the files
  > > and are not representative of them. *The sweep that found the 18 counter-examples is the
  > > same sweep that killed the constant.*
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the tables are packed, and they are now decoded from the file.** Control: [`cu3_fixup_tables.py`](../../_index/candidates/cu3-fixup-tables/cu3_fixup_tables.py)
  (3 checks, FAILS 0). The decoder is a line-for-line transcription of the loader's two decoders. It was made by a
  delegated read-only pass and is adopted here with its controls, re-run over the full corpus.
  - **Where they are.** After the header-class tables, in stage order: pointer-array, then pointer, then array.
    Each stage reads `size` packed bytes and decodes every instance list's share into fixed entries. The entries
    are 16 bytes for the array and pointer-array tables and `0x1C` for the pointer table. So **`size` is the
    packed byte length and `count` the decoded entry count**. This settles the narrowing's open choice: compressed.
  - **The encoding.** A table is a series of groups. Each group is a mode byte (low 3 bits: 0 dense, 1 sub-groups,
    2 explicit list, 3 all-except, 4 bitmask, 5 explicit entries, 6 arithmetic progression), then a varint key
    rotated right by one, then the mode's object indices and a varint payload per entry. Flag bits in the mode
    byte suppress payload fields. A group of 955 entries can take a few bytes, which is why `size < count` occurs.
  - **Verified on the data.** In all 35,984 shipped clusters, every list decodes to exactly its per-list count, and
    each table consumes exactly its `size`. For every mesh and "neither" cluster, what follows the array table is
    exactly the index plus vertex buffer size.
  - **Sensitivity.** On a 300-file sample, starting a byte early or late, or reading the tables in the wrong
    order, fails every file.
  - **Not decoded:** what each entry's fields mean (which offset is patched with what), and the texture clusters'
    trailing bytes.
- [x] ~~**UQ-287.** **`m_userFixupCount` / `m_userFixupDataSize`** — a user-extensible fixup channel; whether this
  title uses it for anything is unestablished (the mesh sample has 26 of them).~~ **ANSWERED 2026-09-25 (FABLE,
  Claude Opus 5.5): every shipped cluster uses it, and it is how a file names runtime objects.** All 35,984
  headers have a non-zero count. The loader `0059E880` resolves each fixup through its type's `+0x48`
  resolver; the one exception is `PAssetReferenceImport`, which is kept as raw bytes. The fixups name class
  descriptors (`PTexture2D`, `PMaterial`, …), enum values (`ARGB8`, `Opaque`) and asset-reference imports.
  See [§ The user-fixup channel](#the-user-fixup-channel--named-references-resolved-at-load-fable-claude-opus-55-2026-09-25).
- [x] ~~Whether the uniformity of the 169-file sample holds over all 35,984.~~ **`CU-4` ANSWERED 2026-09-12 (FABLE)** and recorded in this document's own section 216: the uniformity holds over all 35,984 entries, read from their first VBF block. The box below the answer was never ticked.

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| The 21 fields, names and byte offsets | the engine's own `PClassDataMemberBase` registrations at `005983E0` / `00598C50` / `00598DF0`, one call per field with the offset as the fifth argument | 1 |
| All 21 are `unsigned int` | every registration passes `PTypeDefault<unsigned int>` at `01F2E5A0` | 1 |
| Header is 84 bytes | `m_size` field of 169/169 files reads 84; independently, the loader reads `0x54` and copies 21 dwords | 1 |
| Marker `0x50485952` | the two `cmp` sites in `0059A3B0`, and the first four bytes of 169/169 files | 1 |
| Big-endian files are accepted via byte-swap | the swap-and-retest branch, complete body | 1 |
| `PHYR` occurs zero times in `.text` | byte scan of the section, with `RYHP` (7 sites) as the positive control | 1 |
| Platform `0x44583131`, physics `0x424C4C54` | the two constant-return leaves, disassembled | 1 |
| The platform check is live | `0059E129 mov byte [rsp+0x30], 1` at the sole call site, with a direct-call scan confirming one caller | 1 |
| Error codes 6 / 9 / 0xD | the `return` statements of `0059A3B0` | 1 |
| Version tolerance both ways | the `m_size != 0x54` branches, complete | 1 |
| Corpus uniformity | 169 extracted files parsed | 1 |
| **169 is 0.47 % of shipped** | the archive census's 35,984 `.phyre` entries — **the sample is not shown to be representative** | 3 |
| `TLLB` is Bullet | the four bytes reversed, plus Bullet's presence in this build's RTTI and third-party inventory | 2 |

## 7. The `0059E070` exclusive subtree — the loader's ~40 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 38 frontier functions to `0059E070` (the `PostProcessing.Vignette`
call site is one entry; the subtree is the loader machinery beneath it); an audit census
(AUDITSEM-CONTRA-FRONTIER-59E070) adds `00599670` (254 B) and `0059FCA0` (108 B) — exclusive
callees the first pass missed because their only callers are themselves members — for ~40.
All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| orchestrator | `0059E300` (1,141 B — interior verified 2026-09-17, SWE2-FRONTIER: `00686C20`→`00686D10` head confirmed at [`0059E336`](../../_index/ADDRESS-INDEX.md), `00584730` ×4 + `00861EC0` ×3) | calls **12 distinct listed members** in body order — `00686C20`→`00686D10`→`0059FCA0`→`0059E780`→`0059D6A0`→`0059F500`→`0059E880`→`0059D940`→`0059CE30`→`0059C700`→`0059C250`→`0059F7A0`/`0059BDC0` — plus `00599670`/`00686DD0` and `0016D6A0`; reads `02CF8580`/`02D3E680` |
| object builders | `0059AC00` (1,154 B — interior verified 2026-09-17, SWE2-FRONTIER: `005CDAA0` ×4 first at [`0059ACF7`](../../_index/ADDRESS-INDEX.md), `00861EBA`/`00808C40`/`0063BB10`), `0059C250` (1,192 B), `0059C700` (1,829 B), `0059CE30` (1,181 B — interior verified 2026-09-17, SWE2-FRONTIER: `0017D260` first at [`0059CEFB`](../../_index/ADDRESS-INDEX.md), `005CDAA0` ×3 + `00584730` ×2 + `00861EC0`), `0059D940` (1,828 B), `0059E880` (959 B), `0059F500` (672 B) | `[rax+0x28]`/`[rax+0x40]`/`[rax+8]` indirect calls + `005CDAA0`/`0017D260`/`00584730` — construct/fill loaded objects, keyed on `00D26xxx`/`00D27xxx` `.rdata` descriptor tables |
| deserializers | `0059AC00` (1,154 B — `00D27610`/`58`/`98`/`D0` table row), `0059B430` (1,547 B — `00D274D0`/`520`/`5C0`; interior 2026-09-17, SWE2-FRONTIER — `00637440`/`005CDAA0`/`0063BA10` field-read sequence begins [`0059B4B2`](../../_index/ADDRESS-INDEX.md), with `0059D2D0`/`0059BE00`/`0059BA40` container calls), `0059AAE0` (`0059FCA0` ×3), `0059D6A0` (`00D26D50`), `0059D590`, `0059E780` (`00596FC0`) | per-type block readers; each descriptor-table row pairs a reader with its class |
| byte-swap / stream ops | `00596890` (1,811 B — `0059FFC0` ×6 + `00597400`/`00597560`, tables `005971F0`/`00597200` + `00D27A08`/`00D27A38`), `00599500` (`0063E2E0` ×2 + `00599670`/`00686D00`, `02CAA0A0`), `00599670` (254 B — `0063BB10` + `0059B090` + `00861EBA`), `0059FCA0` (108 B — `00584730` only), `0059A3B0` (the CONTRACT subject — `0063E2E0` ×2 + `0059A6F0`/`00686D00`/`0069E780`), `0059A6F0`, `00596FC0`, `00597070`, `00597130`, `00597400` (`call r13`), `00597560` (`call r12`) | the stream layer — `0063E2E0` is the byte-swap block the CONTRACT names; `call r13`/`r12` are tail-dispatched ops |

| `0063xxxx`/`0068xxxx` Phyre side | `00632B30` (`00D58358`/`01F2DF28`), `006393A0`, `0063A4C0` (`00597220`), `0063BBA0`, `0063C630`, `0063DD30` (`00680100`), `00680100`, `00686C20`, `00686D10`, `0069E780`, `0059BDC0`, `0059BE00` (`0067FF40` ×2), `0059C180` (`0059A780`), `0059A780`, `0059A8B0` (`00D27A80`/`90`), `0059F7A0` (788 B — `0067F580`/`0067FFB0`/`0063BA10`/`00680150`/`00680200`/`0067F700`/`00597220`/`0067F6F0`/`006803D0`/`00680030`, `009038E0`) | the engine-side helpers the readers call — allocation, list insert, class lookup |

*Interior reads 2026-09-17 (SWE2-FRONTIER):* `0059C700` runs `005CDAA0`/`0059BED0`/`00584730`/
`0063DC30`/`0063BFA0` pairs over the descriptor tables (first `005CDAA0` at
[`0059CAEA`](../../_index/ADDRESS-INDEX.md)); `0059D940` is the same builder shape —
`005CDAA0` ×3, `00584730` ×2, `0017D260` ×2, `00599670` + `00861EBA` (first `005CDAA0` at
[`0059DD79`](../../_index/ADDRESS-INDEX.md)); `00596890` repeats `0059FFC0` six times with the
`00597400`/`00597560` `call r13`/`call r12` tail ops exactly as tabled (first `0059FFC0` at
[`00596BBB`](../../_index/ADDRESS-INDEX.md)).

What this adds to §2: the loader is not one reader but a descriptor-table-driven family — each
`00D2xxxx` table row selects a builder+reader pair, and `0059E300` runs the table in order.
Which asset class each `00D26xxx`/`00D27xxx` row names is not established this pass.

> **Crossing named for FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** `0063BB10`, which the table above lists under
> `00599670`, forms a mutually recursive pair with `00639A60`. The ledger files `00639A60` under Presentation, but the
> code does not support that label: `00639A60` is Phyre reflection machinery.
>
> - It builds instances and `memcmp`s them through virtual slots `+0x50` and `+0x58`.
> - It warns *"Class '%s' has a position dependant constructor and should be marked as having no default constructor…"*
>   (`00639B5E`).
> - It calls `0063BB10` back at `00639C0E`, and `0063BB10` calls it at `0063BB34` after a slot-`+0x60` call.
>
> [The class descriptor system](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) cites the
> same function reading `+0xC0`. The edge is a reflection walk inside the loader's stream helpers, not a rendering
> dependency.

## 8. Related

- [`README.md`](README.md) — this folder's statement of the obligation an `external` disposition
  carries. **This document is the discharge of it: the loader contract, from this build.**
- [`../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`](../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md)
  — the registration mechanism the header layout was recovered through.
- [`../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md`](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
  — the 169-file corpus and its limits; owner of the `phyre` format disposition.
- [`../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
  — the `PClusterHeaderBase` descriptor and the vftable it is built on.
- [`../../23-Third-Party-Libraries/third-party-middleware-inventory.md`](../../23-Third-Party-Libraries/third-party-middleware-inventory.md)
  — Bullet, whose four-character id the header carries.

## Falsification pass — 2026-09-07, `xiionline-61`

**Self-attack, same day as authorship.** The session that wrote this document had a demonstrated
error rate, so its own claims were re-derived rather than re-read.

**The systematic attack:** every "only caller" / "N callers" statement in the day's four documents was
made with a scan that matched `E8 call rel32` only. **The CRT block later established that this
binary reaches things through `E9 jmp rel32` tail calls and import thunks**, so every one of those
claims was re-run against **both** instruction forms, and against `data_xref_scan.py` for
address-taken references (vtables, pointer tables) with a passing control.

### Result for this document — **one field list corrected**

| claim re-tested | result |
|---|---|
| `0059A3B0` has **exactly one caller** | **stands, and is now properly evidenced** — 1 `call`, **0 `jmp`**, and `data_xref_scan.py` finds **0** address-taken references against a control of 150. The address is never in a vtable or pointer table. |
| `PInstanceListHeader` has **ten** fields | **WRONG — it has nine.** Corrected in §2; the tenth was a grep artifact, and the false "file-vs-binary discrepancy" it produced is refuted in the namespace document. |
| the three D3D11 sizes partition the corpus | **stands** — 6 mesh / 70 texture / 93 neither sums to 169 with no mixed case. |

**Not attacked:** the version-tolerance branches, which no shipped file exercises; the packed
namespace, which has its own document; `0059A6F0`'s callee.

## SWE2-EC7-19 update (2026-05-15) — `0063BFA0`/`0063BA10`/`0063A790` loader-support fragments

`0063BFA0` (59 B) is the index-bounded slot resolve over this page's descriptor tables: `edx >= [rcx+0x70]` returns 0 (`0063BFA3`); else `r9=[+0x50]` supplies the stride — `slot = [rcx+0x60] + [r9+0x38]*edx` (`0063BFB3`..`0063BFBA`) — then the `[+0x10]` link chain is walked and a slot found on the list returns 0 (`0063BFBE`..`0063BFCE`); a clean slot returns `slot + dword[r9+0xF8]` (`0063BFD0`..`0063BFDA`). The descriptor-row pointer the loader's indexed reads hand out.

`0063BA10` (215 B) is the string-keyed record lookup in the same adapter band: `rdx==0` returns 0 (`0063BA2A`); it walks the `+0x10` intrusive list — `r9 = [rcx+0x10]` head vs the `&rcx+0x10` sentinel, records at `r9-0x50` (`0063BA33`..`0063BA4B`) — byte-comparing each record's `[r9+0x30]` name against `rsi` (`0063BA60`..`0063BA75`), a hit returning the record. A miss recurses over the `[rdi+0x28]` child chain (`0063BA8E`..`0063BAC9`): `0063BA10(rbx, rsi)` per linked node until one resolves. The name→record resolution the loader's pair-walkers share.

`0063A790` (461 B) is the mask-blend composite the `0059AC00`/`0059E300` deserializers and `00636280` call: `rdx` null exits (`0063A793`); when `[rcx+0xFC]` has bit `0x1E` set the `+0x60` vcall runs first (`0063A7D1`..`0063A7DA`), then `00639A60(rcx,0)` + `00639C80(rcx,0)` (`0063A7DD`..`0063A7EC`). With `rbp=[+0x38]` rows and `r8=[+0xC8]` mask non-null it composites `dst[r9]` = `(src[rdi] & ~mask[r8]) | (dst[r9] & mask[r8])` — 32 B/iteration SSE (`movdqu`/`pandn`/`pand`/`por` at `0063A860`..`0063A8BC`, with overlap checks routing to the same byte formula at `0063A8E0`). It closes by walking the `+0x78` parent chain to the `02E4E720` root and publishing `rbx` into `[[rsi] + dword[rbx+0xF8] + 0x10]` (`0063A914`..`0063A948`) — the merge-and-publish the container's deserializer bodies run per element.

## SWE2-EC7-34 update (2026-09-19) - `0059E880`

`0059E880` (959 B) is ~~the cluster-header debug dump~~ **the user-fixup loader; the dump is only its
failure diagnostic** *(corrected 2026-09-25, FABLE, Claude Opus 5.5, see
[§ The user-fixup channel](#the-user-fixup-channel--named-references-resolved-at-load-fable-claude-opus-55-2026-09-25))* - `" %c "`/`"%02x "`/`"UNKNOWN"` strings, `00584730`/`0059FCA0`/`0063DC30`/`005CDAA0`. Interior anchor `0059E917` (an `00584730` call).

## SWE2-EC7-35 update (2026-09-19) - `0059F7A0`

`0059F7A0` (788 B) is the `"PMapPair"` metadata init - `0067F580` pair then the `006803D0`/`00680200`/`00680150`/`00680030`/`0067FFB0`/`0067F700` registration chain. Interior anchor `0059F81F` (a `0067F580` call).

## SWE2-EC7-35 update (2026-09-19) - `0059BA40`

`0059BA40` (766 B) is the class/descriptor name printer - `"Class %'s"` and `"Data mem"` format strings plus `"UNKNOWN TYPE"`, eight `005CDAA0` allocator calls and `0063BC70` pair. Interior anchor `0059BAC9` (a `005CDAA0` call).

## SWE2-EC7-36 update (2026-09-19) - `0059F500`

`0059F500` (672 B) is a cluster-header helper - `0059D590`/`00584730`/`0017D260`. Interior anchor `0059F5A5` (a `0059D590` call).

## SWE2-EC7-36 update (2026-09-19) - `0059D6A0`

`0059D6A0` (603 B) is a cluster-header descriptor op - `00D26D50` rdata, `0063DD30`/`006394E0`/`005CDAA0`. Interior anchor `0059D74C` (a `0063DD30` call).

## SWE2-EC7-40 update (2026-09-19) - `00599500`

`00599500` (360 B) is the stream-layer body the page names - `02CAA0A0`, `0063E2E0` pair (the byte-swap block) plus `00599670`/`00686D00`. Interior anchor `00599592` (a `0063E2E0` call).

## SWE2-EC7-41 update (2026-09-19) - `0067F580`

`0067F580` (358 B) is a Phyre serialization pair-init body - `0067F9D0` twice. Interior anchor `0067F641` (a `0067F9D0` call).

## SWE2-EC7-41 update (2026-09-19) - `00597400`

`00597400` (351 B) is a call-free 7-bit varint reader - byte loop `and 0x7f`, `shl cl` (`cl += 7`), `or` accumulate, sign-bit `js` continue. Interior anchor `00597440` (the `and eax, 0x7f`).

## SWE2-EC7-43 update (2026-09-19) - `00597560`

`00597560` (291 B) is a Phyre-container varint reader - three 7-bit varints off a `[r9]` cursor (`shl`/`or` accumulate), then a `r10d`-count loop copying 0x1C-byte records `[r15]`->`[rsi]` with a `call r12` callback per record. Interior anchor `00597658` (the `call r12`).

## SWE2-EC7-44 update (2026-09-19) - `0059AAE0`

`0059AAE0` (275 B) is a sound-request-adjacent body - `0017D260`/`00584730`/`0059FCA0`/`00861EC0`. Interior anchor `0059AB43` (a `0017D260` call).

## SWE2-EC7-45 update (2026-09-19) - `0059E780`

`0059E780` (244 B) is a body - `00596FC0` single call. Interior anchor `0059E7C6` (the `00596FC0` call).

## SWE2-EC7-45 update (2026-09-19) - `0063C630`

`0063C630` (242 B) is a Phyre body - `call [rax+8]`/`[rax+0x10]`/`[r8+0x18]`/`[rax+0x20]`/`[rax+0x38]` vcalls, no direct calls. Interior anchor `0063C667` (the first vcall).

## SWE2-EC7-48 update (2026-09-19) - `0059BE00`

`0059BE00` (202 B) is a body - `0067FF40` single call. Interior anchor `0059BE50` (the `0067FF40` call).

## SWE2-EC7-48 update (2026-09-19) - `0063DD30`

`0063DD30` (198 B) is a body - `0017D260`/`00680100`. Interior anchor `0063DD9B` (an `0017D260` call).

## SWE2-EC7-49 update (2026-09-19) - `00597070`

`00597070` (189 B) is a body - `call [rax+0x28]` vcall only. Interior anchor `005970AD` (the vcall).

## SWE2-EC7-50 update (2026-09-19) - `00597130`

`00597130` (181 B) is a body - `call [rax+0x28]` vcall only. Interior anchor `0059716E` (the vcall).

## SWE2-EC7-51 update (2026-09-19) - `00680150`

`00680150` (173 B) is a PMapPair metadata-init chain member - `0017D260` single call. Interior anchor `0068018A` (the `0017D260` call).

## SWE2-EC7-51 update (2026-09-19) - `00596FC0`

`00596FC0` (173 B) is a body - `call [rax+0x28]`/`call [r9]` vcalls only. Interior anchor `00597000` (the first vcall).

## SWE2-EC7-52 update (2026-09-19) - `0067F9D0`

`0067F9D0` (1097 B) is a call-free ordered-tree erase - `byte[+0x10]&1` color-bit rebalancing with `neg`/`cdqe` parent fetches on the `[rcx+0x18]` head (`0067F580` calls it twice). Interior anchor `0067FA18` (the post-self-check child fetch).

Corrected 2026-09-27 (FABLE BQ-23 tier-6b, `FABLE-REQ-SWE2EC7-BQ23-RELABEL-AND-TWO-NOTES`): the earlier "MSVC `_Tree` shape" attribution was wrong. MSVC `_Tree` keeps `_Color`/`_Isnil` as bytes at `+0x18`/`+0x19` and `_Erase` terminates on the `_Isnil` flag; `0067F9D0` instead packs the colour into bit 0 of the parent word at `+0x10` and loops to null - Phyre's `PRedBlackTreeNode` layout (children `+0`/`+8`, parent|colour `+0x10`, key at node `+0x18`). Label now `GFZ.V121.CodeDomain.Phyre.OrderedContainerRuntime.RedBlackTreePackedParentColorEraseFixup`.

## SWE2-EC7-69 update (2026-09-19) - `006394E0` count-stride adapter measured

`006394E0` (46 B) is the multiply-forward adapter the cluster descriptor ops
call: `edx == 0` returns 0; otherwise it shuffles the register arguments -
`r9 ← r8` (record), `r8d ← edx` (count), `edx ← [record+0x38] * count` - puts
the original fourth arg into the outgoing stack slot, and tails
`00639510(rcx, stride*count, count, record, arg4)`. The `[+0x38]` dword is
the element stride the post-process and descriptor callers share.
Interior anchor `006394FC` (the `imul edx, r8d` product).

## SWE2-EC7-72 update (2026-09-19) - `0059FCA0` slot claim measured

`0059FCA0` (108 B) is the slot-claim the loader runs: `r8d < 0` returns
5; when `[+8]` differs from the incoming `rdx` and the record's sign bit
(bit 31 of `[rcx]`) is clear and `[+8]` is non-NULL it runs `00584730`
on the occupant first - then `[+8] = rdx`, `[rcx] = r8d | 0x80000000`
(the claimed bit), and returns 0.
Interior anchor `0059FCEB` (the `00584730` occupant-release call).

## SWE2-EC7-79 update (2026-09-20) - `0063DC30` dispatch-with-default measured

`0063DC30` (45 B) is the `+0x48`-slot dispatch: a live function
pointer gets `rcx/rdx/r8d/r9d` forwarded and tail-called; a NULL
slot returns `0x15` - the default-error arm the loader callers
expect.
Interior anchor `0063DC53` (the `jmp rax` tail).

## SWE2-EC7-118 update (2026-09-21) - `00680100` / `0067FF40` / `0067F6F0` measured

`00680100` (66 B) is the
freelist-chain builder
`0063DD30` calls: `r8 == 0`
returns 0 and `rdx == 0`
returns 1; otherwise it
threads `r8 - 1` nodes at
`+0x18` stride, each
`[node]` pointing at the
next, then pushes the
chain onto `[r9]` -
returns 0.
Interior anchor `00680123`
(the stride add).

`0067FF40` (99 B) is the
list-iterator increment
`0059BE00`, `005C22B0`,
`005CB8D0` and `00676A70`
run: from `[rdx + 8]` it
follows `[rax]` links until
the head, then climbs
through `byte[+0x10] & 1`
encoded offsets until the
`+0x18` sentinel - the
intrusive-list `_next`.
Interior anchor `0067FF6C`
(the encoded-link load).

`0067F6F0` (13 B) self-links
the three pointers at
`+0x18`, `+0x20` and `+0x28`
to `rcx` - the sentinel
head init `00597F30`,
`0059F7A0`, `005AA080`,
`005C22B0` and `005C35A0`
all run.
Interior anchor `0067F6F4`
(the `+0x20` store).

## SWE2-EC7-121 update (2026-09-21) - three `00639510` callees measured

`00639750` (48 B) is the
aligned bump-allocator on
the `+0x48` block: the
`+0x14` cursor is aligned
up to the `r8` boundary
(`(cur + r8 - 1) & ~(r8-1)`
via `dec`/`not`/`and`), the
padded total is checked
against the `+0x10` bound,
and on fit it returns
`[+8] + pad` and stores the
new cursor - null
otherwise.
Interior anchor `00639774`
(the base-plus-pad
return).

`00639320` (118 B) is the
bucket-aggregate walk: it
follows `rdx`'s `+0x78`
chain, and each node whose
`+0xEC` index falls below
`btr([rbx+0x10], 0x1F)`
indexes a 0x20-stride slot
in the `+0x18` array; the
first hit lazily links
`rdx+0x38` into the slot's
list head, then every hit
adds `rdx+0x70` into
`slot+0x10` and bumps
`slot+0x14`.
Interior anchor `00639381`
(the `slot+0x10`
accumulate).

`00631180` (65 B) is the
three-step teardown
forwarder: `0063B3E0(rdx)`,
`00680030(rdx + 0x10)`,
then it tails
`00680200(rcx, rdx)`.
Interior anchor `0063119D`
(the `0063B3E0` call).

`0059EC40` (289 B) is the extent accumulator `0059BED0` runs for cluster payloads: an early-out returns 0 when `[rcx+0x28]` is null or a flag check passes — flag dword `[[rcx+8]+0x10]` bit `0x02` forces the pass, bit `0x40` gates a `vtable+0x20` query ~~(result `== 1` fails)~~ (result `1` **allows** recursion; any other result stops - *corrected 2026-09-30, FABLE, on SWE2-AUDIT-SPEC's [pointer-keys review](../../_index/candidates/auditspec-review-astra-softedges-pointer-keys-0930/REVIEW.md); record [`astra-returns-softedges-fable-0930`](../../_index/candidates/astra-returns-softedges-fable-0930/README.md)*) applied only while the `[rcx+0x10]` stream's `vtable[+8]` sub-object reports `+0x5C == 2`. On the through path it adds `[[r9+8]+0x14] − [[[rcx+0x28]+8]+0x14] − [[rcx+8]+8]` into `[r12]`, and returns `r13 + [rsi+0x48] + ([[rdi+0x10]+0xF4] − [[r9+0x10]+0xF4])` — a span delta between two `+0xF4` extent fields. *(Qualified 2026-09-30, FABLE, on SWE2-AUDIT-SPEC's [member-boundaries review](../../_index/candidates/auditspec-review-astra-softedges-member-boundaries-0930/REVIEW.md): the sum after `r13` is 32-bit and zero-extended (`0059ED3F` `lea eax, [rdx + rbx]`, then `0059ED42` `add rax, r13`), so the return is `r13 + zext32([rsi+0x48] + child F4 − parent F4)` modulo 2^64.)*

Interior anchor `0059ECD7` (function `0059EC40`).

`0059BDC0` (50 B) is the stride-`0x30` keyed lookup `0059E300` uses: reads count `[rcx+0x28]` (`btr 0x1f`) and array `[rcx+0x30]`, walks elements by `idx*48`, and returns the first whose `+0x10` field equals `rdx`, else 0 — same shape as `00600BE0` but the key sits deeper in the record.

Interior anchor `0059BDED` (function `0059BDC0`).

`00599390` (207 B) is the strided block copy `0059B090` calls for payloads: descriptor `r8` supplies `r12d` row count plus stride pair `[+4]`/`[+8]`, and byte `[r8+0xC]` selects whether each cursor offset comes from `r9`'s `[+8]`-table field `[rax+8]` or the `[+0x10]`-object's `+0x48` (`cmovne` on both). If that object's `vtable[+8]` sub-object reports `+0x5C == 1`, `ebp` = `[table+0xC] * max([table+0x14], 0063BC70(obj))` — the copy length; then `r12` iterations of `00861EBA(dst-cursor, src-cursor, ebp)` advance each cursor by its stride.

Interior anchor `00599439` (function `00599390`).

`00595E70` (114 B) is the byte-granular strided copy sibling `0059B090` also calls: descriptor `r8` = {`ebx` count, `+4` source stride, `+8` dest stride, `+0xC` selector}; the source base is `rcx` plus `[table+8]`-or-`[obj+0x48]` (selector-swapped), the dest base `rdx` plus the other; then `ebx` iterations of `*dst = *src` advance each by its stride — the 1-byte-element version of `00599390`'s block copy.

Interior anchor `00595EC0` (function `00595E70`).

## The user-fixup channel — named references resolved at load (FABLE, Claude Opus 5.5, 2026-09-25)

**Answers UQ-287.** *Static, from the shipping bytes, with a corpus census and a file sample.*

**Every shipped cluster uses the channel.**
[`members/user_fixup_census.py`](members/user_fixup_census.py) reads the 84-byte header of all 35,984
`.phyre` entries from their first VBF block, the CU-4 method, and writes
[`members/user-fixup-census.tsv`](members/user-fixup-census.tsv). Every header passes the
`RYHP`/84/`11XD` control.
- **`m_userFixupCount` is non-zero in all 35,984**: 2,091 meshes, 33,794 textures and 99 of neither.
- The counts run from 1 to 156 per file, with data sizes of a few bytes per fixup.

**What the loader does with them — `0059E880`**, called by the cluster orchestrator `0059E300`.
1. It reads `m_userFixupDataSize` (`+0x34`) and `m_userFixupCount` (`+0x30`) from the header copy
   (`0059E8B0`/`0059E8B3`).
2. It sizes one buffer as `align8(dataSize) + count × 24` (`0059E8B7`–`0059E8D1`), allocates it, and
   reads the **data blob** through stream slot `+0x28`. A short read returns `9` (`0059E95C`–`0059E967`).
3. It reads `count` **12-byte records** `{typeIndex, size, offset}` (`00597130`, `0059E9D2`).
4. **It resolves each record's type through the cluster's namespace tables** (`0059EA00`–`0059EA63`).
   An index below the first table's count selects a 24-byte entry at `[+0x20]`; otherwise
   `index − count − 1` selects a 48-byte entry at `[+0x30]`. A NULL entry address skips the record
   (`0059EA2A`/`0059EA3E` → `0059EBDA`); an entry whose descriptor pointer is NULL aborts the load
   with `0x13` (`0059EA66` → `0059EBF7`).
5. **When the type is `PAssetReferenceImport`** (`02D3E780`, the
   `PClassDescriptorConcrete<PAssetReferenceImport>` its registrar `00165F40` builds), the fixup is
   **kept unresolved**. The stored record is `{type, data pointer, size, 1}` (`0059EA8B`–`0059EAA6`).
6. **Any other type is resolved by its descriptor's `+0x48` slot**, through `0063DC30(type, &out,
   data, size, context)` (`0059EAC9`).
7. **A NULL result is logged, not fatal.** It prints
   `"Resolving fixup for '%s' returned NULL pointer\n"` with the type name (`"UNKNOWN"` if it has none).
   For data under 32 bytes it adds a hex and character dump (`0059EADF`–`0059EBA7`), then stores the
   record and continues.
8. The resolved 24-byte records sit after the blob in the same buffer (`0059EBC3`–`0059EBE5`).

**What the fixups say.** [`members/user_fixup_sample_probe.py`](members/user_fixup_sample_probe.py)
finds the record array by its shape in two named mesh files (`b0001.dae.phyre`, `rbn5001.dae.phyre`) and a seeded random sample of 40 files.
The blob sits directly before the records.
- The array was found in all 42 files (the probe prints each file's first eight records). **Every
  texture carries exactly two fixups**:
  - the class descriptor named by the string `PTexture2D`;
  - its format, typed `PTextureFormatBase` and named by a string: `ARGB8`, `BC5`, `DXT5` or
    `RGBA16F` in the sample. Cube maps name `PTextureCubeMap` instead of `PTexture2D`.
- **Meshes carry more:**
  - class-descriptor names: `PMaterial`, `PNode`, `PMesh`, `PMeshInstance`, `PTexture2D`, `PEffectVariant`;
  - a `PSceneRenderPassType` value named `Opaque`;
  - a 2-byte `PAssetReferenceImport`.

**So the channel is how a cluster refers to runtime-registered objects by name.** Class descriptors
and enum values are looked up by string when the cluster loads. Asset-reference imports are carried
through as raw bytes for later linking.

**Not established here.**
- What each type's `+0x48` resolver does internally.
- When the `PAssetReferenceImport` bytes are consumed, and what their two bytes encode.
- The fixup types in the corpus beyond the 42-file sample: the census counts fixups, it does not
  decode them.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-cluster-header-and-what-the-loader-r-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00597200` | 17 B | stores `edx` to dword `+4` of `rcx`, then tail-jumps to `0059FFC0(rcx, r8, r9d)` | `00597203`, `00597206`, `00597209`, `0059720C` |
| `00597F30` | 78 B | calls `0067F6F0(rcx)`, then `00597F30 + 0x21` and `00597F30 + 0x2B` each with `rcx + 0x30`, then `00597F30 + 0x34` and `00597F30 + 0x3D` each with `rcx`, and returns | `00597F47`, `00597F51`, `00597F5B`, `00597F64`, `00597F6D` |
| `005AA080` | 64 B | calls `0067F6F0(rcx + 0x10)`, then `005AA080 + 0x25` with qword `+8` of `rcx`, then `005AA080 + 0x2F` with `rcx + 0x10`, and returns | `005AA097`, `005AA09B`, `005AA0A1`, `005AA0A5`, `005AA0AF` |
