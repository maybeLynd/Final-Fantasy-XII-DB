---
title: "Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs"
kind: "system"
category: "Saving, loading and settings"
addresses: "0x00580EB0, 0x005819F0, 0x00581DA0, 0x00581B70, 0x00582040, 0x003BB920, 0x003BB9B0, 0x003BB2F0, 0x00866A00, 0x00862590, 0x00866AD0, 0x0057E4D0, 0x0057E310, 0x00582860, 0x00862130, 0x0057FE80, 0x0057F8C0, 0x0057EFE0, 0x00580CD0, 0x00580840, 0x003BA990, 0x008621E0, 0x003BA680, 0x003BB790, 0x001C1720, 0x02B407C0"
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

Each slot is one file named `FFXII_` plus the slot number as three digits (`0x005837F0`, kind 1,
through `0x003935C0` and `sprintf("%s%03d")`) in the save directory
(see the [save file format page](save-file-format.md)). The same formatter names `icon.sys`
(kind 0) and `static.ico` (kinds 2-4), the two companion files the save transaction queues for deletion
(a delete that reaches no file, see The storage queue below); it
returns the name in the controller record at `+0x128` and null when no controller is open
(`0x02CA99B8` = 0).

### The save and load screen

`0x00580EB0(controller, state, popup)` moves the screen between fifteen states and opens a popup
(`0x00583990(popupId, controller)`, kept at `+0xD8`) where one is listed:

| State | What the code does | Popup id | Popup text (`menu_message.bin`, through `0x00583990`'s table at `0x00D23DA0`) |
|---|---|---|---|
| 0 | arms the card-presence poll (`0x0057EC60`) | - (no popup) | |
| 1 | runs the device check (`0x0057EA40`), in save mode when byte `+0xEA` is 0 | - (no popup) | |
| 2 | confirms a new save | `0x15` | "Create new save data for FINAL FANTASY XII THE ZODIAC AGE?" |
| 3 | confirms an overwrite | `0x13` | "Save data ... already exists. Overwrite it?" |
| 4 | opens the save transaction `0x005819F0` as a child widget (`0x00244F50`, `0x00580FFF`) with the slot `+0xEB` and the save counter `+0xE4` + 1; plays sound `0x42` once per controller (`0x00580FBC`) | `0x10` | "Saving... Please do not close ..." |
| 5 | reports the save complete | `0x16` | "Save complete." |
| 6, 7 | the two trial-mode warnings | `0x19`, `0x1A` | "If you resume from this file, all trial mode progress will be lost. Are you sure you wish to proceed?", "Your Trial Version save data will no longer be playable. Are you sure?" |
| 8 | queues kind 1 with the callback `0x00580840`, then kind 9: read the slot's file into the active image, `0x56690` bytes; gauge target 30 | `0x11` | "Loading..." |
| 9 | reports the load complete | `0x17` | "Load complete." |
| `0xA` | confirms a format | `0x12` | "Memory card (PS2) in MEMORY CARD ... is not formatted. Format it now?" |
| `0xB` | queues kind 1 and kind `0xC` (format); gauge target 500 | `0xF` | "Formatting memory card (PS2). Do not remove/insert ..." |
| `0xC` | holds 120 frames (`+0xE8` = `0x78`) | `0x18` | "Format of memory card (PS2) in MEMORY CARD ... successful." |
| `0xD`, `0xE` | the error states; the popup id is the caller's | caller's | |

The popup table's entries are `{u32 text id, u8 kind, u8 flags, u8 sound}`; `0x002F9860` resolves a
text id as group `id / 1000` (2 = `menu_message.bin`) and index `id % 1000`.

The three storage results reach the screen as message `0x1D`: class 3 is the card-presence poll
(`0x0057EBB0`, queue kind 3), class `0xD` the device check (`0x0057E950`, kinds 4 and 5) and class
`0xF` the save transaction's completion (`0x00581B70`).

`0x0057ED40` disarms the card-presence poll: when the queue's front packet has already started (queue
`+0xDC` bit `0x1`) it sets `+0xDC` bit `0x2`, which makes the dequeue `0x00582240` return before that packet's
callback; otherwise it empties the queue (`+0x398` = 0). It also clears bits `0x1` and `0x2` of the poll
widget `0x02CA99D8`. The slot screen calls it when a slot is picked (sub-command `0x8001`) and on
sub-commands `0x8100`-`0x8102`; `0x00580A80` and the load lifecycle `0x00582860` call it too.

### The slot list

The slot screen `0x0057FE80` builds its list on message 1 from two tables: the slot status table
`0x02B407C0` (200 entries of 8 bytes, see Layouts; `0x003BB3E0(slot)` returns an entry's address and
`0x003BB600(slot, entry)` replaces one) and the header cache at `+0x1C0`, the first `0xA0` bytes of each
slot's image at `slot * 0xA0`, filled by the slot scan below.

- Save mode (`+0xEA` = 0) lists slots 1-199. Load mode lists, from slot 0, only the slots whose status
  is 2 or 4.
- A slot whose bit is set in the controller's bit set `+0x568` (200 bits) is first forced to status
  `{4, 1}`; the load callback sets that bit (below).
- The next save counter `+0xE4`, also stored at `0x02CA99B4`, becomes the highest header `+0x50` among
  the listed status-2 slots, slot 0's cache row and the active image.

The starting cursor is passed to `0x002D46F0`:

- In save mode it is the slot whose counter equals the active image's `+0x50` when that is non-zero,
  otherwise the readable slot other than 0 with the highest counter.
- In load mode, when slot 0 is not "Unused file", the autosave row is moved down to just after the newest
  manual save, and the cursor goes to the autosave when its counter is the highest, otherwise to that
  manual save.

`0x0057F8C0` draws a row. For status 2 it fills the row from the slot's cached header (`0x0057FB00`). Any
other status shows a line through `0x0057FA30` (text through `0x002F9860`), and when the screen was opened
with its flag bit `0x1` (`+0xE0`) every row is drawn as status 5:

| Status | Text (`menu_message.bin`) |
|---|---|
| 3 | `0x874` "In use by another game." |
| 4 | `0x873` "Corrupt save data." |
| 5 | `0x872` "Unused file." |
| any other | empty |

A row of any status other than 2 then gets a draw mode through `0x00393240` (`0x0057F965`): 0 when byte `+0xEA` is 0
and dword `+4` of the row's status record is non-zero, else 1 (`0x0057F947`-`0x0057F957`). A status-2 row skips the
draw mode and `0x0057FA30`: after `0x0057FB00` it jumps straight to the slot number (`0x0057F930`). The status-5 record
that flag bit `0x1` forces carries `+4` = 1 (`0x0057F93F`), so in save mode those rows get draw mode 0.

Every row also gets its slot number (`0x00393160`), except slot 0's row in load mode, which hides the
six number parts listed at `0x01F2CD10` and shows its own part `+0xD0`: it clears bit `0x1` of each part's dword
`+8` (`0x0057F9B2`) and sets that bit on part `+0xD0` (`0x0057F9CC`). The number is drawn by two calls,
`0x00393160(row, 4, 3, 9, n)` and `0x00393160(row, 1, 3, 9, n)` with `n = min(slot, 199)` (`0x0057F9D9`-`0x0057FA12`).
`0x0057F8C0` returns 1 on both paths (`0x0057F9C0`, `0x0057FA17`).

`0x0057FB00(row, list, header)` fills a status-2 row from the cached header:

- the region text is the region name of the area `+0x4C` (`0x003778B0`) and the area text its name
  (`0x00377B60`); with flag `+0x57` bit `0x1` set the row also shows its parts `+0xB8` to `+0xC8`, draws a
  frame (`0x002DC290`) and names the area `+0x80` instead, or `+0x4C` when that is 0;
- in the demo (`0x00264150`) the region text of persistence groups 7, 22, 25 and 29 (`0x00264F90`) is
  replaced by the `menu_message.bin` text `0x7EC`, `0x7EB`, `0x7EE` or `0x7ED` (`0x002F9860`), and the
  play time then shows zeros;
- the play time is hours `+0x18`, minutes `+0x1A` and seconds `+0x1B`, the last two capped at 59,
  drawn as three, two and two digits (`0x00393160`); 1,000 hours or more show 999:59:59;
- flag `+0x57` bit `0x4` (New Game-) shows the part `+0xD8`, which every other row hides
  (`0x0057FBA1`-`0x0057FBB3`, `0x0057FBFC`-`0x0057FC0E`): the "New Game−" badge, a 198 × 30 sprite from
  `DataFace_c.tm2` (atlas `dataface_c`, sub-image 0, frame 18) at the row's top left
  ([New Game+ and New Game-](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)).

Moving the cursor (sub-command `0x8000`) calls `0x0057EFE0(pane, header)` for a status-2 slot and hides
the pane for any other. `0x0057EFE0` fills the status pane, whose labels are ESPER (`0x875`), CLAN RANK
(`0x876`) and POINTS (`0x877`), from the cached header:

- the seven roster entries through `0x0057E6D0`: an entry whose character byte is `0xFF` is hidden, and
  the level is capped at 99;
- the gil `+0x08`, capped at 99,999,999;
- the Esper row, shown only when `+0x3C` (the summoned Esper's character row, see the [save file format page](save-file-format.md)) is
  not `0xFF`: `0x0035D330(2, +0x3C)` looks the row up in the character table `[0x02EBF130]` (`0x0031C5D0`)
  and `0x002B58B0` gives its name;
- the clan rank row, shown when `+0x44` is non-zero and the demo flag `0x0209A2A9` (`0x00264150`) is clear:
  the rank title `0x003153F0(+0x44)` for ranks 1-12 and the points `+0x40`, capped at 99,999,999.

### After a save or a load

The controller copies the active image's first `0xE240` bytes (`0x1C4` blocks of 128 bytes and 64
bytes) into a buffer it allocates at `+0x588` when it opens (`0x00583CB0`, called from `0x00582860`
message 1); `0x00583C00` copies them back.

`0x00580CD0`, the slot screen's handler for the class-`0xF` result, closes the popup at `+0xD8`
(`0x00244F00`), sets `+0xCC` of `0x02CA99E0` to 4 and calls `0x00581350(error != 0)`. On success it:

1. adds 1 to the counter `+0xE4` unless it is `0xFFFFFFFF`, and writes it to the active image's
   `+0x50` and to `0x02CA99B4`;
2. sets bit `0x4` of the controller's `+0xC4`;
3. copies the active image's first `0xA0` bytes to the slot's cache row and refreshes the pane
   (`0x0057EFE0`);
4. stores `{2, 0}` in the slot's status entry, recounts `+0xED` (status 5) and `+0xEE` (status 5,
   status 2 or the room flag set), and moves to state 5.

On an error it moves to state `0xD` with popup 5, "Save failed." (`0x818`).

`0x00580840` is the load and format callback; it does nothing once the screen has set `+0xE0` bit `0x10`.
It takes the screen as the low 32 bits of its third argument (`0x00580847`) and ignores kinds other than 9 and
`0xC` (`0x00580861`, `0x005809D6`).

For both kinds it first closes the popup at `+0xD8` (`0x00244F00`) and stores 0 there, sets `+0xCC` of
`0x02CA99E0` to 4 when that widget exists, and calls `0x00581350(error != 0)` and `0x00254CB0(0)` (`0x0058087F`-`0x005808C3`,
`0x005809DC`-`0x00580A16`). Every error path raises bit `0x4` in the gauge's flags at `[0x02CA99C8] + 0xC8` when the
gauge exists (`0x0058091A`, `0x00580A56`).

For the read (kind 9):

| Result | What it does | Next state, popup |
|---|---|---|
| 0 | `0x005813E0`, then `0x00247510([+0xC0], 0x10, 4)` (`0x005808D1`-`0x005808E6`) | 9, "Load complete." |
| 8 | restores the image head (`0x00583C00`), stores `{4, 1}`, sets the slot's bit in `+0x568`, hides the pane; the bit only when the controller `0x02CA99B8` exists and the slot is below 200 (`0x0058095D`-`0x00580983`); the pane, when `+0xC8` is set, gets 0 at its `+0x100` and `0x00247870(pane, 0)` (`0x0058098A`-`0x0058099F`) | `0xE`, popup 10, "Unable to load. Save data is corrupted." (`0x86D`) |
| any other | restores the image head | `0xD`, popup 6, "Load failed." (`0x81C`) |

A failed load therefore puts back the header and the payload up to the first group bank; the rest of
the image keeps whatever the read copied into it. For the format (kind `0xC`), success clears `+0xE0` bit `0x1`,
sets bit `0x8`, runs `0x005813E0` and moves to state `0xC` (`0x00580A1F`-`0x00580A45`), and an error moves to `0xD`
with popup 4, "Failed to format memory card (PS2)." (`0x814`).

### The save transaction

`0x005819F0` opens the transaction on message 1: it copies the request's slot, counter and flags into
the record (`+0xCD` slot, `+0xD0` counter, `+0xC8` = request `+0x18` bit `0x1`, the short variant),
keeps the image's header dword `+0x50` at `+0xD4`, sets the gauge total to `0x1DA`, or `0x17C` for
the short variant (`0x005817D0`, target minus `0x19`), registers the completion callback `0x00581B70`
on the storage queue, and runs step 1 (`0x00581DA0`).

In more detail, message 1 sets `0x02CA99B0` to 1 (`0x00581A57`), keeps the request's first two qwords at `+0xC0`
and `+0xE0` (`0x00581A7F`, `0x00581A8A`), and stores 0 in the index `+0xCE`, the state `+0xCC` and the progress total
`+0xDC` (`0x00581A9B`, `0x00581ABD`, `0x00581B1B`). It calls `0x00244960([+0xC0], record)`, `0x00247870(record, 0)`,
`0x00247930(record, 0x64)` and `0x00254CB0(1)` (`0x00581ACA`-`0x00581AEB`). The callback goes in as a kind-1 packet
`{1, 0x00581B70, low 32 bits of the record}`, queued only when the queue `0x02CA99C0` exists (`0x00581B25`-`0x00581B47`).

Message `0xF` stores 0 in `0x02CA99B0`, calls `0x00254CB0(0)` and then `0x00247510([+0xC0], 0xF, 0xA)`
(`0x00581A24`-`0x00581A47`); message `0x12` calls `0x00247510([+0xC0], 0x12, 0xA)` (`0x00581A1D`). Both return 0; every
other message goes to `0x005C5230` (`0x00581A18`).

`0x00581DA0(record, state)` does nothing when `state` equals the current state `+0xCC` (`0x00581DD2`), and for a
state outside 1-8 it only stores the state (`0x00581DEA`, `0x00581FF4`). Otherwise, after the step and its weight
(the table below), it hands the new total to the gauge's `0x00581860` (`0x00581FE3`-`0x00581FEF`) and stores the state
in `+0xCC` (`0x00581FF4`).

Step 7 queues its kind-8 packet only when the queue `0x02CA99C0` exists (`0x00581F47`), named through `0x00583700`
(`0x00581F3B`) with one descriptor (`0x00581F77`); its weight counts either way. States 5 and 6 run state 4's arm,
the companion name of kind `+0xCE + 2` (`0x00581E9E`-`0x00581EAB`).

`0x00581DA0(record, state)` performs one step and adds its weight to the progress total `+0xDC`:

| State | What it queues | File | Weight |
|---|---|---|---|
| 1 | zeroes the image's first 8 bytes in memory and writes them (kind 7) | the slot file | `0x10`, short `0x50` |
| 2 | delete (kind `0xB`) | `icon.sys` | `0x10`, short `0x14` |
| 3 | delete | the slot file | `0x10` |
| 4 | delete | `static.ico` | `0x10` |
| 7 | builds the submission descriptor (`0x005832B0`), runs the header finaliser `0x00583D60` and keeps its return, the plain CRC (`0x00583F97`), at `+0xD8`, then writes the whole image (kind 8, `0x56690` bytes) | the slot file | `0x168`, short `0xE6` |
| 8 | puts `{checksum, 1}` in the image's first 8 bytes and writes them (kind 7) | the slot file | `0x32` |

The callback `0x00581B70(kind, error, record)` accepts only the kind the current state waits for
(7 for states 1 and 8, `0xB` for 2-4, 8 for 7) and steps on:

- 1 to 2; 2 to 3, or to 7 in the short variant (`0x00581BFD`-`0x00581C06`); 3 to 4 with the counter
  `+0xCE` cleared; 4 to 7; 7 to 8.
- States 5 and 6 share state 4's arm, and no call reaches them: the dispatcher's two callers (`0x005819F0`,
  `0x00581B70`) ask for steps 1, 2, 3, 4, 7 and 8, and for 4 + index only while the index is below 1
  (`0x00581C94`-`0x00581CA0`, after the increment at `0x00581C81`).
- On the last completion, or on any error, it posts message `0x1D` with class `0xF`, the device
  byte from the queue's `+0x39A` and the error code to the controller, and releases the record.
  The device byte is `0xFF` when no queue exists (`0x00581D00`). The message goes through
  `0x00247510([+0xC0], 0x1D, message)` (`0x00581D52`) and the release is `0x00244F00(record)` (`0x00581D5A`).
- On success it first runs `0x005813E0` (`0x00581D19`).
- On an error it also restores the image's `+0x50` from `+0xD4` and raises bit `0x4` in the gauge's
  flags.
- A callback of another kind, or in a state outside 1-8, returns with nothing done (`0x00581B97`, `0x00581BB6`).

So a full save runs states 1, 2, 3, 4, 7, 8 and a short save 1, 2, 7, 8: the short variant still
queues the delete of `icon.sys`, and keeps the old slot file until step 7 overwrites it. No queued delete
removes a file (The storage queue below), so in the full variant too the old slot file stays until step 7
overwrites it. Between step 1 and step
8 the file on disk carries a zeroed header; the second dword is 1 only on a finished save. The
finished file carries the plain CRC at `+0x00`; the finaliser's complement exists only in the image
between step 7 and step 8.

### The storage queue

`0x00582730(path, buffer, size)` queues kind 7, `0x005826D0(path)` kind `0xB`, and the transaction
itself kind 8, all through `0x00582540` on the queue object `0x02CA99C0`. `0x00582040` starts the front
packet:

| Kind | Handler | What the handler sets and runs |
|---|---|---|
| 1 | copies the packet's callback into the queue (`+0xC0`, `+0xC8`) | nothing |
| 2 | `0x003BB730`; the device byte to `+0x39A` | nothing |
| 3 | `0x003BB2C0` | command 5, busy flag clear, no driver |
| 4 | `0x003BB3B0` | command 4, busy flag clear, no driver |
| 5 | `0x003BB740` | copies the name to `0x02B4055C`, sets busy, runs `0x003BAC90` |
| 6 | `0x003BB6A0(index < 200, ptr, name)` | stores `ptr` at `0x02B407C0[index]`, command 8, runs `0x003BA720` |
| 7 | `0x003BB920(name, 0, buffer, size)` | command 2, runs the worker `0x003BAEB0`; refused for a zero size |
| 8 | `0x003BB9B0(name, descriptors, count)` | command 2 with up to 5 descriptors of `0x38` bytes, runs `0x003BAEB0` |
| 9 | `0x003BB440(name, 0, buffer, size)` | the read of `size` bytes |
| `0xA` | `0x003BB4C0` | copies a `0xB8`-byte record to `0x02B40FF0`, command 6, runs `0x003BA990` |
| `0xB` | `0x003BB2F0` | command 7, runs `0x003BA5F0` (its states 0, 1 and `0xC` reach `0x00862130`); the packet's name is not passed on (below) |
| `0xC` | `0x003BB380` | the format command |

`0x00582040(queue)` returns 0 and starts nothing when the queue is null, holds no packet (`+0x398` = 0) or its
front packet has already started (`+0xDC` bit `0x1`) (`0x00582064`-`0x0058207D`). Otherwise it sets that bit
(`0x005820BD`) and returns 1 for kinds 1 and 2, which finish at once, and for kind 0 and kinds above `0xC`, which
run no handler (`0x005820B8`). Kinds 3 to `0xC` return 0, the packet still running.

`0x003BB920` and `0x003BB9B0` refuse while the machine is busy (`0x02B40E10` = 1), copy the name to
`0x02B40EC8`, set command 2 at `0x02B40E1C` and start the worker `0x003BAEB0`. The delete command runs
`0x00862130`: `_wfopen_s(path, "rb")`, and when that succeeds `fclose` then `_wremove`. `0x00862130(device, name)`
never reads its first argument. It builds the path in a zeroed `0x200`-byte buffer as the save directory
`0x02EAF6E0` followed by the name, with `"%s%S"` through `0x008629C0` (`0x0086214E`-`0x0086217D`), and returns 0 on
both paths (`0x008621BC`).

`0x003BB2F0` takes no name: it never reads the packet's name that `0x00582040` passes (`0x005821F1`). It stores command
7, zeroes the retry count, the result and the index, sets the busy flag to 1 with step 0 in one 8-byte store
(`0x003BB2F2`-`0x003BB310`) and jumps to `0x003BA5F0` with 0 (`0x003BB2FC`, `0x003BB31B`); it does not test the busy flag.

`0x003BA5F0` moves from step 0 to step 1 (`0x003BA662`). In step 1 it calls `0x00862130(device 0x02B40E20, 0x02B40E3E)` and
moves to step `0xC` (`0x003BA63E`-`0x003BA651`). In step `0xC` it ends with result 0 when the status it is given is
0 or -4, and with result 9 otherwise (`0x003BA608`-`0x003BA633`).

The name `0x003BA5F0` gives is the text at `0x02B40E3E`, 22 bytes into the command-8 name `0x02B40E28`. No instruction
addresses `0x02B40E3E` except that read (`0x003BA645`). `0x02B40E28` is written only by `0x003BB6A0`'s copy of a kind-6
name (`0x003BB6B9`), a slot file name of nine characters, `FFXII_` and three digits (`0x0057F2F5`, `0x003935E1`), and
by `0x003BB4C0`'s empty name (`0x003BB50E`).

The text at `0x02B40E3E` therefore stays empty, and the path names the save directory itself. `_wfopen_s` cannot
open a directory for reading, so `0x00862130` reaches neither `fclose` nor `_wremove` (`0x008621A2`), and the three
deletes the save transaction queues remove no file.

The two write starters in detail:

- Both refuse for any non-zero busy flag and then return 0 (`0x003BB924`, `0x003BB9B4`). Otherwise they set the busy
  flag to 1 and the step `0x02B40E14` to 0 in one 8-byte store (`0x003BB996`, `0x003BBA36`), call `0x003BAEB0(0)` and
  return 1.
- `0x003BB920` also refuses a zero size (`0x003BB93A`). It copies its name up to the NUL (`0x003BB950`-`0x003BB95C`),
  stores the buffer at `0x02B40EF0`, the start offset at `0x02B40EFC` and the size at `0x02B40EF8` (descriptor 0's
  `+0x28`, `+0x34` and `+0x30`) and the count 1 with index 0 (`0x003BB981`).
- `0x003BB920` zeroes the retry count `0x02B40EC0` and the result `0x02B40E18` (`0x003BB967`, `0x003BB96D`).
- `0x003BB9B0` never reads its first argument. It copies `min(count, 5)` descriptors of `0x38` bytes, each with its
  name at `+0x00`, to `0x02B40EC8` (`0x003BB9CC`-`0x003BBA21`; a count of 0 or less copies no descriptor), and
  zeroes the retry count, the result and the index `0x02B40FE4` (`0x003BBA2F`-`0x003BBA48`).

### The worker's status poll

`0x003BB790` runs at the end of every pass of the request pump `0x0032E070` while `0x0036FD50()` (the byte
`0x02AD9E00`) is non-zero (`0x0032E2B4`-`0x0032E2BD`). With the busy flag `0x02B40E10` at 0 it stores 0 in the dwords
`0x02B40E00` and `0x02B40E04` (`0x003BB90F`, `0x003BB915`) and returns; with a busy value other than 0 or 1 it
returns at once (`0x003BB7A5`).

While the machine is busy (1) it reads the status of the last file call, `0x02EAF8E0`, through
`0x00862600(unused, a, b)`, which stores 0 at `a`, the status at `b` and returns 1. `0x003BB790` gives a null `a`
(`0x003BB7B0`), which `0x00862600` skips. Its tests for an answer of −1 (clear the busy dword, `0x003BB902`) and for
any answer but 1 (return) therefore never fire (`0x003BB7B7`-`0x003BB7C3`).

A status from -19 to -11, from -79 to -70 or from -59 to -40 ends the command with result 4,
and -5 with result 7; both clear the busy flag and the step `0x02B40E14` in one 8-byte store (`0x003BB8EA`,
`0x003BB8D2`). Any other status goes to the command's handler:

| Command (`0x02B40E1C`) | Handler |
|---|---|
| 0 | `0x003BAC90` |
| 1 | `0x003BA7B0` |
| 2 | `0x003BAEB0` |
| 3, 4, 5 | no handler: the command ends with result 0 |
| 6 | `0x003BA990`, the slot scan |
| 7 | `0x003BA5F0` |
| 8 | `0x003BA720` |
| 9 | `0x003BA680`, the save-data check |

The handlers are tried in the order 1, 6, 2, 0, then 3 to 5, 7, 8 and 9, and the command is read again after
each handler (`0x003BB803`-`0x003BB8B7`). A handler that changes the command is therefore followed in the same pass
by a later handler for the new one. Commands 3, 4 and 5 store 0 in the step and the result `0x02B40E18` in one
8-byte store and clear the busy dword (`0x003BB876`, `0x003BB87D`), and `0x003BB790` then returns without trying 7, 8
or 9.

The result is kept at `0x02B40E18` (`0x003BB420` returns it) and the busy flag at `0x02B40E10` (`0x003BB430`).

The handlers keep their own words beside the command:

- Each handler is a switch on the step `0x02B40E14`; the worker's has 18 steps (`0x003BAEEE`-`0x003BAF1E`).
- A file is described by `0x38`-byte descriptors from `0x02B40EC8`: the name at `+0x00`, the buffer at `+0x28`, the size
  at `+0x30` and a start offset at `+0x34`. A positive offset is passed to `0x008625D0` before the read or write
  (`0x003BA85B`-`0x003BA860`, `0x003BAB92`-`0x003BAB97`, `0x003BB039`-`0x003BB040`).
- `0x003BB9B0` copies up to 5 descriptors; the worker walks them with an index against a count (`0x003BB166`-`0x003BB177`).
- The write waits before it closes the file: `t = t + max(0.001, (f32)0x0017D270())` adds the frame time, at least
  0.001, to the time t at `0x02B4112C` (`0x0017D270`, `0x003BB097`-`0x003BB0BB`), until 1.0 has passed while `0x00583920`
  reports a save write, or 0.1 otherwise: it waits while `t < (0x00583920() ? 1.0 : 0.1)` (`0x003BB0C7`-`0x003BB0E9`).
- The device check counts its retries and gives up, with the busy flag clear, after the fifth (`0x003BADA0`-`0x003BADBC`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B40548` | `i32` | 0 (zero-filled tail of `.data`) | the phase of the empty-slot requirement: at the start of state `0x10` the extra unit goes to the first empty slot when it is 0 and then to every other one (`0x003BAAB5`, `0x003BAAC0`) | `0x003BA990`, 0 in state 0 (`0x003BAA4E`) | `0x003BA990` (`0x003BAAA9`) |
| `0x02B40558` | `i32` | 0 (zero-filled tail of `.data`) | the slot of the file a command is on, the index of its status entry `0x02B407C0 + 8 x slot` | `0x003BA990`, the answer of `0x003BA320` in state `0x15` (`0x003BAB38`); `0x003BAC90`, the same (`0x003BAD09`); `0x003BB6A0`, its first argument (`0x003BB6E0`) | `0x003BA990` (`0x003BABCA`, `0x003BABE3`, `0x003BAC18`, `0x003BAC47`); `0x003BA720` (`0x003BA76B`, `0x003BA788`) |
| `0x02B40E14` | `i32` | 0 (zero-filled tail of `.data`) | the running command's step | 42 stores in the handlers, the starters and the poll: the worker `0x003BAEB0` at 11 sites (`0x003BAF36` to `0x003BB1BE`), `0x003BA7B0` at 8 (`0x003BA7DB` to `0x003BA930`), the poll `0x003BB790` at `0x003BB876`; `0x003BB440` stores 1 with the result 0 (`0x003BB49C`, an 8-byte store); the 8-byte busy stores at `0x02B40E10` (`0x003BB8EA`, `0x003BB996`, `0x003BBA36`) zero it | `0x003BA5F0` (`0x003BA5F4`), `0x003BA680` (`0x003BA684`), `0x003BA720` (`0x003BA724`), `0x003BA7B0` (`0x003BA7B4`), `0x003BA990` (`0x003BA9A2`), `0x003BAC90` (`0x003BAC96`), `0x003BAEB0` (`0x003BAEEE`) |
| `0x02B40E24` | `i32` | 0 (zero-filled tail of `.data`) | the open file's handle | `0x003BA7B0` (`0x003BA853`), `0x003BA990` (`0x003BAB8A`), `0x003BAEB0` (`0x003BB02E`), each the non-negative result of the open | `0x003BA7B0` (`0x003BA8A8`, the read; `0x003BA8C6`, the close); `0x003BA990` (`0x003BAB9C`, `0x003BABB5`); `0x003BAEB0` (`0x003BB08F`, `0x003BB0EF`) |
| `0x02B40E28` | `char[]` | 0 (zero-filled tail of `.data`) | the file name of command 8 | `0x003BB6A0`, the name copied up to its NUL (`0x003BB6B9`-`0x003BB6DE`); `0x003BB4C0`, an empty name (`0x003BB50E`) | as a path, through its address: `0x003BA720` to `0x003BA3E0` (`0x003BA735`); `0x003BA7B0` to `0x008620D0` (`0x003BA7F7`); `0x003BAEB0` to `0x008620D0` (`0x003BAF4F`, `0x003BAF8B`) |
| `0x02B40EC0` | `i32` | 0 (zero-filled tail of `.data`) | the device check's retry count | `0x003BAC90`, 0 (`0x003BAD5C`) and 1 more (`0x003BADA8`); 0 at 15 other sites in the handlers and starters (`0x003BA66C` to `0x003BBA2F`) | `0x003BAC90` (`0x003BADA0`), which gives up above 4 |
| `0x02B40EFC` | `i32` | 0 (zero-filled tail of `.data`) | descriptor 0's start offset (`+0x34`) | `0x003BB440` (`0x003BB470`) and `0x003BB920` (`0x003BB973`), their second argument; `0x003BB4C0`, 0 (`0x003BB527`) | `0x003BA7B0` (`0x003BA84D`); `0x003BA990` (`0x003BAB82`) |
| `0x02B40FE0` | `i32` | 0 (zero-filled tail of `.data`) | the number of descriptors | `0x003BB920`, 1 (`0x003BB981`, an 8-byte store that also zeroes the index); `0x003BB9B0`, its count (`0x003BB9D3`); `0x003BB4C0`, 0 (`0x003BB53B`) | `0x003BB9B0` (`0x003BBA1B`, its copy loop); `0x003BAEB0` (`0x003BB169`) |
| `0x02B40FE4` | `i32` | 0 (zero-filled tail of `.data`) | the descriptor the worker is on | `0x003BAEB0`, 1 more (`0x003BB170`); 0 from `0x003BB9B0` (`0x003BBA48`) and the other starters (`0x003BB2D2` to `0x003BB77A`, 9 sites); `0x003BB920`, with the count (`0x003BB981`) | `0x003BAEB0` (`0x003BAEBA`), which picks the descriptor `0x02B40EC8 + 0x38 x index` |
| `0x02B40FE8` | `void*` | 0 (zero-filled tail of `.data`) | the cache row of the file being read: `0x02B40EF0` plus the slot times the row size `0x02B40EF8` | `0x003BA990` (`0x003BAB72`) | `0x003BA990` (`0x003BABA9`), as the buffer of the read `0x00862590` |
| `0x02B41128` | `u8` | 0 (zero-filled tail of `.data`) | the save and load screen's mode as the listing command receives it: the controller's byte `+0xC1`, 0 when the screen was opened to save and 1 otherwise | `0x003BB4C0`, its second argument (`0x003BB4CE`, `0x003BB5B5`), which `0x00582040` passes from `[0x02CA99B8] + 0xC1` (`0x005821E0`, `0x005821E7`) | no reader: no RIP-relative, image-base-relative or address-forming reference reads it, the record copy that `0x003BB4C0` makes from `0x02B40FF0` ends `0xB8` bytes on, and no 8-byte pointer or 4-byte RVA in the image holds its address |
| `0x02B4112C` | `f32` | 0 (zero-filled tail of `.data`) | the time the write has waited before its close | `0x003BAEB0`: 0 (`0x003BB074`, `0x003BB0F8`), and the frame time added (`0x003BB0BB`) | `0x003BAEB0` (`0x003BB0AB`, `0x003BB0E2`) |

The controller's `+0xC1` comes from the screen's creation. The request dispatcher `0x0027F5D0` keeps its request's second
dword at `+0xD4` (`0x0027F74F`) and passes it to `0x00583930` (`0x0027F979`, `0x0027F984`), whose creation block holds it as a
flag at `+0x08` (`0x0058394E`, `0x00583955`); the screen procedure `0x00582860` copies the flag to `+0xC1` on message 1
(`0x005828C2`, `0x005828CB`). A request argument of 0 is the save: the dispatcher first builds the save image with
`0x005844A0` (`0x0027F8DB`, `0x0027F953`).

### The slot scan

`0x0057F6B0` queues kind 1 with the callback `0x0057F630`, then kind `0xA` with the pattern `FFXII_*`, the
header cache and a row size of `0xA0`. `0x00393630(buffer, size)` writes the pattern with
`sprintf("%s*")` and returns an empty string when the buffer is under 64 bytes. Kind `0xA`
(`0x003BB4C0`) copies the pattern to `0x02B4055C`, the buffer and row size to `0x02B40EF0` and `0x02B40EF8`, and
starts command 6, `0x003BA990`, which steps on each call:

1. State 0 sets every status entry to `{1, 0}`, takes the free space `0x02B4054C` from `0x02B40E0C` and lists
   the files with `0x008621E0(device, pattern, 0, 200, 0x02B41140)`. With no file found it goes to state `0x10`,
   otherwise to `0x15`.
2. State `0x15` handles one listed file per call. `0x003BA320(name)` gives its slot; the file is opened
   for reading (`0x008624D0`), read for `0xA0` bytes into the cache at `slot * 0xA0` (`0x00862590`) and
   closed (`0x008620E0`).
3. A full read stores status 2. A short read stores 4, with the room flag 1 when the requirement from
   `0x003BA3E0` fits the free space (which it then reduces) and 0 otherwise.
4. State `0x10`, after the last file: every entry still at status 1 becomes `{5, 1}` when its
   requirement fits the free space, which it reduces, and `{3, 0}` when it does not. The machine is then
   idle.

The requirement for an empty slot alternates between 95 and 94 units:
`(0x02B40540 + 1) / 2 + 0x02B40544 + 1`, plus 1 for every other slot.

`0x003BA320(name)` counts the pattern's characters before the `*` (ignoring `/`), requires two decimal
digits at that position of the name, and returns `atoi` of up to three characters from there; anything
else returns -1.

`0x008621E0(device, pattern, unused, count, out)` does not read the directory; it probes names:

- With `count` = 1 it opens the save directory plus the pattern (`"%s%S"`), copies the name to
  `out + 0x20` and the file size to `out + 0x10`, and returns 1 when the file exists, else 0.
- Otherwise the prefix is the pattern without its `*`, and the function tries prefix plus `%03d` for 0
  to `count - 1`. Each file that opens adds a `0x40`-byte row to `out`: the size at `+0x10` and the name
  at `+0x20`. It returns the number of rows.
- Either way the return value is also stored as the status `0x02EAF8E0`.

### The space requirement

The figures come from the PS2 memory card. `0x00393600(kind)` gives a file size for the kinds of the name
formatter `0x005837F0`: 964 bytes for kind 0 (`icon.sys`), `0xE240` (57,920) for kind 1 (the slot file)
and `0x8398` (33,688) for kinds 2-4 (`static.ico`). `0x003936B0` passes the sizes of kinds 0-2 to
`0x003BB630`, which stores the count, 3, at `0x02B40540` and the total in 1 KB units, each size rounded up
(1 + 57 + 33 = 91), at `0x02B40544`, and returns the total in bytes. `0x003936B0` adds `0x2400` and returns
102,400.

- The storage queue keeps that value at `+0xD0` (`0x005823B0`).
- The popup opener `0x00583FD0` rounds it up to KB for the "at least ... KB" text of popups 1, 7 and 9
  (popup-table kinds 3 and 4), which therefore reads 100.

`0x003BA3E0(name, out, n)` ignores the name. It sets `out` to `(max(0, 0x02B40540 - 2 * ((n - 1) / 2)) + 1)
/ 2`, adds `0x02B40544` and subtracts the rounded-up KB of the first `n` rows of the table at
`0x02B405D0` (stride `0x40`), and clamps the result at 0; it always returns 1. The free space comes from
the device check (command 0, `0x003BAC90`): `0x00862490` writes `0x2000000` to `0x02B40E0C`, 2 to
`0x02B40E08` and 1 to `0x02B41130`, and sets the status to 0.

### The save-data check

The title-screen script asks whether any save exists with two verbs:

1. `fsttl_opendatacheck` (`0x00511F20`, a jump to `0x00394600`) creates the `0x108`-byte widget `0x00393EA0`
   unless a check is running (`0x01EFAC10` = 2).
2. The widget's message 1 sets `0x01EFAC10` to 2. On its first message 2 it calls `0x0036FD80(1)`, writes
   the pattern `FFXII_*` with `0x00393630`, selects device 0 (`0x003BB730`) and starts command 9 with
   `0x003BB320`.
3. `fsttl_getdatacheckstatus` (`0x00511F30`) returns `0x01EFAC10` through `0x00394440`: 2 while running, 1
   when a save file exists, 0 when no save file does, and 3, the byte's value in the image, before the first check.

`0x003BB320(pattern)` copies the pattern to `0x02B4055C`, sets command 9 at `0x02B40E1C`, the busy flag and
state 1. The handler `0x003BA680` lists the files (`0x008621E0(device, 0x02B4055C, 0, 200, 0x02B41140)`) and
moves to state `0xD`; on the next poll a positive count ends the command with result 0, anything else
with result 9.

The device is the byte `0x02B40E20` (`0x003BA6C6`). The count is the handler's argument, the status `0x02EAF8E0` that
the poll passes and `0x008621E0` stored. Result 0 is one 8-byte store that zeroes the step and the result
(`0x003BA69E`), followed by clearing the busy flag (`0x003BA6A5`). Result 9 (`0x003BA6B0`) is followed by an 8-byte
store that clears the busy flag and the step (`0x003BA6BA`). In state 0 the handler only moves to state 1 and zeroes
`0x02B40554` and the retry count `0x02B40EC0` (`0x003BA6FD`-`0x003BA70F`); in any other state it returns (`0x003BA696`).

When the machine is idle the widget reads the result: 0 sets `0x01EFAC10` to 1; otherwise it runs
command 9 once more and then sets `0x01EFAC10` to 1 or 0 from the second result. Either way it calls
`0x0036FD70` and closes itself.

### The file layer

The worker reads and writes through a byte vector (`0x01F44D40` begin, `0x01F44D48` end, `0x01F44D50`
capacity):

- Open (`0x008666B0`) loads the whole existing file into the vector, decoding the container when it
  is one; in write mode a missing file leaves the vector empty.
- Read (`0x00866A00(cursor, dest, count)`) copies byte by byte while the cursor is inside the vector
  and returns 1 only when every requested byte was copied. The wrapper `0x00862590(mode, ..., size)`
  returns `copied ? size : 0` for mode 0 and -4 otherwise, so a short read overwrites the front of
  the destination, advances the cursor by the bytes it took, and reports 0.
- Write (`0x00866AD0(cursor, src, count)`) overwrites inside the vector and appends past its end; no
  file is touched until close. Its wrapper `0x00862620(mode, src, size)` stores `ok ? size : 0` as the
  status for mode 0 and -4 otherwise.
- `0x00866AD0` returns 0 for a null cursor or source (`0x00866AE0`-`0x00866AEC`) and 1 for any other call
  (`0x00866B5E`). A byte whose cursor is at or past the end goes to the end: in place while the end is below the
  capacity `0x01F44D50` (`0x00866B22`-`0x00866B40`), otherwise through `0x00865720(vector, end, src)` (`0x00866B4E`). The
  cursor moves on by one byte either way (`0x00866B53`).
- `0x00866A00` returns 0 at once for a null cursor or destination (`0x00866A08`-`0x00866A10`), and 1 for a count of 0
  (`0x00866A61`).
- Seek (`0x008625D0(mode, offset, origin)`) calls `0x00866A80` for mode 0, which moves the cursor to
  `offset` from the start (origin 0), the cursor (1) or the end (2) only when the new position is inside
  the vector; the status is set to 0 either way.
- Close (`0x00866200`) writes the vector as a new container to a temporary file and copies it over the
  slot file (see the [save file format page](save-file-format.md)). Every written file is a replaced copy, never written in place;
  step 8's 8-byte write loads the file step 7 wrote, patches its first 8 bytes and rewrites it.

The stream calls keep one open file. Each acts only for handle 0 (`test ecx, ecx` at the head of each) and works on
the object at `0x02EAF8E8`. The opener `0x008624D0` first closes a file still open, writing it out through `0x00866200`
(`0x00862508`), and then keeps the new one:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAF8E8` | `void*` | 0 (zero-filled tail of `.data`) | the open file's byte-vector object from `0x008666B0` | `0x008624D0`, 0 after closing the old file (`0x0086250D`) and the new object (`0x00862548`); the closer `0x008620E0`, 0 (`0x008620FB`) | `0x008624D0` (`0x008624F4`); `0x008620E0` (`0x008620E8`), which passes it to `0x00866200`; the read `0x00862590` (`0x0086259D`), the seek `0x008625D0` (`0x008625D8`) and the write `0x00862620` (`0x0086262D`) |

### The autosave on an area change

`0x0057E4D0`, the autosave widget, runs `0x0057E310` on construction (message 1) and again on
sub-commands `0x8100`-`0x8102`. `0x0057E310` copies the capture image to the write buffer, stores the
CRC, the 1 and the save counter in its header, names the file for slot 0 (`0x00584610` with slot 0,
`sprintf("%s%03d")`), hands the descriptor to `0x003BB9B0` and sets the busy flag `0x02CA99E8`.

Before `0x0057E310`, message 1 stores 0 at `+0x98` with 512 and 448 at the words `+0x9C` and `+0x9E` (the dwords at
`0x01E0C1D8` and `0x01E0C1DC`, written only for a non-null widget), clears bit `0x800` of `+0x40`, and stores 50 at
the word `+0x44` and 0 at `+0xC8` (`0x0057E5A6`-`0x0057E5E0`). After it, it calls `0x00244960([0x0208EA50], widget)` and
`0x00247870(widget, 1)` (`0x0057E5F5`, `0x0057E602`).

The sub-commands arrive as message `0xC` (`0x0057E4F2`); after `0x0057E310` the widget stores 0 in its popup
pointer `+0xC0` (`0x0057E522`), and other sub-commands do nothing. Message 4 returns 0, and messages other than 1,
2, 4 and `0xC` go to `0x005C5230` (`0x0057E4FF`).

`0x0057E310(widget)` copies `0xACD` blocks of `0x80` bytes and 16 more (`0x0057E347`-`0x0057E3A6`). It takes the CRC
over the active buffer's `+0x08` for `0xE1F8` bytes (`0x0057E3A9`-`0x0057E3BF`) and raises the save counter `0x02CA99B4`
only while it is below `0xFFFFFFFF` (`0x0057E3CE`-`0x0057E3DD`). The descriptor it hands over is the 56 bytes at widget
`+0xD0`: the name from `0x00584610(name, 0x40, 1, 0)` at `+0x00`, the write buffer at `+0x28` and the size
`0x56690` at `+0x30` (`0x0057E3E0`-`0x0057E42F`).

It also builds `FFXII_000` with `0x003935C0` and `sprintf("%s%03d")` on its stack (`0x0057E43A`-`0x0057E472`), calls
`0x0036FD80(1)` (`0x0057E479`), and then calls `0x003BB9B0` with that text, the descriptor and a count of 1
(`0x0057E47E`-`0x0057E490`).

On message 2, once the machine is idle (`0x003BB430()` = 0), the widget looks at the result
`0x003BB420()`:

- zero: the widget completes (`+0xC8` = 1, `0x02CA99E8` = 0, `0x0036FD80(0)`, `0x00245020`);
- non-zero with no popup open (`+0xC0` = 0): it opens popup 1 through `0x00583FD0(1, widget)`, text
  2065, "Insufficient disk space. In order to create a save game, at least ... KB of free space is
  required."

Nothing is shown while the write runs.

While the machine is busy, message 2 returns 0 (`0x0057E536`). With a non-zero result and a popup already open it
also returns 0 (`0x0057E54D`). Before it opens the popup it stores 1 in the busy flag `0x02CA99E8` (`0x0057E559`); it
gives `0x00583FD0` the third argument 1 (`0x0057E553`) and keeps the popup at `+0xC0` (`0x0057E56E`).

### Which area changes autosave

The zone-change stager `0x003145E0` captures the autosave only when `0x0020E500(field, story counter,
entrance)` returns non-zero (`0x00314774`; the story counter is `0x00265270()`). `0x0020E500` passes the
SaveloadManager (`0x01F81260`, `0x001C18E0`) to `0x001C1720(manager, field, story, entrance)`:

1. It returns 0 when the manager's dword `+0x0C` is not 0 (the constructor `0x001C0E20` clears it) or
   the field id is not positive.
2. When bit `0x1000` of the party block's flag dword is set (`0x00236760`), the story value is replaced
   by -2.
3. It walks the rows of the vector at `+0x50` (16 bytes each, see Layouts). A row matches when its
   field equals the field, its entrance is 0 or equal, and its story value is 0, equal, or its variable
   is non-zero with `0x002EF390(variable)` true (the active image byte `+0xC00 + variable` is 1).
4. A matching row returns 0, so no autosave; no match returns 1.

The rows come from `./GameData/disableAutosaveList/disableAutosaveList.txt` (`0x008F9AC8`):

- At start-up `0x001C1710` queues the file through `0x001C1810`, with `0x001C18F0` as the callback, which
  runs the parser `0x001C0F20` while the manager exists.
- The parser reads one token per line (`sscanf("%s")`), steps over it plus two bytes, splits it at
  commas into four columns and converts each with `strtol` (a missing column is 0).
- It appends the rows with `0x001858A0`, the vector's grow-and-insert, and frees the text.
- When the second column is empty the parser takes the rest of the line as that column, so it
  converts to 0 and the later columns are 0.

Two more entry points that fetch the manager, `0x0020E540` (from `0x002EF690`) and `0x0020E5C0` (from
`0x0027F5D0`), end in a jump to the empty stub `0x0016D6A0` and do nothing.

### What a load runs

The load lifecycle `0x00582860` creates the slot screen and its panes (message `0xC`, `0x8001`), and
on message `0x12` with flag bit `0x10` of `+0xC4` set runs the post-load sequence: `0x001831A0`,
`0x005843E0` and `0x00182D40` when the controller's byte `+0x598` is clear (that arm also sets
`0x0209AC10` to 1), `0x00394400` when `0x00394520` reports a pending mode, then `0x00584210`, which handles the mode-3 stash and reseeds the gameplay generator from the clock
(see the [save file format page](save-file-format.md)).

Message `0x10` records the load mode: with `0x00394450()` = 3 it calls
`0x00238A30(1)`, else `0x00238A30(0)`, then `0x00285E60(-1)`.

On message 1 `0x00582790` loads the screen's two layouts into `+0x100` and `+0x108` and, unless byte
`+0xC1` is set, the two icon resources (kind 7, ids `0x2C` and `0x2D`) into `+0x110` and `+0x118`,
with `0x00393600(2)` at `+0x120`. `0x00582FC0`, on message `0x12`, releases them, and the buffers at
`+0x588` and `+0x590` are freed after it. `0x00581310(pane)`, run on sub-commands `0x8100`-`0x8102` and
on message `0xF` with value 4, closes the pane and calls `0x00291D40` and `0x002CA110`, then
`0x002CC9C0(0x002CC9B0())` when bit `0x8` of `+0xC4` is set.

## Layouts

### The slot screen

The slot screen is the `0x1C8`-byte widget with procedure `0x0057FE80` that `0x00583040` builds in place (`0x00583205`; The slot list above).

`SlotScreen` (`0x1C8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0057FE80` |
| `+0x0C0` | `void*` | owner | the widget the slot screen opens under, the creation record's first qword (`0x0057FEE1`); the construct message opens the screen under it (`0x00246AD0`, `0x005802F6`) and the screen posts it message 12 with sub-command `0x12` and 4 when it closes (`0x00580790`) |
| `+0x0C8` | `void*` | statusPane | the status pane, the creation record's second qword (`0x0057FEEC`); a cursor move on a status-2 slot fills it from the slot's cached header with `0x0057EFE0` (`0x00580446`, `0x00580E25`) |
| `+0x0D0` | `void*` | saveTransaction | the save transaction widget `0x005819F0` that state 4 opens as a child (`0x00581031`); 0 at construction and when the screen takes the result (`0x0057FEFD`, `0x005804F3`) |
| `+0x0D8` | `void*` | popup | the popup the state machine opens with `0x00583990` (The save and load screen above; `0x00581237`); closed and cleared when the popup's answer arrives (`0x00580383`-`0x005803A8`, `0x0058061B`, `0x00580AC5`-`0x00580AE7`, `0x00580CE5`-`0x00580D09`); 0 at construction (`0x0057FF04`) |
| `+0x0E0` | `u32` | flags | bit `0x1`: the creation record's `+0x14` bit `0x1` (`0x0057FF2D`), with which every row is drawn as status 5 and the list skips the status-2 work (`0x00580073`); bit `0x8`: a save waits for the device check, taken by `0x00580B40`, which then goes to state 4 (`0x00580BCB`-`0x00580BE1`); bit `0x10` is tested by the confirm (`0x00580495`). 0 before the creation record is read (`0x0057FEF6`) |
| `+0x0E4` | `u32` | nextCounter | the next save counter: the active image's `+0x50` at construction (`0x0057FFA5`), raised to the highest header `+0x50` among the listed status-2 slots and slot 0's cache row, each time also stored at `0x02CA99B4` (`0x005800AF`-`0x005800BD`, `0x00580179`-`0x00580187`); state 4 passes it plus 1 to the save transaction (`0x00580FA7`); `0x00580CD0` reads and raises it after a save (`0x00580D35`-`0x00580D92`) |
| `+0x0E8` | `u8` | holdFrames | frames left in state `0xC`, which sets `0x78` (The save and load screen above); counted down by 1 (`0x00580376`) |
| `+0x0E9` | `u8` | state | the screen's state 0-`0xE` (The save and load screen above), set by the state machine `0x00580EB0` (`0x00581246`) and `0xFF` at construction (`0x0057FF0B`); `0x00580EB0` compares the new state with it (`0x00580EE2`); the popup answer handlers dispatch on it (`0x00580369`, `0x005803D5`, `0x0058062B`, `0x00580A86`, `0x00580A9D`) |
| `+0x0EA` | `u8` | loadMode | 0 for the save screen, 1 for the load screen, the creation record's `+0x10` (`0x0057FF16`): it chooses the slots listed (`0x0057FF56`, `0x00580055`), the device check's mode (`0x00580F29`), the row draw mode, and how a confirm (`0x00580541`), a cursor move (`0x0058030F`) and `0x00580B40` (`0x00580B46`) proceed |
| `+0x0EB` | `u8` | slot | the slot the player confirmed (`0x0058053A`); state 4 opens the save transaction with it (The save and load screen above) |
| `+0x0EC` | `u8` | rowCount | the rows listed: 0 at construction (the word store at `0x0057FFAB`), 1 more for each listed slot (`0x005800E1`-`0x005800F0`); `0x00580CD0` adds a row after a save (`0x00580E49`-`0x00580E5E`) |
| `+0x0ED` | `u8` | unusedRows | the listed slots with status 5, "Unused file" (`0x0058002F`); 0 at construction (`0x0057FFAB`) |
| `+0x0EE` | `u8` | usableRows | the listed slots with status 5, status 2, or room reserved (`0x00580035`, `0x0058004F`); 0 at construction (`0x0057FFB3`) |
| `+0x0EF` | `u8[200]` | rowSlot | the slot number of each row: the list build stores each listed slot (`0x005800E8`); in load mode the autosave row is moved down past the newest manual save by swapping neighbours (`0x0058012A`-`0x00580154`); the row draw, the confirm and the cursor move read it (`0x00580437`, `0x0058050C`, `0x00580C5E`, `0x00580D6F`) |
| `+0x1B7` | `u8` | pad1B7 | read and written by no function; nothing fixes its width |
| `+0x1B8` | `void*` | list | the slot list widget, layout item 0's `+0x18` (`0x0057FF9A`); the construct message sets it up and starts its cursor (`0x0058018D`-`0x005801D9`); `0x00580B40` (`0x00580C24`) and `0x00580CD0` (`0x00580D2B`) read it |
| `+0x1C0` | `void*` | headerCache | the header cache, the first `0xA0` bytes of each slot's image at slot x `0xA0`, the creation record's `+0x18` (`0x0057FF20`); read for the counters `+0x50` and the row draw (`0x00580088`, `0x00580156`, `0x0058016A`, `0x0058045A`, `0x00580C72`, `0x00580DB0`, `0x00580E1E`, `0x00580FF8`) |

### The storage queue object

The queue is the `0x720`-byte widget kept at `0x02CA99C0` with procedure `0x005823B0` (The storage queue above).

`StorageQueue` (`0x720` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x005823B0` |
| `+0x0C0` | `void*` | callback | the completion callback a kind-1 packet installs (`0x005820A5`); the dequeue `0x00582240` calls it with the finished packet's kind, its result and `+0xC8` (`0x00582373`-`0x0058238E`); 0 at construction (`0x005824A9`) |
| `+0x0C8` | `u32` | callbackArg | the callback's argument, copied from the kind-1 packet with the callback (`0x005820B2`) and passed to it as its third argument (`0x0058237F`) |
| `+0x0CC` | `u8` | busy | 1 while a front packet is running: the enqueue sets it when the start `0x00582040` answers 0, the packet still running (`0x005826BA`), and starts nothing new while it is set (`0x00582698`); the dequeue clears it when the queue empties (`0x00582280`); the tick (message 2) completes and starts packets while it is set (`0x00582443`-`0x0058248A`); the device check `0x0057EA40` (`0x0057EA9F`), the poll arm `0x0057EC60` (`0x0057ECC0`) and the disarm `0x0057ED40` (`0x0057ED94`) clear it with the queue; 0 at construction (`0x005824B0`) |
| `+0x0CD` | `u8` | pad0CD | read and written by no function; nothing fixes its width |
| `+0x0CE` | `u8` | pad0CE | read and written by no function; nothing fixes its width |
| `+0x0CF` | `u8` | pad0CF | read and written by no function; nothing fixes its width |
| `+0x0D0` | `u32` | spaceNeeded | the space a save needs, 102,400 bytes from `0x003936B0`, stored by the first tick (`0x0058243D`); the popup opener `0x00583990` rounds it up to KB for the popup text (`0x005839C8`) |
| `+0x0D4` | `u32` | spaceKnown | bit `0x1` set once the first tick has measured `+0xD0` (`0x00582436`), which it does only while the bit is clear (`0x0058240A`); the load lifecycle `0x00582860` waits for it (`0x00582A6A`); 0 at construction (`0x005824B7`) |
| `+0x0D8` | `u8[704]` | queue | the eight `0x58`-byte packets of the queue (The storage queue above) |
| `+0x398` | `u8` | count | the packets queued, 0-8: the enqueue refuses a ninth (`0x0058254E`-`0x0058255D`), copies the packet to entry count (`0x00582570`-`0x005825AD`) and adds 1 (`0x00582692`); the dequeue takes 1 off and moves the rest down (`0x0058224F`-`0x005822D9`); the device check, the poll arm and the disarm empty the queue by setting it to 0 or keep the started packet with 1 (`0x0057EA72`-`0x0057EA98`, `0x0057EC8F`-`0x0057ECB9`, `0x0057ED61`-`0x0057ED8D`); 0 at construction (`0x005824BD`) |
| `+0x399` | `u8` | pad399 | read and written by no function; nothing fixes its width |
| `+0x39A` | `u8` | device | the device byte a kind-2 packet stores (`0x005820FA`), `0xFF` at construction (`0x005824C4`); read by the device-check result `0x0057E950` (`0x0057E9F0`), the presence poll's result `0x0057EBB0` (`0x0057EC0F`), `0x0057F630` (`0x0057F654`), `0x0057F6B0` (`0x0057F78E`) and the save transaction's completion `0x00581B70` (`0x00581D04`) |
| `+0x39B` | `u8` | descriptorNext | the next free entry of the descriptor ring at `+0x3A0`: a kind-8 packet's descriptors are copied from it on (`0x00582608`-`0x0058264C`), the packet's `+0x48` is pointed at the first (`0x0058265F`-`0x0058267F`) and it advances by their count (`0x0058268C`); it restarts at 0 when the count would pass 16 (`0x005825D2`-`0x005825E4`); 0 at construction (the word store at `0x005824C4`) |
| `+0x39C` | `u8[4]` | pad39C | read and written by no function; nothing fixes its width |
| `+0x3A0` | `u8[896]` | descriptors | the ring of sixteen `0x38`-byte file descriptors that kind-8 packets (the save transaction) carry, copied in by the enqueue (`0x00582617`-`0x0058264C`); the handler `0x003BB9B0` reads them through the packet's `+0x48` |

### The progress gauge

The gauge is the `0x110`-byte widget kept at `0x02CA99C8` with procedure `0x00581490` that counts a save, a load or a
format in tenths of the full count.

`ProgressGauge` (`0x110` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00581490` |
| `+0x0C0` | `void*` | owner | the widget that made the gauge, the creation record's first qword (`0x005816AC`-`0x005816B7`); the gauge opens under it (`0x00246AD0`, `0x005817A9`) and posts it message 12 with sub-command `0xF` on message 15 (`0x005814F4`) and `0x12` on message 18 (`0x005814C9`) |
| `+0x0C8` | `u32` | flags | bit `0x1`: the count has been sent to its full value, set by `0x005813E0` (`0x00581462`, `0x00581480`) and cleared by it and by `0x00581860` before a new target (`0x00581408`, `0x005818A7`); while it is set the tick does not creep past the target (`0x005815DB`). Bit `0x2`: the shown value is creeping past the target one unit a tick (`0x005815E9`-`0x0058161D`). Bit `0x4`: the count is stopped, set by `0x0057F360` (`0x0057F479`), `0x00580840` (`0x0058091A`, `0x00580A56`) and the save transaction's completion `0x00581B70` (`0x00581D3A`), and the tick does nothing then (`0x00581529`). 0 at construction and on reset (`0x0058171A`, `0x005812E2`, `0x0058180F`) |
| `+0x0CC` | `u32` | soundOn | bit `0x1` set while the working sound runs: `0x005819A0` plays sound `0x42` unless its argument is 1, keeps its handle at `+0xE8` and sets the bit (`0x005819B9`-`0x005819D7`); `0x00580EB0` sets it for the save, load and format states (`0x00580FC6`, `0x0058107E`, `0x0058118A`); `0x00581350` stops the sound (`0x0024A1A0`) and clears the bit (`0x00581368`-`0x0058138B`). 0 at construction (`0x0058174F`) |
| `+0x0D0` | `u8` | operation | the operation the gauge counts: 2 a save (`0x00580FD3`), 3 a load (`0x0058108B`), 4 a format (`0x00581197`), or `0x005819A0`'s argument (`0x005819DE`); `0xFF` at construction (`0x00581748`). On success `0x00581350` plays sound `0x27` for 0, 1 and 4 and `0x43` for 2 and 3 (`0x00581396`-`0x005813CD`) |
| `+0x0D1` | `u8[3]` | pad0D1 | read and written by no function; nothing fixes its width |
| `+0x0D4` | `u32` | full | the full count in tenths, 10 x `0x005817D0`'s first argument (`0x00581833`), `0xFFFF` at construction and reset (`0x00581708`, `0x005812D0`, `0x005817FD`); `0x005813E0` sends the count to it (`0x005813F6`) and `0x00581860` caps its target at it (`0x00581899`); the number is drawn in colour `0xD2` once the shown value reaches it (`0x00581966`) |
| `+0x0D8` | `u32` | shown | the value on the number display: `0x00581930` stores the value it draws (`0x0058195B`); the high half of the qword store of `0xFFFF` clears it (`0x005812D0`, `0x005817FD`); `0x005813E0` and `0x00581860` start their animations from it (`0x005813FC`, `0x0058188B`) |
| `+0x0DC` | `u32` | target | the count's target in tenths: `0x005813E0` sets the full value (`0x00581415`), `0x00581860` 10 x its first argument capped at the full value, or the full value for -1 (`0x005818AE`); the tick creeps the shown value past it while it is below (`0x005815DF`); 0 on reset (`0x005812DB`, `0x00581808`) |
| `+0x0E0` | `u32` | softCap | 10 x `0x005817D0`'s second argument (`0x00581848`); while it is not 0 and the value passes it, the tick holds the value at it and raises it by 1 a tick up to one below the full value (`0x00581623`-`0x00581642`); 0 on reset (the qword stores at `0x005812DB`, `0x00581808`) |
| `+0x0E4` | `u32` | creep | how far past the target the shown value has crept: 1 when creeping starts (`0x00581600`), then 1 more each tick (`0x005815ED`) |
| `+0x0E8` | `i32` | soundHandle | the handle of the working sound `0x42` (`0x005819D1`) or of `0x00580EB0`'s sound for the save, load and format states (`0x00580FCD`, `0x00581085`, `0x00581191`); `0x00581350` stops it and sets -1 (`0x00581371`, `0x00581381`); -1 at construction (`0x00581735`) |
| `+0x0EC` | `u8[4]` | pad0EC | read and written by no function; nothing fixes its width |
| `+0x0F0` | `void*` | numberNode | the gauge's number display, layout entry 1 (`0x00394690`, `0x005816CA`): the construct message pads its `+0x48`/`+0x4A` by `0x200` (`0x005816D6`-`0x005816FB`), `0x00581930` writes the value (`0x00225580`) and its colour (`0x0029F480`) into it (`0x00581952`, `0x0058197C`), the reset clears it (`0x005812C2`, `0x005817EF`, `0x00581821`) |
| `+0x0F8` | `u32` | animStep | the steps taken of the animation: 0 when one starts (`0x0058144D`, `0x005818F2`), 1 more each tick (`0x00581555`) |
| `+0x0FC` | `u32` | animSteps | the animation's length in ticks: 4 for `0x005813E0`'s run to the full value (`0x0058145C`), or the steps `0x00581860` works out (`0x00581902`), at least 1; 0 when the animation ends (`0x005815C5`), when there is nothing to animate (`0x0058147A`, `0x00581918`) and on reset (`0x005812F4`, `0x0058182D`, `0x00581742`). The tick animates only while it is not 0 (`0x00581536`) |
| `+0x100` | `u32` | animFrom | the value the animation starts from, the shown value (`0x00581422`, `0x005818C6`); read by the tick (`0x00581561`) |
| `+0x104` | `u32` | animSpan | the full value less the start (`0x0058143E`, `0x005818DE`); the tick adds animSpan x animStep / animSteps to the start (`0x00581571`-`0x005815A9`), and the whole span at the end (`0x005815B1`) |
| `+0x108` | `u32` | animValue | the value the animation has reached, which the tick shows (`0x0058142B`, `0x005818CF`, `0x00581567`, `0x005815A9`, `0x005815B9`) |
| `+0x10C` | `f32` | animFraction | animStep / animSteps (`0x00581599`), 1.0 at the end (`0x005815CB`), 0 when an animation starts (`0x00581453`, `0x005818F8`); read by no instruction |

### The card-presence poll

The poll is the `0xD0`-byte widget kept at `0x02CA99D8` with procedure `0x0057EB30`.

`CardPresencePoll` (`0xD0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0057EB30` |
| `+0xC0` | `u32` | flags | bit `0x1`: the second argument of the poll arm `0x0057EC60` (`0x0057ECC7`-`0x0057ECD1`); bit `0x2`: a presence poll is queued, set by `0x0057EC60` (`0x0057ED13`) and by the device check `0x0057EA40` after it queues its packets (`0x0057EAFE`); while bit `0x2` is set each of the three, `0x0057EA40` (`0x0057EA5D`), `0x0057EC60` (`0x0057EC7A`) and the disarm `0x0057ED40` (`0x0057ED4C`), first empties the storage queue, or marks its started front packet to skip its callback. The disarm clears bits `0x1` and `0x2` (`0x0057ED85`, `0x0057ED9B`); the construct message sets 0 (`0x0057EB74`) |
| `+0xC4` | `u8[4]` | pad0C4 | read and written by no function; nothing fixes its width |
| `+0xC8` | `void*` | controller | the first argument of the poll arm `0x0057EC60`, the save and load screen that armed it (`0x0057ECD7`); 0 at construction (`0x0057EB6A`) |

### The backdrop

The backdrop is the `0xD0`-byte widget kept at `0x02CA99E0` with procedure `0x0057F7D0` that opens screen layer 1 behind
the save and load popups.

`SaveScreenBackdrop` (`0xD0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0057F7D0` |
| `+0xC0` | `void*` | layer | the screen layer 1 the construct message opens with the descriptor `0x00D23E98` (`0x002CCCA0`, `0x0057F893`) |
| `+0xC8` | `u32` | closing | bit `0x1` set once the layer has been closed (`0x0057F83E`); 0 at construction (the qword store at `0x0057F8A4`) |
| `+0xCC` | `i32` | countdown | steps left before the backdrop goes: the save and load code sets 4 when its popup sequence ends (`0x0058039B`, `0x00580611` in `0x0057FE80`; `0x00580890`, `0x005809F4` in `0x00580840`; `0x00580ADD` in `0x00580A80`; `0x00580CFD` in `0x00580CD0`; `0x00582D65` in `0x00582860`; `0x0058312E` in `0x00583040`); the popup opener `0x00583990` sets 0 (`0x00583BA2`) and the construct message clears it (`0x0057F8A4`). Each step on which `0x001EDEC0`(`+0xB4`) answers non-zero lowers it; at 0 the layer closes (`0x002CCB10`), bit `0x1` of `+0xC8` is set and 14 more steps run (`0x0057F81E`-`0x0057F847`), after which the widget releases itself (`0x0057F85E`-`0x0057F869`) |

### Slot and list records

The slot status table, the save list rows and the disable-autosave rows are laid out as follows.

`SlotStatusEntry` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | status | 1 no file yet, 2 header read in full, 3 no file and no room, 4 file shorter than the header or failed to load, 5 no file with room reserved (`0x003BA990`, `0x00580840`) |
| `+0x04` | `i32` | room | 1 when the slot's space requirement was reserved (`0x003BA990`, `0x003BA720`) |

The table holds 200 entries at `0x02B407C0`; slot `n` is entry `n` (`0x003BB3E0`, `0x003BB600`).

`SaveListRow` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[16]` | pad10 | not written by `0x008621E0` |
| `+0x10` | `i32` | size | the file's length from ftell (`0x008621E0`) |
| `+0x14` | `u8[12]` | pad14 | not written by `0x008621E0` |
| `+0x20` | `char[32]` | name | the file name, prefix plus three digits (`0x008621E0`) |

`DisableAutosaveRow` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | field | the destination field id (`0x001C1720`) |
| `+0x04` | `i32` | story | 0 any story counter; otherwise the counter it must equal; -2 matches only while battle-state bit `0x1000` is set |
| `+0x08` | `i32` | entrance | 0 any entrance; otherwise the entrance it must equal |
| `+0x0C` | `i32` | variable | 0 no variable; otherwise the row also matches while `0x002EF390`(variable) is true |

## Shipped data

Measured from `gamedata/disableautosavelist/disableautosavelist.txt` in the archive:

| Fact | Value |
|---|---|
| File size | 673 bytes, 73 lines, each ending in CR LF |
| Rows | 73, naming 72 distinct field ids (1124 appears twice) |
| Field only, always excluded | 21 rows: fields 12, 13, 50, 769, 854, 858, 860, 862, 864, 866, 867, 868, 869, 910, 912, 914, 918, 922, 924, 1113, 1147 |
| Field and entrance | 1 row: field 1140, entrance 9 |
| Field and story counter | 28 rows, story values 16 to 6750 (for example `48,301`) |
| Story -2 (battle-state bit `0x1000`) | 10 rows: fields 1155 to 1299 in steps of 16 |
| Story -1 with a variable | 13 rows, variables 15 to 56; two of them (field 1124) also name entrance 5 or 4 |
| Empty second column | 1 row, `1113,,5303`, which parses as field 1113 alone |

[`saving-and-loading-disable-autosave-rows.tsv`](saving-and-loading-disable-autosave-rows.tsv) lists all 73 rows in file order: the line as shipped, its four
columns, the field's zone, map name and region, the story stage a story value names, the script variable's name
and the boss whose fight it tracks, and the rule in words. What the rows show:

- The ten story -2 rows are the Trial Mode stages 1, 11, 21 and so on to 91 (fields 1155 to 1299, `tri_a01` to
  `tri_s01`): the story value -2 stands for battle-state bit `0x1000` (`0x00236760`), so entering those stages in
  Trial Mode does not autosave.
- Each of the 13 variable rows names a boss flag (`g_btl_...`). The zone scripts set it to 1 when the fight is
  waiting and to 2 once it is won, so the area change skips the autosave only while that boss is still to be
  fought: for example field 441 (Cloister of Solace) while Humbaba Mistant waits (variable 15, image byte
  `+0xC0F`).
- Field 769 (`vic_a04`) is listed, but the US script table holds no script for that field, so no area change
  reaches it and its row never matches; `vic_a04.ebp` still ships in the archive.

### Columns of saving-and-loading-disable-autosave-rows.tsv

| Column | Holds |
|---|---|
| `variable_name` | the name of the script global the row's `variable` names, the global at payload offset `0xA00` plus `variable` ([Script variables](../Scripts-And-Script-Commands/script-variables.md)): `g_btl_` and the boss's name in Japanese, on the 13 rows with a variable; empty on the other 60, whose `variable` is 0 |
| `entered` | `yes` on 72 rows, where the `us` script array names a script for the field, so an area change can reach it; `no: the us script array names no script for it` on line 18, field 769 (`vic_a04`) |

## Operations

| Function | Role |
|---|---|
| `0x00580EB0` | the save and load screen's state machine |
| `0x005819F0` | opens the save transaction; `0x00581DA0` runs a step; `0x00581B70` completes it |
| `0x005837F0` | slot, icon and static file names |
| `0x00582730`, `0x005826D0` | queue a write of `size` bytes, queue a delete |
| `0x00582040` | starts the queue's front packet |
| `0x003BB920`, `0x003BB9B0`, `0x003BB2F0` | the write, image-write and delete starters |
| `0x008666B0`, `0x00866A00`, `0x00866AD0`, `0x00866200` | open, read, write, close on the byte vector |
| `0x00862590` | the read wrapper that turns the boolean into a byte count |
| `0x00862130` | delete a file if it exists |
| `0x0057E4D0`, `0x0057E310` | the autosave widget and its writer |
| `0x00582860` | the load lifecycle |
| `0x0057FE80` | the slot screen: builds the slot list |
| `0x0057F8C0`, `0x0057FA30` | draw a slot row, the status line |
| `0x0057EFE0` | fill the status pane from a cached header |
| `0x00580CD0`, `0x00580840` | the save result, the load and format result |
| `0x00583CB0`, `0x00583C00` | back up, restore the image's first `0xE240` bytes |
| `0x0057ED40` | disarm the card-presence poll |
| `0x003BB3E0`, `0x003BB600` | read, replace a slot status entry |
| `0x003BB790`, `0x00862600` | the worker's per-frame status poll, the status getter |
| `0x0057F6B0`, `0x003BA990` | queue the slot scan, run it |
| `0x008621E0` | probe one file, or list `prefix000` to `prefix199` |
| `0x003BA320` | slot number from a file name |
| `0x003936B0`, `0x00393600`, `0x003BB630`, `0x003BA3E0` | the space requirement |
| `0x00393630` | the `FFXII_*` pattern |
| `0x00394600`, `0x00393EA0`, `0x003BB320`, `0x003BA680` | the save-data check |
| `0x008625D0`, `0x00862620` | the seek and write wrappers |
| `0x001C1720` | decide whether an area change autosaves |
| `0x001C0F20` | parse `disableAutosaveList.txt` |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02CA99B8` | `void*` | the open save/load controller | `0x00582860` |
| `0x02CA99C0` | `void*` | the storage queue | the queue owner |
| `0x02CA99C8` | `void*` | the gauge widget | the controller |
| `0x02CA99B0` | `i32` | a save transaction is open | `0x005819F0` |
| `0x02CA99B4` | `u32` | the save counter written at header `+0x50` | `0x0057E310` |
| `0x02CA99E8` | `i32` | an autosave write is busy | `0x0057E310`, `0x0057E4D0` |
| `0x02B40E10` | `i32` | the storage machine is busy | `0x003BB920`, `0x003BB9B0`, `0x003BB2F0` |
| `0x02B40E1C` | `i32` | the worker command | the three starters |
| `0x01F44D40` / `0x01F44D48` / `0x01F44D50` | `void*` | the file vector's begin, end and capacity | `0x008666B0`, `0x00866AD0`, `0x00866200` |
| `0x02B407C0` | 200 x 8 bytes | the slot status table | `0x003BA990`, `0x003BA720`, `0x003BB600`, `0x003BB6A0` |
| `0x02B40E18` | `i32` | the last command's result | the command handlers |
| `0x02EAF8E0` | `i32` | the status of the last file call | `0x008621E0`, `0x00862590`, `0x00862620`, `0x008625D0`, `0x00862490` |
| `0x02B4054C` | `i32` | the free space the slot scan draws on | `0x003BA990`, `0x003BA720` |
| `0x01EFAC10` | `u8` | the save-data check: 3 in the image, before the first check; 2 running, 1 a save exists, 0 no save file | `0x00393EA0` |
| `0x01F81260` | `void*` | the SaveloadManager, holding the autosave exclusion rows at `+0x50` | `0x001C18A0` |

The device-check pane:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA99D0` | `void*` | 0 (zero-filled tail) | the device-check pane, the `0xD0`-byte widget with procedure `0x0057E8D0` that the save and load screen `0x00582860` builds while it is 0; the device check `0x0057EA40` stores the controller at its `+0xC8` and bit `0x1` of its second argument, the save-or-load mode, in bit `0x2` of `+0xC0` | `0x0057E8D0`: itself on message 1 (`0x0057E903`), 0 on message 18 (`0x0057E8F4`) | `0x00582860`, which builds it only while it is 0 (`0x00582A90`-`0x00582AA9`) and closes it with `0x00244F00` on leaving (`0x00582B7C`, `0x00582BEF`, `0x00582C38`); `0x0057EA40` (`0x0057EAA6`) |

No other instruction reaches `0x02CA99D0`: no other RIP-relative, image-base-relative or 32-bit offset reference names
it.

## Modding notes

- A tool that writes a slot file must also write the zeroed-header then stamped-header sequence
  only if it wants the game's own semantics; the game never reads the companion files `icon.sys`
  and `static.ico`, it only queues deletes for them, which reach no file (The storage queue).
- The autosave always targets slot 0, which the save list never offers for a manual save (save mode
  lists slots 1-199); a slot 0 file copied in from outside the game is overwritten at the next area change that autosaves.
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
- [`storage-byte-stream-vector-01f44d40-accesses.tsv`](storage-byte-stream-vector-01f44d40-accesses.tsv): every
  access to the file worker's byte vector `0x01F44D40` (its begin, end and capacity pointers) (23 rows).
