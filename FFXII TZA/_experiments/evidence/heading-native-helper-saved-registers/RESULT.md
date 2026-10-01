# Native helper has an explicit conditional saved-register return path

Method A, STATIC_ONLY. Producer-checked source supplement, not independent
acceptance or native/live execution. Existing EC-7 transform classification
is reused; this answers its caller's specific RBX/RSI/R13 preservation condition.

The retained catalogue's 9,526-byte 00533B20 range decodes completely into
1,653 instructions, with one local RET at 00536055, no indirect jumps and no
external jump tails. Entry pushes RBX at 00533B20, RSI at 00533B22, R13 at
00533B23, then R14/R15, and subtracts 0x3A0 from RSP. The sole local return
path adds 0x3A0 at 00536046, pops R15/R14, then R13 at 00536051, RSI at
00536053 and RBX at 00536054. Every selected save, frame adjustment and
restore dominates the local RET in the normal-return CFG.

The shared reviewed adapter finds no other local RSP-changing operation
outside those pushes/pops/sub/add, calls and RET. With calls modelled as
normal returns at the same RSP, the R13/RSI/RBX saved slots are frame-relative
[3B0,3B8), [3B8,3C0), [3C0,3C8). The actual adapter classified all 1,101
memory operands; 96 direct RSP-based store intervals avoid those slots, and
none has an unresolved RSP index. This is a direct-stack-store source check,
not absence of aliasing from arbitrary native pointer writes or callees.

The actual capture imports the central hash/path-checked reg_tracking.py.
Original 00533B5E MOVUPS memory store is classified as a store by that policy;
store, LEA and locked-XADD controls check w/addr/rw. Raw shipping body bytes,
normal graph, saved-register instruction bytes, tool identities and classified
store intervals are retained. The feasibility read is preserved separately.

Two same-size private static input controls preserve the 1,653-instruction
count. Redirecting the real near conditional branch at 00535FC8 directly to
RET yields a concrete path bypassing the R13 restoration. Changing POP R13
415D to POP R12 415C is detected through the actual operand/write-role checks.
These controls are neither execution of mutated FF12 nor a live intervention.
The final producer has checked exit 0; no unchanged repeat is needed.

Consumer implication after nonauthor review: the caller's source R13/RBX/RSI
dependency can cite this explicit native save/restore path rather than rely
only on a blanket nonvolatile-register convention. Preserve **normal return,
coherent RSP and intact saved stack bytes** as conditions. The cookie check
at 00536038 calls 00808C40 before the pops; its success is not observed here.
Exceptions/non-return, alternate entries, native pointer/callee alias effects,
valid receiver, initialized state, flag persistence, scheduling, lifetime,
class meaning and presentation remain open. No metadata supplies execution
edges. A modelled path does not prove branch feasibility or actual invocation.

The existing OPUS source-consumer task is ACTIVE; no peer-owned page was
edited or duplicate consumer created. A new independent review and guarded
publication are still required. Reference EXE unchanged; no game/PC controls,
instrumentation, save/config/reference or peer writes. Full L1+L2 remains active.

Player version: the effect helper contains the normal return machinery that
restores the caller's working values. This makes the earlier flag-clear and
loop description better grounded. Real timing and visible effects are still
separate questions.
