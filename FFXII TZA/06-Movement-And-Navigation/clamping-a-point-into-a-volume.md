---
system: Clamping a point into a volume
category: 06-Movement-And-Navigation
status: AUDITED — SD-180 and SD-181 are ANSWERED and every box on the page is closed (owner re-status 2026-09-30, OPUS) — the second result is an output: the one caller of 00363FD0 keeps the nearest of a chain of segments by it (2026-09-30, SWE2-DATA); the history's reader found 2026-09-18 (0025C830, the two-point test); what the emitter-volume walk does with the clamped point (SD-180) and which file carries the volume records (SD-181) are answered in the register and on the page (status line current 2026-09-30, SWE2-DATA)
owner_layer: CodeDomain — shared geometry
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 4 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
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
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record first-read-repos-55; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# Clamping a point into a volume

`00361DE0` (1,102 B), `003623C0` (1,122 B) and `00363FD0` (537 B). **All three surfaced on the
SSE-density ranking at 47-50 % with no loops**, all three cited by one document as members of a shared
workbench, and **none of them read.** Taken as a family, because three entries from one document are
one under-described document counted three times.

## `00361DE0`: a point pushed onto the boundary of a rotated ellipse

**The volume is four fields:** a centre at `+0x20`, two radii at `+0x30` and `+0x34`, and **a rotation
angle at `+0x50`.**

```asm
00361E02  comiss xmm9, dword ptr [r8 + 0x30]   ; radius 0 <= 0 ?
00361E10  comiss xmm9, dword ptr [r8 + 0x34]   ; radius 1 <= 0 ?
00361E15  jnc    <degenerate>
00361E22  movups xmmword ptr [0x022D92B0], xmm1   ; the point, into GLOBAL scratch
00361E36  subss  xmm1, xmm2                       ; point - centre
```

**A volume with either radius at or below zero collapses to its centre** — the output is the centre
itself with `w = 1.0`, and no arithmetic runs at all. **That is a defined behaviour, not a guard.**

Otherwise: the offset from the centre is **rotated by `cos`/`sin` of the authored angle**, the
**ellipse radius in the point's own direction** is computed from the two inverse-square radii, and

- **if that radius is at or below the point's distance, the point is outside** and the output is
  `centre + offset × (radius / distance)` — **on the boundary, in the original unrotated frame**;
- **otherwise the point is returned unchanged.**

> **Only two components are rotated and tested.** The third is carried through the scale but never
> enters the ellipse test — **so this is a 2-D containment applied to a 3-D point**, which is what a
> ground-plane volume in a world with height looks like.

**Zero and negative intermediates are handled by two dedicated helper calls before use**, not by
branches around the arithmetic — the function checks `== 0.0` and `< 0.0` separately and calls a
different helper for each.

## `00363FD0`: the closest approach parameter, returned twice

Given two points and a direction, it computes the parameter of closest approach, **clamps it between
two authored constants**, and returns it.

> **And it returns a second value through a global.** The squared distance at that parameter is left in
> the shared scratch block, where a caller must read it. **A function with one return value and two
> results.**

**When the direction's squared length is not positive, the clamp's lower constant is returned
unchanged** — a degenerate direction yields the low bound rather than an error.

*(Added 2026-09-30, SWE2-DATA.)* The arguments are point A (`rcx`), point B (`rdx`) and a direction (`r8`),
copied to `022D92B0` / `022D92C0` / `022D92A0`. The parameter is `t = −dot(B − A, dir) / |dir|²`, and the two
~~clamp constants are `0.0` (`01EF93F0`) and `1.0` (`01EF93FC`)~~ clamp bounds are loaded from `01EF93F0` (0.0) and `01EF93FC` (1.0), so `t` is a position along a segment from B. *(Corrected 2026-09-30, SWE2-DATA, per SWE2-AUDIT-SEM's batch-5 review C1: the bounds are not constants. `01EF93F0` / `01EF93FC` are the x and w lanes of a `.data` cell, the software `vf00` image, which `00363FD0` loads live. Its three writers `0036D9A8`, `0036D9E8` and `0036DD87` all store `[0, 0, 0, 1]`, so the bounds read 0.0 and 1.0 in practice, as a load and not an immediate ([CONTRACT-transform-primitives](../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md) §15b).)* The
second result is `|(B − A) + t·dir|²`, stored to `022D92D4` (`003641DC`) and `022D92E4` (`003641D4`). `_index/candidates/dd-data-5-0930/mv_clamp_checks.py` A1–A3.

## `003623C0`: the same record, clamped as a box

**The third of the family takes the identical volume record** — same centre at `+0x20`, same two
extents at `+0x30`/`+0x34`, same angle at `+0x50`, **same collapse-to-centre when either extent is at
or below zero** — and clamps into a **rectangle** instead of an ellipse.

**It normalises each axis by its own extent**, builds an **outcode** from four comparisons against
`±1`, clamps both normalised coordinates into `[−1, +1]`, and

- **if the outcode's `0x33` bits are all clear the point is inside** and is returned unchanged;
- otherwise the clamped coordinates are multiplied back by the extents, **rotated by the negative of
  the angle**, and added to the centre.

**The vertical component is carried through untouched**, exactly as in the ellipse version — *the same
2-D containment on a 3-D point.*

> **Three functions, one record format, three shapes.** Nothing in the volume says whether it is an
> ellipse, a box, or a line to measure against — **the shape is the function the caller invokes.**
> Same pattern as the four sound-selection policies over one descriptor and the two remapping policies
> over one binding array: **this engine stores one format and selects behaviour by entry point.**

**And the outcode is kept.** Before the four tests, the global holding it is **shifted left by six**,
and afterwards masked to **24 bits**:

```asm
003625FB  mov eax, dword ptr [0x022D9130]
```

**Six bits per call, twenty-four bits retained — the last four outcodes**, and the result is copied to
a second global. **Nothing in this function reads the history back**, so what it is for is not
established here; that it *is* a history is arithmetic.

## The workbench is the finding

**Neither function computes in registers or on the stack. Both compute in a fixed global block**
around `022D9198 … 022D9318`, writing intermediates to absolute addresses.

> **These functions are not reentrant, and they cannot be**: two callers overlapping in time share one
> set of intermediates. **Anything hooking either one — or calling them from a second thread — is
> writing into the other's working memory.**

**And it is why they ranked so high on SSE density with no loops:** almost every instruction is a move
between a parameter and a fixed global, around a few lines of arithmetic. **The ranking found them for
exactly the reason they are worth documenting.**

## A third user of the workbench, and it borrows its caller's argument

`00521BB0` (1,757 B, **56 % SSE, one loop**) blends two 64-byte records into a third. **It computes in
the same global block** — `022D92xx` — plus a second region at `022D8Fxx`, confirming the scratch is
**shared across the geometry layer rather than private to one family.**

**The blend weight is a ratio of one component of two vectors, and which component is chosen by
rotating the data rather than by indexing it:**

```asm
00521E90  shl   ebx, 0x1
00521E9F  andps xmm0, xmm13          ; absolute value, by mask
00521EAE  movss dword ptr [0x022D92A0], xmm5
00521EBA  movss dword ptr [0x022D8FA0], xmm5   ; the same value, two scratch regions
```

**A count supplied by the caller drives a loop that cycles both three-vectors' components left one
place per iteration**, until the count reaches a global sentinel. **The wanted component always ends
up first**, and the weight is then `a[0] / (a[0] + b[0])`.

> **That is why a family that is otherwise loop-free has a loop here: the axis is selected by moving
> the data, not by indexing it.**

**And the loop decrements a field inside the caller's own argument structure, then restores it from a
copy saved at entry.**

> **The function temporarily corrupts a structure it does not own.** A concurrent reader of that field
> sees a value counting down to a sentinel; anything that observes it mid-call observes garbage. **The
> restore makes it invisible to the caller and not to anything else.**

Two of the four rows are scaled by one global on the way in and by a second on the way out, so **the
blend is not a plain lerp: two rows carry a scale the other two do not.** *(Anchored 2026-09-30, SWE2-DATA: the
way in is the broadcast of `022D9380` multiplied into two rows at `00521C46`–`00521C6B`; the way out is the multiply
at `00522211`–`0052221B`.)*

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the degenerate case a guard or a defined result? | It **writes the centre and `w = 1.0` to the output** and returns — a produced value, not an early-out. |
| Are the two radii really radii? | Both are **squared and inverted** (`1 / (r × r)`) and used as the two coefficients of an ellipse form. |
| Is the third component tested? | **No** — it is scaled with the others in the output, but only two components enter the squared sums that the comparison uses. |
| Is the global scratch really shared between the two? | **Both write `022D92B0` and `022D9198`**, in different roles, from independently compiled bodies. |
| Is the box version a copy of the ellipse version? | **No** — same prologue and same degenerate rule, but the ellipse scales **radially by one factor**; the box **clamps each axis independently and rotates back by the negated angle.** Different arithmetic, same record. |
| Is the shifted global really a history? | **Shifted left 6, four bits OR-ed in, masked to 24** — the arithmetic retains exactly four generations. **Its reader is found (2026-09-18, FABLE): `0025C830`** (ActorEntity, 3,118 B, one caller `0025C170`) calls the sibling clamp `0025A8E0` twice on the workbench pair `022D9300` / `022D9350` and then reads `022D9130` (`0025CEFA`), splitting off the two newest outcodes — `(h >> 6) & 3`, `(h >> 6) & 0x3000`, `h & 0x30000`, `h & 0x30` (`0025CF00`–`0025CF26`) — so the history is how a two-point test recovers the outcode of the point clamped just before it, the classic segment-against-box use; `00521450` (1,886 B) shifts the same global with the same arithmetic and is a third sibling of the clamp. ~~What the second result is for is still not established.~~ *(Corrected 2026-09-30, SWE2-DATA: see the last row.)* |
| Is the rotation loop really an axis selector? | It **cycles three components left one place per iteration** and the weight is then taken from index 0. **A selector implemented as a rotation, with the count as the index.** |
| Does the caller's field really get restored? | Saved to a local at entry and **written back as the last statement**, after the loop has driven it to a sentinel. |
| Could the second "result" be a leftover rather than an output? | ~~**Not established.** It is written last and never read in-body — *consistent with* an output, and this document does not identify a consumer.~~ *(Corrected 2026-09-30, SWE2-DATA: **an output.** `00363FD0` has one caller, the 388-byte segment-chain body that the pass-22 block below files to Audio. It loads `022D92D4` right after each call and keeps the segment with the smallest squared distance, then writes that segment's closest point. `_index/candidates/dd-data-5-0930/mv_clamp_checks.py` A4, A7.)* |

**What this document does not claim:** what the volume is used for, ~~who calls either function, what the~~
~~two clamp constants are (they are `.data` addresses, not immediates),~~ what the two zero/negative
helpers do~~, or whether any caller actually reads the global left behind by `00363FD0`~~.
*(Corrected 2026-09-30, SWE2-DATA: the callers, the ~~constants~~ bounds (`0.0` and `1.0`) and the reader of the second result
are now read. The struck "they are `.data` addresses, not immediates" was true and is restored: see the C1 note in the section on `00363FD0` and [CONTRACT-transform-primitives](../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md) §15b. See the added sections below and `_index/candidates/dd-data-5-0930/mv_clamp_checks.py`.)*


## What the player sees (SWE2-DATA, 2026-09-30)

Nothing directly. The clamps pull a point onto an authored area: an ellipse, a rotated box, or a chain of segments.
The one reader read here is the sound-emitter walk, which measures a ~~listener-side~~ point against an emitter's volume
record. ~~So the player hears the effect as where a sound seems to come from, not as a visible shape.~~ *(Corrected 2026-09-30, SWE2-DATA, per SWE2-AUDIT-SEM's batch-5 review N2: that this is heard as where a sound comes from is an inference from the ledger's Audio filing of `003631B0`, `00361810`, `003638B0` and `00362850` (the last reads the party-focus handle). The bodies after the clamp are not read here (`SD-180`'s row).)*

## Key addresses (SWE2-DATA, 2026-09-30)

| address | role |
|---|---|
| `00361DE0` | the ellipse clamp (record kind 0) |
| `003623C0` | the box clamp (record kind 1), keeps the four-deep outcode history in `022D9130` |
| `00363FD0` | the closest point on a segment: returns `t` in [0, 1], leaves the squared distance in `022D92D4` |
| `022D92A0`..`022D9318` | the shared scratch block (the workbench) |
| `01EF93F0` / `01EF93FC` | ~~the clamp constants `0.0` / `1.0`~~ the clamp bounds: x and w lanes of the `.data` `vf00` image, loaded live and stored `[0, 0, 0, 1]` by `0036D9A8` / `0036D9E8` / `0036DD87` ([CONTRACT-transform-primitives](../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md) §15b) |
| `0025C830` | the reader of the outcode history (2026-09-18) |

## Call chain (SWE2-DATA, 2026-09-30)

The volume walk (the 512-byte Audio-filed body) reads each volume record's byte `+9` (`& 0x7F`) and dispatches on it:
- 0 calls the ellipse clamp `00361DE0`;
- 1 calls the box clamp `003623C0`;
- 2 calls the 388-byte segment-chain body. That body walks `[record+0x14]` segments of `0x20` bytes from
  `record+0x40` (a start, then a direction), calls `00363FD0` for each, keeps the nearest by the squared distance, and
  writes `start + t·dir`;
- any other value leaves the point unchanged.

So the record's kind byte chooses the shape. "The shape is the function the caller invokes" is true one level down:
the caller reads the choice from the record. The records are offsets from a base held at `022CBAF0`. Evidence:
`mv_clamp_checks.py` A7, A8; the walk's own caller is listed in that script's output.

- [x] **What the volume walk does with the clamped point:** the record's `+0x38`, `+0x54` and `+0x58` floats it reads
  after the clamp, and what it returns to its caller. **SD-180** (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30; register row SD-180, record [`sd180-181-emitter-walk-0930`](../_index/candidates/sd180-181-emitter-walk-0930/README.md).)*
- [x] **Which shipped file carries the volume records** that the base at `022CBAF0` points into. **SD-181**
  (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30 (OPUS `2e1bb015e`); register row SD-181, record [`sd181-sp1-loader-0930`](../_index/candidates/sd181-sp1-loader-0930/README.md): slot 16 (`SP1`, the sound-emitter section) of the current map's `map_ctrl` pack `<map>.mpk`, stored by the pack's load completion.)*

## Modding notes (SWE2-DATA, 2026-09-30)

- The shape comes from a byte in the record (`+9`, low seven bits), not from separate record formats. An authored
  volume can be switched between ellipse, box and segment chain by that byte alone. The fields each shape reads differ,
  though: `+0x20` centre, `+0x30`/`+0x34` radii or extents and `+0x50` angle for the first two; `+0x14` count and
  `+0x40` segments for the chain.
- A radius or extent at or below zero collapses the volume to its centre. That is a defined result, not an error.
- The functions share one global scratch block. A hook that calls them from another thread corrupts a caller that is
  mid-computation.

## Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| the three clamps and their record fields | the bodies, quoted above | 1 |
| `00363FD0`'s arguments, constants and second result | `mv_clamp_checks.py` A1–A3 | 1 |
| the second result is read by its one caller, which keeps the nearest segment | `mv_clamp_checks.py` A4, A7 (control C1: the sweep sees the body's own store) | 1 |
| the volume walk dispatches on record byte `+9` | `mv_clamp_checks.py` A8 | 1 |
| the outcode history's reader is `0025C830` | falsification table; `mv_clamp_checks.py` A6, C2 | 1 |

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Four edges, two carriers, and both are cited here as READERS rather than as subjects.**

**Party — one edge, and it is a five-byte thunk.** `0025C830` is named in §165 as the reader of the
shifted four-generation history; it also calls `PartyFocus_CommitPendingPackedActorHandle_Thunk`,
which is **five bytes** of forward. **A 3,118-byte reader committing a packed actor handle says
nothing about clamping a point into a volume**, and the party layer owns that thunk.

**Presentation — three edges, all inbound.** `00521450` is cited once here; three presentation
bodies call it — the heaviest is over twenty thousand bytes. **This page is the SERVICE at all
three**: it documents what the clamp does, and the presentation layer is one of the things that asks
for it.

**Neither layer is owned here.** The page's subject is the clamp arithmetic and who reads the
shifted global; what a reader does with the answer belongs to its own layer's pages — the same
reader-list shape recorded against `five-small-bin-tables.md`.

*No far end is named by address, and that was measured: naming the party thunk, or the heaviest of
the three presentation callers, would each import a CoreRuntimeScheduling edge this page does not
mention — two findings closed and a fifth opened. Symbols and roles carry the same information at no
cost.*
- **WorldAreaField - SERVICE (1 edge).** `0025C830` reaches bodies filed to WorldAreaField (world area): `00377C20` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Audio — CLIENT.** The volume tests are used by the sound-emitter code.

- The 512-byte Audio-filed body that carries the emitter records, with position at record `+0x20`, calls the clamp
  entries `00361DE0` and `003623C0`.
- A 388-byte Audio-filed body calls `00363FD0`.

So a sound emitter's volume uses the same point-into-volume clamp as movement. ~~What the audio side does with the
clamped point is not read.~~ *(Corrected 2026-09-30, SWE2-DATA: the selection half is read; see "Call chain" below.
The two bodies are listed with their addresses in `_index/candidates/dd-data-5-0930/mv_clamp_checks.py`. What the walk does with the clamped point after
the clamp is `SD-180`.)*
