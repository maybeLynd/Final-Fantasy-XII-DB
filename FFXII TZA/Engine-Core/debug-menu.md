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

When the player changes one of these Config rows, the game turns the row into one of the menu's command numbers, runs
that command's step on the setting, then reads the new setting back to show beside the row. The other 266 commands
have nothing in the retail game that reaches them.

## How it works

### The console object

`0x001D50D0()` returns the console settings object, created on first use (`0x00210EC0(0x10E8)`, then
the constructor `0x001CCB20`) and cached at `0x01F81428`; a failed allocation skips the constructor and caches 0
(`0x001D50FB`, `0x001D5106`). The constructor zeroes and defaults the
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

The information page (page 14) runs its ids through the filter `0x001D0190(ctx, id, buffer)` first. An id that
passes is rendered by the filter itself, `0x001CD0E0(ctx, id, buffer)`, and the filter returns 1 (`0x001D021B`,
`0x001D024F`, `0x001D0274`); a dropped id returns 0 with no call (`0x001D01F8`). The arms come from the byte table at
`0x001D02A4` and the offsets at `0x001D028C`:

- ids 1, 2, 6, 9, 102, 204, 221, 222 and 290 always;
- 7 only while an event slot holds queued events (`0x01DFE40C`, the slot of the most recent
  `startscene` push, at most 4 and its counter at `0x01F832B0` non-zero; `0x0020AF10` sets it and
  `0x0020AC30` leaves it at -1);
- 8 only while the procedural-texture context `0x001C0DA0()` (`[0x01F81258]`,
  [map art](../World-Areas-And-Travel/map-art.md)) is not 0 and has its byte `+9` set (`0x001D023A`, `0x001D0241`);
- 10 only while `0x0022A550()` holds (main-loop state 2 with `0x00358330(1)`);
- 101 only while `+0xA74` is 2; any other id is dropped, ids above 290 included (`0x001D01AD`).

Page 14's own list in the table below holds id 3, which the filter drops, and does not hold ids 1 and 7, which
the filter passes.

`0x001D5520`, called from the render pass list `0x00187950`, redraws rows 9 and 10 of the information page at their
remembered positions `+0x10B0` / `+0x10B4`. It returns at once unless the open byte `+0xA70` and the information-page
flag `+0xC56` are both set (`0x001D553B`, `0x001D554B`).

A row whose position is -1 is skipped (`0x001D5558`, `0x001D5599`); otherwise the renderer formats it into a cleared
256-byte buffer (`0x001CD0E0(ctx, 9 or 10, buffer)`) and `0x001EA380(obj + 8, position, buffer)` puts that text into
string `position` of the menu's text object (`0x001EAD40`, then its byte `+0xE8` = 1), or hands it to `0x001EA1E0` when
`position` is not below the object's string count.

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
  `0x01F832E9` for a `spc_` name without `sum_`, both cleared by the setter on every call) the setter
  `0x0020AC30` keeps from the `plan_master\<locale>\event\` paths the resource loads hand it, and whose
  counts the pusher `0x0020AF10` raises.

The setter's test that a path has that form is `0x0020A800`, a `std::regex` match
([MSVC containers](../Compiler-And-C-Runtime/msvc-containers.md),
story and events).

The setter takes the slot's name from the path with `0x0020AA50(out, path)`: the text between the last
`\` and the last `.`, the event file's name without its extension (`0x0020AB60`-`0x0020ABE5`). A path without a `\`
gives its text from the first character, and one without a `.` after its last `\` gives its text to the end: the
length `0x001A9E50` receives is cut to what remains of the path (`0x001A9E7F`).

The setter first clears both classification bytes (`0x0020AC56`, `0x0020AC5D`) and marks the slot (`0x0020AC64`). It
compares the new name with the slot's (length, then `memcmp` at `0x0020ACCB`) and stops when they are equal, so a
repeated name leaves both bytes at 0. A new name is copied into the slot (`0x001A5760`, `0x0020AD07`), and a `sum_`
name also has `<name>.json` loaded through `0x001C5750` (`0x0020AD6A`) before its `0001` test.

`0x0020AF10(slot, value)` is the pusher. It copies the slot's name into the shared name `0x01F832C8` (`0x001A5760`,
`0x0020AF56`) and stores the slot in the marker `0x01DFE40C` (`0x0020AF5B`), both before it tests the slot. For a slot above
4 (unsigned), a value of -1 or an empty slot name it stops there, leaving the marker on that slot; otherwise it
appends the value to the slot's vector `0x01F83390 + slot × 0x20` (in place, or through `0x001A4250` when the vector is
full), sets the counter `0x01F832C4` to 0 and adds 1 to the slot's count at `0x01F832B0` (`0x0020AF88`-`0x0020AFB4`).

After a push it passes `0x00189120()` to `0x0016D6A0`, a bare `ret` (`0x0020AFBB`, `0x0020AFC3`); the three early stops skip
that call.

`0x0020A760(slot)` empties a slot. It first stores the slot in the marker `0x01DFE40C` (`0x0020A760`). For a slot below 5
(an unsigned compare, so a negative slot is skipped too, `0x0020A768`) it clears the shared name `0x01F832C8` and the
slot's name (each, when not already empty, by a zero first byte and its end set back to its begin), its vector
`0x01F83390 + slot × 0x20` (end set to begin) and its count; in every case it leaves the marker `0x01DFE40C` at -1
(`0x0020A7E7`).

The setter `0x0020AC30` calls it when the new name differs from the slot's and the slot's count is non-zero
(`0x0020ACD8`), and so does `0x001EC4B0` (from `0x00360120`, from `0x00356D40`, the begin of `eventdispose_f2`, and from
`0x00350960`, the result callback of script call `0x5AB`, which passes the calling manager's index `+0x28`), which
then raises the byte `0x01FD3AE3` (`0x00214B30`).

The shared name is a static string: `0x01F832C8` its begin, `0x01F832D0` its end and `0x01F832D8` its capacity end, with
its allocator at `0x01F832E0`. The initialiser `0x0015DBB0` builds it empty (`0x0015DBDC`); `0x0020A760` empties it by
setting the end back to the begin (`0x0020A774`, `0x0020A787`); and `0x001C50C0` copies it out through `0x001A4BF0`
(`0x001C50EA`).

On that byte `0x00214C30` runs `0x001C5040`, which empties `0x01F812A8`, clears the two scene maps of the
current index `0x01F813F8` (`0x01F813A8` and `0x01F813D8`, through `0x00202880`) and sets that index's
words at `0x01F81400` and `0x01F81408` to -1. Script call `0x5C9` (`0x00352F00`) pushes `0x001EC500()`, the
queued count of the marked slot, or 0 when no slot is marked.

`0x001EC560()` returns 1 only while a slot is marked (`0x01DFE40C` at most 4, unsigned), that slot's queued count is
non-zero and `0x00265680()` returns 0 (`0x001EC56F`-`0x001EC58A`); otherwise it returns 0. The frame update and the
graphics settings read it ([frame update order](frame-update-order.md), [graphics settings](graphics-settings.md)).

### The read-out rows

Several rows print a live value that the renderer `0x001CD0E0` gathers itself:

| Row | Label | What the renderer prints |
|---|---|---|
| 2 | (information) | the frame rates and the background, with the loaded map `0x00314910()` (payload `+0x105C`, [zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) and the story-progress word `0x00265270()` as its `(%d/%d)`, and, while the marked slot's queued count at `0x01F832B0` is non-zero, `event:` with the slot's name from `0x001C5110` (the name at `0x01F832F0 + slot × 0x20`) |
| 7 | (information) | `CutSceneName: %s Cut: %d(id: %d) Frame: %d`: the slot name (`0x001C5110`, an empty string when no slot is marked: `0x01DFE40C` above 4, unsigned, `0x001C512D`, `0x001C517F`-`0x001C51B8`), its queued count, the last entry of its vector `0x01F83390`, and the counter `0x01F832C4` |
| 8 | (information) | for the picked object of `0x001C0DA0()` while its byte `+9` is set and the information page is open: its name (`0x001C0330`: `Disabled`, `NULL` or its own), its mesh texture (`0x001C0540`), its procedural texture (`0x001C0480`) and its tiling and blending values |
| 57 | Operate cube map | `0x001AD440()` `+0x168` through `0x0017F5E0` (-1 without the object), marked `NOT EDITABLE` unless its `+0x40` is 1 |
| 59 | Recapture cube maps | the status string `0x001AC7A0` picks: `+0x204 + [+0x200] × 0x20` of the cube-map object |
| 102 | Current GPU Temperature | the current adapter's temperature, `%d(C)` (below) |
| 220 | Extra BGM status | `0x0017E010`: `Not forced`, `Forced on` or `Forced off` from `0x01DF0018` by `0x01DF0010` |
| 222 | Control character position | `x:%f, y:%f, z:%f` from `0x003091C0`: the position (`0x00265020`) of the actor `0x00263750(0x003272F0())` when `0x00265970` holds; `0x003272F0` is the party leader's roster slot ([party leader](../Party/party-leader.md)) and the call goes through `0x0031ABF0`, a jump to `0x00263750` |
| 246 | Chara Name | `(%d) %s`: `0x00308E80(i)` gives a name from the record that `0x022C24E0 + i × 8` points to: its byte `+4`, below 6, picks one of `Vaan`, `Ashe`, `Fran`, `Balthier`, `Basch`, `Penelo` at `0x01EEC268`; otherwise `Nobody` |
| 264 | Game Display Resolution | `0x001DCD30` (`[0x01F82D20]`) and `GetSystemMetrics`: the two lines below |
| 266 | System Adapter | `0x001DCB90`: ` Count %d ,Now: %s ,Video Memory: %lld MB, Temperature: %d(C)`, the memory being the adapter's `+0x110` divided by 1,000,000 |
| 290 | Game Time Stop is | `Off` while the running byte `[0x0018A7D0()]` is 0; else `On by Debug` when its second byte is set (`0x0018A790`), `On by Focus` when its third is (`0x0018A7B0`), else the third string at `0x008FFF08` |

Row 222's `0x003091C0(&x, &y, &z)` writes the console's `+0xE20`, `+0xE24` and `+0xE28` (`0x001CF574`-`0x001CF589`)
only when the actor `0x0031ABF0` returns exists (`0x003091EC`) and `0x00265970` returns non-zero (`0x003091FC`);
otherwise the three fields keep their last values. Row 246's `0x00308E80(i)` takes `i` from the console's
`+0x10A8` (`0x001CFC23`) and also gives `Nobody` (`0x00D10394`) when the record pointer is null (`0x00308E95`).

Row 264 prints `0x001DCD30`'s `%d X %d ,%dHz, %dHz` and then `Screen Resolution :%dx%d` from `GetSystemMetrics`
(`SM_CXSCREEN` by `SM_CYSCREEN`, called at `0x001CD53F` and `0x001CD535`; format `0x008FFAB8`).

`0x001DCD30` fills the first with the configured resolution (`[0x01F82D20]` `+0x06` by `+0x04` with `+0x08` set,
else `+0x2E` by `+0x2C`; the two `%d` take them in that order, `0x001DCD8D`-`0x001DCDA7`), then the selected
mode's rate, the mode record `m = [+0x28] + [+0x24] × 0x1C` of the `0x001DDAB0`
object with its `+0x08` divided by its `+0x0C`, the unsigned `[m + 0x08] / [m + 0x0C]` (`0x001DCD68`-`0x001DCD80`), then
the desktop's refresh rate (`EnumDisplaySettingsW(0, -1)`, its `dmDisplayFrequency`); it writes the text into the
object's `+0x80` and returns that buffer.

Row 266's `0x001DCB90` fills ` Count %d ,Now: %s ,Video Memory: %lld MB, Temperature: %d(C)` with the `0x001DDAB0`
object's `+0x54`, the current adapter's name, its `+0x110` divided by 1,000 twice, `[+0x110] / 1000 / 1000` as
unsigned 64-bit numbers (each through the constant `0x0624DD2F1A9FBE77`, `0x001DCC69`-`0x001DCC95`) and the
temperature, which stays 0 when no provider answers (`0x001DCBBF`); it writes the text into the object's `+0x80` and
returns that buffer.

For row 8, `0x001C0540(object, out)` asks the map-art context `0x001A9930()`:
`0x001A74A0(context, out, [object + 0x10])` finds the `+0x260` of the object's `+0x10` in the map at `+0x448`, inserting
a default record with an empty name when the key is absent (`0x001A2F70`, `0x001A3089`), takes the name at the entry's
`+0x40`, and keeps the part after the last `/` minus its last ten characters, or all of that part when it is shorter
than ten (`0x001A758A`, `0x001A9E7F`). While the object's byte `+9` is 0, or its `+0x10` is 0, `0x001C0540` returns an empty
string
instead (`0x001C0557`, `0x001C05B1`).

`0x001C0480` copies, with `0x001BE660`, the string that `+0x80` of the first entry of the `+0x18` list of the
object's `+0x10` points to, with that pointer's bit `0x1` cleared (`0x001C04B7`, `0x001E3E90`).

Rows 102 and 266 query the graphics vendors' libraries. The current adapter is the record at
`[+0x78] + [+0x48] × 0x140` of the `0x001DDAB0` object (`0x001DC9C0`), and `0x0020D2B0` builds a chain of `AdapterInfos`
providers whose head sits on
the stack and whose second link is the static provider at `0x01E02580`. `0x0020DA50` asks each provider in turn (vtable
slot 0) for the temperature of the adapter id at the record's `+0x104` until one answers, and `0x0020D9F0` asks the same
way (slot 1) for the name.

When no provider gives the name, `0x001DCB90` falls back to the record's own wide name (`+0x00`, formatted with `%ws`,
`0x001DCC4D`).

### The dispatcher

`0x001D1660(ctx, dir, !dir, id)` is 13,753 bytes long. At
`0x001D166F` it subtracts 12 from the id, refuses anything above 281 unsigned (so ids below 12 too)
with the do-nothing arm `0x001D4C09`, and jumps through a 282-entry table of image-relative
offsets at `0x001D4C1C`, placed right after the body: arm = `0x120000 + table[id - 12]`. The 282
entries name 227 distinct targets, 226 arms and the shared do-nothing arm `0x001D4BFA` that 56 ids
share; 212 of the arms end in a jump to it. Valid ids are 12 to 293, so ids 1 to 11 are label-only
rows.

The arms are small. 110 adjust a float in both directions. Most `movss` the field, `test bl, bl`
(the direction), `subss` or `addss` one constant from the float pool and `movss` it back. 102 of
the 110 have one magnitude, symmetric in both directions: 0.01 for 58 arms, 0.02 for 11, 0.05 for
10, 0.1 for 9, 0.001 for 7, 0.03 for 3, 1.0 for 2, 0.5 and 0.005556 for one each. The sign composes
from the mnemonic and the constant's own sign (`+0.01` at `0x008F30E4`, `-0.01` at `0x009002F4`).

Two kinds scale instead of adding a constant. Id 106 multiplies the field by 0.99 or 1.01 (`0x001D2BC5`,
`0x001D2BDA`), and ids 190 to 193 scale their step by the field `+0xC58` / 5 while that field is above
20 (`0x001D3CCB`, `0x001D3CE7`).

The rest call a subsystem, step an integer with a wrap, toggle a byte or cycle a mode; the table
on [debug menu commands](debug-menu-commands.md) gives every id. The shared helpers are
singleton getters: `0x001A9930` (`0x01F81168`), `0x00193D50` (the `0x4A8` post-process parameter object
kept at `0x01F7F5F0`), `0x001DDAB0` (`0x01F82D18`), `0x001C2F40` (`0x01F81270`), the game-setting object pointer
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
only when its path ends in `.cm` (`0x002EEF9D`-`0x002EEFBF`; the value is loaded at `0x002EEFF3` and the one return is
`0x002EF006`).

With no path, or one not ending in `.cm`, it moves to the next letter of the table with the number reset to 0 and
tries again (`0x002EEFC1`-`0x002EEFE9`); a letter missing from the table logs `get character id error!` (`0x00D0F8C0`, at
`0x002EEFDC`) and retries (`0x002EEFE1`). It never returns 0.

### Who reaches the dispatcher

`0x001D1660` has one caller (the data references at `0x01D5D550` and `0x01D5D560` are exception
records, not a call table), the adapter `0x001CD040(ctx, dir, id)`, whose one caller is `0x0017DB90`,
whose two callers are the message procedures `0x0023B330` and `0x0023B6F0` of the retail Config
screen's rows.

`0x0023B330` handles a press on its message 10 (`0x0023B399`): while its `+0x1D0` is 0, bit `0x80` of the repeat word
`0x02F9736C` gives direction 1 and, without it, bit `0x20` gives direction 0 for `0x0017DB90([+0xC0], [+0xC4],
direction)`, and the returned value goes back to `+0xC4` (`0x0023B3D5`); with neither bit, or with `+0x1D0` set, the
message does nothing. Message 12 sets `+0x1D0` to 1 when the message's `+0x08` is 1 and to 0 otherwise (`0x0023B37C`).

Message 1 takes the row kind `+0xC0` from the message's `+0x08`, reads its value into `+0xC4` with `0x0017E070`
(`0x0023B4B6`-`0x0023B4C4`) and clears `+0x1D0`; message 4 rebuilds the row's text (`0x0023B530`), and message 14 calls
`0x002470D0`.

`0x0017DB90(kind, value, dir)` maps a row kind to a console id and dispatches it as
`0x001CD040(0x001D50D0(), dir != 0, id)` (`0x0017DD34`), then calls the empty stub `0x0016D6A0` (`0x0017DD39`) and,
for every kind but 6, returns the row's new value from `0x0017E070(kind)`, a read of `[0x01F82D20] + offset` for
most kinds;
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
`[0x01F82D20] + 8` is 0, and 6 cycles its value through 0, 1, 2.

Kind 5 passes `dir == 0` to `0x001DC940` (`0x0017DC1E`) and does neither call while `0x001DDAB0()` returns 0
(`0x0017DC08`). Kind 6 steps the passed `value` up by one for `dir` 0 and down by one otherwise, wrapping at both
ends (`0x0017DC46`-`0x0017DC64`), and returns that value itself, without the stub or `0x0017E070` (`0x0017DD45`). Kinds
0, 2, 3, 11, 14 and 17 (the Config screen's headings) and any kind outside 1 to 23 dispatch nothing and read back -1.
While `0x001D50D0()` returns 0 no kind dispatches or steps (`0x0017DBB9`), and the value comes from `0x0017E070(kind)`.

So sixteen of the 282 ids are
retail, reached from the Config screen; the other 266 have no caller in the shipped game, and
the menu that would reach them never opens.

Two console bytes are read by input code instead of a menu arm. While `+0xC3D` (row 293, "Key
Board Debug For Japanese Keyboard") is set, the control-code lookups `0x00197790` and `0x00197800`
use the 107-entry table `0x01DF1030` in place of `0x01DF0E80` (both read for indexes 0 to 106, `0x00197825`, `0x00197842`),
and while `+0xC35` (row 187, "Enable
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

`debug_eventload`'s begin `0x0050D030` stores the id at `+4`, the kind at `+0` and 0 at `+8` of the call's state. The
poll `0x0050D0C0` issues the request on its first run, while `+8` is 0, and then sets `+8` to 1 (`0x0050D11A`). For a kind
other than 4 it first looks at actor manager `kind` (`0x00263FF0`): while that manager has bit `0x1` of `+0x10` set and
a non-zero byte `+0x13`, the poll requests its teardown (`0x0026A5F0(kind)`) and holds without issuing the load or
setting `+8`, so it tries again on its next run (`0x0050D0EC`-`0x0050D103`).

After the request a kind-4 call ends at once (`0x0050D11D`); any other kind holds while `0x0032E520(1)` reports a load,
and each holding run sets `0x022C253D` to 1 through `0x00314D40(1)` (`0x0050D13C`).

### The debug text display

The rows that print text in the 3D view do it through the `MultipleDebugDisplay` singleton at `0x01F81270` (getter
`0x001C2F40`). `0x001C2F00` returns at once while `[0x01F81270]` is set; otherwise it allocates its `0x4670` bytes
(`0x00210EC0`), runs the constructor `0x001C1D40` on them and stores the result at `0x01F81270` (`0x001C2F34`; 0 when the
allocation returns 0). `0x001C2120` is the destructor body and `0x001C2670` the deleting wrapper. The start-up step
`0x0017D6B0` makes the call to `0x001C2F00` ([game application](game-application.md)).

A line is a `0x230`-byte record: x and y floats, a 256-byte text buffer at `+0x08` and a text object at `+0x108`.

The destructor body `0x001C2120` stores the vtable `0x008F9DC8` again and releases, with `0x001EAE10`, the 32 fixed
text objects (`0x001C215A`) and the text object of every record in the vector at `+0x4618` (`0x001C21B5`). It then
runs `0x001C2070` on the vectors at `+0x4640` and `+0x4618`, which calls `0x001EA180` on each record's text object and
frees the storage through the vector's allocator (its slot `+0x18`), and last runs `0x001C2110` (`0x001EA180` on the
record's text object) over the 32 fixed records through the array destructor `0x00809054` (`0x001C2208`).

The constructor stores the vtable `0x008F9DC8` (its first slot is the deleting wrapper `0x001C2670`) and clears the byte
`+0x08`. It builds 32 fixed records at `+0x10` through the array constructor `0x00808FE4`, each by `0x001C1D20` (the text
object's constructor `0x001E9F40` at `+0x108`; `0x001C2110` is the matching destructor), and empties the vectors at
`+0x4618` and `+0x4640` (begin, end and capacity end 0, an `EASTL vector` allocator) with their counts `+0x4638` and
`+0x4660` (`0x001C1DBF`, `0x001C1DF4`). It then prepares each fixed text object with `0x001EA3C0`.

That loads `PhyreText.fx` and the font `tuffysdf.fgen` (the two paths at `0x01DFDE00`), binds the technique
`RenderText_SoftEdges` (`0x006CCCE0` looks it up by name from the table at `0x00D89BE0` and caches it), writes `"Debug
Info:"`.

`0x006CCCE0(i)` returns the cached entry `[0x02E5BE50 + i × 8]` when it is non-zero. Otherwise it takes the name at
`0x00D89BE0 + i × 16` and walks the list from `[0x02CBF998]` (name pointer at `+0x00`, next node at `+0x08`) for the
node whose name is the same string; it stores that node, or 0 when the name pointer is null or no node matches,
in the cache (`0x006CCD53`) and returns it, so a miss is searched again on the next call.

It sizes the glyph arrays for 128 entries (`0x0067C310`, which
grows them with `0x00672B80` and `0x00672C70`). The constructor then calls, on each, `0x001EAC30(object, 1)` (1 into
the object's `+0xFC`), `0x001EAA90(object, 1280, 720)` and `0x001EAC40(object, 1)` (the visible byte `+0xEA`), sets
the fixed count `+0x4610` and the mode `+0x0C` to 0 (`0x001C1E40`, `0x001C1E46`), leaves the overlay byte `+0x463C` at
0 (`0x001C1DC5`), and sets the scales `+0x4664 = -5.5` and `+0x4668 = -10.0` (`0xC0B00000` and `0xC1200000`,
`0x001C1E49`, `0x001C1E53`).

`0x001C2980(display, line, kind)` queues a line. Both kinds map the position as x × `+0x4664` - 1.65 and
y × `+0x4668` - 2.0, written back in place: kind 0 through `0x001C2D10(display, &x, &y)`, which changes nothing when
either pointer is 0 (`0x001C2D13`, `0x001C2D18`), kind 1 inline (`0x001C2C74`-`0x001C2CA1`), testing only the y pointer;
both hand the text to the object (`0x001EADB0`, `0x001EAD20`) and mark it visible (`0x001EAEA0`):

- kind 0, from `0x00181F20` (the character-name printer `0x0053AB50`): taken only while the mode is
  non-zero and fewer than 32 fixed lines are queued (`+0x4610`);
- in mode 2 kind 0 drops lines that start with `W`; in mode 3 it keeps only lines that start with
  `C`, `M` or `N` (either case); a kind-0 line that starts with `H` or `M` gets 1 added to its y,
  one with `G` gets 2;
- kind 1, from `0x00181E70`: taken only while `+0x463C` is set, appended to the vector at `+0x4618`
  (count `+0x4638`). The vector grows through `0x001C2D50` and `0x001C2790`, which copy records with
  `0x001C1B00`, `0x001C1C80`, `0x001C2230`, `0x001C1E70` and `0x0067ACF0`.

`0x00181F20(pos, text)` and `0x00181E70(pos, text)` build the line on their stack: a text object made by `0x001E9F40`,
x and y from `pos` `+0x00` / `+0x04`, and `text` copied byte by byte up to and including its terminator into the
256-byte buffer, with no length check. They pass it to `0x001C2980(0x001C2F40(), line, 0)` (`0x00181F8E`) and
`0x001C2980(0x001C2F40(), line, 1)` (`0x00181EE1`) and then release the text object with `0x001EA180`.

Growing a vector copies `DebugLine` records. `0x001C1C80(dst, src)` copy-constructs one: x, y and the
256-byte text, then the text object through `0x001C1E70`, and returns `dst`. `0x001C1B00(out, first, last, dest)`
does the same for a range into new storage, `0x230` bytes apart: it keeps the next destination in `*out`
(`0x001C1B1B`, `0x001C1BDB`), skips the copy for a destination of 0 (`0x001C1B40`) and returns `out`.

`0x001C1A60(first, last, destEnd)` copy-assigns a range backward, the text object through `0x001C22A0`, and returns
the lowest record it wrote, the last one copied (`0x001C1AF0`), `destEnd` itself for an empty range.

`0x001C1E70` takes the
object's array of strings with `0x001C1C00(dst, src)`: a new array of the same count (the low 31 bits
of its count word) from `0x0017D260(count × 8, 8)`, and `0x001C19A0(dst, src, n)` duplicates each string into its own
block, its source pointer read with bit `0x1` cleared. An empty source, or a failed allocation, leaves the copy
with count 0 and array pointer 0 (`0x001C1C2F`, `0x001C1C45`, `0x001C1C69`).

`0x001C22A0` builds the same array itself (`0x001C2317`, `0x001C232D`). It releases the destination's old array and
its strings through `0x00584730`, keeping a string that is 0 or has bit `0x1` set, unless the old pointer is the
new one, the old pointer is null or the old count word has bit `0x80000000` set (`0x001C2342`-`0x001C2383`). It then
stores the new pointer and the count (`0x001C2388`, `0x001C238C`), so a failed allocation leaves array pointer 0 with
the source's count. In both copies the count word never has bit `0x80000000` set.

For each string `0x001C19A0` measures the text, takes a block of its length plus one from
`0x0017D260(length + 1, 2)` and copies the text and its terminator with `memcpy` (`0x00861EBA`, `0x001C1A2C`); a source
pointer of 0 after the clear, or a failed allocation, stores 0 (`0x001C19F4`, `0x001C1A21`). For `n` = 0 it returns at
once (`0x001C19A3`).

The render pass list `0x00187950` calls `0x001C2DB0`. While the render manager `0x00189120()` exists it calls `0x00186AA0` and
`0x00186A90` (the render width and height, both results dropped) and then draws, each line through `0x001EA830(object,
[manager + 0x08], 0)`, the fixed lines while the mode is set, the overlay lines while `+0x463C` is set, and the lines
of the vector at `+0x4640` (count `+0x4660`), then zeroes the counts.

With or without the manager (`0x001C2DC7`) the counts it zeroes are `+0x4610` while the mode is set, `+0x4660` always
and `+0x4638` while `+0x463C` is set (`0x001C2ECD`, `0x001C2ED3`, `0x001C2EE2`); the fixed count is also zeroed right after
the fixed lines are drawn (`0x001C2E39`).

Each line goes through `0x001EA830(object, context, bracket)`: when the object is visible (`+0xEA`) and built (`+0x20`)
it sets the string (`0x0067C4F0` on the glyph object, with the pointer at `+0x48`, or a null pointer while the dword
`+0x50` is 0, `0x001EA886`), posts the render queue's block (`0x00185A50`), and draws the string in black at its position
plus the offset `+0x100` to `+0x108` (summed into `+0xC8` to `+0xD0`, `0x001EA8E1`), then in white at its position, both
through `0x001EAC60`, which writes the placement into the glyph object `+0x20` at its `+0x208` to `+0x234`;

the colours go to the material `+0x18` (`0x0067C440`). `0x001EAC60` takes a 4 × 4 transform (`+0x98` for black, `+0x58`
for white) and stores rows 1 to 3's first three values, with row 0's x, y and z as each row's fourth value.

`0x001EA830` returns 0 after both draws, and 0 for an object that is not visible or not built (`0x001EA979`). A
non-zero result of a call it checks (`0x005FEFD0`, `0x0067C4F0`, either `0x0067C260` draw, `0x00600A60`) ends it at once
and is returned, so a zero `+0x50` (for which `0x0067C4F0` returns 1) draws nothing. A non-zero `bracket` opens
the context's bit `0x1` bracket first (`0x005FEFD0(context, 0)`, `0x001EA86B`) and closes it after the white draw
(`0x00600A60(context, 3)`, `0x001EA970`); the three calls in `0x001C2DB0` give it 0.

`0x001EAE10` releases a text object: its material (`0x001EA050`),
its glyph object (`0x0067B3A0`) and its two assets (`0x0019CC50`). Each of the first two, when present, is then
freed with `0x00584730` and its pointer `+0x18` or `+0x20` set to 0 (`0x001EAE42`, `0x001EAE65`); the assets are the
pointers at `+0x00` and `+0x08`, each handed to `0x0019CC50` with the loaded-asset registry `0x0019CE20()`.
`0x001EA130`, reached from the unwind handlers `0x0089873C` and `0x0089E880`, frees a counted array the same way
`0x001EA050` does.

Four console rows drive it. Row 51 "Draw Chr Names" cycles the mode through 0 to 3 (`0x001D5230`).
Rows 218 and 219 step `+0x4664` and
`+0x4668` by 0.1. Row 176 "Show Map Hide Group" sets `+0x463C` (`0x001D2C08`), which makes the pump run
`0x0022FFE0`.

`0x0022FFE0`
walks the cells of the collision grid `0x0026E500(0)`, draws a four-vertex quad over each cell and prints at its
centre the list of eight-bit group numbers found in the cell's polygon attribute words
(`"%d, %s"`). It places the text with `0x00181FD0` and `0x001820E0`, which multiply a point by the
first (`+0x08`) and second (`+0x78`) matrix of the camera block: the camera pair's (`0x0018A620`, the block
`0x0018A620() + 8`) while its first byte is set, else the render manager's (`0x00189120()`) `+0x690`.

Both write the point's x, y and z back in place and store 1.0 in its `+0x0C` (`0x001820C7`, `0x00182133`).
`0x00181FD0` reads the twelve floats `+0x08` to `+0x34`: new x = x·`+0x14` + y·`+0x08` + z·`+0x18` + `+0x28`,
new y = x·`+0x24` + y·`+0x0C` + z·`+0x1C` + `+0x2C`, new z = x·`+0x34` + y·`+0x10` + z·`+0x20` + `+0x30`.
`0x001820E0` multiplies the row vector (x, y, z, 1) by the 4 × 4 matrix whose rows are at `+0x78`, `+0x88`,
`+0x98` and `+0xA8`, keeping the first three columns.

### The cube-map capture camera

The cube-map object (`0x001AD440`, `0x258` bytes at `[0x01F811C8]`) carries a developer capture: a step
that would point the render manager's cameras at each face of a cube, or around a panorama, one
step per frame. Console rows 56 "Capture cube map" and 59 "Recapture cube maps" name it (labels
stored at `0x001D07FE` and `0x001D0828`). The capture never runs in the shipped game.

The step `+0xA8` is set to -2 by the constructor `0x001AA9E0` (`0x001AAA5C`). The only other store,
`0x001AC7D6` in `0x001AC7C0`, sets it to -1 when the step is -2 and byte `+0xA4` is set; `0x001AC7C0` then, when the
shadow object `0x001F0850()` is not 0, jumps to `0x001EF540(shadow object, 1)` (`0x001AC7F8`), and in every other case
returns with no store or call. `+0xA4` is
written only by the constructor, with 0 (`0x001AAA55`). The step stays at -2.

`0x001ACC30(object, &fov, &scale, &aspect, &a, &b, &c)` turns the step into a camera. It returns false
and writes nothing when the count `+0xB8` is 2 or the step is negative or odd. Otherwise it writes the
defaults (fov 2π, scale and aspect 1, the angles 0), takes `n` = count / 2 and the face `f` = step / 2,
and continues by the mode `+0xBC`:

| Mode | fov | Angles |
|---|---|---|
| 0, 1 | 2π / (n − 2), 90° for the constructor's count of 12 | face 0: `a` = −π/2; 1: `a` = π/2; 2: `b` = π/2; 3: `b` = −π/2; 4: `a` = π; 5: the angles stay 0 |
| 2 | 2π / n | `a` = f × fov + `+0x190` + π; scale and aspect from `0x01DF1B70` and `0x01DF1B74` (1.0 each) |
| 3 | `+0x1E0` degrees (180) / `+0x1E4` (3) | `a` = `+0x190`; `b` = −`+0x194`, or 0 while byte `0x01F811D0` is set; `c` = fov / 2 − span / 2 + π + f × fov |
| other | 2π | the angles stay 0 |

`0x00189570`, run by the per-frame pump `0x0017D6E0` and by the render pass list `0x00187950`, asks
`0x001ACC30` and, on true, sets five cameras through `0x00185C30`; on false it returns with no further call
(`0x001895E6`):

- the render manager's cameras at `+0x690`, `+0x820`, `+0x358` and `+0x4E8`, with the controllers at
  `+0x798`, `+0x928`, `+0x460` and `+0x5F0`, and, while the camera pair's first byte is set, the
  pair's camera `0x0018A620() + 8` with the controller at `+0x9C8`, after which `0x0018A680(pair, pair + 8)` copies
  that camera into the pair's camera at `+0xE0` (`0x001897A1`,
  [scripted camera](../Graphics/scripted-camera.md));
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

`0x00189130` rebuilds the 3 × 4 world matrix that the camera's `+0xB8` points to. It starts from axes (1, 0, 0), (0, −1,
0) and (0, 0, −1) with the matrix's own `+0x20`, `+0x24` and `+0x28` as the last row, multiplies in turn (`0x00185100`)
by a rotation of `a` about (0, −1, 0), a rotation of `b` about x, and a rotation of `c` about (0, −1, 0), and writes
the result back. `0x00188E60(out, angle, axis)` builds the rotation about a unit axis; `0x0062E1C0` uses it too.

With S = sin(angle) (`0x00861F0E`), C = cos(angle) (`0x00861F08`), T = 1 − C and the axis (x, y, z), it writes the 4 × 4
rows (xxT + C, xyT + zS, xzT − yS, 0), (xyT − zS, yyT + C, yzT + xS, 0), (xzT + yS, yzT − xS, zzT + C, 0) and (0, 0,
0, 1) from `0x008C5FD0`, and returns `out`.

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
| `0x01F81428` | `void*` |  | the console object (`0x10E8`), from `0x001D50D0` |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0130` | `char*` | row labels | one per id at `+0x130` + id*8, ids 1-294 (`0x001D0390`) |
| `+0x0A70` | `u8` |  | open (always 0) |
| `+0x0A74` | `u32` | mode |  |
| `+0x0A88` | `...` | page |  |
| `+0x0A90` | `...` |  | row count |
| `+0x0AAC` | `i32` |  | weather-slot override |
| `+0x0AB4` | `u32` |  | field id for the code table |
| `+0x0C56` | `u8` |  | information page |
| `+0x10B0` | `...` |  | row of id 9 |
| `+0x10B4` | `...` |  | row of id 10 |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x008FCE00` | `u32[15][22]` |  | the page table (id, 0 = no row) |
| `0x001D4C1C` | `u32[282]` |  | arm RVAs for ids 12-293; `0x001D4BFA` the shared do-nothing arm; `0x001D4C09` the out-of-range arm |
| `0x01DF6E68` | `{char* code; u32 index+1; u32 0}[1314]` |  | the authored-code table (601 codes) |
| `0x01F832B0` | `u32[5]` |  | event-slot counts |
| `0x01F832E8` | `u8` | classification | with `0x01F832E9` |
| `0x01F832E9` | `u8` | classification | with `0x01F832E8` |
| `0x01F832F0` | `string[5]` |  | event-slot names, `0x20` each |
| `0x01F83390` | `vector[5]` |  | event-slot vectors, `0x20` each |
| `0x01DFE40C` | `i32` |  | slot marker |
| `0x01F82D20` | `void*` |  | the game-setting object the Config rows read |
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
| `+0xC0C` | `u8` |  | override rows 60 and 103 |
| `+0xC10` | `f32` | fov | row 104; 0.785 |
| `+0xC14` | `f32` | aspect | row 105; 1.778 |
| `+0xC18` | `f32` | scale | row 106; 1.155 |
| `+0xC1C` | `f32` | c | third angle; 0 |
| `+0xC24` | `u8` | capFov | takes the fov from the cube-map object; 0 |
| `+0xC28` | `i32` |  | panorama row 60, 0 to 12 |


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
  the achievement counter behind it moves too: `0x00254EE0` calls `0x00316A50` with counter 6 and the gain
  (`0x00254EF8`), or counter 7 and the loss, whenever the new value differs from the purse; with gil already at
  99,999,999 it makes no call (`0x00254EF6`, `0x00254EFC`)
  ([achievements](../Steam-And-Achievements/achievements.md)).

## Related

- [Debug menu commands](debug-menu-commands.md): every id with its label, arm, kind and field.
- [`debug-menu-settings-01f81428-accesses.tsv`](debug-menu-settings-01f81428-accesses.tsv): every access
  to the console object `[0x01F81428]` outside its constructor, one row per instruction (754 rows).
- [Graphics settings](graphics-settings.md): the block most stepped fields live in.
- [Frame update order](frame-update-order.md): the draw block and the display flag.
- [Weather](../World-Areas-And-Travel/weather.md): the slot override at `+0xAAC`.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the codes in the authored-code table.
- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md): the setter the gil row calls.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Status periodic terminal: `0x00265680` is called by `0x00310DB0`; those functions are documented on
  [frame update order](frame-update-order.md).
- World area: `0x00314D40` is called by `0x00266D10`; those functions are documented on
  [force fight mode](force-fight-mode.md).
