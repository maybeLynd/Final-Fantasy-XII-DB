# CPostEffect +0x7A4: six 4x4 float matrices, not 45 integer rows (OPUS, 2026-09-28)

**What was wrong.** CPostEffect `+0x7A0..+0x92F` sat in the store as 56 rows from the census re-cut: `u64`, `uint32`
and "overlapping widths [4, 8]" spans. Two instruction patterns made those widths, and neither is a field access:
- **The reset's zero-fill.** `0070FF10` clears each matrix with six qword stores, and those qwords straddle float cells.
  For example, `+0x7B0` is row 0, column 3 together with row 1, column 0.
- **A 64-byte assignment done in dwords** (`007145E0`).

The `uint32` rows at `+0x7CC`, `+0x7E0`, `+0x80C` and so on were diagonal float cells holding `1.0f`.

**Check:** [`cpe_matrix_array.py`](cpe_matrix_array.py) is STATIC, refuses any image but the certified one, and ends
FAILS 0.

| check | observation |
|---|---|
| R1 | `0070FF10(this, index)` resets matrix `index` to identity, or all six when `index == -2` (a loop `rcx = 0..5`, stride 0x40 from `+0x7A4`). Each reset is six qword zero-fills plus `1.0f` at the diagonal cells `+0x00`, `+0x14`, `+0x28` and `+0x3C`, and it clears byte `+0x924 + index`. |
| R2 | `006FB810` handles matrices 0 and 1 by 16-byte rows: 8 `movups` reads (`+0x7A4..+0x814`), identity diagonals, then 8 `movups` writes. This is the 4x4 row structure, seen from a second, independent body. |
| R3 | The per-matrix bytes are compared one at a time: `006FE984` (`+0x924`), `006FE990` (`+0x925`), `006F723B` (`+0x926`) and `006F724E` (`+0x927`). |
| N | `007145E0` copies 64 bytes as 16 dwords, and its callers pass matrix-aligned destinations in their own objects (`+0x5D4` in the `+0x210` sub-object is `+0x7E4`). Its 4-byte "fields" are an assignment, not a layout. |
| S | The store now has `+0x7A0` `float`, `+0x7A4` `float[6][4][4]` (384 B), `+0x924` `u8[6]`, and nothing starting inside them. S FAILED before the patch. |

**The new rows.** 56 rows became 5. Every absorbed row's name and old type is kept verbatim in the matrix row's evidence
cell.
- `+0x7A0` `float`: read by `movss`. The census had joined it with the first cell of the array.
- `+0x7A4` `matrices7A4` `float[6][4][4]`.
- `+0x924` `matrixFlags924` `u8[6]`.
- The remainder of the old `mixed928`, both DISCOVERED:
  - `+0x92A` `u8[2]`, with no access;
  - `+0x92C` `u8[4]`, a 4-byte write and the head of 16-byte reads that continue into `+0x930`.

**Kept apart.**
- **Physical access:** rows of 16 bytes, float diagonal constants, qword fills and a dword copy.
- **Representation:** `float[6][4][4]` and `u8[6]`.
- **Meaning:** NOT claimed, neither what the matrices transform nor what a set byte means.

**Regressions, at 9723be78d.**
- `types_index.py --validate`: 795 types, 8260 fields, 0 errors, 0 gaps.
- `check_census_widths.py`: 0 disagreements.
- `check_type_refs.py`: 0 dangling.
- `cpe_recut_check.py`: FAILS 0 (212 re-cut rows still match; none DISCOVERED).

## Part 2 (OPUS, 2026-09-28, later): a seventh matrix at +0x92C, and the bytes are enables

**Check:** [`cpe_matrix_part2.py`](cpe_matrix_part2.py), with checks P1, P2, P3 and S, ends FAILS 0. Part 1's check is
left unchanged.

| check | observation |
|---|---|
| P1 | `0070AED0(this, nine floats)` writes a 4x4 float matrix at `+0x92C`. It stores the 3x3 linear part **column by column** from its arguments: `xmm1` / `xmm2` / `xmm3` go to `+0x92C` / `+0x93C` / `+0x94C`, and the stack floats fill columns 1 and 2. It zeroes column 3 and row 3 and stores `1.0f` at `+0x968`. |
| P2 | `006FE7F0` reads it as four 16-byte rows into `xmm8..xmm11`. |
| P3 | The per-matrix bytes are **enables**. In `006FE7F0`, a zero byte at `+0x924` replaces matrix 0's address with null, and a non-zero byte at `+0x925` selects matrix 1's address. The reset clears the byte, so a reset matrix is identity and disabled. What enabling does downstream is not claimed. |
| S | The store has `+0x92C` `float[4][4]`, with nothing inside it, and the old 16-byte `mixed968` split at `+0x96C`. S FAILED before the patch. |

**The new rows.** 9 rows became 6:
- `+0x92C` `float[4][4]`;
- `+0x96C` and `+0x970` `uint32`: `006FE7F0` compares the two and calls `006E2C30` / `006E3000` when they
  differ;
- `+0x974` and `+0x975` `u8`;
- `+0x976` `u8[2]`, DISCOVERED.

The `+0x924` row gains the enable behaviour.

**Regressions, at 4933c61e6.**
- `types_index.py --validate`: 8257 fields, 0 errors, 0 gaps.
- `check_census_widths.py`: 0 disagreements.
- `check_type_refs.py`: 0 dangling.
- `cpe_matrix_array.py`: FAILS 0.
- `cpe_recut_check.py`: FAILS 0.
