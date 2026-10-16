---
title: "Keymap file: keymap.ini, the control config file, when it is read and written, its names in slot order, and the shipped defaults"
kind: "format"
category: "Controls and input"
summary: "The keyboard control file keymap.ini: where it lives, the one read at input start-up and the checks that throw a file away, the line grammar the parser accepts, the 28 names that are the slots of each of three profiles, the control codes the values hold, the two times the game writes the file, the Circle and Cross exchange, and the shipped default bindings of all three profiles."
addresses: ["00197EE0", "00195060", "00198000", "00196550", "001965E0", "00198B60", "001993B0", "01DF11E0"]
---

# Keymap file: keymap.ini, the control config file, when it is read and written, its names in slot order, and the shipped defaults

## What the player sees

- The keyboard controls are kept in `keymap.ini` and changed on the Config screen; the file can also be edited by
  hand.
- A file with a mistake in it is ignored as a whole, and the default controls are used instead.
- Changing the confirm button between Circle and Cross swaps those two bindings without changing the file.

## Where it comes from

`00197EE0` builds the path once into `01F80D90`: the Documents folder (`SHGetFolderPathW` with folder 5), then
`\My Games\`, `FINAL FANTASY XII THE ZODIAC AGE\`, the Steam account id from `001F3ED0`, and `keymap.ini`, creating
each folder that is missing. The reader and the writer both use that one path.

`InputManager_Initialize` (`00195060`, from `0019877E`) reads the file once, at start-up (`001950A9`-`001950EB`):

1. It clears the three profiles, `0x150` bytes at `01F80F90`.
2. It builds the path and reads the file into the profiles (`00198000`).
3. It checks that no code repeats and none is reserved (`00196550`), and that profile 1 is filled with legal codes
   (`001965E0`).
4. When both checks pass it publishes what was read (`00195DF0`); otherwise it installs the shipped defaults over it
   (`00198B60`).

The file is written by `001993B0`, from the Config screen (`001E0F40`, called at `0023D263`) and when the game shuts
down (`0017D670`, from `0017CDC0`). A first run with no file therefore ends by writing the defaults.

## Layouts

```struct KeymapProfile base=record size=0x70
+0x00  u32[16]  buttons   group 0: Select, L3, R3, Start, Up, Right, Down, Left, L2, R2, L1, R1, Triangle, Circle, Cross, Square
+0x40  u32[8]   sticks    group 1: RX_P, RX_N, RY_P, RY_N, LX_P, LX_N, LY_P, LY_N
+0x60  u32[4]   extras    group 2: Speed1, Speed2, Speed3, WalkMode
```

The three profiles sit at `01F80F90`, `0x70` bytes apart, and the file's `[Keyboard1]`-`[Keyboard3]` fill them in
order. A slot's name is its place in the three name groups at `01DF11E0`, sixteen pointers per group, read by both
the reader and the writer; the `.tsv` lists them in slot order.

### Reading

`00198000` opens the file with mode `0x23`, read and write without creating it, so a missing file reads as
nothing, and skips an empty one. Then,
line by line, at most 127 characters each:

1. An empty line is skipped.
2. A line whose characters 2-9 are `Keyboard` is a header: the number before `]` minus one becomes the profile. The
   first character can be anything, and a header without `]` ends the read.
3. A line with `=` is a binding: the name before it is compared case-insensitively with all 28 names, and a match
   stores the number after it in that slot of the current profile; a name that matches none changes nothing.
4. Any other line ends the read, keeping what was read before it.

A value with no digits, or one too large, stops the game with a standard library error.

The profile starts at -1, before any header, and is never checked against 0-2: a binding is stored at
`01F80F90 + 0x70 * profile + 4 * slot`. So a binding before the first header, or under `[Keyboard0]`, lands
`0x70` bytes below the profiles, in the end of the path buffer at `01F80D90`, and a large profile number lands past
them.

### The two checks

- `00196550` looks at all 84 slots of the three profiles: a non-zero code that appears twice, or a code in the list
  of 35 reserved codes at `01DF13E0`, fails the file.
- `001965E0` looks at profile 1 only: every one of its 28 codes must be 1-152, and profiles 2 and 3 may hold any code.

The reserved codes are 2, 81, 82, 84, 85, 88, 89, 90, 119, 122, 123, 125 and 130-152.

### Writing

`001993B0` opens the file with mode `0x26`, creating it anew, and writes, for each profile, `[KeyboardN]` and then every name as `Name=code`, 28
lines, in slot order, one per line with a bare line feed: 87 lines.

### Codes

A code is the value the input name registries give a key or a button ([Control names](control-names.md)): 11-26
are the pad buttons and 28 and up the keyboard keys, with 28-53 the letters A-Z. Codes 1-3, which no name has, are
the three mouse buttons: the filter `001967D0`, which keeps only the confirm binding's input when it runs, reads a
code of 1-3 as one of the mouse device's three button bytes and any other code as a key, code minus 28
(`0019686E`-`001968AC`). 0 is no binding.

### Circle and Cross

When the published profiles are built from the file or from the defaults, the Circle and Cross codes, slots 13 and
14, are exchanged when the confirm-button setting `+0x64` of the game settings is not 0: `001DFA70` answers whether it
is 0 (`001DFA70`-`001DFA77`), and the swap runs when it is not (`00195F03`-`00195F24`, `00198B60`). The file keeps them as written.

## Shipped data

`keymap-file.tsv` lists the 28 slots with the default code of each profile, as `00198B60` installs them: group 0
from `01DF09C0`, the stick pairs from the records at `01DF0A80`, and group 2 from `01DF1470` for profile 1 only.
Profile 1 binds every slot; profiles 2 and 3 bind only a few, and leave the rest 0.

Profile 1 is the familiar layout: W, A, S and D move, the arrow keys turn the camera, I, J, K and L are the
direction pad, Space confirms, C cancels, and F1-F3 set the game speed.

## Loader behaviour

`00198B60` copies each profile's defaults into the profiles at `01F80F90`, builds the published records at
`01DF1738` with L2 and R2 cleared (`01DF1758`), applies the Circle and Cross exchange, and copies the records to
`01F80130`.

## Modding notes

- Lines may be in any order inside a profile, and blank lines are allowed; a comment line ends the read.
- One repeated code anywhere, or one reserved code, makes the game ignore the whole file.
- Profile 1 must bind all 28 slots; profiles 2 and 3 may leave slots at 0.

## Related

- [Control names](control-names.md) - the names and codes of keys and buttons.
