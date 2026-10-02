---
system: The two steering slots, and what a character resumes
category: 06-Movement-And-Navigation
status: AUDITED
owner_layer: PrimaryOwner:Movement
evidence_tier: 1
level: L2
readiness: TYPE RESOLVED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 95 addresses cited - 8 data, 34 entry, 53 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-steering-slots-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The two steering slots, and what a character resumes

## 1. What the player sees

Vaan is walking somewhere. A cutscene starts, or a conversation, or a battle transition — and he
stops and does whatever the interruption tells him to. Then it ends, and **he goes back to what he
was doing**, not to standing still.

He can do that because he was never only doing one thing. **Every steerable character carries two
complete sets of steering state**, and the engine flips between them with a single byte: one is
handed to the interruption, the other keeps the walk it was in the middle of. When the
interruption ends, the engine flips back and **replays the parameters it saved**.

And the depth is exactly one. **A second interruption while one is outstanding is refused** — not
queued, not nested. It simply does nothing.

## 2. Where the record lives — and it is not allocated

[How a character turns](how-a-character-turns.md) and
[setting the movement mode](../Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md)
both reach *"the steering record"* the same way, `actor → +0xB8 context → +0xF0`, and neither says
what it is. It is not a heap object:

```asm
00269F90  movzx eax, byte ptr [rcx + 0xDC]   ; the slot selector
00269F97  cmp   al, 1
00269F99  ja    0x269FB3                     ; out of range -> return, changing NOTHING
00269F9B  movsx rax, al
00269F9F  shl   rax, 7                       ; * 0x80
00269FA3  add   rax, 0x120
00269FA9  add   rax, rcx
00269FAC  mov   qword ptr [rcx + 0xF0], rax  ; the cursor
00269FB3  ret
```

```c
void Movement_SelectSteeringSlot(Context *ctx)          /* 00269F90, 36 B */
{
    uint8_t sel = ctx->slot_DC;
    if (sel > 1) return;                                 /* leaves the old cursor standing */
    ctx->steering_F0 = (SteeringRecord *)((char *)ctx + 0x120 + (sel << 7));
}
```

> **`shl rax, 7` is the size.** The record is **`0x80` = 128 bytes**, and there are **exactly two**,
> inline in the movement context at **`+0x120`** and **`+0x1A0`**. `+0xF0` is not an owning pointer
> — it is a **cursor into an embedded array of two**. Nothing allocates a steering record and
> nothing frees one.

**The bound check fails silently and open.** `sel > 1` returns without touching `+0xF0`, so a
selector that goes out of range does not clear the cursor or fault — it leaves whichever record was
selected last. That is fail-*open*, and it is worth knowing before writing to `+0xDC`.

### The context fields this uses

```
actor   +0x03   packed (kind << 5) | sequence   -- & 0xE0 == 0x60 gates every entry point
actor   +0x18   byte; == 1 also refuses the push and the pop
actor   +0xB8   -> movement context
context +0xA8   f32  current heading, radians
context +0xDC   u8   THE SLOT SELECTOR, 0 or 1
context +0xF0   ->   cursor into the two records below
context +0x120  SteeringRecord[0]      0x80 bytes
context +0x1A0  SteeringRecord[1]      0x80 bytes
```

## 3. Push and pop

Two functions call the selector and nothing else does — **three `E8` sites in the whole image, no
`E9`, no address-taken reference** (controls: `E8` positive at `001DE4F0`, `E9` positive at
`001D1660`, operand instrument positive at `02ADD0A8`).

### Push — `002EAB80`, 99 B

```c
if (actor->_18 == 1) return;
if ((actor->packed_03 & 0xE0) != 0x60) return;          /* steerable kinds only */
ctx = actor->context_B8;
if (ctx->slot_DC != 0) return;                          /* ALREADY PUSHED -- refuse */
FUN_002627C0(ctx);                                      /* unread */   /* <- corrected 2026-10-02, OPUS - read: it copies the 0x80 steering record from slot [+0xDC] to [+0xDC+1] (CONTRACT-facing-and-steering.md section 14 item 2) */
ctx->slot_DC += 1;                                      /* -> slot 1 */
Movement_SelectSteeringSlot(ctx);
Movement_SetSteeringMode(actor, 0);                     /* 0026AE90 */
Movement_SetMode(actor, 0);                             /* 0026C120 */
```

**The new slot is handed over in mode 0, twice** — once through each of the two mode setters (§4),
which is how the interruption gets a clean state rather than the walk's.

### Pop — `002EAAA0`, 145 B

```c
if (actor->_18 == 1) return;
if ((actor->packed_03 & 0xE0) != 0x60) return;
ctx = actor->context_B8;
if (ctx->slot_DC == 0) return;                          /* NOTHING PUSHED -- refuse */
ctx->slot_DC -= 1;                                      /* -> slot 0 */
Movement_SelectSteeringSlot(ctx);
rec = ctx->steering_F0;
switch (rec->flags_62 & 7) {                            /* which resume shape */
    case 0:  FUN_002EC2C0(actor, &rec->resume_10);      break;   /* pass the triple by address */
    case 1:  FUN_002EBFA0(actor, rec->resume_10,
                                 rec->resume_14,
                                 rec->resume_18);       break;   /* pass it by value */
    default: break;                                             /* resume nothing */
}
FUN_002EC3F0(actor);
FUN_002E8EE0(actor);
```

> **The saved walk is three dwords and a shape code.** `flags & 7` chooses whether the resume
> parameters go to `002EC2C0` **by address** or to `002EBFA0` **by value**, and any other value
> resumes nothing at all. **Only 0 and 1 were observed**; what the remaining six encode is not
> established, and no caller was traced that sets them *(answered: see DW-1 in §8 — 4–7 are never written, FABLE 2026-09-15; 2026-10-02, OPUS)*. `DW-1`.

**Both guards are symmetric and both fail closed**: push refuses when the selector is already 1, pop
refuses when it is already 0. So **the stack is depth one** — the engine cannot nest two
interruptions, and the second one silently does nothing rather than corrupting the first.

## 4. Two adjacent mode bytes, and they are not the same field

The two existing documents each call one byte *"the steering mode"*, and they name **different
bytes**. Read against the binary, **both are right and they are two fields**:

| offset | written by | what it selects |
|---|---|---|
| `+0x28` | `0026C120` (354 B) | the **movement** mode — 0 teardown · 1 inert · 2/3 turn + rate · 4 one-shot facing |
| `+0x29` | `0026AE90` `Movement_SetSteeringMode` (127 B) | the **steering** mode — the speed-ramp shape of a scripted move: 0 off · 1 constant · 2 accelerate · 3 decelerate · 4 both; collapsed to 1 when `+0x2C` (the ramp acceleration) is exactly `0.0` ([how a character turns](how-a-character-turns.md) §2, 2026-09-12) |

Both reach the same record by the same chain — `0026AE90` at `0026AEA3`/`0026AECD`, `0026C120` at
`0026C13C`/`0026C148` — so this is one record with two adjacent one-byte mode selectors, written by
two different setters, and the push calls **both** in sequence. **`+0x28` governs the facing**
(spin / face-the-movement / turn-to-target / timed turn / wait — [the movement-mode page](../Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md) §10)
**and `+0x29` governs the speed ramp of a steer toward a target** ([how a character turns](how-a-character-turns.md) §2); a move verb sets both — `+0x29` from `setaccr`'s configuration and `+0x28 = 2` so the actor faces the way it walks.

## 5. The whole record, from its readers

`record_field_scan.py --chain 0xB8,0xF0` follows the two hops register by register inside each
function body and records every displacement off the register that ends up holding the record.
**55 functions reach it this way; 32 distinct fields; `+0x00` to `+0x7C`, which exactly fills the
`0x80` the stride proves.** Two hand-derived controls reproduce (§7).

**Extended 2026-09-17:** two more functions reach the record by the *one*-hop `arg+0xF0` — the
context arrives as an argument, so the two-hop chain never forms inside the body and the original
sweep could not see them. `record_field_scan.py --chain 0xF0` (control `002E45E0` = `+0x2A`,
`+0x20`, both reproduced) adds 22 rows to the checker-wired access census — nineteen from
`Movement_UpdateSteeringTowardTarget` `002E45E0` (the busiest reader: `+0x00`/`+0x04`/`+0x20`/
`+0x24`/`+0x28`/`+0x29`/`+0x2A`/`+0x2C`/`+0x50`/`+0x54`) and three from
`Movement_ClearSteeringRequest` `002E55C0` (`+0x29` clear, `+0x28` read, `+0x24` clear), all
carrying `route=chain:0xF0`. Every function the field rows cite is now in the census.

Full census with every site: [`steering-record-fields-observed.tsv`](steering-record-fields-observed.tsv);
per-access, checker-wired: [`steering-record-accesses.tsv`](../Steering-Record/steering-record-accesses.tsv).
In the type store as **`SteeringRecord`** — 32 fields, **13 named, 19 `UNRESOLVED`**.

| offset | type | name | what establishes it |
|---|---|---|---|
| `+0x00`/`+0x04`/`+0x08`/`+0x0C` | `f32` ×4 or `u32`,`i32` | `target` | kind 0: the target position `(x, y, z, 1.0)` (`0026AE6F`); kind 1: the target actor's ordinal and manager index, negative = the party focus (`0026AE08`, `0026AE11`) — 2026-09-12 |
| `+0x10`/`+0x14`/`+0x18` | `u32` ×3 | `resume_a/b/c` | the three parameters the pop replays (§3) |
| `+0x20` | `f32` | `arrival_radius` | `setreachr` (`0x0076` → `0026B450`); subtracted from the distance before every ramp and arrival test — 2026-09-12 |
| `+0x24` | `f32` | `requested_speed` | the move verb's speed × `[01DFE0BC]` (`0026D72C`, `0026D842`); the ramps' `v`; zeroed on arrival and on mode 0 — 2026-09-12 |
| `+0x28` | `u8` | `movement_mode` | `0026C153` writes it, `0026C14F` reads the previous; bit 7 is set by the turn body `002690D0` and masked off by every reader |
| `+0x29` | `u8` | `steering_mode` | `0026AED4`; 0 off · 1 constant · 2 accelerate · 3 decelerate · 4 both — 2026-09-12 |
| `+0x2A` | `u8` | `target_kind` | 0 position (`0026AE79`), 1 actor (`0026AE1C`) — 2026-09-12 |
| `+0x2B` | `u8` | `configured_steering_mode` | `setaccr`'s mode operand, default 4 (`00269C60`); the move verbs copy it into `+0x29` when `+0x2C ≠ 0` — 2026-09-12 |
| `+0x2C` | `f32` | `ramp_accel` | `setaccr`'s acceleration × `[01DFE0BC]` (`00269C54`); divides `v²/2a` in `002E45E0`, hence the setter's **exactly `0.0`** collapse of modes 2–4 to 1 (`0026AEBC`) — was `mode_enable` |
| `+0x34` | `f32` | `target_heading` | radians; `0026C17C`, `0026C1BE`, `0026C1ED` |
| `+0x3C` | `f32` | `spin_rate` | movement mode 1's per-frame heading increment (`002E60C0` ← `setvelrotangzx`; read `002E4BF0`) — 2026-09-12 |
| `+0x50`/`+0x54` | `f32` ×2 | `heading_approach_step` / `pitch_approach_step` | the per-frame caps on the desired heading `ctx+0xA4` / pitch `ctx+0xA0` approaching the target bearing (`002E46FA`, `002E471D`; setter `Movement_SetDesiredHeadingTurnLimit` `002E5B60`) — 2026-09-12 |
| `+0x58` | `f32` | `turn_step` | `0x3E20D97C` = **π/20 = 9°**, written literally at `0026C224`; the per-frame cap of the facing approach in movement modes 2 / 3 and the divisor of mode 4's frame count; floored at 0.5° by the integrator — `DP-1` |
| `+0x5C` | `f32` | `turn_limit` | `0x40490FDB` = **π = 180°**, at `0026C237`; **no reader found** (record census and the inline-slot aliases) — a dead store, `DP-1` |
| `+0x62` | `u8` | `flags` | **bits 0–2** the resume shape; **bit 6** the turn direction |
| `+0x65` | `u8` | `teardown_gate` | non-zero makes mode 0 run the `002EBE50`/`002E8EE0` teardown |
| `+0x68` | `i16` | `turn_frames` | total frames of a mode-4 turn: `(target − heading) / turn_step` (`002690D0`) or `[01DFE0B4] + frames / [01DFE0BC]` (`0026C330`); the setter's mode 4 completes when it is `≤ [01DFE0B4]` — was `frame_countdown` |
| `+0x78` | `f32` | `turn_frame_index` | the elapsed-frame counter mode 4 divides by `+0x68`; seeded with `[01DFE0B4]`, advanced by `0026C300` each frame — 2026-09-12 |
| `+0x7C` | `f32` | `steer_speed_request` | the move verb's speed operand (`0026A640`), re-issued to `Movement_SetRequestedSpeed` every frame by `0025DF00` while `+0x29 ≠ 0`; zeroed by mode 0; **the last field** — was `off_marker` |

### `+0x62` is the busiest byte in the record, and it is a bitfield

**15 functions touch it** — more than any other field, and more than twice the next. Two disjoint
bit-fields are proven:

```
bits 0-2   the resume shape the pop dispatches on     002EAAE7  and ecx, 7
bit 6      the turn direction, 1 = turn negative      0026C19D  and byte [rax+0x62], 0xBF
                                                      0026C1A3  or  byte [rax+0x62], 0x40
```

**Bits 3–5 and 7 are untouched by any site in the census** *(answered: see DW-1's 2026-09-15 census in §8 — bits 3–5 are written by `002EC380` / `002EBE50`, bit 7 by `0026A1A0` / `00263230`; 2026-10-02, OPUS)*. That is an observation about the 57
censused functions, not a claim that nothing uses them.

### 21 of 128 bytes are undeclared — and two declared fields have no per-offset accessor

`+0x30..+0x33`, `+0x40..+0x4F` and `+0x6B` are the undeclared gaps `types_index.py` reports
because the record's **size is declared** — 107 of 128 bytes accounted for, **83.6 %**. The
store reports them rather than rounding the record up to "understood". Two further rows —
`target_z` `+0x08` and `target_w` `+0x0C` — have no access *at their own displacement*: their
only coverage is the 16-byte `movups` at `+0x00`, so the width checker reports them as "census
has no access at that displacement" even though the bytes are written. (`+0x54` left this class
on 2026-09-17, when the one-hop extension added `002E471D`'s read; corrected the same day —
the earlier version of this note had counted both declared-without-access ranges as gaps.)

### The `002E5750` exclusive subtree — all 13 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the facing integrator **13 frontier functions**. Every member
body was disassembled from the shipping image within its declared extent (2026-09-14). Twelve are
one purpose: **the kind-3 accessor layer over this record** — each gates on
`[unit+3] & 0xE0 == 0x60` (kind 3, per
[the mode page](../Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)) and then
reads or writes a field of `[[unit+0xB8]+0xF0]`, the steering slot this page maps. They give
`+0x64` and `+0x66` their first documented accessors: `+0x64` is a byte flag (`00265510` reads,
`0026C070` clears) that mode 3's arm clears once the `+0x78` index passes `+0x66` — the frame cap
`00265530` reads — before the linked-record notify `003DDAD0`.

| cluster | members | role | interior |
|---|---|---|---|
| integrator | `002E5750` (935 B) | the facing integrator — `edx≠0` applies a caller delta directly; `edx==0` dispatches on the ~~steering~~ movement mode (`00265600`) *(corrected 2026-10-02, OPUS: `0026561B`–`0026561F` return `+0x28 & 0x7F`, the movement mode; `+0x29` is the steering mode, §4)*: mode 1 wraps `+spin_rate`, mode 2 eases via `00263CC0`, mode 3 walks the `+0x64`/`+0x66`/`+0x68`/`+0x78` progress fields, mode 4 divides by `turn_frames`, the rest test `002EA780` | `002E57D9` (`call 00265600` — fetch the mode) |
| record probe | `00264750` (19 B), `00265810` (19 B), `002E4BF0` (39 B) | kind-3 fronts tail-jumping the null-guarded getters — `00264750`→`002E4BC0` reads `+0x58` (`turn_step`), `00265810`→`002E4BF0` reads `+0x3C` (`spin_rate`) | `00264754` / `00265814` (`and al,0xE0` gates) / `002E4C0D` (`movss` of `+0x3C`) |
| turn-state reads | `002654E0` (40 B), `002655D0` (38 B) | `+0x28` movement_mode byte < 0 → the in-progress bit §5 describes; `+0x62` bit 6 → the turn direction | `00265501` (`cmovl` on `+0x28`) / `002655EC` (`shr eax,6`) |
| turn-profile reads | `002651C0` (50 B), `002652A0` (34 B), `00265530` (32 B), `00265660` (32 B) | `+0xB8`-record floats `+0x54`/`+0xAC` selected by kind ~~1/2~~ 1/3 *(corrected 2026-10-02, OPUS: `002651C7` `sub edx, 1` / `je` class 1, `002651CC` `cmp edx, 2` / `je` class 3)*; slot `+0x38` float; slot `+0x66` u16; slot `+0x68` (`turn_frames`) i16 | `002651E5` / `002652BC` / `0026554B` / `0026567B` |
| frame-counter pair | `00265510` (32 B), `0026C070` (28 B), `00265630` (33 B), `0026C300` (37 B) | `+0x64` byte read / `+0x64` byte write; `+0x78` (`turn_frame_index`) read-as-int / write-from-int | `00265528` / `0026C088` / `0026564B` / `0026C31F` |

The integrator's own account of modes 2–4 is in
[how a character turns](how-a-character-turns.md) §2 and the mode page §10; this table binds the
helpers those arms call so the record's reader set is complete.

## 6. Modding notes

- **Writing `context +0xDC` directly is the switch.** `0` selects the walking state, `1` the
  interruption's. Anything above 1 is **ignored** and the previous cursor stands — so a bad write
  does not crash, it silently keeps the old record.
- **A push while pushed does nothing.** If you want to interpose, pop first; there is no nesting.
- **The record is inline.** Copying `context+0x120` over `context+0x1A0` copies a whole steering
  state, and nothing allocates or frees, so there is no lifetime to respect.
- **`+0x2C == 0.0` is a kill switch** for steering modes 2–4, tested with an equality compare, and
  it applies to `+0x29` only — `+0x28`'s modes are not gated by it.

## 7. Evidence

| claim | evidence | tier |
|---|---|---|
| the record is `0x80` bytes, inline, two of them | `shl rax,7` + `add rax,0x120` at `00269F9F`–`00269FA9` | 1 |
| the selector is `context+0xDC`, values 0/1 | `movzx eax,[rcx+0xDC]` / `cmp al,1` / `ja` | 1 |
| out-of-range selector changes nothing | the `ja` skips the store at `00269FAC` | 1 |
| push/pop are the only callers | **four instruments**: `E8` 3 sites, `E9` 0, operand 0, each with a positive control | 1 |
| the stack is depth one | `002EABA5 cmp byte [rdi+0xDC], 0 / jne` and `002EAAC5 test al,al / je` | 1 |
| the pop replays three saved dwords | `002EAAF5`/`002EAAFC`/`002EAB00` load `+0x18`/`+0x14`/`+0x10` into `r9d`/`r8d`/`edx` | 1 |
| 32 fields, `+0x00`–`+0x7C` | `record_field_scan.py`, 55 functions, **2 controls reproducing** | 1 |
| `+0x28` and `+0x29` are distinct fields | both setters read the chain themselves; the offsets differ by one byte | 1 |

### The scan's controls, and the defect one of them caught

Both controls are hand-read function bodies: `0026AE90` must yield `+0x29, +0x2C, +0x7C` and
`0026C120` must yield `+0x28, +0x34, +0x58, +0x5C, +0x62, +0x65, +0x68`.

**The second failed on the first run**, missing `+0x58`, `+0x5C` and `+0x65`. The cause was real:
the scan is **linear, not control-flow aware**, and `0026C120` restores `mov rbx, [rsp+0x30]` in
its mode-4 epilogue at `0026C1D2` — which killed register tracking for the mode-2/3 block at
`0026C1E6` that is only reachable with that register still live. An epilogue restore is now treated
as not invalidating, which is the less wrong approximation for a linear pass over MSVC output.

> **The tool refused to report until the control reproduced.** Without it the record would have
> been published with 29 fields and no sign that three were missing.

## 8. What this does not claim

- ~~**What the interruption actually is.** Push and pop are named for what they do to the slot. **No
  caller of either was traced**, so *"a cutscene or a conversation"* in §1 is the shape of the
  mechanism, not an observed trigger.~~ **`DW-2` ANSWERED 2026-09-12 (FABLE) — a script taking the
  actor.** A function-list-independent index of every `E8` / `E9` in `.text` finds the callers the
  four instruments missed. **Push** (`002EAB80`) is called once, at `00263408` in `00263230`, the
  mode-1 path of `ActorResource_StartEntryScriptExecution` (`003DBDC0` → `003DBE78`): with the actor
  record (`02098E10 + idx·0x288`) it increments the record's running-script count `+0x1E0`
  (`002633C6`), folds the global flags at `02098E20` / `020990A8` / `02099330` into `02099DB4`, and
  pushes the steering state of the record it was given (`002633FF`–`00263408`). **Pop** (`002EAAA0`)
  is called twice, both in `00263050`, the per-record op handler that `ActorResource_RemoveActiveEntry`
  (`003DB2A0` → `003DB392`) drives: **~~op 2~~ op 4** pops *(corrected 2026-10-02, OPUS: `00263059` `sub edx, 1` (op 1), `0026305E` `sub edx, 2` (op 3), `00263063` `cmp edx, 1` / `jne 0026321C` leaves op 2 without a pop; op 4 tests `+0xB` bit 4 at `0026306C`)* when the record's "pushed" bit (`+0xB` bit 4) is set
  and clears it (`0026306C`–`0026307B`); **op 1** decrements `+0x1E0` (`002630B7`) and, when the
  record's slot word `[rcx + rbx + 0x24]` is negative, pops (`0026320A`–`0026320D`), otherwise sets
  the pushed bit (`002631F6`); op 3 tail-jumps to `0025B500`. So the interruption is **an event
  script starting on the actor** (the actor-resource entry beginning script execution) and the
  resume is **that entry's removal** — a cutscene, a conversation or any scripted control, exactly
  the shape §1 named, now with the mechanism's two ends observed. Which script kinds run through
  `ActorResource_StartEntryScriptExecution` mode 1 is the residue.
- **What `FUN_002627C0`, `FUN_002EC2C0`, `FUN_002EBFA0`, `FUN_002EC3F0` or `FUN_002E8EE0` do.**
  Named as the push/pop chain, ~~unread~~ *(answered: see [the facing-and-steering contract](../CONTRACT-facing-and-steering.md) §14 item 2 and §18 — all five read 2026-09-18; 2026-10-02, OPUS)*.
  *One of the five read, 2026-09-19 (FABLE):* `002EC3F0` is where this record's shape reaches the **head**. It takes the
  shape from bits 0-2 of `+0x62` and a selector from bits 3-5 and stages one of six head-look requests with the frame
  count at `+0x60` and, for shapes 2 and 3, the pair at `+0x10` / `+0x14`. So the statement below that an interrupted
  look-at is not resumed by the pop is about the **body turn**; the head look is re-staged from the same record by this
  function on the bind and resume chain. The request word and the six services are on
  [the staged look command](../../17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md).
- **What resume shapes 2–7 mean.** `flags & 7` has three arms in the switch and only 0 and 1 lead
  anywhere. **Narrowed 2026-09-12 (FABLE): shapes 2 and 3 are set** — `002EC140` stores
  `(flags & 0xFA) | 2` with the raw pair `(+0x10, +0x14)` and `002EC1C0` stores `(flags & 0xFB) | 3`
  with the same pair wrapped, and both then write the wrapped pair to `+0x70` / `+0x74`
  (`0026A8E0` / `0026A870`). Their callers are the **look-at verbs** (`rlookatr_4bb` / `_4bc`,
  `rlookatrt` / `lookatrt`, `rlookatrt_4c7` → shape 2; `lookatt` / `rlookatt` / `rlookatwt` /
  `lookatwt`, `rlookat_27b`, `rlookatw_4c2`, `rlookatwt_4cb` → shape 3; `002EC510` reaches both), so
  **an interrupted look-at is not resumed by the pop** — its shape falls into the default arm. No
  writer of a value 4–7 was found among the sites read. `DW-1`.
  **Answered 2026-09-15 (FABLE): 4–7 are never written, so the shape takes only the values 0–3.** This is a census of
  every write to displacement `0x62` in `.text` (`work/FABLE/drift4/dw1_shape_writers.py`): byte stores with the
  `and` / `or` constants before them, plus direct `and` / `or` / `xor` on memory.
  - **Bits 0–2 (the shape)** have four writers, every one reaching the record as `[[actor + 0xB8] + 0xF0]`:
    - `002EC2C0` clears to 0 (`and 0xF8`, `002EC308`);
    - `002EBFA0` sets 1 (`002EC058`);
    - `002EC140` sets 2 (`002EC18A`);
    - `002EC1C0` sets 3 (`002EC294`).
  - **The byte's other bits are separate fields, not wider shapes:**
    - bits 3–5 are a three-bit field. `002EC380` inserts its argument there (`xor` / `and 0x38` / `xor`, `002EC39B`–`002EC3A1`)
      and `002EBE50` sets it to 2 (`and 0xD7` / `or 0x10`, `002EBF51`–`002EBF55`);
    - bit 6 is `0026C120`'s;
    - bit 7 is set by `0026A1A0` and `00263230`.
    None of these touches bits 0–2.
  - **The 16 other byte stores at `+0x62`** (script, resource and renderer code) write other structures. None loads the
    `+0xB8` / `+0xF0` route except `00645520`, whose store is inside a vtable object's constructor (`00D62800`).
  - So the `& 7` mask covers values the program never produces. Shapes 0 and 1 are resumed, shapes 2 and 3 (look-at) are
    not, and 4–7 do not occur. **Bound:** a register-rebased base that avoids the `+0xF0` load would not show.
- **That 32 is all the fields.** It is what **this chain** reaches. A record passed to a callee as
  an argument is invisible to the scan, so 32 is a **floor**, and the 33 unaccounted bytes are
  where the rest would be.
- ~~**That the two mode bytes mean different things.**~~ Both governed behaviours are now read
  (§4, 2026-09-12): `+0x28` the facing, `+0x29` the speed ramp.
- ~~**Anything about how the turn is actually integrated.**~~ `DP-1` answered 2026-09-12: the
  integrator is `002E5750`, on [the movement-mode page](../Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md) §10.

## 9. Related

- [How a character turns](how-a-character-turns.md) — the two facing setters and the angle wrap
- [Setting the movement mode](../Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md) — `+0x28`'s five modes
- [The record behind every actor](../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md) — `actor +0x03` and `+0xB8`

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py --addr 00269F90 --addr 002EAB80` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

`00269F90` is **36 B** and `002EAB80` **99 B**, and §2's quotation of the selector is **instruction
for instruction** what the image holds — the `ja` that returns without touching `+0xF0`, the
`shl rax, 7`, the `add rax, 0x120`, the `mov qword ptr [rcx + 0xf0], rax`. **`shl rax, 7` is the
size**, as §2 says, and the fail-open bound is the `ja` skipping the store.

### §3's negative, re-run — and its own control caught my instrument

§3 claims **three `E8` sites, no `E9`, no address-taken reference**, and names three controls. Run
over every function body in the image:

| instrument | on `00269F90` | on §3's control | verdict |
|---|--:|---|---|
| direct `call` | **3** | `001DE4F0` → **1** | control positive |
| direct `jmp` | **0** | `001D1660` → **1** | control positive |
| rip-relative operand | **0** | `02ADD0A8` → **3** | control positive — *after a fix, below* |
| the address as a raw qword *(added here)* | **0** | — | a fourth route, so not in any dispatch table either |

**All three of §3's figures reproduce**, and the fourth instrument adds that the selector's address
appears nowhere as a raw qword, so it is not reachable through a table.

> **The operand control did its job on me.** My first instrument counted only `lea` and returned
> **zero on the control** — which, taken at face value, would have let me report the selector's zero
> as evidence from a broken check. `02ADD0A8` is reached by **`mov`**, not `lea`; widening the
> instrument to any rip-relative operand made the control return **3** and the selector's **0**
> meaningful. **A zero from an uncontrolled instrument is not a finding**, and this is the control
> earning its place rather than decorating the claim.

**Not claimed:** the push and pop bodies (`002EAB80` and its partner), the depth-one refusal, the
`(kind << 5) | sequence` gate at actor `+0x03` and the `+0x18` refusal were **not** re-read — this
pass took the selector and §3's reachability claim. Nothing was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **CoreRuntimeScheduling — CLIENT.** `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) does three
  things here:
  - it asks the per-frame gate body `001EDE80`
    ([the per-frame update gate](../../00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md));
  - it asks the half-rate-mode test;
  - it resolves tables through `ImageAddress_ResolveRuntimePointer`, as `00263050` also does.

  So part of `0025DF00`'s work is gated by the per-frame gate and the half-rate test. Which parts of the
  steering-slot update fall under those gates is not read.
- **Presentation — SERVICE.** `0025DF00` calls three Presentation-filed helpers of 42–84 bytes.
- **Input — CLIENT.** `00263230` calls the 1,936-byte Input-filed body that is still unread.
- **Audio and Presentation, through the console — CLIENT.** `001D1660`, the 13,753-byte developer console body, calls:
  - the console's audio legs (a 9-byte and a 46-byte Audio-filed helper);
  - three Presentation-filed console bodies of 257–446 bytes, one of which also calls `001DE4F0`.

  Those are the console machinery described in
  [what the console tunes](../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md). They are
  not part of steering.
- **ActorEntity - CLIENT and SERVICE (54 edges).** `0025B500` is also called by bodies filed to ActorEntity: `0025C830`, `00263050`; `0025DF00` reaches bodies filed to ActorEntity: `00359B80`, `003DB2A0` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (3 edges).** `00263050`, `00263230`, `002E45E0` reach bodies filed to party: `003590D0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (1 edge).** `001D1660` reaches bodies filed to resource: `002EEEE0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (114 edges).** `0025B500` is also called by bodies filed to script VM / native bridge: `0025E4C0`; `0025DF00` reaches bodies filed to script VM / native bridge: `0025E4C0`, `00267420`, `002674B0` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (1 edge).** `00263230` reaches bodies filed to WorldAreaField (world area): `00377700` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — CLIENT.** `FUN_003fa790`, owned by that layer, calls `001EDE80` on this page. That caller is a 143-byte pass over the sub-object at `[+0x2490]`, reading its `[+0x278]` list and clearing `word[+0x272]` when `dword[+0x260]` is zero; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
