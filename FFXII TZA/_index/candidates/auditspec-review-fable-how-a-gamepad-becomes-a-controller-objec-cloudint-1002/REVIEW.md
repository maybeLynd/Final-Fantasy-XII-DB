# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-how-a-gamepad-becomes-a-controller-objec-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOW-A-GAMEPAD-BECOMES-A-CONTROLLER-OBJ` · Package: `_index/candidates/fable-how-a-gamepad-becomes-a-controller-objec-cloudint-1002/` · Page: `15-Input/how-a-gamepad-becomes-a-controller-object.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- Semantic pass: **all 2 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Both exact: `test al,0xFA` on `v-0x14` admits 0x14/0x15/0x18/0x19, 0x19 excluded by the following compare; returns 1 on every path.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
