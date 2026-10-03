# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-egistered-before-main-phyre-ppostprocessing-module-1-r9b)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-EGISTERED-BEFORE-MAIN-PHYRE-PP-16F4A` · Package: `_index/candidates/opus-member-egistered-before-main-phyre-ppostprocessing-module-1-r9b/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 9 functions, 45 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 9 rows, 45 anchors, mode `member`; rejected 0, missing 0, skipped 30 (README agrees); 6 corrections (`0060F830`, `00654E20`, `00657870`, `00657A20`, `00657BC0`, `006580D0`), each present in its sentence.
- Every row read in full against its sentence, clause by clause (bodies in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/full_<pkg>.txt`, rip targets resolved with the value at each target):
  - `0060F830` exact: P and E are entry +0x28/+0x30. x is built from bits 1/2/3 (the word is zero-extended). The two counting loops step 0x18 and count a non-zero `eax` from `005FD5F0`. k is 32-bit, and `cmp eax, 1; jbe` is unsigned, as the correction says. S = ((0x10 or 8(k-1)+0x10) + 0xF) AND ~0xF. `00600B30(b, S+x, masked dword [d+8])` falls back to slot +0x10 on `al` = 0. The bit-0 P store and the `00604750` cache, the bit-1 `00602A40(b, q)` store, and the `jbe`/`ja` bump/rewind of qword [b+0x38] against qword [b+0x30] all match.
  - `00654E20` exact. memcpy has dst = qword [a+8], src = qword [d+8], n = dword [qword [d+8]], after the low-31-bit xor test. The three Focus strings are confirmed at `00D62E18`/`00D62E30`/`00D62E40`, the two samplers at `00D62BB0`/`00D62E50`. The k store goes to [qword [o+0x38]] or o+0x38. The records are (0x47, `02D34718`/`02D35140`, 0) at `rsp+0x20`, with the `ja`/`jb` bounds and an uncapped copy length.
  - `00657870` exact: the gate; the 6 + 3 + 2 dword copies; the four calls; the loop with `jbe`/`jb` re-reading dword [p+0x80]; the float 1.0 only at i = 0. The four per-step calls sit at the join `006579BF` whether or not `t` is null, as the corrected sentence says.
  - `00657A20`, `00657BC0` and `006580D0` exact: each reloads qword [p+0x58] at every use, as stated. The records are 0x4D/0x4E with the stated value fields, the 5/3 returns use `jbe`/`jae`, and the 0x42 (`001B81B0`) and 0x43 (`0065CC90`) records carry the stated fields. The stores are `02D36EE0`/`02D36F00`/`02D36E80` at [c+0x80]. The `006007B0` arguments are (+0x6C, +0x70 shr 2, 1) for the first and (+0x74, +0x78, +0x7C shr 2) for the other two.
  - `0065C330` exact: `sub 1`/`sub 1`/`cmp 1` dispatch on dword [p+0x4114]; 3, 4 and 6 `00650500` targets at the stated qword ranges; the first non-zero result returns; otherwise `00650D40(p, w, h)`.
  - `0065C4D0` and `0065C760` exact. Each slot check is: null slot, byte +8 or null `t` returns 1; on a size mismatch, `00625F00` then `0062BCB0`, then `0060DD70(t, a, b, qword [t], 0)`. `0065C760` walks j = 0..2 over +0xA0+8j and +0xB8+8j with W, H >> (2+j) (`shr` each step), then +0xD0 with W >> 1, H >> 1.

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- Each row in this family is a different function, so there is no shared shape to compare mechanically; every row was read in full instead.
- Callee behaviour is not reviewed except where the sentence states it (a float or `al` result). The skipped functions are not reviewed. The page's other text is outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
