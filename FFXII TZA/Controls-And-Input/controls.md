---
title: "Controls: how a key, button or stick becomes a game action, the control codes each device answers to, and how presses, holds and repeats are told apart"
kind: "system"
category: "Controls and input"
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

The manager is a `40`<sub>h</sub>-byte object whose pointer is at `01F7FFE0`. `00198750` creates it, called only from
`0017D571`, and `00198790` returns it. Its start-up `00195060` clears the three keymap profiles (`001950A2`), reads
[keymap.ini](keymap-file.md), checks it and publishes it (`001950DA`) or installs the defaults (`001950EB`).

| Field offset | Meaning | Read at |
|---|---|---|
| `08`<sub>h</sub>, `09`<sub>h</sub> | invert the right stick's X and Y | `0019740F`, `0019751A`, `001975CB` |
| `0C`<sub>h</sub>, `10`<sub>h</sub> | mouse wheel notches, total and this frame | `0019739A`, `001973A4` |
| `39`<sub>h</sub> | poll on or off | `0019701D` |
| `3A`<sub>h</sub> | movement-key mode bits 0, 1 and 2 | `00197040`-`001970F8` |
| `3B`<sub>h</sub> | rebuild the records before the next poll | `00197032` |

### One poll

The device poll runs from the vsync callback `0035EC90`, installed at `0035E943`, through `0035FCA0` and `0035F420`.
`0035F420` reaches the manager's poll `00196FF0(manager, frame)` through two thunks: `00862670` jumps to `001E09B0`,
which calls it at `001E09D3`, and `00862680` jumps to `001E09E0`, which calls it through a pointer. The poll runs in
this order:

1. With `+39`<sub>h</sub> at 0 it returns at once (`0019701D`).
2. It updates every device (`007999E0`, `0019702D`), which lists them again after a pad arrives
   ([Controllers](controllers.md)).
3. With `+3B`<sub>h</sub> set it copies the published profiles back into the records, rebuilds the movement-key blocks and
   clears the flag (`0019703B`-`00197073`).
4. It starts the 18-byte frame: a button mask of `FFFF`<sub>h</sub>, four stick bytes of `80`<sub>h</sub> and twelve zero bytes
   (`00197085`-`001970A9`).
5. It runs the translator `00197160` over the five records at `01DF1480` (`001970B0`), then over the three at
   `01F80550` when mode bit 1 is set, and the three at `01F80970` when bit 0 or 2 is set (`001970C8`-`001970FE`).
6. It copies the frame out (`0019711D`).

### Control codes

A record holds sixteen button codes and sixteen axis entries, `15C`<sub>h</sub> bytes apart. The translator tests each button
code against three bands (`001971C5`-`00197218`):

| Codes | Device | Read by |
|---|---|---|
| `1`-`3` | mouse buttons | `0079E6D0` |
| `11`-`27` | any of up to 18 pads | `0079E650` |
| `28`-`152` | the keyboard | `0079E6A0`, keyboard 0 |

A code in no band, such as 0, 4-10 or 153 and up, is never polled. While `001C1990()` reports state 1 and `00228480`
answers 0, the translator skips the band tests (`001971B2`-`001971C3`), and mode 3 leaves the sticks centred. A held code clears its button's bit (`0019723D`), so
the mask is active-low. [Control names](control-names.md) lists the codes by name.

### Axis entries

Each axis entry is `{mode, axis, codeA, codeB}`, dispatched on its mode (`001972A0`-`001972C1`):

| Mode | Effect on stick byte i |
|---:|---|
| `1` | `FF`<sub>h</sub> while codeA is held (`00197680`) |
| `2` | codeA and codeB push the byte down and up by `7F`<sub>h</sub> and `80`<sub>h</sub>; for entries 0 and 1 the right stick's invert flags swap them, and entries 2 and 3 always push up with codeA (`0019748E`) |
| `3` | the pad stick `axis`, scaled from -1..1 to 0..255, with axes 2 and 3 flipped and flipped again by the invert flags (`001973E5`) |
| `4` | mouse: buttons through the backend bytes `+170`<sub>h</sub>-`+172`<sub>h</sub>, and code 3 as the wheel, one notch per 120 (`001972C7`-`001973BC`) |

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

Each poll writes one 36-byte frame into a 16-frame ring at `+44`<sub>h</sub> of the channel record `022CAE90` (`0035F420`):

1. The sixteen per-button bytes are the frame's stick and pressure bytes in the order of `01EF9238`.
2. `0035FAC0` makes the held mask from the frame's mask. Up with Down (`50`<sub>h</sub>) and Left with Right (`A0`<sub>h</sub>) cancel each
   other (`0035FB6D`-`0035FB7E`). It writes held, pressed and released for set 0, the buttons, and held for set 1
   (`0035FB92`-`0035FBBD`).
3. `0035F760` snaps a stick inside a radius of `20`<sub>h</sub> to the centre (`0035F7BD`, `0035F83F`). A left stick past `68`<sub>h</sub>
   adds the Up, Right, Down or Left bit to set 1 (`0035F8AE`), which is the buttons plus the left stick as directions.

Byte 0 of a frame is the device state, the second argument of `0035F420` (`0035F572`). `0035FCA0` passes 1, the
answer of `0053DD10`, which always returns 1 (`0035FCF0`-`0035FD85`). `0035EEB0(channel, i, back)` reads per-button
byte i of a frame, the newest for `back` 0, and `0046DB10(i)` is `0035EEB0(0, i, 0)`.

### The device-state count

`00227D70`, called by the Start handler `002287D0` (`00228885`), reads the state byte of channel 0's newest frame
through `0035F150(0, 0, 0)`:

- state 1 sets the count `01E027F8` to 6 and answers 0; any other non-zero state sets it to 6 and answers 2;
- state 0 counts `01E027F8` down and answers 2 while it was above 0, and answers 1 once it is 0.

Every frame `0035F420` writes holds state 1, so once channel 0 has been polled the answer is 0.

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

`0022A4F0` sets the confirm mask `01E0C2A0` and the cancel mask `01E0C2A4` to Circle and Cross, `2000`<sub>h</sub> and `4000`<sub>h</sub>,
when the Config setting `+64`<sub>h</sub> is 0 (`0017E210`), and the other way round otherwise. It also stores the setting's
answer at `01FD4A64` (`0022A510`).

Among the readers of `01FD4A64`, `0022A540` answers whether it is 0, for the input filter `001967D0` (`00196803`), and
the script verbs `get_pad_ok` `518`<sub>h</sub> and `get_pad_cancel` `519`<sub>h</sub> return the confirm and cancel masks through
`002E12B0` and `002E1290` (handlers `0034AF20` and `0034B290`).

### The mouse wheel in menus

`002D3900(list)` runs a menu list's cursor with the wheel added to the buttons (`002D392B`-`002D39C5`):

1. It takes held, pressed and repeat of set 0 (`02F97368`, `02F9736A`, `02F9736C`).
2. Every second call (the count `0209E65C` against `01E0CF88`, 2) it reads and clears the wheel's notch total with
   `001E0A10` (manager `+0C`<sub>h</sub>, cleared by `001986D0`).
3. With notches, 3 or more (`01E0CF84`) count as one when the list's `+E8`<sub>h</sub> is below 13 (`002D397C`). A positive
   total adds Up (`10`<sub>h</sub>) to pressed and repeat, a negative one Down (`40`<sub>h</sub>).
4. It then moves the list once per notch with `002D3BA0`, stopping at the first or last row (`002D4F10`) or when
   `002D0580` holds the cursor.
5. Without notches it moves the list once with the plain buttons.

`002D0580` arms a stop (`0209E660`) when the cursor is one row past the row at `+F6`<sub>h</sub> while moving up, or one row
before the last while moving down. While the stop is armed, the cursor is on that end row and the wheel is still
turning (`001E0E30`), it answers 1; with the cursor anywhere else it disarms. `002D3A50` is the
same with the filtered copy `02F97390`-`02F97394`, for the gambit screen (`0056984D`, `0056B871`, and `00569CF5` in `005691E0`), and `002D09F0`
moves a list with the filtered copy and no wheel (`00560D48`).

The Config screen's lists (`0023F240`, `00240DE0`), the clan primer's (`00570CE0`) and `00284EC0`, `002A9980`,
`002C2F90` and `002C4220` repeat the same pacing with their own code. The debug menu code `001D1660` can change the
pacing through `002D4F70` (1-10) and `002D4F90` (1-5).

`002C2F90` and `002C4220` move grid cursors for `002C1A80`, the input step shared by the Party Menu's member list
(`00284EC0`), the Status and Equip screen (`002C2320`, `002C59D0`, `003FF360`, `003FDAD0`), the gambit editor
(`005691E0`) and `0055C740`:

- `002C2F90` moves one cursor `+AE8`<sub>h</sub> with `002C2DA0(grid, dir, wrap)`: cells `20`<sub>h</sub> apart from `+C8`<sub>h</sub>,
  bounded by `+AEC`<sub>h</sub> and `+AEE`<sub>h</sub>, columns from the list's `+EC`<sub>h</sub>, skipping empty cells. `002C3C80(grid, dir)`
  answers whether a move would leave the grid.
- `002C4220` moves a cursor `+7A0`<sub>h</sub>, 0 to 53, over four panels at `+C0`<sub>h</sub> with `002C3D70(grid, dir, wrap)`.
  Each panel's first and last cells come from the 12-byte rows of `00916D30`, and a move off a panel's edge
  enters the next shown panel (`+40`<sub>h</sub> bit 0). `002C54B0(grid, dir)` answers whether a move would leave them.

### Pad or keyboard prompts

The input manager's byte `+38`<sub>h</sub> records whether the pad was used last:

- `0079D010`, the device poll, compares every key, pad button and mouse button with its previous state, and on a
  change calls application slot 25 with 0 for a key, 1 for a pad button and 0 for a mouse button (`0079D087`,
  `0079D107`, `0079D181`). Slot 25 is `0017D1E0`, which stores the byte through `00198E70`.
- The translator sets it to 1 when a pad stick axis reads non-zero (`0019744B`), and F9 clears it (`0017DE60`).

`001E0C10` reads it (`00197780`). An icon in text asks `002AB8F0` for its button (`002AEBCE`). The answer is an index
in the order Circle, Triangle, L1, L2, R1, R2, L3, R3, Square, Cross, Left, Right, Up, Down:

| Icon code | Index |
|---|---|
| `20`<sub>h</sub>, `21`<sub>h</sub>, `23`<sub>h</sub> | the confirm mask's button, 0 or 9; 0 when the keyboard was used last |
| `27`<sub>h</sub> | the cancel mask's button, 0 or 9; 9 when the keyboard was used last |
| `22`<sub>h</sub>, `24`<sub>h</sub> | 8, Square |
| `25`<sub>h</sub>, `26`<sub>h</sub> | 1, Triangle |
| `28`<sub>h</sub>, `29`<sub>h</sub>, `2A`<sub>h</sub>, `2B`<sub>h</sub> | 2, 4, 3 and 5: L1, R1, L2 and R2 |

Any other code is returned unchanged. `002B5B60`, run by the script verb `5CD`<sub>h</sub> (handler `00341030`), fills the 14
bytes at `01E0CE30` in that order with the key-cap index of each button's first-profile key (`001E0BD0`,
`001E0DA0`), exchanging entries 0 and 9 when the Config setting `+64`<sub>h</sub> is not 0.

Entries 10-13 then take the
direction keys of the active movement-key block (`001E0DC0`, slots 7, 5, 4 and 6). With no block active that
call gives code 0, which the index search `00197790` never finds, since it covers indices 0-105 only; the entry
then keeps the first pass's key, the Left, Right, Up or Down binding, because both passes store only an index
other than -1 (`002B5B60`). A scan of rip-relative and image-base displacement
operands in the listed functions finds no other reference to `01E0CE30`.

### Controls read straight from the keymap

Six controls are not in the published records. Their readers ask `00197710(manager, 0, group, slot)` for the first
profile's code, read from `01F80F90` (`0019775A`-`0019776F`), and test it on the keyboard only:

| Control | Reader | Read by |
|---|---|---|
| L2, group 0 slot 8 | `0017DDC0` | the target cursor (`003C9141`) |
| R2, group 0 slot 9 | `0017DE10` | the input arbiter (`002541D4`), [Escape Mode](escape.md) |
| Speed1-3, group 2 slots 0-2 | `0017DEA0` | `0022AA59` |
| WalkMode, group 2 slot 3 | `0017DFC0` | the party's movement (`00359518`) |

### The field buttons

The input arbiter `00253C70` reads the field's presses once per field frame. It returns before reading a button
while Game Over is armed, bit 1 of the mode word `022C83E8` (`0035C740`; [Game over](../World-Areas-And-Travel/game-over.md)), when the byte `0215F1A0` is set (`002E12D0`),
or when `00228380` or the Start handler `002287D0` answers non-zero (`00253C97`-`00253CCC`). The buttons are read
only while `00265680` answers non-zero (`00253D0D`), from held and pressed of set 0.

While `003135E0` (bit 0 of `+5B04`<sub>h</sub> of `02EBF190`) and `0035C750` (bit 4 of the mode word `022C83E8`, not the battle mode register `022C83EC` of [Escape Mode](escape.md)) both answer non-zero, the
confirm button, the four directions and Square are dropped from the presses (`00253D3D`-`00253D5E`). The arms then
run in this order, and the policy bits are those of [Action availability](action-availability.md):

| Presses | Condition | What happens |
|---|---|---|
| Triangle alone, held and pressed | policy bit 0 clear | the main menu, request 2 (`00253D61`-`00253D78`) |
| Select or L3 | see [Menus](../Menus-And-HUD/menus.md) | the map requests; `002500F0(mask, 2)` answers 1 when policy bit 11 is clear, `00236760` answers 0 and `002E25B0(2)` allows request 2 (`00253E6D`) |
| any | `02092730` is 0 and `00303EC0` answers non-zero | `003CA200`, and the presses are cleared (`00253F62`-`00253F70`) |
| Square | `02092730` is 0, policy bit 10 clear, `003669D0` answers 0 | `002F1710`, then request 1 (`00253F7C`-`00253F98`, `002541B9`-`002541C7`) |
| cancel | `02092730` is 0 | `003C8950` (`00253F9D`-`00253FA9`) |
| Left or Right | L1 not held, `003669D0` answers 0, `02092730` is 0 or 3 | unless `02092734` is 1 or request 5 is refused, the target-cycling route `0035DA80`, `003C8990`, `003C87B0(5)` (`00253FB3`-`00254044`) |
| Up or Down, or wheel notches | L1 not held, two of the nine members `00320040(3, i)` returns have `+60`<sub>h</sub> not negative and flag bit 1 clear or flag `4008`<sub>h</sub> is set, `02092730` is 0 or 5 | request 3; with the area's bit 15 the wheel total is cleared first (`00254052`-`002540D2`) |
| confirm or Square, or a pending pick | `02092730` is 0 | the interaction (`00254132`-`0025415A`), or request 1 (`002541A4`-`002541C7`) |

The helpers the arms call:

- `003C9570` returns the pick at `+CC`<sub>h</sub> of the object in `02B47730` while its `+C0`<sub>h</sub> bit 3 is set, and
  `003C9550` clears that bit; `003C8950` runs `00268620` and clears bit 1 when bit 1 is set.
- `003CA200` calls the callback at `+2A0`<sub>h</sub> of the object in `02B47758` with message `1F`<sub>h</sub> when that callback is set
  (`00273A20`) and the object's `+2E0`<sub>h</sub> bit 4 is set.
- `002F1710` finishes the entry in `022BE7D0`: it copies the entry's second word over its first, calls its callback
  at `+08`<sub>h</sub>, sets `+1C`<sub>h</sub> to 1 and clears the entry's bit, numbered by `+18`<sub>h</sub>, in `022BE7C0`.
- `002F1C50(n)` arms that entry: it takes one (`002F16B0`) into `022BE7D0` with the callback `002F18A0`, sets bit 1
  of hold word 10 (`002E1C20(10, 1)`, the words at `0215F1C0`), and sets the count to 0 and the length to n x
  `[01DFE0B4]` (n alone while `001EDDA0()` answers). `002F18A0` clears that bit (`002E1CA0(10, 1)`) and `022BE7D0`.
- `00267720` answers 1 only when `0209A2AA` is set, the controlled character exists (`003590D0`, `003588B0`), its record is not one that `002373A0` accepts and
`00233D70` refuses, no
  menu is open (`002E05C0`), `00265680` answers non-zero and `02099DB4` is 0.
- `00273950()`, asked before the interaction (`0025412B`) and by `002C6F70` and `002736B0`, answers 0 while policy
  bit 1 is set without bit 21 (the policy word `00254500`, the OR of the `01E0C2C0` masks of the set hold-mask bits);
  otherwise 1 when `02092730` is not 1, Escape Mode is not armed (`003669D0`) and hold-mask bit 4 is clear.
- `002736B0()`, from the HUD's `002C6F70` and `002C64C0`, answers 1 only when `00267720()` answers 1, hold-mask
  bit 4 is clear, `0028FA00()` and `00273950()` pass, and `0209A2C0` holds no handle or one whose class-1 or class-3
  actor has `+0C`<sub>h</sub> bit 1 set (`0025B4C0`).
- `0028FA00()` needs the HUD part `+10F80`<sub>h</sub> with word `+1D7A`<sub>h</sub> bit 3 and `+1D78`<sub>h</sub> times the controlled character's
  byte `+14`<sub>h</sub> in the part's list `+1D70`<sub>h</sub> above `3FFF`<sub>h</sub>, or `+1D78`<sub>h</sub> above `7F`<sub>h</sub> when the character is not
  listed.
- `00252DE0`, from the area unload `002628B0`, clears `02092730` and `02092734` and sets `020927C8` and `020927CC`
  to 1 (`00252DF5`-`00252E0B`).

The R2 toggle after the arms is on [Escape Mode](escape.md).

### The field target cycle

The field's target cursor is the object in `02B47730`: `+C4`<sub>h</sub> the chosen target's handle, `+C8`<sub>h</sub> the handle it
shows, `+CC`<sub>h</sub> the pick and `+C0`<sub>h</sub> its state bits. `003C9250(mode)`, called from `003C87B0` and `003C8B70`, chooses
from the target list at `022C83F0` (a count, then handles from `+8`) for the controlled character `0035BAD0()`
(`022C806C`), and gives 0 without a cursor, a character or a list:

1. `0035DCC0` fills one 12-byte entry per handle (the handle, its screen x through `00249110`, its index) and
   returns the handle nearest the character (`sqrtf` of the summed squares); mode 0 returns that one.
2. `0035DEB0` sorts the entries by screen x; mode 3 returns the leftmost and mode 4 the rightmost.
3. Modes 1 and 2 find the current `+C4`<sub>h</sub> with `0035DC90(entries, n, handle)`, the index of the entry holding that
   handle or -1, and return the entry before or after it, or 0 at either end.

The cursor's setters:

- `003C9420(h)` (`003C88CB`, `003C8CC8`) stores `h` at `+C4`<sub>h</sub>, after `0028FE40(6, h)` and, for a new non-zero
  `h`, sound 1 (`00249C60(1)`); then it sets `+C8`<sub>h</sub> as `003C93E0` does.
- `003C93E0(h)` stores `h` at `+C8`<sub>h</sub>, or 0 when `00273710(h)` refuses it or it is the controlled character.
- `003C94A0()` (`003C90BB`) re-shows the target of the record `0035BAF0()` returns (`022C8078`): nothing when its
  bit 15 is set, `003C93E0(+8)` when its `+4` and `+8` differ (`003C94DD`), otherwise `+C8`<sub>h</sub> = 0.
- `003C94F0()` does the same only while `+C0`<sub>h</sub> bit 2 is set, and otherwise clears `+C8`<sub>h</sub>; the menu steps
  `00276D30`, `002778C0`, `00279E20` and `0027B880` call it.
- `003C9370(h)` answers 1 when `h` is one of the handles of the target list `022C83F0` (`0035D3E0`) and 0
  otherwise; `003C87B0` (`003C8847`) and `003C8B70` (`003C8FB2`) call it.

## Modding notes

- A pad code (11-27) written into keymap.ini is polled like a key, but the six controls above ignore it.
- Binding L2, R2, a speed key or WalkMode to a mouse button is accepted and never fires, because those readers test the
  keyboard band only.
- The repeat timing is two bytes per channel, written at `0035F312`: 12 polls before the first repeat, then 5.
- The right-stick invert flags are manager `+08`<sub>h</sub> and `+09`<sub>h</sub>.

## Related

- [keymap.ini](keymap-file.md) - the bindings and their slots.
- [Control names](control-names.md) - every control code by name.
- [Controllers](controllers.md) - how pads are found.
- [Action availability](action-availability.md) - when a press is refused.
- [Escape Mode](escape.md) - the R2 control.
