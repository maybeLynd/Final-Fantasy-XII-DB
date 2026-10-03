# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-render-event-selection-evidence-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-RENDER-EVENT-SELECTION-EVIDENCE-CLOUDINT-10` · Package: `_index/candidates/opus-render-event-selection-evidence-cloudint-1002/` · Page: `17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 4 rows, 18 anchors; rejected 0, missing 0.
- Semantic pass: **all 4 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 4 exact, including `0042DC10`'s null read through `+6` when the id is -1 or `+0x284` is 0.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
