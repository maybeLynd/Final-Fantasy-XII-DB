---
title: "Controls: how a key, button or stick becomes a game action, the control codes each device answers to, and how presses, holds and repeats are told apart"
kind: "system"
category: "Controls and input"
addresses: "0x01F7FFE0, 0x00196FF0, 0x00197160, 0x01DF1480, 0x0035F420, 0x0035FAC0, 0x0035FBD0, 0x002498B0, 0x02F97360"
---

## What the player sees

- The keyboard, a pad and the mouse all drive the same sixteen buttons and two sticks.
- Holding a direction in a menu moves once, waits a moment, then repeats.
- Pressing Up and Down together, or Left and Right together, counts as neither.
- A small push of a stick does nothing; a larger push of the left stick also works as a direction button.
- Which of Circle and Cross confirms follows the Config setting.

## How it works

### The input manager

The manager is a `0x40`-byte object whose pointer is at `0x01F7FFE0`. `0x00198750` creates it, called only from
`0x0017D571`, and `0x00198790` returns it. Its start-up `0x00195060` clears the three keymap profiles (`0x001950A2`), reads
[keymap.ini](keymap-file.md), checks it and publishes it (`0x001950DA`) or installs the defaults (`0x001950EB`).

| Field offset | Meaning | Read at |
|---|---|---|
| `+0x08`, `+0x09` | invert the right stick's X and Y | `0x0019740F`, `0x0019751A`, `0x001975CB` |
| `+0x0C`, `+0x10` | mouse wheel notches, total and this frame | `0x0019739A`, `0x001973A4` |
| `+0x39` | poll on or off | `0x0019701D` |
| `+0x3A` | movement-key mode bits 0, 1 and 2 | `0x00197040`-`0x001970F8` |
| `+0x3B` | rebuild the records before the next poll | `0x00197032` |

### One poll

The device poll runs from the vsync callback `0x0035EC90`, installed at `0x0035E943`, through `0x0035FCA0` and `0x0035F420`.
`0x0035F420` reaches the manager's poll `0x00196FF0(manager, frame)` through two thunks: `0x00862670` jumps to `0x001E09B0`,
which calls it at `0x001E09D3`, and `0x00862680` jumps to `0x001E09E0`, which calls it through a pointer. The poll runs in
this order:

1. With `+0x39` at 0 it returns at once (`0x0019701D`).
2. It updates every device (`0x007999E0`, `0x0019702D`), which lists them again after a pad arrives
   ([Controllers](controllers.md)).
3. With `+0x3B` set it copies the published profiles back into the records, rebuilds the movement-key blocks and
   clears the flag (`0x0019703B`-`0x00197073`).
4. It starts the 18-byte frame: a button mask of `0xFFFF`, four stick bytes of `0x80` and twelve zero bytes
   (`0x00197085`-`0x001970A9`).
5. It runs the translator `0x00197160` over the five records at `0x01DF1480` (`0x001970B0`), then over the three at
   `0x01F80550` when mode bit 1 is set, and the three at `0x01F80970` when bit 0 or 2 is set (`0x001970C8`-`0x001970FE`).
6. It copies the frame out (`0x0019711D`).

### Control codes

A record holds sixteen button codes and sixteen axis entries, `0x15C` bytes apart. The translator tests each button
code against three bands (`0x001971C5`-`0x00197218`):

| Codes | Device | Read by |
|---|---|---|
| `1`-`3` | mouse buttons | `0x0079E6D0` |
| `11`-`27` | any of up to 18 pads | `0x0079E650` |
| `28`-`152` | the keyboard | `0x0079E6A0`, keyboard 0 |

A code in no band, such as 0, 4-10 or 153 and up, is never polled. While `0x001C1990()` reports state 1 and `0x00228480`
answers 0, the translator skips the band tests (`0x001971B2`-`0x001971C3`), and mode 3 leaves the sticks centred. A held code clears its button's bit (`0x0019723D`), so
the mask is active-low. [Control names](control-names.md) lists the codes by name.

### Axis entries

Each axis entry is `{mode, axis, codeA, codeB}`, dispatched on its mode (`0x001972A0`-`0x001972C1`):

| Mode | Effect on stick byte i |
|---:|---|
| `1` | `0xFF` while codeA is held (`0x00197680`) |
| `2` | codeA and codeB push the byte down and up by `0x7F` and `0x80`; for entries 0 and 1 the right stick's invert flags swap them, and entries 2 and 3 always push up with codeA (`0x0019748E`) |
| `3` | the pad stick `axis`, scaled from -1..1 to 0..255, with axes 2 and 3 flipped and flipped again by the invert flags (`0x001973E5`) |
| `4` | mouse: buttons through the backend bytes `+0x170`-`+0x172`, and code 3 as the wheel, one notch per 120 (`0x001972C7`-`0x001973BC`) |

All records add into the same frame, so a key and a pad stick move the same byte.

### The records

| Record | Address | Holds |
|---:|---|---|
| 0 | `0x01DF1480` | the pad: its sixteen buttons and both sticks, fixed in the file |
| 1 | `0x01DF15DC` | the mouse, filled at start-up by the static initialiser `0x0015C280` |
| 2-4 | `0x01DF1738`, `0x01DF1894`, `0x01DF19F0` | the three keyboard profiles of keymap.ini |

The mouse record is zero in the file. `0x0015C280` copies its 16 button codes from `0x01F800F0`, which is zero in the file
and has no other reader, so the mouse record has no buttons. It then copies its axis entries from `0x01DF0D80`:
entries 0 and 1 are `{4, 2, 0, 0}` and `{4, 3, 0, 0}`, entry 4 is `{4, 4, 3, 0}`, entry 6 is `{4, 4, 0, 3}`, and the
rest are zero.

The mode-4 arm acts only on an entry whose second value is 4 and whose third is 11, 12 or 13, the
mouse buttons, or 3, the wheel (`0x001972C7`-`0x0019734F`). So entry 4 is the wheel, and entries 0, 1 and 6 do nothing:
entry 6's 3 is in its fourth value, which this arm does not read.

The two extra blocks turn movement keys into direction buttons. Mode bit 1 makes `0x00196DF0` build three records at
`0x01F80550` whose Up, Right, Down and Left are each profile's movement keys. Mode bits 0 and 2 build the same at
`0x01F80970` with L2 and R2 added (`0x00196EE0`, `0x00196C40`); bit 2 also clears the right-stick keys of records 2-4
(`0x00196D34`).

### Channel history

Each poll writes one 36-byte frame into a 16-frame ring at `+0x44` of the channel record `0x022CAE90` (`0x0035F420`):

1. The sixteen per-button bytes are the frame's stick and pressure bytes in the order of `0x01EF9238`.
2. `0x0035FAC0` makes the held mask from the frame's mask. Up with Down (`0x50`) and Left with Right (`0xA0`) cancel each
   other (`0x0035FB6D`-`0x0035FB7E`). It writes held, pressed and released for set 0, the buttons, and held for set 1
   (`0x0035FB92`-`0x0035FBBD`).
3. `0x0035F760` snaps a stick inside a radius of `0x20` to the centre (`0x0035F7BD`, `0x0035F83F`). A left stick past `0x68`
   adds the Up, Right, Down or Left bit to set 1 (`0x0035F8AE`), which is the buttons plus the left stick as directions.

Byte 0 of a frame is the device state, the second argument of `0x0035F420` (`0x0035F572`). `0x0035FCA0` passes 1, the
answer of `0x0053DD10`, which always returns 1 (`0x0035FCF0`-`0x0035FD85`). `0x0035EEB0(channel, i, back)` reads per-button
byte i of a frame, the newest for `back` 0, and `0x0046DB10(i)` is `0x0035EEB0(0, i, 0)`.

### The device-state count

`0x00227D70`, called by the Start handler `0x002287D0` (`0x00228885`), reads the state byte of channel 0's newest frame
through `0x0035F150(0, 0, 0)`:

- state 1 sets the count `0x01E027F8` to 6 and answers 0; any other non-zero state sets it to 6 and answers 2;
- state 0 counts `0x01E027F8` down and answers 2 while it was above 0, and answers 1 once it is 0.

Every frame `0x0035F420` writes holds state 1, so once channel 0 has been polled the answer is 0.

### Repeats

`0x0035FBD0` makes the repeat mask of each set from eight button groups. A change fires at once and waits 12 polls
(`0x0035FC5D`); a group still held fires again every 5 polls (`0x0035FC35`, `0x0035FC52`). The two counts are stored at
`0x0035F312`. Left and Right keep counting through a change of direction (`0x0035FC3C`).

### The button words

`0x002498B0` rebuilds the words at `0x02F97360` once per game frame, ORing every poll since the last game frame. The
table is channel 0; channel 1's words follow at `0x02F97374`, and a filtered copy of channel 0 at `0x02F97388` is masked
by the block at `0x02F973A0` when that block is not zero:

| Word | Holds |
|---|---|
| `0x02F97360` | held, set 1 |
| `0x02F97362` | pressed, set 1 |
| `0x02F97364` | repeat, set 1 |
| `0x02F97366` | released, set 1 |
| `0x02F97368` | held, set 0 |
| `0x02F9736A` | pressed, set 0 |
| `0x02F9736C` | repeat, set 0 |
| `0x02F9736E` | released, set 0 |
| `0x02F97370`-`0x02F97373` | left X, left Y, right X, right Y, from -128 to 127, zero below 50 (`0x003590A0`) |

Bit i of every mask is button i in this order: Select, L3, R3, Start, Up, Right, Down, Left, L2, R2, L1, R1, Triangle,
Circle, Cross, Square. It is called from the main loop (`0x0022B908`) and from `0x0022A7F6`, `0x0022BC50` and `0x00249C4D`.

### Confirm and cancel

`0x0022A4F0` sets the confirm mask `0x01E0C2A0` and the cancel mask `0x01E0C2A4` to Circle and Cross, `0x2000` and `0x4000`,
when the Config setting `+0x64` is 0 (`0x0017E210`), and the other way round otherwise. It also stores the setting's
answer at `0x01FD4A64` (`0x0022A510`).

Among the readers of `0x01FD4A64`, `0x0022A540` answers whether it is 0, for the input filter `0x001967D0` (`0x00196803`), and
the script verbs `get_pad_ok` `0x518` and `get_pad_cancel` `0x519` return the confirm and cancel masks through
`0x002E12B0` and `0x002E1290` (handlers `0x0034AF20` and `0x0034B290`).

### The mouse wheel in menus

`0x002D3900(list)` runs a menu list's cursor with the wheel added to the buttons (`0x002D392B`-`0x002D39C5`):

1. It takes held, pressed and repeat of set 0 (`0x02F97368`, `0x02F9736A`, `0x02F9736C`).
2. Every second call (the count `0x0209E65C` against `0x01E0CF88`, 2) it reads and clears the wheel's notch total with
   `0x001E0A10` (manager `+0x0C`, cleared by `0x001986D0`).
3. With notches, 3 or more (`0x01E0CF84`) count as one when the list's `+0xE8` is below 13 (`0x002D397C`). A positive
   total adds Up (`0x10`) to pressed and repeat, a negative one Down (`0x40`).
4. It then moves the list once per notch with `0x002D3BA0`, stopping at the first or last row (`0x002D4F10`) or when
   `0x002D0580` holds the cursor.
5. Without notches it moves the list once with the plain buttons.

`0x002D0580` arms a stop (`0x0209E660`) when the cursor is one row past the row at `+0xF6` while moving up, or one row
before the last while moving down. While the stop is armed, the cursor is on that end row and the wheel is still
turning (`0x001E0E30`), it answers 1; with the cursor anywhere else it disarms. `0x002D3A50` is the
same with the filtered copy `0x02F97390`-`0x02F97394`, for the gambit screen (`0x0056984D`, `0x0056B871`, and `0x00569CF5` in `0x005691E0`), and `0x002D09F0`
moves a list with the filtered copy and no wheel (`0x00560D48`).

The Config screen's lists (`0x0023F240`, `0x00240DE0`), the clan primer's (`0x00570CE0`) and `0x00284EC0`, `0x002A9980`,
`0x002C2F90` and `0x002C4220` repeat the same pacing with their own code. The debug menu code `0x001D1660` can change the
pacing through `0x002D4F70` (1-10) and `0x002D4F90` (1-5).

`0x002C2F90` and `0x002C4220` move grid cursors for `0x002C1A80`, the input step shared by the Party Menu's member list
(`0x00284EC0`), the Status and Equip screen (`0x002C2320`, `0x002C59D0`, `0x003FF360`, `0x003FDAD0`), the gambit editor
(`0x005691E0`) and `0x0055C740`:

- `0x002C2F90` moves one cursor `+0xAE8` with `0x002C2DA0(grid, dir, wrap)`: cells `0x20` apart from `+0xC8`,
  bounded by `+0xAEC` and `+0xAEE`, columns from the list's `+0xEC`, skipping empty cells. `0x002C3C80(grid, dir)`
  answers whether a move would leave the grid.
- `0x002C4220` moves a cursor `+0x7A0`, 0 to 53, over four panels at `+0xC0` with `0x002C3D70(grid, dir, wrap)`.
  Each panel's first and last cells come from the 12-byte rows of `0x00916D30`, and a move off a panel's edge
  enters the next shown panel (`+0x40` bit 0). `0x002C54B0(grid, dir)` answers whether a move would leave them.

### Pad or keyboard prompts

The input manager's byte `+0x38` records whether the pad was used last:

- `0x0079D010`, the device poll, compares every key, pad button and mouse button with its previous state, and on a
  change calls application slot 25 with 0 for a key, 1 for a pad button and 0 for a mouse button (`0x0079D087`,
  `0x0079D107`, `0x0079D181`). Slot 25 is `0x0017D1E0`, which stores the byte through `0x00198E70`.
- The translator sets it to 1 when a pad stick axis reads non-zero (`0x0019744B`), and F9 clears it (`0x0017DE60`).

`0x001E0C10` reads it (`0x00197780`). An icon in text asks `0x002AB8F0` for its button (`0x002AEBCE`). The answer is an index
in the order Circle, Triangle, L1, L2, R1, R2, L3, R3, Square, Cross, Left, Right, Up, Down:

| Icon code | Index |
|---|---|
| `0x20`, `0x21`, `0x23` | the confirm mask's button, 0 or 9; 0 when the keyboard was used last |
| `0x27` | the cancel mask's button, 0 or 9; 9 when the keyboard was used last |
| `0x22`, `0x24` | 8, Square |
| `0x25`, `0x26` | 1, Triangle |
| `0x28`, `0x29`, `0x2A`, `0x2B` | 2, 4, 3 and 5: L1, R1, L2 and R2 |

Any other code is returned unchanged. `0x002B5B60`, run by the script verb `0x5CD` (handler `0x00341030`), fills the 14
bytes at `0x01E0CE30` in that order with the key-cap index of each button's first-profile key (`0x001E0BD0`,
`0x001E0DA0`), exchanging entries 0 and 9 when the Config setting `+0x64` is not 0.

Entries 10-13 then take the
direction keys of the active movement-key block (`0x001E0DC0`, slots 7, 5, 4 and 6). With no block active that
call gives code 0, which the index search `0x00197790` never finds, since it covers indices 0-105 only; the entry
then keeps the first pass's key, the Left, Right, Up or Down binding, because both passes store only an index
other than -1 (`0x002B5B60`). A scan of rip-relative and image-base displacement
operands in the listed functions finds no other reference to `0x01E0CE30`.

### Controls read straight from the keymap

Six controls are not in the published records. Their readers ask `0x00197710(manager, 0, group, slot)` for the first
profile's code, read from `0x01F80F90` (`0x0019775A`-`0x0019776F`), and test it on the keyboard only:

| Control | Reader | Read by |
|---|---|---|
| L2, group 0 slot 8 | `0x0017DDC0` | the target cursor (`0x003C9141`) |
| R2, group 0 slot 9 | `0x0017DE10` | the input arbiter (`0x002541D4`), [Escape Mode](escape.md) |
| Speed1-3, group 2 slots 0-2 | `0x0017DEA0` | `0x0022AA59` |
| WalkMode, group 2 slot 3 | `0x0017DFC0` | the party's movement (`0x00359518`) |

### The field buttons

The input arbiter `0x00253C70` reads the field's presses once per field frame. It returns before reading a button
while Game Over is armed, bit 1 of the mode word `0x022C83E8` (`0x0035C740`; [Game over](../World-Areas-And-Travel/game-over.md)), when the byte `0x0215F1A0` is set (`0x002E12D0`),
or when `0x00228380` or the Start handler `0x002287D0` answers non-zero (`0x00253C97`-`0x00253CCC`). The buttons are read
only while `0x00265680` answers non-zero (`0x00253D0D`), from held and pressed of set 0.

While `0x003135E0` (bit 0 of `+0x5B04` of `0x02EBF190`) and `0x0035C750` (bit 4 of the mode word `0x022C83E8`, not the battle mode register `0x022C83EC` of [Escape Mode](escape.md)) both answer non-zero, the
confirm button, the four directions and Square are dropped from the presses (`0x00253D3D`-`0x00253D5E`). The arms then
run in this order, and the policy bits are those of [Action availability](action-availability.md):

| Presses | Condition | What happens |
|---|---|---|
| Triangle alone, held and pressed | policy bit 0 clear | the main menu, request 2 (`0x00253D61`-`0x00253D78`) |
| Select or L3 | see [Menus](../Menus-And-HUD/menus.md) | the map requests; `0x002500F0(mask, 2)` answers 1 when policy bit 11 is clear, `0x00236760` answers 0 and `0x002E25B0(2)` allows request 2 (`0x00253E6D`) |
| any | `0x02092730` is 0 and `0x00303EC0` answers non-zero | `0x003CA200`, and the presses are cleared (`0x00253F62`-`0x00253F70`) |
| Square | `0x02092730` is 0, policy bit 10 clear, `0x003669D0` answers 0 | `0x002F1710`, then request 1 (`0x00253F7C`-`0x00253F98`, `0x002541B9`-`0x002541C7`) |
| cancel | `0x02092730` is 0 | `0x003C8950` (`0x00253F9D`-`0x00253FA9`) |
| Left or Right | L1 not held, `0x003669D0` answers 0, `0x02092730` is 0 or 3 | unless `0x02092734` is 1 or request 5 is refused, the target-cycling route `0x0035DA80`, `0x003C8990`, `0x003C87B0(5)` (`0x00253FB3`-`0x00254044`) |
| Up or Down, or wheel notches | L1 not held, two of the nine members `0x00320040(3, i)` returns have `+0x60` not negative and flag bit 1 clear or flag `0x4008` is set, `0x02092730` is 0 or 5 | request 3; with the area's bit 15 the wheel total is cleared first (`0x00254052`-`0x002540D2`) |
| confirm or Square, or a pending pick | `0x02092730` is 0 | the interaction (`0x00254132`-`0x0025415A`), or request 1 (`0x002541A4`-`0x002541C7`) |

The helpers the arms call:

- `0x003C9570` returns the pick at `+0xCC` of the object in `0x02B47730` while its `+0xC0` bit 3 is set, and
  `0x003C9550` clears that bit; `0x003C8950` runs `0x00268620` and clears bit 1 when bit 1 is set.
- `0x003CA200` calls the callback at `+0x2A0` of the object in `0x02B47758` with message `0x1F` when that callback is set
  (`0x00273A20`) and the object's `+0x2E0` bit 4 is set.
- `0x002F1710` finishes the entry in `0x022BE7D0`: it copies the entry's second word over its first, calls its callback
  at `+0x08`, sets `+0x1C` to 1 and clears the entry's bit, numbered by `+0x18`, in `0x022BE7C0`.
- `0x002F1C50(n)` arms that entry: it takes one (`0x002F16B0`) into `0x022BE7D0` with the callback `0x002F18A0`, sets bit 1
  of hold word 10 (`0x002E1C20(10, 1)`, the words at `0x0215F1C0`), and sets the count to 0 and the length to n x
  `[0x01DFE0B4]` (n alone while `0x001EDDA0()` answers). `0x002F18A0` clears that bit (`0x002E1CA0(10, 1)`) and `0x022BE7D0`.
- `0x00267720` answers 1 only when `0x0209A2AA` is set, the controlled character exists (`0x003590D0`, `0x003588B0`), its record is not one that `0x002373A0` accepts and
`0x00233D70` refuses, no
  menu is open (`0x002E05C0`), `0x00265680` answers non-zero and `0x02099DB4` is 0.
- `0x00273950()`, asked before the interaction (`0x0025412B`) and by `0x002C6F70` and `0x002736B0`, answers 0 while policy
  bit 1 is set without bit 21 (the policy word `0x00254500`, the OR of the `0x01E0C2C0` masks of the set hold-mask bits);
  otherwise 1 when `0x02092730` is not 1, Escape Mode is not armed (`0x003669D0`) and hold-mask bit 4 is clear.
- `0x002736B0()`, from the HUD's `0x002C6F70` and `0x002C64C0`, answers 1 only when `0x00267720()` answers 1, hold-mask
  bit 4 is clear, `0x0028FA00()` and `0x00273950()` pass, and `0x0209A2C0` holds no handle or one whose class-1 or class-3
  actor has `+0x0C` bit 1 set (`0x0025B4C0`).
- `0x0028FA00()` needs the HUD part `+0x10F80` with word `+0x1D7A` bit 3 and `+0x1D78` times the controlled character's
  byte `+0x14` in the part's list `+0x1D70` above `0x3FFF`, or `+0x1D78` above `0x7F` when the character is not
  listed.
- `0x00252DE0`, from the area unload `0x002628B0`, clears `0x02092730` and `0x02092734` and sets `0x020927C8` and `0x020927CC`
  to 1 (`0x00252DF5`-`0x00252E0B`).

The R2 toggle after the arms is on [Escape Mode](escape.md).

### The field target cycle

The field's target cursor is the object in `0x02B47730`: `+0xC4` the chosen target's handle, `+0xC8` the handle it
shows, `+0xCC` the pick and `+0xC0` its state bits. `0x003C9250(mode)`, called from `0x003C87B0` and `0x003C8B70`, chooses
from the target list at `0x022C83F0` (a count, then handles from `+8`) for the controlled character `0x0035BAD0()`
(`0x022C806C`), and gives 0 without a cursor, a character or a list:

1. `0x0035DCC0` fills one 12-byte entry per handle (the handle, its screen x through `0x00249110`, its index) and
   returns the handle nearest the character (`sqrtf` of the summed squares); mode 0 returns that one.
2. `0x0035DEB0` sorts the entries by screen x; mode 3 returns the leftmost and mode 4 the rightmost.
3. Modes 1 and 2 find the current `+0xC4` with `0x0035DC90(entries, n, handle)`, the index of the entry holding that
   handle or -1, and return the entry before or after it, or 0 at either end.

The cursor's setters:

- `0x003C9420(h)` (`0x003C88CB`, `0x003C8CC8`) stores `h` at `+0xC4`, after `0x0028FE40(6, h)` and, for a new non-zero
  `h`, sound 1 (`0x00249C60(1)`); then it sets `+0xC8` as `0x003C93E0` does.
- `0x003C93E0(h)` stores `h` at `+0xC8`, or 0 when `0x00273710(h)` refuses it or it is the controlled character.
- `0x003C94A0()` (`0x003C90BB`) re-shows the target of the record `0x0035BAF0()` returns (`0x022C8078`): nothing when its
  bit 15 is set, `0x003C93E0(+8)` when its `+4` and `+8` differ (`0x003C94DD`), otherwise `+0xC8` = 0.
- `0x003C94F0()` does the same only while `+0xC0` bit 2 is set, and otherwise clears `+0xC8`; the menu steps
  `0x00276D30`, `0x002778C0`, `0x00279E20` and `0x0027B880` call it.
- `0x003C9370(h)` answers 1 when `h` is one of the handles of the target list `0x022C83F0` (`0x0035D3E0`) and 0
  otherwise; `0x003C87B0` (`0x003C8847`) and `0x003C8B70` (`0x003C8FB2`) call it.

## Modding notes

- A pad code (11-27) written into keymap.ini is polled like a key, but the six controls above ignore it.
- Binding L2, R2, a speed key or WalkMode to a mouse button is accepted and never fires, because those readers test the
  keyboard band only.
- The repeat timing is two bytes per channel, written at `0x0035F312`: 12 polls before the first repeat, then 5.
- The right-stick invert flags are manager `+0x08` and `+0x09`.

## Related

- [keymap.ini](keymap-file.md) - the bindings and their slots.
- [Control names](control-names.md) - every control code by name.
- [Controllers](controllers.md) - how pads are found.
- [Action availability](action-availability.md) - when a press is refused.
- [Escape Mode](escape.md) - the R2 control.
