# Scaled procedural random arithmetic: preserve multiply-then-subtract

**PASS_ORIGINAL_WINDOW — method B. Not a live game or whole invocation.**
Verified shipping image73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
complete418B3D8E50 parent32f4c93324e6c153518b5b42e85597f75495de8f66171fd58daf355e7b9a063a.
Executed unchanged58B3D8F3F..3D8F78, SHA
f35064469004fa9448432dd22dc7c46767058dbb4c833ab86c8063ea4bc3cdd8.
Retained parent source/manifest and shipping-reader identity were checked against
the exact executable. The existing emulator/reader were reused; no platform rebuild.

The RNG page's `A * (sample - 1.0)` is an algebraic description, **not a bit-exact
replacement**. Source3D8F52 MULSS multiplies sample by amplitude;3D8F5D separately
multiplies amplitude by the shipping1.0 at01EF93FC;3D8F6D SUBSS subtracts those
rounded products. The store3D8F71 leaves the result at022D92E0.

| Injected finite input under MXCSR1F80 | Original observed result | Factored binary32 formula |
|---|---|---|
| A3E99999A (0.3f), sample3F900001 | 3D1999A0 | 3D1999A4 |
| A3F000000 (0.5f), same sample | agrees | agrees |

The ordinary0.3f case refutes bit equivalence. The power-of-two control shows
why agreement on an easier input would not discriminate. Before capture, the
common-seed sample3FB90003 with0.3f predicted agreement under both formulas; that
**failed discriminator** is retained, not represented as another original run.
Candidate seed45848000's source recurrence predicts3F900001 after five steps;
the experiment **injects that sample** rather than claiming to have executed the
recurrence, native save/restore or normal caller path.

Raw capture preserves initialized register/stack/scratch/constant state, every
instruction PC, read events, raw write events and normalized per-instruction
before/after writes. It confirms four writes at3D8F44/56/65/71, the result in
XMM1 **and** stored memory, unchanged input/constant, exact stop/RSP and MXCSR
controls. A disposable SUBSS-to-ADDSS instruction mutation changes the stored
result and is rejected by the original-order predicate. It is an explicit
instrument/detection intervention, not shipping behavior. The normal cases
execute original instructions unchanged. Nonempty complete receipt checks pass.

Useful consequence: a bit-exact numeric implementation must retain
`f32(f32(A*sample) - f32(A*one))`, with the actual constants/FP environment. This
packet establishes the finite prepared examples and source order; it does not
prove every amplitude, all rounding/exception modes, negative/subnormal behavior,
live rendering, native effects, whole-function return or normal reachability.
Entry skips the initial amplitude test, mode branch, five recurrences and native
save; stop precedes the second gate/two recurrences/restore/return. None are
silently stubbed as proof of effects. Existing EXP070/071 inputs/results untouched.

Python/version/interpreter hash, decoder/emulator version, module and driver hash
were preserved in raw.json. `tool-identity-supplement.json` supplies actual loaded
DLL paths/hashes **after** capture, with that timing disclosed; it is not a false
pre-run provenance receipt. Current repeatability checks can pin those binaries.

FABLE owns rng-streams formula; OPUS exact arithmetic/contract consumers. The
authored-integer sibling and workbench page already describe multiply-then-
subtract and are not refuted by this packet. Route only the factored consumer
and new numeric rule. Independent acceptance and canonical incorporation remain
pending. Game/PC stays OFF; disposable emulator only, no saves/config/reference
changes or live cleanup claim. Database L1+L2 goal NOT_MET; no L3 phase.

Player version: simplifying the formula for small visual variations can slightly
change its value. We tested the real arithmetic instructions with controlled
inputs; when the game reaches them in play remains a separate question.
