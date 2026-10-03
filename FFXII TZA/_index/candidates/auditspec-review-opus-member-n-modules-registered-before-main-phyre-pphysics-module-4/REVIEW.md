# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PPhysics module part 4 (opus-member-n-modules-registered-before-main-phyre-pphysics-module-4)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-N-MODULES-REGISTERED-BEFORE-MA-6E8A8` · Package: `_index/candidates/opus-member-n-modules-registered-before-main-phyre-pphysics-module-4/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 9 functions, 41 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 9 rows, 41 anchors, mode `member`, family `Phyre PPhysics module`. Rejected 0, missing 0, corrections none. Skipped 3, each "too large for one precise sentence": `006A4E30`, `006A5C00` and `006A6180`.
- Semantic pass: **all 9 rows** (the request asks for at least 15; the record has 9) read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with the byte table and jump table of `006BA630` decoded:
  - `006A5450` exact: `lea [rbx+rbx*8]; shl 2` (0x24), align 4; free gated `!= p`, bit 31 clear, non-null.
  - `006A54E0` exact: `00693BC0(edx)`; `lea eax,[rsi+0xd]`.
  - `006A5770` and `006A5790` exact.
  - `006A5B10` exact. `[rcx+0x60]` gets slot `+0` (it, 0), then `00584730` on the re-read qword, then zero. `+0x68` and `+0x70` each get slot `+0` (obj, 1) when non-null, and both are zeroed either way. The two (count, pointer) pairs follow; it returns 0.
  - `006A5BE0` exact: `movaps xmm2,xmm3`, the three stores, tail `jmp 006A5C00`.
  - `006A65A0` exact. Nothing happens when `dl == r8b`. The non-zero arm calls slot `+0x130` with (`w`, `b`, `1 << cl` computed as a 16-bit `shl ax,cl`, word `[t + 0x78 + 2*byte]`), then `0083A030([rcx+0x118], 0)`. The zero arm calls slot `+0xA0` with (`w`, `b`). Byte `+0xE9` = `dl` is stored on every path of the differing case, including the null-link exits.
  - `006BA630` exact: all 0x33 entries of the byte table at 006BA6EC were checked against the jump table at 006BA6B8. 4..0x2F give the value AND 0xFFFFFFFC, 0x32 gives 0x33, and 0..3, 0x30 and 0x31 reach 006BA6B4 (`edx` = 0). Values above 0x32 take `ja` (unsigned) to 0.
  - `008B3BE0` exact: `0016D6A0(02E4B038)`; the pair (02E4B020, 02E4B028) is freed under the bit-31 and null tests and zeroed; the tail is `jmp 0016D6A0` with 02E4AFF0.
- Batch-wide sentence (shared by the 8 PFramework, PHierarchy, PProfiling, PScene and PPhysics records of 6a52fe414): "154 rows … 150 stood, 4 rows were corrected in 4 clauses (three signed compares, one operand grouping)" matches the records and `verify_pphys_small_1003.json`, as checked in the PFramework record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
