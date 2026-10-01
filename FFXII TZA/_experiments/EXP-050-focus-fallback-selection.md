---
experiment: EXP-050
title: focus-selection fallback and dispatch order
status: COMPLETE - bounded isolated original-code evidence
contract: none - Focus fallback selection 00326500 is outside the existing party-slot assignment contract; its native queries and dispatcher are omitted.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original selection body and encoder with controlled query returns; stop before native tail dispatcher.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-050-focus-fallback-selection/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-050: focus-selection fallback and dispatch order

**Result:** eleven original-body selection/call-order cases passed with controlled
dependency returns. A private three-slot-loop fault was detected. ASTRA, 2026-09-11.
No live game, native dependency effects or completed focus dispatch are claimed.

## Question and authority

[EXP-049](EXP-049-handle-renewal-focus.md) stops before `00326500`. This experiment
tests that function's selection control flow: which selector it asks for, how it
searches fallback slots, and which handle it forwards to the final dispatcher.

[check.py](evidence/EXP-050-focus-fallback-selection/check.py) verifies the certified
executable SHA-256 and extracts the complete 274-byte body at `00326500` through
the back-jump at `00326610`. The original 38-byte handle encoder is also executed
and must match EXP-048's retained bytes. Exact
[body](evidence/EXP-050-focus-fallback-selection/function.bin),
[encoder](evidence/EXP-050-focus-fallback-selection/encoder.bin) and
[disassembly](evidence/EXP-050-focus-fallback-selection/disassembly.txt) are retained.

## Controlled dependencies

Every case gets fresh Unicorn memory and synthetic units, actor and state. Calls
to `00311E20`, `00326620`, `0030D9A0`, `00377C70`, `0031B770`, `00322C50`, `002367A0`,
`00263750` and `00317400` record arguments and return controlled values. These
stubs perform no native memory effects. The original body and encoder execute;
the final tail target `003594B0` is a stop boundary, not an executed stub.

The retained checks assert the complete expected sequence of calls, meaningful
arguments, selected handle and dispatch boundary. The caller's return address and
original RSP must be restored at the tail dispatch. No non-stack write is allowed
under these controlled dependency returns. Thus this experiment establishes the
wrapper's decisions and invocation order, not what its callbacks actually do.

## Selection behavior

Calls start in this order: `00311E20`, `00326620`, then mode query `0030D9A0`.
The selector passed to `0031B770` is:

| First mode result | Selector |
|---|---|
| 0 or 1 | preferred byte at state+5AA4 |
| 2 | 1Ah |
| 3 | low byte returned by `00377C70` |
| Other tested value (4) | FFh |

A nonnull returned unit qualifies only if its stats pointer at +698 is nonnull.
Otherwise, the original body considers fallback slots 0, 1, 2, 3 in order. For
each it calls `00322C50(17h, slot, 0)`. A nonzero result selects the byte at
state+5A5A+2*slot; zero selects FFh. That byte is passed to `002367A0`, and again
a unit needs a nonnull stats pointer. The first qualifying unit ends the search.

If no unit qualifies, it calls `00263750(0)`. A nonnull actor is encoded by the
original encoder; a null actor produces handle zero. This fallback does not
invent a unit/stats check around the slot-0 actor.

For a qualifying unit, the dispatched handle comes from its cached dword +8.
The mode is queried **again**; only a second result of 1 invokes `00317400(unit)`.
Every tested path then calls `00311E20` and tail-dispatches the selected handle
to `003594B0`. A control with first mode 0 and second mode 1 confirms the second
query controls this callback. It is a deliberate input distinction, not a claim
that mode changes during this function in the live game.

## Evidence and falsification

The eleven cases cover modes 0/1/2/3/4, low-byte truncation of a field selector,
the differing second mode, a first fallback hit, a fourth fallback hit after
rejecting a primary unit with null stats, a disabled fallback slot, actor-slot-0
fallback, and no actor. Exact sequences and outputs are in
[result.json](evidence/EXP-050-focus-fallback-selection/result.json).

A private mutant changes only the fallback-loop limit from four to three. With
the sole qualifying unit in slot 3, it incorrectly falls through to actor slot 0;
the selected handle and expected call sequence both differ. This demonstrates
that merely reaching a dispatch is insufficient for a passing result.

The [manifest](evidence/EXP-050-focus-fallback-selection/manifest.json) seals the
package. Run `check.py` with the repository's existing Windows Python/Unicorn
environment. The native query definitions, callback effects, dispatcher behavior,
live focus change and lifecycle timing remain outside this controlled execution.
