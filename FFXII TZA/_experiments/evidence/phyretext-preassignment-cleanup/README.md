# Conditional shader-array preclear and cleanup

Method A only: retained original code, ABI/dataflow and finite branch partition.
Producer checked; independent review and canonical acceptance pending.

Player version: loading a shader reference clears its array pointer before calling
its setter. For the matching unchanged registered layout, cleanup then sees NULL.
A rejected negative count can still leave that pointer cleared while the outer
callback reports success. This is source behavior under explicit conditions; it
is not an observation of a successful game load or the lifetime of its memory.

QUESTION: does reached59CD14 clear the same array+8 slot60EFE0 reads, and can this
cleanup release the old storage? Competing explanations: matching current offset
state yields the same slot; changed/rebound metadata or object identity does not.
Static analysis is sufficient for this conditional implementation question.
Natural initialization, no-rebind history and successful resource loading remain
separate, requiring additional evidence if retained as database obligations.

REFERENCE: EXE SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
preferred base120000. The shared reviewed reg_tracking adapter is actually invoked
by capture-index-path.py, with SSE-store, LEA/address and atomic-RMW controls.
Raw original instruction bytes, normal physical spans and exact producer hashes
are retained. Constructor632D80/63E410 have no pdata; closed reachable leaf CFGs
establish their spans632D80..632E71 and63E410..63E487.6372A0 is a complete8B leaf.
No original-code execution, game, process read, archive extraction or runtime
pointer sample was performed for this package.

CORRECTED ATTRIBUTION:6372A0 returns02CF8270 and supplies registrar arg6 ->
constructor descriptor+78 (parent).6373D0 normally returns01F2E330 and supplies
arg2/RDX ->+70 (sub-object). The earlier private driver called6373D0 the root
getter; that wording was false. Its original capture and driver remain immutable,
with the correction here and in final02. No published field/member/key result
claimed this getter was the parent. Lazy-init effects of6373D0 remain unproved.

OFFSET PROOF: named descriptor02CEA460 is constructed with arg7=0 ->F0=0,
parent02CF8270 and initially zeroF4/F8. If current ownF0=0 and parent remains the
root, original63E410 recomputation adds own0 then stops BEFORE reading the rootF0;
F4=0 follows. This is not all later writer/rebind invariance. For registered
m_els offset8, its preclear address is suppliedObject+sext32((8-ownerF4)mod2^32).
It equals suppliedObject+8 iff the current ownerF4 DWORD is0. This is an exact
modular identity, not extrapolation from a few offsets or universal alias safety.

REACHED PATH: current matching m_els kind2,flags bits1/6clear,original getter and
callback identities unchanged.59CC38 zeros nonvolatileR13,59CD14 writes it before
59CD25 passes the supplied object/source/count directly through60F3D0/60F280 to
60EFE0. With same slot/no interfering write and valid memory, its old pointer
read isNULL. Positive/nonnegative sourceNULL skips cleanup; nonnull source plus
borrowed old count skips; nonnull source plus owned old count calls5F03A0(NULL,
maskedCount). That callee jumps straight toRET5F0407: no object-memory access or
nested call. RET still reads the return address/advancesRSP; RAX is unasserted.
The nonnegative setter writes new pointer and count|80000000. It cannot release
the overwritten old pointer through this cleanup. No universal allocation leak
or general nonnull cleanup behavior is inferred.

NEGATIVE BOUNDARY: preclear has already happened, then60EFE0 rejects signed
negative count with5 before reading array storage or storing its count.60F280
returns0 anyway. Pointer remainsNULL and count unchanged under these premises.
This extends the COMPOSED caller effects; the earlier standalone setter's
negative-count/no-write statement remains valid. Retained shader keys22/27 use
counts11/1 (nonnegative); no malformed negative count was observed in the game.
The eight result branches are exhaustive Boolean path partitions from the source,
not eight native executions or new samples.

CONTROLS/FAILURES: initial pdata/extent expectations failed with no capture result.
Each exact failed driver/receipt is preserved. The constructor ends at632E71,
not632E77. A later parent-getter pdata expectation also failed; the actual8B
LEA/RET leaf corrected the method. The first ungated dependent read failed with
FileNotFoundError, no semantic result. The actual corrected invocation uses the
existing checked_run before reading and rejects old outputs. Three procedural
controls prevent reads after upstream failure even with readable output, exit0
without output, and preexisting stale output. Three actual final reducer CLI
controls reject missing parent source, false parent-store normalization and
false borrowed-flag normalization without creating a result. These are producer
controls, not independent acceptance or external reviewer executions. First-pass
result01/driver remain; final02 strengthens the exact predicate checks.

REPRODUCE reduction from repository root with fresh output:

    python <packet>/reduce-softedges-preassignment-cleanup.py <fresh-result.json>

Optional second argument selects a disposable source directory for the retained
CLI refusal controls. Do not rerun capture into immutable paths. All invoked
producers/checkers exit; no background worker or terminal needs to remain active.

CONSUMERS: independent SWE2-AUDIT-SPEC review, then FABLE's asset-loader/reflection
and OV42 owning pages, routing OPUS type/contract changes through ownership.
Prior field5bbbe5528/member7a524fda9/keya50f9dea4 reviews/consumption remain separate.
No peer page was edited. Actual load, source ownership/lifetime, arbitrary aliases,
complete constructor/caller/writer closure and wholeOV42 remain OPEN. This result
answers a conditional effects/offset question without live gameplay; it closes
no additional whole runtime row. Cumulative source-retired runtime request1.

CLEANUP: all own synchronous captures/checkers terminated. No @runtime/PC/game,
input, instrumentation, save/config/reference writes; no global process-absence
claim or peer termination. Menu setup remains parked with spent allowance;
EXP127 remains invalid. Full L1+L2/M0-M5 goal remains ACTIVE/NOT_MET.
