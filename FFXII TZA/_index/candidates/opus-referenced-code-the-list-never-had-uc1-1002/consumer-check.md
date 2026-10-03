# Consumer check: 15 UC-1 entry statements corrected (OPUS, 2026-10-03)

SWE2-AUDIT-SPEC rejected this record ([review](../auditspec-review-opus-referenced-code-the-list-never-had-uc1-1002/REVIEW.md)).
Fifteen rows said "no direct reference was found" for bodies that are referenced:
- fourteen by a conditional jump;
- one, `00195340`, through the image-relative destructor field of a C++ throw-info record.

The first census (`uc1_credible.py`) indexed calls and unconditional jumps only. Each of the fifteen rows' entry clause
is replaced with the site SPEC verified. The body sentences are unchanged: SPEC's semantic sample covered three of
them and found them exact.

- **Affected:** 99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the host page's 53-row UC-1 section | revised-here |
  | rows.json (the record) | revised-here, with the correction listed |
  | the F gate's UC-1 credit (check_dispositions, progress.py) | agrees: the series-break phrase and the interior anchors are unchanged |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-referenced-code-the-list-never-had-uc1-1002/uc1_entry_check.py, verified at fb2de5ab8: 53 rows, FAILS 0 ([`uc1_entry_check.out`](uc1_entry_check.out)).
  - It re-derives test 1 image-wide: every decoded `call`, `jmp` and `jcc`, qword tables, and 32-bit image-relative fields outside `.pdata`.
  - On the published rows it fails exactly the fifteen.
