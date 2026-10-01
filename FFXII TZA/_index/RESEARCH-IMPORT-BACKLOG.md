# Research import backlog — native knowledge this project has but the database does not

**Measured 2026-09-08** by `Tools/analysis-kit/gfz-scripts/research_import_gap.py`. Regenerate it;
do not quote from memory.

Charter §10 and §38 require locating existing local research and importing what is valuable **with
provenance**, rather than re-deriving it. This is the result of that search.

## What was measured, and what the honest denominator is

A first pass over **every** local tree found 6,796 function entries cited outside the database. **That
number is misleading and is not the headline**: most of it is generated output — `decompile/`
(3,852), `Collaboration/tools/analysis/out/rtti_classes.json`, and address constants inside tool
source. A decompiler dump citing an address is not research knowledge.

Restricting to **hand-written research prose** — the 115 markdown documents at the top level of
`Collaboration/` — gives the real figure:

| | count | denominator |
|---|---:|---:|
| function entries cited by that prose | 291 | — |
| **not cited anywhere in the database** | ~~145 (49.8 %)~~ **51** | 291 (**17.5 %**) |
| of the gap, carrying a `PrimaryOwner` | ~~109~~ **36** | 51 |
| of the gap, carrying a real semantic name | ~~66~~ **9** | 51 |
| **named *and* owned — someone identified it and the database lacks it** | ~~64~~ **8** | 51 |

~~**Half of the addresses this project's own research prose discusses have never entered the
database.** The 64 named-and-owned entries below are the actionable set.~~

**Re-measured 2026-09-13 (OPUS): the gap has closed by two thirds.** 145 → **51** uncited, and the
actionable named-and-owned set 64 → **8**. **Ninety-four of the 145 have entered the database since
2026-09-08**, which is what five days of import looks like from the other side. The list below is
the 2026-09-08 set and is left as written; the eight that remain are named here so the difference
is visible rather than implied:

| addr | bytes | name | owner | research document |
|---|---:|---|---|---|
| `00328B20` | 163 | `PartyConfiguration_RemoveSelector00To06` | Party | `XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md` |
| `003288F0` | 159 | `PartyConfiguration_RemoveSelector07To25` | Party | `XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md` |
| `002ED2A0` | 93 | `CharacterRender_DispatchCombatRelationEvent` | Presentation | `CLAUDE_PROGRESS.md` +2 |
| `0028FB80` | 88 | `Reward_PublishExpLpPresentation` | Presentation | `MOB_LIFECYCLE_RESEARCH_HISTORY.md` |
| `002697A0` | 50 | `Actor_RequestResourceReentry` | ActorEntity | `CLAUDE_PROGRESS.md` +1 |
| `002EBB80` | 41 | `Actor_SetPresentationVisibilityEnabled` | ActorEntity | `CLAUDE_PROGRESS.md` +2 |
| `00237080` | 29 | `SpawnEntry_ClearSelectionTransientStateFor…` | Spawn_Encounter_Lifecycle | `MOB_LIFECYCLE_RESEARCH_HISTORY.md` +1 |
| `00356150` | 8 | `Actor_RequestResourceReentry_Thunk` | ActorEntity | `X55_NATIVE_REPLAY_CONTRACT.md` |

> **Eight functions, 631 bytes, four owners.** That is the whole of what this project's own research
> prose names and owns and the database still does not cite. **Regenerate with
> `research_import_gap.py` before quoting any figure on this page** — the ones above it were five
> days old and wrong by a factor of three.

## The gap is concentrated in the player-facing systems

| owner | count |
|---|---:|
| `Spawn_Encounter_Lifecycle` | 17 |
| `Script_VM_Native_Bridge` | 11 |
| `Movement` | 10 |
| `ActorEntity` | 8 |
| `CombatAction` | 5 |
| `Party`, `Presentation` | 3 each |
| `WorldAreaField`, `CombatAI`, `CombatFormula` | 2 each |
| `Items_Equipment_Shops_License` | 1 |

**These are not obscure corners.** `SpawnGroup_RecordMemberDeathAndHandleCompletion`,
`BattleUnit_TryCommitEngageAutoAttack`, `PartyConfiguration_SetSelectorsAndReconcileRoster`,
`Actor_SetFacingHeading_Variant0/1` — the systems a modder asks about first.

## ⚠ How these must be imported

**The research prose is a prior session's claim, not a source.** The same rule that governs the GFZ
applies here without exception: *binary > fresh derivation > prose annotation*. A name in
`CLAUDE_PROGRESS.md` is tier 9 at best until it is joined to a body that has been read.

**Do not bulk-import.** Each entry earns its place by being read from the binary, exactly as if it
had never been named. The name is a **lead**, and its value is that it says where to look.

**Keep original behaviour separate from extension behaviour** (charter §23/§24). These documents were
written for the multiplayer project; their *native findings about the original game* belong in the
database, their *multiplayer design decisions* do not.

## Status

- **Imported so far: 24 of 64** (one of the three combat entries, `BattleAction_CheckTargetEligibility`, is **partial** - only its two opening gates were read).
  - the Movement facing/steering trio →
    [`../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md`](../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md)
  - six of the Spawn respawn/completion cluster →
    [`../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`](../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md)
  - the whole `Script_VM_Native_Bridge` cluster (7 verbs + 4 thunks, disposition **C**) →
    [`../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md`](../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md)
  - `ActorStorage_InitializeRecord`, the largest entry in the whole backlog →
    [`../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md`](../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md)
  - three `CombatAction`/`CombatFormula` entries appended to
    [`../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`](../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md),
    **extending an existing document rather than competing with it**

> **⚠ Two imports, two corrections — the "lead, not a source" rule is earning its keep.**
> `SpawnEntry_GetElapsedTicksSinceLastDeath` (`00235FB0`) **does not return ticks**: it divides the
> frame counter by the frame rate first, so it returns **seconds**, and the field it subtracts is a
> second-stamp. Carried across unchecked, that name would have put a factor of 30 or 60 into any
> reimplementation of respawn timing — and the error would have been invisible at 30 fps.
- Tracked as **`ED-1`** in [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md).

## The 64

| address | bytes | name | owner | researched in |
|---|---:|---|---|---|
| `00266530` | 1439 | `ActorStorage_InitializeRecord` | ActorEntity | PROGRAM_B_NATIVE_REFERENCE.md |
| `00236300` | 321 | `BattleUnit_SnapshotWorldActorRuntimeState` | ActorEntity | CLAUDE_PROGRESS.md +3 |
| `00265A20` | 320 | `ActorSystem_BindBattleUnitsForEligibleRecords` | ActorEntity | CLAUDE_PROGRESS.md +3 |
| `002396B0` | 82 | `BattleUnit_SetRuntimeUnitCategoryMode` | ActorEntity | MOB_LIFECYCLE_RESEARCH_HISTORY.md +2 |
| `002697A0` | 50 | `Actor_RequestResourceReentry` | ActorEntity | CLAUDE_PROGRESS.md +1 |
| `002671C0` | 46 | `ActorSystem_IsPrimaryBattleSimulationReady` | ActorEntity | MOB_LIFECYCLE_RESEARCH_HISTORY.md +5 |
| `002EBB80` | 41 | `Actor_SetPresentationVisibilityEnabled` | ActorEntity | CLAUDE_PROGRESS.md +2 |
| `00356150` | 8 | `Actor_RequestResourceReentry_Thunk` | ActorEntity | X55_NATIVE_REPLAY_CONTRACT.md |
| `00308C20` | 357 | `AiOrder_ComputeBoundedSelectorScalar` | CombatAI | CLAUDE_PROGRESS.md |
| `00324F20` | 315 | `BattlePerception_RefreshCandidateCacheGeneration` | CombatAI | CLAUDE_PROGRESS.md |
| `00325260` | 1215 | `BattleUnit_HandleActionTimelineEvent` | CombatAction | XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md |
| `003083B0` | 596 | `BattleAction_CheckTargetEligibility` | CombatAction | CLAUDE_PROGRESS.md |
| `003191B0` | 471 | `Battle_ProcessActionTargetEntry` | CombatAction | CAPTURE_2026-08-14_08F97-combat-baseline.md +1 |
| `00312FA0` | 382 | `BattleUnit_TryCommitEngageAutoAttack` | CombatAction | XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md |
| `00307BE0` | 137 | `BattleUnit_AdvanceActionState` | CombatAction | XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md |
| `00387A50` | 165 | `BattleRuntime_ResolveAndCacheEffectiveActionId` | CombatFormula | CAPTURE_2026-08-14_08F97-combat-baseline.md |
| `00386C10` | 95 | `BattleRuntime_ResetPersistentStatePrefix` | CombatFormula | CAPTURE_2026-08-14_08F97-combat-baseline.md |
| `00300B80` | 28 | `Inventory_GrantEncodedLootItem` | Items_Equipment_Shops_License | XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md |
| `003003F0` | 152 | `BattleUnit_PublishLocomotionPositionAndFacing` | Movement | PROGRAM_E_PLAYER_PRESENCE_PLAN.md +1 |
| `0026AE90` | 127 | `Movement_SetSteeringMode` | Movement | PROGRAM_E_PLAYER_PRESENCE_PLAN.md |
| `0026B620` | 120 | `Actor_SetFacingHeading_Variant1` | Movement | PROGRAM_C_COMBAT_NATIVE_RESEARCH.md +1 |
| `0026B5A0` | 117 | `Actor_SetFacingHeading_Variant0` | Movement | PROGRAM_E_PLAYER_PRESENCE_PLAN.md |
| `0026AE30` | 82 | `Movement_SetSteeringTargetPosition` | Movement | PROGRAM_E_PLAYER_PRESENCE_PLAN.md |
| `0026ADF0` | 49 | `Movement_SetSteeringTargetActorRef` | Movement | PUPPET_MOTION_END_TO_END_2026-09-04.md |
| `002E5B60` | 35 | `Movement_SetDesiredHeadingTurnLimit` | Movement | PROGRAM_E_PLAYER_PRESENCE_PLAN.md |
| `0026D6D0` | 26 | `Actor_StopRequestedMovement` | Movement | PROGRAM_E_PLAYER_PRESENCE_PLAN.md |
| `0026AF10` | 26 | `Movement_SnapshotSteeringStartPosition` | Movement | PROGRAM_E_PLAYER_PRESENCE_PLAN.md |
| `00383C80` | 13 | `Navigation_HasDataset` | Movement | MOB_REAUDIT5_CHANGELOG.md +2 |
| `003273D0` | 1075 | `PartyConfiguration_SetSelectorsAndReconcileRoster` | Party | XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md |
| `00328B20` | 163 | `PartyConfiguration_RemoveSelector00To06` | Party | XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md |
| `003288F0` | 159 | `PartyConfiguration_RemoveSelector07To25` | Party | XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md |
| `003125E0` | 254 | `BattleUnit_ComputePresentationSuppressionMask` | Presentation | CLAUDE_PROGRESS.md +1 |
| `002ED2A0` | 93 | `CharacterRender_DispatchCombatRelationEvent` | Presentation | CLAUDE_PROGRESS.md +2 |
| `0028FB80` | 88 | `Reward_PublishExpLpPresentation` | Presentation | MOB_LIFECYCLE_RESEARCH_HISTORY.md |
| `00510160` | 72 | `VM_Spawn_ApplySelectedUnit` | Script_VM_Native_Bridge | MOB_LIFECYCLE_RESEARCH_HISTORY.md +3 |
| `005103F0` | 67 | `VM_Spawn_BindEntryAndMarkCapTracked` | Script_VM_Native_Bridge | MOB_LIFECYCLE_RESEARCH_HISTORY.md +2 |
| `00510620` | 63 | `VM_Spawn_SetEntryMapAndResetTransientEntries` | Script_VM_Native_Bridge | CLAUDE_PROGRESS.md |
| `005101F0` | 54 | `VM_SpawnEntry_GetRespawnCooldownTicks` | Script_VM_Native_Bridge | X55S_PHASE_B2_SCRIPT_NATIVE_LIFECYCLE_EVIDENCE.md |
| `00510260` | 32 | `VM_Spawn_SelectContinuousEntry` | Script_VM_Native_Bridge | MOB_LIFECYCLE_RESEARCH_HISTORY.md +3 |
| `00510230` | 32 | `VM_Spawn_SelectPreviousMapEntry` | Script_VM_Native_Bridge | MOB_LIFECYCLE_RESEARCH_HISTORY.md +3 |
| `00510370` | 32 | `VM_SpawnEntry_SetRangeRetireInhibitTag` | Script_VM_Native_Bridge | PROGRAM_B_NATIVE_REFERENCE.md |
| `00354740` | 5 | `thunk_FUN_003541b0` | Script_VM_Native_Bridge | CLAUDE_PROGRESS.md |
| `00511F20` | 5 | `thunk_FUN_00394600` | Script_VM_Native_Bridge | TITLE_NEWGAME_SYNC_RESEARCH.md |
| `005120B0` | 5 | `thunk_FUN_003945e0` | Script_VM_Native_Bridge | TITLE_NEWGAME_SYNC_RESEARCH.md |
| `00512130` | 5 | `thunk_FUN_00394640` | Script_VM_Native_Bridge | TITLE_NEWGAME_SYNC_RESEARCH.md |
| `00236450` | 538 | `SpawnPoint_GeneratePositionFromAuthoredRegion` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md |
| `00306F00` | 303 | `SpawnGroup_RecordMemberDeathAndHandleCompletion` | Spawn_Encounter_Lifecycle | MOB_LIFECYCLE_RESEARCH_HISTORY.md +1 |
| `0023A200` | 185 | `SpawnEntry_ConfigureFreshLifecycleFloatMode` | Spawn_Encounter_Lifecycle | MOB_LIFECYCLE_RESEARCH_HISTORY.md +4 |
| `00239410` | 169 | `SpawnEntry_SetCurrentCandidateState` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md +3 |
| `0023A2E0` | 161 | `SpawnUnit_SetEntryMapAndResetTransientEntries` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md +1 |
| `00236030` | 155 | `SpawnEntry_GetCandidateUnitId` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md |
| `00235FB0` | 121 | `SpawnEntry_GetElapsedTicksSinceLastDeath` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md +1 |
| `00236670` | 103 | `SpawnEntry_QueryRangeReentryPending` | Spawn_Encounter_Lifecycle | X55_NATIVE_REPLAY_CONTRACT.md |
| `00236140` | 95 | `SpawnEntry_GetScriptSelection` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md |
| `00238FC0` | 95 | `BattleUnit_SetNativeLifecycleMode` | Spawn_Encounter_Lifecycle | MOB_WORK_PRIORITIES_DETAIL.md |
| `00235F50` | 93 | `SpawnEntry_GetDeathCount` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md |
| `002366E0` | 93 | `SpawnEntry_GetRespawnCooldownTicks` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md +2 |
| `0023A3B0` | 86 | `Spawn_ApplyScriptSelectedUnit` | Spawn_Encounter_Lifecycle | CLAUDE_PROGRESS.md +5 |
| `002391C0` | 80 | `SpawnEntry_SetRangeRetireInhibitTag` | Spawn_Encounter_Lifecycle | PROGRAM_B_NATIVE_REFERENCE.md +3 |
| `00307090` | 73 | `SpawnGroup_ResetLifecycleLedger` | Spawn_Encounter_Lifecycle | MOB_STATE_LEDGER.md |
| `002360D0` | 39 | `SpawnLaneMap_ResolveBkeiIndex` | Spawn_Encounter_Lifecycle | MOB_LIFECYCLE_SPEC_CURRENT.md +9 |
| `00237080` | 29 | `SpawnEntry_ClearSelectionTransientStateForTeardown` | Spawn_Encounter_Lifecycle | MOB_LIFECYCLE_RESEARCH_HISTORY.md +1 |
| `00229B40` | 469 | `WorldTransitionSnapshot_CaptureRuntimeState` | WorldAreaField | MOB_LIFECYCLE_RESEARCH_HISTORY.md |
| `00584580` | 143 | `WorldTransitionSnapshot_CapturePersistencePairForActiveSlot` | WorldAreaField | MOB_LIFECYCLE_RESEARCH_HISTORY.md +1 |
