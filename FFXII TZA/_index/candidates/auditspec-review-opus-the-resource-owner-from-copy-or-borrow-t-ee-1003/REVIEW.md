# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-resource-owner-from-copy-or-borrow-t-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-RESOURCE-OWNER-FROM-COPY-OR-BORRO-B5F9F` · Package: `_index/candidates/opus-the-resource-owner-from-copy-or-borrow-t-ee-1003/` · Page: `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `00427B00` exact: `[022C6F28]`, -1 head at `+0x48800`; per record R = g + 0x740 i the three `0020E600` compares against `rcx` with their stores (`+0x68` qword and `0020E620(0)` to `+0x69C`; `+0xD8`/`+0xE0`; `+0xF0`/`+0xF8`); g re-read at `00427B9C`; next = `movsx` word `[g+0x740i+4]` until -1.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
