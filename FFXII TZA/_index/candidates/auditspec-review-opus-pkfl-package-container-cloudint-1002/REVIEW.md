# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-pkfl-package-container-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PKFL-PACKAGE-CONTAINER-CLOUDINT-1002` · Package: `_index/candidates/opus-pkfl-package-container-cloudint-1002/` · Page: `26-PKFL-Package-Container/Container/pkfl-package-container.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 1 rows, 5 anchors; rejected 0, missing 0.
- Semantic pass: **all 1 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Exact; image-base-relative tables resolved (`0x120000+0x21A6EC0 = 022C6EC0`, `+0x21A6EE8 = 022C6EE8`).
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
