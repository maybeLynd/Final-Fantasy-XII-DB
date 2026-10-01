# Original integer quotient overflow before result — 80

QUESTION: after OPDIV's nonzero-divisor guard, does INT_MIN/-1 wrap, saturate or
stop at IDIV before producing a result? Major system ScriptVM arithmetic; FABLE
BF-1 semantic/OPUS VM contracts consumers. Zero guard alone does not answer it.

METHOD B: verified shipping5 bytes `99 F7 FB 8B C8` at25F0D9..25F0DE:
CDQ, IDIV EBX, MOV ECX,EAX. Supplied register entry after the original guard,
stop before the following JMP/common result path. No calls/stubs or memory
accesses. Disposable x64 Unicorn instance with <=8 instructions per arm.
This is isolated original machine code, not the live game or a full opcode run.

REFERENCE: original EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`;
certified reader, actual reviewed access-role adapter, Python/Capstone/Unicorn
backend/providers pinned. Slice/guard independently matched against original
OPDIV298/table/descriptor/name bytes from frozen79's manifest-verified inputs.
Raw records whether that parent was committed or frozen/unpublished at capture;
pending publication is not acceptance. Inputs/driver/results remain immutable.

STATE/CONTROLS: EAX signed dividend bits, EBX divisor bits; EDX poisonA5A5A5A5,
ECX12345678, flags2, RIP25F0D9, known nonvolatile registers, one CC-filled guest
page with original5B. Code/page read back before and after; actual visit bytes
read from guest memory; no memory effects allowed; all mappings empty after unmap.
Three original positive arms precede the intended boundary and error controls.

| arm | observed isolated guest outcome |
|---|---|
| 20 / 3 | quotient6, remainder2, MOV/stop reached |
| -20 / 3 | quotient-6, remainder-2, MOV/stop reached |
| INT_MIN / 1 | quotientINT_MIN, remainder0, MOV/stop reached |
| INT_MIN / -1 | UC_ERR_EXCEPTION at original IDIV, MOV unexecuted |
| 1 / 0, entered after guard | same observer error at IDIV; detection intervention |
| INT_MIN / -1, private IDIV→NOP | MOV/stop reached, supplied EAX retained |

The zero arm explicitly BYPASSES original TEST EBX/JE, which naturally skips IDIV
for zero. It does not claim normal OPDIV0 faults. Private NOP is an intervention,
not original behavior. These controls distinguish quotient boundary/instruction
from broken setup or an error detector that never fires.

IMPLICATION: the source nonzero guard allows the MIN/-1 register state to reach
IDIV. In this original-code guest it stops before the result copy; neither wrap
nor saturation is an observed original result. The specification must separate
this boundary from zero-guard behavior. Default reduction and rejected wrap/
saturating/private-still-fails alternatives preserve the exact observations.
Private store/LEA/RMW bytes control the actual shared adapter; not native tests.

LIMITS: generic guest UC_ERR_EXCEPTION is not a measured native OS exception
vector, handler disposition or game crash. Full OPDIV classification/pops/pushes,
caller reachability, authored values, flags and real process exception handling
remain OPEN. No host native allocation, live game, PC input/attach, save/config/
reference writes; no lifecycle/restoration claim borrowed from other experiments.
All six disposable mappings cleaned individually. Owner incorporation and
independent acceptance pending. S19 spent/unapproved extension persists; full
L1+L2 goal ACTIVE / NOT_MET. Stop the settled guest question, next discriminator
for native handling is actual original unwind/caller exception policy evidence.
