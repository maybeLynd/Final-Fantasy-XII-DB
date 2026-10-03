# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-dules-registered-before-main-phyre-pphysics-module-1-r9a)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-DULES-REGISTERED-BEFORE-MAIN-P-EFF57` · Package: `_index/candidates/opus-member-dules-registered-before-main-phyre-pphysics-module-1-r9a/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 7 functions, 35 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 7 rows, 35 anchors, mode `member`; rejected 0, missing 0, skipped 13 (README agrees); 1 correction (`00691C00`, branch scope).
- Every row read in full against its sentence, clause by clause (bodies in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/full_<pkg>.txt`, rip targets resolved with the value at each target):
  - `0063CD20` exact. `f` is read before the first slot +8 call. `k` - 3 <= 1 (`setbe`) is stored at byte [o+0x18]. The k = 2/3/4 path calls slots +0x20, +0x38 and +0x40, with `r8` = b and `r9d` = a. The other path gives the early return on a non-null slot +8 of qword [d+0x30] with bit 1 of `f` clear, and `m` from slot +0x20 only when k = 1. `e`, `s` and `u` follow, and the 8-vs-s choice is bit 1 of g OR (NOT bit 6 of g AND u-kind 2). The memcpy has `rcx` = [o+0x10]+e and `rdx` = [o+8]+e.
  - `00691C00` exact; the README correction (the slot calls happen whether or not `g` is null) is in the sentence and matches `je 00691CDF`. Both unlinks and the three zeroings match, and the tail is `jmp 00691D40`.
  - `0069F690` exact. Every field of `s` (at rbp-0x41) maps to the stated offset: the 1.0 floats come from `0x3F800000` qwords and dwords, +0x60 = 4 and +0x70 = `xmm1`. `d` is at entry +0x10 (rdx home) and the fifth dword at entry +0x28. `rcx`/`r8`/`r9` pass through untouched. `cmove` gives d or -1. The vtables `00D79858` and `00D79830` are stored before and after the call.
  - `0069F980` exact. `s` is the pair at `[rsp+0x28]`/`[rsp+0x30]`; `n` is read after `00671600`. r = 9 and both r = 0xE paths skip the +0x68 copy. The rebuild path destroys the just-stored object through its slot +0 before building the replacement. qword [t+0x10] is read before `00834890`, `008343A0(&t)` comes before r = 0xE, and the `00584730` release is gated on bit 31 and a non-null qword.
  - `006A2080` and `006A21D0` exact. `s` sits at rbp-0x61 / rbp-0x69, with `P` 16 bytes below. Every field offset matches the sentence, and so do the arguments q, A and B (entry +0x28/+0x30/+0x38) and k (entry +0x40, dword, `006A21D0` only). The `006A1DD0` call gets `r8` = the entry `r9`, the stores land at s+0x80/+0x88, and the else path stores 0 and `006372A0()`.
  - `006A4870` exact: the list search from qword [w+0x48] and the unlink; the node walk with `rdi` = qword [n] read first; the +0xD8 unlink from qword [w+0x58]; the gated slot +0xA0 call. qword [n+0xC8] is zeroed on both arms, then qword [b+0x10].

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- Each row in this family is a different function, so there is no shared shape to compare mechanically; every row was read in full instead.
- Callee behaviour is not reviewed except where the sentence states it (a float or `al` result). The skipped functions are not reviewed. The page's other text is outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
