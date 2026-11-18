[Home](../../README.md) / [Saving, loading and settings](README.md) / Saving and loading

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Saving and loading: the save slots, their files, and the three parts of a save and a load | system | Saving, loading and settings | Saving and loading | How a manual save and a load are carried out: the slot files and their names, the save and load screen's state machine and its popups, the transaction that zeroes the image header on disk, runs three deletes that name the save directory itself and so remove no file, writes the whole image and then stamps the header, the storage queue and the worker commands behind it, the stream primitives that make a short read report zero, the autosave the game writes to slot 0 when an area changes, and the lifecycle that normalises a loaded image. It also covers the slot list and its status table, the slot scan that reads every slot's header, the save-data check the title screen runs, and the shipped list of area changes that do not autosave. | 0x0057E310, 0x00582860, 0x003BA990, 0x02B407C0 |

## What the player sees

Saving at a save crystal opens the slot list. Picking a slot asks for confirmation when the slot is
empty or already holds a save, shows "Saving" while the file is written, and reports completion or
failure. Loading from the title screen reads the slot's file, shows "Loading", and continues into
the saved area with the clock, the gil and the party as they were saved. The game also writes a
hidden autosave to slot 0 whenever an area changes.

A save that was interrupted part-way through is left on disk with its first eight bytes zeroed: the
checksum and the mark that is 1 only on a finished save. The slot list does not test that mark: a slot
whose first `0xA0` bytes read in full is drawn from those bytes, and only a short read shows "Corrupt
save data." ([the slot scan](saving-and-loading-transaction.md#the-slot-scan)).

Loading does not test the mark or the checksum either
([what a load checks](save-file-format.md#what-a-load-checks)), so such a save loads. The zeroing write
rewrites the file at its full length ([the file layer](saving-and-loading-transaction.md#the-file-layer)), so a save stopped before the
whole image was written (state 7 of [the save transaction](saving-and-loading-transaction.md#the-save-transaction)) loads as the save it
was replacing, and one stopped after that write loads as the new save.

The slot list shows each used slot's party, gil, Esper row and clan rank, and marks the others
"Unused file." or "Corrupt save data."; the load list puts the autosave next to the newest manual
save. The title screen asks whether any save file exists before it offers loading. A shipped list
names the area changes that do not autosave.

A save writes the game's live save image, the block that holds the party, the story flags, the gil and the clock
during play, to the slot's file, and a load reads that file back into the same block. The slot list reads only the
first part of each slot's image, its header, which carries the party, gil, Esper and clan rank it shows.

## How it works

The mechanism is explained on three pages, one for each part of the operation:

- [Save and load screen](saving-and-loading-screen.md): the screen's fifteen states and their popups, the slot list
  with its rows and status pane, what the screen does after a save or a load, and the widgets the screen keeps.
- [Save transaction](saving-and-loading-transaction.md): the six steps that write a slot file, the storage queue and
  the worker behind it, the slot scan, the space a save needs, the title screen's save-data check and the file layer.
- [Area-change autosave](saving-and-loading-autosave.md): the autosave written to slot 0 when an area changes, which
  area changes skip it and the shipped list that names them, and what a load runs.

### The files

Each slot is one file named `FFXII_` plus the slot number as three digits (`0x005837F0`, kind 1,
through `0x003935C0` and `sprintf("%s%03d")`) in the save directory
(see the [save file format page](save-file-format.md)). The same formatter names `icon.sys`
(kind 0) and `static.ico` (kinds 2-4), the two companion files the save transaction queues for deletion
(a delete that reaches no file, see [the storage queue](saving-and-loading-transaction.md#the-storage-queue)); it
returns the name in the controller record at `+0x128` and null when no controller is open
(`0x02CA99B8` = 0).

`0x003935C0(buffer, size)` copies the six characters `FFXII_` from `0x00D113D4` with `0x008C2F70(buffer, 0x00D113D4, 6)`, the
import `strncpy`, stores 0 at the byte `+0x6` to end the text and returns the buffer; for a size of 6 or less, an
unsigned compare, it writes nothing and returns the empty string at `0x01CEB638`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003935C9`-`0x003935F1` |

</details>

## Operations

| Function | Role |
|---|---|
| `0x005837F0` | slot, icon and static file names |

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02CA99B8` | `void*` | the open save/load controller | `0x00582860` |
| `0x02CA99B4` | `u32` | the save counter written at header `+0x50` | `0x0057E310` |
| `0x02B407C0` | 200 x 8 bytes | the slot status table | `0x003BA990`, `0x003BA720`, `0x003BB600`, `0x003BB6A0` |

</details>

## Modding notes

- The autosave always targets slot 0, which the save list never offers for a manual save (save mode
  lists slots 1-199); a slot 0 file copied in from outside the game is overwritten at the next area change that autosaves.

## Related

- [Save and load screen: the screen's states and popups, the slot list and its status pane, what follows a save or a load, and the screen's widgets](saving-and-loading-screen.md)
- [Save transaction: its steps, the storage queue and its worker, the slot scan, the space requirement, the save-data check and the file layer](saving-and-loading-transaction.md)
- [Area-change autosave: when it runs, which area changes skip it, the shipped list of those area changes, and what a load runs](saving-and-loading-autosave.md)
- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md)
- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](../World-Areas-And-Travel/zone-changes-and-mapjump.md)
- [`storage-byte-stream-vector-01f44d40-accesses.tsv`](storage-byte-stream-vector-01f44d40-accesses.tsv): every
  access to the file worker's byte vector `0x01F44D40` (its begin, end and capacity pointers) (23 rows).

---

[Loading a save →](loading-a-save.md)
