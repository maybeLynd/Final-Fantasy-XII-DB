# Consumer-check record: the page-wait decrement runs in modes 3 and 7, not 5; 002AF340's return (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`

## What changed

For `DATA-REQ-FABLE-UQ173-MODE5-AND-002AF340-LINES-0930`.

1. **The page-wait decrement.** UQ-173's 2026-09-18 narrowing, and the same sentence on the numeric-formatting page,
   said the reveal stepper `002ABF70` decrements the page-wait count `+0x88` in mode 5. FABLE re-read the dispatch.
   The jump table `002AC1B4` is indexed directly by the mode byte `+0xB0` (`002ABF79`–`002ABF9D`). It sends modes 3
   and 7 to `002ABF9F` and `002AC18B`, and both arms start `movzx eax, word ptr [rbx + 0x88]`. `002ABF9F` then does
   `sub ax, 1` and stores the result back. The mode-5 arm `002ABFFC` reads `+0x9C` instead. The phrase is struck and
   corrected in the register row. The numeric-formatting page's copy is routed (see Consumers), because that page
   carries another lane's uncommitted edits.
2. **`002AF340`'s return.** It returns the number of characters laid out, up to the stop string, or -1 (SWE2-DATA,
   `measure_checks.py`, 71af93479). The glyph-quads page gains a dated narrowing. Nothing is struck there, because
   the function's inside is still only partly read.

## Consumers

- consumer: `_index/OPEN-QUESTIONS.md` row UQ-173: revised-here.
- consumer: `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md` (the same sentence): routed-to-board-note. The page carries a peer overlay (6 lines, uncommitted since 02:35), so it is corrected after that lane publishes.
- consumer: `99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md` L827: revised-here.
- consumer: `16-UI/Request-Router/ui-request-router.md` L696 ("what `002AF340` returns" not established):
  routed-to-board-note. The page carries another lane's uncommitted edits, so FABLE did not touch it. A board note
  asks that lane to fold in the narrowing.
- consumer: frozen copies under `_experiments/evidence/*/retained/` and `source-preimages/`: agrees. They are
  hash-pinned receipts, not live text.

## Regression

run: measure_checks.py at 71af93479 (SWE2-DATA, `_index/candidates/dd-data-3-0930/`, FAILS 0)
