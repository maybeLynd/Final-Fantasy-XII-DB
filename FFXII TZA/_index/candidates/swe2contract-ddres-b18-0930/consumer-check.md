# Consumer check: DD batch 18 correction on the lifetime evidence note (SWE2-CONTRACT for OPUS, owner re-status pending, 2026-10-01)

SWE2-CONTRACT's batch 18 (this folder's README) brought the note's Limits section current and gave every remaining
open-residue sentence in sections 1–20 a dated pointer. One statement is struck, in Limits item 7. No status word was
moved; OPUS re-statuses after its owner read.

- **Corrects:** in authored-reference-lifetime-evidence.md, Limits item 7's bullet "**Register: SD-166** still reads OPEN
  at HEAD. The row has not yet been updated with that answer, and that update is the register owner's. Until then this
  note stays PARTIAL on it." The row is ANSWERED at HEAD (restated by SWE2-DATA on OPUS's record `sd166-arena-7-0930`,
  `06c849caf`), so the note no longer stays PARTIAL on arena 7.
- **Affected:** 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the note's own Limits items, sections 1–20 pointers and Findings | revised-here |
  | the note's front-matter status line ("the one row still open is arena 7's") | disagrees; untouched, because the status line is OPUS's; the README proposes its replacement |
  | where-the-games-memory-comes-from.md, line 160 ("is not established (`SD-166`, SWE2-DATA, 2026-09-30)") | disagrees: the row is ANSWERED; routed to the page's owner, untouched |
  | swe2contract-ddres-b7-0930 (README "SD-166 still reads OPEN at HEAD"; `b7_lifetime.py` R1 pins OPEN) | a dated receipt; rerun at HEAD its R1 fails on that row only. Untouched; b18 R1 pins the current state |
  | OPEN-QUESTIONS.md SD-166 | agrees (ANSWERED) and is cited |
  | the parent, the-resource-owner-from-copy-or-borrow-to-disposal.md | agrees; it does not name SD-166. Untouched |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b18-0930/b18_checks.py (99 checks; R1 rejects the
  struck reading through SD-166's lead word at HEAD, and Z1 confirms the struck sentence is kept verbatim with its
  correction note).
  run: _index/candidates/swe2contract-ddres-b18-0930/b18_checks.py at b0e414d9d (FAILS 0)
