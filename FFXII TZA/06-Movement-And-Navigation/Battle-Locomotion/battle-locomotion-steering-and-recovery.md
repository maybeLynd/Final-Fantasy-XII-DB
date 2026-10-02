---
system: Battle locomotion — steering, avoidance and recovery
category: 06-Movement-And-Navigation
status: AUDITED — SD-183 and SD-184 are ANSWERED and every box on the page is closed (owner re-status 2026-09-30, OPUS) — the modes 1/4/2/6 bodies and the mode-bit authors (AM-7's residue, registered as SD-183 2026-09-30) and whether any heading writer stores outside [-pi, pi] (SD-184) are answered in §6; AM-5 answered 2026-09-18 (the 0x4020 case read: wander around the unit's own spawn position; every opcode's case now read across DE-1..DE-4); the 0x4021/0x4025 holes explained 2026-09-08 (DE-2)
owner_layer: PrimaryOwner:Movement — driven entirely from CombatAction
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 3
  last_pass: 2026-09-08
  last_pass_state: GN160-xiionline-61-rand-and-order-opcodes
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record GN160-xiionline-61-rand-and-order-opcodes; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# Battle locomotion — steering, avoidance and recovery

> Why units in battle stop and pivot instead of turning while they walk, why they shuffle around
> each other instead of overlapping, and what happens when one gets stuck.

~~**PARTIAL.**~~ **AUDITED.** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`, every box closed 2026-09-30)* The family's 26 functions, their call structure, the two recovery layers' constants and
the **complete turn limiter** are read. ~~Most other individual bodies are not.~~ *(Corrected 2026-09-30, SWE2-DATA:
since this line was written, the arrival curve (§10), the avoidance RNG and the order-goal decoder (AM-5, AM-6,
DE-1..DE-4) and two of the six steering modes (§6) have been read, and the exclusive subtrees are bound. What
remains unread is the other steering modes' bodies and who sets the mode bits: `SD-183`.)* *(2026-09-30, OPUS owner read: SD-183 is ANSWERED and read into §6, so nothing on this line stays unread.)*

## 1. What the player sees

Watch a battle without fighting and the movement has a distinct character. A unit given a new
direction does not swing smoothly onto it — past a certain angle it **stops, turns on the spot, then
walks**. Units approaching the same target do not pile into one another; they **spread out and
sidestep**. And a unit that cannot make progress does not stand there forever — after about a second
it **tries something else**, often a visibly odd little detour.

None of that is animation. It is a steering solver with two independent recovery layers, and this
document is that solver.

## 2. Native mechanism

### The pipeline

`BattleLocomotion_SolveAndPublishNextStep` (`00336CE0`) is the top of the family. It is reached from
`BattleUnit_UpdateCombatNavigationStep` (`00325BB0`, Movement), which is driven from four
**CombatAction** sites — so battle movement is *requested by combat*, not by the movement system.

```
BattleUnit_UpdateCombatNavigationStep            (00325BB0, Movement)
  -> SolveAndPublishNextStep                     (00336CE0)
       -> BuildSolverContext                     (00336710)
       -> SolveClassMode2Step                    (003394A0)   one unit class
       |    -> ComputeStepDistance
       |    -> ApplyHeadingTurnLimiter
       -> SolveDefaultStep                       (0033BED0)   the other
            -> ComputeStepDistance               (00339BF0)
            -> ResolveDefaultHeadingConstraint   (0033A570)
            -> ResolveTargetSpacingAndAvoidance  (00338140)
            |    -> ApplyHeadingTurnLimiter      (003364D0)
            |    -> CheckActorPairClearance      (0033D660)
            |    -> TestForwardStepClearance     (00335B60)
            |         -> QueryDynamicActorObstruction (003357B0)
            |    -> TryStartRandomizedAvoidanceManeuver (003343D0)
            -> UpdateDetourRecoveryState         (0033C870)
            |    -> TryChooseReachableRandomDetour     (00334E00)
            |    -> ResetAvoidanceStateRandomized      (0033E1F0)
            -> UpdateStallRecoveryState          (0033C200)
            |    -> ComputeRemainingPathDistance  (00334950)
            |    -> TryRecoverFromStalledPath     (0033BD70)
            |         -> SamplePointAlongCurrentPath (003347C0)
            -> FinalizeHeadingState              (0033BFB0)
                 -> TestForwardStepClearance
```

**Two solver variants, chosen by unit class**, and only the default one carries avoidance and
recovery — `SolveClassMode2Step` computes a step distance and clamps the turn, and stops there.

### The turn limiter, and the stop-and-turn behaviour

`BattleLocomotion_ApplyHeadingTurnLimiter` (`003364D0`, 564 B) compares against exactly three
floating-point constants, and all three are **angles in radians**:

| constant | radians | degrees |
|---|---:|---:|
| `0.785398` | π/4 | **45°** |
| `2.094395` | 2π/3 | **120°** |
| `0.349066` | π/9 | **20°** |

They form **one hysteresis loop**, not three independent clamps — **45°** starts a turn, **120°**
gates the faster of two turn rates, **20°** releases it. The body is read in full in section 9,
which supersedes this paragraph.

*(An earlier revision of this section said the bands were unestablished — true when written — and
also attributed the stop-and-pivot to `ApplyStopAndTurn` / `ApplySimpleHeadingLimit`. **That
attribution was ~~wrong~~ not wrong for `ApplyStopAndTurn`**: ~~neither is called from anywhere inside this family. The behaviour comes from~~ both are modes 3 and 5 of the family's own steering dispatcher, and the stop-and-pivot also comes from
the limiter's own 45° deadband. See section 9.)* *(corrected 2026-10-02, OPUS: `0033BED0` calls `00339F00` at `0033BF8D`, which calls `ApplyStopAndTurn` `0033CE60` at `0033A06E`; `0033CE7B` zeroes the speed `+0xB0`; section 6, AM-7)*

### Two independent recovery layers

The default solver runs **both** every step, and they are structurally different:

**Detour recovery** — `UpdateDetourRecoveryState` → `TryChooseReachableRandomDetour` /
`ResetAvoidanceStateRandomized`. Both callees are **randomised**, so a blocked unit picks a detour it
did not pick last time. Its one recovered constant is an `addss` of **5** (`0033C956`, the float `5.0` at `009146E4`; `_index/candidates/dd-data-5-0930/mv_loco_checks.py` L1).

**Stall recovery** — `UpdateStallRecoveryState` → `ComputeRemainingPathDistance` /
`TryRecoverFromStalledPath` → `SamplePointAlongCurrentPath`. This one is **measured, not random**: it
compares remaining path distance ~~, decrements by **0.01**, adds **1.5**,~~ with the stored one — a drop of more than **0.01** re-stores it and zeroes the counter, a rise past it **+ 1.5** re-stores it, anything else counts up *(corrected 2026-10-02, OPUS: `0033C2B7`–`0033C2C9`, `0033C2CF`–`0033C2DC`, `0033C2E3`–`0033C2ED`; AM-4)* — and tests a counter against
**60**.

**60 is one second at 60 fps.** A unit that has not made progress for about a second is treated as
stalled — which matches the roughly one-second pause before a stuck unit visibly tries something
else.

### Avoidance is pairwise and predictive

`ResolveTargetSpacingAndAvoidance` (`00338140`) is where units are kept apart. It calls:

- `CheckActorPairClearance` (`0033D660`) — pairwise separation; constants `×0.5` and `÷3` (`0033D747` multiplies by
  `0.5` at `01CEBB70`, `0033D751` divides by `3.0` at `008F311C`; `_index/candidates/dd-data-5-0930/mv_loco_checks.py` L2)
- `TestForwardStepClearance` (`00335B60`) → `QueryDynamicActorObstruction` (`003357B0`) — tests the
  step **before** taking it, against *dynamic* (moving) actors
- `TryStartRandomizedAvoidanceManeuver` (`003343D0`) — when the forward step is blocked

So obstruction is checked against other **moving units** each step, not against static geometry
alone, and the response is randomised.

### Step distance

`ComputeStepDistance` (`00339BF0`) is a **quadratic arrival curve**: the step is `rem² × speedB`,
where `rem` is the distance still to cover beyond the stop radius, divided by a per-situation factor
(`÷7`, `÷5`, `÷3`, `÷1.5` or `×0.25`). A final `×0.99` guard stops a unit ever stepping past its
target. Read in full in section 10.

## 3. Key addresses

| Address | Size | Role |
|---|---:|---|
| `00325BB0` | 465 B | `BattleUnit_UpdateCombatNavigationStep` — entry, from CombatAction |
| `00336CE0` | 342 B | `SolveAndPublishNextStep` — top of the family |
| `00336710` | 965 B | `BuildSolverContext` |
| `0033BED0` | 213 B | `SolveDefaultStep` — the full pipeline |
| `003394A0` | 394 B | `SolveClassMode2Step` — reduced pipeline for another class |
| `003364D0` | 564 B | `ApplyHeadingTurnLimiter` — the 45° / 120° / 20° thresholds |
| `0033CE60` | 136 B | `ApplyStopAndTurn` |
| `0033CDE0` | 124 B | `ApplySimpleHeadingLimit` |
| `00338140` | 839 B | `ResolveTargetSpacingAndAvoidance` |
| `0033D660` | 548 B | `CheckActorPairClearance` |
| `00335B60` | 748 B | `TestForwardStepClearance` |
| `003357B0` | 943 B | `QueryDynamicActorObstruction` |
| `003343D0` | 955 B | `TryStartRandomizedAvoidanceManeuver` |
| `0033C870` | 319 B | `UpdateDetourRecoveryState` |
| `00334E00` | 882 B | `TryChooseReachableRandomDetour` |
| `0033E1F0` | 278 B | `ResetAvoidanceStateRandomized` |
| `0033C200` | 267 B | `UpdateStallRecoveryState` — the 60-frame test |
| `0033BD70` | 351 B | `TryRecoverFromStalledPath` |
| `00334950` | 287 B | `ComputeRemainingPathDistance` |
| `003347C0` | 397 B | `SamplePointAlongCurrentPath` |
| `00339BF0` | 503 B | `ComputeStepDistance` |
| `0033BFB0` | 590 B | `FinalizeHeadingState` |
| `0033A570` | 432 B | `ResolveDefaultHeadingConstraint` |
| `0033A120` | 188 B | `IsApproachConstraintActive` |
| `00319110` | 40 B | `SetApproachAndReferenceTargets` |
| `003291B0` | 90 B | `ResetPathAndSetTargets` |
| `00312730` | 965 B | `DecodeOrderGoal` |

### The `00336CE0` exclusive subtree — all 19 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the solver **19 frontier functions**. Twelve were already named
in the tree above; the other seven slot in as follows — `00339F00` and `0033C310` were missing from
that tree entirely (`edges.tsv`: `0033BED0 → 00339F00`, `0033C200 → 0033C310`). Every member body
was disassembled from the shipping image within its declared extent (2026-09-14); the interior
column cites one instruction inside each body.

| cluster | members | role |
|---|---|---|
| solver top (`0033BED0`'s own callees) | `00336040` (461 B — `BattleUnit_GetPartyLeader` + `Vector3_ComputeXZDistance` ×2 + `BattleRuntime_GetModeDependentDistanceThreshold` ×2: builds the leader-distance context), `00339F00` (531 B — the step-application arm: `0020xxxx` vector pack, `004687F0`/`00468700`, then calls `ApplyStopAndTurn` and `ApplySimpleHeadingLimit`), `00469A50` (160 B — the publish tail: `00320A30` ×2 + `0046AB10`) | the three stages the default solver runs around the spacing/recovery blocks |
| avoidance | `00338140` `ResolveTargetSpacingAndAvoidance` (839 B), `003341A0` (125 B — gates on `[[unit+0x100]+0x38] & 1` then `BattleTarget_IsRelationshipClass0Or1`: the per-pair eligibility predicate), `00337A50` (442 B — `BattleUnit_ResolveByFocusHandle` + `002F8E70` ×2 + `BattleAction_ComputeChargeProgressStep` ×3: spacing against the focus target), `003343D0` (955 B `TryStartRandomizedAvoidanceManeuver`), `00334C30` (87 B — `Vector3_ComputeXZDistance` on `unit+0x40`: distance to the candidate detour point) | pairwise spacing plus the randomized escape |
| detour recovery | `0033C870` `UpdateDetourRecoveryState` (319 B), `00334E00` `TryChooseReachableRandomDetour` (882 B — calls `003377C0`) | the randomized detour pick |
| stall recovery | `0033C200` `UpdateStallRecoveryState` (267 B — the 60-frame test), `0033C310` (1,362 B — **the largest member**: `BattleUnit_GetBySlotIndex`, `ComputeRemainingPathDistance`, `0031ABE0`, `002EA7F0`, `00391D10` — the path-stall walker the §2 tree did not list), `0033BD70` `TryRecoverFromStalledPath` (351 B), `003347C0` `SamplePointAlongCurrentPath` (397 B) | the measured, non-random recovery layer |
| heading primitives | `0033BFB0` `FinalizeHeadingState` (590 B), `0033A570` `ResolveDefaultHeadingConstraint` (432 B — `Vector3_ComputeXZDistance`), `0033CDE0` `ApplySimpleHeadingLimit` (124 B), `0033CE60` `ApplyStopAndTurn` (136 B) — both call `00334120` | `Angle_ApproachWrappedRadians` (`00334120`) sits under both clamps |

Interior citations — verified inside each declared extent (`interior_cite.py scan`; no boundary
crossings):

| body | interior | what is there |
|---|---|---|
| `003341A0` | `003341D6` | `call 0030BCB0` — `BattleTarget_IsRelationshipClass0Or1` |
| `003343D0` | `003343FF` | `call 003588B0` — handle→registry resolve before the maneuver |
| `003347C0` | `003348D0` | `call 004686D0` — `Vector3_ComputeXZDistance` along the path |
| `00334C30` | `00334C40` | `call 004686D0` — the candidate-point distance |
| `00334E00` | `00334E65` | `call 003377C0` — reachability test for the random detour |
| `00336040` | `003360B4` | `call 003272A0` — `BattleUnit_GetPartyLeader` |
| `00337A50` | `00337A88` | `call 002F8E70` — the target query under the focus handle |
| `00338140` | `0033817F` | `call 00236820` — `BattleUnit_GetBySlotIndex`, the pairwise scan |
| `00339F00` | `00339F3E` | `call 00203170` — first of the `0020xxxx` vector ops |
| `0033A570` | `0033A5B0` | `call 004686D0` — XZ distance under the heading constraint |
| `0033BD70` | `0033BDB2` | `call 002F8E70` — target query inside the stall recovery |
| `0033BED0` | `0033BEE4` | `call 00336040` — the leader-distance context build |
| `0033BFB0` | `0033BFEF` | `call 00203080` — vector pack inside heading finalize |
| `0033C200` | `0033C229` | `call 002F8E70` — the stall state's target query |
| `0033C310` | `0033C37E` | `call 002646C0` — the unit query at the walker's head |
| `0033C870` | `0033C8A8` | `call 00334E00` — the random detour pick |
| `0033CDE0` | `0033CE3C` | `call 00334120` — `Angle_ApproachWrappedRadians` under the simple clamp |
| `0033CE60` | `0033CE9D` | `call 00334120` — same helper under stop-and-turn |
| `00469A50` | `00469A81` | `call 00320A30` — the publish tail's first store |

## 4. Data structures and formulas

```
turn thresholds (radians)      pi/4 = 0.785398   45 deg
                               2pi/3 = 2.094395  120 deg
                               pi/9 = 0.349066   20 deg

stall recovery                 counter tested against 60      (= 1.0 s at 60 fps)
                               distance stepped by -0.01, +1.5   <- corrected 2026-10-02, OPUS - thresholds, not steps: a drop below old - 0.01 or a rise above old + 1.5 re-stores the distance (0033C2B7-0033C2DC)
detour recovery                +5
pair clearance                 x0.5, /3
step distance                  +0.5, /7, x0.25, /5, /1.5, /3, x0.99
```

## 5. Modding notes

- **The three angles are the character of the movement.** `π/4`, `2π/3` and `π/9` are plain floats in
  `.rdata`; changing them changes how sharply units turn and when they stop to pivot.
- **The 60 in stall recovery is a frame count**, not a distance. Raising it makes stuck units persist
  longer before improvising.
- **Recovery is randomised on purpose.** Detour selection and avoidance reset both draw random
  values, so identical situations do not produce identical stuck loops.
- **Only one of the two solver variants has avoidance.** `SolveClassMode2Step` clamps a turn and
  computes a distance and nothing more — a unit on that path will not sidestep.
- **Combat drives movement, not the reverse.** Every entry into this family comes from CombatAction.
- **XIIOnline:** the recovery layers consume RNG, so two clients diverge on avoidance and detours
  unless the stream is shared — the same conclusion the RNG document reaches for other systems. The
  positions are the sync target, not the steering decisions.

## 6. What is not known

- [x] ~~Which angular band selects which behaviour.~~ **ANSWERED 2026-09-02** — they are a
      hysteresis loop: **45°** is the deadband that starts a turn, **120°** gates the fast rate,
      **20°** releases it. Two rates at `st[0xEC]` / `st[0xF0]`. Section 9. **AM-1.**
- [x] ~~What `ApplyStopAndTurn` and `ApplySimpleHeadingLimit` do. Neither is called from inside this
      family; section 2's association of them with the stop-and-pivot behaviour was wrong.~~
      **AM-7 ANSWERED 2026-09-12 (FABLE): two of the six steering modes, and they are inside the family
      after all.** Their caller `00339F00` is called only by `BattleLocomotion_SolveDefaultStep`
      (`0033BF8D`). It projects the step into the solver context (`00339F27`–`0033A031`), then
      dispatches on **the low five bits of the actor flag word at ctx `+0x100`** — mode 1 and 4 →
      `0033CEF0`, 2 → `0033D200`, **3 → `ApplyStopAndTurn`**, **5 → `ApplySimpleHeadingLimit`**, 6 →
      `0033BAA0` (`0033A039`–`0033A0A6`) — and afterwards treats **bits 5–14 of the same word as a
      countdown**: cleared when the speed `ctx+0xB0` exceeds `004686D0`'s threshold, otherwise
      decremented by one each step (`0033A0B8`–`0033A0E8`). **`ApplyStopAndTurn` (`0033CE60`)** zeroes
      the speed `+0xB0`, turns the heading `st+0xE0` toward the desired heading with the *slow* rate
      `st+0xEC` through `Angle_ApproachWrappedRadians` (`00334120`), stores the desired heading at
      `+0xB4` and the limited one at `+0xBC`, arms the countdown at **10** when none is running
      (`0033CEBB`–`0033CEC5`, `(0x140 >> 5)`), and clears it once the heading has arrived
      (`0033CEC7`–`0033CED2`) — a stop-in-place pivot. **`ApplySimpleHeadingLimit` (`0033CDE0`)** keeps
      the speed and turns at `st+0xE4` while `+0xB0` is positive and above `st+0x104`, else at
      `st+0xE8`, storing the same two headings (`0033CDE6`–`0033CE4E`) — a turn-while-moving limiter.
      *Not read:* modes 1 / 4, 2 and 6's bodies, and what authors the mode bits *(answered: see the SD-183 answer in the next box — the flag word, the three bodies and the mode writers; 2026-10-02, OPUS)*. **AM-7.**
- [x] **What the other steering modes do, and who sets the mode.** The dispatcher sends modes 1 and 4 to `0033CEF0`,
      2 to `0033D200` and 6 to `0033BAA0` (`0033A039`–`0033A0A6`, `_index/candidates/dd-data-5-0930/mv_loco_checks.py` L3). The bodies have only
      census-level descriptions on the field-map and transform-primitive pages, and no writer of the low five bits
      of the flag word at the solver context's `+0x100` is traced. **SD-183** (SWE2-DATA, 2026-09-30).
      *(Answered 2026-09-30 (SWE2-ORACLE `8acf79ac7`); register row SD-183, record [`sd183-steering-modes-0930`](../../_index/candidates/sd183-steering-modes-0930/README.md): the flag word is `BattleUnit +0x80` - bits 0-4 the mode, bits 5-14 a countdown, bit 15 mode 6's orbit direction - and the dispatcher runs only while the countdown is non-zero, so a mode is a steering override with a lifetime. Modes 1 and 4 share `0033CEF0` (turn toward the goal, move inside a cone) and nothing tells them apart at run time; 2 turns or gives way to the turning circle; 6 orbits a point. The mode writers are the avoidance search's setter (modes 1-5), `003343D0` (mode 6) and `0033E1F0` (mode 0); the record's 'What changes on the page' lists the section-6 amendments.)*
- [x] ~~What `st[0x170] & 0x1C == 0x1C` tests — the extra condition gating the fast turn rate.~~
      **AM-8 ANSWERED by reference 2026-09-12 (FABLE):** `st` is the unit's movement block at `+0x80`,
      so `st[0x170]` is the unit's **`locomotionFlags` `+0x1F0`** ([the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)), and `0x1C` is its
      bits **2 | 3 | 4** — bit 2 = the model's `@FCP` section-9 **slot 41 dword is non-zero** (`00239F73`,
      authored per model, non-zero in 360 of 723 files, [the FCP block](../../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md)), bit 3 = **unit flag bit 23**
      (`00325CC9`), bit 4 = **the unit is executing a non-Attack action** — `+0x714 ≤ 0x21E` and
      `≠ 0x96` (`00325CF4`); bits 3 and 4 are recomputed every `BattleUnit_UpdateCombatNavigationStep`
      (`00325C72`–`00325CFD`). So the fast turn rate latches beyond 120° only for a unit whose model
      authors slot 41, whose flag bit 23 is up, and which is mid-cast of something other than Attack.
      **AM-8.**
- [x] ~~What `ComputeStepDistance`'s seven constants select between.~~ **ANSWERED 2026-09-02** —
      they are **one quadratic arrival curve** (`rem² × speedB`) with a per-situation divisor, plus a
      `×0.99` overshoot guard. Section 10. **AM-2.**
- [x] What the fixed-speed escape identifies: `record[5] == 0` **and** a literal `0x4022` at
      *(2026-09-08: `0x4022` is now placed — it is an **order opcode** with its own decode case at `0031289E`, not a magic number.)*
      `unit + 0x714`. One unit kind moves at a fixed speed with no arrival curve. **AM-9.**
      *(Narrowed 2026-09-12, FABLE: the kind is 0, a party-kind unit — `0x4022`'s own decode case admits only
      those — and `0x4022` is the order under which `004697C0` posts "Action interrupted … cancels" (message 6,
      [the battle message table](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)) for a party unit; but **no issuer was found**: `0x4022` never occurs in the 50,050 shipped
      enemy order records, in any of the 1,114 script images' constant pools, or in the battle tables as an
      order, and all twelve `0x4022` immediates in the image are compares — the id reaches `+0x714` through a
      computed value or a table this search did not cover.)*
      *(Issuer found 2026-09-12, FABLE: the static re-plan set `01EEC3C0` in `.data` holds one record naming `0x4022`,
      installed at a party-kind unit's `+0x6E8` by the combat-stance enter / exit, the engaged-action setup, terminal
      recovery and the `resetemergency` verbs — [the gambit-set page](../../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md) §7.)*
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (AM-9): **a party member regrouping after a
      combat-state reset while force fight mode is on.*** The escape (`00339C18`–`00339C64`) has three conditions. The unit is
      party kind (`record[5] == 0`). `thunk_00253B90()` returns 0; that predicate is `flag 01E0C2B8 == 0` and is true when force
      fight mode is **off** ([force fight mode](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md), "mind the
      polarity"), so 0 means the mode is **on**. And the unit's current order at `+0x714` is `0x4022`, the regroup follow that
      every combat-state reset installs (the gambit-set page §7). When all three hold, the function returns **speed B**
      (`st[0xFC]`) immediately. It skips both speed-flag branches and the quadratic arrival curve below (`rem² × speedB`,
      clamped between speed A and speed B). **So in force fight mode a regrouping party member runs at full speed B the whole
      way to its place, instead of easing in.** The stop itself is still the order's mode-dependent stop distance
      (`0031289E`–`0031290E`). Why force fight mode should skip the ease-in is design intent and is not asserted.
- [x] ~~What `st[0x174]`, `st[0x40]` and `ctx[0xD0] & 1` select — the three conditions choosing the
      divisor regime.~~ **AM-10 ANSWERED 2026-09-12 (FABLE).** `st` is the unit's movement block at
      `+0x80`. **`st[0x174]`** is the unit's **`placementMode` `+0x1F4`** ([the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)): 1 by
      default, 2 for an enemy-table record, 3 with the probe gate's bit 3 — so `≥ 2` is *an
      enemy-table unit*, and the `÷ 7` gentlest approach is theirs. **`st[0x40]`** is the unit's
      **`+0xC0` approach mode**, three writers image-wide: the movement-order handler zeroes it for
      every movement order (`002FDB14`) and sets **2** for order **`0x414E`** alone — approach the
      focus target's presentation-adjusted position, storing the `+0x710` handle at `+0x150`
      (`002FDB5B`–`002FDB68`) — and the standard action commit sets **1** (`00304BEC`). So `== 1` is
      *closing on an action target* (the arrival test against the stop radius) and `== 2` the
      `0x414E` approach with the class-3 clearance margin. **`ctx[0xD0]` bit 0** is set by
      `BattleLocomotion_BuildSolverContext` when a party leader exists, the unit's order is `0x4124`
      — or `0x4022` outside force-fight mode — and `Navigation_CheckDirectRouteAcrossRegionsXZ(ctx,
      &ctx+0x60, 1)` does not return 1 (`003368BD`–`00336932`; cleared first at `003368B6`): the
      **party-follow regime without a direct route**, which is why that branch takes its distance
      from a different source and divides by 4 or 5 by force-fight state. **AM-10.**
- [x] ~~What unit class chooses `SolveClassMode2Step` over `SolveDefaultStep`, and why that class
      needs no avoidance.~~ **AM-3 ANSWERED 2026-09-12 (FABLE): an authored boss motion mode on the
      `.ard` class row, and the class is the Sephira.** `BattleLocomotion_SolveAndPublishNextStep`
      routes on **bits 1–3 of byte `+0x18` of the unit's `.ard` slot-0 class row** (unit `+0xE68`,
      [the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)): value **1 or 3 → no solve at all** (return, `00336D33`–`00336E1D`), value **2 →
      `SolveClassMode2Step`** (`00336D61`–`00336D6B`), anything else → `SolveDefaultStep`
      (`00336D72`). Censused over the 954 distinct class rows the 166 shipped areas spawn, the field
      is 0 on 944 and non-zero on exactly five boss rows: **1 Rook, 2 Sephira, 3 The Undying, 4 Doctor
      Cid, 5 Vayne Novus** (bank-8 names). So the reduced solver serves one class only — the Sephira,
      the orbs that circle their master — which is *why* it needs no avoidance or stall recovery: their
      motion is a scripted orbit, not pathing (the "why" is read from the class, not from the bytes);
      the Rook and The Undying skip the solver altogether, and Cid and Vayne take the default step.
      **AM-3.**
- [x] ~~Whether the `60` counter is frames or ticks. One second at 60 fps is the natural reading and
      matches observed behaviour, but the counter's increment site is unread.~~ **AM-4 ANSWERED
      2026-09-12 (FABLE): solver frames — the updater increments it itself.**
      `UpdateStallRecoveryState` (`0033C200`, called once per `SolveDefaultStep`, `0033BF3E`) runs only
      for a unit whose stats `002F8E90` classes as 1 / 2 / 4 (`0033C229`–`0033C230`) under order
      `0x4124` or `0x4022` (`0033C236`–`0033C256`); it first tries `TryRecoverFromStalledPath`, then
      `0033C310` (returning 1 ends it), and, when the follow target `ctx+0xE8` is absent or
      `00265830(target) == 0`, compares `ComputeRemainingPathDistance` with the byte-record `fl`
      (`ctx+0x100`) float `+0x10`: dropped by more than **0.01** (`008F30E4`) → store it and zero the
      counter `fl+0x14` (`0033C2C4`–`0033C2C9`); risen above the old value **+ 1.5** (`00901B3C`) →
      store it; otherwise **`fl+0x14 += 1`, capped at 60** (`0033C2E3`–`0033C2ED`). The counter
      therefore counts consecutive stall updates — one per locomotion solve of that unit — not clock
      ticks; it is a second only because the unit solves every frame at 60 fps. **AM-4.**
- [x] What `DecodeOrderGoal` (965 B) decodes, and the order format it reads. **AM-5 — ADVANCED
      2026-09-08.** Format: `order+0x00` u16 opcode, `order+0x02` s16 parameter. The opcode space is
      `0x4000`-based: **32 opcodes `4000–401F` share one case** (index = opcode − 0x3FFF), **16
      opcodes `4026–4035` share one path** (~~one handler `002367A0`~~ *corrected 2026-09-13 (FABLE): `002367A0` is `BattleUnit_FindByDefinitionSelector`, called with opcode − 0x4026 at `00312976`; the unit it returns takes the shared go-to-unit path `00312918` — [the identity resolvers](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md)*), four specials
      `4020`/`4022`/`4023`/`4024`, **two holes `4021` and `4025` that reject**, and a separate chain
      from `0x4124`. **What each case does is unread — `DE-1`.**
      > **DE-3 answered 2026-09-12 (FABLE): the higher band is five opcodes** (`0031297D`–`003129A3`;
      > anything else above `0x4035` rejects), each a *goal source*, with the s16 parameter and the larger of
      > the two `00265090` floats (`xmm6`) feeding the stop distance:
      >
      > | opcode | goal | stop distance |
      > |---|---|---|
      > | `0x4124` | the unit's **own** `+0x120` vector (aux `+0x130`), allowed only when the handle at unit `+0x24` resolves (`BattleUnit_ResolveByFocusHandle`) to **another** unit (`00312A91`–`00312ACB`) | own `+0x154` |
      > | `0x4125` | the 32-family sampler `00312DF0(unit + 0xD0, −1, 20, unit, aux)` — ~~reference position **20**~~ around the unit's own `+0xD0` within **±20**, the parameter *(corrected 2026-10-02, OPUS: `00312A50` `lea rcx, [rdi+0xD0]` is the reference, `00312A57` `mov r8d, 0x14` the third argument)* (`00312A50`–`00312A8F`) | `xmm6` |
      > | `0x414A` | the unit the `+0x24` handle names, through the **`0x4023` body** (`00312A43` → `00312918`): its `+0xD0` position, not self | `BattleUnit_GetNavigationClearanceRadius(target)` + `xmm6` + parameter |
      > | `0x414E` | the `+0x710` focus target's `Actor_GetPresentationAdjustedPosition` (`003129F3`–`00312A3E`) | 0 |
      > | `0x4165` | **`Loot_FindNearestActivePickupPosition(unit, out)`** (`00319850`, `003129A9`–`003129EE`) — the nearest world pickup, [the loot page](../../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md); the periodic maintenance runs the pickup overlap for a unit whose current order is `0x4165` (`003110E8`–`003110F4`) | `xmm6` + one constant − another |
      >
      > The low specials read the same way: `0x4023` = the `+0x710` focus target, `0x4024` = the party leader
      > (`003272A0`), both through the `0x4023` body; `0x4022` (`0031289E`–`0031290E`) = a **party-kind** unit
      > (`[+0x698]+5 == 0`) whose `+0x24` handle resolves, goal its own `+0x120`, aux the resolved unit's `+0xD0`,
      > stop `00309B10(unit)` + `BattleRuntime_GetModeDependentDistanceThreshold()`. **The handler behind these
      > ids is `caseD_4000` (`002FDA60`, [the handler-table page](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md))**, read whole: a phase byte at unit `+0x6B4` — 0: decode
      > the goal, store the distance at ctx `+0xD0`, `BattleLocomotion_ResetPathAndSetTargets`, phase 1; 1:
      > for `0x4022`, `0x4024`, `0x4026`–`0x4035`, `0x4124`, `0x414A`, `0x414E`, `0x4165` re-decode each tick
      > and `BattleLocomotion_SetApproachAndReferenceTargets` (`002FDB25`–`002FDBB6`; `0x414E` also sets ctx
      > `+0x40 = 2`, `+0x150 =` the focus handle); then `BattleLocomotion_IsApproachConstraintActive` ends
      > the order (phase 2, returns 1), otherwise `0x4022` / `0x4124` set ctx `+0x170 |= 0x100` and
      > `BattleUnit_UpdateCombatNavigationStep` runs (`002FDBC1`–`002FDBF4`).
      >
      > **DE-2 answered the same day:** `0x4021` is not a retired number — it is **the engine's own default
      > order**, the static record `{0x4021, 0, flags 0x2000}` at `01EEC298` that `BattleUnit_SelectAndCommitNextAction`
      > commits when nothing else was chosen (`00305C7E`–`00305C9B`), the third most-used opcode in the shipped
      > enemy order sets (3,018 of 50,050 records), and the one `PartyFollow_SolveFormation` (`00338E10`) and
      > `BattleLocomotion_QueryDynamicActorObstruction` (`00335A81`) test a unit's `+0x714` for — an idle order
      > with no goal, so its "hole" in this decoder is by design. `0x4025` never occurs in the shipped sets and
      > has no handler slot: the one true hole. (The sibling static record at `01EEC2B0` is `{150 Attack, 0,
      > 0x2000}`, the engage auto-attack `BattleUnit_TryCommitEngageAutoAttack` commits at `003130CB`.)
      **ANSWERED 2026-09-18 (FABLE) — the last unread case is read, and every opcode now has one.** The low-band dispatch is two image-relative tables (index bytes at `00312B10`, case RVAs at `00312AF8`, `003127AA`–`003127C5`) and they send `0x4020` alone to `003127D7`: the arm requires the battle-state record at unit `+0x698` to carry kind byte **1** at `+5` (`003127E7`; the page's `0x4022` reading tests the same byte for 0, the party kind), takes the **SpawnRecord** at unit `+0x6A0` and points at its `+0x50` — the *live persisted world position* on [the spawn page](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — keeps the `s16` parameter in `r8d`, and jumps to the shared sampler tail `00312A5D`, which calls `00312DF0(reference, −1, parameter, unit, out)` and, on success, copies the sampled point into the goal and stores the radius (`00312A5D`–`00312A8F`). So **`0x4020` is “wander within ±N of your own spawn position”**, the non-party sibling of the `0x4000`–`0x401F` family (which samples around a POSENT reference by index) and of `0x4125` (which samples around ~~reference 20~~ the unit's own `+0xD0` within ±20 *(corrected 2026-10-02, OPUS: `00312A50`–`00312A57`)*). With that, every opcode's case is read: `0x4000`–`0x401F` and `0x4026`–`0x4035` under `DE-1`, the index under `DE-4`, `0x4021` under `DE-2` (the engine's default order), `0x4022` / `0x4023` / `0x4024` and the `0x4124`+ band under `DE-3` above, `0x4025` the one true hole, and `0x4020` here. Static: the two tables and the arm.
- [x] ~~Which RNG stream the randomised recovery draws from.~~ **AM-6 ANSWERED 2026-09-08 — the
      process-global CRT `rand`.** All three randomised functions call IAT slot `008C3098`, which
      the import table resolves to `api-ms-win-crt-utility-l1-1-0.dll!rand`; `ResetAvoidanceStateRandomized`
      calls nothing else at all. **Not the shared gameplay LCG and not either Mersenne Twister**, so
      the draw is shared with every other `rand()` caller in the process and **a detour choice is not
      reproducible across machines.**

## 7. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The 26-function family and its sizes | `functions.tsv`, name prefix `BattleLocomotion_*` | 1 |
| The call structure | intra-family edges from `edges.tsv`, all 25 pairs listed in section 2 | 1 |
| Entry is from CombatAction | callers of `BattleUnit_UpdateCombatNavigationStep`: `caseD_4000`, `BattleUnit_AdvanceTargetedMovementOrder`, `BattleUnit_AdvanceStandardActionState`, `FUN_003082F0` — all CombatAction | 1 |
| Turn thresholds are 45° / 120° / 20° | the three `comiss` constants in `003364D0` decoded from `.rdata` and converted: `0.785398`→45.0000°, `2.094395`→120.0003°, `0.349066`→20.0000° | 1 |
| Stall recovery tests a counter against 60 | `cmp` against `60` in `0033C200`, with `subss 0.01` / `addss 1.5` | 1 |
| Recovery is randomised | `TryChooseReachableRandomDetour` and `ResetAvoidanceStateRandomized` are the two callees of `UpdateDetourRecoveryState` | 2 |
| Obstruction is tested against dynamic actors before stepping | `TestForwardStepClearance` → `QueryDynamicActorObstruction`, called from `ResolveTargetSpacingAndAvoidance` | 1 |
| Only the default solver has avoidance | `SolveClassMode2Step` calls exactly `ComputeStepDistance` and `ApplyHeadingTurnLimiter` | 1 |

**Scope honesty:** constants are read; ~~the branches that select between them mostly are not. Every~~
~~"which threshold does what" question in section 6 is open for that reason, and no behaviour is~~
~~assigned to a specific angle here.~~ *(Corrected 2026-09-30, SWE2-DATA: the threshold questions of section 6 are
answered. The three angles are one hysteresis loop (45° starts a turn, 120° gates the fast rate, 20° releases it;
AM-1, §9), and the arrival curve is read (AM-2, §10). The open branches are the steering modes of `SD-183`.)*

## 8. Related

- [`../heading-speed-to-position-delta.md`](../heading-speed-to-position-delta.md) — the layer *below* this one: turning a chosen heading and speed into a position delta
- [`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md) — the streams the randomised recovery draws from
- [`../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) — the kind byte at record `+5`. **`BattleLocomotion_DecodeOrderGoal` tests it**, at `003127E7`:

  ```asm
  003127D7  mov  rax, qword ptr [rdi + 0x698]   ; the record view
  003127DE  test rax, rax
  003127E1  je   0x312ad4                       ; null -> bail
  003127E7  cmp  byte ptr [rax + 5], 1          ; the kind byte, against 1
  003127EB  jne  0x312ad4
  ```

  **Citation corrected 2026-09-03.** This line previously read *"is one of the 82 functions testing
  that byte"* and cited the neighbour as its support. The neighbour states a **cardinality** — "104
  sites across 82 functions" — and never enumerates the members, so it cannot support a
  **membership** claim about any particular function. The claim is true, but it needed the site
  above, not a count. Found by the cross-document citation checker; the membership was then
  established by rebuilding that document's census from its own stated criterion and confirming
  `00312730` in the result, then reading the site by hand.

## 9. Falsification pass 2026-09-02 — AM-1: the three angles are a hysteresis loop

**Attack chosen.** Section 2 published three angular constants and explicitly refused to say which
did what. That refusal is the thing to test: either the bands are genuinely unreadable without more
work, or one disassembly settles them. **One disassembly settles them**, and the answer is more
interesting than three independent thresholds.

### `ApplyHeadingTurnLimiter`, read in full (564 B)

```c
float ApplyHeadingTurnLimiter(ctx, float desired)
{
    st    = ctx->[0x108];                       /* motion state */
    fl    = ctx->[0x100];                       /* flag block   */
    cur   = st->[0xE0];                         /* current heading */
    a     = fabs(Angle_NormalizeRadiansPi(cur - desired));

    if (a > 45°)            fl[0x38] |= 8;      /* raise "turning" */
    if (!(fl[0x38] & 8))    return cur;         /* not turning: heading unchanged */

    if (a > 120°) {
        if ((st->[0x170] & 0x1C) == 0x1C)  fl[0x3C] |= 1;      /* latch FAST rate */
        rate = (fl[0x3C] & 1) ? st->[0xF0] : st->[0xEC];
    } else if (a > 20°) {
        rate = (fl[0x3C] & 1) ? st->[0xF0] : st->[0xEC];       /* keep whatever is latched */
    } else {
        fl[0x3C] &= ~1;                                        /* release the latch */
        rate = st->[0xEC];                                     /* always the SLOW rate */
    }

    d = Angle_NormalizeRadiansPi(desired - cur);   /* <- corrected 2026-10-02, OPUS - not on the latched path: above 120 deg with fl[0x21] & 6 set, 0033659D-0033661D step cur +/- rate with no wrap and no snap */
    new = (fabs(d) <= rate) ? desired                          /* close enough: snap */
                            : Angle_NormalizeRadiansPi(cur ± rate);

    /* record which way it turned */
    if (Angle_NormalizeRadiansPi(new - cur) > 0) { fl[0x21] &= ~4; fl[0x21] |= 2; }
    else                                          { fl[0x21] &= ~2; fl[0x21] |= 4; }

    if (new == desired) { fl[0x38] &= ~8; fl[0x3C] &= ~1; }    /* arrived: stop turning */
    return new;
}
```

### The three angles are one mechanism, not three

| angle | role |
|---:|---|
| **45°** | **deadband / entry.** A heading change of 45° or less **does not start a turn at all** — the function returns the current heading unchanged. |
| **120°** | **fast-rate gate.** Only beyond 120° can the faster of the two turn rates be latched, and only if `st[0x170] & 0x1C == 0x1C`. |
| **20°** | **release.** Once within 20° of the target the fast latch is cleared and the turn finishes at the slow rate. |

Entry at 45°, escalate past 120°, ease off inside 20°, stop on arrival — **a hysteresis loop with two
turn rates** (`st[0xEC]` slow, `st[0xF0]` fast), not three unrelated clamps.

### What a player sees, now explained

- **Big reversals snap round quickly, then visibly slow as they line up.** That is the 120° latch
  followed by the 20° release, not an animation blend.
- **Small course corrections produce no turn at all.** Under 45°, the unit keeps its facing and walks
  slightly off-axis — which is why units in battle so often appear to drift or strafe rather than
  aim exactly where they are going.
- **A turn, once started, continues until the heading matches**, because the "turning" flag is only
  cleared on arrival. The deadband applies to *starting* a turn, not to finishing one.

### Corrections to section 2

Section 2 called these "three thresholds, not one — so turning is not a single clamp but a banded
decision", which is right as far as it goes, and said *"which band selects which behaviour is not
established"*. It is now. Section 2's caution stands as written; this section supersedes its open
question.

One thing section 2 implied and should not have: it grouped `ApplyStopAndTurn` and
`ApplySimpleHeadingLimit` with the limiter as "the mechanism behind the stop-and-pivot". **Neither is
called by `ApplyHeadingTurnLimiter`~~, and neither is called from anywhere inside this family~~** — their
~~only callers are outside it~~ caller is the family's own steering dispatcher (`00339F00`) *(corrected 2026-10-02, OPUS: `0033BED0` → `00339F00` at `0033BF8D` → `0033CE60` at `0033A06E`; section 6, AM-7)*. The stop-and-pivot behaviour described above comes from
the limiter's own deadband, not from those two functions. ~~Their role is unread.~~ *(answered: see section 6, AM-7 — modes 3 and 5 of the dispatcher, `ApplyStopAndTurn` zeroing the speed; 2026-10-02, OPUS)* **AM-7.**

### A shared utility identified

`Angle_NormalizeRadiansPi` (`0033CB70`, 128 B) normalises an angle into ~~(−π, π] by repeated addition~~ [−π, π] by repeated addition of ±2π when it lies within ±4π, and beyond that by one truncating division with no loop, which can leave a result in (−2π, 2π) *(corrected 2026-10-02, OPUS: `0033CB73` / `0033CB84` against `[00D10B0C]` / `[00D10B20]` (±4π), loops `0033CBA0` / `0033CBC0`, division `0033CBCD`–`0033CBEF`)*
— and it has **25 call edges** across the image, so it is an engine-wide helper rather than a
locomotion detail.

## 10. Falsification pass 2026-09-02 (second) — AM-2: the arrival curve

**Attack chosen.** Section 2 listed `ComputeStepDistance`'s seven constants and said *"multiple
divisors imply several speed regimes selected by condition. **Not read** — listed so the numbers are
on record."* Numbers on record without their branches is exactly the state that produced a false
elemental-affinity reading elsewhere today. Read.

### `ComputeStepDistance`, read in full (503 B)

```c
float ComputeStepDistance(ctx)
{
    dist = Vector3_ComputeXZDistance(ctx + 0x30, target);   /* HORIZONTAL distance */
    st   = ctx->[0x108];

    /* fixed-speed escape for one specific unit kind + id */
    u = ctx->[0xF0];
    if (u && u->[0x698] && u->[0x698][5] == 0 && !thunk_00253B90()
        && *(u16 *)(u + 0x714) == 0x4022)      return st->[0xFC];

    if (st->[0x170] & 1)   return st->[0xF8];              /* speed A */
    if (st->[0x170] & 2)   return st->[0xFC];              /* speed B */

    if (st->[0x40] == 1 && u->[0x768] >= u->[0x76C] && dist > st->[0xD0])
                           return st->[0xFC];

    rem = dist - st->[0xD0];                               /* beyond the stop radius */
    if (st->[0x40] == 2) {
        ActorRuntime_GetClass3FloatPair(ctx->[0xE0], &a, &b);
        rem -= min(a, b) + 0.5;                            /* extra clearance margin */
    }
    rem = max(0, rem);

    if (st->[0x174] >= 2)            rem /= 7;
    else if (ctx->[0xD0] & 1)        rem  = thunk_00253B90() ? d2 * 0.25 : d2 / 5;
    else                             rem /= thunk_00253B90() ? 1.5 : 3;

    v     = rem * rem * st->[0xFC];                        /* QUADRATIC in remaining distance */
    speed = (st->[0xF8] > v) ? v : min(st->[0xFC], v);   /* <- corrected 2026-10-02, OPUS - (st->[0xF8] > v) ? st->[0xF8] : min(st->[0xFC], v): 00339DA8 loads A, 00339DBB ja keeps it, 00339DBD-00339DC0 min(B, v) */

    if (speed > dist)  speed = dist * 0.99;                /* never overshoot */
    return speed;
}
```

### Three findings, all player-visible

**1. The approach is a quadratic easing curve.** The step is `rem² × speedB` — proportional to the
**square** of the distance still to cover beyond the stop radius. A unit therefore decelerates
smoothly into its stopping point rather than travelling at full speed and halting. The seven
constants are not seven speeds; they are **one curve with a per-situation divisor** applied to `rem`
before squaring.

**2. `× 0.99` is an overshoot guard.** If the computed step exceeds the remaining distance, the unit
moves `dist × 0.99` instead — landing **1 % short every frame**. Units approach their target
asymptotically and never step past it, which is why a unit closing on a target visibly creeps the
last fraction rather than snapping onto it.

**3. Distance is horizontal only.** `Vector3_ComputeXZDistance` ignores Y, so height difference does
not count toward "am I close enough". A target directly above or below is treated as distance zero
by this solver.

### The divisor regimes

| condition | applied to `rem` |
|---|---|
| `st[0x174] >= 2` | `÷ 7` — gentlest approach |
| `ctx[0xD0] & 1` | uses a **different distance source**, then `× 0.25` or `÷ 5` |
| otherwise | `÷ 1.5` or `÷ 3` |

The `1.5` / `3` and `0.25` / `5` choices are both made by the **same predicate**, `00253B90` —
since identified as the **force fight mode** flag test (true when the mode is *off*). See
[`../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md`](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md).

### `00253B90` appears in a third documented system

The selector is reached as `thunk_FUN_00253B90` (`0030C0D0`, a 5-byte `jmp`). `00253B90` is already
recorded as the null predicate over `01E0C2B8` feeding the
[capability-inhibition policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)'s
bit 1, and as a gate in the
[action availability cascade](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md).
**Three independently documented systems now branch on it** — capability, action availability, and
movement speed — which raises it well above a local detail.

*(It is reached here through a `jmp` thunk, so an edge-list census of `00253B90`'s callers does not
show this one. That is the `E8`-versus-`E9` blind spot this database has already recorded twice,
appearing again.)*

### Also noted

The fixed-speed escape tests `record[5] == 0` — the
[battle record kind byte](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) — and
a literal id `0x4022` at `unit + 0x714`. One specific kind of unit moves at a fixed speed with no
arrival curve at all. **AM-9.**

## Cross-reference added 2026-09-02: how an order id becomes a goal

`00312730` `BattleLocomotion_DecodeOrderGoal` (965 B, owner Movement) sits upstream of the steering
described here. It takes an id from the **extended order space** — one of **two disjoint spaces that
share `BattleUnit+0x714`**, the other being ordinary target-carrying actions at `<= 0x21E` — bounds it
at ~~**`0x4000`-`0x4024`** (37 ids), and switches to~~ `0x4035` with five higher ids beside it, and switches its low band **`0x4000`-`0x4024`** (37 ids) to **six** goal-resolution bodies *(corrected 2026-10-02, OPUS: `00312780` `cmp ebx, 0x4035` / `ja` the ids `0x4124`, `0x4125`, `0x414A`, `0x414E`, `0x4165`; `0031278C` `cmp ebx, 0x4026` / `jae` the band `0x4026`–`0x4035`; `00312798`–`003127A1` the switch, `0x4025` rejected)*, 32 ids sharing the
first and `0x4021` deliberately resolving to none.

**These are orders, not player commands.** The distinction is made in `BattleUnit_CommitAction`
(`0030F760`) by `cmp di, 0x21E`, and it matters here: an order in this range carries **no target
buffer**, which is consistent with locomotion resolving its own goal rather than being handed one.

Three of the special cases read the actor's own record at `+0x698` -> `[+5]` (the kind byte) and
`+0x6A0` (the record base), corroborating
[the battle record kind byte](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)
from this subsystem.

The id space and its dispatch table are documented in
[the battle action handler table](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)
section 8. The two derivations meet exactly: Movement ~~bounds at `0x4024`~~ bounds its switch at `0x4024`, the decoder also taking `0x4026`–`0x4035` and five higher ids *(corrected 2026-10-02, OPUS: `0031279E` `cmp ecx, 0x24`; `00312780`, `0031278C`)*, and the action table's
first empty slot is `0x4025`.

## `AM-6` and `AM-5` — 2026-09-08

### ⚠ `AM-6` answered: the avoidance draws from the CRT `rand`, which nothing owns

All three randomised recovery functions call **one** external import, and it is the same one:

| function | size | external calls |
|---|---:|---|
| `TryStartRandomizedAvoidanceManeuver` `003343D0` | 955 B | IAT `008C3098` |
| `TryChooseReachableRandomDetour` `00334E00` | 882 B | IAT `008C3098` |
| `ResetAvoidanceStateRandomized` `0033E1F0` | 278 B | IAT `008C3098` — **its only call of any kind** |

**IAT slot `008C3098` resolves, in the import table, to
`api-ms-win-crt-utility-l1-1-0.dll!rand`.** Not the shared gameplay LCG at `00328370`, not either
Mersenne Twister — the **process-global C runtime `rand()`**, the stream
[`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md)
classifies as *external, external mixed authority*.

> **So a blocked unit's detour is not reproducible.** The CRT stream is shared with every other
> `rand()` caller in the process — 48 sites across 30 functions — so its state depends on everything
> else the frame happened to do. **Two machines running the same battle will pick different
> detours**, and no amount of synchronising the game's own RNG changes that.
>
> **This is engine evidence for a rule the project already holds on other grounds:** foe avoidance is
> *a local decision*, decided independently on each machine, with no counterpart to send or receive.
> **It could not be made deterministic without replacing the draw.**

`ResetAvoidanceStateRandomized` is the sharpest case — 278 bytes whose **only** call is `rand`.

### `AM-5` advanced: the order format and its opcode space

`DecodeOrderGoal` (`00312730`, 965 B) reads the order through `rdx`:

```
order + 0x00   u16   opcode
order + 0x02   s16   parameter          (carried into every handler as r8d)
```

and separately obtains two floats through `00265090`, keeping **the larger of the two**
(`movss xmm6, [rsp+0x70]` / `maxss xmm6, [rsp+0x78]`) — an extent or radius, not part of the order
record.

**The opcode space is a `0x4000`-based band**, dispatched in three tests
(`cmp 0x4035 / ja`, `cmp 0x4026 / jae`, `sub 0x4000 / cmp 0x24 / ja`) and one MSVC two-level jump
table — byte indices at `00312B10`, image-relative targets at `00312AF8`:

| opcodes | count | handling |
|---|---:|---|
| `0x4000` – `0x401F` | **32** | **one shared case** at `003127C7`: `index = opcode − 0x3FFF` (1…32), the `s16` parameter passed through, tail `00312A60` |
| `0x4020` | 1 | own case, `003127D7` |
| **`0x4021`** | 1 | **routed to the default/reject** at `00312AD4` — a hole inside the valid band |
| `0x4022` | 1 | own case, `0031289E` — **the opcode the fixed-speed escape tests for** |
| `0x4023` | 1 | own case, `00312804` |
| `0x4024` | 1 | own case, `00312913` |
| **`0x4025`** | 1 | fails `<= 0x24` and is below `0x4026` — **also rejected** |
| `0x4026` – `0x4035` | **16** | **one shared path**: the target is `BattleUnit_FindByDefinitionSelector(opcode − 0x4026)` (`00312970`–`00312976`), the unit whose stats record `+4` is 0…15, then the go-to-unit path `00312918` that `0x414A` also uses (~~"one shared handler `002367A0`"~~ corrected 2026-09-13) |
| `0x4124`, `0x4125`, `0x414A`, `0x414E`, `0x4165` | 5 | the higher band — five goal sources (DE-3, above); every other opcode above `0x4035` rejects |

> **Thirty-two of the thirty-seven low opcodes are one behaviour with an index.** The order language
> is far narrower than its opcode count suggests: a family of 32, a family of 16, four specials, and
> **two holes** — `0x4021` and `0x4025` — that sit inside the band and reject like an unknown opcode.
>
> **`0x4022` is now placed.** The document's open item on the fixed-speed escape describes it testing
> `record[5] == 0` and a literal `0x4022`; that literal is an **order opcode with its own decode
> case**, not a magic number.

**What is not read:** *(answered: see DE-1 to DE-4 below and the ANSWERED 2026-09-18 box — every case is read; 2026-10-02, OPUS)* what any of the six cases *does*. The format and the dispatch are established;
**the semantics of the 32-family, the 16-family and the four specials are not**, and neither is the
`0x4124`+ band. `AM-5` is advanced, not closed. `DE-1`.

### `DE-1` answered for 48 of the 53 opcodes — 2026-09-08

Two handler reads, as the question predicted.

#### The sixteen — `0x4026`–`0x4035` name a unit

The shared ~~handler is~~ path first calls `002367A0` and then goes to `00312918` *(corrected 2026-10-02, OPUS: `00312970`–`0031297B`; the 2026-09-13 correction)*, **`BattleUnit_FindByDefinitionSelector`** (126 B), already named in
the ledger, called with `opcode − 0x4026` (0…15).

> **Sixteen opcodes are sixteen ways of saying "that unit".** The order does not carry a unit handle;
> it carries an opcode whose *number* is the definition selector.

#### The thirty-two — `0x4000`–`0x401F` sample a random point nearby

The shared case reaches `00312DF0` (237 B) with the index and the order's `s16` parameter, and its
core is:

```asm
00312E40  mov  eax, edi          ; attempt counter
00312E42  inc  edi
00312E44  cmp  eax, 8
00312E47  jg   0x312ebc          ; give up after NINE attempts
00312E49  lea  ebx, [rbp*2 + 1]  ; rbp = the order's s16 parameter
00312E50  call 0x328370          ; RNG_SharedGameplayLCG_NextU32
00312E56  idiv ebx
00312E58  sub  edx, ebp          ; remainder - param
```

```
offset = (LCG() % (2 * param + 1)) - param      /* uniform in [-param, +param] */
```

**A point is sampled around a reference position, up to nine times, until one passes.** On success
the caller copies the resulting 16-byte position out and writes the actor's radius — the
`maxss` of the pair from `ActorRuntime_GetClass3FloatPair` (`00265090`) — through the optional
out-pointer.

> **So the order language's largest family is "go somewhere random near here, within ±N", and `N` is
> the order's own parameter.** Thirty-two opcodes share it; what distinguishes them is the index
> `opcode − 0x3FFF` passed alongside, which selects *which* reference position — not read here.

#### ⚠ And it is a different RNG from the avoidance recovery

**`00312DF0` calls `00328370` — the shared gameplay LCG.** The randomised avoidance functions
documented above call **`rand`** through IAT `008C3098`.

| system | stream | reproducible? |
|---|---|---|
| **order-goal random point** (`0x4000`–`0x401F`) | **shared gameplay LCG** `00328370` | **yes, if the LCG state is synchronised** |
| avoidance / detour recovery | **CRT `rand`**, process-global | **no, ever** |

> **Two randomised movement systems in one subsystem, on two different streams, with opposite
> determinism properties.** An authored order that says "wander within ±N" can be reproduced on
> another machine; a unit deciding for itself how to get around an obstacle cannot.
>
> **And this call site is a real `call`, not one of the seven inlined copies** the RNG document
> records — so it is one of the LCG draws that a hook on `00328370` would actually see.

#### Still open

~~**What the index `opcode − 0x3FFF` selects** — thirty-two reference positions, or thirty-two modes.
`00312DF0` is read only as far as the sampler; the rest of its 237 bytes, and the four special
opcodes' cases, are not. `DE-4`.~~

> **DE-4 answered 2026-09-12 (FABLE): the index is a POSENT record number — the area's authored
> position entries.** `00312DF0(ref, index, param, unit, out)` read whole: when `ref` is NULL — and
> the 32-family's case passes NULL (`003127D0`) — it fetches the reference through
> `FieldData_GetFormat0RecordVectorByIndex(index, &pos)` (`00312EA3`–`00312EB1`; `−1` when the index
> is past the table), which is `FieldData_CopyIndexedRecordByFormatClass(0, index, rec)` returning the
> record's `+0x10` / `+0x14` / `+0x18` floats — format class 0 is section 016, the `FF12POS3` position
> table ([the POSENT table](../../25-EBP-Script-Container/Sections/section-016.md)), the same records [spawn placement](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) resolves a unit's lifecycle anchor
> point from. So order `0x4000 + k` means **"wander within ±param of POSENT entry k + 1"**. When
> `ref` is given the index is ignored: `0x4020` samples around the ~~actor record's~~ SpawnRecord's (`[unit+0x6A0]`) `+0x50` *(corrected 2026-10-02, OPUS: `003127F1` `mov rcx, [rdi+0x6A0]` / `003127FB` `add rcx, 0x50`)* (an
> enemy-kind unit only, `003127D7`–`003127FF`) and `0x4125` around the unit's own `+0xD0`, its last
> navigable position ([the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)). Each try (nine at most, `00312E44`) offsets x and z by
> `LCG % (2·param + 1) − param`, writes `out` and asks `00317DE0(unit, &pos, param != 0)` — a
> four-float `{x, y, z, const}` placement test that is `00337700` for a zero radius and `003377C0`
> otherwise — returning 0 on the first accepted point, `−2` after nine refusals. The reference's y
> is written to `out + 4` before the loop (`00312E2D`–`00312E33`).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **InputGameplay — CLIENT.** A cited locomotion function is called by the 289-byte function labelled InputGameplay, a single unowned body inside the Input layer.
- **Rewards_Progression_Economy — CLIENT and SERVICE.** `Loot_FindOverlappingPickupIndex` (twice) calls cited functions. Cited functions call `Loot_FindNearestActivePickupPosition` and `LootPresence_GetSlotPosition`.
- **ActorEntity - CLIENT (60 edges).** `00203170`, `002367A0`, `00236820` are also called by bodies filed to ActorEntity: `003F1E90` (StateInterpolation), `0031B810`, `0031B770` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (25 edges).** `002367A0`, `00236820` are also called by bodies filed to combat AI: `00301AD0`, `00308C20`, `003219D0` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - SERVICE (1 edge).** `0046AB10` reaches bodies filed to core runtime: `0032A150` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (26 edges).** `00202F00`, `00203080`, `00203170` are also called by bodies filed to Gameplay: `00339630` (Combat); `002367A0` reaches bodies filed to Gameplay: `00322C50` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (25 edges).** `002367A0`, `00236820` are also called by bodies filed to party: `00326500`, `00328DB0`, `003261D0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (61 edges).** `00202F00`, `00203080` are also called by bodies filed to presentation: `003F3710`, `00466550`, `00274CB0` (AuthoredLineGeometry) - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - CLIENT and SERVICE (2 edges).** `00328370` is also called by bodies filed to random selection: `00308EC0`; `00312DF0` reaches bodies filed to random selection: `00328370` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (11 edges).** `00202F00`, `00203170`, `002E28E0` are also called by bodies filed to script VM / native bridge: `00356160`, `003409F0`, `00342640` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (8 edges).** `00236820`, `003272A0`, `00328370` are also called by bodies filed to spawn/encounter lifecycle: `00308D90`, `00234AF0`, `002350C0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (3 edges).** `002F8E70`, `002F8E90`, `00311F70` are also called by bodies filed to status/periodic terminal: `00386860`, `00301140` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (2 edges).** `002E5180` is also called by bodies filed to World: `0025E400` (ActorManager), `002623A0` (ActorManager) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (8 edges).** `002E28E0`, `0030F760`, `00310920` reach bodies filed to WorldAreaField (world area): `00377C20`, `00320940` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `FUN_00388320`, owned by that layer, calls `002F8E90` on this page. That caller is a 48-byte gate: bit 0 of `byte[+8]` and an agreeing predicate leave the globals alone, and anything else stamps both `[02AEDFBC]` and `[02AEDFB8]` with 1; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `FUN_00318cd0`, owned by that layer, calls `003272A0` on this page. That caller is an 869-byte routine that dispatches on its second argument and carries the constant `0x2C` as a width through the whole call; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `FUN_0031a300`, owned by that layer, calls `00236820` (`BattleUnit_GetBySlotIndex`) on this page — a slot-scan loop (`edi` counting up, a table at `022C257C` walked alongside). The accessor is a bounds-guarded pointer computation: negative slot → null, slot at or above `dword[0208E6A0]` → null (`00236824`–`0023682E`), otherwise `[0208E688] + slot * 0xF50`; `00236850` returns that same `dword[0208E6A0]` as the count, so the bound and the count are one value and cannot drift apart. The crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS reading, verified SWE2-CONTRACT).

## The `00312730` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`BattleLocomotion_DecodeOrderGoal` (`00312730`, ~~396 B~~ 965 B *(corrected 2026-09-30, SWE2-DATA: the function list
gives 965 bytes, as §3 does; `_index/candidates/dd-data-5-0930/mv_loco_checks.py` L4)*) is the order-goal
bytecode decoder: `ebx = word[rdx]` opcode (`00312742`), `00265090`
(`0031276B`), compares `ebx` against `0x4035` / `0x4026`
(`00312780`/`0031278C`), a `0x24`-bounded image-base switch
`byte[00120000 + rax + 0x1F2B10]` → `jmp rcx` (`0031279E`–`003127C5`),
with arms through `00312A60`/`00312A5D`/`00312AD6`, `0031B7E0` /
`0030A130` / `00312DF0` calls, and `byte[rax+5] == 1` checks
(`003127E7`/`003128AE`).

| member | role | interior |
| --- | --- | --- |
| `00309B10` (48 B) | heading/range classifier — `[rcx+0x10]` → `00265090` (`00309B22`), `xmm0 += [008C5F6C]` (the π/2 pair `3FC90FDB`) (`00309B33`), `00320A40` (`00309B44`), then word compares vs `0xFFFF` / `0xF000` / `0xE000` (`00309B60`–`00309B7E`) | [`00309B33`](../../_index/ADDRESS-INDEX.md) |
| `00312DF0` (237 B) | goal-record writer — `[01F44830]` save (`00312DFA`), `rsi = [rsp+0x90]` out-record, `float[rsi+4]`/`float[rsi]` stores (`00312E2D`–`00312E67`), `eax` vs `8` bound, `00328370` (`00312E50`) | [`00312E33`](../../_index/ADDRESS-INDEX.md) |
| `00317DE0` (111 B) | callback dispatch — `[01F44830]` save, reads `float[rdx]`/`+4`/`+8` position triple, `lea 00337700`/`003377C0` handler pair (`00317DF7`/`00317E11`), `xmm1 = 1.0f`, indirect `call rax` (`00317E3B`) | [`00317E22`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00265090`, `0031B7E0`, `0030A130`,
`00320A40`, `00328370`, `00312A60`, `00312A5D`, `00312AD6`. The
`0x4035`/`0x4026` opcodes sit in the `0x40xx` order family the
action-handler table already names.

## Typed census of `st+0xE0` / `st+0xBC` / `st+0xEC` — SWE2-STRUCT, 2026-09-17

`STRUCT-REQ-FABLE-LOCOMOTION-ANGLE-FIELDS`. The census instrument is
`Database/Tools/work/SWE2-STRUCT/loco_census.py`; the site list is
`locomotion-angle-accesses.tsv` beside this page. Forward propagation follows
`st` (the object `BuildSolverContext` parks at `ctx+0x100`/`ctx+0x108`), the
solver `ctx` itself (stack region marked by the `00336710` call-site
`lea rcx,[rsp+d]`), and the unit base through `lea r,[unit+0x80]`;
backtracing is gated to the seed set or a proven `lea +0x80` formation.

**Object identity — the displacement census conflated three objects.** The
three offsets are *not* one field set. On `st` (the locomotion state,
`BattleUnit+0x80`):

- **`st+0xE0` = `BattleUnit+0x160`** — the current heading.
- **`st+0xBC`** — **no access anywhere in the corpus.** FABLE's six `+0xBC`
  operands are `ctx+0xBC`, the solver-local copy of `st+0xE0` that
  `BuildSolverContext` makes at `003367F9`/`003367FF`. `BattleUnit+0x13C`
  carries no locomotion traffic.
- **`st+0xEC` = `BattleUnit+0x16C`** — the slow turn rate. Six readers, all
  `st`-typed (`00336595`, `00336650`, `0033A665`, `0033A68E`, `0033B3D8`,
  `0033CE8D`), each feeding it as the `step` argument of
  `Angle_ApproachWrappedRadians` (`00334120`) or the turn limiter.
  **Writers: two, neither a displacement store.** `BattleUnit_ResetStateForReuse`
  zeroes `unit+0x80..+0x690` at `00236B12`–`00236B28`, and the FCP tunable
  installer `003204E0` (called by `FUN_00239E10` with `r8 = &unit+0x16C`)
  stores the authored `@FCP` slot 3 (9 when `sel`) float at `0032053D`
  `movss [rbx], xmm0` — a `+0x0` store on an out-pointer, which is why no
  displacement census can see it. Observed authored values are in-range
  (party slot 3 = `0.7854` = 45°), but the store performs no clamp — the
  bound is authored data, not code. The stores a raw `+0xEC` displacement
  scan surfaces are on other objects: `002E28E0` writes `record+0xEC`,
  `002E5180` writes `MovementContext+0xEC` (`[rbx+0xB8]` at `002E51FE`),
  `003DA9F0` writes a word on the `0x130`-stride movement-body pool entry.

**Writers of `st+0xE0`.** Five routes, two frames:

| route | site | source |
| --- | --- | --- |
| solver publish (st frame) | `00336DC5` (`00336CE0`), `0033A35E` (`0033A240`) | `ctx+0xBC` verbatim |
| facing publish (unit frame `BU+0x160`) | `00300426` (`BattleUnit_PublishLocomotionPositionAndFacing`) | `xmm2` — a caller argument, stored raw |
| facing publish, record loop | `00310B00`, `00310BB1`, `00310CA6` (`00310920`, caller `0037D000`) | `xmm6` — caller argument |
| facing publish | `003120AF` (`00311F70`; callers include `00326D60`, `00313670`) | `xmm6` — caller argument |
| solver publish, alternate entries | none — `0033A120`/`0033A1E0`/`0033C9B0` do not write `st+0xE0` | — |

The two displacement-census `+0xE0` stores FABLE listed that are *not* on
`st`: `00266335` writes `MovementContext+0xE0 = 0.1f` (`r14 = [rbp+0xB8]` at
`00266042`), and `003DB130` writes the **movement body's** `+0xE0`
(`rcx = [[record+0xC0]+0x138]` at `002684BB`–`002684C5` in its only caller
`00268380`), with `xmm1` = `MovementContext+0x68` or
`MovementContext+0xC0 × MovementContext+0x24` — a params-derived magnitude,
not an angle.

**Is every stored value `Angle_NormalizeRadiansPi` output? No — on every
level.** `ctx+0xBC`'s own writers split four ways: normalizer returns
(`0033D09F`, `0033D15D`, `0033D388`, and `0033E1BC` via `00334120`'s
normalized paths), `ApplyHeadingTurnLimiter` returns (`0033960F`,
`003383B2`, `0033841C` — itself returning raw `st+0xE0` on its `00336530`
early path), yaw-from-direction `004687F0` returns (`0033C8D6`, `0033DB26`,
`0033DF93` — bounded by construction, the sine-LUT helper `0046F460`, never
through `0033CB70`), and **raw copies**: `0033D108`/`0033D398` refresh
`st+0xE0` verbatim, and the `jbe` fallbacks at `0033D099`/`0033D15A` store
`xmm6` = the solver's *desired-heading argument* unnormalized.
`Angle_ApproachWrappedRadians` (`00334120`) also has a `00334187` early path
returning its `target` argument raw. So the publish chain can carry a value
that never passed through the normalizer — and the facing-publish route
carries caller data that provably does not (e.g. `00326D60` reads the facing
from `[r8+r13+0x30]` table data at `00326F78`/`00327076`).

**Can a writer store outside `[−π, π]`?** Mechanically, yes: the facing
publish (`003003F0`/`00310920`/`00311F70`) performs no normalization, and
its callers supply authored/table facing; the `0033CEF0` fallbacks store the
raw desired-heading argument; `00334120`'s early path returns the raw
target. Whether any *reaches* a value outside the range — and whether the
normalizer's defective fast path fires — is the semantic question this
census deliberately does not answer.

- [x] **Whether any heading writer stores a value outside [−π, π], and whether the normaliser's defective fast path
  then fires.** The writers above do not normalise; no traced input is shown to leave the range. **SD-184**
  (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30 (SWE2-ORACLE `8acf79ac7`, after OPUS's first half `50890aa7f`); register row SD-184, record [`sd184-facing-sources-0930`](../../_index/candidates/sd184-facing-sources-0930/README.md): yes, shipped data stores headings outside the range - authored `setposparty` facings up to 5.846853 rad reach `BU+0x160` raw through `00310920`; no, the defective fast path does not fire from any of them, because it mis-normalises only |x| in (5π, 6π), (7π, 8π) and so on, and every traced non-debug value is below 4π. Residual: the `evt_t0505` debug accumulator can pass 5π, if that event is reachable in retail play (a runtime question). The record's 'What changes on the page' lists the writer-table amendments.)*

**`00202F00`** (the body FABLE flagged as unread): it is a `0x40`-byte
transform copy plus two CRT math thunks, tail-jumping `00217880` — a
heading-basis builder called from the solvers, not the out-parameter writer.
The `ctx+0xBC` store inside `0033DFD0` is direct: `0033E1BC`.

**Read/write type agreement.** Every `st+0xE0`/`st+0xEC` reader in the
solver corpus resolves to the same object the writers hit: `st`, obtained
either as `arg0` of the solve entries (`00336CE0`, `0033A120`, `0033A1E0`,
`0033A240`, `0033C9B0`), as `arg2` of `BuildSolverContext`, through
`[ctx+0x108]`/`[ctx+0x100]` inside solver internals (`003394A0`, `00335640`,
`00339DF0`, `0033A570`, `0033CEF0`, `0033D200`, `0033DFD0`, `0033CE60`,
`003364D0`, `00338140`), or as `unit+0x80` (`002FDC30`, `00325BB0`). The
unit-frame `BU+0x160` facing writers are the same field viewed one embed
out. The only type breaks in the corpus are the `MovementContext+0xE0`,
`MovementBody+0xE0` and `SecondaryContext+0x138`-entry accesses the raw
displacement scan also surfaces — none of them are `st`.
