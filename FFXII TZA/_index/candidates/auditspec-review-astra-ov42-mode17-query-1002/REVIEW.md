# SWE2-AUDIT-SPEC review: ASTRA OV-42 mode-17 query boundaries

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV42-MODE17-QUERY-1002` · Packages: `_experiments/evidence/ov42-resource-mutator-mode17/` and
`_experiments/evidence/ov42-resource-eligibility-domain/` (publisher commit `7b4e2b92c`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The governing artifacts are `qualified-result-02` (`0051dcc8`) and `result-02`.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`0030B770` (`BattleTarget_ComputeGlobalEligibilityMask`, 77h bytes, no calls):**
  - `mov dword [rbp],0`, after which only WORD stores happen: bits 1, 2, 4, 8 and 10h from `02089340` and
    `022C2158`.
  - The DWORD return therefore always has upper WORD = 0 and a low mask of 0..31.
  - So the earlier "first global upper non-zero" CFG partition is a control or intervention, not a normal native
    case.
- **`00300CE0` (`BattleStats_ModifyPrimaryResource`):**
  - Initial bit 0 of r8d bypasses both queries.
  - Otherwise it calls `30B770` and then `30B7F0(owner, edx=0)`, and either non-zero low WORD jumps to the veto
    arm (`00300D57..00300D63`).
  - The own WORD `+4Ch` arithmetic follows.
  - The exact retained caller passes EDX = 0, which excludes the low-bit-1 arm.
- **`001D50D0`:**
  - A non-null root `01F81428` returns with no call and no store.
  - A NULL root allocates `10E8h` through `210EC0`, constructs through `1CCB20` when the allocation is non-null,
    and publishes RAX.
  - This agrees with existing canonical knowledge; it is not a new discovery.

## SWE2-AUDIT-SPEC reproduction (disposable copies, repository-root cwd)

- `ov42-resource-mutator-mode17` `prove.py` (proof-02) re-run: output **byte-identical** to `result-02.json`.
- `ov42-resource-eligibility-domain` `prove.py` (proof-02) re-run: output **byte-identical** to `result-02.json`.
- `qualify-singleton.py` (qualification-02) re-run: output **byte-identical** to `qualified-result-02.json`.
- `control.py` re-run into a fresh `controls-01`: exit 0, stdout identical ("Three exact upstream/artifact failures
  refused without downstream result").

Owner upper bits 0..3 are bounded only under the stated initialized non-NULL root, no root `C20` interference and
private-frame ABI premises. The constructor's `C20=0` store is intermediate. There is no final-default, all-play or
lifetime proof.
