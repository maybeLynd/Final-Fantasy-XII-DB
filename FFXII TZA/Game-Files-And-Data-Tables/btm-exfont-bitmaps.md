---
title: "ExFont sheets (.btm): the 4-bit glyph cells of the six staff-roll faces, how they are loaded and how a glyph finds its cell"
kind: "format"
category: "Game files and data tables"
addresses: "0x00365810, 0x00D10C98, 0x022CBE00, 0x022CBBB0, 0x00364950, 0x003658F0, 0x003643A0, 0x00366080, 0x00364380, 0x003657E0, 0x00364210, 0x003649A0, 0x00474650, 0x003A1F20, 0x0053EB90, 0x0053E0B0, 0x002DF9A0, 0x0017FC00, 0x001E7F90"
---

## What the player sees

The staff roll's scrolling text is set in six faces, three typefaces each with a drop-shadow companion. The
`.btm` sheets are the PS2-era pixel cells of those faces. A line with a shadow is drawn twice, the shadow face
first and the face over it; the quad the remaster puts on screen takes its pixels from the matching `font_stf` font of
the [font list](../Menus-And-HUD/fonts.md), and the sheet cell goes into the GS packet path beside it.

## Where it comes from

The sheets are kind-7 resources `0xDA` to `0xDF` in the archive folder `ps2data/image/ff12/myoshiok/<lang>/exfont/`.
`0x00365810` maps a sheet slot to its resource id through the twelve-entry table `0x00D10C98`:

| Slot | Id | File |
|---:|---|---|
| 1-6 | `0x82`-`0x87` | none: the path arrays hold null and every size table holds -1 |
| 7 | `0xDA` | `font_stf_a_normal.btm` |
| 8 | `0xDB` | `font_stf_a_shadow.btm` |
| 9 | `0xDC` | `font_stf_b_normal.btm` |
| 10 | `0xDD` | `font_stf_b_shadow.btm` |
| 11 | `0xDE` | `font_stfc_normal.btm` (`font_stf_c_normal.btm` in the `kr` and `cn` arrays) |
| 12 | `0xDF` | `font_stf_c_shadow.btm` |

The kind-7 path array is chosen per language id by `0x002DF9A0`. Language ids 1-6 and the default array name the
`in` sheets, id 8 the `ch` sheets, ids 7 and 11 `kr` and `cn` sheets. The glyph tables that locate the cells come
from `packfiles/fontpack_fs.bin` (kind 7, `0xD2`): the `us` copy for ids 1-6, `kr`, `ch` and `cn` for 7, 8 and 11,
and `in` for the default.

## Layouts

A sheet has no header, magic or count. It is a run of glyph cells, each `roundW x roundH` texels at 4 bits per
texel, rows of `roundW / 2` bytes, where `roundW` and `roundH` are the glyph record's width and height rounded
up to 8, 16, 32, 64 or 128. A cell starts at its glyph record's sheet offset.

The glyph tables, as `0x003643A0`, `0x00366080` and `0x00364210` read them:

Fontpack_fs.bin:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | fontBlock | offset of the font block from the file start (`0x003643A0`) |

Font block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | tableCount | number of glyph tables walked by `0x00366080` |
| `+0x02` | `i16` | value | rounded up to even and doubled into state +`0x244` |
| `+0x04` | `...` | table 0 | first glyph table |

Glyph table:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | next | offset of the next table from this one |
| `+0x04` | `i32` | glyphCount | number of 12-byte records |
| `+0x08` | `u8[8]` | not read by 0x00364210 |  |
| `+0x10` | `...` | records | glyphCount records |

Glyph record (12 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | code | character code matched by `0x00364210` |
| `+0x02` | `u8` | cellW | glyph width in texels |
| `+0x03` | `u8` | cellH | glyph height in texels |
| `+0x04` | `u8[4]` | skipped by 0x00364210 |  |
| `+0x08` | `u32` | sheetOffset | byte offset of the cell in the sheet of the same face |

The font state is a `0x250`-byte block at `0x022CBBB0`; `0x00364950` zeroes it and stores its address in `0x022CBE00`.

Font state (pointer at `0x022CBE00`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `void*` | fontpack | the loaded fontpack_fs.bin |
| `+0x008` | `void*` | fontBlock | fontpack + u32[0] |
| `+0x010` | `void*` | tables[16] | glyph table of face n at +`0x10` + 8n |
| `+0x090` | `void*` | tableEnds[16] end of face n's records |  |
| `+0x110` | `void*` | sheets[16] | .btm buffer of face n at +`0x110` + 8n |
| `+0x228` | `void*` | cacheTail | least recently used glyph cache entry |
| `+0x230` | `void*` | cacheHead | most recently used glyph cache entry |
| `+0x240` | `u32` | ready | bit n set when face n's sheet has arrived |

Sheet slot `s` is face `s - 1`, so the six staff-roll faces are faces 6 to 11 and their sheets sit at state
`+0x140` to `+0x168`.

## Shipped data

| Fact | Value |
|---|---|
| files | 12: the six names in `in/exfont` and `ch/exfont`; no `.btm` ships in any other folder |
| distinct contents | 6; each `ch` sheet is byte-identical to its `in` sheet |
| sizes | `font_stf_a_*` 42,240; `font_stfc_normal` and `font_stf_c_shadow` 32,256; `font_stf_b_*` 29,184 |
| first four bytes | `00 00 00 00` in all 12; the first non-zero byte is at file offset `0x15` to `0x64` |
| texel values | all 16 nibble values occur in every sheet |
| size tables | 42,240 / 29,184 / 32,256 for ids `0xDA`-`0xDF` in every table except `KR` and `CN`, which hold -1 |
| `fontpack_fs.bin` tables | 12 in every copy; faces 6 to 11 are the staff-roll faces |
| glyphs per face (`in`, `ch`, `kr`, `cn`) | 78: `A`-`Z`, `a`-`z`, `,.!?`, `1`-`0`, `&*-_\|:'"()/` and `・` (U+30FB) |
| glyphs per face (`us`, `it`) | 78 in faces 6 and 7; 127 in faces 8 to 11, the 78 followed by 49 accented Latin letters (`À` to `ß`) |
| cell packing (`in` tables against the `in` sheets) | cells in table order, back to back, no gaps or overlaps, ending exactly at the end of each sheet |
| rounded cell sizes | 16 x 32, 32 x 32, 32 x 64 and 64 x 32 in faces 6 and 7; 16 x 32 and 32 x 32 in faces 8 to 11 |
| `us` faces 8 to 11 | the first 78 records equal the `in` records; the 49 extra cells lie wholly past the end of the 29,184- and 32,256-byte sheets |

## Loader behaviour

### Requesting a sheet

`0x00365810(slot, mode)` does nothing while `0x022CBE00` is null. When face `slot - 1` has no sheet yet, it takes the
size from the size table (`0x0032E400(7, id)`, `0x00365882`), allocates it (`0x002497E0` when `mode` is 0,
`0x00249810` otherwise), stores the buffer at state `+0x110 + 8 x (slot - 1)` and files a kind-7 request
(`0x0032E620`, `0x003658C7`) whose completion is `0x00364380` with `slot - 1` as its value. It never checks the size.
In both cases it then passes `slot + 10`, the `font_stf` font ids 17 to 22, to `0x0017FC00`.

`0x0017FC00(id)` registers the font with the text renderer at `[0x01F811F8]`: `0x001E7F90` takes a 16-byte
record from the renderer's list at `+0xE70`, fills it with `{id, 0x20 * n + id, 0, 2}` (`n` the
first dword of the object at `[0x01F81200]`) and files it under the key `(2 << 32) | id` in the tree at
`+0xF30`, adding the key when it is missing (`0x001E78D0`).

`0x00364380` ORs `1 << (slot - 1)` into the ready word (`0x00364393`) and returns at once when the state pointer is
null. `0x003657E0(slot)` reads that bit. `0x00365810` does not request a face whose buffer is already set.

`0x00365570(slot)`, run by `0x0053EEA0`, gives a face back: it frees the sheet (`0x003697F0`), clears its ready bit
and unregisters the font id `slot + 10` (`0x0017FC70`). `0x00365990()`, run by `0x00252840`, `0x002528A0`,
`0x00252990`, `0x00252A20` and the frame's UI step `0x00252A70`, acts only while bit 30 of the ready word is set:
it calls `0x0039BD50(0x34E0)` and uploads the buffer at state `+0x190` with `0x00474600(buffer, 0x3500, 0, 0x10,
[+0x244])`.

### The glyph tables

`0x00365DD0()`, run by `0x00364950`, allocates the glyph cache: `0xA00` bytes, 64 entries of `0x28` bytes linked
both ways, each with `0xFF0000` at `+0x10`, kept at `+0x220`, with the first entry at `+0x228` and the last at
`+0x230`.

`0x00364950` points `0x022CBE00` at the state block and calls `0x003658F0`, which requests `fontpack_fs.bin` with the
completion `0x003643A0`. That completion stores the font block pointer and calls `0x00366080`, which stores each
table's address at `+0x10 + 8n` and the end of its records at `+0x90 + 8n`, stepping by each table's `next`
offset.

### The staff-roll task

`0x0053EB90` requests slots 7 to 12 with mode 1 (`0x0053EC9A`) and the logo picture `sf_logo_c.tm2` (kind 7,
`0x47`). On later updates it returns until `0x003657E0` reports all six slots ready (`0x0053EBF3`). `0x0053ED10`
starts it (through `0x00511540`). The drawing task `0x0053E0B0` passes each line to `0x003649A0`: when the line asks
for a shadow, first with its face index plus 1 (the shadow face) at an offset, then with the face index.

### Finding and drawing a cell

`0x003649A0` draws nothing for a face whose ready bit is clear. For each character it takes a cached entry
(`0x00365FD0`) or calls `0x00364210(code, face)`:

- `0x00364210` first recycles the least recently used cache entry: it moves the head of the list at
  `[0x022CBE00] + 0x228` to the tail `+0x230` and, when the entry held texels, clears it (key `0xFF0000`, texel and
  record pointers null) (`0x0036422B`-`0x00364272`).
- It then scans face `n`'s table for the code and returns null when it is absent (`0x003642A1`), so that character
  is skipped and the recycled entry stays empty.
- It rounds `cellW` and `cellH` each with `r = v <= 8 ? 8 : v <= 16 ? 16 : v <= 32 ? 32 : v <= 64 ? 64 : 128`
  (`0x003642D0`-`0x00364342`).
- The entry gets the record, the rounded size and `sheet + sheetOffset`, or a null texel pointer when face
  `n` has no sheet. No offset is checked against the sheet's size.

For a cell with texels, `0x003649A0` builds a GS upload of `roundW x roundH` texels in pixel format `0x14`
(4 bits per texel, `0x00474650` at `0x00364BFF`); `0x003A1F20` sizes such a transfer as `width x height / 8` words,
half a byte per texel. The pen advance and the screen quad come from the `font_stf` font with id `face + 11`
(`0x0017FD00`, `0x0017F8C0`): the quad drawn through `0x0017F7C0` uses that font's glyph record for its atlas
rectangle, and only when the colour's alpha byte is non-zero.

### Control codes and measuring

`0x003649A0` reads the line as 16-bit codes and hands each to `0x003647E0` first (`0x00364B58`), which
consumes the codes below `0x21` and the escape `0x7B` and returns any other code for drawing. `0x00364530`
walks the same codes without drawing to measure the line; `0x003656A0` calls it (`0x00365778`), and the
staff roll's line layout `0x0053DD20` measures through `0x003656A0`.

| Code | `0x003647E0` (drawing) | `0x00364530` (measuring) |
|---|---|---|
| `0x0000` | ends the line | ends the line |
| `0x0001` | advances the pen `+0x38` by the width of the face's `0x30` cell: the font's advance `+0x1C` through `0x0017F9C0`, times the scale `+0x04` | the same |
| `0x0002` | sets the byte `+0x33` to a fifth of `+0x37`, unless `+0x63` bit `0x1` is set | skipped |
| `0x0003` | sets `+0x33` to `+0x37`, unless `+0x63` bit `0x1` is set | skipped |
| `0x0020` | advances by the renderer's space width `0x0017F920(1)` times the scale | the same |
| `0x3000` | advances by `0x0017F920(0)` times the scale | the same |
| `0x007B` | `0x00366110` reads the escape up to its `0x7D`, with its last argument 1 | the same, with 0 |

For any other code `0x00364530` finds the face's record (the 12-byte entries at `+0x10` of the face table)
and the `font_stf` glyph (`0x0017FD00(face + 11)`, `0x0017F8C0(code)`), advances by the glyph's `+0x20`
(`0x0017F8E0`) plus its `+0x1C` (`0x0017F9C0`) times the scale `+0x04`, keeps the cell size `+0x10`, `+0x14` in
`+0x40`, `+0x44` and the record at `[0x022CBE00] + 0x238`, and returns the largest `(+0x4C, or +0x44 when
that is 0) + +0x50`, times `+0x08`, it saw. At the end, with `+0x62` set, it adds the last record's byte
`+0x02` less its byte `+0x04`, times the scale, when that is positive.

## Modding notes

- A replacement sheet must hold every cell its face's glyph table places in it, `roundW x roundH / 2` bytes
  at each record's `sheetOffset`, and its size must match the size table entry the loader allocates from.
- Edit `fontpack_fs.bin` to add, move or resize a glyph; the sheet itself carries no index.
- With the `us` glyph tables (language ids 1-6), faces 8 to 11 list 49 accented letters whose cells lie past
  the end of the shipped `in` sheets, so drawing one reads beyond the allocation. Extend the sheet and its size
  table entry before using them.
- The `KR` and `CN` size tables list all six sheets as -1 and no `kr` or `cn` sheet ships. `0x00365810`
  files the requests without checking the size, and a −1 request completes as delivered
  ([file requests](file-requests-and-the-read-queue.md)), so those faces are marked ready without sheets.
- The shapes the remaster draws come from the `font_stf` atlases ([fonts](../Menus-And-HUD/fonts.md)); changing a
  sheet does not change them.

## Related

- [Fonts](../Menus-And-HUD/fonts.md): the `font_stf` fonts 17 to 22 whose glyph records place the drawn quads.
- [TIM2 images](tim2-images.md): the 4-bit glyph sheets of the font pack and menus.
- [File size tables](file-size-tables-fst.md): the per-language sizes the loader allocates.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the kind-7 request and its completion.
