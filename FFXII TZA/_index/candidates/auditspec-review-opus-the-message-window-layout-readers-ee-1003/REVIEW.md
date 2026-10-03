# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-message-window-layout-readers-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-MESSAGE-WINDOW-LAYOUT-READERS-EE-6130E` · Package: `_index/candidates/opus-the-message-window-layout-readers-ee-1003/` · Page: `16-UI/Message-Windows/the-message-window-layout-readers.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `002A36A0` exact: the `0x180000` / `0x100000` sete gate; byte `+0x3F3` & 0x3C and the signed word count; the loop runs at least once, `rcx` advanced by 0x60 from its value after each `002A7D30` call (the callee may clobber it), the bound re-read each step; `002A5BC0(w)`, `and 0xE3`, then `or 0x80` on both paths.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
