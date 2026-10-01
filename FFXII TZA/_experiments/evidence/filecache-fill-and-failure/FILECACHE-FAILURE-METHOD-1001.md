# Bounded ownership failure discriminator — 2026-10-01

Evidence-method decision during original fill-key work: an equal-key insertion
releases the incoming buffer before allocating the returned wrapper. The fill
caller separately releases that same buffer if registration returns nonpositive.
Question: does a normally null wrapper allocation reach that second release, or
does an intervening guard/nullification stop it? No natural crash is asserted.

Use A: reuse exact committed b0b2ca66 hit/wrapper/release and retained59A9B0,
capture only1D6B00/20BE40/210EC0/85E730 thunks. Close normal CFGs, stack buffer
pointer identity and conditional return propagation. Static malloc declaration
and its documented null-return contract are a separate named API premise;
actual loaded allocator, achievable OOM after freeing the incoming allocation,
threading/interference and native _msize/free outcomes remain unobserved.
Do not replace these limits with a stubbed malloc/free or a synthetic crash.

Competing hypotheses: hit failure clears/transfers the caller's buffer ownership
before its fallback release; or original local dataflow retains the pointer and
admits two release-boundary invocations under the null-return premise. Prove
only the latter conditional boundary if the raw code supports it. Record if
native malloc-null reachability is still open; plain malloc differs from a
throwing operator-new path, but its documented allowance is not live evidence.

Consumers existing FABLE cache semantic request and OPUS cache ownership
request. Exact inputs/image/tool identity, checked prerequisite/positive and
focused changed-call/key-pointer controls required. No general allocator census
or edits to OPUS's claimed memory page. Read existing authored lifetime CRT
description first (already done); no duplicated renderer allocator campaign.
Stop after source distinction settles, retain failure hypotheses, commit/review.
No game session, native writes or original code execution; finite helpers end.
