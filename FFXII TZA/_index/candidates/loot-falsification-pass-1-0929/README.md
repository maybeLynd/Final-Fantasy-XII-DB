# Consumer check: falsification pass 1 on CONTRACT-loot-rolls-and-the-chain (OPUS, 2026-09-29)

corrects: 13-Rewards-Progression-Economy/CONTRACT-loot-rolls-and-the-chain.md (the draw-count bounds in sections 2, 4 and 12: CON-175)

## What was corrected

- **The orchestrator's draws are P + C + Q + E, from 0 to 13**, not "2 to 13":
  - P: the profile draw, only when `[022C3164] > 0`;
  - C: one chance draw per slot with an id;
  - Q: one quantity draw per kept slot;
  - E: the extras, 0-2.
- **An empty slot can draw.** A `0xFFFF` slot goes to the `+0xE64` override. When the override's index matches, the
  slot is kept as `0xFFFF` and a quantity is drawn. LC-7a's clear later zeroes that entry's quantity, so nothing drops,
  but the stream has moved.
- So section 12's all-empty kill draws 0, 1 or 2 times, not "at most once".
- The override's default value, and whether it can match in shipped play, is §14's open question and is not settled
  here.
- **Precision, not a correction:** LC-2's inline copy has one extra register move. The arithmetic and the writeback are
  identical.
- **What survives.**
  - LC-1's 17 / 9 / 8, on two instruments with linear-only 0, and the generator's 23 call sites in 15 functions, none
    of the seven inliners.
  - LC-3's three steps and the `% 100` constant.
  - LC-4's guards, and the three rolls that draw before any branch.
  - LC-5's single tick call site.
  - LC-6's rank default and the 20-byte accessor.
  - LC-7's fourteen pre-fill stores and bucket + 1.
  - §10's null-table skip.

## Current consumers

- consumer: [loot-drops-and-enemy-chain.md](../../../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md) states no
  draw-count bound; it agrees.
- consumer: [OPUS block 349](../s32-opus-replay-loot-rolls/README.md) measured 4-7 draws per kill on one foe with 4 non-empty
  slots. That is inside 0-13 and agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-175`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_loot.py` K1 and L4. They fail unless an empty slot's `je` at
`003181FC` reaches the override, a match stores the id and calls the quantity roll, and the chance, quantity and
profile rolls draw before any branch.

run: verified at 3b5a40685 (BROKEN 0), against the certified image `73461d08…`.
