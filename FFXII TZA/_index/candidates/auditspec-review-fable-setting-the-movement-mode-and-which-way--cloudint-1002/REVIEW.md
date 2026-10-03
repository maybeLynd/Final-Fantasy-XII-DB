# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-setting-the-movement-mode-and-which-way--cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-SETTING-THE-MOVEMENT-MODE-AND-WHICH-WA` · Package: `_index/candidates/fable-setting-the-movement-mode-and-which-way--cloudint-1002/` · Page: `06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 12 rows, 55 anchors; rejected 0, missing 0.
- Semantic pass: **all 12 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 12 exact, including the float wrap logic of `0026D630` and `003EC510` (constants `01CEBC50`, `00915620`, `01CEBC78`, `00915624` read from the image) and the shared `0x740`-row guard chain in `002E8170`, `002EA780` and `002EA910`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
