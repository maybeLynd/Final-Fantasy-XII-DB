# Type-0x6B request-field zero: remaining source discriminator

Question: within prior captured 917-byte `00529D50` normal-entry control
flow, does `00529FEC xor r13d,r13d` dominate `0052A063`'s comparison and
`0052A06C`'s store to `node+0x3D4`, with no later local R13 definition?
H1 yes, narrowing these to compare-against-zero and a zero store under the
stated callee ABI preconditions; H2 a branch bypasses the definition or
redefines the register before either use. The prior source-consumer package
explicitly left this open. OPUS owns the consumer; do not duplicate its page.

Method A is sufficient: reuse its pinned body identity and original shipping
bytes, form only this body's direct normal-return graph, check dominance and
local register writes with the shared reviewed reg_tracking adapter. Calls
are fallthrough ONLY conditional on normal return; record calls crossing the
zero-to-use region and do not substitute stubs for native effects. The
9,526-byte `00533B20` already has a canonical native transform description;
do not recapture it for this bounded register question. Nonvolatile R13/RBX
preservation and valid instance/layout remain explicit preconditions.

Controls: the original entry must reach both uses; mutate an actual same-size
conditional branch before the definition to jump to the comparison and
require a bypass witness; replace the three-byte XOR with a same-size R12
XOR and require rejection of the zero-value premise. Keep mutants private
and label them as controls, never original-code execution or live writes.
CMP/store/LEA/read-modify-write role controls exercise the same imported
adapter that the producer invokes. Capture full original body bytes and
branch/path/control receipts. Invalid decode, unresolved indirect branch or
out-of-bound conditional edge invalidates the intended graph claim.

Stop once this source question is settled. No game/menu setup, no full
callee/lifetime/schedule/class proof, no final flag persistence or visible
result inferred. Do not promote source count or a green control to L1/L2
completion; request nonauthor review and owner incorporation after publication.
