---
title: "Keymap file: keymap.ini, the control config file, when it is read and written, its names in slot order, and the shipped defaults"
kind: "format"
category: "Controls and input"
addresses: "0x00197EE0, 0x00195060, 0x00198000, 0x00196550, 0x001965E0, 0x00198B60, 0x001993B0, 0x01DF11E0"
---

## What the player sees

- The keyboard controls are kept in `keymap.ini` and changed on the Config screen; the file can also be edited by
  hand.
- What a mistake in the file does depends on the mistake:
  - a code used for two controls, a reserved code, or a control of the first set left empty or out of range: the
    whole file is ignored and the default controls are used;
  - a line that is neither a `[KeyboardN]` header nor a `name=value` binding: reading stops there and the lines
    before it are kept, unless the first set is then incomplete, which makes the game ignore the whole file;
  - a value or set number that is not a number, or is too large: the game stops;
  - a line of 128 characters or more: its first 127 are read as a line and the rest is lost. If that part is a
    binding with a value, or a header with `]` and a number, the game hangs while it starts, reading the file
    forever; otherwise it is treated like any other line of its kind;
  - a set number other than 1-3: its bindings are written outside the three sets, over other data;
  - a control name longer than 64 characters: the game stops.
- Changing the confirm button between Circle and Cross swaps those two bindings without changing the file.

## Where it comes from

`0x00197EE0` builds the path once into `0x01F80D90`: the Documents folder (`SHGetFolderPathW` with folder 5), then
`\My Games\`, `FINAL FANTASY XII THE ZODIAC AGE\`, the Steam account id from `0x001F3ED0`, and `keymap.ini`, creating
each folder that is missing: `0x001F3EA0` calls `_wmkdir` when `_waccess` fails, once per folder (`0x00197F22`-`0x00197F98`).
The reader and the writer both use that one path.

`InputManager_Initialize` (`0x00195060`, from `0x0019877E`) reads the file once, at start-up (`0x001950A9`-`0x001950EB`):

1. It clears the three profiles, `0x150` bytes at `0x01F80F90`.
2. It builds the path and reads the file into the profiles (`0x00198000`).
3. It checks that no code repeats and none is reserved (`0x00196550`), and that profile 1 is filled with legal codes
   (`0x001965E0`).
4. When both checks pass it publishes what was read (`0x00195DF0`); otherwise it installs the shipped defaults over it
   (`0x00198B60`).

The file is written by `0x001993B0`, from the Config screen (`0x001E0F40`, called at `0x0023D263`) and when the game shuts
down (`0x0017D670`, from `0x0017CDC0`). A first run with no file therefore ends by writing the defaults.

## Layouts

All multi-byte fields are little-endian.

The file itself is text; the table is one profile as the reader fills it, with offsets from the start of the
profile.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32[16]` | buttons | group 0: Select, L3, R3, Start, Up, Right, Down, Left, L2, R2, L1, R1, Triangle, Circle, Cross, Square |
| `+0x40` | `u32[8]` | sticks | group 1: RX_P, RX_N, RY_P, RY_N, LX_P, LX_N, LY_P, LY_N |
| `+0x60` | `u32[4]` | extras | group 2: Speed1, Speed2, Speed3, WalkMode |

The three profiles sit at `0x01F80F90`, `0x70` bytes apart, and the file's `[Keyboard1]`-`[Keyboard3]` fill them in
order. A slot's name is its place in the three name groups at `0x01DF11E0`, sixteen pointers per group, read by both
the reader and the writer; the `.tsv` lists them in slot order.

### Reading

`0x00198000` opens the file with mode `0x23`, read and write without creating it, so a missing file reads as
nothing, and skips an empty one. Then,
line by line, at most 127 characters each:

1. An empty line is skipped.
2. A line whose characters 2-9 are `Keyboard` is a header: the number before `]` minus one becomes the profile. The
   first character can be anything, and a header without `]` ends the read.
3. A line with `=` is a binding: the name before it is compared case-insensitively with all 28 names, and a match
   stores the number after it in that slot of the current profile; a name that matches none changes nothing.
4. Any other line ends the read, keeping what was read before it (`0x00198278`, `0x00198387`).

A value or profile number with no digits, or one too large for an `i32`, stops the game: `wcstol` (`0x00198328`,
`0x0019843C`) leads to `_Xinvalid_argument` or `_Xout_of_range` (`0x00198531`, `0x0019853F`, `0x0019857C`, `0x0019858A`), and
nothing on the way up catches the exception. This holds for a binding whose name matches nothing too, because the
value is parsed before the names are compared (`0x00198415`-`0x0019847C`).

Each line is read by `getline` into a 128-character buffer (`0x00198210`-`0x00198222`). `getline` tests every
character for the end of the file first, then for LF, then against the count, so a line of up to 127 characters,
ended by LF or by the end of the file, reads normally; a CR before the LF counts as one of the 127. A line of 128
or more characters stores its first 127, leaves the rest unread and sets the fail bit, and the 127-character part
is parsed as a line:

- a header without `]`, or a line that is neither a header nor a binding, ends the read there as usual
  (`0x00198278`, `0x00198387`);
- a header whose number has no digits, or a binding whose value has none, stops the game (`0x0019853F`,
  `0x0019858A`);
- a binding with a value, or a header with `]` and a number, lets the loop go on. Every later `getline` on the
  failed stream reads nothing and gives an empty line, which is skipped (`0x0019823D`), and the loop tests only the
  end-of-file bit (`0x00198515`-`0x00198523`), which a failed read never sets, so the read never ends.

The name before `=` is copied into a 64-character buffer with no length check (`0x0019838F`-`0x001983BF`). A name of 65
characters or more overwrites the function's stack guard at `+0x220` of its frame (`0x00198038`), and the guard check
stops the game when the read returns (`0x00198646`).

The reader and the writer go through a wide-character file buffer whose vtable is `0x008F38F0` (`0x001980B9`,
`0x00199453`); its put-back and seek methods `0x00197E10`, `0x001987A0` and `0x00198880` use the library's buffer helpers
`0x00195C10` and `0x00195BD0`. The reader copies text from each line into a wide string with `0x00196140`
(`0x001982FB`, `0x0019840F`), which grows the string's buffer with `0x00195820`.

The number in a `[KeyboardN]` header, minus one, is the profile, which starts at -1 before any header, and
nothing tests it (`0x0019834A`-`0x0019834C`). Each of the three name groups has its own base: group 0 (buttons)
`0x01F80F90` (`0x001984BF`), group 1 (sticks) `0x01F80FD0` (`0x001984AF`) and group 2 (extras) `0x01F80FF0` (`0x0019849F`).
A binding whose name is entry *i* of its group is stored at `base + 0x70 * profile + 4 * i` (`0x0019849B`-`0x001984E9`).
So:

- a binding before the first header, or under `[Keyboard0]` (profile -1), lands in the `0x70` bytes below the
  profiles, `0x01F80F20`-`0x01F80F8F`, the end of the path buffer at `0x01F80D90`;
- under `[Keyboard4]` (profile 3) it lands in the `0x70` bytes above them, `0x01F810E0`-`0x01F8114F`: buttons at
  `0x01F810E0`-`0x01F8111F`, sticks at `0x01F81120`-`0x01F8113F` and extras at `0x01F81140`-`0x01F8114F`. Each binding below
  overwrites half of an 8-byte word:
  - Select and L3: the word `0x01F810E0`, which the reader and the writer load (`0x001980DC`, `0x00199486`);
  - R3 and Start: the object pointer `0x01F810E8` that `0x00194F50` publishes (`0x00195028`);
  - Up and Right: the pause byte's pointer `0x01F810F0`;
  - Down and Left: the first AsyncJobManager `0x01F810F8`; L2 and R2: the second, at `0x01F81100`;
  - Triangle and Circle: the archive manager `0x01F81110`;
  - Speed1 and Speed2: the word `0x01F81140`, read by `0x0019B8C0`, `0x0019B990`, `0x0019C031` and `0x00202930`;
  - Speed3 and WalkMode: the object pointer `0x01F81148` that `0x0019B2F0` publishes (`0x0019B3C8`).

  An L1 binding overwrites the byte `0x01F81108`, which `0x0080C440` sets to 1 (`0x0080C4D0`);
- any larger or negative number reaches `0x70 * (N - 1)` bytes from the table in either direction.

Only profiles 1-3 are ever read back (`0x001965E0`, `0x00196550`, `0x00198B60`).

### The two checks

- `0x00196550` looks at all 84 slots of the three profiles: a non-zero code that appears twice, or a code in the list
  of 35 reserved codes at `0x01DF13E0`, fails the file.
- `0x001965E0` looks at profile 1 only: every one of its 28 codes must be 1-152, and profiles 2 and 3 may hold any code.

The reserved codes are 2, 81, 82, 84, 85, 88, 89, 90, 119, 122, 123, 125 and 130-152.

### Writing

`0x001993B0` opens the file with mode `0x26`, creating it anew, and writes, for each profile, `[KeyboardN]` and then every name as `Name=code`, 28
lines, in slot order, one per line with a bare line feed: 87 lines.

### Codes

A code is the value the input name registries give a key or a button ([Control names](control-names.md)): 11-26
are the pad buttons and 28 and up the keyboard keys, with 28-53 the letters A-Z. Codes 1-3, which no name has, are
the three mouse buttons: the filter `0x001967D0`, which keeps only the confirm binding's input when it runs, reads a
code of 1-3 as one of the mouse device's three button bytes and any other code as a key, code minus 28
(`0x0019686E`-`0x001968AC`). 0 is no binding.

### Circle and Cross

When the published profiles are built from the file or from the defaults, the Circle and Cross codes, slots 13 and
14, are exchanged when the confirm-button setting `+0x64` of the game settings is not 0: `0x001DFA70` answers whether it
is 0 (`0x001DFA70`-`0x001DFA77`), and the swap runs when it is not (`0x00195F03`-`0x00195F24`, `0x00198B60`). The file keeps them as written.

## Shipped data

[`keymap-file.tsv`](keymap-file.tsv) lists the 28 slots with the default code of each profile, as `0x00198B60` installs them: group 0
from `0x01DF09C0`, the stick pairs from the records at `0x01DF0A80`, and group 2 from `0x01DF1470` for profile 1 only.
Profile 1 binds every slot. Profile 2 binds Select, R3, the four directions, Circle and Cross (Numpad Plus,
Numpad 0, Numpad 8/6/2/4, Enter and Backspace); profile 3 binds Select, R3, Right, Left, Circle and Cross
(Z, X, E, Q, mouse button 1 and mouse button 3). Every other slot of profiles 2 and 3 is 0.

Profile 1 is the familiar layout: W, A, S and D move, the arrow keys turn the camera, I, J, K and L are the
direction pad, Space confirms, C cancels, and F1-F3 set the game speed.

## Loader behaviour

`0x00198B60` copies each profile's defaults into the profiles at `0x01F80F90`, builds the published records at
`0x01DF1738` with L2 and R2 cleared (`0x01DF1758`), applies the Circle and Cross exchange, and copies the records to
`0x01F80130`.

### From the file to the input records

The file is converted field by field: `0x00198000` parses each binding's text into a `u32` in its profile slot at
`0x01F80F90`. When both checks pass, `0x00195DF0` turns each profile *p* into a `0x15C`-byte record at
`0x01DF1738 + 0x15C * p` (`0x00195E30`-`0x00195FD5`):

1. It copies the 16 button codes, profile `+0x00`-`+0x3F`, to record `+0x00`-`+0x3F`.
2. It clears L2 and R2, record `+0x20` and `+0x24` (`0x00195E86`).
3. It writes the eight stick codes as four 16-byte entries at record `+0x40`, `+0x50`, `+0x60` and `+0x70`, each
   `2`, `4` and then the profile's pair: `+0x40`/`+0x44`, `+0x48`/`+0x4C`, `+0x50`/`+0x54`, `+0x58`/`+0x5C`
   (`0x00195E97`-`0x00195EFA`).
4. It exchanges Circle and Cross, record `+0x34` and `+0x38`, when `0x001DFA70` returns 0 (`0x00195F03`-`0x00195F24`).
5. It copies the whole record to `0x01F80130 + 0x15C * p` (`0x00195F2C`-`0x00195FCF`).

It reads each profile only up to `+0x5F`, so group 2 (`+0x60`-`+0x6F`) does not enter the records, and it writes
no record byte from `+0x80` on. It then sets byte `+0x3B` of the input manager it was passed (`0x00195FE0`).

## Modding notes

- Lines may be in any order inside a profile, and blank lines are allowed; a comment line ends the read.
- One repeated code anywhere, one reserved code, or one empty or out-of-range code in profile 1 makes the game
  ignore the whole file.
- Keep every line under 128 characters and every name under 65: longer ones hang or stop the game.
- Profile 1 must bind all 28 slots; profiles 2 and 3 may leave slots at 0.

## Related

- [Control names](control-names.md) - the names and codes of keys and buttons.
