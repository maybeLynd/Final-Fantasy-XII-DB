---
title: "Bin_menu images: the headerless 8-bit guest portraits and area icons pasted into menu pictures"
kind: "format"
category: "Game files and data tables"
addresses: "0035C5B0, 0035C430, 00283270, 002CEAE0, 002CE980, 003C9A30, 003C9950, 003C9E50, 00280750, 00280670, 00181580, 00180C80, 00180A70, 0024A5A0, 022CA470, 0209AC30, 022C314C, 0031A7B0"
---

## What the player sees

The game pastes these files into three menu pictures at run time:

- when a guest is in the party, the guest's portrait `face_guestNN` into `partytop_8_c`;
- a guest's small face, one cell of `mini_guest_face`, into `mini_face_c`;
- when an area flag is set, the icon `map_efe0N` into `battle_4_c`. Flags `4`<sub>h</sub> to `20`<sub>h</sub> are the ones that make
  `0031A7B0` refuse commands of four action classes.

## Where it comes from

All eighteen are kind-7 resources in `ps2data/image/ff12/myoshiok/<lang>/bin_menu/`:

| Id | File | Requested by |
|---|---|---|
| `0D`<sub>h</sub> | `mini_guest_face.bin` | `0035C5B0` |
| `0E`<sub>h</sub>-`14`<sub>h</sub> | `map_efe00.bin`-`map_efe06.bin` | `003C9950` |
| `17`<sub>h</sub>-`20`<sub>h</sub> | `face_guest07.bin`-`face_guest16.bin` | `002CEAE0` |

The language's kind-7 path array (`002DF9A0`) names the folder: `us`, `fr`, `de`, `it` and `es` for language
ids 1-5, `in` for id 6 and the default, `kr`, `ch` and `cn` for 7, 8 and 11. The destination pictures come
from the same language's `packfiles/tex2pack_ys.bin` (kind 7, `D7`<sub>h</sub>).

## Layouts

A file has no header, magic, size or palette. It is a run of 8-bit colour indices that the paste routine
reads as rows of its destination rectangle's width:

Mini_guest_face.bin (73,728 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `+ 2000h n` | u8[128][64] | cell for guest character id 7 + n: 128 rows of 64 indices |

Map_efe0N.bin (16,384 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0000`<sub>h</sub> | `u8[64][128]` | first cell: 64 rows of 128 indices |  |
| `2000`<sub>h</sub> | `u8[64][128]` | second cell, copied into the 64 rows below the first |  |

Face_guestNN.bin (12,288 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8[]` | rows of the partytop_8_c rectangle's width |  |

The destination rectangle is a sub-image record of the picture's `eXt` block, found as the
[UI typed lists](ui-typed-lists.md) page gives it (`page = u16[T + 14h + (code >> 8) x 2]`, then the entry, then
an 8-byte record `x, y, w:12, h:12`):

| Destination | Sub-image code | Read at | Record in the shipped pictures |
|---|---|---|---|
| `mini_face_c` | `0000`<sub>h</sub> | `0035C487` | 64 x 128 at (0, 0) |
| `partytop_8_c` | `0003`<sub>h</sub> | `002CE9E6` | 400 x 102 at (550, 800) |
| `battle_4_c` | `0C00`<sub>h</sub> | `003C9E50` | 128 x 64 at (0, 256) |

## Shipped data

| Fact | Value |
|---|---|
| copies | 162: 18 files in each of `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us` |
| sizes | `face_guest` 12,288; `map_efe` 16,384; `mini_guest_face` 73,728 (nine 8,192-byte cells, none blank) |
| `face_guest07`-`16` | byte-identical in all nine languages; `08` = `09`, `10` = `13`, `11` = `12`, `14` = `16` |
| `face_guest` at a 128-byte stride | every 2 x 2 block uniform in all 90 copies: a 64 x 48 picture doubled on both axes |
| `face_guest15` | starts `2F 2F 32 32`, pixel indices that read as `//22` |
| `map_efe00` | 4 contents: `fr`, `es`, `de`, and one shared by the other six |
| `map_efe01` | 2 contents: `es` and `fr` share one, the other seven another |
| `map_efe02`-`06` | one content in all nine languages |
| `map_efe` halves | the two 64-row cells differ in 1,274 to 3,959 bytes; every file uses all 256 index values |
| `mini_guest_face` | 3 contents: `us`; `es` and `fr`; the other six |
| destination pictures (all nine `tex2pack_ys.bin`) | `mini_face_c`, `partytop_8_c` and `battle_4_c` are TEX0 format `13`<sub>h</sub>, image type 5, CLUT type 3 |
| destination CLUT colours | `mini_face_c` 256; `partytop_8_c` 4,608; `battle_4_c` 27,648 (`us`, `fr`, `es`) or 27,392 |

## Loader behaviour

### The guest portrait

- The menu task `00281AE0` calls `00283270(1)`, which scans the nine party records (`00320040(3, i)`). It clears
  bit `2`<sub>h</sub> of `[0209AC30] + D3Ch` and sets `+B2D`<sub>h</sub> to `FF`<sub>h</sub>. A member whose record has bit `2`<sub>h</sub> of byte 0
  sets bit `2`<sub>h</sub> and stores its character id (record `+60`<sub>h</sub>) at `+B2D`<sub>h</sub>.
- `002CEAE0` then requests kind 7, id `+B2Dh + 10h` into `+3C0`<sub>h</sub> through `00249180`, so guest ids 7 to 16
  load `face_guest07` to `face_guest16`.
- On message `10`<sub>h</sub> the menu task `00280DE0` calls `002CE980`. When the bit and the buffer are set, it finds
  `partytop_8_c` by name (`0024A5A0`) and copies `h` rows of `w` bytes from the buffer into the picture's
  pixels at `(x, y)`, stepping the picture width. It re-uploads the picture through `00181580`, frees the
  buffer (`003697F0`) and clears `+3C0`<sub>h</sub>.
- The shipped sub-image `0003`<sub>h</sub> is a 400 x 102 party-panel frame, so whenever a guest is in the party
  `002CE980` copies 40,800 bytes from the 12,288-byte `face_guest` buffer, reading 28,512 bytes past it,
  and lays the 128 x 96 portrait out in 400-byte rows at (550, 800). When the sub-image lookup fails it
  falls back to 64 x 48, the size of a `face_guest` picture.

### The small face

- `0035C5B0` requests `mini_guest_face` (id `0D`<sub>h</sub>) with `menubtlwndinfo` (id `25`<sub>h</sub>) and keeps it at
  `022CA470`.
- `0035C430(g)` returns when the `mini_face_c` slot `[0209AC30] + 358h` is null or `g` is below 7. Otherwise it
  copies `h` rows of `w` bytes from `022CA470 + (g - 7) x w x h` into the sub-image and re-uploads the picture.
- `g` is the character id `0035BB50` returns; `00298250` and `00276D30` call it. No upper bound is checked.

### The area icon

- The menu object of `003C9A30` takes the first of bits `1`<sub>h</sub> to `40`<sub>h</sub> set in the area flags `022C314C`
  (table `00D11710`). When that differs from the icon in use and some bit is set, it stores the bit number `k`
  at `+C1`<sub>h</sub>.
- `003C9950` frees any previous buffer at `+D0`<sub>h</sub> and requests kind 7, id `0Eh + k`, into it.
- `003C9E50` copies `2h` rows of `w` bytes into `battle_4_c` from the sub-image's top-left corner, writing `w` to
  `01EFE384` and `2h` to `01EFE388`. It re-uploads the picture and frees the buffer.
- The flags are set by `0031A910` and cleared by `0031A8C0`. `0031A7B0` refuses a command whose command-record byte
  `+1E`<sub>h</sub> is 0, 1, 2 or 3 while bit `4`<sub>h</sub>, `8`<sub>h</sub>, `10`<sub>h</sub> or `20`<sub>h</sub> is set, with codes `16`<sub>h</sub> to `19`<sub>h</sub>.

### The destination pictures and the palette

`00280750` registers ten named pictures at `[0209AC30] + 338h` to `+380`<sub>h</sub> (`battle_4_c` first,
`mini_face_c` fifth, `partytop_8_c` seventh) and requests `tex2pack_ys.bin`. `00280670` binds the pack's
pictures to them in order through `0024A1D0`. For format `13`<sub>h</sub>, `0024A1D0` registers the index plane and one
256-colour palette per 256 CLUT colours under the picture's name ([TIM2 images](tim2-images.md)).

`00181580(name, pixels, width, height, imageType)` refreshes the named texture from the edited index plane:
image type 5 copies the bytes as they are (`00180C80`), type 4 splits each byte into two 4-bit indices, low
nibble first (`00180A70`). All three destinations are type 5, so each byte of a `bin_menu` image is an
8-bit index into the destination picture's CLUT.

## Modding notes

- Write palette indices, not colours. The colours come from the destination picture's CLUT in
  `tex2pack_ys.bin`; change that CLUT to recolour.
- A replacement must be `w x h` bytes per cell for its sub-image: 8,192 per `mini_guest_face` cell and 16,384
  for a `map_efe` file. Its size must match the size table entry the request allocates from.
- To paste a guest portrait intact, give `partytop_8_c` a sub-image `0003`<sub>h</sub> of the portrait's size.
- `mini_guest_face` holds nine cells, for character ids 7 to 15. A larger `g` reads past the file.
- Area icon `k` is `map_efe0k` for the lowest set flag bit `k`. Only one icon is pasted at a time.

## Related

- [TIM2 images](tim2-images.md): the destination pictures, their CLUTs and the texture binder.
- [UI typed lists](ui-typed-lists.md): the named-picture registry and the sub-image lookup.
- [File size tables](file-size-tables-fst.md): the sizes the requests allocate.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the kind-7 requests.
