---
title: "Debug menu: the developer console object, its fifteen pages, its command dispatcher and the retail rows that still reach it"
kind: "system"
category: "Engine core"
addresses: "0x001D1660, 0x001D4C1C, 0x001D4BFA, 0x001D4C09, 0x001CD040, 0x0017DB90, 0x0017E070, 0x0023B330, 0x0023B6F0, 0x001D50D0, 0x001CCB20, 0x001D0390, 0x001CD0E0, 0x001D5260, 0x001D5520, 0x0017DAA0, 0x00187950, 0x001D0190, 0x008FCE00, 0x01DF6E68, 0x0017D490, 0x001A9930, 0x00193D50, 0x001DF340, 0x001DDAB0, 0x001C2F40, 0x003058B0, 0x00254EE0, 0x0020AC30, 0x0020AF10, 0x001EC560, 0x00358330, 0x0022A550, 0x01F82D20, 0x01DF6E48, 0x01F81270, 0x001C2F00, 0x001C1D40, 0x001C2120, 0x001EA3C0, 0x006CCCE0, 0x001C2980, 0x001C2D10, 0x00181F20, 0x00181E70, 0x001C2DB0, 0x001EA830, 0x001EAC60, 0x001EAE10, 0x0022FFE0, 0x00181FD0, 0x001820E0, 0x0020A760, 0x001EC4B0, 0x001C5040, 0x001EC500, 0x0050C8A0, 0x0050D0C0, 0x002E05E0, 0x00254FE0, 0x00255020, 0x001C5110, 0x001C0540, 0x001DCB90, 0x001DCD30, 0x0020DA50, 0x00308E80, 0x003091C0, 0x001C1C80, 0x001C1B00, 0x001C1A60, 0x001C1C00, 0x001C19A0, 0x0020AA50, 0x001ACC30, 0x001AC950, 0x00189130, 0x00188E60, 0x00189570, 0x001AC7C0"
---

## What the player sees

Nothing, in a retail game. The remaster carries the developers' tuning menu: fifteen pages of
rows such as "Invincible", "Set gill to max", "Shadow Level", "Water Fresnel Factor" and "Enable
100% successful steal", each a name with a value beside it that a press of left or right would
step. The code that draws it and the code that runs every row are in the shipped game, but the
byte that opens the menu is never set, so no button sequence shows it.

What a player does see is the Config screen's graphics rows: brightness, V-sync, anisotropic filtering, shadows, anti
aliasing, ambient occlusion, depth of field, glare and the rest are the same rows, driven through
the same dispatcher.

## How it works

### The console object

`0x001D50D0()` returns the console settings object, created on first use (`0x00210EC0(0x10E8)`, then
the constructor `0x001CCB20`) and cached at `0x01F81428`. The constructor zeroes and defaults the
object and calls `0x001D0390`, which stores the row labels when `0x001EA3C0(obj + 8)` returns 0,
noting that at `+0xA68`: one string pointer per id at `+0x130 + id × 8` for ids 1 to 294 (id 2's
string is empty), 293 names in all.

`0x001D0390` also primes page 0 through the renderer, sets the text parameters and writes nine
32-byte strings at `+0xAE4`, `+0xB04` to `+0xBE4` (`OFF`, `Black
Hole`, `Luminescence`, `Ark Blast`, `Whiteout`, `Windburst`, `Torrent`, `Cataclysm`, `Inferno`),
the concurrence names an information row prints.

Before those strings it runs `0x002F79E0` (`0x001D03DC`), which copies the eight-word constant `0x00D0F9E0` (`0xF1`, `0xE7`,
`0xEA`, `0xED`, `0xE5`, `0xE4`, `0xE3`, `0xE2`) into `0x022BE930`. `0x002F8D60` returns word `[0x01EEBAF0]` of that table whenever
`0x01EEBAF0` is not negative.

The open byte `+0xA70` is written once, to 0, by the constructor; no other instruction in the
image writes it. The page cursor is `+0xA88`, the row count `+0xA90`, the information-page flag
`+0xC56`, the weather-slot override `+0xAAC` (read through `0x0017D490` by the field runtime,
[weather](../World-Areas-And-Travel/weather.md)), and the field id for the code table `+0xAB4`.

### The pages and the renderer

The page table at `0x008FCE00` holds 15 pages of 22 ids (0 = no row). `0x001D5260`, called from the
field frame's draw block through `0x0017DAA0` when `0x00358330(1)` holds ([frame update
order](frame-update-order.md)), returns at once unless `+0xA70` is set; otherwise it prints `<Page
n/14>` or `<Information Page>` and, for every id on the page, has the row renderer `0x001CD0E0(ctx,
id, buffer)` format the row (`"None content!!"` when it prints nothing).

The information page (page 14) runs its ids through the filter `0x001D0190` first:

- ids 1, 2, 6, 9, 102, 204, 221, 222 and 290 always;
- 7 only while an event slot holds queued events (`0x01DFE40C`, the slot of the most recent
  `startscene` push, at most 4 and its counter at `0x01F832B0` non-zero; `0x0020AF10` sets it and
  `0x0020AC30` leaves it at -1);
- 8 only while the save-load manager at `0x01F81258` has its byte `+9` set;
- 10 only while `0x0022A550()` holds (main-loop state 2 with `0x00358330(1)`);
- 101 only while `+0xA74` is 2; any other id is dropped.

`0x001D5520`, called from the render pass list `0x00187950`, redraws rows 9 and 10 of the information
page at their remembered positions `+0x10B0` / `+0x10B4`.

| Page | Row ids |
|---|---|
| 0 | 2, 18, 20, 19, 21, 22, 23, 4, 5, 51, 198, 202, 203, 204, 12, 13, 9, 10, 183, 188, 293, 294 |
| 1 | 2, 14, 182, 185, 184, 197, 199, 200, 201, 224, 261, 15, 16, 205, 206, 207, 217, 220, 187, 186, 292 |
| 2 | 2, 223, 225 to 242, 209, 210 |
| 3 | 2, 17, 243 to 246, 259, 247 to 258, 209, 210 |
| 4 | 2, 100, 101, 103 to 106, 60, 11, 61, 152, 190 to 195, 176 to 179, 209 |
| 5 | 2, 26 to 32, 62, 34 to 39, 175, 40, 24, 25, 209, 210 |
| 6 | 2, 42, 43, 44, 46, 47, 48, 279, 53 to 59, 90, 91, 94, 107, 209, 210 |
| 7 | 2, 72 to 89, 209, 210 |
| 8 | 2, 136 to 144, 153, 154, 155, 167 to 173, 209, 210 |
| 9 | 2, 174, 95 to 99, 108 to 119, 209, 210 |
| 10 | 2, 120 to 135, 165, 166, 209, 210 |
| 11 | 2, 63 to 71, 156 to 164, 209, 210 |
| 12 | 267, 268, 288, 271, 269, 270, 147 to 151, 92, 93, 145, 146, 286, 180, 181, 289, 209, 210, 287 |
| 13 | 2, 266, 264, 265, 263, 272, 273, 284, 283, 274, 134, 275 to 281, 166, 285, 282, 291 |
| 14 | 2, 3, 222, 221, 6, 8, 204, 9, 10, 101, 102, 290 (the information page) |

The renderer prints the label from `+0x130 + id × 8` and the row's value with `"%s%s%f"`. Its
read-out rows use two more tables:

- the authored-code table at `0x01DF6E68`, 1,314 records of 16 bytes (`char* code, u32 index + 1,
  u32 0`; 601 codes such as `ous0101`, the map pack of the field with that index, [MPK map
  pack](../World-Areas-And-Travel/mpk-map-pack.md)), indexed by the field id at `+0xAB4`;
- the event-slot panel: five slots whose names (`0x01F832F0 + slot × 0x20`), queued event counts
  (`0x01F832B0`) and classification bytes (`0x01F832E8` for a `sum_` name containing `0001`,
  `0x01F832E9` for a `spc_` name) the setter `0x0020AC30` and the pusher `0x0020AF10` maintain from
  the `plan_master\<locale>\event\` paths the resource loads hand them.

The setter's test that a path has that form is `0x0020A800`, a `std::regex` match
([MSVC containers](../Compiler-And-C-Runtime/msvc-containers.md),
story and events).

The setter takes the slot's name from the path with `0x0020AA50(out, path)`: the text between the last
`\` and the last `.`, the event file's name without its extension.

`0x0020A760(slot)` empties a slot. For a slot below 5 it clears the shared name `0x01F832C8`, the
slot's name, its vector `0x01F83390 + slot × 0x20` and its count; in every case it leaves the marker
`0x01DFE40C` at -1. The setter `0x0020AC30` calls it, and so does `0x001EC4B0` (from `0x00360120` and from
`0x00356D40`, the begin of `eventdispose_f2`), which then raises the byte `0x01FD3AE3` (`0x00214B30`).

On that byte `0x00214C30` runs `0x001C5040`, which empties `0x01F812A8`, clears the two scene maps of the
current index `0x01F813F8` (`0x01F813A8` and `0x01F813D8`, through `0x00202880`) and sets that index's
words at `0x01F81400` and `0x01F81408` to -1. Script call `0x5C9` (`0x00352F00`) pushes `0x001EC500()`, the
queued count of the marked slot, or 0 when none is marked.

### The read-out rows

Several rows print a live value that the renderer `0x001CD0E0` gathers itself:

| Row | Label | What the renderer prints |
|---|---|---|
| 2 | (information) | the frame rates and the background, with the loaded map `0x00314910()` (payload `+0x105C`, [zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) and the story-progress word `0x00265270()` as its `(%d/%d)`, and, with an event slot marked, `event:` with the slot's name from `0x001C5110` (the name at `0x01F832F0 + slot × 0x20`, empty without a marked slot) |
| 7 | (information) | `CutSceneName: %s Cut: %d(id: %d) Frame: %d`: the slot name (`0x001C5110`), its queued count, the last entry of its vector `0x01F83390`, and the counter `0x01F832C4` |
| 8 | (information) | for the picked object of `0x001C0DA0()` while its byte `+9` is set and the information page is open: its name (`0x001C0330`: `Disabled`, `NULL` or its own), its mesh texture (`0x001C0540`), its procedural texture (`0x001C0480`) and its tiling and blending values |
| 57 | Operate cube map | `0x001AD440()` `+0x168` through `0x0017F5E0` (-1 without the object), marked `NOT EDITABLE` unless its `+0x40` is 1 |
| 59 | Recapture cube maps | the status string `0x001AC7A0` picks: `+0x204 + [+0x200] × 0x20` of the cube-map object |
| 102 | Current GPU Temperature | the current adapter's temperature, `%d(C)` (below) |
| 220 | Extra BGM status | `0x0017E010`: `Not forced`, `Forced on` or `Forced off` from `0x01DF0018` by `0x01DF0010` |
| 222 | Control character position | `x:%f, y:%f, z:%f` from `0x003091C0`: the position (`0x00265020`) of the actor `0x00263750(0x003272F0())` when `0x00265970` holds; `0x003272F0` is the party leader's roster slot ([party leader](../Party/party-leader.md)) and the call goes through `0x0031ABF0`, a jump to `0x00263750` |
| 246 | Chara Name | `(%d) %s`: `0x00308E80(i)` gives a name from the record that `0x022C24E0 + i × 8` points to: its byte `+4`, below 6, picks one of `Vaan`, `Ashe`, `Fran`, `Balthier`, `Basch`, `Penelo` at `0x01EEC268`; otherwise `Nobody` |
| 264 | Game Display Resolution | `0x001DCD30`: `%d X %d ,%dHz, %dHz`, the configured resolution (`[0x01F82D20]` `+0x04` / `+0x06` with `+0x08` set, else `+0x2C` / `+0x2E`), the desktop's refresh rate (`EnumDisplaySettingsW`) and the selected mode's rate; then `Screen Resolution :%dx%d` from `GetSystemMetrics` |
| 266 | System Adapter | `0x001DCB90`: ` Count %d ,Now: %s ,Video Memory: %lld MB, Temperature: %d(C)`, the memory being the adapter's `+0x110` divided by 1,000,000 |
| 290 | Game Time Stop is | `Off` while the running byte `[0x0018A7D0()]` is 0; else `On by Debug` when its second byte is set (`0x0018A790`), `On by Focus` when its third is (`0x0018A7B0`), else the third string at `0x008FFF08` |

For row 8, `0x001C0540` asks the map-art context: `0x001A74A0` finds the object's `+0x260` in the map at
`+0x448`, takes the name at the entry's `+0x40`, and keeps the part after the last `/` minus its
last ten characters. `0x001C0480` copies the string at `+0x80` of the first entry of the object's
`+0x18` list (`0x001E3E90`) with `0x001BE660`.

Rows 102 and 266 query the graphics vendors' libraries. The current adapter is the record at
`+0x78 + [+0x48] × 0x140` of the `0x001DDAB0` object (`0x001DC9C0`), and `0x0020D2B0` builds a chain of
`AdapterInfos` providers whose head sits on the stack and whose second link is the static
provider at `0x01E02580`. `0x0020DA50` asks each provider in turn (vtable slot 0) for the
temperature of the adapter id at the record's `+0x104` until one answers, and `0x0020D9F0` asks the
same way (slot 1) for the name. `0x001DCB90` falls back to the record's own name (`+0x00`).

### The dispatcher

`0x001D1660(ctx, dir, !dir, id)` is 13,753 bytes long. At
`0x001D166F` it subtracts 12 from the id, refuses anything above 281 unsigned (so ids below 12 too)
with the do-nothing arm `0x001D4C09`, and jumps through a 282-entry table of image-relative
offsets at `0x001D4C1C`, placed right after the body: arm = `0x120000 + table[id - 12]`. The 282
entries name 227 distinct targets, 226 arms and the shared do-nothing arm `0x001D4BFA` that 56 ids
share; 212 of the arms end in a jump to it. Valid ids are 12 to 293, so ids 1 to 11 are label-only
rows.

The arms are small. 110 step a float: `movss` the field, `test bl, bl` (the direction), `subss`
or `addss` by one constant from the float pool, `movss` back. 102 of them have one magnitude,
symmetric in both directions: 0.01 for 58 arms, 0.02 for 11, 0.05 for 10, 0.1 for 9, 0.001 for
7, 0.03 for 3, 1.0 for 2, 0.5 and 0.005556 for one each. The sign composes from the mnemonic and
the constant's own sign (`+0.01` at `0x008F30E4`, `-0.01` at `0x009002F4`).

The rest call a subsystem, step an integer with a wrap, toggle a byte or cycle a mode; the table
on [debug menu commands](debug-menu-commands.md) gives every id. The shared helpers are
singleton getters: `0x001A9930` (`0x01F81168`), `0x00193D50` (the `0x4A8` post-process parameter object
at `0x01F7F5F0`), `0x001DDAB0` (`0x01F82D18`), `0x001C2F40` (`0x01F81270`), the game-setting object pointer
`0x01F82D20` loaded in 18 arms, and the indexed store `0x001DF340(obj, i, v)`.

Rows 205 to 207 (Music, Voice, Sound Effect) set the music, voice and sound-effect category
volume to 1.0 or 0 through `0x001DBB00`, and row 217 steps the 3D sound behind ratio with the
getter `0x002DEBA0` and the setter `0x002DF2A0` ([audio manager](../Sound-And-Music/audio-manager.md)).

Most stepped fields are in the render settings block ([graphics settings](graphics-settings.md)); the gil row is
`0x003058B0`, which hands 99,999,999 to the ordinary setter `0x00254EE0`
([gil](../Rewards-EXP-Gil-And-Loot/gil.md)).

Row 20, Load chr, steps a bound model id with `0x002EEEE0(id, step)`, step 1 or -1 (`0x001D171B`, `0x001D1730`). It
adds the step to the id's number; when that goes below 0 it takes the letter before the id's in the eight-letter
table at `0x00D0F870` (pairs of two dwords `{letter, kind}`: `b` 22, `s` 23, `t` 25, `g` 13, `w` 16, `c` 14, `m` 34,
`n` 19; only the letters are read, and no instruction refers to the 8 at `0x00D0F860`) and restarts the number at 0.

The stepper then takes the kind and file index from `0x002ED6F0` ([Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)),
moves the number on by the step again while the file has no size (`0x002DF980`, `0x002DF8E0`), and returns the id
when its path ends in `.cm`, else 0.

### Who reaches the dispatcher

`0x001D1660` has one caller (the data references at `0x01D5D550` and `0x01D5D560` are exception
records, not a call table), the adapter `0x001CD040(ctx, dir, id)`, whose one caller is `0x0017DB90`,
whose two callers are the message procedures `0x0023B330` and `0x0023B6F0` of the retail Config
screen's rows.

`0x0017DB90(kind, value, dir)` maps a row kind to a console id and dispatches it,
then returns the row's new value from `0x0017E070(kind)`, a read of `[0x01F82D20] + offset` for most kinds;
kind 5 reads the display object through `0x001DD050(0x001DDAB0())` (its `+0x38` when its `+0x18` is 0, else
`+0x24`), kind 6 reads `+0x08`, and any kind not in the table returns -1:

| Row kind | Console id | Label | Value read |
|---|---|---|---|
| 1 | `0x11B` | Apply Graphic Quality Default | `+0x0C` |
| 4 | `0x10A` | System Adapter | `0x001DDAB0() + 0x48` |
| 7 | `0x110` | Brightness | `+0x10` |
| 8 | `0x111` | Vsync | `+0x14` |
| 9 | `0x11C` | BackBufferCount | `+0x44` |
| 10 | `0x11D` | Frame Limit | `+0x48` |
| 12 | `0x112` | Anisotropic filtering | `+0x18` |
| 13 | `0x86` | Water Quality | `+0x40` |
| 15 | `0x113` | Shadows Quality | `+0x1C` |
| 16 | `0x114` | Character self-shadow | `+0x3C` |
| 18 | `0x115` | Anti-aliasing | `+0x20` |
| 19 | `0x116` | Post process AA | `+0x24` |
| 20 | `0x117` | Ambient Occlusion | `+0x28` |
| 21 | `0x118` | Depth of Field | `+0x30` |
| 22 | `0x119` | Glare | `+0x34` |
| 23 | `0xA6` | Use soft particle | `+0x38` |

Kinds 5 and 6 do not dispatch: 5 runs `0x001DC940` on the `0x001DDAB0` object and `0x001DC730` when
`[0x01F82D20] + 8` is 0, and 6 cycles its value through 0, 1, 2. So sixteen of the 282 ids are
retail, reached from the Config screen; the other 266 have no caller in the shipped game, and
the menu that would reach them never opens.

Two console bytes are read by input code instead of a menu arm. While `+0xC3D` (row 293, "Key
Board Debug For Japanese Keyboard") is set, the control-code lookups `0x00197790` and `0x00197800`
use the 106-entry table `0x01DF1030` in place of `0x01DF0E80`, and while `+0xC35` (row 187, "Enable
mouse control camera") is set the input translator `0x00197160` calls `GetForegroundWindow` at
`0x001973DA` ([on-screen keyboard](../Controls-And-Input/on-screen-keyboard.md), [controls](../Controls-And-Input/controls.md)).

### The debug script verbs

The verb table keeps a family of `debug_` calls that event scripts could issue. Their handlers in the
shipped game:

| Verb | Handler | What it does |
|---|---|---|
| `debug_mapjump` `0x2026` | `0x0050C8A0` | `0x00314440(map, 0, 0, 0)`, the map-jump funnel ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)), then `0x00314D60(1)`, which stores 0 in `0x022C2540` because its gate, the stub `0x005C5230`, returns 0 |
| `debug_eventload` `0x202D` | begin `0x0050D030`, poll `0x0050D0C0` | kind 4 goes to `0x00314410(id)`, which, while `0x01EED060` is negative, requests a teardown (`0x0026A5F0(4)`) and stores the id there; any other kind is the scene load request `0x0032FC30(kind, id)`; the poll holds while `0x0032E520(1)` reports a load |
| `debug_isnewcharsep` `0x2070` | `0x0050CAD0` | pushes `0x003A1640(v)`, which is `v < -1` |
| `debug_isopen_total_menu` `0x2085` | `0x0050D200` | pushes `0x002E05A0()`: the menu mode `0x02092730` is neither 0 nor 5 |
| `debug_isopen_menu` `0x2081` | `0x0050D220` | pushes `0x002E05E0()`: the same, or any of the 8 records at `0x0215F200` (stride `0x68`) live with its byte `+0x38` or bit `0x1` of `+0x3E` set |
| `debug_switchstatusdisplay` `0x2036` | `0x0050DA20` | jumps to `0x002E2290`, which jumps to `0x00255020`: flips `0x020927E8` and hands it to `0x00251F40`, which returns at once while bits `0x40` and `0x80` of `0x01E0C320` are both set, and otherwise runs one set of calls for a positive value and another for 0 |
| `debug_switchmonsterhpgauge` `0x206A` | `0x0050C890` | jumps to `0x00254FE0`: flips `0x01E0C2A8` and hands it to `0x0028FFE0(0, v)`, as 0 while bit `0x400` of `0x002E0FA0()` is set |

### The debug text display

The rows that print text in the 3D view do it through the `MultipleDebugDisplay` singleton at
`0x01F81270` (getter `0x001C2F40`). `0x001C2F00` allocates its `0x4670` bytes and runs the constructor
`0x001C1D40`; `0x001C2120` is the destructor body and `0x001C2670` the deleting wrapper. The start-up
step `0x0017D6B0` makes the call to `0x001C2F00` ([game application](game-application.md)). A line
is a `0x230`-byte record: x and y floats, a 256-byte text buffer at `+0x08` and a text object at `+0x108`.

The constructor builds 32 fixed records at `+0x10` and prepares each text object with `0x001EA3C0`.
That loads `PhyreText.fx` and the font `tuffysdf.fgen` (the two paths at `0x01DFDE00`), binds the
technique `RenderText_SoftEdges` (`0x006CCCE0` looks it up by name from the table at `0x00D89BE0` and
caches it), writes `"Debug Info:"`.

It sizes the glyph arrays for 128 entries (`0x0067C310`, which
grows them with `0x00672B80` and `0x00672C70`). The constructor then calls `0x001EAA90(object, 1280, 720)` on each
and leaves the mode `+0x0C` at 0, the overlay byte `+0x463C` at 0, and the scales
`+0x4664` / `+0x4668` at -5.5 and -10.0.

`0x001C2980(display, line, kind)` queues a line. Both kinds map the position through `0x001C2D10`
(x × `+0x4664` - 1.65, y × `+0x4668` - 2.0), hand the text to the object (`0x001EADB0`, `0x001EAD20`) and
mark it visible (`0x001EAEA0`):

- kind 0, from `0x00181F20` (the character-name printer `0x0053AB50`): taken only while the mode is
  non-zero and fewer than 32 fixed lines are queued (`+0x4610`);
- in mode 2 kind 0 drops lines that start with `W`; in mode 3 it keeps only lines that start with
  `C`, `M` or `N` (either case); a kind-0 line that starts with `H` or `M` gets 1 added to its y,
  one with `G` gets 2;
- kind 1, from `0x00181E70`: taken only while `+0x463C` is set, appended to the vector at `+0x4618`
  (count `+0x4638`). The vector grows through `0x001C2D50` and `0x001C2790`, which copy records with
  `0x001C1B00`, `0x001C1C80`, `0x001C2230`, `0x001C1E70` and `0x0067ACF0`.

Growing a vector copies `DebugLine` records. `0x001C1C80(dst, src)` copy-constructs one: x, y and the
256-byte text, then the text object through `0x001C1E70`. `0x001C1B00(out, first, last, dest)` does the
same for a range into new storage, `0x230` bytes apart, and `0x001C1A60(first, last, destEnd)`
copy-assigns a range backward, the text object through `0x001C22A0`.

Both text-object copies take the
object's array of strings with `0x001C1C00(dst, src)`: a new array of the same count (the low 31 bits
of its count word) from `0x0017D260`, and `0x001C19A0(dst, src, n)` duplicates each string into its own
block, its source pointer read with bit `0x1` cleared.

The render pass list `0x00187950` calls `0x001C2DB0`, which draws the fixed lines while the mode is set,
the overlay lines while `+0x463C` is set, and the lines of the vector at `+0x4640` (count
`+0x4660`), then zeroes the counts.

Each line goes through `0x001EA830`: when the object is visible
(`+0xEA`) and built (`+0x20`) it draws the string in black at its position plus the offset
`+0x100` to `+0x108`, then in white at its position, both through `0x001EAC60`, which writes the
placement into the material at `+0x208` to `+0x234`. `0x001EAE10` releases a text object: its material (`0x001EA050`),
its glyph object (`0x0067B3A0`) and its two assets (`0x0019CC50`). `0x001EA130`, reached from
the unwind handlers `0x0089873C` and `0x0089E880`, frees a counted array the same way `0x001EA050` does.

Four console rows drive it. Row 51 "Draw Chr Names" cycles the mode through 0 to 3 (`0x001D5230`).
Rows 218 and 219 step `+0x4664` and
`+0x4668` by 0.1. Row 176 "Show Map Hide Group" sets `+0x463C` (`0x001D2C08`), which makes the pump run
`0x0022FFE0`.

`0x0022FFE0`
walks the cells of the collision grid `0x0026E500(0)`, draws a four-vertex quad over each cell and prints at its
centre the list of eight-bit group numbers found in the cell's polygon attribute words
(`"%d, %s"`). It places the text with `0x00181FD0` and `0x001820E0`, which multiply a point by the
first (`+0x08`) and second (`+0x78`) matrix of the camera block: the camera pair's (`0x0018A620`)
while its first byte is set, else the render manager's `+0x690`.

### The cube-map capture camera

The cube-map object (`0x001AD440`, `0x258` bytes at `[0x01F811C8]`) carries a developer capture: a step
that would point the render manager's cameras at each face of a cube, or around a panorama, one
step per frame. Console rows 56 "Capture cube map" and 59 "Recapture cube maps" name it (labels
stored at `0x001D07FE` and `0x001D0828`). The capture never runs in the shipped game.

The step `+0xA8` is set to -2 by the constructor `0x001AA9E0` (`0x001AAA5C`). The only other store,
`0x001AC7D6` in `0x001AC7C0`, sets it to -1 when the step is -2 and byte `+0xA4` is set, and `+0xA4` is
written only by the constructor, with 0 (`0x001AAA55`). The step stays at -2.

`0x001ACC30(object, &fov, &scale, &aspect, &a, &b, &c)` turns the step into a camera. It returns false
and writes nothing when the count `+0xB8` is 2 or the step is negative or odd. Otherwise it writes the
defaults (fov 2π, scale and aspect 1, the angles 0), takes `n` = count / 2 and the face `f` = step / 2,
and continues by the mode `+0xBC`:

| Mode | fov | Angles |
|---|---|---|
| 0, 1 | 2π / (n − 2), 90° for the constructor's count of 12 | face 0: `a` = −π/2; 1: `a` = π/2; 2: `b` = π/2; 3: `b` = −π/2; 4: `a` = π; 5: none |
| 2 | 2π / n | `a` = f × fov + `+0x190` + π; scale and aspect from `0x01DF1B70` and `0x01DF1B74` (1.0 each) |
| 3 | `+0x1E0` degrees (180) / `+0x1E4` (3) | `a` = `+0x190`; `b` = −`+0x194`, or 0 while byte `0x01F811D0` is set; `c` = fov / 2 − span / 2 + π + f × fov |
| other | 2π | none |

`0x00189570`, run by the per-frame pump `0x0017D6E0` and by the render pass list `0x00187950`, asks
`0x001ACC30` and, on true, sets five cameras through `0x00185C30`:

- the render manager's cameras at `+0x690`, `+0x820`, `+0x358` and `+0x4E8`, with the controllers at
  `+0x798`, `+0x928`, `+0x460` and `+0x5F0`, and, while the camera pair's first byte is set, the
  pair's camera `0x0018A620() + 8` with the controller at `+0x9C8`;
- `0x00185C30` stores the fov at the camera's `+0xD0`, the scale at `+0xD4` and the aspect at `+0xC8`,
  attaches the controller (`0x00184AF0`) and hands it `a`, `b` and `c` through its slot `+0x50`.

`0x001AC950(object, out, view, view2)` runs every frame from `0x00189CE0` while the render manager's
byte `+0x1C` is clear. It copies the 3 × 4 matrix `view` into the 4 × 4 `out`: the fourth column
(`+0x0C`, `+0x1C`, `+0x2C`) as the first row, the three rows after it, 1.0 at `+0x3C`. `0x00189CE0`
passes `out` to `0x001941F0` when `0x0018E470` allows. The two matrices are the render manager's `+0xF8`
and `+0x288`, or the camera pair's `[+0xC0]` and `[+0x198]` while its first byte is set.

With a valid step (count not 2, step 0 or more) `0x001AC950` would first overwrite both matrices: first
row (0, −1, 0), second row (0, 0, −1), the third row kept and the fourth column (1, 0, 0).

### The console's camera override

While the camera pair's first byte is set, `0x00187950` and the render manager's camera query
`0x00186670` apply the console's camera rows to the pair's camera `0x0018A620() + 8`:

- with console byte `+0xC0C` set and the capture step below -1 or its count 2: the fov from
  `+0xC10` (row 104), the aspect from `+0xC14` (row 105) and the scale from `+0xC18` (row 106);
- in `0x00187950` only, with `+0xC0C` clear, byte `+0xC24` set and the step below -1: the fov from
  the cube-map object's `+0x1E8` (0.785).

Either way they then call `0x00189130(manager, camera, a, b, c)` with the console's `+0x00`, `+0x04`
and `+0xC1C`.

`0x00189130` rebuilds the 3 × 4 world matrix that the camera's `+0xB8` points to. It starts from axes
(1, 0, 0), (0, −1, 0) and (0, 0, −1) with the matrix's own `+0x20`, `+0x24` and `+0x28` as the last
row, multiplies in turn (`0x00185100`) by a rotation of `a` about (0, −1, 0), a rotation of `b` about
x, and a rotation of `c` about (0, −1, 0), and writes the result back. `0x00188E60(out, angle, axis)`
builds the rotation about a unit axis; `0x0062E1C0` uses it too.

None of this reaches the screen in a retail game. The console constructor `0x001CCB20` zeroes `+0x00`
and `+0x04` (`0x001CCB47`), writes `+0xC18` and `+0xC1C` as one qword with `+0xC1C` = 0 (`0x001CCC40`)
and clears `+0xC0C` (`0x001CCC25`) and `+0xC24` (`0x001CCC51`). Only the arms of rows 60 and 103 set
`+0xC0C`, and neither is a retail id:

- row 60 "Capture panorama" sets `+0xC28 = clamp(+0xC28 + step, 0, 12)`, `step` -1 when the arm's
  direction byte is set and +1 otherwise (`0x001D1F5A`-`0x001D1F89`); it sets `+0xC0C` when the value
  is 1 (`0x001D1F98`) and otherwise clears it (`0x001D1FA4`) and runs row 103's copy;
- row 103 "Camera Over Write" toggles `+0xC0C` (`0x001D2B07`); switching it off copies the render
  manager's `+0xCC4`, `+0xCC8` and `+0xCCC` into `+0xC10`, `+0xC14` and `+0xC18`.

No arm of `0x001D1660` writes `+0x00`, `+0x04`, `+0xC1C` or `+0xC24`.

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01F81428` | `void*` | the console object (0x10E8), from 0x001D50D0 |  |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0130` | `char*` | row labels | one per id at `+0x130` + id*8, ids 1-294 (`0x001D0390`) |
| `+0x0A70` | `u8` | open (always 0) |  |
| `+0x0A74` | `u32` | mode |  |
| `+0x0A88` | `...` | page |  |
| `+0x0A90` | `...` | row count |  |
| `+0x0AAC` | `i32` | weather-slot override |  |
| `+0x0AB4` | `u32` | field id for the code table |  |
| `+0x0C56` | `u8` | information page |  |
| `+0x10B0` | `...` | row of id 9 |  |
| `+0x10B4` | `...` | row of id 10 |  |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x008FCE00` | `u32[15][22]` | the page table (id, 0 = none) |  |
| `0x001D4C1C` | `u32[282]` | arm RVAs for ids 12-293; 0x001D4BFA the shared do-nothing arm; 0x001D4C09 the out-of-range arm |  |
| `0x01DF6E68` | `{char* code; u32 index+1; u32 0}[1314]` | the authored-code table (601 codes) |  |
| `0x01F832B0` | `u32[5]` | event-slot counts |  |
| `0x01F832E8` | `u8` | classification | with `0x01F832E9` |
| `0x01F832E9` | `u8` | classification | with `0x01F832E8` |
| `0x01F832F0` | `string[5]` | event-slot names, 0x20 each |  |
| `0x01F83390` | `vector[5]` | event-slot vectors, 0x20 each |  |
| `0x01DFE40C` | `i32` | slot marker |  |
| `0x01F82D20` | `void*` | the game-setting object the Config rows read |  |
| `0x022C7F90` | `u16` | display flag words | one per i at `0x022C7F90` + i*4 (`0x00358330`(i)); word 1 gates the menu draw |

`MultipleDebugDisplay`, `0x4670` bytes at `[0x01F81270]` (constructor `0x001C1D40`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000C` | `i32` | mode | 0 to 3, row 51 |
| `+0x0010` | `DebugLine[32]` | fixedLines | the fixed lines |
| `+0x4610` | `i32` | fixedCount | fixed lines queued |
| `+0x4618` | `DebugLine*` | overlayLines | vector of overlay lines |
| `+0x4638` | `i32` | overlayCount | overlay lines queued |
| `+0x463C` | `u8` | overlayOn | row 176 |
| `+0x4640` | `DebugLine*` | moreLines | a further vector of lines |
| `+0x4660` | `i32` | moreCount | its lines queued |
| `+0x4664` | `f32` | scaleX | -5.5, row 218 |
| `+0x4668` | `f32` | scaleY | -10.0, row 219 |

`DebugLine`, `0x230` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `f32` | x | position |
| `+0x004` | `f32` | y | position |
| `+0x008` | `char[256]` | text | the string |
| `+0x108` | `TextObject` | object | built by `0x001EA3C0` |

The capture fields of the cube-map object:

`CubeMapCapture` (`0x258` bytes, offsets from the start of the [0x01F811C8]):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A4` | `u8` | arm | lets `0x001AC7C0` move the step from -2 to -1; 0, written only by the constructor |
| `+0x0A8` | `i32` | step | -2; an even step of 0 or more selects face step / 2 |
| `+0x0B8` | `i32` | count | 12; 2 turns the capture off; n = count / 2 |
| `+0x0BC` | `i32` | mode | 1; 0 to 3 select the shape in `0x001ACC30` |
| `+0x190` | `f32` | angleA | base of the first angle in modes 2 and 3; 0 |
| `+0x194` | `f32` | angleB | the second angle in mode 3, negated; 0 |
| `+0x1E0` | `i32` | span | degrees covered in mode 3; 180 |
| `+0x1E4` | `i32` | slices | frames in mode 3; 3 |
| `+0x1E8` | `f32` | fov | 0.785; the console's `+0xC24` path |

The console fields the camera override reads:

`ConsoleCamera` (`0x10E8` bytes, offsets from the start of the [0x01F81428]):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `f32` | a | first angle for `0x00189130`; 0 |
| `+0x004` | `f32` | b | second angle; 0 |
| `+0xC0C` | `u8` | override rows 60 and 103 |  |
| `+0xC10` | `f32` | fov | row 104; 0.785 |
| `+0xC14` | `f32` | aspect | row 105; 1.778 |
| `+0xC18` | `f32` | scale | row 106; 1.155 |
| `+0xC1C` | `f32` | c | third angle; 0 |
| `+0xC24` | `u8` | capFov | takes the fov from the cube-map object; 0 |
| `+0xC28` | `i32` | panorama row 60, 0 to 12 |  |


## Shipped data

| Fact | Value |
|---|---|
| labels | 293 (ids 1 to 294, id 2 empty) |
| pages | 15 of up to 22 rows; page 14 the information page |
| command ids | 12 to 293 (282); 226 arms, 56 ids on the do-nothing arm |
| float-stepping arms | 110; 102 with one symmetric magnitude |
| retail ids | 16, from the Config screen's row kinds |
| authored codes | 601 of 1,314 entries |

## Operations

Per frame in the field: `0x0017DAA0` draws the menu only while `+0xA70` is set, which never
happens; the render pass list's `0x001D5520` the same. Per Config-screen press: `0x0017DB90` maps
the row to an id, `0x001D1660` runs the arm, `0x0017E070` reads the value back for the row.

## State

The console object, the page table and the arm table (both in the image), the game-setting
object, the display flag words, the event-slot arrays.

### The shared event-slot name

`0x01F832C8` is a static EASTL string (`+0x00` begin, `+0x08` end, `+0x10` capacity end). Its initialiser `0x0015DBB0`
sets it up without copying a text, and the destructor `0x008A72D0` frees it. `0x0020A760` empties it (`0x0020A787`) and
`0x0020AF10` assigns the slot's name to it through `0x001A5760` (`0x0020AF3E`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F832D8` | `void*` | 0 (zero-filled tail of `.data`) | `+0x10` capacity end of the shared event-slot name | `0x0015DBB0` (`0x0015DBEA`); `0x001A52A0` (`0x001A537F`), when `0x001A5760` grows it | `0x001A52A0` (`0x001A52BB`, `0x001A534C`, `0x001A535E`); `0x008A72D0` (`0x008A72DD`) |

No other instruction reaches this word: no other RIP-relative, image-base-relative or disp32 reference names it, and
the string's address is taken only at `0x0020AF3E`.

## Modding notes

- The concurrence override assumes the action numbering. `0x002F79E0` copies the eight action rows `0xF1`, `0xE7`,
  `0xEA`, `0xED`, `0xE5`, `0xE4`, `0xE3` and `0xE2` into `0x022BE930` from the 16-byte constant `0x00D0F9E0`, and `0x002F8D60` returns the one
  `0x01EEBAF0` selects in place of the concurrence the Quickening chain earned
  ([concurrence list](../Battle-Actions/concurrence-list.md)).
- The information row's names at `+0xB04` to `+0xBE4` follow the same order. Moving a concurrence to another
  action row needs both lists changed with it.
- The menu is one byte away: a write of 1 to `+0xA70` of the object at `[0x01F81428]` while the
  field frame runs (`0x00358330(1)` must hold, [frame update order](frame-update-order.md)) draws
  page `+0xA88`; the arms then need a caller, since no input code in the image dispatches a row
  from the menu.
- The arm table is in `.text` after the body and holds RVAs; the 56 ids on the do-nothing arm are
  free slots for new commands without growing the table, and the bound `0x119` at `0x001D167D` is
  the immediate to raise otherwise.
- A row's label names the field; the arm defines its type, step and range. Three adjacent rows
  labelled "Enable 100% successful steal / poach / drop" cycle four, three and five states.
- The gil row is not a cheat path of its own: it calls the setter every shop and reward uses, so
  the achievement counter behind it moves too: `0x00254EE0` calls `0x00316A50`
  ([achievements](../Steam-And-Achievements/achievements.md)).

## Related

- [Debug menu commands](debug-menu-commands.md): every id with its label, arm, kind and field.
- [Graphics settings](graphics-settings.md): the block most stepped fields live in.
- [Frame update order](frame-update-order.md): the draw block and the display flag.
- [Weather](../World-Areas-And-Travel/weather.md): the slot override at `+0xAAC`.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the codes in the authored-code table.
- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md): the setter the gil row calls.
