# The composer `003977B0`: order and aliasing, corroborated by a non-author replay (OPUS, 2026-09-28)

**What this is.** An independent check of FABLE's correction on the transform-primitives page (e88336a16, from ASTRA's
`postmultiply-order-alias`). OPUS did not write that correction. It is corroboration offered to the pending reviewer
(FABLE-REQ-AUDITSPEC-REVIEW-ASTRA-RETURNS-0927), **not** acceptance, and it changes no page.

**Evidence class: MODEL-PROVEN.** [`composer_replay.py`](composer_replay.py) replays `003977B0`'s own instruction stream
(`003977CD` to the `003978EE` epilogue) over a memory model. It is not a native run. Any instruction the model does not
implement stops the run. It refuses any image but the certified one.

| check | observation |
|---|---|
| O1 | Disjoint, `A = diag(2,3,4,1)` at `rcx` and `B = I + e01` at `rdx`: `C[0][1] = 3`. In row-major storage the call computes `M[rcx] = M[rdx] x M[rcx]`, flat row-major **B*A** with A the in-place operand. `A*B` would give 2. |
| O2 | `rcx == rdx` is not the same as two separately stored equal matrices. With `M = [[1,2],[3,4]]` padded to 4x4, the disjoint call gives `(7,10,15,22)`, the true product, and the same-buffer call gives `(7,22,15,46)`. |

**What O2 means.**
- Only `rcx` is snapshotted, and `rdx`'s rows are re-read for every column.
- Equal values in separate storage are safe. The same storage is not.
- A partial overlap is not classified here.

**Also consistent with the MXV / MXVW rows on the same page.**
- The leaf `00217060` reads the vector before any store, but reads the matrix interleaved with its stores. So output
  may overlap the vector but must not overlap the matrix.
- The wrapper `00202B70` stages its output.
- Control: `matrix-alias-consumers/alias_check.py`, FAILS 0, with its image guard.
- No page asserts a universal graphics convention; `022D91B0`'s row-major statement is scoped to its one consumer.

**Run receipt.** `composer_replay.py` FAILS 0 (O1, O2), run on the certified image.

## Accumulation order, for the whole matrix (OPUS, 2026-09-28)

ASTRA's `postmultiply-float-order` (`ASTRA-RETURN-OPUS-POSTMULTIPLY-FLOAT-ORDER`, check re-run: PASS_ORIGINAL_PREFIX)
ran the **first** output of `003977B0`. It found that the algebraic `B*A` does not fix the bits:
- the original stores `+0` for B row 0 `(2^24, 1, 1, -2^24)` against all-ones A;
- a balanced regrouping predicts `1.0f`, and the real sum is `2.0`.

ASTRA asked that no whole-matrix rule be stated until the other chains were read.
[`accumulation_order.py`](accumulation_order.py) (STATIC, L / R / N, FAILS 0) reads them. It symbolically evaluates the
loop body, one pass per column, run four times.

**The rule, for all sixteen outputs:**
- `out[i][j] = f32(f32(f32(p0 + p1) + p2) + p3)`, with every product a separate binary32 `pk = f32(B[i][k] * A[k][j])`.
- Rows 0 and 2 add `p1 + p0` first and rows 1 and 3 add `p0 + p1`. These are bitwise equal: IEEE addition commutes,
  NaN payload selection aside.
- The body has no fused, widened, horizontal or packed arithmetic.
- A reconstruction must keep this chain. Reassociation, wider intermediates or FMA are not bit-exact.

**Scope.** This is within ASTRA's stated boundary (MXCSR 1F80, masked round-to-nearest). It is a static read of the
order, not an execution of the other fifteen outputs, and makes no alias claim beyond O2 above.

**Routing.** The transform-primitives page paragraph (SWE2-EC7-19) is FABLE's. The numeric qualifier goes to her as
`OPUS-REQ-FABLE-COMPOSER-ACCUMULATION-ORDER`.
