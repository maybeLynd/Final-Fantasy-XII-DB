# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-config-screen-and-what-a-setting-cha-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-CONFIG-SCREEN-AND-WHAT-A-SETTING-C` · Package: `_index/candidates/fable-the-config-screen-and-what-a-setting-cha-cloudint-1002/` · Page: `16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 7 rows, 34 anchors; rejected 0, missing 0.
- Semantic pass: **all 7 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 7 exact, including `002CD8A0`'s 10-entry image-base-relative jump table decoded from `002CD8F4` (0x4B4->0x11, 0x4B6->0x12, 0x4B5->0x13, 0x4B9->0x14, 0x4B7->0x15, 0x4B8->0x16, 0x4BC->0x17, 0x4B3/0x4BA/0x4BB->0x10) and `002726C0`'s 64-bit products with arithmetic shifts.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
