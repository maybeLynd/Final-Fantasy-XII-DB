# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-dules-registered-before-main-phyre-pphysics-module-1-r9b)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-DULES-REGISTERED-BEFORE-MAIN-P-07816` · Package: `_index/candidates/opus-member-dules-registered-before-main-phyre-pphysics-module-1-r9b/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 2 rows, 10 anchors, mode `member`; rejected 0, missing 0, skipped 18 (README agrees); corrections none.
- Every row read in full against its sentence, clause by clause (bodies in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/full_<pkg>.txt`, rip targets resolved with the value at each target):
  - `00690BF0` exact, traced register by register. All nine doubled products are formed as stated: xx = (x+x)x, ..., zw = (z+z)w. The diagonal is (1.0 - a) - b with 1.0 from `01CEBBA8`. The off-diagonals xy + zw, xz - yw, xy - zw, yz + xw, xz + yw and yz - xw sit at +4/+8/+0x10/+0x18/+0x20/+0x24; float addition is commutative bitwise, so the stated operand order of the sums is immaterial. +0xC/+0x1C/+0x2C are 0, row 3 copies [r8..r8+8], +0x3C = 1.0, and the return is `rcx`.
  - `00691570` exact. t = (m11 + m00) + m22, and N = `comiss 0, t; seta`. The three flag ladders reduce to the stated P, Q and U. The sign mask `01CEBDA0` (-0.0) negates (m22, m10), (m00, m21) and (m11, m02) respectively. S adds 1.0, and h = 0.5 (`01CEBB70`) / `sqrtf`(S) (`00861F14`). a, b and c take their first terms from the saved unnegated rows (`[rsp+0x28]`/`[rsp+0x30]`/`[rsp+0x44]` = m12/m20/m01), and d = h * S. The P permutation gives (d, c, b, a), and the Q permutation swaps (0,1) and (2,3).

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- Each row in this family is a different function, so there is no shared shape to compare mechanically; every row was read in full instead.
- Callee behaviour is not reviewed except where the sentence states it (a float or `al` result). The skipped functions are not reviewed. The page's other text is outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
