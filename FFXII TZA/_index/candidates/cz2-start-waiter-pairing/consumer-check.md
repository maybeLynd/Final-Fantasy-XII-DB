# Affected-consumer check: CZ-2 answered; "both halves of the idiom are accounted for" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `cz2_start_waiter_pairing.py` beside this file (6 checks, FAILS 0).

The dispatch page named the 77 begin-without-poll verbs as the class of "earlier verb" a waiter waits for, and
called both halves of the idiom accounted for. The starts and waiters do not pair one-to-one:
- 37 of the 77 pair many-to-one with three movement waiters, through shared begins;
- instantaneous verbs also start work that waiters wait for: `vibplay` precedes all 45,691 `vibsync` calls;
- 28 of the 77 are never called by a shipped script;
- two waiters can never report busy.

| consumer | what it said | state |
|---|---|---|
| `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`, the start-and-return quote | "the 77 … Both halves of the idiom are accounted for" | revised-here (struck the last sentence; the pairing beneath) |
| same page, "three behaviours, not two" | finish, start-and-return, block | agrees (the answer refines who starts, not the three behaviours) |
| `01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md` | a `*sync` verb waits for something started by an earlier verb | agrees |
| `_index/COVERAGE.md` ("Not examined … `CZ-2`") | a dated coverage log entry | agrees as history (a record of what that pass did not examine); not edited |
| `_index/OPEN-QUESTIONS.md` CZ-2 | OPEN | revised-here (ANSWERED; the previous status kept as history) |
