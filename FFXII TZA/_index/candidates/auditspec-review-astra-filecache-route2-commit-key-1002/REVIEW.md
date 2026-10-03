# SWE2-AUDIT-SPEC review: ASTRA filecache route-2 commit key

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the Devin session while it is rate-limited) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-FILECACHE-ROUTE2-COMMIT-KEY-1002` · Package: `_experiments/evidence/filecache-route2-commit-key/`
(publisher commit `81cbc06f0`).

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped as the package states. The 606 arm-byte CFG states are analysis states, not native executions. The
composition is conditional on a private frame, normal ABI, no alias and opaque-state stability.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- `0059EE90` resolver:
  - `lea r9,[r15+28h]` goes to wrapper `1D6D20` (`59EFD7`/`59EFE5`), which forwards it as the fifth arg
    `[rsp+20h]` of `20C1B0` (`1D6D47`).
  - On a hit (`rax>=0`) the resolver returns early. On a miss it continues to the archive arm.
  - The armed path (`test r12b,r12b`) then does `mov edx,[r15+28h]` (`59F1B0`) and calls `59A9B0`.
- `0059A9B0`: `mov esi,edx` (`59A9C3`). The only other write to `rsi` (`59A9EA`) is on the early `-1` exit path.
  The body ends with `mov ecx,esi` and `call 1D6A20` (`59AAA2`/`59AAA4`), so the record+28h DWORD reaches the
  insert entry ECX unchanged.
- `0020C1B0`:
  - The out-key pointer is `r14=[rsp+1A0h]` (entry `SP+28h`, the fifth arg).
  - Empty normalization (`cmp byte [rsp+40h],0 / je 20C2C7`) returns `-1` with no write to `[r14]`.
  - A nonempty path calls hash `674A00` and stores `[r14]=eax` (`20C22D`) before the tree lookup, so it is stored
    on both hit and miss.
  - `674A00` has one `ret`, preceded by `btr eax,1Fh`, so the stored key is 31-bit.
- Consequence, confirmed: when normalization is empty, a later armed archive hit forwards whatever `record+28h`
  held before. That is a retention, not a fresh key.

## SWE2-AUDIT-SPEC reproduction (disposable copy at the ASTRA directory depth)

- `prove.py result-02` (prove-03, the current driver) re-run: exit 0, stdout identical, result **byte-identical**.
- `control.py` (control-01) was run against the six-refusal-tested producer: `prove.py` was replaced by the
  retained `prove-before-publication-map-02.py`, whose sha matches the `prove-02` status. It reproduced exit 0 and
  the same six refusals with matched diagnostics.
- `control-publication-map.py` re-run, with ASTRA's current `prepare-residue-packet-publication.py` as sibling.
  The AST check passed, so `prove.py` differs from `-02` only in the source-map metadata. Both refusals were the
  same (missing map, stale map pin). `actual_guard_sha256` differs from retained because the shared publisher
  has changed since. This is recorded, not a defect in the package.

## SWE2-AUDIT-SPEC limits (unchanged from the package)

- No natural empty archive hit.
- No high-bit key.
- No initialization, reuse, all-caller, callback or lifetime closure.
