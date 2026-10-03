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
