# Consumer check: falsification pass 1 on CONTRACT-which-generator-serves-which-roll (OPUS, 2026-09-29)

corrects: 21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md (I5: the graphics MT's index cells are the generator instance's, reset by the twist; the census bound +0x9C4 -> +0x9C0)

## What was corrected

- **I5's ownership claim.** The page and `CON-155` said two things:
  - the two cells above the graphics-noise MT array (`01F7FFC0`, the 8-byte cursor; `01F7FFC8`, the remaining count) are
    the consumer's;
  - neither generator routine touches them, because `0018EE20` has no operand at or above `+0x9A0`.

  Both are false. `0018EE20` opens `mov r10, rcx` and ends `mov dword ptr [r10 + 0x9c8], 0x270` (`0018EECD`) and
  `mov qword ptr [r10 + 0x9c0], r10` (`0018EED8`), so every twist resets the count to 624 and the cursor to the array's
  start. The cells are the generator instance's index, kept as a pointer and a count. The census that made the claim
  counted RIP-relative operands only, and the twist addresses its instance through `rcx`.
- **What survives.** The widths and kinds (`u32*` at `+0x9C0`, `u32` at `+0x9C8`). And, for a different reason,
  `CON-155`'s conclusion that `Mt19937State` must not declare one `u32` index field for both instances: the gameplay
  instance's index is a `u32` at `+0x9C0`, so the layouts differ.
- **The census bound.** `+0x9C4` is the type's extent and contains `01F7FFC0`; the 624-dword array ends at `+0x9C0`.

## Current consumers

- consumer: `_index/CONTRADICTIONS.tsv`: revised-here. `CON-157` records the correction, and `CON-155`'s correction cell
  points to it; its history is kept.
- consumer: `_types/types.tsv` rows `GraphicsNoiseDrawCursor` and `GraphicsNoiseRefillCount`: revised-here.
  - Ownership is corrected in the instance cell.
  - The access census now names the twist's register-relative write.
  - The refill row's "NOT CLAIMED: the value the twist leaves behind" is answered: 624.
- consumer: `_types/fields.tsv` rows `Mt19937State +0x9C0` and `GraphicsNoiseDrawCursor +0x0`: revised-here.
- consumer: [which-roll-is-on-which-generator.md](../../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) agrees.
  It carries no claim about the graphics MT's index cells.
- consumer: [rng-streams.md](../../../21-RNG-And-Determinism/rng-streams.md) agrees. It calls `01F7FFC0` / `01F7FFC8` "index
  words" and makes no ownership claim.
- consumer: [EXP-144](../../../_experiments/EXP-144-s46-generator-routing-exec.md) agrees. Its execution recorded the consumer's
  cursor and count, and a first draw that re-twists before consuming index 0, which is the twist's reset in action.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_which_generator.py`, checks W0-W11. W11 decodes `0018EE20` and
fails if the twist stops resetting both cells, which rejects the old claim. W8 fails on any third toucher of the two cells,
or on a reference inside the 0x9C0-byte array.

run: verified at 7393cec76 (BROKEN 0), against the certified image `73461d08…`.
