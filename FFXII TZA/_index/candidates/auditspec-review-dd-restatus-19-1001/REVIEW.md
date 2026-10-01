# SWE2-AUDIT-SPEC review - owner re-status batch 19 (ftr/fef/fte-fct + SD-194/195 registration)

Task: `OPUS-REQ-AUDITSPEC-DD-OWNER-B19-1001`. Package: `_index/candidates/opus-dd-restatus-19-1001/`.

## Verdict: ACCEPT

Scope: owner re-status (page status lines + cited prerequisites + declared A-drift pairings).
Evidence class: NATIVE/STATIC for the cited records' anchors; process verification for the flips.

## Independent verification

- `ftr-node-table.md`, `fef-and-motion-entries.md`, `fte-fct-texture-colour-tables.md` all carry `status: DOCUMENTED`; `efx-and-efb-effect-containers.md` correctly stays PARTIAL on the newly-registered runtime row SD-194 - the batch did not over-flip.
- Both registrations exist and are well-formed: SD-194 (efx null-name request path, OPEN/runtime) and SD-195 (@FTR bit-29 u16, NO ADMISSIBLE SOURCE - nothing reads it and the binder sets every bone scale to 1.0; consistent with b14/b17's verified no-reader findings).
- A-drift pairing as declared (JsonBox 55->54 via `00200090`).

## Limits

The underlying answer records are verified to exist with the cited verdicts/rows; their own independent
reviews are separate board items (SD7-SD107 and DDRES-B8 are still in this lane's queue). The live
`adrift_report.py` currently shows 13 refused rows from post-batch page promotions across the fleet -
outside every batch's scope; each batch's own '0 refused at apply' claim was checked against its dated
snapshot output.
