# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PRendering module part 7 (opus-member-modules-registered-before-main-phyre-prendering-module-7)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-2C4BE` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-prendering-module-7/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 23 functions, 90 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 23 rows, 90 anchors, mode `member`, family `Phyre PRendering module`. Rejected 0, missing 0, corrections none. Skipped 1, "too large for one precise sentence": `006BED60` (3248 B).
- Semantic pass: **15 of 23 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings and constants resolved:
  - `006BA590` exact: `and [rdi],0x80000000` then `or [rdi],min`, which keeps bit 31. The release loop runs only when bit 31 is clear and new < old (`jae` skip). The final `00584730(qword [rcx+8])` runs when the whole dword is 0 (no null test on that call), followed by the zero store.
  - `006BE410` exact: `lea rdx,[rax+rax*2]` and `[rax+rdx*8]` (stride 0x18, `edx` zero-extended); tail `jmp 006D5120` with (o, r8, r9).
  - `006BEAC0` exact: `006B6820(02E58EB0, 00D82F30 "PLightType", 0x20, 8, [rsp+0x20] 00876870, [rsp+0x28] 006BFCF0)`; store 00D82F48; exit routine 008B6140.
  - `006BFCF0` exact.
  - `006C0540` exact: 01CEBB70 = 0.5. `comiss xmm2,0` comes before the `addss` and `jbe` uses its flags, so unordered takes the "not above" arm.
  - `006C05C0`, `006C05D0`, `006C05F0` and `006C0600` exact.
  - `006C0EB0` exact. `lea rax,01F2EDC8` stores the address itself to qword `+8`. 0x3727C5AC goes to dword `+0x50`. The four byte stores and the `or 0x40` each re-read dword `[b+0x1C]` and test bit 7.
  - `006C1060` exact: `imul 0xe8`, `006C0BA0` fill, free gated `!= p`, bit 31 clear, non-null.
  - `006C15D0` exact. All four guard dwords and exit routines match. `m_splits` takes (0x10, 0, 3, 8) and stores 00D83C00. `or [02E59FB8],0x10` is the target of both guard exits. `m_shadowCasterType` is (8, 0x12), `m_zbias` (0x50, 0x10) and `m_light` (0, 0x12) with type 02E58DB0.
  - `006C1810` exact: "m_farPlane", `006301F0()`, n 0xC8, f 0x10; exit routine 008B68D0.
  - `006C2410` exact.
  - `006D5120` exact. All header stores match. `s` = `(2n + 0x4F) AND 0xFFFFFFF0`. The per-entry callbacks take (`h`+`s`+0x10, r8) for slot `+0x38` and add `round16(r) + 0x10`; slot `+0x40` takes (`h`+`s`, r8) and adds `round16(r)`. The 0xFFFF fill starts at `h + 0x40 + 2n` (`lea rcx,[rdi+(n+0x20)*2]`) and stops at the address's 16-byte boundary (`test cl,0xf`). Then come word `[h+0x1E]` = `s`, `rep stosq` of `m` qwords at `h`+`s`, and return 0.
- Advisory, not a defect: `006BA590`'s `min` is unsigned (`cmovb`). With the old count masked to 31 bits, it differs from a signed minimum only when `edx` has bit 31 set. OPUS may add "(unsigned)".
- Batch-wide sentence (shared by the 7 PRendering records of 83b4566ab): "203 rows … 199 stood, 4 rows were corrected in 6 clauses (signed compares)" matches the records and `verify_prendering_1003.json`, as checked in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
