# OV-26, the format half: every shipped @FRP container keeps its offsets in bounds (FABLE, Claude Opus 5.5, 2026-09-29)

**Box (OV-26, `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md` §9):** "Establish authored
format bounds, shipped alignment/index guarantees, and allocation-failure behavior."

[`frp_bounds.py`](frp_bounds.py) runs V, O and M: FAILS 0 ([output](frp_bounds.out)). Data: every `.ca`, every `.cm` and
every `@FRP` block in all 4,392 `.mot` PKFL packs in the shipped VBF.

- **V.** All 14,139 containers have the `@FRP` magic and variant 0 or 1 (12,944 and 1,195). Each content length fits its
  block, and each offset table ends inside the content. The count reproduces the independent 2026-09-12 tag census exactly
  (3,164 `.ca` + 1,066 `.cm` + 9,909 `.mot` blocks).
- **O.** All 320,736 entries start inside their content: base + offset + 4 ≤ content length. Every id is `@F` plus two
  letters, the same eleven tags with the same counts as that census. Variant 1 carries 72,827 empty (zero) slots.
- **Alignment.** Every entry starts 16-byte aligned relative to its container:

  | largest alignment | entries |
  |---|---:|
  | 16 B | 241,616 |
  | 64 B | 60,795 |
  | 256 B | 16,238 |
  | 2 KB | 2,087 |

  None is less than 16-aligned.
- **M (sensitivity).** Read file-relative (the format's named trap), 319,349 of 320,736 ids fail the check. O discriminates
  the base it assumes.

**So, for the shipped data:** the loader's unchecked offsets and counts are safe, because the authoring kept every container
in bounds, and 16-byte alignment holds throughout. A reimplementation may rely on both for shipped files, and should
validate other inputs.

**Not covered: the allocation-failure half.** In the setup `00409A60`, the copy at `00409BC2` is skipped when a buffer
pointer is null. What the surrounding calls allocate, and what a caller then sees, is not read here. That half stays open,
and it is static.
