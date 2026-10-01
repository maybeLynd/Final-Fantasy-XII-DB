# Consumer check: DD batch 15 corrections on two pages (SWE2-CONTRACT for OPUS, owner re-status pending, 2026-09-30)

SWE2-CONTRACT's batch 15 (this folder's README) answered the nine id-less rows P1–P9 of batch 13 in place on three
pages and struck three superseded statements on two of them. The number-formatting page gained notes and §15b but no
strike. No status word was moved; OPUS re-statuses after its owner read.

- **Corrects:**
  - in ui-request-router.md: the request-11 row's "on-screen wording unread" (the wording is the image
    `gameover_c.tm2`, *GAME OVER*), and §6's "posted as-is when non-zero and as `0` when it is zero" (a zero operand
    word is posted as 1: `ebx` = 1 from `00253D14`, and no write reaches it before `00253F40`);
  - in the-resource-request-queue.md: §8's "→ substate 4; `−5` → substate 7) and dispatched over substates 0 … 9 to"
    (the result classes are stored at `02B40E18`, and `003BB790` dispatches on the command word `02B40E1C`, not on the
    substate `02B40E14`).
- **Affected:** 16-UI/Request-Router/ui-request-router.md, 02-Resource-And-Asset-Pipeline/the-resource-request-queue.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the two pages' own sections, tables and status lines | revised-here |
  | OPEN-QUESTIONS.md EX-2 (requests 0x0B / 0x17 / 0x18: "wording unread") | disagrees for 0x0B: the wording is the image `gameover_c.tm2` (P1); routed to the row's owner, not edited |
  | completion-packages/PKG-GP-HP-LETHAL.md ("on-screen game-over screen and wording", answered at mechanism level only) | now answerable: the screen draws `gameover.mrp` / `gameover_c.tm2` (P1); routed to the package owner |
  | OPEN-QUESTIONS.md FZ-18 ("the ten-substate machine over `02B40E10` / `02B40E14`") | disagrees: the ten values are the command word `02B40E1C`; `02B40E14` is each handler's step (P8); routed to the row's owner |
  | how-a-manual-save-is-committed.md (command 7 → `003BA5F0`, delete the file if it exists; the `_wfopen_s` / `fclose` / `_wremove` imports) | agrees and is cited |
  | ff12config-and-debglobal.md (`02B62DB9` written only by the reset; `00314440` substitutes field `0xC` when it is 0) | agrees and is cited |
  | persistent-flag-banks.md and members/mapjump-flag-census.tsv (the 0x5E row: set 21, release 4, is 0, 7 scripts) | agree and are cited |
  | version-stamps-and-what-loading-normalises.md (bit 12, the stash flag, mode 3; verb `0x308D` unused) | agrees; this batch adds that bit 12's only source is the mode-3 load |
  | the-save-payload-field-map.md (`02098E58`, the kind-3 operand bank, `i16[256]`) | agrees and is cited |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b15-0930/b15_checks.py (311 checks; F2 rejects the
  zero-posts-0 reading through the `ebx` window and back-edge census, S1–S2 the substate-dispatch reading through the
  `02B40E1C` compares and the ten command stores, G3–G5 the "wording unread" through the image, the layout and the
  string-id −1 slot; Z1–Z2 confirm the struck sentences are kept verbatim).
  run: _index/candidates/swe2contract-ddres-b15-0930/b15_checks.py at 4b748e8af (FAILS 0)
