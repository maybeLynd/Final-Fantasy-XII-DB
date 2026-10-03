# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PPhysics module part 3 (opus-member-n-modules-registered-before-main-phyre-pphysics-module-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-N-MODULES-REGISTERED-BEFORE-MA-E400D` · Package: `_index/candidates/opus-member-n-modules-registered-before-main-phyre-pphysics-module-3/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 29 functions, 142 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 29 rows, 142 anchors, mode `member`, family `Phyre PPhysics module`. Rejected 0, missing 0. Corrections 1 (`006A0B60`).
  - Skipped 9, each "too large for one precise sentence": `0069F150`, `0069F690`, `0069F980`, `006A0310`, `006A0680`, `006A2080`, `006A21D0`, `006A2600` and `006A4870`.
- Correction confirmed at the bytes: in `006A0B60`, `mulss` at 006A0B70 first forms `[rdx]` * `[b+0x180]`, and `mulss xmm0,xmm1` at 006A0B9F then multiplies `[b+0x170]` by that product. The row now writes `float [b+0x170] * (float [rdx+k] * float [b+0x180+k])`.
- Semantic pass: **16 of 29 rows**, spread over the package and including the corrected function, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `0069EFA0` exact. The grow test is `cmp [rcx+0x3C],edx; jb` (unsigned "not below"), and the new capacity is `lea edx,[rdx*2+1]`. The element index is re-read from `[r9]` before each group (stride `*9*4` = 0x24). The fifth argument is `[rsp+0x50]`.
  - `0069F770` exact. The three floats `[rcx+0x70..0x78]` are loaded before `00831D90(p)`. The vtable store is 00D7A838 with dword `[p+8]` = 0. The products minus `[p+0x40]` and a 0.0 fill the 16 bytes at `p+0x30`. 0xE is returned through `lea eax,[rbx+0xe]` with `rbx` = 0.
  - `0069F8E0` exact: `v` = (`[+0x70]`, `[+0x78]*0.5` (01CEBB70), `[+0x70]`, 0.0); `008353F0(p, &v)`.
  - `006A0540` and `006A0980` exact. The two bodies differ only in the shape qword (`[rcx+0x80]` / `[rcx+0x78]`). The slot `+0` early return passes through the result. The 9 return covers a null `[rdx+0x120]`. Each ends with `00832590(w, 006A2600(&t, rcx+0x20), shape)`; cookie 01F44830.
  - `006A0B60` exact (corrected row): tail `jmp 0083A030` with the re-read `b` and `edx` = 0.
  - `006A1C70` exact. The 15 goes in `[rsp+0x20]` as the fifth argument of `006A1A70`. `k` = `rsp+0x40`, and its `+0x20` pair is cleared by `movdqu`. The fifth and sixth arguments are at `[rsp+0xA0]` / `[rsp+0xA8]`.
  - `006A23F0` and `006A2540` exact. The bit edits are `and 0xFFFFFFFC`, and `and 0xFFFFFFFD` then `or 1`. The 0xF-to-0/1 byte rewrite is applied. The `+0xD8`-linked unlink comes next. Byte `+0xE8` is set to 1, or 0 (`cl` = 0 on the not-found path), on every path.
  - `006A27C0` exact. The slot `+0x78` call takes `rdx` = `[rcx+0x138]`. For the slot `+0x40` call, the vtable is read before `005C5310` and `this` is re-read after it. The release and the three zero stores follow.
  - `006A28C0`, `006A2960` and `006A2A60` exact.
  - `006A3860` exact: the bound is `jae` (unsigned "below"); `jp`-then-`je` counts unordered as not equal; the fifth argument is `[rsp+0x70]`; the 1.0 and 0 fourth lanes are stored.
  - `006A4670` exact: the membership walk, the unlink walk from the head, then the slot `+0x78` and `+0x40` calls with the re-read `[rdx+0x130]`.
  - `006A49A0` exact: the inner next is read first (`mov rbx,[rax]`); `w` falls back to 0; the slot `+0xA0` call is gated on `o` non-null, `o == w` and a non-null `[b+0x118]`; then `[g+0x10]` = 0.
- Batch-wide sentence (shared by the 8 PFramework, PHierarchy, PProfiling, PScene and PPhysics records of 6a52fe414): "154 rows … 150 stood, 4 rows were corrected in 4 clauses (three signed compares, one operand grouping)" matches the records and `verify_pphys_small_1003.json`, as checked in the PFramework record. This record holds the one grouping correction.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
