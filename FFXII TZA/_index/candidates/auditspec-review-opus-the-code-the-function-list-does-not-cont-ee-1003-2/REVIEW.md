# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-code-the-function-list-does-not-cont-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-CODE-THE-FUNCTION-LIST-DOES-NOT-C-263D9` · Package: `_index/candidates/opus-the-code-the-function-list-does-not-cont-ee-1003-2/` (reviewed at HEAD `a028be1b9`) · Page: `99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row. It was read clause by clause against a raw capstone decode of the certified image. This session checked the image hash: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. The row holds as written; all 16 cell formulas were recomputed from the instructions. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0` and exited 0. The row is already in the page block `## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-the-code-the-function-list-does-not-cont-ee-1003-2)`, line 995 (heading at line 991).
- **Counts.** 1 row, 5 anchors. The listing (`00179920`-`00179A2B`, function-table size 0x10C) ends in `ret`.

Per row:

- **`00179920`**: exact.
  - Loads, `00179938`-`00179961`: `esi` = t0 = `[r9]`, `ebx` = L = `[r8-1]`, `r15d` = t1 = `[r9+1]`, `r14d` = t2 = `[r9+2]`, `r11d` = u0 = `[r8]`, `ebp` = t3 = `[r9+3]`, `r10d` = u1 = `[r8+1]`, `r9d` = u2 = `[r8+2]`, all `movzx`. The first store is `0017996F`, after the last load at `00179961`, and `r8` is overwritten only at `00179966`, so all eight are read before any store.
  - `00179966`/`0017996C`: `r8` = `rdi`+3·`rdx` (row 3).
  - h(t0, L) `00179952`-`0017996A`, stored at `0017996F` `[rcx+rdx+2]` = (1,2) and `00179973` `[rcx]` = (0,0).
  - h(t0, t1) `00179975`-`0017997B`, stored at `[rcx+2rdx+2]` = (2,2) and `[rcx+rdx]` = (1,0).
  - h(t1, t2) `00179984`/`00179988`/`00179991`, stored at `00179995` `[r8+2]` = (3,2) and `00179999` `[rdi+2rdx]` = (2,0).
  - h(t2, t3) `0017998B`/`0017998F`/`00179993`, stored at `0017999C` `[r8]` = (3,0).
  - q(u0, u1, u2): `0017999F`-`001799AA` = (2(u1+1) + u2 + u0) >> 2, stored at `001799AD` `[rdi+3]` = (0,3).
  - q(L, u0, u1): `001799B0`-`001799BA` = (2(u0+1) + u1 + L) >> 2, stored at `001799BD` `[rdi+2]` = (0,2).
  - q(t0, L, u0): `001799C0`-`001799C9` = (2(L+1) + u0 + t0) >> 2, stored at `001799CC` `[rdi+rdx+3]` = (1,3) and `001799D0` `[rdi+1]` = (0,1).
  - q(L, t0, t1): `001799D3`/`001799DB`/`001799DE`/`001799E4` = (L+2 + 2t0 + t1) >> 2 (the `lea eax,[rbx+2]` precedes the `rbx` restore at `001799D6`), stored at `001799E7` `[rdi+2rdx+3]` = (2,3) and `001799EB` `[rdi+rdx+1]` = (1,1).
  - q(t0, t1, t2): `001799E1` t0+2, `001799EF`/`001799F3`/`001799FE` = (t2 + 2t1 + t0+2) >> 2, stored at `00179A01` `[r8+3]` = (3,3) and `00179A05` `[rdi+2rdx+1]` = (2,1).
  - q(t1, t2, t3): `001799F5` t1+2, `00179A09`/`00179A16`/`00179A1D`/`00179A20` = (2t2 + t3 + t1+2) >> 2, stored at `00179A23` `[r8+1]` = (3,1).
  - The 16 stores cover 16 distinct cells, the first coordinate being the `rdx` multiple, as the row defines it. All arithmetic is 32-bit on zero-extended bytes with `shr`, so the formulas are exact for byte inputs.

**1 of 1 exact.** All 5 anchors were checked.

## SWE2-AUDIT-SPEC limits

- Body statements were checked against the bytes. Meanings were not reviewed, including any codec or prediction-mode name a page may give this function.
- The row names no callee.
- README.md records 2 functions as missing (`0017B960`, `00729920`). They are outside this review.
- This review is a non-author read. It does not replace a live check of any behaviour.
