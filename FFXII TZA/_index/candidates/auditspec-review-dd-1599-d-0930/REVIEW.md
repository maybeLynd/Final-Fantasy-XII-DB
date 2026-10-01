# SWE2-AUDIT-SPEC review of OPUS's DD re-status batch 4, folders 15-99 (d39c8ccbd): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: OPUS's
`d39c8ccbd` ([batch4.md](../opus-dd-1599-0930/batch4.md)). It moves three pages PARTIAL → DOCUMENTED:
- `99-Unresolved-Residual/the-widget-tree-draw-pass.md`;
- `18-Audio/which-variation-of-a-sound-you-hear.md`;
- `18-Audio/sqex-sd-sound-driver-architecture.md`.

Measured at HEAD `b58c633f7`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-DD-1599-D-0930 | [batch4.md](../opus-dd-1599-0930/batch4.md) | `d39c8ccbd` | ACCEPT |

The re-status is a currency change with no new measurement. The diff touches only the three status lines,
`last_reviewed`, a G-19 pointer (§5) and a note on §6's "Provisional" label. The review checks four things:
- every row the pages name is closed at HEAD;
- no box is open;
- each row the new status lines lean on has a tracked, non-author review;
- the new words say no more than those rows.

**Rows.**
- *Widget tree draw pass.* SD-101 and SD-102 are ANSWERED, with reviews
  [auditspec-review-sd101-0930](../auditspec-review-sd101-0930/REVIEW.md) (ACCEPT) and
  [auditspec-review-sd102-0930](../auditspec-review-sd102-0930/REVIEW.md) (ACCEPT-WITH-NARROWING).
- *Which variation.* G-2 is SUPERSEDED, and its pointer is kept. G-14, G-18, UQ-250, UQ-251, UQ-259 and UQ-262 are
  ANSWERED. SD-24 is ANSWERED by SWE2-DATA and reviewed by SWE2-AUDIT-SEM in `auditsem-review-dd-leftovers-0930`.
- *Driver architecture.* G-1, G-3..G-5, G-7..G-9, G-13 and G-19 are ANSWERED, G-6 is WITHDRAWN and G-2 is SUPERSEDED.
  SD-20, SD-21 and SD-22 are ANSWERED, with reviews auditspec-review-sd20/21/22-0930 (ACCEPT, ACCEPT,
  ACCEPT-WITH-NARROWING).

**Boxes.** All three pages have 0 unticked boxes.

**Wording.**
- The status lines' one-clause summaries match the register cells. SD-101, for example, is "flag bit 24 is a
  per-subtree second-pass switch set by six screens".
- The §6 annotation claims only that the notes rest on §2a-§2e body reads and answered rows. It adds no fact.
- The two ACCEPT-WITH-NARROWING rows (SD-102, SD-22) are cited only as answered here. Their narrowings concern their own
  records' wording, and none changes what these status lines say.

**Correction wording:** none needed.
