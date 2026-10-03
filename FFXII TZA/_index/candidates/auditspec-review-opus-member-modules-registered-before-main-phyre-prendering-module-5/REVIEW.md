# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PRendering module part 5 (opus-member-modules-registered-before-main-phyre-prendering-module-5)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-DA0CA` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-prendering-module-5/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 32 functions, 150 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 32 rows, 150 anchors, mode `member`, family `Phyre PRendering module`. Rejected 0, missing 0, corrections none. Skipped 4, each "too large for one precise sentence": `00622010`, `006221E0`, `0062D0D0` and `0062D740`.
- Semantic pass: **15 of 32 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved:
  - `0060F350` exact: the slot `+8` call takes rcx = 02CB6C80. The three-way test is `cmp rsi,rdi; jne`, then `cmp ebx,1; jne`, then `test rax; je`. The `00639850` arm takes (r, rcx+8, 1); the other arm is `006A5950(rcx, rdx, r8d)`. Both return 0.
  - `0060F7D0` and `0060F810` exact.
  - `00613690` exact: the bit-0 strip (`sub rdi,(byte&1)`), strlen+1, `0017D260(len, 2)`, `00861EBA`, and the 0 store on a null string or a failed allocation; the source advances only inside the non-null-destination branch.
  - `00615CF0` exact: each qword and dword offset listed matches a store (`+0x30..+0x68` through `rax` = 0).
  - `00615DD0` exact: eight groups at 0x1C0, 0x1E0, …, 0x2A0, each with qword `+0`, dword `+8`, qword `+0xC` and qword `+0x18`.
  - `006164B0` exact: order `+0x18`, `+0x10`, `+8`, each zeroed only when non-null; tail `jmp 0016D6A0`.
  - `00616880` exact: the `+8` dword test (`test eax,eax; je`) gates both the free and the zeroing; tail `jmp 00616B40`.
  - `00616B40` exact.
  - `00616D80` exact: `shl rcx,5` (0x20), `00613690` fill, `00619070` free.
  - `00618870` exact: the null return passes through `rax` = 0 from `0063BC00`; `al` = 1 on both remaining arms.
  - `00627C60` exact: `00617720` and `00619070`; early exit on the full-dword compare; `lea eax,[rsi+0xd]`.
  - `0062CC80` exact: `006B6820(02CF7A70, 00D56200 "PTextureFormatBase", 0x20, 8, [rsp+0x20] 006CD4C0, [rsp+0x28] 0062D660)`; store 00D56220; exit routine 008AF080.
  - `0062D660` exact: byte-compare loop to the terminator, then `cmovne eax,ebx` gives 0 for a found entry, else 0x13; the entry or 0 goes to `[rcx]`.
  - `0063DE00` exact.
- Advisory, not a defect: `00627C60`'s `min` is unsigned (`cmovb`); see the same note in the part 4 record. OPUS may add "(unsigned)".
- Batch-wide sentence (shared by the 7 PRendering records of 83b4566ab): "203 rows … 199 stood, 4 rows were corrected in 6 clauses (signed compares)" matches the records and `verify_prendering_1003.json`, as checked in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
