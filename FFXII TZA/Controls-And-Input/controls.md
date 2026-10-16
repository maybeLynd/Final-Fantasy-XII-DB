---
title: "Controls: how a key, button or stick becomes a game action, the control codes each device answers to, and how presses, holds and repeats are told apart"
kind: "system"
category: "Controls and input"
summary: "How input reaches the game: the input manager and its poll, the three bands of control codes and the device each reads, the records that turn codes into a 16-button mask and four stick bytes, the movement-key modes, the 16-frame channel history, how a press, a hold, a release and a menu repeat are made, the stick dead zone and the stick-to-direction bits, the button words the game reads each frame, the confirm and cancel buttons, and the six controls read straight from the keymap."
addresses: "01F7FFE0, 00196FF0, 00197160, 01DF1480, 0035F420, 0035FAC0, 0035FBD0, 002498B0, 02F97360"
---

## What the player sees

- The keyboard, a pad and the mouse all drive the same sixteen buttons and two sticks.
- Holding a direction in a menu moves once, waits a moment, then repeats.
- Pressing Up and Down together, or Left and Right together, counts as neither.
- A small push of a stick does nothing; a larger push of the left stick also works as a direction button.
- Which of Circle and Cross confirms follows the Config setting.

## How it works

### The input manager

The manager is a `0x40`-byte object whose pointer is at `01F7FFE0`. `00198750` creates it, called only from
`0017D571`, and `00198790` returns it. Its start-up `00195060` clears the three keymap profiles (`001950A2`), reads
[keymap.ini](keymap-file.md), checks it and publishes it (`001950DA`) or installs the defaults (`001950EB`).

| Field | Meaning | Read at |
|---|---|---|
| `+0x08`, `+0x09` | invert the right stick's X and Y | `0019740F`, `0019751A`, `001975CB` |
| `+0x0C`, `+0x10` | mouse wheel notches, total and this frame | `0019739A`, `001973A4` |
| `+0x39` | poll on or off | `0019701D` |
| `+0x3A` | movement-key mode bits 0, 1 and 2 | `00197040`-`001970F8` |
| `+0x3B` | rebuild the records before the next poll | `00197032` |

### One poll

The device poll runs from the vsync callback `0035EC90`, installed at `0035E943`, through `0035FCA0` and `0035F420`.
`0035F420` reaches the manager's poll `00196FF0(manager, frame)` through two thunks: `00862670` jumps to `001E09B0`,
which calls it at `001E09D3`, and `00862680` jumps to `001E09E0`, which calls it through a pointer. The poll runs in
this order:

1. With `+0x39` at 0 it returns at once (`0019701D`).
2. It updates every device (`007999E0`, `0019702D`), which lists them again after a pad arrives
   ([Controllers](controllers.md)).
3. With `+0x3B` set it copies the published profiles back into the records, rebuilds the movement-key blocks and
   clears the flag (`0019703B`-`00197073`).
4. It starts the 18-byte frame: a button mask of `0xFFFF`, four stick bytes of `0x80` and twelve zero bytes
   (`00197085`-`001970A9`).
5. It runs the translator `00197160` over the five records at `01DF1480` (`001970B0`), then over the three at
   `01F80550` when mode bit 1 is set, and the three at `01F80970` when bit 0 or 2 is set (`001970C8`-`001970FE`).
6. It copies the frame out (`0019711D`).

### Control codes

A record holds sixteen button codes and sixteen axis entries, `0x15C` bytes apart. The translator tests each button
code against three bands (`001971C5`-`00197218`):

| Codes | Device | Read by |
|---|---|---|
| 1-3 | mouse buttons | `0079E6D0` |
| 11-27 | any of up to 18 pads | `0079E650` |
| 28-152 | the keyboard | `0079E6A0`, keyboard 0 |

A code in no band, such as 0, 4-10 or 153 and up, is never polled. While `001C1990()` reports state 1 and `00228480`
answers 0, the translator skips the band tests (`001971B2`-`001971C3`), and mode 3 leaves the sticks centred. A held code clears its button's bit (`0019723D`), so
the mask is active-low. [Control names](control-names.md) lists the codes by name.

### Axis entries

Each axis entry is `{mode, axis, codeA, codeB}`, dispatched on its mode (`001972A0`-`001972C1`):

| Mode | Effect on stick byte i |
|---:|---|
| 1 | `0xFF` while codeA is held (`00197680`) |
| 2 | codeA and codeB push the byte down and up by `0x7F` and `0x80`; for entries 0 and 1 the right stick's invert flags swap them, and entries 2 and 3 always push up with codeA (`0019748E`) |
| 3 | the pad stick `axis`, scaled from -1..1 to 0..255, with axes 2 and 3 flipped and flipped again by the invert flags (`001973E5`) |
| 4 | mouse: buttons through the backend bytes `+0x170`-`+0x172`, and code 3 as the wheel, one notch per 120 (`001972C7`-`001973BC`) |

All records add into the same frame, so a key and a pad stick move the same byte.

### The records

| Record | Address | Holds |
|---:|---|---|
| 0 | `01DF1480` | the pad: its sixteen buttons and both sticks, fixed in the file |
| 1 | `01DF15DC` | the mouse, filled at start-up by the static initialiser `0015C280` |
| 2-4 | `01DF1738`, `01DF1894`, `01DF19F0` | the three keyboard profiles of keymap.ini |

The mouse record is zero in the file. `0015C280` copies its 16 button codes from `01F800F0`, which is zero in the file
and has no other reader, so the mouse record has no buttons. It then copies its axis entries from `01DF0D80`:
entries 0 and 1 are `{4, 2, 0, 0}` and `{4, 3, 0, 0}`, entry 4 is `{4, 4, 3, 0}`, entry 6 is `{4, 4, 0, 3}`, and the
rest are zero.

The mode-4 arm acts only on an entry whose second value is 4 and whose third is 11, 12 or 13, the
mouse buttons, or 3, the wheel (`001972C7`-`0019734F`). So entry 4 is the wheel, and entries 0, 1 and 6 do nothing:
entry 6's 3 is in its fourth value, which this arm does not read.

The two extra blocks turn movement keys into direction buttons. Mode bit 1 makes `00196DF0` build three records at
`01F80550` whose Up, Right, Down and Left are each profile's movement keys. Mode bits 0 and 2 build the same at
`01F80970` with L2 and R2 added (`00196EE0`, `00196C40`); bit 2 also clears the right-stick keys of records 2-4
(`00196D34`).

### Channel history

Each poll writes one 36-byte frame into a 16-frame ring at `+0x44` of the channel record `022CAE90` (`0035F420`):

1. The sixteen per-button bytes are the frame's stick and pressure bytes in the order of `01EF9238`.
2. `0035FAC0` makes the held mask from the frame's mask. Up with Down (`0x50`) and Left with Right (`0xA0`) cancel each
   other (`0035FB6D`-`0035FB7E`). It writes held, pressed and released for set 0, the buttons, and held for set 1
   (`0035FB92`-`0035FBBD`).
3. `0035F760` snaps a stick inside a radius of `0x20` to the centre (`0035F7BD`, `0035F83F`). A left stick past `0x68`
   adds the Up, Right, Down or Left bit to set 1 (`0035F8AE`), which is the buttons plus the left stick as directions.

### Repeats

`0035FBD0` makes the repeat mask of each set from eight button groups. A change fires at once and waits 12 polls
(`0035FC5D`); a group still held fires again every 5 polls (`0035FC35`, `0035FC52`). The two counts are stored at
`0035F312`. Left and Right keep counting through a change of direction (`0035FC3C`).

### The button words

`002498B0` rebuilds the words at `02F97360` once per game frame, ORing every poll since the last game frame. The
table is channel 0; channel 1's words follow at `02F97374`, and a filtered copy of channel 0 at `02F97388` is masked
by the block at `02F973A0` when that block is not zero:

| Word | Holds |
|---|---|
| `02F97360` | held, set 1 |
| `02F97362` | pressed, set 1 |
| `02F97364` | repeat, set 1 |
| `02F97366` | released, set 1 |
| `02F97368` | held, set 0 |
| `02F9736A` | pressed, set 0 |
| `02F9736C` | repeat, set 0 |
| `02F9736E` | released, set 0 |
| `02F97370`-`02F97373` | left X, left Y, right X, right Y, from -128 to 127, zero below 50 (`003590A0`) |

Bit i of every mask is button i in this order: Select, L3, R3, Start, Up, Right, Down, Left, L2, R2, L1, R1, Triangle,
Circle, Cross, Square. It is called from the main loop (`0022B908`) and from `0022A7F6`, `0022BC50` and `00249C4D`.

### Confirm and cancel

`0022A4F0` sets the confirm mask `01E0C2A0` and the cancel mask `01E0C2A4` to Circle and Cross, `0x2000` and `0x4000`,
when the Config setting `+0x64` is 0 (`0017E210`), and the other way round otherwise. It also stores the setting's
answer at `01FD4A64` (`0022A510`).

### Controls read straight from the keymap

Six controls are not in the published records. Their readers ask `00197710(manager, 0, group, slot)` for the first
profile's code, read from `01F80F90` (`0019775A`-`0019776F`), and test it on the keyboard only:

| Control | Reader | Read by |
|---|---|---|
| L2, group 0 slot 8 | `0017DDC0` | the target cursor (`003C9141`) |
| R2, group 0 slot 9 | `0017DE10` | the input arbiter (`002541D4`), [Escape Mode](escape.md) |
| Speed1-3, group 2 slots 0-2 | `0017DEA0` | `0022AA59` |
| WalkMode, group 2 slot 3 | `0017DFC0` | the party's movement (`00359518`) |

## Modding notes

- A pad code (11-27) written into keymap.ini is polled like a key, but the six controls above ignore it.
- Binding L2, R2, a speed key or WalkMode to a mouse button is accepted and never fires, because those readers test the
  keyboard band only.
- The repeat timing is two bytes per channel, written at `0035F312`: 12 polls before the first repeat, then 5.
- The right-stick invert flags are manager `+0x08` and `+0x09`.

## Related

- [keymap.ini](keymap-file.md) - the bindings and their slots.
- [Control names](control-names.md) - every control code by name.
- [Controllers](controllers.md) - how pads are found.
- [Action availability](action-availability.md) - when a press is refused.
- [Escape Mode](escape.md) - the R2 control.
