# Matrix composition: exact first-output rounding

Question: does the original flat row-major B*A composer produce the real-number
or regrouped four-term sum for finite inputs? Consumer: FABLE/OPUS two-transform
primitives composer rule. Matrix order and same-buffer hazards already settled;
those experiments must not be repeated. The MXV row already names addition order,
so its proposed test was rejected during preflight without any original execution.

A preflight: retained349B003977B0 shows products followed by ADDSS p1+p0,
then p2, then p3. For A column0=(1,1,1,1) and B row0=(2^24,1,1,-2^24),
source/IEEE prediction is0; balanced grouping predicts1; real sum is2.
This distinguishes exact numeric rule from the algebraic product alone.

B: verified shipping prefix003977CD..00397862 includes original A snapshot,
pointer setup and first output, ending immediately after its store. No calls or
stubs. Injected disjoint A/B, aligned mapped stack, MXCSR1F80; explicit initial
register/memory readback. Preserve byte identity, raw instruction/read/write
events and committed output bytes, stop/budget/stack controls. Ordinary integer
case agrees across groupings. Labelled ADDSS->SUBSS disposable mutant must change
the stored ordinary output and fail original code identity. Budget128instructions
per case, three cases; stop on first observer/source/state/control failure.

Limits: only first row/column of prepared prefix, no other output/general input
domain/NaN payload/subnormal/rounding mode/alias safety/full invocation or live
renderer behavior. Skip cookie/prologue ABI saves and all later rows/columns,
loop/return/cookie check; no native callback effects. Original arithmetic executed
in emulator, not live game or hardware equivalence certification. Retain exact
prior inputs/manifest/consumer preimage; do not promote source predictions as runs.

Cleanup: disposable emulator objects only, PC OFF; no original image/peer files,
saves/config/processes touched. Source/own controls do not equal independent
acceptance. Freeze byte policy before manifest, publish explicit reviewed paths,
route exact numeric qualifier with consumer ownership respected, then continue.
