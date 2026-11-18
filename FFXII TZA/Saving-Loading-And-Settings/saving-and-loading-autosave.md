[Home](../../README.md) / [Saving, loading and settings](README.md) / Area-change autosave

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Area-change autosave: when it runs, which area changes skip it, the shipped list of those area changes, and what a load runs | system | Saving, loading and settings | Saving and loading | How the game writes its hidden autosave to slot 0 when an area changes, how it decides which area changes skip it from the shipped disableAutosaveList.txt and what that list holds, and the calls a load runs once the slot's file has been read. | 0x003BB9B0, 0x0057E4D0, 0x0057E310, 0x00582860, 0x001C1720 |

## What the player sees

The game writes a hidden autosave to slot 0 whenever an area changes, except for the area changes a shipped list
names. Loading continues into the saved area with the clock, the gil and the party as they were saved.

## How it works

### The autosave on an area change

`0x0057E4D0`, the autosave widget, runs `0x0057E310` on construction (message 1) and again on
sub-commands `0x8100`-`0x8102`. `0x0057E310` copies the capture image to the write buffer, stores the
CRC, the 1 and the save counter in its header, names the file for slot 0 (`0x00584610` with slot 0,
`sprintf("%s%03d")`), hands the descriptor to `0x003BB9B0` and sets the busy flag `0x02CA99E8`.

Before `0x0057E310`, message 1 stores 0 at `+0x98` with 512 and 448 at the words `+0x9C` and `+0x9E` (the dwords at
`0x01E0C1D8` and `0x01E0C1DC`, written only for a non-null widget), clears bit `0x800` of `+0x40`, and stores 50 at
the word `+0x44` and 0 at `+0xC8`¹. After it, it calls `0x00244960([0x0208EA50], widget)` and
`0x00247870(widget, 1)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057E5A6`-`0x0057E5E0` |
| ² | `0x0057E5F5`, `0x0057E602` |

</details>

The sub-commands arrive as message `0xC`¹; after `0x0057E310` the widget stores 0 in its popup
pointer `+0xC0`², and other sub-commands do nothing. Message 4 returns 0, and messages other than 1,
2, 4 and `0xC` go to `0x005C5230`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057E4F2` |
| ² | `0x0057E522` |
| ³ | `0x0057E4FF` |

</details>

`0x0057E310(widget)` copies `0xACD` blocks of `0x80` bytes and 16 more¹. It takes the CRC
over the active buffer's `+0x08` for `0xE1F8` bytes² and raises the save counter `0x02CA99B4`
only while it is below `0xFFFFFFFF`³. The descriptor it hands over is the 56 bytes at widget
`+0xD0`: the name from `0x00584610(name, 0x40, 1, 0)` at `+0x00`, the write buffer at `+0x28` and the size
`0x56690` at `+0x30`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057E347`-`0x0057E3A6` |
| ² | `0x0057E3A9`-`0x0057E3BF` |
| ³ | `0x0057E3CE`-`0x0057E3DD` |
| ⁴ | `0x0057E3E0`-`0x0057E42F` |

</details>

It also builds `FFXII_000` with `0x003935C0` and `sprintf("%s%03d")` on its stack¹, calls
`0x0036FD80(1)`², and then calls `0x003BB9B0` with that text, the descriptor and a count of 1³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057E43A`-`0x0057E472` |
| ² | `0x0057E479` |
| ³ | `0x0057E47E`-`0x0057E490` |

</details>

On message 2, once the machine is idle (`0x003BB430()` = 0), the widget looks at the result
`0x003BB420()`:

- zero: the widget completes (`+0xC8` = 1, `0x02CA99E8` = 0, `0x0036FD80(0)`, `0x00245020`);
- non-zero with no popup open (`+0xC0` = 0): it opens popup 1 through `0x00583FD0(1, widget)`, text
  2065, "Insufficient disk space. In order to create a save game, at least ... KB of free space is
  required."

Nothing is shown while the write runs.

While the machine is busy, message 2 returns 0¹. With a non-zero result and a popup already open it
also returns 0². Before it opens the popup it stores 1 in the busy flag `0x02CA99E8`³; it
gives `0x00583FD0` the third argument 1⁴ and keeps the popup at `+0xC0`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057E536` |
| ² | `0x0057E54D` |
| ³ | `0x0057E559` |
| ⁴ | `0x0057E553` |
| ⁵ | `0x0057E56E` |

</details>

### Which area changes autosave

The zone-change stager `0x003145E0` captures the autosave only when `0x0020E500(field, story counter,
entrance)` returns non-zero (`0x00314774`; the story counter is `0x00265270()`). `0x0020E500` passes the
SaveloadManager¹ to `0x001C1720(manager, field, story, entrance)`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01F81260`, `0x001C18E0` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It returns 0 when the manager's dword `+0x0C` is not 0 (the constructor `0x001C0E20` clears it) or the field id is not positive. |   |
| 2 | When bit `0x1000` of the party block's flag dword is set, the story value is replaced by -2. | `0x00236760` |
| 3 | It walks the rows of the vector at `+0x50` (16 bytes each, see [the slot and list records](saving-and-loading-screen.md#slot-and-list-records)). A row matches when its field equals the field, its entrance is 0 or equal, and its story value is 0, equal, or its variable is non-zero with `0x002EF390(variable)` true (the active image byte `+0xC00 + variable` is 1). |   |
| 4 | A matching row returns 0, so no autosave; no match returns 1. |   |

The constructor `0x001C0E20` stores the class `0x008F9B80` at `+0x00` and zeroes `+0x08`-`+0x0F`, `+0x14`-`+0x33`,
`+0x38`-`+0x42` and `+0x44`-`+0x4B`¹. Of the `0xA78` bytes `0x001C18A0` allocates for it², `+0x10`-`+0x13`, `+0x34`-`+0x37`, `+0x43`, `+0x4C`-`+0x4F`, `+0x70`-`+0x56F` and
`+0xA71`-`+0xA77` keep what they held.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001C0E29`-`0x001C0E5D` |
| ² | `0x001C18B7`-`0x001C18CE` |

</details>

It sets up the row vector: it zeroes the three qwords at `+0x50` and stores the allocator class `0x00902720` at `+0x68`
through `0x001EDF00(+0x68, 0x008C5F58)`, which does not read the text `EASTL vector` it is passed¹.
It clears the byte `+0xA70`, zeroes the `0x500` bytes from `+0x570` with `0x00861EC0(+0x570, 0, 0x500)` (`memset`) and
returns the manager².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001EDF00`-`0x001EDF0D` |
| ² | `0x001C0E61`-`0x001C0E94` |

</details>

The rows come from `./GameData/disableAutosaveList/disableAutosaveList.txt`¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008F9AC8` |

</details>

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
`0x0209AC10` to 1), `0x00394400` when `0x00394520` returns 1, then `0x00584210`, which handles the mode-3 stash and
reseeds the gameplay generator from the clock (see the [save file format page](save-file-format.md)).

`0x00394520` returns 1 while the qword `0x02AEE4C0`, the title asset's pointer, is non-zero¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00394522`-`0x00394529` |

</details>

Message `0xC` with sub-command `0x10` records the load mode: it sets bit `0x10` of `+0xC4`¹
and, with `0x00394450()` = 3, calls `0x00238A30(1)`, else `0x00238A30(0)`, then `0x00285E60(-1)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00582CB3` |
| ² | `0x00582CBA`-`0x00582CE6` |

</details>

On message 1 `0x00582790` loads the screen's two layouts into `+0x100` and `+0x108` and, unless byte
`+0xC1` is set, the two icon resources (kind 7, ids `0x2C` and `0x2D`) into `+0x110` and `+0x118`,
with `0x00393600(2)` at `+0x120`. `0x00582FC0`, on message `0x12`, releases them, and the buffers at
`+0x588` and `+0x590` are freed after it. `0x00581310(pane)`, run on sub-commands `0x8100`-`0x8102` and
on sub-command `0xF` with value 4¹, closes the pane and calls `0x00291D40` and `0x002CA110`, then
`0x002CC9C0(0x002CC9B0())` when bit `0x8` of `+0xC4` is set.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00582CF2`-`0x00582D04` |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

Measured from `gamedata/disableautosavelist/disableautosavelist.txt` in the archive:

| Fact | Value |
|---|---|
| File size | 673 bytes, 73 lines, each ending in CR LF |
| Rows | 73, naming 72 distinct field ids (1124 appears twice) |
| Field only, always excluded | 21 rows: fields 12, 13, 50, 769, 854, 858, 860, 862, 864, 866, 867, 868, 869, 910, 912, 914, 918, 922, 924, 1113, 1147 |
| Field and entrance | 1 row: field 1140, entrance 9 |
| Field and story counter | 28 rows, story values 16 to 6750 (for example `48,301`) |
| Story -2 (bit `0x1000` of the dword at `[0x02EBF190] + 4`) | 10 rows: fields 1155 to 1299 in steps of 16 |
| Story -1 with a variable | 13 rows, variables 15 to 56; two of them (field 1124) also name entrance 5 or 4 |
| Empty second column | 1 row, `1113,,5303`, which parses as field 1113 alone |

[`saving-and-loading-disable-autosave-rows.tsv`](saving-and-loading-disable-autosave-rows.tsv) lists all 73 rows in file order: the line as shipped, its four
columns, the field's zone, map name and region, the story stage a story value names, the script variable's name
and the boss whose fight it tracks, and the rule in words. What the rows show:

- The ten story -2 rows are the Trial Mode stages 1, 11, 21 and so on to 91 (fields 1155 to 1299, `tri_a01` to
  `tri_s01`): the story value -2 stands for bit `0x1000` of the dword at `[0x02EBF190] + 4`¹, so
  entering those stages in Trial Mode does not autosave.
- Each of the 13 variable rows names a boss flag (`g_btl_...`). The zone scripts set it to 1 when the fight is
  waiting and to 2 once it is won, so the area change skips the autosave only while that boss is still to be
  fought: for example field 441 (Cloister of Solace) while Humbaba Mistant waits (variable 15, image byte
  `+0xC0F`).
- Field 769 (`vic_a04`) is listed, but the US script table holds no script for that field, so no area change
  reaches it and its row never matches; `vic_a04.ebp` still ships in the archive.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00236760` |

</details>

### Columns of saving-and-loading-disable-autosave-rows.tsv

| Column | Holds |
|---|---|
| `variable_name` | the name of the script global the row's `variable` names, the global at payload offset `0xA00` plus `variable` ([Script variables](../Scripts-And-Script-Commands/script-variables.md)): `g_btl_` and the boss's name in Japanese, on the 13 rows with a variable; empty on the other 60, whose `variable` is 0 |
| `entered` | `yes` on 72 rows, where the `us` script array names a script for the field, so an area change can reach it; `no: the us script array names no script for it` on line 18, field 769 (`vic_a04`) |

</details>

## Operations

| Function | Role |
|---|---|
| `0x0057E4D0`, `0x0057E310` | the autosave widget and its writer |
| `0x00582860` | the load lifecycle |
| `0x001C1720` | decide whether an area change autosaves |
| `0x001C0F20` | parse `disableAutosaveList.txt` |

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02CA99E8` | `i32` | an autosave write is busy | `0x0057E310`, `0x0057E4D0` |
| `0x01F81260` | `void*` | the SaveloadManager, holding the autosave exclusion rows at `+0x50` | `0x001C18A0` |

</details>

## Modding notes

- To make an area change autosave, or stop it from autosaving, edit
  `disableAutosaveList.txt`: one `field,story,entrance,variable` row per line, CR LF line ends, no
  spaces, and no empty column in the middle of a row.

## Related

- [Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs](saving-and-loading.md)
- [Save and load screen: the screen's states and popups, the slot list and its status pane, what follows a save or a load, and the screen's widgets](saving-and-loading-screen.md)
- [Save transaction: its steps, the storage queue and its worker, the slot scan, the space requirement, the save-data check and the file layer](saving-and-loading-transaction.md)
- [Loading a save: the steps from choosing a slot to the party standing where it saved](loading-a-save.md)
- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](../World-Areas-And-Travel/zone-changes-and-mapjump.md)
