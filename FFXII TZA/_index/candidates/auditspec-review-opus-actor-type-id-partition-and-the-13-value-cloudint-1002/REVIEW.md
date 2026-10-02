# Audit-spec review: OPUS cloudint interior citations (opus-actor-type-id-partition-and-the-13-value-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-ACTOR-TYPE-ID-PARTITION-AND-THE-13-VALUE-CL` · Package: `_index/candidates/opus-actor-type-id-partition-and-the-13-value-cloudint-1002/`
Page: `the 13-value actor-type partition page`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent; every anchor an
  instruction boundary inside its function extent with the recorded mnemonic).
- `rows.json` reconciles with the README: 7 rows applied, 33 anchors, rejected/skipped/missing all 0.
- Semantic sample: 7/7 rows vs bytes - all exact, incl. the bit-mask/budget/tail-jump body 0034E7D0.
- The README's own limits hold: body statements only, cloud draft treated as a pointer with OPUS's
  re-read as the standing claim; no semantic overreach found in the sampled rows.
