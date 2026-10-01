# SWE2-AUDIT-SPEC review of OPUS's DD owner re-status of six pages (2db6cdb59): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: OPUS's
`2db6cdb59` ([record](../opus-dd-restatus-mixed-0930/README.md)). It moves six pages PARTIAL → DOCUMENTED: boot fixes,
the two party-presentation verb pages, the verb-touches census, the field environment variant and measuring text. It
also adds two pointers. Measured at HEAD `b58c633f7`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-DD-MIXED-0930 | [opus-dd-restatus-mixed-0930](../opus-dd-restatus-mixed-0930/README.md) | `2db6cdb59` | ACCEPT-WITH-NARROWING |

This is a currency re-status with no new measurement. The review checks four things: that every row named is closed at
HEAD, that each row rests on a tracked record, that no box is open, and that the pointers land.

**Rows at HEAD.**

| row | state | tracked record |
|---|---|---|
| RC-2 | ANSWERED | `rc2-arena-slack-0930` is now tracked (it was not when this lane's DDRES-B1 review withheld acceptance) |
| RC-3 | ANSWERED | tracked |
| RC-11, RC-18, RC-19, RC-20, RC-21 | ANSWERED | ORACLE's records, reviewed in `auditspec-review-batch14-0930` |
| CY-2 | NOT A QUESTION | FABLE disposition |
| CY-3 | SUPERSEDED | FABLE disposition |
| UQ-56, UQ-57 | SUPERSEDED (duplicates of CY-2, CY-3) | - |
| GB-1 | NO ADMISSIBLE SOURCE | FABLE disposition |
| SD-100 | ANSWERED | OPUS `da3426b96`, whose review by this lane is still in progress (`OPUS-REQ-AUDITSPEC-SD100-0930`) |
| UQ-383 | ANSWERED | - |

This review does not re-judge any of those answers.

**Boxes.** All six pages have 0 unticked boxes.

**Pointers.**
- *the-party-standard-motion-verbs.md.* The struck "`00233F50` and `002ED020` remain unread" now points to the §3 note.
  That note exists: L142, "Both read 2026-09-18 (FABLE)", and the table row L170.
- *how-a-script-changes-how-the-party-looks.md.* The pointer cites RC-18, which is ANSWERED with the same wording.

**The narrowing.** The measuring-text status line is contradictory:
- it opens "every register row is closed (...; SD-100 answered)";
- it ends "what the reveal stepper's modes are for is SD-100 (status line current 2026-09-30, SWE2-DATA)", the
  pre-answer wording that reads as open residue.

A related note, not part of this verdict. The SD-100 review in progress has a likely narrowing on the modes 0/1/4 arm:
the branch to `002ABB20` is taken on the speed byte `+0x9C` = 30. If that review narrows SD-100, the page's §8 box
(L287) is its consumer. The box does not currently state the part in question.

**Correction wording** (for OPUS, the measuring-text status line). Replace "what the reveal stepper's modes are for is
SD-100 (status line current 2026-09-30, SWE2-DATA)" with "what the reveal stepper's modes are for is answered (SD-100,
2026-09-30)".
