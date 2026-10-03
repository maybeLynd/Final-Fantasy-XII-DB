# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PRendering module part 6 (opus-member-modules-registered-before-main-phyre-prendering-module-6)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-EF586` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-prendering-module-6/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 20 functions, 94 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 20 rows, 94 anchors, mode `member`, family `Phyre PRendering module`. Rejected 0, missing 0. Skipped 2, both "too large for one precise sentence": `006B7A00` and `006B9630`. Corrections 6, in 4 functions, all signed compares: `006B6E50` x1, `006B73E0` x3, `006B7E00` x1 and `006B7F00` x1.
- Corrections, all 6 confirmed at the bytes and present in the rows:
  - `006B6E50`: `cmp rax,0x28; jle` (006B6E71), now "greater than 0x28 (signed)".
  - `006B73E0`: `jl` at 006B73FE, now "less than 2 (signed)". `jge`/`jl` at 006B746E/006B74A7 on `h` against `q`, now "less than `q` (signed)". `jge`/`jl` at 006B74DF/006B7519 on `i` against `h`, now "greater than `i` (signed)".
  - `006B7E00`: `jge`/`jl` at 006B7E50/006B7E97, now "less than `q` (signed)".
  - `006B7F00`: `jge`/`jl` at 006B7F31/006B7F87 on top against `h`, now "greater than `r8` (signed)".
- Semantic pass: **15 of 20 rows**, spread over the package and including all four corrected functions, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings and imports resolved:
  - `0067AE30` exact: strlen+1, `0067B100(rcx, n+0x80)`, count store, `00861EBA` only when qword `[rcx+8]` (re-read after the call) is non-null.
  - `0067AEA0` exact: `0019C5D0(rsp+0x20, 0x32, 00D6CF10 "%u", edx)`, `0067AF00(rcx, buf)`, cookie 01F44830 / `00808C40`.
  - `006B6E50` exact (corrected row): `n` by `sar 4`, `s` = (`n` + 1) / 8 by `cqo; and edx,7; add; sar 3` (signed division). The three median-of-three calls and the tail call take the stated triples, with `r9` (saved in `r15`) as the fourth argument each time; the short arm tail-jumps with the original registers.
  - `006B70C0` exact: `memmove` is the import at IAT slot `008C2A40` and moves [first, element) to first+16. The inner loop has no lower-bound test; it relies on the failed first-element compare, as the row's wording implies.
  - `006B73E0` exact (corrected row): the outer loop runs from `n`/2 - 1 down to 0 (`dec r14`, `test r14; jg`). The sift-down, the odd/even fix-up (`test r13b,1`) and the sift-up all use signed compares, and the final store goes to `h`.
  - `006B7E00` exact (corrected row): the fifth argument is read at `[rsp+0x80]` after 5 pushes and `sub 0x30`, and is written back before the tail `jmp 006B7F00`; top = the incoming `rdx` (saved at `[rsp+0x68]`).
  - `006B7F00` exact (corrected row): `f` is the fifth argument at `[rsp+0x60]`; the loop runs while top < `h` (signed) and `f(base+16p, r9)` returns non-zero; the final 16-byte copy is from `r9`.
  - `006B8100` exact: `006B7E00(rcx, 0, (l - rcx)/16, &t, [rsp+0x20] = r8)`; the loop condition recomputes the count after dropping `l`.
  - `006B8930` exact: `setb` (unsigned, stated).
  - `006B8940` exact.
  - `006B89C0` exact. `_stricmp` is the import at IAT slot `008C3000`. The string at 00D4E5C0 begins "PNam". Both free lists refill through `00680150` with the dwords at 02E524A4 / 02E524CC, then pop with `head = [entry]`. `006B8590(e, 0, s)` is called only when both are non-null, otherwise `e` is returned.
  - `006B8DE0` exact: the 4-bit count, then two 5-bit fields per entry (first through `r14+rdi` = `rcx`+4j, second to `rdx`+4j), each field split across dwords by the `cmovb` width clamp; the advance is `((bits + 0x1F) >> 5) << 2`.
  - `006B94C0` and `006B9A20` exact (identical bodies, identical rows). The string pieces resolve to 00D81068 = "-D" and 01CEBB4C = "=". The copy length is the string object's dword `+0x10`, which holds the length including the terminator (`0067AE30`'s layout). When that count is 0 the buffer is 0 and `c` stays 0.
  - `006BA3A0` exact: the entry loop is `cmp ebx,r15d; jb` (unsigned, worded as "each `j` below `n`"); both 0xD returns; the `006B8940` free omits a null test, and the per-entry free includes one.
- Batch-wide sentence (shared by the 7 PRendering records of 83b4566ab): "203 rows … 199 stood, 4 rows were corrected in 6 clauses (signed compares)" matches the records. This record holds all 6 entries, in 4 functions, all signed compares, and `verify_prendering_1003.json` agrees (199 OK, 6 FIX in 4 functions).
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
