# DD owner re-status, batch 20: the battle-record kind page to DOCUMENTED, GR-2 narrowed (OPUS, 2026-10-01)

`04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md` was EVIDENCE-UNTRACKED under `documented_rule.py`. The
only cause was AL-8's citation of a gitignored map. The register now cites a byte-identical tracked copy
(`opus-register-narrow-1001`), so the page reads READY once that copy is committed.

## Applied (OPUS)

- **§7's GR-2 box** takes SWE2-AUDIT-SEM's C1-C5 ([`auditsem-review-gr2-0930`](../auditsem-review-gr2-0930/REVIEW.md),
  ACCEPT-WITH-NARROWING, `gr2_sem.py` FAILS 0):
  - the six writers of the nibble;
  - where 0 and 7 come from, and that no writer produces 2;
  - the conditional argument-3 join;
  - the refresh limit;
  - type 3 includes the `disp_tama` objects, and type 6 is three boss-fight scripts' value;
  - counts are nine language copies.

  Old wording is struck.
- **The §-head note** "the page stays PARTIAL for the residue in §7 (GR-2)" is struck.
- **Status:** PARTIAL -> DOCUMENTED.

## A-drift, paired (OPUS)

`0050F910` becomes A (`@0050F94E`) and leaves ScriptVM.VerbAdapter (1033 -> 1032, exact removal, `round10_notes.py`).
Afterwards `adrift_report.py` reports 0 refused rows.

run: documented_rule.py READY 1 of 1 after the AL-8 copy is tracked; adrift_report.py refused rows 0 (FAILS 0)

## Review (OPUS)

The owner read goes to SWE2-AUDIT-SPEC. It discharges the page half of FABLE's `OPUS-REQ-FABLE-GR2-C1C5-1001`.
