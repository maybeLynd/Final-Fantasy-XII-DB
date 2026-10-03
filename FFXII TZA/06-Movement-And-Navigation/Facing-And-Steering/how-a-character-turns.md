---
system: Facing and steering — how a character's heading is set
category: 06-Movement-And-Navigation
status: AUDITED
owner_layer: PrimaryOwner:Movement
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: three function bodies disassembled from the shipping EXE; every float constant read from
    its RIP target with a tool; names taken as leads from Collaboration research prose and then
    re-derived from the binary
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-how-a-character-turns-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# Facing and steering — how a character's heading is set

> **Imported from the research backlog, then re-derived.** These three functions were named in this
> project's multiplayer research and had **never entered the database**. The names were used as leads
> only; every claim below comes from the disassembled body. See
> [`../../_index/RESEARCH-IMPORT-BACKLOG.md`](../../_index/RESEARCH-IMPORT-BACKLOG.md).

## 1. What the player sees

When a character turns to face something — a party member spinning to answer an enemy that stepped
behind them, an NPC pivoting as you walk past — the game does not simply store the direction you
asked for. **It first folds the angle back into a single turn.**

That matters because angles accumulate. A character told to face "one and a half turns clockwise"
would, without folding, be storing a value that keeps growing, and everything downstream that
compares two headings would eventually disagree about which way is shorter. The engine normalises
every heading the moment it is set, so **the stored facing is always within half a turn of straight
ahead** and the shortest-rotation comparison is always correct.

Separately, a character has a **steering mode** — how it decides where to put its feet. Setting the
mode to *off* does more than stop the steering: it clears a flag and resets a counter, which is why a
character whose steering is switched off does not resume mid-turn when it is switched back on.

## 2. Native mechanism

### The heading wrap — two variants that differ by one flag

`Actor_SetFacingHeading_Variant0` (`0026B5A0`, 117 B) and `Actor_SetFacingHeading_Variant1`
(`0026B620`, 120 B) are **the same function with one immediate changed**:

```asm
0026B5CF  xor  r8d, r8d          ; Variant0 -> mode 0
0026B64F  mov  r8d, 1            ; Variant1 -> mode 1
```

Everything else is instruction-for-instruction identical. The body:

```c
void Actor_SetFacingHeading(Actor *a /*rcx*/, float heading /*xmm1*/)
{
    float pi = (heading >= 0.0f) ?  3.14159274f    /* 01CEBC50 */
                                 : -3.14159274f;   /* 00915620 */
    float t = heading + pi;
    int   n = (int)(t / 6.28318548f);              /* 01CEBC78, truncates toward zero */
    t = t - (float)n * 6.28318548f;
    t = t - pi;

    FUN_0026B6A0(a, t, mode);      /* mode = 0 or 1, the only difference */
    return FUN_0026C090(a, t);     /* tail call */
}
```

**Written out with the real constants**, this is a fold into a single turn:

```
wrapped = ((heading ± π) − 2π·trunc((heading ± π) / 2π)) ∓ π
          π  = 3.14159274f   (float32 nearest π)
          2π = 6.28318548f
          +π when heading ≥ 0, −π when heading < 0
```

> **The sign-dependent π is what makes the result land in ~~(−π, +π]~~ [−π, +π] rather than [0, 2π).** *(corrected 2026-10-02, OPUS: `0026A8E6` `comiss` / `jb` takes the bias `[00915620]` (`-π`) for a negative angle, else `[01CEBC50]` (`+π`); [−π, +π) for a non-negative input and (−π, +π] for a negative one, so `+π` lands on `−π` and `−π` on `+π`)* Adding π
> before the modulo and subtracting it after re-centres the interval on zero; choosing the sign of π
> from the sign of the input keeps the truncating division — which rounds toward zero, not down —
> from putting negative inputs in the wrong bucket. **A reimplementation that uses `fmod` and a fixed
> `+π` will disagree with the game for negative headings.**

**Both π constants are distinct addresses:** `+π` at `01CEBC50` and `−π` at `00915620`, in different
sections. They are not one constant negated at run time.

### Steering mode — `Movement_SetSteeringMode` (`0026AE90`, 127 B)

```c
void Movement_SetSteeringMode(Actor *a /*rcx*/, int mode /*edx*/)
{
    if ((a->b03 & 0xE0) != 0x60) return;              /* actor-kind gate */

    Ctx *c = a->p_B8;
    if ((unsigned)(mode - 2) <= 2) {                  /* mode ∈ {2, 3, 4} */
        if (c->p_F0->f_2C == 0.0f)                    /* the scalar is exactly zero */
            mode = 1;                                 /* downgrade */
    }
    c->p_F0->b_29 = (unsigned char)mode;              /* the mode is stored here */

    if (mode == 0) {
        a->b0D &= ~0x10;                              /* clear bit 4 */
        FUN_002E55C0(a, c);
        if ((a->b03 & 0xE0) == 0x60)                  /* gate RE-CHECKED after the call */
            a->p_B8->p_F0->d_7C = 0;                  /* reset the counter */
    }
}
```

**Three things in that body are worth naming:**

**The actor-kind gate is `(byte@+0x03 & 0xE0) == 0x60`** — the top three bits of a byte at `+0x03`
must be exactly `011`. Anything else returns immediately, having done nothing. **Setting a steering
mode on the wrong kind of actor is silently ignored**, not an error. **`011` is class 3, the
steerable actor class** (`ED-6`, `K-2`, reconciled 2026-09-12 with `BV-4`): the record carver
stamps `+0x03 = (class << 5) | sequence` and the shipped scripts declare every actor with its
sequence, so class 3 (sequences 5–7: `PC`, `VAN`, `summon`, `treasure_`, `WARP_PC`, `NPC`,
`hitactor`, `monster_`, `unique_monster_`, `trial_`) is the only class with a full movement context
and a steering record. Movement excludes **class 0** (script-only controllers, no `+0xB8` at all),
**class 1** (placed objects — a `0x80`-byte block whose `+0x38` is a heading, so the position and
heading accessors admit it but no setter does) and **class 2** (trigger lines). See
[how the engine chooses 3-D or flat movement](../Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)
(`BV-4`).

**Modes 2, 3 and 4 are conditionally downgraded to 1.** `lea eax,[rdx-2]; cmp eax,2; ja` is the
compiler's unsigned range test for `2 ≤ mode ≤ 4`. If the float at `p_F0 + 0x2C` is **exactly zero**
— tested with `ucomiss` plus a `jp` NaN guard — the requested mode becomes `1` before it is stored.
So **a mode the caller asked for is not necessarily the mode that ends up stored**, and a
reimplementation that skips this check will diverge only when that scalar happens to be zero.

**The kind gate is re-checked after `FUN_002E55C0` — and that is an inlined helper's own gate, not
a hint that the call can change the actor** (`ED-5`, read 2026-09-12). `002E55C0`
(`Movement_ClearSteeringRequest`, 73 B) does four things and nothing else: `rec->+0x29 = 0`; if the
movement mode `(rec->+0x28 & 0x7F) == 2`, `0026C120(actor, 0)`; `rec->+0x24 = 0`; `ctx->+0xD0 = 0`.
Nothing on its call tree writes `actor+0x03` (the 80-reader census has **no** writer of that byte
outside the carver, which stamps it before the record is live) or `actor+0xB8` (two writers in the
image, the region-map bind `00266AD0` — called only by the initialiser `00266530` and the teardown
`002693D0` — and `00262F90`, called only by `00262F50`; `0026C120`'s mode-0 callees `002EBE50`,
`002E8EE0` and `002E6300` reach neither). The tail that follows the re-check, `rec->+0x7C = 0`, is
**exactly `0026A640(actor, 0.0f)` inlined** — the setter of the steer-speed request, whose body
opens with the same `(+0x03 & 0xE0) == 0x60` test and re-loads `+0xB8` itself. The compiler kept the
helper's gate. **Hoisting the check is faithful.**


### The steering mode, read at its consumer — 2026-09-12 (FABLE)

`+0x29` is **the speed-ramp shape of a scripted move**, and it is only ever non-zero because a
move verb asked for it. Read from every writer and the one consumer:

**Who writes it.** `Movement_SetSteeringMode` is the sole writer (`0026AED4`; the raw `E8`/`E9`
index finds fourteen call sites, no others). Twelve of them pass **0** — `movecancel` (`0x0080`,
`0034D8F0`), `ucmovecancel` / `ucmovecancel_52d` (`0x04DD` / `0x052D`, the party leader / an actor
by id), the teleports `setpos` / `setpos_19` / `setpos2` / `setpos2_20d` / `setmapjumppos`
(`0x0001` / `0x0019` / `0x020C` / `0x020D` / `0x008F`), `setposparty` / `setposparty_mapjump`
(`0x03B1` / `0x056D` → `0037D000`, all four party slots), the steering push `002EAB80`, and the
actor teardown `002693D0` (twice). **Only two bodies pass anything else:**
`VM_ActorSteerToPosition` (`00357A20`) and `VM_ActorSteerTowardActor` (`00357980`), and every
`begin` handler of the move family ends in one of them — `move` / `rmove` / `cmove` / `rcmove` /
`amove` / `ramove` / `ucmove` in their 3- and 4-operand forms (`0x003E`–`0x0045`, `0x0059`–`0x0060`,
`0x009A`, `0x04CE`–`0x04D5`, `0x052B`, `0x3092`; the `-a` forms steer toward an actor). Both bodies
pop the speed, store it (`Movement_SetRequestedSpeedScaled` → `+0x24`, and `0026A640` → `+0x7C`),
set the target and snapshot the start position (`0026AF10`: context `+0x00..+0x0F` → context
`+0x30`), then choose the mode at `003579DE`–`003579FC` / `00357AA9`–`00357AC7`:

```
mode = (record->+0x2C == 0.0f) ? 1 : record->+0x2B
```

`+0x2B` and `+0x2C` are written together by **`setaccr`** (`0x0122`, one operand: `00352D10`
pushes **4** as the mode before popping) and `setaccr_123` (`0x0123`, `(accel, mode)`) through
`00269C30`: `+0x2C = accel × [01DFE0BC]` (the `FrameLimit` inverse scale), `+0x2B = mode`. **Shipped
scripts call `setaccr` twice in the whole corpus** (`4e-05` and `0.006`, both one-operand, so mode
4) against 5 `setvelr`, 546 `setreachr`, 1,271 `movecancel` and 41 `ucmovecancel`; **almost every
scripted move therefore runs in mode 1.** The setter's own downgrade (modes 2–4 → 1 when `+0x2C` is
exactly `0.0`) is the same rule applied a second time, and it exists because the consumer **divides
by `+0x2C`**.

**The one consumer.** `Movement_UpdateActorFrame` (`002E5030`) calls
`Movement_UpdateSteeringTowardTarget` (`002E45E0`, 963 B) only when `+0x29 − 1 ≤ 3` unsigned
(`002E50A7`–`002E50B8`), i.e. for modes 1–4; mode 0 is *off*. Per frame, with `rec` the steering
record and `ctx` the movement context:

1. **The target point** (`002E462C`–`002E46CD`). `rec->+0x2A` is the target kind, written by the
   two target setters: **0** = the position at `rec->+0x00..+0x08` (`Movement_SetSteeringTargetPosition`
   `0026AE30` stores `(x, y, z, 1.0)`), reach = `rec->+0x20` (`setreachr` `0x0076` → `0026B450`);
   **1** = an actor (`Movement_SetSteeringTargetActorRef` `0026ADF0`: `+0x00` the ordinal, `+0x04`
   the manager index, resolved by `003587C0`; a **negative** `+0x04` means the party focus actor,
   `PartyFocus_GetCurrentPackedActorHandle` → `ActorHandle_ResolveRegistryEntryByPackedId`), whose
   position is read live and whose reach is `rec->+0x20` **plus a radius term from both bodies**
   (`003DA6A0`: `sqrt(003DA730(a)) + a->+0x5C + sqrt(003DA730(b)) + b->+0x5C` over the two `+0x50`
   sub-blocks). An unresolvable actor target steers toward the origin with reach `+0x20`.
2. **The bearing** (`003A19C0`): yaw `atan2(dx, dz)` and pitch `atan2(dy, √(dx²+dz²))` from the
   actor to the target, both wrapped; `ctx->+0xA4` (desired heading) and `ctx->+0xA0` (desired
   pitch, the `K-1` pitch) each **approach** them by at most `rec->+0x50` / `rec->+0x54` per frame
   (`003A1AD0`: wrap the difference into (−π, π], step by `min(|diff|, max)`, re-wrap).
3. **Optional snap** (`002E4727`–`002E4751`): when the manager flag `02099011[actor->+0x15 × 0x288]`
   is set, `0026AFE0(actor, target, 0)` places the actor on the target every frame.
4. **Remaining distance** = `distance(ctx, target) − reach`, three-dimensional (`003A1920`) when the
   controller's fly / float bits (`00264460`: `+0x151` bits 0 | 1, `BV-1`) or actor `+0x08` bit 2 is
   set, otherwise flat XZ (`Vector3_ComputeXZDistance`).
5. **The ramp** (`002E47A7`–`002E4895`), with `v = rec->+0x24` and `a = rec->+0x2C`:

   | mode | shape |
   |---:|---|
   | 1 | `v` unchanged — constant speed |
   | 2 | **accelerate from the start**: `d0 = distance(ctx, ctx->+0x30)`; if `max(a, d0) < v²/2a` then `v = max(a, √(2a·max(a, d0)))` |
   | 3 | **decelerate into the target**: if `max(a, remaining) < v²/2a` then `v = max(a, √(2a·max(a, remaining)))` |
   | 4 | both, accelerate then decelerate (`002E485B` skips the second block only for mode 2) |

   `v` is written to `ctx->+0xD0` and `ctx->+0xF8` (`002E48B5`, `002E48C0`).
6. **The near flag**: actor `+0x0D` bit 4 is set when `[02164200] × rec->+0x24 > remaining`
   (`002E4899`–`002E48D0`). `02164200` is zero in the image and **3.0** at run time (`00266D10`
   stores it at boot through `002EBE40`, `00266D83`–`00266D8B`; the debug verb
   `debug_charmovestopvelrratio` `0x208E` rewrites it) — "within three frames' travel". This is the
   bit mode 0 clears at `0026AEDB`.
7. **Arrival**: when `[01DFE0B8] × v > remaining` (`01DFE0B8` is the `FrameLimit` scale, 1.0 or 2.0)
   the move ends (`002E48F9`–`002E4978`): a position target with zero reach is snapped onto exactly
   (`0026AFE0`), `+0x24`, `ctx->+0xD0` and `+0x2C` are zeroed, then `+0x29 = 0`, a movement mode 2
   (`+0x28 & 0x7F`) is torn down through `0026C120(actor, 0)`, and `+0x24` / `ctx->+0xD0` are zeroed
   again — the same four writes `Movement_ClearSteeringRequest` (`002E55C0`) performs for mode 0.

   The rest of `002E5030`'s frame — heading publish `002E5C10`, the spatial-grid update
   `003DB020`/`0046AD20`, and the ~~`02AC7CC8`~~ `02B57CC8` *(corrected 2026-10-02, OPUS: `02AC7CC8` has no reference; `02B57CC8` is the list head `003DB0D0` appends to)* deferred-register tail `002E6330`/`003DB0D0` —
   is bound member by member on the
   [heading-speed-to-position-delta](../heading-speed-to-position-delta.md) page's `002E5030`
   subtree section.

**Why the speed survives a frame.** While `+0x29 ≠ 0`,
`WorldActor_UpdateRuntimeAndScriptExecutionState` re-issues
`Movement_SetRequestedSpeed(actor, rec->+0x7C × [01DFE0BC], …)` every frame (`0025DF43`–`0025DF83`);
`+0x7C` is **the speed operand the move verb popped**, kept for that re-arm — which is why mode 0
zeroes it. `setvelr` (`0x0002`) writes the same pair.

So the five values are: **0 off · 1 constant speed · 2 accelerate from the start snapshot ·
3 decelerate into the target · 4 both.** `ED-4`. The ramps are the classical `v = √(2·a·d)` with
`a` floored in, so a stopping distance never goes negative; a reimplementation needs the
**`max(a, ·)` floors and the arrival scale** or it will overshoot at 60 fps.

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `0026B5A0` | 117 B | `Actor_SetFacingHeading_Variant0` — wrap, then `FUN_0026B6A0(a, t, 0)` |
| `0026B620` | 120 B | `Actor_SetFacingHeading_Variant1` — identical but `mode = 1` |
| `0026AE90` | 127 B | `Movement_SetSteeringMode` |
| `0026B6A0` | 120 B | the shared consumer of the wrapped angle — ~~**not read**~~ *(answered: see ED-2 in §5 and the facing contract's §2 — kind 1 writes context `+0x38` / `+0x48`, kind 3 forwards the flag to `002E5FB0`; 2026-10-02, OPUS)* |
| `0026C090` | 129 B | the tail target of both variants — ~~**not read**~~ *(answered: see ED-3 in §5 — it wraps again and dispatches on the kind; 2026-10-02, OPUS)* |
| `002E55C0` | 73 B | `Movement_ClearSteeringRequest` — called on the mode-0 path — ~~**not read**~~ *(answered: see ED-5 in §2 — it clears `+0x29`, `+0x24` and `ctx+0xD0` and ends mode 2; 2026-10-02, OPUS)* (name and size filled in 2026-09-13) |

### Data addresses

| address | value |
|---|---|
| `01CEBC50` | `3.14159274f` (+π) |
| `00915620` | `-3.14159274f` (−π) |
| `01CEBC78` | `6.28318548f` (2π) |

### Field offsets used

| offset | on | meaning |
|---|---|---|
| `+0x03` | actor | byte; top three bits gate the whole steering call (`& 0xE0 == 0x60`) |
| `+0x0D` | actor | byte; bit 4 cleared when steering is set to mode 0 |
| `+0xB8` | actor | pointer to the movement context |
| `+0xF0` | context | **cursor** into an inline array of two records — see below |
| `+0x29` | steering record | byte; **the stored steering mode** |
| `+0x2C` | steering record | float; zero forces modes 2–4 down to 1 |
| `+0x7C` | steering record | dword; zeroed when steering is switched off |

> ### 2026-09-08 — `+0xF0` is not an owning pointer, and `+0x29` is not the only mode byte
>
> **The record is `0x80` bytes and there are two of them, inline in the context** at `+0x120`
> and `+0x1A0`; `+0xF0` is a cursor selected by the byte at context `+0xDC`
> (`shl rax,7` at `00269F9F`). Nothing allocates or frees a steering record.
>
> **And `+0x29` is one of two adjacent mode bytes.** `0026C120` writes `+0x28` and calls it
> the mode too; both setters reach the same record by the same chain, so these are **two
> fields, not one described twice.** Neither this document nor
> [setting the movement mode](../Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md)
> was wrong; between them they had named two different bytes the same thing.
>
> The full 32-field census, the push/pop pair that flips the slots, and the type store entry
> are in [the two steering slots](the-two-steering-slots-and-what-a-character-resumes.md).

## 4. Modding notes

- **Do not write a heading directly into whatever `0026C090` stores.** The wrap is the contract; an
  unwrapped value will compare wrongly against every other heading in the game.
- ~~**The two variants differ only in the flag passed to `0026B6A0`.** Whatever that flag
  selects, it is the only behavioural difference — hooking one and not the other will produce
  an asymmetry.~~ **CORRECTED 2026-09-18.** The 2026-09-08 withdrawal was itself too broad:
  `0026B6A0` never touches `r8` in its own 120 bytes, but its **kind-3 arm tail-jumps with the
  flag still live** — `002E5FB0` (`r9d = r8d`) → `002E5E10` → `003EC260`, where it gates the
  steering-slot commit. Variant0 **stages** the ~~`{rate, heading, 0}`~~ `{pitch, heading, 0}` triple *(corrected 2026-10-02, OPUS: lane 0 is context `+0xAC`, `002E5FBA` → `002E5F4F` → `003EC348`)*; Variant1
  **stages and commits** (`004288B0`/`003B3CA0`). The asymmetry is real **on kind-3 actors
  only** — hooking one variant changes steering commit behaviour there; on every other kind
  the flag dies and the variants coincide. `ED-2` corrected; see
  [the contract](../CONTRACT-facing-and-steering.md) §2.
- **A steering mode you set may not be the mode that sticks.** Modes 2–4 collapse to 1 when the
  record's `+0x2C` float is exactly zero — and `+0x2C` is the ramp acceleration the consumer divides
  by, so the collapse is a divide-by-zero guard: `setaccr` first, then move.
- **To make a scripted walk ease in or out, call `setaccr(a)` (mode 4) or `setaccr(a, 2|3)` before
  the move verb.** The shipped scripts do it twice. Arrival is tested against `[01DFE0B8] × v`, so
  a 60 fps player's walks end one frame earlier in distance terms than a 30 fps player's.
- **Steering calls on an actor whose `+0x03` kind bits are not `0x60` do nothing at all** — no error,
  no partial effect.

## 5. What is not known

- [x] ~~**What `FUN_0026B6A0`'s third argument selects** — the only difference between the two facing
  variants, and therefore the reason both exist. `ED-2`.~~ **CORRECTED 2026-09-18 — it selects the commit gate on kind 3:**
  `0026B6A0` never reads `r8` itself, but its kind-3 arm forwards it live to `002E5E10`→`003EC260`; flag 0 stages, flag 1 stages+commits. Identical only on kind ≠ 3 ([the facing-and-steering contract](../CONTRACT-facing-and-steering.md) §2). *(Ticked 2026-09-14, FABLE: the register's `ED-2` verdict answers this box; the page box had been left open.)*
- [x] ~~**What `FUN_0026C090` does with the wrapped angle** — the tail call, i.e. where the facing
  actually lands. `ED-3`.~~ **ANSWERED 2026-09-08:** it wraps again and dispatches on the actor kind (kind 3 writes the
  record's target heading, kind 1 calls `0026B6A0(a, t, 1)`, other kinds do nothing; the contract §6). *(Ticked 2026-09-14, FABLE: the register's `ED-3` verdict answers this box; the page box had been left open.)*
- [x] ~~**What the steering-mode values 0–4 mean.**~~ **`ED-4` ANSWERED 2026-09-12 (FABLE)** — from
  the consumer `002E45E0`: 0 off, 1 constant speed, 2 accelerate from the start snapshot, 3
  decelerate into the target, 4 both; chosen by the move verbs from `setaccr`'s `+0x2B` unless the
  ramp acceleration `+0x2C` is zero. §2, "The steering mode, read at its consumer".
- [x] ~~**Whether `FUN_002E55C0` can change the actor's kind bits.**~~ **`ED-5` ANSWERED 2026-09-12
  (FABLE)** — it cannot: it writes three record fields and one context field, its call tree reaches
  no writer **of the two fields `+0x03` and `+0xB8`** — an absence claim about those FIELDS, not
  about `0026A640`, which §2 shows is *called* here, inlined — and the re-check is that
  function's own gate, hoisted. §2.
- [x] ~~What the actor-kind encoding `(b03 & 0xE0) == 0x60` denotes.~~ **`ED-6` ANSWERED 2026-09-12
  (FABLE)** — class 3, the steerable actor class of `BV-4`. §2.
- [x] ~~**UQ-101.** **Who sets movement mode 5**, whose arm in the facing integrator `002E5750` waits on an
  animation-state test (`002EA780`); none of the 29 call sites of `0026C120` passes a constant 5.~~
  **Answered 2026-09-14 (FABLE):** the untimed turn body `002690D0` (the turn verbs `raturn_25e`, `raturna`, `raturnya`, `003578B0`, `unkCall_3092`) **stores 5 into the steering record's `+0x28` itself** (`002692E8`, `mov byte ptr [rcx + 0x28], 5`), without calling `0026C120`. It takes that branch when all three hold:
  - the absolute wrapped delta from the heading to the target is below `1.0472` (π/3, 60°; `0026928F`–`0026929F`);
  - record byte `+0x65` is 0 (`002692A8`);
  - `002E7600(actor)` is non-zero (`002692B0`). That predicate requires the actor's render record (`022C6F28` + index × `0x740`) to have `+0x284` set, which is the same field mode 5's wait arm tests, and then tail-jumps to a second predicate (`002E763A`).
  On that branch it first calls `002EC380(actor, 2, n)`, which puts 2 in bits 3–5 of record `+0x62` and a frame count (`n` over the frame-rate scale, `n` ≥ 1) at `+0x60` (`002692BF`–`002692C7`). The other branch calls it with 1 and takes the frame-counted steering path. **So a small untimed turn on an actor with a ready render record is handed to the animation layer, and mode 5 waits for it**, where a larger one is integrated. The 29-site census stays exact, because this store never reaches the setter. It was found by scanning every byte write to `+0x28` through a register loaded from `[x + 0xF0]`: five writes in all, only this one with the constant 5.
  See [setting the movement mode](../Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md) §10.
  The integrator's 13-member exclusive subtree — its mode dispatch plus the twelve kind-3
  accessors over the steering record — is bound member-by-member on
  [the two steering slots](the-two-steering-slots-and-what-a-character-resumes.md) §5
  (SWE2-FRONTIER, followup queue).

## 6. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The two variants differ only in `r8d` | both bodies disassembled and compared instruction for instruction | 1 | PROVEN |
| The wrap formula and its constants | every float read from its RIP target with a tool, not by hand | 1 | PROVEN |
| `+π` and `−π` are distinct addresses in different sections | `01CEBC50` and `00915620`, both resolved | 1 | PROVEN |
| The actor-kind gate `(b03 & 0xE0) == 0x60` | `movzx`/`and 0xE0`/`cmp 0x60` at `0026AE96` and again at `0026AEEA` | 1 | PROVEN |
| Modes 2–4 downgrade to 1 on a zero scalar | `lea eax,[rdx-2]; cmp eax,2; ja` plus `ucomiss`/`jp`/`jne` | 1 | PROVEN |
| The gate is re-checked after `002E55C0` | the second test at `0026AEEA`, with `+0xB8` re-loaded | 1 | PROVEN |
| Steering modes 1–4 are constant / accelerate / decelerate / both, 0 is off | `002E45E0` read in full: the gate `002E50A7`–`002E50B0`, the switch `002E47BD`–`002E47CE`, the two ramp blocks and the `+0x29 == 2` skip at `002E485B` | 1 | PROVEN |
| Non-zero steering modes come only from the two steer bodies, from `+0x2B` unless `+0x2C == 0` | raw `E8`/`E9` index of `.text`: 14 call sites of `0026AE90`, 12 pass 0; `003579DE`–`003579FC`, `00357AA9`–`00357AC7` | 1 | PROVEN |
| `setaccr` writes `+0x2B` / `+0x2C`; two shipped uses | `00352D10` (pushes 4), `003528F0`, `00269C30`; corpus census of 1,114 decompiled scripts | 1 / 2 | PROVEN |
| `002E55C0` changes neither `+0x03` nor `+0xB8`; the re-check is `0026A640`'s gate inlined | `002E55C0` read in full; writer censuses of `+0x03` (0) and `+0xB8` (2, neither reachable); `0026A640` body | 1 | HIGH — the writer census follows actor-rooted chains only |
| Class 3 is the steerable class | `BV-4` corpus census plus the carver's stamp `00267AE1`–`00267B13` | 1 / 2 | PROVEN |
| What `0026B6A0` / `0026C090` do | ~~**not read**~~ *(answered: see ED-2 and ED-3 in §5; 2026-10-02, OPUS)* | — | ~~UNKNOWN~~ PROVEN |

## 7. Related

- [`../../_index/RESEARCH-IMPORT-BACKLOG.md`](../../_index/RESEARCH-IMPORT-BACKLOG.md) — where these
  three came from, and the 61 still to import.
- [`../heading-speed-to-position-delta.md`](../heading-speed-to-position-delta.md) — what a heading
  becomes once it is set.

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| five stated sizes | **5 of 5 exact** |
| `+π` at `01CEBC50`, `−π` at `00915620`, `2π` at `01CEBC78` | **3.1415927410125732**, its negation, and **6.2831854820251465**, at exactly those addresses and in different sections |
| the two variants are the same function with one immediate changed | **29 instructions each**, and **three** textual differences — see below |

### "Identical but one immediate" is exactly right, and the diff says how exactly

Disassembled and compared instruction by instruction, the two bodies differ in **three positions**:

| position | Variant0 | Variant1 |
|---:|---|---|
| 7 | `jb 0x26b5c3` | `jb 0x26b643` |
| 9 | `jmp 0026B5CB` | `jmp 0026B64B` |
| **12** | **`xor r8d, r8d`** | **`mov r8d, 1`** |

The first two are **the same jump at a different address** — an artefact of the two copies living
`0x80` apart, not a difference in the code. **Exactly one position differs semantically**, and the
byte counts agree with it independently: `mov r8d, 1` is six bytes and `xor r8d, r8d` is three, so
the bodies must differ by **3** — and 120 − 117 = 3.

### The reimplementation warning is true, and the error is a whole turn

§ warns: *"a reimplementation that uses `fmod` and a fixed `+π` will disagree with the game for
negative headings."* That is a claim about behaviour, so it was tested as behaviour — both formulas
in float32, over 4,016 headings (16 chosen, 4,000 uniform in ±20):

| | |
|---|---|
| disagreements | **1,744** |
| of which at **negative** headings | **1,744** |
| at non-negative headings | **0** |

**The split is total.** And the disagreement is not a rounding difference: every one is **2π**
exactly — `h = −19.9929` gives the game `−1.14330` and the naive version `−7.42648`, and
`7.42648 − 1.14330 = 6.28318`. A reimplementation making this mistake does not produce a slightly
wrong facing; it produces one a **full turn** out, and for negative headings it does not even return
a wrapped angle, because C's `fmod` keeps the sign of the dividend.

Over the same sample the game's own formula stays inside **[−π, +π]** — measured range `−3.137042` to
`3.140685` — which is what § claims for it.

> This is the rare documentation claim that is *about the reader's future mistake*, and those are
> worth testing as behaviour rather than reading as prose. It cost one simulation and it is now a
> measured fact rather than an inference from the shape of the code.

**Not claimed:** nothing here was executed against the game, and no live observation is involved —
the simulation is arithmetic over the same float32 constants, not the engine running. `0026B6A0`,
`0026C090` and `002E55C0` remain unread, as § says *(answered: see ED-2, ED-3 and ED-5 — all three read; 2026-10-02, OPUS)*; the steering-mode gate and §'s 2026-09-12
consumer reading were not re-derived.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **CoreRuntimeScheduling — CLIENT and MECHANICAL.**
  - The area initialiser `00266D10` is called by the boot-time subsystem initialiser (the one that seeds the gameplay MT).
  - `ActorStorage_InitializeRecord` (`00266530`) resolves its tables through `ImageAddress_ResolveRuntimePointer`.
- **Presentation — SERVICE.**
  - `00266D10` initialises the camera records through `CameraSystem_InitializeRecords`, and a 271-byte Presentation
    body.
  - `003587C0` is called by a 714-byte render-cluster body that also reads the 32-byte manager accessor.
- **Audio — SERVICE.** `00266D10` calls a 516-byte Audio-filed body that reaches the sound entries.
- **CombatAction — CLIENT.**
  - `Battle_ProcessActionTarget` turns units through `Actor_SetFacingHeading_Variant1`.
  - `BattleUnit_TryTriggerNearbyAuthoredFieldAction` uses the distance `003A1920`, which returns a real distance
    ([walking into an authored trigger point](../../03-World-Area-Field/walking-into-an-authored-trigger-point.md),
    crossings).
- **CombatFormula — CLIENT.** A 681-byte CombatFormula-filed body calls the same distance after resolving stats owners
  and `Actor_GetWorldPosition`.
- **Input - CLIENT and SERVICE (2 edges).** `00263750` is also called by bodies filed to input: `00226BE0` (ActorControlMaskPropagationRuntime); `00266D10` reaches bodies filed to input: `00226BE0` (ActorControlMaskPropagationRuntime) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (19 edges).** `00263750` is also called by bodies filed to party: `003261D0`, `00326500`, `003272F0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (145 edges).** `00262F50` is also called by bodies filed to script VM / native bridge: `003410C0`, `0034C3D0`, `0034C950` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `002EBE40` is also called by bodies filed to World: `00266D10` (NativeSupport) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (13 edges).** `00266D10` reaches bodies filed to WorldAreaField (world area): `002342F0`, `00268750`, `0026D910` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — SERVICE.** `00266D10` on this page calls `FUN_002ef2d0`, owned by that layer. What it reaches is a 38-byte clear that gives the block a size: **`0x1538` bytes at the persistent payload base**, `002EF640()` plus `0x200`, before it tail-jumps; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).


## Interior citation — frontier hub `002EBE50` (2026-09-18, SWE2-EC7)

`002EBE50` — 327 B, 21 callers (5 A-measured); the tracking-delta publish sibling of
`Movement_SetRequestedSpeed` (`0026D6F0`, measured on the facing contract). Interior verified:
same `byte[rcx+3] & 0xE0 == 0x60` tag gate (`002EBE5A`–`002EBE67`); `edx == 0` clears
`[+0xB4]`/`[+0x224]` on the `[+0xB8]` context (`002EBE7D`–`002EBE8B`); otherwise it measures
`[+0xF0]` sub-record fields `+0x70`/`+0x74` minus the stored values through `003A1C50`
~~(fabsf-shaped)~~ (the two-loop wrap into `[-pi, pi]`, no absolute value *(corrected 2026-10-02, OPUS: `002EBEC3`–`002EBED0` and `002EBEE5`–`002EBEF2` call `003A1C50` on the signed difference)*) at [`002EBED0`/`002EBEF2`](../../_index/ADDRESS-INDEX.md), writes the fresh
pair back (`002EBF01`/`002EBF0A`), and the `+0x62` byte's `0x38` mask chooses which follow-up
lane runs. This is the "how far did the target drift" half of the turn decision.


### Interior citation — frontier hub `0026C120` (2026-09-18, SWE2-EC7)

`0026C120` — 354 B, 27 callers: the steering-mode setter `mode==2` arm and the
+0x24/+0xD0 clears sit next to. `(byte[rec+3] & 0xE0) == 0x60` gates the whole
body. The steering sub-record is `[rec+0xF0]`; `byte[obj+0x28]` is saved and set
to `edx`. Arms: `edx` 2–3 and 4 both compute `subss([obj+0x34], [rec+0xA8])`
through `003A1C50`, set/clear `byte[obj+0x62]` bit `0x40` on the sign, and ~~arm-4~~ the mode 2–3 arm *(corrected 2026-10-02, OPUS: `0026C167` `cmp edx, 3` / `0026C16A` `jle 0026C1E6`; the stores `0026C224` / `0026C237` are in that block, while mode 4 calls `0026B620` and clears `+0x28`)*
additionally stamps `dword[obj+0x58] = 0x3E20D97C`, `dword[obj+0x5C] =
0x40490FDB` (π) at [`0026C224`](../../_index/ADDRESS-INDEX.md); `edx == 0` runs
`002EBE50` + `002E8EE0` (when `+0x65` is set) ~~; `edx <= 1` falls to `002E6300(rec, rbx, sil)`.~~ and then `002E6300(rec, rbx, sil)` (`0026C26D`); `edx == 1`, negative modes and modes above 4 go straight to the epilogue *(corrected 2026-10-02, OPUS: `0026C156` `je 0026C244` for 0 only, `0026C15E` `cmp edx, 1` / `0026C161` `jle 0026C272`, `0026C16F` `jne 0026C272`)*. The mode
table the turn verbs write through.
## SWE2-EC7-45 update (2026-09-19) - `0037D000`

`0037D000` (250 B) is a body - `00263750`/`00263F40`/`0026A0D0`/`0026AE90`/`0026B0C0`/`0026B620`/`00310920`. Interior anchor `0037D029` (a `00263750` call).

## SWE2-EC7-98 update (2026-09-20) - `002E6300` measured

`002E6300` (10 B) is the sign-gate `002693D0` and `0026C120`
call: `r8b` negative tails `00265510`, anything else returns -
the sign-bit fork the turn helpers consult before committing
to the shared path.
Interior anchor `002E6303` (the `js`).

## SWE2-EC7-104 update (2026-09-20) - `0026D6A0` + `0026AF10` + `0026A640` measured

`0026D6A0` (38 B) is the sign-select head
`00357980` and `00357A20` call before tailing
`0026D6F0`: it loads the constant at
`01DFE0BC`, scales `xmm2` by it, and sets
`r8d = 0` when `xmm2 > 0` else `2` - the
two-way branch selector fed to the shared
tail.
Interior anchor `0026D6B9` (the constant
scale).

`0026AF10` (26 B) is the class-3 snapshot
`00357980` and `00357A20` run: when
`byte[rcx + 3] & 0xE0 == 0x60` it copies the
16-byte vector at `[[rcx + 0xB8]]` into
`[+0x30]` of the same record - the staged
position copy the turn arms publish.
Interior anchor `0026AF21` (the `movaps`
load).

`0026A640` (30 B) is the class-3 scalar write
`00357980` and `00357A20` run: same
`0x60` test, then `[[[rcx + 0xB8] + 0xF0] +
0x7C] = xmm1` - a single float pushed through
two levels of indirection into the bound
record.
Interior anchor `0026A658` (the `movss`
store).

## SWE2-EC7-105 update (2026-09-20) - `00263720` + `002636F0` measured

`00263720` (35 B) and `002636F0` (34 B) are
the class-3 fetches `00357980` and
`00357A20` call through the
`[[rcx + 0xB8] + 0xF0]` indirection:
`00263720` answers `byte[rec + 0x2B]` (or 1
when the class test fails), `002636F0`
answers `float[rec + 0x2C]` (or `0.0f`) -
the paired byte/float reads on the bound
record.
Interior anchors `0026373E` and `0026370C`
(the `+0x2B` / `+0x2C` loads).

`003A19C0` (268 B) is the yaw/pitch pair `002E45E0` derives from a delta: `xmm8 = [r9] - [r8]`, `xmm6 = [r9+4] - [r8+4]`, `xmm7 = [r9+8] - [r8+8]`; `00861F14` square-roots ~~`dy^2 + dx^2`~~ `dz^2 + dx^2` *(corrected 2026-10-02, OPUS: `003A1A02`–`003A1A12` square `xmm7` and `xmm8`, the z and x lanes)* for the planar magnitude, two `00861F02` calls turn `xmm6`/`(xmm8, xmm7)` into the two angles, and each is wrapped into `[-pi, pi]` by add-`2pi`/`sub-`2pi` loops against `00915620` (`-pi`), `01CEBC78` (`2pi`), `01CEBC50` (`pi`), `00915624` (`-2pi`) before `*rdi` and `*rbx` take them - the heading decomposition every steering consult starts from.

Interior anchor `003A1A24` (function `003A19C0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-how-a-character-turns-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00269C30` | 53 B | when byte `+3` of `rcx` AND `0xE0` equals `0x60`, takes the qword `+0xF0` of qword `+0xB8` of `rcx`, stores `xmm1` times float `01DFE0BC` (decoded 1.0) at its float `+0x2C` and `r8b` at its byte `+0x2B`; otherwise returns without work | `00269C36`, `00269C49`, `00269C54`, `00269C60` |
| `0026AE30` | 82 B | builds the 16 bytes (`xmm1`, `xmm2`, `xmm3`, 1.0 from `01CEBBA8`) on the stack; when byte `+3` of `rcx` AND `0xE0` equals `0x60`, copies them to offsets `+0x00`..`+0x0C` of the qword `+0xF0` of qword `+0xB8` of `rcx` and zeroes its byte `+0x2A`; otherwise returns without storing | `0026AE53`, `0026AE59`, `0026AE6F`, `0026AE79` |
| `0026B450` | 35 B | when `rcx` is non-null and byte `+3` of `rcx` AND `0xE0` equals `0x60`, stores `xmm1` at float `+0x20` of the qword `+0xF0` of qword `+0xB8` of `rcx`; otherwise returns without work | `0026B45B`, `0026B466`, `0026B46D` |
| `002EA780` | 110 B | returns 0 unless `rcx` is non-null, qword `+0xC0` of `rcx` is non-null, the dword at that pointer is not -1, its low word is not -1, the row qword `022C6F28` plus the sign-extended word times `0x740` is non-null, dword `+0x284` of that row is non-zero and the call at `002EA780` + 0x45 (with `rcx` = the row) returns non-zero; then returns 1 when `002EA910` called with the incoming `rcx` returns 1 and 0 otherwise (`sete`) | `002EA7AC`, `002EA7BC`, `002EA7C5`, `002EA7D1`, `002EA7DB` |
