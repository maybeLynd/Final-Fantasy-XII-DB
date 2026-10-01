# Consumer check: two pages re-statused DOCUMENTED after the status-currency ruling (OPUS, 2026-09-30)

corrects: 22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md (the status line and two prose clauses that still called AQ-2 and AQ-5 open)
corrects: 23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md (the status line that still called UQ-302, BN-2, UQ-304 and UQ-305 open)

## What was corrected

Nothing about the engine changed. These are status-currency corrections under FABLE's status-currency ruling. The two
pages still described register rows as open after their owners had closed them:

- **phyre-subsystem-map.md**
  - AQ-5 is ANSWERED (973 of 993 non-glue functions reachable).
  - AQ-2 is SUPERSEDED as a population-coverage statement; its population is carried by
    `members/phyre-function-class-map.tsv`.
  - The clauses "both still open below" and "stays PARTIAL on the 2,254 unplaced functions" are struck and pointed at
    the boxes.
- **phyre-to-bullet-rigid-body-materialization.md**
  - UQ-302 is SUPERSEDED as a duplicate of BN-1, which is answered (the 2.77 line).
  - BN-2 is answered.
  - UQ-304 and UQ-305 are SUPERSEDED as duplicates of BN-4 and BN-6, as their register rows state.

These were the two of the 89 unattributed pages that the owner read found READY-WITH-POINTER
(`_index/candidates/dd-owner-read-0929/`, 43b8ff75e).

## Current consumers

- consumer: `_index/OPEN-QUESTIONS.md` rows `AQ-2`, `AQ-5`, `UQ-302`, `BN-1`, `BN-2`, `BN-4`, `BN-6`, `UQ-304` and `UQ-305`. They already
  carry the dispositions these status lines now repeat, so they agree and are not edited.
- consumer: the pages' own question boxes. They agree with the rows; `check_questions.py` reports the table and the
  checklists consistent.
- consumer: `_index/candidates/dd-owner-read-0929/worksheet.tsv` lists both pages as READY-WITH-POINTER, so it agrees.

## Regression

regression: `FFXII TZA/_index/candidates/status-currency-ruling-fable/documented_rule.py` on the two pages reports
`TALLY READY-WITH-POINTER=2 of 2`. The publish runs it as its gate, and it fails if either page's status line
disagrees with its register rows or evidence sections. `Database/Tools/analysis-kit/gfz-scripts/check_questions.py`
reports the register and the document checklists consistent.
