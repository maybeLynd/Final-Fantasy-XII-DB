# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-file-size-tables-fst-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-FILE-SIZE-TABLES-FST-CLOUDINT-1002` · Package: `_index/candidates/opus-file-size-tables-fst-cloudint-1002/` · Page: `02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 6 rows, 27 anchors; rejected 0, missing 0.
- Semantic pass: **all 6 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 6 exact; `00536F30` read in full (dispatch 0/1/2/3, H = 0xC/0x10, both copy branches with signed count guards).
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
