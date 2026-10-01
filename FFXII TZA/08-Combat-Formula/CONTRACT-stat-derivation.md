---
contract: Derive a unit's effective stats — two sources, one writeback, one clamp block
category: 08-Combat-Formula
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: where-a-stat-number-comes-from.md
entries: ["002FEF30"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the body's extent, every cap immediate located in its real form, the
    writeback block read in full, the effect-layer test sites swept with the page's known pair as a
    positive control, and the head and tail read in order. **This records checks performed on that
    date, not the method of the original derivation**, which is on the stat page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-stat-derivation-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — stat derivation

> **Authored 2026-09-21 by FABLE.** S-24's binding gap is *"the rebuild is contracted; stat
> derivation itself is not"*. The system's index row names three pages and one contract, and that
> contract — [`CONTRACT-auto-status-rebuild.md`](../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) —
> covers the auto-status rebuild. **Where a stat number comes from had no contract at all.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants, and the first three are about two sources meeting at one block of code.

## 1. Purpose

Produce a unit's **effective stats** — the numbers every formula reads — from everything that
contributes to them: the unit's own definition, its level or its area's battle tables, its five
equipment slots, and its statuses. One function does all of it, for party characters and for
enemies alike, by two source paths that never overlap.

## 2. Interface

| | |
|---|---|
| **Entry** | `BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`), **2,859 bytes, 735 instructions** |
| **Output** | the effective-stats block at `rsi` — `[rsi]` the main value, `[rsi+4]` a word, then the byte fields |
| **Side effects** | may cancel the unit's in-flight action (`003105D0`); ~~always~~ ends `call 00307D10` (`002FFA40`) **only when the tail runs** (D-7) *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 305; bytes re-read.)* |

## 3. Types

Sources, by path (selected per D-1):

| | party path | area / enemy path |
|---|---|---|
| base | growth definitions at registry slot `02EBF130`, indexed by the type byte `+0x04` | four `.ard` records resolved by type byte, then by `+0x22` / `+0x24` out of the first, then one by its `[+0x00]` |
| shape | `float` fields converted to `int`, plus the level at `+0x08` | `growth[col] × (rec[+0x1C2] − rec[+0x88]) + base[col] + own[col]` |

Contributors common to both paths: five equipment slots, each validated by
`BattleEncodedId_IsValidForClass(6, id)` (`00322C50`) and classified by `0031E9A0`; and the statuses
held in **either** effect layer.

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**D-1 — One byte selects between two complete, non-overlapping stat sources, and nothing else
does.** `rec[+0x05]` chooses the growth-definition path or the `.ard` path; a party character and a
Marlboro are computed by different code from different files, in one function. *A tool that assumes
one layout writes nonsense into the other.*

**D-2 — Both paths converge on one writeback block, and every output is clamped there.** The block
runs `002FF7B1`–`002FF8D6`. Nothing is clamped where it is computed; the caps are register immediates
inside that block — `0x270F` at `002FF7BD`, `0x3B9ACA00` at `002FF7C3`, `0x7FFF` at `002FF7F5`,
`0x3E7` at `002FF817`, `0x63` at `002FF829`, `0xFF` at `002FF8D6`. **This is what makes the two paths
comparable at all**, and it is why the column map on the stat page could be derived by pairing each
value with the cap it lands on.

**D-3 — The party/foe cap is one `cmove`, not two code paths.**

```asm
002FF7BB  test  edi, edi
002FF7BD  mov   r8d, 0x270f          ; 9,999
002FF7C3  mov   eax, 0x3b9aca00      ; 1,000,000,000
002FF7C8  cmove eax, r8d             ; one flag picks the cap
002FF7CF  cmp   r14, rax
002FF7D2  cmovg r8, rax
002FF7E2  mov   dword ptr [rsi], r8d
```

*The famous 9,999 is not a party-side code path; it is the value a conditional move selects.*

**D-4 — The 32,767 band cap is a SECOND WRITE of the same slot, not a third cap.** Immediately after
`002FF7E2` stores the main value, a separate condition can compute and store it again:

```asm
002FF7E5  cmp   dword ptr [rsp + 0x5c], ebp
002FF7E9  je    002ff808              ; condition absent -> keep the first store
002FF7F5  mov   r9d, 0x7fff
002FF801  cmovg r15, r9
002FF805  mov   dword ptr [rsi], r15d ; the SAME slot, overwritten
```

> **Corrective.** [The stat page](where-a-stat-number-comes-from.md) lists 32,767 in a table of caps
> alongside 9,999 and 1,000,000,000, which reads as three alternatives. It is not: 9,999 and
> 1,000,000,000 are alternatives to each other, and **32,767 belongs to a conditional re-computation
> that overwrites whichever of them was just written.** An implementation that treated it as a third
> branch of one clamp would produce the right number by luck and the wrong intermediate.

**D-5 — Statuses count from *either* effect layer, at three independent sites.** Sweeping this body
for the two layer displacements returns **three pairs** — `002FF5CA`/`002FF5D1`,
`002FF668`/`002FF66F`, `002FF708`/`002FF70F` — one per authored status list (16, 16 and 12 ids).
**This subsystem is therefore a direct consumer of
[the effect-layer contract's](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md) L-3 and L-4**,
and the consequence is concrete: because the two layers share bit positions and are both tested here,
**the Disease / Weatherproof alias reaches stat numbers**, not only formula early-outs.

**D-6 — One authored boolean gates a base term and its matching equipment term together.** Bits 0 and
1 of the definition's `+0x15` select whether the block and magick-evade values come from the `.ard`
row's own bytes or from the shield, **and** suppress the corresponding equipment contribution. *One
flag, two sources, in two different parts of the function — which is precisely the kind of statement
a contract over "the equipment pass" alone could not make.*

**D-7 — A stat rebuild is not side-effect-free, and its tail ~~always runs~~ is conditional.** When the party side is
rebuilt and two specific flag bits changed, the unit's in-flight action is cancelled through
`003105D0`; ~~and whatever path was taken, the body ends by clearing runtime fields~~ *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 305; bytes re-read.)* the tail
does three things:
- clears runtime fields (`002FFA14`, `002FFA22`);
- sets `[unit + 4]` bit `0x200000` at `002FFA38`;
- calls `00307D10` at `002FFA40`.

It runs **only when all three guards pass**: `edi == 0` (`002FF970` / `jne 002FFA45`), `[rsp + 0x64] != 0`
(`002FF978` / `je`), and a status-word change in bits `0x8000020` (`002FF982`–`002FF98E`). On any other path
the body returns 0 at `002FFA45` with none of these writes. EXP-103's tail-skip cases measure the skip. **Recomputing a stat can interrupt what a character was
doing.**

## 5. State

**Written:** the effective-stats block at `rsi`, and — in the tail only — the unit's `+0x4`,
`+0x6B0`, `+0x74C`, `+0x750` and `+0x788`. **Read, never written:** the growth definitions at
`02EBF130`, the four `.ard` records, the equipment rows, the three authored status-id lists and both
effect layers.

## 6. Relationships

| | |
|---|---|
| **Consumes** | [the two effect layers](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md) — D-5 |
| **Sibling** | [the auto-status rebuild](../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) — the other half of S-24 |
| **Shares a quantity** | the foe path's `rec[+0x1C2] − rec[+0x88]` is the same difference the experience formula multiplies by, read independently in two functions |
| **Downstream** | every formula that reads an effective stat |

## 7. State transitions

`definition + level + equipment + statuses → intermediates → one clamped writeback`. The main value
may transition twice within one call (D-4). No stat can leave the block negative: each clamp is
two-sided, the floor taken from a register rather than an immediate.

## 8. Script · resource · event interactions

Authored inputs only: the growth definitions, the `.ard` area battle tables (the loader page covers
their binding), the equipment rows, and the three status-id lists. **The grouping of the 44 flat-bonus
statuses into three lists is data** — moving an id between lists changes which stat it raises without
touching an instruction.

## 9. Determinism

Fully deterministic. No generator is drawn: a sweep of this body for a call into the generator family
returns nothing, and its eight distinct callees are `0031B860`, `0020E600`, `002F8E50`, `002F9180`,
`00322C50`, `0031E9A0`, `003105D0` and `00307D10`.

## 10. Failure paths and edge conditions

- An equipment id failing `BattleEncodedId_IsValidForClass(6, id)` contributes nothing and is not an
  error.
- A negative intermediate is written as the floor, never as a negative.
- A `.ard` row with `+0x15` bit 1 set and its own bytes zero has **no shield-side evasion at all** —
  authored, not a bug, and `CB-9` identifies the 30 rows.
- `+0x15` **bit 4 has no consumer anywhere in `.text`**; a reimplementation may carry it and cannot
  diverge on it.

## 11. Observable behaviour

A character's Strength and a Marlboro's are edited in different files because they are computed from
different tables. A character's damage stops rising at 9,999 where an enemy's does not. And a
character who is diseased gains whatever a Weatherproof-bearing character gains, because both are bit
16 in a merged bitmap this function tests.

## 12. Reproduction formula

Drive both paths with known definitions and assert every output lands inside its cap; set the band
condition and assert `[rsi]` is written twice with the second value surviving; set a status in the
derived layer only and assert the flat bonus still applies.

## 13. Runtime validation

~~**None.** No experiment executes `002FEF30`.~~ **Superseded 2026-09-25:** EXP-103 and EXP-104 execute
`002FEF30`, including the tail-skip cases D-7 now states. [OPUS block 342](../_index/candidates/s24-opus-replay-stat-derivation/README.md) (7/7) executed §14's four conditions.
S-24's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*

## 14. Unresolved

- [x] ~~What `edi` is at `002FF7BB` and `[rsp+0x5C]` at `002FF7E5` — the two conditions selecting the cap
  and triggering the re-write. Named here as conditions, not as meanings.~~ **ANSWERED** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 342](../_index/candidates/s24-opus-replay-stat-derivation/README.md), which executed it 7/7; `002FEF6E`–`002FF026`, `002FF5A7`, `002FF796`–`002FF7E9` and `002FF982`–`002FF98E` re-read.)*.
  **`edi` is the record's class byte `+0x05`**, loaded at `002FF796` from the copy made at `002FEFFB`; a null record
  stores `0xFF` (`002FF018`). The cap is **9,999** when it is 0 (party class) and 1,000,000,000 otherwise.
  **`[rsp+0x5C]` is 1 exactly when `+0x05 == 0` and the kind `+0x04` is in `0x1B`–`0x27`** (`002FF007`–`002FF011`).
  That band is the thirteen Espers
  ([the type-id partition](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md)).
  So D-4's second store is the **summon** case. OPUS measured kinds `0x1B`, `0x1E` and `0x27` storing 9,999 and
  then 32,767, while `0x00` and `0x1A` store once. *That the band is the Espers is the partition page's reading,
  and what the main value means on screen is not claimed here.*
- [x] ~~Which two flag bits trigger D-7's action cancel; the stat page records the mask, not the meaning.~~
  **The bits are answered; their meaning is not** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 342](../_index/candidates/s24-opus-replay-stat-derivation/README.md), which executed it 7/7; `002FEF6E`–`002FF026`, `002FF5A7`, `002FF796`–`002FF7E9` and `002FF982`–`002FF98E` re-read.)*. The test is on bits **5 and 27** of `+0x3C` (mask
  `0x8000020`, `002FF989`), taken as the XOR of the value before and after the rebuild. D-7's gate `[rsp+0x64]` is 1
  exactly when the output argument is null and the record's owning-unit lookup finds a unit (`002FEF6E`–`002FEF89`).
- [x] ~~The floor register's value is taken from the stat page's reading rather than re-measured here.~~
  **Re-measured** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 342](../_index/candidates/s24-opus-replay-stat-derivation/README.md), which executed it 7/7; `002FEF6E`–`002FF026`, `002FF5A7`, `002FF796`–`002FF7E9` and `002FF982`–`002FF98E` re-read.)*: the floor is `r15d = 1` (`002FF5A7`, compared at `002FF7B1`), and OPUS measured it.
  OPUS also found that for some party types a large `+8` makes the per-type computation return a value `<= 0`,
  so the result lands on the floor (type `0x06` at `0x7FFFFFFF` returns `-1`).

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| The body is 2,859 bytes / 735 instructions | the function table of the authority image | 1 |
| D-2, D-3, D-4 — one writeback block, the `cmove` cap, the second store | every cap immediate located in its real form (`mov reg, imm`, **not** `cmp reg, imm` — a search for the `cmp` form returns zero sites for all eight), then the block read in full | 1 |
| D-5 — three layer-test pairs | the body swept for both layer displacements, **with the stat page's known pair `002FF708`/`002FF70F` as a positive control**; it returns that pair and two more | 1 |
| D-7's tail | the last sixteen instructions read in order | 1 |
| §9's determinism claim | the callee list enumerated from the body; no generator among them | 1 |
| D-1, D-6, the column map, `CB-9` and `CB-10` | [the stat page](where-a-stat-number-comes-from.md), read from the shipping bytes and extended 2026-09-07 and 2026-09-12 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on D-1 through D-7. **D-4 is the one to test first**:
the main value is stored, and then conditionally stored again with a different cap.

## 16a. Crossings into other layers (FABLE, 2026-09-21)

Nine layers are reached, **all of them through this body's eight callees** and their own fan-in. *No
caller or further callee is cited by address below: each is a hub, and naming one imports its whole
edge set into this contract for a one-line remark.*

- **CombatFormula — internal.** This body is that category's own.
- **Items_Equipment_Shops_License — SERVICE.** `00322C50` validates every equipment id and
  `0031E9A0` classifies the row. The equipment contribution is a stated part of this subsystem and
  the dependency is in §2 and §3.
- **Status_Periodic_Terminal — SERVICE.** Both effect layers are read here; that is D-5, stated in §6.
- **ActorEntity, CombatAction, Gameplay, Movement, Presentation, WorldAreaField, UI,
  Rewards_Progression_Economy, CombatAI — MECHANICAL.** Every one is reached either as a *callee of
  one of this body's eight callees* or as *another caller of them*. `00322C50`, the encoded-id
  validator, is the widest of these and is consulted by most combat and movement code; `003105D0`
  and `00307D10` reach further layers when they run. **Fan-in and fan-out on shared helpers, not
  shared responsibility** — this contract asserts nothing about any of them beyond what §2 records.

## 17. Related

- [Where a stat number comes from](where-a-stat-number-comes-from.md) — the mechanism
- [Contract — the two effect layers](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md) — D-5's supplier
- [Contract — the auto-status rebuild](../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) — S-24's other half
- [The formula scratch block](Scratch-Block/the-formula-scratch-block.md) — where the four evasions are spent

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** D-2 to D-5 and D-7 became checks that fail if the shipping image says otherwise. Script:
`Tools/analysis-kit/gfz-scripts/falsify_stat_derivation.py`, output `falsify_stat_derivation.out`, image `73461d08…`,
0 BROKEN. The tail-skip behaviour is EXP-103's and OPUS block 305's executions, and is not re-run.

| # | Clause attacked | Result |
|---|---|---|
| D0 | §2 size | **survives**: 2,859 B, 735 instructions |
| D2 | D-2 the six caps | **survives**: `0x270F`, `0x3B9ACA00`, `0x7FFF`, `0x3E7`, `0x63` and `0xFF` at the cited sites |
| D3 | D-3 | **survives**: `test edi, edi` / `cmove eax, r8d`; the store at `002FF7E2` |
| D4 | D-4 | **survives**: `cmp [rsp+0x5c], ebp` / `je 002FF808`, then `cmovg r15, r9` and a second store to `[rsi]` at `002FF805` |
| D5 | D-5 | **survives**: all three sites read the same pair of layer displacements, `+0x68` and `+0x78` |
| D7 | D-7 | **survives**: `003105D0` is called; the tail's guards (`edi`, `[rsp+0x64]`, the `0x8000020` change) precede the writes, the `0x200000` bit at `002FFA38` and `call 00307D10` at `002FFA40` |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's dispositions stand; its heading is numbered, so the crossings gate does not read it, and this section names the far ends it deliberately left out. Every edge below goes through the rebuild `002FEF30` or through five of its eight callees — `BattleStats_FindOwningBattleUnit` (`0031B860`), `BattleEncodedId_IsValidForClass` (`00322C50`), the equipment-row classifier `0031E9A0`, `BattleUnit_CancelAndResetCurrentAction` (`003105D0`) and `BattleUnit_UpdateEngagementStateFlag` (`00307D10`).*

**ActorEntity — SERVICE and CLIENT (13 edges).** `0031B860` and `003105D0` call `BattleUnit_GetBySlotIndex` (`00236820`) and `BattleUnit_GetSlotCount` (`00236850`); `003105D0` is called by `BattleUnit_ResetStateForReuse` (`00236A60`), `BattleUnit_TeardownAndDespawn` (`00300E40`), `00300FC0` and `BattleGroup_RefreshFourActorDefinitions` (`003266C0`); and `00322C50` is called by `BattleUnit_FindByDefinitionSelector` (`002367A0`), `BattleUnit_ApplyUnitDefinition` (`0023A570`), `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`), `003266C0` and `BattleSlotMap_InitializeMappingClasses` (`00329CC0`). The rebuild reaches that layer only through the unit-slot walk that finds a stats record's owner; the other edges are actor reuse, teardown and definition install using the same action cancel and id validator.

**CombatAI — CLIENT, OUT-OF-SCOPE (11 edges).** `BattleUnit_UpdateCombatFrame` (`00308610`) calls `003105D0`, and `00322C50` is called by `AiOrder_EvaluateTargetSelector` (`00301AD0`), the enmity family (`BattleEnmity_ReadForCombatantId` `003215C0`, `BattleEnmity_WriteForCombatantId` `00321850`, `BattleEnmity_PropagateToPerceivingFoes` `003219D0` and four more) and `GambitConfig_ClassifyActionTargetPairCompatibility` (`00327A10`) and `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` (`00327CB0`). The AI and enmity code validates combatant and gambit ids with the same validator and the combat frame cancels actions with the same body; none of it reads the effective-stats block this contract writes.

**CombatAction — SERVICE and CLIENT (16 edges).** `002FEF30` calls `003105D0` (D-7), which calls `BattleAction_RefundReservedExecutionResources` (`00300280`), `BattleAction_ReleasePresentationSlot` (`0030C970`) and `BattleUnit_ReleaseTargetRelationAndActionState` (`00310780`), and which `BattleUnit_CommitAction` (`0030F760`) also calls; `0031B860` is called by `BattleAction_EvaluateTargetPreviews` (`00303830`), `BattleAction_EvaluateTargetPreviewRecursive` (`00303A00`), `BattleAction_CheckDefinitionCategoryAvailability` (`003060E0`) and `003879C0`; `00322C50` by `BattleAction_CheckActionAvailabilityReason` (`002FFCF0`), `BattleAction_GetPrimaryRangeScalar` (`00309300`) and five more action bodies. D-7's cancel is that layer's own body — it refunds the reserved cost and releases the action's slot and target relation — so a stat rebuild can undo a queued action; the rest are action code using the same lookup and validator.

**Gameplay — SERVICE and DEPENDENCY (10 edges).** `002FEF30` calls `00307D10` and `00322C50`, both filed to that label; `00307D10` calls `BattleUnit_HasActiveEngagementEvidence` (`00307CE0`), `BattleUnit_HasRelationshipClass2PlusInTrackedActorList` (`0030B050`) and `BattleUnit_IsPointerInEngagementRecordPools` (`0030BF20`); `003105D0` calls `BattleTargetBuffer_ResetPreservingFlag0` (`00316CF0`); `0031E9A0` calls `BattleDefinition_MapByte9ToRuntimeCategory` (`0031E9F0`) and folds its nine runtime categories into classes 0 to 3; and `0031C5D0` (an 8,136-byte body) and `BattleSlotMap_ResolveMappedBattleSlot` (`0031B9F0`) call the classifier or the validator. The equipment contribution depends on that category mapping and on the validator accepting each slot's id (section 3), and the D-7 tail recomputes the unit's engagement flag from the engagement tests; nothing in this contract depends on the other callers.

**Items_Equipment_Shops_License — CLIENT and DEPENDENCY (18 edges).** `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` (`0030A4E0`) calls `002FEF30`; `0031B860` is called by `BattleStats_SetEquipmentSlotByStatsIndex` (`0031A410`), `BattleStats_SetEquipmentSlotByMappedId` (`0031A510`), `BattleStats_SetEquipmentSlotDirect` (`0031A630`) and `BattleStats_SetLicenseNodeStateAndApplySideEffects` (`00323910`); and `00322C50` by thirteen equipment and licence bodies, among them `Equipment_CheckItemEligibleForSlot` (`00317930`), `BattleStats_HasRequiredLicenseForEquipment` (`00323C60`) and `BattleStats_CheckLicenseNodeAcquireReason` (`00323D10`). The candidate-loadout evaluator runs this very rebuild to preview stats, the slot setters find the owning unit the same way, and equipment rows are this contract's input (section 3); licence checks share only the validator.

**Movement — SERVICE and CLIENT (6 edges).** `003105D0` calls `BattleLocomotion_ResetPathAndSetTargets` (`003291B0`) and `0033C9B0`, so cancelling an action also resets the unit's path; `0031B860` is called by `0033CB10` and `0033D890`, and `00322C50` by `0031BAC0` and `00326BB0` — movement bodies using the same owner lookup and validator, outside anything this contract states.

**Party — CLIENT, OUT-OF-SCOPE (9 edges).** `00322C50` is called by the roster-configuration family — `PartyConfiguration_CollectRuntimeRosterSelectors0To3` (`0031B510`), `PartyConfiguration_SetDefinitionSelectorForIndex` (`00329080`), `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors` (`00328DB0`) and five more — and by `PartyFocus_SelectAndRequestDefaultActor` (`00326500`): party code validates selector ids with the same validator, and does not read derived stats through it.

**Presentation — CLIENT (1 edge).** `BattleUnit_ComputePartyBattleStance` (`00308130`) calls `00307D10`: the stance computation refreshes the same engagement flag the D-7 tail refreshes, and shares nothing else with the rebuild.

**Rewards_Progression_Economy — CLIENT (2 edges).** `Reward_ComputeExperienceForRecipient` (`002F8BB0`) and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`) call `0031B860`: the reward evaluator and the level advance find a stats record's owning unit with the same lookup, and share nothing else with the rebuild through these edges.

**Status_Periodic_Terminal — CLIENT (13 edges).** `BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`) calls `002FEF30` and also `0031B860`, `0031E9A0` and `00322C50`; `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) calls `00307D10` and `0031B860`; `BattleUnit_ResetActionControlForStatusTransition` (`00300140`) and `BattleUnit_RecoverFromTerminalStatusSetIfClear` (`00301140`) call `003105D0`; and `002F9400`, `BattleStats_RemoveStatusesFromMaskAndRecompute` (`0030F690`), `00386860`, `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (`0030E130`) and `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) call the lookup or the validator. The auto-status recompute is the rebuild's caller — the sibling of section 6 — and status transitions cancel actions and refresh engagement through the same two bodies the D-7 tail uses.

**UI — CLIENT, OUT-OF-SCOPE (1 edge).** `BattleMenu_BuildCommandEntryList` (`0031EB20`) calls `00322C50` to validate the ids it lists; it does not read the effective stats through that call.

**WorldAreaField — SERVICE (1 edge).** `00307D10` calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`): the engagement flag the D-7 tail recomputes consults the active field record's bit 15, and the rebuild itself reads nothing from the field.
