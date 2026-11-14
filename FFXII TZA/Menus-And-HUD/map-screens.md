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

The map screens draw from the `menumap` files: `menumap_world.bin` for the World Map, `menumap_location.bin` for the
location maps and `menumap_common.bin` for both. Whether a place, link or name shows is decided by story flags, the
visit record kept for each area, and whether the party owns that area's map.

## How it works

### Names

| Map | Shipped text | Code |
|---|---|---|
| World Map | `menu_command.bin` `0x4B7`, help `0xCCA` | main-menu entry `0x00281C36` |
| location map | the phrase in `0xCCA`; opened by the control "Display Map" (`0x589`) | menu request 2 with parameter `0x21` ([Menus](menus.md)) |
| map overlay | toggled by the control "Map Transparency" (`0x586`); its layout keys are `TrackMap*` | `0x002B6220` |
| minimap | shown by the script verbs `shownavimap` (`0x00352390`) and `shownavimapfast` (`0x00352AD0`), hidden by `hidenavimap` (`0x003527D0`) and `hidenavimapfast` (`0x00352E20`); `setnavimapindex` (`0x00356BF0`) picks its picture | widget `0x003C5910` |

The two controls are rows 28 and 25 of the Controls screen (`0x002414B0`; [Control remapping](../Controls-And-Input/control-remapping.md)).

### Opening from the field

The input arbiter `0x00253C70` keeps the map state in `0x02092750`:

1. Map Transparency toggles the state between 0 and 3 and remembers it in `0x0209E5B0` (`0x00253E2F`-`0x00253E63`).
   Each toggle also sets `0x0209E5B4` to 1 (`0x00253E45`, `0x00253E5D`). On a later frame, when `0x001EDE70` answers
   non-zero, the arbiter clears it and skips the Map Transparency and Display Map press tests for that frame
   (`0x00253D82`-`0x00253D98`, past `0x00253DEC`-`0x00253E9A`); while `0x001EDE70` answers 0 it stays set and the tests run.
2. State 3 opens the map overlay with `0x002B6220(1)` (`0x00253DE2`) when the field-time container is ready (`0x003CB3E0`),
   `0x02092754` is 0, the field has a map record (`0x003BFDF0`) and the story counter is at least 16
   (`0x00253DD1`-`0x00253DDA`).
3. Display Map closes the overlay and posts menu request 2 with parameter `0x21`, the location map
   (`0x00253EA4`-`0x00253EF2`, `0x002E1B10` at `0x00253EE6`). Leaving the location map restores the overlay as it was
   (`0x002BBA2F`-`0x002BBA3C`). The arbiter's other post of request 2 (`0x00253F01`-`0x00253F58`) also sends `0x21` until
   story flag `0x5E` is set (`0x00253F21`); then it sends `0x00264640(2)`, or 1 when that is 0 ([Menus](menus.md)).
4. While the state is not 3, the overlay is closed every frame (`0x002B6260`, `0x00253C92`).

The location map also opens from `0x0028E630`, `0x0028E660` and `0x0028E690`, and the World Map host `0x00550400` from
`0x0028E690` and `0x0028E790` ([Menus](menus.md)).

### The two-page container

The overlay and the location map each have a container of 0x179E0 bytes, at `0x0209E5C0` (`0x002B6350`, procedure
`0x002B7590`) and `0x0209E5F0` (`0x002B9D30`, procedure `0x002BA700`). Each holds two 0xBC08-byte pages in place, at `+0x1B0`
and `+0xBDC0`, and flips between them:

1. The first call creates the container with no page (`0x002B638F`-`0x002B63D7`). `0x002B6350(a, b)` keeps a at
   `+0x179DA` and returns the address of the page slot that bit `0x4` does not name (`0x002B63AF`-`0x002B63D7`).
2. A container message `0x20` sets its open request, bit `0x80` of `+0x179D2`.
3. The next frame's step builds a page in the other slot (`0x00245000`, `0x002B6474`), flips bit `0x4`, attaches the page
   and sends it `0x21` (`0x002B6526`-`0x002B6541`).
4. That build is `0x002B6350` again, which the step calls with the container's word `+0x179D0` and byte `+0x179D8`
   while bit `0x200` is clear, clearing the request on a non-null answer (`0x002B77DB`-`0x002B77FD`). It answers 0 while
   the other slot still holds a page (`0x00273A20`, `0x002B640E`-`0x002B6415`).
5. The page has the procedure `0x002B7B80` and a create record of 0, a and the low 32 bits of the container + `0x190`,
   sign-extended (`0x002B63DC`-`0x002B63F1`, `0x002B6427`). Its `+0xBBF0` is the container, which then gets message
   `0x29` (`0x002B6483`-`0x002B64B0`).
6. The page's `+0xBBEE` takes `[0x01E0C1DC]` (`0x1C0`), `+0xBBE0` takes b and `+0xBBE2` the container's old
   `+0x179DA`, which then takes a (`0x002B64B9`-`0x002B6513`). `0x00244960` attaches the page (`0x002B651B`), and the call
   returns it.

The location map's builder `0x002B9D30` does the same with four differences: the page procedure is `0x002BAF80`
(`0x002B9E0C`); `+0xBBEE` takes `[0x01E0C1DC]` less `0x002C9430(0x81)` when `0x002C9430(0x80)` plus the container's
answer to message `0x29` (0 when the container or its procedure is null) is not 0 (`0x002B9E80`-`0x002B9EC6`);
`+0x48` takes the `0x28`-byte descriptor at `0x00916A70` + 40 x `+0x179D9` (entry 8 for `0xFF`, `0x002B9ED4`-
`0x002B9EFA`); and `+0xBBE0` takes 5 instead of b while the dword `0x02B457D8` is not 0 (`0x002B9F1B`-`0x002B9F33`).

A page posts messages to every ancestor up to the root through `0x00275440`, which follows the parent link `+0x10`
that `0x00244960` sets; its container acts on `0x2B` when it has opened and `0x1F` when it is cancelled. The page procedures `0x002B7B80` and `0x002BAF80` answer
the same 17 messages through their tables at `0x198EB0` and `0x19C28C` from the image base.

`0x002B6220` also copies the field-time container's resources into the overlay's `+0x190` and sends it `0x10` and
`0x20` (`0x002B6570`).

### The field-time container

`0x02B47760` (`0x003CB440`, procedure `0x003CB650`) draws nothing. It holds the map resources, the map-data widget and a
preload child `0x003CB4F0` that fills the map cache, and its bit `0x80` marks the preload as finished (`0x003CB551`-`0x003CB55F`),
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

`0x003BC450(world, location, owner)` creates the widget `0x02B457E0` once (`0x003BC463`) and answers 1; when a widget
already exists it creates no second one and answers 0 (`0x003BC4C5`). On creation `0x003BC2D0` loads:

| File (kind 7) | When |
|---|---|
| `menumap_world.bin` (`0xA2`) | `world` is set: only the World Map (`0x003BC440`, `0x005505E4`) |
| `menumap_location.bin` (`0xA3`) | `location` is set: all three creators |
| `menumap_common.bin` (`0xA4`) | always |

`0x003BC2D0` files the three in heap 2 in one request set (`0x00249580`, closed by a tail jump to `0x00249410` at
`0x003BC3D1`). In the same set it asks for text groups 6 (`menu_mapname`) and `0x17` (`menu01`) when
`0x002F8040` finds them missing (`0x002491B0`), setting bits `0x1` and `0x2` of the widget's `+0xD0`
(`0x003BC37A`-`0x003BC3B3`).

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
mode `+0xBBE0`, each marked with bit `0x8000` when the page's `+0x13A` bit `0x8` is set, and `0x00402D20` turns them into the
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
2. unless the page's `+0x28` bit `0x200` is set, it skips an icon other than `0x14`, `0x17` and `0x18` whose 16-unit cell is
   not visited (`0x00255150`), on the visit mask that `0x00403F90` copies from `0x002551B0` (all `0xFF` when there is no
   visit mask or `+0x28` bit `0x8000` is set; the buffer of `0x003C4AE0` when bit `0x1` is set);
3. an icon `0x0E` adds no row: its entry number goes to `+0xC` of the row before it;
4. each other entry adds a 0x18-byte row {entry, kind `+8`, entry number `+0xA`, `0xFFFF` at `+0xC`}, and the count is
   returned (a null `rows` only counts).

`0x004022F0(sloc, icon)` returns 1 when any icon of kinds 3 to 8 equals `icon`, treating `0x14`, `0x17` and `0x18` as one
icon (`0x003BCBA0`, `0x003BCC46`). `0x00402250(x, y, page, kind, i)` returns the `at` position (`+4`, `+6`) of one sloc entry.

### Page element helpers

The element list of a map page is linked through `+0x60`. The two page procedures (`0x002B7B80`, `0x002BAF80`) share these
helpers:

- `0x004026B0(list, id)` finds the element whose byte `+1` is `id`; `0x00402200` the first with `+0x28` bit `0x20`;
  `0x00402230` the first with bit `0x1`, or the head.
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
- `0x00403180(list, selected)` animates each element per frame: `+0x4C` steps by 16 up to `0x80` (`0x40` with `+0x4E`
  bit `0x2`) while `+0x4E` bit `0x1` is set, and otherwise down to 0 (`0x40` with bit `0x2`). The highlight `+0x50`
  rises by 16 to 256 on the selected element and falls by 16 to 0 on the others.
- The same pass grows each element's scale `+0x38` by 0.05625 (0.046875 when the language test `0x00254A10` is true) to
  1.0, or shrinks it to 0.9 (0.75) with `+0x4E` bit `0x4`.
- While `0x00264790()` is below 1, `0x00402F00(list, w, h)` copies the first bit `0x1` element's rectangle
  `+0x20`-`+0x26` to `+0x30`-`+0x36`, projects the party leader (`0x0035D320`, `0x003588B0`, `0x00265020`) through the
  minimap view (`0x003C3F90`, `0x00202B70`) and shifts the element by how far the leader falls outside a `w` by `h` box.
- `0x00402610(item, src)` stores `0x00275320` of the item's current values at `+0`, copies `src`'s rectangle
  `+0x30`-`+0x36` to `+8` and clears `+0x10`; `0x004026D0(out, src)` copies the same rectangle twice; `0x004022D0` sets
  a rectangle: the words {0, 0, 8, 8} at `+0x00` and again at `+0x08`, and `0x100` at `+0x10` (`0x004022D2`,
  `0x004022DA`, `0x004022DC`, `0x004022E3`).
- `0x00403330(fade)` raises `+0x10` by a sixth of its distance to 256, at least 6, and returns true at 256.
- `0x00403600(out, sprite)` and `0x00403F00` (pane `0x002BC9C0`) size and draw a sprite 1.75 times its height
  (`0x002D8C80`).
- `0x004041D0(slots)` releases three child widgets (`0x0024A680(w, 1)`) and the buffer in the fourth slot (`0x003697F0`), for
  the location container (`0x002BADD9`) and the field-time container (`0x003CB931`).

The location map's caption pane `[0x02B62D78]` (created by `0x00402680`, procedure `0x00403380`) carries an icon and three
labels. `0x00402490(texts)` sets the labels from the text ids at `+8`, `+0x10` and `+0x18` of its argument (`-1` keeps a
label; `-1` at `+0x10` also clears bit `0x1` of node 3, which sits between the first two labels, and any other value
sets it), measures the first with `0x0029CD00` to place the rest, and a non-negative `+0` picks the row of node 1 of the
widget at `+0x18` of node 4. `0x00402730(atlas, group, frame)` sets the icon and moves the second label past its width.

`0x002BA1B0(v)` gives the location container a y from the menu bars: the screen height `0x01E0C1DC`, less
`0x002C9430(0x81)` when `0x002C9430(0x80) + v` is not 0.

`0x002BA1F0` is the location sprite pane's continuation, which the pane's procedure `0x002BC9C0` installs at its
`+0x08` on message 1 (`0x002BCA18`, `0x002BCA1F`): it clears the pane's cell `0x0209E5F8` (`0x002BA1FC`), and when the
location container `0x0209E5F0` is gone and `0x00402220` answers 0, it returns to the menu with `0x002814E0(0x417)`. `0x002BC2C0`, the exit callback `0x002BAF80` installs
(`0x002BB202`), does the same when neither `0x0209E5F0` nor `0x0209E5F8` is set, after `0x00285F00(0x0209E608)`.

### What is shown

The story gate `0x0032A8A0` ([Story flags](../Story-Events-And-Hunts/story-flags.md)) and the encoded-id query
`0x00309EC0` decide every map element:

| Element | Shown when |
|---|---|
| area point (`0x003C18A0`) | its gate (word `+0xE`) passes and the area is current, visited or its map is owned, or one of two more bits of its state is set (`0x003BCBA0`). The gate passes when it is `0xFFFF`; with no bit of `0xFC0` in the point's dword `+0x10` it is the story gate `0x0032A8A0`, otherwise the encoded-id query `0x00309EC0(gate, 0)`, and a failed query still passes when the area is current or visited, state bits `0x401` (`0x003C18BF`-`0x003C1915`). The point then shows when `0x003BCBA0`'s state is non-zero (`0x003C195F`-`0x003C1965`): bit `0x1` the current area, `0x400` visited, `0x2` the encoded-id query passing for a point gated by it and the map owned (`0x002543F0`) for any other, `0x8000` bit `0x800` of the map-data widget's `+0xD0`, and `0x1000` an icon `0x14` (with `0x17` and `0x18`) in the area's sloc block, which also makes an empty state `0x2800` unless that `+0xD0` bit is set or the widget's `+0xCA` is 6 (`0x003BCBC3`-`0x003BCC77`). While `0x02B457D8` is set the gate is skipped, and a point whose area `+0xC` equals `0x0037ED70()` shows (`0x003C1918`-`0x003C193E`); with the widget's `+0xCA` at 6, a `0x0037ED80()` of 1 shows it (`0x003C1945`-`0x003C195D`) |
| link point (`0x003C0F70`) | its gate `+0x16` passes, and its map is owned, or its gate `+0x12` is `0xFFFF` or set |
| label (`0x003C2320`) | revealed; otherwise "???" (`0x3EC`, `0x003C25B1`) |
| location (`0x003C12B0`) | its kind's gate passes and its map is owned, or one of its points can be drawn |
| World Map destination (`0x003C08B0`) | its area entry's region byte `+0xA` is non-zero and the story counter (`0x00265270`) is below its word `+8`, where `0xFFFF` never hides (`0x003C08DD`-`0x003C0930`); then it shows when it is the current area, when the screen mode's own test passes (mode 0 every area, 2 the area gate `+0x14` through `0x003C0B70`, 3 the area's bit at `+0x270`, 4 its map owned through `0x003C0BE0`, 6 `0x003C0A00`), or when one of its persistence groups passes `0x003C0D70(g, 1)` (`0x003C0936`-`0x003C09E4`) |
| icon of a sub-location (`0x003DFB50`, `0x003FFF40`, `0x00400CF0`) | its word `+0xA` is 0, or its gate passes; 1 never shows |

`0x003BCBA0` builds the state an area point reads: bit `0x1` for the current area (`0x003C1070`), bit `0x400` when any of
the 32 saved bytes at `[0x020927C0] + 0x224 + 32 x entry` is non-zero (`0x00255200`), and bit `0x2` when the map is held:
the item in word `+0x0E` of the point when that word is not `0xFFFF` and any of bits `0xFC0` of its `+0x10` is set
(`0x003C06E0`), otherwise the area's map as a key item of class `0x8000` (`0x002543F0`; the map list is `menumap_area.bin`
`+0xC`).

### The minimap

The minimap is the widget `0x003C5910`, at `0x02B476B0` (`0x003C80C0`):

1. `0x003C5E00` shows it and `0x003C58B0` hides it (see [Who shows and hides the minimap](#who-shows-and-hides-the-minimap)).
2. Every world tick, `0x003C6000` keeps it in step while the save-RAM status allows it (`0x00377750`) and copies the party
   position to `0x02B45810` (`0x00359150`).
3. Its draw callback `0x003C32B0` calls `0x003C4070` in mode 0, which draws the zone's own map picture `[0x02B457F0]` at 4
   pixels per world unit (`0x004001D0`), a 12-spoke ring (`0x003C34E0`), the blinking party marker (`0x003C2E60`) and up to
   64 icons (`0x003C3340`, `0x00400CF0`).
4. While the map is jammed (`0x00377780`, verb `setnavimapjamming`), `0x004001D0` draws its jamming passes over the
   picture (`0x00401620`, `0x004014E0`, `0x004010A0`) and `0x003C4070` leaves out the ring, the party marker and the icons.

The parts of that draw:

- `0x003C6140(writer, record)` (`0x003C3595`, from the ring) scales the eight constant bytes `0x01EFE370`-`0x01EFE377` by the
  record's words `+0x5A` (bytes 0-2 and 4-6) and `+0x58` (bytes 3 and 7), each `(byte x word) >> 7`, opens a packet
  (`0x00248EB0(writer)`), moves the writer's cursor `+0x10` on by `0x30` and writes the two colours as four dwords each,
  moving the cursor by `0x10` after each.
- `0x003C7EA0(record, m, r, n, first)` (`0x003C326D`, from the party marker) emits a fan of `n` vertices through
  `0x00181350(v, 1)`: the point (0, 0, 0, 1) through the matrix `m` (`0x00202B70`, `0x00202CA0`) with the record's colour
  bytes `+0x94`-`+0x97`, then n - 1 points in the colour `0x00D116A0` (0, 0, 0, 0x80): the first is `first`, each next
  is the previous through the matrix `r`, and all go through `m`.
- `0x003C2E60` passes `first` = (cos, sin, 0, 1) of the marker's angle times its radius and closes the batch
  (`0x00181330`).
- `0x004006A0(table)` (from `0x004001D0`) draws every triangle of an index table (count the `i16` at `+0x04`, 12-byte
  entries from the pointer at `+0x18`) in packets of at most 24. Each entry's three index pairs become a `0x20`-byte
  row. A packet is drawn when it holds 24 rows (`0x00400705`) or the entries run out (`0x0040070F`), and a new packet is
  opened (`0x004007C7`) while entries remain (`0x004007C3`), so no entry is dropped.
- The packet header is the packet's row count ORed with `0x3025C00000008000` when `0x00377780()` reports the map
  jammed, or `0x302DC00000008000` otherwise, with `0x412` as its second qword (`0x00400721`-`0x0040073B`).
- `0x004001D0` passes the table `0x01E0C590` (`0x0040032C`), whose count is 136 in the executable. No instruction writes
  that count: `0x004006A0` reads it at `0x004006AC`, `0x0040070A` and `0x004007BB`, and `0x004017D0` and `0x00401D40`, which also
  receive the table, read only its `+0x00`, `+0x02`, `+0x08` and `+0x10`. Its triangles are drawn as five packets of 24 and
  one of 16.
- `0x00400870(rows, n)` (`0x004007B6`) builds each triangle's three vertices from the row's index pairs: x and y from the
  float pairs at `0x02B5F2D0`, four ints from the floats at `0x02B5F2A0` and the pair at `0x02B5F820`; it submits them three
  at a time (`0x00181350`).
- `0x004010A0` (the jamming pass) takes two phases from the frame counter `f` at `0x0208F570`, `sinf((f % 60) × π / 60)`
  and `sinf((f % 30) × π / 30)`, modulo 60 and modulo 30 as angles through `0x00861F0E` (`sinf`; `0x00401139`-`0x004011A9`),
  beside a third angle `f × π / 15` of the whole counter (`0x004010C3`-`0x00401130`). It then fills the vertex scratch
  `0x02B5FD70` with `0x004019F0` (`0x00401353`) and submits it with `0x004009C0` (`0x00401478`).
- `0x004019F0(points, n, m, q, ..., scaleX, scaleY, picture)` sets a block up from `m` and `q` (`0x00202D70`) and writes
  two scratch vertices per `0x30`-byte point at `0x02B5FD70 + 0x30 x [0x02B62D70]`, counting it up: x - 640 and x + 640
  (`0x008C5A98`) with the point's `+0x24`, transformed by the block (`0x00202B70`, `0x00202CA0`).
- Each of those vertices carries the colour bytes `0x80`, `0x80`, `0x80` with the alpha from argument 7's `+0x58`, and
  texture coordinates from the picture's words `+0x14`, `+0x16` times `scaleX`, `scaleY`.
- `0x004009C0()` hands the 256 scratch vertices to the batcher as a strip (`0x00181460(0x02B5FD70, 256)`), then for every
  six vertices up to 250 appends vertices 0 and 1, then 4, 1, 4 and 5 one at a time (`0x00181350`), and resets
  `0x02B62D70` to 0.

The ring takes its entry count from `0x00264AC0(list)` (`0x003C350B`), the first dword of that per-class table of the zone
script's image (header `+0x70`, `0x00264AE0`), and gets a 6-byte style for each entry from `0x002648F0(entry, out)`
(`0x003C35D5`, `0x003C36BA`):

- the defaults are bytes 1, 1, 1, 1 and the word `0xFFFF`;
- for an entry, `0x00264920` refills them from record `+0x1D` of the image's table at header `+0x8C` (`0x00264870`):
  the story-flag gate `0x0032A8A0` of its words 0, 1, a mode word (4 on a chocobo, `0x00303EC0`; 3 while `0x003135C0`
  answers; else 2) and 6, then its word 5.

The ring draws the lines of its entries with `0x003C7B30`, twice: with the colour pair at `0x01EFE370` for the entries
whose byte 2 is 1 (`0x003C3642`-`0x003C3668`), and with the pair at `0x00D11640` for those whose byte 2 is 0
(`0x003C372B`-`0x003C374E`). Each call draws an entry only when its byte 0 is set (`0x003C7D2E`) and its byte 2 equals the
call's last argument (`0x003C7D39`-`0x003C7D40`).

`0x003C7B30` takes a pair's first colour `a` from bytes 0-3 and its second `b` from bytes 4-7, each byte scaled
`(byte x word) >> 7` by the record's word `+0x5A` (bytes 0-2 and 4-6) or `+0x58` (bytes 3 and 7)
(`0x003C7B7E`-`0x003C7BF4`), and gives both vertices of a line the colour `(a + (b - a) x t) x 0.5`
(`0x003C7C22`-`0x003C7CB6`, `0x003C7E00`-`0x003C7E0C`).

`t` is `(f % 60) / 30` of the frame counter `0x0208F570`, folded to `2 - t` above 1.0 (`0x003C351A`-`0x003C357A`), and both
calls take it (`0x003C365B`, `0x003C3741`). So the lines pulse between the two colours of their pair every 60 frames: the
ring colours at `0x01EFE370` and `0x01EFE374`, or the fixed bytes `ff 20 00 80` and `ff c0 40 80` at `0x00D11640`.

The minimap's other small state:

- `0x003C5060`, from the tick (`0x003C609B`), keeps a trail of party positions while `0x0035D600()` answers 1 (bit `0x20` of
  `0x022C83E8`, which `0x0035D610(v)` sets to v): when the party is more than 3.0 from the last point `0x02B45850`/`0x02B45858`
  in x and z, it writes the position to `0x02B45860 + 16 x [0x02B45960]`, makes it the last point, counts `0x02B45962` up
  to 16 and moves the index on modulo 16.
- `0x003C5030` clears that block (`0x120` bytes from `0x02B45850`) and the live marker list (`0x1430` bytes from
  `0x02B46280`). The script verb `clearnavimapfootmark` (`0x415`) runs it, through the forwarders `0x00343330`,
  `0x003EB980` and `0x0035D5F0`, each a single `jmp`.
- `0x003C5400(i, v)` and `0x003C53E0(i)` set and clear the dword `0x02B45970 + 4i`; `0x003FFF70` sets slot 1 to the
  controlled character's record `+8` (`0x00272E10`) when that is non-zero, and clears it otherwise.
- `0x003C5720(box, item, angle, &x, &y)`, from the widget's draw (`0x003C5CE7`, `0x003C5D21`), returns the item's position,
  turned by `angle` about the centre of the box `+0x0C`-`+0x12` when the angle is not 0.

The tick also uncovers the map around the party: `0x003C6000` calls `0x003C5500` (`0x003C6096`).

1. It works only while `0x0035D630()` answers 1, bit `0x80` of `0x022C83E8` clear (`0x0035D640(v)` sets the bit for v = 0 and
   clears it otherwise, through the thunk `0x002E23D0`).
2. It works only when the party position `0x02B45810`/`0x02B45818` or the angle `0x02AEDF94` has changed since its last run.
3. It turns a 6 by 6 grid of points, -24 to 16 in steps of 8 around the party, by the angle.
4. For each point inside the map (width `0x02B45A58`, height `0x02B45A5A`) it sets the bit of the point's 16-unit cell in
   the explored mask `0x02B45A50` (row stride `0x02B45A60` bytes), the mask the map pictures are drawn through
   ([Menu map files](../Game-Files-And-Data-Tables/menu-map-files.md)).

The picture comes from the zone's map pack: `0x003C63A0` registers it and `0x00379870` places it, chosen by
`setnavimapindex` (`0x00377400`) ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

### Who shows and hides the minimap

`0x003C5E00` has three callers and `0x003C58B0` six; the creator `0x003C80C0` is reached only from `0x003C5E00` and the
world tick `0x003C6000`, and `0x003C8070`, which also closes it, only from that tick (`0x003C606B`).

| Step | Shows it (`0x003C5E00`) | Hides it (`0x003C58B0`) |
|---|---|---|
| verb `shownavimap`, body `0x00352390` | `0x0035239F` | - |
| verb `shownavimapfast`, body `0x00352AD0` | `0x00352AE2` | - |
| verb `hidenavimap`, body `0x003527D0` | - | `0x003527DF` |
| verb `hidenavimapfast`, body `0x00352E20` | - | `0x00352E32` |
| HUD switch `0x00251F40(on)`: shows for `on` above 0, hides otherwise | `0x00251F6E` | `0x00251FF7` |
| HUD-off step `0x00254AC0`, called by the field change `0x00314440` (`0x003144F6`) | - | `0x00254AEB` |
| `0x00255330(mode)`, reached from `0x00254440` (`0x0025446E`): mode 1 hides, any other mode applies the HUD switch (`0x002553A2`) | - | `0x00255357` |
| `0x0035CA70`, called from `0x0035C960` (`0x0035C9CE`) | - | `0x0035CB4B` |

No other script verb's body calls or jumps to either function. Any other verb that changes the minimap does so
through the HUD switch, the two HUD-off steps or `0x0035CA70`: `debug_switchstatusdisplay` (`0x0050DA20`) flips the HUD
switch through `0x00255020`, and `setnavimapindex` (`0x00356BF0`) only passes its argument to `0x00377400`.

### Minimap markers

The actors come from a list the minimap tick rebuilds first: `0x003C6000` calls `0x0035D070` (`0x003C6013`), which runs
`0x0035E5F0(0x022C8060)`. That builds the lists of actor managers 0 to 2 (`0x0046B560(2)`) and copies them in order, at most
128: handles to `0x022C8500` (`0x0035D500`), actors to `0x022C8700` (`0x0035D4F0`), the total at `0x022C8B00` (`0x0035D510`),
and each manager's start and count at `0x022C8B02 + i` and `0x022C8B04 + i`.

`0x003C5130` rebuilds the minimap's marker list: one 32-byte entry per actor at `0x02B45A80` (count `0x02B45A70`), then the
navigation icons (`0x00400550`), then `0x004000E0` merges them into the live list at `0x02B46280`:

1. every live node gets `+0x20` bit `0x2` (stale);
2. `0x00400AC0(entry, list, i)` handles entry `i`. Unless the entry's bit `0x40000` is set, the actor `0x003588B0(+4)` must
   exist, and its state `0x00234D40` of 2 hides a node it already has (`+0x20` bit `0x4`).
3. A node with the same id is moved to position `i` (`0x00400650` unlinks it); a new id takes the next free node of
   64 (0x50 bytes each from `+0x10`, ring index `+0x1411`, count `+0x1412`), zeroed, with `+0x22` = `0x80` and
   the scale `+0x24` = 1.0 only before the list's first fill.
4. The 32 bytes are copied in and the stale bit cleared. After the pass every node still stale and not hidden loses
   its live bit `0x1`, and `+0x1410` bit `0x1` records the first fill.

The draw `0x003C6B70` scales each marker's colour by `+0x22` (`0x80` is full) and its size by `+0x24`. It finds the
sprite with `0x00400420(out, entry)`: kinds 5 to 7 use the entry's byte `+1`; other kinds look up the byte table
`0x00D120E0` by kind, plus 6 when bit `0x80000` is set, in the shared atlas `0x0035D460`.

The routines below these draws, the trail, ring and marker quads, the picture binds and colour records written
into the VIF packets, the explored-mask set-up and the page helpers, are listed with their callers in
[map-screens-subroutines.tsv](map-screens-subroutines.tsv).

### The World Map host

The World Map host `[0x02CA8F38]` (`0x00550400`) keeps its state in the word `+0x170`. `0x00550510(v)` stores `v` in bit `0x8`
(`0x0028E72A`, `0x0028E7EE`). `0x00550610()` re-attaches the host to the root `[0x0208EA20]` and its screen `+0x160` to
`[0x0208EA28]` (`0x00246AD0`) when bits `0x1` and `0x4` are both set, clearing bit `0x2`; otherwise it sets bit `0x2` (`0x0028E770`,
`0x0028E81A`).

### World Map places

The view `0x005528C0` keeps its places in a list linked through `+0x140`; each place has its screen position at
`+0x3C`/`+0x3E` and its flags at `+0x130` and `+0x54`.

- `0x00554BD0` sorts the places into a tree through `+0x150`-`+0x160` by a key at `+0x168` (0 or 1.0, from the byte
  `+0x3B` and the word `+0x3E`), paints each in order with `0x00550BD0`, then re-sorts them by `+0x130` bit `0x2`.
- `0x00550BD0(place, ctx)` sets the place's marker pieces from its flags: a place with `+0x130` bit `0x4` or `+0x54` bit `0x10000`
  pulses `64 x sin(frame x pi / 30) + 128` (`0x0208F570`), bit `0x8` dims it to `0x40`, and `+0x54` bits `0x1`, `0x4`, `0x10`, `0x20` and `0x20000`
  pick the frames shown; it places them with `0x00562190` (`0x00562850`, through the map view `+0x80`).
- `0x00554A60(list)` eases each place's two scales `+0x138` and `+0x13A` by `0x400` a frame. A place with `+0x130` bit
  `0x1` eases toward `0x4000`, or, with bit `0x2` as well, toward `0x2666`/`0x3666` (`0x3CCC`/`0x2CCC` when the
  language test `0x00254A10` is true). A place without bit `0x1` shrinks, `+0x138` to 0 and `+0x13A` to `0x3666`
  (`0x2CCC` when the language test is true). A place with `+0x54` bit `0x10000` is held at `0x4000`.
- `0x00554EA0` draws the place names in the same order (`0x002D8650`), re-measuring a name (`0x0029CD00`) when its scale
  changes and anchoring it by `0x002718C0`.
- `0x00551130(x, y, list, find, id)` returns the place whose `+0x39` is `id` when `find` is non-zero. With `find` 0 or
  no such place it returns the first with `+0x54` bit `0x1`, or else the list's first place, and 0 for an empty list.
  It gives that place's position less half the screen (`0x01E0C1D8`, `0x01E0C1DC`), passed through `0x005552A0`.

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
| overlay container `0x0209E5C0` | `0x002B6350` from the arbiter | `0x002B6260` sets bit `0x8`; the container releases itself once both pages are gone (`0x002B7590`, continuation `0x002B7540`) |
| overlay page while the HUD is off | the HUD switch `0x00251F40` hides the current page (`0x002B6140`: bit `0x2` off through `0x00247870`, then `0x002B6260`) | `0x002B61B0` sets bit `0x2` again |
| location container `0x0209E5F0` | `0x002B9D30` | `0x002B9B30`; continuation `0x002BA6B0` |
| field-time container `0x02B47760` | `0x003CB440` | `0x003CB410`, from `0x00253A30`, `0x00282122`, `0x0028E7A3` and `0x002BA080` |
| World Map host `0x02CA8F38` | `0x00550400` | continuation `0x00552230`, which returns to the menu (`0x002814E0(0x418)`) |
| map-data widget `0x02B457E0` | the first of its three creators | the field-time container (`0x003CB91C`), the World Map host (`0x005525CB`) or the location container (`0x002BADCD`) |
| minimap `0x02B476B0` | `0x003C80C0` | `0x003C58B0`, `0x003C8070` |

## Layouts

The container's own fields, the same for the three containers `0x0209E5C0`, `0x0209E5F0` and `0x02B47760`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00180` | `u8` | legendClosing | bit `0x1` of the dword `+0xC0` of the 0xD0-byte child at `+0xC0` (`0x002B6CE0` for the overlay, the legend pane `0x002BC310` for the location map): the child sets it on message 15 (`0x002B6D02`, `0x002BC332`); the container asks a live child to close (`0x00244F00`) only while it is clear (`0x002B7899`, `0x002B7938`, `0x002B7970`, `0x002BAC3D`, `0x002BACDC`, `0x002BAD14`); the field-time container builds no child, so its test `0x003CB8D2` is not reached |
| `+0x00190` | `void*` | backImage | `LocaBack_c.tm2` (kind 7 `0xBA`), `+0x00` of the resources record `+0x190`-`+0x1AF` that `0x00404060` loads (`0x004040CC`); the overlay and the location map copy the field-time container's record (`0x002B6570`, `0x002BA040`); given to the location map's background widget (`0x002B9C46`) and freed by `0x004041D0` (`0x004041D9`) |
| `+0x001A0` | `void*` | lineImage | `w_line01.tm2` (`0xB0`), the texture of a page's line quad (`0x004040FA`); read through the page's `+0x130` by `0x002B7B80` (`0x002B8A8C`), `0x002BAF80` (`0x002BBE93`) and `0x00403640` (`0x004036B0`); freed by `0x004041D0` (`0x004041F9`) |
| `+0x179D0` | `u16` | mapRecord | the map record shown: creation word `+8` (`0x002B75F0`, `0x002BA76D`, `0x003CB6A8`; 0 for the field-time container); after a load, `0x003BC160`'s answer in mode 6 or the field's own record `0x003BFDF0` (`0x002B7750`, `0x002BA8F1`, `0x003CB7F8`); handed to the next page's builder (`0x002B77EC`, `0x002BAB8F`); a followed map link stores its target (`0x002BB964`) |
| `+0x179D4` | `u32` | requestedMap | the id mode 6 hands to the map-data request `0x003BC9F0` (`0x002B76A8`, `0x002BA816`, `0x003CB74B`); set only on the location container, by `0x002B9FE0` (`0x002B9FEC`) from `0x0028E630` |
| `+0x179D8` | `u8` | openMode | creation byte `+0x10` (`0x002B760C`, `0x002BA77B`, `0x003CB6B6`): 5 from `0x002B6220`, `0x0028E660`, `0x0028E690` and the field-time container, 6 from `0x0028E630`; compared with 6 at 12 sites in the three procedures |
| `+0x179D9` | `u8` | linkTransition | the next location-map page's opening animation, an index into the `0x28`-byte descriptors at `0x00916A70` (`0xFF`: entry 8): `0xFF` from message 1, byte `+0x20` of a followed map link (`0x002BB909`); read by `0x002B9D30` (`0x002B9ED4`) |
| `+0x179DA` | `u16` | shownMapRecord | the map record of the page last built; the builders hand the old value to the new page's `+0xBBE2` (`0x002B64FF`, `0x002B9F51`) and store the new one (`0x002B6513`, `0x002B9F63`) |
| `+0x179DC` | `u16` | linkMarker | the marker the next location-map page selects: word `+0x22` of a followed map link (`0x002BB921`), looked up with `0x004026B0` (`0x002BB397`) |
| `+0x179DE` | `u16` | linkMarkerSet | 1 when `+0x179DC` is to be used (`0x002BB928`), tested by `0x002BB389`; the overlay page makes the same tests on its own container (`0x002B7F31`; `0x002B7F3F` reads its `+0x179DC`), where nothing sets them |

A marker, `0x70` bytes, 24 in a page's list at `+0xB140`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x40` | `void*` | mapPoint | the map point it stands for, `0x003BF520(record +0x1C, record +0x1E)`, 0 for no map point (`0x00402CA8`); read by the marker painters `0x002B8EE0` (`0x002B91CF`, `0x002B925C`, `0x002B956D`, `0x002B96CF`) and `0x002BCB00` (`0x002BCE90`, `0x002BCF0C`, `0x002BD160`, `0x002BD2D2`) and by `0x00403970` (`0x00403A3A`), `0x00403F90` (`0x00403FF7`, `0x00404007`) and `0x00404730` (`0x0040476D`, `0x00404840`) |
| `+0x4E` | `u16` | markerFlags | bit `0x1` the page's selected marker (`0x002B7F57`, `0x002B80D1`, `0x002BB3B3`, `0x002BB52A`, `0x002BBC1C`), which loses bits `0x6`; bits `0x6` set on a kind-1 marker (`0x00402CBE`, `0x002BBC04`); `0x00402BF0` sets bits `0x1` and `0x8` on every kind-1 marker (`0x00402C0A`); read by `0x00403180` (`0x00403200`-`0x00403211`: bit `0x2` picks colour `0x40`, and `0x80` without it) and the labels `0x004044D0` (`0x00404624`, bit `0x8`) |

### The location sprite pane

The pane is the `0xC8`-byte widget kept at `0x0209E5F8` with procedure `0x002BC9C0`.

`LocationSpritePane` (`0xC8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x002BC9C0` |
| `+0xC0` | `void*` | sprite | the sprite the pane draws: on the draw message 4, when it is not 0, `0x00403F00` sizes and draws it 1.75 times its height in the pane's rectangle `+0x98` (`0x002BC9E7`-`0x002BCA06`). `0x002B9BE0` stores the location container's background image `+0x190` there when it builds the pane (`0x002B9C46`, `0x002B9C4D`), and `0x002BA700` stores 0 after releasing the location container (`0x002BADEA`) |

### The location caption pane

The caption pane is the `0xD0`-byte widget kept at `0x02B62D78` with procedure `0x00403380` (above).

`LocationCaptionPane` (`0xD0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00403380` |
| `+0xC0` | `void*` | iconAtlas | the atlas of the caption's icon, `0x00402730`'s first argument (`0x00402747`); the draw draws the icon from it with `0x002D8C80` (`0x004033C7`, `0x004034B1`) only while it and `+0xCA` are not 0; 0 at construction (`0x0040352C`) |
| `+0xC8` | `i16` | iconGroup | the icon's group in the atlas, `0x00402730`'s second argument (`0x00402756`): its high byte picks the group and its low byte the entry, which the draw resolves to the icon's frame record (`0x004033ED`-`0x00403402`) |
| `+0xCA` | `i16` | iconFrame | the icon's frame, `0x00402730`'s third argument (`0x0040274E`); the draw draws no icon while it is 0 (`0x004033D7`); -1 at construction (`0x0040353A`); `0x00402730` moves the second label past the frame's width only when it is not negative (`0x0040276B`) |
| `+0xCC` | `u16` | iconX | the x where the icon goes, the first label's x plus its measured width, set by `0x00402490` (`0x00402542`); `0x00402730` places the second label at it plus the icon's width (`0x004027AB`), or at it with no icon (`0x004027B9`); the draw draws the icon there (`0x0040348B`) |
| `+0xCE` | `u16` | iconY | the second label's y, `+0x0E` of its layout item, stored by `0x00402490` (`0x0040255E`); the draw draws the icon at it plus 4 (`0x0040349C`-`0x004034A3`) |

### The minimap widget's fields

The minimap is the `0xC8`-byte widget kept at `0x02B476B0` with procedure `0x003C5910` (The minimap above).

`MinimapWidget` (`0xC8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x003C5910` |
| `+0xC0` | `void*` | overlayList | the child list widget of the minimap's layout node 2, the node's `+0x18` (a type-1 node), stored on construction (`0x003C59EC`-`0x003C59F8`). Construction clears its flags bit `0x800` (`0x003C59FF`) and bit `0x1` of its nodes 0 and 1 (`0x003C5A06`-`0x003C5A3A`) and turns its activation off with `0x00247870`(child, 0) (`0x003C5A40`-`0x003C5A47`), so the tree does not draw it; on message 4 the minimap draws the child's nodes 0 and 1 itself at the child's position `+0x98`, through `0x003C5720` and `0x0029F5D0` (`0x003C5C94`-`0x003C5D3C`) |

### The World Map host's fields

The World Map host is the `0x188`-byte widget kept at `0x02CA8F38` with procedure `0x00552250`; its `+0xC0`-`+0x15B` is
the mesh object of [World Map mesh](../Game-Files-And-Data-Tables/world-map-mesh-mg.md).

`WorldMapHost` (`0x188` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00552250` |
| `+0x0C0` | `void*` | subMesh0 | the World Map mesh object starts here (meshdata.mg, World Map mesh): sub-mesh 0, the map tiles, set by the binder `0x00563110` from the file (`0x00563133`-`0x00563141`); the binder resolves its slots' images (`0x00563154`-`0x005631CD`), and the draw (message 4) passes it to `0x005556A0` through `0x00562F30` (`0x005527C3`-`0x005527D2`) |
| `+0x0C8` | `void*` | subMesh1 | sub-mesh 1, the strip mesh, set by the binder (`0x00563138`-`0x00563149`), which resolves its slots (`0x005631D7`-`0x0056324D`); the World Map view `0x005528C0` draws it through `0x00562F40` (`0x00562F70`) |
| `+0x0D0` | `void*` | meshFile | the buffer of meshdata.mg, kind-7 resource `0xA8`, requested by `0x00562F90` when `0x00550540` sets the World Map up (`0x00562FB6`-`0x00562FDA`, `0x005505D0`); the binder reads both sub-meshes from it (`0x0056312F`, `0x00563138`); freed by `0x00563080` on destroy (`0x00563099`-`0x005630A7`, `0x005525C6`) |
| `+0x0D8` | `void*` | menuList | w_menu.mrp, kind-7 resource `0xA6`, requested by `0x00562F90` (`0x0056303B`-`0x00563061`); the `0xC0`-byte frame `0x00555330` builds itself from its list record 6 (`0x00555384`-`0x00555388`); freed by `0x00563080` (`0x005630E0`-`0x005630ED`) |
| `+0x0E0` | `void*` | shadeImage | the image w_shade_p, kind-7 resource `0xAA`, registered by `0x00562F90` (`0x0056301F`-`0x00563024`, entry 0 of `0x00D231C0`); `0x00562F40` passes it to the strip-mesh draw `0x00555400` (`0x00562F74`); released by `0x00563080` (`0x005630B6`-`0x005630C8`) |
| `+0x0E8` | `void*` | main0Image | the image w_main0, resource `0xAB`, registered by `0x00562F90` (`0x00563024`, entry 1); released by `0x00563080` (`0x005630B6`-`0x005630C8`) |
| `+0x0F0` | `void*` | main1Image | the image w_main1, resource `0xAC` (`0x00563024`, entry 2); released by `0x00563080` |
| `+0x0F8` | `void*` | main2Image | the image w_main2, resource `0xAD` (`0x00563024`, entry 3); released by `0x00563080` |
| `+0x100` | `void*` | main3Image | the image w_main3, resource `0xAE` (`0x00563024`, entry 4); released by `0x00563080` |
| `+0x108` | `void*` | iconImage | the image w_icon_p, resource `0xAF` (`0x00563024`, entry 5); released by `0x00563080` |
| `+0x110` | `void*` | line1Image | the image w_line01, resource `0xB0` (`0x00563024`, entry 6); released by `0x00563080` |
| `+0x118` | `void*` | line2Image | the image w_line02, resource `0xB1` (`0x00563024`, entry 7); released by `0x00563080` |
| `+0x120` | `void*` | winImage | entry 8, w_win_c: `0x00562F90` skips it (`0x00562FE0`-`0x00562FE8`), so it keeps the constructor's 0; `0x00563080` clears it |
| `+0x128` | `void*` | mapPicture | entry 9, the map picture: `0x005632C0` loads picture `+0x148` through `0x003C1D70` under the image name map_gra_c, releasing the one before (`0x005632FB`-`0x0056333F`); `0x00562F90` skips it; `0x00563080` releases it (`0x005630B6`-`0x005630C8`) |
| `+0x130` | `void*` | cursorImage | entry 10, the registered image cursol_4_p looked up by `0x0024A5A0` (`0x00562FEF`-`0x00563024`); `0x00563080` clears it without releasing it (`0x005630B1`-`0x005630C8`) |
| `+0x138` | `void*` | lineImage | the image w_line01 the binder looks up by name after binding the sub-meshes (`0x00563258`-`0x00563273`) |
| `+0x140` | `void*` | mapScreen | the World Map screen, which stores itself here through its `+0x108` (`0x00553EF9`-`0x00553F00`); that `+0x108` holds the low 32 bits of this object's address + `0xC0`, formed in a 32-bit register at `0x005522EE` and zero-extended, handed over when the screen is built (`0x005522EE`-`0x00552316`, `0x005529BD`-`0x005529C1`). `0x00562920` reads it nine times (`0x00562920`-`0x00562A21`) and clears bit `0x1` of the dword `+0x08` of each of the nine pieces listed at `+0x60` of the screen |
| `+0x148` | `i32` | mapPictureId | the id of the map picture at `+0x128`: -1 from `0x00562F90` (`0x00563065`); `0x005632C0` loads nothing when asked for the same id and stores a new one (`0x005632DB`-`0x005632F5`); the picture pane `0x00553F40` zero-extends it to 64 bits and compares it with the whole 64-bit id it is asked for (`0x00553FAA`-`0x00553FB0`), so a stored -1 equals a request of `0xFFFFFFFF` and not a 64-bit -1; on a mismatch it passes `0x005632C0` only the request's low 16 bits (`0x00553FF1`) |
| `+0x14C` | `f32` | bind8C | 1.0, stored by the binder `0x00563110` (`0x00563282`); no function reads it |
| `+0x150` | `f32` | bind90 | 1.0, stored by the binder (`0x0056328C`); no function reads it |
| `+0x154` | `u64` | bind94 | 0, stored by the binder as one qword (`0x00563277`); no function reads it. The mesh object ends here |
| `+0x15C` | `u8[4]` | gap15C | read and written by no function; nothing fixes its width |
| `+0x160` | `void*` | screen | the `0xA020`-byte World Map screen with procedure `0x005528C0`, built on construction with the mesh object's address (`0x005522EE`-`0x0055231B`) and given the host at its `+0x110` (`0x0055232C`); it clears this when it goes (`0x00553A23`-`0x00553A2C`). The host passes it its flags and words (`0x0055244B`-`0x005524C0`), opens it (`0x005524D3`, `0x00550643`-`0x00550664`), scrolls its `+0x100`/`+0x102` on input (`0x005526B2`-`0x00552745`), draws the tiles at its scroll (`0x00552786`-`0x005527A8`) and closes or destroys it (`0x00552570`, `0x0055259E`-`0x005525BA`) |
| `+0x168` | `void*` | frame | the `0xC0`-byte frame with procedure `0x00555330`, built from list record 6 of w_menu.mrp when the World Map opens (`0x00552435`-`0x00552455`) and opened under the main root (`0x005524E6`-`0x005524F9`); it clears this when released (`0x0055535B`-`0x00555364`); closed on closing and destroyed on destroy (`0x0055255F`-`0x0055256B`, `0x0055258D`-`0x00552599`) |
| `+0x170` | `u16` | state | bit `0x1`: the mesh's batch has loaded and is bound (`0x00552353`-`0x00552362`). Bit `0x2`: `0x00550610` asked for the host before it was ready (`0x00550675`); cleared when the World Map opens or is re-attached (`0x005523FD`, `0x00550636`). Bit `0x4`: the map data has loaded (message 16 with bit `0x100`, `0x00552349`). The World Map opens when bits `0x1`, `0x2` and `0x4` are set (`0x00552367`-`0x00552380`). Bit `0x8`: `0x00550510`'s value (`0x00550510`-`0x0055052B`); release then skips `0x00285F00` (`0x005525E1`-`0x005525EA`). Bit `0x10`: message 39's first argument (`0x00552625`-`0x00552638`), passed to `0x00285F00` on release (`0x005525F2`). Bit `0x20`: the set-up record's `+0x04` bit `0x1` (`0x0055056C`-`0x00550580`), copied to the screen's `+0x150` bit `0x8` (`0x0055245C`-`0x00552472`). Bit `0x40`: set by message 40, which then asks for the World Map to open (`0x0055280B`). Bit `0x80`: closing asked by `0x00550470` on cancel (`0x005504EC`); the tick closes the host once the screen and the frame are gone (`0x0055251B`-`0x00552551`). Bit `0x100`: the set-up record's `+0x04` bit `0x2` (`0x00550591`-`0x005505A5`), copied to the screen's `+0x150` bit `0x40` (`0x00552495`-`0x005524AB`) |
| `+0x172` | `u16` | openMode | the creation's first argument (`0x005522A6`-`0x005522AC`): 6 asks for the map data `0x003BC9F0` with `+0x17A` before opening (`0x00552386`-`0x005523B3`); 2, 3 and 4 show the captions `0xC03`, `0xC04` and `0xBFA` through `0x0028FCB0` (`0x005523F1`-`0x00552430`); message 35 answers it (`0x005527FE`); `0x00550690`, `0x00550820` and `0x00550A00` read it (`0x005506FD`, `0x00550860`, `0x00550A1D`) |
| `+0x174` | `u16` | mapType | the creation's second argument (`0x005522B3`-`0x005522B7`), passed to `0x003BCAF0` when the World Map opens (`0x005523CC`-`0x005523DC`) |
| `+0x176` | `u16` | releaseArg | message 39's second argument (`0x0055263F`-`0x00552643`), passed to `0x00285F00` with bit `0x10` on release (`0x00552603`-`0x00552619`) |
| `+0x178` | `u16` | setupWord0 | the set-up record's word `+0x00` (`0x00550587`-`0x0055058A`), copied to the screen's `+0x14C` (`0x00552479`-`0x00552487`) |
| `+0x17A` | `u16` | mapDataId | the set-up record's word `+0x08` (`0x00550557`-`0x00550561`), the id mode 6 hands to the map-data request `0x003BC9F0` (`0x005523A9`-`0x005523B3`) |
| `+0x17C` | `i16` | lastScrollX | the screen's scroll x `+0x100` at the last draw (`0x00552792`, `0x005527D7`); the draw uses it when the screen is gone (`0x005527AE`) |
| `+0x17E` | `i16` | lastScrollY | the screen's scroll y `+0x102` at the last draw (`0x00552799`, `0x005527E8`); the draw uses it when the screen is gone (`0x005527B7`) |
| `+0x180` | `u16` | setupWordC | the set-up record's word `+0x0C` (`0x005505AC`-`0x005505B0`), copied to the screen's `+0x14A` (`0x005524B2`-`0x005524C0`) |
| `+0x182` | `u8[6]` | tail182 | read and written by no function; nothing fixes its width |

## Shipped data

| | |
|---|---|
| guide table in `menumap_common.bin` (`us`) | 77 entries, story counter thresholds 0 to 6,150; every entry selects `menumap_guide00.bin` |
| "???" sites | 6 places in the code load `0x3EC` |

## State

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209E5B4` | `i32` | 0 (zero-filled tail) | 1 after a Map Transparency toggle: the next frame on which `0x001EDE70` answers non-zero skips the map press tests once. `0x001EDE70` returns the frame-rate mode flag `0x01F82E38`, which `0x001EDDC0` sets to 1 for a frame limit of 1 ([Startup constants](../Engine-Core/startup-constants.md)) | `0x00253C70`: 1 on each toggle (`0x00253E45`, `0x00253E5D`), 0 when it skips (`0x00253D98`) | `0x00253C70` (`0x00253D82`) |
| `0x022C83B8` | `void*` | 0 (zero-filled tail) | the address of the minimap's map record `0x02B45A00`, which `0x003C5E40` returns | `0x0035C560`, from the interface start-up `0x00253970`: 0 with the `0x23C8` bytes from `0x022C8060` (`0x0035C573`), then the address (`0x0035C598`) | no instruction |
| `0x02B476B8` | `i32` | 0 (zero-filled tail) | the area (`0x003148F0`) whose explored mask the minimap's field set-up loaded into `0x02B45978` (`0x003C5410`); on leaving, the 32 bytes at `0x02B45978` go back into that area's Map record (`0x002551B0`) when the area has a Map entry (`0x003779F0`) | `0x003C5F00`, the field set-up (`0x003C5F77`) | `0x003C5E50`, the teardown (`0x003C5E67`); `0x003C8670`, from the jump staging `0x003145E0` (`0x003C8676`) |

These are all the accesses to `0x0209E5B4`.

No other instruction reaches `0x022C83B8` or `0x02B476B8`. The one address taken nearby, `0x022C8388` by `0x0035BC50`, reaches
`0x022C8388`-`0x022C83A7` only.

### The minimap's box and view

The minimap procedure `0x003C5910` keeps its layout box in globals. On construction (message 1) it copies the box of its
first layout node (`[+0x60]`, `+0x0C`-`+0x12`) and three quarters of its size (`0x003C5A5C`-`0x003C5ABD`); on each draw
before its content (message 3) it gives the node the smaller box, centred in the full one (`0x003C5B69`-`0x003C5BDD`).
All of these are 0 in the file (the zero-filled tail).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B476C0` | `i32` | 0 | the box's x | `0x003C5910` (`0x003C5A7A`) | `0x003C5910` (`0x003C5B9D`) |
| `0x02B476C4` | `i32` | 0 | the box's y | `0x003C5910` (`0x003C5A6E`) | `0x003C5910` (`0x003C5BC5`) |
| `0x02B476C8` | `i32` | 0 | a second copy of the x; nothing reads it | `0x003C5910` (`0x003C5A80`) | no instruction |
| `0x02B476CC` | `i32` | 0 | a second copy of the y; nothing reads it | `0x003C5910` (`0x003C5A74`) | no instruction |
| `0x02B476D0` | `i32` | 0 | three quarters of the width, `w x 96 / 128` | `0x003C5910` (`0x003C5AA8`) | `0x003C5910` (`0x003C5B89`, `0x003C5BBE`) |
| `0x02B476D4` | `i32` | 0 | three quarters of the height | `0x003C5910` (`0x003C5ABD`) | `0x003C5910` (`0x003C5BB0`, `0x003C5BD1`) |
| `0x02B476D8` | `i32` | 0 | the width | `0x003C5910` (`0x003C5A9C`) | `0x003C5910` (`0x003C5B7C`) |
| `0x02B476DC` | `i32` | 0 | the height | `0x003C5910` (`0x003C5A93`) | `0x003C5910` (`0x003C5B97`) |
| `0x01EFE374` | `u32` | `0x8040C0FF` | the ring colour: `0x002DD7E0(0xFE)` on construction (`0x003C5B34`); `0x003C6140` scales its four bytes with the other ring bytes from `0x01EFE370` | `0x003C5910` (`0x003C5B39`) | `0x003C6140`, byte by byte (`0x003C6174`, `0x003C617B`, `0x003C6182`, `0x003C6189`) |

The minimap's draw callback `0x003C32B0` hands the view record `0x02B45820` to the map view `0x003C4070` in mode 0
(`0x003C3315`). `0x003C4070` builds the view matrix `0x02B476F0` from it (identity `0x003C40AF`, then the scale and turn) and
passes the record on to `0x004001D0` (`0x003C41AB`), `0x003C3340` (`0x003C4611`, outside mode 2) and `0x003C29A0` (`0x003C4640`):

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B45820` | `i32` | 0 | `+0x00`, the view mode, 0 for the minimap | `0x003C5910`, 0 (`0x003C5ACE`) | `0x003C4070` (`0x003C4192`, `0x003C42BC`, `0x003C42F8`, `0x003C4356`, `0x003C4473`, `0x003C4587`, `0x003C45DB`, `0x003C4645`); `0x003C3340` (`0x003C33C2`, `0x003C347A`), from `0x003C4611`; `0x003C29A0` (`0x003C29C5`) |
| `0x02B45824` | `f32` | 0 | `+0x04`, the view's width, the node's width | `0x003C5910` (`0x003C5AE6`) | `0x003C4070` (`0x003C411B`); `0x003C3340` (`0x003C3414`); `0x004001D0` (`0x0040024D`, `0x004002C0`) |
| `0x02B45828` | `f32` | 0 | `+0x08`, the view's height | `0x003C5910` (`0x003C5B08`) | `0x003C4070` (`0x003C413A`); `0x003C3340` (`0x003C3428`); `0x004001D0` (`0x00400252`, `0x004002B6`) |
| `0x02B4582C` | `f32` | 0 | `+0x0C`, the centre's x: the party position `0x02B45810`, copied on each draw | `0x003C5910` (`0x003C5BF2`) | `0x003C4070` (`0x003C415C`); `0x004001D0` (`0x004002FA`) |
| `0x02B45830` | `f32` | 0 | `+0x10`, the centre's z, from `0x02B45818` | `0x003C5910` (`0x003C5BFA`) | `0x003C4070` (`0x003C4166`); `0x004001D0` (`0x0040031C`) |
| `0x02B45834` | `f32[2]` | 0 | `+0x14`, `+0x18`: the offset `0x003C4070` puts in the view matrix's translation row `0x02B47720` | `0x003C5910`, 0 (`0x003C5AFA`) | `0x003C4070` (`0x003C40B4`, `0x003C40C6`) |
| `0x02B4583C` | `f32` | 0 | `+0x1C`, the turn, 0 on each draw | `0x003C5910` (`0x003C5C1D`) | `0x003C4070` (`0x003C4101`); `0x004001D0` (`0x004002E5`) |
| `0x02B45840` | `f32` | 0 | `+0x20`, the scale: the layout record's `+0x0C` over 100 on construction, then `0x001814D0()` on each draw | `0x003C5910` (`0x003C5B1C`, `0x003C5C12`) | `0x003C4070` (`0x003C40D8`); `0x004001D0` (`0x004002D5`, `0x004002DA`) |
| `0x02B47720` | `f32` | 0 | x of the translation row of the view matrix `0x02B476F0`, the record's `+0x14` | `0x003C4070` (`0x003C40BE`) | through the matrix's address, which `0x003C4070` hands to the matrix helpers (`0x003C412D`, `0x003C416B`, `0x003C4230`, `0x003C4256`, `0x003C4281`, `0x003C42C9`, `0x003C4314`, `0x003C43E0`, `0x003C4453`, `0x003C4514`, `0x003C4607`) |
| `0x02B47724` | `f32` | 0 | y of that row, the record's `+0x18` | `0x003C4070` (`0x003C40CB`) | the same |
| `0x02B47698` | `void*` | 0 | `0x003C4070`'s fourth argument, stored in modes other than 2 before `0x003C3340` runs (`0x003C45DB`-`0x003C4611`); nothing reads it | `0x003C4070` (`0x003C4600`) | no instruction |
| `0x02B45800` | `f32` | 0 | the world x of the zone's map picture, NPS2 placement `+0x10` ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)), or 0 without one | `0x003C6360` (`0x003C6360`), from `0x00379870` (`0x003798D5`) | `0x003C4070` (`0x003C426C`); the uncovering step `0x003C5500` (`0x003C55CE`) |
| `0x02B45804` | `f32` | 0 | the picture's second coordinate, placement `+0x14` | `0x003C6360` (`0x003C6368`) | `0x003C4070` (`0x003C4279`); `0x003C5500` (`0x003C55D6`) |

### The location map and the overlay

Both containers hand a 6-byte return record to `0x00285F00` when they are gone, which copies it into the menu block
`[0x0209AC30] + 0x3E0` before the return to the menu (`0x002814E0`): the overlay's from `0x002B7540` (`0x002B7563`), the
location map's from `0x002BA6B0` (`0x002BA6D3`), `0x002BA1F0` (`0x002BA213`) and `0x002BC2C0` (`0x002BC2E2`). The page procedure
fills it when a page is picked (`0x002B79DD`-`0x002B7A53`, `0x002BADF1`-`0x002BAE5C`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209E5D0` | `u16` | 0 | the overlay's record `+0`: 3 with container bit `0x400` of `+0x179D2`, otherwise 2 with bit `0x40` and `0x1` without | `0x002B7590` (`0x002B79E4`, `0x002B7A19`, `0x002B7A41`) | `0x00285F00` (`0x00285F00`, 4 bytes), from `0x002B7540` |
| `0x0209E5D2` | `u16` | 0 | `+2`: `0x8000`, bit `0x8000` kept and set with an empty low byte (`0x002B79FB`-`0x002B7A53`) | `0x002B7590` (`0x002B79E4`, `0x002B7A0F`, `0x002B7A53`) | `0x002B7590` (`0x002B79EA`); `0x00285F00` (`0x00285F00`) |
| `0x0209E5D4` | `u16` | 0 | `+4`: the container's `+0x179D0` | `0x002B7590` (`0x002B79F1`, `0x002B7A27`) | `0x00285F00` (`0x00285F0F`) |
| `0x0209E608` | `u16` | 0 | the location map's record `+0`, set the same way | `0x002BA700` (`0x002BADF8`, `0x002BAE28`, `0x002BAE4B`) | `0x00285F00` (`0x00285F00`), from `0x002BA6B0`, `0x002BA1F0` and `0x002BC2C0` |
| `0x0209E60A` | `u16` | 0 | `+2`: bit `0x8000` set, and the second byte of the page's message record `[rbp - 0x28]` (`0x002BAE52`) | `0x002BA700` (`0x002BADF8`, `0x002BAE1E`, `0x002BAE5C`) | `0x002BA700` (`0x002BADFE`); `0x00285F00` (`0x00285F00`) |
| `0x0209E60C` | `u16` | 0 | `+4`, as for the overlay | `0x002BA700` (`0x002BAE05`, `0x002BAE36`) | `0x00285F00` (`0x00285F0F`) |
| `0x0209E600` | `void*` | 0 | the location map's pane `0x002BCA70`, `0xC0` bytes, built under the root `[0x0208EA20]` | `0x002B9BE0` (`0x002B9C0C`), from `0x002BA700` (`0x002BA8BA`); `0x002B9B30`, 0 after closing it (`0x002B9B8E`) | `0x002B9BE0`, which builds it only while it is 0 (`0x002B9BE4`); `0x002B9B30` (`0x002B9B75`) |
| `0x02B457D8` | `i32` | 0 | 1 when `0x003BC160` finds the map's quest step at an index other than 0, 0 when at index 0 (`0x003BC23D`-`0x003BC247`); `0x002BA700` clears it | `0x003BC160` (`0x003BC247`); `0x002BA700`, 0 (`0x002BAD7F`) | `0x002B9D30` (`0x002B9F1B`); the location page `0x002BAF80` (`0x002BB23B`, `0x002BB36E`, `0x002BB609`, `0x002BB99A`, `0x002BBB79`, `0x002BBC5D`); the zone gate `0x003C18A0` (`0x003C191D`, `0x003C1929`) |
| `0x02B47768` | `i32` | 0 | the area whose map resources the preload child `0x003CB4F0` loads: its argument on the opening run (message 14); 0 when `0x003C0CF0` answers 2 and the child destroys itself, and when it is destroyed (message 18) | `0x003CB4F0` (`0x003CB584`; 0 at `0x003CB597`, `0x003CB542`) | `0x003CB4F0`: the requests `0x003C2190` (`0x003CB5BC`, `0x003CB5FB`, `0x003CB618`), `0x003C21C0` (`0x003CB5F0`), and `0x003C2200` when the batch has loaded (message 16, `0x003CB569`) |

The World Map's route draw keeps the route picture's size, which `0x005520F0` reads from the picture header
(`+0x14`, `+0x16`) and hands to `0x00562E30` (`0x00552215`):

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F2CAF8` | `i32` | 16 | the route picture's width, which the two route draws give the sprite batcher as its width (`0x001819A0`) | `0x00562E30` (`0x00562E9A`) | `0x005621A0` (`0x0056234E`, `0x005623B9`); `0x00562A30` (`0x00562AE5`, `0x00562AF7`) |
| `0x01F2CAFC` | `i32` | 16 | its height | `0x00562E30` (`0x00562EA7`) | `0x005621A0` (`0x00562341`, `0x005623C1`); `0x00562A30` (`0x00562AD8`, `0x00562B02`) |

No other instruction reaches these globals. The one indexed table near `0x01F2CAF8`, `[0x01F2CA10 + 8i]` in `0x0053AB50`
(`0x0053C807`), takes an index of at most 23 (`0x0053C7AB`-`0x0053C7F9`), so it ends at `0x01F2CACF`.

The same line-state call also fills a `0x54`-byte block at `0x02CA9680` for the two route draws: `0x00562E30` passes its
own arguments to `0x00563430` (`0x00562E89`), whose fifth argument is the four floats at `+0x8C` of `0x005520F0`'s second
argument (`0x005521F2`).

- `0x02CA9680`-`0x02CA96BF` is a 4 x 4 matrix. `0x00563430` makes it the identity (`0x00203170`, `0x00563445`), stores 1.0 at
  `0x02CA9680` and `0x02CA9694` (`0x00563474`, `0x0056347E`), and stores the translation 2048 less half the screen
  (`0x01E0C1D8`, `0x01E0C1DC`) less its third and fourth arguments at `0x02CA96B0` and `0x02CA96B4` (`0x005634C6`, `0x005634BE`).
- The draws pass every route point through the matrix (`0x00202B70`; `0x005621A0` at `0x00562501` and `0x00562568`,
  `0x00562A30` at `0x00562BC4` and `0x00562BF5`).
- Float `+0x00` of the rectangle goes to `0x02CA96C8` (`0x005634F7`).
- The ribbon's texture comes from the route picture: the first segment takes the column `0x02CA96C0` x width and each
  further segment the next column (`0x00562D3B`), between the rows `0x02CA96C4` x height and that row plus `0x02CA96CC` x
  height (`0x00562B0A`-`0x00562B7B`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA96C0` | `f32` | 0 | the ribbon's first texture column as a fraction of the route picture's width (`0x01F2CAF8`): float `+0x08` of the rectangle | `0x00563430` (`0x005634D8`) | `0x005621A0` (`0x005623FB`); `0x00562A30` (`0x00562B1B`) |
| `0x02CA96C4` | `f32` | 0 | the ribbon's first texture row as a fraction of the picture's height (`0x01F2CAFC`): float `+0x0C` of the rectangle | `0x00563430` (`0x005634E4`) | `0x005621A0` (`0x00562403`); `0x00562A30` (`0x00562B23`) |
| `0x02CA96C8` | `f32` | 0 | float `+0x00` of the rectangle, stored beside the other three; no route draw reads it | `0x00563430` (`0x005634F7`) | no reader |
| `0x02CA96CC` | `f32` | 0 | the ribbon's height in the picture as a fraction of its height: float `+0x04` of the rectangle; the second row is the first plus this times the height | `0x00563430` (`0x005634FF`) | `0x005621A0` (`0x005623F3`); `0x00562A30` (`0x00562B13`) |
| `0x02CA96D0` | `i32` | 0 | a copy of the World Map line scale `0x01F2CAF4` (16 in the file, `WorldMapLineScale` in [screen layouts](screen-layouts.tsv)): each draw scales a segment's direction to this length (`0x00202FE0`) | `0x00563430` (`0x00563507`) | `0x005621A0` (`0x005625C9`); `0x00562A30` (`0x00562C54`) |

Nothing reaches these five globals beyond the listed instructions.

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Save load settings: `0x00249410` is called by `0x00582790`; `0x00249580` is called by `0x00582790`; `0x00254440` is called by
  `0x00280140`; `0x00314440` is called by `0x00280140`; `0x003145E0` calls `0x0020E500`.
- Save load settings: those functions are documented on
  [mrp menu resource packages](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md),
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md),
  [changing areas](../World-Areas-And-Travel/changing-areas.md).
