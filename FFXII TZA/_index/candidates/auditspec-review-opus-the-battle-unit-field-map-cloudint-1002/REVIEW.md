# Audit-spec review: OPUS cloudint interior citations (opus-the-battle-unit-field-map-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-BATTLE-UNIT-FIELD-MAP-CLOUDINT-1002` · Package: `_index/candidates/opus-the-battle-unit-field-map-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 18 rows applied, 77 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 18 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all rows exact vs the certified image, including the battle-unit field-map bodies (offsets, widths and the field reads/writes).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
