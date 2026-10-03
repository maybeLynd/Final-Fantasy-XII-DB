# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-thunk-layer-and-why-call-counts-disa-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-THUNK-LAYER-AND-WHY-CALL-COUNTS-DI` · Package: `_index/candidates/fable-the-thunk-layer-and-why-call-counts-disa-cloudint-1002/` · Page: `24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 4 rows, 17 anchors; rejected 0, missing 0.
- Semantic pass: **all 4 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 4 exact, including `002CEAE0`'s argument set (`r9d` = `rdx`-5 = 2, stack dword 1 and qword 0) and `003B5440`'s bit-0 replace (xor/and/xor).
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
