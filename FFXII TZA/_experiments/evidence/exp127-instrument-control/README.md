# EXP127 instrument boundary: unowned single-step dispatch

2026-09-21, ASTRA. **Method A plus synthetic instrument fixtures. No new FF12
execution, native debugger call, PC control or save/config write.** This is a
bounded repair/control package under ASTRA-SKELETAL-RESET-LIVE, not a new game
experiment or an answer to the skeletal/arena semantics question.

Player version: the measuring tool could wrongly swallow a stop that it did not
cause. The saved failed session does not show that particular mistake. Its crash
is still unexplained; we have improved the tool's decision and specified what
must be tested before another game trace.

## Question, method and identity

Does the exact tracer used in EXP127 restrict resume writes and handled-exception
replies to its own execute breakpoints? H1: its foreign-step path changes state
or consumes an exception; H2: it passes such an event through without a resume
write. Separately, do EXP127's saved API receipts exhibit that defect?

Existing source and API receipts distinguish these hypotheses without touching
FF12. `original/` contains the four exact executed files, matched to BOTH raw
capture result source dictionaries. `check.py` pins all four hashes, extracts
only selected definitions with Python AST, and supplies fake event/context APIs.
It never loads the historical WinDLL or invokes its CLI. Candidate files contain
the bounded functions only; there is no launch/deployment wrapper. The fixture is
not original-code execution, and its contexts are injected synthetic data.

Original capture SHA256:
`41b548c7a71c0713928ed7d8e62a5b4607172da23a29de2e18f3785ab7b93633`.
Original cleanup SHA256:
`865d788d6c98bd5b4de7a19b1d3c845e434cdd96e12119249a00711ad1d3fe7a`.
Original hardware helper SHA256:
`81a8510288dc5a4e1d93c221659c49926039e66aa277da3f1fea59aa193879f6`.
The remaining source digest, Python identity, raw input digests and each fixture's
ordered calls are retained in `result.json`. Input evidence is the unchanged
`../skeletal-reset-live/{control,skeletal}/capture/{api,result}.json`.

The historical game identity is EXP127 PID31940, shipping EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Its process, module, state and health receipts remain in that package. This
analysis does not turn those historical receipts into a new verified live state.

## Demonstrated defect and scoped correction

The old capture recognizes `EXCEPTION_SINGLE_STEP`, checks RIP against its slot
list, but calls `resume_past_breakpoint` even if RIP is foreign or the context
read failed. It then replies `DBG_CONTINUE` before reporting INVALID. A step at
a matching RIP is accepted without checking whether DR6 identifies that slot or
another debug cause. Cleanup resumes **every** single-step event and can still
report PASS when the later requested cleanup breakpoint succeeds.

This matters because `DBG_CONTINUE` marks the exception handled, while
`DBG_EXCEPTION_NOT_HANDLED` continues exception processing. See Microsoft's
[ContinueDebugEvent semantics](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent).
A final INVALID label does not undo an earlier resume write or handled reply.

`ownership.py` requires the observed RIP and exception address to agree, the
configured execute slots/enable bits to agree, and the relevant DR6 slot bit to
identify the event without competing causes or TF. It conservatively rejects
other modes. The DR6/DR7 interpretation follows Intel SDM volume3B, sections
19.2.3-19.2.4 ([revision088](https://cdrdv2-public.intel.com/858456/253669-088-sdm-vol-3b.pdf)).
This is a predicate for this particular recipe, not a general exception decoder
or proof that a software-raised event could never imitate hardware state.

`capture_candidate.py` and `cleanup_candidate.py` apply that predicate. Foreign
or unreadable steps get **no resume write**, are passed through as unhandled,
and invalidate the capture/cleanup. Owned steps retain the original resume path.
Historical files and mutations remain untouched.

The 16 controls cover both capture and cleanup: owned positive, foreign RIP,
TF at the same RIP, mixed causes, wrong slot bit, disabled slot, data-break mode,
and context-read failure. Every old foreign case calls resume and replies handled;
every corrected foreign case avoids resume and replies unhandled. Both owned
positives still pass. Replacing the predicate with the old address-only decision
causes the same-RIP TF case to pass incorrectly, so that regression discriminates.

**Not yet native-qualified:** these controls establish Python dispatch decisions
under the supplied API outcomes. Passing an exception through can legitimately
terminate a process that has no handler. An aborted cleanup is still INVALID and
does not prove cleared registers, safe detach or recovery. The candidate does not
repair all recovery paths, qualify arbitrary concurrent thread churn, or reduce
the existing full-context write to a minimal-context write. No live reuse is
authorized by its fixture PASS labels alone.

## What EXP127's saved events actually show

`check.py` independently pairs every successful event with its continuation,
checks the event thread against OpenThread and context handles, verifies the
requested context flags, and compares each recorded SetThreadContext proposal
against its preceding read. Main-window event sequences match result.hits in
thread, RIP and RSP exactly.

| Window | Recorded main hits | Additional cleanup steps | Total step events |
|---|---:|---:|---:|
| Known-entry control | 202 | 2 at003A1C50 | 204 |
| Skeletal | 5453 | 1 at003E3C7A | 5454 |

All5658 saved step events satisfy the conservative address/debug-register
predicate. In the recorded context fields, every resume proposal changes only
EFLAGS.RF and DR6. There are **no detected foreign-step or recorded-write
mismatches in these receipts**. The extra cleanup pre-call event was serviced
but not included in the semantic hit log; do not extend the2113 paired-boundary
claim to cover all execution through cleanup/detach.

This is a bounded negative with positive/detection controls, not proof that the
instrument was harmless. FirstChance was not logged. The API context receipts
omit most integer registers and all floating/vector state, although the helper
requests and rewrites full context. They do not record later target-side effects
or exceptions after detach. None of those unknowns is silently supplied by the
successful API return values.

## Claims and next discriminating control

- **Established:** the old source mishandles synthetic unowned/unreadable steps;
  the scoped candidate fixes that decision in the retained controls.
- **Not observed in the historical run:** that dispatch defect in the saved
  step-event/context fields. This is not an explanation for the fatal dialog.
- **Unchanged:** EXP127 remains INVALID_POST_TRACE;2113 recorded pairs remain
  provisional boundaries. Healthy session, crash cause, native callback effects,
  arena/lifetime/extent and integrated semantics are not promoted.
- **Affected reuse:** EXP030's cold/positive controls do not establish foreign
  exception ownership. Its exact tracer is referenced by EXP031/window_run.py
  and EXP127/run_window.py. Reuse needs the ownership correction and independent
  qualification; no claim that all earlier observations are false follows.

The next tool-specific test is bounded and disposable: reuse the existing
EXP029/030 owned heartbeat target for an execute-breakpoint positive, and add one
deliberately raised single-step event with a known target-side handler. Compare
handled versus passed-through behavior, exact context writes, target handler
receipt, debugger absence and post-detach heartbeat/clean exit. The saved source
and corrected candidate must be pinned. An unhandled event, failed restoration,
missing handler/control or dead target invalidates that arm. This is a native
instrument control, **not FF12 evidence**. Do not rerun the unchanged four-slot
game recipe to qualify it.

Even if that disposable control succeeds, any later FF12 trace needs separately
qualified state, a narrowly justified event budget, and an actual post-detach
response/normal exit plus fatal-dialog check. The previous dialog appeared about
47seconds after the last logged hit; an immediate CPU sample cannot exclude that
delayed failure. No causal health interval is inferred from that one delay.

The independent EXP127 review is
`Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-EXP127-SKELETAL-FAILED-SESSION.md`.
Its raw-hit acceptance does not establish that the program was healthy before
the visible error. ASTRA preserves that stricter limit. The independent review
of this new instrument finding and OPUS arena-consumer acknowledgement are queued.

## Reproduce and cleanup

Run `check.py` using the existing analysis Python. Without `--write` it only
reads retained evidence and runs disposable Python fixtures. Empty/malformed or
unmatched evidence cannot satisfy its assertions. `--write` refuses to overwrite
the original result. `validation.txt` records the final source/receipt recheck.

No FF12 process was launched/opened, no PC-control session or @runtime reservation
was acquired, and no native instrument was attached. No save/config/reference
restoration was needed or performed. Last actual full save/reference restoration
remains the separately recorded07:27:13UTC checkpoint; do not restore that old
backup over subsequent user state. Database L1+L2 completion remains open.
