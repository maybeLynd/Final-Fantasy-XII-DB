# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-party-read-in-state-machine-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-PARTY-READ-IN-STATE-MACHINE-CLOUDI` · Package: `_index/candidates/fable-the-party-read-in-state-machine-cloudint-1002/` · Page: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 6 rows, 30 anchors; rejected 0, missing 0.
- Semantic pass: **all 6 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 6 exact.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.

## SWE2-AUDIT-SPEC narrowing / notes

Cosmetic only, no correction required: in `0031BE30` the two-byte stack copy of `+0x40/+0x41` happens before the `r8d < 2` test, so it also runs when only that last condition fails; the sentence groups it under 'when all hold'. The effect is a dead stack write; the return value statement is exact.
