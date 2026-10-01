---
experiment: EXP-071
title: native procedural initialization followed by a draw
status: COMPLETE - bounded isolated original-code evidence
contract: none - Procedural initialization and draws are outside the LCG/MT gameplay-generators contract; native startup dependencies are omitted.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original initializer then original draw on the same memory; preparation and tail stubs plus labeled early/tail interventions.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-071-procedural-rng-init/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-071: native procedural initialization followed by a draw

**Result:** nine controls passed on first execution; a disabled-initialization
mutation was detected. ASTRA, 2026-09-11. Offline original-code composition with
explicit downstream stubs; no live game access.

## Question and method

[EXP-070](EXP-070-procedural-rng-controls.md) tested the procedural draw from a
synthetic seed. Here the original initializer supplies the seed and mode to the
original draw, establishing the local setup-to-use path without injecting the
expected seed between phases.

The [checker](evidence/EXP-071-procedural-rng-init/check.py) verifies the reference
EXE hash, executes all 179 bytes of `00259180`, then executes either the original
bounded helper `003A6E60` or one-step helper `004005E0` in the same memory fixture.
All 21 preparation calls and the final tail destination `0036C140` are recording
RET stubs. They clobber volatile integer and XMM0–5 registers; no native work by
these callees is inferred. The draw helpers have no stubs.

The original initializer constants at `008C5F6C` and `008C5F78` are checked as
binary32 0.10000000149011612 and 1000.0. Reused draw bodies/constants are retained
with [raw results](evidence/EXP-071-procedural-rng-init/result.json), full
[disassembly](evidence/EXP-071-procedural-rng-init/disassembly.txt), and the exact
source/byte [manifest](evidence/EXP-071-procedural-rng-init/manifest.json).

## Native initialization order

The first callback is `0036C1D0(8, 10)`. The remaining preparation sequence is
recorded exactly in the checker and raw events. Two later argument boundaries
are explicit: `003CBFF0` receives RCX `02096ED0`, and `0025A600` receives XMM0
bits `3DCCCCCD` and XMM1 bits `447A0000`. Other argument contracts are not claimed.

Only after these 21 calls return does the original body perform three dword
writes, in this order:

| instruction | destination | value |
|---|---|---|
| `0025920C` | scratch `022D92E0` | `458DC800` |
| `00259216` | recurrence state `01EF93E8` | `458DC800` |
| `00259220` | mode `022D9138` | 1 |

The function restores its stack and **tail-jumps** to `0036C140`, whose entry sees
all three values. Thus these writes are late in this caller, but they are not
the last possible native startup effects: the real tail destination is excluded.
The caller's return EAX follows the tail stub's configured return, tested at zero
and `FFFFFFFF`; a fixed success value is not established.

## Composition and interventions

After the initializer returns, the harness re-establishes only the caller's
registers, return address, stack pointer and controlled MXCSR for the draw.
State/mode/scratch remain as produced. Both cold state and prior state `FFFFFFFF`
with mode 2 are replaced by the same native seed/mode. First bounded draw at
bound 100 returns **44** and leaves state `3FE4000D`; first one-step draw leaves
`3F9B9000` and returns float bits `3E5C8000`.

Two labeled interventions distinguish which boundary determines final state:

- The first preparation stub writes recurrence state `DEADBEEF` and mode 9.
  Later preparation entries observe those values; the caller's three native
  writes overwrite them. The first draw still returns 44.
- The tail stub changes mode to zero **after** seeing the native seed and mode 1.
  The next draw returns zero and leaves seed `458DC800` unchanged. This tests
  the boundary; it does not claim the real tail callee makes that write.

Bound zero still consumes seven enabled steps. Bound -100 returns -44; bound
1,000,000,000 returns 445,312,896 using EXP-070's exact binary32 operation order.
These are original draws from native initialization, not values supplied by stubs.

## Validation, mutation and limits

Nine fixtures cover cold/dirty input state, alternate stub return, early and tail
interventions, zero/negative/rounding-sensitive bounds, and the one-step helper.
Each initializer and draw must reach its expected return boundary and preserve
RSP plus eight nonvolatile integer registers. Exact ordered callback identities,
tested argument bits, callback state snapshots, native write instructions and
bytes, labeled interventions, full draw returns, and complete relevant fixture
pages are compared. Reads and visited instructions are retained. The recorder
checks all 16 bytes of SIMD scratch stores, using the EXP-070 method.

A private mutation changes the initializer's mode-store immediate from 1 to 0
at `00259226`. Both bodies still return normally, but the tail snapshot and
initialization page differ; the bounded draw returns zero and does not advance
the seed. The event, return and memory oracles reject it. No EXE is modified.

This establishes the initializer's local write order and its composition with
the draw under the listed stubs. Native preparation/tail effects, who calls the
initializer, live initialization timing, and other consumers of shared scratch
remain outside the experiment. These limits prevent promotion to full startup
or deterministic rendering parity.
