---
system: The battle unit (BattleUnit, 0xF50) — a field map from every reached accessor
category: 04-Actor-Entity
status: AUDITED
owner_layer: PrimaryOwner:ActorEntity — the fields belong to the pages that read their writers
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: a typed field scan over every function in functions.tsv, seeded by the unit pool
    *(0208E688)+slot*0xF50 and by the three unit-returning accessors (ActorWork_GetBattleUnit 0031B760,
    ActorWork_GetBattleUnitRaw 00263E30, BattleStats_FindOwningBattleUnit 0031B860), propagated
    through call arguments and record-returning callees for three hops, control the recompute's read
    of +0xE90 (found); every access row is published beside this page in battle-unit-accesses.tsv.
    LIMIT LIFTED (2026-09-11, FZ-16 / FABLE-PUB140) - the earlier bound ("the routes follow the seed
    register only; a callee-saved copy hides the rest of a function") was misdiagnosed: the loss was
    the pop of the first early-return epilogue, which killed every callee-saved register for the rest
    of the function. hop_scan.py generation 3 fixes that and the census now carries the installer
    0023A570's thirty accesses; the N / N cells are re-counted from it. Still linear (address order)
    and still blind to index-register forms and to sub-objects reached through untracked pointers.
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-battle-unit-field-map-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The battle unit — a field map from every reached accessor

> The 3,920-byte battle unit is the object every combat function starts from. Nine of its fields are
> in the type store; a dozen pages name a few more. This page lists every offset any reached function
> touches — ~~163 of them, from 328 functions~~ 168, from 345 functions in the census on disk — with writers and readers, the name a page
> established, and the ~~3206 bytes on 41 ranges~~ 3,174 bytes on 35 ranges that nothing enumerated reaches *(answered: see §2.1 and §2.3, re-counted 2026-09-11; measured on `battle-unit-accesses.tsv`; 2026-10-02, OPUS)*.

## 1. What the player sees

Nothing directly: the unit is the runtime object behind every combatant on the field. What the
player sees is what its fields drive — where the actor stands (`+0xE0`), which spawn record and
stats record it carries (`+0x6A0`, `+0x698`), which group it belongs to (`+0xE98`), and the flag
word that decides whether it is even in play (`+0x00`).

## 2. Native mechanism

### 2.1 How the accessors were found

Three seeds: the pool itself (`*(0208E688) + slot × 0xF50`, [the slot pool](../battleunit-slot-pool-and-actor-class.md)) and the three
functions the engine uses to get a unit from an actor or from a stats record. From each, the
scanner follows the register through `mov` / `lea` / `add`, reports every `[reg + disp]`, queues
callees that receive the pointer in an argument register, and seeds callers of functions that return
it in `rax`; three hops.

| | count |
|---|---|
| access rows | 2203 (758 at a seed, 1445 through propagation; the seeds include the constructor `BattleUnit_ResetStateForReuse` since 2026-09-11) plus the four `sweep` rows of §2.6 — re-run 2026-09-11 with the generation-3 scanner (FZ-16): 1836 → 2203, and the two `+0xBE0` rows retracted (§2.3) |
| functions reached | 342 |
| offsets touched | 168 |
| hottest | `+0x698` (175 r / 2 w), `+0x0` (99 r / 56 w), `+0x10` (71 r / 0 w), `+0x8` (43 r / 2 w), `+0x6A0` (39 r / 2 w), `+0x714` (38 r / 3 w), `+0xEA9` (32 r / 0 w), `+0x4` (10 r / 17 w), `+0x710` (22 r / 5 w), `+0xE68` (21 r / 2 w), `+0xE0` (20 r / 3 w), `+0xE60` (17 r / 2 w) |
| control | `BattleStats_RecomputeDerivedStateAndAutoStatuses` reads `+0xE90` at `003103E0` after `0031B860` — found |

**What the enumeration cannot see:** index-register forms; pointers stored into other objects and
loaded back (the actor record's reverse link at ActorStorageRecord `+0x30`, for one); anything
below the third hop; and — the largest effect here — **sub-objects the unit embeds**: a function
that takes `lea rcx, [unit + 0x298]` and hands it on is reported as one `addr` row at `+0x298` and
nothing inside. The long untouched ranges in §2.3 are where those live.

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: the pool array, the three unit-returning accessors, and — since 2026-09-11 — `BattleUnit_ResetStateForReuse` `00236A60` as a constructor seed (its 55 rows doubled to 110; 45 more writes, no new offsets). `BattleUnit_CommitAction` and the other writers reached through the accessors were already in.
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 The field map

Width is the most common operand size at that offset; "w / r" counts distinct functions.

| offset | width | type | name (source) | w / r | writers | readers |
|---|---|---|---|---|---|---|
| `+0x000` | 8 | u64 | **unitFlags — bit 0 slot in use; bit 21 cleared at bind; bits 33 / 47 the group-completion deferral pair; bit 26 required on the enemy apply path; bit 40 / 49 set by the lifecycle verbs; **bit 36 set while the time-stop registry's battle-side stop set `+0xF18` is non-zero** (`00312130`, 2026-09-12)** ([store](../../_types/fields.tsv); [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §5) | 56 / 99 | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233AFB` +2); `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`0023412D`); `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200` (`002342D3`); +53 more | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233AEE` +2); `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`00233FAB` +2); +97 more |
| `+0x004` | 4 |  | *not named as a whole* — **bit 5 set while the time-stop registry's stop set `+0xF14` is non-zero** (`00238B40`, 2026-09-12, [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §5) | 17 / 10 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236A95` +1); `00238B40` (`00238B52` +1); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FFA38`); +14 more | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`002340F1`); `BattleAction_EvaluateTargetPreviews` `00303830` (`003039D2`); +8 more |
| `+0x008` | 4 | u32 | **actorHandle — the encoded registry handle of the bound actor** ([store](../../_types/fields.tsv)) | 2 / 43 | `00322080` (`003220B9`); `00322050` (`00322073`) | `002392D0` (`00239305` +1); `BattleStats_ModifyHPAndProcessLethalState` `00300530` (`003006DE` +3); +41 more |
| `+0x010` | 8 | ptr | **actorWork — the bound ActorStorageRecord** ([store](../../_types/fields.tsv)) | 0 / 71 |  | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`0023401E` +1); `002F8E90` (`002F8ED5`); +69 more |
| `+0x018` | 8 | ptr | **the definition's text reference (first string of the 5 : 11 text block)** ([page](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)) | 1 / 1 | `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023AC08`, the installer — now in the census, §10.1) | `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0` (`00238EAD`) |
| `+0x024` | 4 |  | *not named by any page* | 2 / 4 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AD4` +1); `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` (`00310DE4`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003024C8` +1); `BattleUnit_CommitAction` `0030F760` (`0030F91B` +5); +2 more |
| `+0x028` | 4 |  | *not named by any page* | 3 / 2 | `BattleUnit_HandleReactionAnimationEvent` `003250F0` (`003251E3`); `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` (`00312FB5`); `00308270` (`00308282`) | `0031ADB0` (`0031B120`); `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` (`00312FAF`) |
| `+0x02C` | 4 |  | *not named by any page* | 5 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AD0` +1); `00328640` (`003286A4` +1); `0032A170` (`0032A1B1` +1); +2 more | `0031ADB0` (`0031AE36`) |
| `+0x030` | 4 | u32 | **the killer id the lethal transition records** ([page](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)) | 3 / 0 | `BattleStats_ModifyHPAndProcessLethalState` `00300530` (`003007E5`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300F4A` +1); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`003012F6`) |  |
| `+0x038` | 8 | ptr | **the per-unit frame callback the world tick calls** ([page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)) | 1 / 2 | `SpawnUnit_SetLaneCandidateTable` `002393E0` (`002393FA`) | `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0` (`0023560C`); `SpawnEntry_GetCandidateUnitId` `00236030` (`00236049`) |
| `+0x040` | 8 | ptr | **the lane map (count at +0, slots from +1) installed by the spawn verbs** ([page](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)) | 1 / 17 | `SpawnUnit_SetEntryMapAndResetTransientEntries` `0023A2E0` (`0023A2FD`) | `Spawn_SelectContinuousEntry` `00235360` (`00235385`); `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0` (`0023561C`); +15 more |
| `+0x048` | 4 | s32 | **the HP floor the HP write honours, and the value its lethal test compares against; zeroed on every apply** ([page](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)) | 2 / 1 | `00239820` (`00239832`, the verb `btlAtelSetHpLowLimit` `3061` through `005105E0`); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023ABDB`, zero) — *corrected 2026-09-11, see §10* | `BattleStats_ModifyHPAndProcessLethalState` `00300530` (`0030056D`) |
| `+0x04C` | 4 |  | *not named by any page* | 1 / 1 | `BattleUnit_SetNativeLifecycleMode` `00238FC0` (`00239006`) | `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` (`0023519C`) |
| `+0x050` | 1 |  | *not named by any page* | 1 / 1 | `BattleUnit_SetNativeLifecycleMode` `00238FC0` (`00238FE1`) | `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` (`00235104` +1) |
| `+0x051` | 1 |  | *not named by any page* | 1 / 1 | `BattleUnit_SetNativeLifecycleMode` `00238FC0` (`0023900B`) | `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` (`0023518A`) |
| `+0x052` | 2 |  | *not named by any page* | 2 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B39` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023AC14`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003021F3`) |
| `+0x054` | 1 |  | *not named by any page* | 3 / 3 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B3D` +1); `00239170` (`00239189`); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023AC18`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`0030329B`); `BattleTarget_MatchesRelationMode` `0030BD00` (`0030BDD1` +5); +1 more |
| `+0x055` | 1 |  | *not named by any page* | 2 / 5 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B35` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023ABF0`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003021CC`); `BattleFormula_BuildEvaluationContext` `003847C0` (`0038487C`); +3 more |
| `+0x056` | 1 |  | *not named by any page* | 1 / 3 | `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023AC11`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003021EC` +1); `002FE950` (`002FE97E`); +1 more |
| `+0x057` | 1 | u8 | **the lane byte, written at bind** ([store](../../_types/fields.tsv)) | 1 / 4 | `SpawnUnit_BindEntryAndMarkCapTracked` `00239840` (`002398A9`) | `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0` (`00235620`); `SpawnEntry_QueryRangeReentryPending` `00236670` (`00236682`); +2 more |
| `+0x058` | 1 | u8 | **runtime category mode (4 sets spawn-record flag bit 5)** ([page](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)). **AND IT IS COPIED ONTO THE ACTOR RECORD** ([page](../Actor-Storage-Record/the-record-behind-every-actor.md)): `BattleUnit_RefreshActorRuntimeFromDefinition` reads it at `00238E0D` and, only when it is **NON-ZERO** (`00238E34`), calls `00269FE0([+0x10], mode)`, which writes the **low nibble of `ActorStorageRecord +0x0E`** (`0026A033`–`0026A03B`). Three consequences a reader of this row would otherwise not reach. **Mode 0 leaves that nibble UNCHANGED rather than writing 0**, because the call is skipped entirely. **The nibble copy runs for EVERY record kind** — `0026A033` is the join point reached both by the kind test failing and by the mode paths — while **only the `+0x1C` bits are kind-gated** on `(byte[+0x03] & 0xE0) == 0x60`, where mode 4 raises bits 8 and 13 (`0026A00C`, `0026A01E`) and any other mode clears both with `& 0xFFFFDEFF` (`0026A003`). **Neither raise is silent**: each is followed by a `00268EA0` notify when `byte[+0x0B] & 8` (`0026A013`, `0026A025`). A null actor record returns without writing anything (`00269FE0`/`00269FE3`) | 2 / 2 | `BattleUnit_SetRuntimeUnitCategoryMode` `002396B0` (`002396D6`); `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0` (`00238DC3` +1) | `BattleUnit_SetRuntimeUnitCategoryMode` `002396B0` (`002396EC`); `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0` (`00238DBD` +2) |
| `+0x05C` | 4 |  | *not named by any page* | 5 / 0 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AF8` +1); `00328640` (`003286B4`); `0032A170` (`0032A1C4`); +2 more |  |
| `+0x060` | 4 |  | *not named by any page* | 1 / 1 | `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` (`00310DEC`) | `BattleUnit_CanAdvanceCombatNavigation` `00325D90` (`00325DC2`) |
| `+0x064` | 4 |  | *not named by any page* | 2 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B41` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023ABD1`) | `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` (`0032497E`) |
| `+0x068` | 4 |  | *not named by any page* | 1 / 1 | `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023AC0C`) | `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` (`00324992` +1) |
| `+0x06C` | 4 |  | *not named by any page* | 2 / 0 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B45` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023ABD6`) |  |
| `+0x070` | 4 |  | *not named by any page* | 3 / 3 | `00329A80` (`00329AD0`); `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450` (`00320492`); `BattleUnit_AddPrimaryResourceRecoveryAccumulator` `00329A20` (`00329A62`) | `00329A80` (`00329ACB`); `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450` (`0032048D`); +1 more |
| `+0x074` | 4 |  | *not named by any page* | 4 / 2 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AF1` +1); `BattleUnit_HandleActionTimelineEvent` `00325260` (`00325646`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300F2E`); +1 more | `BattleUnit_TeardownAndDespawn` `00300E40` (`00300ECB`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`0030129E`) |
| `+0x080` | 0 |  | *not named by any page* | 0 / 8 |  | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`0023406F`); `BattleUnit_ResetStateForReuse` `00236A60` (`00236B12` +1); +6 more |
| `+0x0D0` | 16 |  | *not named by any page* | 3 / 4 | `00311F70` (`00312062`); `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`0023642A`); `BattleUnit_PublishLocomotionPosition` `00300310` (`00300398`) | `BattleLocomotion_ResetPathAndSetTargets` `003291B0` (`003291D9` +3); `BattleUnit_UpdateCombatNavigationStep` `00325BB0` (`00325C02`); +2 more |
| `+0x0D8` | 4 |  | *not named by any page* | 0 / 1 |  | `Navigation_BuildOrReusePathXZ` `00383620` (`0038362B`) |
| `+0x0C0` | 4 |  | *not named by any page* | 1 / 0 | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304BEC`) |  |
| `+0x0E0` | 4 | f32[4] | **the world position copied to the spawn record at release** ([page](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)) | 3 / 20 | `00311F70` (`00312069`); `BattleUnit_PublishLocomotionPosition` `00300310` (`003003A2`); `Actor_GetWorldPosition` `00265020` (`00265043` +1) | `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200` (`0023428A`); `AiOrder_EvaluateTargetSelector` `00301AD0` (`003029FA` +1); +18 more |
| `+0x0E4` | 4 |  | inside `+0xE0` — the world position copied to the spawn record at release | 1 / 6 | `Actor_GetWorldPosition` `00265020` (`00265048` +1) | `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` (`00324A68` +8); `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`002363BC`); +4 more |
| `+0x0E8` | 4 |  | inside `+0xE0` — the world position copied to the spawn record at release | 1 / 10 | `Actor_GetWorldPosition` `00265020` (`0026504E` +1) | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`002363B5`); `Vector3_ComputeXZHeadingOrFallback` `0031AC90` (`0031ACA0` +1); +8 more |
| `+0x0F0` | 4 |  | *not named by any page* | 1 / 2 | `Navigation_SelectNextWaypointXZ` `00383670` (`00383713`) | `BattleLocomotion_BuildSolverContext` `00336710` (`00336757`); `BattleUnit_UpdateCombatNavigationStep` `00325BB0` (`00325C51`) |
| `+0x0F4` | 4 |  | *not named by any page* | 1 / 1 | `Navigation_SelectNextWaypointXZ` `00383670` (`00383721`) | `BattleLocomotion_BuildSolverContext` `00336710` (`0033675D`) |
| `+0x0F8` | 4 |  | *not named by any page* | 1 / 1 | `Navigation_SelectNextWaypointXZ` `00383670` (`00383718`) | `BattleLocomotion_BuildSolverContext` `00336710` (`00336763`) |
| `+0x100` | 4 |  | *not named by any page* | 1 / 3 | `BattleLocomotion_ResetPathAndSetTargets` `003291B0` (`003291E0`) | `BattleLocomotion_BuildSolverContext` `00336710` (`00336770`); `BattleUnit_UpdateCombatNavigationStep` `00325BB0` (`00325C15` +1); +1 more |
| `+0x104` | 4 |  | *not named by any page* | 0 / 1 |  | `BattleLocomotion_BuildSolverContext` `00336710` (`00336779`) |
| `+0x108` | 4 |  | *not named by any page* | 0 / 2 |  | `BattleLocomotion_BuildSolverContext` `00336710` (`00336782`); `Navigation_BuildOrReusePathXZ` `00383620` (`0038364D`) |
| `+0x110` | 4 |  | *not named by any page* | 1 / 1 | `BattleLocomotion_ResetPathAndSetTargets` `003291B0` (`003291F8`) | `BattleLocomotion_BuildSolverContext` `00336710` (`00336792`) |
| `+0x114` | 4 |  | *not named by any page* | 0 / 1 |  | `BattleLocomotion_BuildSolverContext` `00336710` (`0033679B`) |
| `+0x118` | 4 |  | *not named by any page* | 0 / 1 |  | `BattleLocomotion_BuildSolverContext` `00336710` (`003367A4`) |
| `+0x140` | 0 |  | *not named by any page* | 1 / 1 | `BattleLocomotion_SolveAndPublishNextStep` `00336CE0` (`00336DE1`) | `BattleUnit_UpdateCombatNavigationStep` `00325BB0` (`00325D3B`) |
| `+0x144` | 4 |  | *not named by any page* | 1 / 0 | `BattleLocomotion_SolveAndPublishNextStep` `00336CE0` (`00336DEF`) |  |
| `+0x148` | 4 |  | *not named by any page* | 1 / 0 | `BattleLocomotion_SolveAndPublishNextStep` `00336CE0` (`00336DFD`) |  |
| `+0x150` | 4 |  | *not named by any page* | 2 / 0 | `00239E10` (`0023A03F`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304CA0` +1) |  |
| `+0x158` | 4 |  | *not named by any page* | 4 / 1 | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`00236359`); `0033A240` (`0033A334`); `BattleUnit_UpdateCombatNavigationStep` `00325BB0` (`00325D1E` +1); +1 more | `BattleUnit_ApplyMovementIntentToWorldActor` `0023A070` (`0023A0EB`) |
| `+0x15C` | 4 |  | *not named by any page* | 5 / 1 | `00311F70` (`003120A7`); `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`00236328`); `0033A240` (`0033A345`); +2 more | `BattleLocomotion_BuildSolverContext` `00336710` (`003367E1`) |
| `+0x160` | 4 | f32 | **a yaw the party combat stance writes; copied to spawn record +0x74 at release** ([page](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)) | 5 / 7 | `00311F70` (`003120AF`); `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`0023634A`); `0033A240` (`0033A35E`); +2 more | `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200` (`00234295`); `AiOrder_EvaluateTargetSelector` `00301AD0` (`003029EA` +1); +5 more |
| `+0x164` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239ED4`); `003204E0` (`00320560` +2) |
| `+0x168` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239EE6`); `003204E0` (`00320560` +2) |
| `+0x16C` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239E9B`); `003204E0` (`00320560` +2) |
| `+0x170` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239EF8`); `003204E0` (`00320560` +2) |
| `+0x174` | 4 |  | *not named by any page* | 3 / 2 | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`00236339`); `0033A240` (`0033A356`); `BattleLocomotion_SolveAndPublishNextStep` `00336CE0` (`00336DB7`) | `BattleUnit_ApplyMovementIntentToWorldActor` `0023A070` (`0023A0C0`); `BattleLocomotion_BuildSolverContext` `00336710` (`003367ED`) |
| `+0x178` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239E80`); `003204E0` (`00320560` +2) |
| `+0x17C` | 4 |  | *not named by any page* | 2 / 1 | `00239E10` (`00239F6B`); `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`002363FF`) | `00239E10` (`0023A017`) |
| `+0x180` | 4 |  | *not named by any page* | 1 / 3 | `003204E0` (`0032053D` +4) | `00239E10` (`00239E66` +1); `00233A20` (`00233A32` +2); +1 more |
| `+0x184` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239EBA` +1); `003204E0` (`00320560` +2) |
| `+0x188` | 4 | f32 | **the candidate-position y adjustment at activation** ([page](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)) | 1 / 1 | `00239E10` (`0023A026`) | `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` (`0023A4C8`) |
| `+0x18C` | 4 |  | *not named by any page* | 1 / 2 | `FloatPair_CopyToOptionalOutputs` `003DA710` (`003DA717`) | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`002363DA`); `BattleLocomotion_BuildSolverContext` `00336710` (`003367C2`) |
| `+0x190` | 4 |  | *not named by any page* | 1 / 2 | `FloatPair_CopyToOptionalOutputs` `003DA710` (`003DA721`) | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`002363D3`); `BattleLocomotion_BuildSolverContext` `00336710` (`003367CA`) |
| `+0x194` | 4 |  | *not named by any page* | 1 / 0 | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`002363F2`) |  |
| `+0x198` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239F0A`); `003204E0` (`00320560` +2) |
| `+0x19C` | 4 |  | *not named by any page* | 2 / 1 | `00239E10` (`0023A035`); `003057D0` (`00305867`) | `003057D0` (`0030583D`) |
| `+0x1A0` | 4 |  | *not named by any page* | 2 / 0 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031073E`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304A8E` +1) |  |
| `+0x1A4` | 8 |  | *not named by any page* | 2 / 0 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310734`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304A83` +1) |  |
| `+0x1AC` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239F4E`); `003204E0` (`00320560` +2) |
| `+0x1A8` | 4 |  | *not named by any page* | 1 / 0 | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304C0F`) |  |
| `+0x1B0` | 4 |  | *not named by any page* | 1 / 2 | `003204E0` (`0032053D` +4) | `00239E10` (`00239F3C`); `003204E0` (`00320560` +2) |
| `+0x1C0` | 16 |  | *not named by any page* | 1 / 0 | `00329B00` (`00329B40`) |  |
| `+0x1D0` | 4 |  | *not named by any page* | 1 / 1 | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304BE3`) | `BattleLocomotion_BuildSolverContext` `00336710` (`003369B3` +1) |
| `+0x1E0` | 4 |  | *not named by any page* | 1 / 0 | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304BD3`) |  |
| `+0x1F0` | 4 |  | *not named by any page* | 9 / 4 | `002392D0` (`00239320`); `0023A120` (`0023A136` +1); `00329B00` (`00329B33` +1); +6 more | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`0023638E`); `BattleLocomotion_BuildSolverContext` `00336710` (`00336827`); +2 more |
| `+0x1F4` | 1 |  | *not named by any page* | 1 / 2 | `00239E10` (`0023A02E`) | `BattleLocomotion_QueryDynamicActorObstruction` `003357B0` (`0033596E`); `BattleUnit_UpdateCombatNavigationStep` `00325BB0` (`00325C06`) |
| `+0x1F5` | 1 |  | *not named by any page* | 1 / 0 | `00239E10` (`00239F88`) |  |
| `+0x1F6` | 1 |  | *not named by any page* | 1 / 1 | `00239E10` (`00239FD4`) | `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` (`0023A49E`) |
| `+0x1F7` | 1 |  | *not named by any page* | 1 / 1 | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`00236314`) | `BattleLocomotion_BuildSolverContext` `00336710` (`00336805`) |
| `+0x200` | 0 |  | *not named by any page* | 1 / 4 | `Navigation_SelectNextWaypointXZ` `00383670` (`00383700`) | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BF5` +3); `003278D0` (`003278F7`); +2 more |
| `+0x20C` | 2 |  | *not named by any page* | 1 / 1 | `003839C0` (`003839D2`) | `003839C0` (`003839C2` +1) |
| `+0x20E` | 0 |  | *not named by any page* | 0 / 1 |  | `003839C0` (`003839D7`) |
| `+0x210` | 0 |  | *not named by any page* | 1 / 1 | `Navigation_ResetPathPredecessors` `003839F0` (`00383A02`) | `Navigation_ResetPathPredecessors` `003839F0` (`003839F2` +1) |
| `+0x211` | 0 |  | *not named by any page* | 0 / 1 |  | `Navigation_ResetPathPredecessors` `003839F0` (`00383A05`) |
| `+0x290` | 8 |  | *not named by any page* | 0 / 1 |  | `Navigation_SelectNextWaypointXZ` `00383670` (`003836F8`) |
| `+0x690` | 4 |  | *not named by any page* | 6 / 1 | `BattleUnit_HandleActorTimelineEvent` `00319F50` (`0031A031`); `BattleUnit_HandleReactionAnimationEvent` `003250F0` (`003251BE`); `BattleUnit_HandleActionTimelineEvent` `00325260` (`00325695`); +3 more | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304886` +2) |
| `+0x694` | 1 |  | *not named by any page* | 3 / 2 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236A8C` +1); `BattleUnit_ReleaseTargetRelationAndActionState` `00310780` (`00310825`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304B7A`) | `BattleUnit_ReleaseTargetRelationAndActionState` `00310780` (`00310812`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304B6F` +1) |
| `+0x695` | 1 |  | *not named by any page* | 4 / 4 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236A7C` +1); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031061D`); `00308270` (`00308295`); +1 more | `0030CA50` (`0030CA50`); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310611`); +2 more |
| `+0x696` | 1 |  | *not named by any page* | 2 / 2 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310633`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304B9C`) | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310624`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304B91`) |
| `+0x698` | 8 | ptr | **the unit's stats record — kind 0: the BattleSystemState element; kind 1: its SpawnKeep entry `+0x80`; a different record per unit, kind byte at +5** (reworded 2026-09-13 from "one type, two homes") ([page](../Battle-Record-Kind/battle-record-kind-byte.md)); *observed live, [EXP-081](../../_experiments/EXP-081-live-battleunit-bindings.md): kind 0 = block `+8`, kind 1 = spawn `+0x80` on three units* | 2 / 175 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AB4` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023ABFA`) | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233B8F` +2); `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`00233FCC` +2); +173 more |
| `+0x6A0` | 8 | ptr | **the spawn record for kind-1 units, NULL for party** ([page](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)); *observed live ([EXP-081](../../_experiments/EXP-081-live-battleunit-bindings.md)): primary keep entries 0 / 1 / 3, NULL on the party unit* | 2 / 39 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AC9` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023AC01`, the installer — from `SpawnKeep_ResolvePrimaryEntry` `00236100(unit+0x40, s8 unit+0x57)`, null-tested at `0023A77E`) | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233BA1`); `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200` (`0023427E`); +37 more |
| `+0x6B0` | 4 | u32 | **bit 0 set by the party combat stance entry** ([page](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)); **bit 1 = a command issued and not yet committed** — set by `BattleUnit_IssueCommand` `00311CF0` (`00311D81` clears, `00311D8C` sets), cleared by `BattleUnit_CommitAction` when it finds it set (`0030F865`–`0030F872`) and by the same five action-state resets that clear entry 0's bit 10 (`00300EB7`, `003001A5`, `003011EE`, `0030B008`, `002FFA22`); bit 0 also set at `00312F33` | 9 / 4 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B9D` +1); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FFA22`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300EB7`); +6 more | `BattleUnit_ReleaseTargetRelationAndActionState` `00310780` (`0031081E`); `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F04A` +2); +2 more |
| `+0x6B4` | 1 | u8 | **the action phase (literals 2, 5, 9 by the action code)** ([page](../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md)). *Census 2026-09-12 (every `[reg + 0x6B4]` access, and every store at `+0x6B0`–`+0x6B3`):* stores are only **0** at commit (`0030F814`, `esi` zeroed at `0030F796`) and at the reset, **2** by the direct-state order arms (`002FDE50`… and `002FE8F6`, `002FE932`, each when the byte is 0), **4** by `00300060` after it releases the presentation slot of a unit whose byte is 6 or 7 and whose action definition has `+0x0C` bit 30, **5** by the combo continue and the engage auto-attack, and **`inc`** in three order handlers (`002FDA60`, `002FDC30`, `002FE840`). Readers compare 0, 3, 6, 6–7 and ≥ 9. ~~How an ordinary committed action reaches 6–9 is not in any displacement store — asked live, `FABLE-REQ-ASTRA-ACTION-PHASE`~~ *Corrected 2026-09-14 (FABLE, UQ-108): `BattleUnit_AdvanceStandardActionState` advances it through 16 `inc byte [rsi + 4]` sites with `rsi = unit + 0x6B0` (`0030487F`), the advances of a 13-phase machine (0–12) whose arms fall through; the census searched `[reg + 0x6B4]` only, and the live question is no longer needed* | 5 / 9 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`003106F2`); `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` (`003130F2`); `BattleAction_TryContinueComboSequence` `0030FA00` (`0030FA80`); +2 more | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF9B5`); `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E78A`); +7 more |
| `+0x6B5` | 1 |  | *not named by any page* | 1 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BA3` +1) | `BattleUnit_SelectAndCommitNextAction` `00305AB0` (`00305C34`) |
| `+0x6B6` | 1 |  | *not named by any page* | 3 / 5 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031060A`); `Battle_ProcessActionTarget` `00307300` (`0030744B`); `BattleUnit_CommitAction` `0030F760` (`0030F894`) | `0030C0E0` (`0030C149`); `BattleFormula_EvaluateTargetPreview` `00385680` (`00385735`); +3 more |
| `+0x6B7` | 1 | u8 | **combo progress; cleared with `+0x6B8` in one word store at `003106EB`** ([page](../../07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md)) | 2 / 4 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`003106EB`); `BattleAction_TryContinueComboSequence` `0030FA00` (`0030FA79`) | `BattleFormula_EvaluateTargetPreview` `00385680` (`003857C6`); `BattleFormula_RollAndStoreComboCount` `00388660` (`0038868A`); +2 more |
| `+0x6B8` | 1 | u8 | **saved and restored across the combo continue, cleared with `+0x6B7`** ([page](../../07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md)) | 2 / 2 | `BattleAction_TryContinueComboSequence` `0030FA00` (`0030FA65`); `Battle_ProcessActionTarget` `00307300` (`00307665`) | `BattleAction_TryContinueComboSequence` `0030FA00` (`0030FA19`); `Battle_ProcessActionTarget` `00307300` (`0030765C`) |
| `+0x6B9` | 1 |  | *not named by any page* | 1 / 4 | `BattleUnit_CommitAction` `0030F760` (`0030F88E`) | `BattleFormula_EvaluateTargetPreview` `00385680` (`00385756`); `004698C0` (`00469924`); +2 more |
| `+0x6C0` | 16 |  | *not named by any page* | 1 / 1 | `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (`0030EDCF`) | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F06B`) |
| `+0x6D0` | 4 |  | *not named by any page* | 4 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BA9` +1); `00238AB0` (`00238AC6`); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031070E`); +1 more | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F073`) |
| `+0x6D4` | 4 |  | *not named by any page* | 2 / 1 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031074B`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304AAF`) | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304A7F` +1) |
| `+0x6D8` | 8 |  | *not named by any page* | 2 / 1 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310707` +1); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304A99`) | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304A8A` +1) |
| `+0x6DC` | 4 |  | *not named by any page* | 1 / 1 | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304AAC`) | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304A95` +1) |
| `+0x6E0` | 8 |  | *not named by any page* | 4 / 2 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BC4` +1); `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` `00239040` (`00239081` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023A95E` +1); +1 more | `BattleUnit_SelectAndCommitNextAction` `00305AB0` (`00305C3E`); `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F07B`) |
| `+0x6E8` | 8 |  | *not named by any page* | 3 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BBD` +1); `0030F2D0` (`0030F331`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`0030126B`) | `BattleUnit_SelectAndCommitNextAction` `00305AB0` (`00305B95`) |
| `+0x6F0` | 8 |  | *not named by any page* | 3 / 2 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BB6` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023ABB5`); `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (`0030EDE7`) | `BattleUnit_SelectAndCommitNextAction` `00305AB0` (`00305C61`); `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F083`) |
| `+0x6F8` | 8 |  | *not named by any page* | 7 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BAF` +1); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF9CC`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300E68`); +4 more | `BattleUnit_SelectAndCommitNextAction` `00305AB0` (`00305C05`) |
| `+0x700` | 4 | u32 | **action block head: bits 0–1 masked at commit (`0030F7F2`); the 16 bytes from here are copied to `+0x718` at commit (`0030F80D`–`0030F823`)** ([page](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)) | 4 / 4 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`003106C5`); `Battle_ProcessActionTargetEntry` `003191B0` (`003192BC`); `BattleUnit_CommitAction` `0030F760` (`0030F7F2`); +1 more | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B5C` +1); `Battle_ProcessActionTargetEntry` `003191B0` (`00319241`); +2 more |
| `+0x708` | 8 | ~~ptr~~ `AiOrderRecord*` | **the action context — `-1` / non-zero gates "an action is in progress"; written by `BattleUnit_CommitAction` (`0030F7F9`), cleared by `BattleUnit_CancelAndResetCurrentAction` (`00310722`)** *— typed 2026-09-29 (SWE2-DATA, from OPUS `4e8e01efd`, [`battleunit-order-record-opus`](../../_index/candidates/battleunit-order-record-opus/README.md), `order_record.py` FAILS 0): the **committed order record**. `CommitAction`'s five callers pass a gambit set's record (`set + 0x20 + 0x18k`), the unit's own `+0xBA0`, the static records `01EEC298` / `01EEC2B0`, or `+0x708` itself; BattleUnit bodies read its `+2` (signed word), its `+4` flag bits `0x2000` / `0x200` / `0x100` / `4` / sign, and its `+6` through this pointer* ([page](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)) | 3 / 12 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B48` +1); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310722`); `BattleUnit_CommitAction` `0030F760` (`0030F7F9`) | `WorldActor_HasActiveBattleActionOrUnitFlag14` `0030BA30` (`0030BA54`); `BattleUnit_UpdateCombatFrame` `00308610` (`0030868B` +1); +10 more |
| `+0x710` | 4 | u32 | **the target focus handle (resolved by `BattleUnit_ResolveByFocusHandle`, `0031B7E0` — the decode contract on [the slot-pool page](../battleunit-slot-pool-and-actor-class.md) §11); written at commit (`0030F800`), cleared at cancel (`00310729`)** ([page](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)) | 5 / 22 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B4F` +1); `00328640` (`0032869E`); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310729`); +2 more | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B6A` +1); `AiOrder_EvaluateTargetSelector` `00301AD0` (`00302A84` +3); +20 more |
| `+0x714` | 2 | u16 | **the action id; written at commit (`0030F806`), cleared at cancel (`0031071B`)** ([page](../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md)) | 3 / 38 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B55` +1); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031071B`); `BattleUnit_CommitAction` `0030F760` (`0030F806`) | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF9A3`); `AiOrder_EvaluateTargetSelector` `00301AD0` (`003030C8` +2); +36 more |
| `+0x718` | 16 | u8[16] | **a copy of the action block `+0x700`–`+0x70F` taken right after the commit stores (`0030F80D`, `0030F823`)** ([page](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)) | 3 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B80` +1); `BattleUnit_UpdateCombatFrame` `00308610` (`00308762`); `BattleUnit_CommitAction` `0030F760` (`0030F823`) | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`003106B9`) |
| `+0x720` | 16 |  | *not named by any page* | 1 / 1 | `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (`0030EDFF`) | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F09B`) |
| `+0x728` | 8 |  | *not named by any page* | 2 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B95` +1); `BattleUnit_CommitAction` `0030F760` (`0030F82A`) | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`003106CC`) |
| `+0x730` | 16 | u8[16] | **the cancelled action's record: `+0x718`–`+0x727` copied here by `BattleUnit_CancelAndResetCurrentAction` (`003106B9` → `003106D7`) — its flags and `actionData`** ([commit page](../../07-Combat-Action/the-moment-an-action-is-committed.md), the cancellation section) | 3 / 2 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B72` +1); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`003106D7`); `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (~~`0030EE13`~~ `0030EDC7` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB30; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*) | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F060` +1); `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (`0030EDB6`) |
| `+0x738` | 8 |  | *not named by any page* | 0 / 1 |  | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304989`) |
| `+0x740` | 8 | u32 + u16 | **the cancelled action's `targetId` (`+0x740`) and `actionId` (`+0x744`)** — `+0x728`–`+0x72F` copied by the cancel (`003106CC` → `003106E3`); the next commit compares its own target and id against them for the queued-repeat drop (`0030F84E`–`0030F857`) | 3 / 3 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B8D` +1); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`003106E3`); `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (~~`0030EE1A`~~ `0030EDCF` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB40; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*) | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (~~`0030F0B5`~~ `0030F06B` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB40; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*); `BattleUnit_CommitAction` `0030F760` (`0030F857`); +1 more |
| `+0x744` | 2 | u16 | **the cancelled action's `actionId`** (the high half of the `+0x740` copy; read by `BattleUnit_CommitAction` at `0030F84E`) | 0 / 2 |  | `BattleUnit_CommitAction` `0030F760` (`0030F84E`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304ADE` +1) |
| `+0x748` | 4 |  | *not named by any page* | 7 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BD2` +1); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF9D3`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300E6F`); +4 more | `BattleTarget_MatchesRelationMode` `0030BD00` (`0030BE2A`) |
| `+0x74C` | 4 |  | *not named by any page* | 5 / 0 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FFA31`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300EC5`); `BattleUnit_ResetActionControlForStatusTransition` `00300140` (`003001B3`); +2 more |  |
| `+0x750` | 8 |  | *not named by any page* | 9 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BCB` +1); `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FFA2A`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300EBE`); +6 more | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (~~`0030F0BD`~~ `0030F073` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB50; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*) |
| `+0x754` | 4 |  | *not named by any page* | 1 / 1 | `BattleUnit_CommitAction` `0030F760` (`0030F920` +3) | `00305E70` (`00305EF6`) |
| `+0x758` | 2 |  | *not named by any page* | 1 / 0 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BD9` +1) |  |
| `+0x75C` | 4 |  | *not named by any page* | 2 / 1 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310715`); `BattleUnit_AdvanceActionState` `00307BE0` (`00307C35`) | `BattleAction_CheckAndHandleExecutionTimeout` `0030AF30` (`0030AF67` +1) |
| `+0x760` | 8 |  | *not named by any page* | 4 / 2 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B87` +1); `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310700`); `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (~~`0030EE2A`~~ `0030EDDF` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB60; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*); +1 more | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (~~`0030F0C5`~~ `0030F07B` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB60; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304A20`) |
| `+0x764` | 8 |  | *not named by any page* | 2 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B79` +1); `BattleUnit_AdvanceStandardActionState` `00304850` (`003049E5`) | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304A1A`) |
| `+0x768` | 8 |  | *not named by any page* | 2 / 2 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`003106F9`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304AF6` +1) | `BattleUnit_AdvanceActionState` `00307BE0` (`00307C2D`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304B11` +2) |
| `+0x76C` | 8 |  | *not named by any page* | 2 / 2 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B63` +1); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304B0B`) | `BattleUnit_AdvanceActionState` `00307BE0` (`00307C27`); `BattleUnit_AdvanceStandardActionState` `00304850` (`00304CDD`) |
| `+0x770` | 4 |  | *not named by any page* | 8 / 3 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF9DA`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300E75`); `BattleUnit_ResetActionControlForStatusTransition` `00300140` (`00300163`); +5 more | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (~~`0030F0CD`~~ `0030F083` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB70; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*); `BattleUnit_CommitAction` `0030F760` (`0030F832`); +1 more |
| `+0x774` | 4 |  | *not named by any page* | 2 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BE6` +1); `00319420` (`00319441`) | `00319420` (`00319429`) *(2026-09-30, SWE2-DATA, [GR-17 residue record](../../_index/candidates/gr17-effect-residue-0930/README.md): a third writer, `0032A045` in `00329F80`, stores the one real effect handle - the unit's action-charge effect)* |
| `+0x778` | 0 | u8 | **`BattleTargetBuffer` `+0` — the header byte; bit 0 survives the reset** (`BattleTargetBuffer_ResetPreservingFlag0` `00316CF0`: `movzx` at `00316CFA`, `memset(0x208)` at `00316D0B`, re-OR at `00316D16`). The whole 0x208-byte buffer sits here — every `lea … +0x778` in this table hands it to the helpers (§2.4) | 1 / 6 | `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0` (`00316D10` +1) | `BattleStats_ModifyHPAndProcessLethalState` `00300530` (`00300704`); `BattleUnit_HandleActorTimelineEvent` `00319F50` (`00319FD8` +1); +4 more |
| `+0x779` | 2 | u16 | **buffer `+1` — the word the reset zeroes** (`00316D1D`); no other route touches it | 1 / 0 | `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0` (`00316D1D`) |  |
| `+0x77C` | 4 | i32 | **`BattleTargetBuffer.count`** — live entries, at most 32 (`00316CD4` refuses at `0x20`, `00316CE1` increments); the walkers bound on it (`0031B40A`, `003227B9`, `003192C9`, `003254CC`) | 1 / 11 | `BattleTargetBuffer_TryAppendActorWork` `00316CD0` (`00316CE1`) | `0031ADB0` (`0031B40A` +1); `00322760` (`003227B9`); +9 more |
| `+0x780` | 8 | ptr | **`entries[0].actor`** — the first of 32 sixteen-byte entries (`+0x780`–`+0x97F`): the `ActorWork*` `BattleTargetBuffer_TryAppendActorWork` `00316CD0` stores at `[buf + (2·count)·8 + 8]` (`00316CD9`–`00316CDC`, stride 16). The non-indexed `cmp qword [unit+0x780], 0` (`0030C03B`, `00308786`) asks whether there is a first target | 2 / 11 | `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (~~`0030EE3A`~~ `0030EDEF` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB80; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*); `BattleTargetBuffer_TryAppendActorWork` `00316CD0` (`00316CDC`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003033A4`); `0031ADB0` (`0031B41E` +3); +9 more |
| `+0x788` | 4 | u32 | **`entries[0].outcome`** — the first entry's outcome word: byte 0 the target-entry code (`BattleFormula_MapOutcomeToTargetEntryCode` `0030DAE0` → `003075BF`), bits 8 / 9 / 10 = **knockback rolled / parry rolled / the combo continues** (the resolved result's flag word B bits 3 / 2 / 1 — [the scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.4) and bit 11 a caller mask (`Battle_ProcessActionTarget` `00307300`, `003075CB`–`003075F9`). The five `and … 0xFFFFFBFF` writers clear **bit 10 of entry 0 only** — an index folded into the displacement, not a separate field (§2.4) | 5 / 7 | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FFA14`); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300EAD`); `BattleUnit_ResetActionControlForStatusTransition` `00300140` (`0030019B`); +2 more | `BattleStats_ModifyHPAndProcessLethalState` `00300530` (`0030071A`); `0031ADB0` (`0031B44F` +6); +5 more |
| `+0x790` | 16 | ptr | **`entries[1].actor`** — ~~reached by immediate displacement only inside the snapshot's block copy (`0030F0DD`; `+0x6B0` for `0x4F0` bytes)~~ reached only through the suspend / restore block copy's loop body (`0030F093` read, `0030EDF7` write, on the pass whose pointer sits at `+0x7B0`; the copy covers `+0x6B0` for `0x4F0` bytes) *(corrected 2026-10-03, OPUS: `0030F0DD` is the loop tail and reads `+0xB90`; SWE2-STRUCT's loop attribution)*; entries 1–31 are otherwise reached by index | 1 / 1 | `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (~~`0030EE44`~~ `0030EDF7` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB90; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*) | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (~~`0030F0DD`~~ `0030F093` *(corrected 2026-10-03, OPUS, from SWE2-STRUCT's loop attribution: the tail site addresses +0xB90; this offset is reached by the loop body on the pass whose pointer sits at `+0x7B0`)*) |
| `+0x988` | 8 |  | *not named by any page* | 1 / 2 | `BattleAction_EvaluateTargetPreviewRecursive` `00303A00` (`00303B9D`) | `00322760` (`0032281A`); `Battle_ProcessActionTargetEntry` `003191B0` (`0031930C` +1) |
| `+0xB88` | 8 |  | *not named by any page* | 1 / 1 | `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F0F1`) | `BattleUnit_RestoreSuspendedActionState` `0030EDA0` (`0030EDA0`) |
| `+0xB90` | 4 |  | *not named by any page* | 1 / 0 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236BE0` +1) | *(2026-09-30, SWE2-DATA, [GR-7 record](../../_index/candidates/gr7-kind10-reader-0930/README.md): operand-store kind 10 - also written at `00329F29` (the operand-store writer's case-10 arm, from `00312170` and `002FE660`) and read at `0032127C` (from `00301AD0`), indexed forms this census does not type)* |
| `+0xBA0` | 2 |  | *not named by any page* | 0 / 6 |  | `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` (`002FF9EF` +1); `BattleUnit_TeardownAndDespawn` `00300E40` (`00300E8A` +1); +4 more |
| `+0xBB8` | 4 |  | *not named by any page* | 0 / 1 |  | `BattleUnit_SelectAndCommitNextAction` `00305AB0` (`00305B12`) |
| `+0xBC0` | 1 |  | *not named by any page* | 3 / 5 | `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` (`00324872` +2); `00316D30` (`00316D3A` +2); `BattlePerception_RefreshCandidateCacheGeneration` `00324F20` (`00324FED` +1) | `BattleUnit_ResetStateForReuse` `00236A60` (`00236A85` +1); `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` (`00324857` +1); +3 more |
| `+0xBC1` | 2 |  | *not named by any page* | 3 / 0 | `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` (`0032487C`); `00316D30` (`00316D60`); `BattlePerception_RefreshCandidateCacheGeneration` `00324F20` (`00324FF7`) |  |
| `+0xBC4` | 4 | i32 | **the perception candidate cache's count** — entries at `+0xBC8`, rebuilt by `BattleUnit_RebuildPerceptionCandidateCache`; walked by the tick's out-of-combat regeneration (stage 5), the enmity propagation and the target selector ([the periodic tick](../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md) §13) | 2 / 6 | `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` (`00324EBB`); `BattlePerception_RefreshCandidateCacheGeneration` `00324F20` (`0032503C`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003025BC` +4); `BattleEnmity_PropagateToPerceivingFoes` `003219D0` (`00321A82` +1); +4 more |
| `+0xBC8` | 8 | ptr[] | **the perception candidate cache** — 16-byte entries, the perceived actor's work pointer at `+0` (`ActorWork_GetBattleUnitRaw` resolves it), count at `+0xBC4` (same page) | 2 / 5 | `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` (`00324EB3`); `BattlePerception_RefreshCandidateCacheGeneration` `00324F20` (`00325037`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`003025CD` +3); `BattleEnmity_PropagateToPerceivingFoes` `003219D0` (`00321A9A` +3); +3 more |
| `+0xDC8` | 2 | u16 | **the reserved consumed item** (`0xFFFF` = none): `BattleAction_PrepareExecutionResources` `0030EF20` stores the action row's `+0x22` when its `+0x1E` is 3 and removes the item (`0030EF79`–`0030EFB0`); `BattleAction_RefundReservedExecutionResources` `00300280` gives it back and resets `0xFFFF` (`003002A5`–`003002D0`); `BattleUnit_TryCommitEngageAutoAttack` stashes it per slot (`003130AB`) and `00308270` restores it (`003082B2`) ([the spend side](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) §2) | 5 / 3 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AFC` +1); `00308270` (`003082B2`); `BattleAction_RefundReservedExecutionResources` `00300280` (`003002D0`); +2 more | `003037A0` (`003037F9`); `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` (`003130AB`); +1 more |
| `+0xDCC` | 4 |  | *not named by any page* | 5 / 2 | `0030F2D0` (`0030F318`); `00307C70` (`00307CC7`); `BattleUnit_UpdateEngagementStateFlag` `00307D10` (`00307D7C`); +2 more | `BattleUnit_ComputePartyBattleStance` `00308130` (`003081B2`); `BattleUnit_SeedPartyCombatStanceRecheckTimer` `003081E0` (`003081F1`) |
| `+0xDD0` | 4 |  | *not named by any page* | 2 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AEB` +1); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`003012DB`) | `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` (`00310DF4`) |
| `+0xDD4` | 0 |  | *not named by any page* | 0 / 1 |  | `003176C0` (`003176C5` +1) |
| `+0xE54` | 4 | u32 | **the gil amount the target preview computed** — the preview record's `+0x08`, copied by `BattleAction_EvaluateTargetPreviews` (`00303954`) and `…Recursive` (`00303B2E`) right after `004698C0` posts the not-enough-gil notice, and deducted by `BattleAction_ConsumeExecutionResources` (`00305712`–`0030572B`); non-zero for recipe 61 (action `0xB5`, the gil throw — [the recipes page](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.6); reset with the unit (`00236AE5`) | 3 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AE5` +1); `BattleAction_EvaluateTargetPreviews` `00303830` (`00303954`); `BattleAction_EvaluateTargetPreviewRecursive` `00303A00` (`00303B2E`) | `BattleAction_ConsumeExecutionResources` `00305640` (`00305712`) |
| `+0xE58` | 4 | u32 | **the reserved gil cost** of the pending action: `BattleAction_ComputeGilCost` `00309060`'s result, stored and deducted by `BattleAction_PrepareExecutionResources` `0030EF20` (`0030EFC0`–`0030EFD8`), compared by the availability check (`00303C8F`), refunded and zeroed by `BattleAction_RefundReservedExecutionResources` `00300280` (`003002D7`–`003002F5`); with `+0xDC8` it forms the 12-byte per-slot stash at `022C1DB0` (`{u16 item, u32 gil}` at `slotIndex × 12`) that `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` fills before `BattleUnit_CommitAction` (`00313088`–`003130C7`) and `00308270` restores (`0030829C`–`003082C0`) | 4 / 2 | `00308270` (`003082C0`); `BattleAction_RefundReservedExecutionResources` `00300280` (`003002F5`); `BattleAction_ConsumeExecutionResources` `00305640` (`003056B3`); +1 more | `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` (`003130C1`); `BattleAction_RefundReservedExecutionResources` `00300280` (`003002D7`) |
| `+0xE60` | 8 | ptr | **the definition row (enemy table 02EBF120 or party table 02EBF130)** ([page](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)); *observed live ([EXP-081](../../_experiments/EXP-081-live-battleunit-bindings.md)): enemy rows 6 / 5 / 0, party row 0* | 2 / 17 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236ABB` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023A915` +1) | `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` `00239040` (`0023906C`); `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` (`0023A433`); +15 more |
| `+0xE68` | 8 | ptr | ~~the spawn record's +0x80 stats page (enemy path only)~~ **CORRECTED 2026-09-12 (FABLE): the `.ard` slot-0 class row** (*observed live, [EXP-081](../../_experiments/EXP-081-live-battleunit-bindings.md): class rows 4 / 3 / 0 = the enemy rows' u16 `+0`, outside both keep banks; 0 on the party unit*) (which answers AL-7: `+0x698` and `+0xE68` are two different objects — the stats record and the class row — not one record at two homes, so no reader treats them interchangeably and the `+0x698` census is not under-counting) (84 B, `02EBF150`) selected by the spawn row's word `+0x00` — `r15 = base + stride × word` at `0023A6F0`–`0023A6FC`, stored at `0023A91C` before `r15` is reloaded with the page for `+0x698`; its `+5` is the unit's type byte (`+0x56`), `+0x28` bit 1 the "does not chain" flag and `+0x40` the model id ([the chain page](../../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md) §8b; [the area-file loader](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)) ([page](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)) | 2 / 21 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AC2` +1); `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023A91C`) | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`00234054`); `0031E880` (`0031E933`); +19 more |
| `+0xE70` | 8 | ptr | **the reward base row** — ard slot 5 (`02EBF148`) selected by the enemy row's `+0x22`: word `+0` counter-`0x11` points, byte `+0x2F` LP, dword `+0x30` gil, dword `+0x34` experience ([the unit-definition page](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §7, FB-5) | 1 / 4 | `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023A9A5`) | `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` (`0031253F`); `Reward_ComputeExperienceForRecipient` `002F8BB0` (`002F8C7E` +1); +2 more |
| `+0xE78` | 8 | ptr | **the per-level reward row** — ard slot 6 (`02EBF140`) selected by the enemy row's `+0x24`, the same four offsets multiplied by `level − stats +0x88`; its LP byte is 0 on every shipped row (same page) | 1 / 4 | `BattleUnit_ApplyUnitDefinition` `0023A570` (`0023A9F4`) | `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` (`00312534`); `Reward_ComputeExperienceForRecipient` `002F8BB0` (`002F8C73` +1); +2 more |
| `+0xE80` | 8 | u8[16] | **the innate augment source, from btlAtelSetAbility (bit-reversed halves)** ([page](../../08-Combat-Formula/the-auto-status-rebuild.md)) | 2 / 0 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B21` +1); `002390B0` (`002390D8`) |  |
| `+0xE88` | 8 |  | inside `+0xE80` — the innate augment source, from btlAtelSetAbility (bit-reversed halves) | 2 / 0 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B2E` +1); `002390B0` (`002390DF`) |  |
| `+0xE90` | 4 | u32 | **code-3 status immunities from btlAtelSetStatus, installed into `+0x38` by the recompute's mode-5 pass** ([page](../../08-Combat-Formula/the-auto-status-rebuild.md)) | 2 / 1 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236B19` +1); `002394C0` (`002394FC` +1) | `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (`003103E0`) |
| `+0xE98` | 1 | u8 | **spawnGroupId — 1-based group id; 0 = none** ([store](../../_types/fields.tsv)) | 0 / 4 |  | `00233EA0` (`00233F0B`); `SpawnGroup_UpdateExpectedMemberLaneMask` `00306E60` (`00306E8F`); +2 more |
| `+0xE99` | 1 | u8 | **spawnGroupMode — bits 0 / 1** ([store](../../_types/fields.tsv)) | 1 / 2 | `SpawnGroup_ConfigureUnitMembershipAndMode` `00239710` (`00239766`) | `BattleUnit_TeardownAndDespawn` `00300E40` (`00300F89`); `SpawnGroup_RecordMemberDeathAndHandleCompletion` `00306F00` (`00306FB6`) |
| `+0xE9A` | 1 | u8 | **bit 0 / bit 1: status 8 / 2 applied by a party-side source**; bit 2: the result carries flag C bit 14 — **a Poison beat**, the only writer of that flag being `00386C70` — set inside that flag's block whether or not sound `0x34` resolves (`003113BF`; wording corrected 2026-09-12); bit 3: the result's flag A bit 19 — taken, not struck (`0031138D`) ([page](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)) | 2 / 1 | `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` (`0030E7C9` +3); `BattleFormula_ApplyTargetResult` `003112F0` (`0031138D` +2) | `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` (`003122F4`) |
| `+0xE9C` | 4 |  | *not named by any page* | 1 / 1 | `002392D0` (`0023932A` +1) | `003229A0` (`003229C4`) |
| `+0xEA0` | 4 |  | *not named by any page* | 1 / 1 | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031069C` +1) | `BattleUnit_TeardownAndDespawn` `00300E40` (`00300EEE`) |
| `+0xEA4` | 4 |  | *not named by any page* | 3 / 3 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236ADF` +1); `00322080` (`003220A3`); `00322050` (`00322059`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00301D7D` +1); `AiOrder_ComputeBoundedSelectorScalar` `00308C20` (`00308D10`); +1 more |
| `+0xEA8` | 1 |  | *not named by any page* | 3 / 2 | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AD8` +1); `00322080` (`003220AD`); `00322050` (`00322063`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00301E95` +1); `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` (`0038698C`) |
| `+0xEA9` | 1 | u8 | **slotIndex — the slot's own index in the pool** ([store](../../_types/fields.tsv)) | 0 / 32 |  | `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400` (`002F945A` +1); `002FA290` (`002FA2F0` +5); +30 more |
| `+0xEAC` | 4 |  | *not named by any page* | 2 / 1 | `002FE950` (`002FE9D3` +1); `002FEAB0` (`002FEAB2`) | `002FE950` (`002FE9DD`) |
| `+0xEB0` | 4 |  | *not named by any page* | 1 / 1 | `002FE950` (`002FE9CD`) | `002FE950` (`002FE9C5` +1) |

### 2.3 What nobody reaches

35 ranges totalling 3174 bytes have no access on any enumerated route (re-counted 2026-09-11
from the generation-3 census; an access covers its operand width, an `addr` row its first byte). The
ones of 64 bytes or more: `+0x212`–`+0x28F` (126 B), `+0x298`–`+0x68F` (1016 B) *(2026-09-26: reached by index — the waypoint table, `FF-2`)*, `+0x7A0`–`+0x987`
(488 B), `+0x990`–`+0xB87` (504 B), `+0xBD0`–`+0xDC7` (504 B — the `+0xBE0` rows that split this
range were wrong, see below), `+0xDD8`–`+0xE53` (124 B), `+0xEB4`–`+0xF4F` (156 B). The former
`+0x81`–`+0xCF` (79 B) fell below the threshold: `+0xC0` is now reached, leaving `+0x81`–`+0xBF`
(63 B) and `+0xC4`–`+0xCF` (12 B). By the scan's own limits these are the candidates for embedded
sub-objects addressed through a pointer the scan does not follow, not evidence of unused space.
One of them is now read: `+0x7A0`–`+0x987` is entries 2–31 of the target buffer (§2.4), reached
only by index.

> **Retracted 2026-09-11 (FABLE-PUB140): the `+0xBE0` row.** The two accesses filed there
> (`AiOrder_EvaluateTargetSelector` `003026E1` / `0030326C`, `movups xmm0, [rbx + r8 + 8]`) are not
> unit accesses: `rbx` is the selector index shifted left by four, reloaded from `[rsp+0x28]` where
> `00301E19` stored it, and `r8` is the table pointer at `[rsp+0x140]`. The generation-2 scanner
> exempted every frame reload as a "restore" and kept `rbx` as the ledger cursor `unit+0xBD8` it had
> been inside the loop; the row was **wrong, not missing**. No store row existed for it.

### 2.4 What the map says that no single page did

- **`+0x00` has 38 writers and 81 readers** — the flag word is the most written field on the unit;
  every one of the writers is a candidate for a bit-level table the store's row only begins.
- **`+0x698` is read by 151 functions and written by one** (the installer): the stats record is the
  unit's face to the combat engine, and the unit-side accessors almost never touch the stats
  through anything else.
- **`+0x4` has 12 writers** against 7 readers, and the action-state trio `+0x708` / `+0x710` /
  `+0x714` (the context, the target focus, the action id — named by the 07 pages) is written by
  `BattleUnit_CommitAction` and cleared by `BattleUnit_CancelAndResetCurrentAction` and the reset,
  and read from 4 / 17 / 25 places.
- **`+0x5C` is written by five functions and read by none the enumeration reaches.**
- **`+0x778`–`+0x97F` is one object, the `BattleTargetBuffer`** (resolved 2026-09-11,
  OPUS-CONTRA-BUTARGET): a header byte, a zeroed word, a count at `+0x77C` and 32 entries of 16
  bytes from `+0x780` — `{ActorWork* actor; u32 outcome; u32 unused}`. The contradiction was an
  index folded into a displacement: `and dword [unit+0x788], ~0x400` in the five resets and
  `test dword [unit+0x788], 0x400` in the combo gate (`BattleUnit_UpdateCombatFrame` `00308610` at
  `00308790` before `BattleAction_TryContinueComboSequence` `0030FA00`, whose predicate `0030C010`
  repeats it at `0030C045`) address **entry 0's outcome word** — the primary target — exactly as
  `mov r13d, [unit + (2·idx)·8 + 0x788]` (`0030071A`) addresses entry *idx*'s. Every entry's
  outcome is written by one function, `Battle_ProcessActionTarget` `00307300`, through the entry
  pointer it receives in `r9` (`[r14+8]`: the code byte at `003075BF`; bits 8 / 10 / 9 / 11 at
  `003075CB` / `003075E0` / `003075EC` / `003075F9` from the local result's `+0x18` bits 3 / 1 / 2
  and ~~the caller's `r12b` mask~~ bit 0 (`r12b` is the constant 1, `FT-4`); bit 10 is withheld when the target unit's `+0x4` has bit 21,
  `003075D7`); nothing writes an outcome word through the unit base. `Battle_ProcessActionTargetEntry`
  `003191B0` finds that entry by walking `+0x780` (`003192C9`–`003192F0`). The buffer is
  block-copied with the rest of `+0x6B0`–`+0xB9F` by `BattleUnit_SnapshotAndSuspendActionState`
  `0030EFF0`, **restored wholesale** by `00309990` (`003099E1`–`00309A46`: 4 × 0x80 + 8 bytes from a
  static image, `lea` at `003099E8`) and rebuilt through its own pointer by
  `BattleAction_ResolveSpecialSequenceTargets` `0030EC00` (`0030ED1B` / `0030ED2F`).
- **`+0x6B0` bit 1 is the issued-not-committed mark** (see the row) — the same five resets clear
  it beside entry 0's bit 10.

### 2.5 The flag word, bit by bit — 2026-09-10 (FABLE-UNITBITS1)

Every `or` / `and` / `bts` / `btr` / `test` / `bt` with an immediate on `+0x00` (low dword or
qword) or `+0x04` (the high dword, bits 32–63) in the access table, decoded per bit. Register-mask
sites (a `movabs` mask applied through a register) are not decodable from the table alone; the
ones the pages have read are added below it.

| bit | mask | set by | cleared by | tested by |
|---|---|---|---|---|
| 0 | `0x1` |  | `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200` (`002342D3`) |  |
| 1 | `0x2` | `BattleUnit_TeardownAndDespawn` `00300E40` (`00300F2A`) |  | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`00234039`); `BattleUnit_HandleActorTimelineEvent` `00319F50` (`00319FA3`); `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326AD0`); `003243F0` (`00324420`); +1 more |
| 2 | `0x4` |  | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AA6`) | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233AEE`); `BattleStats_ClearAllEquipmentSlotsByMappedId` `0031A300` (`0031A3BD`); `00324380` (`003243B5`); `BattleUnit_HandleReactionAnimationEvent` `003250F0` (`00325117`); +4 more |
| 3 | `0x8` | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233B4B`) | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AA6`) | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233B3A`); `00317E60` (`00317E8B`); `00319090` (`003190C3`); `00319490` (`003194CF`); +4 more |
| 4 | `0x10` | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`0023412D`) | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AA6`) | `ActorSystem_ReleaseBattleUnitSlotForActor` `00234200` (`00234263`); `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` (`00235126`); `00237D80` (`00237D93`); `AiOrder_EvaluateTargetSelector` `00301AD0` (`00301D30`); +27 more |
| 5 | `0x20` |  | `BattleUnit_ReleaseTargetRelationAndActionState` `00310780` (`0031080B`); `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F0FD`) |  |
| 6 | `0x40` | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326AFA`); `00324470` (`003244E1`) | `00324450` (`00324463`) | `00324450` (`00324456`) |
| 8 | `0x100` | `00313500` (`00313531`) | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`00306AC0`); `00233EA0` (`00233EC7`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`00301295`); `00313F70` (`00313F70`); +1 more |  |
| 9 | `0x200` | `BattleUnit_HandleActorTimelineEvent` `00319F50` (`0031A1B1`) | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`00306AC0`); `00233EA0` (`00233EC7`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`00301295`); `003082F0` (`0030835A`); +1 more |  |
| 10 | `0x400` | `BattleUnit_HandleActorTimelineEvent` `00319F50` (`0031A14E`) | `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`00301295`); `BattleUnit_ResetStateForReuse` `00236A60` (`00236AA6`) |  |
| 11 | `0x800` | `SpawnGroup_SetUnitFlag800ByGroupMask` `00234A10` — the verb `hideenemy` `0479` | `SpawnGroup_ClearUnitFlag800ByGroupMask` `00234A80` — the verb `showenemy` `0478`; `BattleUnit_ResetStateForReuse` `00236A60` (`00236AA6`) | `BattleUnit_ComputePresentationSuppressionMask` `003125E0` (`0031268A`): reason bit 1 of the mask that hides the actor (L-3, 2026-09-11) |
| 12 | `0x1000` | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304E74`) — queued in the presentation cursor ring `022BEDA4` (added 2026-09-12, FABLE; [the ladder page](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §"the target-selection cursor") | `00313DB0` (`00313E17`) — popped |  |
| 13 | `0x2000` | `00313DB0` (`00313E1E`) — popped, its presentation shown | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304FE9`) — presentation finished (`0030BC40`) | `00313DB0` (`00313EEC`): hold the selection |
| 14 | `0x4000` |  | `BattleUnit_ResetStateForReuse` `00236A60` (`00236AA6`) |  |
| 16 | `0x10000` | `BattleUnit_UpdateEngagementStateFlag` `00307D10` (`00307DE2`, recomputed) | the same (`00307DD8`) | the field frame ([page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)); added 2026-09-12 (FABLE) |
| 15 | `0x8000` | `00239170` (`00239190`) | `00239170` (`002391A2`) |  |
| 18 | `0x40000` | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`00236382`); `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`002363AA`) | `BattleUnit_SnapshotWorldActorRuntimeState` `00236300` (`00236352`); `BattleUnit_UpdateCombatNavigationStep` `00325BB0` (`00325BE6`) |  |
| 19 | `0x80000` | `BattleUnit_HandleActionTimelineEvent` `00325260` (`003256FB`) |  |  |
| 20 | `0x100000` | `003057D0` (`00305896`) |  |  |
| 21 | `0x200000` | `SpawnUnit_BindEntryAndMarkCapTracked` `00239840` (`002398D1`) | `00234480` (`00234503`) *(corrected 2026-10-02, OPUS: the slot allocator's `and dword ptr [rbx], 0xFFDFFFFF` at bind)* | `Spawn_CountActiveCapTrackedActors` `00308D90` (`00308DB3`) |
| 22 | `0x400000` | `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` (`003130D2`) |  |  |
| 23 | `0x800000` |  | `0030F2D0` (`0030F2F2`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`0030122B`) | `Battle_EmitReactionPresentationForSlot` `003176E0` (`0031776C`); `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` (`00313059`); `BattleUnit_SeedPartyCombatStanceRecheckTimer` `003081E0` (`003081E6`) |
| 24 | `0x1000000` | `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`003012A1`); `00313500` (`00313537`) | `BattleUnit_HandleReactionAnimationEvent` `003250F0` (`0032517C`); `003083A0` (`003083A6`) | *(2026-09-30, SWE2-DATA, [SD-4 record](../../_index/candidates/sd4-unit-flag-bit24-0930/README.md) (SD-4, a transition in progress): the setters are five - also `BattleUnit_EnterPartyCombatStance` `00313400` (`00313469`), `BattleUnit_ExitPartyCombatStance` `00313480` (`003134EB`) and `Battle_ProcessActionTarget` `00307300` (`00307A97`); the clearers also `00307C70` (`00307CA2` / `00307CD7`) and `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031066F`), and the slot memsets `002342CE` / `002344D2` zero the word; the capability recompute `0023B040` tests it. Scope, SWE2-AUDIT-SPEC [review](../../_index/candidates/auditspec-review-sd4-0930/REVIEW.md): dword / qword memory-destination `or` / `and` / `bts` / `btr` forms; `00227680` also sets bit 24 with bit 27 through a register (`00227BC8`, `00227BD7`), and byte-width writers at `+3` in `003DE710`, `003EDAD0`, `00517650` and `00346C00` are on unidentified objects.)* |
| 25 | `0x2000000` | `00313500` (`00313531`) | `003083A0` (`003083A0`) |  |
| 26 | `0x4000000` | `Spawn_SelectPreviousMapEntry` `002354F0` (`0023557E`); `00238FA0` (`00238FAE`); `SpawnEntry_SetCurrentCandidateState` `00239410` (`0023946D`); `00311F70` (`003120A0`); +1 more | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233AFB`); `SpawnUnit_SetLaneCandidateTable` `002393E0` (`002393F3`); `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690` (`0030F6FC`); `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326AFD`); +1 more |  |
| 28 | `0x10000000` |  | `BattleUnit_ReleaseTargetRelationAndActionState` `00310780` (`0031080B`); `BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` (`0030F0FD`) |  |
| 30 | `0x40000000` | `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`003012AD`) | `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` (`00310DFC`) |  |
| 34 | `0x4` (high dword) | `BattleUnit_HandleActorTimelineEvent` `00319F50` (`0031A147`); `BattleUnit_HandleActorTimelineEvent` `00319F50` (`0031A198`) | `BattleUnit_TeardownAndDespawn` `00300E40` (`00300F16`); `00300FC0` (`0030101A`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`00301287`); `BattleUnit_ResetStateForReuse` `00236A60` (`00236A95`) | `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` (`002340F1`) |
| 37 | `0x20` (high dword) |  | `00238B40` (`00238B52`) | `0046AB10` (`0046AB52`); `BattleTarget_ComputeUnitEligibilityMask` `0030B7F0` (`0030B817`) |
| 38 | `0x40` (high dword) | `00313500` (`0031352D`) | `00233EA0` (`00233ECD`); `003082F0` (`00308346`); `BattleUnit_ResetStateForReuse` `00236A60` (`00236A95`) | `BattleUnit_HandleActorTimelineEvent` `00319F50` (`0031A1AB`) |
| 39 | `0x80` (high dword) |  | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310651`) |  |
| 41 | `0x200` (high dword) | `00311F50` (`00311F5E`) | `0030F2D0` (`0030F2F8`); `BattleUnit_UpdateEngagementStateFlag` `00307D10` (`00307DD1`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`00301231`) | `BattleUnit_UpdateEngagementStateFlag` `00307D10` (`00307D84`) |
| 42 | `0x400` (high dword) | `00311F50` (`00311F5E`) | `0030F2D0` (`0030F2F8`); `BattleUnit_UpdateEngagementStateFlag` `00307D10` (`00307D9E`); `BattleUnit_UpdateEngagementStateFlag` `00307D10` (`00307DD1`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`00301231`) | `BattleUnit_UpdateEngagementStateFlag` `00307D10` (`00307DA7`) |
| 48 | `0x10000` (high dword) |  | `0030F2D0` (`0030F2F8`); `BattleUnit_UpdateEngagementStateFlag` `00307D10` (`00307DD8`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`00301231`) |  |
| 52 | `0x100000` (high dword) |  | `BattleUnit_ResetStateForReuse` `00236A60` (`00236A95`) |  |
| 53 | `0x200000` (high dword) | `BattleUnit_TeardownAndDespawn` `00300E40` (`00300ECE`); `BattleUnit_ResetActionControlForStatusTransition` `00300140` (`003001BA`); `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`0030120B`) | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`00310651`) | `Battle_ProcessActionTarget` `00307300` (`003075D7`) |

**Register-mask sites the pages have read** (not decodable from the table):

| bit | set by | cleared by | tested by | page |
|---|---|---|---|---|
| 33 | `BattleUnit_HandleReactionAnimationEvent` `003250F0` (`00325185`) | | | [group completion](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) |
| 35 | `BattleUnit_AdvanceStandardActionState` `00304850` (`00304DA5`–`00304DBA`, when the committed action id is `0x9F`, the random-draw placeholder) | | | [the scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.5 |
| 40 | `SpawnEntry_ConfigureFreshLifecycleFloatMode` `0023A200` (`0023A240`, float ≠ 0) | `0023A200` (`0023A231`, float = 0) | | [the spawn-keep entry](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) §3 |
| 45 | | | the minimum-distance opt-in with bit 49 (`0x0002200000000000`) | [spawn placement](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) §8f |
| 46 | `BattleUnit_AdvanceStandardActionState` `00304850`, phase 9 (`00304EF3`–`00304EFD`), for every action | the same function, phase 10 (`00304F9F`–`00304FA9`), only for an action whose definition `+0x0C` lacks bit 30, and only once `animationEventFlags` `+0x690` holds bits 1 and 3 (`00304F91`–`00304F9A`); a bit-30 action's phase 10 advances without clearing it (`00304F62`–`00304F8C`), ~~and no other clear is found (**FF-6**)~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's REJECT, [review](../../_index/candidates/auditsem-review-bit46-0930/REVIEW.md) §5)* it is also cleared by `00304850` phases 0 and 6 (`00304967`–`00304975`, `00304DDD`–`00304DEB`, mask `0xFFFFBFF75FFFCFFF`), a cancel (`BattleUnit_CancelAndResetCurrentAction` `003105D0`, `0031063F`–`0031064B`, same mask), `00308270` (`003082CB`–`003082DF`, mask `0xFFFFBFFFFFBFFFFF`), and the slot release / allocation memsets (`002342CE`, `002344D2`) (**FF-6** answered) | the capability recompute (`0023B0E6`–`0023B0E9`): set on the party leader, it forces the all-suppressed mask | [the native command seam](../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md) (the phase table); [capability policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) §10; [`bit46_writers.py`](../../_index/candidates/bit46-fable-0930/bit46_writers.py) |
| 47 | `0030700C` | `00306FC9`; `SpawnGroup_MarkCompletionPendingAfterReaction` `00307110` (`0030711A`) | `003250F0` (`0032519C`) | [group completion](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) |
| 49 | `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` (`00233B82`–`00233B8C`) | | the minimum-distance opt-in | [the spawn-keep entry](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) §3; [spawn placement](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) §8f |

**Whole-word writers**: `BattleUnit_TeardownAndDespawn` (`00300E40`, `00300EAA`) and
`BattleUnit_ResetActionControlForStatusTransition` (`00300140`, `00300198`) store a computed qword;
`BattleUnit_ResetStateForReuse` (`00236A60`) clears bits 2, 3, 4, 8, 9, 10, 11, 14 in one `and`
(`00236AA6`) and bits 34, 38, 52 in another (`00236A95`). Bit 0 — the pool's slot-in-use marker —
is set by the allocator scan ([the slot pool](../battleunit-slot-pool-and-actor-class.md)) and cleared at release (`00234200`, `002342D3`).

### 2.6 What the unresolved rows are — 2026-09-11 (OPUS-REQ-FABLE-BATTLEUNIT-NAMES)

OPUS measured the type store: 115 of the unit's 144 rows carry no name, and asked whether the
census can carry names for a useful share of them. It can for most. Every row below was read from
its cited writer and reader bodies (tier 1, static); the confidence column says how far the reading
goes — **PROVEN** means the mechanism is in the bytes cited, **PARTIAL** means the mechanism is
proven but the value's meaning is not, **OPEN** means only a write or a reset was found. Proposed
type-store names are in the name column; OPUS owns the store rows.

**Two bases were being confused.** Two pages say "unit" for the *stats record* the unit points to
at `+0x698`: the periodic-tick page's status timers at `+0x17C + slot × 2` and its HP / max-HP
reads at `+0x48` / `+0x24`, and the licence page's owned-licence mask at `+0x194` are all
`BattleStatsRecord` fields (`BattleFormula_AdvanceStatusLinkedAuxTimers` `00385570` indexes the
status layers at `+0x68` / `+0x78` and the timers at `+0x17C` off its first argument, which the
periodic builder passes through; `BattleStats_HasRequiredLicenseForAction` `00323EC0` tests the kind
byte at `+5` and the job at `+4` of its first argument — record bytes). Both pages are corrected
today. **In the unit itself `+0x17C` is a float, `+0x24` an actor handle and `+0x194` a movement
snapshot** — the rows below — and the type store must not inherit the other pages' offsets.

#### 2.6.1 Header, team and presentation

| Offset | Width | Name | What it is | Sites | Confidence |
|---|---|---|---|---|---|
| `+0x024` | 4 | `groupLeaderActorHandle` | the actor handle of the unit's group leader, refreshed every maintenance tick from `00305E70`: for a party-kind record the party leader (`003271E0` → `+8`), otherwise the first pooled unit with the same `+0x54` team byte whose flag bit 15 is set (`00305EB0`–`00305ED1`). Compared with `+8` in relation mode ("am I the leader", `0030BDBC`–`0030BDC4`) and by the commit's group broadcast (`0030F8D5`–`0030F91B`). | `00310DDC`–`00310DE4` | PROVEN |
| `+0x028` | 4 | `retaliationTargetHandle` | the **attacker's** actor handle: `Battle_ProcessActionTarget` stores the source unit's `+8` into the target's `+0x28` when the action row's `+8` has bit 9 and the source's flag bit 22 is clear (`00307782`–`00307798`); `BattleUnit_TryCommitEngageAutoAttack` `00312FA0` takes and clears it (`00312FAF`–`00312FB5`) and resolves it through `BattleUnit_ResolveByFocusHandle`; cleared by the reaction-animation handler (`003251E3`) and the reservation restore (`00308282`); the display builder turns "non-zero" into a bit (`0031B120`). Setter found 2026-09-11 by an image-wide displacement sweep (FW-2). | as cited | PROVEN |
| `+0x02C` | 4 | `presentationEventParameter` | `BattleUnit_DispatchActorPresentationEvent` `003299B0` stores its third argument here *before* the actor event `002EB030` and zeroes it *after* (`003299C2`, `003299F6`); `00317810` and `00328640` use the same protocol with 0. **Consumer found 2026-09-11:** the render record's event receiver `00427320` calls `00420890(record, event)`, which asks the unit for a presentation view through `002ED500` → `0031B4B0` → `0031ADB0(unit, selector, out)` with selector `0x100` for events `0x2006`–`0x2036` and `0x2038`; that selector copies `+0x2C` into the view's `+0x30` (`0031AE36`–`0031AE51`), and the receiver stores the view's `+0x30` at record `+0x110` (`0042093E`–`00420942`). | as cited | PROVEN |
| `+0x04C` | 4 | `nativeLifecycleRange` | **f32**, world units: `VM_Spawn_SetNativeLifecycleMode` `0050F4A0` → `00238FC0` stores `r8d ? r8d / 10.0 : 6.0` (`00238FE9`–`00239006`, `008F8180`, `01CEBC74`) when the mode is 2; `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` squares it and compares with the squared XZ distance from the anchor vector to the party leader (`0023519C`–`002351B9`). | as cited | PROVEN |
| `+0x050` | 1 | `nativeLifecycleMode` | the verb's fourth argument (`00238FE1`); 0 = none (the checker returns at `00235104`), 1 and 2 are its two branches (`00235162`–`0023517B`), 2 the ranged retire. | as cited | PROVEN |
| `+0x051` | 1 | `nativeLifecycleAnchorIndex` | the verb's second argument (`0023900B`), used as the index into `FieldData_GetFormat0RecordVectorByIndex` `00320940` for the anchor point (`0023518A`–`00235193`). | as cited | PROVEN |
| `+0x052` | 2 | `definitionWord80` | a u16 the installer copies from its stack slot `+0x80` (`0023AC14`), 0 at reset; read once by the AI target selector (`003021F3`). ~~Which definition field feeds the stack slot is not traced.~~ *(answered: the class row's word `+6` on the enemy path, `0023A910` → `0023A936`, and `-1` on the party path, `0023AB73` → `0023AB98`; 2026-10-02, OPUS)* | as cited | PARTIAL |
| `+0x054` | 1 | `teamId` | verb `00510280` → `00239170(actor, isLeader, team)`: `+0x54 = team` (`00239189`) and flag bit 15 = leader (`00239190` / `002391A2`). Relation modes compare two units' bytes for equality or difference (`0030BDCB`–`0030BE11`); `0xFF` at install (`0023AC18`) and reset. | as cited | PROVEN |
| `+0x055` | 1 | `definitionTypeByte` | the definition row's `+4` (`0023ABF0`), already named by [the evaluation context](../../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md); compared with `0xD` at `0038D4D9`. | by reference | PROVEN |
| `+0x056` | 1 | `definitionCategoryByte` | the installer's `bl` (`0023AC11`); the HP-stage pulse runs only for category `0xF` enemies (`002FE97E`); read by chain-on-defeat (`00317F21`, `003180CC`) and the selector (`003021EC`, `003025FC`). The category values are not decoded. | as cited | PARTIAL |
| `+0x057` | 1 | `actorClassDerivedByte` | the store's own meaning stands: written at bind from `00263D30(actor)` (`00234509`); read as a signed index by the spawn-entry queries (`00236682`, `00239435`) and rewritten by `SpawnUnit_BindEntryAndMarkCapTracked` (`002398A9`). | as cited | PARTIAL |
| `+0x05C` | 4 | `lastPresentationEventId` | **FF-3 answered:** the event id the dispatcher just sent, `id \| 0x5000` when `(id & 0xFFF) ≥ 0x100` (`003299CA`–`003299EE`); the literals `0x2001` (`00317835`, `0032A1C4`) and `0x201C` (`003286B4`) are the same field written by the two fixed-event callers. | as cited | PROVEN |
| `+0x060` | 4 | `currentPresentationEventId` | copied every maintenance tick (`00310DEC`) from `002E8100(actorHandle)`: actor → controller → render record → `0041FCA0`, which returns the record's word `+0xCE` when `+0xC8 ≠ −1` and `004235C0(record, +0xCE, +0xCC)` holds, else `+0xCC` — *2026-09-12: the argument order was written inverted here; the call passes the alternate `+0xCE` as the candidate and the current `+0xCC` as the selector, and under stable valid records the predicate cannot reject ([render-event selection evidence](../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md) §4, agreed by FABLE), so the field is `+0xCE` whenever `+0xC8` (the record's **alternate presentation-entry id**, released and reset to −1 by `CharacterRenderRecord_MaintainPresentationResourceReferences` at `00422BB8`–`00422BBD`) is present.* `+0xCC` is the record's current presentation event: the event receiver compares it with `0x2001` / `0x2009` / `0x2031` (`004273C1`–`004273FF`), `CharacterRenderRecord_MaintainPresentationResourceReferences` clears it (`00422AEB`) and the presentation state machines write it (`00423F6B`, `00424E61`–`00425274`); [the render record page](../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md) still calls it the subtype. `+0xCE` is its alternate (`004247D0`). | as cited | PROVEN |
| `+0x068` | 4 | `perceptionRangeThreshold` | **f32** from an integer in the definition (`0023AC0C`), copied to the display record `+0x1C`; the perception rebuild compares a distance against it (`00324992`, `00324A7A`). | as cited | PARTIAL |
| `+0x06C` | 4 | `definitionFloatB` | the installer's `xmm7` (`0023ABD6`), 0 at reset; no reader on any route. | as cited | OPEN |
| `+0x070` | 4 | `primaryResourceRecoveryAccumulator` | **f32** added by `BattleUnit_AddPrimaryResourceRecoveryAccumulator` `00329A20` (`00329A5D`–`00329A62`) and taken-and-zeroed by `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450` (`0032048D`–`00320492`); [the MP page](../../10-Status-Periodic-Terminal/where-mp-comes-from.md). | as cited | PROVEN |
| `+0x074` | 4 | `attachedEffectHandle` | `BattleUnit_HandleActionTimelineEvent` creates it through `002EACD0(actorHandle, 1, &+8, 0x78)` (`0032562A`–`00325646`) unless the stats page's `+0x18 & 0xE == 4`; teardown releases it through `00319E30` and stores −1 (`00300ECB`, `00300F2E`), recover-from-terminal likewise (`0030129E`–`003012B3`); −1 at reset. | as cited | PROVEN |
| `+0x0D0` | 16 | `lastNavigablePosition` | the snapshot copies the world position `+0xE0` here when a navmesh region exists for it (`00236407`–`0023642A`); `Navigation_BuildOrReusePathXZ` reads its z at `+0xD8` (`0038362B`). | as cited | PROVEN |

#### 2.6.2 The embedded locomotion state at `+0x80` (0x180 bytes, `BattleLocomotionState`)

Every battle-locomotion function takes `unit + 0x80` as its record (`00325BC4`, `003105F9`,
`0030F056`); its offsets below are unit offsets, with the record offset in brackets.

| Offset | Width | Name | What it is | Sites | Confidence |
|---|---|---|---|---|---|
| `+0x0F0` [`+0x70`] | 12 | `currentWaypoint` | x / y / z: `Navigation_SelectNextWaypointXZ` receives the triple's address (`lea r8, [rbx + 0x70]`, `00325C51`) and writes x and z from the chosen path node and y from the source (`00383713`–`00383721`); `BattleLocomotion_BuildSolverContext` copies the three dwords into a homogeneous vector with `w = 1.0` (`00336757`–`00336769`); `Navigation_BuildOrReusePathXZ` reads it through the same pointer (`0038364D`). **The vector reading rests on those consumers, not on access widths** — every access is a separate dword, which is why the type store keeps three float rows (OPUS-NOTICE-FABLE-BU760, 2026-09-11). | as cited | PROVEN |
| `+0x100` [`+0x80`] | 16 | `pathGoal` | `BattleLocomotion_ResetPathAndSetTargets` writes it (`003291E0`); `Navigation_BuildOrReusePathXZ` reads it (`00383639`, `0038364D`); solver context `+0x20` (`00336770`–`0033678B`). | as cited | PROVEN |
| `+0x110` [`+0x90`] | 16 | `secondaryTarget` | the second vector the same reset writes (`003291F8`); solver context `+0x30` (`00336792`–`003367AD`). Which of the two is "goal" and which "look-at" is open. | as cited | PARTIAL |
| `+0x140` [`+0xC0`] | 16 | `solvedPosition` | `BattleLocomotion_SolveAndPublishNextStep` stores its solved triple (`00336DE1`–`00336DFD`); the navigation step hands the address (`lea rdx, [rbx + 0xC0]`, `00325D3B`) to `BattleUnit_PublishLocomotionPositionAndFacing` → `BattleUnit_PublishLocomotionPosition` `00300310`, which compares `[rsi]`, `[rsi + 4]`, `[rsi + 8]` with the actor's world position, passes them as x / y / z to `0026B0C0`, and then **copies 16 bytes** (`movaps xmm0, [rsi]`) into unit `+0xD0` and `+0xE0` and the spawn record's `+0x50` (`0030037B`–`003003CE`). So it is a four-float position by consumption, `+0x14C` its w lane; the store's three float rows describe the same bytes (OPUS-NOTICE-FABLE-BU760, 2026-09-11). | as cited | PROVEN |
| `+0x150` | 4 | `approachDiameter` | `2 × +0x17C` (`0023A017`–`0023A03F`). | as cited | PROVEN |
| `+0x158` [`+0xD8`] | 4 | `solverScalarA` | a float the solver writes (`00336D95`, `0033A334`), zeroed at the snapshot (`00236359`) and when the step is consumed (`00325D1E`, `00325D46`). | as cited | OPEN |
| `+0x15C` [`+0xDC`] | 4 | `motionYaw` | the snapshot stores `00263CC0(actor)` = `movementState + 0xA4` (`00236328`); the publisher stores its facing argument here and in `+0x160` (`0030041E`–`00300426`); solver context `+0xB4`. | as cited | PROVEN |
| `+0x160` [`+0xE0`] | 4 | `currentHeading` | the locomotion state's current heading — read as `cur` by `Angle_ApproachWrappedRadians` in every solver; written by the solver publish (`00336DC5`, `0033A35E` — source `ctx+0xBC`, a *derived* heading, not always a `0033CB70` result) and by the facing publish (`00300426`, `00310B00`/`00310BB1`/`00310CA6`, `003120AF` — caller-supplied facing, unnormalized). Typed census: [locomotion-angle-accesses.tsv](../../06-Movement-And-Navigation/Battle-Locomotion/locomotion-angle-accesses.tsv). | as cited | PROVEN |
| `+0x164`, `+0x168`, `+0x16C`, `+0x170`, `+0x178`, `+0x180`, `+0x184`, `+0x198`, `+0x1AC`, `+0x1B0` | 4 each | `fcpAngleSlot4`, `fcpAngleSlot47`, `fcpAngleSlot3or9`, `fcpAngleSlot38`, `fcpRadiusSlot0or6`, `fcpBodyRadiusSlot2or8`, `fcpRadiusSlot1or7`, `fcpAngleSlot39`, `fcpAngleSlot50`, `fcpIntSlot49` | **the twelve authored tunables** `FUN_00239E10` installs (`00239E64`–`00239F5B`) through `003204D0(actorWork, index, out)` (`003204E0`): each index selects a property id from the table at `01EED320`, read from the model container's `@FCP` block — [the parameter-block page](../../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md) decodes the ids (section 9 of the block, file slot in the id's low byte, 2026-09-11): `+0x178` ← slot 0 (6 when `sel`), `+0x180` ← slot 2 (8), `+0x184` ← slot 1 (7), `+0x16C` ← slot 3 (9), `+0x164` ← slot 4, `+0x168` ← slot 47, `+0x170` ← slot 38, `+0x198` ← slot 39, `+0x1AC` ← slot 50, `+0x1B0` ← the integer at slot 49 (60 in 420 of 723 files, −1 in 173); `+0x178`, `+0x180` and `+0x184` are **multiplied by the actor's y-scale** (`00265240` → `movementState + 0x24`, `00320570`–`0032057A`), the rest raw. `sel` is true when the stats record's kind is 1 and the definition's `+0x13 ≠ 0xFF` (`00239E3D`–`00239E5C`); a model without section 9 (every weapon) yields the engine's default table. `+0x184` is forwarded to the render record's `+0x420` (`0023A006`–`0023A012`, `002E86B0`). In the party files opened slots 0–2 are `0.0667 / 0.1333 / 0.2` and slots 3, 4, 38, 39, 47 are angles (`0.1047` = 6°, `0.7854` = 45°); the monster's alternate slots 6–8 are `0.1333 / 0.2667 / 0.4`. One consumer is now known: `+0x16C` is `st+0xEC` on the locomotion state — the **slow turn rate**, read as the `step` argument of `Angle_ApproachWrappedRadians` at `00336595`/`00336650`/`0033A665`/`0033A68E`/`0033B3D8`/`0033CE8D` (flag-selected against `+0x170` = `st+0xF0`, the fast rate); the `003204E0` store is the only writer and performs no clamp. What the other slots *mean* beyond their consumers is **FW-1**. *2026-09-26 (FABLE, Claude Opus 5.5): `FW-1` answered by consumer, through the solver context's `+0x108` pointer to unit + 0x80: the fast-moving turn step (`+0x164`) and the other turn step (`+0x168`), chosen by whether the step length exceeds the threshold `+0x184`; the minimum step length (`+0x178`); the maximum step length, derived from `+0x180` (scaled by 1.0, 1.5 or 1.2 and stored at `+0x17C`); a bound on how far the limited heading may sit from the desired one (`+0x198`); the avoidance manoeuvre's sweep angle (`+0x1AC`) and its chance divisor (`+0x1B0`, `-1` disables it); and a profile index into a speed/heading table (`+0x1F5`). The names `fcpRadiusSlot0or6` / `fcpRadiusSlot1or7` are census labels; their consumers use them as a step length and a step-length threshold. Control: [`fw1_tunable_consumers.py`](../../_index/candidates/fw1-tunable-consumers/fw1_tunable_consumers.py).* | as cited | PROVEN mechanism and source; meaning by consumer 2026-09-26 |
| `+0x174` [`+0xF4`] | 4 | `motionPitch` | the snapshot stores `00263C80(actor)` = `movementState + 0xA0` (`00236339`); solver (`00336DB7`); context `+0xB8`. | as cited | PROVEN |
| `+0x17C` | 4 | `effectiveApproachRadius` | `+0x180` scaled by `00233A20`: × 1.0 for a controllable party member (`0030BE80`), × 1.2 (`008FCC90`) when the party job byte is in `0x1B`–`0x27`, else × 1.5 (`00901B3C`); stored at install (`00239F6B`) and every snapshot (`002363FA`–`002363FF`). | as cited | PROVEN |
| `+0x18C` / `+0x190` [`+0x10C` / `+0x110`] | 4 + 4 | `collisionExtentPair` | `ActorRuntime_GetClass3FloatPair` `00265090` (called at `002363D3`–`002363E1`); the solver takes the larger as its radius (`003367C2`–`003367D9`). | as cited | PROVEN |
| `+0x194` | 4 | `movementStateD4Snapshot` | `00264670(actor)` = `movementState + 0xD4` (`002363EA`–`002363F2`), the float after the requested speed on [the heading page](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md); no reader on any route. | as cited | PARTIAL |
| `+0x19C` | 4 | `presentationYOffsetRamp` | 0.08 at install (`0023A035`); `003057D0` subtracts it from `002638F0(actor)`, advances it by 0.02 (`009002BC`) and passes `max(0, difference)` to `Actor_SetPresentationYOffsetPrimary` `00269E20` (`0030583D`–`00305873`). | as cited | PROVEN |
| `+0x1A0` / `+0x1A4` / `+0x1A8` [`+0x120` / `+0x124` / `+0x128`] | 4 × 3 | `orderRangeBands` | zeroed together by the cancel (`00310734`–`0031073E`); **written by the advance at the order handoff (2026-09-12, FW-2)**: `BattleUnit_AdvanceStandardActionState` copies the action block's three effective range bands `+0x6D4` / `+0x6D8` / `+0x6DC` here (`00304BF3`–`00304C0F`) while it sets `+0x1E0` = 3, `+0x1D0` = the action's target handle (block `+0x60`) and `+0x1F0` bit 5. **No reader on any route, including the locomotion sub-object routes**: every callee that receives `unit + 0x80` (`0033A240`, `BattleLocomotion_BuildSolverContext` — which reads `+0x60`–`+0x98`, `+0xDC`, `+0xE0`, `+0xF4`, `+0x10C`, `+0x110`, `+0x177` of it — `Navigation_BuildOrReusePathXZ`, `Navigation_SelectNextWaypointXZ`, `Vector3_ComputeXZHeadingOrFallback`) and every function holding it in a register (`003105D0`, `002FDC30`, `00325BB0`, `00304850`) leaves `+0x120`–`+0x128` unread. | as cited | PARTIAL |
| `+0x1C0` [`+0x140`] | 16 | `overrideVector` | `00329B00(actorHandle, enable, vec*)` (from `002E5610`) copies 16 bytes and sets `+0x1F0` bit 9, or clears the bit (`00329B33`–`00329B52`). | as cited | PROVEN mechanism; use OPEN |
| `+0x1D0` [`+0x150`] | 4 | `locomotionTargetHandle` | the solver context resolves it to a unit (`003369B3`) and an actor (`003369C5`). | as cited | PROVEN |
| `+0x1F0` [`+0x170`] | 4 | `locomotionFlags` | bit 0 = action row `+4` bit 9 (`00325C89`), bit 1 = row bit 8 (`00325CB0`), bit 2 = the `@FCP` section-9 slot 41 dword non-zero (`0x29010229`, `00239F73`; non-zero in 360 of 723 files), bit 3 = unit flag bit 23 (`00325CC9`), bit 4 = action id `≤ 0x21E` and `≠ 0x96` (`00325CF4`), bit 5 cleared by the cancel (`00310751`), bit 7 publish pending (`00325D2F`–`00325D4F`), bit 9 override vector active (`00329B33`), bit 10 step consumed (`00325D0F`), bit 12 from verb `00510300` → `002392D0` flag bit 0 (`00239320`), bit 13 from `0023A120` (`00473830`; `0023A136` / `0023A146`). | as cited | PROVEN per bit |
| `+0x1F4` | 1 | `placementMode` | 1 by default, 2 for a kind-1 (enemy) record, 3 when the probe gate additionally has bit 3 (`00239FDA`–`0023A02E`); `BattleLocomotion_QueryDynamicActorObstruction` lets two mode-3 units ignore each other under flag `0x40` (`00335960`–`00335975`). | as cited | PROVEN |
| `+0x1F5` | 1 | `fcpSlot40LowByte` | the low byte of the `@FCP` section-9 slot 40 dword, read in integer mode (`0x29010128`, `00239F83`–`00239F88`); 0 in the files opened. | as cited | PARTIAL |
| `+0x1F6` | 1 | `heightProbeGate` | [the placement page](../../05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md): values 1, 2, 5, 6 (no probe) and 8, 12 (probe). | by reference | PROVEN |
| `+0x1F7` [`+0x177`] | 1 | `ownerSlotIndex` | the snapshot copies `+0xEA9` here (`00236314`) so the solver can fetch its unit by slot (`00336805`, `00336856`). | as cited | PROVEN |

#### 2.6.3 The navigation path state at `+0x200` (`NavigationPathState`)

`FUN_003278D0` resets it for every unit with flag bit 4 (`003278F7`–`00327909`): `003839C0` writes
`0xFFFF` into two words at `+0x20C` / `+0x20E`, `Navigation_ResetPathPredecessors` `003839F0`
writes `0xFF` into 128 bytes at `+0x210`. `Navigation_SelectNextWaypointXZ` reads the current index
at `+0x200` (`00383699`), takes ~~the node pointer~~ from `+0x290 + index × 8` (`003836F8`) and writes
the new index back (`00383700`). So: `+0x200` s32 `currentNodeIndex`, `+0x20C` u16[2]
`pathEndpoints`, `+0x210` u8[128] `predecessors`, `+0x290` ~~ptr[] `pathNodes`~~. **PROVEN** as a
structure; the node record is the navigation pages' business. *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5): the entry is not a
pointer. The reader spills the qword and uses its low dword as x and its high dword as z, so `+0x290` is
`{f32 x, f32 z}[128]` `waypointXZ[region]`, as [the navigation-mesh page](../../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md) §3 has it. The table runs to `+0x68F`; see `FF-2`.)*

#### 2.6.4 The action-state block at `+0x6B0` (0x4F0 bytes)

`BattleUnit_SnapshotAndSuspendActionState` `0030EFF0` copies `+0x6B0`–`+0xB9F` as one block
(`0030F04A`–`0030F0E1`) and keeps the copy's pointer at **`+0xB88`** (`0030F0F1`);
`BattleUnit_RestoreSuspendedActionState` `0030EDA0` is its inverse. Everything inside is
action-scoped.

| Offset | Width | Name | What it is | Sites | Confidence |
|---|---|---|---|---|---|
| `+0x690` | 4 | `animationEventFlags` | bit 0 = a reaction-animation event arrived (`003251BE`), bit 1 = an action-timeline event (`00325695`), bit 3 = an actor-timeline event (`0031A031`); zeroed by the cancel (`00310658`) and the reservation restore (`003082D5`). | as cited | PROVEN |
| `+0x694` | 1 | `presentationSlot0` | **the intake stage of a three-deep slot queue at `+0x694`/`+0x695`/`+0x696`, behind the flag word at `+0x690`** (renamed 2026-09-13, `FABLE-REQ-OPUS-SLOTSTAGES` — the old `targetRelationPresentationSlot` was taken from one of its clearers, and the field holds nothing specific to a target relation). **THE ONLY WRITER THAT INSTALLS A VALUE HERE IS INVISIBLE TO A DISPLACEMENT CENSUS:** `BattleAction_AcquirePresentationSlot` `0030CFB0` writes it at `0030D056` as `mov byte ptr [rdi + 4], al` with `rdi = unit + 0x690`. **All six writes a `0x694` census can see are clears to `0xFF`** (`00236A8C`, `0030010C`, `0030678B`, `0030FE3D`, `00310825`, `003132E3`). Released through `BattleAction_ReleasePresentationSlot` `0030C970`. The slots are the 32 × 0x30-byte records at `022C17B0` (`0030CA5B`–`0030CA6E`), which end exactly where the reservation stash table `022C1DB0` begins. | as cited | PROVEN |
| `+0x695` | 1 | `presentationSlot1` | **stage 2: filled by a GUARDED MOVE from `+0x694`** — three advance stores the earlier row omitted, each of the shape *if `+0x694 != 0xFF` and `+0x695 == 0xFF` then `+0x695 = +0x694`; `+0x694 = 0xFF`*: `BattleAction_UpdateSpecialPresentationSequence` `00306778`–`0030678B`, `BattleAction_DispatchResolvedPresentationEvent` `0030FE37`, and `003132DD`. **The guard is the point: a move never overwrites an occupied stage.** Cleared to `0xFF` by the cancel (`00310611`–`0031061D`), the reservation restore (`00308289`–`00308295`), `00309A55` and the `+0x696` move; `0030CA50` returns that slot's `+0x24`. | as cited | PROVEN |
| `+0x696` | 1 | `presentationSlot2` | **stage 3, and the queue ends here** — filled by the same guarded move from `+0x695`, at **one site only**: `BattleAction_UpdateSpecialPresentationSequence` `00306877`–`00306891`. Cleared to `0xFF` by the cancel (`00310624`–`00310633`) and by `003066E4`. **`BattleUnit_AdvanceStandardActionState` `00304850` releases all three together** through `r12 = unit + 0x690` — three identical release-and-clear pairs at `[r12+4]`, `[r12+5]`, `[r12+6]` (`00304B6F`–`00304B9C`), which is what makes the three one object rather than three fields that happen to be adjacent. | as cited | PROVEN |
| `+0x6B5` | 1 | `aiOrderSubgroup` | [the gambit page](../../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md). | by reference | PROVEN |
| `+0x6B6` | 1 | `pendingResultCount` | the commit stores 1 (`0030F894`); `Battle_ProcessActionTarget` walks that many bytes from `+0x6B9`, resolves each through `BattleStats_GetByBattleSlotIndex` `00320A40` and applies through `BattleFormula_ApplyTargetResult`, then stores 0 (`003073D7`–`0030744B`); the cancel stores 0 (`0031060A`); the preview and post-result evaluators read it the same way (`00385735`, `004698FD`). | as cited | PROVEN |
| `+0x6B9` | 1+ | `pendingResultSlotIndices` | the battle-slot indices the count covers; the commit writes the first from byte `+8` of this unit's reservation-stash row (`0030F878`–`0030F88E`). | as cited | PROVEN |
| `+0x6C0` | 16 | `actionScopedBlockA` | only touched by the suspend copy. | `0030F06B` | OPEN |
| `+0x6D0` / `+0x6D4` / `+0x6D8` / `+0x6DC` | 4 / 4 × 3 | `actionScopedFloat` and `effectiveRangeBands[3]` | `FUN_00238AB0(handle, f)` stores a float at `+0x6D0` (`00238AC6`); the cancel zeroes all (`0031070E`–`0031074B`). **`+0x6D4`–`+0x6DC` are the three floats `BattleAction_ComputeEffectiveRangeBands` returns through output pointers (2026-09-12, FW-2, through the action-block base `unit + 0x6B0`):** the advance zeroes them and passes their addresses as its 4th–6th arguments (`00304A7F`–`00304AB9`; the callee's stores `002FED0F`, `002FED21`, `002FED32`), then reads them back into the locomotion order words `+0x1A0` / `+0x1A4` / `+0x1A8` (`00304BF3`–`00304C0F`). *What they mean (2026-09-19, FABLE):* `+0x6D4` is the **near** band, `+0x6D8` the **middle** band, `+0x6DC` the **reach**, each centre to centre - [how close a unit must stand to act](../../07-Combat-Action/how-close-a-unit-must-stand-to-act.md). | as cited | PROVEN for `+0x6D4`–`+0x6DC`; `+0x6D0` PARTIAL |
| `+0x6E0` | 8 | `aiOrderSetVariant` | `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` `00239040`: definition `+0x50 + variant × 2` → table → `ImageAddress_ResolveRuntimePointer` `0020E600` (`00239073`–`00239081`); the gambit page's set C. | as cited | PROVEN |
| `+0x6E8` | 8 | `aiOrderSetA` | **the re-plan set** (2026-09-12: installed by six functions — the party combat stance's enter and exit, `BattleUnit_SetupEngagedActionState`, `002FEDC0`, recovery from a terminal status and `0030F2D0`, the handler of the `resetemergency` verbs; static sets `01EEC3C0` = order `0x4022` for party-kind, `01EEC410` = order `0x414D` otherwise; the census's writer count here missed the `rcx`-based stores) — `0030F2D0` chooses one of two static sets by record kind (`0030F31F`–`00310331`); recover-from-terminal rewrites it (`0030126B`). | as cited | PROVEN |
| `+0x6F0` | 8 | `aiOrderSetD` | **the static default set `01E09350`** given by `BattleUnit_ApplyUnitDefinition` (`0023ABB5`, 2026-09-12); ~~reset only on the census;~~ the gambit page's set D. | `00236BB6` | PROVEN by reference |
| `+0x6F8` | 8 | `aiOrderSetB` | **the player-issued command's set** (2026-09-12: `BattleUnit_IssueCommand` installs `01EEC2D0`, `00311DE1`) — zeroed by the status transition (`00300155`), teardown (`00300E68`) and recover (`0031119C`); the gambit page's set B. | as cited | PROVEN |
| `+0x728` | 8 | `committedTargetAndActionCopy` | the commit copies `+0x710`–`+0x717` (focus handle + action id) here (`0030F81B`–`0030F82A`); the cancel moves it to `+0x740` (`003106CC`–`003106E3`). | as cited | PROVEN |
| `+0x730` | 16 | `lastCancelledActionBlock` | the cancel's copy of `+0x718` (`003106B9`–`003106D7`); with `+0x740` / `+0x744` (the last cancelled target and id, [the commit page](../../07-Combat-Action/the-moment-an-action-is-committed.md)) it is what the queued-repeat check compares (`0030F84E`–`0030F857`). | as cited | PROVEN |
| `+0x748` | 4 | `commandedTargetHandle` | the target focus of the command a unit was issued: `BattleUnit_IssueCommand` `00311CF0` stores its ~~third argument~~ target-handle argument (`edx`, `00311D16`) here and points order set B (`+0x6F8`) at the command's static set — one `Attack` record aimed by this field (`00311DD0`–`00311DE1`); relation mode ~~8~~ **10** (jump-table slot 10, corrected 2026-09-12) compares a candidate's `+8` with it (`0030BE2A`–`0030BE35`); zeroed together with `+0x6F8` wherever the command is dropped — the next-action selector (`00305C25`–`00305C2C`, `00305C45`–`00305C4C`), the execution timeout (`0030AFB2`–`0030AFB9`), the stats rebuild's cancel path (`002FF9CC`–`002FF9D3`), the status transition, teardown and recover. Setter found 2026-09-11 (FW-2). | as cited | PROVEN |
| `+0x74C` | 4 | `relationWordB` | zeroed with `+0x748` (`003001B3`, `00300EC5`, `00301202`); no reader. | as cited | OPEN |
| `+0x750` / `+0x754` | 4 + 4 | `groupTargetFocus` (follower copy / broadcast) | the commit writes its target focus into `+0x754` of every unit sharing the leader (`0030F8CF`, `0030F920`) and into `+0x750` (`0030F8A3`, `0030F931`); `00305E70` copies `+0x754` → `+0x750` on the leader (`00305EF6`–`00305EFC`); no reader beyond those. | as cited | PARTIAL |
| `+0x758` | 2 | `actionScopedWordC` | `0xFFFF` at reset only. | `00236BD9` | OPEN |
| `+0x75C` | 4 | `actionAgeCounter` | `BattleUnit_AdvanceActionState` increments it on every advance where `+0x768 ≥ +0x76C` (`00307C27`–`00307C35`); `BattleAction_CheckAndHandleExecutionTimeout` compares it with `10 × trunc(scale)` — or a shorter bound for ids `≤ 0x21E` — and drops the action when it exceeds it (`0030AF8C`–`0030AFB9`); zeroed by the cancel (`00310715`). Found 2026-09-11 by the same sweep. | as cited | PROVEN |
| `+0x760`–`+0x76F` | 16 | `actionProgressBlock` | **corrected 2026-09-11 (OPUS-NOTICE-FABLE-BU760):** not four dwords by any census access — the two clears cover the region with differently aligned qword stores (`003106F9`–`00310700`, `00236B63`–`00236B79`) — but an image-wide displacement sweep finds three dword accesses outside the census: `BattleUnit_ResetStateForReuse` stores a dword at `+0x760` (`00236B87`), and `BattleUnit_AdvanceActionState` (`00307C27`–`00307C2D`) and `BattleLocomotion_ComputeStepDistance` (`00339CA5`–`00339CB1`) each read `+0x76C` and compare `+0x768` against it as a pair (`current ≥ target`). So `+0x760 u32`, `+0x768 u32 actionProgressCurrent`, `+0x76C u32 actionProgressTarget`; ~~`+0x764` is only ever bulk-written~~ **`+0x764` is read through the action-block base (2026-09-12, FW-2)**: `BattleUnit_AdvanceStandardActionState` holds `unit + 0x6B0` in `rsi` and stores `+0x764` = 0 for the action rows the checks at `003049AC`–`003049D6` pick out, otherwise `002FA1A0(unit)` (`003049E5`) — CRT `rand() % (900 k) + 1200 k` when the unit's `+0x698` object has byte `+5` == 1, else `rand() % (1500 k) + 1500 k`, `k` = the frame-rate scale `01DFE0B4` — and then, when `+0x760 < +0x764`, adds `002F9F10()` = 100 to `+0x760` (`00304A1A`–`00304A30`). So `+0x760 actionProgressAccumulator` counts up by 100 per qualifying advance toward `+0x764 actionProgressThreshold`, a randomised budget. | as cited | PROVEN |
| `+0x774` | 4 | `releasedEffectHandle` | `00319420` (on `+0x6B0`, field `+0xC4`) releases a non-negative handle through `002EAEA0(handle, 1)` and stores −1 (`00319429`–`00319441`), from `BattleUnit_ReleaseTargetRelationAndActionState` (`0031082C`) and `00304850`. *(2026-09-30, SWE2-DATA, [GR-17 residue record](../../_index/candidates/gr17-effect-residue-0930/README.md): the one store of a real handle is `0032A045` in `00329F80`, which creates the unit's action-charge effect; GR-17's residue shows no shipped effect that can sit here has a hit or self-KO event.)* | as cited | PARTIAL |
| `+0x778` | 0x208 | `targetBuffer` | `BattleTargetBuffer`: `+0` flags (bit 0 preserved by the reset `00316D10`–`00316D16`), `+1` u16 zeroed, `+4` s32 `count` (`+0x77C`), `+8` 32 entries of 16 bytes `{actorWork, u8 state}` (`+0x780`…): the state byte at entry `+8` takes values 1–10 (`Battle_EmitReactionPresentationForSlot` `00317783`–`00317790`) and 8 means "result ready" (`00322810`). | as cited | PROVEN |
| `+0x988` | 0x200 | `targetResultPointers` | 32 entries of 16 bytes `{resultRecord*, aux}` parallel to the target buffer: `BattleAction_EvaluateTargetPreviewRecursive` stores the record it built per target index (`00303B6D`) or zero (`00303B9D`); `Battle_ProcessActionTargetEntry` requires it non-null (`0031930C`); `00322760` reads it when the entry's state is 8 (`00322810`–`0032281A`). | as cited | PROVEN |
| `+0xB88` | 8 | `suspendedActionStateCopy` | see the block note above. | `0030F0F1` | PROVEN |
| `+0xB90` | 4 | `actionScopedWordF` | ~~zeroed at reset only.~~ *(Corrected 2026-09-30, SWE2-DATA, [GR-7 record](../../_index/candidates/gr7-kind10-reader-0930/README.md), [consumer check](../../_index/candidates/data-gr7-gr17-fieldmap-0930/README.md):)* **operand-store kind 10, the unit's what-was-used-on-me mask.** The composer `00312170` ORs in the acting row's `+0x3A` bit, element byte `+0x13` and `+0x0C` bits 13 / 14 on the second unit it is handed; the enemy AI store op `002FE660` sets or clears an order's parameter bit (orders `0x4122` / `0x4123`); both land through the operand-store writer's case-10 arm. The one reader is the enemy AI selector `00301AD0` (opcode `0x36` / `0x37` mode 3), through `AiTargetSelector_ResolveOperandValue` `00321190`. | `00236BE0`, `00329F29`; read `0032127C` | ANSWERED (GR-7) |

#### 2.6.5 After the block

| Offset | Width | Name | What it is | Sites | Confidence |
|---|---|---|---|---|---|
| `+0xBA0` | ~~2~~ 0x18 | ~~`issuedCommandActionId`~~ `issuedCommandOrder` (`AiOrderRecord`; its `+0` is the old `issuedCommandActionId`) | *Re-cut 2026-09-29 (SWE2-DATA, from OPUS `4e8e01efd`): `+0xBA0`..`+0xBB7` is one embedded `AiOrderRecord`, the issued command's order record — when unit flag `0x4000` is set `SelectAndCommitNextAction` commits `unit + 0xBA0` itself (`00305AE4`–`00305B2F`), so `+0xBA2` / `+0xBA6` are read at record `+2` / `+6` through `+0x708`, and the `0x8000` IssueCommand sets in `+0xBA4` is the record's sign bit tested at `00308736` / `00328604`. Who writes record `+2` and `+6`..`+0x17` is not established.* `BattleUnit_IssueCommand` stores the command's action id here once the status layers admit it (`00311D65`–`00311D7A`), with the commanded actor handle (or its own) at `+0xBB8` and bit 15 of `+0xBA4` (`00311DB0`–`00311DBB`); the status transition keeps unit flag bit 14 only while this is `0x113` or `0x95` (`00300178`–`00300198`), teardown and recover test the same pair, and the display record copies it to `StatusView + 0x5E` under bit 14. Setter found 2026-09-11 (FW-2). | as cited | PROVEN |
| `+0xBC0` | 0x208 | `perceptionCandidates` | a second `BattleTargetBuffer`: `BattleUnit_RebuildPerceptionCandidateCache` clears it preserving bit 0 (`00324857`–`00324872`, `00316D30`) and appends every tracked actor of relation class ≥ 2 while the count `+0xBC4` is below 32 (`00324E9B`–`00324EBB`); `BattleEnmity_PropagateToPerceivingFoes` (`00321A82`–`00321AA1`) and `BattleUnit_HasRelationshipClass2PlusInTrackedActorList` (`0030B056`–`0030B082`) walk it. It ends at `+0xDC8`, where the reservation fields begin. | as cited | PROVEN |
| `+0xDC8`, `+0xE54`, `+0xE58` | 2 / 4 / 4 | `reservedItemId`, `previewGilAmount`, `reservedGil` | already in §2.2 (2026-09-11); the store rows lag the page. | §2.2 | PROVEN |
| `+0xDCC` | 4 | `stanceRecheckDeadlineTick` | `BattleUnit_SeedPartyCombatStanceRecheckTimer` writes `rawTick + (rng & 3) × k + base` when it is 0 and flag bit 23 is clear (`003081E6`–`0030825C`); `BattleUnit_UpdateEngagementStateFlag` writes it (`00307D7C`); `BattleUnit_ComputePartyBattleStance` compares it with the tick (`003081B2`); 0 = due (`0030124A`, `0030F318`). | as cited | PROVEN |
| `+0xDD0` | 4 | `flag30ExpiryTick` | [the periodic page](../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md): the maintenance tick clears unit flag `0x40000000` once the raw tick passes it (`00310DF4`–`00310DFC`); recover-from-terminal writes it (`003012DB`); 0 at reset. | by reference | PROVEN |
| `+0xDD4` | 0x80 | `attackerHitTickBySlot` | 32 dwords indexed by the **attacker's** slot: `Battle_ProcessActionTargetEntry`, on the target unit, stores `rawTick − 10 × trunc(1.0 × −30.0)` = the raw tick counter `0208D45C` plus 300 into `+0xDD4 + sourceSlot × 4` (`00319206`–`0031923F`; `01DFE0B8`, `01CEBCAC`) on the entry's first pass; `FUN_003176C0` zeroes all 32 from the reset (`003176C5`–`003176D3`). The only other readers on the image are `001CF774` / `001D40C7`, whose base is unverified. | as cited | PARTIAL |
| `+0xE70` / `+0xE78` | 8 + 8 | `rewardBaseRow` / `rewardPerLevelRow` | the installer computes each as a table base plus the definition's `+0x22` / `+0x24` index × stride (`0023A994`–`0023A9F4`); `Reward_ComputeExperienceForRecipient` reads `+0x34` of both as `base + perLevel × (recipientLevel − stats + 0x88)` (`002F8C63`–`002F8C85`), `00317090` reads word `+0` the same way into category counter 17 (`003170AA`–`003170D8`), `Reward_ComputeLicensePointsForRecipient` likewise (`002F912B`–`002F9136`). | as cited | PROVEN |
| `+0xE9C` | 4 | `verbFlagWord` | bit 0 = the verb flag bit 14 of `002392D0` (`0023932A`–`00239339`); read by `003229C4`. | as cited | PARTIAL |
| `+0xEA0` | 4 | `inFlightAttackerSlotMask` | bit = the slot of a unit whose action is executing against this one: `FUN_00305230` (from `BattleUnit_AdvanceStandardActionState` `00304850`), for an action row with `+0x2C` bit 6, resolves the source's target focus and sets the source's slot bit in the target's word (`003052F0`–`00305326`); `Battle_ProcessActionTarget` clears it when the row's `+0x2C` has bit 7 (`003074FD`–`00307511`); the cancel clears this unit's bit in every other unit's word (`0031068C`–`0031069C`); teardown requires it zero (`00300EEE`). Setter found 2026-09-11 (FW-2). | as cited | PROVEN |
| `+0xEA4` / `+0xEA8` | 4 + 1 | `committedAttackerSlotMask` / `committedAttackerCount` | on the **target**: the commit, unless the source's flag bit 22 is set, tests the source's slot bit in the target's mask and, when clear, increments the count and sets the bit (`0030F940`–`0030F962`); `BattleUnit_ReleaseTargetRelationAndActionState` reverses both (`003107C5`–`003107EA`); the AI target selector tests the mask against `1 << slot` (`00308D10`, `00303380`) and for zero (`00301D7D`) and treats a count of 3 or more as full (`00301E95`); `00322050` / `00322080` zero both with a re-encode of the actor handle into `+8`. Setters found 2026-09-11 (FW-2). | as cited | PROVEN |
| `+0xEAC` / `+0xEB0` | 4 + 4 | `hpStagePulsePhase` / `hpStageReached` | `002FE950` (from the maintenance tick), for category-`0xF` enemies with a max HP: stage 2 below 51 % HP, 1 below 76 %, else 0 (`002FE995`–`002FE9C2`); when the stage rises it stores the stage and `1.0` (`002FE9CD`–`002FE9D3`); while the phase is positive a sine pulse drives a uniform actor scale through `002E5FD0` and the phase advances until it wraps to 0 (`002FE9DD`–`002FEA8C`). | as cited | PROVEN |

#### 2.6.6 What is genuinely not determinable from this census

~~Fourteen~~ ~~Nine~~ **Six** rows (2026-09-12) have a write or a reset and nothing else on any enumerated route: `+0x06C`,
`+0x158`, `+0x6C0`, `+0x74C`, `+0x758`, ~~`+0xB90`~~ *(answered: `+0xB90` has a reader — operand-store kind 10, corrected 2026-09-30 above; 2026-10-02, OPUS)* — `+0x75C`, `+0x760`, `+0x768` / `+0x76C` and `+0xDD4` gained readers or setters from the
image-wide sweeps (their rows), and **the sub-object-base scan FW-2 asked for (2026-09-12, FABLE)** settled
three more: the action block `unit + 0x6B0` is taken as a base at exactly five sites image-wide
(`0030487F`, `0030F04A` / `0030F0E5`, `0031081E`, and `003CA988` — the last on a different object) and
reaches `00319420` (reads `+0xC4` only), `memset` (the suspend zeroes the `0x4F0`-byte block after copying
it to the heap object at `+0xB88`, which only the restore reads back) and the advance's own `rsi`
accesses — which read `+0x6D4`–`+0x6DC` and `+0x764` (their rows) and none of `+0x6C0`, `+0x74C`, `+0x758`,
`+0xB90`; the locomotion state `unit + 0x80` is taken as a base at fourteen sites in battle code and no
receiver reads `+0x158` or `+0x1A0`–`+0x1A8` (the `+0x1A0` row). The six are write-only on every static
route there is; `+0x1A0`–`+0x1A8` are written from the bands and unread. ~~Four more have readers whose setter is unreached:
`+0x028`, `+0x748`, `+0xBA0`, `+0xEA0`, `+0xEA4` / `+0xEA8`.~~ Those setters were found the same
day by an image-wide sweep for stores through the displacements (the census's routes did not reach
them because they write through the *target* unit resolved from a focus handle, or from a verb
entry): see the rows. The class of evidence that answers
them is static, not live: a write scan seeded on the *action-state block* (`unit + 0x6B0`) and on
the locomotion state (`unit + 0x80`) as sub-object bases — the census's declared blind spot
(§2.3) — and, for the twelve tunables, the FCP property catalogue (FW-1, *answered by consumer 2026-09-26 — see the tunables row* *(answered: see the `+0x164` row; 2026-10-02, OPUS)*). Only the *values'*
distributions would need the game.
## 3. Key addresses

| address | what |
|---|---|
| `0208E688` | the unit pool base; `0208E6A0` ~~the slot count factor (`0xEA7900` per bank)~~ the slot count, `0x20` (`002368EB`–`002368FE`), which the release check multiplies by `0xEA7900` = `0xF50` × `0xF50` *(corrected 2026-10-02, OPUS: `002342AD`–`002342B4`; no bank is involved)* |
| `0031B760`, `00263E30`, `0031B860` | the three unit-returning accessors used as seeds |
| `0023A570` | `BattleUnit_ApplyUnitDefinition` — the installer of `+0x18`, `+0x48`, `+0x698`, `+0x6A0`, `+0xE60`, `+0xE68` |
| `00236A60` | `BattleUnit_ResetStateForReuse` — the reset that precedes every apply |
| `00234200` | `ActorSystem_ReleaseBattleUnitSlotForActor` — the release that zeroes the slot |

### The `00304850` exclusive subtree — all 13 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns `BattleUnit_AdvanceStandardActionState` **13 frontier
functions** — the private machinery under the action-state advance. Interior cites are one
instruction inside each declared extent (`interior_cite.py scan`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| state arms | `00305110` (287 B), `00305430` (517 B), `0030A370` (305 B), `0030D160` (1,004 B), `00339630` (1,061 B) | the advance's state arms — each opens with `0020E600` row lookups (`rax = row_base + id`) and the `0031B7E0` gated query, then drives its own helper set; `0030D160`/`00339630` are the two largest and touch `01CExxxx`/`01F44830`/`02EBF138` | `0030511B` / `0030543B` / `0030A37B` / `0030D166` / `00339635` |
| orchestrator | `00306010` (208 B) | calls `0031B760` (the unit seed), `00328530`, and the `0031B9A0`/`00253760` pair twice — the arm-dispatch layer | `0030601A` |
| `+0x698`-gated predicates | `002FA1A0` (102 B), `0031B9A0` (74 B) | both require `[unit+0x698]` non-null and `[rec+5]==1`: the first computes a `frame / 0x384`, `× 0x4B0` duration from `01DFE0B4` behind two indirect calls; the second runs `00263C20([unit+0x10])` and compares the state to 3 | `002FA1A9` / `0031B9A9` |
| handlers | `00328530` (266 B), `003126E0` (23 B), `00329F80` (209 B) | `00328530` — the `003126E0`→`003125E0` event call plus `0031AA30`/`00290320`/`0030BCB0`/`0030BCD0` and two message-stub sites; `00329F80` a one-call wrapper into `002EACD0`, whose result it also stores at unit `+0x774` (`0032A045`; [GR-17 residue record](../../_index/candidates/gr17-effect-residue-0930/README.md)) | `0032853A` / `003126EB` / `00329F8D` |
| locomotion + effect | `0033A1E0` (94 B), `00469AF0` (192 B) | `0033A1E0` builds the solver context (`00336710` `BattleLocomotion_BuildSolverContext`, `0033D660`, `01F44830`); `00469AF0` — `002F8E90`, two `0020E600` lookups, `0046AB10` | `0033A1F1` / `00469AF8` |

The subtree confirms the field map's picture from the call side: the advance is not one body but
five state arms over the shared `0020E600` row lookup, gated by the `+0x698` sub-record's live
byte, and it hands off to the locomotion solver (`00336710`) and the `00469xxx` effect layer —
the `+0x6B0` action block's runtime half.

### The `00307300` exclusive subtree — all 7 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns `Battle_ProcessActionTarget` **7 frontier functions** —
the outcome-code map, the two-stage id resolver, the flag probe, the timed-marker tracker,
and the dispatch leaf under its target loop. Interior cites are one instruction inside each
declared extent (`interior_cite.py scan`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| outcome map | `002FEE20` `BattleFormula_MapTargetEntryCodeToOutcome` (96 B) | a 12-case jump table: target-entry code `0`–`0xB` → outcome `0,5,1,3,2,4,6,7,8,0xA,0xB`, default 9 — called at `00307557` before the `+0x788` outcome word is assembled | `002FEE39` (`jmp rcx` — the dispatch) |
| singleton probe | `0017D360` (27 B) | `001D50D0()` → `byte [rax+0xC34] != 0` — a shared-singleton flag check the root runs at `0030757C` | `0017D36B` |
| id resolver | `0030AD90` (48 B) → `0030AC50` (305 B) | `0030AD90` extracts `{word [rcx+0x714], word [[rcx+0x698]+0x50]}` when `[rcx] & 0x10`, else `{0xFFFF,0xFFFF}`, and tails `0030AC50` — the two-stage `00322C50`/`0020E600` registry resolve over `02EBF138`: kind `0x14` pass (`id × [rec+8] + row`), kind `6` pass (`(id − 0x1000) × [rec+8] + row`), then a sign-bit test on `[rec+0x24]`/`[rec+0x2C]` returning a `btr 0xF` index or `−1` | `0030ADB3` / `0030AC6E` (`call 00322C50`) |
| marker tracker | `0028E920` (26 B) → `00289D70` (475 B) | `0028E920` is the adapter: swaps the two args, bases `0209BE80 + 0x5380`, tails `00289D70` — the bounded-6 timed-marker pass: `002718E0` position resolve, `+0x428` list walk for the code, `0017D2E0` nibble-pair → duration clamped `0x12`, node decay `×45/60` per tick with recursion, else a free 0x28-stride slot at `+0x256` is claimed `{xyz, code, +0x16\|=1}` and appended | `0028E935` (`jmp 00289D70`) / `00289E14` (`cmp r8d, eax` — the decay/clamp branch) |
| dispatch leaf | `00329F70` (14 B) | `[rcx+8]` non-null → `0046CBB0` — the per-target event dispatch the root calls at `00307727` between the `00328480` pushes | `00329F75` |

`0020E600`/`00322C50`/`002718E0`/`0017D2E0`/`0046CBB0`/`001D50D0`/`0030DAE0` are shared
callees — deliberately not census members. The root's remaining calls (`00328480`,
`002EACD0`, `00377C20`, `00265020`, `00263F40`, `00311F70`, `0026A0D0`, …) are the
published movement/effect layer.

## 4. Data structures and formulas

The store's `BattleUnit` rows (`_types/fields.tsv`) plus the names in §2.2. The full access list is
the TSV beside this page: one row per instruction, with the route that reached it.

## 5. Call chain

Every combat function reaches the unit through one of the three seeds or receives it as an
argument; the TSV's `route` column records which, per access.

## 6. Modding notes

- **Read the unit through its accessors, not by walking the pool**: `ActorWork_GetBattleUnit` is
  what the engine itself uses from an actor, and `BattleStats_FindOwningBattleUnit` from a stats record.
- **A mod that adds state to a unit has 3206 bytes of ranges the enumeration never touches**, but
  §2.3 says why that is not free space: it is where embedded sub-objects most likely live.

## 7. What is not known

- [x] ~~**The bit table of `+0x00`** — 38 writers, each setting or clearing specific bits; the store
  names five bits and the pages a few more.~~ **FF-1** — ANSWERED 2026-09-10 for every immediate
  site: §2.5 lists 33 bits with their setters, clearers and testers, plus five register-mask
  bits from the pages. What each bit *means* is still open per bit; the meanings the pages
  established are the ones cited in §2.5.
- [x] **FF-2.** **What the embedded sub-objects are** — the long untouched ranges (`+0x298`–`+0x68F`,
  `+0x990`–`+0xB8F`, `+0xBD0`–`+0xDC7`, `+0xDD5`–`+0xE53`) and the `addr` rows that take their
  addresses. **FF-2.** Narrowed 2026-09-11: `+0x778`–`+0x97F` is the target buffer (§2.4);
  narrowed again 2026-09-11 (§2.6): `+0x80`–`+0x1FF` the locomotion state, ~~`+0x200`–`+0x297`~~ `+0x200`–`+0x68F` *(answered: see the 2026-09-26 answer below; 2026-10-02, OPUS)* the
  navigation path state, `+0x6B0`–`+0xB9F` the suspended action-state block, `+0x988`–`+0xB87` the
  per-target result pointers, `+0xBC0`–`+0xDC7` the perception candidate buffer, `+0xDD4`–`+0xE53`
  a 32-dword per-slot array. Left: `+0x298`–`+0x68F` — and an image-wide sweep for any
  instruction addressing a displacement in that range (2026-09-11) finds none through a unit base
  (the battle functions' hits are all `rsp`-relative), so whatever lives there is reached only
  through interior pointers or is unused; the same tool's FW-2 run, which found the six unit setters,
  is the control. **Corroborated 2026-09-11 (OPUS-NOTICE-BU298)** from the two functions the census
  is blind to: `BattleUnit_ApplyUnitDefinition`'s twenty displacements and
  `BattleUnit_ResetStateForReuse`'s forty-nine include none in `+0x298`–`+0x68F`, and the eleven
  image-wide `lea` of `+0x298` are all in unrelated ranges — so no static source reaches the span,
  ~~which reads as reserved or padding rather than an embedded object~~; an interior-offset `lea` is the
  one form not yet excluded.
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): `+0x298`–`+0x68F` is entries 1–127 of the navigation path record's waypoint
  table.** The record sits at `+0x200`, its `+0x90` field is `{f32 x, f32 z}[128]`, and so it covers
  `+0x290`–`+0x68F` ([the navigation-mesh page](../../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md) §3).
  - **Why no sweep saw it.** The path builder writes the table by index, `[rec + idx*8 + 0x90]`, and the waypoint
    reader reads it the same way. A displacement or `lea` sweep cannot see an index form.
  - **The size.** The region bound is 128 (the builder's reset loop), and the unit-reuse reset zeroes `+0x80` for
    `0x610` bytes, which ends exactly at `+0x690`.
  - So the navigation path state is `+0x200`–`+0x68F`, not `+0x200`–`+0x297`, and nothing in the range is padding.
  - Control: [`ff2_waypoint_table.py`](../../_index/candidates/ff2-waypoint-table/ff2_waypoint_table.py) (4 checks, FAILS 0).
- [x] ~~**What the outcome word's bits 9, 10 and 11 mean**~~ — **FF-5 ANSWERED 2026-09-11**: bit 8
  is knockback rolled, bit 9 parry rolled, bit 10 the combo continues (flag word B bits 3 / 2 / 1,
  named on [the scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md)
  §2.4); ~~bit 11 is the caller's `r12b` mask (`003075F4`), still unnamed — carried by `FT-4`~~ **bit 11 is flag word B
  bit 0, the mode-2 resource reaction chance rolled** (corrected 2026-09-15, `FT-4`: `r12b` is the local constant 1 from
  `0030746E`, so `test r12b, al` at `003075F4` tests bit 0 — [the scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §7).
- [x] ~~**What `+0x5C` is** — five writers, no enumerated reader.~~ **FF-3 ANSWERED 2026-09-11:** the
  last presentation event id the dispatcher sent (§2.6.1).
- [x] **UQ-96.** **The names of the 128 offsets no page names** — each has cited writers and readers *(closed — the register row is WITHDRAWN.)*
  in §2.2 to start from. **FF-4.** Narrowed 2026-09-11: §2.6 names or classifies every one of
  the 115 store rows OPUS listed; what is left is the meaning behind the PARTIAL rows, the
  twelve tunables' properties (**FW-1**, *(answered: by consumer, 2026-09-26, the `+0x164` row; 2026-10-02, OPUS)*) and the unreached writers (**FW-2**).
- [x] ~~**FF-6.** **What clears unit bit 46 after an action whose definition `+0x0C` has bit 30** *(2026-09-30, FABLE, Claude Opus 5.5)*. Phase 9 sets the bit for every action (`00304EF3`–`00304EFD`). The only clear the image holds is phase 10's, on the other arm (`00304F9F`–`00304FA9`), and the bit-30 arm advances past it (`00304F62`–`00304F8C`). Excluded: any other immediate-mask, bit-test or register-index clear, and the two whole-word writers, which keep the bit ([`bit46_writers.py`](../../_index/candidates/bit46-fable-0930/bit46_writers.py), [`bit46_regindex.py`](../../_index/candidates/bit46-fable-0930/bit46_regindex.py), both FAILS 0). Not excluded: a whole-qword store of a saved or computed value, or a mask loaded from memory. So the only clear found for a unit whose last action had bit 30 is the phase 10 of its next action without it.~~ **FF-6 ANSWERED 2026-09-30** *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's REJECT, [review](../../_index/candidates/auditsem-review-bit46-0930/REVIEW.md) §5)*: the unit's next standard action clears it in phase 0 and phase 6, and so do a cancel, `00308270` and the slot release / allocation memsets: `00304850` phases 0 and 6 (`00304967`–`00304975`, `00304DDD`–`00304DEB`, mask `0xFFFFBFF75FFFCFFF`), a cancel (`BattleUnit_CancelAndResetCurrentAction` `003105D0`, `0031063F`–`0031064B`, same mask), `00308270` (`003082CB`–`003082DF`, mask `0xFFFFBFFFFFBFFFFF`), and the slot release / allocation memsets (`002342CE`, `002344D2`). So a party leader whose last action had bit 30 keeps the capability recompute's all-suppressed mask (`0023B0E6`–`0023B0E9`) only until one of these runs. A bulk copy of a saved unit image (a snapshot restore) is not excluded; that is a narrower question than FF-6 asked.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Every row of the table | `battle-unit-accesses.tsv`; `hop_scan.py --array 0x0208E688:0xF50 --gptr 0208E688 --retseed 0031B760,00263E30,0031B860,0031B7E0,0031B810,00236820 --argseed 00236A60:0,002F9820:0,002FDC30:0,002FDDA0:0,002FED60:0,00305080:0,0030BB30:0,0030C210:0,00311CF0:0,00313400:0,00313480:0,002FA540:0,00307CE0:0,003126E0:0 --size 0xF50 --depth 3`, control `0030FED0:0xE90` found (generation-3 scanner; WIDENED 2026-09-16, OPUS-REQ-STRUCT-WIDEN-FOUR-CENSUS-SEED-LISTS — `--gptr` admits self-discovering pool walkers, the three added retseeds are the handle resolvers, the added argseeds are the type-named functions proven to take the record in arg0; 2,639 rows in 410 functions (2,635 scanner + 4 hand-verified sweep rows) vs the committed 2,207 in 344 — the delta is widened seeds plus scanner-generation drift, not field movement; nine stale `nop`-operand rows dropped by the TWOREG fix; ten type-named functions still absent because their own bodies touch no `[record+disp]` field — adjudication in `Tools/work/STRUCT/widen_four_census_dispositions.tsv`) | 1 | PROVEN |
| The names in the name column | the store rows and the linked pages | 1 | PROVEN (by reference) |
| The untouched ranges | absence on every enumerated route with a passing control | 1 | PROVEN (for those routes) |
| What the untouched ranges and the unnamed fields are | ~~**not established**~~ *(answered in part: `+0x298`–`+0x68F` is the navigation path record's waypoint table, FF-2, 2026-09-26; 2026-10-02, OPUS)* | — | UNKNOWN |

## 9. Related

- [`../battleunit-slot-pool-and-actor-class.md`](../battleunit-slot-pool-and-actor-class.md) — the pool and the actor class.
- [`../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) — the installer.
- [`../Battle-Record-Kind/battle-record-kind-byte.md`](../Battle-Record-Kind/battle-record-kind-byte.md) — the kind byte behind `+0x698`.
- [`../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md`](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) — the spawn record at `+0x6A0`, mapped the same way.
- [`../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) — the stats record at `+0x698`, mapped the same way.
- [`../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) — `+0xE98` and the group ledger.
## 10. The `+0x48` row corrected, and a blind spot in the census — 2026-09-11 (OPUS-REQ-FABLE-EY2)

**Two writers, not one.** `BattleUnit_ApplyUnitDefinition` zeroes the floor on every apply —
`0023ABDB` `mov dword ptr [rdi+0x48], 0`, `rdi` bound to the unit argument at `0023A588` and never
reassigned (OPUS) — the instruction after the `+0x64` / `+0x6C` stores this page already cited. The
only setter is `00239820` (`00239832`), reached solely by the VM thunk `005105E0`, which is the
handler of the script verb **`btlAtelSetHpLowLimit` (`3061`, one int)**. So a non-zero floor can come
from a script and from nothing else.

**The shipped scripts use it constantly, and almost always to write zero.** A byte walk of all 1,115
`us` `.ebp` files for the four call opcodes followed by `3061` finds **6,756 sites in 505 scripts**
(6,746 `CALLPOPA`, 7 `CALL`, 3 `CALLACTPOPA`): 6,723 are preceded by `push 0`, 33 by a
non-immediate push (opcode `0x50` with operands 0–3, or a computed value), and **two push a
non-zero immediate — `dst_a01.ebp` at `0x4926` pushes 67 and `naf_a02.ebp` at `0x4336` pushes
1000**. Which actor each of those targets needs the script decompiled. `EY-2`. *Corrected 2026-09-13:* **23 calls in 14 scripts set a non-zero floor, not two** (corrected 2026-09-13, FABLE, on `OPUS-REQ-FABLE-HPFLOOR-MEANING`, from the 1,114 decompiled `us` scripts): the byte walk counted only integer immediates, and 21 of the 33 "non-immediate" pushes are **float literals**, which the verb truncates (`005105EC` `VMValueStack_PopInt32CoerceFloat32`). Every one sits in a boss's or a mark's own spawn-entry preamble, and **every one of those units registers with event-flag mode 1** — the completion arm that sets the ledger flag and posts `0x2005` ([the group page](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) §5): Gabranth (`bhm_b01` 35,359; `dgl_g01` 32,024 and 12,809), Vayne and his next form (`bhm_c01` 35,877 and 67,105), Cid (`dor_b01` 18,247; `dgl_g01` 41,046), the Onmyoji (`dgl_n01` 222,462), Judge Ghis (`rsn_a01` 824), Ba'Gamnan (`lus_g01`–`g04`, 796 each), Remora (`naf_a02`, 1000), the Rogue Tomato mark (`dst_a01`, 67) and Gilgamesh as four consecutive actors whose floors are **exactly 4 : 3 : 2 : 1** (`lus_c01` 98,482 / 73,861 / 49,241 / 24,620; `lus_e01` 378,596 / 283,947 / 189,298 / 94,649 — the fractional literals are what an authored fraction of a maximum HP would leave). **So a non-zero floor is how an encounter ends — or changes phase — at an authored HP instead of at zero:** reaching it runs the lethal sequence, which completes the unit's mode-1 group, and the map script resumes. Read in one case: `lus_g01` binds `scratch1_var_2` with `sysDVAR(1, …)`, waits on it with `waitv` during the fight, then suspends battle, plays a blur sequence, calls `bosskillall()` / `zakokillall()` and advances the scenario flag — the Ba'Gamnan fight ends by script at 796 HP. The other thirteen scripts share the floor-plus-mode-1 shape but were not read to their event code.

> **Corrected 2026-09-13 (`OPUS-HPFLOOR-NOT-INVULNERABILITY`).** This sentence used to end *"that
> two shipped areas make a unit unkillable below a threshold is now a fact, not a mechanism"*.
> **A non-zero floor does not make a unit unkillable.** The HP write's lethal test compares the
> stored HP against **this same `+0x48` floor** (`0030078B cmp [rsi+0x48], eax` / `jg`, `eax`
> reloaded from the floor slot), so `hp == floor` — the only bottom the clamp can produce *with ordered bounds (floor <= cap)* — falls
> through into the death sequence. A floor of 1000 means the unit runs the lethal sequence **at**
> 1000 HP: the threshold moves up, it does not disappear. See
> [the contract](../../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md) §6 and §9.
> The two shipped non-zero values (67, 1000) stand; only their consequence was misread.
>
> *Qualified 2026-09-27 (OPUS, on FABLE-REQ-OPUS-FIELDMAP-HP-FLOOR-ORDERED-BOUNDS):* with a floor above the effective cap the clamp can store the cap, below the floor - `00300651` / `00300654` jump past every cap test only when the candidate is below the floor, and the cap branch has no floor recheck before `00300749`. The lethal test (`jg` on floor > hp) then fires for that value too. Whether any shipped floor exceeds its unit's cap is not claimed. See the contract's §4 qualification (`63df3d49b`).

**The census behind the `N / N` column has a blind spot at `0023A570`.** `battle-unit-accesses.tsv`
~~holds two rows for it (displacements `0x0` and `0x698`)~~ held two rows for it before the generation-3 re-run *(answered: see §10.1, FZ-16; the file now holds 32 `0023A570` rows, measured; 2026-10-02, OPUS)* while the function touches twenty distinct
unit displacements across thirty instructions: the hop scan follows the argument register and loses
the pointer at `mov rdi, rcx` (OPUS). This page compensated by hand for `+0x64` and `+0x6C`
(`0023ABD1`, `0023ABD6`) and missed `+0x48`. **Any "no writer found" or "N of N accesses" that
rests on that file inherits the gap for the installer's fields** — the `+0x18`, `+0x48`, `+0x698`,
`+0x6A0`, `+0xE60`, `+0xE68` rows this page attributes to `0023A570` are attributed by reading, not
by the census. A second, quieter shape is the block store (AL-8): one displacement marks a write
that covers sixteen offsets, so *no store row at `+0xNN`* never proves *never written* — **7 of
this census's no-write displacements sit inside a wider store's range** (`+0x104/+0x108/+0x114/+0x118`
in `BattleLocomotion_ResetPathAndSetTargets`'s 16-byte clears alone;
`work/STRUCT/blockwrite_overlap.tsv`).
### 10.1 The limit stated where the counts print, and the installer's twenty displacements — 2026-09-11 (OPUS-REQ-FABLE-CENSUS-ROUTE)

> **FZ-16 answered 2026-09-11 (FABLE-PUB140).** The diagnosis below was wrong in one word: the
> scanner did follow `mov rdi, rcx`; what it lost was `rdi` itself at the **`pop rdi` of the first
> early-return epilogue** in address order, after which every callee-saved register was dead for
> the rest of the function. `hop_scan.py` generation 3 no longer treats a pop as a kill, exempts
> frame reloads only inside a real epilogue (one ending in `ret` or a tail `jmp`, allowing the
> security-cookie call and interleaved stores), requires a qword load for a restore, and follows a
> record through its own spill slot. The re-run census holds the installer's thirty accesses at the
> twenty displacements listed below — the table now serves as the reading that verified them — and
> every `N / N` cell on this page is re-counted from it. The bound in the paragraph below is history.

The route limit was recorded in the frontmatter's `method` and in the evidence row, not only here.
The installer's accesses, read from `0023A570` after `mov rdi, rcx` (`0023A588`), are these:

| displacement | access | where | row's conclusion |
|---|---|---|---|
| `+0x698` | read before the copy, write, read | `0023A5A1`, `0023ABFA`, `0023AC29` | count only |
| `+0x40`, `+0x57` | read (the spawn-keep key pair) | `0023A772`, `0023A76E` | count only |
| `+0xEA9` | read | `0023A9EC` | count only |
| `+0xE60` | write (twice) | `0023A915`, `0023ABC3` | count only |
| `+0xE68` | write | `0023A91C` | count only |
| `+0x6E0` | write (twice) | `0023A95E`, `0023AB9F` | count only |
| `+0xE70`, `+0xE78` | write | `0023A9A5`, `0023A9F4` | **"0 writers" → 1** — the reward rows (§7 already named the arithmetic) *(2026-09-30, SWE2-DATA, [GR-17 record](../../_index/candidates/gr17-reward-table-lifetime-0930/README.md): field-addressed stores only; the whole-record memsets `002344D2` (allocate) and `002342CE` (release) also zero both, and are what closes GR-17)* |
| `+0x6F0` | write | `0023ABB5` | count only |
| `+0x64`, `+0x6C`, `+0x68` | write | `0023ABD1`, `0023ABD6`, `0023AC0C` | `+0x68`: **"0 writers" → 1** |
| `+0x48` | write 0 | `0023ABDB` | corrected in §10 |
| `+0x55`, `+0x56` | write | `0023ABF0`, `0023AC11` | `+0x56`: **"0 writers" → 1** |
| `+0x6A0` | write | `0023AC01` | **"1 writer (NULL)" → 2** — the installer stores `SpawnKeep_ResolvePrimaryEntry`'s result |
| `+0x18` | write | `0023AC08` | **"0 writers" → 1** — the definition's text reference |
| `+0x52`, `+0x54` | write | `0023AC14`, `0023AC18` | count only |

Twenty distinct displacements, thirty accesses (OPUS's measurement, reproduced by reading and, since
2026-09-11, by the census itself — `battle-unit-accesses.tsv` carries ~~thirty~~ thirty-two `0023A570` rows *(answered: measured on the file; 2026-10-02, OPUS)*). Six
rows changed a conclusion, marked above; the rest changed a count, and the counts are now the
census's own.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every cited access site in this map was disassembled and its memory displacement compared with the
offset of the row that cites it — **577 sites across 194 rows**, checked mechanically rather than
sampled.

| outcome | sites |
|---|---:|
| the instruction's displacement **is** the row's offset | **432** |
| resolved through an embedded sub-object base (below) | **132** |
| cites the **source object** of a documented cross-object copy | 2 |
| not an access site at all — a data address or a control-flow instruction | 7 |
| indexed form, indeterminate by displacement alone | 4 |

**No site contradicts its row.** But saying so took three corrections to the check, and they are the
part worth keeping.

### The check was wrong three times before the map was

**First:** comparing an absolute field offset against a raw displacement calls 134 sites wrong. They
are not wrong — the base register is already offset into the unit. Subtracting gives a small set of
**sub-object bases**, which §2.1 warns exist but never enumerates:

| base | sites | | base | sites |
|---|---:|---|---|---:|
| `+0x080` | **41** | | `+0x690` | 4 |
| `+0x730` | **18** | | `+0x778` | 4 |
| `+0x6B0` | **16** | | `+0x0F0` | 3 |
| `+0xBC0` | 7 | | `+0x200` | 3 |

34 distinct bases in all. **`+0x80`, `+0x6B0` and `+0x730` alone account for 75 of the 132** — those
three are where the unit's embedded records live, and this is the first time the map has counted them.

**Second:** two sites under `+0x060` write `word [rbx+0xCC]` and `word [rdi+0xCE]` — displacements
*larger* than the row's offset, which no base can explain. They are not accesses to the unit at all:
that row documents a **copy from the render record**, and those two are the render record's own
fields, where the value is produced. A row that describes a cross-object chain cites addresses in the
other object.

**Third:** four "sites" are not code. `02EBF140` and `02EBF148` are `.data`; `008FCC90` and
`009002BC` are `.rdata`. And three more are real instructions that touch no memory —
`0030BE80 test rcx, rcx`, `0031119C je`, `0031082C call` — cited for the control flow around a field
rather than for an access to it.

> **An address in a citation is not automatically an instruction, and an instruction is not
> automatically the access.** That is the fifth trap of this shape in the sweep, and the largest: at
> face value it reported a 23 % error rate in a document that has none.

### What the two `.data` citations turn out to be

`+0xE70` cites **`02EBF148`** and `+0xE78` cites **`02EBF140`** — and both are **registry slots in
the forty** that
[`CONTRACT-authored-table-row-lookup`](../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md)
§15a enumerates.

That closes a three-way join: `+0xE70` and `+0xE78` are the two reward-row pointers
[the experience and licence award](../../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md)
dereferences **without a null check** — and the rows they point at are supplied by the authored-table
lookup, whose resolve *can* fail and return zero. **The award's unchecked dereference and the
lookup's one-sided guard are the same hazard, seen from the two ends of one pointer**, and the field
map is the document that names the slot in the middle.

**Not claimed:** the census's own coverage limits stand unchanged — §2.1's warning about
constructor-side writes, index-register forms and third-hop propagation is untouched by this pass,
which checks what the map *says*, not what it might be missing.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** Six cited functions read `GameClock_GetRawTickCounter`.
- **Resource — SERVICE.** Cited functions call `ResourceTable_ResolveEntryByIndex` and a 28-byte Resource helper.
- **Rewards_Progression_Economy — CLIENT and SERVICE, 35 edges.**
  - Cited unit functions are called by `BattleUnit_ProcessDefeatRewardsAndLoot` (4), `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (3), `Loot_FindOverlappingPickupIndex` (2), a 432-byte rewards body (2) and `Reward_ComputeExperienceForRecipient`.
  - Cited functions call `GameState_SetGil` (5), `GameState_GetGil` (4), `Loot_CollectWorldPickupByIndex` and the defeat-rewards body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**InputGameplay — SERVICE.** `00313DB0` on this page calls `FUN_00313a00`, owned by that layer. What it reaches is a state query that tests the pointer at `[02089350]` and the global equality predicate `00253B90`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `00305640` on this page calls `FUN_00316440`, owned by that layer. What it reaches is a 55-byte achievement gate: bit 5 of `byte[singleton + 0x3845]`, then `00863280(0x13)`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `FUN_0027fb70`, owned by that layer, calls `00300060` on this page. That caller is a 1,237-byte screen-message handler dispatching on `dword[+0]` by successive subtraction, answering messages **1, 2 and 0x12**; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — CLIENT (SWE2-EC7-163, 761 edges).** The field map's subjects are
consulted throughout by the Movement layer — `00202B10` alone is called by
`00334220`/`003347C0`/`00334E00`/`00335B60` — and the `00469410` per-axis
interpolator this page measured is itself called by the Movement-owned
`00468A70`/`00468F70`. Consultation in both directions, no shared ownership.

**Presentation — CLIENT (SWE2-EC7-167, 200 edges).** `003B0980` — the `02EBEC18`
first-zero-field locator this page measured — is called by `003B02A0`, owned by that layer,
and the `0024EE60` re-drive it invokes is called by `003B3300`/`003B2D80`/`003AFFB0`/`003B2BC0`
there; `003B02A0` itself carries `003B0C50`/`003B0B70` edges. The presentation layer consults
the unit's field locator; the locator owns nothing on that side.

**Status — PEER.** `0030EAE0`'s mode-3 lane targets `0030E360`, which sits inside the status layer's own call graph — `0030E990`/`0030F690`/`0030FED0` call it and it calls `00300140`/`00301140`/`0030FED0`/`003876D0`/`00387730` on that layer — the field map cites the shim; the crossing is the status graph reaching the shared mode dispatcher.
**Party — SERVICE (shared-callee edges, SWE2-EC7-188).** The `0033BED0` dispatch's callees `00336040` and `00469A50` both call `003272A0` on the party layer, and its `00338140` arm reaches `0031B7E0` there; the crossing is the unit's dispatch consulting party-layer helpers, not shared responsibility. Edge list from `edges.tsv`.

**CombatAI, Script VM, Spawn/Encounter — CLIENT (shared-callee edges, SWE2-EC7-189).** The dispatch callees and transform helpers my batch-154 entries name (`0033CEF0`/`0033D200`/`0033CE60`/`0033BAA0`/`0033CDE0` kind arms, `00202E90`/`00203170`/`00203080` rotation primitives, `00334E00`/`0033E1F0` turn steps, `003272A0`/`002F8E70`/`00265830` probes) are also reached by the combat-AI layer (`0032A4D0`/`00308610`/`003247F0`-family), the script-VM bridge (`00356160`) and the spawn/encounter lifecycle (`002350C0`/`003070E0`/`00307030`). The crossing is those layers consulting shared helpers this page names, not shared responsibility. Edge list from `edges.tsv`.

*Added 2026-09-29 (FABLE, pass-22 debt): four layers the audit still reported. Group counts are from the rebuilt edge lists; each group is one set of far-end functions, and every edge is in exactly one group.*

**CombatFormula — CLIENT and SERVICE (152 edges in seven groups).** The unit and the formula layer's stats record (`0x1C8` bytes, forty of them from `[02EBF190]+8`) point at each other through `+0x698`, and the formula layer crosses that link in both directions. The record is [the battle stats record](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)'s.
- *F1, the stats-to-unit lookup `0031B860`, 23 edges.* SERVICE, 21: unit-side action, status, reward, movement and formula functions this page cites find the unit that owns a stats pointer through it. The lookup scans the unit pool with `BattleUnit_GetSlotCount` / `BattleUnit_GetBySlotIndex` until `[unit+0x698]` matches (`0031B87D`-`0031B8A4`), which is the other 2 edges (CLIENT).
- *F2, the other stats-unit lookups, 16 edges.* SERVICE, 13: `BattleStats_GetByBattleSlotIndex` `00320A40` and `BattleStats_GetByMappedBattleSlot` `00320AB0` index the forty records (`imul 0x1C8` at `00320A4B`, `00320AC7`), and `BattleStats_ResolveByActorHandle` `00320A70` goes handle, unit, `[unit+0x698]` (`00320A7D`-`00320A94`). CLIENT, 3: `BattleStats_GetOwningActorHandle` `0031E800` walks the pool as F1 does, and `00320A70` calls `ActorWork_GetBattleUnitRaw` `00263E30`.
- *F3, the stats record's writers and the rebuild, 35 edges.* The HP writers `00300520` / `00300530` and the reconcile `0030F340`, the resource writers `00300BC0` / `00300C90` / `00300CE0`, the rebuild `002FEF30` with two of its leaves, and the definition initialiser `0023AC80`. SERVICE, 15: unit-side code writes through them. CLIENT, 20: they call back into unit-side helpers this page cites; for example the secondary-resource writer finds the owning unit and then recomputes `BattleTarget_ComputeGlobalEligibilityMask` `0030B770` (`00300BDD`-`00300BF0`), and the HP writer reaches the lethal-state helpers. [The HP write contract](../../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md) owns the writers.
- *F4, evaluate, resolve and apply a result, 42 edges.* The preview `00385680`, the resolver `00385F60`, the applier `003112F0`, the evaluation context `003847C0` and their leaves. SERVICE, 20: the action code this page cites (`Battle_ProcessActionTarget` `00307300`, the previews `00303830` / `00303A00`, the periodic maintenance `00310DB0`) calls into the chain. CLIENT, 22: the chain reads and writes unit state through page-cited functions; for example the applier computes a gil change from `GameState_GetGil` (`00311A8D`). Owned by [the evaluation context](../../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md) and [the formula scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md).
- *F5, the battle-runtime action-id and persistent-state bodies, 8 edges.* `00386C10`, `00387090`, `00387A50` and `00387B00` find the unit through `0031B860`, cache it at `02EBF188` and read its byte `+0xEA9` (`00386C2E`-`00386C3F`, `00387B32`-`00387B43`): CLIENT, 4. The unit-side activation bodies `00233AD0` / `0023A410` call the prefix reset `00386C10`, and the action advance `00304850` calls the two action-id bodies: SERVICE, 4.
- *F6, table-dispatched roll and recipe bodies, 20 edges, all CLIENT.* Nineteen bodies with no direct caller in `edges.tsv` (they are reached through the formula step and recipe tables). Each finds the unit through `0031B860` and caches it at `02EBF188`, or classifies it with the unit-category classifier `002F8E90`, and then reads unit fields: `BattleFormula_SelectPoachRewardItem95_5` `00390680` reads `[unit+0xE60]` (`003906BD`-`003906CE`), `0038DA00` reads `+0xEA9` (`0038DA1E`-`0038DA2F`). [The step table](../../08-Combat-Formula/Step-Table/combat-formula-step-table.md) owns the dispatch.
- *F7, the per-unit scan `00384F40`, 8 edges, all CLIENT.* A 681-byte formula body that resolves the source unit, then walks every unit `BattleUnit_GetSlotCount` reports (`0038504E`), through eight page-cited functions: the unit count and `BattleUnit_GetBySlotIndexIfUnitFlag4Set` `00321170`, `Actor_GetWorldPosition`, the lookup `0031B860`, the category classifier `002F8E90` and its slot-keyed wrapper `002F8E70`, the field's bit 15 through `00313F60`, and `003A1920`.
- Tier: `0031B860`, `00320A40`, `00320A70`, `00320AB0`, `0031E800` and `002F8E90` read whole; the call sites cited above read; the other far ends are classified by their ledger names and their call direction, not read one by one.

**Items_Equipment_Shops_License — CLIENT and SERVICE, with one MECHANICAL and one OUT-OF-SCOPE group (64 edges in six groups).** Owned by [equipment slots and the single-stat rebuild](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md), [the licence check](../../12-Items-Equipment-Shops-License/CONTRACT-license-check.md) and [inventory class storage](../../12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md).
- *I1, equipment-slot writers, 15 edges - CLIENT.* After a slot changes, `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410` recomputes the stats (`0030FED0` with `0x97`), finds the owning unit (`0031B860`) and re-applies it through `00324470` (`0031A4C2`-`0031A4DF`), which cancels the current action (`003105D0`), may tear the unit down when its stats' status words carry a bit of `0x80000003` outside a bit-15 field, runs three actor routines on `[unit+0x10]`, and sets unit flag bit 6 (`or dword [rbx], 0x40` at `003244E1`); `BattleStats_SetEquipmentSlotByMappedId` `0031A510` does the same and then calls `00324380` (`0031A602`-`0031A60C`), which rebuilds the four-slot id snapshot at `022C257C` from each unit's `[+0x698]+4` (`00324398`-`003243CC`). A gear change reaches the unit only to refresh it.
- *I2, the licence writer and checks, 10 edges - CLIENT and SERVICE.* `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` re-applies the unit through `00324470` for node `0xE5` (`00323A30`-`00323A48`) and shares the recompute and the lookup with I1; the page-cited `BattleStats_HasRequiredLicenseForAction` `00323EC0` calls the licence prerequisite and bit-count helpers (2 edges, SERVICE).
- *I3, gil movers, 11 edges - OUT-OF-SCOPE.* `Shop_CommitPurchaseItemAndGil` `002FEEB0`, `Shop_CommitSaleItemAndGil` `00310870` and the two inventory-bundle gil appliers call `GameState_GetGil` / `GameState_SetGil` and the overflow-message builder `00469E80`, which this page names only as the defeat-reward commit's callees. Gil is party-global, not a unit field; [gil storage](../../13-Rewards-Progression-Economy/CONTRACT-gil-storage-and-movement.md) owns it.
- *I4, inventory and the equipment snapshot, 14 edges - SERVICE and CLIENT.* SERVICE, 3: the action-resource functions `00300280` (refund) and `0030EF20` (prepare) and the applier `003112F0` add or remove an item through `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0` (`003002CB`, `0030EFB0`, `00311457`). CLIENT, 11: the equipment snapshot, restore and unequip bodies read stats through `00320AB0` and refresh the id snapshot through `00324380`; the owned-count query uses `0031B810` and the field bit `00377C20`.
- *I5, loadout evaluation and compatibility, 9 edges - CLIENT.* `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` builds a candidate's derived stats with the rebuild `002FEF30` and the stats accessor `00320AB0`; the compatibility checks ask `BattleDefinition_GetRuntimeCategoryBySelector` `0031EA90` and the id validity test.
- *I6, class-D (bazaar) id flag accessors, 5 edges - MECHANICAL.* Five small accessors reach this page only through `BattleEncodedId_IsValidForClass` `00322C50`, the shared id-validity query read in [the shared neighbours page](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md). Thirteen of the 64 edges run through `00322C50` in all, spread across I1, I2, I4, I5 and I6.
- Tier: `00324380`, `00324470` and the call sites above read; group membership from ledger names and call direction.

**RNG_Random_Selection — SERVICE and CLIENT (7 edges).** SERVICE, 6: four page-cited functions draw from the shared LCG `RNG_SharedGameplayLCG_NextU32` `00328370` - the spawn candidate pick `002355A0` (`002356A3`, `% span`), `00236210`'s bounded top-up (`% 50`, quoted in the SWE2-EC7-107 note), `002394C0` (`00239547`, a bit test on the draw) and `BattleUnit_SeedPartyCombatStanceRecheckTimer` `003081E0` (`003081FF`, `& 3` scaled into the timer) - and two formula bodies draw from the Mersenne Twister through `00379CD0`: the status-timer body `00386C70` and the combo count `00388660`. CLIENT, 1: `BattleData_ResolveWeightedId` `00308EC0`, the LCG's weighted-selection caller, calls `00328370`, which the page names. [Which roll is on which generator](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) §3 lists these draw sites. Tier 1 for the four LCG call sites.

**Save_Load_Settings — OUT-OF-SCOPE (4 edges).** `00236760` and `00236780` are not unit accessors: each is `mov rax, [02EBF190]; mov eax, [rax+4]; shr eax, N; and eax, 1; ret`, bit 12 and bit 14 of the battle-system state's flag dword. The save layer reads them: `SaveloadManager_ShouldAutosaveForTransition` `001C1720` (`001C1758`), `SaveImage_CopyCaptureToWriteSubmissionBuffer` `002EF690` (`002EF696`, which of the two group banks the capture goes to) and `SaveImage_FinalizeHeaderAndChecksum` `00583D60`, which ORs header byte `+0x57` with 1 for bit 12 and with 4 for bit 14 (`00583F5A`-`00583F70`). This page cites the two only as gates on the reward path and in a teardown list; [the save image buffers contract](../../19-Save-Load-Settings/CONTRACT-save-image-buffers.md) owns the bank selector. *Correction to section 11's crossing note:* `00236780` is this flag-bit getter, not "the shared RNG/roll helper". Tier 1: both bodies and all four call sites read.

## 11. Exclusive subtree `00312280` — `BattleUnit_ProcessDefeatRewardsAndLoot` member census — 2026-09-15 (SWE2-FRONTIER)

`00312280` is the 857-byte defeat-resolution body the status machine calls once a unit
reaches a terminal status — the function that turns a kill into experience, licence points,
level-ups, gil and a loot bundle. All five exclusive members verified against the shipping
image; every cite below is interior to the named body.

The body runs in six phases:

1. **Victim classification.** `rdx` is the defeated unit, `rcx` the killer. When the
   victim's `[+0x698]` child exists and its `+5` byte is `1`, and the killer's `+5` byte is
   `0`, `00317ED0` runs first (`003122BF`–`003122D0`). Member `003171C0` then fires the
   licence-notification battery unconditionally (`003122D5`).
2. **Reward eligibility.** The victim's `[+0x698]` child must still read `+5 == 1`
   (`003122EA`); a set bit 3 of `+0xE9A` skips everything (`003122FC` — the "rewards taken"
   flag the `+0xE9A` row already names). If `+0xE9A & 5` is not fully set, the result flags
   `([+0x64] | [+0x3C]) & 2` route through a further `+0xE9A & 2` test, and failing that the
   killer must be a player-side body (`[rbx+5] == 0`, `00312326`).
3. **Roster.** Slots 0–8 are enumerated through `00320AB0(i, 3)`; a candidate whose
   `([+0x64] | [+0x3C]) & 0x80000003` is nonzero must additionally pass `00377C20`
   (`00312374`–`00312389`). Up to nine survivors are stacked into the scratch array at
   `022C1740` (`00312391`).
4. **Per-member award.** For each roster member: `002F8BB0` computes the experience base
   and `002F90C0` the licence-point base, each clamped `0..999999` / `0..999`
   (`003123E5`–`00312406`). If bit `0x10` of the member's `+0x69` or `+0x79` is set, the LP
   award is *redirected*: `r12` accrues `level × LP × 5` (`+0x1C2` is the member's level,
   `00312415`–`00312425`) and the member's own LP add is suppressed. Otherwise
   `00236780` gates the EXP commit (`+0x18C`, capped `0x5F5E0FF` = 99,999,999,
   `00312432`–`00312444`); a level-up loop then advances `+0x1C2` while
   `002F8F20(next level)` returns positive and ≤ the new EXP total (`0031244A`–`00312473`
   — `002F8F20` returning `−1` above level 98 is the loop's natural stop). LP lands in
   `+0x190` capped `0x1869F` = 99,999 (`00312475`–`0031248F`), `00316A50(LP, 0xB)` fires
   the achievement hook, and `0030C650(member, new level, 0)` publishes the level
   (`00312496`–`003124A3`).
5. **Presentation and gil.** The victim's own EXP/LP pair is recomputed with `rcx = 0`
   (`003124B9`–`003124D4`), `00236780` can zero the EXP display (`0031250E`–`00312513`),
   and `0028FB80([+0x8], exp, lp)` posts both floating-text entries (`00312518`). Gil is
   `(victim level − stats +0x88) × per-level-row +0x30 + base-row +0x30 + r12`
   (`00312524`–`00312549` — the two `+0x30` dwords are the gil fields of the `+0xE70` /
   `+0xE78` reward rows in this map), committed through `00253690`/`00254EE0` with
   `00469E80` receiving the clamped overflow (`00312551`–`00312566`).
6. **Loot.** `00265020` fetches the victim position, `00319490` decides whether a bundle
   may spawn there (`0031257E`–`00312597`), `003180F0` rolls the drop array, and
   `00319CA0` spawns it (`003125A1`–`003125B4`). ~~`00317090` closes the record~~ `00317090` (`003125BC`) closes nothing.
   For a spawn-backed victim it adds the reward rows' word `+0` × the level span to **achievement counter `0x11`**
   through `00253770` → `AchievementCounter_UpdateAndMaybeFire` `00316A50`
   ([achievement counters](../../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md)). *(Corrected
   2026-09-28, FABLE, Claude Opus 5.5; the unit-definition page already read it as "game counter `0x11`".)* What
   achievement `0x11` counts is not established here.

| Member | Role |
|---|---|
| `003171C0` (106 B) | licence-notification battery — when the `[+0x698]` child's `+5` is 1, fires `00253770(4, 1)` (`003171E7`); then if `00263C20([+0x10])` ≠ 3 and the `[+0xE68]` record's `+0x52` word ≠ `0xFFFF`, fires `00253750` (`003171FE`–`0031721F`) |
| `0028FB80` (88 B) | `Reward_PublishExpLpPresentation` — pushes two presentation entries onto the manager at `[0209BE80] + 0x5380`: kind 0 (EXP) then kind 1 (LP), via `00289D00` (`0028FBAA`, `0028FBC8`) |
| `00289D00` (107 B) | presentation enqueue adapter — `003588B0` resolves the message id, `002E9D10` packs a 12-byte arg record on the stack, then `00289BD0` enqueues it (`00289D32`–`00289D4C`) |
| `00289BD0` (295 B) | the floating-text queue itself — scans twelve `0x30`-stride slots at `rcx+0xF` for a clear flag byte (`00289C00`–`00289C10`), `003EFD00` renders the number string into `slot+0x10`, its measured length lands in `+0x28` (`00289C5F`), the kind byte in `+0xE`, and the lifetime word `+0x2A = word[01DFE0B4] × 0x3C + (kind == 1 ? 8 : 2)` (`00289C8B`–`00289CA4`); the slot is then appended to the `+0x18`/`+0x20` intrusive list rooted at `+0x420` (`00289CA8`–`00289CE0`) |
| `003180F0` (641 B) | `Loot_RollDropEntries` — builds the seven-entry `{u16 item, u32 count}` result: five common-drop words from the `[+0xE60]` record at `+0x28` stride 2, each gated by `003185D0(chain, i)` or a `0017D340() == i` chain bonus and counted by `003186F0(page, i) + 1` (`003181F8`–`00318231`); two monograph/poach slots from the `+0x42`/`+0x43` chance bytes with `+0x48`/`+0x4A` and `+0x4C`/`+0x4E` item pairs through `00318510` (`0031823A`–`00318283`); the chain multiplier `r12` is `dword[022C3158]`, overridden by `00318820()` when `dword[022C3164] > 0` (`0031815C`–`0031816A`); the drop-page index is scanned against `dword[022C3160]` (`003181D2`); a backward dedup pass folds duplicate item ids into the earlier slot (`003182A0`–`003182C6`); returns 1 when any slot is non-empty |

Crossing note: `00253770`/`00253750`, `00316A50`, `0030C650`, `00253690`/`00254EE0`,
`00265020`, `00319490`, `00319CA0`, `00317090` and `00317ED0` are shared callees outside
the subtree; ~~`00236780` is the shared RNG/roll helper.~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-p22-fable-0930 §2 N1:)* `00236780` is the bit-14 flag getter of the battle-system state's flag dword (`mov rax, [02EBF190]; mov eax, [rax+4]; shr eax, 0xE; and eax, 1; ret`), as this page's pass-22 **Save_Load_Settings** entry (under "Cross-subsystem neighbours — FINAL-AUDIT pass 22") says. None are claimed here.

## 12. The `00238BF0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`BattleUnit_RefreshActorRuntimeFromDefinition` (`00238BF0`, 929 B) is the re-derive
that runs when a unit's definition or mode changes underneath it — the second writer
on this map's `+0x018`, `+0x058` and friends. The body splits on `[+0x698]+5 == 0`
(`00238C5D`–`00238CDA`): the zero side reads `[+0xE60]+0x7A` as a signed speed count
normalised by `float[00848178]` and sets the child `+0xF` byte through member
`00269F30` — 3 when `def+4 − 0x1B ≤ 0xC`, else 2 (`00238C91`–`00238CC3`). The nonzero
side normalises `word[[+0xE68]+0x10]` and the three `[+0xE60]` words `+0xA`/`+0xC`/`+0xE`
against `float[00843134]`, unpacks `[+0xE68]+0x12` bits 4/6 and `[+0xE60]+3` bit 5
(`00238D6C`–`00238D94`), and chooses between the `[+0x6A0]`-bit-5 branch
(`00267CC0` + `0026B4A0([+0x10], 0xA)`) and the `+0x58` category branch — mode 4 is
rewritten to 1 here (`00238DBD`–`00238DC7`, the spawn-record flag interaction the
`+0x058` row already notes) and mode 1 runs `002659A0` + `0025D5E0([+0x10], 0xA)`.

| member | role | interior |
| --- | --- | --- |
| `00269F30` (9 B) | null-gated `+0xF` byte store on the `[+0x698]` child — the runtime sub-category write | [`00269F35`](../../_index/ADDRESS-INDEX.md) |
| `0026AD00` (14 B) | `+0x13` bit-7 = sign-of-`edx` on the `[+0x10]` object — the `neg`/`sbb`/`and 0x80` idiom | [`0026AD04`](../../_index/ADDRESS-INDEX.md) |
| `002E8A10` (93 B) | attach-record flag update: `ctx+0xC0` → word → `0x740`-stride record at `022C6F28` gated on `[+0x284]`; sets `+0x304` bits 12–13 = `edx & 3` and raises `+0x290` bit `0x400000` — called with `r15` = `[+0xE60]+3` bit 5 | [`002E8A4C`](../../_index/ADDRESS-INDEX.md) |
| `002361B0` (89 B) | the category-mode computation feeding `edi`: `[+0x698]+5 == 0` → 1; else from `[+0xE68]+0x18`: bit 4 → {8 or 12}, bit 5 → {1 or 5}, else {0 or 4}, the low choice when bit 6 is set — a {flag4, flag5} × flag6 code | [`002361D6`](../../_index/ADDRESS-INDEX.md) |

The tail (`00238EC4`–`00238F4D`) applies the computed mode to `[+0x10]` through
`0026A7F0`/`0026A7C0`/`00269E20`, re-runs `00236210` when mode bit 1 is set, and
closes with `0026A330` + `00312700`. Shared callees — all deliberately outside the
census: `00267CC0`/`0026B4A0`/`002659A0`/`0025D5E0`, `0026A7F0`/`0026A7C0`/
`00269E20`/`0026A330`, `00236210`, `00312700`, `00269F20`/`00269FE0`/`00269E20`,
`002E5FD0`/`002EC5B0`/`002E8220`, `0026DAC0`/`0026A430`/`0026A3A0`/`0026A330`.

## 13. The `003247F0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`BattleUnit_RebuildPerceptionCandidateCache` (`003247F0`, 1,805 B) is the rebuilder
the `+0xBC0`/`+0xBC4`/`+0xBC8` rows name: it clears the cache preserving bit 0
(`00324857`–`00324872`), walks the tracked-actor list through `00236820`/
`00236850`, filters each candidate through `00263E30`/`0030BCB0`/`00313F60`, and
appends the survivors while `+0xBC4 < 32`. The spatial prefilter and the
visibility test live in the exclusive members.

| member | role | interior |
| --- | --- | --- |
| `0032A4D0` (370 B) | `BattlePerception_TestCachedSpatialVisibilityPair` — the pairwise cache: `1 << byte[+0xEA9]` indexes the per-side bitmask matrix at `022C26A0` (and the revealed bank at `+0x80`); on a cache miss it sets both bits and runs the real test — distance from `+0xE0`/`+0xE4`/`+0xE8` through `00263940` against a `1.0` constant pair, then the LOS helper on context `[02EC1378]` | [`0032A51D`](../../_index/ADDRESS-INDEX.md) |
| `00391710` (659 B) | the spatial-hash cell range — gated on buffer `[02AEE0A0]` non-null, memsets `dword[02AEE0B8]` cells, converts `(pos − radius − origin) / cellSize` to indices via `cvttss2si` with `cellSize = float[02AEE090]`, `dim = dword[02AEE060]`, origins `02AEE070`/`02AEE078`, clamped `[0, dim−1]` | [`0039179E`](../../_index/ADDRESS-INDEX.md) |
| `003919B0` (114 B) | the two-phase adapter — `00391710` computes the cell range into the `0x840` stack block, then `003911D0` walks it with the same `(record, tag, flags)` args | [`003919E2`](../../_index/ADDRESS-INDEX.md) |
| `00468A70` (662 B) | the vision-cone test — early-out when origins coincide, squared-distance gate `(r1+r2)² > d²`, then the FOV: `[rec+0x24]` against `float[01CEBC78]`, `[rec+0x20]` normalised by it, `0x2000` angle units against the table at `01F004E0` | [`00468AF4`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `00324F20`, `00861EC0`,
`00313F60`, `00236820`/`00236850`, `002FFEF0`, `00263E30`, `0030BCB0`,
`00391D10`, `003588B0`, `00263940`, `003911D0`, `00808C40`. The exact pair
produced for `r8 == 0` vs `r8 != 0` in `0032A4D0` (direct vs revealed bank) is
recorded but the bank's reader is left as a named unknown.

## 14. The `00325260` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`BattleUnit_HandleActionTimelineEvent` (`00325260`, 1,215 B) is the authored
action-timeline event dispatcher. It resolves the unit's work object via
`00263E30` (`00325276`), requires bit `0x10` on it (`00325287`), then lets member
`00306BA0` veto (`00325290`: nonzero → return 1). The event byte `[rdx+2]` ≤
`0x83` goes through a two-level jump table — case-index byte at
`rdx+rax+0x20574C` (i.e. `0032574C[op]`) selects one of 11 case slots, the dword
at `00325720[slot*4]` gives the arm offset from the `00120000` base
(`003252AC`–`003252C5`). Of the 132 opcodes, 121 land on the `return 1` arm at
`00325702`; the ten real arms:

| arm | opcodes | behaviour |
| --- | --- | --- |
| `003252C7` | 1 | the authored-table scan: `[+0x698]` flag gate (`+0x64`\|`+0x3C` & `0x80000003` → `00313F60`), the `0208CD18 == 1` first-event check (`00317850`), then four `02EBF138`-section lookups via `0020E600` against `word[+0x714] ≤ 0x21E`, sentinel `+0x24 == 0xFFFF`, flag `+0xC & 0x40000000`, `+0x24 < 0`; survivors loop `+0x77C` slots at `+0x780` stride `0x10`, `003589B0` ID compare vs `+0x710`, `003191B0` per match (`003254E4`–`00325526`) |
| `0032553D`/`00325584`/`003255A1`/`003255BE` | 4 | `003257D0(rbx, 2/4/5/1)` — single-class applicator calls |
| `0032555A` | 1 | the pair arm: `003257D0(rbx, 3)` then `003257D0(rbx, 0xA)` |
| `003255DB` | 2 | inverted flag gate (`00313F60` must return *false*), skip when `[+0x698]+5 == 1` and `([+0xE68]+0x18 & 0xE) == 4`, else `002EACD0` writes `+0x74` (`00325646`), `0026A430` on `+0x10`, then `0033CB10` |
| `00325666` | 1 | `002EB4A0` on `+0x10`, then `+0x690 \|= 2` (`00325695`) — the `+0x690` write the field table cites |
| `003256AC` | 1 | flag gate, then `0030CA50(rbx)` count `+1 > 1` → `002FD0C0(count, byte[rdx+3])` |
| `003256FB` | 1 | `[rbx] \|= 0x80000` — the bit-19 write the field table cites |

| member | role | interior |
| --- | --- | --- |
| `00306BA0` (13 B) | the veto predicate — returns `dword[022C2160] == 5` | [`00306BA2`](../../_index/ADDRESS-INDEX.md) |
| `00317850` (98 B) | the `0208CD18 == 1` first-event consumer — `002EB030` on `[0208CD08]` with `0x2008`, `003589B0` ID → `002EACD0` with flag `0x72`, stores to `0208CD1C`, clears `0208CD18` | [`00317854`](../../_index/ADDRESS-INDEX.md) |
| `003257D0` (552 B) | the class applicator — same flag gate and `+0x714` table scan as the big arm, then walks `+0x77C` slots at `+0x788` stride `0x10` and calls `003176E0(rbx, i)` for every entry whose type byte equals the `edx` class (`003259C4`–`003259E1`) | [`003259C7`](../../_index/ADDRESS-INDEX.md) |
| `0033CB10` (89 B) | the per-category flag setter — when `[+0x698]` exists and `+5 == 0` it uses `byte[+4]` against base `0208D480`, else resolves via `0031B860` and uses `byte[unit+0xEA9]` (~~the perception category~~ the unit's slot index, as this page's `+0xEA9` row and CS-6 say *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))*) against `0208DE80`; sets `dword[base + cat*0x40 + 0x1C] \|= 1` | [`0033CB46`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `00263E30`, `00313F60`,
`0020E600`, `003589B0`, `003191B0`, `003176E0`, `002EACD0`, `0026A430`,
`002EB4A0`, `002EB030`, `0030CA50`, `002FD0C0`, `0031B860`.

## 15. The `0033A240` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`0033A240` (319 B) is the per-unit locomotion-step publisher: it builds a
`0x110`-byte solver context on the stack via `BattleLocomotion_BuildSolverContext`
(`00336710` at `0033A269`), takes the unit pointer the context carries at its
`+0x110` tail (`0033A26E`), and gates on `[+0x698]` present, `[+0x698]+5 == 1`,
`[+0xE68]` present, `kind = (byte[[+0xE68]+0x18] >> 1) & 7 != 0`, `[+0x1F0] &
0x3000` clear, and — when `[unit]` bit `0x12` is clear — `float[+0x158] == +0.0`
(`0033A2D1`). With no override pending (`qword[02089350] == 0`) it dispatches
`kind−1` to the three per-kind solvers — kind 1 → `0033DFD0`, kind 2 →
`0033D890`, kind 3 → the shared `0033DB60` (`0033A2F1`–`0033A322`) — then copies
the context's solved `float4` at `rsp+0xD0` into the unit as
`+0x158`/`+0x15C`/`+0x174`/`+0x160` (`0033A334`–`0033A35E`, called on
`unit+0x80` so the raw stores land at `+0xD8`/`+0xDC`/`+0xF4`/`+0xE0` — this is
the writer the `+0x158`/`+0x15C`/`+0x160`/`+0x174` rows cite).

| member | role | interior |
| --- | --- | --- |
| `00337C10` (372 B) | census pass A — clears `byte[022C7CEB]`, iterates `00236850()` units via `00321170(i)`, and for each unit with `[+0x698]+5 == 1` and flag bit 0 counts those of kind 2 (`00337C89`); the lazy init behind `022C7D04 & 1` in `0033D890` | [`00337C40`](../../_index/ADDRESS-INDEX.md) |
| `00337D90` (937 B) | census pass B — the same unit loop clearing `byte[022C7CEA]` with an extra `003125E0` predicate (`00337DF4`), accumulating the shared step value `float[022C7CE0]` and the `word[022C7CE4]`/`byte[022C7CE6]` counters the kind-1 solver divides by; behind the same `022C7D04 & 1` gate in `0033DFD0` | [`00337DD0`](../../_index/ADDRESS-INDEX.md) |
| `0033D890` (706 B) | the kind-2 solver — when flag bit 0 is clear and `02089340 & 0x20` it just copies `[+0x108]+0xF8`/`+0xBC` into `+0xB0`/`+0xB4` and clears `+0xB8`; otherwise it requires the category record's `+0x1C` ~~bit 1~~ bit 0, value 1 (`0033D953`; the bit `0033CB10` sets at `0033CB60` — same `0208D480`/`0208DE80` bases, indexed by `+0xEA9`, ~~category~~ the slot index); bit 1, value 2, is the solver's own latch, set at `0033DA73` and tested at `0033DA77` *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr8-unit-record-64-0930`](../../_index/candidates/gr8-unit-record-64-0930/README.md); record [`gr8-page-corrections-fable-0930`](../../_index/candidates/gr8-page-corrections-fable-0930/README.md))*, builds the heading basis via `00202FE0`/`00203170`/`00202F00`/`00202B70`/`00202B10`, scales the step by `float[01CEBC78] / max(1,kind2count)` plus `022C7CE0`, and writes `+0xB0`/`+0xB4`/`+0xB8` on the context with `+0x1C \|= 2` when the `008C5F6C` heading limit binds (`0033DA73`) | [`0033D953`](../../_index/ADDRESS-INDEX.md) |
| `0033DFD0` (544 B) | the kind-1 solver — same basis-vector pipeline, but divides `float[01CEBC78]` by `byte[022C7CEA]` (kind-1 count), scales `byte[022C7CE9]` by the quotient, and substitutes `word[022C7CE4] / (0x5A * dword[01DFE0B4]) + float[008FCC90]` when `byte[022C7CE6] == 3` (`0033E05D`) | [`0033E010`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `00336710`, `0033DB60`,
`0033CB70`, `003125E0`, `00321170`, `00236850`, `0031B860`, the
`00202B10`–`00203170` basis family, `004686D0`/`00468700`/`004687F0`, and
`00808C40` (stack-cookie check). `0033DB60` is the kind-3 solver — shared, not
owned by this root.

## The `002392D0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`002392D0` (157 B) is a flags-to-unit-state mapper: `0031B760(edx)` resolves
the unit (null → out, `002392EF`); `bl & 0x10` → `002E83B0(rsi, 0)`
(`002392FB`); `bl & 8` clear → `002EACD0([rdi+8], 1, rdi+8, 0x7B)`
(`00239316`); `bl & 1` → `[rdi+0x1F0] |= 0x1000` (`00239320`); `[rdi+0xE9C]`
bit 0 ← `(bl >> 0xE) & 1` (`0023932A`–`00239339`); and when `[rdi+0x6A0]`'s
low byte has neither bit 0 nor 2, `00321810(rdi, ~bl >> 0xF & 1)`
(`0023934B`–`00239358`).

| member | role | interior |
| --- | --- | --- |
| `002E83B0` (80 B) | attach-record flag writer — `word[[rcx+0xC0]]` (≠ `0xFFFF`, `[rcx] ≠ -1`) × `0x740` into `[022C6F28]`; when `[rcx+0x284]` nonzero: `byte[+0xD2] &= ~2`, then `edx` → `\|= 2` (`002E83EC`–`002E83F9`) | [`002E83D3`](../../_index/ADDRESS-INDEX.md) |
| `00321810` (47 B) | flag-byte writer + tail — `byte[[rcx+0x6A0]+0x19] = edx ? 1 : 0` when the `+0x6A0` object exists, then tail `00321DC0` (`00321831`–`00321839`) | [`00321824`](../../_index/ADDRESS-INDEX.md) |
| `00321DC0` (127 B) | per-slot iterate-and-clamp — loops `ebx` over `00322C50(1, ebx)` checks, clamping `esi` into `[0, 0xFF]` (`r14d = 0xFF`, `cmovg`/`cmovs` at `00321E07`–`00321E12`) | [`00321DF0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0031B760`, `002EACD0`, `00322C50`.

## The `00300E40` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`BattleUnit_TeardownAndDespawn` (`00300E40`, 458 B exclusive) is a
teardown-then-rematerialize pipeline: `00300FC0` + `003105D0` open
(`00300E59`/`00300E61`), `00319E30` and `00322050` release mid-state
(`00300ED5`/`00300EFC`), `00301310` walks the roster (`00300F0A`), then
`003125E0`, `0026DC60`, `00237080` (`00300F35`/`00300F45`/`00300F68`), a full
`0023A570` unit-definition re-apply (`00300F75`), `00236760`, `0025AB30`,
`002697E0`, a second `003105D0`, and tail `003138D0` (`00301005`).

| member | role | interior |
| --- | --- | --- |
| `00237080` (29 B) | `SpawnEntry_ClearSelectionTransientStateForTeardown` — null-gated field reset: `[rcx] &= 0xFFFFFF7A` (clears bits 0/2/7), `word[+0x16] = 0xFF`, `dword[+0x78] = 0`, `byte[+0x7C] = 0` (`00237085`–`00237098`) | [`0023708B`](../../_index/ADDRESS-INDEX.md) |
| `002697E0` (7 B) | thunk → `00269860`: stats-record refresh comparing `word[+0x1DE]` vs `word[+0x1D6]` (`0026980F`–`00269822`), `00358940` rebind on mismatch (`0026982B`) | [`002697E2`](../../_index/ADDRESS-INDEX.md) |
| `00301310` (422 B) | roster-walk teardown — iterates the `022C1788` list (`0030132E`), `0031B810` resolves each unit's `[+0x698]` stats record (`00301344`–`00301351`), keeps only `dword[+0x64] & 0x80000003` members through `00377C20` (`00301363`–`0030136B`), bound `4` on `rbx`/`edi` (`00301374`/`00301386`), default `ebp = 0x115` (`00301398`), reads `[rcx+0xBB8]` (`003013AE`) | [`00301363`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00300FC0`, `003105D0`, `00319E30`,
`00322050`, `003125E0`, `0026DC60`, `0023A570`, `00236760`, `0025AB30`,
`003138D0`, `0031B810`, `00377C20`, `00358940`, `00269860`. (`00229ED0` and
`00861EC0` seen adjacent belong to sibling `002370A0`, not this subtree.)
The `0x80000003` mask is the same party-eligibility word the
defeat-rewards walk uses (`00312280` subtree, §12).

## The `00308610` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`BattleUnit_UpdateCombatFrame` (`00308610`, 550 B) is the per-frame combat
pipeline: `003E7DE0`/`003299B0`/`0030DA30` open (`00308634`–`00308650`),
`0033A240` (`0030867A`) then `00307DF0` (`00308682`), `00308270` +
`003105D0` (`003086AA`/`003086B2`), the `022BE981`/`022BE984` byte ops
(`003086BB`–`003086DA`), `00237670` (`003086E9`), `002FFB60`
(`003086FC`), `00305AB0` + `00307BE0` (`0030874C`/`00308754`),
`00253B90` (`0030877D`), `0030FA00` (`0030879F`), with `00308270` /
`00316D30` tails and `00316CF0` (`0030880E`).

| member | role | interior |
| --- | --- | --- |
| `002FFB60` (385 B) | flag-mask writer + state-code gate — `[rbx] &= rcx` (`002FFB90`–`002FFB93`), `word[+0x714]` vs `0x414E` / `0x21E` compares (`002FFB96`/`002FFBC3`) | [`002FFB96`](../../_index/ADDRESS-INDEX.md) |
| `00307DF0` (115 B) | status-gated action — `[+0x698]` stats `byte[+5]` must be nonzero and `02089340` bit `0x20` must be set (`00307E0A`–`00307E12`), then `(dword[+0x64] \| dword[+0x3C]) & 0x8000201B` gates `00308130(rbx)` (`00307E22`–`00307E33`) | [`00307E28`](../../_index/ADDRESS-INDEX.md) |
| `00313F20` (50 B) | multi-gate guard — `word[+0x714]` vs `0x21E` (`00313F2E`), `byte[+0x6B4]` vs 9 (`00313F37`), `dword[rcx] & 0x800000` (`00313F40`), tail `00313400` (`00313F4C`) | [`00313F40`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003E7DE0`, `003299B0`, `0030DA30`,
`0033A240`, `00308270`, `003105D0`, `00237670`, `00305AB0`, `00307BE0`,
`00253B90`, `0030FA00`, `00316D30`, `00316CF0`, `00308130`, `00313400`.
The `0x8000201B` mask composes the party word `0x80000003` with bits
`0x18`/`0x10`/`0x8`/`0x2`/`0x1` — the status-id family the suppression
recompute (`0023B040` subtree) publishes against.

## The `0030AF30` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`BattleAction_CheckAndHandleExecutionTimeout` (`0030AF30`, 501 B): loads
the `01DFE0B8` float pair (`0030AF50`/`0030AF77`), runs `004697C0`
(`0030B035`), then the `00290540` verification chain (`0030B03D`),
`0031B760` resolves the unit (`0030B085`), `0030AB40` closes
(`0030B098`).

| member | role | interior |
| --- | --- | --- |
| `00289F50` (289 B) | record-match verifier — saves `[01F44830]` (`00289F5F`), `002718E0(edi)` must pass (`00289F7D`), then compares `[rsi+0x430]`'s `dword[+0xC]` / `dword[+0x14]` against `edi` / `ebx` (`00289F8A`–`00289F9B`) | [`00289F96`](../../_index/ADDRESS-INDEX.md) |
| `00290540` (80 B) | two-call verification chain — `[0209BE80]+0x10F78` context into `00296E00(rcx, ebx)` (`0029054F`–`0029055D`), `00273320(ebx)` (`00290564`), tail `00289F50` (`00290585`) | [`0029055D`](../../_index/ADDRESS-INDEX.md) |
| `00296E00` (132 B) | slot-validity predicate — `byte[rcx+0xB42]` count vs `bl` (`00296E1B`), `0035D320` index resolve then `[rax+rcx+0x24]` vs `esi` (`00296E23`–`00296E30`), `qword[rdi+0x880]` nonzero check (`00296E53`) | [`00296E1B`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `004697C0`, `0031B760`, `0030AB40`,
`002718E0`, `00273320`, `0035D320`. `00296E00` and `00289F50` are reached
through `00290540`, not from the root directly.

## The `00300FC0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`00300FC0` (371 B) is the teardown prelude `00300E40` opens with: reads the
`[+0x698]` stats `byte[+5]` / `byte[+4]` (`00300FDF`/`00300FE7`, the `+4`
against `0xC`), `003105D0` / `00310780` releases (`00300FF4`/`0030100D`),
`002ED180` on `dword[rbx+8]` (`00301015`), `0026DAC0` / `0026A330` on
`[rbx+0x10]` with `xmm1 = -1.0f` (`00301028`–`00301043`), `003219D0` /
`002372E0` (`0030105E`/`00301063`), `02089340 |= 0x400` (`0030106C`), tail
`003138D0` (`00301005`).

| member | role | interior |
| --- | --- | --- |
| `002373C0` (88 B) | party-eligibility gate — `003137F0`/`0031B770`/`003135C0` resolve chain (`002373C6`–`002373D5`), then `[rbx+0x698]`'s `dword[+0x64] & 0x80000003` (`002373EF`–`002373F5`) before `00313F60` (`002373FC`) | [`002373F5`](../../_index/ADDRESS-INDEX.md) |
| `002ED180` (83 B) | attach-record clear — `003588B0` → `word[[rax+0xC0]]` (≠ `0xFFFF`) × `0x740` into `[022C6F28]`, `[rcx+0x284]` nonzero gate, tail `003E6B40` (`002ED1C9`) | [`002ED1B3`](../../_index/ADDRESS-INDEX.md) |
| `003E6B40` (12 B) | multi-exit thunk table — `jmp` forwarders to `00512EE0`/`00512F30`/`003E3120`/`003E31C0`/`003E31E0`/`003E3320`/`003E33A0`/`003E33C0`/`003E33E0` (`003E6B47`–`003E6BC7`) | [`003E6B47`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003105D0`, `00310780`, `0026DAC0`,
`0026A330`, `003219D0`, `002372E0`, `003138D0`, `003137F0`, `0031B770`,
`003135C0`, `00313F60`, `003588B0`. `002ED180` uses the same `022C6F28` /
`0x740`-stride attach table as `002E83B0` (`002392D0` subtree).

## The `00234200` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00234200` = `ActorSystem_ReleaseBattleUnitSlotForActor` (~215 B):
`00263E30` unit resolve (`00234210`), member `00263980` word read
(`00234220`), member tail `003589A0` (`00234232`); the release arm
runs `00300140(rbx, 1)` / `00319140(rbx, 2)` (`0023423F`/`0023424C`),
reads the stats record `[rbx+0x698]` (`byte[+5]` vs 1, `dword[+0x64]`,
`0023425D`/`00234268`), `00313F60` (`00234275`), copies
`dword[rbx+0x160]` → `dword[[rbx+0x6A0]+0x74]` — the yaw into the
spawn record (`0023429E`), bounds-checks `rbx` against the
`0208E688`/`0208E6A0` BtlWork array (`002342A8`/`002342AD`), and
~~frees~~ zeroes the slot through `00861EC0` *(corrected 2026-10-02, OPUS: a `memset` thunk — `002342C3 xor edx, edx` / `002342C5 mov r8d, 0xF50`)* with stride `0xF50` (`002342CE`) —
the same `0xF50` `BtlWork` stride `002368D0` builds.

| member | role | interior |
| --- | --- | --- |
| `00263980` (4 B) | word getter — `movzx eax, word[rcx]; ret` | [`00263980`](../../_index/ADDRESS-INDEX.md) |
| `003589A0` (8 B) | byte getter — `movzx eax, byte[rcx+3]; ret` (the `003589B5` body is a sibling) | [`003589A0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00263E30`, `00300140`, `00319140`,
`00313F60`, `00861EC0`.

## The `00307C70` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00307C70` (158 B) — a flag-gated dispatcher on `qword[rcx]`: bit
`0x4000000000000` → `002E7290` on `[rbx+0x10]` (`00307C7C`–`00307C8F`);
bit `0x8000000000000` → `002E72E0` (`00307CAB`–`00307CBE`); on a zero
result the flags are cleared — `and qword[rbx],
0xFFFBFFFFFEFFFFFF` (`00307C98`/`00307CA2`).

| member | role | interior |
| --- | --- | --- |
| `002E7290` (79 B) | mode-3 check — `[rcx+0xC0]` null-gate, `dword[rax] == -1` / `cx == -1` (`002E72A1`/`002E72A9`), `rcx += [022C6F28]` then `dword[+0x284]` (`002E72BD`/`002E72C6`), `edx = 3` (`002E72CF`) | [`002E72C6`](../../_index/ADDRESS-INDEX.md) |
| `002E72E0` (79 B) | mode-4 twin — identical shape, `edx = 4` (`002E731F`) | [`002E731F`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none — the members are leaf checks
over the shared `022C6F28` attach-record table.

## The `00383620` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00383620` `Navigation_BuildOrReusePathXZ` (~80 B) — packs the XZ
endpoint record on the stack (`[rcx]`/`[rcx+8]` → `[rax+0x10]`/
`[rax+0x14]`, `[rdx]`/`[rdx+8]` → `[rax-0x18]`/`[rax+8]`/`[rax+0xC]`,
`00383627`–`0038365B`), then enters `00382FF0` (`00383660`).

| member | role | interior |
| --- | --- | --- |
| `00382FF0` (1,575 B) | the path-search body — `(rcx, rdx, r8, r9d)` arg spill (`00383017`/`00383024`), calls `00383850` | [`00383017`](../../_index/ADDRESS-INDEX.md) |
| `00383850` `Navigation_EvaluatePortalTraversalCost` (368 B) | portal traversal cost — `[02AEDFB0]` context + `dword[+0x1C]` (`00383863`/`00383874`), `_hypotf`, `00382EA0` `Geometry_DistancePointToSegmentXZ`, `0020E600`, `0032A780` | [`00383874`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `_hypotf`, `0020E600`, `0032A780`,
`00382EA0`, `00383A30`, `00383C90` (the last two belong to sibling
`00383670` `Navigation_SelectNextWaypointXZ`).

## The `00383670` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00383670` `Navigation_SelectNextWaypointXZ` ~~(1,223 B)~~ (204 B) *(answered: see the 2026-09-19 correction below; the body ends at `0038373B ret`; 2026-10-02, OPUS)* — the waypoint
select: `00383A30` called twice (both endpoints' region-polygon
containment, `003836B8`/`003836D0`), `00383C90` portal-clearance
adjust (`003836ED`), then a battery of `[02AEDFB0]` + `0020E600` row
lookups (`00383779`–`00383800`+).

| member | role | interior |
| --- | --- | --- |
| `00383A30` `Navigation_IsPointInsideRegionPolygonXZ` (591 B) | region-polygon containment — `edx` region vs `0xFF` bound (`00383A41`), `[02AEDFB0]` context (`00383A55`) | [`00383A41`](../../_index/ADDRESS-INDEX.md) |
| `00383C90` `Navigation_AdjustPortalWaypointForClearance` (632 B) | portal waypoint clearance — `[02AEDFB0]` context (`00383CA6`), `(rcx, rdx, r8)` → `rsi/rbp/r12` (`00383CBC`/`00383CC8`) | [`00383CA6`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0020E600`. The `02AEDFB0` cell is
the shared navigation-data context all three functions consult.

*Correction and pointer (2026-09-19, FABLE).* `00383670` is **204 B**, not 1,223; the battery of `[02AEDFB0]` row
lookups at `00383779`-`00383800` belongs to the next body, `00383740`, which returns the mesh grid's rectangle. What
these bodies do - the region search, the waypoints, and that this record's byte `+0x1F4` is the **mover class** a
portal is opened or closed for - is on
[how a unit finds its way across the navigation mesh](../../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md).

## The `003057D0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`003057D0` (58 B) — a gated clamped-float write. Requires `qword[rbx+0x698]`
non-null with `(dword[+0x64] | dword[+0x3C]) & 0x80000003` nonzero and
`00377C20` returning 0 (`003057EB`/`003057F6`), bits 19 set and 20 clear on
`[rbx]` (`00305806`/`00305811`), and `00264490([rbx+0x10])` nonzero
(`00305820`). On pass it loads `xmm8 = float[rbx+0x19C]`, computes
`maxss(0, 002638F0([rbx+0x10]) - xmm8)` into `xmm6` (`00305863`), stores
`xmm8 + 0.02f` back to `[rbx+0x19C]` (`00305854`/`00305867`), then calls
`00269E20([rbx+0x10], xmm6)` (`00305873`) — a per-call +0.02 accumulator
feeding the clamped delta downstream.

| member | role | interior |
| --- | --- | --- |
| `002638F0` (25 B) | safe float getter — `[rcx+0xC0]` null → `xorps`; else `movss [rax+0x140]` (`00263904`/`002638FC`) | [`002638FC`](../../_index/ADDRESS-INDEX.md) |
| `00264490` (33 B) | safe bit getter — `rcx`/`[rcx+0xC0]` null → 0; else `(byte[+0x151] >> 1) & 1` (`002644A1`/`002644AA`) | [`002644A1`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00377C20`, `00269E20`. The `+0xC0`
sub-object carries `+0x140` (float) and `+0x151` (flag byte); `+0x698` is
the gate object on the battle unit.

## The `00233AD0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00233AD0` (`BattleUnit_ActivateAppliedDefinitionRuntime`, ~300 B) —
`0031B760(rcx)` resolves the applied definition (`00233ADD`), null →
return; `test byte[rax], 4` selects the kind-1 arm (`00233AEE`) whose
`+0x48`/flag-word writes ~~set `ACTIVATION_COMMITTED` (bit 1)~~ clear bit 26 (`00233AFB`) and set bit 3 (`00233B4B or dword ptr [rbx], 8`) *(corrected 2026-10-02, OPUS: bit 1's setter is `00300F2A`)* as documented
in the flag table above.

| member | role | interior |
| --- | --- | --- |
| `0037C8C0` (13 B) | safe `byte[+0x23]` getter — null → `al = 0` (`0037C8C5`/`0037C8CA`) | [`0037C8C5`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0031B760`.

## The `00305E70` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00305E70` (~27 B) — null-gate, then `qword[+0x698]` (`00305E79`/`00305E7E`).

| member | role | interior |
| --- | --- | --- |
| `003271E0` | `00327150()` non-null gate (`003271E4`/`003271EC`) | [`003271E4`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00327150`.

## The `0030BD00`/`0030CFB0`/`0030EC00`/`0030EFF0`/`00310780` exclusive-subtree quintuple — all 5 roots bound (SWE2-FRONTIER, followup queue)

`0030BD00` (`BattleTarget_MatchesRelationMode`, 7 B) — `movsxd rbp, r8d`
index prologue.

| member | role | interior |
| --- | --- | --- |
| `00321840` | `edx = 0` then `jmp 00321770` — mode-0 forward (`00321840`/`00321842`) | [`00321840`](../../_index/ADDRESS-INDEX.md) |

`0030CFB0` (`BattleAction_AcquirePresentationSlot`, 185 B — ~~229 B~~; the `ret` sits at `0030D068`, then int3 pad to `0030D070`; 229 B was the allocator `0030D070`'s size *(corrected 2026-10-02, FABLE)* ) —
`byte[+4] == 0xFF` compare, `movzx r8w` (`0030CFBF`/`0030CFC3`).

| member | role | interior |
| --- | --- | --- |
| `0030D070` | `022C17B0` scan with `0xFFFF` sentinel, ~~`r8b = 0` found flag~~ `r8b` = the slot index, 0 to 31 (`xor` at `0030D088`, bound `cmp r8b, 0x1f` at `0030D090`, index `movsx rax, r8b` at `0030D096`) *(corrected 2026-10-02, FABLE; strike placed on the page's own former words 2026-10-03, OPUS)* | [`0030D078`](../../_index/ADDRESS-INDEX.md) |

`0030EC00` (`BattleAction_ResolveSpecialSequenceTargets`, ~66 B) —
stack-cookie `0x198` frame (`0030EC0C`).

| member | role | interior |
| --- | --- | --- |
| `00317670` | `1.0 x 01CEBCAC` -> `cvttss2si`, `x5` scale, `0208D45C` read (`00317670`/`0031768B`) | [`00317670`](../../_index/ADDRESS-INDEX.md) |

`0030EFF0` (`BattleUnit_SnapshotAndSuspendActionState`, ~112 B) —
`bt dword[rcx], 0x18` (`0030EFFA`/`0030EFFF`).

| member | role | interior |
| --- | --- | --- |
| `0030DFA0` | `022BEFB0` table walk, `& 7` slot masking (`0030DFA2`/`0030DFB6`) | [`0030DFA2`](../../_index/ADDRESS-INDEX.md) |

`00310780` (`BattleUnit_ReleaseTargetRelationAndActionState`, ~10 B) —
`qword[+0x698]` null gate (`0031078E`).

| member | role | interior |
| --- | --- | --- |
| `00317E50` | `ecx = 1, edx = 0` then `jmp 0025AAD0` — mode-1 forward (`00317E50`/`00317E55`) | [`00317E50`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00321770`, `0025AAD0`.

## The `00319F50`/`003204E0`/`00323EC0` exclusive-subtree triple — all 3 roots bound (SWE2-FRONTIER, followup queue)

`00319F50` (`BattleUnit_HandleActorTimelineEvent`, ~7 B prologue into a
`0x180` stack-cookie frame — `00319F5D`/`00319F67`).

| member | role | interior |
| --- | --- | --- |
| `00313F70` | `and dword[rcx], 0xFFFFFEFF` — clears bit 8 (`00313F70`) | [`00313F70`](../../_index/ADDRESS-INDEX.md) |

`003204E0` (~~~33 B~~ **255 B**; the 33 bytes are its first unwind fragment, the five-register prologue — 2026-09-29, OPUS, `CON-173`) — five-register body.

| member | role | interior |
| --- | --- | --- |
| `002ECE80` | `rcx`/`qword[+0xC0]` non-null, `dword[rax] == -1` sentinel probe (`002ECE83`/`002ECE91`) | [`002ECE83`](../../_index/ADDRESS-INDEX.md) |

`00323EC0` (`BattleStats_HasRequiredLicenseForAction`, ~61 B) — `r8d =
0`, `rsi = rcx`, `ebx = edx` (`00323ECA`/`00323ED0`).

| member | role | interior |
| --- | --- | --- |
| `0030A330` | `r9 = rcx` null-checked scan, `r8d = 0` index (`0030A330`/`0030A340`) | [`0030A330`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hubs `004686D0` / `002EACD0` / `004687F0` (2026-09-17, SWE2-EC7)

Three field-map helpers, all read against the shipping image:

- `004686D0` (35 B, 14 A-callers) — the named `Vector3_ComputeXZDistance`: loads `[rcx].x/.z`,
  subtracts `[rdx]`, squares and adds at [`004686E2`](../../_index/ADDRESS-INDEX.md)–`004686EA`,
  tail `jmp 00861F14` (the sqrt thunk). Returns squared-XZ-distance's sqrt via the tail.
- `002EACD0` (42 B, 11 A-callers) — the `attachedEffectHandle` creator this page cites as
  `002EACD0(actorHandle, 1, &+8, 0x78)`. Interior verified: `edx == 0` short-returns 0; otherwise
  it forwards `rcx`/`r8`/`edx` into `003B02A0` with a **fixed fifth stack arg of 5**
  (`mov dword [rsp+0x20], 5` at [`002EACE5`](../../_index/ADDRESS-INDEX.md)) — a typed-handle
  request wrapper that pins the mode, not a constructor.
- `004687F0` (144 B, 10 A-callers) — sibling of `004686D0`'s family: builds the vec4
  `{[rcx+8], 0, [rcx], const}` on the stack, runs `00469320` + `00202D20(&rec)` + `0046F460`
  (first call [`00468840`](../../_index/ADDRESS-INDEX.md)), then conditionally scales the result
  when `0.0 > [rbx]` — a projected-distance helper with a sign-side scalar.

NOT claimed: `002EACD0`'s mode-5 meaning in `003B02A0`'s dispatch, or `004687F0`'s constant.

## Interior citation — frontier hub `00321170` (2026-09-18, SWE2-EC7)

`00321170` — 26 B, 8 A-measured callers; `BattleUnit_GetBySlotIndexIfUnitFlag4Set` — the census
name is exact. Interior verified: `rcx` passes straight through to `BattleUnit_GetBySlotIndex`
(`00236820`) at `00321174`; on a non-null unit, [`0032117E`](../../_index/ADDRESS-INDEX.md) tests `byte[unit] & 0x10`
and returns the unit only when the flag is set, else `rax = 0`. The `0x10` bit is the
unit-present/enabled flag this map's `+0x00` byte carries.

## Interior citation — frontier hubs `00202FE0`, `0026B0C0` (2026-09-18, SWE2-EC7)

`00202FE0` — 67 B, 7 A-measured callers; the lane-wise vec4 multiply beside `00202B10`'s
add. Interior verified: `dst[i] = xmm2[i] * dword[rdx + i*4]` for i = 0..3 via four scalar
`mulss` lanes staged through `rsp` at [`00202FEA`](../../_index/ADDRESS-INDEX.md)–`00203011`, one `movups` store.
Component-wise scale, no horizontal ops.

`0026B0C0` — 165 B, 7 callers; the `[+3]>>5` tag-dispatch float writer in the same variant
family as `00265200`/`002D45C0`. Interior verified: tag 1 writes the three `xmm1`–`xmm3`
floats three times into `[+0xB8]`'s sub-record at `+0x00/+0x10/+0x20` strides and sets
`[rax+0x5D]` bit 0 at [`0026B120`](../../_index/ADDRESS-INDEX.md); tag 2 instead runs `002EB930()` then
`002E5C70(rcx)` + `002E4A10(rcx)` (`0026B0F4`–`0026B113`); other tags no-op. Position-write
vs deferred-dispatch on the same record.


## Interior citation — frontier hub `00263F40` (2026-09-18, SWE2-EC7)

`00263F40` — 44 B, 29 callers (5 A-measured); the resolve-or-self on the `+0x18` kind byte.
Interior verified: `[rcx+0x18] == 1` (`00263F46`) routes to `003587C0(sign-extended
byte[+0x19], word[+0x1A])` at [`00263F57`](../../_index/ADDRESS-INDEX.md) and the result
replaces the return (`cmovne` at `00263F5F`); every other kind returns `rcx` itself. Kind 1 is
a reference record; the rest are already the unit.


## Interior citation — frontier hubs `00263C20`, `0031B760` (2026-09-18, SWE2-EC7)

`00263C20` — 16 B, 23 callers; `ActorRuntime_GetClassNibble`. Interior verified:
null-guarded (`00263C22` returns 0), then `movzx eax, byte [rcx+0xE]` +
`and eax, 0xF` at [`00263C25`/`00263C29`](../../_index/ADDRESS-INDEX.md) — the class nibble is
the low half of record byte `+0xE`.

`0031B760` — 13 B, 61 callers; `ActorWork_GetBattleUnit`, one of the three unit-returning
accessors this map's seeds use. Interior verified: null `rcx` returns 0
(`0031B763`), else `jmp 00263E30` at [`0031B768`](../../_index/ADDRESS-INDEX.md) — the real
accessor is `00263E30`; this wrapper only adds the guard.

## Interior citation — frontier hub `00320940` (2026-09-18, SWE2-EC7)

`00320940` — 117 B, 9 callers; `FieldData_GetFormat0RecordVectorBy*` confirmed: it delegates
to `003DFD00(id, 0, &tmp)` (`00320961`) and, on success, copies the returned vec3 out of the
stack record into `[rbx]`/`[+4]`/`[+8]` ([`00320998`](../../_index/ADDRESS-INDEX.md));
failure returns `-1` with the out-param untouched. The field-data format-0 row's position
triple, surfaced to battle-unit construction.

## Interior citation — frontier hub `002E9600` (2026-09-18, SWE2-EC7)

`002E9600` — 36 B, 8 callers (four CombatAction bodies: `00305110`, `00305230`, `00305430`,
`00307300`, plus Status's `00301140`); the "does this unit's linked record carry bit 3"
predicate. Tag gate `byte [rcx+3] & 0xE0 == 0x60`, then requires `[rcx+0xC0]` non-null and
returns `byte [[+0xC0]+0x10] >> 3 & 1` ([`002E961A`](../../_index/ADDRESS-INDEX.md)); every
other shape returns 0. The combat rows consult it when an action needs the unit's
secondary-record flag, not the unit word itself.


### Interior citation — frontier hub `00273320` (2026-09-18, SWE2-EC7)

`00273320` — 86 B, 7 callers. Read from the shipping image: rejects `ecx == 0`
with `-1`, otherwise linear-searches the `0035BB00` accessor sequence — the count
comes from `0035BB60()` and each index's value is compared to `edi` at
[`0027334C`](../../_index/ADDRESS-INDEX.md) — returning the matching index or
`-1`. A find-by-value over a counted accessor table.

### Interior citation — frontier hub `00202D20` (2026-09-18, SWE2-EC7)

`00202D20` — 37 B, 14 callers: the vec3 dot product leaf — `a1*b1 + a0*b0 +
a2*b2` in `xmm0` ([`00202D3C`](../../_index/ADDRESS-INDEX.md)), no calls, no
stack. The maths leaf the unit-field consumers share.

### Interior citation — frontier hub `0046F460` (2026-09-18, SWE2-EC7)

`0046F460` — 75 B, 10 callers: the normalised-input table trig leaf. `xmm0` is
clamped to `[-1.0, 1.0]` (`comiss`/`maxss`), shifted `+1.0`, scaled `×0.5`
then `×0x3D08850A`, truncated `cvttss2si`, masked `& 0x3FFF`, and used to index
the `00D12590` float table at
[`0046F4A5`](../../_index/ADDRESS-INDEX.md) — the lookup the unit-field
consumers share. No calls.

### Interior citation — frontier hub `00391D10` (2026-09-18, SWE2-EC7)

`00391D10` — 121 B, 5 callers: cookie-guarded two-phase adapter — `r8d &
0x10` selects the flag, calls `00391A30` at
[`00391D49`](../../_index/ADDRESS-INDEX.md) returning a value via the stack
slot, then `003911D0(rsi, edi, &out)` completes the second phase.
### Interior citation — frontier hub 0026A330 (2026-09-18, SWE2-EC7)

**0026A330** (`Actor_SetMovementSpeed`, 37 B, 4 A-measured callers) — the setter the field map's movement-speed entry reaches. `Actor_IsLocked` (`002E9780`) vetoes; then `jae`-clamps a float parameter and tails `0026D6F0` — the same request channel `Actor_StopRequestedMovement` ends on. So `+0x44`-block writes come in two forms: bulk zero (stop) or a single scaled value (this), both through `0026D6F0`. In-scope: lock gate call [`0026A343`](../../_index/ADDRESS-INDEX.md); clamp + tail [`0026A359`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-18 update (2026-05-15) — `0031ABE0` compare-merge fragment

`0031ABE0` (16 B) is the global-flag gate the six `0033xxxx`/`00312730` battle-unit callers (`00312730`, `003357B0`, `00336710`, `003377C0`, `00338490`, `0033C310`) reach: `test byte[02089340], 0x10` (`0031ABE0`) — set, it forwards into `003588B0` (`0031ABE7`); clear, it returns `eax=0` (`0031ABED`) — the master-enable check this region's per-field paths consult before doing work.

## SWE2-EC7-19 update (2026-05-15) — `00469E80` overflow-mask builder + `0037B4B0` merge fragment

`00469E80` (60 B) is the gated `0046AB10` post this page names behind `00312551`–`00312566`: it zeroes a six-qword stack record (`[r11-0x38]`..`[r11-0x10]`, `00469E89`..`00469E9D`), parks `ecx` at `[rsp+0x30]`, and only when `ecx > 0` calls `0046AB10` with `edx=0x26`, `ecx=0`, `r8=&record` (`00469EA5`..`00469EB2`) — the kind-`0x26` message post the clamped-overflow path raises, suppressed when the count is non-positive.

`0037B4B0` (10 B) is the null-gated `+0x23` byte clear the `0031A300`/`00324380`/`003261D0`/`003273D0` battle-unit callers reach: `rcx` non-null writes `byte[rcx+0x23]=0` (`0037B4B5`) and returns — a single-field reset the callers share.

## SWE2-EC7-20 update (2026-09-18) — `0030A880` four-slot unit filter window

`0030A880` (31 B) is the `BattleUnit_BuildFilteredFourSlotUnitBuffer` seed the
four-slot enumerators share: it stores the `022C1788` static unit table into
`[rcx]`, then tails `0030A8A0` with `edx = 4` — the four-slot count the filter
body fills. Interior anchor `0030A88C` (the `[rcx]` table install). Nine callers —
`00234590`/`002348E0`/`00237EA0`/`00237F40`/`00321630`/`00321B00`/`003246C0`/`00326620`/
`00326D60` — the candidate-record enumeration behind the max-scan `00321630` this page names.

## SWE2-EC7-21 update (2026-09-18) — `00469320` normalize-or-zero vector helper

`00469320` (240 B) is the three-float normalize-or-zero helper this page's
shared-callee list names: it compares each component of `[rcx]`/`[rcx+4]`/
`[rcx+8]` against the `±[009002C8]`/`±[00D12538]` epsilon pair in double
precision (`cvtps2pd` + `comisd` at `0046933C`..`00469384`) — when all three
fall inside the band it writes `[rcx]=0`/`[rcx+4]=0` (`00469388`..`0046938C`,
a dead vector collapse); when any component escapes, it computes
`sqrtf(x²+y²+z²)` through `00861F14` (`004693CD`), divides 1.0f by the length,
scales all three components, and stores the unit vector back in place
(`004693DE`..`00469400`). Interior anchor `00469322` (the `sub rsp,0x50`
prologue).

## SWE2-EC7-23 update (2026-09-18) — `003B02A0` kind-dispatch marshal

`003B02A0` (958 B) is the kind-dispatch marshal the unit record paths share:
`r13d = [rsp+0xCE0]` kind arg gated to `{5,6,9}` (`test (r13d-5), ~5` +
`r13d != 0xA`), `rdi - 0x64` range check, the `0xCA0` frame staging the per-kind
record the callers submit. Interior anchor `003B02DB` (the kind mask test).

## SWE2-EC7-24 update (2026-09-18) — `00382EA0` + `003920F0` unit helpers

`00382EA0` (332 B) is a 2D point-in-segment classifier: `([rcx].y - [rdx].y) *
([r8].y - [rdx].y) + ([rcx].x - [rdx].x) * ([r8].x - [rdx].x)` — the dot-product
segment test — and on `comiss <= 0` publishes `qword[rdx]` into `[r9]` before
the `008C2C38` tail call; the mirrored second half tests the `rcx`-anchored
segment the same way. Interior anchor `00382EF6` (the first `mulss`).

`003920F0` (121 B) is a cookie-checked compose (`0x840` frame, `00808C40`
guard): `00391D90` seeds `rsp+0x30` with `r8d = r9d & 0x10`, then `003911D0`
runs the record through `rcx=rsi`/`edx=edi`. The `0033xxxx` unit-format
callers share it. Interior anchor `00392129` (the `00391D90` call).

## SWE2-EC7-25 update (2026-09-18) — `003911D0` flagged pointer visitor

`003911D0` (263 B) iterates `r9d` pointers at `[r8 + i*8]`, `00263E30`-
resolving each, with flag lanes off `r15d`: `&2` requires the resolve to
succeed, `&4` tests the node's `+0x698` object (`[+0x64] | [+0x3C]` masked
`0x80000003`) through `00313F60`, `&8` runs `002EA7F0` — the multi-gate
filter the `0033xxxx` unit-format callers share. Interior anchor `00391228`
(the `00263E30` call).

## SWE2-EC7-26 update (2026-09-18) — `0030BCB0` / `00313F80` / `00314EB0` / `0030A130` unit-record helpers

`0030BCB0` (24 B) calls `0030AB40()` and returns `setbe (eax <= 1)` —
the availability boolean the unit paths read. Interior anchor
`0030BCBB` (the compare).

`00313F80` (115 B) — reached through its `003357B0`/`003377C0`/
`00338490`/`0033C310` callers — `002646A0`-resolves both arguments,
runs `00314F50(rsi, rax, 0, &out)` when both resolve, and publishes
the result float to `*[r8]` when an out pointer is given; returns the
both-resolved bool. Interior anchor `00313FBD` (the `00314F50` call).

`00314EB0` (112 B) — same caller set — null-safely digs `+0xC0` ->
`+0x138` on both arguments and compares the two sub-records:
`byte[+6]` must match, and `byte[+0x119]` must be zero on the first or
equal on both — returns 1 on a difference. The record-difference test
paired with `00313F80`. Interior anchor `00314EF8` (the `+6` compare).

`0030A130` (40 B) — reached through `00312730`/`00325BB0` — passes
`[rcx+0x10]` to `00265090` with two stack outs and returns
`maxss(out1, out2)` — the larger-of-two metric read. Interior anchor
`0030A142` (the `00265090` call).

## SWE2-EC7-27 update (2026-09-18) — `002ED500` view-request null arm

`002ED500` (43 B) is the entry the `+0x2C` consumer chain names: `rcx`
null zeroes all eight qwords of the `[r8]` view out-record and returns,
non-null tail-jumps `0031B4B0` — the presentation-view request whose
empty branch yields a zeroed 64-byte view. Interior anchor `002ED50B`
(the zero fill).

## SWE2-EC7-30 update (2026-09-18) — `00269E20` `+0x140` float store

`00269E20` (26 B) is `Actor_SetPresentationYOffsetPrimary`: while the
actor's `+0xC0` secondary context exists it writes `xmm1` to
`ctx+0x140` and tails `00268380(actor)` — the float setter half of
the `00269E20`/`00269E40` pair (`00269E40` writes `+0x144`),
no-op when the context is absent. Interior anchor `00269E2C` (the
`+0x140` store).

## SWE2-EC7-34 update (2026-09-19) - `00391D90`

`00391D90` (851 B) is a battle-unit field fill - `02AEE0A0` null guard, `003912E0`/`003A1920`/`00468F90`/`003920CC`/`003920AA`/`00392038` plus `00861EC0`. Interior anchor `00391EBE` (an `003912E0` call).

## SWE2-EC7-35 update (2026-09-19) - `00391A30`

`00391A30` (721 B) is a battle-unit field body - `02AEE0A0`/`02AEE0B8`/`02AEE0B0`/`02AEE090` records, `00469060`/`00468D10`/`002FB500`/`002FB340`/`00861EC0`. Interior anchor `00391AAB` (an `00861EC0` call).

## SWE2-EC7-37 update (2026-09-19) - `003377C0`

`003377C0` (565 B) is a battle-unit field path - `01F44830`, `0031ABE0` flag-gate consult plus `00265090`/`00236820`/`002EA7F0`/`00391D10`/`003920F0`/`00263E30`. Interior anchor `00337832` (a `00265090` call).

## SWE2-EC7-37 update (2026-09-19) - `00321B00`

`00321B00` (551 B) is a battle-unit field writer - `00313F60`/`00322C50` pairs plus `0030A880`/`00321770`/`00321E40`. Interior anchor `00321B36` (a `00313F60` call).

## SWE2-EC7-37 update (2026-09-19) - `0033D660`

`0033D660` (548 B) is a battle-unit sibling - `01F44830`/`008C5FD0`/`01CEBB70`/`008F311C`, `00265090`/`00263940` pairs plus `002646C0`/`004686D0`/`00334C90`/`00318CA0`/`00808C40`. Interior anchor `0033D6C8` (a `002646C0` call).

## SWE2-EC7-45 update (2026-09-19) - `00468700`

`00468700` (239 B) is a body - `00202D20`/`00469320`/`0046F460`/`00808C40`. Interior anchor `0046873E` (a `00202D20` call).

## SWE2-EC7-48 update (2026-09-19) - `0030A8A0`

`0030A8A0` (204 B) is the four-slot battle-unit tail body - `0031B810`/`00377C20`. Interior anchor `0030A8D4` (a `0031B810` call).

## SWE2-EC7-51 update (2026-09-19) - `0030C210`

`0030C210` (173 B) is a `BattleUnit_GetBySlotIndex` hub caller - `00236820`/`0030AB40`/`00377C20`. Interior anchor `0030C237` (a `00236820` call).

## SWE2-EC7-53 update (2026-09-19) - `00334C90`

`00334C90` (362 B) is a battle-unit sibling - `00263940`/`002646C0`/`002F8E70` plus `008C5FD0`/`01CEBC08`/`01CEBD80`. Interior anchor `00334CBC` (a `002F8E70` call).

## SWE2-EC7-54 update (2026-09-19) - `003912E0`

`003912E0` (292 B) is a battle-unit field body - `00861EC0` single call plus `02AEE060`/`02AEE064`/`02AEE0A0`/`02AEE0A8`/`02AEE0B0` state. Interior anchor `0039130E` (a `00861EC0` call).

## SWE2-EC7-56 update (2026-09-19) - `00468F90`

`00468F90` (205 B) is a battle-unit field body - `00468580`/`004691A0`/`00861F14`. Interior anchor `00468FC5` (a `004691A0` call).

## SWE2-EC7-58 update (2026-09-19) - `002348E0`

`002348E0` (169 B) is a battle-unit body - `002FEDC0`/`00300140`/`00300E40`/`00307FF0`/`0030A880`/`00321170` plus `0208E6A0`. Interior anchor `002348F8` (a `00321170` call).

## SWE2-EC7-59 update (2026-09-19) - `0030DA30`

`0030DA30` (162 B) is the pipeline-open body the battle-unit map names - `00237670`/`00377C20` plus `02089340`. Interior anchor `0030DA63` (a `00377C20` call).

## SWE2-EC7-60 update (2026-09-19) - `00473830`

`00473830` (156 B) is a battle-unit body - `0023A120`/`00263BE0`/`00263FF0`/`00358940`. Interior anchor `00473840` (a `00263FF0` call).



## SWE2-EC7-65 update (2026-09-19) - `002FD0C0`

`002FD0C0` (136 B) is the `002FD0C0(count, byte[rdx+3])` body - `0024FE70`/`0036C140`/`0036C1D0` plus `02EC32E0`. Interior anchor `002FD10D` (a `0036C1D0` call).


## SWE2-EC7-68 update (2026-09-19) - `00263940` kind-dispatched float reader

`00263940` (55 B) is the record float the stat marshal `003223C0`
and the battle-unit bodies read: `(byte[rcx+3] >> 5)` selects the
arm - `1` returns `float[[rcx+0xB8]+0x68]`, `3` returns
`float[[rcx+0xB8]+0xC0] * float[[rcx+0xB8]+0x24]`, and every other
kind returns `0.0`. Call-free. Interior anchor `00263960` (the
`mulss` product).

## SWE2-EC7-74 update (2026-09-19) - `00306BB0` + `002FB340` unit helpers measured

`00306BB0` (20 B) is the `022C2160` range check: `(value - 5) <= 1`
unsigned - true when the mode byte is 5 or 6.
Interior anchor `00306BBB` (the `cmp eax, 1` bound).

`002FB340` (98 B) is the two-out fetch the unit bodies call:
`002646C0(rbx, rcx, rcx+4, rcx+8)` fills the record, then
`00265090(rbx, rsp+0x30, rsp+0x40)` supplies two floats whose
`maxss` lands at `[rsi+0x10]` with `[rsi+4]` zeroed - the
clamped-extent write.
Interior anchor `002FB375` (the `00265090` call).

## SWE2-EC7-82 update (2026-09-20) - `00512EE0` record reset measured

`00512EE0` (15 B) is the small reset the battle-unit callers share:
`byte[rcx+0xF]` keeps its high nibble, `word[+0xC]` goes `0xFFFF` and
`byte[+0xE]` goes 0 - a three-field init with no calls.
Interior anchor `00512EE4` (the `+0xC` store).

## SWE2-EC7-84 update (2026-09-20) - `004268D0` + `0041E690` measured

`004268D0` (117 B) is the recursive record-tree visitor the unit
callers run: `cx` != -1 enters, and while `+0x290` bit `0x100000` is
clear the supplied `rsi(rec, rdi)` runs per record; `word[+8]`
recurses and `word[+0xA]` iterates, all at the 0x740 stride.
Interior anchor `00426914` (the `call rsi` visitor invoke).

`0041E690` (455 B) is the kind-gated predicate the same callers run:
masked `word[+0x3B4]` (or `+0xCC` when it is 0) is tested against
`0x35`/`0x36` by `edx` in {0,3,4}, `004232D0` and the `00422D50`
record probe (`+0x31C & 0xF000 == 0x2000`, then a 0xA0-stride scan
or-ing `word[e]>>6` bits) qualify the path, the `+0xCC` fallback
accepts {9,0xA,0x31,0x32}, `003E7D10(+0x6A4, 3)` is the final gate,
and the failure arm resolves `word[+0]` at 0x740 into
`00427320(rec, 0x302F)` before returning 1 - 0 on dead ends.
Interior anchor `0041E6EA` (the `004232D0` call).

## SWE2-EC7-94 update (2026-09-20) - `00335760` + `00322280` measured

`00335760` (66 B) is the gated classification `003343D0`,
`003357B0` and `0033C310` use: `rcx` and its `+0x698` link must be
nonzero with `byte[+5]==1`, then `00263C20([rcx+0x10])` runs and
the result maps - 3 returns 0, otherwise `(code-1 > 1) + 1` gives
the 1-or-2 class.
Interior anchor `0033577F` (the `00263C20` call).

`00322280` (66 B) is the message-kind predicate `0031ADB0` and
`003250F0` run: `ecx-0x200A <= 0x3E` indexes a combined
jump/dispatch table (`+0x2022C4` dwords, `+0x2022CC` arm ids) whose
arm `003222AA` returns 1; anything outside the window is true only
when `(ecx & 0xF000) == 0x5000`.
Interior anchor `00322294` (the table byte fetch).

## SWE2-EC7-95 update (2026-09-20) - five unit-side helpers measured

`003216E0` (141 B) is the triple-write orchestrator `00307300`
and `0030EC00` call: `+0x698` must exist with `byte[+5] == 0`,
then it runs `00321850` (the clamped table write above) with
`[r9+4]`/`[r8+0x1D]`, `003219D0` with `[rsi+0x1F]`, and
`00321B00` with the negated `[rsi+0x20]` - the three-field apply
the callers compose.
Interior anchor `0032172E` (the `00321850` call).

`0031EA90` (119 B) is the `0xFFFF`-gated table indexer
`00301AD0`, `00309480`, `003231F0` and `003343D0` use: a
`0xFFFF` argument returns 0 early; otherwise two `0020E600`
resolves on the `02EBF0xx` globals build `word[+8]*(cx-0x1000)+eax`
and it tails `0031E9F0` - the same two-resolve shape
`003203B0` uses.
Interior anchor `0031EABC` (the first `0020E600` call).

`00319E30` (13 B) is the two-value gate `00300E40` and
`00301140` call: `ecx` must not be 0 or `0xFFFFFFFF` to tail
`003B0770`, else it returns inline.
Interior anchor `00319E36` (the conditional `ja`).

`00319140` (54 B) is the two-bit flag fan `00234200` and
`00310780` run: bit 0 of `edx` calls `00290B90([rcx+8])`, bit 1
calls `003BBC80([rbx+0x10])` - independent arms, either or both.
Interior anchor `00319157` (the `00290B90` call).

`00312170` (264 B) is the flag-word composer `00307300` and
`0030EC00` also call: two `0020E600` resolves index `edi =
r8w*word[+8]+eax`, `0030AB40` must return above 1, then `ebx`
accumulates - `bts` from `byte[+0x3A]` in 1..0xFE, `or` from
`byte[+0x13]`, the `cmove` pair at `0031221E`-`00312232` sets bit
8 iff the action row's `[+0xC]` bit 13 (`0x2000`) is set and bit
9 iff bit 14 (`0x4000`) is set, `00321190(0xA, ...)` ORs in more,
and `00329E60(0xA, rsi, ebx)` publishes the composed mask.
(Corrected 2026-09-27, UQ-107: the earlier "set unless" reading
was inverted.)
Interior anchor `0031219F` (the first `0020E600` call).

## SWE2-EC7-96 update (2026-09-20) - `0030DAE0` + `0030B8E0` + `002FB500` measured

`0030DAE0` (96 B) is the twelve-arm constant dispatch `00303A00`
and `00307300` call: `ecx <= 0xB` indexes a dword-offset jump table
whose arms return 0..0xA in permuted order (arm order 0,2,4,3,5,1,
6,7,8,9,0xA); anything above returns 0xB inline.
Interior anchor `0030DAF9` (the `jmp rcx` dispatch).

`0030B8E0` (109 B) is the pair-validity check `00300530` and
`0030E360` call: both arguments non-null and `0030AB40` above 1
arms `ebx`, then `0030B770` + `0030B7F0` run and the result is
`word[out+2] != 0 || (dword >> 16) != 0`.
Interior anchor `0030B90D` (the `0030B770` call).

`002FB500` (92 B) is the three-call record fill `00391A30` and
`00391D90` run: `002646C0` unpacks the source into `rcx`'s `+0`/
`+4`/`+8`, `00265090` reads `+0x10`/`+0x14`, `00265200` produces
`xmm0` for `+0x18`, and `+4` is re-cleared - the staged-record
shape the builders emit.
Interior anchor `002FB53B` (the `00265200` call).

## SWE2-EC7-98 update (2026-09-20) - `002E5FD0` measured

`002E5FD0` (38 B) is the type-0x60 vector write `00238BF0`,
`002FE950`, `0050E6F0` and `0050E7B0` call: `byte[rcx+3] &
0xE0 == 0x60` admits, `xmm1/2/3` land at `[rcx+0xB8] +0x20/
+0x24/+0x28`, and the tail `jmp 002E8E20` falls into the
four-parameter apply - the staged position write the battle
record's callers drive.
Interior anchor `002E5FF0` (the `002E8E20` tail jmp).

## SWE2-EC7-103 update (2026-09-20) - `002718E0` measured

`002718E0` (121 B) is the angle-accumulate publish
`00289D70`, `00289F50`, `0028A350` and `0028A620`
call: `ecx == 0` returns 0; `003588B0()` null also
returns; otherwise `00265470` resolves the record
against `rsi`/`rsi + 4`/`rsi + 8`, `00263940`
answers a float which is divided by
`[008F311C]` (`3.1415..`) and accumulated into
`float[rsi + 4]` - returning 1, the
radian-scaled add the unit arms post.
Interior anchor `00271925` (the `00265470`
call).

## SWE2-EC7-104 update (2026-09-20) - `00265390` measured

`00265390` (182 B) is the position-plus-offset
read `002C6F70` and `00312730` call - the
same `byte[+3] >> 5` class dispatch as
`00265470`, but the class-2 arm adds
`[[rcx + 0xC0] + 0x140] + [+0x144]` to the y
out-slot when the `[+0xC0]` record is live,
and when `byte[[+0xB8] + 0x107]` bit 0 is set
it additionally adds the record's
`+0x40 / +0x44 / +0x48` float offsets into
all three out-slots. Class 1 copies
`+0x10 / +0x14 / +0x18` unchanged; other
classes zero the triple. This is the read that
carries the per-instance height adjust into
the callers' position queries.
Interior anchor `002653B7` (the class-2
record load).

## SWE2-EC7-107 update (2026-09-20) - `00236210` + `002360D0` measured

`00236210` (239 B) is the gated
heal roll `00238BF0` and `00239E10`
call: `[rcx + 0x698]` must be live
with `byte[+5] == 1`, then
`byte[[+0xE68] + 0x18]` steers -
bit 4 forces 8, bit 5 picks 1-or-2,
bit 6 keeps it raw, `| 4` applied
unless bit 6 - and `ecx & 0xA` runs
`003204D0(rcx, 6, &out)`; when the
`[+0x698]` record re-validates and
`byte[[+0xE60] + 3] & 0x10` arms the
answer is `out` alone, else
`out + (00328370() % 50) / 100.0`
(the `008F3134` constant) - the bounded
random top-up the unit arms share.
Interior anchor `0023626B` (the
`| 4` fold).

`002360D0` (39 B) is the counted
byte fetch `00306E60` and
`00306F00` call: `edx` must sit in
`[0, byte[rcx] - 1]`, then answers
`byte[rcx + 1 + edx]` unless that
byte is `0xFF` - either failure
answers `-1` - the sentinel-aware
table read the unit builders share.
Interior anchor `002360E5` (the
`+1 + edx` fetch).

## SWE2-EC7-108 update (2026-09-20) - `002315E0` measured

`002315E0` (176 B) is the
`0022F430` descriptor post
`00318CA0` and `0032A4D0` call:
null `rcx` or `[rcx]` answers
`0xFFFF`; otherwise it stages
`0022D4B0` as the callback, copies
the caller's two 16-byte blocks
(`rdx` and `r8`) into the frame,
seeds `word = 0xFFFF` and
`dword = 0`, runs `0022F430(&desc)`
and returns the signed
`word[+0x44]` out field - the
sibling post to `00232490`'s
`0022F830` shape.
Interior anchor `00231652` (the
`0022F430` call).

`00469410` (346 B) is the vec3 delta `00468A70`/`00468F70` call: pure SSE - `xmm10 = [rcx + 4] - [r9 + 4]` times `[rcx + 4] - [rdx + 4]`, `xmm9 = [rcx] - [r9]` against `[rcx] - [rdx]`, `[rcx + 8]`/`[rdx + 8]`/`[r9 + 0x10]` round the triple - the unit's per-axis interpolation.

Interior anchor `00469421` (function `00469410`).

`0031AA30` (325 B) is the gated attribute compute `00328530` calls: `00322C50` validates the selector, then `02EBF138`'s record resolves `[rax+0xC]` through `0020E600` and computes `esi * word[rcx+8] + result`; `rdi+0x698`/`+0xE60` flag gates (`byte[+5]==1`, `byte[+0x15]&8`) choose between the computed value and zero before writing the `r9` out-pair (`-1`/`0` defaults) - the unit's conditional stat accessor.

Interior anchor `0031AA83` (function `0031AA30`).

`003B0980` (324 B) is the first-zero-field locator `003B02A0` calls: walks `02EBEC18` records at 0x90 stride to `02EBEF78`, probing six dword slots each (`-0x18`, `0`, `+0x18`, `+0x30`, `+0x48`, `+0x60`); `ecx` accumulates the ordinal of the first zero field across the whole table (record x 6 + field), `cmp ecx, 0x24` bounds it to the 36-field span, then clears bit0 of `byte[02EBEC00 + ecx*0x18 + 0x13]` and `0024EE60` re-drives the record - the unit-slot free-field claim.

Interior anchor `003B09B1` (function `003B0980`).

`00334950` (287 B) is the predecessor-chain scorer `0033C200`/`0033C310` run on the unit's `[+0x108]` context: `+0x60/+0x68` load into the stack vec and `00384130` normalises it; then up to `0x80` hops follow `byte[rbx + rdi + 0x190]` links (the walk exits on `ecx == ebp`, `== dword[rdi+0x188]`, or `== 0xFF`), each hop's waypoint pair at `[rdi + rbx*8 + 0x210]`/`+0x214` dot-products the running direction through `004686D0` accumulating into `xmm6`; a final `004686D0` against the base vec adds the tail term - the path-alignment score the solver consumes.

Interior anchor `00334A11` (function `00334950`).

`00334950` (287 B) is the predecessor-chain scorer `0033C200`/`0033C310` run on the unit's `[+0x108]` context: `+0x60/+0x68` load into the stack vec and `00384130` normalises it; then up to `0x80` hops follow `byte[rbx + rdi + 0x190]` links (the walk exits on `ecx == ebp`, `== dword[rdi+0x188]`, or `== 0xFF`), each hop's waypoint pair at `[rdi + rbx*8 + 0x210]`/`+0x214` dot-products the running direction through `004686D0` accumulating into `xmm6`; a final `004686D0` against the base vec adds the tail term - the path-alignment score the solver consumes.

Interior anchor `00334A11` (function `00334950`).

`0030EAE0` (38 B) is the mode-3 shim: repacks the two caller stack args into the callee frame and calls `0030E360` with a literal mode 3 - the fixed-mode lane the battle-unit, spawn-keep and post-result callers share.

Interior anchor `0030EAFC` (function `0030EAE0`).

`0033D200` (475 B) is the scalar channel driver `0033A720` ticks per battle-unit field: `00236820` selects the `[rbx+0x108]`-record's `+0x177` lane, `[rbx+0xB0] > 0` picks `+0xE4` or `+0xE8` as the step `xmm7` by the `+0x104` compare, and when `[rdi]` carries no `0x7FE0` bits and `00334220` passes, `00334120` integrates `xmm6` toward `[rax+0xE0]` into `[rbx+0xBC]`/`+0xB4` and returns state 5; the decay arm instead magnitudes `[rbx+0xBC] - xmm6` through `0033CB70`, scales `xmm7` by the `(|delta|*80/bound + 20)/100` curve (`008F6D58`/`00901988`/`008F3134` constants) while `|delta|` stays under the `00915614` bound, `004686D0`-transforms the `+0x10` block, clamps against `[rax+0xF8]*12.0`, and finally clears the `0x7FE0` lanes while setting `0x140` in `[rdi]` - returning 2.

Interior anchor `0033D30F` (function `0033D200`).

`0035BB00` (22 B) is the indexed field read `00273320`, `002734F0` and `0029AEF0` share over the `022C8080` slot table: it sign-extends `ecx`, scales the index by `0xC0` (`rax + rax*2 << 6`), and returns the dword at `022C8084 + idx*0xC0` - the `+4` field of the `0xC0`-stride record the `00254B50` claim probe walks

Interior anchor `0035BB0B` (function `0035BB00`).

`0033BED0` (213 B) is the flag-dispatch `00336CE0` runs on the unit's `+0x100` object: `00336040` failing stores `+0xB0 = 0` after `00469A50(+0xF0, +0xF8)`; passing clears `+0xCC` bit `0x80`, runs `00339BF0` into `+0xB0`, then `0033C870`/`0033C200` gates and `[+0x100] & 0x7FE0` select `00338140` (when `+0x108`->`+0x40 == 1`), `0033A570`, or `00339F00`, all tailing `0033BFB0`

Interior anchor `0033BEFB` (function `0033BED0`).

`00339F00` (531 B) is the facing solver `0033BED0` runs as its last dispatch arm: quaternion/matrix helpers `00203170`/`00202E90`/`00202B70`/`00202FE0`/`00202B10`/`00203080`/`004687F0`/`00468700` build a turn target from `[+0x108]+0x110 + +0xA4 + pi/2`, write `movdqa` to `+0x10` and the solved angle to `+0xB8`, then `[rdi] & 0x1F` dispatches kinds 1-6 to `0033CEF0`/`0033D200`/`0033CE60`/`0033BAA0`/`0033CDE0` before `004686D0` compares `+0xB0` and clears `[rdi] & 0xFFFF801F`

Interior anchor `00339F3E` (function `00339F00`).

`00336040` (461 B) is the target-acquisition gate `0033BED0` calls first: `[+0x108]+0x174 == 1`, `[+0xF0]+0x714 < 0x21F`, `[+0xF0]+0x698` flags `+0x64|+0x3C` bit `0x20` clear, `[+0xF0] != [+0xF8]`; then `003272A0` resolves the target and a `+0x190`-byte chain walk (bounded 0x80) runs `004686D0` heading + `00309A90` angular-norm comparisons against the unit `+0x40` frame - returns the acquire verdict

Interior anchor `003360B4` (function `00336040`).

`0033C870` (319 B) is the turn-state transition `0033BED0` calls after `00336040` passes: with `+0xCC` bit `0x400` set it runs `00334E00` on `+0x50`, resolves `+0xBC` via `00203080`/`004687F0` when `[+0x108]+0x40 == 1`, clears bit 10 / sets bit 7 of `+0xCC`, `0033E1F0`s and clears `[+0x100]+0x3C` bit 3; without it, `[+0x108]+0x176` bit 2 / `+0x170` bits and a `+0x110 + +0xA4 + 5.0f` heading margin decide whether `00334E00` fires, `+0xCC |= 0x400` and `+0xB0 = 0`

Interior anchor `0033C8A8` (function `0033C870`).

`0033C200` (267 B) is the ID-gated lane `0033BED0` consults: `[+0xF0]` must pass `002F8E70` (`& 7` nonzero) and its `+0x714` word must be `0x4124` or `0x4022`; then `0033BD70` or `0033C310` gate further, `00265830` on `+0xE8` must not return nonzero, and `00334950`'s result clamps `[+0x100]+0x10` between `+0x10 - 0.0188f` and `+0x10 + 1.54f` with `+0x14` cleared on the low arm

Interior anchor `0033C229` (function `0033C200`).

`00334E00` (882 B) is the sampled heading search `0033C870` runs: it seeds `xmm14` from `+0xA4 + +0xA0 + pi/2` (or `+0xAC - pi/2` when `[+0x108]+0x40 != 1`, after `003377C0`/`004686D0` fast exits that write `+0x20`/`[rdi]` direct), then loops 2x4 samples - `[008C3098]` tick mod 360 scaled to radians, angle-normalised against the 2pi/4pi constants, `00203170`/`00202F00`/`00202B70`/`00202FE0`/`00202B10` rotate a direction, `0033D3E0` under `[+0x108]+0x174` mode tests clearance - first clear direction returns `eax=1` with the vec4 at `[rbp]`, else `[rdi]`/0

Interior anchor `00335087` (function `00334E00`).

`0033BD70` (351 B) is the landing probe `0033C200` runs: gated by `[+0xF0]` live + `002F8E70` low-3 flags + `[+0x100]+0x14 >= 0x3C` + `[+0xF0]+0x714` in {`0x4124`,`0x4022`} + `004686D0` heading >= 20.0 + `00322360` idle, it steps `xmm6` outward by 1.0 up to 20 - `003347C0` builds the candidate point, `003377C0` must clear it, and the first candidate whose `+0x30`/`+0x38` differs from the unit's current pair wins: `[rsi+0x14] = 0`, `+0xCC |= 0x80`, the point stored to `+0x50`, returns 1

Interior anchor `0033BE30` (function `0033BD70`).

`003347C0` (397 B) is the candidate-point builder `0033BD70`'s landing probe steps: it walks the `[rdx+0x108]` record's `+0x184`/`+0x188` cursors over the `+0x190` byte lane (bound 0x80, `0xFF` ends it), builds the output vec4 at `[rcx]` from the `+0x210`/`+0x214` pair at the selected index (or copies `[rbp]` when ebx is 0), then `004686D0`-measures it against arg `xmm6` and returns the comparison

Interior anchor `00334818` (function `003347C0`).

`00337700` (184 B) is the placement predicate `003377C0` consults per candidate position: a null `rcx` or dead `[rcx+0x10]` refuses; `00265090` resolves the bound record's float pair, `00391410` on the out-vector must return `0`, and `00384130` on the staged `(x, z)` pair must not return `0xFF`; `00336390` then decides with `r8b = [rdi+0x1F4]` and `xmm1 = max(f0, f1)` - the world-space acceptance test the placement loop ANDs in

Interior anchor `00337784` (function `00337700`).

`00321630` (175 B) is the max-reduction `00301AD0` (`AiOrder_EvaluateTargetSelector`) folds over the filtered unit list: `0030A880` fills the four-slot buffer, each unit's `[rcx+0x698]` record supplies the `+4` byte for the `00322C50` kind-2 resolve, and the table byte `[rsi + rbp + 1]` (`rbp = [rcx+0x6A0] + 0x19`) replaces `ebx` whenever larger - `-1` folds in on a failed resolve; returns the maximum

Interior anchor `0032166A` (function `00321630`).

`004230A0` (120 B) is the event-code accept gate `00427320` (the render record's event receiver) and `002EF100` both run: `003E56C0` resolves the record, then `edx` codes carrying `0xF000` bits with low-12 in `0xA`..`0x47` ride the `00423118`/`00423128` offset+index table pair - two arms refuse (return 0) when `+0xB4` byte is set or `+0xAC != 2`, every other code returns 1

Interior anchor `004230D5` (function `004230A0`).

`004272A0` (18 B) is the `+0x294` arm `002EF100` and `002EB0D0` run on the `022C6F28 + i*0x740` battle row: sets bit `0x1000` in the row's flag dword and stores `dx` at `+0x3B6`

Interior anchor `004272AA` (function `004272A0`).

`00427860` (22 B) is the sibling flag commit on the same row's `+0x294`: masks off `0x00020520` (clearing bits 5, 8, 10 and 17) then force-sets bit 7

Interior anchor `0042786B` (function `00427860`).

`003B4930` (169 B) is the `+0x2CA` emit `00420890` runs on the `022C6F28 + cx*0x740` row: a `-1` index, an absent (`+0x284 == 0`) row or a `-1` selector all bail; otherwise it packs a 0x40 scratch record - byte pair `0`/`2`, kind word `0x201`, the selector sign-extended at `+4`, dims `0x280028`, `0x80FF`, `0.1f` at `+0x10`, the `1.0f` pair at `+0x20` - into `003B4160`

Interior anchor `003B49CF` (function `003B4930`).

`00469A50` (160 B) is the staged lookup `0033BED0` runs: `00320A30` resolves both `rcx` and `rdx` into the `[rsp+0x20]`/`+0x28` frame slots with `word[rbx+0x714]` at `+0x48`, `003272A0` supplies the comparison record, and `0046AB10` runs with `edx` = `0xA` or `8` chosen by whether `rbx` equals that record

Interior anchor `00469AE0` (function `00469A50`).

`0026BBC0` (146 B) is the two-mode float-pair apply `002E8E20`'s tail region and `0023B260`/`0026BB50`/`0026BD50` share: `byte[rcx+3] >> 5` selects the lane - 1 writes the constant 1.0f pair into `[rcx+0xB8]+0x40` through `003DA860`, 3 runs `003DA860` on `[+0xB8]+0x70`/`+0x90` with the live `+0x20`/`+0x28` floats and clears `byte[+0xDE]`; other modes no-op - the same record the field map's `+0xB8` arm documents.

Interior anchor `0026BC0B` (function `0026BBC0`).

`0026BF60` (144 B) is the two-mode `+0xB8` arm `002E8E20` calls beside `0026BBC0`: `byte[rcx+3] >> 5` selects - mode 2 copies the caller's `xmm1`/`xmm2` floats, stack-loads `[rbx+0x28]`/`[rbx+0x20]`, runs `003DA860` on the `+0x60` row with the `+0x88` arg and clears `byte[rbx+0xDF]`; mode 1 runs `003DA860` on the `+0x30` row with `1.0f` stack constants and sets `byte[rbx+0x5d] |= 2` - the per-mode float-pair application the field map's arm family shares.

Interior anchor `0026BFA8` (function `0026BF60`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-battle-unit-field-map-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0022D4B0` | 815 B | returns at once unless the signed word `[rdx + 0x40]` is positive; otherwise walks that many word ids from index word `[rdx + 0x3E]` of the array at qword `[rcx + 0x28]`, skipping ids at or above `0x5000` (signed): ids from `0x4000` take the `0x90`-byte record `id - 0x4000` under qword `[rcx + 0x18]` (flags dword `+4`), lower ids the `0x20`-byte record under qword `[rcx + 0x10]` (flags dword `+0xC`), the flags merged under the mask and value dwords at `0209A2D0 + 0x110 + 8 * (0x20 + flag bits 13-17)`; a record passes when the merged low three bits are 0, are 1 with bit 31 clear and (bit 30 clear or word `[rdx + 0x46]` not 4), or are 4 with that word equal to 4; a 263-byte (high ids) or 249-byte (low ids, which also need a nonzero 381-byte check) routine gives a float d, and when 0 <= d < float `[rdx + 0x30]` it either sets word `+0x44` to 1 if zero (merged bit 23 set) or stores d to `+0x30`, 16 stack bytes to qword `[rdx + 0x20]`, the id to word `+0x42` and 2 to `+0x44` | `0022D536`, `0022D581`, `0022D5D2`, `0022D5F8`, `0022D767` |
| `00234A10` | 99 B | for each slot index below dword `0208E6A0` (signed) gets the unit through `BattleUnit_GetBySlotIndexIfUnitFlag4Set` and, when it is non-null, its qword `+0x698` is non-null with byte `+5` equal to 1, and bit `byte [unit + 0xE98]` of `ecx` is set, ORs `0x800` into the unit's dword `+0` and passes the unit to a 35-byte refresher | `00234A1E`, `00234A28`, `00234A4B`, `00234A50`, `00234A59` |
| `00234A80` | 99 B | for each slot index below dword `0208E6A0` (signed) gets the unit through `BattleUnit_GetBySlotIndexIfUnitFlag4Set` and, when it is non-null, its qword `+0x698` is non-null with byte `+5` equal to 1, and bit `byte [unit + 0xE98]` of `ecx` is set, clears bit 11 (`AND 0xFFFFF7FF`) of the unit's dword `+0` and passes the unit to a 35-byte refresher | `00234A8E`, `00234A98`, `00234ABB`, `00234AC0`, `00234AC9` |
| `0023B260` | 49 B | calls a 146-byte routine on `rcx` with 1.5 (`00901B3C`) in both `xmm1` and `xmm2`, then tail-jumps to a 144-byte routine on `rcx` with 4.0 (`01CEBC70`) in both | `0023B266`, `0023B274`, `0023B279`, `0023B28C` |
| `002646A0` | 32 B | returns qword `[[rcx + 0xC0] + 0x138]`, or 0 when `rcx` or `[rcx + 0xC0]` is null | `002646A3`, `002646A5`, `002646B1`, `002646BD` |
| `002659A0` | 40 B | clears bits 8 and 13 of dword `[rcx + 0x1C]` (`AND 0xFFFFDEFF`, applied a second time when the top three bits of byte `[rcx + 3]` are 3), sets byte `+0xE` to `(byte AND 0xF5) OR 5` and stores 0 to byte `+0xF4` | `002659A4`, `002659AD`, `002659B8`, `002659BC`, `002659C0` |
| `00267CC0` | 125 B | clears bit 3 of dword `[rcx + 0x1C]`, ORs in `0x100` and then `0x2000`, calling `00268EA0(rcx)` after each OR while bit 3 of byte `+0xB` is set; when the top three bits of byte `+3` are 3 it repeats the two ORs with their calls; it then sets byte `+0xE` to `(byte AND 0xF4) OR 4` and stores 2 to byte `+0xF4` | `00267CC6`, `00267CCD`, `00267CDA`, `00267CFA`, `00267D30` |
| `0026BB50` | 8 B | copies `xmm1` into `xmm2` and tail-jumps to a 146-byte routine with `rcx` and `xmm1` unchanged | `0026BB53` |
| `0026BD50` | 113 B | takes the absolute values of `xmm1` and `xmm2` (through double with the sign mask at `01CEBD80`) and switches on the top three bits of byte `[rcx + 3]`: for 1 it ORs 4 into byte `+0x5D` of `[rcx + 0xB8]` and stores the two values to its floats `+0x40` and `+0x44`, each replaced by float `+0x30` or `+0x34` when larger; for 3 it tail-jumps to a 146-byte routine with the two values in `xmm1` and `xmm2`; any other value returns | `0026BD5E`, `0026BD88`, `0026BD94`, `0026BDB1`, `0026BDBB` |
| `0028A350` | 499 B | walks the node list from qword `[rcx + 0x428]` along qword `+0x18`: with k = dword `01DFE0B4`, each node adds `16 / k` (unsigned) to word `+0x10` and, once it is at least `0x100` (signed), pins it at `0x100`, increments word `+0x12` and caps that at `60k`; when dword `+0xC` is nonzero and `002718E0(+0xC, buffer)` returns 0 it zeroes `+0xC` and raises word `+0x12` to `60k - (60k >> 2)` when below it, otherwise a 79-byte lerp with 0.5 (`01CEBB70`) moves floats `+0`, `+4`, `+8` halfway toward the buffer; a node stays when `+0xC` is nonzero, `ActorHandle_ResolveRegistryEntryByPackedId(+0xC)` is non-null and word `+0x10` is below `0x100` or word `+0x12` below `60k`, else it is unlinked (advancing the head when it is the head), bit 0 of word `+0x16` is cleared and its links `+0x18`/`+0x20` are zeroed | `0028A3BB`, `0028A3FE`, `0028A477`, `0028A4A3`, `0028A4CB` |
| `0028A620` | 361 B | walks the node list from qword `[rcx + 0x430]` along qword `+0x18`: when a node's dword `+0xC` is nonzero it zeroes it if `002718E0(+0xC, buffer)` returns 0, else a 79-byte lerp with 0.5 (`01CEBB70`) moves floats `+0`, `+4`, `+8` halfway toward the buffer; it then adds `6 / dword 01DFE0B4` (unsigned) to word `+0x10` and, once that is at least `0x100` (signed), zeroes word `+0x12`, unlinks the node (advancing the head `[rcx + 0x430]` when it is the head) and zeroes its links `+0x18` and `+0x20` | `0028A680`, `0028A6D0`, `0028A6FC`, `0028A71A`, `0028A743` |
| `002E86B0` | 69 B | when `rcx` and its qword `+0xC0` (the sub) are non-null, the sub's dword `+0` and word `+0` are not -1, and the `0x740`-byte record at that index under qword `022C6F28` is non-null with a nonzero dword `+0x284`, stores `xmm1` to the record's float `+0x420`; otherwise it returns without a store | `002E86C1`, `002E86D3`, `002E86E3`, `002E86EC` |
| `002E9780` | 36 B | returns bit 6 of byte `+0x11` of qword `[rcx + 0xC0]` when the top three bits of byte `[rcx + 3]` are 3 and that pointer is non-null; otherwise returns 0 | `002E9786`, `002E9794`, `002E9796`, `002E979A`, `002E97A1` |
| `00346C00` | 269 B | ORs `0x40` into byte `[r8 + 3]` and reads a 22-byte per-slot byte getter on byte `[rdx + 0x15]`; on both paths it then pops three integers a, b, c through `VMValueStack_PopInt32CoerceFloat32(r9)`, replacing a negative c by a 7-byte dword getter; when the byte was nonzero it pushes -1, b and a through `VMValueStack_PushInt32`, calls a 180-byte routine with `(rcx, rdx, r8, r9)`, clears bit 7 of byte `[r8 + 3]` and passes `(c, 0, 0)` to a 29-byte three-dword setter; otherwise it stores b to dword `[r8 + 8]` and c to word `[r8]`, sets bit 4 of byte `+2` (its high nibble cleared first) when a is nonzero and keeps only bits 6-7 of byte `+3` before setting bit 7; both paths tail-jump an 8-byte routine that clears bit 7 of a global byte | `00346C12`, `00346C27`, `00346C96`, `00346CE2`, `00346D08` |
| `003589A0` | 8 B | returns the top three bits of byte `[rcx + 3]` (the byte shifted right by 5) | `003589A4` |
| `00468D10` | 53 B | returns 1 when the square of float `[rcx + 0x10]` plus float `[rdx + 0x10]` is greater than the squared distance over the floats `+0` and `+8` of `rcx` and `rdx`, else 0 (also 0 for an unordered compare) | `00468D1B`, `00468D29`, `00468D3A`, `00468D3E`, `00468D41` |
| `00468F70` | 17 B | loads float `[rcx + 0x20]` into `xmm2`, moves `rdx` into `r9`, sets `rdx = rcx + 0x10` and tail-jumps to a 346-byte routine | `00468F75`, `00468F78`, `00468F7C` |
| `00469060` | 79 B | gets a float from a 325-byte routine called with `(rcx, rdx)`, adds float `[rdx + 0x10]`, and returns 1 when the square of that sum is at least the squared distance over the floats `+0` and `+8` of `rdx` and `rcx`, else 0 | `00469070`, `00469085`, `0046909F`, `004690A3`, `004690A6` |
