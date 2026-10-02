# Audit-spec review: OPUS cloudint interior citations (opus-contract-shared-transform-workbench-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-SHARED-TRANSFORM-WORKBENCH-CLOUDIN` · Package: `_index/candidates/opus-contract-shared-transform-workbench-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 1 rows applied, 5 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 1 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — the single row 00455560 exact vs the certified image: 64-byte stack-matrix copy, bits 2-4 of R byte+0x4A arm select (02AEEC30/02AEEC70/02AEEA60 via the 360/466-byte routines), the helper call chain, R byte+0x240==2/4 gate -> 728-byte routine, the seven globals filled (02AEE908/02AEE900/02AE0370/02AE0360/02AE02B0/02AE02B4/02AE02A0-02AE02AC), the P=0020E600 non-null path, bits 1-2 of R byte+0x294 arm select (02AE0280=0/2, 154-byte vs 280-byte routines, case-3 double call).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
