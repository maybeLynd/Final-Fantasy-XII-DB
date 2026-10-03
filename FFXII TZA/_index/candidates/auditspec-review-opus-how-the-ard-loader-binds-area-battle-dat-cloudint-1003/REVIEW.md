# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-how-the-ard-loader-binds-area-battle-dat-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-THE-ARD-LOADER-BINDS-AREA-BATTLE-89EFC` · Package: `_index/candidates/opus-how-the-ard-loader-binds-area-battle-dat-cloudint-1003/` · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md` (commit 890844135)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `003414A0` exact: `rcx` = `r9` then `00267E10` (`003414AC`); its result to `002E9A60` (`003414B3`); `id` stored at dword `[r8]` (`003414BA`, `rbx` = `r8`); `002E99C0(id)` result passed in `rcx` to `002E9810`, stored at dword `+4` (`003414C9`); dword `+8` = 0 (`003414CC`).
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
