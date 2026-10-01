---
contract: Push overlapping bodies apart once per world tick — registration, pairing, resolution, consumption
category: 06-Movement-And-Navigation
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: the-movement-body-pool-and-the-separation-pass.md
entries: ["003DAA40", "003DAC70", "003DAAB0", "003DAB50", "00314F50", "003DA9F0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the six bodies' extents, the resolver's refusal chain read in order from its
    first instruction, its mode argument traced to both call sites, and the accumulator read/write
    sites swept. **This records checks performed on that date, not the method of the original
    derivation**, which is on the pool page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-separation-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the separation pass

> **Authored 2026-09-21 by FABLE.** S-19's binding gap is *"the pool is contracted, the separation
> pass is not"*. [`CONTRACT-movement-body-pool.md`](CONTRACT-movement-body-pool.md) is `scope: family`
> over taking a body from a pool of 128. **What the bodies then do to each other had no contract.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants, and five of them are about the order things happen in — which is the whole
> difficulty of a separation pass.

## 1. Purpose

Once per world tick, find every pair of collision bodies that overlap and accumulate a push on each
so they stop overlapping. The pass moves nothing itself: it fills per-body accumulators that the
movement step spends on its next candidate position.

## 2. Interface

| | body | size | role |
|---|---|---:|---|
| reset | `003DAA40` | 108 B | zero the 32 cell masks, clear every body's `+7` |
| walk | `003DAC70` | 131 B | iterate the active list, calling the pair callback |
| pair set | `003DAAB0` | 155 B | build the candidate bitmap at `02B57EE0` |
| visit | `003DAB50` | 283 B | call the callback per candidate and per remembered pair |
| **resolve** | `00314F50` | **1,080 B** | refuse or contact, and split the push |
| clear | `003DA9F0` | 35 B | zero one body's accumulators |

`00314F50(A, B, mode, out)` — **`mode` is load-bearing**, see P-4.

## 3. Types

```
CollisionBody
  +0x06   u8     layer
  +0x07   u8     active this tick          (set by registration, cleared by the reset)
  +0x08   ?      weight
  +0x18   u128   remembered pair bitmap
  +0xE8   f32    squared push length
  +0xEC   u8     "a push is pending"
  +0xED   u8     contact count
  +0xEE   u8     immovable-contact marker
  +0xF0   f32    radius A         +0xF4  f32  radius B
  +0xFC   ?      margins
  +0x100  f32    accumulated push x     +0x104  f32  (third component)     +0x108  f32  push z
  +0x110 / +0x114  weight masks
  +0x119  u8     owner
  +0x120  u128   the cells this body registered in
```

Shared: 32 cell masks of 16 bytes at `02B57CE0`; the candidate scratch at `02B57EE0`.

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**P-1 — The reset runs first, and it is what makes `+0x07` mean anything.** `003DAA40` is called at
the head of the world tick: it zeroes the 32 cell masks and clears every body's `+7`. Registration
happens per *frame* (`003DB020`, which sets `+7` and ORs the body's bit into each cell it touches);
the pass runs per *tick*. **A body that did not register during the frame is not active for the
pass** — the coupling between the two rates is this one byte, and it is cleared before the pass, not
after.

**P-2 — Each unordered pair is visited at most once.** `003DAAB0` ORs the masks of the body's cells,
then clears the body's own bit **and every lower index**. Without that second clear, every pair would
resolve twice per tick with each body taking the other's share.

**P-3 — The pair bitmap is hysteresis, not a cache.** ~~`003DAB50` walks the candidate bits **and every
bit still set in the body's own `+0x18`**~~; it clears the bit, calls the callback, and **sets it again
only if the callback returns non-zero**. ~~*So a contact is retried next tick even after the two bodies
stop sharing a cell*, and it is forgotten the first tick the resolver refuses it.~~ *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 337](../_index/candidates/s19-opus-replay-separation-pass/README.md) and [the index probe](../_index/candidates/s19-fable-visit-index-probe/README.md), which executes the shipped walk; `003DAB50` re-read.)*
**What the walk actually visits.** `003DAB50` walks the **candidate** set a byte at a time (`003DAB94`–`003DAC48`).
It skips a zero qword (`003DAB9A`) and a zero byte (`003DABA7`). Inside a non-zero byte it steps only while
candidate bits remain (`shr rbp, 1` / `jne`, `003DAC0E`–`003DAC11`). At each step it calls the resolver where the
position is a candidate **or** its remembered bit is set (`003DABCF`–`003DABDD`). So a remembered bit is visited
only below the highest candidate of a non-zero byte. OPUS measured all three cases: with no candidate, a remembered
pair is neither retried nor forgotten. Below a candidate in the same byte, it is retried and dropped. Above the
highest candidate, it is never visited and persists.
**And the two indices drift apart** (executed). The body pointer advances eight bodies per candidate byte, zero
bytes included, but not past a qword's trailing zero bytes or an all-zero qword. The remembered-bit index `r14d`
advances once per step, so a zero byte and a byte's zeros above its highest candidate do not advance it. On the
shipped bytes:
- candidate 9 alone is resolved against body 9, but its bit is set at index **1**;
- candidate 64 alone is resolved against body **0**;
- with candidate 2 present, candidate 64 is resolved against body **8**.

The byte-0 control maps exactly. `003DAAB0` clears every candidate bit at or below the visiting body's own index,
so for any visiting body at index 8 or above, byte 0 is empty and the remembered bitmap is written at the wrong
indices. *The resolver re-tests whatever pair it is handed (P-4), so a mis-indexed call pushes only if that body
really overlaps. How many bodies are registered in normal play, and so how often this happens live, is not
established.* A port that indexes both by body reproduces the intended design, not the shipped behaviour.
**Body indices are handed out in ascending order per area** (read here, not executed). The area initialiser
re-threads the pool at `00267141`. The thread routine links entry `i` to `i - 1` and `i + 1` for `i = 0..127` and
sets the free head to 0 (`003DAE3A`–`003DAE9D`). The allocator pops the free head and advances it to the popped
entry's `+2` link (`003DA8A6`–`003DA903`). Until the first release, the n-th body allocated in an area is
therefore index `n - 1`, and **the ninth is index 8**, the first whose remembered bits land at the wrong index.
*How many bodies an area allocates in play is the live question that remains.* *(Added 2026-09-25, FABLE, Claude Opus 5.5.)*

**P-4 — The third argument selects push mode, and in query mode two of the refusals do not apply.**
The resolver's refusal chain, read from its first instruction:

| order | refusal | site |
|---|---|---|
| 1 | `A` is null | `00314F78` |
| 2 | A's `+0xF0` **and** `+0xF4` not both positive | `00314F97`, `00314FA0` |
| 3 | B's likewise | `00314FB0`, `00314FC5` |
| — | **`test esi, esi` / `je 00314FEA` — with `mode == 0` the next test is skipped entirely** | **`00314FD2`** |
| 4 | either body not active this tick | `00314FD6`, `00314FE0` |
| 5 | layer bytes `+6` differ | `00314FEA`–`00314FF1` |
| 6 | **A's owner byte `+0x119` is non-zero AND equal to B's** | `00314FF7`–`00315008` |

*(Made exact 2026-09-29, pass 1: in push mode a seventh refusal follows - vertical spans from `+0xE4`/`+0xE0` that do not
overlap (`003150CA`, `003150DB`). Query mode skips it, together with every body write.)*

Both modes exist in the image: `00314F30`, the separation pass's own callback, passes **1**
(`00314F39`); `00313F80` passes **0** (`00313FB4`). *A query may therefore ask about a body that did
not register this tick; a push may not.* **[The pool page](the-movement-body-pool-and-the-separation-pass.md)
§2.7 lists "both are active this tick" in a flat list of refusals; it is conditional on the mode, and
that distinction is the difference between the two callers.**

**P-5 — The pass is ORDER-DEPENDENT, and the dependence is in the resolver's own reads.** Before
testing separation it adds each body's *accumulated* push into the position it tests —
`003150F8` / `00315100` for A and `0031512A` / `0031513E` for B — and on contact it writes the
updated accumulators back at `0031532B` / `00315333` and `00315360` / `00315369`. **Read-then-write
on the same cells inside one pass: a pair resolved later in the tick sees the pushes from pairs
resolved earlier.** *A reimplementation that gathers all contacts and then applies them will produce
different positions from the same inputs.* This is the single most important thing in this contract
and the pool page states it only in passing.

**P-6 — A push is accumulated by one subsystem and consumed exactly once by another.** The resolver
sets `+0xEC` and accumulates into `+0x100` / `+0x108`. `002E5180` sees `+0xEC` and re-runs the
integrator; `Movement_PrepareCandidatePosition` (`002E5380`) adds the accumulators into the candidate
delta; `003DA9F0` then zeroes `+0x100`, `+0x104`, `+0x108`, `+0xE8`, `+0xEC`, `+0xED` and `+0xEE`
together. **A push moves the actor on its next candidate position and is gone the tick after.** When
`+0xEC` is clear, `002E5180` clears them directly. *The accumulator's lifetime spans two subsystems
and neither one's own contract can state it.*

**P-7 — The weight split has three outcomes, and each advances a different set of counters.**
`00314E10` returns A's share `w` from the two weights `+8` and the masks `+0x110` / `+0x114`, and the
resolver compares it against 0 and against 1:

| `w` | meaning | counters | return |
|---|---|---|---|
| **0** | A takes none of the separation | `inc [rdi + 0xED]` and `mov [rdi + 0xEE], 1` — **one** body's, at `0031525D` | 3 |
| **1** | A takes all of it | `inc [rbx + 0xED]` and `mov [rbx + 0xEE], 1` — **one** body's, at `00315281` | 4 |
| otherwise | shared | **both** `+0xED` advance and **both** `+0xEE` are cleared, `00315298`–`003152AB` | 1 |

A receives `w × separation` and B `(1 − w) × separation`.

> **Corrected 2026-09-22 (FABLE) on SWE2-AUDIT-SEM's return (rev 27568).** This invariant said the
> immovable case advances **no** counters — *"the counters do not advance"* — and that both `+0xEE`
> are set on "the moving one". **Each immovable case advances exactly one `+0xED` and sets that same
> body's `+0xEE`.** I read the two `jmp 003152B2` exits as skipping the counter block when they skip
> only *each other*. *The tell I had and did not use: each arm sets `eax` to a distinct return value —
> 3 and 4 — which is the function telling the caller the two cases are different, and I had already
> written "2, 3 or 4" into §10 without asking what distinguishes them.*

## 5. State

**Owned by the pass:** the 32 cell masks, the candidate scratch, and each body's `+0x07`, `+0xE8`,
`+0xEC`, `+0xED`, `+0xEE`, `+0x100`–`+0x108` and `+0x18`. **Read, never written:** radii, margins,
layer, owner, weights and weight masks, and the positions (through `003DAE00`). **Written by others,
read here:** `+0x120`, the body's cell bits, written by registration each frame.

## 6. Relationships

| | |
|---|---|
| **Upstream** | registration during the frame (`003DB020`), which is what P-1 depends on |
| **Sibling** | [`CONTRACT-movement-body-pool.md`](CONTRACT-movement-body-pool.md) — where a body comes from |
| **Downstream** | the movement step, which consumes the accumulators (P-6) |

## 7. State transitions

Per tick: *reset → for each active body: build candidates → for each candidate or remembered pair:
resolve → accumulate*. Per frame afterwards: *consume → clear*. A pair goes
`unknown → contact → remembered` and back to `forgotten` on the first refusal.

## 8. Script · resource · event interactions

None. Nothing authored reaches this pass; its inputs are the bodies' own fields and the navimap cells
the registration step derives.

## 9. Determinism

Deterministic **given the order of the active list** — which P-5 makes observable. No generator is
drawn.

## 10. Failure paths and edge conditions

- A body with a non-positive radius is refused before anything else is read.
- Two bodies on different layers never contact, and neither do two with the **same non-zero owner**.
  **A body whose owner byte is zero is exempt from the owner test entirely** (`00314FFE` / `00315000`
  skip the comparison), so an unowned body can contact anything — *the opposite of what this contract
  said before 2026-09-22.*
- Vertical extents that do not overlap refuse the pair after the cheap tests.
- A pair whose separation is not negative returns without a push; the remembered bit is dropped.
- The resolver returns 1 for a contact, 2, 3 or 4 when the callback ran without a mutual push, and
  writes the raw separation to `out` when the caller asked for no push.

## 11. Observable behaviour

Characters and foes crowding a doorway slide apart instead of interpenetrating, one frame late; a
heavy body pushes a light one further; and a body that stops registering — because it left the
world, or its owner cleared the registration gate — stops participating on the very next tick.

## 12. Reproduction formula

Place two bodies overlapping, run the reset, register both, run the walk, and assert both `+0x100`
sets are non-zero, `+0xEC` set on both, and `+0xED` advanced on both. Then resolve a third pair in the
same tick and assert its test position already includes the first pair's push (P-5). Call `00314F50`
with `mode = 0` against a body whose `+7` is clear and assert it is **not** refused (P-4).

## 13. Runtime validation

~~**None.** No experiment executes these six bodies. S-19's runtime cell is not addressed by this
contract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*~~ **Superseded 2026-09-25.** [OPUS block 337](../_index/candidates/s19-opus-replay-separation-pass/README.md) executed the six bodies as shipped code, and [the index probe](../_index/candidates/s19-fable-visit-index-probe/README.md)
executes the visit walk's index mapping. The evidence class is native replay, not live.

## 14. Unresolved

- What `00313F80`, the query-mode caller, uses the raw separation for.
- The units and meaning of the weight masks `+0x110` / `+0x114`.
- Whether the active list's order is stable across ticks — P-5 makes this matter, and it is not
  established here.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| P-4 — the mode argument and the two call sites | the resolver's opening read in order from its first instruction; `test esi, esi` / `je` at `00314FD2`; `r8d` traced at both call sites (`00314F39` sets 1, `00313FB4` zeroes it) | 1 |
| P-4's refusal chain | each test read at its address, in the order the body executes them | 1 |
| P-5 — order dependence | the accumulator displacements swept across the resolver: read at `003150F8`/`00315100`/`0031512A`/`0031513E`, written at `0031532B`/`00315333`/`00315360`/`00315369` | 1 |
| P-7's three outcomes | `0031523C`–`003152AB` read in full, including the two `ucomiss` against 0 and 1 and the distinct `eax` values 3 and 4 | 1 |
| Refusal 6's exemption | `00314FFE` `test al, al` / `00315000` `je 0031500E` **before** the comparison | 1 |
| The six bodies' extents | the function table of the authority image | 1 |
| P-1, P-2, P-3, P-6 | [the pool page](the-movement-body-pool-and-the-separation-pass.md) §2.5–§2.8, read from the shipping bytes and falsified once 2026-09-13 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on P-1 through P-7. **P-5 is the one to test first**:
gather-then-apply is the natural implementation and it is the wrong one.

## 16a. Crossings into other layers (FABLE, 2026-09-21)

- **Movement — internal.** Five of the six bodies are this category's own.
- **CoreRuntimeScheduling — SERVICE.** The world tick calls the reset and the walk; that ordering is
  P-1 and is stated in §4.
- **Party and Presentation — MECHANICAL.** Both are reached only through `002E5180`, the consumer
  named in P-6: it calls into them when it re-runs the integrator and refreshes presentation state.
  That is downstream of this contract's boundary — the pass fills accumulators and asserts nothing
  about what the consumer then does with the actor.
- **Every other layer reached is MECHANICAL** in the same way, through the resolver's and the
  consumer's own callees and their fan-in. *Those addresses are deliberately not cited: each is a
  hub, and naming one imports its whole edge set for a one-line remark.*

## 17. Related

- [The movement body pool and the separation pass](the-movement-body-pool-and-the-separation-pass.md) — the mechanism
- [Contract — the movement body pool](CONTRACT-movement-body-pool.md) — S-19's other half
- [The world tick and the field frame](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) — where the pass is called

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - SERVICE (1 edge).** `002E5180` reaches bodies filed to ActorEntity: `00264010` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (1 edge).** `002E5180` reaches bodies filed to party: `003590D0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - SERVICE (2 edges).** `002E5180` reaches bodies filed to presentation: `002E8000` (CharacterRenderQuerySupport), `00420A10` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (2 edges).** `002E5180` is also called by bodies filed to World: `0025E400` (ActorManager), `002623A0` (ActorManager) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT (2 edges).** `003DAA40`, `003DAC70` are also called by bodies filed to WorldAreaField (world area): `00314020` - shared machinery across the layer boundary, no shared ownership.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives; query mode is write-free, and push mode has a seventh refusal

**Attack.** Every clause of §2-§5 became a check that fails if the shipping image says otherwise. Script:
`Tools/analysis-kit/gfz-scripts/falsify_separation.py`, output `falsify_separation.out`, image `73461d08…`, 0 BROKEN. The
behavioural results are OPUS block 337's executed replay and FABLE's index probe, and are not re-run.

| # | Clause attacked | Result |
|---|---|---|
| S0 | §2 sizes | **survives**: 108 / 131 / 155 / 283 / 1,080 / 35 |
| S1 | P-1 | **survives**: 512 bytes (32 × 16) cleared at `02B57CE0`; `+7` cleared on 128 bodies of `0x130` |
| S2 | P-2 | **survives**: the cell masks are ORed into `02B57EE0`, then the own bit and every lower bit are cleared |
| S3 | P-4's six refusals and the two modes | **survives** at every cited site; `00314F30` passes 1, `00313F80` passes 0 |
| S4 | P-4 / P-5's scope | **made exact** (below) |
| S5 | P-6's clear | **survives**: seven fields in five stores |
| S6 | P-7's three outcomes | **survives, made exact**: 3 / 4 / 1 with the stated counters, each behind `test esi, esi / je 00315377` |
| S7 | §5 "read, never written" | **survives**: the resolver and the split write only `+0xE8`, `+0xEC`-`+0xEE`, `+0x100` and `+0x108` |

* **Query mode writes no body state.** A second mode test (`00315084`, `je 00315220`) sends query mode past the whole push
  geometry. Every body write in the resolver sits behind a mode test that sends query mode to `00315377`, which stores only
  the out-parameter `[r15]`, A's share. So P-5's read-then-write order dependence and P-7's counters are **push-mode
  facts**. A query computes the same outcome codes without disturbing either body.
* **Push mode has a seventh refusal.** Before it adds the accumulators, push mode reads both positions (`003DAE00`) and
  refuses a pair whose vertical spans `[y + height_offset, y + height_offset + height]` do not overlap. The fields are
  `+0xE4` (base offset) and `+0xE0` (height), tested at `003150CA` and `003150DB`. P-4's table stops at six. [The pool
  page](the-movement-body-pool-and-the-separation-pass.md) documents both fields ("overlap vertically"). §3 did not list them.

No correction row: nothing the contract asserted was false.
