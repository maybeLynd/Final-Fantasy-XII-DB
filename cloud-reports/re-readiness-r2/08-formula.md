# Reconstruction readiness, pass 2: 08-Combat-Formula

- **System folder:** `FFXII TZA/08-Combat-Formula/` (slug `08-formula`). All 22 `.md` pages in the folder and its
  subfolders were read. The member `.tsv` files were consulted only for headers and counts.
- **Stream:** R2, FABLE (r2-9). Pass 1 did **not** map this system, so this is the pass-1 task (part B of
  `docs/cloud-briefs/re-readiness-r2.md`): Interface, Gaps with a class column, Rating.
- **Snapshot:** `main` at `b23bdddd` (synced from XIIOnline `f9d9053b9`). Text only; nothing here was checked against
  the executable.
- **Citations** are `page:line`, with `page` given **below `FFXII TZA/08-Combat-Formula/`** unless it starts with `../`
  (then it is relative to that folder). A range `:a-b` covers lines a to b. "Not stated" means no page says it.

## Summary

| item | count |
|---|---:|
| pages read | **22** (1 category README, 1 namespace README, 14 mechanism pages, 6 contracts) |
| pass-1 gaps (CLOSED / NARROWED / OPEN / WRONG-IN-PASS-1) | n/a: pass 1 did not map this system |
| register rows owned by these pages, still open | **0** (§2.1) |
| new gaps, total | **17** (§2.2) |
| new gaps, STATIC | **7** (G-3, G-5, G-6, G-8, G-9, G-10, G-11) |
| new gaps, DOC | **7** (G-1, G-2, G-7, G-13, G-14, G-15, G-16) |
| new gaps, DATA | **2** (G-4, G-12) |
| new gaps, RUNTIME | **1** (G-17) |
| rating | **MOSTLY** (new; no pass-1 rating) |

The gaps that matter most: **G-1**, the merged-bitmap status / augment contradiction between this folder and
10-Status; **G-3**, the slot 96 conditions on every weapon hit; and **G-5** / **G-6**, the slot formulas and the 109
recipe lists still to extract.

## 1. Interface

### 1.1 Pages read, with the status each states

| page | status, as the page states it |
|---|---|
| `README.md` | category index, no front matter; per-page statuses at `README.md:13-74` |
| `Step-Table/combat-formula-step-table.md` | `status: AUDITED` (`:4`) |
| `CONTRACT-formula-step-table.md` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`:5-6`) |
| `Recipe-System/ranged-weapon-recipes.md` | `status: DOCUMENTED — owner read done …` (`:4`) |
| `Recipe-System/the-count-clock-and-bank-recipes.md` | `status: AUDITED` (`:4`) |
| `CONTRACT-weapon-recipes.md` | `CONTRACT READY`, `PROVEN` (`:5-6`) |
| `Scratch-Block/the-formula-scratch-block.md` | `status: AUDITED` (`:4`) |
| `Evaluation-Context/the-evaluation-context-field-map.md` | `status: AUDITED` (`:4`) |
| `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md` | `status: AUDITED` (`:4`) |
| `CONTRACT-preparation-step-family.md` | `readiness: BEHAVIORALLY UNDERSTOOD` (`:5`) |
| `Current-HP/the-hp-write-and-the-lethal-transition.md` | `status: AUDITED` (`:4`) |
| `CONTRACT-hp-write-and-lethal-transition.md` | `BEHAVIORALLY UNDERSTOOD`, `PROVEN` (`:5-6`) |
| `Battle-Stats-Record/the-battle-stats-record-field-map.md` | `status: AUDITED` (`:4`) |
| `the-auto-status-rebuild.md` | `status: AUDITED` (`:4`) |
| `where-a-stat-number-comes-from.md` | `status: DOCUMENTED — … No open residue is left` (`:4`) |
| `CONTRACT-stat-derivation.md` | `CONTRACT READY`, `PROVEN` (`:5-6`) |
| `Steal/the-steal-roll.md` | `status: AUDITED` (`:4`) |
| `Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md` | `status: AUDITED` (`:4`) |
| `CONTRACT-environmental-element-scaling.md` | `CONTRACT READY`, `PROVEN` (`:5-6`) |
| `elemental-affinity-and-the-five-bytes.md` | `status: AUDITED` (`:4`) |
| `combos-and-the-guard-parry-flag.md` | `status: DOCUMENTED — its one registered residue, GR-8, is ANSWERED` (`:6`) |
| `Status-And-Augment-Namespaces/README.md` | no front matter (`README.md:68` says so) |

### 1.2 Entry points, with their callers

| entry | what it is | callers | cite |
|---|---|---|---|
| `BattleFormula_ResolveTargetResult` `00385F60` (2,302 B) | the committed resolver: recipe id → second list → step loop → post-modifiers → copy-out into the result record | `Battle_ProcessActionTarget` `00307300` (`00307419`, `00307577`), `BattleFormula_QueryResolvedScalarPreview` (`00308BE3`), `BattleAction_ResolveSpecialSequenceTargets` (`0030ECA4`), `BattleUnit_RunPeriodicCombatMaintenance` (`0031108C`, `0031124D`), `BattleUnit_HandleActorTimelineEvent` (`0031A0CD`); every caller discards the return | `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:462-472`; `CONTRACT-weapon-recipes.md:296-300` |
| `BattleFormula_EvaluateTargetPreview` `00385680` | runs a recipe's **first** list when the action executes and memoises the outcome in the source's 64-byte record | `BattleAction_EvaluateTargetPreviews` `00303830` (`00303910`) and `00303A00` (`00303AD7`); `00303830` is called by `BattleUnit_AdvanceStandardActionState` (`00304F1D`, execution stage 9) and `00313120` (`003132A6`) | `CONTRACT-weapon-recipes.md:223-227`; `Recipe-System/ranged-weapon-recipes.md:58-67`; `Step-Table/combat-formula-step-table.md:668-678` |
| the step table `01EFA5C0` (202 × 8 B, `.data`) | the calculator catalogue; each slot is called `(sourceStats rcx, targetStats rdx, &ctx r8)` | the two indexed dispatchers `003859FF` and `003863D0`; three flat `call [01EFA5C0]` to slot 0 (`00388282`, `00388A63`, `00388ADD`); direct fixed-slot calls from six functions (slots 0, 20, 24, 31, 32, 37, 40, 46, 118, 180, 181) | `CONTRACT-formula-step-table.md:45-48`; `Step-Table/combat-formula-step-table.md:438`, `:623-646`, `:860-870`; `CONTRACT-preparation-step-family.md:514-528` |
| `BattleFormula_ApplyTargetStatusActionPostModifiers` `00390F20` | runs once after the committed list, outside the stop-flag test | `00385F60` at `003863F8` | `Step-Table/combat-formula-step-table.md:532-560`, `:697`, `:709-711` |
| `BattleFormula_BuildEvaluationContext` `003847C0` (273 B) | builds the `0x30`-byte context every slot receives | `00385F60` at `003860D5` | `Evaluation-Context/the-evaluation-context-field-map.md:43-54`, `:118` |
| `BattleFormula_ResetScratchState` `003849B0` (340 B) | resets the 44 scratch words | `00385680` (`0038585E`) and `00385F60` (`00386001`) | `Scratch-Block/the-formula-scratch-block.md:44-48`; `CONTRACT-preparation-step-family.md:139-142` |
| `BattleStats_ModifyHPAndProcessLethalState` `00300530` (880 B) and the absolute thunk `BattleStats_SetCurrentHP` `00300520` (8 B) | every HP change and every death | the applier `003112F0` (`call rax` at `00311668`), the deferred-HP committers `003065D0` (`00306699`) and `0030EB10` (`0030EB5F`), the reconcile clamp `0030F340` (`0030F3DC`, flags `0x217`); `00300520` from `002352E0`, `0023A410`, `00319F50`, `00329BD0` (the `sethp` verb family) | `Current-HP/the-hp-write-and-the-lethal-transition.md:95-101`, `:230-246`, `:306-346`; `CONTRACT-hp-write-and-lethal-transition.md:39-49` |
| `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (1,787 B) | rebuilds the derived layer, re-installs foe immunities, reconciles affinity, runs the stat rebuild and three clamps | 25 call sites in 14 functions (equipment and licence setters, level-up, status writes, spawn activation, direct-state orders) | `the-auto-status-rebuild.md:137-170` |
| `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (2,859 B) | effective stats from base + equipment + status-bonus lists, one clamped writeback | `0030FED0` (`003103AD`) and the loadout preview `0030A4E0` (`0030A6B7`) | `where-a-stat-number-comes-from.md:444-463`; `CONTRACT-stat-derivation.md:45-51` |
| the steal roll `00390390` (slot 195) | three-roll / one-roll steal | recipe 49 only, used only by action `0xA9` | `Steal/the-steal-roll.md:48-66` |

### 1.3 Inputs and outputs, with layouts

**Authored tables read.**

| table | layout as stated | cite |
|---|---|---|
| recipe pointer table `0x01EF96C0` | 109 pointers (ids 0..108); each blob = `i32` slot ids `[first list] -1 [second list] -1`; the next qword `000000B4FFFFFFFF` ends the table | `CONTRACT-weapon-recipes.md:58-74`, `:76-79` |
| recipe id selection | action row `+0x08`; id **0** means "use the equipped weapon row's `+0x19`"; returns −1 / −2 on a bad id or weapon word, and no formula runs | `CONTRACT-weapon-recipes.md:42-56`; `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:462-472` |
| the step table `0x01EFA5C0` | 202 slots, 152 distinct targets, 42 slots on the shared `ret 0` `0016D6A0`, seven targets with several ids | `CONTRACT-formula-step-table.md:65-92` (ST-1 to ST-3) |
| action definition row (`02EBF138`, 543 × 60 B) | `+0x08` recipe; `+0x0C` flags (bits 13 / 14 magick / physical, read by `00390F20`); `+0x10` power; `+0x11` second power byte; `+0x12` hit threshold; `+0x13` element mask (`0x01` Fire … `0x20` Wind); `+0x14` on-hit status chance; `+0x2C` word (bits 10 / 11 wake / clear Invisible) | `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:255-258`; `Step-Table/combat-formula-step-table.md:179`, `:540-560`; `CONTRACT-environmental-element-scaling.md:54-56`; `Recipe-System/ranged-weapon-recipes.md:129-133` |
| equipment row (`02EBF0F8`, 557 × 52 B) | `+0x11` category; `+0x19` recipe; `+0x1A` attack / status grant; `+0x1B` knockback base; `+0x1C` combo / critical rate; `+0x1D` weapon evade; `+0x1E` element; `+0x1F` on-hit chance; `+0x18` / `+0x19` shield evade / magick evade or defence / magick resist by kind | `Step-Table/combat-formula-step-table.md:440-470`; `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:380-398`, `:698-711`; `where-a-stat-number-comes-from.md:177-181` |
| party row (`02EBF130`) and the `.ard` growth / base tables (`02EBF140` / `02EBF148`, class-4 `02EBF150`) | party: HP / MP scale bytes `+0x18` / `+0x19` / `+0x1D`, four float bases, status masks `+0x48` / `+0x4C`; foe: `growth[col] × (level − growthBaseLevel) + base[col] + record modifier`, with the full column map | `where-a-stat-number-comes-from.md:75-99`, `:288-320`, `:391-418` |
| three stat-bonus id lists `00D10290` / `00D102A0` / `00D102B0` | 16 / 16 / 12 effect-layer ids → Strength / Magick Power / max HP, bonus = augment row `+4` (`02EBF040`) | `where-a-stat-number-comes-from.md:247-252` |

**Records read and written.**

| record | layout as stated | cite |
|---|---|---|
| battle stats record (`0x1C8`, unit `+0x698` or party array `*(02EBF190) + 8 + k × 0x1C8`) | every offset, writers and readers; `+0x10`–`+0x1F` is a union by kind byte `+0x05` (party f32[4], foe i16[8]); effective block `+0x24`–`+0x36`; status words `+0x38` / `+0x3C` / `+0x64`; layers `+0x68` / `+0x78`; affinity `+0x40`–`+0x44`; HP `+0x48`; MP `+0x4C`; charges `+0x4E`; equipment `+0x50`; level `+0x1C2` | `Battle-Stats-Record/the-battle-stats-record-field-map.md:90-179`, `:181-216`, `:428-437` |
| evaluation context (`0x30` B on the resolver stack at `rsp+0x48`) | `+0x00` action id; `+0x04` / `+0x08` source / target status words `+0x64 \| +0x3C`; `+0x10` result pointer; `+0x18` target unit `+0x55` (enemy class, `0xD` Undead) or −1; `+0x1A`–`+0x29` the source's two layers merged; `+0x2A`–`+0x2F` padding | `Evaluation-Context/the-evaluation-context-field-map.md:63-79`, `:123-135`, `:168` |
| formula scratch block `02AEDFB8`–`02AEE05F` (44 words) | every word with reset value, writers, readers; numbers use −1 as "absent"; the copy-out rules | `Scratch-Block/the-formula-scratch-block.md:57-105`, `:219-249` |
| per-unit 64-byte record `0208D480 + kind × 0x40` / `0208DE80 + unit[0xEA9] × 0x40` | 32 bytes of data: `+0x00` u32 stash, `+0x04` / `+0x08` per-target failed / immune bits, `+0x0C` marked targets, `+0x10` cached `0x9F` draw, `+0x12` preview flags and combo count, `+0x14`, `+0x18`, `+0x1C`; `+0x20`..`+0x3F` unused | `Scratch-Block/the-formula-scratch-block.md:158-181` |
| result record (07's) — fields this system writes | kind `+4` (6 failed, `0xA` immune, 7 voided, `0xB` special guard); flag word B `+0x18` bits 0–3; flag word A `+0x2C`; HP / MP `+0x20` / `+0x24` / `+0x28` / `+0x2A`; charges `+0x1D`; steal `+0x32`–`+0x34`; remove mask `+0x58`; levels `+0x11C` / `+0x11D`; stat deltas `+0x11E`–`+0x124`; counters `+0x138` / `+0x13C`; flag C `+0x140` | `Scratch-Block/the-formula-scratch-block.md:96-97`, `:138-147`, `:219-249`; `Steal/the-steal-roll.md:105-111`; `Step-Table/combat-formula-step-table.md:545-554` |

**The core formulas, as stated.** Damage `raw = (ATK + variance) − DEF; damage = raw ≤ 0 ? 0 : trunc(raw × multiplier)`
(`Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:530-545`); the sixteen preparation members and their
six multiplier forms (`CONTRACT-preparation-step-family.md:159-187`); the variance draw and its only guard
(`CONTRACT-preparation-step-family.md:160-166`, `:232-237`); the weapon modifier chain 96–99, 165, 171, 176, 182
(`Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:683-720`); the outcome roller's bands
(`Scratch-Block/the-formula-scratch-block.md:109-136`) and the ranged ladder (`Recipe-System/ranged-weapon-recipes.md:253-273`);
knockback, counter, combo and ranged-critical odds (`Step-Table/combat-formula-step-table.md:473-530`); the combo count
(`combos-and-the-guard-parry-flag.md:55-84`); element affinity (`elemental-affinity-and-the-five-bytes.md:40-61`) and the
weather / terrain rule table (`CONTRACT-environmental-element-scaling.md:114-136`); the HP clamp and the lethal / revive
predicates (`Current-HP/the-hp-write-and-the-lethal-transition.md:262-295`); the stat caps
(`CONTRACT-stat-derivation.md:75-111`); the steal thresholds (`Steal/the-steal-roll.md:158-169`); the count, walk and bank
recipes (`Recipe-System/the-count-clock-and-bank-recipes.md:128-137`).

### 1.4 State, with lifetime

| state | lifetime as stated | cite |
|---|---|---|
| scratch block `02AEDFB8`–`02AEE05F` | reset at the start of every preview and every resolution; global, so one resolution at a time; `02AEDFD4` (action id) is the one word the reset leaves | `Scratch-Block/the-formula-scratch-block.md:44-48`; `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:138-139` |
| per-unit 64-byte record | written by the preview, read back by the resolution of the same action; `+0x00`..`+0x1F` cleared at activation by `00386C10`; `+0x12` bit 0 cleared by the resolver | `Scratch-Block/the-formula-scratch-block.md:170-183` |
| `02EBF188` | the last resolved target unit pointer, written by the context builder, the weather stage and the steal roll | `Evaluation-Context/the-evaluation-context-field-map.md:224-239`; `CONTRACT-environmental-element-scaling.md:121-122`; `Steal/the-steal-roll.md:72` |
| battle-state block `+0x5AC8` / `+0x5ACC` (walked distance) and echoes `+0x5B00` / `+0x5B0C` / `+0x5B0E` | persistent; saved and loaded with the save image; the accumulator is fed every presentation frame | `Recipe-System/the-count-clock-and-bank-recipes.md:89-114`, `:160-171` |
| the gameplay MT19937 (`00379CD0` → `00863BF0`) | one lazily seeded static generator shared by every roll, in recipe order, and by other systems | `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:448-461`; `Step-Table/combat-formula-step-table.md:579` |
| `02099DA8` / `02099DAC` (environment / MWeather class) | published by the weather apply, read only here; environment domain 0..4, class 4 the common no-effect value | `Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md:54-58`, `:292-307` |
| unit HP floor `unit + 0x48` | zeroed by every definition apply; set only by the script verb `btlAtelSetHpLowLimit` | `CONTRACT-hp-write-and-lethal-transition.md:495-504`; `Current-HP/the-hp-write-and-the-lethal-transition.md:141-152` |
| foe masks `unit + 0xE80` (innate layer source) / `+0xE90` (immunities) | written by script verbs `btlAtelSetAbility` / `btlAtelSetStatus`; zeroed by unit reset | `the-auto-status-rebuild.md:172-199` |
| effective stats `+0x24`–`+0x36` | zeroed and rebuilt on every recompute | `where-a-stat-number-comes-from.md:43-45`; `Battle-Stats-Record/the-battle-stats-record-field-map.md:260-263` |
| steal override `[001D50D0() + 0xE5C]` | −1 from the constructor; no retail code path changes it | `Steal/the-steal-roll.md:217-218` |
| the step table itself | in `.data`, writable; nothing in the game writes it | `CONTRACT-formula-step-table.md:153-158` |

### 1.5 Order: what runs when, and what triggers it

1. **Action executes** (stage 9 of `BattleUnit_AdvanceStandardActionState`): the target-preview walk runs each target's
   **first list** through `00385680` — reset, slot loop with the stop flag, then the outcome (failed / immune bits, flag
   word B bits 1–3, combo count) is parked in the **source's** 64-byte record (`Recipe-System/ranged-weapon-recipes.md:180-190`;
   `Scratch-Block/the-formula-scratch-block.md:163-183`).
2. **Per target**, `Battle_ProcessActionTarget` calls `00385F60` (`00307419`): recipe id → reset (`00386001`) → context
   (`003860D5`) → preview bits copied in (`003860DF`–`00386108`) → the skip test (`00386249`–`003862AE`) → the **second
   list**, stopping after the first step that sets `02AEDFB8` → `00390F20` → the copy-out (`0038641D`–`00386813`)
   (`CONTRACT-weapon-recipes.md:86-97`; `Step-Table/combat-formula-step-table.md:680-713`;
   `Scratch-Block/the-formula-scratch-block.md:219-249`).
3. Inside a weapon list: preparation → 96, 97, 98, 99 → finaliser 125 → 165 (166 on 64), 171, 176, 182
   (`Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:683-696`). Order is the semantics (ST-4,
   `CONTRACT-formula-step-table.md:95-107`).
4. **Apply**: `BattleFormula_ApplyTargetResult` (`00307436`) turns the result into HP writes through `00300530` with flags
   built from `+0x2C` (`Current-HP/the-hp-write-and-the-lethal-transition.md:95-101`).
5. **HP write**: gate 1 and the downed refusal → clamp → publish reaction and number → event-variant bit → gate 3 →
   store → heal / lethal branch (`CONTRACT-hp-write-and-lethal-transition.md:189-203`, `:221-274`).
6. **Status change** → `0030FED0` → `002FEF30` → clamps → charge count (`the-auto-status-rebuild.md:142-158`); on the
   party side a Confuse / Berserk change can cancel the action in flight (`where-a-stat-number-comes-from.md:201-226`).
7. **Every presentation frame**: the walk recipe's distance feeder (`Recipe-System/the-count-clock-and-bank-recipes.md:91-96`).
   **Periodic tick**: `00310DB0` resolves results through the same `00385F60` (`CONTRACT-weapon-recipes.md:300`).

### 1.6 Dependencies on other systems

| system | what this system takes from it | cite |
|---|---|---|
| 07-Combat-Action | the action row, the result record, the applier, the target buffer (entry bits 8–11), the commit callers | `Scratch-Block/the-formula-scratch-block.md:149-156`; `Current-HP/the-hp-write-and-the-lethal-transition.md:95-101` |
| 10-Status-Periodic-Terminal | the two effect layers and their writer `0030E130`, the status write `0030E360` (KO set / clear, immunities) | `the-auto-status-rebuild.md:56-75`, `:152`; `Current-HP/the-hp-write-and-the-lethal-transition.md:193-222` |
| 21-RNG-And-Determinism | the gameplay MT19937 | `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:448-461` |
| 03-World-Area-Field | environment / MWeather classes, the terrain resolver `00263DD0`, field bit 15 `00377C20` | `CONTRACT-environmental-element-scaling.md:80-87`; `CONTRACT-hp-write-and-lethal-transition.md:541-543` |
| 04-Actor-Entity | `BattleStats_FindOwningBattleUnit` `0031B860`, the unit classifier `002F8E90`, unit fields `+0x48` / `+0x55` / `+0x6A0` / `+0xE60` / `+0xE80` / `+0xE90` | `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:767-779`; `Steal/the-steal-roll.md:72-74` |
| 05-Spawn-Encounter-Lifecycle | spawn record `+0x14` steal bits, `+0x08` / `+0x0C` death statistics, group completion `00306F00` | `Steal/the-steal-roll.md:74`; `CONTRACT-hp-write-and-lethal-transition.md:257-288` |
| 12-Items-Equipment-Shops-License | the equipment table, slot setters, licence board bitmap | `the-auto-status-rebuild.md:145-148` |
| 02-Resource-And-Asset-Pipeline | the registry resolver `0020E600`, the `.ard` tables, `battle_pack.bin`, the text banks | `Step-Table/combat-formula-step-table.md:438-446` |
| 01-Script-VM-Native-Bridge | `btlAtelSetAbility` / `btlAtelSetStatus`, `btlAtelSetHpLowLimit`, the `sethp` verbs | `the-auto-status-rebuild.md:179-182`; `Current-HP/the-hp-write-and-the-lethal-transition.md:334-346` |
| 11-Party / 19-Save-Load-Settings | the battle-state block and its save round trip | `Recipe-System/the-count-clock-and-bank-recipes.md:160-171` |

## 2. Gaps

### 2.1 The questions the pages themselves registered: all closed

Every register row these pages carry is closed in `../_index/OPEN-QUESTIONS.md`. No page in the folder has an open
checkbox left. Rows checked, each with its status cell:
- **ANSWERED:** `E-2`, `E-3`, `E-4`, `AK-1` to `AK-4`, `AK-6`, `AK-7`, `AJ-1`, `AJ-2`, `AJ-5` to `AJ-12`, `FT-1` to
  `FT-4`, `FQ-1`, `FQ-2`, `FU-1`, `FU-2`, `FK-1` to `FK-4`, `FE-1` to `FE-7`, `EY-1` to `EY-6`, `FC-1` to `FC-4`,
  `CB-5`, `CB-9`, `CB-12`, `CB-13`, `GR-8`, `FZ-17`, `UQ-123`.
- **CLOSED:** `E-1`, `AJ-3` and `AJ-4` as intent residues; `AK-5` as undecidable from the image.
- **SUPERSEDED:** `UQ-119` and `UQ-120`, duplicates of `FE-4` and `FT-2`.

What follows in §2.2 are gaps a re-implementer would still hit. They were found by reading the pages against each other
and against the criteria of the pass-1 brief. None of them has a register row; where a closed row touches one, the row
is named.

### 2.2 Gaps a re-implementer would still hit

| id | gap | class | evidence (`page:line`) | register row |
|---|---|---|---|---|
| G-1 | **The formula pages and the status pages disagree on whether the 32 battle statuses reach the merged bitmap.** The context builder ORs only the two effect layers `+0x68` / `+0x78` into `+0x1A`. The status side says the 32 statuses live in the status words `+0x64` / `+0x3C`, which go to context `+4` / `+8`, so "a merged-id test does not see Silence, Disease or Lure". Many formula pages still read the merged ids as statuses: Lure steals like the Thief's Cuffs (corrected that way on 2026-10-02, the same day the status side was corrected the other way); Petrify and Disease fire the weather bypasses; Silence opens slot 72's unarmed formula; the eval-context id table names Poison, Silence, Sap, Oil, Immobilize, Slow and Protect as the statuses; `WE-5` says a diseased combatant gets the weatherproof early-out; `D-5` says Disease reaches stat numbers; slot 0 and slot 129 read layer id 1 as Stone. A re-implementer cannot tell from this folder whether inflicting Lure, Disease, Silence, Petrify or Stone changes a formula. The builder's bytes (`+0x68` / `+0x78` only) favour the status pages, so the formula pages' status readings are what needs changing. | DOC | `Status-And-Augment-Namespaces/README.md:18-22`, `:36-44`; `Evaluation-Context/the-evaluation-context-field-map.md:51`, `:86-97`, `:149-150`, `:155-159`; `Steal/the-steal-roll.md:204-212`, `:322-325`; `Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md:77-79`; `CONTRACT-environmental-element-scaling.md:104-107`, `:176-177`; `CONTRACT-stat-derivation.md:113-119`, `:188-190`; `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:282-285`; `Step-Table/combat-formula-step-table.md:174`; `Scratch-Block/the-formula-scratch-block.md:395`; against `../10-Status-Periodic-Terminal/the-thirty-two-statuses.md:142` and `../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md:102` | `E-1` (CLOSED; its cell still says Disease "fires the Weatherproof bypass at the caster test"), `FK-1` and `FQ-1` (ANSWERED, with status names) |
| G-2 | **The preparation contract names the third slot argument wrongly.** It calls `r8` "the caller's stack result record" and reads slot 72's test as "bit 1 of the result record's `+0x1B`". Three other pages say `r8` is the evaluation context (`rsp+0x48`) and that `+0x1B` bit 1 is merged id 9. A port that follows the contract's §12 signature passes the wrong object to slot 72. | DOC | `CONTRACT-preparation-step-family.md:51`, `:196-197`, `:255`; against `Evaluation-Context/the-evaluation-context-field-map.md:118`, `Step-Table/combat-formula-step-table.md:176`, `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:247-250`, `:282-285` | — |
| G-3 | **Slot 96 (`0038B950`) runs on every weapon recipe, and its conditions are not stated.** The modifier chain is "96, 97, 98, 99", and AJ-8 calls 96 / 97 "the paired constant scalers of §12". §12 reads only 97. For 96 it gives three constants with bare compares (`× 1.3` after `cmp ecx, 0x15`, `× 0.75` after `cmp eax, 0x12`, `× 3` after `test bl, 1`). It does not say which fields those compares read, and it does not attribute the profiled constants `10` and `1.5` at all. The step table calls it "eight field reads, repeated `02AEE054` rewrites". The damage multiplier of every weapon hit therefore has one unstated stage. | STATIC | `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:650-653`, `:693-695`, `:823-827`; `Step-Table/combat-formula-step-table.md:270` | `AJ-8`, `AJ-10` (ANSWERED; neither reads 96's gates) |
| G-4 | **Augment ids that formula code tests have no names on any page cited here.** Slot 165 multiplies the finished damage by 1.2 on context `+0x20` bit 1 and doubles it on bit 2 (merged ids 49 and 50). On the doubling path it also writes `02AEE014` (source HP loss) = the damage. The ids are unnamed (the context table lists 48–55 with no names), so what the two bits are, and why the doubling also costs the source HP, is not stated. Likewise the 44 ids in the three stat-bonus lists are deferred to "the thirty-two statuses and augment pages", which by G-1 cannot name them as statuses. | DATA | `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:628-644`; `Evaluation-Context/the-evaluation-context-field-map.md:75`, `:104`; `where-a-stat-number-comes-from.md:247-252`, `:503-506` | — |
| G-5 | **Some recipe-reached step bodies have a role but no formula.** `AK-3` closed on "every slot a shipped recipe names is read **or named**". Several are named only by a signature: slot 17 (a prime / divisibility gate on the source level against "the row-derived product", which is not defined); 23 / 24 (hit chance from row `+0x12` "under the row-resolved guard"); 102 ("row-driven multiplier / fail step, four field reads"); 104 ("rolled target HP loss, two RNG calls + four field reads"); 120 ("three write paths"); 166. The second writer of the knockback chance, `00388B50`, is "not read here". Slot 2 (`RollSpecialGuardOutcome`) builds band A as a running total across seven writes, and the addends are not stated. Several bodies appear only as writers in the scratch census, with no slot id and no formula: `0038CB00`, `0038DB50`, `00388E80`, `003891F0`, `0038AF20`, `0038AF50`, `0038AF90`, `0038D400`, `0038D630`, `0038F800`, `00389BE0`. | STATIC | `Step-Table/combat-formula-step-table.md:225-233`, `:253-254`, `:273-274`, `:280`, `:300`, `:487`; `Scratch-Block/the-formula-scratch-block.md:66-91`, `:102`, `:135-136`, `:487-491` | `AK-3` (ANSWERED at the "named" bar) |
| G-6 | **The 109 recipes' slot lists are not published.** The weapon-recipe contract says so outright: "What the other 107 recipes name. Two are decoded; the rest are authored data this contract does not enumerate." The pages quote about forty lists between them. `recipe-users.tsv` gives each recipe's users, not its slots. Each list is the program for its actions (ST-4), so a re-implementer must extract all 109 from the image. | STATIC | `CONTRACT-weapon-recipes.md:230-231`; `Recipe-System/recipe-users.tsv:1` (columns `recipe, action_count, action_ids, action_names, weapon_rows`); `CONTRACT-formula-step-table.md:95-107` | `E-2` (ANSWERED for users only) |
| G-7 | **Step bodies and terms described only outside this folder, with no pointer from it.** The trap slots 106–109 and 163 are given on the persistent-flag page, as `(1 + roll % power) × (1 + roll % level)` into four output slots; the step table gives 106 / 108 only as "rolled … same shape". The Potion / Ether / Phoenix Lore slots 127 / 128 / 130 are on the battle-text-banks page; the step table does not list them. The equipment sub-record (`row +0x28`) that every item adds through is described on the equipment page; the stat page mentions it without a pointer. | DOC | `Step-Table/combat-formula-step-table.md:274-277`; `where-a-stat-number-comes-from.md:167-172`; against `../14-Story-Event-Quest-Hunt/persistent-flag-banks.md:774-783`, `../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md:276-281`, `../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md:263-265` | — |
| G-8 | **How many draws the one-roll steal takes.** The intro calls it "one first-hit roll". §2.2 writes the three tests on a single `r`. §4 writes `r0`, `r1`, `r2`, and the falsification pass finds the `% 100` idiom "six times (three per branch)". Whether the one-roll branch draws once, or up to three times and stops at the first hit (each hit jumps to `00390584`), is not stated. The difference moves the shared MT stream for every later roll. | STATIC | `Steal/the-steal-roll.md:31`, `:78`, `:163-168`, `:271` | — |
| G-9 | **Repeated ids and a second finalise.** "Whether ids may repeat, and what a second finalize does are … open (ST-5)". Ids 113 and 125 are one body, and nothing in the table stops a list from naming both. Neither page states whether any shipped list repeats an id, or what `0038D280` does when its loss / gain words are already set. | STATIC | `CONTRACT-formula-step-table.md:109-111`, `:214-215` | — |
| G-10 | **The terrain class: its domain and its failure value.** The terrain table lists classes 0–2 only. The contract says an unresolvable target "falls back through `00263DD0`'s own path; this contract does not read it". No page in the folder states what `00263DD0` returns when the field record cannot be resolved, or whether values above 2 occur. The environment class needed exactly this fix (class 4, `CON-146`). | STATIC | `Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md:60-62`, `:121-127`, `:292-307`; `CONTRACT-environmental-element-scaling.md:169-172` | — |
| G-11 | **What un-KOs a unit with a non-zero HP floor.** Such a unit dies at its floor, and the HP write's revive arm (which tests old HP against zero) can never fire for it. "Whether anything *else* in the game clears that KO is not read here and is not claimed." | STATIC | `CONTRACT-hp-write-and-lethal-transition.md:244-248`; `Current-HP/the-hp-write-and-the-lethal-transition.md:202-208` | — |
| G-12 | **Thirteen of the fourteen floor-setting scripts are unread to their event code.** One case is read (`lus_g01`, Ba'Gamnan ends at 796 HP); "the other thirteen scripts share the floor-plus-mode-1 shape but were not read to their event code". | DATA | `Current-HP/the-hp-write-and-the-lethal-transition.md:151` | `EY-2` (ANSWERED; the residue is in its cell) |
| G-13 | **Text left stale after corrections, read by a re-implementer as current.** (a) The scratch block's §4 struct still names `02AEDFC4` / `02AEDFDC` `parryRolled` / `parryChance`, `02AEDFF8`..`02AEE000` "resolver-private", and `02AEE044` / `48` "u8 (two bytes)"; §2.2 corrects all of these (counter flag and chance; charge loss / gain; the new levels). (b) The scratch §2.6 kind table still says "parry". (c) `FT-4`'s status cell and scratch §7 still call entry bit 11 "the mode-2 resource reaction" (it is the ranged critical). (d) The stats record's §4 struct gives `+0x88` as "u8 grower arg" and omits the party gambit block. (e) The preparation contract says slots 73 and 131 "are reachable by nothing at all" (refuted on the step table, §12b.2); and that "semantic names for the nine unnamed members" are open (named on the attack-defence page §5.1). (f) The environmental contract says the step table and the weapon recipes are "uncontracted". (g) The weapon-recipe contract §16a calls the preview caller "§14's open question" (answered in §14). (h) The category README still lists "Magick / Technick / item formula families" as not yet documented. | DOC | (a) `Scratch-Block/the-formula-scratch-block.md:275-286` against `:64`, `:70`, `:77-78`, `:96-97`; (b) `:204-210`; (c) `:413` and `../_index/OPEN-QUESTIONS.md` row `FT-4`; (d) `Battle-Stats-Record/the-battle-stats-record-field-map.md:435` against `:163`; (e) `CONTRACT-preparation-step-family.md:92-94` against `Step-Table/combat-formula-step-table.md:866`, `:916-918`; `CONTRACT-preparation-step-family.md:360-361` against `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:260-274`; (f) `CONTRACT-environmental-element-scaling.md:226`; (g) `CONTRACT-weapon-recipes.md:261-263` against `:223-227`; (h) `README.md:83` | `FT-4` (ANSWERED) |
| G-14 | **Slot 166 reads a byte the action-row page calls padding.** The attack-defence page says slot 166 (recipe 64 only) adds `value × row +0x15 / 100`, "keyed by the parked action row". The action-row page says `+0x15`–`+0x17` are 0 on all 543 rows and calls them padding. Either the row is a different table, or the step is a no-op on shipped data. Neither page says which. | DOC | `Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md:718-720`; `Step-Table/combat-formula-step-table.md:300`; against `../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md:72` | — |
| G-15 | **Action row `+0x13`: one bit per element, or a gate?** The action-row page says "bit 0 gates the weather / terrain scaling". This folder reads `+0x13` as the element mask, with bit 0 = Fire tested by the first rule of the stage, and the stage gated by layer id 16 instead. | DOC | `../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md:70`; against `CONTRACT-environmental-element-scaling.md:54-56`, `:124-131`, `Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md:64-75` | — |
| G-16 | **The affinity stage's nested `0x400` arm is left as "a status that reacts".** Elsewhere it is shown to be dead. The page names layer id 52 "a status that reacts specifically to being hit by an element the target is weak to", calls `00384B10` (a random pick from the element mask), and sets result `+0x140` bit `0x400`. It does not say what consumes that bit or the pick. The two-layer page has since read id 52 as the "NOT USED" augment, which nothing the tables ship grants. | DOC | `elemental-affinity-and-the-five-bytes.md:88-96`, `:136-141`; against `../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md:331-335` | — |
| G-17 | **No live observation of anything in the system.** Every contract carries isolated native replay at most. Explicit requests are open: break on `003863D0` and record the slots that actually occur; confirm that `0038AA90` faults with a null registry; and the two queued checks for the alias (a petrifying bow user in severe weather; a diseased caster against weather scaling). G-1 changes what the second pair should expect. | RUNTIME | `CONTRACT-formula-step-table.md:210`; `CONTRACT-weapon-recipes.md:207`; `CONTRACT-environmental-element-scaling.md:219-220`; `CONTRACT-preparation-step-family.md:330-338`; `CONTRACT-hp-write-and-lethal-transition.md:476-482`; `Status-And-Augment-Namespaces/README.md:44-46` | — |

## 3. Rating

**MOSTLY** (first rating; pass 1 did not map this system).

The machinery a re-implementation needs is stated to the instruction, and most of it has been executed in isolation:
- the recipe resolver, its two lists, the skip and stop rules, and the `-1` sentinel (`CONTRACT-weapon-recipes.md` RW-1 to RW-5);
- the 202-slot table and the order-is-the-semantics rule (ST-1 to ST-7);
- the 44 scratch words, with resets and the copy-out (`Scratch-Block/the-formula-scratch-block.md` §2.2, §2.7);
- the evaluation context, at `0x30` bytes;
- the sixteen preparation members, as six closed forms with bit-exact partial writes;
- the damage equation, the modifier chain and the outcome ladder;
- the HP write with its floor, cap, gates, event variants and lethal sequence;
- the stat rebuild with its caps and the second store;
- the auto-status rebuild;
- the stats record, offset by offset;
- steal, weather / terrain scaling, element affinity, combos, and the count / walk / bank recipes.

Every register row these pages raised is closed (§2.1).

The system is not READY for two reasons, and neither is structural:
- **The per-slot catalogue is not complete at the formula level.** Slot 96, which runs on every weapon hit, has unstated
  conditions (G-3). Some recipe-reached bodies are named but not given a formula (G-5). The 109 slot lists themselves
  are not published (G-6). Each of these is a bounded desk read of the image.
- **One cross-page contradiction changes outcomes.** G-1 decides whether inflicting Lure, Disease, Silence, Petrify or
  Stone changes the steal, the weather bypasses, slot 72, the stat bonuses and slots 0 / 129. The builder's bytes settle
  it, so the fix is to reconcile the pages.

The remaining gaps (G-2, G-7 to G-16) are single facts, pointers or stale sentences. G-17 is the usual live-observation
residue.
