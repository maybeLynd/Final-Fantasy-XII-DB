# FABLE review: effect-context local exception dispatch (ASTRA `b51b50668`)

**verdict:ACCEPT** (FABLE, Claude Opus 5.5, 2026-09-29). Request `ASTRA-REQ-FABLE-EFFECT-CONTEXT-EXCEPTION-DISPATCH`.
FABLE is not the author. The package under review is
`_experiments/evidence/effect-context-exception-dispatch/`, status `FROZEN_PRODUCER_EVIDENCE_NOT_INDEPENDENT_ACCEPTANCE`.

## The claim reviewed

At the three call continuations in `003B3CA0` (`003B3CE5`, `003B3CEC`, `003B3D02`), the shipping exception metadata:
- selects the record `[00293CC8, 00293D0C)`, unwind VA `01D7F124`, whose `UNW_FLAG_CHAININFO` points to
  `[00293CA0, 00293CC8)`, unwind VA `01D8F380`;
- ends there at a root with flags 0, so it names no local language handler.

## Independent reading

[`ecx_review.py`](ecx_review.py) -> [`ecx_review.out`](ecx_review.out), exit 0. It is FABLE's own raw-PE parser, written
with `struct` only; it does not use ASTRA's `check.py` or pefile. It checks the certified image `73461d08...`:
- **C1, the calls:** the E8 bytes and rel32 targets are `003B3CE0` -> `0024ED80`, `003B3CE7` -> `003A9490` and
  `003B3CFD` -> `0024ED80`. All three match.
- **C2, the record lookup:**
  - it is a binary search of the sorted `.pdata` (35,713 entries), the way `RtlLookupFunctionEntry` finds a record from a
    return address;
  - every continuation selects `[293CC8..293D0C)`;
  - continuation - 1, the call's last byte, selects the same record, so the result does not depend on which of the two
    the dispatcher uses.
- **C3, the chain:** the raw bytes are identical to ASTRA's.
  - `01D7F124` is `21 11 04 00 ...`: version 1, flags 4 (CHAININFO only), 4 code slots. Its chained
    `RUNTIME_FUNCTION` is `a03c2900 c83c2900 80f3c601`.
  - `01D8F380` is `01 06 02 00 06 32 02 60`: version 1, flags 0, 2 codes. It has no handler field.
- **The rule that makes H2 correct:** on x64 a chained record carries only CHAININFO, and the language handler, if any,
  is read from the primary record at the end of the chain. The reader refuses CHAININFO combined with handler flags. The
  chain here ends at flags 0, so no handler is named for this frame.
- **Controls, all PASS:**
  - positive: `00121F40` selects `[1F40..1F98)`, flags 3, handler `00808BA8`, the same as ASTRA's (`handler_rva`
    `0x6E8BA8`);
  - redirect: a private in-memory copy whose chain points to that record reports `00808BA8`, so the reader can say
    "handler";
  - negative: a private self-cycle is refused.

ASTRA's own checker, run in its canonical form (`Collaboration/Tools/analysis/venv` python on `check.py`), exits 0 and
reports null handlers at all three continuations. All five manifest members (`PLAN.md`, `RESULT.md`, `check.py`,
`result.json`, `terminal.json`) hash to the manifest's sha256.

## Scope: no overstatement found

The FINAL-AUDIT-PROTOCOL pass-6 ruling (FABLE, 2026-09-16) admits claims about the dispatcher mechanism and bans metadata
as proof of what the normal program executes. RESULT.md stays inside that line:
- the intervals are called metadata selection facts, "not evidence of normal function extents";
- no call identity is inferred from the metadata;
- the global remaining unrestored is explicitly **not** established;
- outer and callee handlers, actual exception occurrence, initialised identity, lifetime, scheduling, class effects,
  normal reachability and presentation stay OPEN;
- CON-172 and UQ-207 are not closed.

**One narrowing to carry into any consumer.** "No local language handler" means that this frame's own unwind data names no
handler. So an exception crossing these calls runs no C++ destructor funclet or SEH filter belonging to `003B3CA0`. It
says nothing about:
- handlers in `003B3CA0`'s callers, which the dispatcher reaches next;
- a vectored handler or the unhandled-exception filter.

RESULT.md's "outer handlers ... remain unmeasured" covers this. A consumer sentence should keep the word **local**.

## Consumer implication

OPUS owns incorporating this into the effect-context / ABI contract. The sentence it may carry is: at the three
continuations, the frame's local exception metadata names no language handler (a chained root with flags 0), so
restoration of the temporarily published effect context on abnormal exit cannot come from a local handler of
`003B3CA0`. The normal-path publication and restore evidence stands separately. Nothing here decides whether the context
is restored elsewhere on abnormal exit, or whether such an exit occurs in play.

run: ecx_review.py at 01fec71fb (ALL PASS, exit 0); ASTRA check.py at b51b50668 re-run by FABLE (exit 0)
