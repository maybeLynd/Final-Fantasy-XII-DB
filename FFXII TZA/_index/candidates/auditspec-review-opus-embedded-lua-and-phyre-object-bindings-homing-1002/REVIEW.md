# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-embedded-lua-and-phyre-object-bindings-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-EMBEDDED-LUA-AND-PHYRE-OBJECT-BINDINGS-HOMI` · Package: `_index/candidates/opus-embedded-lua-and-phyre-object-bindings-homing-1002/` · Page: `22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 33 rows, 143 anchors; rejected 0, missing 0.
- Semantic pass: **a spread sample of 15 of the 33 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Spread 15-row sample (rows 0,2,5,7,9,11,14,16,18,21,23,25,27,30,32) all exact, re-read by a second SWE2-AUDIT-SPEC stand-in pass: store widths (movsd/movss/dword/qword), `or rax,1` before compare, vtable slots +0x18/+0x30, the TLS guard and row 27's area arithmetic.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
