---
title: "TIM2 images: the PS2-era .tm2 picture format, how the game reads one, and the seven-slot image registry"
kind: "format"
category: "Game files and data tables"
addresses: "0x0024A1D0, 0x0024A480, 0x0024A4E0, 0x002493D0, 0x0208F580, 0x00181000, 0x00180E70, 0x00181250, 0x00181190, 0x0039BEC0, 0x00D11470, 0x02AEE810, 0x0039BF50, 0x0039BDA0, 0x003EFDF0, 0x0039BB60, 0x0039BB30, 0x0039BA30, 0x0039BAD0, 0x0039C150, 0x0039C3F0, 0x0029CAC0, 0x0029CB10, 0x0209C320, 0x0037F1F0, 0x003BC4E0, 0x00575710, 0x0020E600, 0x0020E620"
---

## What the player sees

The menu screens' flat pictures: backdrops, frames, the map screens' location art and line texture, the
handbook and licence pictures. Separately, the font pack, the handbook pages and the map guide carry
4-bit glyph sheets (pictures of pre-rendered text) that are put into a shared image area holding a fixed
number of them at once.

## Where it comes from

Standalone TIM2 files sit in the archive under `ps2data/image/ff12/myoshiok/` as `.tm2` and as the nine
`<language>/quest/menuquest.nfs`. Many more TIM2 images are embedded in other files: packs, `.dat`
handbook bundles, `.ebp` scripts and `.mpk` map packs.

A standalone menu picture is requested as a kind-7 resource with a texture entry: `0x002493D0` files the
request (`0x00249210`), takes an entry from the 64-entry texture table at `0x0208F580` (`0x0024A4E0`, `0x48`
bytes each) and sets the completion `0x00249670`, which jumps to the binder `0x0024A1D0(entry, file)`. The pack
binders call `0x0024A1D0` directly on TIM2s inside a pack (`0x00246A10` binds five from the pack at
`0x0208EA88` by its directory offsets), and `0x0024A480` binds one with a caller-supplied CLUT.

## Layouts

TIM2 file header (16 bytes; the first picture always starts at +`0x10`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "TIM2"; checked by the registry gate (`0x0039BEE3`), not by the binder |
| `+0x04` | `u8` | version | read by neither the binder nor the registry |
| `+0x05` | `u8` | format | read by neither; 0 in every shipped file |
| `+0x06` | `u16` | pictures | picture count; walked by the registry (`0x0039BF50`, `0x0039BDA0`), not by `0x0024A1D0` |
| `+0x08` | `u8[8]` | reserved |  |

Picture header (`0x30` bytes, then the game block or eXt area up to header size):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | totalSize | header + image + CLUT; the registry steps to the next picture by it |
| `+0x04` | `u32` | clutSize |  |
| `+0x08` | `u32` | imageSize | `0x0024A1D0`: CLUT = picture + headerSize + imageSize |
| `+0x0C` | `u16` | headerSize | pixels start at picture + headerSize; > `0x30` marks a game block |
| `+0x0E` | `u16` | clutColors | CLUT colour count (`0x0024A1D0`) |
| `+0x10` | `u8` | pictFormat |  |
| `+0x11` | `u8` | mipmaps |  |
| `+0x12` | `u8` | clutType | passed to the CLUT builders |
| `+0x13` | `u8` | imageType | passed to the CLUT builders |
| `+0x14` | `u16` | width |  |
| `+0x16` | `u16` | height |  |
| `+0x18` | `u64` | gsTex0 | bits 20-25 pick the binder's path; bits 51-54 kept in the entry |
| `+0x20` | `u64` | gsTex1 |  |
| `+0x28` | `u32` | gsRegs |  |
| `+0x2C` | `u32` | gsTexClut |  |

A registered glyph sheet carries a game block at picture `+0x30` instead of an `eXt` area:

Glyph-sheet block (picture +`0x30`; present when headerSize > `0x30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `u32` | flags | low nibble 1 for the gate (file +`0x40` of picture 0); `0x4000` = offsets converted; bits `0x18000` select the sheet in `0x0039BA30` |
| `+0x34` | `u32` | self | written: handle of this picture |
| `+0x38` | `u32` | next | written: handle of the following picture, or of address 0 when that picture has a block |
| `+0x3C` | `u32` | offsetA | offset from +`0x30`, converted once to a handle |
| `+0x44` | `u32` | offsetB | offset from +`0x30`, converted once to a handle |
| `+0x48` | `u32` | offsetC | offset from +`0x30`, converted once to a handle |
| `+0x4C` | `u16` | bandBase | written: `0x2A00` + `0xA0` x (row / 128) |
| `+0x4E` | `u16` | bandRow | written: row mod 128 |

A handle is a 32-bit offset from the base pointer at `0x01F83530`: `0x0020E620` subtracts it and `0x0020E600`
adds it back.

## Shipped data

| Fact | Value |
|---|---|
| standalone files | 456: 447 `.tm2` (318,584,160 bytes, 1,344 to 4,195,456 each) and 9 `.nfs` (47,584 bytes, 208 to 29,008) |
| folders | `<lang>/tm2_menu` 396 (40 in `us`, `it`, `in`, `fr`, `es`, `de`; 39 in `kr`, `in_sdver`, `cn`, `ch`), `in/worldmap/bin/areatim2` 39, `in/quest/questtim2` 6, `ch/quest/questtim2` 6, `<lang>/quest/menuquest.nfs` 9 |
| magic, format byte | `TIM2` and `+0x05` = 0 in all 456 |
| version byte `+0x04` | `0xD8` in 437, 4 in 19 (12 `.tm2`: the `w_line01`, `w_line02` and `lic_over` pictures; 7 `.nfs`) |
| pictures | 1 in 455; 2 in `in/quest/menuquest.nfs` |
| sizes | in all 456 every picture's total is header + image + CLUT and the pictures end exactly at the end of the file |
| `.tm2` pixel formats | TEX0 PSM `0x13` with image type 5 in 441, PSM `0x14` with image type 4 in 6; CLUT type 3 in all 447 |
| `.tm2` dimensions | width and height powers of two in all 447; 1024 x 1024 in 138, 512 x 512 in 63, 128 x 128 in 48; 22 distinct sizes |
| `.tm2` CLUT colours | 8-bit pictures: 256 in 282, then multiples of 256 up to 16,384 (36 have 4,096); 4-bit: 16 to 272 |
| `.tm2` header size | `0x30` in 30; larger in 417, all with `eXt\0` at picture `+0x30` |
| `.nfs` | 4-bit, no CLUT, TEX0 zero, widths 16 to 640 (not powers of two), a game block whose first dword ends `0x2F41` |
| gate value (low nibble of file `+0x40`) | 5 in 417, 0 in 19, `0xC` in 10, 1 in 10: the nine `.nfs` and `in_sdver/tm2_menu/w_line01.tm2`, whose `0x30`-byte header puts pixel bytes `01 01 01 01` there |
| embedded TIM2 (under `ps2data/`) | `.mpk` 21,419 in 459 files, `.dat` 6,767 in 2,795, `.ebp` 5,430 in 4,695, `.bin` 3,267 in 492; all at 16-byte-aligned offsets |
| embedded glyph sheets | block tag `0x2F41`: `.ebp` 2,150, `.dat` 74, `.bin` 36; tag `0xAF41`: `.ebp` 569 |
| font pack (`packfiles/fontpack_it.bin`, 6 languages) | directory dwords 0 to 5 are offsets, 6 and 7 are `0xFFFFFFFF`; entry 0 a two-picture 4-bit sheet 640 wide (225 rows `us`, 1,646 `cn`), entry 1 a 32 x 16 picture of image type 3 |
| script glyph sheets (`us`) | 67 scripts carry a TIM2 in section 6: 58 with one picture, 9 with two; version 4 in 66 and `0xD8` in one; all 4-bit (`imageType` 4); first picture 24 x 23 in 55; gate nibble 1 in all 67 |

## Loader behaviour

### The texture binder

`0x0024A1D0(entry, file)` reads only the first picture and never checks the magic, version, format byte or
picture count:

- It stores the file at entry `+0x18` and picture `+0x10` at `+0x20`, copies TEX0 bits 20-25 (the PSM)
  into entry `+0x38` bits 8-13 and bits 51-54 into bits 14-17, and names the texture from the entry's
  name, or the name plus `%03d` of entry `+0x40`.
- PSM `0x13`: the pixels (`0x00181250`) and the CLUT (`0x00181000`) are registered; PSM `0x14`: `0x00181190` and
  `0x00180E70`. Any other PSM registers nothing, and the entry is still marked bound (`+0x38` bit `0x40`).
- `0x00181250` and `0x00181190` pass the pixels, width, height and both rounded up to a power of two to
  `0x00184140` (8-bit) or `0x00183EE0` (4-bit), then register the texture under the name (`0x001B21D0`).
- `0x00181000` registers one 256-colour palette per 256 CLUT colours (`0x400` bytes apart, `0x001B20B0`);
  `0x00180E70` one 16-colour palette per 16 colours (`0x40` apart). Both reorder when
  `clutType << 8 | imageType` is `0x105`, `0x205`, `0x305`, `0x4104`, `0x4204` or `0x4304`.
- The reorder swaps bits 3 and 4 of each colour index within a 256-colour palette. In a 16-colour palette
  it moves colours 8 to 15 outside the palette and leaves those entries unfilled.
- For PSM `0x14` the binder also keeps a copy of the CLUT at entry `+0x10` with the same bit 3 and 4
  swap; for `0x13` the entry points at the file's CLUT. A CLUT given to `0x0024A480` (entry `+0x28`, count in `+0x38` bits 18 up)
  replaces the file's.

### The registry gate

`0x0039BEC0(buffer)` registers a loaded glyph sheet and returns its slot, or 0:

- null buffer: 0 (`0x0039BEC9`);
- the first four bytes are compared with `"TIM2"` at `0x00D11470` (`0x0039BEE3`, `strncmp` with 4); any
  difference: 0;
- the low nibble of the dword at file `+0x40`, the first picture's block flags, must be 1
  (`0x0039BEF0`–`0x0039BEF4`), or 0;
- slots 1 to 7 of `0x02AEE810` are scanned for the first empty one (`0x0039BF02`, `0x0039BF1C`); none: 0;
- the buffer is stored there, `0x0039BF50` lays out every slot again, and the slot number is returned.

The compare at `0x0039BF31` tests the empty slot against the buffer, so it never matches: registering the
same buffer twice takes two slots. Nothing else in the header is checked.

### The registry

`0x02AEE810` holds eight buffer pointers. Slots 1 to 7 are handed out by `0x0039BEC0`; slot 0 and slot 7 are
also written by the font-pack completion `0x0039C150`.

- Font pack: `0x0039C3F0` requests kind 7, id `0xD5` into `0x02AEE868` with completion `0x0039C150`. That fills
  an empty slot 0 with the pack's directory entry 0, and an empty slot 7 with entry 6 when entry 6 is not
  `0xFFFFFFFF` and the language test `0x00254A10` is false. It then calls `0x0039BF50` and sets the ready byte
  `0x02AEE890`.
- `0x0029CAC0(buffer)` (from `0x00330060`) keeps a six-entry `{pointer, count}` table at `0x0209C320`: a buffer
  already there has its count raised and is not registered again; a new one takes an empty entry with
  count 1 and goes to `0x0039BEC0`; with six in use nothing happens. `0x0029CB10` lowers the count and, at 0,
  unregisters the buffer.
- `0x0037F1F0`, on a request record whose type byte is 4, registers the buffer and calls `0x0017FBC0(5)`; `0x0037F860`
  unregisters it with `0x0017FA70(5)`.
- `0x003BC4E0`, the map-data widget, registers the TIM2 inside the guide file it holds at `+0xF8` (at that
  file's u16 `+0x0A`, `0xFFFF` for none, `0x003BD8F0`), with `0x0017FBC0(4)`; it, `0x003BBFB0` and `0x003BC970`
  unregister it with `0x0017FA70(4)`.
- `0x00575710`, the handbook page, registers the TIM2 at the bundle's i32 `+0x0C` (unless -1), with
  `0x0017FBC0(6)` when its kind byte `+0xD2` is 4; `0x00575640` unregisters it.
- `0x0039BB60(buffer)` clears the first of slots 1 to 7 whose low 32 bits equal the buffer's and lays out
  every slot again; a buffer not found changes nothing.
- `0x0039BB30` (from `0x0029CE40`, which also zeroes the `0x0209C320` table) clears `0xF0` bytes from
  `0x02AEE810`, including the font-pack pointer, and calls `0x0039C3F0`, which requests the pack again.

The table `0x0209C320` holds six 16-byte entries, a buffer pointer at `+0x00` and a count at `+0x08`. `0x0029CE40` zeroes
every entry with plain stores (`0x0029CE7A`-`0x0029CEC2`); `0x0029CAC0` and `0x0029CB10` reach the entries only through the
table's address. All are 0 in the file (the zero-filled tail of `.data`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209C330`, `0x0209C340`, `0x0209C350`, `0x0209C360`, `0x0209C370` | `void*` each | 0 | the buffers of entries 1 to 5, 0 for an empty entry | `0x0029CE40` (`0x0029CE87`, `0x0029CE94`, `0x0029CEA1`, `0x0029CEAE`, `0x0029CEBB`); through the address: `0x0029CAC0`, a new buffer (`0x0029CAF4`), and `0x0029CB10`, 0 at a count of 0 (`0x0029CB41`) | through the address: `0x0029CAC0` (`0x0029CAD0`, `0x0029CAE2`); `0x0029CB10` (`0x0029CB20`) |
| `0x0209C328`, `0x0209C338`, `0x0209C348`, `0x0209C358`, `0x0209C368`, `0x0209C378` | `i32` each | 0 | the counts of entries 0 to 5 | `0x0029CE40` (`0x0029CE81`, `0x0029CE8E`, `0x0029CE9B`, `0x0029CEA8`, `0x0029CEB5`, `0x0029CEC2`); through the address: `0x0029CAC0`, 1 for a new buffer (`0x0029CAF7`) and one more for a known one (`0x0029CB03`), and `0x0029CB10`, one less (`0x0029CB36`) | through the address: `0x0029CAC0` (`0x0029CB03`); `0x0029CB10` (`0x0029CB36`) |

No other instruction reaches these globals: no other RIP-relative, image-base-relative or 32-bit offset reference
names them, and the table's address is taken only by `0x0029CAC0` and `0x0029CB10`.

`0x0039BAD0(buffer)` returns the slot from 1 to 7 whose low 32 bits match, or 0. `0x0039BA30(slot, mode)`
returns null for an empty slot, else the first picture's block (picture `+0x30`). With mode 0 it returns
null when that block's flags have a bit of `0x18000` set. With a non-zero mode and `0x00254A10` true it
returns the first block whose flags have `0x8000` and not `0x10000`, or null.

### Script glyph sheets (EBP section 6)

A script container (`.ebp`) can carry a glyph sheet in directory slot 6
([script container](../EBP-Script-Files/ebp-script-container.md)). When the container arrives,
`0x003304A0` passes that section, with the area slot in the low four bits, to `0x00330060` (`0x00330565`), which:

1. stores it at `0x022C6CF0[g]` and in the area record (`0x0026C860`, `0x02098EC0 + g × 0x288`);
2. clears pending bit `0x40` of `0x022C6E48[g]`;
3. hands it to the text layer (`0x0017F790` → `0x001B47A0`, which gives it to the first waiting font entry whose
   id matches the packed value, or logs a load failure and attaches nothing when none does);
4. registers it through `0x0029CAC0`.

`0x001B4590(font, entry)` is that attach (`0x001B483F`): it places the entry in the first empty of the font's
16 slots at `+0x278` (nothing happens when all are taken) and registers the slot with the text renderer
`[0x01F811F8]` through `0x001E7F90`: by the entry's kind `+0x18` alone while its byte `+0x00` is clear, otherwise
through the list the key `(font id << 5) + kind` finds in the font's tree at `+0x30` (kinds 2 and 3 when
`+0x18` is 0), when `0x001FDD60(list, entry +0x14)` accepts it. `0x001B6510` attaches an entry the same way.

### Layout and upload

`0x0039BF50` walks slots 0 to 7 and, in each, the pictures by `totalSize`, keeping one row counter across all
slots. Each picture with a block gets `self`, `next`, `bandBase` and `bandRow` for the current row; the
three offsets are converted only while flag `0x4000` is clear, which the pass then sets. The counter then
grows by the picture's height, and the walk of a slot stops once the counter exceeds 60 times the dword at
`0x01E0CDC4` (23 in the executable).

`0x0039BDA0`, called from the screen bodies (`0x00252840`, `0x002528A0`, `0x00252990`, `0x00252A20`, `0x00252A70`)
once `0x02AEE890` is set, sends the font pack's 32 x 16 picture to block `0x32FC` and then every picture of
every slot to block `0x2A00`, 640 pixels wide, 4-bit (PSM `0x14`), at `x = 0` and `y` = the same running
row, `width` x `height` from the picture header. `0x003EFDF0` builds each transfer: GS registers `0x50` to
`0x53`, the pixels from `picture + headerSize`, then `0x3F`.

## Modding notes

- Keep a replacement `.tm2` a single 16-byte-aligned picture at `+0x10`: the binder reads no picture count
  and no format byte, and only the first picture.
- The PSM in TEX0 (`+0x28` of the file, bits 20-25) must be `0x13` (8-bit) or `0x14` (4-bit); any other
  value leaves the texture unregistered. The image type and CLUT type decide whether the CLUT is reordered;
  a 4-bit picture should keep CLUT type 3 as shipped, since `0x41` to `0x43` break its 16-colour palettes.
- An 8-bit picture gets one palette per 256 CLUT colours and a 4-bit one per 16; `clutColors` must match
  the CLUT that follows the pixels.
- A glyph sheet for the registry needs `headerSize` above `0x30` and a block whose first dword has low
  nibble 1; its pixels are uploaded as 4-bit rows at most 640 wide.
- At most seven registered sheets fit in slots 1 to 7, fewer when slot 7 is the font pack's. An eighth
  returns 0, the same as a bad header, and the caller gets no image.
- Registry matches use the low 32 bits of the buffer address (`0x0039BB60`, `0x0039BAD0`), and `0x00575710` and
  `0x003BD8F0` form the sheet's address with 32-bit arithmetic (`0x00575763`).

## Related

- [File requests and the read queue](file-requests-and-the-read-queue.md): how a kind-7 request reaches its completion.
- [Bigfile archive](bigfile-archive.md): where the `.tm2` and `.nfs` files are stored.
- [Map screens](../Menus-And-HUD/map-screens.md): the location art, the line texture and the map-data widget.
- [Clan Primer](../Menus-And-HUD/clan-primer.md): the handbook pages that register their glyph sheets.
- [Fonts](../Menus-And-HUD/fonts.md): the PC font files.
