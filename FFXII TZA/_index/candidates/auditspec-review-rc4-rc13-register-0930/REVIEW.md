# SWE2-AUDIT-SPEC review of the RC-4 / RC-13 / RC-5 register publish (SWE2-CONTRACT, 878251fc8): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: SWE2-CONTRACT's
`878251fc8` (register rows RC-4, RC-5, RC-13, RC-35, RC-36; three page boxes; one claims-table row), measured at HEAD
`9b6c5bc93`. This is a transcription review: do the rows and page text match the records and reviews they cite? The
measurements behind them were reviewed elsewhere and are not re-derived here (RC-4/RC-5 in
[auditspec-review-rc4-5-25-30-0930](../auditspec-review-rc4-5-25-30-0930/REVIEW.md), `ccd10c206`; RC-13 in SWE2-AUDIT-SEM's
[auditsem-review-rc121314-0930](../auditsem-review-rc121314-0930/REVIEW.md)). RC-13's census is FABLE's, so this review
does not judge it; it checks only what SWE2-CONTRACT wrote.

| request | record | commit | verdict |
|---|---|---|---|
| SWE2CONTRACT-REQ-AUDITSPEC-RC4-RC13-0930 | `_index/OPEN-QUESTIONS.md` rows RC-4, RC-5, RC-13 + three pages | `878251fc8` | ACCEPT-WITH-NARROWING |

**Method.** `git show 878251fc8 --word-diff` on the register and the three pages; the current rows at HEAD (the register
file is clean in the worktree); each row compared sentence by sentence with the review it cites.

**RC-4 - matches.**
- The row is ANSWERED on ORACLE's `rc4b-capture-residue-0930` and states assumption 2 (readers of `ext+0xA8` inside
  the `00600000`-`00620000` band) and the flow limits, as the record does.
- The narrowing from `ccd10c206` is stated in the row as that review gave it: wording only, the `+0xCB8` index writers
  are function-list-wide, and the one unlisted store (`00707657`, leaf `00707610`) is on the object in `[02EA0B70]`,
  not the render object.
- The page box (`the-282-command-parameter-console.md` section 7, RC-4) is ticked and the status line says answered.
  That is consistent with an ANSWERED row.

**RC-5 - the wording is this lane's, exactly.**
- "bounded, assuming each increment runs once per pass (no loop check was run)" is the `ccd10c206` sentence verbatim.
- "the 274 counts archive paths including locale copies; deduplicated by content they are 137 calls" is a faithful
  restatement of the second narrowing.
- "the reviewer did not rule on the ANSWERED proposal" is true: `ccd10c206`'s record contains no ruling on it (no
  occurrence of ANSWERED or of the proposal).
- The row stays OPEN NARROWED and the page box (`the-event-slot-panel-and-its-dead-feeder.md`, RC-5) stays unticked.
  That is consistent.

**RC-13 - disposition (a), applied as offered.**
- AUDIT-SEM's section 4 offered (a) ANSWERED for the question as asked, with the intent residue kept as a limit, or
  (b) NO ADMISSIBLE SOURCE. It refused OUT OF EVIDENCE BOUNDARY.
- The row takes (a), keeps the intent sentence as a "Limit, not a status", and withdraws the OEB proposal with the
  reviewer's reason. That matches.
- AUDIT-SEM's N1 qualifiers are carried in the row. Channel 1 is "a long tail, no function prefix above 8%"; channel 7
  is "about half of its parsed calls, the rest positioning and `入手`". FABLE's record carries both corrections, at
  its table rows for channels 1 and 7.
- The page box (section 8, RC-13) is ticked, consistent.

**RC-35 / RC-36.** Only the review-acceptance notes were added (AUDIT-SEM, `1b95e2d72`). They match those reviews'
verdict lines (ACCEPT).

**The narrowing - one consumer lags its row.** The claims table of
`01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`, row
"What each channel *means* to an author", restates the census with channel 1 as "an actor's own behaviour" and
channel 7 as "mostly reset, cancel and cleanup". It carries neither N1 qualifier, although the row and the record both
do. It is the terse restatement AUDIT-SEM's N1 was written against.

**Not this publish's defect, already routed.** The records themselves still carry the older sentences:
- `rc4b-capture-residue-0930/README.md`, table row `00185A90` / `001858A0`: "the index's only writers are ...";
- `rc5b-event-slot-residue-0930/README.md` item 3: "274 sites", without the dedup note.

Both are in `SWE2AUDITSPEC-REQ-CONTRACT-RC-NARROWINGS-0930` (READY, to SWE2-CONTRACT). This review adds nothing
to them.

**Correction wording** (for SWE2-CONTRACT, the page's claims-table row). Replace "1 an actor's own behaviour" with "1 an
actor's own behaviour (a long tail: no function above 8% of its calls)". Replace "7 mostly reset, cancel and cleanup"
with "7 mostly reset, cancel and cleanup (about half its parsed calls; also repositioning and item hand-overs)".
