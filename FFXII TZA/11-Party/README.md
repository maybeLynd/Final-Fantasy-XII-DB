# Party

**Engine category.** Party composition, active/reserve members, leader, PartyFocus identity, guests.

| | |
|---|---|
| Classification source | PrimaryOwner: Party |
| Functions | 79 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`the-setsavedata-presets-test-battle-scenarios.md`](the-setsavedata-presets-test-battle-scenarios.md) —
  **PARTIAL, tier 1.** The script verb `btlAtelSetNextSetSaveData(n)` stores one byte; the next area
  initialisation rebuilds the party from scenario row `n` (formation, gil, 64 items) and its 226
  party presets (level, five equipment ids, gambit preset, LP or licence mask, MP %). Reks alone is 0.
- [`party-roster-and-control-suppression.md`](party-roster-and-control-suppression.md) —
  **DOCUMENTED, tier 1.** The four-slot roster at `0209A1F0`, the negative-index "current
  focus" convention, and why you lose control when your leader is disabled — the **third**
  subsystem found using one shared functional predicate.

Known anchors: `PartyFocus_GetPreferredDefinitionSelector`, `PartyFocus_GetCurrentPackedActorHandle`, `0035BAA0` (one-shot native party-leader setter - do not repeatedly pin it), `0031B9F0` `BattleSlotMap_ResolveMappedBattleSlot`.

- [`Battle-State-Block/the-battle-state-block-field-map.md`](Battle-State-Block/the-battle-state-block-field-map.md) —
  **DOCUMENTED, tier 1.** The 0x7410-byte image-backed record behind `02EBF190`, field by field above
  the forty stats records: the nine party selectors, the four-entry battle slot map, the leader byte,
  the special-presentation sequence, the mode ladder's words, three combat-formula echoes, the
  inventory snapshot and forty members' gambit banks. The access table is published beside it.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `BattleStats_GetByMappedBattleSlot`, owned by that layer, calls `0031B9F0` on this page. That caller is a 49-byte accessor over the battle stats table: the mapped slot byte is rejected above `0x27`, and the rest index `[02EBF190] + 8` at a stride of `0x1C8` - the same **40 records of `0x1C8` bytes** the battle runtime reset walks; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — SERVICE.** `0035BAA0` on this page calls `FUN_0035bc50`, owned by that layer. What it reaches is a 1,014-byte routine that takes a **`0x1128`-byte stack allocation** through the stack probe and then refuses to do anything when bit 0 of `byte[022C83EC]` is set; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
