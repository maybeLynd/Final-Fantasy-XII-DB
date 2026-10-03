# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-unlabelled-procedures-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-UNLABELLED-PROCEDURES-EE-1003-FA8B9` · Package: `_index/candidates/opus-the-unlabelled-procedures-ee-1003/` · Page: `16-UI/Unlabelled-Panes/the-unlabelled-procedures.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `00345830` exact: `00267DB0(r9)` twice (a, b); `00265020(d, &x, &y, &z)` with x/y/z at `rsp+0x24`/`+0x28`/`+0x20`; the two `ucomiss` with `jp` making NaN unequal; `003A19A0` with (z, x, a, b) in xmm0-xmm3; `0026B4C0(rcx, f)`; `r8` never read.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
