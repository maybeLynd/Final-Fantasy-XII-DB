# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-post-processing-effect-catalogue-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-POST-PROCESSING-EFFECT-CATALOGUE-C` · Package: `_index/candidates/fable-the-post-processing-effect-catalogue-cloudint-1002/` · Page: `17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 1 rows, 5 anchors; rejected 0, missing 0.
- Semantic pass: **all 1 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Exact: slot 1 release of `+0`, slot 0 with `edx`=1 on `+8`, both zeroed after.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
