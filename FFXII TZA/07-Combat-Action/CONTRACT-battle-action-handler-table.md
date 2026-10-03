---
contract: Dispatch 359 AI-order ids through one table into eight handlers, with availability reading the same table
category: 07-Combat-Action
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: 07-Combat-Action/Action-Dispatch/battle-action-handler-table.md
entries: ["00305080", "002FDDA0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's figures **read from the
    table's own bytes rather than carried** — the 359 slots decoded, the distinct handlers counted,
    the slot past the bound read as a non-pointer, and **the bulk handler opened to confirm it
    re-reads the id the tail-call does not pass it**. **This records checks performed on that date,
    not the method of the original derivation**, which is on the handler-table page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-handler-table-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the battle action handler table

> **Authored 2026-09-22 by FABLE.** S-20's binding gap is *"2 contracts over 4 pages"*. **This takes
> the handler table**, which no contract covered.
>
> Written against FRONTIER's adequacy test. **`HT-4` is why this is not an operation-scoped
> contract:** two bodies in two different layers read this table with the same bounds and the same
> emptiness test, and the invariant is that they *agree* — which neither of them can state alone.

## 1. Purpose

Turn an AI-order id into the routine that carries it out, and answer separately whether that order
is available at all.

## 2. Interface

| | body | owner |
|---|---|---|
| **dispatch** | `BattleUnit_AdvanceExtendedActionState` (`00305080`) | `CombatAction` |
| **availability** | `AiOrder_CheckActionPreconditions` (`00301830`) | `CombatAI` |

```
01EEC460   void*[359]    index = id - 0x4000,  ids 0x4000 .. 0x4166
```

## 3. Types

```
battle unit
  +0x708   ptr   the order record the handlers read
  +0x714   u16   THE ORDER ID -- the handler re-reads it here (HT-3)
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**HT-1 — 359 slots, and the extent is OVER-DETERMINED rather than asserted.** Index is `id − 0x4000`
bounded by `cmp eax, 0x166` / `ja` in **both** consumers. Decoded from the table's own bytes: **341
non-null, 18 empty, and every non-null entry is a valid `.text` pointer.** *The qword just past the
bound is `0000000400000002` — not an address — so the table's end is visible in its data.*

**HT-2 — 359 ids resolve to just EIGHT distinct handlers, and one of them serves 249.**
`002FDDA0 BattleUnit_ExecuteDirectStateCommandOrder` is named by **249** ids, `002FDA60` — whose
recovered name is literally `caseD_4000` — by **57**, then 25 and 6, with four further handlers on
the remaining slots — **one id each**, measured over the whole id space ([OPUS block 350](../_index/candidates/s20-opus-replay-handler-table/README.md), 2026-09-25). *So this is not
a 359-way dispatch. **The id is a parameter at least as much as
a selector**, and a reimplementation that writes a routine per id has mistaken the design.*

**HT-3 — The dispatcher TAIL-CALLS with only `this` set, so the handler must re-read the id from the
unit — and it does.** `003050F1 mov rcx, rbx` then `003050FE jmp rdx`: no id is passed. `002FDDA0`
then does `002FDDB0 movzx edx, word ptr [rcx + 0x714]`, reading the order id back off the unit.

> ***That is what makes `HT-2` and the tail-call consistent with each other.*** A handler shared by
> 249 ids needs the id; a tail-call cannot hand it over; the id is therefore **state on the unit**,
> not an argument. *A port that passes the id as a parameter and drops `+0x714` works until something
> else reads that field, and a port that keeps `+0x714` but makes the dispatch a normal call changes
> what the handler's return value means (`HT-5`).*

**HT-4 — TWO consumers in TWO layers read this table with the SAME bounds and the SAME emptiness
test, and the invariant is that they agree.** Dispatch subtracts `0x4000`, bounds at `0x166`, loads
`[table + i*8]`, and **returns `−1` on an empty slot**. Availability does the identical arithmetic
and bound, compares the slot against zero, and **reports the order unavailable on an empty slot**.
*So an order cannot be available-but-undispatchable or dispatchable-but-unavailable: emptiness is
one fact with two readings.* **A port that gives either side its own table, or its own bound, breaks
an invariant neither body states.**

**HT-5 — The dispatcher's return IS the handler's return**, because the call is a `jmp`. *There is
no post-processing step in which a reimplementation could normalise a handler's result, and `−1` is
the dispatcher's own value for "out of range or empty" — so a handler returning `−1` is
indistinguishable from a missing one.*

**HT-6 — Before dispatching, a presentation event is posted, and which one depends on the battle
state block.** Event `0x2001` ordinarily; `0x2010` for a party-table unit of type `0x1A` when the
block reached through `02EBF190` has bit 1 of `+0x5AE0`. *That is the block
[the battle-state-block contract](../11-Party/Battle-State-Block/CONTRACT-battle-state-block.md)
covers, so the choice of presentation event depends on save-image state.* *(OPUS block 350 measured the event's
destination: the presentation-event dispatcher stores it in unit `+0x5C` and forwards it to the object at unit
`+0x10`.)*

## 5. State

**Owned:** nothing. **Read:** the table, and the unit's `+0x708`/`+0x714`. **Written:** whatever the
handlers write, which is theirs.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-combo-continuation.md`](CONTRACT-combo-continuation.md) — S-20's only other page-implementing contract |
| **Availability half** | `AiOrder_CheckActionPreconditions`, `CombatAI`'s — `HT-4` |
| **Depends on** | [the battle state block](../11-Party/Battle-State-Block/CONTRACT-battle-state-block.md) — `HT-6` |
| **Not an action** | ids above `0x21E` are orders, and `BattleAction_CheckTargetEligibility` rejects them because an order carries no target |

## 7. State transitions

*id → bound check → slot → empty? return −1 : post the presentation event → tail-call the handler →
the handler re-reads the id from `+0x714`.*

## 8. Script · resource · event interactions

The order vocabulary is AI-side, not authored per action. The presentation event ids `0x2001` and
`0x2010` are posted to the event system.

## 9. Determinism

Deterministic at this level. Whatever the eight handlers do is theirs.

## 10. Failure paths and edge conditions

- An id outside `0x4000`–`0x4166` returns `−1` (`HT-1`).
- An empty slot returns `−1` **and** reports unavailable (`HT-4`).
- A handler returning `−1` is indistinguishable from an empty slot (`HT-5`).

## 11. Observable behaviour

None directly. This is how an AI decision becomes a unit doing something; the visible consequence of
`HT-4` breaking is an order the AI believes it can issue and the unit silently refuses.

## 12. Reproduction formula

Decode the 359 slots and assert **341 non-null, 18 empty**, all `.text`, and the next qword not a
pointer (`HT-1`). Count distinct handlers and assert **eight**, with the largest covering **249**
(`HT-2`). Dispatch an id and assert the handler reads `unit + 0x714` rather than a register (`HT-3`).
Empty a slot and assert **both** consumers change answer (`HT-4`).

## 13. Runtime validation

~~**None.** No experiment executes this dispatch. S-20's runtime cell is not addressed by this
contract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*~~ **Superseded 2026-09-25:** [OPUS block 350](../_index/candidates/s20-opus-replay-handler-table/README.md) executed the dispatcher `00305080` over all 359 ids and past both
ends (4/4): every non-empty id reaches exactly `table[id − 0x4000]`. HT-1 to HT-3, HT-5 and HT-6 hold; the evidence
class is native replay, not live.

## 14. Unresolved

- **What the eight handlers do.** Two are opened here only far enough to establish `HT-3`; the
  page's §8 decodes the locomotion sub-range and the rest is its open work *(answered in part: see Action-Dispatch/battle-action-handler-table.md - AT-3, the `0x4021` wait handler, and AT-4 with section 10, the set/clear-status runs; 2026-10-02, OPUS)*.
- ~~Why 18 slots are empty, and whether any id in those gaps is ever issued.~~ *(answered: AT-2, closed 2026-09-12 - rejected everywhere and never authored, Action-Dispatch/battle-action-handler-table.md section 4; 2026-10-02, OPUS)*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `HT-1` — 359, 341/18, over-determined | the table decoded from its base; the slot past the bound read as `0000000400000002` | 1 |
| `HT-2` — eight handlers, one with 249 | distinct targets counted over the 341 non-null slots and the multiplicities enumerated | 1 |
| `HT-3` — the handler re-reads the id | `003050F1`/`003050FE` shown to set only `rcx`, and `002FDDB0` read in the 249-id handler | 1 |
| `HT-4` — two consumers, one test | both bodies' index arithmetic, bound and emptiness test compared, per [the page](Action-Dispatch/battle-action-handler-table.md) §2 | 1 |
| `HT-6` and the order/action split | [the page](Action-Dispatch/battle-action-handler-table.md) §2 and §11, falsified 2026-09-02 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `HT-1` through `HT-6`. **`HT-2` is the one that
decides whether the port is structurally right** — 359 routines instead of eight. **`HT-3` is the
one that looks like a cleanup**: passing the id as an argument is obviously better and silently
changes which field is authoritative. **`HT-4` is the one no single body states**, so a port written
from either side alone will get it wrong.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CombatAction — internal.** The dispatcher, the table and the handlers are this category's own.
- **CombatAI — PEER, and `HT-4` is the statement.** The availability half belongs to that layer.
  **This contract asserts that it performs the same index arithmetic, the same bound and the same
  emptiness test** — the three things that make the agreement an invariant — and **nothing about the
  id-specific tests that follow them**, which are that layer's.
- **Party — SERVICE, through `HT-6`.** The battle-state block whose `+0x5AE0` bit selects the
  presentation event is that category's; this contract asserts only **which bit is read and which
  event each way selects**.
- **Status_Periodic_Terminal — MECHANICAL, and it is inside the 249-id handler.** That handler
  calls several bodies of that layer. **This contract opens it only far enough to establish `HT-3`
  — that it re-reads `+0x714` — and §14 records what it does as unresolved rather than sketching
  it.**
- **Gameplay and RNG_Random_Selection — MECHANICAL, through the availability half's callees.**
  `HT-4` asserts only that body's index arithmetic, bound and emptiness test, all three before any
  of those calls; *that the availability half goes on to draw the generator is that layer's and is
  not a claim here.*
- **Every other layer reached is MECHANICAL**, through these two bodies' own callees. *Only the
  dispatcher and the 249-id handler are cited by address — the two `HT-3` needs; the other seven
  handlers are counted, not read, and are deliberately not cited.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun.

## 17. Related

- [The battle action handler table](Action-Dispatch/battle-action-handler-table.md) — the mechanism
- [Contract — the battle state block](../11-Party/Battle-State-Block/CONTRACT-battle-state-block.md) — `HT-6`
- [Contract — combo continuation](CONTRACT-combo-continuation.md) — S-20's other page contract

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** HT-1 to HT-4 and HT-6 became checks that fail if the shipping image says otherwise, with the table decoded from its
own bytes. Script: `Tools/analysis-kit/gfz-scripts/falsify_handler_table.py`, output `falsify_handler_table.out`, image
`73461d08…`, 0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| A0 | HT-1 | **survives**: 359 qwords at `01EEC460`: 341 non-null, all inside `.text`; 18 null; the next qword is `0000000400000002` |
| A1 | HT-2 | **survives**: eight distinct handlers. `002FDDA0` × 249, `002FDA60` × 57, `002FDC30` × 25, `002FE660` × 6, and `002FE7D0`, `002FE840`, `002FE8D0`, `002FE910` × 1 each |
| A2 | HT-3 | **survives**: `mov rcx, rbx` / `jmp rdx`; `002FDDA0` re-reads `+0x714` at `002FDDB0` |
| A3 | HT-4 / HT-5 | **survives**: both consumers subtract `0x4000`, bound at `0x166` and read `01EEC460`; the dispatcher's own miss value is `-1` |
| A4 | HT-6 | **survives**: events `0x2001` and `0x2010` in the dispatcher |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity — SERVICE (1 edge).** The movement-order handler `BattleUnit_AdvanceTargetedMovementOrder` `002FDC30` calls `ActorRuntime_GetClass3FloatPair` `00265090`. The handler reads a pair of floats from the actor's class-3 runtime context while it advances the order; the table's dispatch does not depend on it.

**CombatAI — SERVICE and CLIENT (3 edges).** The direct-state handler `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` calls `BattleEnmity_AdjustOtherRelevantCombatants` `00321B00`; the handler `002FE660` calls `AiTargetSelector_ResolveOperandValue` `00321190`; and the availability test `AiOrder_CheckActionPreconditions` `00301830` is called by `AiOrder_EvaluateAndResolveActionTarget` `003014C0`. Two handlers the table dispatches update enmity or resolve a gambit-selector operand, and the AI's order resolution is the caller of this contract's availability test.

**Gameplay — SERVICE (4 edges).** `002FDC30` calls `00312B40`; `00301830` calls `BattleUnit_HasNonPartyEngagementEvidence` `00308040` and `BattleRuntime_GetModeDependentDistanceThreshold` `00309A90`; the dispatcher `BattleUnit_AdvanceExtendedActionState` `00305080` calls `BattleUnit_DispatchActorPresentationEvent` `003299B0`. The availability test asks the domain's engagement and distance-threshold helpers, and the dispatcher raises a presentation event; these are helpers the table's operations use, not table entries.

**Movement — SERVICE (10 edges).** The movement handlers `002FDA60` and `002FDC30` call `BattleUnit_UpdateCombatNavigationStep` `00325BB0`, `BattleLocomotion_ResetPathAndSetTargets` `003291B0` and `BattleLocomotion_IsApproachConstraintActive` `0033A120`, and `002FDA60` also calls `BattleLocomotion_DecodeOrderGoal` `00312730` and `BattleLocomotion_SetApproachAndReferenceTargets` `00319110`; `00301830` calls `00312730` and `0033A120`. Two of the eight handlers are movement orders, so they drive the locomotion layer's path and step functions, and the availability test decodes the order's goal and the approach constraint before an action may run.

**Party — SERVICE (3 edges).** `002FE660` calls `BattleUnit_ResolveByFocusHandle` `0031B7E0`, and `002FE840` calls `BattleUnit_EnterPartyCombatStance` `00313400` and `BattleUnit_ExitPartyCombatStance` `00313480`. One single-id handler switches the unit into or out of the party combat stance, and another resolves the focus unit; the party layer supplies those operations to the table.

**Presentation — SERVICE (1 edge).** `00301830` calls `BattleUnit_ComputePartyBattleStance` `00308130`. The availability test consults the presentation-filed stance computation; it reads a stance value and does not draw anything.

**RNG_Random_Selection — SERVICE (1 edge).** `00301830` calls `RNG_SharedGameplayLCG_NextU32` `00328370`. The availability test draws from the shared gameplay LCG, so evaluating an order can advance the stream that loot and spawn rolls also use.

**Status_Periodic_Terminal — SERVICE (5 edges).** `002FDDA0` calls `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveAllMode0StatusesAndRecompute` `0030E8F0`, `BattleStats_ClearStatusLayer0AndProcessSideEffects` `0030E970` and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`. The handler that 249 ids name executes direct state commands, and changing statuses is one of those commands, done through the status layer's own change and recompute entries.
