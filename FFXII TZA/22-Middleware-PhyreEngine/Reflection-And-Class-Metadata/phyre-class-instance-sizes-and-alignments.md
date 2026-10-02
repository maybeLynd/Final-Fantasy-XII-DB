---
system: Phyre per-class instance sizes and alignments
category: 22-Middleware-PhyreEngine
status: DOCUMENTED
owner_layer: CodeDomain:Phyre.Reflection
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). This document cites no function classified since GN158; it names the descriptor constructors 00632D80 / 00632C90 and the 177 registrars that call them, all of which are already-owned family members. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-19
audit:
  passes: 1
  last_pass: 2026-09-19
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# Phyre per-class instance sizes and alignments

> For 177 Phyre classes, exactly how many bytes an instance occupies and what boundary it must sit
> on — the two numbers a reconstruction needs before it can allocate anything.

## 1. What this adds, and what it does not

**It does not re-identify the fields.** That `descriptor + 0x38` and `+0x3C` hold a `u32` size and
alignment is already the corpus's position — stated in
[`how-a-class-registers-its-array-members-and-annotations.md`](how-a-class-registers-its-array-members-and-annotations.md)
and carried as a layout row in
[`CONTRACT-phyre-class-descriptor.md`](CONTRACT-phyre-class-descriptor.md). The descriptor's byte
layout, its six intrusive lists, the name at `+0x30` and the parent at `+0x78` are all recorded
there, and the reading below agrees with every one of them.

Two things here are new:

1. **The values.** No file in the database carried a per-class instance size.
   [`phyre-field-schema.tsv`](phyre-field-schema.tsv) gives 680 field records with offsets, which
   tells a reader where a field sits but never how large the object containing it is.
   [`members/phyre-class-instance-sizes.tsv`](members/phyre-class-instance-sizes.tsv) supplies
   `size` and `alignment` for 177 classes.
2. **An external control.** The size/alignment identification previously rested on reading this
   image. Four of the 177 classes are structures whose layout is fixed by a published Microsoft
   header and owes nothing to FFXII, and all four match exactly — see §3.

## 2. Where the numbers come from

Each registered class has one registrar function that constructs its descriptor. 173 of them call
`00632D80`; 4 call the near-identical `00632C90`. The constructor is branchless and assigns every
field in one place, which is why
[`member-registration-and-the-recovered-field-schema.md`](member-registration-and-the-recovered-field-schema.md)
already calls it *"the derivation that should be trusted"*.

Its argument mapping, with the Win64 shift applied — a callee's `[rsp+0x28]` is the caller's
`[rsp+0x20]`, the fifth argument, once the return address is pushed:

| argument | register / slot | store | destination |
|---|---|---|---|
| 1 | `rcx` | — | the descriptor itself |
| 2 | `rdx` | `00632DD6 mov [rcx+0x70], rdx` | `+0x70`, the sub-object |
| 3 | `r8` | `00632DB0 mov [rcx+0x30], r8` | `+0x30`, **the class name** |
| 4 | `r9d` | `00632DB4 mov [rcx+0x38], r9d` | `+0x38`, **the instance size** |
| 5 | `[rsp+0x20]` | `00632DA5`/`00632DA9 mov [rcx+0x3c], eax` | `+0x3C`, **the alignment** |
| 6 | `[rsp+0x28]` | `00632DD1`/`00632DDA mov [rcx+0x78], rax` | `+0x78`, the parent descriptor |

A single registrar, `00597730`, builds `PClusterHeaderBase`: `mov r9d, 0x48` and
`mov dword ptr [rsp+0x20], 4` — size 72, alignment 4.

The name argument is what makes the sweep possible. Each of the 177 registrars loads its class's
bare name string with a `lea r8, [rip -> ...]` and immediately calls the constructor, so the class a
registrar belongs to is stated by the same instruction sequence that states its size. **All 177
loads put the name in `r8` and all 177 are followed by the constructor call within eight
instructions** — there is no second shape to disambiguate.

### The extent is the constructor's, not an assumption

The constructor's last store is `00632E69 mov dword ptr [rcx+0xfc], r10d`, so it initialises
`+0x00` through `+0xFF` and nothing beyond. Sweeping every displacement any of the 177 registrars
touches on the descriptor register gives a **maximum of `0xFC` and zero accesses at or beyond
`0x100`**. The descriptor is 0x100 bytes.

## 3. The controls

A control that cannot fail is not a control, so both of these are stated with what would have
refuted them.

### Control 1 — internal, and sharp

If `+0x38` is the instance size, then every field the field schema independently places in a class
must lie inside it. That schema was recovered by a different method from different call sites, so
it can disagree.

* **177 of 177 classes fit. 0 exceed.**
* Sharpness: **33 classes fit exactly** — their last recovered field ends on the final byte of the
  declared size — and 117 of 177 have less than 8 bytes of slack. A number that merely bounded the
  fields from above would not land on the last byte 33 times.
* Weakening: 269 of the 682 field rows have a type with no width in the table used, and those were
  counted as 1 byte. That understates field ends, so it makes the control *easier* to pass; the
  slack figures are therefore lower bounds on tightness, and the 33 exact fits are conservative.

### Control 2 — external

Four registered classes are Direct3D 11 structures whose layout is fixed by the Windows SDK header
and is public. Nothing about their sizes depends on this image, this constructor, or this reading.

| class | recovered size | recovered alignment | documented layout | |
|---|---|---|---|---|
| `D3D11_RENDER_TARGET_BLEND_DESC` | `0x20` | 4 | `BOOL` + 6 enums + `UINT8`, padded to 32 | match |
| `CD3D11_BLEND_DESC` | `0x108` | 4 | 2 `BOOL` + `RenderTarget[8]` of `0x20` = 264 | match |
| `CD3D11_DEPTH_STENCIL_DESC` | `0x34` | 4 | 4 dwords + 2 `UINT8` + pad + 2 × `DEPTH_STENCILOP_DESC` (`0x10`) = 52 | match |
| `CD3D11_RASTERIZER_DESC` | `0x28` | 4 | 10 × 4-byte members = 40 | match |

**Four of four, on both numbers.** A mis-identified argument would have had to reproduce four
independently published layouts by accident.

### Control 3 — shape of the alignment values

Across 177 classes the alignment argument takes exactly four values: **8 (137), 4 (22), 16 (12),
2 (6)**. All are powers of two and all are plausible alignments. An argument that was something
else — an index, a count, a flag word — would not be confined to `{2, 4, 8, 16}`.

## 4. Key addresses

| address | role |
|---|---|
| `00632D80` | class-descriptor constructor, 241 B, branchless; called by 173 of the 177 registrars |
| `00632C90` | the near-identical variant, 226 B; called by the other 4 |
| `00597730` | the `PClusterHeaderBase` registrar, the worked example in §2 |
| `006372A0`, `006373D0` | the two calls whose results become arguments 6 and 2 — **not dispositioned here** |

## 5. What is not claimed

* **What arguments 2 and 6 are computed from.** `006372A0` and `006373D0` produce the sub-object and
  the parent descriptor. Their values are not link-time constants, so the parent of each class is
  *not* recovered by this sweep and no class hierarchy is asserted *(answered: see member-registration-and-the-recovered-field-schema.md §19 and members/phyre-class-parent-chain.tsv; 2026-10-02, OPUS)*. The field at `+0x78` is the
  parent — that is the corpus's existing finding, not a new one — but this document does not say
  which parent any class has.
* **The other 138 classes.** 177 registrars were decoded of the roughly 315 in the registrar census.
  The remainder either register by name only (no size argument reaches the constructor in the shape
  scanned) or set the argument from a non-immediate. Their sizes are **unknown**, not zero.
* **That a recovered size is the C++ `sizeof`.** It is the value the engine registers and allocates
  by. For the four D3D11 structures those coincide exactly; for a class with a vtable and virtual
  bases the two need not, and nothing here distinguishes them.
* **Anything about `+0xEC`, `+0xF0`, `+0xF4`.** The constructor writes them
  (`mov dword [rcx+0xec], 0xffffffff`, `mov [rcx+0xf0], eax` from argument 7,
  `mov qword [rcx+0xf4], r10`). The `+0xF4` store is an 8-byte zero at an offset that is not
  8-aligned, which is the signature of the compiler merging two adjacent zeroed fields into one
  instruction — so it is **not** evidence of a single qword field, and no field is declared there.
  `CONTRACT-phyre-class-descriptor.md` owns these offsets.

## 6. Evidence

Static disassembly only. `00632D80` and `00632C90` read in full; the 177 registrars scanned by
tracking the descriptor register from `rcx` on entry and recording every displacement and every
`lea` of a known class-name string. The class names are the 179 leaf names in
`phyre-field-schema.tsv`, located as bare NUL-terminated strings in sections with raw data: 177 of
179 were found and every one of those 177 resolves to exactly one registrar.

Cross-checks recorded as agreement, not as new findings: the name at `+0x30` is where
`PType_FindOrRegisterByName` (`006388C0`) reads it and where
`PObjectAccessor<T>::Get` formats it from; the six self-linked list heads the constructor
initialises (`+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0`, `+0xB0`) are exactly the six that
`0063D550` re-initialises; `+0x70` and `+0xE8` match the destructor's operands.

Data: [`members/phyre-class-instance-sizes.tsv`](members/phyre-class-instance-sizes.tsv), 177 rows.

*Claim table added 2026-09-30 (OPUS) for FINAL-AUDIT pass 7; the claims and their evidence are the ones this section
already states, now each with its tier ([EVIDENCE-STANDARD](../../_index/EVIDENCE-STANDARD.md) tiers):*

| Claim | Evidence | Tier |
|---|---|---|
| each registrar stores the class's instance size and alignment into the descriptor it builds | `00632D80` and `00632C90` read in full; the 177 registrars scanned from `rcx` on entry, every displacement recorded | 1 |
| the 177 sizes and alignments in `phyre-class-instance-sizes.tsv` belong to the named classes | each registrar `lea`s its class-name string; 177 of 179 leaf names found, each resolving to exactly one registrar | 1, 2 |
| the name at `+0x30` is the one the by-name lookup reads | `PType_FindOrRegisterByName` (`006388C0`) and `PObjectAccessor<T>::Get` read it there | 1 |
| the six list heads `+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0`, `+0xB0` are the constructor's | the constructor initialises exactly these six, and `0063D550` re-initialises the same six | 1 |
| `+0x70` and `+0xE8` are the destructor's operands | the destructor's operands match | 1 |
| the class names are Phyre's own | the 179 leaf names of `phyre-field-schema.tsv`, located as NUL-terminated strings | 2 |

## An independent control on these sizes: the linker packed the default instances (2026-09-19, OPUS)

The instance sizes in this table were read from one place — the argument the class-descriptor
constructor is handed (`mov r9d, <SIZE>` into `00632D80`). A single instrument is a single point
of failure, and the sizes are now load-bearing: `PCluster::create` uses `descriptor[0x38]` both to
stride between instances and as the length of the per-instance `memcpy`.

A second, unrelated fact tests them. Every one of the 173 classes with a located constructor
registers a **default instance**, a static object of exactly that class, and the linker laid all
173 out in `.bss` (see `members/phyre-default-instances.tsv`). Static objects **do not overlap**.
So sorting the default instances by address and advancing each by this table's instance size is a
test the table can fail.

**It does not fail: 0 overlaps across all 173**, spanning `02CA99F0`…`02EB9E00`.

The result is only as sharp as the packing is tight, and in places it is exactly tight — these
would collide on a single byte of error:

| default instance | class | size | ends | next | gap |
|---|---|---|---|---|---|
| `02CBEDD0` | `PRenderTargetBase` | `0x10` | `02CBEDE0` | `PMaterialSwitch` | **0** |
| `02CBF760` | `PSceneRenderPass` | `0x50` | `02CBF7B0` | `PShaderParameterCaptureBufferD…` | **0** |
| `02CBE9B0` | `PConstantBufferBase` | `0xC` | `02CBE9BC` | `PMeshInstanceBounds` | 4 |
| `02CBEC50` | `PMeshInstanceAttachPoint` | `0x18` | `02CBEC68` | `PShaderParameterCaptureBufferL…` | 8 |
| `02E47210` | `PPhysicsShapeBase` | `0x68` | `02E47278` | `PPhysicsPlaneBase` | 8 |
| `02CBED40` | `PStructuredBufferBase` | `0x14` | `02CBED54` | `PShaderParameterCaptureBufferL…` | 12 |

Two exact abutments and four near-misses agreeing with a size read from a completely different
instruction is not a coincidence the table could survive if the sizes were wrong.

**What it does not prove.** Non-overlap is a one-sided test: a size that is too *small* passes it
trivially. It rules out over-statement, not under-statement. Under-statement is what the earlier
control covers — the 177 independently derived Phyre reflection member rows all fit inside their
stated sizes, and 15 sum exactly, which is a lower bound. The two controls bound the sizes from
opposite directions and they are not the same evidence.
