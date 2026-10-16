---
title: "On-Screen Keyboard: the F9 overlay that shows every keyboard binding, its seven panels, the key colours and the keys that light up while held"
kind: "system"
category: "Controls and input"
addresses: "0017DE60, 0027E9E0, 002878E0, 0209AC18, 0209AC50, 00287C20, 002891A0, 00289040, 00197790, 01DF0E80"
---

## What the player sees

- F9 shows the On-Screen Keyboard and F9 hides it again; a label on it reads "Hide On-Screen Keyboard".
- It shows a picture of the keyboard and the mouse, and panels such as Character Movement, Camera Movement,
  Confirm, Cancel, Escape and Pause Game with the keys bound to each.
- Every key in the picture takes the colour of the panel whose control it is bound to, and a key lights up
  while it is held.
- An unbound control shows an empty key.
- The key caps follow the Windows keyboard layout (French and German layouts have their own) and the game
  language.

## How it works

### Opening and closing

`0017DE60` answers whether F9 was pressed: it reads and clears the latch of code 73 (`Key_F9`) on keyboard 0
(`0079AE90`, `0017DE69`-`0017DE77`), and on a press it also clears the input manager's last-device flag `+0x38` through `001E1100(0)`.
Three frame handlers call it while the keyboard is closed and call `0027E9E0` on a press: the field frame
(`0022AB51`-`0022AB5A`), the full menu frame (`0022B984`-`0022B98D`) and the capture-backed frame
(`0022BCFA`-`0022BD03`). Each first asks `002878A0`, which returns the open flag `0209AC50`.

`0027E9E0` creates the keyboard only when `0209AC18` is empty: it starts a task of `0xC0` bytes running
`002878E0`, stores it in `0209AC18`, and sets `0209AC50` and `0209AC14` to 1 (`0027E9F3`-`0027EA3A`). A raw scan of
the executable sections for calls, jumps and `lea` to `002878E0` finds only the `lea` at `0027EA18`.

On each update (`00287A07`, `00287AC8`) the task closes itself (`00244F00`) when `0017DE60` reports F9 again
(`00287A3B`-`00287A4B`). The branch that closes on the cancel button instead (`00287A10`-`00287A34`) runs only when
`0209AC50` is 0, which `0027E9E0` never leaves it. Destroying the task clears `0209AC18` and `0209AC50` and sets
`0209AC14` (`00287953`-`0028796E`).

### The task

`002878E0` handles its messages in this order of work:

1. On creation it builds its widgets with `002432B0` from the layout at `+0xA8` of `0209AC30` (`00287B86`-`00287B9E`).
2. On a redraw (`0028797D`-`002879FD`) it resets the keyboard picture (`00287400`), colours it (`002891A0`),
   writes the mouse labels (`002875D0`), builds the seven panels and writes the hint label (`00287850`).
3. On each update (`00287A50`-`00287ABE`) it lights the held keys (`00289040`), colours the picture again
   (`002891A0`), lights the mouse (`00289390`) and updates the seven panels.

`00287C20` rebuilds the seven panels of an open keyboard and does nothing when `0209AC18` is empty
(`00287C24`). The Config screen's binding row calls it after every change (`0023C660`, `0023C787`, `0023C8FF`),
and so does restoring the defaults (`0023E18A`), so a remap shows at once.

### The seven panels

Each panel has a title and one key cell per control and profile. A cell shows the key-cap of the binding
`001E0BD0(profile, group, slot)` reads from the editable profiles, turned into a key-cap index by `001E0DA0`;
an unbound control gets the empty cap `0x6C` and the panel's dim colour.

| Panel | Built, updated | Title | Controls (group, slots) | Profiles |
|---:|---|---|---|---|
| `1` | `00286010`, `00287E60` | Character Movement, or Cursor Movement while a movement-key mode is on | LY_N, LY_P, LX_N, LX_P (1: 7, 6, 5, 4) | the first |
| `2` | `002862A0`, `002880B0` | Camera Movement, or Scroll while mode bit 2 is on | RY_N, RY_P, RX_N, RX_P (1: 3, 2, 1, 0) | the first |
| `3` | `00286500`, `002882F0` | Change Leader/Change Target | Up, Down, Left, Right (0: 4, 6, 7, 5) | all three |
| `4` | `00286780`, `00288500` | Cancel, Confirm, Battle Menu, Party Menu, one row each | Cross, Circle, Square, Triangle (0: 14, 13, 15, 12) | all three |
| `5` | `00286A80`, `002887B0` | Map Transparency, Display Map | L3, Select (0: 1, 0) | all three |
| `6` | `00286D60`, `00288A60` | Escape, Game Speed/Change Group, Change Group, Lock On, Reset Camera | R2, L1, R1, L2, R3 (0: 9, 10, 11, 8, 2) | all three |
| `7` | `002870D0`, `00288DB0` | Pause Game, Regular Game Speed, Double Game Speed, Quadruple Game Speed, Toggle Walk/Run | Start (0: 3), Speed1-3, WalkMode (2: 0-3) | the first |

The titles are the text ids at `00286010` (`0x542`, or `0x54C` when `001E0EE0` reports any of mode bits 0-2),
`002862A0` (`0x547`, or `0x58E` with mode bit 2 from `001E0F00(2)`) and `00286500` (`0x561`), and the per-row tables
at `00915DD0` (panel 4), `00286AA4`-`00286AAF` (panel 5), `00915DE0` (panel 6) and `00915DF0` with `0028711E`
(panel 7). With mode bit 2 on, panel 6 reads the second table at `00915E00` instead: Escape,
Previous, Next, Zoom and Reset Camera (`00286E8D`-`00286EC0`). In panel 7 an unbound control hides its cell
(`0028735A`).

### The keyboard picture

The picture has one cell per key-cap index: 104 keys, then the mouse codes 1 and 3; index 106 is code 0. The index of a control
code is its position in the 107-entry table `01DF0E80` (`00197790`), and `00197800` reads the code back.
The search covers indices 0-105 only, so it answers -1 for code 0; only `00197800`, which accepts an index
below 107, reads index 106 back as code 0. When
the debug settings object's byte `+0xC3D` is set, both use `01DF1030` instead, whose first 21 entries are the
codes 132-152 in place of Escape, F1-F12, the accent key and 1-7.

Each update colours the picture in two passes:

1. `00289040` lights every cell whose key is held (`001E0E70` on the cell's index, `002890C7`) and gives the
   others the base colour.
2. `002891A0` gives every key bound in any profile to a panel's control that panel's colour, unless it is held
   (`00287D10`, indexes below `0x68` only). `00289830` does the same for the movement keys of an active
   movement-key block (`001E0DC0`), in the colour of panel 3.

`001E0E70` sends codes 1 and 3 to the mouse device (`0079E6D0`) and any other code to the keyboard
(`0079E6A0`).

### The mouse

`00289390` lights the mouse cells, and skips the work while `00228480` answers non-zero:

- cells 0 and 2 while mouse code 1 is held, cells 1 and 3 while code 3 is held (`001E0E00(0)`, `001E0E00(2)`);
- cells 4 and 6 while the wheel is turning (`001E0E30`) with a positive notch total (`001E0D80`), cells 5 and 7
  with a negative one.

`002875D0` writes the mouse panel's four labels: Camera Movement, Confirm, Cancel and Cursor Movement
(`0x547`, `0x551`, `0x552`, `0x54C`).

### Key-cap sets

A cell's picture is one entry of a two-level set table on its sprite sheet. The 21 keys listed at `01E0C3F0`,
whose caps carry words (Backspace, Enter, both Shift and Control keys, Space, Insert to Page Down, Numpad Enter,
the two mouse buttons and the five unnamed codes 124 and 126-129), take the language set; every other key takes
the layout set.

| Windows keyboard layout (`001E0B90`) | Layout set |
|---|---:|
| French, `0x40C` | `8` |
| German, `0x407` | `7` |
| any other | `9` |

`00285F60` turns the game language from `0017E270` into the language set: `fr` 6, `de` 5, `it` 4, `es` 3, `kr` 0,
`ch` 2, `cn` 1, and `en`, `jp` and anything else 9.

## Modding notes

- F9 is read as code 73 directly (`0017DE60`), not through the keymap, and 73 is not a reserved code, so a
  control bound to F9 also toggles the keyboard.
- The panels list fixed slots: remapping changes the key a panel shows, never its title or row.
- Panels 1, 2 and 7 show the first profile only.

## Related

- [Controls](controls.md) - the movement-key modes and the input manager.
- [Control remapping](control-remapping.md) - the binding rows that refresh the keyboard.
- [Keymap file](keymap-file.md) - the profiles the panels read.
- [Control names](control-names.md) - the codes behind every key.
