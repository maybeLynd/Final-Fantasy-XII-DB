---
title: "Map screens: the World Map, the location map, the map overlay and the minimap, and the map data and story flags they read"
kind: "system"
category: "Menus and HUD"
addresses: "00253C70, 002B6350, 002B9D30, 003BC450, 003BC2D0, 003C18A0, 003C5910, 003C4070"
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
| World Map | `menu_command.bin` `4B7`<sub>h</sub>, help `CCA`<sub>h</sub> | main-menu entry `00281C36` |
| location map | the phrase in `CCA`<sub>h</sub>; opened by the control "Display Map" (`589`<sub>h</sub>) | menu request `21`<sub>h</sub> ([Menus](menus.md)) |
| map overlay | toggled by the control "Map Transparency" (`586`<sub>h</sub>); its layout keys are `TrackMap*` | `002B6220` |
| minimap | the script verbs `shownavimap`, `hidenavimap`, `setnavimapindex` and others | widget `003C5910` |

The two controls are rows 28 and 25 of the Controls screen (`002414B0`; [Control remapping](../Controls-And-Input/control-remapping.md)).

### Opening from the field

The input arbiter `00253C70` keeps the map state in `02092750`:

1. Map Transparency toggles the state between 0 and 3 and remembers it in `0209E5B0` (`00253E2F`-`00253E63`).
2. State 3 opens the map overlay with `002B6220(1)` (`00253DE2`) when the field-time container is ready (`003CB3E0`),
   `02092754` is 0, the field has a map record (`003BFDF0`) and the story counter is at least 16
   (`00253DD1`-`00253DDA`).
3. Display Map closes the overlay and posts menu request `21`<sub>h</sub>, the location map (`00253EA4`-`00253EF2`). Leaving
   the location map restores the overlay as it was (`002BBA2F`-`002BBA3C`).
4. While the state is not 3, the overlay is closed every frame (`002B6260`, `00253C92`).

The location map also opens from `0028E630`, `0028E660` and `0028E690`, and the World Map host `00550400` from
`0028E690` and `0028E790` ([Menus](menus.md)).

### The two-page container

The overlay and the location map each have a container of `179E0`<sub>h</sub> bytes, at `0209E5C0` (`002B6350`, procedure
`002B7590`) and `0209E5F0` (`002B9D30`, procedure `002BA700`). Each holds two `BC08`<sub>h</sub>-byte pages in place, at `+1B0`<sub>h</sub>
and `+BDC0`<sub>h</sub>, and flips between them:

1. The first call creates the container with no page (`002B638F`-`002B63D7`).
2. A container message `20`<sub>h</sub> sets its open request, bit 7 of `+179D2`<sub>h</sub>.
3. The next frame's step builds a page in the other slot (`00245000`, `002B6474`), flips bit 2, attaches the page
   and sends it `21`<sub>h</sub> (`002B6526`-`002B6541`).

A page posts messages to every ancestor up to the root through `00275440`, which follows the parent link `+10`<sub>h</sub>
that `00244960` sets; its container acts on `2B`<sub>h</sub> when it has opened and `1F`<sub>h</sub> when it is cancelled. The page procedures `002B7B80` and `002BAF80` answer
the same 17 messages through their tables at `198EB0`<sub>h</sub> and `19C28C`<sub>h</sub> from the image base.

`002B6220` also copies the field-time container's resources into the overlay's `+190`<sub>h</sub> and sends it `10`<sub>h</sub> and
`20`<sub>h</sub> (`002B6570`).

### The field-time container

`02B47760` (`003CB440`, procedure `003CB650`) draws nothing. It holds the map resources, the map-data widget and a
preload child `003CB4F0` that fills the map cache, and its bit 7 marks the preload as finished (`003CB551`-`003CB55F`),
which the overlay waits for. It is created from `00253A30` and the HUD-on step `00251F40`, and destroyed by
`003CB410`.

### Map resources

`00404060` loads the 32-byte record every page reads at `+130`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32[2]` | back | LocaBack_c.tm2 (kind 7 `BA`<sub>h</sub>) |
| `08`<sub>h</sub> | `u32[2]` | atlas | Loca_8_c.tm2 (`B9`<sub>h</sub>) |
| `10`<sub>h</sub> | `u32[2]` | line | w_line01.tm2 (`B0`<sub>h</sub>), the texture of the page's line quad |
| `18`<sub>h</sub> | `u32[2]` | mrp | Loca.mrp (`BF`<sub>h</sub>) |

### The map-data widget

`003BC450(world, location, owner)` creates the widget `02B457E0` once (`003BC463`), and `003BC2D0` loads:

| File (kind 7) | When |
|---|---|
| `menumap_world.bin` (`A2`<sub>h</sub>) | `world` is set: only the World Map (`003BC440`, `005505E4`) |
| `menumap_location.bin` (`A3`<sub>h</sub>) | `location` is set: all three creators |
| `menumap_common.bin` (`A4`<sub>h</sub>) | always |

The location container (`002BA15C`) and the field-time container (`003CB4CC`) pass `(0, 1)`. `003C1DF0` then picks the
last entry of the guide table in `menumap_common.bin` whose story counter and story gate pass (`003BD950`) and loads
`menumap_guideNN.bin` (kind 7 `496`<sub>h</sub> + the entry's byte `+4`). `menumap_area.bin` (`A5`<sub>h</sub>) is loaded separately into
`020927D0` (`00253780`).

### What a page draws

Each frame, a page rebuilds its element list (`00402A40`) and draws (`002B8A19`-`002B8B11`):

1. one quad textured with `w_line01.tm2` (`00404230`);
2. the line elements (`004043B0`), pulsing the marked ones;
3. one marker per point, each a small map view through `003C4070` in mode 2 (`00404120`, `002B96E7`);
4. the labels (`004044D0`).

### Zoom and panning

A page keeps its zoom in percent at `+D4`<sub>h</sub> and its scroll at `+C8`<sub>h</sub>/`+CC`<sub>h</sub>:

1. The overlay page starts at `TrackMapScale` (200, `002B806C`) through `002B7210` and `002B6AE0`.
2. `002B6AE0(page, zoom)` changes the zoom and keeps the view centre still: `002B69B0` scales the centre's distance
   from the scroll by the new zoom, rounding to the nearest unit.
3. Each frame `002B66E0` keeps the tracked point at `+BBD8`<sub>h</sub>, placed at the current zoom (`00403550`), inside a box
   of 32 units either side of the view centre. It moves the scroll a sixth of the way per call, at least 1 unit,
   within the bounds `+F8`<sub>h</sub>-`+104`<sub>h</sub>, and centres an axis whose bounds cross (`002B6865`-`002B6923`).

`002B6950(out, w, h, mw, mh)` gives a page's margins: 24 units, or the half difference when the map is smaller than
the view. `002B6B50` gives the icon scale from the display aspect (`0017FFD0`) and the floats `01E0CE50`, `01E0CE58`
and `01E0CE5C`, 1.5 for an aspect below one third.

### Points, lists and the legend

`002B7460(page)` lists the page's points: `003BE3A0` fills up to `480`<sub>h</sub> bytes of rows for the map `+138`<sub>h</sub> in the
mode `+BBE0`<sub>h</sub>, each marked with bit 15 when the page's `+13A`<sub>h</sub> bit 3 is set, and `00402D20` turns them into the
element list `+BBC0`<sub>h</sub>; mode 6 also runs `00402BF0`. `002B9A20` draws each element of a list through `002B8EE0`,
passing the highlight to the selected one.

A point's name comes from `002B9C70` by its kind byte `+0D`<sub>h</sub>:

| Kind | Name |
|---:|---|
| `1` | the area name `00377B60` ([area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)) |
| `2` | an NPC name, `0026DEA0` with the Bank2048 bit (`0032A930`) ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `3` | a shop's name, through the shop's name id `002FAE40` |
| `4` | the text id itself |
| other | the legend label of its icon `+08`<sub>h</sub> |

The legend is the 14 pairs of icon frame and text id `187F`<sub>h</sub>-`188C`<sub>h</sub> at `00916A10`. The location map's legend
pane `002BC310` paints each row with `002BA650`, and the point list pane `002BA310` sizes itself to the widest name
(`002BA530`, measured with `0029CD00`) and paints each row with `002BD8C0`: the name and an icon, from the shared atlas
(`0035D460`) for icons below `13`<sub>h</sub> and from the page's own atlas for the rest. `002B6310(location)` returns the area
of a sub-location's persistence group (`003C02B0`, `003BF6C0`;
[menu map files](../Game-Files-And-Data-Tables/menu-map-files.md)).

The point list pane takes its rows from the sub-location icons of the page's sloc block (`003BE2D0` of the page's
`+1C`<sub>h</sub>), through `00402000(rows, page)` (`002BA347`, `002BA3A2`):

1. it walks kinds 3 to 8 with `003DFBB0` and `003DFB50`, keeping the entries `003FFF40` accepts;
2. unless the page's `+28`<sub>h</sub> bit 9 is set, it skips an icon other than `14`<sub>h</sub>, `17`<sub>h</sub> and `18`<sub>h</sub> whose 16-unit cell is
   not visited (`00255150`), on the visit mask that `00403F90` copies from `002551B0` (all `FF`<sub>h</sub> when there is none or
   `+28`<sub>h</sub> bit 15 is set; the buffer of `003C4AE0` when bit 0 is set);
3. an icon `0E`<sub>h</sub> adds no row: its entry number goes to `+C`<sub>h</sub> of the row before it;
4. each other entry adds a `18`<sub>h</sub>-byte row {entry, kind `+8`, entry number `+A`<sub>h</sub>, `FFFF`<sub>h</sub> at `+C`<sub>h</sub>}, and the count is
   returned (a null `rows` only counts).

`004022F0(sloc, icon)` returns 1 when any icon of kinds 3 to 8 equals `icon`, treating `14`<sub>h</sub>, `17`<sub>h</sub> and `18`<sub>h</sub> as one
icon (`003BCBA0`, `003BCC46`). `00402250(x, y, page, kind, i)` returns the `at` position (`+4`, `+6`) of one sloc entry.

### Page element helpers

The element list of a map page is linked through `+60`<sub>h</sub>. The two page procedures (`002B7B80`, `002BAF80`) share these
helpers:

- `004026B0(list, id)` finds the element whose byte `+1` is `id`; `00402200` the first with `+28`<sub>h</sub> bit 5;
  `00402230` the first with bit 0, or the head.
- `00402DB0(element, buttons)` moves the cursor (`002BBBD4`): bits `10`<sub>h</sub>, `40`<sub>h</sub>, `80`<sub>h</sub> and `20`<sub>h</sub> take the
  element named by bytes `+8`, `+9`, `+A`<sub>h</sub> and `+B`<sub>h</sub>, and the element stays put when that id is `-1` or absent.
- `004023D0(lines, line)` returns 1 when the line list (linked through `+98`<sub>h</sub>) already holds a line with the same
  two ids (`+80`<sub>h</sub>, `+82`<sub>h</sub>) and the same two end points (`+84`<sub>h</sub>/`+86`<sub>h</sub>, `+8C`<sub>h</sub>/`+8E`<sub>h</sub>), each pair in either
  order; the element-list rebuild `00402A40` asks it before adding a line (`00402B25`).
- `00403130(list, zoom)` sets the size `+34`<sub>h</sub>/`+36`<sub>h</sub> of every element of type 1 (byte `+2`) to its base
  `+48`<sub>h</sub>/`+4A`<sub>h</sub> divided by the zoom.
- `00403180(list, selected)` animates each element per frame: `+4C`<sub>h</sub> steps by 16 toward `80`<sub>h</sub> (`40`<sub>h</sub> with `+4E`<sub>h</sub>
  bit 1) while `+4E`<sub>h</sub> bit 0 is set and down otherwise; the scale `+38`<sub>h</sub> grows by 0.05625 (0.046875 when the
  language test `00254A10` is true) to 1.0, or shrinks to 0.9 (0.75) with `+4E`<sub>h</sub> bit 2; the highlight `+50`<sub>h</sub> rises by
  16 to 256 on the selected element and falls by 16 to 0 on the others.
- `00402F00(list, w, h)` copies the first bit-0 element's rectangle `+20`<sub>h</sub>-`+26`<sub>h</sub> to `+30`<sub>h</sub>-`+36`<sub>h</sub> and, while
  `00264790()` is below 1, projects the party leader (`0035D320`, `003588B0`, `00265020`) through the minimap view
  (`003C3F90`, `00202B70`) and shifts the element by how far the leader falls outside a `w` by `h` box.
- `00402610(item, src)` stores `00275320` of the item's current values at `+0`, copies `src`'s rectangle
  `+30`<sub>h</sub>-`+36`<sub>h</sub> to `+8` and clears `+10`<sub>h</sub>; `004026D0(out, src)` copies the same rectangle twice; `004022D0` sets
  a rectangle to {0, 8, 8, 8, 8, `100`<sub>h</sub>}.
- `00403330(fade)` raises `+10`<sub>h</sub> by a sixth of its distance to 256, at least 6, and returns true at 256.
- `00403600(out, sprite)` and `00403F00` (pane `002BC9C0`) size and draw a sprite 1.75 times its height
  (`002D8C80`).
- `004041D0(slots)` releases three child widgets (`0024A680(w, 1)`) and the buffer in the fourth slot (`003697F0`), for
  the location container (`002BADD9`) and the field-time container (`003CB931`).

The location map's caption pane `[02B62D78]` (created by `00402680`, procedure `00403380`) carries an icon and three
labels. `00402490(texts)` sets the labels from the text ids at `+8`, `+10`<sub>h</sub> and `+18`<sub>h</sub> of its argument (`-1` keeps a
label; `-1` at `+10`<sub>h</sub> hides the second), measures the first with `0029CD00` to place the rest, and a non-negative
`+0` picks the row of the fourth child. `00402730(atlas, group, frame)` sets the icon and moves the second label past its
width.

`002BA1B0(v)` gives the location container a y from the menu bars: the screen height `01E0C1DC`, less
`002C9430(81h)` when `002C9430(80h) + v` is not 0. `002BA1F0` is the location map's exit callback: when the location container `0209E5F0` is gone
and `00402220` answers 0, it returns to the menu with `002814E0(417h)`.

### What is shown

The story gate `0032A8A0` ([Story flags](../Story-Events-And-Hunts/story-flags.md)) and the encoded-id query
`00309EC0` decide every map element:

| Element | Shown when |
|---|---|
| area point (`003C18A0`) | its gate (word `+E`<sub>h</sub>) passes and the area is current, visited or its map is owned (`003BCBA0`) |
| link point (`003C0F70`) | its gate `+16`<sub>h</sub> passes, and its map is owned, or its gate `+12`<sub>h</sub> is `FFFF`<sub>h</sub> or set |
| label (`003C2320`) | revealed; otherwise "???" (`3EC`<sub>h</sub>, `003C25B1`) |
| location (`003C12B0`) | its kind's gate passes and its map is owned, or one of its points can be drawn |
| World Map destination (`003C08B0`) | its gates pass and the story counter (`00265270`) is below its word `+8` |
| icon of a sub-location (`003DFB50`, `003FFF40`, `00400CF0`) | its word `+A`<sub>h</sub> is 0, or its gate passes; 1 never shows |

`003BCBA0` builds the state an area point reads: the current area (`003C1070`), a visit byte at
`[020927C0] + 224h + 32 x entry` (`00255200`), and the area's map as a key item of class `8000`<sub>h</sub> (`002543F0`; the
map list is `menumap_area.bin` `+C`<sub>h</sub>).

### The minimap

The minimap is the widget `003C5910`, at `02B476B0` (`003C80C0`):

1. `003C5E00` shows it, from the HUD-on step and the verb `shownavimap` (`00352390`), and `003C58B0` hides it.
2. Every world tick, `003C6000` keeps it in step while the save-RAM status allows it (`00377750`) and copies the party
   position to `02B45810` (`00359150`).
3. Its draw callback `003C32B0` calls `003C4070` in mode 0, which draws the zone's own map picture `[02B457F0]` at 4
   pixels per world unit (`004001D0`), a 12-spoke ring (`003C34E0`), the blinking party marker (`003C2E60`) and up to
   64 icons (`003C3340`, `00400CF0`).
4. While the map is jammed (`00377780`, verb `setnavimapjamming`), `004001D0` draws its jamming passes over the
   picture (`00401620`, `004014E0`, `004010A0`) and `003C4070` leaves out the ring, the party marker and the icons.

The picture comes from the zone's map pack: `003C63A0` registers it and `00379870` places it, chosen by
`setnavimapindex` (`00377400`) ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

### Minimap markers

`003C5130` rebuilds the minimap's marker list: one 32-byte entry per actor at `02B45A80` (count `02B45A70`), then the
navigation icons (`00400550`), then `004000E0` merges them into the live list at `02B46280`:

1. every live node gets `+20`<sub>h</sub> bit 1 (stale);
2. `00400AC0(entry, list, i)` handles entry `i`. Unless the entry's bit 18 is set, the actor `003588B0(+4)` must
   exist, and its state `00234D40` of 2 hides a node it already has (`+20`<sub>h</sub> bit 2).
3. A node with the same id is moved to position `i` (`00400650` unlinks it); a new id takes the next free node of
   64 (`50`<sub>h</sub> bytes each from `+10`<sub>h</sub>, ring index `+1411`<sub>h</sub>, count `+1412`<sub>h</sub>), zeroed, with `+22`<sub>h</sub> = `80`<sub>h</sub> and
   the scale `+24`<sub>h</sub> = 1.0 only before the list's first fill.
4. The 32 bytes are copied in and the stale bit cleared. After the pass every node still stale and not hidden loses
   its live bit 0, and `+1410`<sub>h</sub> bit 0 records the first fill.

The draw `003C6B70` scales each marker's colour by `+22`<sub>h</sub> (`80`<sub>h</sub> is full) and its size by `+24`<sub>h</sub>. It finds the
sprite with `00400420(out, entry)`: kinds 5 to 7 use the entry's byte `+1`; other kinds look up the byte table
`00D120E0` by kind, plus 6 when bit 19 is set, in the shared atlas `0035D460`.

### The World Map host

The World Map host `[02CA8F38]` (`00550400`) keeps its state in the word `+170`<sub>h</sub>. `00550510(v)` stores `v` in bit 3
(`0028E72A`, `0028E7EE`). `00550610()` re-attaches the host to the root `[0208EA20]` and its screen `+160`<sub>h</sub> to
`[0208EA28]` (`00246AD0`) when bits 0 and 2 are both set, clearing bit 1; otherwise it sets bit 1 (`0028E770`,
`0028E81A`).

### World Map places

The view `005528C0` keeps its places in a list linked through `+140`<sub>h</sub>; each place has its screen position at
`+3C`<sub>h</sub>/`+3E`<sub>h</sub> and its flags at `+130`<sub>h</sub> and `+54`<sub>h</sub>.

- `00554BD0` sorts the places into a tree through `+150`<sub>h</sub>-`+160`<sub>h</sub> by a key at `+168`<sub>h</sub> (0 or 1.0, from the byte
  `+3B`<sub>h</sub> and the word `+3E`<sub>h</sub>), paints each in order with `00550BD0`, then re-sorts them by `+130`<sub>h</sub> bit 1.
- `00550BD0(place, ctx)` sets the place's marker pieces from its flags: a place with `+130`<sub>h</sub> bit 2 or `+54`<sub>h</sub> bit 16
  pulses `64 x sin(frame x pi / 30) + 128` (`0208F570`), bit 3 dims it to `40`<sub>h</sub>, and `+54`<sub>h</sub> bits 0, 2, 4, 5 and 17
  pick the frames shown; it places them with `00562190` (`00562850`, through the map view `+80`<sub>h</sub>).
- `00554A60(list)` eases each place's two scales `+138`<sub>h</sub> and `+13A`<sub>h</sub> by `400`<sub>h</sub> a frame toward `4000`<sub>h</sub>, or toward
  `2666`<sub>h</sub>/`3666`<sub>h</sub> (`3CCC`<sub>h</sub>/`2CCC`<sub>h</sub> when the language test `00254A10` is true) for a place with `+130`<sub>h</sub> bit 1;
  a place with `+54`<sub>h</sub> bit 16 is held at `4000`<sub>h</sub>.
- `00554EA0` draws the place names in the same order (`002D8650`), re-measuring a name (`0029CD00`) when its scale
  changes and anchoring it by `002718C0`.
- `00551130(x, y, list, find, id)` returns the place whose `+39`<sub>h</sub> is `id` (or the first with `+54`<sub>h</sub> bit 0) and its
  position less half the screen (`01E0C1D8`, `01E0C1DC`), passed through `005552A0`.

### World Map routes and panes

- `005551F0` draws the routes: `005520F0` sets the line state (`00562E30`) and `00562A30` draws each route of the list
  linked through `+1A8`<sub>h</sub> as a ribbon of `w_line01` (`00563360` sets the blend state). `005621A0` draws a moving dashed
  stretch along a curve (`00270420`, `00270260`), its colour pulsing by `sin`.
- `00553DD0` builds the four corner arrows at `+9F58`<sub>h</sub> (`30`<sub>h</sub> bytes each; `00562080` resets one) from the atlas
  `+108`<sub>h</sub> `+48`<sub>h</sub>, and `00553BB0` draws them at the screen edges below the menu bars (`002C9430(80h)`) through
  `00561F90`, which blends each arrow's two colours by its level `+24`<sub>h</sub>; `00561F60` steps the level by `+26`<sub>h</sub>
  toward 256 or 0.
- `00562120`, `005620A0` and `00550FB0` move the view: they lerp the centre `+10`<sub>h</sub> toward a target (`00275490`), and
  `00550FB0` precomputes 16 points of a three-point path (`00275490`, or the curve `00270260` when the path bends).
- `00562920` hides the nine pieces of the map view `+80`<sub>h</sub>, and `00563080` frees the view's resources (`003697F0`,
  `0024A680`).

The location list pane `005542D0` uses row painters installed at `+120`<sub>h</sub> of its list:

- `005516A0` (installed by `00551D80` with row type 3) picks by the type at `+10`<sub>h</sub> between `00551610` (type 0), its
  own code (type 1) and `00552050` (type 3); each sets the row's icon frame, label and arrow, and hides the row when
  its alpha is 0. `005511F0` hides an empty row's three nodes.
- `00551C20` copies the chosen row out, and `00551CD0(rect, mode)` gives the pane's rectangle for mode 0 or 1.
- `0057E030` appends a node to a list (`00550954`); `0057E070` and `0057E2F0` clear `28`<sub>h</sub>- and `38`<sub>h</sub>-byte records.
- `0057E190` moves a cursor between nodes by the direction bits `80`<sub>h</sub>, `20`<sub>h</sub>, `10`<sub>h</sub> and `40`<sub>h</sub>; `0057E090` gives the
  scroll that keeps the cursor 8 units inside a box, an eighth of the distance per frame; `0057E210` draws the cursor
  (`00368360`).

### Lifetimes

| Object | Created | Released |
|---|---|---|
| overlay container `0209E5C0` | `002B6350` from the arbiter | `002B6260` sets bit 3; the container releases itself once both pages are gone (`002B7590`, continuation `002B7540`) |
| overlay page while the HUD is off | the HUD switch `00251F40` hides the current page (`002B6140`: bit 1 off through `00247870`, then `002B6260`) | `002B61B0` sets bit 1 again |
| location container `0209E5F0` | `002B9D30` | `002B9B30`; continuation `002BA6B0` |
| field-time container `02B47760` | `003CB440` | `003CB410`, from `00253A30`, `00282122`, `0028E7A3` and `002BA080` |
| World Map host `02CA8F38` | `00550400` | continuation `00552230`, which returns to the menu (`002814E0(418h)`) |
| map-data widget `02B457E0` | the first of its three creators | the field-time container (`003CB91C`), the World Map host (`005525CB`) or the location container (`002BADCD`) |
| minimap `02B476B0` | `003C80C0` | `003C58B0`, `003C8070` |

## Shipped data

| | |
|---|---|
| guide table in `menumap_common.bin` (`us`) | 77 entries, story counter thresholds 0 to 6,150; every entry selects `menumap_guide00.bin` |
| "???" sites | 6 places in the code load `3EC`<sub>h</sub> |

## Modding notes

- An area's map item is listed in `menumap_area.bin`; owning it reveals the area's points without visiting them.
- A World Map destination disappears once the story counter reaches its word `+8`; `FFFF`<sub>h</sub> keeps it forever.
- The overlay cannot open before story counter 16 (`00253DDA`).
- The minimap's picture is the zone pack's own image, not a menu file.

## Related

- [Menus](menus.md) - the requests that open the maps.
- [Story flags](../Story-Events-And-Hunts/story-flags.md) - the gates the map elements read.
- [Story progress](../Story-Events-And-Hunts/story-progress.md) - the story counter.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md) - the zone pictures and placements.
- [Controls](../Controls-And-Input/controls.md) - the input words.
