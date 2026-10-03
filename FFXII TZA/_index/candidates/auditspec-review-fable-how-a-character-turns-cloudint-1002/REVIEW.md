# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-how-a-character-turns-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOW-A-CHARACTER-TURNS-CLOUDINT-1002` · Package: `_index/candidates/fable-how-a-character-turns-cloudint-1002/` · Page: `06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 4 rows, 16 anchors; rejected 0, missing 0.
- Semantic pass: **all 4 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 4 exact.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
