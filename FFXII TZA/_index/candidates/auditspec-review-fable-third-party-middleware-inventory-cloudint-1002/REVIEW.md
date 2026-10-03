# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-third-party-middleware-inventory-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THIRD-PARTY-MIDDLEWARE-INVENTORY-CLOUD` · Package: `_index/candidates/fable-third-party-middleware-inventory-cloudint-1002/` · Page: `23-Third-Party-Libraries/third-party-middleware-inventory.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 3 rows, 15 anchors; rejected 0, missing 0.
- Semantic pass: **all 3 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 3 exact. `00887630` was read in full (0x1CB bytes, 4x-unrolled loop and its tail loop): stack slots `[rsp+28h]`/`[rsp+30h]`/`[rsp+38h]` = fifth/sixth/seventh, constants read from the image as doubles 30.0 (`01CEBC48`) and 0.10000000149011612 (`01CEBBB0`) and float 16.0 (`01CEBC84`), the 0..7 clamp, store-only-when-greater, and the bound checked only after each store.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
