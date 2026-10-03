---
contract: Facing and steering — wrap a heading, dispatch on the actor kind, set a mode, push and pop a steering slot
category: 06-Movement-And-Navigation
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: Facing-And-Steering/how-a-character-turns.md
entries: [0026B5A0, 0026B620, 0026B6A0, 0026C090, 0026AE90, 0026C120, 00269F90, 002EAB80, 002EAAA0, 003A1C50]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 52 addresses cited - 6 data, 24 entry, 22 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-facing-and-steering-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — facing and steering

> **The fifth behavioural contract.** It formalises
> [how a character turns](Facing-And-Steering/how-a-character-turns.md),
> [setting the movement mode](Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md)
> and [the two steering slots](Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md),
> and **corrects one claim in the first of them** (§10).
>
> **Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`** — §13 carries no LIVE observation.

## 1. Purpose

Points a character somewhere and gets them turning. Three layers: **wrap** a requested heading into
a canonical range, **dispatch** on what kind of body it is, and **run** a turn over the following
frames from a record that also survives being interrupted.

## 2. Interface

| operation | entry | signature | returns |
|---|---|---|---|
| set facing, variant 0 | `0026B5A0` (117 B) | `(Actor* rcx, float heading xmm1)` | — |
| set facing, variant 1 | `0026B620` (120 B) | `(Actor* rcx, float heading xmm1)` | — |
| apply a wrapped heading | `0026B6A0` (120 B) | `(Actor* rcx, float heading xmm1, int flag r8d)` | — |
| the facing tail target | `0026C090` (129 B) | `(Actor* rcx, float heading xmm1)` | — |
| set the steering mode | `0026AE90` (127 B) | `(Actor* rcx, int mode edx)` | — |
| set the movement mode | `0026C120` (354 B) | `(Actor* rcx, int mode edx)` | — |
| select a steering slot | `00269F90` (36 B) | `(Context* rcx)` | — |
| push a steering slot | `002EAB80` (99 B) | `(Actor* rcx)` | — |
| pop a steering slot | `002EAAA0` (145 B) | `(Actor* rcx)` | — |
| normalise an angle (loop) | `003A1C50` | `(float xmm0)` | `xmm0` in **`[−π, π]`** — closed at **both** ends, corrected 2026-09-08 from the 61-byte body |

> ### `003A1C50` returns `[−π, π]`, not `(−π, π]` — corrected 2026-09-08
>
> The whole body, and the four constants read out of the image:
>
> ```text
> 003A1C50  movss xmm1, [00915620]   ; -pi   C0490FDB
> 003A1C58  comiss xmm1, xmm0 / jbe  ; skip when -pi <= x
> 003A1C65  addss xmm0, [01CEBC78]   ; +2pi  40C90FDB   -- loop while -pi > x
> 003A1C6E  movss xmm1, [01CEBC50]   ; +pi   40490FDB
> 003A1C76  comiss xmm0, xmm1 / jbe  ; skip when x <= pi
> 003A1C83  addss xmm0, [00915624]   ; -2pi  C0C90FDB   -- loop while x > pi
> 003A1C8C  ret
> ```
>
> The first loop exits when **`−π ≤ x`** and the second when **`x ≤ π`**, so both endpoints are
> attainable: an input of exactly `−π` skips both loops and is returned unchanged. The half-open
> `(−π, π]` written here excluded a value the function can return.
>
> **This applies to `003A1C50` only.** `0033CB70` and `0026A0D0` reach the same idea by different
> idioms — a truncating `fmod` and a sign-dependent `π` — and their ranges were not re-derived here.

> ### `flag` on `0026B6A0` is dead **only on kinds ≠ 3** — on kind 3 it is the commit gate
>
> Normalising both variants — RIP targets resolved, internal branch targets ignored — leaves **29
> instructions each, differing in exactly one**:
>
> ```
>   Variant0 0026B5A0        Variant1 0026B620
> - xor  r8d, r8d          + mov  r8d, 0x1
> ```
>
> **`0026B6A0`'s own 120 bytes never touch `r8`** — the operand analysis that established this is
> right — **but the claim that the flag is never read was wrong**: the kind-3 arm tail-jumps
> `002E5FB0` with `r8d` still live, `002E5FB0` moves it to `r9d`, and `002E5E10` keeps it in
> `r14d` until `test r14d, r14d` / `setne bpl` at `002E5F42`–`002E5F4B` writes it as the stack
> argument to `003EC260`. There `cmp dword [rsp+0x50], ecx` at `003EC362` gates the commit
> block: flag **0** stages the new ~~`{rate, heading, 0}`~~ `{pitch, heading, 0}` triple *(corrected 2026-10-02, OPUS: lane 0 is context `+0xAC`, the pitch — `002E5FBA` loads it, `002E5F4F` passes it, `003EC348` stores it at `+0x120`, and `00420C00` → `0046D380` turns that lane into the rotation about X)* into the steering slot's
> `+0x120`–`+0x128` ~~and returns~~, after copying the old triple to `+0x250`–`+0x258` when it changed, and returns *(corrected 2026-10-02, OPUS: `003EC316`–`003EC358` run before the flag test at `003EC362`)*; flag **1** additionally shifts the triple into `+0x250`–`+0x258`
> and calls `004288B0(slot, -1)` (slot bit `0x20000` clear) ~~or~~ **and then**, when `[slot+0x288]` is set,
> `003B3CA0([slot+0x288], 0x1E)` (`003EC39E` → `003EC3A3` → `003EC3BC`).
>
> **Refinements** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 308, which executed these arms; bytes re-read.)*:
> - **Flag 0 also writes `+0x250`–`+0x258`.** When the triple changed, the **old** triple is copied there before
>   the flag is tested (`003EC31C`–`003EC340`).
> - **A non-idle slot is reset.** A slot whose word `+6` is not `−1`, with `+0x290` bit `0x100000` clear, is reset
>   to `{0, 0, 0}` with `+0x12C = 1.0`, and the flag is ignored.
> - **An unset record counts as absent.** `+0x284 == 0` makes the `cmove` treat the record as absent.
> - **No actor context, no write.** On kind 3 the arm writes nothing when `[actor + 0xC0]` is null (`002E5E5F`).
>
> So the two variants differ exactly where [how a character turns](Facing-And-Steering/how-a-character-turns.md)
> said they did: **`0026B5A0` stages the heading, `0026B620` stages and commits it** — on kind-3
> actors, the only kind whose arm forwards `r8d`. The modding warning about hooking one and not
> the other is correct **for kind 3**; for kind 1 the flag dies in the arm and the variants
> coincide.
>
> **This answers `ED-2` differently than recorded before**: the third argument selects
> **stage-only versus stage-and-commit** in `003EC260`. It is the reason both entry points
> exist — but only kind-3 callers can observe the difference.

## 3. Types

**`SteeringRecord`, `0x80` bytes** — in `_types/`; the census now carries 40 field rows, 33
semantically named (re-measured and extended 2026-09-18; this line previously read "32 fields,
13 named" — FABLE's naming pass split and named most of the remainder, and five more fields are
named below from this contract's own readings). **Not allocated:** two of
them are inline in the movement context, and `+0xF0` is a cursor selecting one.

```
actor   +0x03   u8    packed (kind << 5) | sequence   -- kind = kindTable[sequence].kind (see 4), so kind 3 <=> sequence 5, 6 or 7
actor   +0x0D   u8    bit 4 cleared when steering goes to mode 0
actor   +0x18   u8    == 1 refuses both push and pop
actor   +0xB8   ->    movement context

context +0x38   f32   written by 0026B6A0 on kind 1
context +0x48   f32   written by 0026B6A0 on kind 1, same value
context +0xA8   f32   current heading, radians
context +0xDC   u8    THE SLOT SELECTOR, 0 or 1
context +0xF0   ->    cursor into the two records below
context +0x120  SteeringRecord[0]     0x80
context +0x1A0  SteeringRecord[1]     0x80
```

## 4. Preconditions · postconditions · invariants

**Preconditions.** Everything below `0026B5A0`/`0026B620` requires an actor; the kind gate is
checked by the callee, not the caller. `0026AE90` and `0026C120` return immediately unless
`(actor->packed_03 & 0xE0) == 0x60`, i.e. **kind 3**.

**Kind 3 implies sequence 5, 6 or 7 — by construction, not by census** (added 2026-09-11,
OPUS-REQ-FABLE-SEQKIND). The two bitfields are written together, once, by
`ActorStorage_AllocateAndInitializeRecords` (`002679F0`): the row loop walks the eight-row kind
table at `01E0C328` (`{u8 kind, u8 sub, u16 size}`) with the row index in `r10d` and the row
pointer in `r8` advancing in lockstep (`00267B2A`–`00267B38`), and every record of row *i* gets
`+0x03 = (table[i].kind << 5) | i` (`00267AE1`–`00267B13`) and `table[i].size` bytes (`00267B16`–
`00267B21`). Rows 5, 6 and 7 are the only rows with `kind == 3` (`01E0C328`: kinds
`0, 1, 1, 2, 2, 3, 3, 3`), and the region planter `00266AD0` switches on the same low five bits
(`00266AD3`–`00266AF9`), giving sequences 5–7 the full `0x230`-byte movement context
(`00266B54`–`00266B6F`) — the only sequences whose context reaches `+0xA8`, `+0xDC`, `+0xF0`
and the two `SteeringRecord`s this contract lists. No other writer of the actor's `+0x03` exists
on any route the actor census reaches (89 readers, 0 writers); of the image's 247 byte stores to
some object's `+3`, the two in the allocator are the only ones in the actor family, and
`0026F470` (`0026F5DD`, `0026F83F`) copies the byte whole from a source record. **So the field
list above needs no sequence precondition beyond the kind gate the callees already apply**; a
kind-3 actor with a shorter context cannot be built by the shipping allocator. A reimplementation
that lets the two fields diverge would be the out-of-bounds write OPUS described, and must not.

**Invariants.**

- **A heading is always wrapped before it is stored.** Both facing variants wrap, and `0026C090`
  wraps **again** on the value its caller already wrapped ~~— idempotent, so harmless, and it means
  `0026C090` is safe to call directly~~.
  *Corrected 2026-09-28 (FABLE, Claude Opus 5.5), on ASTRA's facing-wrap-antipode and OPUS's
  FABLE-directed request.* The wrap is **not idempotent** at the exact antipodes.
  - +π maps to −π and back to +π, and −π maps to +π and back: a two-cycle. +0 is a fixed point.
  - This is computed in binary32 from the image's constants `40490FDB` / `C0490FDB` / `40C90FDB`, and the sign branch
    is at `0026C09C`.
  - So the number of wraps on a path decides the stored sign at ±π, although the geometric direction is the same.
    OPUS's qualification (3683ff941) counts the paths: kind 1 wraps three times, and the kind-3 target wraps twice.
  - A wrap can therefore not be removed or added "because it is idempotent".
  - No downstream turn or presentation consequence is claimed, nor native exception behaviour.
  - [Record](../_index/candidates/facing-wrap-antipode-consumer/README.md).
- **The slot selector is 0 or 1 and nothing else.** `00269F90` compares `> 1` and returns without
  touching the cursor — **fail-open**: the previously selected record stays selected.
- **The steering stack is depth one.** Push refuses when the selector is already 1, pop when it is
  already 0.

## 5. State

| | detail |
|---|---|
| **read** | `actor+0x03`, `+0x18`, `+0xB8`; `context+0xA8`, `+0xDC`, `+0xF0`; the record's 32 fields; `01DFE0B4` the `FrameLimit` time base |
| **written** | `actor+0x0D` bit 4; `context+0x38`, `+0x48`, `+0xDC`, `+0xF0`; the record |
| **allocated / freed** | **none** — the records are inline in the context |

## 6. Relationships

```
caller
  -> 0026B5A0 / 0026B620   wrap, then
     -> 0026B6A0(a, wrapped, flag)        kind 1 : context->+0x38 = +0x48 = wrapped
     |                                    kind 3 : 002E5FB0 -> 002E5E10 steering-record write
     |                                             (wraps again; context->+0xA8; three/four   <- corrected 2026-10-02, OPUS - one to four: +0x50 always (002E5EC6), +0x70 / +0x60 only with actor +0x0D bit 5 clear (002E5ECB-002E5EE4), body +0xF0 only when one exists (002E5EF3-002E5F0B)
     |                                              {id,target} sub-records; flag -> 003EC260's
     |                                              commit gate — stage vs stage-and-commit)
     -> tail-jump 0026C090(a, wrapped)    kind 1 : 0026B6A0(a, wrapped, 1)
                                          kind 3 : record->target_heading_34 = wrapped

interruption
  -> 003DBDC0 -> 00263230 (op 1) -> 002EAB80 push : gate +0x18!=1 & kind 3 & depth==0;
     002627C0 clones slot 0 -> slot 1, selector -> 1, 00269F90, SetSteeringMode(0), 0026C120(0)
  -> 003DB2A0 -> 00263050 (op 4, actor+0xB bit 4) -> 002EAAA0 pop : gate +0x18!=1 & kind 3 &
     depth>0; selector -> 0 (slot 0 was never overwritten — it IS the saved pre-push state; true right after the push, but
     pop's always-run tail 002EC3F0 / 002E8EE0 then changes slot 0's +0x6A — 2026-09-25, OPUS block 308),
     00269F90, then replay sub->flags_62 & 7: 0 -> 002EC2C0(actor, sub+0x10) Vec4 write,
     1 -> 002EBFA0(actor, sub+0x10/14/18) re-steer, else nothing; always 002EC3F0 + 002E8EE0;
     caller clears actor+0xB bit 4
```

**The kind dispatch is the shape of the whole subsystem.** `0026B6A0` and `0026C090` each branch on
`actor->packed_03 >> 5` and each handles **kind 1 and kind 3 differently and every other kind not at
all**. Kind 1 gets its heading written straight into two context floats; kind 3 goes through the
steering record.

## 7. State transitions

**Movement mode, `0026C120`, five arms:**

| mode | effect |
|---:|---|
| 0 | if `record->teardown_gate_65` then `002EBE50(body,0,0)` and `002E8EE0(actor)`; then `002E6300(actor, body, prev)` |
| 1 | writes `+0x28` and returns |
| 2, 3 | choose the turn direction; write `turn_step_58 = π/20` and `turn_limit_5C = π` |
| 4 | choose the turn direction; **if `frame_countdown_68 <= FrameLimit base`** — an **unsigned** compare (`movsx` then `ja`, `0026C1AE`–`0026C1B8`), so a negative countdown never completes *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 308, which executed these arms; bytes re-read.)* — set the facing and reset the mode to 0 |
| other | writes `+0x28` and returns |

**Steering mode, `0026AE90`:** modes 2–4 collapse to 1 when `record->mode_enable_2C == 0.0f`
(equality, not a threshold). Mode 0 additionally clears `actor+0x0D` bit 4, calls `002E55C0`, and
zeroes `record->off_marker_7C`.

## 8. Script · resource · event interactions

None directly. `0026C120` mode 4 reads the **`FrameLimit` time base** at `01DFE0B4`, which is
1 or 2 depending on the player's Frame Rate setting — the only authored input to this subsystem, and
it comes from `GameSetting.ini`.

## 9. Determinism

**RNG:** none. **Timing:** mode 4 is frame-rate sensitive by construction (§7). **Threading:** no
synchronisation primitive appears in any of the ten entries; single-threaded access is **not
proven**.

## 10. Failure paths and edge conditions

- **A non-steerable actor is a silent no-op.** `0026AE90`, `0026C120`, push and pop all return
  without effect when `(packed_03 & 0xE0) != 0x60`. No error, no partial effect.
- **`0026B6A0` and `0026C090` are no-ops for every kind except 1 and 3**, likewise silently.
- **A slot selector above 1 leaves the old cursor standing** — fail-open (§4).
- **A second push while pushed does nothing**, and a pop with nothing pushed does nothing.
- **A resume shape above 1 resumes nothing.** `flags_62 & 7` has arms for 0 and 1 only.
- **The wrap is a truncating `fmod`, and it is not the same normaliser as `003A1C50`.** Both exist
  in this subsystem:

```c
/* the facing wrap — 0026B5A0, 0026B620, 0026B6A0, 0026C090 — single pass, no loop */
float bias = (h >= 0.0f) ? +3.14159274f : -3.14159274f;   /* 01CEBC50 / 00915620 */
float t    = h + bias;
t -= truncf(t / 6.28318548f) * 6.28318548f;               /* 01CEBC78 */
return t - bias;

/* the steering normaliser — 003A1C50, used by 0026C120 — a loop */
while (x < -3.14159274f) x += 6.28318548f;
while (x >  3.14159274f) x -= 6.28318548f;
```

> **Two angle normalisers, same constants, different arithmetic.** The loop form is exact for any
> input; the `fmod` form does one pass and inherits `float` rounding at large magnitudes.
>
> ### `DY-1` ANSWERED 2026-09-08: they disagree on 88.8 % of a 4,130-input sweep
>
> Both forms were run **as shipped** under emulation over 4,140 distinct float bit patterns.
> Of the 4,130 where both terminate, **3,668 disagree**. The disagreements are structural,
> not marginal:
>
> ```
> in   -0.0        loop  -0.0          fmod  +0.0        the sign of zero
> in    1.0        loop   1.0          fmod   1.0000002  ALREADY IN RANGE, still perturbed
> in   +pi         loop  +pi           fmod  -pi         opposite sign at the boundary
> in    2pi        loop   0.0          fmod  -2.384e-07
> ```
>
> **The `fmod` form is not the identity on its own output range.** It adds `±pi`, takes a
> truncating `fmod`, and subtracts `±pi` again; that round trip costs a couple of ulp even
> for a value that needed no wrapping at all. The loop form leaves an in-range value exactly
> alone, because its two `while` conditions are simply false.
>
> **And the loop form does not always terminate.** Once `ulp(x) > 2 × 2pi` — that is
> `|x| >= 2**27`, about `1.34e8` — adding `2pi` is absorbed and the loop cannot make
> progress. **6 of the 4,140 inputs are in that state, verified by `x + 2pi == x` rather than
> assumed**, and they include both infinities. A NaN is safe: `comiss` is unordered, both
> `jbe`s are taken, and it falls straight through.
>
> **For a reimplementation:** these are two different functions and the call site decides
> which. Substituting one for the other changes the stored heading on almost nine inputs in
> ten. [`diff_angle_wrap.py`](../../../Reconstruction/Tests/Differential/diff_angle_wrap.py).

## 11. Observable behaviour

- A character turns **the short way round**, because the difference to the target is wrapped before
  its sign is taken.
- The turn is **9 degrees per step ~~with a half-turn ceiling~~** (`π/20`~~, `π`~~) *(corrected 2026-10-02, OPUS: `+0x5C` = `π` is never read — `002E5750` reads only `+0x58`, through `00264750` → `002E4BC0` (`002E4BDD`), and `002690D0` divides by `+0x58` at `00269345`; DP-1, §14)*.
- **Mode 4 ends a frame earlier at one Frame Rate setting than the other** (§7).
- A character interrupted mid-walk **resumes it**, because the walk's steering state was pushed
  aside rather than overwritten.

## 12. Reproduction formula

```c
/* wrap (facing path) */   bias = h >= 0 ? PI : -PI;
                           t = h + bias; t -= truncf(t / TWO_PI) * TWO_PI; t -= bias;
/* actor kind */           kind = actor->packed_03 >> 5;      /* gate: (p & 0xE0) == 0x60 */
/* slot address */         rec  = (char*)ctx + 0x120 + (ctx->sel_DC << 7);   /* sel <= 1 */
/* turn direction */       neg  = wrap(rec->target_34 - ctx->heading_A8) < 0;
                           neg ? (rec->flags_62 |= 0x40) : (rec->flags_62 &= 0xBF);
/* turn rate, modes 2/3 */ rec->turn_step_58 = 0x3E20D97C;    /* pi/20 = 9 degrees */
                           rec->turn_limit_5C = 0x40490FDB;   /* pi    = 180 degrees */
/* mode 4 completion */    if (rec->frame_countdown_68 <= *(int32*)0x01DFE0B4) { setFacing; mode = 0; }
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent, and this is the gate the
subsystem fails.**

**RECLASSIFIED 2026-09-12 (`OPUS-S13-CLASSIFY-THREE`).** This section read *"None. Empty
deliberately"*, and that was true of the **live** half only. The angle-wrap operation has been
executed against the shipped bytes for some time — `check_gate26` was scoring the contract
`nothing executed` while a passing harness sat beside it, because this section described the gap and
not the evidence.

**Instrument:** [`diff_angle_wrap.py`](../../../Reconstruction/Tests/Differential/diff_angle_wrap.py)
against [`angle_wrap.c`](../../../Reconstruction/Game/Math/angle_wrap.c).
**Re-run 2026-09-12: 8280 comparisons, 0 mismatches** against the shipped bytes.

**Nothing about the live gap changes**, and the three cheap confirmations below are still the ones
worth asking for. An isolated run says the arithmetic matches; it says nothing about what the fields
hold in a running game.

### The mutation campaign, and the two survivors it took an exhaustion to settle

**Re-run 2026-09-12 under the corrected generator** (`OPUS-CONTRA-MUTATION-LIT-SUFFIX`). The pattern
that generates literal mutations could not see a literal carrying a `u`, `U`, `l`, `L` or `f` suffix
until that day, so **this pilot's earlier campaign measured 5 mutation points where the file has 9**
— the three `f`-suffixed angle constants in `angle_wrap.h` were invisible, and so was the second
literal of `0.0f`. Every count published before that date is a floor, here and in every other
pre-fix pilot.

**9 generated points: 4 KILLED, 3 provably EQUIVALENT, 2 SURVIVED.** Verdict `FAIL`, which is what
the instrument returns whenever a survivor exists, and it is fully explained below rather than
argued away.

The table for every pilot, and the four kinds a survivor can be, are on
[`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**The three EQUIVALENT are the newly visible constants**, and they are a fact about the header rather
than a gap: `3.14159274101257324f` mutated to `…325f` compiles to the **same** float32, so no test
could ever kill them. That is proven by the `/Brepro` hash, not judged.

**Both survivors mutate one line** — `float bias = (x >= 0.0f) ? ANGLE_PI : ANGLE_NEG_PI;` — and
neither could be adjudicated by reading. Each was settled by **exhausting the complete set of inputs
on which the mutant takes the other branch**, compiled with this pilot's own compiler and flags so
the float semantics are the mutant executable's rather than a model of them:

| mutant | inputs where the branch differs | distinguishing | verdict |
|---|---|---:|---|
| `>=` → `>` | `{+0.0, -0.0}` | **0 of 2** | **EQUIVALENT**, both give `00000000` |
| `0.0f` → `0.1f` | every float32 in `[+0.0, 0.1)` | **0** | **EQUIVALENT** — every distinguishing input in `[+0.0, 1.0)` is at or above `4 − π`, and none is below `0.1` |
| `0.0f` → `1.0f` | every float32 in `[+0.0, 1.0)` | **890,824 of 1,065,353,216** | killable, and **KILLED** — by the sweep that was already there |

**So the campaign's two survivors are both equivalent, and no case set could kill either.** The
instrument's own rule is that identical machine code proves equivalence and different code proves
nothing; these differ in code, so it could not settle them, and exhausting a bounded differing domain
is what does.

### The binade crossing, which the exhaustion found on the way

`Angle_WrapFmod` adds `bias`, truncates a quotient, subtracts `q × 2π` and subtracts `bias` again.
For `|x| < π` the quotient is zero and the whole operation is a **round trip** — which is why the
algebra says the bias choice cannot matter there.

**It does matter, because the round trip is exact only while `x + bias` stays inside one binade.** At
**`x = 4 − π`** the sum crosses `4.0`, the ulp doubles, `(x + π) − π` comes back **one ulp low**, and
`(x − π) + π` does not. Above `4 − π` the branch that chose the bias is **observable in the result**;
below it, it is not. The first distinguishing input is `x = 0.858407438` → `0.858407259` against
`0.858407497`, and 890,824 of the floats in `[+0.0, 1.0)` behave that way — **every one of them at or
above the crossing.**

The harness now drives that family directly: the crossing at `4 − π` and its ulp neighbours, a
64-point spread across `[4 − π, 1)`, the negative mirror, and the same crossing one binade up at
`8 − 2π`. **8,448 comparisons, 0 mismatches against the shipped bytes** (8,280 before), so this is a
statement about the original as well as the reconstruction: **the shipped inline wrap loses the same
ulp at the same crossing.**

> **⚠ The family was added on a prediction that was wrong, and it is kept for a different reason.**
> I expected it to kill a survivor. It killed nothing: the counts are 4/3/2 before and after, index
> for index, in both `campaign.json` receipts. The mutant I aimed at — `(x >= 1.0f)` — was **already**
> killed by the existing `-4π…4π` sweep, which lands on roughly twenty inputs above the crossing; the
> survivor on that line is the *other* literal, `0.1f`, whose domain lies entirely below it. What the
> family actually buys is **direct, named coverage of the crossing** instead of incidental coverage
> nobody had noticed, and the mechanism written down. **A mutation score that did not move is the
> honest result, and the prediction is recorded because it was wrong.**

## 14. Unresolved

1. ~~**What `002E5FB0` does** — the kind-3 arm of `0026B6A0`, unread. The single largest gap
   here.~~ **Read 2026-09-18** — a thunk into `002E5E10`, the steering-record write; §2's flag
   callout and §15 carry the detail.
2. ~~What `002EBE50`, `002E8EE0`, `002E6300`, `002E55C0`, `002627C0`, `002EC2C0`, `002EBFA0`
   do~~ **All read.** `002E8EE0` by EC7 (interior citation below), `002E55C0` by `ED-5`,
   the rest 2026-09-18: `002E6300` is a 10-byte flag gate (`test r8b; js → 00265510`, the
   `sub[+0x64]` byte getter — head of the eight-leaf accessor cluster `00265510`–`0026567F`);
   `002627C0` copies the `0x80` steering record from slot `[+0xDC]` to `[+0xDC+1]` — the
   push half of the depth-one stack; `002EC2C0` stores an input `Vec4` into the `+0xF0`
   sub-record `+0x10`, clears `+0x62` bits 0–2, and runs a position→heading apply chain
   (`0026A8E0`) plus two zeroed channels; `002EBE50` is the mode initiator (snapshot
   `+0x70`/`+0x74` into `+0xB4`/`+0x224`, wrap deltas via `003A1C50`, frame count from
   rate `+0x6C` → `word[+0x60]`, mode byte into `+0x63`, then `002EC3F0` + `002E8EE0`);
   `002EBFA0` steers toward a resolved target body (target triple+id into `+0x10`–`+0x1C`,
   heading from both world positions via `00265020`×2 + `003A19A0`). `002EC3F0` is read
   (§18): the mode-pair dispatched steering-parameter writer into the render record's
   `+0x580` sub-record.
3. ~~What actually pushes and pops. `DW-2`.~~ **Caller side closed 2026-09-18** — §6's
   interruption diagram carries the full chain: `003DBDC0`→`00263230`(op 1) pushes,
   `003DB2A0`→`00263050`(op 4, gated on `actor+0xB` bit 4, cleared after) pops.
4. ~~What resume shapes 2–7 mean. `DW-1`.~~ **ANSWERED 2026-09-15 (FABLE), corroborated
   byte-for-byte 2026-09-18** — the shape is 0–3, never 4–7: `002EC2C0` stamps 0,
   `002EBFA0` stamps 1, `002EC140` stamps 2 (`&0xFA|2`, raw `{xmm1,xmm2}` pair into
   `sub+0x10`/`+0x14`), `002EC1C0` stamps 3 (`&0xFB|3`, the same pair two-sided-wrapped).
   The pop replays 0 and 1 only; the look-at pair (2, 3) is not resumed — an interrupted
   look-at is abandoned, which is consistent: look-at is per-frame reissued anyway.
5. ~~**Why two facing entry points exist**, given that the only difference between them is an
   argument the callee ignores.~~ **Narrowed 2026-09-18**: the flag is *not* ignored on kind 3 —
   `0026B5A0` stages, `0026B620` stages and commits (§2's corrected callout). What remains open
   is why two entry points exist **for kind-1 callers**, where the flag still dies in the arm.
6. ~~Whether the two normalisers can disagree. `DY-1`.~~ **ANSWERED 2026-09-08** — yes, on
   88.8 % of a 4,130-input sweep (`diff_angle_wrap.py`); the truncating-`fmod` form and the
   `003A1C50` loop form are different functions and the call site decides which.
7. ~~What `turn_step_58` and `turn_limit_5C` are consumed as. `DP-1`.~~ **ANSWERED
   2026-09-12 (FABLE)** — `+0x58` (π/20) is the per-frame cap in movement modes 2/3 and the
   divisor for mode 4's frame count; `+0x5C` (π) is read by nothing — a dead store.
8. ~~19 of the record's 32 fields, and 33 of its 128 bytes with no accessor at all.~~
   **Narrowed 2026-09-18 (re-measurement):** the census now lists 40 field rows; the residual is
   5 placeholder-named fields (`steerParamByte64`, `steerParamWord66`,
   three ctor-zeroed dwords) and **9 bytes** in two
   never-observed spans
   (`+0x44`–`+0x4B`, `+0x6B`), plus 12 ctor-zeroed bytes with no censused reader — 21 bytes total,
   down from 33. Eight more fields were named from this contract's own readings the same day:
   `+0x1C` is `resume_target_handle` — `002EBFA0` stores the `003589B0`
   (`ActorHandle_EncodeRegistryEntry`) return there beside the `resume_a/b/c` replay params;
   `+0x60` is `derived_turn_frames`, `cvttss2si(wrappedΔ / +0x6C)`, the initiator path's
   counterpart to mode-4's `turn_frames`; `+0x38` is `turn_start_heading` — the mode-4
   integrator interpolates `+0x38 + wrap(target_heading − +0x38) × (frame_index / turn_frames)`;
   and `+0x70`/`+0x74` are the two steer channels' wrapped targets — `steer_target_heading` /
   `steer_target_pitch` — which the initiator `002EBE50` deltas against the context mirrors
   `+0xB4`/`+0x224` before snapshotting them across; `+0x63` is `steer_arm_state` — the
   initiator stores its `edx` op there and the teardown paths zero it alongside the context
   mirrors; `+0x6C` is `initiator_turn_step` — `0026AAD0` stores `wrap(arg) ×` the rate global
   `[01DFE0BC]` and `002EBE50` divides the wrapped delta by it for `derived_turn_frames`;
   `+0x6A` is `steer_dispatch_flags` — bit 0 is a one-shot latch the dispatcher `002EC3F0`
   consumes: when set with dispatch mode 2, the run remaps to mode 1 and the bit clears.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the record is `0x80`, inline, two of them | `shl rax,7` + `add rax,0x120` at `00269F9F`–`00269FA9` | 1 | PROVEN |
| the wrap and its three constants | resolved by tool: `01CEBC50` = +π, `00915620` = −π, `01CEBC78` = 2π | 1 | PROVEN |
| the bias cancels exactly only while x + bias stays in its binade | the round trip `(x + bias) − bias` is exact below `4 − π` and loses one ulp above it, where `x + bias` crosses `4.0` into the next binade. Executed — the crossing, its ulp neighbours, a spread across `[4 − π, 1)`, the negative mirror and the `8 − 2π` crossing all run against the shipped bytes, 0 mismatches. Found by a mutation the old case set could not kill, and its differing domain then exhausted: 890,824 of the 1,065,353,216 floats in `[+0.0, 1.0)` distinguish the bias choice, every one of them at or above `4 − π` | 1 | PROVEN |
| the two facing variants are identical **for kind ≠ 3** | 29 instructions each, one differs; the differing register is never read **by the callee's own bytes** — the pair `0026B5A0`/`0026B620`. **Both halves are now re-checked mechanically on every harness run** — normalised instruction diff, and `regs_access` including implicit touches with a positive control on `rcx`. **Qualified 2026-09-18**: on kind 3 the flag leaves the body live through the tail-jump and gates `003EC260`'s commit — the variants differ there | 1 | PROVEN |
| `0026B6A0` never touches `r8` — but its kind-3 arm forwards it live | operand analysis over all 120 bytes stays true of the body; the tail-jump at `0026B701` passes `r8d` to `002E5FB0`, which moves it `r8d`→`r9d` (`002E5FB7`) into `002E5E10`'s `r14d` | 1 (static) | PROVEN |
| kind dispatch in `0026B6A0` and `0026C090` | `movzx ecx,[rcx+3]` / `shr ecx,5` / `sub ecx,1` / `cmp ecx,2` in both. **All three arms of `0026C090` run per case since 2026-09-08**, and they are behaviourally distinct: **kind 1 tail-jumps to `0026B6A0`** carrying the `r8` it never reads, **kind 2 does nothing at all**, and **only kind 3 writes the record** at `[[actor+0xB8]+0xF0]+0x34` | 1 | PROVEN |
| push/pop are the only slot callers | four instruments, each with a positive control | 1 (static) | PROVEN |
| mode 4 reads the `FrameLimit` base | `movsx eax,[rcx+0x68]` / `cmp eax,[01DFE0B4]` | 1 | PROVEN |
| `002E5FB0` is a 12-byte thunk into `002E5E10`: `context = actor[+0xB8]`, `xmm2 = context[+0xAC]` (~~the prior rate~~ the pitch, handed back unchanged *(corrected 2026-10-02, OPUS: `002E5E88` stores it back to `+0xAC`, `003EC348` puts it in render lane `+0x120`, which `0046D380` rotates about X)*), `r9d = flag` | `002E5FB0`–`002E5FC2` in full | 1 (static) | PROVEN |
| `002E5E10` is the kind-3 steering-record write: re-wraps the heading (third wrap site), stores `context[+0xA8]` and `{id,target}` fields `+0x50`/`+0x60`/`+0x70` via `003DA850` (a `[rcx+8]` leaf) — `+0x60`/`+0x70` only when `actor+0x0D` bit 5 clear — plus `record[+0x138]+0xF0` when that object exists, and finally ~~`003EC260(word[record], prior_rate, heading, 0, flag!=0)`~~ `003EC260(word[record], pitch, heading, 0, flag!=0)` *(corrected 2026-10-02, OPUS: `002E5F4F` `movaps xmm1, xmm8`, the `+0xAC` pitch)* | `002E5E44`–`002E5F57` whole body; `record = actor[+0xC0]` null-bails everything at `002E5E5F`; `dword[record]==-1` skips the `003EC260` call at `002E5F3D` | 1 (static) | PROVEN |
| the flag is `003EC260`'s commit gate: 0 stages the ~~`{rate, heading, 0}`~~ `{pitch, heading, 0}` triple into slot `+0x120`–`+0x128`, copying the old triple to `+0x250`–`+0x258` when it changed; 1 additionally shifts it to `+0x250`–`+0x258` and calls `004288B0(slot,-1)` (unless `+0x284` bit 17 is set) ~~or~~ and then `003B3CA0([slot+0x288],0x1E)` when `+0x288 != -1` *(corrected 2026-10-02, OPUS: `003EC316`–`003EC358` before the flag test; `003EC368`–`003EC39E`, then `003EC3A3`–`003EC3BC`)* | `003EC362 cmp dword [rsp+0x50],ecx` / `je` skips the whole commit block; slot table `022C6F28 + id*0x740` at `003EC27C`–`003EC283`; `[rbx+0x290]&0x100000` skips the rate compare at `003EC29D` | 1 (static) | PROVEN |
| `002E6300` is a 10-byte flag gate — `test r8b,r8b` / `js → 00265510` / `ret` | whole body; bit 7 of the flag tail-jumps into `00265510`, the `sub[+0x64]` byte getter (below) | 1 (static) | PROVEN |
| `00265510`–`0026567F` is an eight-leaf kind-3 accessor cluster — each gated `(+3 & 0xE0)==0x60` (else 0): `sub[+0x64]` byte, `sub[+0x66]` word, `slot[+0xDC]` record `+0x34` float, slot-`edx` (clamped) record `+0x34`, `sub[+0x62]>>6 &1`, `sub[+0x28]&0x7F`, `cvttss2si(sub[+0x78])`, `movsx(sub[+0x68])` | whole cluster; leaves at `00265510`/`00265530`/`00265550`/`00265580`/`002655D0`/`00265600`/`00265630`/`00265660`; `002E6300`'s `js` enters the head leaf with `rcx` still the actor | 1 (static) | PROVEN |
| `002627C0` copies the `0x80` steering record from slot `+0xDC` to slot `+0xDC+1` | `movsx rax, byte[rcx+0xDC]` / `inc eax` / eight `movaps` pairs at `+0x120`+`idx*0x80`; the push half of the depth-one stack — caller `002EAB80` owns the depth byte itself | 1 (static) | PROVEN |
| `002EC2C0` is the kind-3 vector-writer: stores `[rdx]` (a `Vec4`) into `[ctx+0xF0]+0x10`, clears `+0x62` bits 0–2, then `002E7B40`/`00265020`/`003A19A0`/`0026A8E0` apply a position-derived heading and `0026A870`/`0026A950` zero two channels | `002EC2C0`–`002EC37A` whole body; kind gate `(+3 & 0xE0)==0x60` at `002EC2D9`; `and byte[+0x62],0xF8` at `002EC308` | 1 (static) | PROVEN |
| `002EBE50` is the mode initiator: `edx==0` zeroes `+0xB4`/`+0x224`; else snapshots `sub[+0x70]`/`+0x74` into them after `003A1C50`-wrapping the deltas, derives a frame count `abs(Δ)/sub[+0x6C]` (clamped by a constant) into `word[+0x60]` (`derived_turn_frames` in `_types/`), `+0x62` bit 5 cleared and bit 4 set, stamps `+0x63 = arg2`, then calls `002EC3F0` and `002E8EE0` | `002EBE50`–`002EBF96` whole body; frame-count arm gated on `+0x62 & 0x38 == 0` at `002EBF14`; `00265200()` supplies the initial `+0xB4` when `sub[+0x63]!=0` or `r8d==0` | 1 (static) | PROVEN |
| `002EBFA0` steers toward a resolved target body: `003587C0` resolves the target, `[rsi+0xC0]` record must exist with `dword != -1`; writes the target triple `+0x10`/`+0x14`/`+0x18` and `003589B0(rsi)` id into `+0x1C` (`resume_target_handle` in `_types/`), `+0x62` bit 0 set and bits 1–2 cleared; heading from both `00265020` world positions via `003A19A0` → `0026A8E0`; fallback arms call `00265470`+`002EC2C0` or `002E64E0` | `002EBFA0`–`002EC137` whole body; the three `-1`/null rejections at `002EBFF3`–`002EC005` | 1 (static) | PROVEN |
| `002EAB80` is the push driver: gated `actor[+0x18]!=1` then kind-3 then `ctx[+0xDC]==0`; `002627C0` clones slot 0→1, `inc [+0xDC]`, `00269F90(ctx)`, `0026AE90(actor,0)`, `0026C120(actor,0)` | `002EAB80`–`002EABE2` whole body; the three gates at `002EAB86`/`002EAB8F`/`002EABA5`; `inc` at `002EABB6` | 1 (static) | PROVEN |
| `002EAAA0` is the pop driver: same `+0x18`/kind gates, then `ctx[+0xDC]!=0`; `dec [+0xDC]` (slot 0 was never overwritten — it is the saved pre-push state), `00269F90(ctx)`, then replays `sub[+0x62]&7` — 0 → `002EC2C0(actor,sub+0x10)`, 1 → `002EBFA0(actor,sub+0x10/0x14/0x18)`, else nothing — and always `002EC3F0`+`002E8EE0` | `002EAAA0`–`002EAB30` whole body; `dec`+store at `002EAAD0`–`002EAAD5`; mode dispatch at `002EAAE7`–`002EAB15` | 1 (static) | PROVEN |
| the push/pop caller side is a script op dispatch: `003DBDC0`→`00263230`(op==1) drives push; `003DB2A0`→`00263050`(op==4) drives pop only when `actor[+0xB]` bit 4 is set and clears that bit after | `00263050`–`0026308F` dispatch head (`edx-1`/`edx-3`/`edx-4` arms); `test byte[+0xB],0x10` at `0026306C`; `and [+0xB],0xEF` at `0026307B`; edges.tsv `003DB2A0`/`003DBDC0` rows | 1 (static) | PROVEN |
| `002EC140` stamps resume shape 2: kind-3 gate, raw `{xmm1,xmm2}` into `sub+0x10`/`+0x14`, `+0x62 = (&0xFA) or 2`, then `0026A8E0`/`0026A870` apply and `0026A9C0`/`0026A950` zero | `002EC140`–`002EC1BE` whole body; the `&0xFA or 2` store at `002EC186`–`002EC18A` | 1 (static) | PROVEN |
| `002EC1C0` stamps resume shape 3: two-sided wrap (±π offset by arg sign, mod 2π) of `{xmm1,xmm2}` into `sub+0x10`/`+0x14`, `+0x62 = (&0xFB) or 3`, then `0026A8E0`/`0026A870` apply | `002EC1C0`–`002EC2BC` whole body; wrap sequence `002EC1F3`–`002EC25B`; the `&0xFB or 3` store at `002EC28C`–`002EC294` | 1 (static) | PROVEN |
| the mode-4 timed turn interpolates `heading(t) = turn_start_heading(+0x38) + wrap(target_heading(+0x34) − +0x38) × min(turn_frame_index, turn_frames)/turn_frames`, then advances the frame index by 1; `0026C290` captures `+0x38` as the argument's two-sided wrap at arm time | `002E58BB`–`002E5931` in `002E5750`: `subss` at `002E58BF`, sign-π at `002E58EB`, `mod 2π` at `002E5900`–`002E5917`, `mulss`/`addss` at `002E591B`/`002E591F` → `0026B6A0`; `min` at `002E589D`; index advance via `0026C300` at `002E5931`; `0026C290` writer at `0026C2BB`–`0026C2EF` | 1 (static) | PROVEN |
| `+0x70`/`+0x74` are the two steer channels' wrapped targets (heading and aux/pitch): written only via wrap helpers `0026A8E0`/`0026A870`; the initiator `002EBE50` wraps `(+0x70 − ctx+0xB4)` against a mirror seeded from `ctx+0xA8` via `00265200`, derives `derived_turn_frames` from the residual, then snapshots both to `ctx+0xB4`/`ctx+0x224` | `0026A8E0`/`0026A870` whole bodies (sign-π, mod-2π, store); `002EBEC3`/`002EBEE5` delta reads, `002EBF01`/`002EBF0A` mirror stores, `00265216` the `ctx+0xA8` seed; arg sources `00269242` (mode-4: `target_heading`), `002EC18E`/`002EC199` + `002EC297`/`002EC29C` (look-at arg pair); `+0x74`/`+0x224` zeroed by mode-4 at `00269275`/`00269289` | 1 (static) | PROVEN |
| `+0x63` is `steer_arm_state` — the steer channel's armed-state byte: `002EBE50` stores its `edx` op verbatim and gates fresh-arm mirror reseeding on the byte being 0; the teardown/reset paths zero it in the same store sequence that clears `ctx+0xB4`/`ctx+0x224` | `002EBF76` (`mov byte[+0x63], sil`, `sil = esi = edx`); `002EBE9C` (`cmp byte[+0x63],0` → seed path); teardown zero-stores `002E6519` (`xor ebx,ebx` at `002E64FF`), `002E3043`, `002E32BD` (the function's zero register `r12b`); observed values 0 (teardown) and 1 (mode-4 arm via `002690D0` `edx=1`) | 1 (static) | PROVEN |
| `+0x6C` is `initiator_turn_step` — the per-frame angular step the initiator divides the wrapped delta by to derive `derived_turn_frames` (`+0x60`): `max(1.0, abs(Δwrapped) / +0x6C)`; written by `0026AAD0` as the two-sided wrap of its argument times the rate global `[01DFE0BC]` — a rate-scaled step, not a bare residual | `002EBF18`–`002EBF5F` (`divss`/`cvttss2si` in `002EBE50`); `0026AAD0` whole body (sign-π at `0026AADB`/`0026AAE5`, `mod 2π` at `0026AAFE`–`0026AB2B`, `mulss [01DFE0BC]` at `0026AB2F`, store `0026AB37`); no `E8` caller — arg source is indirect | 1 (static) | HIGH |
| `002EC3F0` is the steer dispatcher: it decodes two packed fields from `+0x62` — dispatch mode = bits 3–5 (`shr 3, &7`), resume shape = bits 0–2 (`&7`) — then tail-jumps one of six apply arms carrying `derived_turn_frames` as `xmm1` (shape ≤1: mode 1 → `002E7650`, mode 2 → `002E79A0`; shape 2: mode 1 → `002E7720`, mode 2 → `002E77F0`; shape 3: mode 1 → `002E78D0`, mode 2 → `002E7860`; the shape-2/3 arms also forward the `+0x10`/`+0x14` resume pair in `xmm2`/`xmm3`). `+0x6A` bit 0 is a one-shot latch that remaps mode 2 → mode 1 and is consumed (`&0xFE`) in the same pass | `002EC3F0`–`002EC4F6` whole body; mode/shape decode `002EC40F`–`002EC422`; latch test `002EC424`, remap `cmovne` `002EC42F`, clear `002EC433`; shape-3 conditional arms `002EC4AD`/`002EC47B` match §18's member table; setter `002EC3C0`–`002EC3EA` writes bit 0 from `edx != 0` | 1 (static) | PROVEN |
| any runtime observation | **none exists** | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every claim reproduced, and the two that carry the most weight — a **negative** and an **identity** —
were tested exhaustively rather than by sampling.

### The three wrap constants, dereferenced rather than quoted

| address | bytes | value | claimed |
|---|---|---|---|
| `01CEBC50` | `DB 0F 49 40` | **3.14159274** | +π ✔ |
| `00915620` | `DB 0F 49 C0` | **−3.14159274** | −π ✔ |
| `01CEBC78` | `DB 0F C9 40` | **6.28318548** | 2π ✔ |

All three are the `float` roundings of their constants. The record stride is confirmed at
`00269F9F shl rax, 7` — **×128 = 0x80** — followed by `add rax, 0x120`.

### The identity claim, and the negative that makes it matter, close on each other

Normalising both variants the way §2 describes — RIP targets resolved, branch targets ignored:

| | instructions | differing positions |
|---|---:|---|
| `0026B5A0` (117 B) | **29** | — |
| `0026B620` (120 B) | **29** | **1**, at index 12 |

The single difference is `xor r8d, r8d` against `mov r8d, 1` — the flag, passed in `r8`. And the
callee `0026B6A0` (120 B, **30 instructions**) mentions `r8` in **zero** operands: not as a register,
not as a memory base, not as an index.

> **The two halves are the same fact from opposite ends.** The variants differ only in what they put
> in `r8`, and the function they hand it to provably never looks at `r8`. Neither statement alone
> settles that the variants are interchangeable; together they do, and both are exhaustive over their
> whole bodies rather than over a sampled path.
>
> **Correction 2026-09-18:** exhaustive over *the dispatcher's* body, not over the path. The
> kind-3 arm tail-jumps `002E5FB0` with `r8d` still live, and `003EC260` reads it as the
> commit gate — the variants are interchangeable only for kind ≠ 3. The measurements above
> stay exactly as measured; the conclusion's scope is what narrowed.

### Also confirmed

The kind dispatch is byte-identical in both consumers — `movzx ecx, byte [rcx+3]` / `shr ecx, 5` /
`sub ecx, 1` / `cmp ecx, 2` in `0026B6A0` **and** `0026C090`.

**Not claimed:** ~~the seven remaining named callees are still unread, and~~ *(answered: see §14 items 1–2, all read 2026-09-18; 2026-10-02, OPUS)* nothing here is a
runtime observation. *(`002E5FB0` was read 2026-09-18 — §14 item 1.)*

## 16. Parity plan

**Testable now, statically:** `CALCULATION` — the wrap over a large float sweep including
denormals, ±0, large magnitudes and values already in range; the turn-direction bit; the slot
address arithmetic. `STRUCTURAL` — the record layout against `_types/`.

**Requires the running game:** `STATE-TRANSITION` for the mode arms that call unread functions,
`INTEGRATION`, `TIMING` (mode 4's frame-rate sensitivity is exactly a timing claim).

**Will not be tested, and why:** `RNG` — none is drawn. `SERIALIZATION` — nothing here is
serialised; the steering records are not part of the save payload.

> **The wrap was the honest pilot here**, and it paid: `CALCULATION` is now **covered for
> both forms** — 8,280 comparisons against the shipped bytes, **0 mismatches** — and `DY-1`
> is answered outright. [`diff_angle_wrap.py`](../../../Reconstruction/Tests/Differential/diff_angle_wrap.py) and
> `Reconstruction/Game/Math/angle_wrap.{h,c}`. **The subsystem's readiness does not move:**
> two pure functions of the ten entries, on a machine that never rendered a frame.

## 17. Charter §26 readiness assessment — 2026-09-10, OPUS (not this contract's author)

Run as an adversarial check: the same §26 question list I applied to actor storage, on a subsystem
I did not write, whose front matter claims `CONTRACT READY`. **A sample of its claims was verified
against the binary rather than accepted.**

### What survived checking

| claim as written | checked | result |
|---|---|---|
| record is `0x80`, inline, two of them at context `+0x120` | `00269F9F shl rax,7` then `00269FA3 add rax,0x120` | **holds exactly** |
| the slot selector is 0 or 1 and the out-of-range path is **fail-open** | `00269F97 cmp al,1` / `ja 0x269FB3` → `ret` without touching `+0xF0` | **holds exactly** |
| `_types/` carries 32 fields, 13 named | 32 and 13 | **holds** |
| 33 of 128 bytes have no accessor | 95 declared of 128 | **holds** |

*(The two count rows were true of the census at audit time; re-measured 2026-09-18 the census
carries 40 rows / 33 named and 21 bytes with no censused reader — §14 item 8.)*

**Nothing in the sample failed.** Worth recording, because the point of checking is that it could
have. One detail the contract does not mention and a reimplementation should: the selector is
loaded `movzx`, compared **unsigned** against 1, and only then sign-extended with `movsx` — the
unsigned guard is what makes the later sign-extension safe. Reorder those and a `0x80` selector
becomes `-128` and indexes far outside the context.

### §26, axis by axis

**Answered:** responsibilities; owner; what it owns (nothing — both records are inline and `+0xF0`
is a cursor); key types; the kind-3 gate and its silent return; update ordering within the family;
state read and written, enumerated per field; state transitions including the depth-one stack and
both refusal conditions; determinism; the `FrameLimit` time base dependency; invariants, including
~~that the wrap is idempotent so `0026C090` is safe to call directly~~ that a heading is wrapped before it is
stored, and that the re-wrap is a two-cycle at exactly ±π, so each path's wrap count is part of its behaviour
*(corrected 2026-09-28, FABLE, Claude Opus 5.5)*.

**Not answered:**

1. **No LIVE runtime observation.** §13 says so itself — *"Evidence class: isolated original-code.
   Live capture: still absent, and this is the gate the subsystem fails."*
   ~~*"None. Empty deliberately, and this is the gate the subsystem fails."*~~ **This summary
   quoted §13's pre-correction wording until 2026-09-14.** §13 was rewritten under
   `OPUS-NOTICE-S13-CLASSES` (`f921048`) precisely because a none-or-some field made a contract
   holding isolated original-code evidence say it held nothing; the quotation here was not updated
   with it, so this section went on reporting *no* evidence where §13 now reports a **class** of it.
2. **Eight named callees unread**, `002E5FB0` first among them, which the contract calls the single
   largest gap. The mode-0 and pop chains are named and not decoded, so what a pop actually
   restores is not established.
   *(Closed 2026-09-18: all eight named callees are now read — §14 items 1–2, the
   `js` target `00265510` turned out to be the head of the eight-leaf kind-3 accessor
   cluster `00265510`–`0026567F`, and the pop chain's caller side closed with it —
   `003DB2A0`→`00263050`(op 4)→`002EAAA0`, §14 item 3.)*
3. **What pushes and pops is unknown** (`DW-2`). A depth-one stack whose callers are unidentified
   is a state machine with an unknown driver.
   *(Answered since — `DW-2`, 2026-09-12: a script taking the character over pushes and pops it; see
   [the two steering slots](Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md).)*
4. ~~19 of 32 fields unnamed and 33 bytes with no accessor.~~ **Narrowed 2026-09-18:** 5
   placeholder-named fields of the current 40 rows (33 semantically named after eight
   contract-side renames), and 21 bytes without a censused reader
   (9 never observed, 12 ctor-zeroed) — see §14 item 8.

### Verdict, and the reason it matters beyond this subsystem

**Not reconstruction-ready** — same verdict as actor storage, and **failing on the same first
axis**.

That is the finding worth carrying up. Two subsystems, assessed independently by the same list, one
of which I built and one of which I did not, both answer most of §26 and both fail at *"have major
assumptions been runtime validated?"*. Neither fails for want of static reading: actor storage
declares 1,662 of 1,760 bytes and this contract's every checkable number is exact. **The shared
blocker is a class of evidence, not a quantity of it** — which means more static work does not move
either one, and the project's readiness is currently limited by runtime access rather than by
analysis.

This contract also states its own cheapest unblock — three values, *"one attach answers all
three"*. That is the same shape as the request I filed for actor storage
(`OPUS-REQ-ASTRA-ACTORLIVE`), and the two could plausibly share a single capture.

**This is one subsystem's assessment and an observation across two.** It is not a project gate
decision, which §§26–27 require the three identities to take together.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **CombatAction — CLIENT.** `Battle_ProcessActionTarget` sets heading through `Actor_SetDesiredMovementHeading` and
  `Actor_SetFacingHeading_Variant1`.
- **Party — CLIENT.** `PartyControl_ApplyAnalogLocomotionToActor` uses `Actor_SetDesiredMovementHeading` and
  `Actor_SetFacingHeading_Variant0`. A 639-byte Party-filed body uses the desired-heading and variant-1 setters. So
  analog stick steering and AI steering meet in the same two setters.
- **Gameplay — CLIENT.** `BattleAction_FindApproachGeometryAroundTarget` calls `Angle_NormalizeRadiansPi` (`0033CB70`).
- **Audio — CLIENT.** The angle wrap `003A1C50` folds an angle into `[−π, π]` by adding or subtracting `2π` (constants
  `00915620`, `01CEBC78`, `01CEBC50`, `00915624`). It is called by two Audio-filed bodies of 982 and 1,036 bytes.
  Both call `atan2f`, and the second reads the party focus actor's world position. They read as positional sound
  panning, and they are not read here.

**Script VM — CLIENT.** `002EC380` is called from the script bridge (`0034EB40`, `0034F470`, `0034FBB0`, `003520B0`, `00350410`, `00357C40`, `00357D10`, `00357BA0`, `00357B10`, `00343F90`, `003517E0`, `00351D10`) — the steering-bits write is script-driven, not shared ownership.
- **Input - SERVICE (1 edge).** `00263230` reaches bodies filed to input: `00226BE0` (ActorControlMaskPropagationRuntime) - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (63 edges).** `0024ED80`, `00265020` are also called by bodies filed to presentation: `003B27A0`, `003B3480`, `003EE2D0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (3 edges).** `00422940`, `004256E0` reach bodies filed to resource: `002ED570`, `00409600`, `00409F50` - shared machinery across the layer boundary, no shared ownership.

## 18. The `002EC3F0` exclusive subtree — all 15 members bound (SWE2-FRONTIER, followup queue)

`002EC3F0` is the mode-pair dispatched steering-parameter writer §14 asked about. It gates on the
`0x60` record kind (`[rcx+3]&0xE0`), loads the profile record `[[rcx+0xB8]+0xF0]`, and reads two
mode nibbles from `[+0x62]` — `eax` = low `&7`, `edx` = high `>>3 &7` (high 2 folds to 1 when
`[+0x6A]` bit 0 is set, and the bit is cleared). The pair picks one of four apply arms: `eax` 2–3
runs a vec3 arm (`xmm1` = `cvtdq2ps(word[+0x60])`, `xmm2`/`xmm3` = `[+0x10]`/`[+0x14]`), `eax` ≤1 a
scalar arm (`xmm1` only). Every member was disassembled from the shipping image; interior citations
are instructions inside each member's declared extent.

| member | role | interior |
| --- | --- | --- |
| `002E7720` | 196 B — the vec3 pair arm: resolves `[rcx+0xC0]`'s linked record → `word[rax]` index ×`0x740` into `022C6F28` (`+0x284` gate) **twice**, writing via `003E6B80` then `003E6C00(1,0x30B)`, each marking `+0x290 \|= 0x800` | [`002E7770`](../_index/ADDRESS-INDEX.md) |
| `002E77F0` | 97 B — the second vec3 arm: same resolve/gate, writes via `003E6B60`, marks `+0x290 \|= 0x800` | [`002E7838`](../_index/ADDRESS-INDEX.md) |
| `002E79A0` | 97 B — the scalar arm: same resolve/gate, writes via `003E6BA0`, marks `+0x290 \|= 0x800` | [`002E79E8`](../_index/ADDRESS-INDEX.md) |
| `003E6B60` | 12 B — `+0x580` sub-record adapter, tails `003E3120` | [`003E6B67`](../_index/ADDRESS-INDEX.md) |
| `003E6B80` | 12 B — `+0x580` adapter, tails `003E31E0` | [`003E6B87`](../_index/ADDRESS-INDEX.md) |
| `003E6BA0` | 12 B — `+0x580` adapter, tails `003E33A0` | [`003E6BA7`](../_index/ADDRESS-INDEX.md) |
| `003E3120` | 29 B — vec3 store (`xmm1`/`xmm2`/`xmm3` → `+4`/`+8`/`+0xC`) + flag edit `&0xFFE26DFF`, `bts 0x11` | [`003E3127`](../_index/ADDRESS-INDEX.md) |
| `003E31E0` | 29 B — same vec3 store, flag edit `&0xFFE0EDFF`, `bts 0xF` | [`003E31E7`](../_index/ADDRESS-INDEX.md) |
| `003E33A0` | 18 B — scalar store `xmm1` → `+4`, flag edit `&0xFFF07FFF \| 0x100000` | [`003E33A6`](../_index/ADDRESS-INDEX.md) |
| `002E78D0` | 196 B — the `al==3` vec3 two-record arm: same shape as `002E7720` — resolves `[rcx+0xC0]`'s linked record twice, writes record 1 via `003E6B90` and record 2 via `003E6C00(1,0x30B)`, marking `+0x290 \|= 0x800` each time | [`002E7920`](../_index/ADDRESS-INDEX.md) |
| `002E7860` | 97 B — the `al==3` single-record vec3 arm: same resolve/gate as `002E77F0`, writes via `003E6B70`, marks `+0x290 \|= 0x800` | [`002E78A8`](../_index/ADDRESS-INDEX.md) |
| `003E6B70` | 12 B — `+0x580` sub-record adapter, tails `003E31C0` | [`003E6B77`](../_index/ADDRESS-INDEX.md) |
| `003E6B90` | 12 B — `+0x580` adapter, tails `003E3320` | [`003E6B97`](../_index/ADDRESS-INDEX.md) |
| `003E31C0` | 29 B — vec3 store (`xmm1`/`xmm2`/`xmm3` → `+4`/`+8`/`+0xC`) + flag edit `&0xFFE46DFF`, `bts 0x12` | [`003E31C7`](../_index/ADDRESS-INDEX.md) |
| `003E3320` | 29 B — same vec3 store, flag edit `&0xFFE16DFF`, `bts 0x10` | [`003E3327`](../_index/ADDRESS-INDEX.md) |

The `002E78D0`/`002E7860` pair was first excluded as having other callers — **that was wrong**
(SWE2-AUDIT-SPEC, `AUDITSPEC-REQ-FRONTIER-EC3F0-EXCLUDED-PAIR`): they have *zero* callers in
`edges.tsv`. The extractor records call and unconditional-jmp edges only, and the root reaches the
pair by **conditional** `je` — `002EC4AD` (`al==3` → `002E78D0`, else `jmp 002E7720`) and
`002EC47B` (`al==3` → `002E7860`, else `jmp 002E77F0`). Under the exclusivity criterion the pair
and their private adapter/setter chains are members — the census is **15**, not 9. The
`002E7650`/`003E6C00` exclusions stand: `002E7650` is also called by `003B75E0`, and `003E6C00`
has seven callers. So the mode matrix is: low mode 2–3 × high 1 → `002E7720` (`al==2`) /
`002E78D0` (`al==3`); high 2 → `002E77F0` (`al==2`) / `002E7860` (`al==3`); low ≤1 × high 1 →
`002E7650`; high 2 → `002E79A0`.

## Interior citation — frontier hubs `0026B620`, `0026A0D0` (2026-09-18, SWE2-EC7)

`0026B620` — 120 B, 7 A-measured callers; `Actor_SetFacingHeading_Variant1`, the wrap-half
of the facing contract. Interior verified: the input float gets a `+/-0.5`-turn bias by sign
(constants `01CEBC50`/`00915620`), is divided by the `01CEBC78` period, `cvttss2si` at
[`0026B660`](../_index/ADDRESS-INDEX.md) truncates, and `value - trunc*period - bias` lands in `xmm6` — a
range-wrap, not a clamp. `0026B6A0(rcx, xmm6)` stores it, `0026C090` is the notification
tail.

`0026A0D0` — 97 B, 7 callers; `Actor_SetDesiredMovementHeading`, the desired-arc sibling.
Interior verified: the `byte[rcx+3] & 0xE0 == 0x60` tag gate (`0026A0D9`), then the same
bias/truncate/wrap arithmetic — `divss` at [`0026A105`](../_index/ADDRESS-INDEX.md) — writes the wrapped value
to `[+0xB8] + 0xA4` and returns. Desired heading lives on the secondary record, not the
facing field itself.


## Interior citation — frontier hub `00424370` (2026-09-18, SWE2-EC7)

`00424370` — 228 B, 6 A-measured callers; yaw-from-position-delta, the geometric half of this
contract's "face a point" path. Interior verified: `*rdx − [rcx+0x30..0x38]` gives the vec3
delta (`0042438B`–`004243B1`), `005213F0` normalises it ([`004243C7`](../_index/ADDRESS-INDEX.md)),
`0046D100`/`0046D340`/`0046D0C0` build and apply the reference frame against the identity
constant at `008C5FD0` (`004243D9`–`00424411`), and only when both transformed X and Z are
nonzero does it call `atan2f` (`00861F02`) at [`00424436`](../_index/ADDRESS-INDEX.md) — so a
degenerate delta returns without touching the heading. GS-cookie checked.

**Presentation — CROSSING.** Every caller of `00424370` lives in that layer —
`003E6340` and the `00422630`/`004226C0`/`004227D0`/`00422870`/`00422940`/`004256E0`
render-record bodies — and its matrix frame is built by Presentation's `0046D100`
(`Matrix4x4f_Copy`) with the `0046D340`/`0046D0C0` transform pair. The crossing is render-side
"face this point" work (relation-look and camera-facing records) borrowing this contract's
yaw math, not a facing system reaching into Presentation.


## Interior citation — frontier hub `002E8EE0` (2026-09-18, SWE2-EC7)

`002E8EE0` — 227 B, 10 callers; the render-record resolve sibling of `002E8FD0` (batch 8).
Interior verified: same `byte[rcx+3] & 0xE0 == 0x60` tag gate (`002E8EE6`–`002E8EF1`), reads
the `[+0xB8]` context's `[+0xF0]` sub-record bit `+0x62 >> 7` (`002E8F0F`–`002E8F1A`), then the
`[+0xC0]` record's `word [+0]` handle — both `-1` sentinels rejected (`002E8F22`–`002E8F2E`) —
indexes the `0x740`-stride table at `022C6F28` (`imul rbx, rax, 0x740` at
[`002E8F34`](../_index/ADDRESS-INDEX.md)) and requires `[rbx+0x284]` present before calling
through (`002E8F44`). The visibility path's "does this record exist and is it populated" half.

## SWE2-EC7-22 update (2026-09-18) — `0026B5A0` angle wrap-and-quantize

`0026B5A0` (117 B) is the wrap/quantize helper the steering math shares:
`comiss xmm6, 0` selects ~~`xmm1 = [01CEBC50]` (a `+pi`-class constant)~~ `xmm1 = [00915620]` (`-pi`) when the
input is negative, else ~~`[00915620]` (`-pi`-class)~~ `[01CEBC50]` (`+pi`) *(corrected 2026-10-02, OPUS: `0026B5B4` `comiss xmm6, 0` / `0026B5B7` `jb` → `0026B5C3` `movss xmm1, [00915620]`; otherwise `0026B5B9` `[01CEBC50]`; the bias is `h >= 0 ? +pi : -pi`, as §12 states)*, `addss` the correction,
`divss [01CEBC78]`, `cvttss2si` + `cvtdq2ps` round-trip — the signed wrap-then-
scale sequence the heading/steering evaluators call before quantizing.
Interior anchor `0026B5B4` (the `comiss` sign test). `rbx = rcx` keeps the
owner record for the continuation.

## SWE2-CONTRACT correction (2026-09-18) — the facing flag is live on kind 3

The earlier claim that `0026B6A0` "never touches `r8`" made the flag dead was true
of the dispatcher body and wrong of the path: its kind-3 arm tail-jumps with
`r8d` still live into `002E5FB0` (`r9d = r8d`) → `002E5E10` (`[rsp+0x50] =
r14d != 0`) → `003EC260`, where it gates the slot commit. `0026B5A0` (flag 0)
stages the ~~`{rate, heading, 0}`~~ `{pitch, heading, 0}` triple *(corrected 2026-10-02, OPUS: lane 0 is the `+0xAC` pitch, `002E5F4F` → `003EC348`)* only; `0026B620` (flag 1) stages and
commits through `004288B0` ~~or~~ and then `003B3CA0` *(corrected 2026-10-02, OPUS: `003EC39E`, then `003EC3A3`–`003EC3BC`)*. The variants are identical only for
kind ≠ 3. §15/§15a wording and the `diff_angle_wrap` CONTRACT_MAP updated to
match; the old "what `002E5FB0` does" OPEN QUESTION is closed.

## SWE2-EC7-29 update (2026-09-18) — `0026A8E0`/`0026A870` `+0x70`/`+0x74` wrap stores

`0026A8E0` and `0026A870` (101 B each) are the `+0x70`/`+0x74` angle wrap
stores — the `0026B5A0` wrap sequence applied to a steering-record slot:
`xmm3 = xmm1` receives `+pi` (`01CEBC50`) or `-pi` (`00915620`) by sign,
`byte[rcx+3] & 0xE0 == 0x60` gates the write, the
`divss`/`cvttss2si`/`cvtdq2ps`/`mulss` round-trip through `01CEBC78`
(2pi) truncates the wrap count, and two `subss` recentre into
~~`[-pi, pi)`~~ `[-pi, pi]` — `[-pi, pi)` for a non-negative input and `(-pi, pi]` for a negative one *(corrected 2026-10-02, OPUS: `0026A8E6` `comiss` / `jb` selects the bias by sign; `0026A876`–`0026A8CB` the same in `0026A870`)*; the result lands at `[[rcx+0xB8]+0xF0]+0x70` / `+0x74`.
Interior anchors `0026A90E`/`0026A89E` (the `divss`). The adjacent
`0026A950`/`0026A9C0` siblings write `+0x224` and further slots.

## SWE2-EC7-36 update (2026-09-19) - `003E6340`

`003E6340` (657 B) is a facing/steering body - `00915624`/`01CEBBA8`, `00424370` triple plus `00861F14`/`0041F2F0`/`003E6E60`/`00808C40`. Interior anchor `003E636A` (a `00424370` call).

## SWE2-EC7-48 update (2026-09-19) - `002E7B40`

`002E7B40` (201 B) is a body - `003E6C00`/`003E6CC0`. Interior anchor `002E7B95` (an `003E6C00` call).

## SWE2-EC7-48 update (2026-09-19) - `003B75E0`

`003B75E0` (199 B) is a body - `002E7600`/`002E7650`/`002E7A10`/`002E7B40`. Interior anchor `003B7623` (a `002E7600` call).

## SWE2-EC7-67 update - `0026C090`

`0026C090` (129 B) is the call-free facing tail target - `comiss` sign pick `+-pi` (`40490FDB`/`C0490FDB`), `cvttss2si`/`cvtdq2ps` wrap by `2pi` (`40C90FDB`), kind `byte[+3]>>5`: kind 1 tail `0026B6A0(rcx,wrapped,1)`, kind 3 stores `[[rdx+0xB8]+0xF0]+0x34`, else no-op. Interior anchor `0026C0BE` (the `2pi` `divss` wrap).

## SWE2-EC7-68 update (2026-09-19) - `004288B0` steering-slot commit flags measured

`004288B0` (40 B) is the slot-flag setter the commit path calls as
`004288B0(slot, -1)`: `+0x290` always gains bit `0x400`; with
`edx == -1` it sets `+0x284` bit `0x20000` and zeroes
`byte[+0x40A]`, and with any other `edx` it adds `dl` to
`byte[+0x40A]` instead. Note the measured direction: the `-1` arm
*sets* the `0x20000` bit where the contract prose above calls it a
clear - the byte reset at `+0x40A` is the clear the commit
consumes. Call-free. Interior anchor `004288BF` (the `0x20000`
or).

## SWE2-EC7-84 update (2026-09-20) - `00424280` float wrap measured

`00424280` (39 B) is the two-constant range wrap the steering
callers run: `xmm0 > [const1]` adds `[const2]`, then `[const3] >
xmm0` adds `[const4]` - a phase-style normalization folded to two
guarded `addss`, call-free.
Interior anchor `00424289` (the first `addss`).

## SWE2-EC7-89 update (2026-09-20) - `003B3CA0` keyed global-swap measured

`003B3CA0` (114 B) is the generation-checked swap the steering
callers run: `ecx & 0x3F` picks the 0x38-stride slot in
`02EBD480`, and only when the slot key matches and `+0x10` is
live does it `0024ED80` the slot record, run `003A9490(edx)`,
restore the `02F97340`/`02F97348` globals it saved, and
`0024ED80` once more - a scoped global override.
Interior anchor `003B3CE0` (the first `0024ED80` call).

`002EC380` (60 B) is the `0x60`-kind steering write: records whose `byte[+0x3] & 0xE0 == 0x60` get `dl << 3` xor-folded into bits 3-5 of `[+0xB8]`'s `+0xF0` sub-record `byte[+0x62]`, then `word[+0x60]` takes `cvttss2si(xmm2 / 1.0f)` - the masked steering-bits update the stop-registry and facing callers share.

Interior anchor `002EC3A4` (function `002EC380`).

`002E7A80` (178 B) is the pair-link commit `002EBFA0` runs for two facing records: each argument's `[+0xC0]` block must resolve with a `[0] != -1` head before `002EDB30` is invoked (`ecx = word[rcx-block]`, `edx = 0`, `r8d = [rdx-block]`); afterwards, when `rbx`'s own block carries a live `u16` index, its `idx * 0x740 + [022C6F28]` row with `[+0x284] != 0` is committed - `003E6C00(row, 1, 0x30B)` plus `or [row+0x290], 0x800` - the paired link plus the row's steering-flag arm

Interior anchor `002E7AF6` (function `002E7A80`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-facing-and-steering-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00265550` | 43 B | when the top three bits of byte `[rcx + 3]` are 3 (`AND 0xE0` equals `0x60`) it returns float `+0x154` of the `0x80`-byte slot selected by the signed byte `+0xDC` of `[rcx + 0xB8]`; otherwise it returns 0.0 | `00265556`, `0026555A`, `00265565`, `0026556D`, `00265571` |
| `00265580` | 78 B | when the top three bits of byte `[rcx + 3]` are 3 (`AND 0xE0` equals `0x60`) it returns float `+0x154` of a `0x80`-byte slot of `[rcx + 0xB8]`: the slot is the signed byte `+0xDC` when `edx` is negative, else `edx` capped (signed) at that byte; otherwise it returns 0.0 | `00265586`, `00265597`, `002655A7`, `002655BA`, `002655C4` |
| `00265600` | 35 B | when the top three bits of byte `[rcx + 3]` are 3 (`AND 0xE0` equals `0x60`) it returns the low seven bits of byte `+0x28` of qword `[[rcx + 0xB8] + 0xF0]`; otherwise it returns 0 | `00265606`, `0026560A`, `00265614`, `0026561F` |
| `0026A9C0` | 97 B | adds pi (`01CEBC50`) to the angle `xmm1` when it is at least 0.0, else -pi (`00915620`); then, when the top three bits of byte `[rcx + 3]` are 3 (`AND 0xE0` equals `0x60`), it subtracts the truncated quotient of that sum by 2pi (`01CEBC78`) times 2pi and the same signed pi again, and stores the result to float `+0xB4` of `[rcx + 0xB8]`; otherwise it stores nothing | `0026A9C9`, `0026A9E1`, `0026A9F6`, `0026AA14`, `0026AA18` |
| `002EDB30` | 72 B | when the word `cx` is not -1 and the `0x740`-byte record at that signed index under qword `022C6F28` is non-null with a nonzero dword `+0x284`, passes the record to a 12-byte forwarder (which works on `record + 0x580`) and ORs `0x800` into its dword `+0x290`; otherwise it returns without a call | `002EDB34`, `002EDB43`, `002EDB53`, `002EDB5F`, `002EDB64` |
| `00343F90` | 103 B | pops an integer through `VMValueStack_PopInt32CoerceFloat32(r9)` and a float through `VMValueStack_PopNumericDiscard`, calls `002EC1C0(rdx)` with the float in `xmm1` and 0.0 in `xmm2`, then `002EC380(rdx, 2)` with the integer converted to float in `xmm2`, and tail-jumps `002EBE50(rdx, 1, 0)` | `00343FA8`, `00343FB2`, `00343FC0`, `00343FD4`, `00343FF2` |
| `0034EB40` | 121 B | pops two floats through `VMValueStack_PopNumericDiscard`, calls `0026AAD0(rdx)` with the first in `xmm1`, `002EC1C0(rdx)` with the second in `xmm1` and 0.0 in `xmm2`, `002EC380(rdx, 0)` with 0.0 in `xmm2`, and tail-jumps `002EBE50(rdx, 1, 0)` | `0034EB5D`, `0034EB76`, `0034EB84`, `0034EB91`, `0034EBB4` |
| `0034F470` | 121 B | pops two floats through `VMValueStack_PopNumericDiscard`, calls `0026AAD0(rdx)` with the first in `xmm1`, `002EC140(rdx)` with the second in `xmm1` and 0.0 in `xmm2`, `002EC380(rdx, 0)` with 0.0 in `xmm2`, and tail-jumps `002EBE50(rdx, 1, 0)` | `0034F48D`, `0034F4A6`, `0034F4B4`, `0034F4C1`, `0034F4E4` |
| `0034FBB0` | 146 B | pops three floats through `VMValueStack_PopNumericDiscard`, calls `0026AAD0(rdx)` with the first in `xmm1`, `002EC140(rdx)` with the third in `xmm1` and the second in `xmm2`, `002EC380(rdx, 0)` with 0.0 in `xmm2`, and tail-jumps `002EBE50(rdx, 1, 0)` | `0034FBEA`, `0034FBF8`, `0034FC07`, `0034FC14`, `0034FC3D` |
| `00350410` | 146 B | pops three floats through `VMValueStack_PopNumericDiscard`, calls `0026AAD0(rdx)` with the first in `xmm1`, `002EC1C0(rdx)` with the third in `xmm1` and the second in `xmm2`, `002EC380(rdx, 0)` with 0.0 in `xmm2`, and tail-jumps `002EBE50(rdx, 1, 0)` | `0035044A`, `00350458`, `00350467`, `00350474`, `0035049D` |
| `003517E0` | 100 B | pops two floats through `VMValueStack_PopNumericDiscard`, calls `002EC140(rdx)` with the second in `xmm1` and 0.0 in `xmm2`, then `002EC380(rdx, 2)` with the first in `xmm2`, and tail-jumps `002EBE50(rdx, 1, 0)` | `003517F8`, `00351803`, `00351811`, `00351821`, `0035183F` |
| `00351D10` | 121 B | pops three floats through `VMValueStack_PopNumericDiscard`, calls `002EC140(rdx)` with the third in `xmm1` and the second in `xmm2`, then `002EC380(rdx, 2)` with the first in `xmm2`, and tail-jumps `002EBE50(rdx, 1, 0)` | `00351D43`, `00351D48`, `00351D51`, `00351D61`, `00351D84` |
| `003520B0` | 121 B | pops three floats through `VMValueStack_PopNumericDiscard`, calls `002EC1C0(rdx)` with the third in `xmm1` and the second in `xmm2`, then `002EC380(rdx, 2)` with the first in `xmm2`, and tail-jumps `002EBE50(rdx, 1, 0)` | `003520E3`, `003520E8`, `003520F1`, `00352101`, `00352124` |
| `00357B10` | 143 B | calls an 8-byte global getter (result unused), pops a float through `VMValueStack_PopNumericDiscard` and two integers through `VMValueStack_PopInt32CoerceFloat32`, and passes the second integer to a 53-byte actor lookup; when it returns non-null it calls `002EBFA0(rdx, byte [actor + 0x15], word [actor], first integer)`, `002EC380(rdx, 2)` with the float in `xmm2` and `002EBE50(rdx, 1, 0)`; a null lookup returns without those calls | `00357B2A`, `00357B4E`, `00357B66`, `00357B76`, `00357B85` |
| `00357BA0` | 149 B | pops a float through `VMValueStack_PopNumericDiscard` and two integers through `VMValueStack_PopInt32CoerceFloat32`, and passes the second integer to a 53-byte actor lookup; when it returns non-null it calls `0026AAD0(rdx)` with the float in `xmm1`, `002EBFA0(rdx, byte [actor + 0x15], word [actor], first integer)`, `002EC380(rdx, 0)` with 0.0 in `xmm2` and `002EBE50(rdx, 1, 0)`; a null lookup returns without those calls | `00357BD9`, `00357BE4`, `00357BEC`, `00357BFF`, `00357C1B` |
| `00357C40` | 193 B | builds a four-float stack block whose last float is 1.0 (`01CEBBA8`): pops a first float through `VMValueStack_PopNumericDiscard` and a second into float `+8` of the block, then a third into `+4` when a 39-byte predicate on `rdx` is zero (0.0 there, with no pop, when it is nonzero), and a fourth into `+0`; it calls `002EC2C0(rdx, &block)`, `002EC380(rdx, 2)` with the first float in `xmm2` and `002EBE50(rdx, 1, 0)` | `00357C69`, `00357C8E`, `00357CA1`, `00357CC0`, `00357CD0` |
| `00357D10` | 206 B | builds a four-float stack block whose last float is 1.0 (`01CEBBA8`): pops a first float through `VMValueStack_PopNumericDiscard` and a second into float `+8` of the block, then a third into `+4` when a 39-byte predicate on `rdx` is zero (0 there, with no pop, when it is nonzero), and a fourth into `+0`; it calls `0026AAD0(rdx)` with the first float in `xmm1`, `002EC2C0(rdx, &block)`, `002EC380(rdx, 0)` with 0.0 in `xmm2` and `002EBE50(rdx, 1, 0)` | `00357D47`, `00357D5E`, `00357D77`, `00357D93`, `00357DA0` |
