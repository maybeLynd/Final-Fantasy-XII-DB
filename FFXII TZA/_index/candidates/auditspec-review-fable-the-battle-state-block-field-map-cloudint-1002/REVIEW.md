# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-the-battle-state-block-field-map-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-BATTLE-STATE-BLOCK-FIELD-MAP-CLOUD` · Package: `_index/candidates/fable-the-battle-state-block-field-map-cloudint-1002/` · Page: `11-Party/Battle-State-Block/the-battle-state-block-field-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 8 anchors; rejected 0, missing 0.
- Semantic pass: **all 2 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Both exact: the XOR-AND-XOR single-bit merges into `022C83E8` (bit 4 via `shl 4`, bit 0) and the `+0x18`/`+0x15` tail jumps.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
