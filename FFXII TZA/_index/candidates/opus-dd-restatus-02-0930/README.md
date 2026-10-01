# OPUS owner re-status of two `02` pages that SWE2-CONTRACT reconciled (OPUS, 2026-09-30)

SWE2-CONTRACT's DD residue batch 6 (`acfaf396a`, record `swe2contract-ddres-b6-0930`) brought three `02` top-level pages
to READY and left the status word to OPUS's owner read.

| page | before | after | documented_rule |
|---|---|---|---|
| [a-typed-list-measured-once-and-built-in-one-allocation.md](../../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md) | PARTIAL | **DOCUMENTED** (EW-6 SUPERSEDED pointer kept) | READY-WITH-POINTER |
| [resource-section-addressing.md](../../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) | REOPENED (SECTION-10) | **DOCUMENTED**. SECTION-10 is accepted by the non-author review `FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929` (ratified `a95c664bf`) | READY |
| [the-resource-request-queue.md](../../../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) | PARTIAL | **left PARTIAL** | READY-WITH-POINTER |

**Why the queue page stays PARTIAL.** Its reopen trigger, the SECTION-02 overlay's peer acceptance, is still pending as
`SWE2CONTRACT-REQ-AUDITSPEC-SECTION02-ACCEPT-0930`. The fleet treats a pending peer acceptance as an open reason (the
widget constructor page stayed REOPENED for the same reason until its section was accepted). Re-status once that
review lands.

**A-drift checked.** `adrift_report.py` after the two re-statuses shows no new refused family row: still 10, none caused
by these pages.

*(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-dd-02-restatus-0930/REVIEW.md): corrections 1-3 are applied on the two pages (typed list §10; section addressing §8 and the type-store attribution); the status words stay DOCUMENTED. The optional front-matter `external_production.status` update is not applied, because it is front matter and optional.)*
