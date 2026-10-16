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
| World Map | `menu_command.bin` `0x4B7`, help `0xCCA` | main-menu entry `00281C36` |
| location map | the phrase in `0xCCA`; opened by the control "Display Map" (`0x589`) | menu request `0x21` ([Menus](menus.md)) |
| map overlay | toggled by the control "Map Transparency" (`0x586`); its layout keys are `TrackMap*` | `002B6220` |
| minimap | the script verbs `shownavimap`, `hidenavimap`, `setnavimapindex` and others | widget `003C5910` |

The two controls are rows 28 and 25 of the Controls screen (`002414B0`; [Control remapping](../Controls-And-Input/control-remapping.md)).

### Opening from the field

The input arbiter `00253C70` keeps the map state in `02092750`:

1. Map Transparency toggles the state between 0 and 3 and remembers it in `0209E5B0` (`00253E2F`-`00253E63`).
2. State 3 opens the map overlay with `002B6220(1)` (`00253DE2`) when the field-time container is ready (`003CB3E0`),
   `02092754` is 0, the field has a map record (`003BFDF0`) and the story counter is at least 16
   (`00253DD1`-`00253DDA`).
3. Display Map closes the overlay and posts menu request `0x21`, the location map (`00253EA4`-`00253EF2`). Leaving
   the location map restores the overlay as it was (`002BBA2F`-`002BBA3C`).
4. While the state is not 3, the overlay is closed every frame (`002B6260`, `00253C92`).

The location map also opens from `0028E630`, `0028E660` and `0028E690`, and the World Map host `00550400` from
`0028E690` and `0028E790` ([Menus](menus.md)).

### The two-page container

The overlay and the location map each have a container of 0x179E0 bytes, at `0209E5C0` (`002B6350`, procedure
`002B7590`) and `0209E5F0` (`002B9D30`, procedure `002BA700`). Each holds two 0xBC08-byte pages in place, at `+0x1B0`
and `+0xBDC0`, and flips between them:

1. The first call creates the container with no page (`002B638F`-`002B63D7`).
2. A container message `0x20` sets its open request, bit 7 of `+0x179D2`.
3. The next frame's step builds a page in the other slot (`00245000`, `002B6474`), flips bit 2, attaches the page
   and sends it `0x21` (`002B6526`-`002B6541`).

A page posts messages to every ancestor up to the root through `00275440`, which follows the parent link `+0x10`
that `00244960` sets; its container acts on `0x2B` when it has opened and `0x1F` when it is cancelled. The page procedures `002B7B80` and `002BAF80` answer
the same 17 messages through their tables at `0x198EB0` and `0x19C28C` from the image base.

`002B6220` also copies the field-time container's resources into the overlay's `+0x190` and sends it `0x10` and
`0x20` (`002B6570`).

### The field-time container

`02B47760` (`003CB440`, procedure `003CB650`) draws nothing. It holds the map resources, the map-data widget and a
preload child `003CB4F0` that fills the map cache, and its bit 7 marks the preload as finished (`003CB551`-`003CB55F`),
which the overlay waits for. It is created from `00253A30` and the HUD-on step `00251F40`, and destroyed by
`003CB410`.

### Map resources

`00404060` loads the 32-byte record every page reads at `+0x130`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32[2]` | back | LocaBack_c.tm2 (kind 7 `0xBA`) |
| `08` | `u32[2]` | atlas | Loca_8_c.tm2 (`0xB9`) |
| `10` | `u32[2]` | line | w_line01.tm2 (`0xB0`), the texture of the page's line quad |
| `18` | `u32[2]` | mrp | Loca.mrp (`0xBF`) |

### The map-data widget

`003BC450(world, location, owner)` creates the widget `02B457E0` once (`003BC463`), and `003BC2D0` loads:

| File (kind 7) | When |
|---|---|
| `menumap_world.bin` (`0xA2`) | `world` is set: only the World Map (`003BC440`, `005505E4`) |
| `menumap_location.bin` (`0xA3`) | `location` is set: all three creators |
| `menumap_common.bin` (`0xA4`) | always |

The location container (`002BA15C`) and the field-time container (`003CB4CC`) pass `(0, 1)`. `003C1DF0` then picks the
last entry of the guide table in `menumap_common.bin` whose story counter and story gate pass (`003BD950`) and loads
`menumap_guideNN.bin` (kind 7 `0x496` + the entry's byte `+4`). `menumap_area.bin` (`0xA5`) is loaded separately into
`020927D0` (`00253780`).

### What a page draws

Each frame, a page rebuilds its element list (`00402A40`) and draws (`002B8A19`-`002B8B11`):

1. one quad textured with `w_line01.tm2` (`00404230`);
2. the line elements (`004043B0`), pulsing the marked ones;
3. one marker per point, each a small map view through `003C4070` in mode 2 (`00404120`, `002B96E7`);
4. the labels (`004044D0`).

### What is shown

The story gate `0032A8A0` ([Story flags](../Story-Events-And-Hunts/story-flags.md)) and the encoded-id query
`00309EC0` decide every map element:

| Element | Shown when |
|---|---|
| area point (`003C18A0`) | its gate (word `+0xE`) passes and the area is current, visited or its map is owned (`003BCBA0`) |
| link point (`003C0F70`) | its gate `+0x16` passes, and its map is owned, or its gate `+0x12` is `0xFFFF` or set |
| label (`003C2320`) | revealed; otherwise "???" (`0x3EC`, `003C25B1`) |
| location (`003C12B0`) | its kind's gate passes and its map is owned, or one of its points can be drawn |
| World Map destination (`003C08B0`) | its gates pass and the story counter (`00265270`) is below its word `+8` |
| icon of a sub-location (`003DFB50`, `003FFF40`, `00400CF0`) | its word `+0xA` is 0, or its gate passes; 1 never shows |

`003BCBA0` builds the state an area point reads: the current area (`003C1070`), a visit byte at
`[020927C0] + 0x224 + 32 x entry` (`00255200`), and the area's map as a key item of class `0x8000` (`002543F0`; the
map list is `menumap_area.bin` `+0xC`).

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

### Lifetimes

| Object | Created | Released |
|---|---|---|
| overlay container `0209E5C0` | `002B6350` from the arbiter | `002B6260` sets bit 3; the container releases itself once both pages are gone (`002B7590`, continuation `002B7540`) |
| location container `0209E5F0` | `002B9D30` | `002B9B30`; continuation `002BA6B0` |
| field-time container `02B47760` | `003CB440` | `003CB410`, from `00253A30`, `00282122`, `0028E7A3` and `002BA080` |
| World Map host `02CA8F38` | `00550400` | continuation `00552230`, which returns to the menu (`002814E0(0x418)`) |
| map-data widget `02B457E0` | the first of its three creators | the field-time container (`003CB91C`), the World Map host (`005525CB`) or the location container (`002BADCD`) |
| minimap `02B476B0` | `003C80C0` | `003C58B0`, `003C8070` |

## Shipped data

| | |
|---|---|
| guide table in `menumap_common.bin` (`us`) | 77 entries, story counter thresholds 0 to 6,150; every entry selects `menumap_guide00.bin` |
| "???" sites | 6 places in the code load `0x3EC` |

## Modding notes

- An area's map item is listed in `menumap_area.bin`; owning it reveals the area's points without visiting them.
- A World Map destination disappears once the story counter reaches its word `+8`; `0xFFFF` keeps it forever.
- The overlay cannot open before story counter 16 (`00253DDA`).
- The minimap's picture is the zone pack's own image, not a menu file.

## Related

- [Menus](menus.md) - the requests that open the maps.
- [Story flags](../Story-Events-And-Hunts/story-flags.md) - the gates the map elements read.
- [Story progress](../Story-Events-And-Hunts/story-progress.md) - the story counter.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md) - the zone pictures and placements.
- [Controls](../Controls-And-Input/controls.md) - the input words.
