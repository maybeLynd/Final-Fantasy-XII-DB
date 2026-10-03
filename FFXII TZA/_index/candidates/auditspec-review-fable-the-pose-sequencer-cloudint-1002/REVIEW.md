# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-pose-sequencer-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-POSE-SEQUENCER-CLOUDINT-1002` · Package: `_index/candidates/fable-the-pose-sequencer-cloudint-1002/` · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/the-pose-sequencer.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- Semantic pass: **all 2 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Both exact, including the 32-bit truncated `word + r8d` base in `00477670` (`add edx, r8d` zero-extends) and the `+0x1E<<16 | +0x20` return of `00504800`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
