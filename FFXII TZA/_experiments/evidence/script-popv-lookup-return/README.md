# POPV lookup return is discarded — 71

**STATIC_ONLY, method A.** Exact original32B `0032F240`,30B POPV gate/continuation,
and23B store prefix through complete instruction boundaries. No native, guest,
VM or live-game execution. EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Alreadyverified67 reader/adapter/store source bytes are pinned at commit8db582868.

Question: does the POPV call emit a notification or use its returned ID to affect
the store? The canonical page already identifies the callee as a registration
lookup; the additional question is whether its return influences this caller.

All entry-reachable instructions in the32B lookup form a closed direct graph:
the registered byte at `022C6D18+i` is compared with0; if nonzero, it loads the
ID dword at `022C6D28+4*i`; otherwise EAX becomesFFFFFFFF. Both paths return.
There is **no source call or memory write**. Actual source-compiled shared adapter
classifies the two table accesses as reads and the image-base LEA as address
computation. RET still requires a valid stack; this is not a no-fault guarantee.

The POPV caller gate is `uint32(slot_index-1)<=2 && ESI==0`. Following the lookup,
`00267F32` computes the record pointer in RCX, then `00267F37` calls the store leaf.
Neither continuation instruction consumes returned EAX. In the store prefix,
the first three instructions read record/base/index without reading RAX;
`0026D53B MOV EAX,[R9+18]` overwrites the complete returned RAX before any use.
The registration ID therefore does not affect storage through this return value.

Controls: a labelled **decoded-only** private load→store opcode makes the actual
adapter report a write; replacing the first EAX overwrite with NOPs exposes an
incoming RAX read at the later SHR. Neither mutation executes. Three checker
faults reject inventing an event write, using the discarded return, and disabling
the write detector. Default invocation reduces unchanged raw evidence.

Consumer change: qualify “notification path” as this read-only registration/ID
query with a discarded return on POPV. Narrow70's historically open omitted-helper
effect question using this additive source evidence; preserve70 raw/results and
its remaining limitations. Do not imply70 executed the full caller or this lookup.
FABLE/OPUS/DATA own consumers; SPEC audit and independent acceptance remain pending.

Not proved: actual table contents/initialization/writers, current memory validity,
native faults, normal caller reachability, other notification/callback systems,
thread scheduling or lifetime. The claim is the exact ordinary-memory source
contract, not an observed live event. No instrument/process/PC/save/config/reference
changes. S19 spent budget and unapproved extension persist. FullL1+L2 NOT_MET.
