# Audit-spec review: SD-162 — Trial Mode award path (group-completion wake)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `sd162-trial-award-path-0930` (SWE2-ORACLE)
Board task: `ORACLE-REQ-AUDITSPEC-SD162-0930`

## Verdict: ACCEPT

## What was checked

- **Checker re-run.** `python sd162_award_path.py` at HEAD (the ~6-minute authored-script census
  over all 900 `tri_*` stage files): `FAILS 0`, matching the retained `sd162_award_path.out`.
- **Negative control is real.** K3 runs the *same* dominator classification on the 100 `us`-file
  `bossgaugeopen()` calls that precede the `waitv` — 100 sites, 0 credited. A classifier that
  credits whatever precedes a wait would have lit these; it did not. This is a positive control
  for the instrument, satisfying the absent-evidence rule.
- **K4 wake provenance.** No POPV in any `tri_*` file writes scratch1 @0x06 — the wake is the
  engine's group-completion post, cross-referenced to
  `CONTRACT-group-completion-and-respawn.md` (EE-9) rather than claimed fresh here.
- **K5/K6 census figures reproduce.** `btlAtelSetEventFlagGroup` in `tri_*` files: group 0 = 1827,
  group 1 = 3123 — group 1 is the only event group Trial Mode authors. Every one of the 900 stage
  files places ≥1 unit in group 1 (units/file ∈ [1,9]∪{18}); `tri_j05`/`tri_t05` counts match the
  retained output exactly.
- **Scope.** The record claims the award path's shape (group-1 completion posts the wake the
  `waitv` blocks on), not a timing/liveness proof — correctly bounded.

## Narrowing / notes

None required.
