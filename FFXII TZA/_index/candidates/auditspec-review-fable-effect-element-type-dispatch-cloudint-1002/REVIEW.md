# Audit-spec review: FABLE cloudint interior citations (fable-effect-element-type-dispatch-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-EFFECT-ELEMENT-TYPE-DISPATCH-CLOUDINT` · Package: `_index/candidates/fable-effect-element-type-dispatch-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 50 rows applied, 229 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 50 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 50 rows exact vs the certified image, including the byte-map+offset-table dispatch (decoded: per-type arm addresses verified one level deeper), the entry init/flag helpers and every typed arm body.
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
