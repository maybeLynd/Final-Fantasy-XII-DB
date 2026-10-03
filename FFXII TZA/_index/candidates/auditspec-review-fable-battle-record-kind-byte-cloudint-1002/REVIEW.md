# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-battle-record-kind-byte-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-BATTLE-RECORD-KIND-BYTE-CLOUDINT-1002` · Package: `_index/candidates/fable-battle-record-kind-byte-cloudint-1002/` · Page: `04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 5 rows, 25 anchors; rejected 0, missing 0.
- Semantic pass: **all 5 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 5 exact, including `00235AB0`'s unsigned byte window (`sub al,1Bh / cmp al,0Ch / ja` = 0x1B..0x27) and `0030BA80`'s `bt 0Eh` / `+708h` / `word +714h <= 21Eh` chain.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
