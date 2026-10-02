# Audit-spec review: FABLE cloudint interior citations (fable-the-rig-of-seventeen-controllers-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-RIG-OF-SEVENTEEN-CONTROLLERS-CLOUD` · Package: `_index/candidates/fable-the-rig-of-seventeen-controllers-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 17 rows applied, 82 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 17 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 17 rows exact vs the certified image, including the controller-setter family (object lookup by signed index, controller flags, state bits/masks, values 0x2000/0x4000, selector values 0/0xB, 0xFFF sentinel, linked-list traversal with global-base re-reads).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
