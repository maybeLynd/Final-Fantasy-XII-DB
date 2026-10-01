# Owner admission needs a separate reset/retirement premise

**Method A producer evidence; independent review and scope adjudication pending.**
No native execution, live process, natural two-request observation or whole OV closure.

The existing OV36 producer checks only these two instructions for its O claim:
`003DDA3B CMP DWORD[owner+4],0` and `003DDA4E MOV DWORD[owner+4],2`.
Its unmodified actual CLI still exits0/FAILS0. That preserves the admission
fact; it does not check the stronger headline “an owner has one live request”
across a separate owner reset. This is a scope defect in sufficiency, not an
automatic rejection of all OV36 or of its valid per-slot delivery evidence.

Original `003DD790(group)` unconditionally clears each owner handle+state
qword, assigns local identities and clears that group's pending mask. It has
no entry-state test or local call. Its same owner `+4` is what the armer tests.
The reset69B are reused unchanged from owner-reset-barrier/qualified-02;
only the missing76B armer source was captured. Both match the certified EXE
and SECTION09 original-body hashes. Shared reviewed access roles are actually
used and checked; reset/store/address identities are not guessed from prose.

The exact conditional discriminator uses valid group1/slot0, owner `02B58360`:

| Conditional input | After original reset | Original armer admission | Queue marker |
|---|---|---|---|
| state3; a pending request still exists | state0 | accepts, writes state2 | unchanged by these local functions |
| state5; a pending request still exists | state0 | accepts, writes state2 | unchanged by these local functions |

These are source-compositional countermodels **if reset precedes retirement**.
The queue marker is abstract; it is not a captured or executed queue slot.
No original second submission occurred. A normal-caller/FIFO/disabled-producer
invariant may exclude both cases. Admission alone cannot provide that exclusion.
Ordinary queued primary delivery and the D4 synchronous override/world reset
must be kept separate while proving it. This is the next static discriminator.

`prove_owner_admission_scope.py` checks capture exit/stdout/stderr/driver,
immutable reset manifest/member, SECTION09 manifest, original bytes, exact
state/address/loop operations, armer memory reads and actual O predicate AST.
An upstream FAIL cannot be suppressed by the old check's PASS. Four actual CLI
refusals cover failed capture, changed armer, missing retained reset source
and failed original O invocation; each exits nonzero with no result.

First controls01 was incomplete: changed armer correctly failed at the earlier
immutable range-hash gate, while the control expected the later byte-comparison
message. Preserve that run, stdout/stderr and controller preimage. Corrected
controls02 passes all four actual refusals; the scientific proof01 did not
change or rerun. No prior game evidence depended on this diagnostic expectation.
Failed fixture input copies remain immutable in owned preparation; their
bytes match the corresponding qualified02 fixtures. The additive failure map
records these hashes rather than counting the incomplete run as PASS.

Reproduce with a fresh output path, this packet as reducer source, repository
Python/Capstone5.0.7 and the pinned canonical owner-reset/SECTION09 dependencies.
All tools are terminal; original binaries, saves/configuration and peer files
are untouched. Source algebra, producer control and independent acceptance
remain separate.

FABLE must narrow or justify the stronger O headline; OPUS owns the downstream
owner lifetime/type contracts. SPEC independently checks source/control scope.
Preserve D/P/H's existing per-slot result and explicit reentrancy limits.
