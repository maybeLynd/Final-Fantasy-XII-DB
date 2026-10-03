# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-les-registered-before-main-phyre-pframework-module-1-r9a)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-LES-REGISTERED-BEFORE-MAIN-PHY-E1843` · Package: `_index/candidates/opus-member-les-registered-before-main-phyre-pframework-module-1-r9a/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 2 rows, 10 anchors, mode `member`; rejected 0, missing 0, skipped 3 (README agrees); corrections none.
- Every row read in full against its sentence, clause by clause (bodies in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/full_<pkg>.txt`, rip targets resolved with the value at each target):
  - `007A10A0` exact. `h` is `[rsp+0x50]` after `sub rsp, 0x28` (entry +0x28). `ucomiss` against `01CEBBA8` (1.0) with `jp`/`jne`, so a NaN takes the else path. The equal path stores +0x24..+0x30 and jumps to vtable slot +0x20. On the else path each operand is zero-extended to 64 bits before `cvtsi2ss`. `H` = `cvttss2si` of w / a; `T` uses (h - H) * 0.5 (`01CEBB70`); `W` = h * a; `S` uses (w - W) * 0.5. `add ebx, r8d; je` tests y + T, and `cmp r11d, r10d; jae` tests H below h (unsigned). The two store sets and the shared slot +0x20 tail match.
  - `008744F0` exact: five `00625ED0`/`0062B890` then `00625F00`/`0062BCB0` pairs, each gated on `test al, al`, at the five stated (A, B) offsets in order, then `0060EDA0(o+8, 0)` and the `jmp` to `0060EDA0` with (o+0x18, 0).

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- Each row in this family is a different function, so there is no shared shape to compare mechanically; every row was read in full instead.
- Callee behaviour is not reviewed except where the sentence states it (a float or `al` result). The skipped functions are not reviewed. The page's other text is outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
