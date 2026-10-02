# Audit-spec review: FABLE cloudint interior citations (fable-field-record-table-navimapdata-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-FIELD-RECORD-TABLE-NAVIMAPDATA-CLOUDIN` · Package: `_index/candidates/fable-field-record-table-navimapdata-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 3 rows applied, 12 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 3 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 3 rows exact: 00255330 (ecx!=1 -> 00251F40(dword 020927E8) + word 01E0C2AC |= 0xC; ecx==1 -> nine-call init sequence unless both 0xC0 bits of dword 01E0C320 set, clears bit7 of dword 020927EC, then word &= 0xFFF3 and tail 0017E7D0), 002AC2C0 (cl|0x80 -> byte 01E0CDFF, returns 01E0CDFC), 003778B0 (p=02ADD0F8 non-null, i < dword p+8, word at p+0x10+2*(dword p+4+i) nonzero -> p+w else 01CEB638).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
