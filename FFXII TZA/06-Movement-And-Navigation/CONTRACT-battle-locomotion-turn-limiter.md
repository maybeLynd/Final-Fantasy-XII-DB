---
contract: Limit a battle actor's turn through one hysteresis loop whose three angles are a single mechanism
category: 06-Movement-And-Navigation
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: 06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md
entries: ["003364D0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants **re-measured at
    the instructions rather than carried** — all three angular constants read from the operands they
    are compared against, the latch's second condition read at its mask and compare, the release read
    at its `and`, and the direction pair read at its four bit operations. **This records checks
    performed on that date, not the method of the original derivation**, which is on the battle
    locomotion page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-turn-limiter-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the battle locomotion turn limiter

> **Authored 2026-09-22 by FABLE.** S-18's contract column carried two contracts over three pages.
> **This takes the third, so all three of S-18's pages now carry one.**
>
> Written against FRONTIER's adequacy test. **`BL-4` is why no single threshold can be contracted
> separately:** the middle band's behaviour is defined by what the *other two* bands last did, so
> the three angles are one state machine and not three comparisons.

## 1. Purpose

Stop a battle actor from turning instantly, and decide how fast it may turn.

## 2. Interface

`BattleLocomotion_ApplyHeadingTurnLimiter` (`003364D0`), **564 B**, `(ctx, float desired) → float`.

## 3. Types

```
ctx +0x108 -> motion state          ctx +0x100 -> flag block
  st +0xE0   f32  current heading     fl +0x38  bit 3  "turning"      (BL-1)
  st +0xEC   f32  SLOW turn rate      fl +0x3C  bit 0  FAST latched   (BL-3)
  st +0xF0   f32  FAST turn rate      fl +0x21  bits 1,2  last turn direction (BL-5)
  st +0x170  u32  locomotion flags -- the latch's second condition
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**BL-1 — The three angles are ONE mechanism, and each does a different job.** Read at the operands
they compare against:

| constant | value | what it does |
|---|---|---|
| `00336519` | `0.785398` = **45°** | **raises** the turning flag `fl[0x38] |= 8` |
| `0033654E` | `2.0944` = **120°** | gates the **latch** of the fast rate |
| `00336625` | `0.349066` = **20°** | **releases** the latch and forces the slow rate |

*They are not three thresholds on one quantity; they are the entry, the escalation and the release
of a loop.*

**BL-2 — Entry and exit are NOT the same angle, which is what makes it hysteresis.** Turning begins
when the error exceeds **45°**, and once `fl[0x38]` bit 3 is set the body no longer consults that
angle — it turns until it **arrives**. *So an actor 40° off heading does not turn at all, while an
actor that was 50° off and has closed to 40° is still turning.* **The same error produces different
behaviour depending on history**, and `0033652A test r9b, 8` is the instruction that makes it so:
if the flag is clear, the heading is returned unchanged.

**BL-3 — The FAST rate needs a SECOND condition, so a large angle alone does not grant it.**
`00336572`–`0033657A`: `and ecx, 0x1C` then `cmp cl, 0x1C` — **three specific bits of the
locomotion flags must all be set** — before `fl[0x3C] |= 1` latches. *A port that selects the rate
from the angle alone turns fast in cases the original turns slow.*

**BL-4 — The middle band KEEPS whatever is latched, and that is the cross-operation invariant.**
Above 120° the latch may be set; below 20° it is cleared (`00336645 and dword [rdx+0x3c],
0xFFFFFFFE`); **between them the body only reads it** (`0033657E test byte [rdx+0x3c], 1`).
*So at 60° the actor turns fast or slow depending on whether it passed through 120° on the way —
the rate is a function of the path, not of the angle.* **No single-threshold contract can state
this**, because the band that decides is not the band being executed.

**BL-5 — The turn direction is a MUTUALLY EXCLUSIVE bit pair, written as clear-then-set.**
`003366CD`–`003366DB`: one arm does `and 0xFB` / `or 2`, the other `and 0xFD` / `or 4`. *Each write
clears its opposite, so the pair can never both be set — a reimplementation using two independent
booleans admits a state the original cannot reach.*

**BL-6 — Arrival SNAPS, and the snap is what clears the loop.** When ~~the remaining delta is within~~ the step is not a latched one (a latched direction is read only above 120°) and the remaining delta is within *(corrected 2026-10-02, OPUS: `0033654E` / `0033655F` split at 120°; above it `0033659D` reads `fl[0x21] & 6` and `003365FF`–`0033661D` step `cur ± rate` with no wrap and no snap, the 2026-09-23 closure below)*
the rate the result is exactly `desired` rather than an overshoot, and reaching `desired` clears
both `fl[0x38]` bit 3 and `fl[0x3C]` bit 0. *So the loop is self-terminating and cannot oscillate
around the target — and a port that steps by the rate unconditionally will orbit it.*

## 5. State

**Read:** the current heading, both rates, and the locomotion flags *(and, made exact 2026-09-29 in pass 1, the flag block's
`+0x38`, `+0x3C` and the direction pair `+0x21`, which above 120° chooses the step's direction)*. **Written:** the turning flag,
the latch and the direction pair — all in the caller's flag block. *This body owns nothing.*

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-facing-and-steering.md`](CONTRACT-facing-and-steering.md) — S-18's first |
| **Sibling** | [`CONTRACT-heading-speed-to-position-delta.md`](CONTRACT-heading-speed-to-position-delta.md) — S-18's second; the heading this body limits is what that one decomposes |
| **Called from** | the battle navigation step, through the solver family |

## 7. State transitions

*not turning → error > 45° → turning.* *turning, error > 120° and the three flags set → fast
latched.* *turning, error < 20° → latch released, slow.* *turning, arrived → snap, both flags
cleared, not turning.* **The 20°–120° band changes nothing**; it executes whatever the last
transition left (`BL-4`).

## 8. Script · resource · event interactions

None directly. The desired heading arrives from the step solver.

## 9. Determinism

Deterministic. No generator is drawn in this body. *The avoidance and detour machinery on the same
page does draw one; that is not this contract's subject.*

## 10. Failure paths and edge conditions

- Below 45° with the flag clear, the heading is returned **unchanged** (`BL-2`).
- A 120°+ error without the three locomotion bits turns at the **slow** rate (`BL-3`).
- The same mid-band angle can turn at either rate (`BL-4`).

## 11. Observable behaviour

Why a character in battle pivots smoothly instead of snapping to face a new target, and why a
sharp reversal turns visibly faster than a gentle correction of the same remaining angle.

## 12. Reproduction formula

Drive the error to 40° from below and assert **no turn**; reach 50° then close to 40° and assert it
**still turns** (`BL-2`). Set a 130° error with the three locomotion bits clear and assert the
**slow** rate (`BL-3`). Pass through 120° then evaluate at 60° and assert **fast**; approach 60°
from 30° and assert **slow** (`BL-4`). Assert `fl[0x21]` bits 1 and 2 are never both set (`BL-5`).
Place the error inside one rate step and assert the result equals `desired` exactly and both flags
clear (`BL-6`).

## 13. Runtime validation

**None.** No experiment executes this body. S-18's runtime cell is not addressed by this contract —
*its gap is separately recorded as 92 bodies executed across `EXP-132`–`137` whose records name no
contract, which is a different half of S-18 and is not claimed here.*

## 14. Unresolved

- [x] ~~What the three locomotion-flag bits of `BL-3` mean individually.~~ **CLOSED 2026-09-23
      (SWE2-CONTRACT) by reference, re-verified.** The sibling page's AM-8 (FABLE 2026-09-12)
      resolves it: `st[0x170]` is the unit's **`locomotionFlags` `+0x1F0`** ([the battle-unit
      field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)) and `0x1C` is its
      bits **2 | 3 | 4** — bit 2 = the model's `@FCP` section-9 **slot-41 dword non-zero**
      (`00239F73`, authored per model, non-zero in 360 of 723 files), bit 3 = **unit flag bit
      23** (`00325CC9`), bit 4 = **executing a non-Attack action** — `+0x714 ≤ 0x21E` and
      `≠ 0x96` (`00325CF4`). Bits 3 and 4 re-verified at the instructions: `bt rax,0x17` →
      `or [rbx+0x170],8`; `+0x714` word `≤ 0x21E` `∧ ≠ 0x96` → `or [rbx+0x170],0x10` — both
      recomputed every `BattleUnit_UpdateCombatNavigationStep`. Why all three: the fast rate
      latches only for a unit whose model authors slot 41, whose flag 23 is up, and which is
      mid-execution of something other than Attack — a deliberate intersection, not a mask of
      convenience.
- [x] ~~Whether any caller depends on the direction pair in `BL-5` rather than merely
      maintaining it.~~ **CLOSED 2026-09-23 (SWE2-CONTRACT): the limiter itself depends on it —
      it is a committed-direction latch, not a write-only record.** `0033659D` reads `fl+0x21`,
      masks it to `6`, and when either bit is set jumps to `003365FF`, which selects
      `current + rate` when the pair is `2` and `current − rate` when it is `4` — **stepping in
      the latched direction without recomputing the wrap delta or the arrival snap**. Only when
      the pair is clear does the body fall through to `desired − current` (`0033CB70`
      normalised, `andps` abs). So the pair is written at the end of one invocation
      (`003366CD`/`003366D7`) and consumed at the head of the next — the turn direction is
      sticky across frames, a second hysteresis alongside BL-4's rate latch. **No outside
      reader exists**: the only other `+0x21` accesses on solver-family records are bit 0 — a
      different flag (`0033C13E`/`0033C1CA` in `0033BFB0`, `0033E278` in `0033E1F0`) — and
      `00334204`'s `test [rax+0x21],2` sits on the `.ard` slot-0 class row (`[unit+0xE68]`),
      a different record entirely (verified at `003341FD`–`00334204`).

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `BL-1` — the three constants | each read from the operand it is compared against: `0.785398`, `2.0944`, `0.349066` | 1 |
| `BL-2` — the entry flag and the early return | `00336522` for the raise and `0033652A test r9b, 8` for the unchanged-heading exit | 1 |
| `BL-3` — the second condition | `00336572`/`00336575` read as a three-bit mask and equality before the latch at `0033657A` | 1 |
| `BL-4` — the band that only reads | the release at `00336645` and the read at `0033657E`, with no write between the two angle tests | 1 |
| `BL-5` — the exclusive pair | all four bit operations at `003366CD`–`003366DB` | 1 |
| the pair is *consumed*, by the limiter itself: `0033659D` masks `fl+0x21` to 6 → `003365FF` selects `+rate` (pair 2) / `−rate` (pair 4) skipping the wrap delta; no outside reader (the `00334204` `+0x21` is on the `[+0xE68]` class row) | `0033659D`–`00336620` and `003341FD`–`00334208` decoded; image-wide `+0x21` byte-access census, 2026-09-23 | 1 |
| `BL-3`'s three bits are `locomotionFlags+0x1F0` bits 2/3/4 (FCP slot-41 authored; unit flag 23; non-Attack action `+0x714 ≤ 0x21E ≠ 0x96`) | sibling page AM-8 (FABLE 2026-09-12); bits 3/4 re-verified at `00325CC0`–`00325CF4` | 1 |
| `BL-6` and the decoded body | [the battle locomotion page](Battle-Locomotion/battle-locomotion-steering-and-recovery.md) §9, falsified 2026-09-02 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `BL-1` through `BL-6`. **`BL-4` is the one a
port cannot arrive at by reading one branch** — the mid-band rate depends on the path taken, and a
port written threshold-by-threshold will choose a rate from the angle. **`BL-2` is the one that
looks like a bug**: an actor that keeps turning below its start threshold reads as sticky until the
hysteresis is seen. **`BL-6` is the one that produces visible oscillation** when dropped.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Movement — internal.** The limiter, the rates and the flag block are this category's own.
- **CombatAction — CLIENT.** The battle navigation step that reaches this family belongs to that
  layer. *It is named and not cited: this contract asserts what the limiter does with a desired
  heading, not who supplies one.*
- **Every other layer reached is MECHANICAL**, through this body's own callees — the angle
  normaliser among them. *Its address is deliberately not cited: `BL-1`–`BL-6` are statements about
  comparisons and bit operations in this body, and none of them depends on how a normalisation is
  computed.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Movement" would otherwise be cleared by the word
> alone.*

## 17. Related

- [Battle locomotion, steering and recovery](Battle-Locomotion/battle-locomotion-steering-and-recovery.md) — the mechanism
- [Contract — heading, speed and the position delta](CONTRACT-heading-speed-to-position-delta.md) — S-18's second
- [Contract — facing and steering](CONTRACT-facing-and-steering.md) — S-18's first

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **Gameplay - CLIENT (1 edge).** `0033CB70` is also called by bodies filed to Gameplay: `00339630` (Combat) - shared machinery across the layer boundary, no shared ownership.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** Every clause of §2-§5 became a check that fails if the shipping image says otherwise. Script:
`Tools/analysis-kit/gfz-scripts/falsify_turn_limiter.py`, output `falsify_turn_limiter.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| T0 | §2 564 B | **survives** |
| T1 | BL-1 the three angles | **survives**: 45° (`00915614`), 120° (`00915FE0`) and 20° (`00D10AD8`), read from the compared operands; the raise is `or [rdx+0x38], 8` |
| T2 | BL-2 history decides | **survives**: with bit 3 clear the current heading is returned unchanged |
| T3 | BL-3 / BL-4 | **survives**: the latch needs `and ecx, 0x1c / cmp cl, 0x1c`; the release is `and [rdx+0x3c], ~1`; the middle band only tests the latch |
| T4 | BL-5 | **survives**: the pair is written clear-then-set. It is also **read** above 120° (`0033659D`), which steps the rate in the stored direction with no wrap call, as this contract's later section already says |
| T5 | BL-6 | **survives**: when the result equals `desired`, bit 3 of `+0x38` and bit 0 of `+0x3C` are cleared |
| T6 | §5 writes only the flag block | **survives**: every write goes through `rdx = ctx + 0x100` |

§5's read list omitted the direction pair and the two flag words it reads. It now lists them. No correction row: the
contract stated the committed-direction read elsewhere.
