# SWE2-AUDIT-SPEC review: ASTRA filecache read zero-view

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-FILECACHE-READ-ZERO-VIEW-1002` · Package: `_experiments/evidence/filecache-read-zero-view/`
(publisher commit `4a818c6d3`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- `0059D4B0` (92 bytes):
  - When `rax = q30` is non-zero, it calls `2150E0` first and returns its result.
  - When q30 = 0, `mov [rsp+40h],eax` seeds the count slot with 0. Then:
    - `R8D == 0` goes to the exit with full RAX = 0 (the zero q30) and no call;
    - `R8D != 0` with `q28 == -1` and signed `q40 <= 0` (`jle`) also exits with RAX = 0 and no call;
    - `q28 != -1` calls through IAT `008C2140` and returns `eax` = the stack DWORD count.
  - `test r8d,r8d` tests only the lower 32 bits, as the request says.
- So q28=-1, q30=0, q40=0 passes IsOpen, yet both Read count classes return zero with no helper and no I/O.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (prove-02, final) re-run: exit 0, output **byte-identical** to `result-02.json`.
- `control.py`: three CLI refusals identical to retained (failed Read capture, missing retained predicate result,
  missing Read source).

## SWE2-AUDIT-SPEC limits (unchanged)

- The IAT declaration is not live `ReadFile` semantics.
- There is no natural caller, allocation failure, read fault or lifetime evidence.
