# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-phyre-script-object-accessors-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PHYRE-SCRIPT-OBJECT-ACCESSORS-HOMING-1002` · Package: `_index/candidates/opus-phyre-script-object-accessors-homing-1002/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 71 rows, 322 anchors; rejected 0, missing 0.
- Semantic pass: **a spread sample of 15 of the 71 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Spread 15-row sample (rows 0,5,...,70) all exact, re-read by a second SWE2-AUDIT-SPEC stand-in pass: the 0x48-byte copy, Q = qword - (byte & 1), the `001EAD40` skip polarity, the `00684080` argument forms and the `00810450`/`00810580` hand-offs.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
