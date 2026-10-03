# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-widget-message-protocol-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-WIDGET-MESSAGE-PROTOCOL-HOMING-1002` · Package: `_index/candidates/opus-the-widget-message-protocol-homing-1002/` · Page: `16-UI/Widget-Object-Model/the-widget-message-protocol.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 23 rows, 110 anchors; rejected 0, missing 0.
- Semantic pass: **a spread sample of 15 of the 23 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Spread 15-row sample (rows 0,2,3,5,6,8,9,11,13,14,16,17,19,20,22) all exact, re-read by a second SWE2-AUDIT-SPEC stand-in pass, with truncated bodies (rows 0,3,8,13) read in full. Checked: row 3's 5th stack argument (3 pushes + `sub rsp,0x30` -> `[rsp+0x70]` = entry+0x28), row 8's `sub ecx` chain (1,2,3,0x11,0x12) and row 22's case map.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
