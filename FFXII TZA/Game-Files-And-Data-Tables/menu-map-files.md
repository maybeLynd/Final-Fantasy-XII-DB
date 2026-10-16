---
title: "Map menu files: the sloc picture files and the amap, cmap, gmap, lmap and wmap tables behind the location map and the World Map"
kind: "format"
category: "Game files and data tables"
summary: "The menumap files under worldmap/: the 48 sloc files holding each sub-location's zone pictures, their sizes and icon sets; lmap, the zones, markers, links and zoom levels of every sub-location; cmap, the sub-location directory, the per-map exploration thresholds and the guide-line schedule; gmap, the guide lines; wmap, the World Map's regions, areas, routes and Strahl destinations; amap, the area names, area maps and group-to-area table. Covers the layouts as the readers read them, the map-data widget that loads them, what each reader does on the map screens, the shipped files and the rules an edit must follow."
addresses: "02B457E0, 003BC450, 003BC2D0, 00253780, 020927D0, 003C1F00, 003C26C0, 003BF520, 003BF5E0, 003BE2D0, 003BECA0, 003DFBB0, 003DFB50, 003C0340, 003BF430, 003BFF20, 003C1070, 003C0380, 003BE680, 003C2320, 003BCDE0, 003BDFF0, 003C17E0, 003C1680, 003C1DF0, 003BD950, 003BD890, 003BD8F0, 003BD040, 003BD480, 003C08B0, 003BCCA0, 003BFE10, 003C0250, 003C1D70, 00254380, 002543A0, 002543D0, 002543F0, 003BEC50, 003C4AE0, 003BF920"
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
| `menumap_world.bin` | `wmap` | `0xA2` | `003BC2D0` (`003BC305`), when the creator asks for the World Map data |
| `menumap_location.bin` | `lmap` | `0xA3` | `003BC2D0` (`003BC333`), when the creator asks for the location data |
| `menumap_common.bin` | `cmap` | `0xA4` | `003BC2D0` (`003BC35D`), always |
| `menumap_area.bin` | `amap` | `0xA5` | `00253780` (`00253917`) |
| `menumap_guide00.bin` to `04` | `gmap` | `0x496` + n | `003C1DF0` (`003C1EB1`) |
| `menumap_sub00.bin` to `47` | `sloc` | `0x142` + n | `003C1F00` (`003C1FF6`) |

The sloc number n is the sub-location index, the position of the sub-location in `menumap_common.bin`'s
directory; the shipped `menumap_world.h` names the 48 indices (`rbn01_s01` = 0 … `sav01_s02` = 47).

Each language's kind 7 path array, installed by `002DF9A0`, names its own folder: `us`, `fr`, `de`, `it`,
`es`, `kr`, `ch` and `cn`; language 6's array names a `uk` folder that the archive does not contain, and
the remaining languages use `in`. The same arrays name `menumap_guide05.bin` to `15.bin` and
`menumap_sub48.bin` to `73.bin`, which do not ship.

## Layouts

All values are little-endian. The readers form a table address as a `u16` offset plus the low 32 bits of
the buffer address, so the readers assume a buffer below 4 GiB.

### sloc: menumap_subNN.bin

```
header
+0x00  char[4]  magic       "sloc"
+0x04  u32      -           100
+0x08  u16      recordsOff  record directory, from the file start (0x10 in every file)
+0x0A  u16      picturesOff picture table, from the file start
+0x0C  u32      -           0

record directory (at recordsOff)
+0x00  u32      count       one record per zone field
+0x04  u16[count] offset    each record's offset from the directory start

record
+0x00  u16      fieldId     the zone's field id
+0x02  u16      lcmOff      LCMPOS1 block, from the record start; 0xFFFF = none
+0x04  u16      naviOff     NAVIICN2 block, from the record start; 0xFFFF = none

picture table (at picturesOff)
+0x00  u16      count       pictures; 003C26C0 reads only the low byte
+0x02  u16      keysOff     key array, from the table start
+0x04  s32[count] picture   TIM2 picture, from the table start; -1 = none
+0x04 + 4*count  s32[count] placement  NPS2 record, from the table start
keysOff: {u16 fieldId, u8 variant, u8 0}[count]

NPS2 record (32 bytes)
+0x00  char[4]  magic       "NPS2"
+0x18  f32      width       the picture's width on the page
+0x1C  f32      height      the picture's height on the page

NAVIICN2 block
+0x00  char[8]  magic       "NAVIICN2"; byte +7 must be above '1'
+0x08  u16      kinds       icon kinds present (10 in every block)
+0x0A + 4k  u16  offset     kind k's entries, from the block start (k = 1 to 9)
+0x0C + 4k  u16  count      kind k's entry count

icon entry (16 bytes)
+0x00  s16[2]   from        start of the pointer line
+0x04  s16[2]   at          icon position
+0x08  s16      icon        icon number
+0x0A  s16      gate        story gate (0032A8A0)
+0x0C  u8[4]    -
```

The pictures are TIM2 images ([TIM2 images](tim2-images.md)); the files end with the NPS2 records.

### lmap: menumap_location.bin

Header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | magic | "lmap" |
| `04` | `u32` | - | 202 |
| `08` | `u8` | - | 0 |
| `09` | `u8` | count | records (48); every accessor bounds the index by it |
| `0A` | `u16[count] offset` | each record's offset from the file start |  |

Record, one per sub-location:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | zones | A entries |
| `01` | `u8` | markers | B entries |
| `02` | `u8` | links | C entries |
| `03` | `u8` | members | D entries |
| `04` | `A[zones], B[markers]` | 24 bytes each | C[links]              20 bytes each zoom                  8 bytes D[members]            4 bytes each |

A zone and B marker (one point space: A first, then B):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i16[2]` | x, y | position on the page |
| `04` | `u8[4]` | next | four neighbouring points (`003BE810`); `0xFF` = none |
| `08` | `u16[2]` | - | copied to the draw row |
| `0C` | `u16` | fieldId | A: the zone's field id s32      label       B: destination label text id; -1 = destination's name |
| `0E` | `i16` | gate | A: story gate |
| `10` | `u32` | flags | A: bits 0-1 picture variant, bits 2-5 zone group |
| `10` | `u8` | - | B: copied to the draw row |
| `11` | `u8` | dest | B: destination sub-location |
| `12` | `i16` | gate | B: unlock gate; -1 = always |
| `14` | `u8` | - | B: second link point |
| `15` | `u8` | destPoint | B: point in the destination |
| `16` | `i16` | gate | B: second gate |

C link:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16[2]` | fieldIds | the two zones it joins |
| `04` | `i16[6]` | points | three x, y pairs |
| `10` | `i16` | gate | map-jump flag gate; -1 = none |
| `12` | `u16` | - | 0 |

Zoom:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16[3]` | zoom | the record's zoom levels |
| `06` | `u16` | - | 0 |

D member:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16` | node | an A field id |
| `02` | `u16` | member | a further field shown as that zone |

### cmap: menumap_common.bin

Header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | magic | "cmap" |
| `04` | `u32` | - | `0xCB` |
| `08` | `u16` | dirOff | `0x0C` |
| `0A` | `u16` | mapsOff | `0x190` |

Directory (at dirOff), one entry per sub-location:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | count | 48 |
| `04` | `entry[count],` | 8 | bytes: |
| `00` | `u8` | group | persistence group |
| `01` | `u8` | palette | 0 = none, else kind 7 id `0xE1` + palette |
| `02` | `i16` | - |  |
| `04` | `i32` | name | sub-location name text id; -1 = none |

Maps (at mapsOff):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16` | count | 369 |
| `02` | `u16[count] value` | low byte: explored cells a map needs |  |

Guide schedule (at mapsOff + 2 + 2*count, rounded up to 4):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | count | 77 |
| `04` | `entry[count],` | 8 | bytes: |
| `00` | `u16` | counter | story counter at which it applies |
| `02` | `u16` | gate | story gate; `0xFFFF` = none |
| `04` | `u8` | file | guide file number |
| `05` | `u8` | - | 0 |
| `06` | `u16` | line | line index in the guide file |

### gmap: menumap_guideNN.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | magic | "gmap" |
| `04` | `u32` | - | `0x64` |
| `08` | `u16` | textOff | string area, from the file start |
| `0A` | `u16` | tim2Off | TIM2 picture, from the file start; `0xFFFF` = none |
| `0C` | `u16` | - | 0 |
| `0E` | `u16` | count | lines |
| `10` | `entry[count],` | 8 | bytes: |
| `00` | `u16` | counter | copy of the schedule entry's counter |
| `02` | `u16` | gate | copy of the schedule entry's gate |
| `04` | `u16` | text | string offset from textOff; `0xFFFF` = none |
| `06` | `u16` | - | 0 |

The strings are zero-terminated game text ([Text drawing](../Menus-And-HUD/text-drawing.md)).

### wmap: menumap_world.bin

```
header
+0x00  char[4]  magic       "wmap"
+0x04  u32      -           0xCA
+0x08  u16      regionsOff  0x14
+0x0A  u16      areasOff    0x48
+0x0C  u16      routesOff   0x5C8
+0x0E  u16      -           0
+0x10  u16      destsOff    0x7AC
+0x12  u16      -           0

regions: u32 count, s32 name text id[count]; -1 = none
areas:   u32 count, area[count] of 28 bytes, then extra[count] of 8 bytes

area
+0x00  s16[2]   x, y        position on the World Map
+0x04  u8[4]    next        four neighbouring areas
+0x08  u16      until       story counter at which the area disappears; 0xFFFF = never
+0x0A  u8       region      0 = never shown
+0x0B  u8       picture     area picture number
+0x0C  s16[2]   -           copied beside the name
+0x10  s32      name        area name text id (repeated at +0x18)
+0x14  s16      gate        story gate; -1 = none
+0x16  s16      item        area map key item; -1 = none
+0x18  s32      name2

extra
+0x00  s16      gate        story gate; -1 = none
+0x02  u8       type        type byte used while the area is hidden
+0x03  u8[5]    -           0

route: {u8 areaA, u8 areaB, u8 type, u8 0, s16 x, s16 y}
destination: {u16 value, u8 area, u8 0}
```

### amap: menumap_area.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | magic | "amap" |
| `04` | `u32` | - | `0xC9` |
| `08` | `u16` | typeOff | u8 count, u8 type[count], per area |
| `0A` | `u16` | groupOff | u8 count, u8 area[count], per persistence group |
| `0C` | `u16` | mapOff | u16 count, u16 item[count], per group; `0xFFFF` = none |
| `0E` | `u16` | nameOff | u32 count, s32 text[count], per area |

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

## Loader behaviour

### The map-data widget

`003BC450(world, location, owner)` creates the widget `02B457E0` (0x278 bytes, procedure `003BC4E0`) when none
exists. On creation `003BC4E0` clears the sub-location slots and calls `003BC2D0`, which requests
`menumap_world.bin` into `+0xD8` when `world` is set, `menumap_location.bin` into `+0xE0` when `location` is
set, and `menumap_common.bin` into `+0xE8` always, all through `00249210`.

The widget frees the three tables and the guide file at `+0xF8` in its message `0x10` handler, and the
palette at `+0x118` and both slots when it is released (`003C2210`). `menumap_area.bin` is loaded separately
by `00253780` into `020927D0`.

### Sub-location slots and pictures

The widget holds up to two sloc files, in two 0xA8-byte slots at `+0x120`: data pointer `+0`, key array
`+8`, sub-location index `+0x10`, picture count `+0x13` and 18 picture handles from `+0x18`.

1. `003C1F00(widget, owner, request, n)`, through `003C2190`, takes a free slot and requests
   `menumap_sub<n>` (`00249180`). It refuses when both slots are in use, or when one is in use and no other
   cmap entry shares entry n's group.
2. When cmap entry n's palette byte is non-zero it requests kind 7 `0xE1` + that byte into `+0x118`
   (`003C207A`): `Loca_gil.cl2` for 1, `Loca_bhm.cl2` for 2.
3. The overlay page `002B7B80`, the location page `002BAF80` and the preload child `003CB4F0` call it; when it
   refuses they free the other slot (`003C21C0`) or both (`003C21B0`) and try again.
4. When the file has arrived, `003C2200` → `003C26C0` stores the key array and registers every picture whose
   offset is not -1 as the named image `loca_<fieldId>_<variant>` (`0024A480`), with the palette at `+0x118`
   when the entry names a `.cl2`, otherwise the third table of `clutpack_ys.bin` at `+0x110`
   ([Cl2 menu colour tables](cl2-menu-colour-tables.md)). `003C0CF0` reports 0 (absent), 1 (loading) or 2
   (ready).

### Readers of sloc

- `003BF520(field, variant)` returns the picture handle whose key matches, from the slot of the field's
  sub-location; `003C1180` uses the picture's TIM2 size for explored-cell tests and `00402C30` binds it to the
  zone's draw element.
- `003BF5E0` returns the same key's NPS2 record, and `003BEC50(field, key)` returns it for a field,
  finding the field's sub-location with `003C0380` first. `003C2320` copies its width and height into the zone's
  draw row (`+0x24`, `+0x26`), and `003BED70` uses them to size the page around the drawn zones.
- `00404730` draws a zone picture through the zone's explored-cell mask from `002551B0`, which `003C4AE0`
  asks for with `00264790()` when that is positive, and otherwise, or on a null result, takes the block at `02B45A50`; with no mask, or
  with bit 15 of the element's flags, every cell is shown.
- `003BE2D0(field)` returns the field's NAVIICN2 block. `003DFBB0` gives a kind's count (kinds 1 to 9 below
  the block's `kinds`); `003DFB50` gives entry i and drops it when its gate fails.
- `004048E0` draws icon kinds 3 to 8 (through `00403640`, called by `00403970`), and `00403BC0` kind 9. An
  icon whose `from` differs from `at` can get an 8-segment pointer line; with a mask, icons other than 14,
  20, 23 and 24 are shown only when the cell at `from` is explored (`00255150`).
- `003BECA0(field)` returns the field's LCMPOS1 block; the draw paths `002B8EE0` and `002BCB00` pass it to
  `00403640` and `00403BC0`, which leave it unused.

The minimap draws the zone pack's own picture and placement, not these ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

### Readers of lmap

- `003C0340(n)` returns `zones + markers` of record n; `003BF430(n, i)` returns point i (zone for
  `i < zones`, else marker) and its kind (0 zone, 1 marker, 3 none). `003BF920(n, i)` returns point i's
  field id when it is a zone that passes `003C18A0`, and `FFFF` otherwise (callers `003BDB30`, `003BDCD0`).
- `003C0380(field)` finds the field's sub-location: for each cmap entry whose group is the field's
  persistence group (`00264F90`), it maps the field through the record's members (`003BFF20`) and looks for a
  zone with that field id. `003C1070` tells whether the player stands in a zone or one of its members.
- `003C2320` builds a point's draw row. For a zone: position, neighbours, field id, picture variant, the
  zone name (`00377B60`) and the picture size. For a marker: the destination, resolved by `003BDDE0`; the
  label text, or "???" (`0x3EC`) while locked; destination 13 (`sav01_s01`) becomes 47 (`sav01_s02`) when
  the story gate `0x107` passes (`0032A8A0`).
- `003BCDE0` keeps a link when its gate passes and, outside screen mode 6, when `003C1180` accepts its point
  at `+4` or `+0xC`: the zone's area map is owned (`002543F0`), `00377A40` accepts the field, or the point's
  cell is explored.
- `003BDFF0` picks the one zone of a zone group that stands for the group; `003BED70` and `003BCDE0` use it.
- `003BE680(n)` returns the three zoom levels. The pages keep the remembered level (`0209E5B8`) when it is
  one of them, otherwise the first, and scale by 3200 / level (`002B7FFA`-`002B8067`).

### Readers of cmap

- The directory's group byte joins a sub-location to its persistence group (`003C0380`, `003BD480`), and its
  name id gives the marker label fallback (`003C2320`) and the location entry (`003C02B0`).
- `003C17E0(field)` reads the maps array at the field's map index (`003779F0`); a zone counts as explored
  when its explored-cell count (`00255060` on the current zone's mask, `002550E0` on the saved 32 bytes at
  `[020927C0] + 0x224 + 32 × index`) reaches the low byte. `003C1680` reports a sub-location explored when
  all its zones are.
- `003C1DF0` passes the guide schedule to `003BD950`, which walks it from the last entry down and returns the
  first whose counter is at most the story counter (`00265270`) and whose gate is `0xFFFF` or passes. The
  entry goes to `+0xF0` and the request for `menumap_guide<file>` to `+0xF8`.

### Readers of gmap

- `003BD890` returns the text of line `+6` of the chosen schedule entry, once the widget's bit `0x40` is set;
  `003BD8F0` returns the same text and the picture at `tim2Off`, which `003BC4E0` registers at `+0x108`.
- The location map's container procedure `002BA700` hands the text and picture to `0028FD00`; the overlay
  (`002B7590`) and the field-time container (`003CB650`) also read the text.

### Readers of wmap

- `003BD040(area)` builds a World Map entry: position, neighbours, region, the amap type and name, and the
  state bits of `003BD480`.
- `003BD480` sets: 1 current area; 2 an area map of one of its groups is owned; `0x4000` every sub-location of
  its groups explored; 4 area gate passes; 8 marked in the widget's bit set at `+0x270`; `0x10` key item
  `+0x16` owned; `0x20` from `003C0A00`; `0x10000` extra gate passes, plus `0x800` when the area is hidden,
  which makes `003BD040` use the extra type byte.
- `003C08B0(area)` decides whether an area is shown: region non-zero and story counter below `until`; then the
  current area is always shown; otherwise the screen mode's own test (`02B457E0 + 0xCA`) decides, and when
  it fails the area is still shown if one of its persistence groups passes `003C0D70(g, 1)`.
- `003BFFF0` and `003C00C0` list the type 0 routes of an area for the World Map host (`00550820`,
  `00550690`), `003C0180` the routes of one special type for its child widget `005528C0`; `003BCCA0` keeps a
  route when its far area is shown and returns both areas' positions and the route's `x`, `y`.
- `003BFE10(region)` returns a region's name for `005528C0`.
- `003C1D70(area)` requests the area picture, kind 7 `0xE8` + `picture` (`003C1DC2`), named `map_gra_c`, for
  the World Map host (`005632C0`).
- `003C0250(area)` returns the destination value of an area; `002901D0` stores it at `[0209BE80] + 0x10FAC`,
  which a script reads back after opening the World Map as a destination picker (menu states `0x11` and
  `0x12`, `00254710`).

### Readers of amap

| Function | Reads | Out of range | Result |
|---|---|---|---|
| `00254380(group)` | group table | 0 | the group's area |
| `002543A0(area)` | name table | area 0 or above the count: empty string | the area name (`002F9920`) |
| `002543D0(area)` | type table | 0 | the area's type byte, copied by `003BD040` |
| `002543F0(group)` | map table | 0, also for `0xFFFF` | whether the key item is owned (`00309EC0`) |

## Modding notes

- Every file is read whole into a buffer of its kind 7 size in the file-size tables; a resized file needs its
  entry changed in every table ([File size tables](file-size-tables-fst.md)).
- Edit the folder each language loads; `in` serves every language without its own folder.
- A sloc file may hold at most 18 pictures; the slot has room for 18 handles. Keep the picture table's byte
  `+1` at 0, since one reader reads the count as a byte and two as a `u16`.
- Each sloc picture's key must equal an lmap zone's field id and its flag bits 0-1, or the zone has no
  picture. NPS2 `+0x18` and `+0x1C` set the size the zone takes on the page.
- A NAVIICN2 block needs byte `+7` above `'1'` and a `kinds` value above the highest kind used; the location
  map's draw paths draw kinds 3 to 9.
- A new lmap link must name two zones of its own record, or `003BCDE0` drops it. A marker's `dest` is a
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
- [File requests and the read queue](file-requests-and-the-read-queue.md): `00249210` and the kind 7 reads.
- [File size tables (.fst)](file-size-tables-fst.md): the sizes that bound each read.
