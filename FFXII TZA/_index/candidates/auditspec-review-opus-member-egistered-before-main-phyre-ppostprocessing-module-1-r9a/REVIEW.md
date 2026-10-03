# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-egistered-before-main-phyre-ppostprocessing-module-1-r9a)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-EGISTERED-BEFORE-MAIN-PHYRE-PP-4685B` · Package: `_index/candidates/opus-member-egistered-before-main-phyre-ppostprocessing-module-1-r9a/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 1 row, 5 anchors, mode `member`; rejected 0, missing 0, skipped 38 (README agrees); corrections none.
- Every row read in full against its sentence, clause by clause (bodies in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/full_<pkg>.txt`, rip targets resolved with the value at each target):
  - `00654470` exact. The 0x16 early return; `h` = `0063A990(c, 1, 02CBB900, 0)` and `e` = `005D8E40(c, h)`, each null returning `ebx` = 0. r = 5 goes to F on byte [e+8] or a null `p`. A non-zero `0060DD70(p, x, y, 02CF7838, 0)` goes to F with that r; on the zero path come the bit-1 clear, byte [p+9] = 0, `00610990(p)` and byte [e+9] = 0. Then `q` (qword [e] or 0, no test), its bit-1 clear and `00610990(q)`. `0064A000(c, x, y, 02CF7480, 0, 0, 0)` is stored at +0xD18. The re-check of +0xD68 returns 0x16, the `02CF7838` compare on q' returns 5, else e goes to +0xD68 and the return is 0. F calls `0063ABF0` twice, (c, e) then (c, h).

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- Each row in this family is a different function, so there is no shared shape to compare mechanically; every row was read in full instead.
- Callee behaviour is not reviewed except where the sentence states it (a float or `al` result). The skipped functions are not reviewed. The page's other text is outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
