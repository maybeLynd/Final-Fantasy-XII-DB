# Consumer check: falsification pass 1 on ftr-node-table (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md (section 2's field table, section 3, the section-1 count: CON-181)

## What was corrected

- **`+0x80` / `+0x84` / `+0x94` are dword arena offsets, and `+0x80` is not the entry lookup.** `0020E620` subtracts the
  arena base `[01F83530]`. The `00409A30` lookup is stored at `+0x1C`. `+0x80` is the offset of the core block the
  caller passes as the fifth argument, `+0x84` the offset after `003AB7F0`'s live resolution, `+0x94` the offset of
  `core + coreBytes`.
- **Only kind 0 runs the `0x4C` loop.** Any other non-2 kind branches to `00372E84`, builds no records and only fills
  the override slots. Every shipped entry is kind 2, so both arms stay dead in shipped data.
- **55, not 71.** 55 listed functions multiply an index by `0x290`. The other 16 in `imul290.txt` hold `0x290` as a
  stack frame (12), a size or an offset.
- **Added, not corrected:** flag bits 31 and 22 each skip one more u16 in the rich arm. The census says whether shipped
  records set them.
- **What survives.**
  - The sizer's formula.
  - `+0x88`, `+0x8A`, `+0x90` and `+0xB0` with its `0x30`-stride name table.
  - The flag table's listed bits.
  - `00373DC0`'s identities and cleared links.
  - The parent / first-child / next-sibling threading.
  - The FCP tail copy.
  - `003E1C50`'s `0x740` index, rebases and helpers.

## Current consumers

- consumer: `_index/candidates/uq218-cm-entry-residues/` (`notes.md` lines 109-110, `ftr.tsv` row 6, and `imul290.txt`)
  is FABLE's evidence record and keeps its original text. Routed-to-FABLE: the count note should read 55 imul strides
  of 71 listed.
- consumer: `17-Presentation-Rendering/Model-And-Motion-Formats/fdm-and-for-entries.md` states the slot array address as
  `core + count*0x292 + 2*ordinal`, which holds once the core is resolved from `+0x84`; it agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-181`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_ftr_node_table.py` N3, N8 and N10. Each row fails unless:
- N3: `+0x1C` takes the `00409A30` result and `+0x80` / `+0x84` / `+0x94` take `0020E620` results;
- N8: kind 0 and the other non-2 kinds branch to different targets;
- N10: exactly 55 listed bodies carry an `imul` by `0x290`, all inside the 71-row list.

run: verified at 56feea579 (BROKEN 0, exit 0), against the certified image `73461d08…`.
