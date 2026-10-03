# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-battle-text-banks-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-BATTLE-TEXT-BANKS-HOMING-1002` · Package: `_index/candidates/opus-battle-text-banks-homing-1002/` · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 3 rows, 15 anchors; rejected 0, missing 0.
- Semantic pass: **all 3 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 3 exact; `00510E40` read in full (pointers r14,rsi,rdi,rbx -> word0 to rbx ... word3 to r14), and `0056CF10` read in full. Note only: `0056CF10` also sets the first element's dword `+8` bit 0 to (entry byte `+0xA` != 0xFF); the row omits this but states nothing false.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.
