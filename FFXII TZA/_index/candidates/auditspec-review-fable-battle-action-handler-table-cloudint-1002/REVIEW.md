# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-battle-action-handler-table-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-BATTLE-ACTION-HANDLER-TABLE-CLOUDINT-1` · Package: `_index/candidates/fable-battle-action-handler-table-cloudint-1002/` · Page: `07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 3 rows, 15 anchors; rejected 0, missing 0.
- Semantic pass: **all 3 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 3 exact, including the A/B crossing in `00344390` (A's mapped value reaches `+0x4D`, B's `+0x42`, then `rcx`=mapped A, `rdx`=mapped B into `004686D0`) and the `cmove` row zeroing in `00426520`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
