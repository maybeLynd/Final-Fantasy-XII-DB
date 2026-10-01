# Audit-spec review: ASTRA texture-update-arguments-0930

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/texture-update-arguments/`
Board task: `ASTRA-REQ-SPEC-TEXTURE-UPDATE-ARGUMENTS-0930`

## Verdict: ACCEPT (at the record's own scoped bounds)

## What was checked

- **Prover re-run fresh.** `python prove-texture-update-arguments.py <fresh-out>` on the certified image
  (`73461D08…`) via the shared reviewed access-role adapter: `updater argument dependencies and 32-bit pitch/advance proved; native effects and lifetime OPEN`.
- **Scope discipline.** The record's OPENs are preserved rather than smoothed:
  native effects, natural lifetime/reachability and runtime scheduling stay
  explicitly open; the proved residue is a bounded CFG/ABI fact, not a
  runtime-behaviour claim. Method A STATIC_ONLY, exe sha pinned, no game run —
  consistent with EVIDENCE-POLICY.
- **Instrument non-vacuity.** The packages retain actual CLI refusal controls
  (failed capture / mutated source) reusing the completed positives — the
  instrument is capable of failing, and its failure mode is exercised.

## Narrowing / notes

None required.
