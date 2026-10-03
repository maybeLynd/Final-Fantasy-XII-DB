# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-les-registered-before-main-phyre-prendering-module-1-r9a)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-LES-REGISTERED-BEFORE-MAIN-PHY-D714E` · Package: `_index/candidates/opus-member-les-registered-before-main-phyre-prendering-module-1-r9a/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 1 row, 5 anchors, mode `member`; rejected 0, missing 0, skipped 23 (README agrees); corrections none.
- Every row read in full against its sentence, clause by clause (bodies in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/full_<pkg>.txt`, rip targets resolved with the value at each target):
  - `006221E0` exact. B uses `btr eax, 0x1f` with `cmp 1; jbe` (unsigned above 1) and `test; je` for the 0 case. `P` = qword [B + (i<<6) + 0x18], with i zero-extended through `mov r12d, edx`. `L` is 0 when bit 1 of dword [o+0x18] is set (`shr 1; test al, 1`), else `cmovb` gives min(dword [o+0x10], 0xB). `D` = qword [`005FD050()` + 0x110].
  - The loops: an outer counter of 6 in `[rsp+0x70]`, with `w` reloaded from +0x28 at each f. The inner `esi` runs 0..L inclusive (`jbe`), with `F` = qword [o] and B reloaded each step. The slot +0x180 call gets (D, qword [B + 64i], r14 + esi, 0, P, ((dword [F+0x14] * a) * k) >> 3, 0); `r14` grows by L + 1 per f.
  - The step: `z` = w, or dword [o+0x28] when w is 0, rounded to 4 under bit 0 of byte [F+0x18]. P += (z * dword [F+0x14] * z) >> 3: two 32-bit `imul`s, then `shr rax, 3` on the zero-extended product. Then w = max(w >> 1, 1) via `cmova`.

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- Each row in this family is a different function, so there is no shared shape to compare mechanically; every row was read in full instead.
- Callee behaviour is not reviewed except where the sentence states it (a float or `al` result). The skipped functions are not reviewed. The page's other text is outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
