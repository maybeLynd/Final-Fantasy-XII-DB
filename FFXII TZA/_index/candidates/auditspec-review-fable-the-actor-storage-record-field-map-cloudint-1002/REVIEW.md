# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-actor-storage-record-field-map-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-ACTOR-STORAGE-RECORD-FIELD-MAP-CLO` · Package: `_index/candidates/fable-the-actor-storage-record-field-map-cloudint-1002/` · Page: `04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 6 rows, 27 anchors; rejected 0, missing 0.
- Semantic pass: **all 6 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 6 exact, including the `0x740`-record guards at `022C6F28` (dword -1 / word 0xFFFF / null / `+0x284` zero) in `002E6420` and `002EA970`, and `00358A00`'s unsigned bound with sign-extended index.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
