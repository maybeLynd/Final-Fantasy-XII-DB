# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-hchk-hctg-hdat-handbook-indexes-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HCHK-HCTG-HDAT-HANDBOOK-INDEXES-CLOUDI` · Package: `_index/candidates/fable-hchk-hctg-hdat-handbook-indexes-cloudint-1002/` · Page: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 4 rows, 20 anchors; rejected 0, missing 0.
- Semantic pass: **all 4 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Rows `002C2280`, `005766E0` and `00576DA0` are exact. That includes `005766E0`'s read of byte `R+0xC9` before R is tested, and the 32-bit table base. Row `00574080` is exact except for one edge-case parenthetical, below.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing (row `00574080`):** the parenthetical "a null `rcx` leaves the middle value 0, so the last load reads address 0" skips an earlier fault. With `rcx` = 0 the body first executes `mov rax, qword ptr [rsi+0xE0]` at `005740BD`, a read of address 0xE0. Replacement wording: "(a null `rcx` faults first at `005740BD`, reading qword `+0xE0` of address 0)". Everything else in the row is exact: the three-load chain, B with its two null guards and the 100 default, the unsigned `div` by word `+0xA` of the 20-byte entry, and byte `+7` = byte `P+8` minus the stored low byte. The producer applies the narrowing.
