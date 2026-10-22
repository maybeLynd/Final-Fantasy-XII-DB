---
title: "Keymap file: keymap.ini, the control config file, when it is read and written, its names in slot order, and the shipped defaults"
kind: "format"
category: "Controls and input"
addresses: "0x00197EE0, 0x00195060, 0x00198000, 0x00196550, 0x001965E0, 0x00198B60, 0x001993B0, 0x01DF11E0"
---

## What the player sees

- The keyboard controls are kept in `keymap.ini` and changed on the Config screen; the file can also be edited by
  hand.
- A file with a mistake in it is ignored as a whole, and the default controls are used instead.
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
4. Any other line ends the read, keeping what was read before it.

A value with no digits, or one too large, stops the game with a standard library error.

The reader and the writer go through a wide-character file buffer whose vtable is `0x008F38F0` (`0x001980B9`,
`0x00199453`); its put-back and seek methods `0x00197E10`, `0x001987A0` and `0x00198880` use the library's buffer helpers
`0x00195C10` and `0x00195BD0`. The reader copies text from each line into a wide string with `0x00196140`
(`0x001982FB`, `0x0019840F`), which grows the string's buffer with `0x00195820`.

The profile starts at -1, before any header, and is never checked against 0-2: a binding is stored at
`0x01F80F90 + 0x70 * profile + 4 * slot`. So a binding before the first header, or under `[Keyboard0]`, lands
`0x70` bytes below the profiles, in the end of the path buffer at `0x01F80D90`, and a large profile number lands past
them.

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

`keymap-file.tsv` lists the 28 slots with the default code of each profile, as `0x00198B60` installs them: group 0
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

## Modding notes

- Lines may be in any order inside a profile, and blank lines are allowed; a comment line ends the read.
- One repeated code anywhere, or one reserved code, makes the game ignore the whole file.
- Profile 1 must bind all 28 slots; profiles 2 and 3 may leave slots at 0.

## Related

- [Control names](control-names.md) - the names and codes of keys and buttons.
