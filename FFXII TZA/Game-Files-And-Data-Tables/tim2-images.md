[Home](../../README.md) / [Game files and data tables](README.md) / TIM2 images

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| TIM2 images: the PS2-era .tm2 picture format, how the game reads one, and the seven-slot image registry | format | Game files and data tables | Image files | The TIM2 container behind the 447 .tm2 menu pictures, the nine menuquest.nfs glyph sheets and thousands of images embedded in packs, scripts and map files: the file and picture headers as the texture binder 0x0024A1D0 and the image registry read them, the 4-bit glyph-sheet block at picture +0x30, the eight-entry registry at 0x02AEE810 with its seven caller slots and its fillers and clearers, the shipped header values, and the rules a replacement must follow. | 0x0024A1D0, 0x0024A480, 0x0024A4E0, 0x002493D0, 0x0208F580, 0x00181000, 0x00180E70, 0x00181250, 0x00181190, 0x0039BEC0, 0x00D11470, 0x02AEE810, 0x0039BF50, 0x0039BDA0, 0x003EFDF0, 0x0039BB60, 0x0039BB30, 0x0039BA30, 0x0039BAD0, 0x0039C150, 0x0039C3F0, 0x0029CAC0, 0x0029CB10, 0x0209C320, 0x0037F1F0, 0x003BC4E0, 0x00575710, 0x0020E600, 0x0020E620 |

## What the player sees

The menu screens' flat pictures: backdrops, frames, the map screens' location art and line texture, the
handbook and licence pictures. Separately, the font pack, the handbook pages and the map guide carry
4-bit glyph sheets (pictures of pre-rendered text) that are put into a shared image area holding a fixed
number of them at once.

## Where it comes from

Standalone TIM2 files sit in the archive under `ps2data/image/ff12/myoshiok/` as `.tm2` and as the nine
`<language>/quest/menuquest.nfs`. Many more TIM2 images are embedded in other files: packs, `.dat`
handbook bundles, `.ebp` scripts and `.mpk` map packs.

A TIM2 picture holds a grid of colour numbers followed by its palette. When the file arrives the game makes a texture
from the grid and one palette for every 256 colours, or every 16 for a 4-bit picture, and names them with the name the
requesting screen gave.

A standalone menu picture is requested as a kind-7 resource with a texture entry: `0x002493D0` files the
request (`0x00249210` with a last argument of 1, so the buffer is taken top-down with `0x0036A190`), takes an entry
from the 64-entry texture table at `0x0208F580` (`0x0024A4E0` with the caller's name and flags, `0x48` bytes each)
and stores it at request `+0x18` (`0x002493FB`). It sets the completion `0x00249670` at request `+0x10`
(`0x002493FF`), which jumps to the binder `0x0024A1D0(entry, file)`, and returns the entry.

Nothing tests the entry: with all 64 entries busy it is null, and when the file arrives the binder faults on its
read of entry `+0x40` (`0x0024A206`). The pack binders call `0x0024A1D0` directly on TIM2s inside a pack (`0x00246A10`
binds five from the pack at `0x0208EA88` by its directory offsets), and `0x0024A480` binds one with a caller-supplied
CLUT.

## Layouts

All multi-byte fields are little-endian.

TIM2 file header (16 bytes; the first picture always starts at `+0x10`):

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
| `+0x18` | `u64` | gsTex0 | the bits under mask `0x3F00000` pick the binder's path; mask `0x78000000000000` kept in the entry |
| `+0x20` | `u64` | gsTex1 |  |
| `+0x28` | `u32` | gsRegs |  |
| `+0x2C` | `u32` | gsTexClut |  |

A registered glyph sheet carries a game block at picture `+0x30` instead of an `eXt` area:

Glyph-sheet block (picture `+0x30`; present when headerSize > `0x30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `u32` | flags | low nibble 1 for the gate (file `+0x40` of picture 0); `0x4000` = offsets converted; bits `0x18000` select the sheet in `0x0039BA30` |
| `+0x34` | `u32` | self | written: handle of this picture |
| `+0x38` | `u32` | next | written: handle of the following picture, or of address 0 when that picture has a block |
| `+0x3C` | `u32` | offsetA | offset from `+0x30`, converted once to a handle |
| `+0x44` | `u32` | offsetB | offset from `+0x30`, converted once to a handle |
| `+0x48` | `u32` | offsetC | offset from `+0x30`, converted once to a handle |
| `+0x4C` | `u16` | bandBase | written: `0x2A00` + `0xA0` x (row / 128) |
| `+0x4E` | `u16` | bandRow | written: row mod 128 |

A handle is a 32-bit offset from the base pointer at `0x01F83530`: `0x0020E620` subtracts it and `0x0020E600`
adds it back.

A standalone `.tm2` picture whose header is longer than `0x30` bytes carries an `eXt` block at picture `+0x30`
instead. It lists the picture's sprites: a menu draws a sprite as a rectangle of the picture with its own palette
([Menu sprites](../Menus-And-HUD/menu-sprites.md), "Finding a sprite"; [Typed UI lists](ui-typed-lists.md), "Sub-image
lookup").

EXt block (picture `+0x30`; present when headerSize > `0x30`; offsets in the block are from `+0x30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `char[4]` | tag | "eXt\0" |
| `+0x34` | `u32` | size | headerSize - `0x30` |
| `+0x38` | `u32` | size2 | headerSize - `0x30` |
| `+0x3C` | `u32` | zero | 0 |
| `+0x40` | `u16` | recordsOff | records start at `+0x30` + recordsOff; 48 or 64 (`0x0029F59E`, `0x00242634`) |
| `+0x42` | `u16` | paletteOff | palette table at `+0x30` + paletteOff; always recordsOff - 16 (`0x0029F6A6`) |
| `+0x44` | `u16[]` | index | up to the palette table: 6 entries when recordsOff is 48, 14 when 64 index[0]            the set count, and also where set 0's group list starts index[s]            for each set s: where its group list starts, as a position in index[] group lists         per set, the first record of each group; unused entries are 0 |

```
+0x30+paletteOff  u8[16]     palette base of each palette group
+0x30+recordsOff  record[]   8 bytes each, up to headerSize; there is no count field
```

Sprite record (8 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | x |  |
| `+0x02` | `u16` | y |  |
| `+0x04` | `u32` |  | bits 0-11 width, bits 12-23 height, bits 24-27 palette added, bits 28-31 palette group palette = palette table[group] + added |

A sprite is named by a code, `set << 8 | group`, and a frame; its record is record
`index[index[set] + group] + frame`. `0x0029F580` binds the code's first record to a widget: it reads the code from
the widget template `+0x0E` and stores the record address at widget `+0x20` (`0x0029F586`-`0x0029F5BC`). The draw
`0x0029F5D0` then takes record `widget +0x0A` from that address (`0x0029F5DA`-`0x0029F622`), looks the palette up
through `paletteOff` (`0x0029F65E`-`0x0029F6B4`) and writes the palette number to the draw context `+0x5C`
(`0x0029F6BC`).

The set count in `index[0]` is read only as set 0's start: neither the code nor the frame is checked against
the table. The tag and the three dwords after it are read by none of the 87 functions that compute a record
address.

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
| `.tm2` dimensions | width and height powers of two in all 447; 1024 x 1024 in 138, 512 x 512 in 63, 128 x 128 in 48; 16 distinct sizes; one mipmap level in all 447 |
| `.tm2` CLUT colours | 8-bit pictures: 256 in 282, then multiples of 256 up to 16,384 (36 have 4,096); 4-bit: 16 to 272 |
| `.tm2` header size | `0x30` in 30; larger in 417, all with `eXt\0` at picture `+0x30`, the two size dwords equal to the header size minus `0x30` and the third 0 |
| `eXt` record and palette offsets | 48 and 32 in 367 files, 64 and 48 in 50 (`loca_8_c`, `w_icon_p`, `hand_4_c`, `lic_4_c` and `lic_8_c` in every folder that has them) |
| `eXt` sets and groups | one set of one group in 287 (all 39 `areatim2`, all 12 `questtim2`, 236 `tm2_menu`); several groups or sets in 13 names, 10 files each: `dataface_c` 2 sets, `hand_4_c` 2, `maru_c_2` 3, `lic_4_c` and `lic_8_c` 4, and one set of 2 to 11 groups in `lic_8_c2`, `lic_b_8_c`, `loca_8_c`, `medal_c`, `shop_8_c`, `title_c`, `w_icon_p` and `w_win_c` |
| `eXt` records | 7,266 in the 417 files, 2 to 158 each (2 in 209 files); 323 all-zero records, every one after the last used record; group starts below the record count and rising within each set in all 417 |
| records outside their picture | 7, all in `in_sdver/tm2_menu`: `hand_4_c` records 0 to 2 keep the `us` x halved (193, 195, 198) on a picture of width 128; `lic_4_c` record 39 ends at row 144 of 128; `lic_8_c` records 125 to 127 start at row 512 of 512 |
| palette past the CLUT | `medal_c` records 1 to 3 name palette 1 in all 10 folders; the picture has one 256-colour palette |
| every `eXt` block | one row per file in [`tim2-images-ext.tsv`](tim2-images-ext.tsv), 417 rows: header size, both offsets, the index table split into sets and groups, record and zero-record counts, the palette table, the largest palette named, the CLUT's palette count, width, height and PSM |
| every sprite record | one row per record in [`tim2-images-sprites.tsv`](tim2-images-sprites.tsv), 26,752 rows: the 7,266 of the standalone files and the 19,486 of the 149 `texpack_ys.bin` and `tex2pack_ys.bin` pictures. Each row gives the `picture` (a file, or pack`#`entry), its `atlas` name, `folder`, `record`, `set`, `group`, `frame`, the rectangle, `palette_group`, `palette_added`, the `palette` they give, and a `status`: `ok` (26,223), `zero` (390), `outside the picture` (8) or `palette past the CLUT` (131). A count of records is not a count of usable icons, because the zero and out-of-range records are listed too |
| every standalone file | one row per picture in [`tim2-images-files-rows.tsv`](tim2-images-files-rows.tsv), 457 rows for the 456 files: size and SHA-256 prefix, version, picture count, every picture header field, whether the `eXt` block follows, and the gate nibble |
| every `.tm2` and its path | one row per file in [`tim2-images-tm2-files.tsv`](tim2-images-tm2-files.tsv), 447 rows: folder, path, size, SHA-256, the kind 7 ids and languages whose path array names it, the languages whose size table gives that id the file's size, the `in_sdver` entry, the pack entries with the same bytes, and how many prefetch lists name it |
| named by a kind 7 array | 402: every `.tm2` under `us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn` and `ch` except `title_logo_fore3.tm2`; each naming language's size table gives the id the file's size |
| named by no path array | 45: `title_logo_fore3.tm2` in `us`, `de`, `es`, `fr`, `it` and `in` (526,496 bytes each), and the 39 `in_sdver/tm2_menu` files. `0x002DF9A0` points kind 7 ids at the `in_sdver` paths only when its second argument is 0 (`0x002DFF86`-`0x002E03EE`); the word it passes, `[0x01E0280C]`, ships as 1 ([Asset paths](asset-paths.md)) |
| named but not shipped | kind 7 id 141, `logo_s_c.tm2`: every language's array names it in its own folder, and the `in_sdver` entries name an `in_sdver` copy; no folder ships it and no size table sizes the id |
| pack directories | the six `packfiles` packs' directories hold offsets, not names ([PS2Data bin families](ps2data-bin-families.md)); no pack entry has the bytes of a `.tm2` file |
| `.nfs` | 4-bit, no CLUT, TEX0 zero, widths 16 to 640 (16 in `es` and `fr`; 24, 360, 504, 520 and 640, not powers of two, in the others), a game block whose first dword ends `0x2F41` |
| gate value (low nibble of file `+0x40`) | 5 in 417, 0 in 19, `0xC` in 10, 1 in 10: the nine `.nfs` and `in_sdver/tm2_menu/w_line01.tm2`, whose `0x30`-byte header puts pixel bytes `01 01 01 01` there |
| embedded TIM2 (under `ps2data/`) | `.mpk` 21,419 in 459 files, `.dat` 6,767 in 2,795, `.ebp` 5,430 in 4,695, `.bin` 3,703 in 492 (all under `image/ff12/myoshiok`); all at 16-byte-aligned offsets; the last TIM2 of each of the 436 `worldmap/menumap_sub*.bin` files ends 448 to 960 bytes past the end of its file, inside its CLUT |
| embedded glyph sheets | block tag `0x2F41`: `.ebp` 2,150, `.dat` 74, `.bin` 36; tag `0xAF41`: `.ebp` 664 pictures in 664 files, 569 of them the first picture |
| font pack (`packfiles/fontpack_it.bin`, 6 languages) | directory dwords 0 to 5 are offsets, 6 and 7 are `0xFFFFFFFF`; entry 0 a two-picture 4-bit sheet 640 wide (225 rows `us`, 1,646 `cn`), entry 1 a 32 x 16 picture of image type 3 |
| script glyph sheets (`us`) | 67 scripts carry a TIM2 in section 6: 58 with one picture, 9 with two; version 4 in 66 and `0xD8` in one; all 4-bit (`imageType` 4); first picture 24 x 23 in 55; gate nibble 1 in all 67 |

### Who requests each picture

The 408 `.tm2` files outside `in_sdver` are 40 `tm2_menu` names (39 in `kr`, `cn` and `ch`, which lack
`title_logo_fore3`), the six `questtim2` pictures in `in` and `ch`, and the 39 `areatim2` pictures in `in`. The
requester of each kind 7 id comes from the request sites of
[PS2Data bin families](ps2data-bin-families.md) Request entries, with the ids the callers compute or read from
their tables:

| Pictures (kind 7 id) | Files | Requested by | Screen |
|---|---:|---|---|
| `cm2_win_c` (`0x2B`), `lic_8_c` (`0x78`), `lic_bk` (`0x7A`), `lic_8_c2` (`0x7C`), `lic_8_c3` (`0x7D`) | 45 | `0x00561390` (`0x0056169E`-`0x0056175E`) | the License Board ([License board screen](../Menus-And-HUD/license-board-screen.md)) |
| `maru_c` (`0x70`), `maru_c_2` (`0x71`), `lic_b_8_c` (`0x76`), `lic_b_4_c` (`0x77`) | 36 | the chooser window `0x00558FB0` (`0x0055926E`-`0x005592FE`) | the board chooser (same page) |
| `lic_4_c` (`0x79`) | 9 | `0x00556500` (`0x00556541`), from the start-up step `0x0022A4B0` | the License Board (same page) |
| `gameover_c` (`0x39`) | 9 | the game-over task `0x003EF830`, entry 0 of the table `0x00D11C88` (`0x003EF9C4`, through `0x00393460`) | the game-over screen ([Game over](../World-Areas-And-Travel/game-over.md)) |
| `title_logo` (`0x3D`) | 9 | `0x00393FF0` (`0x00394029`) | the screen that also loads `title.mrp` ([Menu resource packages](mrp-menu-resource-packages.md)) |
| `sf_logo_c` (`0x47`) | 9 | the staff-roll loader `0x0053EB90` (`0x0053ECDF`) | the staff roll ([Staff roll](../Menus-And-HUD/staff-roll.md)) |
| `shop_8_c` (`0x63`) | 9 | `0x002CBD50` (`0x002CBD85`), from `0x0057B780` | the shops ([Shop screens](../Menus-And-HUD/shop-screens.md)) |
| `dataface_c` (`0x7F`) | 9 | the save and load setup `0x00582790`, table `0x00D23D80` (`0x005827BC`, through `0x00393460`) | saving and loading ([Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md)) |
| `itemgra_c` (`0x98`) | 9 | `0x00291C80` from `0x0022A4B0` (`0x00291D04`) | the item pictures ([Menu graphics (.as7)](as7-menu-graphics.md)) |
| `w_shade_p`, `w_main0` to `w_main3`, `w_icon_p`, `w_line01`, `w_line02` (`0xAA` to `0xB1`) | 72 | `0x00562F90`, entries 0 to 7 of `0x00D231C0` (`0x0056301F`); `w_line01` also `0x00404060` (`0x004040F0`) | the World Map ([Map screens](../Menus-And-HUD/map-screens.md), [World map mesh](world-map-mesh-mg.md)) |
| `loca_8_c` (`0xB9`), `locaback_c` (`0xBA`) | 18 | the location-map resources `0x00404060` (`0x00404093`, `0x004040C2`) | the location map ([Map screens](../Menus-And-HUD/map-screens.md)) |
| `q_under_c` (`0xC0`), `q_c00` to `q_c05` (`0xC1` to `0xC6`) | 21 | the Clan Primer hunt list `0x00579AF0`, table `0x00D237E0` (`0x00579F50`, through `0x00393460`) | the Hunts page ([Clan Primer](../Menus-And-HUD/clan-primer.md)) |
| `hand_4_c` (`0xCD`), `handback_c` (`0xCE`) | 18 | the Clan Primer back panel `0x00574E80`, table `0x00D23628` (`0x00574F78`, through `0x003934F0`) | the Clan Primer |
| `medal_c` (`0xCF`) | 9 | `0x00572D80`, table `0x00D23668` (`0x00572DAC`, through `0x00393460`), from the Sky Pirate's Den page `0x00572E10` | the Clan Primer |
| `handback2_c` (`0xD0`) | 9 | `0x0056F2A0` (`0x0056F39B`), from `0x00574E80` | the Bestiary page of the Clan Primer |
| `tuto_win_c` (`0xD8`) | 9 | the task `0x002D6EE0` of the script verb `fsmenu_loadresource` (`0x002D6F59`, through `0x00249380`) | loaded when a script runs `fsmenu_loadresource` ([Menu screens](../Menus-And-HUD/menu-screens.md)) |
| `loca_01` to `loca_38` (`0xE9` to `0x10E`) | 38 | `0x003C1D70(area)`, `0xE8` + the area's picture byte (`0x003C1DB4`-`0x003C1DC2`), for the World Map host `0x005632C0`; area n's picture byte is n in every `menumap_world.bin` ([`menu-map-files-wmap-rows.tsv`](menu-map-files-wmap-rows.tsv)), so `loca_NN` is the picture of World Map area NN | the World Map ([Map menu files](menu-map-files.md)) |

Of these request sites, the 70 kind 7 request sites pass no id of `title_c` (`0x3C`), `titlemenu1`
(`0x3E`), `titlemenu2` (`0x3F`), `lic_over` (`0x7B`), `w_win_c` (`0xB2`), `map_gra_c` (`0xB3`) or `l_mapunder`
(`0xB7`): 63 files. `0x00562F90` skips entries 8 and 9 of `0x00D231C0` (`0x00562FE0`-`0x00562FE8`), the names
`w_win_c` and `map_gra_c`. `loca_00` (`0xE8`), the picture of area 0, is not requested by `0x003C1D70`, which
returns for area 0 before the request (`0x003C1D92`-`0x003C1D95`). The six `title_logo_fore3.tm2` files have no kind
7 id (named by no path array, above).

A kind 7 site, formula or table therefore gives the id of 338 of the 408 pictures with the shipped data, and no id
of the other 70: the 63 copies of those seven names,
`loca_00` and the six `title_logo_fore3.tm2`. [`myoshiok-file-meanings.tsv`](myoshiok-file-meanings.tsv) gives every
picture's kind 7 id, request site, screen and use.

`0x00579AF0` loads `q_c00` to `q_c05` as entries 0 to 5 of `0x00D237E0` (ids `0xC1` to `0xC6`, label `q_img_c`) and
`q_under_c` as entry 6. The Hunts row builder `0x00577C30` picks sheet `2 x (picture / 24)`, plus 1 once the hunt is
done, and the cell `picture % 24` (`0x00577CE0`-`0x00577CFF`); a sheet number of 6 or more gives sheet 0
(`0x00577CEE`-`0x00577CF1`). The hunts' pictures run from 19 to 63 ([Quest menu files](quest-menu-files.md)).

The sheets are those seven files: `0x00579AF0` stores their requests at `[0x02CA9748] + 0xD8` (`0x00579F2F`-`0x00579F50`,
`0x003934B7`), creates the Hunts pane through `0x00577F00` with that address (`0x00579CD8`-`0x00579CFF`), the pane keeps
it at `+0xC8` (`0x0057800F`), and `0x005780D0` hands it to `0x00577C30` as the sheet array (`0x0057810A`-`0x00578116`).

## Loader behaviour

### The texture binder

`0x0024A1D0(entry, file)` reads only the first picture and never checks the magic, version, format byte or
picture count:

- It stores the file at entry `+0x18` and picture `+0x10` at `+0x20`, copies TEX0 bits under mask `0x3F00000` (the PSM)
  into entry `+0x38` bits `0x3F00` and the bits under mask `0x78000000000000` into the bits under mask `0x3C000`, and names the texture from the entry's
  name, or the name plus `%03d` of entry `+0x40`.
- PSM `0x13`: the pixels (`0x00181250`) and the CLUT (`0x00181000`) are registered; PSM `0x14`: `0x00181190` and
  `0x00180E70`. Any other PSM registers nothing, and the entry is still marked bound (`+0x38` bit `0x40`).
- `0x00181250` and `0x00181190` pass the pixels, width, height and both rounded up to a power of two to
  `0x00184140` (8-bit, `0x001812E3`) or `0x00183EE0` (4-bit, `0x00181223`), then register the texture that call returns
  under the name with `0x001B21D0` on the sprite batcher `[0x01F811E8]` (`0x001B1C00`), as a tail jump (`0x00181308`,
  `0x00181248`).
- `0x00181000` registers one 256-colour palette per 256 CLUT colours (`0x400` bytes apart, `0x001B20B0`);
  `0x00180E70` one 16-colour palette per 16 colours (`0x40` apart). Both reorder when
  `clutType << 8 | imageType` is `0x105`, `0x205`, `0x305`, `0x4104`, `0x4204` or `0x4304`.
- The reorder swaps bits `0x8` and `0x10` of each colour index within a 256-colour palette. In a 16-colour palette
  it moves colours 8 to 15 outside the palette and leaves those entries unfilled.
- For PSM `0x14` the binder also keeps a copy of the CLUT at entry `+0x10` with the same bit `0x8` and `0x10`
  swap; for `0x13` the entry points at the file's CLUT. A CLUT given to `0x0024A480` (entry `+0x28`, count in
  `+0x38` the bits from `0x40000` up) replaces the file's when its colour count is below `0x4000`
  (`0x0024A4AA`); with a larger count `0x0024A480` stores neither, and the file's CLUT is used.
- The `0x14` copy is a block of `((colours + 255) >> 8) × 0x400` bytes from `0x0036A190` in arena 3
  (`0x0036C1D0(3, 12)`, popped by `0x0036C140`), filled with `colours >> 4` groups of 16 (`0x0024A2A0`-`0x0024A32E`).
  Nothing checks the block: a null one makes the first store write at address 0, which faults, whenever there are
  16 colours or more (`0x0024A304`).
- After naming the texture the binder stores `0x00181520(entry)` at entry `+0x44` (`0x0024A25E`-`0x0024A266`).

### The registry gate

`0x0039BEC0(buffer)` registers a loaded glyph sheet and returns its slot, or 0:

- null buffer: 0 (`0x0039BEC9`);
- the first four bytes are compared with `"TIM2"` at `0x00D11470` (`0x0039BEE3`, `strncmp` with 4); any
  difference: 0;
- the low nibble of the dword at file `+0x40`, the first picture's block flags, must be 1
  (`0x0039BEF0`–`0x0039BEF4`), or 0;
- slots 1 to 7 of `0x02AEE810` are scanned for the first empty one (`0x0039BF02`, `0x0039BF1C`); with no empty slot: 0;
- the buffer is stored there, `0x0039BF50` lays out every slot again, and the slot number is returned.

The compare at `0x0039BF31` tests the empty slot against the buffer, so it never matches: registering the
same buffer twice takes two slots. Nothing else in the header is checked.

### The registry

`0x02AEE810` holds eight buffer pointers. Slots 1 to 7 are handed out by `0x0039BEC0`; slot 0 and slot 7 are
also written by the font-pack completion `0x0039C150`.

- Font pack: `0x0039C3F0` requests kind 7, id `0xD5` into `0x02AEE868` with completion `0x0039C150`. It returns at once
  while `0x02AEE868` is set (`0x0039C3FC`); otherwise it sizes the file with `0x0032E400`, allocates that many bytes with
  `0x003EFCD0` (arena 3, `0x0039C43B`), files the read with `0x0032E620` (`0x0039C45D`) and then stores the buffer at
  `0x02AEE868` (`0x0039C467`).
- That completion fills an empty slot 0 with the pack's directory entry 0, and an empty slot 7 with entry 6 when
  entry 6 is not `0xFFFFFFFF` and the language test `0x00254A10` is false. It then calls `0x0039BF50` and sets the
  ready flag `0x02AEE890`, a dword (`0x0039C3C6`).
- With `0x02AEE868` null the completion returns and stores nothing (`0x0039C163`-`0x0039C16D`). Entries 1 to 5
  go to `0x02AEE850`, `0x02AEE870`, `0x02AEE878`, `0x02AEE880` and `0x02AEE888`, each only while that pointer is 0
  (`0x0039C1B5`-`0x0039C26B`). `0x02AEE800` takes slot 0 plus `0x40` while it is 0, and `0x02AEE808` slot 7
  plus `0x40` while it is 0 and slot 7 is set (`0x0039C295`-`0x0039C2CB`).

  With entry 1 it also stores the entry's address + `0x10` in `0x02AEE858` and
  `that address + its word +0x0C` in `0x02AEE860`, and calls the empty stub `0x0016D6A0`
  (`0x0039C1C5`-`0x0039C1F3`). While slot 7 is set, `0x02AEE880` is then overwritten with entry 7
  (`0x0039C244`-`0x0039C254`). After `0x0039BF50` come `0x0017FBC0(1)` and, when the language test is false,
  `0x0017FB90(3, 7)` (`0x0039C272`-`0x0039C290`).
- `0x0029CAC0(buffer)` (from `0x00330060`) keeps a six-entry `{pointer, count}` table at `0x0209C320`: a buffer
  already there has its count raised and is not registered again (`0x0029CAD0`, `0x0029CB03`); a new one takes the
  first empty entry with count 1 and goes to `0x0039BEC0` as a tail jump (`0x0029CAF4`-`0x0029CAFE`); with six in use
  nothing happens (`0x0029CAF3`). The entry is filled before the gate, so a buffer `0x0039BEC0` refuses still holds it.
- The match compares the empty entries too, so a null buffer raises the count of the first empty one. `0x0029CB10`
  lowers the count of the buffer's entry (`0x0029CB36`) and, at 0, unregisters the buffer with `0x0039BB60`
  (`0x0029CB3C`) and empties the entry (`0x0029CB41`); a buffer not in the table changes nothing (`0x0029CB30`).
- `0x0037F1F0`, on a request record whose type byte is 4, registers the buffer and calls `0x0017FBC0(5)`; `0x0037F860`
  unregisters it with `0x0017FA70(5)`.
- `0x003BC4E0`, the map-data widget, registers the TIM2 inside the guide file it holds at `+0xF8` (at that
  file's u16 `+0x0A`, `0xFFFF` for no picture, `0x003BD8F0`), with `0x0017FBC0(4)`; it, `0x003BBFB0` and `0x003BC970`
  unregister it with `0x0017FA70(4)`.
- `0x00575710`, the handbook page, registers the TIM2 at the bundle's i32 `+0x0C` (unless -1) when its slot
  byte `+0xC8` is 1 (`0x0057572E`-`0x00575738`), with `0x0017FBC0(6)` when its kind byte `+0xD2` is 4;
  `0x00575640` unregisters it.
  - For kind 5 it hands the sheet to the font manager as `handbook_monster<NNN>.txt`, `NNN` being the word
    `+0xCC`: `0x0017FA90(NNN + 1, 1, name, 7)`, `0x0017FB70(NNN + 1)`, `0x0017F790(NNN, sheet)` and `0x0017FBE0()`
    (`0x00575782`-`0x005757D9`).
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
returns null for an empty slot (`0x0039BA49`), else the first picture's block (picture `+0x30`). With mode 0 it
returns null when that block's flags have a bit of `0x18000` set (`0x0039BA63`). A non-zero mode calls `0x00254A10`
(`0x0039BA80`): while it is false the first picture's block is returned whatever its flags (`0x0039BA87`).

With a non-zero mode and `0x00254A10` true it walks the file's `+0x06` pictures by `totalSize` and returns the first
block, of a picture whose `headerSize` is above `0x30`, whose flags have `0x8000` and not `0x10000`
(`0x0039BA95`-`0x0039BAA9`), or null (`0x0039BAB7`).

### Script glyph sheets (EBP section 6)

A script container (`.ebp`) can carry a glyph sheet in directory slot 6
([script container](../EBP-Script-Files/ebp-script-container.md)). When the container arrives,
`0x003304A0` passes that section, with the manager slot in the low four bits, to `0x00330060` (`0x00330565`), which:

1. stores it at `0x022C6CF0[g]` and in the area record (`0x0026C860`, `0x02098EC0 + g × 0x288`);
2. clears pending bit `0x40` of `0x022C6E48[g]`;
3. hands it to the text layer (`0x0017F790` → `0x001B47A0`, which gives it to the first waiting font entry whose
   id matches the packed value; when no entry matches it attaches nothing, and its failure message goes to the
   no-op `0x0016D6A0`, so nothing is logged);
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

The test follows each picture (`0x0039C08A`-`0x0039C09A`) and the counter is never reset, so once it is over the
limit each later slot still lays out its first picture and then stops.

`0x0039BDA0`, called from the screen bodies (`0x00252840`, `0x002528A0`, `0x00252990`, `0x00252A20`, `0x00252A70`),
returns at once while `0x02AEE890` is clear (`0x0039BDB7`). Otherwise it sends the font pack's 32 x 16 picture to
block `0x32FC` as a 32-bit image (PSM 0) one 64-pixel unit wide at `x = 0`, `y = 0`, with the width and height
from that picture's header (`0x0039BDBD`-`0x0039BE07`).

It then sends every picture of every slot, with a block or without one, to block `0x2A00`, 640 pixels wide,
4-bit (PSM `0x14`), at `x = 0` and `y` = the same running row, `width` x `height` from the picture header
(`0x0039BE40`-`0x0039BE72`). The row grows by every picture's height (`0x0039BE7D`) with no limit, so a slot whose
layout stopped before its last picture is still sent whole, and every later picture then goes below the row its
`bandBase` and `bandRow` name.

`0x003EFDF0(block, pixels, buffer width, PSM, x, y, width, height)` builds each transfer in the current packet
buffer (`0x02EBEFC0` + `0x18` x `[0x02EBEFF0]`): GS registers `0x50` to `0x53` under an A+D tag (`0x003A2090`), the
pixels from `picture + headerSize` through `0x003A21A0` as `0x003A1F20(width, height, PSM) / 4` quadwords, rounded
down, plus one (`0x003EFE22`-`0x003EFE4F`, `0x003EFF85`), then `0x3F` under a second tag. It ends by flipping the packet
buffers with `0x003A1DB0` (`0x003F001A`).

The font pack's picture is kept apart by `0x0039C150`: `0x02AEE858` points at its picture header, `0x10` bytes past the
TIM2 file at `0x02AEE850` (`0x0039C1D0`), and `0x02AEE860` at its pixels, the header plus its `u16 +0x0C` header size
(`0x0039C1DF`). `0x0039BDA0` reads both for the 32 x 16 transfer (`0x0039BDBD`, `0x0039BDC8`), and so does `0x0039BD50`
(`0x0039BD5D`, `0x0039BD77`).

## Modding notes

- Keep a replacement `.tm2` a single 16-byte-aligned picture at `+0x10`: the binder reads no picture count
  and no format byte, and only the first picture.
- The PSM in TEX0 (`+0x28` of the file, mask `0x3F00000`) must be `0x13` (8-bit) or `0x14` (4-bit); any other
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Input: `0x0022A4B0` calls `0x00291C80`; `0x0032E620` is called by `0x00291C80`; those functions are documented on
  [startup constants](../Engine-Core/startup-constants.md).
- Script VM: `0x0032E400` is called by `0x0050DF70`; `0x0032E620` is called by `0x0050DFE0`; those functions are documented on
  [file requests and the read queue](file-requests-and-the-read-queue.md).
- World area: `0x0032E400` is called by `0x00268750`, `0x003319D0`, `0x00378030`, `0x00379A10`, `0x003EA820`; `0x0032E620` is called
  by `0x00268750`, `0x00378030`, `0x003EA820`; `0x0036A190` is called by `0x00268750`, `0x00377DC0`, `0x00378030`, `0x00378BC0`.
- World area: those functions are documented on [ps2data bin families](ps2data-bin-families.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [resource arena and relocation](resource-arena-and-relocation.md),
  [standard file formats](standard-file-formats.md).
- World area: and on [item and ability ids](../Engine-Core/item-and-ability-ids.md),
  [async load manager](async-load-manager.md), [graphics settings](../Engine-Core/graphics-settings.md).
