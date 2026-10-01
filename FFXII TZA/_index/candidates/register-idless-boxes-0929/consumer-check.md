# Consumer-check record: the 49 OV register rows and page-box dispositions

Companion to the staged delta `README.md` in this directory (FABLE, committed 3ef8baac6).
EVIDENCE-POLICY 4a record for the correction-marked publish that ticks/annotates the
checklist boxes and writes the register rows.

## Affected

Affected rows: OV-1 through OV-49 — the checklist boxes on the eleven SECTION-overlay
pages named in the README table (eight committed pages plus three newly committed `02`
pages) and their new register rows in `_index/OPEN-QUESTIONS.md`. Affected rows close as
SUPERSEDED (class-1 declared limit or duplicate), NOT A QUESTION (class-2 process item
carried by a board carrier), ANSWERED (evidence named on the row), or stay OPEN with a
required-scope/runtime split. No executable claim shape is edited: every struck span is a
verbatim quote of the box's own removed text plus a disposition annotation.

## Consumers and agreement

The consumer of each box is the register gate: the row's disposition is the agreement the
page box records. FABLE's staged classification (the README table) is the producer
agreement for all 32 committed-page rows; this publish applies it row-for-row, and the
same classes to the 17 rows on the three pages committed alongside. For the class-2 rows
the named carrier task is the consumer that agrees the process item exists: nine rows ride
FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929, OV-30 rides
FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926, and OV-31 is routed-to-SWE2-STRUCT
(FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE). Nothing self-awards independent acceptance.

## Regression

`Database/Tools/analysis-kit/gfz-scripts/check_questions.py --db "Database/FFXII TZA"`
— run after the apply on this publish's working tree: 0 row/header cell mismatches,
0 ticked-boxes-still-OPEN, table and document checklists agree. The same run is the
continuous regression for the row/page agreement this record describes.
