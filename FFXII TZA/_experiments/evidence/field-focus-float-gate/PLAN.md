# Field focus-input floating gate

Question: does the field frame's pre-arbiter focus-send gate admit only a
zero step accumulator, or also an unordered comparison? Consumer: FABLE GG-1
static-order O5 and SWE2-CONTRACT input GG-1 qualification. FABLE's frame/reader
census and actual live gates remain separate work.

Known evidence: gg1_order.py checks UCOMISS at0022AB79, xmm7 zeroing at0022A9EF
and bit3 helper003583A0. Its O5 does not bind the actual branch after UCOMISS.
Competing explanations: ordered-equal gate; ZF-only equality; or additional
parity/domain validation elsewhere that excludes unordered input.

Method A first, cheapest sufficient: exact shipping bytes/operands/CFG around
the comparison, immediate branches and zero provenance; conditional flag
semantics for positive/negative zero, ordinary nonzero, infinities and NaNs.
If branch/data provenance requires execution, select B only for that bounded
original slice. No live test establishes normal NaN reachability here.

Controls: nonzero rejection versus zero admission, parity-sensitive hypothetical
branch/control and exact source-obligation mutation. Pin executable/reader/tools;
retain all source inputs and primary consumer preimages. Pass only with nonempty
exact decode and complete immediate gate identification. Fail/invalidate on
hash/identity mismatch, unresolved additional gate or unsupported FP exception
assumption. No claim about game MXCSR, normal malformed input, native exception
handling, all51 readers, dispatch/callback effects or scene timing.

Stop after the gate domain is settled. Keep producer obligation correction
additive and route peer-owned producer/consumer changes; independent acceptance
pending. No published input rewrite, PC control, game/reference/save/config writes.

Learned discriminator: original JP0022AB7C and JNE0022AB7E both target0022AB90.
The unordered-admission hypothesis is false. Do not rerun it. Bind both branches
and targets in O5; UCOMISS presence alone is insufficient. Exact-zero source
bits additionally need DAZ/domain qualification: effective equality may include
subnormals with DAZ enabled. Actual game MXCSR/accumulator occurrence is unobserved.
No live escalation needed to settle the branch's conditional flag predicate.
