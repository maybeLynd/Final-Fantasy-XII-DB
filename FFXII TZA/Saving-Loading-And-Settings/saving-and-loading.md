---
title: "Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs"
kind: "system"
category: "Saving, loading and settings"
addresses: "00580EB0, 005819F0, 00581DA0, 00581B70, 00582040, 003BB920, 003BB9B0, 003BB2F0, 00866A00, 00862590, 00866AD0, 0057E4D0, 0057E310, 00582860, 00862130, 0057FE80, 0057F8C0, 0057EFE0, 00580CD0, 00580840, 003BA990, 008621E0, 003BA680, 003BB790, 001C1720, 02B407C0"
---

## What the player sees

Saving at a save crystal opens the slot list. Picking a slot asks for confirmation when the slot is
empty or already holds a save, shows "Saving" while the file is written, and reports completion or
failure. Loading from the title screen reads the slot's file, shows "Loading", and continues into
the saved area with the clock, the gil and the party as they were saved. The game also writes a
hidden autosave to slot 0 whenever an area changes. A save that was interrupted part-way through
is left on disk with its header zeroed, so the slot shows it as unusable rather than as an older
save.

The slot list shows each used slot's party, gil, Esper row and clan rank, and marks the others
"Unused file." or "Corrupt save data."; the load list puts the autosave next to the newest manual
save. The title screen asks whether any save file exists before it offers loading. A shipped list
names the area changes that do not autosave.

## How it works

### The files

Each slot is one file named `FFXII_` plus the slot number as three digits (`005837F0`, kind 1,
through `003935C0` and `sprintf("%s%03d")`) in the save directory
(see the [save file format page](save-file-format.md)). The same formatter names `icon.sys`
(kind 0) and `static.ico` (kinds 2-4), the two companion files the save transaction deletes; it
returns the name in the controller record at `+0x128` and null when no controller is open
(`02CA99B8` = 0).

### The save and load screen

`00580EB0(controller, state, popup)` moves the screen between fifteen states and opens a popup
(`00583990(popupId, controller)`, kept at `+0xD8`) where one is listed:

| State | What the code does | Popup id | Popup text (`menu_message.bin`, through `00583990`'s table at `00D23DA0`) |
|---|---|---|---|
| 0 | arms the card-presence poll (`0057EC60`) | none | |
| 1 | runs the device check (`0057EA40`), in save mode when byte `+0xEA` is 0 | none | |
| 2 | confirms a new save | `0x15` | "Create new save data for FINAL FANTASY XII THE ZODIAC AGE?" |
| 3 | confirms an overwrite | `0x13` | "Save data ... already exists. Overwrite it?" |
| 4 | opens the save transaction `005819F0` as a child widget (`00244F50`, `00580FFF`) with the slot `+0xEB` and the save counter `+0xE4` + 1; plays sound `0x42` once per controller (`00580FBC`) | `0x10` | "Saving... Please do not close ..." |
| 5 | reports the save complete | `0x16` | "Save complete." |
| 6, 7 | the two trial-mode warnings | `0x19`, `0x1A` | "If you resume from this file, all trial mode progress will be lost. Are you sure you wish to proceed?", "Your Trial Version save data will no longer be playable. Are you sure?" |
| 8 | queues kind 1 with the callback `00580840`, then kind 9: read the slot's file into the active image, `0x56690` bytes; gauge target 30 | `0x11` | "Loading..." |
| 9 | reports the load complete | `0x17` | "Load complete." |
| `0xA` | confirms a format | `0x12` | "Memory card (PS2) in MEMORY CARD ... is not formatted. Format it now?" |
| `0xB` | queues kind 1 and kind `0xC` (format); gauge target 500 | `0xF` | "Formatting memory card (PS2). Do not remove/insert ..." |
| `0xC` | holds 120 frames (`+0xE8` = `0x78`) | `0x18` | "Format of memory card (PS2) in MEMORY CARD ... successful." |
| `0xD`, `0xE` | the error states; the popup id is the caller's | caller's | |

The popup table's entries are `{u32 text id, u8 kind, u8 flags, u8 sound}`; `002F9860` resolves a
text id as group `id / 1000` (2 = `menu_message.bin`) and index `id % 1000`.

The three storage results reach the screen as message `0x1D`: class 3 is the card-presence poll
(`0057EBB0`, queue kind 3), class `0xD` the device check (`0057E950`, kinds 4 and 5) and class
`0xF` the save transaction's completion (`00581B70`).

`0057ED40` disarms the card-presence poll: when the queue's front packet has already started (queue
`+0xDC` bit 0) it sets `+0xDC` bit 1, which makes the dequeue `00582240` return before that packet's
callback; otherwise it empties the queue (`+0x398` = 0). It also clears bits 0 and 1 of the poll
widget `02CA99D8`. The slot screen calls it when a slot is picked (sub-command `0x8001`) and on
sub-commands `0x8100`-`0x8102`; `00580A80` and the load lifecycle `00582860` call it too.

### The slot list

The slot screen `0057FE80` builds its list on message 1 from two tables: the slot status table
`02B407C0` (200 entries of 8 bytes, see Layouts; `003BB3E0(slot)` returns an entry's address and
`003BB600(slot, entry)` replaces one) and the header cache at `+0x1C0`, the first `0xA0` bytes of each
slot's image at `slot * 0xA0`, filled by the slot scan below.

- Save mode (`+0xEA` = 0) lists slots 1-199. Load mode lists, from slot 0, only the slots whose status
  is 2 or 4.
- A slot whose bit is set in the controller's bit set `+0x568` (200 bits) is first forced to status
  `{4, 1}`; the load callback sets that bit (below).
- The next save counter `+0xE4`, also stored at `02CA99B4`, becomes the highest header `+0x50` among
  the listed status-2 slots, slot 0's cache row and the active image.

The starting cursor is passed to `002D46F0`:

- In save mode it is the slot whose counter equals the active image's `+0x50` when that is non-zero,
  otherwise the readable slot other than 0 with the highest counter.
- In load mode, when slot 0 is not "Unused file", the autosave row is moved down to just after the newest
  manual save, and the cursor goes to the autosave when its counter is the highest, otherwise to that
  manual save.

`0057F8C0` draws a row. For status 2 it fills the row from the slot's cached header (`0057FB00`). Any
other status shows a line through `0057FA30` (text through `002F9860`), and when the screen was opened
with its flag bit 0 (`+0xE0`) every row is drawn as status 5:

| Status | Text (`menu_message.bin`) |
|---|---|
| 3 | `0x874` "In use by another game." |
| 4 | `0x873` "Corrupt save data." |
| 5 | `0x872` "Unused file." |
| any other | empty |

Every row then gets its slot number (`00393160`), except slot 0's row in load mode, which hides the
six number parts listed at `01F2CD10` and shows its own part `+0xD0`.

`0057FB00(row, list, header)` fills a status-2 row from the cached header:

- the region text is the region name of the area `+0x4C` (`003778B0`) and the area text its name
  (`00377B60`); with flag `+0x57` bit 0 set the row also shows its parts `+0xB8` to `+0xC8`, draws a
  frame (`002DC290`) and names the area `+0x80` instead, or `+0x4C` when that is 0;
- in the demo (`00264150`) the region text of persistence groups 7, 22, 25 and 29 (`00264F90`) is
  replaced by the `menu_message.bin` text `0x7EC`, `0x7EB`, `0x7EE` or `0x7ED` (`002F9860`), and the
  play time then shows zeros;
- the play time is hours `+0x18`, minutes `+0x1A` and seconds `+0x1B`, the last two capped at 59,
  drawn as three, two and two digits (`00393160`); 1,000 hours or more show 999:59:59;
- flag `+0x57` bit 2 shows the part `+0xD8`.

Moving the cursor (sub-command `0x8000`) calls `0057EFE0(pane, header)` for a status-2 slot and hides
the pane for any other. `0057EFE0` fills the status pane, whose labels are ESPER (`0x875`), CLAN RANK
(`0x876`) and POINTS (`0x877`), from the cached header:

- the seven roster entries through `0057E6D0`: an entry whose character byte is `0xFF` is hidden, and
  the level is capped at 99;
- the gil `+0x08`, capped at 99,999,999;
- the Esper row, shown only when `+0x3C` (the summoned Esper's character row, see the format page) is
  not `0xFF`: `0035D330(2, +0x3C)` looks the row up in the character table `[02EBF130]` (`0031C5D0`)
  and `002B58B0` gives its name;
- the clan rank row, shown when `+0x44` is non-zero and the demo flag `0209A2A9` (`00264150`) is clear:
  the rank title `003153F0(+0x44)` for ranks 1-12 and the points `+0x40`, capped at 99,999,999.

### After a save or a load

The controller copies the active image's first `0xE240` bytes (`0x1C4` blocks of 128 bytes and 64
bytes) into a buffer it allocates at `+0x588` when it opens (`00583CB0`, called from `00582860`
message 1); `00583C00` copies them back.

`00580CD0`, the slot screen's handler for the class-`0xF` result, closes the popup at `+0xD8`
(`00244F00`), sets `+0xCC` of `02CA99E0` to 4 and calls `00581350(error != 0)`. On success it:

1. adds 1 to the counter `+0xE4` unless it is `0xFFFFFFFF`, and writes it to the active image's
   `+0x50` and to `02CA99B4`;
2. sets bit 2 of the controller's `+0xC4`;
3. copies the active image's first `0xA0` bytes to the slot's cache row and refreshes the pane
   (`0057EFE0`);
4. stores `{2, 0}` in the slot's status entry, recounts `+0xED` (status 5) and `+0xEE` (status 5,
   status 2 or the room flag set), and moves to state 5.

On an error it moves to state `0xD` with popup 5, "Save failed." (`0x818`).

`00580840` is the load and format callback; it does nothing once the screen has set `+0xE0` bit 4.
For the read (kind 9):

| Result | What it does | Next state, popup |
|---|---|---|
| 0 | `005813E0` | 9, "Load complete." |
| 8 | restores the image head (`00583C00`), stores `{4, 1}`, sets the slot's bit in `+0x568`, hides the pane | `0xE`, popup 10, "Unable to load. Save data is corrupted." (`0x86D`) |
| any other | restores the image head | `0xD`, popup 6, "Load failed." (`0x81C`) |

A failed load therefore puts back the header and the payload up to the first group bank; the rest of
the image keeps whatever the read copied into it. For the format (kind `0xC`), success moves to state
`0xC` and an error to `0xD` with popup 4, "Failed to format memory card (PS2)." (`0x814`).

### The save transaction

`005819F0` opens the transaction on message 1: it copies the request's slot, counter and flags into
the record (`+0xCD` slot, `+0xD0` counter, `+0xC8` = request `+0x18` bit 0, the short variant),
keeps the image's header dword `+0x50` at `+0xD4`, sets the gauge total to `0x1DA`, or `0x17C` for
the short variant (`005817D0`, target minus `0x19`), registers the completion callback `00581B70`
on the storage queue, and runs step 1 (`00581DA0`).

`00581DA0(record, state)` performs one step and adds its weight to the progress total `+0xDC`:

| State | What it queues | File | Weight |
|---|---|---|---|
| 1 | zeroes the image's first 8 bytes in memory and writes them (kind 7) | the slot file | `0x10`, short `0x50` |
| 2 | delete (kind `0xB`) | `icon.sys` | `0x10`, short `0x14` |
| 3 | delete | the slot file | `0x10` |
| 4 | delete | `static.ico` | `0x10` |
| 7 | builds the submission descriptor (`005832B0`), runs the header finaliser `00583D60` and keeps its return, the plain CRC (`00583F97`), at `+0xD8`, then writes the whole image (kind 8, `0x56690` bytes) | the slot file | `0x168`, short `0xE6` |
| 8 | puts `{checksum, 1}` in the image's first 8 bytes and writes them (kind 7) | the slot file | `0x32` |

The callback `00581B70(kind, error, record)` accepts only the kind the current state waits for
(7 for states 1 and 8, `0xB` for 2-4, 8 for 7) and steps on:

- 1 to 2; 2 to 3, or to 7 in the short variant (`00581BFD`-`00581C06`); 3 to 4 with the counter
  `+0xCE` cleared; 4 to 7; 7 to 8.
- States 5 and 6 share state 4's arm and are never entered: the counter is incremented and tested
  against zero first.
- On the last completion, or on any error, it posts message `0x1D` with class `0xF`, the device
  byte from the queue's `+0x39A` and the error code to the controller, and releases the record.
- On an error it also restores the image's `+0x50` from `+0xD4` and raises bit 2 in the gauge's
  flags.

So a full save runs states 1, 2, 3, 4, 7, 8 and a short save 1, 2, 7, 8: the short variant still
deletes `icon.sys`, and keeps the old slot file until step 7 overwrites it. Between step 1 and step
8 the file on disk carries a zeroed header; the second dword is 1 only on a finished save. The
finished file carries the plain CRC at `+0x00`; the finaliser's complement exists only in the image
between step 7 and step 8.

### The storage queue

`00582730(path, buffer, size)` queues kind 7, `005826D0(path)` kind `0xB`, and the transaction
itself kind 8, all through `00582540` on the queue object `02CA99C0`. `00582040` starts the front
packet:

| Kind | Handler | What the handler sets and runs |
|---|---|---|
| 1 | copies the packet's callback into the queue (`+0xC0`, `+0xC8`) | nothing |
| 2 | `003BB730`; the device byte to `+0x39A` | nothing |
| 3 | `003BB2C0` | command 5, busy flag clear, no driver |
| 4 | `003BB3B0` | command 4, busy flag clear, no driver |
| 5 | `003BB740` | copies the name to `02B4055C`, sets busy, runs `003BAC90` |
| 6 | `003BB6A0(index < 200, ptr, name)` | stores `ptr` at `02B407C0[index]`, command 8, runs `003BA720` |
| 7 | `003BB920(name, 0, buffer, size)` | command 2, runs the worker `003BAEB0`; refused for a zero size |
| 8 | `003BB9B0(name, descriptors, count)` | command 2 with up to 5 descriptors of `0x38` bytes, runs `003BAEB0` |
| 9 | `003BB440(name, 0, buffer, size)` | the read of `size` bytes |
| `0xA` | `003BB4C0` | copies a `0xB8`-byte record to `02B40FF0`, command 6, runs `003BA990` |
| `0xB` | `003BB2F0` | command 7, runs `003BA5F0` (its states 0, 1 and `0xC` reach `00862130`) |
| `0xC` | `003BB380` | the format command |

`003BB920` and `003BB9B0` refuse while the machine is busy (`02B40E10` = 1), copy the name to
`02B40EC8`, set command 2 at `02B40E1C` and start the worker `003BAEB0`. The delete command runs
`00862130`: `_wfopen_s(path, "rb")`, and when that succeeds `fclose` then `_wremove`.

### The worker's status poll

`003BB790` runs each frame from `0032E070` while the machine is busy. It reads the status of the last
file call, `02EAF8E0`, through `00862600(unused, a, b)`, which stores 0 at `a`, the status at `b` and
returns 1. A status from -19 to -11, from -79 to -70 or from -59 to -40 ends the command with result 4,
and -5 with result 7. Any other status goes to the command's handler:

| Command (`02B40E1C`) | Handler |
|---|---|
| 0 | `003BAC90` |
| 1 | `003BA7B0` |
| 2 | `003BAEB0` |
| 3, 4, 5 | none: the command ends with result 0 |
| 6 | `003BA990`, the slot scan |
| 7 | `003BA5F0` |
| 8 | `003BA720` |
| 9 | `003BA680`, the save-data check |

The result is kept at `02B40E18` (`003BB420` returns it) and the busy flag at `02B40E10` (`003BB430`).

### The slot scan

`0057F6B0` queues kind 1 with the callback `0057F630`, then kind `0xA` with the pattern `FFXII_*`, the
header cache and a row size of `0xA0`. `00393630(buffer, size)` writes the pattern with
`sprintf("%s*")` and returns an empty string when the buffer is under 64 bytes. Kind `0xA`
(`003BB4C0`) copies the pattern to `02B4055C`, the buffer and row size to `02B40EF0` and `02B40EF8`, and
starts command 6, `003BA990`, which steps on each call:

1. State 0 sets every status entry to `{1, 0}`, takes the free space `02B4054C` from `02B40E0C` and lists
   the files with `008621E0(device, pattern, 0, 200, 02B41140)`. With none it goes to state `0x10`,
   otherwise to `0x15`.
2. State `0x15` handles one listed file per call. `003BA320(name)` gives its slot; the file is opened
   for reading (`008624D0`), read for `0xA0` bytes into the cache at `slot * 0xA0` (`00862590`) and
   closed (`008620E0`).
3. A full read stores status 2. A short read stores 4, with the room flag 1 when the requirement from
   `003BA3E0` fits the free space (which it then reduces) and 0 otherwise.
4. State `0x10`, after the last file: every entry still at status 1 becomes `{5, 1}` when its
   requirement fits the free space, which it reduces, and `{3, 0}` when it does not. The machine is then
   idle.

The requirement for an empty slot alternates between 95 and 94 units:
`(02B40540 + 1) / 2 + 02B40544 + 1`, plus 1 for every other slot.

`003BA320(name)` counts the pattern's characters before the `*` (ignoring `/`), requires two decimal
digits at that position of the name, and returns `atoi` of up to three characters from there; anything
else returns -1.

`008621E0(device, pattern, unused, count, out)` does not read the directory; it probes names:

- With `count` = 1 it opens the save directory plus the pattern (`"%s%S"`), copies the name to
  `out + 0x20` and the file size to `out + 0x10`, and returns 1 when the file exists, else 0.
- Otherwise the prefix is the pattern without its `*`, and the function tries prefix plus `%03d` for 0
  to `count - 1`. Each file that opens adds a `0x40`-byte row to `out`: the size at `+0x10` and the name
  at `+0x20`. It returns the number of rows.
- Either way the return value is also stored as the status `02EAF8E0`.

### The space requirement

The figures come from the PS2 memory card. `00393600(kind)` gives a file size for the kinds of the name
formatter `005837F0`: 964 bytes for kind 0 (`icon.sys`), `0xE240` (57,920) for kind 1 (the slot file)
and `0x8398` (33,688) for kinds 2-4 (`static.ico`). `003936B0` passes the sizes of kinds 0-2 to
`003BB630`, which stores the count, 3, at `02B40540` and the total in 1 KB units, each size rounded up
(1 + 57 + 33 = 91), at `02B40544`, and returns the total in bytes. `003936B0` adds `0x2400` and returns
102,400.

- The storage queue keeps that value at `+0xD0` (`005823B0`).
- The popup opener `00583FD0` rounds it up to KB for the "at least ... KB" text of popups 1, 7 and 9
  (popup-table kinds 3 and 4), which therefore reads 100.

`003BA3E0(name, out, n)` ignores the name. It sets `out` to `(max(0, 02B40540 - 2 * ((n - 1) / 2)) + 1)
/ 2`, adds `02B40544` and subtracts the rounded-up KB of the first `n` rows of the table at
`02B405D0` (stride `0x40`), and clamps the result at 0; it always returns 1. The free space comes from
the device check (command 0, `003BAC90`): `00862490` writes `0x2000000` to `02B40E0C`, 2 to
`02B40E08` and 1 to `02B41130`, and sets the status to 0.

### The save-data check

The title-screen script asks whether any save exists with two verbs:

1. `fsttl_opendatacheck` (`00511F20`, a jump to `00394600`) creates the `0x108`-byte widget `00393EA0`
   unless a check is running (`01EFAC10` = 2).
2. The widget's message 1 sets `01EFAC10` to 2. On its first message 2 it calls `0036FD80(1)`, writes
   the pattern `FFXII_*` with `00393630`, selects device 0 (`003BB730`) and starts command 9 with
   `003BB320`.
3. `fsttl_getdatacheckstatus` (`00511F30`) returns `01EFAC10` through `00394440`: 2 while running, 1
   when a save file exists, 0 when none does.

`003BB320(pattern)` copies the pattern to `02B4055C`, sets command 9 at `02B40E1C`, the busy flag and
state 1. The handler `003BA680` lists the files (`008621E0(device, 02B4055C, 0, 200, 02B41140)`) and
moves to state `0xD`; on the next poll a positive count ends the command with result 0, anything else
with result 9.

When the machine is idle the widget reads the result: 0 sets `01EFAC10` to 1; otherwise it runs
command 9 once more and then sets `01EFAC10` to 1 or 0 from the second result. Either way it calls
`0036FD70` and closes itself.

### The file layer

The worker reads and writes through a byte vector (`01F44D40` begin, `01F44D48` end, `01F44D50`
capacity):

- Open (`008666B0`) loads the whole existing file into the vector, decoding the container when it
  is one; in write mode a missing file leaves the vector empty.
- Read (`00866A00(cursor, dest, count)`) copies byte by byte while the cursor is inside the vector
  and returns 1 only when every requested byte was copied. The wrapper `00862590(mode, ..., size)`
  returns `copied ? size : 0` for mode 0 and -4 otherwise, so a short read overwrites the front of
  the destination, advances the cursor by the bytes it took, and reports 0.
- Write (`00866AD0(cursor, src, count)`) overwrites inside the vector and appends past its end; no
  file is touched until close. Its wrapper `00862620(mode, src, size)` stores `ok ? size : 0` as the
  status for mode 0 and -4 otherwise.
- Seek (`008625D0(mode, offset, origin)`) calls `00866A80` for mode 0, which moves the cursor to
  `offset` from the start (origin 0), the cursor (1) or the end (2) only when the new position is inside
  the vector; the status is set to 0 either way.
- Close (`00866200`) writes the vector as a new container to a temporary file and copies it over the
  slot file (see the format page). Every written file is a replaced copy, never written in place;
  step 8's 8-byte write loads the file step 7 wrote, patches its first 8 bytes and rewrites it.

### The autosave on an area change

`0057E4D0`, the autosave widget, runs `0057E310` on construction (message 1) and again on
sub-commands `0x8100`-`0x8102`. `0057E310` copies the capture image to the write buffer, stores the
CRC, the 1 and the save counter in its header, names the file for slot 0 (`00584610` with slot 0,
`sprintf("%s%03d")`), hands the descriptor to `003BB9B0` and sets the busy flag `02CA99E8`.

On message 2, once the machine is idle (`003BB430()` = 0), the widget looks at the result
`003BB420()`:

- zero: the widget completes (`+0xC8` = 1, `02CA99E8` = 0, `0036FD80(0)`, `00245020`);
- non-zero with no popup open (`+0xC0` = 0): it opens popup 1 through `00583FD0(1, widget)`, text
  2065, "Insufficient disk space. In order to create a save game, at least ... KB of free space is
  required."

Nothing is shown while the write runs.

### Which area changes autosave

The zone-change stager `003145E0` captures the autosave only when `0020E500(field, story counter,
entrance)` returns non-zero (`00314774`; the story counter is `00265270()`). `0020E500` passes the
SaveloadManager (`01F81260`, `001C18E0`) to `001C1720(manager, field, story, entrance)`:

1. It returns 0 when the manager's dword `+0x0C` is not 0 (the constructor `001C0E20` clears it) or
   the field id is not positive.
2. When bit 12 of the battle-state block's flag dword is set (`00236760`), the story value is replaced
   by -2.
3. It walks the rows of the vector at `+0x50` (16 bytes each, see Layouts). A row matches when its
   field equals the field, its entrance is 0 or equal, and its story value is 0, equal, or its variable
   is non-zero with `002EF390(variable)` true (the active image byte `+0xC00 + variable` is 1).
4. A matching row returns 0, so no autosave; no match returns 1.

The rows come from `./GameData/disableAutosaveList/disableAutosaveList.txt` (`008F9AC8`):

- At start-up `001C1710` queues the file through `001C1810`, with `001C18F0` as the callback, which
  runs the parser `001C0F20` while the manager exists.
- The parser reads one token per line (`sscanf("%s")`), steps over it plus two bytes, splits it at
  commas into four columns and converts each with `strtol` (a missing column is 0).
- It appends the rows with `001858A0`, the vector's grow-and-insert, and frees the text.
- When the second column is empty the parser takes the rest of the line as that column, so it
  converts to 0 and the later columns are 0.

Two more entry points that fetch the manager, `0020E540` (from `002EF690`) and `0020E5C0` (from
`0027F5D0`), end in a jump to the empty stub `0016D6A0` and do nothing.

### What a load runs

The load lifecycle `00582860` creates the slot screen and its panes (message `0xC`, `0x8001`), and
on message `0x12` with flag bit 4 of `+0xC4` set runs the post-load sequence: `001831A0`,
`005843E0` and `00182D40` when the controller's byte `+0x598` is clear (that arm also sets
`0209AC10` to 1), `00394400` when `00394520` reports a pending mode, then `00584210`, which handles the mode-3 stash and reseeds the gameplay generator from the clock
(see the format page). Message `0x10` records the load mode: with `00394450()` = 3 it calls
`00238A30(1)`, else `00238A30(0)`, then `00285E60(-1)`.

On message 1 `00582790` loads the screen's two layouts into `+0x100` and `+0x108` and, unless byte
`+0xC1` is set, the two icon resources (kind 7, ids `0x2C` and `0x2D`) into `+0x110` and `+0x118`,
with `00393600(2)` at `+0x120`. `00582FC0`, on message `0x12`, releases them, and the buffers at
`+0x588` and `+0x590` are freed after it. `00581310(pane)`, run on sub-commands `0x8100`-`0x8102` and
on message `0xF` with value 4, closes the pane and calls `00291D40` and `002CA110`, then
`002CC9C0(002CC9B0())` when bit 3 of `+0xC4` is set.

## Layouts

`SlotStatusEntry` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | status | 1 no file yet, 2 header read in full, 3 no file and no room, 4 file shorter than the header or failed to load, 5 no file with room reserved (`003BA990`, `00580840`) |
| `04` | `i32` | room | 1 when the slot's space requirement was reserved (`003BA990`, `003BA720`) |

The table holds 200 entries at `02B407C0`; slot `n` is entry `n` (`003BB3E0`, `003BB600`).

`SaveListRow` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8[16]` | pad10 | not written by `008621E0` |
| `10` | `i32` | size | the file's length from ftell (`008621E0`) |
| `14` | `u8[12]` | pad14 | not written by `008621E0` |
| `20` | `char[32] name` | the file name, prefix plus three digits (008621E0) |  |

`DisableAutosaveRow` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | field | the destination field id (`001C1720`) |
| `04` | `i32` | story | 0 any story counter; otherwise the counter it must equal; -2 matches only while battle-state bit 12 is set |
| `08` | `i32` | entrance | 0 any entrance; otherwise the entrance it must equal |
| `0C` | `i32` | variable | 0 none; otherwise the row also matches while `002EF390`(variable) is true |

## Shipped data

Measured from `gamedata/disableautosavelist/disableautosavelist.txt` in the archive:

| Fact | Value |
|---|---|
| File size | 673 bytes, 73 lines, each ending in CR LF |
| Rows | 73, naming 72 distinct field ids (1124 appears twice) |
| Field only, always excluded | 21 rows: fields 12, 13, 50, 769, 854, 858, 860, 862, 864, 866, 867, 868, 869, 910, 912, 914, 918, 922, 924, 1113, 1147 |
| Field and entrance | 1 row: field 1140, entrance 9 |
| Field and story counter | 28 rows, story values 16 to 6750 (for example `48,301`) |
| Story -2 (battle-state bit 12) | 10 rows: fields 1155 to 1299 in steps of 16 |
| Story -1 with a variable | 13 rows, variables 15 to 56; two of them (field 1124) also name entrance 5 or 4 |
| Empty second column | 1 row, `1113,,5303`, which parses as field 1113 alone |

## Operations

| Function | Role |
|---|---|
| `00580EB0` | the save and load screen's state machine |
| `005819F0` | opens the save transaction; `00581DA0` runs a step; `00581B70` completes it |
| `005837F0` | slot, icon and static file names |
| `00582730`, `005826D0` | queue a write of `size` bytes, queue a delete |
| `00582040` | starts the queue's front packet |
| `003BB920`, `003BB9B0`, `003BB2F0` | the write, image-write and delete starters |
| `008666B0`, `00866A00`, `00866AD0`, `00866200` | open, read, write, close on the byte vector |
| `00862590` | the read wrapper that turns the boolean into a byte count |
| `00862130` | delete a file if it exists |
| `0057E4D0`, `0057E310` | the autosave widget and its writer |
| `00582860` | the load lifecycle |
| `0057FE80` | the slot screen: builds the slot list |
| `0057F8C0`, `0057FA30` | draw a slot row, the status line |
| `0057EFE0` | fill the status pane from a cached header |
| `00580CD0`, `00580840` | the save result, the load and format result |
| `00583CB0`, `00583C00` | back up, restore the image's first `0xE240` bytes |
| `0057ED40` | disarm the card-presence poll |
| `003BB3E0`, `003BB600` | read, replace a slot status entry |
| `003BB790`, `00862600` | the worker's per-frame status poll, the status getter |
| `0057F6B0`, `003BA990` | queue the slot scan, run it |
| `008621E0` | probe one file, or list `prefix000` to `prefix199` |
| `003BA320` | slot number from a file name |
| `003936B0`, `00393600`, `003BB630`, `003BA3E0` | the space requirement |
| `00393630` | the `FFXII_*` pattern |
| `00394600`, `00393EA0`, `003BB320`, `003BA680` | the save-data check |
| `008625D0`, `00862620` | the seek and write wrappers |
| `001C1720` | decide whether an area change autosaves |
| `001C0F20` | parse `disableAutosaveList.txt` |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `02CA99B8` | ptr | the open save/load controller | `00582860` |
| `02CA99C0` | ptr | the storage queue | the queue owner |
| `02CA99C8` | ptr | the gauge widget | the controller |
| `02CA99B0` | i32 | a save transaction is open | `005819F0` |
| `02CA99B4` | u32 | the save counter written at header `+0x50` | `0057E310` |
| `02CA99E8` | i32 | an autosave write is busy | `0057E310`, `0057E4D0` |
| `02B40E10` | i32 | the storage machine is busy | `003BB920`, `003BB9B0`, `003BB2F0` |
| `02B40E1C` | i32 | the worker command | the three starters |
| `01F44D40` / `01F44D48` / `01F44D50` | ptr | the file vector's begin, end and capacity | `008666B0`, `00866AD0`, `00866200` |
| `02B407C0` | 200 x 8 bytes | the slot status table | `003BA990`, `003BA720`, `003BB600`, `003BB6A0` |
| `02B40E18` | i32 | the last command's result | the command handlers |
| `02EAF8E0` | i32 | the status of the last file call | `008621E0`, `00862590`, `00862620`, `008625D0`, `00862490` |
| `02B4054C` | i32 | the free space the slot scan draws on | `003BA990`, `003BA720` |
| `01EFAC10` | u8 | the save-data check: 2 running, 1 a save exists, 0 none | `00393EA0` |
| `01F81260` | ptr | the SaveloadManager, holding the autosave exclusion rows at `+0x50` | `001C18A0` |

## Modding notes

- A tool that writes a slot file must also write the zeroed-header then stamped-header sequence
  only if it wants the game's own semantics; the game never reads the companion files `icon.sys`
  and `static.ico`, it only deletes them.
- The autosave always targets slot 0; a manual save to slot 0 is overwritten at the next area
  change.
- A read that falls short reports 0 and leaves the destination partly overwritten; a reimplementation
  must copy before it compares, in that order.
- The game finds saves by probing `FFXII_000` to `FFXII_199` in the save directory, not by listing
  it; a file under any other name is ignored.
- To make an area change autosave, or stop it from autosaving, edit
  `disableAutosaveList.txt`: one `field,story,entrance,variable` row per line, CR LF line ends, no
  spaces, and no empty column in the middle of a row.

## Related

- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md)
- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](../World-Areas-And-Travel/zone-changes-and-mapjump.md)
