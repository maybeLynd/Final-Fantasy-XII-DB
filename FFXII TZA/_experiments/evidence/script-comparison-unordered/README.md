# Masked qNaN compare returns +1, including self — 77

Method **B**: full shipping comparator25D740/413B in a disposable guest with
observed initial RCX/value stack, depth2/tag2 operands, aligned Windows frame,
masked MXCSR1F80, known nonvolatile registers and return sentinel. No calls were
executed or stubbed. Method **A**: original six24B comparison consumers and their
six-entry opcode table. EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

Question: does unordered float comparison return a special code, equality, or an
ordered result? Finite less/equal/greater positive controls succeed first:

| left / right bits | bounded original result |
|---|---:|
| 3F800000 / 40000000 (1 / 2) | −1 |
| 3F800000 / 3F800000 (1 / 1) | 0 |
| 40000000 / 3F800000 (2 / 1) | +1 |
| 7FC12345 / 3F800000 (qNaN / 1) | +1 |
| 3F800000 / 7FC12345 (1 / qNaN) | +1 |
| 7FC12345 / 7FC12345 (qNaN / same qNaN) | +1 |

Each full comparator return pops both operands: depth2→1→0. Only depth/frame
writes occur; original payload/tags/guards/code and nonvolatile registers are
preserved, RET reaches the sentinel and all guest mappings are discarded.
Actual initial registers/bytes and transition instruction/flag/memory records
are retained under128-instruction budgets, with exact tool/provider identities.

Original UCOMISS25D8B2 sets unordered guest flags; JP25D8B5 keeps unordered out
of the equality return. COMISS25D8D3 is then unordered too; CMOVA25D8D6 does
not take its −1 selection and EDI stays +1. Guest flags are observations of this
emulator, **not native exception/status evidence**. One labelled private control
replaces JP with two NOPs: same qNaN-left input now returns0. This intervention
does not describe unmodified FF12, but discriminates the branch's contribution.

Source consumers TEST the returned EAX then set CL. For the observed +1 result:
opcode0A/EQ=0,0B/NE=1,0C/GT=1,0D/LS=0,0E/GTE=1,0F/LSE=0. These are source
decision bytes from SETE/SETNE/SETG/SETS/SETNS/SETLE; **the interpreter/common
push was not executed**. A replacement with ordinary IEEE host comparisons would
give different greater/ge decisions for NaN. Do not infer actual scripted NaN
reachability or gameplay consequences from these injected operands.

First capture invocation finished the guest cases but failed its final pipeline
step because check.py was not yet written. It remains **INCOMPLETE**, never PASS.
Its exact driver/raw are retained; a later successful raw-default independently
reduces all cases and guards, without original guest replay. The producer now
requires a present compilable checker before preparation. Three faults reject
unordered=equality, unordered=−1 and an unchanged JP control. Published inputs
and the failed-invocation history are preserved.

FABLE/OPUS/DATA consumers should state the exact tested masked unordered return,
operand order/pop effects and source boolean decisions in prose/contracts/spec,
without substituting host IEEE operators. Independent SPEC acceptance remains
separate. Unknown: other NaN payloads/signaling NaN, native flags/unmasked traps,
game MXCSR, mixed/int-path general coverage, bad tags/underflow/fault-callback
effects, normal caller reachability/full interpreter and live consequences.
PC OFF/no host game process/native allocation/save/config/reference changes;
parked S19 spent/unapproved extension persists; full L1+L2 DB_GOAL=NOT_MET.
