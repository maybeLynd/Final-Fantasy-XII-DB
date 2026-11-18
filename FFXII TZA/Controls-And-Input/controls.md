[Home](../../README.md) / [Controls and input](README.md) / Controls

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Controls: how a key, button or stick becomes a game action, the control codes each device answers to, and how presses, holds and repeats are told apart | system | Controls and input | How input works | How input reaches the game: the input manager and its poll, the three bands of control codes and the device each reads, the records that turn codes into a 16-button mask and four stick bytes, the movement-key modes, the 16-frame channel history, how a press, a hold, a release and a menu repeat are made, the stick dead zone and the stick-to-direction bits, the button words the game reads each frame, the device-state count, the confirm and cancel buttons and the verbs that read them, the mouse wheel in menu lists, whether prompts show pad buttons or keys, the six controls read straight from the keymap, and what each button does in the field. | 0x01F7FFE0, 0x00196FF0, 0x00197160, 0x01DF1480, 0x0035F420, 0x0035FAC0, 0x0035FBD0, 0x002498B0, 0x02F97360 |

## What the player sees

- The keyboard, a pad and the mouse all drive the same sixteen buttons and two sticks.
- Holding a direction in a menu moves once, waits a moment, then repeats.
- Pressing Up and Down together, or Left and Right together, counts as neither.
- A small push of a stick does nothing; a larger push of the left stick also works as a direction button.
- Which of Circle and Cross confirms follows the Config setting.

Each device has a record that says which key or button stands for each of the sixteen buttons and two sticks. On every
poll the game checks all the records, merges them into one set of buttons and stick values, keeps the last 16 sets,
and compares them to tell presses, holds, releases and repeats apart.

## How it works

### The input manager

The manager is a `0x40`-byte object whose pointer is at `0x01F7FFE0`. `0x00198750` creates it, called only from
`0x0017D571`, and `0x00198790` returns it. Its start-up `0x00195060` clears the three keymap profiles (`0x001950A2`), reads
[keymap.ini](keymap-file.md), checks it and publishes it (`0x001950DA`) or installs the defaults (`0x001950EB`).

| Field offset | Meaning | Read at |
|---|---|---|
| `+0x08`, `+0x09` | invert the right stick's X and Y | X: `0x0019740F`, `0x0019751A`, `0x001975CB`; Y: `0x00197422`, `0x0019752E`, `0x001975DF` |
| `+0x0C`, `+0x10` | mouse wheel notches, total and this frame | `0x0019739A`, `0x001973A4` |
| `+0x39` | poll on or off | `0x0019701D` |
| `+0x3A` | movement-key mode bits `0x1`, `0x2` and `0x4` | `0x00197040`-`0x001970F8` |
| `+0x3B` | rebuild the records before the next poll | `0x00197032` |

### One poll

The device poll runs from the vsync callback `0x0035EC90`, installed at `0x0035E943`, through `0x0035FCA0` and `0x0035F420`.
`0x0035F420` reaches the manager's poll `0x00196FF0(manager, frame)` through `0x00862670` (`0x0035F467`), which jumps to
`0x001E09B0`, which tail-jumps to the poll at `0x001E09D3`. Its next call, `0x00862680` (`0x0035F473`), jumps to `0x001E09E0`,
which tail-jumps to the return stub `0x0016D6A0` (`0x001E0A03`) and so does nothing. The poll runs in this order:

1. With `+0x39` at 0 it returns at once (`0x0019701D`).
2. It updates every device (`0x007999E0`, `0x0019702D`), which lists them again after a pad arrives
   ([Controllers](controllers.md)).
3. With `+0x3B` set it copies the published profiles back into the records, rebuilds the movement-key blocks and
   clears the flag (`0x0019703B`-`0x00197073`): it calls `0x00196680`, then `0x00196C40` when mode bit `0x4` is set,
   `0x00196EE0` when bit `0x1` is set and `0x00196DF0` when bit `0x2` is set (`0x00197040`-`0x0019706E`).
4. It starts the 18-byte frame: a button mask of `0xFFFF`, four stick bytes of `0x80` and twelve zero bytes
   (`0x00197085`-`0x001970A9`).
5. It runs the translator `0x00197160` over the five records at `0x01DF1480` (`0x001970B0`), then over the three at
   `0x01F80550` when mode bit `0x2` is set, and the three at `0x01F80970` when bit `0x1` or `0x4` is set (`0x001970C8`-`0x001970FE`).
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
mouse buttons, or 3, the wheel (`0x001972C7`-`0x0019734F`). An entry whose second value is not 4 only calls
`GetForegroundWindow`, and drops its answer, while byte `+0xC35` of the object `0x001D50D0` returns is set
(`0x001973C8`-`0x001973E0`). So entry 4 is the wheel, and entries 0, 1 and 6 change nothing in the frame: entry 6's 3
is in its fourth value, which this arm does not read.

The two extra blocks turn movement keys into direction buttons. Mode bit `0x2` makes `0x00196DF0` build three records at
`0x01F80550` whose Up, Right, Down and Left are each profile's movement keys. Mode bits `0x1` and `0x4` build the same at
`0x01F80970` with L2 and R2 added (`0x00196EE0`, `0x00196C40`); bit `0x4` also clears the right-stick keys of records 2-4
(`0x00196D34`).

### Channel history

Each poll writes one 36-byte frame into a 16-frame ring at `+0x44` of the channel record `0x022CAE90` (`0x0035F420`):

1. The sixteen per-button bytes are the frame's stick and pressure bytes in the order of `0x01EF9238`. The frame is
   ring slot `byte 0 & 0xF` (`0x0035F487`-`0x0035F4A0`). The mask word it reads at `0x022CB642` has every bit set,
   because `0x00862660` stores `0xFFFFFFFF` at `0x022CB640` first (`0x0035F44A`-`0x0035F456`): frame word `+0x02` becomes
   `0xFFFF`.
   - So every byte is copied from the manager's frame `0x022CB680` (`0x0035F4D0`-`0x0035F4E8`), and the stores of `0x80`
     and 0 for a clear bit never run (`0x0035F4F0`-`0x0035F4F8`).
   - After the three steps, `0x0035F420` calls the return stub `0x0016D6A0` and the vibration step `0x0035F590`
     ([Vibration](vibration.md); `0x0035F537`, `0x0035F548`), and stores the device state in byte 0 of the frame last
     (`0x0035F572`).
2. `0x0035FAC0` makes the held mask from the frame's mask: a button is held when its bit is clear
   (`0x0035FB50`-`0x0035FB5A`). Up with Down (`0x50`) and Left with Right (`0xA0`) cancel each
   other (`0x0035FB6D`-`0x0035FB7E`). It writes held, pressed and released for set 0, the buttons, and held for set 1
   (`0x0035FB92`-`0x0035FBBD`).
   - Set 0's held word is frame `+0x04`, pressed `+0x0C` and released `+0x10`, against the held word of the frame
     before (`0x0035FB66`, `0x0035FB92`-`0x0035FBB4`); set 1's held word is `+0x06` (`0x0035FBBD`). With bit `0x2` of
     channel byte `+0x09` set it writes only set 1's word (`0x0035FB88`-`0x0035FB8D`); otherwise it also runs the
     repeats of set 0, `0x0035FBD0` (`0x0035FBB8`).
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

The eight group masks are the words at channel `+0x34`-`+0x43`, and each group's count is the signed byte at
channel `+0x24` + set + 2 × group (`0x0035FC09`-`0x0035FC18`); the two counts are channel bytes `+0x04` (12) and
`+0x05` (5). An unchanged group counts down and, at 0, fires its held bits and starts again from 5
(`0x0035FC2F`-`0x0035FC35`, `0x0035FC62`).

A changed group fires its new held bits at once, so a release fires nothing (`0x0035FC5D`-`0x0035FC62`). A group with
Left or Right (mask bits `0xA0`) that stays held through the change keeps counting, and the count that ends then
fires the group's bits of the poll before (`0x0035FC3C`-`0x0035FC57`). The repeat mask goes to word `+0x08` + 2 × set
of the newest frame (`0x0035FC87`).

### The button words

`0x002498B0` rebuilds the words at `0x02F97360` once per game frame, ORing the polls selected for that game frame: at
most `0x00184950()` of them, and none while `0x01FD4A84` is clear (Where a game frame reads the history, below). The
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

Each word is the OR of a history word over the polls selected for the game frame, the count `+0x08`
(`0x0035F130` at `0x00249928`, `0x00249940`-`0x0024999F`):
held `+0x06`, pressed `+0x0E`, repeat `+0x0A`, released `+0x12` for set 1, and `+0x04`, `+0x0C`, `+0x08`, `+0x10`
for set 0. `0x002498B0` clears the three records first (`0x002498BD`-`0x002498E0`), as does `0x002284F0` (`0x00228605`-`0x00228628`).
Set 1 is read by few functions; set 0 is the one menus and the field read:

| Word | Read by |
|---|---|
| held, set 1 | `0x00253C70` (`0x0025420A`, R2) and `0x00252B60` (`0x00252BD2`, R2) |
| pressed, set 1 | `0x00252B60` (`0x00252B7F`, R2), `0x002501A0` (`0x002501CA`, L3), `0x00250200` (`0x00250223`, L3), `0x002A9980` (`0x002A99EC`, the confirm mask) and the confirmation window `0x0057C480` (`0x0057C9DA`) |
| repeat, set 1 | `0x002498A0` (`0x002498A0`, R1) |
| released, set 1 | no function but `0x002498B0`, which copies it to the filtered words (`0x00249A5E`) |

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
  enters the next shown panel (`+0x40` bit `0x1`). `0x002C54B0(grid, dir)` answers whether a move would leave them.

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
other than -1 (`0x002B5B60`).

The only other instruction that reaches `0x01E0CE30` is in the inline-icon reader
`0x002AEB20` ([Text codes](../Menus-And-HUD/text-codes.md)), which reads one byte of it, relative to the image base, at the
icon letter minus `0x40` (`0x002AEBA4`-`0x002AEBAD`, `0x002AECA3`; a value from `0x20` first goes through `0x002AB8F0`).

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
while Game Over is armed, bit `0x2` of the mode word `0x022C83E8` (`0x0035C740`; [Game over](../World-Areas-And-Travel/game-over.md)), when the byte `0x0215F1A0` is set (`0x002E12D0`),
or when `0x00228380` or the Start handler `0x002287D0` answers non-zero (`0x00253C97`-`0x00253CCC`). The buttons are read
only while `0x00265680` answers non-zero (`0x00253D0D`), from held and pressed of set 0.

While `0x003135E0` (bit `0x1` of `+0x5B04` of `0x02EBF190`) and `0x0035C750` (bit `0x10` of the mode word `0x022C83E8`, not the battle mode register `0x022C83EC` of [Escape Mode](escape.md)) both answer non-zero, the
confirm button, the four directions and Square are dropped from the presses (`0x00253D3D`-`0x00253D5E`). The arms then
run in this order, and the availability bits are those of [Action availability](action-availability.md):

| Presses | Condition | What happens |
|---|---|---|
| Triangle alone, held and pressed | availability bit `0x1` clear | the main menu, request 2 (`0x00253D61`-`0x00253D78`) |
| Select or L3 | see [Menus](../Menus-And-HUD/menus.md) | the map requests; `0x002500F0(mask, 2)` answers 1 when availability bit `0x800` is clear, `0x00236760` answers 0 and `0x002E25B0(2)` allows request 2 (`0x00253E6D`) |
| any | `0x02092730` is 0 and `0x00303EC0` answers non-zero | `0x003CA200`, and the presses are cleared (`0x00253F62`-`0x00253F70`) |
| Square | `0x02092730` is 0, availability bit `0x400` clear, `0x003669D0` answers 0 | `0x002F1710`, then request 1 (`0x00253F7C`-`0x00253F98`, `0x002541B9`-`0x002541C7`) |
| cancel | `0x02092730` is 0 | `0x003C8950` (`0x00253F9D`-`0x00253FA9`) |
| Left or Right | L1 not held, `0x003669D0` answers 0, `0x02092730` is 0 or 3 | unless `0x02092734` is 1 or request 5 is refused, the target-cycling route `0x0035DA80`, `0x003C8990`, `0x003C87B0(5)` (`0x00253FB3`-`0x00254044`) |
| Up or Down, or wheel notches | L1 not held, two of the nine members `0x00320040(3, i)` returns have `+0x60` not negative and flag bit `0x2` clear or flag `0x4008` is set, `0x02092730` is 0 or 5 | request 3; with the area's bit `0x8000` the wheel total is cleared first (`0x00254052`-`0x002540D2`) |
| confirm or Square, or a pending pick | `0x02092730` is 0 | the interaction (`0x00254132`-`0x0025415A`), or request 1 (`0x002541A4`-`0x002541C7`) |

The helpers the arms call:

- `0x003C9570` returns the pick at `+0xCC` of the object in `0x02B47730` while its `+0xC0` bit `0x8` is set, and
  `0x003C9550` clears that bit; `0x003C8950` runs `0x00268620` and clears bit `0x2` when bit `0x2` is set.
- `0x003CA200` calls the callback at `+0x2A0` of the object in `0x02B47758` with message `0x1F` when that callback is set
  (`0x00273A20`) and the object's `+0x2E0` bit `0x10` is set.
- `0x002F1710` finishes the entry in `0x022BE7D0`: it copies the entry's second word over its first, calls its callback
  at `+0x08`, sets `+0x1C` to 1 and clears the entry's bit, numbered by `+0x18`, in `0x022BE7C0`.
- `0x002F1C50(n)` arms that entry: it takes one (`0x002F16B0`) into `0x022BE7D0` with the callback `0x002F18A0`, sets bit `0x2`
  of hold word 10 (`0x002E1C20(10, 1)`, the words at `0x0215F1C0`), and sets the count to 0 and the length to n x
  `[0x01DFE0B4]` (n alone while `0x001EDDA0()` answers). `0x002F18A0` clears that bit (`0x002E1CA0(10, 1)`) and `0x022BE7D0`.
- `0x00267720` answers 1 only when `0x0209A2AA` is set, the controlled character exists (`0x003590D0`, `0x003588B0`), its record is not one that `0x002373A0` accepts and
`0x00233D70` refuses, no
  menu is open (`0x002E05C0`), `0x00265680` answers non-zero and `0x02099DB4` is 0.
- `0x00273950()`, asked before the interaction (`0x0025412B`) and by `0x002C6F70` and `0x002736B0`, answers 0 while policy
  bit `0x2` is set without bit `0x200000` (the policy word `0x00254500`, the OR of the `0x01E0C2C0` masks of the set hold-mask bits);
  otherwise 1 when `0x02092730` is not 1, Escape Mode is not armed (`0x003669D0`) and hold-mask bit `0x10` is clear.
- `0x002736B0()`, from the HUD's `0x002C6F70` and `0x002C64C0`, answers 1 only when `0x00267720()` answers 1, hold-mask
  bit `0x10` is clear, `0x0028FA00()` and `0x00273950()` pass, and `0x0209A2C0` holds no handle or one whose class-1 or class-3
  actor has `+0x0C` bit `0x2` set (`0x0025B4C0`).
- `0x0028FA00()` needs the HUD part `+0x10F80` with word `+0x1D7A` bit `0x8` clear (`0x0028FA16`-`0x0028FA25`) and
  `+0x1D78` times the controlled character's byte `+0x14` in the part's list `+0x1D70` above `0x3FFF`, or
  `+0x1D78` above `0x7F` when the character is not listed.
- `0x00252DE0`, from the area unload `0x002628B0`, clears `0x02092730` and `0x02092734` and sets `0x020927C8` and `0x020927CC`
  to 1 (`0x00252DF5`-`0x00252E0B`).

The R2 toggle after the arms is on [Escape Mode](escape.md).

### The field target cycle

The field's target cursor is the object in `0x02B47730`: `+0xC4` the chosen target's handle, `+0xC8` the handle it
shows, `+0xCC` the pick and `+0xC0` its state bits. `0x003C9250(mode)`, called from `0x003C87B0` and `0x003C8B70`, chooses
from the field target cycle list at `0x022C83F0` (a count, then handles from `+8`; code `0x1A` of the list builder `0x0031EB20`, filled by the party rebuild of [Party list](../Menus-And-HUD/party-list.md)) for the controlled character `0x0035BAD0()`
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
  bit `0x8000` is set, `0x003C93E0(+8)` when its `+4` and `+8` differ (`0x003C94DD`), otherwise `+0xC8` = 0.
- `0x003C94F0()` does the same only while `+0xC0` bit `0x4` is set, and otherwise clears `+0xC8`; the menu steps
  `0x00276D30`, `0x002778C0`, `0x00279E20` and `0x0027B880` call it.
- `0x003C9370(h)` answers 1 when `h` is one of the handles of the field target cycle list `0x022C83F0` (`0x0035D3E0`) and 0
  otherwise; `0x003C87B0` (`0x003C8847`) and `0x003C8B70` (`0x003C8FB2`) call it.

## Layouts

### The target cursor's fields

The field's target cursor is the `0xD8`-byte widget kept at `0x02B47730` with procedure `0x003C8B70` (The field target
cycle above).

`FieldTargetCursor` (`0xD8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x003C8B70` |
| `+0xC0` | `u32` | stateBits | the cursor's state bits, bits `0x2` and `0x8` cleared on construction (`0x003C9222`). Bit `0x1`: set when the cursor gains the focus (message 8, `0x003C8F8F`); the next input turn only clears it (`0x003C8BCF`-`0x003C8BE1`). Bit `0x2`: tested and cleared by `0x003C8950` after `0x00268620` (`0x003C8960`, `0x003C8975`), cleared after a confirm (`0x003C8F6A`); no access sets it. Bit `0x4`: the target is shown: set while the pad's L2 is held (`0x003C917C`), cleared on each turn in pad mode (`0x003C9134`), toggled by a new keyboard L2 press (`0x003C91AA`-`0x003C91BB`), cleared when the target record shows nothing (`0x003C90D7`); `0x003C8B20`, `0x003C94F0` and `0x003C9590` test it. Bit `0x8`: a pick is waiting at `+0xCC` (`0x003C8E7B`); `0x003C9570` tests it and `0x003C9550` clears it |
| `+0xC4` | `u32` | chosenTarget | the handle of the chosen target, stored by `0x003C9420`; 0 on construction (`0x003C9211`) and when the cycle opens or a Left or Right press finds no target, by a qword store that also clears `+0xC8` (`0x003C8806`, `0x003C8CBA`, `0x003C8D8F`). `0x003C87B0` zeroes it before its table (`0x003C8806`) and then tests the 0 with `0x003C9370` (`0x003C8841`-`0x003C884F`); each tick the cursor closes with way 4 when it has left the list, has no actor or is no longer targetable (`0x003C8FAA`-`0x003C9051`); `0x003C8B50` returns it when the way `+0xD0` is 1 (`0x003C8B5C`-`0x003C8B65`) |
| `+0xC8` | `u32` | shownTarget | the handle of the target the cursor shows, stored by `0x003C93E0`, 0 when `0x00273710` refuses it or it is the controlled character (`0x003C90EA`-`0x003C9126`); 0 on construction and whenever the cursor closes (`0x003C89E8`, `0x003C8ACF`, `0x003C8C7E`, `0x003C8D53`, `0x003C8DFF`, `0x003C8F16`, `0x003C906C`). `0x003C8B20` returns it while bit `0x4` is set, `0x003C9590` answers whether it is set, and a confirm hands it to `0x0028F260` (`0x003C8F54`-`0x003C8F5E`) |
| `+0xCC` | `u32` | pick | the handle `0x0028F5B0` answers when the interaction button is pressed on an actor `0x00265460`, `0x002647D0` and `0x0025B4C0` accept (`0x003C8E44`-`0x003C8E82`); the cursor sets bit `0x8` and closes with way 1 (`0x003C8E76`). `0x003C9570` returns it while bit `0x8` is set (`0x003C9585`) |
| `+0xD0` | `u32` | closeWay | how the cursor last closed, 0 on construction (`0x003C9229`): 1 a target confirmed or a pick taken (`0x003C8EFD`, and `0x003C8A50` for 1 and 2), 3 cancelled (`0x003C8DE2`, `0x003C8990`), 4 the target was lost or Escape Mode armed (`0x003C9051`), 5 Left found no target, before or wrapping round (`0x003C8C61`), 6 Right found no target (`0x003C8D36`); `0x003C8A50`(n) stores the others as given (`0x003C8AB8`). `0x003C87B0` picks the next target from it (`0x003C880D`): the nearest for 0 and 4, the nearest as well for 1, 3 and 7 unless the list holds a handle 0, since `+0xC4` is 0 by then (`0x003C8841`-`0x003C8860`), no target for 2, for 5 the rightmost when Left is in the pressed word `0x02F9736A` and the leftmost when it is not, and for 6 the leftmost when Right is in it and the rightmost when it is not (`0x003C889D`-`0x003C88BB`) |
| `+0xD4` | `u8[4]` | tail0D4 | read and written by no function; nothing fixes its width |

## State

### Record button codes

The static initialiser `0x0015C280` fills the records' button codes in 16-byte stores; the globals below are the
stores that land on buttons 4-7 (`+0x10`), 8-11 (`+0x20`) and 12-15 (`+0x30`). All are 0 in the file. The translator
`0x00197160` reads every button code of the five records through the record list `0x01DF1480` that the poll passes it
(`0x00197089`, `0x001971C5`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01DF15EC`, `0x01DF15FC`, `0x01DF160C` | `u32[4]` each | 0 | buttons 4-7, 8-11 and 12-15 of record 1, the mouse: copies of `0x01F80100`, `0x01F80110` and `0x01F80120`, which are 0 in the file, so they stay 0 | `0x0015C280` (`0x0015C2B2`, `0x0015C2C0`, `0x0015C2C7`) | `0x00197160` |
| `0x01DF1748`, `0x01DF1768` | `u32[4]` each | 0 | buttons 4-7 and 12-15 of record 2, the first keyboard profile | `0x0015C280`, from the defaults `0x01DF09D0` and `0x01DF09F0` (`0x0015C350`, `0x0015C365`); the publisher `0x00195DF0` (`0x00195E64`, `0x00195E82`); the defaults `0x00198B60` (`0x00198C8D`, `0x00198C9D`); the rebuild `0x00196290` (`0x001962CD`, `0x001962DD`); Circle and Cross only: `0x00195DF0` (`0x00195F1C`, `0x00195F24`), `0x00198B60` (`0x00198D1F`, `0x00198D27`), `0x00198960` (`0x0019896C`, `0x00198972`) | `0x00197160`; the copies into the master `0x01F80130` (`0x00195F47`-`0x00195FCF`, `0x00198D47`-`0x00198D91`); Circle or Cross only: `0x001967D0` (`0x00196864`), `0x00195DF0` (`0x00195F0C`, `0x00195F14`), `0x00198B60` (`0x00198D0F`, `0x00198D17`), `0x00198960` (`0x00198960`, `0x00198966`) |
| `0x01DF18A4`, `0x01DF18B4`, `0x01DF18C4` | `u32[4]` each | 0 | buttons 4-7, 8-11 and 12-15 of record 3, the second profile | `0x0015C280` (`0x0015C3F0`, `0x0015C3FE`, `0x0015C405`); `0x00195DF0` (`0x00195E64`, `0x00195E78`, `0x00195E82`); `0x00198B60` (`0x00198C8D`, `0x00198C95`, `0x00198C9D`); `0x00196290` (`0x0019636D`, `0x00196375`, `0x0019637D`); Circle and Cross as for record 2, `0x00198960` at `0x00198990` and `0x00198996` | as for record 2; `0x00198960` at `0x0019897E` and `0x0019898A` |
| `0x01DF1A00`, `0x01DF1A10`, `0x01DF1A20` | `u32[4]` each | 0 | the same for record 4, the third profile | `0x0015C280` (`0x0015C48D`, `0x0015C49B`, `0x0015C4A2`); `0x00195DF0`, `0x00198B60` as for record 3; `0x00196290` (`0x0019640D`, `0x00196415`, `0x0019641D`); Circle and Cross as for record 2, `0x00198960` at `0x001989B4` and `0x001989BA` | as for record 2; `0x00198960` at `0x001989A2` and `0x001989AE` |

### The movement-key blocks

Each block is three records, one per keyboard profile, `0x15C` bytes apart: `0x01F80550`, `0x01F806AC` and `0x01F80808`,
and `0x01F80970`, `0x01F80ACC` and `0x01F80C28`. All are 0 in the file.

The static initialisers `0x0015C0D0` and `0x0015BF20`, which run from the C++ initialiser table (entries `0x008C3208` and
`0x008C3210`), fill each record's sixteen button codes with the 64-byte prototype `0x01DF0980`: button 0, Select, gets
code 53 (`Key_Z`), button 2, R3, gets code 51 (`Key_X`), and the others 0. They also copy `0x100` bytes from `0x01F7FFF0`
into each record's axis entries at `+0x40`.

The builders rewrite all sixteen codes of each record of their block, profile *p* for record *p*:

- `0x00196DF0` (mode bit `0x2`, block `0x01F80550`; `0x00196E32`-`0x00196E54`): Up, Right, Down and Left, buttons 4-7, get the
  profile's left-stick keys LY_N, LX_P, LY_P and LX_N, read at `0x01F80FEC`, `0x01F80FE0`, `0x01F80FE8` and `0x01F80FE4` +
  `0x70` × *p* ([keymap.ini](keymap-file.md)); every other button gets 0.
- `0x00196EE0` (mode bit `0x1`; `0x00196F2D`-`0x00196F59`) and `0x00196C40` (mode bit `0x4`; `0x00196C9B`-`0x00196CC1`), block
  `0x01F80970`: the same, and L2 and R2, buttons 8 and 9, get the profile's group 0 slots 8 and 9, at `0x01F80FB0` and
  `0x01F80FB4` + `0x70` × *p*.

The poll runs the builders on a pass with the manager's `+0x3B` set, before it translates (`0x00197040`-`0x00197073`).
The mode setters `0x00198670`, `0x00198690`, `0x001986B0`, `0x001986E0`, `0x00198710` and `0x00198730` store `+0x3A` and set
`+0x3B` to 1 together (`0x00198680`, `0x00198684` in the first), and `0x00198700` writes both bytes in one word store, 0
and 1 (`0x00198700`).

Two functions read the codes, one of them through a lookup:

- The translator `0x00197160` reads a record's sixteen codes (`0x001971B0`, while the index is below 16, an unsigned
  32-bit compare at `0x0019724A`). The poll passes it each record of `0x01F80550` while mode bit `0x2` is set
  (`0x001970C8`-`0x001970F6`) and each record of `0x01F80970` while bit `0x1` or `0x4` is (`0x001970F8`-`0x0019711B`).
- `0x00197870(manager, record, 0, button)` answers one code: from `0x01F80970` when mode bit `0x1` is set, else from
  `0x01F80550` when bit `0x2` is, else from `0x01F80970` when bit `0x4` is, else 0 (`0x00197870`-`0x00197902`). The button must be
  below 16, an unsigned 32-bit compare (`0x001978E5`, `0x0019790F`).
- `0x001E0DC0` reaches `0x00197870` (`0x001E0DF9`). Its two callers ask record 0 for buttons 7, 5, 4 and 6 (`0x002B5B60` at
  `0x002B5C3B`, the table `0x00916780`) and 4, 6, 7 and 5 (`0x00289830` at `0x00289889`, the table `0x00915DA0` of `0x002891A0`).
  Of the globals below, only `0x01F80560` and `0x01F80980` are read through it.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F80560`, `0x01F80570`, `0x01F80580` | `u32[4]` each | 0 | block `0x01F80550`, record 0, the first profile: buttons 4-7 (Up, Right, Down, Left), 8-11 and 12-15 | `0x0015C0D0`, the prototype's 0 (`0x0015C10D`, `0x0015C114`, `0x0015C11B`); `0x00196DF0`, the movement keys and 0 (`0x00196E4C`, `0x00196E50`, `0x00196E54`) | `0x00197160` (`0x001971B0`); buttons 4-7 also `0x00197870` (`0x001978FC`) |
| `0x01F806AC`, `0x01F806BC`, `0x01F806CC`, `0x01F806DC` | `u32[4]` each | 0 | record 1, the second profile: buttons 0-3, 4-7, 8-11 and 12-15 | `0x0015C0D0`, the prototype, 53 and 51 in buttons 0 and 2 (`0x0015C175`, `0x0015C186`, `0x0015C190`, `0x0015C197`); `0x00196DF0`, second pass (`0x00196E32`, `0x00196E4C`, `0x00196E50`, `0x00196E54`) | `0x00197160` (`0x001971B0`) |
| `0x01F80808`, `0x01F80818`, `0x01F80828`, `0x01F80838` | `u32[4]` each | 0 | record 2, the third profile: buttons 0-3, 4-7, 8-11 and 12-15 | `0x0015C0D0` (`0x0015C1F3`, `0x0015C201`, `0x0015C208`, `0x0015C20F`); `0x00196DF0`, third pass | `0x00197160` (`0x001971B0`) |
| `0x01F80980`, `0x01F80990`, `0x01F809A0` | `u32[4]` each | 0 | block `0x01F80970`, record 0, the first profile: buttons 4-7 (Up, Right, Down, Left), 8-11 (L2, R2 and two zeros) and 12-15 | `0x0015BF20`, the prototype's 0 (`0x0015BF5D`, `0x0015BF64`, `0x0015BF6B`); `0x00196EE0` (`0x00196F43`, `0x00196F55`, `0x00196F59`) and `0x00196C40` (`0x00196CAE`, `0x00196CBD`, `0x00196CC1`) | `0x00197160` (`0x001971B0`); buttons 4-7 also `0x00197870` (`0x00197926`) |
| `0x01F80ACC`, `0x01F80ADC`, `0x01F80AEC`, `0x01F80AFC` | `u32[4]` each | 0 | record 1, the second profile: buttons 0-3, 4-7, 8-11 and 12-15 | `0x0015BF20`, the prototype, 53 and 51 in buttons 0 and 2 (`0x0015BFC5`, `0x0015BFD6`, `0x0015BFE0`, `0x0015BFE7`); `0x00196EE0` and `0x00196C40`, second pass | `0x00197160` (`0x001971B0`) |
| `0x01F80C28`, `0x01F80C38`, `0x01F80C48`, `0x01F80C58` | `u32[4]` each | 0 | record 2, the third profile: buttons 0-3, 4-7, 8-11 and 12-15 | `0x0015BF20` (`0x0015C043`, `0x0015C051`, `0x0015C058`, `0x0015C05F`); `0x00196EE0` and `0x00196C40`, third pass | `0x00197160` (`0x001971B0`) |

### The filtered button words

`0x002498B0` copies the button words `0x02F97360`-`0x02F9736F` to the filtered copy `0x02F97388`-`0x02F97397` and the stick
bytes to `0x02F97398` every game frame (`0x00249A5E`-`0x00249A71`). When `0x02F973A0` is not 0 it then applies the masks
below (`0x00249A7E`-`0x00249BF8`). The masks are set by `0x002D6640(mask, sticks)` for every set at once, by
`0x002D6620`, which masks every button and the sticks without setting `0x02F973A0`, by `0x002D66A0(buttons)`, the forced
presses that the gambit screen and the licence board use, and cleared by `0x00249840`. All are
0 in the file.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02F9738A` | `u16` | 0 | filtered pressed mask, set 1 | `0x002284F0`, 0 (`0x00228628`); `0x002498B0` (0 at `0x002498E0`; `0x00249A71`, `0x00249B80`) | `0x002498B0` (`0x00249AC7`) |
| `0x02F9738C` | `u16` | 0 | filtered repeat mask, set 1 | `0x002284F0` (`0x00228628`); `0x002498B0` (0 at `0x002498E0`; `0x00249A71`, `0x00249B9E`) | `0x002498B0` (`0x00249AD3`) |
| `0x02F9738E` | `u16` | 0 | filtered released mask, set 1 | `0x002284F0` (`0x00228628`); `0x002498B0` (0 at `0x002498E0`; `0x00249A71`, `0x00249AEA`) | `0x002498B0` (`0x00249AEA`) |
| `0x02F97396` | `u16` | 0 | filtered released mask, set 0 | `0x002284F0` (`0x0022862F`); `0x002498B0` (0 at `0x002498E7`; `0x00249A71`, `0x00249AF4`) | `0x002498B0` (`0x00249AF4`) |
| `0x02F97399` | `u8` | 0 | filtered left stick Y: the copy of `0x02F97371`, then, while `0x02F973A0` is set, the forced byte `0x02F973B5` when that is not 0, otherwise 0 when `0x02F973A2` is set | `0x002284F0`, 0 with the four stick bytes (`0x00228636`); `0x002498B0`: 0 (`0x002498EE`), the 4-byte copy (`0x00249A6B`), the masked value (`0x00249BAD`) | `0x002498B0` (`0x00249B2C`); the licence board's `0x0055C740`, which takes the left stick negated and over 32 (`0x0055CC00`); the widget step `0x002BC3E0`, which takes the left stick over 16 (`0x002BC6FA`) |
| `0x02F9739A` | `u8` | 0 | filtered right stick X: the copy of `0x02F97372`, masked the same way with the forced byte `0x02F973B6` | `0x002284F0`, 0 with the four stick bytes (`0x00228636`); `0x002498B0`: 0 (`0x002498EE`), the 4-byte copy (`0x00249A6B`), the masked value (`0x00249BC8`) | `0x002498B0` (`0x00249B24`); `0x0055C740`, which reads the right stick when the left one is at rest (`0x0055CC19`) |
| `0x02F973A2` | `u8` | 0 | 1: the filtered stick bytes become 0 | `0x002D6620`, 1 (`0x002D6620`); `0x002D6640`, whether `sticks` is not 0 (`0x002D6659`); `0x00249840`, 0 (`0x00249842`) | `0x002498B0` (`0x00249AFB`) |
| `0x02F973A4` | `u16` | 0 | buttons taken out of both held masks | `0x002D6620`, `0xFFFF` (`0x002D6627`); `0x002D6640`, `mask` (`0x002D6675`); `0x00249840`, 0 (`0x00249842`) | `0x002498B0` (`0x00249A7E`) |
| `0x02F973A6` | `u16` | 0 | buttons taken out of both pressed masks | `0x002D6620` (`0x002D6627`); `0x002D6640` (`0x002D666E`); `0x00249840` (`0x00249842`) | `0x002498B0` (`0x00249A9D`) |
| `0x02F973A8` | `u16` | 0 | buttons taken out of both repeat masks | `0x002D6620` (`0x002D6627`); `0x002D6640` (`0x002D6667`); `0x00249840` (`0x00249849`) | `0x002498B0` (`0x00249AA8`) |
| `0x02F973AA` | `u16` | 0 | buttons taken out of both released masks | `0x002D6620` (`0x002D6627`); `0x002D6640` (`0x002D6660`); `0x00249840` (`0x00249849`) | `0x002498B0` (`0x00249AB2`) |
| `0x02F973AC` | `u16` | 0 | buttons forced into both held masks while a mask is on; `0x002498B0` does not clear it, so it stays until `0x00249840` | `0x002D66A0`, `buttons` (`0x002D66A8`); `0x00249840`, 0 (`0x00249849`) | `0x002498B0` (`0x00249B59`, `0x00249B61`) |
| `0x02F973AE` | `u16` | 0 | buttons forced into both pressed masks for one game frame | `0x002D66A0`, `buttons` (`0x002D66B6`); `0x002498B0`, 0 after use (`0x00249BF8`); `0x00249840` (`0x00249849`) | `0x002498B0` (`0x00249B3A`, `0x00249B4A`) |
| `0x02F973B0` | `u16` | 0 | buttons forced into both repeat masks for one game frame | `0x002D66A0`, `buttons` (`0x002D66AF`); `0x002498B0`, 0 after use with `0x02F973AE` (`0x00249BF8`); `0x00249840`, 0 (`0x00249850`) | `0x002498B0` (`0x00249B42`, `0x00249B52`) |

`0x002D6680` loads 8 bytes from `0x02F973A1` and uses only the first: the byte `0x002D66C0` stores, which is the argument of the script verb `fsmenu_setrepeat`, with 0 read as 8 (`0x002D668E`).

### Channel 1's button words

`0x002498B0` builds channel 1's eight words at `0x02F97374`-`0x02F97383` the same way as channel 0's, from the base
`0x02F97386` it steps to (`0x00249A4A`): each poll's word is ORed in through `[rbx - 0x12]` to `[rbx - 4]`
(`0x00249949`-`0x002499A4`). No function reads them back except those ORs; the stick readers `0x00249860` and `0x00249880`
take a channel number, and their two callers ask for channel 0 (`0x001EC17B`, `0x001EC192`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02F97378` | `u16` | 0 | channel 1's repeat mask, set 1 | `0x002284F0`, 0 with `0x02F9737A`-`0x02F9737F` (`0x0022861A`); `0x002498B0`: 0 (`0x002498D2`), each poll's word ORed in (`0x00249963`) | `0x002498B0`, that OR (`0x00249963`) |
| `0x02F97380` | `u16` | 0 | channel 1's repeat mask, set 0 | `0x002284F0`, 0 with `0x02F97382`-`0x02F97387` (`0x00228621`); `0x002498B0`: 0 (`0x002498D9`), each poll's word ORed in (`0x00249997`) | `0x002498B0`, that OR (`0x00249997`) |

No other instruction reaches these two globals or `0x02F97399`, `0x02F9739A`, `0x02F973AC` and `0x02F973B0` above. The
addresses taken near them are those of `0x002498B0`, `0x00249860` and `0x00249880` above and `0x02F97350`, the 16-byte copy
`0x003600C0` fills (`0x00249BFF`).

### The field target cursor and L2

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01EFE378` | `i32` | 1 | 1 while the pad's L2 (held mask set 0, bit `0x100`, `0x003C9163`-`0x003C9168`) drives the target cursor's `+0xC0` bit `0x4`, which it sets while held (`0x003C917C`) and the next call clears (`0x003C9134`); 0 once the keyboard's L2 (`0x0017DDC0`) has taken over, which toggles the bit on each new press (`0x003C912C`-`0x003C91C1`) | `0x003C8B70`: 0 on the keyboard key (`0x003C9158`), 1 on the pad button (`0x003C9183`) | `0x003C8B70` (`0x003C912C`, `0x003C918E`) |
| `0x02B47738` | `u8` | 0 | whether the keyboard's L2 was held at the last call, so that only a new press toggles the bit | `0x003C8B70` (`0x003C91C1`) | `0x003C8B70` (`0x003C914A`) |

The toggle and the set are skipped while bit `0x40000` of `0x002E0FA0()` is set (`0x003C9171`-`0x003C917A`, `0x003C919A`-`0x003C91A3`).

### Channel set-up

`0x0035F260` sets up the two input channels. All of these are 0 in the file.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CB3B8` | `i32[2]` | 0 | the device each channel reads: -1 for both, and nothing stores another value; `0x0035FCA0` passes it to `0x0053DD10`, which answers 1 whatever it is | `0x0035F260` (`0x0035F27E`) | through the address: `0x0035F420` (`0x0035F441`, `0x0035F451`), `0x0035FCA0` (`0x0035FCC3`, `0x0035FCE3`), `0x0035FDD0` (`0x0035FDF7`, `0x0035FDFE`) |
| `0x022CB6C0`, `0x022CB6C8` | `u8[8]` each | 0 | a 16-byte block that stays 0: `0x0035F420` hands its address to `0x00862680`, which reaches the return stub `0x0016D6A0` through `0x001E09E0` and writes nothing (`0x0035F46C`), and `0x003600C0` copies it to `0x02F97350` each game frame (`0x00249C06`) | `0x0035F260`, 0 (`0x0035F403`, `0x0035F40A`) | `0x003600C0` (`0x003600C0`) |
| `0x022CB700` | `i32` | 0 | 2 | `0x0035F260` (`0x0035F28C`, `0x0035F2B9`) | no instruction |
| `0x022CB704` | `i32` | 0 | the channel `0x0035F260` is setting up, 1 when it returns | `0x0035F260` (`0x0035F28C`, `0x0035F2D3`) | no instruction |
| `0x022CB708` | `u8[8]` | 0 | 0 | `0x0035F260` (`0x0035F2A1`) | no instruction |
| `0x022CB710` | `u8[8]` | 0 | 0 | `0x0035F260` (`0x0035F293`, `0x0035F2C9`) | no instruction |
| `0x022CB718` | `u8[8]` | 0 | 0 | `0x0035F260` (`0x0035F2B2`) | no instruction |

No other instruction reaches these globals. `0x00195DF0` and `0x00198B60` reach records 2-4 relative to the image base,
at the sites listed.

### Where a game frame reads the history

Each poll advances byte `+0x00` of the channel record, the ring slot of the newest frame, `+0x00 = (+0x00 + 1) & 0xF`
(by 1 modulo 16: `inc al`, `and al, 0xf`; `0x0035FCE0`-`0x0035FCEE`, `0x0035FDEA`-`0x0035FDF5`). Once per game frame
`0x0035FF90` catches the read position `+0x01` up to it:

1. With `0x01FD4A84` set it stores the number of polls since the last game frame at `+0x08`: `+0x00` less `+0x01`,
   taken 16 lower first when `+0x01` is the larger (both bytes zero-extended, `0x00360030`).
2. When that count is above `0x00184950()`, the number of 1/60 s periods in a game frame (a signed 32-bit compare,
   `0x00360054`), the count becomes that number and `+0x01` moves on by it only; the remaining polls are taken by the
   next game frame (`0x00360052`-`0x00360062`).
3. With `0x01FD4A84` clear the count is 0 and `+0x01` keeps its value.

When `0x00408B00()` answers 1 it does this for both channels through `rdi` = `0x022CAE98` + channel × `0x294`
(`0x0035FFC0`-`0x00360007`); otherwise for channel 0 only, by the addresses.

The history readers take a channel and a step `k <= 0` and read slot `+0x01` + `k` modulo 16, `(+0x01 + k) & 0xF`
(`0x0035EE6F`-`0x0035EE94` in `0x0035EE50`). `0x002498B0` and `0x0036FDF0` walk `k` from 1 - `+0x08` to 0, so they OR exactly
the polls the game frame has caught up with (`0x0024992D`-`0x002499A4`, `0x0036FE55`-`0x0036FEB8`).

`0x0036FDF0` keeps a second copy of set 0's words for each channel. It ORs the polls' repeat, pressed and released
words (frame `+0x08`, `+0x0C`, `+0x10`) into the globals below, then passes each through the channel's button map,
sixteen signed bytes at record `+0x284` that `0x0035F260` sets to 0-15 (`0x0035F3C3`-`0x0035F3DB`): input bit i sets
result bit `map[i]`, and a negative entry drops the bit (`0x0035EDE0`). The mapped words go to `0x02AD9E08`,
`0x02AD9E0C` and
`0x02AD9E10` + 2 × channel (`0x0036FEEA`, `0x0036FF01`, `0x0036FF30`). The held word, frame `+0x04`, goes the same way
through `0x02AD9E20`.

By address, `0x0036FDF0` first zeroes both channels' ORed repeat, pressed and released words and their mapped
words `0x02AD9E08`, `0x02AD9E0C` and `0x02AD9E10` (`0x0036FE14`-`0x0036FE3D`), then runs channel `c`, 0 then 1 (back
branch `0x0036FF47`); a third channel would end in the range-check failure `0x00809728()` (`0x0036FE4B`-`0x0036FE4F`,
`0x0036FF68`).

Per channel it first stores 0 in the ORed held word `0x02AD9E20 + 2c` (`0x0036FE5A`), so that word
too starts each game frame at 0. It then ORs the polls' held word into it from `0x0035EF10(c, k)`, beside
`0x0035EF70(c, k)`, `0x0035EFD0(c, k)` and `0x0035F030(c, k)` for the other three (`0x0036FE63`-`0x0036FEB8`).

The four ORed words then pass through the map: `0x0035EDE0(c, held)` is stored at `0x02AD9E04 + 2c`
(`0x0036FEBA`-`0x0036FED3`), and `0x0035EDE0(c, repeat)`, `0x0035EDE0(c, pressed)` and `0x0035EDE0(c, released)` at the
three addresses named above (`0x0036FEDB`-`0x0036FF30`). The repeat word is then copied to `0x02AD9E14 + 2c`, the
pressed word to `0x02AD9E18 + 2c` and the released word to `0x02AD9E1C + 2c` (`0x0036FF0E`-`0x0036FF38`).

Eight functions return one of these words each, with no argument and no store:

| Function | Word it returns | What the word is |
|---|---|---|
| `0x0036FF70()` | `0x02AD9E04` | channel 0, held, after the button map |
| `0x0036FF80()` | `0x02AD9E18` | channel 0, the copy of the pressed word `0x02AD9E0C` |
| `0x0036FF90()` | `0x02AD9E06` | channel 1, held, after the button map |
| `0x0036FFA0()` | `0x02AD9E0A` | channel 1, repeat, after the button map |
| `0x0036FFB0()` | `0x02AD9E0E` | channel 1, pressed, after the button map |
| `0x0036FFC0()` | `0x02AD9E08` | channel 0, repeat, after the button map |
| `0x0036FFD0()` | `0x02AD9E0C` | channel 0, pressed, after the button map |
| `0x0036FFE0()` | `0x02AD9E10` | channel 0, released, after the button map |

`0x0046DB40` is a jump to `0x0036FF80`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CAE91` | `u8` | 0 | channel 0's read position, the ring slot of the newest poll the game frame has taken | `0x0035F260`: the record cleared (`memset`, `0x0035F2F2`), then 0 (`0x0035F30F`); `0x0035FF90` (`0x00360065`; `0x0035FFFA` in the two-channel loop) | `0x0035FF90` (`0x00360020`; `0x0035FFC7`); the history readers, through `0x022CAE90` + channel × `0x294`: `0x0035EE50` (`0x0035EE6F`), `0x0035EEB0` (`0x0035EED5`), `0x0035EF10` (`0x0035EF2F`), `0x0035EF70` (`0x0035EF8F`), `0x0035EFD0` (`0x0035EFEF`), `0x0035F030` (`0x0035F04F`), `0x0035F090` (`0x0035F0AF`), `0x0035F150` (`0x0035F16C`), `0x0035F1A0` (`0x0035F1BF`), `0x0035F200` (`0x0035F21F`) |
| `0x022CAE98` | `u8` | 0 | channel 0's poll count for the current game frame, at most `0x00184950()` | `0x0035F260`, the record cleared (`0x0035F2F2`); `0x0035FF90` (`0x00360040`, `0x0036005A`; `0x0035FFE1`, `0x0035FFF3` in the loop) | `0x0035FF90` (`0x0036004B`; `0x0035FFE8`); `0x0035F130(channel)` (`0x0035F141`), called by `0x002498B0` (`0x00249928`) and `0x0036FDF0` (`0x0036FE46`) |
| `0x02AD9E24` | `u16` | 0 | channel 0's repeat word of set 0, ORed over the game frame's polls before the button map | `0x0036FDF0`: 0 with channel 1's word in a 32-bit store (`0x0036FE14`), the ORs (`0x0036FE8A`); `0x0036FD90(channel)`, 0 (`0x0036FDA9`) | `0x0036FDF0` (`0x0036FEC9`), into `0x02AD9E08` |
| `0x02AD9E28` | `u16` | 0 | channel 0's pressed word of set 0, the same way | `0x0036FDF0`: 0 with channel 1's word (`0x0036FE1E`), the ORs (`0x0036FE9B`); `0x0036FD90`, 0 (`0x0036FDB1`) | `0x0036FDF0` (`0x0036FEE0`), into `0x02AD9E0C` |
| `0x02AD9E2C` | `u16` | 0 | channel 0's released word of set 0, the same way | `0x0036FDF0`: 0 with channel 1's word (`0x0036FE28`), the ORs (`0x0036FEAC`); `0x0036FD90`, 0 (`0x0036FDB9`) | `0x0036FDF0` (`0x0036FEF7`), into `0x02AD9E10` |

`0x0036FD90(channel)` clears the channel's three ORed words and its mapped words at `0x02AD9E08`-`0x02AD9E10`. It sign-extends
the channel and doubles it, `rax = channel + channel` (`0x0036FD94`-`0x0036FD97`), and the result must be below 4 as an
unsigned 64-bit compare (`cmp rax, 4`, `jae`), so only channels 0 and 1 pass; any other value ends in the
range-check failure `0x00809728()` (`0x0036FD9A`-`0x0036FD9E`, `0x0036FDDE`). The field tick `0x00314020` calls
`0x0036FD90(0)` when `0x00228480()` answers 0 (`0x003142B0`-`0x003142B6`).

It leaves the held words `0x02AD9E04` and `0x02AD9E06`, their sources at `0x02AD9E20` and the copies
`0x02AD9E14`-`0x02AD9E1E` as they are: its six stores are the three ORed words and the mapped words `0x02AD9E08`,
`0x02AD9E0C` and `0x02AD9E10` of the channel (`0x0036FDA9`-`0x0036FDD1`).

No other instruction reaches `0x02AD9E24`-`0x02AD9E2F`, and the two record bytes are reached only through the record
addresses at the sites listed.

### The Party Menu's wheel stop

`0x0027E810(notches)` is the stop of `0x002D0580` for the Party Menu's member list, the widget at `[0x0209AC30] + 0xF8`, whose
rows are the pointers at `+0xC0`, cursor `+0x117` (`i8`) and last row `+0x118` (`i8`); a row is shown when bit `0x1` of
its `+0x40` is set. The member list's input step `0x00284EC0` calls it once per notch and stops moving when it answers
1 (`0x00285140`-`0x0028515B`). A positive notch total moves up.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209AC28` | `u32` | 0 | 1 while the stop is armed. It is armed when the cursor is on the shown row after the first shown row and the wheel turns up (`0x0027E937`), or on the shown row before the last shown row and it turns down (`0x0027E9AE`). While it is armed, the cursor is on row 0 turning up or on the last shown row turning down, and the wheel is still turning (`0x001E0E30`), `0x0027E810` answers 1 (`0x0027E8A6`-`0x0027E8AB`); with the cursor anywhere else it disarms (`0x0027E8B2`) | `0x0027E810` (`0x0027E8B2`, `0x0027E937`, `0x0027E9AE`) | `0x0027E810` (`0x0027E82D`) |

No other instruction reaches `0x0209AC28`.

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Enemy AI and gambits** (explained on [gambit screen](../Menus-And-HUD/gambit-screen.md))

| Function | | Functions |
|---|---|---|
| `0x0031EB20` | calls | `0x00327A10` |

</details>
