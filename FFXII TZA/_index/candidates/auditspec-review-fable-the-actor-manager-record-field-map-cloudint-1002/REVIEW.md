# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-actor-manager-record-field-map-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-ACTOR-MANAGER-RECORD-FIELD-MAP-CLO` · Package: `_index/candidates/fable-the-actor-manager-record-field-map-cloudint-1002/` · Page: `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 4 rows, 20 anchors; rejected 0, missing 0.
- Semantic pass: **all 4 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 4 exact, including `002A26A0`'s fifth/sixth stack-argument roles (`[rsp+28h]` -> `e+5Ch`, `[rsp+30h]` -> the test and `e+5Ah`) and `00345CD0`'s full body (re-push order f3, f2, f1, then `003590B0()`).
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
