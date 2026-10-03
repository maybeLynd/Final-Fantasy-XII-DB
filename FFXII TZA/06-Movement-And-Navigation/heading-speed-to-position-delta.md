---
system: Heading + speed to position delta
category: 06-Movement-And-Navigation
status: AUDITED
owner_layer: PrimaryOwner:Movement
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: falsification-pass-1-repos-46
  crossref_clean: true
  reopened_count: 3
---

# Heading + speed to position delta

> The arithmetic that turns "facing this way, moving this fast" into an actual step across the
> ground — the innermost piece of how anything in FFXII walks.

## 1. What the player sees

Every character, monster and NPC that moves does so as a sequence of small steps, each one
computed from two angles and a speed: which way it is facing, how steeply it is going up or
down, and how fast it is going. This is where those three numbers become an actual displacement.

Three things a player meets without knowing it:

**Not everything can walk.** The engine checks an actor's class before it will accept a speed,
accept a facing, or produce a step. Objects outside that one class silently refuse — no error,
no movement, and the step it hands back is a flat zero.

**Walking uphill is slower across the ground than walking on the flat.** The step is a genuine
3-D decomposition: the steeper the climb angle, the less of the speed goes into horizontal
progress. On terrain flagged as flat-only, the climb term is dropped entirely and the whole
speed goes sideways.

**Animation can drive the character instead of the controller.** A character in certain
animation states has its facing and speed *taken over* by the animation — the value the
locomotion code computed is stashed away, the animation's own values are substituted, and they
decay by a fixed 0.83 per frame until they fall below 0.05 and control returns. This is the
mechanism behind knockback slides and animation-locked lunges: your stick input is genuinely
ignored, not merely overridden later.

## 2. Native mechanism

### The actor class gate

Movement is restricted to one actor class. The class is the **top three bits of the byte at
`WorldActor + 3`**, and only the value `3` (`0x60` once masked) may move:

```c
if ((actor->bActor_class_flags & 0xE0) != 0x60)
    return;                        // ComputeDelta first writes out_delta = {0,0,0,1.0}
```

The same gate appears in `Movement_SetRequestedSpeed`, `Actor_SetDesiredMovementHeading`,
`Movement_ComputeDeltaFromHeadingSpeed` and **twice** in `Movement_UpdateActorFrame`, so it is a
precondition of the whole API rather than a quirk of one function.

`Actor_GetWorldPosition` uses the same field with a **wider** test — it admits class `1` *or*
class `3` — and on refusal it writes `(0,0,0)` into the caller's outputs rather than leaving
them alone. A caller that ignores the class silently receives the world origin.

### The delta formula — a spherical decomposition, not a planar one

`Movement_ComputeDeltaFromHeadingSpeed` reads three values out of the movement state and writes
a 4-component vector:

| Field | Role in this function |
|---|---|
| `movement_state + 0xA4` | **yaw** — drives the horizontal X/Z decomposition |
| `movement_state + 0xA0` | **pitch** — drives the vertical Y term and foreshortens X/Z |
| `movement_state + 0xD0` | **speed** |

Both angles are first wrapped into ~~`(-π, π]`~~ `[-π, π]`, an exact `+π` becoming `-π` and `-π` becoming `+π`, *(corrected 2026-10-02, OPUS: `0026A8E6` `comiss` / `jb` takes the bias `[00915620]` (`-π`) for a negative angle, else `[01CEBC50]` (`+π`), then truncates at `0026A90E`–`0026A93B`; the contract's LD-6)* by the truncating-`fmod` idiom described in §4.
Then:

```c
X = sinf(yaw) * cosf(pitch) * speed
Y = sinf(pitch)             * speed
Z = cosf(yaw) * cosf(pitch) * speed
W = 1.0                                  // on every exit path
```

That is textbook spherical-to-Cartesian. **`X` and `Z` are not scaled by `speed` — they are
scaled by `speed * cos(pitch)`**, which is why an actor climbing a slope covers less ground per
frame than one on the flat at the same requested speed.

**The planar branch.** The pitch term is dropped entirely when
`FUN_00267260(actor) != 0 && FUN_00264460(actor) == 0`:

```c
X = sinf(yaw) * speed
Y = 0
Z = cosf(yaw) * speed
```

On that branch only, the formula collapses to the familiar 2-D one.

**`W` is 1.0 on all four exits** — class-gate rejection, override, zero speed, and the normal
path — so a caller cannot distinguish "refused" from "computed" by inspecting it. On rejection
the whole vector is `(0, 0, 0, 1.0)`: the output is written, not left untouched.

**Zero speed short-circuits.** If `speed == 0.0` after the object-state modifier has run, none
of the three components is written and the vector stays at the zeros stored on entry.

### The animation-state override — Presentation writes back into Movement

Before the decomposition, if the actor carries a presentation-state index other than `-1`:

```c
Movement_ModifyHeadingSpeedForObjectState((short)*actor->pSwbiPresentationState, &yaw, &speed);
```

`00424080` indexes the **character render record array** by `object_index * 0x740` and may
rewrite **both** the yaw and the speed by reference. The array base is the pointer at `022C6F28`,
assigned a **297,264-byte (`0x48930`)** allocation by `CharacterRenderSystem_AllocateAndInitialize`
(`003325D0`); records run `base + i * 0x740` for **exactly 160 records** (`160 × 0x740 = 0x48800`),
and `FUN_00426480` writes a trailing dword at **`+0x48830`** — `0x30` past the last record, **not** at the
array's end. The trailer is therefore `0x130` = **304 bytes**, not 256.

> **PROPAGATED 2026-09-19 (OPUS). THE CORRECTION ALREADY EXISTED AND NEVER REACHED THIS PAGE.**
> [the character render record array](../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md)
> corrected this equation when it was written — *"the product is `0x48800`. The address `0x48830`
> is real and is where `00426480` writes, but it is **inside the tail**, not the end of the record
> area. Two correct numbers joined by a wrong equation."* That page names the pattern exactly: **"individually
> correct figures, joined by an equation nobody evaluated."** This page, `character-render-object.md`
> and `_index/_inbox/repos-46.md` kept the uncorrected version, so what is recorded here is a
> **pass-24 propagation failure**, not a new discovery. `check_arithmetic.py` found it independently,
> which is worth stating only because reproducing a known-true correction is how an instrument earns
> trust before it is believed about anything else. This read
> ~~*"`160 × 0x740 = 0x48830`, which is where `FUN_00426480` writes a trailing dword`, leaving a
> 256-byte trailer"*~~. **Every cited fact in that sentence is right and the equation is wrong.**
> The binary gives `003325E7 mov ecx, 0x48930` (the allocation), `0033264D mov ecx, 0xa0` (160)
> and `00426493 mov dword ptr [rcx + 0x48830], eax` (the trailing dword) — all three as stated.
> But `160 × 0x740` is `0x48800`, and **`0x48830` is not a multiple of `0x740` at all** (160.03
> records), so it cannot be where the array ends. The dword sits `0x30` beyond the last record,
> and the trailer that follows the records is `0x48930 - 0x48800 = 0x130` = 304 bytes.
> **The wrong figure was load-bearing twice over**: it supplied the array's end offset *and* the
> 256-byte trailer, and 256 is exactly what `0x48930 - 0x48830` gives, so the two errors agreed
> with each other and the sentence read as if it checked out. **NOT CLAIMED:** what occupies the
> `0x30` between the last record and that dword — and the corpus already answers it elsewhere:
> `0x48830` is **`CharacterRenderSystemTail +0x30`**, the field `encodedRootPointer`, whose store row
> records it as *written by 00426480*, and `BT-3` in the question register already names it *"encoded
> root `+0x30`"* within *"the remaining `0x130` system tail"*.
>
> **NOTHING IN THIS CORRECTION IS NEW, AND THAT IS THE POINT.** The right figures are in at least four
> places already: [the record-array page](../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md), [the
> pool-lifecycle contract](../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md) — which spells out
> `160 × 0x740 = 0x48800`, `+ 0x130 = 0x48930` — the audit log, and `BT-3`. Three documents kept the
> wrong one anyway. **A correction is not propagated by being correct somewhere.**
> **The same equation appears in `17-Presentation-Rendering/Character-Rendering/character-render-object.md` (the `count` row of the two-class comparison) and in `_index/_inbox/repos-46.md`**; both were peer-held at the time of writing and are not edited here.

**This is not the `CharacterRenderObject` class** — see §8f.

- **Latched (record `+0x62C` bit 0 set):** `speed *= 0.83` each call, then `yaw` and `speed` are
  replaced by the record's own `+0x620` / `+0x624`. The latch clears once the substituted speed
  falls to `<= 0.05`. This is the animation-driven slide.
- **Entering the latch:** requires state `0x10`, an incoming `speed == 0.0`, and a per-character
  counter at record `+0x457` having reached `(int)(_DAT_01DFE0B4 * 30)` — a **frame count**,
  30 per unit of the engine time-base mode (§4).
- **Not latched:** the incoming yaw/speed are *saved into* the record and the previous pair
  preserved, then a second gate keyed on the state value can scale or kill the speed:
  `state 0x35`/`0x36` → `speed *= (accumulator *= 0.9)`; **`state 0x0D` → `speed = 0.0`**;
  anything else resets the accumulator to `1.0`.

So an animation state can stop an actor dead, decay it, or steer it — from Presentation-owned
data, inside a Movement-owned function.

### The override path

When the caller passes a non-zero override flag, the supplied vector is copied through
unchanged and its Euclidean length is stored:

```c
if (use_override) {
    movement_state[0xF8] = sqrtf(|dx*dx + dy*dy + dz*dz|);   // via 003A1D30
    out_delta[0..2] = override_delta[0..2];                  // copied verbatim
    out_delta[3] = 1.0;
    return;                                                  // class gate still applies first
}
```

`003A1D30` is a 23-byte leaf: it converts its single float argument to double, masks the sign bit
with the 128-bit constant at `01CEBD80` (`7FFFFFFFFFFFFFFF` twice), converts back and **tail-jumps
to `sqrtf`**. It is `sqrtf(fabs(x))` — a scalar helper, not a vector routine; the caller supplies
the sum of squares. It has **12 direct callers across Movement, Party, Script VM and Audio, at 17 call sites**.

**A second, unrelated write to `+0xF8`.** On the *non*-override path, before anything else:

```c
if (movement_state[0xF8] < 0.0)
    movement_state[0xF8] = speed;          // negative sentinel is repaired to the current speed
```

So `+0xF8` is not exclusively the override magnitude; a negative value there is treated as
"unset" and refilled from the requested speed.

### Integration

`Movement_IntegratePositionAndMeasureDisplacement` applies the delta **and returns the squared
distance actually moved**, which the frame driver stores in the movement state.

```c
if (world_ctx == NULL) {
    candidate[0] = movement_state->flPosition_x + candidate[0];      // X — yes, all three
    candidate[1] = movement_state->flPosition_y + candidate[1];
    candidate[2] = movement_state->flPosition_z + candidate[2];
} else {
    Movement_PrepareCandidatePosition(actor, world_ctx, movement_state, candidate, mode);
}
// then, either way:
if (FUN_00264460(actor) == 0 && (actor->bFlags_08 >> 2 & 1) == 0)
     d2 = (cand.x - pos.x)^2 + (cand.z - pos.z)^2;                   // planar measure
else d2 = (cand.x - pos.x)^2 + (cand.y - pos.y)^2 + (cand.z - pos.z)^2;
movement_state->position = cand;
return d2;
```

The no-context path is a plain three-component addition onto the current position. With a
context, the step goes through world-coordinate preparation and accumulation instead — the path
where terrain and collision participate.

**`bFlags_08` bit 2 selects whether displacement is measured in 3-D or on the XZ plane only** —
it does not change where the actor ends up, only the number reported back.

The world-context path is a **chain, not a pair**: `Movement_IntegratePositionAndMeasureDisplacement`
calls `Movement_PrepareCandidatePosition`, which calls `Movement_TransformAndAccumulateCandidate`.
`002E54A0` has exactly one caller (`002E5380`), which itself has exactly one caller (`002E5610`).

`Movement_PrepareCandidatePosition`'s own body only does work when `mode != 0`. The per-frame
driver always passes `mode = 0`, so from the walking path it is a pure forwarder; the
`world_ctx + 0xE8/0xEC/0xEE/0xEF` flag block and the `+0x100..+0x108` offset add are reachable
only from the other caller, `002E5180`.

## 3. Key addresses

| Address | Name | Body | Role |
|---|---|---|---|
| `002E4380` | `Movement_ComputeDeltaFromHeadingSpeed` | 601 B | yaw + pitch + speed → delta vector |
| `002E5610` | `Movement_IntegratePositionAndMeasureDisplacement` | 314 B | apply the delta, return displacement² |
| `002E5380` | `Movement_PrepareCandidatePosition` | 273 B | world-context path, step 1 |
| `002E54A0` | `Movement_TransformAndAccumulateCandidate` | 282 B | world-context path, step 2 |
| `002E45E0` | `Movement_UpdateSteeringTowardTarget` | 963 B | steering toward a target |
| `002E5030` | `Movement_UpdateActorFrame` | 330 B | per-frame driver — calls all of the above |
| `002E5C10` | `Movement_PublishHeadingState` | 85 B | copies both angles into the render record |
| `0026D6F0` | `Movement_SetRequestedSpeed` | 275 B | speed setter, same class gate |
| `0026D6A0` | `Movement_SetRequestedSpeedScaled` | 38 B | scaled variant — applies `DAT_01DFE0BC` |
| `0026A0D0` | `Actor_SetDesiredMovementHeading` | 97 B | writes the wrapped yaw to `+0xA4` |
| `002E55C0` | `Movement_ClearSteeringRequest` | 73 B | cancel |
| `00424080` | `Movement_ModifyHeadingSpeedForObjectState` | 427 B | animation-state override of yaw and speed |
| `00265020` | `Actor_GetWorldPosition` | 61 B | class `1` or `3`; zero-fills on refusal |
| `003A1D30` | *(unnamed)* — `sqrtf(fabs(x))` | 23 B | used by the override path |
| `0023A070` | `BattleUnit_ApplyMovementIntentToWorldActor` | 151 B | combat-side producer of `+0xA4` and `+0xD0` |

All fifteen resolve in the current parent with the body extents shown
(`DumpFullCoverageGraph`, 2026-09-02, 38,161 functions).

**Names inherited from GFZ annotation.** `002E4380`, `0026D6F0`, `0026A0D0`, `002E5610`,
`002E5380`, `002E54A0`, `002E5030`, `002E5C10`, `00424080`, `00265020` and `0023A070` were read
at tier 1 in this pass and all match their names. `002E45E0` is named but its body is not yet
read here *(answered: see [how a character turns](Facing-And-Steering/how-a-character-turns.md), where `002E45E0` is read in full; 2026-10-02, OPUS)*.

## 4. Data structures and formulas

```
WorldActor
  +0x03   u8    bActor_class_flags   movement requires (v & 0xE0) == 0x60; position read allows
                                     (v >> 5) == 1 or 3
  +0x08   u8    bFlags_08            bit 2 -> measure displacement in 3-D instead of XZ
  +0x0C   u8    bFlags_0C            bit 4 set by the speed setter as a change flag
  +0xB8   ptr   pMovement_state_ptr
  +0xC0   ptr   pSwbiPresentationState

Movement state
  +0x00   f32   position x
  +0x04   f32   position y
  +0x08   f32   position z
  +0xA0   f32   pitch    (GFZ struct calls this flCurrent_heading - see K-6)
  +0xA4   f32   yaw      (GFZ struct calls this flDesired_heading; written by
                          Actor_SetDesiredMovementHeading, read for X/Z)
  +0xD0   f32   requested speed
  +0xF0   ptr   steering request  -> +0x24 f32 requested speed, +0x29 u8 steering mode
  +0xF8   f32   override magnitude; also a "<0 means unset" sentinel repaired to speed

World context   (= the movement body; K-4)
  +0x70         f32[4] the placement displacement, normalised when bit 4 is set
  +0x90   u32   bit 4 = the field-cell solver moved the body this step
  +0xE8/0xEC/0xEE/0xEF, +0x100..+0x108   used only when Prepare is called with mode != 0

Character render record array   base ptr 022C6F28, 160 records, stride 0x740 (1,856 B)
  +0x000  i16   record id; -1 means the slot is empty (NOT a vtable pointer)
  +0x006  i16   compared against -1 by the object-state modifier
  +0x0CC  i16   object/animation state, masked & 0xFFF
  +0x284  u32   bit 0x8000000 gates the save/substitute block
  +0x457  i8    per-record frame counter, compared against _DAT_01DFE0B4 * 30
  +0x240/+0x244/+0x248   written by Movement_PublishHeadingState (pitch, yaw, 0.0)
  +0x610 .. +0x61F       incoming yaw / speed / accumulator / flags, 16 B, saved by the modifier
  +0x620 .. +0x62F       the preserved previous group; +0x620 yaw, +0x624 speed,
                         +0x628 accumulator, +0x62C bit 0 = the animation-override latch
```

**Class gate**

```
movement permitted   iff  (actor.bActor_class_flags & 0xE0) == 0x60
position readable    iff  (actor.bActor_class_flags >> 5) == 1  ||  == 3
```

**Angle wrap into ~~`(-π, π]`~~ `[-π, π]`, the endpoints swapping** *(corrected 2026-10-02, OPUS: `0026A8E6` `comiss` / `jb` takes the bias `[00915620]` (`-π`) for a negative angle, else `[01CEBC50]` (`+π`); `+π` maps to `-π` and `-π` to `+π`)* — used identically by `Actor_SetDesiredMovementHeading` and by
both angles inside `ComputeDelta`:

```
w      = (a >= 0) ? PI : -PI                 // PI  = 0x01CEBC50 =  3.14159274
wrap(a)= ((a + w) - trunc((a + w) / TWO_PI) * TWO_PI) - w
                                             // TWO_PI = 0x01CEBC78 = 6.28318548
```

**Delta from yaw, pitch and speed** (`002E4380`, byte-verified at `002E4419`-`002E45C0`)

```
speed = movementState[0xD0]
if (movementState[0xF8] < 0) movementState[0xF8] = speed

yaw   = wrap(movementState[0xA4])
pitch = wrap(movementState[0xA0])

if (actor.pSwbiPresentationState && *pSwbiPresentationState != -1)
        Movement_ModifyHeadingSpeedForObjectState(*pSwbiPresentationState, &yaw, &speed)

if (speed == 0)         delta = (0, 0, 0, 1.0)
else if (FUN_00267260(actor) != 0 && FUN_00264460(actor) == 0)
        delta = ( sin(yaw)*speed,              0,             cos(yaw)*speed,              1.0 )
else    delta = ( sin(yaw)*cos(pitch)*speed,   sin(pitch)*speed,
                                               cos(yaw)*cos(pitch)*speed,                  1.0 )
```

**Override path**

```
delta.xyz            = supplied vector, verbatim
movementState[0xF8]  = sqrt(|dx² + dy² + dz²|)        via 003A1D30
delta.w              = 1.0
```

**Integration and the displacement measure**

```
if (world_ctx == NULL)  candidate.xyz += position.xyz
else                    candidate = Prepare(...) -> TransformAndAccumulate(...)

planar = (FUN_00264460(actor) == 0) && ((actor.bFlags_08 >> 2) & 1) == 0
d2     = planar ? (Δx² + Δz²) : (Δx² + Δy² + Δz²)
position = candidate
movementState.flLast_displacement_squared = d2
```

**Scaled speed setter** — the only place a global scalar touches authored speed:

```
Movement_SetRequestedSpeedScaled(actor, authored):
    mode = (authored > 0) ? 0 : 2
    Movement_SetRequestedSpeed(actor, DAT_01DFE0BC * authored, mode)
```

**Published locomotion rate**, written by `Movement_SetRequestedSpeed` into the world context:

```
world_ctx[+0xC8] = DAT_01DFE0B8 * 30.0 * 3.6 * speed        // = 108.0 * speed as shipped
```

`DAT_01DFE0B4 = 1` (int), `DAT_01DFE0B8 = 1.0f`, `DAT_01DFE0BC = 1.0f` in the shipped image
(read at file offsets `01CDC6B4`/`B8`/`BC`). `30.0` is `008F8D80`; `3.6` is `00915734`. See §8e —
this is the same triple that `OPEN-QUESTIONS.md` carries as **Z-10 / Z-11**.

## 5. Call chain

**Corrected 2026-09-02 — the three stages are siblings, not a nest.**

```
per frame
  -> WorldActor_UpdateRuntimeAndScriptExecutionState (0025DF00)
     -> Movement_UpdateActorFrame (002E5030)                      [class gate; lifecycle != 1;
        |                                                          pSwbi != NULL; pSwbi[0x14F] bit 0 clear]
        |  world_ctx = pSwbiPresentationState[0x138]
        +-> Movement_UpdateSteeringTowardTarget (002E45E0)         ONLY IF
        |      (u8)(steeringRequest->bSteeringMode - 1) < 4        i.e. modes 1..4
        +-> Movement_ComputeDeltaFromHeadingSpeed (002E4380)       <- THIS
        |      -> Movement_ModifyHeadingSpeedForObjectState (00424080)   [Presentation data]
        |      -> sinf / cosf, or the verbatim override
        +-> Movement_PublishHeadingState (002E5C10)                -> CharacterRenderObject +0x240   <- corrected 2026-10-02, OPUS - the 0x740-byte render record at 022C6F28 (002E5C33-002E5C4C, section 8f), not CharacterRenderObject
        +-> Movement_IntegratePositionAndMeasureDisplacement (002E5610)   [mode = 0 always]
               -> world_ctx == NULL : position += delta
               -> otherwise         : 002E5380 -> 002E54A0
        +-> FUN_002EA7F0 / FUN_003DB020 / FUN_002E6330
```

`Movement_ComputeDeltaFromHeadingSpeed` has **exactly one caller** in the whole binary:
`Movement_UpdateActorFrame`. `Movement_UpdateSteeringTowardTarget` does **not** call it, and does
not call the integrator either.

`Movement_IntegratePositionAndMeasureDisplacement` has **two** callers: `Movement_UpdateActorFrame`
(mode 0) and `FUN_002E5180`.

**Upstream of the two angles and the speed:**

| Producer | Writes |
|---|---|
| `Actor_SetDesiredMovementHeading` (`0026A0D0`) | yaw at `+0xA4`, wrapped |
| `Movement_SetRequestedSpeed` (`0026D6F0`), 10 distinct callers | speed at `+0xD0` |
| `Movement_SetRequestedSpeedScaled` (`0026D6A0`) | speed, pre-multiplied by `DAT_01DFE0BC` |
| `Movement_ClearSteeringRequest` (`002E55C0`) | zeroes the steering mode and both speeds |
| `BattleUnit_ApplyMovementIntentToWorldActor` (`0023A070`) | drives the two setters for combat actors |

**Downstream:** the actor's world position, and the ~~CharacterRenderObject record~~ `0x740`-byte render record at `022C6F28` (`+0x240`) *(corrected 2026-10-02, OPUS: `002E5C33`–`002E5C4C`; §8f)*.

**Do not confuse with:** `BattleUnit_ApplyMovementIntentToWorldActor` (`0023A070`) — but note it
is not a lookalike, it is the **upstream producer** for every battle unit. It reads the combat
locomotion solver's output and calls `Actor_SetDesiredMovementHeading` and `Actor_SetMovementSpeed`;
when the global battle-state word `02089340` has any of bits `0x600` set and the unit's stats
record passes a selector test it instead **forces speed to 0**, and unit-flag bit 18
(`0x40000`) suppresses the speed write on the normal path.

### The `002E5030` exclusive subtree — all 7 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the per-frame driver **7 frontier functions** — the
heading publish, the spatial-grid update it feeds, and the deferred-registration tail.
Interior cites are one instruction inside each declared extent (`interior_cite.py scan`; no
boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| heading publish | `002E5C10` `Movement_PublishHeadingState` (85 B) | copies the `+0xA0`/`+0xA4` angle pair (plus a zero third float) into the render record — `+0xC0` context → word id `×0x740` over the `022C6F28` base, gated on `+0x284`, stores xmm1/2/3 at `+0x240`–`+0x248` | `002E5C4C` |
| spatial-grid update | `003DB020` (168 B) | the occupancy publish the driver calls when `002EA7F0` passes: sets `+7` on the context's `+0x138` mover object, gates `003B7730`, runs `0046AD20(record+0x120, max(+0,+4) radius, position)`, then walks the returned mask and ORs `1<<(id&0x3F)` into the ~~`02AC7CE0`~~ `02B57CE0` bucket array *(corrected 2026-10-02, OPUS: `02AC7CE0` has no reference; `02B57CE0` is used by `003DAA40`, `003DAAB0`, `003DAE30`, `003DB020`)* by `id>>6` (16-byte stride) | `003DB068` |
| cell recompute | `0046AD20` (638 B) | the position→cell worker: caches the last position in the `02CA60xx` state block, `003A1D30` + `00861F02` float helpers, hysteresis compare, refreshes the cell mask | `0046AD3E` |
| deferred register | `002E6330` (117 B) | the driver's tail: same class gates plus `+9` bit 6, `002E9FE0`, flag byte `00263FB0` == 1 → context `+0x151` bit 7 via `00264EA0`, then `+0x138` non-null + `+0x14E` set → tail-appends the record to the ~~`02AC7CC8`/`02AC7CD0`~~ `02B57CC8`/`02B57CD0` list via `003DB0D0` *(corrected 2026-10-02, OPUS: the `02AC7Cxx` pair has no reference; `02B57CC8` / `02B57CD0` are used by `003DAA20`, `003DAE30`, `003DB0D0`)* | `002E635A` |
| list append | `003DB0D0` (73 B) | intrusive single-link append — node `rcx+0x30`, link at `+0xA0`, head ~~`02AC7CC8`~~ `02B57CC8` / tail ~~`02AC7CD0`~~ `02B57CD0` *(corrected 2026-10-02, OPUS: the same references as the row above)* | `003DB106` |
| flag probes | `00263FB0` (8 B), `00264EA0` (24 B) | the ~~`0209BDA3`~~ `02099DA3` flag-byte getter *(corrected 2026-10-03, SWE2-EC7, record `swe2ec7-corr-02099da3-typo-1003`: `00263FB0 movsx eax, byte ptr [rip+0x1E35DEC]` reads `0x263FB7 + 0x1E35DEC` = `02099DA3`, MirrorBlockBytes02099DA0 +0x03)*, and context `+0x151` bit-7 extractor | `00263FB0` / `00264EB3` |

`002E45E0`/`002E4380`/`002E5610`/`002EA7F0`/`002E9FE0`/`003B7730`/`003A1D30`/`00861F02`/`00808C40`
are shared callees already bound in §3–§5 — deliberately not census members.

## 6. Modding notes

- **The class gate is the first thing to check** when an actor will not move. `(flags & 0xE0)
  != 0x60` refuses silently. It refuses in the *speed* setter, the *heading* setter and the
  delta computation alike, so a partial workaround is not possible.
- **The delta out-vector is written even on refusal**: you get `(0, 0, 0, 1.0)`, not your old
  contents. And `W` is always `1.0` — do not use it to detect success.
- **Do not model the step as `sin(heading) * speed`.** That is only the planar branch. The
  general case multiplies both horizontal components by `cos(pitch)`, so an actor on a slope
  covers less ground per frame at the same requested speed.
- **`+0xA0` is a pitch even though the GFZ struct names it `flCurrent_heading`.** Writing a yaw
  into it will tilt the actor's step out of the ground plane and shrink its horizontal travel by
  `cos(that value)`.
- **The override path bypasses both angles.** If you need to impose an exact displacement, that
  is the intended door, and the engine records `sqrt(|Σ squares|)` at `+0xF8` for you. Note the
  same field is also used as a `<0` sentinel on the normal path.
- **Animation can and does take the wheel.** `Movement_ModifyHeadingSpeedForObjectState` will
  replace your yaw and speed outright while the render record's latch is set, decaying at `0.83`
  per call until below `0.05`; object state `0x0D` forces speed to `0.0` whenever the record's
  presentation entry resolves. If an actor refuses to move and the class gate is fine, look at
  its presentation state next.
- **Two integration paths exist**, and which you get is not a caller choice in the walking path:
  `Movement_UpdateActorFrame` always passes `pSwbiPresentationState[0x138]`. The plain-addition
  branch is reached only when that field is null.
- **`bFlags_08` bit 2 changes the reported displacement, not the movement.** Clearing it makes
  `flLast_displacement_squared` a flat XZ measure, which matters to anything gating on
  "did this actor actually move".
- **XIIOnline:** this is the innermost movement seam. Prefer setting yaw and speed and letting
  the native step run, over writing positions; the override path exists if an exact vector is
  genuinely required. The class gate applies to remote puppets too — and so does the animation
  override, which will fight an injected speed while a slide latch is set.

## 7. What is not known

- [x] ~~The source of the second angle driving `delta.y`.~~ **K-1 ANSWERED** — it is
      `movement_state + 0xA0`, consumed as a pitch: `Y = sin(pitch) * speed`, and the same
      `cos(pitch)` foreshortens X and Z.
- [x] ~~What actor class `0x60` denotes, and which classes are excluded.~~ **K-2 ANSWERED
      2026-09-12 (FABLE), by reconciliation with `BV-4`:** class 3 is the **steerable actor class**
      (sequences 5–7 of the record carver's table: `PC`, `VAN`, `summon`, `treasure_`, `WARP_PC`,
      `NPC`, `hitactor`, `monster_`, `unique_monster_`, `trial_` in the shipped scripts) — the only
      class with a full movement context and a steering record. Excluded: class 0 (script-only
      controllers, no `+0xB8`), class 1 (placed objects, a `0x80`-byte block whose `+0x38` is the
      heading `00265200` returns — readable, never steered) and class 2 (trigger lines). See
      [how the engine chooses 3-D or flat movement](Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)
      and [how a character turns](Facing-And-Steering/how-a-character-turns.md) §2.
- [x] ~~What `003A1D30` computes.~~ **K-3 ANSWERED** — `sqrtf(fabs(x))`, a 23-byte tail-call
      leaf with a 128-bit sign mask at `01CEBD80`. Scalar, not vector.
- [x] The world-context integration path and what `world_ctx+0x90` bit 4 selects. **K-4.**
      Narrowed: bit 4 is passed as the second argument to `FUN_00329B00` together with
      `world_ctx + 0x70`, and only when a `pBattleUnit` is present.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (K-4): the "world context" is the actor's
      movement body. Bit 4 means "the field-cell solver moved the body this step", and `+0x70` is that move's unit
      direction, which a battle unit then turns to face.*
      - **The object.** `002E5610`'s second argument is the movement body, so `+0x70` / `+0x90` are its placement
        record's displacement and flags ([the movement body pool](the-movement-body-pool-and-the-separation-pass.md)
        §2.4: the placement starts at body `+0x30`, so the same fields are placement `+0x40` / `+0x60`).
      - **The integration path.**
        1. `Movement_UpdateActorFrame` (`002E5101`) calls `002E5610`, which calls `Movement_PrepareCandidatePosition`
           `002E5380` (it adds the push vector `+0x100`–`+0x108` when mode ≠ 0).
        2. That tail-jumps to `Movement_TransformAndAccumulateCandidate` `002E54A0` (`002E548C`).
        3. When `00267260` holds, `002E54A0` hands the move to `003DB140(body, move)` → **`00380C40(placement, move)`**
           (`002E54C7`, `003DB149`).
      - **Where bit 4 comes from.** `00380C40` starts every move by zeroing the displacement to `(0, 0, 0, 1)` and
        **clearing bit 4** (`00380C64`–`00380C74`).
        - If the field has a cell record and the move is longer than 0.001, it runs the cell solver `002327D0`
          (`00380CCC`). The solver adds each sub-step it takes into `+0x40`–`+0x48` and **sets bit 4** (`00232DC0`–`00232E17`);
          its helper `0022F9B0` does the same (`0022FDE8`–`0022FE0E`).
        - Afterwards, when bit 4 is set, `00380800` normalises the displacement to a unit vector, or zero below
          `1e-6` (`00380CF4`–`00380D02`, `00380800`–`00380891`).
      - **What reads it.** Back in `002E5610`, `00329B00(handle, bit 4, &body+0x70)` (`002E5659`–`002E56AF`) sets the battle
        unit's `+0x1F0` bit 9 and copies the vector to `+0x1C0`, or clears the bit.
        - `BattleLocomotion_FinalizeHeadingState` `0033BFB0` (called by `BattleLocomotion_SolveDefaultStep`) reads that
          vector through the locomotion sub-object (`[+0x108] + 0x140` / `+0x170`) and, when bit 9 is set, derives a
          heading from the angle between it and the current forward vector, wrapped to ±π (`0033C003`–`0033C0CD`).
        - **So a battle unit that the field solver has moved turns toward the direction it actually moved**, the resolved
          (e.g. slid) direction rather than the requested one.
      - **Not traced:** ~~what `00267260` tests, and~~ *(answered for `00267260`: see K-7 below and [the 3-D or flat page](Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)'s flat selector; 2026-10-02, OPUS)* the part of `0033BFB0` after the angle.
- [x] ~~Where the delta's `X` component is applied.~~ **K-5 ANSWERED — there was never a missing
      path.** The no-context branch adds all three components; the earlier transcription dropped
      the `X` line. See §8d.
- [x] ~~**K-6** — which of the two GFZ heading names is wrong, and what is `+0xA8`?~~
      **ANSWERED 2026-09-07 — the question was malformed and `+0xA8` is the facing angle.** A
      dataflow scan finds **exactly one** float writer image-wide, `FUN_002E5E10`, which stores the
      angle **through a single sign-biased wrap** (corrected 2026-09-11: not a range guarantee, and
      not `Angle_NormalizeRadiansPi`'s result — exact `±pi` flips sign, infinities and NaN pass
      through, and past the signed conversion limit the pass stores `f32(a ± π + T) ∓ π`, not `a` —
      corrected 2026-09-12, EXP-074; EXP-072). **The pair `+0xA0`/`+0xA4` was never a complete account of
      the group:** those two drive *motion* per `K-1`, and the unnamed `+0xA8` is what the engine
      reports as *facing* to the accessor's 33 callers. **No renaming proposed for the pair.**
      See the 2026-09-07 extension. Residue: `K-11` (facing versus motion), `K-12` (the `+0x0D`
      bit 5 copy exemption — corrected 2026-09-11 from "invalidation"), `K-13` (`+0xAC`).
      > **K-12 answered 2026-09-12 (FABLE): bit 5 means "this actor carries a non-zero position
      > offset".** An image-wide scan of every `or` / `and` / `test` / `bt*` on an actor's `+0x0D` byte
      > with the `0x20` mask finds one writer pair and one reader: `0026B170(actor, x, y, z)` — for
      > actors whose class bits are `0x60` — stores the vector at the movement state's `+0x40` /
      > `+0x44` / `+0x48` and then **sets bit 5 when `x² + y² + z² ≠ 0` and clears it when the vector is
      > zero** (`0026B1BC`–`0026B1EF`); `ActorStorage_InitializeRecord` clears it at `0026666C`; the one
      > reader is the facing writer `002E5E10` at `002E5ECB`. The vector is what the script verb
      > **`setposoffset`** (`0x0505`, `00348F80`, [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)) sets — it pops an int and three floats and
      > calls `0026B170` (`00348FD3`) — and `0026BA70` is its other caller. So an actor a script has
      > displaced from its logical position keeps only the primary facing copy (`+0x58`); the two
      > secondary copies (`+0x78`, `+0x68`) are left to whatever re-derives the offset presentation.
- [x] **K-7 ANSWERED 2026-09-02** — see [`Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`](Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md): `00264460` is the 3-D test (`bit0 | bit1` of controller `+0x151`), `00267260` the flat test (four conditions, gated on the actor system being initialised). **3-D is the default.** Originally: What `FUN_00267260` and `FUN_00264460` actually test. Together they select
      the planar branch; `FUN_00264460` additionally selects the 3-D displacement measure.
      `FUN_00264460` reads bits 0-1 of `pSwbiPresentationState[0x151]`; `FUN_00267260` reads
      `actor[+0x08]` bit 1 behind a global check.
- [x] ~~**K-8 (new).**~~ **ANSWERED 2026-09-02, closes with Z-10.** Whether `DAT_01DFE0BC` (the authored-speed multiplier) and `DAT_01DFE0B8`
      (the published-rate multiplier) are ever written away from `1.0` during play. See §8e and
      `OPEN-QUESTIONS.md` **Z-10**.
- [x] ~~**K-10 (new).**~~ **ANSWERED 2026-09-02 — documented.** The character render record array itself — 160 records × 1,856 B at
      `022C6F28`, five authored render stages, owned by Presentation and written by Movement. It
      has no document. See §8f.
- [x] **UQ-102.** The other 399 unnamed Movement functions.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 06-Movement-And-Navigation/heading-speed-to-position-delta.md. See the register row.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Class gate `(flags & 0xE0) == 0x60`, and its presence in five functions | complete bodies of `002E4380`, `0026D6F0`, `0026A0D0`, `002E5030` (×2) | 1 |
| Position read admits class `1` or `3`, zero-fills otherwise | complete body of `00265020`; `shr r10d,5; sub r10d,1; je; cmp r10d,2; jne` at `00265025` | 1 |
| `bActor_class_flags` at `WorldActor+3`, `pMovement_state_ptr` at `+0xB8` | `movzx eax,[rcx+3]` and `mov rdx,[rcx+0xB8]` in `0026A0D0` | 1 |
| Speed read from `movement_state + 0xD0` | `movss xmm3,[rdi+0xD0]` at `002E4419` | 1 |
| `X = sin(yaw)·cos(pitch)·speed`, `Z = cos(yaw)·cos(pitch)·speed`, `Y = sin(pitch)·speed` | byte-level trace of `002E4419`-`002E45A1`: `[rdi+0xA4]`→`[rsp+0x88]`→X/Z; `[rdi+0xA0]`→xmm6→Y and the common factor | 1 |
| Planar branch when `FUN_00267260 != 0 && FUN_00264460 == 0` | `002E4528`-`002E4547`, `xmm7` left zero and `xmm8 = speed` | 1 |
| `W = 1.0` on every path | `mov dword ptr [rbx+0xC], 0x3F800000` at `002E45B9`, plus the gate-rejection and override stores | 1 |
| Delta zeroed before the gate | `xor eax,eax; mov [rdx],rax; mov [rdx+8],eax` at `002E4389`-`002E4394` | 1 |
| Override copies verbatim and stores `sqrt(Σ squares)` at `+0xF8` | `002E43BC`-`002E4419`; `003A1D30` disassembly `andps` + `jmp sqrtf` | 1 |
| **The override input must not be the output buffer** (added 2026-09-29, FABLE, on ASTRA `2ada8a5a0`): the entry keeps only the input *pointer* (`002E438B` `mov r14, r9`), clears the output's `+0`..`+0xB` (`002E4389`-`002E4394`), and only then reads the input's `+4`, `+0`, `+8` (`002E43BC`, `002E43C2`, `002E43C7`); for an input that *is* the output, those first reads see zero bits. The one recorded caller passes a local output (`002E50C0`, `rsp+0x30`) and the input `r9 = r14` from its entry `r8` (`002E50BD`, `002E504C`), so the buffers differ as constructed. *Limits:* a conditional calculation from the bytes, not an executed run; nothing is claimed about partial overlap, the later `sqrtf` and `+0xF8` results, or every live pointer; `002E45E0` between the two gates is 963 B with 21 calls, so no leaf argument about it is made here (the contract's section-14 closure that used one is reopened, CON-172 *(answered: see the heading-speed contract's §14, ANSWERED 2026-09-30 (OPUS) — the refusal does not run there; 2026-10-02, OPUS)*) | `002E438B`, `002E4389`-`002E4394`, `002E43BC`-`002E43C7`, `002E50BD`-`002E50C5`; ASTRA [`heading-passthrough-alias-boundary`](../_experiments/evidence/heading-passthrough-alias-boundary/README.md) | 1 |
| `+0xF8` also repaired from a negative sentinel | `comiss xmm7,[rdi+0xF8]; jbe; movss [rdi+0xF8],xmm3` at `002E443E` | 1 |
| Angle wrap into `(-π, π]`, `TWO_PI = 01CEBC78`, `PI = 01CEBC50` | `0026A0D0` disassembly; constants read from the image: `6.2831855`, `3.1415927` | 1 |
| Integration adds all three components on the no-context path | complete body of `002E5610` | 1 |
| Displacement measure is planar or 3-D by `bFlags_08` bit 2 | same body, both branches | 1 |
| `002E5610 -> 002E5380 -> 002E54A0` is a chain; `002E54A0` has one caller | fresh call graph, 2026-09-02 | 1 + 11 |
| `002E4380` has exactly one caller | fresh call graph + exact call-site census over all 38,161 function bodies | 1 + 11 |
| Object-state modifier reaches `g_pCharacterRenderRecordArray` at stride `0x740` | complete body of `00424080`; same array and stride in `002E5C10` (`imul rcx, rax, 0x740`) | 1 |
| Decay constants `0.83`, `0.9`, release `0.05` | image reads at `00D12434`, `008FCC8C`, `008F30E8` | 1 |
| `Movement_SetRequestedSpeedScaled` applies `DAT_01DFE0BC` | complete body of `0026D6A0` | 1 |
| Published rate `= DAT_01DFE0B8 * 30.0 * 3.6 * speed` | complete body of `0026D6F0`; constants read at `008F8D80` = `30.0`, `00915734` = `3.6` | 1 |

**On the inherited names.** Eleven of the fifteen §3 addresses were read at tier 1 in this pass
and match their GFZ names. The GFZ annotation's own summary of `002E4380` —
*"X=sin(heading)\*speed and Z=cos(heading)\*speed, magnitude stored at +0xF8"* — is **accurate
only on the planar branch**; the `cos(pitch)` factor and the `Y` term are missing from it. The
`+0xF8` half is exact.

## 8b. Reopened 2026-09-02 — Movement walks the combat slot pool

Cross-reference audit pass 3 counted callers of `BattleUnit_GetBySlotIndex` (`00236820`) by
subsystem. **Movement is the single largest owned consumer.**

> **Numbers relabelled 2026-09-02.** This read *"10 call sites, against Combat AI's 5"*. Those are
> **distinct caller** counts, not call sites — they came from the call-graph edge census, and an
> edge count can never be a call-site count (one row per caller-callee pair; see
> [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md) rule 6). An instruction-level
> count gives both figures, and **the conclusion is unchanged — it holds on either measure.**

> **RE-DERIVED 2026-09-02 (falsification pass 1) and the table is exact.** Rebuilt from scratch
> against a freshly regenerated graph *and* an independent instruction-level census (capstone over
> the exact body extent of all 38,161 functions — not Ghidra). **Every one of the eleven rows
> reproduces to the unit, both columns.**

| Owner | Call sites | Distinct callers |
|---|---:|---:|
| *(no owner tag)* | 12 | 12 |
| **Movement** | **11** | **10** |
| Combat AI | 7 | 5 |
| Combat Action | 5 | 4 |
| Party | 3 | 2 |
| Actor/Entity | 2 | 2 |
| Combat Formula | 2 | 2 |
| UI | 2 | 1 |
| Spawn/Encounter/Lifecycle | 1 | 1 |
| Items/Equipment/License | 1 | 1 |
| **Total** | **46** | **40** |

Movement leads every owned subsystem on both measures — 11 sites to Combat AI's 7, 10 callers to
5. The Movement callers are `00326D60`, `003278D0`, `BattleLocomotion_QueryDynamicActorObstruction`,
`BattleLocomotion_BuildSolverContext` (2 sites), `003377C0`,
`BattleLocomotion_ResolveTargetSpacingAndAvoidance`, `PartyFollow_SolveFormation`, `0033C310`
(read 2026-09-17, SWE2-FRONTIER: a 1,362-B Movement body — `01F44830` record base at
[`0033C343`](../_index/ADDRESS-INDEX.md), then `002646C0`/`00203080`/`004692F0`/`0033CB70`/
`00335760` solver helpers), `0033CEF0`, `0033D200`.

That is a relationship this document did not have. The BattleUnit pool is not a combat-only
structure — locomotion code walks it routinely, so movement and combat share one unit registry
rather than each keeping its own.

Movement also accounts for **16 of the 79 callers of `Actor_GetWorldPosition`** — re-derived and
exact. Full census, by call sites / distinct callers: Script VM 27/23, *(no owner)* 25/16,
**Movement 21/16**, Presentation 8/5, Actor-Entity 5/5, Spawn 4/3, Combat Action 4/3, Party 4/3,
Rewards 2/2, Combat Formula 2/1, Audio 1/1, UI 1/1 — 104 sites, 79 callers, 11 owned subsystems.
*Second only to the Script VM* holds among owned subsystems; the untagged group ties Movement at
16 callers.

Two consequences worth carrying:

- The actor **class gate** (`class == 1 || class == 3` to read a position, `class == 3` to move)
  is inherited by every one of those call sites. **Verified at tier 1 this pass** — see §8.
- A mod changing BattleUnit pool semantics changes locomotion, not just combat.

Static call sites, not execution frequency — see U-4.

## 8c. Audit pass 4 disposition - inherited hub neighbours

Crossref audit pass 4 reported four **NEW SINCE BASELINE** relationships for this document:
`CombatFormula`, `Gameplay`, `Items_Equipment_Shops_License` and `Spawn_Encounter_Lifecycle`.
All four are consequences of section 8b.

| Edge | Explanation |
|---|---|
| `00236820` caller `0031B860`, `0031E800` (CombatFormula) | callers of the BattleUnit slot hub |
| `00236820` caller `0030C210` (Gameplay) | same |
| `00236820` callers in Items / Spawn | same |

Section 8b added `BattleUnit_GetBySlotIndex` (`00236820`), which has **40 callers across 9
subsystems**. Citing it imported all of them.

**Disposition: accounted for by reference.** The complete census lives in
[`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md). What this document claims about
that hub is only the measured fact that **Movement is its largest single consumer** - and that
claim is about Movement, not about CombatFormula or Items.

## 8d. Corrections, falsification pass 1 (2026-09-02)

Kept in full, per the standing rule that the path to a wrong answer is itself evidence.

### Correction 1 — the headline formula was incomplete (OVERTURNED)

**Was believed.** *"`out_delta[0] = sinf(heading) * speed; out_delta[2] = cosf(heading) * speed;
out_delta[1] = <second-angle term>`"*, with §4 restating `delta.x = sin(heading) * speed` and
`delta.y = f(secondAngle) // separate sin/cos pair, source not yet identified`.

**Now believed.** `X = sin(yaw)·cos(pitch)·speed`, `Y = sin(pitch)·speed`,
`Z = cos(yaw)·cos(pitch)·speed`, with a planar branch that drops the pitch terms entirely.

**What proved it.** A byte-level trace of `002E4419`-`002E45A1`. The two `sinf`/`cosf` pairs are
not independent: `cosf(pitch)` is multiplied into `xmm8`, which is then the *common factor* for
both `sin(yaw)` and `cos(yaw)`. The decompiler renders this as three unrelated stores, and the
shared `fVar7` is easy to read as "speed".

**Why the earlier reading was reachable.** The two pairs really are computed in separate places
in the body, and the decompiler's variable naming (`fVar7` reused for both `speed` and
`speed*cos(pitch)`) hides the coupling. The GFZ annotation for this function makes the same
omission, so a reader checking the annotation against the decompilation would have found
agreement. **Two sources agreeing is not two pieces of evidence when one was derived from the
other's neighbourhood.**

### Correction 2 — K-5 was a transcription omission, not a missing code path

**Was believed.** *"Where the delta's `X` component is applied — the no-context path shown adds
only `Y` and `Z`. K-5 — this may indicate a third path or a decompiler artefact."*

**Now believed.** The no-context path adds all three. `*candidate_or_delta =
movement_state->flPosition_x + *candidate_or_delta;` is the first of the three lines in
`002E5610`.

**What proved it.** Re-decompiling `002E5610` in this pass. The line is present and always was.

**Why the earlier reading was reachable.** The `X` line uses `*candidate_or_delta` while the
other two use `candidate_or_delta[1]` and `[2]`; an excerpt built by pattern-matching the
indexed form drops it. It then survived because "the X term is missing" was *interesting* and got
written up as an open question instead of being re-checked. **A surprising negative should be
re-read before it is registered.**

### Correction 3 — the call chain was a nest; it is three siblings

**Was believed.**
`Movement_UpdateActorFrame -> Movement_UpdateSteeringTowardTarget -> Movement_ComputeDeltaFromHeadingSpeed
-> ... -> Movement_IntegratePositionAndMeasureDisplacement`.

**Now believed.** `Movement_UpdateActorFrame` calls steering (conditionally, when
`(u8)(mode - 1) < 4`), then the delta computation, then heading publication, then integration —
as four flat calls. `Movement_UpdateSteeringTowardTarget` calls neither of the other two.

**What proved it.** The fresh call graph: `002E4380` has one caller and it is `002E5030`;
`002E45E0`'s callee set contains neither `002E4380` nor `002E5610`.

**Why the earlier reading was reachable.** The nesting is the *conceptually* right order and the
functions are named as though they compose. Nobody checked the edges.

### Correction 4 — the "world-context pair" is a chain, and `mode` is always 0 from the frame path

**Was believed.** *"route through `002E5380` / `002E54A0` world-coordinate handling"*, presented
as a pair the integrator selects.

**Now believed.** `002E5610 -> 002E5380 -> 002E54A0`, one caller each. And
`Movement_PrepareCandidatePosition`'s own body is inert when `mode == 0`, which is what the
per-frame driver always passes — so the `+0xE8`/`+0xEC`/`+0xEF` and `+0x100..0x108` block
described nowhere in this document is unreachable from walking.

### Correction 5 — the observed-distance claim in the GFZ summary

§8's *"the GFZ annotation's own summary ... is **accurate**"* is **withdrawn** and replaced with
*"accurate only on the planar branch"*. The `+0xF8` half of that summary stands.

### Not a correction, but newly documented

The animation-state override (`00424080`), the heading publication into the ~~CharacterRenderObject~~ render-record
array (`002E5C10`) *(corrected 2026-10-02, OPUS: `022C6F28` + id × `0x740`, `002E5C33`–`002E5C4C`; §8f)*, the negative-sentinel repair at `+0xF8`, the displacement-measure switch, and
the `DAT_01DFE0BC` / `DAT_01DFE0B8` scalars are all mechanisms this document did not mention at
all. None contradicts what was written; all four change what a modder would do.

## 8e. The time-base triple appears in the locomotion path (cross-document)

`OPEN-QUESTIONS.md` carries **Z-10** (is `DAT_01DFE0B8` a speed-mode scalar?) as *REOPENED* and
**Z-11** (what does `0x01DFE0B4`-`0x01DFE0BC` hold?) as *ANSWERED — a time-base triple*, with the
recorded caution that *"nothing ties it to a player-facing speed control."*

**All three members appear in this document's mechanism, and this is new information for Z-10/Z-11:**

| Address | Shipped | Where it appears here |
|---|---|---|
| `01DFE0B4` (int) | `1` | `Movement_ModifyHeadingSpeedForObjectState`: the animation latch arms once a per-character counter reaches `(int)(_DAT_01DFE0B4 * 30)` — a **frame count** |
| `01DFE0B8` (f32) | `1.0` | `Movement_SetRequestedSpeed`: published locomotion rate `= DAT_01DFE0B8 * 30.0 * 3.6 * speed`; and `Spawn_SelectAndPrepareAutomaticEntry` converts raw ticks to seconds by dividing by `(int)(DAT_01DFE0B8 * 30.0)` |
| `01DFE0BC` (f32) | `1.0` | `Movement_SetRequestedSpeedScaled`: every authored speed is multiplied by it before reaching the state |

The `× 30.0` companion is the shipped constant at `008F8D80`, and it is used **as a frame rate**:
dividing a raw tick counter by `DAT_01DFE0B8 * 30` yields a value compared against a field named
`wRespawnCooldownTicks` and against `g_nSpawnKeepReturnWindow` (default `300`). At the shipped
scalar of `1.0` that makes the return window **300 seconds**.

**What this does and does not settle.** It ties the triple firmly to the engine's *time base* —
frames-per-unit, a rate scale and its reciprocal — and it shows `01DFE0BC` scaling authored
locomotion speed directly, which is the tie to something player-facing that Z-10 said was
missing. ~~It does **not** show the triple ever being written away from `1.0` during play;~~ The image writes it away from `1.0`: `001EDDC0` stores 2.0, 0.5 and 2 into `01DFE0B8` / `01DFE0BC` / `01DFE0B4` when its argument is non-zero *(corrected 2026-10-02, OPUS: `001EDDC4` `test ecx, ecx`, stores at `001EDDD8`, `001EDDE0`, `001EDDF2`; tail-jumped from `0022BDF0` at `0022BE7D`)*; the
single writer identified in audit pass 129 remains the only one. Registered as **K-8**.

## 8f. Correction, falsification pass 2 (2026-09-02) — a conflation of my own, caught before it propagated

**Was believed** (written in falsification pass 1, earlier the same day): that
`Movement_ModifyHeadingSpeedForObjectState` and `Movement_PublishHeadingState` index *the*
`CharacterRenderObject` array — the class documented in
[`../17-Presentation-Rendering/Character-Rendering/character-render-object.md`](../17-Presentation-Rendering/Character-Rendering/character-render-object.md) — and that the
render-object document therefore had to reopen to absorb a Presentation → Movement write-back.

**Now believed.** They index a **different** Presentation structure. The two are unrelated objects
that share a family resemblance and a similar symbol name.

| | `CharacterRenderObject` | the array these functions index |
|---|---|---|
| size | `0x668` = **1,640 B** | stride `0x740` = **1,856 B** |
| first field | vtable pointer `00903B68` | `i16` record id, compared against `-1` |
| allocation | one object at a time, `0x668` via `FUN_00210EC0` | one block of `0x48930` via `FUN_0036A100` |
| allocated by | `FUN_001BD4A0` (sole construction site) | `CharacterRenderSystem_AllocateAndInitialize` (`003325D0`) |
| count | cardinality not established | **exactly 160** |

**What proved it.** Four independent observations, any one of which is sufficient:

1. **The sizes differ.** `0x668 ≠ 0x740`.
2. **`cmp word ptr [rbx], -1` at `0042409F`.** The record's first two bytes are an id that can be
   `-1`. A `CharacterRenderObject` begins with a vtable pointer, which is never `-1`.
3. **No function in the binary references both.** An exhaustive memory-operand census over the
   exact body extent of all 38,161 functions finds the vtable `00903B68` referenced by exactly two
   functions (`CharacterRenderObject_Construct` and `FUN_001F51E0`) and the array base `022C6F28`
   referenced by 636 sites in a disjoint set. **The intersection is empty.**
4. **Different allocators, different call sites.** Neither `FUN_001BD4A0` nor
   `CharacterRenderObject_Construct` touches `022C6F28`.

**Why the earlier reading was reachable — and why it is the exact error this pass was created to
catch.** The decompiler renders the base as `g_pCharacterRenderRecordArray`. That is a GFZ-assigned
name; "CharacterRender" plus a large per-character stride plus a Presentation owner *looks* like
the class a Presentation document already describes. **That is "it looks like it belongs to X" —
banned as proof by the evidence standard — and it was committed in the same pass whose §10 boasts
of refusing address adjacency.** Refusing one banned inference does not inoculate against another
in a different costume. The tell was available at the time and not checked: the two sizes were both
written down, in two documents, and never subtracted.

**What is unaffected.** Every mechanical claim about the override itself — the `0x740` stride, the
by-reference rewrite of yaw and speed, the `0.83` decay to a `0.05` floor, the `+0x62C` latch, the
`_DAT_01DFE0B4 × 30` frame threshold, object state `0x0D` forcing speed to zero, and
`Movement_PublishHeadingState` writing `+0x240`/`+0x244`/`+0x248` — was read from the bodies and is
re-verified byte-exactly at `0042408A`-`004241A0`. **Only the identification of the container was
wrong.** The Presentation → Movement write-back is real; it simply belongs to a structure this
database has not documented yet, registered as **K-10**.

**What the correct structure is, as far as this pass establishes it.** A Presentation-owned array
of **160 records × 1,856 bytes** at the pointer `022C6F28`, with a dword at `base + 0x48830` and a
~~256-byte~~ 304-byte (`0x130`) trailer *(corrected 2026-10-02, OPUS: `003325E7` `mov ecx, 0x48930` allocates; 160 × `0x740` = `0x48800`; the 2026-09-19 propagation above)*, allocated and initialised by `CharacterRenderSystem_AllocateAndInitialize`. Its
sibling pointer `022C6F20` is written by `RenderSystem_RunCharacterUpdatePipeline` (`003323D0`).
The pass dispatcher `FUN_00332440` selects one of five stages by an integer argument, each pushing
an authored profiler label: **`"display character : preprocessing"`, `"display character : shadow"`,
`"display character : draw clip"`, `"display character : draw objects"`,
`"display character : after emission"`** (strings at `00D10A38`, `00D10A60`, `00D10A18`,
`00D10A80`, `00D10AA8`). Those five names are tier-2 evidence for what the array is *for*, and are
the natural starting point for the document it deserves.

## 9. Related

- [`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — the measured reach behind §8b
- [`../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md) — combat-side movement intent
- [`../17-Presentation-Rendering/Character-Rendering/character-render-object.md`](../17-Presentation-Rendering/Character-Rendering/character-render-object.md) — a **different** Presentation structure, 1,640 B and vtable-backed; §8f records why the two must not be conflated
- [`../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md`](../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md) — Movement owns the trigger there, not the mechanism
- [`../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — uses the identical `X = sin(θ)·r`, `Z = cos(θ)·r` convention and the same `atan2(dx, dz)` inverse
- [`../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) — carries the `01DFE0B8` reading that §8e extends

## 10. Falsification pass 1 — 2026-09-02

**Program state:** parent `2ed8affb…`, snapshot `46f02e26…`, embedded EXE `73461d08…`, ledger
38,161 / 38,003 / 158 unresolved, verified before any reading (`Verify-GfzCheckpoint.ps1`,
`CHECKPOINT VERIFIED`).
**Instruments:** `DumpFullCoverageGraph.java` regenerated fresh (38,161 functions);
`audit_crossrefs.py` against that graph; `DecompileAddressFileBounded.java` (83 bodies, 83/83);
and an **independent** instruction-level census — capstone over the exact body extent of every
one of the 38,161 functions, reading the authorized EXE directly, with 3 functions incompletely
disassembled and reported.

> **Instrument caveat and re-verification, 2026-09-02.** "Exact body extent" is the ledger's
> extent, and the ledger's extent is not always exact: **29 of the 38,161 functions carry a
> `body_bytes` that over-runs the next function's entry** (1,917 bytes in total), so a naive
> `entry + body_bytes` walk reads the *following* function's code as part of the first. The
> canonical example is `00350320` — ledger size 56, real function 11 bytes ending in a tail jump,
> then `int3` padding, then a different function at `00350330`.
>
> The census was rebuilt with the extent clamped to the next entry **and** truncated at the first
> `int3` following a terminator, and the two runs were diffed:
>
> | | raw extent | clamped | spurious |
> |---|---:|---:|---:|
> | call sites | 155,220 | 155,179 | **41** (0.026 %) |
> | caller→callee pairs | 110,611 | 110,580 | **33** (0.030 %) |
> | RIP-relative memory references | 164,489 | 164,460 | **29** (0.018 %) |
>
> **Every figure this document cites is byte-identical under both walks** — all ten call-count
> claims, the Movement share of the slot hub, every writer census and the empty vtable/array
> intersection. None of the 29 affected functions calls anything counted here. The diff is the
> positive control: the instruments genuinely differ, and the difference lands elsewhere.


### Killer observations named, and hunted

| Claim | What would kill it | Result |
|---|---|---|
| `X = sin(heading)·speed`, `Z = cos(heading)·speed` | any third factor multiplied into the `sinf`/`cosf` results before the store | **KILLED.** `cos(pitch)` is that factor. Rewritten. |
| `Y` comes from an unidentified second angle | finding the angle's source and its exact expression | **KILLED as an unknown.** `Y = sin(movementState[0xA0])·speed`. K-1 closed. |
| the delta's `X` is never applied | reading the no-context branch again, in full | **KILLED.** All three components are added. K-5 closed as a transcription error. |
| the chain `UpdateActorFrame → Steering → ComputeDelta → Integrate` | either arrow being absent from the current edge set | **KILLED.** Both arrows absent; they are siblings. |
| `002E5380` / `002E54A0` are a pair | one calling the other | **KILLED.** It is a chain, one caller each. |
| `W = 1.0` on every path | any exit that leaves `+0xC` alone | **SURVIVED.** Four exits, all write `0x3F800000`. |
| override stores the magnitude at `+0xF8` | `003A1D30` not being a square root | **SURVIVED and sharpened.** It is `sqrtf(fabs(x))`; K-3 closed. |
| class gate `(flags & 0xE0) == 0x60` | any movement-producing function without it | **SURVIVED and widened.** Present in five functions, and `Actor_GetWorldPosition` uses the same field with the wider `1 or 3` test. |
| §8b: Movement is the largest owned consumer of the slot hub, 11 sites / 10 callers of 46 / 40 | any row of the table failing to reproduce on a fresh graph or an independent counter | **SURVIVED exactly.** All eleven rows, both columns, reproduced twice by two different instruments. |
| §8b: Movement is 16 of 79 callers of `Actor_GetWorldPosition` | a different total or a different Movement share | **SURVIVED exactly.** 79 callers, Movement 16. |

### What was tried and failed to break it

- **Re-counted the `00236820` census two independent ways.** This was the most likely thing to
  break, because it had already been corrected once (edges-vs-sites). A capstone census over
  exact function extents — which never consults Ghidra's edge model — returned 46 sites from 40
  callers and Movement at 11/10. Nothing moved.
- **Attacked the class gate as possible caller-inheritance.** It is not: the mask and compare are
  in the callee bodies, five of them, at tier 1.
- **Attacked `W = 1.0` by enumerating exits.** The gate-rejection path, the override path, the
  `speed == 0` path and the normal path all store `1.0`; there is no fifth exit.
- **Attacked "the GFZ names are wrong" as a blanket suspicion.** Ten of eleven named addresses
  matched their bodies exactly. The one disagreement (`flCurrent_heading` at `+0xA0`) is recorded
  as K-6 rather than resolved by fiat.
- **Checked for banned evidence in the citation chain.** No `.pdata`, `.xdata`, unwind, EH-map or
  adjacency reasoning appears anywhere in §§2-8. The one adjacency-shaped observation available
  (`0208936C` sitting `0x2C` past the battle-state word) was deliberately **not** used; the
  grouping is asserted only where a single writer sets the whole group.
- **Ran a positive control on the absence claims.** Before reporting "`002E45E0` does not call
  `002E4380`", the same query was run for `002E5030 → 002E4380`, which returned the edge. The
  instrument works.

### Crossref findings, dispositioned

`audit_crossrefs.py` reported **3 findings** for this document, all `UNACCOUNTED NEIGHBOUR`, and
**zero** `GHOST ADDRESS`, `BODY DRIFT` or `CLASSIFICATION`.

| Finding | Disposition |
|---|---|
| `Audio` — `003A1D30` caller `00361810` | **Accounted for and now stated.** `003A1D30` is `sqrtf(fabs(x))`, a shared math leaf with 12 direct callers (17 sites) across Movement, Party, Script VM and Audio. §2 now says so. Not an Audio relationship. |
| `Rewards_Progression_Economy` — `0031B860` callers `002F8BB0`, `0030C650` | **Accounted for by reference.** `0031B860` is cited only inside §8c's hub table; its neighbours belong to `BattleUnit_GetBySlotIndex`, whose complete census lives in `cross-subsystem-accessor-hubs.md`. Not a Movement relationship. |
| `WorldAreaField` — `0030C210` callee `00377C20` | **Accounted for by reference.** Same: `0030C210` appears only as a row in the §8c hub table. |

**Second-order neighbours, and a property of the tool worth recording.** Re-running the audit
after this amendment dropped this document from **3 findings to 1**, and the one that remains is
an artefact of the disposition itself: quoting a finding verbatim puts the *neighbour's* address
into this document's own citation surface, so `00377C20` is now treated as cited here and its
callers are imported in turn.

| Residual finding | Disposition |
|---|---|
| `InputGameplay` — `00377C20` caller `00313A00` | **Not a Movement relationship.** `00377C20` is `FieldData_GetActiveFieldRecordBit15` (78 B), the real body behind the 5-byte thunk `00313F60`. It appears in this document only inside the quoted text of the row above; `00313A00` is one of its callers and has no relationship to locomotion. **Caller counts corrected 2026-09-02 — see the note below.** |

> **Correction: a caller count was attached to the wrong function.** This row originally gave the
> 78-byte predicate the thunk's caller count — the figure 47, which belongs to `00313F60`, was
> written against the body instead. Re-derived both ways against the current parent, and the two
> instruments agree exactly:
>
> | Address | Role | Distinct callers | Call sites |
> |---|---|---:|---:|
> | `00313F60` | 5-byte `JMP rel32` thunk | **47** | 67 |
> | `00377C20` | the 78-byte predicate, **excluding the thunk** | **65** | 79 |
> | union, distinct functions reaching the predicate by either route | | **110** | 146 |
>
> Two functions call both routes, which is why the union is 110 and not 112. Ghidra's edge model
> and a capstone census over exact body extents return the same 47 and 65; neither has address
> references, so there is no third route. **The selector must travel with the number** — "callers
> of the predicate" is ambiguous by 18 unless it says whether the thunk is included.
>
> The 65 and 110 figures in
> [`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) and
> [`../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md)
> **are correct and already carry their selectors.** `check_consistency.py` flagged a three-way
> disagreement; the odd one out was this document. Neither of the other two needs to reopen.

Also noted honestly: the `WorldAreaField` finding above stopped being reported not because this
disposition was written, but because the amended §2 contains a table whose header cell reads
`Field` — and `field` is one of `audit_crossrefs.py`'s aliases for that subsystem. **A finding
that disappears because of an incidental word is not a finding that was answered**, which is why
the row is dispositioned above on its merits rather than left to the alias match.

### Reopening propagation

- **`09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` should reopen.** §8e supplies new
  evidence bearing directly on its §8f / `Z-10` / `Z-11`: all three members of the `01DFE0B4`
  triple appear in the locomotion path, and `01DFE0BC` scales authored movement speed — the tie
  to a player-facing quantity that Z-10 recorded as missing.
- **`17-Presentation-Rendering/Character-Rendering/character-render-object.md` — WITHDRAWN.**
  This pass originally claimed the two Movement functions write into *that class's* array. They do
  not; the array is a different structure. The claim was retracted before it propagated — §8f
  carries the disproof, and the render-object document gets a "do not confuse with" note rather
  than a reopen.
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` is amended in the same pass and
  now cross-links the shared angle convention; no contradiction between the two.

## Extension 2026-09-07 — `K-6`: `movementState + 0xA8` is the facing angle, and it has exactly one writer

`xiionline-61`, GN160 `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`.

### What a player sees

Which way a character is **pointing** and which way they are **travelling** are not the same number,
and the engine stores them separately. That is why a character can back away from a foe while still
facing it, why a turn looks like a pivot rather than a slide, and why the direction the camera and
the targeting reticle agree on is the *facing*, not the motion.

### The field, and why it was the unnamed one

`K-6` recorded the problem exactly: the GFZ names `movementState + 0xA0` `flCurrent_heading` and
`+0xA4` `flDesired_heading`, while the engine's **canonical heading accessor**
`FUN_00265200` — **33 distinct callers** — returns neither. For actor class 3 it returns **`+0xA8`**:

```c
undefined4 FUN_00265200(WorldActor *a)
{
    if (a == 0) return 0;
    switch (a->classFlags >> 5) {            /* byte at actor + 3 */
        case 1: return *(float *)(a[0xB8] + 0x38);
        case 3: return *(float *)(a[0xB8] + 0xA8);
    }
    return 0;                                 /* every other class */
}
```

**Three angle fields, two names, and the one the rest of the engine reads is unnamed.**

### The single writer, and it is a wrap

A dataflow scan — *a register proven loaded from `[actor + 0xB8]`, then stored through at `+0xA8`* —
finds **exactly two** writers image-wide. One (`00266241`) writes a **qword**, which cannot be a
float field. The other is the answer:

```c
/* FUN_002E5E10(WorldActor *a, float angle /*XMM1*/, float aux /*XMM2*/, int commit /*R9D*/)  — 374 B, owner Movement
   (corrected 2026-09-11: four arguments, the third a float, and everything gated on the controller — see the correction) */
ctrl  = a[0xC0];                                       /* 002E5E49; a null actor still faults at 002E5E55 */
state = a[0xB8];
if (ctrl == 0) return;                                 /* 002E5E5F: no store, no callback */
bias  = (angle >= 0.0f) ? +pi : -pi;                   /* 01CEBC50 : 00915620; NaN takes -pi */
state[0xAC] = aux;                                     /* 002E5E88 */
state[0xA8] = ((angle + bias) - (float)(int)((angle + bias) / 2pi) * 2pi) - bias;   /* 002E5EBE; 01CEBC78 */
```

**That is a single sign-biased wrap aimed at `[-pi, pi]`**, written so that C's truncating cast
rounds toward the correct side on both halves. ~~It is the same result `Angle_NormalizeRadiansPi`
(`0033CB70`) produces, open-coded here rather than called.~~ **Corrected 2026-09-11:** it is *not*
that helper's result (the helper loops and leaves an exact `±pi` alone; this pass flips it), and it is
not a range guarantee — an exact endpoint changes sign, `+1.0` comes back as `3F800002`, ~~inputs of
magnitude `≥ 2^31 × 2pi` pass through unchanged~~ (**corrected 2026-09-12, EXP-074:** past the signed
conversion limit the pass adds `T = 2^31 × 2π` instead, and only from `|a| ≥ 2^58` does that round
away), and infinities and NaN do pass through. See the correction section below for the
instruction-level reasons and the controls.

> **`movementState + 0xA8` is the actor's facing angle in radians, and every write re-runs the
> wrap.** There is still only one writer; what the wrap guarantees is narrower than "in range".

### Setting a facing is not just a store

The rest of `FUN_002E5E10` is what a facing change *costs*:

```c
/* corrected 2026-09-11 — only reached when ctrl != 0; FUN_003DA850(p, f) is `*(float *)(p + 8) = f` */
FUN_003DA850(state + 0x50, facing);               /* state+0x58 = facing */
if ((a->flags0D & 0x20) == 0) {                   /* unless actor +0x0D bit 5 */
    FUN_003DA850(state + 0x70, facing);           /* state+0x78 */
    FUN_003DA850(state + 0x60, facing);           /* state+0x68 */
}
node = a[0xC0] ? a[0xC0][0x138] : 0;              /* the controller is re-read here */
if (node) {
    FUN_003DA850(node + 0xF0, facing);            /* node+0xF8 */
    FUN_003DAF20(node, (u8)state[0x104], (u8)state[0x105], (u8)state[0x106]);   /* zero-extended */
}
if (*(int *)ctrl != -1)                           /* ctrl = the pointer saved at entry */
    FUN_003EC260((u16)*(u16 *)ctrl, aux, facing, 0.0f, commit != 0);
```

~~Three or four sub-objects are pushed through `FUN_003DA850` on every facing change~~ **Corrected
2026-09-11:** `FUN_003DA850` is a six-byte store, so a facing change writes **one to four copies** of
the new angle — into `state + 0x58` always (given a controller), `+0x78` / `+0x68` unless actor
`+0x0D` bit 5 is set, and the controller node's `+0xF8` when that node exists — then rebuilds the
node's placement (`FUN_003DAF20`) and updates the render record's `{aux, facing, 0, 1}` group
(`FUN_003EC260`). Bit 5 is an exemption from two of the copies, not from an "invalidation".

~~`FUN_002E5F90` … sets nothing new~~ **Corrected 2026-09-11:** the wrapper
`FUN_002E5F90(a, float aux, int commit)` keeps the field's own facing but **sets a new `+0xAC`** from
its second argument and re-runs the callbacks; and since the wrap is not idempotent, re-applying an
exact `±pi` flips its sign. Its mirror `FUN_002E5FB0(a, float angle, int commit)` keeps `+0xAC` and
sets a new angle.

### Correction 2026-09-11 — the writer's ABI, its gate, its wrap and its callbacks (ASTRA-CONTRA-FABLE-FACING-WRITER)

ASTRA's [EXP-072](../_experiments/EXP-072-facing-writer-controls.md) executed the original 374 bytes
of `FUN_002E5E10` in isolation with the three callees stubbed (isolated original-code execution — not
live, and the callees' native effects are not part of it) and contradicted four statements above. My
re-reading of the bytes (tier 1, static) agrees with every one and adds the callees' bodies, which
change what a facing write *is*. The prose above is kept as written, with this section as the record.

**Four arguments, not three, and the third is a float.** The body saves `XMM2` into `XMM8`
(`002E5E3A`) and `R9D` into `R14D` (`002E5E37`); `R8` is never read. So the signature is
`FUN_002E5E10(WorldActor *a, float angle /*XMM1*/, float aux /*XMM2*/, int commit /*R9D*/)`. `aux`
is stored to `state + 0xAC` unchanged (`002E5E88`) and later forwarded to `FUN_003EC260`; `commit`
only matters as "zero or not" (`002E5F42`–`002E5F4B`, `setne`) and travels as that callee's fifth
argument.

**Everything is gated on the controller.** `a[0xC0]` is loaded once into `RDI` (`002E5E49`); when it
is null the body jumps straight to the epilogue (`002E5E5F` → `002E5F61`): **no store to `+0xAC`, no
store to `+0xA8`, no callback**. "Always" above was wrong for that case. The `test rcx, rcx` at
`002E5E44` only chooses `RDI = 0`; `[rcx + 0xB8]` is still read at `002E5E55`, so a null actor faults
rather than returning — the guard is not a null-actor guard.

**The wrap is a single sign-biased pass, not a range guarantee.** Every step is a binary32 operation
with its own rounding: `addss` (`002E5E84`), `divss` by `2pi` (`002E5E98`), `cvttss2si` (`002E5EA0`),
`cvtdq2ps`, `mulss` by `2pi`, two `subss`. Consequences, each visible from the instructions and
confirmed bit-for-bit by EXP-072's twenty-five controls:

| Input | Stored | Why |
|---|---|---|
| exactly `+pi` (`40490FDB`) | `-pi` | `(pi + pi) / 2pi = 1` truncates to `1`, `2pi − 2pi = 0`, `0 − pi` |
| exactly `-pi` | `+pi` | the mirror; so **re-applying the field at either endpoint flips its sign** |
| `+1.0` (`3F800000`) | `3F800002` | `1 + pi` rounds, `− pi` does not round back |
| `-0.0` | `+0.0` | `(−0 + −pi) − (−pi)` |
| `±2pi` | `∓2^-22` (`B4800000` / `34800000`) | the residual of the rounded sum |
| `≈ ±1e20` | unchanged | `q = ±1.6e19` overflows `cvttss2si` to the integer indefinite `80000000` = `−2^31`, so `p = −T` and the pass computes `f32(a + T)`; **at `1e20` that addition is below half an ulp and rounds away — absorption, not pass-through** (corrected 2026-09-12, see below) |
| `±inf`, quiet NaN | stored as is | no comparison rejects them; NaN takes the `-pi` bias (`COMISS` unordered → `JB`) |

For small finite inputs the result does land in `[-pi, pi]`; for `|angle| ≥ 2^31 × 2pi ≈ 1.35e10`
(where the stored value is `f32(a ± π + T) ∓ π` — `2T` at the positive limit — until `|a| ≥ 2^58`
collapses it back to the input), for the exact endpoints, and for non-finite input it does not. The
largest input for which the wrap lands in range is not derived here.

> **CORRECTED 2026-09-12 (ASTRA-CONTRA-FABLE-ANGLE-OVERFLOW, EXP-074) — the large-angle row above was
> generalised from the only inputs that had been executed, and it is wrong everywhere else.**
> *"Inputs of magnitude `≥ 2^31 × 2π` pass through unchanged"* held for `±1e20` because at that
> magnitude adding `T` is below half an ulp; it does **not** hold from the conversion limit up to
> `2^58`. The arithmetic, every step a binary32 operation:
>
> ```
> s      = f32(a + bias)                        bias = (a >= 0) ? +π : −π      (writer only; the helper starts at q)
> q      = f32(s / 2π)
> k      = trunc(q)   if −2^31 <= q < 2^31,  else −2^31    (cvttss2si: the integer indefinite 80000000)
> p      = f32(f32(k) × 2π)                     = −T when the conversion is invalid, T = 50490FDB = 13,493,038,080
> stored = f32(f32(s − p) − bias)               invalid conversion ⇒ f32(f32(s + T) − bias)
> ```
>
> **The boundary is signed, not a magnitude.** `−2^31` is a *valid* conversion and `+2^31` is not.
> ASTRA's [EXP-074](../_experiments/EXP-074-angle-conversion-boundary.md) executed the shipped
> 374-byte writer and the 128-byte helper at ten new inputs (isolated original-code, recording stubs,
> the pass-through mutant detected); the writer column is what this function stores:
>
> | input | stored by the writer | by the helper `0033CB70` | why |
> |---|---|---|---|
> | `T − 1024` (`50490FDA`) | `−π` | `0` | quotient 2,147,483,520, valid |
> | `T` (`50490FDB`) | **`2T`** (`50C90FDB`) | `2T` | `+2^31` is invalid → `p = −T` |
> | `T + 1024` | `2T + 1024` | same | positive overflow |
> | `−T + 1024` (`D0490FDA`) | `+π` | `0` | valid |
> | `−T` (`D0490FDB`) | **`+π`** | **`0`** | `−2^31` **is valid**, though its bits equal the indefinite |
> | `−T − 1024` (`D0490FDC`) | `−1024 + π` (`C47F36F0`) | `−1024` | negative overflow |
> | `≈ ±1.4e10`, `≈ ±1e11` | `a + T` (`50CCD6CF` / `CDF1BD00`, `51D365B2` / `D1A121BC`) | same | overflow |
>
> Every one of the ten is reproduced by emulating the instruction sequence in binary32 with the
> indefinite rule above (FABLE, 2026-09-12); the same emulation gives the absorption threshold the
> experiment deliberately did not derive: **`f32(a + T) == a` exactly when `|a| ≥ 2^58 ≈ 2.9 × 10^17`**
> (at `2^57` `T` is 0.785 ulp and the sum moves; at `2^58` it is 0.393 ulp and rounds away) — so the
> `±1e20` row is absorption, and between `1.35e10` and `2.9e17` the stored facing is a large wrong
> angle, not the input. Derived, not executed: the ten executed points bracket it but do not test it.
> **Reconstruction rule:** truncate through a 32-bit integer with the indefinite value on invalid
> conversion; a `truncf`, a 64-bit truncation, a saturating conversion or a pass-through all diverge
> from the original immediately past `1.35e10`. Nothing here says the shipped game ever produces such
> an input.


**It is not `Angle_NormalizeRadiansPi`'s result.** `FUN_0033CB70` (`0033CB70`–`0033CBEF`) is a
different algorithm: only when `|x| > 4pi` (`00D10B0C` / `00D10B20`) does it take the truncating
division ~~, and then it **loops**~~ and returns without a loop, leaving a result in `(−2pi, 2pi)` (`0033CBCD`–`0033CBEF`); only an input within `±4pi` **loops** *(corrected 2026-10-02, OPUS: `0033CB73` / `0033CB84` jump to `0033CBCD` beyond `±4pi`)* — `addss −2pi` while `x > pi` (`0033CBA0`–`0033CBA7`), `addss +2pi`
while `x < −pi` (`0033CBC0`–`0033CBC7`) — and leaves an exact `±pi` untouched. The facing writer
never loops and flips the endpoints. "The same result, open-coded" is withdrawn; the two agree only
on inputs where a single biased pass suffices.

**`FUN_003DA850` is a six-byte store, not an invalidation.** Its whole body is
`movss [rcx + 8], xmm1; ret` (`003DA850`–`003DA855`). Each call therefore writes **a copy of the new
facing** into a sub-record: `state + 0x58` (via `state + 0x50`, `002E5EC6`), and unless actor
`+0x0D` bit 5 is set, `state + 0x78` and `state + 0x68` (`002E5ED8`, `002E5EE4`); then, when the
*re-read* `a[0xC0]` and its `+0x138` node are both non-null, `node + 0xF8` (`002E5F0B`). That is
**one to four copies** — one when bit 5 is set and there is no node — not "three or four".
`FUN_0026B520`'s class-1 branch writes the same wrapped angle straight into `state + 0x54` /
`+0x58` (`0026B58D`–`0026B592`), which is consistent with `+0x58` being a facing copy.

**`FUN_003DAF20(node, u8 s104, u8 s105, u8 s106)` rebuilds the node's placement from that copy.**
The three bytes arrive zero-extended (`movzx`, `002E5F17`–`002E5F27`). The body takes `cosf` /
`sinf` of `node + 0xF8` (the copy just written) into `node + 0x40` / `+0x48` with `+0x44 = 0`,
`+0x4C = 1.0` (`003DAF3C`–`003DAF7A`), copies `+0xF0` / `+0xF4` / `+0xE0` to `+0x94` / `+0x98` /
`+0x9C`, and writes `+0xA0 = s104 × [+0xF0] / 50`, `+0xA4 = s106 × [+0xF4] / 50`,
`+0xA8 = s105 × [+0xE0] / 50 + [+0xE4]` (`003DAFA9`–`003DB000`; `50.0` at `008F3130`). So the
three state bytes are percent-of-fifty scale factors applied to the node's extents.

**`FUN_003EC260` receives the controller's low word unsigned, plus four more arguments.** The call
site is `movzx ecx, word ptr [rdi]` (`002E5F3F`) — the *saved* controller pointer, not the re-read
one — so a first word of `0xFFFF` arrives as `65535`, `0x8000` as `32768`; only a whole first dword
of `-1` skips the call (`002E5F3A`). Inside, the callee compares `cx` with `-1` and sign-extends it
(`003EC267`, `003EC276`) as an index into the `0x740`-byte render records at `[022C6F28]`, so the
`0xFFFF` case is rejected there as well. The remaining arguments are `XMM1 = aux`,
`XMM2 = the wrapped facing`, `XMM3 = 0.0f`, and the stack fifth `= (commit != 0)`. The body, for a
record whose `+0x284` is non-zero: with `+0x290` bit 20 clear and word ~~`+6 == -1`~~ `+6 != -1` (and `+0x284` bit 27 clear; with that bit set such a record returns untouched) *(corrected 2026-10-02, OPUS: `003EC2AA`–`003EC2BB`, then `003EC2C1` `cmp word [rbx+6], -1` / `je` to the staging path; the reset `003EC2C8`–`003EC2D5` runs only for `+6 != -1`)* it zeroes the
four-lane group `+0x120..+0x12C` to `{0, 0, 0, 1.0}` and returns; otherwise it compares
`{aux, facing, 0}` with `+0x120 / +0x124 / +0x128` and, when any lane differs, clears `+0x284`
bit 9, moves the old lanes to `+0x250 / +0x254 / +0x258` and stores the new group with `+0x12C =
1.0` (`003EC316`–`003EC358`). When `commit` is set it snaps `+0x250..+0x258` to the current lanes,
calls `FUN_004288B0(record, -1)` unless `+0x284` bit 17 is already set (that callee sets `+0x290`
bit 10 and `+0x284` bit 17 and zeroes byte `+0x40A`), and, if `+0x288 != -1`, tail-calls
`FUN_003B3CA0(+0x288, 30)`. The render record therefore holds the facing as lane 1 of a
`{aux, facing, 0, 1}` group with a previous-value copy — the first reader of `+0xAC`'s value found,
which narrows `K-13` (below).

> **K-13 answered 2026-09-12 (FABLE): `+0xAC` is the actor's pitch — the rotation about the X axis
> that the model transform applies beside the heading.** The consumer of the four-lane group is
> `CharacterRenderRecord_ComposeModelTransformFromParent` (`00420A40`): it loads `+0x120` / `+0x124`
> / `+0x128` into `XMM1` / `XMM2` / `XMM3` (`00420BE4`–`00420C00`) and calls
> `Matrix4x4f_BuildEulerRotation(record + 0x180, a1, a2, a3)` (`0046D380`), then multiplies the result
> by the scale and parent transforms (`00420C17`, `00420C4A`). The builder divides each angle by `2π`
> (`01CEBC78`), scales by `32768` (`00D10820`) into a 32,768-entry sine table at `01F004E0` (cosine =
> the entry a quarter turn on, `0x2000 − i`), and writes the row-major matrix `[c2c3, c2s3, −s2 /
> s1s2c3 − c1s3, s1s2s3 + c1c3, s1c2 / c1s2c3 + s1s3, c1s2s3 − s1c3, c1c2]` (`0046D49F`–`0046D550`),
> which with `a2 = a3 = 0` is a rotation about **X**, with `a1 = a3 = 0` about **Y**, and with
> `a1 = a2 = 0` about **Z**. Y is up in this engine (§3's `Y = sin(pitch) × speed`), so lane 1 — the
> facing — is the yaw, lane 0 — `+0xAC` — the pitch, and lane 2 the roll, always 0. **Its accessor and
> its writer.** `FUN_002651C0(actor)` (`002651C0`) is the mirror of the facing accessor
> `FUN_00265200`: for class 3 it returns `movementState + 0xAC`, for class 1 the bound object's
> `[+0xB8] + 0x54` ([the slot pool and actor class](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md)). `FUN_0026B520(actor, angle, commit)` is its setter — for class 3 it
> wraps the angle and tail-jumps into `002E5F90` as `aux`, for class 1 it writes the wrapped angle to
> that object's `+0x54` and `+0x58` (`0026B586`–`0026B592`). Both are used once: the per-actor update
> `FUN_002E5750(actor, flag, float pair[2])` (`002E5750`, called from
> `WorldActor_UpdateRuntimeAndScriptExecutionState` at `0025E3AA`) adds `pair[1]` to the facing
> (`00265200` → `0026B6A0`) and `pair[0]` to the pitch (`002651C0` → `0026B520`) when `flag` is set
> (`002E5783`–`002E57BE`); the flag is bit 0 of what `003E6A70` reports for the actor's render record
> (`0025E35A`–`0025E36E`). *Limits:* the pair's producer inside `0025DF00` is not read; the class-1
> object behind `+0xB8` is described only by its two offsets; all static.
>
> *Update 2026-09-20 (FABLE): what FILLS the producer is authored command `0x1A` and the `@FRM` profiles -
> [how an animation moves and turns a character](how-an-animation-moves-and-turns-a-character-toward-its-target.md).*
>
> *Update 2026-09-15:* the pair's producer is now read — `003E6EF0` → `003AF220` computes
> `min(step, |v|)·v̂` into the `rsp+0x30`/`rsp+0x40` out-structs, gated per linked render record
> (`+0x284` match on `022C6F28`). See [the `0025DF00` subtree §13](../04-Actor-Entity/the-field-runtime-pass.md).

**The wrapper sets something new.** `FUN_002E5F90(a, float aux /*XMM1*/, int commit /*R8D*/)`
loads the field's own `+0xA8` as the angle and passes *its caller's* `XMM1` as `aux`
(`002E5F90`–`002E5FA5`): it is "keep the facing, set `+0xAC`, re-run the callbacks". And because the
wrap is not idempotent, re-applying the field at an exact endpoint flips its sign and at other values
can move it by an ulp. The mirror wrapper `FUN_002E5FB0(a, float angle, int commit)` keeps `+0xAC`
and sets a new angle (`002E5FB0`–`002E5FC2`). The two direct callers, `002E28E0` (`002E2C53`–
`002E2C6C`) and `002E6B10` (`002E6B69`–`002E6B82`), both re-apply `(+0xA8, +0xAC, commit = 1)`
right after the position setter `FUN_002E5C90`; `FUN_0026B520(a, float angle, commit)` wraps the
angle itself with the same arithmetic and, for class 3, tail-jumps into `002E5F90` with the wrapped
angle **as `aux`** (`0026B57B`–`0026B581`).

**Evidence tiers.** Everything in this section is static reading of the bytes cited, except the
stored-bit table, which EXP-072 also produced by executing the original body with recording stubs
(its checker mutates `002E5F3F` to `movsx` as a positive control and detects it). No claim here is
live, and the callees' native effects (`003DAF20`'s trigonometry, `003EC260`'s render-record work)
are static only. EXP-073 (ASTRA, in progress) is to execute the wrapper.

### How this sits against the movement formula, and what is still inference

`K-1` established the position delta as a spherical decomposition over
`yaw = wrap(movementState[0xA4])` and `pitch = wrap(movementState[0xA0])`.

> **So the two named fields drive *motion*, and this unnamed third field is what the engine reports
> as *facing*.** That reading is consistent with every reader found and with `FUN_00265200`'s 33
> callers, and it is **an inference from combining two results, not a single reading.** No function
> observed here writes `+0xA8` from `+0xA4` or vice versa, and the relationship between them —
> whether facing follows motion, leads it, or is independent — **is not established.** Recorded as
> `K-11`.
>
> **K-11 answered 2026-09-12 (FABLE): independent in the movement code — facing is commanded, motion
> yaw is steered, and only the battle and script layers couple them.** *Facing side.* A
> function-list-independent `E8`/`E9` index gives `FUN_002E5E10` exactly **four** call sites, so the
> "prove none exists" half is closed over the complete set: `002E2C6C` (`002E28E0` — its 11-member
> exclusive subtree is bound on
> [the script-naming page](../01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md) §4c) and `002E6B82`
> (`002E6B10`) pass `xmm1 = [state + 0xA8]` — the **current** facing, re-committed after the
> position reset `002E5C90` — with `xmm2 = [+0xAC]` and `commit = 1`; `002E5F90` is a wrapper that
> keeps the current facing and supplies only `aux`; and `002E5FB0` is the wrapper that supplies a
> **caller's** angle (`xmm1` untouched, `aux = [+0xAC]`, `commit = r8`). No site reads `+0xA4`, and
> the angle that reaches `002E5FB0` comes through `0026B6A0` from `Actor_SetFacingHeading_Variant0`
> (`0026B5A0`) and `_Variant1` (`0026B620`) — whose callers are the **battle** layer
> (`BattleUnit_ApplyMovementIntentToWorldActor` `0023A070`, `BattleUnit_PublishLocomotionPose` `003003F0`,
> `00239210`, `00304180`, `0024C6B0`, `0024C870`, `0024F9B0`, `0026C120`, `00341AB0`, `0034BE50`) — and
> from the actor update `002E5750` under `WorldActor_UpdateRuntimeAndScript` (`0025DF00`), the
> **script** side. *Motion side.* `+0xA4` (and the pitch `+0xA0`) is written by
> `Movement_UpdateSteeringTowardTarget` at `002E4797` / `002E479F` as the output of
> `003A1AD0(current, target, rate)` — the current yaw `[+0xA4]`, a **target yaw** that `003A19C0`
> derives from a direction vector (the target-position delta from `003DA6A0`, or the steering
> record's own vector, `002E4681`–`002E46E1`), and a rate from the steering parameters `[+0xF0]+0x50`
> — a smoothing toward the target direction, and the function never reads `+0xA8`. So neither
> field is ever written from the other: the yaw the position delta uses follows where the actor is
> steering, while the facing the accessor reports is whatever the last intent or script verb set.
> "Backing away while still facing a foe" is exactly that: `BattleUnit_ApplyMovementIntentToWorldActor` sets
> the facing explicitly while steering carries the yaw away. Whether the battle setters compute
> their angle from the target's position is the battle layer's question, not this page's.

**No renaming is proposed for `+0xA0`/`+0xA4`.** `K-6` asked which of the two GFZ names is wrong; the
answer is that the question was malformed — **the pair is not a complete account of the group**, and
the field that needed a name was never in it.

### Method note

The first scan for writers used *co-occurrence* — a function that stores to `[reg + 0xA8]` and
somewhere also loads `[reg + 0xB8]` — and returned **283 of 450 sites**, which is no signal at all:
`0xA8` and `0xB8` are ordinary struct offsets and almost any large function touches both. The
dataflow version tracks the register actually loaded from `+0xB8` and finds **2**.

**The positive control is what made the second scan trustworthy**: it was run first against
`FUN_00265200`, whose read of `+0xA8` is already known, and it found it. A scan that cannot find its
own control is not evidence about anything else.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Resource — SERVICE.** `CharacterRenderRecord_ComposeModelTransformFromParent` (`00420A40`) looks up an entry
through `ResourceTable_ResolveEntryByIndex`. It is a table lookup on the render side and does not feed the
heading-to-delta arithmetic.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT, 12 edges.** Cited functions are called by `BattleStats_RemoveStatusesFromMaskAndRecompute`, `BattleStats_ChangeStatusAndProcessSideEffects` and `BattleUnit_RunPeriodicCombatMaintenance` (twice each), and by `BattleUnit_AddPrimaryResourceRecoveryAccumulator`. One calls `BattleStats_RecomputeDerivedStateAndAutoStatuses`.


**Presentation — CLIENT and SERVICE (SWE2-EC7-156, 157 edges).** `001BD4A0` is called by `001BC190`/`001D5xxx` and calls `001F4DA0`/`001F89E0` of that layer; batch-121's `0022F250` helpers `00202B70`/`00202B90`/`00808C40`/`00861F14` share the exchange — two-way helper fan-in, not a second owner.

**ActorEntity — MECHANICAL (SWE2-EC7-169, 112 edges).** The workbench primitives the
cell solver's bodies name — `00203170`, `00202B70`, `00202D70` and the `00236820`/
`00239210` accessors — are called from the actor layer (`003F1E90`, `0031B770`,
`00321170`, `0031B810` among 112 edges): shared-math fan-in, not an actor
relationship of the solver.

**Gameplay — MECHANICAL (SWE2-EC7-169, 18 edges).** The same shared primitives
(`00202B70`, `00203170`, `00202E10`, `00203080`) are called from gameplay code
(`00339630`, `0030C210` among 18 edges) — fan-in.

**Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-169, 196 edges).** `00203170`,
`00202B70`, `0025DF00` and `00239210` reach that layer (`00356160`, `00510760`,
`0025E4C0` among 196 edges) — the script bridge drives the same primitives; fan-in.

**UI — MECHANICAL (SWE2-EC7-169, 26 edges).** `00202D70`/`00203170`/`00202E10`/
`00203080` are called from the UI layer (`00247AE0`, `002D2600`, `005512B0`,
`0027BED0` among 26 edges) — shared-math fan-in.
- **Audio - CLIENT and SERVICE (12 edges).** `00203080`, `00265020` are also called by bodies filed to audio: `00362850`; `0030C650` reaches bodies filed to audio: `002DF220`, `003A1180` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (14 edges).** `00236820` is also called by bodies filed to combat AI: `00301AD0`, `00308C20`, `003219D0` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT and SERVICE (45 edges).** `00236820`, `00265020` are also called by bodies filed to combat formula: `0031B860`, `0031E800`, `00384F40`; `002F8BB0` reaches bodies filed to combat formula: `0031B860` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (4 edges).** `003323D0` is also called by bodies filed to core runtime: `0022A770`, `0022B8C0`; `0025DF00` reaches bodies filed to core runtime: `001EDDA0`, `001EDE80` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT (3 edges).** `00313F60`, `003590D0`, `00377C20` are also called by bodies filed to input: `00253C70`, `00226BE0` (ActorControlMaskPropagationRuntime) - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT (1 edge).** `00377C20` is also called by bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (7 edges).** `00236820`, `0031B860` are also called by bodies filed to items/equipment: `0031A300`, `0031A410`, `0031A510` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (35 edges).** `00236820`, `00264010` are also called by bodies filed to party: `003261D0`, `003273D0`, `00353530`; `00264010` reaches bodies filed to party: `003590D0` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `00239210` reaches bodies filed to random selection: `00328370` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT and SERVICE (11 edges).** `00265020`, `002F8BB0` are also called by bodies filed to rewards/progression: `002FB150`, `00312280`; `0030C650` reaches bodies filed to rewards/progression: `002F9A60` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (9 edges).** `00236820`, `00265020` are also called by bodies filed to spawn/encounter lifecycle: `00308D90`, `00234AF0`, `00234DA0` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (4 edges).** `002E5180`, `003590D0` are also called by bodies filed to World: `0025E400` (ActorManager), `002623A0` (ActorManager) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (12 edges).** `002E28E0`, `00304180`, `0030C210` reach bodies filed to WorldAreaField (world area): `00377C20` - shared machinery across the layer boundary, no shared ownership.

## The `00348F80` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00348F80` (~160 B) — `xmm6`-save vector body, `rcx = r9`
(`00348F8F`/`00348F94`).

| member | role | interior |
| --- | --- | --- |
| `0026B230` | `(byte[+3] & 0xE0) == 0x60` record-kind test — same selector as `0026AE90` (`0026B230`/`0026B23C`) | [`0026B230`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `002E9FE0` (2026-09-18, SWE2-EC7)

`002E9FE0` — 73 B, 9 A-measured callers; the eligible-again predicate the heading writer
consults. Interior verified: `byte[rcx+3] & 0xE0` must equal `0x60` (tag class 3) else
returns 1 unconditionally ([`002E9FFC`](../_index/ADDRESS-INDEX.md) falls through on tag match); for a tagged
record the linked object `[+0xC0]` must be non-null with `[+0x164] == 0`, and the byte pair
`[+0x10]`/`[+0x11]` is tested two ways — `[+0x11]&0x20` set requires `[+0x10]&3 == 3`,
clear requires `[+0x10]&0xB == 0xB` — with `[+0x11]&6 == 6` as the final gate. Returns 1
(eligible) or 0.

## Interior citation — frontier hub `0026D6F0` (2026-09-18, SWE2-EC7)

`0026D6F0` — 275 B, 7 A-measured callers; `Movement_SetRequestedSpeed`, the speed half of
this contract. Interior verified: tag `byte[rcx+3] & 0xE0 == 0x60` gates the write
(`0026D70E`); `xmm6` lands on `[+0xB8]->[+0xF0]+0x24` and on `[+0xD0]` at
[`0026D72C`](../_index/ADDRESS-INDEX.md)/`0026D750`, with `[+0xC]` bit 4 set when the value changes under
`r8d == 2`. A scaled copy (`xmm6 * 1.0 * 0xB1` band constants) is pushed to
`[+0xC0]->[+0x138]+0x30 -> +0x98` when that chain resolves (`0026D764`–`0026D792`), then
`002E9BB0` supplies the flag word — `+0x12 <= 3` and `xmm6 == 0` sets bit 2, `003590D0()` /
`003588B0` self-compare sets bit 10 and `esi == 1` clears bit 3 — and `002EC5B0(rcx, flags)`
publishes at `0026D7E9`.

## Interior citation — frontier hub `004692F0` (2026-09-18, SWE2-EC7)

`004692F0` — 46 B, 8 callers; a two-stage movement-math helper. It calls `00469320(rcx)`
first (the guard/resolve step), then tail-jumps to `00202FE0` with `rdx = rcx` and the
caller's `xmm1` carried through `xmm6` ([`00469319`](../_index/ADDRESS-INDEX.md)) — the
delta apply step this page's "heading · speed → Δposition" chain ends in.


### Interior citation — frontier hub `002EA7F0` (2026-09-18, SWE2-EC7)

`002EA7F0` — 117 B, 6 callers: the movement-permission predicate. All gates
must pass — `[rcx+0x18] != 1`, `[+0xC0]` live, `[+0x14F] & 1` clear,
`[+0x138]` live with `[+0x138 +0xF0] > 0.0f`, `byte[rcx+8] & 8` set — then
`002E9FE0(rcx)` at [`002EA844`](../_index/ADDRESS-INDEX.md) or
`byte[rcx+4] == 3` decides: 1 only on a hit. The can-move test the steering
paths consult.
## SWE2-EC7-18 update (2026-05-15) — `003A1D30` magnitude-store stage

`003A1D30` (23 B) is the `sqrtf(fabsf(x))` leaf this page's Audio crossing already names: `cvtss2sd` promotes `xmm0`, `andps` with `[01CEBD80]` (`0x7FFFFFFFFFFFFFFF` — the absolute-value mask, `003A1D37`), `cvtpd2ps` narrows back (`003A1D3E`), then `jmp 00861F14` (`003A1D42`) — the shared `|x|`-then-sqrt tail the movement-state writers call, which is why the movement-and-secondary-context page shows `003DA730`+`003A1D30` paired in its steering-angle stage.

## SWE2-EC7-23 update (2026-09-18) — `003A1AD0` angle-delta normalizer

`003A1AD0` (217 B) is the delta normalizer the heading math shares:
`xmm4 = xmm1 - xmm0`, `xmm5 = [00915620]` (-pi-class bound) with the
`addss [01CEBC78]` (2pi-class) wrap-up loop, then the `comiss` against
`[01CEBC50]` (+pi) wrap-down — the signed-delta -> (-pi, pi] normalization
the steering evaluators call. Interior anchor `003A1B0B` (the first bound
compare). Sibling of `0026B5A0`'s wrap-and-quantize, which this page's
steering contract also names.

## SWE2-EC7-26 update (2026-09-18) — `00316DA0` heading-add wrap

`00316DA0` (74 B) computes `wrap(x0 + x1)`: adds the angles and folds
into [-pi, pi] by the same +/-pi constant pair (`00915620`/`00915624`)
as `0031A930`, without the absolute-value tail — the raw wrapped sum
heading arithmetic uses. Interior anchor `00316DA8` (the add).
## SWE2-EC7-31 update (2026-09-18) — `00264460` 3-D test, verified

`00264460` (37 B) is the 3-D test this page's K-7 answer already
describes — and the bytes confirm the description: it returns 0
when `rcx` or `qword[rcx+0xC0]` is null, else reads
`byte[ctx+0x151]` and answers `(b | b>>1) & 1` — true when either
of the controller's low two bits is set. Interior anchor `0026447A`
(the `shr`/`or`/`and` fold).

## SWE2-EC7-44 update (2026-09-19) - `0024C6B0`

`0024C6B0` (261 B) is a body - `0024C870`/`0026A3A0`/`0026A430`/`0026AF80`/`0026B5A0`/`003588B0`/`003B7E10`. Interior anchor `0024C6EE` (a `0024C870` call).

## SWE2-EC7-45 update (2026-09-19) - `0024C870`

`0024C870` (242 B) is a body - `0024C6B0`/`0026A3A0`/`0026A430`/`0026AF80`/`0026B5A0`/`003588B0`/`003A6D90`. Interior anchor `0024C8AE` (a `0024C6B0` call).

## SWE2-EC7-46 update (2026-09-19) - `0034BE50`

`0034BE50` (233 B) is a body - `00264010`/`00265020`/`00265200`/`00267DB0`/`00267E10`/`00267F60`/`0026C090`. Interior anchor `0034BE76` (a `00264010` call).


## SWE2-EC7-65 update (2026-09-19) - `0026BA70`

`0026BA70` (137 B) is a kind-1 divert body - `0026B170` single call. Interior anchor `0026BA79` (a `0026B170` call).


## SWE2-EC7-104 update (2026-09-20) - `0026B2E0` + `0026AFE0` measured

`0026B2E0` (365 B) is the blend-and-clamp pass
`002E28E0` and `002E8E20` call on the
`byte[+3] >> 5` class dispatch: class 2 runs
`003DA860` over the `[+0x50]` / `[+0x80]`
halves of the `[+0xB8]` record, blends
`base20 * xmm9 + base28 * xmm8`, halves the
sum, clamps it against the `008F30E4` floor
and writes the result to `[+0xFC]` (class 2)
or `[+0x70]` (class 1); class 1 runs the same
`003DA860` on `[+0x30]` with `1.0f`
constants. When the class byte is `0x60`
(class 3) it additionally runs `003DA890` on
`[+0x70]` and `[+0x60]` against `[+0x50]`
wherever the `+0xDE` / `+0xDF` flags are
armed, then tails `00268380`.
Interior anchor `0026B34E` (the first
`003DA860` call).

`0026AFE0` (222 B) is the sibling class
dispatch `0026AF80` and `002E45E0` call:
class 2 either runs `002EB930` then
`002E5C70` (stack arg nonzero) or `002E5DF0`
alone; class 1 splats the `xmm8 / xmm7 /
xmm6` float3 three times into the `[+0xB8]`
record's `+0x00 / +0x10 / +0x20` rows and
sets `byte[+0x5D] |= 1`. It then walks
`[rcx + 0xC0] -> [+0x138]` when
`byte[rcx + 0x18] == 1`, runs `003DA9F0`
on the resolved record and clears its
`+0xEF` byte.
Interior anchor `0026B021` (the `002EB930`
call).

## SWE2-EC7-105 update (2026-09-20) - `003DA890` measured

`003DA890` (16 B) is the copy-plus-scalar store
`00265FF0`, `0026B2E0`, `0026BB60` and
`0026BEE0` call: `[rdx]` and `[rdx + 4]` are
copied into `[rcx]` and `[rcx + 4]`, then
`xmm2` lands at `[rcx + 0xC]` - the two-word
base copy plus one float that the
`0026B2E0` class-3 blend runs on the
`[+0xB8]` record halves.
Interior anchor `003DA894` (the `[rdx + 4]`
load).

`0022D7E0` (1659 B) is the per-cell walk the cell solver `002327D0` runs: `r14w` iterates `word[rcx+0x14]` cells over `r15 = [rcx+8]` with `0209A670`/`0209A2D0` context, `+0x12` seeds each step, and `00230790`, `00381D90`, `003810B0`, `0022E7D0` run per cell with `00861F14` x5 - the solver's element pass.

Interior anchor `0022D8FB` (function `0022D7E0`).

`003810B0` (923 B) is the per-cell body `0022D7E0` runs: `edx` mode-selects (`test`/`cmp 1`), `00202B70` x2, `00861F14` x5 and `00381450` step the cell's delta - the cell solver's per-element move, one of the four bodies its loop names.

Interior anchor `00381318` (function `003810B0`).

`0022E7D0` (740 B) is the per-cell body `0022D7E0` calls: `00202E10` does the delta step and `00861F14` copies under the cookie check - the cell solver's second per-element move.

Interior anchor `0022E8E8` (function `0022E7D0`).

`00381450` (477 B) is the delta helper `00380FA0` and `003810B0` call: `[r8] - [rdx]` takes the four-component difference into xmm3/xmm0/xmm2/xmm1, then `0046BFA0` + `00808C40` + `00861F14` run the magnitude/normalise pass - the heading delta's length arm.

Interior anchor `003814E2` (function `00381450`).

`0022F250` (471 B) is the nearest-scan `00232760`/`002327D0` call: stack-cookie prologue, `dword[020891E4]` bounds a loop over the `020891F0` table, each entry's `movss`/`subss` against `[rbx]`/`[rbx+4]` builds the delta vector on `[rsp+0x20]`, and `00202B70`/`00202B90`/`00808C40`/`00861F14` score it - the delta family's table search.

Interior anchor `0022F2FA` (function `0022F250`).

`0046BFA0` (294 B) is the projection coefficient `00381450`/`00381630` call: `d = rcx - r9` (three `subss`), `00861F14` consumes `|rdx|^2`, then `xmm3 = -(rdx.d) / (r8.d)` computes the ratio and `xmm0 = |rdx|^2 x xmm3` returns the scaled coefficient - the length arm's numerator/denominator pass.

Interior anchor `0046C03C` (function `0046BFA0`).

`0022EF20` (293 B) is the `02089280` block init `00232760`/`002327D0` call: `02089270`/`02089274` set 1, `020892B0`/`020892B8` clear, `00380A60` and `00202D50` prepare `02089280`/`020892C0`; two stack records take `00203170`, `rbx+0x80`/`rbx+0x84` floor-clamp at `0.05` (`008F30E4`), their `1.0/x` reciprocals land at `rsp+0x60`/`+0x88`, and `00202D70` twice commits the normalized pair into the block - the cell solver's scale install.

Interior anchor `0022EF95` (function `0022EF20`).

`00381D90` (288 B) is the three-kind transformer `0022D7E0`/`0022DE60`/`00232160` call: `00202B70` reads `rcx+0x50` into `rsp+0x20`, then `dword[rdi]` dispatches - kind 0 normalises the vector (`x^2+y^2+z^2` into `00861F14`, `[rbx+0xC] = 1.0f`), kinds 1/2 run `00380EB0`/`00380E00` on `rbx`; all paths then `00202B70(rbx, rdi+0x10)` and `00380800(rbx, rbx)` - the per-cell value's class-conditioned write the solver loops.

Interior anchor `00381E37` (function `00381D90`).

`00380A60` (12 B) is the constant-preload trampoline `0022EF20` and the cell solver `002327D0` enter through: `r8` takes `00D22740` (the packed `3F800000_00000000` - a `1.0f / 0.0f` float pair) and the body tail-jumps `00380A70` - the shared entry that feeds the solver its unit scale without duplicating the constant.

Interior anchor `00380A67` (function `00380A60`).

`00380A60` (12 B) is the constant-preload trampoline `0022EF20` and the cell solver `002327D0` enter through: `r8` takes `00D22740` (the packed `3F800000_00000000` - a `1.0f / 0.0f` float pair) and the body tail-jumps `00380A70` - the shared entry that feeds the solver its unit scale without duplicating the constant.

Interior anchor `00380A67` (function `00380A60`).

`00380A70` (265 B) is the delta-record builder `00380A60` forwards to: `rdx` gets `-[rcx+0x10]` (sign-flipped) at `+0` and `[rcx+0x18]` at `+8` with `+4`/`+0xC` zeroed, `r8`'s 16 bytes copy to `+0x10` with `+0x1C` zeroed, `00202E10` runs on `+0x20`/`+0x10`, the `+0x20` vec3 is normalized by `00861F14` sqrt of its squared length (`+0x2C` zeroed), a second `00202E10` runs on `+0x10`, and `rsi`'s 16 bytes land at `+0x30` - the 0x40-byte frame the heading pipeline hands downstream.

Interior anchor `00380ACE` (function `00380A70`).

`00380EB0` (227 B) is the heading-record builder `00381D90` runs: it writes `{0, elev', x', 1.0, z'}` to `rcx` from `rdx`'s `(x, elev, z)` triple - `elev` is single-wrapped into the `+/-0x3F7FBE77` band (~0.999 rad), and when the planar magnitude `sqrt(x*x + z*z)` exceeds that bound the residual is kept and the `(x, z)` direction is renormalised to unit length into `+0`/`+8`

Interior anchor `00380F29` (function `00380EB0`).

`00380E00` (171 B) is the per-component heading wrap `00381D90` applies to the delta vector: `+0`/`+4`/`+8` zero with `+0xC` = `1.0f`, then each `rdx` component is folded into range - `> 0.999390` (the `3F7FBE77` lane at `00D112A0`) subtracts it, `< -0.999390` (`BF7FBE77`) adds it - three scalar single-wrap corrections into `rcx`

Interior anchor `00380E23` (function `00380E00`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-heading-speed-to-position-delta-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0022DE60` | 1240 B | with c = `rcx`, m = qword `+8` of c, p = qword `+0x20` of c and N(x) = `00861F14` of x's squared length, for i below signed word `+0x14` of c, id = word [signed word `+0x12` + i] of qword `+0x28` of m; signed ids from `0x5000` are skipped; a gate on dword x skips when bit 31 is set after the mask/value pair at `0209A2D0` + `0x110` + 8k (k = 32 + bits 13-17 of x) is merged into x; an id from `0x4000` takes the `0x90`-byte element e = id - `0x4000` of qword `+0x18` of m, gates its dword `+4`, fills v by `00381D90(e, &v, p)`, skips unless L = N(v through the 3x3 at qword `+0x18` of c) exceeds r = `003810B0(e, p)`, and scales v by d = L - r; a lower signed id takes the 32-byte element e of qword `+0x10` of m, gates its dword `+0xC` only when its low 3 bits are 1, sets v to its four floats and L likewise, and needs s = (p minus 16-byte vertex [signed word e`+0x10`] of qword `+8` of m) dot v in (-0.001, L), the call at `0022DE60` + 0x35E (m, id, p, &w) non-zero and q = N(w) below L, taking v = w, s = q when q exceeds s; v is scaled by d = L - s over N(v); a d above float `+0x30` of c is stored there with id at word `+0x34`, and v is added to the three floats at qword `+0x28` of c | `0022DF05`, `0022DF59`, `0022E006`, `0022E1BE`, `0022E21A` |
| `00232760` | 104 B | calls the callee at `00232760` + 0x10 with `rcx` and `rdx` unchanged and then `0022EF20(rdx)`; stores 0 in dword `020891E0` and, when the signed word `+0x52` of `rdx` is not negative, stores it in dword `02088FE0` and 1 in `020891E0`; stores 0 in dword `020891E4`, calls `0022F9B0(rcx, rdx, rdx)` and tail-jumps to `0022F250(rdx)` | `00232778`, `00232790`, `00232792`, `002327B1`, `002327C3` |
| `00380FA0` | 263 B | builds A = `00202B70(&A, rdx+0x50, r8)` and B = `00202B70(&B, rdx+0x50, r9)` and on dword `+0` of `rdx` calls the callee at `00380FA0` + 0x95 for 0, `00381630` for 1 or `00381450` for 2, each as (&C, &A, &B); for any other kind or a zero result it returns -1.0 (`01CEBC9C`); otherwise it writes `00202B70(rcx, rdx+0x10, &C)` and returns `00861F14` of the squared distance between the first three floats at `rcx` and at `r8` | `00380FE0`, `00380FE5`, `0038103C`, `0038104A`, `00381087` |
