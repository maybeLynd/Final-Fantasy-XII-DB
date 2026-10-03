# Reconstruction readiness, pass 2: `FFXII TZA/10-Status-Periodic-Terminal/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part B |
| Session | FABLE r2-11 |
| Date | 2026-10-03 |
| Snapshot | this repo's text snapshot only (`b23bdddd`, synced from XIIOnline `f9d9053b9`). No executable, Ghidra or live game was used. |
| Pass 1 | **none.** `cloud-reports/re-readiness/` has no `10-status.md`, so this is pass 1's full task (Interface, Gaps with a class column, Rating). |
| Status of this file | **draft / pointer.** Nothing here is evidence. Every item quotes or paraphrases a page and gives its location. |

## 0. Summary

*(Filled in when the Gaps and Rating sections are written; see the end of the file.)*

## Pages read, and how they are cited

Citation form: `ALIAS:line`. All paths are under `FFXII TZA/10-Status-Periodic-Terminal/`.

| alias | page | lines | status as the page states it |
|---|---|---:|---|
| `README` | `README.md` | 54 | category index; "Functions \| 24" (`README:8`) |
| `SWC` | `CONTRACT-status-write.md` | 702 | `readiness: CONTRACT READY`, `confidence: PROVEN` (`SWC:5`–`6`); one falsification pass, 2026-09-12 (`SWC:19`–`20`) |
| `ELC` | `CONTRACT-effect-layers.md` | 312 | `CONTRACT READY`, `PROVEN` (`ELC:5`–`6`); falsification pass 1, 2026-09-29 (`ELC:19`–`21`) |
| `PTC` | `CONTRACT-periodic-tick.md` | 421 | `CONTRACT READY`, `PROVEN` (`PTC:5`–`6`); falsification pass 1, 2026-09-30 (`PTC:19`–`21`) |
| `ASC` | `CONTRACT-auto-status-rebuild.md` | 2,653 | `readiness: BEHAVIORALLY UNDERSTOOD`, `PROVEN` (`ASC:5`–`6`); `implements:` a page in `12-Items-Equipment-Shops-License` (`ASC:7`) |
| `SWP` | `Status-Write/the-status-write-and-its-side-effects.md` | 915 | `status: AUDITED`, `readiness: BEHAVIORALLY UNDERSTOOD` (`SWP:4`, `SWP:7`) |
| `TSV` | `Status-Write/status-definition-record-accesses.tsv` | 22 | 21 data rows: the reads of `status_data` row bytes `+0x06`, `+0x08`, `+0x09`, `+0x20` by eight functions; used for layout checks only |
| `PTP` | `Periodic-Tick/what-the-periodic-tick-does.md` | 674 | `status: AUDITED` (`PTP:4`) |
| `TLP` | `Status-And-Augment-Layers/two-layer-effect-model.md` | 419 | `status: DOCUMENTED` (`TLP:4`) |
| `T32` | `the-thirty-two-statuses.md` | 505 | `status: AUDITED` (`T32:4`) |
| `MP` | `where-mp-comes-from.md` | 803 | `status: AUDITED` (`MP:4`) |

"Not stated" means no page in this folder says it. Where only a page in another category says it, the pointer is
given as a path from `FFXII TZA/`; those pages were not audited for this report. Register rows are from
`FFXII TZA/_index/OPEN-QUESTIONS.md` (`OQ:line`).

---

## 1. Interface

The category is four operations that call one another, plus the authored tables they read:

- **The status write** `0030E360`: the only setter and clearer of the 32 battle statuses, which are bits of the status
  words at stats record `+0x64` and `+0x3C` (and the third word `+0x38`). "**Nothing else in the game sets or clears a
  status bit.**" (`SWC:42`–`43`).
- **The two effect layers**: two 128-bit bitmaps per stats record, `+0x68` (mutable) and `+0x78` (derived), written only
  by the mutate body `0030E130`, rebuilt by `0030FED0`, and merged for formulas by `003847C0` (`ELC:41`–`51`).
- **The auto-status rebuild** `0030FED0`: recomputes the derived layer from definition row, equipment and licences, and
  applies only the difference (`ASC:27`–`30`).
- **The periodic tick** `00310DB0`: once per unit, it builds a result record in five stages and hands it to the
  ordinary applier `003112F0` (`PTC:42`–`51`).

The 32 statuses are **not** in either effect layer: "The 32 battle statuses, Poison among them, live in the status
words `+0x64` / `+0x3C`. … An inflicted Poison never enters `+0x68`." (`TLP:119`–`122`).

### 1.1 Entry points (functions, with their callers)

#### The status write

| entry | callers | what it does | cite |
|---|---|---|---|
| `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, 1,323 B | "**14 sites in 10 functions**": `BattleStats_ModifyHPAndProcessLethalState` (KO add and remove), `BattleFormula_ApplyTargetResult`'s two mask loops, the wrappers `0030E990` / `0030EAE0`, `BattleStats_RemoveStatusesFromMaskAndRecompute`, `BattleStats_RecomputeDerivedStateAndAutoStatuses`, itself (the cascade); also `BattleUnit_AdvanceStandardActionState`, `BattleUnit_ExecuteDirectStateCommandOrder`, `BattleSpecialSequence_CommitAccumulatedTargetHp` | gates → Esper shortcut → mask write (six modes) → per-status arrays → presence test → own result record → applier → cascade → reaction → extra effect → terminal case → recompute | `SWC:49`–`54`, `SWC:155`–`158`, `SWP:415`–`419`, `SWC:257`–`259` |
| `0030E990` / `0030EAE0` | not stated | `RemoveStatusMode0` / `AddStatusMode3` wrappers, 35 / 38 B | `SWP:340` |
| `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`, 196 B | `0030C470` (level-set) | calls the write with the literal flags `0x217` per status, then recomputes once | `SWP:341`, `SWP:408`, `SWP:735` |
| `BattleStatus_ComputeDefaultDwordParameter` `00387730`, 645 B | `0030E360` (`0030E581`), `BattleFormula_AppendStatusAddOperation` `00387BB0`, `0038FCE0` | the default duration (formula in §1.6) | `SWP:114`, `SWP:146`–`158`, `SWC:698` |
| `BattleStatus_ComputeDefaultShortTimer` `003876D0`, 88 B | `0030E360` (`0030E5A2`), `00387BB0` | the default beat, `row.+9 × [01DFE0B4] × 30` | `SWP:118`, `SWP:128`–`132`, `SWC:453` |
| `00386A50` (add) / `00386A70` (remove) transition builders, 32 / 103 B | `0030E360` through `call rax` (`0030E5EA`–`0030E60E`) | add: clears result `+0x2C` bit 0, nothing else; remove: status 28 with `+0x48 != 0` → mask `0x109`, `+0x24 = (HP + 1) / 2` toward zero; else clears bit 0 | `SWC:54`, `SWC:467`–`477`, `SWP:233` |
| `003284D0` the status-applied reaction, 83 B | `0030E360` (`0030E6E7`–`0030E6FF`) | behind `002FA3B0` ("within 24 units of the party leader"), enqueues `{p_10, status, 2}` | `SWP:236` |
| `0046A800` the extra effect, 106 B | `0030E360` only, by `call rax` at `0030E727` | status 1 → event `0x12`, status 31 → `0x11`, into the poster `0046AB10`; modes 0, 1, 2, 5 call the `ret 0` stub `0016D6A0` instead | `SWC:54`, `SWP:237`, `SWP:578`–`597` |
| `00300FC0` defeat cleanup, 371 B | the three terminal adds, the Esper shortcut (flag 0), `BattleUnit_TeardownAndDespawn` (`00300E59`, flag 1) | Esper: cancel action + `003138D0(0)`; otherwise release, stop, enmity, the four `02089340` latches and party requests | `SWP:262`–`286`, `SWP:296`–`315`, `ASC:706`–`714` |
| `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280`, 857 B | the terminal adds of 0, 1, 31 | rewards; reads unit `+0xE9A` bits 0–3 | `SWP:248`, `SWP:474`–`478` |
| `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140`, 452 B | the terminal removes of 0, 1, 31 | bails if `(+0x64 \| +0x3C) & 0x80000003`; else full release, event `0x200D`, deadline `+0xDD0` | `SWP:248`, `ASC:724`–`730` |
| eligibility gates `0030B9B0` / `0030B8E0`, 116 / 109 B | `0030E360`, `00300530`, `003112F0`, `00301AD0` and others | one shape over the low / high halves of a packed mask | `PTP:452`–`467`, `ASC:672`–`681` |

#### The effect layers and the rebuild

| entry | callers | what it does | cite |
|---|---|---|---|
| `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130`, 553 B | `003112F0` (applier step 14), `002FDDA0`, `0030FED0` | sets or clears one bit in either layer by mode (0 clear `+0x68`, 1 clear `+0x78`, 2 set `+0x68`, 3 set `+0x78`); side effects only when presence in either layer changes | `ELC:49`, `ELC:96`–`102`, `ELC:248`, `TLP:221`–`254` |
| `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`, 1,787 B | "22 call sites in 12 functions": `BattleUnit_ExecuteDirectStateCommandOrder` ×12, `0030E360` (`0030E828`), `0030E130`, `RemoveAllMode0StatusesAndRecompute`, `RemoveStatusesFromMaskAndRecompute`, `SpawnUnit_FinalizeSpawnEntryActivation`, `BattleFormula_ApplyTargetResult`, `AdvanceLevelToTargetAndRecomputeGrowth`, two equipment setters, `0030C470` | accumulate → diff against `+0x78` → apply each changed bit through `0030E130` → `002FEF30` → kind-1 tail → clamps | `ASC:2527`–`2534`, `ASC:132`–`226` |
| `BattleFormula_BuildEvaluationContext` `003847C0`, 273 B | `BattleFormula_EvaluateTargetPreview` `00385680`, `BattleFormula_ResolveTargetResult` `00385F60` | merged bitmap at context `+0x1A` = caster `+0x68 \| +0x78`, ids 0–127, then id 15 revoked under two conditions | `ELC:51`, `ELC:104`–`138`, `ELC:298` |
| `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` | `0030FED0` once, at `003103AD` | zeroes and rebuilds `rec+0x24..0x47` (which includes status word `+0x3C` and `+0x38`) | `ASC:184`, `ASC:1607`–`1653`, `SWC:115`–`117` |
| `0030E060` (200 B, "the charge count") | `0030FED0`, `00300BC0` | `+0x4E = (+0x37 > 0) ? +0x06 / +0x28 : 0` | `MP:152`–`156` |

#### The periodic tick

| entry | callers | what it does | cite |
|---|---|---|---|
| `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0`, 1,338 B | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` | gates → deadline → Esper dismiss check → readiness probe and masks → build/apply 1 → trap applies → walk MP → pickup and Chain Bonus → enmity decay and `002FE950` | `PTC:63`, `PTC:364`, `PTP:516`–`555` |
| `BattleFormula_BuildPeriodicStatusResult` `00385DF0`, 83 B | `00310DB0` (`00310F8B`) | five calls in fixed order, the last a `jmp` | `PTC:64`–`76`, `PTC:406` |
| stage 1 `BattleFormula_InitializeResultRecord` `003848E0`, 205 B | `00385DF0`; also `00386A50`, `00386A70`, `00386AE0`, `00385680`, `00385F60` | memset `+0x08`–`+0x147`, `−1` sentinels, `+0x2C` bit 0 | `PTC:146`–`151`, `PTC:372` |
| stage 2 `BattleFormula_AdvanceStatusTimersAndBuildResult` `00386C70`, 935 B | `00385DF0` | the 32 statuses' durations and beats; Poison, Sap, Regen; Petrify/Doom count; HP Critical | `SWP:169`–`182`, `PTP:498`–`514` |
| stage 3 `BattleFormula_AdvanceStatusLinkedAuxTimers` `00385570`, 262 B | `00385DF0` | the eight effect-slot timers `+0x17C`, keyed by the effect table `02EBF040` | `PTP:109`–`145`, `PTP:276` |
| stage 4 `BattleFormula_ApplyGlobalPeriodicDrainModes` `00385CA0`, 336 B | `00385DF0` | field drains: MP `maxMP / −50`, HP `maxHP / −100`, gated by `022C314C` masks 2 and 1 | `PTC:275`–`284`, `PTC:417`–`421` |
| stage 5 `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860`, 485 B | `00385DF0` (tail `jmp`) | out-of-combat HP credit 1 / 2 / 5 % per second for a category-8 unit that perceives no foe; **overwrites** result `+0x24` | `PTP:436`–`450`, `PTC:168`–`169` |
| `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, 458 B | `00310DB0` only (`003110C3`) | walk-MP step, returns 0 or 1 | `MP:277`–`322`, `MP:695` |
| `BattleEnmity_UpdatePeriodicDecay` `00321530`, 142 B | `00310DB0` common tail (`003112A4`) | enmity decay (CombatAI layer) | `PTP:244`, `PTP:547` |

#### MP (the gain and spend side homed here)

| entry | callers | what it does | cite |
|---|---|---|---|
| `BattleStats_ModifyPrimaryResource` `00300CE0`, 351 B | `00307300` (`0x10`), `00305640`, `00310DB0` (`0x90`), `0030F5A0` (`0x217`), `003112F0`, `00329BD0` | MP `+0x4C` clamped to `+0x28` (0 under effect 39) | `MP:73`–`115`, `MP:566`–`570` |
| `BattleStats_ModifySecondaryResource` `00300BC0`, 207 B | `00300CE0` on a positive delta, `00300C90`, `003112F0` | the Mist Charge pool `+0x06`, cap `+0x28 × (+0x37 or 1)` | `MP:147`–`162`, `MP:552`–`561` |
| `002F91A0` / `002F9240` gain from being hit / dealing damage | `Battle_ProcessActionTarget` `00307300` only | effect ids 21; 86 + row `+0x2C` bit 3, 20 + bit 4; kill bonus id 23 | `MP:169`–`240`, `MP:691`–`693` |
| `002FB6C0` damage ladder lookup, 500 B | `002F91A0`, `002F9240` | slot `02EBF0B8` rows 1–19 | `MP:244`–`273` |
| `BattleAction_ComputePrimaryResourceCost` `00309110`, 165 B | `00303BD0`, `00305640` | row `+0x0A`, exemptions, effects 32 / 91–93 / 51 / 36 | `MP:371`–`401` |

### 1.2 Inputs and outputs (record layouts)

**`BattleStatsRecord`** (`0x1C8` B, `SWC:73`), the fields this category reads or writes:

| field | width | meaning | written by | cite |
|---|---|---|---|---|
| `+0x06` | s16 | Mist Charge pool | `00300BC0`; clamped by `0030FED0` against `+0x28 × +0x37` | `MP:147`–`151`, `ASC:217` |
| `+0x24` | i32 | max HP (in the `+0x24..+0x47` block `002FEF30` zeroes and rebuilds) | `002FEF30` | `ASC:1609`–`1643`, `PTC:196`–`199` |
| `+0x28` | s16 | max MP | `002FEF30` | `MP:82`–`87` |
| `+0x2C` | u8 | Vitality (default-duration input) | not stated here | `SWC:73`, `SWP:153` |
| `+0x37` | u8 | Mist Charge multiplier, `min(+0x20, 3)` for kind 0, else 0 | `002FEF30` | `MP:554`–`555` |
| `+0x38` | u32 | status word 3, the immunity word: mode 5 sets, mode 2 clears; mode 3 refuses a bit set here; **not** part of presence | `0030E360`; zeroed and rebuilt in `002FEF30`'s block; re-installed by `0030FED0`'s mode-5 pass | `SWC:113`–`114`, `SWC:444`, `ASC:198`–`204` |
| `+0x3C` | u32 | status word 2 (mode 1 clears, mode 4 sets); "a status in word 2 never runs out" | `0030E360`; **also rebuilt** by `002FEF30` (`d[rec+0x3C]` is "a rebuilt output") | `SWC:113`–`117`, `SWP:184`, `ASC:1645`–`1649` |
| `+0x48` | i32 | current HP | the HP write; `0030FED0`'s clamp at `00310508` | `ASC:213`–`221` |
| `+0x4C` | s16 | current MP | `00300CE0`; `0030FED0`'s clamp | `MP:73`–`80`, `ASC:216` |
| `+0x4E` | | charge count, `+0x06 / +0x28` | `0030E060` | `MP:152`–`156` |
| `+0x50` | u16[5] | equipment ids | not this category | `ASC:60` |
| `+0x64` | u32 | status word 1 (mode 0 clears, mode 3 sets); only these two modes write the per-status arrays | `0030E360` | `SWC:200`–`212`, `SWP:74` |
| `+0x68` | u8[16] | mutable effect layer (effect ids, not the 32 statuses) | `0030E130` modes 0 / 2 only | `ELC:57`–`58`, `ELC:96`–`97` |
| `+0x78` | u8[16] | derived effect layer | `0030E130` modes 1 / 3, driven only by `0030FED0`'s diff | `ELC:77`–`93`, `ASC:81`–`88` |
| `+0xBC[32]` | u32 | per-status remaining duration (Petrify / Doom: a count) | `0030E360` modes 0 / 3; committed from result `+0x5C[s]` by the applier's step 9 | `SWC:145`–`151`, `SWP:136`–`144` |
| `+0x13C[32]` | u16 | per-status beat | the same, from result `+0xDC[s]` | `SWP:136`–`144` |
| `+0x17C[8]` | s16 | effect-slot timers | the applier, from result `+0x42`–`+0x50` | `PTP:137`–`139`, `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md:166` |
| `+0x194` | u8[46] | owned licence nodes, ids 0–360 | not this category | `ASC:61` |
| `+0x1C2` | u8 | level (Regen's divisor) | not stated here | `SWP:179`, `PTC:314` |

**`BattleResultRecord`** (`0x148` B, on the caller's stack, `SWC:74`, `PTC:80`–`91`):

| field | meaning | cite |
|---|---|---|
| `+0x24` | HP value / delta accumulator | `PTC:86`, `PTP:309` |
| `+0x2A` | MP delta (stage 4) | `PTC:87` |
| `+0x2C` | flag word A (bit 0 = apply, bit 8 = HP write, bit 3 = absolute) | `PTC:88`, `SWP:233`, `SWP:182` |
| `+0x3E` | expired effect ids (no bound) | `PTC:89`, `PTC:157`–`159` |
| `+0x42 + 2·slot` | new effect-slot timer values | `PTC:90` |
| `+0x54` / `+0x58` | status add / remove masks | `SWP:181`, `SWP:416` |
| `+0x5C[32]` / `+0xDC[32]` | next duration / next beat | `PTC:98`, `SWP:142`–`144` |
| `+0x140` | flag word C | `PTC:91` |

**`FormulaEvaluationContext`** (`ELC:61`–`66`): `+0x04` / `+0x08` the target's status words `+0x64` / `+0x3C`;
`+0x18` the target unit's `+0x55` (`0xFFFF` with no unit, `0` with a null target); `+0x1A` the merged effect bitmap.

**`BattleUnit`** (`0xF50`, `SWC:76`): kind / type bytes for the Esper test; `+0xE9A` bits 0 (Poison) and 1 (Petrify)
"applied by a party-side source" (`SWP:391`); `+0xDD0` deadline and flag bit `0x40000000` (`PTP:297`–`306`);
`+0xE80` the kind-1 auto-status source and `+0xE90` the scripted immunities (`ASC:134`–`137`, `ASC:198`–`204`).

**Authored tables**

| table | slot | layout used here | cite |
|---|---|---|---|
| `status_data.bin` | `02EBF118` | 32 × `0x28`; `+0x00` name word; `+0x06` flag word (bit 5 = refreshable, bit 13 = harmful); `+0x08` duration base (`0xFF` none); `+0x09` beat; `+0x0A` text id; `+0x0C` clear mask; `+0x10`/`+0x13`/`+0x26`/`+0x27`/`+0x02` order keys; `+0x20` block mask; `+0x24` flag byte; `+0x11`, `+0x12`, `+0x14`–`+0x1D` read by no code | `SWC:75`–`97`, `SWC:241`–`246`, `T32:158`–`163`, `T32:257`, `T32:318`–`339` |
| effect table (augments) | `02EBF040` | 129 × 8: `{u16 nameId, u16 0x5000 + row, u16 parameter, u16}`, byte `+6` = stage-3 timer slot (`03`/`04`/`05` on rows 55/56/57) | `MP:424`–`427`, `PTP:276` |
| MP ladder | `02EBF0B8` | rows 1–19 `{u16 threshold, u8, u8}`, rows 20–24 `{s32 interval, s32 mpThreshold}`; shipped values tabulated | `MP:459`–`461`, `MP:494`–`543` |
| equipment / licence tables | `02EBF0F8` / `02EBF038` | equipment row `+0x1A` = granted id; licence row `+5` gate byte, eight `u16` ids at `+0x08`–`+0x16` | `ASC:153`–`165` |
| `listhelp_status.bin` | MMSG bank 12 | help text per status | `T32:229`–`242` |

### 1.3 State (globals and objects, with lifetime)

| state | lifetime / scope | cite |
|---|---|---|
| `[01DFE0B4]` frame base, 1 at 30 fps, 2 at 60; one writer (`001EDDF2`), 212 readers | process; sets every rate in the category | `SWP:625`–`633`, `PTC:176`–`180` |
| `*0x02EBF118` registry slot (null before the table loads); `*0x01F83530` runtime base; the row address is truncated to 32 bits | written by `003847B0` at install | `SWC:85`–`97`, `T32:265`–`268` |
| `0x02089340` bits `0x100` / `0x200` / `0x400` / `0x800` (defeat latches) | set by the defeat cleanup; re-evaluated each field frame | `SWP:280`–`286` |
| `02EBF188` "current target unit" slot, written by the merge | shared, 93 stores image-wide | `ELC:156`–`158` |
| `0208D480` / `0208DE80` 64-byte per-combatant records; `+0x14` stage-5 counter, `+0x18` walk-MP carry | party array keyed by definition row (survives the slot); non-party by slot `+0xEA9` | `PTP:481`–`486`, `MP:583`–`593` |
| `022C314C` active field-effect word, masks 1 (HP drain) and 2 (MP drain) | not stated in this folder (see gap N-12) | `PTC:280`–`282` |
| the result record, the rebuild's three 16-byte stack bitmaps | one call | `PTC:184`–`185`, `ASC:64`–`66` |
| `[02EBF190] + 0x5AD0` bit 0, `+0x5AD5` summoner, `+0x5B04` mode word | battle | `ASC:2119`–`2134`, `SWP:305` |

### 1.4 Order (what runs when)

- **Per frame, per unit:** `00233F70` calls `00310DB0` (`PTC:364`). Gates 1–3 (stats block, global mode not 5 / 6,
  field bit 15 clear) exit to the epilogue; the deadline check sits between gate 1 and gate 2 (`PTC:122`–`126`); the
  Esper dismiss check runs next and, if it dismisses, returns (`PTP:522`–`529`); then the readiness probe, the two
  masks and the unit flag fall to the common tail (`PTP:530`, `PTP:549`–`553`); then build 1 / apply 1, the trap
  applies, walk MP, the pickup and Chain Bonus, and the tail (`PTP:531`–`547`).
- **Inside a build:** stage 1 → 2 → 3 → 4 → 5, no reordering; stage 5 overwrites `+0x24` (`PTC:141`–`169`).
- **Inside the status write:** "mask → arrays → presence test → result record → applier → cascade → reaction → extra
  effect → terminal case → recompute. **The cascade runs before the reaction**" (`SWC:257`–`259`).
- **Inside the rebuild:** kind-0 masks or kind-1 `+0xE80` → equipment → licences → diff → apply (mode 3 adds, mode 1
  removes) → `002FEF30` → (kind 1 only) mode-5 pass over `+0xE90` and the five-byte exchange → three clamps
  (`ASC:132`–`217`).
- **Status expiry:** detected in stage 2 (status words) or stage 3 (effect slots); removed only inside `003112F0`
  (`PTC:171`–`174`, `PTC:214`–`215`).
- **Triggers of the rebuild:** equipment setters, the licence setter, level change, spawn activation, the status
  write's tail, the mutate body, `resetJobs` (`ASC:2558`–`2568`, `ELC:302`–`310`).

### 1.5 Dependencies

| system | relation | cite |
|---|---|---|
| CombatFormula `003112F0` (the applier) | the sink of every result here; calls `0030E360`, `0030E130`, `0030FED0` back | `PTC:65`, `PTC:346`–`349`, `ELC:298` |
| CombatFormula `003847C0`, `002FEF30`, HP write `00300530` | merge, stat rebuild, KO add / remove | `ELC:51`, `ASC:1607`, `SWP:415` |
| ActorEntity `0031B860` (record → unit, full-qword match, count re-read each pass) | used throughout | `ASC:625`–`659` |
| WorldAreaField `00377C20` (field bit 15) | gate 3, terminal-on-terminal waiver | `ASC:2119`–`2124` |
| Rewards `00312280`; CombatAI enmity `00321530`, `003219D0`; gambit counter `003279B0` | defeat, decay, effect ids `0x68`–`0x71` | `SWP:248`, `PTP:244`, `TLP:279`–`296` |
| RNG `00379CD0` (MT19937) | stage 2 Regen draw only | `PTC:226`–`251` |
| Items / licence tables; party focus and roster | rebuild sources; Esper dismiss `003138D0` | `ASC:153`–`165`, `ASC:2087`–`2091` |

### 1.6 Formulas the pages give whole

- **Default duration** (`00387730`): Petrify / Doom → 11; `0xFF` base → 0; harmful (`+6` bit 13)
  `trunc(2·b − b·Vit/100)`, else `trunc(b + b·Vit/100)` and ×1.5 under effect id 30; × `[01DFE0B4]` × 300
  (`SWC:367`–`375`, `SWP:146`–`158`).
- **Default beat** (`003876D0`): `row.+9 × [01DFE0B4] × 30` (`SWC:365`).
- **Stage 2 per status** (Poison `floor(maxHP/16)`, Bubble doubles, Disease uses `max(HP,1)`, zero share → 1; Sap −1
  above 1 HP; Regen `(rand % level) + 1`; Petrify → Stone, Doom → HP 0; HP Critical below `maxHP / 5`) (`SWP:173`–`182`).
- **Stage 4**: `+0x2A = maxMP / −50`, `+0x24 = maxHP / −100`, every `[01DFE0B4] × 10` ticks (`PTC:417`, `PTP:163`).
- **Stage 5**: 1 % after 10 beats, 2 % after 30, 5 % from 50 (`PTP:443`–`448`).
- **Refresh**: fourteen statuses with `+6` bit 5 restart their timers on a re-cast, one level up (`SWC:123`–`131`).
- **MP gain, walk MP, cost**: ladders and formulas whole, with shipped data (`MP:199`–`300`, `MP:371`–`427`,
  `MP:501`–`543`).

---

## 2. Gaps

Each row is one thing a re-implementer would need and cannot find, or two pages that disagree. **Class** is the
brief's routing class: STATIC (a desk read of the executable or data answers it), RUNTIME (needs a live observation),
DATA (needs a census of shipped data), DOC (the answer is on another page; this one lacks the pointer or contradicts
it). **Register** gives the `OPEN-QUESTIONS.md` row and its state cell, or "no row".

Four ids the contracts carry as open (`SW-1`, `SW-4`, `OPUS-NOTICE-NODE360`, the poison-arm request) have **no row in
the register** (a grep of `OPEN-QUESTIONS.md` for each returns nothing). That is noted per row and is itself a
register-hygiene finding.

### 2.1 STATIC

| id | gap | evidence | register |
|---|---|---|---|
| N-1 | **Whether the null-table fault is reachable** (`SW-1`). Both defaults (`003876D0`, `00387730`) and the cascade read through a null row when `status_data` is not loaded; nothing shows whether a status can be applied before the table installs. | `SWC:527`–`530` ("Nothing establishes whether a status can be applied before the table loads"); `SWC:277`, `SWC:289`–`303` | no row for `SW-1` |
| N-2 | **Status above 31, or no target unit: does the recompute tail still run?** Row 9 says the terminal switch is skipped by `0030E737 cmp ecx, 0x1F` / `ja`, but the `ja` target is not given. §15a shows the recompute lives in the shared tail `0030E816` that the switch cases reach; the §12 formula runs the recompute unconditionally after the switch. Which is right for `status > 31` and for a null `targetUnit` is not stated. | `SWC:275`, `SWC:358`–`359`, `SWC:615`–`628`; `SWP:238`–`239` (row 6 gate "target unit, status ≤ 31") | no row |
| N-3 | **`003E6B40`, the render side's defeat call**, is not read. The defeat cleanup's `002ED180` tail-calls it. | `SWP:302` ("the render side's defeat call, unread"), `SWP:471` ("What `003E6B40` … does on the render record … is not read") | `FA-3` **ANSWERED** (`OQ:2158`); the residue the page keeps is not on the row |
| N-4 | **The "auxiliary update" in `0030E130`.** The page says a re-apply returns "before the auxiliary update", and never says what that update is. | `TLP:240`–`242` | no row |
| N-5 | **What `BattleFormula_BuildRandomElementStatusTransitionResult` (`00386AE0`) writes**, and when it leaves result `+0x2C` bit 0 set so that the mutate body's `003112F0` apply fires. The mutate body selects it on every *set* (`cmovne`). The two status-write builders are specified (`SWC:467`–`477`); this one is only named. | `TLP:262`–`270`; `ELC:298` (names it only); `08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md:165` (it "carries" unit `+0x55`, `00386B71`); `_index/candidates/s24-runtime-per-invariant-exposure.md:145` ("Not read: `00386AE0`'s path condition for keeping bit0") | no row |
| N-6 | **Whether result `+0x2C` and `+0x140` flag bits are read anywhere but `003112F0`.** | `PTC:313` | no row |
| N-7 | **Stage 4's fallback below 50 max MP.** "a source value below fifty produces a **fallback** written from a different register"; the value is not given. §11 says "MP drains by max MP / 50 per beat (at least 1)", which implies but does not state the fallback. The HP arm (`maxHP / −100`) has no stated behaviour below 100 max HP. | `PTP:192`–`193`; `PTC:267`–`268`; `PTC:280` | no row |
| N-8 | **Is stage 4's HP arm on the same interval as the MP arm?** The interval test (`00385D78` raw tick, `div`, `jne done`) is shown before the MP store at `00385DBC`–`00385DCD`; the HP arm stores at `00385D51`–`00385D62`, **before** `00385D78`. §11 says both drain "per beat", but no page shows the HP arm passing an interval test. | `PTP:149`–`160`, `PTP:185`; `PTC:281`–`284`, `PTC:417` | no row |
| N-9 | **What keeps Regen's divisor non-zero.** `byte[stats + 0x1C2]` (the level) divides with no guard in that arm. §14 strikes the item as answered, but the answer gives only the field's meaning; the guarantee the §10 bullet asks for is not stated. | `PTC:270`–`271`; `PTC:314`–`315` | no row |
| N-10 | **What the rebuild's gate values mean**: equipment rows contribute only when `0031E9A0` returns 3, licence rows only when `00323890` returns 2. §13a gives the class-to-gate mappings; what the gate classes are is still "FABLE's". | `ASC:2442`; `ASC:429`–`435`; `ASC:513`–`515` | no row |
| N-11 | **Whether licence node 360's owned bit is reachable** (the grant refuses node 360 until presence bit `0xC01F` is set; what sets that bit is not traced). | `ASC:246`–`247` (`OPUS-NOTICE-NODE360`) | no row |
| N-12 | **Initial values at record creation.** No page in this folder states what `+0x64`, `+0x3C`, `+0x38`, `+0xBC[32]`, `+0x13C[32]`, `+0x17C[8]`, `+0x68` and `+0x78` hold when a stats record is created or reset before its first rebuild. `+0x3C` and `+0x38` are rebuilt by `002FEF30`; the others are not stated. *(The stats-record field map in `08-Combat-Formula/Battle-Stats-Record/` lists writers; it was not audited here.)* | `SWC:136`–`143` (state: "read / written", no initial value); `ASC:1645`–`1649`; `ELC:150`–`158` | no row |
| N-13 | **What feeds the walk-MP accumulator.** The recovery step drains and re-adds unit `+0x70` (`00320450`, `00329A20`) and earns a point when it exceeds the row's interval ("every 9 accumulator units of walking"); what adds walking distance to `+0x70`, and in what unit, is not stated. | `MP:283`, `MP:293`–`296`, `MP:541`–`543` | no row |
| N-14 | **`byte [rsi]` bit 5 in the merge's second revocation** (`003847C0`, `003848A1`). Narrowed elsewhere: the evaluation-context page calls it "the result's `+0` bit 5", but what that bit means is not stated. | `ELC:125`–`130`, `ELC:219`; `08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md:160`–`161` | no row |
| N-15 | **Which on-screen list each status order-key kind drives** (`+0x10`, `+0x26`, `+0x27`, `+0x13`, `+0x02` → listings 0–4). The page still carries it as open; the register row is closed. | `T32:367`–`370`, `T32:375` ("Still open: which on-screen list each key kind drives") | `GA-1` **ANSWERED** (`OQ:2419`), the residue is not on the row |

### 2.2 RUNTIME

| id | gap | evidence | register |
|---|---|---|---|
| N-16 | **Whether natural KO reaches the defeat cleanup's release and dismiss legs**, the bit-22 state a fallen unit is in, the helpers' transitive effects, the relation cache's binding, timing. | `SWP:323`, `SWP:331`–`333`; `ASC:2102`–`2105`, `ASC:2139`–`2140` | `UQ-147` **SUPERSEDED** under the runtime rule (`OQ:2861`) |
| N-17 | **No live observation of any operation here.** The status write's three queued observations (Slow on Haste, the Petrify count, KO of a party member and a foe), the rebuild's §11 ("Observable behaviour: Not established"), and the layers and tick (native replay only) are all unobserved in a game. | `SWC:519`–`523`; `ASC:254`–`258`, `ASC:2428`–`2434`; `ELC:212`–`214`; `PTC:305`–`306` | no row |
| N-18 | **The tick's cadence.** Every wall-clock figure (Poison 12 s, Regen 1.5 s, the 1 %/2 %/5 % per second ramp) "rest[s] on the tick running once per unit per frame"; `00233F70` is named as the caller but its call rate is not established here. | `PTC:275`–`278`; `PTP:443`–`446`; `PTC:364` | no row |

### 2.3 DATA

| id | gap | evidence | register |
|---|---|---|---|
| N-19 | **The name of effect id 15** (the one the merge revokes) and **the rest of the effect-id namespace map** (`02EBF040`, 129 rows). Named so far: 2, 16, 17 (`TLP:90`–`94`), 20, 21, 23, 32, 36, 39, 51, 86, 91–93 (`MP:354`–`364`), 52 and 104–113 (`TLP:331`–`336`), 55–57 (timer slots). | `ELC:218`, `ELC:220` | no row |
| N-20 | **The mutable-layer meaning of effect ids 2, 16 and 17, and the name of effect id 30.** After the 2026-10-02 correction the mutable-layer column of the namespace map can no longer be the status names Petrify / Disease / Lure (see N-32), and no page gives what those ids are in `+0x68`. Effect id 30 (×1.5 duration) is "the shape of a duration-extending augment, whose authored name is not read here". | `TLP:90`–`94`, `TLP:102`; `SWP:165`–`167` | `E-1` **CLOSED** (`OQ:178`) on the old reading |
| N-21 | **"173 of 1,154 fields"** (field selector 2 or 3, the MP tripling) is borrowed at tier 2 and not re-censused. | `MP:627`, `MP:62`–`63` | no row |

### 2.4 DOC (pointer missing, or pages disagree)

| id | gap | evidence | register |
|---|---|---|---|
| N-22 | **`SW-4` is answered elsewhere.** The contract still asks what `0046AB10` does with `0x12` / `0x11` beyond posting. The two-layer page describes the poster's ten-entry dedup ring and its tick window; the rebuild contract executed it (§13bc, §13bf, §13bg). | open: `SWC:539`–`545`; answer: `TLP:401`, `ASC:1949`, `ASC:2008`, `ASC:2028` | no row for `SW-4`; `EY-3` **ANSWERED** (`OQ:2132`) |
| N-23 | **"What the mask BITS mean — `0x108` names two bits whose consumers are not identified"** is answered on the page: `+0x2C \|= 0x108` is "apply HP, absolute", and the tick page reads flag A bit 8 as the HP write and bit 3 as absolute. | open: `SWC:534`–`536`; answer: `SWP:233`, `SWP:182`, `PTP:309` | no row |
| N-24 | **The row-4 predicate is attributed to the wrong function.** `SWC` says `FieldData_GetActiveFieldRecordBit15` holds "`dword[unit]` bit 24 denies; `word[+0x714] > 0x21E` … `== 0x113` denies". The rebuild contract reads `00377C20` as a closed field-record bit query with no unit read, and the status-write page gives that bit-24 / `+0x714` / `+0x6B4` / `0x113` filter as the **case-4 (statuses 5, 27) reset filter**. | `SWC:446`; `ASC:2119`–`2124`; `SWP:254`, `SWP:541` | no row |
| N-25 | **Kind and type byte offsets are swapped inside `SWC`.** §3 lists the unit's "`+0x04` kind byte and `+0x05` type byte"; §10 row 3 and the page use kind `+5 == 0`, type `+4` in `0x1B..0x27`. | `SWC:76` vs `SWC:269`, `SWC:333`; `SWP:90`–`91` | no row |
| N-26 | **Stale "party-side" / "Vanished" / "+9 timer" wording** survives beside the corrections: the page's header, call chain and evidence table still say "party-side shortcut" / "party shortcut"; the terminal table still says "31 (Vanished)"; `SWC`'s formula comment says `/* party side */`; the thirty-two-statuses corpus line still calls `+9` "the default timer". | `SWP:29`, `SWP:250`, `SWP:422`, `SWP:490`; `SWC:334`; `T32:43` | no row |
| N-27 | **The tick's gate count and the deadline's position disagree across the pair.** `PTP` says the deadline check is "run before any of them" (gates); `PTC` I-1 says it runs after gate 1 and before gate 2. `PTP`'s call chain and evidence table still say six gates; `PTC`'s text says seven but its gate table has six rows (the readiness probe is missing) and §7 still reads "gates 2–6". | `PTP:62`, `PTP:257`, `PTP:316`; `PTC:103`–`112`, `PTC:122`–`126`, `PTC:213` | no row |
| N-28 | **Stage 5's record base.** `PTC` §5 and §8 still say the records are "at `0208D494`" and that the counter is their "first word"; `PTC` §14 and `PTP` correct this to records based at `0208D480`, counter at field `+0x14`, walk-MP carry at `+0x18`. | `PTC:193`, `PTC:220`–`222` vs `PTC:310`, `PTP:481`–`486` | no row |
| N-29 | **"Not executed: stage 2's Poison, Sap and expiry arms"** is stale. The requested replay is recorded as run (14/14) in the builder replay's candidate record, and the page cites an independent Method A acceptance of the Poison and HP Critical boundaries. | `PTC:304`–`305`; `_index/candidates/s27-opus-replay-periodic-builder/README.md:88`–`119`; `SWP:182` | no row (the request `FABLE-REQ-OPUS-POISON-ARM-REPLAY` is not a register id) |
| N-30 | **`022C314C` is named only "the active field's word".** The post-result page reads it as the active magick-field mask that `set_field_effect` / `clear_field_effect` drive and posts its begin and end lines; the unit-definition page records a block wipe that zeroes it. | `PTC:280`–`282`; `07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:352`, `:513`; `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:664` | no row |
| N-31 | **Gate 2's "global mode" is unnamed** in both tick pages. The gambit page names it: `022C2160` 5 or 6, a special-sequence presentation on screen (`00310E02`–`00310E0E`). | `PTC:109`, `PTP:53`; `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md:478`–`479`; `ASC:676` | no row |
| N-32 | **The Disease / Weatherproof alias is both asserted and refuted.** The 2026-10-02 corrections say the 32 statuses are not in either layer, so a Diseased unit does **not** satisfy the Weatherproof early-out. Uncorrected text still says it does, or names the mutable-layer ids by status names: `TLP` §1, the namespace map's "Mutable status" column, §7 (E-1 closed as "Petrify and Disease casters fire the … bypasses"), §11, §12 ("exactly as Disease aliases Weatherproof"); `MP`'s "a temporary status and a derived augment are interchangeable"; `T32`'s "read" column for ids 2, 9, 15, 16, 17; and `ELC` §11 ("a character afflicted with Disease are … the same character"), which contradicts its own corrected L-4. | stale: `TLP:36`–`39`, `TLP:90`–`94`, `TLP:143`, `TLP:256`–`258`, `TLP:366`–`368`; `MP:366`–`367`; `T32:65`, `T32:72`, `T32:78`–`80`; `ELC:197`–`198`. Corrected: `ELC:112`, `TLP:102`, `TLP:119`–`122`, `T32:142` | `E-1` **CLOSED** (`OQ:178`), closed on the refuted reading |
| N-33 | **Internal inconsistencies in `ASC`.** §7a now has three stages, but §4 still says "four more things are true afterwards" and the §15 claim table says "four further stages follow". §13ak labels the kind-0 row table `FOED` (foe) while §13g and §13al correct kind 0 to the 40-row party table. | `ASC:186` vs `ASC:91`–`94`, `ASC:2478`; `ASC:1566`–`1570` vs `ASC:743`, `ASC:1617` | no row |
| N-34 | **The rebuild has no whole reproduction formula.** §12's block is "the kind-0 accumulation and the apply, and nothing else … **Do not implement from this block alone.**" The kind-1 source, the eight licence fields and the §7a tail are given only in prose and in §13ak's notes. | `ASC:262`–`266`; prose: `ASC:132`–`217`, `ASC:1566`–`1591` | no row |
| N-35 | **The README's "Not yet documented" list is stale.** It still lists "KO, revive and terminal state transitions" and "Status timers and the augment Timer Link field"; the terminal cases, recover and defeat paths (`SWP` §2.7, §2.7a; `ASC` §13g), the status timers (`SWP` §2.4a) and the effect-slot timer byte (`PTP` §4, §9) now cover them. | `README:35`–`36`; `SWP:241`–`315`, `ASC:706`–`730`, `SWP:136`–`191`, `PTP:137`–`139`, `PTP:276` | no row |
