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

---

## 2. Gaps

### 2.1 Open or partly open items the pages list themselves

| id | item | cite |
|---|---|---|
| O-01 | **No live runtime observation anywhere in the folder.** Every contract records isolated or replayed execution at best. The search and the follower are not even replayed. | `C-FS:327-342`, `:498`; `C-TL:151-155`; `C-CQ:338-345`, `:436`; `C-NAV:184-190`; `C-POOL:217-219`, `:343-357`; `C-SEP:241-246` |
| O-02 | Whether the actor class is stable across `002E45E0` against **other writers or another thread**. The direct-actor-store question is answered 2026-09-30. | `C-HSD:249`, `:375-377` |
| O-03 | Why two facing entry points exist for **kind-1** callers. | `C-FS:436-439` |
| O-04 | Single-threaded access to the steering entries is not proven. | `C-FS:244-246` |
| O-05 | Whether ordinary play approaches 128 movement bodies, and what the live list's order means to the pass. | `C-POOL:359-363`; `C-SEP:250-253` |
| O-06 | What `00313F80` (the query-mode caller of the resolver) does with its output. | `C-SEP:250` |
| O-07 | What `003DAE30`'s two extra globals `02B57CC8` / `02B57CD0` are. The pool page calls them "unexplained" (see `C-V27`). | `POOL:418-419` |
| O-08 | Who writes `+0x114` through a path other than `[x+0x138]`. Answered "never written" by the 2026-09-18 sweep, which still excludes indexed or block-copy stores. Bit classes are unnamed. | `POOL:347-349`, `:357` |
| O-09 | Why a locomotion reset keeps the dead-end cache; what class 3's "probe gate bit 3" means; what verb kinds 0, 7 and 9 gate. | `C-NAV:194-198`; `NAV:236-237` |
| O-10 | The direct-route check `Navigation_CheckDirectRouteAcrossRegionsXZ` and six other callers of the region lookup are not read. | `NAV:234-236`; `LOCO:322-323` |
| O-11 | Which consumer reads obstacle ids ≥ 128 from the mask; the registry count's double read; the `u8` occupancy wrap. | `NAV:267`, `:271-275` |
| O-12 | Whether the nav root pointer stays 0 until the grid teardown finishes. | `NAV:42` |
| O-13 | `QWALK == 1` read as "blocked" only from `BLKCHK`'s use, which fixes `PATHW`'s polarity at HIGH. `GATE`'s candidate population is a fixture. | `C-CQ:367-370`, `:430` |
| O-14 | `003912E0` with a zero count dimension. | `C-CQ:261-264` |
| O-15 | Animation layer: battle-unit view selector bit 3; where mode `0x16`'s profile comes from; the `@FRM` entry's other parts; the last `0x50` bytes of `003AEF90`; what the engine plays for the 24 commands naming an empty slot; the setters of the two switches. | `ANIM:22-25`, `:47-48`, `:112-113`, `:124` |
| O-16 | The `evt_t0505` debug accumulator may pass 5π if that event is reachable in retail. | `LOCO:918` |
| O-17 | Why force-fight mode skips the ease-in (design intent, not asserted). | `LOCO:309` |
| O-18 | The largest input for which the facing wrap lands in range is "not derived". The `2^58` absorption threshold is derived but not executed. | `HSD:1116-1117`, `:1150-1153` |
| O-19 | The class-1 object behind `+0xB8` is described only by its two offsets. The pair's producer inside `0025DF00` was "not read", later answered by the update notes. | `HSD:1223-1231` |
| O-20 | What `00267260` tests is listed under K-4 as "not traced", and so is the part of `0033BFB0` after the angle. The first half is answered elsewhere (`C-S05`). | `HSD:532` |
| O-21 | What the two zero/negative helpers of the ellipse clamp do. | `CLAMP:179-181` |
| O-22 | The planted siblings `0022D7E0`, `0022DE60`, `00230790`, `0022E7D0`, `003810B0` are "read at call level only and have not been executed". | `SHAPE:205-206` |
| O-23 | The commit-dispatch flags `+0x3D4` / `+0x3D8` / `+0x434` / `+0x3F8`: what object, what they mean, their lifetime, and whether `002F2530` ever returns non-zero. | `C-HSD:261-262`, `:297-312` |
| O-24 | Whether the pre-call zero stores at body `+0x100` / `+0x108` matter, which depends on whether `003DA830` reads them. | `C-POOL:327-330` |
| O-25 | The `+0x88` "mj" class: its mechanism is complete, but "what 'mj' abbreviates is authoring vocabulary the image does not carry". | `POOL:295` |

### 2.2 Structural gaps — a function, formula or format a port needs that no page states

| id | gap | where it shows |
|---|---|---|
| G-01 | **The weather-indexed field-resource banks.** The README names the category as covering them, with the anchors `0026E8D0` resource reconfiguration, `0026E290` dirty observation, `00379290` the WorldAreaField→Movement bridge and `00379630` the alternate rebuild. **No page in the folder documents any of the four.** | `README:3`, `:39-42`, `:56-59` |
| G-02 | **Frame order inside `0025DF00`.** It is not stated whether `002E5030` runs before or after `002E5750`, or where the speed re-issue sits relative to both. Within the world tick, the relative order of `0046AFA0`, the obstacle builder (step 21), the per-slot `002623A0` / `002E5180` consumer and the separation tail is not given as one sequence. Nor is where the frame steps fall relative to the tick. | `HSD:393-395`; `MODE:187-189`; `TURN:236-240`; `POOL:137-141`, `:179`, `:301`; `NAV:249` |
| G-03 | **The field-cell solver.** When `00267260` holds, every walking step goes `002E54A0` → `003DB140` → `00380C40` → `002327D0` / `0022F9B0`. The pages state only that the solver adds sub-steps into the placement displacement and sets bit 4. Its per-cell bodies (`0022D7E0`, `003810B0`, `0022E7D0`, `00381450`, `00380EB0`, `00380E00`) have census-level one-liners only. **No collision-against-terrain formula is stated.** | `HSD:516-524`, `:1494-1544`; `SHAPE:205-216` |
| G-04 | **The field cell lookup and ground height.** `00233050` / `00233110` (cell resolution), `00232090` (blocked mask), `00231890` (second height) and `00231F80` are named with roles but not formulas. The step-toward-radius tail of `003808A0` (bounded increments) gives no increment value. The `026E530` solve of the derived position `+0x50` is census-level. | `POOL:96-115`, `:508-512`, `:533-547` |
| G-05 | **Battle steering modes 1/4, 2 and 6.** The pages carry only the SD-183 summary: "turn toward the goal, move inside a cone"; "turns or gives way to the turning circle"; "orbits a point". The record's "What changes on the page" amendments have not been applied to §6. **No formula.** | `LOCO:270-274` |
| G-06 | **Avoidance and recovery bodies.** The pages give no formula for: `QueryDynamicActorObstruction` `003357B0` geometry (the contract gives only its return codes), `TryStartRandomizedAvoidanceManeuver` `003343D0`, `TryChooseReachableRandomDetour` `00334E00` (beyond one constant `+5`), `ResetAvoidanceStateRandomized` `0033E1F0`, `CheckActorPairClearance` `0033D660` (only `×0.5`, `÷3`), `ResolveDefaultHeadingConstraint` `0033A570`, the stall walker `0033C310` (1,362 B), `SamplePointAlongCurrentPath` `003347C0`, `TryRecoverFromStalledPath` `0033BD70`, the rest of `FinalizeHeadingState` `0033BFB0`, and the publish tail `00469A50`. | `LOCO:112-136`, `:187-191`; `C-CQ:97-101`; `HSD:532` |
| G-07 | **What the stall counter does at 60.** AM-4 says the counter is "capped at 60". Nothing states what reaching 60 triggers. | `LOCO:346-351`, `:119-123` |
| G-08 | **Initial values and sources of the locomotion rates and speeds.** `st+0xF0` (fast rate), `+0xF8` / `+0xFC` (speeds A/B), `+0xE4` / `+0xE8` / `+0x104` (the simple limiter's rates and threshold) and `+0xD0` (stop radius) have no stated writer. Only `+0xEC` has one (`@FCP` slot 3). | `LOCO:266-268`, `:862-868`; `C-TL:50-52` |
| G-09 | **The body weight's source.** `+8` copies the context's float `+0x148`. Who writes context `+0x148`, and its default, are not stated. | `POOL:63-64` |
| G-10 | **The initial value of the `+0xF8` sentinel.** The movement state's `+0xF8` is "a `<0` means unset" sentinel. No page states that it starts negative, or who sets it. | `HSD:201-209` |
| G-11 | **The mode-3 step `003EC040`.** SD-193 says it turns "at a constant angular step per call". The step value, the "forced direction" input and the snap rule are not on the page. The step is in the register record only. | `MODE:182`, `:433` |
| G-12 | **The render-record override's inputs.** `00424080` arms the slide latch on a counter at record `+0x457` reaching `(int)([01DFE0B4] × 30)`. The counter's writer is not stated. Neither are the meanings of the object states `0x10`, `0x35`, `0x36`, `0x0D`, nor what sets record `+0x284` bit `0x8000000`. | `HSD:168-177`, `:303-312` |
| G-13 | **`Movement_PrepareCandidatePosition`'s mode ≠ 0 block** (`world_ctx+0xE8/0xEC/0xEE/0xEF`, `+0x100..+0x108`). The pages give its only reachable use as the push add (`POOL:182`), and the flag block is "described nowhere". | `HSD:243-246`, `:742-745` |
| G-14 | **`002E5180`'s whole behaviour.** The pages state the push consumption, `+0x151` bit 2, the `+0xD4` ground-height store and the `003A1920` measure under `+0x08` bit 2. They do not give the function as a whole; it is cited in pieces from four pages. | `POOL:179-186`; `3DF:306-307`, `:390-392` |
| G-15 | **The corridor leaves `QWALK` `0033D3E0`, `PRED` `00335E50`, `AGENTQ` `00318CA0`.** They are named as callees with no body description. `PATHW`'s polarity rests on `QWALK`'s unread meaning. | `C-CQ:200-205`, `:367-368` |
| G-16 | **The obstacle builder's address and trailer kinds ≥ 2.** The builder is identified only in an `_index` record. Trailer records of kinds other than 0 and 1 "are skipped but still use an id" — their meaning is not stated. | `NAV:242-243`, `:256` |
| G-17 | **The separation extent `003DA730`.** It is given only as an EC7 one-liner ("scales by `1/[rbx]^2` and `1/[rbx+4]^2` and returns the summed correction"). The ellipse-extent formula a port needs is not written as a formula. The `D5A0` output disagrees between pages (`C-V33`). | `POOL:614`; `SHAPE:116-118`; `C-CQ:406-412` |
| G-18 | **Nav dataset trailer `+0x28` layout.** "Readers since read" (`00392740`, `00391597`), but the 32 × `0x20` records are described only as position, radius and kind for kinds 0/1. | `NAV:56`, `:256` |
| G-19 | **The commit dispatch `002EC3F0`'s six apply arms.** Their targets (`003E3120` etc.) store into the render record's `+0x580` sub-record. What that sub-record drives is left to a Presentation page ("the staged look command"). | `C-FS:666-703`; `SLOTS:313-318` |

### 2.3 CONTRADICTIONS — statements a re-implementer would have to choose between

Every quotation below is exact, cut to the clause that matters, with `TAG:line`. The items are in two groups:
- **A** — value-changing: a port gets a different number, address, branch or layout depending on the side it takes. **All of them are page-text only - needs local check.** This session cannot see the executable.
- **B** — stale "not read / open" claims, status banners, naming and counts that do not change a ported value.

A **favoured side** is named only where a dated correction on these pages settles the point. Otherwise the entry says "none by the rule".

#### A. Value-changing (page-text only - needs local check)

**C-V01 — The range of the sign-biased truncating-`fmod` wrap: three different intervals.**
- `HSD:87`: "Both angles are first wrapped into `(-π, π]` by the truncating-`fmod` idiom". `HSD:322`: "**Angle wrap into `(-π, π]`** — used identically by `Actor_SetDesiredMovementHeading` and by both angles inside `ComputeDelta`". `TURN:86`: "makes the result land in (−π, +π]".
- `C-HSD:133`: "**LD-6 — Both angles are wrapped into ~~`(−π, π]`~~ `[−π, π]` before use** *(2026-09-25 …)*". `C-HSD:135`: "That maps `+π → −π` and `−π → +π`, so both endpoints are reachable". `C-FS:170` (corrected 2026-09-28): "+π maps to −π and back to +π, and −π maps to +π and back: a two-cycle". `HSD:1106-1107`: the facing writer stores `+pi` as `-pi` and `-pi` as `+pi`.
- `C-FS:777-778` (`0026A8E0` / `0026A870`, the same idiom): "two `subss` recentre into `[-pi, pi)`".
- `MODE:467` (`0026AC70`, the same idiom): "an exact `(-π, π]` normalize".
- **Favoured:** `[−π, π]` with the endpoints swapping, for `002E4380` and the facing setters. The dated corrections `C-HSD:133` (2026-09-25) and `C-FS:168-170` (2026-09-28) settle it. For `0026A8E0` / `0026A870` / `0026AC70` no correction names those functions, so their ranges are open.

**C-V02 — The loop normaliser `003A1C50`: open or closed at −π.**
- `C-FS:55`: "`xmm0` in **`[−π, π]`** — closed at **both** ends, corrected 2026-09-08 from the 61-byte body". `C-FS:71-72`: "The first loop exits when **`−π ≤ x`** … an input of exactly `−π` skips both loops and is returned unchanged".
- `MODE:98`: "call  0x3A1C50 ; wrap into (-pi, pi]". `MODE:113`: "wrapped into (−π, π] before its sign is taken". `MODE:338`: "the angle normaliser into (−π, π]". `MODE:306-307` (falsification pass 2026-09-13, which postdates the correction): "so the result is closed at `+π` and open at `-π` — which is what §5's "(−π, π]" says".
- **Favoured:** `C-FS:57`'s dated correction (2026-09-08). A **later** pass (`MODE:306-307`, 2026-09-13) re-asserts the old interval without citing the correction, so the dates alone do not close it.

**C-V03 — `Angle_NormalizeRadiansPi` `0033CB70`: range and algorithm.**
- `LOCO:518`: "normalises an angle into (−π, π] by repeated addition".
- `HSD:1160-1163` (the 2026-09-11 correction section): "only when `|x| > 4pi` … does it take the truncating division, and then it **loops** … and leaves an exact `±pi` untouched".
- **Favoured:** `HSD:1160-1163`, a dated correction that names the function.

**C-V04 — The sign of the bias in `0026B5A0`.**
- `C-FS:752-753` (EC7-22, 2026-09-18): "`comiss xmm6, 0` selects `xmm1 = [01CEBC50]` (a `+pi`-class constant) when the input is negative, else `[00915620]` (`-pi`-class)".
- `C-FS:261`: "float bias = (h >= 0.0f) ? +3.14159274f : -3.14159274f;". `TURN:65-66` and `TURN:83`: "+π when heading ≥ 0, −π when heading < 0". `C-FS:708-709`: the same rule for `0026B620`.
- **Favoured:** none by the rule. Four statements against one.

**C-V05 — Does commit flag 0 write the previous-value lanes `+0x250..+0x258`?**
- `C-FS:93-94`: "flag **0** stages the new `{rate, heading, 0}` triple into the steering slot's `+0x120`–`+0x128` and returns; flag **1** additionally shifts the triple into `+0x250`–`+0x258`". `C-FS:481`: "0 stages … 1 additionally shifts it to `+0x250`–`+0x258`".
- `C-FS:99-100` (2026-09-25): "**Flag 0 also writes `+0x250`–`+0x258`.** When the triple changed, the **old** triple is copied there before the flag is tested". `HSD:1193-1195` agrees.
- **Favoured:** `C-FS:99-100`, a dated refinement backed by OPUS block 308's execution.

**C-V06 — The commit tail: `004288B0` *or* `003B3CA0`, or both in turn.**
- `C-FS:95`: "~~or~~ **and then**, when `[slot+0x288]` is set". `HSD:1196-1198`: "calls `FUN_004288B0(record, -1)` unless `+0x284` bit 17 is already set … and, if `+0x288 != -1`, tail-calls `FUN_003B3CA0(+0x288, 30)`".
- Unstruck "or" remains at `C-FS:481` ("calls `004288B0(slot,-1)` or `003B3CA0([slot+0x288],0x1E)`") and `C-FS:766` ("commits through `004288B0` or `003B3CA0`").
- **Favoured:** none by the rule; the strike at `C-FS:95` is undated. Two statements say "and then".

**C-V07 — `003EC260`'s reset arm: word `+6` equal to −1, or not.**
- `C-FS:101-102` (2026-09-25): "A slot whose word `+6` is not `−1`, with `+0x290` bit `0x100000` clear, is reset to `{0, 0, 0}` with `+0x12C = 1.0`".
- `HSD:1191-1192`: "with `+0x290` bit 20 clear and word `+6 == -1` it zeroes the four-lane group `+0x120..+0x12C` to `{0, 0, 0, 1.0}` and returns".
- **Favoured:** none by the rule.

**C-V08 — What context `+0xAC` is: the pitch, or a "rate".**
- `HSD:1202` (K-13, answered 2026-09-12): "**`+0xAC` is the actor's pitch — the rotation about the X axis**".
- `C-FS:479`: "`xmm2 = context[+0xAC]` (the prior rate, handed back unchanged)". `C-FS:93`, `C-FS:765` and `TURN:302` name the group "`{rate, heading, 0}`".
- **Favoured:** none by the rule. K-13 is the only dated determination of the field; the "rate" wording does not cite it.

**C-V09 — Which arm of `0026C120` writes `turn_step` / `turn_limit`.**
- `TURN:472-475` (EC7, 2026-09-18): "arm-4 additionally stamps `dword[obj+0x58] = 0x3E20D97C`, `dword[obj+0x5C] = 0x40490FDB` (π) at [`0026C224`]".
- `MODE:115`: "### Modes 2 and 3 also set the rate". `MODE:165`: "| 2, 3 | choose the turn direction; set rate `π/20` and limit `π`". `C-FS:228` agrees. `SLOTS:283-285` places `0026C1D2` in "its mode-4 epilogue" and the `+0x58` / `+0x5C` stores in "the mode-2/3 block at `0026C1E6`".
- **Favoured:** none by the rule.

**C-V10 — `0026C120` with mode 1: return, or call `002E6300`.**
- `MODE:155-156`: "**Mode 1 does nothing at all in this routine** beyond writing `+0x28` — it falls straight to the epilogue". `MODE:164` and `C-FS:227`: "writes `+0x28` and returns".
- `TURN:476`: "`edx <= 1` falls to `002E6300(rec, rbx, sil)`".
- **Favoured:** none by the rule.

**C-V11 — `turn_limit` π: a ceiling, or a dead store.**
- `C-FS:306`: "The turn is **9 degrees per step with a half-turn ceiling** (`π/20`, `π`)". `MODE:36-37`: "**9 degrees per step, and never more than a half-turn at once.**". `MODE:122`: "**Nine degrees, and a ceiling of a half-turn.**".
- `C-FS:443-445` (DP-1, answered 2026-09-12): "`+0x5C` (π) is read by nothing — a dead store". `MODE:123` (superseded 2026-09-26) and `SLOTS:197` agree.
- **Favoured:** dead store. DP-1 (2026-09-12) and the supersession note (2026-09-26) settle it. The "ceiling" sentences are a corrected claim still repeated unstruck.

**C-V12 — What `002EBE50` runs `003A1C50` as.**
- `TURN:461-462` (EC7, 2026-09-18): "measures `[+0xF0]` sub-record fields `+0x70`/`+0x74` minus the stored values through `003A1C50` (fabsf-shaped)".
- `C-FS:62-68`: `003A1C50` is the two-loop wrap, with no absolute value. `C-FS:486`: "snapshots `sub[+0x70]`/`+0x74` into them after `003A1C50`-wrapping the deltas, derives a frame count `abs(Δ)/sub[+0x6C]`".
- **Favoured:** none by the rule.

**C-V13 — Which op of `00263050` pops the steering slot, and how many pop paths exist.**
- `SLOTS:302-306` (DW-2, 2026-09-12): "**op 2** pops when the record's "pushed" bit (`+0xB` bit 4) is set and clears it … **op 1** decrements `+0x1E0` … and, when the record's slot word `[rcx + rbx + 0x24]` is negative, pops". So there are two pop sites.
- `C-FS:207`: "`003DB2A0 -> 00263050 (op 4, actor+0xB bit 4) -> 002EAAA0 pop`". `C-FS:428-429` (2026-09-18): "`003DB2A0`→`00263050`(op 4, gated on `actor+0xB` bit 4, cleared after) pops". `C-FS:490`: "(`edx-1`/`edx-3`/`edx-4` arms)".
- **Favoured:** none by the rule.

**C-V14 — `002651C0`'s class dispatch.**
- `HSD:1214-1216`: "for class 3 it returns `movementState + 0xAC`, for class 1 the bound object's `[+0xB8] + 0x54`". `MODE:237`: "class 1 → `pitch_approach_step`, class 3 → `+0xAC`". Note that `pitch_approach_step` is the steering record's `+0x54` name (`SLOTS:195`), not the class-1 object's.
- `SLOTS:246`: "`+0xB8`-record floats `+0x54`/`+0xAC` selected by kind 1/2".
- **Favoured:** none by the rule.

**C-V15 — The pitch formula of `003A19C0`.**
- `TURN:200`: "pitch `atan2(dy, √(dx²+dz²))`".
- `TURN:534`: "`xmm8 = [r9] - [r8]`, `xmm6 = [r9+4] - [r8+4]`, `xmm7 = [r9+8] - [r8+8]`; `00861F14` square-roots `dy^2 + dx^2` for the planar magnitude". That is the y and x lanes, not x and z.
- **Favoured:** none by the rule.

**C-V16 — The stall-recovery constants: steps, or thresholds.**
- `LOCO:118-119`: "compares remaining path distance, decrements by **0.01**, adds **1.5**, and tests a counter against **60**". `LOCO:226`: "distance stepped by -0.01, +1.5".
- `LOCO:347-349` (AM-4, 2026-09-12): "dropped by more than **0.01** … → store it and zero the counter `fl+0x14` …; risen above the old value **+ 1.5** … → store it; otherwise **`fl+0x14 += 1`, capped at 60**".
- **Favoured:** none by the rule. AM-4 is the only body-level reading and is not phrased as a correction of §2 / §4.

**C-V17 — The order-goal decoder's accepted opcode range.**
- `LOCO:621-623` (2026-09-02): "bounds it at **`0x4000`-`0x4024`** (37 ids), and switches to **six** goal-resolution bodies". `LOCO:636-637`: "Movement bounds at `0x4024`, and the action table's first empty slot is `0x4025`".
- `LOCO:681-695` (2026-09-08): three tests (`cmp 0x4035`, `cmp 0x4026`, `sub 0x4000 / cmp 0x24`), the band `0x4026`–`0x4035` (16), and five higher opcodes `0x4124`, `0x4125`, `0x414A`, `0x414E`, `0x4165`. `LOCO:358-368` agrees (DE-3, 2026-09-12).
- **Favoured:** none by the rule; no strike or correction note is attached to `LOCO:621-637`. Both later dated readings give the wider band.

**C-V18 — Order `0x4020`: whose `+0x50`.**
- `LOCO:782` (DE-4, 2026-09-12): "`0x4020` samples around the actor record's `+0x50` (an enemy-kind unit only, `003127D7`–`003127FF`)".
- `LOCO:390` (2026-09-18): "takes the **SpawnRecord** at unit `+0x6A0` and points at its `+0x50` — the *live persisted world position*".
- **Favoured:** none by the rule.

**C-V19 — Order `0x4125`: is 20 a radius or a reference.**
- `LOCO:365`: "the 32-family sampler `00312DF0(unit + 0xD0, −1, 20, unit, aux)` — reference position **20**". `LOCO:390`: "`0x4125` (which samples around reference 20)".
- `LOCO:775-783` (DE-4): the signature is `00312DF0(ref, index, param, unit, out)`, and "`0x4125` around the unit's own `+0xD0`". On that reading 20 is the ±param, not a reference index.
- **Favoured:** none by the rule.

**C-V20 — The arrival curve's clamp.**
- `LOCO:560` (the decoded body): "speed = (st->[0xF8] > v) ? v : min(st->[0xFC], v);". If speed A exceeds `v`, the result is `v`, below speed A.
- `LOCO:306-307`: "the quadratic arrival curve below (`rem² × speedB`, clamped between speed A and speed B)".
- **Favoured:** none by the rule.

**C-V21 — The turn limiter's committed-direction path.**
- `LOCO:469-471`: the pseudo-code always recomputes `d = Angle_NormalizeRadiansPi(desired - cur)` and snaps when `|d| <= rate`. `C-TL:96-98` (BL-6): "When the remaining delta is within the rate the result is exactly `desired`".
- `C-TL:174-178` (closed 2026-09-23): "when either bit is set jumps to `003365FF`, which selects `current + rate` … — **stepping in the latched direction without recomputing the wrap delta or the arrival snap**". `C-TL:246` (pass 1, 2026-09-29) scopes the read differently: "It is also **read** above 120° (`0033659D`)".
- **Favoured:** none by the rule. Two open questions follow. Does the snap apply on the latched path? Is the latch read at every error, or only above 120°?

**C-V22 — Mode 3: a curve, or a constant step; and which mode's flag `002654E0` is.**
- `MODE:199`: "along the curve `003EC040(target, +0x78, …)`". `MODE:355`: "`003EC040` (mode-3 curve)". `MODE:239`: "`002654E0` … the mode-4 curve-eligibility flag".
- `MODE:182` (answered 2026-09-30): "there is no easing curve. `003EC040` turns the heading toward the target at a constant angular step per call". `MODE:199` itself uses `002654E0` in the **mode-3** arm.
- **Favoured:** a constant step, settled by the dated answer at `MODE:182`. The "mode-4" label at `MODE:239` is settled by nothing.

**C-V23 — Which kinds `00268380` sizes, and with which defaults.**
- `POOL:80`: "secondary `+0xA8` (class 2) or `+0x38` (class 1), else 0". `POOL:82`: the height for "(class 2) or `+0x68` (class 1)". `POOL:84`: "37 / 37 / 50 for the party class `0x60`, else the secondary context's bytes `+0x104`–`+0x106`". `C-POOL:126`: "**`00268380` sizes the shape only for kind 3**".
- `C-POOL:257-259` (EXP-087, consumed 2026-09-16): "kind 1 → `pb+0x68`/`pb+0x38` with rgb defaults `0x25`/`0x32`/`0x25`, kind 3 → `pb+0xC0 * pb+0x24` / `pb+0xA8` with rgb from `pb+0x104..106`". `HSD:1059` agrees that the class-3 path feeds `state[0x104..0x106]`.
- These conflict on four points: the class labels, which kind gets the 37/50 defaults, their order (37/37/50 against 37/50/37), and whether kind 1 is sized at all.
- **Favoured:** none by the rule. EXP-087 is executed evidence, but not a correction of the page.

**C-V24 — `003DAF20`'s scale: percent, or per-fifty.**
- `POOL:84`: "`a % × +0xF0`, `c % × +0xF4`, `b % × +0xE0 + +0xE4`".
- `HSD:1180-1182`: "`+0xA0 = s104 × [+0xF0] / 50` … (`50.0` at `008F3130`). So the three state bytes are percent-of-fifty scale factors".
- **Favoured:** none by the rule.

**C-V25 — A zero weight: immovable, or fully yielding.**
- `POOL:283-284`: "A zero weight (or a mask bit `00314E10` honours) makes a body immovable; the other body takes the whole separation".
- `POOL:336`: "the weights decide: `w = wB / (wA + wB)`". `POOL:171` and `C-SEP:175`: "A receives `w × separation` and B `(1 − w) × separation`". With `wA = 0`, `w = 1` and A takes all of it. `POOL:41-42` ("the lighter body yielding more") agrees with the formula.
- **Favoured:** none by the rule.

**C-V26 — The free-list head's address.**
- `POOL:207` (key-address table, unstruck): "`02B525C4` / `02B57CC0` | … | free-list head / active-list head".
- `POOL:54`: "**`02B57CC4`** — *corrected 2026-09-13; this read `02B525C4`, which is inside the pool*". `POOL:394-416` and `C-POOL:54` agree.
- **Favoured:** `02B57CC4`, settled by the dated correction of 2026-09-13. A port reading the table would corrupt entry 54 (`POOL:413-416`).

**C-V27 — The cell-mask array and the deferred-registration list: `02AC7Cxx` or `02B57Cxx`.**
- `HSD:446`: "ORs `1<<(id&0x3F)` into the `02AC7CE0` bucket array by `id>>6` (16-byte stride)". `HSD:448-449`: "tail-appends the record to the `02AC7CC8`/`02AC7CD0` list … head `02AC7CC8` / tail `02AC7CD0`". `TURN:231`: "the `02AC7CC8` deferred-register tail".
- `POOL:131-133`: `003DB020` "ORs the body's own bit into the 128-bit mask of every cell it touches (`02B57CE0`, sixteen bytes per cell". `C-SEP:78` agrees. `POOL:418-419`: "`003DAE30` also references `02B57CC8` and `02B57CD0` … Recorded as unexplained".
- `separation-cell-masks-accesses.tsv` routes `STATIC 0x02B57CE0` for `003DAA40`, `003DAAB0` and `003DAE30`. It has **no row for `003DB020`** at either address.
- **Favoured:** none by the rule. If the two pairs are the same globals, `O-07` closes as well.

**C-V28 — What the resolver writes to `out` in query mode.**
- `POOL:174-175`: "the raw separation is written to `out` when the caller did not ask for a push (`00315377`)". `C-SEP:225-226` agrees.
- `C-SEP:316-318` (pass 1, 2026-09-29): "query mode to `00315377`, which stores only the out-parameter `[r15]`, A's share".
- **Favoured:** none by the rule.

**C-V29 — Does the resolver refuse an inactive body in query mode.**
- `POOL:156-158`: a flat list including "both are active this tick (`00314FD6`–`00314FE4`)".
- `C-SEP:134` (P-4): "**`test esi, esi` / `je 00314FEA` — with `mode == 0` the next test is skipped entirely**". `C-SEP:144-146`: "The pool page §2.7 lists "both are active this tick" in a flat list of refusals; it is conditional on the mode". Also `C-SEP:139-140`: push mode adds a seventh, vertical refusal.
- **Favoured:** `C-SEP` P-4. The contract (authored 2026-09-21, pass 1 2026-09-29) explicitly corrects the page.

**C-V30 — Header `+0x0A` of the navigation dataset: region count, or triangle count.**
- `NAV:49`: "+0x0A  u16   regionCount      <= 0x80". This is tested on 461 files: `NAV:59-66`.
- `NAV:344` (EXP-131 table): "`deg = w[root+0xA]` — the triangle count".
- `nav-run-state-block-accesses.tsv`: `+0xA` is read by the search (`003830F4` …), by the cost function next to the `+0x1C` adjacency (`00383883`) and by the re-aim. `+0x6` is read only by `00383A30`, the whole-mesh triangle loop (`NAV:95-96`). The layout favours `regionCount`.
- **Favoured:** none by the rule.

**C-V31 — The portal record's bytes `+5` and `+6`.**
- `NAV:52`: "u8 gated (+4), u8 mapId (+5), u8 classMask (+6)". `NAV:150-156` uses `+5` as the map id and `+6` as the class mask.
- `NAV:346` (EXP-131): "`{w va, w vb, b +4, b class@+5, b flag@+6}`".
- `nav-portal-record-accesses.tsv`: `00383850` compares `+4` with `0xff`, loads `+5` into `ecx` (the map id passed on), and tests `+6` against `r8b` (the class bit). The layout favours `NAV:52`.
- **Favoured:** none by the rule.

**C-V32 — The out-vector of the capsule distance `D5A0`.**
- `C-CQ:409-411`: "Optional out `r14` receives `{Δx, Δy, Δz, horizontalDist}`".
- `SHAPE:116-117`: "`out = {posA - posB, 1.0}`".
- **Favoured:** none by the rule.

**C-V33 — Which verbs reach the navigation caches.**
- `C-NAV:154-155`: "**`setmapidfloor` is the only script verb that reaches this subsystem**". `C-NAV:227-228` repeats it.
- `NAV:191`: "Every change to the override table ends in `003278D0`". `POOL:294` (2026-09-18): the setters "each end in the notify `003278D0`. Their callers are the family `003791D0`..`003795A0`, and those are the tails of the script verbs `00F6`..`010B`". That family includes the floor-ground, wall and mj override verbs.
- **Favoured:** none by the rule.

**C-V34 — Does the time base ever leave 1.**
- `HSD:781-782` (2026-09-02): "It does **not** show the triple ever being written away from `1.0` during play".
- `MODE:136-138`: "**1 or 2**, chosen by the player's Frame Rate setting". `MODE:313-314` (2026-09-13): "**1 at 30 fps, 2 at 60**, written only when `FrameLimit=60`". `TURN:224`: "`01DFE0B8` is the `FrameLimit` scale, 1.0 or 2.0". `C-HSD:471`: "`2 / [01DFE0B4]` in half-rate".
- **Favoured:** none by the rule; the later pages cite another folder's page and do not strike `HSD:781-782`. This decides the mode-4 frame difference (`MODE:140-144`) and every `× [01DFE0B4]` / `× [01DFE0BC]` in §1.2.

**C-V35 — Who drops and raises flag B `02B40534`.**
- `3DF:561` (2026-09-03): "`003B6ED0` and three others store `1`; **three store `0`**; two store a register". That totals 9 stores for 8 sites.
- `3DF:459-466` (BV-5, 2026-09-14): `003B6ED0` 1; `003B7E00` the argument; `003B6F30`, `003B7080` 0; `003B72F0`, `003B7E20` 0 through a register; `003B7BB0`, `003B7C60` 1. `3DF:468`: "§10's "two store a register" are these two zero stores".
- **Favoured:** none by the rule; BV-5 is itemised and later.

**C-V36 — How many `+0x14F` bit-0 readers veto movement.**
- `3DF:329-331`: "**six of its eight readers are movement vetoes** — the two field-pass selectors, `Movement_UpdateActorFrame` …, `002E5750` …, `002E6000` …, `002E6330` … and `002EA7F0`".
- `3DF:358` (narrowed 2026-10-01): "every movement-side reader refuses (the attach guard and two presentation readers excepted)". That implies one of the six does not refuse, and the page does not say which.
- **Favoured:** the 2026-10-01 narrowing. Which reader is "the attach guard" is not stated.

**C-V37 — The animation step's frame windows.**
- `ANIM:95-101`: "the frame counter `+4` goes up; past `duration` the entry is unlinked … **while the counter is below `moveFrames`** … `move += direction x speed[frame] x distance x scale x timebase`".
- `ANIM:163` (pass 1, 2026-09-29): "**survives**: duration and move windows × the frame-rate word; the curve indexed by counter / word". So the windows and the curve index are scaled by the frame-rate word, which §4 does not state.
- **Favoured:** none by the rule; the pass records "survives" without amending §4.

**C-V38 — What the corridor agent's `+0x108` points to.**
- `C-CQ:133`: "every path passes `BattleUnit + 0x80`" (seven `lea` sites).
- `C-CQ:356-359`: "at `003019BF`, `lea rcx, [rsp+0x30]` … copies `unit+0x80..+0x68F` … and overwrites `+0x40`, `+0xD0` and `+0x160` … **The corridor is asked about an edited snapshot of the unit, not the unit.**"
- **Favoured:** none by the rule. Both are dated 2026-09-25.

**C-V39 — What produces the battle stop-and-pivot.**
- `LOCO:104-106`: "**That attribution was wrong**: neither is called from anywhere inside this family. The behaviour comes from the limiter's own 45° deadband". `LOCO:510-514` agrees.
- `LOCO:254-268` (AM-7, 2026-09-12): "two of the six steering modes, and they are inside the family after all … **`ApplyStopAndTurn` (`0033CE60`)** zeroes the speed `+0xB0` … — a stop-in-place pivot". The struck question at `LOCO:252-253` agrees.
- **Favoured:** AM-7, the dated answer that strikes the earlier claim.

**C-V40 — The render-record trailer.**
- `HSD:833-834` (§8f, unstruck): "with a dword at `base + 0x48830` and a 256-byte trailer".
- `HSD:131-132`: "The trailer is therefore `0x130` = **304 bytes**, not 256", under "**PROPAGATED 2026-09-19 (OPUS)**" (`HSD:134`).
- **Favoured:** 304 bytes, settled by the 2026-09-19 correction.

**C-V41 — The headline formula in the index.**
- `README:15`: "`x = sin(heading)*speed`, `z = cos(heading)*speed`, plus a separate vertical term".
- `HSD:91-93` and the correction `HSD:683-690` ("Correction 1 — the headline formula was incomplete (OVERTURNED)", 2026-09-02): X and Z carry `cos(pitch)`.
- **Favoured:** `HSD`, settled by the 2026-09-02 correction.

**C-V42 — How many facing copies a facing change writes.**
- `C-FS:197-199`: "`002E5FB0 -> 002E5E10` steering-record write (wraps again; context->+0xA8; three/four {id,target} sub-records".
- `HSD:1065-1068`: "~~Three or four sub-objects …~~ **Corrected 2026-09-11:** `FUN_003DA850` is a six-byte store, so a facing change writes **one to four copies**".
- **Favoured:** one to four, settled by the dated correction of 2026-09-11.

**C-V43 — `usemapid(0)` actors: no branch, or the default 3-D branch.**
- `3DF:393-394`: "an actor with `usemapid(0)` is neither flat nor 3-D by these selectors".
- `3DF:209-216`: the consumers take the planar path only when flat is true, "else -> spherical path"; "**3-D is the default.**" On that formula a `usemapid(0)` actor takes the spherical branch.
- **Favoured:** none by the rule.

#### B. Stale "not read / open" claims, banners, names and counts (no ported value changes)

| id | the stale or banner side | the side that answers it | note |
|---|---|---|---|
| C-S01 | `README:14` "**DOCUMENTED, tier 1.**" (HSD); `README:20` (ANIM) and `README:23` (NAV) the same; `README:29` "**PARTIAL, tier 1.**" (SHAPE); `README:34` "**PARTIAL, tier 1.**" (POOL) | `HSD:4`, `ANIM:4`, `NAV:4` `status: AUDITED`; `SHAPE:6` `status: DOCUMENTED …`; `POOL:4` `status: AUDITED` | The README also lists 5 of the 18 pages; facing/steering, the mode pages, battle locomotion, the clamps and all seven contracts are absent |
| C-S02 | `LOCO:33` "**PARTIAL.**" | `LOCO:4` "`status: AUDITED`"; `LOCO:37` "nothing on this line stays unread" | body banner against front matter |
| C-S03 | `NAV:23-24` front-matter note "Not read - the locomotion solver that consumes the waypoint …; pending first review"; `NAV:234` "**Not read:** the locomotion solver that consumes the waypoint"; `C-NAV:198` the same | `NAV:24` "promoted: 2026-10-01 DOCUMENTED -> AUDITED"; the solver is read on `LOCO:446-565` | — |
| C-S04 | `HSD:273-274` "`002E45E0` is named but its body is not yet read here" | `TURN:186-228` ("`002E45E0` read in full", `TURN:358`); `HSD:1277-1282` | — |
| C-S05 | `HSD:532` "**Not traced:** what `00267260` tests" (K-4, 2026-09-14) | `HSD:558` K-7 answered 2026-09-02; `3DF:100-108` | the answer predates the "not traced" note |
| C-S06 | `TURN:254-256` "`0026B6A0` … **not read**", "`0026C090` … **not read**", "`002E55C0` … **not read**"; `TURN:363` "What `0026B6A0` / `0026C090` do \| **not read**"; `TURN:421-422` "remain unread" | `TURN:139-142` (ED-5, 2026-09-12); `TURN:321-323` (ED-3, 2026-09-08); `C-FS:476`, `:479-480` | — |
| C-S07 | `SLOTS:106` "`FUN_002627C0(ctx); /* unread */`"; `SLOTS:311-312` "What `FUN_002627C0`, `FUN_002EC2C0`, `FUN_002EBFA0`, `FUN_002EC3F0` or `FUN_002E8EE0` do. Named as the push/pop chain, unread." | `C-FS:413-426` "**All read.**" (2026-09-18) | `SLOTS:313` reads only one of the five |
| C-S08 | `SLOTS:139-140` "**Only 0 and 1 were observed**; what the remaining six encode is not established" | `SLOTS:328` "**Answered 2026-09-15 (FABLE): 4–7 are never written**" | — |
| C-S09 | `SLOTS:215` "**Bits 3–5 and 7 are untouched by any site in the census.**" | `SLOTS:337-340` (2026-09-15): bits 3–5 written by `002EC380` / `002EBE50`, bit 7 by `0026A1A0` / `00263230` | scoped to "the census", but unstruck |
| C-S10 | `C-FS:546-547` "the seven remaining named callees are still unread"; `C-FS:610` "**Eight named callees unread**" (closed at `C-FS:613`) | `C-FS:413-426` | seven against eight is itself a count disagreement |
| C-S11 | `C-SEP:251` "The units and meaning of the weight masks `+0x110` / `+0x114`" (open) | `POOL:334-349` (2026-09-14 / -18): priority bits, vetoes, freezes; `+0x114` never written | — |
| C-S12 | `C-CQ:236-239` "two concurrent `RDEC` calls would race — nothing in this family protects it" | `C-CQ:415-421` (2026-09-25): "**no caller can run concurrently** … the bank has exactly one user thread" | `C-CQ:238` (2026-09-29) re-words it as overwriting by every workbench user |
| C-S13 | `POOL:196-197` "What the nibble and its two sibling fields mean, and what fills the mask table, is **FZ-11**"; `POOL:328-330` "The bullet stays open for those" | `POOL:295` (FZ-11 ANSWERED 2026-09-18); `POOL:301` (UQ-103 ANSWERED 2026-09-18) | — |
| C-S14 | `C-HSD:354-357` "**Still OPEN:** … Class stability and the refusal's reachability stay OPEN"; `HSD:584` (2026-09-29) "the contract's section-14 closure that used one is reopened, CON-172" | `C-HSD:358-361` "**ANSWERED 2026-09-30 … The refusal does not run there, and no caller receives `{0,0,0,1.0}`.**" | `C-HSD:249` (2026-10-01) still keeps "the class's stability across other writers" open (`O-02`) |
| C-S15 | `LOCO:705-707` "**What is not read:** what any of the six cases *does*"; `LOCO:715` "The shared handler is `002367A0`" | `LOCO:709-787` (DE-1..DE-4) and `LOCO:390` (2026-09-18); `LOCO:355` and `LOCO:694`: "~~one shared handler `002367A0`~~" corrected 2026-09-13 | — |
| C-S16 | `HSD:422` "`Movement_SetRequestedSpeed` (`0026D6F0`), 10 distinct callers" | `HSD:1373` "`0026D6F0` — 275 B, 7 A-measured callers" | different measures, unlabelled |
| C-S17 | `3DF:486` "It has 33 distinct callers at 33 sites" | `3DF:605` "33 callers over 37 sites" | — |
| C-S18 | Steering-record size: `SLOTS:166` "32 distinct fields"; `SLOTS:180` "32 fields, **13 named, 19 `UNRESOLVED`**"; `C-FS:188` "the record's 32 fields"; `TURN:290` "The full 32-field census"; `SLOTS:218-221` "21 of 128 bytes are undeclared … `+0x30..+0x33`, `+0x40..+0x4F` and `+0x6B`"; `SLOTS:347-348` "the 33 unaccounted bytes" | `C-FS:118-121` "40 field rows, 33 semantically named (re-measured and extended 2026-09-18)"; `C-FS:449-451` "**9 bytes** in two never-observed spans (`+0x44`–`+0x4B`, `+0x6B`), plus 12 ctor-zeroed bytes" | `steering-record-fields-observed.tsv` has **32** rows, with no `+0x04C` and no `+0x054`; `steering-record-accesses.tsv` has rows at `0x4c` (2) and `0x54` (3) and **57** distinct functions (`SLOTS:215`'s "57") |
| C-S19 | `C-POOL:173` "all four functions the creation sequence calls"; `C-POOL:367` "all four consumers"; `C-POOL:390` "all four consumers" | `C-POOL:93-97` (pass 1, 2026-09-12): "**There are FIVE consumers, not four.**"; `C-POOL:225` names five | — |
| C-S20 | `POOL:27`, `:29-30`, `:61` and `README:33-34` place the body at "the movement context's `+0x138`" | `POOL:74` (corrected 2026-09-18): "`+0xB8` is the **movement** context … and `+0xC0` the **secondary** context"; `C-POOL:56` "`secondaryContext + 0x138`"; `HSD:397` "`pSwbiPresentationState[0x138]`" (actor `+0xC0`) | a naming-only change; the offset is the same |
| C-S21 | `HSD:403` "`Movement_PublishHeadingState` (`002E5C10`) -> CharacterRenderObject +0x240"; `HSD:427` "the CharacterRenderObject record (`+0x240`)"; `HSD:754` "the heading publication into the CharacterRenderObject array" | `HSD:784-830` §8f (2026-09-02): it is the `0x740` render-record array, **not** the `0x668` `CharacterRenderObject` | the offset is the same, the structure differs |
| C-S22 | EC7 notes on `HSD` call nav-shape bodies "heading" helpers: `HSD:1506` `00381450` "the heading delta's length arm"; `HSD:1522` `00381D90` "the three-kind transformer"; `HSD:1538` `00380EB0` "the heading-record builder"; `HSD:1542` `00380E00` "the per-component heading wrap" | `SHAPE:77` `00381450` "box primitive"; `SHAPE:169` and `SHAPE:215` `00381D90` "push-out direction", whose callees include `00380E00` / `00380EB0` | role naming only |
| C-S23 | `MODE:343` and `MODE:525` call `00263CC0` "the movement-kind speed read" | `MODE:198` and `MODE:525` itself: it returns `[+0xB8]+0xA4` (class 3) / `+0x38` (class 1), the **desired heading** | name against value |
| C-S24 | `SLOTS:243` "`edx==0` dispatches on the steering mode (`00265600`)" | `C-FS:483`: `00265600` reads "`sub[+0x28]&0x7F`", which `SLOTS:153-154` names the **movement** mode | the page's own two-field distinction |
| C-S25 | `C-FS:95` "`004288B0(slot, -1)` (slot bit `0x20000` clear)" | `C-FS:803-807` "the `-1` arm *sets* the `0x20000` bit where the contract prose above calls it a clear"; `HSD:1196-1197` reads it as a precondition, "unless `+0x284` bit 17 is already set" | wording; both readings agree on the bytes |
| C-S26 | `CLAMP:119-120` "a fixed global block around `022D9198 … 022D9318`"; `CLAMP:172` "Both write `022D92B0` and `022D9198`" | `CLAMP:199` "`022D92A0`..`022D9318` \| the shared scratch block" | the range start disagrees |
| C-S27 | `CLAMP:113-115` "**Nothing in this function reads the history back**, so what it is for is not established here" | `CLAMP:174` "Its reader is found (2026-09-18, FABLE): `0025C830`" | — |
| C-S28 | `ANIM:124` "Two global switches and a per-list enable can stop all of it" | `ANIM:61-63` (corrected 2026-09-29, `CON-186`): "with it up requests still queue while nothing advances or frees" | — |
| C-S29 | `LOCO:269` "*Not read:* modes 1 / 4, 2 and 6's bodies, and what authors the mode bits"; `LOCO:270-273` "no writer … is traced" | `LOCO:274` (SD-183 answered 2026-09-30) | the answer's amendments are not applied (`G-05`) |
| C-S30 | `3DF:134-136` "it reads as a guard against running the flat path during bootstrap or after a teardown"; `3DF:229-231` "actor system bootstrap … [the gate opens]" | `3DF:116-120` banner "**OVERTURNED in section 10.**"; `3DF:552-597` | flagged by a banner, the text unstruck |

