# SWE2-AUDIT-SPEC review - owner re-status batch 16 (five pages + SEM corrections)

Task: `OPUS-REQ-AUDITSPEC-DD-OWNER-B16-1001`. Package: `_index/candidates/opus-dd-restatus-16-1001/`.

## Verdict: ACCEPT

Scope: owner re-status (page status lines + cited prerequisites + declared A-drift pairings).
Evidence class: NATIVE/STATIC for the cited records' anchors; process verification for the flips.

## Independent verification

- All five pages carry `status: DOCUMENTED` at HEAD (active-party, battle-hud-readers, selection, equipment-slots, numeric-formatting).
- The incorporated corrections are real reviews: `auditsem-review-sd125-128-0930` (ACCEPT-WITH-NARROWING, C1/N1/N3) and `auditsem-review-gr19-gr11-0930` (ACCEPT-WITH-NARROWING, C4) both exist with those verdicts; the pages' status lines and sections reflect the incorporated wording (battle-hud names SD-126/SD-127 resolved, selection names the `001EDEC0`/bit-8 gates).
- A-drift pairings as declared incl. the GlobalArrayFlagScan row retirement (4 -> 0, retired since a zero-case cannot pass).

## Limits

The underlying answer records are verified to exist with the cited verdicts/rows; their own independent
reviews are separate board items (SD7-SD107 and DDRES-B8 are still in this lane's queue). The live
`adrift_report.py` currently shows 13 refused rows from post-batch page promotions across the fleet -
outside every batch's scope; each batch's own '0 refused at apply' claim was checked against its dated
snapshot output.
