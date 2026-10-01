# NEXT CHAT HANDOFF — GFZ/GZF V121 WIP 761B — GM160 RECOVERY TRANSFER + GN READ-ONLY CLOSURE — 160 PERSISTED UNRESOLVED / 2 STRONG GN ROWS READY FOR EXACT-CURRENT MUTATION

**Date:** 2026-09-01  
**Project:** For Xeavin — FFXII TZA authoritative GFZ/GZF full-executable reconstruction  
**Semantic branch:** `761B`  
**Status:** **PERSISTENCE_CERTIFIED_GM160_RECOVERY_TRANSFER / GN_READ_ONLY_ANALYSIS_COMPLETE_FOR_TWO_PROTECTED_HOLDS / NO_GN_MUTATION_YET / NONCANONICAL V121 WIP**

# 0. READ THIS FIRST — EXACT CONTINUATION CONTRACT

This handoff is written so a chat with **no prior GFZ context** can continue safely.

The project is reconstructing an authoritative, evidence-backed semantic map of the **entire 38,161-function `FFXII_TZA.exe`**, not merely XIIOnline-relevant functions. XIIOnline determines research priority because gameplay/network seams are immediately useful, but it is **not** the final scope or stopping condition.

The package contains the actual usable persistence-certified GM160 recovery-transfer GZF and all evidence/tools needed to continue. **Use that GZF as the physical parent. Do not silently substitute an older GZF.**

Current certified persisted state is still:

- internal functions: **38,161**
- explicitly accounted: **38,001**
- unresolved: **160**
- explicit coverage: **99.58072%**
- PrimaryOwner/CodeDomain overlap: **0**

This chat performed substantial **read-only GN analysis** but deliberately did **not** mutate the GZF. Two of the previously protected 160-current holdouts now have strong, complete-body semantic proposals:

1. `00313A00` — `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`
2. `002F7380` — `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

These are **proposed rows only**. The next chat must first fresh-import the supplied GM160 GZF, reproduce its certified state, regenerate/verify the 160-current residual, exact-current-body fence both rows, and only then mutate if they still pass.

If both pass and are applied/persisted correctly, the prospective ledger would be:

- explicit: **38,003**
- unresolved: **158**
- coverage: **99.58596%**

That prospective state is **not yet a checkpoint**.

---

# 1. WHAT GFZ/GZF WORK IS — FIRST-TIME-CHAT ORIENTATION

The GFZ/GZF is the durable Ghidra reconstruction of FFXII TZA's native executable semantics. The job is not merely naming functions. The goal is to reconstruct, with audit-grade evidence:

- which subsystem truly owns a state/resource/lifecycle transaction;
- what each function actually implements at mechanism level;
- important globals/fields/records/tables;
- state machines and native transitions;
- call chains and downstream side effects;
- library/middleware mechanisms;
- authored resource/script relationships;
- native seams useful to XIIOnline and future tooling;
- enough exact provenance that every semantic mutation can be replayed, challenged, diffed, packed, reopened, and audited independently.

Two semantic layers must stay separate:

## V120 `PrimaryOwner`
Answers:

**Which FFXII subsystem owns the state/resource/lifecycle transaction?**

PrimaryOwner is an authority classification. It must never be inherited from callers, address neighborhoods, references, or convenience.

## V121 `CodeDomain`
Answers:

**What mechanism/library/runtime behavior does the function implement?**

CodeDomain can classify math, containers, middleware, runtime helpers, rendering mechanisms, callbacks, reflection, etc. without granting PrimaryOwner.

These layers are intentionally orthogonal. **Cross-layer overlap must remain 0.**

100% explicit accounting is not automatically “GFZ finished.” After closure, a deep whole-executable audit must still look for better names, signatures, structures, field semantics, state machines, native transitions, cross-function inconsistencies, stale evidence, overbroad classifications, and hidden contamination.

---

# 2. PHYSICAL AUTHORITY / VERSION RULES

## 2.1 Current physical continuation parent

Use:

`FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GM160_RECOVERY_TRANSFER_99P58_2026-08-31.gzf`

- size: **82,110,895 bytes**
- SHA-256: `381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b`
- deterministic fresh-reopen annotation snapshot SHA-256: `d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20`
- embedded authorized EXE SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

The GZF is included at package root. The game EXE is **not** bundled.

## 2.2 Historical GM distinction

Historical GM was separately persistence-certified at the same ledger depth:

`FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_CORRECTED_POST_CS_AUDIT_GM_99P58_2026-08-31.gzf`

- size: **82,126,436 bytes**
- SHA-256: `7b637b471ec66f3fc44efca88f956b52230599cb5d8dff0452743187e1b0d1b0`
- snapshot: `b4491ebbf9dc40a49830fd04c4c4754679ce8e120f3c8bc6bbab041204cf2cff`
- explicit/unresolved: **38,001 / 160**

That original historical GM binary was unavailable when the recovery-transfer package was built. The current GZF therefore reconstructs the same ledger depth from certified provenance but **does not claim byte identity** with historical GM and does not claim to reproduce the hidden historical GI→GK rows exactly.

Historical GM remains provenance authority; the supplied recovery-transfer GZF is the **actual physical continuation parent**.

## 2.3 Canonical V120 remains final-replay parent

V121 is still noncanonical WIP.

Canonical V120 SHA-256:

`507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9`

When V121 semantic closure and deep audit are truly complete, replay the complete proven V121 delta deterministically onto a **fresh import of canonical V120**, then independently pack/reopen/verify before declaring canonical V121.

Do not canonicalize by renaming this WIP GZF.

## 2.4 Superseded CS branch

Forbidden as continuation parent:

`cd50cea3fa7449e45d6499fa3e0311e467cb497b3f1dddeb4fe256550402c92b`

That old 99.00422% CS branch overread PE `.pdata`, `.xdata`, unwind and EH/IP-state metadata as semantic registration evidence. Corrected audit re-proved 186 functions and rejected 182.

**Never restore those 182 rejected rows without new independent proof.**

---

# 3. EXACT CURRENT CERTIFIED MACHINE STATE

| Item | Current value |
|---|---:|
| Internal functions | **38,161** |
| PrimaryOwner | **9,409** |
| PrimaryOwner categories | **22** |
| FinalNoPrimaryOwner | **585** |
| V121 CodeDomain | **28,007** |
| Explicitly accounted | **38,001** |
| Unresolved | **160** |
| Coverage | **99.58072%** |
| Cross-layer overlap | **0** |

PrimaryOwner category counts inherited from canonical V120:

- ActorEntity 235
- Audio 2,064
- CombatAI 43
- CombatAction 134
- CombatFormula 198
- CoreRuntimeScheduling 73
- Input 1,047
- Items/Equipment/Shops/License 70
- Movement 485
- Party 79
- Platform/Online/Achievements 59
- Presentation 1,564
- RNG 18
- Resource 572
- Rewards/Progression/Economy 38
- Save/Load/Settings 87
- Script/VM Native Bridge 1,900
- Spawn/Encounter/Lifecycle 52
- Status/Periodic/Terminal 24
- Story/Event/Quest/Hunt 15
- UI 544
- WorldAreaField 108

---

# 4. EXACT CURRENT 160-RESIDUAL FACTS

The exact current residual was regenerated from the **fresh-reopened GM160 recovery-transfer GZF**.

- address file: `evidence/GM160_CURRENT160_ADDRS.txt`
- address-list SHA-256: `fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a`
- unresolved functions: **160**
- incoming data references: **382**
- functions with direct PrimaryOwner references: **2**
- direct owner references: **4**
- direct strings: **0**
- exact-body clone hits: **0**
- qualified Phyre/std/EASTL symbol hits: **0**

The two owner-referenced current holdouts are exactly:

- `002F7380` — one incoming Movement owner reference
- `00313A00` — two CombatAction and one WorldAreaField owner references

Owner references alone were intentionally insufficient to classify them. This chat resolved them only after complete-body and independent semantic challenge.

---

# 5. WHAT THIS CHAT ACTUALLY DID — CONCRETE DISCOVERIES

This section is important. The project requires reporting **what native mechanisms were learned**, not merely counts/categories.

## 5.1 Protected hold `00313A00` — now a strong GN proposal

### Proposed CodeDomain

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

### Exact body

- 289 bytes
- exact authorized-EXE body SHA-256: `c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246`

### Native mechanism

`00313A00` rebuilds **row 2** of a central 16-row × 32-bit gameplay capability/inhibition policy.

Exact primitives:

- `002E1C20(row, bit)` — set bit
- `002E1CA0(row, bit)` — clear bit
- `002E0FA0()` — OR-reduce the 16 policy rows into the effective mask

Row-2 bits reconciled by `00313A00`:

`0,1,2,3,4,5,6,7,8,10,11,12,20`

Inputs include:

- `02089350` — canonical CombatAction current-selected-BattleUnit state;
- WorldAreaField policy through `00377C20`;
- additional runtime/global predicates.

The function does **not** inherit CombatAction or WorldAreaField PrimaryOwner from those inputs.

### Native UI-request projection

`00254500` translates aggregate gameplay-policy bits into a native UI-request inhibit mask. The exact requests inhibited by the `00313A00` row-2 contribution are:

**1, 2, 3, 5, 14, 21**

Latest request identities:

| Request | Strongest current identity |
|---:|---|
| 1 | **Battle Menu open/request** |
| 2 | **Party Menu / Menu Screen open/request family** |
| 3 | **Field party-leader selection/change** |
| 5 | **Field free-target actor cycle / target selection** |
| 14 | **Valid persistent/current fullscreen UI mode/request slot 14; friendly name still open** |
| 21 | **Valid generic/transient UI request slot 21; friendly name still open** |

Request 2 is strongly tied to Triangle/Party Menu input and is also the default/fallback native fullscreen-menu request family. Its parameter values (`0`, `0x21`, `0x40`, `0x41`, `0x42`, dynamic values) must **not** be casually named as individual Party Menu submenus without independent evidence.

Request 14 is structurally stronger than 21: native current-fullscreen-mode translator `002E0E30` represents modes `0..19`, and current mode 14 maps back to request 14. No ordinary hardcoded retail producer or friendly screen/resource name was found.

Request 21 is router-valid but is not represented in that persistent fullscreen-mode 0..19 translator. Keep numeric.

The debug ScriptVM namespace contains `debug_open_triangle_menu2`, which can inject arbitrary numeric request IDs through the ordinary native request mailbox. That proves IDs 14/21 are exercisable slots but does not name them.

### Meaning for XIIOnline

This policy is local gameplay/UI capability state, not server world authority. Do not network request-mask bits themselves. Multiplayer-significant state underneath menus/leader/target operations must be synchronized at its real owner:

- party composition/identity;
- equipment;
- inventory;
- licenses;
- Gambits;
- stable actor identity;
- action intent.

Raw local target/actor handles are process-local and must not be wire identities.

---

## 5.2 Protected hold `002F7380` — now a strong GN proposal

### Proposed CodeDomain

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

### Exact body

- 723 bytes
- SHA-256: `15594f6181100f7fa10ac8a770566d60b963e47c93176fd7d7f33152b3ac8583`

### What it actually does

It rebuilds a derived Presentation table for FFXII's retained **PlayStation 2 GS-compatible texture/local-memory model**.

The source record bank uses 0x60-byte image/texture records. Exact helper `00466190` computes complete mip-chain storage by repeatedly calling the native format-size helper while halving dimensions.

The routine:

1. computes each texture's full mip-chain footprint;
2. computes maximum/aggregate image-storage metrics;
3. clears derived reference/slot state;
4. counts references from 0x30-byte reference descriptors;
5. ignores textures referenced at most once;
6. admits multiply referenced texture mip chains only while cumulative accepted storage remains strictly below the available aligned GS-local-memory budget;
7. gives accepted textures compact consecutive slot IDs;
8. gives rejected/unselected textures `-1`;
9. allocates and zeroes one **40-byte derived slot record** per admitted texture.

### Why this is specifically Legacy PS2 GS

Internal executable evidence includes:

- exact GS PSM-family literal values;
- exact GS page geometry;
- effective **4 MiB** local-memory model;
- **8 KiB** allocation/page quantum;
- literal GS image-transfer register IDs `0x50/0x51/0x52/0x53` in sibling Presentation code;
- canonical V120 Presentation ownership of the surrounding graphics-transfer family.

`00466220` recognizes exactly PSM values `0x14`, `0x24`, `0x2C`, corresponding to GS 4-bit indexed texture formats.

Native format sizing `003A1E50` reproduces GS page geometry and a minimum allocation unit of `0x800` 32-bit words = **8 KiB**.

Budget helper `00467AA0` derives an `0x800`-aligned threshold from an effective `0x100000` 32-bit-word arena = **4 MiB**.

### Cross-category boundary

A Movement-owned dirty/resource dispatcher calls `002F7380`, but older V120 boundary evidence already distinguished:

- Movement owns the upstream resource/dirty transaction;
- `002F7380` belongs to the Presentation dataset side.

Caller ownership is not inherited.

### Native seam implication

`002F7380` is **derived state**, not an authoritative configuration API. Upstream Movement reconfiguration `0026E8D0` sets resource configuration/dirty state; `0026E290` observes the dirty state and invokes `002F7380` normally.

For native-coherent code, prefer the upstream owner transition and let this table regenerate naturally.

---

# 6. MAJOR SURROUNDING DISCOVERIES FROM THIS CHAT

These functions were largely already explicit/canonical, so the findings below improve the semantic graph and XIIOnline architecture but **do not increase the persisted explicit count**.

## 6.1 Combat native-seam correction

An earlier read-only note incorrectly treated `00313DB0` as though it could be an arbitrary BattleUnit-selection API.

That is **withdrawn**.

`00313DB0` is a zero-argument consumer of a native **64-entry presentation-slot-ready BattleUnit ID ring**. The producer lives in the committed standard-action/presentation lifecycle.

The established higher multiplayer command seam remains the native `BattleUnit_IssueCommand` family, with stable network actor/target identity translated to receiver-local native focus/BattleUnit/BattleStats identities.

Do not:

- write `02089350` directly;
- insert arbitrary IDs into the presentation-ready ring;
- call `00313DB0` as a remote-command substitute;
- call `00313A00` merely to repair consequences of lower-level direct writes.

## 6.2 Weather Slot native architecture

Authored script call mapping proves:

- `0x021A setweatherslot(int)`
- `0x040C getweatherslot()`

VM wrappers are intent evidence only. **Do not use VM wrappers as XIIOnline replay seams.**

Lower native getter:

`00265920` — current Weather Slot 1..3, honoring debug override.

Lower native apply owner:

`0026D910` — applies a chosen Weather Slot, commits/preserves persistent slot state as appropriate, materializes authored field/environment parameters, and performs downstream Presentation refresh.

Persistent payload:

- `+0x1060` — zero-based durable Weather Slot 0..2
- `+0x1061` — **world-transition `bInitializationRestoreState`**, not a Weather-owned flag

Earlier working descriptions of `+0x1061` as merely “preserve weather on next apply” are superseded. Weather consumes this broader restore policy during initialization/restore.

## 6.3 Native Weather probability is EBP/script-authored

Native `002658B0` reads script-header offset `+0x64`.

Bundled ff12-script source proves that exact section is serialized/deserialized as:

`weatherProbability`

The native model is:

1. read current-slot `weatherProbability`;
2. 0 → cannot retain current slot;
3. >=100 → always retain;
4. 1..99 → native MT19937 roll 0..99;
5. on failure, select another eligible Weather Slot;
6. apply the resulting slot through `0026D910`.

This is not a generic MapRef probability. Earlier wording that attributed the probability table to MapRef is superseded.

## 6.4 Weather roll timing

The normal Weather transition roll occurs during a **primary ActorManager (index 0) field-runtime initialization transaction**, guarded by a one-shot initialization bit.

It is not proven as a free-running periodic weather timer.

For XIIOnline, authoritative weather generation should preserve native EBP `weatherProbability` and MT19937 behavior, then synchronize the **committed Weather Slot outcome**.

Do not independently reroll on every client.

## 6.5 Runtime Weather vs field-resource initialization

Runtime authored `setweatherslot` and field initialization are different native transactions.

Runtime `setweatherslot` delegates to `0026D910`, refreshing WorldAreaField/Presentation state. It does **not** directly force the Movement/LegacyPS2GS field-resource reconfiguration path.

During field initialization/re-entry, the committed Weather Slot is published into additional resource/environment channels and reaches Movement resource selection; that eventually dirties and rebuilds the LegacyPS2GS table through `002F7380`.

Do not force the field-init Movement/GS rebuild after every networked runtime Weather change unless the engine itself enters that lifecycle.

## 6.6 `MWeather` authored resource

The executable contains authored resource name:

`MWeather`

Its packed record is **9 bits per selector × Weather Slot combination**:

- bits 0..2 — 3-bit Presentation preset/mode
- bits 3..6 — 4-bit azimuth/orientation sector
- bits 7..8 — 2-bit elevation/orientation class

Presentation uses:

- preset 0..7;
- 16 azimuth sectors at `π/8` = 22.5°;
- elevation classes centered around 0°, +30°, or -30° branches;
- receiver-local procedural random angular perturbation;
- normalized embedded visual-controller basis.

The final visual basis feeds the large embedded Presentation visual evaluator. Do not overname it as “sun direction” or another global lighting term without stronger evidence.

## 6.7 MWeather also affects gameplay CombatFormula

The same MWeather 3-bit preset is collapsed into gameplay class:

- preset 0 → class 0
- presets 1..3 → class 1
- presets >=4 → class 2

Class 2 has the exact native **strong-wind** combat effect:

- Fire ×1.2
- Water ×0.5
- Wind ×1.2

Thus MWeather is not merely visual input.

## 6.8 Weather/Terrain factorized CombatFormula

Canonical `0038B220` applies pre-affinity environment/terrain element scaling.

Native global environment classes:

- class 0 — Rain behavior: Fire ×0.5, Lightning ×1.2
- class 1 — Sand base behavior: Earth ×1.2
- class 2 — Snow/Ice base behavior: Ice ×1.2
- class 3 — Fog behavior: Water ×1.2

Target-local terrain classes:

- local 0 — Water terrain: Lightning ×1.2, Water ×1.2, Earth ×0.5
- local 1 — Sand terrain: Earth ×1.2
- local 2 — Snow/Ice terrain: Ice ×1.2

MWeather strong wind multiplies with those layers. This naturally produces Heavy Rain, Sandstorm, Snowstorm, etc. without a separate hardcoded formula for every named combination.

The later canonical element-affinity stage remains separate.

## 6.9 Bow/Crossbow recipes internally closed

ActionDefinition `+0x08` selects one of **109** formula recipes. Each recipe contains a preview-side calculator list and a committed-result calculator list.

Recipe 25 is the **Bow-family** recipe:

- severe-weather accuracy ×0.8
- committed damage uses `Strength × (Level + Speed) / 218`
- specialized ranged defensive outcome resolver includes an additional avoid-threshold branch

Recipe 26 is the **Crossbow-family** recipe:

- severe-weather accuracy ×0.5
- committed damage uses `Strength × (Level + Strength) / 256`
- sibling ranged defensive resolver omits that additional avoid branch

These identities are supported by multiple independent native differences, not merely the familiar weather percentages.

## 6.10 Status vs Augment namespace correction

This correction is critical.

BKBI has two relevant bit layers:

- `+0x68` — ordinary/mutable status-effect layer
- `+0x78` — derived/automatic effect/augment layer

`BattleFormula_BuildEvaluationContext` ORs both layers into one merged formula bitmap. Equal numeric bit positions therefore can represent **different semantic namespaces** before the merge.

Public Xeavin Workshop source independently closes:

### Status namespace
- bit 2 = Petrify
- bit 16 = Disease
- bit 17 = Lure

### Augment namespace
- bit 2 = AccuracyBoost
- bit 16 = Weatherproof
- bit 17 = Thievery

The native Weather/Terrain element-scaling bypass uses merged bit **16**. In the derived augment namespace this is **Weatherproof / Ignore Weather & Terrain**.

Bow/Crossbow severe-weather accuracy bypass uses merged bit **2**. In the derived augment namespace this is **AccuracyBoost**.

Because the formula bitmap merges the layers, same-position mutable statuses can alias those bits after merging. Preserve that as an observed engine property; do not collapse the namespaces.

## 6.11 Shared procedural Presentation PRNG

Weather decision RNG and Presentation randomization are separate.

Presentation helper `003D8E50(amplitude)` consumes a shared bit-feedback pseudo-random float stream, not gameplay MT19937. Each nonzero call advances the recurrence seven times and returns a scaled `[0, amplitude)` sample from an intermediate state.

The Presentation backend orientation rebuild calls it twice, so one backend rebuild consumes 14 recurrence steps.

Broad bootstrap contains two consecutive `0026D910(1)` environment applies. The first restore-aware apply is overwritten in final visible environment state by the second baseline slot-1 apply, but it is not entirely idempotent because it consumes transition state and advances this shared procedural Presentation random stream.

Do not interpret that Presentation PRNG as authoritative world RNG.

---

# 7. SUPERSESSIONS / CORRECTIONS — READ THIS BEFORE USING THE GN EVIDENCE

The `evidence/gn_read_only/` directory preserves the reasoning trail. Some older documents are intentionally kept for provenance but are superseded in part.

Use this priority order:

1. `V121_GN_INPUTGAMEPLAY_UI_REQUEST_MAPPING_SUPERSEDING_2026-09-01.md`  
   **Latest request-map authority** for `00313A00`.

2. `V121_GN_WEATHER_TERRAIN_AUGMENT_NAMESPACE_CORRECTION_2026-09-01.md`  
   Supersedes stale status/augment-bit interpretation. Weatherproof = derived augment bit 16; AccuracyBoost = derived augment bit 2.

3. `V121_GN_BOW_CROSSBOW_RECIPE_AND_WEATHER_FORMULA_CLOSURE_2026-09-01.md`  
   Use recipe/Bow/Crossbow closure, but apply the augment-namespace correction above to any stale status-only wording.

4. `V121_GN_MWEATHER_COMBATFORMULA_AND_PRESENTATION_ADDENDUM_2026-09-01.md`  
   Current corrected local copy contains the corrected `00389610` SHA.

5. `V121_GN_WEATHER_TRANSITION_RESTORE_AND_PRIMARY_MANAGER_CORRECTION_2026-08-31.md`  
   Supersedes the earlier Weather-specific interpretation of persistent `+0x1061`.

6. `V121_GN_WEATHER_PROBABILITY_NATIVE_APPLY_CORRECTION_2026-08-31.md`  
   Supersedes the earlier generic/MapRef attribution for `weatherProbability`; the probability table is EBP/script-authored.

7. `V121_GN_WEATHER_RUNTIME_VS_FIELD_INIT_RESOURCE_SPLIT_2026-08-31.md`  
   Corrects the idea that every runtime Weather change immediately triggers Movement/LegacyPS2GS field-resource rebuild.

8. `V121_GN_NATIVE_SEAM_CORRECTION_SUPERSEDING_2026-08-31.md`  
   Supersedes the earlier implication that `00313DB0` is an arbitrary selected-BattleUnit replay API.

9. `V121_GN_READ_ONLY_LEGACY_PS2GS_ADDENDUM_2026-08-31.md`, `V121_GN_READ_ONLY_INPUTGAMEPLAY_POLICY_ADDENDUM_2026-08-31.md`, and `V121_GN_READ_ONLY_FOLLOWUP_2026-08-31.md`  
   Earlier detailed evidence remains useful where not superseded.

10. `V121_GN_READ_ONLY_PROPOSED_ROWS_2026-08-31.md`  
    Original two-row GN proposal provenance.

Do **not** let an older addendum override a later correction.

---

# 8. EXACT STATE OF GN WORK AT HANDOFF

## Persisted GN mutations performed in this chat

**0**

No annotation/tag/comment was written to the GM160 GZF.

## Strong read-only rows ready for exact-current challenge

### `00313A00`
Proposed:

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

Body:
- 289 bytes
- SHA `c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246`

### `002F7380`
Proposed:

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Body:
- 723 bytes
- SHA `15594f6181100f7fa10ac8a770566d60b963e47c93176fd7d7f33152b3ac8583`

## Intentionally still open semantic subquestions

These are **not blockers** to applying the two conservative CodeDomain rows if exact-current GZF challenge passes:

- friendly/player-facing identity of native UI request 14;
- friendly/player-facing identity of request 21;
- exact authored/designer name of the MWeather selector paired with Weather Slot;
- exact designer reason for broad bootstrap's two consecutive environment applies;
- whether certain same-bit status/augment aliases were intentional design shortcuts or incidental bit-namespace collisions;
- higher non-VM receiver-safe Weather apply seam, if one exists above `0026D910` with demonstrably better downstream coherence.

Preserve these as open rather than overnaming them.

---

# 9. IMMEDIATE NEXT WORK — GN MUTATION GATE

The next chat should **not restart read-only discovery from scratch** for the two holds.

Exact sequence:

1. Verify `SHA256SUMS.txt` and the new package seal.
2. Verify the bundled GM160 GZF exact size/hash.
3. Import the GZF into a **brand-new writable Ghidra project** with auto-analysis disabled.
4. Reproduce exactly:
   - 38,161 functions
   - 38,001 explicit
   - 160 unresolved
   - 99.58072%
   - overlap 0
5. Reproduce deterministic snapshot:
   `d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20`
6. Extract/verify embedded EXE SHA:
   `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`
7. Regenerate the current unresolved list from that fresh parent. Require exactly 160 and residual SHA:
   `fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a`
8. Verify `00313A00` and `002F7380` are still unresolved.
9. Recompute complete exact-current body size/hash for both.
10. Re-run caller/callee/data/structure challenge against the imported GM160 state.
11. Reject a row on any body/classification drift.
12. Build a GN pre-enrichment manifest only for rows that still pass.
13. Run exact-current enrichment; preserve the specific evidence sentences.
14. Apply with **exact expected count**, never “whatever passes.”
15. Snapshot all 38,161 functions post-mutation.
16. Whole-project diff against fresh parent. Require:
    - only intended functions changed;
    - only intended comment/tag fields changed;
    - function additions/removals = 0/0;
    - tag removals = 0;
    - body/range/name/prototype/thunk drift = 0;
    - immutable drift = 0.
17. Report the actual semantic discoveries to the user, not just count movement.
18. Close the target DomainFile.
19. Pack in a **separate headless invocation** with `PackClosedDomainFile.java`.
20. Require preconditions:
    - `open=false`
    - `busy=false`
    - `changed=false`
    - preferably `canSave=false`
    - explicit `PACK_PASS`
21. Verify plausible resulting file size/hash.
22. Import the packed GZF into a **completely new project**.
23. Reproduce post-mutation snapshot, ledger, overlap and embedded EXE.
24. Only then claim a persistence-certified GN checkpoint.
25. Regenerate the unresolved residual from the fresh post-GN state. Never reuse the old 160 list after mutation.

If both rows pass, expected persisted arithmetic after proper certification:

- functions: 38,161
- explicit: **38,003**
- unresolved: **158**
- coverage: **99.58596%**
- overlap: 0

If one row fails exact-current challenge, apply only the passing row with exact expected count and report why the other remained unresolved.

---

# 10. AFTER THE TWO GN ROWS — CONTINUE FULL-EXECUTABLE CLOSURE

After a fresh post-GN residual is generated:

1. rank the remaining tail by **complete-body mechanism evidence**, not address neighborhood;
2. group small coherent families where shared structure genuinely helps;
3. decompile/challenge only bounded batches;
4. use callers/callees, actual data refs, RTTI/vtables, strings, resources, script data and upstream source as independent evidence;
5. create pre-enrichment rows only when semantics survive challenge;
6. exact-current enrich;
7. apply exact expected count;
8. whole-project diff;
9. separate closed pack;
10. fresh reopen;
11. regenerate residual;
12. repeat.

The entire current 160-address list is included in Appendix A and as `evidence/GM160_CURRENT160_ADDRS.txt`.

---

# 11. NON-NEGOTIABLE GFZ EVIDENCE HIERARCHY

Prefer evidence roughly in this order:

1. **Complete exact-current body**: disassembly/decompilation/control flow, field accesses, constants, loops, native ABI, real mechanics.
2. Authored/runtime strings directly tied to the body/data.
3. Qualified symbols when genuine.
4. Real MSVC RTTI/vtables/class descriptors with independently verified object identity.
5. Exact-body clones with unanimous interpretation.
6. Coherent upstream source/library matches.
7. Genuine typed pointer/vtable/static registration evidence **after excluding exception metadata**.
8. Actual code address-taking/data-reference context.
9. ff12-script / EBP / VBF / other game-data schema corroboration.
10. LiveLab/runtime/CE corroboration when it materially improves certainty.
11. Call graph/neighborhood only as supporting context.

A stronger later evidence source may supersede an earlier tentative label. Preserve the correction trail and explain why.

---

# 12. ABSOLUTE ANTI-CONTAMINATION RULES

Never use these shortcuts as semantic proof:

- caller ownership → callee ownership;
- address adjacency or address-range ownership;
- “looks like it belongs to X” without complete mechanics;
- owner references alone;
- generic category filler to force 100%;
- stale residual lists after mutation;
- PE `.pdata` / `.xdata`;
- unwind records;
- EH maps;
- IP-to-state maps;
- `_IMAGE_RUNTIME_FUNCTION_ENTRY` metadata;
- exception tables misread as callback/vtable/registration tables.

Corrected CS audit exists because this mistake already happened once.

PrimaryOwner must follow true state/resource/lifecycle authority.

CodeDomain may describe a generic mechanism without changing PrimaryOwner.

Preserve unresolved status whenever evidence is insufficient.

---

# 13. EXACT-CURRENT-BODY FENCING RULE

Every proposed mutation row must be tied to the **current physical parent body**, not an older EXE listing or historical GZF.

Before mutation:

- confirm entry address;
- confirm complete body extent;
- recompute body hash;
- confirm function/range identity;
- confirm current annotation state;
- enrich current body with exact evidence;
- reject drift.

Do not apply a historical manifest blindly to a newer checkpoint.

---

# 14. MUTATION / SNAPSHOT / DIFF RULE

After every mutation batch:

- snapshot the **entire project**, all 38,161 functions;
- diff against the exact fresh parent snapshot;
- require exact intended changes;
- immutable drift must be 0 unless explicitly authorized as a separate operation;
- no function additions/removals;
- no accidental tag removals;
- no name/prototype/thunk/range/body drift merely because analysis tools touched the project.

Small batch size is preferred over large speculative batches.

---

# 15. PACK / PERSISTENCE RULE

A modified working Ghidra project is **not** a durable GFZ checkpoint.

Mutation/save and pack are separate operations.

Before packing, the target DomainFile must be closed and stable:

- `open=false`
- `busy=false`
- `changed=false`
- preferably `canSave=false`

Run `PackClosedDomainFile.java` in a separate invocation.

Require explicit:

`PACK_PASS`

File existence is not proof of successful packing.

After pack:

- check size/hash;
- fresh-import into a new project;
- rerun coverage;
- rerun full snapshot;
- verify overlap;
- extract embedded original;
- reproduce expected state.

Only then call the checkpoint persistence-certified.

---

# 16. TIMEOUT / HANG RECOVERY RULE

A UI/tool timeout proves neither success nor failure.

On interruption:

1. inspect files/projects/logs first;
2. determine whether mutation actually completed;
3. inspect snapshots/diffs;
4. inspect pack log for `PACK_PASS`;
5. check file size/hash;
6. treat partial/truncated packs as invalid;
7. if mutation completed and exact post-state is intact, **do not duplicate the mutation**—rerun only the failed pack/reopen/evidence step;
8. clear stale locks only after confirming no live process owns them;
9. finish a human-readable persistence seal.

Never roll back merely because the chat response timed out.

---

# 17. TOOLING / SCRIPT RULES

Primary annotation environment:

- Ghidra **12.1.2**
- Java **21**
- GhidraMCP/Bethington **6.0.0** when useful

Additional independent challenge tools are allowed when they materially improve certainty:

- radare2
- LIEF
- Capstone
- angr
- DynamoRIO
- CE/runtime evidence
- LiveLab
- upstream source/library repositories
- VBF/EBP/game-data tooling

The authoritative GFZ mutation identity remains the exact current Ghidra body/persisted annotation state.

### Important script argument traps

`DecompileAddressFileBounded.java`

**OUTPUT FILE, ADDRESS FILE, TIMEOUT SECONDS**

`DumpUnresolvedMechanismFeatures.java`

**OUTPUT FILE, MAX_INSNS**

`EnrichCurrentBodyManifest.java`

**INPUT, OUTPUT**

`ApplyCurrentBodyCodeDomainBatch.java`

**MANIFEST, BATCH_ID, EXPECTED_COUNT, SUMMARY**

A bad invocation must fail before mutation.

Snapshot:

`GFZFunctionAnnotationSnapshotV2.java`

Diff:

`tools/analysis_scripts/diff_fas2.py`

Pack:

`PackClosedDomainFile.java`

Read `tools/README_GFZ_TOOL_USE_2026-08-30.md` before running scripts.

### Archive rule

**Do not use the 7z CLI.**

Use standard ZIP handling or system libarchive for archive/multipart work.

---

# 18. ff12-script / EBP / VBF / SOURCE RULE

The package includes `tools/ff12-script-master.zip`.

Use it to corroborate:

- native ScriptVM call names;
- authored script header fields;
- EBP data layout;
- Weather probability;
- other script/resource semantics.

But:

- ScriptVM wrapper identity is evidence of authored intent, not automatic ownership;
- **do not use VM wrappers as XIIOnline replay seams**;
- descend to the underlying native owner/apply transaction;
- ff12-script alone cannot assign PrimaryOwner.

Same rule for VBF/other game-data source: use it as independent schema/semantic evidence, not as automatic authority.

---

# 19. XIIOnline “BEST NATIVE SEAM WINS” RULE

GFZ addresses named in prompts are **starting points, not sacred interfaces**.

If further Ghidra, ff12-script/VBF/EBP, CE, LiveLab, other-mod or runtime research discovers a higher-level native transition that:

- achieves the same intended outcome;
- performs fewer direct writes;
- allows more native downstream coherence;
- better preserves mod compatibility;
- reduces duplicated engine logic;

prefer the better seam when concrete evidence supports it.

Document:

- old seam;
- new seam;
- evidence;
- native call chain/downstream effects;
- why it is better;
- compatibility/risk impact;
- tests needed.

### Calls-only / coherence preference

Prefer native calls/state transitions over direct memory writes.

Do not periodically overwrite engine state (“every X seconds”) to fight native logic.

Do not forward multiple low-level derived writes when one higher native owner transition naturally regenerates them.

### Stable identity rule

Process-local pointers, BattleUnit handles, focus handles, BattleStats slots, resource pointers and UI actor handles are not network identities.

XIIOnline must carry stable logical/network identity and translate to each receiver's local native identity before entering the native seam.

---

# 20. STATIC GFZ PROOF VS RUNTIME MULTIPLAYER PROOF

GFZ semantic reconstruction is static/native-code understanding.

It can identify:

- owner transitions;
- better native calls;
- state machines;
- authored data dependencies;
- combat/weather/menu mechanics;
- useful telemetry points.

It does **not** replace real linked XIIOnline certification.

Runtime observations may corroborate or challenge GFZ semantics, but they must be reconciled with exact code evidence.

---

# 21. USER-FACING PROGRESS REPORTING RULE

Every continuation response must tell the user what was actually learned.

Good examples:

- “this rebuilds a 4 MiB GS-local-memory texture-mip slot table”;
- “this maps Weather Slot through EBP weatherProbability and native MT19937”;
- “this inhibits Battle Menu / Party Menu / leader change / target cycling”;
- “this is the Bow `STR*(Lv+SPD)/218` formula”;
- “this is Weatherproof augment bypass of Weather/Terrain scaling.”

Bad progress reports:

- “moved 2 functions”;
- “more Presentation explicit”;
- “generic owner resolved”;
- percentages with no semantic explanation.

Always report both:

1. count/coverage movement; and
2. concrete native meaning discovered.

---

# 22. CORRECTED HANDOFF PACKAGING RULE

The older 2026-08-30 build standard said not to bundle GZFs. That rule is **superseded for GFZ continuation** by the corrected GM160 handoff rule.

A GFZ next-chat handoff must now include the **latest usable persistence-certified GZF itself** inside the handoff ZIP.

If a platform transfer limit genuinely prevents bundling, the exact same GZF must be supplied as a separate same-response artifact with explicit size/hash binding.

Never leave the next chat with only a hash for an unavailable GZF.

Still do **not** bundle the game EXE.

A proper package includes:

- main handoff;
- usable persistence-certified GZF;
- persistence seal;
- current-state JSON;
- next-frontier JSON;
- current residual/evidence;
- mutation/diff/pack/fresh-reopen evidence;
- relevant source context;
- scripts/tools needed to continue;
- research source such as ff12-script;
- SHA256 manifest;
- package seal;
- supersession index when interpretations changed.

---

# 23. FINAL V121 CONDITION

Even if unresolved reaches 0:

1. do a deep whole-executable semantic audit;
2. improve weak names/signatures/structures where stronger proof exists;
3. challenge every V121 delta for owner inheritance;
4. challenge EH/unwind contamination;
5. challenge stale evidence and overbroad middleware/runtime labels;
6. reconcile conflicts;
7. confirm overlap 0;
8. deterministically replay the complete proven V121 delta onto fresh canonical V120;
9. pack/reopen independently;
10. verify embedded EXE and complete snapshot;
11. only then call V121 canonical.

**100% explicit accounting alone is not final GFZ completion.**

---

# 24. FILES THE NEXT CHAT SHOULD OPEN FIRST

In this order:

1. `NEXT_CHAT_HANDOFF_2026-09-01_Gfz9_V121_GM160_GN_READ_ONLY_FINAL_160.md`
2. `GFZ_V121_CONTINUATION_REQUIREMENTS_2026-09-01.md`
3. `GFZ_HANDOFF_BUILD_STANDARD_2026-09-01.md`
4. `V121_CORRECTED_POST_CS_GM160_RECOVERY_TRANSFER_PERSISTENCE_SEAL_2026-08-31.md`
5. `V121_CURRENT_STATE_GM160_GN_READ_ONLY_2026-09-01.json`
6. `V121_NEXT_FRONTIER_GN_MUTATION_2026-09-01.json`
7. the bundled GM160 recovery-transfer GZF
8. `evidence/GM160_CURRENT160_ADDRS.txt`
9. `evidence/GM160_CURRENT160_STRUCTURE.tsv`
10. `evidence/GM160_CURRENT160_DATAREF_CONTEXTS.tsv`
11. `evidence/GM160_CURRENT160_MECHANISM_FEATURES.tsv`
12. `evidence/GM160_CURRENT160_NEIGHBORHOODS.tsv`
13. `evidence/GN_SUPERSESSION_INDEX_2026-09-01.md`
14. `evidence/gn_read_only/V121_GN_INPUTGAMEPLAY_UI_REQUEST_MAPPING_SUPERSEDING_2026-09-01.md`
15. `evidence/gn_read_only/V121_GN_READ_ONLY_LEGACY_PS2GS_ADDENDUM_2026-08-31.md`
16. `evidence/gn_read_only/V121_GN_WEATHER_TERRAIN_AUGMENT_NAMESPACE_CORRECTION_2026-09-01.md`
17. `tools/README_GFZ_TOOL_USE_2026-08-30.md`

Do not start by reading one old addendum in isolation; use the supersession index.

---

# 25. WHAT IS LEFT — FULL PROJECT VIEW

## Immediate

- persistence-gate and apply the two strong GN rows if exact-current checks pass;
- fresh-reopen certify;
- regenerate the residual.

## Remaining semantic tail

- continue through the remaining post-GN unresolved functions family-by-family;
- do not force weak closures merely to reach 100%;
- exploit exact residual evidence in the package.

## Open refinements from this chat

- UI request 14 friendly identity;
- UI request 21 friendly identity;
- exact MWeather selector authored name;
- exact higher-level purpose of the duplicate bootstrap environment apply;
- more exact authored names for some environment transition helpers;
- higher Weather receiver seam if later evidence proves a better non-VM owner transition.

## Whole V121 finalization

- deep adversarial audit;
- deterministic replay onto fresh canonical V120;
- pack/reopen verification;
- canonical V121 declaration only after all gates pass.

## XIIOnline remains a separate runtime program

GFZ discoveries should feed the multiplayer roadmap, but no static GFZ closure is a substitute for live 2/3/4-client certification, late join, reconnect, authority handoff, world persistence, combat, Weather, spawn eligibility, menus/time semantics, etc.

---

# 26. APPENDIX A — EXACT CURRENT 160 UNRESOLVED ADDRESSES

The authoritative machine-readable copy is `evidence/GM160_CURRENT160_ADDRS.txt`.

```text
00180A70
00188B10
0018EEE0
001B0CE0
001C22A0
001C2980
001D72F0
001D76A0
001D7A20
001D7DD0
001E59B0
001E5C40
001E8070
001E8580
001E9D20
001F57E0
0020AC30
0020ED30
0020F3E0
0020FF10
00226640
002376F0
0023ED80
0023EFC0
0023F8B0
00244A20
00245170
002455A0
00245E60
00246C20
00247AE0
00248A90
0024B580
0024B9B0
00256960
00256CA0
00258350
0026F470
00273BA0
00275570
002856B0
00287400
002875D0
0028A350
0028AAA0
0028B140
0028B860
0028BB50
0028DC00
00292B70
0029E3B0
002A0440
002A4430
002A4830
002A5020
002A86A0
002AAE40
002ABB20
002ABF70
002AC5F0
002AE610
002AF340
002AF960
002AFDC0
002B2150
002B2DF0
002B5390
002B6350
002B6DB0
002B8EE0
002BA310
002BCB00
002C3D70
002C7660
002C7B10
002C84E0
002D2600
002D4330
002D66D0
002D8D40
002DA2D0
002DA7C0
002DBDD0
002DC290
002DC7F0
002EE430
002F0280
002F67C0
002F7380
002FCCC0
00313A00
0032C650
0032D820
00364530
003649A0
00366110
00367200
00367AA0
00368010
0036A2A0
0036A570
00392A10
00392CE0
003AEF90
003BA7B0
003BA990
003BAC90
003BDDE0
003BDFF0
003BE3A0
003BE950
003BED70
003C1A20
003F3E40
003F8790
003FAF10
003FBE90
003FD360
003FDFE0
00402000
004027D0
00402F00
004044D0
004058E0
00407D10
004EDB50
004F5360
0053E0B0
0053E640
00564430
00564780
005651E0
00565720
00565A00
00565E00
00566680
005680E0
0056C490
0056E140
0056E880
0056F810
005709E0
005713C0
00571710
00571F60
00572920
005734C0
00573690
00573BE0
00576300
005771F0
0057CF20
0057D620
0057E6D0
005BF110
005C6770
005C6A90
005DC8D0
005DD890
005DF890
```

---

# 27. NEXT-CHAT STARTUP PROMPT

Use the following exact prompt if helpful:

`We are continuing the For Xeavin FFXII_TZA GFZ/GZF V121 full-executable reconstruction from the attached 2026-09-01 GM160+GN handoff package. Read the complete new handoff, continuation requirements, build standard, persistence seal, and GN supersession index before acting. The ZIP itself contains the usable persistence-certified GM160 recovery-transfer GZF; use that exact GZF as the physical continuation parent and do not substitute an older artifact. First verify the package hashes/seal and GZF size/SHA, fresh-import it into a brand-new writable Ghidra project with auto-analysis disabled, and reproduce 38,161 functions / 38,001 explicit / 160 unresolved / 99.58072% / overlap 0, deterministic snapshot d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20, authorized embedded EXE SHA 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, and the exact 160-current residual SHA fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a. Then exact-current challenge the two strong GN read-only proposals: 00313A00 = InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation and 002F7380 = Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild. If they still pass complete-body/current-state challenge, build an exact expected-count GN manifest, enrich current bodies, mutate only passing rows, whole-project FAS2 diff with immutable drift 0, close the target, pack in a separate invocation requiring PACK_PASS, fresh-import the pack into a completely new project, reproduce the exact post-state, regenerate the residual, and only then claim a persisted GN checkpoint. Preserve all GFZ evidence rules: full-executable scope, PrimaryOwner vs CodeDomain separation, no caller-adjacency ownership, no .pdata/.xdata/EH/unwind semantic contamination, no forced 100%, no VM wrappers as XIIOnline replay seams, best native seam wins, no 7z CLI, and always tell me what native behavior was actually learned rather than only counts/percentages.`
