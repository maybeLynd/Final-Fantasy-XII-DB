# REVIEW — EXP127 instrument-ownership + native dispatch + FP boundary

Reviewer: SWE2-AUDIT-SPEC, 2026-09-21.
Board items: ASTRA-REVIEW-EXP127-INSTRUMENT-OWNERSHIP plus routed notices
ASTRA-NOTICE-AUDITSPEC-NATIVE-DISPATCH-ADDENDUM and
ASTRA-NOTICE-AUDITSPEC-NATIVE-FP-BOUNDARY (both scoped as addenda to this
review, not separate ceremonies).

Packages reviewed:
- `_experiments/evidence/exp127-instrument-control/` (synthetic dispatch)
- `_experiments/evidence/exp127-native-dispatch-control/` (native control)

## Method

Re-ran both `check.py` scripts from the committed evidence (read-only
replay), walked their full JSON output, and inspected the decision claims
against the receipt fields rather than the prose.

## Findings

### Synthetic package — ACCEPT

`check.py` exits clean and its output confirms:

- Historical-run negative is real and bounded: in both `control` (410
  events / 204 steps) and `skeletal` (5661 events / 5454 steps) arms,
  `ownership_or_recorded_write_anomalies` is empty, every recorded context
  write touched only `EFlags` and `Dr6`, and `raw_hit_sequence_matches` is
  true. The defect path (foreign RIP or failed context read) was never
  exercised in the saved EXP127 run — the negative covers exactly what the
  receipts record and no more.
- 16 synthetic checks, 0 native calls — evidence tier honesty maintained.
- The four slots observed (`003A1C50`, `003E3C30`, `003E3C7A`, `003E3C7F`)
  are consistent with the known EXP127 recipe.

### Native dispatch control — ACCEPT

Three disposable targets, decisive arm separation:

- `original` arm: foreign event answered `0x10002` (handled),
  `foreign_context_writes = 1` (a resume write on a step the tracer did
  not cause — the demonstrated defect), `handler_delta = 0` (the target's
  vectored handler was suppressed).
- `candidate` arm: `0x80010001` (not handled), `foreign_context_writes = 0`,
  `handler_delta = 1` (delivery restored).
- `positive` arm: 21/21 owned hits, handler_total 1, PASS — the corrected
  predicate still services its own breakpoint.
- All three targets detached and exited normally; 5 malformed receipts
  rejected.

This upgrades the defect from synthetic decision-analysis to demonstrated
native delivery behavior: the handled reply provably swallows the target's
exception. It is still an instrument control, not FF12 evidence — the
README says so and nothing in the package overclaims.

### FP-boundary notice — consumed

The FIP/FXSAVE transparency counterexample stands unchanged: the corrected
predicate fixes dispatch ownership, not context fidelity. Narrowing
CONTEXT flags is explicitly not a fix. This review therefore accepts the
dispatch-ownership scope only — no universal trace-safety claim is implied
or awarded. EXP127 itself remains INVALID_POST_TRACE; its crash cause is
still unknown and no live qualification is inferred.

## Verdict

ACCEPT for both packages within their stated scopes. The bounded negative
(historical run does not exhibit the defect) is honestly drawn from the
receipts. Required next steps per the package — a separately qualified
live trace with post-detach health — remain open and are not pre-approved
by this review.
