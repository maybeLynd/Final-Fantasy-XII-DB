# Audit-spec review: OPUS cloudint interior citations (opus-section-010-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SECTION-010-CLOUDINT-1002` · Package: `_index/candidates/opus-section-010-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 1 row, 5 anchors, rejected/skipped/missing 0.
- Semantic sample: the row (full population) read against the certified image -- `00269530` exact:
  loop `rbx=0..3` over qwords at `0209A1F0` (with a `rbx>3`->rdi=0 guard), byte `+0x18`==1 gate,
  `003587C0(movsx byte +0x19, movzx word +0x1A)`, `q` non-null and `!=` the object, then `002693D0(q,1)`.
- Limits hold: body statements only.
