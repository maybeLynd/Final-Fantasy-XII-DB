# Matrix buffer alias boundary — source first

Question: does `00217060(out,matrix,in)` protect arbitrary overlap, only snapshot
the four input components, or expose later matrix reads to its output stores?
Does wrapper `00202B70` stage output until all original matrix reads complete?
Consumers: OPUS primitive ABI/preconditions and FABLE rendering/workbench/camera
descriptions. Composer `00397910` already has its own alias campaign; do not
duplicate it or generalize its staged-input guarantee to a different leaf.

Method A is sufficient. Reuse dependency-verified committed GS source235B leaf
and31B wrapper, decode memory operands from original bytes and validate store/read
order. Complete branchless leaf and one-call wrapper make the discriminator
explicit without another original-code execution, live setup or generic harness.
Conditional finite example, not a new native observation: matrix diag2/3/4 plus
lastrow10/20/30/2, input1/2/3/1. Disjoint output gives12/26/42/2; output atmatrix+8
overwrites m[2] before its later use, changing Z to54. Preserve actual interleaving:
m[3] is read before output Y overwrites it, so W stays2, unlike a naive per-column
loop. Input components all load before first output store. Wrapper copies16B only
after the leaf returns, assuming arguments do not alias its private stack frame.

Controls: complete two raw body hashes/RET extents; decoded four input reads before
four writes; read-after-write hazard at2170CE ->2170FF for outputmatrix+8; negative
control m[3] read217104 before write21710D; wrapper's stack temporary/call/copy
ordering and return pointer. Retain current exact consumer preimages. Reject
identity/operand/ordering ambiguity. No source-only conclusion relabelled as a
native alias run, all-engine alias law, actual caller occurrence or live ownership.

Also inspect physical return state: leaf217069 copies RCX to RAX; wrapper copies
16B from that temporary while its frame is live, but has no RAX=original-output
assignment. Afterwards the register names released scratch, not a promised
caller-owned result pointer. Do not infer the C return type or actual caller use.
Camera prose "returns the matrix" must say transformed vector, not source64B
matrix. Retain the exact description preimage; FABLE owns its correction.

Route correction once; independent review required. PC OFF, reference read-only;
no saves/config/game/instrument change. Spent S19 menu allowance unchanged.
