# EO-3: correct the observation boundary before a live trace

ASTRA, 2026-09-21, `FABLE-REQ-ASTRA-EO3-PATH-POINTER`.
Major system: resource request queue / raw-path loading. Consumers: FABLE queue
semantics, OPUS queue types/contracts, FRONTIER state/observer preparation.

## Question, hypotheses and chosen method

The existing reviewed static mechanism is a pointer narrowed to a request's
32-bit index and later sign-extended. The unresolved live question is whether
the original allocator/caller actually supplies a pointer that changes under
that roundtrip, and whether the same request reaches the reported failing read.
Alternatives: low-address allocation preserves the pointer; sign extension
changes its high half; truncation loses high bits without setting the sign bit;
or the historical crash came from another corruption/path. **Unknown cause stays
unknown.** A similarly shaped fault address is not the complete causal chain.

**Method A is sufficient for this preflight:** verify original instruction
boundaries, argument staging and the exact integer representation. Existing
captures cannot establish the missing allocator/caller linkage. No live run,
isolated execution, new instrumentation platform or broad call census is needed
to correct the requested observation sites. `check.py` preserves exact original
bodies/anchors and explicit calculated boundary examples in `observation.json`.
Those examples are instruction-semantics calculations, not original-code runs.

Controls: complete nonempty decodes, exact bytes/operands at producer/storage/
consumer sites, and sign-bit/above4GB examples distinguishing the old predicate.
Stop preparation on an identity/anchor discrepancy. Stop before live setup until
the actual state/trigger and observer feasibility/control below are satisfied.

## Two corrections

1. **A breakpoint at `0032E846` observes BEFORE `mov edx,edi`.** RDI is the source
   pointer there; EDX is not yet this instruction's output. Use the verified
   pre-call boundary **`0032E84D`** to observe the supplied EDX/RDX and ECX=FF after
   both argument instructions have executed. A hit at the call instruction alone
   does not prove the call completed. At the builder, `0032E897 mov ebp,edx`
   preserves the incoming32-bit index; `0032E902` stores **EBP**, not the then-live
   EDX, at `[r10+24]`. A stop at that store is also before its effect. The builder
   has later state/ID writes; inspect its completed-record boundary `0032E983`
   and match the actual request ID, rather than treating an early slot as complete.
2. Let `P` be the full pointer and `L=P & FFFFFFFF`. The issued pointer is
   **`Q=sign_extend_64(L)`**. A negative/sign-filled Q depends on **L's bit31**,
   not simply `P >= 80000000`. For example `P=100001000` satisfies the latter but
   becomes `Q=0000000000001000`, not `FFFFFFFF00001000`. It still loses identity.
   `P=000000018BC13000` and `P=000000008BC13000` both yield `FFFFFFFF8BC13000`;
   the resulting fault-address shape alone cannot recover the original high half.
   Exact pointer preservation requires `P==Q`; for ordinary positive user-space
   pointers that means a value below80000000. No such allocation is fabricated
   or forced here. A transformed pointer need not fault immediately if its target
   happens to be mapped; a wrong-string read is a distinct possible consequence.

The semantic page already distinguishes loss above4GB, but its preceding
"whenever at or above80000000" sentence and the queued prediction overgeneralize
the sign-filled result. The established narrowing/sign-extension mechanism stands.

## Future live evidence specification — NOT READY yet

Required reference: exact authority EXE and mapped-module/tool identities; clean
designated test process, fresh disposable backup/Cloud isolation, ordinary
responsive game baseline. Reuse the established modern Stepping000 or old
Southgate004 load route only after static/captured evidence identifies which
normal transition triggers the intended raw-path requester. **An arbitrary area
load is not a positive control for this path.** Missing: exact scene/action and
expected raw-path request, plus failure-aware observer qualification following
EXP-127. Do not repeat its unchanged four-breakpoint design.

Required correlated observations, which may demand a narrower experiment than
the original boot-plus-load request:

- Producer pre-call `0032E84D`: thread/call instance, full RDI=P, RDX/EDX=L,
  ECX=FF, expected return boundary and bounded source bytes when readable.
- Completed builder `0032E983`: R10 slot within the actual64-slot pool,
  state/kind/index/request-ID and relevant destination/length. Match the producer
  invocation; the builder can pump/reenter while no free slot exists, so "the next
  hit on the same thread" is insufficient by itself.
- Issuer pre-call `0032E111`: RBX slot **and the same live request ID**, kindFF,
  nonzero count, stored+24=L, RCX=Q, destination and offset. Slot address alone
  does not identify a request across reuse. The normal arm additionally requires
  the read layer's idle check; any omitted branch remains a limit.
- A consequence claim additionally needs the actual fallback path into
  `001D6D90` and its first source-byte read at `001D6E20`. That instruction also
  runs for later characters: subsequent RBX values are cursor advances, not new
  original path pointers. Do not infer the fallback merely from issuance.

Start with **one correctly correlated request**, not a broad trace. Suggested
maximum feasibility exposure:10seconds of instrumentation or8 producer hits,
whichever arrives first; at most32KiB event payload,128readable path bytes each.
One known normal low-pointer request is a delivery/observer positive control;
exact pre/post instruction-state fixtures or equivalent validated observer tests
must establish capture phase and request matching. Include a no-trigger baseline;
zero path hits mean no evidence, not safety. Only enlarge the capture if the small
probe actually discriminates and a canonical consumer needs more cases.

Acceptance: complete matched producer/builder/issuer records, exact identity,
qualified observer, no dropped/misordered required events, healthy responsive
game after detach. Low pointers establish only the sampled allocations. A P!=Q
pair proves narrowing changed that request's pointer; proving a historical crash
cause additionally needs the matched consequence or separately justified original
execution, not a guessed association with a prior exception address.

Failure/stop: missing control, ambiguous reused slot, unavailable observer,
unexpected module/state, timeout/budget, user stop/takeover or unhealthy/fatal
session. Do not deliberately provoke a native fault. Preserve failed traces as
provisional, revoke semantic acceptance on failed game health, and use the existing
authorized safe-close/restart cleanup for the designated disposable instance.
Never patch the queue merely to keep an experiment green. Restore/verify original
saves/config, detach/close handles, verify process responsiveness or safe absence,
check reference identity, and end PC control as soon as unused.

Raw identity and boundary observations, normalized matched records, rejected
records/reasons, controls, health and restoration receipts must reach the named
consumers. No fresh runtime claim is closed by this preflight.

Player version: a file-loading request may squeeze a memory address into too few
bits. Before testing whether that explains a crash, we must record the address
after the game has filled it and follow the same request through loading. Watching
the wrong moment could make the test report an unrelated old value.
