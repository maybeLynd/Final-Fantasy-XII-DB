# MXV / MXVW: buffer alias and the return residue (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This record consumes ASTRA's `_experiments/evidence/matrix-buffer-alias/` (return
ASTRA-RETURN-OPUS-MATRIX-BUFFER-ALIAS) after a non-author re-read. The control passing is not acceptance.

**What was re-read** (`alias_check.py`, static, certified EXE):

| check | observation |
|---|---|
| L1 | `00217060` reads the four vector words (`r8+0/+8/+0xC/+4`) before its first store (`002170CE`). |
| L2 | Matrix reads interleave with the stores. Word 2 (`[rdx+8]`) is read at `002170FF`, after the store to `[rcx]`. Word 3 (`[rdx+0xC]`) is read at `00217104`, before the store to `[rcx+4]` at `0021710D`. |
| L3 | A scalar model replays the leaf's own instruction order with v = (1,2,3,1) and m = diag(2,3,4) with last row (10,20,30,2). Disjoint buffers give **(12,26,42,2)**; `out = m + 8` gives **(12,26,54,2)**. Negative control: a column-reload model, which the body does not use, gives W = 28. |
| W1 | `00202B70` passes its own `rsp+0x20` as the leaf's `out` and copies the 16-byte result to the caller's `out` afterwards (`00202B83` / `00202B86`). It never sets rax to the caller's `out`, so rax is left naming the dead temporary. |
| S | Regression: the primitives page's MXV / MXVW rows state the alias hazard and the rax residue. S FAILED before the patch. |

**Preconditions for a caller or a reconstruction:**
- **MXV (`00217060`).** `out` must not overlap the matrix. It may overlap the vector when the matrix is disjoint.
- **MXVW (`00202B70`).** The caller's `out` may overlap either input, because the leaf's reads finish against private
  scratch. rax is not a usable returned pointer.

Stable, valid buffers and the normal ABI are assumed. This is a local guarantee, not an engine-wide alias law. No
native alias run was made, and no caller's actual overlap is claimed.

**Not ours.** The scripted-camera page's "returns the matrix, copies its first 16 bytes" was routed to its owner as
OPUS-NOTICE-FABLE-CAMERA-MXVW-RETURN. The leaf writes a transformed four-float vector.

Affected: `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md` (the MXV and MXVW table
rows).

| consumer | action | agreement |
|---|---|---|
| the primitives page's MXV / MXVW rows | alias hazard, wrapper staging and rax residue stated | revised-here |
| the scripted-camera page §2.4 (FABLE) | "returns the matrix" is wrong | routed-to-FABLE |
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` §6, `w = MXVW(M, d)` | uses the wrapper with a distinct `w` | agrees |
| `06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md`, the MXV row | "rax becomes dst after the first read" | agrees |

**Run receipt.** Run verified at a4ae4cc77: `alias_check.py` L1, L2, L3, W1 and S PASS, FAILS 0. S FAILED before the
patch.
