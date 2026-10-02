# Audit-spec review: OPUS cloudint interior citations (opus-contract-text-control-codes-and-dyngeo-d-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-TEXT-CONTROL-CODES-AND-DYNGEO-D-CL` · Package: `_index/candidates/opus-contract-text-control-codes-and-dyngeo-d-cloudint-1002/` · evidence commit `73a856c52`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> `VERIFY 2 functions, 8 anchors`, `ALREADY`, `FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows, 8 anchors, no rejections.
- Semantic sample: both rows (full population) read against the certified image, byte-exact:
  - `001E0C30`: `call 00796E20` -> `mov rcx,[rax+0xDF8]` -> tail `jmp 00225680`; rdx/r8/r9 untouched. Exact.
  - `00214890`: `rax=[rdx]` vtable; `r9d=zx r8b`; `rcx=rdx`; `r8d=0`; `edx=zx r9b` (so edx==r9d==zx of r8's low byte); `jmp [rax+0x118]`. Exact.
- Limits hold: body statements only.
