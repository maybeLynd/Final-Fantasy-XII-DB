# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-what-the-engine-fixes-at-boot-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-WHAT-THE-ENGINE-FIXES-AT-BOOT-CLOUDINT-1002` · Package: `_index/candidates/opus-what-the-engine-fixes-at-boot-cloudint-1002/` · Page: `00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 4 rows, 20 anchors; rejected 0, missing 0.
- Semantic pass: **all 4 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 4 exact, including `00467AD0`'s signed divide-by-64 (`cdq; and edx,0x3F; add; sar 6`) and every constant in `00475310`.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
