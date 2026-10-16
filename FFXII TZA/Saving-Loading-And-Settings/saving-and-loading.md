---
title: "Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs"
kind: "system"
category: "Saving, loading and settings"
summary: "How a manual save and a load are carried out: the slot files and their names, the save and load screen's state machine and its popups, the transaction that zeroes the image header on disk, deletes the slot's old files, writes the whole image and then stamps the header, the storage queue and the worker commands behind it, the stream primitives that make a short read report zero, the autosave the game writes to slot 0 when an area changes, and the lifecycle that normalises a loaded image."
addresses: ["00580EB0", "005819F0", "00581DA0", "00581B70", "00582040", "003BB920", "003BB9B0", "003BB2F0", "00866A00", "00862590", "00866AD0", "0057E4D0", "0057E310", "00582860", "00862130"]
---

# Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs

## What the player sees

Saving at a save crystal opens the slot list. Picking a slot asks for confirmation when the slot is
empty or already holds a save, shows "Saving" while the file is written, and reports completion or
failure. Loading from the title screen reads the slot's file, shows "Loading", and continues into
the saved area with the clock, the gil and the party as they were saved. The game also writes a
hidden autosave to slot 0 whenever an area changes. A save that was interrupted part-way through
is left on disk with its header zeroed, so the slot shows it as unusable rather than as an older
save.

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
  file is touched until close.
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

### What a load runs

The load lifecycle `00582860` creates the slot screen and its panes (message `0xC`, `0x8001`), and
on message `0x12` with flag bit 4 of `+0xC4` set runs the post-load sequence: `001831A0`,
`005843E0` and `00182D40` when the controller's byte `+0x598` is clear (that arm also sets
`0209AC10` to 1), `00394400` when `00394520` reports a pending mode, then `00584210`, which handles the mode-3 stash and reseeds the gameplay generator from the clock
(see the format page). Message `0x10` records the load mode: with `00394450()` = 3 it calls
`00238A30(1)`, else `00238A30(0)`, then `00285E60(-1)`.

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

## Modding notes

- A tool that writes a slot file must also write the zeroed-header then stamped-header sequence
  only if it wants the game's own semantics; the game never reads the companion files `icon.sys`
  and `static.ico`, it only deletes them.
- The autosave always targets slot 0; a manual save to slot 0 is overwritten at the next area
  change.
- A read that falls short reports 0 and leaves the destination partly overwritten; a reimplementation
  must copy before it compares, in that order.

## Related

- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md)
- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
