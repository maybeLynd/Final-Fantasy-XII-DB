---
system: Setting the movement mode, and which way a character turns
category: 06-Movement-And-Navigation
status: AUDITED — SD-190 and SD-193 are ANSWERED and DP-2 is SUPERSEDED (owner re-status 2026-09-30, OPUS) — DP-2 SUPERSEDED 2026-09-26 (FABLE, runtime rule: the mode-4 mechanism is tier-1 static; whether the difference is visible in play is a live observation, not queued); DP-1 answered on the page 2026-09-12 (+0x5C is a dead store); residue registered as SD-190 (when the per-frame pass takes the integrator's direct-delta path) and SD-193 (the mode-3 curve 003EC040), both since answered (§6); status line current 2026-09-30, SWE2-DATA
owner_layer: PrimaryOwner:Movement
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: HIGH
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 83 addresses cited - 8 data, 39 entry, 36 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-movement-mode-pass-1 - the mode census re-derived from the last edx write at each site gives exactly section 10's counts (2 x10, 3 x7, 4 x5, 0 x7, and NONE passes 5) over 29 sites in 27 distinct callers, so section 2's '26 callers' is a third number; 0034DC60 does not forward but hardcodes 0 and takes its second argument as the actor; all four normaliser constants and the 9 / 180 / 0.5 degree values are exact; and 01DFE0B4 ships as 1 and is the same global the widget pass found rate-compensating the UI frame counter
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-movement-mode-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# Setting the movement mode, and which way a character turns

## 1. What the player sees

Point Vaan at something behind him and he turns — and he turns **the short way round**. Ask a foe to
face you and it does the same. That choice, left or right, is made once when the new heading is set,
recorded as a single bit, and then spent over the following frames.

The same routine also decides **how fast** the turn goes: **9 degrees per step~~, and never more than~~
~~a half-turn at once~~.** *(corrected 2026-10-02, OPUS: the `π` stored at `0026C237` is never read — DP-1, §5)*

And one of its five modes is **frame-rate sensitive** — it finishes early or late depending on
whether the game is running its 30 or its 60 frames-per-second time base.

## 2. Where this sits

[How a character turns](../Facing-And-Steering/how-a-character-turns.md) documents
`Actor_SetFacingHeading_Variant0` (`0026B5A0`) and its variant `Actor_SetFacingHeading_Variant1` (`0026B620`), and names `+0xF0` as *"pointer to the steering
record"*. **This document is the layer above**: `0026C120` (354 B, **27 distinct callers over 29 call sites** (corrected §11) — the most-called
undocumented `Movement`-owned function in the image) is the routine that sets the *mode* and calls
that facing setter as one of its five outcomes.

## 3. It only ever runs on one kind of actor

```asm
0026C126  movzx eax, byte ptr [rcx + 3]
0026C12D  and   al, 0xE0
0026C12F  cmp   al, 0x60
0026C131  jne   -> return, doing nothing
```

`+0x03` is the actor record's packed discriminator, `(kind << 5) | (sequence & 0x1F)`, so
`& 0xE0 == 0x60` is **`kind == 3`** — the steerable kind. **Every other actor kind falls straight
out of this function**, which is why 27 callers can invoke it unconditionally.

## 4. The record it works on

```
actor  +0x03   packed (kind << 5) | sequence
actor  +0xB8   -> body
body   +0xA8   current heading, f32 radians
body   +0xF0   -> steering record        (named in `how-a-character-turns.md`)
steer  +0x28   MODE, u8            - written on entry, read back as `prev`
steer  +0x29   a SECOND mode byte  - written by Movement_SetSteeringMode, not by this one
steer  +0x34   target heading, f32 radians
steer  +0x58   f32 = 0x3E20D97C  = 0.15707964  = pi/20  = 9 degrees
steer  +0x5C   f32 = 0x40490FDB  = 3.14159274  = pi     = 180 degrees
steer  +0x62   flags; bit 0x40 = the turn direction chosen below
steer  +0x65   u8 gate on the mode-0 path
steer  +0x68   i16 counter, compared against the frame-rate time base
```

> **`+0x28` and `+0x29` are two fields, settled 2026-09-08.**
> [How a character turns](../Facing-And-Steering/how-a-character-turns.md) names `+0x29`
> *“the stored steering mode”*; this document names `+0x28` *“MODE”*. Both setters reach the
> same record by the same `actor → +0xB8 → +0xF0` chain, so the two documents had named two
> **different adjacent bytes** the same thing. The record is `0x80` bytes, inline, and there
> are two of them — [the two steering slots](../Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md).

**The previous mode is captured before the new one is written** (`movzx esi, [rax+0x28]` then
`mov [rax+0x28], dl`), and it is handed to `002E6300` on the mode-0 path — so a transition is
`(prev, new)`, not just `new`.

## 5. Which way it turns, with the real arithmetic

Modes 2, 3 and 4 all begin with the same three lines:

```asm
movss xmm0, dword ptr [steer + 0x34]     ; target heading
subss xmm0, dword ptr [body  + 0xA8]     ; minus current heading
call  0x3A1C50                           ; wrap into (-pi, pi]   ; <- corrected 2026-10-02, OPUS - closed [-pi, pi]: 003A1C58 and 003A1C76 return an exact -pi or +pi unchanged
comiss xmm0, 0
jb    -> or  byte ptr [steer + 0x62], 0x40      ; negative: set the bit
      -> and byte ptr [steer + 0x62], 0xBF      ; non-negative: clear it
```

`003A1C50` is an angle normaliser, and its four constants say so exactly:

```
while (x < -pi) x += 6.2831855      ; 00915620 = -pi,  01CEBC78 = +2pi
while (x >  pi) x -= 6.2831855      ; 01CEBC50 = +pi,  00915624 = -2pi
```

> **So the turn direction is the sign of the shortest signed angle to the target**, and that is the
> whole of it: one bit, `steer->+0x62 & 0x40`, decided once. **A character turns the short way round
> because the difference is wrapped into ~~(−π, π]~~ [−π, π] before its sign is taken.** *(corrected 2026-10-02, OPUS: `003A1C50` is closed at both ends — `003A1C58` and `003A1C76` leave an exact `−π` or `+π` unchanged)*

### Modes 2 and 3 also set the rate

```asm
0026C224  mov dword ptr [steer + 0x58], 0x3E20D97C     ; pi/20  = 9.0 degrees
0026C237  mov dword ptr [steer + 0x5C], 0x40490FDB     ; pi     = 180 degrees
```

**Nine degrees~~, and a ceiling of a half-turn~~.** *(corrected 2026-10-02, OPUS: no instruction reads `+0x5C`; `002E5750` reads `+0x58` only, `002E57EE`; see the supersession note that follows)* ~~Whether `+0x58` is per-frame or per-step, and whether
`+0x5C` is a clamp or a threshold, is **not established here** — the consumer was not read. `DP-1`.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **DP-1** was answered on 2026-09-12. `+0x58` is the per-frame facing cap in modes 2 and 3 and the frame-count divisor in mode 4; `+0x5C` is read by nothing (a dead store).*

## 6. Mode 4 is frame-rate sensitive

```asm
0026C1AE  movsx eax, word ptr [steer + 0x68]
0026C1B2  cmp   eax, dword ptr [01DFE0B4]      ; the frame-rate time base
0026C1B8  ja    -> leave the mode as set
0026C1BE  movss xmm1, dword ptr [steer + 0x34] ; the target heading
0026C1C6  call  0x26B620                       ; Actor_SetFacingHeading_Variant1
0026C1DC  mov   byte ptr [steer + 0x28], 0     ; and RESET the mode to 0
```

`01DFE0B4` is the `FrameLimit` time base documented in
[the game settings config](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
— **1 or 2**, chosen by the player's Frame Rate setting.

> **Mode 4 is a one-shot that completes when its counter has run down to the time base.** With the
> base at 1 the comparison `counter > 1` holds for one more frame than it does at 2, so **the mode
> ends a frame earlier at one frame-rate setting than the other.** That is a real behavioural
> difference driven by a menu option, and it is stated here as what the code does — **whether a
> player can see it is not established.** `DP-2`.

*(2026-09-30, SWE2-DATA: `DP-2` is SUPERSEDED 2026-09-26 (FABLE) under the runtime rule. The mechanism above is the tier-1 answer; whether the one-frame difference is visible in play is a live observation and is not queued.)*

## 7. Mode 0 tears the movement down

```asm
0026C244  if (steer->+0x65 != 0) { 002EBE50(body, 0, 0); 002E8EE0(actor); }
0026C26D  002E6300(actor, body, prev)        ; prev = the mode that was replaced
```

~~The three callees are unread.~~ *(Corrected 2026-09-30, SWE2-DATA: all three are read on [the facing and steering contract](../CONTRACT-facing-and-steering.md), open-questions item 2: `002EBE50` is the steer-mode initiator, `002E8EE0` the render-record resolve gate, and `002E6300` a 10-byte sign gate that tail-jumps to the `+0x64` byte getter when `prev` has bit 7 set.)* **Mode 1 does nothing at all in this routine** beyond writing `+0x28` —
it falls straight to the epilogue; the per-frame integrator then spins the facing by `+0x3C` each
frame (§10), so it is inert only while `+0x3C` is zero.

## 8. Summary of the five modes

| mode | what the routine does |
|---:|---|
| 0 | conditional teardown through `002EBE50` / `002E8EE0`, then `002E6300(actor, body, prev)` |
| 1 | writes the mode and returns (the integrator spins by `+0x3C` per frame — §10) |
| 2, 3 | choose the turn direction; set rate `π/20` and limit `π` (2 turns toward the movement heading, 3 toward `target_heading` — §10) |
| 4 | choose the turn direction; **if `+0x68 <= FrameLimit base`**, set the facing and reset the mode to 0 |
| other | writes the mode and returns |

## 9. What this does not claim

- ~~**What `+0x58` and `+0x5C` are consumed as.**~~ **`DP-1` ANSWERED 2026-09-12 (FABLE):** `+0x58`
  is the per-frame cap of the facing approach in modes 2 and 3 (`003A1AD0`'s third argument, floored
  at 0.5°) and the divisor that converts a heading delta into mode 4's frame count (`002690D0`);
  **`+0x5C` is written and never read** — a dead store by two instruments. §10.
- ~~**That the mode-4 frame-rate difference is visible in play.** The comparison is real; nothing here~~
  ~~measures its effect.~~ `DP-2` *(SUPERSEDED 2026-09-26, FABLE, runtime rule; noted 2026-09-30, SWE2-DATA — §6).*
- ~~**What `002EBE50`, `002E8EE0` and `002E6300` do.** Named as the mode-0 chain, unread.~~ *(Corrected 2026-09-30, SWE2-DATA: read on [the facing and steering contract](../CONTRACT-facing-and-steering.md) — §7.)*
- ~~**What the mode numbers mean.**~~ Named from the integrator and the verbs that pass them, §10:
  1 spin, 2 face the movement heading, 3 turn to a target heading, 4 timed turn, 5 wait for an
  animation state. ~~**Who sets 5 is not found.**~~ *(Corrected 2026-09-30, SWE2-DATA: the untimed turn body `002690D0` stores 5 directly at `002692E8` — the §10 amendment, UQ-101.)*
- **~~What `002654E0` tests and~~ What curve `003EC040` is.** Mode 3's eased path is read only as far
  as its inputs (`target`, the frame index `+0x78`). *(2026-09-30, SWE2-DATA: `002654E0` is read in §10's subtree table — the `+0x28` bit-7 curve-eligibility flag. The curve itself is registered as **SD-193**.)* *(Answered 2026-09-30 (OPUS `79ba50e5c`); register row SD-193, record [`sd193-turn-step-0930`](../../_index/candidates/sd193-turn-step-0930/README.md): there is no easing curve. `003EC040` turns the heading toward the target at a constant angular step per call, the shortest way or a forced direction, and snaps onto the target within one step.)*
- **When the per-frame pass takes the integrator's direct-delta path** (non-zero second argument, §10). The one caller sets it only on a render-side predicate ~~whose meaning is not read~~ *(read 2026-09-30, per SWE2-AUDIT-SEM's batch-5 review C2: bit 0 of a walk over the render record's embedded tween nodes; see the §10 note)*. What stays open is what a tween node's byte `+1` means. **SD-190** (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30 (OPUS `8de16e58c`); register row SD-190, record [`sd190-tween-turn-bit-0930`](../../_index/candidates/sd190-tween-turn-bit-0930/README.md): byte `+1` is the tween's turn phase, so bit 0 reports that an authored move-and-turn tween on the render record is still turning; the direct-delta path also needs actor `+0x0D` bit 1 and a live tween list (the `003E68B0` gate).)*

## 10. The integrator, per mode — 2026-09-12 (FABLE)

The setter is half the story. The other half is **`002E5750`** (935 B), called once per actor per
frame from `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025E3AA`), which reads
`+0x28 & 0x7F` (`00265600`) and dispatches on it. It is skipped when the actor's `+0x18` is 1 or the
controller's `+0x14F` bit 0 is set (attached to another actor's bone, `BV-2`). Before the switch it
reads `turn_step` (`00264750` → `002E4BC0` → `+0x58`) and, **when any mode is active, floors it at
`0x3C0EFA35` = π/360 = 0.5° per frame** (`002E5806`–`002E5821`, through the setter `0026AC70`).

| mode | what the integrator does each frame | set by |
|---:|---|---|
| 0 | nothing | the teardown callers (§7) |
| 1 | `heading += +0x3C`, wrapped, through `Actor_SetFacingHeading_Variant0` (`002E5A9E`–`002E5AED`) — **a constant spin**, inert only because `+0x3C` is zero unless `setvelrotangzx` (`0x003C` → `003535C0` → `0026D630` → `002E60C0`) set it | `0026C120`'s downgrade target |
| 2 | heading approaches **the desired movement heading** (`00263CC0`: context `+0xA4` for class 3, `+0x38` for class 1) by at most `turn_step` (`003A1AD0`, `002E5A78`–`002E5A94`) — "face the way you are going" | every move-family verb, right after its steer (`movea_45`, `amove`, `move`, `rmove`, `cmove`, `ucmove`… — 10 sites pass 2) |
| 3 | heading approaches **`target_heading` `+0x34`** (`00265550`): by `turn_step` through `003A1AD0`, or, when `002654E0` holds and the actor has a render record with a valid index, ~~along the curve~~ by the constant step of `003EC040(target, +0x78, …)` *(corrected 2026-10-02, OPUS: `003EC12E`–`003EC15A` step = `[01DFE0BC]` × `[rec+0x28]` or × `[rec+0x24]`; `003EC1C3` snaps within one step; SD-193)* (`002E595C`–`002E5A5D`); **ends in mode 0 when the heading equals the target exactly** (`ucomiss` / `je` → `0026C120(actor, 0)`) | the untimed turns: `rturn_48` / `turn_62` (`00341AB0`), `rturna` (`0034BE50`), `rturn_50` (`0034CD60`), `rturnt_4b` (`0034D1B0`, first site), `raturn_25e` (`0034E710`), `00357DE0`, `unkCall_3092` — 7 sites pass 3 |
| 4 | **timed linear interpolation** from the start heading (`002652A0`) to `+0x34`: `t = +0x78 / +0x68` (frame index over total frames, `00265630` / `00265660`), `heading = start + wrap(target − start) × t`, then `+0x78 += 1` (`0026C300`); at `t ≥ 1` (or when the manager flag `02099011[…]` forces it) the heading is set to the target and the mode to 0 (`002E5862`–`002E5931`) | the timed turns: `turnt` / `rturnt` (`003425D0`), `rturnt_4b` (second site), `rturnat` / `turnat` (`0034D9B0`), `dira` (`0034E040`), `dir_4e` (`0034E360`) — 5 sites pass 4 |
| 5 | waits: `002EA780` is true when the render record's `+0x284` is set and `002EA910` returns 1 (an animation-state test); then `0026C120(actor, 0)` (`002E5853`–`002E5A6E`) | **nobody found** — all 29 call sites of `0026C120` pass 0, 2, 3 or 4, re-derived independently §11 (`0034DC60` does **not** forward: it is `mov rcx, rdx / xor edx, edx / jmp`, so it hardcodes 0 and takes its *second* argument as the actor) |

> **Amended 2026-09-14 (FABLE) — mode 5 is set after all, by a direct store.** The table's "nobody found" was true only of `0026C120`'s callers. The untimed turn body `002690D0` (the turn verbs `raturn_25e`, `raturna`, `raturnya`, `003578B0`, `unkCall_3092`) **stores 5 into the steering record's `+0x28` itself** (`002692E8`, `mov byte ptr [rcx + 0x28], 5`), without calling `0026C120`. It takes that branch when all three hold:
> - the absolute wrapped delta from the heading to the target is below `1.0472` (π/3, 60°; `0026928F`–`0026929F`);
> - record byte `+0x65` is 0 (`002692A8`);
> - `002E7600(actor)` is non-zero (`002692B0`). That predicate requires the actor's render record (`022C6F28` + index × `0x740`) to have `+0x284` set, which is the same field mode 5's wait arm tests, and then tail-jumps to a second predicate (`002E763A`).
> On that branch it first calls `002EC380(actor, 2, n)`, which puts 2 in bits 3–5 of record `+0x62` and a frame count (`n` over the frame-rate scale, `n` ≥ 1) at `+0x60` (`002692BF`–`002692C7`). The other branch calls it with 1 and takes the frame-counted steering path. **So a small untimed turn on an actor with a ready render record is handed to the animation layer, and mode 5 waits for it**, where a larger one is integrated. Both this section's census and §11's re-derivation counted call sites of the setter, so neither could see a store that bypasses it (UQ-101).

**Where the frame count comes from.** The untimed turn body `002690D0` (`raturn_25e`, `raturna`,
`raturnya`, `003578B0`, `unkCall_3092`) computes it from `turn_step`:
`+0x68 = (i16)((target_heading − heading) / +0x58)` at `00269338`–`00269351`, sets `+0x28 |= 0x80`
(the bit every reader masks off) and `+0x78 = [01DFE0B4]`. The timed turn setter `0026C330`
(`turnt`, `rturnt_4b`, `rturnat`, `dira`, `dir_4e`) sets `+0x68 = +0x66 = [01DFE0B4] + frames /
[01DFE0BC]` and `+0x78 = [01DFE0B4]`. **So `turn_step` is consumed twice — as the per-frame cap in
modes 2 and 3, and as the divisor that turns a heading delta into a frame count for mode 4 — and
`+0x5C` (π) is consumed nowhere**: no reader in the 55-function record census and no access at the
inline-slot aliases `+0x17C` / `+0x1FC` in the 303-row context census. `DP-1`.

With a non-zero second argument `002E5750` skips all of this and instead adds the two floats at its
third argument to the heading and pitch (`002E5787`–`002E57BE`); ~~which caller passes that is not read.~~ *(Corrected 2026-09-30, SWE2-DATA: one caller exists, the per-frame pass at `0025E3AA`, and it passes `ebp`. ~~That is 0 unless actor `+0x0D` bit 1 is set, the actor's render record is live, and the render-side predicate it calls just before returns a value with bit 0 set (`0025E328`–`0025E36E`). What that bit reports is `SD-190`.~~ *(Corrected 2026-09-30, SWE2-DATA, per SWE2-AUDIT-SEM's batch-5 review C2: `ebp` is 1 only if `003E68B0(rec)` is non-zero (`0025E31D`, selected by a `cmovne` just before `0025E328`–`0025E36E`), **and** actor `+0x0D` bit 1 is set, **and** the record is live, **and** bit 0 of `003E6A70`'s result is set. Both predicates are read. `003E68B0` wraps `003AEF20` (armed and list non-empty). `003E6A70` is `003E6E60(rec)` tail-jumping to `003AEF50(rec + 0x550)` over the embedded tween object; it walks the node list `[obj+0x18]` (`rec + 0x568`) by `+0x48`. Bit 0 means some node's byte `+1` is non-zero, and bit 1 means some node's byte `+2` is non-zero. Bit 1 feeds `esi`, then `[rbx+0x10]` bit 2, then actor `+0x0C` bit 4, then `002E5030`'s `edx`. What stays open is what a tween node's byte `+1` means: `SD-190`.)* `_index/candidates/dd-data-5-0930/mm_checks.py` I1, I2.)*

### The `002E5750` exclusive subtree — all 13 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the integrator **13 frontier functions**, and they are one
family: every member opens with the actor-kind gate `([actor+3] & 0xE0) == 0x60` and then reads or
writes the steering record at `[[actor+0xB8]+0xF0]`. They are the gated accessors the mode arms
consult — the getters in §10's table, named here against the field map on
[the steering-slots page](../Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md).
Interior cites are one instruction inside each declared extent (`interior_cite.py scan`; no
boundary crossings).

| member | record field | role | interior |
|---|---|---|---|
| `00264750` (19 B) | `+0x58` | `turn_step` getter — gate, then tail-jump `002E4BC0`; returns 0.0 for unsteerable kinds | `0026475E` |
| `00265810` (19 B) | `+0x3C` | `spin_rate` getter — gate, then tail-jump `002E4BF0` | `0026581E` |
| `002E4BF0` (39 B) | `+0x3C` | `spin_rate` itself — null-guards the actor and `+0xC0`, no kind gate (its callers hold it) | `002E4C0D` |
| `002651C0` (50 B) | `+0x54` / `+0xAC` | actor-class switch: class 1 → `pitch_approach_step`, class 3 → `+0xAC`, else 0.0 | `002651D5` |
| `002652A0` (34 B) | `+0x38` | mode 4's start-heading getter | `002652BC` |
| `002654E0` (40 B) | `+0x28` bit 7 | the ~~mode-4 curve-eligibility flag~~ mode-3 flag that picks the render-step path *(corrected 2026-10-02, OPUS: its one caller `002E596B` is in `002E5750`'s mode-3 arm, reached by the third `sub edi, 1` at `002E583C` / `002E583F`; mode 4 is `002E5862`)* — `record+0x28` tested signed (`cmovl`): the `0x80` bit `002690D0` sets | `00265504` |
| `002655D0` (38 B) | `+0x62` bit 6 | turn-direction getter — `(flags >> 6) & 1` | `002655E8` |
| `00265510` (32 B) | `+0x64` | u8 getter | `00265528` |
| `0026C070` (28 B) | `+0x64` | u8 setter — the write side of the pair | `0026C088` |
| `00265530` (32 B) | `+0x66` | u16 getter | `0026554B` |
| `00265660` (32 B) | `+0x68` | `turn_frames` getter (i16) | `0026567B` |
| `00265630` (33 B) | `+0x78` | `turn_frame_index` getter, truncated `cvttss2si` | `0026564B` |
| `0026C300` (37 B) | `+0x78` | `turn_frame_index` setter — `(f32)edx`, the per-frame advance | `0026C31F` |

The subtree is the whole private surface of the mode machinery: every arm's read goes through
one of these stubs, and every one refuses non-`0x60` actors with the same three instructions —
the gate the two-steering-slots page describes is enforced per accessor, not once at the top.

## 11. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. `check_already_answered.py` run on the addresses this pass touches — `01DFE0B4` is
already documented, and is credited rather than re-announced. Nothing executed.)*

### ✔ The mode census re-derived, and §10's three counts are exact

Every `E8`/`E9` site targeting `0026C120` was found, its owning function resolved, and **the last
write to `edx` before each call** read from the owner's own body — so the mode is taken from the call
site rather than from the caller's name:

| mode | sites | §10 says |
|---:|---:|---|
| 2 | **10** | 10 |
| 3 | **7** | 7 |
| 4 | **5** | 5 |
| 0 | **7** | the rest |
| **5** | **0** | "nobody found" |

**29 sites, 27 distinct caller functions**, body **354 B**. Two functions call it twice — `002E5750`
(the integrator, at `002E58B4` and `002E5A6E`) and `0034D1B0` (`rturnt_4b`, passing **3** then **4**).
**The census is exact and its conclusion was wrong, and those are two different facts.** Every figure above reproduces: 29 sites, 27 distinct callers, 354 bytes, and zero of them passing 5. What does not follow is *"nobody sets mode 5"*, because **mode 5 is stored without the setter** - `002690D0` writes `mov byte ptr [rcx + 0x28], 5` at `002692E8` into `[[actor + 0xB8] + 0xF0]`, on the branch where the actor's kind bits are `0x60` and the wrapped turn is small (FABLE 2026-09-14, verified here from the shipping bytes; see the §10 amendment).

**The instrument was keyed on the call and the write bypasses the call**, which is the failure mode this whole section exists to demonstrate - it simply demonstrates it one level further out than the section claimed. A census that counts call sites answers "who calls this", and it was read as answering "who sets this". The two questions differ by exactly one direct store.

**§2's "26 callers" is a third number.** The site count is 29 and the distinct-caller count is 27;
26 is neither.

### ✖ Corrected: `0034DC60` does not forward

§10 says it *"forwards its caller's value, which is 0"*. Its whole body is three instructions:

```asm
0034DC60  mov rcx, rdx        ; the SECOND argument becomes the actor
0034DC63  xor edx, edx        ; the mode is hardcoded 0
0034DC65  jmp 0x26C120
```

It **discards its first argument**, takes its second as the actor, and passes a literal 0. The
conclusion is unaffected — it still contributes a 0 — but a reader tracing "whose value" would look
for a caller that has none.

### ✔ Every constant resolves, to the address and to the value

| the page says | measured |
|---|---|
| `003A1C50`'s four constants at `00915620`, `01CEBC78`, `01CEBC50`, `00915624` | **all four, at those exact addresses**, holding `-3.1415927`, `6.2831855`, `3.1415927`, `-6.2831855` |
| `+0x58` = `0x3E20D97C` = π/20 = 9° | `0.157079637` rad = **9.000000°** |
| `+0x5C` = `0x40490FDB` = π | `3.141592741` rad = **180.000005°** |
| §10's floor `0x3C0EFA35` = π/360 | `0.008726646` rad = **0.500000°** |
| §3's discriminator | `movzx eax, byte [rcx+3] / and al, 0xE0 / cmp al, 0x60 / jne` — exact |
| the capture-then-write of `+0x28` | `movzx esi, [rax+0x28]` then `mov [rax+0x28], dl` — exact, in that order |

The normaliser's shape is worth stating once more precisely: it is two `while` loops, **`+2π` while
`-π > x` and `-2π` while `x > +π`** (`003A1C5B`–`003A1C8A`), so the result is closed at `+π` and ~~open~~ closed
~~at `-π` — which is what §5's "(−π, π]" says.~~ at `-π` too: an input of exactly `-π` fails `-π > x`, skips both loops and is returned unchanged, so §5's "(−π, π]" is wrong *(corrected 2026-10-02, OPUS: `003A1C58` `comiss xmm1(-π), xmm0` / `jbe` skips the `+2π` loop, `003A1C76` `comiss xmm0, xmm1(+π)` / `jbe` returns)*.

### ○ The frame-rate global, joined rather than discovered

`01DFE0B4` **ships as `1`** in `.data` — not BSS — and
[what the engine fixes at boot](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)
already records it as the time-base mode word (**1 at 30 fps, 2 at 60**, written only when
`FrameLimit=60`, which is why the shipped `1` matters). Credited, not re-derived.

> **The same global was met from the other side today.** The falsification pass on
> [the widget animation start](../../16-UI/Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md)
> found the UI tick advancing the frame counter `0208F570` by **`2 / [01DFE0B4]`** — 1 at 60 fps, 2 at
> 30 — so the counter stays in 60 Hz units. **One setting, two subsystems**: it rate-compensates the
> UI clock and it moves mode 4's completion threshold. §6's "a real behavioural difference driven by a
> menu option" is the same lever, seen where it does *not* compensate.

**Not claimed.** `DP-2` — nothing here measures whether the mode-4 difference is visible, and
**nothing was run**. `002EBE50`, `002E8EE0`, `002E6300`, `002654E0`, `003EC040` remain unread *(2026-09-30, SWE2-DATA: since read, all but the `003EC040` curve — §7, §9)* *(2026-09-30, OPUS owner read: `003EC040` read too — SD-193 ANSWERED, a constant angular step toward the target rather than a curve, §6)*. The
`+0x5C`-is-never-read negative is **FABLE's census and was not re-run**; this pass measured the
constant's value, not its readers.

## 12. Key addresses, call chain, modding notes and evidence (SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-DATA) from the facts §3–§11 establish; each row points at where it is read.*

### Key addresses (SWE2-DATA, 2026-09-30)

| address | role | where |
|---|---|---|
| `0026C120` | the mode setter: kind-3 gate, writes steer `+0x28`, turn direction, rate, mode-4 early end, mode-0 teardown | §3–§8 |
| `002E5750` | the per-frame integrator, dispatching on `+0x28 & 0x7F` | §10 |
| `003A1C50` | the angle normaliser into ~~(−π, π]~~ [−π, π] *(corrected 2026-10-02, OPUS: `003A1C58` / `003A1C76`)* | §5 |
| `0026B620` | `Actor_SetFacingHeading_Variant1`, mode 4's final set | §6 |
| `002EBE50` / `002E8EE0` / `002E6300` | the mode-0 chain | §7 |
| `002690D0` | the untimed turn body: frame count from `turn_step`, and the direct store of mode 5 | §10 |
| `0026C330` | the timed turn setter | §10 |
| `00263CC0` | ~~the movement-kind speed read~~ the desired-heading read (class 1 `+0x38`, class 3 `+0xA4`) *(corrected 2026-10-02, OPUS: `00263CD6`–`00263CED` return context `+0xA4` / `+0x38`, the desired movement heading §10's mode-2 row names)* | §10, EC7-105 |
| `01DFE0B4` / `01DFE0BC` | the `FrameLimit` time base and the frame-rate scale | §6, §10 |

### Call chain (SWE2-DATA, 2026-09-30)

```
script verbs (move family, turns, 0034CD60 / 0034D1B0 / 0034E710 ...) -- 29 sites --> 0026C120(actor, mode)
    mode 0      -> 002EBE50 + 002E8EE0 (when steer +0x65) -> 002E6300(actor, body, prev)
    mode 2 / 3  -> 003A1C50 (direction bit), rate pi/20, limit pi
    mode 4      -> 003A1C50; when +0x68 <= [01DFE0B4]: 0026B620, mode := 0
untimed turns -> 002690D0 -> 002692E8 stores mode 5 directly
per frame: WorldActor_UpdateRuntimeAndScriptExecutionState -- 0025E3AA --> 002E5750
    -> 00265600 (mode), 00264750 -> 002E4BC0 (turn_step), 003A1AD0 (approach), 003EC040 (mode-3 curve),   <- corrected 2026-10-02, OPUS - a constant angular step, not a curve (003EC12E-003EC1E1, SD-193)
       002EA780 (mode-5 wait), 0026C120(actor, 0) (ends 3 and 5)
```

### Modding notes (SWE2-DATA, 2026-09-30)

- The turn rate of modes 2 and 3 is the immediate `0x3E20D97C` (π/20, 9°) stored at `0026C224`, and the integrator floors any active mode's step at `0x3C0EFA35` (0.5°, `002E5806`–`002E5821`).
- `+0x5C` (π) is written and never read, so changing it has no effect (DP-1).
- Mode 4's length depends on the player's Frame Rate setting through `01DFE0B4` (§6).

### Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| the kind-3 gate and the `(prev, new)` capture | `0026C126`–`0026C131`; §3, §4 | 1 |
| the turn direction is the sign of the wrapped delta | `003A1C50` and its four constants; §5 | 1 |
| mode 4 ends against the `FrameLimit` base | `0026C1AE`–`0026C1DC`; §6 | 1 |
| the mode census (29 sites, 0 / 2 / 3 / 4) | §11; `_index/candidates/dd-data-5-0930/mm_checks.py` C1 (29 raw call sites) | 1 |
| mode 5 is stored directly by `002690D0` | `002692E8`; §10 amendment, UQ-101 | 1 |
| `00263CC0` reads class 1 `+0x38`, class 3 `+0xA4` | `_index/candidates/dd-data-5-0930/mm_checks.py` K1 | 1 |
| the integrator has one caller, and its second argument is gated | `_index/candidates/dd-data-5-0930/mm_checks.py` I1, I2 | 1 |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Party — CLIENT.**
  - `PartyControl_ApplyAnalogLocomotionToActor` calls `003A1AD0` and `003EC040`.
  - The 639-byte Party-filed body sets heading through `Actor_SetFacingHeading_Variant1`.
- **CombatAction — CLIENT.** `Battle_ProcessActionTarget` calls `Actor_SetFacingHeading_Variant1`.
- **Presentation — SERVICE.** `003EC040` resolves the character's active presentation entry
  (`CharacterRenderRecord_ResolveActivePresentationEntry`) and calls a 32-byte Presentation helper. So this step
  consults the render record.
- **Audio — CLIENT.** The angle wrap `003A1C50` is shared with two Audio-filed positional bodies
  ([facing and steering](../CONTRACT-facing-and-steering.md), crossings).
- **CombatFormula — CLIENT.** `00265020` on this page — a callee of `00357DE0` — is also called by a body in that
  layer's census. The crossing is that layer consulting this page's function, not that this page owns anything in
  that layer. MECHANICAL accounting (SWE2-EC7, 2026-09-19).
- **Gameplay — CLIENT.** `00265020` on this page is also called by bodies in that layer's census. The crossing is
  that consultation, not a shared responsibility. MECHANICAL accounting (SWE2-EC7, 2026-09-19).
- **Rewards_Progression_Economy — CLIENT.** `00265020` on this page is also called by bodies in that layer's census.
  The crossing is that consultation, not a shared responsibility. MECHANICAL accounting (SWE2-EC7, 2026-09-19).
- **Spawn_Encounter_Lifecycle — CLIENT.** `00265020` and `00265200` on this page are also called by bodies in that
  layer's census. The crossing is that consultation, not a shared responsibility. MECHANICAL accounting (SWE2-EC7,
  2026-09-19).

**Script_VM_Native_Bridge — SERVICE (124 edges through 32 of this page's functions, 65 script
bodies; six subjects read in full).** This is the widest crossing in the pass, and counting it as
124 relationships would be wrong in a specific way: it is one layer calling a family of primitives
that all begin the same way.

**Six of this page's busiest functions open with the identical three instructions** —
`movzx eax, byte [actor+3] / and al, 0xE0 / cmp al, 0x60` — and return without doing anything if it
does not match. `0026C120` (16 edges), `002EBE50` (13), `002EC380` (12), `0026AC70` (9), `002690D0`
(5) and `0026C330` (5). That is **kind 3**, and it is the same field and the same value the movement
bodies on [the FCP parameter block](../../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md)
test. There is no shared gate function; each body tests it for itself.

Two further things came out of reading them. `002EC380` writes **only bits 3 to 5** of
`byte[[actor+0xB8]+0xF0 + 0x62]`, with the read-modify-write idiom `shl dl, 3 / xor dl, [rax+0x62] /
and dl, 0x38 / xor [rax+0x62], dl` — and `0026A1A0` on the other page writes **bit 7** of that same
byte the same way, so it is a shared bitfield with each writer confined to its own bits. And the
float at `01DFE0BC` is **in `.data`, not `.rdata`**: `0026AC70` multiplies by it, `002EC380` and
`0026C330` divide by it, and it holds `1.0f`. A scale factor that is a no-op as shipped is still a
scale factor, and the three of them move together.

On the other side, the busiest script neighbours are the stack pops themselves —
`VMValueStack_PopNumericDiscard` (7) and `VMValueStack_PopInt32CoerceFloat32` (6) — which is what a
layer of verb handlers looks like from here. The angle wrap `003A1C50`, already noted above for
Audio, is the one body doing no kind test at all: it loops adding `2π` while the value is below
`-π` and subtracting while above `+π`, and cares about nothing else.

**Six of the 65 script bodies are read; the rest are counted.** Edge count and subject list from
`edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
- **UI - CLIENT (2 edges).** `00265020`, `00265200` are also called by bodies filed to UI: `003C5130` - shared machinery across the layer boundary, no shared ownership.

## SWE2-EC7-39 update (2026-09-19) - `003EC040`

`003EC040` (433 B) is a movement-mode body - `01DFE0BC`/`022C6F28`, `003A1AD0` pair plus `00422D50`/`003E56C0`/`003EC510`/`003A1980`. Interior anchor `003EC0D2` (a `00422D50` call).

## SWE2-EC7-44 update (2026-09-19) - `00357DE0`

`00357DE0` (273 B) is an effect-element body - `00263D00`/`00265020`/`00265200`/`00267DB0`/`00267F60`/`0026C090`/`0026C120`. Interior anchor `00357E13` (a `00263D00` call).

## SWE2-EC7-48 update (2026-09-19) - `003578B0`

`003578B0` (200 B) is a mode-5 turn body - `00263D00`/`002690D0`/`0026A1A0`/`0026AC70`/`002E9B10`/`002EC510`/`00357DE0`. Interior anchor `003578DA` (a `00263D00` call).

## SWE2-EC7-50 update (2026-09-19) - `0034E710`

`0034E710` (183 B) is a body - `00265200`/`00267DB0`/`002690D0`/`0026AC70`/`0026C090`/`0026C120`/`0026C290`/`002E9B10`. Interior anchor `0034E737` (a `00265200` call).


## SWE2-EC7-63 update (2026-09-19) - `0034CD60`

`0034CD60` (144 B) is a movement-mode body - `00265200`/`00267DB0`/`0026C090`/`0026C120`/`0026C290`/`003A1C50`. Interior anchor `0034CD85` (a `00267DB0` call).



## SWE2-EC7-63 update (2026-09-19) - `0034D1B0`

`0034D1B0` (143 B) is a movement-mode body - `00265200`/`00267DB0`/`00267E10`/`0026C090`/`0026C120`/`0026C290`. Interior anchor `0034D1D0` (a `00267E10` call).


## SWE2-EC7-69 update (2026-09-19) - `0026AC70` angle-wrap setter measured

`0026AC70` (98 B) is the turn setter the mode page names: `xmm3 = xmm1 *
float[01DFE0BC]` (the `.data` scale factor, currently `1.0f`), then a
sign-picked wrap bias - `+π` (`01CEBC50`) for nonnegative input, `-π`
(`00915620`) for negative - is added before the gate. Only objects whose
`byte[+3] & 0xE0 == 0x60` (kind 3) continue: `xmm3` is divided by `2π`
(`01CEBC78`), truncated to int and back, the integer turns subtracted, the
bias un-added - an exact ~~`(-π, π]`~~ `[-π, π]` normalize, `+π` and `-π` swapping *(corrected 2026-10-02, OPUS: `0026AC7E`–`0026ACC5`, the sign-biased truncation of `0026A8E0`)* - and the result tails into
`002E5B90(rcx, xmm3)` as `xmm1`. Non-kind-3 objects return without the call.
Interior anchor `0026ACAE` (the `divss xmm0, [01CEBC78]` 2π divide).

## SWE2-EC7-75 update (2026-09-19) - `002EC510` + `002E9B10` movement-mode helpers measured

`002EC510` (114 B) is the `0x60`-kind four-tail dispatch: `byte[rdx+3]
& 0xE0 == 0x60` and `[rdx+0xB8]` non-NULL gate a `ecx` selector - 0
tails `002EC2C0`, 1 tails `002EBFA0` with `(byte[r9+0x15], word[r8],
0x30B)`, 2 tails `002EC140`, 3 tails `002EC1C0` (the last two with
`xmm1 = [r8+4]`, `xmm2` zeroed).
Interior anchor `002EC571` (the `jmp 002EBFA0` tail).

`002E9B10` (43 B) is the gated `003E6150` call: `rcx`, `[rcx+0xC0]`,
`[rax] != -1` gate `003E6150(ecx=[rax], edx=0x9000909)` with
`xmm0 = 0x3FBF7CD1` (~1.497) - the constant-flagged call the
movement-mode bodies share.
Interior anchor `002E9B35` (the `jmp 003E6150` tail).

## SWE2-EC7-76 update (2026-09-19) - `0026A1A0` chained-record bit-7 setter measured

`0026A1A0` (46 B) is the `0x60`-kind chained setter: `[rcx+0xB8]` ->
`[rax+0xF0]` -> `byte[+0x62] = (edx != 0) << 7 | (old & 0x7F)` - the
two-hop bit-7 write the movement-mode bodies share.
Interior anchor `0026A1C9` (the `+0x62` store).

## SWE2-EC7-87 update (2026-09-20) - `003DDAD0` flag-decoded record build measured

`003DDAD0` (100 B) is the coded-arg forward the movement-mode
callers run: `00263F40(rcx)` resolves the record and
`byte[+0xD] >> 7` feeds `002E8170`; then `r8d` bit `0x18`
selects a `01EFE9D0` table dword indexed by `r8d & 0xFFFFFF`,
or `(byte[rbx+0x15] << 0x14) | r8d | bit 0xC`; the body tails
`002EB3E0(rcx, decoded, -1.0f)`.
Interior anchor `003DDB2F` (the `002EB3E0` tail).

## SWE2-EC7-98 update (2026-09-20) - `002E4BC0` measured

`002E4BC0` (39 B) is the chained float read `00264750` and
`002690D0` call: null `rcx` or `[rcx+0xC0] == 0` yields
`xmm0 = 0`, else `xmm0 = [[[rcx+0xB8]]+0xF0] +0x58` - the
two-deref fetch the movement-mode arms read a scalar
parameter through.
Interior anchor `002E4BDD` (the `movss` read).

## SWE2-EC7-105 update (2026-09-20) - `00263D00` measured

`00263D00` (39 B) is the class-3 threshold
test `003578B0`, `00357C40`, `00357D10` and
`00357DE0` call: `byte[rcx + 3] & 0xE0 ==
0x60` gates, then
`byte[[[rcx + 0xB8] + 0xF0] + 0x62] >= 0x80`
answers 1 else 0 - the two-level
indirection predicate the movement-mode
arms share.
Interior anchor `00263D18` (the `0x80`
compare).

`00263CC0` (55 B) is the ~~movement-kind speed read~~ desired-heading read *(corrected 2026-10-02, OPUS: `00263CDD` / `00263CED` load context `+0xA4` / `+0x38`, the field `Actor_SetDesiredMovementHeading` writes)*: `byte[rcx+3] >> 5` selects the class - kind 1 returns `float[[rcx+0xB8] + 0x38]`, ~~kind 2 returns~~ kind 3 returns `float[[rcx+0xB8] + 0xA4]` *(corrected 2026-09-30, SWE2-DATA: `sub edx, 1` then `cmp edx, 2` selects class 3, as §10 says; `_index/candidates/dd-data-5-0930/mm_checks.py` K1)*, every other kind and the null record return 0.0f - the ~~two-speed~~ two-class heading branch the facing and battle-unit callers share *(corrected 2026-10-02, OPUS: it returns a heading, not a speed, `00263CD6`–`00263CED`)*.

Interior anchor `00263CD6` (function `00263CC0`).

`003EBF60` (219 B) is the speed-factor compute `002690D0` runs for record `cx`: a `-1` index or a `022C6F28` `0x740` record with `+0x284` clear returns `0`; else `003E56C0` resolves the object and its `[+0x24]` scales the `01DFE0BC` frame quantum into `xmm2` - `*rbx` gets `(xmm1 - (1 - (xmm1 - 6.7)^2 / 67.7) * 0.79) / xmm2` (constants `00915730`/`00915738`/`00915614`) and `*rdi` gets `|xmm1 / xmm2|` - the normalized turn/speed pair the mode selector consumes

Interior anchor `003EBFD8` (function `003EBF60`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-setting-the-movement-mode-and-which-way--cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0026C330` | 117 B | computes `r8d` as the truncated quotient of `edx` by float `01DFE0BC` (decoded 1.0) when `edx` is greater than 0 (signed), else 0; then, only when byte `+3` of `rcx` AND `0xE0` equals `0x60` (else it returns), takes the qword `+0xF0` of qword `+0xB8` of `rcx` and stores word `01DFE0B4` plus `r8w` at its word `+0x68` and word `+0x66`, and dword `01DFE0B4` (decoded 1) converted to float at its float `+0x78` | `0026C33B`, `0026C353`, `0026C373`, `0026C389`, `0026C3A0` |
| `0026D630` | 98 B | multiplies `xmm1` by float `01DFE0BC` (decoded 1.0) and adds 3.141593 (`01CEBC50`) when the product is not below 0.0, or -3.141593 (`00915620`) when it is (`jb`); when byte `+3` of `rcx` AND `0xE0` does not equal `0x60` it returns; otherwise it subtracts from the sum the truncated quotient of the sum by 6.283185 (`01CEBC78`) times 6.283185, then the same added offset, and tail-jumps `002E60C0` with `rcx` unchanged and that result in `xmm1` | `0026D636`, `0026D641`, `0026D65F`, `0026D66E`, `0026D68C` |
| `002E60C0` | 35 B | when `rcx` is non-null and qword `+0xC0` of `rcx` is non-zero, stores `xmm1` at float `+0x3C` of the qword `+0xF0` of qword `+0xB8` of `rcx`; otherwise returns without work | `002E60C5`, `002E60D6`, `002E60DD` |
| `002E8170` | 87 B | returns without work unless `rcx` is non-null, qword `+0xC0` of `rcx` is non-null, the dword at that pointer is not -1, its low word is not -1, the row qword `022C6F28` plus the sign-extended word times `0x740` is non-null and dword `+0x284` of that row is non-zero; then sets bit 19 (`bts 0x13`) of that dword when `edx` is non-zero, or clears it (`btr`) when `edx` is zero, and stores it back | `002E8193`, `002E81A3`, `002E81B1`, `002E81BC`, `002E81C0` |
| `002EA780` | 110 B | returns 0 unless `rcx` is non-null, qword `+0xC0` of `rcx` is non-null, the dword at that pointer is not -1, its low word is not -1, the row qword `022C6F28` plus the sign-extended word times `0x740` is non-null, dword `+0x284` of that row is non-zero and the call at `002EA780` + 0x45 (with `rcx` = the row) returns non-zero; then returns 1 when `002EA910` called with the incoming `rcx` returns 1 and 0 otherwise (`sete`) | `002EA7AC`, `002EA7BC`, `002EA7C5`, `002EA7D1`, `002EA7DB` |
| `002EA910` | 96 B | returns 1 unless `rcx` is non-null, qword `+0xC0` of `rcx` is non-null, the dword at that pointer is not -1, its low word is not -1, the row qword `022C6F28` plus the sign-extended word times `0x740` is non-null, dword `+0x284` of that row is non-zero and the call at `002EA910` + 0x40 (with `rcx` = the row) returns non-null; in that case tail-jumps `003E2C00` with that pointer as `rcx` | `002EA937`, `002EA947`, `002EA950`, `002EA961`, `002EA966` |
| `003425D0` | 110 B | calls `0026C330(rdx, 00267E10(r9))`, then `0026A1A0(rdx, 0)`, then `00357DE0` with the four incoming arguments `rcx`, `rdx`, `r8`, `r9`, and tail-jumps `0026C120(rdx, 4)` | `003425F3`, `003425FD`, `00342607`, `00342618`, `00342639` |
| `0034D9B0` | 100 B | calls `0026C330(rdx, 00267E10(r9))`, then `0034BE50` with the four incoming arguments `rcx`, `rdx`, `r8`, `r9`, and tail-jumps `0026C120(rdx, 4)` | `0034D9D3`, `0034D9DD`, `0034D9EE`, `0034DA0F` |
| `0034E040` | 110 B | calls `00267F90(r9, 0)`, then `0026C330(rdx, 00267E10(r9))`, then `0034BE50` with the four incoming arguments `rcx`, `rdx`, `r8`, `r9`, and tail-jumps `0026C120(rdx, 4)` | `0034E065`, `0034E06D`, `0034E077`, `0034E088`, `0034E0A9` |
| `0034E360` | 120 B | calls `00267F90(r9, 0)`, then `0026C330(rdx, 00267E10(r9))`, then `0026A1A0(rdx, 0)`, then `00357DE0` with the four incoming arguments `rcx`, `rdx`, `r8`, `r9`, and tail-jumps `0026C120(rdx, 4)` | `0034E385`, `0034E397`, `0034E3A1`, `0034E3B2`, `0034E3D3` |
| `003A1980` | 23 B | converts `xmm0` to double, clears its sign bit with the mask `01CEBD80` (`andps`), converts it back to float and returns the `minss` of that absolute value and `xmm1` | `003A1983`, `003A1987`, `003A1992` |
| `003EC510` | 103 B | adds 6.283185 (`01CEBC78`) to `xmm0` while it is below -3.141593 (`00915620`), then adds -6.283185 (`00915624`) while it is above 3.141593 (`01CEBC50`); returns 0.0 when the result equals 0.0; otherwise when `edx` is 0 adds 6.283185 to a negative result, when `edx` is 1 adds -6.283185 to a positive result, and returns the value (unchanged for any other `edx`) | `003EC525`, `003EC543`, `003EC54F`, `003EC568`, `003EC572` |
