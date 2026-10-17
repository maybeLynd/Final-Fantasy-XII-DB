---
title: "Debug menu: the developer console object, its fifteen pages, its command dispatcher and the retail rows that still reach it"
kind: "system"
category: "Engine core"
addresses: "001D1660, 001D4C1C, 001D4BFA, 001D4C09, 001CD040, 0017DB90, 0017E070, 0023B330, 0023B6F0, 001D50D0, 001CCB20, 001D0390, 001CD0E0, 001D5260, 001D5520, 0017DAA0, 00187950, 001D0190, 008FCE00, 01DF6E68, 0017D490, 001A9930, 00193D50, 001DF340, 001DDAB0, 001C2F40, 003058B0, 00254EE0, 0020AC30, 0020AF10, 001EC560, 00358330, 0022A550, 01F82D20, 01DF6E48, 01F81270, 001C2F00, 001C1D40, 001C2120, 001EA3C0, 006CCCE0, 001C2980, 001C2D10, 00181F20, 00181E70, 001C2DB0, 001EA830, 001EAC60, 001EAE10, 0022FFE0, 00181FD0, 001820E0, 0020A760, 001EC4B0, 001C5040, 001EC500, 0050C8A0, 0050D0C0, 002E05E0, 00254FE0, 00255020, 001C5110, 001C0540, 001DCB90, 001DCD30, 0020DA50, 00308E80, 003091C0, 001C1C80, 001C1B00, 001C1A60, 001C1C00, 001C19A0, 0020AA50, 001ACC30, 001AC950, 00189130, 00188E60, 00189570, 001AC7C0"
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

`001D50D0()` returns the console settings object, created on first use (`00210EC0(10E8h)`, then
the constructor `001CCB20`) and cached at `01F81428`. The constructor zeroes and defaults the
object and calls `001D0390`, which stores the row labels when `001EA3C0(obj + 8)` returns 0,
noting that at `+A68`<sub>h</sub>: one string pointer per id at `+130h + id × 8` for ids 1 to 294 (id 2's
string is empty), 293 names in all.

`001D0390` also primes page 0 through the renderer, sets the text parameters and writes nine
32-byte strings at `+AE4`<sub>h</sub>, `+B04`<sub>h</sub> to `+BE4`<sub>h</sub> (`OFF`, `Black
Hole`, `Luminescence`, `Ark Blast`, `Whiteout`, `Windburst`, `Torrent`, `Cataclysm`, `Inferno`),
the concurrence names an information row prints.

Before those strings it runs `002F79E0` (`001D03DC`), which writes the eight words `F1`<sub>h</sub>, `E7`<sub>h</sub>, `EA`<sub>h</sub>, `ED`<sub>h</sub>,
`E5`<sub>h</sub>, `E4`<sub>h</sub>, `E3`<sub>h</sub> and `E2`<sub>h</sub> at `022BE930`. `002F8D60` returns word `[01EEBAF0]` of that table whenever
`01EEBAF0` is not negative.

The open byte `+A70`<sub>h</sub> is written once, to 0, by the constructor; no other instruction in the
image writes it. The page cursor is `+A88`<sub>h</sub>, the row count `+A90`<sub>h</sub>, the information-page flag
`+C56`<sub>h</sub>, the weather-slot override `+AAC`<sub>h</sub> (read through `0017D490` by the field runtime,
[weather](../World-Areas-And-Travel/weather.md)), and the field id for the code table `+AB4`<sub>h</sub>.

### The pages and the renderer

The page table at `008FCE00` holds 15 pages of 22 ids (0 = no row). `001D5260`, called from the
field frame's draw block through `0017DAA0` when `00358330(1)` holds ([frame update
order](frame-update-order.md)), returns at once unless `+A70`<sub>h</sub> is set; otherwise it prints `<Page
n/14>` or `<Information Page>` and, for every id on the page, has the row renderer `001CD0E0(ctx,
id, buffer)` format the row (`"None content!!"` when it prints nothing).

The information page (page 14) runs its ids through the filter `001D0190` first:

- ids 1, 2, 6, 9, 102, 204, 221, 222 and 290 always;
- 7 only while an event slot holds queued events (`01DFE40C`, the slot of the most recent
  `startscene` push, at most 4 and its counter at `01F832B0` non-zero; `0020AF10` sets it and
  `0020AC30` leaves it at -1);
- 8 only while the save-load manager at `01F81258` has its byte `+9` set;
- 10 only while `0022A550()` holds (main-loop state 2 with `00358330(1)`);
- 101 only while `+A74`<sub>h</sub> is 2; any other id is dropped.

`001D5520`, called from the render pass list `00187950`, redraws rows 9 and 10 of the information
page at their remembered positions `+10B0`<sub>h</sub> / `+10B4`<sub>h</sub>.

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

The renderer prints the label from `+130h + id × 8` and the row's value with `"%s%s%f"`. Its
read-out rows use two more tables:

- the authored-code table at `01DF6E68`, 1,314 records of 16 bytes (`char* code, u32 index + 1,
  u32 0`; 601 codes such as `ous0101`, the map pack of the field with that index, [MPK map
  pack](../World-Areas-And-Travel/mpk-map-pack.md)), indexed by the field id at `+AB4`<sub>h</sub>;
- the event-slot panel: five slots whose names (`01F832F0 + slot × 20h`), queued event counts
  (`01F832B0`) and classification bytes (`01F832E8` for a `sum_` name containing `0001`,
  `01F832E9` for a `spc_` name) the setter `0020AC30` and the pusher `0020AF10` maintain from
  the `plan_master\<locale>\event\` paths the resource loads hand them.

The setter's test that a path has that form is `0020A800`, a `std::regex` match
([MSVC containers](../Compiler-And-C-Runtime/msvc-containers.md),
story and events).

The setter takes the slot's name from the path with `0020AA50(out, path)`: the text between the last
`\` and the last `.`, the event file's name without its extension.

`0020A760(slot)` empties a slot. For a slot below 5 it clears the shared name `01F832C8`, the
slot's name, its vector `01F83390 + slot × 20h` and its count; in every case it leaves the marker
`01DFE40C` at -1. The setter `0020AC30` calls it, and so does `001EC4B0` (from `00360120` and from
`00356D40`, the begin of `eventdispose_f2`), which then raises the byte `01FD3AE3` (`00214B30`).

On that byte `00214C30` runs `001C5040`, which empties `01F812A8`, clears the two scene maps of the
current index `01F813F8` (`01F813A8` and `01F813D8`, through `00202880`) and sets that index's
words at `01F81400` and `01F81408` to -1. Script call `5C9`<sub>h</sub> (`00352F00`) pushes `001EC500()`, the
queued count of the marked slot, or 0 when none is marked.

### The read-out rows

Several rows print a live value that the renderer `001CD0E0` gathers itself:

| Row | Label | What the renderer prints |
|---|---|---|
| 2 | (information) | the frame rates and the background, with the loaded map `00314910()` (payload `+105C`<sub>h</sub>, [zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) and the story-progress word `00265270()` as its `(%d/%d)`, and, with an event slot marked, `event:` with the slot's name from `001C5110` (the name at `01F832F0 + slot × 20h`, empty without a marked slot) |
| 7 | (information) | `CutSceneName: %s Cut: %d(id: %d) Frame: %d`: the slot name (`001C5110`), its queued count, the last entry of its vector `01F83390`, and the counter `01F832C4` |
| 8 | (information) | for the picked object of `001C0DA0()` while its byte `+9` is set and the information page is open: its name (`001C0330`: `Disabled`, `NULL` or its own), its mesh texture (`001C0540`), its procedural texture (`001C0480`) and its tiling and blending values |
| 57 | Operate cube map | `001AD440()` `+168`<sub>h</sub> through `0017F5E0` (-1 without the object), marked `NOT EDITABLE` unless its `+40`<sub>h</sub> is 1 |
| 59 | Recapture cube maps | the status string `001AC7A0` picks: `+204h + [+200h] × 20h` of the cube-map object |
| 102 | Current GPU Temperature | the current adapter's temperature, `%d(C)` (below) |
| 220 | Extra BGM status | `0017E010`: `Not forced`, `Forced on` or `Forced off` from `01DF0018` by `01DF0010` |
| 222 | Control character position | `x:%f, y:%f, z:%f` from `003091C0`: the position (`00265020`) of the actor `00263750(003272F0())` when `00265970` holds; `003272F0` is the party leader's roster slot ([party leader](../Party/party-leader.md)) and the call goes through `0031ABF0`, a jump to `00263750` |
| 246 | Chara Name | `(%d) %s`: `00308E80(i)` gives a name from the record that `022C24E0 + i × 8` points to: its byte `+4`, below 6, picks one of `Vaan`, `Ashe`, `Fran`, `Balthier`, `Basch`, `Penelo` at `01EEC268`; otherwise `Nobody` |
| 264 | Game Display Resolution | `001DCD30`: `%d X %d ,%dHz, %dHz`, the configured resolution (`[01F82D20]` `+04`<sub>h</sub> / `+06`<sub>h</sub> with `+08`<sub>h</sub> set, else `+2C`<sub>h</sub> / `+2E`<sub>h</sub>), the desktop's refresh rate (`EnumDisplaySettingsW`) and the selected mode's rate; then `Screen Resolution :%dx%d` from `GetSystemMetrics` |
| 266 | System Adapter | `001DCB90`: ` Count %d ,Now: %s ,Video Memory: %lld MB, Temperature: %d(C)`, the memory being the adapter's `+110`<sub>h</sub> divided by 1,000,000 |
| 290 | Game Time Stop is | `Off` while the running byte `[0018A7D0()]` is 0; else `On by Debug` when its second byte is set (`0018A790`), `On by Focus` when its third is (`0018A7B0`), else the third string at `008FFF08` |

For row 8, `001C0540` asks the map-art context: `001A74A0` finds the object's `+260`<sub>h</sub> in the map at
`+448`<sub>h</sub>, takes the name at the entry's `+40`<sub>h</sub>, and keeps the part after the last `/` minus its
last ten characters. `001C0480` copies the string at `+80`<sub>h</sub> of the first entry of the object's
`+18`<sub>h</sub> list (`001E3E90`) with `001BE660`.

Rows 102 and 266 query the graphics vendors' libraries. The current adapter is the record at
`+78h + [+48h] × 140h` of the `001DDAB0` object (`001DC9C0`), and `0020D2B0` builds a chain of
`AdapterInfos` providers whose head sits on the stack and whose second link is the static
provider at `01E02580`. `0020DA50` asks each provider in turn (vtable slot 0) for the
temperature of the adapter id at the record's `+104`<sub>h</sub> until one answers, and `0020D9F0` asks the
same way (slot 1) for the name. `001DCB90` falls back to the record's own name (`+00`<sub>h</sub>).

### The dispatcher

`001D1660(ctx, dir, !dir, id)` is 13,753 bytes long. At
`001D166F` it subtracts 12 from the id, refuses anything above 281 unsigned (so ids below 12 too)
with the do-nothing arm `001D4C09`, and jumps through a 282-entry table of image-relative
offsets at `001D4C1C`, placed right after the body: arm = `120000h + table[id - 12]`. The 282
entries name 227 distinct targets, 226 arms and the shared do-nothing arm `001D4BFA` that 56 ids
share; 212 of the arms end in a jump to it. Valid ids are 12 to 293, so ids 1 to 11 are label-only
rows.

The arms are small. 110 step a float: `movss` the field, `test bl, bl` (the direction), `subss`
or `addss` by one constant from the float pool, `movss` back. 102 of them have one magnitude,
symmetric in both directions: 0.01 for 58 arms, 0.02 for 11, 0.05 for 10, 0.1 for 9, 0.001 for
7, 0.03 for 3, 1.0 for 2, 0.5 and 0.005556 for one each. The sign composes from the mnemonic and
the constant's own sign (`+0.01` at `008F30E4`, `-0.01` at `009002F4`).

The rest call a subsystem, step an integer with a wrap, toggle a byte or cycle a mode; the table
on [debug menu commands](debug-menu-commands.md) gives every id. The shared helpers are
singleton getters: `001A9930` (`01F81168`), `00193D50` (the `4A8`<sub>h</sub> post-process parameter object
at `01F7F5F0`), `001DDAB0` (`01F82D18`), `001C2F40` (`01F81270`), the game-setting object pointer
`01F82D20` loaded in 18 arms, and the indexed store `001DF340(obj, i, v)`.

Rows 205 to 207 (Music, Voice, Sound Effect) set the music, voice and sound-effect category
volume to 1.0 or 0 through `001DBB00`, and row 217 steps the 3D sound behind ratio with the
getter `002DEBA0` and the setter `002DF2A0` ([audio manager](../Sound-And-Music/audio-manager.md)).

Most stepped fields are in the render settings block ([graphics settings](graphics-settings.md)); the gil row is
`003058B0`, which hands 99,999,999 to the ordinary setter `00254EE0`
([gil](../Rewards-EXP-Gil-And-Loot/gil.md)).

### Who reaches the dispatcher

`001D1660` has one caller (the data references at `01D5D550` and `01D5D560` are exception
records, not a call table), the adapter `001CD040(ctx, dir, id)`, whose one caller is `0017DB90`,
whose two callers are the message procedures `0023B330` and `0023B6F0` of the retail Config
screen's rows. `0017DB90(kind, value, dir)` maps a row kind to a console id and dispatches it,
then returns the row's new value from `0017E070(kind)`, a read of `[01F82D20] + offset`:

| Row kind | Console id | Label | Value read |
|---|---|---|---|
| 1 | `11B`<sub>h</sub> | Apply Graphic Quality Default | `+0C`<sub>h</sub> |
| 4 | `10A`<sub>h</sub> | System Adapter | `001DDAB0() + 48h` |
| 7 | `110`<sub>h</sub> | Brightness | `+10`<sub>h</sub> |
| 8 | `111`<sub>h</sub> | Vsync | `+14`<sub>h</sub> |
| 9 | `11C`<sub>h</sub> | BackBufferCount | `+44`<sub>h</sub> |
| 10 | `11D`<sub>h</sub> | Frame Limit | `+48`<sub>h</sub> |
| 12 | `112`<sub>h</sub> | Anisotropic filtering | `+18`<sub>h</sub> |
| 13 | `86`<sub>h</sub> | Water Quality | `+40`<sub>h</sub> |
| 15 | `113`<sub>h</sub> | Shadows Quality | `+1C`<sub>h</sub> |
| 16 | `114`<sub>h</sub> | Character self-shadow | `+3C`<sub>h</sub> |
| 18 | `115`<sub>h</sub> | Anti-aliasing | `+20`<sub>h</sub> |
| 19 | `116`<sub>h</sub> | Post process AA | `+24`<sub>h</sub> |
| 20 | `117`<sub>h</sub> | Ambient Occlusion | `+28`<sub>h</sub> |
| 21 | `118`<sub>h</sub> | Depth of Field | `+30`<sub>h</sub> |
| 22 | `119`<sub>h</sub> | Glare | `+34`<sub>h</sub> |
| 23 | `A6`<sub>h</sub> | Use soft particle | `+38`<sub>h</sub> |

Kinds 5 and 6 do not dispatch: 5 runs `001DC940` on the `001DDAB0` object and `001DC730` when
`[01F82D20] + 8` is 0, and 6 cycles its value through 0, 1, 2. So sixteen of the 282 ids are
retail, reached from the Config screen; the other 266 have no caller in the shipped game, and
the menu that would reach them never opens.

Two console bytes are read by input code instead of a menu arm. While `+C3D`<sub>h</sub> (row 293, "Key
Board Debug For Japanese Keyboard") is set, the control-code lookups `00197790` and `00197800`
use the 106-entry table `01DF1030` in place of `01DF0E80`, and while `+C35`<sub>h</sub> (row 187, "Enable
mouse control camera") is set the input translator `00197160` calls `GetForegroundWindow` at
`001973DA` ([on-screen keyboard](../Controls-And-Input/on-screen-keyboard.md), [controls](../Controls-And-Input/controls.md)).

### The debug script verbs

The verb table keeps a family of `debug_` calls that event scripts could issue. Their handlers in the
shipped game:

| Verb | Handler | What it does |
|---|---|---|
| `debug_mapjump` `2026`<sub>h</sub> | `0050C8A0` | `00314440(map, 0, 0, 0)`, the map-jump funnel ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)), then `00314D60(1)`, which stores 0 in `022C2540` because its gate, the stub `005C5230`, returns 0 |
| `debug_eventload` `202D`<sub>h</sub> | begin `0050D030`, poll `0050D0C0` | kind 4 goes to `00314410(id)`, which, while `01EED060` is negative, requests a teardown (`0026A5F0(4)`) and stores the id there; any other kind is the scene load request `0032FC30(kind, id)`; the poll holds while `0032E520(1)` reports a load |
| `debug_isnewcharsep` `2070`<sub>h</sub> | `0050CAD0` | pushes `003A1640(v)`, which is `v < -1` |
| `debug_isopen_total_menu` `2085`<sub>h</sub> | `0050D200` | pushes `002E05A0()`: the menu mode `02092730` is neither 0 nor 5 |
| `debug_isopen_menu` `2081`<sub>h</sub> | `0050D220` | pushes `002E05E0()`: the same, or any of the 8 records at `0215F200` (stride `68`<sub>h</sub>) live with its byte `+38`<sub>h</sub> or bit 0 of `+3E`<sub>h</sub> set |
| `debug_switchstatusdisplay` `2036`<sub>h</sub> | `0050DA20` | jumps to `002E2290`, which jumps to `00255020`: flips `020927E8` and hands it to `00251F40`, which returns at once while bits 6 and 7 of `01E0C320` are both set, and otherwise runs one set of calls for a positive value and another for 0 |
| `debug_switchmonsterhpgauge` `206A`<sub>h</sub> | `0050C890` | jumps to `00254FE0`: flips `01E0C2A8` and hands it to `0028FFE0(0, v)`, as 0 while bit 10 of `002E0FA0()` is set |

### The debug text display

The rows that print text in the 3D view do it through the `MultipleDebugDisplay` singleton at
`01F81270` (getter `001C2F40`). `001C2F00` allocates its `4670`<sub>h</sub> bytes and runs the constructor
`001C1D40`; `001C2120` is the destructor body and `001C2670` the deleting wrapper. The start-up
step `0017D6B0` makes the call to `001C2F00` ([game application](game-application.md)). A line
is a `230`<sub>h</sub>-byte record: x and y floats, a 256-byte text buffer at `+08`<sub>h</sub> and a text object at `+108`<sub>h</sub>.

The constructor builds 32 fixed records at `+10`<sub>h</sub> and prepares each text object with `001EA3C0`.
That loads `PhyreText.fx` and the font `tuffysdf.fgen` (the two paths at `01DFDE00`), binds the
technique `RenderText_SoftEdges` (`006CCCE0` looks it up by name from the table at `00D89BE0` and
caches it), writes `"Debug Info:"`.

It sizes the glyph arrays for 128 entries (`0067C310`, which
grows them with `00672B80` and `00672C70`). The constructor then calls `001EAA90(object, 1280, 720)` on each
and leaves the mode `+0C`<sub>h</sub> at 0, the overlay byte `+463C`<sub>h</sub> at 0, and the scales
`+4664`<sub>h</sub> / `+4668`<sub>h</sub> at -5.5 and -10.0.

`001C2980(display, line, kind)` queues a line. Both kinds map the position through `001C2D10`
(x × `+4664`<sub>h</sub> - 1.65, y × `+4668`<sub>h</sub> - 2.0), hand the text to the object (`001EADB0`, `001EAD20`) and
mark it visible (`001EAEA0`):

- kind 0, from `00181F20` (the character-name printer `0053AB50`): taken only while the mode is
  non-zero and fewer than 32 fixed lines are queued (`+4610`<sub>h</sub>);
- in mode 2 kind 0 drops lines that start with `W`; in mode 3 it keeps only lines that start with
  `C`, `M` or `N` (either case); a kind-0 line that starts with `H` or `M` gets 1 added to its y,
  one with `G` gets 2;
- kind 1, from `00181E70`: taken only while `+463C`<sub>h</sub> is set, appended to the vector at `+4618`<sub>h</sub>
  (count `+4638`<sub>h</sub>). The vector grows through `001C2D50` and `001C2790`, which copy records with
  `001C1B00`, `001C1C80`, `001C2230`, `001C1E70` and `0067ACF0`.

Growing a vector copies `DebugLine` records. `001C1C80(dst, src)` copy-constructs one: x, y and the
256-byte text, then the text object through `001C1E70`. `001C1B00(out, first, last, dest)` does the
same for a range into new storage, `230`<sub>h</sub> bytes apart, and `001C1A60(first, last, destEnd)`
copy-assigns a range backward, the text object through `001C22A0`.

Both text-object copies take the
object's array of strings with `001C1C00(dst, src)`: a new array of the same count (the low 31 bits
of its count word) from `0017D260`, and `001C19A0(dst, src, n)` duplicates each string into its own
block, its source pointer read with bit 0 cleared.

The render pass list `00187950` calls `001C2DB0`, which draws the fixed lines while the mode is set,
the overlay lines while `+463C`<sub>h</sub> is set, and the lines of the vector at `+4640`<sub>h</sub> (count
`+4660`<sub>h</sub>), then zeroes the counts.

Each line goes through `001EA830`: when the object is visible
(`+EA`<sub>h</sub>) and built (`+20`<sub>h</sub>) it draws the string in black at its position plus the offset
`+100`<sub>h</sub> to `+108`<sub>h</sub>, then in white at its position, both through `001EAC60`, which writes the
placement into the material at `+208`<sub>h</sub> to `+234`<sub>h</sub>. `001EAE10` releases a text object: its material (`001EA050`),
its glyph object (`0067B3A0`) and its two assets (`0019CC50`). `001EA130`, reached from
the unwind handlers `0089873C` and `0089E880`, frees a counted array the same way `001EA050` does.

Four console rows drive it. Row 51 "Draw Chr Names" cycles the mode through 0 to 3 (`001D5230`).
Rows 218 and 219 step `+4664`<sub>h</sub> and
`+4668`<sub>h</sub> by 0.1. Row 176 "Show Map Hide Group" sets `+463C`<sub>h</sub> (`001D2C08`), which makes the pump run
`0022FFE0`.

`0022FFE0`
walks the cells of the collision grid `0026E500(0)`, draws a four-vertex quad over each cell and prints at its
centre the list of eight-bit group numbers found in the cell's polygon attribute words
(`"%d, %s"`). It places the text with `00181FD0` and `001820E0`, which multiply a point by the
first (`+08`<sub>h</sub>) and second (`+78`<sub>h</sub>) matrix of the camera block: the camera pair's (`0018A620`)
while its first byte is set, else the render manager's `+690`<sub>h</sub>.

### The cube-map capture camera

The cube-map object (`001AD440`, `258`<sub>h</sub> bytes at `[01F811C8]`) carries a developer capture: a step
that would point the render manager's cameras at each face of a cube, or around a panorama, one
step per frame. Console rows 56 "Capture cube map" and 59 "Recapture cube maps" name it (labels
stored at `001D07FE` and `001D0828`). The capture never runs in the shipped game.

The step `+A8`<sub>h</sub> is set to -2 by the constructor `001AA9E0` (`001AAA5C`). The only other store,
`001AC7D6` in `001AC7C0`, sets it to -1 when the step is -2 and byte `+A4`<sub>h</sub> is set, and `+A4`<sub>h</sub> is
written only by the constructor, with 0 (`001AAA55`). The step stays at -2.

`001ACC30(object, &fov, &scale, &aspect, &a, &b, &c)` turns the step into a camera. It returns false
and writes nothing when the count `+B8`<sub>h</sub> is 2 or the step is negative or odd. Otherwise it writes the
defaults (fov 2π, scale and aspect 1, the angles 0), takes `n` = count / 2 and the face `f` = step / 2,
and continues by the mode `+BC`<sub>h</sub>:

| Mode | fov | Angles |
|---|---|---|
| 0, 1 | 2π / (n − 2), 90° for the constructor's count of 12 | face 0: `a` = −π/2; 1: `a` = π/2; 2: `b` = π/2; 3: `b` = −π/2; 4: `a` = π; 5: none |
| 2 | 2π / n | `a` = f × fov + `+190`<sub>h</sub> + π; scale and aspect from `01DF1B70` and `01DF1B74` (1.0 each) |
| 3 | `+1E0`<sub>h</sub> degrees (180) / `+1E4`<sub>h</sub> (3) | `a` = `+190`<sub>h</sub>; `b` = −`+194`<sub>h</sub>, or 0 while byte `01F811D0` is set; `c` = fov / 2 − span / 2 + π + f × fov |
| other | 2π | none |

`00189570`, run by the per-frame pump `0017D6E0` and by the render pass list `00187950`, asks
`001ACC30` and, on true, sets five cameras through `00185C30`:

- the render manager's cameras at `+690`<sub>h</sub>, `+820`<sub>h</sub>, `+358`<sub>h</sub> and `+4E8`<sub>h</sub>, with the controllers at
  `+798`<sub>h</sub>, `+928`<sub>h</sub>, `+460`<sub>h</sub> and `+5F0`<sub>h</sub>, and, while the camera pair's first byte is set, the
  pair's camera `0018A620() + 8` with the controller at `+9C8`<sub>h</sub>;
- `00185C30` stores the fov at the camera's `+D0`<sub>h</sub>, the scale at `+D4`<sub>h</sub> and the aspect at `+C8`<sub>h</sub>,
  attaches the controller (`00184AF0`) and hands it `a`, `b` and `c` through its slot `+50`<sub>h</sub>.

`001AC950(object, out, view, view2)` runs every frame from `00189CE0` while the render manager's
byte `+1C`<sub>h</sub> is clear. It copies the 3 × 4 matrix `view` into the 4 × 4 `out`: the fourth column
(`+0C`<sub>h</sub>, `+1C`<sub>h</sub>, `+2C`<sub>h</sub>) as the first row, the three rows after it, 1.0 at `+3C`<sub>h</sub>. `00189CE0`
passes `out` to `001941F0` when `0018E470` allows. The two matrices are the render manager's `+F8`<sub>h</sub>
and `+288`<sub>h</sub>, or the camera pair's `[+C0h]` and `[+198h]` while its first byte is set.

With a valid step (count not 2, step 0 or more) `001AC950` would first overwrite both matrices: first
row (0, −1, 0), second row (0, 0, −1), the third row kept and the fourth column (1, 0, 0).

### The console's camera override

While the camera pair's first byte is set, `00187950` and the render manager's camera query
`00186670` apply the console's camera rows to the pair's camera `0018A620() + 8`:

- with console byte `+C0C`<sub>h</sub> set and the capture step below -1 or its count 2: the fov from
  `+C10`<sub>h</sub> (row 104), the aspect from `+C14`<sub>h</sub> (row 105) and the scale from `+C18`<sub>h</sub> (row 106);
- in `00187950` only, with `+C0C`<sub>h</sub> clear, byte `+C24`<sub>h</sub> set and the step below -1: the fov from
  the cube-map object's `+1E8`<sub>h</sub> (0.785).

Either way they then call `00189130(manager, camera, a, b, c)` with the console's `+00`<sub>h</sub>, `+04`<sub>h</sub>
and `+C1C`<sub>h</sub>.

`00189130` rebuilds the 3 × 4 world matrix that the camera's `+B8`<sub>h</sub> points to. It starts from axes
(1, 0, 0), (0, −1, 0) and (0, 0, −1) with the matrix's own `+20`<sub>h</sub>, `+24`<sub>h</sub> and `+28`<sub>h</sub> as the last
row, multiplies in turn (`00185100`) by a rotation of `a` about (0, −1, 0), a rotation of `b` about
x, and a rotation of `c` about (0, −1, 0), and writes the result back. `00188E60(out, angle, axis)`
builds the rotation about a unit axis; `0062E1C0` uses it too.

None of this reaches the screen in a retail game. The console constructor `001CCB20` zeroes `+00`<sub>h</sub>
and `+04`<sub>h</sub> (`001CCB47`), writes `+C18`<sub>h</sub> and `+C1C`<sub>h</sub> as one qword with `+C1C`<sub>h</sub> = 0 (`001CCC40`)
and clears `+C0C`<sub>h</sub> (`001CCC25`) and `+C24`<sub>h</sub> (`001CCC51`). Only the arms of rows 60 and 103 set
`+C0C`<sub>h</sub>, and neither is a retail id:

- row 60 "Capture panorama" steps `+C28`<sub>h</sub> and clamps it to 0 to 12; it sets `+C0C`<sub>h</sub> when the value
  is 1 (`001D1F98`) and otherwise clears it (`001D1FA4`) and runs row 103's copy;
- row 103 "Camera Over Write" toggles `+C0C`<sub>h</sub> (`001D2B07`); switching it off copies the render
  manager's `+CC4`<sub>h</sub>, `+CC8`<sub>h</sub> and `+CCC`<sub>h</sub> into `+C10`<sub>h</sub>, `+C14`<sub>h</sub> and `+C18`<sub>h</sub>.

No arm of `001D1660` writes `+00`<sub>h</sub>, `+04`<sub>h</sub>, `+C1C`<sub>h</sub> or `+C24`<sub>h</sub>.

## Layouts

```
01F81428  ptr  the console object (0x10E8), from 001D50D0
  +0x130 + id*8  char*  row labels, ids 1-294 (001D0390)
  +0xA70  u8  open (always 0)   +0xA74  u32 mode   +0xA88  page   +0xA90  row count   +0xAAC  i32 weather-slot override
  +0xAB4  u32 field id for the code table   +0xC56  u8 information page   +0x10B0 / +0x10B4  rows of ids 9 and 10
008FCE00  u32[15][22]  the page table (id, 0 = none)
001D4C1C  u32[282]  arm RVAs for ids 12-293; 001D4BFA the shared do-nothing arm; 001D4C09 the out-of-range arm
01DF6E68  {char* code; u32 index+1; u32 0}[1314]  the authored-code table (601 codes)
01F832B0  u32[5] event-slot counts   01F832E8 / 01F832E9  u8 classification   01F832F0  string[5]   01F83390  vector[5]   01DFE40C  i32 slot marker
01F82D20  ptr  the game-setting object the Config rows read
022C7F90 + i*4  u16  display flag words (00358330(i)); word 1 gates the menu draw
```

`MultipleDebugDisplay`, `4670`<sub>h</sub> bytes at `[01F81270]` (constructor `001C1D40`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000C`<sub>h</sub> | `i32` | mode | 0 to 3, row 51 |
| `0010`<sub>h</sub> | `DebugLine[32]` | fixedLines | the fixed lines |
| `4610`<sub>h</sub> | `i32` | fixedCount | fixed lines queued |
| `4618`<sub>h</sub> | `DebugLine*` | overlayLines | vector of overlay lines |
| `4638`<sub>h</sub> | `i32` | overlayCount | overlay lines queued |
| `463C`<sub>h</sub> | `u8` | overlayOn | row 176 |
| `4640`<sub>h</sub> | `DebugLine*` | moreLines | a further vector of lines |
| `4660`<sub>h</sub> | `i32` | moreCount | its lines queued |
| `4664`<sub>h</sub> | `f32` | scaleX | -5.5, row 218 |
| `4668`<sub>h</sub> | `f32` | scaleY | -10.0, row 219 |

`DebugLine`, `230`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `f32` | x | position |
| `004`<sub>h</sub> | `f32` | y | position |
| `008`<sub>h</sub> | `char[256]` | text | the string |
| `108`<sub>h</sub> | `TextObject` | object | built by `001EA3C0` |

The capture fields of the cube-map object:

`CubeMapCapture` (`258`<sub>h</sub> bytes, offsets from the start of the [01F811C8]):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0A4`<sub>h</sub> | `u8` | arm | lets `001AC7C0` move the step from -2 to -1; 0, written only by the constructor |
| `0A8`<sub>h</sub> | `i32` | step | -2; an even step of 0 or more selects face step / 2 |
| `0B8`<sub>h</sub> | `i32` | count | 12; 2 turns the capture off; n = count / 2 |
| `0BC`<sub>h</sub> | `i32` | mode | 1; 0 to 3 select the shape in `001ACC30` |
| `190`<sub>h</sub> | `f32` | angleA | base of the first angle in modes 2 and 3; 0 |
| `194`<sub>h</sub> | `f32` | angleB | the second angle in mode 3, negated; 0 |
| `1E0`<sub>h</sub> | `i32` | span | degrees covered in mode 3; 180 |
| `1E4`<sub>h</sub> | `i32` | slices | frames in mode 3; 3 |
| `1E8`<sub>h</sub> | `f32` | fov | 0.785; the console's +`C24`<sub>h</sub> path |

The console fields the camera override reads:

`ConsoleCamera` (`10E8`<sub>h</sub> bytes, offsets from the start of the [01F81428]):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `f32` | a | first angle for `00189130`; 0 |
| `004`<sub>h</sub> | `f32` | b | second angle; 0 |
| `C0C`<sub>h</sub> | `u8` | override rows 60 and 103 |  |
| `C10`<sub>h</sub> | `f32` | fov | row 104; 0.785 |
| `C14`<sub>h</sub> | `f32` | aspect | row 105; 1.778 |
| `C18`<sub>h</sub> | `f32` | scale | row 106; 1.155 |
| `C1C`<sub>h</sub> | `f32` | c | third angle; 0 |
| `C24`<sub>h</sub> | `u8` | capFov | takes the fov from the cube-map object; 0 |
| `C28`<sub>h</sub> | `i32` | panorama row 60, 0 to 12 |  |


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

Per frame in the field: `0017DAA0` draws the menu only while `+A70`<sub>h</sub> is set, which never
happens; the render pass list's `001D5520` the same. Per Config-screen press: `0017DB90` maps
the row to an id, `001D1660` runs the arm, `0017E070` reads the value back for the row.

## State

The console object, the page table and the arm table (both in the image), the game-setting
object, the display flag words, the event-slot arrays.

## Modding notes

- The menu is one byte away: a write of 1 to `+A70`<sub>h</sub> of the object at `[01F81428]` while the
  field frame runs (`00358330(1)` must hold, [frame update order](frame-update-order.md)) draws
  page `+A88`<sub>h</sub>; the arms then need a caller, since no input code in the image dispatches a row
  from the menu.
- The arm table is in `.text` after the body and holds RVAs; the 56 ids on the do-nothing arm are
  free slots for new commands without growing the table, and the bound `119`<sub>h</sub> at `001D167D` is
  the immediate to raise otherwise.
- A row's label names the field; the arm defines its type, step and range. Three adjacent rows
  labelled "Enable 100% successful steal / poach / drop" cycle four, three and five states.
- The gil row is not a cheat path of its own: it calls the setter every shop and reward uses, so
  the achievement counter behind it moves too: `00254EE0` calls `00316A50`
  ([achievements](../Steam-And-Achievements/achievements.md)).

## Related

- [Debug menu commands](debug-menu-commands.md): every id with its label, arm, kind and field.
- [Graphics settings](graphics-settings.md): the block most stepped fields live in.
- [Frame update order](frame-update-order.md): the draw block and the display flag.
- [Weather](../World-Areas-And-Travel/weather.md): the slot override at `+AAC`<sub>h</sub>.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the codes in the authored-code table.
- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md): the setter the gil row calls.
