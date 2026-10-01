---
experiment: EXP-063
title: original action MP-cost calculation
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies action MP cost 00309110 and its modifier chain; commit-action is commitment, not cost computation.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Four complete original cost bodies without stubs, synthetic tables and original float constants; setup failures and invalid-input faults preserved.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-063-mp-cost-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-063: original action MP-cost calculation

**Result:** 31 controls passed after correcting an invalid table fixture; an
exclusive-upper-bound mutant was detected. ASTRA, 2026-09-11. No game process
was accessed.

## Question and original-code boundary

CS-5 on [the MP page](../10-Status-Periodic-Terminal/where-mp-comes-from.md) leaves
`00309110` unread. The [availability page](../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md)
already names the modified-cost and gil-channel helpers, but does not decode the
complete calculation. This experiment tests the wrapper and those helpers together.

The [checker](evidence/EXP-063-mp-cost-controls/check.py) verifies the certified EXE
SHA-256 and executes four complete original bodies: `00309110` (165 bytes),
`002F95D0` (589), `002F9820` (51) and `0020E600` (10). **No callees are stubbed.**
The pointer resolver executes its original `zeroExtend(ECX) + [01F83530]` operation.
Synthetic action/effect tables, unit, stats and relocation base provide its inputs.
Original float constants are retained: `008F3134 = 100.0`, `00916318 = 64.0`, and
`008F3130 = 50.0`. No authored table values are claimed from these fixtures.

Original bytes, [disassembly](evidence/EXP-063-mp-cost-controls/disassembly.txt),
executed source and [results](evidence/EXP-063-mp-cost-controls/result.json) are
sealed in the [manifest](evidence/EXP-063-mp-cost-controls/manifest.json).

## Wrapper `00309110(unit, actionId)`

The argument is consumed as a **16-bit action id**. Values through `0x21E` are
admitted; `0x21F` returns zero. An input dword `0x1021E` behaves as id `0x21E`.
The action row comes from registry `02EBF138`, header word stride `+8` and resolved
header dword `+0xC`; its base cost is an unsigned byte at row `+0x0A`.

Before consulting unit effects, action row byte `+0x1E` equal to **5 or 6** returns
zero MP cost. Category 7 is a positive control. With a null unit and an admitted
row category, the wrapper returns the base-cost byte directly.

With a unit, `002F9820` reads `unit+0x698`. A nonnull stats record whose kind byte
`+5` equals 1 returns false. Other kinds select the alternate channel when bit 0 of
either `stats+0x6C` or `+0x7C` is set (effect id 32 under the two-layer convention).
When that predicate is true, this **MP** wrapper returns zero; it does not compute
or deduct the alternative resource. Its established database name is
`BattleUnit_UsesGilActionCostChannel`; the naming was not independently recovered
from player-facing data here.

If the predicate is false, the wrapper tail-calls `002F95D0(unit, low16(id))`.

## Modified amount `002F95D0`

The helper resolves the action row again and starts from its unsigned cost byte.
For stats kinds other than 1, action ids **`0xD0..0xE1`** and **`0x106..0x112`**
return that base before the modifier effects. Controls exercise both endpoints
and both adjacent outside values for each range. Kind 1 skips this range bypass.
The wrapper's earlier alternate-channel predicate still has priority over it.

The remaining rules, in original order, are:

1. If effect 32 is set in either layer, return
   `10 * trunc(f32(f32(base * 64.0) / 50.0))`.
   In the wrapper composition this branch is reachable for **kind 1**, whose
   channel predicate returned false. Base 31 produces 390. This is not merely
   `trunc(base * 12.8)`; the truncation occurs before multiplication by ten.
2. Otherwise, sum unsigned words at **row `+4`** of registry **`02EBF040`** for
   enabled effects 91, 92 and 93. These correspond to masks `0x08`, `0x10`, `0x20`
   at stats byte `+0x73` or `+0x83`. Each effect contributes once even though either
   layer may enable it; the corresponding table row is `0x5B`, `0x5C` or `0x5D`.
3. Calculate the float32 reduction, preserving separate operation rounding:
   `trunc(f32(base - f32(f32(base / 100.0) * sum)))`.
4. Effect 51 (mask `0x08` at `+0x6E` or `+0x7E`) overrides that result to zero.
5. Otherwise effect 36 (mask `0x10` at `+0x6C` or `+0x7C`) halves the **already
   truncated integer**, truncating toward zero.

Synthetic percentages 10/15/20 with base 31 yield individual costs 27/26/24;
together they yield 17, and the half effect then yields 8. Half without reductions
yields 15. The two effect layers are exercised independently. Oversized percentages
80/80/80 plus half return signed -21 (`EAX FFFFFFEB`): this helper does not clamp
an excessive reduction to zero. That is an out-of-domain fixture result, not proof
that the shipped tables produce a negative cost.

## Required input state and failed setup

A null action-table header is not a safe zero-cost fallback: the wrapper reaches
an unmapped read of byte `0x1E`. A nonnull unit with null stats reaches byte `0x6C`
in the channel helper. Those two controls require the precise fault addresses and
an actual emulation error. They are **expected invalid-input faults**, not successful
function returns; valid fixtures supply the positive read/return controls.

The first development run stopped at the first enabled reduction. The fixture had
initialized effect registry `02EBF140`, while original `002F96A0` reads `02EBF040`.
A diagnostic-only retry identified RIP `002F96E5` reading word address 4. Neither
run produced a PASS result. The [failed setup receipt](evidence/EXP-063-mp-cost-controls/failed-setup.json)
and [original failed checker](evidence/EXP-063-mp-cost-controls/failed-initial-check.py)
are preserved. Correcting that synthetic registry input made all 31 controls pass;
no original instruction or expected formula was changed to hide the failure.

## Validation, falsification and integration

Every valid control reaches the injected return, restores RSP and all eight
nonvolatile integer registers, and compares full EAX plus the exact native call
sequence and measured register arguments. All cases reject nonstack writes and
compare the entire synthetic table/unit/global fixture regions. Results preserve
inputs, expected/actual values or faults, call events, read addresses and widths,
instruction visits, errors and final RIP. Nonvolatile SIMD preservation and
live-process ABI/scheduling are outside this test.

The private mutant changes the unsigned `JA` at `00309128` to `JAE`. Id `0x21E`
then returns zero rather than base 31. It reaches the normal return but loses the
required table/helper calls and result, so both comparisons reject it.

FABLE/OPUS receive the exact wrapper, effect precedence, ranges, float operation
order, table-field widths and null-input requirements. This closes the local
calculation gap, subject to owner integration; **resource deduction timing, the
alternative-channel deduction, authored costs/percentages, action category names,
and the full availability cascade remain separate questions**. The experiment
writes no MP or other resource state and does not claim to exercise spending.
