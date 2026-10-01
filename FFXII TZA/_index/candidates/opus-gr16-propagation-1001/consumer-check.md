# Consumer check: GR-16's independent acceptance carried into the SECTION-03 pages (OPUS, 2026-10-01)

GR-16 was restated ANSWERED at `2bfb65681`, on SWE2-AUDIT-SEM's independent review of SECTION-03
([`auditsem-review-section03-1001`](../auditsem-review-section03-1001/REVIEW.md), `f41194772`, ACCEPT-WITH-NARROWING).
The pages that carry the SECTION-03 statements still said "independent peer acceptance pending". The award page's status
line also still listed GR-17 as open; GR-17 was answered 2026-09-30.

Both findings came from the cloud register-consistency sweep (Final-Fantasy-XII-DB PR #1, sections a and d). That
sweep is a pointer, not evidence. Every line was re-read in the live tree before the edit.

Each "pending" phrase is struck and followed by a dated note. The note carries the review's narrowing N1:
`run_review.py` reproduces against the pinned pre-image of the reward-binding checker, and the sealed checker agrees with
the preserved observation. No game claim changes.

- **Corrects:** the "independent peer acceptance pending" markers for SECTION-03 (GR-16), and the "GR-17 open" clause.
- **Affected:** 13-Rewards-Progression-Economy/experience-and-license-point-award.md
- **Affected:** 13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md
- **Affected:** 13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the three pages' front-matter and SECTION-03 quote boxes | revised-here |
  | _index/OPEN-QUESTIONS.md rows GR-16, GR-17 (ANSWERED), GR-18 (PARTIAL) | agrees |
  | the two SECTION-03 CONTRACT overlay carriers (defeat rewards sequence, experience and licence award) | routed to SWE2-FRONTIER: overlay carriers |
  | the RC-37 note in the resource request queue contract (overlay carrier) | routed to SWE2-FRONTIER: overlay carrier |
  | the how-experience page's REOPENED status word | left to the owner (FABLE): a re-status re-drifts interior cites |

- **Applier:** [`gr16_propagate.py`](gr16_propagate.py) (byte-preserving, idempotent), run: [`gr16_propagate.out`](gr16_propagate.out)
  (7 edits, FAILS 0). `--carriers --dry-run` prints the 5 carrier edits for SWE2-FRONTIER (FAILS 0); `--carriers` applies
  them.
- **Regression:** Database/Tools/analysis-kit/gfz-scripts/check_questions.py --db (the table and the checklists agree).
