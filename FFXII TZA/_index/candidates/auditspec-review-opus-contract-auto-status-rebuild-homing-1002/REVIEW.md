# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-contract-auto-status-rebuild-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-AUTO-STATUS-REBUILD-HOMING-1002` · Package: `_index/candidates/opus-contract-auto-status-rebuild-homing-1002/` · Page: `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 5 rows, 25 anchors; rejected 0, missing 0.
- Semantic pass: **all 5 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 5 exact, including the null-`+0xC0` path addressing byte `0x10` and `0034F5A0`'s slots 3..0, the -1 fill from the `0031B510` result and the pointer-i stores.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
