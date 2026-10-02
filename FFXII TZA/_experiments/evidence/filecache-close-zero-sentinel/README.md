# Close true does not certify the IsOpen predicate becomes false

MethodA STATIC_ONLY. Original streamClose64B plus the retained27BIsOpen predicate
settle a conditional lifecycle contract without native calls or gameplay.

For the player: this Close function can report success while the engine's
bookkeeping still says “open.” In the zero-cache-view case it skips release and
reset, leaving the field that IsOpen accepts unchanged. No gameplay failure,
leak or naturally exhausted heap was observed.

## Question, original paths and distinguishing result

H1: normalCloseAL1 guarantees laterIsOpenAL0. H2: it returns true even on a
no-helper/no-state-write arm, and that arm can preserve a true sentinel predicate.

59BD40..59BD80 is64 bytes. The routine readsQWORD30, and if nonzero calls2150D0
then storesQWORD30=0. It next readsQWORD40, uses TEST RDX,RDX followed by **JLE**,
and for **signed64 values<=0 skips both**1D6AA0 and the storeQWORD40=-1.
For a positive value it reads the keyDWORD48, calls1D6AA0 and writesQWORD40=-1.
All local normal-return paths share MOV AL,1 at59BD78. UpperRAX is not assigned.

The four logical buffer-nonzero/cache-signed-positive partitions have precisely
their corresponding helper calls and backing writes. These are static branch
partitions, not four machine-code runs. TEST setsOF0; JLE'sZF/SF condition gives
the signed<=0 rule. Fixed-width boundary models are mathematics, not sampled
live pointers or proof any negative non-sentinel pointer is naturally supplied.

For readableinput28=-1,30=0,40=0, both helpers and both object writes are skipped.
Close returnsAL1 and leaves those three fields unchanged. Retained original
IsOpen accepts the preserved state and returnsAL1. This refutes a universal
“Close true means IsOpen false” contract at the source/input level. Close has no
own access to28; a non-sentinel28 with the same no-helper guard is another
mathematical witness, not an actualWin32handle or observed leak.

No opaque helper effects are needed for the zero no-helper arm. Other branches
keep normalABI/normalreturn/nativeeffect/noalias/nointerference premises.
All paths require a readable validrecord/privateframe/normalexecution. Natural
allocation failure, actual callers, laterRead effects, allwriters, resource
cardinality, ownership/reuse, lifetime and scheduling remain open.

## Identity, producer and controls

EXE SHA25673461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000h. Actualsourcecapture uses the shared reviewed access-role adapter.
Retained IsOpen manifest7479a4f8d544249b398a57419aab50ac4296bc14eb717c4517cd478320ad2f45
is producer-valid/frozen and independently pending at retention. Parent bytes,
driver/result/status/manifest are exact pins. Its pure checkedgetter() is reused
against again-revalidated original bytes; this is not repeated original execution
or acceptance of its complete constructor/failure composition.

Producer01 terminal0 driverd498f547510f5998b7cf0b33bea37c4e20073cf86724dde064752bbd92d329d7.
Control02 terminal0 driver601edfd2d79c8b50f78fa19be86fb34d87541e0ee6ef07a3479300fa099201d8.
Three actual CLI prerequisite refusals: failed Close capture, missing retained
predicate result, missing Close source. Four synthetic controls exercise the
exact derive() invoked by the positive: signednonpositive versus zero-only guard,
fullQWORD reset width, AL versusEAX return, skip-release-also-skips-reset target.
They are decoded-record controls, not patched-image or native executions.

Control01 is **INVALID_CONTROL_INVOCATION_BEFORE_CASES**: Python CFG call pairs
were tuples while immutableJSON serialized them to lists, causing the checked
positive comparison to refuse before any negative cases. Original driver/receipt
are retained. The correction compares the entire derived value through the exact
producer JSON representation, preserving all fields/order/values. Control02
checks the corrected actual invocation and all cases; no source producer rerun.
`control-comparison-correction-01.json` binds cause/preimage/current identities.
Incomplete/zero-case output cannot pass or supply a historical green control.

Reproduce with the existing analysis venv: `python -B prove.py fresh-result.json`.
Restore refusal file sets/overlays/removals from frozen input-identities receipts.
Review raw terminal/exit/exception/diagnostic/no-result status, not only counts.

## Consumer and cleanup

FABLE path-to-bytes streamClose description: distinguish source return true,
conditional backing reset and the later sentinel predicate. OPUS stream/Close
ABI and resource-readiness contracts: retain signed64guard, fullQWORD writes,
ALreturn and the no-helper zero witness. Do not infer leak/readfault from this
conditional result or replace it with a simulated native effect. Independent
review and actual canonical consumption remain required.

Owned capture/proof/control processes terminal; no game/PC/native instrument/
save/config/reference/peer changes. Published/frozen inputs immutable. No live
allowance used. Historicalfour accepted former-runtime needs eliminatedoffline
unchanged; this new producer answer is pending acceptance, zero wholeOVclosures.
FullL1+L2 ACTIVE/NOT_MET; K14closed, EXP127invalid, menu spent/unapproved.
