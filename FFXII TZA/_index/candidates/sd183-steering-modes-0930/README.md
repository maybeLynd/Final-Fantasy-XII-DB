# SD-183: steering modes 1/4, 2 and 6, and the code that writes the mode bits (SWE2-ORACLE, 2026-09-30)

Register row SD-183 (SWE2-DATA, DD batch 5, `b92561451`) sits on
[battle-locomotion-steering-and-recovery.md](../../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
section 6. It asks two things:

- what steering modes 1 / 4 (`0033CEF0`), 2 (`0033D200`) and 6 (`0033BAA0`) compute: the limited facing `ctx+0xBC`,
  the move heading `ctx+0xB4`, and `+0xB0` / `+0xB8`;
- which code writes the mode bits, the low five bits of `dword[[ctx+0x100]]`.

Modes 3 and 5 are already on the page (AM-7).

Sub-package `SWE2-ORACLE-SD182-184-0930` under OPUS's parent claim `OPUS-SD180-193-0930`.

| file | evidence class | result |
|---|---|---|
| `sd183_steering_modes.py` → `.out` | **static** (S1–S13), **executed** (E1–E5), **model** (M, compared inside E1/E2) | `FAILS 0` |
| `emu.py`, `img.py` | the unicorn harness and the image reader | — |

## The answer (SWE2-ORACLE)

### Where the mode lives, and when it runs

- **The flag word is `dword[st+0]` = `BattleUnit +0x80`** (S2). `BuildSolverContext` stores `st` at both `ctx+0x100`
  and `ctx+0x108`.
  - Bits 0–4 are the mode.
  - Bits 5–14 are a countdown.
  - Bit 15 is mode 6's orbit direction.
- **The dispatcher `00339F00` runs only while the countdown is non-zero.** Its one caller, `SolveDefaultStep`, tests
  `0x7FE0` first (`0033BF47`). With the countdown at zero, the unit takes the ordinary spacing and avoidance step instead.
- **The dispatcher's steps (S1, S3):**
  - Its desired heading is `004687F0`'s yaw toward the goal `st+4 / +8 / +0xC`.
  - After the mode body, the countdown is cleared once `ctx+0xB0` exceeds the XZ distance to the goal; otherwise it is
    decremented. **A mode is a steering override with a lifetime.**

### Mode 1 and mode 4, `0033CEF0`: turn toward the goal, move inside a cone

Executed on seven fixtures (E1), and the reading below predicts every output.

- **The turn rate.** It is `st+0xE4` while `ctx+0xB0 > 0` and `ctx+0xB0 > st+0x104`, else `st+0xE8`.
  - Near alignment it eases. With `d = |wrap(ctx+0xBC − desired)| < π/3`, the rate is
    `½(1 − cos 3d)·(rate − 1°) + 1°`, where 1° = `008C5F68`.
  - It falls to 1° per step as `d → 0` (S11).
- **Far from the goal.** "Far" means the XZ distance exceeds `(d / st+0xE8) · st+0xF8`: the distance covered while
  turning, taken as 30 steps when `st+0xE8 = 0`.
  - `ctx+0xBC` = `st+0xE0` turned toward the desired heading by at most the rate. It is the desired heading itself
    (raw) when that is within one step.
  - `ctx+0xB4` = `ctx+0xBC` clamped into the cone **desired ± `st+0x118`**. So the unit moves along its facing only
    while that facing is within `st+0x118` of the desired heading, and along the cone's edge otherwise.
- **Near the goal.**
  - `ctx+0xB4` = the desired heading.
  - `ctx+0xBC` = `st+0xE0` unchanged while the distance is under `st+0xFC`, otherwise the same bounded turn.
- **The countdown.** With the countdown at zero, it re-arms at 6. It re-arms at 5 instead when three things hold:
  - `0030C0D0` returns non-zero. That is `00253B90`, `flag 01E0C2B8 == 0`, which the force-fight page reads as force
    fight mode **off**.
  - The unit is party kind.
  - Its order is `0x4022`.
- **`ctx+0xB0` / `+0xB8` are not written** by this body.
- **Modes 1 and 4 are indistinguishable at run time.** The only code that compares the five bits is the dispatcher
  and `003343D0`'s "already mode 6" guard (S13). The two labels differ only in who set them (below).

### Mode 2, `0033D200`: turn, or give way to the turning circle

Executed on five fixtures (E2). The turning-circle test `00334220` ran its shipped bytes.

- **With the countdown at zero,** `00334220` builds two turning circles:
  - the radius is `max(2π/st+0xE8 · st+0xF8, 2π/st+0xE4 · st+0xFC) / 2π`;
  - the centres sit at ±90° of `ctx+0xBC`.

  If the goal lies inside either circle, the goal cannot be reached by turning while moving forward. The body then
  sets `ctx+0xBC` = the bounded turn and `ctx+0xB4` = the desired heading, and **returns 5** without arming the
  countdown (S7).
- **Otherwise:**
  - The rate scales by `(80·d/(π/4) + 20)` % when `d < π/4`.
  - More than 5 × `st+0xF8` from the goal: **both `ctx+0xBC` and `ctx+0xB4` get the turned heading** (`0033D385`
    overwrites `xmm6`). Within one step, both get the desired heading raw.
  - Within 5 steps of the goal: `ctx+0xBC` holds `st+0xE0` and `ctx+0xB4` = desired.
  - The countdown arms at **10** if it was zero, and the body **returns 2**.
- **`0033D3B9` is a countdown arm, not a mode transition.** `and 0xFFFF815F` / `or 0x140` keeps bits 0–4 (S12).

### Mode 6, `0033BAA0`: orbit a point

Executed with two stubs (E3, E4), listed under Limits.

- **The step.** `00334AB0` turns the vector from the orbit centre `ctx+0x40` to the unit by one arc step,
  `a = st+0xF8 / (2π r) · 2π`.
  - `a` is negated when bit 15 is set.
  - The radius eases toward `st+4` over the remaining countdown.
  - The result is the chord's yaw. It is 0 when the speed exceeds the circumference.
- **When the forward step is clear and no actor pair blocks** (`00335B60 ≠ 0`, `0033D660 = 0`), the orbit ends: the
  countdown and `ctx+0xB0` are cleared and the mode bits are kept.
- **Otherwise the body writes:**
  - `ctx+0xB4` = the chord heading;
  - `ctx+0xB8` = 0, or ±π/2 when `0033BC80` sees a height change of at least 0.3 for a `placementMode 3` unit, in which
    case `ctx+0xB0` = `st+0xE8`;
  - `ctx+0xB0` = `st+0xF8`;
  - `ctx+0xBC` = `ctx+0xBC` turned toward `ctx+0xA8` by 1.5 × the arc angle. `ctx+0xA8` is `BuildSolverContext`'s yaw
    toward the locomotion target.

### Who writes the mode bits

A census of every dword store through `st = [ctx+0x100 / 0x108]` in `00330000`–`00341FFF` finds 24 stores (S10). Only
four change bits 0–4.

| writer | what it sets | when |
|---|---|---|
| `0033CC80` (`0033CD7F`, xor-insert) | the goal `st+4 / +8 / +0xC` = position + dist × direction(yaw, pitch), and **mode = its argument** | only from `0033A720`, the obstacle-avoidance direction search (S5) |
| — from `0033B156` | **mode 4** | the candidate loop found no direction; `0033CEF0` ran on the base heading |
| — from `0033B582` | **mode 1, 2, 3 or 5** | the chooser `00339DF0` returns 3.0 (turn in place: \|candidate − `st+0xE0`\| above the row's first angle), or 1 / 2 from the 48-row table `01EED4C0` (S6). A 2 becomes 1 when the forward step is clear, or `0033D200`'s return (2 or 5) otherwise |
| `003343D0` (`003346CD` / `003346D4`) | **mode 6**; bit 15 = rand & 1; countdown = `st+0x12C` / arc step, halved when `0031EA90 == 4`; `st+4` = orbit radius ± (rand % 5 + 5)/100 | `TryStartRandomizedAvoidanceManeuver` (S8) |
| `0033E1F0` (`0033E272`) | **mode 0**, countdown 0 | `ResetAvoidanceStateRandomized` (S9) |

- The other 20 stores preserve bits 0–4: countdown arms and clears, and bit-15 flips.
- The unit-reuse reset zeroes the whole word with the rest of `unit+0x80…` (the field map, `00236B12`).
- The chooser's table row is `profile · 6 + (st+0x170 bit 3 clear ? 3 : 0) + speed band`. The profile is
  `st+0x175`, the `@FCP` slot-40 byte, and values of 8 or more use row set 1.

## What changes on the page, for SWE2-DATA (SWE2-ORACLE)

- **Section 6: SD-183 answered.**
  - Replace "no writer of the low five bits is traced" with the table above.
  - Add the countdown gate (`0033BF47`).
  - Record that 1 and 4 share a body and are told apart by nothing.
- **"`0033D200` writes the order word = a mode transition"** (OPUS's brief wording) is wrong: `0033D3B9` arms the
  countdown and keeps the mode.

## Evidence classes, kept separate (SWE2-ORACLE)

- **Static (S1–S13):** decoded instructions and the image's constant table `01EED4C0`.
  - The store census (S10) follows `st` loaded from `ctx+0x100/0x108` inside the solver band.
  - The reader census (S13) covers `and 0x1F; cmp` in `00300000`–`00344FFF`.
- **Executed (E1–E5):** unicorn runs of the shipped bodies.
  - **Fixtures:** a zero-filled context and state with the listed fields set, and `ctx+0x100 = ctx+0x108 = &st`.
  - **Injected globals:** `0208E6A0 = 0`, so `00236820` returns null; `01E0C2B8 = 1`.
  - **IAT thunks answered in Python** (float32): `cosf`, `sinf`, `sqrtf`.
  - **Stubs, `0033BAA0` only:** `00335B60` returns 0 (orbit) or 1 (end); `0033D660` returns 0.
  - Every other callee ran its shipped bytes.
- **Model (inside E1 / E2):** a Python transcription of the reading. **Agreement with the execution shows the reading
  predicts these fixtures; it is not independent evidence.** The execution corrected the reading once: mode 2's
  `ctx+0xB4` on the turning path is the turned heading, not the desired one.
- **Control from the documents (E5):** executed `0033CE60` reproduces the page's AM-7 description of mode 3. The speed
  is zeroed, B4 = BC = the slow-rate turn, the countdown arms at 10 and clears on arrival.

## Limits (SWE2-ORACLE)

- **The stubbed clearance tests.** Mode 6's clearance tests (`00335B60`, a nav-mesh probe, and `0033D660`) were not
  executed. Which of the two branches a real unit takes depends on geometry the fixtures do not model.
- **The unexecuted helpers.** `0033BC80`'s height branch is read, not executed. `ctx+0xA8` came from the fixture (0),
  not from `BuildSolverContext`.
- **The `0033CEF0` countdown.** The re-arm value 5 needs a live party unit with order `0x4022`. The fixture's null unit
  exercised only the 6 branch.
- **The mode-5 path.** `0033D200`'s 5-return does not arm the countdown. A mode 5 written by `0033CC80` runs only while
  an earlier countdown is still running. The consequence is read, not observed.
- **The census bounds.** The store census is bounded to st loaded from a solver context and to the solver band. `st`
  reached as `unit+0x80` elsewhere (`002FDC30`, `00325BB0`, `00304850`, `003105D0`, `003291B0`) was read for `+0`
  stores and has none. A write through an unrelated alias is not excluded.
- **Not asked.** What the chooser's table rows mean per profile (design intent) is not asked here.

## Review and routing (SWE2-ORACLE)

- Review: `ORACLE-REQ-AUDITSPEC-SD183-0930` (SWE2-AUDIT-SPEC).
- Row restatement: `ORACLE-REQ-DATA-SD183-ROW-0930` (SWE2-DATA). The register row and the page are not edited here.
