---
experiment: EXP-073
title: facing reapply composition and angle-helper comparison
status: COMPLETE - bounded isolated original-code evidence
contract: none - Reapply 002E5F90 and helper 0033CB70 are different from the facing-and-steering contract entry set; equivalence to those entries is not established.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original reapply and writer twice on the same state with three callback stubs; separate original angle helper has no stubs.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-073-facing-reapply-comparison/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-073: facing reapply composition and angle-helper comparison

**Result:** 20 paired controls and three additional wrapper controls passed on
first execution; two private mutations were detected. ASTRA, 2026-09-11. Offline
original-code execution; no live game process or native downstream transforms.

## Question and method

At experiment design, [K-6](../06-Movement-And-Navigation/heading-speed-to-position-delta.md) said that
the facing writer computes the same result as `0033CB70` and that reapplying
through `002E5F90` sets nothing new. [EXP-072](EXP-072-facing-writer-controls.md)
already found writer rounding and endpoint changes. This experiment executes
the original reapply wrapper and compares the two actual calculations.

The [checker](evidence/EXP-073-facing-reapply-comparison/check.py) verifies the
reference EXE SHA-256 and executes the 26-byte wrapper `002E5F90` plus the original
374-byte writer `002E5E10`. Each fixture calls the wrapper **twice without
reinitializing actor, state, controller or node memory between calls**. Only
caller registers, MXCSR and the synthetic stack return address are reset.
The second call reads the facing stored by the first. Initial field A8 and the
wrapper's auxiliary float input deliberately differ.

The writer's three downstream targets remain the same explicit recording RET
stubs as EXP-072, clobbering volatile integer registers and XMM0–5. Expected
write and callback streams span both calls. Every phase checks its stored angle,
STOP return, RSP+8 and all eight nonvolatile integer/full XMM6–15 registers;
the aggregate oracle checks exact event order/arguments, full fixture and
constant pages, and final EAX machine state. It does not infer a semantic return.

Each paired control separately executes all 128 bytes of `0033CB70` from the
same original input angle in a fresh fixture, with no stubs. It checks the low
XMM0 result bits, near/far branch selection, no memory writes, constant pages,
return boundary, stack and nonvolatile registers. Arithmetic oracles round each
operation to binary32. MXCSR starts at `1F80`; exception flags are not a parity
claim. The tested source uses Unicorn 2.1.4 and Capstone 5.0.7.

[Raw results](evidence/EXP-073-facing-reapply-comparison/result.json) contain
every phase, expected and observed events, reads, visited instruction addresses,
helper results and mutation verdicts. Original bodies/constants, complete
[disassembly](evidence/EXP-073-facing-reapply-comparison/disassembly.txt) and
source identities are sealed in the
[manifest](evidence/EXP-073-facing-reapply-comparison/manifest.json).

Reproduce from the shared repository root with the existing analysis runtime:

```powershell
& '.\Collaboration\Tools\analysis\venv\Scripts\python.exe' 'Database/FFXII TZA/_experiments/evidence/EXP-073-facing-reapply-comparison/check.py'
```

## What the wrapper actually forwards

The complete wrapper ends in a tail jump, not a call/return pair:

| Instruction | Effect |
|---|---|
| `002E5F90` | RAX = actor+B8 movement-state pointer |
| `002E5F97` | XMM2 = XMM1, forwarding the wrapper's auxiliary float input |
| `002E5F9A` | R9D = R8D, forwarding its third integer input |
| `002E5F9D` | XMM1 low dword = state+A8, the current facing |
| `002E5FA5` | JMP `002E5E10` |

Its input positions are therefore actor in RCX, auxiliary float in XMM1, and
integer flag in R8D. It takes the angle from state and supplies four positions
to the writer. The controlled 17.25 auxiliary value and flag 2 reach the writer's
field AC and final callback, whose fifth argument is 1. The FFFF handle reaches
that callback as 65535. With a null controller both calls preserve the original
facing and auxiliary sentinel and issue no callbacks. A present controller with
flag 20, no node and sentinel handle issues just one transform stub per call.

## The computations are not interchangeable

Representative exact bits from paired original execution follow. All rows use
a present controller. W1 and W2 are the first and second wrapper outputs; H is
the separate helper applied once to the original input.

| Original input | W1 | W2 | H |
|---|---|---|---|
| `3F800000` (+1) | `3F800002` | `3F800002` | `3F800000` |
| `BF800000` (-1) | `BF800002` | `BF800002` | `BF800000` |
| `00000000` | `00000000` | `00000000` | `00000000` |
| `80000000` (-0) | `00000000` | `00000000` | `80000000` |
| `40490FDA` (below pi) | `40490FD9` | `40490FD9` | `40490FDA` |
| `40490FDB` (+pi) | `C0490FDB` | `40490FDB` | `40490FDB` |
| `40490FDC` (above pi) | `C0490FD9` | `C0490FD9` | `C0490FDA` |
| `C0490FDB` (-pi) | `40490FDB` | `C0490FDB` | `C0490FDB` |
| `40C90FDB` (+two pi) | `B4800000` | `B4800000` | `00000000` |
| `C0C90FDB` (-two pi) | `34800000` | `34800000` | `00000000` |
| `41490FDA` (below four pi) | `B5400000` | `B5400000` | `B5800000` |
| `41490FDB` (+four pi) | `34800000` | `34800000` | `00000000` |
| `41490FDC` (above four pi) | `35A00000` | `35A00000` | `35800000` |
| `C1490FDC` (beyond negative four pi) | `B5A00000` | `B5A00000` | `B5800000` |
| `418A3AE7` (about +5.5pi) | `BFC90FD6` | `BFC90FD6` | `4096CBE6` |
| `C18A3AE7` (about -5.5pi) | `3FC90FD6` | `3FC90FD6` | `C096CBE6` |
| `60AD78EC` (about +1e20) | unchanged | unchanged | unchanged |
| `E0AD78EC` (about -1e20) | unchanged | unchanged | unchanged |
| `7F800000` (+infinity) | unchanged | unchanged | unchanged |
| `7FC12345` (quiet NaN) | unchanged | unchanged | unchanged |

**Reapply is not an identity operation:** pi changes sign on each of the two
calls, and input 1 changes on the first call. This does not establish an
observable visual difference between pi and negative pi. The helper preserves
the exact pi endpoints and small inputs instead. Replacing either calculation
with the other changes tested outputs even within the ordinary small-angle
range.

The helper's exact four-pi input stays on the near path; the adjacent larger
float takes the far path. Its far path uses signed 32-bit CVTTSS2SI, not a
general-purpose mathematical fmod. For +/-5.5pi the helper returns magnitude
about 4.712389, outside the pi interval; the wrapper produces about the opposite
signed 1.570796. For the tested +/-1e20, the conversion is invalid and the
helper also leaves the enormous finite value unchanged. Thus the maths page's
then-unqualified far-path `(-two pi, two pi)` bound is false. Quiet NaN follows the
helper's near path and is returned, so an unconditional near-path interval
guarantee also needs an input qualification.

## Falsification and limits

The wrapper mutant changes its field displacement A8 to AC at `002E5FA1`,
reading the auxiliary field as an angle. Both calls return normally and preserve
stack/registers, but phase angles, write/callback events and final pages disagree.
The helper mutant changes JBE to JB at `0033CB94`, making exact positive pi enter
the subtraction loop. It returns normally with no writes and correct stack and
registers, but returns negative pi instead of positive pi. Both defects are
detected on first execution. Original sealed bytes remain unchanged.

This provides local composition and calculation evidence for the
[facing page](../06-Movement-And-Navigation/heading-speed-to-position-delta.md)
and [maths page](../24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md).
It does not establish the live input distribution or support the maths page's
claim that normal play never reaches the far-path issue. Native transform effects,
actor lifetime, timing, movement parity, all floating-point inputs and other
normalizers remain outside this experiment. Runtime automation remains paused.

## Publication recovery — 2026-09-12

Execution and source/results review occurred before ASTRA's usage pause. Recovery verified every
manifest hash unchanged; these completed controls were not rerun. During the pause FABLE corrected
K-6 in `2f419ae` and qualified the maths page in `e307fa1`, using the available evidence. Those
changes are preserved. This publication supplies the durable original execution receipts; it does
not claim that the old wording is still active. The exact scope of the later maths qualification
needs its own boundary check: observing unchanged +/-1e20 does not prove every value beyond the
signed-conversion threshold is returned unchanged.
