# SWE2-AUDIT-SPEC review: ASTRA render review-phase qualification (additive)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-RENDER-REVIEW-PHASE-QUALIFICATION-1002` · Package: `_experiments/evidence/render-review-phase-qualification/`
(publisher commit `2eb3f2fe6`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

This review covers the additive producer, control and summary only. The three parent packets were already accepted
(SPEC `fd96f1634`), and their censuses are not re-counted here.

## SWE2-AUDIT-SPEC re-derivation of the five contracts from the shipping image

1. **Pending-list publication order:**
   - Empty arm: `00427A21` writes the head at `+48810h`.
   - Non-empty arm: `00427A37` writes the old tail row's WORD `+4` and `00427A43` writes the new row's WORD `+2`.
   - Both arms write the tail at `+48814h` (`00427A47`) **before** WORD ID `[rdi]` (`00427A4D`).
2. **`006C0520`:** four MOVSS stores per call (`+0Ch`, `+0`, `+4`, `+8`), 16 bytes per call in total.
3. **Mark arm of `00429140`:**
   - `004291A9` does `and [rax+0Ch],~2` on the result of `422D50` (the call at `0042919F`) when non-NULL.
   - `004291E4` does `and [rax],~4` on the `2ED570` result.
   - `004291F3` stores the `20E620` EAX at `[rbx+0A0h]`.
4. **After `4200A0`:** `00427DB3` does `or dword [rdi+48818h],20h`, where `rdi = q[022C6F28]` (`00427C9A`), the
   pool root.
5. **Shared count/cursor:** the pending (`48810/48814`) and active endpoints share the pool root's count and cursor,
   as stated. Taken from the producer's source map; the root load was confirmed.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` re-run: exit 0, output **byte-identical** to `result-01.json`.
- `control.py` re-run: exit 0. The three actual CLI refusals (failed parent producer, missing parent result,
  missing returned review) are identical, each with its result absent.

Callback and helper effects, valid pointers, no-alias, normal ABI, reachability, lifetime and scheduling stay
premises.
