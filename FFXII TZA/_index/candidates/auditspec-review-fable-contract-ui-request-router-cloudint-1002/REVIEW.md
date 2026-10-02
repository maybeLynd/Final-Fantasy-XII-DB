# Audit-spec review: FABLE cloudint interior citations (fable-contract-ui-request-router-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CONTRACT-UI-REQUEST-ROUTER-CLOUDINT-10` · Package: `_index/candidates/fable-contract-ui-request-router-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 4 rows applied, 19 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 4 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 4 rows exact: 002E0DA0 (btr 15 + keep 0x8000; >6 unsigned -> 2|kept; seven-entry offset table at 002E0E08 -> 0x11/0x12/0xA/0xF/0x13/6/0x16 each ORed with the kept bit), 002E1AE0 (byte 0215F1A1==0 -> byte 0215F1A0=1, dword 0215F1A4=0xC, 0215F1A8=0), 003462D0/003470D0 (00229EB0 byte -> r8+4, 0 -> r8+8, two 00267E10 pops, 002E1A60(b,a), 002E1690, tail 002E0650).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
