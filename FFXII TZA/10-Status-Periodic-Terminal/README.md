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
  `BattleStats_ChangeStatusAndProcessSideEffects` in execution order: the gates, the ~~party-side
  terminal shortcut~~ Esper terminal shortcut *(corrected 2026-10-02, OPUS: a party member takes the full path; only a summoned Esper, type `0x1B..0x27`, is short-cut — CONTRACT-status-write.md §10 row 3)*, the six modes, the two per-status arrays it initialises from `status_data`,
  the "only a presence change fires anything" rule, the status's own result record (only status 28's
  removal applies one: HP halved), the cascade from the definition's clear mask, the per-status
  terminal table, and the defeat cleanup with its four `02089340` latches - ~~**DOCUMENTED**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*

- [`the-thirty-two-statuses.md`](the-thirty-two-statuses.md) - the status ids 0-31 with their bank-5
  names, `listhelp_status.bin` help text, `status_data.bin` timers and clear-on-apply masks, and
  where the database has read the engine acting on each - ~~**DOCUMENTED**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*

- [`where-mp-comes-from.md`](where-mp-comes-from.md) - MP gain, walk recovery, cost and Mist Charges - **AUDITED**

- [`Periodic-Tick/what-the-periodic-tick-does.md`](Periodic-Tick/what-the-periodic-tick-does.md) - the gated per-unit tick and its five-stage result builder - **AUDITED**

- Contracts: [`CONTRACT-status-write.md`](CONTRACT-status-write.md), [`CONTRACT-effect-layers.md`](CONTRACT-effect-layers.md) and [`CONTRACT-periodic-tick.md`](CONTRACT-periodic-tick.md) - **CONTRACT READY**; [`CONTRACT-auto-status-rebuild.md`](CONTRACT-auto-status-rebuild.md) - **BEHAVIORALLY UNDERSTOOD** *(six pages added to this list 2026-10-02, OPUS, each with the status its front matter states)*

## Not yet documented

- ~~Periodic/tick effect processing~~ *(now documented: the periodic tick page and its contract, listed above; 2026-10-02, OPUS)*
- KO, revive and terminal state transitions
- Status timers and the augment Timer Link field
- ~~Status side effects processed by `0030E130`~~ *(now documented: two-layer-effect-model.md §11 reads the body and CONTRACT-effect-layers.md specifies it; 2026-10-02, OPUS)*

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
