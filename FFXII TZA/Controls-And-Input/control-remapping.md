---
title: "Control remapping: how the Config screen binds a key, the swap when a key is already in use, the keys that cannot be bound, the default profiles and how a change reaches the game"
kind: "system"
category: "Controls and input"
summary: "How remapping works: where the three keyboard profiles live, the Config screen's binding rows and which profiles each row can edit, capturing a key, the assignment with its result codes, the yes-or-no swap when the key is in use, clearing a binding, the reserved keys, publishing a profile into the records the game reads, the Circle and Cross exchange, saving on leaving the screen, restoring the defaults, and the gaps a modder can hit."
addresses: "01F80F90, 0023C5C0, 001E1050, 00198A00, 01DF13E0, 00195DF0, 00198B60, 00198960, 002414B0"
---

## What the player sees

- The Config screen lists every control. Most have one keyboard column; the directions, Circle, Cross, R3 and Select
  have three, one per keyboard profile.
- Choosing a control and pressing a key or mouse button binds it. A key already bound elsewhere asks whether to swap.
- Square clears a binding, except in the first profile.
- Some keys refuse to be bound, and the screen cannot be left while a first-profile control is unbound.
- A row restores every default.

## How it works

### Where a binding lives

The bindings are the three profiles at `01F80F90`, `0x70` bytes apart: sixteen button codes in group 0, the eight
stick codes in group 1 at `+0x40` (`01F80FD0`) and Speed1-3 and WalkMode in group 2 at `+0x60` (`01F80FF0`), the
layout of [keymap.ini](keymap-file.md). The game does not poll these; it polls the records the publisher builds from
them ([Controls](controls.md)).

### The binding rows

The Config screen `0023CE10` builds 41 rows from the table at `0208E6E0`, which `002414B0` fills, 0x14 bytes each:
`{index, type, text, help, columns}`. A row of type 1 or 2 with columns is a binding row, `0023C5C0`, and
`001E0650` turns its index into a group and slot:

| Rows | Controls | Profiles |
|---|---|---|
| 2-5 | left stick: up, down, left, right | 1 |
| 7-10 | right stick: up, down, left, right | 1 |
| 12-15 | Up, Down, Left, Right | 3 |
| 17, 18 | Circle, Cross | 3 |
| 19-25 | Square, Triangle, L1, R1, L2, R2, L3 | 1 |
| 26 | R3 | 3 |
| 27 | Start | 1 |
| 28 | Select | 3 |
| 29-32 | Speed1, Speed2, Speed3, WalkMode | 1 |
| 40 | restore the defaults | - |

So every control has a row, and profiles 2 and 3 can be edited only for the eight with three columns, the ones the
shipped profiles 2 and 3 bind.

### Binding a control

Inside a row (`0023C5C0`):

1. Left and right repeats move between the row's columns, wrapping (`0023C847`-`0023C897`); this is the only bound on
   the profile.
2. The confirm button starts capture and clears every key and mouse latch (`0023C80C`-`0023C823`, `001E0920`).
3. Each frame of capture, `001E0C50` returns the first held mouse button 1-3 or key 28-152 and clears it
   (`0023C729`). A pad button is never captured.
4. The row calls `001E1050(row, profile, code, swap 0)` (`0023C74A`).

`001E1050` maps the row, calls the assigner `00198A00` (`001E10AA`) and publishes on success (`001E10D0`):

| Result | Meaning | What the row does |
|---:|---|---|
| 0 | bound | refreshes the screen (`00287C20`, `002B5C90`) |
| 1 | the key is in use | opens the swap question, dialog `0x2A` (`0023C7E9`) |
| 2 | a reserved key, or a bad group or slot | plays the error sound (`0023C7B9`) |

A yes to the question calls `001E1050` again with swap 1 (`0023C637`); a no changes nothing. Square clears the
binding with `001E1050(row, profile, 0, 1)` (`0023C8F5`), and in the first profile it plays error sound 4 instead
(`0023C8BF`-`0023C8CF`).

### The assignment

`00198A00(manager, profile, group, slot, code, swap)` is the only writer of one binding:

1. Groups 0, 1 and 2 take 16, 8 and 4 slots (`00198A49`-`00198AA5`); another group answers 3 and a bad slot 2
   (`00198A28`, `00198B4D`).
2. A reserved code answers 2 (`00198AB4`-`00198AD2`).
3. Code 0 is stored at once (`00198AD9`).
4. It looks for the code in all 84 slots of all three profiles except the target (`00198AF0`-`00198B04`), and stores
   it when it is nowhere else (`00198B06`).
5. When it is in use, swap 0 answers 1 (`00198B22`). Swap 1 gives the other slot the target's old code and then stores
   the new one (`00198B32`-`00198B3C`).

### Reserved keys

The 35 codes at `01DF13E0` are refused at assignment (`00198AC0`) and at load (`001965B4`):

| Codes | Controls |
|---|---|
| 2 | mouse button 2, the second of the three mouse codes |
| 81, 82, 84, 85 | `Key_Minus`, `Key_Equals`, `Key_RightBracket`, `Key_Backslash` |
| 88, 89, 90 | `Key_Comma`, `Key_Period`, `Key_Slash` |
| 119, 122, 123 | `Key_Left_Alt`, `Key_Right_Alt`, `Key_AccentGrave` |
| 125, 130-152 | keys with no registered name |

[Control names](control-names.md) and its table `control-names.tsv` name every code.

### Publishing

`00195DF0` runs after every binding, at start-up and after a restore. For each profile:

1. Group 0 goes to the record's buttons, with L2 and R2 stored as 0.
2. Group 1 becomes four stick entries of mode 2 at `+0x40`-`+0x7F`.
3. Circle and Cross are exchanged when `001DFA70` is false, that is when the Config setting `+0x64` is not 0.
4. The record is copied to the master copy `01F80130`.
5. The manager's rebuild flag `+0x3B` is set (`00195FE0`), so the next poll copies the master into the records.

It does not rewrite the record's entries 4-15, the pressure entries from `+0x80`. Group 2 never reaches a record:
those four controls are read from the profile itself.

### Circle and Cross

Changing the Config setting runs `0017E6E0` (`00240959`), which stores it, calls `00198960` and resets the confirm and
cancel masks (`0022A4F0`). `00198960` exchanges the Circle and Cross codes of records 2-4 and writes the exchanged pair
to `01F80130` (`00198960`-`001989C6`); it does not read the new value, so it always exchanges.

### Saving and restoring

1. Leaving the screen with the cancel button runs `001E08F0` (`0023D24F`-`0023D25A`), which checks the first profile
   with `001965E0`. A slot out of range keeps the screen open with an error sound.
2. Otherwise `001E0F40` writes keymap.ini through `001993B0` (`0023D263`). The file is also written at shutdown
   (`0017D68B`).
3. Row 40 asks dialog `0x29` (`0023D3AF`-`0023D3C0`). Yes runs `001E0F70` (`0023E185`), which installs the defaults with
   `00198B60` (`001E0F86`) and publishes them (`001E0F97`), and the confirm and cancel masks are reset.

### The defaults

`00198B60` copies the shipped defaults: group 0 from `01DF09C0`, the stick entries from `01DF0A80` and group 2 from
`01DF1470`. Only the first profile has stick keys (the arrow keys and W, A, S, D) and group 2 keys (F1, F2, F3 and Left
Shift); profiles 2 and 3 bind only the directions, Circle, Cross, R3 and Select. [keymap.ini](keymap-file.md) lists
every default.

## Modding notes

- One code can be bound once across all three profiles.
- The swap can leave a first-profile control unbound when the target slot was empty; the screen then will not close
  until it is filled (`001E08F0`).
- The pressure entries 4-15 keep the shipped codes after any remap.
- `00198A00` and `00197710` take the profile as a byte and do not check it; the screen keeps it in range, a direct call
  does not.
- The assigner stores any code that is not reserved, including codes no band polls. The range check at saving covers
  the first profile only.
- L2, R2, the speed keys and WalkMode accept the left and right mouse buttons, which never fire for them.

## Related

- [keymap.ini](keymap-file.md) - the file the profiles are read from and written to.
- [Controls](controls.md) - the records the game polls.
- [Control names](control-names.md) - the codes and their names.
