# Audit-spec review: ASTRA texture async boundary (physical copy + pointer-key insertion)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/texture-async-boundary/`
Board task: `ASTRA-REQ-SPEC-TEXTURE-ASYNC-BOUNDARY-0930`

## Verdict: ACCEPT (at the record's own scoped bounds)

## What was checked

- **Both provers re-run fresh.** `prove-texture-async-admission-boundary.py` →
  `PRODUCER_CHECKED_ASYNC_ADMISSION_BOUNDARY_INDEPENDENT_PENDING`;
  `prove-texture-queue-tree-boundary.py` → pointer-key insertion/count/order established locally,
  async invocation and element-counter writer remain OPEN. Verdicts match the README exactly —
  including the explicit OPENs (the record claims less than its title might suggest; that is
  honest bounding, not failure).
- **Independent byte verification** (certified image `73461D08…`, capstone):
  - `62C360`: unsigned element-index guard `cmp edx,eax; jb` else `mov eax,3` — the claimed
    "returns 3 on guard failure"; null element resource `mov eax,0x15` — "returns 15h" ✓; the
    index scaling `imul r15, r9, 0x58` on the element row and the `[rbx+0x30]` `btr 0x1f` slot-flag
    clear are present in body.
  - `62EB90`: `movzx r9d, byte [rsp+0x50]` (= entryRSP+0x18 — the "wrapper loads its R9D from a
    stack byte, not the incoming R9D" claim, which is load-bearing for the no-unused-ABI
    narrowing); `imul r10, rax, 0x38; add rcx, r10` = context + 0x38·index; `call 0x199db0` ✓.
- **Negative space preserved.** The record explicitly excludes: async-callback direct invocation
  (not found in the bounded closure — correctly stated as OPEN, not absent), container+28 ≠
  element+38 wait field under distinct-allocation premise, scheduler consumption, and the
  empty-root incoming-R9 leak to the opaque allocator. The 115-state CFG event invariant is
  correctly described as an invariant proof, not 115 executions.
- **Provenance.** exe sha `73461D08…` pinned in the manifest and result JSONs; the shared
  reviewed access-role adapter is named with its sha256; the instrument is byte-redecode +
  CFG/invariant checking, no game execution — consistent with Method A STATIC_ONLY.
- **Prior work cited, not re-claimed.** OPUS's `ptexture2dd3d11` (`513baa66d`) and
  `d3d11-element-release` (`773c08600`) are cited as corroboration/premises accepted under
  AUDIT-SEM, and the record says it did not rerun those controls — correct scope honesty.

## Narrowing / notes

None required. The package asks for review "only" of its new claims and delivers a bounded
admission/insertion semantics with explicit residual OPENs.
