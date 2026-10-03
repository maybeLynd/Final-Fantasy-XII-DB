# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PHierarchy module (opus-member-modules-registered-before-main-phyre-phierarchy-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-C3142` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phierarchy-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 11 functions, 45 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 11 rows, 45 anchors, mode `member`, family `Phyre PHierarchy module`. Rejected 0, missing 0, corrections none. Skipped 5, each "too large for one precise sentence": `00877EE0`, `008780F0`, `008786F0`, `00878980` and `0087A8C0`.
- Semantic pass: **all 11 rows** (the request asks for at least 15; the record has 11) read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved:
  - `00877EA0` exact: the order of `+0x18` = 0 then the `+0x18` to `+8` copy holds; the qword store of 1 at `+0x2C` sets dword `+0x2C` = 1 and dword `+0x30` = 0.
  - `00878070` exact: `00809054(s+8, 0x50, 8, 00878070)` (the function's own address as the per-element callback, `lea r8d,[rdx-0x48]`), then `00680200(qword [02EBA2A0], s)` with the qword loaded before the first call. Both arms zero `+0x38` and `+0x40`.
  - `00879130` exact: guard 02EB9D48; `0067FFB0(02EB9D20, 0x78, 0x64, 8, [rsp+0x20] = 00D4B590 "PCheckVisibleBoundsJob")`; exit routine 008BDDA0.
  - `008791D0` exact: `0067FFB0(02EB9D50, 0x28, 0x64, 8, 01CD9898 "PMergeOctreeNodesJob")`; exit routine 008BDDB0.
  - `00879270` and `008792A0` exact: each getter is called twice, once per call, and the second call feeds the tail `jmp 00680210`.
  - `008792D0` exact. `c_k = (a[k] + (a[k] + a[0x18+k])) * 0.5` with 01CEBB70 = 0.5. The three transformed components sum as `(c1*m[0/4/8] + c0*m[0xC/0x1C/0x2C]) + c2*m[0x10/0x14/0x18] + m[0x20/0x24/0x28]`, in the row's order.
  - `0087AE00` exact: `0067FFB0(p, 0x288, 0xA, 8, 01CD9320 "POctreeChildren")`; `p` (or 0) is stored to 02EBA2A0.
  - `0087AE80` exact.
  - `008BDDA0` and `008BDDB0` exact.
- Batch-wide sentence (shared by the 8 PFramework, PHierarchy, PProfiling, PScene and PPhysics records of 6a52fe414): "154 rows … 150 stood, 4 rows were corrected in 4 clauses (three signed compares, one operand grouping)" matches the records and `verify_pphys_small_1003.json`, as checked in the PFramework record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
