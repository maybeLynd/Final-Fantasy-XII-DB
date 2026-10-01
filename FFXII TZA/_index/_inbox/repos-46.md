# repos-46 inbox — Phase D adversarial re-audit

Session `repos-46`. Project `Tools/work/proj_h46` / `GFZ_H46`. Scratch `Tools/work/repos-46/`.
Read-only against the GZF: no `Apply-*`, no `Pack-*`, no edits to any `_index/*.md`.

Program state for everything below: parent `2ed8affb…`, snapshot `46f02e26…`, embedded EXE
`73461d08…`, ledger 38,161 internal / 38,003 explicit / 158 unresolved / 99.58596 % / overlap 0.
`Verify-GfzCheckpoint.ps1` returned **CHECKPOINT VERIFIED** on all four gates before any reading.

---

## COVERAGE

Two documents amended in place. No new documents, no moves, no renames.

| Document | Before | After |
|---|---|---|
| `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` | `PARTIAL`, `audit.passes: 1`, 5 claims at tier 3 | **`DOCUMENTED`**, `audit.passes: 2`, every §3 address read at tier 1, 0 claims resting on annotation |
| `06-Movement-And-Navigation/heading-speed-to-position-delta.md` | `DOCUMENTED`, `audit.passes: 1` | `DOCUMENTED`, `audit.passes: 2`, headline formula corrected |

Both now carry a `## 10. Falsification pass 1` section with the killer-observation table, the
attacks that failed, the crossref disposition and the reopening propagation.

`reopened_count` raised 2 → 3 on both. `last_pass_state: falsification-pass-1-repos-46`.
`verified_against` unchanged — both already named the current parent and the claims were
re-derived against it, so the stamp was earned rather than advanced.

`check_links.py`: **161 files, 761 relative links, all resolve.**

### Debt table — please move these two rows

Both rows in *Now owed instead* are discharged:

| Document | Owed | Result |
|---|---|---|
| `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` | a first named falsification pass | **OVERTURNED in five places and corrected** |
| `06-Movement-And-Navigation/heading-speed-to-position-delta.md` | a first named falsification pass | **OVERTURNED in four places and corrected** |

---

## OPEN-QUESTIONS

**Closures — the ticked boxes are already in the documents, the ledger rows are not.**
`check_questions.py` will show these as ticked-box-vs-OPEN drift until this section is merged.

| ID | New status | Answer |
|---|---|---|
| **K-1** | ANSWERED | The second angle is `movement_state + 0xA0`, consumed as a **pitch**: `Y = sin(pitch)·speed`, and the same `cos(pitch)` foreshortens `X` and `Z`. The two `sin`/`cos` pairs are not independent — they are one spherical decomposition. |
| **K-3** | ANSWERED | `003A1D30` is `sqrtf(fabs(x))`: 23 bytes, `cvtss2sd` → `andps` with the 128-bit sign mask at `01CEBD80` → `cvtpd2ps` → **`jmp sqrtf`**. Scalar, not a vector routine; the caller supplies the sum of squares. 12 direct callers, 17 sites. |
| **K-5** | ANSWERED — **the premise was wrong** | There is no missing path and no decompiler artefact. `Movement_IntegratePositionAndMeasureDisplacement`'s no-context branch adds **all three** components; the earlier excerpt dropped the `X` line because it is written `*candidate_or_delta` while the other two use `[1]`/`[2]`. |
| **K-2** | still OPEN, **narrowed** | Class is `bActor_class_flags >> 5` (byte at `WorldActor+3`). Movement requires `3`; position-read admits `1` or `3`; `FUN_00265200` reads a heading from `movementState+0x38` for class 1 versus `+0xA8` for class 3, so the two classes have differently-shaped movement states. |
| **K-4** | still OPEN, **narrowed** | `world_ctx+0x90` bit 4 is passed as argument 2 to `FUN_00329B00` together with `world_ctx+0x70`, and only when the actor has a `pBattleUnit`. |
| **L-1** | ANSWERED — **neither of the two options offered** | `accept ⟺ (∃ at least one eligible slot) ∧ (∀ eligible slots: bounds hold)`. Rejection is universal (first violation returns 0); acceptance is existential (`accepted` starts at 0 and is set only inside the eligible branch), so **"no eligible player" is a rejection, not a vacuous pass**. And with the flag the spawn path actually passes (`0`), "eligible" narrows to the **party focus alone**. |
| **L-2** | ANSWERED — **seconds** | `SpawnKeep_RotatePersistenceBanksForAreaTransition` compares a raw tick delta against `(int)(DAT_01DFE0B8 * 30.0) * g_nSpawnKeepReturnWindow`. Default 300 ⇒ 9,000 ticks ⇒ **300 seconds**. The same `/(DAT_01DFE0B8*30)` converts ticks to the unit of `wRespawnCooldownTicks`. |
| **L-4** | ANSWERED | `g_flNativeLifecycleRange` at `02089368`, script-installed **43.0**, **squared**, compared against the **squared XZ** distance from the retiring actor to the **party focus** (not the party). Plus a second mode: `bLifecycleMode == 2` retires on the *leader approaching* an authored field point within `flLifecyclePointThreshold`. |
| **L-5** | ANSWERED | Two banks tagged **`btlKeepCharWork1`** / **`btlKeepCharWork2`** (authored strings at `009146B8` / `009146D0`), **`0x9400` = 37,888 B each = 296 entries × 128 B**. Rotation **exchanges** them when `enteringFieldId == g_wSpawnKeepPreviousFieldId` (the **A → B → A** pattern) inside the window; otherwise bank2 ← bank1, bank1 is `memset` to 0 and 64 history counters are reset to 1. Both banks plus the two field-id registers are serialised into a `0x20010`-byte save buffer. |
| **L-6** | ANSWERED | Squared, **and XZ-only**: `(p1[2]-p2[2])² + (p1[0]-p2[0])²`. Verified from the 31 bytes, not the decompiler. Both callers square their bounds before passing them. |
| **L-3** | still OPEN, **narrowed** | Bit 11 of the low dword of `qwUnitFlags`; set/cleared across a 32-bit spawn-group mask; every change is followed by `FUN_00312700(unit)`. |
| **Z-10** | **more evidence — see K-8** | Movement supplies the tie Z-10 recorded as missing: `DAT_01DFE0BC` multiplies **every authored locomotion speed** in `Movement_SetRequestedSpeedScaled`. Still no observed write away from `1.0` during play. |
| **Z-11** | **corroborated and extended** | All three members appear in the locomotion path: `_DAT_01DFE0B4 × 30` is a **frame count** threshold in `Movement_ModifyHeadingSpeedForObjectState`; `DAT_01DFE0B8 × 30.0 × 3.6 × speed` is the published locomotion rate; `DAT_01DFE0BC` scales authored speed. The `× 30.0` companion (`008F8D80`) is used as a **frame rate** — dividing raw ticks by `DAT_01DFE0B8 × 30` yields seconds. Shipped values re-read independently from the image: `1`, `1.0f`, `1.0f`. |

### New IDs proposed

| Proposed ID | Owner document | Question |
|---|---|---|
| `PROPOSED-repos46-1` (suggest **K-6**) | movement | The GFZ struct names `movementState+0xA0` `flCurrent_heading` and `+0xA4` `flDesired_heading`, but `002E4380` consumes `+0xA0` as an **elevation** and `+0xA4` as the yaw. Which name is wrong, and what is `+0xA8` (read by `FUN_00265200` for class 3)? |
| `PROPOSED-repos46-2` (suggest **K-7**) | movement | What do `FUN_00267260` and `FUN_00264460` test? Together they select the planar branch; `FUN_00264460` also selects the 3-D displacement measure. |
| `PROPOSED-repos46-3` (suggest **K-8**) | movement | Are `DAT_01DFE0BC` / `DAT_01DFE0B8` ever written away from `1.0` during play? Ties to Z-10. |
| `PROPOSED-repos46-4` (suggest **L-7**) | spawn | What supplies the **Y** coordinate of a generated spawn position? `FUN_00319390` writes only `[0]` and `[2]`; `[1]` is passed on unwritten. |
| `PROPOSED-repos46-5` (suggest **L-8**) | spawn | Meaning of the status mask `0x80000003` tested against BKBI `+0x3C` / `+0x64`, and of the `FieldData_GetActiveFieldRecordBit15()` escape that overrides it. |
| `PROPOSED-repos46-6` (suggest **L-9**) | spawn | What do unit-flag **bit 49** and **bit 53** (`0x2200000000000`) denote? They decide whether a minimum spawn distance is enforced at all. |
| `PROPOSED-repos46-7` (suggest **L-10**) | spawn | Is `FUN_0023A520` invoked by every zone? It is the only writer of the `39/42/43/180/1` default set, its sole call site is a ScriptVM thunk, and the globals are BSS — so a zone that never calls it runs with all-zero radii. |
| `PROPOSED-repos46-8` (suggest **L-11**) | spawn | The `bPersistenceKey` / `bPersistenceRestoreValue` policy in `Spawn_SelectContinuousEntry` (`00235360`), read only in part. |

### Naming disagreements found — recorded, not renamed

| Address | GFZ name | What the body does |
|---|---|---|
| `00321170` | `BattleUnit_GetBySlotIndexIfUnitFlag4Set` | tests `qwUnitFlags & 0x10`, not `& 4` |
| `002350C0` | `SpawnLifecycle_CheckAndRetireByNativeRange` | mode 2 retires on **approach** to an authored point — the opposite of a range check |
| `movementState+0xA0` | `flCurrent_heading` | consumed as an elevation angle by `002E4380` |

---

## AUDIT-LOG

Two pass entries follow, written for direct paste. Suggested numbers 130 and 131.

---

### 2026-09-02 - pass 130: the walk formula was two-thirds of a sphere, and K-5 was a dropped line

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `06-Movement-And-Navigation/heading-speed-to-position-delta.md` (+ sections 8d, 8e, 10;
5 in-place corrections); `_index/OPEN-QUESTIONS.md` K-1 K-3 K-5 answered, K-2 K-4 narrowed,
K-6 K-7 K-8 opened, Z-10 Z-11 extended
**Tool run:** fresh `DumpFullCoverageGraph` (38,161 fn); `audit_crossrefs.py`;
`DecompileAddressFileBounded` 83/83; **independent** capstone census over the exact body extent of
all 38,161 functions; PE VA→file-offset constant reads

**THE HEADLINE FORMULA WAS INCOMPLETE, AND SO IS THE GFZ ANNOTATION IT AGREED WITH.** The
document said `X = sin(heading)·speed`, `Z = cos(heading)·speed` with `Y` from an unidentified
"second angle". A byte-level trace of `002E4419`-`002E45A1` gives:

```
X = sin(yaw) * cos(pitch) * speed          yaw   = wrap(movementState[0xA4])
Y = sin(pitch)            * speed          pitch = wrap(movementState[0xA0])
Z = cos(yaw) * cos(pitch) * speed          W     = 1.0 on all four exits
```

**The two sin/cos pairs are not independent** — `cos(pitch)` is the *common factor* for both
horizontal components. **An actor on a slope covers less ground per frame at the same requested
speed.** A planar branch (`FUN_00267260 != 0 && FUN_00264460 == 0`) drops the pitch terms and
recovers the old formula, which is why it read as correct.

> **Two sources agreeing is not two pieces of evidence when one was derived from the other's
> neighbourhood.** The GFZ annotation makes the identical omission; a reader checking the doc
> against the annotation found agreement and stopped.

**K-5 WAS A TRANSCRIPTION ERROR THAT GOT PROMOTED TO A FINDING.** The document asked *"where is
`delta.x` applied? — this may indicate a third path"*. The line is in the body and always was:
`*candidate_or_delta = movement_state->flPosition_x + *candidate_or_delta;`. It uses the deref
form while the other two use `[1]`/`[2]`, so an excerpt built by matching the indexed form drops
it. **A surprising negative should be re-read before it is registered as an open question.**

**THE CALL CHAIN WAS A NEST; IT IS THREE SIBLINGS.** `002E4380` has **exactly one caller** and it
is `Movement_UpdateActorFrame`. `Movement_UpdateSteeringTowardTarget` calls neither the delta
computation nor the integrator. Steering is *conditional* on `(u8)(bSteeringMode - 1) < 4`.
Likewise `002E5380`/`002E54A0` are a **chain**, one caller each, not a pair — and `Prepare`'s own
body is inert at `mode == 0`, which is all the walking path ever passes.

**PRESENTATION WRITES BACK INTO MOVEMENT, AND THE DOCUMENT HAD NONE OF IT.**
`Movement_ModifyHeadingSpeedForObjectState` (`00424080`) indexes the CharacterRenderObject array
(`0x740` stride) and **rewrites yaw and speed by reference**: a latch substitutes the record's own
values decaying at **0.83** per call until below **0.05**; object state **`0x0D` forces speed to
zero**. `Movement_PublishHeadingState` writes both angles back to record `+0x240`.

**§8b SURVIVED AN ATTACK BY TWO INSTRUMENTS.** The `BattleUnit_GetBySlotIndex` census — already
corrected once for edges-vs-sites — was re-derived from a fresh graph *and* from a capstone census
that never consults Ghidra's edge model. **All eleven rows, both columns, exact**: 46 sites / 40
callers, Movement 11/10. `Actor_GetWorldPosition` likewise: 79 callers, Movement 16.

**Crossref:** 3 findings, all `UNACCOUNTED NEIGHBOUR`, 0 ghost / 0 drift / 0 classification; all
three dispositioned, and the re-run dropped it to 1 second-order survivor.

---

### 2026-09-02 - pass 131: the spawn ring measured, and "a distance rule, not luck" was luck

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` — **`PARTIAL` →
`DOCUMENTED`**, 5 corrections, sections 8d and 10 added; `_index/OPEN-QUESTIONS.md` L-1 L-2 L-4
L-5 L-6 answered, L-3 narrowed, L-7..L-11 opened
**Tool run:** same instruments as pass 130, plus PE string reads and an exhaustive
memory-operand writer census

**THE WHOLE TUNABLE RING IS RECOVERED, WITH ITS DEFAULTS AND ITS OWNERS.**

```
02089358  arc degrees              180      -> the FORWARD HALF-PLANE, +/-90 deg of leader facing
02089360  min spawn distance        39.0
02089364  max spawn distance        42.0
02089368  retire range              43.0    -> one unit of hysteresis past the spawn ring
0208D457  position attempt limit     1
0208936C  return window            300      seconds
0208D458  automatic active cap      28      of a 32-slot BattleUnit pool
02F973B8  max considered distance  +INF     shared with AI targeting and loot pickup
```

**Two of these are engine defaults and five are authored.** The window and the cap are written by
native initialisers (`BattleStorage_InitializeWorkArrays`, `BattleSystem_InitializeAreaState`).
The radii, arc and attempt limit are written **only** by `FUN_0023A520`, **whose single call site
in the whole binary is a ScriptVM thunk** — and the globals are BSS. Every one has a `VM_*` setter.
That *weakened* a claim the amendment was about to make and is registered as **L-10** rather than
papered over.

**"MONSTERS DO NOT MATERIALISE IN YOUR FACE … THAT IS A DISTANCE RULE, NOT LUCK" IS WRONG TWICE.**
`Spawn_TrySelectCandidatePosition` has **two exclusive modes** keyed on the first byte of an
authored field-class-0 record. In *area* mode it **draws the position from the shared gameplay
LCG** — a radius quantised to 1/100 in `[min,max)` and a heading inside the arc, around the party
leader — and **never calls the distance validator at all**. And the minimum distance is applied
only when the unit carries flag bit 49 or 53; **every other spawn-backed unit is given `minR = 0.0`
and may be placed on top of the player.**

The thread was an `UNACCOUNTED NEIGHBOUR`: `00234AF0 callee 00328370` under
`RNG_Random_Selection`, a subsystem the document never mentioned. **The mechanical finding was
right and the human had no reason to look.**

**`0031B810` IS NOT A TABLE.** The document listed it as *"party/player slot table (up to 4)"*. It
is `BattleUnit_FindMappedDefinitionSelectorByIndex`, a **70-byte function** with 27 callers; the
table it consults is at `DAT_02EBF190 + 0x5A5A`. **An address in a document is a claim about what
lives at that address, separately checkable from the claim about behaviour** — the behavioural
half ("up to four slots") was correct all along.

**L-1 IS ANSWERED AND IT IS NEITHER OF THE TWO OPTIONS THE DOCUMENT OFFERED.**
`accept ⟺ (∃ eligible slot) ∧ (∀ eligible slots: bounds hold)`. **"Nobody to measure against" is a
rejection.** And the spawn path passes `include_all_party_slots = 0`, so "eligible" is **one
character** — the one you are steering.

**EVERY DISTANCE IN THIS SYSTEM IS SQUARED AND XZ-PLANAR.** `003A1960` is
`(p1[2]-p2[2])² + (p1[0]-p2[0])²` — verified from 31 bytes of disassembly. Both callers square
their bounds first (`min*min` in the spawn path, `x*x` in `00308040`). **Height never counts**, in
spawning, retiring or engagement.

**THE RETIRE FUNCTION HAS AN OPPOSITE SECOND MODE.** `bLifecycleMode == 2` retires a unit when the
**leader comes within** `flLifecyclePointThreshold` of an authored point. Naming it
"CheckAndRetireByNativeRange" describes half its behaviour.

**L-2 AND L-5 CLOSE TOGETHER FROM ONE LINE.** Restore fires **only** on
`enteringFieldId == g_wSpawnKeepPreviousFieldId` — the **A → B → A** pattern, not "you came back"
— within `(int)(DAT_01DFE0B8 * 30.0) * window` raw ticks: **30 × 300 = 9,000 ticks = 300 seconds**.
Banks are `btlKeepCharWork1`/`2` (authored strings), `0x9400` each, **296 entries × 128 B**, and
**enmity per combatant is banked and restored** along with death counts and positions.

**THE INSTRUMENTS DISAGREED AND THE DISAGREEMENT WAS RESOLVED BY LOOKING.** Ghidra's graph reports
`FUN_0023A520` with **zero** callers; the capstone census found **one** — `thunk_FUN_0023a520`.
Ghidra models thunk forwarding, capstone counts the `jmp`. The same difference explains
`003A1960` at 7 callers versus 8 sites. **Both instruments are right; neither was preferred by
provenance.** Had only the graph been trusted, the document would have said the default installer
is unreachable.

**Crossref:** 8 findings, all `UNACCOUNTED NEIGHBOUR`, 0 ghost / 0 drift / 0 classification. Three
were **real and two of them overturned text**; five were hub-by-reference. Re-run: 8 → 1.

---

### Structural note for the log — not mine, but new since this pass started

The 2026-09-02 `audit_crossrefs.py` run at the start of this block reported **247 findings, all
`UNACCOUNTED NEIGHBOUR`, zero `GHOST ADDRESS` and zero `BODY DRIFT`**. A re-run about two hours
later, same graph, reports **10 `GHOST ADDRESS` and 1 `BODY DRIFT`** in three documents none of
this session's work touched:

```
22-Middleware-PhyreEngine/Animation-Channel-Binding/...        7 ghosts
    01CEBBA8  01F2CE40 01F2CE58 01F2CE70 01F2CE88 01F2CEA0 01F2CEB8
23-Third-Party-Libraries/Bullet-Physics-Integration/...        2 ghosts
    01F44CF0  02EAF6C4
24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/...  1 ghost + 1 drift
    01F44850 ; 00896280 says 59,914 B, current body is 12 B
```

Every ghost is a **`.data` / `.rdata` address written into a table cell that carries a body
size** — a data address formatted as though it were a function. That is the *same defect class*
this pass just corrected in the spawn document (`0031B810` listed as a table in a key-address
table), arrived at independently by three other documents in one session. `GHOST ADDRESS` had
been **zero in every prior pass**; the standard's own corollary says that is the number to watch.

Flagging for the coordinator: this looks like a live pattern worth a note in the writing
standard — *a key-address table means "this address is a function"; data addresses belong in the
data-structure block, without a body-size column.*

---

## CALL-CHAINS / ADDRESS-INDEX

### New cross-subsystem transitions, in both directions

| From (owner) | To (owner) | Kind | Note |
|---|---|---|---|
| `Movement` `002E4380` | `Presentation` `00424080` | **owner transition** | reads the CharacterRenderObject array and **writes back** the caller's yaw and speed by reference |
| `Movement` `002E5C10` | `Presentation` (`g_pCharacterRenderRecordArray`) | data write | both angles → record `+0x240`/`+0x244` |
| `Movement` `0026D6F0` | `Party` `003590D0` | trigger | the speed setter consults the party focus and sets a distinct flag bit when the actor **is** the focus |
| `Movement` `0026D6F0` | world context `+0xC8` | data write | published locomotion rate `= DAT_01DFE0B8 × 30.0 × 3.6 × speed` |
| `Movement` `0026D6A0` | `DAT_01DFE0BC` | data read | **every authored speed** is multiplied by the time-base reciprocal |
| `Spawn` `00234AF0` | `RNG` `00328370` | **owner transition** | 2 LCG draws per attempt in area mode |
| `Spawn` `00234AF0` | `Party` `003272A0` | trigger | the party **leader** is the origin of every generated candidate |
| `Spawn` `00234AF0` | `Movement` `FUN_00265200` | trigger | reads the leader's heading through the actor-class discriminator |
| `Spawn` `00234AF0` / `002350C0` | `WorldAreaField` `003209C0` / `00320940` / `002374E0` | trigger | field-class-0 records supply both the spawn region and the retirement point |
| `Spawn` `00234DA0` / `002350C0` | `ActorEntity` `0031B810`, `Party` `003273B0` | trigger | slot resolution and the focus test |
| `Spawn` `002352E0` | `CombatFormula` `00300520` | **owner transition** | HP-zero routes through `BattleStats_ModifyHPAndProcessLethalState`, so death processing runs |
| `Spawn` `002350C0` | `ActorEntity` `00300E40` | **owner transition** | retirement is a teardown-and-despawn |
| **`Gameplay` `00308040`** | **`Spawn` `00234DA0`** | **inbound owner transition** | a Combat-side predicate calls the spawn validator with `include_all_party_slots = 1` and **inverts** the result |
| `ActorEntity` `00233F70` | `Spawn` `002350C0` | trigger | the per-actor lifecycle frame drives range retirement |
| `Spawn` `00235720` | `Spawn` `00308D90` | internal | the 28-actor cap gate |
| `Script VM` `0050F410` / `0050F470` / `0050FC00` / `005107F0` / `00510320` / `00510710` | `Spawn` `0023A1D0` / `0023A1F0` / `00239020` / `00235340` / — / `0023A520` | **authored-intent seam** | the complete script control surface for spawn tunables |

### Addresses to add to ADDRESS-INDEX

| Address | Name | Body | Owner | Document |
|---|---|---|---|---|
| `00235720` | `Spawn_SelectAndPrepareAutomaticEntry` | 841 B | Spawn | spawn |
| `002368D0` | `BattleStorage_InitializeWorkArrays` | 353 B | ActorEntity | spawn |
| `0023A520` | spawn tunable reset (unnamed) | 66 B | — | spawn |
| `0023A1D0` | `Spawn_SetNativeLifecycleRanges` | 25 B | Spawn | spawn |
| `0023A1F0` | `Spawn_SetCandidateHeadingArcDegrees` | 11 B | Spawn | spawn |
| `00239020` | `Spawn_SetPositionAttemptLimit` | 19 B | Spawn | spawn |
| `00308040` | `BattleUnit_HasNonPartyEngagementEvidence` | 237 B | — | spawn |
| `00308D90` | `Spawn_CountActiveCapTrackedActors` | 69 B | Spawn | spawn |
| `0031B810` | `BattleUnit_FindMappedDefinitionSelectorByIndex` | 70 B | ActorEntity | spawn |
| `003A1960` | `Vector3_ComputeSquaredXZDistance` | 31 B | — | spawn |
| `0031E620` | thunk → `003A1960` | 5 B | — | spawn |
| `00320940` | `FieldData_GetFormat0RecordVectorByIndex` | 117 B | WorldAreaField | spawn |
| `003209C0` | field-record copy wrapper, class 0 | 29 B | WorldAreaField | spawn |
| `0031AC90` | `Vector3_ComputeXZHeadingOrFallback` | 44 B | — | spawn |
| `0031A930` | `Math_NormalizeAngleDifference` | 89 B | — | spawn |
| `00319390` | sine-table polar offset (unnamed) | 139 B | — | spawn |
| `00316DA0` | angle wrap (unnamed) | 74 B | — | spawn |
| `00424080` | `Movement_ModifyHeadingSpeedForObjectState` | 427 B | Movement | movement |
| `002E5C10` | `Movement_PublishHeadingState` | 85 B | Movement | movement |
| `00265020` | `Actor_GetWorldPosition` | 61 B | ActorEntity | both |
| `003A1D30` | `sqrtf(fabs(x))` (unnamed) | 23 B | — | movement |
| `00265200` | class-dependent heading getter (unnamed) | 55 B | Movement | both |

### Constants worth indexing (all read from the image, VA → file offset)

```
01CEBC78  6.2831855  TWO_PI      01CEBC50  3.1415927  PI
00915620 -3.1415927 -PI          00915624 -6.2831855 -TWO_PI
00902438  360.0                  008F3134  100.0    (radius quantum, also a threshold in 00308040)
008F8D80  30.0    (frame rate)   00915734  3.6
008F30E8  0.05    (slide release) 008FCC8C  0.9     00D12434  0.83  (slide decay)
01CEBD80  7FFFFFFFFFFFFFFF x2    (double abs mask)
00914700  +INF -> 02F973B8       009146EC/F0/F4  39.0 / 42.0 / 43.0
009146B0 "BtlWork"  009146B8 "btlKeepCharWork1"  009146D0 "btlKeepCharWork2"
```

---

## Notes for the coordinator

1. **`Verify-GfzCheckpoint.ps1` writes into the shared `Tools\work\verify\` directory** — not a
   per-session path. With four sessions running concurrently, two verifications overlapping there
   would race on `snapshot.fas2`, `embedded_exe.bin` and `residual_addrs.txt`. Mine passed with
   the correct hashes, and I copied `embedded_exe.bin` into my own scratch before using it, but
   the wrapper should probably take a `-WorkDir`.
2. **No mutation authority was exercised.** No `Apply-*`, no `Pack-*`, no `_index/*.md` edits.
   `Tools/work/proj_h46` and `Tools/work/repos-46` are the only paths written, plus the two
   documents.
3. **Two documents should reopen on evidence from this pass** —
   `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` (§8e: the `01DFE0B4` triple in the
   locomotion path, bearing on Z-10/Z-11) and
   `17-Presentation-Rendering/Character-Rendering/character-render-object.md` (two Movement
   functions write into its `0x740`-stride array, one of them replacing an actor's yaw and speed).
   `21-RNG-And-Determinism/rng-streams.md` gains a draw-count consumer, and
   `13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md` shares both the squared-XZ leaf
   and the `+INF` threshold. All four are listed in the respective §10s.
4. **The `GHOST ADDRESS` regression above is not mine and is worth acting on** — see the
   structural note in the AUDIT-LOG section.

---
---

# BLOCK 2 — the reopens, three corrections to my own pass 1, and an instrument audit

Same program state and instruments as block 1. Read-only against the GZF; no `Apply-*`, no
`Pack-*`, no `_index/*.md` edits.

## COVERAGE

| Document | Change |
|---|---|
| `06-Movement-And-Navigation/heading-speed-to-position-delta.md` | §8f added — **a conflation of mine retracted**; §4 data block rewritten with the real record layout; K-10 opened; caller counts corrected; instrument caveat added |
| `17-Presentation-Rendering/Character-Rendering/character-render-object.md` | §8b added — **a separation check, not a reopen**; `audit.passes` 1 → 2; status stays `DOCUMENTED`, still owes its first attack |
| `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` | §8k added — enmity persistence; `audit.passes` 1 → 2, `reopened_count` 8 → 9 |
| `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` | §8e added — **a tier error of mine corrected**; §2 bank-copy passage rewritten; two §8 rows split and re-cited; third-order dispositions; instrument caveat |

`check_links.py` — **167 files, 789 links, all resolve.**
`check_consistency.py` — **0 SIZE / 0 NAME / 0 CALLER-COUNT / 0 frontmatter gaps. Fully clean.**
`audit_crossrefs.py` — **266 findings database-wide, all `UNACCOUNTED NEIGHBOUR`**; your ghost fixes
landed and the 10 GHOST + 1 BODY DRIFT are gone. Of my four documents: movement **0**,
character-render-object **0**, gambit **0**, spawn **2** (both third-order, dispositioned in place).

## THE EXTENT DEFECT — MEASURED, AND MY CONCLUSIONS SURVIVE

You were right to make me check rather than assume. **29 of the 38,161 functions carry a
`body_bytes` that over-runs the next function's entry**, 1,917 bytes in total. `00350320` is one of
them exactly as repos-f1 described.

I rebuilt the census with the extent clamped to the next entry **and** truncated at the first
`int3` following a terminator, then diffed the two runs:

| | raw extent | clamped + int3 | spurious |
|---|---:|---:|---:|
| call sites | 155,220 | 155,179 | **41** (0.026 %) |
| caller→callee pairs | 110,611 | 110,580 | **33** (0.030 %) |
| RIP-relative memory references | 164,489 | 164,460 | **29** (0.018 %) |

**Every number I published is byte-identical under both walks.** All ten call-count claims
(`00236820` 46/40 with Movement 11/10, `00265020` 104/79, `00313F60` 67/47, `00377C20` 80/66,
`003A1960` 8/8, `003A1D30` 17/12, `0031B810` 27/27, `0023A520` 1/1, `00234DA0` 2/2, `002E4380`
1/1), every writer census, and the empty vtable/array intersection. None of the 29 affected
functions calls anything I counted.

**The diff is its own positive control** — the two runs genuinely differ by 41/33/29, so a null
result is not a silent instrument. Two of the spurious edges point at `001DDD0A` and `0030517E`,
addresses that are not function entries at all: **a spurious edge to a mid-instruction target is
the cheapest available tell that an extent walk has run off the end.** Worth adding to the
checker.

The caveat and this table are now written into both of my documents' §10, replacing the bare
phrase "exact body extent".

## 00313F60 — SETTLED, AND THE ODD ONE OUT WAS MINE

| Address | Role | Distinct callers | Call sites |
|---|---|---:|---:|
| `00313F60` | 5-byte `JMP rel32` thunk | **47** | 67 |
| `00377C20` | the 78-byte predicate, **excluding the thunk** | **65** | 79 |
| union — distinct functions reaching the predicate by either route | | **110** | 146 |

Ghidra's edge model returns 47 and 65. The capstone census returns 47 and 66, where the extra one
**is** the thunk; subtract it and the two instruments agree exactly, so thunk forwarding does not
need to be invoked to explain the gap. Two functions call both routes, which is why the union is
110 and not 112. Neither address is address-taken, so there is no third route.

**Both other documents are already correct and already state their selectors.**
`field-record-bit15-action-permission.md` says *"65 direct callers, 110 including the thunk"* and
names `00313F60` as a thunk with *"47 further callers"*; `cross-subsystem-accessor-hubs.md` carries
the merged row with its own 2026-09-02 correction note. **Neither reopens.** The wrong number was
in my movement document, which attached the thunk's 47 to the body. Fixed, with the selector beside
every figure.

### Two `check_consistency.py` artefacts found while settling it

1. **It reads a quoted retraction as a live claim.** Writing the correction in the form the
   evidence standard mandates — *"this row originally read `00377C20` … with 47 callers"* — puts
   the retracted pairing back on the page, and the COUNT pattern matches it. The file has a
   `CORRECTION` regex that plainly intends to cover this; it is not applied to the count patterns.
   **Every future correction of a count will trip the checker that the correction exists to
   satisfy.** I rephrased mine to state the figure without re-adjoining it to the address, which
   preserves the trail, but the parser is the right place to fix it.
2. **A sentence naming two addresses and two counts mis-pairs them.** In
   `field-record-bit15-action-permission.md`, *"`00377C20` with 65 callers and `00313F60` with
   47"* extracts as `00313F60 = 65`, because pattern 2 searches backwards up to 40 characters and
   finds the nearer address. Harmless there; it would not be if those figures were compared
   against another document.

## THREE CORRECTIONS TO MY OWN PASS 1

### 1. The `0x740` array is NOT `CharacterRenderObject` — retracted before it propagated

I reported that `Movement_ModifyHeadingSpeedForObjectState` and `Movement_PublishHeadingState`
write into *the class* `character-render-object.md` documents, and asked you to reopen it.
**They do not.** Four independent disproofs, any one sufficient:

```
size        CharacterRenderObject 0x668 = 1,640 B   vs   record stride 0x740 = 1,856 B
first field vtable ptr 00903B68                     vs   i16 id, compared against -1
allocator   FUN_00210EC0, one object at a time      vs   FUN_0036A100, one 0x48930 block
functions referencing BOTH the vtable and the array base 022C6F28 : NONE
```

The memory-operand census finds vtable `00903B68` in exactly 2 functions and array base
`022C6F28` in 636 sites, **with an empty intersection** under both extent walks. The array is a
Presentation-owned block of **exactly 160 records** — `160 × 0x740 = 0x48830`, precisely where
`FUN_00426480` writes a trailing dword — allocated by `CharacterRenderSystem_AllocateAndInitialize`
(`003325D0`).

**Why I got it wrong, and it is the exact error this pass exists to catch.** The decompiler renders
the base as `g_pCharacterRenderRecordArray`. "CharacterRender" plus a large per-character stride
plus a Presentation owner *looks like* a class a Presentation document already describes. **That is
"it looks like it belongs to X" — banned as proof — committed in the same pass whose §10
congratulates itself for refusing address adjacency.** Refusing one banned inference does not
inoculate against another in a different costume. The tell was on the page the whole time: both
sizes were written down, in two documents, and never subtracted.

**Every mechanical claim about the override survives** — stride, by-reference rewrite of yaw and
speed, `0.83` decay to a `0.05` floor, the `+0x62C` latch, `_DAT_01DFE0B4 × 30`, state `0x0D`
zeroing speed — all re-verified byte-exactly at `0042408A`-`004241A0`. Only the container's
identity was wrong. So `character-render-object.md` received a **`Do not confuse with`** section
carrying the disproof, **not a reopen**, and its status stays `DOCUMENTED` with its first
falsification pass still owed.

### 2. A decompiler's struct is not a body — a tier error in the spawn document

I wrote *"per-entry fields visible in the copy loops"* and cited it at **tier 1**. All four bank
loops are **eight `movups` per entry — 128 bytes, wholesale** — and reference no field at all.
Ghidra printed sixty-odd named member assignments because a struct type is applied at those
addresses. **The names are painted onto a `memcpy`.**

The give-away was available and unread: `SpawnKeep_RestorePersistenceBank` has a **127-byte body**
and decompiled to about a hundred lines of member copies. **A function cannot copy sixty named
fields in 127 bytes.** Proposed standing check: *when a decompilation names fields, confirm the
instruction stream addresses them — and a body size that cannot hold the printed work is the
cheapest possible test.*

The conclusion survived on better evidence, and the corrected evidence is **stronger** than the
original: it fixes the block's extent, which the struct annotation had implied was `0x2E` bytes of
enmity alone.

### 3. `003A1D30` caller count 13 → 12 — already merged in block 1, restated for completeness.

## OPEN-QUESTIONS

| ID | Status | Note |
|---|---|---|
| **K-9** | **DOES NOT ARISE — please close or re-scope** | You filed it for the Presentation → Movement latch on my assumption that it belonged to `CharacterRenderObject`. The latch is real; the container was misidentified. Re-scope onto **K-10** or close as superseded. |
| `PROPOSED-repos46-9` (suggest **K-10**) | new | The character render **record array** — 160 records × 1,856 B at `022C6F28`, five authored render stages, Presentation-owned, written by Movement. No document exists; §8f names the starting evidence. |
| **L-8** | still OPEN, **now cross-subsystem** | The `0x80000003` status predicate has a **fourth** site: `BattleEnmity_WriteAllCombatantIds` refuses to write threat unless it passes. One masked status pair plus one field-record escape now gates spawn eligibility, range retirement **and** enmity adjustment. Closing it is worth more than it was. |
| `PROPOSED-repos46-10` | new, low priority | `gambit-evaluation-and-enmity.md` carries **duplicate section letters** — two `8i` and two `8f`, from concurrent appends — which makes cross-references ambiguous. I used `8k` to avoid a third collision. |

### Promoted from tier 3 to tier 1 in the gambit document

```asm
0032156D  lea rdi, [rax + 0x19]     ; BattleEnmity_UpdatePeriodicDecay,  rax = unit[0x6A0] = BKEI
00321D61  lea r9,  [rax + 0x19]     ; BattleEnmity_WriteAllCombatantIds, same base
00321DA3  cmp ebx, 0x28             ; the write loop bound: exactly 40 combatant ids
```

`timer = BKEI + 0x19`; `enmity[id] = BKEI + 0x1A + id` for `id` in `0..39`, ending at `+0x41`. Both
figures were recorded in that document as *"GFZ records"*; they are now read from the instructions.

### On the question-ledger drift

`check_questions.py --drift` reports 26 items. **None is in a document I have touched.** The three
cross-check items are `input-stack-device-channel-and-bindings.md` (AP-1, AP-3, stale ticks owed)
and `gi-render-command-family.md` (BG-1/BG-6, an early tick); the other 23 are the duplicate
`BC-*` / `BD-*` / `BE-*` / `BG-*` / `BH-*` ids. My block-1 ticks match their ledger rows because
you merged the closures in the same pass — which is the protocol working.

## AUDIT-LOG

Suggested pass 132.

---

### 2026-09-02 - pass 132: the threat table is saved world state, and I caught myself doing the banned thing

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` (+ section 8k);
`06-Movement-And-Navigation/heading-speed-to-position-delta.md` (+ section 8f, **a retraction**);
`05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` (+ section 8e, **a tier
correction**); `17-Presentation-Rendering/Character-Rendering/character-render-object.md`
(+ section 8b, a separation check); OPEN-QUESTIONS K-9 K-10 L-8
**Tool run:** memory-operand census over all 38,161 function extents, **run twice** — raw and
clamped — and diffed; `check_consistency.py`; targeted disassembly of four block-copy loops and
three enmity functions

**AN ENEMY'S GRUDGE IS SAVED WORLD STATE, NOT FIGHT STATE.** The enmity table the gambit document
describes lives at `unit[0x6A0] + 0x19` — **inside a 128-byte entry of the spawn persistence bank
`btlKeepCharWork1`**. The bank is block-copied on every area transition, so **threat is carried,
wiped or reloaded by walking**: return on the **A → B → A** pattern within **300 seconds** and every
enemy resumes hating exactly who it hated at exactly the value it held; arrive any other way and
**every threat value in the zone is zeroed at once**. It is also serialised into the save image.
Decay runs only for units with `pBkbi[+5] == 1`, so a unit with no keep entry has nothing to decay
and nothing to persist.

**A FOURTH SITE OF THE `0x80000003` PREDICATE.** `BattleEnmity_WriteAllCombatantIds` refuses to
write threat unless `((bkbi[0x64] | bkbi[0x3C]) & 0x80000003) == 0 || FieldRecordBit15()`. Byte for
byte the gate on spawn candidate eligibility and on range retirement. One masked status pair with
one field-record escape decides whether a unit may be **spawned near, retired, or hated**.

**I COMMITTED THE BANNED INFERENCE IN THE PASS THAT BOASTED OF REFUSING IT.** Pass 130 reported that
two Movement functions write into the `CharacterRenderObject` array and asked that document to
reopen. **They write into a different structure.** `0x668` versus `0x740`; a vtable pointer versus
an `i16` id that can be `-1`; two allocators; and **no function in the binary references both** the
vtable and the array base.

> **Refusing one banned inference does not inoculate against another in a different costume.** Pass
> 130's own section 10 records refusing address adjacency for the spawn tunable block — correctly —
> while "looks like it belongs to X" went through unchallenged two sections earlier. **Both sizes
> were written down, in two documents, and never subtracted.** The reopen was withdrawn before it
> propagated; the render-object document received the disproof instead, and its first falsification
> pass is still owed.

**A DECOMPILER'S STRUCT IS NOT A BODY.** Pass 131 cited *"per-entry fields visible in the copy
loops"* at tier 1. All four loops are **eight `movups` per entry, 128 bytes, wholesale**, naming
nothing. **The tell was the body size: `SpawnKeep_RestorePersistenceBank` is 127 bytes and
decompiled to a hundred lines of member copies.** New standard: *when a decompilation names fields,
confirm the instructions address them; a body that cannot hold the printed work is the cheapest
possible check.* The conclusion survived on better evidence and the extent was corrected —
`+0x19..+0x41`, not `0x2E` bytes of enmity.

**THE EXTENT DEFECT, MEASURED RATHER THAN ASSUMED.** 29 of 38,161 ledger extents over-run the next
entry. Re-running the whole census clamped and diffing gives **41 spurious call sites (0.026 %), 33
spurious edges, 29 spurious memory references** — and **every figure passes 130-132 published is
identical under both walks.** Two spurious edges target `001DDD0A` and `0030517E`, which are not
function entries: **an edge to a mid-instruction target is the cheapest tell that an extent walk
has run off the end**, and belongs in the checker.

**THE THREE-WAY CALLER-COUNT DISAGREEMENT WAS ONE DOCUMENT'S ERROR, AND IT WAS MINE.** `00313F60`
is a thunk with **47** callers; `00377C20` is the predicate with **65** direct plus those 47,
**110 distinct functions** in all, 2 using both routes. **Both other documents were already correct
and already carried their selectors**; neither reopens. `check_consistency.py` is now 0/0/0.

**TWO CHECKER ARTEFACTS, BOTH REPORTED.** `check_consistency.py` reads a *quoted retraction* as a
live claim — so writing a correction in the form the evidence standard mandates trips the checker
that correction was meant to satisfy. And a sentence naming two addresses with two counts mis-pairs
them, because the backward search finds the nearer address.

---

## CALL-CHAINS / ADDRESS-INDEX

| From (owner) | To (owner) | Kind | Note |
|---|---|---|---|
| `CombatAI` `00321530` / `00321D30` | `Spawn` BKEI `+0x19` | **data ownership** | the enmity table is a field of the spawn keep entry, not of the BattleUnit |
| `Spawn` `00233780` / `00233440` / `00233550` | `CombatAI` enmity | **implicit carry** | blind 128-byte copies transport the threat table across transitions and into the save image |
| `Movement` `00424080` / `002E5C10` | character render **record array** `022C6F28` | **owner transition** | **not** `CharacterRenderObject` — see the retraction |
| `Presentation` `003325D0` | `022C6F28` | allocation | 160 records × `0x740`, dword at `+0x48830`, 256-byte trailer |
| `Presentation` `00332440` | five authored render stages | authored intent | the `"display character : …"` labels |

| Address | Name | Body | Owner |
|---|---|---|---|
| `003325D0` | `CharacterRenderSystem_AllocateAndInitialize` | 139 bytes | Presentation |
| `00332440` | character display pass dispatcher | 200 bytes | Presentation |
| `003323D0` | `RenderSystem_RunCharacterUpdatePipeline` | — | Presentation |
| `00426480` | writes the record-array trailing dword at `+0x48830` | 30 bytes | — |
| `00377C20` | `FieldData_GetActiveFieldRecordBit15` — the real body | 78 bytes | WorldAreaField |
| `00321D30` | `BattleEnmity_WriteAllCombatantIds` | 141 bytes | CombatAI |

Data addresses, no size column, per the new template rule: `022C6F28` record array base ·
`022C6F20` sibling written by the update pipeline · `02089370` most-recent field id ·
`02089372` previous field id · `02089374` transition tick · `00D10A18` / `00D10A38` / `00D10A60` /
`00D10A80` / `00D10AA8` the five render-stage labels.

---
---

# BLOCK 3 — `character-render-object.md`, first falsification pass

Same program state and instruments. Read-only against the GZF; no `Apply-*`, no `Pack-*`, no
`_index/*.md` edits.

## COVERAGE

| Document | Change |
|---|---|
| `17-Presentation-Rendering/Character-Rendering/character-render-object.md` | **first falsification pass** — §8c added; 3 claims overturned in place, 1 sharpened; §1, §2, §4, §7 amended; `audit.passes` 2 → 3 |

`check_links.py` — **169 files, 813 links, all resolve.**
`check_consistency.py` — **0/0/0, clean.**
`audit_crossrefs.py` — **275 findings database-wide, all `UNACCOUNTED NEIGHBOUR`.** All four
documents I have touched now report **zero findings each**.

Please move this row out of *Now owed instead*:

| Document | Owed | Result |
|---|---|---|
| `17-Presentation-Rendering/Character-Rendering/character-render-object.md` | a first named falsification pass | **3 claims OVERTURNED and corrected; BB-5 answered; BB-1 upgraded** |

## THREE OVERTURNS

**1. `11,874` bytes of method code → `11,879`.** The document's own §3 table sums to 11,879. The
headline was short by exactly **5** — the size of slot 29 (`00848340`), the single method living
outside the class's `001Fxxxx` cluster. Almost certainly the total was taken over the clustered
slots with the outlier dropped and the exclusion never stated. **The table was right, the headline
was wrong** — the same shape as the ScriptVM superlative in pass 128.

**2. The ready flag has two writers, not one.** `CharacterRenderObject_Construct` writes
`+0x4B4 = 0` at `001F4EC9` (`sil`, `esi` zeroed at `001F4DDF` and not reloaded); slot 2 writes `1`
at +2233 of 2,328 bytes. The original census ran **across the vtable**, and the constructor is not
in the vtable — the number was right for the set measured and the sentence generalised past it
("*the only method that touches it as a destination*"). **The conclusion is unharmed and the
evidence is better:** an explicit zero at construction supports "ready flag" more strongly than
relying on the allocator's zero-fill, and nothing clears the byte afterwards.

**3. Thirteen readers, not twelve — and one is not a gate.** Slot 16
(`SubmitMaterialsWithFadeMode`) reads the flag at **instruction 118**, inside a submission loop, as
one condition among several in a per-element skip test. The stated *"reads within the first 12
instructions: 12 of 12"* also contradicted the *"reads: 13"* two lines above it **in the same
block** — a block that disagreed with itself and had stood unchecked.

## BB-5 ANSWERED, BB-1 UPGRADED

**BB-5.** `FUN_001F51E0` is the class's **destructor body**: it re-installs the vtable at `[rcx]`
(standard MSVC destructor behaviour), zeroes `+0x28`, destroys a container at `+0x3E0`, then walks
`+0x390`/`+0x3A0`/`+0x3A8` at element stride `0x38`. **Exactly one caller: slot 0**, the scalar
deleting destructor. Not a second construction site.

**BB-1** was a standing admission that no draw call had ever been traced. It is now a **measured
negative**: the 31 methods call **46 real functions** at one hop, and the complete named set is CRT
and nothing else — `memcpy` ×15, `memset`, `sqrtf`, `tan`, `free`, `_alloca_probe`,
`__security_check_cookie`, `__report_rangecheckfailure`, `_guard_check_icall`. The other 37 are
untagged internals owned by nothing. **No graphics API entry point anywhere in the set.** That does
not prove the class never causes a draw; it bounds it exactly — *whatever draws, it is not reached
in one call from these methods* — and it points the next search at the five authored stage labels
from block 2, which belong to the record array's dispatcher.

## WHAT SURVIVED A NAMED ATTACK

- **31 vtable slots** — read out of the PE image, not the recovered index. Slot 31 is
  `7865646E496E7573`, ASCII, not a pointer. The table ends at 31.
- **All 31 addresses and all 31 sizes** — 31/31 and 31/31 against the image.
- **Object size `0x668`** — and now confirmed *twice*: exactly three sites load the immediate,
  the allocation at `001BD527`, an unwind funclet (noted and **excluded**, banned), and **slot 0
  passing `0x668` to a sized `operator delete`**. Allocation and deallocation agree.
- **One construction site** — attacked three ways (callers of the constructor, other `0x668` loads,
  other vtable references) and it held.
- **Highest field `+0x664`** — and it is a **dword**, so it ends at `+0x668`, flush with the
  allocation rather than four bytes short as §4 implied.
- **`UpdateViewParameters` calls `tan` and `sqrtf`** — both present in its callee set.

## I CAUGHT MY OWN INSTRUMENT BEFORE IT PRODUCED A FOURTH "OVERTURN"

A scan for the highest displacement on any non-`RIP` base returned **`+0x10D9`**, which would have
overturned `+0x664`. It was on `rax`, loaded from a *different* object inside slot 16. Re-run with
a bounded `this`-tracker (`rcx` at entry, plus registers receiving a direct `mov` from a tracked
register, invalidated on any other write) the answer is **`+0x664`**, with `+0x654`, `+0x634`,
`+0x624`, `+0x614` beneath it — a coherent tail.

**A scan that is too broad invents a finding exactly as readily as one that is too narrow misses
one.** Worth pairing with the existing noise-floor rule in the standard: that one covers wide byte
scans, this one covers *structurally* wide scans, where every hit is a real instruction and the
error is in attribution rather than in decoding.

Second instrument note, smaller: my call-site census counts `JMP imm` alongside `CALL imm` so it
catches tail calls. Applied to a *callee* census that produces noise — 37 of an apparent 83
"callees" of the 31 methods were intra-function jump targets, not functions. Filtering to real
function entries gives 46. **My published caller/site counts are unaffected** because they are all
keyed on function-entry callees, which is what a tail call is.

## OPEN-QUESTIONS

`next_question_id.py --check BB` reports BB **TAKEN, 5 rows**, so BB-6 and BB-7 are free.

| ID | Status | Note |
|---|---|---|
| **BB-5** | **ANSWERED** | `FUN_001F51E0` is the destructor body, sole caller slot 0. |
| **BB-1** | still OPEN, **narrowed to a bounded negative** | 46 real one-hop callees, zero graphics API. Row text should carry the bound. |
| **BB-4** | unchanged, but note | The one-construction-site fact is now *stronger* (a matching sized delete) and still does not settle cardinality. |
| `PROPOSED-repos46-11` (suggest **BB-6**) | new | The class's **non-virtual** methods. `CharacterRenderObject_ResetState` (`001F89E0`, 137 B) reads the ready flag and is not in the vtable, so §3's 31 slots are the *virtual* inventory, not the method inventory. `FUN_001F5D70` and `FUN_001FAD50` also read `+0x4B4`. |
| `PROPOSED-repos46-12` (suggest **BB-7**) | new | `FUN_001F7790` (3,895 B), called twice from slot 2, larger than every vtable method except slot 19 — the biggest unexamined body in the class's neighbourhood. |

## AUDIT-LOG

Suggested pass 133.

---

### 2026-09-02 - pass 133: the ready flag has two writers, and a too-broad scan nearly invented a fourth overturn

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `17-Presentation-Rendering/Character-Rendering/character-render-object.md` (+ section 8c,
4 in-place corrections); OPEN-QUESTIONS BB-1 BB-5 BB-6 BB-7
**Tool run:** vtable read directly out of the PE image; all 31 method bodies disassembled with
clamped extents; a `+0x4B4` displacement scan across all 38,161 functions; a bounded `this`-register
tracker

**A CLASS THAT HAS NEVER BEEN ATTACKED LOSES THREE CLAIMS.** The headline **11,874 bytes** is
**11,879** - the document's own table said so and the headline had dropped slot 29, the one method
outside the class's address cluster, without stating the exclusion. **The ready flag has two
writers**, not one: the constructor writes `0` and slot 2 writes `1`; the original census ran across
the vtable and the constructor is not in it. **Thirteen methods read the flag, not twelve**, and
slot 16 reads it at instruction 118 as a per-element loop condition rather than an entry gate - a
figure that contradicted the read count two lines above it in the same block.

> **A census is right for the set it measured and wrong for the sentence it is written into.** All
> three overturns share one shape: a correct number, scoped to the vtable, generalised to the class.

**BB-5 CLOSED.** `FUN_001F51E0`, the only other function referencing the vtable, is the **destructor
body** - it re-installs the vtable, zeroes `+0x28` and destroys containers at `+0x3E0` and
`+0x390`-`+0x3A8` at stride `0x38`. Sole caller: slot 0.

**BB-1 UPGRADED FROM AN ADMISSION TO A MEASURED NEGATIVE.** The 31 methods call **46 real functions**
at one hop and **not one is a graphics API entry point** - the named set is entirely CRT. The claim
is now bounded rather than confessed: whatever draws, it is not reached in one call from this class.

**THE OBJECT SIZE IS NOW PROVEN TWICE.** Exactly three sites load the immediate `0x668`: the
allocation, an unwind funclet (**excluded, banned**), and **slot 0 passing it to a sized
`operator delete`**. Allocation and deallocation agree, which is stronger than the single allocation
site the document had.

**I CAUGHT MY OWN INSTRUMENT BEFORE IT PRODUCED A FOURTH OVERTURN.** A scan for the highest
displacement on any non-`RIP` base returned **`+0x10D9`** against the document's `+0x664`. It was on
`rax`, holding a different object inside slot 16. With a bounded `this`-tracker the answer is
**`+0x664`** exactly, with a coherent tail beneath it.

> **A scan that is too broad invents a finding exactly as readily as one that is too narrow misses
> one.** The existing noise-floor rule covers wide *byte* scans, where the error is in decoding.
> This is the structural sibling: every hit was a real instruction, and the error was entirely in
> **attribution**. Both are cured by characterising the instrument before believing the reading.

---

## CALL-CHAINS / ADDRESS-INDEX

| From | To | Kind | Note |
|---|---|---|---|
| slot 0 `001F52F0` | `001F51E0` | internal | scalar deleting destructor to destructor body |
| slot 0 `001F52F0` | sized `operator delete` | lifecycle | passes `0x668`, confirming the object size |
| `001F4DA0` constructor | `this+0x4B4` | data write | `= 0` |
| slot 2 `001F6E70` | `this+0x4B4` | data write | `= 1`, at +2233 of 2,328 bytes |
| slot 2 `001F6E70` | `001F7790` | internal | 3,895 B, called twice — BB-7 |
| the 31 methods | 46 real functions | census | CRT only among the named; **no graphics API** |

| Address | Name | Body | Note |
|---|---|---|---|
| `001F51E0` | `CharacterRenderObject` destructor body | 266 bytes | BB-5 |
| `001F89E0` | `CharacterRenderObject_ResetState` | 137 bytes | non-virtual, reads the ready flag |
| `001F7790` | unnamed, called twice from slot 2 | 3,895 bytes | BB-7 |

Data addresses, no size column: `00903B68` the vtable · `00903B60` its RTTI complete-object-locator
pointer, read but supporting no claim.

---
---

# BLOCK 4 — `worldactor-scriptvm-interpreter.md`, first attack on its own claims

Same program state. Read-only against the GZF; no `Apply-*`, no `Pack-*`, no `_index/*.md` edits.

## COVERAGE

| Document | Change |
|---|---|
| `01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md` | §12 added; §4 corrected and extended twice, §10 extended, §7 BQ-6 upgraded; `audit.passes` 3 → 4 |

`check_links.py` — **172 files, 835 links, all resolve.** `check_consistency.py` — **0/0/0.**

**Zero claims overturned.** One stale cross-section contradiction, three mechanisms it did not
have, one absence upgraded to a measured negative, and §11's rotation independently re-derived.

Please move its row out of *Now owed instead*.

## THE CONSTRAINT I SET MYSELF

§11's correction rests on ff12-script, so **I excluded it entirely**. Everything below is the PE
image and the interpreter's own body — no decompiler, no recovered index, no external name source.
That was the point of your brief: *check whether the new names survive a test the rewriter did not
use.* They do, twice.

## §11's ROTATION, RE-DERIVED FROM ENGINE DATA ALONE

**1. The arithmetic closes, and only under the rotation.** Records `0x00`–`0x62` carry
mnemonic-shaped strings; record `0x63` holds `0x0A`, not a pointer. Under the rotation those 99
strings name opcodes `0x01`–`0x63` and `NOP` (confirmed at `0x00D11A10`, immediately before record
0's `LABEL` at `0x00D11A14`) names opcode `0x00` — **exactly 100 names for exactly 100 opcodes, with
no remainder.** Unrotated you get 99 names for 100 opcodes *plus* an orphaned string: one opcode
unnamed, one string unexplained. **The rotation is the only alignment that balances.**

**2. The name column has no readers at all.** A displacement scan across all 38,161 function bodies
finds the descriptor table touched by **exactly one function** in the binary — the interpreter — at
**22 sites, every one of them `+0x00`**. Not one instruction anywhere reads `+0x08`. §11 asserted
this; it is now measured. **A column no code reads is a column nothing can keep honest** — that is
the mechanism by which a rotated name table ships and survives.

## BQ-6 — AN ABSENCE CLAIM, NOW WITH A POSITIVE CONTROL

```
descriptor + 0x00  (length)    22 sites   <- CONTROL: reproduces the document's own figure exactly
descriptor + 0x02  (unknown)    0 sites   <- the absence claim
descriptor + 0x08  (mnemonic)   0 sites
functions touching the table at all : 1
```

The instrument returns the expected 22 on the field that *is* read, so its zero on `+0x02` is a
measurement and not a silence. **The absence holds.**

## THREE MECHANISMS THE DOCUMENT DID NOT HAVE

**1. Suspension is implemented by rewinding the program counter.** The interpreter modifies `r14` by
an instruction length at 25 sites: **4 advance, 21 rewind**. A handler that must wait subtracts the
length of the instruction it just executed, so on re-entry the interpreter **re-fetches and
re-executes the same instruction**. There is no continuation and no resume state. Consequence for
scripts: **a suspending instruction runs more than once**, and any side effect performed before the
decision to wait repeats on every retry. That is a real hazard for anyone hooking a script command,
and for XIIOnline it means a replicated script step can fire its effects repeatedly on one client.

**2. The operand pre-decode is off by one from the length bands.** Operands are decoded for opcodes
**at or above `0x47`**; the length-3 band begins at **`0x48`**. Exactly one opcode falls in the gap
— **`0x47`, length 1** — and the VM reads two bytes past the end of it. **It never manifests because
`0x47 LONGCODESTART` is one of the six inert opcodes** and the operand is discarded. That is a
fourth independent argument that `0x47` really is inert: were it live, this would be a shipped bug.

**3. The third shared-handler group is the strongest evidence for the corrected names, and §11 used
only two.** There are **92 distinct jump-table targets for 100 opcodes**, so exactly three are
shared. §11 cited `PREQ/PREQSW/PREQEW` and `JMP/JMPINTERNAL`. The third is the six inert opcodes —
and rotated, that group contained **`PUSHA` and `PUSHV`**, which would make this a stack machine
whose *push* instructions do nothing. Corrected, it is six markers and pseudo-ops. **All three
groups are incoherent rotated and clean corrected — 0/3 against 3/3**, whole-table, engine data
only.

## THE ONE DEFECT — and you called its shape in advance

**§4 and §7 contradicted each other about BF-2.** §7 ticks it answered and §10 answered it (*the
`0x0A`–`0x0F` helper pops two typed operands from the VM return-value list*), while §4 still read
**"What `FUN_0025D740` does is not established. BF-2."** A stale sentence left behind when the
answer landed in a later section.

Same shape as the `12 of 12` / `13 reads` contradiction in `character-render-object.md` this
morning: **a document disagreeing with itself, in two places no reader would compare.**
Append-only correction sections make this the characteristic defect of a heavily-revised document —
the correction is written where it was discovered and the original statement stays where it was.
Worth a checker: *a question id marked ANSWERED in the ledger should not appear beside "not
established" anywhere in its owning document.*

Your §6 suspicion did **not** land, for the record — §6 and §4 were both properly updated by the
rewrite, the opcode numbers were never rotated, and the trap warning is correct as written. I
checked it rather than assuming it, which was the right instruction regardless of the outcome.

## THE NEAR-MISS — third this session, same shape

I disassembled from `0x0025E5E0`, found `movsx rax, word ptr [r8 + rcx*8 + 0x1ddea60]` followed by
**`sub r14, rax`**, and compared it with §10's block, which quotes the same lookup followed by
**`add r14, rax`**. That read as the document inverting the direction of the program counter — which
would have made §6's *"the other four are length 1 and genuinely are free"* advice wrong, because a
length-1 handler would walk backwards.

**The document was right and I was reading a different site.** There are 22 descriptor lookups; the
one at `0x25E5FE` is a rewind in a suspend path, and §10 quotes the one at `0x25E631`, followed by
`add r14, rax` at `0x25E641` exactly as written.

> **Three near-overturns in one session, all the same shape** — `+0x10D9` from an untracked
> register, 37 phantom callees from counting `JMP imm`, and now an `add`/`sub` inversion from
> reading one of 22 identical sites. Every one was an **attribution** error in an instrument, not a
> decoding error, and every one would have produced a confident, wrong correction to a document that
> was right. **When a document quotes assembly, identify *which* site it quotes before concluding it
> is wrong** — in a 14,646-byte function with 22 copies of one idiom, "the binary says otherwise" is
> a claim about which copy you happened to read.

## AUDIT-LOG

Suggested pass 134.

---

### 2026-09-02 - pass 134: the interpreter attacked without ff12-script, and the rotation re-derived from engine data

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md`
(+ section 12; section 4 corrected and extended twice, section 10 extended, BQ-6 upgraded)
**Tool run:** descriptor and jump tables read directly out of the PE image; capstone over the
complete 14,646-byte body; a descriptor-table displacement scan across all 38,161 function bodies.
**ff12-script deliberately excluded** - pass 131's correction rests on it, so re-using it would test
nothing.

**ZERO CLAIMS OVERTURNED**, and the rotation is now confirmed twice without any external source.
**The arithmetic closes only under the rotation:** 99 mnemonic-shaped strings in records
`0x00`-`0x62`, record `0x63` holding `0x0A` rather than a pointer, and an orphaned `NOP` immediately
before record 0's string - **exactly 100 names for 100 opcodes with no remainder**, where the
unrotated reading leaves one opcode unnamed and one string unexplained. **And the name column has no
readers at all:** the descriptor table is touched by **exactly one function** in the whole binary, at
**22 sites, all `+0x00`**. *A column no code reads is a column nothing can keep honest* - which is
precisely how a rotated name table ships and survives.

**BQ-6's ABSENCE NOW CARRIES A CONTROL.** `+0x00` returns 22 sites - reproducing the document's own
figure - and `+0x02` returns 0. The instrument answers on the field that is read, so the zero is a
measurement rather than a silence.

**THREE MECHANISMS ADDED.** *Suspension is a PC rewind*: 21 of 25 instruction-length writes to the PC
**subtract**, so a waiting handler rewinds and the instruction is **re-executed** on re-entry - there
is no continuation, and any side effect before the wait repeats on every retry. *The operand
pre-decode is off by one*: operands are decoded from `0x47` up but length 3 starts at `0x48`, so
opcode `0x47` is read two bytes past its end - harmless only because `0x47 LONGCODESTART` is inert,
which is a fourth argument that it is. *The third shared-handler group settles the names*: rotated,
the six inert opcodes included **`PUSHA` and `PUSHV`** - a stack machine whose push instructions do
nothing. **All three shared groups: 0/3 coherent rotated, 3/3 corrected.**

**ONE DEFECT, AND IT IS THE SHAPE THIS DATABASE KEEPS FINDING.** Section 7 ticks BF-2 answered and
section 10 answers it, while section 4 still read *"What `FUN_0025D740` does is not established"*.
Same shape as `character-render-object.md`'s `12 of 12` versus `13 reads` hours earlier: **a document
disagreeing with itself in two places no reader would compare.** Append-only correction sections make
this the characteristic defect of a heavily-revised document. Proposed checker: *an id the ledger
calls ANSWERED must not sit beside "not established" in its own document.*

**THE THIRD NEAR-OVERTURN OF THE SESSION, AND THE THIRD OF ONE KIND.** Reading from a mid-function
address I found `sub r14, rax` where section 10 quotes `add r14, rax`, and nearly reported the
document as having inverted the program counter. **There are 22 copies of that lookup; section 10
quotes a different one, correctly.** With `+0x10D9` from an untracked register and 37 phantom callees
from counting `JMP imm`, that is three instrument **attribution** failures in one session, none of
them a decoding failure, each of which would have produced a confident wrong correction to a correct
document.

> **When a document quotes assembly, identify which site it quotes before concluding it is wrong.**
> In a 14,646-byte function containing 22 copies of one idiom, *"the binary says otherwise"* is a
> claim about which copy you happened to read.

---

## CALL-CHAINS / ADDRESS-INDEX

| Fact | Value |
|---|---|
| descriptor table readers, whole binary | **1 function, 22 sites, all `+0x00`** |
| jump-table targets | 92 distinct for 100 opcodes; 3 shared |
| PC writes by instruction length | 4 advance, **21 rewind** |
| operand pre-decode threshold | opcode `>= 0x47`; length-3 band `>= 0x48`; gap = `0x47` alone |
| image base materialisation | `lea r8, [rip - 0x13e5dd]` at `0025E5D6`, and `lea rax, [rip - 0x13e631]` at `0025E62A`, both `0x120000` |

Data addresses, no size column: `01EFEA60` descriptor table · `00261DF8` jump table ·
`00D11A10` the orphaned `NOP` · `00D11A14` record 0's `LABEL`.

---
---

# BLOCK 5 — `game-application.md`, first falsification pass

Same program state. Read-only against the GZF; no `Apply-*`, no `Pack-*`, no `_index/*.md` edits.

## COVERAGE

| Document | Change |
|---|---|
| `00-Engine-Core-Runtime/Application-Root/game-application.md` | **first falsification pass** — §10 added; **6 claims overturned**; headline, §3, §4, §5, §7 rewritten; `audit.passes` 1 → 2 |

`check_links.py` — **175 files, 858 links, all resolve.**
`check_answered_not_established.py` — its only hit is the language/locale one you already flagged;
none of mine.

Please move its row out of *Now owed instead*.

## SIX OVERTURNS

**1. There IS a deleting destructor, and it states the object size.** §4 argued the application root
is never deleted, so no sized `operator delete` exists to state its size, and `≥ 0x1140` was a lower
bound from field access. **Slot 0 (`0017CC70`) is a textbook MSVC scalar deleting destructor** — it
re-installs the vtable, calls the base destructor, tests bit 0 of the flag, and on the sized path
carries **`mov edx, 0x1140`**. The object is **exactly `0x1140` = 4,416 bytes. BE-4 answered.**

> The reasoning that produced the wrong claim was sound and its premise was simply unchecked: *the
> application is never deleted* is probably true at runtime, but a C++ compiler emits the deleting
> destructor for any polymorphic class whether or not the program ever calls it. **"This never
> happens at runtime" does not predict "the code is not there."**

**A caution I kept separate from the size claim:** the sized-delete callee `0x0016D6A0` is three
bytes — `ret 0` — with **2,480 callers**. It is an `/OPT:ICF` fold and worthless as evidence about
deletion. The **size immediate is emitted at the call site by the compiler** and does not depend on
what its target got folded with. Claiming the size while claiming nothing about the callee is the
correct split, and I said so in the document.

**2. Slot 5's address is a GHOST.** §3 gave `0017CE40`. That is **not a function** — it is a
**mid-body address inside slot 24** (`0017CE20`, 39 B, spanning `0017CE20`–`0017CE47`). The real
slot 5 is `0017CDE0`. The *claim* about slot 5 is correct of the real address, so this is a citation
error, not a reading error.

**3 + 4. Slots 23/24 were read from a DIFFERENT VTABLE — and that one mix-up explains the folding
claim too.** §3 gave slots 23/24 as `0079D560`/`0079D5B0`. Those sit at `0x01CB25C0`/`0x01CB25C8`,
which are **slots 23 and 24 of the vtable at `0x01CB2508`**. The slot *numbers* were right; the
vtable was not. GameApplication's own 23/24 are `0017CDF0`/`0017CE20`.

**`0x01CB2508` is `GameApplication`'s BASE CLASS vtable**, proven from the destructor chain:
`0x00793250`, called from slot 0 right after this class's vtable is installed, writes `0x01CB2508`
into `[this + 0]`. Installing a different vtable at offset 0 during destruction is what a base
destructor does.

That base vtable also has **31 slots**, and **all 10 non-stub slots this class does not override
appear in it at identical indices** — 1, 12, 13, 17, 18, 19, 20, 28, 29, 30. **Identical indices
across two vtables is inheritance; `/OPT:ICF` folding would place a shared body at arbitrary,
unrelated indices.** So §7's *"13 of the 31 slots are folded with other classes and absent from this
analysis entirely"* is wrong in mechanism: **10 are inherited and fully visible in the base vtable**;
only 3 are genuine stubs. **BE-3 answered in substance**, with the base's own identity opened as
**BE-5**.

**5. `+0x1138` is not the highest field, and §2 already said so.** §2 documents `+0x113C` and
`+0x113D` at length; §3 then states the highest field observed is `+0x1138`. **The document
contradicted itself in two sections a reader would not compare** — the *third* instance of that shape
today, after `character-render-object.md`'s *12 of 12 / 13 reads* and the interpreter's *ANSWERED /
not established*. Here it was load-bearing: the `≥ 0x1140` bound was derived from `+0x1138`, and
`+0x113D` reaches the same bound only by alignment coincidence.

**6. BE-1 ANSWERED — slot 4 is the frame tick.** It gates on the latch, converts a double at
`this + 0x48` to a float, publishes it, runs a one-shot initialiser behind `+0x113D`, and calls
**`0x0017D6E0`** on **all three** exit paths with that double in `xmm0` and a mode in `edx`.
`0x0017D6E0` is 404 B, tagged `CoreRuntimeScheduling`, with **37 callees of which 16 are 8–10 byte
singleton getters**, each paired with a substantial update body. The one pair whose names are
recovered fixes the pattern:

```
001C18E0  SaveloadManager_GetSingleton                (8 B)
001C1910  SaveloadManager_ProcessPendingCaptureCopy  (43 B)
```

**`0x0017D6E0` is the per-frame subsystem pump: for each subsystem, fetch its singleton and advance
it.** Opened **BE-6** for the other fifteen — they name the engine's per-frame subsystem set.

## WHAT SURVIVED

- **31 vtable slots** ✓ — slot 31 onward is the ASCII `'../../..'`.
- **18 uniquely owned / 13 shared** ✓ **exactly**, by an image-wide qword-reference census.
- **The `+0x113C` latch: 1 write, 3 reads, image-wide** ✓ **exactly**, and the byte offsets
  **+116, +6, +39, +4** all reproduce. Better than the render-object latch: **no other structure in
  the binary has a field at `+0x113C`**, so this claim needs no type-scoping caveat.
- **`+0x113D` is method-local** ✓ — 2 accesses, both inside slot 4, 19 bytes apart.
- **Slot 2 mounts the VBF** ✓ — `'../../..'` at `008C5858`, `'../FFXII_TZA.vbf'` at `008C5868`. Two
  further authored paths sit immediately after: **`.\\GameData\\code_steam.txt`** and
  **`.\\GameData\\data.txt`**.
- **Slot 5 is an explicitly empty override** ✓ in substance (right shape, wrong address).

**The latch — this document's centrepiece — survived every attack exactly, including all four byte
offsets.** So did both structural counts.

## HOW THE TWO BAD ROWS BECAME VISIBLE

I **located the vtable independently** instead of taking any slot address on trust: searched the
image for slot 2's address as a qword, found exactly one occurrence, and confirmed the base by
checking that four separately documented slots (2, 4, 7, 8) land on their stated indices. They did.
**Slots 5, 23 and 24 did not** — which is what exposed them. The document never stated the vtable
address at all; it does now (`0x008C5760`).

## A BOUNDED NEGATIVE FOR repos-f1's WORKBENCH

You asked whether this document's scheduler reaches the `0x022D91B0` argument-passing area. **It does
not, at one hop or two.**

```
functions touching 022D91B0..+0x400         : 247
slot 4 (0017CCD0)                           : no
its target 0017D6E0                         : no
any of the 22 GameApplication vtable bodies : no
the tick's 37 hop-1 callees                 : none
the tick's 109 hop-2 callees                : none
```

**The two documents should not cite each other on this basis.** If the workbench is reached from the
application root at all, it is deeper than two calls, and nothing here establishes that it is.

## YOUR NEW CHECKER JUST CAUGHT A FALSE DISAGREEMENT — AND IT IS THE ARTEFACT I FLAGGED

`check_consistency.py` now reports a `00313F60` disagreement across **three** documents:

```
47 callers   24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md
65 callers   00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md
65 callers   03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md
```

**All three documents are correct and none of them says what the checker reports.** Both "65"s come
from `COUNT_PATTERNS[1]`, the backward search, reading sentences in which **65 belongs to
`00377C20`** and `00313F60` merely happens to be the nearest address within the following 40
characters:

```
"...`00377C20` with 65 callers and `00313F60` with 47."           -> extracts 00313F60 = 65
"...`00377C20` with 13 subsystems / 65 callers and `00313F60`..." -> extracts 00313F60 = 65
```

This is artefact (b) from block 2, which I said was *"harmless there; it would not be if those
figures were compared against another document."* **A third document has now stated the thunk's 47
correctly, and the comparison fires.** A false disagreement is worse than a missed one — it costs
whoever picks it up a full re-derivation of something already settled.

**Suggested fix, and you already applied its logic today:** reject a `COUNT_PATTERNS[1]` match when
another 8-hex address appears between the number and the matched address, because the number's owner
is then ambiguous. That is exactly the rule
`check_answered_not_established.py` had to learn — *ambiguity must be judged over all ids in the
window, not just the one you matched.*

## OPEN-QUESTIONS

| ID | Status | Note |
|---|---|---|
| **BE-1** | **ANSWERED** | Slot 4 is the frame tick; `0x0017D6E0` is the per-frame subsystem pump, 37 callees, 16 singleton getters. |
| **BE-3** | **ANSWERED in substance** | 10 of the 13 are **inherited** from the base vtable `0x01CB2508` at identical indices, fully visible there; only 3 are `/OPT:ICF` stubs. |
| **BE-4** | **ANSWERED** | **`0x1140` = 4,416 bytes**, stated by the sized `operator delete` in slot 0. |
| **BE-2** | still OPEN, **and now weaker** | The addresses in §3 were wrong; the real pairs are `0017CFD0`/`0017D170` and `0017CDF0`/`0017CE20`, and **the shared-target claim has not been re-tested against the corrected addresses.** |
| `PROPOSED-repos46-13` (suggest **BE-5**) | new | What the base class at vtable `0x01CB2508` is. 31 slots, supplies 10 of this class's, sits among the input-device vtables in `.rdata`. |
| `PROPOSED-repos46-14` (suggest **BE-6**) | new | The 16 singleton getters the tick pumps. Only `SaveloadManager` is recovered; the other fifteen name the engine's per-frame subsystem set. |

## AUDIT-LOG

Suggested pass 135.

---

### 2026-09-02 - pass 135: the application root has a destructor, a size and a base class, and one bad row explained three wrong claims

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `00-Engine-Core-Runtime/Application-Root/game-application.md` (+ section 10; headline,
sections 3, 4, 5 and 7 rewritten); OPEN-QUESTIONS BE-1 BE-3 BE-4 answered, BE-2 weakened, BE-5 BE-6
opened
**Tool run:** vtable located and read directly out of the PE image; capstone over the class's bodies
with clamped extents; `+0x113C`/`+0x113D` displacement scans across all 38,161 functions; an
image-wide qword-reference census for all 31 slot pointers

**THE APPLICATION ROOT IS `0x1140` = 4,416 BYTES, AND THE CODE SAYS SO.** Section 4 argued that
because the root is never deleted, no sized `operator delete` exists to state its size. **Slot 0 is a
scalar deleting destructor** and its sized path carries `mov edx, 0x1140`. *The reasoning was sound
and its premise was unchecked:* a C++ compiler emits the deleting destructor for any polymorphic
class whether or not the program calls it. **"This never happens at runtime" does not predict "the
code is not there."** The size immediate was claimed and the **callee deliberately was not** -
`0x0016D6A0` is a 3-byte `ret` with 2,480 callers, an ICF fold that proves nothing about deletion.

**ONE BAD ROW EXPLAINED THREE WRONG CLAIMS.** Section 3 listed slots 23/24 as `0079D560`/`0079D5B0`.
Those are **slots 23 and 24 of a different vtable** - `0x01CB2508`, which the destructor chain proves
is **`GameApplication`'s base class** (`0x00793250` writes it into `[this + 0]`). The slot numbers
were right and the vtable was not. **That single mix-up also explains the "13 folded" reading:** ten
of the thirteen non-overridden slots sit in that base vtable **at identical indices**, which is
inheritance, not folding. Reading some rows from the derived vtable and some from the base makes
inherited slots look like they belong to unrelated classes.

**A GHOST ADDRESS AND A SELF-CONTRADICTION.** Slot 5 was published as `0017CE40`, which is not a
function - it is a **mid-body address inside slot 24**. And section 3's *"highest field observed
`+0x1138`"* is contradicted by **section 2 of the same document**, which documents `+0x113C` and
`+0x113D` at length. **Third instance today of a document disagreeing with itself in two places no
reader would compare**, and the first where it was load-bearing: the object-size lower bound was
derived from the wrong field.

**BE-1 ANSWERED.** Slot 4 gates on the latch, converts a double at `this + 0x48`, and calls
`0x0017D6E0` on all three exit paths. That function is 404 B, `CoreRuntimeScheduling`, with **37
callees of which 16 are 8-10 byte singleton getters** each paired with a substantial update body -
`SaveloadManager_GetSingleton` / `SaveloadManager_ProcessPendingCaptureCopy` is the one recovered
pair and fixes the pattern. **Slot 4 is the frame tick and `0x0017D6E0` is the per-frame subsystem
pump.**

**WHAT SURVIVED, EXACTLY.** The `+0x113C` latch - 1 write, 3 reads, image-wide, at byte offsets
**+116, +6, +39, +4**, all four reproduced - and it is **cleaner than the render-object latch**,
because no other structure in the binary has a field at that offset, so it needs no type-scoping
caveat. Both structural counts (31 slots; 18 owned / 13 shared) reproduced exactly. The VBF strings
reproduced, with two further authored paths beside them.

**HOW THE BAD ROWS BECAME VISIBLE:** the vtable was **located independently** rather than taken on
trust - found by searching the image for slot 2's address, then confirmed by four separately
documented slots landing on their stated indices. Four landed; three did not. **A document that cites
slot numbers without citing the vtable cannot be checked**, and this one did not state its vtable
address until this pass.

---

## CALL-CHAINS / ADDRESS-INDEX

| From | To | Kind | Note |
|---|---|---|---|
| `GameApplication` slot 4 `0017CCD0` | `0017D6E0` | **owner transition** | the frame tick to the per-frame pump |
| `0017D6E0` | 16 subsystem singletons | trigger | each getter paired with an update body |
| `0017D6E0` | `SaveloadManager_GetSingleton` / `_ProcessPendingCaptureCopy` | **owner transition** | the one recovered pair |
| `GameApplication` slot 0 | base destructor `00793250` | lifecycle | installs base vtable `01CB2508` at `[this]` |
| `GameApplication` vtable `008C5760` | base vtable `01CB2508` | **inheritance** | 10 slots inherited at identical indices |

| Address | Name | Body | Note |
|---|---|---|---|
| `0017D6E0` | the per-frame subsystem pump | 404 bytes | `CoreRuntimeScheduling`; BE-1 |
| `00793250` | `GameApplication` base destructor | 353 bytes | installs `01CB2508` |
| `0017CC70` | `GameApplication` scalar deleting destructor | 92 bytes | states `0x1140` |

Data addresses, no size column: `008C5760` GameApplication vtable · `01CB2508` its base class
vtable · `008C5858` `'../../..'` · `008C5868` `'../FFXII_TZA.vbf'` · `008C5888`
`'.\\GameData\\code_steam.txt'` · `008C58A8` `'.\\GameData\\data.txt'`.

---
---

# BLOCK 6 — BE-5 answered, BE-6 half answered, and a name/address transposition in a new document

Same program state. Read-only against the GZF; no `Apply-*`, no `Pack-*`, no `_index/*.md` edits.

## COVERAGE

| Document | Change |
|---|---|
| `00-Engine-Core-Runtime/Application-Root/game-application.md` | §11 added; headline, §4, §7 and §9 amended; `audit.passes` 2 → 3 |

`check_links.py` — **176 files, 865 links, all resolve.**
`check_consistency.py` — **CALLER-COUNT back to 0** (your fix works), and it has produced its **first
true positive** — see the last section.

## BE-5 ANSWERED — the application root is a PhyreEngine application

`0x01CB2508 - 8` is a complete-object locator whose type descriptor reads
**`.?AVPApplication@PFramework@Phyre@@`**. `GameApplication`'s own class-hierarchy descriptor gives
the chain:

```
GameApplication  :  Phyre::PFramework::PApplication  :  Phyre::PBase  :  Phyre::PMemoryBase
                    mdisp 0                             mdisp 8         mdisp 8
```

**Two independent derivations agree and neither used the other.** Block 5 concluded from the
*destructor chain* that `0x01CB2508` is the primary base's vtable, because `0x00793250` writes it to
`[this + 0]`. RTTI independently says `mdisp = 0`, which means exactly that.

**Your neighbourhood question — the second hypothesis is right.** Naming every vtable in
`0x01CB2400`–`0x01CB2800` gives twelve classes and **all twelve are `Phyre::PFramework`**:

```
PInputDeviceKeyboard · PWindowWin32Base · PWindow · PApplicationScriptBuffer ·
PApplicationScript · PApplicationScriptProxy · PInputDevicePad · PApplication ·
PApplicationViewport · PInputDevicePadDirectInput · PInputDevicePadXInput ·
PInputDevicePadSteamController
```

So the base is a **generic middleware framework object**, and the input devices sit beside it because
they are framework classes too — **not** because they share ancestry with the application root. The
neighbourhood was a `.rdata` locality artefact of PhyreEngine's own vtables, nothing more.

**What that makes `GameApplication`:** the game's subclass of PhyreEngine's application class,
supplying 18 of 31 virtual methods and inheriting 10. **The frame tick, the VBF mount and the startup
latch are all game code overriding middleware entry points** — which is a cleaner statement of the
game/middleware boundary than anything currently in the database.

Incidental but player-facing: **`PInputDevicePadSteamController`** is a shipped input-device class.

## BE-6 HALF ANSWERED — the per-frame subsystem set

The tick pumps **13** lazily-constructed singletons (not 16 — three of the small callees are not
getters). Each follows one shape: a global pointer, an `Ensure` that allocates a fixed size and
constructs on first use, and an 8-byte getter the tick calls.

| global | `Ensure` | object size | class |
|---|---|---:|---|
| `01F810F8` | `0019A0A0` | `0x158` | **`AsyncJobManager`** |
| `01F81160` | `001A11B0` | — | **`AsyncLoadManager`** |
| `01F81218` | `001B7EE0` | `0xBB8` | **`Phyre::PCameraPerspective`** |
| `01F81260` | `001C18A0` | `0xA78` | **`SaveloadManager`** |
| `01F81270` | `001C2F00` | `0x4670` | **`MultipleDebugDisplay`** |
| `01F7F598` | `00189000` | `0xDD8` | no vtable |
| `01F810F0` | `00199790` | — | no vtable |
| `01F81168` | `001A98B0` | `0xA0` | no vtable |
| `01F81240` | `001BBFC0` | `0x238` | no vtable |
| `01F81248` | `001BDA50` | `0x108` | no vtable |
| `01F81258` | `001C0D40` | `0x1B8` | no vtable |
| `01F82CE0` | `001D8CD0` | `0x38` | no vtable |
| `01F82D30` | `001E0550` | — | no vtable |

**Positive control:** `SaveloadManager` was already named in the ledger, and the method recovered it
**from the global alone**, blind. That is why the other four are reported.

**One candidate rejected, and the control is what made it visible.** `01F81168` first resolved to
`.?AVallocator@eastl@@`. Its `Ensure` allocates `0xA0` bytes and calls an EASTL container
constructor, so that vtable is **construction machinery the constructor touched, not the class of the
object stored in the global**. *Reading a vtable within one hop of an allocation is not the same as
reading the object's vtable* — and had `SaveloadManager` also come back as a container type, the
method would have been unusable rather than merely noisy.

**Eight of thirteen have no vtable at all** — a bounded negative, not a failure to look. Non-polymorphic
singletons carry no RTTI, so those eight need strings, call-site context or authored data. **BE-6
stays open for them.**

## check_consistency.py's FIRST TRUE POSITIVE — and it is a transposition, not a typo

One merge after your backward-search fix, the checker found a real defect:

```
002E5380
   Movement_IntegratePositionAndMeasureDisplacement
       06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md
   Movement_PrepareCandidatePosition
       06-Movement-And-Navigation/heading-speed-to-position-delta.md
```

**The new document has the address and size from one function and the name and the behavioural claim
from another.** Its row reads `| 002E5380 | Movement_IntegratePositionAndMeasureDisplacement | 273 B
| consumer; calls the 3-D selector |`, and its §5 chain repeats the pairing.

The binary:

```
002E5380  Movement_PrepareCandidatePosition                 273 B   calls FUN_00264460 : NO
002E5610  Movement_IntegratePositionAndMeasureDisplacement  314 B   calls FUN_00264460 : YES
002E54A0  Movement_TransformAndAccumulateCandidate          282 B   calls FUN_00264460 : NO
```

**The name and the behavioural claim are mutually consistent and both point at `002E5610`; the
address and the body size are both `002E5380`'s.** So the row is not a mislabel — two different rows
of source data were combined. The fix is to change the address to `002E5610` and the size to 314 B,
**not** to change the name.

Flagging rather than fixing: it is not my document, even though it is in a category I have been
working. Worth noting for the owner that the *body size* travelled with the wrong address, so a
size-based check would not have caught it — **only the name/address pairing did**, which is precisely
what your checker compares.

## OPEN-QUESTIONS

| ID | Status | Note |
|---|---|---|
| **BE-5** | **ANSWERED** | `Phyre::PFramework::PApplication`, with `Phyre::PBase` / `PMemoryBase` above it. Neighbourhood is the framework's vtable region; input devices are siblings. |
| **BE-6** | **PARTLY ANSWERED** | 13 singletons, not 16. Five named by RTTI; eight are non-polymorphic and need another route. |

### Propagation

**`22-Middleware-PhyreEngine/` should reopen.** `GameApplication` deriving from
`Phyre::PFramework::PApplication` means the application root is a middleware subclass, and the
PhyreEngine documents do not currently say so. The twelve-class `PFramework` vtable cluster is
enumerated in §11 and is theirs to absorb.

## AUDIT-LOG

Suggested pass 136.

---

### 2026-09-02 - pass 136: the application root is a PhyreEngine subclass, and a positive control rejected a name

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `00-Engine-Core-Runtime/Application-Root/game-application.md` (+ section 11; headline,
sections 4, 7, 9 amended); OPEN-QUESTIONS BE-5 answered, BE-6 partly answered
**Tool run:** MSVC RTTI read directly out of the image - complete-object locators at `vtable - 8`,
type descriptors and class-hierarchy descriptors - plus the singleton census from pass 135

**FFXII's APPLICATION ROOT IS A PHYRENGINE APPLICATION.** `GameApplication :
Phyre::PFramework::PApplication : Phyre::PBase : Phyre::PMemoryBase`, read from the class-hierarchy
descriptor. **Two independent derivations agree and neither used the other:** pass 135 concluded from
the *destructor chain* that `0x01CB2508` is the primary base's vtable because `0x00793250` writes it
to `[this + 0]`; RTTI independently reports `mdisp = 0`, which means exactly that. **The frame tick,
the VBF mount and the startup latch are all game code overriding middleware entry points.**

**THE SURPRISING NEIGHBOURHOOD WAS NOT A FINDING.** Pass 135 noted the base sits among input-device
vtables and left open whether that was meaningful. Naming every vtable in `0x01CB2400`-`0x01CB2800`
gives **twelve classes, all of them `Phyre::PFramework`** - window, viewport, the application-script
trio and five input devices. The base is a generic middleware object and the input devices are
**siblings, not relatives**; the neighbourhood was `.rdata` locality of PhyreEngine's own vtables.
*A cluster of related-looking things around a target is a fact about the linker's layout until
something says otherwise.*

**BE-6 HALF ANSWERED, AND THE POSITIVE CONTROL EARNED ITS PLACE.** The tick pumps **13** lazily
constructed singletons; five are named from RTTI - `AsyncJobManager`, `AsyncLoadManager`,
`Phyre::PCameraPerspective`, `SaveloadManager`, `MultipleDebugDisplay` - and **eight have no vtable at
all**, a bounded negative rather than a failure to look. `SaveloadManager` was already named in the
ledger and the method recovered it **from the global alone, blind**, which is why the other four are
reported. **One candidate was rejected because of that control:** `01F81168` resolved to
`.?AVallocator@eastl@@`, which is the container machinery its constructor touched, not the class
stored in the global. *Reading a vtable within one hop of an allocation is not reading the object's
vtable* - and without a control that returned a known-correct answer, the difference would have been
invisible.

**check_consistency.py's FIRST TRUE POSITIVE, ONE MERGE AFTER THE FALSE-POSITIVE FIX.** A new
movement document pairs `002E5380` with the name `Movement_IntegratePositionAndMeasureDisplacement`
and the claim *"calls the 3-D selector"*. The binary: `002E5380` is `Movement_PrepareCandidatePosition`
(273 B) and **does not** call `FUN_00264460`; `002E5610` (314 B) **does**. The name and the
behavioural claim are mutually consistent and both point at `002E5610`, while the address **and the
body size** are `002E5380`'s. **Two rows of source data were combined, not one label mistyped** - and
because the size travelled with the wrong address, a size check would not have caught it. **Only the
name/address pairing did.**

---

## CALL-CHAINS / ADDRESS-INDEX

| From | To | Kind | Note |
|---|---|---|---|
| `GameApplication` | `Phyre::PFramework::PApplication` | **inheritance** | primary base, `mdisp 0`, 10 of 31 slots |
| `PApplication` | `Phyre::PBase` → `Phyre::PMemoryBase` | inheritance | `mdisp 8` |
| slot 4 tick `0017D6E0` | 13 lazily-constructed singletons | trigger | 5 named, 8 non-polymorphic |

Data addresses, no size column: `01CB2508` `Phyre::PFramework::PApplication` vtable · `01D3E310` its
complete-object locator · `01CB2430`/`2468`/`2480`/`2498`/`24A8`/`24B8`/`24C8`/`2608`/`2638`/`2678`/`26B8`
the other eleven `PFramework` vtables · `01F810F8`/`01F81160`/`01F81218`/`01F81260`/`01F81270` the five
named singleton globals.

---
---

# BLOCK 7 — BE-6: eight instruments, seven dead ends, one more name, thirteen characterised

Same program state. Read-only against the GZF; no `Apply-*`, no `Pack-*`, no `_index/*.md` edits.

## COVERAGE

| Document | Change |
|---|---|
| `00-Engine-Core-Runtime/Application-Root/game-application.md` | §11 extended — the singleton table rebuilt with update functions and behavioural identities; the instrument-failure table added; `audit.passes` 3 → 4 |

`check_links.py` **177 / 878, all resolve** · `check_consistency.py` **clean** · `progress` **43.99 %**.

## ONE MORE NAME, AND IT IS PLAYER-FACING: `ScreenImage`

`0x01F82CE0`'s update calls the engine's **named-scope push with an authored label**:

```c
FUN_001eb150("ScreenImage");    // the SAME scope-push that pushes the
FUN_001d8bb0(this);             // "display character : ..." labels from block 2
FUN_001eb110();
```

and the body is a fade ramp:

```
if (this[0x00] == 0) return;                  // disabled -> nothing
mode = this[0x10]
if (mode == 0)  this[0x1C] += this[0x20]      // ramp one way
if (mode == 1)  this[0x1C] -= this[0x20]      // ramp the other
if (mode == 0 && this[0x0C] >= this[0x14] && this[0x1C] > threshold)
        this[0x1C] = 255.0                    // clamp
```

`Ensure` constructs it disabled with `mode = 3`, which the update ignores — idle. **A level ramping
between 0 and 255 at a per-frame step, with an up mode and a down mode, is a screen fade.** This is
the object behind the screen going to and from black on area transitions and event boundaries — and
it is one of the thirteen things the application root pumps every frame.

Evidence tier 2 (authored string), not 4 — but for *naming* that is the stronger of the two, because
the engine wrote the name itself.

## SEVEN INSTRUMENTS FAILED, AND I TESTED EACH AGAINST KNOWN ANSWERS FIRST

Your caution — *check that the answer has the shape the question implies* — is what shaped this
block. Every instrument was run against the **five already-named singletons as controls before**
being pointed at the eight unknowns:

| instrument | result against the known singletons |
|---|---|
| strings referenced by `Ensure`/update, depth 1 | EASTL allocator tags or nothing — **fails** |
| named callees of the update, depth 1 | 1 of 3 gives a thematic hint, 2 give nothing — **fails** |
| named callees of the update, depth 2 | **`vpx_codec_destroy` for `PCameraPerspective`** — **actively misleading** |
| named callers of the getter | 1 of 3 gives a thematic hint — **fails** |
| named functions touching the global | only the already-named ones — **circular** |
| allocator tag string at the `Ensure` | none passes one — **fails** |
| a master function walking the singleton block | no such function exists — **fails** |
| **authored profiler scope labels** | **works — named `ScreenImage`** |

**The depth-2 row is the one worth keeping.** It would have named a *camera* singleton after a **VP8
video codec teardown function**. Had I not run controls first, that is a name I could have published
with a straight face, sourced from a real call edge.

**And the winning instrument fires exactly once in thirteen** — which is the shape a sound scan
should have. A label scan that returned a name for all thirteen would have been reporting its own
noise, which is precisely the failure `repos-94` hit.

**A nuance worth recording about controls:** the profiler-label instrument *also* "fails" the
control — `SaveloadManager`'s update carries no label. That does not condemn it. **A positive
instrument with no false positives cannot be validated by a control that has nothing to find**; what
validates it is that its one hit is an authored string, in the right place, corroborated by the body
it wraps. Controls disprove instruments that *invent* answers; they cannot disprove one that is
merely silent.

## ALL THIRTEEN NOW CHARACTERISED

Six named; the other seven identified by what their update actually does:

| global | size | identity |
|---|---:|---|
| `01F810F8` | `0x158` | **`AsyncJobManager`** |
| `01F81160` | — | **`AsyncLoadManager`** |
| `01F81218` | `0xBB8` | **`Phyre::PCameraPerspective`** |
| `01F81260` | `0xA78` | **`SaveloadManager`** |
| `01F81270` | `0x4670` | **`MultipleDebugDisplay`** |
| `01F82CE0` | `0x38` | **`ScreenImage`** — the screen fade |
| `01F7F598` | `0xDD8` | pumped **three times per tick**, with two different update bodies — the only one pumped more than once, so its ordering is load-bearing |
| `01F81248` | `0x108` | a **pending-completion queue** — walks an intrusive list, calls `vtable+0x18` on each node, unlinks those returning non-zero; gated off entirely while `FUN_0017d980()` is non-zero |
| `01F82D30` | — | an **end-of-frame reset** — fetches several *other* singletons, finishes each, zeroes two bytes of its own state; consistent with being the last getter in the tick |
| `01F81258` | `0x1B8` | a **one-shot latch** — does its work once behind a condition and sets a byte so it never runs again |
| `01F81240` | `0x238` | unnamed; largest update body at 1,828 B |
| `01F81168` | `0xA0` | unnamed |
| `01F810F0` | — | unnamed |

**BE-6 stays open for the seven.** They are non-polymorphic, carry no authored label, and defeated
seven instruments; naming them needs runtime evidence or authored data from outside the executable.
That is a bounded negative with the boundary stated, not an unfinished search.

## OPEN-QUESTIONS

| ID | Status | Note |
|---|---|---|
| **BE-6** | still open, **6 of 13 named, 13 of 13 characterised** | Seven remain; the eight instruments tried and their control results are in §11 so nobody repeats them. |

## AUDIT-LOG

Suggested pass 137.

---

### 2026-09-02 - pass 137: the screen fade named by the engine itself, and seven instruments that could not name the rest

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `00-Engine-Core-Runtime/Application-Root/game-application.md` (section 11 extended);
OPEN-QUESTIONS BE-6 advanced
**Tool run:** eight naming instruments, each validated against the five already-named singletons
before use; 18 bodies decompiled

**THE SCREEN FADE IS ONE OF THE THIRTEEN THINGS THE APPLICATION ROOT PUMPS EVERY FRAME.**
`0x01F82CE0`'s update wraps itself in the engine's named-scope push with the authored label
**`"ScreenImage"`** - the same `FUN_001EB150` that pushes the `"display character : ..."` labels -
and its body ramps a level at `+0x1C` by `+0x20` per frame, up in mode 0 and down in mode 1, clamped
at **255.0**, constructed disabled with an idle mode. **A 0-255 level with an up mode and a down mode
is a screen fade**, and this is the object behind the screen going to and from black.

**SEVEN INSTRUMENTS FAILED, AND EACH WAS TESTED ON KNOWN ANSWERS FIRST.** Strings at depth 1, named
callees at depth 1 and 2, named callers of the getter, named touchers of the global, allocator tag
strings, and a master walker over the singleton block - all run against the five RTTI-named
singletons as controls before being pointed at the eight unknowns. **The depth-2 callee scan would
have named `PCameraPerspective` after `vpx_codec_destroy`** - a VP8 codec teardown, reached by a real
call edge. *Without controls that is a name that could have been published with a straight face.*

**THE WINNING INSTRUMENT FIRES ONCE IN THIRTEEN, WHICH IS THE RIGHT SHAPE.** A label scan returning a
name for all thirteen would have been reporting its own noise.

> **A nuance about controls, worth its own line.** The profiler-label instrument *also* returns
> nothing for the controls, because those subsystems carry no label. **That does not condemn it. A
> positive instrument with no false positives cannot be validated by a control that has nothing to
> find** - what validates it is that its single hit is an authored string, in the right place,
> corroborated by the body it wraps. **Controls disprove instruments that invent answers; they cannot
> disprove one that is merely silent.**

**ALL THIRTEEN ARE NOW CHARACTERISED EVEN WHERE UNNAMED:** one is pumped **three times per tick** with
two different update bodies and is the only one pumped more than once; one is a **pending-completion
queue** polling `vtable+0x18` on an intrusive list; one is an **end-of-frame reset** that finishes
other singletons; one is a **one-shot latch**, not a per-frame update at all. **BE-6 stays open for
seven**, with the boundary stated: they need runtime or authored evidence from outside the
executable.

---

## CALL-CHAINS / ADDRESS-INDEX

| Address | Role | Evidence |
|---|---|---|
| `001EB150` / `001EB110` | the engine's **named profiler scope** push / pop | authored labels at two independent call sites |
| `001D9080` | `ScreenImage` per-frame fade update | authored label + body |
| `001D8CD0` | `ScreenImage` `Ensure` — constructs disabled, mode 3 | body |
| `001BDAC0` | pending-completion queue pump | body |
| `001E0590` | end-of-frame reset | body |

Data addresses, no size column: `01F82CE0` the `ScreenImage` singleton pointer · the twelve other
singleton globals listed in §11.

---
---

# BLOCK 8 — `persistent-flag-banks.md`, first falsification pass

Same program state. Read-only against the GZF; no `Apply-*`, no `Pack-*`, no `_index/*.md` edits.

## COVERAGE

| Document | Change |
|---|---|
| `14-Story-Event-Quest-Hunt/persistent-flag-banks.md` | **first falsification pass** — §10 added; §2 substantially extended, §4 and §4b added, §5 extended, AA-6 opened; `audit.passes` 1 → 2 |

`check_links.py` **180 / 903, all resolve.** `check_consistency.py` — 9 NAME disagreements, **none of
them mine**; see the last section.

Please move its row out of *Now owed instead*.

## NOTHING IN THE BANK MECHANICS BROKE — and I attacked the right thing

The five bank offsets, their sizes, the bit arithmetic, the range guards, the reserved ids `0`/`1`
and all **fifteen rows** of §3's address table reproduced **exactly**, re-derived by censusing every
caller of `SaveImage_GetPersistentPayloadBase` (70 of them) with a base-tracking displacement scan.

**The attack most likely to succeed was aimed by the engine's own naming, and it failed.** Two
functions are called **`WorldPersistence_ResetBanksAndMarkInitializationState`** and
**`WorldPersistence_ResetBanksForFieldTransition`**. If either cleared a flag bank, §1's *"set once
and remembered"* — the document's whole irreversibility claim, and the reason story progress works
the way it does — would fall. **Neither touches a bank:** tracked through the payload base,
`00268320` writes exactly one byte (`+0x1061`) and `0026DB30` tests exactly one (`+0x1062`), both in
the world-transition cluster, nowhere near `+0x1384`–`+0x1533`. **"Banks" in those names is not these
banks.**

## THE BIG FIND: the other half of the gate is not a flag lookup at all

The document said bit 14 of an encoded id chooses "the authored threshold schedule" and stopped
there. Reading `00377970` shows **that half leaves the save system entirely**:

```c
off = table[10 + index*2];  if (!off) return false;
v = FieldData_GetVariable0();           // the field's authored progress variable, NOT a flag
result = false;
for (;;) {
    entry = *p;
    if ((short)v < (entry & 0x7FFF)) return result;   // below this threshold: stop
    p++;  result = !result;                            // TOGGLE at every crossing
    if ((short)entry < 0) return result;               // bit 15 = last entry
}
```

**The answer is the parity of how many authored thresholds the progress variable has passed.** Each
entry is a `u16` — bits 0-14 a threshold, bit 15 the end marker.

**So an authored condition can be true only *between* two story points** — on at the first threshold,
off at the second, on again at the third. **A flag cannot express that, because a flag never goes
back.** That is the mechanism behind a line of dialogue or an event that is live for one stretch of
the game and gone afterwards, and it is why the engine needs both halves of the gate.

`FieldData_GetVariable0` (`00265270`, 22 callers) is the first `u16` of the current field's authored
variable block, `0` when absent.

**`0xFFFF` is a sentinel and nine call sites use it** — bit 14 set, index `0x3FFF` = 16,383, beyond
any plausible entry count when every index actually observed is `<= 0x67`. It returns **false**.
Whether a caller reads that as "never" or "absent" depends on its polarity and is **not** asserted.

**The observed id vocabulary**, harvested from the gate's 32 call sites:

```
threshold queries    0x4004 0x4006 0x4007 0x4008 0x4009 0x400A 0x400B 0x400C
                     0x400D 0x4010 0x4011 0x4067  and the sentinel 0xFFFF
Primary bank reads   0x0001 0x0002 0x0054 0x005E 0x006F 0x0107
```

## TWO SMALLER CORRECTIONS

**The payload map was one field short.** Primary ends at `+0x1533` and the map stopped there.
**`+0x1534` has six access sites** (`ActorManager_RunFieldRuntimePass` among them) and `+0x1535` is
reached through the raw buffer accessor. Opened as **AA-6**.

**The gate has 32 callers, not the one documented** — including two five-byte thunks §3 does not
list, and **`InputGameplay_ArbitrateDigitalInputAndModalState`**. Story flags participate in input
arbitration, which is a cross-subsystem relationship the document did not carry.

## AA-5's GAP SURVIVES, AND I CHECKED THE ESCAPE ROUTE

The 32-byte gap at `+0x1394` has **no accessor** — but an absence claim about a memory range is only
as good as the enumeration of ways to reach it, and there were **two**. The payload base is
`rawBuffer + 0x200`, so the accessor can be bypassed entirely. That bypass has **28 callers and 36
displacements, none of them in the gap.**

**Limit stated rather than assumed away:** neither census would see a payload pointer stored to
memory and read back later, nor a bulk `memcpy` over the whole payload — the same two-hop bound as
audit pass 129.

## NINE `check_consistency.py` NAME DISAGREEMENTS — NONE MINE, BUT ONE I CAN SETTLE

Eight are between two new `18-Audio/Audio-Boundary/` documents naming the same eight addresses
differently — `repos-78`'s to resolve.

**The ninth I have direct evidence on:**

```
0016D6A0
   ICF_FoldedRetStub     18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md
   _guard_check_icall    24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/...
   _guard_check_icall    24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/...
```

**The audio document's name is the correct one.** `0016D6A0` is three bytes — `ret 0` — with **2,480
callers**. In block 5 I found `GameApplication`'s deleting destructor calling it as a **sized
`operator delete`**, with `mov edx, 0x1140` as the size argument. A stubbed CFG check and a stubbed
sized delete are both a bare `ret`, so `/OPT:ICF` merged them. **`_guard_check_icall` asserts one of
its roles as its identity**; `ICF_FoldedRetStub` describes what it actually is. The category-24
documents should adopt the audio name or qualify theirs.

Flagging, not fixing — none of the three is mine.

## OPEN-QUESTIONS

| ID | Status | Note |
|---|---|---|
| **AA-5** | still open, **strengthened** | The gap survives a two-route census; the bound on both censuses is stated. |
| `PROPOSED-repos46-15` (suggest **AA-6**) | new | The live field at payload `+0x1534`/`+0x1535`, immediately after Primary. |

## AUDIT-LOG

Suggested pass 138.

---

### 2026-09-02 - pass 138: a story condition that can switch off again, and two functions named to look guilty

**Program state:** snapshot `46f02e26...` - parent `2ed8affb...` - ledger 38,003 / 158, verified
**Scope:** `14-Story-Event-Quest-Hunt/persistent-flag-banks.md` (+ section 10; sections 2, 4, 4b, 5
extended); OPEN-QUESTIONS AA-5 strengthened, AA-6 opened
**Tool run:** base-tracking displacement census over all 70 callers of the payload accessor **and**
all 28 callers of the raw buffer accessor beneath it; exact call-site census; six bodies decompiled

**THE OTHER HALF OF THE FLAG GATE IS NOT A FLAG LOOKUP.** Bit 14 of an encoded id was documented as
choosing "the authored threshold schedule"; the body shows it **leaves the save system entirely**.
It walks authored `u16` thresholds against `FieldData_GetVariable0()` and **toggles** the answer at
each one passed, bit 15 marking the last entry. **The answer is a parity**, so an authored condition
can be true *only between two story points* - which a flag cannot express, because a flag never goes
back. That is the mechanism behind an event or a line of dialogue that is live for one stretch of the
game and gone afterwards.

**`0xFFFF` IS A SENTINEL AND NINE CALL SITES USE IT** - index `0x3FFF` against a table whose every
observed index is `<= 0x67`.

**THE ATTACK MOST LIKELY TO SUCCEED WAS AIMED BY THE ENGINE'S OWN NAMING, AND IT FAILED.**
`WorldPersistence_ResetBanksAndMarkInitializationState` and
`WorldPersistence_ResetBanksForFieldTransition` would, if either cleared a flag bank, destroy this
document's irreversibility claim. **Neither touches a bank** - one writes `+0x1061`, the other tests
`+0x1062`, both in the world-transition byte cluster. *"Banks" in those names is not these banks.*

**NOTHING IN THE BANK MECHANICS BROKE.** Five offsets, five sizes, the bit arithmetic, the range
guards, the reserved ids and **all fifteen rows** of the address table reproduced exactly from a
70-caller census.

**AN ABSENCE CLAIM IS ONLY AS GOOD AS THE ENUMERATION OF ROUTES.** AA-5's 32-byte gap survives -
**but the payload base is `rawBuffer + 0x200`, so the accessor can be bypassed**, and that second
route was censused too: 28 callers, 36 displacements, **none in the gap**. Neither census sees a
pointer stored and read back later, and that limit is published with the result.

**TWO SMALLER CORRECTIONS:** the payload map stopped at Primary's last byte while **`+0x1534` has six
access sites**; and the gate has **32 callers**, not the one documented, including
`InputGameplay_ArbitrateDigitalInputAndModalState` - **story flags reach input arbitration.**

---

## CALL-CHAINS / ADDRESS-INDEX

| From | To | Kind | Note |
|---|---|---|---|
| the flag gate `0032A8A0` | `PersistentFlag_QueryAuthoredThresholdSchedule` | **system transition** | bit 14 set leaves the save payload for authored field data |
| `PersistentFlag_QueryAuthoredThresholdSchedule` | `FieldData_GetVariable0` (`00265270`) | trigger | the progress variable the thresholds are compared against |
| `InputGameplay_ArbitrateDigitalInputAndModalState` | the flag gate | **inbound** | story flags participate in input arbitration |
| `SaveImage_FinalizeHeaderAndChecksum` + 2 others | the flag gate with `0x400B` | trigger | threshold query 11, three call sites not one |

| Address | Name | Body | Note |
|---|---|---|---|
| `00265270` | `FieldData_GetVariable0` | 28 bytes | 22 callers; the threshold schedule's input |
| `0032A920` | thunk to the flag gate | 5 bytes | not in §3 |
| `0032ABE0` | thunk to `PersistentFlag_SetPrimary` | 5 bytes | not in §3 |

Data addresses, no size column: payload `+0x1534`/`+0x1535` the new field · `+0x1394`-`+0x13B3` the
confirmed gap · `02ADD0C8` the authored threshold table pointer · `02098E58` the field variable block.
