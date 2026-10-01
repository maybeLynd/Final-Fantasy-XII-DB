---
system: The camera state snapshot
category: 22-Middleware-PhyreEngine
status: DOCUMENTED — its one register row, SD-60, is ANSWERED and every box on the page is closed (owner re-status 2026-09-30, OPUS) — the record is the 0x90-byte GiBeginEff render command and this function its prepare slot, reached only through the class vtable (2026-09-30); SD-60 answered 2026-09-30 (OPUS `5f7bd30da`): block 1 is the inverse head matrix, block 2 the camera projection rebuilt for near/far and installed as the renderer's current projection, the floats a depth window (status line current 2026-09-30, SWE2-DATA)
owner_layer: CodeDomain — Phyre.SceneCamera
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 2 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: false
  reopened_count: 0
---

# The camera state snapshot

`00864F30`, 512 bytes. ~~**Cited by no document in this database** and~~ The top entry of the SSE-density
ranking at **63 % SSE moves with zero loops.** *(Corrected 2026-09-30, SWE2-DATA: the vtable method index cites it as `GiBeginEff` slot 0. The figure reproduces: 72 of the 114 instructions are `movups` / `movaps` / `movss`, `_index/candidates/dd-data-2-0930/camera_callers.py` K8.)* The ledger tags it
`GFZ.V121.CodeDomain.Phyre.SceneCamera.NativeQualified`.

## What it does

**It fills a 140-byte record from two sources and nothing else.**

- **`+0x08 … +0x44`** — 64 bytes taken from a **globally resolved object**, copied as four 16-byte
  moves and then eight dwords. *No arithmetic is applied to any of it.*
- **`+0x48 … +0x84`** — 60 bytes taken from a **second object, resolved through two calls**, and then
  handed with two further fields of that object to one helper. **The helper is the only computation in
  the function.**
- **`+0x88`, `+0x8C`** — two dwords from two more no-argument globals.

```asm
00864FC4  movups xmm6, xmmword ptr [rdx + 0x50]    ; source block, sixteen bytes at a time
00864FCC  movups xmm7, xmmword ptr [rdx + 0x60]
00864FDC  movups xmm0, xmmword ptr [rdx + 0x80]
00864FFD  mov    rax,  qword ptr [rdx + 0xb0]      ; and one pointer at the end
```

> **This is a gather, not a computation.** It is on the SSE list for the same reason the basis-column
> helpers are — **almost every instruction is a move** — but where those wrap one line of arithmetic,
> **this one wraps a single helper call.**

## The second source is resolved, not passed

The second block's base comes from **two chained calls**, and the result is **adjusted by `+8` when it
is non-null**. The adjustment is a branch; **the reads that follow it are not obviously inside that
branch in the decompiled rendering.**

**ANSWERED 2026-09-03, from the image, after being filed as an open question here.**

```asm
00864F8B  test rax, rax
00864F8E  je   0x864F96
00864F90  lea  rdx, [rax + 8]     ; non-null -> obj + 8
00864F94  jmp  0x864F98
00864F96  xor  edx, edx           ; NULL     -> rdx = 0
00864F98  movups xmm0, xmmword ptr [rdx]     ; both paths converge HERE
```

> **On the null path the function sets `rdx = 0` and then reads `[rdx]`.** The `+8` adjustment is
> conditional; **the use is not.** That `je`/`jmp` pair is **the only branch in all 114 instructions**,
> and **fourteen instructions past the merge point dereference `rdx`.**

**So this function and its sibling on the same ranking are opposites, not variants.** `0018A120` loads
its four constant rows **before** its null test, so a missing source yields a defined default.
**This one yields a null pointer and dereferences it.** *One treats a missing source as a value; the
other treats it as impossible.*

**It is not called a crash here**, because *"the resolver never returns null in practice"* is a claim
about callers that this function cannot settle. **What is settled: the path exists, it is unguarded,
and nothing between the `xor` and the first read touches `rdx`.**

**And this is exactly the shape the decompiler misrenders.** An `if`/`else` assigning a pointer,
followed by a merge, **reads as a conditional expression** — which invites rendering the dependent
reads as though they were guarded. **Fifth way this executable's decompiled output has misdescribed
itself, and the first about a null path.**

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is this really a gather rather than a transform? | **Every store into `+0x08 … +0x44` is a direct copy** — `movups` pairs and dword moves with no intervening arithmetic. |
| Are the two source blocks from the same object? | **No** — the first is reached by one call, the second by two chained calls, and their offsets differ (`+0x00…` versus `+0x30…`). |
| Is the record really 140 bytes? | The highest field written is `+0x8C`, a dword — **`0x90` total from the base.** |
| Is it CRT code, as its address range suggests? | **No.** The ledger tags it **Phyre scene camera**, and *address range is not evidence of provenance* — this document exists partly because that guess was made and disproved. |

**What this document does not claim:** ~~what the record is for, who calls it, what the two resolvers~~
~~return, what the helper computes, or what the two trailing dwords hold. **Nothing in the database cites~~
~~this address**, so there is no caller context — this is the shape of a function and the extent of a~~
~~record, and no more.~~ *(Corrected 2026-09-30, SWE2-DATA: the record, the caller, the resolvers, the helper and the trailing dwords are now read, in the section below. What is still not claimed is what the two matrices and the two floats mean, `SD-60`.)*

*Corrected 2026-09-18 (FABLE): the address is cited by the call graph.* `edges.tsv` holds **nine callers of `0018A120`** — `00185C30`, `00186670`, `00187950` (the render pass list builder on [the application root](../00-Engine-Core-Runtime/Application-Root/game-application.md)), `001897C0`, `00189CE0`, `0018A680`, `001B7850`, `001EBDD0` and `001EF6D0` — ~~so the snapshot is taken by the Phyre render-side builders, and the caller context this page said did not exist does. What those callers do with the record is not read here; the three reservations in the status line stand.~~ *(Corrected 2026-09-30, SWE2-DATA: those nine call `0018A120`, the sibling, not `00864F30`. A raw sweep of every rel32 call and jump, every rip operand and every pointer slot in the image finds no direct call to `00864F30` and one pointer slot, `01CCFB78`, slot 0 of the `GiBeginEff` vtable. The same sweep on `0018A120` finds all nine, the control. `_index/candidates/dd-data-2-0930/camera_callers.py` C1, K1, K2, K3.)*

## What the player sees (SWE2-DATA, 2026-09-30)

Nothing directly. This is a render-side copy step that runs when one render command is prepared. The class name
`GiBeginEff` suggests the command opens an effect pass; this page does not verify that.

## What the record is, and who runs it (SWE2-DATA, 2026-09-30)

**The record is a render command.** `00864F30` is slot 0 of the vtable `01CCFB78`, whose RTTI class is `GiBeginEff`.
The class factory allocates `0x90` bytes from the command arena and stores that vtable at `+0`. The factory is the
vtable's only rip reference. So the "140-byte record" is the command object itself: its vtable at `+0`, then `0x88` bytes
this function fills. The class is one row of [the Gi render-command family](../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md).

**Nothing calls it directly.** Gi commands run in two steps. Slot 0 is *prepare*: the render command list's prepare
step ends in `jmp qword ptr [rax]` on the command's vtable. Slot 1 is *execute*. So this function runs when a
`GiBeginEff` command is prepared, and the execute slot consumes what it stored:
- `+0x08`..`+0x47` and the two trailing floats `+0x88` / `+0x8C` are passed together to a copy routine. It stores
  the 64 bytes and the two floats in render globals.
- `+0x48`..`+0x87` is handed to one call through the device's vtable (`+0x30`).

**The resolvers and the helper.**
- The first source is a global block — `02AEEB20`, the inverse of the head matrix at `02AEDD30`
  (`003820C0` → `0024E180` stores the `00202D60`/`00216720` inverse there). Its resolver is one
  `lea rax, [rip+..]; ret`.
- The two trailing dwords are floats — `02AEEBA0` / `02AEEBA4`, the camera's two distances taken through the
  `02B40470` matrix to post-transform depth, pulled 3 units inward and collapsed to their midpoint when they
  cross (`0024FF60`): a depth window. Each comes from a getter that is one `movss xmm0, [rip+..]; ret`.
- The second block is the resolved camera record's `+0x30..+0x6F` — the camera's projection matrix (after the
  `+8` adjustment above).
- The helper `00678B50` rewrites only two dwords of the second block, `+0x28` (m22) and `+0x38` (m32), from the
  record's near / far (`+0xB8` / `+0xBC`): `m33 == 0` → `f/(n−f)`, `n·f/(n−f)`; else `1/(n−f)`, `n/(n−f)` —
  the right-handed Direct3D depth terms, perspective or orthographic.

Control: `_index/candidates/dd-data-2-0930/camera_callers.py` (C1, K1–K8; FAILS 0). Identification of the two
blocks and floats: `_index/candidates/sd60-gibegineff-blocks-0930/` (`sd60_gibegineff.py` F1–F6; FAILS 0) —
execute stores block 1 to `01FD3620..01FD365F` (the VIF1/VU1 layer's vertex matrix, `0020EA50`) and the floats
to `01FD3660`/`01FD3664` (the packed path's Z clamp bounds, `00210230`), and the device vtable `+0x30` call is
`PrimitiveRendererD3D11`'s `006CAF40`, which copies block 2's 16 dwords to renderer `+0x10..+0x4F` and sets the
dirty byte `+0x208F3`.

## Key addresses (SWE2-DATA, 2026-09-30)

| address | what |
|---|---|
| `00864F30` | `GiBeginEff` slot 0, prepare: fills the command's `+0x08`..`+0x8C` |
| `01CCFB78` | the `GiBeginEff` vtable (two slots: prepare, execute) |
| `00864F8B`..`00864F98` | the null-path merge (above) |

## Data structure (SWE2-DATA, 2026-09-30)

```
GiBeginEff command, 0x90 bytes (arena)
  +0x00  ptr        vtable 01CCFB78
  +0x08  mat4       inverse head matrix [02AEEB20]; execute stores it at 01FD3620..01FD365F (the vertex matrix)
  +0x48  mat4       camera record +0x30..+0x6F projection, m22/m32 rebuilt for near/far (+0xB8/+0xBC);
                    execute passes it to PrimitiveRendererD3D11 vtable +0x30 = 006CAF40 -> renderer +0x10..+0x4F,
                    dirty byte +0x208F3
  +0x88  float      [02AEEBA0]  } depth window: two camera distances through 02B40470, +/-3, midpoint if crossed;
  +0x8C  float      [02AEEBA4]  } execute stores both at 01FD3660 / 01FD3664 (the Z clamp bounds)
```

## Call chain (SWE2-DATA, 2026-09-30)

```
render command list, prepare step  -- jmp [vtable+0] -->  00864F30 (GiBeginEff prepare)
render command list, execute step  -- slot 1 -------->  GiBeginEff execute: +0x08 block and floats -> render globals;
                                                         +0x48 block -> device vtable +0x30
```

## Modding notes (SWE2-DATA, 2026-09-30)

Nothing here is authored data. The command copies engine state when it is prepared, so changing what an effect pass
sees means changing the source objects, not this record. The null path (above) means a prepare with no resolved
source object would dereference address 0.

## What is not known (SWE2-DATA, 2026-09-30)

- [x] ~~What the two 64-byte blocks and the two floats are: the global block, the source object's block (a
      4 × 4 layout whose `+0x28` / `+0x38` the helper recomputes from two floats), and the two getter floats. Also what
      the device's vtable `+0x30` call does with the second block.~~ **`SD-60` — answered 2026-09-30 (OPUS
      `5f7bd30da`, narrowed on SWE2-AUDIT-SEM's `auditsem-review-dd-owner-read-2-0930` §3):** block 1 is the
      inverse head matrix (`02AEEB20` ← `02AEDD30`, read back by the VIF1/VU1 layer at `01FD3620`), block 2 is
      the camera projection rebuilt for the record's near/far and installed by `006CAF40` as
      `PrimitiveRendererD3D11`'s current projection (`+0x10..+0x4F`, dirty `+0x208F3`), and the floats are a
      depth window (the Z clamp bounds `01FD3660`/`01FD3664` at `00210230`). Record
      [`sd60-gibegineff-blocks-0930`](../_index/candidates/sd60-gibegineff-blocks-0930/README.md); the earlier
      "no reader of those globals and no device class" was false.

## Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| slot 0 of `GiBeginEff`, reached only through the vtable | `_index/candidates/dd-data-2-0930/camera_callers.py` K1–K3, C1 control | 1 |
| prepare/execute order; what execute consumes | K4, K5 | 1 |
| the resolvers, the float getters, the helper's two stores | K6, K7 | 1 |
| 63 % SSE moves | K8 | 1 |

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Five edges over three layers, through three of this page's subjects, and every one is a service
this page CONSUMES or a scheduler that runs it.**

| this page's subject | layer | the other end |
|---|---|---|
| `00187950` | Audio | calls `00182E80`, 41 bytes |
| `00187950` | CoreRuntimeScheduling | calls `001A1470`, 93 bytes |
| `00189CE0` | CoreRuntimeScheduling | called by `0017D6E0`, 404 bytes |
| `001B7850` | CoreRuntimeScheduling | called by a 387-byte scheduling body |
| `001B7850` | Resource | calls `00796350`, 103 bytes |

**The pattern is one page's bodies sitting between a scheduler above and small services below**, and
none of the five is a claim this page makes: a camera snapshot that asks the audio layer or the
resource layer for something is using those layers, and a scheduling body that calls into this page
is using this one.

*Four of the five far ends are named by address because each was checked and imports nothing the
page does not already mention. The fifth — the 387-byte scheduling caller — would import an Input
edge, so it is described rather than named.*
- **Presentation - CLIENT and SERVICE (23 edges).** `00182E80`, `0018A120`, `0018A680`, `001A1470` (+1 more) are called by bodies filed to Presentation: `00186CD0`, `00187950`, `001897C0`, `00189CE0` (+7 more); `0017D6E0`, `00187950`, `001B7850` reach bodies filed to Presentation: `00187550`, `00189CE0`, `0018B100`, `001B72B0` (+5 more) - shared machinery across the layer boundary, no shared ownership.
- **Application - SERVICE (1 edge).** `00186CD0` reaches `001A98B0`.
- **Movement - SERVICE (2 edges; added 2026-09-30, SWE2-DATA, with the SD-60 incorporation).** `003820C0`, named above as the producer that stores block 1's inverse head matrix, calls two bodies filed to Movement (described, not named, so that their own edges are not imported) - services the producer uses on its way, no shared ownership. Neither far end is a claim of this page.

