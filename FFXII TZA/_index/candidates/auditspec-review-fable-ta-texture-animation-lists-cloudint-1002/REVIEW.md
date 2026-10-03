# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-ta-texture-animation-lists-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-TA-TEXTURE-ANIMATION-LISTS-CLOUDINT-10` · Package: `_index/candidates/fable-ta-texture-animation-lists-cloudint-1002/` · Page: `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 17 rows, 81 anchors; rejected 0, missing 0.
- Semantic pass: **all 17 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 17 exact, including the stack-argument forwarding of `00180900` and `001AA240` (fifth..eighth stack slots re-homed one by one), `001AB350`'s /0x30 count by the `0xAAAAAAAAAAAAAAAB` multiply plus `shr 5` with `rcx` = record+0x20, and `00467B60`'s double-precision abs mask at `01CEBD80` read from the image (`0x7FFFFFFFFFFFFFFF` x2).
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
