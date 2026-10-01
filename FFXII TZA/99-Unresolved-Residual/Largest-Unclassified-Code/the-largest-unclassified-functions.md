---
system: The largest unclassified functions — 2.67 MB the GFZ owns but does not classify
category: 99-Unresolved-Residual
status: PARTIAL — what the packed-id bucket registry family holds (BI-11) is answered 2026-09-27 (OPUS); the two items this status used to name, the second index list +0x174 (BI-3b) and what distinguishes the two out-of-line draw paths from inline (BI-3c), are answered in the register (restated 2026-09-26 (FABLE, Claude Opus 5.5) from the 2026-09-18 measurements); the three labels of §20's untested list, which were never registered, are answered 2026-09-30, and the page's residue is registered as SD-120 to SD-123 (status line current 2026-09-30, SWE2-DATA)
evidence_tier: 1
owner_layer: mixed PrimaryOwner, no CodeDomain
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 12
  last_pass: 2026-09-02
  last_pass_state: GN158 checkpoint 2ed8affb… / snapshot 46f02e26… / residual c5d4b7f7…, sections 12-15 re-derived in project GFZ_HD2
  falsification_passes: 2
  last_falsification: 2026-09-02
  last_falsification_by: repos-d2
  last_falsification_state: GN158 checkpoint, residual sha c5d4b7f7…, project GFZ_HD2
  falsification_result: pass 1 (repos-9e) 5 overturned / 8 survived, section 20; pass 2 (repos-d2, sections 12-15) 5 overturned / 7 survived, section 21
---

# The largest unclassified functions

**A second residual, larger than the famous one and differently shaped.**
[The unresolved 158](../the-unresolved-158.md) covers functions with *no owner at all*. This covers a
bigger set: **10,024 functions carrying 2,524,402 bytes that have no `CodeDomain`** — and **9,409 of
them do have a `PrimaryOwner`**.

> **Corrected 2026-09-14 (aggregate-claims sweep).** The headline read 10,152 / 2,666,058 — the
> GN158-era figures. R109's additive GN161 batch removed 128 functions from the untagged set
> (the residual cell dropped 139→30; `codeDomain` rose 28,009→28,137). The 9,409 owner-only cell
> is unchanged — owner and CodeDomain never co-occur, so R109 could only tag ownerless functions. The GFZ knows whose code it is. It does not say what the code does.

> **Corrected 2026-09-02 by falsification pass 1 (§20).** These figures read **10,154** and
> **2,667,070** until that pass. They were computed from `Tools/work/graph/functions.tsv`, which is
> stale by the two functions the GN checkpoint closed — the exact defect
> [the-unresolved-158 §13](../the-unresolved-158.md) records as *"a census over `functions.tsv` will
> return 160 and be wrong by construction."* The corrected values are derived from the certified
> ledger and reproduced independently. **The 9,409 was right and is unchanged.**

**`PARTIAL` deliberately.** The three largest are characterised and placed in their call chains.
**None of the three is identified.**

## 1. What the player sees

~~Unknown, and that is the finding worth stating plainly.~~ These are among the largest functions in the
game — 21 KB each — sitting in the **Presentation** layer, which means a player is looking at their
output constantly. ~~**The database cannot yet say which part of the screen they are responsible for.**~~
*(Corrected 2026-09-30, SWE2-DATA: the later sections say which. `003CD840` and `003D2B60` belong to the render-model subresource-variant binding system that the `CharacterRenderRecord_*` binding pair drives, so they serve character rendering (§19). `00438860` is one of the draw paths of an effect's per-frame mesh, effect element type `0x05` (§22). What each binding operation does is still `SD-120`.)*

## 2. Native mechanism

### The three largest, and they are three different animals

| address | size | instructions | SIMD | direct calls | character |
|---|---:|---:|---:|---:|---|
| `003CD840` | **21,276** | 4,128 | **66 %** | **0** | pure integer-SIMD, **calls nothing** |
| `003D2B60` | **20,710** | 3,795 | 33 % | 7 (1 distinct) | comparison-heavy over packed data |
| `00438860` | **20,603** | 4,198 | 20 % | **448** (45 distinct) | ~~pointer fixup at scale~~ a mesh draw path of effect element type `0x05` (§22) |

**`003CD840` is the one that stands out.** 21 KB, 4,128 instructions, **not a single call**, and its
opcode profile is integer SIMD shuffling rather than float maths:

```
movd 882    psrldq 686    movdqa 588    pextrw 294    movups 294
```

~~`psrldq` and `pextrw` in that volume, with no calls and no strings, is **the shape of a codec or an
unpacker**.~~ **CORRECTED in section 10 — it is not a codec.** It is straight-line data
transformation, and it is explicitly not the float arithmetic of
[the builder region](../../00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md),
but the destination pattern rules out a stream codec.

**`00438860` is the opposite:** 448 direct calls, of which **239 are to
`ImageAddress_ResolveRuntimePointer`** — the RVA-to-pointer resolver this database documents in eight
places.

### Two chains, discovered by call-scan

```
CHAIN A                                    CHAIN B
00258D70 / 00258E40                        002F4020
   -> 003CCF20  (887 B, 12 callees)           -> 00449AB0  (1,741 B)
        -> 003CD840   21 KB, 0 calls               -> 004355D0  (5,936 B, 76 resolves)
        -> 003D2B60   20 KB                             -> 00438860 (20,603 B, 239 resolves)
```

**Chain B performs 315 pointer resolutions across two functions**, and both are dominated by the
**same struct field**: `+0x170`, touched **143 times** in `00438860` and **71** in `004355D0`. They
operate on one object type.

> **Read 2026-09-14 (FABLE), §22: these are not fixups.** The object is a loaded effect mesh record (resource kind
> `0x54`), and `+0x170` is its u16 index list, stored as an image-relative u32. The draw code resolves that one
> field again for every index it reads, so the 315 calls are repeated dereferences of five fields of one record.
> Nothing is relocated.

### Both chains write into memory with no file image

```
00438860 RIP targets : .data 022D9000  x198     <- beyond raw
004355D0 RIP targets : .data 02AEE000  x12      <- beyond raw
.data raw covers only : 01DF0000 .. 01F7E400   <- corrected 2026-09-13, see below
```

**Every one of those targets lies past the section's raw extent.** *(The boundary above read
`020793F0` until 2026-09-13 and was wrong by about a megabyte. The section table says `.data` is
`VirtualAddress 01DF0000`, `SizeOfRawData 0018E400`, so the raw image ends at **`01F7E400`** — the
figure eight other documents already use, and this page was the only place carrying the other one,
so nothing propagated. **The conclusion is unaffected**: `022D9000` and `02AEE000` are past either
boundary. A wrong number that does not change a conclusion is still a wrong number in a page other
pages cite for exactly this fact.)*

This is the **second independent
system** found doing that — the builder region at `0x480000` constructs into `02ADEF40`–`02AED330` by
the same trick. **FFXII builds a great deal of its static-looking data at run time.**

## 3. Key addresses

| | |
|---|---|
| untagged functions | **10,024**, **2,524,402 bytes** (corrected, §20; re-derived at GN161 2026-09-14) |
| of those, with a `PrimaryOwner` | **9,409** |
| largest three | `003CD840`, `003D2B60`, `00438860` |
| chain A | `00258D70` / `00258E40` → `003CCF20` → the two SIMD kernels |
| chain B | `002F4020` → `00449AB0` → `004355D0` → `00438860` |
| chain B's shared field | `+0x170` |
| chain B's fixup targets | `.data 022D9000` (×198), `.data 02AEE000` (×12) |

**Where the untagged mass sits** (64 KB buckets, by untagged bytes):

```
00430000  50 fn   68,447 B     00450000  92 fn  64,931 B
007B0000 241 fn   64,301 B     007E0000 248 fn  63,160 B
00540000  71 fn   62,937 B     00520000 109 fn  62,832 B
```

**Audio-layer adjacency, accounted.** The unclassified set is not layer-isolated: 22 call edges
cross into **Audio** — `002DEBB0` is called by `003EA540`/`003E9B10`/`003E9C10`/`003EA430`,
`00181DD0` by five Audio bodies (`003B99D0`, `003D7DC0`, `003D7E90`, `003D7CE0`, `00332C40`),
`00258D70`/`00258E40` call `003D7DC0`, the `0036DD90` accessor family is called by `00361DE0`/
`003623C0`, `0036B130` by `003A1650`, `003C8B70` calls `00249C60`, and the `007B0000`-band member
bodies neighbour the `007DFxxx`/`007Exxxx` Audio cluster on both sides. Unclassified means *no
domain tag*, not *no callers* — audio code already consumes several of these bodies.

## 4. Data structures and formulas

~~**Not established.** `+0x170` is the field chain B revolves around; its meaning is unknown. The
`022D9000` table is walked 198 times; its layout is unread.~~ **Superseded 2026-09-14.** `+0x170` is the
index list of the kind-`0x54` effect mesh record, whose whole layout the loader `00436D00` fixes (§22.2). `022D9000`
is the VU0 register bank ([the EE and VU0 register bank](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md)).

## 5. Call chain

See section 2 — the two chains are the structural result.

*Stated 2026-09-30 (SWE2-DATA) from §3, §19, §20 and §22:*

```
bind:     00258D70 / 00258E40 -> 003CCF20 (8-opcode dispatcher) -> 0050xxxx operations
          per pending entry: 003CD840 on its target; after its operation list, the tail -> 003D2B60
release:  0053AB50 -> 003CD2C0 (the same 8-opcode map) -> 003CD650 release
enqueue:  RenderModelInstance_EnsureSubresourceVariantBinding (00504D30) -> 003CCB60
          RenderModelInstance_RemoveSubresourceVariantBinding (00504610) -> 003CD5D0
chain B:  002F4020 -> 00449AB0 -> 004355D0 -> 00438860 / 00437130 / the inline path
```

## 6. Modding notes

- **`003CD840` calls nothing** — confirmed, 0 callees. ~~and is called from one dispatcher~~
  **OVERTURNED §20: it has three callers** (`003CCF20`, `003CD2C0`, `00431B10`), and it is **not** self-contained:
  it reads 6 and writes 21 fixed globals (section 10). Its contract is that global state, not its
  arguments — so it cannot be replaced without reproducing the state layout.
- **Chain B's fixups run over runtime-built memory**, so nothing in it can be patched in the file.

## 7. What is not known

- [x] ~~What `003CD840` is a state machine for.~~ **PARTLY ANSWERED - the machine has no
      class identity** (section 17): not an object, no vtable, no RTTI, so no name exists to be
      found. **What it DOES is still unknown.** **BI-1.**
- [x] ~~What `003D2B60` classifies.~~ **PARTLY ANSWERED - it is the same machine as `003CD840`**, not a separate system: **6 of 6 load addresses and 21 of 21 store addresses in common**, and each reads five globals the other writes. Section 11. **What the machine models is still unknown. BI-2.**
- [x] What `00438860` and `004355D0` fix up — **315 pointer resolutions** over an object keyed on
      `+0x170`, into a `.data` table with no file image. **BI-3.**
      *Narrowed 2026-09-14 (FABLE):* chain B is effect element type `0x05`'s walk (`00449AB0` → `004355D0` → `00438860`).
      The "`.data` table" is the VU0 register bank ([the EE and VU0 register bank](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md)).
      What the resolves walk in the element definition is still unread.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (§22):* **nothing is fixed up.** The
      object is a loaded kind-`0x54` effect mesh record. All 315 resolves are dereferences of five image-relative u32
      fields of it: 214 `+0x170`, 90 `+0x20`, 9 `+0x174`, 2 `+0x188`. The index-list field is re-resolved at every
      index read.
- [x] What `+0x170` is. **BI-4.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (§22.2):* the mesh record's primitive
      index list, u16 × (3 · `+0x10` triangles + 4 · `+0x12` quads), present when header bit 0 is set. Its size is fixed by the
      loader `00436D00` (`00436F5B`–`00436F80`) and its stride by the draw loops (`00435E54` step 3, quads at `00435E80`).
- [x] ~~Whether the **9,409 owned-but-unclassified functions** are unclassified for one reason or many.~~
      **The GFZ assigns them an owner and then declines to say more, and why is not known.** **BI-5.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror: **one cause, and it is the pipeline's rule,
      not the functions' difficulty.*** Over all 38,161 functions of the exported table (`Tools/work/graph/functions.tsv`),
      the owner column and the `GFZ.V121.CodeDomain.*` tags **never co-occur**. The four cells are: CodeDomain only 28,028;
      owner only 9,409; FinalNoPrimaryOwner only 585; neither 139 (the residual)
      *(GN158 figures; at GN161 the cells are 28,137 / 9,409 / 585 / 30 — the decomposition and the co-occurrence rule are unchanged)*. The ledger enforces this.
      `ReportV121Coverage.java` counts a function as explicit when it has an owner, a FinalNo or a CodeDomain, and counts
      **`overlap`** when more than one applies. `Tools/ghidra/run/Verify-GfzCheckpoint.ps1` line 60 fails any checkpoint
      whose overlap is not 0. So the V121 CodeDomain pass could only label functions that had no owner, and an owned
      function gets no mechanism label by construction. **The verifier and [the evidence standard](../../_index/EVIDENCE-STANDARD.md)
      agree**: the standard states the rule itself in the imperative (*cross-layer overlap must remain 0*, one label per
      function), and its worked example `002F7380` is **two functions**, a Movement-owned caller and a callee whose
      CodeDomain is Presentation. `002F7380` itself carries an empty owner and one CodeDomain tag. The 9,409 are
      therefore not "declined". They are the population the mechanism layer was never applied to (EC-7 frames them as
      **unclassified-by-pipeline**), and nothing about any one of them is implied by its lack of a tag. Ruled by OPUS in
      `FABLE-NOTICE-OPUS-LAYER-OVERLAP-RULE` (commit eb0b4465), which accepted this consequence.
      *(Corrected 2026-09-14: this note first said the standard describes the layers as "orthogonal" and that the checkpoint
      makes them exclusive, as if the two disagreed. They do not. The defect was the standard's old heading word
      "orthogonal", which OPUS replaced with "independent layers — one label per function".)*

- [x] What each of the eight `0050xxxx` binding operations does: the opcode to operation map is decoded (§16, §20) but no operation body is read (§18, §19). **SD-120** (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30; register row SD-120, record [`sd120-binding-ops-0930`](../../_index/candidates/sd120-binding-ops-0930/README.md).)*
- [x] What the three dword arrays at `022D97B0` / `022D98B0` / `022D99B0` hold (§12). **SD-121** (SWE2-DATA, 2026-09-30). *(SD-121 answered 2026-09-30 by OPUS `06230b6a0`, [record](../../_index/candidates/sd121-effect-actor-slots-0930/README.md).)*
- [x] The binding record's 32-byte payload, what its `+0x34` is bounded against, and who writes `+0x38` / `+0x40` (§18). **SD-122** (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30, FABLE, [record](../../_index/candidates/sd122-binding-record-fable-0930/README.md): the payload is 48 bytes (`+0x00`-`+0x2F`, three `movups` pairs in the allocator `003CCC20`), not 32; `+0x34` is the record's elapsed-time word: the updater `003CCF20` counts the start delay `+0x0A` down by its per-call step, seeds `+0x34` with the overshoot and then advances it, and bounds it by the payload's duration word `+0x08` (0 = no limit; past it the expiry path at `003CD009` runs); `+0x38` / `+0x40` are the next / prev links the allocator writes when it inserts the record into its handle-table entry's list (head `+0x28`, tail `+0x30`), ordered by payload byte `+2` (`sd122_record.py`, FAILS 0).)*
- [x] What effect record kind `0x52` (the mesh record's `+0x184` handles) is (§22.5). **SD-123** (SWE2-DATA, 2026-09-30). *(SD-123 answered 2026-09-30 by OPUS `524d5aacd`, [record](../../_index/candidates/sd123-kind52-image-record-0930/README.md).)*

## 8. Evidence

**Tier 1** for the census, the chains and the instruction profiles; **nothing is claimed about
purpose.**

~~**The census is exact.**~~ **OVERTURNED §20 — it was over by two, and the stated check could not
have caught it.** A function is counted here if its tag string contains no `CodeDomain`. The claimed
guard — *"the owner column reproduces the ledger's `owner=9409` exactly, which is the check that the
column is being read correctly"* — **is vacuous**: the ledger reports `overlap=0`, so every owned
function lacks a `CodeDomain` by construction and the owner count among untagged functions is 9,409
**whatever the CodeDomain filter does**. §20 demonstrates it passing with a filter that misclassifies
all 38,161 functions.

**The chains were traced by decoding every `E8` in `.text`** and attributing each site to its
containing function. Adjacency is a banned evidence class here and is not used.

**The instruction profiles are counts, not readings — and one of them was wrong.** "Codec or
unpacker" for `003CD840` was inferred from opcode mix (`psrldq`, `pextrw`, `movdqa` in volume, no
calls, no strings), published as a shape, and **overturned one pass later by reading the function**:
the opcode census cannot see *where* the data goes, and the destinations are 21 literal globals
rather than a stream. **An opcode profile constrains what code does to values; it says nothing about
what it does to memory.** `003D2B60` and the chain-B pair remain profiled-but-unread, and ~~**BI-2**
through **BI-4** hold their semantic questions open on exactly the same footing the codec reading
had before it fell.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **BI-3** and **BI-4** were answered on 2026-09-14 (BI-4: `+0x170` is the mesh record's primitive index list). **BI-2** is partly answered: the function is not a separate system but part of chain A's emulated machine, whose meaning stays with BI-1.*

**One caution about the framing.** Calling this "a second residual" is a description of the ledger's
state, not a claim that these functions resisted classification for the same reason as
[the 158](../the-unresolved-158.md). **They are a different set with a different cause**: the 158 have
no owner at all, while 9,409 of these have one. **BI-5** asks why, rather than assuming the two sets
are alike.

## 9. Related

- [`../the-unresolved-158.md`](../the-unresolved-158.md) — the smaller residual, with no owner at all.
- [`../../00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md`](../../00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md)
  — the other system found writing into `.data` with no file image.
- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — `ImageAddress_ResolveRuntimePointer`, which chain B calls 315 times.

## 10. `003CD840` read — and the "codec" reading is wrong

The shape guess in section 2 was checkable and **it fails on the destinations.**

### What it actually does

```asm
003CD855  movups xmm1, [rip -> 022D8F..]     ; load 16 bytes from a fixed global
003CD86A  movd   eax, xmm1                   ; take byte 0
003CD877  mov    byte ptr [rip -> ...], al   ; store it to a fixed global
003CD872  psrldq xmm0, 1                     ; shift, take byte 1
003CD885  psrldq xmm0, 2                     ; byte 2
003CD898  psrldq xmm0, 3                     ; byte 3   ... and so on, unrolled
```

**Every address on both sides is a fixed global, and there are very few of them:**

| | |
|---|---|
| loads | **299 sites, 6 distinct addresses**, all `movups` (128-bit), `022D8F10`–`022D8FD0` |
| stores | **1,235 sites, 21 distinct addresses**, all byte/word `mov`, `022D8F90`–`022D94A0` |
| per destination | each of the 21 is written **~59 times** |
| control flow | **one** backward branch, spanning **14,011 bytes** |

### Why that is not a codec

**A codec streams.** It walks a source buffer and a destination buffer through registers that advance,
and its addresses are computed, not literal. **This does the opposite**: it hammers **21 fixed
addresses** 1,235 times, reading from **6 fixed vectors**, with almost no branching — 21 KB of code
and a single loop.

> **It is a state machine over a small fixed register file, fully unrolled** — load a 16-byte
> "register", extract its bytes, write them to individually-addressed state, repeat. The 1,296-byte
> span of the destinations is the size of the state it maintains.

**What it is a state machine *for* is still unknown**, and that is the honest limit. The combination —
16-byte vector registers, byte-addressable state, no calls, no strings, and a PS2-heritage codebase
([the `Gi*` family](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)
carries the PlayStation 2 Graphics Synthesizer vocabulary) — is *suggestive* of emulating a
fixed-function unit. **That is a suggestion, not a finding, and it is not asserted.** **BI-1** stays
open with a sharper description.

> **2026-09-14 (FABLE): the suggestion is now a finding for the globals.** The `022D8F10`–`022D94A0` state is the
> register bank of the PS2 assembly emulation, which the engine names (`"PS2 Assembly emulation initilization
> completed!"`, `0036D990`). `003CD840` and `003D2B60` use EE general-purpose registers t0–t5 with 980 and 339
> MMI-shaped SIMD instructions, so their bodies are translated MMI assembly. See
> [the EE and VU0 register bank](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md).
> What the machine binds (BI-1's recorded answer) is unchanged.

### It shares its state with chain B

The globals `003CD840` reads and writes (`022D8F10`–`022D94A0`) sit in the **same `.data` page** that
`00438860` fixes up **198 times** (`022D9000`). **Chain A computes over state that chain B relocates
pointers into.** The two chains that looked unrelated in section 2 touch the same region. **BI-6.**

> **BI-6 ANSWERED 2026-09-14 (FABLE), ledger mirror pending: they share a CPU, not an object.** The region is the
> [EE and VU0 register bank](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md).
> Chain A uses the general-purpose registers. `00438860` uses VU0 ACC and four vector rows (180 writes), and its
> "fixups into `022D9000`" are register writes on that page. The `ImageAddress_ResolveRuntimePointer` calls are a
> separate matter. Chain B is effect element type `0x05`'s walk method (`002F4020` → `00449AB0`,
> [effect type dispatch](../../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md) §2.5),
> which narrows BI-3.

### The dispatcher's menu

`003CCF20` (887 B) calls ten distinct functions ~~and `003CD840` **twice**~~ — **twelve distinct,
§16; and `003CD840` THREE times, §20**:

```
00181DD0     21 B      0036B130     41 B (x3)    003CD840  21,276 B (x2)
0050AC20  6,192 B      00506B40  1,501 B         005080A0   3,048 B
0050A100  2,842 B      00509BB0  1,345 B         00507490   3,074 B
00508C90  3,861 B
```

~~**Six of the ten are 1.3–6.2 KB functions in the `0x0050xxxx` range**~~ **— EIGHT, not six: the 1.3 KB floor dropped `00507120` at 867 B (section 16).** A second cluster of large
code reached from the same dispatcher, and none of them is documented either. **BI-7.**

## 11. The operand test applied to the other two — and chain A is one machine

The measure that overturned the codec reading was applied to the remaining giants. **It separates them
cleanly, and it was validated against the case already settled.**

| | `003CD840` (known) | `003D2B60` | `00438860` |
|---|---:|---:|---:|
| literal-global **loads** | 299 over **6** addrs | 1,039 over **16** | 37 over 14 |
| literal-global **stores** | 1,235 over **21** addrs | 963 over **28** | 189 over 15 |
| **indexed** `[r + r*s]` | **0** | **0** | **234** |
| backward branches | **1** | **1** | **52** |
| literal range | `022D8F10`–`022D94A0` | **`022D8F10`–`022D94A0`** | `008C5FB0`–`02AEED50` |

**The discriminator holds.** A fully-unrolled state machine has **no computed addressing and one
loop**; a table walker has **234 indexed accesses and 52 loops**. The opcode census could not see this
difference — both use the same shuffles.

### `003D2B60` is not a second system. It is the same machine.

The two chain-A functions do not merely sit in the same address range — **they share the actual
addresses**:

```
load addresses in common                    :  6 of 6
store addresses in common                   : 21 of 21
addresses 003CD840 STORES that 003D2B60 LOADS :  5
addresses 003D2B60 STORES that 003CD840 LOADS :  5
combined footprint : 32 distinct addresses, 022D8F10..022D94A0 = 1,424 bytes
```

**Every address `003CD840` touches, `003D2B60` touches too**, and **each reads five globals the other
writes.** That is not two systems sharing a page; it is **two operations over one machine state**,
passing values to each other through it.

> **Chain A is a single emulated machine with a ~1,424-byte register file, and the dispatcher
> `003CCF20` selects between its operations.** The dispatcher calls `003CD840` twice among ten
> callees, **eight** of which are further functions in `0x0050xxxx` (**BI-7, answered in section 16**) — candidates for
> being further operations of the same machine.

**What the machine models is still unknown.** Naming it would need the meaning of the 32 globals, and
none has been decoded. **BI-1** stands.

### `00438860` is confirmed as the odd one out

234 indexed accesses, 52 loops, and a literal range spanning `.rdata` through high `.data` — the
profile of code that **walks structures** rather than maintaining state. That is consistent with its
239 `ImageAddress_ResolveRuntimePointer` calls and with `+0x170` dominating its field access, and it
places it firmly with chain B rather than with the two above.

## 12. The state identified — a global transform block, and a qualification of §11

Asking **who else touches `022D8F00`–`022D9500`** identified it. **267 functions do**, and the small
ones are accessors that name the structure.

### A 4×4 matrix with a getter and a setter

```asm
003970A0  (44 B)   movups xmm0, [022D91B0] ; movups [rcx],      xmm0
                   movups xmm1, [022D91C0] ; movups [rcx+0x10], xmm1
                   movups xmm0, [022D91D0] ; movups [rcx+0x20], xmm0
                   movups xmm1, [022D91E0] ; movups [rcx+0x30], xmm1

0039AF70  (44 B)   the exact inverse — [rcx+0x00..0x30] -> 022D91B0..022D91E0
```

**Four consecutive 16-byte vectors at a 0x10 stride is a 4×4 matrix**, and these two functions are its
**getter and setter**. `022D91B0`–`022D91EF` is **64 bytes of global transform.**

### Vector arithmetic primitives over the same block

```asm
003A2B60  (42 B)   cvtdq2ps ; shufps xmm0,xmm0,0 ; mulps   — scale a vector by a broadcast int
003A28C0  (53 B)   shufps xmm0,xmm0,0 ; addps              — add a broadcast scalar
003A2B20  (53 B)   shufps xmm0,xmm0,0 ; mulps              — multiply by a broadcast scalar
```

Each reads and writes `[rcx]` **and** mirrors the operand into `022D92E0` / `022D92F0` — a scratch pair
beside the matrix.

### A 32-entry descriptor table at `022D94B0`

```asm
0036E500 / 0036DF80 / 0036E5E0 :
    cmp ecx, 0x1F ; cmovg ecx, eax        <- index clamped to 31  => 32 entries
    lea rcx, [rax + rax*2]                <- index * 3
    lea rax, [022D94B0]
    mov eax, [rax + rcx*8]                <- *3*8 = STRIDE 24 BYTES
    cmp word ptr [rax + rcx*8 + 4], 0     <- a 16-bit TYPE TAG at +4
```

**32 entries of 24 bytes, with a type tag at `+4`** — one variant tests it against `0`, another against
`3`. A descriptor table, bounds-clamped rather than validated.

### What this makes the region

**A shared global transform / geometry state block**, not one function's private machine:

| range | what |
|---|---|
| `022D8F10`–`022D8FD0` | chain A's byte-addressed vector registers |
| `022D91A0`–`022D91E0` | **the 4×4 matrix** (getter `003970A0`, setter `0039AF70`) |
| `022D92E0`–`022D92F0` | vector-arithmetic scratch |
| `022D9470` | a dword touched by `or […], 0` in two 8/11-byte functions |
| `022D94B0` | **32 × 24-byte descriptor table**, type tag at `+4` |

`RelationLook_SolveAnglesAndMatrices` (`005131C0`) — the one **named** function among the heavy users —
touches **53** addresses here, concentrated on `022D91A0`–`022D91E0`, with **178 `movss`**: scalar float
access into the matrix. Its name and its access pattern agree.

### This qualifies §11

> §11 called chain A's 32 addresses "a ~1,424-byte register file" belonging to one machine.
> **The two functions do share those 32 addresses exactly — that stands.** But the region they sit in
> is **much larger and shared with 267 functions**, and chain A overlaps
> `RelationLook_SolveAnglesAndMatrices` on only **4** addresses (`022D8F90`–`022D8F9C`).

**So chain A works one sub-block of a shared transform state; it does not own the region.** The
footprint measurement was right and the ownership implied by calling it "its register file" was too
strong. **What chain A computes over that sub-block is still unknown — BI-1 stands** — but it is now
positioned inside an identified structure rather than floating.

## 13. The descriptor table decoded — 32 typed slots with an accessor family

**BI-8 advanced.** The table at `022D94B0` is referenced by **16 functions**.

> **OVERTURNED in section 21.** This paragraph said the table `022D94B0` has *"no writer anywhere in `.text`"*,
> that *"all 16 only read"*, and that *"like everything else in this region it is built at run time,
> through a computed pointer rather than a literal address."* **All three are false.** At least eight
> of the sixteen write into the table through a register `lea`-d from the **literal** base
> `022D94B0`; `0036E320` initialises a slot (`+0x00`, `+0x04`, `+0x08`, `+0x10`) and `0036E540`
> writes the tag.
>
> **A ninth writer, added 2026-09-08, and it was named nowhere in this database:** `0036E3B0`
> writes the table through an **image-base** register rather than a literal `lea`, which is why no
> RIP-relative scan could see it — the blind spot recorded as `DD-3`. It writes six locations:
>
> ```text
> 0036E3DB  mov dword [r9 + rcx*8 + 0x21b94b0], r8d   -> 022D94B0
> 0036E3E3  mov word  [r9 + rcx*8 + 0x21b94b4], r8w   -> 022D94B4
> 0036E3EC  mov qword [r9 + rcx*8 + 0x21b94c0], r8    -> 022D94C0
> 0036E414  mov dword [r9 + rcx*4 + 0x21b97b0], r8d   -> 022D97B0
> 0036E42F  mov dword [r9 + rcx*4 + 0x21b98b0], r8d   -> 022D98B0
> 0036E44C  mov dword [r9 + rcx*4 + 0x21b99b0], r8d   -> 022D99B0
> ```
>
> The `rcx*8` on the first three and `rcx*4` on the last three, at bases `0x100` apart, are stated
> as read; **what the three arrays at `022D97B0`/`022D98B0`/`022D99B0` are is not established** (`SD-121`; 2026-09-30, SWE2-DATA: [the world-tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) reads a slot clearer over the first two), and
> `0036E3B0`'s body was not read beyond these six sites. §12's own matrix setter `0039AF70` also writes the region through a literal
> RIP-relative address, so this document contradicted itself one section apart.

**The 16 readers are an accessor family**, 8–179 bytes each, in one tight range
`0036DD90`–`0036E5E0`:

| accessor | size | entry offsets | widths | index clamp | tag test | tail |
|---|---:|---|---|---|---|---|
| `0036DF80` | 49 | `+0` | u16, u32 | `0x1F` | **`== 0`** | `003B27A0` |
| `0036E460` | 73 | `+0` | u32 ×2 | `0x1F` | **`== 0`** | internal |
| `0036E500` | 52 | `+0` | u32 ×2 | `0x1F` | — | — |
| `0036E540` | 93 | `+0` | u16 | `0x1F` | **`== 1`** | internal |
| `0036E5A0` | 54 | `+0` | u16 ×2 | `0x1F` | — | — |
| `0036E5E0` | 51 | `+0` | u16, u32 | `0x1F` | **`== 3`** | `0024FDA0` |
| `0036E290` | 125 | `+0` | — | `0x1F` | — | — |
| `0036DDC0` | 91 | `+0` | — | `0xFFFB` | — | `thunk_FUN_003B18E0` |
| `0036E320` | 133 | `+0` | — | `0x1000` | — | internal |

### What the table is

```
32 entries x 24 bytes at 022D94B0
   +0x00  u32   payload          written by 0036E320, 0036E1E0, 0036E460
   +0x04  u16   TYPE TAG      — tested against 0, 1 and 3; WRITTEN as 1, 2 and others
   +0x06  u16                 written by 0036E1E0
   +0x08  u8                  written by 0036E320
   +0x10  u64                 zeroed by 0036E320
   +0x0A .. +0x17  still unread   (see section 21)
```

**A typed slot table.** Six accessors clamp the index to `0x1F` — **32 slots** — read the payload at
`+0`, and **branch on the tag at `+4`**, tail-calling a different handler per type. Tag values **0, 1
and 3** are tested in the family.

> **Corrected in section 21.** Tag **2** is not tested but it **is written**, by `0036E540`, as a
> transition out of tag 1. The tag is a **lifecycle state** as well as a type discriminator. Also,
> the row below for `0036E460` mis-records its test: it compares the **payload `u32` at `+0`**
> against zero, not the tag at `+4`.

Two accessors use different clamps — `0xFFFB` and `0x1000` — so **not every function in the family
indexes this table the same way**, and those two are not established as belonging to it.

**What the slots hold is still unknown.** The payload is a `u32` read and passed on; the tag selects a
handler; neither has been followed. **BI-8** stays open with a defined shape.
*Status 2026-09-26 (FABLE, Claude Opus 5.5): kept as history. **BI-8** was answered on 2026-09-14 further down this
page ("`BI-8` answered 2026-09-14"): the table is the per-manager list of script-requested event-effect loads.*

### The pattern this region keeps repeating

**Three structures in `022D8F00`–`022D9500` are now identified by their accessors, and none by its
data:** the 4×4 matrix (§12), the vector-arithmetic scratch (§12), and this table. **All are in
uninitialised `.data` with no file image, and all are read by small dedicated functions.** In a region
where the data cannot be read statically, **the accessors are the schema** — which is why 8-byte
functions turned out to be worth reading.

## 14. The tag handlers — a handle encoding, read out

The accessor family tail-calls a different handler per tag. Two are decoded.

### Tag 3 → `0024FDA0`: the top nibble of a 32-bit id selects a bucket

```asm
0024FDA9  mov   eax, ecx
0024FDAE  sar   eax, 0x1C            ; >> 28
0024FDB3  and   al,  0xF             ; keep 4 bits   -> the TOP NIBBLE of the id
0024FDB8  lea   rax, [rip -> table]
0024FDBF  mov   rcx, [rax + rcx*8]   ; 16 bucket heads
0024FDC6  je    <miss>               ; empty bucket
      ; walk the chain
0024FDD0  cmp   word ptr [rcx + 4], r8w   ; match key A (u16)
0024FDD7  cmp   word ptr [rcx + 6], ax    ; match key B (u16)
0024FDDD  mov   rcx, [rcx + 0x348]        ; next in chain
0024FDE7  jne   0024FDD0
```

**A 32-bit handle whose top 4 bits are a bucket selector**, resolving through **16 bucket heads** into
records **chained at `+0x348`** and matched on **two 16-bit keys at `+4` and `+6`**.

| | |
|---|---|
| id bits 28–31 | bucket index, 0–15 |
| bucket table | 16 pointers |
| record chain link | `+0x348` — so a record is at least 0x350 bytes |
| match keys | `u16` at `+4` **and** `u16` at `+6` |

**Two keys, not one.** The second comes from the caller's stack (`[rsp+0x32]`), so a lookup takes a
handle **and** a qualifier — the same record chain is searched for a specific pair.

### Tag 0 → `003B27A0`: a bounded linear scan over an 11-entry table

> **OVERTURNED in section 21, twice.** The polarity is backwards — `0036DF80` does
> `cmp [slot+4], 0` / `je` **skip** / `jmp 003B27A0`, so the handler is reached when the tag is
> **non-zero**; tag 0 means *no handler*. And the table is **32 entries**, not 11: the walk is
> bounded by `rdx = base + 0x600`, and `0x600 / 0x30 = 32`. The `0xB` is a bound on the second
> argument, which this section correctly says and then does not apply.

```asm
003B27B4  cmp  edi, 0xB            ; reject >= 11
003B27BE  lea  rdx, [rip -> end]
003B27C5  lea  rbx, [rip -> base]
003B27D0  mov  eax, [rbx]          ; key at +0
003B27D4  je   <empty>             ; zero terminates
003B27D6  cmp  eax, ecx            ; match
003B27DA  add  rbx, 0x30           ; STRIDE 48 BYTES
003B27DE  cmp  rbx, rdx
```

**A table of at most 11 entries, 48 bytes each, keyed on a `u32` at `+0`, with zero as a terminator.**
The `0xB` bound is on the *second* argument, not the table walk — the walk is bounded by `rdx`.

### What this adds up to

The descriptor table's tag is a **discriminated union selector**, and the two decoded arms resolve
completely different things:

```
descriptor slot (32 max)
  +0  u32 payload
  +4  u16 tag  --> 0   : NO handler - 0036DF80 returns without calling
                   !=0 : bounded linear scan, 32 x 48 B table at 02EBE5E0, u32 key   [corrected, s21]
                   1   : 0036E540 queries, and on success WRITES the tag to 2        [s21]
                   3   : hashed handle resolve, top-nibble bucket, chained +0x348
```

**These are not two views of one structure.** A 48-byte flat table and a 0x350-byte chained record set
have nothing in common but the accessor that reaches them. **The tag is a real type discriminator, and
the slots hold references to unrelated object kinds.**

**Still unknown:** what any of it *holds*. **BI-8** narrows to: what the 32-entry `48`-byte table
at `02EBE5E0` and the bucketed record set contain. The handle encoding is now the most tractable lead — **an id with a
4-bit type field in its top nibble is a pattern that shows up in authored data**, and this database
has [an id-encoding document](../../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)
that may or may not be the same scheme. **That is a lead, not a claim — nothing has been compared.**

## 15. BI-10 answered — not the same scheme, but a house convention

The resemblance between the tag-3 handle encoding and the documented
[item id encoding](../../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)
was recorded as a lead. **Tested: they are different schemes.**

| | item ids | the tag-3 handle |
|---|---|---|
| width | **16-bit** | **32-bit** |
| type field | bits **15..12** (`id >> 0xC`) | bits **31..28** (`sar 0x1C ; and 0xF`) |
| resolution | **direct index**, `record = id - 0x1000` | **bucket + chain**, 16 heads, link at `+0x348` |
| match | index arithmetic | **two `u16` keys** at `+4` and `+6` |

**Different width, different field position, different resolution mechanism.** Sharing "a type field
in the high bits" makes them the same *idiom*, not the same scheme, and **BI-10 is answered NO.**

### But the idiom is a house convention, with at least three variants

Scanning the image for a right shift that leaves a small field, followed within four instructions by
an `AND 0xF`/`0xFF` or a small `CMP`:

```
shift 0xC   16-bit id, bits 15..12   : 15 sites in  6 functions
shift 0x14  bits 31..20              :  2 sites in  2 functions
shift 0x18  bits 31..24              :  2 sites in  2 functions
shift 0x1C  32-bit id, bits 31..28   : 10 sites in 10 functions
                                       29 sites, 19 distinct functions
```

> **Not reproducible as stated — section 21.** The criterion says *"a small `CMP`"* without giving
> the bound, and the figures move with it: taking "small" as `imm <= 0x20` yields **59 sites in 47
> functions**. The *conclusions* survive — several distinct shift widths coexist, and both named
> corroborations hold — but the counts are not checkable without the threshold. **State the
> predicate with a census.**

**At least three distinct packed-id schemes coexist**, and one of the `0x14` sites is a function the
GFZ already names: **`ActorHandle_ResolveRegistryEntryByPackedId`** (`0x003588B0`), documented in
[the party roster](../../11-Party/party-roster-and-control-suppression.md). **The codebase's own
vocabulary for this is "packed id"**, which settles that the convention is intentional rather than
three coincidences.

### An independent corroboration of the tag-3 reading

The ten `0x1C` sites cluster in `0024Cxxx`–`0024Fxxx`, and **the GFZ tags one of them
`Runtime.PackedIdBucketRegistry`** (`0x0024E210`).

> **Qualified in section 21.** The clustering is real but its *exclusivity* is criterion-dependent:
> under the wider predicate 11 of 18 `0x1C` sites fall in `0024xxxx` and seven do not. The
> `0024E210` tag was verified and stands.

> **That name was arrived at without reference to this analysis**, and it independently states the two
> things §14 read out of `0024FDA0`'s disassembly: **packed id**, and **bucket**. Two sources, no
> shared derivation — unlike an agreement between two readings of the same dump.

**What the buckets hold is still unknown.** This does not answer BI-8; it confirms the mechanism and
names the family. **BI-11** records the family as a unit worth reading.

## 16. BI-7 answered — the machine has eight operations, and two of them compose

### Eight, not six

`FUN_003CCF20` calls **twelve** functions: two helpers, chain A's pair, and **eight** in
`0x0050xxxx` — `00506B40`, `00507120`, `00507490`, `005080A0`, `00508C90`, `00509BB0`, `0050A100`,
`0050AC20`.

**§11's "six" was wrong because of an arbitrary size floor.** `00507120` is **867 bytes** and fell
under the 1.3 KB threshold used to list the cluster. **A size cut-off is not a membership test**, and
it silently dropped a real member of the family.

### The dispatcher, decoded

`FUN_003CCF20` walks a work list at `[0x02B47778]`, tests a pending flag (`[rec+1] & 0x80`), and
switches on a **byte opcode at `[rec+0]`** through a jump table at **`0x003CD298`**:

```
003CD101  jmp rcx                      <- computed dispatch
jump table 003CD298 : 8 entries, all landing inside the dispatcher's own body
                      (entry 8 reads as CCDECCCC - past the end, so the table is exactly 8)
```

| opcode | operation | | opcode | operation |
|---:|---|---|---:|---|
| 1 | `0050AC20` | | 5 | `00509BB0` |
| 2 | `00506B40` | | 6 | `00507490` |
| 3 | `005080A0` | | 7 | `00508C90` |
| **4** | **handle-resolve → `003CD840` → `0050A100`** | | **8** | **handle-resolve → `003CD840` → `00507120`** |

Every operation receives a fixed context in `rcx` (`0x02B477A0`) and the record in `rdx`/`r8`.

### Opcodes 4 and 8 are the evidence

**Verified here** by disassembling both dispatch arms:

```
opcode 4 (003CD13F) : call 0036B130 ; call 003CD840  [chain A] ; call 0050A100  [0x0050xxxx]
opcode 8 (003CD1D2) : call 0036B130 ; call 003CD840  [chain A] ; call 00507120  [0x0050xxxx]
```

**A chain-A function and a `0x0050xxxx` function run back to back inside a single dispatch arm.**
That is composition within one operation — and **it rests on nothing but the call sequence**, so it is
independent of any shared-state or access-role measurement.

### They share the register file exactly

```
chain A register file : 022D8F10..022D94A0   1,432 bytes

function     cells   in region   elsewhere        function     cells   in region   elsewhere
003CD840        22          22           0        00508C90        51          50           1
003D2B60        32          32           0        00509BB0        26          25           1
00506B40        27          27           0        0050A100        32          32           0
00507120        21          20           1        0050AC20         9           8           1
00507490        46          45           1
005080A0        48          48           0
```

**All ten confine their global state to that one region** — "elsewhere" is 0 or 1 per function, being
the stack cookie and two singletons. Together they touch **86 cells** of it, against chain A's 32.

*(The analyst's first version of this table reported percentages over 100 %, from counting cells
against chain A's 32-cell subset rather than the address range and summing reads and writes so that
cells doing both were counted twice. **Caught and corrected before publication**; the figures above are
the repaired metric.)*

### Handle resolution, with a generation check

Opcodes 4 and 8 begin with:

```
idx   = (u8)[rec + 0x20]
entry = [0x02B47790] + idx * 64
check   [entry + 4] == [rec + 0x20]        <- GENERATION CHECK
else    fall back to FUN_0036B130
```

**A generation-checked handle table with 64-byte entries** — the standard defence against a stale
handle referring to a recycled slot.

### An adjacency, flagged and not claimed

The register file's last cell is at **`022D94A0`**; the [no-writer descriptor table](#) is at
**`022D94B0`**. **Adjacent, but adjacency is a banned evidence class here**, and the analyst declined
to claim a link. It is recorded only as a reason to look: if the two are one allocation, the
descriptor table's missing writer may be one of these ten operations under an addressing form the
original scan did not match. **Untested. BI-12.**

### What this does not establish

**No operation is individually identified.** Opcode → function and shared state are structural facts;
**not one of the eight bodies has been read** to say what it does. The machine itself is unnamed, and
`[0x02B47778]` (work list), `[0x02B47790]` (handle table), `[0x02B477A0]` (context) and `[0x02B487A0]`
are all unexamined. **BI-1 stands.**

## 17. BI-1 answered — the machine has no name because it is not a class

### The context object is not an object

| test | result |
|---|---|
| how often `0x02B477A0`'s address is taken | **10 times, all inside the dispatcher `FUN_003CCF20`**, nowhere else in the image |
| where it lives | **uninitialised `.data`** — past the section's raw size, so no file image and **no static vtable** |
| vtable calls through `rcx` across all eight operations | **zero** |

**No allocation, no constructor, no vtable, no RTTI.** That is why nothing in the
[vtable index](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) names it — **the name
does not exist to be found.**

### The initializer states the shape

`FUN_003CD6E0` (210 B), verified here:

```asm
003CD6E4  cmp   qword ptr [02B47790], 0    ; lazily
003CD6F5  call  FUN_0036C1D0               ; allocator tag scope open
003CD6FA  mov   ecx, 0x800
003CD6FF  call  FUN_0036A100               ; -> HANDLE TABLE, 2,048 B
003CD70B  call  FUN_0036C140               ; scope close
003CD728  mov   ecx, 0x2800
003CD72D  call  FUN_0036A100               ; -> SECOND TABLE, 10,240 B
003CD74F  mov   dword ptr [02B47774], ...
003CD75A  mov   qword ptr [02B47778], ...  ; work list emptied
003CD761  mov   ecx, 0x20                  ; <- 32, STATED
003CD766  mov   qword ptr [02B47780], ...
```

**`0x800 / 64 = 32`, and `mov ecx, 0x20` states 32 independently in the same function** — the entry
count is not only derived from the allocation size.

### The whole machine

```
static state block   02B47698   272 B of referenced fields, uninitialised .data
  +0x098 (02B47730)  hottest field: 63 reads / 2 writes; written ONLY by two UI functions
  +0x0E0 (02B47778)  work list head
  +0x0F8 (02B47790)  handle table base      (written once, by the init)
  +0x100 (02B47798)  second table base      (written once, by the init)
  +0x108 (02B477A0)  scratch block passed as rcx to every operation
handle table         heap, 32 x 64 B, generation-checked
second table         heap, 10,240 B  — the largest unexamined thing here
register file        022D8F10, 1,432 B static, 86 cells
dispatcher           003CCF20, byte opcode 1-8, ten operations
```

### BI-12 closes as a negative

**None of the ten operations writes into the descriptor table**, tested by tainting every register
loaded with a `lea` into the register file and following writes through it, **including indexed
forms** — not only RIP-relative addressing.

**The instrument was checked for vacuity before the negative was believed:** the taint fired **23
times across two functions**, so for those it had bases to follow and found nothing reaching the
table; **the other eight never form a pointer into the region at all**, touching it only by direct
RIP-relative addressing that stops at `022D94A0`. **Two complementary arguments, not an absence of
opportunity.**

> **The adjacency was a coincidence.** The descriptor table's missing writer is elsewhere, and that
> hypothesis is now **eliminated rather than untested**.

### The general consequence

**Two unnamed things in this database are unnamed for the same reason.** The
[`Gi*` render device](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)
and this machine both resisted every RTTI-based route because **neither is a C++ object**.

> **The vtable index can never reach them.** A 4,275-method index recovered from RTTI has a hard
> ceiling: **subsystems built as static state plus free functions are invisible to it by
> construction**, however large. Two have now been found, both substantial. **That is a property of
> the recovery technique, not a gap in its execution.**

### Still open

- **No operation is semantically identified.** Opcode → function, shared state and composition are
  structural. **BI-1** is answered as *"it has no class identity"*, not as *"here is what it does"*.
- **The 10,240-byte second table is unexamined** — its allocation is known and nothing else. **BI-13.**
- The hot field is written **only by two UI functions** (`003C8A20`, `003C8B70`), which suggests the
  subsystem is UI-driven; **neither writer has been read. BI-14.**
- The 272-byte block is a **referenced-address span**, not a proven structure — adjacency is not
  treated as evidence here.

## 18. BI-13 — the second table is a handle-allocated record pool

**A hypothesis of this database's was disconfirmed.** It was suggested the 10,240-byte table might be
`32 × 320`, with the handle table's cardinality explaining its shape. **It is `128 × 80`.**

```asm
movzx edx, cl               ; index = LOW BYTE of the handle
lea   r8,  [rdx + rdx*4]    ; * 5
shl   r8,  4                ; * 16   ->  * 80
add   r8,  [02B47798]
```

**Stride `0x50` = 80 bytes; `0x2800 / 80 = 128` entries** — and the allocator states both outright:
`add rbx, 0x50` and `cmp edx, 0x80`. **Confirmed three ways** — derived from the allocation size, and
stated twice in code. **The `mov ecx, 0x20` in the initializer is the *handle table's* 32, not this
one's.** Two tables, two counts, and the cardinalities are unrelated.

### The handle format

`FUN_003CCC20` allocates:

```asm
scan 128 slots for [entry+0x30] == 0      ; 0 marks free
gen = ++[02B47774]                        ; 24-bit generation counter
if gen > 0xFFFFFF: gen = 1                ; wraps to 1, never 0
handle = (gen << 8) | index
[entry+0x30] = handle
movups [entry], [arg0] ; movups [entry+0x10], [arg0+0x10]   ; 32-byte payload
```

**`handle = (generation << 8) | index`.** `FUN_003CD650` releases: validates `[entry+0x30] == handle`,
zeroes it, and decrements a refcount in the handle-table entry it links to.

**A concern raised and resolved by the format.** The index is taken as a **full byte** (0–255) while
the pool holds only **128** entries — flagged as a possible overrun. It is not: **the allocator never
assigns an index ≥ 128**, so the range is safe *by construction* rather than by a mask.

### Entry layouts

```
POOL ENTRY (0x50 = 80 B)                  HANDLE-TABLE ENTRY (0x40 = 64 B)
+0x00..0x1F  32-byte payload              +0x00  byte   refcount
   +0x04     byte: index into the         +0x01  byte   flags (tested & 0x3F)
             32-entry handle table        +0x02  word   passed to chain A as arg 3
+0x30 dword  handle; 0 = free             +0x04  dword  handle, generation-validated
+0x34 dword  bounds-checked by dispatch   +0x10         payload pointer
+0x38 qword  pointer, written later       +0x28, +0x30  qwords, written only
+0x40 qword  pointer, written later
```

*(Corrected 2026-09-30, SWE2-DATA, on SWE2-ORACLE's [`sd120-binding-ops-0930`](../../_index/candidates/sd120-binding-ops-0930/README.md) X1 / X2 and FABLE's [`sd122-binding-record-fable-0930`](../../_index/candidates/sd122-binding-record-fable-0930/README.md); [consumer check](../../_index/candidates/data-s18-binding-list-0930/README.md)): the block keeps its first reading, and three of its cells are wrong. In the pool entry, `+0x00..+0x2F` is a 48-byte payload (the operations read their operands at `+0x20..+0x2A`); `+0x34` is the elapsed-time word, bounded by the duration `+0x08`; `+0x38` / `+0x40` are the record's next / prev links. In the handle-table entry, `+0x28` / `+0x30` are the head and tail of that operation list, which both dispatchers read. `003CCC20` links a record in and `003CCF20` unlinks it.)*

**The two tables are cross-linked**: a pool record's payload carries a byte index into the handle
table, and releasing a record decrements that handle entry's refcount. **That is the relationship —
not a shared cardinality**, which was the hypothesis and was wrong.

### Not established

- ~~**The 32-byte payload is opaque** — copied wholesale from the caller; only byte 4 is understood. (`SD-122`)~~ *(Corrected 2026-09-30, FABLE, [record](../../_index/candidates/sd122-binding-record-fable-0930/README.md); this also corrects the "32-byte payload" comments in the two code blocks above:)* the payload is **48 bytes**, `+0x00`-`+0x2F`, copied wholesale by three `movups` pairs; byte 4 is the handle-table index, byte `+2` orders the record in its entry's list, word `+0x08` is its duration, `+0x0A` its start delay (with a spread from `+0x0C`); `+0x34` is elapsed time and `+0x38` / `+0x40` are the list links (`SD-122`, answered).
- ~~`+0x34` is bounds-checked by the dispatcher **against something unidentified**.~~ *(Corrected 2026-09-30, SWE2-DATA: `+0x34` is the elapsed-time counter. The updater `003CCF20` seeds it with the start-delay overshoot and compares it with the duration `+0x08` (`003CCFF5`; [`sd120-binding-ops-0930`](../../_index/candidates/sd120-binding-ops-0930/README.md) D4, `SD-122`).)*
- ~~`+0x38` / `+0x40` are read as pointers later; **their writers were not found**.~~ *(Corrected 2026-09-30, SWE2-DATA: they are the record's next / prev links in its handle-table entry's operation list, whose head and tail are the entry's `+0x28` / `+0x30`. `003CCC20` writes them when it links a record in, `003CCF20` when it unlinks one ([`sd120-binding-ops-0930`](../../_index/candidates/sd120-binding-ops-0930/README.md) X2).)*
- **The field maps come from three user functions only**, with a conservative taint — **the layout is a
  floor, not a census**.
- ~~**No operation body has been read.** Nothing here says what the machine *does*.~~ (`SD-120`) *(Answered 2026-09-30, SWE2-ORACLE, [`sd120-binding-ops-0930`](../../_index/candidates/sd120-binding-ops-0930/README.md): the eight operations are palette (CLUT) animation effects on an 8.8 fixed-point colour table - permute, tint ramp, fade to a colour, fade to another palette, desaturate, tint by strength, colour sweep, and a curve cross-fade to another palette.)*

## 19. The machine identified — and §17's state block was proximity clustering

### First, a correction to §17

§17 described a **272-byte static state block at `02B47698`** with `02B47730` as its hottest field.
**That block was built by clustering referenced addresses on proximity**, which is the banned evidence
class, and §17 even carried the caveat *"I did not verify the 272-byte block is one structure rather
than adjacent globals"* while describing it as the machine's state anyway.

> **Writing the caveat is not the same as heeding it.**

Re-partitioned by **who touches each address** rather than by where it sits:

```
02B47698..02B47768   25 addresses   machine refs:  0   other refs: 100   <- NOT the machine
02B47770..02B477A0    6 addresses   machine refs: 39   other refs:   0   <- the machine
02B47790                            machine 10, other 8                 <- SHARED
```

**The machine's static state is 56 bytes, not 272.** The other 25 addresses belong to an unrelated UI
subsystem that happens to sit immediately before it.

**And `02B47730` is not the machine's field at all** — 65 references, every one from the
`003C8xxx`–`003C9xxx` UI cluster; **none of the ten operations touches it, nor does the dispatcher.**
It is a lazily-created **216-byte UI widget** (`FUN_003C8A20`, factory `FUN_00244F50`) whose message
proc `FUN_003C8B70` handles ids 1, 2, 8, 10, 18 — the same WndProc architecture as the battle-menu
widget in AV-8. **So BI-14 as posed had no answer: the premise that the machine is UI-driven came
from a field that is not the machine's.**

```
CORRECTED STATE BLOCK - 56 bytes
02B47770  byte   flag, zeroed at init
02B47774  dword  handle generation counter (24-bit, wraps to 1)
02B47778  qword  work list head
02B47780  qword  zeroed at init
02B47790  qword  handle table base    <- SHARED: 8 references from outside the machine
02B47798  qword  record pool base
02B477A0         scratch/context passed to every operation
```

**The handle table being indexed from outside the machine is new** — it is a resource table other
subsystems also use, not private state.

### The machine is the render-model subresource-variant binding system

The right question was **who enqueues work**. The work-list head `02B47778` has three writers, and
their callers are **GFZ-named**:

```
FUN_003CCB60  <-  RenderModelInstance_EnsureSubresourceVariantBinding   (00504D30)
FUN_003CD5D0  <-  RenderModelInstance_RemoveSubresourceVariantBinding   (00504610)
              <-  FUN_00504C40, FUN_00468160, FUN_004680D0
```

**Verified here** — both names are in the ledger, alongside a wider family:

```
RenderModelInstance_EnsureSubresourceVariantBinding
RenderModelInstance_RemoveSubresourceVariantBinding
CharacterRenderRecord_EnsureModelSubresourceVariantBindings
CharacterRenderRecord_RemoveModelSubresourceVariantBindings
```

**Everything now reads coherently:**

| structure | role |
|---|---|
| handle table, 32 × 64 B, refcounted, generation-checked, shared | **the resources being bound** |
| record pool, 128 × 80 B, each carrying a byte index into the handle table and decrementing its refcount on release | **the bindings** |
| work list at `02B47778` | **pending bind / unbind requests** |
| 8 opcodes, two composing a chain-A operation with a `0x0050xxxx` one | **binding operation kinds** |
| 1,432-byte register file | the operations' working state |
| no class, no vtable, no RTTI | a C-style subsystem, as §17 concluded |

**And it connects to documented work.** The `CharacterRenderRecord_*` pair ties this subsystem to
[`CharacterRenderObject`](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md)
— **the largest unclassified function in the image turns out to serve character rendering**, which is
what §1 guessed a player was looking at without being able to say which part.

### Still not established

- **No operation body has been read.** The opcode → semantics map is empty. *(2026-09-30, SWE2-DATA: the opcode to operation map is decoded for both dispatchers, §20; what each operation does is `SD-120`.)*
- **The 56-byte block is a *usage* partition, not a proven structure.** Six addresses touched by the
  same code could still be separate globals — stronger than proximity, not proof.
- The 32-byte record payload remains opaque apart from its index byte.

## 21. Falsification pass 2 — 2026-09-02, session `repos-d2`, sections 12-15

**Scope.** §12 (the transform block), §13 (the descriptor table), §14 (the tag handlers) and
§15 (the packed-id convention). Pass 1 read these and explicitly did not attack them.

**Program state.** Parent `2ed8affb…`, snapshot `46f02e26…`, embedded EXE `73461d08…`, ledger
38,161 / 38,003 / 158, project `proj_hd2` / `GFZ_HD2`, `CHECKPOINT VERIFIED` before any reading.
Every listing below was re-disassembled from the authorized EXE with capstone; every RIP-relative
target was resolved arithmetically rather than taken from a decompiler.

### Overturned

**1. §14's tag-0 arm has the polarity backwards.** The complete body of `0036DF80`:

```asm
0036DFA0  cmp word ptr [rax + rcx*8 + 4], 0
0036DFA6  je  0x36dfb0            <- tag == 0 jumps PAST the call
0036DFA8  mov ecx, dword ptr [rax + rcx*8]
0036DFAB  jmp 0x3b27a0            <- reached only when the tag is NON-zero
0036DFB0  ret
```

`003B27A0` is the handler for **tag != 0**; **tag 0 means no handler at all**. The tag-3 accessor
`0036E5E0` has the opposite polarity (`jne` skips, so the call fires on `== 3`) and *that* one the
document read correctly. **The two arms differ in polarity and were read as if they matched.**

**2. The tag-0 table is 32 entries, not 11.** `003B27A0` walks:

```asm
003B27B4  cmp edi, 0xb           <- a bound on the SECOND ARGUMENT
003B27BE  lea rdx, [rip+...]     -> 02EBEBE0   (end)
003B27C5  lea rbx, [rip+...]     -> 02EBE5E0   (base)
003B27DA  add rbx, 0x30          <- stride 48
003B27DE  cmp rbx, rdx
```

`0x02EBEBE0 - 0x02EBE5E0 = 0x600`, and `0x600 / 0x30 = 32`. §14 states *"the `0xB` bound is on
the second argument, not the table walk"* — correctly — and then titles the subsection *"an
11-entry table"* and carries 11 into its summary. **The document contained the observation that
refutes its own figure.**

**3. §13's central absence claim is false: the descriptor table is written in `.text`.**
`0036E320` and `0036E540` both `lea` the **literal** base `022D94B0`, index it by the clamped slot,
and store:

```asm
0036E346  lea rax, [rip+0x1f6b163]   -> 022D94B0        ; 0036E320
0036E34D  lea rbx, [rax + rcx*8]
0036E37A  mov qword ptr [rbx + 0x10], 0
0036E387  mov dword ptr [rbx], eax                       ; payload  +0x00
0036E389  mov byte  ptr [rbx + 8], dil                   ;          +0x08
0036E396  mov word  ptr [rbx + 4], ax                    ; TAG      +0x04

0036E55F  lea rax, [rip+0x1f6af4a]   -> 022D94B0        ; 0036E540
0036E586  mov word ptr [rbx + 4], ax                     ; TAG      +0x04
```

Eight of the sixteen referencing functions show this shape. `0036E320` is a **constructor**. The
follow-on claim — *"like everything else in this region it is built at run time, through a
computed pointer rather than a literal address"* — is false in both halves, and §12's own
matrix setter `0039AF70` (which writes `022D91B0`–`022D91E0` through literal RIP addresses) already
disproved it **one section earlier**.

**4. Tag value 2 exists, and the tag is a lifecycle state.** `0036E540`:

```c
if (slot->tag == 1) {
    r = FUN_0024DE70(slot->payload);
    if ((u32)(r - 2) <= 1)      /* r == 2 or 3 */
        slot->tag = 2;          /* 0036E586 */
}
```

§13 said tag 2 *"is not tested, which is a gap rather than evidence of absence."* The gap closes
from the other side: **2 is never tested and is written**, as a transition out of 1. So the tag is
not only a type discriminator (§14's framing) — it also carries slot state.

**5. §13's accessor table mis-records `0036E460`.** Its row says *tag test `== 0`*. The
instruction is `cmp dword ptr [rax + rcx*8], 0` at `0036E487` — the **payload `u32` at `+0x00`**,
not the `u16` tag at `+0x04`. A null-payload check, not a tag test.

### Survived

| Claim | How attacked | Result |
|---|---|---|
| §12: **267 functions** touch `022D8F00`-`022D9500` | independent census over all 38,161 bodies | **SURVIVED, exactly 267.** |
| §12: `003970A0` / `0039AF70` are getter and setter for a 4×4 matrix at `022D91B0` | both re-disassembled in full | **SURVIVED byte for byte.** 44 B each, four `movups` at a `0x10` stride, exact inverses. |
| §12: descriptor table is **32 × 24 B**, `u16` tag at `+4`, index clamped to `0x1F` | verified in three accessors independently | **SURVIVED.** |
| §13: **16 functions** reference the table | recounted | **SURVIVED** — see the miscount note below. |
| §14: the tag-3 reading — top nibble, 16 buckets, chain at `+0x348`, two `u16` keys, second key from `[rsp+0x32]` | full re-disassembly of `0024FDA0` | **SURVIVED entirely**, including the stack offset. |
| §15: BI-10 — item ids and the tag-3 handle are different schemes | field positions and resolution re-read | **SURVIVED.** |
| §15: `ActorHandle_ResolveRegistryEntryByPackedId` is a `0x14` site; `0024E210` carries `Runtime.PackedIdBucketRegistry` | re-derived; tag read from the ledger | **SURVIVED, both.** |

**And the tag-3 reading is strengthened.** §14 leaves *"match key A"* unidentified. `r8d` is loaded
with the **original id** at `0024FDAB`, before the shift, so **key A is the low 16 bits of the handle
itself** and key B is the caller's qualifier. The bucket table is at **`0x020910F0`**
(`lea rax,[rip+0x1e41331]` at `0024FDB8`), an address §14 does not give. The abridged listing in
§14 omits `movzx ecx, al` at `0024FDB5`, which is what makes the nibble the index — the listing
is abridged, not wrong.

### Not reproducible as stated

§15's shift census. Its predicate is *"a right shift that leaves a small field, followed within
four instructions by an `AND 0xF`/`0xFF` or a small `CMP`"* — and **"small" is never defined.**
Re-implemented with `imm <= 0x20`, the same sweep returns **59 sites in 47 functions** against the
published **29 in 19**. This is not a refutation: without the threshold the figure cannot be
reproduced either way. The conclusions do not depend on it — several shift widths coexist, and both
named corroborations hold — but the exclusivity of the `0024Cxxx`-`0024Fxxx` cluster does: under
the wider predicate 11 of 18 `0x1C` sites fall in `0024xxxx` and seven do not. **A census is a claim
about a predicate; publish the predicate.**

### A miscount of my own, chased rather than reported

My first count of functions referencing `022D94B0` was **13** against the document's **16**. Rather
than file a disagreement I widened the window from the base address to the table's **full 768-byte
extent** (`32 × 24`): **16**, matching exactly. Three functions (`0036DE20`, `0036DF30`, `0036E5A0`)
reach the table at a non-zero offset. **The document is right and my window was one address wide.**
This is the second time in two passes that a count disagreement resolved into a population
difference rather than an error, which is now a standing expectation rather than a surprise.

### What was tried and failed to break anything

- **Tried to break the 267 figure** by scanning a wider population than the document had available
  (all 38,161 ledger bodies). It reproduced exactly, on 315 distinct addresses.
- **Tried to make the matrix a coincidence** — four unrelated 16-byte globals rather than one
  structure. The setter is the byte-exact inverse of the getter over the same four addresses in the
  same order; there is no reading of that pair which is not a 64-byte object.
- **Tried to find a fourth tag arm** among the accessors by reading `0036E500` and `0036E5A0` in
  full. Neither tests the tag; both only read the payload. No new arm.
- **Checked for banned evidence.** No `.pdata`, `.xdata`, unwind, EH map or
  `_IMAGE_RUNTIME_FUNCTION_ENTRY` reasoning appears in this pass. Address adjacency was available
  and refused: the `02EBE5E0` table sits near the `02EBF008` content registry documented elsewhere
  and **no relationship is claimed**, because proximity is not evidence.

### Consequences

- **BI-8 changes shape.** It is no longer *"what fills a table nothing writes"* — the table is built
  by its own accessor family, in `.text`, and the constructor is `0036E320`. The open part is what
  the payload denotes and what the two resolved object kinds contain.
- **The section 13 generalisation should not be reused.** *"In a region where the data cannot be read
  statically, the accessors are the schema"* is a good heuristic and it was over-stated into a claim
  that nothing writes the region. The accessors **are** the schema **and** several of them are
  writers; reading only the readers is what produced the error.
- **`0024DE70`** is now a lead worth its own read: it is the query whose result drives the tag
  1 → 2 transition, and it is also one of the `0x1C` packed-id sites.

> **`BI-8` answered 2026-09-14 (FABLE): the table is the per-manager list of script-requested event-effect loads.**
> - **Who fills an entry.** A script verb handler `003576D0` pops three integers (slot, effect id, variant), takes the bound
>   manager's id (`[002640C0() + 0x28]`) and calls `0036E320(manager, slot, id, variant)` (`003576F3`–`0035772F`).
>   - For a free slot (tag `+4 == 0`), `0036E320` clamps the slot to `0..31` and adds `0x1000` for variant 1 or `0x2000`
>     for variant 2 to the id.
>   - It stores the handle from `003B1A80(id, …)` at `+0`, the manager at byte `+8`, clears `+0x10`, and sets tag `+4 = 1`
>     (`0036E340`–`0036E396`).
> - **What the handle is.** `003B1A80` allocates a class-7 handle (`0x70000000 | …`) in the 32-entry, `0x30`-stride pool
>   `02EBE5E0`. It shares an existing record with the same key that is already in state 5 or 6, and otherwise starts one
>   with `003B2310` (`003B1A93`–`003B1B7A`).
>   - `003B2310` loads resource **kind 12** (`0032E400(0xC, id)`). Kind 12's path array `01E88E00` begins
>     `PS2Data\effect_finish\jp\event\e0000.efx`, the event effects (532 sized entries, maximum id 883, in the US size table).
>   - The variant bits choose a fallback id: `0x1000` → `id + 0x200`, `0x2000` → `id + 0x240`, bit 15 → `0x1FF`, and `0xC3`
>     → `0x1FE` when `002DEBB0` says so (`003B2343`–`003B2391`).
> - **The per-tick poll.** `0036E1E0`, called from `World_UpdateSimulationTick`, asks `0024DE70(handle)` for every
>   non-free entry and stores the state at `+6`. State 0 frees the entry (`+0 = 0`, `+4 = 0`); state 5, loaded, sets tag
>   `+4 = 5` (`0036E22D`–`0036E25A`).
> - **Cancellation.** `0036DE70(m)` (the skip path, `EX-8`) and the resets `0036DE20` / `0036DF30` set tag `4`. The first
>   releases the class-7 record through `003B24C0` / `003B1700`.
> - **So the record is `{u32 class-7 handle; u16 tag 0 free / 1 requested / 4 cancelled / 5 loaded; u16 last state; u8
>   manager; …; flags at +0x10}`**, 24 bytes × 32. The two resolved object kinds of the earlier tag-arm reading belong to
>   other handle classes that the accessor family also serves; this table's own handles are class 7.

> **`BI-11` narrowed 2026-09-14 (FABLE), not answered: the family is the engine's typed-handle layer, and the class nibble
> names the subsystem.**
> - **The family.** Exactly ten functions in `0024C000`–`00250000` shift a handle right by 28: `0024CFF0`, `0024DE70`,
>   `0024E210`, `0024E2F0`, `0024E6D0`, `0024ED50`, `0024F8D0`, `0024F920`, `0024FDA0` and `0024FE30`. That matches the
>   question's count.
> - **Two dispatchers route a handle by class** `handle >> 28` through nine-entry tables:
>
>   | class | state `0024DE70` | release `0024CFF0` | pool behind it |
>   |---:|---|---|---|
>   | 1 | `002FCA00` | `002FC340` → `002FCB60` | 48 × `0x38` records at `02EC32E0`; the state is the low nibble of byte `+0x23` |
>   | 2–4 | — (returns 0) | — | no arm in either table |
>   | 5, 6, 9 | `003B0AD0` | `003B0770` | 36 × `0x18` records at `02EBEC00`, each holding an object pointer at `+8` |
>   | 7 | `003B2510` | `003B1700` | 32 × `0x30` event-effect load records at `02EBE5E0` (`BI-8` above) |
>   | 8 | `00375AE0` | `00375470` | 32 × `0x70` screen-effect descriptors at `02EBF9E0`, the handle dword at `+0x68` ([screen fade](../../17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md) §2.1) |
>
> - **The bucket registry proper.** `0024FDA0` and its neighbours index `020910F0[class]`, a head per class. They walk
>   records chained at `+0x348` and match the handle's low word at `+4` and a qualifier at `+6` (`0024FDB8`–`0024FDE7`).
> - **The routers.** `0024FE30` sends class 1 to `002FD0C0`, classes 5, 6 and 9 to `003B1260`, and class 7 to `003B2830`.
>   `0024ED50` sends class 1 to `002FCFB0` and classes 5, 6 and 9 to `003B0F30` (`lea eax, [rdx-5]; test eax, 0xFFFFFFFA`, excluding 10).
> - **Residue:** what classes 1 and 5/6/9 are as subsystems. Class 1 is the battle family `002FCA00` that the timeline
>   interpreter calls; 5/6/9 share the `02EBEC00` pool with a `+0x370` kind byte. The chained records at `020910F0`
>   (≥ `0x350` bytes) are not identified.
>
> **`BI-11` NARROWED 2026-09-27 (OPUS): classes 5/6/9 are the presentation-record classes.**
> - **The creator.** `003B02A0` is the only creator, and it admits exactly {5, 6, 9} (`003B02D7`–`003B02EA`).
>   It zeroes a `0x3B0`-byte record, writes the class as byte 0, and mints `class << 28 | ++serial`.
>   An unflagged presentation number is refused at 24 live; the per-id flag table is `01EFE260`.
> - **Class 5 creators:** `002EACD0` (level-up, action-timeline attached effect), `0036E700`, `003A3E30`,
>   `003B0C30` (root-animation phase, number `0x63`) and `003B0C50` (the footstep effect).
> - **Class 9 creators:** `003BA1F0`, and `0036E750` through its index table `01EF9400`, called from
>   `002EFD80`, `002EFDC0` and `003B7180` (`changetonormalparty`).
> - **Class 6** is reached only through the script bridge `00357620`'s class operand. No direct call passes 6.
> - **So** the `020910F0` chained records above are these `0x3B0`-byte presentation records, and `02EBEC00` is
>   their side-table.
> - ~~**Still open:** class 1~~ (answered below), and what separates 5 from 9 inside the driver `0024B9B0`.
>   Control: `_index/candidates/bi11-presentation-classes/bi11_classes.py`.
>
> **`BI-11` ANSWERED 2026-09-27 (OPUS): class 1 is the loaded magic-effect files.**
> - **The records.** `002FC200` lays out 48 × `0x38` records at `02EC32E0` with handle dword `(1 << 28) + slot`.
> - **The loader.** `002FC4A0` sums the 5-bit load cost at `02EC19C4 + id*8` over live records in states 5–7 and
>   adds the new record's own (id at `+0x20`).
>   - It refuses a total above 24.
>   - Otherwise it requests resource kind `0x26`, or `0x0B` when `002DEBB0` says so, for that id.
>   - `002FCFF0` sizes the same 512-entry table from those kinds: `effect_finish` magic `.efx` on the
>     [file-size-table page](../../02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md).
> - **One budget.** `003B02A0` adds `002FC9B0` (the class-1 cost sum) to `003B0B70` before its own cap of 24. So
>   loaded magic effects and spawned presentation records compete for the same 24.
> - **Not claimed:** what separates classes 5 and 9 in `0024B9B0`, or which `.efx` an action loads beyond its id.

## 20. Falsification pass 1 — 2026-09-02, session `repos-9e`

**The first deliberate attempt to destroy this document**, run by a session that did not write it,
against the GN158 checkpoint (`CHECKPOINT VERIFIED`, residual sha `c5d4b7f7…`, project `GFZ_H9E`).
**Five claims overturned, eight survived.** Every figure below was re-derived from the ledger or the
image, not re-read from the document.

The document had eleven recorded amendments and no recorded attack. The distinction matters: nine of
those amendments were the author extending their own reading, and **the two things that broke here
had both survived all eleven**.

### Overturned

**1. The headline census is stale by two.** Claimed 10,154 functions / 2,667,070 bytes. The certified
ledger gives `internal=38161`, `codeDomain=28009`, so functions with no `CodeDomain` = **10,152**,
independently cross-checked as `owner(9409) + finalNo(585) + unresolved(158) = 10,152`. Corrected
bytes **2,666,058**.

The cause is proven rather than inferred: re-running the census over `Tools/work/graph/functions.tsv`
reproduces the document's three figures **exactly** — 10,154 / 2,667,070 / 9,409 — and that dump is
the 01:09 state, stale by the two functions the GN checkpoint closed (`00313A00` 289 B, `002F7380`
723 B; 1,012 B together). The frontmatter claims verification against the GN hashes, so the
document's **stated program state and its actual data source disagree**.

**This is the defect [the-unresolved-158 §13](../the-unresolved-158.md) records, in the same category
folder** — *"a census over `functions.tsv` will return 160 and be wrong by construction."* The
warning was written and then walked into.

**2. The census's stated self-check is vacuous — it cannot fail for the right reason.** §8 claimed
that reproducing `owner=9409` was *"the check that the column is being read correctly."* It is not.
The ledger reports `overlap=0`, so no owned function carries a `CodeDomain`; every owned function
lands in the untagged set **by construction**, and the owner count is 9,409 whatever the CodeDomain
filter does:

| CodeDomain filter | untagged | owned | the stated check |
|---|---:|---:|---|
| correct (`;`/`,` split) | 10,154 | 9,409 | **passes** |
| split on `,` only | 12,779 | 9,409 | **passes** |
| deliberately broken — nothing has a CodeDomain | 38,161 | 9,409 | **passes** |
| deliberately broken — everything has one | 0 | 0 | fails |

**The guard passes on an answer wrong by 28,007.** It tests that the owner column is readable, which
was never in doubt, and is blind to the only column that could go wrong.

*(The `,`-only row is not hypothetical. This pass made that exact mistake first, got a plausible
12,779, and caught it only because it contradicted the independently recorded 28,007 CodeDomain tags
in the-unresolved-158 §13. **A control must vary with the thing being measured**; both this
document's guard and this auditor's first attempt failed that test.)*

**3. §6's "called from one dispatcher" is false.** `003CD840` has **three** callers — `003CCF20`,
`003CD2C0`, `00431B10`. `003D2B60` also has three — `003A9C10`, `003CCF20`, `003CD2C0`. The modding
note reasoning from a single caller does not hold.

**4. §10's "`003CD840` twice" is wrong — it is three, and the third changes the model.** Decoding
every `E8` in the dispatcher body:

```
003CCFBE  E8 7d080000  -> 003CD840   PRE-DISPATCH, before the jmp rcx at 003CD101
003CD17F  E8 bc060000  -> 003CD840   opcode 4 arm
003CD20E  E8 2d060000  -> 003CD840   opcode 8 arm
```

**Chain A's main operation runs unconditionally on the common path**, not only under two opcodes — so
"eight operations, two of which compose with chain A" understates it. `0036B130` is called **four**
times (`003CCFA2`, `003CD168`, `003CD1F7`, `003CD24D`), not the three §10 lists. There is also a
**tail region past every one of the eight arms** — `003CD24D call 0036B130`, `003CD261 call
003D2B60` — and that is where `003D2B60` is actually invoked. §11 proved `003D2B60` is "the same
machine" without ever establishing **when it runs**.

**5. There is a second dispatcher, and it is the half of the system §19 was looking for.**
`003CD2C0` (688 B, `PrimaryOwner.Presentation`, no `CodeDomain` — inside this document's own
population) sits **8 bytes past `003CCF20`'s jump table** and is a structural twin:

| | `003CCF20` | `003CD2C0` |
|---|---|---|
| computed dispatch | `jmp rcx` at `003CD101` | `jmp rcx` (`ff e1`) at `003CD3F7` |
| jump table | `003CD298`, **8** entries, all inside its body | `003CD570`, **8** entries, all inside its body |
| distinct callees | 12 | **13** — the same 12, plus `003CD650` |
| reached from | `00258D70`, `00258E40` | `0053AB50` (9,695 B) — a different entry path |

So the machine has **two byte-opcode dispatchers of eight arms each**, on two independent entry
paths. §16's *"dispatcher `003CCF20`, byte opcode 1-8, ten operations"* and §17's *"the whole
machine"* each describe half of it.

**And the one callee that differs identifies which half.** `003CD650` is the release function §18
decoded — it validates `[entry+0x30] == handle`, zeroes it, and decrements the handle entry's
refcount. It has exactly two callers:

```
003CD650  <-  003CD2C0                                            (the second dispatcher)
          <-  RenderModelInstance_RemoveSubresourceVariantBinding (00504610)
```

**The second dispatcher shares its release primitive with the GFZ-named `Remove` entry point that
§19 identifies as a work-list writer.** So §19's Ensure/Remove pair is mirrored in the dispatch
layer: `003CCF20` never frees a record, `003CD2C0` does. **This extends §19's identification rather
than contradicting it** — the binding system has a bind dispatcher and a release dispatcher, and the
document described only the first.

### Survived — attacked and not broken

Recorded because an unrecorded audit did not happen.

| Claim | How it was attacked | Result |
|---|---|---|
| Jump table `003CD298`, exactly 8 entries, all inside the body | raw dwords decoded from the EXE, independently of the decompiler | **exact** — entries 0–7 → `003CD103`…`003CD1D2` |
| "entry 8 reads as `CCDECCCC`, so the table is exactly 8" | same decode | **exact**, and the reasoning is sound — `0xCCCCCCCC` padding |
| All eight opcode → operation mappings (§16) | decoded every `E8` in every arm | **all eight exact** |
| Opcodes 4 and 8 compose handle-resolve → `003CD840` → a `0x0050xxxx` op | byte level | **exact**, both arms |
| `003CD840` "calls nothing" | call graph and byte scan | **confirmed**, 0 callees |
| `003CCF20` calls twelve distinct functions (§16 correcting §10's ten) | independent census | **exact** — §16 was right to correct §10 |
| Dispatcher reached from `00258D70` / `00258E40` | call graph | **exact** |
| `003CD650` is the release primitive (§18) | caller census | **corroborated** — its other caller is the named `Remove` function |

**The "no strings" claim survives, and now rests on a sound instrument.** This document repeats "no
calls and no strings" for `003CD840`, and that rested on `DumpUnresolvedStringReferences.java`, which
this session [proved returns a structural
zero](../Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md): it tests whether Ghidra
holds a *typed string* at the target, and this program has none, so it reports "no strings" for
**every function in the binary**. That silently removed the support from every "no strings" claim in
the database.

Re-tested with the corrected byte-level scanner (positive control `0017F850` → `"display : draw
Font"`, PASS) across all fourteen functions of the machine — `003CD840`, `003D2B60`, `00438860`,
`004355D0`, both dispatchers, the initializer and all eight operations — at depth 0 **and** depth 1:
**no authored string anywhere.** The claim is unchanged and is now *supported* rather than merely
unrefuted.

### What this pass did not test

- **No operation body was read.** BI-1's semantic core is untouched.
- ~~The second dispatcher's eight arms were **not** decoded to opcodes. Whether its map matches~~
  ~~`003CCF20`'s is unknown~~ *(Corrected 2026-09-30, SWE2-DATA: decoded. `003CD2C0`'s table `003CD570` maps every opcode 1–8 to the same operation as `003CCF20`'s table: `0050AC20`, `00506B40`, `005080A0`, handle-resolve → `003CD840` → `0050A100`, `00509BB0`, `00507490`, `00508C90`, handle-resolve → `003CD840` → `00507120`. Control `_index/candidates/dd-data-3-0930/ui_bi17_dispatch.py` D1, D2, C1. This item and the next two carried register labels that were never opened; the labels are dropped.)*
- ~~What reaches the tail region at `003CD24D` is not established~~ *(Corrected 2026-09-30, SWE2-DATA: the tail runs once per pending work-list entry (byte `+1` at least `0x80`), after that entry's operation list, when the entry's resolved target is non-null (`003CD239`). The target is the entry's handle `+8`, or the last handle an opcode-4 or opcode-8 arm resolved. The tail resolves the entry's `+0x10` and calls `003D2B60` with it and word `+2` (`003CD252`–`003CD261`). Control `_index/candidates/dd-data-3-0930/ui_bi17_dispatch.py` T1–T3.)*
- ~~`00431B10` and `003A9C10`, the two other callers of chain A, were not read~~ *(Corrected 2026-09-30, SWE2-DATA: both are read on [the authored-number page](../../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md). `00431B10` is the record kind dispatch the expression evaluators share: it loads the record context through `003CD840` and calls one of six of this machine's `0050xxxx` operations per kind. `003A9C10` is the authored-number republish that calls `003D2B60`.)*
- §12–§15 (the transform block, the descriptor table, the tag handlers, the packed-id convention)
  were read but not attacked. **They are now the largest untested surface in this document.**

### The killer observations, named

- *The structural claims would be false if the jump table were not 8 entries, or if any arm's calls
  differed from the stated mapping.* Checked directly against the image; neither failed.
- *The census would be wrong if the ledger and a fresh derivation disagreed.* They did, and the
  document lost.
- *The single-dispatcher model would be false if any other function called the same operation set.*
  One does, and it is adjacent to the first dispatcher's own jump table.

## 22. Chain B read — BI-3 and BI-4: an effect's per-frame mesh, drawn and blended (2026-09-14, FABLE)

**Chain B does not fix anything up.** It is the draw path of effect element type `0x05`. Each frame it picks one of up to
32 mesh records, optionally blends toward the next one, and draws the record's triangles and quads. The "315 pointer
resolutions" (§2) are an artefact of how the port stores pointers. Every array in the mesh record is held as a u32
relative to a base (`ImageAddress_ResolveRuntimePointer` `0020E600` is `mov eax, ecx; add rax, [01F83530]; ret`).
The compiled draw loops call that resolver again for every index they read, instead of resolving once before the loop.

Static only. **The game was not run**, and nothing below depends on runtime behaviour.

### 22.1 The chain, with every call site

| step | function | what it does | evidence |
|---|---|---|---|
| walk method, type `0x05` | `00449AB0` | chooses the frame's mesh slot and blend (§22.3), then calls the draw with `rcx` = mesh record, `rdx` = draw parameter block | `0044A148`–`0044A15B` |
| draw entry | `004355D0` | returns 0 without drawing unless record flags `+0x18C` bits 2 **and** 0 are set; then runs one vertex prep, then one of three draw paths | `0044A15B` is its only direct call site; flag tests `00435618`–`0043562E` |
| vertex prep, blended | `00434CD0` | when the parameter block's next-mesh byte `+0x1E8` is non-zero | `00435622`–`00435636` |
| vertex prep, unblended | `00435050` | when `+0x1E8` is zero | `0043565C`–`00435666` |
| draw path: VU0 | `00438860` | after a successful prep, when parameter byte `+0x1F1` ≥ `0x80` | `0043566F`–`00435681` |
| draw path: alternative | `00437130` | otherwise, when `+0x1F1` bit 3 is set | `00435688`–`00435692` |
| draw path: inline | `004355D0` itself | otherwise; the triangle and quad loops of §22.2 | from `00435699` |

Each of the five callees of `004355D0` has exactly one direct call site in the raw call index, inside `004355D0`. Indirect
references were not searched, so "only caller" is claimed for direct calls only.

### 22.2 The mesh record — layout fixed by its loader

The record is resource kind `0x54`. The effect record store dispatches it to loader **`00436D00`** (`005009AB` in
`00500980`; see [the record-store switch census](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/members/switch-family-record-store-5x.tsv)).
The loader is also reached from `003A9EF0` and the thunk `0043D8E0`. It reads a file header of one flag byte plus eight
u16 counts, and each array's element size comes from the loader's own shift:

| record field | from file | holds | size (loader) |
|---|---|---|---|
| `+0x18C` bits 0–2 | header byte 0 | flags. Bit 0 gates the index lists (and drawing, §22.1). Bit 3 is tested but not written by this loader (it masks only bits 0–2); when set, arrays point into the file image and are not copied | `00436D2D`–`00436D43`; bit 3 tests `00436D98` ff. |
| `+0x10` | u16 @ +2 | triangle count | `00436D4D` |
| `+0x12` | u16 @ +4 | quad count | `00436D55` |
| `+0x14` → `+0x20` | u16 @ +6 | **vertex positions**, 16 B each; the loader forces every w to `1.0` | `shl 4` `00436D95`; w store `00436DFF` |
| `+0x16` → `+0x24` | u16 @ +8 | 16-byte vectors | `shl 4` `00436E1C` |
| `+0x18` → `+0x28` | u16 @ +0xA | 4-byte entries | `shl 2` `00436E77` |
| `+0x1A` → `+0x2C` | u16 @ +0xC | 8-byte entries | `shl 3` `00436ED2` |
| `+0x1E` → `+0x30` | u16 @ +0x10 | 20-byte records copied inline into the record | `lea [rax+rax*4]; shl 2` `00436F30` |
| **`+0x170`** | — | **index list**: u16 × (3 · triangles + 4 · quads), i.e. 6·`+0x10` + 8·`+0x12` bytes | `00436F5B`–`00436F80` / `00436FA8` |
| `+0x174` | — | a second list of the same byte size, immediately after the first | `00436F8E` / `00436FD9` |
| `+0x188` | — | one byte per primitive (`+0x10` + `+0x12` bytes) | `00436FF5`–`00437029` |
| `+0x1C` → `+0x180` / `+0x184` | u16 @ +0xE | `+0x1C` id bytes, and `+0x1C` × 8 handles resolved from them as kind `0x52` through `003AA280` | `00437068`–`004370F3` |

**BI-4:** `+0x170` is this record's primitive index list. The draw loops independently confirm the size the loader gives.
The triangle loop in `004355D0` reads three u16 per triangle, advances by 3 (`00435E54`) for `+0x10` triangles, and passes
three 16-byte vertices to `0039E820`. The quad loop continues at byte offset 6·`+0x10`, reads four u16 (`+0`, `+2`, `+4`,
`+6`), advances 8 bytes (`00435F14`) for `+0x12` quads, and passes four vertices to `0039EC30`.

### 22.3 How the walk chooses the mesh — two modes

The element's setup method `00538DB0` fills 32 slots. For each id byte at record `+0x570 + i`, it resolves the resource
(kind `0x54`, through `003AA280` / `0020E620`) into the u32 at `+0x5A0 + 4i` (`00538E47`–`00538E90`). A zero id leaves the
slot empty. Record byte `+0x590` bit 4 selects the mode:

- **Track mode (bit clear).** The walk evaluates the track at record `+0x190` at the element's time `+0x44`
  (`004309C0`, `00449DB7`–`00449DC9`). If the value v is positive, slot `trunc(v)` is used when it is below 32; otherwise the
  slot and fraction are reset to 0 (`00449DD1`–`00449DF9`). The fraction `v − trunc(v)` goes to parameter `+0x1EC`.
  When slot `trunc(v)+1` is also populated and the current mesh's `+0x14` is not larger than the next mesh's, the walk
  stores the next slot's id byte at parameter `+0x1E8` and the next mesh at `+0x48` (`0044A03F`–`0044A0FF`).
- **Random mode (bit set).** The step method `00449970` picks `+0x294 = 003A6E60(count +0x591)` and falls back to the
  first populated slot if that one is empty (`00449A16`–`00449A84`). The walk then draws that slot with fraction 0 and no
  next mesh (`0044A112`). `003A6E60` has the shape of the VU0 random-number step (`0x1FC00000 | 22 bits` over
  `01EF93E8`). That is a reading, not a verified identification. *(Anchored 2026-09-30, SWE2-DATA: [the authored-expression contract](../../02-Resource-And-Asset-Pipeline/Authored-Expressions/CONTRACT-authored-expression-evaluation.md) reads `003A6E60` whole as the draw `f(bound)`, a leaf that calls nothing.)*

**The blend is vertex-position interpolation.** `00434CD0` loads the next mesh (`+0x48`) and `t` (`+0x1EC`), computes
`1 − t`, resolves `+0x20` in both meshes, and calls `00431F10(out, cur, next, 1 − t, t, count = +0x14)`
(`00434D00`–`00434DE0`). `00431F10` computes `cur·(1 − t) + next·t` per 16-byte vertex as translated VU0 code, with its
intermediates in ACC and the vector rows (`00431F50`–`00431FC9`). The walk's `+0x14` comparison is what keeps the next
mesh's position array at least as long as the current one's.

### 22.4 BI-3 — what the 315 resolves read

`members/resolve_fields.py` classifies the operand loaded into `ecx` before each call to `0020E600`. Output:
[`members/chain-b-resolve-fields.txt`](members/chain-b-resolve-fields.txt).

| function | resolves | `+0x170` | `+0x20` | `+0x174` | `+0x188` |
|---|---:|---:|---:|---:|---:|
| `004355D0` | 76 | 71 | — | 4 | 1 |
| `00438860` | 239 | 143 | 90 (72 through `rsi`, 12 `r14`, 6 `rax`; which mesh each register holds was not traced) | 5 | 1 |
| **the two functions §2 counted** | **315** | **214** | **90** | **9** | **2** |
| `00437130` (not counted in §2) | 77 | 71 | — | 5 | 1 |

All 315 are dereferences of fields §22.2 names. **None relocates anything**, and the "RVA-to-pointer" description of the
resolver in §2 was a fair description of the function but not of what chain B uses it for. The `022D9000` targets (×198)
of `00438860` are the VU0 register bank; the page cited in §4 covers them.

### 22.5 What this does not establish

- [x] What the `+0x24` 16-byte vectors, the `+0x28` 4-byte entries and the `+0x2C` 8-byte entries are. **BI-3a —
      ANSWERED 2026-09-16 (SWE2-DATA) by authored census over all 3,698 effect files (2,252 records):**
      `+0x24` is 52,808/52,808 unit-length vectors with `w = 0` (direction vectors — the normals hypothesis);
      `+0x28` is packed 4-byte entries dominated by `0x80808080` at ~47 % with byte 3 in `{0x80, 0x81}` (the
      RGBA-colour hypothesis, corroborated by the `0x80808080` default written into element `+0x1F0` at
      `002F30A1`); `+0x2C` is float pairs ~74 % in `[0,1]`, no NaN (the UV hypothesis — the `+0x1EC`-driven
      work in `004355D0` at `00435CE3`–`00435DA2`, a float pair scaled by 1.15 and offset by 0.5 over a
      `+0x1A`-counted array, points the same way). The labels remain
      distributional — no consumer body read. The census also shows `+0x18 == +0x1A` in every record and
      `+0x16 != +0x14` in 1,670/2,252. Full tables:
      [effect-mesh-records-kind-54](../../17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md).
- [x] What the second index list `+0x174` indexes, and what the per-primitive byte `+0x188` selects. **BI-3b.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)*
      **Narrowed 2026-09-18 (FABLE): both halves read from the consumers.* **The second list is the normal-index list.** Every one of the fourteen `+0x174` resolves hands the list to one of two helpers with the vector counts: `00432CC0(dst, prim, base, list, +0x18, +0x16)` takes `word[list] << 4 + base` and loads sixteen bytes from it into the workbench (`00432CCF`–`00432D24`), bounded by `+0x16`, the count of the 16-byte vectors at `+0x24`; and `00396F20(base, list, dst, count)` walks `count` words, scaling each by 16 off the base and copying a qword per index (`00396F50`–`00396FBE`), called with the second list and `+0x18` at `00435AF6`, `00435BD5`, `00438D9D`, `00438E86`, `004375C3`, `004376AA`. So `+0x174` indexes the 16-byte vectors exactly as `+0x170` indexes the 16-byte positions: **a normal index per corner beside the position index per corner**, which is why the loader sizes it identically. **The per-primitive byte selects a parameter entry.** After the `+0x188` resolve the loop reads one byte per primitive and forms `r9 = (byte + 0xB) << 4 + r15` — entry `byte + 11` of the 16-byte-stride block in the walk's parameter object — and passes it as the primitive's vector operand (`004361AF`–`004361C8`, `00436375`–`0043638C`; the same idiom at `00437B90` in `00437130`), so it is a per-primitive **parameter-slot index** from slot 11 upward. What those parameter entries hold (a colour, a material vector) is the effect element pages' to name and is not read here. Static: the two helpers and the three loops.*
- [x] What distinguishes the `00438860` (VU0) and `00437130` paths from the inline path. Both are selected by parameter byte
      `+0x1F1`, built in the walk from record bytes `+0x4A` and `+0x590` (`00449B93`–`00449C6D`). **BI-3c.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row; box ticked in a follow-up)*
      *Narrowed 2026-09-15 — the selection is answered, the distinction is not (register `BI-3c` PARTIAL).*
      - **The ladder** (OPUS, re-read by FABLE). `004355D0` loads `+0x1F1` at `0043566F`. Bit 7 set → `00438860`
        (`00435677`); otherwise bit 3 set → `00437130` (`00435688`); otherwise the inline path at `00435699`.
      - **The builder** (OPUS's decode, re-derived byte for byte by FABLE). `00449B93`–`00449C6D` is seven bitfield
        inserts. `rec[+0x4A]` bits 2–4 go to bits 0–2, and `v = rec[+0x590]` fills the rest:
        - bits 4 / 5 / 6 ← `v` bits 1 / 2 / 3;
        - bit 7 ← `v` bit 5;
        - bit 3 ← `v` bit 5 OR `v` bit 0, the one insert whose source is `(v >> 2) | (v << 3)`;
        - `+0x1F2` bits 0–1 ← `v` bits 6–7.
        So **`v` bit 5 selects `00438860`, `v` bit 0 alone selects `00437130`, and neither selects the inline path.**
      - **What the comparison shows, and what it does not.** Callee sets nest: 33 shared; `00437130` has exactly
        those; `00438860` adds 12. That does not make the bodies one operation at three costs:
        - The inline body and `00437130` are the same size (5,936 B and 5,930 B).
        - Only the inline path calls `0053DD10` (`00435D2E`, `00435D7C`, inside the `+0x1EC` block cited for `BI-3a`).
        - Each body has primitive loops of its own over the same `+0x170` indices, 84 / 238 instructions against
          173 / 154, and they are only 0.27–0.55 similar to each other.
        - One concrete difference: per triangle, `00437130` loads the three 16-byte corner entries from the `r14` array
          (`00437862`–`004378A6`) and **skips the primitive when any corner's first qword is zero** before calling
          `0039E820` (`0043789C`–`004378CC`). `00438860` tests corner entries before its call too (`004390B3`,
          `004390BD`). The inline path loads the same three corners and calls `0039E820` untested (`00435DFD`–`00435E4B`).
          Both testing paths are the ones with bit 3 set, so the skip goes with bit 3. That pairing is an observation,
          not a traced rule.
        What those entries are, and what each path draws differently, is unread.
      **Narrowed 2026-09-18 (FABLE): the distinction is measured on both paths.* **`00437130` is the inline drawing compiled apart from its ladder.** A callee-set diff over `edges.tsv` gives it 33 callees, every one also a callee of `004355D0`, and nothing of its own; it is 6 bytes shorter, and a diff of the two bodies with addresses stripped shows the prologue ladder missing — the two prep calls, the `+0x18C` bit tests and the `+0x1F1` selection — with the mnemonic stream agreeing on about two thirds of the remaining instructions (432 of 1,279 differ, mostly register and frame-slot allocation). So the bit-3 path re-enters the same drawing without re-running the dispatch; what the re-arranged third does is not read. **`00438860` transforms and clips in software.** It adds twelve callees the other two never call, and its primitive loop runs, per triangle or quad: `00431D30` three (or four) times — one vertex each loaded into the workbench `022D8F30` through `0036D930` — then the outcode clamp `00521450` (the clipping test whose four-generation history [the clamping page](../../06-Movement-And-Navigation/clamping-a-point-into-a-volume.md) reads), the workbench restore `003AFDD0`, `0039A150`, and an emit through `0043E440` or `0043D8F0` (a 40-byte record into the command ring at `02F8F2F8`, `0043E45E`–`0043E486`) — the sequence `00439272`–`00439341`, repeated at `00439613`, `0043988A` and `00439BE2`; once per mesh it composes the workbench matrix from `+0x1F1 & 7` (`003977B0`, `0043890E`) and installs the projection × viewport (`0039B550`, `0043891A`). The inline path does none of that: it hands the raw 16-byte vertices to `0039E820` / `0039EC30` and lets the backend transform. So bit 7 of `+0x1F1` selects the PS2-style VU0 transform-and-clip path and bit 3 the ladder-less re-entry. Static: the edge list and the three bodies.*
- [x] The 20-byte inline records at `+0x30`. **BI-3d — ANSWERED 2026-09-16 (SWE2-DATA): never.** `+0x1E` is `0`
      in all 2,252 authored records, so the unbounded copy is never exercised and the over-16 question is vacuous.
      ([effect-mesh-records-kind-54](../../17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md))
- What kind `0x52` (the `+0x184` handles) is. The same kind is the first child list of the kind-`0x50` group record in the
  census cited above, so it belongs to the effect container's own record set. Its meaning is not read here (`SD-123`).

### 22.6 Controls, and what did not discriminate

- **Two derivations of the index-list size agree.** The loader's allocation (6·tri + 8·quad bytes) and the draw loops'
  strides (3 u16 per triangle, 4 per quad, the quad loop starting at 6·tri) come from different functions. A different
  `+0x170` layout would break one of them.
- **Positions are fixed by more than the name.** The loader writes `1.0` into every fourth float of the `+0x20` array,
  and the only arithmetic read over that array is the interpolation of 16-byte vertices.
- **Did not discriminate:** the `+0x14 ≤ next +0x14` test is consistent with either "same topology" or merely "long
  enough to read". The claim is limited to the second.
- ~~**Did not discriminate:** the element-type table gives `0x05` its methods, but no authored effect file was opened. No
  statement is made about which effects use type `0x05` or how many slots they fill.~~ **Superseded — every authored
  effect file has now been opened.** SWE2-DATA's census over all 3,698 shipped `.efx`/`.efb` files
  ([effect-mesh-records-kind-54](../../17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md) §5)
  finds **5,164 type-`0x05` elements in 1,088 files**, every one an `0xA00`-byte element record carrying the full
  `+0x570`/`+0x590`/`+0x5A0` region of §22.3, filling **at most 3 of the 32 slots** (`0:1, 1:4,268, 2:894, 3:1`), and
  every non-zero slot id resolving to a kind-`0x54` sub-record of the same file. So the 32-slot window §22.3 describes is
  capacity, not use: in shipped data the track-mode walk never has more than three populated slots to choose from, and
  the "next slot populated" test at `0044A03F` can only fire on slots 0–1. *(Adopted into §22 by FABLE, 2026-09-17, on
  `SWE2-DATA-REQ-FABLE-SEC22-5-BOXES`. The distributional labels of `BI-3a` remain hypotheses until a consumer body is
  read — §22.5 says so and nothing here changes that.)*

*(Pass 22 adjacency, 2026-09-14, tail rows: `003C8B70` calls **input** `0017DDC0` and `00313A00`
is called by **combat-action** `00313DB0` (2 edges) — same point as the Audio note: unclassified
means no domain tag, not no neighbours.)*

*(Pass 22 live-graph completion, 2026-09-15: `00313DB0` — the selection-cursor body — calls
`Gameplay` `0030D9A0` (1 edge); same point, unclassified is a tag state not a neighbour
claim.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** `BattleUnit_RunPeriodicCombatMaintenance` calls a cited function.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (16 edges through 8 of this page's functions).** The ActorEntity layer reaches this page at `003C8B70`, `0032E400`, `0030D9A0`, `0036A100` and 4 more. `FUN_002628b0` is the worked example, read in full - it is a 1,689-byte manager routine that indexes `02098E10` at the **`0x288` stride** - the same records the manager indexer walks - in a `0x50`-byte frame with a stack cookie; **7 of the 13 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

Every citation on this page is a census entry of unresolved or unowned code, so each layer below arrives with those bodies' ordinary call graphs. None of them is a claim this page makes.

**The weight of the neighbourhood is a pointer, not a classification.** 730 of the 865 edges are Presentation: `004309C0`, `0039AF70`, `0039B550` and `002F4020` alone account for 257 render-path edges (88, 72, 57 and 40). So the render pages are where these bodies' classification should start (tier 2, from callers only).

**CoreRuntimeScheduling — MECHANICAL, 14 edges.** `00181DD0` is called by `MainLoop_UpdateAndRenderFrame` (`0022B8C0`); `0024B9B0` calls `001EDDA0`; `00258D70` calls `00229EA0`; `00258D70` is called by `0022A770`; `00258E40` is called by `MainLoop_UpdateAndRenderFrame` (`0022B8C0`); `002F4020` calls `001EDDA0`; `0036D990` is called by `0022A0B0`; `00375470` is called by `00374FD0`; `003B99D0` calls `001EDDA0`; `003BA1F0` calls `001EDDA0`; `00434CD0` calls `00229E40`; `00435050` calls `00229E40`; `0053AB50` calls `001EDE70`; `InputDevice_QueryAvailabilityState_Always1` (`0053DD10`) is called by `0022B6E0`.

**Gameplay — MECHANICAL, 2 edges.** `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) is called by `BattleRuntime_GetModeDependentDistanceThreshold` (`00309A90`); `00313DB0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`).

**InputGameplay — MECHANICAL, 1 edge.** `00313DB0` calls `00313A00`.

**Movement — MECHANICAL, 5 edges.** `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) is called by `BattleRuntime_GetModeDependentBaseDistance` (`00309AE0`), `00311F70`; `002EACD0` is called by `00313500`; `002F7380` is called by `0026E290`; `00313DB0` is called by `00234520`.

**Party — MECHANICAL, 6 edges.** `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) is called by `00303CC0`, `00303F00`, `PartyFocus_SelectAndRequestDefaultActor` (`00326500`); `002EACD0` is called by `00312EE0`; `00313DB0` calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`); `003B7180` calls `PartyRoster_GetActorBySlot` (`00263750`).

**Presentation — MECHANICAL, 730 edges.** `004309C0` is called by `002F2530`, `003D83A0`, `003D92C0`, `00441B30` and 84 more; `0039AF70` is called by `003D92C0`, `004355D0`, `00437130`, `00438860` and 68 more; `0039B550` is called by `0039C4C0`, `0039C550`, `0039C5D0`, `0039C6B0` and 53 more; `002F4020` calls `003A3D10`, `00442550`, `004427D0`, `004453D0` and 36 more; `003970A0` is called by `0044CC50`, `0044D080`, `0044D4A0`, `0044DD00` and 25 more; `003A6E60` is called by `003A69F0`, `00422870`, `00441B30`, `00448DE0` and 25 more; `0036A100` is called by `002561C0`, `CharacterRenderSystem_AllocateAndInitialize` (`003325D0`), `003A7BE0`, `003A9790` and 22 more; `003A2B20` is called by `002F2530`, `003B0C50`, `004428F0`, `0044BAC0` and 19 more; `003AA280` is called by `00436D00`, `00502CB0`, `00503180`, `005375B0` and 17 more; `003A9EF0` calls `004354E0`, `00436D00`, `00500B70`, `00500C00` and 16 more; `0053AB50` calls `003CD2C0`, `003CD6C0`, `CharacterRenderRecord_EvaluateQ12PresentationChannel` (`003E48E0`), `003E6150` and 14 more; `004355D0` calls `00394B70`, `00395780`, `00395CF0`, `00396560` and 13 more; `00438860` calls `00394B70`, `00395780`, `00395CF0`, `00396560` and 13 more; `00437130` calls `00394B70`, `00395780`, `00395CF0`, `00396560` and 9 more; `00181DD0` is called by `002512B0`, `VFXSystem_RenderLayerPass` (`00258EE0`), `003820C0`, `003B4160` and 8 more; `003CD2C0` calls `003CD650`, `003CD840`, `003D2B60`, `00506B40` and 7 more; `003CCF20` calls `003CD840`, `003D2B60`, `00506B40`, `00507120` and 6 more; `00431B10` is called by `004490D0`, `0044BAC0`, `0044EDD0`, `0044F970` and 6 more; `00500980` calls `00436D00`, `00500C00`, `00501520`, `00502CB0` and 6 more; `00431D30` is called by `00438860`, `0044BAC0`, `00453CF0`, `004640A0` and 5 more; `00250000` is called by `002F2530`, `002F3BC0`, `0043EF40`, `0043F450` and 4 more; `003977B0` is called by `002B7B80`, `003C4070`, `003C46B0`, `00403640` and 4 more; `0039A150` is called by `00434CD0`, `00435050`, `00438860`, `004453D0` and 4 more; `00431B10` calls `003A9C10`, `003CD840`, `00506B40`, `00507490` and 4 more; `0024B9B0` calls `003A7050`, `003A7300`, `003A74F0`, `003A7EE0` and 1 more; `0039EC30` is called by `004355D0`, `00437130`, `00438860`, `004434D0` and 1 more; `00258D70` calls `003B25D0`, `003B4840`, `003CCF20`, `003D8190`; `003AFDD0` is called by `003B0C50`, `00438860`, `0044BAC0`, `00502280`; `RelationLook_SolveAnglesAndMatrices` (`005131C0`) calls `FCPPayload_ResolvePrimaryConfigBlock` (`003E56A0`), `003E5B30`, `003E5FA0`, `RelationLook_BeginNeutralReturn` (`00513150`); `00258E40` calls `003B4840`, `003CCF20`, `003D8190`; `002F7380` calls `00467AA0`, `00467B00`, `00467B10`; `00396F20` is called by `004355D0`, `00437130`, `00438860`; `0039E820` is called by `004355D0`, `00437130`, `00438860`; `003D2B60` is called by `003A9C10`, `003CCF20`, `003CD2C0`; `00432CC0` is called by `004355D0`, `00437130`, `00438860`; `00504C40` calls `003CD590`, `005049E0`, `00521250`; `RenderModelInstance_EnsureSubresourceVariantBinding` (`00504D30`) calls `003CCB60`, `003CCC20`, `003CD7C0`; `00521450` is called by `00438860`, `00501A50`, `00502280`; `0024CFF0` is called by `CharacterRenderRecord_TeardownAndReset` (`004200A0`), `CharacterRenderRecord_UpdateRootAnimationPresentationPhase` (`0042C410`); `0024E2F0` is called by `003ACC10`, `003B4A50`; `0024E6D0` is called by `003ACC10`, `003B4A50`; `0024FE30` calls `003B1260`, `003B2830`; `002DEBB0` is called by `003B2310`, `003E9780`; `002FC4A0` calls `002FBA60`, `003EDAD0`; `0032E400` is called by `003B2310`, `003B53C0`; `0036B130` is called by `003CCF20`, `003CD2C0`; `0036D930` is called by `0044BAC0`, `00462260`; `0036DD90` is called by `0040ACF0`, `0040D890`; `0039E820` calls `003A2C70`, `003A3D20`; `0039EC30` calls `003A2C70`, `003A3D20`; `003A3E30` calls `003B02A0`, `003B0FD0`; `003A9C10` calls `002D81D0`, `003D2B60`; `003B02A0` calls `003B0980`, `003B0B70`; `003B0C50` calls `003B02A0`, `003B1260`; `003B18E0` calls `0024F410`, `003B21E0`; `003CCB60` is called by `00468160`, `RenderModelInstance_EnsureSubresourceVariantBinding` (`00504D30`); `003CCC20` is called by `00468160`, `RenderModelInstance_EnsureSubresourceVariantBinding` (`00504D30`); `003CD5D0` is called by `RenderModelInstance_RemoveSubresourceVariantBinding` (`00504610`), `00504C40`; `003CD650` is called by `003CD2C0`, `RenderModelInstance_RemoveSubresourceVariantBinding` (`00504610`); `003CD840` is called by `003CCF20`, `003CD2C0`; `0043E440` calls `003A2C70`, `003A3D20`; `00468160` calls `003CCB60`, `003CCC20`; `RenderModelInstance_RemoveSubresourceVariantBinding` (`00504610`) calls `003CD590`, `003CD650`; `00506B40` is called by `003CCF20`, `003CD2C0`; `00507120` is called by `003CCF20`, `003CD2C0`; `00507490` is called by `003CCF20`, `003CD2C0`; `005080A0` is called by `003CCF20`, `003CD2C0`; `00508C90` is called by `003CCF20`, `003CD2C0`; `00509BB0` is called by `003CCF20`, `003CD2C0`; `0050A100` is called by `003CCF20`, `003CD2C0`; `0050AC20` is called by `003CCF20`, `003CD2C0`; `RelationLook_SolveAnglesAndMatrices` (`005131C0`) is called by `CharacterRender_UpdateCombatLookAndAuxControllers` (`003E00C0`), `003E3B80`; `InputDevice_QueryAvailabilityState_Always1` (`0053DD10`) is called by `004355D0`, `00462540`; `0024E2F0` calls `003B0BF0`; `002EACD0` calls `003B02A0`; `002F4020` is called by `00441970`; `002FC9B0` is called by `003B02A0`; `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) is called by `BattleUnit_ComputePresentationSuppressionMask` (`003125E0`); `0036DF80` calls `003B27A0`; `0036E700` calls `003B02A0`; `0036E750` calls `003B02A0`; `00375470` is called by `EffectSystem_ProcessQueuedGraphicsEffectsForPass` (`00375500`); `003A28C0` is called by `00465690`; `003A2B60` is called by `00441B30`; `003A3E30` is called by `003337B0`; `003A9EF0` is called by `003ED8A0`; `003B02A0` is called by `003B0C50`; `003B0B70` is called by `003B02A0`; `003B0C30` calls `003B02A0`; `003B0C30` is called by `CharacterRenderRecord_UpdateRootAnimationPresentationPhase` (`0042C410`); `003B1260` is called by `003B0C50`; `003B1A80` calls `003B2310`; `003B2310` is called by `003B25D0`; `003BA1F0` calls `003B02A0`; `003CD2C0` is called by `0053AB50`; `003D7CE0` is called by `00504060`; `00431F10` is called by `00434CD0`; `00434CD0` calls `00399B80`; `00434CD0` is called by `004355D0`; `00435050` calls `00399B80`; `00435050` is called by `004355D0`; `004355D0` is called by `00449AB0`; `00436D00` calls `004352C0`; `00436D00` is called by `003A9EF0`; `00437130` is called by `004355D0`; `00438860` is called by `004355D0`; `thunk_FUN_00436d00` (`0043D8E0`) is called by `003AA470`; `0043D8F0` is called by `00438860`; `0043E440` is called by `00438860`; `00449970` calls `0044A180`; `00449970` is called by `002F3BC0`; `00449AB0` calls `004355D0`; `00449AB0` is called by `002F4020`; `00468160` is called by `002F6AB0`; `00500980` is called by `003A9EF0`; `RenderModelInstance_RemoveSubresourceVariantBinding` (`00504610`) is called by `CharacterRenderRecord_RemoveModelSubresourceVariantBindings` (`003E69E0`); `00504C40` is called by `RenderModelInstanceContainer_DestroyInstanceByIndex` (`00478070`); `RenderModelInstance_EnsureSubresourceVariantBinding` (`00504D30`) is called by `CharacterRenderRecord_EnsureModelSubresourceVariantBindings` (`003E7210`); `00538DB0` calls `00500470`; `0053AB50` is called by `0053D780`.

**Resource — MECHANICAL, 19 edges.** `0032E400` is called by `00249210`, `0024AC30`, `00259DF0`, `00379E90` and 4 more; `0036A100` is called by `00249210`, `0024EF90`, `0024F240`; `003B18E0` calls `0032E4D0`, `0032E520`, `0032E590`; `003B2310` calls `0032E400`, `0032E620`; `002FC4A0` calls `002DF980`; `002FCFF0` calls `0032E400`; `00504C40` calls `00409CA0`.

**Rewards_Progression_Economy — MECHANICAL, 1 edge.** `002EACD0` is called by `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`).

**Script_VM_Native_Bridge — MECHANICAL, 53 edges.** `InputDevice_QueryAvailabilityState_Always1` (`0053DD10`) is called by `00341840`, `00341F90`, `00345250`, `00346AA0` and 13 more; `003576D0` is called by `0034B880`, `0034BC90`, `0034C0F0`, `0034C430` and 2 more; `00357620` is called by `00342A80`, `00353860`, `00353C50`; `0036DDC0` is called by `0034EF60`, `0034FD80`, `003501D0`; `0024CFF0` is called by `00342A80`, `003433A0`; `00357620` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`), `VMResult_WriteInt32` (`0026B4E0`); `0036DF80` is called by `003504D0`, `00350990`; `003B7180` is called by `0034D330`, `00350F30`; `002DEBB0` is called by `0034B650`; `002EFD80` is called by `00354670`; `002EFDC0` is called by `00354090`; `0032E400` is called by `0050DF70`; `003576D0` calls `VMValueStack_PopInt32CoerceFloat32` (`00267E10`); `0036A100` is called by `0050D8F0`; `0036B130` is called by `0050D5E0`; `0036E320` is called by `003576D0`; `0036E460` is called by `0034D690`; `0036E500` is called by `00354CB0`; `0036E540` is called by `0034D740`; `0036E5A0` is called by `0034EF60`; `0036E5E0` is called by `00355F40`; `0036E750` is called by `00357620`; `003EA430` is called by `00352E80`; `003EA540` is called by `00353C20`.

**UI — MECHANICAL, 19 edges.** `003C8B70` calls `00254B40`, `0028FFE0`, `0035BAD0`, `0035BAF0` and 10 more; `0017DDC0` is called by `003C8B70`; `00181DD0` is called by `0024B9B0`; `00258D70` calls `0024B9B0`; `00258E40` calls `0024B9B0`; `InputDevice_QueryAvailabilityState_Always1` (`0053DD10`) is called by `003C80C0`.

**World — MECHANICAL, 1 edge.** `0032E400` is called by `00378540`.

**WorldAreaField — MECHANICAL, 14 edges.** `0032E400` is called by `MapRef_BeginLoadResources` (`00268750`), `003319D0`, `00378030`, `00379A10` and 1 more; `0036A100` is called by `00267930`, `003319D0`, `AreaArd_LoadOrUnloadFieldResource` (`003EA820`); `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`); `00313A00` calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`); `00313A00` is called by `BattleSystem_RunFieldFrameOrchestrator` (`00234590`); `00313DB0` calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`); `0036E1E0` is called by `World_UpdateSimulationTick` (`00314020`); `InputDevice_QueryAvailabilityState_Always1` (`0053DD10`) is called by `003789A0`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
