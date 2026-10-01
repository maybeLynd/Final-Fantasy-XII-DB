# Consumer check: falsification pass 1 on fte-fct-texture-colour-tables (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md (the table-A/B bullet: CON-182)

## What was corrected

- **Table B's row multiplier is `s8[target + 0xB9]`, not a count.** `0053AB9F` loads it, `0053B4BB` multiplies
  `byte[@FOR + 0x32]` by it, and `0053B4E2` adds the product to table A's byte.
- `00504F00` stamps `+0xB9` from its argument when `0 <= v < byte[@FOR + 0x33]`, and to 0 otherwise.
- **What survives.**
  - The `@FCT` consumer's bounds, resource slots and 20-slot map.
  - The page selection through `+0xBA` and its 7-byte setter.
  - The builder's two calls and its private frame offsets.
  - The `+0xB8` key selection.
  - Table A's triplet addressing.
  - The seed list and the pair de-duplication.
  - The record reader and the PSM packing.
  - The 256-slot cache and the teardown walks.
- **Precision, not corrected:** the setter has three call sites, `00428D3C` and `00428D82` (both in `00428CD0`) and
  `0042E520`. The page's "`00428D3C`, plus `00428CD0` twice" counts one of them twice.

## Current consumers

- consumer: `17-Presentation-Rendering/Model-And-Motion-Formats/fdm-and-for-entries.md` (SWE2-DATA pass 16) writes
  `bIdx = byte[tableA + 3·sel + part] + byte[@FOR+0x32]·variant`. That is the right placement; its "variant" is the
  `+0xB9` selector, which the same page describes two paragraphs later. It agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-182`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_fte_fct.py` X5 and X6. X5 fails unless `0053AB9F` loads
`[rdx + 0xB9]` into the frame slot that `0053B4BB` multiplies. X6 fails unless `00504F00` clamps `+0xB9` by
`@FOR + 0x33`.

run: verified at 098204632 (BROKEN 0, exit 0), against the certified image `73461d08…`.
