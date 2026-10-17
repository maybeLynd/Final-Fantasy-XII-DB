---
title: "Message windows: the script's eight window slots, the text window and its choice lists, the message log, window pictures and the obtained-item notice"
kind: "system"
category: "Menus and HUD"
addresses: "0215F200, 002E16B0, 002E09A0, 002E08C0, 002A2C00, 002A6190, 0209C4D0, 0209C510"
---

## What the player sees

- Conversations and system messages appear in text windows. Text types out, and a cursor at the end of a page waits
  for the confirm button; pressing confirm while the text types shows the rest of the page at once.
- A window can end in a list of choices. Up and Down move the cursor, Triangle with Up or Down jumps to the first or
  last choice, and cancel moves the cursor to the choice the script names as the cancel answer.
- In a conversation window, Triangle opens the message log: the window's earlier pages can be scrolled back through
  and cancel closes the log again.
- Small signals beside the window show which button continues, and some windows show small animated pictures.
- When something is obtained, a "You obtain ...!" window or a battle-log line names it.

## How it works

### The script's eight slots

A script owns eight message slots, records of `0x68` bytes at `0215F200` (layout below). Every setter clamps the
slot number to 0-7 before use (`002E1D10`, `002E1F80` and the others below). The verbs fill a slot's settings first and
then open its window with `002E16B0`; the settings apply to the next window opened in that slot.

| Verb | Id | Setter | What it sets |
|---|---|---|---|
| `mesopenspeed`, `mesopenspeed_1b` | `0x1A`, `0x1B` | `002E1D10` | the run lengths, each the value times 33 ms or a negative value kept: `mesopenspeed` (`00350B50`) sets the opening run `+0x30` and writes -1 to the closing run `+0x34`; `mesopenspeed_1b` (`003510D0`) sets both |
| `askpos`, `debug_mesask_43` | `0x13`, `0x2043` | `002E1D50` | the choice list's start row `+0x24`, cancel row `+0x28` and cancel switch `+0x39`, with the flag `+0x3B` |
| `setaskselectignore` | `0x475` | `002E20D0` | sets or clears bit n of the hidden-choices mask `+0x18` |
| `setmeswinactive` | `0x476` | `002E2160` | bit 0 of `+0x44`: the next window opens without taking the focus |
| `setmeswinhidestatus` | `0x3D3` | `002E21E0` | on the open window: 2 sets bit 20 of its `+0x40`, any other value clears it (`002A31F0`) |
| `setmesmacro` | `0x1A8` | `002E1B70` | entry n of the slot's 32 macros at `0215F540 + slot x 0x100`: a kind and a value |
| `updatemesmacro` | `0x1A9` | `002E22A0` | re-reads macro n into the open window (`002A30B0`) |
| `shapewin`, `debug_meswinrect`, `mes`, `aask_1ff` | `0x17C`, `0x2020`, `0x461`, `0x1FF` | `002E1F80` | the window rectangle `+0x10`-`+0x16`, with the flag `+0x3A` |
| `shapewin` | `0x17C` | `002E1FD0` | `+0x42`: the window gets picture parts |
| `mes`, `aask_1ff`, `shapewin`, `debug_mesask_43` | | `002E1EA0` | the window style `+0x3D` (0-4) |
| `mes`, `aask_1ff` | | `002E1F40` | the window kind `+0x3C` |

Verb names and ids are those of the [verb table](../Scripts-And-Script-Commands/verb-table.md). `messync` and
`messync2` (`0x11`, `0x129`) set bit 1 and bit 0 of `+0x3E` (`00357820`, through `002E1E70` and `002E1E40`).

### Opening a window

`002E16B0(actor, slot, text, font)` builds a creation request from the slot and the text, and creates the window
(`002E194A`):

1. With an actor, it sets the actor's name-id bit through `0032ABF0` (`002E16EB`).
2. The window kind `+0x3C` becomes the request's kind through `002E11B0`: 1-15 stay, -5, -4 and -3 become 14, 13 and
   15, -1 becomes 16 (the conversation window), any other value 0. The old kind is kept at `+0x40` and `+0x3C`
   becomes 1 (`002E17AD`-`002E17B1`).
3. A set rectangle (`+0x3A`) with a width and height of 1 or more is used as given; otherwise the request asks for an
   automatic size (`002E17C2`).
4. With `+0x30` 0 or above the opening run is `+0x30` and the closing run `+0x34`, or the opening run when `+0x34`
   is negative; with a negative `+0x30` both are 132 ms (`002E17CF`-`002E17F0`). So after `mesopenspeed` a window
   closes as fast as it opens. A window of kind 0 opens and closes at once (`002E177E`).
5. If the slot still holds a window, a kind -1 window takes the new text as a further page (`002A35B0`, which adds it
   through `002A3250`); any other window is closed and destroyed first (`002E1846`-`002E18A5`).
6. After creation: with `+0x42` set, `002A2AD0` gives the window `+0x56` picture parts (16 by default);
   with `+0x3B` set, `002A3210` applies `askpos` (`002E1952`-`002E1987`).
7. The slot is reset for the next use: state 1, the answers `+0x0C` and `+0x2C` -1, the flags, the mask, the run
   lengths and the 32 macros cleared (`002E198C`-`002E1A25`).

`+0x3F` keeps the value `002640D0` reads from the current actor manager (`[02099D70]+0x28`).

### Slot states

Each tick the request drain `002E09A0` ([frame update order](../Engine-Core/frame-update-order.md)) steps
every slot whose state is not 7. `002A2A60` reads the window's pager state, the low byte of the window's `+0x180`, and
answers 1 while text is still running (pager states 0, 3, 5 and 7), 3 while a choice list is open (2 and 4) and 2
once the page is done (1, 6 and any other); for pager states 2, 4 and 6 it also returns the cursor or the answer (window `+0x124`).

| State | Set by | Means |
|---:|---|---|
| `1` | `002E16B0`; the drain on answer 1 | the text is running |
| `2` | answer 2 with `+0x3E` bits 0 and 1 clear; with bit 0 set, the tick after state 3 | done, the window stays |
| `3` | answer 2 with bit 1 set; with bit 0 set, a confirm press (`002A29A0`, `002E0B35`-`002E0B4D`); a choice slot on answer 2 | done and acknowledged |
| `4` | answer 3 | a choice list is open |
| `6` | the close paths | closing |
| `7` | the close paths; `002E1130` answers 7 for an empty slot | no window |

A slot whose byte `+0x38` is set is a choice slot; `mes` and `aask_1ff` store it from the text section's flag
([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)). While the list is open the drain copies the
cursor to `+0x2C`; on answer 2 it copies the answer to `+0x2C` and `+0x0C` once, guarded by `+0x41`
(`002E0AE3`-`002E0B19`).

`002A2A60` returns only 1, 2 or 3, so the drain's arms for 0, 4 and other answers, which write states 0, 5 and 8,
are not taken (`002E0AB1`-`002E0AD2`). `002A29A0` answers the confirm button whenever a window is skipping
(`+0x3C5` negative) and 0 while the log of a focused window is open.

The getters the verbs read are `002E1130` (the state), `002E10F0` (`+0x0C`), `002E1080` (`+0x2C`, read by
`mesisselect`), `002E1170` (`+0x40`, read by the `aask_1ff` poll `0034BDC0`) and `002E10C0` (bit 0 of `+0x3E`).

### Waiting on a window

`messync`'s poll `00348920` calls `00357790`, which keeps the script waiting by answering 1
([native commands](../Scripts-And-Script-Commands/native-commands.md): a poll that returns odd keeps waiting):

- state 3 with `+0x3E` bit 0 clear: 0, the script goes on and the window stays;
- state 3 with bit 0 set: the window is closed with `002E08C0` and the wait goes on;
- state 6: it waits only when the call's own flag byte `+0xD` is set;
- state 7: 0;
- any other state: 1.

It also sets `022C7F88` to 1 (`0035780F`).

### Closing

`002E08C0(slot)` closes a slot's window: it starts the window's closing run (`002A2720`), sets state 6, calls
`002F1C50([0215F1B6])` when `+0x40` is -1, and writes `0xFE` to `+0x40`. Once the window reports its run over
(`002A28B0`, bit 9 of its `+0x40` clear), the drain destroys it with `002A2830`, clears the slot and sets state 7
(`002E0A2E`-`002E0A64`).

`002E06F0` closes all eight slots the same way. The script unload `0032ED80(n)` calls `002E0780(n)`, which closes and
destroys at once every window whose `+0x3F` is n (`0032EEBF`).

`002A2720(window)` starts the closing run (`00244DD0`) unless bit 20 of `+0x40` or bit 5 of `+0x7C` is set, and, for a
window that keeps a log, clears the log rows (`0209C700`, `0x280` bytes) and the published text `0209C980`/`0209C988`.
`002A27C0` asks a window to close: it sets bit 6 of `+0x40`, then runs the closing run when bits 0 and 5 are set and
otherwise sends message 15 and destroys it at once (`00245020`). `002A27F0` closes with a run of 1 ms, which is 0
frames.

### The window object

`002A2C00(request)` builds the window as a `0x410`-byte widget with procedure `002A6190` (`002A2C10`). Message 1
registers it in the first free entry of the eight pointers at `0209C4D0` and keeps the index at `+0x3B8`
(`002A6202`-`002A623E`). Every entry point first checks that the entry still holds the window (`002A2720`,
`002A27C0`, `002A2830`, `002A28B0`, `002A2BB0`).

Message 18 clears the entry only for an index of 6 or below (`002A695B`), so a window registered in entry 7 stays
there after it is destroyed. A scan of the listed functions for rip-relative and image-base-relative operands on
`0209C4D0`-`0209C50F` finds two other writers: the register `002A6236` and the reset `002A79E0`, which the startup
step `00253970` runs once and which also clears the eight picture slots at `0209C510`.

`002A2BB0` answers 1 while a live window has a procedure or a run in progress. `002A3090` builds a window for the
obtained-item notice and the talking-message host (`0035E4C5`, `00474271`).

### What the window procedure does

| Message | Arm |
|---:|---|
| `1` | register (above) |
| `2` | per tick: the mode step `002A7720`, the conversation window's signals, the log scroll `002A5930`, the parts `002A3F90` |
| `3` | when bit 22 of `+0x3E8` is set (kind 14, `002A70B0`), a box through `00392A00` in colours `0x54`-`0x57` of the colour table `002DD7E0` |
| `4` | draws the text (`002A4430`, or `002A4830` in the log), then the parts (`002A4EE0`) and the caption (`002A4170`) |
| `10` | input: after `+0x3BC` ticks of delay, `002A5CC0` in mode 0, `002A5F40` in the log; a caption window with bit 18 closes on confirm (`002A66D0`) |
| `12` | the choice list's cursor, confirm and cancel (below) |
| `15` | closing: the signals close (`002A8410`) and so does the mask |
| `18` | destroyed: parts freed (`002A2860`), signals destroyed (`002A84F0`), mask destroyed, entry cleared |
| `21` | the mask follows the window |

Message ids are those of [widget messages](widget-messages.md).

### Typing and the page end

The window's text runs in the text context at `+0xD0`, the same context the confirm window uses. Its kind byte
`+0xA3` picks three handlers from the table at `009164C0`: kinds 0 and 1 have the input `002A9980` and the pager
`002A8C50` ([text codes](text-codes.md)); kind 2, which `002B3400` sets for plain menu text, has none. `002B3930`
jumps to the kind's input handler, and `002ABEC0` and `002ABF20` to its pager after copying the shown count `+0x8C` to
the painter's `+0x10D8`.

`002B1E20(text, speed)` sets the type-out: 0 sets the shown count `+0x8C` to the length `002B43C0` measures, so the
page shows at once; 1-30 is the rate `+0x9C` itself; a larger value is rate 30 with a step `+0xA0` of value / 30,
halved (at least 1) outside the field frame. In mode 0, confirm with no wait pending (`+0x54` of the text 0) calls
`002B1E20(text, 0)` (`002A5EFB`).

The page-end cursor bobs by the offset `+0x3DA`, which `002A40B0` alternates (`002A46D0`):

```python
phase 0: offset 0, lasts 40 / n + 2 ticks
phase 1: offset 4, lasts 8 / n + 2 ticks
n = 2 in the field frame (main state 2), 1 otherwise (00248F20)
```

`002B2D60` hands the drawer the cursor's box while the pager state is not 0.

### Choice lists

A string with a choice list (token `0x0E`) gets a list widget at `+0xC0`: `002A5590` parses the list and builds it with
`002D14E0`, with the row painter `002A1B00` (`002A5836`-`002A5855`). The painter finds the row's option text with
`002B2D90` and draws it from the scratch `0209CB90` through `002D89E0`.

Options whose bit is set in the text's mask `+0x84` are left out. `002B2D20` counts the shown options, `002B2CA0` turns
an option number into its row and `002B2CE0` a row into its option. The mask is the slot's `setaskselectignore` bits:
`002A6A80` passes the request's `+0x24` to the text set-up `002B32D0`, which stores it at `+0x84` (`002A6AF7`,
`002B3310`). The confirm windows set up their text through `002B3280`, which passes its arguments on to `002B32D0` with the
last two set to 0 (`002B3284`-`002B32B6`).

When the list starts (`002A9066`), the start row is option `+0xA4` and the cancel row `+0xA5`, from the token, or from
`askpos` when bit 17 of `+0xB0` is set; `002A3210` sets that bit and copies the cancel switch to bit 18. In the list:

- Up and Down move one row and wrap round only on a fresh press; with Triangle held they jump to the first or last
  row (`002B3B20`). A move plays sound 1, a jump `0x17`.
- Confirm plays sound 2, ends the list (pager state 6) and leaves the option at `+0x54` (`002A9D05`-`002A9D32`).
- Cancel with bit 18 set plays 3 and moves the cursor to the cancel row without answering; with no
  cancel row it plays 5 (`002A9D3A`-`002A9D9C`).

The window answers the list's messages (`002A66E7`-`002A6801`): `0x8000` keeps the option under the cursor at
`+0x124`, `0x8001` sets pager state 6 with that option, and `0x8002` gives the list its cancel mode in `+0xFE` (`0xFF`
without bit 18, 3 with a cancel row, after moving the list there with `002D4840`, and 5 without one).

### The message log

A conversation window (kind 16, bit 12 of `+0x3E8`) keeps its pages as rows of `0x28` bytes at `0209C700`, unless bit 14 is set (`002A733A`-`002A735C`). Its mode is
bits 8-10 of `+0x3E8`:

1. In mode 0, while the text is not typing, Triangle pressed without cancel opens the log (`002A5CC0`) when the
   window has earlier text: the cursor `+0x3C0` goes to the last of the `+0x3C1` rows, the scroll `+0x3BE` to that
   row (`002A5020`), the mode to 1, and sound `0x4E` plays (`002A5E7C`).
2. Mode 1 waits until the window's position and size tweens end, sets mode 3 and fades the mask to colours
   `0x67`/`0x68` over 80 ms (`002A3DF0(1, 0x50)`, `002A7783`).
3. In mode 3, Up or Triangle moves to an earlier row and Down or confirm to a later one (`002A5F40`), each move a
   12-frame scroll with curve 1 through `0209C618`-`0209C628` that `002A5930` steps.
4. Cancel, when no scroll runs, sets mode 2 and plays sound 3; mode 2 sets mode 0, fades the mask back to
   `0x69`/`0x6A` and restores `0209C980` from `0209C988` (`002A77DE`).

`002A3DF0(open, ms)` tweens the mask's two colours from their current values over `ms x 60 / 1000` frames, and does
nothing when they already match. `002A69E0` resizes the window's height to its text, at least three lines, with a
150 ms tween that keeps the bottom edge (`00247260`); `002B27E0` and `002B28B0` measure the height of the text shown.

`002B27E0` cuts the text with `002B20B0(text, n)` (`002B280B`). That walks the text a token at a time (`002B1FB0`),
adding each token's `002B41F0(token, 0)`. It returns the byte offset where the sum has reached n and the next byte
is `0x10` or above, or where the text ends. `002ABB20` also calls it (`002ABCEC`).

### Signals

A conversation window shows up to three small signal widgets, procedure `002A86A0`, kept at `0209CC18`, `0209CC20` and
`0209CC28`:

| Widget | Built by | Shown | Placed by |
|---|---|---|---|
| right signal `0209CC18` | `002A8220` | any kind but 0 | `MsgWinSignalRightOffset` |
| left signal `0209CC20` | `002A7F70` | kinds 4-6 | `MsgWinSignalLeftOffset` |
| log signal `0209CC28` | `002A8100` | while the log is open | `MsgWinLogSignalPosX`, `MsgWinLogSignalPosY` |

The kind comes from `002A7ED0`: 4 in the log, the text's own value `+0xAE` (escape `0F =`) when it is set, and
otherwise from the pager state and whether the window has a log. `002A8550(kind)` measures the signal's label, the
template text `0x467C` with a button from `0029DA70`. A signal is replaced when its kind changes and closed with
`002A84B0`; `002A8410` closes them and `002A84F0` destroys them with the window. Their layout keys are listed on
[screen layouts](screen-layouts.md).

### Window pictures

Scripts register a picture with `registshape` (`0x17A`): `002A7950` takes the first free of the eight `0x20`-byte
picture slots at `0209C510`, loads the picture as the image label `shape` (`0024A440`) and returns the slot.
`002A7A40` frees a slot. A window with parts has an array of `0x60`-byte parts at `+0x3F8`, its count at `+0x3F0`
and a draw order at `+0x400`, made by `002A2AD0` with each part hidden, colour `0x80808080` and scale 1.0.

| Verb | Id | Function | Does to a part |
|---|---|---|---|
| `setshape` | `0x17E` | `003E9320` → `002A3650` | shows a picture's group and frame, then sets the position and centring (`003E9570`) |
| `setshapeanime` | `0x17D` | `003E9440`, `003E9320` → `002A3830` | stores the animation in the slot (`+0x46`-`+0x50`, `+0x4C` = 1), then runs frames from the first to the last with a delay and a loop count |
| `setshapecolor_18a` | `0x18A` | `003E94D0` → `002A2650` → `002A7C70` | sets the colour, or tweens it over n ticks with a curve |
| `setshapescale_187` | `0x187` | `003E9690` → `002A26A0` | sets the scale, or tweens it over n ticks with a curve |

`003E9320` uses `002A3830` whenever the slot's `+0x4C` is set, so after `setshapeanime` a later `setshape` on the
same window animates too (`003E9377`). `002A7A60` reads a frame's box and palette from the picture's tables. Each tick `002A3F90` steps every part with
`002A7AD0`: the frame timer, the colour tween and the scale tween, each through `00248F40` ([widgets](widgets.md)).
A loop count of 0 loops for ever. The parts do not step while a time stop restricts anything (`00226BA0`) and story
flag `0x6F` is clear ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).

`002A5BC0` sorts the draw order by each part's priority byte `+0x0E`, highest first, when `+0x3F2` asks for it, and
`002A4EE0` draws the shown parts in that order, centred when bit 1 is set. `002A2860` frees the arrays.

### Skipping

While any actor-manager slot has a skip pending (`00267310` for slots 0-4), the drain calls `002A38C0(1)`
(`002E09DD`). For every window, `002A3730` marks the text window as skipping (`+0x3C5` = `0x80`) and steps its pager
until a page end, a choice list or an answer, and `002A36A0` finishes every part's animation and tweens at once
(`002A7D30`) and freezes the parts (bit 7 of `+0x3F3`). `002A38C0(0)` clears the freeze and `+0x3C5`.

`002A3730` also calls `002B3950(text)` (`002A37C9`). It moves the page counter `+0x8C` on by one, keeping the old
value at `+0x8E` and the new one at `+0x90`. It clears `+0x88`, the low byte of `+0xB0` and bit 19 of `+0xB0`, and
sets `+0x9B` and `+0x9D` to 1.

### Captions and sizes

Kinds 13 and 14 build caption windows (bit 13 of `+0x3E8`) with `002A70B0`. A kind 14 window matches its width to the
other caption window `002A3F50` finds, and `002A4030` widens a caption window and its two frame parts. `002A5460`
measures a caption's text plus 4, and `002A5520` gives the y of a style-3 caption: `0028F810`, or the screen height
`01E0C1DC` when that is negative, less 5 font sizes and 38 times `0024ABA0`. `002A6F80` places the caption window of
style 0 or 3.

`002B39A0(text, c)` returns the first byte c in a zero-terminated string, or null; the message windows (`002A3250`,
`002A5590`, `002A6C40`, `002A70B0`) and the Clan Primer (`00573BE0`) use it. `002B39D0` and `002B3A80` find a string inside
the window's text, the second stopping at a given character
(`002A2E52`, `002A3438`).

### The letterbox mask

The conversation window builds a mask widget, procedure `002A3960`, stored at `0209C610` (`002A70B0`). Message 21 keeps
it from `MessageWinMaskTop` above the window's top edge to the bottom of the screen (`002A68AF`-`002A68FA`), and the
window's messages 15 and 18 close and destroy it. Its layout keys are on [screen layouts](screen-layouts.md).

### Hiding windows with the HUD

The HUD switch `00251F40` ([HUD](hud.md)) hides and shows windows with the rest of the HUD:

- `0035D0E0` walks the widget tree from `0208EA28` (`0035D280`) and starts the closing run (`002A2720`) of every
  window with parts (`+0x44` bits 19-20 equal to `0x100000`, set by `002A2AD0`) whose `+0x40` bit 20 is clear
  (`0035E5C0`). With bit 7 of `[020927EC]` it takes every window with parts (`0035E5A0`) and then every text window
  (`0x180000`, `0035E580`). It then marks slot 6's window inactive (`002E2010(6, 0)`).
- `0035D1B0` reopens them the same way (`0035D2D0`, `00246AC0`) and marks slot 6's window active (`002E2010(6, 1)`).

`002A2720` itself skips a window whose `+0x40` bit 20 is set, so `setmeswinhidestatus(slot, 2)` keeps a window up
while the HUD is off.

### Message macros

Each window holds 32 resolved macros at `+0x1B8`, `0x10` bytes each, made from the slot's macro table when it is built
(`002A2D95`) and again by `updatemesmacro`. The text's `+0x70` points at them (`002A6AD4`), and the escape `0F .`
reads its argument from there (`002AD8F9`). `002A30B0(window, n)` resolves entry n by its kind:

| Kind | Becomes |
|---:|---|
| `0` | the number |
| `1`, `2` | the name of `0035D330(1, value << 16)` |
| `3`, `4`, `6` | the name of `0035D330(0x14, value)`, `0035D330(2, value)`, `0035D330(0x19, value)` |
| `5` | the string `003153F0(value)` |
| `15` | the raw value |
| other | nothing |

The escape is listed on [text codes](text-codes.md).

### The obtained-item notice

`002A59C0(ids, gil, count, times, log, flag)` fills the one notice record at `022CA438` (`0035E550`), which
`0035E560` clears first, with up to three lines through `0035E500`, and posts it with `0035DF40`:

- with `gil` 1, one gil line;
- otherwise by the id's class (`00309440`, [item and ability ids](../Engine-Core/item-and-ability-ids.md)):
  classes 5-12 and 17 give one line with the count `times` for a single id and nothing for a list;
- key items (13) give one line, or a line per id with count 1 for a list, and are never written to the battle log
  (bit 0 of `+0x08`, `002A5B69`, `002A5B82`);
- reward packages (14) give their gil and up to two item lines from `0030AEA0`, each times `times`;
- any other class gives nothing.

`0035DF40` writes battle-log lines through `0046AA70` when `log` was set ([battle log](../Battle-Actions/battle-log.md))
and otherwise builds the "You obtain ...!" window `0035E070` when none is open (`022CA430`). `002A3060(item, count,
log)` is the single-item entry the item verbs use ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)),
and `002A5B90(ids, count)` the list entry (`003F3F6B`).

## Layouts

`MessageSlot`, the script slot record, `0x68` bytes, eight of them at `0215F200`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | window | the open window widget, 0 for none |
| `+0x08` | `i32` | state | slot state, above |
| `+0x0C` | `i32` | answer | the chosen option, -1 until chosen |
| `+0x10` | `i16[4]` | rect | x, y, width, height |
| `+0x18` | `u32` | hidden | hidden-choices mask |
| `+0x1C` | `i32` | req1C | its low byte goes into the creation request; the reset writes -1 |
| `+0x20` | `i32` | req20 | its low byte goes into the creation request; the reset writes 0 |
| `+0x24` | `i32` | startRow | `askpos` start row |
| `+0x28` | `i32` | cancelRow | `askpos` cancel row |
| `+0x2C` | `i32` | cursor | the cursor or answer, -1 until set |
| `+0x30` | `i32[2]` | runMs | opening and closing run lengths, -1 for the default |
| `+0x38` | `u8` | choice | choice slot |
| `+0x39` | `u8` | cancelOn | `askpos` cancel switch |
| `+0x3A` | `u8` | rectSet | the rectangle is set |
| `+0x3B` | `u8` | askSet | `askpos` was used |
| `+0x3C` | `i8` | kind | window kind for the next window |
| `+0x3D` | `u8` | style | window style 0-4 |
| `+0x3E` | `u8` | sync | bit 0 and bit 1 from `messync` |
| `+0x3F` | `u8` | owner | the value `002640D0` read at the open |
| `+0x40` | `i8` | lastKind | the kind of the open window; `0xFE` after a close |
| `+0x41` | `u8` | answered | the answer was copied |
| `+0x42` | `u8` | hasParts | the window gets picture parts |
| `+0x43` | `u8` | flag43 | the reset writes 0 |
| `+0x44` | `u8` | noFocus | bit 0: open without the focus |
| `+0x4C` | `u8` | flag4C | the reset writes 0 |
| `+0x54` | `u16` | partsBuilt | the part count given to `002A2AD0`, 0 for a window without parts |
| `+0x56` | `u16` | partCount | parts for a shape window, 16 |
| `+0x58` | `u16` | req58 | copied into the creation request |
| `+0x5C` | `u8` | req5C | copied into the creation request with the style `+0x3D`; the reset clears `+0x58`-`+0x5F` |

`PicturePart`, `0x60` bytes, the array at `+0x3F8` of a window with parts:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `PictureSlot*` | picture | an entry of `0209C510` |
| `+0x08` | `u32` | flags | bit 0 shown, 1 centred, 2 frames running, 3 colour tween, 4 scale tween; bit 5 is set on every part when it is built (`002A2AD0`) |
| `+0x0D` | `u8` | palette | from the frame when `0xFF` |
| `+0x0E` | `i8` | priority | draw order, highest first |
| `+0x10` | `i16[2]` | pos | x, y |
| `+0x14` | `i16` | group | picture group |
| `+0x16` | `i16` | frame | current frame |
| `+0x18` | `u16[4]` | box | the frame's atlas box |
| `+0x20` | `u8[4]` | colour | RGBA |
| `+0x24` | `f32[2]` | scale | x and y |
| `+0x2C` | `u8` | loops | loops left, 0 for ever |
| `+0x2D` | `u8` | timer | ticks to the next frame |
| `+0x2E` | `u8` | delay | ticks per frame |
| `+0x2F` | `u8` | last | last frame |
| `+0x30` | `u8` | first | first frame of the loop |
| `+0x34` | `u8[4]` | colourFrom | colour tween start |
| `+0x38` | `i16[4]` | colourBy | colour tween change |
| `+0x40` | `i16[3]` | colourTime | tick, length, curve |
| `+0x48` | `f32[4]` | scaleTween | x start, x change, y start, y change |
| `+0x58` | `i16[3]` | scaleTime | tick, length, curve |

`PictureSlot`, `0x20` bytes, eight at `0209C510`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | used | bit 0 |
| `+0x08` | `void*` | image | the image label `0024A440` made |
| `+0x10` | `u8*` | groups | the picture's group table |
| `+0x18` | `u8*` | frames | the picture's frame table |

## Modding notes

- `mesopenspeed` values are stored in 33 ms units, but the window keeps run lengths in ten bits of `+0x7C`:
  bits 12-21 take `open & 0x3FF` and bits 22-31 `close << 22` (`002A2FAF`-`002A2FDF`), so values above 31
  (31 × 33 = 1,023 ms) wrap round.
- The eighth simultaneous window (registry entry 7) is not removed from the registry when it is destroyed; the entry
  keeps pointing at the destroyed widget, which the loops over `0209C4D0` (`002A28E0`, `002A29A0`, `002A38C0`,
  `002A3F50`) still read until the reset.
- Hidden choices keep their option numbers: `askpos` and the answer use option numbers, which `002B2CA0` and
  `002B2CE0` convert to and from rows.

## Related

- [Text codes](text-codes.md) - the codes inside the window text, the choice list token and the pager escapes.
- [Widgets](widgets.md) - the widget object, runs, tweens and focus the window is built on.
- [Screen layouts](screen-layouts.md) - the MsgWin, MessageWin and Talking layout keys.
- [Dialogs](dialogs.md) - the confirm window, which uses the same text context.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md) - the message verbs and their handlers.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - where the window text comes from.
