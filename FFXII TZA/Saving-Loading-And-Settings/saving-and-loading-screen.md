[Home](../../README.md) / [Saving, loading and settings](README.md) / Save and load screen

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Save and load screen: the screen's states and popups, the slot list and its status pane, what follows a save or a load, and the screen's widgets | system | Saving, loading and settings | Saving and loading | How the save and load screen runs: its fifteen states and the popup each opens, how the slot list is built and drawn from the slot status table and the header cache, what the status pane shows, what the screen does after a save or a load, and the layouts of the slot screen, the progress gauge, the card-presence poll, the backdrop and the slot and list records. | 0x00580EB0, 0x005819F0, 0x00581B70, 0x00582860, 0x0057FE80, 0x0057F8C0, 0x0057EFE0, 0x00580CD0, 0x00580840, 0x003BA990, 0x008621E0, 0x001C1720, 0x02B407C0 |

## What the player sees

Saving at a save crystal or loading from the title screen opens the slot list, which shows "Saving" or "Loading" while
the file is written or read and then reports completion or failure. The list shows each used slot's party, gil, Esper
row and clan rank, and marks the others "Unused file." or "Corrupt save data."

## How it works

### The save and load screen

`0x00580EB0(controller, state, popup)` moves the screen between fifteen states and opens a popup
(`0x00583990(popupId, controller)`, kept at `+0xD8`) where one is listed:

| State | What the code does | Popup id | Popup text (`menu_message.bin`, through `0x00583990`'s table at `0x00D23DA0`) |
|---|---|---|---|
| 0 | arms the card-presence poll (`0x0057EC60`) | - (no popup) | |
| 1 | runs the device check (`0x0057EA40`), in save mode when byte `+0xEA` is 0 | - (no popup) | |
| 2 | confirms a new save | `0x15` | "Create new save data for FINAL FANTASY XII THE ZODIAC AGE?" |
| 3 | confirms an overwrite | `0x13` | "Save data ... already exists. Overwrite it?" |
| 4 | opens the save transaction `0x005819F0` as a child widget (`0x00244F50`, `0x00580FFF`) with the slot `+0xEB` and the save counter `+0xE4` + 1, or `0xFFFFFFFF` as it is; plays sound `0x42` when the gauge `[0x02CA99C8]` exists and does not already have it running (`0x00580FAE`-`0x00580FCD`) | `0x10` | "Saving... Please do not close ..." |
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

`0x00580EB0(controller, state, popup)` does nothing for a controller of 0, nor when the state asked for is the one in
its byte `+0xE9`¹. A state above `0xE` is only stored; the others go through the state table
`0x00581268`², and every state that passes both tests is stored at `+0xE9` at the end³. The stack cookie is checked with `0x00808C40`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00580EB0`-`0x00580EE8` |
| ² | `0x00580EEE`-`0x00580F13` |
| ³ | `0x00581246` |
| ⁴ | `0x0058124D`-`0x00581254` |

</details>

State 0 runs `0x0057EC60(controller, 1)` and state 1 `0x0057EA40(controller, +0xEA == 0)`, neither with a popup¹. States 2, 3, 5, 6, 7, `0xA`, `0xC`, `0xD` and `0xE` run `0x0057EC60(controller, 1)` before
their popup, and state `0xC` first stores `0x78` in the byte `+0xE8`². States `0xD` and `0xE` open the popup of the third argument, and none when it is `0xFF`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00580F15`-`0x00580F3C` |
| ² | `0x00580F41`-`0x00580F90`, `0x0058103D`-`0x0058104D`, `0x00581149`-`0x00581220` |
| ³ | `0x00581225`-`0x00581237` |

</details>

States 4, 8 and `0xB` work on the gauge `[0x02CA99C8]` when it exists. Unless bit `0x1` of its `+0xCC` is set they play
sound `0x42` with `0x00249C60(0x42)`, set the bit and keep the handle at `+0xE8`; then they store the operation 2, 3 or
4 in its byte `+0xD0`¹. States 8 and `0xB` call
`0x00254CB0(1)` first².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00580F95`-`0x00580FD3`, `0x00581066`-`0x0058108B`, `0x00581172`-`0x00581197` |
| ² | `0x00581052`-`0x00581057`, `0x0058115E`-`0x00581163` |

</details>

State 4 takes the counter `+0xE4` plus 1, or `0xFFFFFFFF` as it is¹. It fills a
block on its stack with the controller, the controller's qword `+0x1C0`, the slot byte `+0xEB`, the counter and a zero
dword, and opens the save transaction with `0x00244F50(0x4B0, 0x005819F0, record)`, the record pointing at that block; the
new widget is kept at `+0xD0`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00580FA7`, `0x00580FDA`-`0x00580FE0` |
| ² | `0x00580FE3`-`0x00581031` |

</details>

State 8 queues kind 1, the callback `0x00580840` and the low dword of the controller's address, with
`0x00582540(queue, packet)` while the queue object `[0x02CA99C0]` exists¹. It takes the active
image `0x002EF640()` and the name `0x005837F0(1, slot)`, and while the queue exists queues kind 9 with the name copied
into the packet, the image and the size `0x56690`². It then calls `0x005817D0(0x1E, 0x1C)` and
`0x00581860(0x1E, 0x1E)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581092`-`0x005810B7` |
| ² | `0x005810BC`-`0x0058111E` |
| ³ | `0x00581123`-`0x00581137` |

</details>

State 9 opens only its popup¹. State `0xB` queues kind 1 the same way and then kind `0xC`, each with
`0x00582540(queue, packet)` while the queue exists, and calls `0x005817D0(0x1F4, 0x1DB)` and `0x00581860(0x1F4, 0x1F4)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581141` |
| ² | `0x0058119E`-`0x005811F8` |

</details>

`0x00583990(id, controller)` uses entry 0 of the table `0x00D23DA0` for an id of `0x1F` or more¹.
It takes the entry's text `0x002F9860(text id)`, a second text, `0x002F9860(0x49A)` when `0x00254A10()` answers other than 0
and `0x002F9860(0x49C)` when it answers 0, and the size in KB, the queue object's dword `+0xD0` plus `0x3FF` shifted
right by 10, 0 with no queue object².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005839E0`-`0x005839E9` |
| ² | `0x005839AB`-`0x00583A08` |

</details>

The entry's kind byte says how the text is made, into one of two `0x200`-byte buffers from `+0x168` of the save/load
controller `[0x02CA99B8]`, the one its byte `+0xC2` picks: kind 1 calls `0x002B4090(0x200, buffer, text, second)`, kind 2
`0x002B4090(0x200, buffer, text, second, second)`, and kinds 3 and 4 `0x002B4090(0x200, buffer, text, KB)`¹. Kind 0 shows the table's text as it is; any other kind shows the buffer, which a kind above 4
leaves unwritten².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583A0D`-`0x00583AA3` |
| ² | `0x00583ABB`-`0x00583AD9` |

</details>

Without bit `0x10` of the flags byte the entry's sound byte is played with `0x00249C60(sound)`¹.
With bit `0x1` the popup is a choice made by `0x003948B0(controller, text, style, block)`: the style is `0x2021001`, or
`0x20210D1` with bit `0x2`, and the dword `+0x48` of the `0x50`-byte block, zeroed with `0x00861EC0(block, 0, 0x50)`,
gets bit `0x1` for every entry but `0x14` and bits `0x1` and `0x4` with bit `0x20`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583AA8`-`0x00583AB6` |
| ² | `0x00583ADC`-`0x00583B3F` |

</details>

Without bit `0x1` it is a notice made by `0x003949B0(controller, text, block)`, the block, its first `0x18` bytes
zeroed, holding 3 in its byte `+0x10` and `0x88` in its dword `+0x14`, `0xB8` with bit `0x20`¹.
With bit `0x8` the new popup goes through `0x002470C0(popup)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583B46`-`0x00583B7E` |
| ² | `0x00583B83`-`0x00583B91` |

</details>

Last, when the widget `[0x02CA99E0]` exists its `+0xCC` is zeroed; when it does not, the `0xD0`-byte widget with
procedure `0x0057F7D0` is created with `0x00244F50(0xD0, 0x0057F7D0, 0)`¹. The byte `+0xC2` becomes 1
when it was 0 and 0 otherwise, and the opener returns the popup².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583B96`-`0x00583BBD` |
| ² | `0x00583BC2`-`0x00583BE5` |

</details>

`0x00583FD0(id, parent, mode)` opens a popup from the same table by the same rules, with its own size in KB,
`0x003936B0()` plus `0x3FF` shifted right by 10, and its own buffer `0x02CA97B0`. It takes the texts with
`0x002F9860(text id)`, `0x00254A10()` and `0x002F9860(0x49A)` or `0x002F9860(0x49C)`, and makes the text with
`0x002B4090(0x200, 0x02CA97B0, text, ...)` for kinds 1 to 4; kind 0 shows the table's text¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583FF9`-`0x005840A3` |

</details>

It plays the sound with `0x00249C60(sound)` without bit `0x10`¹. With bit `0x1` it makes the
choice with `0x00861EC0(block, 0, 0x50)` and `0x003948B0(parent, text, style, block)` as `0x00583990` does². Without it the notice is made by `0x00394A90(parent, text, block)` when mode is not 0 and by
`0x003949B0(parent, text, block)` when it is 0³. With bit `0x8` the popup goes through
`0x002470C0(popup)`⁴. Its body does not touch `[0x02CA99E0]`, and it returns the popup⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005840A7`-`0x005840B5` |
| ² | `0x005840BA`-`0x00584120` |
| ³ | `0x00584127`-`0x0058416C` |
| ⁴ | `0x00584171`-`0x0058417F` |
| ⁵ | `0x00584184`-`0x0058418C` |

</details>

The three storage results reach the screen as message `0x1D`: class 3 is the card-presence poll
(`0x0057EBB0`, queue kind 3), class `0xD` the device check (`0x0057E950`, kinds 4 and 5) and class
`0xF` the save transaction's completion¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581B70` |

</details>

`0x0057E950(kind, result, pane)` acts on kinds 4 and 5 only¹. For kind 4 with a result of 0 and
bit `0x2` of the pane's `+0xC0` set it sends nothing: it takes the pattern from `0x00393630(buffer, 0x40)` and, when the
queue object `0x02CA99C0` exists, copies the pattern into a kind-5 packet and queues it with `0x00582540(queue, packet)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057E96E`-`0x0057E976` |
| ² | `0x0057E997`-`0x0057E9E9` |

</details>

In every other case it sends `0x00247510(widget, 0x1D, message)` to the widget at the pane's `+0xC8`, the message
holding the class `0xD`, the device byte `+0x39A` of the queue object (`0xFF` when there is none) and the result, and
clears bit `0x1` of the pane's `+0xC0`¹. It checks its stack cookie with `0x00808C40(cookie)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057E97C`-`0x0057EA1E` |
| ² | `0x0057EA30` |

</details>

`0x0057ED40` disarms the card-presence poll: when the queue's front packet has already started (queue
`+0xDC` bit `0x1`) it sets `+0xDC` bit `0x2`, which makes the dequeue `0x00582240` return before that packet's
callback; otherwise it empties the queue (`+0x398` = 0). It also clears bits `0x1` and `0x2` of the poll
widget `0x02CA99D8`. The slot screen calls it when a slot is picked (sub-command `0x8001`) and on
sub-commands `0x8100`-`0x8102`; `0x00580A80` and the load lifecycle `0x00582860` call it too.

`0x00580A80(screen, message)` acts only while the state `+0xE9` is not `0xD` and the message's dword `+0x08` is not 0¹. It first disarms the poll with `0x0057ED40`; then for states 2, 3, 5, 6, 7, `0xA`, `0xC` and
`0xE` (the jump table at `0x00580B0C`) it closes the popup `+0xD8` with `0x00244F00(popup)`, sets `+0xCC` of `[0x02CA99E0]`
to 4 when that exists, and zeroes `+0xD8`². For every state it ends in a jump to
`0x00580EB0(screen, 0xD, 0)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00580A86`-`0x00580A96` |
| ² | `0x00580A98`-`0x00580AE7` |
| ³ | `0x00580AF2`-`0x00580AFF` |

</details>

### The slot list

The slot screen `0x0057FE80` builds its list on message 1 from two tables: the slot status table
`0x02B407C0` (200 entries of 8 bytes, see Layouts; `0x003BB3E0(slot)` returns an entry's address and
`0x003BB600(slot, entry)` replaces one) and the header cache at `+0x1C0`, the first `0xA0` bytes of each
slot's image at `slot * 0xA0`, filled by [the slot scan](saving-and-loading-transaction.md#the-slot-scan).

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
- The cursor stays 0 when no listed manual save has a non-zero counter (none is looked at while `+0xE0` bit `0x1` is
  set, `0x0058007A`), or when the newest one takes row 0 because slot 0 is not listed (a status other than 2 or 4,
  `0x0058006D`, `0x005800A8`); then, when slot 0's counter is below `+0xE4`, the cursor is -1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00580126`-`0x00580168` |

</details>

`0x0057F8C0` draws a row. For status 2 it fills the row from the slot's cached header¹. Any
other status shows a line through `0x0057FA30` (text through `0x002F9860`), and when the screen was opened
with its flag bit `0x1` (`+0xE0`) every row is drawn as status 5:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057FB00` |

</details>

| Status | Text (`menu_message.bin`) |
|---|---|
| 3 | `0x874` "In use by another game." |
| 4 | `0x873` "Corrupt save data." |
| 5 | `0x872` "Unused file." |
| any other | empty |

A row of any status other than 2 then gets a draw mode through `0x00393240`¹: 0 when byte `+0xEA` is 0
and dword `+4` of the row's status record is non-zero, else 1². A status-2 row skips the
draw mode and `0x0057FA30`: after `0x0057FB00` it jumps straight to the slot number³. The status-5 record
that flag bit `0x1` forces carries `+4` = 1⁴, so in save mode those rows get draw mode 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F965` |
| ² | `0x0057F947`-`0x0057F957` |
| ³ | `0x0057F930` |
| ⁴ | `0x0057F93F` |

</details>

`0x0057F8C0` then calls `0x0057FA30(row, unused, status)`¹, which first calls `0x00393190(row, 0)`. Of the row's
parts (`[row + 0x10]`) it hides `+0xD8` and `+0xD0`, clearing bit `0x1` of their `+0x08`, and shows `+0xB0` and the
seven parts at `+0x00`, `+0x20`, `+0x28`, `+0x30`, `+0x08`, `+0x10` and `+0x18` (the byte table `0x00D23EAC`) by setting
it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F973` |
| ² | `0x0057FA42`-`0x0057FA98` |

</details>

The part `+0xB0` then gets at its `+0x18` the status text: `0x002F9860(0x874)`, `0x002F9860(0x873)` or `0x002F9860(0x872)`
for a status `[status]` of 3, 4 or 5, and the empty string `0x01CEB638` for any other; and at its `+0x20` the dword
`0x0020E620(0)` answers, 0 less the dword `0x01F83530`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057FA9C`-`0x0057FAE7` |

</details>

Every row also gets its slot number¹, except slot 0's row in load mode, which hides the
six number parts listed at `0x01F2CD10` and shows its own part `+0xD0`: it clears bit `0x1` of each part's dword
`+8`² and sets that bit on part `+0xD0`³. The number is drawn by two calls,
`0x00393160(row, 4, 3, 9, n)` and `0x00393160(row, 1, 3, 9, n)` with `n = min(slot, 199)`⁴.
`0x0057F8C0` returns 1 on both paths⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00393160` |
| ² | `0x0057F9B2` |
| ³ | `0x0057F9CC` |
| ⁴ | `0x0057F9D9`-`0x0057FA12` |
| ⁵ | `0x0057F9C0`, `0x0057FA17` |

</details>

`0x0057FB00(row, list, header)` fills a status-2 row from the cached header:

- the region text is the region name of the area `+0x4C`¹ and the area text its name
 ²; with flag `+0x57` bit `0x1` set the row also shows its parts `+0xB8` to `+0xC8`, draws a
  frame³ and names the area `+0x80` instead, or `+0x4C` when that is 0;
- in the demo⁴ the region text of persistence groups 7, 22, 25 and 29⁵ is
  replaced by the `menu_message.bin` text `0x7EC`, `0x7EB`, `0x7EE` or `0x7ED`⁶, and the
  play time then shows zeros;
- the play time is hours `+0x18`, minutes `+0x1A` and seconds `+0x1B`, the last two capped at 59,
  drawn as three, two and two digits⁷; 1,000 hours or more show 999:59:59;
- flag `+0x57` bit `0x4` (New Game-) shows the part `+0xD8`, which every other row hides
 ⁸: the "New Game−" badge, a 198 × 30 sprite from
  `DataFace_c.tm2` (atlas `dataface_c`, sub-image 0, frame 18) at the row's top left
  ([New Game+ and New Game-](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003778B0` |
| ² | `0x00377B60` |
| ³ | `0x002DC290` |
| ⁴ | `0x00264150` |
| ⁵ | `0x00264F90` |
| ⁶ | `0x002F9860` |
| ⁷ | `0x00393160` |
| ⁸ | `0x0057FBA1`-`0x0057FBB3`, `0x0057FBFC`-`0x0057FC0E` |

</details>

The frame of a row with bit `0x1` of `+0x57` is `0x002DC290(list, rect, colours)`: a rectangle at 2, 2 that is 4 less
than the words `+0x08` and `+0x0A` of the row's `+0x08` in each direction, with `0x4816224A` in all four colours¹. Every row then goes through `0x00393190(row, 1)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057FB2A`-`0x0057FB8F` |
| ² | `0x0057FB94`-`0x0057FB9C` |

</details>

In the row's part array `+0x10` it hides the parts `+0xD8` and `+0xB0`, shows the seven parts the byte table
`0x00D23EAC` lists, `+0x00`, `+0x20`, `+0x28`, `+0x30`, `+0x08`, `+0x10` and `+0x18`, and hides the part `+0xD0`, by bit
`0x1` of each part's dword `+0x08`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057FBA1`-`0x0057FBF8` |

</details>

With bit `0x1` the part `+0xB8` gets the area name `0x00377B60(+0x4C)` at `+0x18` and `0x0020E620(0)`, 0 less the dword
`0x01F83530`, at `+0x20`, is shown and is measured with `0x0029FE20(part, &width, &height)`. The part `+0xC8` is shown
with its word `+0x0C` set to the `+0x0C` of part `+0xB8` less its own word `+0x10`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057FC12`-`0x0057FC82` |

</details>

The part `+0xC0` gets the region name `0x003778B0(+0x4C)`: its word `+0x0C` takes the `+0x0C` of part `+0xB8` less the
word `+0x10` of part `+0xC8` and its own word `+0x10`, and its word `+0x0E` the `+0x0E` of part `+0xB8`; it goes to
`0x0029FB50(part)`, is shown, and its `+0x0C` becomes word `+0x04` of its first pointer less the width; the name goes at
`+0x18` and `0x0020E620(0)` at `+0x20`¹. Without bit `0x1` the parts `+0xC0`, `+0xC8` and `+0xB8`
are hidden².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057FC86`-`0x0057FCD9` |
| ² | `0x0057FCE5`-`0x0057FD0E` |

</details>

The region and area texts of the list above, the demo's replacements included¹, go to the
parts: `+0x90` gets the region text at `+0x18` and `0x0020E620(0)` at `+0x20`, the part `+0xA0` is hidden by clearing
bit `0x1` of its `+0x08`, and `+0x98` gets `0x00377B60(area)` at `+0x18` and `0x0020E620(0)` at `+0x20`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057FD12`-`0x0057FD66` |
| ² | `0x0057FD69`-`0x0057FDAE` |

</details>

The play time of the list above (`0x0057FDB1`-`0x0057FDF6`, the hours cap an unsigned compare) is drawn by
`0x00393160(row, 8, 3, 3, hours)`, `0x00393160(row, 0xB, 2, 1, minutes)` and `0x00393160(row, 0xD, 2, 1, seconds)`, with the
part `+0x38` hidden between the first two by clearing bit `0x1` of its `+0x08`¹. The stack
cookie is checked with `0x00808C40`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057FDF9`-`0x0057FE4D` |
| ² | `0x0057FE52`-`0x0057FE5A` |

</details>

Moving the cursor (sub-command `0x8000`) calls `0x0057EFE0(pane, header)` for a status-2 slot and hides
the pane for any other. `0x0057EFE0` fills the status pane, whose labels are ESPER (`0x875`), CLAN RANK
(`0x876`) and POINTS (`0x877`), from the cached header:

- the seven roster entries through `0x0057E6D0`: an entry whose character byte is `0xFF` is hidden, and
  the level is capped at 99;
- the gil `+0x08`, capped at 99,999,999;
- the Esper row, shown only when `+0x3C` (the summoned Esper's character row, see the [save file format page](save-file-format.md)) is
  not `0xFF`: `0x0035D330(2, +0x3C)` looks the row up in the character table `[0x02EBF130]`¹
  and `0x002B58B0` gives its name;
- the clan rank row, shown when `+0x44` is non-zero and the demo flag `0x0209A2A9`² is clear:
  the rank title `0x003153F0(+0x44)` for ranks 1-12 and the points `+0x40`, capped at 99,999,999.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031C5D0` |
| ² | `0x00264150` |

</details>

`0x0057EFE0(pane, header)` does nothing for a pane of 0¹. It keeps the header at the pane's `+0x100` and
shows the pane, or hides it for a header of 0, with `0x00247870(pane, header != 0)`; with a header of 0 it stops there². The roster entries are `0x0057E6D0(part, header)` on the parts at `+0xC8` to `+0xF8`³, and the gil is drawn with `0x00394850(pane, 0, 2, 8, 0, gil)`, its cap an unsigned compare⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057EFE3` |
| ² | `0x0057EFF3`-`0x0057F014` |
| ³ | `0x0057F01F`-`0x0057F053` |
| ⁴ | `0x0057F055`-`0x0057F07B` |

</details>

The three rows are the pane's children `0x00394660(pane, 0)`, `0x00394660(pane, 1)` and `0x00394660(pane, 2)`. Child 0's
parts 1 and 11 of its part array `+0x60` go to `0x0029FB50(part)`¹. Child 1, the Esper row, is
hidden with `0x00247870(child, 0)` when the dword `+0x3C` is `0xFF`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F080`-`0x0057F0B6` |
| ² | `0x0057F0BB`-`0x0057F0E4` |

</details>

Otherwise `0x00247870(child, 1)` shows it. Part 2 gets the byte `+0x0F` of its own `+0x20` at its `+0x39` and 1 in its
word `+0x0A`; part 1 gets the name `0x002B58B0([row + 0x18], 0)` at `+0x18` and `0x0020E620(0)`, 0 less the dword
`0x01F83530`, at `+0x20`; and part 0 goes to `0x0029FB50(part)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F0E9`-`0x0057F169` |

</details>

Child 2 is hidden with `0x00247870(child, 0)` in the cases the list above gives¹ and shown with `0x00247870(child, 1)` otherwise. The title `0x003153F0(rank)` is asked only for a
rank below `0xD`; bit `0x1` of part 2's `+0x08` is set when there is a title and cleared when there is not, and with a
title part 2 gets it at `+0x18` and `0x0020E620(0)` at `+0x20`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F16E`-`0x0057F18E`, `0x0057F24C`-`0x0057F251` |
| ² | `0x0057F194`-`0x0057F1F7` |

</details>

Parts 1 and 3 go to `0x0029FB50(part)`, and the points are drawn by `0x00394800(child, 4, 8, 3, points)`, the cap a signed
compare¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057F1FB`-`0x0057F245` |

</details>

### After a save or a load

The controller copies the active image's first `0xE240` bytes (`0x1C4` blocks of 128 bytes and 64
bytes) into a buffer it allocates at `+0x588` when it opens (`0x00583CB0`, called from `0x00582860`
message 1); `0x00583C00` copies them back.

`0x00580CD0`, the slot screen's handler for the class-`0xF` result, closes the popup at `+0xD8`¹, sets `+0xCC` of `0x02CA99E0` to 4 and calls `0x00581350(error != 0)`. On success it:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00244F00` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | adds 1 to the counter `+0xE4` unless it is `0xFFFFFFFF`, and writes it to the active image's `+0x50` and to `0x02CA99B4`; |   |
| 2 | sets bit `0x4` of the controller's `+0xC4`; |   |
| 3 | copies the active image's first `0xA0` bytes to the slot's cache row and refreshes the pane; | `0x0057EFE0` |
| 4 | stores `{2, 0}` in the slot's status entry, recounts `+0xED` (status 5) and `+0xEE` (status 5, status 2 or the room flag set), and moves to state 5. |   |

On an error it moves to state `0xD` with popup 5, "Save failed." (`0x818`).

`0x00580840` is the load and format callback; it does nothing once the screen has set `+0xE0` bit `0x10`.
It takes the screen as the low 32 bits of its third argument¹ and ignores kinds other than 9 and
`0xC`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00580847` |
| ² | `0x00580861`, `0x005809D6` |

</details>

For both kinds it first closes the popup at `+0xD8`¹ and stores 0 there, sets `+0xCC` of
`0x02CA99E0` to 4 when that widget exists, and calls `0x00581350(error != 0)` and `0x00254CB0(0)`². Every error path raises bit `0x4` in the gauge's flags at `[0x02CA99C8] + 0xC8` when the
gauge exists³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00244F00` |
| ² | `0x0058087F`-`0x005808C3`, `0x005809DC`-`0x00580A16` |
| ³ | `0x0058091A`, `0x00580A56` |

</details>

For the read (kind 9):

| Result | What it does | Next state, popup |
|---|---|---|
| 0 | `0x005813E0`, then `0x00247510([+0xC0], 0x10, 4)` (`0x005808D1`-`0x005808E6`) | 9, "Load complete." |
| 8 | restores the image head (`0x00583C00`), stores `{4, 1}`, sets the slot's bit in `+0x568`, hides the pane; the bit only when the controller `0x02CA99B8` exists and the slot is below 200 (`0x0058095D`-`0x00580983`); the pane, when `+0xC8` is set, gets 0 at its `+0x100` and `0x00247870(pane, 0)` (`0x0058098A`-`0x0058099F`) | `0xE`, popup 10, "Unable to load. Save data is corrupted." (`0x86D`) |
| any other | restores the image head | `0xD`, popup 6, "Load failed." (`0x81C`) |

A failed load therefore puts back the header and the payload up to the first group bank; the rest of
the image keeps whatever the read copied into it. For the format (kind `0xC`), success clears `+0xE0` bit `0x1`,
sets bit `0x8`, runs `0x005813E0` and moves to state `0xC`¹, and an error moves to `0xD`
with popup 4, "Failed to format memory card (PS2)." (`0x814`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00580A1F`-`0x00580A45` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

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
| `+0x0EA` | `u8` | loadMode | 0 for the save screen, 1 for the load screen, the creation record's `+0x10` (`0x0057FF16`): it chooses the slots listed (`0x0057FF56`, `0x00580055`), the device check's mode (`0x00580F29`), the row draw mode, and how a confirm (`0x00580541`), the text of message `0xE` (`0x0058030F`) and `0x00580B40` (`0x00580B46`) proceed |
| `+0x0EB` | `u8` | slot | the slot the player confirmed (`0x0058053A`); state 4 opens the save transaction with it (The save and load screen above) |
| `+0x0EC` | `u8` | rowCount | the rows listed: 0 at construction (the word store at `0x0057FFAB`), 1 more for each listed slot (`0x005800E1`-`0x005800F0`); `0x00580CD0` adds a row after a save (`0x00580E49`-`0x00580E5E`) |
| `+0x0ED` | `u8` | unusedRows | the scanned slots with status 5, "Unused file" (`0x0058002F`), counted before the load-mode filter (`0x00580055`-`0x0058006D`), so in load mode also slots that are not listed; 0 at construction (`0x0057FFAB`) |
| `+0x0EE` | `u8` | usableRows | the scanned slots with status 5, status 2, or room reserved (`0x00580035`, `0x0058004F`), counted before the load-mode filter as `+0xED`; 0 at construction (`0x0057FFB3`) |
| `+0x0EF` | `u8[200]` | rowSlot | the slot number of each row: the list build stores each listed slot (`0x005800E8`); in load mode the autosave row is moved down past the newest manual save by swapping neighbours (`0x0058012A`-`0x00580154`); the row draw, the confirm and the cursor move read it (`0x00580437`, `0x0058050C`, `0x00580C5E`, `0x00580D6F`) |
| `+0x1B7` | `u8` | pad1B7 | read and written by no function; nothing fixes its width |
| `+0x1B8` | `void*` | list | the slot list widget, layout item 0's `+0x18` (`0x0057FF9A`); the construct message sets it up and starts its cursor (`0x0058018D`-`0x005801D9`); `0x00580B40` (`0x00580C24`) and `0x00580CD0` (`0x00580D2B`) read it |
| `+0x1C0` | `void*` | headerCache | the header cache, the first `0xA0` bytes of each slot's image at slot x `0xA0`, the creation record's `+0x18` (`0x0057FF20`); read for the counters `+0x50` and the row draw (`0x00580088`, `0x00580156`, `0x0058016A`, `0x0058045A`, `0x00580C72`, `0x00580DB0`, `0x00580E1E`, `0x00580FF8`) |

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
| `+0x0F0` | `void*` | numberNode | the gauge's number display, layout entry 1 (`0x00394690`, `0x005816CA`): the construct message adds `0x200` to its words `+0x48` and `+0x4A`, each only when it is below `0x10`, an unsigned compare (`0x005816D6`-`0x005816FB`), `0x00581930` writes the value (`0x00225580`) and its colour (`0x0029F480`) into it (`0x00581952`, `0x0058197C`), the resets `0x005812B0` and `0x005817D0` do nothing when [`0x02CA99C8`] is 0 (`0x005812BD`, `0x005817EA`); otherwise they store 0 in the display's `+0x18` with `0x00225580`(display, 0) when the display is not 0 (`0x005812C2`-`0x005812EF`, `0x005817EF`-`0x0058181C`), and `0x005817D0` then stores 10 x its first argument at the display's `+0x1C` with `0x0029F4B0`(display, 10 x first argument) without testing the display for 0 (`0x00581821`-`0x00581839`); that value and 10 x its second argument also replace the reset's `+0xD4` and `+0xE0` in the same call (`0x00581833`, `0x00581848`) |
| `+0x0F8` | `u32` | animStep | the steps taken of the animation: 0 when one starts (`0x0058144D`, `0x005818F2`), 1 more each tick (`0x00581555`) |
| `+0x0FC` | `u32` | animSteps | the animation's length in ticks: 4 for `0x005813E0`'s run to the full value (`0x0058145C`), or the steps `0x00581860` works out (`0x00581902`), at least 1; 0 when the animation ends (`0x005815C5`), when there is nothing to animate (`0x0058147A`, `0x00581918`) and on reset (`0x005812F4`, `0x0058182D`, `0x00581742`). The tick animates only while it is not 0 (`0x00581536`) |
| `+0x100` | `u32` | animFrom | the value the animation starts from, the shown value (`0x00581422`, `0x005818C6`); read by the tick (`0x00581561`) |
| `+0x104` | `u32` | animSpan | the full value less the start (`0x0058143E`, `0x005818DE`); the tick adds animSpan x animStep / animSteps to the start (`0x00581571`-`0x005815A9`), and the whole span at the end (`0x005815B1`) |
| `+0x108` | `u32` | animValue | the value the animation has reached, which the tick shows (`0x0058142B`, `0x005818CF`, `0x00581567`, `0x005815A9`, `0x005815B9`) |
| `+0x10C` | `f32` | animFraction | animStep / animSteps (`0x00581599`), 1.0 at the end (`0x005815CB`), 0 when an animation starts (`0x00581453`, `0x005818F8`); read by no instruction |

The procedure `0x00581490(gauge, message)` handles messages 1, 2, `0xF` and `0x12` and passes every other one to
`0x005C5230(gauge, message)`¹. Messages `0xF` and `0x12` make the posts the `+0xC0` row gives
with `0x00247510(owner, 0xF, 3)` and `0x00247510(owner, 0x12, 3)`; message `0x12` also zeroes `0x02CA99C8`². Every handled message answers 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0058149D`-`0x005814C4` |
| ² | `0x005814C9`-`0x00581515` |

</details>

Message 1 takes the creation record at the message's `+0x08`. It calls
`0x002432B0(gauge + 0x50, the record's second qword, 1, gauge)` and, when the gauge is not 0, copies the words `+0x04`
to `+0x0A` of what it returns to the gauge's `+0x98` to `+0x9E`¹. It then stores the owner, the
gauge at `0x02CA99C8` and the number display².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0058165F`-`0x005816A5` |
| ² | `0x005816AC`-`0x005816CA` |

</details>

The display's words `+0x48` and `+0x4A` gain `0x200` only when below `0x10`, an unsigned compare¹. The qword stores set `+0xD4` to `0xFFFF` with `+0xD8` 0 and zero `+0xDC` and `+0xE0`; `+0xC8`
becomes 0, and `0x00225580(display, 0)` is called when the display exists²; then `+0xE8` becomes
-1, `+0xFC` 0, the byte `+0xD0` `0xFF` and `+0xCC` 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005816D1`-`0x005816FB` |
| ² | `0x005816FF`-`0x00581727` |
| ³ | `0x0058172C`-`0x0058174F` |

</details>

It then calls `0x0029F4B0(display, full)`, `0x00225580(display, shown)` and `0x0029F480(display, &colour, 1)` with the
colour `0x002DD7E0(0xD1)`, then `0x00394720(gauge, 0, 0x50)`, `0x00246AD0(owner, gauge)` and `0x00247930(gauge, 0x63)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581755`-`0x005817B6` |

</details>

Message 2, the tick, works only when `0x001EDEC0(+0xB4)` answers other than 0 and the `+0xC8` and `+0xFC` rows let it¹; a second read of `+0xFC` that finds 0 takes the value -1². It adds 1
to the step `+0xF8` and runs the animation of the `+0xF8` to `+0x10C` rows in floats and stores the value `+0x108` as
an integer³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00581516`-`0x0058153D` |
| ² | `0x00581543`-`0x00581550` |
| ³ | `0x00581555`-`0x005815CB` |

</details>

With bit `0x1` of `+0xC8` set the value `+0x108` is drawn as it is¹. Otherwise the creep of the
`+0xDC` and `+0xE4` rows applies, its compare unsigned², and then the soft cap of the `+0xE0`
row³. Every tick that works ends in `0x00581930(gauge, value)`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005815D5`-`0x005815DD` |
| ² | `0x005815DF`-`0x0058161D` |
| ³ | `0x00581623`-`0x00581642` |
| ⁴ | `0x00581648`-`0x0058164D` |

</details>

### The card-presence poll

The poll is the `0xD0`-byte widget kept at `0x02CA99D8` with procedure `0x0057EB30`.

`CardPresencePoll` (`0xD0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0057EB30` |
| `+0xC0` | `u32` | flags | bit `0x1`: the second argument of the poll arm `0x0057EC60` (`0x0057ECC7`-`0x0057ECD1`); bit `0x2`: a presence poll is queued, set by `0x0057EC60` (`0x0057ED13`) and by the device check `0x0057EA40` after it queues its packets (`0x0057EAFE`); while bit `0x2` is set each of the three, `0x0057EA40` (`0x0057EA5D`), `0x0057EC60` (`0x0057EC7A`) and the disarm `0x0057ED40` (`0x0057ED4C`), first empties the storage queue, or marks its started front packet to skip its callback. The disarm clears bits `0x1` and `0x2` (`0x0057ED85`, `0x0057ED9B`); the construct message sets 0 (`0x0057EB74`) |
| `+0xC4` | `u32` | pollResult | written by the presence-poll callback `0x0057EBB0`: a result of 0 sets bit `0x1` (`0x0057EBD4`); any other result clears bit `0x1` and sets bit `0x2` (`0x0057EBDD`, `0x0057EBE4`) |
| `+0xC8` | `void*` | controller | the first argument of the poll arm `0x0057EC60`, the save and load screen that armed it (`0x0057ECD7`); 0 at construction (`0x0057EB6A`) |

The procedure `0x0057EB30(widget, message)` handles messages 1 and 18 and passes every other one on with a jump to
`0x005C5230(widget, message)`¹. Message 18 zeroes `0x02CA99D8` and answers 0². Message 1 stores the widget at `0x02CA99D8`, zeroes `+0xC8` and `+0xC0`, calls
`0x00244960([0x0208EA28], widget)`, `0x00247870(widget, 0)` and `0x00247930(widget, 0x64)`, and answers 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057EB36`-`0x0057EB4D` |
| ² | `0x0057EB52`-`0x0057EB60` |
| ³ | `0x0057EB61`-`0x0057EB9D` |

</details>

While the poll widget `[0x02CA99D8]` exists, `0x0057EC60(screen, flag)` and `0x0057EA40(widget, flag)` first settle the
storage queue `0x02CA99C0` when bit `0x2` of the widget's `+0xC0` is set and the queue's byte `+0x398` is 1 or more:
with bit `0x1` of the queue's `+0xDC` set they set its bit `0x2` and store 1 at `+0x398`, otherwise they store 0 at
`+0x398` and at `+0xCC`¹. With no widget they do nothing².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057EC7A`-`0x0057ECC0`, `0x0057EA5D`-`0x0057EA9F` |
| ² | `0x0057EC74`, `0x0057EA57` |

</details>

`0x0057EC60` then copies the flag's low bit into bit `0x1` of the widget's `+0xC0` and stores the screen at `+0xC8`¹. With the queue it queues a kind-1 packet with the callback `0x0057EBB0` and the low dword of
the widget's address through `0x00582540(queue, packet)`². It then sets bit `0x2` of `+0xC0` and,
with the queue, queues kind 3³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057ECC7`-`0x0057ECD7` |
| ² | `0x0057ECDE`-`0x0057ED00` |
| ³ | `0x0057ED13`-`0x0057ED2C` |

</details>

`0x0057EA40` instead stores its arguments, the caller's widget (the screen from `0x00580EB0`, `0x00580F37`, or `0x0057F360`'s
own `0xF0`-byte widget, `0x0057F607`) and the flag, in the pane `[0x02CA99D0]` (the device-check pane under State;
`0x0057EAA6`-`0x0057EAC2`). With the queue it queues kind 1 with the callback `0x0057E950` and the low dword of the pane's
address¹. It then sets bit `0x2` of the poll widget's `+0xC0` and, with the queue, queues kind
4 with `0x00582540(queue, packet)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057EAC9`-`0x0057EAEB` |
| ² | `0x0057EAFE`-`0x0057EB17` |

</details>

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

`0x002CCB10` closes screen layer 1, the widget at `+0x298` of `[0x0209AC30]`, with a jump to `0x00244F00(layer)`, and only
when the layer exists and bit `0x20` of its `+0x7C` is clear¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CCB10`-`0x002CCB27` |

</details>

### Slot and list records

The slot status table, the save list rows and the disable-autosave rows are laid out as follows.

`SlotStatusEntry` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | status | 1 no file yet, 2 header read in full, 3 no file and no room, 4 file shorter than the header or failed to load, 5 no file with room reserved (`0x003BA990`, `0x00580840`) |
| `+0x04` | `i32` | room | 1 when the slot's space requirement was reserved (`0x003BA990`, `0x003BA720`) |

The table holds 200 entries at `0x02B407C0`; slot `n` is entry `n`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BB3E0`, `0x003BB600` |

</details>

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
| `+0x04` | `i32` | story | 0 any; otherwise the counter it must equal; -2 only while bit `0x1000` of [`0x02EBF190`]+4 is set |
| `+0x08` | `i32` | entrance | 0 any entrance; otherwise the entrance it must equal |
| `+0x0C` | `i32` | variable | 0 no variable; otherwise the row also matches while `0x002EF390`(variable) is true |

</details>

## Operations

| Function | Role |
|---|---|
| `0x00580EB0` | the save and load screen's state machine |
| `0x0057FE80` | the slot screen: builds the slot list |
| `0x0057F8C0`, `0x0057FA30` | draw a slot row, the status line |
| `0x0057EFE0` | fill the status pane from a cached header |
| `0x00580CD0`, `0x00580840` | the save result, the load and format result |
| `0x00583CB0`, `0x00583C00` | back up, restore the image's first `0xE240` bytes |
| `0x0057ED40` | disarm the card-presence poll |
| `0x003BB3E0`, `0x003BB600` | read, replace a slot status entry |

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02CA99C8` | `void*` | the gauge widget | the controller |

The device-check pane:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA99D0` | `void*` | 0 (zero-filled tail) | the device-check pane, the `0xD0`-byte widget with procedure `0x0057E8D0` that the save and load screen `0x00582860` builds while it is 0; the device check `0x0057EA40` stores the controller at its `+0xC8` and bit `0x1` of its second argument, the save-or-load mode, in bit `0x2` of `+0xC0` | `0x0057E8D0`: itself on message 1 (`0x0057E903`), 0 on message 18 (`0x0057E8F4`) | `0x00582860`, which builds it only while it is 0 (`0x00582A90`-`0x00582AA9`) and closes it with `0x00244F00` on leaving (`0x00582B7C`, `0x00582BEF`, `0x00582C38`); `0x0057EA40` (`0x0057EAA6`) |

No other instruction reaches `0x02CA99D0`: no other RIP-relative, image-base-relative or 32-bit offset reference names
it.

</details>

## Related

- [Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs](saving-and-loading.md)
- [Save transaction: its steps, the storage queue and its worker, the slot scan, the space requirement, the save-data check and the file layer](saving-and-loading-transaction.md)
- [Area-change autosave: when it runs, which area changes skip it, the shipped list of those area changes, and what a load runs](saving-and-loading-autosave.md)
- [Loading a save: the steps from choosing a slot to the party standing where it saved](loading-a-save.md)
- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md)
- [Widgets: how every menu element is built, sized, attached, focused, animated and torn down](../Menus-And-HUD/widgets.md)

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 89 calls with 20 other topics</summary>

**Characters and objects** (explained on [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002B58B0`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) | is called by | [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) |

**Sound and music** (explained on [sound banks](../Sound-And-Music/sound-banks.md), [sound driver objects](../Sound-And-Music/sound-driver-objects.md), [audio manager](../Sound-And-Music/audio-manager.md), [force fight mode](../Engine-Core/force-fight-mode.md), [message windows](../Menus-And-HUD/message-windows.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00225580`](saving-and-loading-screen.md) | is called by | [`0x00222740`](../Sound-And-Music/sound-banks.md) (on sound banks)<br>[`0x00222F20`](../Sound-And-Music/sound-banks.md) (on sound banks)<br>[`0x00223190`](../Sound-And-Music/audio-manager.md) (on audio manager)<br>[`0x00223DA0`](saving-and-loading-screen.md)<br>[`0x00224570`](../Sound-And-Music/audio-manager.md) (on audio manager)<br>[`0x00224C40`](../Sound-And-Music/audio-manager.md) (on audio manager)<br>[`0x00224E40`](saving-and-loading-screen.md)<br>[`0x00224F10`](saving-and-loading-screen.md)<br>[`0x002251B0`](../Sound-And-Music/audio-manager.md) (on audio manager)<br>[`0x002252C0`](saving-and-loading-screen.md) |
| [`0x0024A1A0`](../Menus-And-HUD/message-windows.md) (on message windows) | calls | [`0x002DEE80`](../Sound-And-Music/sound-effects.md) (on sound effects)<br>[`0x002DF0F0`](../Sound-And-Music/sound-effects.md) (on sound effects) |
| [`0x00581350`](saving-and-loading-screen.md) | calls | [`0x0024A1A0`](../Menus-And-HUD/message-windows.md) (on message windows) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md), [startup constants](../Engine-Core/startup-constants.md), [global state accessors](../Engine-Core/global-state-accessors.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002465F0`](../Menus-And-HUD/widgets.md) (on widgets) | calls | [`0x001EDDA0`](../Graphics/effect-lifecycle.md) (on effect lifecycle) |
| [`0x00254A10`](../Menus-And-HUD/text-string-tables.md) (on text string tables) | calls | [`0x00229E40`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences) |
| [`0x0057F7D0`](saving-and-loading-screen.md) | calls | [`0x001EDEC0`](saving-and-loading-screen.md) |
| [`0x0057FE80`](saving-and-loading-screen.md) | calls | [`0x001EDEC0`](saving-and-loading-screen.md) |
| [`0x00581490`](saving-and-loading-screen.md) | calls | [`0x001EDEC0`](saving-and-loading-screen.md) |
| [`0x00582860`](saving-and-loading-screen.md) | calls | [`0x001EDEC0`](saving-and-loading-screen.md) |

**Gameplay** (explained on [item and ability ids](../Engine-Core/item-and-ability-ids.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031C5D0`](../Engine-Core/item-and-ability-ids.md) (on item and ability ids) | calls | [`0x00309EC0`](../Enemy-AI-And-Gambits/gambit-conditions.md) (on gambit conditions)<br>[`0x0030AE30`](../Engine-Core/item-and-ability-ids.md) (on item and ability ids)<br>[`0x0030B0E0`](../Battle-Actions/command-availability.md) (on command availability)<br>[`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) |
| [`0x0035D330`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors) | calls | [`0x0031C5D0`](../Engine-Core/item-and-ability-ids.md) (on item and ability ids) |

**Controls and input** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00582860`](saving-and-loading-screen.md) | calls | [`0x00182D40`](saving-and-loading-autosave.md) (on saving and loading autosave) |

**Graphics** (explained on [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md), [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md), [escape](../Controls-And-Input/escape.md), [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md), [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [battle numbers](../Menus-And-HUD/battle-numbers.md), [btm exfont bitmaps](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md), [sprite batcher](../Graphics/sprite-batcher.md), [widgets](../Menus-And-HUD/widgets.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [hud](../Menus-And-HUD/hud.md), [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDEC0`](saving-and-loading-screen.md) | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002BC3E0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002D2DB0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00366B80`](../Controls-And-Input/escape.md) (on escape) |
| [`0x00225580`](saving-and-loading-screen.md) | is called by | [`0x0029A930`](../Menus-And-HUD/party-list.md) (on party list) |
| [`0x00247510`](saving-and-loading-screen.md) | is called by | [`0x002D2DB0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00579420`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |
| [`0x00247870`](saving-and-loading-transaction.md) (on saving and loading transaction) | is called by | [`0x00579420`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |
| [`0x00254A10`](../Menus-And-HUD/text-string-tables.md) (on text string tables) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing)<br>[`0x002D2DB0`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x00264150`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) | is called by | [`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x0029F480`](saving-and-loading-screen.md) | is called by | [`0x0029A930`](../Menus-And-HUD/party-list.md) (on party list) |
| [`0x002B58B0`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables) | is called by | [`0x00506700`](../Menus-And-HUD/battle-numbers.md) (on battle numbers) |
| [`0x002D46F0`](saving-and-loading-screen.md) | is called by | [`0x00579420`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |
| [`0x002DC290`](saving-and-loading-screen.md) | calls | [`0x003A1DB0`](../PhyreEngine/the-frame.md) Render command: submit current buffer and swap (on the frame) |
| [`0x002DC290`](saving-and-loading-screen.md) | is called by | [`0x00392CE0`](../Graphics/sprite-batcher.md) (on sprite batcher) |
| [`0x002DD7E0`](saving-and-loading-screen.md) | is called by | [`0x00245170`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002455A0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0029A930`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x002B8EE0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BCB00`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002D0650`](../Graphics/sprite-batcher.md) (on sprite batcher)<br>[`0x003FB3E0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003FBA80`](../Game-Files-And-Data-Tables/prefetch-manifests.md) (on prefetch manifests)<br>[`0x004048E0`](../Game-Files-And-Data-Tables/menu-map-files.md) (on menu map files)<br>[`0x00506700`](../Menus-And-HUD/battle-numbers.md) (on battle numbers) |
| [`0x0035D330`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors) | is called by | [`0x003BBD00`](../Random-Numbers/which-roll-uses-which-generator.md) (on which roll uses which generator)<br>[`0x00506700`](../Menus-And-HUD/battle-numbers.md) (on battle numbers) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x00394660`](saving-and-loading-screen.md) | is called by | [`0x00578450`](../Game-Files-And-Data-Tables/quest-menu-files.md) (on quest menu files) |
| [`0x00394720`](saving-and-loading-screen.md) | is called by | [`0x00579420`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |
| [`0x0057FB00`](saving-and-loading-screen.md) | calls | [`0x002DC290`](saving-and-loading-screen.md) |

**Rewards: EXP, LP, gil and loot** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264150`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) | is called by | [`0x002F90C0`](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md) Reward: compute license points for recipient (on exp lp and level ups) |

**Scripts and script commands** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [shared zone script actors](../Story-Events-And-Hunts/shared-zone-script-actors.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00254CB0`](loading-a-save.md) (on loading a save) | is called by | [`0x0050D9A0`](save-file-format.md) (on save file format)<br>[`0x0050ED70`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors)<br>[`0x0050EEA0`](saving-and-loading-transaction.md) (on saving and loading transaction)<br>[`0x0050EF50`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors)<br>[`0x0050F0A0`](saving-and-loading-transaction.md) (on saving and loading transaction) |
| [`0x00264150`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) | is called by | [`0x0050CC30`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x00357450`](saving-and-loading-screen.md)<br>[`0x0050CDE0`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |

**World, areas and travel** (explained on [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md), [changing areas](../World-Areas-And-Travel/changing-areas.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [native limits](../Engine-Core/native-limits.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264150`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) | is called by | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x003778B0`](saving-and-loading-screen.md)<br>[`0x003C0450`](../Game-Files-And-Data-Tables/menu-map-files.md) (on menu map files)<br>[`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x0029FB50`](saving-and-loading-screen.md) | is called by | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x0029FE20`](../Menus-And-HUD/text-drawing.md) (on text drawing) | is called by | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x002DC290`](saving-and-loading-screen.md) | is called by | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x002EF640`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | is called by | [`0x00229B40`](save-data-fields.md) World transition snapshot: capture runtime state (on save data fields)<br>[`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) |
| [`0x003778B0`](saving-and-loading-screen.md) | calls | [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) |
| [`0x003778B0`](saving-and-loading-screen.md) | is called by | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x00393160`](saving-and-loading-screen.md) | is called by | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x00393190`](saving-and-loading-screen.md) | is called by | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x0057F8C0`](saving-and-loading-screen.md) | calls | [`0x0057FB00`](saving-and-loading-screen.md) |
| [`0x0057FB00`](saving-and-loading-screen.md) | calls | [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list)<br>[`0x003778B0`](saving-and-loading-screen.md) |
| [`0x00582860`](saving-and-loading-screen.md) | calls | [`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) |

</details>
