---
title: "Debug menu: the developer console object, its fifteen pages, its command dispatcher and the retail rows that still reach it"
kind: "system"
category: "Engine core"
summary: "The developer menu the remaster still carries: the settings object and its 293 row labels, the fifteen pages of row ids, the row renderer and the two per-id tables it reads, the dispatcher that runs one of 226 command arms by id and the shape of the arms, the single byte that would open the menu and that nothing in the shipped game sets, and the sixteen graphics rows of the retail Config screen that reach the dispatcher anyway."
addresses: ["001D1660", "001D4C1C", "001D4BFA", "001D4C09", "001CD040", "0017DB90", "0017E070", "0023B330", "0023B6F0", "001D50D0", "001CCB20", "001D0390", "001CD0E0", "001D5260", "001D5520", "0017DAA0", "00187950", "001D0190", "008FCE00", "01DF6E68", "0017D490", "001A9930", "00193D50", "001DF340", "001DDAB0", "001C2F40", "003058B0", "00254EE0", "0020AC30", "0020AF10", "001EC560", "00358330", "0022A550", "01F82D20", "01DF6E48"]
---

# Debug menu: the developer console object, its fifteen pages, its command dispatcher and the retail rows that still reach it

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

`001D50D0()` returns the console settings object, created on first use (`00210EC0(0x10E8)`, then
the constructor `001CCB20`) and cached at `01F81428`. The constructor zeroes and defaults the
object and calls `001D0390`, which stores the row labels when `001EA3C0(obj + 8)` returns 0,
noting that at `+0xA68`: one string pointer per id at `+0x130 + id × 8` for ids 1 to 294 (id 2's
string is empty), 293 names in all.

`001D0390` also primes page 0 through the renderer, sets the text parameters and writes nine
32-byte strings at `+0xAE4`, `+0xB04` to `+0xBE4` (`OFF`, `Black
Hole`, `Luminescence`, `Ark Blast`, `Whiteout`, `Windburst`, `Torrent`, `Cataclysm`, `Inferno`),
the concurrence names an information row prints.

The open byte `+0xA70` is written once, to 0, by the constructor; no other instruction in the
image writes it. The page cursor is `+0xA88`, the row count `+0xA90`, the information-page flag
`+0xC56`, the weather-slot override `+0xAAC` (read through `0017D490` by the field runtime,
[weather](../World-Areas-And-Travel/weather.md)), and the field id for the code table `+0xAB4`.

### The pages and the renderer

The page table at `008FCE00` holds 15 pages of 22 ids (0 = no row). `001D5260`, called from the
field frame's draw block through `0017DAA0` when `00358330(1)` holds ([frame update
order](frame-update-order.md)), returns at once unless `+0xA70` is set; otherwise it prints `<Page
n/14>` or `<Information Page>` and, for every id on the page, has the row renderer `001CD0E0(ctx,
id, buffer)` format the row (`"None content!!"` when it prints nothing).

The information page (page 14) runs its ids through the filter `001D0190` first:

- ids 1, 2, 6, 9, 102, 204, 221, 222 and 290 always;
- 7 only while an event slot holds queued events (`01DFE40C`, the slot of the most recent
  `startscene` push, at most 4 and its counter at `01F832B0` non-zero; `0020AF10` sets it and
  `0020AC30` leaves it at -1);
- 8 only while the save-load manager at `01F81258` has its byte `+9` set;
- 10 only while `0022A550()` holds (main-loop state 2 with `00358330(1)`);
- 101 only while `+0xA74` is 2; any other id is dropped.

`001D5520`, called from the render pass list `00187950`, redraws rows 9 and 10 of the information
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

- the authored-code table at `01DF6E68`, 1,314 records of 16 bytes (`char* code, u32 index + 1,
  u32 0`; 601 codes such as `ous0101`, the map pack of the field with that index, [MPK map
  pack](../World-Areas-And-Travel/mpk-map-pack.md)), indexed by the field id at `+0xAB4`;
- the event-slot panel: five slots whose names (`01F832F0 + slot × 0x20`), queued event counts
  (`01F832B0`) and classification bytes (`01F832E8` for a `sum_` name containing `0001`,
  `01F832E9` for a `spc_` name) the setter `0020AC30` and the pusher `0020AF10` maintain from
  the `plan_master\<locale>\event\` paths the resource loads hand them.

### The dispatcher

`001D1660(ctx, dir, !dir, id)` is 13,753 bytes long. At
`001D166F` it subtracts 12 from the id, refuses anything above 281 unsigned (so ids below 12 too)
with the do-nothing arm `001D4C09`, and jumps through a 282-entry table of image-relative
offsets at `001D4C1C`, placed right after the body: arm = `0x120000 + table[id - 12]`. The 282
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
singleton getters: `001A9930` (`01F81168`), `00193D50` (the `0x4A8` post-process parameter object
at `01F7F5F0`), `001DDAB0` (`01F82D18`), `001C2F40` (`01F81270`), the game-setting object pointer
`01F82D20` loaded in 18 arms, and the indexed store `001DF340(obj, i, v)`.

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
| 1 | `0x11B` | Apply Graphic Quality Default | `+0x0C` |
| 4 | `0x10A` | System Adapter | `001DDAB0() + 0x48` |
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

Kinds 5 and 6 do not dispatch: 5 runs `001DC940` on the `001DDAB0` object and `001DC730` when
`[01F82D20] + 8` is 0, and 6 cycles its value through 0, 1, 2. So sixteen of the 282 ids are
retail, reached from the Config screen; the other 266 have no caller in the shipped game, and
the menu that would reach them never opens.

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

Per frame in the field: `0017DAA0` draws the menu only while `+0xA70` is set, which never
happens; the render pass list's `001D5520` the same. Per Config-screen press: `0017DB90` maps
the row to an id, `001D1660` runs the arm, `0017E070` reads the value back for the row.

## State

The console object, the page table and the arm table (both in the image), the game-setting
object, the display flag words, the event-slot arrays.

## Modding notes

- The menu is one byte away: a write of 1 to `+0xA70` of the object at `[01F81428]` while the
  field frame runs (`00358330(1)` must hold, [frame update order](frame-update-order.md)) draws
  page `+0xA88`; the arms then need a caller, since no input code in the image dispatches a row
  from the menu.
- The arm table is in `.text` after the body and holds RVAs; the 56 ids on the do-nothing arm are
  free slots for new commands without growing the table, and the bound `0x119` at `001D167D` is
  the immediate to raise otherwise.
- A row's label names the field; the arm defines its type, step and range. Three adjacent rows
  labelled "Enable 100% successful steal / poach / drop" cycle four, three and five states.
- The gil row is not a cheat path of its own: it calls the setter every shop and reward uses, so
  the achievement counter behind it moves too.

## Related

- [Debug menu commands](debug-menu-commands.md): every id with its label, arm, kind and field.
- [Graphics settings](graphics-settings.md): the block most stepped fields live in.
- [Frame update order](frame-update-order.md): the draw block and the display flag.
- [Weather](../World-Areas-And-Travel/weather.md): the slot override at `+0xAAC`.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the codes in the authored-code table.
- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md): the setter the gil row calls.
