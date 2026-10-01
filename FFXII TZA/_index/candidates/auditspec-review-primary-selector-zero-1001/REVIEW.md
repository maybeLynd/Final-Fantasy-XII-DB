# Audit-spec review: ASTRA primary-selector-zero-1001

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/primary-selector-zero/`
Board task: `ASTRA-REQ-SPEC-PRIMARY-SELECTOR-ZERO-1001`

## Verdict: ACCEPT (at the record's own scoped bounds)

## What was checked

- **Prover re-run fresh.** `python prove-primary-selector-zero.py <fresh-out>` on the certified image
  (`73461D08…`) via the shared reviewed access-role adapter: `caller selector always zero under normal ABI; alternate edge excluded without live observation`.
- **Scope discipline.** The record's OPENs are preserved rather than smoothed:
  native effects, natural lifetime/reachability and runtime scheduling stay
  explicitly open; the proved residue is a bounded CFG/ABI fact, not a
  runtime-behaviour claim. Method A STATIC_ONLY, exe sha pinned, no game run —
  consistent with EVIDENCE-POLICY.
- **Instrument non-vacuity.** The packages retain actual CLI refusal controls
  (failed capture / mutated source) reusing the completed positives — the
  instrument is capable of failing, and its failure mode is exercised.

## Independent byte verification

- `5C5230` is `xor eax,eax; ret` — the shipping leaf genuinely returns 0
  unconditionally (verified, not a stub).
- `32FCA0` prefix: mode-gate arm `32FCEE` does `xor r14d; mov r13d,r14d`;
  the default arm runs `5C5230(5)` then `xor r14d; test eax,eax; setne r13b`
  — with eax provably 0, r13d=0 on all three classes.
- `33000C test r13d,r13d` precedes the `33000F` restore of the saved r13; only
  MOVs intervene before `je 330030` → `call 330310` (indexed), not `3306E0`.
- The claim is correctly scoped to "normal ABI": ABI-violating callees and
  reachability of `3306E0` from *other* callers are excluded by name.

## Narrowing / notes

None required.
