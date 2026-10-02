# SWE2-AUDIT-SPEC review - DD residue batch 21-1002: PARTIAL status-line currency

Task: `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B21-1002`. Package: `_index/candidates/swe2contract-ddres-b21-1002/`,
page diffs at `85718f321`.

## Verdict: ACCEPT-WITH-NARROWING

Evidence class: NATIVE/STATIC (committed-diff verification + register reconciliation; no native bodies
involved). Reviewed the committed package as routed; no claims weakened.

## Independent verification

- All nine pages carry **1/1 numstat** at `85718f321` — same-line status rewrites only, verified on the
  commit itself (the package's own claim "the diff is status lines only"). Sampled diffs show exactly
  that: a bare `status: PARTIAL` rewritten to name the live row(s) + batch-21 stamp; efx-and-efb gains
  `still open: SD-194` appended inside the same line. No status word moved (all stay PARTIAL).
- Every id named on a status line reconciles with `documented_rule.out`'s per-page `live=` list:
  OV-8; OV-10; OV-16; OV-19+OV-21; OV-21+OV-33+OV-42; OV-42 (x2); OV-29; SD-194 — and each register row
  is genuinely open at HEAD (OV-16/21/29/SD-194 OPEN; OV-8/10/19/33/42 PARTLY ANSWERED with RT
  remainders carried by FABLE-REQ-ASTRA-RT-REMAINDERS-0929 / AQ-ARENA / OV-21-BANK-REACHABILITY;
  EO-3 SUPERSEDED, cited as pointer-only on resource-request-queue which took no status edit — correct,
  since its line was already current).
- `documented_rule.out` re-run receipt: PARTIAL 9/9, FAILS 0 — the registered live rows remain open,
  which is the truthful state.
- The two non-PARTIAL census pages (effect-mesh-records-kind-54 READY, authored-data-table-registry
  READY-WITH-POINTER) and the skipped dirty page take no edits — consistent with the commit's file set.

## Narrowing: stale control

- `b21_checks.py` at HEAD reports **FAILS 9 — all Z4**: it diffs the *working tree* (`git diff
  --numstat`) expecting the uncommitted 1/1 edits, but the batch is committed at `85718f321`, so the
  working diff is empty for all nine pages. Same stale-control class as DDRES-B7-R1 and B20-Z1. Z1-Z3
  pass. Z4's intent is independently verified at-commit (numstat 1/1 per page, status-line diffs only).
  Routed `AUDITSPEC-REQ-CONTRACT-DDRES-B21-Z4-CONTROL-1002` for the repair (diff the pinned commit, or
  accept the committed state), matching the B7-R1/B20-Z1 repairs already in flight.
