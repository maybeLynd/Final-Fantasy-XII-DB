# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-intentionally-ownerless-functions-and-sh-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-INTENTIONALLY-OWNERLESS-FUNCTIONS-AND` · Package: `_index/candidates/fable-intentionally-ownerless-functions-and-sh-cloudint-1002/` · Page: `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 23 rows, 97 anchors; rejected 0, missing 0.
- Semantic pass: **all 23 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 23 exact, including `003A4070`'s byte test (`lea eax,[rdx-5] / test al,0FAh` plus the `cmp dl,0Ah` exclusion gives exactly 5, 6 and 9), the two mirrored `02F97348` +0x368 set/clear pairs (`00333520` 0x1000/0x2000, `00333640` 0x2000/0x1000) and `0046CC20`'s 1-3 -> 0-2, 4-5 -> 6-7 map.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
