# Audit-spec review: OPUS cloudint interior citations (opus-contract-bazaar-unlock-and-purchase-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-BAZAAR-UNLOCK-AND-PURCHASE-CLOUDIN` · Package: `_index/candidates/opus-contract-bazaar-unlock-and-purchase-cloudint-1002/`
Page: `bazaar unlock/purchase`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent; every anchor an
  instruction boundary inside its function extent with the recorded mnemonic).
- `rows.json` reconciles with the README: 4 rows applied, 16 anchors, rejected/skipped/missing all 0.
- Semantic sample: 4/4 rows vs bytes - all exact, incl. clamp arithmetic 002524C0 and the double 0016D6A0-clamped index use in 002535D0 (documented correction present).
- The README's own limits hold: body statements only, cloud draft treated as a pointer with OPUS's
  re-read as the standing claim; no semantic overreach found in the sampled rows.
