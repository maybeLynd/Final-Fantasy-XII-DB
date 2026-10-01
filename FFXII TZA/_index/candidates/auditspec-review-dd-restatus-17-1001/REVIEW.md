# SWE2-AUDIT-SPEC review - owner re-status batch 17 (enemy-death REOPENED->DOCUMENTED)

Task: `OPUS-REQ-AUDITSPEC-DD-OWNER-B17-1001`. Package: `_index/candidates/opus-dd-restatus-17-1001/`.

## Verdict: ACCEPT

Scope: owner re-status (page status lines + cited prerequisites + declared A-drift pairings).
Evidence class: NATIVE/STATIC for the cited records' anchors; process verification for the flips.

## Independent verification

- `what-happens-when-an-enemy-dies.md` now carries `status: DOCUMENTED` citing the SECTION-03 reopening resolved and GR-16 ANSWERED.
- FABLE's REOPENED protocol held: the trigger is resolved (SEM's `auditsem-review-section03-1001` at `f41194772`, ACCEPT-WITH-NARROWING) and the falsification condition is met by the SEM GR-19 review's CORRECTED pass whose C1-C3 corrections are applied on the page (batch-12's standing decision: a corrected pass with corrections applied counts).
- `audit.passes` 1->2, `reopened_count` 0->1 and `falsification_passes` 1->2 are consistent front-matter bookkeeping for a REOPENED page that completed the pass cycle.

## Limits

The underlying answer records are verified to exist with the cited verdicts/rows; their own independent
reviews are separate board items (SD7-SD107 and DDRES-B8 are still in this lane's queue). The live
`adrift_report.py` currently shows 13 refused rows from post-batch page promotions across the fleet -
outside every batch's scope; each batch's own '0 refused at apply' claim was checked against its dated
snapshot output.
