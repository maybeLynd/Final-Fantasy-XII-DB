# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-contract-save-image-buffers-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-SAVE-IMAGE-BUFFERS-HOMING-1002` · Package: `_index/candidates/opus-contract-save-image-buffers-homing-1002/` · Page: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- Semantic pass: **all 2 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Both exact; `001AA120` read in full (map at `rcx+0x268`, key `+0x20`, `001A37C0` insert, `00183320` argument layout from the 32-byte record copy).
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
