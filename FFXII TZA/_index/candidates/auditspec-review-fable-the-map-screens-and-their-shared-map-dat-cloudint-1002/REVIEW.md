# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-map-screens-and-their-shared-map-dat-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-MAP-SCREENS-AND-THEIR-SHARED-MAP-D` · Package: `_index/candidates/fable-the-map-screens-and-their-shared-map-dat-cloudint-1002/` · Page: `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 13 rows, 51 anchors; rejected 0, missing 0.
- Semantic pass: **all 13 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 13 exact, including `002BA240`'s switch (1/14/16/18, default `r8d` = value-16, stack record dword 0x20 + zeroed +8..+0x17) and the whole of `0057FB00` (T-table set/clear, the 7-entry `00D23EAC` loop, id selection, the `264F90` 7/0x16/0x19/0x1D -> 0x7EC/0x7EB/0x7EE/0x7ED map, and the 999/59/59 caps with a=b=c=0 when a `2F9860` value was stored).
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
