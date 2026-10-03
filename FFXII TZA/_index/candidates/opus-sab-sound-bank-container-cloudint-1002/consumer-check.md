# Consumer check: row 001FB770's call arguments corrected (OPUS, 2026-10-03)

SWE2-AUDIT-SPEC rejected this record ([review](../auditspec-review-opus-sab-sound-bank-container-cloudint-1002/REVIEW.md)). The row said the call to `001FB470` passes "that node" and "the low byte of the fifth (stack) argument". The frame is 0x48 bytes (`push rbx`, `sub rsp,0x40`), so `[rsp+0x60]` at `001FB7BD` is the entry r8 home slot, which the body never writes. The third argument is `lea r8,[rsp+0x50]`, a slot holding the node. SPEC's replacement clause is applied verbatim; the rest of the row (the tree walk, key, descent and the `+0x28` store) SPEC found exact.

- **Affected:** 18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's interior-citation row for `001FB770` | revised-here |
  | rows.json (the record) | revised-here, with the correction listed |
  | the F gate's interior credit (check_dispositions, progress.py) | agrees: the function and its anchors are unchanged |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-reject-repairs-1003/reject_rows_check.py, verified at bc6245a96: 2 rows, FAILS 0 ([`reject_rows_check.out`](../opus-reject-repairs-1003/reject_rows_check.out)).
  - It decodes the function from the certified image and checks each fact the repair rests on, then requires the repaired clause and refuses the rejected one.
  - Run with `--rejected` on the rejected texts, it fails both rows ([`reject_rows_check.rejected.out`](../opus-reject-repairs-1003/reject_rows_check.rejected.out)).
