# ShadowSettings01F82EA8: eight 4x4 float matrices, 0xD8 apart (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SEM.

[`shadow_matrices.py`](shadow_matrices.py) (STATIC, M1 / M2 / S, FAILS 0; S failed before the patch).

- **M1.** `001F0AD0` unrolls eight identical blocks. Each loads four 16-byte rows at `+0x1C0 + 0xD8*i` (i = 0..7).
- **M2.** It splits every row into float lanes (`shufps` 0x55 / 0xaa / 0xff, `movss` to globals), so each is
  `float[4][4]`.
- **The census agrees.** The four-seed census receipts (`../opus-shadow-settings-0b08/`) show no other access inside any
  of the eight matrices, and they reach no writer.

**Change.** Each of the eight `u8[84]` span rows becomes `matrixN float[4][4]` (64 bytes) plus a `u8[20]` DISCOVERED
remainder. The old row is kept verbatim as WAS.

**Not claimed: a 0xD8 element type.**
- Only these 64 bytes are read uniformly in every stride.
- The bytes after them are touched stride by stride.
- The eighth stride's tail holds the container's own named fields: `decayDistance` +0x830, `mapHeightMin` / `Max`,
  `cascadePartition0-2`.
- So 0xD8 is a spacing here, not a proven element size.

What the matrices transform is not claimed either.

**Run receipt.** Run verified at 68dc90f7c:
- `shadow_matrices.py` FAILS 0;
- `types_index.py --validate` 0 errors;
- `check_census_widths.py` 0 disagreements.
