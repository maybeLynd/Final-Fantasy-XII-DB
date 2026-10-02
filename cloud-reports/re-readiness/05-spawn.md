# Reconstruction readiness — `FFXII TZA/05-Spawn-Encounter-Lifecycle/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-05-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `4da4b9d0` only; no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives its location. |

## Counts

| | |
|---|---:|
| `.md` pages read (every one in the folder and its subfolders) | 8 |
| member `.tsv` files checked for layout and row counts | 2 |
| entry-point rows listed (§1.1) | 47 |
| open items the pages list themselves (§2.1) | 14 |
| structural gaps: a function, formula or format a port needs that no page states (§2.2) | 16 |
| **contradictions, total (§2.3)** | **52** |
| — A. value-changing (each marked "page-text only - needs local check") | 18 |
| — B. counts and sizes that disagree but change no ported behaviour | 6 |
| — C. stale "open / not read" claims, banners and names | 28 |
| — of all 52, items where a dated correction on the pages names a favoured side | 16 |
| **Rating (§3)** | **NOT YET** overall. Group ledger and keep-entry map: MOSTLY. |

## Citation form

`ABBR:line` means a line of the page below. Every path is relative to `FFXII TZA/05-Spawn-Encounter-Lifecycle/`.
"Not stated" means none of these eight pages says it.

| abbr | page | status as the page states it |
|---|---|---|
| README | `README.md` | category index. It lists 2 of the 7 system pages (`README:11-24`) and gives "Functions 52" (`README:8`) |
| SPR | `spawn-placement-and-retirement.md` | front matter: `status: DOCUMENTED — owner re-status 2026-10-01 …` (`SPR:4`), `audit.passes: 3`, `reopened_count: 5` (`SPR:20-24`). The body has a 2026-09-02 banner, reconciled at `SPR:36-37` |
| HT | `spawn-placement-height-and-authored-tunables.md` | `status: AUDITED` (`HT:4`), `audit.passes: 1` (`HT:20`). The body says "`status` is `DOCUMENTED`, `audit.passes` is `0`" (`HT:872-873`); see C7 |
| WHY | `why-the-enemies-you-killed-come-back.md` | `status: AUDITED`, `evidence_tier: 1` (`WHY:4-6`) |
| C-SP | `CONTRACT-spawn-placement.md` | `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (`C-SP:6-7`). Falsification pass 1 dated 2026-09-29 (`C-SP:274-338`) |
| C-GC | `CONTRACT-group-completion-and-respawn.md` | `readiness: CONTRACT READY`, `confidence: PROVEN`, `crossref_clean: false` (`C-GC:6-7`, `:22`) |
| GC | `Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` | `status: AUDITED`, `readiness: BEHAVIORALLY UNDERSTOOD` (`GC:4`, `:8`) |
| FM | `Spawn-Record/the-spawn-keep-entry-field-map.md` | `status: AUDITED`, `readiness: BEHAVIORALLY UNDERSTOOD` (`FM:4`, `:8`) |

**Member files checked.**
- `spawn-group-ledger-accesses.tsv`: 19 data rows, columns `function name site disp kind instruction route note`. It covers three functions only (`00306E60` ×3, `00306F00` ×4, `00307090` ×12). The pages count six functions; see B3.
- `Spawn-Record/spawn-record-accesses.tsv`: 106 data rows in 21 functions, the same columns. That matches FM's "the array census beside this page (`--array`, depth 2, 106 rows)" (`FM:76-77`). No row falls in the three ranges FM calls untouched (`+0x42`–`+0x4F`, `+0x7D`–`+0x7F`, `+0x248`–`+0x24F`), and none is at `+0x74`.

---

## 1. Interface

The folder documents five connected mechanisms:
- **tunables**, installed by script;
- **placement**: choosing a candidate (point or area mode), then the activation-time height;
- **range and point retirement**;
- **the spawn-keep record and its two persistence banks**, rotated on area transition;
- **the group-completion ledger** and the respawn clock.

### 1.1 Entry points (functions, with their callers)

#### Script-facing tunables and verbs

All of these are reached from the family-3 (`0x30xx`) ScriptVM result-callback column at `01F281D0 + 0x20 × (opcode & 0xFF)` (`HT:304-318`, `HT:484-485`).

| entry | caller | what it does | cite |
|---|---|---|---|
| `FUN_0023A520` (66 B), the tunable reset | thunk `00510710`, verb `0x3053` `btlAtelSetupActorStart` | installs min 39.0, max 42.0, retire 43.0, arc 180, attempt limit 1 | `HT:285-302`, `HT:581-587` |
| `Spawn_SetNativeLifecycleRanges` `0023A1D0` (25 B) | `0050F410`, verb `0x300B` `btlAtelSetSpawnDistance` | script order `(min, max, retire)`; native order `xmm0→retire, xmm1→max, xmm2→min` | `HT:329`, `HT:589-596` |
| `Spawn_SetCandidateHeadingArcDegrees` `0023A1F0` (11 B) | `0050F470`, verb `0x305B` `btlAtelSetSpawnLimitDegree` | truncates a float to the i32 arc at `02089358` | `HT:337`, `HT:461`; `C-SP:125-127` |
| `Spawn_SetPositionAttemptLimit` `00239020` (19 B) | `0050FC00`, verb `0x3038` | clamps below 1 only, stores `CL` | `HT:331`, `SPR:1444-1446` |
| `VM_Spawn_SetAutomaticActiveCap` `00510320` | verb `0x304E` | writes cap byte `0208D458` inline | `HT:333` |
| `FUN_00510360` / `VM_Spawn_GetActiveCapTrackedCount` `00510390` → `00308D90` | verbs `0x304F` / `0x3050` | cap getter / count of units with flag bit 21 | `HT:334-335`; `SPR:334-338` |
| `SpawnKeep_SetReturnWindow` `00235340` (17 B) / `GetReturnWindow` `00235330` (7 B) | `005107F0`, verb `0x306C` `btlAtelSetMapJumoKeep` (0 of 1,114 US scripts call it) | `w < 0 → 300`, else store | `SPR:111-120`; `HT:338`, `HT:749-753` |
| `FUN_005102D0` (35 B) | verb `0x304D` `btlAtelCanselInitialSpawnFlag` | `unit.qwUnitFlags \|= 1<<45` | `HT:245`, `HT:257-262` |
| `SpawnKeep_InitializeEntriesFromDefinitionTable` `002395A0` (268 B) | tail of `005106D0`, verb `0x3018` `btlAtelSetEntryStruct` | rolls the death limit and cooldown per uncommitted entry; sets the persistence key | `FM:127-145` |
| `SpawnUnit_SetEntryMapAndResetTransientEntries` `0023A2E0` (161 B) | `00510620` | installs the lane map at unit `+0x40`; resets fresh entries | `FM:161` |
| `SpawnEntry_ResetTransientState` `00236860` (103 B) | `005104D0` | the same reset for one entry; lane in `r8d` | `FM:162`; `GC:954-955` |
| `SpawnUnit_BindEntryAndMarkCapTracked` `00239840` (168 B) | `005103F0` | lane byte `+0x57`, keep `+0x16`, unit flag bit 21 | `FM:164` |
| `SpawnEntry_SetCurrentCandidateState` `00239410` (169 B) | `0050FCB0` | keep `+0x50`/`+0x60` from two floats; unit flag bit 26 | `FM:165`, `FM:102` |
| `SpawnEntry_SetRangeRetireInhibitTag` `002391C0` (80 B) | `00510370` | keep `+0x15` and flag bit 4 | `FM:166`, `FM:94` |
| `BattleUnit_SetRuntimeUnitCategoryMode` `002396B0` (82 B) | `00510340` | unit `+0x58` from the 4-entry table `01E09EE8`; keep flag bit 5 | `FM:167` |
| `SpawnEntry_ConfigureFreshLifecycleFloatMode` `0023A200` (185 B) | `005107C0` | keep `+0x04` float and flag bits 3/6; unit flag bit 40 | `FM:168`, `FM:87` |
| `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` (270 B) | `00510250`, verb `0x304C` `btlAtelSetUnitFinish` | starting-HP override; clears bits 0/2; ground probe; publishes the position | `FM:169`; `HT:133-154` |
| keep getters `00235F50`, `00235FB0`, `002366E0`, `00235EF0`, `00236140`, `00236030`, `00236670` (93–155 B) | VM wrappers; the three respawn readers' only callers are `0050F660`, `0050FAB0`, `005101F0` | the shared 7-check prologue, then one field | `FM:172`; `C-GC:95-99`; `GC:56-76` |
| `Spawn_SelectAndPrepareAutomaticEntry` `00235720` (841 B) | `VM_Spawn_SelectAutomaticEntry` `0050F520` only, verb `0x301A` `btlAtelDecideEntryPointAuto` | cap gate, respawn eligibility per lane, min-radius choice, attempt loop | `SPR:288-317`, `SPR:694`; `HT:465` |
| `Spawn_SelectContinuousEntry` `00235360` (390 B) | `00510260`, verb `0x305F` `btlAtelDecideEntryGroupByContinuous` | same-key match in the history bank; whole-entry copy | `SPR:839-850`, `SPR:695` |
| `Spawn_SelectPreviousMapEntry` `002354F0` (166 B) | `00510230` (pass-22 edge only, `FM:406`); script name `btlAtelDecideEntryGroupByPreviousMap` (`HT:271`) | **not stated**: only that it tests flag bits 1 and 2 (`FM:117`) | `FM:173` |
| `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0` (376 B) | **not stated** | writes keep `+0x50`/`+0x60` (`FM:101-102`); draws from the RNG (`FM:404`) | `FM:173`; `HT:473` |

#### Placement

| entry | caller | what it does | cite |
|---|---|---|---|
| `Spawn_TrySelectCandidatePosition` `00234AF0` (584 B) | `00235720` only | `(ECX candIdx, RDX outPos, XMM2 min, XMM3 max, arg5 out_observed, arg6 slotFlag)`; point mode or area mode | `C-SP:310-316`; `SPR:128-159` |
| `003209C0` (29 B), wrapping `FieldData_CopyIndexedRecordByFormatClass` | `00234AF0` | format class 0, record `ECX`; returns 0 on success, −1 on failure | `C-SP:49`, `C-SP:65-67`; `SPR:1434` |
| `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` (290 B) | `00234AF0` (flag 0); `BattleUnit_HasNonPartyEngagementEvidence` `00308040` (flag 1, result inverted) | squared-XZ band; every eligible slot must pass and at least one must exist | `SPR:180-229`, `SPR:682-686`; `C-SP:294-307` |
| `FUN_00319390` (139 B) | `00234AF0` | polar offset; writes `[0]` and `[2]` only | `HT:87-101`, `HT:533-545` |
| `FieldRegion_ContainsWorldPosition` `002374E0` (334 B) | `00234AF0` | area mode's only filter; reads XZ only | `HT:115-120`; `C-SP:190` ("`1` box, `2` ellipsoid") |
| `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (316 B) | `0037B4D0` (pass-22 edge, `FM:399`) and others not stated | sets keep flag bit 1 and unit bits 49 and 3; clears bit 26; calls `00239E10` | `HT:251-255`, `HT:452`; `FM:117`, `FM:170` |
| `FUN_00239E10` (594 B) | `00233AD0` at `00233B51` | writes unit `+0x1F6` (height mode) and `+0x188` (vertical offset) | `HT:178-216` |
| `FUN_003208C0` (119 B), the ground probe | `0023A410` at `0023A4BC` | `{x, 1.0, z, 1.0}` → `0026E3C0`; Y, or 0.0 on a miss | `HT:156-174` |

#### Retirement, banks, save and load

| entry | caller | what it does | cite |
|---|---|---|---|
| `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` (529 B) | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` at `00234022` only | gate chain, then mode 1 (range) or mode 2 (authored point) | `SPR:233-284`, `SPR:696`; `SPR:1368-1379` |
| `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780` (672 B) | `BattleSystem_InitializeAreaState` `002342F0` at `00234423` only | A→B→A swap inside the window, else push and wipe | `SPR:349-380`; `WHY:41-81` |
| `BattleSystem_InitializeAreaState` `002342F0` (390 B) | `00266D10` at `00267136`; `0026CE60` at `0026CEC6` (manager index 0 only) | gate `02089300`; cap ← 28; ledger reset; rotation | `SPR:1650-1656`, `SPR:1688-1702`; `GC:215-216` |
| `SpawnKeep_SerializePersistenceBanks` `00233440` (260 B) | `00229CF2`; `005845AA`, `005845E1` | both banks into a `0x20010` buffer, with the field-id pair | `SPR:382-386`, `SPR:435-437`, `SPR:698` |
| `SpawnKeep_RestorePersistenceBank` `00233550` (127 B) | `0058443B`, `0058445E` in `005843E0` | buffer `+0x10` → bank 2, then the field-id pair | `WHY:140-146`; `SPR:1583-1601` |
| `BattleSystem_ResetRuntimeState` `00237DF0` | the guard `00233C10` | tick stamp ← 0, field ids ← `0xFFFF`, parity ← 0, clock ← 0 (via `0032A160`) | `WHY:88-97`; `SPR:3407-3414`, `SPR:3526-3529` |

#### Group ledger and death

| entry | caller | what it does | cite |
|---|---|---|---|
| `SpawnGroup_ConfigureUnitMembershipAndMode` `00239710` (114 B) | `0050F8C0`, verb `0x3030` `btlAtelSetEventFlagGroup` | `+0xE98 = group`, `+0xE99 = mode bits`, then `00306E60(unit, 1)` | `GC:303-327`; `C-GC:78-79` |
| `SpawnGroup_UpdateExpectedMemberLaneMask` `00306E60` (158 B) | `00239710` (add); `002350C0` at `002352BB` (remove) | `memberMask` set or clear; `deadMask` bit always cleared | `GC:271-301` |
| `SpawnGroup_RecordMemberDeathAndHandleCompletion` `00306F00` (303 B) | `00300530` at `0030082F` | dead bit; completion test; event lock; arm by mode | `GC:377-413`; `C-GC:212-231` |
| `BattleStats_ModifyHPAndProcessLethal…` `00300530` (880 B) | `BattleStats_SetCurrentHP` `00300520`, among others | lethal branch: keep `+0x08 += 1`, `+0x0C = seconds`, then `00306F00` | `GC:130-147`, `GC:428-433` |
| `SpawnGroup_DispatchPendingCompletionSignals` `00307030` (82 B) | `BattleSystem_RunFieldFrameOrchestrator` `00234590` | per frame, gated by `00233D20`; posts `table[3] = group` | `GC:263`, `GC:464-472` |
| `SpawnGroup_HasPendingCompletionSignal` `003070E0` (39 B) | `00233F70` at `00234095` | none pending → `02089340 \|= 2` | `GC:568-571` |
| `SpawnGroup_MarkCompletionPendingAfterReaction` `00307110` (40 B) | `003250F0` only, reached through guard stub `002E70A0` in handler slot `02CA4470` (id `0xC`, track end) | clear unit bit 47; `flags \|= 1` | `GC:265`; `C-GC:343-351`, `C-GC:570-584` |
| `SpawnGroup_ResetLifecycleLedger` `00307090` (73 B) | `002342F0` only | both masks ← 0; flag bit 0 cleared | `GC:165-252`; `C-GC:450` |
| event-lock trio `00307140`, `00238B70`, `00238AE0` | `00306F00` (literal 1); other callers `0026C5D0`, `00359A30`, `0035A6F0`, `0035AB20` | row 12 capability bits; party suppression; `02089340` bits `0x20`, `0x80` | `GC:573-589` |
| post `0026ADC0` (35 B) | `00307030` | `*(02098E68)[index] = value` when `index < 64`, `02098E20` bit 0 is set and the pointer is non-null | `C-GC:84`; `GC:469-477` |
| group-mask ops `00234880`, `00234990`, `00234A10`, `00234A80`, `002352E0` | `hideenemy` `00349940` / `showenemy` `00349200` (bit-11 pair); others not stated | teardown, or set/clear flag `0x800`, or set HP to zero, over `1 << (groupId & 31)` | `SPR:439-462`, `SPR:793-802` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

**The spawn-keep entry (`SpawnRecord`, BKEI), `0x250` bytes, 64 per bank.** This is the full layout as FM states it (`FM:84-108`, `FM:182-198`).

```
+0x00 u32  lifecycleFlags   b0 range-reentry-pending  b1 activation-committed  b2 released
                            b3 point mode (+)  b4 range-retire-inhibited  b5 category-4 mode
                            b6 point mode (−)  b7 affinity dirty                    (FM:116-123)
+0x04 f32  |threshold|; the sign chose b3/b6 (0023A200)
+0x08 u16  death count      +0x0A u16 death limit = base + rand % (range+1), or 0
+0x0C u32  last-death second
+0x10 u16  respawn cooldown, whole seconds = base + rand % (range+1), or 0          (FM:137-139)
+0x12 u8   spawn-history counter copy        +0x14 u8 steal bits 0-2
+0x15 u8   range-retire tag   +0x16 u8 script selection (0xFF none)
+0x17 u8   persistence key    +0x18 u8 authored key (the restore value)
+0x19 u8   enmity decay       +0x1A..+0x41 u8[40] enmity by combatant id
+0x42..+0x4F untouched
+0x50 f32[4] persisted world position     +0x60 f32[4] candidate {x, y, z, -}
+0x70 f32  facing yaw         +0x74 u32 from unit +0x160 at release (no reader)
+0x78 u8[5] elemental affinity            +0x7D..+0x7F untouched
+0x80 BattleStatsRecord (0x1C8)           +0x248..+0x24F untouched
```

- **"Fresh"** means `(flags & 5) == 0` (`FM:200-202`).
- The selector's direct field reads are listed at `SPR:295-300`.
- The SPR §4 diagram disagrees on offsets; see A5.

**The group ledger (`SpawnGroupLedger`).** 64 entries of 24 bytes at `02EC13C0`, BSS, addressed as `(group − 1) × 24` (`C-GC:140-145`; `GC:184-197`):

```
+0x00 u64 memberMask   +0x08 u64 deadMask   +0x10 u8 flags (bit 0 = completion pending)   +0x11..+0x17 padding
```

Only bit 0 of `flags` is touched anywhere in the image (`GC:231-248`).

**Battle-unit fields this system reads or writes**:

| offset | meaning | cite |
|---|---|---|
| `+0x00` u64 flags | bit 4 (`0x10`, the slot-pool predicate); bit 11 (`0x800`, script hide); bit 21 (cap-tracked); bit 26 (entry point prepared); bit 33 (reaction handled); bit 45 (script: not an initial placement); bit 47 (completion deferred); bit 49 (activated once) | `HT:506-512`; `SPR:452-462`, `SPR:851-857`; `SPR:334-338`; `C-GC:150-151`; `GC:622-623` |
| `+0x08` | packed actor handle | `SPR:526` |
| `+0x10` | actor work; its `+0xF6` word is the bkei | `C-GC:530-546` |
| `+0x40` | lane map: `[0]` count, then one slot byte per lane, `0xFF` = empty | `GC:703`; `FM:50` |
| `+0x188` f32 | spawn vertical offset | `HT:513`, `HT:215-216` |
| `+0x1F6` u8 | height mode; bit 3 (value 8) runs the probe | `HT:514`, `HT:210-213` |
| `+0x698` | stats record; `[+5] == 1` means spawn-backed (enemy table) | `C-GC:152-153`; `GC:749-754` |
| `+0x6A0` | the keep entry | `C-GC:154` |
| `+0xE68` | applied definition; `[+0x18]` bits 4/5/6 | `HT:517-522` |
| `+0xE98` u8 | 1-based group id; 0 = no group; sole writer `00239746` | `GC:706` |
| `+0xE99` u8 | bit 0 = mode 1, bit 1 = mode 2 | `GC:707` |
| `bLifecycleMode`, `bLifecyclePointId`, `flLifecyclePointThreshold` | names only; **offsets not stated** | `SPR:530-535`; see G4 and A8 |

**Other records.**

| record | layout as stated | cite |
|---|---|---|
| definition table, the `0x3018` argument | `b_00` count, `b_01` keys-authored flag, `w_02` row stride, rows from `+4`. Row: `b_00`/`b_01` death-limit base/range, `w_02`/`w_04` cooldown base/range, `b_06` key, `+7` = 0. Shipped data: stride 8 in all 502 scripts; `b_01` = 100 | `FM:129-141`, `FM:252-268` |
| format-class-0 candidate record | byte `+0x00` selects the mode (0 = point); `+0x10` is the authored position. **Nothing else is stated**; see G2 | `C-SP:55-56`; `SPR:137` |
| applied definition `+0x18` | bit 4 → height mode 8 (probe); bit 5 → 2 rather than 1; bit 6 adds 4 | `HT:519-522` |
| persistence save buffer, `0x20010` bytes | `+0x00` previous field id, `+0x02` most recent, bank 2 at `+0x10`, bank 1 at `+0x10010` | `SPR:435-437`, `SPR:886` |
| save-image placement | group A `E240`, keep A `E440`, group B `2E450`, keep B `2E650`, metadata `4E660` (whole-image offsets) | `SPR:1624-1632` |
| field table at `*(02098E68)` | 64 elements. Slot 3 is the script variable `scratch1 short @0x06`; scripts `waitv` on it | `GC:817`; `C-GC:294-305` |

**Outputs.**

| output | cite |
|---|---|
| actor placement: keep `+0x60..+0x68` passed to `BattleUnit_PublishLocomotionPosition` `00300310` | `HT:137-151` |
| the completed group's number in table slot 3 | `C-GC:237-238` |
| the event lock: row 12 bits `{0,3,4,5,6,7,8,11,12,20}`, party suppression, `02089340 \|= 0x20 \| 0x80` | `C-GC:442`; `GC:579-584` |
| presentation events `0x2005` / `0x2008` | `GC:403-410` |
| unit teardown through `BattleUnit_TeardownAndDespawn` `00300E40` | `SPR:271-277` |
| the save image (see "Other records") | — |

### 1.3 State (globals and objects, with lifetime)

| state | type / initial value | written by | lifetime as stated | cite |
|---|---|---|---|---|
| `02089358` arc degrees | i32, BSS 0; 180 after the reset | `0023A520`, `0023A1F0` | until the next script install | `SPR:80`, `C-SP:125-127` |
| `02089360` / `02089364` / `02089368` min / max / retire | f32, BSS 0; 39 / 42 / 43 after the reset | `0023A520`, `0023A1D0` | the same; "at process start are zero" | `SPR:81-83`; `HT:656-658`, `HT:1056` |
| `0208D457` attempt limit | u8 storage, used as signed i8; 1 after the reset | `0023A520`, `00239020` | the same | `HT:498`; `SPR:1442-1455` |
| `0208D458` active cap | u8, used as signed i8; 28 | `002342F0` at `0023433C` | reinstalled at every area init | `SPR:86`, `SPR:876`, `SPR:1457-1459` |
| `0208936C` return window | i32; 300 | `002368D0` at `00236A0D`; `00235340` | process; not in the save | `SPR:85`, `SPR:864`; `WHY:85-95` |
| `0208935C` | f32 5.0, never read | `002368D0` | dead | `SPR:106-107` |
| `02F973B8` max considered squared distance | f32 +INF, from `00914700` | `002368D0` | shared with AI and loot | `SPR:324-329`, `SPR:877` |
| `0208E690` / `0208E698` keep banks | heap pointers to `0x9400`-byte zeroed allocations (`btlKeepCharWork1`/`2`) | `002368D0` | process. Bank 1 = live, bank 2 = history | `SPR:342-347`; `WHY:88-92` |
| `02089370` / `02089372` field history (last / two ago) | u16; `0xFFFF` on the reset path | `00233780` tail; `00233550` (slot-0 load); `00237DF0` | in-process; restored only on an autosave load | `WHY:80-81`, `WHY:92`; `SPR:3412-3413` |
| `02089374` transition stamp | u32; 0 on the reset path | `00233780`; `00237DF0` | never restored | `WHY:93` |
| `0208D45C` raw tick counter | u32; 0 on the reset path | "advanced by `0032A100`"; reset by `0032A160` | never restored. **Advance rate not stated** (G1, A9) | `WHY:94`; `SPR:3526-3529` |
| `0208D454` parity | flips on every rotation; 0 on reset | `00233780`; `00237DF0` | never restored | `WHY:75`, `WHY:95` |
| `0208D354 + parity × 0x80` | u16[64]; filled with 1 on the wipe path | `00233780` | reader **not stated** (G10) | `WHY:76-78`, `WHY:180-181` |
| ledger `02EC13C0` | 64 × 24, BSS zero | `00306E60`, `00306F00`, `00307110`, `00307030`, `00307090` | reset at every area init; rebuilt by script; never saved | `C-GC:192-193`, `C-GC:677-678` |
| `*(02098E68)` table | 64 × 16-bit (signedness: A2) | `0026ADC0` | `scratch1`, cleared on every field transition | `GC:605`, `GC:817` |
| `02089340` battle-state word | bits `0x2`, `0x20`, `0x80` written here; `0xF00` read | `00238B70`, `00238AE0`, `00233F70` | not stated | `GC:694` |
| keep entry | `0x250` bytes in a bank. Rolled by `002395A0` when uncommitted; reset when fresh | see §1.1 | wiped when a rotation misses the window | `FM:134-145`; `SPR:738-739` |
| unit flags 45 / 49 | never cleared; reuse preserves them | `005102EB` / `00233B8C` | for the unit slot's life | `HT:247-249`, `HT:688-690` |

### 1.4 Order (what runs when, and what triggers it)

1. **Area entry.**
   - `002342F0` runs when `02089300` admits it. It sets the cap to 28, resets the ledger (`00307090`) and calls the rotation `00233780` at `00234423` (`SPR:1650-1653`; `GC:215-217`).
   - It is reached from `00266D10` and from `0026CE60(index 0)` (`SPR:1686-1702`).
   - `00266D10` then zero-fills `scratch1` (`02099DF0`) and `scratch2` (`02099FF0`) after the call (`SPR:1688-1691`).
   - **Not stated:** whether the ledger reset runs before or after the rotation inside `002342F0`. Both are named; their order is not given.
2. **Zone script `setup` / `battle()`.**
   - `btlAtelSetupActorStart` first, then optional overrides (`HT:383-392`, `HT:674-675`).
   - Per spawn group: the entry preamble `btlAtelSetUnit … SetLevel, SetEventFlagGroup …` registers each member (`GC:354`).
   - `btlAtelSetEntryStruct` initialises keep entries (`FM:129-134`).
   - The continuous and previous-map selectors, or `btlAtelCanselInitialSpawnFlag` on the fresh branch (`HT:268-276`).
3. **Placement, on script demand.**
   - Verb `0x301A` → `00235720` → `00234AF0` × attempts. The result is written to keep `+0x50`/`+0x60`; unit flag bit 26 is set (`SPR:288-316`).
   - The actor is created later, at activation: `00233AD0` (bit 49, `00239E10`), then `btlAtelSetUnitFinish` → `0023A410` (probe, publish) (`HT:632-639`; `SPR:701-705`).
4. **Each unit frame.**
   - `00233F70`, through the actor record's `+0x38` callback, runs the retire check `002350C0` and `003070E0` (`SPR:696`; `GC:568-571`).
5. **Each field frame.**
   - `00234590` → `00307030`, when the gate `00233D20` is open (`C-GC:236-238`).
   - **Not stated:** the order of steps 4 and 5 within one frame.
6. **Death.**
   - `00300530`, lethal branch → keep stats → `00306F00`. Completion runs the lock, then mode 1 posts the flag at once; any other mode posts it when the track-end dispatch reaches `003250F0` (`C-GC:222-234`).
   - The body is torn down in the per-unit idle path once bits 33 and 34 are set; the slot is freed later, at actor-record release (`GC:617-653`).
7. **Save and load.**
   - Capture: `00584580` / `00229B40` (`SPR:1614-1637`).
   - Restore: load-controller message 18 → `005843E0` → A, B or neither (`SPR:1583-1601`, `SPR:2577-2596`).
   - The ordering between load completion and the next area init's rotation is L-13's live residue (`SPR:781-786`).

### 1.5 Dependencies (on other systems)

| system | what this one needs from it | cite |
|---|---|---|
| Script VM (01) | verb dispatch, pop order (LIFO, `00267DB0`), `waitv`, `scratch1` | `HT:589-596`; `C-GC:294-305` |
| Party (11) | `BattleUnit_GetPartyLeader` `003272A0`; `PartyFocus_*` `003590D0` / `003273B0` | `C-SP:294-301` |
| ActorEntity (04) | `0031B810` slot resolver; `Actor_GetWorldPosition` `00265020`; `00265200` class-dependent heading; unit definition; teardown | `SPR:486-497`; `SPR:889` |
| World / field data (03) | `003148F0` field id, from save payload `+0x1044`; the format-0 records; `FieldRegion_ContainsWorldPosition`; the bit-15 escape `00377C20` | `SPR:914-919`; `SPR:818-826` |
| Movement (06) | `0026E3C0` cell-dataset height query; `00300310` publish; sine table `01F004E0` | `HT:723-736`; `C-SP:116-120` |
| RNG (21) | `00328370` shared LCG, three steps per call | `C-SP:324-327` |
| CombatFormula (08) and Status (10) | HP write `00300530`; terminal statuses `0x80000003` = KO, Stone, X-Zone | `SPR:818-826` |
| Presentation (17) | events `0x2005` / `0x2008` into the animation layer; handler table `02CA4410` | `GC:502-507`; `C-GC:570-584` |
| Input / capability (15) | row 12 inhibitions; `0209A2C4[2]` | `GC:779-807` |
| Save / Load (19) and UI (16) | capture and restore paths; load-controller messages | `SPR:1560-3540` |
| Core clock | `0032A150` reads `0208D45C`; scale `01DFE0B8` (1.0 or 2.0) × `30.0f` (`008F8D80`) | `GC:98-114` |

---

## 2. Gaps

### 2.1 Open or partly open items the pages themselves list

1. **L-12, the area-path acceptance word.**
   - Area mode never writes `out_observed`, yet the caller reads it, so one stack word decides the whole call (`SPR:1502-1510`).
   - "What that word actually holds in ordinary play — still live-only" (`SPR:1513-1514`); the register row is SUPERSEDED, not answered (`SPR:760`).
   - The contract restates it as "*Not established:* which values the slot holds in ordinary play. That is `L-12`'s live question" (`C-SP:104`, `C-SP:211-213`).
2. **L-13, live residue.**
   - "a slot-0 field-transition autosave load with non-zero keep banks, and whether the requeued area init's rotation then brings the same enemies back" (`SPR:781-783`).
   - "still without a carrier" (`SPR:786`). WHY keeps it too: "what the session values are in practice … are live questions" (`WHY:110-112`).
3. **The area-mode Y in practice.**
   - For 895 of 954 definitions the probe bit is clear, so the placed Y is "whatever `[rsp+0x54]` held … stays open" (`HT:722`).
   - The contract's parity plan says not to assert it (`C-SP:229-231`).
4. **The modded attempt skip.** "Whether the modded skip is reachable unmodified" (`C-SP:214`). There is no live evidence for placement at all: EXP-145 ran on planted fixtures (`C-SP:215-216`).
5. **No live capture of completion.**
   - "Live capture of the completion transition: still absent" (`C-GC:483-485`); EXP-019 stopped before a kill (`C-GC:497-498`).
   - `INTEGRATION` and `PRESENTATION` need the running game (`C-GC:673-675`).
6. **`waitv` width selector.** Widths above 5 return "stop waiting" at once; "which widths the group-number import actually uses … is recorded, not attributed" (`C-GC:314-317`).
7. **EE-8 residue.**
   - Row 12 bits 7, 11, 12 and 20 reach no direct test (`GC:788-790`).
   - `02089340` bit `0x2` "has no direct test on any enumerated route … residue" (`GC:805-807`).
8. **Body release.**
   - "which tracks carry these entries … and whether any other code sets bit 34" (`GC:639-640`).
   - "Which presentation that handle names, and what the states mean, is not claimed" (`GC:648-649`).
9. **The window's purpose and the clock.** "what the 64 `u16` entries mean beyond being reset to `1`, what `0032A150` returns as a clock, or **why the window exists**" (`WHY:180-183`).
10. **Threading.** "the ledger is a bare global array with no lock … **single-threaded use is assumed, not proven**" (`C-GC:323-325`).
11. **Bits 45/49 and bulk zeroing.** "**Not closed for bulk zeroing** — 387 sixteen-byte zero stores at displacement 0 exist and cannot be attributed to a BattleUnit statically" (`HT:882`).
12. **Unread accessors and unexplained bytes.**
   - "`00236030` and `00236670` — were not read here" for the prologue shape (`GC:965-966`).
   - "What the untouched bytes and `+0x74` are for | **not established**" (`FM:328`).
13. **Unaudited parts of HT.**
   - §11 did not attack §2a/§2b, the §2e census, §4's formulas or `002D81D0` (`HT:1032-1041`).
   - §12 lists §2a-§2c, §2f, §3-§5 and "the `167 zone scripts` count in §1" as not examined (`HT:1128-1132`).
14. **Guard and metadata side effects.**
   - "Which of the guard's callees run on every call, and which only on the null path, is not read here" (`WHY:224-225`).
   - The metadata wrappers' "downstream effects are not established here" (`SPR:1607-1609`); their consumer is left to another page (`SPR:1609-1612`).

### 2.2 Structural gaps: what a port needs and no page states

**G1. The clock's source and rate.**
- Every respawn and return-window computation divides `*(u32*)0208D45C` by `(int)(scale × 30.0f)` (`GC:107-110`; `SPR:356-359`).
- The only statement about who advances it is "advanced by `0032A100`" (`WHY:94`).
- HT says "What advances the counter is not restated here" (`HT:1138-1139`); WHY lists "what `0032A150` returns as a clock" as unclaimed (`WHY:181`).
- **The per-frame-or-per-tick rate is not stated, and the pages disagree on it (A9).** A port cannot reproduce the seconds conversion without it.

**G2. Field-data record formats for placement and mode-2 retirement.**
- The format-class-0 candidate record is given only as "byte `+0x00` selects the mode, `+0x10` carries the authored position" (`C-SP:55-56`).
- Not stated:
  - the record's size, and what `003209C0` copies (`SPR:491`, "field-record copy wrapper, class 0");
  - the region shapes beyond "`1` box, `2` ellipsoid" (`C-SP:190`);
  - the containment formula of `FieldRegion_ContainsWorldPosition` `002374E0`. The page states only that it is XZ-only and calls `00325EA0` (`HT:115-120`, `HT:1180-1182`);
  - the record read by `FieldData_GetFormat0RecordVectorByIndex` `00320940` for mode 2 (`SPR:266`, `SPR:490`).
- Area mode cannot be written without the region test.

**G3. Where the candidate index comes from, and which lane wins.**
- The selector is written as "for each lane 1 .. laneCount-1 … for each candidate in the lane … `Spawn_TrySelectCandidatePosition(candId, …)` … `remember this lane and position`" (`SPR:294-309`).
- Not stated:
  - how `candId` is derived from a lane, and how many candidates a lane has;
  - why the loop starts at 1, when the accessor prologue accepts lane 0 (`GC:68-70`);
  - which lane is returned when several qualify (first, last, or another rule).

**G4. The unit-side retirement fields.**
- `bLifecycleMode` (0 off, 1 range, 2 authored point), `bLifecyclePointId` and `flLifecyclePointThreshold` are named with no offsets (`SPR:530-535`); the interior cite reads the threshold at `[rsi+0x4C]` (`SPR:1377`).
- Their writers are not stated.
- The per-actor opt-in bit `actorWork +0x0D` bit 6 is read through `FUN_002672F0` (`SPR:543`, `SPR:641`); its writer is not stated.
- See also A8.

**G5. Two of the four selectors are not described.**
- `Spawn_SelectPreviousMapEntry` `002354F0` (166 B) and `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0` (376 B) are listed with sizes and a few field sites (`FM:101-102`, `FM:117`, `FM:173`; `HT:473-474`).
- Their logic, callers (other than the pass-22 edge `00510230`, `FM:406`) and return values are not stated.
- The zone scripts call the previous-map verb on every restorable branch (`HT:268-272`).

**G6. Creating the actor for a chosen entry.**
- "automatic selection does not create the actor — it writes the keep entry's position … and activation places the unit later" (`SPR:701-705`).
- The native effect of the verbs that bind and create the unit is not described in this folder: `btlAtelSetUnit`, `btlAtelSetKeepWorkGroup`, `setentrygroup`, `requestreentry` (`HT:270-272`; `GC:354`).
- The installer `BattleUnit_ApplyUnitDefinition` is deferred to 04-Actor-Entity (`FM:51`, `FM:221`).

**G7. Teardown.**
- `BattleUnit_TeardownAndDespawn` `00300E40` is called by the retire action with argument 1 (`SPR:275`). Its body is not described.
- Stated pieces:
  - mode bit 1 of `+0xE99` skips `0025AB30` and `002697E0` (`GC:342-345`, `GC:818-830`);
  - mode 0 calls `00237080`, "per `X55_NATIVE_REPLAY_CONTRACT.md`", a research import (`FM:163`).

**G8. Enmity decay.** The table lives at keep `+0x19..+0x41` (`SPR:412-423`). The decay rule of `BattleEnmity_UpdatePeriodicDecay` is deferred to 09 (`SPR:423`) and is not stated here.

**G9. The spawn-history counters.**
- `0208D354 + parity × 0x80` (u16[64]) is filled with 1 on a wipe (`WHY:76-78`).
- Keep `+0x12` holds "the pre-increment counter of the row's byte `+2` at a fresh spawn" (`FM:92`).
- The reader of the `0208D354` arrays, and how they tie to `+0x12`, are not stated: "a correspondence this page has not traced" (`WHY:77-78`).

**G10. The RNG's exact step.**
- Stated: the multiplier `0x41C64E6D`, three steps per call, at most 31 bits, "(11+10+10 selected bits)" (`C-SP:324-326`; `SPR:1518-1519`).
- Not stated in this folder: the increment, and which bits are selected.
- Area placement and the `002395A0` rolls both draw from it, so draw-exact parity needs those details.

**G11. Angle and heading helpers.**
- `00316DA0` "wraps an angle" (`C-SP:132`; `SPR:154`); its formula is not stated. `0031A930` is (`HT:1161-1166`).
- `FUN_00265200`'s "class-dependent heading read" is deferred to 06 (`SPR:141`, `SPR:1136`).

**G12. Order within a frame and within area init.**
- Not stated: the order of the unit pass `00233F70` (retire check, `003070E0`) and the field pass `00234590` (`00307030`) in one frame.
- Not stated: the order of the ledger reset `00307090` and the rotation `00233780`, both inside `002342F0` (`GC:215-216`; `SPR:1650-1653`).

**G13. Group ids above the ledger.**
- `+0xE98` is a u8 stored raw (`C-GC:561-562`), and the ledger index is `(group − 1) × 24` over 64 entries (`C-GC:140`).
- No bounds check is stated for groups 65–255.
- The group-mask operations use `1 << (groupId & 31)` (`SPR:452`), so groups 32 and up alias. The pages do not reconcile 64 ledger groups with a 32-bit mask.

**G14. The ground probe's dataset.**
- `0026E3C0` is described as a walk: cell → height → kind-6 escape → segment (`HT:723-736`). The callees `00231900`, `00231890`, `00232490`, `0022F830` and `00230B60`, and the cell dataset format, are not described here.
- Only `00233050`'s cell linearisation is given (`HT:1167-1178`).

**G15. Timing of the deferred completion arm.**
- `003250F0` runs "whenever a track ends on a unit whose guard passes (`[rcx+0x0D]&1` clear, `[rcx+0x30]` non-null)" (`C-GC:582-583`).
- Not stated: when the death track ends, and what happens to bit 47 and the group when the guard fails.

**G16. The rest of the spawn verb surface.**
- Native effects are not stated for verbs that appear only as script text:
  - `btlAtelSetCallGroup`, `btlAtelSetUnitType`, `btlAtelSetBelong`, `btlAtelSetHpLowLimit`, `btlAtelSetDefaultLogic`, `btlAtelSetDirection` (`GC:354`);
  - `btlAtelGetRespawnCause` (`GC:739`);
  - `btlAtelGetDeadCountNow` (`C-GC:394-395`). This one is presumably `00235F50`, but no page names it as such.
- FM's verb list (`FM:210-220`) and HT's table of ten (`HT:327-338`) are the only native mappings.

**Fields written by documented functions but left unexplained.**

| field | cite |
|---|---|
| keep `+0x74` (written at release, never read) | `FM:104`, `FM:296-311` |
| `0208935C` = 5.0, never read | `SPR:106-107` |
| unit flag bit 40 (set by `0023A200`) | `FM:168` |
| unit lane byte `+0x57` | `FM:164` |
| unit `+0x58` category mode and its table `01E09EE8` | `FM:167` |
| `02089344` bit 0 (`00238A30`, also script thunk `0050F5A0`) | `SPR:3567` |
| state `+5B04` bit 1, cleared on restore | `SPR:1595-1596` |
| height-mode values 1, 2, 5, 6, 12, which nothing reads | `HT:714-716` |
| ledger `flags` bits 1–7, never written or read | `GC:245-248` |

### 2.3 CONTRADICTIONS

These are statements a re-implementer would have to choose between. Each item quotes both sides exactly, with `ABBR:line`.

- **A** is value-changing: an offset, address, constant, formula, signedness, control flow or order that a port would hard-code.
  Every A item is **page-text only - needs local check**: this session cannot see the executable.
- **B** is a count or size that disagrees but does not change ported behaviour. These are also page-text only.
- **C** is a stale "open / not read" claim that a later dated section answers, a status banner that disagrees with front matter, or a corrected name still in use.

A favoured side is named **only** where a dated correction on the pages settles it. Otherwise the item says "not settled on the pages".

#### A. Value-changing

**A1. The dead-mask bit: 64-bit shift, or sign-extended 32-bit shift.**
- GC §5 pseudocode: "`L->deadMask |= (1ull << lane);`" (`GC:393`).
- C-GC §12: "`bit = (int64_t)(int32_t)(1u << (slot & 31));            /* same in BOTH writers */`" and "`L->deadMask |= bit;   /* CORRECTED, see below */`" (`C-GC:437`, `C-GC:440`). The correction box "The dead-mask bit is a 32-bit shift, sign-extended — corrected 2026-09-08" gives slot 31 → `0xFFFFFFFF80000000` and 32–63 aliasing onto `v & 31` (`C-GC:453-479`).
- GC's own §4 agrees with the contract for the register path: "**The bit is the same sign-extended 32-bit shift the death handler uses**" (`GC:299-301`). Only the §5 pseudocode keeps `1ull << lane`.
- **Favoured: C-GC**, by the dated correction of 2026-09-08. *Page-text only - needs local check.*

**A2. The field-table element: `u16` or signed `i16`.**
- C-GC §2: "`((~~u16~~ **i16***)*(02098E68))[index] = value` … **CORRECTED 2026-09-11 (OPUS-REQ-FABLE-OPERAND):** the element is **signed**: the consumer `AiTargetSelector_ResolveOperandValue` (`00321190`) sign-extends every kind-1 / 2 / 3 element (`movsx ecx, ax` at `003211C2` …)" (`C-GC:84`).
- Still `u16`, unstruck:
  - GC: "`0026ADC0(index, value)` stores `value` as a `u16`" (`GC:469`);
  - GC: "`table[index] = (u16)value`" (`GC:677`);
  - GC: "pointer to a 64-entry `u16` table" (`GC:692`);
  - C-GC: "`u16` slot 3 of the table" (`C-GC:207`, `C-GC:289`);
  - C-GC's reproduction formula: "`(*(u16**)0x02098E68)[index] = value`" (`C-GC:449`).
- GC also says the getter `00264D20` reads it with "`movzx` of the same table at `00264D3D`" (`GC:476-477`). C-GC's correction says the consumer sign-extends at `003211C2`. These may be two different instructions in one chain (a zero-extending getter, then a sign-extending consumer); the pages do not reconcile them.
- **Favoured for the element type: signed (C-GC:84, dated 2026-09-11).** Whether `00264D20` itself zero-extends is not settled. *Page-text only - needs local check.*

**A3. The continuous-entry match predicate.**
- FM's row for `+0x17`: "committed (bit 1) **and** range-reentry-pending **or** released (bits 0 / 2 — `test r8b, 5` skips only when *both* are clear, `00235419`–`0023541D`; this row first read it as "neither", corrected 2026-09-11)" (`FM:96`).
- SPR L-11 agrees: "`ACTIVATION_COMMITTED` **and** `RANGE_REENTRY_PENDING` **or** `released`" (`SPR:846-847`).
- FM §4 keeps the pre-correction "neither" reading: "**The continuous-entry match**: `history[j].flags & 2 && !(history[j].flags & 5) && history[j].b_17 == live.b_17`" (`FM:204`).
- **Favoured: `(flags & 2) && (flags & 5)`, the dated correction of 2026-09-11 at FM:96.** *Page-text only - needs local check.*

**A4. Who clears keep-flag bits 0, 2 and 7.**
- FM §2.3, bit 7: "`0030FED0` does not clear it — nothing found does" (`FM:123`).
- FM §2.3 also lists only `0023A410` and `00239840` as clearers of bit 0 and bit 2 (`FM:116`, `FM:118`).
- FM §3, same page:
  - `0023A2E0` "for every fresh entry clears bits 0 / 2 / 7" (`FM:161`);
  - `00236860` does "the same clears for one entry" (`FM:162`);
  - `00237080`: "flags `& 0xFFFFFF7A` (bits 0 / 2 / 7) … body re-read 2026-09-15" (`FM:163`).
- **Partly settled:** the 2026-09-15 re-read settles that `00237080` clears bits 0, 2 and 7. Nothing dated settles `0023A2E0` or `00236860`. The §2.3 table was not updated. *Page-text only - needs local check.*

**A5. Keep-entry offsets in SPR §4 against FM.**
- SPR §4 diagram: "`+0x14.. bEnmityTableHeader + aEnmityByCombatantId[0x2E]`" (`SPR:533`).
- SPR §8f: "The per-entry field offsets in §4 stand" (`SPR:1109-1110`).
- Other side:
  - FM: `+0x14` is "`bStealAvailabilityFlags`", `+0x19` is the decay timer and `+0x1A`–`+0x41` is `aEnmityByCombatantId` (`FM:93`, `FM:98-99`);
  - SPR's own §2: "`BKEI + 0x19` is the decay timer and `BKEI + 0x1A + id` … ending at `+0x41`" (`SPR:418-419`);
  - SPR §8e: "the struct annotation had implied `0x2E` bytes of enmity alone" (`SPR:1057-1059`).
- **Favoured: FM.** SPR §8g (2026-09-12): "[The keep-entry field map] is the authority for offsets" (`SPR:1126`). *Page-text only - needs local check.*

**A6. What `0208E6A0` is.**
- FM: "`0208E690` … the live bank (`btlKeepCharWork1`); `0208E698` the history bank; `0208E6A0` the bank flag" (`FM:159`).
- SPR: "`0208E6A0  i32  g_nBattleUnitSlotCount               32; BattleUnit stride 0xF50`" (`SPR:516`); "All five iterate the battle-unit slot pool (`g_nBattleUnitSlotCount`, `32`)" (`SPR:441`).
- C-GC: "`0208E688`/`0208E6A0` (unit array and count, in `00238B70`)" (`C-GC:206`).
- GC: "for every battle-unit slot `i < [0208E6A0]` in the array at `[0208E688]`" (`GC:580`).
- Not settled on the pages. Three pages against one. *Page-text only - needs local check.*

**A7. Which argument of `00234DA0` is the slot flag: the fifth or the sixth.**
- C-SP P0: "`slotFlag` is `[rbp + 0x7f]`, passed on as the validator's fifth argument" (`C-SP:316`).
- SPR gives a five-parameter signature whose last is `int include_all_party_slots` (`SPR:184-186`).
- C-SP P4, the same pass: "Its sixth argument decides eligibility. With 0, only the slot whose actor handle equals `PartyFocus_GetCurrentPackedActorHandle` …" (`C-SP:297-298`).
- Not settled on the pages. Both sides date from 2026-09-29. *Page-text only - needs local check.*

**A8. Where the mode-2 retire threshold lives: keep `+0x04`, or a unit field at `+0x4C`.**
- FM: "`+0x04` | f32 | `flLifecyclePointThreshold` (placement page) ✓", written by `0023A200`, and read **only** by `00308040` (`FM:87`).
- SPR mode 2: "`unit->flLifecyclePointThreshold ^ 2)) retire; // COMISS/JBE`" (`SPR:268`).
- SPR interior table: "mode 2's per-unit squared threshold | `0023519C` — `movss xmm6, [rsi+0x4C]`" (`SPR:1377`). Neither page says what `rsi` is.
- FM does not list `002350C0` among the readers of `+0x04`. Not settled on the pages. *Page-text only - needs local check.*

**A9. The rate of `0208D45C`: a frame counter or a 30 Hz tick.**
- C-GC: "the raw frame counter | `0032A150` (7 B)" (`C-GC:53`).
- GC: "The game divides its frame counter by the current frame rate" (`GC:46`); "`0x0208D45C` | the raw frame counter" (`GC:689`).
- WHY: "`01DFE0B8 × 30.0` is ticks per second — 30 at 30 fps, 60 at 60 fps" (`WHY:62`).
- C-GC §10: "`00235FFA  call 0x32A150                ; the 30 Hz tick counter at 0208D45C`" (`C-GC:399`), with "`ecx = 30`" (`C-GC:402`).
- These are incompatible at 60 fps. A 30 Hz counter divided by 60 gives half-seconds. Not settled on the pages; nothing names the advance rate (G1). *Page-text only - needs local check.*

**A10. Does the return window survive a save and load.**
- SPR §8b (2026-09-02): "`g_wSpawnKeepPreviousFieldId` and `g_wSpawnKeepMostRecentFieldId`, are themselves **written into and restored from the persistence buffer** by `00233440` / `00233550`. The return window therefore survives a save/load in both directions." (`SPR:922-925`).
- SPR §2: "neither helper serialises/restores the transition tick or window setting" (`SPR:388-389`).
- WHY (2026-09-13): `00233550` "does not touch bank 1, the tick stamp `02089374` or the window" (`WHY:143-144`); the stamp is "**never restored**" (`WHY:93`).
- **Favoured: tick and window not restored.** That is ASTRA's 2026-09-12 falsification (§11, `SPR:1440`) and WHY's 2026-09-13 correction. *Page-text only - needs local check.*

**A11. Does native code compare the cooldown with the elapsed seconds.**
- C-GC §6 diagram: "`-> the three record accessors                     [THE ONLY READERS]`" (`C-GC:245`).
- C-GC §10: "**Nothing native relates the two values** … **The comparison is made in authored script or not at all**" (`C-GC:385-388`).
- GC EE-1: "compared strictly … and by script, not native code" (`GC:739`).
- C-GC correction (2026-09-29): "the automatic spawn selector … reads the fields **directly** … it skips while `seconds − stamp (+0x0C) < cooldown (+0x10)` … So the native gate re-admits an entry at **elapsed ≥ cooldown**, while the scripts' own checks use `>`" (`C-GC:103-109`). This agrees with SPR's pseudocode "`seconds - bkei->dwLastDeathTick >= bkei->wRespawnCooldownTicks`" (`SPR:300`, `SPR:626`) and FM's reader lists (`FM:88-91`).
- **Favoured: native `>=` in `00235720`, plus script `>`. Dated 2026-09-29.** *Page-text only - needs local check.*

**A12. Does a mode-≠1 group ever post its completion.**
- GC box: "**So the static reading of arm B is: bit 47 is set, `0x2008` is played, and nothing observed clears bit 47 or raises the ledger flag.** Only mode-1 groups post their completion to slot 3." (`GC:509-510`).
- GC EE-12, unstruck tail: "No static route of any enumerated form reaches them; if they are dead, mode ≠ 1 groups never post their completion." (`GC:835-836`).
- C-GC §7 diagram: "`00307110 runs -- its sole caller 003250F0 has NO static route (section 10)`" (`C-GC:259-260`).
- C-GC §10 (refuted 2026-09-19/22): "`003250F0` **does run** … A mode ≠ 1 completion sets unit bit 47, plays `0x2008`, and the ledger flag posts when the track-end dispatch reaches `003250F0` → `00307110`." (`C-GC:343-351`). Also C-GC §14 item 9: "**So the deferred arm can post**" (`C-GC:582`).
- **Favoured: it posts.** EE-12 was answered 2026-09-19 and re-verified 2026-09-22. *Page-text only - needs local check.*

**A13. The accessor failure sentinel.**
- C-GC: "**`-1` is "no such lane", never a value.** All three readers share a seven-check prologue (§4) and every failure returns `-1`" (`C-GC:89-90`).
- C-GC: "**Every accessor failure is `-1`**" (`C-GC:329`).
- C-GC: "seven checks, identical in nine accessors" (`C-GC:164`).
- GC (corrected 2026-09-13): "~~Every one of the nine returns **`-1`**~~ **Corrected 2026-09-13: `SpawnEntry_GetScriptSelection` (`00236140`) returns `-2`, and `-2` *is* inside its value range**" (`GC:78`; detail `GC:934-952`).
- **Favoured: `00236140` returns −2 (GC, 2026-09-13).** C-GC:89 is scoped to the three respawn readers and stays true. C-GC:329's "Every accessor" does not. *Page-text only - needs local check.*

**A14. How many ledger entries exist.**
- C-GC §4a: "The index is `group − 1` with a `0x18` stride, so entries exist for groups 1–5 and there is no slot a 0 could address" (`C-GC:75`).
- C-GC §3: "`0x02EC13C0 + (group - 1) * 24               BSS, 64 entries, 1,536 bytes`" (`C-GC:140`).
- GC: "base 0x02EC13C0 · walked to 0x02EC19C0 · 1,536 bytes / 24 = exactly 64 groups" (`GC:193`); modding note "`group` 1–64" (`GC:721-722`).
- Not settled on the pages. "1–5" is the range authored in the corpus (`C-GC:59`); the 64 comes from the reset loop's bounds (`C-GC:591`). *Page-text only - needs local check.*

**A15. Does `00235AF0` copy when the transition record matches, or when it differs.**
- SPR subtree note: "each `dword`/`word` of `qword[02EBF190]` is compared against it (`00235B19`/`00235B1E` …), `002EF4A0` copies the matched row (`00235B76`)" (`SPR:3680-3682`).
- SPR §27: "All four equal means no preparation. **Any difference calls`002EF4A0`**, then rebuilds records." (`SPR:3350-3351`).
- Not settled on the pages. The subtree note's 2026-09-30 correction changes only `002EF4A0`'s size (`SPR:3687`). *Page-text only - needs local check.*

**A16. What the guard `00233C10` does around `00237DF0`.**
- WHY: "`002EF640` snapshots the block (`00233C25`) and stores back `02EBF190` (`00233C33`) … then the `00237DF0` reset branches (`00233C48`/`00233C59` — the null-path first-bind)" (`WHY:241-244`).
- WHY table: "`BattleSystem_ResetRuntimeState` `00237DF0` runs only on its null path (first bind, e.g. at boot) or when the battle-state block's stamp mismatches" (`WHY:97-98`).
- SPR §22.4: "Its null-pointer branch calls `002EF640`, adds`0x4E68C`, and stores the result in`02EBF190`: **this local code binds into the active image; it does not directly allocate a fresh block** … calls`00237DF0` at`00233C3F` and tail-calls it again at`00233C48` if the first call returns. A nonnull stamp mismatch takes only the tail at`00233C59`." (`SPR:2651-2655`).
- SPR §27: "a null`B` makes`00233C10` bind the active image and call then tail-call`00237DF0`" (`SPR:3407-3409`).
- So: is `00233C59` part of the null path (WHY) or the mismatch path (SPR), and does the null path run the reset twice? Not settled on the pages. *Page-text only - needs local check.*

**A17. The engine call site for handler id `0xC`.**
- C-GC: "`call rax` on `[02CA4470]` (id 0xC) at `0041DC84`/`0041DD03`/`0041CEC6`" (`C-GC:364`; the same address at `C-GC:579`).
- GC EE-12: "slot `02CA4470` is called by the engine when a track ends or is switched (`0041DC84`, `0041DD03`, `0041CEC0`)" (`GC:835`).
- Not settled on the pages. *Page-text only - needs local check.*

**A18. The height-mode value for a unit that is not spawn-backed.**
- HT §2c: "`00239FA7  mov   ecx, esi   ; NOT spawn-backed -> esi (1, 2 or 3)`" (`HT:189`).
- HT §2c prose: "whose values are 1, 2 and 3" (`HT:212-213`).
- HT §4: "`mode = esi;   // 1, 2 or 3 - never 8`" (`HT:563`).
- HT §7, answered 2026-09-12: "a party unit gets **1**" (`HT:712`).
- Not settled on the pages: the 2026-09-12 answer does not say it corrects §2c. Only bit 3 is ever read (`HT:714-716`), so the difference changes no reader. *Page-text only - needs local check.*

#### B. Counts and sizes that disagree

**B1. The `0x250`-stride census.**
- HT §11 (2026-09-03): "`stride    'imul reg, reg, 0x250' -> 50 sites`" (`HT:971`); "**18 of its 50 sites inside one function**, `0043F450`" (`HT:1007`).
- HT §12 (2026-09-07): "Image-wide, `imul r, r, 0x250` appears in **18 functions across 27 sites** — a UI function once and a Presentation function ten times" (`HT:1123-1125`).
- 50 sites against 27, and 18 sites against 10 in the Presentation function. Not settled on the pages. *Page-text only.*

**B2. Function sizes.**
- `00307140`: "`00307140` (183 B)" (`C-GC:85`; also `GC:579`, `GC:674`) against "`00307140` (~97 B)" (`C-GC:739`).
- `00312EE0`: "`00312EE0` | 187 B" (`FM:175`) against "`00312EE0` (~208 B)" (`FM:512`).
- Not settled on the pages. *Page-text only.*

**B3. The member TSV against the ledger census.**
- GC: "addressed by exactly six functions" (`GC:687`). Six `lea` sites are listed (`GC:233-234`), and four flag-byte sites outside the reset (`GC:239-242`).
- `spawn-group-ledger-accesses.tsv` has 19 rows in three functions (`00306E60`, `00306F00`, `00307090`). It has no row for `00307030`, `003070E0` or `00307110`, nor for the flag set at `00306FE0`.
- No page says the TSV is register-route only. Its `route` column reads `array 02EC13C0 reg`. *TSV and page text only.*

**B4. Corpus counts from the 828-file population, still stated beside the 1,114-file recount.**

| statement (828-file population) | whole-corpus figure from HT's table |
|---|---|
| "**167 zone scripts use it.**" (`HT:66`) | `btlAtelCanselInitialSpawnFlag`: 253 (`HT:362`) |
| "167 zone scripts set their own active-actor cap" (`HT:79`) | 234 (`HT:363`) |
| "146 of the 406 spawn-capable zones" (`HT:433-434`) | 210 of 515 |
| "Every one of the 406 shipped scripts that calls it" (`HT:674-675`) | 515 (`HT:358`) |
| "as the 167 shipped zones that care already do" (`HT:680-681`) | 253 |
| "the 368 zones that do not override, and none of the 38 that do" (`HT:700-701`) | 70 override `btlAtelSetSpawnDistance` (`HT:365`) |
| SPR L-10: "Across the 828 decompiled US scripts, 406 call it" (`SPR:835-836`) | 515 |

- **Favoured for whole-corpus statements: the 1,114-file figures**, from the re-carve dated 2026-09-12 (`HT:352-354`). The 828-file figures remain true of that subset. *Page-text only.*

**B5. How many accessors carry the unreachable `js` arm.**
- "It appears in **all nine** accessors — one template, copied" (`GC:84-86`; `C-GC:177-178`).
- GC's falsification pass: "that exact three-instruction shape appears in **seven**" (`GC:960-961`), with two accessors unread (`GC:965-966`).
- Not settled on the pages.

#### C. Stale "open / not read" claims, banners and names

| # | stale or banner side | the side that answers or disagrees | favoured by a dated correction? |
|---|---|---|---|
| C1 | README: "`spawn-placement-and-retirement.md` — **PARTIAL.**" (`README:13`) | SPR front matter: "`status: DOCUMENTED — owner re-status 2026-10-01`" (`SPR:4`) | yes, SPR:4 (2026-10-01) |
| C2 | README: field map "**DOCUMENTED, tier 1.**" (`README:21`) | FM front matter: "`status: AUDITED`" (`FM:4`) | no date settles it |
| C3 | README lists 2 system pages (`README:11-24`) | the folder has 7 `.md` system or contract pages; WHY, HT, GC and both contracts are not indexed | — |
| C4 | SPR body: "**Status raised from `PARTIAL` to `DOCUMENTED` on 2026-09-02.**" (`SPR:32`) | reconciled on the page: "that raise is history … the current status is the front-matter line" (`SPR:36-37`) | yes (2026-09-30), already annotated |
| C5 | SPR §11: "`crossref_clean` is now false because this amended citation surface has not had a fresh graph audit" (`SPR:1555-1557`) | front matter `crossref_clean: true` (`SPR:23`), and "a fresh graph audit of this page reports 0 findings" (`SPR:4`, 2026-10-01) | yes, front matter (2026-10-01) |
| C6 | front matter `last_pass_state`: "consumer propagation and remaining caller questions open (§11)" (`SPR:22`) | the status line closes L-12 and L-13 (`SPR:4`) and §7 reconciles them (`SPR:760-786`) | yes (2026-09-30 / 10-01) |
| C7 | HT §10: "`status` is `DOCUMENTED`, `audit.passes` is `0`" (`HT:872-873`) | HT front matter: `status: AUDITED` (`HT:4`), `passes: 1` (`HT:20`) | no date on the §10 sentence; front matter later by §11/§12 |
| C8 | SPR §2: "What supplies the vertical coordinate is recorded as **L-7**." (`SPR:175-176`) | SPR §7: "~~**L-7.**~~ **ANSWERED — nothing does, at generation** … supplied later, at activation, by a terrain probe" (`SPR:812-817`) | yes (HT, 2026-09-02) |
| C9 | WHY: L-13 "is the open question `L-13` on the retirement page, and nothing here closes it" (`WHY:145-146`); "`L-13` keeps bank 1 and the timer" (`WHY:176`) | SPR §7: L-13 "SUPERSEDED 2026-09-27"; the static question is answered (`SPR:765`, `SPR:775-781`) | yes (2026-09-27) |
| C10 | SPR §§11-29: closing lines saying L-12/L-13 "remains open", e.g. `SPR:1469`, `SPR:1656`, `SPR:1812`, `SPR:1876-1879`, `SPR:1987-1990`, `SPR:2091-2094`, `SPR:2171-2176`, `SPR:2321-2324`, `SPR:2434-2436`, `SPR:2533-2535`, `SPR:2683-2686`, `SPR:2801-2803`, `SPR:3166-3167`, `SPR:3315-3316`, `SPR:3445-3446`, `SPR:3488`, `SPR:3537-3540` | each annotated "*Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7*", and the reading note at `SPR:1562-1571`. The text is annotated, not struck | yes (2026-09-30) |
| C11 | C-GC §8: "no decompiled script has confirmed it (`EE-11`)" (`C-GC:285-286`) | C-GC §4a: "the order and placement are **observed** rather than inferred" (`C-GC:59`); §14 item 8: "**OBSERVED, not inferred, 2026-09-13**" (`C-GC:569`) | yes (2026-09-13) |
| C12 | evidence rows: "pop-order law only; no decompiled script \| 2 (static) \| PROBABLE" (`C-GC:610`); "no decompiled script seen \| 2 \| PROBABLE" (`GC:901`) | `C-GC:569`; GC: "**ANSWERED 2026-09-13 (FABLE), observed in the shipped scripts**" (`GC:831-834`) | yes (2026-09-13) |
| C13 | GC box under the heading "~~inferred, not observed~~ observed 2026-09-13" still reads "No shipped script has been decompiled to confirm it" (`GC:347`, `GC:350-352`) | the next paragraph: "**`EE-11` answered 2026-09-13 (FABLE),** **observed in the shipped scripts.**" (`GC:354`) | yes (2026-09-13) |
| C14 | GC §9: "Whether `+0x10` is seconds \| **not established** \| — \| UNKNOWN" (`GC:886`); GC §3: "whether its unit is seconds is **unverified**. `EE-1`." (`GC:126-127`, annotated but not struck) | GC §8: "**`EE-1` ANSWERED 2026-09-13 (FABLE):** **yes**" (`GC:738-739`); C-GC §14 item 3 (`C-GC:525`) | yes (2026-09-13) |
| C15 | GC §9: "`003250F0`, `00325090`, `00325260` have no static route \| … \| PROVEN (as a negative over the listed routes)" (`GC:896`) | C-GC §15 row struck as "**REFUTED 2026-09-16**" and re-verified 2026-09-22 (`C-GC:607`); GC EE-12 answered (`GC:835`) | yes (2026-09-16/19/22) |
| C16 | GC §9: "What the row-12 bits and slot 3's reader are \| **not established** \| UNKNOWN" (`GC:902`); GC §5: "which script or operand reads slot 3 is `EE-9`" (`GC:477`) | EE-8: "**ANSWERED 2026-09-12 (FABLE), with two bits left as residue**" (`GC:779-781`); EE-9: "**ANSWERED 2026-09-18 (FABLE): the zone script reads it, by sleeping on it**" (`GC:817`) | yes (2026-09-12 / 09-18) |
| C17 | GC §5b: "`EE-12` is ANSWERED: see [the contract] §14, whose EE-12 handlers were verified live" (`GC:615`) | C-GC: "**REFUTED 2026-09-19/22 (`EE-12`, re-verified owner-side)**" (`C-GC:343`), a static route census (`C-GC:570-584`); GC EE-12: "The runtime request is withdrawn; a live session could add confirmation, not discovery" (`GC:835`). No page records a live verification | yes: static (2026-09-19/22) |
| C18 | GC heading: "### The reset zeroes all three fields — added 2026-09-10" (`GC:199`) | GC box: "**The masks are zeroed. The flag byte is not.** (corrected 2026-09-13 …)" (`GC:220-229`) | yes (2026-09-13) |
| C19 | C-GC §2: the interface table is split by the §4a block (`C-GC:57-77`); its rows resume at `C-GC:78-87` with no header row, under the note "Rows below the first nine were added 2026-09-10" (`C-GC:92-93`) | — a structural defect. Ten interface rows (`00239710` … `00238AE0`) sit outside the rendered table | — |
| C20 | names that say ticks: "`wRespawnCooldownTicks` ✓" (`FM:91`; `HT:527`; `SPR:529`); "`SpawnEntry_GetRespawnCooldownTicks`" (`GC:94`, `GC:663`); "`dwLastDeathTick` (seconds) ✓" (`FM:90`); the VM wrapper name (`C-GC:379-381`) | the unit is "**whole seconds, compared with a strict `>`**" (`C-GC:407`); "`+0x10  u16   respawn cooldown, WHOLE SECONDS`" (`C-GC:138`) | yes, the unit is seconds (EE-1, 2026-09-13). The names are kept knowingly (`C-GC:379-381`; `GC:126-127`) |
| C21 | `00300530` as "`BattleStats_ModifyHPAndProcessLethalState`" (`GC:132`, `GC:429`, `GC:679`; `SPR:457`, `SPR:888`) | "`BattleStats_ModifyHPAndProcessLethalTransition`" (`FM:88`, `FM:224`) | no |
| C22 | HT: "`0043F210` (159 B) is a spawn-placement body" (`HT:1186`) | HT §11: `0043F450` "is `PrimaryOwner:Presentation` … an unrelated structure", and calls `0043F210` once (`HT:1007-1013`) | no date settles the label |
| C23 | GC: "`003E6770` (276 B) is a group-respawn body" (`GC:1140`), unstruck; "`003C9250` (280 B) is a group-respawn body" (`GC:1131`), with no support | the correction directly above: "`003E6770` is not a group-respawn body and has no part in respawning" (`GC:1135-1138`, 2026-09-19). `003C9250` is not corrected | yes for `003E6770` (2026-09-19) |
| C24 | `last_reviewed` older than the dated content on the page: GC `2026-09-12` (`GC:19`), with content to 2026-09-29 (`GC:617`); FM `2026-09-10` (`FM:19`), with content to 2026-09-19 (`FM:544`); C-GC `2026-09-11` (`C-GC:17`), with content to 2026-09-29 (`C-GC:103`) | HT explains its own case: the stamp records the last review, not the last edit (`HT:1097-1106`) | — |
| C25 | HT §7 UQ-100: "*(closed — the register row is WITHDRAWN.)*" (`HT:717`) | the same row: "what that stale word holds in practice remains runtime evidence (tier 10) and stays open" (`HT:722`) | no |
