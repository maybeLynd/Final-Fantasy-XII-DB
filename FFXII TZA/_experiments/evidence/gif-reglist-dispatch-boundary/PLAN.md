# GIF replay REGLIST boundary — method A

Question: does00210320 traverse all tags by EOP regardless of mode, or does a
positive-NLOOP REGLIST tag end its local walk early? Consumer: FABLE legacy VIF/GIF
mechanism; OPUS exact input domain/representation/preconditions; SPEC independent
review. Current sizing formulas are correct and are not the result being changed.

Existing evidence: actual dispatcher preflight shows FLG1 jump00210476->002104A0,
while normal EOP check is00210489. NLOOP0 skips mode handling. Competing explanations:
normal REGLIST payload processing/continuation; intentional local mode termination;
or an entry-fragment/zero-loop misread.

A is sufficient for the exact local branch question. Validate the complete424-byte
body through its return against three contiguous PE fragments and CHAININFO parents;
read both NLOOP tests and all mode paths. Retain bytes/disassembly/current page.
Positive discriminators: PACKED's payload-handler call, IMAGE2/3 cursor skip and
EOP continuation, zero-NLOOP REGLIST EOP0 continuation. REGLIST positive EOP0/1
both reach the completion call before the EOP check. These are symbolic branch
witnesses, not native/emulated/live runs or a support census of authored packets.

Acceptance: full primary extent and exact branch/dataflow support this limited
distinction. Stop/invalidate if chaining/extents, branch dominance or an intervening
guard contradict it. Do not spend runtime to prove a static local branch. Callee
effects, actual packet occurrence, scheduling, flush submission and pictures remain
unknown; a completion call may have native effects even without local payload dispatch.

Cleanup: PC off/reference read-only; no game, emulator, native process or save/config
changes. Only owned artifacts; owner changes are routed, never silently performed.
Full L1+L2 goal/final reviews remain NOT_MET; no L3 or full campaign.
