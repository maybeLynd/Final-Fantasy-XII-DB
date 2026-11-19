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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 151 calls with 30 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236760`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | is called by | [`0x00300E40`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md), [game application](../Engine-Core/game-application.md), [debug menu](../Engine-Core/debug-menu.md), [global state accessors](../Engine-Core/global-state-accessors.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00182D40`](saving-and-loading-autosave.md) | is called by | [`0x0022B8C0`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake) |
| [`0x001831A0`](saving-and-loading-autosave.md) | is called by | [`0x0017D4C0`](../Engine-Core/startup-constants.md) (on startup constants) |
| [`0x001C1710`](saving-and-loading-autosave.md) | is called by | [`0x0017D4C0`](../Engine-Core/startup-constants.md) (on startup constants) |
| [`0x001C18A0`](saving-and-loading-autosave.md) | is called by | [`0x0017D4C0`](../Engine-Core/startup-constants.md) (on startup constants) |
| [`0x001C18E0`](saving-and-loading-autosave.md) | is called by | [`0x0017D4C0`](../Engine-Core/startup-constants.md) (on startup constants)<br>[`0x0017D6E0`](../Engine-Core/game-application.md) (on game application) |
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001EC760`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x00582860`](saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x001EDEC0`](saving-and-loading-screen.md) (on saving and loading screen) |

**Controls and input** (explained on [controls](../Controls-And-Input/controls.md), [game application](../Engine-Core/game-application.md), [force fight mode](../Engine-Core/force-fight-mode.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00182D40`](saving-and-loading-autosave.md) | calls | [`0x001986E0`](../Controls-And-Input/controls.md) (on controls)<br>[`0x00198790`](../Controls-And-Input/controls.md) (on controls) |
| [`0x00236760`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |
| [`0x0027F5D0`](saving-and-loading-transaction.md) (on saving and loading transaction) | calls | [`0x002D66A0`](../Controls-And-Input/controls.md) (on controls) |
| [`0x00582860`](saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x00182D40`](saving-and-loading-autosave.md) |

**Steam and achievements** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [achievements](../Steam-And-Achievements/achievements.md), [loading a save](loading-a-save.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x003154B0`](../Menus-And-HUD/clan-primer-entries.md) (on clan primer entries)<br>[`0x003161A0`](../Steam-And-Achievements/achievements.md) (on achievements) |
| [`0x00584210`](save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00316810`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Graphics** (explained on [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md), [debug menu](../Engine-Core/debug-menu.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00247870`](saving-and-loading-transaction.md) (on saving and loading transaction) | is called by | [`0x00579420`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001CD0E0`](../Engine-Core/graphics-settings.md) (on graphics settings) |
| [`0x002CC9B0`](saving-and-loading-autosave.md) | is called by | [`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x002CC9C0`](saving-and-loading-autosave.md) | is called by | [`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |

**Random numbers** (explained on [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00584210`](save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00379CF0`](../Engine-Core/startup-constants.md) (on startup constants) |

**Game files and data tables** (explained on [async load manager](../Game-Files-And-Data-Tables/async-load-manager.md), [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md), [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md), [debug menu](../Engine-Core/debug-menu.md), [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md), [verb table](../Scripts-And-Script-Commands/verb-table.md), [mrp menu resource packages](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001C1810`](saving-and-loading-autosave.md) | calls | [`0x001A0A90`](../Game-Files-And-Data-Tables/async-load-manager.md) (on async load manager)<br>[`0x001A0BB0`](../Game-Files-And-Data-Tables/async-load-manager.md) (on async load manager)<br>[`0x001A1220`](../Game-Files-And-Data-Tables/async-load-manager.md) (on async load manager) |
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001DA220`](../Game-Files-And-Data-Tables/prefetch-manifests.md) (on prefetch manifests)<br>[`0x001DA970`](../Game-Files-And-Data-Tables/prefetch-manifests.md) (on prefetch manifests) |
| [`0x0027F5D0`](saving-and-loading-transaction.md) (on saving and loading transaction) | calls | [`0x0024A5A0`](../Game-Files-And-Data-Tables/binmenu-images.md) (on binmenu images) |
| [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) | calls | [`0x0032E520`](../Graphics/effect-file-loading.md) (on effect file loading) |
| [`0x00582790`](saving-and-loading-autosave.md) | calls | [`0x00249210`](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md) (on mrp menu resource packages)<br>[`0x00249580`](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md) (on mrp menu resource packages)<br>[`0x003933F0`](../Menus-And-HUD/clan-primer.md) (on clan primer)<br>[`0x00393460`](../Game-Files-And-Data-Tables/tim2-images.md) (on tim2 images) |

**Scripts and script commands** (explained on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [debug logging](../Engine-Core/debug-logging.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001831A0`](saving-and-loading-autosave.md) | is called by | [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) |
| [`0x00236760`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | is called by | [`0x0050F540`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |
| [`0x003BB420`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | is called by | [`0x0050C670`](../Engine-Core/debug-logging.md) (on debug logging)<br>[`0x0050C8D0`](saving-and-loading-autosave.md)<br>[`0x0050C990`](saving-and-loading-autosave.md)<br>[`0x0050EEA0`](saving-and-loading-transaction.md) (on saving and loading transaction)<br>[`0x0050F0A0`](saving-and-loading-transaction.md) (on saving and loading transaction) |
| [`0x003BB430`](saving-and-loading-autosave.md) | is called by | [`0x0050C960`](saving-and-loading-autosave.md)<br>[`0x0050ED50`](saving-and-loading-autosave.md) |

**Enemy spawning** (explained on [native limits](../Engine-Core/native-limits.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) | calls | [`0x00233550`](save-data-fields.md) Spawn keep: restore persistence bank (on save data fields) |

**Story, events and hunts** (explained on [model effects and motion commands](../Graphics/model-effects-and-motion-commands.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001ED240`](../Graphics/model-effects-and-motion-commands.md) G0999; (on model effects and motion commands) |
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x00377970`](../Story-Events-And-Hunts/story-flags.md) (on story flags) |

**Menus and HUD** (explained on [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md), [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md), [force fight mode](../Engine-Core/force-fight-mode.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [subsystem update flags](../Engine-Core/subsystem-update-flags.md), [battle menu](../Menus-And-HUD/battle-menu.md), [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md), [party list](../Menus-And-HUD/party-list.md), [map screens](../Menus-And-HUD/map-screens.md), [hud](../Menus-And-HUD/hud.md), [menu screens](../Menus-And-HUD/menu-screens.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md), [cl2 menu colour tables](../Game-Files-And-Data-Tables/cl2-menu-colour-tables.md), [widget messages](../Menus-And-HUD/widget-messages.md), [party member status record](../Characters-And-Objects/party-member-status-record.md), [controls](../Controls-And-Input/controls.md), [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [clan primer](../Menus-And-HUD/clan-primer.md), [text handbook unrequested](../Menus-And-HUD/text-handbook-unrequested.md), [on screen keyboard](../Controls-And-Input/on-screen-keyboard.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00244960`](loading-a-save.md) (on loading a save) | is called by | [`0x0023ED80`](../Menus-And-HUD/config-screen.md) (on config screen)<br>[`0x00252030`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00276D30`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002778C0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00279E20`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0027AD70`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x00298250`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x002985D0`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x0029BB40`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x0029C770`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x0029C850`](saving-and-loading-autosave.md)<br>[`0x0029C9D0`](../Menus-And-HUD/party-list.md) (on party list) |
| [`0x00244960`](loading-a-save.md) (on loading a save) | is also called by | [`0x002B6350`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002B9D30`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BDCE0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x002BFB40`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x002C9BF0`](../Menus-And-HUD/shop-screens.md) (on shop screens)<br>[`0x003CA310`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CA860`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CAE00`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CB0C0`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CB650`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x003F8790`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x00551E00`](loading-a-save.md) (on loading a save) |
| [`0x00244960`](loading-a-save.md) (on loading a save) | is also called by | [`0x00551F00`](loading-a-save.md) (on loading a save)<br>[`0x005528C0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x00567200`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x0056C170`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x00245020`](../Menus-And-HUD/widgets.md) (on widgets) | is called by | [`0x00253780`](../Game-Files-And-Data-Tables/ps2data-bin-families.md) (on ps2data bin families)<br>[`0x002778C0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00279E20`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0027AD70`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x0027EFA0`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x0027FB70`](../Story-Events-And-Hunts/tutorials-scenes.md) (on tutorials scenes)<br>[`0x0028B860`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x0028F2F0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x00296670`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x002985D0`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x0029A0A0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0029C850`](saving-and-loading-autosave.md) |
| [`0x00245020`](../Menus-And-HUD/widgets.md) (on widgets) | is also called by | [`0x002BF3D0`](../Game-Files-And-Data-Tables/ui-typed-lists.md) (on ui typed lists)<br>[`0x002BF4F0`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x002BFB40`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x002C0870`](../Engine-Core/subsystem-update-flags.md) (on subsystem update flags)<br>[`0x003CA310`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CB410`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x003CB4F0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x003CB650`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x005519E0`](../Game-Files-And-Data-Tables/as7-menu-graphics.md) (on as7 menu graphics)<br>[`0x00552250`](../Game-Files-And-Data-Tables/world-map-mesh-mg.md) (on world map mesh mg)<br>[`0x005528C0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x00558BB0`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) |
| [`0x00247870`](saving-and-loading-transaction.md) (on saving and loading transaction) | is called by | [`0x00276960`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00279E20`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0027DCA0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00297880`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x0029A0A0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002BE450`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x002BF690`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x002C0400`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x002C3560`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x002C4720`](../Game-Files-And-Data-Tables/ui-typed-lists.md) (on ui typed lists)<br>[`0x002CC2A0`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x003C5910`](../Menus-And-HUD/map-screens.md) (on map screens) |
| [`0x00247870`](saving-and-loading-transaction.md) (on saving and loading transaction) | is also called by | [`0x00553F40`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x005542D0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x005771F0`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables)<br>[`0x0057E6D0`](saving-and-loading-screen.md) (on saving and loading screen) |
| [`0x0027F5D0`](saving-and-loading-transaction.md) (on saving and loading transaction) | calls | [`0x0028E790`](../Menus-And-HUD/map-screens.md) (on map screens) |
| [`0x002CA110`](saving-and-loading-autosave.md) | is called by | [`0x002C2320`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen)<br>[`0x00558FB0`](../Menus-And-HUD/license-board-screen.md) (on license board screen)<br>[`0x00560910`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables)<br>[`0x00561390`](../Graphics/menu-effects.md) (on menu effects)<br>[`0x00565E00`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) |
| [`0x002CC9B0`](saving-and-loading-autosave.md) | is called by | [`0x005528C0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x005542D0`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x002CC9C0`](saving-and-loading-autosave.md) | is called by | [`0x0027FB70`](../Story-Events-And-Hunts/tutorials-scenes.md) (on tutorials scenes)<br>[`0x00281ED0`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x005528C0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x005542D0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0056F810`](../Menus-And-HUD/dialogs.md) (on dialogs) |
| [`0x0036FD80`](saving-and-loading-autosave.md) | is called by | [`0x00252030`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x003BB420`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | is called by | [`0x00252030`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x003BB430`](saving-and-loading-autosave.md) | is called by | [`0x00252030`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x00582860`](saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x002814E0`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [game application](../Engine-Core/game-application.md), [changing areas](../World-Areas-And-Travel/changing-areas.md), [native limits](../Engine-Core/native-limits.md), [model effects and motion commands](../Graphics/model-effects-and-motion-commands.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [debug menu](../Engine-Core/debug-menu.md), [script variables](../Scripts-And-Script-Commands/script-variables.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) | is called by | [`0x00266D10`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x001831A0`](saving-and-loading-autosave.md) | is called by | [`0x00314530`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: requeue current field for restore (on zone changes and mapjump) |
| [`0x0020E500`](saving-and-loading-autosave.md) | is called by | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) |
| [`0x00236760`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | is called by | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships)<br>[`0x00584580`](save-data-fields.md) World transition snapshot: capture persistence pair for active slot (on save data fields) |
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001EDCD0`](../Graphics/model-effects-and-motion-commands.md) M1126 (on model effects and motion commands)<br>[`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x003EAA70`](../Sound-And-Music/sound-banks.md) (on sound banks) |
| [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) | calls | [`0x00229B40`](save-data-fields.md) World transition snapshot: capture runtime state (on save data fields)<br>[`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list)<br>[`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries)<br>[`0x00287D00`](../Scripts-And-Script-Commands/script-variables.md) (on script variables)<br>[`0x00584580`](save-data-fields.md) World transition snapshot: capture persistence pair for active slot (on save data fields) |
| [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) | is called by | [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) |
| [`0x00394450`](saving-and-loading-autosave.md) | is called by | [`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) |
| [`0x00582860`](saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) |
| [`0x00584210`](save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00269A20`](save-data-fields.md) World persistence: import group persistent bank (on save data fields)<br>[`0x00314DC0`](loading-a-save.md) World transition: set active or pending field id (on loading a save) |
| [`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) | calls | [`0x00269A20`](save-data-fields.md) World persistence: import group persistent bank (on save data fields) |

</details>
