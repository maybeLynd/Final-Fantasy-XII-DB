# EO3: one stop retains both pointer forms

This package corrects a required observation boundary and qualifies parts of a
scoped recorder. It contains **no fresh FF12 observation or original-code
execution**. The live EO3 allocator/caller/issuance question remains open.

The original bytes `8B D7 B9 FF 00 00 00` at0032E846 are `mov edx,edi` and
`mov ecx,FF`. They do not change RDI. Immediately before the call at0032E84D,
one context therefore contains **RDI=P, RDX=zero_extend(low32(P)), ECX=FF**.
FABLE's current resource-request-queue EO3 table says the earlier0032E846 stop
is the only place the full pointer exists and both stops are necessary. That is
incorrect for this sequence. `staging.json` retains exact bytes and register
effects; `qualify_boundaries.py` checks the complete retained bodies against the
hash-identified original executable. The consumer correction is pending, not
silently applied to peer-owned prose. A pre-call stop still does not prove the
call executes or completes.

The producer's caller return is atRSP+38. The completed builder's RSP is40 below
the producer's, with return0032E852 at its ownRSP+38. These original prologue/call
facts permit correlation by thread and frame, including nested builder pumping.
The issuer additionally needs the same aligned pool slot and request ID. A slot
address alone can join different occupants. Full selected slot snapshots retain
state, kind, low32 path value, count, offset and both destination fields.

The usual candidate hit list omits RDI, R10, RBX and RAX. `project.py` requires
successful observed GetThreadContext bytes with AMD64 CONTROL and INTEGER groups.
The local SDK and frozen helper declarations agree on1232-byte layout/offsets.
`project_control.py` reuses42 known-gate context reads from the prior21-hit native
fixture, checking its known above4GiB RCX/RBX values. These are repeated reads of
existing events, not42 new events or game states. All57 retained no-INTEGER reads
are rejected. RDI/R10 semantic values are not independently seeded in this prior
fixture. SetThreadContext proposals and failed/short reads are not observations.

`match.py` tests frame/return/slot/ID correlation with supplied Python records.
`observe.py` adds bounded reads, preservation of raw context/read receipts and
stop decisions. `control.json` and `recorder-control.json` are explicitly
**synthetic instrument controls**, including reentry, reused IDs, wrong sites,
failed/short reads, missing flags, empty/incomplete chains and exhausted budgets.
They establish these decisions, not Windows delivery, process/thread binding or
game behavior. The retained initial generator versions are history, not current
verification entrypoints.

The recorder's first complete chain is only `STOP_MATCHED_PENDING_HEALTH`.
A selected P!=sign_extend(low32(P)) at the producer requests
`HOLD_FOR_OWNED_ABORT` before enqueue: it retains a useful producer sample but
cannot assert issuance/consequence. **Do not connect this to the old candidate's
unconditional resume path.** No FF12 adapter or launcher is included. Required
next work is the owned-event/receipt binding, bounded stopped-event read adapter,
and verified pending-event abort/cleanup, followed by the small native feasibility
control. The existing FP-context counterexample remains; no narrower-flags fix
or scheduling transparency is asserted. EXP127 remains INVALID_POST_TRACE.

`PLAN.md` names the question, consumers, exact state/trigger provenance, competing
cases, budget, controls, acceptance limits and future restoration requirements.
The historical Stepping-to-Eastgate route is preparation, not a fresh guarantee
that the gated primary requester executes. No saves, config, reference binary or
game process were modified here. PC control remained off; the last full original
game restoration receipt is still the prior07:27:13UTC receipt.

Run `check.py` with the repository venv Python. It validates the manifest when
present and replays the bounded controls read-only; writes require explicit
`--write` and use exclusive output creation. Passing it is not live readiness or
database completion. FABLE and OPUS must consume any supported claim changes.

Player version: one correctly placed observation can compare a loading file's
original memory address with its shortened version. The recorder is being
prepared to follow that same file through the queue and stop safely if the
address changes. No new loading crash or game behavior is claimed.


The subsequent retained-receipt binding check (`bind_contexts.py`) identifies the
21 original observer events and their separate21 resume rereads. It joins
WaitForDebugEvent -> OpenThread -> successful GetThreadContext -> full raw
context -> same-event continuation, verifies the owned execute-breakpoint cause,
and reproduces the frozen capture hit sequence. Deliberate wrong thread/handle,
write proposal, wrong DR6, foreign PID, missing continuation and empty-journal
controls reject. CloseHandle was not logged: this is ordered source/receipt
binding, not an independent handle-lifetime census. The live adapter and its
pending-event abort still require qualification. No new events were captured.


## Native reader feasibility follow-up — ASTRA, 2026-09-21

`native-reader-1` is a fresh **native instrument control with supplied data**,
separate from both shipping FF12 code execution and live FF12. The existing
`runtime_probe.py` Probe class was extracted from its frozen source; its CLI,
process search and game attach were not executed. A directly launched Python
child allocated two data pages, placed a known NUL-terminated fixture path at the
first page's end and made the second page NOACCESS. Its actual path address was
0x1896E8C0FDF, above4GiB. The parent used only read/query access to that child.

Exact full-width and final-readable-byte controls passed. Crossing the boundary
or reading the protected page failed with error299 and **zero bytes transferred**;
these do not demonstrate a native nonzero partial transfer. The existing reader
returned None, rather than buffer contents. Reading bytes only through the first
NUL succeeded, and an exact positive repeated after the failures succeeded.
Native source/selected Python and kernel32 identities, raw API returns/counts,
parent/child/image identity and cleanup receipts are retained. This is not a full
forwarded-module census. No reference executable, saves, config or FF12 process
was touched; no debugger or PC control was used.

The child38728 was directly owned by parent46232, freed its allocation, reported
no debugger and exited0. The parent closed its read handle. No force-stop was
needed. `native_read_check.py` replays these receipts without native calls and
rejects corrupt identity, address width, failure results, cleanup and positive
controls. It qualifies this reader behavior on supplied stable memory only.
Live memory lifetime, debug-event binding/reads, pending-event abort and FF12
session health remain unqualified. Do not interpret this as a new game result.


## Stopped-event read and abort controls — ASTRA, 2026-09-21

The next native controls reuse the existing FP fixture, frozen owned-event
predicate, cleanup and API observer, and the existing Probe. They add a bounded
stopped callback and explicit abort branch; **no FF12 or shipping instructions
are executed**. `STOP-CONTROL-PLAN.md` records the experiment before the runs.
`capture_scoped.py` invokes the callback only after exception ownership is
established and before the resume-context write. The observer preserves the
native thread-handle/context/event connection, full GPR bytes, exact stopped
code/path/counter reads and raw API ordering. Supplied RDI and R10 pointers are
above4GiB; RAX has a distinct64-bit seed. Nonvolatile RDI is saved/restored by the
labelled fixture additions. The old FP body remains around those additions.

Two stages are retained, with different claims:

- `native-stop-*`: a stop on the original fixture's NOP. Normal resume advanced
  the following shared counter; both aborts left it unchanged. These establish
  successor-counter effects only. **A NOP could execute without changing that
  counter**, so these runs do not establish execution/nonexecution of the stopped
  instruction. Their raw results were retained and the boundary was corrected.
- `native-instruction-*`: the same binary body, with the breakpoint moved one
  byte forward onto `INC qword [RBX+A08]` itself. Normal resume committed that
  stopped instruction's counter effect. Both the requested abort and deliberate
  NOACCESS-read failure left that effect uncommitted through verified process
  exit. This is an architectural memory-effect observation, not a claim about
  invisible micro-operations or every instruction/host.

For each stage, the normal arm had stopped counters5/4, final9/9, continued
native sentinel returns, successful debug-register clear/readback and detach,
no debugger, normal exit and explicit code/mapping cleanup. The abort arms
terminated the exact parent/nonce/image/creation-identified disposable subject
with exitEA03; the pending event and process-exit event were serviced and terminal
state was verified. No resume Get/SetThreadContext occurred after the hold
choice. Counters stayed5/4. They remain **CONTROL_ABORTED**, not healthy semantic
captures. The killed targets did not run finally: there is no target VirtualFree
receipt or graceful-restoration claim for them. Parent handles/mappings closed,
all target/debugger processes ended and no supervisor emergency kill was needed.

The native NOACCESS control returned failure/error299 with zero transferred
bytes after valid stopped reads. It triggered abort, with the raw useful stopped
observation preserved separately and no successful semantic observation appended.
Raw `error` values on successful ReadProcessMemory/TerminateProcess calls are
GetLastError values and can be stale (18 here); API return and transferred count,
not a stale last-error field, determine success.

`native_stop_check.py` and `native_instruction_stop_check.py` independently reduce
raw context/API order, process identity, mapped fixture bytes, shared markers and
cleanup, with corrupt-event/ownership/continuation/effect controls. The initial
synthetic dispatch replay caught a tuple-versus-JSON-array comparison defect
before native runs. Its source/receipt and repair note remain; normalization
fixed replay without changing the branch result. No prior published game claim
was dependent on that new checker.

`eo3_callback.py` connects the same event/context/probe shape to the scoped EO3
recorder. Its own three-site connection is **synthetically checked**: ordinary
correlation completes, changed-pointer producer requests hold, stale/foreign/
second-chance/proposed-write contexts reject. This is not a fresh native FF12
three-site test. A live runner still must establish designated process/reference
identity and save/state/trigger, supply the tested bounded cleanup/abort handling,
and perform real post-detach responsiveness/fatal-dialog/restoration checks.
Independent review is requested for this high-impact connection and abort
boundary. The existing FIP counterexample and EXP127 INVALID_POST_TRACE are
unchanged; neither historical crash cause nor real game allocation is closed.

Player version: the recorder can distinguish stopping before an observed memory
change from closing the test program after it happened. That confidence is
bounded to this controlled native program. The real area's file-loading request
still needs its own identity, normal trigger and healthy-session evidence.


## Explicit-completion correction — ASTRA, 2026-09-21

Pre-live falsification found that the old capture status could label one
CONTINUE observation followed by timeout MATCHED_PENDING_HEALTH. The raw first
reproducer is retained in timeout-repro.initial.json. The old native source
remains unchanged for identity/replay; use capture_scoped_v2.py for the next
candidate. It requires an explicit completed-request stop and a successful
continuation before recording a match. Empty/partial clean timeouts are
INCOMPLETE; failed cleanup remains INVALID. Recorder.finish and actual game
health remain independent requirements.

Read timeout-completion-correction.md for the dependency assessment and the
small offline regression. No previously collected native control depended on
CONTINUE-plus-timeout acceptance, and no EO3 live result exists to promote.
Native v1 control evidence does not become a fresh native v2 run.

LIVE-RUN-PLAN.md binds the selected three phases to the existing Stepping route,
exact save/reference identity, positive controls, budget, changed-file
restoration and explicit unresolved operating work. At the selected producer
RCX=FF; the copied path is in RDI. No extra pre-MOV breakpoint is needed.
Independent review is still queued; actual FF12 allocation/issuance stays open.


## Designated-lifetime abort adapter — ASTRA, 2026-09-21

OWNED-ABORT-ADAPTER.md and owned_game_abort.py reuse the exact source/AST-pinned
pending-event abort body from the native controls. The supplied designated
image/lifetime is checked before that existing body rechecks the opened handle.
Synthetic controls reject stale identity, foreign events, failed termination
and an unexpected exit code. This is a connection check, not a new native/game
run or proof of the supplied identity's provenance. The earlier native reader
had no creation-time receipt; the stale-time test value is explicitly supplied,
not attributed to that earlier subject. Its initial checker-schema failure and
correction remain. The live runner's attach/setup/health obligations stay open.


## Connected runner and cleanup-stop counterexample — ASTRA, 2026-09-21

RUNNER-CONNECTION.md describes run_eo3.py, which connects the existing capture,
EO3 recorder, reader and retained abort. Synthetic complete-chain evidence stays
pending actual session health; wrong lifetime/reference and stale context reject.
The timing challenge found that a stop arriving inside timeout cleanup initially
prevented clearing. That failed path, source and correction are retained; both
stop timings now permit clearing/detach without another semantic capture. Failed
arming/readiness cannot signal a prepared recorder. The clock starts after
qualification and conservatively includes attachment time. The CLI native
qualification, actual game state and health/restoration remain unperformed.
This candidate awaits independent review; no live result is established.
