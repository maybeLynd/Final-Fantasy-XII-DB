---
title: "Menu graphics containers (.as7): the compressed page archives behind item pictures and character silhouettes"
kind: "format"
category: "Game files and data tables"
addresses: "0x0024AA00, 0x00248500, 0x02090788, 0x02091090, 0x00291C80, 0x0209BEA0, 0x00291D90, 0x00292050, 0x00292390, 0x01E0C470, 0x01E0C474, 0x002C8EE0, 0x0209E638, 0x002CEB40, 0x002CEFD0, 0x002CEE00, 0x0024A440, 0x0024A1D0, 0x002C9040, 0x0029F580"
---

## What the player sees

Two kinds of menu picture come out of these files. The item pictures that menu list rows show are 64 x 96 pages of the eight `item_gra` sheets, decoded one at a time when a row
needs one. The large character silhouette behind the Gambits screen is one of six groups of pages in
`char_silhouette.as7`, picked by the party member being edited.

## Where it comes from

The files are resource kind 7, in the `in` and `ch` locale folders only:
`ps2data/image/ff12/myoshiok/<locale>/bin_menu/<name>.as7`. In the US kind-7 path array (`0x01EC73A0`) the ids are
`0x75` for `Char_Silhouette.as7` and `0x9A` to `0xA1` for `Item_Gra00.as7` to `Item_Gra07.as7`. The KR, CH and CN arrays
(`0x01E0E530`, `0x01E5A3D0`, `0x01EABBA0`) name the `ch` copy; the others name `in`.

- Items: at start-up `0x0022A4B0` calls `0x00291C80`, which requests kind 7 ids `0x98` to `0xA1` (`itemgra_c.tm2`,
  `Item_Clut.bin`, then the eight sheets) through `0x0032E620`, sizing each with `0x0024AB90` (a jump to `0x0032E400`) and
  allocating it from heap 2 (`0x00249810`). Request `i` fills the 16-byte slot `0x0209BEA0 + 16 × i` (status, then
  buffer at `+8`).
- Silhouettes: the field HUD root `0x00253780` calls `0x002C8EE0`, which requests ids `0x74` (`monotone_chr.bin`) and
  `0x75` (`Char_Silhouette.as7`) into the slots at `0x0209E638`. `0x002CEB40` copies them into its widget, so the
  container's buffer sits at widget `+0xD8`. Each slot holds the request id at `+0`, which the delivery
  callback `0x002C9040(i)` clears to 0, and the buffer at `+8`.

## Layouts

All multi-byte fields are big-endian.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[2]` | "A7" | read by no function: the container buffers reach only the walker `0x0024AA00` (from `0x00292390` at `0x00292768` and `0x002CEFD0` at `0x002CF2B4` and `0x002CF2CE`), which starts at byte `+0x02`, and the codec `0x00248500`, which reads the page streams and the dictionary; the slot and widget copies `0x00291D90`, `0x00292050`, `0x002CEB40` and `0x002C8EE0` move the pointer only; nothing fixes its width |
| `+0x02` | `u16be` | count | number of pages |
| `+0x04` | `u32be` | dictOff | file offset of the dictionary blob |
| `+0x08` | `u32be[count]` | pageOff | file offset of each page's token stream |

```
...    page streams
dictOff  dictionary blob, to the end of the file
```

The dictionary blob:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | mode | 0 or 3 decode; any other value fails |
| `+0x01` | `u8` | b | length bit count |
| `+0x02` | `u16be` | outLen | mode 0 only: bytes every page decodes to |
| `+0x04` | `u8[]` | dict | mode 0; for mode 3 the dictionary starts at `+0x02` |

In mode 3 each page stream begins with its own big-endian u16 output length instead. A page stream is tokens:

```python
t >= 0x80   literal: copy the next (t & 0x7F) + 1 stream bytes
t <  0x80   reference: w = t << 8 | next byte
            offset = w & (0xFFFF >> (b + 1))
            length = ((t × 2) >> (8 − b)) + 3
            copy length bytes from dict + offset (the dictionary, never the output)
```

With `b` = 5 a reference reaches dictionary offsets 0 to 1,023 and copies 3 to 34 bytes.

## Shipped data

Measured over every `.as7` in the archive.

| Fact | Value |
|---|---|
| files | 18: `char_silhouette` and `item_gra00` to `item_gra07`, each in `in` and `ch`; 9 distinct contents, the two copies identical |
| sizes | 6,190 (`item_gra07`) to 2,134,185 bytes (`char_silhouette`) |
| pages | 64 in every `item_gra`; 3,096 in `char_silhouette` |
| directory | the first page starts right after it (`8 + 4 × count`) and offsets rise, the last below `dictOff`, in all 18 |
| dictionary | mode 0 and `b` = 5 in all 18; 34 to 1,024 dictionary bytes |
| decoding | every page of all 18 decodes exactly to `outLen`, and every reference stays inside the dictionary |
| `outLen` | 6,144 in `item_gra00` to `06`; 1,536 in `item_gra07`, whose 64 pages are all zero bytes; 1,024 in `char_silhouette` |
| every page | one row each in [`as7-menu-graphics-pages-rows.tsv`](as7-menu-graphics-pages-rows.tsv), 3,608 rows for the 9 distinct files: stream offset and bytes, decoded bytes, the decoded page's SHA-256 prefix, its non-zero bytes, its largest byte, and whether it begins a `TIM2` picture (12 pages, two per silhouette group) |
| zero pages | 176 of the 3,096 `char_silhouette` pages decode to zero bytes only, in runs inside the groups (pages 1 to 29 and 517 to 559 among them), besides the 64 of `item_gra07` |
| item pages | one byte per pixel; the largest index in each of `item_gra00` to `06` is 255 |
| silhouette groups | pages `516 × g` to `516 × g + 257` and the next 258 each decode to 264,192 bytes beginning with a `TIM2` header, for all six groups |
| `Item_Clut.bin` | 7,168 bytes in `in` and `ch`, identical: seven 1,024-byte palettes |
| `itemgra_c.tm2` | 128 x 128, 8-bit, 512 colours in nine locales; 64 x 64 in `in_sdver` |

## Loader behaviour

### The walker

`0x0024AA00(file, out, first, n)` reads the count from bytes 2 and 3 and returns 1 at once when `first` is not below
it. `n` = 0, or an `n` above the count, means the count; the run is clipped to the pages that exist. It points the
codec's output base `0x02090788` at `out`, zeroes `out[0]` and the output cursor `0x02091090`, then decodes pages
`first` onward, each with `0x00248500(file + pageOff[i], file + dictOff)`, so consecutive pages are appended. It
returns 0 when all pages decoded and 1 when one fails. Nothing bounds the output against the buffer.

### The codec

`0x00248500(stream, blob)` reads the mode and `b`, takes the output length from the blob (mode 0) or the stream
(mode 3), and returns 0 for any other mode. It writes at `[0x02090788] + [0x02091090]`, advancing the cursor, until the
count of decoded bytes reaches the length: an exact finish returns 1, an overshoot returns 0. A length of 0 returns
1 with nothing written.

### Item pictures

`0x00291D90`, the item-graphic object's procedure, copies the ten slots into the object (`+0xC8 + 16 × i`, buffer at
`+0xD0 + 16 × i`), sets bits 0 to 9 of its word `+0x168`, and registers the `itemgra_c.tm2` buffer as the atlas
`itemgra_c` through `0x0024A440`. `0x00292050(i)` returns slot `i`'s buffer when its bit is set.

The list item procedure `0x00292390` takes a graphic id from message `0x0C` (payload word `+2`) and decodes on its next
update (message 2):

1. The sheet is `id >> 6` and the page `id & 63`; `0x00292050(sheet + 2)` gives the container, and `0x0024AA00`
   decodes that one page into the item's own buffer at `+0x2C8`.
2. When the sheet differs from the last one shown, it points the atlas palette at `Item_Clut + sheet × 1,024` (slot
   1's buffer) and takes the colour count from the atlas picture.
3. It copies 64 x 96 bytes (`0x01E0C470`, `0x01E0C474`) into the `itemgra_c` pixels, at column 0 or 64 by a toggle that
   flips each time, and re-uploads the atlas (`0x0024A1D0`).

The id is signed. On the update the procedure does nothing for an id with bit `0x8000` set (`0x0029269A`-`0x0029269D`).
For any other id it takes slot `(id >> 6) + 2` through `0x00292050`, which shifts 1 left by the slot with a 32-bit shift,
keeps the low 16 bits and tests them against the object's word `+0x168` (`0x00292063`-`0x0029206D`); the shift counts the
slot modulo 32.

`0x00291D90` sets bits 0 to 9, one per slot, so sheets 0 to 7 answer and ids 0 to 511 (512 pictures,
highest 511) decode. An id whose slot modulo 32 is 10 to 31 finds no container: ids 512 to 1919, and the same band in
every later block of 2,048 ids. For those the procedure binds the `itemgra_c` atlas as it stands (`0x00292702`-`0x00292712`,
`0x0029F580`) without decoding.

The other 9,728 ids from 1920 to `0x7FFF` pass the test, because their slot modulo 32 is 0 to 9: ids 1920 to 2559
(slots 32 to 41) test the bits of slots 0 to 9, and so do ids `2048 × k + 1920` to `2048 × k + 2559` up to 32640 to
32767 (`0x7FFF` is slot 513 and tests bit `0x2`).

`0x00292050` then reads the container at `+0xD0 + 16 × slot` with the full
slot (`0x00292075`-`0x0029207F`): `+0x2D0` for slot 32 up to `+0x20E0` for slot 513, all past the end of the `0x170`-byte
object (`0x002920C0` creates it through `0x00244F50`). A zero there is treated as no container; any other value is decoded
as a container by `0x0024AA00`, with the palette at `Item_Clut + sheet × 1,024` for sheet 30 or more, past the 7,168-byte
file. What the row shows for these ids depends on the memory after the object.

The toggle and the last sheet are shared by every item picture, so the atlas holds two item pictures at
once: a third decode overwrites the older one, and both are drawn with the palette of the last sheet
decoded, so two items from different sheets on screen together show one in the wrong colours.

### Silhouettes

`0x002CEE00(index, flags)` stores the index at widget `+0x10D`; an index above 5 clears the decode bit. The Gambits
screen passes the member's word `+0x60` when it reloads the centre pane (`0x0056A044`) and -1 when it closes
(`0x00567A52`).

`0x002CEFD0` maps the index through `{0, 1, 3, 2, 4, 5}` to a group `g`, allocates two 264,192-byte buffers from heap
2 on first use, decodes pages `516 × g` (258 pages) into the first and the next 258 into the second, and registers
them as the atlases `chrback_top` and `chrback_bottom` (`0x0024A440`), or re-uploads them (`0x0024A1D0`) after the first
time. It ignores the walker's result, so a page that fails to decode leaves a partial picture that is
uploaded all the same.

## Modding notes

- The game never checks `A7`; it trusts the count, the offsets and the dictionary offset as they stand.
- Keep the dictionary blob at the end of the file and every page offset below it. Use mode 0 or 3; any other
  mode decodes nothing.
- An item page must decode to 6,144 bytes: the copy always takes 64 x 96 bytes from the decode buffer, whatever
  the decode wrote.
- A silhouette group is 516 pages that together must decode to two TIM2 images of at most 264,192 bytes each.
- A real sheet 7 needs an eighth palette: `Item_Clut.bin` ships with seven.
- Picture ids are `sheet × 64 + page`, 512 in all (0 to 511). A ninth sheet needs a container in slot 10, which the
  ten-slot request list of `0x00291C80` and the `+0x168` bits do not provide.
- Keep picture ids at 0 to 511. Above that only the ids whose slot modulo 32 is 10 to 31 are refused; the others read a
  container pointer from past the end of the item-graphic object.
- Request sizes come from the file-size tables, so a resized file needs its kind 7 entry changed there.

## Related

- [UI typed lists](ui-typed-lists.md): the atlas registry `itemgra_c`, `chrback_top` and `chrback_bottom` are
  registered in.
- [Menu resource packages (.mrp)](mrp-menu-resource-packages.md): `save_load.mrp` and `shop_new.mrp` name the
  `itemgra_c` atlas the item pages are copied into.
- [File size tables (.fst)](file-size-tables-fst.md): the kind 7 path arrays and request sizes.
- [File requests and the read queue](file-requests-and-the-read-queue.md): `0x0032E400` and `0x0032E620`.
- [Gambit screen](../Menus-And-HUD/gambit-screen.md): the screen that sets the silhouette.
