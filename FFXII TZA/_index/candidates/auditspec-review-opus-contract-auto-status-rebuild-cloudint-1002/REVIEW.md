# Audit-spec review: OPUS cloudint interior citations (opus-contract-auto-status-rebuild-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-AUTO-STATUS-REBUILD-CLOUDINT-1002` · Package: `_index/candidates/opus-contract-auto-status-rebuild-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 13 rows applied, 55 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 13 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 13 rows exact vs the certified image, including 001E0C30 (singleton -> qword+0xDF8 tail 00225680), 002B3E30 (the float min/max ladder: +0x24 += +0x14; +0x20 raised to +0x10, +0x30 to +0x20, +0x34 to +0x24 via comiss; then zeroes +0x10..+0x28 and stores 0x3F800000 at +0x1C/+0x2C), 003592C0 (bts/btr bit ecx of byte 022C8005, four-byte OR bit-0 test, 003588B0 non-null -> tail 0026D6D0), 0050E060 (three-pointer resolve then r/q/p float stores through first/second/third pointers), and 003241D0's decoded dispatch.
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
