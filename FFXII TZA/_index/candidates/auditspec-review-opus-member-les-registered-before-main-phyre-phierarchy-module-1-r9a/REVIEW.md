# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-les-registered-before-main-phyre-phierarchy-module-1-r9a)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-LES-REGISTERED-BEFORE-MAIN-PHY-04D10` · Package: `_index/candidates/opus-member-les-registered-before-main-phyre-phierarchy-module-1-r9a/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 1 row, 5 anchors, mode `member`; rejected 0, missing 0, skipped 4 (README agrees); corrections none.
- Every row read in full against its sentence, clause by clause (bodies in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/full_<pkg>.txt`, rip targets resolved with the value at each target):
  - `00877EE0` exact. A byte-level simulation of the body (`Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/sim877.py`, output `sim877.out`; initial bytes symbolic) gives written ranges `+0..+B +10..+1B +20..+33 +38..+43 +48..+83 +88..+93 +98..+C7`, exactly the sentence's seven ranges. Non-zero final dwords are only +0x20 = 1, +0x24 = 0xA, +0x50 = 0xA, +0x54 = 1, +0xA0 = 0xA and +0xA4 = 1. No written byte ends unknown, so every copy reads a field already zeroed or is overwritten. The `cmp qword [rcx+0x68], r9` sees 0, and `rax` = `rcx` at return.
  - Control: `sim877.py --plant` changes the immediate of `mov qword [rcx+0x24], 0xa` to 0xB in memory; the simulation then reports +0x24 = 11 and +0xA0 = 11 (`sim877_plant.out`), so the simulator responds to the bytes it reads.

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- Each row in this family is a different function, so there is no shared shape to compare mechanically; every row was read in full instead.
- Callee behaviour is not reviewed except where the sentence states it (a float or `al` result). The skipped functions are not reviewed. The page's other text is outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
