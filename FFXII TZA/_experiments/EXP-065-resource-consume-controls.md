---
experiment: EXP-065
title: original execution-resource consumption
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies execution-resource consumption 00305640; commit-action and inventory class storage do not specify this caller.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original consumer and pointer resolver with eight stubs and two labeled callback interventions; native resource stores omitted.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-065-resource-consume-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-065: original execution-resource consumption

**Result:** 23 controls passed on the first execution; a stale-stats-pointer mutant
was detected. ASTRA, 2026-09-11. Isolated original instructions, no game process.

## Question and boundary

The [item lifecycle page](../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md)
summarizes consumption as clearing reservations and charging resources, and says
all three lifecycle functions begin with the same kind guard. This experiment
checks the complete consumer, including the extent of that guard and callback
ordering. [EXP-064](EXP-064-resource-payer-controls.md) covers preparation;
[EXP-061](EXP-061-mp-writer-controls.md) covers native MP/secondary writers.

The [checker](evidence/EXP-065-resource-consume-controls/check.py) verifies the
reference executable SHA-256 and runs original `00305640` (393 bytes, RET at
`003057C8`) plus the native pointer resolver `0020E600` (10 bytes). Synthetic
memory supplies unit, stats, action header/row, relocation globals and stack.
Original instructions are in the [disassembly](evidence/EXP-065-resource-consume-controls/disassembly.txt).
[Results](evidence/EXP-065-resource-consume-controls/result.json), source and bytes
are sealed by the [manifest](evidence/EXP-065-resource-consume-controls/manifest.json).

Eight callees are explicit stubs: MP cost `00309110`, tier cost `00308FF0`,
MP writer `00300CE0`, secondary writer `00300BC0`, gil getter/setter `00253690` /
`00254EE0`, category-10 callback `00316440`, and counter callback `00253770`.
They record exact arguments and reservation snapshots and clobber volatile
integer registers. Only two named controls intervene in fixture memory through
callbacks; those writes are recorded separately. Native downstream effects,
including actual MP/gil/counter stores, are not executed here.

## Observed contract

1. Action id derivation precedes all unit checks, as in preparation: resolve
   registry `02EBF138` header token `+0xC`, subtract low dword row/base pointers,
   unsigned-divide by header word stride `+8`, retain the quotient.
2. Nonnull unit with nonnull stats `unit+0x698` and kind byte `stats+5 == 0`
   clears **dword `unit+0xE58` first, then word `unit+0xDC8` to `0xFFFF`**.
   The guard protects only these stores. Other kinds retain both reservations
   and continue to the resource calls. There is no return at the failed guard.
3. Call MP cost then tier cost, both `(unit, low16(actionId))`. Call the MP writer
   with `(unit->stats, u32(-mpCost), 0x10 + (low32(inputFlag) != 0))`.
   Zero costs still produce calls. Input flag 1 and -1 both select `0x11`;
   input `0x100000000` behaves as zero and selects `0x10`.
4. **Reread the stats pointer after the MP callback.** Call the secondary writer
   with this pointer, `u32(-s16(stats+0x28) * tierCost)`, and the same flags.
   The multiplication and negation wrap in 32 bits. Negative capacities and
   costs are preserved as arithmetic inputs in the synthetic controls.
5. Read **dword `unit+0xE54`**, negate in 32 bits, get gil, and pass the wrapped
   sum when its sign is clear or zero otherwise to the gil setter. This path
   executes even with zero extra charge. The field is distinct from the cleared
   reservation at `+0xE58`. No authored meaning of `+0xE54` is newly assigned.
6. Reread stats and its kind for category accounting. Only kind zero enters
   this tail. Category byte `row+0x1E` 0 / 1 / 2 calls `00253770(category, 1)`.
   Category 10 calls `00316440()`, resolves the action table again, rederives the
   full unsigned quotient, then calls `00253770(13, quotient)`. Categories 3,
   9 and 11 are negative controls with no accounting callback. No native counter
   semantics or reset effects are inferred from the stub names.

## Discriminating controls

Nineteen normal-return controls cover three flag patterns, kind 1 / 3,
categories 0 / 1 / 2 / 3 / 9 / 10 / 11, zero and negative costs, signed capacity,
32-bit multiplication overflow, an insufficient-gil case, and two interventions.
The base control passes MP delta -31, secondary delta -200, flags `0x10`,
and gil setter argument 93 from balance 100 and extra charge 7.

The **MP-callback intervention** changes the unit's stats pointer to an alternate
record (capacity 200, kind 1) and extra charge to 13. Secondary receives the
alternate pointer and -400; gil setter receives 87; kind 1 suppresses the
category counter. This proves the three later reads occur after the callback;
it does not claim that the native MP writer changes these fields.

The **category-10 intervention** changes header stride from 64 to 32 during
`00316440`. Initial cost calls receive id 3, while the final counter call receives
`(13, 6)`, proving fresh derivation rather than reuse of the initial quotient.

Four expected failures are separate from normal returns: missing header faults
on dword address `0xC`; zero stride raises a CPU division exception at `00305690`;
null unit reaches both cost stubs then faults reading pointer address `0x698`;
null stats reaches both cost stubs and MP stub then faults reading word address
`0x28`. The last two paths depend on the controlled callees returning; actual
native callees can fail earlier, so these are local caller-boundary controls.

Every case compares exact call order, multiplicity, arguments and reservation
snapshots; exact native non-stack writes; planned intervention writes; and
complete fixture pages. Normal returns must reach the stop address, restore RSP
and all eight nonvolatile integer registers. No SIMD or return-value contract
is asserted. Reads, visited instructions, stop address and errors are retained.

A private mutant changes the post-MP pointer load at `003056F9` from `+0x698`
to a fixture slot holding the old pointer at `+0x690`. It returns normally but
passes the old pointer and -200 to the secondary writer, failing the exact event
oracle. The original executable and production source are never modified.

## Propagation and limits

The item page's shared early-return sketch must not describe the entire consume
body: its kind check limits reservation clearing only. Cost/MP/secondary/extra-gil
calls follow regardless of kind. Its prepare and refund claims require their
own bodies; this result does not silently change them.

This closes the isolated caller dispatch boundary. It does not compose native
cost calculation or setters into consumption, establish live timing, prove a
whole action, or promote replacement parity. The original code may reread state
changed by native callbacks; the interventions establish those dependencies
without supplying their native causes.
