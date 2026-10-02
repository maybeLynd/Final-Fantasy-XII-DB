# Audit-spec review: OPUS cloudint interior citations (opus-cmap-menumap-common-sublocation-director-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CMAP-MENUMAP-COMMON-SUBLOCATION-DIRECTOR-CL` · Package: `_index/candidates/opus-cmap-menumap-common-sublocation-director-cloudint-1002/`
Page: `cmap/menumap sublocation director`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent; every anchor an
  instruction boundary inside its function extent with the recorded mnemonic).
- `rows.json` reconciles with the README: 1 rows applied, 5 anchors, rejected/skipped/missing all 0.
- Semantic sample: 1/1 row vs bytes - exact; full 5-case dispatch incl. case-1 entry-copy block and both 0020E620(0) stores verified; documented correction present.
- The README's own limits hold: body statements only, cloud draft treated as a pointer with OPUS's
  re-read as the standing claim; no semantic overreach found in the sampled rows.
