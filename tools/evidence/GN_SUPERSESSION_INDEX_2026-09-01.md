# GN READ-ONLY EVIDENCE — SUPERSESSION INDEX — 2026-09-01

Use this file before relying on any `evidence/gn_read_only/` document.

The evidence directory preserves the reasoning trail, including documents that were later corrected. Later corrections outrank earlier interpretations where they conflict.

## Current authoritative read-only interpretations

### `00313A00`
Current proposed CodeDomain:

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

Primary files, newest-first:

1. `V121_GN_INPUTGAMEPLAY_UI_REQUEST_MAPPING_SUPERSEDING_2026-09-01.md`
   - current six-request map;
   - request 1 Battle Menu;
   - request 2 Party Menu/Menu Screen family;
   - request 3 field party-leader selection/change;
   - request 5 free-target actor cycle/target selection;
   - request 14 valid unnamed fullscreen mode/request slot;
   - request 21 valid unnamed generic/transient request slot.

2. `V121_GN_INPUTGAMEPLAY_UI_REQUEST_MAPPING_ADDENDUM_2026-09-01.md`
   - detailed body/call-chain proof for request 1/3/5;
   - request 2/14/21 portions are superseded by the file above.

3. `V121_GN_READ_ONLY_INPUTGAMEPLAY_POLICY_ADDENDUM_2026-08-31.md`
   - complete central policy/mask mechanics;
   - UI request router and policy→request projection.

4. `V121_GN_READ_ONLY_FOLLOWUP_2026-08-31.md`
   - earlier refined proposal context.

5. `V121_GN_READ_ONLY_PROPOSED_ROWS_2026-08-31.md`
   - original read-only proposal provenance.

### `002F7380`
Current proposed CodeDomain:

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Primary files, newest/current interpretation first:

1. `V121_GN_READ_ONLY_LEGACY_PS2GS_ADDENDUM_2026-08-31.md`
   - internal GS PSM/page/local-memory proof;
   - 4 MiB arena / 8 KiB page geometry;
   - texture-mip/ref-count slot-table mechanics.

2. `V121_GN_READ_ONLY_FOLLOWUP_2026-08-31.md`
   - earlier refined budget/ref-slot interpretation.

3. `V121_GN_READ_ONLY_PROPOSED_ROWS_2026-08-31.md`
   - original proposal provenance.

Weather/MWeather research below is important upstream/downstream context but does **not** rename `002F7380` as a Weather owner.

---

## Native seam correction

### Superseding file
`V121_GN_NATIVE_SEAM_CORRECTION_SUPERSEDING_2026-08-31.md`

It supersedes the CombatAction replay-seam implication in:

`V121_GN_READ_ONLY_NATIVE_SEAM_ADDENDUM_2026-08-31.md`

Correct interpretation:

- `00313DB0` is a zero-argument consumer of a 64-entry presentation-ready/action-lifecycle BattleUnit-ID ring;
- it is **not** an arbitrary BattleUnit-selection API;
- ordinary XIIOnline command replication remains upstream through the proven `BattleUnit_IssueCommand` family with stable-to-local identity translation.

The Movement/`002F7380` derived-state topology from the earlier seam addendum remains useful where not contradicted.

---

## Weather / MWeather correction chain

Read in this order:

1. `V121_GN_WEATHER_TERRAIN_AUGMENT_NAMESPACE_CORRECTION_2026-09-01.md`
   - current status-vs-augment namespace model;
   - derived augment bit 16 = Weatherproof;
   - derived augment bit 2 = AccuracyBoost;
   - ordinary status bit 16 = Disease;
   - ordinary status bit 2 = Petrify;
   - formula context merges the layers.

2. `V121_GN_BOW_CROSSBOW_RECIPE_AND_WEATHER_FORMULA_CLOSURE_2026-09-01.md`
   - Bow recipe 25 / Crossbow recipe 26 closure;
   - severe-weather accuracy 0.8/0.5;
   - damage formula distinctions;
   - apply the later augment-namespace correction above to any older status-only wording.

3. `V121_GN_MWEATHER_COMBATFORMULA_AND_PRESENTATION_ADDENDUM_2026-09-01.md`
   - authored `MWeather` packed record;
   - Presentation preset/orientation;
   - gameplay strong-wind projection;
   - Weather/Terrain multiplier matrix.
   - package copy contains the corrected `00389610` SHA.

4. `V121_GN_BOOTSTRAP_SHARED_PRNG_AND_RENDER_FRAME_ADDENDUM_2026-08-31.md`
   - separate Presentation procedural-random stream;
   - duplicate bootstrap environment apply is non-idempotent at least through transition state and PRNG phase.

5. `V121_GN_WEATHER_TRANSITION_RESTORE_AND_PRIMARY_MANAGER_CORRECTION_2026-08-31.md`
   - supersedes Weather-specific interpretation of persistent `+0x1061`;
   - `+0x1061` is broader world-transition `bInitializationRestoreState`;
   - normal Weather roll belongs to primary ActorManager field-runtime initialization.

6. `V121_GN_WEATHER_RUNTIME_VS_FIELD_INIT_RESOURCE_SPLIT_2026-08-31.md`
   - runtime scripted Weather application is not the same transaction as field-resource initialization;
   - do not force Movement/LegacyPS2GS rebuild after every runtime Weather change.

7. `V121_GN_WEATHER_PROBABILITY_NATIVE_APPLY_CORRECTION_2026-08-31.md`
   - supersedes generic/MapRef source attribution for transition probability;
   - native probability table is EBP/script `weatherProbability`.

8. `V121_GN_READ_ONLY_WEATHER_SLOT_TRIGGER_ADDENDUM_2026-08-31.md`
   - earlier Weather Slot trigger evidence remains useful where not superseded;
   - its old generic probability/latch wording is superseded by files above.

---

## Known specific supersessions

- **Old:** `00313DB0` as preferred arbitrary selected-BattleUnit replay API.  
  **New:** false; it consumes a native presentation-ready ring. Use upstream native command/action intent seam.

- **Old:** `002658B0` as generic/MapRef per-slot threshold.  
  **New:** exact EBP/script-header `weatherProbability` reader.

- **Old:** persistent `payload+0x1061` as narrowly Weather-owned preserve flag.  
  **New:** world-transition `bInitializationRestoreState`; Weather consumes it during restore-aware apply.

- **Old:** every runtime Weather change immediately triggers Movement/LegacyPS2GS resource rebuild.  
  **New:** field-init/resource lifecycle does; runtime `setweatherslot` has a separate lower apply path.

- **Old:** `0038B220` early-out described as target status 17 / caster 16.  
  **New:** fresh disassembly shows bit index 16 on all relevant tests; derived augment namespace identifies bit 16 as Weatherproof.

- **Old:** severe-weather accuracy gate described only as status bit 2.  
  **New:** formula context merges namespaces; derived augment bit 2 is AccuracyBoost, while ordinary status bit 2 is Petrify.

- **Old:** request 2 left numeric in first UI mapping addendum.  
  **New:** request 2 strongly closed as Party Menu / Menu Screen family in the superseding request-map file.

---

## Persistence warning

All GN files in this directory are **read-only analysis evidence**.

Applied GM160 GN rows: **0**.

Do not treat an evidence document as a persisted GZF mutation.

The certified parent remains:

**38,001 explicit / 160 unresolved / 99.58072% / overlap 0**

until exact-current mutation + whole-project diff + closed-file `PACK_PASS` + independent fresh reopen succeeds.
