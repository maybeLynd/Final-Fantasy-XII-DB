---
title: "Map menu files: the sloc picture files and the amap, cmap, gmap, lmap and wmap tables behind the location map and the World Map"
kind: "format"
category: "Game files and data tables"
addresses: "0x02B457E0, 0x003BC450, 0x003BC2D0, 0x00253780, 0x020927D0, 0x003C1F00, 0x003C26C0, 0x003BF520, 0x003BF5E0, 0x003BE2D0, 0x003BECA0, 0x003DFBB0, 0x003DFB50, 0x003C0340, 0x003BF430, 0x003BFF20, 0x003C1070, 0x003C0380, 0x003BE680, 0x003C2320, 0x003BCDE0, 0x003BDFF0, 0x003C17E0, 0x003C1680, 0x003C1DF0, 0x003BD950, 0x003BD890, 0x003BD8F0, 0x003BD040, 0x003BD480, 0x003C08B0, 0x003BCCA0, 0x003BFE10, 0x003C0250, 0x003C1D70, 0x00254380, 0x002543A0, 0x002543D0, 0x002543F0, 0x003BEC50, 0x003C4AE0, 0x003BF920, 0x003C0450, 0x003C12B0"
---

## What the player sees

- The location map (Display Map) and the map overlay show the current sub-location as a set of drawn zone
  pictures, with markers for the exits to other places, lines joining the zones and icons, each zone drawn
  through the record of which parts of it the party has explored.
- Exit markers show their destination's name, or "???" while locked.
- A line of guide text tells the player where the story leads next.
- The World Map shows the regions and areas of Ivalice, the routes between areas, an area picture, and,
  when the map is opened to choose a destination, the Strahl's landing points.

[Map screens](../Menus-And-HUD/map-screens.md) covers the screens themselves; this page covers the files they read.

## Where it comes from

All six kinds are resource kind 7 files under `ps2data/image/ff12/myoshiok/<folder>/worldmap/`:

| File | Magic | Kind 7 id | Requested by |
|---|---|---|---|
| `menumap_world.bin` | `wmap` | `0xA2` | `0x003BC2D0` (`0x003BC305`), when the creator asks for the World Map data |
| `menumap_location.bin` | `lmap` | `0xA3` | `0x003BC2D0` (`0x003BC333`), when the creator asks for the location data |
| `menumap_common.bin` | `cmap` | `0xA4` | `0x003BC2D0` (`0x003BC35D`), always |
| `menumap_area.bin` | `amap` | `0xA5` | `0x00253780` (`0x00253917`) |
| `menumap_guide00.bin` to `04` | `gmap` | `0x496` + n | `0x003C1DF0` (`0x003C1EB1`) |
| `menumap_sub00.bin` to `47` | `sloc` | `0x142` + n | `0x003C1F00` (`0x003C1FF6`) |

The sloc number n is the sub-location index, the position of the sub-location in `menumap_common.bin`'s
directory; the shipped `menumap_world.h` names the 48 indices (`rbn01_s01` = 0 … `sav01_s02` = 47).

Each language's kind 7 path array, installed by `0x002DF9A0`, names its own folder: `us`, `fr`, `de`, `it`,
`es`, `kr`, `ch` and `cn`; language 6's array names a `uk` folder that the archive does not contain, and
the remaining languages use `in`. The same arrays name `menumap_guide05.bin` to `15.bin` and
`menumap_sub48.bin` to `73.bin`, which do not ship.

A kind 7 site, formula or table gives the id of 477 of the 507 shipped `.bin` files with the shipped data. The guide schedule in `menumap_common.bin` has file byte 0 in
all 77 entries, so `0x003C1DF0` asks only for `menumap_guide00.bin` and gives no id of the 26 copies of `menumap_guide01.bin`
to `04`; no path array names the four `_e3` files. [`myoshiok-file-meanings.tsv`](myoshiok-file-meanings.tsv)
gives every file's kind 7 id, request site, screen and use, each `menumap_subNN.bin` as the zone pictures of
sub-location NN.

## Layouts

### Sub-location slots

Each of the two slots at `+0x120` of the map-data widget is `0xA8` bytes.

`MapSlot` (`0xA8` bytes, offsets from the start of the [mapdata+0x120]+i*0xA8):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | file | the menumap_sub file of the slot, requested through `0x00249180` by `0x003C1F00` (`0x003C200D`-`0x003C2012`); `0x003C22B0` frees it with `0x003697F0` and clears it (`0x003C230B`, `0x003C2310`), and the release `0x003C2210` does the same for both slots (`0x003C227C`, `0x003C2281`) |
| `+0x08` | `void*` | keys | the file's key array, the table at the file's word `+0x0A` plus that table's word `+0x02`, set when the file has arrived (`0x003C2727`-`0x003C273F`); each picture's name is formatted from a key's field id word and variant byte (`0x003C27F4`-`0x003C2808`); `0x003C0CF0` reports the slot ready once it is set (`0x003C0D23`) |
| `+0x10` | `u8` | subLocation | the sub-location n the slot holds, stored by `0x003C1F00` (`0x003C1FF2`); `0x003C0CF0`, `0x003C21C0` and the sloc readers `0x003BE2D0`, `0x003BECA0`, `0x003BF520` and `0x003BF5E0` find a slot by it (`0x003C0D08`, `0x003C21D9`, `0x003BE30E`, `0x003BECDE`, `0x003BF558`, `0x003BF620`); `0x003C26C0` reads it when registering (`0x003C26EC`) |
| `+0x11` | `u8[1]` | gap11 | read and written by no function; nothing fixes its width |
| `+0x12` | `u8` | palette | byte `+0x10` of the request descriptor `0x003C1F00` is given, copied when the slot is requested (`0x003C2015`-`0x003C201A`); 2 from all three callers (`0x002B7D00`, `0x002BB108`, `0x003CB5DF`); passed with each picture to its registration (`0x003C2815`) as the flags of `0x0024A480`, whose low four bits `0x0024A4E0` keeps in the atlas flags; the widget uses the .cl2 at its `+0x118` whenever that is set (`0x003C2794`) |
| `+0x13` | `u8` | pictureCount | the number of pictures, the first byte of the key table (`0x003C2730`-`0x003C2733`); `0x003C22B0` and `0x003C2210` release that many handles and set it to 0 |
| `+0x14` | `u8[4]` | gap14 | read and written by no function; nothing fixes its width |
| `+0x18` | `void*[18]` | pictures | the registered pictures loca_&lt;fieldId&gt;_&lt;variant&gt;, one handle per key whose offset is not -1 (`0x0024A480` in `0x003C26C0`); released with `0x0024A680` and cleared by `0x003C22B0` and `0x003C2210` (`0x003C2249`-`0x003C2268`); the registering loop stores a handle only where the qword is still 0 (`0x003C2780`-`0x003C2784`) and runs over the key count `+0x13`, offset -1 keys included, with no test against 18 (`0x003C283A`): from the first slot the 19th key lands on the second slot's `+0x00` file pointer, written only while that slot holds no file; from the second slot it lands on the widget's `+0x270` areaBits, and later keys past the widget's `0x278` bytes |

### The map-data widget's fields

The map-data widget is the `0x278`-byte widget kept at `0x02B457E0` with procedure `0x003BC4E0` (The map-data widget
below).

`MapDataWidget` (`0x278` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x003BC4E0` |
| `+0x0C0` | `void*` | owner | the widget told when loads finish: the creation record's first qword (`0x003BC91E`-`0x003BC921`), replaced by `0x003BC9F0`'s second argument when a quest's map data is asked for (`0x003BCA16`); `0x003BC3E0` sends it `0x100` when the tables have loaded, `0x101` when the quest data has, `0x102` when the map data request ends (`0x003BC702`-`0x003BC71E`, `0x003BC86E`-`0x003BC88C`, `0x003BC7FE`-`0x003BC813`) |
| `+0x0C8` | `u8` | stage | 0 while the tables load, 1 once they have (`0x003BC709`), 2 while the widget is being released by `0x003BBFB0` (`0x003BBFDA`); the loaded message is handled by it (`0x003BC593`-`0x003BC6CD`); `0x003BC9F0` and `0x003BCAF0` act only at 1 (`0x003BCA0D`, `0x003BCB21`); 0 with `+0xC9` on creation (`0x003BC8F8`) |
| `+0x0C9` | `u8` | routeType | the route type `0x003BCAF0` last marked (`0x003BCB32`); `0x003BD040` compares it with `0x0F` (`0x003BD0FF`) |
| `+0x0CA` | `u8` | screenMode | the map screen's mode, stored by the screens that read the maps: `0x003BD1B0`, `0x003BE3A0`, `0x003BED70`, `0x003BF7C0`, `0x003BFFF0`, `0x003C00C0`, `0x003C0180`, `0x003C0450` and `0x003C0890` (`0x003BD1EE`, `0x003BE424`, `0x003BEDBC`, `0x003BF7F9`, `0x003C0014`, `0x003C00E4`, `0x003C01A7`, `0x003C0483`, `0x003C0897`); `0x003BCBA0` and `0x003BCDE0` test it for 6 (`0x003BCC64`, `0x003BCEC0`), `0x003BF7C0` for 0 (`0x003BF828`) and `0x003C08B0` uses it as its test (`0x003C0955`); 0 on creation (`0x003BC8FF`) |
| `+0x0CB` | `u8` | questSteps | the number of steps of the selected quest, `0x00473B70`(0) when the quest data has loaded (`0x003BC836`-`0x003BC83B`); the step readers `0x003BD1B0`, `0x003BD9F0`, `0x003BDB30`, `0x003BDCD0`, `0x003BF9A0` and `0x003C0A00` loop to it (`0x003BD312`, `0x003BDA5D`, `0x003BDBC9`, `0x003BDD58`, `0x003BFA2B`, `0x003C0A5B`) |
| `+0x0CC` | `u16` | quest | the quest `0x003BC9F0` is asked to show (`0x003BCA1D`); `0x003BC260` tests it with `0x0046B240`, `0x00315DC0` and `0x00380170` and hands it to `0x0046B180` (`0x003BC269`-`0x003BC2A6`); `0x003BCAB0` and `0x003C0A00` look it up (`0x003BCAB9`, `0x003C0AAA`-`0x003C0ADD`) |
| `+0x0CE` | `u16` | questEntry | `0x0037EDB0`'s answer for `+0xCC` (`0x003BCA77`-`0x003BCA8E`, `0x003BCAB9`-`0x003BCAD8`), handed to `0x0037FD50` with the widget |
| `+0x0D0` | `u32` | flags | 0 on creation (`0x003BC8F2`). Bits `0x1` and `0x2`: text groups 6 (menu_mapname) and `0x17` (menu01) of the battle text tables (`0x02EC3D80`) were missing (`0x002F8040`) and are loaded by the widget through its request set (`0x002491B0`, `0x003BC37A`-`0x003BC3B3`), released on destroy through `0x002F83E0` (`0x003BC522`-`0x003BC543`). Bit `0x4`: a guide file is held at `+0xF8` (`0x003C1EDC`). Bits `0x8`, `0x10`, `0x20`: menumap_world, menumap_location and menumap_common are held (`0x003BC6D9`-`0x003BC6FB`), cleared as each is freed (`0x003BC009`-`0x003BC06F`, `0x003BC5D2`-`0x003BC610`). Bit `0x40`: the guide picture `+0x108` is registered (`0x003BC76A`-`0x003BC76D`); `0x003BD860` and `0x003BD890` test it (`0x003BD86F`, `0x003BD89C`). Bit `0x80`: the quest's map data is loading (`0x003BC7E4`), cleared when it ends (`0x003BC5A9`); the release waits for it (`0x003BC0FF`). Bit `0x100`: the quest data has loaded (`0x003BC82A`); `0x003BC160` tests it (`0x003BC19D`). Bits `0x200` and `0x400`: `0x0037F130` and `0x0037F140` answers (`0x003BC841`-`0x003BC878`); bit `0x400` picks the labels in mode 6 (`0x003BD42A`, `0x003BDC43`, `0x003BE5E1`). Bit `0x800`: show every point whatever its gate: set and cleared by the location pages `0x003BE3A0` and `0x003BED70` (`0x003BE48A`, `0x003BE430`, `0x003BF023`, `0x003BEDC6`), tested by `0x003BCBA0`, `0x003BDFF0`, `0x003BED70`, `0x003C12B0` and `0x003C1A20` (`0x003BCC58`, `0x003BE061`, `0x003BEE44`, `0x003C13F6`, `0x003C1B27`). Bit `0x1000`: set by `0x003BE3A0` on its first pass (`0x003BE41A`), which sets bit `0x2000` for location `0x0D` or `0x2F` and bit `0x4000` for `0x2F` (`0x003BE3F1`-`0x003BE414`) |
| `+0x0D4` | `u8[4]` | gap0D4 | read and written by no function; nothing fixes its width |
| `+0x0D8` | `void*` | worldTable | menumap_world.bin, kind-7 resource `0xA2`, requested by `0x003BC2D0` when the world argument is set (`0x003BC2F8`-`0x003BC31B`); freed by `0x003BBFB0` and the loaded message (`0x003BC004`-`0x003BC010`, `0x003BC5CD`-`0x003BC5D9`); `0x003BCAF0` walks its routes (`0x003BCAFE`) |
| `+0x0E0` | `void*` | locationTable | menumap_location.bin, kind-7 resource `0xA3`, requested when the location argument is set (`0x003BC326`-`0x003BC349`); freed as `+0xD8` (`0x003BC037`-`0x003BC04A`, `0x003BC5EC`-`0x003BC5F8`) |
| `+0x0E8` | `void*` | commonTable | menumap_common.bin, kind-7 resource `0xA4`, always requested (`0x003BC350`-`0x003BC373`); `0x003C1DF0` picks the guide entry from it (`0x003C1E15`-`0x003C1E48`); freed as `+0xD8` (`0x003BC06A`-`0x003BC07D`, `0x003BC60B`-`0x003BC617`) |
| `+0x0F0` | `void*` | guideEntry | the guide entry `0x003BD950` returns for the common table (`0x003C1E15`-`0x003C1E59`); its byte +4 picks the guide file (`0x003C1E9D`-`0x003C1EB1`) and its word +6 the line whose text `0x003BD8F0` returns (`0x003BC78E`-`0x003BC7A3`, `0x003BC7A7`); `0x003BD890` reads it (`0x003BD8B1`) |
| `+0x0F8` | `void*` | guideFile | menumap_guide&lt;n&gt;.bin, kind-7 resource `0x496` + the entry's byte +4, requested by `0x003C1DF0` (`0x003C1EA7`-`0x003C1ECC`); freed with the guide picture by `0x003BBFB0`, `0x003BC970` and the loaded message (`0x003BC0C1`-`0x003BC0DB`, `0x003BC652`-`0x003BC665`) |
| `+0x100` | `void*` | guideText | the text `0x003BD8F0` returns for the guide entry's line when the guide file has loaded (`0x003BC7A7`-`0x003BC7B3`); 0 on creation (`0x003BC8E4`) |
| `+0x108` | `void*` | guidePicture | the guide picture: the guide file's tim2Off picture, which `0x003BD8F0` stores through its third argument `+0x108` (`0x003BC795`-`0x003BC7A7`), set up with `0x0039BEC0` and `0x0017FBC0`(4) (`0x003BC795`-`0x003BC7CD`); `0x003BD860` returns it; released with `0x0039BB60` and `0x0017FA70`(4) and cleared (`0x003BC0A9`-`0x003BC0BA`, `0x003BC637`-`0x003BC64B`, `0x003BC9A9`) |
| `+0x110` | `void*` | clutTable | the third table of clutpack_ys.bin, `0x0035D520`'s answer, set by `0x003C2100` while it is 0 (`0x003C212C`-`0x003C213B`); pictures without a .cl2 use it (`0x003C27A0`); `0x003C20D0` and the destroy clear it (`0x003C20E7`, `0x003BC553`) |
| `+0x118` | `void*` | cl2Palette | the .cl2 palette, kind-7 resource `0xE1` + the cmap entry's palette byte (1 Loca_gil.cl2, 2 Loca_bhm.cl2), requested by `0x003C1F00`, replacing the one before (`0x003C2024`-`0x003C209D`); pictures with a palette use it (`0x003C2794`); freed on destroy (`0x003BC55A`-`0x003BC56B`) |
| `+0x120` | `u8[336]` | slots | the two MapSlot records (above), cleared on creation with `+0x270` (`0x003BC8C7`-`0x003BC914`) |
| `+0x270` | `u32[2]` | areaBits | one bit per area, 64 areas: `0x003BCAF0` clears it and sets the bits of both areas of every route of the given type (`0x003BCB1A`-`0x003BCB85`); `0x003BD480` and `0x003C08B0` read an area's bit (`0x003BD601`, `0x003C09A3`) |

### The map files

The shipped map files are laid out as follows.

All values are little-endian. The readers form a table address as a `u16` offset plus the low 32 bits of
the buffer address, so the readers assume a buffer below 4 GiB.

### sloc: menumap_subNN.bin

Header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "sloc" |
| `+0x04` | `u32` | - | 100 |
| `+0x08` | `u16` | recordsOff | record directory, from the file start (`0x10` in every file) |
| `+0x0A` | `u16` | picturesOff | picture table, from the file start |
| `+0x0C` | `u32` | - | 0 |

Record directory (at recordsOff):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | one record per zone field |
| `+0x04` | `u16[count]` | offset | each record's offset from the directory start |

Record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | fieldId | the zone's field id |
| `+0x02` | `u16` | lcmOff | LCMPOS1 block, from the record start; `0xFFFF` = no block |
| `+0x04` | `u16` | naviOff | NAVIICN2 block, from the record start; `0xFFFF` = no block |

Picture table (at picturesOff):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | count | pictures; `0x003C26C0` reads only the low byte |
| `+0x02` | `u16` | keysOff | key array, from the table start |
| `+0x04` | `i32[2][count]` | pictures | two arrays of count entries: each entry's TIM2 picture, from the table start (-1 when the entry has no picture), then from `+0x04` + 4 × count each entry's NPS2 placement record, from the table start |

```
keysOff: {u16 fieldId, u8 variant, u8 0}[count]
```

NPS2 record (32 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "NPS2" |
| `+0x18` | `f32` | width | the picture's width on the page |
| `+0x1C` | `f32` | height | the picture's height on the page |

NAVIICN2 block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | magic | "NAVIICN2"; byte +7 must be above '1' |
| `+0x08` | `u16` | kinds | icon kinds present (10 in every block) |
| `+0x0E` | `u16[9][2]` | kindTable | per kind k, 1 to 9, the pair at `+0x0A` + 4k: the offset of the kind's entries from the block start, then their count |

Icon entry (16 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16[2]` | from | start of the pointer line |
| `+0x04` | `i16[2]` | at | icon position |
| `+0x08` | `i16` | icon | icon number |
| `+0x0A` | `i16` | gate | story gate (`0x0032A8A0`) |
| `+0x0C` | `u8[4]` | - |  |

The pictures are TIM2 images ([TIM2 images](tim2-images.md)); the files end with the NPS2 records.

### lmap: menumap_location.bin

Header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "lmap" |
| `+0x04` | `u32` | - | 202 |
| `+0x08` | `u8` | - | 0 |
| `+0x09` | `u8` | count | records (48); every accessor bounds the index by it |
| `+0x0A` | `u16[count]` | offset | each record's offset from the file start |

Record, one per sub-location:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | zones | A entries |
| `+0x01` | `u8` | markers | B entries |
| `+0x02` | `u8` | links | C entries |
| `+0x03` | `u8` | members | D entries |
| `+0x04` | `...` | entries | in order: A[zones] and B[markers], 24 bytes each; C[links], 20 bytes each; an 8-byte zoom record; D[members], 4 bytes each |

A zone and B marker (one point space: A first, then B):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16[2]` | x, y | position on the page |
| `+0x04` | `u8[4]` | next | four neighbouring points (`0x003BE810`); `0xFF` = no point |
| `+0x08` | `u16[2]` | - | copied to the draw row |
| `+0x0C` | `u16` | fieldId | A: the zone's field id s32      label       B: destination label text id; -1 = destination's name |
| `+0x0E` | `u16` | gate | A: `0xFFFF` = no gate; a key item when flags `+0x10` have a bit of `0xFC0` (`0x00309EC0`), otherwise a story flag (`0x0032A8A0`); decoded by `0x003C18A0` |
| `+0x10` | `u32` | flags | A: mask `0x3` picture variant, mask `0x3C` zone group |
| `+0x10` | `u8` | - | B: copied to the draw row |
| `+0x11` | `u8` | dest | B: destination sub-location |
| `+0x12` | `i16` | gate | B: unlock gate; -1 = always |
| `+0x14` | `u8` | - | B: second link point |
| `+0x15` | `u8` | destPoint | B: point in the destination |
| `+0x16` | `i16` | gate | B: second gate |

C link:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[2]` | fieldIds | the two zones it joins |
| `+0x04` | `i16[6]` | points | three x, y pairs |
| `+0x10` | `i16` | gate | map-jump flag gate; -1 = no gate |
| `+0x12` | `u16` | - | 0 |

Zoom:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[3]` | zoom | the record's zoom levels |
| `+0x06` | `u16` | - | 0 |

D member:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | node | an A field id |
| `+0x02` | `u16` | member | a further field shown as that zone |

### cmap: menumap_common.bin

Header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "cmap" |
| `+0x04` | `u32` | - | `0xCB` |
| `+0x08` | `u16` | dirOff | `0x0C` |
| `+0x0A` | `u16` | mapsOff | `0x190` |

Directory (at dirOff), one entry per sub-location:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | 48 |
| `+0x04` | `...` |  | entry[count], 8 bytes: |
| `+0x00` | `u8` | group | persistence group |
| `+0x01` | `u8` | palette | 0 = no palette, else kind 7 id `0xE1` + palette |
| `+0x02` | `i16` | gate | story gate; -1 = no gate (`0x003C12B0`) |
| `+0x04` | `i32` | name | sub-location name text id; -1 = no name |

Maps (at mapsOff):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | count | 369 |
| `+0x02` | `u16[count]` | value | low byte: explored cells a map needs |

Guide schedule (at mapsOff + 2 + 2*count, rounded up to 4):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | 77 |
| `+0x04` | `...` |  | entry[count], 8 bytes: |
| `+0x00` | `u16` | counter | story counter at which it applies |
| `+0x02` | `u16` | gate | story gate; `0xFFFF` = no gate |
| `+0x04` | `u8` | file | guide file number |
| `+0x05` | `u8` | - | 0 |
| `+0x06` | `u16` | line | line index in the guide file |

### gmap: menumap_guideNN.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "gmap" |
| `+0x04` | `u32` | - | `0x64` |
| `+0x08` | `u16` | textOff | string area, from the file start |
| `+0x0A` | `u16` | tim2Off | TIM2 picture, from the file start; `0xFFFF` = no picture |
| `+0x0C` | `u16` | - | 0 |
| `+0x0E` | `u16` | count | lines |
| `+0x10` | `...` |  | entry[count], 8 bytes: |
| `+0x00` | `u16` | counter | copy of the schedule entry's counter |
| `+0x02` | `u16` | gate | copy of the schedule entry's gate |
| `+0x04` | `u16` | text | string offset from textOff; `0xFFFF` = no string |
| `+0x06` | `u16` | - | 0 |

The strings are zero-terminated game text ([Text drawing](../Menus-And-HUD/text-drawing.md)).

### wmap: menumap_world.bin

Header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "wmap" |
| `+0x04` | `u32` | - | `0xCA` |
| `+0x08` | `u16` | regionsOff | `0x14` |
| `+0x0A` | `u16` | areasOff | `0x48` |
| `+0x0C` | `u16` | routesOff | `0x5C8` |
| `+0x0E` | `u16` | - | 0 |
| `+0x10` | `u16` | destsOff | `0x7AC` |
| `+0x12` | `u16` | - | 0 |

```
regions: u32 count, s32 name text id[count]; -1 = no name
areas:   u32 count, area[count] of 28 bytes, then extra[count] of 8 bytes
```

Area:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16[2]` | x, y | position on the World Map |
| `+0x04` | `u8[4]` | next | four neighbouring areas |
| `+0x08` | `u16` | until | story counter at which the area disappears; `0xFFFF` = never |
| `+0x0A` | `u8` | region | 0 = never shown |
| `+0x0B` | `u8` | picture | area picture number |
| `+0x0C` | `i16[2]` | - | copied beside the name |
| `+0x10` | `i32` | name | area name text id (repeated at `+0x18`) |
| `+0x14` | `i16` | gate | story gate; -1 = no gate |
| `+0x16` | `i16` | item | area map key item; -1 = no item |
| `+0x18` | `i32` | name2 |  |

Extra:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | gate | story gate; -1 = no gate |
| `+0x02` | `u8` | type | type byte used while the area is hidden |
| `+0x03` | `u8[5]` | - | 0 |

```
route: {u8 areaA, u8 areaB, u8 type, u8 0, s16 x, s16 y}
destination: {u16 value, u8 area, u8 0}
```

### amap: menumap_area.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "amap" |
| `+0x04` | `u32` | - | `0xC9` |
| `+0x08` | `u16` | typeOff | u8 count, u8 type[count], per area |
| `+0x0A` | `u16` | groupOff | u8 count, u8 area[count], per persistence group |
| `+0x0C` | `u16` | mapOff | u16 count, u16 item[count], per group; `0xFFFF` = no list |
| `+0x0E` | `u16` | nameOff | u32 count, s32 text[count], per area |

## Shipped data

| Fact | Value |
|---|---|
| folders | `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us` |
| `menumap_world.bin` | 9 copies, 2,040 bytes; 4 distinct contents (`us`, `ch`, `cn`, `de`, `kr` / `es` / `fr` / `in`, `it`) |
| wmap contents | 12 region slots, 39 areas (area 0 a placeholder with region 0 and no name), 60 routes (45 of type 0, types 1 to 15 once each), 18 destinations |
| wmap areas | `until` 10 and 1,450 on one area each, `0xFFFF` on the rest; 18 gates in `0x40xx`; 29 key items in `0x80xx`; 15 extra gates |
| `menumap_location.bin` | 9 copies, 23,852 bytes; 6 distinct contents; 48 records |
| lmap entries | 384 zones, 111 markers, 545 links, 97 members; every link joins two zones of its own record, every member's node is a zone of its record |
| lmap zoom | (240, 240, 320) in 46 records, (235, 235, 235) and (210, 210, 210) once each |
| `menumap_common.bin` | 9 identical copies, 1,760 bytes |
| cmap contents | 48 entries, 47 groups (group 14 twice: `sav01_s01` and `sav01_s02`); palette 1 on entry 40, 2 on entry 46; maps: 358 × `0xFFFE`, 10 × `0xFFFF`, 1 × 0 |
| guide schedule | 77 entries, counters 0 to 6,150 ascending, file byte 0 in all |
| `menumap_area.bin` | 9 identical copies, 396 bytes: 39 types (values 0 to 5), 59 groups, 59 map items (46 in `0x8000`-`0x802F`, 13 `0xFFFF`), 39 names (60100 to 60137 after an empty slot) |
| `menumap_guide00.bin` | 9 copies, 4,376 to 8,880 bytes, 77 lines each; a TIM2 picture in `ch`, `cn`, `in`, `kr`; in `de`, `es`, `fr`, `it`, `us` the picture offset points at or past the file end |
| `menumap_guide01.bin` to `04` | 8, 6, 6 and 6 copies; never requested |
| sloc files | 436: 48 per folder plus `menumap_sub01_e3`, `07_e3`, `25_e3` in `in` and `26_e3` in `us`, which no path array names |
| sloc sizes | 1,049,520 to 11,544,192 bytes, 2,405,224,352 in all; 24 of the 48 files are identical in every folder |
| sloc contents | 2 to 17 records and 2 to 18 pictures per file; every picture and NPS2 offset lands on its magic in all 436 |
| sloc `us` | 380 records (5 without LCMPOS1, 179 without NAVIICN2); 384 pictures, one for each lmap zone, keyed by its field id and variant |
| icons (`us`) | 609 entries: kind 3 88, kind 5 423, kind 8 13, kind 9 85 |
| area pictures | `worldmap/bin/areatim2/loca_00.tm2` to `loca_38.tm2` in `in` only, 1,049,728 bytes each, named by every language's array |

Every shipped map file and every record in it, decoded with the layouts above. The record tables list each distinct
content once, with the folders that hold it; the four `_e3` sloc files are included. Sub-location and area names are
the define names of the shipped `menumap_world.h`. Guide lines are decoded with the font of each folder's language,
and `{expansion glyph N}` marks glyph N of the guide file's own picture.

| table | rows | one row per |
|---|---:|---|
| [`menu-map-files-files-rows.tsv`](menu-map-files-files-rows.tsv) | 507 | shipped file: folder, size, SHA-256, the folders with the same bytes, magic and header fields |
| [`menu-map-files-sloc-rows.tsv`](menu-map-files-sloc-rows.tsv) | 644 | sloc zone record: field id, `LCMPOS1` and `NAVIICN2` offsets and the icon count of each kind |
| [`menu-map-files-sloc-pictures-rows.tsv`](menu-map-files-sloc-pictures-rows.tsv) | 654 | sloc picture: key field id and variant, picture and NPS2 offsets, the TIM2 header fields, the NPS2 width and height, and the NPS2 dwords `+0x04` to `+0x14` as stored |
| [`menu-map-files-sloc-icons-rows.tsv`](menu-map-files-sloc-icons-rows.tsv) | 1,053 | `NAVIICN2` icon entry: record, kind, `from`, `at`, icon number, gate and bytes `+0x0C` to `+0x0F` |
| [`menu-map-files-lmap-rows.tsv`](menu-map-files-lmap-rows.tsv) | 288 | lmap record: zone, marker, link and member counts and the zoom levels |
| [`menu-map-files-lmap-entries-rows.tsv`](menu-map-files-lmap-entries-rows.tsv) | 6,822 | lmap zone, marker, link and member, every field, with the gate kind of each zone |
| [`menu-map-files-cmap-rows.tsv`](menu-map-files-cmap-rows.tsv) | 494 | cmap directory entry, maps value and guide-schedule entry |
| [`menu-map-files-gmap-rows.tsv`](menu-map-files-gmap-rows.tsv) | 800 | guide line: counter, gate, text offset, text length and the line decoded |
| [`menu-map-files-wmap-rows.tsv`](menu-map-files-wmap-rows.tsv) | 516 | wmap region, area with its extra record, route and destination |
| [`menu-map-files-amap-rows.tsv`](menu-map-files-amap-rows.tsv) | 98 | amap area (type and name text) and persistence group (area and map item) |
| [`menu-map-files-world-areas.tsv`](menu-map-files-world-areas.tsv) | 39 | World Map area as the `us` file gives it: code, name, region, the story counter at which it disappears, its gate and extra gate as story counter bands, its map key item by name, its neighbours by code and its destination value |
| [`menu-map-files-names.tsv`](menu-map-files-names.tsv) | 138 | name text id of every wmap region and area, amap area and cmap sub-location, with the `us` string it resolves to |
| [`menu-map-files-gates.tsv`](menu-map-files-gates.tsv) | 742 | every gate word of the `us` files: the entry, the word, the reader that tests it with its instruction address, and what opens it as a story counter band, a story flag, a key item or a fixed answer |

Names and gates in those two tables are resolved as the engine resolves them:

- A name text id goes through `0x002F9920`: group `id / 10000` is 6, `menu_mapname`, and the string is the one at the
  position of the row whose id equals it. The `us` file numbers its 285 rows 60000 to 60010, 60100 to 60359 and
  60400 to 60413.
- Every area gate and extra gate is a story schedule id (bit `0x4000`), answered from `mapjumpgroupflagrom.bin` as
  `0x00377970` reads it ([Story flags](../Story-Events-And-Hunts/story-flags.md)).

What they show:

- Region slot 0 has no name. Slots 1 to 9 name Dalmasca to Jagd Naldoa, and slots 10 and 11, the regions of the
  Leviathan and the Bahamut, read `???`.
- The 18 areas with a gate are the 18 areas a destination names. 17 of the gates pass from story counter 5150 on, and
  the Bahamut's from 6100. Of the 15 extra gates, 13 pass over one story counter band and
  Rabanastre's and Mt Bur-Omisace's over three.
- 29 areas name a map key item.
- 45 of the 48 sub-location name ids resolve to an empty `us` string. `sav01_s01` reads `Giza Plains - The Dry`, and
  `slm01_s01` and `sav01_s02` read `Giza Plains - The Rains`.

[`menu-map-files-marker-labels.tsv`](menu-map-files-marker-labels.tsv) gives the text of the 42 label ids on the 666
marker rows of the lmap table, and [`menu-map-files-icon-numbers.tsv`](menu-map-files-icon-numbers.tsv) what the four
icon kinds and the 26 icon numbers of the NAVIICN2 table show, with the atlas cell each one draws; its `us` counts are
631 `us` rows, the 609 of the path-array files and the 22 of `menumap_sub26_e3.bin`. Both are resolved as the map
draws them:

- A marker whose label `+0x0C` is not -1 shows `0x002F9920(label)` (`0x003C25BD`, `0x003C2629`): group 6, `menu_mapname`.
  The 42 ids are 60201 to 60244 without 60224 and 60225, rows 112 to 155, `To Lowtown` to `To the Subterra` in `us`,
  with the same row ids in all nine languages.
- The map draws every icon from `loca_8_c.tm2`, the atlas at `+0x08` of the page's resource record: `0x00400420` takes
  cell 9 plus the low byte of the icon number from its `eXt` table (`0x0040047D`-`0x0040049C`). `0x004048E0` draws kinds 3
  to 8 and `0x00403BC0` kind 9, which pulses every icon and passes over icon 14.
- The legend pairs 14 icon numbers with the text ids `0x187F` to `0x188C` (`0x00916A10`, `0x002BA650`), rows 271 to 284
  of `menu_mapname`. Those rows are empty in `us` and `it`, `DUMMY` in `es`, and named in `de` and `fr`. The legend's
  icons, and the point list's icons below `0x13`, are cell 135 plus the icon number of `battle_4_c`: the same
  pictures at 32 by 32.
- Icon -1, on two kind 9 entries of `rbn01_s01`, selects cell 264, past the 56 cells of `loca_8_c`; the 8 bytes there
  read as a cell 0 by 0.

[`menu-map-files-gates.tsv`](menu-map-files-gates.tsv) gives what opens each of the 742 gate words of the `us` files:
lmap zones, markers and links, NAVIICN2 icons, the cmap directory and guide schedule, gmap lines, and the World Map's
area gates, extra gates and map key items. Each row names the reader that tests the word, with its instruction
address. The readers decode the words this way:

- A key item word passes when the item is owned (`0x00309EC0`): an lmap zone whose flags have a bit of
  `0xFC0` (`0x003C18F7`), and a World Map area's map key item (`0x003BD64C`, `0x003C0C31`). A zone whose key item is not
  owned still passes while its draw state has a bit of `0x401` (`0x003C190D`).
- Every other word goes to the story gate `0x0032A8A0` ([Story flags](../Story-Events-And-Hunts/story-flags.md)). With
  bit `0x4000` it reads a story schedule record, given as story counter bands. Index 0 opens, index 1 shuts, and any
  other index is a Primary flag, explained by its row in [Story flag ids](../Story-Events-And-Hunts/story-flag-ids.md).
- An icon's gate goes to `0x0032A8A0` with no `0xFFFF` test (`0x003DFB8D`), so 0 shows the icon and 1 hides it. The other
  readers let `0xFFFF` pass before the gate.
- A marker's unlock gate `+0x12` is passed over when the area map of its sub-location is owned (`0x003C1027`). Its
  second gate `+0x16` is tested first and refuses on a fail (`0x003C0F8E`).

The 742 words are 177 lmap words (26 key items, 121 flags, 30 schedule bands), 323 icon words (175 flags, 41
schedule bands and 107 of index 1), 3 cmap directory flags, 77 guide schedule bands, 100 gmap lines that carry a
copy of a schedule gate, and on the World Map 29 key items and 33 schedule bands.

Five icon flags, `0x5D`, `0x9B`, `0x9C`, `0xC4` and `0xC5`, are set by no `us` script, by no battle order record and by no entry of the new-game list
([Story flags](../Story-Events-And-Hunts/story-flags.md), Primary writers).
Battle orders write a story flag through `0x0032ABE0` (`0x00329EEC`-`0x00329EF7`) when `0x002FE660` runs a register order
whose word `+0x06` is kind 8. The 4,467 register orders of the 166 area files' order sets write kinds 10, 9 and 1, and
no weighted run of `battle_pack.bin` entry `+0x2C` holds a register order in any language.

## Loader behaviour

### The map-data widget

`0x003BC450(world, location, owner)` creates the widget `0x02B457E0` (0x278 bytes, procedure `0x003BC4E0`) when no such
widget exists and answers 1; when a widget already exists it creates no second one and answers 0 (`0x003BC463`,
`0x003BC4C5`). On creation `0x003BC4E0` clears the sub-location slots and calls `0x003BC2D0`, which requests
`menumap_world.bin` into `+0xD8` when `world` is set, `menumap_location.bin` into `+0xE0` when `location` is
set, and `menumap_common.bin` into `+0xE8` always, all through `0x00249210`.

`0x003BC2D0` files the three in heap 2 in one request set, opened with `0x00249580` and closed by a tail jump to
`0x00249410` (`0x003BC3D1`). In the same set it asks for text groups 6 and `0x17` when `0x002F8040` finds them
missing (`0x002491B0`), setting bits `0x1` and `0x2` of `+0xD0` (`0x003BC37A`-`0x003BC3B3`). It tests no return:
with all twelve sets in use `0x00249580` returns 0 and a request for a file with a size then adds to the
count at address `0x18` (`0x002492F8`); with all 48 request entries in use `0x00249210` stores through a null
entry (`0x0024928D`).

The widget frees the three tables and the guide file at `+0xF8` in its message `0x10` handler, and the
palette at `+0x118` and both slots when it is released (`0x003C2210`). `menumap_area.bin` is loaded separately
by `0x00253780`, the field HUD root, into `0x020927D0`: on its message 1 it frees the buffer held there
(`0x003697F0`, `0x00253901`-`0x00253906`) and requests kind 7 `0xA5` (`0x00249180`, `0x00253928`-`0x00253930`).

Small queries on the widget:

- `0x003BC2C0()` answers whether no map-data widget exists; the location map's procedure `0x002BA700` and the
  field-time container `0x003CB650` ask it.
- `0x003BD860()` returns the guide picture at `+0x108` once the widget's bit `0x40` is set and the guide file
  `+0xF8` is held, otherwise 0 (`0x002BA700`).
- `0x003C0CC0()` returns bit `0x40` of `+0xD0` while its bit `0x4` is set, and 1 when that bit is clear or
  no widget exists (`0x002B7590`, `0x002BA700`).
- `0x003C20D0()` clears the `clutpack_ys.bin` table pointer `+0x110` and returns 1, or 0 with no widget
  (`0x002BA700`, `0x003CB650`).
- `0x003BC3E0(owner, value)` sends `{0x10, value}` to an owner through its handler; `0x003BC4E0` and
  `0x003BC9F0` use it.

### Sub-location slots and pictures

The widget holds up to two sloc files, in two 0xA8-byte slots at `+0x120`: data pointer `+0`, key array
`+8`, sub-location index `+0x10`, picture count `+0x13` and 18 picture handles from `+0x18`.

1. `0x003C1F00(widget, owner, request, n)`, through `0x003C2190`, takes a free slot and requests
   `menumap_sub<n>` (`0x00249180`). It refuses when both slots are in use, or when one is in use and no other
   cmap entry shares entry n's group.
2. It counts the group among the first 50 entries only, an index at or past the count reading as group 0,
   and refuses when exactly one matches (`0x003C1F8A`-`0x003C1FD3`). Refusing returns 0 with no request
   (`0x003C1F52`); otherwise it returns 1 (`0x003C20A4`).
3. When cmap entry n's palette byte is non-zero it requests kind 7 `0xE1` + that byte into `+0x118`
   (`0x003C207A`): `Loca_gil.cl2` for 1, `Loca_bhm.cl2` for 2. Whatever the byte, it first frees the palette
   already at `+0x118` and clears the pointer (`0x003C2024`-`0x003C203C`).
4. The overlay page `0x002B7B80`, the location page `0x002BAF80` and the preload child `0x003CB4F0` call it; when it
   refuses they free the other slot (`0x003C21C0`) or both (`0x003C21B0`) and try again.
5. When the file has arrived, `0x003C2200` → `0x003C26C0` stores the key array and registers every picture whose
   offset is not -1 as the named image `loca_<fieldId>_<variant>` (`0x0024A480`), with the palette at `+0x118`
   when the entry names a `.cl2`, otherwise the third table of `clutpack_ys.bin` at `+0x110`
   ([Cl2 menu colour tables](cl2-menu-colour-tables.md)). `0x003C0CF0` reports 0 (absent), 1 (loading) or 2
   (ready).
6. `0x003C26C0` tests `+0x118` itself, so the palette is whichever the last request left (`0x003C2794`). It
   registers only into handles that are still 0, gives the slot's byte `+0x12` as the flags (`0x003C2815`),
   returns 0 when no slot holds sub-location n (`0x003C2704`) and 1 otherwise (`0x003C2864`).
7. `0x003C22B0(slot)`, run by `0x003C21C0`, empties a slot: it releases each registered picture
   (`0x0024A680`), sets the count `+0x13` to 0 and frees the file (`0x003697F0`).

### Readers of sloc

- `0x003BF520(field, variant)` returns the picture handle whose key matches, from the slot of the field's
  sub-location (`0x003C0380`), and 0 when no slot holds that sub-location or no key matches (`0x003BF5BE`);
  `0x003C1180` uses the picture's TIM2 size for explored-cell tests and `0x00402C30` binds it to the zone's draw
  element.
- `0x003BF5E0(widget, n, field, variant, out)` finds the same key in the slot of sub-location n and returns its
  picture handle; it stores the key's NPS2 record through `out`, which it sets to 0 first, so a missing key
  leaves 0 there (`0x003BF608`, `0x003BF69C`-`0x003BF6AD`). `0x003BEC50(field, variant)` returns that NPS2 record for
  a field, finding the field's sub-location with `0x003C0380` first.
- `0x003C2320` copies the NPS2 record's width and height into the zone's draw row (`+0x24`, `+0x26`), and
  `0x003BED70` uses them to size the page around the drawn zones.
- `0x00404730` draws a zone picture through the zone's explored-cell mask from `0x002551B0`, which `0x003C4AE0` asks for
  with `0x00264790()` when that is positive, and otherwise, or on a null result, takes the pointer kept at `0x02B45A50`
  (`0x003C4AED`, `0x003C4B05`); with no mask, or with bit `0x8000` of the element's flags, every cell is shown.
- `0x00404730` places the picture with `0x003C46B0(…, element, …)`: from the element record it sets up a matrix from
  `+0x20`, turns it by -π/2 (`0xBFC90FDB`, `0x003985B0`) and by the negated `+0x1C` (`0x00398C50`), sets it at half of
  `+0x04` and `+0x08`, and combines it (`0x003977B0`) with the record's `+0x14`/`+0x18` and with a second matrix moved
  by -`+0x0C` and -`+0x10`; `0x003C6420` then draws with the result.
- `0x003BE2D0(field)` returns the field's NAVIICN2 block, and 0 when no slot holds the field's sub-location
  (`0x003C0380`), no record has the field id, or the record's `naviOff` is `0xFFFF` (`0x003BE365`, `0x003BE38E`).
- `0x003DFBB0` gives a kind's count (kinds 1 to 9 below the block's `kinds`); `0x003DFB50(block, kind, i)` gives
  entry i and drops it when its gate fails. It also gives 0 for a null block, a byte `+7` below `'2'`, or an i
  at or past the kind's count (`0x003DFB5E`-`0x003DFB74`).
- `0x004048E0` draws icon kinds 3 to 8 (through `0x00403640`, called by `0x00403970`), and `0x00403BC0` kind 9. An
  icon whose `from` differs from `at` can get an 8-segment pointer line; with a mask, icons other than 14,
  20, 23 and 24 are shown only when the cell at `from` is explored (`0x00255150`).
- `0x00400190(page, record)` appends each drawn icon's record to the page's draw list: head `+0x00`, tail `+0x08`,
  count `+0x1412`; records link forward through `+0x28` and back through `+0x30`. `0x00403BC0` and `0x004048E0` call
  it for every icon they draw.
- `0x003BECA0(field)` returns the field's LCMPOS1 block, and 0 in the same three cases as `0x003BE2D0`, here for
  an `lcmOff` of `0xFFFF` (`0x003BED35`, `0x003BED5E`); the draw paths `0x002B8EE0` and `0x002BCB00` pass it to
  `0x00403640` and `0x00403BC0`, which leave it unused.

The minimap draws the zone pack's own picture and placement, not these ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

### Readers of lmap

- `0x003C0340(n)` returns `zones + markers` of record n, and 0 with no lmap held or n past the count
  (`0x003C0370`); `0x003BF430(n, i)` returns point i (zone for `i < zones`, else marker) and its kind (0 zone,
  1 marker, 3 no point). `0x003BF920(n, i)` returns point i's field id when it is a zone that passes
  `0x003C18A0`, and `FFFF` otherwise (callers `0x003BDB30`, `0x003BDCD0`).
- `0x003C0380(field)` finds the field's sub-location: for each cmap entry whose group is the field's
  persistence group (`0x00264F90`), it maps the field through the record's members (`0x003BFF20`) and looks for a
  zone with that field id. `0x003BFF20(n, field)` gives the node of the member that names the field, or -1, and
  then the field stands for itself (`0x003C03F0`). It returns the first matching entry of the first 50, or -1
  (`0x003C042B`).
- `0x003C1070(n, field)` tells whether the player stands in a zone or one of its members. It answers 1 when
  `field` is the current field (`0x00264790()` when that is positive, otherwise `0x003148F0()`), or when a member
  of record n has `field` as its node and `0x003148F0()` as its member (`0x003C1118`-`0x003C1152`); otherwise 0.
- `0x003C2320` builds a point's draw row. For a zone: position, neighbours, field id, picture variant, the
  zone name (`0x00377B60`) and the picture size. For a marker: the destination, resolved by `0x003BDDE0`; the
  label text, or "???" (`0x3EC`) while locked; destination 13 (`sav01_s01`) becomes 47 (`sav01_s02`) when
  the story gate `0x107` passes (`0x0032A8A0`).
- `0x003BCDE0(n, i, link, out)` keeps a link when its gate passes and, outside screen mode 6, when `0x003C1180`
  accepts its point at `+4` or `+0xC`: the zone's area map is owned (`0x002543F0`), `0x00377A40` accepts the
  field, or the point's cell is explored.
- Point i must also pass its gate (`0x003C18A0` for a zone, `0x003C0F70` for a marker), be a zone, lack draw bit
  `0x800` (`0x003BCBA0`) and have its field id at one end of the link (`0x003BCE1D`-`0x003BCEA7`). The record's
  zone with the field id at the other end is the far zone (`0x003BCF20`-`0x003BCF4A`).
- A far zone in a zone group gives way to the zone `0x003BDFF0` picks for the group, and stays when it picks
  no zone; a far zone in no group must pass its gate (`0x003C1980`, `0x003BCFBE`). A kept link answers 1 and,
  with `out` set, fills a 16-byte row: i, the far point's index, then the link's three `x`, `y` pairs
  (`0x003BCFCC`-`0x003BD018`). Any failed test answers 0.
- `0x003BDFF0(n, group)` picks the one zone of a zone group that stands for the group; `0x003BED70` and
  `0x003BCDE0` use it. It returns the index of the first zone of record n whose group bits (flags mask `0x3C`)
  equal `group` and whose gate passes (`0x003C0D30`), or, while the widget's `+0xD0` has bit `0x800`, whose
  `0x003C06E0` answer has bit `0x1` (`0x003BE061`-`0x003BE107`); -1 when no zone does.
- `0x003BE680(n, second, third)` returns the three zoom levels: the first as its answer and the second and
  third through its pointer arguments when they are set (`0x003BE6D9`-`0x003BE6F3`), and 0 with no lmap held or
  n past the count (`0x003BE6F7`). The pages keep the remembered level (`0x0209E5B8`) when it is one of them,
  otherwise the first, and scale by 3200 / level (`0x002B7FFA`-`0x002B8067`).
- `0x003BE1E0(n, group, out)` returns the point that stands for zone group `group` of record n (`0x003BDFF0`),
  with its index in `out`, -1 when no point stands for it; `0x003BDDE0`, `0x003BED70`, `0x003C12B0` and `0x003C1A20` use it.
- `0x003BE700(n, dest)` returns the first marker of record n whose destination byte `+0x11` is `dest`, or -1
  (`0x003C2320`).
- `0x003C0D30(n, i)` runs point i's gate test, `0x003C18A0` for a zone and `0x003C0F70` for a marker
  (`0x003BDDE0`, `0x003BDFF0`).
- `0x003C0740(out, n, i)` lists, as 16-byte rows, the links of record n that `0x003BCDE0` keeps for zone point
  i, when the point passes its gate and its draw state (`0x003BCBA0`) lacks bit `0x800`; it returns the count.
  `0x003C0890`, called by `0x00402A40`, first stores its fourth argument at the widget's `+0xCA`.
- `0x003C1A20(out, n, kind, x, y)` lists record n's points for the location page `0x003BE3A0`: zones for kind
  0 (at most 20), markers for 1 (at most 16), both for 2 (at most 24). A zone group appears once, through
  `0x003BE1E0`; other points only when their gate passes or the widget's `+0xD0` has bit `0x800`.
- Each of its `0x18`-byte rows holds the point index, the point and its kind, and `x`, `y` receive the
  smallest zone position.
- `0x003BE950(row, dir, rows, n)` picks the next cursor point in direction dir (0 up, 1 down, 2 left, 3
  right) for `0x003C2320`. It measures from the centres of the points, a zone's from its picture size
  (`0x003BF5E0`), a marker's from its label size (`0x0029CD00`), and takes the point on that side that
  `0x003BD6F0` scores lowest with the direction vector `0x01EFE330`, skipping zones with draw bit `0x800`; 0xFF
  when no point lies on that side.

### Readers of cmap

- `0x003C0450(out, group, check)` lists the sub-locations that share a persistence group for the World
  Map (`0x00551800`, `0x00551930`, `0x00551B30`). It first stores `check` at the widget's `+0xCA` (`0x003C0483`).
- It returns 0 for a group of `0x3B` or more and for a group with fewer than two of the first 50 directory
  entries, where an index at or past the directory's count reads as group 0 (`0x003C0532`); with `check` set
  and a group other than the current field's (`0x003148F0`, `0x00264F90`), also when no entry of the group is
  accepted.
- Otherwise it writes a `0x18`-byte row per entry of the group that `0x003C12B0` accepts (index, group,
  the name text through `0x002F9920` or null for -1, and `0x003C05F0(index)`) and returns the count; with `out`
  null it counts the rows without writing them (`0x003C057A`).
  `0x003C12B0(n)` refuses an entry whose gate is set and does not pass (`0x0032A8A0`) and accepts it at
  once when the area map is owned (`0x002543F0`).
- `0x003BF8E0(n)` returns directory entry n's group byte, 0 past the count (`0x002BA700`, `0x002BAF80`), and
  `0x003C0F00(group)` answers 1 when every entry of the group is explored (`0x003C1680`), for `0x003BF6C0`.
- `0x003BF7C0(out, area, mode)` lists persistence groups for the World Map (`0x00551800`, `0x00551930`,
  `0x00551B30`, `0x005528C0`): a `0x18`-byte row (`0x003BF6C0`) for each group 0 to 58 whose area (`0x00254380`) is
  `area`. It stores `mode` at the widget's `+0xCA`.
- With a non-zero mode a group other than the current field's (`0x003148F0`, `0x00264F90`) needs an entry that
  `0x003C12B0` accepts. In mode 6 a row gets bit `0x20` when the selected quest marks the group
  (`0x003C0E30`). It returns the count.

- The directory's group byte joins a sub-location to its persistence group (`0x003C0380`, `0x003BD480`), and its
  name id gives the marker label fallback (`0x003C2320`) and the location entry (`0x003C02B0`).
- `0x003C17E0(field)` reads the maps array at the field's map index (`0x003779F0`); a zone counts as explored
  when its explored-cell count (`0x00255060` on the current zone's mask, `0x002550E0` on the saved 32 bytes at
  `[0x020927C0] + 0x224 + 32 × index`) reaches the low byte.
- It takes the current zone's mask (`0x003C4AD0`) when `0x003C1070` finds the player in the field's zone or one
  of its members (`0x003C182F`-`0x003C1850`). A map index of 0 or less counts as explored, and an index at or
  past the maps count as not explored (`0x003C17F4`, `0x003C188A`).
- `0x003C1680` reports a sub-location explored when all its zones are, and also answers 1 with no lmap held,
  n past the count or a record without points (`0x003C16A7`-`0x003C16DE`).
- `0x003C1DF0` passes the guide schedule to `0x003BD950`, which walks it from the last entry down and returns the
  first whose counter is at most the story counter (`0x00265270`) and whose gate is `0xFFFF` or passes, and 0
  for a null schedule or when no entry does (`0x003BD959`, `0x003BD9B9`). The entry goes to `+0xF0` and the
  request for `menumap_guide<file>` to `+0xF8`.
- `0x003C1DF0` answers 0 without a widget, without `menumap_common.bin` (bit `0x20`), while a guide file is
  held whose picture is not registered (bit `0x4` without `0x40`), or with no schedule
  (`0x003C1DFE`-`0x003C1E46`).
- It frees the guide file and picture it holds before the request (`0x003BC970`, `0x003C1E71`); with no entry it
  frees them and answers 0 (`0x003C1E65`). After the request it clears bit `0x40`, sets bit `0x4` and answers 1
  (`0x003C1ED3`-`0x003C1EF2`).

### Readers of gmap

- `0x003BD890` returns the text of line `+6` of the chosen schedule entry, once the widget's bit `0x40` is set;
  `0x003BD8F0` returns the same text and the picture at `tim2Off`, which `0x003BC4E0` registers at `+0x108`.
- `0x003BD890` answers 0 without a widget, guide file `+0xF8` or entry `+0xF0`, for a line at or past the
  file's `count`, and for a text of `0xFFFF` (`0x003BD89A`-`0x003BD8DC`).
- `0x003BD8F0(file, line, picture)` answers 0 for a null file or a line at or past `count`. When `picture` is
  set it stores the picture there, 0 for a `tim2Off` of `0xFFFF`, before it answers 0 for a text of `0xFFFF`
  (`0x003BD910`-`0x003BD938`).
- The location map's container procedure `0x002BA700` hands the text and picture to `0x0028FD00`; the overlay
  (`0x002B7590`) and the field-time container (`0x003CB650`) also read the text.

### Readers of wmap

- `0x003BD040(area)` builds a World Map entry: position, neighbours, region, the amap type and name, and the
  state bits of `0x003BD480`. It writes area `+1`, region `+2`, the amap type `+3` (`0x002543D0`), position `+4`,
  neighbours `+8`, the name `+0x10` (`0x002543A0`), the area's pair `+0x0C` at `+0x18`, the state bits `+0x1C`
  and 0 at `+0x20` (`0x003BD0A7`-`0x003BD13A`).
- While the widget's `+0xC9` is `0x0F` the name is text `0x17DE` (`0x002F9860`, `0x003BD108`). With state bit
  `0x800` a non-zero extra type byte replaces the amap type and adds state bit `0x20000`
  (`0x003BD171`-`0x003BD181`). It answers 1, and 0 for area 0 with nothing written (`0x003BD19F`).
- An area at or past the table's count, or a table address of 0, leaves the entry pointer 0 (`0x003BD088`,
  `0x003BD094`): the area byte `+1` is written (`0x003BD0A7`) and the next read is of address `0xA` (`0x003BD0AB`).
- `0x003BD480` sets: 1 current area; 2 an area map of one of its groups is owned; `0x4000` every sub-location of
  its groups explored. The current area is that of the current field (`0x003148F0`, `0x00264F90`, `0x00254380`);
  its groups are the groups 0 to 58 whose area (`0x00254380`) it is, and `0x4000` stays set when the area has
  no group or a group has no directory entry (`0x003BD4D1`-`0x003BD578`).
- It also sets 4 area gate passes; 8 marked in the widget's bit set at `+0x270`; `0x10` key item `+0x16`
  owned; `0x20` from `0x003C0A00`. Bits 4 and `0x10` need region non-zero and a word other than `0xFFFF`
  (`0x003BD5B2`-`0x003BD5BF`, `0x003BD63B`-`0x003BD648`).
- Last, `0x10000` extra gate passes, for an extra gate other than `0xFFFF` (`0x003BD6AA`-`0x003BD6BC`), plus
  `0x800` when the area is hidden (`0x003C08B0` answers 0, `0x003BD6C6`), which makes `0x003BD040` use the extra
  type byte.
- `0x003C08B0(area)` decides whether an area is shown: region non-zero and story counter below `until`; then the
  current area is always shown; otherwise the screen mode's own test (`0x02B457E0 + 0xCA`) decides, and when
  it fails the area is still shown if one of its persistence groups passes `0x003C0D70(g, 1)`.
- It answers 0 for area 0 or an area at or past the count, and an `until` of `0xFFFF` never hides
  (`0x003C08DD`-`0x003C0930`). The mode tests (`0x003C0955`-`0x003C09AD`): mode 0 shows every area, mode 2 needs the
  area gate `+0x14` to pass (`0x003C0B70`), mode 3 the area's bit at `+0x270`, mode 4 its map key item owned
  (`0x003C0BE0`) and mode 6 `0x003C0A00`.
- Every other mode goes straight to the group test, over the groups 0 to 58 whose area (`0x00254380`) is this
  one (`0x003C09C2`-`0x003C09E4`).
- `0x003BFFF0` and `0x003C00C0` list the type 0 routes of an area for the World Map host (`0x00550820`,
  `0x00550690`), `0x003C0180` the routes of one special type for its child widget `0x005528C0`.
- `0x003BCCA0(area, route, out)` keeps a route when its far area is shown and returns both areas' positions and
  the route's `x`, `y`. It answers 1, and 0 for a route with `area` at neither end (`0x003BCDCD`) or a far area
  `0x003C08B0` does not show (`0x003BCD2F`); with `out` set it writes a 16-byte row: area, far area, the area's
  `x`, `y`, the route's `x`, `y` and the far area's `x`, `y` (`0x003BCD84`-`0x003BCDBE`).
- `0x003BFE10(region, out)` returns a region's name for `0x005528C0`: it writes the region at `+0`, the name text
  (`0x002F9920`, null for -1) at `+8` and `0x003BFEA0(region)` at `+0x10`, and answers 1; region 0 or a region at
  or past the count answers 0 with nothing written (`0x003BFE34`, `0x003BFE49`).
- `0x003C1D70(widget, area, request)` requests the area picture, kind 7 `0xE8` + `picture` (`0x003C1DC2`), named
  `map_gra_c`, for the World Map host (`0x005632C0`). It hands `0x002493D0` the widget, the request record's
  dword `+0`, the image name at `+8` and dword `+0x10`, and returns its answer; for area 0 or an area at or
  past the count it answers 0 with no request (`0x003C1DE4`).
- `0x003C0250(area)` returns the destination value of an area: the value of the first destination whose area
  byte is `area`, or -1 when no destination names it (`0x003C0294`); `0x002901D0` stores it at
  `[0x0209BE80] + 0x10FAC`, which a script reads back after opening the World Map as a destination picker (menu
  states `0x11` and `0x12`, `0x00254710`).
- `0x003BD1B0(out, region, mode)` builds the World Map's area list for its host `0x00550A00`: a `0x28`-byte
  entry (`0x003BD040`) for every area of the region, or of all regions for -1, that is shown (`0x003C08B0`) or
  passes `0x003C0C50`. In mode 6, with `+0xD0` bit `0x400`, an entry with bit `0x20` takes its labels from
  the selected quest's `QHT0` entry (`0x00473CC0`).
- It then fills each entry's four neighbours: `0x003BFB60(entry, dir, list, n, empty)` follows the authored
  neighbour chain until it meets a listed area, giving -1 for no neighbour (`empty` = 1), a loop or the
  chain's end. When the chain leads nowhere, `0x003BFC70(entry, dir, list, n)` takes the listed area on that
  side (0 up, 1 down, 2 left, 3 right) that `0x003BD6F0` scores lowest, 0xFF when there is no such area.
- `0x003BCAF0(type)`, for the World Map host `0x00552250`: with a non-zero type it clears the bit set `+0x270`,
  and when byte `+0xC8` is 1 it stores the type at `+0xC9` and sets the bits of both areas of every route
  of that type (state bit `0x8` of `0x003BD480`).
- `0x003BFEA0(region)` answers whether the current field's area (`0x003148F0`, `0x00264F90`, `0x00254380`) is in
  the region, or, for an area outside the table, whether the region is 0; `0x003BFE10` uses it.
- `0x003C0BE0(area)` answers whether a shown area's map key item `+0x16` is owned (`0x00309EC0`), for
  `0x003C08B0`.

### Quest steps on the maps

While the widget's `+0xD0` has bits `0x100` and `0x200`, the maps read the selected quest's `QHD0` entry through
`0x00473BB0`, `+0xCB` steps ([Quest menu files](quest-menu-files.md)):

- `0x003C0E30(group)` answers whether a type-1 step's location lies in persistence group `group`
  (`0x00264F90`), and `0x003C15B0(n)` whether it lies in sub-location n (`0x003C0380`); `0x003C05F0` uses the second.
- `0x003BD9F0(location, kind, out)`, for the location page `0x003BE3A0`, counts the shown steps at a location:
  the unlabelled ones for kind 0, the labelled ones for 1, all for any other. It copies into `out` the
  step whose ordinal is `out[0]`, and returns 0 at the first step that is not of type 1.

### Readers of amap

| Function | Reads | Out of range | Result |
|---|---|---|---|
| `0x00254380(group)` | group table | 0 | the group's area |
| `0x002543A0(area)` | name table | area 0 or above the count: empty string | the area name (`0x002F9920`) |
| `0x002543D0(area)` | type table | 0 | the area's type byte, copied by `0x003BD040` |
| `0x002543F0(group)` | map table | 0, also for `0xFFFF` | whether the key item is owned (`0x00309EC0`) |

## Modding notes

- Every file is read whole into a buffer of its kind 7 size in the file-size tables; a resized file needs its
  entry changed in every table ([File size tables](file-size-tables-fst.md)).
- Edit the folder each language loads; `in` serves every language without its own folder.
- A sloc file may hold at most 18 pictures; the slot has room for 18 handles. Keep the picture table's byte
  `+1` at 0, since one reader reads the count as a byte and two as a `u16`.
- Each sloc picture's key must equal an lmap zone's field id and its flag bits under mask `0x3`, or the zone has no
  picture. NPS2 `+0x18` and `+0x1C` set the size the zone takes on the page.
- A NAVIICN2 block needs byte `+7` above `'1'` and a `kinds` value above the highest kind used; the location
  map's draw paths draw kinds 3 to 9.
- A new lmap link must name two zones of its own record, or `0x003BCDE0` drops it. A marker's `dest` is a
  sub-location index and `destPoint` a point of that sub-location's record.
- A guide line is chosen by the schedule in `menumap_common.bin`, not by the guide file; the schedule's
  `file` byte selects `menumap_guide<file>`, and only `00` to `04` have sizes.
- A cmap palette byte k requests kind 7 `0xE1` + k, which must exist in every language.
- The `_e3` sloc copies are never loaded; edit the numbered file.

## Related

- [Map screens](../Menus-And-HUD/map-screens.md): the screens, the containers and the story checks around these files.
- [World map mesh (.mg)](world-map-mesh-mg.md): the World Map picture and its mesh.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the minimap's pictures and placements.
- [TIM2 images](tim2-images.md): the picture format inside sloc and gmap.
- [Cl2 menu colour tables](cl2-menu-colour-tables.md): the palettes the location map takes.
- [Story flags](../Story-Events-And-Hunts/story-flags.md): the gates the tables name.
- [File requests and the read queue](file-requests-and-the-read-queue.md): `0x00249210` and the kind 7 reads.
- [File size tables (.fst)](file-size-tables-fst.md): the sizes that bound each read.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Party: `0x002FE660` calls `0x0031B7E0`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
