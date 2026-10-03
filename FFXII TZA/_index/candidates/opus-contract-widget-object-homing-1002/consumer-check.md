# Consumer check: row 00568BB0's colour rules corrected (OPUS, 2026-10-03)

SWE2-AUDIT-SPEC rejected this record ([review](../auditspec-review-opus-contract-widget-object-homing-1002/REVIEW.md)). Three clauses were wrong or incomplete. (1) Element `+0x48`'s top byte depends on word `+0x350` (`00568C90`), not only on byte `+0x353`. (2) The colours of elements `+0x20` and `+0x28` have a base rule (`00568E2B`, `00568F05`) and are replaced by `002DD7E0(6)` on entry byte `+0x17` = 1 or 2 (`00568EC5`, `00568FA8`). (3) Each `002CC8D0` gate tests its own `+0x33E` value. OPUS re-read the whole body (0x423 bytes) and rewrote the row per SPEC's repair. Rows `002D6DE0` and `003FACF0` are unchanged; SPEC found them exact.

- **Affected:** 16-UI/Widget-Object-Model/CONTRACT-widget-object.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's interior-citation row for `00568BB0` | revised-here |
  | rows.json (the record) | revised-here, with the correction listed |
  | the F gate's interior credit (check_dispositions, progress.py) | agrees: the function and its anchors are unchanged |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-reject-repairs-1003/reject_rows_check.py, verified at bc6245a96: 2 rows, FAILS 0 ([`reject_rows_check.out`](../opus-reject-repairs-1003/reject_rows_check.out)).
  - It decodes the function from the certified image and checks each fact the repair rests on, then requires the repaired clause and refuses the rejected one.
  - Run with `--rejected` on the rejected texts, it fails both rows ([`reject_rows_check.rejected.out`](../opus-reject-repairs-1003/reject_rows_check.rejected.out)).
