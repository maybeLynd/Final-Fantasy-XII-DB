---
experiment: EXP-070
title: procedural RNG steps, scratch writes and exact rounding
status: COMPLETE - bounded isolated original-code evidence
contract: ../02-Resource-And-Asset-Pipeline/Authored-Expressions/CONTRACT-authored-expression-evaluation.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Two complete original procedural RNG helpers, synthetic state and controlled MXCSR, no stubs; failed fixtures and rounding corrections preserved.
contract_coverage: Bounded isolated evidence for the procedural helpers' rounding, seven-step cost, mode behaviour and scratch writes; not the full expression evaluator, initialization, live ordering or scratch ownership.
tool: evidence/EXP-070-procedural-rng-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-070: procedural RNG steps, scratch writes and exact rounding

**Result:** 14 controls passed, including two rounding counterexamples and a
detected final-state mutation. ASTRA, 2026-09-11. Two initial fixture/oracle
address errors were preserved and corrected before any PASS; see below.
Original code executed offline with synthetic memory and **no callee stubs**.

## Question and method

The [authored-expression page](../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md)
and RN-1 leave the bit algorithm unresolved and describe the bounded result as
`trunc(u * bound)`. The [RNG page](../21-RNG-And-Determinism/rng-streams.md) already
supplies the recurrence. This experiment tests the bounded helper's use of that
recurrence and whether the simplified scaling preserves native rounding.

The [checker](evidence/EXP-070-procedural-rng-controls/check.py) verifies the EXE
SHA-256 and executes complete bodies `004005E0` (108 bytes, one-step float) and
`003A6E60` (345 bytes, bounded integer). Both native 1.0 constants are extracted
and checked. MXCSR is set to `1F80`: round-to-nearest-even, exceptions masked,
without flush-to-zero or denormals-are-zero. No live MXCSR claim is made.

The independently implemented recurrence is:

```text
next(s) = (((s & 003FFFFF) | 1FC00000) << 1)
          | ((((s >> 18) ^ s) >> 4) & 1)
```

Global state is `01EF93E8`; mode is dword `022D9138`. Nonzero mode enables
advancement, including tested value 2. Mode zero leaves state unchanged but
**still writes scratch memory**. Inputs and complete fixture construction are
retained in the checker, with [raw results](evidence/EXP-070-procedural-rng-controls/result.json),
[disassembly](evidence/EXP-070-procedural-rng-controls/disassembly.txt), and
[manifest](evidence/EXP-070-procedural-rng-controls/manifest.json).

## Native step and output contract

`004005E0` advances once when enabled, reinterprets the new state as binary32,
and subtracts 1.0. Disabled, it returns zero. It stores the sample at `022D92E0`
and copies **16 bytes** from there to **`022D8F90`**, including the other three
pre-existing lanes. This copy occurs even when disabled.

`003A6E60` advances **five** steps to obtain sample `v`, then **two more** to
leave the final shared state. It has no zero-bound early return: bound zero
returns zero but consumes all seven steps while enabled. Disabled, it uses
sample 1.0 and leaves the recurrence state unchanged.

For signed dword bound `b`, the exact tested arithmetic is:

```text
B = round_binary32(b)
P = round_binary32(v * B)
D = round_binary32(P - round_binary32(B * 1.0))
result = CVTTPS2DQ(D).low_dword
```

Each rounding boundary matters. From seed `458DC800`, the fifth-step sample is
bits `3FB90003` = 1.4453128576278687. With bound **1,000,000,000**, native returns
**445,312,896**, whereas binary32 `(v - 1) * B` followed by truncation returns
**445,312,864**. Bound -1,000,000,000 gives the corresponding negative pair.
Thus the previously tested `trunc(u * bound)` shorthand is not an exact general
replacement, despite matching the older finite set of controls.

The first three bound-100 results from that seed are 44, 0, 0. One bounded
call leaves state `3FE4000D`, exactly the state after seven successive original
one-step calls. This is state-phase equivalence, **not scratch/output equivalence**.

## Exact scratch effects

The enabled bounded helper performs these writes in order:

1. Fifth-step state to `01EF93E8` (`003A6F0C`).
2. Product P to `022D91A0` (`003A6F39`).
3. Difference D to `022D92E0` (`003A6F45`).
4. Seventh-step state to `01EF93E8` (`003A6F8C`).
5. Seventh-step sample to **`022D92F0`** (`003A6FA1`).
6. Converted four-lane integer vector to `022D92E0..022D92EF` (`003A6FAD`).

The vector conversion reads D plus the three existing lanes at E4/E8/EC;
the write to F0 is outside that vector. The fixture starts those lanes at
2.5, -3.5, 4.75, proving their conversion to 2, -3, 4. A subsequent call
reinterprets the resulting integer bits as floats before converting again.
Disabled execution omits both state writes and puts 1.0 at F0; the remaining
scratch writes still occur. Shared scratch is not private per-generator state.

## Controls, failures and falsification

The 14 fixtures cover seeded sequential draws; zero, negative, signed-limit and
large rounding-sensitive bounds; zero/all-bits state; disabled/mode-2 paths;
and seven sequential one-step calls. All 22 original invocations require the
expected return boundary, RSP and eight nonvolatile integer registers. Full
return bits, exact ordered write instructions/addresses/bytes, and complete
state/mode/constant/scratch pages are checked. Reads and visited instructions
are retained. SIMD preservation and live initialization are not claimed.

The write recorder combines contiguous Unicorn fragments from a single native
instruction and reads the bytes after that instruction, so a 16-byte MOVUPS
store is checked in full rather than trusting a truncated hook value.

Two failed setups are preserved in [failed-setup.txt](evidence/EXP-070-procedural-rng-controls/failed-setup.txt)
and their exact source files. First, the one-step copy destination was wrongly
assumed to be `022D91A0`, causing an unmapped write at its actual `022D8F90`.
Second, the bounded final sample was predicted at E8 instead of actual F0;
the exact write/page oracle rejected it. Both were corrected from RIP-relative
instructions. Twelve controls then passed; two new rounding controls were added
and the final 14-case set passed. No invalid run was promoted.

A private mutation removes the final state store at `003A6F8C`. The bounded
return still reaches its normal boundary but state/write/page oracles reject
the missing two-step advancement. The reference EXE is never modified.

The recurrence, draw cost and precise arithmetic are ready for local parity
work. The seeder's callers, live draw order, full consumer census and ownership
of shared scratch remain outside this experiment. RN-1 and its scaling claim
are routed to FABLE for correction and propagation.

## ASTRA contract consumption — 2026-09-21 UTC

The recovery metadata said no matching contract existed: the gameplay-generator
contract covers the separate LCG/MT family. That historical distinction remains
correct. The new [authored-expression contract](../02-Resource-And-Asset-Pipeline/Authored-Expressions/CONTRACT-authored-expression-evaluation.md)
now cites these exact procedural-helper results in §13. ASTRA accepts that bounded
match in response to `OPUS-REQ-ASTRA-EXP070-NOW-HAS-A-CONTRACT` and links it above.

This incorporates existing method-B evidence. It adds no execution, fixture,
live observation or independent review. The expression evaluator's other entries,
operand/operator dispatch, live initialization, draw scheduling and shared-scratch
ownership are not established by this experiment. The original raw results,
failed fixtures, mutation and controlled-MXCSR limits remain unchanged.
