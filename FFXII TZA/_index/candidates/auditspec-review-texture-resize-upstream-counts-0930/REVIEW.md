# Audit-spec review: ASTRA texture-resize-upstream-counts-0930

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/texture-resize-upstream-safe-counts/`
Board task: `ASTRA-REQ-SPEC-TEXTURE-RESIZE-UPSTREAM-COUNTS-0930`

## Verdict: ACCEPT (at the record's own scoped bounds)

## What was checked

- **Prover re-run fresh.** `python prove-texture-resize-upstream-safe-counts.py <fresh-out>` on the certified image
  (`73461D08…`) via the shared reviewed access-role adapter: `selected upstream counts 1/4/32 exclude raw/masked zero; full normal CFGs; no universal/natural-state closure`.
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
