# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-spatial-audio-object-model-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-SPATIAL-AUDIO-OBJECT-MODEL-CLOUDIN` · Package: `_index/candidates/fable-the-spatial-audio-object-model-cloudint-1002/` · Page: `18-Audio/the-spatial-audio-object-model.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 5 rows, 23 anchors; rejected 0, missing 0.
- Semantic pass: **all 5 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 5 exact, including the stack-argument layout of `00223EB0` (`[rsp+20h]` dword 0, `[rsp+28h]` byte 1, `[rsp+30h]` incoming `r9`) and the signed bound/sign tests of `001A7600`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
