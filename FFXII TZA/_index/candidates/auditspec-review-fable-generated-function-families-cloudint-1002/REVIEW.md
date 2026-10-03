# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-generated-function-families-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-GENERATED-FUNCTION-FAMILIES-CLOUDINT-1` · Package: `_index/candidates/fable-generated-function-families-cloudint-1002/` · Page: `24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- Semantic pass: **all 2 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Both rows exact (vtable-address stores and intrusive-list unlink/self-link).
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
