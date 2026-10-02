# Reconstruction readiness — `FFXII TZA/06-Movement-And-Navigation/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-06-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only. No executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page, with its location |

## Counts

*(filled in when the report is complete)*

## How to read the citations

A citation is `TAG:line` or `TAG:line-line`. The tags stand for these paths, all under `FFXII TZA/06-Movement-And-Navigation/`:

| tag | page | status line as the page states it |
|---|---|---|
| `README` | `README.md` | category index; lists 5 systems (`README:11-37`) |
| `HSD` | `heading-speed-to-position-delta.md` | `status: AUDITED` (`HSD:4`) |
| `C-HSD` | `CONTRACT-heading-speed-to-position-delta.md` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`C-HSD:6-7`) |
| `C-FS` | `CONTRACT-facing-and-steering.md` | `readiness: CONTRACT READY` (`C-FS:6`) |
| `TURN` | `Facing-And-Steering/how-a-character-turns.md` | `status: AUDITED`, `readiness: BEHAVIORALLY UNDERSTOOD` (`TURN:4`, `:8`) |
| `SLOTS` | `Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md` | `status: AUDITED`, `readiness: TYPE RESOLVED` (`SLOTS:4`, `:8`) |
| `MODE` | `Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md` | `status: AUDITED — SD-190 and SD-193 are ANSWERED …` (`MODE:4`) |
| `3DF` | `Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md` | `status: AUDITED — SD-191 and SD-192 are ANSWERED …` (`3DF:4`) |
| `LOCO` | `Battle-Locomotion/battle-locomotion-steering-and-recovery.md` | `status: AUDITED — SD-183 and SD-184 are ANSWERED …` (`LOCO:4`); the body still opens "**PARTIAL.**" (`LOCO:33`) |
| `C-TL` | `CONTRACT-battle-locomotion-turn-limiter.md` | `readiness: CONTRACT READY` (`C-TL:6`) |
| `C-CQ` | `CONTRACT-corridor-query-family.md` | `readiness: BEHAVIORALLY UNDERSTOOD` (`C-CQ:6`) |
| `NAV` | `how-a-unit-finds-its-way-across-the-navigation-mesh.md` | `status: AUDITED` (`NAV:4`) |
| `C-NAV` | `CONTRACT-navigation-search-and-follow.md` | `readiness: CONTRACT READY` (`C-NAV:6`) |
| `POOL` | `the-movement-body-pool-and-the-separation-pass.md` | `status: AUDITED — every box closed …` (`POOL:4`) |
| `C-POOL` | `CONTRACT-movement-body-pool.md` | `readiness: BEHAVIORALLY UNDERSTOOD` (`C-POOL:6`) |
| `C-SEP` | `CONTRACT-separation-pass.md` | `readiness: CONTRACT READY` (`C-SEP:6`) |
| `ANIM` | `how-an-animation-moves-and-turns-a-character-toward-its-target.md` | `status: AUDITED` (`ANIM:4`) |
| `CLAMP` | `clamping-a-point-into-a-volume.md` | `status: AUDITED — SD-180 and SD-181 are ANSWERED …` (`CLAMP:4`) |
| `SHAPE` | `the-unit-shape-distance-primitives.md` | `status: DOCUMENTED — SD-182 is ANSWERED …` (`SHAPE:6`) |

The member `.tsv` files were read only to confirm layouts and counts (§2.4):
`Battle-Locomotion/locomotion-angle-accesses.tsv`, `Facing-And-Steering/steering-record-fields-observed.tsv`,
`Steering-Record/steering-record-accesses.tsv`, `movement-body-accesses.tsv`, `nav-broad-phase-header-accesses.tsv`,
`nav-mesh-triangle-accesses.tsv`, `nav-mesh-vertex-accesses.tsv`, `nav-portal-record-accesses.tsv`,
`nav-region-record-accesses.tsv`, `nav-run-state-block-accesses.tsv`, `nav-slot-pointer-array-accesses.tsv`,
`separation-candidate-scratch-accesses.tsv`, `separation-cell-masks-accesses.tsv`.

"Not stated" means none of these pages says it. Pages outside this folder are named only where a page here defers to them.

---

## 1. Interface

The system has seven parts. The pages give them in this order:

1. **The field step:** heading and speed become a position delta.
2. **Facing and steering:** a heading setter, two mode bytes, two inline steering slots and a per-frame facing integrator.
3. **3-D or flat selection.**
4. **Battle locomotion:** a solver with a turn limiter, avoidance and two recovery layers, driven from combat.
5. **The navigation mesh:** region search, waypoints and the corridor queries above them.
6. **The movement-body pool and the separation pass.**
7. **Two helper families:** the animation-driven move and turn, and the shape and volume geometry.

### 1.1 Entry points (functions, with their callers)

#### The field step, per frame

| entry | callers | what it does | cite |
|---|---|---|---|
| `Movement_UpdateActorFrame` `002E5030` (330 B) | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` | Gates: the class, lifecycle `!= 1`, `pSwbi != NULL`, `pSwbi[0x14F]` bit 0 clear. Then four sibling calls: steering, delta, publish, integrate. Then `002EA7F0` / `003DB020` / `002E6330` | `HSD:393-408`, `:257`; corrected nest→siblings `HSD:721-735` |
| `Movement_UpdateSteeringTowardTarget` `002E45E0` (963 B) | `002E5030`, only when `(u8)(steeringMode − 1) < 4` | target point, bearing, optional snap, remaining distance, speed ramp, near flag, arrival | `TURN:186-228`; `HSD:398-399` |
| `Movement_ComputeDeltaFromHeadingSpeed` `002E4380` (601 B) | exactly one: `002E5030` at `002E50CB` | yaw + pitch + speed → `{x,y,z,1.0}`; override pass-through when `r8d != 0` | `HSD:410-412`; `C-HSD:46`, `:49-54`, `:200` |
| `Movement_PublishHeadingState` `002E5C10` (85 B) | `002E5030` | copies `+0xA0`/`+0xA4` and a 0.0 into render record `+0x240..+0x248` | `HSD:258`, `:445` |
| `Movement_IntegratePositionAndMeasureDisplacement` `002E5610` (314 B) | `002E5030` (mode 0) and `002E5180` | applies the delta, returns displacement² | `HSD:213-230`, `:414-415` |
| `Movement_PrepareCandidatePosition` `002E5380` → `Movement_TransformAndAccumulateCandidate` `002E54A0` | one caller each (`002E5610`, `002E5380`) | world-context path; Prepare is inert when `mode == 0` | `HSD:239-246` |
| `003DB140` → `00380C40(placement, move)` → cell solver `002327D0` | `002E54A0` when `00267260` holds | field-cell move; sets placement `+0x90` bit 4 | `HSD:512-524` |
| `002E5750` facing integrator (935 B) | once per actor per frame, `0025DF00` at `0025E3AA` | dispatches on `+0x28 & 0x7F` | `MODE:187-201`; `HSD:1219-1222` |
| `002E5180` push consumer (506 B) | the world tick's per-slot step `002623A0` (`0026241D`) and `0025E400` | re-runs the integrator with a zero delta when the body's `+0xEC` is set | `POOL:179-186` |

#### Setters and getters the rest of the engine calls

| entry | callers | what it does | cite |
|---|---|---|---|
| `Movement_SetRequestedSpeed` `0026D6F0` (275 B) | "10 distinct callers" / "7 A-measured callers" (see `C-S16`) | class gate, writes `+0xD0` and `[+0xF0]+0x24`, publishes the rate | `HSD:259`, `:422`, `:1371-1381` |
| `Movement_SetRequestedSpeedScaled` `0026D6A0` (38 B) | `00357980`, `00357A20` | `× [01DFE0BC]`, mode `= authored > 0 ? 0 : 2` | `HSD:370-376`; `TURN:492-500` |
| `Actor_SetDesiredMovementHeading` `0026A0D0` (97 B) | 7 callers; among them `Battle_ProcessActionTarget` and `PartyControl_ApplyAnalogLocomotionToActor` | wrapped yaw to `[+0xB8]+0xA4` | `HSD:261`; `C-FS:650-654`, `:714-718` |
| `Movement_ClearSteeringRequest` `002E55C0` (73 B) | `0026AE90` mode 0 | `+0x29=0`; movement mode 2 → `0026C120(actor,0)`; `+0x24=0`; `ctx+0xD0=0` | `TURN:139-142` |
| `BattleUnit_ApplyMovementIntentToWorldActor` `0023A070` (151 B) | battle layer | drives both setters; forces speed 0 under `02089340 & 0x600` | `HSD:429-434` |
| facing writer `002E5E10` (374 B, 4 arguments) | four call sites: `002E28E0`, `002E6B10`, wrappers `002E5F90` / `002E5FB0` | the only writer of `+0xA8`; writes `+0xAC`; 1–4 facing copies; render commit `003EC260` | `HSD:1022-1029`, `:1086-1097`, `:1264-1271` |
| `Actor_SetFacingHeading_Variant0/1` `0026B5A0` / `0026B620` | battle layer: `0023A070`, `003003F0`, `00239210`, `00304180`, `0024C6B0`, `0024C870`, `0024F9B0`, `0026C120`, `00341AB0`, `0034BE50` | wrap, then `0026B6A0(a,t,0|1)`, then tail `0026C090` | `C-FS:44-49`; `HSD:1272-1276` |
| `0026B6A0` / `0026C090` | the two variants | kind 1: context `+0x38`/`+0x48`; kind 3: `002E5FB0` → `002E5E10` / record `+0x34` | `C-FS:193-202`, `:476` |
| `Movement_SetSteeringMode` `0026AE90` (127 B) | 14 call sites: 12 pass 0; `VM_ActorSteerToPosition` `00357A20` and `VM_ActorSteerTowardActor` `00357980` pass `+0x2C == 0 ? 1 : +0x2B` | writes `+0x29`; modes 2–4 collapse to 1 when `+0x2C == 0.0` | `TURN:97-116`, `:158-175` |
| `0026C120` movement-mode setter (354 B) | 29 call sites in 27 functions (modes 0/2/3/4) | writes `+0x28`; turn direction; rate; mode-4 early end; mode-0 teardown | `MODE:46`, `:159-167`, `:257-273` |
| `002690D0` untimed turn body | verbs `raturn_25e`, `raturna`, `raturnya`, `003578B0`, `unkCall_3092` | frame count from `turn_step`; stores mode 5 directly at `002692E8` | `MODE:203-213` |
| `0026C330` timed turn setter | `turnt`, `rturnt_4b`, `rturnat`, `dira`, `dir_4e` | `+0x68 = +0x66 = [01DFE0B4] + frames / [01DFE0BC]` | `MODE:212-214` |
| `setaccr` `00352D10` / `setaccr_123` → `00269C30` | script | `+0x2C = accel × [01DFE0BC]`, `+0x2B = mode` (default 4) | `TURN:177-179`; `SLOTS:191` |
| `00269F90` slot selector (36 B) | `002EAB80`, `002EAAA0` only (3 `E8` sites) | cursor `ctx+0xF0 = ctx + 0x120 + sel×0x80` when `sel <= 1` | `SLOTS:51-68`, `:95-97` |
| push `002EAB80` (99 B) / pop `002EAAA0` (145 B) | push: `00263230` from `003DBDC0`; pop: `00263050` from `003DB2A0` (the op numbers disagree, `C-V13`) | depth-one steering stack; pop replays shape 0 / 1 | `SLOTS:99-135`, `:296-306`; `C-FS:204-212` |
| `Actor_GetWorldPosition` `00265020` (61 B) | 79 callers / 104 sites | classes 1 and 3 only; refusal writes `(0,0,0)` | `C-HSD:78-81`; `HSD:644-647` |
| `00265200` heading accessor (55 B) | 33 callers | class 1 → `[+0xB8]+0x38`, class 3 → `+0xA8`, else 0 | `3DF:67-75`; `HSD:1001-1011` |
| `002651C0` pitch accessor / `0026B520` its setter | `002E5750` | class 3 → `+0xAC` (class split disputed, `C-V14`) | `HSD:1214-1222` |
| `00264460` 3-D test (37 B), `00267260` flat test (78 B), `003B7730` gate (27 B) | `002E4380`, `002E45E0` ×2, `002E5610` | see §1.2 | `3DF:83-126`, `:488` |
| `setflystatus` `0026A7F0`, `setfloatstatus` `0026A7C0` | verbs `01E0` / `01E1`, and `BattleUnit_RefreshActorRuntimeFromDefinition` | controller `+0x151` bits 0 / 1 | `3DF:279-305` |

#### Battle locomotion

| entry | callers | what it does | cite |
|---|---|---|---|
| `BattleUnit_UpdateCombatNavigationStep` `00325BB0` (465 B) | `caseD_4000`, `BattleUnit_AdvanceTargetedMovementOrder`, `BattleUnit_AdvanceStandardActionState`, `FUN_003082F0` (all CombatAction) | builds or reuses the route, then takes the next waypoint and hands it to the solver | `LOCO:54-56`, `:404`; `NAV:205-210` |
| `caseD_4000` `002FDA60` | the action handler table | order phases 0/1/2 at unit `+0x6B4` | `LOCO:374-380` |
| `BattleLocomotion_DecodeOrderGoal` `00312730` (965 B) | `caseD_4000` | opcode → goal | `LOCO:352-390`, `:681-695` |
| `BattleLocomotion_SolveAndPublishNextStep` `00336CE0` (342 B) | `00325BB0` | `.ard` class row `+0x18` bits 1–3: 1/3 → no solve; 2 → `SolveClassMode2Step`; else `SolveDefaultStep` | `LOCO:58-83`, `:327-338` |
| `ApplyHeadingTurnLimiter` `003364D0` (564 B) | both solver variants, `ResolveTargetSpacingAndAvoidance` | the 45°/120°/20° loop | `C-TL:44`; `LOCO:446-480` |
| `ComputeStepDistance` `00339BF0` (503 B) | both solvers | quadratic arrival curve | `LOCO:529-565` |
| steering-mode dispatcher `00339F00` (531 B) | `SolveDefaultStep` only (`0033BF8D`) | flag word low 5 bits → modes 1/4 `0033CEF0`, 2 `0033D200`, 3 `ApplyStopAndTurn`, 5 `ApplySimpleHeadingLimit`, 6 `0033BAA0` | `LOCO:254-274` |
| other members | see the tree | the full tree and the 19-member subtree | `LOCO:58-83`, `:177-216` |

#### Navigation

| entry | callers | what it does | cite |
|---|---|---|---|
| `00384160` bind and rebase (372 B) | area setup | stores slot 4's address in `02AEDFB0`, rebases the offsets | `NAV:39-42` |
| `00383A20` clear / `00383C80` test / `00383840` get | startup chain and area-unload reset / tick / readers | — | `NAV:42`, `:547` |
| `00383620` → `Navigation_FindPathAndBuildPortalWaypoints` `00382FF0` (1,575 B) | `00325BB0` | returns 0 / -1 / -2 / -3 | `NAV:116-143`; `C-NAV:51` |
| `00383670` follow step (204 B) → `Navigation_AdjustPortalWaypointForClearance` `00383C90` | `00325BB0` | advances `next[]`, re-aims, keeps the mover's `y` | `NAV:195-203` |
| `Navigation_FindRegionForPointXZ` `00383F10` (542 B), `00382D10`, `00383A30`, `00383740` | the search and 6 other callers ("not read") | region lookup | `NAV:71-97`, `:236` |
| `003278D0` invalidator (84 B) | every override-table change (`setmapidfloor` family) | wipes both caches of every live unit | `NAV:191-193`; `C-NAV:85-90` |
| `BattleUnit_GetNavigationClearanceRadius` `0030A130` (40 B) | `00325BB0` ×2, plus combat-AI callers | `maxss` of the two radii; the caller multiplies by 1.414 | `C-NAV:106-121` |
| obstacle builder (address only in an `_index` record) | step 21 of the world tick | refills the 288-id obstacle grid each frame | `NAV:245-275` |
| corridor queries `PVAL` `00335B60`, `GATE` `003357B0`, `PATHW` `0033A3D0`, `BLKCHK` `00335F90`, `LQUERY` `00391410` | the locomotion solver; `AiOrder_CheckActionPreconditions` `00301830` (snapshot) | small-integer verdicts | `C-CQ:74-101`, `:349-366` |

#### Body pool and separation

| entry | callers | what it does | cite |
|---|---|---|---|
| `003DAE30` pool init (230 B) | `00266D10` (`00267141`) | threads 128 entries, clears the masks and heads | `POOL:50-54` |
| `003DA8A0` allocate / `003DAD00` release | `002E3500` / `002E3D00`, `002E3AF0` | free-list LIFO; NULL when exhausted | `C-POOL:45-46`, `:133-141` |
| `002E3500` create (128 B) | `002E28E0` (`002E2C21`), `002E3580` | release old, allocate, store at `+0x138` untested, then 5 consumers | `POOL:60-70`; `C-POOL:143-151`, `:93-97` |
| `003DB020` register (168 B) | `002E5030` when `002EA7F0` passes | sets `+7`, computes cell bits, ORs into the masks | `POOL:124-133` |
| `003DAA40` reset / `003DAC70(00314F30)` pass | `World_UpdateSimulationTick` at `003140C5` / `00314244` | per-tick reset, then the pair walk | `POOL:135-152`; `C-SEP:47-54` |
| `00314F50(A,B,mode,out)` resolver (1,080 B) | `00314F30` (mode 1), `00313F80` (mode 0) | refuse / contact / push split | `C-SEP:126-146`; `POOL:154-175` |
| `0046AFA0` (128 B) | `World_UpdateSimulationTick` `00314020` | divides the per-tick sums into the cell centre | `POOL:301` |

#### Helper families

| entry | callers | what it does | cite |
|---|---|---|---|
| command `0x1A` handler `00520C10` → `003E6340` → `003AED70` | the animation command stream | builds and queues a move/turn request | `ANIM:39-66` |
| `003E6EF0` → `003AF220` → `003AEF90` | the actor update (`0025DF00`, via the pair `002E5750` consumes) | per-frame step and turn, clamped | `ANIM:88-104`; `HSD:1229-1231` |
| `003AF2B0` pool init | the character render system's initialiser | 128 × `0x60` at `[02B3F530]` | `ANIM:59-60` |
| `00361DE0` ellipse / `003623C0` box / `00363FD0` segment | the Audio-filed volume walk (by record byte `+9`) | clamp a point into a volume | `CLAMP:205-215` |
| D4B0 `0022D4B0`, FA0 `00380FA0`, EB0 `00381EB0`, primitives | planted by `002315E0`; `0022F8B0` | shape distance and containment | `SHAPE:69-94` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

**WorldActor** (`HSD:278-285`; `3DF:164-171`; `C-FS:124-128`):
- `+0x03`: packed `(kind<<5)|sequence`. Movement needs `& 0xE0 == 0x60`; position read admits class 1 or 3.
- `+0x08`: bit 1 "uses the map", bit 2 3-D displacement measure.
- `+0x09`: bit 0 "field movement enabled".
- `+0x0B`: bit 4 "pushed".
- `+0x0C`: bit 4, set by the speed setter.
- `+0x0D`: bit 4 near flag; bit 5 position offset present.
- `+0x18`: `== 1` refuses push and pop.
- `+0xB8`: movement context. `+0xC0`: the controller, also called the secondary context.
- Sources for `+0x08`/`+0x09`/`+0x0B`/`+0x0D`: `3DF:381-407`; `SLOTS:302-304`; `TURN:219-223`; `HSD:547-553`.

**Movement context, class 3** (`0x230` B; `C-FS:153-155`). The page sources are `HSD:287-296`, `:984-1043`, `:1202-1213`, `C-FS:130-137` and `TURN:266-276`:

| offset | field |
|---|---|
| `+0x00..+0x08` | position |
| `+0x30` | start snapshot |
| `+0x40..+0x48` | position offset |
| `+0x58` / `+0x68` / `+0x78` | facing copies |
| `+0xA0` | pitch, motion |
| `+0xA4` | yaw, motion |
| `+0xA8` | facing |
| `+0xAC` | aux / pitch for presentation (disputed, `C-V08`) |
| `+0xB4` / `+0x224` | the steer-channel mirrors |
| `+0xD0` | requested speed |
| `+0xDC` | slot selector |
| `+0xF0` | steering-record cursor |
| `+0xF8` | override magnitude, and a `<0` "unset" sentinel |
| `+0x104..+0x106` | percent bytes for the body shape |
| `+0x120` / `+0x1A0` | the two inline `SteeringRecord`s |

**Controller / secondary context at actor `+0xC0`** (`3DF:173-178`, `:282-377`):
- `+0x138` → the movement body.
- `+0x14F`: bit 0 attached, bit 1 fight stance, bit 2 attach offsets, bits 3–7 standard-motion variation.
- `+0x151`: bit 0 fly, bit 1 float, bit 2 moved this frame, bits 3/4/5/7 other.
- `+0x152`: locomotion kind (1 ground, 2 airborne).
- `+0x120/+0x128/+0x130`: attach-offset pointers.

**SteeringRecord, `0x80` B, two inline** (`SLOTS:182-202`; `C-FS:118-122`, `:452-465`):

| offset | field |
|---|---|
| `+0x00` | target, 16 B |
| `+0x10/+0x14/+0x18` | resume a/b/c |
| `+0x1C` | resume target handle |
| `+0x20` | arrival radius |
| `+0x24` | requested speed |
| `+0x28` | movement mode; bit 7 set by the turn body |
| `+0x29` | steering mode |
| `+0x2A` | target kind |
| `+0x2B` | configured steering mode |
| `+0x2C` | ramp acceleration |
| `+0x34` | target heading |
| `+0x38` | turn start heading |
| `+0x3C` | spin rate |
| `+0x50/+0x54` | approach steps |
| `+0x58` | `turn_step` π/20 |
| `+0x5C` | `turn_limit` π, a dead store |
| `+0x60` | derived turn frames |
| `+0x62` | flags: bits 0–2 resume shape, bits 3–5 dispatch mode, bit 6 turn direction, bit 7 |
| `+0x63` | steer arm state |
| `+0x64` / `+0x66` | progress byte / frame cap |
| `+0x65` | teardown gate |
| `+0x68` | turn frames |
| `+0x6A` | dispatch latch |
| `+0x6C` | initiator turn step |
| `+0x70/+0x74` | steer targets |
| `+0x78` | turn frame index |
| `+0x7C` | steer speed request |

**Character render record array** (Presentation-owned, written by Movement): pointer `022C6F28`, 160 × `0x740` (`HSD:127-132`, `:303-312`).
- `+0x000` i16 id, `-1` = empty.
- `+0x0CC` state.
- `+0x120..+0x12C` the `{aux, facing, 0, 1}` group, read by `00420A40` (`HSD:1191-1213`).
- `+0x240..+0x248` the published heading.
- `+0x250..+0x258` the previous group.
- `+0x284` / `+0x290` flags.
- `+0x457` frame counter.
- `+0x610..+0x62F` the override save and latch.

**MovementBody, `0x130` B** (`POOL:229-250`). See `C-V23`–`C-V27` for disputed details:

| offset | field |
|---|---|
| `+0/+2/+4` | links |
| `+6` | layer |
| `+7` | active |
| `+8` | weight |
| `+0x18` | pair bits |
| `+0x30` | placement record: position, orientation, cell words `+0x80..+0x8E`, flags `+0x90`, ground height `+0xAC`, requested speed `+0xC8` |
| `+0xE0/+0xE4` | height / base offset |
| `+0xE8..+0xEF` | push bookkeeping |
| `+0xF0/+0xF4` | radii |
| `+0xF8` | heading |
| `+0xFC` | margin |
| `+0x100..+0x108` | push |
| `+0x110/+0x114` | masks |
| `+0x119` | owner |
| `+0x120` | cell bits |

**Battle locomotion state `st` = `BattleUnit + 0x80`** (`LOCO:276-277`, `:853-873`; `C-TL:48-54`):
- `+0xE0` current heading (`= BU+0x160`).
- `+0xEC` / `+0xF0` slow / fast turn rate. `+0xEC` comes from `@FCP` slot 3, `LOCO:862-868`.
- `+0xF8` / `+0xFC` speed A / B.
- `+0xD0` stop radius.
- `+0x40` approach mode.
- `+0x170` locomotion flags (`BU+0x1F0`).
- `+0x174` placement mode / mover class (`BU+0x1F4`).
- Flag block `fl` at ctx `+0x100`: `+0x21` direction pair, `+0x38` bit 3 turning, `+0x3C` bit 0 fast latch, `+0x10` / `+0x14` stall distance and counter (`LOCO:346-350`).
- Mode flag word `BattleUnit +0x80`: bits 0–4 mode, 5–14 countdown, 15 orbit direction (`LOCO:274`).

**Order record**: `+0` u16 opcode, `+2` s16 parameter (`LOCO:672-675`). Opcode bands are at `LOCO:685-695` and `:358-390`.

**NavDataset** = map pack slot 4 (`NAV:44-57`). It has a header, then:
- vertices 8 B: x, z;
- triangles 8 B;
- portals 8 B: `+4` gated, `+5` map id, `+6` class mask;
- regions `0x22` B;
- adjacency `regionCount²` u16, 1-based;
- the grid;
- the trailer table.

**NavPath** at unit `+0x200`, `0x490` B (`NAV:104-112`). **Obstacle grid**: `0x24`-byte bitset per cell plus a u8 occupancy (`NAV:245-257`).

**Map-id override table** `0209A3E0`: 80 × `{mask, value}` in three sub-tables. Floor 0–31, wall 32–63, mj 64–79 (`POOL:294`).

**Packed actor handle**: bits 30–20 tag, 19–16 slot, 15–0 index (`C-CQ:140-152`; `NAV:493-503`). **`CorridorNavAgent`**: `0x110` stack local; `+0x108` → `BattleUnit+0x80` (`C-CQ:133-134`).

**Animation request pool entry** `0x60` B, and the `@FRM` profile table (`ANIM:59-82`).

**Volume record**: `+9` kind, `+0x20` centre, `+0x30/+0x34` radii, `+0x50` angle, `+0x14` / `+0x40` segment chain (`CLAMP:39`, `:205-227`).

**Shape record**: `+0` type, `+0x10` forward, `+0x50` inverse, authored in the nav chunk (`SHAPE:101-118`, `:177-181`).

#### Formulas a port can take as stated

| formula | cite |
|---|---|
| delta: `X = sin(yaw)cos(pitch)speed`, `Y = sin(pitch)speed`, `Z = cos(yaw)cos(pitch)speed`; flat branch drops pitch; `W = 1.0` on every exit | `HSD:331-348`; `C-HSD:93-111` |
| the fmod wrap (range disputed, `C-V01`) | `HSD:322-329`; `C-FS:259-264` |
| the large-angle reconstruction rule for the facing wrap | `HSD:1125-1157` |
| published rate `= [01DFE0B8] × 30 × 3.6 × speed` | `HSD:378-386` |
| steering ramps (modes 1–4), near flag, arrival | `TURN:209-245` |
| mode-4 timed interpolation | `MODE:200`; `C-FS:493` |
| turn limiter | `LOCO:448-479`; `C-TL:60-99` |
| step distance | `LOCO:531-564` |
| order-goal sampler `offset = LCG % (2p+1) − p`, 9 tries | `LOCO:737-738`, `:784-787` |
| separation geometry and the weight rule | `POOL:252-265`, `:334-340`; `C-SEP:165-175` |
| portal cost `trunc(100 × d)` | `NAV:158-161` |
| waypoint split and clearance | `NAV:131-140`, `:173-176` |
| clearance factor `0x3FB4FDF4` | `C-NAV:106-121` |
| animation step | `ANIM:95-104` |
| corridor `BLKCHK` and `PATHW` | `C-CQ:323-336` |
| shape primitives | `SHAPE:107-118` |
| clamps | `CLAMP:37-115` |

### 1.3 State (globals and objects, with lifetime)

| state | lifetime as stated | cite |
|---|---|---|
| movement-body pool `02B4E4C0` (128 × `0x130`), heads `02B57CC0` (active) / `02B57CC4` (free) | threaded per area by `003DAE30` from `00266D10`; a body lives as long as its actor's presentation | `POOL:50-70`; `C-POOL:53-60` |
| cell masks `02B57CE0` (32 × 16 B), candidate scratch `02B57EE0` | cleared at the head of every world tick; filled per frame | `POOL:137-139`; `C-SEP:84-89` |
| cell-centre accumulators `02CA6034..02CA604C` | summed per placement; divided and reset once per simulation tick by `0046AFA0` | `POOL:301-316` |
| steering records | inline in the context; never allocated or freed | `SLOTS:71-74` |
| time base `01DFE0B4` (int), `01DFE0B8`, `01DFE0BC` (f32) | ship as 1 / 1.0 / 1.0; `01DFE0B4` written when `FrameLimit=60` (values disputed, `C-V35`) | `HSD:384`; `MODE:311-314` |
| near-flag ratio `02164200` | 0 in the image, 3.0 from boot (`00266D10` → `002EBE40`) | `TURN:219-223` |
| flat-path gate `02B40530` (A) / `02B40534` (B) | zero at load; A follows the engine's lifecycle; B dropped and raised by the party-swap verbs | `3DF:449-475` |
| nav root `02AEDFB0`, `NavGridParams` `02AEE060`, obstacle list `02AEE0C0` / count `02AEE0BC` | per area; the obstacle grid is refilled every frame | `NAV:40-42`, `:245-251`; `C-CQ:137` |
| map-id override table `0209A3E0` | zeroed at area initialisation by `0026E960`; written by the verbs `00F6..010B` | `POOL:294` |
| `NavPath` per unit | wiped by `003278D0` on any override change; the route-only wipe by `003291B0` | `C-NAV:77-90` |
| animation request pool `[02B3F530]`, switches `02B3F53C` / `02B3F540` | allocated once by the render system's initialiser; setters of the switches not traced | `ANIM:59-63`, `:124` |
| render record array `022C6F28` | `CharacterRenderSystem_AllocateAndInitialize` `003325D0` | `HSD:127-132` |
| shared workbench `022D91B0` (vf1), `022D92xx` scratch | process-global; overwritten by any user; one user thread | `C-CQ:415-421`, `:514-522`; `CLAMP:119-124` |
| RNG | avoidance and detours: CRT `rand` via IAT `008C3098`; order sampler: shared gameplay LCG `00328370` | `LOCO:641-666`, `:750-758` |

### 1.4 Order (what runs when, and what triggers it)

- **Per actor, per frame, inside `0025DF00`:**
  1. While `+0x29 != 0`, re-issue `Movement_SetRequestedSpeed(+0x7C × [01DFE0BC])` (`TURN:236-240`).
  2. `002E5030`: steering (modes 1–4), then delta, publish, integrate, and the grid / deferred tail (`HSD:393-408`).
  3. `002E5750` at `0025E3AA` (`MODE:187-189`).
  4. The order of 2 and 3 inside `0025DF00` is **not stated** (`G-02`).
- **Per world tick, `World_UpdateSimulationTick` `00314020`:**
  - `003DAA40` first (`003140C5`) and the separation walk at its tail (`00314244`) (`POOL:137-141`);
  - `0046AFA0`, at a position not stated (`POOL:301`);
  - the obstacle builder at "step 21" (`NAV:249`);
  - the per-slot step `002623A0` → `002E5180`, which consumes pushes (`POOL:179`).
  - Pushes are consumed on the next candidate position and gone the tick after (`C-SEP:157-163`).
  - Registration is per frame and the pass per tick; `+0x07` couples the two (`C-SEP:84-89`).
- **Battle units:**
  1. CombatAction runs `caseD_4000` phase 0, which decodes and resets the path (`LOCO:374-380`).
  2. Phase 1 runs each tick: re-decode for the chasing opcodes, then `IsApproachConstraintActive`, else `00325BB0`.
  3. `00325BB0` runs search or follow (`NAV:205-208`), then `00336CE0`.
- **Triggers:**
  - script verbs: the move family, turn verbs, `setaccr`, `setvelrotangzx`, `setmapidfloor` family, `usemapid`, `attach`, `setfly/floatstatus`, `capturepartyforsummon` and siblings (`TURN:158-182`; `MODE:197-201`; `NAV:178-193`; `3DF:279-470`);
  - script start and end (steering push and pop, `SLOTS:295-310`);
  - the animation command `0x1A` (`ANIM:39-55`);
  - the animation latch inside `00424080` (`HSD:168-177`).

### 1.5 Dependencies (on other systems)

| system | what this one uses | cite |
|---|---|---|
| 17 Presentation | the render record array (override latch, heading publish, `{aux,facing}` commit, the attach transform, mode-5 animation wait, tween bits) | `HSD:119-180`, `:1184-1213`; `MODE:183`, `:201` |
| 04 Actor-Entity | the record carver and `+0x03`; the context region map; manager slots `02098E10`; the packed handle | `C-FS:145-161`; `C-CQ:135-152` |
| 07 Combat-Action / 09 Combat-AI | entry into battle locomotion; order ids; `BattleUnit_GetBySlotIndex` | `LOCO:54-56`; `HSD:604-642` |
| 03 World-Area-Field | map pack slot 4 (nav), slot 16 (`SP1` volumes), field cells and attributes, `00377C20` | `NAV:39`; `CLAMP:219-220`; `POOL:104-115` |
| 01 Script VM | every steering, turn, door and party-swap verb | §1.4 |
| 00 Core runtime | `FrameLimit` time base; half-rate test `001EDDA0`; the transform workbench | `C-HSD:469-472`; `C-CQ:514-522` |
| 21 RNG | CRT `rand` (avoidance) and the gameplay LCG (order sampler) | `LOCO:750-758` |
| 18 Audio | clients of the clamp family and of `003A1C50` | `CLAMP:205-215`; `C-FS:656-659` |
| 19 Save | `00266D10` clears the `0x1538`-byte persistent block | `TURN:452` |
