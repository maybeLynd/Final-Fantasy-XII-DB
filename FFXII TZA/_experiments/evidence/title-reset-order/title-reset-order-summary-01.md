# Candidate count writer: cleanup first, clear afterward

Exact question: does611F80 establish valid count/storage before the already
proved62B100 first selected-field read, and does5DE290 locally repair that state?
Competing explanations were establishment-before-cleanup versus cleanup of the
incoming object followed by a reset. Method A original instructions suffice for
the local order and writes. A native forced call adds no natural-state proof.
Actual constructors/callers, native effects and initialized reachability remain
separate unresolved dependencies. No FF12 process was launched.

The pinned original image SHA256 is
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, base120000.
The PE Exception directory identifies611F80..611FE2 (98B, unwind1DA8660) and
5DE290..5DE2CF (63B, unwind1D9FE28). Both complete entry-normal CFGs close at
their normal RET. Exceptions, transitive calls and arbitrary object/stack aliases
are outside this proof. Capture uses the shared reviewed role adapter by default
and its actual store/address/RMW controls; the reader validates bytes against all
decoded operations/memory roles before reduction and pins the original span hashes.

611F80 obtains the object from RDX, preserves it in RBX, passes it in RCX to
62B100, then62BCB0. These calls precede local object writes and any empty-state
skip or normalization. After normally returning cleanup it conditionally calls
584730 when current count bit31 is clear, masked count exceeds1 and pointer+38
is nonNULL. It then clears QWORD+38 and DWORD+30 on every local normal path,
passes the same object in RCX to5DE290, and writes AL1 on return. Only the low
byte is established; this is not a full32-bit Boolean return guarantee.

5DE290 has no local nonstack writes. Byte+8nonzero selects5CDAA0(ECX3), and
pointer+20nonNULL selects6108C0(RCX=that pointer). Neither branch locally writes
count+30 or establishes count1. Native callee/alias effects remain unknown, so
the count is proved cleared immediately before5DE290, not necessarily afterward.
No ownership/refcount/constructor purpose is assigned from these offsets/names.

This candidate therefore does not discharge the incoming count/storage
precondition. The earlier count-zero absolute38 result remains conditional;
neither a natural malformed state, a live crash nor unsafe ordinary gameplay is
established. Next inspect actual constructors/count writers and their cleanup
callers. Do not reopen the parked menu or EXP127.

One successful source reduction is retained without rerunning it. Four actual
reader CLI controls reject missing wrapper proof, a false RDX-to-RCX annotation,
a consistently re-decoded AL0 counterfixture, and wrong unwind metadata, with
nonzero exit and no result. They are producer regression controls, not external
review executions or native/live experiment counts. Driver/source/result/cases
are immutable here; non-author review must bind these exact final identities.

Canonical consumers: FABLE cleanup/count-state semantics and OPUS callback
argument/return ABI. Required change: preserve cleanup-before-clear and RDX/AL
scope, retain initialization/native service/caller/lifetime/idempotence gaps.
Only accepted findings should reach peer-owned pages and types. Source data can
be reduced using the included reader/helpers and Capstone5.0.7 with the reviewed
adapter SHA5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38.
Capture additionally needs the private pinned EXE, which is not redistributed.

All synchronous helpers terminal. No game/input/instrument/save/config/reference
or peer process writes. Whole runtime rows closed0; cumulative previously-runtime
request retired1. Full L1+L2/M0-M5 goal remains ACTIVE/NOT_MET.
