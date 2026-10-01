---
experiment: EXP-064
title: original execution-resource preparation
status: COMPLETE - bounded isolated original-code evidence
contract: ../12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original preparation and pointer resolver; inventory and gil dependencies controlled, invalid header and stride faults separate.
contract_coverage: Caller-side five-argument inventory request at 003008A0 after local reservation; inventory is a no-effect stub, so native class storage and item deduction are untested.
tool: evidence/EXP-064-resource-payer-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-064: original execution-resource preparation

**Result:** all 17 controls passed on the first execution; an inverted item gate
was detected. ASTRA, 2026-09-11. Isolated original code, no game process accessed.

## Question and method

The [item lifecycle page](../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md)
and [gil page](../13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md)
describe preparation as reserving an item and gil. This package tests exact local
ordering, call arguments, input guards and writes; it complements their static
research rather than measuring live execution timing.

The [checker](evidence/EXP-064-resource-payer-controls/check.py) verifies the reference
EXE SHA-256 and executes complete original `0030EF20` (205 bytes, through RET at
`0030EFEC`) and pointer resolver `0020E600` (10 bytes). Synthetic unit, stats,
action row/header and relocation globals supply memory. Inventory `003008A0`,
gil-cost `00309060`, gil getter `00253690` and setter `00254EE0` are explicit
no-effect stubs, recording calls and returning configured values. Each stub
clobbers volatile integer registers. The resolver runs natively.

[Original bytes and disassembly](evidence/EXP-064-resource-payer-controls/disassembly.txt),
[raw results](evidence/EXP-064-resource-payer-controls/result.json) and executed
source are sealed by the [manifest](evidence/EXP-064-resource-payer-controls/manifest.json).

## Findings

1. **Table access and division precede the null-unit guard.** The body resolves
   header dword `+0xC` from registry `02EBF138`, subtracts the low 32 bits of the
   resolved base from the low 32 bits of the row pointer, and unsigned-divides
   the wrapped difference by header unsigned word `+8`. Only then does it check
   unit, stats pointer `unit+0x698`, and stats kind byte `+5 == 0`.
   A null unit with a valid table returns normally after the resolver call;
   a null unit with no header faults reading dword address `0xC`; zero stride
   raises a division exception at `0030EF5B`. No reservations are written in
   these controls. A guard-first pseudocode summary must retain this precondition.
2. For admitted kind zero, nonnull row with category byte `+0x1E == 3` supplies
   unsigned word item `+0x22`; otherwise the reserved item is `0xFFFF`.
   The word at `unit+0xDC8` is stored **before** inventory is called. A reserved
   item other than `0xFFFF`, including zero, calls inventory with five arguments
   `(item, -1, 0, 1, 0)`. The fifth dword is read at callee `RSP+0x28`.
3. Next the gil-cost stub receives `(unit, low16(quotient))`. The returned dword
   is stored at `unit+0xE58` before the gil getter/setter. Zero skips both.
   Nonzero obtains the balance and calls the setter with the wrapped 32-bit
   subtraction if its sign bit is clear, otherwise zero. This is a sign-bit
   test of machine subtraction, not an unbounded mathematical clamp: synthetic
   balance `0x80000000` minus cost 1 passes `0x7FFFFFFF`; cost `0xFFFFFFFF`
   with balance 100 passes 101. These are arithmetic controls, not shipped costs.
4. A null row with valid table is admitted for kind zero: it reserves no item
   but still computes and passes a quotient-derived cost id. Row pointers one
   and 63 bytes beyond the aligned fixture both truncate to the same row id.
   There is no alignment check in this body. No claim that callers supply such
   pointers is made.

## Controls and falsification

The 17 cases cover item plus gil, zero cost, insufficient/exact gil, non-item
category, item sentinel, item zero, null unit, null stats, kind one, null row,
two unaligned row pointers, negative synthetic cost, subtraction wrap, missing
header with null unit, and zero stride with null unit. Fifteen normal returns
and two expected invalid-input failures are distinguished in the results.

Each case compares exact callback order, multiplicity and arguments, reservation
values observed at every callback, exact non-stack writes, and complete fixture
pages after execution. Normal cases must reach the expected return address,
restore RSP and all eight nonvolatile integer registers. No SIMD preservation
or return-value contract is asserted for this preparation routine.

A private mutation changes `0030EF9D` from JE to JNE, suppressing inventory for
a valid item. It returns normally but fails the exact event oracle. It is never
applied to the reference executable or shared production source.

## Limits and propagation

Inventory contents, actual gil storage/counters, cost calculation and side
effects inside downstream callees are omitted. Reservation snapshots prove the
local ordering at stub entry, not behaviour under mutating native callbacks.
The caller's scheduling, consume/refund paths and MP deduction remain outside
this package. No live or replacement-parity promotion follows.

The item page's prepare pseudocode currently puts `if (!unit) return` first;
the evidence narrows that simplification: valid action-table header/stride are
required before the guard. Its reservation and gil ordering agree with the
normal controls. Route this precondition and evidence to the semantic owner.
