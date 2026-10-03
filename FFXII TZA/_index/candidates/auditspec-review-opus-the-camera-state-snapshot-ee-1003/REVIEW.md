# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-camera-state-snapshot-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-CAMERA-STATE-SNAPSHOT-EE-1003-A1E49` · Package: `_index/candidates/opus-the-camera-state-snapshot-ee-1003/` · Page: `22-Middleware-PhyreEngine/the-camera-state-snapshot.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. Output: `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the page and the package was clean afterwards (HEAD b5028e7e9).
- `rows.json`: 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** was read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...).
  - `00216720` (2200 B; `.pdata` 00216720-00216FB8 is the same extent), exact.
    - There is no `call` in the body.
    - The sixteen outputs are `[rsp+4]`, `[rsp]`, `[rsp+8]`, `[rsp+0xC]`, `[rsp+0x10]`, `[rsp+0x14]`, `[rsp+0x30]`, `[rsp+0x34]`, `[rsp+0x18]`, `[rsp+0x20]`, `[rsp+0x1C]`, `[rsp+0x24]`, `[rsp+0x28]`, `[rsp+0x2C]`, `[rsp+0x38]` and `xmm6`. Each is a sum of three triple products minus a sum of three.
    - det = `[rdx+0x10]`·`[rsp]` + `[rdx]`·`[rsp+4]` + `[rdx+0x20]`·`[rsp+8]` + `[rdx+0x30]`·`[rsp+0xC]` (`00216E38`..`00216E8F`). These are the floats `+0`/`+0x10`/`+0x20`/`+0x30` times the cofactors that land at `rcx+0..0xC`.
    - `ucomiss det,0` (`00216E93`). `jp` → division, then `je` → factor 0. `xmm1`=0 from `xorps`.
    - 1.0 is `01CEBBA8` (`.rdata` 3F800000), and `divss` is at `00216EA2`.
    - The sixteen `movss` stores to `rcx..rcx+0x3C` run `00216EF0`..`00216FAA`, and the function returns.
    - Control: a unicorn emulation of the body (reviewer scratch, not committed) on 200 random 4×4 matrices matched `numpy.linalg.inv`. The worst relative error was 5.7e-6, in the same layout (the transposed layout gives an error of 9.6). Two singular inputs (equal rows) gave all-zero outputs, which confirms the "cofactor", "determinant" and "factor 0" clauses.
- Observation (no narrowing): in IEEE terms, "(all outputs zero)" means each cofactor ×0.0. A cofactor of ±inf would give NaN, but no finite input reaches that while the determinant compares exactly equal to 0. The emulated singular cases gave ±0.0.

Limits: these are body statements read from static evidence plus one emulation control. The draft and OPUS's re-read are not independent review; this record is.
