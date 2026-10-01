# RC-26 to RC-28: .btm texel packing, the font_stf glyph tables, and glyph coverage (ORACLE, 2026-09-30)

## The question

SWE2-CONTRACT's batch 3 registered three rows from
`02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/btm-exfont-bitmaps.md` section 7:
- **RC-26:** the `.btm` texel packing, 8 bits per texel or 4-bit nibbles;
- **RC-27:** which resource file supplies the glyph table for the `font_stf` faces, taking "the ids 130 to 135 half"
  of `00365810`'s 12-id table `00D10C98` through the kind-7 path array;
- **RC-28:** how many glyphs each `font_stf` face carries, against the `f1` family's 1,237 kerning pairs.

## Method

[`rc26_fonts.py`](rc26_fonts.py), output [`rc26_fonts.out`](rc26_fonts.out). It uses:
- the batch helper `../rc22-as7-pages-0930/arc.py` (VBF and image);
- RC-5's `ResourcePath_Init` replay, `../rc6-console-map-codes-0930/rc5_paths.py`, for the kind-7 rows of all 13
  region arrays.

The script checks the code facts it relies on against the image bytes (C1), then reads:
- every shipped `fontpack_fs.bin` (kind 7, id `0xD2`);
- every shipped `.btm`;
- the twelve d3d11 `font_stf_*.dat` / `.ker` files.

Controls, all PASS:

| control | what it checks |
|---|---|
| C1a-C1e | the loader, its single caller loop, the glyph lookup's pairing of table and sheet, and the fontpack fix-up, all read from the image |
| C2 | ids 130 to 135 name no path in any of the 13 region arrays |
| C3 | the 4-bit reading reproduces every sheet's size exactly; the 8-bit reading never does |

## Result

**RC-26: ANSWERED. A `.btm` holds 4 bits per texel, one glyph cell after another. Each cell's width and height are
rounded up to a power of two (8 to 128), which is the rounding the lookup `00364210` applies (`003642D0`-`00364342`).**
- Every glyph record's `pixelOffset` (`+8`) advances by exactly `pow2(w) * pow2(h) / 2` bytes.
- The last cell of each of tables 6 to 11 ends exactly at the end of its sheet: 42,240, 29,184 and 32,256 bytes. This
  holds in 28 of the 36 (pack, table) pairs; the 8 that do not are the overruns below.
- At 8 bits per texel the last cell would end 256 bytes past the end every time, so no 8-bit reading fits.
- `00364210` itself copies no texels. It stores the cell pointer `sheet + pixelOffset` and the rounded dimensions in
  a cache node (`+0x18`, `+0x14`, `+0x15`).

**RC-27: ANSWERED, and the row's premise is corrected. The `font_stf` glyph tables come from `fontpack_fs.bin`
(kind 7 id `0xD2`, the language's `PackFiles` directory), tables 6 to 11 of its 12-table header. Ids 130 to 135 are
not the source; they are never requested.**
- **`00365810(n)`** requests id `00D10C98[n-1]` into pixel slot `+0x110 + (n-1)*8`.
- **Its only caller** is the staff-roll setup `0053EB90`, a loop `n = 7..12` (`0053EC90`-`0053ECA4`). That loop loads
  only ids 218 to 223, the six `.btm` sheets, into font slots 6 to 11.
- **Ids 130 to 135 (n = 1 to 6)** are requested by no code, and they name no path in any region array.
- **The glyph tables:** the completion of the `fontpack_fs.bin` request (`003658F0` → `003643A0`) sets
  `[022CBE00]+8 = pack + dword[pack]`. `00366080` then walks that header (word count 12) and fixes table `k` into
  `+0x10 + 8k`.
- **Pairing:** `00364210` looks a glyph up in table `font` and takes its pixels from sheet `font` at the same index
  (`00364276`, `00364346`). So faces 6 to 11 read tables 6 to 11 against the six `.btm` sheets.
- **Region to directory:** `0xD2` resolves to `in` in regions 0, 9, 10 and 12, `us` in 1 to 6, `kr` in 7, `ch` in 8,
  and `cn` in 11. Every region's ids 218 to 223 point at `in/ExFont` except `kr`, `ch` and `cn`. The archive holds
  `.btm` files only under `in` and `ch`.

**RC-28: ANSWERED.**

- **PS2-heritage exfont faces (tables 6 to 11):**
  - Faces a and as carry 78 glyphs in every pack.
  - In the `in`, `kr`, `ch` and `cn` packs, all six faces carry 78 glyphs.
  - In the `us` and `it` packs, faces b, bs, c and cs carry **127**: the 78, plus 49 accented Latin letters (`À`
    to `ü`, `Œ`/`œ`, `ß`).
- **The 49 extra cells lie past the only shipped sheet.** Those 49 glyphs' pixel offsets fall beyond the 29,184- and
  32,256-byte sheets that every region loads. A US or Italian staff roll that asks faces b or c for an accented
  letter therefore reads past the end of the loaded sheet buffer.
- **d3d11 faces, where the `f1` family's 1,237 pairs live** (`gamedata/d3d11/artdata/font/{us,jp}/font_stf_*`):
  - each face carries **78** glyphs (`jp/font_stf_a` 77), 69 of them with a kern code point;
  - each face's `.ker` has 1,237 pairs, but **only 398 of them have both characters in the face**;
  - the other 839 pairs name characters the face does not carry.

## Corroboration

SWE2-DATA answered these rows first (`../rc22-34-resource-readers-0930/` section 5, commit `1261e2044`). This record
agrees on all three and was derived independently.

- **RC-26.** SWE2-DATA has the stronger proof: the cell upload `00474650` with PSM `0x14`, the PSMT4 case of
  `003A1F20`, and the low-nibble-first order. This record reproduces the size arithmetic from the data alone.
- **RC-27.** Same answer. This record also names the region-to-directory map for id `0xD2` and for ids 218 to 223
  across all 13 region slots (some slots share an array; SWE2-DATA counts ten arrays).
- **RC-28.** Same exfont counts (78 / 127) and the same 49 accented glyphs lying past the sheet. This record adds the
  d3d11 faces themselves: 78 glyphs (`jp/a` 77), 69 kerned, and 398 of 1,237 pairs inside each face.

## Not claimed

- **Whether the exfont staff-roll path draws anything in the PC build**, whose credits may use the d3d11 faces instead.
  This record establishes the data and the code paths, not which one a playthrough takes. The overrun above matters
  only if the exfont path runs in a US or Italian session. Measuring that is ASTRA's method if wanted.
- What fills pixel slots 1 and 5, which the pack does not fill.
- What the 12-byte glyph record's bytes `+5` to `+7` mean. UQ-364 found no reader for them.
- The kerning is structurally inert in the shipped build (the kerning page, section 3). The 398 / 839 split describes
  the authored data, not a rendered effect.
