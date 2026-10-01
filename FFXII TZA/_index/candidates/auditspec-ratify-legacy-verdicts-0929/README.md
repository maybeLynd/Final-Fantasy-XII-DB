# Ratifying 35 legacy verdict-less reviews by SWE2-AUDIT-SPEC (for `OPUS-REQ-AUDIT-SPEC-RATIFY-LEGACY-VERDICTS-0929`)

SWE2-AUDIT-SPEC. This lane was run by the FABLE session's executor `73162e75` on 2026-09-29.

**What this is.** Since `ed127d443`, a review that carries a `reviews` field finishes with exactly one structured
`verdict:<V>` ref. `a16-finish-verdict-gate-0929/legacy-verdictless-reviews.tsv` lists 35 DONE reviews by this lane
whose verdicts are stated only in prose.

**How ratification works.** This is additive. Each ratifiable review gets a new task, `RATIFY-<original id>`. The
new task carries the original `reviews` field plus `"ratifies": "<original id>"`, and it is finished with the
verdict the lane's own record already states.

- No original task is edited.
- No verdict is changed.
- No review is re-performed.

## The source record

All 35 rows cite `Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-0929-FINAL-BATCH.md`. That file is in the gitignored
`work/` tree, so it is not durable. It is copied here **verbatim** as `source-REVIEW-0929-FINAL-BATCH.md`, and the
`source_line` numbers in `ratify-map.tsv` refer to that copy.

## Mapping rule (stated so it can be checked, not guessed)

The record gives each disposition in one of the following words. The task each disposition reviewed is ASTRA's or
OPUS's package, and each disposition is the lane's judgement *of that package*:

| record wording | meaning in the record | structured verdict |
|---|---|---|
| `ACCEPT` (section heading or bold line) | the package's claim is supported | `ACCEPT` |
| `ACCEPT scoped …` (S70 table, S71, S74) | the package's **own** scoped result (for example `ACCEPT_SCOPED_ADMISSION`) is reproduced and supported as written. S70's preamble: "Package limits preserved verbatim; NO package result was promoted". No narrower wording is imposed. | `ACCEPT` |
| `REJECTION ACCEPTED` / `REJECTION VERIFIED` / `REJECTION OF BASIS ACCEPTED` | the package's claim is itself a rejection, and the lane reproduced it and upheld it. S70's note: "all REJECT dispositions mean the ASTRA rejection stands under independent re-execution" | `ACCEPT` |

Nothing in the record is an `ACCEPT-WITH-NARROWING` that states the narrowed words, and nothing is a REJECT of the
package. So every ratifiable row is `ACCEPT`.

A row is matched to the table only when the table's package directory equals the board task's `reviews.record`
directory. If they differ, the row is reported rather than guessed.

## Result (`ratify-map.tsv`)

- **33 ratified as `verdict:ACCEPT`.** Each `RATIFY-*` task cites this record, the ratification commit and its
  source line.
- **2 reported as UNCLEAR and not ratified:**
  - `ASTRA-REQ-SPEC-HEADING-COMMIT-TAIL-SUPPLEMENT` (package `eab9cdf34`): the lane's record has **no** verdict line
    for it.
  - `ASTRA-REQ-SPEC-TYPED-POP-REPORT-BOUNDARY`: the S70 row (L345) names package `EXP-013-vm-pop-boundaries`, but
    the task's `reviews.record` is `_experiments/evidence/scriptvm-retail-report-consumer-boundary/README.md`. The
    record and the task disagree about which package was reviewed.

  Each of these needs a real review, or the original session's statement of what was reviewed. Both are listed in
  the board finish of the request.
