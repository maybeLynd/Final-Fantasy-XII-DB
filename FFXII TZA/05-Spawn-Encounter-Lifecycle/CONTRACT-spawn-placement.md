---
contract: choose where a spawn appears relative to the party leader - an authored point validated against an arc and a distance band, or a random point filtered only by field-region containment
category: 05-Spawn-Encounter-Lifecycle
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md
entries: ["00234AF0", "003209C0", "00234DA0", "00265200", "00316DA0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the placement modes, the return window and the polar construction are the page's reading
    with site citations; the modded-settings behaviour is ASTRA's falsification package. OPUS
    assembled and scoped this contract on 2026-09-20 and did not re-derive the bodies. RE-DERIVED
    2026-09-29 (OPUS, falsification pass 1, falsify_spawn_placement.py P0-P8) - see the end of this page.
last_reviewed: 2026-09-29
audit:
  by: OPUS
  date: 2026-09-20
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-spawn-placement-falsification-pass-1
---

# Contract — spawn placement and the return window

> **Provenance, stated once.** **[page]** marks what is carried from
> [the spawn page](spawn-placement-and-retirement.md). **[FALSIF]** marks ASTRA's
> `spawn-lifecycle-falsification` package (methods A and B, no live game, 2026-09-12). **[live]**
> marks what only a running game settles.
>
> **A live record was deliberately NOT cited.** `EXP-080` is live (`live_game: true`, method C,
> COMPLETE) and sits in this subsystem's evidence directory, but it is about an older save
> restoring battle state and **touches no placement body**. Citing it would have given this
> contract a live runtime row it has not earned.

## 1. Purpose

When an encounter spawns, something has to decide **where**. That decision is made relative to the
**party leader**, either by validating a position the field data authored or by drawing one at
random inside an arc in front of them.

## 2. Interface

| | |
|---|---|
| choose a position | `Spawn_TrySelectCandidatePosition` (`00234AF0`), candidate index in `ECX` **[page]** |
| fetch the candidate | `FieldData_CopyFormat0Candidate` via `003209C0` — **0 on success, −1 on failure** **[page]** |
| return window | `SpawnKeep_GetReturnWindow` / `SpawnKeep_SetReturnWindow` **[page]** |
| returns | non-zero placed, `0` not placed **[page]** |

## 3. Types

The format-class-0 candidate record: **byte `+0x00` selects the mode**, `+0x10` carries the
authored position **[page]**.

## 4. Preconditions · postconditions · invariants

**I1 — A NEGATIVE RETURN WINDOW RESTORES THE DEFAULT, IT IS NOT AN ERROR.**
`SpawnKeep_SetReturnWindow` is `test ecx,ecx / mov eax,0x12C / cmovs ecx,eax`: **strictly negative →
300**. It is neither rejected nor clamped to zero. **The unit is seconds**, multiplied by the frame
rate before comparison with a raw tick delta **[page]**.

**I2 — THE CALLER REJECTS A NEGATIVE RETURN, NOT A ZERO ONE.** `003209C0` returns **0 on success**
and **−1 on failure**, and the placement code tests for negative. A reconstruction that treats
`0` as failure inverts the whole path **[page]**.

**I3 — THE TWO MODES ARE EXCLUSIVE, AND THEY ARE VALIDATED DIFFERENTLY.** Branching on the
record's first byte:

* **POINT mode** — the authored position is used, gated by an **arc test** about the leader's
  heading, `|wrap(leaderYaw − toCandidate)| ≤ (arcDeg / 2) · 2π / 360`, and **then** by the
  distance-band validator.
* **AREA mode** — a position is **drawn at random**: `r = (RNG() % ((max−min)·100)) / 100 + min`,
  `θ = wrap(leaderYaw + ((RNG() % arcDeg) − arcDeg/2) · 2π/360)`, and **the only filter is whether
  it lands inside the field region**. **No distance validation runs in area mode** **[page]**.

**I4 — THE LEADER ALONE IS CONSULTED, NOT THE PARTY.** `BattleUnit_GetPartyLeader`, and a null
leader returns 0. **No other party member is considered** in the radius calculation **[page]**.
*Made exact 2026-09-29 (OPUS, falsification pass 1). Point mode's band reaches the leader through a slot walk:
`00234DA0` measures to the party-focus slot among 0-3, and that is the handle `003272A0` resolves. So the leader
must also be one of those slots and pass their status gate, or point mode returns 0.*

**I5 — AN EMPTY BAND IS REFUSED FIRST.** `max_radius − min_radius == 0.0` → `0`, before the
candidate is even fetched **[page]**.

**I6 — AREA MODE DOES NOT PUBLISH `out_observed`, AND THE AUTOMATIC CALLER READS ITS SLOT ANYWAY.**
The same uninitialised-read shape found elsewhere in this engine: the producer leaves the slot
untouched on one path while the consumer reads it regardless **[page]**.
**RULED 2026-09-25 (FABLE, Claude Opus 5.5), on `FABLE-REQ-OPUS-S16-I6-SLOT-GATES-ACCEPTANCE`: the slot is consumed
meaningfully. It decides whether a successful candidate is accepted.** **[static]**
- **The caller's use.** The automatic caller `Spawn_SelectAndPrepareAutomaticEntry` passes a stack slot as
  `out_observed`. When the placement returns non-zero it reads the slot back and compares
  it with the threshold `[02F973B8]`, loaded once into `xmm6` at entry. A value **below** the threshold accepts
  the candidate. Otherwise the attempt counts as a miss and is retried, up to `[0208D457]` times.
- **Nothing else writes the slot.** The caller never writes that slot. The placement writes it only on the point
  path, and only when the unit is the party focus (`PartyFocus_IsCurrentPackedActorHandle`, the page's §11
  pseudocode).
- **So two cases read a value this call did not produce:** the area path, and the point path for a non-focus unit.
  They read the value left by an earlier point-mode call in the same loop, or older stack contents. If it is not
  below the threshold, every successful candidate on that path is refused and the loop exhausts its retries.

*Not established:* which values the slot holds in ordinary play. That is `L-12`'s live question on the page.

**I7 — THE POLAR CONSTRUCTION DOES NOT WRITE `Y`, AND THE CALLER COPIES THE UNWRITTEN LOCAL.** Only `X`
and `Z` are set; **what supplies the vertical coordinate is unresolved** and recorded as `L-7`
**[page]**. **NARROWED 2026-09-25 (OPUS), consuming EXP-145:** `00319390` writes `[rdx]` and
`[rdx+8]` only (`00319411`, `00319415`); `00234AF0` hands it `rdx = rsp+0x50` (`00234CB2`) and later
copies `[rsp+0x54]` into `result.y` (`00234CDD` → `00234CF2`) with **no write to `rsp+0x50..0x5B`
anywhere in its body**, and `FieldRegion_ContainsWorldPosition` (`002374E0`, handed the same buffer)
makes no memory write of its own. So in area mode **`result.y` is uninitialised stack** — EXP-145
observed its `0xCD` fill replacing an authored `y = 7.5` **[exec]**, and the static read agrees
**[static]**. Whatever supplies the real `Y` runs **downstream** of `00234AF0`.

**I8 — the trig is a table, and its convention is shared.** A **32,768-entry** sine table at
`01F004E0`, indexed `(θ/2π)·scale & 0x7FFF`, with `cos = sin[(0x2000 − i) & 0x7FFF]`. The
convention `X = sin(θ)·r, Z = cos(θ)·r` is **identical** to `Movement_ComputeDeltaFromHeadingSpeed`,
and `Vector3_ComputeXZHeadingOrFallback` is its exact inverse `atan2(dx, dz)`, falling back to the
supplied heading when the two points coincide **[page]**.

## 5. State

`g_nSpawnKeepReturnWindow` (seconds, default 300), the authored format-class-0 candidate records,
and the sine table at `01F004E0`. *Added 2026-09-29 (pass 1):* the arc width `arcDeg` is the global `02089358`. It is read only by `00234AF0`, stored as
180 by `0023A520`, and set by script through `VM_Spawn_SetCandidateHeadingArcDegrees` (`0050F470` → `0023A1F0`).
The verbs are `btlAtelSetupActorStart` and `btlAtelSetSpawnLimitDegree`. Their zone census, including the two zones that
open the arc to 360°, is on [the tunables page](spawn-placement-height-and-authored-tunables.md).

## 6. Relationships

`00265200` reads the leader's class-dependent heading; `00316DA0` wraps an angle;
`FieldRegion_ContainsWorldPosition` is area mode's only filter; the distance validator is point
mode's **[page]**.

## 7. State transitions

```
place(candidateIndex):
    if (max - min == 0.0)                      return 0        (I5)
    if (003209C0(candidateIndex, &rec) < 0)    return 0        (I2)
    leader = GetPartyLeader(); if (!leader)    return 0        (I4)
    if (rec[0] == 0)   POINT: arc test, then distance band     (I3)
    else               AREA:  random r,theta; region test only (I3)
```

## 8. Script · resource · event interactions

The candidate records are **authored field data**; the script selects which encounter spawns, not
where it lands **[page]**.

## 9. Determinism

**Area mode is NOT deterministic** — it draws twice from the generator, once for the radius and once
for the angle, so placement consumes RNG state and **the draw count is part of the contract** in the
same way S-10's is. Point mode draws nothing. *(2026-09-29, pass 1: each draw is one call to `00328370`, which
steps the LCG three times, so an area placement advances the shared stream by six steps.)*

## 10. Failure paths and edge conditions

* **Empty band** (I5), **negative fetch** (I2), **null leader** (I4) → `0`.
* **Arc miss in point mode** → `0` without a distance test.
* **Region miss in area mode** → `0` without a distance test (I3).
* **`out_observed` unset in area mode** while the caller reads it (I6).
* **`Y` unwritten** (I7).
* **Two unguarded divisors in area mode** *(2026-09-29, pass 1, static)*: `(int)((max − min) · 100)` and `arcDeg`
  reach `idiv` untested. A band narrower than 0.01, but not exactly 0.0, and an arc of 0 divide by zero. A NaN band
  is not refused by I5 (`jp` proceeds).
* **MODDED SETTINGS CAN SKIP PLACEMENT ENTIRELY.** ASTRA's falsification found that **large modded
  attempt settings can skip choosing a position and accept old coordinates** — normal spawn rules
  survived the other checks **[FALSIF]**.

## 11. Observable behaviour

Foes appear in front of the party leader at a plausible distance. Under modded settings they can
appear where the last thing was (§10) **[FALSIF]**.

## 12. Reproduction formula

Implement §7 in order. **Take I2 literally** — `0` is success. **Do not add a distance check to area
mode**; the absence of one is the contract. **Do not initialise `out_observed` on the area path**
unless you also change the consumer, because I6 describes a real asymmetry rather than a bug to be
tidied. Draw exactly twice in area mode (§9).

## 13. Runtime validation

**EXECUTED — [EXP-145](../_experiments/EXP-145-spawn-placement-exec.md)** (method B, no live game;
SWE2-ORACLE; 20/20, stable ×3). `00234AF0` ran on shipped bytes in both modes with planted
field-data, leader and unit fixtures: I1's window (negative → 300, **zero NOT clamped**), I2's
`0/−1` fetch convention, I3's modes and region shapes (`1` box, `2` ellipsoid), I4's null leader
copying the authored position out **before** failing, I5's empty band refused before the fetch,
I7's unwritten `Y` (above), and §9's draw counts (point **0**, area **exactly 2**, including on a
region miss). **Consumed by OPUS 2026-09-25:** I7 was re-read statically and agrees; the other
verdicts are recorded as executed, not re-derived. *The section's former "No placement body has
been executed" is superseded by this record.*

What also exists is **ASTRA's `spawn-lifecycle-falsification`** (methods A and B, **no live game**), which
is genuine evidence *about this subsystem* and produced §10's modded-settings finding **[FALSIF]**.

**`EXP-080` IS NOT CITED, AND THE OMISSION IS DELIBERATE.** It is live, complete, and filed under
this subsystem's evidence — but it concerns an older save restoring battle state and **touches no
placement body**. An adjacent live record is not evidence for a mechanism it never ran.

~~UNLINKED / nothing-executed~~ — **LINKED to EXP-145** (2026-09-25). No exemption was ever added.

## 14. Unresolved

* **What supplies `Y`** — `L-7` (I7). **Narrowed, not closed:** nobody at this level; the area-mode
  `result.y` is uninitialised stack, so the supplier (a ground snap or similar) is **downstream of
  `00234AF0`** and not yet identified **[exec + static]**.
* ~~**Whether I6's uninitialised slot is ever consumed meaningfully**, or merely read and discarded.~~ **Ruled
  2026-09-25 (FABLE, Claude Opus 5.5): meaningfully.** It gates acceptance against `[02F973B8]` (I6). What values it
  holds in play stays `L-12` **[live]**.
* **Whether the modded skip is reachable unmodified** **[FALSIF]**.
* **No live evidence** for placement **[live]** — EXP-145 is original-code execution on planted
  fixtures, not a game session.

## 15. Evidence

The modes, the window, the polar construction and the shared trig convention are the page's
**[page]**; the modded-settings behaviour is ASTRA's **[FALSIF]**. This contract's contribution is
I1–I8 stated as a contract, §12's three "do not tidy this" notes, and §13's explicit refusal to
borrow an adjacent live record.

## 16. Parity plan

Test I2 first with a `0` return and assert **success** — a reimplementation that inverts it fails
everything downstream and looks like a data problem. Then point mode at the arc boundary, area mode
for region containment only, and **assert the generator advances exactly twice per area placement**
(§9). **Do not assert anything about `Y`** (I7) or about `out_observed` on the area path (I6): both
are contract holes, and a fixture that pins them would be testing the harness.

## SWE2-EC7-107 update (2026-09-20) - `00234DA0` measured

`00234DA0` (290 B) is the four-slot
range probe `00234AF0` and
`00308040` run: `edi = 0..3` walks
`0031B810(edi)` slots - each must
be live with `[+0x698]` populated
and pass the `([+0x64] | [+0x3C]) &
0x80000003` / `00313F60()` gate
(`r12d == 0` additionally requires
`003273B0(dword[+8])`); surviving
slots resolve a triple through
`00265020([+0x10], &out)` and score
it through `0031E620(rcx, &out)`,
which must fit inside the optional
`[r15]` lower / `[r14]` upper
bounds; `rbp` non-null with
`003273B0(dword[+8])` writes the
score to `[rbp]` and returns 1 -
the bounded placement probe the
spawn arms share.
Interior anchor `00234DE2` (the
first `0031B810` call).

Mechanical neighbours introduced by
this section's citations: the shared
helpers `00265020`, `00313F60`,
`0031B810`, `003273B0` and
`00308040` carry caller fan-in from
ActorEntity (24 edges), Gameplay
(11), Presentation (10), CombatAI
(9), UI (4), CombatFormula,
Status_Periodic_Terminal and
Rewards_Progression_Economy (3
each), Audio, Input and
Items_Equipment_Shops_License (1
each). These are edges of the
helpers, not of the placement
contract - noted so the audit
accounts for them.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives; the bodies re-derived, four facts added

**Attack.** The frontmatter said the bodies were never re-derived. This pass derives them. Every clause of §2-§10 became a
check that fails if the shipping image says otherwise. The checks decode every listed body in `.text`, so caller counts and
reference censuses are whole-image. Script: `Tools/analysis-kit/gfz-scripts/falsify_spawn_placement.py`, output
`falsify_spawn_placement.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Killer | Result |
|---|---|---|---|
| P0 | §2 the interface | another caller, or other argument registers | **survives, made exact** (below) |
| P1 | I1 the negative window restores 300 | another body | **survives**: `test ecx, ecx / mov eax, 0x12c / cmovs ecx, eax`, cell `0208936C` |
| P2 | I5 before the fetch; I2 `js`; I4's null leader after the copy-out | another order or test | **survives**; a NaN band is not refused (`jp` proceeds) |
| P3 | I3 point mode's arc test, then the distance band | another comparison or unsquared bounds | **survives**: `|wrap(yaw − toCandidate)|` (`0031A930` ends in `andps`) ≤ integer `arcDeg / 2` × 2π/360; bounds squared by the caller |
| P4 | I4 "the leader alone ... no other party member is considered" | a band measured to a unit other than the leader | **survives, made exact** (below): the band walks four slots, but the one caller admits only the leader's |
| P4b | that the focus slot is the leader | the leader getter and the focus test read different handles | **survives**: both read `003590D0` |
| P5 | I3 area mode's formula and its one filter | another formula or a distance test | **survives, made exact**: both remainders are integer `idiv` (below) |
| P6 | §9 two draws in area mode, none in point mode | a third call, or a draw on the point path | **survives**, and each draw steps the LCG three times (below) |
| P7 | where `arcDeg` comes from | nothing; the contract did not say | **global state** `02089358` (below) |
| P8 | I7 the polar writer writes X and Z only; I8's table | a `Y` write | **survives**: `00319390` writes `[rdx]` and `[rdx+8]` through `01F004E0` with `& 0x7fff` and the `0x2000` offset |

* **P4: I4 survives, but its mechanism is a slot walk, not the leader pointer.**
  * Point mode's band is `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`). It walks party slots 0-3 through
    `0031B810`, never calls the leader getter, and rejects on the first eligible slot outside `[min², max²]`.
  * Its sixth argument decides eligibility. With 0, only the slot whose actor handle equals
    `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`, through `003273B0`) is eligible.
  * `BattleUnit_GetPartyLeader` (`003272A0`) resolves that same handle. So with 0 the band is measured to the leader's
    own slot, and the one caller, `Spawn_SelectAndPrepareAutomaticEntry`, passes 0 (`mov dword ptr [rsp + 0x28], 0`
    before `00235950`).

  I4 holds for shipped play. What the slot walk adds is a failure path I4 did not state: the leader must also be one of
  slots 0-3 and pass the slot's status gate (`([+0x64] | [+0x3C]) & 0x80000003` → `00313F60`). Otherwise no slot is
  eligible and point mode returns 0. A non-zero flag, which no caller of `00234AF0` passes, would require every eligible
  slot inside the band. *A first draft of this pass read the slot walk as refuting I4. P4b, which pins the shared handle,
  withdrew that before publication.*
* **P0: the signature, exact.**

  ```
  00234AF0(ECX = candidateIndex, RDX = outPosition, XMM2 = minRadius, XMM3 = maxRadius,
           arg5 = out_observed (float *), arg6 = slotFlag)
  ```

  `ECX` reaches `003209C0` untouched. `out_observed` is `r14` (`[rbp + 0x77]`), handed to `00234DA0` as its `r9`.
  `slotFlag` is `[rbp + 0x7f]`, passed on as the validator's fifth argument.
* **P5: quantisation and two unguarded divisors.**
  * The radius is `(RNG % (int)((max − min) · 100)) / 100 + min`: `cvttss2si` truncates the divisor, so the radius comes
    in steps of 0.01.
  * The angle offset is `(RNG % arcDeg) − arcDeg / 2` whole degrees. For an even arc that is `[−arcDeg/2, arcDeg/2 − 1]`,
    one degree short on the positive side.
  * Neither divisor is tested. A band with `0 < (max − min) · 100 < 1`, or `arcDeg = 0`, reaches `idiv` with a zero
    divisor. I5 refuses only an exact `0.0`. *Static, not executed; §10 records it.*
* **P6: two draws, six LCG steps.** `RNG_SharedGameplayLCG_NextU32` (`00328370`) steps the `0x41C64E6D` LCG **three
  times** per call and stores once. It returns at most 31 bits, so the signed `idiv` never sees a negative dividend. An
  area placement therefore advances the shared stream by six steps. A reproduction that counts "two draws" as two LCG
  steps drifts. The point path's closure, 23 functions, draws nothing.
* **P7: `arcDeg` is global, script-set state.** The cell `02089358` is read only by `00234AF0`. Two functions write it:
  * `Spawn_SetCandidateHeadingArcDegrees` (`0023A1F0`), called only by the script verb's native
    `VM_Spawn_SetCandidateHeadingArcDegrees` (`0050F470`);
  * `0023A520`, which stores **180** (`0xB4`).

  §5 did not list it. It is recorded there now.
* **Currency.** The frontmatter's "did not re-derive the bodies" is superseded by this pass. EXP-145 remains the executed
  evidence.

Consumer record: [`_index/candidates/spawn-placement-falsification-pass-1-0929/`](../_index/candidates/spawn-placement-falsification-pass-1-0929/README.md).
No contradiction row: nothing the contract asserted was false.

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT and SERVICE (38 edges).** `00265020` is also called by bodies filed to ActorEntity: `00236300`; `00234AF0`, `00234DA0` reach bodies filed to ActorEntity: `00265020`, `0031B810` - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT (2 edges).** `00265020`, `003590D0` are also called by bodies filed to audio: `00362850` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (14 edges).** `00308040`, `00313F60` are also called by bodies filed to combat AI: `00301830`, `00321850`, `00321B00` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (15 edges).** `00265020`, `00265200` are also called by bodies filed to combat action: `002F8060`, `00307300`, `00320E10` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (3 edges).** `00265020`, `00313F60`, `0031B810` are also called by bodies filed to combat formula: `00384F40`, `00388D50` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (14 edges).** `00234DA0`, `00265020` are also called by bodies filed to Gameplay: `00308040` (Combat), `0031ADB0` (CombatAction), `00339630` (Combat); `00308040` reaches bodies filed to Gameplay: `0030B050` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT (2 edges).** `00313F60`, `003590D0` are also called by bodies filed to input: `00253C70`, `00226BE0` (ActorControlMaskPropagationRuntime) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (1 edge).** `0031B810` is also called by bodies filed to items/equipment: `00309FB0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (56 edges).** `00265020` is also called by bodies filed to movement: `0024B6F0`, `002E45E0`, `002EBFA0`; `00234AF0` reaches bodies filed to movement: `00265200` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (20 edges).** `00265020` is also called by bodies filed to party: `00303CC0`, `00304180`; `00234AF0`, `00234DA0` reach bodies filed to party: `003272A0`, `003273B0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (22 edges).** `00265020` is also called by bodies filed to presentation: `002B7B80` (UI), `00322360`, `0037AD40` (EffectConstraint) - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - CLIENT and SERVICE (2 edges).** `00328370` is also called by bodies filed to random selection: `00308EC0`; `00234AF0` reaches bodies filed to random selection: `00328370` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (3 edges).** `00265020`, `0031B810` are also called by bodies filed to rewards/progression: `002FB150`, `00312280`, `002F8BB0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (50 edges).** `0023A1F0`, `00265020` are also called by bodies filed to script VM / native bridge: `0050F470`, `0033FD60`, `00344AF0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (3 edges).** `00313F60`, `003273B0` are also called by bodies filed to status/periodic terminal: `00320450`, `00329A20`, `00310DB0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (7 edges).** `00265020`, `00265200`, `00313F60` are also called by bodies filed to UI: `003C5130`, `0031EB20`, `00322A80` (BattleMenu) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (2 edges).** `003590D0` is also called by bodies filed to World: `0025E400` (ActorManager), `002623A0` (ActorManager) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (6 edges).** `00313F60` is also called by bodies filed to WorldAreaField (world area): `00234590`; `00234AF0`, `00234DA0` reach bodies filed to WorldAreaField (world area): `002374E0`, `003209C0`, `00313F60` - shared machinery across the layer boundary, no shared ownership.
