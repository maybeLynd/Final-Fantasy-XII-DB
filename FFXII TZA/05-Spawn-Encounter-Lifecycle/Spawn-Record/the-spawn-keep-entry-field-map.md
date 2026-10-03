---
system: The spawn-keep entry (SpawnRecord, 0x250) — a field map from every accessor
category: 05-Spawn-Encounter-Lifecycle
status: AUDITED
owner_layer: PrimaryOwner:Spawn_Encounter_Lifecycle — the stats page at +0x80 is CombatFormula's
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every function that reaches a spawn record was enumerated two ways — an absolute-address
    scan of the array base 0208E690 (20 functions) and a two-hop displacement scan that follows a
    register loaded from any object's +0x6A0 into its [reg+disp] accesses (79 functions and 362
    accesses with the generation-3 scanner of 2026-09-11, 78 / 358 after the first epilogue fix, 47
    before; control the recompute's byte-0 test) — and the accessors were
    read from the shipping EXE; the four candidate
    selectors are cited through the scan and the spawn-placement page
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-spawn-keep-entry-field-map-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The spawn-keep entry — a field map from every accessor

> Every enemy that the world remembers — where it stood, who it hated, how often it has died, what
> it still has to steal, what it is weak to — lives in one 592-byte record in a bank of 64 that is
> copied whole across area transitions. Three pages read parts of it. This one lists every byte
> that any function in the executable touches, who touches it, and the bytes nobody does.

## 1. What the player sees

The record is why a zone "remembers": a monster killed three times shows its third death in its
respawn cooldown, the Wolf that chased you keeps chasing when you step back in within the window,
a stolen item stays stolen, and an enemy an ability made weak to fire stays weak until it is
reset. None of that is on the enemy definition row; it is here, and it is banked
([the spawn-placement page](../spawn-placement-and-retirement.md) §"The persistence banks").

## 2. Native mechanism

### 2.1 Three ways a record is reached

| route | who | how |
|---|---|---|
| **the lane map** | 20 functions | `unit + 0x40` is the lane map (count at `+0`, entries from `+1`); `slot = map[1 + lane]` (`0xFF` = none); `record = *(0208E690) + slot × 0x250` — the shared prologue of every `SpawnEntry_*` accessor (e.g. `00235F79`–`00235F91`) |
| **the unit's back-pointer** | 79 functions (78 after the first epilogue fix, 47 before; see the CORRECTED note) | `unit + 0x6A0`, installed by `BattleUnit_ApplyUnitDefinition` (`0023AC01`) for kind-1 units, NULL for party ([the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.4) |
| **the bank copies** | 4 loops | `00233780`, `00233440`, `00233550`, and `Spawn_SelectContinuousEntry` (`00235360`) move whole records with `movups`, structure-blind (§2.5) |

The two enumerations were run with a positive control each: the array scan against `02089340`
(126 references), the two-hop scan against `0030FED0`'s `test byte ptr [rcx], 0x80` at
`0031043A`. Two functions found by the hop are not battle-unit code — `001CA600` (8,186 B,
`001CC373`) reaches a different type through its own `+0x6A0` — and are excluded below.

> ### CORRECTED 2026-09-10 — the enumeration counts
>
> The first run of the two-hop scan dropped a tracked register at every early-return epilogue
> (`mov rbx, [rsp+X]` / `pop rbx` were treated as kills), so functions whose record pointer lived
> in a callee-saved register across an early `ret` block lost their later accesses —
> `ActorSystem_ReleaseBattleUnitSlotForActor` (`00234200`) among them, whose `+0x00`, `+0x60`,
> `+0x74` rows were nevertheless in the table because they were read by hand. With the fix, the
> same seeds (plus argument and return propagation, three hops) reach **78 functions and 358
> accesses**, of which the rows above `+0x80` are the stats page inside the record. **No offset in
> the three untouched ranges appeared**, and no field row changed; the counts in this section and
> in §8 are the corrected ones. The published scanner (`hop_scan.py`) carries the fix.
>
> **Second pass, 2026-09-11 (FZ-16, FABLE-PUB140):** the first fix had exempted *every* frame reload,
> which kept dead registers alive elsewhere; the generation-3 scanner exempts only real epilogues and
> follows a record through its spill slot. Re-run with the same seeds: **79 functions and 362
> accesses** — the four new rows are `Equipment_CheckItemEligibleForSlot` (`00317930`) reading the
> stats page's `+0x84` / `+0x85` and the `+0xD0` word through `BattleStats_SetEquipmentSlotDirect`
> (`0031A677`). No row was lost and no offset changed; the array census beside this page (`--array`,
> depth 2, 106 rows) is byte-identical under the new scanner.

### 2.2 The field map

Widths and directions are from the instructions; the GFZ name (tier 3) is quoted where the
placement page carries one, and marked ✓ where the bytes bear it out.

| offset | width | name | what the bytes say | writers | readers |
|---|---|---|---|---|---|
| `+0x00` | u32 | `lifecycleFlags` ✓ | eight bits, §2.3 | see §2.3 | see §2.3 |
| `+0x04` | f32 | ~~`flLifecyclePointThreshold` (placement page) ✓~~ *(no GFZ name)* - not the placement page's mode-2 threshold, which is the battle unit's `+0x4C` *(corrected 2026-10-02, OPUS: `0023519C` `movss xmm6, dword ptr [rsi + 0x4c]` with `rsi` = `0031B760()`, the battle unit, `002350F3`–`002350F8`; mode at unit `+0x50`, point id at `+0x51`)* | the fresh-lifecycle float: `0` → zeroed with bits 3 / 6 cleared; `> 0` → stored, bit 3 set; `< 0` → negated and stored, bit 6 set (`0023A24F`–`0023A2AC`) | `SpawnEntry_ConfigureFreshLifecycleFloatMode` (`0023A200`) | `BattleUnit_HasNonPartyEngagementEvidence` (`00308040`, `0030808B`, `003080D0`): compared with `100.0` and squared into a distance test |
| `+0x08` | u16 | `wDeathCount` ✓ | incremented by the lethal transition | `BattleStats_ModifyHPAndProcessLethalTransition` (`00300530`; [the HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)); zeroed at `0023965C` | `SpawnEntry_GetDeathCount` (`00235F50`, `00235F9A`); `Spawn_SelectAndPrepareAutomaticEntry` (`00235720`, `002358AB`, against `+0x0A`) |
| `+0x0A` | u16 | `wDeathLimit` ✓ | **authored base plus a random range** — `row.b_00 + rand % (row.b_01 + 1)`, or 0 when the base is 0 (`002395FC`–`00239623`) | the initialiser `002395A0` (§2.4) | `SpawnEntry_GetDeathLimit` (`00235EF0`, `00235F3A`); `00235720` (`002358A1`) |
| `+0x0C` | u32 | `dwLastDeathTick` (seconds) ✓ | the death second | `00300530`; zeroed at `00239657` | `SpawnEntry_GetElapsedTicksSinceLastDeath` (`00235FB0`, `00236017`: `now / (30 × [01DFE0B8]) − this`); `00235720` (`002358D1`) |
| `+0x10` | u16 | `wRespawnCooldownTicks` ✓ | **authored base plus a random range** — `row.w_02 + rand % (row.w_04 + 1)`, or 0 (`00239628`–`00239652`) | the initialiser `002395A0` (§2.4) | `SpawnEntry_GetRespawnCooldownTicks` (`002366E0`, `0023672A`); `00235720` (`002358C1`) |
| `+0x12` | u8 | *(no GFZ name)* — the spawn-history counter copy | the pre-increment counter of the row's byte `+2` at a fresh spawn ([the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.2, §2.8) | `BattleUnit_ApplyUnitDefinition` (`0023A570`) | **`BattleUnit_RefreshActorRuntimeFromDefinition`** (`00238BF0`, `00238EA9`): passed with the unit's text pointer `+0x18` to `00269F20(actor, text, n)`, which stores them at the actor work object's **`+0xF8` and `+0x100`** (`00269F20`–`00269F2F`) — **answers `FB-6`**; `00329220` (`003298BD`) copies it into byte `+0x88` of the record it builds |
| `+0x14` | u8 | `bStealAvailabilityFlags` ✓ | bits 0–2 = a steal slot still available; set at a fresh spawn from the row's words `+0x32`/`+0x34`/`+0x36` | `0023A570` (`0023A7B2`–`0023A7E4`); cleared per slot by `BattleFormula_ApplyTargetResult` (`003112F0`, `0031146F`) and `BattleFormula_ApplyResultMetadata` (`00385BA0`, `00385C17`–`00385C6B`, `and 0xFB/0xFD/0xFE`) | `003112F0` (`00311468`); `00390390` (`0039041E`–`0039047E`) |
| `+0x15` | u8 | `bRangeRetireInhibitTag` ✓ | the tag; written with bit 4 | `SpawnEntry_SetRangeRetireInhibitTag` (`002391C0`, `002391EE`, `00239207`) | `AiOrder_EvaluateTargetSelector` (`00301AD0`, `00301D75`) |
| `+0x16` | u8 | `bScriptSelection` ✓ | the script's selection index, `0xFF` = none; bits 0 / 2 of the flags are cleared when it changes (`002398BE`–`002398C2`) | `SpawnUnit_BindEntryAndMarkCapTracked` (`00239840`, `002398BB`); reset to `0xFF` by `SpawnUnit_SetEntryMapAndResetTransientEntries` (`0023A2E0`, `0023A354`) and `SpawnEntry_ResetTransientState` (`00236860`, `002368B0`, as a word with `+0x17`) | `SpawnEntry_GetScriptSelection` (`00236140`, `0023618A`); `00239840` (`002398AD`) |
| `+0x17` | u8 | `bPersistenceKey` ✓ | the active persistence key; `Spawn_SelectContinuousEntry` looks for a history-bank entry with the same key, committed (bit 1) **and** range-reentry-pending **or** released (bits 0 / 2 — `test r8b, 5` skips only when *both* are clear, `00235419`–`0023541D`; this row first read it as "neither", corrected 2026-09-11), and **copies that whole entry over this one** (`002353FA`–`002354DD`) | `002395A0` (`00239671`, from the row); `0023A2E0` (`0023A366`) and `00239840` (`002398CE`) restore it from `+0x18` when the record is fresh | `00235360` (`002353FA`, `0023541F`) |
| `+0x18` | u8 | `bPersistenceRestoreValue` ✓ | the authored key the two resets restore `+0x17` from; `row.b_06` when the table's byte `+1` is set, else 0 | `002395A0` (`00239675`) | `0023A2E0` (`0023A362`), `00239840` (`002398CA`) |
| `+0x19` | u8 | `bEnmityTableHeader` — the decay timer | | | `BattleEnmity_*` — [the placement page](../spawn-placement-and-retirement.md) §"The persistence banks" |
| `+0x1A`–`+0x41` | u8[40] | `aEnmityByCombatantId` | enmity toward combatant id 0–39 | | same |
| `+0x42`–`+0x4F` | 14 B | — | **untouched** by any function in either enumeration | — | — |
| `+0x50`–`+0x5F` | f32[4] | `afPersistedWorldPosition` ✓ | the persisted world position, 16 bytes stored whole | `BattleUnit_PublishLocomotionPosition` (`00300310`, `003003CE`), `Battle_ProcessActionTarget` (`00307300`, `003079F4`), `00311F70` (`00312092`), `SpawnEntry_SetCurrentCandidateState` (`00239410`, `00239494`), `Spawn_PrepareRandomCandidateForCurrentEntry` (`002355A0`, `002356DE`) | the selectors, through the placement page §"Candidate generation" |
| `+0x60`–`+0x6F` | f32[4] | `candidateStateSecondary` ✓ | the candidate position: `x` at `+0x60`, `y` at `+0x64`, `z` at `+0x68` (`00239474`–`00239490` build `{p3, 0, p2, whatever the stack slot held}` from the verb's two floats) | `00239410` (`00239490`), `002355A0` (`002356D5`), `ActorSystem_ReleaseBattleUnitSlotForActor` (`00234200`, `00234291`, from unit `+0xE0`) | `SpawnUnit_FinalizeSpawnEntryActivation` (`0023A410`, `0023A4AE`–`0023A4D5`: `y += unit + 0x188` after `003208C0`, then published through `00300310`) |
| `+0x70` | f32 | `flPersistedFacingYaw` ✓ | the facing | `BattleUnit_PublishLocomotionPositionAndFacing` (`003003F0`, `0030046E`), `00307300` (`00307A4F`), `00311F70` (`003120F7`), `00239210` (`0023929C`: a random yaw in `[0, 360)` scaled by `2π / 360` when the argument is negative, `00239243`–`0023929C`) | `00312B40` (`00312C84`) |
| `+0x74` | u32 | *(no GFZ name)* | written once, from unit `+0x160` — the float `00312EE0` writes with a yaw (`00312F77`) — at slot release | `00234200` (`0023429E`) | **none found** |
| `+0x78`–`+0x7C` | u8[5] | `dwTransientState_78` / `bTransientState_7C` ✗ — **the persisted elemental affinity** | the five bytes of [the affinity page](../../08-Combat-Formula/elemental-affinity-and-the-five-bytes.md): weak, absorb, resist, immune, and the source's ×1.5 — the record-side home the recompute mirrors with stats `+0x40`–`+0x44` under the dirty bit (flags bit 7) | `003112F0` (`or`/`and` per byte, `00311954`–`00311A74`, then bit 7); `0030FED0` (`00310484`–`003104BC`, stats → record when bit 7 is clear); zeroed by `0023A2E0` (`0023A35A`–`0023A35E`) and `00236860` (`002368B6`–`002368BD`) | `0030FED0` (`0031043F`–`0031047B`, record → stats when bit 7 is set) |
| `+0x7D`–`+0x7F` | 3 B | — | **untouched** | — | — |
| `+0x80`–`+0x247` | `0x1C8` | `battleStats` — the stats record (BKBI) | the enemy's `BattleStatsRecord`, initialised in place ([the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.5). The store models it as ONE typed field on the parent — the 23 rows that once described this span as `SpawnRecord` fields were the subobject's own offsets stated in the parent frame, and they now live once on `BattleStatsRecord` (offset − 0x80), reached by the spawn census through a `SUBOBJECT_CENSUS` shift | `BattleStats_InitializeDefinitionRecord` (`0023AC80`) and everything that writes a stats record | everything that reads one; the hop scan through unit `+0x698` reaches 248 functions |
| `+0x248`–`+0x24F` | 8 B | — | **untouched** — the "`0x250 − 8`" the contract's item 6 asks about is exactly the last eight bytes | — | — |

### 2.3 The flag word, bit by bit

`+0x00` is read as a byte or a dword; the same eight bits either way.

| bit | set by | cleared by | tested by | name (placement page) |
|---|---|---|---|---|
| 0 (`0x01`) | `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`, `002352A6`) — the range retire | `0023A410` (`0023A46F`), `00239840` (`002398C2`, with bit 2); `00236860` (`002368AA`) and `00237080` (`00237085`), unconditionally, with bits 2 and 7 *(corrected 2026-10-02, OPUS: both `and dword ptr [rcx], 0xffffff7a`; `0023A2E0`'s same mask at `0023A34E` runs only on fresh entries, where bits 0 and 2 are already clear)* | the **fresh** test `& 5 == 0` in nine functions (`0023A24A`, `0023A42E`, `002396E2`, `00239918`, `002398C5`, `00239346`, `002394F7`, `0023A349`, `0023541D`); `SpawnEntry_QueryRangeReentryPending` (`00236670`, `002366BC`–`002366C7`: returns bit 0 only when bit 1 is set and bit 2 clear) | `RANGE_REENTRY_PENDING` ✓ |
| 1 (`0x02`) | `BattleUnit_ActivateAppliedDefinitionRuntime` (`00233AD0`, `00233BA8`, kind-1 units) | — (survives until the bank is wiped) | `002395A0` (`002395E3`: an entry already committed is skipped by the initialiser); `00236670`; `00235360` (`00235413`); `Spawn_SelectPreviousMapEntry` (`002354F0`, `0023555C` tests bit 2 alongside) | `ACTIVATION_COMMITTED` ✓ |
| 2 (`0x04`) | `ActorSystem_ReleaseBattleUnitSlotForActor` (`00234200`, `0023429B`) — the unit's slot is released | `0023A410` (`0023A465`), `00239840` (`002398C2`); `00236860` (`002368AA`) and `00237080` (`00237085`), unconditionally *(corrected 2026-10-02, OPUS: both `and dword ptr [rcx], 0xffffff7a`)* | the fresh test; `002391C0` (`002391DE`: refuses when set); `00236670` | *(released)* |
| 3 (`0x08`) | `0023A200` (`0023A282`, float `> 0`) | `0023A200` (`0023A267`), `00312EE0` (`00312F30`) | `00233AD0` (`00233B3A`); `00308040` and `002FFCF0` / `003014C0` / `00384F40` as `0x48` with bit 6; `00312EE0` (`00312F4F`) | *(lifecycle point mode, positive)* |
| 4 (`0x10`) | `002391C0` (`002391FD`, with the tag at `+0x15`) | `002391C0` (`002391E2`, when the tag is 0) | `002350C0` (`00235159`); `00301AD0` (`00301D70`); `00237D80` (`00237D93`); as `0x30` with bit 5 by `002FFCF0` (`002FFD51`), `003014C0`, `003247F0`, `0030DA30`, `00384F40` | `RANGE_RETIRE_INHIBITED` ✓ |
| 5 (`0x20`) | `BattleUnit_SetRuntimeUnitCategoryMode` (`002396B0`, `002396F9`, when the mode byte `+0x58` becomes 4) | `002396B0` (`002396E7`), `00237D80` (`00237DD7`) | `00308040` (`00308075`: no engagement evidence while set); `00238BF0` (`00238D98`); `002FFF50` (`00300014`); the `0x30` tests | *(category-4 mode)* |
| 6 (`0x40`) | `0023A200` (`0023A2AC`, float `< 0`) | `0023A200` (`0023A25D`), `00312EE0` (`00312F21`) | `002FFF50` (`00300023`); `0031FE10` (`0031FE43`); `00329220` (`0032935C`); the `0x48` tests | *(lifecycle point mode, negative)* |
| 7 (`0x80`) | `003112F0` (`0031195E`–`00311A7E`, once per affinity byte changed) | `0030FED0` does not clear it — ~~nothing found does~~ `00236860` (`002368AA`) and `00237080` (`00237085`) do, and `0023A2E0` (`0023A34E`) on fresh entries *(corrected 2026-10-02, OPUS: each masks the flags with `0xffffff7a`, clearing bits 0, 2 and 7)* | `0030FED0` (`0031043A`) | *(affinity dirty)* |

### 2.4 The definition-table initialiser — where a record's numbers are authored

`SpawnKeep_InitializeEntriesFromDefinitionTable` (`002395A0`, 268 B; the tail of
`VM_Spawn_InitializeKeepEntriesFromDefinitionTable`, `005106D0`) walks a script-supplied table —
`b_00` = entry count, `b_01` = whether keys are authored, `w_02` = row stride, rows from `+4` —
**authored in the script's own data area** (FD-1, 2026-09-12): the verb `0x3018
btlAtelSetEntryStruct` pops one int, and every one of the 502 calling scripts pushes a scope-3
reference `0x03xxxxxx`, which the resolver `002650B0` turns into `image + [image+0x40] + offset` —
the section-000 data area ([the verb-dispatch page](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md) §4.5, [the section-000 page](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md)) —
and, for every live-bank entry `i` **not yet committed** (bit 1 clear, `002395E3`), writes:

```
rec.w_0A = row.b_00 ? row.b_00 + rand % (row.b_01 + 1) : 0        ; 002395ED–00239623  death limit
rec.w_10 = row.w_02 ? row.w_02 + rand % (row.w_04 + 1) : 0        ; 00239628–00239652  respawn cooldown
rec.dw_0C = 0 ; rec.w_08 = 0                                      ; 00239657–0023965C
rec.b_17 = rec.b_18 = table.b_01 ? row.b_06 : 0                   ; 00239662–00239675  persistence key
```

`rand` is `RNG_SharedGameplayLCG_NextU32` (`00328370`) — **the death limit and the respawn
cooldown are rolled per entry from an authored base and range**, so two visits to the same zone
can give the same monster different cooldowns.

### 2.5 The blind copies

`Spawn_SelectContinuousEntry` copies `0x250` bytes — four `0x80` blocks and a `0x50` tail
(`00235460`–`002354DD`) — from the matching history entry over the live one; the three bank loops
in `00233780` / `00233440` / `00233550` move `0x9400` bytes per bank in 128-byte `movups` pairs.
None of them names a field; they carry the stats page at `+0x80` along with everything else, which
is how a banked enemy keeps its HP, statuses and level across a return within the window.

## 3. Key addresses

| address | size | what |
|---|---|---|
| `0208E690` | ptr | the live bank (`btlKeepCharWork1`); `0208E698` the history bank; ~~`0208E6A0` the bank flag~~ *(corrected 2026-10-02, OPUS: `0208E6A0` is the battle-unit slot count, 32 - its only writer `002368D0` stores `0x20` (`002368EB`/`002368FE`) and the unit loops bound on `cmp ebx, [0208E6A0]`; no bank flag was found)* |
| `002395A0` | 268 B | `SpawnKeep_InitializeEntriesFromDefinitionTable` — §2.4 |
| `0023A2E0` | 161 B | `SpawnUnit_SetEntryMapAndResetTransientEntries` (tail of `VM_Spawn_SetEntryMapAndResetTransientEntries`, `00510620`): installs the lane map at unit `+0x40`, and for every fresh entry clears bits 0 / 2 / 7, sets `+0x16 = 0xFF`, zeroes `+0x78`–`+0x7C`, restores `+0x17` from `+0x18` |
| `00236860` | 103 B | `SpawnEntry_ResetTransientState` (tail of `VM_Spawn_ResetEntryTransientState`, `005104D0`): ~~the same clears for one entry~~ `0023A2E0`'s mask for one entry, applied without the fresh test, and `+0x17` zeroed rather than restored *(corrected 2026-10-02, OPUS: `002368AA` `and dword ptr [rcx], 0xffffff7a` runs on any mapped entry; `002368B0` `mov word ptr [rcx + 0x16], 0xff` writes `+0x17` = 0)* |
| `00237080` | 29 B | `SpawnEntry_ClearSelectionTransientStateForTeardown` (research import — `MOB_LIFECYCLE_RESEARCH_HISTORY.md` / `PROGRAM_B_NATIVE_REFERENCE.md` "wipes the keep record's flags/+0x16/+0x78/+0x7C"; body re-read 2026-09-15): null-check, then the same transient clears — flags `& 0xFFFFFF7A` (bits 0 / 2 / 7), `+0x16 = 0xFF`, `+0x78`/`+0x7C` zeroed — ~~minus `00236860`'s `+0x17` restore~~ the same four stores as `00236860`, which restores no `+0x17` either *(corrected 2026-10-02, OPUS: `00237085`–`00237098` and `002368AA`–`002368BD` match store for store; both zero `+0x17` through the word store at `+0x16`)*. Called from `TeardownAndDespawn` mode 0 (`00300E40`) per `X55_NATIVE_REPLAY_CONTRACT.md` |
| `00239840` | 168 B | `SpawnUnit_BindEntryAndMarkCapTracked` (tail of `VM_Spawn_BindEntryAndMarkCapTracked`, `005103F0`): lane byte `+0x57`, `+0x16`, unit flag bit 21 |
| `00239410` | 169 B | `SpawnEntry_SetCurrentCandidateState` (tail of `VM_SpawnEntry_SetCurrentCandidateState`, `0050FCB0`): `+0x50` and `+0x60` from two floats, unit flag bit 26 |
| `002391C0` | 80 B | `SpawnEntry_SetRangeRetireInhibitTag` (tail of `VM_SpawnEntry_SetRangeRetireInhibitTag`, `00510370`) |
| `002396B0` | 82 B | `BattleUnit_SetRuntimeUnitCategoryMode` (tail of `VM_BattleUnit_SetRuntimeUnitCategoryMode`, `00510340`): unit `+0x58` from a 4-entry table at `01E09EE8`, flag bit 5 |
| `0023A200` | 185 B | `SpawnEntry_ConfigureFreshLifecycleFloatMode` (tail of `VM_SpawnEntry_ConfigureFreshLifecycleFloatMode`, `005107C0`): unit flag bit 40 and the `+0x04` float with bits 3 / 6 |
| `0023A410` | 270 B | `SpawnUnit_FinalizeSpawnEntryActivation`: the tail of the script verb **`0x304C` `btlAtelSetUnitFinish`** (its 8-byte handler `00510250` jumps here at `00510253`; the graph has no E8 caller, one E9); on a fresh record whose definition row has a non-zero dword `+0x18`, `BattleStats_SetCurrentHP(stats, row.dw_18, 0, 0x297)` (`00300520`, `0023A433`–`0023A451`) — **an authored starting-HP override**; clears bits 0 / 2, publishes the candidate position, recompute with `0x297`, `00386C10` |
| `00233AD0` | 316 B | `BattleUnit_ActivateAppliedDefinitionRuntime`: sets bit 1 and unit flag bit 49 |
| `00234200` | 225 B | `ActorSystem_ReleaseBattleUnitSlotForActor`: bit 2, `+0x60` from unit `+0xE0`, `+0x74` from unit `+0x160`, then the unit slot is zeroed (`0xF50` bytes) |
| `00236670`, `00236140`, `00236030`, `00235FB0`, `00235F50`, `00235EF0`, `002366E0` | 93–155 B | the `SpawnEntry_*` getters (script verbs) |
| `00235720`, `002355A0`, `002354F0`, `00235360` | 841 / 376 / 166 / 390 B | the four selectors — the placement page |
| `00237D80` | 112 B | clears bit 5 for a kind-1 unit with unit flag bit 4 and no terminal status, then `00238BF0` |
| `00312EE0` | 187 B | (from `BattleUnit_EnterPartyCombatStance`, `00313400`) clears bits 3 / 6, sets unit `+0x6B0` bit 0 |
| `00269F20` | 16 B | `(actor, text, n)` → actor `+0xF8`, `+0x100` — the consumer of unit `+0x18` and record `+0x12` |
| `00238BF0` | 929 B | `BattleUnit_RefreshActorRuntimeFromDefinition` — calls it at `00238EB8` |

## 4. Data structures and formulas

```
SpawnRecord (BKEI), 0x250, in btlKeepCharWork1/2 (64 each), reached by lane map or unit+0x6A0
  +0x00 u32  lifecycleFlags     b0 range-reentry-pending  b1 activation-committed  b2 released
                                b3 point mode (+)  b4 range-retire-inhibited  b5 category-4 mode
                                b6 point mode (−)  b7 affinity dirty
  +0x04 f32  lifecycle threshold (|value|; sign chose b3/b6)   # <- corrected 2026-10-02, OPUS - not the mode-2 retire threshold (unit +0x4C, 0023519C); read only by 00308040 (003080D0)
  +0x08 u16  death count        +0x0A u16 death limit (base + rand(range))
  +0x0C u32  last death second  +0x10 u16 respawn cooldown (base + rand(range))
  +0x12 u8   spawn-history counter copy      +0x14 u8 steal bits 0-2
  +0x15 u8   range-retire tag   +0x16 u8 script selection (0xFF none)
  +0x17 u8   persistence key    +0x18 u8 authored key (restore value)
  +0x19 u8   enmity decay       +0x1A u8[40] enmity by combatant id
  +0x42 ..+0x4F  untouched
  +0x50 f32[4] persisted world position     +0x60 f32[4] candidate position {x, y, z, -}
  +0x70 f32  facing yaw         +0x74 u32 from unit+0x160 at release (no reader)
  +0x78 u8[5] elemental affinity (weak, absorb, resist, immune, source x1.5)   +0x7D..+0x7F untouched
  +0x80 BattleStatsRecord (0x1C8)           +0x248..+0x24F untouched
```

**Fresh**: `(flags & 5) == 0` — neither range-reentry-pending nor released. The steal bits, the
spawn counter, the script's one-shot statuses, the key restore and the affinity reset all happen
only then.

**The continuous-entry match**: ~~`history[j].flags & 2 && !(history[j].flags & 5) && history[j].b_17 == live.b_17`~~ `history[j].flags & 2 && (history[j].flags & 5) && history[j].b_17 == live.b_17` *(corrected 2026-10-02, OPUS: `00235413` `test r8b, 2` / `je` skip, `00235419` `test r8b, 5` / `je` skip, `0023541F` `cmp r9b, byte ptr [rax + 0x17]`; the `+0x17` row in §2.2 already says so)*
→ `memcpy(live, history[j], 0x250)`.

## 5. Call chain

```
script verbs (family 0x30xx, VM_Spawn_* / VM_SpawnEntry_*)
  005106D0 -> 002395A0  initialise entries from a definition table   (+0x08..+0x18)
  00510620 -> 0023A2E0  set the lane map, reset fresh entries          (+0x00, +0x16, +0x17, +0x78..+0x7C)
  005103F0 -> 00239840  bind an entry                                  (+0x16, +0x17, +0x00)
  0050FCB0 -> 00239410  set the candidate state                        (+0x50, +0x60)
  00510370 -> 002391C0  range-retire inhibit                           (+0x00 b4, +0x15)
  00510340 -> 002396B0  runtime category mode                          (+0x00 b5)
  005107C0 -> 0023A200  fresh lifecycle float                          (+0x00 b3/b6, +0x04)
  005104D0 -> 00236860  reset one entry                                (+0x00, +0x16/17, +0x78..+0x7C)
  getters   -> 00236140 / 00236030 / 00235FB0 / 00235F50 / 00235EF0 / 002366E0 / 00236670
  0x304C btlAtelSetUnitFinish 00510250 -> 0023A410  finalize activation (b0/b2 cleared, HP override)
BattleUnit_ApplyUnitDefinition 0023A570              -> +0x12, +0x14, +0x80 page, unit+0x6A0
BattleUnit_ActivateAppliedDefinitionRuntime 00233AD0 -> b1
SpawnUnit_FinalizeSpawnEntryActivation 0023A410     -> b0/b2 cleared, +0x60..+0x68 read, recompute 0x297
BattleStats_ModifyHPAndProcessLethalTransition 00300530 -> +0x08, +0x0C
BattleFormula_ApplyTargetResult 003112F0 / ApplyResultMetadata 00385BA0 -> +0x14, +0x78..+0x7B, b7
BattleStats_RecomputeDerivedStateAndAutoStatuses 0030FED0 -> +0x78..+0x7C <-> stats +0x40..+0x44
movement publishers 00300310 / 003003F0 / 00307300 / 00311F70 / 00239210 -> +0x50, +0x70
ActorSystem_ReleaseBattleUnitSlotForActor 00234200   -> b2, +0x60, +0x74
BattleUnit_RefreshActorRuntimeFromDefinition 00238BF0 -> +0x12 (with unit +0x18) -> actor +0xF8/+0x100
SpawnKeep_RotatePersistenceBanksForAreaTransition 00233780 / Serialize 00233440 / Restore 00233550 -> whole banks
Spawn_SelectContinuousEntry 00235360                 -> whole record from the history bank by +0x17
```

## 6. Modding notes

- **A monster's death limit and respawn cooldown are authored as base + range and rolled per
  entry** by `002395A0` from the table the script passes; a mod that wants deterministic respawns
  sets the range bytes to 0.
- **The persistence key `+0x17` / `+0x18` is what lets a monster be "the same one" across a
  return**: `Spawn_SelectContinuousEntry` matches on it and copies the entire record, stats page
  included. Two entries with the same authored key will restore each other's state.
- **The affinity bytes are on the record, not the row**: an ability that changes an enemy's
  weakness writes `+0x78`–`+0x7C` and raises bit 7; the next recompute copies them into the stats
  record. A reset of the entry (`0023A2E0`, `00236860`) zeroes them.
- **Three ranges are never touched** — `+0x42`–`+0x4F`, `+0x7D`–`+0x7F`, `+0x248`–`+0x24F` — by
  any function either enumeration reaches; they are padding or fields only the blind copies carry.
- **`+0x74` is written and never read.** A reconstruction may keep it for save-image fidelity and
  nothing else.

## 7. What is not known

- [x] ~~**Which script-data table `005106D0` hands to `002395A0`**, and whether the `b_01` flag and
  the `b_06` key column are set in shipped scripts.~~ **FD-1 ANSWERED 2026-09-12 (FABLE) from all
  502 calling scripts.** The table lives in the script's section-000 data area (the `+0x40` region;
  the argument is a scope-3 reference, §2.4). Parsed at that address in every one of the 502
  `btlAtelSetEntryStruct` callers over the 1,114-container corpus, zero failures:
  **`b_00` equals the script's `btlAtelSetUnit` call count in 502 of 502** — one row per authored
  `spawnGroup`, in order; **`w_02` is 8 in all 502**; **`b_01` is `100` (`0x64`) in all 502** — never
  0, so the native's non-zero test (`00239662`) always takes the row's `b_06`, and what else the value
  100 might mean has no reader (`002395A0` is the pointer's only consumer, `005106D0` its only caller);
  row byte `+7` is 0 in every row. **Keys: the `b_06` column is 0 in 6,671 of the 6,746 rows; twelve
  scripts author non-zero keys** — `bhm_a01` and `bhm_a03` (keys 1–18 over 18 rows each), `bhm_a02`
  (rows 12–29 carry 13–18, 7–12, 1–6), `lus_g01`–`lus_g04` (rows 0–3 carry 1–4), `lus_b01` (row 0 = 5),
  `lus_b02` (row 1 = 5), `lus_b03` (row 0 = 5), `mic_e01` and `mic_e02` (row 0 = 1) — so the
  same-key restore of §2.2 `+0x17` operates only between those maps' matching entries. The death
  limit and cooldown columns are overwhelmingly `(1, 2)` and `(120, 60)` (3,395 / 3,494 rows) or all
  zero (1,666 / 2,765 rows). Corpus tally in `Tools/work/repos-d2` (the `.src.data` files there are
  exactly the `+0x40` data area: 602 of 602 byte-equal).
- [x] ~~**What `00386C10` does** — the tail call every activation (`0023A513`) and every runtime
  activation (`00233BFC`) ends in, on the stats record — and what `003208C0` computes for the
  candidate `y` at `0023A4BC`.~~ **FD-2** — answered 2026-09-11, both halves by pages that already
  had them: `BattleRuntime_ResetPersistentStatePrefix` (`00386C10`) zeroes the first 32 bytes of the
  unit's 64-byte record in `0208D480` (party, by stats `+4`) or `0208DE80` (by unit `+0xEA9`)
  ([the handler table](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md) §4;
  confirmed here: `00386C59`–`00386C66`) — the prefix that holds the resolver's `+4` / `+8` masks
  and `+0x10` attack word and the combo nibble at `+0x12`, so every activation resets them; and
  `003208C0` is the field-surface probe, `{x, 1.0, z, 1.0}` through `0026E3C0` on `[02EC1370]`,
  writing the surface height or 0 ([spawn placement](../spawn-placement-height-and-authored-tunables.md)
  §"Height resolution at activation"; confirmed: `003208E1`–`0032091E`).
- [x] ~~**What reads the actor work object's `+0xF8` text pointer and `+0x100` number** that
  `00269F20` stores — the display consumer of the unit's name reference and spawn count.~~ **FD-3**
  — answered 2026-09-11: the actor's display name is `00263990(actor)` — if the word `+0x102` is
  negative it returns the `+0xF8` text pointer (`00263994`–`002639AB`), else it resolves the
  script-assigned name id (`setnpcname` `0x38A` / `setshopname` `0x4A9` → `00269F40` → `+0x102`)
  through `0032A930` and the id table at `[02B5E0D8]` (`003EAC10`) — the table is `npcdic.bin`, 1,141 name pairs with the persistent flag of the same number selecting the second ([the NPC name dictionary](../../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md), 2026-09-11); seven callers (`0025C230`,
  `0025C830`, `00268D10`, `00272CB0`, `00272CE0`, `002AC5F0`, `002B0280`). The `+0x100` count is
  read by `00263A10` (`00263A1A`) for the battle-message realiser's name slot and by `00272C80` /
  `00272CE0`. The stats-side lookup the battle log uses is `00536310`: party row word `+0x30`, or
  the actor's `+0x102`, or the enemy row word `+8` ([the post-result events page](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2.5).
- [x] **What `00329220` (1,933 B) builds** from the unit (its record's `+0x88` takes the spawn
  counter, `+0x10` the empty string at `01CEB638`), and what `00390390` (741 B) does with the steal
  bits. **FD-4** — answered 2026-09-10: the party member status view
  ([the status-view page](../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md)), and
  the steal roll, calculator slot 195, whose three reads of `+0x14` are the availability test per item
  word ([the steal-roll page](../../08-Combat-Formula/Steal/the-steal-roll.md)).
- [x] ~~**What `+0x74` was for**, written from unit `+0x160` at release and read by nothing the two
  enumerations reach; and whether the three untouched ranges are read through a route neither
  enumeration covers (a pointer passed onward).~~ **FD-5 ANSWERED 2026-09-12 (FABLE).** The
  pointer-passed-onward route was followed: `hop_scan.py` re-run with the page's seeds at **depth
  6** (`--hop 0x6A0 --array 0x0208E690:0x250 --size 0x250 --depth 6`, control found) reaches 544
  accesses in 90 functions and 54 propagated `(callee, arg)` pairs against depth 3's 362 / 79 / 30;
  the eleven functions depth 6 adds — `002FEF30`, `00300BC0`, `00300CE0`, `0030E060`, `0030E130`,
  `0030E360`, `0030EA40`, `00323C60`, `003279B0`, `00387730`, `0046A690` — are all reached as
  `arg + 0x80`, the stats record embedded in the entry's second block, and read nothing below
  `+0x84` (one read at `+0x242`, `0046A690`, is the highest). **No route at any depth reads `+0x74`, `+0x42`–`+0x4F`,
  `+0x7D`–`+0x7F` or `+0x248`–`+0x24F`**; the only access in those bytes is the one write at
  `0023429E`. What `+0x74` *was* for is therefore only what its source says: unit `+0x160` is the yaw
  the party combat stance writes ([the unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) `+0x160`), captured at slot release beside the
  facing `+0x70` the spawn paths write — a release-time facing that nothing restores, carried into
  the save image by the whole-bank serializer `00233440` and by the blind copies. Tally in
  `Tools/work/FABLE/bf3-scratch/hop_d6-2026-09-12.txt`.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The 20 direct accessors | `data_xref_scan --addr 0x0208E690`, control `02089340` (126 refs) | 1 | PROVEN |
| The 79 hop accessors and every `[rec+disp]` they perform | `hop_scan.py --hop 0x6A0 --array 0x0208E690:0x250 --size 0x250 --depth 3`, control `0030FED0:0x0` found; 362 accesses with the generation-3 scanner (358 / 78 functions after the first epilogue fix, 47 / 118 before — the CORRECTED note in §2.1) | 1 | PROVEN |
| The direct accessors' offsets | `hop_scan.py --array 0x0208E690:0x250`, control `00235F50:0x8` found; 48 accesses in 14 functions | 1 | PROVEN |
| The initialiser's formulas | `002395E3`–`00239675` | 1 | PROVEN |
| The table is the script's `+0x40` data area; `b_01` = 100, stride 8, one row per `spawnGroup`, twelve keyed scripts | `002650B0`'s jump table at `00265180` (scope 3 → `00265155`); 502 `PUSHI 0x03xxxxxx` arguments; the tables parsed at `image + [image+0x40] + offset` in all 502 scripts, row count = `btlAtelSetUnit` count in 502 of 502 | 1 + 9 | PROVEN (data) |
| The flag bits' writers and readers | the sites in §2.3, read from the listed functions | 1 | PROVEN |
| The continuous-entry match and copy | `002353FA`–`002354DD` | 1 | PROVEN |
| `+0x12` and unit `+0x18` go to actor `+0xF8` / `+0x100` | `00238EA9`–`00238EB8`, `00269F20`–`00269F2F` | 1 | PROVEN |
| The three untouched ranges | absence in both enumerations, each with a passing control | 1 | PROVEN (for the enumerated routes) |
| No pointer-passed-onward route reads `+0x74` or the three ranges | `hop_scan.py` at depth 6 (544 accesses / 90 functions / 54 propagated pairs, control found): the eleven functions beyond depth 3 all enter as `arg + 0x80` and read `+0x84` and above | 1 | PROVEN (to depth 6) |
| The GFZ names marked ✓ | the bytes agree with the imported name | 1 (name 3) | PROVEN |
| What the untouched bytes and `+0x74` are for | **not established** | — | UNKNOWN |

## 9. Related

- [`../spawn-placement-and-retirement.md`](../spawn-placement-and-retirement.md) — the banks,
  the selectors, the enmity table, the retire path.
- [`../CONTRACT-group-completion-and-respawn.md`](../CONTRACT-group-completion-and-respawn.md) —
  item 6 of its open list is this page.
- [`../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)
  — the installer that fills `+0x12`, `+0x14`, `+0x80` and unit `+0x6A0`.
- [`../../08-Combat-Formula/the-auto-status-rebuild.md`](../../08-Combat-Formula/the-auto-status-rebuild.md)
  — the affinity handshake.
- [`../../08-Combat-Formula/elemental-affinity-and-the-five-bytes.md`](../../08-Combat-Formula/elemental-affinity-and-the-five-bytes.md)
  — what the five bytes mean.
- [`../../07-Combat-Action/applying-a-result-to-a-target.md`](../../07-Combat-Action/applying-a-result-to-a-target.md)
  — the steal bits and affinity writes.
- [`../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md`](../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md)
  — the verbs whose tails write here.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every cited access site in this map was disassembled and its displacement compared with the offset of
the row citing it, by
[`check_field_citations.py`](../../../Tools/analysis-kit/gfz-scripts/check_field_citations.py):
**18 sites across 11 rows**.

| outcome | sites |
|---|---:|
| displacement **is** the row's offset | 15 |
| resolved through an embedded sub-object base | 1 |
| indexed form, indeterminate by displacement alone | 0 |
| cites the source object of a cross-object copy | 1 |
| cites a datum rather than an instruction | 0 |

**Nothing failed to decode, and no site contradicts its row.**

**The sub-object bases, counted for the first time** (1 distinct): `+0x2` x1.

Small enough to check by eye, and it agrees with the mechanical pass - which is worth one line as a control on the method itself.

**Not claimed:** this checks what the map *says* — that each citation touches the offset it is filed
under. It says nothing about fields the census never reached, and the document's own coverage limits
stand unchanged.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Rewards_Progression_Economy — SERVICE and CLIENT.**
  - The definition initialiser `BattleStats_InitializeDefinitionRecord` (`0023AC80`) calls the 432-byte level-rank
    function.
  - The status changer `0030E360` reaches `BattleUnit_ProcessDefeatRewardsAndLoot`.
  - The recompute `0030FED0` is called from the level-up path `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`
    and from the level-rank function. The level-up path also calls a body in the battle message poster group.
  - `BattleFormula_ApplyTargetResult` (`003112F0`) calls `GameState_GetGil`, `GameState_SetGil` and the level-up path.
  - The unit display builder `00329220` calls a 122-byte rewards helper.
- **Presentation — SERVICE and CLIENT.**
  - Four action paths ask `BattleUnit_ComputePresentationSuppression…`: `002FFF50`, `00300E40`,
    `Battle_ProcessActionTarget` and `00312EE0`.
  - `00301AD0` asks `BattleUnit_TestActorViewFrustumAtCur…`.
  - The two large render bodies `002AC5F0` and `002B0280` submit through `RenderCommand_SubmitCurrentBufferAnd…`. They
    are called from Presentation bodies of 2,440 and 1,027 bytes, and `002B0280` also reaches `00263990`.
  - `001CA600` is called by a 542-byte Presentation body.
- **CoreRuntimeScheduling — MECHANICAL, with one SERVICE.**
  - Eighteen of the cited functions reach their tables through `ImageAddress_ResolveRuntimePointer`; that is mechanical.
  - `00233780`, `00235720`, `00235FB0` and the HP write `00300530` read `GameClock_GetRawTickCounter`, and
    `002AC5F0` / `002B0280` read a 7-byte core getter. The tick reads are SERVICE edges.
- **Audio — MECHANICAL.** `BattleFormula_ApplyTargetResult` plays its hit sound directly through the resolver and
  player, as documented in [the request chain](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md).
- **ActorEntity - CLIENT and SERVICE (168 edges).** `00233AD0` is also called by bodies filed to ActorEntity: `0037B4D0`; `00233AD0` reaches bodies filed to ActorEntity: `00238BF0`, `00239E10`, `0031B760` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT and SERVICE (117 edges).** `00236850` is also called by bodies filed to combat formula: `0031B860`, `0031E800`, `00384F40`; `00233AD0` reaches bodies filed to combat formula: `00386C10` - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT and SERVICE (38 edges).** `002FEF30`, `00309EC0` are also called by bodies filed to items/equipment: `0030A4E0`, `00317930`; `0023AC80` reaches bodies filed to items/equipment: `0031A630`, `00323910` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (127 edges).** `00236850` is also called by bodies filed to movement: `00326D60`, `003278D0`, `00337C10`; `00233AD0` reaches bodies filed to movement: `00311F70` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (41 edges).** `00236850` is also called by bodies filed to party: `003273D0`; `002350C0`, `0025C830` reach bodies filed to party: `003272A0`, `003273B0`, `00358BB0` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (10 edges).** `002355A0`, `00239210`, `002395A0` reach bodies filed to random selection: `00328370`, `00308EC0` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (1 edge).** `0032A930` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (112 edges).** `00235360`, `002354F0`, `00235720` are also called by bodies filed to script VM / native bridge: `00510260`, `00510230`, `0050F520` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (1 edge).** `002368D0` (`BattleStorage_InitializeWorkArrays`, the slot-count writer named in §3) calls `003843F0` at `002369CE` to register the authored `"STATIC"` table, index `0x13`, as the [authored-table row lookup contract](../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) documents - a table registration the resource layer serves, no shared ownership. *(SWE2-FRONTIER, 2026-10-03.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleUnit_TrySelectAndCommitAiOrderFromSet`, owned by that layer, calls `003014C0` on this page. That caller is the order attempt: it starts from `word[+0x714]`, carries `0xFFFF` as its no-order answer, and works in a `0x50`-byte frame; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT (29 edges through 17 of this page's functions).** The Gameplay layer reaches this page at `00301AD0`, `002FEF30`, `002FFCF0`, `00300530` and 13 more. `BattleSystem_ResetRuntimeState` is the worked example, read in full - it is the runtime reset: it walks **40 records of `0x1C8` bytes** from `[02EBF190] + 8` and resets each through `0023AC80`; **8 of the 15 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — SERVICE.** `0030E360` on this page calls `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer. What it reaches is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — SERVICE.** `00263990` on this page calls `PersistentFlag_QueryBank2048`, owned by that layer. What it reaches is the 2,048-bit bank query, and it states its own range: an id at or above **`0x800`** or below zero answers false without touching the bank; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (6 edges through 5 of this page's functions).** The UI layer reaches this page at `002B0280`, `00272CB0`, `00272CE0`, `002FFCF0` and 1 more. `BattleMenu_BuildCommandEntryList` is the worked example, read in full - it is the command-list build, and the ceiling is in the first instruction: the menu kind is bounded at **`0x22`** into a jump table, after which `dword[+0x40]` is zeroed and `dword[+0x44]` set to `-1` before any entry is written; **2 of the 6 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT (2 edges).** `00226BE0` calls `003590D0` and `00253C70` calls `00377C20` (`FieldData_GetActiveFieldRecordBit15`, the shared action-permission accessor) — both callees are shared helpers named in this page's `003014C0` shared-callee list. Input-layer clients of shared helpers; fan-in, not shared ownership. Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).

**InputGameplay — CLIENT (1 edge).** `00313A00`, owned by that layer, calls `00377C20`, the same shared action-permission accessor. The crossing is the consult, not shared ownership. Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).

**PlatformOnlineAchievements — CLIENT (1 edge).** `00315E90`, a 519-byte body owned by that layer, calls `00309EC0` (`BattleEncodedId_DispatchQueryMode0Value`) — the encoded-id mode-0 query this page's `00317930` eligibility gate consults on the flag-arg path. The crossing is the consult, not shared ownership. Read from `edges.tsv` 2026-09-18 (SWE2-EC7).

## The `002B0280` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`002B0280` (6,441 B, `002B0280`–`002B1BA9` per functions.tsv — the "~500 B"
noted earlier was wrong; corrected 2026-09-17 per
AUDITSEM-CONTRA-FRONTIER-2B0280-SIZE) — the render submit prep — reads `r15 = [rcx+0x28]`,
`r12d = byte[rcx+0x33]`, `dword[rcx+0x44]` (`002B02AA`–`002B02C6`),
`0039C4A0` (`002B030F`), publishes `dword[r14+0x30]` to `0209D480`
(`002B0336`), seeds `xmm12 = 1.0f` (`01CEBBA8`, `002B0329`), takes
`[0209CC40]` (`002B033C`), writes `dword[01E0CDF4] = 1.0f`
(`002B034D`), `byte[rcx+0x10FC] = 0` (`002B0357`), `rsi = [r14+0x68]`
(`002B035E`), `byte[r14+0xAB] = 0` (`002B036D`).

| member | role | interior |
| --- | --- | --- |
| `002B1C90` (143 B) | record write — `[0209E5A0]`/`[0209CC50]` pair (`002B1C90`/`002B1C9A`), `dword[rcx+0xC] = 1` (`002B1CAC`), `dword[rdx] = ecx`, `dword[rdx+4] = r8d` (`002B1CBE`/`002B1CC2`) | [`002B1CBE`](../../_index/ADDRESS-INDEX.md) |
| `002B1D20` (246 B) | record link — `[02EBEFF0]`/`02EBEFC0` context (`002B1D24`/`002B1D31`), `[rax+8]` → `0209E5A0` (`002B1D56`), `byte[r8+0x9F]` (`002B1D47`), `qword[rcx] = rax` (`002B1D79`) | [`002B1D56`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0039C4A0`, `00263990` (the page's
second edge). The `0209CC40`/`0209CC48`/`0209CC50` cells are the
shared render-record heads.

## The `003014C0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`003014C0` `AiOrder_EvaluateAndResolveActionTarget` (876 B per functions.tsv —
the "~447 B" noted earlier was wrong; corrected 2026-09-17 per
AUDITSEM-CONTRA-FRONTIER-3014C0-SHAPE) — the
order-side target resolver. `00308EC0` early-exit (`003014F6` → jmp out
at `0030150C`); `02089340` bit-`0x20` service gate (`00301511`); the
candidate gates read `byte[rcx+5] == 1` (`00301564`), `test [rax], 0x48`
(`00301571`), `word[r12]` vs `ax` (`0030157B`), `qword[rdi+0x738]` vs
`r14` (`003015AD`), `byte[rdi+0x730]` bit 1 (`003015C2`), then
`00301830`, `002E9C00`, `002FFCF0`, `00328370` and `0030F130`
(`00301649`) — the stored-range buffer fill before resolve.

| member | role | interior |
| --- | --- | --- |
| `0030F130` `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` (408 B) | candidate-buffer fill — `(rcx, dx, r8)`; copies `qword[rax]` → `[rdx]` on the hit path (`0030F1C3`/`0030F1C6`), calls `00316CF0` on `r15` (`0030F1D1`) | [`0030F1D1`](../../_index/ADDRESS-INDEX.md) |
| `00319460` `Vector3_IsWithinXZRadius` (39 B) | XZ-radius predicate — `call 003A1960` at `0031946C`, then performs the square-radius compare itself: `mulss xmm6,xmm6; comiss xmm6,xmm0; setae al` — not a tail-jump (AUDITSEM-CONTRA-FRONTIER-3014C0-SHAPE, 2026-09-17) | [`0031946C`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00308EC0`, `00377C20`, `00301830`,
`002E9C00`, `002FFCF0`, `00328370`, `00316CF0`, `00301AD0`,
`003590D0`, `003588B0`, `003A1960`. The `02089340` byte is the shared
service/test flag word.

## The `00384F40` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00384F40` (656 B) — a composite recompute over the resolved battle unit:
`0031B860(rdx)` re-resolves and republishes `02EBF188` three times
(`00384F5E`/`00384FA4`/`00385086`), the flag word is probed through the
`0x30` pair (`003850F7`) and the `0x48` bit-6 test, `0020E600` reads two
`[02EBF138]` scratch rows (`00385009`/`0038501D`), `word[rcx+8]` is
scaled by `[02AEDFD4]` (`0038502D`), a `byte[+5]` quantity is divided by
`10.0f` (`00385046`), and `byte[rax+0xEA9]` feeds `00313F60`
(`00385097`/`003850D1`). The `002F8E70`/`002F8E90` pair apply scaled
arithmetic twice (`0038511A`–`00385141`); the pass ends through
`003A1920` and `00808C40` (`0038516D`/`003851DB`).

| member | role | interior |
| --- | --- | --- |
| `00334790` (36 B) | `minss` helper — `00265090` fills the stack pair, returns `minss` of them (`003347A3`/`003347A9`) | [`003347A9`](../../_index/ADDRESS-INDEX.md) |
| `00334A70` (58 B) | null-safe `maxss` helper — `rcx`/`[rcx+0x10]` null → `xorps`; else `00265090` pair → `maxss` (`00334A77`/`00334A9F`) | [`00334A9F`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0031B860`, `00265020`, `0020E600`,
`00236850`, `00321170`, `00313F60`, `002F8E70`, `002F8E90`, `00265090`,
`003A1920`, `00808C40`.

## The `002FFF50` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002FFF50` (`BattleTarget_ComputeEligibilityBlockMask`, ~96 B) — arg
shuffle `esi = r8d`, `ebp = edx`, `rdi = rcx` (`002FFF5F`–`002FFF64`).

| member | role | interior |
| --- | --- | --- |
| `0030B950` | `0030B770(rcx, edx)` resolve wrapper (`0030B964`) | [`0030B964`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0030B770`.

## The `0030EA40`/`00312EE0` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`0030EA40` (`BattleStats_UpdateStatusAuxiliaryValue`, ~104 B) —
`qword[02EBF040]` base load (`0030EA54`).

| member | role | interior |
| --- | --- | --- |
| `00387020` | `edx == 0xFF` -> 0 sentinel clear (`00387028`/`00387030`) | [`00387028`](../../_index/ADDRESS-INDEX.md) |

`00312EE0` ~~(~208 B)~~ (187 B *(corrected 2026-10-02, OPUS: `ret` at `00312F9A`; `00312FA0` begins the next function)*) — `qword[+0x698]` null-gated walk
(`00312EE3`/`00312EEE`).

| member | role | interior |
| --- | --- | --- |
| `0031ACC0` | stack-cookie `0x60` frame with `xmm6` save — SIMD body (`0031ACC6`/`0031ACCB`) | [`0031ACC6`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-21 update (2026-09-18) — `003FFEE0` stride-walk fragment

`003FFEE0` (33 B) is a two-field bit-extract returning a fixed consumed length:
when `rdx` is non-null it writes `[rdx] = [rcx+1] & 0x7F` (`003FFEE5`..`003FFEEB`),
and when `r8` is non-null it writes `[r8] = [rcx+2] & 0x1F` (`003FFEF2`..`003FFEF8`);
returns 3 (`003FFEFB`). The 7-bit/5-bit lane split the keep-entry readers pull
out of packed record bytes. Callers `002A8C50`/`002AC5F0`/`002B0280` — including
this page's `002AC5F0`/`002B0280` keep-entry readers.

## SWE2-EC7-26 update (2026-09-18) — `00317930` multi-record eligibility gate

`00317930` (493 B) is the keep/spawn eligibility predicate: `r8d > 4`
returns 0; `word[00D107E8 + rsi*2] == r9w` short-circuits 1 (the
per-kind expected id); `r9w == 0xFFFF` returns 0. Otherwise
`00322C50(6, r14d)` must hold (and `00309EC0(r9w)` >= 1 when the flag
arg is set), then the `02EBF0F8` pool row `word[+8] * (r14 - 0x1000) +
0020E600([+0xC])` is checked: `byte[rdi+7] >> 5` must equal `esi`, and
mode 1 additionally requires `byte[rdi+9] != 0x12`, `word[r15] !=
0xFFFF`, and a second resolved row's `byte[+0x11] == byte[rdi+9]`.
Finally a `rbp` record: `byte[+5] == 0`, a `02EBF130` row indexed by
`byte[+4]` must pass `bt [rbx], byte[rdi+9]`, and `00323C60(rbp, r14)`
must be nonzero. Interior anchor `00317A18` (the `+7>>5` kind check).

## SWE2-EC7-45 update (2026-09-19) - `00272CE0`

`00272CE0` (251 B) is the spawn-keep caller - `0024ABE0`/`00263990`/`00263A10`/`003588B0`/`00808C40`. Interior anchor `00272CFE` (a `0024ABE0` call).
