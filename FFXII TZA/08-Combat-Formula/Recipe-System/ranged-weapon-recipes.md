---
system: Formula recipe system — ranged weapon recipes 25 and 26
category: 08-Combat-Formula
status: DOCUMENTED — owner read done (owner re-status 2026-09-30, OPUS, on FABLE's 2026-09-30 content pass as accepted by SWE2-AUDIT-SEM's review auditsem-review-dd-gameplay-0930); every register row it names is closed. ~~E-3's slot-by-slot compute work remains~~ E-3 is ANSWERED (2026-09-12) and E-2 and E-4 are answered; the recipe lists were re-decoded from the image and §2, §4, §5 and §6 corrected against them. No open residue is left beyond §7's declared boundary (reopened_count 1)
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-both-damage-formulas-disassembled
  last_pass_kind: attack
  prior_pass_kind: reverification
  crossref_clean: true
  reopened_count: 1
---

# Formula recipe system — ranged weapon recipes 25 and 26

> Every action in FFXII picks one of **109** damage recipes. This documents the recipe
> machinery, and closes two of them: Bow and Crossbow.

~~**Status is PARTIAL:** the mechanism is fully documented; 107 of the 109 recipes are not yet
identified (open questions **E-2**, **E-3**).~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): both were answered on 2026-09-12. **E-2**: 90 recipes are used by actions, 11 by weapon rows and 8 by nobody (`recipe-users.tsv`). **E-3** (with AK-3): every calculator slot a shipped recipe names is read or named on the step-table page and the pages it cites.*

## 1. What the player sees

Bows and crossbows are the weapons that care about the weather. Bows lose 20 % accuracy in
severe weather, crossbows lose 50 % — and a Cameo Belt (Accuracy Boost) prevents it, while an
Agate Ring does not. They also use different damage stats: bows scale off Speed, crossbows
off raw Strength.

## 2. Native mechanism

`ActionDefinition+0x08` is a recipe ID in `0..108`. `00385F60` resolves it through the recipe
pointer table at `0x01EF96C0`.

Each recipe pointer contains **two** signed 32-bit calculator-slot lists separated by `-1`
sentinels. Slot numbers index the calculator function table at `0x01EFA5C0`.

- **first list** — preview-side calculators
- **second list** — committed-result calculators

The committed resolver explicitly skips the first list and runs the second.

*Corrected 2026-09-30 (FABLE): "preview" is the code's name, not a UI-only pass.*
- **The first list runs when the action executes.** `BattleUnit_AdvanceStandardActionState` calls
  `BattleAction_EvaluateTargetPreviews` at `00304F1D`, in the execution stage (stage 9,
  [the native command seam](../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md)). That walk runs the
  first list through `BattleFormula_EvaluateTargetPreview` (`00385680`, the step call at `003859FF`).
- **The first list decides whether the shot connects.** For recipes 25 and 26 it holds the hit, evade, knockback and
  weather-accuracy steps. It leaves its outcome in the source's per-unit record, and the committed resolve copies
  that record's `+0x12` bits into the result ([the formula scratch block](../Scratch-Block/the-formula-scratch-block.md)
  §2.5 and §5; AJ-7).
- **The second list computes the damage and effects.**

### Recipe 25 — Bow family (`0x01EF9E60`)

| | |
|---|---|
| preview | `[5, 6, 22, 33, 34, 35, 42]` |
| committed | `[29, 66, 96, 97, 98, 99, 125, 165, 171, 176, 182]` |

- slot **35** → `003895D0` — severe-weather hit rate **×0.8**
- slot **42** → `00389820` — ranged outcome resolver **with** a third avoid-threshold branch
- slot **66** → `0038A110` — `Strength × (Level + Speed) / 218`

### Recipe 26 — Crossbow family (`0x01EF9EB0`)

| | |
|---|---|
| preview | `[5, 6, 22, 33, 34, 36, 43]` |
| committed | `[29, 65, 96, 97, 98, 99, 125, 165, 171, 176, 182]` |

- slot **36** → `00389610` — severe-weather hit rate **×0.5**
- slot **43** → `00389950` — sibling resolver **without** that avoid branch
- slot **65** → `0038AAF0` — `Strength × (Level + Strength) / 256`

The lists are otherwise **identical**. The executable itself pairs these two recipes.

### Severe-weather accuracy gate

Both `003895D0` and `00389610` apply their scale only when:
- merged context bit **2** is clear (that is **AccuracyBoost** in the augment namespace), and
- MWeather gameplay class **== 2** (strong wind).

*Anchored 2026-09-30 (FABLE):*
- `003895D4` tests context `+0x1A` bit 2 and skips the scale when it is set.
- `003895DB` calls the thunk to the gameplay-class getter, which reads `02099DAC`. `003895E0` compares the result with 2.
- `003895F0` multiplies `02AEDFE0` by 0.8 (`008F3108`).
- Class 2 is the collapse of MWeather presets 4 and up, "strong wind", on
  [the MWeather page](../../03-World-Area-Field/Weather/mweather-resource-format.md) (its preset table and its class-2
  evidence row).

This is a *different* gate from the weather/terrain element bypass, which uses bit 16
(Weatherproof). Agate Ring does not help your bow in a storm — and the binary is why.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00385F60` | `BattleFormula_ResolveTargetResult` | 2,302 B | recipe dispatch |
| `0x01EF96C0` | *(recipe pointer table)* | — | 109 entries |
| `0x01EFA5C0` | *(calculator function table)* | — | slot → function |
| `003895D0` | severe-weather ×0.8 scaler | 55 B | Bow, slot 35 |
| `00389610` | severe-weather ×0.5 scaler | 55 B | Crossbow, slot 36 |
| `00389820` | ranged outcome resolver (+avoid branch) | 291 B | Bow, slot 42 |
| `00389950` | ranged outcome resolver (no avoid branch) | 243 B | Crossbow, slot 43 |
| `0038A110` | `BattleFormula_PrepareSpeedStrengthAttackVsDefense` | 212 B | Bow, slot 66 |
| `0038AAF0` | Strength×(Lv+Str)/256 preparation | 208 B | Crossbow, slot 65 |
| `00389040` | `BattleFormula_LoadHitAvoidGuardThresholds` | 119 B | ~~loads thresholds~~ slot 25, the action-row threshold loader (reads action `+0x12`); **not named by recipe 25 or 26** *(corrected 2026-09-30, FABLE)* |
| `00388FB0` | (weapon-recipe threshold loader) | 41 B | slot 22, in both first lists: target stats `+0x33` / `+0x32` / `+0x31` → `02AEDFF0` / `02AEDFF4` / `02AEDFEC`, and hit chance `02AEDFE0 = 100` (`00388FCE`) *(added 2026-09-30, FABLE)* |
| `003896B0` | `BattleFormula_RollAvoidGuardParryOutcome` | — | standard resolver |

## 4. Data structures

```
ActionDefinition
  +0x08  u8   recipeId       0..108
  +0x12  u8   bHitRate       -> 02AEDFE0   (slot 25 only - NOT read by recipes 25 / 26, see below)
  +0x13  u8   elementMask                  (slots 94 / 95 only - NOT read by recipes 25 / 26)

BKBI (caster)                      BKBI (target)
  +0x1C2 u8  Level                   +0x2F  u8  Defense
  +0x2A  u8  Strength                +0x31  u8  -> 02AEDFEC  avoid threshold
  +0x2D  u8  Speed                   +0x32  u8  -> 02AEDFF4  weapon guard
  +0x2E  u8  AttackPower             +0x33  u8  -> 02AEDFF0  shield guard
```

*Corrected 2026-09-30 (FABLE):* the two ActionDefinition bytes above belong to other recipes. Neither list of recipe
25 or 26 names slot 25 (`00389040`, which reads `+0x12`) or slots 94 / 95 (`0038B220`, `0038B6A0`, the action-element
stages that read `+0x13`); `rwr_slots.py` maps each of the three to its slot, and none is in the decoded lists. For a
bow or crossbow the hit chance starts at the constant **100** (slot 22, `00388FCE`). The element stages these recipes
run are slots 96–99, whose bodies address the weapon-row table `02EBF0F8` rather than the action row.

Native compact outcome codes: `1` GUARD_WEAPON · `2` PARY_WEAPON · `3` GUARD_SHIELD ·
`4` PARY_SHIELD · `5` AVOID. *(The executable spells "PARY" with one R.)*

### Damage formulas

```
Bow       scale = Strength * (Level + Speed)    / 218 + 1
Crossbow  scale = Strength * (Level + Strength) / 256 + 1     (literal 0.00390625)

damage = [AttackPower * Random(1..1.125) - Defense] * scale
```

## 5. Call chain

```
action committed
  -> 003847C0  BattleFormula_BuildEvaluationContext     (merge status+augment layers)
  -> 00385F60  BattleFormula_ResolveTargetResult
     -> ActionDefinition+0x08 -> recipe pointer @ 0x01EF96C0
        -> SKIP preview list
        -> run committed list, slot -> function @ 0x01EFA5C0
           -> 00389040  load hit/avoid/guard thresholds
           -> 003895D0 | 00389610   weather accuracy scale
           -> 00389820 | 00389950   outcome resolve
           -> 0038A110 | 0038AAF0   attack-vs-defense preparation
           -> 0038B220  weather/terrain element scaling
           -> 0038B6A0  element affinity
```

*Corrected 2026-09-30 (FABLE): the block above is superseded and kept only as the earlier reading. It put first-list
steps, and two steps neither recipe names, under "run committed list". The lists decoded from `0x01EF9E60` / `0x01EF9EB0`
(`rwr_recipes.py`, which checks both pointers) give this order:*

```
execution stage 9: BattleUnit_AdvanceStandardActionState (call at 00304F1D)
  -> BattleAction_EvaluateTargetPreviews
     -> 00385680  BattleFormula_EvaluateTargetPreview        FIRST list, step call at 003859FF
        -> slot 5  00388350 knockback chance ; slot 6 00388440 knockback roll
        -> slot 22 00388FB0 evade bands from the target, hit chance = 100
        -> slot 33 00389310 ; slot 34 00389370                 (evade-band adjustments)
        -> slot 35 003895D0 x0.8  | slot 36 00389610 x0.5     severe-weather accuracy
        -> slot 42 00389820       | slot 43 00389950          ranged outcome resolve (E-4 ladder)
        => outcome parked in the source's per-unit record (+0x12)
Battle_ProcessActionTarget (call sites 00307419 and 00307436)
  -> 00385F60  BattleFormula_ResolveTargetResult (call at 00307419)   SECOND list, step call at 003863D0
        -> slot 29  00389140 resource-reaction roll
        -> slot 66  0038A110 (Bow) | slot 65 0038AAF0 (Crossbow)   attack-vs-defense preparation
        -> slots 96-99  0038B950, 0038BC00, 0038BE00, 0038BE30     element family (weapon rows 02EBF0F8)
        -> slot 125 0038D280 FinalizeTargetHpMagnitude ; slot 165 0038F890 post multipliers
        -> slot 171 0038F9D0 (weapon row -> percent gate 02AEDFE8) ; slot 176 0038FBC0 ; slot 182 0038FCD0
  -> BattleFormula_ApplyTargetResult (call at 00307436)
```

**Upstream:** ~~the ActionDefinition selected by the command/action pipeline.~~ the standard-action state machine's
execution stage for the first list (`00304F1D`). Four callers of `00385F60` start the second:
`Battle_ProcessActionTarget`, the special-sequence target resolver, the actor-timeline handler and the periodic
tick, whose addresses the pass-22 section below gives. The owner transition is
the recipe byte `ActionDefinition+0x08`, or for a plain Attack the weapon row's `+0x19`.
**Downstream:** ~~committed result realization.~~ the result record, applied by `BattleFormula_ApplyTargetResult`
from `00307436`.
**Do not confuse with:** slots 25, 94 and 95 (`00389040`, `0038B220`, `0038B6A0`), the action-row threshold and
element stages of the magick recipes; and slot 41 (`003896B0`), the melee resolver.

## 6. Modding notes

- **To change a weapon family's behaviour:** change its recipe's calculator slot list, or the
  constants inside the calculator. The recipe *pointer* table and *function* table are both
  static data.
- **Preview vs committed:** two lists exist for a reason. ~~A UI damage preview runs the first
  list; the real result runs the second. Change both or previews will lie.~~ *(Corrected 2026-09-30, FABLE.)* The
  first list runs at execution and decides hit, evade, knockback and weather accuracy. The second computes the damage.
  An edit to either changes real outcomes, not only a preview (§2).
- **Changing a bow's hit rate is not an ActionDefinition `+0x12` edit.** These recipes start from 100 (slot 22), so
  the levers are the weather scale slots 35 / 36 and the evade bands (added 2026-09-30, FABLE).
- **XIIOnline:** never network calculator slot numbers, scratch thresholds, or per-weapon
  weather percentages. Send authoritative action intent, resolve on the authority, replicate
  the committed outcome exactly once. Client-side previews only match if the client shares
  the authority's Weather Slot, terrain, statuses, equipment and ActionDefinition.

## 7. What is not known

- [x] ~~Identity of the other **107 recipes** (open question **E-2**).~~ **Every recipe named by its
      users — 2026-09-12 (FABLE).** The `us` battle pack's action section (`st2e`, 543 rows × 60 B at
      `+0x13210`; byte-identical to the archive's `in` / `ch` `action_data.bin`, the `kr` / `cn` copy
      differs) joined on its recipe byte `+8`, with every action's name decoded from the pack's text
      banks (name word `+0x34`, bank `>> 11`, index `& 0x7FF`), plus the weapon rows' recipe byte
      `+0x19` from [the item page](../../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)
      §10. **90 recipes are used by actions**, eleven by weapon rows (20–27, 29, 64, 104), and
      **8 by nobody** (15, 28, 44, 71, 80, 81, 89, 106).
      The whole table is [`recipe-users.tsv`](recipe-users.tsv) (recipe, action count, action ids,
      decoded names, weapon rows). The largest: recipe 65 × 85 actions (`Darkness`, `Ice Break`,
      `Water Spout` … — the special-attack family), 0 × 73 (`Attack`, `Mount`, `Dismount`, the
      `Reserve` rows and other system actions, whose formula is the weapon's own `+0x19`), 7 × 56
      (`Fire`, `Thunder`, `Blizzard` … the attack magicks), 3 × 26 (`Slow`, `Immobilize`, `Disable` …
      the debuffs), 92 × 19 (`Condemnation`, `Red Spiral` … boss techniques), 2 × 18 (`Regen`, `Haste`,
      `Protect` … the buffs), 93 × 16 (`Inferno`, `Cataclysm` … the Esper ultimates), 72 × 14 (the
      gazes and breaths). Singletons carry the technicks one each — 41 `Stamp`, 42 `Achilles`, 43
      `Charge`, 45 `Souleater`, 49 `Steal`, 56 `Numerology`, 58 `Poach`, 60 `Traveler`, 61 `Gil Toss` —
      which also confirms the count-clock page's inferred names for 16 / 17 / 56 / 60 (`Knot of
      Rust` / `Devour Soul`, `Dark Matter` / `Soul Purge`, `Numerology`, `Traveler`). What each recipe
      *computes* remains the slot-by-slot work of E-3; its *users* are now closed. *(E-3 ANSWERED, next item; noted
      2026-09-30, FABLE.)*
- [x] ~~Identity of every **calculator slot** in `0x01EFA5C0` (open question **E-3**).~~ **E-3 ANSWERED 2026-09-12 (FABLE):** every slot a shipped recipe names is read or named on [the step-table page](../Step-Table/combat-formula-step-table.md) and the pages it cites (AK-3 closed the same day).
- [x] ~~Why recipe 26 omits recipe 25's third avoid-threshold branch (open question **E-4**).~~
      **The rule, measured 2026-09-12 (FABLE); the intent stays outside the binary.** The two
      resolvers are the middle rungs of a **four-rung ladder** over the outcome bands [the scratch block](../Scratch-Block/the-formula-scratch-block.md)
      §2.3 names — A the shield's evade (`02AEDFF0`, stats `+0x33`), B the weapon's evade
      (`02AEDFF4`, `+0x32`), C the record's innate evade (`02AEDFEC`, `+0x31`), the parry chance
      (`02AEDFC4`) and the hit chance (`02AEDFE0`). Read from each resolver's rip-relative loads and
      the 109 decoded recipes (`01EF96C0`):

      | slot | resolver | bands it rolls | recipes | weapon rows ([the attack-defense page](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) §4) |
      |---|---|---|---|---|
      | 41 | `BattleFormula_RollAvoidGuardParryOutcome` `003896B0` | A, B, C, parry, hit | 20–24, 28, 29, 64–66, 103, 104 | every melee family |
      | 42 | `00389820` | A, B, C, hit — **no parry** | 25 | bows |
      | 43 | `00389950` | A, B, hit — **no C, no parry** | 26 | crossbows |
      | 44 | `00389A50` (92 B) | **hit only** — one `mt19937 % 100` roll against `[02AEDFE0]`, miss → `02AEDFBC = 02AEDFB8 = 1`, hit → flag word B bit 3 when `[02AEDFC8]` | 27 | guns, measures |

      So the "higher-level rule" is a ranged ladder: a bow shot can be blocked, parried-out by the
      target's weapon evade and dodged by innate evade but never parried back; a crossbow bolt can
      be blocked or weapon-evaded but **not dodged by innate evade**; a gun shot or measure can only
      miss its own hit roll. Recipe 26 does not "omit" a branch of recipe 25 — it binds the next
      rung down, exactly as recipe 27 binds the rung below it. Why the designers ordered the
      families this way is not in the image.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Recipe domain 0..108, two lists, committed skips the first | complete body of `00385F60` (2,302 B, `f887bb1f…8142`) | 1 |
| Bow damage formula | complete body of `0038A110` (212 B, `81a15878…3f2f`) reading `+0x1C2`, `+0x2D`, `+0x2A`, `+0x2E`, `+0x2F` | 1 |
| Crossbow damage formula | complete body of `0038AAF0` (208 B, `d08045b3…255b`), literal `0.00390625` | 1 |
| Weather accuracy ×0.8 / ×0.5 | complete bodies of `003895D0` (55 B, `bb8cfe86…4c37`) and `00389610` (55 B, `bd0ae289…0a90`) | 1 |
| Gate is merged bit 2 = AccuracyBoost | `003847C0` merge + Workshop `EnumHelper.cs` `AccuracyBoost = 0x4` | 1 + 6 |
| Outcome code set | complete body of `003896B0` | 1 |
| Bow/Crossbow identification | **three independent** native differences (damage stat, weather scale, resolver shape) plus external formula documentation agreeing with the exact arithmetic | 1 + 10 |
| both recipes' lists and every slot's function | `rwr_recipes.py` (DD record 2026-09-30): the pointers at `0x01EF96C0 + 8 × 25 / 26` read back as `0x01EF9E60` / `0x01EF9EB0` (control), the `-1`-separated `i32` runs decoded, each slot resolved through `0x01EFA5C0` | 1 |
| action `+0x12` / `+0x13` are not read by these recipes | `rwr_slots.py`: `00389040` is slot 25, `0038B220` slot 94, `0038B6A0` slot 95, none in either list (control: slots 35 and 42) | 1 |
| weapon-recipe thresholds and the hit chance of 100 | `00388FB0` read whole (41 B), `00388FB0`–`00388FCE` | 1 |
| class 2 is strong wind | `003895DB` / `003895E0`; the MWeather page's preset-to-class collapse and its class-2 evidence row | 1 (by reference) |
| the first list runs at execution | `00304F1D` (call in `BattleUnit_AdvanceStandardActionState`) → `BattleAction_EvaluateTargetPreviews` → `00385680`, step call `003859FF`; the command seam's stage-9 row | 1 |
| the committed resolve and the apply | `00307419` (call to `00385F60`) and `00307436` (call to the result applier) in `Battle_ProcessActionTarget` | 1 |

**Superseded readings:**
- *Old:* recipes 25/26 have a single calculator list.
  *New:* two lists — preview and committed.
- *Old:* the accuracy gate is "native status ID 2" (i.e. Petrify).
  *New:* it is a *merged* effect bit; the intended identity is augment AccuracyBoost, with
  Petrify as a same-position alias the calculator cannot distinguish.
- One earlier document recorded a wrong SHA for `00389610`; the correct plain-body hash is
  `bd0ae289c994442a9432cc9d75eaa8080ea7e93248988b1c09ade820a2930cf4`.

## 9. Related

- [`../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md)
- [`../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)

## Re-verification 2026-09-02 (AH-7)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 13 cited - 12 function entries, 1 interior - 0 unresolved.

**Central claim re-derived.** The headline is *"every action in FFXII picks one of **109** damage
recipes"*, with recipe IDs `0..108` indexing a table at `0x01EF96C0`.

`BattleFormula_ResolveTargetResult` (`00385F60`) was decompiled fresh. The bound appears **twice**:

```c
if (0x6c < bVar1) { ... }        // 0x6C = 108 -> reject IDs above 108
...
piVar3 = (int *)(&g_pBattleFormulaRecipeByEffectClass)[(int)(uint)bVar1];
```

`0x6C` is 108, so valid recipe IDs are **0..108 - exactly 109**. The claim holds, and the table's
Ghidra symbol `g_pBattleFormulaRecipeByEffectClass` confirms it is indexed by effect class.

**Stamp advanced because the body was re-read**, per the evidence standard.

## 10. Independent falsification pass 2026-09-07 — `xiionline-61`

**First genuine attack.** The prior stamp was `reverification-against-current-parent` — a provenance
check, not a pass; this document was one of the twelve identified as scored-audited-but-never-attacked.
Program state **GN160** `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`, both
formula functions disassembled in full.

### Both damage formulas survive, to the instruction

**Bow — `BattleFormula_PrepareSpeedStrengthAttackVsDefense` (`0038A110`, 212 B):**

```asm
movzx eax,  byte [rcx+0x2D]      ; Speed
movzx r8d,  byte [rcx+0x1C2]     ; Level
add   r8d, eax                   ; Level + Speed
movzx eax,  byte [rcx+0x2A]      ; Strength
imul  r8d, eax                   ; Strength * (Level + Speed)
cvtdq2ps xmm0, r8d
divss xmm0, [00D112D0]           ; = 218.0
addss xmm0, [01CEBBA8]           ; = 1.0
movss [02AEE054], xmm0
```

> **`scale = Strength * (Level + Speed) / 218 + 1` — exact.**

**Crossbow — `BattleFormula_PrepareStrengthAttackVsDefense` (`0038AAF0`, 208 B):** identical shape,
reading `[rcx+0x2A]` (Strength) where the Bow reads `[rcx+0x2D]` (Speed), and

```asm
mulss xmm0, [009088D8]           ; = 0.00390625
addss xmm0, [01CEBBA8]           ; = 1.0
```

> **`scale = Strength * (Level + Strength) / 256 + 1`, literal `0.00390625` — exact**, including
> this document's own parenthetical about the literal.

**The field map in §4 is confirmed by which byte each function reads**: `+0x1C2` Level, `+0x2A`
Strength, `+0x2D` Speed, `+0x2E` AttackPower, and target `+0x2F` Defense at `0038A1BA`.

### Why one is a division and the other a multiply — and it corroborates another document

A census first reported **`1/218` occurring zero times in the image**, against 49 occurrences of
`0.00390625`. That is true and it is not a defect:

> **The Bow divides; the Crossbow multiplies.** `1/256` is a power of two and therefore *exactly*
> representable, so replacing `x / 256` with `x * 0.00390625` changes no bit and the compiler is free
> to do it. `1/218` is **not** exactly representable, so under `/fp:precise` the division must remain
> a division — and `divss xmm0, 218.0` is what the binary holds.

**That is the same `/fp:precise` build setting
[`the-maths-the-game-runs-on.md`](../../24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md)
established from the `sqrtss`-to-`sqrtf` ratio**, reached here from an entirely different direction:
one document inferred the setting from what the compiler *refused to inline*, this one from what it
*refused to strength-reduce*. **Neither cites the other.**

**And it is the second time in two blocks that a constant's absence was a compiler transformation
rather than a missing operation** — after MT19937's tempering masks. The two cases resolve in
*opposite* directions, which is the useful part: **there the transformation had happened and the
constant was gone; here it had been forbidden and the constant is present in a form the search did
not anticipate.** A reciprocal search finds only the multiply form.

### The variance guard, cross-checked against a neighbouring document

Both functions compute `xmm1 = AttackPower * 0.125` and compare it against `0.01`
(`008F30E4 = 0.009999999776482582`); when `0.01 > AttackPower * 0.125` the variance term is skipped
and zero is used. Past the guard, the draw is

```
variance = (rand() % (int)(AttackPower * 0.125 * 100)) / 100.0
```

`0038A17D`-`0038A1B2`, via `div ecx` taking the remainder in `edx`. **This matches
[`../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md`](../Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)
exactly** — *"only when ATK * 0.125 >= 0.01"* and the 12.5 % upward-only band — **a third
independent agreement between documents written apart.**

Outputs land at `02AEE054` (scale), `02AEE058` (attack plus variance) and `02AEE05C` (defense), the
shared scratch triple that document also records.

### Verdict

**Nothing overturned; nothing softened.** Every formula, every constant and every field offset this
document publishes reproduces from the instructions. `audit.passes: 1 -> 2`, and the pass kind is
recorded as an attack rather than a re-verification.

**Not examined:** the recipe tables at `0x01EF9E60` / `0x01EF9EB0` themselves, the severe-weather
accuracy gate in §2, the outcome-code set, and the §5 call chain.

*Examined 2026-09-30 (FABLE):*
- **The recipe tables.** Decoded from the image; §2's lists reproduce exactly.
- **The severe-weather gate.** `003895D0` read whole; §2 anchors it.
- **The §5 call chain.** Wrong in two ways, and corrected in §5:
  - first-list steps were placed in the committed list;
  - two stages named in it (`0038B220`, `0038B6A0`) are run by neither recipe.
- **The outcome-code set.** Not re-derived here. It comes from slot 41's resolver, which these recipes do not use.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAction — CLIENT (3 edges).** `Battle_ProcessActionTarget` (`00307300`), `BattleAction_ResolveSpecialSequenceTargets` (`0030EC00`) and `BattleUnit_HandleActorTimelineEvent` (`00319F50`) call the recipe dispatcher `BattleFormula_ResolveTargetResult` (`00385F60`). The action layer decides when a Bow or Crossbow action is resolved against a target; the recipe it names then runs the slots this page lists.

**RNG_Random_Selection — SERVICE (6 edges).** Six of the page's step bodies call `RNG_MT19937_NextU32_Thunk` (`00379CD0`): the ranged outcome resolvers `00389820` (slot 42, with the avoid branch) and `00389950` (slot 43, without it), the hit-only roll `00389A50` (slot 44), the standard resolver `BattleFormula_RollAvoidGuardParryOutcome` (`003896B0`, slot 41), and the preparations `BattleFormula_PrepareSpeedStrengthAttackVsDefense` (`0038A110`, slot 66) and `BattleFormula_PrepareStrengthAttackVsDefense` (`0038AAF0`, slot 65) for their variance. Every ranged hit, avoid and damage-variance decision on this page is a draw from the gameplay Mersenne Twister stream.

**Status_Periodic_Terminal — CLIENT (1 edge).** `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) calls the dispatcher `00385F60`. The periodic tick shares the recipe dispatcher with weapon actions; it does not run the ranged recipes this page decodes.
