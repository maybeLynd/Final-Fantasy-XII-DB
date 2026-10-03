# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-r2-force-fight-toggle-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-R2-FORCE-FIGHT-TOGGLE-CLOUDINT-1002` · Package: `_index/candidates/opus-r2-force-fight-toggle-cloudint-1002/` · Page: `15-Input/Modal-Toggles/r2-force-fight-toggle.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 6 rows, 25 anchors; rejected 0, missing 0.
- Semantic pass: **all 6 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 6 exact, including `0028E5F0`'s `dec; cmp 1; setbe` / `cmovne` polarity and `003667E0`'s masks.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
