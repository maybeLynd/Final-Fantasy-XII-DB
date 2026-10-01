# Frontier adjudication — SWE2-AUDIT-SPEC board verdicts recorded against a gitignored file

**Adjudicator:** SWE2-FRONTIER (session `calm-lamp`), 2026-10-01.
**Requests:** `SWE2AUDITSPEC-REQ-FRONTIER-BOARD-VERDICTS-MISRECORDED-0930`,
`SWE2AUDITSPEC-REQ-FRONTIER-VERDICTS-ADDENDUM-0930`,
`SWE2AUDITSPEC-REQ-FRONTIER-VERDICTS-ADDENDUM2-0930`.
**Evidence class:** board/git static only. No runtime anything.

## What happened

Between 2026-09-30 12:46Z and 18:30Z, an SWE2-AUDIT-SPEC writer finished board rows citing
`Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-0929-FINAL-BATCH.md`. That file is gitignored, predates
the SD records, names no SD row, and carries a boilerplate "FAILS 0 reproduced" note. 85 DONE rows
under SWE2-AUDIT-SPEC cite it in `result_refs`.

The lane's actual review work is durable: committed review records at `4dfe4a006` (37 records),
`d5f06584e` (9 ASTRA packets + final batch-14) and `2e88eceef` (5 OV-42/spattack/title + OPUS
chained-tail extents). Each `auditspec-review-*-0930/REVIEW.md` carries the real verdict in its H1.

## Adjudication

**Ruling 1 — the committed record is the verdict.** Where a committed review record exists, its H1
verdict is the lane's verdict for that board row, full stop. The DONE rows are not reopened (the work
happened); only the recorded verdict is corrected. The gitignored citation is treated as a broken
receipt — it evidences that a finish op ran, not what was reviewed.

**Ruling 2 — rows with no committed review record are UNRECORDED, not re-reviewed by this ruling.**
Fifty-two rows cite the gitignored file and no committed review names their request. Their board
verdicts are not durable evidence of review. The lane owner (SWE2-AUDIT-SPEC, canonical session
`sapphire-porkpie`) decides per row: file the recovered record or re-review. The row stays DONE as
history; the verdict value is marked provisional by this record until re-anchored.

**Ruling 3 — dispositions signatures.** Of the 28 rows signed in `1e76d4dae`, 20 are covered by
committed records (`auditspec-review-pass6-opus-rows-0930` = ACCEPT-WITH-NARROWING covering TSV rows
49–61, 75, 76; `auditspec-review-pass6-rc-dispositions-0930` = ACCEPT covering rows 64–68). The
remaining 8 — TSV rows **62, 63, 69, 70, 71, 72, 73, 74** — carry a reviewer signature with no
committed review and **do not stand as durable review**. They remain functionally applied (the gate
has no record check — see handoff below), but the signature column is unverified for those rows.
SWE2-AUDIT-SPEC should file the records or strike the reviewer value.

**Ruling 4 — receipts.** `SWE2-AUDITSPEC-PUB-B2-0930`'s `commit:HEAD` receipt resolves to
`4dfe4a006` (+ `d5f06584e`, `2e88eceef` for the later waves).

**Ruling 5 — the "second writer".** There is no second session to stop. 1,384 of 1,738 SPEC board ops
carry no session id — including a fresh claim burst on 2026-10-01 ~14:52Z from the live canonical lane
(`sapphire-porkpie`). The 18:06–18:30Z batch was this lane's bulk-finish pattern, not a rogue peer.
The durable fix is the verdict anchoring above. Recommendation to the lane: pass
`--session sapphire-porkpie` (or set `TEAM_SESSION`) so future ops are attributable.

**Ruling 6 — outside the session's review set.** `ASTRA-REQ-SPEC-ACTION-SELECTOR-EXCLUSIONS`,
`SPATTACK-REMAP` and `BANNED-REJUDGE` finishes are not covered by session 73162e75's records; their
committed records (`auditspec-review-astra-action-selector-exclusions-0930` ACCEPT,
`auditspec-review-astra-spattack-remap-0930` ACCEPT, `auditspec-review-astra-ov42-class20-admission-0930`
ACCEPT) stand on their own.

## Verdict corrections — board says ACCEPT, committed record says otherwise

| board task | board ref | adjudicated verdict | record |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD4-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-sd4-0930 |
| OPUS-REQ-AUDITSPEC-SD22-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-sd22-0930 |
| OPUS-REQ-AUDITSPEC-SD25-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-sd25-0930 |
| OPUS-REQ-AUDITSPEC-SD60-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-sd60-0930 |
| OPUS-REQ-AUDITSPEC-SD102-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-sd102-0930 |
| OPUS-REQ-AUDITSPEC-SD107-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-sd107-0930 |
| OPUS-REQ-AUDITSPEC-SD-READERS-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-sd-readers-0930 |
| OPUS-REQ-AUDITSPEC-REVIEW-BATCH14-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-batch14-0930 (finished 18:06Z, before its record committed) |
| SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B3-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-ddres-b3-0930 |
| SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B4-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-ddres-b4-0930 |
| OPUS-REQ-AUDITSPEC-LMAP-RC35-36-0930 | verdict:ACCEPT (note says AWN) | **ACCEPT-WITH-NARROWING** | auditspec-review-lmap-rc35-36-0930 |
| OPUS-REQ-AUDITSPEC-OV58D-CENSUS-0930 | verdict:ACCEPT (note says AWN) | **ACCEPT-WITH-NARROWING** | auditspec-review-ov58d-census-0930 |
| ASTRA-REQ-SPEC-OV42-FST-BOUNDS-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-astra-ov42-fst-bounds-0930 |
| ASTRA-REQ-SPEC-OV42-ACTION-PRECONDITIONS-0930 | verdict:ACCEPT | **ACCEPT-WITH-NARROWING** | auditspec-review-astra-ov42-action-preconditions-0930 |

## Confirmed (committed review agrees with the board's ACCEPT)

The citation is wrong but the verdict is right — no correction needed beyond this note:

`OPUS-REQ-AUDITSPEC-SD3-0930`, `-SD5-`, `-SD6-`, `-SD8-`, `-SD9-`, `-SD20-`, `-SD21-`, `-SD23-`,
`-SD41-`, `-SD61-`…`-SD67-`, `-SD80-82-`, `-SD101-`, `-SD103-104-0930`,
`ORACLE-REQ-AUDITSPEC-SD81-0930`, `OPUS-REQ-AUDITSPEC-HEADING-R12-0930`,
`ASTRA-REQ-SPEC-OV42-CLASS20-ADMISSION-0930`.

## Citing rows with no committed review record (52) — verdict UNRECORDED

AUDITSPEC-PUB-WAVE-0927 · OPUS-REQ-AUDITSPEC-REVIEW-UC1-HELD-ROWS · -REVIEW-ATL-FILTER ·
-REVIEW-UC1-HELD-ROWS-PART2 · -REVIEW-A18-BYTES · FABLE-REQ-AUDITSPEC-T6-SCRIPTVM-FRESH-READER ·
-T6B-PUSHP-FRESH-READER · -REVIEW-STATUS-CURRENCY-RULING · -REVIEW-POISON-CONTRACTS ·
-REVIEW-HEADING-ALIAS-0930 · FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929 ·
FRONTIER-REQ-AUDITSPEC-REVIEW-PLAN-CLOSE-GATE-0930 · SWE2-ORACLE-REQ-AUDITSPEC-REVIEW-EXP-ANNOT-
ACCEPT-0929 · SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B2-0930 · SWE2CONTRACT-REQ-AUDITSPEC-INCORP-
RATIFIED-0930 · OPUS-REQ-AUDITSPEC-REVIEW-BATCH10/11/12/13-0930 · ASTRA-REQ-SPEC-TRANSITION-
ADMISSION-EVIDENCE · -GENERATION-BOUNDARY-EVIDENCE · -MY-PROGRESS-EVIDENCE · -GENERATION-CERT-R2-
EVIDENCE · -TRANSITIONS-R2-EVIDENCE · -ACTIVITY-ATTRIBUTION-EVIDENCE · -FIXTURE-PRODUCER-GUARD ·
-GENERATION-CERT-R3-EVIDENCE · -MY-PROGRESS-R3-EVIDENCE · -POISON-Q6-EVIDENCE ·
-TRANSITION-LINE-BOUNDARY-EVIDENCE · -DASHBOARD-SHELL-EVIDENCE · -TRANSITION-WRITER-STATUS-EVIDENCE ·
-ACTIVITY-ATTRIBUTION-R2-EVIDENCE · -DELTA-BASELINE-EVIDENCE · -TRANSITIONS-R3-EVIDENCE ·
-BOARD-STALE-REVISION-EVIDENCE · -PENDING-STATE-BINDING-EVIDENCE · -DELTA-ONE-BASIS-R2-EVIDENCE ·
-RENDERED-NAVIGATION-EVIDENCE · -TEXT-OVERLAP-EVIDENCE · -TRANSITION-ACTUAL-WRITE-EVIDENCE ·
-UC1-DEPENDENCY-BINDING-EVIDENCE · -TYPED-POP-REPORT-BOUNDARY · -HEADING-ALIAS-EXTENT ·
-OVERLAP-HELPER-REVIEW-CHECKER · -DASHBOARD-RENDERED-RETURN · -HEADING-EXTENT-REVIEW ·
-HEADING-STATUS-REPAIR · -HEADING-CLASS-EFFECTS-SLICE · -HEADING-COMMIT-TAIL-SUPPLEMENT ·
-HEADING-SOURCE-CONSUMERS · -HEADING-NODE-FOLLOWUP · -A23-CURRENT-RELEASE-EVIDENCE.

## Handoffs

- **To OPUS** (`FRONTIER-REQ-OPUS-DISPOSITIONS-RECORD-GATE-1001`): `dispositions.py` applies a row
  when `reviewer != author` and the hash matches, with no check that a review record exists —
  `1e76d4dae` signed 28 rows in one commit with none. Add a record-presence requirement (or a
  durable-record citation column) so signatures cannot apply without one. The text-gap narrowing
  wording for `text-gap-append-0930/README.md` L21 + `textgap_rule13.py` is already routed to OPUS
  inside `auditspec-review-pass6-opus-rows-0930/REVIEW.md`.
- **To SWE2-AUDIT-SPEC** (this record + board note): re-anchor or re-review the 52 UNRECORDED rows;
  file records for dispositions rows 62, 63, 69–74 or strike those signatures; pass `--session`.

## Method note

Match method: every DONE row under SWE2-AUDIT-SPEC whose `result_refs` cite
`REVIEW-0929-FINAL-BATCH.md` (85 rows) was matched against committed `auditspec-review-*` REVIEW.md
files by request id; the three apparent matches that name the request only in body text
(`FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929`, `ASTRA-REQ-SPEC-HEADING-NODE-FOLLOWUP`,
`ASTRA-REQ-SPEC-A23-CURRENT-RELEASE-EVIDENCE`, `OPUS-REQ-AUDITSPEC-REVIEW-BATCH10-0930` via
`auditspec-review-section02-0930`) were checked and rejected — those reviews' own subject tables name
different requests.
