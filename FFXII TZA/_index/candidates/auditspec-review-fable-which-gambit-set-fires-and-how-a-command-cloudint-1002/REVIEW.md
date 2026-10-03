# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-which-gambit-set-fires-and-how-a-command-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-WHICH-GAMBIT-SET-FIRES-AND-HOW-A-COMMA` · Package: `_index/candidates/fable-which-gambit-set-fires-and-how-a-command-cloudint-1002/` · Page: `09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 3 rows, 14 anchors; rejected 0, missing 0.
- Semantic pass: **all 3 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 3 exact: pop-then-actor call shapes, the 4-slot party loop with null skip, and the kept flag passed in `r8d` with `edx` 0.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
