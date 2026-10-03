---
contract: The two effect layers — mutate one, rebuild the other, merge both for a formula
category: 10-Status-Periodic-Terminal
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: Status-And-Augment-Layers/two-layer-effect-model.md
entries: ["0030E130", "0030FED0", "003847C0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the three bodies' sizes, a per-body sweep for the two layer displacements
    with the merge as its own positive control, the index arithmetic, the merge loop's bound, and the
    post-merge revocation read in full. **This records checks performed on that date, not the method
    of the original derivation**, which is on the two-layer page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-effect-layers-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the two effect layers

> **Authored 2026-09-21 by FABLE.** S-26's contract cell reads **SCOPE-SHORT** and its binding gap is
> *"operation-scoped; the two-layer model is not stated"*.
> [`CONTRACT-status-write.md`](CONTRACT-status-write.md) is `scope: operation` over
> `0030E360`, *changing a status*; it names the two layers once, in a field list, and states nothing
> about how they relate. **The relation is the system**, and it is what this contract states.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants over three operations.

## 1. Purpose

A battle unit's effects live in **two 128-bit layers that share bit positions and do not share a
namespace**. One is mutated by what happens to the unit; the other is recomputed from what the unit
is wearing and has learned. A formula sees neither — it sees a merge of both, minus a revocation.

## 2. Interface

| operation | body | size | what it owns |
|---|---|---:|---|
| **mutate** | `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (`0030E130`) | 553 B | sets or clears one bit in **either** layer, selected by argument |
| **rebuild** | `BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`) | 1,787 B | recomputes the **derived** layer whole |
| **merge** | `BattleFormula_BuildEvaluationContext` (`003847C0`) | 273 B | produces the merged bitmap a calculator reads |

## 3. Types

```
BattleStatsRecord
  +0x68  u8[16]   mutable status layer    — 128 bits, the effect ids spells and attacks inflict (applier step 14),
                                            not the 32 battle statuses, which are the status words +0x64 / +0x3C
  +0x78  u8[16]   derived augment layer   — 128 bits, rebuilt from equipment, passives, licences

FormulaEvaluationContext
  +0x08  u32      flag word (bits 12, 16 and 23 participate in §4's revocation)   <- corrected 2026-10-02, OPUS: not a flag word; the TARGET's status words +0x64 | +0x3C (0038485F-00384868), so bits 12, 16, 23 are Reverse, Disease, Reflect
  +0x18  u16      ~~a value from the global record at 02EBF188 (+0x55), or 0xFFFF when it is null~~
                  the TARGET's owning unit's byte +0x55; 0xFFFF when the lookup finds no unit; and 0x0000,
                  left from the clear at 003847E5, when the target argument is null  (corrected 2026-09-25)
  +0x1A  u8[16]   MERGED effect bitmap = caster (+0x68 | +0x78), then revoked
```

**Addressing, identical for both layers** (`0030E130`): `byteIndex = n >> 3` (`0030E19C`,
`shr rbx, 3`) and `bit = 1 << (n & 7)` (`0030E1A4`, `and r15d, 7`). The layer is chosen by the
caller, not by the id.

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**L-1 — The rebuild owns the derived layer exclusively and ~~never touches~~ never WRITES the mutable one.** (2026-09-29, OPUS falsification pass 1, `CON-176`)
- ~~Sweeping the three bodies for the two displacements: `0030FED0` reaches `+0x78` at **3** sites and `+0x68` at
  **zero**.~~
- That census counted only the layers' first displacements. Counting every byte of each 16-byte layer on the record
  (`rbx`), the rebuild reads the **mutable** layer twice: `movzx edx, byte ptr [rbx + 0x6c]` / `js` at `0031050B` and
  `00310541`, byte 4, bit 7, **id 39**.
- It reads the derived layer at five sites: the reconcile base `00310303`, and `+0x7C` (the same id 39) at
  `00310513`, `0031052E`, `00310549` and `00310572`.
- Id 39 in **either** layer zeroes the clamp bound for current MP `+0x4C` and for `+0x06`. That is the reading the
  [auto-status rebuild contract](CONTRACT-auto-status-rebuild.md) and the two-layer page's id-39 row already give.
- **What stands:** the rebuild stores nothing into either layer. Its derived changes go through the mutate body only,
  in modes 3 and 1 (`falsify_effect_layers.py` K1, V2).

The census note that follows is kept as dated. **Two of those three sites are not the derived layer** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 341](../_index/candidates/s26-opus-replay-effect-layers/README.md), which executed it 9/9; `003847C0` whole, `0030E242`–`0030E280` and `0031042A`–`0031049C` re-read.)*. `0031043F` and `00310484` address
`[unit + 0x6A0] + 0x78`…`+0x7C`, a different object, copied to or from the record's `+0x40`…`+0x44`. Which way
they copy depends on bit 7 of that block's first byte. The rebuild writes the derived layer only through the
mutate operation, modes 3 and 1, with `flags | 0x202`. *The invariant stands; its census over-counted.* *So a status inflicted by a spell can never be undone by re-equipping, and no equipment
change can clear an inflicted status.* This is the invariant that makes the two layers worth having.

**L-2 — The mutate operation is the only writer of both, and it takes the layer as a parameter.**
`0030E130` reaches `+0x68` at 5 sites and `+0x78` at 6. It is therefore the only place where a
caller's choice decides which namespace a numeric id is interpreted in. **Its side effects key on presence in
EITHER layer** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 341](../_index/candidates/s26-opus-replay-effect-layers/README.md), which executed it 9/9; `003847C0` whole, `0030E242`–`0030E280` and `0031042A`–`0031049C` re-read.)*. After the write it recomputes "the bit is in `+0x68` or `+0x78`"
(`0030E269`–`0030E275`) and enters the handlers only when that differs from the value before (`0030E27B`). So
setting a bit that the other layer already holds writes the layer and runs no handler, and clearing one layer's
copy while the other still holds the bit is equally silent.

**L-3 — The merge is unconditional, whole-range, and lossy.** `003847C0` loops to `0x80`
(`00384851`, `cmp r10d, 0x80`) — **all 128 ids** — testing `[record + 0x68]` at `00384827` and
`[record + 0x78]` at `00384831` and OR-ing into `[ctx + 0x1A]` at `0038484C`. **After it, no consumer
can tell which layer a bit came from**, because the information is not carried anywhere else.

**L-4 — Shared bit positions plus disjoint namespaces produce a real, observable alias.** The layers
index the same bit for different meanings — ~~bit 2 is *Petrify* in the mutable layer and
*AccuracyBoost* in the derived, bit 16 is *Disease* and *Weatherproof*. Because L-3 merges them, **a
unit with Disease satisfies the early-out intended for Weatherproof.**~~ bits 2 and 16 of the mutable layer are effect ids, aliased by L-3 with *AccuracyBoost* and *Weatherproof* of the derived layer. The battle statuses Petrify and Disease are not in either layer: they live in the status words `+0x64` / `+0x3C` (§3), which `003847C0` copies to context `+4` / `+8`, not `+0x1A`, so a unit with the Disease status does not satisfy the Weatherproof early-out unless something writes id 16 into `+0x68`, and no such writer is shown *(corrected 2026-10-02, OPUS: checked at `00384820`–`00384858` and `0030E360`, which has no call to `0030E130`; two-layer-effect-model.md §5, clarified 2026-09-29)*. This is a property of the
engine, not a documentation ambiguity, and it follows from L-3 and L-4 together — which is precisely
why neither operation's own contract can state it.

**L-5 — The merge is not the last word: effect id 15 is revoked afterwards, twice over.** After the
loop, `003847C0` clears bit 7 of the merged bitmap's byte 1 — **id 15** — under two independent
conditions:

```asm
0038488C  call BattleStats_FindOwningBattleUnit      ; 0031B860 -- on the TARGET (4th argument, rdi)
00384894  jne  003848a1
00384896  and  dword ptr [rbx + 8], 0xffffefff       ; target has no owning unit: clear flag bit 12
0038489D  and  byte  ptr [rbx + 0x1b], 0x7f          ;                 and revoke id 15
003848A1  test byte  ptr [rsi], 0x20
003848A4  je   003848bc
003848A6  and  dword ptr [rbx + 8], 0xff7eefff       ; bit 5 set: clear flag bits 12, 16, 23
003848AD  cmp  word  ptr [rbx + 0x18], 0xd
003848B4  mov  word  ptr [rbx + 0x18], bp            ;            reset +0x18 if it was 0xD
003848B8  and  byte  ptr [rbx + 0x1b], 0x7f          ;            and revoke id 15
```

*So a bit present in either layer can still be absent from the context.* **Whose layers, and whose unit** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 341](../_index/candidates/s26-opus-replay-effect-layers/README.md), which executed it 9/9; `003847C0` whole, `0030E242`–`0030E280` and `0031042A`–`0031049C` re-read.)*:
the merged bits come from the **third** argument, the caster's record (`00384803`–`00384858`). The owner test and
context `+8` read the **fourth**, the target (`0038485A`–`00384896`). So "a record with no owning unit" is the
target: a caster's id 15 is revoked because of the target it is aimed at. An implementation that
treated the merged bitmap as `A | B` would grant id 15 to a record with no owning unit — a case the
engine is explicit about refusing.

**L-6 — The derived layer is reconciled, not accumulated.** The rebuild computes a desired bitmap
from the accepted equipment, passives and licences and then **adds what is missing and clears what is
stale** against the current `+0x78`, so repeating it with unchanged inputs is a no-op. ~~*This is taken
from [the two-layer page](Status-And-Augment-Layers/two-layer-effect-model.md) §2 and is the one
invariant here not re-measured for this contract; it is stated as that page's reading, not as a fresh
measurement.*~~ **Measured 2026-09-29 (OPUS falsification pass 1, V7).** The loop at
`00310310`–`00310336` forms `diff = desired XOR current`, stores `diff & desired` (to add) and `diff & current`
(to remove) to two stack buffers, and the id loop to `0x80` calls the mutate body in mode 3 for each add and mode 1
for each remove.

## 5. State

**Owned:** `+0x78` by the rebuild alone (L-1). **Shared:** `+0x68`, written by the mutate operation
and read by the merge. **Derived and transient:** the context's `+0x1A`, valid only for the formula
evaluation it was built for. **Read, never written here:** the equipment definitions, the authored
passive and licence records~~, and the global at `02EBF188` whose `+0x55` supplies context `+0x18`~~.
**`02EBF188` is WRITTEN here** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 341](../_index/candidates/s26-opus-replay-effect-layers/README.md), which executed it 9/9; `003847C0` whole, `0030E242`–`0030E280` and `0031042A`–`0031049C` re-read.)*: whenever the target is non-null, the merge stores the target's owning
unit there (`00384870`) before reading its `+0x55`. The rip-relative census of that global finds 93 stores in
many functions (`tools/ripscan.py`). It is a shared "current target unit" slot, not a read-only input.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-status-write.md`](CONTRACT-status-write.md) — the *operation*; ~~it calls the mutate body and~~ it does not call the mutate body *(corrected 2026-10-02, OPUS: checked at `0030E360`, whose call targets do not include `0030E130`; two-layer-effect-model.md §5)* and states nothing about the layers |
| **Sibling** | [`CONTRACT-periodic-tick.md`](CONTRACT-periodic-tick.md) — reads both layers to decide expiry, and is the clearest consumer of L-3 |
| **Downstream** | every formula calculator, through the merged bitmap |

## 7. State transitions

A bit goes `absent → present` in the mutable layer only through the mutate operation, and in the
derived layer only through a rebuild whose desired bitmap contains it. It goes `present → visible to a
formula` through the merge, **unless** it is id 15 and L-5's revocation fires.

## 8. Script · resource · event interactions

The derived layer's inputs are authored: equipment definitions (one raw augment id byte each, with a
sentinel meaning none) and passive/licence records importing up to eight numeric effect ids each. The
mutable layer's inputs are runtime. **No authored file names a layer**, which is why the namespace map
is reconstructed rather than read.

## 9. Determinism

All three operations are deterministic. No generator is drawn in any of them.

## 10. Failure paths and edge conditions

- A record with **no owning battle unit** loses id 15 and context flag bit 12 (L-5).
- ~~A null `02EBF188` leaves context `+0x18` as `0xFFFF` rather than faulting.~~ A target with no owning unit
  leaves context `+0x18` as `0xFFFF` rather than faulting. A null target leaves it `0x0000` (§3, corrected
  2026-09-25 on OPUS block 341).
- An id at or above 128 is outside the merge loop's range and cannot reach a formula.
- Mutating a bit that is already in the requested state is a no-op for the layer; whether the side
  effects still run is the *operation* contract's subject, not this one's.

## 11. Observable behaviour

A character wearing an Agate Ring and a character afflicted with Disease are, to the weather-scaling
early-out, the same character. Re-equipping never cures a status, and a status never disables an
equipment augment.

## 12. Reproduction formula

Set bit *n* in one layer, clear it in the other, build a context, and assert the merged bit is the OR;
then repeat for *n = 15* with no owning unit and assert it is **clear**. Run the rebuild twice with
unchanged equipment and assert `+0x78` is unchanged and `+0x68` unwritten. It is read: id 39 gates the MP clamp
(`CON-176`).

## 13. Runtime validation

~~**None.** No experiment executes these three bodies. S-26's runtime cell reads **NOT MET** and this
contract does not change that; the gap is execution and it is ASTRA's and SWE2-ORACLE's. *Stated
rather than left blank so a CONTRACT READY header is not mistaken for evidence of execution.*~~ **Superseded
2026-09-25**: OPUS block 341 executed the three bodies (9/9). The four readings it raised are ruled in §3, L-1,
L-2, L-5 and §5. The evidence class is native replay, not live.

## 14. Unresolved

- ~~What the flag bits 12, 16 and 23 of context `+0x8` mean,~~ *(answered: see the-thirty-two-statuses.md §4 — context `+0x8` is the target's status words `+0x64` / `+0x3C`, `0038485F`–`00384868`, so bits 12, 16 and 23 are Reverse, Disease and Reflect; 2026-10-02, OPUS)* and what effect id 15 is named.
- What `byte [rsi]` bit 5 is in L-5's second condition.
- The rest of the namespace map beyond the three bits the page establishes.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| The three bodies' sizes, 553 / 1,787 / 273 | read from the function table of the authority image | 1 |
| L-1, L-2 — the per-body layer ownership | all three bodies swept for `+0x68` and `+0x78`, **with the merge as positive control** (it must show both; it does) — so the rebuild's zero at `+0x68` is ~~a measurement~~ **a measurement of the exact displacement only; a byte-range sweep finds the rebuild's two id-39 reads at `+0x6C` and no store** (`CON-176`; `falsify_effect_layers.py` K1, V2) | 1 |
| L-3 — 128 ids, both layers, one OR | the loop read in full: bound `0x80` at `00384851`, the two `test`s and the `or` | 1 |
| L-5 — the post-merge revocation | the tail of `003847C0` disassembled; both conditions and both `and …, 0x7f` sites | 1 |
| The index arithmetic | `shr rbx, 3` at `0030E19C`, `and r15d, 7` at `0030E1A4` | 1 |
| L-4's namespace map and L-6 | [the two-layer page](Status-And-Augment-Layers/two-layer-effect-model.md), read from the shipping bytes and re-verified 2026-09-02 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on L-1 through L-6, and L-5 is the one most likely to
be missed: the merged bitmap is not `A | B`.

## 16a. Crossings into other layers (FABLE, 2026-09-21)

Nine layers are reached, and **every one of them through four addresses** — the three operation
entries and the owning-unit accessor `0031B860` that L-5 consults. *No further address is cited in
this note: each of those callers and callees is a hub, and naming one imports its whole edge set into
this contract for a one-line remark.*

- **CombatFormula — SERVICE, and the only real relationship.** `003847C0` belongs to that layer and
  is how it reads this one. Stated in §2 and §6; it is the contract's subject.
- **Status_Periodic_Terminal — internal.** `0030E360`, this category's own status write, ~~is the
  principal caller of the mutate operation~~ does not call the mutate operation; its callers are `003112F0` (applier step 14), `002FDDA0` and `0030FED0` *(corrected 2026-10-02, OPUS: checked at `0030E360`)*.
- **CombatAction, Gameplay, Spawn_Encounter_Lifecycle, Party, Rewards_Progression_Economy —
  MECHANICAL.** Each appears only as a *caller of the rebuild or the mutate operation*, or as a
  callee of one of them. **That fan-in is itself a fact this contract asserts**: L-1 holds no matter
  who calls, which is what makes the derived layer safe to rebuild from anywhere.
- **CombatAI, Movement — MECHANICAL.** Reached as one callee of the mutate operation and as further
  callers of the owning-unit accessor. Shared helpers, not shared responsibility.
- **ActorEntity — MECHANICAL.** `0031B860` resolves a record's owning unit through that layer, and
  the status write reaches one of its bodies. One accessor consulted for L-5's predicate; nothing of
  this subsystem's responsibility is shared with it.

## 17. Related

- [The two-layer effect model](Status-And-Augment-Layers/two-layer-effect-model.md) — the mechanism
- [Contract — the status write](CONTRACT-status-write.md) — the operation that mutates a layer
- [Contract — the periodic tick](CONTRACT-periodic-tick.md) — a consumer of both layers
- [The thirty-two statuses](the-thirty-two-statuses.md)

## Falsification pass 1 — 2026-09-29 (OPUS): the model survives; the rebuild reads the mutable layer

**Attack.** §2, the addressing, L-1 to L-3, L-5, L-6 and §5 became checks at their instructions. The layer censuses counted
every byte of each 16-byte layer over each body's chained extent. Script:
`Tools/analysis-kit/gfz-scripts/falsify_effect_layers.py`, output `falsify_effect_layers.out`, image `73461d08…`,
0 BROKEN. OPUS block 341's execution (9/9) is not repeated.

| # | Clause attacked | Result |
|---|---|---|
| V0 | §2 | **survives**: 553 / 1,787 / 273 B; each chain union equals its catalogue size |
| V1 | addressing and layer choice | **survives**: `shr 3` / `and 7`; mode 0 clears `+0x68`, 1 clears `+0x78`, 2 sets `+0x68`, 3 sets `+0x78` |
| K1 | L-1 "never touches the mutable one"; its census `+0x78` at 3, `+0x68` at 0 | **refuted** (`CON-176`): two reads of mutable `+0x6C` and four of derived `+0x7C`, both id 39, gate the MP and `+0x06` clamps |
| V2 | L-1's write side | **survives**: no store into either layer; the reconcile loop writes stack buffers; derived changes go through mode 3 / mode 1 with flags \| 0x202 |
| V3 | L-2 | **survives**: 5 and 6 sites; the either-layer recompute before the handlers |
| V4 | L-3 | **survives**: loop to `0x80`, both `test`s, one `or` |
| V5 | L-5 | **survives**: both revocation conditions exactly as quoted |
| V6 | §5 | **survives**: `00384870` stores `02EBF188` |
| V7 | L-6 | **now measured**: diff = desired XOR current; add with mode 3, remove with mode 1 |

Corrected in place: L-1, its §15 row, §12, and L-6's "not re-measured". The consumer record is
`_index/candidates/effect-layers-falsification-pass-1-0929/`.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names the edges it deliberately left unnamed.*

**ActorEntity — SERVICE (3 edges).** The owning-unit accessor `BattleStats_FindOwningBattleUnit` `0031B860` walks that layer's roster through `BattleUnit_GetSlotCount` `00236850` and `BattleUnit_GetBySlotIndex` `00236820`; the status write `0030E360` calls the ActorEntity body `00300FC0`, which cancels the unit's current action or releases its target relation. L-5's owner lookup is a roster scan owned by that layer, and some status writes reach that layer's unit-release body.

**CombatAI — SERVICE (1 edge).** The mutate operation `0030E130` calls `GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0` after a bit change: for bits `0x68` to `0x71` it passes `+1` when the bit is set and `-1` when cleared (`0030E303`–`0030E317`). Setting or clearing one of those ten effect bits changes how many gambit entries the record may use.

**CombatAction — CLIENT and SERVICE (11 edges).** The direct-state order handler `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` calls the mutate `0030E130`, the rebuild `0030FED0` and the status write `0030E360`; `BattleUnit_AdvanceStandardActionState` `00304850` and `BattleSpecialSequence_CommitAccumulatedTargetHp` `0030EB10` call `0030E360`; `BattleAction_EvaluateTargetPreviews` `00303830`, `BattleAction_EvaluateTargetPreviewRecursive` `00303A00`, `BattleAction_CheckDefinitionCategoryAvailability` `003060E0` and `003879C0` call `0031B860`; `0030E360` calls the eligibility predicates `0030B8E0` and `0030B9B0`. The action layer is a caller of all three operations (section 16a's L-1 point: the derived layer is safe to rebuild from any caller), and the status write consults the action layer's two suppression predicates.

**CombatFormula — SERVICE and CLIENT (51 edges).** The merge `BattleFormula_BuildEvaluationContext` `003847C0` is that layer's and is called by `BattleFormula_EvaluateTargetPreview` `00385680` and `BattleFormula_ResolveTargetResult` `00385F60`; `0031B860` is called by 35 formula bodies (among them `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`, `BattleStats_ModifyHPAndProcessLethalState` `00300530`, `BattleStats_ReconcileCurrentHpToEffectiveMaximum` `0030F340`, `BattleFormula_ApplyTargetResult` `003112F0`, `003847C0`, `00384E50` and `00384F40`); the result sink `003112F0` calls `0030E130`, `0030E360` and `0030FED0`, and `0030E360` and `0030E130` call it back; `0030E360` and `0030E130` call the status builders `BattleFormula_BuildInactiveStatusTransitionResult` `00386A50`, `BattleFormula_BuildConditionalStatusHpTransitionResult` `00386A70` and `BattleFormula_BuildRandomElementStatusTransitionResult` `00386AE0`; `00300530` calls `0030E360`; the rebuild calls `002FEF30` and `0031B860`. This is the contract's subject (section 16a): the formula applies results by calling the mutate and status write, and reads both layers only through the merge.

**Gameplay — SERVICE (4 edges).** `0030E130` and `0030FED0` call `BattleEncodedId_IsValidForClass` `00322C50`; `0030E360` calls `BattleUnit_UpdateEngagementStateFlag` `00307D10` and `BattleUnit_DispatchActorPresentationEvent` `003299B0`. The operations validate ids with the shared class test, and a status write refreshes the unit's engagement flag and dispatches a presentation event.

**Items_Equipment_Shops_License — CLIENT (8 edges).** `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, `BattleStats_SetEquipmentSlotDirect` `0031A630` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` each call `0030FED0` and `0031B860`. Equipping an item or setting a licence node is what triggers a rebuild of the derived layer, which is where equipment and licence effects live.

**Movement — MECHANICAL (2 edges).** The locomotion bodies `0033CB10` and `0033D890` call `0031B860`. They look up a stats record's owning unit with the same accessor; neither touches an effect layer through it.

**Party — CLIENT (1 edge).** The `resetJobs` body `00328BD0` calls `0030FED0`. A party job reset rebuilds the derived layer once for the record it resets.

**Rewards_Progression_Economy — CLIENT and SERVICE (5 edges).** The level-advance bodies `0030C470` and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` call `0030FED0`, and `0030C650` and `Reward_ComputeExperienceForRecipient` `002F8BB0` call `0031B860`; `0030E360` calls `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280`. A level change rebuilds the derived layer, experience is credited through the same owner lookup, and a lethal status write hands off to the defeat-reward path.

**Spawn_Encounter_Lifecycle — CLIENT (1 edge).** `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `0030FED0`. A newly activated spawn gets its derived layer built once.

**WorldAreaField — DEPENDENCY (1 edge).** `0030E360` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`. The status write consults the active field record's action-permission bit, so part of the status write's behaviour depends on that field flag (which branch it gates is not read here).
