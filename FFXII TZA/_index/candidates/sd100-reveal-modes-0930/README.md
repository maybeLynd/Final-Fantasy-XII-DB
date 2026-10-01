# SD-100: the reveal stepper's eight modes, and who sets each (OPUS, 2026-09-30)

Register row SD-100 was registered by SWE2-DATA ([measuring-text-by-drawing-it-with-the-output-off.md](../../../99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md)
section 7). It asks what the reveal stepper `002ABF70`'s modes are for: which writer sets each mode byte of the
window's `+0xB0`, and what the player sees in each.

This record is static. The checker is `sd100_modes.py` (output `sd100_modes.out`, `FAILS 0`). It includes an
image-wide census of byte stores to `+0xB0` over the `pe` module's 38,161 bodies.

## What each mode does (OPUS)

The stepper dispatches on the low byte of `+0xB0` through the table `002AC1B4` (M1). The terms used below:
- `+0x90` is the reveal target: glyphs revealed so far.
- `+0xA0` is the step, in glyphs.
- `+0x9C` is the speed.
- `+0x9B` is an accumulator.
- `+0x88` is a tick count.

| mode | arm | what it does (M2–M4, M6) | on screen |
|---|---|---|---|
| 0, 1, 4 | `002AC06B` | ~~`+0x9B += +0x9C`; each 30 steps `+0x90` by `+0xA0`. When a line is full, it pages through `002ABB20`: automatically when the step `+0xA0` > 1, otherwise only when `00248F20` answers 1. It then restores the `0x7D00` budget.~~ `+0x9B += +0x9C`. When the speed `+0x9C` is 30, it scrolls through `002ABB20`, which advances the head `+0x8C` to the next line or `#` page wait, and snaps `+0x90` to the head with no lag. It does this when `+0xA0` > 1, or when `00248F20` answers 1 (the mode query `00229EA0` is not 2). Otherwise, each time `+0x9B` reaches 30, the head `+0x8C` advances by `+0xA0`, the lag `+0x9D` moves by `+0xA0` toward `+0x9E`, and `+0x90` steps by `+0xA0` while it is at most `+0x8C - +0x9D`. `0x7D00` is an upper clamp on `+0x8C`. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 1)* | text types out at the authored speed and pages |
| 2 | `002AC04F` | counts the fade word `+0x5A` down (bit 22 zeroes it), then does the same as 0/1/4 | a fade, then typing |
| 3 | `002ABF9F` | counts `+0x88` down **and keeps stepping** `+0x90` by `+0xA0` every tick. At zero: `+0x9B = 30` and mode 0. `+0x90` steps only while it is below the head `+0x8C`, which this arm never advances; it exits at once if `+0x88` is already 0 *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 2)* | ~~a timed stretch that types a step per tick, then normal typing~~ catches the reveal up to the head at a step per tick, then normal typing *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 2)* |
| 5 | `002ABFFC` | rate stepping only: `+0x9B += +0x9C`, a step each 30. **`+0x88` is never read**. `+0x90` steps only while it is below the head `+0x8C`, which this arm never advances *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 2)* | ~~typing at the authored rate, with no paging~~ catches the reveal up to the head at the rate, with no paging *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 2)* |
| 6 | `002AC1AB` | nothing (the common exit) | held: the text does not advance |
| 7 | `002AC18B` | counts `+0x88` down **without stepping**, then mode 0 | a frozen pause of `+0x88` ticks, then typing resumes |

## Who sets each mode (OPUS, M5)

| mode | writers |
|---|---|
| 0 | the base fill `002AC1E0`, the kind-0 builder `002B3D50`, the relayout `002A5CC0`, and the stepper itself when a count ends (`002ABFC3`, `002AC1A4`); the pager `002A9980` (`002A9A27`, `dil` = 0 after `002A9A00 xor edi, edi`), the setter `002B3950` (`002B3963`, `al` = 0 after `002B395A xor eax, eax`) and `002A6F80` (`002A6FB3`, through window `+0x180`) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 3)* |
| 1 | the markup parser `002A8C50`: at entry when `+0xC0` = 1 (`002A8D2B`), and at its end when the mode predicate `001EDDA0` answers (`002A9923`); the message-window procedure `002A6190` (`002A6606`, through window `+0x180`, the old mode saved at `+0x181`) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 3)* |
| 2 | `002A8C50` (`002A989E`, after setting up `+0x54` / `+0x58` through `002B2CA0` / `002B2CE0`; bit 19 set) |
| 3 | `002A8C50` (`002A9428`, with `+0x9B` = 1 and a tick count of 30 × a payload byte) |
| 4 | `002A8C50` (`002A9193`, bit 19 set) and `002B0280` (`002B199A`); `002AC5F0` on its stack copy of the element (`002ADBC2`, `(dword & 0xFFF7FF04) or 4`) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 3; the review's bitwise OR is written as the word, since a table cell carries no pipe)* |
| 5 | `002A8C50` (`002A97EA`, and `002A98B5` with bits 19 and 26), and the `#` escape in `002AC5F0` (`002AD225`, bits 19 and 26) |
| 6 | the message-window procedure `002A6190` (`002A67DB`) and the pager `002A9980` (`002A9AA2`, `002A9D1C`) |
| 7 | `002A3250` (`002A3556`), right after it builds its element with `002B3D50` |
| ~~variable~~ | ~~the pager `002A9980` (`002A9A27`, from `dil`) and the setter `002B3950` (`002B3963`, from `al`)~~ both are mode-0 writers (row 0) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 3: the row is deleted)* |
| restore | `002A5F40` (`002A5FE8`) swaps the byte saved at `+0x181` back in, unless the mode is 2 or 4 *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 3)* |

The 007Exxxx byte stores at `+0xB0` belong to the audio code's own structure and are excluded.

## A contradiction this confirms

[the-text-control-code-language.md](../../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md)
(the UQ-178 narrowing, 2026-09-18) calls `002ABF9F` "the mode-5 arm" that decrements `+0x88`. The table puts
`002ABF9F` at **mode 3**, and the mode-5 arm `002ABFFC` never reads `+0x88`. So the `#` escape, which writes mode 5,
does not start a `+0x88` countdown in the stepper. SWE2-AUDIT-SEM's DD-3 review (`e89b4567b`) found the same and
routed it as UQ-173. This record adds the bytes to that routing and does not edit the page.

## Limits (OPUS)

- **Triggers in the parser.** Which control code or markup reaches each `002A8C50` store is read at the store's own
  site, not traced back through the whole parser.
- ~~**`002B3950` and the pager's variable store** set the mode from a value their callers supply. The callers are not
  traced.~~ The writers are complete for stores addressed as `[element + 0xB0]` (any width or base, image-wide)
  and through the window's `+0xD0` element and the stack elements of `002A5460`, `002B3050`, `002B5390`, `002A1B00`
  and `002AC5F0` (SWE2-AUDIT-SPEC review). Elements reached through shifted pointers, `memcpy` copies, and the
  elements handed to `002A8C50` / `002A9980` by pointer are not swept. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd100-0930/REVIEW.md) item 4)*
- **`00248F20`**, the page-advance condition, is not named.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
