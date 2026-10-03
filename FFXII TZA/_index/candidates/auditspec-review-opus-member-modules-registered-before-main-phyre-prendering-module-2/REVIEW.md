# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PRendering module part 2 (opus-member-modules-registered-before-main-phyre-prendering-module-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-D5EF8` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-prendering-module-2/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 30 functions, 147 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 30 rows, 147 anchors, mode `member`, family `Phyre PRendering module`. Rejected 0, missing 0, corrections none. Skipped 6, each "too large for one precise sentence": `005E3F70`, `005E45B0`, `005E4AA0`, `005E7070`, `005E7E60` and `005E81E0`.
- Semantic pass: **15 of 30 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` field names resolved:
  - `005E2CE0` exact: `lea [rdi+rdi*2]; shl 2` (0xC), align 4; words `+0`/`+2` = `si` = 0, dword `+4` = 1, `+8` = 0xFFFFFFFF.
  - `005E2EA0` exact.
  - `005E2FB0` exact: word `+0`, dwords `+4`/`+8`, byte `+0xC` per 0x10 element, align 4.
  - `005E31B0` exact: `005D8230(p, rdx, r8d)` then the tail loop zeroes qwords `+0`/`+8` of `ecx - r8d` elements.
  - `005E34B0` exact: `lea [rdi+rdi*4]; shl 4` (0x50); `005FD1D0(p + r8d*0x50, ecx - r8d)`.
  - `005E3600` exact.
  - `005E3750` exact: tail elements get word `+0` = 0, qword `[elem+4]` = 0 (`[rax-4]` with `rax` = elem+8) and byte `+0xC` = 0x34.
  - `005E3960` exact: six qword stores `elem+0 .. elem+0x28`.
  - `005E3B70` exact: `00632960` stack args `[rsp+0x20]` = 0, `+0x28` = 0x10, `+0x30` = 0, `+0x38` = 0; name 00D27730 = "m_size"; guard 02CE2678; exit routine 008ADAC0.
  - `005E3EB0` exact: "m_dynamicMesh" (00D49948), type 02D3A140, n 8, f 0xA.
  - `005E6400` exact: three guards (02CE41E8 / 02CE4248 / 02CE42A8). The names are "m_destination" (n 0, f 2, type 02E404B0), "m_source" (n 8, f 2, type 02CB6E80) and "m_sourceMatrixIndex" (n 0x10, f 0, type `00630180()`).
  - `005E68B0` exact: all five names, records, types, and n/f pairs, as `[rsp+0x20]`/`[rsp+0x28]`.
  - `005E6C30` exact: the unguarded `005EFB10(qword 01F2DE10)` (01F2DE10 holds 00D4A5E0 "PSharray<PUInt32>"); `00632A10` args (0, 0, 4, 4); qword 02CE44C0 = 00D4A600; `or [02CE44E8],8` is the jump target of both guard exits, so it is unguarded.
  - `005E84D0` exact: "m_structuredBuffer" (0x10, 0x12, type 02CBB600) and "m_dataBlock" (0x18, 0x12, type 02D39E40); `or [02CBA5FC],0x20` before the guards.
  - `005E86D0` exact: "m_indexDataBlock" (0x10, 0x12, type 02D3A340).
- Signed versus unsigned: no range compare in the sample; the guards' `jle` is not worded as a direction (the rows say "under its thread-safe guard").
- Batch-wide sentence (shared by the 7 PRendering records of 83b4566ab): "203 rows … 199 stood, 4 rows were corrected in 6 clauses (signed compares)" matches the records and `verify_prendering_1003.json`, as checked in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
