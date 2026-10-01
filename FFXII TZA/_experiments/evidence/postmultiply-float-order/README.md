# Matrix composition: preserve binary32 accumulation

Question: the flat row-major **B*A** composer is an algebraic product, but does
that expression alone prescribe the exact original floating-point result?
Consumers: FABLE/OPUS composer numeric rule on the two-transform-primitives page.
This is separate from already-established operand order, snapshot and alias facts.
The MXV row already states its addition order; no MXV experiment was performed.

**B isolated original-code evidence.** Shipping image SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
parent349B003977B0 SHA69b03e9207174ab6f16e5d56817186ec446e5348ab0025255fc8a585d064b726,
verified against the read-only reference. Original150B prefix003977CD..00397862
runs its own A snapshot/pointer setup and first output under Unicorn, with no
stubs/calls. Raw instruction/memory events, normalized committed writes, input
register/memory/MXCSR readback, exact driver/interpreter/native-tool DLL identities
before capture and unchanged after, retained inputs/manifest and consumer preimage
are included. Own checker validates a nonempty completed capture and controls.

For row0/column0, define `pk=f32(B[0,k]*A[k,0])`. The observed original chain is
`f32(f32(f32(p1+p0)+p2)+p3)`, from ADDSS00397844/50/57. With all A entries1 and
B row0=(2^24,1,1,-2^24), injected disjoint inputs and MXCSR1F80, the original
stores **0x00000000 (+0)**. A host balanced regrouping predicts **1.0f**, while
the real-number sum is **2.0**. These alternatives are source/host predictions,
not two further original-code runs. The ordinary B row0=(1,2,3,4) control stores
10.0f, matching both groupings. A labelled disposable ADDSS->SUBSS intervention
at00397850 changes that ordinary stored output to4.0f; its code identity differs
and it is not accepted as shipping behavior.

Required numeric qualifier: preserve separate f32 products and this accumulation
chain for the tested first output; algebraic matrix order does not license
reassociation, wider intermediate arithmetic or fused operations while claiming
bit-exact reconstruction. No existing consumer is alleged to have executed a
balanced implementation. Extend a whole-matrix rule only after the other output
chains are independently read; this package does not test them.

Limits: injected snapshot/input/stack state and masked nearest-rounding MXCSR1F80.
The entry skips the cookie/prologue/nonvolatile saves. Stop follows the first
output store, before other outputs/columns, loop, return and cookie check.
No whole invocation, native CPU parity, other MXCSR/input domain, NaN payload,
subnormal, alias law, gameplay reachability or renderer presentation claim.
The emulator's control/state receipts are not live-game health observations.

Cleanup: disposable emulator objects, no PC/game/process/save/config/reference
or peer edits. The initial board preflight refusal and subsequent supported PASS
are retained; its unknown cause is not invented. Supported claim succeeded after
a fresh check, no guard bypass/recovery replay. Independent review and canonical
consumer agreement remain pending; whole L1+L2 goal remains NOT_MET.
