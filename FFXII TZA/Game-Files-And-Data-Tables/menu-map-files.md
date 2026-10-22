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
+0x00  u16      count       pictures; 0x003C26C0 reads only the low byte
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
+0x0A  s16      gate        story gate (0x0032A8A0)
+0x0C  u8[4]    -
```

The pictures are TIM2 images ([TIM2 images](tim2-images.md)); the files end with the NPS2 records.

### lmap: menumap_location.bin

Header:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "lmap" |
| `+0x04` | `u32` | - | 202 |
| `+0x08` | `u8` | - | 0 |
| `+0x09` | `u8` | count | records (48); every accessor bounds the index by it |
| `+0x0A` | `u16[count] offset` | each record's offset from the file start |  |

Record, one per sub-location:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | zones | A entries |
| `+0x01` | `u8` | markers | B entries |
| `+0x02` | `u8` | links | C entries |
| `+0x03` | `u8` | members | D entries |
| `+0x04` | `A[zones], B[markers]` | 24 bytes each | C[links]              20 bytes each zoom                  8 bytes D[members]            4 bytes each |

A zone and B marker (one point space: A first, then B):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16[2]` | x, y | position on the page |
| `+0x04` | `u8[4]` | next | four neighbouring points (`0x003BE810`); `0xFF` = none |
| `+0x08` | `u16[2]` | - | copied to the draw row |
| `+0x0C` | `u16` | fieldId | A: the zone's field id s32      label       B: destination label text id; -1 = destination's name |
| `+0x0E` | `i16` | gate | A: story gate |
| `+0x10` | `u32` | flags | A: bits 0-1 picture variant, bits 2-5 zone group |
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
| `+0x10` | `i16` | gate | map-jump flag gate; -1 = none |
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
| `+0x04` | `entry[count],` | 8 | bytes: |
| `+0x00` | `u8` | group | persistence group |
| `+0x01` | `u8` | palette | 0 = none, else kind 7 id `0xE1` + palette |
| `+0x02` | `i16` | gate | story gate; -1 = none (`0x003C12B0`) |
| `+0x04` | `i32` | name | sub-location name text id; -1 = none |

Maps (at mapsOff):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | count | 369 |
| `+0x02` | `u16[count] value` | low byte: explored cells a map needs |  |

Guide schedule (at mapsOff + 2 + 2*count, rounded up to 4):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | 77 |
| `+0x04` | `entry[count],` | 8 | bytes: |
| `+0x00` | `u16` | counter | story counter at which it applies |
| `+0x02` | `u16` | gate | story gate; `0xFFFF` = none |
| `+0x04` | `u8` | file | guide file number |
| `+0x05` | `u8` | - | 0 |
| `+0x06` | `u16` | line | line index in the guide file |

### gmap: menumap_guideNN.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "gmap" |
| `+0x04` | `u32` | - | `0x64` |
| `+0x08` | `u16` | textOff | string area, from the file start |
| `+0x0A` | `u16` | tim2Off | TIM2 picture, from the file start; `0xFFFF` = none |
| `+0x0C` | `u16` | - | 0 |
| `+0x0E` | `u16` | count | lines |
| `+0x10` | `entry[count],` | 8 | bytes: |
| `+0x00` | `u16` | counter | copy of the schedule entry's counter |
| `+0x02` | `u16` | gate | copy of the schedule entry's gate |
| `+0x04` | `u16` | text | string offset from textOff; `0xFFFF` = none |
| `+0x06` | `u16` | - | 0 |

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
| `+0x00` | `char[4]` | magic | "amap" |
| `+0x04` | `u32` | - | `0xC9` |
| `+0x08` | `u16` | typeOff | u8 count, u8 type[count], per area |
| `+0x0A` | `u16` | groupOff | u8 count, u8 area[count], per persistence group |
| `+0x0C` | `u16` | mapOff | u16 count, u16 item[count], per group; `0xFFFF` = none |
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

## Loader behaviour

### The map-data widget

`0x003BC450(world, location, owner)` creates the widget `0x02B457E0` (0x278 bytes, procedure `0x003BC4E0`) when none
exists. On creation `0x003BC4E0` clears the sub-location slots and calls `0x003BC2D0`, which requests
`menumap_world.bin` into `+0xD8` when `world` is set, `menumap_location.bin` into `+0xE0` when `location` is
set, and `menumap_common.bin` into `+0xE8` always, all through `0x00249210`.

The widget frees the three tables and the guide file at `+0xF8` in its message `0x10` handler, and the
palette at `+0x118` and both slots when it is released (`0x003C2210`). `menumap_area.bin` is loaded separately
by `0x00253780` into `0x020927D0`.

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
2. When cmap entry n's palette byte is non-zero it requests kind 7 `0xE1` + that byte into `+0x118`
   (`0x003C207A`): `Loca_gil.cl2` for 1, `Loca_bhm.cl2` for 2.
3. The overlay page `0x002B7B80`, the location page `0x002BAF80` and the preload child `0x003CB4F0` call it; when it
   refuses they free the other slot (`0x003C21C0`) or both (`0x003C21B0`) and try again.
4. When the file has arrived, `0x003C2200` → `0x003C26C0` stores the key array and registers every picture whose
   offset is not -1 as the named image `loca_<fieldId>_<variant>` (`0x0024A480`), with the palette at `+0x118`
   when the entry names a `.cl2`, otherwise the third table of `clutpack_ys.bin` at `+0x110`
   ([Cl2 menu colour tables](cl2-menu-colour-tables.md)). `0x003C0CF0` reports 0 (absent), 1 (loading) or 2
   (ready).
5. `0x003C22B0(slot)`, run by `0x003C21C0`, empties a slot: it releases each registered picture
   (`0x0024A680`), sets the count `+0x13` to 0 and frees the file (`0x003697F0`).

### Readers of sloc

- `0x003BF520(field, variant)` returns the picture handle whose key matches, from the slot of the field's
  sub-location; `0x003C1180` uses the picture's TIM2 size for explored-cell tests and `0x00402C30` binds it to the
  zone's draw element.
- `0x003BF5E0` returns the same key's NPS2 record, and `0x003BEC50(field, key)` returns it for a field,
  finding the field's sub-location with `0x003C0380` first. `0x003C2320` copies its width and height into the zone's
  draw row (`+0x24`, `+0x26`), and `0x003BED70` uses them to size the page around the drawn zones.
- `0x00404730` draws a zone picture through the zone's explored-cell mask from `0x002551B0`, which `0x003C4AE0`
  asks for with `0x00264790()` when that is positive, and otherwise, or on a null result, takes the block at `0x02B45A50`; with no mask, or
  with bit 15 of the element's flags, every cell is shown.
- `0x00404730` places the picture with `0x003C46B0(…, element, …)`: from the element record it sets up a matrix from
  `+0x20`, turns it by -π/2 (`0xBFC90FDB`, `0x003985B0`) and by the negated `+0x1C` (`0x00398C50`), sets it at half of
  `+0x04` and `+0x08`, and combines it (`0x003977B0`) with the record's `+0x14`/`+0x18` and with a second matrix moved
  by -`+0x0C` and -`+0x10`; `0x003C6420` then draws with the result.
- `0x003BE2D0(field)` returns the field's NAVIICN2 block. `0x003DFBB0` gives a kind's count (kinds 1 to 9 below
  the block's `kinds`); `0x003DFB50` gives entry i and drops it when its gate fails.
- `0x004048E0` draws icon kinds 3 to 8 (through `0x00403640`, called by `0x00403970`), and `0x00403BC0` kind 9. An
  icon whose `from` differs from `at` can get an 8-segment pointer line; with a mask, icons other than 14,
  20, 23 and 24 are shown only when the cell at `from` is explored (`0x00255150`).
- `0x00400190(page, record)` appends each drawn icon's record to the page's draw list: head `+0x00`, tail `+0x08`,
  count `+0x1412`; records link forward through `+0x28` and back through `+0x30`. `0x00403BC0` and `0x004048E0` call
  it for every icon they draw.
- `0x003BECA0(field)` returns the field's LCMPOS1 block; the draw paths `0x002B8EE0` and `0x002BCB00` pass it to
  `0x00403640` and `0x00403BC0`, which leave it unused.

The minimap draws the zone pack's own picture and placement, not these ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

### Readers of lmap

- `0x003C0340(n)` returns `zones + markers` of record n; `0x003BF430(n, i)` returns point i (zone for
  `i < zones`, else marker) and its kind (0 zone, 1 marker, 3 none). `0x003BF920(n, i)` returns point i's
  field id when it is a zone that passes `0x003C18A0`, and `FFFF` otherwise (callers `0x003BDB30`, `0x003BDCD0`).
- `0x003C0380(field)` finds the field's sub-location: for each cmap entry whose group is the field's
  persistence group (`0x00264F90`), it maps the field through the record's members (`0x003BFF20`) and looks for a
  zone with that field id. `0x003C1070` tells whether the player stands in a zone or one of its members.
- `0x003C2320` builds a point's draw row. For a zone: position, neighbours, field id, picture variant, the
  zone name (`0x00377B60`) and the picture size. For a marker: the destination, resolved by `0x003BDDE0`; the
  label text, or "???" (`0x3EC`) while locked; destination 13 (`sav01_s01`) becomes 47 (`sav01_s02`) when
  the story gate `0x107` passes (`0x0032A8A0`).
- `0x003BCDE0` keeps a link when its gate passes and, outside screen mode 6, when `0x003C1180` accepts its point
  at `+4` or `+0xC`: the zone's area map is owned (`0x002543F0`), `0x00377A40` accepts the field, or the point's
  cell is explored.
- `0x003BDFF0` picks the one zone of a zone group that stands for the group; `0x003BED70` and `0x003BCDE0` use it.
- `0x003BE680(n)` returns the three zoom levels. The pages keep the remembered level (`0x0209E5B8`) when it is
  one of them, otherwise the first, and scale by 3200 / level (`0x002B7FFA`-`0x002B8067`).
- `0x003BE1E0(n, group, out)` returns the point that stands for zone group `group` of record n (`0x003BDFF0`),
  with its index in `out`, -1 when there is none; `0x003BDDE0`, `0x003BED70`, `0x003C12B0` and `0x003C1A20` use it.
- `0x003BE700(n, dest)` returns the first marker of record n whose destination byte `+0x11` is `dest`, or -1
  (`0x003C2320`).
- `0x003C0D30(n, i)` runs point i's gate test, `0x003C18A0` for a zone and `0x003C0F70` for a marker
  (`0x003BDDE0`, `0x003BDFF0`).
- `0x003C0740(out, n, i)` lists, as 16-byte rows, the links of record n that `0x003BCDE0` keeps for zone point
  i, when the point passes its gate and its draw state (`0x003BCBA0`) lacks bit 11; it returns the count.
  `0x003C0890`, called by `0x00402A40`, first stores its fourth argument at the widget's `+0xCA`.
- `0x003C1A20(out, n, kind, x, y)` lists record n's points for the location page `0x003BE3A0`: zones for kind
  0 (at most 20), markers for 1 (at most 16), both for 2 (at most 24). A zone group appears once, through
  `0x003BE1E0`; other points only when their gate passes or the widget's `+0xD0` has bit `0x800`.
- Each of its `0x18`-byte rows holds the point index, the point and its kind, and `x`, `y` receive the
  smallest zone position.
- `0x003BE950(row, dir, rows, n)` picks the next cursor point in direction dir (0 up, 1 down, 2 left, 3
  right) for `0x003C2320`. It measures from the centres of the points, a zone's from its picture size
  (`0x003BF5E0`), a marker's from its label size (`0x0029CD00`), and takes the point on that side that
  `0x003BD6F0` scores lowest with the direction vector `0x01EFE330`, skipping zones with draw bit 11; 0xFF
  when none.

### Readers of cmap

- `0x003C0450(out, group, check)` lists the sub-locations that share a persistence group for the World
  Map (`0x00551800`, `0x00551930`, `0x00551B30`). It returns 0 for a group of `0x3B` or more and for a
  group with fewer than two of the first 50 directory entries; with `check` set and a group other
  than the current field's (`0x00264F90`), also when no entry of the group is accepted.
- Otherwise it writes a `0x18`-byte row per entry of the group that `0x003C12B0` accepts (index, group,
  the name text through `0x002F9920` or null for -1, and `0x003C05F0(index)`) and returns the count.
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
  `[0x020927C0] + 0x224 + 32 × index`) reaches the low byte. `0x003C1680` reports a sub-location explored when
  all its zones are.
- `0x003C1DF0` passes the guide schedule to `0x003BD950`, which walks it from the last entry down and returns the
  first whose counter is at most the story counter (`0x00265270`) and whose gate is `0xFFFF` or passes. The
  entry goes to `+0xF0` and the request for `menumap_guide<file>` to `+0xF8`.

### Readers of gmap

- `0x003BD890` returns the text of line `+6` of the chosen schedule entry, once the widget's bit `0x40` is set;
  `0x003BD8F0` returns the same text and the picture at `tim2Off`, which `0x003BC4E0` registers at `+0x108`.
- The location map's container procedure `0x002BA700` hands the text and picture to `0x0028FD00`; the overlay
  (`0x002B7590`) and the field-time container (`0x003CB650`) also read the text.

### Readers of wmap

- `0x003BD040(area)` builds a World Map entry: position, neighbours, region, the amap type and name, and the
  state bits of `0x003BD480`.
- `0x003BD480` sets: 1 current area; 2 an area map of one of its groups is owned; `0x4000` every sub-location of
  its groups explored; 4 area gate passes; 8 marked in the widget's bit set at `+0x270`; `0x10` key item
  `+0x16` owned; `0x20` from `0x003C0A00`; `0x10000` extra gate passes, plus `0x800` when the area is hidden,
  which makes `0x003BD040` use the extra type byte.
- `0x003C08B0(area)` decides whether an area is shown: region non-zero and story counter below `until`; then the
  current area is always shown; otherwise the screen mode's own test (`0x02B457E0 + 0xCA`) decides, and when
  it fails the area is still shown if one of its persistence groups passes `0x003C0D70(g, 1)`.
- `0x003BFFF0` and `0x003C00C0` list the type 0 routes of an area for the World Map host (`0x00550820`,
  `0x00550690`), `0x003C0180` the routes of one special type for its child widget `0x005528C0`; `0x003BCCA0` keeps a
  route when its far area is shown and returns both areas' positions and the route's `x`, `y`.
- `0x003BFE10(region)` returns a region's name for `0x005528C0`.
- `0x003C1D70(area)` requests the area picture, kind 7 `0xE8` + `picture` (`0x003C1DC2`), named `map_gra_c`, for
  the World Map host (`0x005632C0`).
- `0x003C0250(area)` returns the destination value of an area; `0x002901D0` stores it at `[0x0209BE80] + 0x10FAC`,
  which a script reads back after opening the World Map as a destination picker (menu states `0x11` and
  `0x12`, `0x00254710`).
- `0x003BD1B0(out, region, mode)` builds the World Map's area list for its host `0x00550A00`: a `0x28`-byte
  entry (`0x003BD040`) for every area of the region, or of all regions for -1, that is shown (`0x003C08B0`) or
  passes `0x003C0C50`. In mode 6, with `+0xD0` bit `0x400`, an entry with bit `0x20` takes its labels from
  the selected quest's `QHT0` entry (`0x00473CC0`).
- It then fills each entry's four neighbours: `0x003BFB60(entry, dir, list, n, none)` follows the authored
  neighbour chain until it meets a listed area, giving -1 for no neighbour (`none` = 1), a loop or the
  chain's end. When the chain leads nowhere, `0x003BFC70(entry, dir, list, n)` takes the listed area on that
  side (0 up, 1 down, 2 left, 3 right) that `0x003BD6F0` scores lowest, 0xFF for none.
- `0x003BCAF0(type)`, for the World Map host `0x00552250`: with a non-zero type it clears the bit set `+0x270`,
  and when byte `+0xC8` is 1 it stores the type at `+0xC9` and sets the bits of both areas of every route
  of that type (state bit 8 of `0x003BD480`).
- `0x003BFEA0(region)` answers whether the current field's area (`0x003148F0`, `0x00264F90`, `0x00254380`) is in
  the region, or, for an area outside the table, whether the region is 0; `0x003BFE10` uses it.
- `0x003C0BE0(area)` answers whether a shown area's map key item `+0x16` is owned (`0x00309EC0`), for
  `0x003C08B0`.

### Quest steps on the maps

While the widget's `+0xD0` has bits 8 and 9, the maps read the selected quest's `QHD0` entry through
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
- Each sloc picture's key must equal an lmap zone's field id and its flag bits 0-1, or the zone has no
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
