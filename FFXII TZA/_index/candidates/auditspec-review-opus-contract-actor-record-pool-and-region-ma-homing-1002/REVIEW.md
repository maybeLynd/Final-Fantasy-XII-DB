# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-contract-actor-record-pool-and-region-ma-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-ACTOR-RECORD-POOL-AND-REGION-MA-HO` · Package: `_index/candidates/opus-contract-actor-record-pool-and-region-ma-homing-1002/` · Page: `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- Semantic pass: **all 2 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Both exact (`and 0xFFFFFFE7` clears 0x8 and 0x10).
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
