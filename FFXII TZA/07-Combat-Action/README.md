# Combat Action

**Engine category.** BattleUnit commands, action commit, action phases, presentation slots.

| | |
|---|---|
| Classification source | PrimaryOwner: CombatAction |
| Functions | 134 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`Command-And-Action-Seam/native-command-seam.md`](Command-And-Action-Seam/native-command-seam.md) -
  where a command actually enters the engine, and the three things that look like that seam but are not
- [`how-an-action-gathers-its-targets.md`](how-an-action-gathers-its-targets.md) -
  **DOCUMENTED, tier 1.** One chosen target, then a radius, a cone or a line from two action-row bytes; the
  side is the primary target's, confusion ignored. Tallied over all 543 rows.
- [`how-close-a-unit-must-stand-to-act.md`](how-close-a-unit-must-stand-to-act.md) -
  **DOCUMENTED, tier 1.** The three range bands an action start computes - near, middle, reach - where each
  number comes from (the action row, or under flag bit 26 the weapon and the character), the `0.6` / `0.8`
  fallback, and what target spacing and approach pacing do with them.
- [`how-a-combo-continues-and-what-it-blocks.md`](how-a-combo-continues-and-what-it-blocks.md) -
  **PARTIAL, tier 1.** `unit + 0x6B7` is **combo progress**, not an authored count: a combo
  **re-commits the same action** hit after hit, the length is rolled once on hit 1 and memoised, and
  every later hit only asks *have I done enough yet?* A non-zero counter **blocks combat navigation**
  and **overrides party-control suppression**. Corrects one attribution in
  [`../08-Combat-Formula/combos-and-the-guard-parry-flag.md`](../08-Combat-Formula/combos-and-the-guard-parry-flag.md).

- [`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md`](Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) —
  **DOCUMENTED, tier 1.** How a resolved result becomes a battle-log line: the dispatcher's
  action-to-event map (immediates), the poster's ring and rate limit, the visibility filter, the
  realiser's four argument slots, and the table behind it all — `battle_message.bin`, decoded row
  by row and bound to registry slot 7 by content agreement.

- [`Result-Record/the-result-record-field-map.md`](Result-Record/the-result-record-field-map.md) —
  **DOCUMENTED, tier 1.** The record a resolution produces and the applier consumes, offset by
  offset: the initialiser's `-1` sentinels and 0x148 reach, the kind byte, three flag words, the
  numbers, the two status masks with their 33-entry parameter arrays, the timers, the steal slots,
  the foe-only deltas and affinity bytes, and the two echoes to the battle-state block. The access
  table is published beside it.

## Not yet documented

- The 13-phase standard-action pipeline (`00304850` `BattleUnit_AdvanceStandardActionState`)
- Presentation slot pool (`0030C970` / `0030CA80` / `0030CF40` / `0030CFB0` / `0030D070`)
- `BattleUnit_CommitAction` (`0030F760`) and the action context at `BattleUnit+0x708/0x710/0x714/0x6B4`
- Pending action-selection queue (`00313CD0`, up to 8 entries)
- Target set materialization, reservation, enmity

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **ActorEntity — SERVICE.** `BattleUnit_CommitAction` walks the unit table (`BattleUnit_GetBySlotIndex` /
  `BattleUnit_GetSlotCount`). `0030CF40` is called by `BattleStorage_InitializeWorkArrays`.
- **Gameplay — SERVICE.**
  - `BattleUnit_AdvanceStandardActionState` asks `BattleAction_FindApproachGeometryAroundTarget` and dispatches
    presentation events.
  - `BattleUnit_CommitAction` resets and appends to the battle target buffer
    ([the buffer contract](CONTRACT-battle-target-buffer.md)).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this category index.*

**CombatAI — CLIENT (3 edges).** `BattleUnit_SelectAndCommitNextAction` `00305AB0` and `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0` call `BattleUnit_CommitAction` `0030F760`, and the pending action-selection queue `BattleUnit_ProcessPendingActionSelectionQueue` `00313CD0` calls `00305AB0`. The AI layer chooses the action and hands it to this category's commit, and the pending queue drains into the AI's selection; choosing is the AI's, committing is this category's.

**CombatFormula — SERVICE (2 edges).** The standard-action pipeline `BattleUnit_AdvanceStandardActionState` `00304850` calls `BattleRuntime_GetEffectiveActionId` `00387090` and `BattleRuntime_ResolveAndCacheEffectiveActionId` `00387A50`. The pipeline asks the formula layer's runtime which action id is in effect (its get and resolve-and-cache pair) while it advances the phases.

**Movement — SERVICE and CLIENT (5 edges).** `00304850` calls `BattleLocomotion_SetApproachAndReferenceTargets` `00319110`, `BattleUnit_UpdateCombatNavigationStep` `00325BB0`, `BattleLocomotion_ResetPathAndSetTargets` `003291B0` and `0033A1E0` (a 94-byte clearance check that builds a solver context and asks whether an actor pair is clear); the tick's slot-0 step `00234520` calls `00313CD0`. The approach phases of the pipeline steer the unit through the locomotion layer, and the world tick's slot-0 step is where the pending selection queue is drained.

**Party — SERVICE (5 edges).** `00304850`, `BattleAction_ReleasePresentationSlot` `0030C970`, `0030F760` and `00313CD0` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`, and `00304850` also calls `PartyFocus_IsCurrentPackedActorHandle` `003273B0`. The pipeline, the slot pool, the commit and the queue resolve units through the party's focus handle, and the pipeline asks whether the acting unit is the player's current focus.

**Status_Periodic_Terminal — SERVICE (1 edge).** `00304850` calls `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (once, at `00304A76`). One phase of the standard-action pipeline applies a status change through the status layer's routine; which status is not read here.

**WorldAreaField — DEPENDENCY (2 edges).** `0030F760` and `00313CD0` call `FieldData_GetActiveFieldRecordBit15` `00377C20`. Committing an action and draining the selection queue both consult the current field's bit 15, the per-area waiver for disabling statuses.
