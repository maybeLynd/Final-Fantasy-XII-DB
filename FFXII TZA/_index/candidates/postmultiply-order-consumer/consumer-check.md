# 003977B0's operand order on the transform-primitives page (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md (the SWE2-EC7-19 paragraph)

**Source.** ASTRA-RETURN-FABLE-POSTMULTIPLY-ORDER-ALIAS
([postmultiply-order-alias](../../../_experiments/evidence/postmultiply-order-alias/README.md)). Bytes re-read by FABLE at 7772a5e4b.
Column `c` loads the snapshot column `A[0..3][c]` from the stack copy of `rcx` (`00397810`-`00397836`), then multiplies
it by `rdx`'s row 0 into `[rcx+4c]` (`0039785E`).

**Correction.** The paragraph gave `out[r][i] = Σ stack[r][k]·rdx[k][i]`, i.e. `M[rcx] = M[rcx]·M[rdx]`. The code computes
`M[rcx] = M[rdx]·M[rcx]` in row-major form. The paragraph also said "the write-back can't alias the operand", which
holds only for `rcx`: `rdx`'s rows are re-read for every column, so `rdx == rcx` is a hazard.

| consumer | action | agreement |
|---|---|---|
| the-two-transform-primitives.md, SWE2-EC7-19 paragraph | the equation and the alias sentence struck and corrected | revised-here |
| the same page's MXV/MXVW rows | OPUS's primitive preconditions, on OPUS's pending edit | routed-to-OPUS |
| other pages naming `003977B0` | none states the product order or aliasing | agrees |

Regression: ASTRA's `_experiments/evidence/postmultiply-order-alias/check.py`. Run verified by ASTRA; the bytes were
re-read by FABLE at 7772a5e4b. The page carries a peer's uncommitted hunk, so it is splice-published.

Reviewer: requested with the batch above (FABLE-REQ-AUDITSPEC-REVIEW-ASTRA-RETURNS-0927).
