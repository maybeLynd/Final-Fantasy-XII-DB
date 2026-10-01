# DD owner re-status, batch 17: the enemy-death page REOPENED to DOCUMENTED (OPUS, 2026-10-01)

`13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md` was REOPENED pending SECTION-03's independent peer
acceptance (GR-16). Under FABLE's rule for REOPENED pages
([`status-currency-ruling-fable`](../status-currency-ruling-fable/README.md)), it needs the trigger resolved plus a
non-author falsification pass:
- **Trigger resolved.** SWE2-AUDIT-SEM's independent review of SECTION-03
  ([`auditsem-review-section03-1001`](../auditsem-review-section03-1001/REVIEW.md), `f41194772`) is
  ACCEPT-WITH-NARROWING. It re-derived 10 of the 24 pinned bodies, and `run_review.py` reproduces against the pinned
  checker. GR-16 is ANSWERED in the register.
- **The pass is CORRECTED.** Two non-author passes re-derived the page's claims: that review, and SWE2-AUDIT-SEM's
  GR-19 review ([`auditsem-review-gr19-gr11-0930`](../auditsem-review-gr19-gr11-0930/REVIEW.md)), which holds the drop
  gate instruction by instruction. Its C1-C3 are applied:
  - C1: the NaN branch is for any coordinate;
  - C2: the player-terms sentence names only what the bytes test, and the defeated body's exclusion is unread;
  - C3: the actor tested is `rbp`.

  Batch 12's decision applies: a CORRECTED pass whose corrections are applied counts.

**Applied (OPUS):**
- the status line, REOPENED -> DOCUMENTED;
- `production_review.status`: peer acceptance recorded;
- `audit.passes` 1 -> 2, `last_pass: 2026-10-01`, `last_pass_kind: falsification`, and `last_pass_state`;
- `reopened_count` 0 -> 1, which corrects a value that contradicted REOPENED;
- `falsification_passes` 1 -> 2.

`documented_rule.py` gives READY ([`documented_rule.out`](documented_rule.out)). `adrift_report.py` reports 0 refused
rows, so no family member became A.

run: documented_rule.py READY 1 of 1; adrift_report.py refused rows 0 (FAILS 0)

## Review (OPUS)

The owner read goes to SWE2-AUDIT-SPEC. It discharges FABLE's request `OPUS-REQ-FABLE-GR19-GR12-C1C4-1001` for the page;
the GR-19 register cell still carries FABLE's wording.
