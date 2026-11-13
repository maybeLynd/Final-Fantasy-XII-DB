---
title: "Control remapping: how the Config screen binds a key, the swap when a key is already in use, the keys that cannot be bound, the default profiles and how a change reaches the game"
kind: "system"
category: "Controls and input"
addresses: "0x01F80F90, 0x0023C5C0, 0x001E1050, 0x00198A00, 0x01DF13E0, 0x00195DF0, 0x00198B60, 0x00198960, 0x002414B0"
---

## What the player sees

- The Config screen lists every control. Most have one keyboard column; the directions, Circle, Cross, R3 and Select
  have three, one per keyboard profile.
- Choosing a control and pressing a key or mouse button binds it. A key already bound elsewhere asks whether to swap.
- Square clears a binding, except in the first profile.
- Some keys refuse to be bound, and the screen cannot be left while a first-profile control is unbound.
- A row restores every default.

Each binding is kept in one of three keyboard profiles laid out like `keymap.ini`. The game does not read the profiles
for input: after every change it copies them into the records it checks for key presses, and leaving the screen writes
them back to `keymap.ini`.

## How it works

### Where a binding lives

The bindings are the three profiles at `0x01F80F90`, `0x70` bytes apart: sixteen button codes in group 0, the eight
stick codes in group 1 at `+0x40` (`0x01F80FD0`) and Speed1-3 and WalkMode in group 2 at `+0x60` (`0x01F80FF0`), the
layout of [keymap.ini](keymap-file.md). The game does not poll these; it polls the records the publisher builds from
them ([Controls](controls.md)).

### The binding rows

The Config screen `0x0023CE10` builds 41 rows from the table at `0x0208E6E0`, which `0x002414B0` fills, 0x14 bytes each:
`{index, type, text, help, columns}`. A row of type 1 or 2 with columns is a binding row, `0x0023C5C0`, and
`0x001E0650` turns its index into a group and slot:

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

### What a binding row shows

`0x0023C5C0` installs `0x0023CAF0` as the cell writer of its row (`0x0023CA37`). For each column it shows:

- on row 0, which `0x002414B0` builds with type 1 and three columns, the heading Main key, Alternate key 1 or
  Alternate key 2, text `0x53F` plus the column (`0x0023CB0A`, `0x0023CC10`);
- on a binding row, the name of the column's code (`0x0023CB24`-`0x0023CB36`), or Press a Key (`0x46DD`) on the
  column being captured (`0x0023CB8C`-`0x0023CB99`);
- a cursor mark on the selected column, and otherwise one mark when the code still equals the one the row held
  when the screen opened (`+0xDC`, `0x0023CBB6`-`0x0023CBBD`) and another when it was changed.

`0x001E0B00(code)` turns a code into its text id, and `0x0023CAF0` is its only caller (`0x0023CB2F`). The names are
rows of `menu_command_template.bin`, one set of 104 key names per Windows keyboard layout:

| Code | Text id |
|---|---|
| `0` and below | `0x46DC`, Key Not Assigned |
| `1`-`27` | `0x46DD` plus the code: Left Mouse Button, Middle Mouse Button and Right Mouse Button for 1-3 |
| `28` and up | `0x46E1` plus the code minus 28; `0x4749` for the French layout `0x40C`, `0x47B1` for the German layout `0x407` (`GetKeyboardLayout`) |

### Binding a control

Inside a row (`0x0023C5C0`):

1. Left and right repeats move between the row's columns, wrapping (`0x0023C847`-`0x0023C897`); this is the only bound on
   the profile.
2. The confirm button starts capture and clears every key and mouse latch (`0x0023C80C`-`0x0023C823`, `0x001E0920`).
3. Each frame of capture, `0x001E0C50` returns the first held mouse button 1-3 or key 28-152 and clears it
   (`0x0023C729`). A pad button is never captured.
4. The row calls `0x001E1050(row, profile, code, swap 0)` (`0x0023C74A`).

`0x001E1050` maps the row, calls the assigner `0x00198A00` (`0x001E10AA`) and publishes on success (`0x001E10D0`). The map
`0x001E0650(row)` gives the group in bits `0xFF0000` and the slot in the low byte (`0x001E108B`, `0x001E109A`), and the
swap argument is passed as 1 for any non-zero value (`0x001E1084`-`0x001E1088`). The assigner's 1 comes back as 1, its
2 and 3 both as 2, and its 0 as 0 after `0x00195DF0(0x00198790())` (`0x001E10B4`-`0x001E10D5`). With no input manager,
`0x00198790()` null, it assigns nothing and returns 0 (`0x001E107A`-`0x001E107D`):

| Result | Meaning | What the row does |
|---:|---|---|
| 0 | bound | refreshes the screen (`0x00287C20`, `0x002B5C90`) |
| 1 | the key is in use | opens the swap question, dialog `0x2A` (`0x0023C7E9`) |
| 2 | a reserved key, or a bad group or slot | shows notice 2 (`0x0023C7B9`) |

`0x005841B0(parent, n)` shows the Controls screen's notices 1 to 4 as notices `0x1B`-`0x1E` of `0x00583FD0`, the notice
table at `0x00D23DA0` (text id, format, flags, sound per 8-byte entry), each with sound 5:

| `n` | Text (`menu_message.bin`) |
|---:|---|
| 1 | "That key is already being used" with "Override current setting" (`0x891`) |
| 2 | "That key cannot be used" (`0x892`) |
| 3 | "Key assignment not complete" (`0x893`) |
| 4 | "Keyboard ... controls cannot be left unassigned" (`0x899`) |

Leaving the screen with cancel shows notice `0x001E08F0()` when that is not 0 (`0x0023D25A`-`0x0023D297`); notice 2 follows
the assigner's refusal (`0x0023C7B9`), and notice 4 a row whose `+0xE8` is 0 (`0x0023C8CF`).

A yes to the question calls `0x001E1050` again with swap 1 (`0x0023C637`); a no changes nothing. Square clears the
binding with `0x001E1050(row, profile, 0, 1)` (`0x0023C8F5`), and in the first profile it plays error sound 4 instead
(`0x0023C8BF`-`0x0023C8CF`).

### The key-cap pictures

`0x002B5C90`, run when a binding is stored (result 0), repoints the button-prompt pictures at the new keys. For each
prompt it takes the first profile's key for the control (`0x001E0BD0`, `0x001E0DA0`), stores that key-cap index in the
picture's word `+0x0A`, and points its sprite `+0x20` at an entry of the atlas's group 0 (`0x002B5CC8`-`0x002B60BA`):

- for the 21 key-cap indices at `0x01E0C3F0` (`0x002878B0`), the entry follows the game's language: French 6, German 5,
  Italian 4, Spanish 3, Korean 0, the two Chinese languages 2 and 1, any other 9 (`0x00285F60` of `0x0017E270`);
- for any other key it follows the keyboard layout from `GetKeyboardLayout` (`0x001E0B90`): French `0x40C` gives 8,
  German `0x407` gives 7, any other layout 9 (`0x00285FE0`).

The index that test reads is the one the picture held before this call: the word `+0x0A` is read and passed to
`0x002878B0` first (`0x002B5D51`, `0x002B5D55`) and the new index is stored after the choice (`0x002B5D9A`), and so at
each of the six sites. For the prompts whose picture is fixed (`0x002B5EB2` onward) the entry therefore follows the
key shown until now; the pictures of the first two steps are chosen by the key itself (`0x002B5D3A`-`0x002B5D4D`).

It also keeps WalkMode's key-cap index (group 2 slot 3) at `0x01E0CE28` and those of the sixteen group 0 controls at
`0x01E0CE10`.

### The assignment

`0x00198A00(manager, profile, group, slot, code, swap)` is the only writer of one binding:

1. Groups 0, 1 and 2 take 16, 8 and 4 slots (`0x00198A49`-`0x00198AA5`); another group answers 3 and a bad slot 2
   (`0x00198A28`, `0x00198B4D`).
2. A reserved code answers 2 (`0x00198AB4`-`0x00198AD2`).
3. Code 0 is stored at once (`0x00198AD9`).
4. It looks for the code in all 84 slots of all three profiles except the target (`0x00198AF0`-`0x00198B04`), and stores
   it when it is nowhere else (`0x00198B06`).
5. When it is in use, swap 0 answers 1 (`0x00198B22`). Swap 1 gives the other slot the target's old code and then stores
   the new one (`0x00198B32`-`0x00198B3C`).

### Reserved keys

The 35 codes at `0x01DF13E0` are refused at assignment (`0x00198AC0`) and at load (`0x001965B4`):

| Codes | Controls |
|---|---|
| `2` | mouse button 2, the second of the three mouse codes |
| `81`, `82`, `84`, `85` | `Key_Minus`, `Key_Equals`, `Key_RightBracket`, `Key_Backslash` |
| `88`, `89`, `90` | `Key_Comma`, `Key_Period`, `Key_Slash` |
| `119`, `122`, `123` | `Key_Left_Alt`, `Key_Right_Alt`, `Key_AccentGrave` |
| `125`, `130`-`152` | keys with no registered name |

[Control names](control-names.md) and its table [`control-names.tsv`](control-names.tsv) name every code.

### Publishing

`0x00195DF0` runs after every binding, at start-up and after a restore. For each profile:

1. Group 0 goes to the record's buttons, with L2 and R2 stored as 0.
2. Group 1 becomes four stick entries of mode 2 at `+0x40`-`+0x7F`, each `2`, `4` and a pair of the codes
   (`0x00195E97`-`0x00195EFA`).
3. Circle and Cross are exchanged when `0x001DFA70` is false, that is when the Config setting `+0x64` is not 0;
   `0x001DFA70` reads the settings object `[0x01F82D20]` (`0x00195E42`, `0x00195F03`-`0x00195F24`).
4. The record is copied to the master copy `0x01F80130`.
5. The manager's rebuild flag `+0x3B` is set (`0x00195FE0`), so the next poll copies the master into the records.

It does not rewrite the record's entries 4-15, the pressure entries from `+0x80`. Group 2 never reaches a record:
those four controls are read from the profile itself.

### Circle and Cross

Changing the Config setting runs `0x0017E6E0` (`0x00240959`), which stores it, calls `0x00198960` and resets the confirm and
cancel masks (`0x0022A4F0`). `0x00198960` exchanges the Circle and Cross codes of records 2-4 and writes the exchanged pair
to `0x01F80130` (`0x00198960`-`0x001989C6`); it does not read the new value, so it always exchanges.

### Saving and restoring

1. Leaving the screen with the cancel button runs `0x001E08F0` (`0x0023D24F`-`0x0023D25A`), which checks the first profile
   with `0x001965E0`. A slot out of range keeps the screen open with an error sound.
2. Otherwise `0x001E0F40` writes keymap.ini through `0x001993B0` (`0x0023D263`). The file is also written at shutdown
   (`0x0017D68B`).
3. Row 40 asks dialog `0x29` (`0x0023D3AF`-`0x0023D3C0`). Yes runs `0x001E0F70` (`0x0023E185`), which installs the defaults with
   `0x00198B60` (`0x001E0F86`) and publishes them (`0x001E0F97`), and the confirm and cancel masks are reset.

### The defaults

`0x00198B60` copies the shipped defaults: group 0 from `0x01DF09C0`, the stick entries from `0x01DF0A80` and group 2 from
`0x01DF1470`. Only the first profile has stick keys (the arrow keys and W, A, S, D) and group 2 keys (F1, F2, F3 and Left
Shift); profile 2 binds the four directions, Circle, Cross, R3 and Select, and profile 3 the same without Up and Down. [keymap.ini](keymap-file.md) lists
every default.

## State

The Circle and Cross codes of the three keyboard records, the button codes of their master copies, and the Config
screen's row table (the open Controls screen `0x0208E6D0` is on [Config screen](../Menus-And-HUD/config-screen.md)):

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01DF176C`, `0x01DF1770` | `u32`, `u32` | 0 | Circle and Cross, buttons 13 and 14 (`+0x34`, `+0x38`) of record 2, the first keyboard profile ([Controls](controls.md)) | the static initialiser `0x0015C280` from the defaults at `0x01DF09F0` (`0x0015C365`); the publisher `0x00195DF0` (`0x00195E82`, and the exchange `0x00195F1C`, `0x00195F24`); the defaults `0x00198B60` (`0x00198C9D`, and the exchange `0x00198D1F`, `0x00198D27`); the rebuild `0x00196290` from the master copy (`0x001962DD`); the exchange `0x00198960` (`0x0019896C`, `0x00198972`) | `0x00195DF0` (`0x00195F0C`, `0x00195F14`); `0x00198B60` (`0x00198D0F`, `0x00198D17`); `0x00198960` (`0x00198960`, `0x00198966`); the input filter `0x001967D0`, which keeps only the cancel key of each record, the Cross slot's (`0x00196864`); the translator `0x00197160` through the record list `0x01DF1480` (`0x001971C5`) |
| `0x01DF18C8`, `0x01DF18CC` | `u32`, `u32` | 0 | the same two buttons of record 3, the second profile | `0x0015C280` (`0x0015C405`); `0x00195DF0`, `0x00198B60` and `0x00196290` (`0x0019637D`) as for record 2; `0x00198960` (`0x00198990`, `0x00198996`) | `0x00195DF0`, `0x00198B60`, `0x001967D0` and `0x00197160` as for record 2; `0x00198960` (`0x0019897E`, `0x0019898A`) |
| `0x01DF1A24`, `0x01DF1A28` | `u32`, `u32` | 0 | the same two buttons of record 4, the third profile | `0x0015C280` (`0x0015C4A2`); `0x00195DF0`, `0x00198B60` and `0x00196290` (`0x0019641D`) as for record 2; `0x00198960` (`0x001989B4`, `0x001989BA`) | `0x00195DF0`, `0x00198B60`, `0x001967D0` and `0x00197160` as for record 2; `0x00198960` (`0x001989A2`, `0x001989AE`) |
| `0x01F80140`, `0x01F80150`, `0x01F80160` | `u32[4]` each | 0 | buttons 4-7, 8-11 and 12-15 (`+0x10`, `+0x20`, `+0x30`) of the master copy of record 2, `0x01F80130`, first the defaults from `0x01DF09D0`-`0x01DF09FF`; buttons 13 and 14 have the row below | the static initialiser `0x0015BD30` (`0x0015BD62`, `0x0015BD70`, `0x0015BD77`); the copies of `0x00195DF0` (`0x00195F40`-`0x00195FCF`) and `0x00198B60` (`0x00198D40`-`0x00198D91`) | the rebuild `0x00196290` (`0x001962B7`-`0x001962F1`) |
| `0x01F80164`, `0x01F80168` | `u32`, `u32` | 0 | Circle and Cross in the master copy of record 2, `+0x34` and `+0x38` of `0x01F80130` | the static initialiser `0x0015BD30` (`0x0015BD77`); the copies of `0x00195DF0` (`0x00195F40`-`0x00195FCF`) and `0x00198B60` (`0x00198D40`-`0x00198D91`); `0x00198960` (`0x00198978`, `0x00198984`) | the rebuild `0x00196290` (`0x001962B7`-`0x001962F1`), which the poll runs through `0x00196680` |
| `0x01F8029C`, `0x01F802AC`, `0x01F802BC` | `u32[4]` each | 0 | buttons 4-7, 8-11 and 12-15 of the master copy of record 3, `0x01F8028C`, first the defaults from `0x01DF0A10`-`0x01DF0A3F` | `0x0015BD30` (`0x0015BE00`, `0x0015BE0E`, `0x0015BE15`); `0x00195DF0` and `0x00198B60` as above | `0x00196290` (`0x00196357`-`0x00196391`) |
| `0x01F802C0`, `0x01F802C4` | `u32`, `u32` | 0 | the same in the master copy of record 3, `0x01F8028C` | `0x0015BD30` (`0x0015BE15`); `0x00195DF0` and `0x00198B60` as above; `0x00198960` (`0x0019899C`, `0x001989A8`) | `0x00196290` (`0x00196357`-`0x00196391`) |
| `0x01F803F8`, `0x01F80408`, `0x01F80418` | `u32[4]` each | 0 | buttons 4-7, 8-11 and 12-15 of the master copy of record 4, `0x01F803E8`, first the defaults from `0x01DF0A50`-`0x01DF0A7F` | `0x0015BD30` (`0x0015BE9D`, `0x0015BEAB`, `0x0015BEB2`); `0x00195DF0` and `0x00198B60` as above | `0x00196290` (the third copy, from `0x001963DE`) |
| `0x01F8041C`, `0x01F80420` | `u32`, `u32` | 0 | the same in the master copy of record 4, `0x01F803E8` | `0x0015BD30` (`0x0015BEB2`); `0x00195DF0` and `0x00198B60` as above; `0x00198960` (`0x001989C0`, `0x001989C6`) | `0x00196290` (the third copy, from `0x001963DE`) |
| `0x0208E6E0`-`0x0208EA13` | `u32[205]` | 0 | the Config screen's 41 rows (see The binding rows), `0x14` bytes each: `+0x00` the row's own number, which no instruction reads; `+0x04` the type; `+0x08` the text id; `+0x0C` the help text id (`0xD43` on every binding row); `+0x10` the columns of a type 1 or 2 row, or the value a type 3 or 4 row passes to its handler (`0x0023DB40`, `0x0023E710`) | `0x002414B0`, which the screen `0x0023CE10` calls: see the list below | `0x0023CD20`, the type and text (`0x0023CD48`, `0x0023CD67`, `0x0023CD97`); `0x0023CE10`, the type (`0x0023CFA7`, `0x0023D020`, `0x0023D0CF`), `+0x10` (`0x0023D03D`, `0x0023D049`, `0x0023D062`) and the help of the selected row (`0x0023D350`); `0x00241890`, the type of the row under the cursor (`0x002418D0`) |

`0x002414B0` stores the row table in one pass, from 16-byte constants at `0x00914D10`-`0x00915030`:

- 16-byte stores to `0x0208E6E0`, `0x0208E6F0`, `0x0208E700`, `0x0208E710`, `0x0208E720`, `0x0208E730`, `0x0208E740`, `0x0208E760`,
  `0x0208E770`, `0x0208E780`, `0x0208E790`, `0x0208E7A0`, `0x0208E7C0`, `0x0208E7D0`, `0x0208E7E0`, `0x0208E7F0`, `0x0208E800`,
  `0x0208E810`, `0x0208E820`, `0x0208E830`, `0x0208E840`, `0x0208E850`, `0x0208E860`, `0x0208E870`, `0x0208E880`, `0x0208E890`;
- and to `0x0208E8A0`, `0x0208E8B0`, `0x0208E8C0`, `0x0208E8D0`, `0x0208E8E0`, `0x0208E8F0`, `0x0208E900`, `0x0208E910`, `0x0208E920`,
  `0x0208E930`, `0x0208E940`, `0x0208E950`, `0x0208E960`, `0x0208E980`, `0x0208E990`, `0x0208E9A0`, `0x0208E9B0`, `0x0208E9C0`,
  `0x0208E9D0`, `0x0208E9F0`, `0x0208EA00` (`0x002414C2`-`0x0024181A`);
- 4-byte stores: `0x0208E750` = `0xD43`, `0x0208E754` = 1, `0x0208E7B0` = `0x578`, `0x0208E7B4` = `0xD43`, `0x0208E7B8` = 1,
  `0x0208E7BC` = 11, `0x0208E970` = 1, `0x0208E97C` = `0x568`, `0x0208E9E0` = `0x565`, `0x0208E9E4` = `0xD3F`, `0x0208E9E8` =
  `0x26`, `0x0208E9EC` = 39, `0x0208EA10` = 0 (`0x002416C2`-`0x0024182C`);
- 8-byte stores: `0x0208E758` = 6 and `0x0208E974` = 33, the index of rows 6 and 33 with type 0 (`0x00241719`, `0x002416C8`).

No other instruction reaches these globals. `0x01DF176C` and `0x01DF1770` are also reached relative to the image base
(`0x00195F0C`, `0x00198D0F`), and so are `0x0208E6E4` and `0x0208E6EC` (`0x0023CFA7`, `0x0023D350`).

## Modding notes

- One code can be bound once across all three profiles.
- The swap can leave a first-profile control unbound when the target slot was empty; the screen then will not close
  until it is filled (`0x001E08F0`).
- The pressure entries 4-15 keep the shipped codes after any remap.
- `0x00198A00` and `0x00197710` take the profile as a byte and do not check it; the screen keeps it in range, a direct call
  does not.
- The assigner stores any code that is not reserved, including codes no band polls. The range check at saving covers
  the first profile only.
- L2, R2, the speed keys and WalkMode accept the left and right mouse buttons, which never fire for them.
- A pad code from 4 to 27 written into keymap.ini is shown under a key's name: `0x001E0B00` gives code n the text
  of code n + 24, so the pad's code 11 shows as H.

## Related

- [keymap.ini](keymap-file.md) - the file the profiles are read from and written to.
- [Controls](controls.md) - the records the game polls.
- [Control names](control-names.md) - the codes and their names.
