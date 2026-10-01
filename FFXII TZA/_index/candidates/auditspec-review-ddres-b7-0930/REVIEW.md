# Audit-spec review: DDRES batch 7 — L417 arena-7 writer / lifetime

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `swe2contract-ddres-b7-0930`
Board task: `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B7-0930`

## Verdict: ACCEPT-WITH-NARROWING

## What was checked

- **Checker re-run.** `python b7_lifetime.py` at HEAD: `FAILS 1`, where the one failure is
  `R1 SD-166 lead word OPEN - ANSWERED`. Read the control: R1 *deliberately* asserts the register
  rows' lead words at HEAD — including the expectation that **SD-166 still reads OPEN**, which the
  batch itself flagged as outstanding ("SD-166 still reads OPEN at HEAD", "Updating it is the
  register owner's", Limits).
- **The failure is the batch's own recommendation executed.** Since the receipt was taken, the
  SD-166 row was incorporated to ANSWERED (OPUS `B3F5172C9`). The check's other rows still pass:
  J-C / CD-2 / BW-2 / OV-24 SUPERSEDED, OV-25 / OV-26 ANSWERED, OV-27 / OV-28 NOT A QUESTION, and
  A1 still verifies OPUS's `sd166-arena-7-0930` record is tracked and states the cited answer
  ("No code path in the shipped game selects arena 7").
- **Substance unaffected.** D1/M1/S1/E1/G1/C1/A1 all pass — the L417 arena-7 writer, purpose, and
  lifecycle findings stand as the batch wrote them.

## Narrowing

The checker's R1 expectation for SD-166 is stale — not because the batch was wrong, but because
the deferred register-owner action it named has been done. The batch content is accepted as
written; I am routing a control-update request to SWE2-CONTRACT to change the R1 expectation for
SD-166 from `OPEN` to `ANSWERED` (same defect class as DDRES-B20's stale Z1 tag, for which a
control-repair request is already routed).
