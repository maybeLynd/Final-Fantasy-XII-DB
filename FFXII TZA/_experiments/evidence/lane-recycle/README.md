# Lane callback identity and conditional local recycling

Method A, verified shipping machine-code rules. Producer valid; independent
review and canonical incorporation pending. Full L1+L2 goal remains ACTIVE.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
imagebase120000; shared reviewed adapter in actual invocation path. Three new
complete bodies/1001B and retained qualified lane source reused without recapture.

Player version: a load-completion ticket names a resource slot and lane. The
completion checks who owns that slot now. That check alone does not identify
the owner that originally submitted the load. The examined recycler also does
not use the pending flag as a local guard. We still need the real service rules
that prevent old completions from arriving after reuse; no gameplay failure or
unsafe natural sequence is claimed by these local rules.

2E6EB0 builds callback2E4E50 with DWORDtag=(u16 sub-record+20<<16)|lane.
The receiver splits high16 slot/low16 lane, then compares CURRENT sub-record+5C
with CURRENT node+24 selected by CURRENT+22. No original submitting-generation
operand is in this tag. A coherent current generation is not an old-ticket fence.

Reached2E6A80 tests loaded+24|mask28 to call2E9470. Complete2E9470 never
reads pending+34 or calls another function: after normal valid-list operations
it invalidates node index and puts the same storage on free head0215FD70.
Nonzero pending alone does not prevent this local push.2E2660 subsequently
clears all32 lane handles and pending+34 while rebinding node/generation,
without making a release call for the old handles. Natural outstanding-read
or actual reuse histories are outside this proof.

The additional named group-release writer2E4000 tests requested+2C before its
enqueue arm, so an already-requested lane alone does not cause a new enqueue
there either. A different lane or other producer may queue the same shared node.
This is not a global proof of no relink producer.

Pending+34 is not sufficient evidence of a newly accepted asynchronous read:
the requester can set it on an existing-nonzero-handle arm without32E620, and
the new-request arm sets it AFTER32E620 returns. Input/call sent, queue accepted,
completion executed and consequences remain distinct.

Premises: valid array/list/metadata/lane0..31, normal ABI/returns and no
interfering writes. No natural late callback, overlap, leak, crash or universal
safety/unsafety result. Other service contracts could prevent late delivery.
Composed static paths are not native runs or evidence of gameplay reachability.

Reproduce capture/reducer in a writable copy within this repo with the exact
reference EXE and fresh outputs. Actual CLI controls reuse positive01 and
refuse failed capture, missing retained source, changed ticket field and inverted
recycler gate; no result from refusal. Producer checks, independent acceptance
and canonical incorporation remain separate. No external audit credit.

Consumers: FABLE current-owner versus submitting-owner lifetime semantics;
OPUS actual recycle site, ticket and pending preconditions; FRONTIER exact future
scheduling question. Next: original caller/service cancellation/drain guarantees
with accepted IO identity, rather than pending-bit sampling or a forced callback.
No game/PC/native/emulated execution, instruments, save/config/reference changes.
