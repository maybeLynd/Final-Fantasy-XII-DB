# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-seb-se-block-index-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-SEB-SE-BLOCK-INDEX-CLOUDINT-1002` · Package: `_index/candidates/fable-seb-se-block-index-cloudint-1002/` · Page: `18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 1 rows, 4 anchors; rejected 0, missing 0.
- Semantic pass: **all 1 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Exact: register-preserving call at `+0x16` and the rotated re-homing into `00210B60`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
