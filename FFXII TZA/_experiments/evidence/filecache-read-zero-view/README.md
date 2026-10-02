# IsOpen acceptance does not guarantee reader entry or supplied bytes

MethodA STATIC_ONLY. Complete shipping92BRead wrapper59D4B0..59D50C and the
retained27BIsOpen predicate settle a bounded source contract. No native code,
emulator, heap failure, gameplay or I/O was executed.

For the player: a stream labelled “open” can supply no bytes without attempting
a read in this state. This identifies what the engine's checks guarantee; it
does not establish a naturally reached failed load or a gameplay fault.

## Exact question and result

H1 treatsIsOpenAL1 as proof a reader runs or usefulbytes exist. H2 distinguishes
the sentinel predicate fromRead's source and requested-bytecount guards.

The wrapper first loadsQWORDbuffer30 intoRAX. A nonzero buffer calls2150E0 first.
With buffer30=0, it initializes its stackDWORDbytecount fromEAX0. Requested
R8D=0 returns without anycall. For nonzeroR8D, handle28!=-1 calls the shipping
IAT8C2140; otherwise positive signed64cache40 calls1D6CA0. Nonpositive cache40
skips thatcall and preservesfullRAX0. The source has five exhaustive logical
branch classes, not five native/game runs.

Input28=FFFFFFFFFFFFFFFF,30=0,40=0 satisfies the retainedIsOpen predicate and
returnsAL1. Read returns **fullRAX0** and calls neither a reader nor I/O for
either zero or nonzero requestedR8D on that input. Validreadablerecord/private
frame/normalexecution are required. Actual caller, natural allocation failure,
readfault, leak, scheduling and later engine response remain open.

The Win32 branch imports **KERNEL32.dll!ReadFile** throughIAT8C2140, verified
from the shippingPE declaration. After its normal return,59D4F0 loadsDWORD
callerstack40 intoEAX, replacing theAPIreturn. This wrapper returns the count,
not theAPI BOOL. ActualDLLbinding, nativeAPIeffects, error/partial-bytecount
semantics and the2150E0/1D6CA0 helpers are not inferred here.

## Primary evidence, corrected metadata and controls

EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000h. Capture01 uses the actualshared reviewedrole adapter, complete
source bytes and invocationreceipt. Retained IsOpenmanifest7479a4f8d544249b398a57419aab50ac4296bc14eb717c4517cd478320ad2f45
was frozenproducer-valid/independentlypending atretention, notrecaptured.
Exactparent driver/result/status/manifest pins precede use of its puregetter().

Final producer02 terminal0:
e3f7b5fb43f90fc9488947e87be262f9790dfd2e823247bad13b9aead8a76c25.
Control01 terminal0:
e838ee46e91edcd125bfa1c481f4c1ed1c204675b2d5998414831526b2bc1688.
Three actualCLI prerequisite refusals: failedReadcapture, missingretainedpredicate
result, missingReadsource. Four synthetic controls target the actualderive():
requestedbytecount guard, fullQWORDbufferread, signednonpositive cacheguard,
APIreturn replacement bycount. They are decoded-record controls, notpatched
original machine code. Identity/role/CFG/parent/return-carrier gates precede output.

Producer01 derived the same correct source facts/import but inherited wrong
Close metadata: “four”partitions and “AL-only.” Its rawresult/driver/receipt are
immutable. `metadata-correction-01.json` records the additive correction before
publication; finalresult02 states fiveclasses and fullzeroRAX onno-callRead arms.
Control01 compares exactderive/import AST and allscientific facts/sourcepins
between the versions. No changed scientificcase or priorconsumer is hidden.
Reuse must select prerequisite blocks and author current semanticmetadata,
rather than inherit another function's return-width description.

Reproduce with existing analysisvenv `python -B prove.py fresh-result.json`.
Restore refusal sets/overlays/removals from frozen input-identities; inspect
terminal/exit/exception/diagnostic/no-result receipts. Missing/zero-case evidence
cannot pass. Producer checks and externalreview/acceptance remain separate.

## Consumers and cleanup

FABLE path-to-bytes Read explanation; OPUS streamABI/readiness contracts: keep
AL-onlyIsOpen distinct fromRead's fullzero no-call result andAPIcount return.
Preserve nativehelper/API/lifetime/normalreturn/validinput boundaries; do not
claim natural failure, actualRead or universalIOsuccess from the source model.

Only ownedoffline files changed; ownboundedchildren terminal. No game/PC/native
instrument/save/config/reference/peer edits. Independentreview andcanonical
consumption required. Historicalfour accepted former-runtime needs eliminated
offline unchanged; zero wholeOVclosures. FullL1+L2 ACTIVE/NOT_MET; K14closed,
EXP127invalid, menu allowance spent/extensionunapproved.
