# Status / Periodic / Terminal

**Engine category.** Status effects, derived augments, periodic ticks, KO and death.

| | |
|---|---|
| Classification source | PrimaryOwner: Status/Periodic/Terminal |
| Functions | 24 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`Status-And-Augment-Layers/two-layer-effect-model.md`](Status-And-Augment-Layers/two-layer-effect-model.md) -
  the two effect bitmaps, how they merge, and the aliases that produces - **DOCUMENTED**

- [`Status-Write/the-status-write-and-its-side-effects.md`](Status-Write/the-status-write-and-its-side-effects.md) -
  `BattleStats_ChangeStatusAndProcessSideEffects` in execution order: the gates, the party-side
  terminal shortcut, the six modes, the two per-status arrays it initialises from `status_data`,
  the "only a presence change fires anything" rule, the status's own result record (only status 28's
  removal applies one: HP halved), the cascade from the definition's clear mask, the per-status
  terminal table, and the defeat cleanup with its four `02089340` latches - **DOCUMENTED**

- [`the-thirty-two-statuses.md`](the-thirty-two-statuses.md) - the status ids 0-31 with their bank-5
  names, `listhelp_status.bin` help text, `status_data.bin` timers and clear-on-apply masks, and
  where the database has read the engine acting on each - **DOCUMENTED**

## Not yet documented

- Periodic/tick effect processing
- KO, revive and terminal state transitions
- Status timers and the augment Timer Link field
- Status side effects processed by `0030E130`

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

`0030E130`, the status-layer modifier this README names, sits between four layers.

- **Callers.** **CombatAction** `BattleUnit_ExecuteDirectStateCommandOrder` and **CombatFormula**
  `BattleFormula_ApplyTargetResult` call it.
- **Callees.**
  - **CombatFormula:** the two transition-result builders `BattleFormula_BuildInactiveStatusTransitionResult` and
    `BattleFormula_BuildRandomElementStatusTransitionResult`, and `BattleFormula_ApplyTargetResult` itself, so the
    two functions call each other.
  - **CombatAI:** `GambitConfig_AdjustAvailableEntryCountByStatsRecord`.
  - **Gameplay:** the class test `BattleEncodedId_IsValidForClass`.

[`Status-And-Augment-Layers/two-layer-effect-model.md`](Status-And-Augment-Layers/two-layer-effect-model.md) §11
reads the body.
