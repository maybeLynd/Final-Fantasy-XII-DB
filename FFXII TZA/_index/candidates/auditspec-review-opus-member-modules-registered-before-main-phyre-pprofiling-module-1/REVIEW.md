# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PProfiling module (opus-member-modules-registered-before-main-phyre-pprofiling-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-A5D94` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-pprofiling-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 1 row, 5 anchors, mode `member`, family `Phyre PProfiling module`; rejected 0, skipped 0, missing 0, corrections none.
- Semantic pass: **the single row** (the request asks for at least 15; the record has 1) read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `006BA9B0` exact. `test dl,2; je` selects the arm.
    - The array arm calls `00809054(rcx, 8, n = qword [rcx-8], 005DDAF0)`. Under `test sil,1` it then calls `00809950(rcx-8, [rbx-8]*8 + 8)`, with the count re-read through `rbx`, and returns `rcx-8`.
    - The scalar arm calls `006BA860(rcx)`, then `00809950(rcx, 8)` under bit 0x1, and returns `rcx`.
- Batch-wide sentence (shared by the 8 PFramework, PHierarchy, PProfiling, PScene and PPhysics records of 6a52fe414): "154 rows … 150 stood, 4 rows were corrected in 4 clauses (three signed compares, one operand grouping)" matches the records and `verify_pphys_small_1003.json`, as checked in the PFramework record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
