[Home](../../README.md) / [Game files and data tables](README.md) / Menu graphics containers (.as7)

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Menu graphics containers (.as7): the compressed page archives behind item pictures and character silhouettes | format | Game files and data tables | Image files | The big-endian A7 containers in bin_menu: a page directory and a shared static dictionary, the LZ page codec 0x00248500 and its walker 0x0024AA00, how the item-picture path decodes one 64 x 96 page into the itemgra_c atlas with an Item_Clut palette, how the silhouette path decodes 258 pages into each of two TIM2 images, the 18 shipped files, and the rules an edited container must keep. | 0x0024AA00, 0x00248500, 0x02090788, 0x02091090, 0x00291C80, 0x0209BEA0, 0x00291D90, 0x00292050, 0x00292390, 0x01E0C470, 0x01E0C474, 0x002C8EE0, 0x0209E638, 0x002CEB40, 0x002CEFD0, 0x002CEE00, 0x0024A440, 0x0024A1D0, 0x002C9040, 0x0029F580 |

## What the player sees

Two kinds of menu picture come out of these files. The item pictures that menu list rows show are 64 x 96 pages of the eight `item_gra` sheets, decoded one at a time when a row
needs one. The large character silhouette behind the Gambits screen is one of six groups of pages in
`char_silhouette.as7`, picked by the party member being edited.

An item's picture number is its equipment row: the number divided by 64 picks one of the eight `item_gra` sheets and
the rest picks a page. The game unpacks that page, a grid of colour numbers, into the `itemgra_c` menu picture and
gives it the sheet's palette from `Item_Clut.bin`.

## Where it comes from

The files are resource kind 7, in the `in` and `ch` locale folders only:
`ps2data/image/ff12/myoshiok/<locale>/bin_menu/<name>.as7`. In the US kind-7 path array¹ the ids are
`0x75` for `Char_Silhouette.as7` and `0x9A` to `0xA1` for `Item_Gra00.as7` to `Item_Gra07.as7`. The KR, CH and CN arrays² name the `ch` copy; the others name `in`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01EC73A0` |
| ² | `0x01E0E530`, `0x01E5A3D0`, `0x01EABBA0` |

</details>

- Items: at start-up `0x0022A4B0` calls `0x00291C80`, which requests kind 7 ids `0x98` to `0xA1` (`itemgra_c.tm2`,
  `Item_Clut.bin`, then the eight sheets) through `0x0032E620`, sizing each with `0x0024AB90` (a jump to `0x0032E400`) and
  allocating it from heap 2¹. Request `i` fills the 16-byte slot `0x0209BEA0 + 16 × i` (status, then
  buffer at `+8`).
- An item slot's status is `0x0032E620`'s answer, and the read's completion `0x00291C60(i)` sets it to 0
 ².
- Silhouettes: the field HUD root `0x00253780` calls `0x002C8EE0`, which requests ids `0x74` (`monotone_chr.bin`) and
  `0x75` (`Char_Silhouette.as7`) into the slots at `0x0209E638`. `0x002CEB40` copies them into its widget, so the
  container's buffer sits at widget `+0xD8`. Each slot holds the request id at `+0`, which the delivery
  callback `0x002C9040(i)` clears to 0, and the buffer at `+8`.
- For `monotone_chr.bin` `0x002C8EE0` allocates `0x880` bytes more than the file's size and, before filing the read
  of the file's size, copies `0x440` bytes from the `clutpack_ys.bin` entry whose address `[0x0209AC30] + 0x390`
  holds to buffer `+0x1DC0`³. Neither pointer is checked, so a
  null one faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00249810` |
| ² | `0x00291C6D` |
| ³ | `0x002C8F3A`, `0x002C8F57`-`0x002C8FEF`, `0x002C8FCF` |

</details>

## Layouts

All multi-byte fields are big-endian.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[2]` |  | value "A7": read by no function: the container buffers reach only the walker `0x0024AA00` (from `0x00292390` at `0x00292768` and `0x002CEFD0` at `0x002CF2B4` and `0x002CF2CE`), which starts at byte `+0x02`, and the codec `0x00248500`, which reads the page streams and the dictionary; the slot and widget copies `0x00291D90`, `0x00292050`, `0x002CEB40` and `0x002C8EE0` move the pointer only; nothing fixes its width |
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

<details>
<summary>Show the shipped data</summary>

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
| `Item_Clut.bin` alpha | `0x80` in 1,791 of the 1,792 colours, 0 in the other |

Every colour of `Item_Clut.bin`, whose `in` and `ch` copies are identical:

| table | rows | one row per |
|---|---:|---|
| [`as7-menu-graphics-item-clut-rows.tsv`](as7-menu-graphics-item-clut-rows.tsv) | 1,792 | colour: palette 0 to 6, index, file offset, R, G, B and alpha |

</details>

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
1 with nothing written. A token is copied whole before the count is compared, so an overshooting token's bytes are
written past the length¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00248664`-`0x0024866A` |

</details>

### Item pictures

`0x00291D90(object, message)`, the item-graphic object's procedure, copies the ten slots into the object
(`+0xC8 + 16 × i`, buffer at `+0xD0 + 16 × i`), sets the bits under mask `0x3FF` of its word `+0x168`, and
registers the `itemgra_c.tm2` buffer as the atlas `itemgra_c` through `0x0024A440`. `0x00292050(i)` returns slot `i`'s
buffer when its bit is set. It takes the object
from `[0x0209AC30] + 0x300` and returns 0 when that is null or the bit is clear¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00292061`, `0x00292073` |

</details>

`0x00291D90` keeps a state in bits `0xF0000` of its dword `+0x168` and returns 0 for every message:

- message 1 stores the object at `[0x0209AC30] + 0x300`¹, makes the dword `0x10000` (state 1), zeroes the
  ten slot copies and attaches the object (`0x00247950(object, 0)`); message `0x12` sets `[0x0209AC30] + 0x300` to 0
 ²; any other message but 2 goes to `0x005C5230`, which returns 0;
- on message 2, state 1 becomes 2³. In state 2 it copies the slots in order up to the first whose
  status is not yet 0⁴. It registers the atlas into `+0xC0` with `0x0024A440(buffer, "itemgra_c", 2)`
  when slot 0's status is 0, `+0xC0` is 0 and the buffer is non-null⁵;
- only when all ten statuses are 0 does it set the bits under `0x3FF` and make the state 4⁶;
- state 5 becomes 6 and goes on into state 6⁷. State 6 waits while any of the ten requests is pending
 ⁸, then releases the atlas (`0x0024A680(+0xC0, 0)`) and zeroes `+0xC0`, the ten slot
  copies, the slot bits and byte `+0x16B`, and copies bits `0xF00000` into the state⁹;
- state 7 sends a close request¹⁰; every other state does nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00291F96` |
| ² | `0x00291DD2` |
| ³ | `0x00291F78` |
| ⁴ | `0x00291EE7` |
| ⁵ | `0x00291F03`-`0x00291F32` |
| ⁶ | `0x00291F41`-`0x00291F6C` |
| ⁷ | `0x00291E1E` |
| ⁸ | `0x0032E4D0`, `0x00291E4A` |
| ⁹ | `0x00291EA6`-`0x00291EBB` |
| ¹⁰ | `0x00244F00`, `0x00291E14` |

</details>

The list item procedure `0x00292390` takes a graphic id from message `0x0C` (payload word `+2`) and decodes on its next
update (message 2):

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The sheet is `id >> 6` and the page `id & 63`; `0x00292050(sheet + 2)` gives the container, and `0x0024AA00` decodes that one page into the item's own buffer at `+0x2C8`. |   |
| 2 | When the sheet differs from the last one shown, it points the atlas palette at `Item_Clut + sheet × 1,024` (slot 1's buffer) and takes the colour count from the atlas picture. |   |
| 3 | It copies 64 x 96 bytes into the `itemgra_c` pixels, at column 0 or 64 by a toggle that flips each time, and re-uploads the atlas. | `0x01E0C470`, `0x01E0C474`<br>`0x0024A1D0` |

The id is signed. For an id with bit `0x8000` set¹ the update clears the cell once instead:
while the item's word `+0x102CA` is 0 and the container `[[0x0209AC30] + 0x300]` is there with bit `0x1` of its `+0x168`
and its atlas `+0xC0`, it zeroes the 64 x 96 bytes at the toggle's column, flips the toggle, sets `+0x102CA` to 1 and
re-uploads the atlas².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0029269A`-`0x0029269D` |
| ² | `0x00292952`-`0x00292A43` |

</details>

For any other id it takes slot `(id >> 6) + 2` through `0x00292050`, which shifts 1 left by the slot with a 32-bit
shift, keeps the low 16 bits and tests them against the object's word `+0x168`¹; the shift
counts the slot modulo 32: the bits tested are `(1 << (slot & 31)) & 0xFFFF & [object + 0x168]`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00292063`-`0x0029206D` |

</details>

`0x00291D90` sets the bits under mask `0x3FF`, one per slot, so sheets 0 to 7 answer and ids 0 to 511 (512 pictures,
highest 511) decode. An id whose slot modulo 32 is 10 to 31 finds no container: ids 512 to 1919, and the same band in
every later block of 2,048 ids. For those the procedure binds the `itemgra_c` atlas as it stands¹ without decoding.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00292702`-`0x00292712`, `0x0029F580` |

</details>

The other 9,728 ids from 1920 to `0x7FFF` pass the test, because their slot modulo 32 is 0 to 9: ids 1920 to 2559
(slots 32 to 41) test the bits of slots 0 to 9, and so do ids `2048 × k + 1920` to `2048 × k + 2559` up to 32640 to
32767 (`0x7FFF` is slot 513 and tests bit `0x2`).

`0x00292050` then reads the container at `+0xD0 + 16 × slot` with the full
slot¹: `+0x2D0` for slot 32 up to `+0x20E0` for slot 513, all past the end of the `0x170`-byte
object (`0x002920C0` creates it through `0x00244F50`). A zero there is treated as no container; any other value is decoded
as a container by `0x0024AA00`, with the palette at `Item_Clut + sheet × 1,024` for sheet 30 or more, past the 7,168-byte
file. What the row shows for these ids depends on the memory after the object.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00292075`-`0x0029207F` |

</details>

The toggle and the last sheet are shared by every item picture, so the atlas holds two item pictures at
once: a third decode overwrites the older one, and both are drawn with the palette of the last sheet
decoded, so two items from different sheets on screen together show one in the wrong colours.

Message `0x0C` comes from the description box builder `0x00293170` ([Inventory screen](../Menus-And-HUD/inventory-screen.md)
lists its callers and the kind each passes). The builder keeps the box at `[[0x0209AC30] + 0x2F8] + 0xC0`¹, the one store of the box pointer, and of the code that reads that word back only `0x0029329F` sends
message `0x0C`, through `0x00247510`. A new box sends it to itself on message 1, forwarding the line and entry
pointers the builder passed at creation².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00293286` |
| ² | `0x00292ACF`-`0x00292AD9`, `0x00293238`-`0x00293266` |

</details>

Ten other places in the code store message number `0x0C` and call a procedure through a pointer. Each puts a
number from `0x8001` to `0x8102` at payload `+8`, where the box reads the line's address¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023C37F`, `0x0023D1CD`, `0x0023D326`, `0x00241ABA`, `0x00241BA6`, `0x00277DF5`, `0x00277E68`, `0x00278E0A`, `0x0027E436`, `0x00551ADD` |

</details>

The id is the equipment row. The builder has the line composed by `0x00292B70`, which calls the kind's filler from
the 16-entry table `0x01E0C490`¹. Only the fillers of kinds 1 to 5 (weapons, ammunition,
shields, head and body pieces, accessories) set byte `+0` to 1, and each stores the item id minus `0x1000` as
word `+2`². No table and no field of the equipment row takes part.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00292D08`-`0x00292D3B` |
| ² | `0x00295985`-`0x00295991`, `0x002953ED`-`0x002953F8`, `0x00294BDF`-`0x00294BFF`, `0x0029406F`-`0x0029408F`, `0x0029337E`-`0x0029339E` |

</details>

Every other kind leaves byte `+0` at 0. The fillers of kinds 6 to 10 and 12 write 0 there¹, those of kinds 14 and 15 leave the cleared buffer,
and kinds 0, 11 and 13 have no filler, so `0x00292B70` returns 0 and no message is sent². With byte
`+0` clear the procedure stores -1 as the id³ and shows no picture.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002948B7`, `0x00295811`, `0x00293E60`, `0x00293F82`, `0x00294AF2`, `0x00295762` |
| ² | `0x00292D16` |
| ³ | `0x0029254B`-`0x0029257A` |

</details>

In all nine `battle_pack.bin` the equipment table (directory entry `+0x38`) has 557 rows, so the ids run from 0
to 556: 64 on each of sheets 0 to 7 and 45 above 511. The party can hold rows 0 to 419 only, the 420 equipment
counts of [Item and ability ids](../Engine-Core/item-and-ability-ids.md), which fill sheets 0 to 5 and
pages 0 to 35 of sheet 6. The 267 shop lists hold 694 equipment rows among their 2,512, 248 distinct ids from 1
to 415.

The party table's starting equipment goes past row 419 (91 equipment words, 66 distinct ids). On sheet 7 are the
weapon 468 and off hand 469 of Lamont (row 10), the off hand 469 of Larsa (row 13), 485 of Reddas (rows 14 and
16) and 459 of Shemhazai (row 34); above 511 are the body pieces 544 to 556 of the thirteen Esper rows 27 to 39
([Party table](../Party/party-table.md)).

A member's worn pieces reach the box through the Equip screen: `0x0027F210` copies the current member's five
equipment words into the menu block's `+0xD48 + 32 × k`, and `0x003FF920(slot)` sends that slot's word when the
slot cursor moves¹ or the member changes². That screen's member steps pass over records
with flag bit `0x2` (guests) or a member id of 6 or more: the member-record panel sets `+0xD3C` bit `0x10`
unless the screen is Status³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FF77A` |
| ² | `0x003FF545` |
| ³ | `0x002CC07E`-`0x002CC097`, `0x002C24BF`-`0x002C24CE` |

</details>

For an id from 448 to 511 the procedure decodes a page of `item_gra07`: 1,536 zero bytes at the box's `+0x2C8`,
the first 24 of the picture's 96 rows. The copy still takes 6,144 bytes, so rows 24 to 95 show the buffer's
bytes 1,536 to 6,143: 0 in a box that has decoded nothing yet, since `0x002465F0` clears all `0x102D0` bytes when
`0x00244F50` builds it¹, and otherwise the rest of the last picture that box decoded.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00246626` |

</details>

The palette moves to `Item_Clut + 7 × 1,024`, the first byte past the 7,168-byte buffer, so the colours are the
1,024 bytes that follow it, the zero bytes taking the first 4. Nothing in the code fixes them: `0x00291C80`
allocates the size the file-size table gives, 7,168 for kind 7 id `0x99`¹, and
`0x00249810` hands that size unchanged to `0x0036A190`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00291CD2`-`0x00291CE0` |
| ² | `0x00249816`, `0x00249822` |

</details>

### Silhouettes

`0x002CEE00(index, flags)` stores the index at widget `+0x10D`; an index above 5 clears the decode bit. The Gambits
screen passes the member's word `+0x60` when it reloads the centre pane¹ and -1 when it closes².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056A044` |
| ² | `0x00567A52` |

</details>

The widget is `[0x0209AC30] + 0x308`, and with a null one `0x002CEE00` does nothing¹. It stores the flags
at `+0x10C`². The compare with 5 is unsigned³, so -1 also clears the decode bit, bit `0x2`
of `+0x10C`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CEE11` |
| ² | `0x002CEE13` |
| ³ | `0x002CEE24` |
| ⁴ | `0x002CEE45` |

</details>

An index of 0 to 5 sets dword `+0xC4` of the widget at `[0x0209AC30] + 0x310` to 1 and
one of 6 or more sets it to 0, each only when that widget exists¹;
a negative index leaves it. Every call with a widget then stores the UI tick counter `0x0208F570` at `+0x104` and 6
at `+0x100`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CEE26`-`0x002CEE39`, `0x002CEE4F`-`0x002CEE67` |
| ² | `0x002CEE71`-`0x002CEE7E` |

</details>

`0x002CEFD0` maps the index through `{0, 1, 3, 2, 4, 5}` to a group `g`, allocates two 264,192-byte buffers from heap
2 on first use, decodes pages `516 × g` (258 pages) into the first and the next 258 into the second, and registers
them as the atlases `chrback_top` and `chrback_bottom`¹, or re-uploads them² after the first
time. It ignores the walker's result, so a page that fails to decode leaves a partial picture that is
uploaded all the same.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024A440` |
| ² | `0x0024A1D0` |

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 3 calls with 2 other topics</summary>

**Battle actions** (explained on [file requests and the read queue](file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E4D0`](../Graphics/effect-file-loading.md) (on effect file loading) | is called by | [`0x002FC3C0`](../Graphics/effect-element-runtime.md) (on effect element runtime) |

**Saving, loading and settings** (explained on [resource arena and relocation](resource-arena-and-relocation.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00247950`](as7-menu-graphics.md) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x0032E4D0`](../Graphics/effect-file-loading.md) (on effect file loading) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |

</details>
