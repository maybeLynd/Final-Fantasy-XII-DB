# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PRendering module part 3 (opus-member-modules-registered-before-main-phyre-prendering-module-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-E53B3` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-prendering-module-3/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 29 functions, 137 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 29 rows, 137 anchors, mode `member`, family `Phyre PRendering module`. Rejected 0, missing 0, corrections none. Skipped 9, each "too large for one precise sentence": `005E9680`, `005E9970`, `005EA7A0`, `005EAF40`, `005EB7C0`, `005EBE40`, `005EC180`, `005EC4C0` and `005EC800`.
- Semantic pass: **15 of 29 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` field names resolved. For every registration row the record, type and name registers (`rcx`/`rdx`/`r8`/`r9`) and the four stack arguments `[rsp+0x20/0x28/0x30/0x38]` were matched:
  - `005E8790` exact: "m_offset", `006300A0()`, n 0, f 0.
  - `005E8900` exact: "m_type", `0062FFC0()`, n 2, f 0.
  - `005E8B60` exact: `or [02CBA6FC],0x20` before the guards; "m_rwStructuredBuffer" / "m_rwDataBlock" / "m_rwIndirectArgsBuffer" with n 0x10 / 0x18 / 0x20, f 0x12, types 02CBB600 / 02D39E40 / 02CB6980.
  - `005E8E50` exact: "m_texture", 02CBB900, 0x10, 0x12.
  - `005E8FD0` exact: "m_unusedPointer", 02CBB700, 0x10, 0x12.
  - `005E91D0` exact: "m_texture" in record 02CE8CF0.
  - `005E9350` exact: "m_parameterType" (`00630180()`, 0, 0x10), "m_samplerState" (02CB78A0, 8, 0x12), "m_textureBufferIndex" (`00630180()`, 4, 0x10).
  - `005E95C0` exact: "m_constantBuffer", 02CB6480.
  - `005EA220` exact: unguarded `005EE7F0(qword 01F2DE60)` (01F2DE60 holds the name "PArray<PShaderParameterCaptureBufferLocationTypeConstantBuffer>"); `00632A10(…, 0x10, 0, 3, 4)`; qword 02CE88B0 = 00D4B008; `or [02CE88D8],0x10` is the target of both guard exits.
  - `005EA3D0` exact: the two unguarded getter calls (01F2DE78 / 01F2DE80), `00632A10` args (0, 0, 3, 8) and (0x10, 0, 3, 8), stores 00D4ADA0 / 00D49EA0, and the two unguarded `or 0x10`.
  - `005EAAA0` exact: "m_elementCount" / "m_elementSize" / "m_flags", n 0 / 4 / 8, f 0x10.
  - `005EAD90` exact: "m_width" / "m_height" / "m_depth", n 0x28 / 0x2C / 0x30.
  - `005F0220` exact: `+8` before `+0`, each under the null and bit-0 tests; the final `00584730(rcx)` also runs when `edx` = 0.
  - `005F0410` exact.
  - `005F0720` exact. The byte store; the record count, base and stride (`[rcx+0x70]`, `[rcx+0x58]`, `[[rcx+0x50]+0x38]`). The 7 return is `lea eax,[rdi+7]` with `rdi` = 0. The fill loop re-reads 02CB635C each pass (`cmp eax,edx; jb`). The entry store is `mov [rax+rcx*8],r9` under `cmp ecx,-1; je`. The `n` = 0 arm frees under the null and bit-31 tests and stores 0 / 0x80000000.
- Signed versus unsigned: the only range compares in the sample are `jb` (unsigned) in `005F0720`'s fill loop, which the row words as a count ("the next `n` qwords"), and the zero tests on masked counts.
- Batch-wide sentence (shared by the 7 PRendering records of 83b4566ab): "203 rows … 199 stood, 4 rows were corrected in 6 clauses (signed compares)" matches the records and `verify_prendering_1003.json`, as checked in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
