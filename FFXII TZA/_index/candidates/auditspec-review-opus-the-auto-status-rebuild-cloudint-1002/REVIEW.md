# Audit-spec review: OPUS cloudint interior citations (opus-the-auto-status-rebuild-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-AUTO-STATUS-REBUILD-CLOUDINT-1002` · Package: `_index/candidates/opus-the-auto-status-rebuild-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 7 rows applied, 29 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 7 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 7 rows exact vs the certified image, including 0030BEB0 (four-way early-out then inverse of bit 23), 003241D0 (decoded table: 1-3->0x15 ... 30->0x1E, 21-29->0), 0033F100/005105A0/005106D0 (002640C0 + 00267E10 + 002650B0 resolve then distinct tail-jumps), 00505560 (eight-byte-entry indexed tail-jump through table 00D22790).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
