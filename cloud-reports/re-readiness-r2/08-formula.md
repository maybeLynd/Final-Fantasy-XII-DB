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

*(Filled in when sections 1 to 3 were complete.)*

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
