# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-shop-screens-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SHOP-SCREENS-CLOUDINT-1002` · Package: `_index/candidates/opus-the-shop-screens-cloudint-1002/` · Page: `16-UI/Shop-Screens/the-shop-screens.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 13 rows, 59 anchors; rejected 0, missing 0.
- Semantic pass: **all 13 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 13 exact; `003F4060` and `0056DED0` read in full (L/I = bits 16-20/21-25, the 0x400/0x80/0x800/0x20 gates against `02F9736C`, writes to the OLD slot, `005674B0` given the new slot).
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
