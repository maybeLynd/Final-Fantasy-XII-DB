# Packed-member address and shader-definition elements callback boundaries

Method A: original shipping bytes and retained PhyreText, no live or isolated
native execution. Producer checked; independent acceptance and incorporation pending.

Player version: the loader connects arrays by supplying a pointer and a count.
The original callback's success code alone does not tell us whether that count
was accepted. These source facts narrow how a recreated loader must work, but
do not prove this shader loaded successfully or how long its memory remains alive.

QUESTION: which member-assignment ABI is actually registered for the shader
definition array's elements, does it preserve inner count failure, and what
width does the packed-member resolver use for its address adjustment?
H1: the outer array setter supplies the ABI again/propagates rejection, and
the address expression uses unrestricted signed arithmetic.
H2: the inner member delegates the supplied object directly, explicitly
suppresses the inner status, and the address adjustment is modulo32/zero-extended.
Exact instructions discriminate these bounded propositions without a game.

REFERENCE: EXE SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. Retained PhyreText44,634B SHA
f67d4492c21fc687f8897c130f66e8cddf5d8d2f0d262589b8597791a767a4cf.
No new archive read/census. Capture uses the shared reviewed reg_tracking.op_kind
adapter in its actual invocation, with memory-store, LEA and RMW controls.

IDENTITY: retained815B registration5EEB20 references the original m_els literal
atD32DC0 via5EEDAF. File class17 PArray<PShaderParameterDefinition> also names
m_els at packed+4. Prior working shorthand m_data is corrected; it was not a
published canonical name.5EEDCC/5EEDD3 assignsD4BD30 to that metadata, whose exact
8B slot+40 is60F3D0.5EEDEF/5EEDF6 registers60F280 at metadata+70. No whole-vtable
extent or live-descriptor identity follows. Outer60F590 is a different setter.

ORIGINAL OBSERVATIONS:

1. Entire33B dispatcher60F3D0..60F3F1 has two exits: callback-null returns21;
nonnull tail-dispatches with RCX=supplied object,RDX=supplied source,R8D=count.
It adds no member+48/class+F4 offset. Its indirect target is conditionally the
registered60F280; mutation/lifetime of that metadata is unobserved.
2. Exact16B normal callback60F280 calls60EFE0, then XOR EAX,EAX. Original retained
60EFE0 tests signed count and returns5 for negative before array reads/writes.
Thus a normal negative-count inner return can become outer0 with no array write.
The normal nonnegative continuation stores pointer at array+8 and count with
bit31 set at+0. Different owned old storage invokes5F03A0: its cleanup effects,
faults and lifetime are not established. Callback0 is not a count-acceptance proof.
This is original API behavior, not permission for evidence tools to hide failure.
3. Normal59EC40 source comprises seven contiguous chained exception-table entries
through59ED61. Historical19B capture was only a prologue; no previous binding
acceptance relied on it. Verified original chains identify the missing continuation.
The through path adds the residual delta modulo32 and at59ED3F writes EAX with
memberNativeOffset+childF4-parentF4 modulo32, then adds the64-bit object at59ED42.
Return=(object+zext32(delta)) modulo64. It is not unrestricted signed arithmetic.
The source includes null-child/flag/type guards; no unknown callback effects are
inferred. Hypothetical offset0/childF4=0/parentF4=8 produces deltaFFFFFFF8, not
signed-8. This is an ISA-width counterexample calculation, not a native run or
evidence that those values are naturally reachable. Existing accepted class-F4
work remains valid; F4 is not universally zero and must not be guessed here.

OPEN: concrete file-member to mapped-child construction, whether key22/27 reaches
the inner terminal member for this load, successful resource binding, native
descriptor adjustments in that load, installed pointer identity/lifetime,
destination aliases, opaque cleanup and natural caller/action flow. Packed
array keys, runtime arrays and loaded membership remain separate. These bounds
do not close the wholeOV42 row or constructor AE0 survival.

REPRODUCE final source reduction with fresh output:

    python <packet>/check-softedges-member-boundaries.py <packet> <fresh-result.json>

Result01/its exact driver are retained as the first scoped source pass. Final02
adds named registration/fact identity checks. Results were not overwritten;
first driver recovered byte-for-byte from the recorded edit and SHA verified.
No independent acceptance was issued to either. Three actual subprocess controls
refuse missing callback source, incomplete resolver source, and a disclosed
same-width XOR-to-NOP mutation even with its span hash updated. All exits and
no-result receipts are retained. They are producer controls, not FF12 runs or
external audit executions. Capture's three role controls are separate.

CONSUMERS: SWE2-AUDIT-SPEC independently checks the exact identities, branch/ABI/
width proof and controls; FABLE can consume accepted boundaries into OV42 and
the owning reflection/asset-loader specifications, routing OPUS-owned changes.
In particular the existing59EC40 prose's unqualified arithmetic needs a width
qualification, while real-load identity remains unresolved. No peer page edited.

CLEANUP: all own producer/checker/subprocess controls terminated. No FF12, PC
control, instrumentation, save/config/reference writes or primary reconstruction.
Menu allowance remains spent/unapproved; EXP127 remainsINVALID_POST_TRACE.
Full L1+L2 and workflow acceptance goal ACTIVE/NOT_MET.
