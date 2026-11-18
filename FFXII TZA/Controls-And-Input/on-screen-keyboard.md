[Home](../../README.md) / [Controls and input](README.md) / On-Screen Keyboard

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| On-Screen Keyboard: the F9 overlay that shows every keyboard binding, its seven panels, the key colours and the keys that light up while held | system | Controls and input | Keys, bindings and names | How the On-Screen Keyboard works: F9 opens and closes it, the task that draws it, the seven panels and the controls and keymap profiles each lists, the picture of the keyboard and mouse with each key tinted by the panel of its control, the keys that light while held, the key-cap sets chosen by keyboard layout and game language, and the refresh after a binding changes. | 0x0017DE60, 0x0027E9E0, 0x002878E0, 0x0209AC18, 0x0209AC50, 0x00287C20, 0x002891A0, 0x00289040, 0x00197790, 0x01DF0E80 |

## What the player sees

- F9 shows the On-Screen Keyboard and F9 hides it again; a label on it reads "Hide On-Screen Keyboard".
- It shows a picture of the keyboard and the mouse, and panels such as Character Movement, Camera Movement,
  Confirm, Cancel, Escape and Pause Game with the keys bound to each.
- Every key in the picture takes the colour of the panel whose control it is bound to, and a key lights up
  while it is held.
- An unbound control shows an empty key.
- The key caps follow the Windows keyboard layout (French and German layouts have their own) and the game
  language.

Every panel shows the key bound to its control in the same three keyboard profiles that `keymap.ini` fills and the
Config screen edits. The Config screen rebuilds the panels after each change, so a new binding shows at once.

## How it works

### Opening and closing

`0x0017DE60` answers whether F9 was pressed: it reads and clears the latch of code 73 (`Key_F9`) on keyboard 0
(`0x0079AE90`, `0x0017DE69`-`0x0017DE77`), and on a press it also clears the input manager's last-device flag `+0x38` through `0x001E1100(0)`.
Three frame handlers call it while the keyboard is closed and call `0x0027E9E0` on a press: the field frame
(`0x0022AB51`-`0x0022AB5A`), the full menu frame (`0x0022B984`-`0x0022B98D`) and the capture-backed frame
(`0x0022BCFA`-`0x0022BD03`). Each first asks `0x002878A0`, which returns the open flag `0x0209AC50`.

`0x0027E9E0` creates the keyboard only when `0x0209AC18` is empty: it starts a task of `0xC0` bytes running
`0x002878E0` (`0x00244F50`, `0x0027EA1F`), stores it in `0x0209AC18`, and sets `0x0209AC50` and `0x0209AC14` to 1
(`0x0027E9F3`-`0x0027EA3A`). It then gives the task the default animation descriptor `0x00915198` at `+0x48`
(`0x00247570(task, 0)`, `0x0027EA44`) and opens it under the root `[0x0208EA40]` (`0x00246AD0`, `0x0027EA57`). With
`0x0209AC18` already set it returns at once (`0x0027EA0C`). The only
reference to `0x002878E0` in the image is the `lea` at `0x0027EA18`.

On its input turn (message 10, `0x00287A07`) and on its update (message 2, `0x00287AC8`) the task closes
itself (`0x00244F00`) when `0x0017DE60` reports F9 again (`0x00287A3B`-`0x00287A4B`, `0x00287AFC`-`0x00287B0C`). The
branch that closes on the cancel button instead (`0x00287A10`-`0x00287A34`, `0x00287AD1`-`0x00287AF5`) runs on
either only when `0x0209AC50` is 0, which `0x0027E9E0` never leaves it.

Destroying the task (message 18) clears `0x0209AC18` and, when `0x0209AC50` is not 0, clears it and sets
`0x0209AC14` to 1 (`0x00287953`-`0x0028796E`). It then goes on into the update at `0x00287AD1`, after that
update's test of `0x0209AC50`. With a bit of the word `0x01E0C2A4` set in the word `0x02F9736A` it calls
`0x002814E0(0x504)`, `0x00249C60(3)`, `0x002CA110()` and `0x00244F00` with the emptied `0x0209AC18`; in either
case it then makes the ten calls of step 4 (`0x00287AD1`-`0x00287B7F`). The `0x0017DE60` test at
`0x00287AFC` belongs to the other branch and is not on this path.

### The task

For every message `0x002878E0` first works out the layout set and the language set the way `0x00287C20` does
below (`0x002878FB`-`0x00287928`). It hands both to `0x00287400`, `0x002875D0` and the seven panel builders on the
opening (`0x0028797D`-`0x002879F5`) and to the seven panel updates, at step 3 (`0x00287A68`-`0x00287ABE`) and again
at the copy of that work reached by messages 2 and 18 (`0x00287B29`-`0x00287B7F`). It handles its messages in
this order of work:

1. On creation it builds its widgets with `0x002432B0` from the layout at `+0xA8` of `0x0209AC30` (`0x00287B86`-`0x00287B9E`).

   It copies the words `+0x04`, `+0x06`, `+0x08` and `+0x0A` of the record `0x002432B0` answers, read with no
   null test, to its `+0x98`, `+0x9A`, `+0x9C` and `+0x9E`, four stores skipped for a null task
   (`0x00287BA3`-`0x00287BCF`), clears bit `0x800` of its dword `+0x40`
   and zeroes its word `+0x44` (`0x00287BD6`-`0x00287BDF`). When the qword `0x02CA8FE0` or `0x02CA8FE8` is not 0
   it calls `0x00247730(task, 1)` (`0x00287BE3`-`0x00287BFD`).
2. On the opening, message 14 (`0x00287945`-`0x00287948`), which `0x00246AD0` sends (`0x00246BFF`) when `0x0027E9E0`
   opens the keyboard (`0x0027EA57`), it resets the keyboard picture (`0x00287400`), colours it (`0x002891A0`),
   writes the mouse labels (`0x002875D0`), builds the seven panels and writes the hint label (`0x00287850`)
   (`0x0028797D`-`0x002879FD`).
3. On its input turn, message 10 (`0x0028793C`-`0x0028793F`), which the UI ticks give the widget holding the
   focus (`0x002481C0`-`0x002481FB`), after the close test described above (`0x00287A07`-`0x00287A4B`) it lights
   the held keys (`0x00289040`), colours the picture again (`0x002891A0`), lights the mouse (`0x00289390`) and
   updates the seven panels (`0x00287A50`-`0x00287ABE`).
4. Message 2 (`0x00287933`-`0x00287936`), the update the UI ticks send to each widget of the trees they walk
   unless its dword `+0x40` has bit `0x40000` or `0x400` (`0x00248086`-`0x002480F9`), runs a second copy of step 3:
   the same close test (`0x00287AC8`-`0x00287B0C`), then the same ten calls (`0x00287B11`-`0x00287B7F`). Message 18,
   the destroy, joins that copy at `0x00287AD1` after its own stores (`0x00287953`-`0x00287978`), as described
   above.
   - Message 1 is the creation (`0x0028792A`-`0x0028792D`); a message that is none of the five leaves at once
     (`0x0028794A`-`0x0028794D`).

`0x00287C20` rebuilds the seven panels of an open keyboard and does nothing when `0x0209AC18` is empty
(`0x00287C24`). The Config screen's binding row calls it after every change (`0x0023C660`, `0x0023C787`, `0x0023C8FF`),
and so does restoring the defaults (`0x0023E18A`), so a remap shows at once.

It picks the layout set from `0x001E0B90` (8 for French, 7 for German, 9 otherwise, `0x00287C3C`-`0x00287C55`) and the
language set from `0x00285F60` on `0x0017E270` (`0x00287C5A`-`0x00287C61`), writes the mouse labels with
`0x002875D0(task, layout set, language set)` (`0x00287C74`) and then calls the seven panel builders `0x00286010` to
`0x002870D0`, in panel order, with the same three arguments (`0x00287C85`-`0x00287CEB`).

### The seven panels

Each panel has a title and one key cell per control and profile. A cell shows the key-cap of the binding
`0x001E0BD0(profile, group, slot)` reads from the editable profiles, turned into a key-cap index by `0x001E0DA0`;
an unbound control gets the empty cap `0x6C` and the panel's dim colour.

| Panel | Built, updated | Title | Controls (group, slots) | Profiles |
|---:|---|---|---|---|
| `1` | `0x00286010`, `0x00287E60` | Character Movement, or Cursor Movement while a movement-key mode is on | LY_N, LY_P, LX_N, LX_P (1: 7, 6, 5, 4) | the first |
| `2` | `0x002862A0`, `0x002880B0` | Camera Movement, or Scroll while mode bit `0x4` is on | RY_N, RY_P, RX_N, RX_P (1: 3, 2, 1, 0) | the first |
| `3` | `0x00286500`, `0x002882F0` | Change Leader/Change Target | Up, Down, Left, Right (0: 4, 6, 7, 5) | all three |
| `4` | `0x00286780`, `0x00288500` | Cancel, Confirm, Battle Menu, Party Menu, one row each | Cross, Circle, Square, Triangle (0: 14, 13, 15, 12) | all three |
| `5` | `0x00286A80`, `0x002887B0` | Map Transparency, Display Map | L3, Select (0: 1, 0) | all three |
| `6` | `0x00286D60`, `0x00288A60` | Escape, Game Speed/Change Group, Change Group, Lock On, Reset Camera | R2, L1, R1, L2, R3 (0: 9, 10, 11, 8, 2) | all three |
| `7` | `0x002870D0`, `0x00288DB0` | Pause Game, Regular Game Speed, Double Game Speed, Quadruple Game Speed, Toggle Walk/Run | Start (0: 3), Speed1-3, WalkMode (2: 0-3) | the first |

The titles are the text ids at `0x00286010` (`0x542`, or `0x54C` when `0x001E0EE0` reports any of mode bits under mask `0x7`),
`0x002862A0` (`0x547`, or `0x58E` with mode bit `0x4` from `0x001E0F00(2)`) and `0x00286500` (`0x561`), and the per-row tables
at `0x00915DD0` (panel 4), `0x00286AA4`-`0x00286AAF` (panel 5), `0x00915DE0` (panel 6) and `0x00915DF0` with `0x0028711E`
(panel 7). With mode bit `0x4` on, panel 6 reads the second table at `0x00915E00` instead: Escape,
Previous, Next, Zoom and Reset Camera (`0x00286E8D`-`0x00286EC0`). In panel 7 an unbound control hides its cell
(`0x0028735A`).

### The keyboard picture

The picture has one cell per key-cap index: 104 keys, then the mouse codes 1 and 3; index 106 is code 0. The index of a control
code is its position in the 107-entry table `0x01DF0E80` (`0x00197790`), and `0x00197800` reads the code back.
The search covers indices 0-105 only, so it answers -1 for code 0; only `0x00197800`, which accepts an index
below 107, reads index 106 back as code 0. When
the debug settings object's byte `+0xC3D` is set, both use `0x01DF1030` instead, whose first 21 entries are the
codes 132-152 in place of Escape, F1-F12, the accent key and 1-7.

Each update colours the picture in two passes:

1. `0x00289040` lights every cell whose key is held (`0x001E0E70` on the cell's index, `0x002890C7`) and gives the
   others the base colour.
   - It walks the picture's cells, counted by bits `0x3FFFC` of the picture's `+0x50` (`(+0x50 >> 2) & 0xFFFF`,
     `0x00289085`, `0x0028916D`-`0x00289179`); a cell's index is the word `+0x0A` of its data (`0x002890C3`).
   - A held cell gets colour entry 1 and bit `0x1` set in its flag word (`0x002890D4`-`0x002890D8`); any other cell gets
     colour entry 10, the base colour, and that bit cleared (`0x002890DE`-`0x002890E2`). The entry's 16 colour bytes
     `+0x28`-`+0x37` are copied to the cell's sprite (`0x002890F6`-`0x0028916A`).
   - The colour entries are the pointer list at `+0x10` of the block `0x002AB860` returns, `[0x0209CC40]` + `0x1098`.
2. `0x002891A0` gives every key bound in any profile to a panel's control that panel's colour, unless it is held
   (`0x00287D10`, indexes below `0x68` only). `0x00289830` does the same for the movement keys of an active
   movement-key block (`0x001E0DC0`), in the colour of panel 3.
   - `0x00287D10(picture, slots, colour entry, count, group)` reads all three profiles for every panel, also for
     panels 1, 2 and 7, which list only the first (`0x00287D50`-`0x00287E35`); panel n's keys take colour entry n + 1.
   - `0x002891A0` calls it for panels 1 to 5, then panel 7's Start and its group 2 slots, then panel 6, and then calls
     `0x00289830` with entry 4 (`0x00289281`-`0x00289365`), so a key bound to controls of two panels shows the colour of
     the later call.

`0x001E0E70` sends codes 1 and 3 to the mouse device (`0x0079E6D0`) and any other code to the keyboard
(`0x0079E6A0`).

### The mouse

`0x00289390` lights the mouse cells, and skips the work while `0x00228480` answers non-zero:

- cells 0 and 2 while mouse code 1 is held, cells 1 and 3 while code 3 is held (`0x001E0E00(0)`, `0x001E0E00(2)`);
- cells 4 and 6 while the wheel is turning (`0x001E0E30`) with a positive notch total (`0x001E0D80`), cells 5 and 7
  with a negative one.

`0x002875D0` writes the mouse panel's four labels: Camera Movement, Confirm, Cancel and Cursor Movement
(`0x547`, `0x551`, `0x552`, `0x54C`).

### Key-cap sets

A cell's picture is one entry of a two-level set table on its sprite sheet. The 21 keys listed at `0x01E0C3F0`,
whose caps carry words (Backspace, Enter, both Shift and Control keys, Space, Insert to Page Down, Numpad Enter,
the two mouse buttons and the five unnamed codes 124 and 126-129), take the language set; every other key takes
the layout set.

| Windows keyboard layout (`0x001E0B90`) | Layout set |
|---|---:|
| French, `0x40C` | `8` |
| German, `0x407` | `7` |
| any other | `9` |

`0x00285F60` turns the game language from `0x0017E270` into the language set: `fr` 6, `de` 5, `it` 4, `es` 3, `kr` 0,
`ch` 2, `cn` 1, and `en`, `jp` and anything else 9.

## State

Two cells tell the keyboard that a License Board panel is up ([License Board screen](../Menus-And-HUD/license-board-screen.md)).
When the task is built and either is set, it moves itself to the second draw pass (`0x00247730(self, 1)`,
`0x00287BE3`-`0x00287BFD`), so it is drawn over the panel. Each panel's procedure, when it is destroyed (message 18) and
the screen closed itself with `0x02CA9678` set, clears its cell and `0x02CA9678` and puts an open keyboard back in the
first pass (`0x00247730(keyboard, 0)`; `0x00558D14`-`0x00558D3D`, `0x0056190D`-`0x00561936`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA8FE0` | `void*` | 0 | the chooser panel's cell: `0x00558C40`, from the board chooser `0x00557DB0` (`0x00557EDD`, `0x005587AE`), builds a `0xD0`-byte panel with procedure `0x00558CE0` and, when the build succeeds, copies the chooser's `+0xE8` here (`0x00558C95`-`0x00558CB2`) | `0x00558C40` (`0x00558CB2`); `0x00558CE0`, 0 (`0x00558D2A`) | `0x002878E0` (`0x00287BE3`) |
| `0x02CA8FE8` | `void*` | 0 | the second panel's cell: `0x00561830`, from `0x0055DBD0` (`0x0055DC96`) and `0x0055E9E0` (`0x0055EDC8`), builds a `0xF8`-byte panel with procedure `0x005618E0` and stores the panel here, keeping the old value when the build fails (`0x00561885`-`0x005618A4`) | `0x00561830` (`0x005618A4`); `0x005618E0`, 0 (`0x00561923`) | `0x002878E0` (`0x00287BEC`); `0x00561830` (`0x00561899`) |

No other instruction reaches these two.

## Modding notes

- F9 is read as code 73 directly (`0x0017DE60`), not through the keymap, and 73 is not a reserved code, so a
  control bound to F9 also toggles the keyboard.
- The panels list fixed slots: remapping changes the key a panel shows, never its title or row.
- Panels 1, 2 and 7 show the first profile only.

## Related

- [Controls](controls.md) - the movement-key modes and the input manager.
- [Control remapping](control-remapping.md) - the binding rows that refresh the keyboard.
- [Keymap file](keymap-file.md) - the profiles the panels read.
- [Control names](control-names.md) - the codes behind every key.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 12 calls with 3 other topics</summary>

**Items, equipment, shops and licenses** (explained on [license board screen](../Menus-And-HUD/license-board-screen.md), [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md))

| Function | | Functions |
|---|---|---|
| `0x00557DB0` | calls | `0x00323630`, `0x00323670`, `0x003236B0`, `0x003236F0`, `0x00323740` |
| `0x0055DBD0` | calls | `0x00323630` |
| `0x0055E9E0` | calls | `0x00323630` |
| `0x005618E0` | calls | `0x00323630`, `0x00323670`, `0x003236B0` |

**Graphics** (explained on [license board screen](../Menus-And-HUD/license-board-screen.md))

| Function | | Functions |
|---|---|---|
| `0x00557DB0` | calls | `0x003B2D80` |

**Saving, loading and settings** (explained on [game application](../Engine-Core/game-application.md))

| Function | | Functions |
|---|---|---|
| `0x002814E0` | is called by | `0x00582860` |

</details>
