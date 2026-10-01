# Consumer-check record: condition T reads Tools/work citations; five rows re-pointed (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/_index/candidates/status-currency-ruling-fable/documented_rule.py`
affected: `Database/FFXII TZA/_index/candidates/status-currency-ruling-fable/t-tracked-evidence-0929.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

## What changed

This applies `AUDITSEM-REQ-FABLE-DDRULE-T-TOOLSWORK-0930`, both halves of
[the review's](../auditsem-review-ddrule-t-0930/REVIEW.md) §4 repair.

- **T reads `Tools/work` citations.** `EVID` now also matches `(Database/)Tools/work/...`, and such a path always counts
  as untracked, because that tree is gitignored. A new self-test case, "T Tools/work evidence", expects
  EVIDENCE-UNTRACKED. The self-test passes 33 of 33.
- **The note's scope sentence is narrowed (N1)**, and "today's register" gains "in those forms".
- **Five closed rows are re-pointed** to tracked records:
  - EC-2 and GG-3 → `auditsem-review-gg3-event-slot-0925/REVIEW.md` (SWE2-AUDIT-SEM's tracked copy).
  - SN-1 → `auditsem-sign-sn1-x-oeb-0929/SIGN.md`.
  - CD-2 → a new verbatim tracked copy, `auditspec-review-absence-rows-0925/REVIEW.md`.
  - BK-7 → a new verbatim tracked copy, `bk7-pending-batch-0903/README.md`.
  - Each new copy carries a provenance header and nothing else is edited.

## Consumers

- consumer: `_index/OPEN-QUESTIONS.md` rows CD-2, EC-2, GG-3, SN-1, BK-7: revised-here (re-pointed).
- consumer: nine more rows cite gitignored `Tools/work` **datasets**, not records: B-3, AL-8, AQ-2, BA-1, BQ-27,
  EA-2, EE-11, UQ-2 and UQ-297, citing `rtti/*.tsv`, `graph/functions.tsv`, `h94/phyre_schema.tsv` and `repos-d2`.
  routed-to-board-note: their owners should track the dataset under `_index/candidates/` or re-point to a tracked
  generator. T now reports them. Only AQ-2 and UQ-2 are named on any page's status line, one page each, and both
  rows are SUPERSEDED.
- consumer: `documented_rule.out` (the committed tally): agrees. The rule's per-page verdicts outside those rows are
  unchanged.

## Regression

run: documented_rule.py at 1e76d4dae (self-test 33/33 PASS with the new case, run from a copy carrying this change)
