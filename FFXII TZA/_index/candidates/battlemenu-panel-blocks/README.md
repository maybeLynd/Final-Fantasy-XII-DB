# BattleMenuPanelWidget3010 +0xC0..+0x1BF: four copied 0x40-byte blocks of one layout (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` BattleMenuPanelWidget3010, the 53 rows in `+0xC0..+0x1BF`. They repeated one pattern
block by block, with one width outlier (`+0xC0 u8[10]` against `+0x100 qword` plus `+0x108 word`), and carried 16
"unobserved" spans.

**Result** (`blocks.py`, B1–B4):
- **The copies (B1).** The handler `00276D30` copies a whole 0x40-byte template into each of `+0xC0`, `+0x100`,
  `+0x140` and `+0x180`.
- **The reader (B2).** `00276D30` passes a block's base to `0029F5D0`. That function reads `+0x0A` as a sign-extended
  word, `+0x0C..+0x12` as words, `+0x18` and `+0x20` as qwords, and `+0x39` as a byte.
- **The layout closes (B3).** The four blocks tile the span exactly; `+0x1C0` is a separate copy.
- **The width outlier was not a conflict.** `u8[10]` at `+0` is the coverage of the copy's wide moves. Block 1's
  census saw the finer qword plus word.

**Store change.**
- A new type, `BattleMenuPanelWidget3010Block` (0x40), with 14 rows.
- The parent gets one row, `blocks0C0 Block[4]`.
- `+0x0A` becomes `int16`: the reader sign-extends it, where the old rows had `uint16`.
- The 53 replaced rows are written verbatim to `replaced-block-rows.tsv` by the patch.

**Regression.** B4 fails on the pre-fix store and passes after `Tools/work/OPUS/bmpanel/patch_store.py`. On a copy,
`types_index.py --validate` reports 0 errors and 0 gaps, both alone and with the widget-header patch.

**Audit note.** This closes the structural debt behind `unobservedSpan0168`, the last row of the unobserved-row audit.
That row had already been dispositioned as an index misattribution: 002475D0 writes the panel's own widget header, and
the index counted the base twice. Here the span becomes the block's `unobservedSpan28`, still unobserved, on evidence
that does not depend on that hit.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` BattleMenuPanelWidget3010 `+0xC0..+0x1BF` | 53 rows → one block-array row; old rows in `replaced-block-rows.tsv` | revised-here |
| `_types/types.tsv` | block type added | revised-here |

Run receipt: executed at f0421e068 - `blocks.py` B1–B3 PASS; B4 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
