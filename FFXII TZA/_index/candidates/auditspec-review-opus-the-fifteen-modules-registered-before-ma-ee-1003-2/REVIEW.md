# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-fifteen-modules-registered-before-ma-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-FIFTEEN-MODULES-REGISTERED-BEFORE-F3FB1` · Package: `_index/candidates/opus-the-fifteen-modules-registered-before-ma-ee-1003-2/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `00628050` exact: dword `+0x48` non-zero -> 0x16; `btr 0x1f` count compare; `00627CF0(rcx+0x18, n)`; the per-step re-read choosing `[rcx+0x20]` (count > 1), `rcx+0x20` (count 1) or 0; qword and dword `+0xC` zeroed at stride 16; `00584730` on a non-null `+0x10`, zeroed; 0.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
