# Original GS coordinate-format, bounds and vertex composition

The format byte changes more than parsing: zero decodes packed X/Y and Z and
bounds Z **before** the matrix; nonzero reads three floats and bypasses those
depth comparisons. Actual original matrix and division instructions then run
in both paths. This is controlled original-code evidence, not live gameplay.

Question and competing explanations are in PLAN.md. Source identity, four exact
PE function extents, all instruction bytes, directly derived RIP globals, shipping
1/16 constant, tool versions, seeded Windows ABI and consumer preimage are in
source.json. Eight finite original-code executions have raw instruction/register,
memory-access, intermediate-vector, output and cleanup records in raw-results.json.
check.py normalises them; validation.json is a self-check, not independent review.
PE records are only physical range cross-checks, excluded as proof of semantics,
ownership, registration or normal reachability. Original instruction control flow
and the isolated executed traces establish the bounded mechanisms described here.

The retained first feasibility control converts packed (16,32,64) to (1,2,64,1)
under an identity matrix. Identical float-source bytes produce (0,0,1000,1) on
the packed path versus (1,2,3,1) on the direct-float path. Packed Z=2000/0 with
bounds10/1000 becomes1000/10. Direct Z=2000 remains2000 under the same bounds.

The writer reverses the converter's temporary coordinate layout into XYZ and
sets W=1. For each matrix output component, the shipping leaf separately rounds
the f32 products and adds **Y contribution + X contribution, then Z, then W**.
The wrapper copies the temporary transformed vector back to the destination;
the writer divides XYZ by the transformed W and writes W/W. A transform yielding
(12,26,42,2) therefore ends as (6,13,21,1). This says nothing about zero/NaN W.
A finite cancellation control yields X=1.5; an X+Z-first rearrangement yields0.5.
Reconstruction cannot freely rearrange this operation order for bit fidelity.

Four globals' byte values become float components at+0x10/+0x14/+0x18/+0x1C,
without division by255. Their channel names remain a semantic consumer question.
The UV selector chooses distinct pairs written at+0x20/+0x24. Only destination
bytes0..39 are written in these nonalias cases; the48-byte record's last8 bytes
retain the A5 seed. That does not establish padding or all-path initialisation.

All four functions execute at normal entries: 00210230(227B),0020EA50(266B),
00202B70(31B),00217060(235B), including original call/return and preserved XMM6/7.
No native-effect stubs or interior entries. Other Windows nonvolatile registers
are also preserved. Supplied counters3/3 remain unchanged, AL=1; this does not
retest the phase-growth/ADC mechanism or prove full PACKED packet processing.

Limits: globals and state are planted, not original initialisation samples.
No actual game caller, resource binding, ownership, native renderer, pictures,
frequency, exceptional floating point, reversed bounds or aliasing is tested.
MXCSR is1F80. Complete function composition is not complete rendering parity.
FABLE/OPUS incorporation and independent SPEC acceptance remain pending.

Cleanup: each guest's hooks removed, input/code/global bytes checked unchanged.
Shipping executable is read-only; no game process/native attachment/PC control,
input, save/config/reference writes or fresh live cleanup receipt. Original live
permission and spent S19 setup allowance are unchanged. L1+L2 goal remains NOT_MET.

Player version: the old graphics path interprets points in two ways. Only its
packed format restricts depth before transforming them. The final position also
depends on a matrix and a divide, and the precise arithmetic order can matter.
The test proves the conversion machinery, not what a particular frame displays.
