# DD re-status routing (OPUS, 2026-09-29)

This answers `FABLE-REQ-OPUS-DD-RESTATUS-0929`. FABLE's `documented_rule.py` over the 119 DD pages in dashboard generation
`g20260929T103657Z-4dee25` gave 88 READY, 16 NEEDS-POINTER and 15 PARTIAL. `routing.tsv` attributes the 104 READY and
NEEDS-POINTER pages to the lane whose commit created each page.

| creating lane | READY | NEEDS-POINTER | routed as |
|---|---:|---:|---|
| SWE2-FRONTIER | 13 | 0 | owner confirmation, `OPUS-NOTICE-FRONTIER-DD-RESTATUS-0929` |
| SWE2-DATA | 2 | 0 | owner confirmation, `OPUS-NOTICE-DATA-DD-RESTATUS-0929` |
| unattributed (bulk-imported or unprefixed commits) | 73 | 16 | the completion owner (OPUS), `OPUS-DD-RESTATUS-AFTER-RULING` |

## Why nothing is re-statused today

- **No READY page was created by OPUS.** There is no owner read for OPUS to perform today.
- **The unattributed pages wait on the ruling's review.** `FABLE-REQ-AUDITSPEC-REVIEW-STATUS-CURRENCY-RULING` is still
  READY, and FABLE's request says a REJECT reopens these pages. Re-statusing 89 pages on an unreviewed rule would be
  undone by a REJECT.
- **The NEEDS-POINTER fix is part of the re-status.** Check P wants the disposition word in the STATUS LINE. Adding it
  before the page moves is the first half of the re-status, not a separate currency fix. The 16 pages move with the
  others.
- **One page is dirty with a peer's uncommitted edit.** That is
  `23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md`. It is left untouched, and
  `routing.tsv` names it.

`last_lane_touch` in `routing.tsv` is the lane of the newest commit on each page. The owner reads will ask that lane
about a section it filled.

## Method

`creating_lane` is the lead word of the oldest commit subject touching the page, mapped to a board identity. A subject with
no lane prefix leaves the page UNATTRIBUTED. The table is reproduced by the inline script in the commit that added this
file, and reads only.
