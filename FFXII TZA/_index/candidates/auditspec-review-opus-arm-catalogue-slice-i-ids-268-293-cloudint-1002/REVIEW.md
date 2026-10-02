# Audit-spec review: OPUS cloudint interior citations (opus-arm-catalogue-slice-i-ids-268-293-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-ARM-CATALOGUE-SLICE-I-IDS-268-293-CLOUDINT` · Package: `_index/candidates/opus-arm-catalogue-slice-i-ids-268-293-cloudint-1002/`
Page: `arm catalogue slice I`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent; every anchor an
  instruction boundary inside its function extent with the recorded mnemonic).
- `rows.json` reconciles with the README: 3 rows applied, 9 anchors, rejected/skipped/missing all 0.
- Semantic sample: 3/3 rows vs bytes - all exact, incl. the double-constant pick 001E04F0 (mod-10 via 0xCCCCCCCD multiply).
- The README's own limits hold: body statements only, cloud draft treated as a pointer with OPUS's
  re-read as the standing claim; no semantic overreach found in the sampled rows.
