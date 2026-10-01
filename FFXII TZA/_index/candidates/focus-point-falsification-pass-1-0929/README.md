# Consumer check: falsification pass 1 on the-focus-point-of-a-character (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Character-Render-Records/the-focus-point-of-a-character.md (the SWE2-EC7-83 note on 0046FAA0: CON-178)

## What was corrected

- **The appended SWE2-EC7-83 note gave the ease sampler the wrong globals and a word-width count.** `0046FAA0` loads a
  dword count from `01F2053C` (60) and indexes the table at `01F20C80` (0.0097 .. 1.0). That is exactly what the page's
  own section 3 says.
- `01EFAB4C` and `01EFAC80` are neither sampler's; the sibling `0046FBB0` reads `01F20538` / `01F20AA0`.
- **What survives.**
  - Section 7's sizes.
  - The `@FRM` chunk lookup, `[rec + 0x30] + 0x10`, and its `+0xC` twin.
  - The version-3 bone selection.
  - The `+0x670` / `+0x66C` / `+0x6A8` stores and the `8 * [01DFE0B4]` reload.
  - `003E6070`'s zero return.
  - The `+0x290` bit-1 gate in `004288E0`.

## Current consumers

- consumer: `_index/ADDRESS-INDEX.md` lists the page for `0046FAA0` and quotes no table address; it needs no change.
- consumer: the actor-manager field map cites `01EFAC80` for a different structure (a three-address group), not as an
  ease table; it agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-178`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_focus_point.py` K1. It fails unless `0046FAA0`'s only
RIP-relative operands are `01F2053C` (a dword load) and `01F20C80`.

run: verified at 61a31d1a2 (BROKEN 0, exit 0), against the certified image `73461d08…`.
