---
contract: Binding profiles — assign, publish, and translate to a per-frame control frame
category: 15-Input
scope: subsystem
level: L2
readiness: CONTRACT READY   # the READ path is RUNTIME VALIDATED (EXP-005, EXP-006); assignment is not
confidence: PROVEN
implements: binding-profiles-remapping-and-control-state.md
entries: [00198A00, 00197160, 00196FF0, 00195DF0, 00198000, 00198B60, 00196550, 00197710, 001DFA70, 0035F690]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 67 addresses cited - 24 data, 22 entry, 20 interior, 1 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-binding-profiles-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — binding profiles

> Formalises [`binding-profiles-remapping-and-control-state.md`](binding-profiles-remapping-and-control-state.md)
> (`L1` prose, two audit passes) and [`keymap-ini-file-format-and-default-controls.md`](keymap-ini-file-format-and-default-controls.md)
> into something an engineer can reimplement and a differential test can be written from.
>
> **Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`.** The *reading* half — polling a key
> and finding the byte it moves — is runtime validated by
> [`EXP-005`](../../_experiments/EXP-005-driving-the-input-state.md) and
> [`EXP-006`](../../_experiments/EXP-006-the-array-is-written-on-transition.md). **The assignment and
> publication halves have never been observed in a live process.**
>
> **What is new here, stated narrowly.** The record stride `0x15C` and the three banks were
> **already** derived by the keymap page; this contract re-derives the stride a third way, from the
> poll loop's own `add reg, 0x15C`, and closes `DD-2`, which was still filed `OPEN`. The genuinely
> new finding is §7's consequence: **the axis bytes accumulate across every bank**, which no page
> states and which a reimplementation would silently get wrong.

## 1. Purpose

Holds what each button does. Three things happen to a binding: it is **authored** (shipped defaults,
or `keymap.ini`, or the player remapping in the options menu), it is **published** into the records
the engine actually polls, and once per frame it is **translated** into an 18-byte control frame —
sixteen digital bits and sixteen axis bytes — which is what the rest of the game reads.

**The player-facing consequence of getting this wrong is total**: an inverted mask means every
control is held when nothing is pressed.

## 2. Interface

| operation | entry | conv | signature | returns |
|---|---|---|---|---|
| assign a binding | `00198A00` (349 B) | MS x64 | `(Mgr* rcx, int group edx, int slot r8d, int newId r9d, bool allowReplace [rsp+0x28])` | `eax` = result code, §4 |
| validate uniqueness | `00196550` (135 B) | MS x64 | `(…)` — conflict scan over all 84 slots | — |
| poll and build a frame | `00196FF0` (356 B) | MS x64 | `(Mgr* rcx, Frame* rdx)` | — (writes 18 bytes to `rdx`) |
| translate one record | `00197160` (1406 B) | MS x64 | `(Record* rcx, Frame* rdx)` | — (**accumulates** into the frame) |
| publish profiles | `00195DF0` (526 B) | MS x64 | `(…)` — reads `01F80F90`, applies the pair swap, writes `01F80130` | — |
| install shipped defaults | `00198B60` (782 B) | MS x64 | `(…)` — from `01DF09C0` / `01DF0A80` / `01DF1470` | — |
| load `keymap.ini` | `00198000` (1644 B) | MS x64 | `(…)` | — |
| read a slot on demand | `00197710` (99 B) | MS x64 | `(…)` — the six slots that bypass the mask, §11 | — |
| keep authored pair order? | `001DFA70` (8 B) | MS x64 | `(State* rcx)` | `cmp **dword** [rcx+0x64], 0 / sete al` — **32-bit**, see §4 |
| advance channel timing | `0035F690` (205 B) | MS x64 | `(Channel* rcx)` | — |

> **The GFZ names two of these backwards**, and the prose page already records it: `00195DF0` is
> annotated `RestoreDefaultBindingProfiles` but is the **publisher**, and `00198B60` is annotated
> `MaterializeRuntimeBindingProfiles` but is the **defaults-installer**. Binary over annotation.

## 3. Types

### 3.1 The authored profile — `0x70` per profile, at `01F80F90`

```
BindingProfile — 28 × u32 = 112 bytes (0x70); 3 profiles, 84 slots, 336 bytes total

  dword  0 .. 15   group 0   (16 slots)
  dword 16 .. 23   group 1   ( 8 slots)
  dword 24 .. 27   group 2   ( 4 slots)
```

**All zero in the shipped image** — filled at runtime by the defaults-installer or `keymap.ini`.

### 3.2 The runtime record the translator walks — `0x140` read, `0x15C` stride

```
BindingRecord
  +0x000   int[16]    sixteen digital binding codes  -> control-mask bits 0..15
  +0x040   entry[16]  sixteen 16-byte axis entries:
                        +0x00  int  mode     1 = digital->axis, 2 = two codes -> axis, 3 = analog
                        +0x04  int  axisId   passed to GetFilteredAnalogAxisValue; 2 and 3 inverted
                        +0x08  int  codeA    mode 2: negative direction (−0x7F)
                        +0x0C  int  codeB    mode 2: positive direction (+0x80)
  = 0x140 bytes READ by the translator
  ... 0x1C bytes the translator never touches ...
  = 0x15C bytes STRIDE between consecutive records          <-- §7, DD-2
```

> **These are two different shapes and neither derivation is wrong.** A remapping tool that edits the
> `0x70` authored profile has **not** edited the `0x140` runtime record. ~~**What converts one into the
> other is still not established for bank A** — `DD-1`.~~ *Corrected 2026-09-26 (FABLE): §7a of this contract answers
> `DD-1`. `00195DF0` is the conversion; it writes records 2–4 of bank A (`01DF1738` = `01DF1480` + 2 × `0x15C`).*

### 3.3 The control frame — 18 bytes

| offset | size | contents |
|---|---:|---|
| `+0x00` | 2 | digital mask, sixteen bits, **active-LOW** |
| `+0x02` | 16 | sixteen axis bytes |

Initialised, before any binding is examined, by `00196FF0`:

```asm
00197090  mov   word  [rbx],       0xFFFF                  ; mask: every bit SET = nothing held
00197093  movabs rax, 0x8080808080808080
0019709D  mov   dword [rbx + 2],   eax                     ; axes 0..3  = 0x80 (neutral)
001970A2  mov   qword [rbx + 6],   0                       ; axes 4..11 = 0
001970A6  mov   dword [rbx + 0xE], 0                       ; axes 12..15 = 0
```

**Only axes 0–3 get the `0x80` neutral; axes 4–15 are zeroed.** The first four are centred
quantities (two sticks); the rest are not.

## 4. Preconditions · postconditions · invariants

> **`001DFA70` compares a DWORD, and the difference is not cosmetic.** Both prose pages render it
> as *"`return state[0x64] == 0`"*, which reads as a byte test. The eight bytes are
> `83 79 64 00 / 0F 94 C0 / C3` — `cmp dword ptr [rcx+0x64], 0`. **A reimplementation testing one
> byte returns the wrong answer whenever `+0x65`..`+0x67` are non-zero**, and the pair swap then
> runs backwards: Circle and Cross exchange when they should not.
>
> This was found by the differential harness, which had made exactly that mistake in its own
> fixture — it wrote a single byte into a sentinel-filled page, so the compared dword was
> `0x5A5A5A00` and the "keep" case swapped. **The fixture was wrong, not the reconstruction.**

**Preconditions.**
- `00196FF0` does nothing at all unless `mgr[+0x39] != 0` — it branches straight to the epilogue.
- `00198A00` requires `group ∈ {0,1,2}` and a slot inside that group's count (16 / 8 / 4).
- The translator requires a `0x140`-byte record and an **already-initialised** frame (§3.3). Handing
  it a zeroed frame inverts the digital result and biases every axis by −128.

**Postconditions of `00198A00`:**

```
0  assigned (or cleared)
1  conflict, and replacement was not permitted — nothing changed
2  slot index out of range for the group, OR the id is reserved
3  unknown group id
```

**Invariants.**
- Flat index = `profile * 0x1C + slot + {0, 0x10, 0x18}` for groups 0/1/2. `0x1C` dwords = `0x70`
  bytes; group 2's byte-stepped `profile * 0x70` is the same stride written differently.
- The conflict scan bound is `flat <= 0x53` — **all 84 slots, across all three profiles**. Conflict
  detection is **global, not per profile**.
- **A pressed control CLEARS its bit.** The mask is only ever written by `&= ~(1 << n)`. A byte of
  `0xFF` means nothing is held.
- The 35 ids at `01DF13E0` can never be bound; the assigner refuses them with code `2`.

## 5. State

| | detail |
|---|---|
| **read** | `01F80F90` (authored), `01DF13E0` (reserved list), `01DF1480` / `01F80550` / `01F80970` (record banks), `01F7FFE0+8/+9` (axis invert), `008F3A2C` `01CEBBA8` `008C5B40` `01CEBC9C` (constants) |
| **written** | `01F80F90` (assigner), `01F80130` (publisher), `01F7FFE0+0x38` (stick-touched flag), `mgr[+0x3B]` cleared each poll, the caller's 18-byte frame |
| **allocated** | none on these paths — every structure is static |

**Bank A is written by `00195DF0` through an image-base register** (§7a) — invisible to the
RIP-relative map, which is why an earlier pass recorded it as having no writer.

**The other banks have exactly one RIP-relative INITIALISER each** — `01F80130` ← `0015BD30` (484 B),
`01F80550` ← `0015C0D0` (420 B), `01F80970` ← `0015BF20` (420 B). ~~exactly one RIP-relative writer each~~
**Corrected 2026-09-14 (OPUS), on `AUDITSPEC-AU23-15BD30-NOT-EXCLUSIVE`: `01F80130`'s bank has a SECOND
RIP-relative writer.** `FUN_00198960` (109 B) writes `+0x34` / `+0x38` of all three profiles — six references —
exchanging a `.data` word pair in place and mirroring it in, so it is a runtime **toggle**, not initialisation.
A third function, `FUN_00196290` (488 B), holds three more references and reads the profiles **out** into
`01DF1738`. The range `01F80130`–`01F80544` carries **24** RIP-relative references split **15 / 3 / 6**, and the
claim of exclusivity does not survive that count. The word that has to change is *writer*; *initialiser* is
still exact, and nothing about the stride derivation depends on exclusivity. They are **CRT prototype-copy
initializers, already read** by
[static initialization order and injection timing](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md):
`0015BD30` is *"a `0x40` header copy followed by a `0x80`-per-iteration block loop, three records of
stride `0x15C`"* — **a fourth independent derivation of the same stride**, from a different function
in a different category.

`01DF1480` has **no** RIP-relative writer at all — see the note on `DD-1` below.

## 6. Relationships

```
keymap.ini ──00198000──┐
shipped defaults ──00198B60──┤
player remap ──00198A00──┤
                         ▼
                  01F80F90   authored profiles, 0x70 stride
                         │
                    00195DF0   publisher: pair swap, then copy
                         ▼
                  01F80130 ─── 0x420 ──▶ 01F80550 ─── 0x420 ──▶ 01F80970
                                              │                      │
                  01DF1480 (bank A, 5 records)│                      │
                         └──────────┬─────────┴──────────────────────┘
                                    ▼
                             00197160  translator, once per record
                                    ▼
                             18-byte control frame
```

## 7. State transitions — the per-frame poll, in full

`00196FF0` runs the translator over **three banks**, two of them gated. The keymap page already
records the shape — *"polls five records at `01DF1480`, then two conditional banks"* — and this is the
same fact with the gate conditions read out:

| bank | address | records | gate |
|---|---|---:|---|
| A | `01DF1480` | **5** | none (beyond `mgr[+0x39] != 0`) |
| B | `01F80550` | **3** | `mgr[+0x3A] & 2` |
| C | `01F80970` | **3** | `mgr[+0x3A] & 5` |

```asm
001970B0  loop A:  rcx = rsi;  rdx = frame;  call 00197160;  add rsi, 0x15C;  5 times
001970C8  test byte [rdi+0x3A], 2   ; je -> skip bank B
001970E0  loop B:  ... add rsi, 0x15C;  3 times
001970F8  test byte [rdi+0x3A], 5   ; je -> skip bank C
00197105  loop C:  ... add rdi, 0x15C;  3 times
0019711D  movups xmm0,[rbx] / movups [r13],xmm0 / movzx eax,[rbx+0x10] / mov [r13+0x10],ax
```

**So between 5 and 11 records are translated into one frame every frame**, and the three `add`s of
`0x15C` are where the stride comes from.

> **`DD-2` was already answered and still filed `OPEN`.** It asks for the stride between the banked
> records and notes *"one subtraction settles it once any second record's address is known"* — and
> the keymap page had both the subtraction (`01DF1738 = 01DF1480 + 2 × 0x15C`) and the answer
> (`5 × 0x15C`) written down. This pass adds a **third, independent derivation** — the loop's own
> increment, which needs no second address at all — and closes the question.

**Two consequences a reimplementation must not miss — and the second is not recorded anywhere
else:**

1. **The digital mask is an OR across banks, expressed as AND-NOT.** Any record whose bound code is
   active clears the bit. A later bank can never *restore* a bit an earlier one cleared.
2. **The axis bytes ACCUMULATE across banks.** The axis formula reads the byte it is about to write:

   ```c
   out = (v + 1.0) * 128.0 + ((float)currentByte - 128.0);
   ```

   The `− 128.0` exists precisely so that a byte still at the `0x80` neutral contributes nothing.
   Run over eleven records, **the contributions sum**. This is not an assignment, and treating it as
   one would silently drop every axis except the last bank's.

### 7a. How a profile is published — `00195DF0` read, `DD-1` answered

**This is the `0x70` → `0x15C` conversion**, and it is one function. Every global below is reached
through an **image-base register** (`lea r15, [rip - 0x75e23]` → `00120000`), which is why a
RIP-relative reference map cannot see any of it — see §14a.

```c
/* 00195DF0(Mgr *mgr) */
const uint8_t *src = 01F80F90 + 0x48;          /* rdi — profile 0, biased by +0x48 */
const uint8_t *end = 01F81128;                 /* r12 — exactly 3 profiles at stride 0x70 */
size_t off = 0;                                /* rsi — record offset, steps 0x15C */

do {
    uint8_t *rec = 01DF1738 + off;             /* rbx — records 2, 3, 4 of the bank */

    /* 1. group 0 — sixteen digital codes, 64 bytes, four SSE moves */
    memcpy(rec + 0x00, src - 0x48, 0x40);

    /* 2. two of them are FORCED TO ZERO, unconditionally */
    *(uint64_t *)(rec + 0x20) = 0;             /* digital slots 8 and 9 */

    /* 3. group 1's eight codes become FOUR mode-2 axis entries */
    for (k = 0; k < 4; k++)
        rec[0x40 + k*0x10] = (AxisEntry){ .mode = 2, .field04 = 4,
                                          .codeA = grp1[2*k], .codeB = grp1[2*k + 1] };

    /* 4. the platform pair swap */
    if (!InputBinding_ShouldKeepAuthoredPairOrderForPlatformState())
        swap(*(uint32_t *)(rec + 0x34), *(uint32_t *)(rec + 0x38));   /* digital slots 13, 14 */

    /* 5. publish the whole record */
    memcpy(01F80130 + off, rec, 0x15C);

    src += 0x70;  off += 0x15C;
} while (src < end);

mgr[0x3B] = 1;                                 /* the dirty flag 00196FF0 consumes */
```

**Five things a reimplementation would get wrong, and each is load-bearing:**

1. **`0x15C` is the copy length, derived here a fifth way** — `2 × 0x80` in the unrolled loop, then
   `0x50 + 8 + 4` in the tail. Not an inferred stride: an actual `memcpy` size.
2. **Exactly three profiles.** `(01F81128 − 01F80FD8) / 0x70 = 0x150 / 0x70 = 3`.
3. **Group 2 is never published.** The read span is `[src − 0x48, src + 0x17]` = 96 bytes = **24 of
   the profile's 28 dwords.** Dwords 24–27 — group 2, at `01F80FF0` — **never reach the runtime
   record.** They are authored and conflict-checked, and the translator never sees them. (The six
   slots read on demand through `00197710`, `BP-7`, are the obvious place they go; that is **not**
   verified here.)
4. **Digital slots 8 and 9 are zeroed after the copy**, so whatever the profile authored there is
   discarded at publish time.
5. **The pair swap is on the published record, not the authored profile** — slots 13 and 14 of
   `rec`, after the copy. The authored bytes are left alone.

**It writes records 2, 3 and 4** (`01DF1738 = 01DF1480 + 2 × 0x15C`), never 0 and 1. What records 0
and 1 hold remains open.

## 8. Script · resource · event interactions

`keymap.ini` lives at `<Documents>\My Games\FINAL FANTASY XII THE ZODIAC AGE\keymap.ini`; the file
format is fully derived in the keymap page. The platform pair swap (`BP-1`) exchanges **Circle and
Cross** and is driven by `01F82D20[+0x64]` via `001DFA70`.

## 9. Determinism

**Fully deterministic given the banks and the backend's device state.** No randomness on any path
here — this subsystem does not touch the generators in
[`21-RNG-And-Determinism`](../../21-RNG-And-Determinism/rng-streams.md).

The only order-dependence is the bank order in §7, which is fixed: A, then B, then C.

## 10. Failure paths and edge conditions

| condition | behaviour |
|---|---|
| `mgr[+0x39] == 0` | the whole poll is skipped; the caller's frame is **left untouched**, not zeroed |
| control codes `0`, `4`–`10` | matched by **no** band; never polled. `BP-5` asks why they exist |
| reserved id assigned | rejected, code `2`, nothing written |
| conflict, `allowReplace = false` | rejected, code `1`, **nothing written** |
| conflict, `allowReplace = true` | the old value moves to the conflicting slot — a **swap**, not an overwrite |
| `deviceMode == 1` on an axis | `v` forced to `0.0`; the axis still accumulates its `currentByte − 128` term |

```c
/* the exact exchange, from 00198A00 */
if (conflictingFlatIndex >= 0) {
    if (!allowReplace) return 1;
    bindings[conflictingFlatIndex] = target[slot];
}
target[slot] = newId;
return 0;
```

## 11. Observable behaviour

**Six of the 28 slots never appear in the mask at all.** `Speed1/2/3`, `WalkMode`, `L2` and `R2` are
read on demand through `00197710` (`BP-7`). A reimplementation that drove everything from the frame
would lose exactly those six.

**The array the backend fills is indexed by physical key, not by game action** — `index = code − 28`,
**measured**, not inferred (`EXP-006`, 18 keys, every one moved exactly one byte):

| key | index | code | binding name |
|---|---:|---:|---|
| Escape | 36 | 64 | Start |
| Space | 52 | 80 | Circle |
| Tab | 51 | 79 | L3 |
| LControl | 89 | 117 | R2 |
| LShift | 90 | 118 | WalkMode |

**The backend array is transition-written, not a per-frame snapshot.** Holding Escape sets index 36
to 1; overwriting it with 0 while still holding produced **fifteen polls over 300 ms with no
restore**. Anything that expects to re-read a level every frame is wrong.

## 12. Reproduction formula

```c
/* one record into the frame; run per §7's bank order */
void translate(const BindingRecord *r, Frame *f)
{
    for (int i = 0; i < 16; i++) {                    /* digital */
        int code = r->digital[i];
        if (!device_gate()) continue;                 /* DC-2: unread */
        int active;
        if      ((unsigned)(code - 11) < 17)  active = active_any_device(code);
        else if ((unsigned)(code - 28) < 125) active = active_for_bank(code, 0);
        else if ((unsigned)(code -  1) <  3)  active = active_primary(code);
        else continue;                                /* codes 0, 4..10: polled by nothing */
        if (active) f->mask[i >> 3] &= ~(1 << (i & 7));   /* CLEAR */
    }
    for (int i = 0; i < 16; i++) {                    /* axes */
        const AxisEntry *e = &r->axis[i];
        uint8_t cur = f->axis[i];
        switch (e->mode) {
        case 1:
            if (active_of(e->codeA)) f->axis[i] = 0xFF;
            break;
        case 2: {
            int a = cur;
            if (active_of(e->codeA)) a += invert ? +0x7F : -0x7F;
            if (active_of(e->codeB)) a += invert ? -0x80 : +0x80;
            f->axis[i] = (uint8_t)clamp(a, 0, 255);
            break;
        }
        case 3: {
            float v = filtered_axis(e->axisId);
            if (e->axisId == 2) { v = -v; if (invert_x) v = -v; }
            if (e->axisId == 3) { v = -v; if (invert_y) v = -v; }
            if (device_mode == 1) v = 0.0f;
            else if (v != 0.0f) stick_touched = 1;
            float out = (v + 1.0f) * 128.0f + ((float)cur - 128.0f);
            f->axis[i] = (uint8_t)clampf(out, 0.0f, 255.0f);
            break;
        }
        }
    }
}
```

**Mode 2 from the `0x80` neutral gives `1` for full negative and `255` for full positive** —
asymmetric by one, because the contributions are `−127` and `+128`, not `±127.5`. Stated as the code
computes it, not rounded.

*Which way `codeA` pushes, settled 2026-10-01 (OPUS, from the 15-Input reconstruction-readiness map's G-C3x, at the
bytes `0019750A`-`0019753E` and `001975BB`-`001975EF`): the `invert` above is per ENTRY, not one flag. Entry 0 uses the
input manager's byte `+0x08` (non-zero inverts; `0019751A`), entry 1 its `+0x09` (`0019752E`), entries 2 and 3 are
always inverted (`00197536`-`0019753C`), entries 4-15 never. So section 3.2's "`codeA` negative, `codeB` positive"
holds for entries 0 and 1 with those bytes clear and for entries 4-15, while in entries 2 and 3 - the LX and LY slots
of the shipped profiles (`UQ-143`) - `codeA` adds `+0x7F` and `codeB` `-0x80`. That is why the keyboard records list
"positive code, then negative" for D/A and S/W: D and S raise LX and LY. Which on-screen direction a low or high
right-stick value turns the camera is not established here.*

**Channel timing** (`0035F690`), thresholds `1790` / `1760` / `180`, accumulator ceiling `16384`,
rate `±546` at `+0x18`, added once per tick — `16384 / 546 ≈ 30` ticks to traverse the range:

```c
if (flags & 0x10) {                                   /* held */
    if (++holdTimer > 1759) rate = -546;
    if (holdTimer > 1790) {
        phaseCounter++; subCounter++;
        holdTimer = 1790; accumulator = 0; rate = 0;
        if (subCounter   >= 180) subCounter = 180;
        if (phaseCounter >= 180) { phaseCounter = 0; holdTimer = 0; rate = +546; subCounter = 0; }
    } else subCounter = 0;
} else {
    if (holdTimer > 0) { if (++holdTimer > 1790) holdTimer = 1790; }
    if (++subCounter >= 180) { holdTimer = 0; subCounter = 180; accumulator = 16384; rate = 0; }
}
accumulator = clamp(accumulator + rate, 0, 16384);    /* runs unconditionally */
```

## 13. Runtime validation

**The read path only.** [`EXP-005`](../../_experiments/EXP-005-driving-the-input-state.md) resolved
the chain in a live process:

```
[0x02EA5368] -> 0x01F7E350   the input manager
manager + 0xDF8 -> 0x01F7F150   the backend
backend + device*8 + 0x118 -> a HEAP block; it moves between launches
block + 0x30 + (code - 0x1C) -> one byte per input, non-zero means held
```

**Corrected 2026-09-13 (FABLE), statically.** `[0x02EA5368]` is the Phyre application object (constructor `00792350`); the
input manager is `[01F7FFE0]`. The block is `PFramework::PInputDeviceKeyboard`. `+0x30` is a transition latch: `0079D010`
writes it on a level change, and `0079AE90` / `0079AE40` clear it on consumption. The polled level is `+0x231`, written by
`007A1640`. See [the input-stack page](../Input-Stack/input-stack-device-channel-and-bindings.md), §2 *The keyboard byte array*.

**Delivery, and the zero that must not become a claim — 2026-09-13 (`ASTRA-RETURN-OPUS-INPUT-RECOVERY`).**
An earlier live capture at the title screen sampled the keyboard byte array during a Return call and
found **every byte zero**. *Read alone, that reads as "the array is not driven by injected keys," and
it must not.* ASTRA has since driven the game with a **350 ms dual-form** send and observed **Enter
(index 49) act at the title, at load selection, at dismissal and at the field-menu open, and C (index
2) open and close the menu** — PID `22784`, exact shipping image, full mapped `.text` matched, all 26
original saves restored. **So the earlier zero does not establish an unavailable keyboard — a later
send drove the game.** *Narrowed 2026-09-13 (`ASTRA-CONTRA-OPUS-INPUT-CAUSE`, accepted): an earlier
wording here said the first method was “too short”. **That asserts a cause nothing isolated.** The
350 ms dual-form send differs from the brief UI-API press in duration, in packet form and in API
path, and no single-variable comparison was run — so **why** the first attempt produced no bytes is
unknown. The positive establishes a working delivery route, not a duration law.*

**This changes nothing in §13 above**, and that is the point worth recording: everything here is the
**read path** — where held state lives and who latches it. ASTRA's result is about **delivery**, a
different question that happens to share a subsystem. **Still not shown** (ASTRA's own limits, kept):
the cause of one brief Return failure is unisolated; no combat command or action was executed; and no
scheduling or caller law is inferred from any of it.

Device 0 was the only non-null of seven at the title screen, which is what a machine with no gamepad
should look like. `EXP-006` then measured `index = code − 28` over 18 keys.

**Not validated:** assignment, the conflict swap, publication, the pair swap, the three-bank poll
order, and channel timing. **No experiment has driven `00198A00` or observed `01F80130` change.**

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**33 generated points: 24 KILLED · 1 SURVIVED · 5 EQUIVALENT · 0 NO_BUILD · 0 TIMEOUT · 3 INVALID. Verdict `FAIL_INCOMPLETE`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/binding_publish` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../../Reconstruction/MUTATION-CAMPAIGNS.md).

The single survivor is **kind A** and was already documented in the reconstruction's own header before this campaign ran: `BP_GROUP0_BYTES 0x40` → `0x41` puts the extra byte on `rec + 0x40`, which the first axis entry overwrites unconditionally. The three `INVALID` are the driver's buffer guard firing, as in `transform`.

## 14. Unresolved

| id | what |
|---|---|
| ~~`DD-1`~~ | **ANSWERED** — `00195DF0`, in full, §7a |
| ~~`DD-3`~~ | **ANSWERED** — `T-7` was right; the map was blind to image-base addressing, §14a |
| ~~`DC-2`~~ | *(Superseded: **ANSWERED 2026-09-14 (FABLE)**, register `DC-2` - statically the gate never closes: `001C1990` returns `[01F81268]`, whose one field is written once, `= 0`, by `001C1940`; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* the device gate `FUN_001C1990()[0] != 1 \|\| FUN_00228480()`, tested before **every** binding |
| ~~`DC-3`~~ | *(Superseded: **ANSWERED 2026-09-14 (FABLE)**, register `DC-3` - `120.0` is `WHEEL_DELTA` for the mouse-wheel binding mode 4; the load at `00197253` is hoisted and used at `00197383`; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* `008F3A28` = `120.0`, loaded every iteration and used on no path read |
| ~~`BP-3`~~ | *(Superseded: **ANSWERED 2026-09-12 (FABLE)**, register `BP-3` - the walk is over the `0x140` runtime record's axis entries; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* the `(kind, code)` walk in the second half of `00197160`, advancing 18 dwords |
| ~~`BP-4`~~ | *(Superseded: **ANSWERED 2026-09-12 (FABLE)**, register `BP-4` - it is the controller vibration gain, which `0035F590` applies to the motors; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* what the 0–16384 triangular accumulator **drives** |
| ~~`BP-5`~~ | *(Superseded: **CLOSED 2026-09-18 as `NO ADMISSIBLE SOURCE`** (proposed FABLE, signed OPUS), register `BP-5` - the shipped default profile binds none of them; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* why codes `0`, `4`–`10` exist but are polled by nothing |
| `AP-4` | ~~why `InputManager_*` and `InputControl_*` share no call edge~~ **answered 2026-09-13:** one pipeline through the bridge `00862670` → `001E09B0` → `00196FF0`, which fills `InputControl`'s buffer `022CB680` ([input stack §2](../Input-Stack/input-stack-device-channel-and-bindings.md)) |
| new | what `mgr[+0x39]`, `+0x3A` and `+0x3B` are. `+0x39` gates the poll, `+0x3A` bits 1 and 0\|2 gate banks B and C, `+0x3B` is cleared each poll — **their meaning is not established** |
| new | the `0x1C` bytes per record beyond the translator's `0x140` |
| ~~new~~ | *(Superseded: **ANSWERED 2026-09-26 (OPUS)**, register `AU-4` - the region is three blocks at stride `0x420`, each built by its own CRT initialiser before `main`; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* the three bank writers `0015BD30` / `0015C0D0` / `0015BF20`, none read |

### 14a. `DD-3` resolved — `T-7` was right, and the instrument was blind

The previous pass recorded a discrepancy: the static-initialization page's `T-7 RESOLVED` said
`00195DF0` builds profiles at `01DF1738 + i*0x15C` from `01F80F90` and copies `0x15C` bytes to
`01F80130`, while the RIP-relative reference map said `00195DF0` names **none** of those three.

**Reading the function settles it: `T-7` is correct in every particular.** §7a is that claim,
confirmed instruction by instruction.

**The map was not wrong; it was blind.** `00195DF0` does

```asm
00195E1C  lea r15, [rip - 0x75e23]              ; -> 00120000, the IMAGE BASE
00195E37  lea rbx, [r15 + 0x1cd1738]            ; -> 01DF1738
00195F2C  lea rax, [r15 + 0x1e60130]            ; -> 01F80130
```

— it materialises the image base once and addresses every global as `[base + disp]`. **A
RIP-relative scan sees exactly one thing: the `lea` of the base itself.** And that signal was in the
map's own output all along: `00195DF0`'s three references were `01F82D20`, `01F80FD8`, `01F81128`
**plus `00120000`** — the image base, sitting there, read as noise.

> **The lesson is not "the map is unreliable" but "an address-keyed reference map answers a question
> about *naming*, not about *touching*."** A conclusion of the form *"no function writes this"* is
> sound only for functions that name their globals RIP-relatively.

`imagebase_refs.py` now closes the gap. Measured across the image:

| | count | denominator |
|---|---:|---|
| functions using an image-base register | **636** | 38,161 (**1.67 %**) |
| references resolved | **2,027** | — |
| distinct globals reached | **1,054** | after dropping 124 indeterminate rows |
| **globals written here that the RIP map shows as having NO writer** | **103** | of 150 written via the base |
| **globals absent from the RIP map entirely** | **870** | of 1,054 |

## 15. Evidence

Static disassembly at the certified hash, RIP-relative targets computed with capstone (never by
hand), the global read/write map for writer sets, and two live experiments for §13. **`edges.tsv`
caller counts are not used anywhere in this contract**, so the funclet contamination class does not
apply.

**Claim table added 2026-09-12 (`OPUS-S15-CLAIM-TABLES`).** The paragraph above states the *method*
and is kept; what it did not do is enumerate the claims. Nothing here is new analysis — every row
points at something already argued in the body — but a harness cannot map to prose, and until this
table existed `diff_binding_publish.py` could not declare a `CONTRACT` verdict at all. 14 of the 33
contracts were in the same state.

| claim | evidence | tier | confidence |
|---|---|---|---|
| ten operations, their entries and their signatures | §2, each body disassembled at the certified hash | 1 (static, isolated original code) | PROVEN |
| the GFZ names two of these backwards | `00195DF0` is the publisher though annotated `RestoreDefaultBindingProfiles`; `00198B60` is the defaults-installer though annotated `MaterializeRuntimeBindingProfiles`. Binary over annotation | 1 (static, isolated original code) | PROVEN |
| `00195DF0` builds at `01DF1738 + i*0x15C` from `01F80F90` and copies `0x15C` to `01F80130` | §7a, instruction by instruction; `T-7` confirmed and the reference map shown blind to image-base addressing, §14a | 1 (isolated original-code) | PROVEN |
| `001DFA70` compares a DWORD, not a byte | the eight bytes are `83 79 64 00 / 0F 94 C0 / C3`. A one-byte test returns the wrong answer whenever `+0x65`..`+0x67` are non-zero, and the pair swap then runs backwards | 1 (isolated original-code) | PROVEN |
| flat index = `profile * 0x1C + slot + {0, 0x10, 0x18}` | §4; group 2's byte-stepped `profile * 0x70` is the same stride written differently | 1 (static, isolated original code) | PROVEN |
| the conflict scan is global, bound `flat <= 0x53` | §4 — all 84 slots across all three profiles, not per profile | 1 (static, isolated original code) | PROVEN |
| a pressed control CLEARS its bit | the mask's per-bit write is only ever `&= ~(1 << n)` — `btr eax, edx` / `mov byte [rcx+r14], al` at `0019723D`/`00197240` and `0019733F`/`00197342` in `00197160`; a byte of `0xFF` means nothing is held | 1 (static, isolated original code) | PROVEN |
| the 35 ids at `01DF13E0` can never be bound | the assigner refuses them with code `2` | 1 (static, isolated original code) | PROVEN  **§15a: 35 confirmed THREE independent ways** — the table holds exactly 35 dwords then a `0` terminator; the walk is bounded by a literal `00198ACF cmp edx, 0x23` (= 35); and the refusal is `00198B4D mov eax, 2` / `ret` |
| `00196FF0` does nothing unless `mgr[+0x39] != 0` | it branches straight to the epilogue | 1 (static, isolated original code) | PROVEN |
| `00198A00` returns 0, 1, 2 or 3 | §4's postcondition table | 1 (static, isolated original code) | PROVEN |
| the translator requires an already-initialised frame | a zeroed frame inverts the digital result and biases every axis by −128, §3.3 | 1 (static, isolated original code) | PROVEN |
| the read path resolves in a live process | `EXP-005` resolved the manager → backend → device block → per-input byte chain; `EXP-006` measured `index = code − 28` over 18 keys | 10 (live) | PROVEN |
| the assignment and publication paths in a live process | §13 — no experiment has driven `00198A00` or observed `01F80130` change | none | UNKNOWN |
| what the three banks ARE, and what `mgr[+0x39]`/`+0x3A`/`+0x3B` mean | §17 — their control-flow role is read; their meaning is not | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every claim checked reproduced, and the count claim reproduced **three separate ways** — which is
worth more than any one of them, because a count is where this sweep has found every other error.

### `001DFA70` is byte-exact

The contract quotes eight bytes. The image holds **`83 79 64 00 0F 94 C0 C3`** — `cmp dword ptr
[rcx+0x64], 0` / `sete al` / `ret`. **It is a DWORD compare**, as claimed; a one-byte test would read
only the low octet of that field.

### The 35 refusable ids, confirmed three ways

| route | result |
|---|---|
| the table at `01DF13E0`, decoded | **35 dwords** — `2, 81, 82, 84, 85, 88, 89, 90, 123, 119, 122, 130, 125, 131, 132, 133 … 152` — then a **`0` terminator** |
| the walk's own bound | `00198AC0 cmp r8d, [rax]` / `00198ACF cmp edx, 0x23` — a literal **35** |
| the refusal code | `00198B4D mov eax, 2` / `ret` — **code 2**, exactly as §15 says |

**The table's length, the loop's bound and the documented code agree.** Note the list is *not*
sorted — `123` precedes `119` and `130` precedes `125` — so a reader checking it as a range would
mis-sample it.

### The conflict scan is global, and its bound guards are SIGNED

`00196550 InputManager_ValidateBindingUniqueness` bounds the walk with **`cmp r8, 0x54`** twice —
`0019658F` with `jge` and `001965C1` with `jl` — so the flat index runs `0`–`0x53`, **84 slots across
all three profiles**, exactly as §4 has it. `00196663 cmp edx, 0x1c` carries the per-profile slot
count of **28**, and `3 × 28 = 84` closes the arithmetic.

> **New detail: those two guards are `jge`/`jl`, signed.** The counter starts at zero and only
> increments, so signedness changes nothing here — but this database is careful elsewhere about
> exactly this distinction (the reward award's four guards turn on it), so it is recorded rather
> than left for a later reader to rediscover and wonder about.

**Not claimed:** no live observation — `EXP-005` resolved the *read* path in a live process, and §15
already says the assignment and publication paths have never been driven. That stands unchanged.

## 16. Parity plan

**First pilot operation: `translate()` for mode 2 and the digital mask** — it is pure, takes a record
and a frame, touches no globals but the invert flags, and has an exactly stated asymmetry (`1` and
`255`) that a careless reimplementation gets wrong. A differential harness can plant records
directly and compare all 18 bytes.

**Boundary cases that must actually distinguish something** — the recurring failure in this program
has been boundary cases whose *verdict* does not depend on the boundary:

- both `codeA` and `codeB` active at once (contributions `−0x7F` and `+0x80` sum to `+1`, not 0)
- an axis already displaced by an earlier bank, to prove accumulation rather than assignment
- a record where every code is in the `4`–`10` dead band, which must leave the frame untouched
- the mask with all sixteen slots active, which must produce `0x0000`, not `0xFFFF`

### Status — `00195DF0` is IMPLEMENTED and DIFFERENTIAL TESTED, 2026-09-08

**The publish path is reconstructed and compared against the shipped bytes.**
`Reconstruction/Game/Input/binding_publish.c`, driven by
`Reconstruction/Tests/Differential/diff_binding_publish.py`.

| | |
|---|---|
| cases | **42** — 2 designed, 40 randomised over every authored dword and every record byte |
| compared | the 3 runtime records, the 3 published records, the dirty flag — **byte for byte** |
| also compared | **every mapped byte outside those regions**, laid over a sentinel fill |
| mismatches | **0** |
| mutation score | **27 of 28 (96 %)**, 2 provably equivalent and excluded |

`001DFA70` is **not stubbed** — it is eight bytes and a leaf, so it is mapped and executed, and the
pair-order decision is the shipped one.

**The one surviving mutant is a real equivalence, not a gap:** `BP_GROUP0_BYTES` `0x40 → 0x41`
writes one extra byte at `rec + 0x40`, which the first axis entry overwrites unconditionally. No
input makes it observable, and **no case was contrived to "kill" it**.

**Still `CONTRACT READY` as a subsystem, not `RECONSTRUCTION READY`.** One operation of the write
path is done; assignment (`00198A00`) and the translator (`00197160`) are not, and nothing here has
been observed in a live process.

**The original §16 plan's first pilot was `translate()`.** It was set aside for this one because
`translate` computes a value while **`00195DF0` mutates shared state**, which is the gap the program
actually had.

## 17. What this contract does not establish

- ~~**That the three banks are keyboard / pad / something else.**~~ *(Superseded: register `UQ-143`, narrowed 2026-09-18 and 2026-09-25 (FABLE) - bank A's records 0 and 1 are the gamepad and mouse profiles, 2-4 the three keyboard layouts, and the two conditional banks follow system-stop slots: the battle-menu bank and the menu / cutscene-lock bank; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* The prose page calls `01DF1738`
  "live keyboard profile records"; this contract does not confirm what any bank *is*.
- **What `mgr[+0x39]`/`+0x3A`/`+0x3B` mean.** Their control-flow role is read; their meaning is not.
- **Anything about the assignment path in a live process.** §13 covers reading only.
- **That eleven is the maximum.** Eleven is what `00196FF0` runs; no other caller of `00197160` was
  enumerated.
- ~~**Where group 2's four slots are consumed.**~~ *(Superseded: `00197710` is their read surface - the keymap page's "Where the file's bindings are actually read" section; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* They are authored, conflict-checked, and **never
  published**; `00197710` is the obvious candidate and was not read.
- ~~**What records 0 and 1 of the bank at `01DF1480` hold.**~~ *(Superseded: register `UQ-143` - the gamepad and the mouse profiles; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* The publisher writes only 2, 3 and 4.
- **Why digital slots 8 and 9 are zeroed**, or what the authored profile puts there.
- ~~**What the axis entry's `+0x04` field means.**~~ *(Superseded: **ANSWERED 2026-09-18 (FABLE)**, register `UQ-144` - the fields are `{kind, subKind, codeA, codeB}`, and the 4 is a sub-kind only the mouse kind reads; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* The publisher writes the literal `4` into all four
  entries; the translator uses that field only in mode 3, and these are mode 2.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Presentation — CLIENT (SWE2-CONTRACT 2026-09-15, 2 edges, R5-visible).** `001C1990`, cited on this
page, is called by two Presentation bodies, `00187950` and `001BDAC0` — the render layer consults
the same profile helper the binding translation uses. Visible only once `0x`/`FUN_` citations
count.

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 1 edge).** The just-cited `00187950` calls Audio
helper `00182E80` — fan-in imported by the Presentation note, not a binding-layer relationship.
`00182E80` resolves a singleton through `001DDAB0` and **fails open**: a null resolution returns the
literal `0x438` and does nothing else, otherwise it tail-jumps to `002256A0` with the resolved
pointer (OPUS, read from the shipping bytes).

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 3 edges, R5-imported).** The cited
Presentation bodies pull scheduling helpers: `00187950` calls `001A1470` — a buffer capacity check
that rounds the request **down** to a multiple of 16 then adds `0x10` back before comparing against
the object's span — and `001BDAC0` calls `0017D980` (two instructions: `mov eax, [01F7F4B8]` /
`ret`, a plain global read) and is itself reached from `0017D6E0`, a float routine that first tests
the counter at `[01FD4A68]` and whose own callers include a developer-console body (one further hop
of the same fan-in; bodies read by OPUS from the shipping bytes). None of this is a binding-layer
relationship.

**PlatformOnlineAchievements - MECHANICAL (SWE2-EC7-173, 1 edge).** The batch-138 `00196EE0`
section names `00796E20`, the shared context getter whose callers include `008655A0`. Fan-in the
helper carries, not an achievements relationship the profiles layer owns.

**Resource - MECHANICAL (SWE2-EC7-173, 2 edges).** `0017D6E0` calls `001A1220`, and `00796E20`
counts `001A7A50` among its callers - the same shared-helper fan-in, not a resource relationship.

**UI - MECHANICAL (SWE2-EC7-173, 3 edges).** `001A1470` and `00796E20` count `0018EEE0` among their
callers and `00228480` counts `00276D30` - the UI layer consulting shared helpers this page happens
to cite, not a UI relationship the profiles layer owns.

**Save_Load_Settings - MECHANICAL (SWE2-EC7-173, 3 edges).** `0017D6E0` calls `001C18E0` and
`001C1910`, and `001A1220` is reached from `001C1810` - the same float/helper fan-in spilling into
the save/settings layer, not a save relationship the profiles layer owns.
- **Application - CLIENT (1 edge).** `00792350` is also called by bodies filed to application: `0015BC40` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT (1 edge).** `00228480` is also called by bodies filed to world area: `00314020` - shared machinery across the layer boundary, no shared ownership.
## SWE2-EC7-79 update (2026-09-20) - `005DBF80` two-field zero ctor measured

`005DBF80` (13 B) is the minimal ctor the binding callers use:
`[rcx]` and `[rcx+8]` are zeroed and `rcx` returns - an
eight-byte-pair initialiser.
Interior anchor `005DBF85` (the `+8` zero).

`00196EE0` (260 B) is the descriptor-table init the `00196FF0` frame poll is built on: three `0x70`-stride rows of `01F80FEC`..`01F8113C` each build a `0x15C` record at `01F80970` - zeroed head, six staged dwords from the row's `+0`/`-0xC`/`-4`/`-8`/`-0x3C`/`-0x38` - then register four fields each through `00796E20`'s `+0xDF8` context and `0079AE90(ctx, field, 0)` - the fixed three-entry publish the per-frame poll consumes.

Interior anchor `00196F5D` (function `00196EE0`).

`00196DF0` (231 B) is the binding-table expansion `00196FF0` installs: it walks the compact `01F80FE0` records (`0x70` stride, bounded by `01F81130`), writes each `0x15C`-stride runtime record at `01F80550` (16 bytes zeroed, the record's four dwords, 32 bytes zeroed), then posts the four dwords one at a time through `00796E20` + `0079AE90` on the `+0xDF8` object

Interior anchor `00196E76` (function `00196DF0`).
