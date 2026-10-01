# Native qualification of the scoped exception-dispatch correction

ASTRA, 2026-09-21. **Disposable native instrument controls; live_game=false.**
This executes our own two-byte RET and a deliberately raised Windows exception.
It is neither shipping FF12 execution nor a gameplay observation. No experiment
number, database parity credit or healthy-FF12 claim is awarded.

Player version: a tiny test program confirms that the old measuring tool can
swallow an exception that belongs to the program. The corrected decision lets
the program's handler receive it. The correction still detects its own breakpoint,
and every test program was detached and exited normally.

## Question and competing explanations

The preceding package (`../exp127-instrument-control`, commit
`0bae8fe6398da8ccc2a519593fb54c8cf3653840`) demonstrates the dispatch defect
synthetically. Does that decision actually change native target-side exception
delivery, and can the corrected function still service its own execute breakpoint?

H1: the historical tracer's handled reply suppresses the target's handler;
the corrected unhandled reply permits delivery with no resume write at that
foreign event. H2: the target handler receives the exception regardless, or the
candidate loses the owned-breakpoint/cleanup control. Existing FF12 traces cannot
distinguish these because none contains the demonstrated foreign-step case.

The cheapest sufficient next method is a disposable Windows process. The test
reuses EXP029's allocated RET heartbeat and the exact frozen EXP030 helpers;
it adds one target-side vectored handler and one explicit self-raise. No general
debugger, runtime service or laboratory was built.

## Identity, state, controls and budget

`run.py` launches only Popen-owned child/debugger processes through
`C:\Python314\python.exe`. Their actual PID and source hash must match the
ready/plan records. Each arm pins the exact original four sources, candidate
functions, ownership predicate and runner before attach. Sources are the unchanged
ones in the preceding committed package; the candidate was not edited for this run.

Every target first raises exception80000004 **without a debugger** and verifies
one invocation of its installed handler. That is the detection control for any
later missing delivery. The target executes its RET every50ms and writes an
independent heartbeat. In the two foreign-event arms, the wrapper creates the
raise trigger only after the first owned breakpoint has been continued. The
trigger is a labelled experimental intervention, not an ordinary program fault.

Budget: three fresh disposable targets, at most one second of capture per arm,
10seconds for each debugger,15seconds for each target. An initial control failure
would stop the sequence; there were no retries. No user window or PC-control
session was opened. The wrapper adds first-chance receipts but does not alter the
native event, context or continuation arguments it observes.

Python3.14.6, MSC1944 AMD64; host reports Windows11 build26200.
`tool-identity-after.json` preserves Python EXE/DLL and kernel32/KernelBase/ntdll
file SHA256s. **These disk identities were read after the run**, not a complete
before/after in-process module census. The source hashes were checked before
execution. This narrower provenance is sufficient to identify the tested tool
recipe, but must not be presented as full native-module integrity proof.

## Raw evidence and independently reduced observation

Each arm retains plan, target-ready/baseline, raw API log, capture result,
target-side delivery/exit records, heartbeats, logs and wrapper result.
`check.py` reduces the raw event/continuation intervals and handler effects;
`normalized.json` pins all arm artifacts by SHA256.

| Arm | Target / debugger PID | Owned main hits | Foreign event context writes | Foreign reply | Additional handler delivery |
|---|---|---:|---:|---|---:|
| Candidate owned positive | 21596 / 46208 | 21 | no foreign event | — | — |
| Historical foreign event | 35340 / 51908 | 2 | 1 | DBG_CONTINUE | 0 |
| Candidate foreign event | 51556 / 33124 | 2 | 0 | DBG_EXCEPTION_NOT_HANDLED | 1 |

Both foreign events are first chance, at the self-raise's native address rather
than the configured RET. The historical path writes RF/DR6 and reports the
exception handled. Its handler count stays at the baseline1. The candidate
makes no SetThreadContext call between that foreign event and its continuation;
the target then records a second handler invocation with matching thread,
exception code and exception address. Both self-raises return to the target.

The positive capture is PASS. **Both foreign-event captures remain INVALID**
because they encountered an unexpected event. Their expected rejection, different
delivery effects and successful cleanup satisfy this deliberately adversarial
instrument control; neither invalid capture is relabelled as a valid trace.

Microsoft documents the distinction between handled and unhandled continuation
in [ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent).
Here it is supported by target-side observations as well as the API reply.

Five malformed-receipt controls are rejected: zero positive hits, handled reply
substituted for the candidate's reply, missing handler delivery, empty API log,
and a context write inserted into the candidate's foreign-event interval.
A success label, a clean exit or an empty population cannot pass this checker.

## Interpretation, affected claims and limits

**Established:** the old capture's foreign-step decision changes native handler
delivery in this controlled program. The candidate fixes that decision in the
tested path while retaining an owned execute-breakpoint positive and normal
cleanup. This is a demonstrated instrument effect, not merely a return-code test.

**Still unproved:** native foreign-event handling specifically during cleanup;
same-RIP TF/mixed-cause cases outside the synthetic controls; arbitrary failures,
thread churn or prior debug-register preservation; full-context write harmlessness;
hot/multi-slot behavior; real FF12 initialization, scheduling, health or semantics.
The fixture provides one known handler. An unhandled exception in a target with
no handler may terminate it, so passing it through is not a survival guarantee.

**EXP127 stays INVALID_POST_TRACE and its crash cause UNKNOWN.** The preceding
receipt reduction found no instance of this defect in its5658 saved step events.
This package must not be used to claim that its crash is fixed, that2113 boundary
pairs are semantic closure, or that a new unchanged four-breakpoint trace is safe.

The candidate has bounded native qualification now; its historical header and
preceding package correctly describe its earlier synthetic-only checkpoint.
They are preserved. It has not replaced any shared tool or old experiment source.
Independent review should consider both packages together before future use.
OPUS arena/skeletal consumers retain their open initialized-state questions.

## Cleanup and next use

All three arms cleared/read back debug registers at the requested stopped event,
detached, and recorded four post-detach samples with debugger absent and increasing
heartbeats. Normal stop requests led to target exit0, handler removal and allocation
free. Every debugger exited0, and no forced termination was needed. This establishes
health for these small disposable programs only.

No FF12 process, original saves/configuration or reference binary was opened or
modified. No stale game backup was restored. PC control remained off, and @runtime
was not needed for these owned disposable targets. `cleanup-observation.json`
records the later process check separately from the completed handle/exit receipts.

Reproduce the **retained evidence check** with `check.py`; it does not execute a
target. `run.py` is historical execution and refuses existing output directories;
do not run it merely to validate this package. Any future instrument extension
must be driven by a specific queued question and separately qualified. The next
FF12 trace still needs independent review, exact state/trigger, event budget,
post-detach observable response/normal exit and fatal-dialog checks.
