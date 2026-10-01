# The selected original resize caller enforces copy capacity

Method A STATIC_ONLY, producer checked; independent acceptance and canonical
incorporation pending. Exact question: does627DA0 enforceK<=N for its61D100
call, or can the helper-only N2/K3 counterexample occur through it? Original
EXE SHA25673461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No function was executed in native/emulated/game state.

Answer for this selected original caller: yes, it clamps. It takesoldcount from
the record's32-bit DWORD and clears bit31; newN is inputEDX low32. CMP/unsigned
CMOVB setsR9D=min(N,oldcount). The five defining/compare/clamp operations dominate
627DE8 in the complete175-byte normal CFG; the clamp immediately precedes its
61D100 call with no opaque call or intervening write. ThusK<=N holds for every
u32N/oldDWORD pattern on that call path. It refutes using the helper's N2/K3
conditional counterexample as a reachable overflow through this caller.

Three chained-unwind fragments are required:627DA0..627DFE,627DFE..627E38 and
627E38..627E4F. The first fragment's conditional jumps leave it; it alone cannot
support the whole caller result. Raw unwind headers/chains are retained and
checked, along with all original decoded bytes/access roles. Normal CFG proof
does not certify exception unwind or asynchronous interruption effects.

The same caller selects old sourceNULL/inline+8/pointer+8 for masked counts0/1/>1.
InputN equal to the FULL unmasked oldDWORD skips work and returns0. Otherwise
NULL output with nonzeroN returns0Dh before record changes/free; N0/NULL is valid.
Success frees the old pointer through584730 only when different from output,
different frominline, nonNULL and oldbit31clear; it publishes output when not
inline and writes the inputN DWORD. Those are local order/arguments, not native
allocator/free effects. Arbitrary high-bitN is not an encoded-count sanitizer.

Prior33-member copy-construction packet/helper result is a required upstream
producer receipt; both original sources are requalified and its completion and
exact input pin checked. Missing/failed helper evidence refuses the caller
result. Independently accepted OPUS T2 stride/layout is reused, not rerun here.
Normal capacity is now a proved precondition on this caller. Copied counter38
and userdata48/index50 are still preserved; fresh tail leaves userdata local
initialization unassigned. No local wait/queue-key removal/rebinding occurs in
the selected closure; allocator/free transitive effects and higher-level guard
policies remain outside it.

Reproduce using existing analysis Python with a fresh output:

    python <packet>/prove-texture-copy-capacity-caller.py <fresh.json>

Four actual CLI controls reuse the final positive and refuse missing upstream
helper result, helperproducer_complete=false, byte/annotation-consistent CMOVA
instead ofCMOVB, and missing chained-fragment metadata. They are synthetic
producer controls, not native/game runs or independent acceptance. Result01
and its driver preimage are retained as history; final02 separates raw source
pins from checked producer-result pins so the annotation consumer receives
actual raw records, and replaces the stray 'oldWORD' wording with32-bit DWORD.
No raw recapture, semantic widening or extra experiment credit follows.

OPUS owns the caller ABI/failure/capacity contract; FABLE owns the counter-copy
versus lifetime interpretation. Only this new selected caller/guard/order is
submitted, not a duplicate review of accepted stride/layout. Natural pending
resize, higher-caller state/order, original queue remapping, complete wait-counter
writers, real object/allocator identity, ownership/reuse and cancellation remain
OPEN. Raw reference candidates are not a complete caller census. A forced input
would not prove shipped reachability, and no runtime observation is needed to
settle this selected capacity invariant.

Next discriminator: original higher caller supplies ordinary count-domain and
whether it waits/removes outstanding async keys before relocation/free. Prove
that order first; C only for an essential residual natural-state premise.
Cleanup: bounded file reads/static proof; all known children terminal, noPC/game/
input/instrument/save/config/reference or peer-process writes. K14 closed,
EXP127 invalid, parked menu spent/unapproved unchanged. FullL1+L2 goal remains
ACTIVE/NOT_MET; package integrity/producer proof is not independent acceptance.
