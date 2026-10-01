# Field pre-arbiter focus-send: ordered-equality gate

Question: can an unordered accumulator comparison pass the field pre-arbiter
send gate, and does the current evidence producer distinguish that alternative?
Major system: input/frame scheduling, GG-1. Consumers: FABLE static-order O5 and
SWE2-CONTRACT's input contract; independent review: SWE2-AUDIT-SPEC.

Method **A** is sufficient. Original shipping image SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
exact32B at0022AB68..0022AB87 plus zeroing3B and bit3 helper14B,
retained reader/tool identity and producer/consumer preimages. `result.json`
contains the decoded bytes, conditional interpretation and actual Python checker
controls. No original FF12 instructions were executed, no live capture occurred.

The original `UCOMISS xmm0,xmm7` at0022AB79 is followed by **JP0022AB7C** then
**JNE0022AB7E**, both targeting0022AB90, past the send0022AB83. Under the stated
boundary (xmm7 zero, preceding bit3 gate passes, comparison completes), the call
requires **PF=0 and ZF=1**. The hypothesis that NaN slips through ZF-only equality
is **refuted**. The existing zero-gate conclusion is supported in its ordered
comparison domain; no frame-order or reader-placement result is withdrawn.

The existing O5 producer does not assert either branch. Its actual unmodified
invocation still reports O5 PASS/FAILS0 after the single JP line is changed to NOP
in a disposable copy of its derived cache. Original invocation also passes.
This proves a specific missing evidence obligation, not a defect in the shipping
gate or all the checker. Our exact-byte source obligation rejects the corresponding
private JP-removal mutant. **Required owner change:** bind JP, JNE and their targets
in the current producer, retaining prior result/version; do not merely add prose.

Numeric precision matters: +0/-0 pass; ordinary nonzero and infinities fail;
unordered NaN fails **after a completed comparison**. SNaN with an unmasked
invalid exception does not have that completed continuation. A DAZ-enabled
comparison can treat a nonzero subnormal as signed zero. Therefore “the stored
bits must encode zero” requires a DAZ/domain precondition. Actual game MXCSR,
accumulator values and normal subnormal/NaN reachability are **unobserved**.
These are conditional ISA calculations, not extra FF12 tests. The specifications
used are [Intel SDM UCOMISS](https://cdrdv2-public.intel.com/789581/325383-sdm-vol-2abcd.pdf)
and [Intel SDM Vol1 section10.2.3.4](https://cdrdv2-public.intel.com/671436/253665-sdm-vol-1.pdf).

No new whole-frame initialization/callee-preservation proof, synchronous callback
effects, all51 reader order or live scene behavior. Full cache hash and exact
changed line retained; reproducing the peer invocation needs that matching cache.
Shipping primary slices and our read-only checker are included independently.

Cleanup: temporary cache directory removed; image, peer files, saves/config and
processes untouched. PC OFF. Producer tests, external corroboration and independent
project acceptance remain distinct. Review/consumer incorporation pending.
