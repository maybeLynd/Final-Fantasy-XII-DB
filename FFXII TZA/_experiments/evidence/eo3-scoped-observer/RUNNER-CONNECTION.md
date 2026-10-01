# ASTRA — one prepared EO3 capture, still pending native use and review

This continues FABLE-REQ-ASTRA-EO3-PATH-POINTER after48735c54b/37b724494.
Method is offline source connection and synthetic dispatch. The question is
whether the separately controlled pieces can be connected without accepting a
wrong process, partial chain, stale context or failed cleanup as a useful live
result. No new FF12 process, native fixture or original-code execution occurred.

`run_eo3.py` connects the existing capture_scoped_v2, EO3Callback, Recorder,
Probe class and source/AST-pinned owned abort. The CLI requires an explicit
prepared directory, source/identity/setup receipt pins, an active ASTRA @runtime
claim and --execute. It launches no game and sends no input. Preparation receipt
hashes do not by themselves prove save/state/Cloud correctness; those underlying
receipts must be established and read before choosing to execute.

Before debugger attachment, the capture's own opened handle must identify the
prepared PID, creation time, designated path and exact reference file hash.
The native branch reuses the prior module census, preferred-base and read
controls, full selected .text comparison and exact retained function-body bytes.
It additionally requires a successful no-debugger query. These are sequential
reference checks, not an atomic state snapshot or a guarantee about unobserved
module state. This CLI-native qualification was not invoked in the synthetic
connection tests: its outputs there are explicitly supplied.

The recorder clock starts after qualification and immediately before attachment,
so it includes attachment latency and is conservative relative to the ten-second
armed window. It excludes manual state establishment and slow source/module
qualification. It cannot extend the allowed armed exposure. `armed.json` is
written only after all recorded initial thread arming succeeds and that initial
stopped event is continued. The input orchestrator must observe this receipt;
an issued command or an arbitrary delay is not proof that the recorder is ready.
The complete synthetic chain uses the producer, builder and issuer contexts on
their supplied, initially armed threads. It remains
OBSERVATION_PENDING_SESSION_HEALTH, with no input, health or restoration claim.

Stop handling is cooperative at event-loop polling boundaries. A persistent
STOP file prevents another execution and ends the current capture at the next
eligible poll. It permits only the existing cleanup loop to finish; no capture
or UI input restarts. A request arriving while another bounded call is running
cannot make that call atomic or instantly cancel it. User takeover still ends
input automation immediately through the controller's own stop mechanism.

The additional timing control found an actual connection defect before native
use: a stop first seen inside cleanup prevented debug-register clearing.
`cleanup-stop-repro.initial.json`, the exact earlier sources and
`cleanup-stop-correction.md` retain it. The guard now recognizes the existing
timeout_cleanup_begin marker and allows cleanup to service its events. Both
stop-after-producer and stop-arriving-in-cleanup controls require clearing and
detach, with no further semantic events or test restart. Failed readiness
delivery also ends capture after the caller has recorded successful event
continuation; it cannot throw while the caller still thinks that event is
pending. Failed arming never reports readiness.

The first full connection test had not exercised the CLI import path. Source
inspection caught missing access to the frozen original helper directory.
`frozen_loader()` now imports the exact declarations and verifies the Audit
origin without calling the native load_source function in offline controls.
The initial connection observation and source remain. A later source recheck
failure invalidates the result while still preserving the API/result receipts.

The connected controls distinguish a complete chain, partial timeout, high-pointer
hold, stale context, changed process lifetime, failed reference qualification,
stop during capture, stop during cleanup, failed arming and failed readiness
delivery. They execute the real Python connection/dispatch functions with
supplied event/context/memory APIs. They do not prove native delivery, actual
initialization, allocator placement, normal caller reachability, game health or
save restoration. Existing native effect/abort evidence remains unchanged.

Independent review stays ASTRA-REVIEW-EO3-STOPPED-OBSERVER; its review must include
the final connected runner and the new cleanup timing counterexample. No
independent acceptance is self-awarded. The live experiment and any canonical
EO3 promotion remain open. The normal next live step, once review permits use,
is the exact state/trigger and post-detach health/restoration procedure in
LIVE-RUN-PLAN.md, with fresh receipts and active authorization. Database L1+L2
completion remains the goal, not this runner's passing controls.
