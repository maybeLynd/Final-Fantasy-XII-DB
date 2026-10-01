---
experiment: EXP-078
title: Arena allocation returns and encoded neighbor-link effects
status: COMPLETE
contract: ../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md
tool: evidence/arena-allocation-link-width/review_capture.py
method: B - isolated original-code execution
live_game: false
date_designed: 2026-09-12
date_run: 2026-09-12
---

# EXP-078 — consecutive allocations expose the encoded-link boundary

**Result:** seven predicted outcomes matched, including two controlled original
faults. A separate completed control detected a broken predecessor link despite
correct allocation return values. ASTRA, 2026-09-12. Original code ran only in
isolated synthetic fixtures. No live game, native CRT allocation or reconstruction
implementation ran. Subsequent verification and sealing read saved data only.

## Question, reference and prepared state

[EXP-077](EXP-077-arena-initializer-address-width.md) proves high backing pointers
survive initialization. This follow-up asks what happens when the original
allocator actually creates and later consumes encoded neighbor links. Returning
a high pointer once is not evidence that later operations preserve those links.

The reference EXE SHA-256 remains
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base
`00120000`. Fifteen complete original bodies were extracted and checked against
the sealed primary receipts; thirteen were actually reached across these cases.
The [raw result](evidence/arena-allocation-link-width/allocation-result.json)
lists every body hash. The [new helper receipt](evidence/arena-allocation-link-width/primary.json)
adds nine complete bodies, including the unlinker `0036C9D0`, neighbor inserters
`0036B7F0`/`0036B8B0`, page-index helpers and coalescing helpers. The allocator,
encoder and decoder retain their earlier exact receipts.

No initializer case was rerun. Each fresh fixture starts from EXP-077's sealed
native output: zero global region plus its recorded writes, one MiB of `A5`
backing plus its recorded writes, and decoder base zero. The reconstructed `A8`
arena record and `2C0` backing prefix must exactly match the earlier raw final
bytes. Whole fixture hashes are recorded before the next operation.

The original selector `0036C1F0(2,5,0,0)` establishes logical arena 2 and selection
depth 1; both globals are checked. This supplies a real precondition of
`0036BC60`: with no supplied block and zero selection depth it self-loops.
Each allocation then calls `0036BC60(2, size, 0, direction)` from its entry.
Completed cases restore the prior selection through original `0036C140`.

There are **no callee stubs in this allocation stage**. All reached allocator,
list, header, encoding and selection callees execute their original instructions.
EXP-077's output fixture still inherits its earlier no-write formatter limitation;
this follow-up does not retrospectively prove formatting or boot behavior.
Unreached diagnostic/exit branches and the two loaded but unreached free-list
inserters `0036B670`/`0036B730` gain no execution evidence.

Every call initializes its arguments, return sentinel, stack, DF/MXCSR, eight
nonvolatile general registers and full XMM6–15. Successful calls must reach the
original return boundary and restore the stack and those registers. Traces record
all original instruction entries, helper calls/arguments, non-stack reads/writes,
fault details, and final arena/prefix/tail bytes. Unicorn 2.1.4.

## Controls and original outcomes

`P` is the backing address; numbers below are hexadecimal. Ordinary requests are
`40` bytes. Each two-allocation case uses one continuous fixture, so the second
operation consumes the first operation's actual output.

| Case | P | Direction | Observed outcome |
|---|---|---:|---|
| Low positive control | `40010000` | 0 | Returns `P+2C0`, then `P+340` |
| Above 2 GiB | `80010000` | 0 | Same offsets, preserving high bit 31 |
| Above 4 GiB | `100010000` | 0 | First returns `P+2C0`; second faults at `0036CA8A`, writing dword zero to `10290` |
| Above 4 GiB with separate low mirror | `100010000` | 0 | Both returns succeed, but second operation accesses the separate low region as detailed below |
| Whole initial free block | `100010000` | 0 | One request of `FFD40` returns `P+2C0`; free-list ends become zero; no remainder link |
| Reverse positive control | `40010000` | 1 | Returns `P+FFFC0`, then `P+FFF40` |
| Above 4 GiB, reverse | `100010000` | 1 | First returns `P+FFFC0`; second faults at `0036CA75`, writing dword zero to `10FF8C` |

Both faults are `UC_ERR_WRITE_UNMAPPED` at the predicted original store. They are
valid observations of this supplied state, not successful allocator returns.
The corresponding low controls complete, and the high backing remains mapped
throughout. These cases do not establish the backing used in a running game.

## Exact cause and the mirror control

For direction 0, first allocation creates allocated header `P+280` and remainder
header `P+300`. The original inserter stores `10300` at `(P+280)+10` and `10280`
at `(P+300)+0C`. On the second allocation, `0036C9D0` reads the latter encoded
predecessor, resolves it through the original zero-base decoder to `10280`, and
attempts the store at predecessor `+10 = 10290`. It does not use the full
`100010280` address retained elsewhere.

Direction 1 leaves the remainder at `P+280` and allocates a header at `P+FFF80`.
The remainder's `+10` holds `10FF80`. On the second allocation the unlinker uses
that decoded successor and attempts its `+0C` store at low address `10FF8C`.
The free-list links at `+04/+08` and these neighbor links at `+0C/+10` are
different fields; this experiment identifies the latter as the failing path.

The separate mirror is an explicit intervention: immediately before the second
allocation, map one MiB at `10000` and copy the high backing there byte-for-byte.
The copied bytes are checked and hashed. The second allocation now returns the
expected high pointer, while its recorded low-region events are exactly:

| Original instruction | Event |
|---|---|
| `0036CA8A` | Write dword `0` to `10290` |
| `0036CA8D` | Write word `0` to `102BE` |
| `0036B83E` | Read dword `0` from `10290` |
| `0036B853` | Write dword `10300` to `10290` |
| `0036B856` | Write word `0` to `102BE` |

These are accesses to separate storage, even though the returned pointer is
correct. **The exact mirrored bytes end unchanged**: `10290` is temporarily
cleared then restored, and the word was already zero. This proves wrong-region
access, not persistent corruption or a crash in the shipped game.

## Discriminating control and saved-data review

One targeted control, completed before the later method change, makes the
original decoder ignore its input reference before its unchanged base addition.
Its [receipt](evidence/arena-allocation-link-width/mutation-result.json) records
the exact original/modified bytes and hashes. Both expected low allocation
pointers still return with valid stack/register restoration, but the second
allocated header's `+0C` predecessor becomes zero instead of `40010280`.
The predecessor assertion detects the change. A return-value-only comparison
would pass it. No historical mutation campaign was rerun.

The [saved-data reviewer](evidence/arena-allocation-link-width/review_capture.py)
performs no game-code execution. It checks the nonempty case/step census and
recorded call sequence against original instruction entries, then reconciles
**every recorded non-stack read/write** with the initialized memory and preceding
writes. The two unmapped attempts are verified as unmapped and excluded from
successful memory updates. Every recorded final arena/prefix/tail byte agrees
with that reconciliation. Exact faults, returned pointers, selection boundaries,
allocation counters, predecessor values and all mirror events are asserted.
The [review result](evidence/arena-allocation-link-width/review.json) and
[manifest](evidence/arena-allocation-link-width/manifest.json) preserve this check.

The original [probe source](evidence/arena-allocation-link-width/allocation_probe.py)
and [completed control source](evidence/arena-allocation-link-width/mutation_control.py)
are retained unchanged as provenance. They retain repo-relative scratch inputs
and outputs; sealing does not run them or replace historical receipts. All
emulation processes had ended before review. No live game, save, configuration,
shared native laboratory or actual executable file was modified.

## Implications and unresolved work

For these zero-base fixtures, successive original arena operations can follow
32-bit neighbor links into low storage even after high-address initialization
and a first allocation succeed. This is a concrete allocator dependency for
modding and reconstruction. It does not establish a general 2-GiB limit,
placement in an actual process, base/map lifetime, arbitrary size behavior,
exhaustion, reclamation, live resource lifetime or integrated parity.

The user requested a different method after reporting platform resume notices.
Further work in this package therefore uses the completed captures, static
reasoning and consumer integration. Missing live evidence remains open. FABLE
and OPUS must review the new finding in their actual consumers before closure;
this completed local experiment does not complete the L1/L2 database goal.
