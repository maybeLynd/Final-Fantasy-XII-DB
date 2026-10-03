# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-bone-trails-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-BONE-TRAILS-CLOUDINT-1002` · Package: `_index/candidates/fable-the-bone-trails-cloudint-1002/` · Page: `17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 3 rows, 9 anchors; rejected 0, missing 0.
- Semantic pass: **all 3 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 3 exact: `003712C0` +0x9C==2 test with the `+0xC` tail jump, `0042BDD0` field-0x38 forward, `0042E440`'s conditional second call with `+0x2C/+0x30/+0x34` in xmm1..3.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
