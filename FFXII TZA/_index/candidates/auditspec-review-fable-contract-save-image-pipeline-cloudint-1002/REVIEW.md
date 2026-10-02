# Audit-spec review: FABLE cloudint interior citations (fable-contract-save-image-pipeline-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CONTRACT-SAVE-IMAGE-PIPELINE-CLOUDINT` · Package: `_index/candidates/fable-contract-save-image-pipeline-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 5 rows applied, 18 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 5 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 5 rows exact: 002DF060 (ecx=-1 tail-jump 001DBE40), 002EF890 (7 iterations clamped 0..6 via jns/cmovg over 0x30-byte entries at 022BDD60, 0024CFF0 on nonzero dword+0 then zero +0 and byte+4), 00349B30/0034A050 (00267E10 pops, 0017DB70(00D10C20), tail 002EF840), 003633B0 (byte 022CBB2D equality gate -> 00363840, else 002DF0F0(0) when either dword nonzero, then zeroes 022CBA70 and the byte).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
