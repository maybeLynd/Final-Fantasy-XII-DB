# V121 GN — BOW / CROSSBOW RECIPE + WEATHER FORMULA CLOSURE — 2026-09-01

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline authoritative combat/weather research  
**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Hard accounting fence

This document refines already-canonical CombatFormula mechanisms and Weather/MWeather context.

It does **not** mutate GM160.

Official persistence-certified GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

Strong current unresolved GN proposals remain:

1. `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
2. `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

---

# 1. Correct recipe architecture — two calculator lists per recipe

Canonical resolver:

## `00385F60`
`BattleFormula_ResolveTargetResult`

Exact canonical body:
- **2,302 bytes**
- SHA-256:
  `f887bb1f79153f2d402e15802d46fb78528afc3cf39024ce7c53049f522a8142`

The current ActionDefinition supplies:

`ActionDefinition + 0x08`

as a recipe ID.

Valid recipe domain:
- `0..108`
- total: **109 recipes**

Recipe-pointer table:

`0x01EF96C0`

Calculator-function table:

`0x01EFA5C0`

Each recipe pointer contains **two signed 32-bit calculator-slot lists** separated by `-1` sentinels.

The committed resolver explicitly skips the first list and executes the second list.

Existing V13/V40 provenance distinguishes preview-side and committed calculator dispatch, so the first list is safely described as the **preview-side calculator list**, and the second as the **committed-result calculator list**.

Earlier one-list shorthand for recipes 25/26 is superseded.

---

# 2. Exact recipe 25

Recipe pointer:

`0x01EF9E60`

## Preview-side list

`[5, 6, 22, 33, 34, 35, 42]`

## Committed-result list

`[29, 66, 96, 97, 98, 99, 125, 165, 171, 176, 182]`

Key identifying slots:

- **35** → `003895D0` — severe-weather hit-rate ×0.8
- **42** → `00389820` — ranged guard/avoid/hit outcome resolver with shield + weapon + avoid branches
- **66** → `0038A110` — `BattleFormula_PrepareSpeedStrengthAttackVsDefense`

This is the **Bow-family formula recipe**.

---

# 3. Exact recipe 26

Recipe pointer:

`0x01EF9EB0`

## Preview-side list

`[5, 6, 22, 33, 34, 36, 43]`

## Committed-result list

`[29, 65, 96, 97, 98, 99, 125, 165, 171, 176, 182]`

Key identifying slots:

- **36** → `00389610` — severe-weather hit-rate ×0.5
- **43** → `00389950` — sibling ranged guard/hit outcome resolver lacking recipe-25's third avoid-threshold branch
- **65** → `0038AAF0` — Strength × (Level + Strength) attack-vs-defense preparation

This is the **Crossbow-family formula recipe**.

---

# 4. Internal Bow formula proof — calculator slot 66

## `0038A110`
Canonical name:

`BattleFormula_PrepareSpeedStrengthAttackVsDefense`

Exact body:
- **212 bytes**
- SHA-256:
  `81a158784b577f8faca2c5f39035e5450563eaf235a20bd7eec4edf8790e3f2f`

Canonical V40 semantics already prove:

```text
scale = ((Level + Speed) * Strength) / 218 + 1
```

with:
- AttackPower + native MT19937 variance;
- target Defense mitigation.

The exact body reads:
- caster `+0x1C2` — Level
- caster `+0x2D` — Speed
- caster `+0x2A` — Strength
- caster `+0x2E` — Attack Power
- target `+0x2F` — Defense

This is the native FFXII **Speed formula** used by bows.

Independent external FFXII mechanics documentation gives Bow damage as:

```text
[Attack * Random(1..1.125) - Defense]
*
[1 + Strength * (Level + Speed) / 218]
```

The external formula matches the exact executable arithmetic.

---

# 5. Internal Crossbow formula proof — calculator slot 65

## `0038AAF0`

Exact body:
- **208 bytes**
- SHA-256:
  `d08045b30c5ee53bb4354b86b4a7e03ffdee2d244f3dfb6abb5f1b2c4f20255b`

Exact body arithmetic:

```text
Strength = caster byte +0x2A
Level    = caster byte +0x1C2

scale =
    Strength * (Level + Strength) * (1/256)
    + 1
```

The literal scale constant is:

`0.00390625 = 1 / 256`

The same body then prepares:
- Attack Power from caster `+0x2E`;
- native MT19937 attack variance;
- target Defense from `+0x2F`.

Thus the exact native mechanism is:

**Strength × (Level + Strength) / 256 attack-vs-defense preparation**

Independent external FFXII mechanics documentation gives Crossbow damage as:

```text
[Attack * Random(1..1.125) - Defense]
*
[1 + Strength * (Level + Strength) / 256]
```

The external formula matches the exact executable arithmetic.

---

# 6. Weather accuracy provides a second independent weapon-family fingerprint

## Recipe 25 / Bow — slot 35

### `003895D0`

Exact body:
- **55 bytes**
- SHA-256:
  `bb8cfe864078e5b4651a2571686862f6bc59c43f6be7c7569afee6f9784d4c37`

When:
- caster FormulaEvaluationContext status bitmap does **not** contain bit `0x04` in byte `+0x1A`;
- MWeather gameplay class == 2;

it changes native hit-rate scratch:

**×0.8**

Literal constant:
`0.8000000119...`

This is exactly FFXII's severe-weather Bow accuracy modifier.

External mechanics documentation independently states:
- Bows lose 20% accuracy in severe/adverse weather.

## Recipe 26 / Crossbow — slot 36

### `00389610`

Exact body:
- **55 bytes**
- correct SHA-256:
  `bd0ae289c994442a9432cc9d75eaa8080ea7e93248988b1c09ade820a2930cf4`

Under the same native conditions:

**hit rate ×0.5**

Literal constant:
`0.5`

This is exactly FFXII's severe-weather Crossbow accuracy modifier.

External mechanics documentation independently states:
- Crossbow accuracy is halved in adverse weather.

Thus the recipe identification is independently supported by:
1. distinct damage-stat formula;
2. distinct severe-weather accuracy formula.

---

# 7. Preview outcome calculators provide a third internal fingerprint

Canonical:

`BattleFormula_LoadHitAvoidGuardThresholds @ 00389040`

loads:

- ActionDefinition `+0x12` → native hit-rate scratch `02AEDFE0`
- target BKBI `+0x33` → `02AEDFF0`
- target BKBI `+0x32` → `02AEDFF4`
- target BKBI `+0x31` → `02AEDFEC`

Canonical standard resolver:

`BattleFormula_RollAvoidGuardParryOutcome @ 003896B0`

independently establishes the threshold family as:
- shield guard;
- weapon guard;
- avoid;
- final hit-rate gate.

It proves native compact outcomes:
- 1 — GUARD_WEAPON
- 2 — PARY_WEAPON
- 3 — GUARD_SHIELD
- 4 — PARY_SHIELD
- 5 — AVOID

The executable spells `PARY` with one R in its presentation naming.

## Recipe 25 — slot 42

### `00389820`

Exact body:
- **291 bytes**
- SHA-256:
  `9802534f20002d8bcf3f2f3695948d521e2a7b18f44b4ef64e8f57c2ba673df5`

In its special defensive path it tests, in sequence:

1. `02AEDFF0`
   - success writes result code **3**;
2. `02AEDFF4`
   - success writes result code **1**;
3. `02AEDFEC`
   - success writes result code **5**.

It therefore contains:
- shield-guard threshold;
- weapon-guard threshold;
- avoid threshold.

It also retains the ordinary final hit-percent gate.

## Recipe 26 — slot 43

### `00389950`

Exact body:
- **243 bytes**
- SHA-256:
  `4810b7c439e1211d31c1769d98177ce6f42b7d7a7439e8afa9f33bce5aeb493e`

The sibling path tests:

1. `02AEDFF0`
   - result code **3**;
2. `02AEDFF4`
   - result code **1**;

but omits recipe 25's separate `02AEDFEC` / result-code-5 avoid branch.

It then retains the ordinary final hit-percent gate.

This is a third structural distinction between the two ranged recipe families.

The exact higher-level weapon-rule reason for omitting that avoid branch should remain mechanism-level unless another authored/native source names it.

---

# 8. Exact recipe-pair delta

The two formulas are not merely two arbitrary calculators with coincidentally familiar constants.

They form a deliberately paired recipe family.

## Preview-side difference

Recipe 25:

`... 35, 42`

Recipe 26:

`... 36, 43`

Everything else in that preview list is identical.

## Committed-result difference

Recipe 25:

`... 66 ...`

Recipe 26:

`... 65 ...`

Everything else in the committed-result list is identical.

Therefore the executable itself pairs:

### Recipe 25
- 0.8 severe-weather accuracy
- extra avoid-threshold branch in ranged outcome resolver
- Strength × (Level + Speed) / 218 damage preparation

### Recipe 26
- 0.5 severe-weather accuracy
- sibling ranged outcome resolver without that avoid branch
- Strength × (Level + Strength) / 256 damage preparation

Combined with independently documented FFXII formulas, the identification is strong enough to call:

- recipe **25** = **Bow-family**
- recipe **26** = **Crossbow-family**

This attribution no longer rests on a single external weather constant.

---

# 9. Status gate correction — context+0x1A bit 0x04 is native status ID 2

`BattleFormula_BuildEvaluationContext`

constructs a 128-bit caster-status-presence bitmap beginning at:

`FormulaEvaluationContext + 0x1A`

It enumerates native status IDs `0..127` and combines presence from the native BKBI status layers.

Therefore:

```text
context+0x1A & 0x04
```

means:

**caster native status ID 2 is active**

not:
- a recipe flag;
- a Bow flag;
- a Crossbow flag;
- an `IgnoreWeatherAndTerrain` option.

Both slot 35 and slot 36 skip their strong-wind accuracy adjustment when caster status ID 2 is active.

The exact authored/player-facing name of native status ID 2 remains intentionally unresolved in current GFZ evidence.

Do not promote a status name from external status lists until an internal binary/resource/script bridge closes it.

---

# 10. Separate weather/terrain formula bypasses remain numeric

`0038B220`, the environmental element-scaling stage, has different early-out conditions involving:

- target native status ID 17 in either status layer;
- caster native status ID 16.

Those are **not** the same gate as the Bow/Crossbow status-ID-2 weather accuracy gate.

Current static evidence does not justify calling these:
- `Ignore Weather and Terrain`;
- an accessory effect;
- a passive license;
- a specific named status.

Preserve numeric status identity until independently named.

---

# 11. Corrected MWeather artifact hash note

Earlier `V121_GN_MWEATHER_COMBATFORMULA_AND_PRESENTATION_ADDENDUM_2026-09-01.md`
contained one typo in the textual SHA recorded for `00389610`.

Correct function SHA is:

`bd0ae289c994442a9432cc9d75eaa8080ea7e93248988b1c09ade820a2930cf4`

The corrected local MWeather addendum has SHA-256:

`954df59a30fde1b81f1495162bb5b3c6c15f074c2af190d0b9d53f0a671bf8d7`

Any older uploaded/indexed copy carrying the bad `00389610` SHA is superseded on that textual field.

---

# 12. XIIOnline consequence

This recipe closure reinforces the existing CombatFormula authority model.

Weather affects more than local visual state.

For Bow/Crossbow actions the authority's native formula selects the correct:
- damage-stat formula;
- weather hit-rate scaler;
- guard/avoid/hit outcome recipe;
- later element/environment/affinity stages;
- result commit.

Therefore XIIOnline should not independently network:
- Bow weather accuracy as a standalone percentage;
- Crossbow weather accuracy as a standalone percentage;
- formula calculator slot numbers;
- formula scratch thresholds.

Instead:

authoritative action intent  
→ receiver-local/native identity resolution on authority  
→ native Bow/Crossbow recipe  
→ native Weather/Terrain context  
→ authoritative resolved result  
→ exactly-once native result/consequence realization.

Clients that locally preview hit/damage must have the same authoritative:
- Weather Slot;
- relevant area/terrain state;
- caster/target statuses;
- equipment/action definition

before those previews are expected to match.

---

# 13. GFZ state remains unchanged

This closes semantics around already-canonical CombatFormula functions.

It does **not** identify/apply another GM160 unresolved row.

Applied GN rows: **0**

Persistence-certified GM160 remains:

- **38,001 explicit**
- **160 unresolved**
- **99.58072%**
- **overlap 0**

The two strong current unresolved GN proposals remain unchanged.

