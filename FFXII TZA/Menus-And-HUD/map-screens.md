---
title: "Map screens: the World Map, the location map, the map overlay and the minimap, and the map data and story flags they read"
kind: "system"
category: "Menus and HUD"
addresses: "0x00253C70, 0x002B6350, 0x002B9D30, 0x003BC450, 0x003BC2D0, 0x003C18A0, 0x003C5910, 0x003C4070"
---

## What the player sees

- The main menu's "World Map" shows Ivalice: "Select a location map to examine from the map of Ivalice."
- Display Map opens the location map of the current area.
- Map Transparency lays the area map over the field and takes it away again.
- A small map in the corner of the field shows the surroundings, the party and nearby markers.
- Places not yet visited or mapped are hidden, and unrevealed names show "???".

## How it works

### Names

| Map | Shipped text | Code |
|---|---|---|
| World Map | `menu_command.bin` `0x4B7`, help `0xCCA` | main-menu entry `0x00281C36` |
| location map | the phrase in `0xCCA`; opened by the control "Display Map" (`0x589`) | menu request `0x21` ([Menus](menus.md)) |
| map overlay | toggled by the control "Map Transparency" (`0x586`); its layout keys are `TrackMap*` | `0x002B6220` |
| minimap | the script verbs `shownavimap`, `hidenavimap`, `setnavimapindex` and others | widget `0x003C5910` |

The two controls are rows 28 and 25 of the Controls screen (`0x002414B0`; [Control remapping](../Controls-And-Input/control-remapping.md)).

### Opening from the field

The input arbiter `0x00253C70` keeps the map state in `0x02092750`:

1. Map Transparency toggles the state between 0 and 3 and remembers it in `0x0209E5B0` (`0x00253E2F`-`0x00253E63`).
2. State 3 opens the map overlay with `0x002B6220(1)` (`0x00253DE2`) when the field-time container is ready (`0x003CB3E0`),
   `0x02092754` is 0, the field has a map record (`0x003BFDF0`) and the story counter is at least 16
   (`0x00253DD1`-`0x00253DDA`).
3. Display Map closes the overlay and posts menu request `0x21`, the location map (`0x00253EA4`-`0x00253EF2`). Leaving
   the location map restores the overlay as it was (`0x002BBA2F`-`0x002BBA3C`).
4. While the state is not 3, the overlay is closed every frame (`0x002B6260`, `0x00253C92`).

The location map also opens from `0x0028E630`, `0x0028E660` and `0x0028E690`, and the World Map host `0x00550400` from
`0x0028E690` and `0x0028E790` ([Menus](menus.md)).

### The two-page container

The overlay and the location map each have a container of 0x179E0 bytes, at `0x0209E5C0` (`0x002B6350`, procedure
`0x002B7590`) and `0x0209E5F0` (`0x002B9D30`, procedure `0x002BA700`). Each holds two 0xBC08-byte pages in place, at `+0x1B0`
and `+0xBDC0`, and flips between them:

1. The first call creates the container with no page (`0x002B638F`-`0x002B63D7`).
2. A container message `0x20` sets its open request, bit 7 of `+0x179D2`.
3. The next frame's step builds a page in the other slot (`0x00245000`, `0x002B6474`), flips bit 2, attaches the page
   and sends it `0x21` (`0x002B6526`-`0x002B6541`).

A page posts messages to every ancestor up to the root through `0x00275440`, which follows the parent link `+0x10`
that `0x00244960` sets; its container acts on `0x2B` when it has opened and `0x1F` when it is cancelled. The page procedures `0x002B7B80` and `0x002BAF80` answer
the same 17 messages through their tables at `0x198EB0` and `0x19C28C` from the image base.

`0x002B6220` also copies the field-time container's resources into the overlay's `+0x190` and sends it `0x10` and
`0x20` (`0x002B6570`).

### The field-time container

`0x02B47760` (`0x003CB440`, procedure `0x003CB650`) draws nothing. It holds the map resources, the map-data widget and a
preload child `0x003CB4F0` that fills the map cache, and its bit 7 marks the preload as finished (`0x003CB551`-`0x003CB55F`),
which the overlay waits for. It is created from `0x00253A30` and the HUD-on step `0x00251F40`, and destroyed by
`0x003CB410`.

### Map resources

`0x00404060` loads the 32-byte record every page reads at `+0x130`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32[2]` | back | LocaBack_c.tm2 (kind 7 `0xBA`) |
| `+0x08` | `u32[2]` | atlas | Loca_8_c.tm2 (`0xB9`) |
| `+0x10` | `u32[2]` | line | w_line01.tm2 (`0xB0`), the texture of the page's line quad |
| `+0x18` | `u32[2]` | mrp | Loca.mrp (`0xBF`) |

### The map-data widget

`0x003BC450(world, location, owner)` creates the widget `0x02B457E0` once (`0x003BC463`), and `0x003BC2D0` loads:

| File (kind 7) | When |
|---|---|
| `menumap_world.bin` (`0xA2`) | `world` is set: only the World Map (`0x003BC440`, `0x005505E4`) |
| `menumap_location.bin` (`0xA3`) | `location` is set: all three creators |
| `menumap_common.bin` (`0xA4`) | always |

The location container (`0x002BA15C`) and the field-time container (`0x003CB4CC`) pass `(0, 1)`. `0x003C1DF0` then picks the
last entry of the guide table in `menumap_common.bin` whose story counter and story gate pass (`0x003BD950`) and loads
`menumap_guideNN.bin` (kind 7 `0x496` + the entry's byte `+4`). `menumap_area.bin` (`0xA5`) is loaded separately into
`0x020927D0` (`0x00253780`).

### What a page draws

Each frame, a page rebuilds its element list (`0x00402A40`) and draws (`0x002B8A19`-`0x002B8B11`):

1. one quad textured with `w_line01.tm2` (`0x00404230`);
2. the line elements (`0x004043B0`), pulsing the marked ones;
3. one marker per point, each a small map view through `0x003C4070` in mode 2 (`0x00404120`, `0x002B96E7`);
4. the labels (`0x004044D0`).

### Zoom and panning

A page keeps its zoom in percent at `+0xD4` and its scroll at `+0xC8`/`+0xCC`:

1. The overlay page starts at `TrackMapScale` (200, `0x002B806C`) through `0x002B7210` and `0x002B6AE0`.
2. `0x002B6AE0(page, zoom)` changes the zoom and keeps the view centre still. With `c = [+0x9C] >> 1`,
   `0x002B69B0` takes `v = (c - [+0xC8]) * 100 / [+0xD4] * zoom / 10`, adds 10 when `v % 10 >= 5`, and sets the
   scroll to `c - v / 10`, all integer divides; y is the same with `+0x9E` and `+0xCC` (`0x002B69BF`-`0x002B6AD4`).
3. Each frame `0x002B66E0` keeps the tracked point at `+0xBBD8`, placed at the current zoom (`0x00403550`), inside a box
   of 32 units either side of the view centre. It moves the scroll a sixth of the way per call, at least 1 unit,
   within the bounds `+0xF8`-`+0x104`, and centres an axis whose bounds cross (`0x002B6865`-`0x002B6923`).

`0x002B6950(out, w, h, mw, mh)` gives a page's margins: 24 units, or the half difference when the map is smaller than
the view. `0x002B6B50` gives the icon scale from the display aspect (`0x0017FFD0`) and the floats `0x01E0CE50`, `0x01E0CE58`
and `0x01E0CE5C`, 1.5 for an aspect below one third.

### Points, lists and the legend

`0x002B7460(page)` lists the page's points: `0x003BE3A0` fills up to `0x480` bytes of rows for the map `+0x138` in the
mode `+0xBBE0`, each marked with bit 15 when the page's `+0x13A` bit 3 is set, and `0x00402D20` turns them into the
element list `+0xBBC0`; mode 6 also runs `0x00402BF0`. `0x002B9A20` draws each element of a list through `0x002B8EE0`,
passing the highlight to the selected one.

A point's name comes from `0x002B9C70` by its kind byte `+0x0D`:

| Kind | Name |
|---:|---|
| `1` | the area name `0x00377B60` ([area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)) |
| `2` | an NPC name, `0x0026DEA0` with the Bank2048 bit (`0x0032A930`) ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `3` | a shop's name, through the shop's name id `0x002FAE40` |
| `4` | the text id itself |
| other | the legend label of its icon `+0x08` |

The legend is the 14 pairs of icon frame and text id `0x187F`-`0x188C` at `0x00916A10`. The location map's legend
pane `0x002BC310` paints each row with `0x002BA650`, and the point list pane `0x002BA310` sizes itself to the widest name
(`0x002BA530`, measured with `0x0029CD00`) and paints each row with `0x002BD8C0`: the name and an icon, from the shared atlas
(`0x0035D460`) for icons below `0x13` and from the page's own atlas for the rest. `0x002B6310(location)` returns the area
of a sub-location's persistence group (`0x003C02B0`, `0x003BF6C0`;
[menu map files](../Game-Files-And-Data-Tables/menu-map-files.md)).

The point list pane takes its rows from the sub-location icons of the page's sloc block (`0x003BE2D0` of the page's
`+0x1C`), through `0x00402000(rows, page)` (`0x002BA347`, `0x002BA3A2`):

1. it walks kinds 3 to 8 with `0x003DFBB0` and `0x003DFB50`, keeping the entries `0x003FFF40` accepts;
2. unless the page's `+0x28` bit 9 is set, it skips an icon other than `0x14`, `0x17` and `0x18` whose 16-unit cell is
   not visited (`0x00255150`), on the visit mask that `0x00403F90` copies from `0x002551B0` (all `0xFF` when there is none or
   `+0x28` bit 15 is set; the buffer of `0x003C4AE0` when bit 0 is set);
3. an icon `0x0E` adds no row: its entry number goes to `+0xC` of the row before it;
4. each other entry adds a 0x18-byte row {entry, kind `+8`, entry number `+0xA`, `0xFFFF` at `+0xC`}, and the count is
   returned (a null `rows` only counts).

`0x004022F0(sloc, icon)` returns 1 when any icon of kinds 3 to 8 equals `icon`, treating `0x14`, `0x17` and `0x18` as one
icon (`0x003BCBA0`, `0x003BCC46`). `0x00402250(x, y, page, kind, i)` returns the `at` position (`+4`, `+6`) of one sloc entry.

### Page element helpers

The element list of a map page is linked through `+0x60`. The two page procedures (`0x002B7B80`, `0x002BAF80`) share these
helpers:

- `0x004026B0(list, id)` finds the element whose byte `+1` is `id`; `0x00402200` the first with `+0x28` bit 5;
  `0x00402230` the first with bit 0, or the head.
- `0x003C4AB0()` (`0x002B8435`, `0x002BBD60`) passes the block at `0x02EBA488` to `0x002DD550(block, -4)`, which writes it
  into the GS command buffer being filled (`0x02EBEFC8 + 0x18 x [0x02EBEFF0]`) and flips the buffer (`0x003A1DB0`)
  ([Render command list](../Graphics/render-command-list.md)).
- `0x00402DB0(element, buttons)` moves the cursor (`0x002BBBD4`): bits `0x10`, `0x40`, `0x80` and `0x20` take the
  element named by bytes `+8`, `+9`, `+0xA` and `+0xB`, and the element stays put when that id is `-1` or absent.
- `0x004023D0(lines, line)` returns 1 when the line list (linked through `+0x98`) already holds a line with the same
  two ids (`+0x80`, `+0x82`) and the same two end points (`+0x84`/`+0x86`, `+0x8C`/`+0x8E`), each pair in either
  order; the element-list rebuild `0x00402A40` asks it before adding a line (`0x00402B25`).
- `0x00403130(list, zoom)` sets the size `+0x34`/`+0x36` of every element of type 1 (byte `+2`) to its base
  `+0x48`/`+0x4A` divided by the zoom.
- `0x00403180(list, selected)` animates each element per frame: `+0x4C` steps by 16 toward `0x80` (`0x40` with `+0x4E`
  bit 1) while `+0x4E` bit 0 is set and down otherwise; the scale `+0x38` grows by 0.05625 (0.046875 when the
  language test `0x00254A10` is true) to 1.0, or shrinks to 0.9 (0.75) with `+0x4E` bit 2; the highlight `+0x50` rises by
  16 to 256 on the selected element and falls by 16 to 0 on the others.
- `0x00402F00(list, w, h)` copies the first bit-0 element's rectangle `+0x20`-`+0x26` to `+0x30`-`+0x36` and, while
  `0x00264790()` is below 1, projects the party leader (`0x0035D320`, `0x003588B0`, `0x00265020`) through the minimap view
  (`0x003C3F90`, `0x00202B70`) and shifts the element by how far the leader falls outside a `w` by `h` box.
- `0x00402610(item, src)` stores `0x00275320` of the item's current values at `+0`, copies `src`'s rectangle
  `+0x30`-`+0x36` to `+8` and clears `+0x10`; `0x004026D0(out, src)` copies the same rectangle twice; `0x004022D0` sets
  a rectangle to {0, 8, 8, 8, 8, `0x100`}.
- `0x00403330(fade)` raises `+0x10` by a sixth of its distance to 256, at least 6, and returns true at 256.
- `0x00403600(out, sprite)` and `0x00403F00` (pane `0x002BC9C0`) size and draw a sprite 1.75 times its height
  (`0x002D8C80`).
- `0x004041D0(slots)` releases three child widgets (`0x0024A680(w, 1)`) and the buffer in the fourth slot (`0x003697F0`), for
  the location container (`0x002BADD9`) and the field-time container (`0x003CB931`).

The location map's caption pane `[0x02B62D78]` (created by `0x00402680`, procedure `0x00403380`) carries an icon and three
labels. `0x00402490(texts)` sets the labels from the text ids at `+8`, `+0x10` and `+0x18` of its argument (`-1` keeps a
label; `-1` at `+0x10` hides the second), measures the first with `0x0029CD00` to place the rest, and a non-negative
`+0` picks the row of the fourth child. `0x00402730(atlas, group, frame)` sets the icon and moves the second label past its
width.

`0x002BA1B0(v)` gives the location container a y from the menu bars: the screen height `0x01E0C1DC`, less
`0x002C9430(0x81)` when `0x002C9430(0x80) + v` is not 0. `0x002BA1F0` is the location map's exit callback: when the location container `0x0209E5F0` is gone
and `0x00402220` answers 0, it returns to the menu with `0x002814E0(0x417)`. `0x002BC2C0`, the exit callback `0x002BAF80` installs
(`0x002BB202`), does the same when neither `0x0209E5F0` nor `0x0209E5F8` is set, after `0x00285F00(0x0209E608)`.

### What is shown

The story gate `0x0032A8A0` ([Story flags](../Story-Events-And-Hunts/story-flags.md)) and the encoded-id query
`0x00309EC0` decide every map element:

| Element | Shown when |
|---|---|
| area point (`0x003C18A0`) | its gate (word `+0xE`) passes and the area is current, visited or its map is owned (`0x003BCBA0`) |
| link point (`0x003C0F70`) | its gate `+0x16` passes, and its map is owned, or its gate `+0x12` is `0xFFFF` or set |
| label (`0x003C2320`) | revealed; otherwise "???" (`0x3EC`, `0x003C25B1`) |
| location (`0x003C12B0`) | its kind's gate passes and its map is owned, or one of its points can be drawn |
| World Map destination (`0x003C08B0`) | its gates pass and the story counter (`0x00265270`) is below its word `+8` |
| icon of a sub-location (`0x003DFB50`, `0x003FFF40`, `0x00400CF0`) | its word `+0xA` is 0, or its gate passes; 1 never shows |

`0x003BCBA0` builds the state an area point reads: the current area (`0x003C1070`), a visit byte at
`[0x020927C0] + 0x224 + 32 x entry` (`0x00255200`), and the area's map as a key item of class `0x8000` (`0x002543F0`; the
map list is `menumap_area.bin` `+0xC`).

### The minimap

The minimap is the widget `0x003C5910`, at `0x02B476B0` (`0x003C80C0`):

1. `0x003C5E00` shows it, from the HUD-on step and the verb `shownavimap` (`0x00352390`), and `0x003C58B0` hides it.
2. Every world tick, `0x003C6000` keeps it in step while the save-RAM status allows it (`0x00377750`) and copies the party
   position to `0x02B45810` (`0x00359150`).
3. Its draw callback `0x003C32B0` calls `0x003C4070` in mode 0, which draws the zone's own map picture `[0x02B457F0]` at 4
   pixels per world unit (`0x004001D0`), a 12-spoke ring (`0x003C34E0`), the blinking party marker (`0x003C2E60`) and up to
   64 icons (`0x003C3340`, `0x00400CF0`).
4. While the map is jammed (`0x00377780`, verb `setnavimapjamming`), `0x004001D0` draws its jamming passes over the
   picture (`0x00401620`, `0x004014E0`, `0x004010A0`) and `0x003C4070` leaves out the ring, the party marker and the icons.

The ring takes its entry count from `0x00264AC0(list)` (`0x003C350B`), the first dword of that per-class table of the zone
script's image (header `+0x70`, `0x00264AE0`), and gets a 6-byte style for each entry from `0x002648F0(entry, out)`
(`0x003C35D5`, `0x003C36BA`):

- the defaults are bytes 1, 1, 1, 1 and the word `0xFFFF`;
- for an entry, `0x00264920` refills them from record `+0x1D` of the image's table at header `+0x8C` (`0x00264870`):
  the story-flag gate `0x0032A8A0` of its words 0, 1, a mode word (4 on a chocobo, `0x00303EC0`; 3 while `0x003135C0`
  answers; else 2) and 6, then its word 5.

The minimap's other small state:

- `0x003C5060`, from the tick (`0x003C609B`), keeps a trail of party positions while `0x0035D600()` answers 1 (bit 5 of
  `0x022C83E8`, which `0x0035D610(v)` sets to v): when the party is more than 3.0 from the last point `0x02B45850`/`0x02B45858`
  in x and z, it writes the position to `0x02B45860 + 16 x [0x02B45960]`, makes it the last point, counts `0x02B45962` up
  to 16 and moves the index on modulo 16.
- `0x003C5030` clears that block (`0x120` bytes from `0x02B45850`) and the live marker list (`0x1430` bytes from
  `0x02B46280`); Ghidra's references to it are only its unwind entry.
- `0x003C5400(i, v)` and `0x003C53E0(i)` set and clear the dword `0x02B45970 + 4i`; `0x003FFF70` sets slot 1 to the
  controlled character's record `+8` (`0x00272E10`) when that is non-zero, and clears it otherwise.
- `0x003C5720(box, item, angle, &x, &y)`, from the widget's draw (`0x003C5CE7`, `0x003C5D21`), returns the item's position,
  turned by `angle` about the centre of the box `+0x0C`-`+0x12` when the angle is not 0.

The tick also uncovers the map around the party: `0x003C6000` calls `0x003C5500` (`0x003C6096`).

1. It works only while `0x0035D630()` answers 1, bit 7 of `0x022C83E8` clear (`0x0035D640(v)` sets the bit for v = 0 and
   clears it otherwise, through the thunk `0x002E23D0`).
2. It works only when the party position `0x02B45810`/`0x02B45818` or the angle `0x02AEDF94` has changed since its last run.
3. It turns a 6 by 6 grid of points, -24 to 16 in steps of 8 around the party, by the angle.
4. For each point inside the map (width `0x02B45A58`, height `0x02B45A5A`) it sets the bit of the point's 16-unit cell in
   the explored mask `0x02B45A50` (row stride `0x02B45A60` bytes), the mask the map pictures are drawn through
   ([Menu map files](../Game-Files-And-Data-Tables/menu-map-files.md)).

The picture comes from the zone's map pack: `0x003C63A0` registers it and `0x00379870` places it, chosen by
`setnavimapindex` (`0x00377400`) ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

### Minimap markers

The actors come from a list the minimap tick rebuilds first: `0x003C6000` calls `0x0035D070` (`0x003C6013`), which runs
`0x0035E5F0(0x022C8060)`. That builds the lists of actor managers 0 to 2 (`0x0046B560(2)`) and copies them in order, at most
128: handles to `0x022C8500` (`0x0035D500`), actors to `0x022C8700` (`0x0035D4F0`), the total at `0x022C8B00` (`0x0035D510`),
and each manager's start and count at `0x022C8B02 + i` and `0x022C8B04 + i`.

`0x003C5130` rebuilds the minimap's marker list: one 32-byte entry per actor at `0x02B45A80` (count `0x02B45A70`), then the
navigation icons (`0x00400550`), then `0x004000E0` merges them into the live list at `0x02B46280`:

1. every live node gets `+0x20` bit 1 (stale);
2. `0x00400AC0(entry, list, i)` handles entry `i`. Unless the entry's bit 18 is set, the actor `0x003588B0(+4)` must
   exist, and its state `0x00234D40` of 2 hides a node it already has (`+0x20` bit 2).
3. A node with the same id is moved to position `i` (`0x00400650` unlinks it); a new id takes the next free node of
   64 (0x50 bytes each from `+0x10`, ring index `+0x1411`, count `+0x1412`), zeroed, with `+0x22` = `0x80` and
   the scale `+0x24` = 1.0 only before the list's first fill.
4. The 32 bytes are copied in and the stale bit cleared. After the pass every node still stale and not hidden loses
   its live bit 0, and `+0x1410` bit 0 records the first fill.

The draw `0x003C6B70` scales each marker's colour by `+0x22` (`0x80` is full) and its size by `+0x24`. It finds the
sprite with `0x00400420(out, entry)`: kinds 5 to 7 use the entry's byte `+1`; other kinds look up the byte table
`0x00D120E0` by kind, plus 6 when bit 19 is set, in the shared atlas `0x0035D460`.

The routines below these draws, the trail, ring and marker quads, the picture binds and colour records written
into the VIF packets, the explored-mask set-up and the page helpers, are listed with their callers in
[map-screens-subroutines.tsv](map-screens-subroutines.tsv).

### The World Map host

The World Map host `[0x02CA8F38]` (`0x00550400`) keeps its state in the word `+0x170`. `0x00550510(v)` stores `v` in bit 3
(`0x0028E72A`, `0x0028E7EE`). `0x00550610()` re-attaches the host to the root `[0x0208EA20]` and its screen `+0x160` to
`[0x0208EA28]` (`0x00246AD0`) when bits 0 and 2 are both set, clearing bit 1; otherwise it sets bit 1 (`0x0028E770`,
`0x0028E81A`).

### World Map places

The view `0x005528C0` keeps its places in a list linked through `+0x140`; each place has its screen position at
`+0x3C`/`+0x3E` and its flags at `+0x130` and `+0x54`.

- `0x00554BD0` sorts the places into a tree through `+0x150`-`+0x160` by a key at `+0x168` (0 or 1.0, from the byte
  `+0x3B` and the word `+0x3E`), paints each in order with `0x00550BD0`, then re-sorts them by `+0x130` bit 1.
- `0x00550BD0(place, ctx)` sets the place's marker pieces from its flags: a place with `+0x130` bit 2 or `+0x54` bit 16
  pulses `64 x sin(frame x pi / 30) + 128` (`0x0208F570`), bit 3 dims it to `0x40`, and `+0x54` bits 0, 2, 4, 5 and 17
  pick the frames shown; it places them with `0x00562190` (`0x00562850`, through the map view `+0x80`).
- `0x00554A60(list)` eases each place's two scales `+0x138` and `+0x13A` by `0x400` a frame toward `0x4000`, or toward
  `0x2666`/`0x3666` (`0x3CCC`/`0x2CCC` when the language test `0x00254A10` is true) for a place with `+0x130` bit 1;
  a place with `+0x54` bit 16 is held at `0x4000`.
- `0x00554EA0` draws the place names in the same order (`0x002D8650`), re-measuring a name (`0x0029CD00`) when its scale
  changes and anchoring it by `0x002718C0`.
- `0x00551130(x, y, list, find, id)` returns the place whose `+0x39` is `id` (or the first with `+0x54` bit 0) and its
  position less half the screen (`0x01E0C1D8`, `0x01E0C1DC`), passed through `0x005552A0`.

### World Map routes and panes

- `0x005551F0` draws the routes: `0x005520F0` sets the line state (`0x00562E30`) and `0x00562A30` draws each route of the list
  linked through `+0x1A8` as a ribbon of `w_line01` (`0x00563360` sets the blend state). `0x005621A0` draws a moving dashed
  stretch along a curve (`0x00270420`, `0x00270260`), its colour pulsing by `sin`.
- `0x00553DD0` builds the four corner arrows at `+0x9F58` (0x30 bytes each; `0x00562080` resets one) from the atlas
  `+0x108` `+0x48`, and `0x00553BB0` draws them at the screen edges below the menu bars (`0x002C9430(0x80)`) through
  `0x00561F90`, which blends each arrow's two colours by its level `+0x24`; `0x00561F60` steps the level by `+0x26`
  toward 256 or 0.
- `0x00562120`, `0x005620A0` and `0x00550FB0` move the view: they lerp the centre `+0x10` toward a target (`0x00275490`), and
  `0x00550FB0` precomputes 16 points of a three-point path (`0x00275490`, or the curve `0x00270260` when the path bends).
- `0x00562920` hides the nine pieces of the map view `+0x80`, and `0x00563080` frees the view's resources (`0x003697F0`,
  `0x0024A680`).

The location list pane `0x005542D0` uses row painters installed at `+0x120` of its list:

- `0x005516A0` (installed by `0x00551D80` with row type 3) picks by the type at `+0x10` between `0x00551610` (type 0), its
  own code (type 1) and `0x00552050` (type 3); each sets the row's icon frame, label and arrow, and hides the row when
  its alpha is 0. `0x005511F0` hides an empty row's three nodes.
- `0x00551C20` copies the chosen row out, and `0x00551CD0(rect, mode)` gives the pane's rectangle for mode 0 or 1.
- `0x0057E030` appends a node to a list (`0x00550954`); `0x0057E070` and `0x0057E2F0` clear 0x28- and 0x38-byte records.
- `0x0057E190` moves a cursor between nodes by the direction bits `0x80`, `0x20`, `0x10` and `0x40`; `0x0057E090` gives the
  scroll that keeps the cursor 8 units inside a box, an eighth of the distance per frame; `0x0057E210` draws the cursor
  (`0x00368360`).

### Lifetimes

| Object | Created | Released |
|---|---|---|
| overlay container `0x0209E5C0` | `0x002B6350` from the arbiter | `0x002B6260` sets bit 3; the container releases itself once both pages are gone (`0x002B7590`, continuation `0x002B7540`) |
| overlay page while the HUD is off | the HUD switch `0x00251F40` hides the current page (`0x002B6140`: bit 1 off through `0x00247870`, then `0x002B6260`) | `0x002B61B0` sets bit 1 again |
| location container `0x0209E5F0` | `0x002B9D30` | `0x002B9B30`; continuation `0x002BA6B0` |
| field-time container `0x02B47760` | `0x003CB440` | `0x003CB410`, from `0x00253A30`, `0x00282122`, `0x0028E7A3` and `0x002BA080` |
| World Map host `0x02CA8F38` | `0x00550400` | continuation `0x00552230`, which returns to the menu (`0x002814E0(0x418)`) |
| map-data widget `0x02B457E0` | the first of its three creators | the field-time container (`0x003CB91C`), the World Map host (`0x005525CB`) or the location container (`0x002BADCD`) |
| minimap `0x02B476B0` | `0x003C80C0` | `0x003C58B0`, `0x003C8070` |

## Shipped data

| | |
|---|---|
| guide table in `menumap_common.bin` (`us`) | 77 entries, story counter thresholds 0 to 6,150; every entry selects `menumap_guide00.bin` |
| "???" sites | 6 places in the code load `0x3EC` |

## Modding notes

- An area's map item is listed in `menumap_area.bin`; owning it reveals the area's points without visiting them.
- A World Map destination disappears once the story counter reaches its word `+8`; `0xFFFF` keeps it forever.
- The overlay cannot open before story counter 16 (`0x00253DDA`).
- The minimap's picture is the zone pack's own image, not a menu file.

## Related

- [Menus](menus.md) - the requests that open the maps.
- [Story flags](../Story-Events-And-Hunts/story-flags.md) - the gates the map elements read.
- [Story progress](../Story-Events-And-Hunts/story-progress.md) - the story counter.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md) - the zone pictures and placements.
- [Controls](../Controls-And-Input/controls.md) - the input words.
