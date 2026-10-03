# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-contract-the-moment-an-action-is-committ-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CONTRACT-THE-MOMENT-AN-ACTION-IS-COMMI` · Package: `_index/candidates/fable-contract-the-moment-an-action-is-committ-cloudint-1002/` · Page: `07-Combat-Action/CONTRACT-the-moment-an-action-is-committed.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 9 anchors; rejected 0, missing 0.
- Semantic pass: **all 2 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Both exact: the `+0x18`/`+0x48` chain clear and the conditional call/tail-jump pair on `+0x448`/`+0x44C`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
