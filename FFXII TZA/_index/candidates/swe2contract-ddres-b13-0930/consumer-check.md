# Consumer check: DD batch 13 corrections on two pages (SWE2-CONTRACT for OPUS, owner re-status pending, 2026-09-30)

SWE2-CONTRACT's batch 13 (this folder's README) answered residue on three pages and struck the superseded statements on
two of them. The third page, the resource request queue, gained notes and a new §7b but no strike. No status word was
moved; OPUS re-statuses after its owner read.

- **Corrects:**
  - in ui-request-router.md: the request-24 row's "the widget builds the battle-menu selection state (`0035BC50`) —
    the reserve-swap prompt by mechanism" and its "on-screen wording unread"; §2's "who clears the word is unread",
    "Which screen reads those two fields is not followed here." and "are unread, and so is what it shows"; §2's
    "`L-13` stays open for that."; the key-address cell "posts the request word; unread"; and the 2026-09-02 pass's
    "which this page has not read";
  - in numeric-formatting-and-character-mapping.md: §2's "**`UQ-164` is `PARTIAL`, not answered.** What the block is
    *called* is still unknown,"; §6's "which is unread" (of `002A9F00`); and §10's "unread" in "(2,304 B, unread)".
- **Affected:** 16-UI/Request-Router/ui-request-router.md, 16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the two pages' own sections, tables and status lines | revised-here |
  | the-world-tick-and-the-field-frame.md (stage 3 / 18: "builds the battle-menu selection state (`0035BC50`) — the reserve-swap prompt, by mechanism") | disagrees: `0035BC50` is on the widget's request-3 arm; for 24 the widget shows text `0x86F` and posts request 2 (routed to its owner, not edited) |
  | battle-runtime-mode-ladder.md (`0035D080` registers `0035D6B0`; the `0035D6B0` / `0035D8D0` / `0035D980` / `0035DA80` quartet) | agrees |
  | CONTRACT-system-stop-registry.md (UI bodies call the close path `00252D90`) | agrees; this batch adds the two words it zeroes |
  | CONTRACT-per-frame-update-gate.md (group `0x2000` is `00290CF0`) | agrees and is cited |
  | OPEN-QUESTIONS.md L-13 (SUPERSEDED 2026-09-27) | agrees and is cited |
  | OPEN-QUESTIONS.md UQ-164 (CLOSED 2026-09-18) and text-draw-state-accesses.tsv | agree and are cited |
  | drawing-a-line-character-by-character.md and AC-9 (`002A9F00` read) | agree |
  | OPEN-QUESTIONS.md AC-9 ("fixed pitch per call, set by the callers") | a qualification, not a strike: true of the number formatter, not of the general loop `002A9F00`, which re-derives the step per glyph (N3); routed to the row's owner |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b13-0930/b13_checks.py (239 checks; R2 and R3
  reject the `0035BC50` reading for request 24, R1 the "unread" clearer, R8 the unfollowed reader, N7 the PARTIAL UQ-164).
  run: _index/candidates/swe2contract-ddres-b13-0930/b13_checks.py at 5f3b94f75 (FAILS 0)
