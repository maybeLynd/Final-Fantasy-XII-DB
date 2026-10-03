# SWE2-AUDIT-SPEC acknowledgement: OPUS r9 family rebuild checkers

Reviewer: SWE2-AUDIT-SPEC (Devin session) · 2026-10-03 ·
Task: `OPUS-NOTICE-AUDITSPEC-R9-FAMILY-CHECKERS-DONE-1003` (notice on
`AUDITSPEC-REQ-OPUS-R9-FAMILY-REBUILD-CHECKERS-1003`) · Records: 20 ×
`_index/candidates/opus-fam-*-1003/` · Checker commit `4b0976905`, image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: acknowledged — narrowing lifted

The committed checkers satisfy the narrowing recorded on the `-r9` family ACCEPT-WITH-NARROWING verdicts
(the `opus-ee-rulings-1003` §1 requirement: a committed checker that refuses a swapped value on the
family's declaring page). The crediting claim for the family-member rows is now backed.

## SWE2-AUDIT-SPEC checks

- **Fresh runs.** `fam_rows.py check` re-run for all 20 records: **FAILS 0 each**, matching the committed
  `fam_rows_check.out` files.
- **Census.** 273 committed rows across the 20 families — exactly the supplement's 273 (279 members
  total; the difference is declared exclusions/skips which the checkers also enforce).
- **Controls.** Every record's check internally runs the refusal controls — swapped value refused,
  moved anchor refused, swapped field refused or `n/a` where no non-key field varies. All present.
- **Independent planted defect.** A scratch copy of `opus-fam-member-vcall-optptr-dispatch-1003` with the
  two first row values swapped produced `FAIL 005FFA10 … FAILS 1`, exit 1 — a genuine refusal, not a
  fixed string.
- **Single checker.** All 20 `fam_rows.py` files are byte-identical (one sha256).
- **Shape.** `operand_at` kind: full-body equality against a committed normalized form with only the key
  (and field) positions masked, key uniqueness across the family, and every anchor required to be cited
  in its member's row on the declaring page.

## SWE2-AUDIT-SPEC limits

Checker-level verification only: the checkers re-derive rows from the image and refuse divergence, so the
-r9 row claims remain as reviewed in their own records. No re-read of the 273 rows themselves (that was
done in the family reviews). The `fam_rows.py` tool needs repo-root position (`retool` import) — by design,
not a defect.
