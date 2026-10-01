---
contract: Fire at most one authored field trigger per call — proximity, a fixed roll, a once-ever flag
category: 03-World-Area-Field
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: walking-into-an-authored-trigger-point.md
entries: ["002F8060"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the body read at instruction level, both float constants resolved to their
    stored values, the loop bound and the roll threshold read at their instructions, and an
    image-wide re-measurement of the "draws the generator and writes a persistent flag" pair.
    **This records checks performed on that date, not the method of the original derivation**, which
    is on the trigger-point page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-trigger-points-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — authored field trigger points

> **Authored 2026-09-22 by FABLE.** S-11's binding gap is *"1 of 3 pages by subject"* — its one
> contract, [`CONTRACT-field-record-accessors.md`](CONTRACT-field-record-accessors.md), covers the
> field-record accessors. **This takes the trigger points**; the environment variant remains
> uncontracted and this document does not claim it.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants.

## 1. Purpose

Decide whether walking somewhere trips an authored point, and if so which of its two outcomes
happens — once, ever.

## 2. Interface

| | |
|---|---|
| **Entry** | `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`), **648 bytes** |
| **Live set** | a 32-bit mask per field, in a 12-byte-stride table at `02EC3EA0` |

## 3. Types

```
authored point record
  +0x00  s16  first coordinate, in TENTHS
  +0x02  s16  second coordinate, in TENTHS
  +0x04  u8   persistent flag id — 0xFF means "set none"
  +0x06  u16  outcome on the 75 branch
  +0x08  u16  outcome on the 25 branch
  +0x0A  u8   read by 002FB8C0: zero takes a fast path (*out = ctx, return 1)   (added 2026-09-25, OPUS block 317;
              so the record is at least 11 bytes)
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**TP-1 — Coordinates are authored in tenths, and the threshold is the float NEAREST 1.3.** Two
`divss` by `10.0` (`002F818D` loads it; `002F81D0` and `002F81E5` apply it), then
`002F81F4 comiss xmm7, xmm0` against `xmm7` = **`1.2999999523162842`**, the `f32` at `00901B34`.
~~*A reimplementation comparing against a decimal `1.3` in double precision differs at the boundary —
the stored constant is below 1.3, so a distance between the two values fires in the original and not
in the copy.*~~ *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 317, which executed it; bytes re-read.)* **The direction was reversed.** The original fires only for `d ≤ 1.2999999523`. A copy that
compares against a decimal `1.3` in higher precision **also** fires for `d` in `(1.2999999523, 1.3]`. So the boundary
case fires in the copy and not in the original, and only when the copy computes the distance above `f32`: no
`f32` value lies between the two thresholds.

**TP-2 — ~~The authored point has NO HEIGHT, so the unit's height is spent against the same budget.~~ BOTH HEIGHTS ARE
ZEROED, so the radius is horizontal.** *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 317, which executed it; bytes re-read.)* ~~The point's third component is written **zero** while the unit's own
position is real in all three.~~ The point's height is written zero (`002F81C1`). **So is the unit's**: `002F8150 mov
[rsp+0x54], edi` overwrites the height `Actor_GetWorldPosition` just returned (`002F8131`–`002F813E`) with `edi = 0`.
OPUS measured it: a unit 1.0 above a point 1.0 away fires. ~~**A point is therefore harder to reach from above or below
it**, and how much harder is a property of the area's authored ground level rather than of the point.~~ **Height
does not count at all.** *This is a consequence of the code as
written; a distance check summarised as "within 1.3 units" loses it entirely.*

**TP-3 — The 75/25 split is in the instruction stream, not in the record.** `002F8231 cmp r8d, 0x4b`
— `0x4B` is 75 — after a `% 100` on the draw. **The two outcomes are authored per point
(`+0x06`, `+0x08`); the odds are not, and no point can change them.**

**TP-4 — At most one point fires per call, and the once-ever guarantee is a cleared bit.** On a hit
the body sets the persistent flag when the id is not `0xFF` (`002F8247`, then
`PersistentFlag_SetBank512Low`), delivers the chosen outcome, notifies, **clears this point's bit in
the field's live mask, and `break`s**. *So two overlapping points cannot both fire on one call, and
the one that does is chosen by loop order rather than by distance.*
**The "once-ever" is bounded by a ring** *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 317, which executed it; bytes re-read.)*. The field's live mask is held in a **three-slot ring** at `02EC3EA0`
of `{field, mask}` records, 12 bytes each. `002FB3B0`, called only by this body after a fire, stores a field not yet
present at the write index `+0x24`, increments `+0x28` and advances the index modulo 3 (`002FB3CF`–`002FB403`).
`002FA230` clears the ring. It has two call sites in the raw call index, one inside the battle-system runtime reset.
So a cleared bit is remembered for the three most recently fired-in fields, until that clear. Whether an evicted
field is re-armed when revisited is not established.

**TP-5 — The 32-point ceiling IS the mask, and the loop was written to respect it.**
`002F80BC mov ebx, 0x20` bounds the walk at `min(count, 32)`, and the live set is exactly 32 bits
wide. *The limit is not a property of the data; a field authored with more than 32 points would have
the surplus silently unreachable.*

**TP-6 — Eligibility is shared vocabulary, and three other systems use the same fields.** Read from
the acting unit's record: **bit 26** of the combined status words; **bit `0x20` of `+0x6C` and of
`+0x7C`** — *the two effect layers of
[the effect-layer contract](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md)*
(`002F80DA`, `002F80E4`); and **`rec[+0x05]`** with, when it is 0, `rec[+0x04]` outside `0x1B … 0x27`
(`002F8113 cmp al, 0xc` after the subtract). **`rec[+0x05]` is the same selector byte
[stat derivation](../08-Combat-Formula/CONTRACT-stat-derivation.md) and
[enmity](../09-Combat-AI-And-Gambits/CONTRACT-enmity.md) branch on**, and the `0x1B … 0x27` band is
the same one the experience split excludes, written the same way — **the thirteen Espers**
([the type-id partition](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md)):
summons take no experience share and are not trigger-eligible acting units, so the two
exclusions are one fact.

**TP-7 — This is one of exactly TWO functions in the image that both draw the generator and write a
persistent flag.** Re-measured: sweeping every body for a call to the MT19937 thunk `00379CD0` **and**
a call to any of the seven persistent-flag setters returns `002F8060` and `002FAFD0`, and nothing
else. *So a trigger is one of only two places where a random draw becomes permanent save state — and
it is the one whose ratio is fixed (TP-3).*

## 5. State

**Owned:** the field's 32-bit live mask at `02EC3EA0`. **Written outside it:** one persistent flag
per firing point, unless the id is `0xFF`. **Read, never written:** the authored point records and
the acting unit's status words and selector bytes.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-field-record-accessors.md`](CONTRACT-field-record-accessors.md) — S-11's contracted third |
| **Uncontracted** | the field environment variant — S-11's remaining page, not claimed here |
| **Shares the generator** | [the periodic tick](../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md), whose Regen arm draws the same `00379CD0` (TP-7) |
| **Shares a selector** | stat derivation and enmity, on `rec[+0x05]` (TP-6) |

## 7. State transitions

Per call: *eligibility (TP-6) → for each of at most 32 live points: distance (TP-1, TP-2) → on a hit,
roll (TP-3) → set flag → deliver → clear the bit → **stop** (TP-4).* A point transitions `live →
spent` exactly once and never back.

## 8. Script · resource · event interactions

The point records and their two outcomes are authored; the odds and the ceiling are not (TP-3, TP-5).

## 9. Determinism

**Not deterministic**: TP-3 draws the shared generator, so which of the two outcomes a point gives is
a stream position. *Whether it fires at all is deterministic (TP-1, TP-2, TP-6); only which outcome
is not.*

## 10. Failure paths and edge conditions

- A flag id of `0xFF` fires the point and records nothing — repeatable across saves in every respect
  except the live mask, which is per field.
- More than 32 authored points in one field leaves the surplus unreachable (TP-5).
- Two overlapping points: the first in loop order wins, the other stays live (TP-4).

## 11. Observable behaviour

Walking over a spot in the field makes something happen once and never again; the same spot gives one
of two results, three times in four the first one.

## 12. Reproduction formula

Place a unit at exactly the stored threshold distance and assert it fires (TP-1 — **the constant is
below 1.3**). Place it at the point's coordinates but a height away and assert the height is charged
against the same budget (TP-2). Author 33 points and assert the 33rd never fires (TP-5). Overlap two
and assert exactly one fires and the other remains live (TP-4).

## 13. Runtime validation

**None.** No experiment executes this body. S-11's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*

## 14. Unresolved

- ~~What the `0x1B … 0x27` kind band is — **two systems exclude it and neither names it** (TP-6).~~
  **CLOSED 2026-09-23 (SWE2-CONTRACT): the thirteen Espers.** The band is the summon rows
  27–39 of the party definition table — Belias through Zodiark — on
  [the actor type-id partition](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md)
  (AUDITED). `0x1A` = the Chocobo is tested apart because it earns LP; the Espers earn nothing.
  *So both exclusions are the same fact about summons: they take no experience share and are not
  trigger-eligible acting units.*
- ~~What `002FAFD0`, the other RNG-and-flag function, is for (TP-7).~~ **CLOSED 2026-09-23
  (SWE2-CONTRACT): the treasure-chest outcome resolver.** Already answered on
  [the persistent-flag-banks page](../14-Story-Event-Quest-Hunt/persistent-flag-banks.md) §8d
  (AF-6, FABLE 2026-09-12), re-verified by decoding `002FAFD0`–`002FB14A` whole: sole caller is
  the durative verb `btlAtelOpenTreasureMessage`'s end thunk `0050FAF0`; record `+0x0B` is the
  gil chance, `+0xC`–`+0x12` two item pairs swapped 50/50 → 95/5 when the leader carries effect
  layer 25 (Diamond Armlet), `+0x14`/`+0x16` the gil amounts (bit 6 of `+8` = random `1..N`),
  `+9` the persistent flag set unconditionally. The "two RNG-and-flag functions" of TP-7 are a
  trigger point and a chest roll — the entire RNG→persistent-save surface.
- The field environment variant, S-11's other uncontracted page.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| TP-1 — the divisor and the threshold | both constants resolved to their stored `f32` values: `10.0` at `008F8180` and **`1.2999999523162842`** at `00901B34` | 1 |
| TP-3 — 75 in the instruction stream | `002F8231 cmp r8d, 0x4b` | 1 |
| TP-5 — the 32 bound | `002F80BC mov ebx, 0x20` against a 32-bit mask | 1 |
| TP-6 — the shared fields | `002F80DA`, `002F80E4` and `002F8113` read at their addresses | 1 |
| TP-7 — exactly two such functions | every body swept for a call to `00379CD0` **and** to any of the seven `PersistentFlag_Set*` entries; two results | 1 |
| TP-2, TP-4 and the record map | [the trigger-point page](walking-into-an-authored-trigger-point.md), falsified once 2026-09-03 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on TP-1 through TP-7. **TP-1's constant is the one
to copy literally** — `1.2999999523162842`, not `1.3` — and **TP-2 is the one most likely to be
"corrected" into a 2-D distance check**, which would change which points are reachable.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **WorldAreaField — internal.** The body is this category's own.
- **RNG_Random_Selection — SERVICE.** The generator thunk is that layer's and TP-7 is about it.
- **Status_Periodic_Terminal, CombatFormula, CombatAI — MECHANICAL, and their presence is TP-6's
  point.** The status layers and the `rec[+0x05]` selector are read here and branched on there; this
  contract asserts the sharing, not any behaviour of theirs.
- **CoreRuntimeScheduling, Rewards_Progression_Economy — MECHANICAL, through the GENERATOR.** Both
  are simply other callers of `00379CD0`. **A shared generator's callers are not a relationship**;
  they are the rest of the engine, and TP-7's claim is about which of them *also* writes a persistent
  flag — a much narrower set of two.
- **ActorEntity — MECHANICAL.** The body asks that layer for the unit's world position, which is
  TP-2's input.
- **Party — MECHANICAL.** Reached only through `002FAFD0`, the *other* function of TP-7's pair, which
  this contract names and does not read.
- **Every other layer reached is MECHANICAL**, through this body's own callees. *Their addresses
  beyond those named above are deliberately not cited: each is a hub, and naming one imports its
  whole edge set.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

*§16a's heading is numbered, so the crossings gate does not read it as a crossing section. This section states the
crossings that the OPUS block 317 corrections add.*

**ActorEntity — MECHANICAL.** The body's position query and two lookups made by the record helper `002FB8C0` belong
to that layer. TP-2 uses only the position, and zeroes its height before the distance.

**CombatAction — OWNER.** The body is that layer's by primary owner. The ring store `002FB3B0` and the record helper
`002FB8C0` are its callees, each from one site in the raw call index (`002F82A4`, `002F8265`). The generator thunk's
other callers in that layer are not a relationship (TP-7).

**Gameplay — LIFECYCLE.** The ring's clear `002FA230` is called from the battle-system runtime reset. That reset bounds
how long TP-4's cleared bits are remembered. When it runs relative to field entry is not traced here.
- **CombatFormula - CLIENT (53 edges).** `00379CD0` is also called by bodies filed to combat formula: `003851F0`, `00387130`, `00387FD0` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT (2 edges).** `00379CD0` is also called by bodies filed to core runtime: `0022B6E0`, `0022B7E0` - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - SERVICE (1 edge).** `0050FAF0` reaches bodies filed to items/equipment: `00300B80` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (1 edge).** `002FAFD0` reaches bodies filed to party: `003272A0` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (2 edges).** `002F8060`, `002FAFD0` reach bodies filed to random selection: `00379CD0` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT and SERVICE (3 edges).** `00379CD0` is also called by bodies filed to rewards/progression: `002F9A60`, `002F9B20`; `0050FAF0` reaches bodies filed to rewards/progression: `003004B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (4 edges).** `002FAFD0`, `00379CD0` are also called by bodies filed to script VM / native bridge: `0050FAF0`, `00354BF0`, `00355140`; `0050FAF0` reaches bodies filed to script VM / native bridge: `00267E10` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (2 edges).** `002F8060`, `00379CD0` are also called by bodies filed to status/periodic terminal: `00310DB0`, `00386C70` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (2 edges).** `002F8060`, `002FAFD0` reach bodies filed to story/event: `0032AD70` - shared machinery across the layer boundary, no shared ownership.

## 17. Related

- [Walking into an authored trigger point](walking-into-an-authored-trigger-point.md) — the mechanism
- [Contract — field record accessors](CONTRACT-field-record-accessors.md) — S-11's contracted third
- [Contract — the effect layers](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md) — TP-6's supplier

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** TP-1 to TP-3 and TP-5 to TP-7 became checks at their instructions; TP-7's census is image-wide. Script:
`Tools/analysis-kit/gfz-scripts/falsify_trigger_points.py`, output `falsify_trigger_points.out`, image `73461d08…`,
0 BROKEN. TP-4's ring behaviour is OPUS block 317's execution, and is not re-run.

| # | Clause attacked | Result |
|---|---|---|
| P0 | §2 size | **survives**: 648 B |
| P1 | TP-1 | **survives**: 10.0 at `008F8180`, two `divss`; `comiss xmm7, xmm0` against `[00901B34]` = 1.2999999523162842 |
| P2 | TP-2 | **survives**: the unit's height is overwritten with `edi = 0` at `002F8150`; the point's is written 0 at `002F81C1` |
| P3 | TP-3 | **survives**: `cmp r8d, 0x4b` |
| P4 | TP-5 | **survives**: `mov ebx, 0x20` |
| P5 | TP-6 | **survives**: bit `0x20` of `+0x6C` and `+0x7C`; `cmp al, 0xc` |
| P6 | TP-7 | **survives**: of the seven `PersistentFlag_Set*` entries, exactly `002F8060` and `002FAFD0` call one and also call `00379CD0` |

No correction.
