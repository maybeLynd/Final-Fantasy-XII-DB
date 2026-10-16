---
title: "Location-map colour tables (.cl2): the CLT2 palettes some location maps draw with"
kind: "format"
category: "Game files and data tables"
addresses: "003C1F00, 003C26C0, 003C2190, 02B457E0, 0024A9E0, 0024A480, 0024A1D0, 00181000, 00180E70, 0017F3B0, 008C5B34, 02CF7480, 00163D00, 003BC2D0"
---

## What the player sees

The colours of the pictures on a location map. No location-map picture uses its own palette: every map takes the
third colour table of `clutpack_ys.bin`, and the two map entries that name a `.cl2` take that file's table
instead, so the same pixel data can be recoloured without being reshipped.

## Where it comes from

The files are resource kind 7: `ps2data/image/ff12/myoshiok/<locale>/bin_menu/loca_<name>.cl2`. In the US kind-7
path array (`01EC73A0`) id `E2`<sub>h</sub> is `Loca_gil.cl2`, `E3`<sub>h</sub> `Loca_bhm.cl2` and `E4`<sub>h</sub> `Loca_rbl.cl2`.

The map-data widget `02B457E0` loads `menumap_common.bin` (kind 7 `A4`<sub>h</sub>) into its `+E8`<sub>h</sub> (`003BC2D0`). The pane
loader `003C1F00(widget, owner, descriptor, n)`, reached through `003C2190` from `002B7B80`, `002BAF80` and
`003CB4F0`, takes a free pane (two, `A8`<sub>h</sub> bytes apart from `+120`<sub>h</sub>), requests `menumap_sub<n>.bin` (kind 7
`142h + n`) through `00249180`, and then picks the colour table:

1. It releases the table already at widget `+118`<sub>h</sub> (`003697F0`) and clears the pointer.
2. It finds the entry table in `menumap_common.bin` (the u16 at file `+8` is its offset: a u32 count, then 8-byte
   entries) and, when `n` is below the count and byte `+1` of entry `n` is not 0, requests kind 7 id
   `E1h + byte` through `00249210` into heap 3 (`003C2068`-`003C208D`), keeping the buffer at `+118`<sub>h</sub>.

## Layouts

The file is a TIM2 file with the magic changed, one picture and no pixel data.

```
+0x00  char[4]  "CLT2"     not read by the game
+0x04  u8       version    4
+0x05  u8       format     0
+0x06  u16      pictures   1
+0x08  u8[8]    zero
picture header (+0x10)
+0x10  u32      totalSize  file size - 0x10; not read
+0x14  u32      clutSize   colours x 4; not read
+0x18  u32      imageSize  0; read
+0x1C  u16      headerSize 0x30; read
+0x1E  u16      colours    read
+0x20  u8       pictFormat 0
+0x21  u8       mipmaps    0
+0x22  u8       clutType   3 (32-bit colours); not read
+0x23  u8       imageType  5 or 4; not read
+0x24  u8[28]   zero
+0x40  u8[4][colours]  palette: R, G, B, A
```

The palette starts at `+10h + headerSize + imageSize`. The alpha byte is on the PS2 scale, where `80`<sub>h</sub> is
opaque.

## Shipped data

Measured over every `.cl2` in the archive and every `menumap_common.bin`.

| Fact | Value |
|---|---|
| files | 20: `loca_bhm` and `loca_gil` in nine locales, `loca_rbl` in `ch` and `in`; 3 distinct contents, every same-name copy identical |
| sizes | 2,112 bytes (`bhm`, `gil`), 192 bytes (`rbl`) |
| colours | 512 (`bhm`, `gil`, image type 5); 32 (`rbl`, image type 4) |
| header | version 4, format 0, one picture, image size 0, header size `30`<sub>h</sub>, clut type 3, total size = file size - `10`<sub>h</sub>, clut size = colours x 4, all other header bytes zero, in all 20 |
| alpha bytes | `FF`<sub>h</sub> in 239 of 512 colours of `bhm` and `gil`; every other alpha is at most `6F`<sub>h</sub>; none is `80`<sub>h</sub> |
| `menumap_common.bin` | nine copies, 1,760 bytes; entry table at `0C`<sub>h</sub> with 48 entries; byte `+1` is 1 in entry 40 and 2 in entry 46, 0 elsewhere |
| selected | entry 40 requests `E2`<sub>h</sub> (`Loca_gil`), entry 46 requests `E3`<sub>h</sub> (`Loca_bhm`); no entry selects `E4`<sub>h</sub> |

## Loader behaviour

### The reader

`003C26C0(widget, n)` finds the pane holding `menumap_sub<n>` and walks the sub file's picture table. For each
picture whose atlas slot is still empty and whose offset is not -1, it:

1. takes the colour table at `+118`<sub>h</sub>, or the buffer at `+110`<sub>h</sub> when that is empty, and gets its picture header
   through `0024A9E0(buffer, 0)` (buffer `+10`<sub>h</sub>). `+110`<sub>h</sub> is the default: `003C2100` fills it, when it is
   empty, with `0035D520()` = `[0209AC30 + 3A0h]`, which `00280AD0` sets to the third table of
   `clutpack_ys.bin` (kind 7 id `D4`<sub>h</sub>, requested by `002808D0`);
2. reads the image size (`+8`), header size (`+C`<sub>h</sub>) and colour count (`+E`<sub>h</sub>) of that header and computes the
   palette address;
3. names the picture `loca_<a>_<b>` (`sprintf "loca_%d_%d"`) from the sub file's tables and registers it through
   `0024A480(picture, name, flags, palette, colours)`.

`0024A480` registers the atlas (`0024A4E0`) and, for a colour count below `4000`<sub>h</sub>, stores the count in bits 18 and
up of the slot's flags and the palette at slot `+28`<sub>h</sub>, then builds the texture (`0024A1D0`).

### The upload

With a slot palette present, `0024A1D0` passes the stored count, the palette and the picture's own clut and image
type bytes (picture header `+12`<sub>h</sub>, `+13`<sub>h</sub>) to `00181000` for an 8-bit picture or `00180E70` for a 4-bit one, so
the file's `clutType` and `imageType` never matter. Both reach `0017F3B0`, which creates a texture of the format object `02CF7480` (named `RGBA8` by
`00163D00`), copies the colours, and rescales byte 3 of each to `min(255, trunc(a × 255 / 128))`
(`0017F517`-`0017F54A`, factor 1/128 at `008C5B34`).

An alpha of `80`<sub>h</sub> or more draws fully opaque; `6F`<sub>h</sub> draws as
221 of 255.

## Modding notes

- To recolour every map without a `.cl2`, edit the third table of `clutpack_ys.bin`, which uses the
  same layout.
- The game never checks `CLT2`, the version, the picture count, the sizes or the clut and image types. It reads
  only `+18`<sub>h</sub>, `+1C`<sub>h</sub> and `+1E`<sub>h</sub> and the palette they locate.
- Keep the image size 0 and the header size `30`<sub>h</sub>, or move the palette to match `10h + headerSize + imageSize`.
- Write alpha on the PS2 scale: `80`<sub>h</sub> is opaque, and values above it saturate.
- To recolour another map, set byte `+1` of its `menumap_common.bin` entry to `k`; the game then requests kind 7
  id `E1h + k`, which must be a shipped path with a size in the file-size tables.
- `Loca_rbl.cl2` (`E4`<sub>h</sub>) ships only in `ch` and `in`, so a byte of 3 would request a file missing in the other
  locales.

## Related

- [Map screens](../Menus-And-HUD/map-screens.md): the map-data widget and the menumap files it loads.
- [UI typed lists](ui-typed-lists.md): the atlas registry `0024A480` registers each picture in.
- [File size tables (.fst)](file-size-tables-fst.md): the kind 7 path arrays and request sizes.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the request entries.
