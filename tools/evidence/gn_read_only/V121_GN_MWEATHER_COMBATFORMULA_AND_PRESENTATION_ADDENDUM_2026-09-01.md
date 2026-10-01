# V121 GN — MWEATHER → PRESENTATION + COMBATFORMULA ADDENDUM — 2026-09-01

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline authoritative Weather / terrain / combat-coherence research  
**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Accounting / hard fence

This addendum contains exact-current authorized-EXE analysis plus historical canonical V120 evidence and explicitly marked external mechanics corroboration.

It does **not** mutate the GM160 GZF.

Official persistence-certified GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- explicit coverage: **99.58072%**
- overlap: **0**

Strong current unresolved GN proposals remain:

1. `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
2. `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

---

# 1. Authored `MWeather` resource identity

The executable contains the authored resource name:

`MWeather`

The loader/registration path binds that resource and publishes its loaded pointer into the WorldAreaField weather-resource state.

## Resource publisher — `00378F70`

- body: **10 bytes**
- exact SHA-256:
  `c7f7ae307d995792991c1c870e412985134c45549f023fb463cc2acfb9f3335a`

This is the direct MWeather resource-publisher callback.

The identification comes from the literal executable resource name plus the exact loader/publisher topology, not from a guessed weather-shaped data pattern.

---

# 2. Exact packed MWeather record schema

All three field extractors use one packed-bit reader.

## `003777C0`

- body: **144 bytes**
- exact SHA-256:
  `a3688ce25bd89260d39903d96795a76333a86a4ce25ce9a301871d31eae4cd2e`

It reads a variable-width packed bitfield from the loaded MWeather data.

The indexed record basis is:

**9 bits per `(MapRef-derived selector, Weather Slot)` combination**

with effective bit base:

`9 * (3 * selector + weatherSlotIndex)`

The three exact wrappers are:

## `00377850`
- body: **14 bytes**
- SHA:
  `2864424257792a1eedc16082deb6c948d846e75991bf31f0b66b72c00270c715`
- extracts **bits 0..2** — 3 bits

## `003777A0`
- body: **15 bytes**
- SHA:
  `e6ab05cfb1c29eade4091b819716e9ba1a501ebe6a519919d067a18d5889a68e`
- extracts **bits 3..6** — 4 bits

## `003777B0`
- body: **15 bytes**
- SHA:
  `528db1c1c23ce74fd59728f88d2deb855bc888c8ef39c563230fe4d8de06630d`
- extracts **bits 7..8** — 2 bits

The exact designer-facing source name of the MapRef-derived selector is not yet proven and remains conservative.

---

# 3. MWeather Presentation meaning

Native zero-mode WorldAreaField→Presentation refresh reads the current selector + Weather Slot and extracts all three MWeather fields.

Those values feed:

## `0040AAD0`

Canonical V120 Presentation owner:
embedded Presentation backend mode/orientation initializer.

- body: **286 bytes**
- SHA:
  `ace98b940185f121d2eb0819301478dfa1f81c1493d7310a31ca89114039dd9b`

Exact mechanics:

### MWeather bits 0..2
Select embedded Presentation backend preset/mode **0..7** through:

## `0040B3B0`
- body: **118 bytes**
- SHA:
  `bbd1e5c397391ad4596f7af42bbe42f85be9ecea6d7b7747e231ff5575fced35`

### MWeather bits 3..6
Select a **16-sector azimuth/orientation index**.

Each sector advances by:

`π / 8`

= **22.5 degrees**

before local procedural perturbation.

### MWeather bits 7..8
Select an elevation/orientation class:

- `0` → base 0 degrees
- `1` → base +30 degrees
- other encoded branch → base -30 degrees

Current static proof does not establish whether authored value 3 is actually emitted, so do not invent a fourth designer-facing class.

### Local Presentation randomization

`0040AAD0` calls the separate shared procedural Presentation PRNG twice.

Both angular terms receive approximately:

`±0.15 rad`

= **±8.59 degrees**

of receiver-local procedural variation.

That PRNG is not FFXII's gameplay MT19937 and should not be treated as authoritative Weather RNG.

---

# 4. Published Presentation basis

## `0040B430`

Canonical V120 Presentation owner.

- body: **416 bytes**
- SHA:
  `9d74548e867ceb8df5c19a7bb34f29d337d5eeecc7e26b3fcbfa0e64fd1b1084`

It normalizes/publishes the basis constructed from the MWeather preset/orientation state.

The sole identified high-level basis consumer is:

## `0040FF30`

- body: **5,919 bytes**
- SHA:
  `d269c23b3fcb6839c2bf7583e5476ab2aaf421c391c7bde6d246005d92c1d865`

Historical V120 evidence classifies it as a large embedded Presentation visual evaluator that:
- consumes authored controller state;
- evaluates animated/blended transforms;
- updates live visual-runtime channels.

Therefore the MWeather orientation basis is proven to feed the embedded Presentation visual-controller backend.

Do **not** overname it as:
- sun direction;
- sky direction;
- fog direction;
- global light direction;

without stronger authored/runtime proof.

---

# 5. Critical correction — MWeather is not purely visual

Inside lower native Weather apply owner `0026D910`, FFXII extracts the same MWeather 3-bit preset **before** the Presentation refresh.

Exact collapse:

```text
preset == 0   -> runtime class 0
preset 1..3   -> runtime class 1
preset >= 4   -> runtime class 2
```

The resulting class is stored in:

`02099DAC`

Native getter:

## `00263E20`
- body: **7 bytes**
- SHA:
  `fcf608637522a4c96461c71fb7462323d4ab359c306dfa74c0a9f25e41c3994a`

Thunk:

`003214A0`

This class is read by canonical CombatFormula routines.

Therefore MWeather bits 0..2 have two native roles:

1. full 3-bit preset drives embedded Presentation backend selection;
2. collapsed 0/1/2 class drives gameplay CombatFormula behavior.

This makes the committed Weather configuration genuine gameplay state, not merely Presentation state.

---

# 6. Separate global environment class — `02099DA8`

A different WorldAreaField runtime value is stored at:

`02099DA8`

Getter:

## `00263E10`
- body: **7 bytes**
- SHA:
  `6b28db482e91f6ffc23f830c10c5b8dacf5e57513085cdc5425e0f55d744d131`

Thunk:

`00321490`

`0026D910` derives this state separately from authored field/environment data.

Do not conflate:
- `02099DA8`
- `02099DAC`.

They encode different environmental dimensions.

---

# 7. Per-target terrain/environment class

Canonical CombatFormula helper `0038B220` also calls a target-local environment resolver through:

`003210E0`
→ `00263DD0`

## `00263DD0`

- body: **53 bytes**
- SHA:
  `ce24e4da55529d27284ae4f29c18411423da41bd12ef40c692a747097a0e3d27`

The helper:
1. traverses from the target's live runtime state into its current local field/navigation record;
2. reads the target-local authored environment index;
3. resolves that index through the current field environment table.

This creates a **per-target terrain/environment class** independent of the global weather class.

Its behavioral values in the formula are:

- local class `0`
- local class `1`
- local class `2`

Current mechanics identify their effects exactly; the names Water/Sand/Snow-Ice below are additionally corroborated by known FFXII terrain mechanics.

---

# 8. Full environment elemental modifier owner — `0038B220`

## `0038B220`

Canonical V120 category:
**CombatFormula**

- body: **1,138 bytes**
- exact SHA:
  `a0e03037826d41312c3f686a94884a735d59874795a524ffe9a005668800b505`

It operates on canonical:

`g_fFormulaScratchScale` at `02AEE054`

and uses the current ActionDefinition element mask at byte:

`ActionDefinition + 0x13`

The same element byte is independently consumed by:

## `0038B6A0`
`BattleFormula_ApplyActionElementAffinity`

- body: **686 bytes**
- SHA:
  `0696a0d8b8c93c5dc53bdb95479995794fa2dfe8a2bd4259eb6bd7e0b2683817`

Thus `0038B220` is a **pre-affinity environmental/terrain element-scaling stage**, distinct from target resistance/weakness/absorb affinity.

---

# 9. Exact global environment matrix from `02099DA8`

The executable's `0038B220` branches establish:

## Global class `0`
- Fire (`0x01`) → **×0.5**
- Lightning (`0x02`) → **×1.2**

This exactly matches FFXII **Rain** mechanics.

## Global class `1`
- Earth (`0x08`) → **×1.2**

Combined with strong-wind class 2 below, this produces the native Sandstorm pattern.

## Global class `2`
- Ice (`0x04`) → **×1.2**

Combined with strong-wind class 2 below, this produces the native Snow/Snowstorm pattern.

## Global class `3`
- Water (`0x10`) → **×1.2**

This exactly matches FFXII **Fog / Dense Fog** mechanics.

Values outside these tested classes do not receive these specific base element modifiers in this stage.

Strong conservative mapping:

- `0` — Rain environmental class
- `1` — Sand/Sandstorm base environmental class
- `2` — Snow/Ice base environmental class
- `3` — Fog environmental class

The executable mechanics are primary evidence; historical FFXII mechanics documentation provides exact external corroboration.

---

# 10. Exact per-target terrain matrix

`0038B220` also applies the same action-element mask against target-local environment class.

## Target-local class `0`
- Lightning (`0x02`) → **×1.2**
- Water (`0x10`) → **×1.2**
- Earth (`0x08`) → **×0.5**

This exactly matches the documented FFXII **Water terrain** effects.

Notably, the binary does **not** halve Fire solely because the target is standing in Water terrain.

## Target-local class `1`
- Earth (`0x08`) → **×1.2**

Matches **Sand terrain**.

## Target-local class `2`
- Ice (`0x04`) → **×1.2**

Matches **Snow / permanent-ice terrain**.

Therefore strong behavioral names are:

- local class `0` — Water terrain
- local class `1` — Sand terrain
- local class `2` — Snow/Ice terrain

The target-local terrain and global weather modifiers multiply with one another.

---

# 11. MWeather gameplay class 2 = strong-wind effects

When collapsed MWeather class is:

`02099DAC == 2`

`0038B220` applies:

- Water (`0x10`) → **×0.5**
- Fire (`0x01`) → **×1.2**
- Wind (`0x20`) → **×1.2**

This exact combination is FFXII's **strong-wind** combat effect.

Therefore the strongest behavioral description is:

**MWeather gameplay class 2 implements strong-wind Weather effects.**

Do not overstate the original designer enum name of presets 4..7. What is proven is that all MWeather presets `>=4` collapse to this gameplay strong-wind class.

---

# 12. Combination behavior emerges multiplicatively

The engine does not need one unique hardcoded formula for every named weather condition.

It composes:
- global environmental class;
- MWeather strong-wind class;
- target-local terrain class.

Examples:

## Rain
global Rain class only:
- Fire ×0.5
- Lightning ×1.2

## Rain + strong wind / Heavy Rain
Rain class:
- Fire ×0.5
- Lightning ×1.2

times strong wind:
- Fire ×1.2
- Water ×0.5
- Wind ×1.2

Net:
- Fire `0.5 × 1.2 = 0.6`
- Lightning ×1.2
- Water ×0.5
- Wind ×1.2

This exactly matches known FFXII Heavy Rain / Rain+Wind mechanics.

## Snow / Snowstorm
Snow/Ice base class:
- Ice ×1.2

times strong wind:
- Fire ×1.2
- Water ×0.5
- Wind ×1.2

Net:
- Fire ×1.2
- Ice ×1.2
- Water ×0.5
- Wind ×1.2

## Sandstorm
Sand base class:
- Earth ×1.2

times strong wind:
- Fire ×1.2
- Water ×0.5
- Wind ×1.2

Net:
- Fire ×1.2
- Earth ×1.2
- Water ×0.5
- Wind ×1.2

This factorized architecture explains the published FFXII Weather/Terrain table directly from native code.

---

# 13. Severe-weather hit-rate scaling

Two adjacent canonical CombatFormula functions operate on the native hit-rate scratch.

Canonical `BattleFormula_LoadHitAvoidGuardThresholds` copies:

`ActionDefinition.bHitRate (+0x12)`

into:

`02AEDFE0`

before the standard hit/avoid/guard/parry resolver consumes it.

## `003895D0`

- body: **55 bytes**
- SHA:
  `bb8cfe864078e5b4651a2571686862f6bc59c43f6be7c7569afee6f9784d4c37`

When:
- FormulaEvaluationContext byte `+0x1A` bit `0x04` is clear;
- MWeather gameplay class == 2;

it scales native hit-rate scratch:

**×0.8**

using exact float constant `0.8000000119...`.

## `00389610`

- body: **55 bytes**
- SHA:
  `bd0ae289c994442a9432b4745b44fc36c9993f1251990654049aee2045590a90`

Under the same gates:

**hit rate ×0.5**

These exactly reproduce FFXII's severe-weather ranged accuracy penalties:

- bows → 80%
- crossbows → 50%

Current static binary proof establishes the two exact multipliers and that they are formula-calculator routines. External FFXII mechanics identify the corresponding weapon families. A final internal recipe/weapon-family mapping should still be preferred before permanently naming each function specifically Bow vs Crossbow in canonical GFZ metadata.

Strong current working descriptions:

- `003895D0` — strong-wind/severe-weather **0.8 hit-rate scaler**; externally matches Bow penalty
- `00389610` — strong-wind/severe-weather **0.5 hit-rate scaler**; externally matches Crossbow penalty

---

# 14. Formula bypass bits remain intentionally conservative

`003895D0` and `00389610` both skip weather hit-rate scaling when:

`FormulaEvaluationContext+0x1A & 0x04 != 0`

`0038B220` has separate early bypass conditions, including:
- two target BKBI status-layer tests;
- `FormulaEvaluationContext+0x1C & 0x01`.

External FFXII mechanics include an **Ignore Weather and Terrain** capability/passive/equipment behavior.

However, the exact authored/internal names of these individual context/status bits have not yet been closed from current binary/source evidence.

Therefore they remain:

- weather/terrain formula bypass candidates;
- exact native bit identities preserved;
- no permanent `IgnoreWeatherAndTerrain` name yet.

Do not force the external name into GFZ without an internal evidence bridge.

---

# 15. MWeather now crosses three subsystem boundaries

The same authored Weather Slot ultimately influences:

## WorldAreaField
- durable Weather Slot;
- EBP `weatherProbability`;
- global weather class;
- target-local terrain resolution;
- MWeather gameplay-class derivation.

## CombatFormula
- element-specific environmental multiplier;
- target-local terrain multiplier;
- strong-wind multiplier;
- severe-weather hit-rate scaling.

## Presentation
- MWeather backend preset;
- randomized azimuth/elevation orientation;
- normalized embedded visual-controller basis;
- visual-runtime evaluation.

This is an important correction to the earlier idea that MWeather was merely local visual state.

The **full MWeather resource is not itself network authority**, but its gameplay projection proves that every client must be coherent about the authoritative Weather Slot / area state before local gameplay formula prediction is trusted.

---

# 16. XIIOnline authoritative-weather consequence

The multiplayer roadmap already requires shared Weather/environment state.

Static reverse engineering now gives a stronger requirement.

## Authoritative logical state

At minimum, authoritative world state must include:

- map/area identity;
- committed Weather Slot;
- appropriate Weather/world revision fencing.

The native authority should continue to generate Weather through:
- authored EBP `weatherProbability`;
- native MT19937;
- native alternate-slot eligibility.

XIIOnline should synchronize the **committed outcome**, not replace the native Weather algorithm.

## Combat

Weather is gameplay-relevant.

The authority's CombatFormula naturally consumes:
- global weather class;
- MWeather strong-wind class;
- target-local terrain class.

This reinforces the existing XIIOnline design that **committed combat outcomes should be authoritative** rather than independently recomputed on every client.

If clients locally preview actions or UI hit estimates, their local Weather Slot/area state must be reconciled before those previews are expected to match authority.

## Presentation

Receiver-local Presentation state should continue to regenerate from:
- local native MWeather resource;
- shared committed Weather Slot;
- local Presentation PRNG.

Do not network:
- the Presentation random recurrence state;
- randomized azimuth/elevation results;
- normalized basis globals;
- `0040FF30` visual-runtime state.

Those are derived local visual state.

---

# 17. Mod compatibility

This architecture is especially compatible with the project's native/mod-preservation rule.

Potentially moddable native layers remain separate:

1. EBP/script `weatherProbability`
2. field/MapRef environmental data
3. authored `MWeather`
4. native CombatFormula
5. native Presentation backend

A server-authoritative committed Weather Slot allows each layer to keep using the game's/mod's authored data.

However, if clients run **different gameplay-affecting MWeather/field data**, local formula previews can differ even with the same Weather Slot.

For authoritative XIIOnline combat this can be handled by authoritative committed outcomes, but mod/version compatibility should still detect materially incompatible gameplay data when necessary.

---

# 18. Late join / field re-entry ordering

Because Weather affects:
- CombatFormula;
- conditional spawn eligibility;
- Presentation;
- field-resource selection;

late join should follow:

1. authoritative map/area identity established;
2. authoritative committed Weather Slot/revision established;
3. native WorldAreaField Weather state reconciled;
4. native field/resource initialization consumes that Weather;
5. weather-dependent spawn eligibility becomes valid;
6. combat prediction/formula context becomes valid;
7. local Presentation/MWeather visual state regenerates.

Do not let a late joiner perform meaningful weather-sensitive gameplay prediction or conditional spawn decisions against stale local Weather state.

---

# 19. External corroboration boundary

External FFXII mechanics documentation corroborates the exact binary-derived multipliers:

- strong wind: Fire/Wind ×1.2, Water ×0.5;
- rain: Fire ×0.5, Lightning ×1.2;
- rain+wind/heavy rain: Fire ×0.6, Lightning/Wind ×1.2, Water ×0.5;
- snow: Fire/Ice/Wind ×1.2, Water ×0.5;
- sandstorm: Fire/Earth/Wind ×1.2, Water ×0.5;
- fog: Water ×1.2;
- water terrain: Lightning/Water ×1.2, Earth ×0.5;
- sand terrain: Earth ×1.2;
- snow/ice terrain: Ice ×1.2;
- severe weather: Bow ×0.8, Crossbow ×0.5.

The executable remains the semantic authority here. External documentation is used only to attach familiar FFXII names to an already exact native multiplier matrix.

---

# 20. GN ledger remains unchanged

This discovery materially improves the semantic graph but does not identify a new GM160 unresolved row.

Applied GN rows: **0**

Persistence-certified GM160 remains:

- **38,001 explicit**
- **160 unresolved**
- **99.58072%**
- **overlap 0**

Prospective two-row GN state remains only prospective:
- **38,003 explicit**
- **158 unresolved**
- **99.58596%**

No persistence claim until the physical GM160 recovery-transfer GZF can be fresh-imported, exact-current fenced, mutated, whole-project diffed, closed-file packed with `PACK_PASS`, and independently fresh-reopened.

