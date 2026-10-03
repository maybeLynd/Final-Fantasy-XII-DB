# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-how-the-ard-loader-binds-area-battle-dat-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-THE-ARD-LOADER-BINDS-AREA-BATTLE-DAT-HO` · Package: `_index/candidates/opus-how-the-ard-loader-binds-area-battle-dat-homing-1002/` · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 8 anchors; rejected 0, missing 0.
- Semantic pass: **all 2 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Both exact: `[r8]` zeroed, the `byte rdx+0x15` argument to `002E3E20`/`002E4000` with 0 and with -1, and the tail jumps.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
