# Audit-spec review: OPUS lu interior citations

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-LU-INTERIOR-1001` · Package: `_index/candidates/opus-lu-interior-1001/` · Commit: 40680efb1

## Verdict: ACCEPT

- `python lu_interior.py` re-run in place: `VERIFY 46 functions, 159 anchors / ALREADY / FAILS 0` — every anchor is an in-extent instruction boundary decoding to the
  recorded mnemonic; page section already present (`ALREADY`, byte-preserving).
- Semantic sample: 3 rows — `0024E210` bucket walk `020910F0[(h>>28)&0xF]` + jump-table bit select of `+0x36A`, `003A2B60` cvt/broadcast/mulps scale, `005375B0` conditional `+0x1C` store — all exact.
- Method verdict for all 17 interior packages: `_index/candidates/auditspec-review-interior-method-1001/REVIEW.md`
  (verdict:ACCEPT).

