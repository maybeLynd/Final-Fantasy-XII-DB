---
title: "Bin_menu images: the headerless 8-bit guest portraits and area icons pasted into menu pictures"
kind: "format"
category: "Game files and data tables"
addresses: "0x0035C5B0, 0x0035C430, 0x00283270, 0x002CEAE0, 0x002CE980, 0x003C9A30, 0x003C9950, 0x003C9E50, 0x00280750, 0x00280670, 0x00181580, 0x00180C80, 0x00180A70, 0x0024A5A0, 0x022CA470, 0x0209AC30, 0x022C314C, 0x0031A7B0"
---

## What the player sees

The game pastes these files into three menu pictures at run time:

- when a guest is in the party, the guest's portrait `face_guestNN` into `partytop_8_c`;
- a guest's small face, one cell of `mini_guest_face`, into `mini_face_c`;
- when an area flag is set, the icon `map_efe0N` into `battle_4_c`. Four of these flags are the ones that stop
  the party using Attack, Magicks, Technicks or Items ([command availability](../Battle-Actions/command-availability.md)).

Each of these files is a bare grid of colour numbers with no colours of its own. When a guest joins or an area flag is
set, the game copies the grid into a fixed rectangle of one of three menu pictures loaded from `tex2pack_ys.bin`, and
that picture's palette turns each number into a colour.

## Where it comes from

All eighteen are kind-7 resources in `ps2data/image/ff12/myoshiok/<lang>/bin_menu/`:

| Id | File | Requested by |
|---|---|---|
| `0x0D` | `mini_guest_face.bin` | `0x0035C5B0` |
| `0x0E`-`0x14` | `map_efe00.bin`-`map_efe06.bin` | `0x003C9950` |
| `0x17`-`0x20` | `face_guest07.bin`-`face_guest16.bin` | `0x002CEAE0` |

The language's kind-7 path array (`0x002DF9A0`) names the folder: `us`, `fr`, `de`, `it` and `es` for language
ids 1-5, `in` for id 6 and the default, `kr`, `ch` and `cn` for 7, 8 and 11. The destination pictures come
from the same language's `packfiles/tex2pack_ys.bin` (kind 7, `0xD7`).

The area flags behind the icons are set and cleared by the script verbs `set_field_effect` and `clear_field_effect`.
The lowest flag that is set picks the icon pasted into `battle_4_c`, and four of the flags also bar Attack, Magicks,
Technicks or Items.

## Layouts

A file holds single bytes only, so it has no byte order.

A file has no header, magic, size or palette. It is a run of 8-bit colour indices that the paste routine
reads as rows of its destination rectangle's width:

Mini_guest_face.bin (73,728 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[9][128][64]` | cells | cell n, at `0x2000` × n, is the face of guest character id 7 + n: 128 rows of 64 indices |

Map_efe0N.bin (16,384 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0000` | `u8[64][128]` |  | first cell: 64 rows of 128 indices |
| `+0x2000` | `u8[64][128]` |  | second cell, copied into the 64 rows below the first |

Face_guestNN.bin (12,288 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[]` |  | rows of the partytop_8_c rectangle's width |

The destination rectangle is a sub-image record of the picture's `eXt` block, found as the
[UI typed lists](ui-typed-lists.md) page gives it (`page = u16[T + 0x14 + (code >> 8) x 2]`, then the entry, then
an 8-byte record `x, y, w:12, h:12`):

| Destination | Sub-image code | Read at | Record in the shipped pictures |
|---|---|---|---|
| `mini_face_c` | `0x0000` | `0x0035C487` | 64 x 128 at (0, 0) |
| `partytop_8_c` | `0x0003` | `0x002CE9E6` | 400 x 102 at (550, 800) |
| `battle_4_c` | `0x0C00` | `0x003C9E50` | 128 x 64 at (0, 256) |

## Shipped data

| Fact | Value |
|---|---|
| copies | 162: 18 files in each of `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us` |
| sizes | `face_guest` 12,288; `map_efe` 16,384; `mini_guest_face` 73,728 (nine 8,192-byte cells, no blank cell) |
| `face_guest07`-`16` | byte-identical in all nine languages; `08` = `09`, `10` = `13`, `11` = `12`, `14` = `16` |
| `face_guest` at a 128-byte stride | every 2 x 2 block uniform in all 90 copies: a 64 x 48 picture doubled on both axes |
| `face_guest15` | starts `2F 2F 32 32`, pixel indices that read as `//22` |
| `map_efe00` | 4 contents: `fr`, `es`, `de`, and one shared by the other six |
| `map_efe01` | 2 contents: `es` and `fr` share one, the other seven another |
| `map_efe02`-`06` | one content in all nine languages |
| `map_efe` halves | the two 64-row cells differ in 1,274 to 3,959 bytes; every file uses all 256 index values |
| `mini_guest_face` | 3 contents: `us`; `es` and `fr`; the other six |
| destination pictures (all nine `tex2pack_ys.bin`) | `mini_face_c`, `partytop_8_c` and `battle_4_c` are TEX0 format `0x13`, image type 5, CLUT type 3 |
| destination CLUT colours | `mini_face_c` 256; `partytop_8_c` 4,608; `battle_4_c` 27,648 (`us`, `fr`, `es`) or 27,392 |

Every copy and every cell, measured with the layouts above. The cells table has one row per cell within each
distinct whole-file variant, with the folders that hold that variant, so the same cell bytes can appear in more
than one row: `mini_guest_face.bin` cells 0 to 7 are the same in the `us` and the `es`/`fr` variants, and cell 8
differs. The destination pictures' rows are in
[`ps2data-bin-families-packfiles-rows.tsv`](ps2data-bin-families-packfiles-rows.tsv) (`tex2pack_ys.bin` entries 0, 4
and 6).

| table | rows | one row per |
|---|---:|---|
| [`binmenu-images-files-rows.tsv`](binmenu-images-files-rows.tsv) | 162 | copy: folder, size, SHA-256, the folders with the same bytes, the index values used, and the 2 x 2 test and first bytes (`face_guest`) or the bytes in which the two cells differ (`map_efe`) |
| [`binmenu-images-cells-rows.tsv`](binmenu-images-cells-rows.tsv) | 59 | cell of a distinct whole-file variant: offset, size, the guest or area flag it serves, SHA-256, index values used, zero bytes, smallest and largest index |

## Loader behaviour

### The guest portrait

- The menu task `0x00281AE0` calls `0x00283270(1)`, which scans the nine party records (`0x00320040(3, i)`). It clears
  bit `0x2` of `[0x0209AC30] + 0xD3C` and sets `+0xB2D` to `0xFF`. A member whose record has bit `0x2` of byte 0
  sets bit `0x2` and stores its character id (record `+0x60`) at `+0xB2D`.
- Before that scan the task clears the `0x938` bytes from `[0x0209AC30] + 0x408`
  (`0x00281C8B`-`0x00281CA1`), which hold both `+0xB2D` and `+0xD3C`. After it the task runs
  `0x002826F0`, `0x002CD510` and `0x00254E80` (`0x00281CB0`-`0x00281CBA`).
- `0x00254A50` gates two of the menu's entries: `0x002CD3C0(0x4B7, 0xCCA)` (story gate
  `0x4010`) and `0x002CD3C0(0x4BC, 0xCCF)` (story gate `0x4007`) run only when `0x00254A50()`
  answers 0 and `0x0032A8A0` answers non-zero for the gate (`0x00281C13`-`0x00281C3B`,
  `0x00281C4F`-`0x00281C77`). `0x002CD3C0(a, b)` stores `a` in the new entry's dword `+0x00` and
  the answers of `0x002F9860(a)` and `0x002F9860(b)` in its `+0x10` and `+0x18`
  (`0x002CD3F1`-`0x002CD403`).
- The page object comes from `0x00249580(task)`; the task calls `0x002920C0`, `0x002CEFA0`,
  `0x002CEAE0` and `0x00249410` on it in that order (`0x00281D93`-`0x00281DB6`), so the guest
  portrait request of the next item runs after `0x002920C0`.
- `0x002CEAE0` then requests kind 7, id `+0xB2D + 0x10` into `+0x3C0` through `0x00249180`, so guest ids 7 to 16
  load `face_guest07` to `face_guest16`. It requests only while bit `0x2` of `+0xD3C` is set (`0x002CEAEB`); with
  the bit clear it returns at once and leaves `+0x3C0` as it was.
- On message `0x10` the menu task `0x00280DE0` calls `0x002CE980`. When the bit and the buffer are set, it finds
  `partytop_8_c` by name (`0x0024A5A0`) and copies `h` rows of `w` bytes from the buffer into the picture's
  pixels at `(x, y)`, stepping the picture width. It re-uploads the picture through `0x00181580`, frees the
  buffer (`0x003697F0`) and clears `+0x3C0`.
- `0x002CE980` does not test what `0x0024A5A0` returns: with no `partytop_8_c` entry the read of the picture
  header `[0 + 0x20]` at `0x002CE9D1` faults. The re-upload passes the name, the pixels (the header plus its u16
  `+0x0C`), the width `+0x14`, the height `+0x16` and the image type byte `+0x13` (`0x002CEA6F`-`0x002CEA93`).
- The shipped sub-image `0x0003` is a 400 x 102 party-panel frame, so whenever a guest is in the party
  `0x002CE980` copies 40,800 bytes from the 12,288-byte `face_guest` buffer, reading 28,512 bytes past it,
  and lays the 128 x 96 portrait out in 400-byte rows at (550, 800).
- The body holds a fallback to 64 x 48, the size of a `face_guest` picture, at byte offset `49 x width - 64`
  of the pixels (`0x002CEA26`), taken only when the sub-image record address is 0 (`0x002CE9FB`). That address
  is the picture header plus `0x30` plus two u16 offsets, never 0 for a header the reads before it reached,
  so the fallback never runs.
- The sub-image lookup has no failure test: the page and entry indices of code `0x0003` are read with no bound
  (`0x002CE9D5`, `0x002CE9E6`).

### The small face

- `0x0035C5B0` requests `mini_guest_face` (id `0x0D`) with `menubtlwndinfo` (id `0x25`) and keeps it at
  `0x022CA470`.
- `0x0035C430(g)` returns when the `mini_face_c` slot `[0x0209AC30] + 0x358` is null or `g` is below 7. Otherwise it
  copies `h` rows of `w` bytes from `0x022CA470 + (g - 7) x w x h` into the sub-image and re-uploads the picture.
- `g` is the character id `0x0035BB50` returns; `0x00298250` and `0x00276D30` call it. No upper bound is checked.
- `0x0035C430` reads the picture header `[slot + 0x20]` (`0x0035C459`) and the buffer `[0x022CA470]` with no null
  test. A null header faults at `0x0035C46C`; while `0x022CA470` is still null the copy reads from address
  `(g - 7) x w x h`, below `0x10000` for `g` 7 to 14 with the shipped 64 x 128 record, and faults. The
  re-upload passes the slot, the pixels, the width, the height and the image type byte `+0x13` (`0x0035C541`).

### The area icon

- The menu object of `0x003C9A30` takes the first of bits `0x1` to `0x40` set in the area flags `0x022C314C`
  (table `0x00D11710`). When that differs from the icon in use and some bit is set, it stores the bit number `k`
  at `+0xC1`.
- `0x003C9950` frees any previous buffer at `+0xD0` and requests kind 7, id `0x0E + k`, into it. It opens a menu
  set (`0x00249580`), files the request through `0x00249210` (`0x003C999B`), closes the set (`0x00249410`), stores the
  request's buffer (its `+8`) at `+0xD0` and sets bit `0x8` of `+0xC4` (`0x003C99AF`).
- No null return is tested there. With all twelve menu sets in use `0x00249580` returns 0 (`0x002495A0`), and for
  a file with a size `0x00249210` then adds to the count at address `0x18` (`0x002492F8`), and for any other file the close
  `0x00249410` writes address 0 (`0x00249425`); with all 48 request
  entries in use `0x00249210` stores through a null entry (`0x0024928D`). Each of these faults.
- `0x003C9E50` copies `2h` rows of `w` bytes into `battle_4_c` from the sub-image's top-left corner, writing `w` to
  `0x01EFE384` and `2h` to `0x01EFE388`. It re-uploads the picture and frees the buffer. It returns at once while
  `+0xD0` is null (`0x003C9E65`), does not test what `0x0024A5A0` returns (a miss faults on the header read at
  `0x003C9E8B`), and clears `+0xD0` after the free (`0x003C9F6D`).
- The flags are set by `0x0031A910` and cleared by `0x0031A8C0`; their callers are the handlers of the verbs
  `set_field_effect` (`0x4F5`, `0x00344610`) and `clear_field_effect` (`0x4F6`, `0x00344980`) and `0x002FDDA0`
  ([verb table](../Scripts-And-Script-Commands/verb-table.md)).
  `0x0031A910(mask)` first calls `0x00469C00(mask, 1)` and then ORs the mask into
  `0x022C314C` (`0x0031A916`-`0x0031A922`).
- `0x0031A7B0`, asked by the command check `0x002FFCF0`
  ([command availability](../Battle-Actions/command-availability.md)), refuses a command whose command-record byte
  `+0x1E` is 0, 1, 2 or 3 while bit `0x4`, `0x8`, `0x10` or `0x20` is set, with codes `0x16` to `0x19`.
- `0x0031A7B0` first returns 4 when `0x00322C50(0x14, id, 1)` rejects the id (`0x0031A7D5`), and 0 for a stats record
  whose kind byte `+0x05` is 1 (`0x0031A7EA`) or a row kind above 3; a null stats record goes on to the kind test.
  The row is 0 when the action table slot `0x02EBF138` is 0 or `0x0020E600` resolves its `+0x0C` to null
  (`0x0031A837`), and the kind read at `0x0031A839` then faults.

### The destination pictures and the palette

`0x00280750` registers ten named pictures at `[0x0209AC30] + 0x338` to `+0x380` (`battle_4_c` first,
`mini_face_c` fifth, `partytop_8_c` seventh) and requests `tex2pack_ys.bin`. It returns at once while the pack
buffer `+0x3D8` is set (`0x0028077F`), registers (`0x0024A4E0(name, 2)`) only the slots that are still null
(`0x00280807`), stores the request's buffer at `+0x3D8` (`0x0028086D`), and clears bit `0x80` of `+0x38` in the
entries of `party_grd_2` and `icons_c` when `0x0024A5A0` finds them (`0x00280895`, `0x002808AD`).

`0x00280670` binds the pack's pictures to them in order through `0x0024A1D0`. It does nothing while `+0x3D8` is
null (`0x00280683`), skips a null slot (`0x002806A7`), and gives slot `i` the pack entry at the buffer plus the
u32 at buffer `+ 4i`. It stores entry 10 at `+0x388` only while that is null (`0x002806D3`), then releases the
textures `0x0209AC38` and `0x0209AC40` when set (`0x00183720`) and zeroes them (`0x0028070C`, `0x00280728`).

For format `0x13`, `0x0024A1D0` registers the index plane and one 256-colour palette per 256 CLUT colours under
the picture's name ([TIM2 images](tim2-images.md)).

`0x00181580(name, pixels, width, height, imageType)` refreshes the named texture from the edited index plane:
image type 5 copies the bytes as they are (`0x00180C80`), type 4 splits each byte into two 4-bit indices, low
nibble first (`0x00180A70`). All three destinations are type 5, so each byte of a `bin_menu` image is an
8-bit index into the destination picture's CLUT.

`0x00181580` looks the name up in the texture manager `[0x01F811E8]` (`0x001B11D0`). A name that resolves to no
texture, or an image type other than 4 and 5, does no work: the body calls the no-op `0x0016D6A0` and returns
(`0x001815EF`).

Both copiers map the texture (`0x0017EBD0`) and write nothing when the map fails (`0x00180D57`, `0x00180B4E`). Each
rounds the width and the height up to a power of two in 16 bits, `x = w - 1`, then `x |= x >> 1`, `x |= x >> 2`,
`x |= x >> 4`, `x |= x >> 8` and `p = x + 1` (`0x00180CBF`-`0x00180D2D` in the first), except that a size one below
its power stays as it is, `p - w == 1 ? w : p` (`0x00180D3A`, `0x00180B31`); when either rounded size differs, it
first zeroes the mapped buffer (`memset` `0x00861EC0`, `0x00180DB9`, `0x00180BAD`). With a null mapped pointer it
skips the copy.

`0x00180C80` copies `height` rows of `width` bytes at the mapped pitch (`0x00679570`). `0x00180A70` reads `width / 2`
bytes per row and writes each byte's low nibble, then its high nibble (`0x00180BE0`-`0x00180BF9`). Both then commit
(`0x0062C360`) and, when that returns 0, store the buffer slot at `+0x0C` and 0 at `+0x08` (`0x00180E09`,
`0x00180C3C`).

## Modding notes

- Write palette indices, not colours. The colours come from the destination picture's CLUT in
  `tex2pack_ys.bin`; change that CLUT to recolour.
- A replacement must be `w x h` bytes per cell for its sub-image: 8,192 per `mini_guest_face` cell and 16,384
  for a `map_efe` file. Its size must match the size table entry the request allocates from.
- To paste a guest portrait intact, give `partytop_8_c` a sub-image `0x0003` of the portrait's size.
- `mini_guest_face` holds nine cells, for character ids 7 to 15. A larger `g` reads past the file.
- Area icon `k` is `map_efe0k` for the lowest set flag bit `k`. Only one icon is pasted at a time.

## Related

- [TIM2 images](tim2-images.md): the destination pictures, their CLUTs and the texture binder.
- [UI typed lists](ui-typed-lists.md): the named-picture registry and the sub-image lookup.
- [File size tables](file-size-tables-fst.md): the sizes the requests allocate.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the kind-7 requests.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00322C50` is called by `0x002367A0`, `0x0023A570`, `0x0031B810`, `0x003266C0`, `0x00329CC0`; those functions
  are documented on [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [party data](../Party/party-data.md).
- Combat formula: `0x00322C50` is called by `0x002FEF30`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Items equipment shops license: `0x00322C50` is called by `0x003096F0`, `0x0030B180`, `0x0030B4B0`, `0x0030B510`, `0x0030B570`,
  `0x0030B630`, `0x00317930`, `0x0031A510`, `0x00323910`, `0x00323C60`, `0x00323D10`, `0x00323EC0`; `0x00322C50` is also called by
  `0x00325F40`.
- Items equipment shops license: those functions are documented on [stats](../Damage-And-Battle-Formulas/stats.md),
  [bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md),
  [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md),
  [party table](../Party/party-table.md).
- Items equipment shops license: and on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [quickening and esper list](../Battle-Actions/quickening-and-esper-list.md),
  [command availability](../Battle-Actions/command-availability.md).
- Save load settings: `0x00249210` is called by `0x00582790`; `0x00249410` is called by `0x00582790`; `0x00249580` is called by
  `0x00582790`; those functions are documented on [mrp menu resource packages](mrp-menu-resource-packages.md).
