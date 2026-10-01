# Conditional queue wait before indexed owner reset

**STATIC_ONLY; independent review and incorporation pending.** This answers
the exact local prerequisite, not actual pending-owner survival or fullOV19/21.

Original266D10 calls32F430 at266DE6 before its all80 owner-record reset at
267112 ->3DD7E0. Its local CFG establishes that order with opaque calls assumed
to return normally. The body ends in tail3EC620 at2671AC, not RET; the omitted
tail is an explicit boundary. The related binder26C8C0 restores its frame and
tail-jumps3DD790 at26CDE3 with the original group argument inECX.

**The named queue wait is conditional.** 32F430 finishes its5-iteration loop,
uses kind8/index0350 for the size query, and tests its signed result at32F623.
JLE32F625 skips the submit/wait segment. Positive length normally reaches
32E520(0) at32F68D. Under a null runtime size override at022C5230 and the
selected unchanged retained FST, the twelve existing regional tables give
3840 in eleven cases and-1 inUK. Thus a universal wait-at-this-site premise
is false; the table calculation/source branch requires no gameplay.

32E520(0) calls the pump, checks pending-head022C51C0, then the service query;
it repeats through35EA30 until the sequential checks permit a normal return.
Those checks do not prove an atomic, persistently empty queue, a deadline,
successful IO or all-owner cleanup. The nonpositive32F692 suffix still has
opaque callees, including3EA6B0. World/binder have other opaque work. The
finding does **not** prove UK never waits elsewhere, that an actual process
selects UK/null override, or that an older callback reaches a reset/reused
owner. No local tail proves all its transitive effects.

Reproduction:

    python prove_owner_reset_barrier.py FRESH_RESULT.json
    python control_owner_reset_barrier.py FRESH_DIRECTORY

Required original capture/driver/exit/stdout/stderr, actual shared reviewed
access-role adapter, direct shipping EXE reread and pinned upstream manifest
are checked on this invocation. Existing bts-index-binding publication
fdc46b6eba1cf92e283290d1737fd55f945157d0 supplies the exact12 retained FSTs;
manifestc57c6b668c5b567014a01c5da45dcbf7899645e4547a6bc310edce0972891abb.
The reducer reads those full bytes and retains offset163392/rawDWORD/hash.
No new archive extraction or repeated broad resource census.

Capture01 succeeds. Failed producer01 guessed the ECX8 instruction at32F666;
actual32F666 is a stack store and the ECX8 instruction is32F66B. Failed02
refused the world tail3EC620 as unclosed. Both exits/preimages remain, no
semantic result was created by either failure. Corrected03 succeeds; final04
additionally pins the existing retained manifest. No central CFG guard or UC1
extent/catalogue policy changed. Four actual CLI controls refuse failed
capture, missing wait body, coherently changed size-branch bytes, and absent
retained FSTs; invalid/incomplete/empty inputs cannot pass.

Affected consumers: FABLE indexed-source/queue/world initialization/lifetime
prose and OPUS callback-owner/reset preconditions. Preserve SECTION09's earned
synthetic reset footprints and all real scheduling/ownership/reuse gaps.
Independent source acceptance and exact canonical incorporation are required.
This is one new bounded source/data answer, no additional formerly-runtime row
retirement. Existing compressed Esper-order causal correction remains the
current checkpoint's one eliminated live-labelled causal proposition.

No native/emulated FF12/game/PC process, instrumentation, save, config or
reference mutation. Only file reads/own fixtures/synchronous checked tools;
all finished tools exit. Parked menu extension remains unapproved and its
spent allowance persists. FullL1+L2 goal ACTIVE/NOT_MET; reviews are not a stop.

## Delivery qualification02

The initial uncommitted publication failed on three generated .pyc caches.
The actual freezer now excludes only interpreter-cache artifacts; original
70-member frozen candidate and failed publication receipts remain unchanged.
All primary bytes/results/controls are retained; no scientific rerun or new
acceptance. This qualified02 packet is the committed delivery.
