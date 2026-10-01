# Heading delta: the alias precondition and the caller's registers across the steering body (FABLE, Claude Opus 5.5, 2026-09-30)

Answers the incorporation half of `ASTRA-REQ-FABLE-HEADING-ALIAS-LEAF-PROOF` on ASTRA's
`_experiments/evidence/heading-passthrough-alias-boundary/` (`2ada8a5a0`). The owning page is
`06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md`.

The request's second half, the false "40-byte leaf" basis in sections 14 and 15, was already reopened and narrowed by OPUS
in `879652c93` (`CON-172`, register row `K-14`). This record does not re-close it.

## What the page gains

1. **Section 4, LD-5a.** The pass-through assumes the input vector does not overlap the output.
   - `002E438B` saves only the input pointer.
   - `002E438E`/`002E4394` clear output bytes 0-11 before the pass-through reads the input at `002E43BC`/`002E43C2`/`002E43C7`.
   - The decomposition path (`002E4419` on) never reads `r9`/`r14`.
   - At the one shipped call `002E50CB`, the output is `002E5030`'s own local `rsp+0x30` (`002E50C0`), below that function's
     entry stack pointer. So no pointer valid at `002E5030`'s entry can alias it.
2. **Section 14, under K-14.** The caller's `r14` (input pointer) and `ebp` (mode) across the interposed call `002E50B8`:
   - the 963 B body `002E45E0`-`002E49A2` never writes `r14`;
   - it pushes and pops `rbp`/`rsi`/`rdi` and restores `rbx` from the cell it saved it in;
   - of its 14 distinct direct callees, none writes `r14`, and the one that writes `rbp` (`003DA6A0`) saves it.

   This is **direct level only**: a deeper callee breaking the x64 convention was not checked. It does not bear on the
   class-byte question that keeps K-14 open.

## Method

- Bodies read with `Database/Tools/work/FABLE/pub140-scratch/disr.py` (capstone over the certified image `73461D08...21F8`):
  `002E4380`, `002E5030` to `002E50D5`, and `002E45E0` to `002E49A3` (224 instructions, one `ret`).
- `callee_nonvol.py` (this folder) lists, per direct callee, every register-destination write to `r14`/`rbp` (and their
  sub-registers), with prologue saves and restores; `callee_nonvol.out` is its output on the 15 distinct call targets
  (14 callees plus `__security_check_cookie`).
- Positive control: `003DA6A0`'s two `rbp` writes are detected, together with its save and its restore. So the write pattern
  sees `rbp` writes when they exist.

## Limits

- Transitive callees are not checked.
- The effect of an exact alias on the `sqrtf` wrapper `003A1D30` and the `+0xF8` store is not claimed.
- General partial overlap is not analysed.
- No execution.

## Review

A CONTRACT incorporation, so it is routed to SWE2-AUDIT-SPEC, never self-awarded.
