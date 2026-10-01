---
contract: Place a sound in the world — five classes, one slot-34 postcondition, a radius that decides audibility
category: 18-Audio
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 18-Audio/the-spatial-audio-object-model.md
entries: ["007F1D10", "007F1F80", "007F1A50", "007F1340", "007F25E0", "007E5800", "007E57B0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the five RTTI-named vtables read **slot by slot from the image through a
    section-aware offset**, the base vtable read PAST its last slot as the control on where it ends,
    the two smallest slot-34 bodies disassembled in full, the three computing ones swept for every
    store to `+0xD0`/`+0xE0`/`+0xE4` **with the object's own base register identified first**, and
    both slot-39 stubs disassembled. **This records checks performed on that date, not the method of
    the original derivation**, which is on the spatial page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-spatial-sources-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — spatial source objects

> **Authored 2026-09-22 by FABLE.** S-41's binding gap is *"1 of 3 pages contracted"* — its one
> contract, [`Audio-Boundary/CONTRACT-sound-request.md`](Audio-Boundary/CONTRACT-sound-request.md),
> covers the request boundary. **This takes the spatial source objects**; the bank and controller
> family remains uncontracted and this document does not claim it.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants — and **SA-1, SA-3 and SA-6 are statements about five classes at once**, which is
> exactly what no single override's contract can say.

## 1. Purpose

Turn a sound source and a listener into a position and a yes-or-no about whether it can be heard.

## 2. Interface

Five RTTI-named 40-slot vtables. **Slot 34 is the spatial update**; every one of the five overrides
it, and the sizes span a factor of sixty-four:

| class | vtable | slot 34 | size | slot 39 |
|---|---|---|---:|---|
| `AmbientSound` | `01CB9C88` | `007F1D10` | **33 B** | `007E57B0` → false |
| `DirectionSound` | `01CB9DD0` | `007F1F80` | **35 B** | `007E57B0` → false |
| `PointSound` | `01CB9B40` | `007F1A50` | 497 B | `007E5800` → true |
| `DynamicSound` | `01CB99F0` | `007F1340` | 742 B | `007E5800` → true |
| `PolygonSound` | `01CB9F18` | `007F25E0` | **2,115 B** | `007E5800` → true |
| *base* `SoundObject` | `01CBAB68` | — | **ends at 34** (SA-5) | — |

## 3. Types

```
source object
  +0x0D0 .. +0x0DB   f32[3]  the effective position, computed per class
  +0x0DC             f32     w -- ALWAYS FORCED to 1.0, never inherited (SA-2)
  +0x0E0             u8      audibility: distance < radius. NOT a ready flag (SA-3)
  +0x0E4             f32     the radius, and the master gate; <= 0 disables the update
  +0x100             f32[4]  DirectionSound only -- the stored vector slot 34 copies
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**SA-1 — All five classes override slot 34, and all five satisfy ONE two-part postcondition despite
a 64× spread in size.** Every implementation writes the effective position at `+0xD0`–`+0xDC` and
writes the byte at `+0xE0`, and none of them writes anything else two classes do not. *That is the
contract of the slot: a reimplementation may compute the position however the shape demands, and
must leave exactly those two fields behind.*

**SA-2 — The `w` component is FORCED, and in one class that is a SECOND write of the same bytes.**
`AmbientSound` stores `+0xDC = 0x3F800000` explicitly (`007F1D12`). `DirectionSound` copies **all
sixteen bytes** from `+0x100` with a `movdqa` (`007F1F89`) and **then overwrites `+0xDC` with
`0x3F800000`** (`007F1F91`). *So whatever fourth component the stored direction vector carries never
reaches the output, and a port that copies the vector and stops has a `w` the original never
produces.*

**SA-3 — `+0xE0` is NOT a "ready" flag. It is a computed audibility boolean, and only the two
non-geometric classes write it unconditionally.**

| class | how `+0xE0` is written |
|---|---|
| `AmbientSound` | `mov byte ptr [rcx + 0xe0], 1` — always (`007F1D29`) |
| `DirectionSound` | `mov byte ptr [rcx + 0xe0], 1` — always (`007F1F9B`) |
| `PointSound` | from `comiss` against `+0xE4`, twice (`007F1A6E`/`007F1A7A`, `007F1C19`/`007F1C23`) |
| `DynamicSound` | four stores, the last from `comiss` against `+0xE4` (`007F15E4`/`007F15EE`) |
| `PolygonSound` | `setb al` after `sqrtps` vs `+0xE4` (`007F2DD2`–`007F2DEE`), and `0` on the early-out (`007F2DF9`) |

> **This corrects a correction box on the page, written by me.** The `CO-4`/`CO-6` box of 2026-09-14
> states *"Slot 34 writes the source's effective position … and sets the ready byte `+0xE0` = 1."*
> **That is true of two classes of the five**, and it contradicts the same page's own
> *"The early-out, in `PointSound::slot34`"* section, which already had `+0xE0` as
> *"listener-to-source distance `< +0xE4`"*. The page held both readings; the bytes hold one.

**SA-4 — Four classes are GIVEN the radius and exactly one computes its own.** Among the five slot-34
bodies, `+0xE4` is read by Point, Dynamic and Polygon and **written by only `DynamicSound`**
(`007F13EC movss dword ptr [rdi + 0xe4], xmm0`). *So for four classes the radius is an input to the
spatial update and for one it is an output of it, and treating it as input everywhere is wrong for
exactly one class.*

**SA-5 — The base interface ENDS at slot 34, established by reading PAST it.** `SoundObject`'s
vtable `01CBAB68` has slot 34 reading **`0`**, and the qwords after it are not code addresses at all.
*So slots 34–39 are the source-object interface and nothing above it exists to inherit — measured by
running off the end rather than by counting entries.*

**SA-6 — Slot 39 is a queryable form of the property slot 34 exercises, and it is two SHARED 3-byte
stubs.** `007E5800` is `mov al, 1; ret` and `007E57B0` is `xor al, al; ret`. **The three classes
returning true — Point, Dynamic, Polygon — are exactly the three whose slot 34 computes against the
listener and tests a radius (SA-3); the two returning false are exactly the two that do not.** *The
partition is not a coincidence of authoring: slot 39 lets a caller ask, without invoking slot 34,
which of the two behaviours it will get.* The same two stubs serve slot 36 for Ambient and
Direction, so neither stub belongs to this interface alone.

**SA-7 — Every SIMD square root in the executable is in this cluster, and the support for that is
five callers, not twelve.** All twelve `sqrtps`/`rsqrtps` functions are Audio-owned and lie in
`007EF1E0`–`007F74E0`; the caller census was **corrected from twelve edges to nine callers to five
from outside the cluster**, because four of the nine were themselves members — *the cluster vouching
for itself.* Taken from [the page](the-spatial-audio-object-model.md) and not re-derived; recorded
here because a contract that cited the twelve would be repeating a withdrawn figure.

## 5. State

**Owned:** each source object's `+0xD0`–`+0xE0`. **Read, never written here:** the listener, and
`+0xE4` for four of the five classes (SA-4). **Written outside the postcondition:** `+0xE4`, by
`DynamicSound` alone.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`Audio-Boundary/CONTRACT-sound-request.md`](Audio-Boundary/CONTRACT-sound-request.md) — S-41's contracted third |
| **Uncontracted** | [the bank and controller family](Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) — S-41's remaining page, not claimed here |
| **Consumes** | the listener, moved by `Lay` actions rather than by a per-frame poll — [the page](the-spatial-audio-object-model.md) §2 |

## 7. State transitions

Per update, per source: *gate on `+0xE4` → compute the position for this class's shape → store it
with `w` = 1 → store audibility.* No transition belongs to the object; slot 34 is idempotent given a
fixed listener.

## 8. Script · resource · event interactions

The radius and, for `DirectionSound`, the stored vector at `+0x100` are authored per source. Nothing
here is scripted.

## 9. Determinism

Deterministic. No generator is drawn anywhere in this cluster.

## 10. Failure paths and edge conditions

- A non-positive `+0xE4` disables the spatial update and clears `+0xE0` — established for
  `PointSound` on [the page](the-spatial-audio-object-model.md) §2.
- `PolygonSound` returns `-1` on its early-out after writing `+0xE0 = 0` (`007F2DF9`/`007F2E00`) and
  `0` on the computed path (`007F2DF5`).
- `AmbientSound` cannot fail: it writes `(0, 0, 0, 1)` and audible, with no test at all.

## 11. Observable behaviour

A river is audible the moment you are near enough to its bank rather than its centre, and ambience
has no direction at all — the amount of maths each sound costs tracks the shape it models.

## 12. Reproduction formula

Read all five vtables' slot 34 and assert the five sizes `33 / 35 / 497 / 742 / 2115` (SA-1). Give
`DirectionSound` a `+0x100` whose fourth component is not 1.0 and assert the output's is (SA-2).
Place a Point source beyond `+0xE4` and assert `+0xE0` is **0**, then do the same to an Ambient
source and assert it is **1** (SA-3). Read `01CBAB68` slot 34 and assert it is zero (SA-5). Assert
slot 39 and the radius test of slot 34 agree for all five (SA-6).

## 13. Runtime validation

**None.** No experiment executes these bodies. S-41's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*

## 14. Unresolved

- What `DynamicSound` computes its radius **from** (SA-4).
- Whether `+0xE0` is consumed as a cull or only as a mix weight; this contract establishes what
  writes it, not what reads it.
- The bank and controller family, S-41's other uncontracted page.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| SA-1, and the five sizes | the five RTTI-named vtables read slot by slot from the image, each slot's target resolved against the function table | 1 |
| SA-2 — the forced `w` | `007F1D12`, and `007F1F89` against `007F1F91` — the `movdqa` and the store that overwrites part of it, read in order | 1 |
| SA-3 — audibility, not readiness | every store to `+0xE0` in all five bodies, **with the object's base register identified first** so that `[rsp + 0xe0]` is not counted — the trap that hid `PolygonSound`'s store on the first pass | 1 |
| SA-4 — one writer of `+0xE4` | all five bodies swept for a store to `+0xE4`; exactly one hit | 1 |
| SA-5 — the base ends at 34 | `01CBAB68` read **past** its last slot: slot 34 is `0` and the following qwords are not code addresses | 1 |
| SA-6 — the stubs and the partition | `007E5800` and `007E57B0` disassembled in full (3 B each); slot 39 of all five read against slot 34's radius test | 1 |
| SA-7 — the SIMD cluster and its five supports | [the page](the-spatial-audio-object-model.md) §2, whose census was corrected 2026-09-07 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on SA-1 through SA-6. **SA-3 is the one to get right
first**: `+0xE0` reads like an initialisation flag and is a distance test, so a port that sets it to
1 whenever slot 34 runs makes every source audible at every range — and matches the original exactly
for the two classes anyone would test first.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Audio — internal.** All five classes, both stubs and the whole SIMD cluster are this category's
  own; SA-7 is the statement that nothing outside it calls in.
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [The spatial audio object model](the-spatial-audio-object-model.md) — the mechanism
- [Contract — the sound request](Audio-Boundary/CONTRACT-sound-request.md) — S-41's contracted third
- [Audio bank and controller family](Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) — S-41's remaining page

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** §2's vtables, slots and sizes, SA-1 to SA-7 and §10 became checks. The vtable slots were read from `.rdata`,
each slot-34 size was checked against its `.pdata` chain union, and SA-7's square-root census is image-wide. Script:
`Tools/analysis-kit/gfz-scripts/falsify_spatial_sources.py`, output `falsify_spatial_sources.out`, image `73461d08…`,
0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| P0 | §2 | **survives**: each vtable's slot 34 and slot 39 are the cited body and stub; 33 / 35 / 497 / 742 / 2,115 B, none short of its unwind chain |
| P1 | SA-1 | **survives**: all five store the position at `+0xD0`..`+0xDC` and write `+0xE0` |
| P2 | SA-2 | **survives**: Ambient stores `w = 1.0`; Direction loads `+0x100` (`movaps`, `007F1F80`), stores 16 bytes (`movdqa`, `007F1F89`), then overwrites `+0xDC` |
| P3 | SA-3 | **survives**: `+0xE0 = 1` unconditionally in Ambient and Direction; the three geometric classes compare against `+0xE4`, with store sites exactly as tabulated |
| P4 | SA-4 | **survives**: `+0xE4` is written only by DynamicSound, at `007F13EC` |
| P5 | SA-5 | **survives**: SoundObject's slot 34 is 0 |
| P6 | SA-6 | **survives**: the two 3-byte stubs; slot 36 of Ambient and Direction is the false stub |
| P7 | SA-7 | **survives**: exactly 12 functions contain `sqrtps`/`rsqrtps`, all in `007EF1E0`–`007F74E0` |
| P8 | §10 | **survives**: Polygon stores `+0xE0 = 0` and returns `-1` on the early-out, and 0 on the computed path |

No correction.
