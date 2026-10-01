# Combat Formula

**Engine category.** Damage and accuracy recipes, elemental scaling, environment effects.

| | |
|---|---|
| Classification source | PrimaryOwner: CombatFormula |
| Functions | 198 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`Recipe-System/ranged-weapon-recipes.md`](Recipe-System/ranged-weapon-recipes.md) -
  the 109-recipe machinery, with Bow (25) and Crossbow (26) closed - **PARTIAL**
- [`Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) -
  how weather and ground change elemental damage - **DOCUMENTED**

- [`Current-HP/the-hp-write-and-the-lethal-transition.md`](Current-HP/the-hp-write-and-the-lethal-transition.md) -
  **DOCUMENTED, tier 1.** The one function every damage and heal ends in: its eight flag bits and
  where each caller gets them, the two eligibility gates, the refusal of damage to KO/Stone/Vanished
  targets, the floor (`unit + 0x48`) and the cap (max, doubled by status bit 28, frozen by bit 16 =
  Disease), revive-from-zero, and the lethal transition down to the killer id, the death statistics
  and the group ledger.

- [`the-auto-status-rebuild.md`](the-auto-status-rebuild.md) -
  **DOCUMENTED, tier 1.** The recompute every stats write ends in (`0030FED0`, 25 call sites): the
  desired permanent-status set from the party row, the foe's innate mask, equipment and licences;
  the diff against the derived layer; the foe's second mask added as statuses; the affinity
  handshake with the spawn record; the three downward clamps; the charge count.

- [`Battle-Stats-Record/the-battle-stats-record-field-map.md`](Battle-Stats-Record/the-battle-stats-record-field-map.md) —
  **DOCUMENTED, tier 1.** The `0x1C8` stats record, offset by offset, from a typed field scan that
  reaches 283 functions: every writer and reader per byte, the name the owning page established,
  the six ranges nothing enumerated touches, and the scan's stated limits. The access table is
  published beside it.

- [`Steal/the-steal-roll.md`](Steal/the-steal-roll.md) — **DOCUMENTED, tier 1.** Calculator
  slot 195: the availability test on the enemy row's three item words and the spawn record's three
  bits, the two branches (three independent rolls at 6 / 30 / 80 %, one first-hit roll at
  3 / 10 / 55 %), console arm 243's override, the five scratch globals that carry the answer, and
  their consumers — the resolver's copy into the result record, and the two battle messages.

- [`Evaluation-Context/the-evaluation-context-field-map.md`](Evaluation-Context/the-evaluation-context-field-map.md) —
  **DOCUMENTED, tier 1.** The 0x2A-byte record every calculator slot is handed: the action id, the
  two merged flag words, the result pointer, one unit byte, and the source's status / augment layers
  merged into 128 bits — with a table of which slot tests which id (the Thief's Cuffs, the Cameo
  Belt and the Agate Ring are three of twenty-two). The access table is published beside it.

- [`Scratch-Block/the-formula-scratch-block.md`](Scratch-Block/the-formula-scratch-block.md) —
  **DOCUMENTED, tier 1.** The 44 globals at `02AEDFB8`–`02AEE05F` every calculator slot writes and
  the resolver reads back: the reset, every word named or bounded, the outcome roller's three
  evade bands and hit roll decoded (stats `+0x31`–`+0x33` are the band chances), flag word B's
  bits named (combo continues / parry / knockback), the per-unit 64-byte memo that carries the
  preview's rolls to the real resolution, and the kind → entry code → reaction event maps.

- [`Recipe-System/the-count-clock-and-bank-recipes.md`](Recipe-System/the-count-clock-and-bank-recipes.md) —
  **DOCUMENTED, tier 1.** Four recipes whose damage is not a stat: a streak that doubles while it
  keeps landing (`2 ^ count`, the chance to extend falling by `count² / 4`), a walk that pays the
  distance the leader has walked since the last use times 10 / 3 / 2 / 1, and a bank that keeps a
  third of every HP-fraction hit for a later payout. The battle-state block's three echoes and its
  walked-distance accumulator, explained.

## Not yet documented

- `0038B6A0` `BattleFormula_ApplyActionElementAffinity` - resistance/weakness/absorb
- `003896B0` `BattleFormula_RollAvoidGuardParryOutcome` - the standard outcome resolver
- `00389040` `BattleFormula_LoadHitAvoidGuardThresholds`
- The remaining 107 recipes and the full calculator-slot table at `0x01EFA5C0`
- Magick / Technick / item formula families

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **RNG_Random_Selection — SERVICE.** `BattleFormula_RollAvoidGuardParryOutcome` (`003896B0`) draws the gameplay MT
  twice, so guard and parry outcomes are on the combat-formula stream.
- **Rewards_Progression_Economy — CLIENT.** The recompute `0030FED0` is run by the level-up path and by the 432-byte
  level-rank function. **A level-up rebuilds derived stats and auto-statuses.**

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. All of them are edges of the one function this index cites, the recompute `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`, which the auto-status rebuild page documents.*

**CombatAction — CLIENT (1 edge).** The direct-state handler `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` calls `0030FED0`. A direct-state order re-runs the recompute after it changes a unit's state.

**Items_Equipment_Shops_License — CLIENT (4 edges).** `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, `BattleStats_SetEquipmentSlotDirect` `0031A630` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` call `0030FED0`. Setting an equipment slot or a licence node re-derives the member's stats and auto-statuses through the recompute.

**Party — CLIENT (1 edge).** `00328BD0`, which clears a member's equipment, calls `0030FED0`. Stripping a member's equipment is followed by the same recompute.

**Spawn_Encounter_Lifecycle — CLIENT (1 edge).** `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `0030FED0`. A newly activated spawn gets its derived stats and auto-statuses from one recompute.

**Status_Periodic_Terminal — SERVICE and CLIENT (6 edges).** `0030FED0` calls `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` and `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, and is called by `0030E130`, `0030E360`, `BattleStats_RemoveAllMode0StatusesAndRecompute` `0030E8F0` and `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`. The recompute adds and removes auto-statuses through the status layer's write and layer functions, and those status functions call the recompute back after a change.
