# IsOpen is a sentinel predicate, not cache-view validation

MethodA STATIC_ONLY. This package settles an exact downstream question from the
allocation-zero evidence: IsOpen can return true when the selected cache-view
field is zero. It does not establish that normal play reaches allocation failure,
that a later getter runs, or that a read crashes.

For the player: the engine's “file open” check is bookkeeping, not a test that
usable file data exists. Reconstruction must preserve the original sentinel
rules and avoid treating this boolean as a valid-pointer guarantee.

## Original predicate and counterexample

Complete shipping59D920..59D93B is27 bytes, ten instructions, no calls/writes to
the object. It compares three full64-bit fields, then writes **AL only**:

`AL = !(QWORD28 == FFFFFFFFFFFFFFFF && QWORD30 == 0 && QWORD40 == FFFFFFFFFFFFFFFF)`.

The return's upperRAX bits are not assigned by these arms. The Boolean result
is not a full-register clean0/1 contract.

Three comparisons partition all possible readable64-bit field values into eight
equality classes. The producer follows each original branch expression to its
return and establishes false only for the all-sentinel class. These are
exhaustive static proof partitions, not eight original-code/harness/game runs.
State28=FFFFFFFFFFFFFFFF,30=0,40=0 selects59D933→59D938 and returnsAL1. Thus a
zero cache-view is not rejected by this predicate.

## Conditional composition and inherited limits

Retained597970 initializes reader28=-1,30=0,40=-1. It passes receiver+20 to
59EE90. Resolver59EFEA's QWORD[source+20] store therefore targets reader40.
The checked allocation-zero contract establishes conditional lookupRAX0 under
ordinaryNULL/normalreturns and its documented prerequisites. The resolver's
JS-only miss test takes the nonnegative cache path for zero.

The new producer also revalidates the original constructor/resolver bytes and
checks no own prefix writes to the other backing fields, no later own constructor
backing-field writes, and the actual post-zero reachable slice. Under valid
records/privateframes/noalias/nativeABI/normalreturns/successfulcookie and no
opaque field interference, that preserved state is accepted by a later IsOpen.
The constructor returns its object inRAX; resolverstatus0 is a separate value.

This is a conditional composed state, not proof a shipped caller naturally
encounters allocationNULL or invokes IsOpen afterward. Opaque callees retain
their stated premises; no omitted effect is supplied by a stub.

## Inputs, producer and controls

Reference EXE SHA25673461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000h. Source01 actualcapture uses the reviewed shared role adapter.
Retained initialization manifestd5cc7655d068357ee5bd9496b5674f82d4e4679d30d12356ba5411d8b713350e
and allocation-zero manifest93e2351f2132231d53da0597dbef418c7870e0a795e04e0090c4e5089c93c521
are producer-valid/frozen and independently pending at retention. Parent inputs/
drivers/results/statuses are bound in `parent-identities.json`. Revalidation is
reuse, not another capture or independent acceptance.

Producer01 terminal0 driver36759f394f6c326d98ac60a4d68d1280db88ab7e702c5d8e297e02e4aca9a17e.
Control01 terminal0 driverd51fa6b10d4669d8f439f6ca3f8d16ceaf1a65ec75d73f6ccc03766b25947107.
Three actual CLI prerequisite refusals: failed getter capture, missing retained
zero-result, missing getter source. Four synthetic controls exercise the actual
getter checker: zero-versus-allones sentinel, full64-bit width, branch polarity,
AL-versus-fullEAX return. They are synthetic decoded-record changes, not patched
original machine code. Prerequisite/byte/role/CFG/composition gates precede output;
invalid, missing or zero-case runs cannot pass.

Reproduce with the existing analysis venv: `python -B prove.py fresh-result.json`.
Restore the frozen `controls-01/*/input-identities.json` file sets and removals for
actual refusal cases. Inspect raw terminal/exit/exception/diagnostic/no-result
receipts. Static partitions, producer checks, external review and canonical
acceptance are separate.

## Consumers and cleanup

FABLE's existing path-to-bytes page states the sentinel formula correctly, but
“true as soon as a backing is bound” must not be interpreted as non-NULL/valid
cache-view certification. OPUS stream ABI/resource-readiness contracts should
use theAL bool predicate with this conditional zero counterexample. Route to
those owners after publication; do not edit peer-owned pages.

Allwriter/lifetime/ownership/reuse/scheduling/atomicity, native failure frequency,
actual later getter/read consequences remain open. No runtime allowance used;
no game/PC/instrument/nativecall/save/config/reference/peer changes. Owned bounded
helpers terminal. New producer/question answered without gameplay; acceptance
pending, historicalfour accepted runtime-needs eliminations unchanged/zero whole
OV closures. FullL1+L2 ACTIVE/NOT_MET; K14closed, EXP127invalid, menu spent/unapproved.
