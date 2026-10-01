# Title tracker: global callback queue boundary

Method A original-source proof; producer checked, independent acceptance pending.
No native/emulated execution, process read, FF12 input, new title-body capture or
family census. Physical, local semantic, initialized-state and scheduling claims
remain separate. Prior title/shader reviews and consumers are not duplicated.

Player version: this cleanup helper uses a shared engine context to put a cleanup
function and its argument into a queue. It does not look up each supplied object
and immediately finish freeing it. The code can clear its local pointers while
that queued work still needs a separate execution path. Whether the actual game
runs it before a title widget disappears remains an open lifetime question.

QUESTION: does183720 resolve a supplied object and complete release, or read a
shared context and enqueue a callback/data pair? Cheapest sufficient evidence is
original getter/caller/writer branches. No running game is needed to correct that
implementation description. Natural initialization, scheduling and ticket lifetime
are separate questions and are not resolved by a successful source capture.

REFERENCE: shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000, Capstone5.0.7. Capture-index-path actually imports the reviewed
reg_tracking adapter and runs SSE-store/LEA/address/atomic-RMW controls. The actual
queue MOVUPS store rolew and LEA roleaddr are also required by the reduction.
No raw Capstone access flags bypass the policy. The capture's compiler spans,
original bytes/hashes, producer/gate identities and checked exit receipts remain.

BOUNDARIES:1FB660 normal body has three actual runtime-function tuples; both
continuations chain to its87Broot and the entry-reachable CFG closes at1FB71B
RET, total188B/52instructions. Those are coverage metadata, not52tests. No branch
leaves this body except named/indirect callee boundaries. Original18372052B,
1891208B,MOV/RET globalgetter,185A9086B and17ECC027Bcallback are separately
retained. Callback's directtail is a boundary, not unobserved callee proof.

PRIMARY CORRECTION:189120 ignores RCX and readsQWORD01F7F598; it is not an
argument-dependent object resolver.183720 returns for suppliedNULL. Otherwise
it loads that global twice, tests ONLY the first load forNULL, then passes the
second context to185A90 with17ECC0/originalargument. The canonical transform
paragraph saying it resolves the object twice is refuted by those bytes. A
canonical-clause snapshot is retained; FABLE owns the correction and OPUS owns
any type/signature consequences. No peer claimed file was edited. Stability and
nonnullness between global reads are explicit conditions, not process invariants.

QUEUE FAST PATH:queue=ctx+C38+32*signextend32(DWORD[ctx+CB8]). No localindexbounds
check.16Bpair=[callback,data]. If unsignedwritecursor<end and cursornonNULL,
185A90 storescursor+16 atqueue+8 BEFORE copying the16Bpair to oldcursor; it calls
nothing on that branch and does not execute the callback there. This is exact
instruction order, not an atomicity/torn-read/concurrent-race claim. Valid index,
backed16Bspace/stack, no conflicting aliases/writes and ABI premises remain.
IfNULLcursor<end in a malformed suppliedstate, it advancescursor to10 and skips
copy; this is source branch analysis, not an observed/valid constructor state.
Whenwrite>=end it delegates1858A0(queue,write,&pair); effects are not silently
certified. No direct API return or cursor change alone proves a command ran.

TRACKER:1FB660 calls183720 on value+0, then clears+0; it similarly calls it on
circularnode+28 then clears that field. Another list delegates1AF2B0(value+8,
[link]) and vcall18(value+38,link,size30), saving the nextlink before that call.
Normal return resets+20/+28byte/+30 and circular+10/+18. This is conditional
caller effects, not a complete free/cancel/allocator or terminating-list proof.
Callback17ECC0 IF entered with incomingRCX preserves that value for5DE250 then
tails19C590. Queue-consumer argument ABI, actualexecution/thread/frame and both
callee effects still require evidence. It is not a captured live callback.

CONTROLS: one completed positive reduction; three actual reducerCLI refusals
(missingqueue source, wrong globalgetterRIP target with original bytes unchanged,
old/misclassified actual SSEstore role) all exitnonzero and create no result.
The completed positive is reused, not rerun merely for counts. Source capture
and controls are producer evidence; independent acceptance is a separate task.
No partial/missing/zero-case result can pass. No failed input or cited run replaced.

Reproduce from repo root with fresh output:

    python <packet>/prove-title-tracker-callback-boundary.py <fresh-result.json>

Optionalsecondargument chooses a disposable source directory for refusalcontrols;
retained source/driver/result paths remain immutable. Historical boundarydiagnostic
is preparation only; current source01/reduction are the review inputs.

NEXT:original1858A0 insertion and contextqueue consumer; bound5DE250/19C590 and
1AF2B0/vcall identity before asserting release/cancellation. Existing titlemember
notification249632 and separateticketpool are not this cleanup queue. Missing
live initialization/lifetime staysOPEN. No wholeOV29 or fullL1+L2 completion.
One bounded semantic/globalgetter question answered offline; additionalwholeRT
rowsclosed0,cumulative source-retiredrequest1. No native/live count from controls.

CLEANUP:own synchronous scripts exited; no @runtime/PC/game/observer/save/config/
reference write or peer processkill. Menu allowance remains spent/unapproved;
EXP127invalid. FullL1+L2/M0-M5goalACTIVE/NOT_MET.
