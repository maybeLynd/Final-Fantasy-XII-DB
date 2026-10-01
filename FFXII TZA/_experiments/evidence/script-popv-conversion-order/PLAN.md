70 QUESTION: does integer-kind POPV clamp a float directly, or first perform the
original CVTTSS2SI conversion then pass that signed dword through the width clamp?
What happens at the positive signed32 conversion boundary under masked MXCSR?

Method B: original selected POPV post-resolve integer-kind stage, stop before
notification, then the original already-verified resolved-store leaf. A records
caller order but B distinguishes exact float32 input/converted bits/store effects
with a private rounding-opcode control. Not full POPV or normal VM reachability.
No resolver/notification stubs. Entry boundaries/state are explicit interventions
in disposable emulator guests, not a game process. Reuse67 source/table/graph.

Identity/control: shipping EXE73461d08 exact bytes; real caller branch from record
+4=1 and original store call static; initialized depth/tag/payload/record/destination
guards/stack/MXCSR1F80. Controls: 1.75 truncates versus private CVT nearest2;
largest float32 below2^31, +2^31, integer-tag INT_MAX and empty stack. Observe
stack depth, record+20 bits and destination writes separately. Budget32 original
stage instructions +64 store instructions; fail on bad-tag call, unexpected
access, non-boundary exit or guard change. No native MXCSR flag/exception parity.

Consumer FABLE storage prose and OPUS contract/spec, DATA propagation; SPEC audit.
Clean guest objects discarded, no host native allocation/FF12/PC/saves/config/
reference changes. Live caller/bankstate/lifetime/notification remain open. S19
spent budget/unapproved extension persists, fullL1+L2 NOT_MET.

LEARNED PRECONDITION: direct source-loading the existing reader requires module
__file__ for its path setup. First attempt failed before image load/guest execution/
raw/result; copied inputs retained, repaired module namespace. No conclusions
depended on this failure. Always sys.dont_write_bytecode and sourcecompile.
