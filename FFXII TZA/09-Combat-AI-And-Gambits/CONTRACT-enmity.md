---
contract: Hold, generate, spread and decay a foe's threat toward the party
category: 09-Combat-AI-And-Gambits
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: gambit-evaluation-and-enmity.md
entries: ["003216E0", "00321850", "003219D0", "00321B00", "00321530", "00321D30"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the six bodies' extents, the decay read in full from its first instruction,
    the table base and its null guard, the interval's two operands resolved, the class gate's byte,
    and the writer's own suppression chain. **This records checks performed on that date, not the
    method of the original derivation**, which is on the gambit page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-enmity-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — enmity

> **Authored 2026-09-22 by FABLE.** S-25's binding gap is *"operation-scoped over the gambit walk;
> enmity uncontracted"*. [`CONTRACT-gambit-walk.md`](CONTRACT-gambit-walk.md) covers the walk.
> **The threat table it consults had no contract.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is eight
> such invariants across five operations that never call one another.

## 1. Purpose

Answer "who is this foe angriest at". Every foe carries a byte per party combatant; actions raise
and lower those bytes, a propagation step spreads them, and a decay step drains them while nothing
is happening.

## 2. Interface

| operation | body | size |
|---|---|---:|
| apply an action's three parameters | `BattleEnmity_ApplyActionParameters` (`003216E0`) | 141 B |
| write one combatant's entry | `BattleEnmity_WriteForCombatantId` (`00321850`) | 381 B |
| spread to other foes | `BattleEnmity_PropagateToPerceivingFoes` (`003219D0`) | 296 B |
| draw threat off everyone else | `BattleEnmity_AdjustOtherRelevantCombatants` (`00321B00`) | 551 B |
| decay | `BattleEnmity_UpdatePeriodicDecay` (`00321530`) | 142 B |
| write every entry | `BattleEnmity_WriteAllCombatantIds` (`00321D30`) | — |

## 3. Types

```
BKEI (unit + 0x6A0)
  +0x19   u8      the DECAY TIMER
  +0x1A.. u8[]    one threat byte per combatant id — read as table[id + 1] from the +0x19 base
```

**The table base is `BKEI + 0x19` and it is null-guarded by `cmove`, not by a branch** (`00321569`
forms it, `0032156D` replaces it with zero when the BKEI is null, `00321571` then tests it).

## 4. Preconditions · postconditions · invariants

### The eight cross-operation invariants

**E-1 — One vector, two roles: byte 0 of the table *is* the decay timer.** The decay reads
`movzx ecx, byte ptr [rdi]` at `0032158F` with `rdi = BKEI + 0x19`, while every threat read is
`table[id + 1]` (`00321906`, `movzx esi, byte ptr [r14 + rbp + 1]`). *The header byte a reader would
skip past is live state owned by a different operation.*

**E-2 — Threat is stored on the TARGET, not on the angry party.** A foe's own BKEI holds its
opinion of each party member. So "who hates me" is a scatter across every foe's record and is never
materialised anywhere.

**E-3 — The class asymmetry is one byte, and it is the same byte that selects a unit's stat
source.** Only a **party-class** caster generates enmity (`003216E0`'s gate ~~on the definition
selector's high byte~~ on the caster's **stats byte `+0x05`**, `0032170D movzx eax, byte ptr [r9 + 5]` with
`r9 = [caster + 0x698]`, which must be 0) *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 345](../_index/candidates/s25-opus-replay-enmity/README.md), which executed it 8/8; `0032170D`, `00321890`–`003219AD` and `00321A7D`–`00321AB8` re-read.)*; only **foe-class** units decay (`0032154D`, `cmp byte ptr [stats + 5], 1`),
propagate (`00321A33`) and are written to (`003218D0`). **`stats[+0x05]` is the same selector
[stat derivation](../08-Combat-Formula/CONTRACT-stat-derivation.md) D-1 reads to choose between the
growth-definition path and the `.ard` path.** One authored byte decides both where a unit's numbers
come from and which side of the enmity relation it can be on. *With the caster gate corrected, all four enmity
gates read that same byte: generate `== 0`, and decay, propagate and write `== 1`.*

**E-4 — Every action carries three authored enmity parameters and the third is NEGATED.**
`003216E0` makes exactly three calls — `00321850` with the direct parameter (`0032172E`), `003219D0`
with the propagation parameter (`0032173F`), `00321B00` with the **negated** redistribution
parameter (`00321753`). *An action that generates threat on its target simultaneously draws threat
away from everyone else: threat is redistributed, not merely added.*

**E-5 — Propagation reaches only foes that already hold a non-zero grudge** ~~.~~ **and, when there is a direct
target, that also list it.** `003219D0` walks every
slot, keeps foe-class units other than the direct target, and writes **only when the existing entry
is non-zero**. **A second condition** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 345](../_index/candidates/s25-opus-replay-enmity/README.md), which executed it 8/8; `0032170D`, `00321890`–`003219AD` and `00321A7D`–`00321AB8` re-read.)*: with a non-null direct target, the other foe's own list at
`+0xBC8` (count `+0xBC4`, 16-byte entries) must hold the target's `+0x10` (`00321A82`–`00321AB4`). A grudge alone
does not propagate. OPUS measured an unlisted foe unchanged at 5, and a listed one raised from 5 to 7. A null
direct target skips the list test. *"Perceiving" is a grudge already held, not proximity* — a foe that never cared does
not start caring because someone else was attacked.

**E-6 — Decay is −10 per interval and is HELD while engaged.** `00321576` calls
`BattleUnit_HasActiveEngagementEvidence`; a non-zero answer jumps past the decay to the timer reset
(`0032157D`). Otherwise the timer advances and, on reaching the interval, `003215A5` calls the
write-all with `edx = −10` (`0032159F`, `lea edx, [rsi - 0xa]` with `rsi` zeroed at `0032155F`).
**A foe in a fight never forgets; ~~a foe left alone forgets ten a second~~ a foe left alone decays ten a second,
but never below 1.** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 345](../_index/candidates/s25-opus-replay-enmity/README.md), which executed it 8/8; `0032170D`, `00321890`–`003219AD` and `00321A7D`–`00321AB8` re-read.)* The write floors a previously positive entry at `1` (`0032191D`–`00321923`: a
result `<= 0` from an old value `> 0` becomes `1`). So decay drives a held grudge to 1 and holds it there.
OPUS measured `25/12/5 -> 15/2/1 -> 5/1/1 -> 1/1/1`. **A grudge, once held, is never forgotten by decay.**

**E-6a — The first grudge is boosted, and it seeds every other id** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 345](../_index/candidates/s25-opus-replay-enmity/README.md), which executed it 8/8; `0032170D`, `00321890`–`003219AD` and `00321A7D`–`00321AB8` re-read.)*. When the write raises an
entry and `BattleEnmity_AnyAboveThreshold(foe, 1)` returns 0, the new value gets `+10` (`00321931`–`0032193A`).
OPUS measured `12 -> 22`. When the write takes an entry from `<= 0` to `> 0`, the body walks the foe's 40
entries at `[+0x6A0] + 0x1A` and turns into `1` every zero entry whose id is valid for class 2
(`0032194B`–`003219A5`). *So a foe's first grudge gives it a minimal grudge against every such id, and by E-6
those are never forgotten. Read with E-5, this means "already holds a non-zero grudge" is true for every such
id once the foe holds any grudge, so after the first grudge E-5's list test is what limits propagation.*

**E-7 — The interval is the FrameLimit time base, so it is one second at either frame rate.**

```asm
0032157F  movss xmm0, dword ptr [01DFE0B8]   ; the FrameLimit scale: 1.0, or 2.0 at 60 fps
00321587  mulss xmm0, dword ptr [008F8D80]   ; 30.0
00321594  cvttss2si eax, xmm0                ; 30 ticks, or 60
```

*This is the same time base the periodic tick's drain uses, reached independently in another
category* — and it is the cell this author mis-named a render scale on 2026-09-21, corrected
in the boot contract's §13d.

**E-8 — Every write passes the same suppression that gates acting.** `00321850` tests
`(status & 0x80000003)` at `003218AC` with the `FieldData_GetActiveFieldRecordBit15` waiver at
`003218B3`, and validates the id through `BattleEncodedId_IsValidForClass` at `003218F9` before
touching the table. **A unit that may not act may not accrue threat either**, by the same predicate,
in a body that has nothing else to do with acting.

**And the query side:** the highest-relevant scan walks **only the four party slots**, so "angriest
at whom" is always answered against the active party, never the reserve.

## 5. State

**Owned:** each foe's `BKEI + 0x19` vector — its timer byte and its per-combatant entries.
**Read, never written here:** the definition selector, `stats[+0x05]`, the status words, the slot
roster, and each action's three authored parameters.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-gambit-walk.md`](CONTRACT-gambit-walk.md) — the consumer; S-25's other half |
| **Shares a selector** | [stat derivation](../08-Combat-Formula/CONTRACT-stat-derivation.md) — E-3 |
| **Shares a time base** | [the periodic tick](../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md) — E-7 |
| **Shares a predicate** | the `0x80000003` suppression with the status subsystem — E-8 |

## 7. State transitions

An entry goes `0 → positive` ~~only through a party-class action naming that combatant~~ through a party-class action naming that combatant, and every other zero entry valid for class 2 becomes `1` in that same write (E-6a), `positive →
lower` through another action's redistribution or through decay, and ~~`positive → 0` only by decay~~
~~reaching it.~~ never to 0 by any write, since every writer floors a positive entry at `1`; only the keep bank's `memset` on a non-return area entry zeroes it *(corrected 2026-10-02, OPUS: seed `0032194B`–`003219A5`, floor `0032191D`–`00321923` and `00321C4C`–`00321C52`; the `memset` is the gambit page's section 8k)*. Propagation can move an entry that is already non-zero and can never create one.

## 8. Script · resource · event interactions

Three authored bytes per action definition — direct, propagation and redistribution. The table is
part of the **saved** object, so threat survives a save and reload.

## 9. Determinism

Fully deterministic. No generator is drawn in any of the six bodies.

## 10. Failure paths and edge conditions

- A null BKEI yields a null table by `cmove`, and every operation tests it before use.
- An id failing `BattleEncodedId_IsValidForClass(2, id)` contributes `-1` to the query and is skipped
  by the writers.
- A foe with no table answers the highest-relevant query with `-1`, not `0` — *absent and
  indifferent are different answers.*

## 11. Observable behaviour

Heal the tank and the Marlboro turns toward the healer; keep hitting it and it stays angry;
disengage and walk away and ~~it loses interest at ten a second~~ its interest drains ten a second down to a floor of 1, never to none *(corrected 2026-10-02, OPUS: `0032191D`–`00321923`; E-6)*. Attacking one foe can make its
neighbours angrier — but only the ones that already had a reason.

## 12. Reproduction formula

Write a direct parameter and assert the target's entry rose and every other relevant combatant's
fell by the redistribution parameter. Set one foe's entry to zero and another's non-zero, propagate,
and assert only the second moved — provided, when there is a direct target, that the second foe's `+0xBC8` list holds it; unlisted, neither moves *(corrected 2026-10-02, OPUS: `00321A7D`–`00321AB8`, E-5)*. Hold engagement evidence and assert no decay for any number of
intervals.

## 13. Runtime validation

~~**None.** No experiment executes these six bodies. S-25's runtime cell is not addressed by this
contract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*~~ **Superseded 2026-09-25**: [OPUS block 345](../_index/candidates/s25-opus-replay-enmity/README.md) executed the six bodies (8/8). The evidence class is native
replay, not live.

## 14. Unresolved

- ~~The vector's exact length; the page records 40 bytes and this contract does not re-derive it.~~ *(answered: 40 entries, the loop bound `cmp ebx, 0x28` the gambit page reads in section 8k; 2026-10-02, OPUS)*
- ~~Whether an entry saturates, and at what value.~~ *(answered: at 255 — the store `00321E40` clamps to 0–255, the gambit page's `00321850` row; 2026-10-02, OPUS)*
- ~~What `00321B00` counts as an "other relevant combatant" — its 551 bytes are not read here.~~ *(answered: the four party slots other than the source unit, by `00321850`'s per-entry rule — the gambit page's `00321B00` row, read 2026-09-30; 2026-10-02, OPUS)*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| E-1, E-6, E-7 | `00321530` read in full from its first instruction; the timer read, the engagement branch, `lea edx, [rsi - 0xa]`, and both interval operands resolved from their instructions | 1 |
| E-3's gate byte | `cmp byte ptr [rax + 5], 1` at `0032154D`, `00321A33` and `003218D0` — three bodies, one byte | 1 |
| E-4's three calls and the negation | `003216E0`'s three call sites read in order | 1 |
| E-5 | `003219D0`'s slot walk and its non-zero test read | 1 |
| E-8 | `003218AC`, `003218B3`, `003218F9` in `00321850` | 1 |
| The table base `BKEI + 0x19` and its `cmove` guard | `00321569`–`00321571`, and `00321885`–`0032188D` in the writer | 1 |
| The query's four-slot scan, the 40-byte length, the saved-object finding | [the gambit page](gambit-evaluation-and-enmity.md) §§ Enmity, 8e, 8k | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on E-1 through E-8. **E-1 is the one to test first**:
a reader that treats the vector as entries from index 0 will corrupt the decay timer.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CombatAI — internal.** All six bodies are this category's own.
- **ActorEntity — SERVICE.** The slot roster (`BattleUnit_GetSlotCount`, `BattleUnit_GetBySlotIndex`)
  is what E-5's walk iterates; the dependency is stated in §4.
- **Gameplay — MECHANICAL.** The engagement predicate E-6 tests and the encoded-id validator E-8
  calls both belong to that layer; three of the six bodies reach it through the validator alone. Two
  shared predicates, consulted — no responsibility of this subsystem is shared with it.
- **Items_Equipment_Shops_License, WorldAreaField, Status_Periodic_Terminal — MECHANICAL.** Reached
  through the encoded-id validator, the field-record waiver and the engagement predicate that E-8 and
  E-6 name. *Their callers and further callees are deliberately not cited: each is a hub, and naming
  one imports its whole edge set for a one-line remark.*

## 17. Related

- [Gambit evaluation and enmity](gambit-evaluation-and-enmity.md) — the mechanism
- [Contract — the gambit walk](CONTRACT-gambit-walk.md) — S-25's other half
- [Contract — stat derivation](../08-Combat-Formula/CONTRACT-stat-derivation.md) — shares E-3's selector byte
- [Contract — the periodic tick](../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md) — shares E-7's time base

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** E-1 and E-3 to E-8 became checks at their cited instructions. Script:
`Tools/analysis-kit/gfz-scripts/falsify_enmity.py`, output `falsify_enmity.out`, image `73461d08…`, 0 BROKEN. The behaviour
is OPUS block 345's execution (8/8), and is not re-run.

| # | Clause attacked | Result |
|---|---|---|
| Y0 | §2 sizes | **survives**: 141 / 381 / 296 / 551 / 142 B |
| Y1 | E-1 | **survives**: the decay reads `byte [rdi]`; the write reads `[r14 + rbp + 1]` |
| Y2 | E-3 | **survives**: generate reads the caster's stats `+5`; decay, propagate and write each `cmp byte [rax+5], 1` - one byte |
| Y3 | E-4 | **survives**: three calls, the third after `neg edx` |
| Y4 | E-6 | **survives**: the engagement test `00307CE0`, `lea edx, [rsi - 0xa]`, then the write-all `00321D30` |
| Y5 | E-7 | **survives**: `[01DFE0B8] × [008F8D80]`, and `[008F8D80]` is 30.0 |
| Y6 | E-8 | **survives**: `test eax, 0x80000003`, the waiver `00313F60`, the validator `00322C50` |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it. Most edges below reach the two shared helpers the falsification pass cites for E-8 — the field-record waiver `00313F60` (a five-byte jump to `FieldData_GetActiveFieldRecordBit15`) and the encoded-id validator `BattleEncodedId_IsValidForClass` `00322C50` — from their other callers.*

**ActorEntity — SERVICE and CLIENT (18 edges).** E-5's walk in `BattleEnmity_PropagateToPerceivingFoes` `003219D0` iterates `BattleUnit_GetSlotCount` `00236850` and `BattleUnit_GetBySlotIndex` `00236820`, and `BattleEnmity_AdjustOtherRelevantCombatants` `00321B00` builds its list with `BattleUnit_BuildFilteredFourSlotUnitBuffer` `0030A880`; the unit-release body `00300FC0` calls `003219D0`. The rest is fan-in on the two shared helpers: the unit lifecycle bodies `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0`, `00233D70`, `00233EA0`, `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70`, `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200`, `00234D40`, `00237D80`, `BattleUnit_ApplyUnitDefinition` `0023A570` and `BattleGroup_RefreshFourActorDefinitions` `003266C0` call `00313F60`, and `BattleUnit_FindByDefinitionSelector` `002367A0`, `0023A570`, `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810`, `003266C0` and `BattleSlotMap_InitializeMappingClasses` `00329CC0` call `00322C50`. The enmity walk reads the slot roster that layer owns and a released unit spreads its threat once; the other callers only share the waiver and the validator.

**CombatAction — CLIENT (13 edges).** `Battle_ProcessActionTarget` `00307300` and `BattleAction_ResolveSpecialSequenceTargets` `0030EC00` call `BattleEnmity_ApplyActionParameters` `003216E0`, and the direct-state order handler `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` calls `00321B00`; the availability and range tests `BattleAction_CheckActionAvailabilityReason` `002FFCF0`, `BattleAction_CheckDefinitionCategoryAvailability` `003060E0`, `BattleAction_GetPrimaryRangeScalar` `00309300`, `BattleAction_GetSubtype3Field22OrFFFF` `003093D0`, `0030CBE0`, `0030DB70` and `BattleAction_CheckGlobalCategoryDisableReason` `0031A7B0` call `00322C50`, and the timeline handlers `BattleUnit_HandleActorTimelineEvent` `00319F50`, `BattleUnit_HandleActionTimelineEvent` `00325260` and `BattleAction_ApplyKnockbackImpulse` `00323350` call `00313F60`. The action layer is the caller that generates threat (the apply per landed target, and the direct-state order's adjust); its other edges share the validator and the waiver.

**CombatFormula — MECHANICAL (2 edges).** `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` calls `00322C50`, and `00384F40` calls `00313F60`. Two more callers of the shared validator and waiver; the formula layer does not read or write enmity.

**Gameplay — SERVICE and CLIENT (11 edges).** `BattleEnmity_UpdatePeriodicDecay` `00321530` calls the engagement test `BattleUnit_HasActiveEngagementEvidence` `00307CE0` (E-6), which calls `BattleUnit_HasCurrentFocusEngagementEvidence` `0030BB30` and `BattleUnit_HasRelationshipClass2PlusInSlotMask` `0030C210` and is called by `BattleUnit_UpdateEngagementStateFlag` `00307D10`; `BattleEnmity_WriteForCombatantId` `00321850`, `003219D0` and `00321B00` call `00322C50`; `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` and the encoded-id resolver `0031C5D0` call `00322C50`, and `Battle_EmitReactionPresentationForSlot` `003176E0` and `003257D0` call `00313F60`. Section 16a's reading holds: E-6's engagement predicate and E-8's validator are consulted, and decay is suppressed by what that predicate answers; the other edges are fan-in.

**Input — MECHANICAL (1 edge).** `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` calls `00313F60`. The input arbiter consults the same field-record waiver; it has no enmity relationship.

**Items_Equipment_Shops_License — MECHANICAL (13 edges).** `00322C50` is called by `Equipment_CheckMatchingSecondaryPartnerSelectedOrOwned` `003096F0`, the class-D purchase-flag helpers `0030B180`, `0030B4B0`, `0030B510`, `0030B570`, `0030B630`, `Equipment_CheckItemEligibleForSlot` `00317930`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, the licence bodies `00323910`, `00323C60`, `00323D10`, `00323EC0` and `InventoryDerivedIndex_UpdateOnPresenceTransition` `00325F40`. Equipment and licence code validate ids with the same shared validator; nothing there touches threat.

**Movement — MECHANICAL (6 edges).** The locomotion bodies `0031BAC0`, `00326D60`, `00329A80` and `003911D0` call `00313F60`, and `0031BAC0` and `00326BB0` call `00322C50`. Fan-in on the waiver and the validator only.

**Party — MECHANICAL (11 edges).** Nine roster bodies call `00322C50` (`PartyConfiguration_AddSelector07To25ToAvailablePrimaryIndex` `003170E0`, `0031AC00`, `PartyConfiguration_CollectRuntimeRosterSelectors0To3` `0031B510`, `PartyConfiguration_CollectSelectorsOutside07To25` `00320800`, `PartyConfiguration_FindAvailableNonRosterIndex4To8` `00321100`, `PartyFocus_SelectAndRequestDefaultActor` `00326500`, `PartyConfiguration_DemoteOtherRuntimeRosterSelectorsToNonRoster` `003287A0`, `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors` `00328DB0`, `PartyConfiguration_SetDefinitionSelectorForIndex` `00329080`), and `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` and `0031AC00` call `00313F60`. Roster maintenance validates the same selectors; no party body reads the threat table.

**Spawn_Encounter_Lifecycle — MECHANICAL (2 edges).** `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` call `00313F60`. The spawn distance and retire tests consult the same waiver.

**Status_Periodic_Terminal — CLIENT and MECHANICAL (6 edges).** The maintenance tick `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls the decay `00321530` and also `00322C50`; `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` call `00322C50`; `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450` and `BattleUnit_AddPrimaryResourceRecoveryAccumulator` `00329A20` call `00313F60`. The periodic tick is the caller that runs E-6's decay; the other edges are the status code sharing the validator and the waiver.

**UI — MECHANICAL (3 edges).** `BattleMenu_BuildCommandEntryList` `0031EB20` calls `00322C50` and `00313F60`, and `00322A80` calls `00313F60`. The battle menu builds its command list against the same validator and waiver; it does not read enmity.

**WorldAreaField — DEPENDENCY (4 edges).** `00321850`, `00321B00` and `BattleEnmity_WriteAllCombatantIds` `00321D30` call the waiver `00313F60`, and `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls it too. Every enmity write consults the active field record's bit 15 through that layer's accessor (E-8's waiver), so whether threat is written at all depends on the field record.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-enmity-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0030B510` | 93 B | returns 0 unless `cx` AND 0xF000 equals 0xD000 and `00322C50(1, cx, 1)` (`edx` zero-extended) returns non-zero; otherwise returns bit 1 of the byte at `+0x59C8 + (cx AND 0xFFF)` of the pointer in qword `02EBF190` | `0030B529`, `0030B541`, `0030B548`, `0030B55A`, `0030B562` |
