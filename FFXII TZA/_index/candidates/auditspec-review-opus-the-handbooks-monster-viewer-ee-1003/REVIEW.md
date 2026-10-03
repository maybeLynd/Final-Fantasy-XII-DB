# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-handbooks-monster-viewer-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-HANDBOOKS-MONSTER-VIEWER-EE-1003-516FF` · Package: `_index/candidates/opus-the-handbooks-monster-viewer-ee-1003/` · Page: `16-UI/Handbook/the-handbooks-monster-viewer.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `0034B120` exact: `00267E10(r9)`; `002E97B0(e)` and `[a+8]` null tests; `002E6BC0(e, 0)`, `002EB490`, `002ECBA0(.., k, 1)`, `002EC6B0(e, k)` with `[a+8]` re-read; `00314D40(1)` when `002E4C30([a+8], 002E9C00(e))` is 0.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
