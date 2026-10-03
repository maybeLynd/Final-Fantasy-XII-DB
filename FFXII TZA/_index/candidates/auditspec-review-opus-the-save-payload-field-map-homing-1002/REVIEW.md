# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-save-payload-field-map-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SAVE-PAYLOAD-FIELD-MAP-HOMING-1002` · Package: `_index/candidates/opus-the-save-payload-field-map-homing-1002/` · Page: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 6 rows, 28 anchors; rejected 0, missing 0.
- Semantic pass: **all 6 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 6 exact. `00264A40`'s 9-entry jump table was read from the image (0,1,2->0; 3->2; 4->1; 5->3; 6,7->return; 8->4). `00356E10`'s reverse-order float hand-off and `00574160` were read in full: prefix = result-1, length min(word, 0x7F-prefix), and the `+0x2D` masks `0xD7|0x10` / `0xC7`.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
