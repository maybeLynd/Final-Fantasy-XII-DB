---
title: "Widgets: how every menu element is built, sized, attached, focused, animated and torn down"
kind: "system"
category: "Menus and HUD"
addresses: "0x002465F0, 0x00244F50, 0x00245000, 0x00248220, 0x00248030, 0x00244640, 0x00246AD0, 0x00245020"
---

## What the player sees

- Every menu, window, list and gauge is a widget: it opens with a short slide or fade, answers input while it has the
  focus, and closes with the reverse animation.
- Animations take the same time at any frame rate setting, because their durations are given in milliseconds.

## How it works

### Construction

Every widget is built by `0x002465F0(object, size, procedure, record, borrowed)`:

1. It clears the object (`0x00246612`-`0x00246626`).
2. It installs the procedure at `+0x00`, or `0x005C5230` (`xor eax, eax` / `ret`) when none is given
   (`0x0024662B`-`0x00246641`).
3. It writes the header (below).
4. It calls the procedure once with message 1 and the creator's two arguments (`0x00246721`-`0x00246748`).

There are three ways in:

| Entry | Does |
|---|---|
| `0x00244F50(size, procedure, record)` | the factory: size 0 becomes `0xC0`; up to `0x120` bytes it takes a free slot of the 112-slot pool at `*0x0208EA58` (`0x00244F7F`-`0x00244FAE`), otherwise or when the pool is full it allocates from the heap (`0x002497B0`) |
| `0x00245000(object, size, procedure, record)` | builds in memory the caller provides, usually inside the parent |
| `0x002465F0` directly | 7 sites, in `0x00241BF0`, `0x00241C90` and `0x00247AE0` |

A pool or in-place widget is marked borrowed (`+0x40` bit 14): the release then frees only the pool slot
(`0x002483E5`-`0x002483F0`), while a heap widget is freed (`0x002483DE`).

### Sizes

Over the image there are 296 construction sites in 235 functions, building 267 procedures at 83 sizes, from `0xC0` to
`0x179E0`. No procedure is built at two sizes, so a widget's size identifies its type.

| Size | Procedure | Widget |
|---|---|---|
| `0x61F0` | `0x00279E20` | the battle menu ([Battle menu](battle-menu.md)) |
| `0x179E0` | `0x002B7590`, `0x002BA700`, `0x003CB650` | the map containers ([Map screens](map-screens.md)) |
| `0xBC08` | `0x002B7B80`, `0x002BAF80` | the map pages |
| `0x640` | `0x0057C480` | the confirmation window ([Dialogs](dialogs.md)) |

A parent can hold its children inside itself: the battle menu builds two `0x3010` panels at `+0xC0` and `+0x30D0`, the
Dismiss confirmation in a panel slot, and the `0xD0` target tabs at `+0x60E0`, all with `0x00245000`
(`0x0027A12F`-`0x0027A42D`).

### The header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32[2]` | proc | procedure(self, message); `0x005C5230` when none |
| `+0x08` | `u32[2]` | cont | continuation the release jumps to after freeing (`0x00248405`) |
| `+0x10` | `u32[2]` | parent | set by the attach `0x00248220` (`0x00248267`) |
| `+0x18` | `u32[2]` | child | first child (`0x00248239`) |
| `+0x20` | `u32[2]` | next | next sibling (`0x0024825C`) |
| `+0x28` | `u32[2]` | prev | previous sibling (`0x00248260`) |
| `+0x30` | `u32` | nchild | number of children (`0x00248264`) |
| `+0x38` | `u32[2]` | draw | draw record while the draw pass is on this widget |
| `+0x40` | `u32` | flags | below; `0x80A` plus the generation and borrowed bits when built (`0x00246653`) |
| `+0x44` | `u16` | w44 | 100 (`0x002466FA`) |
| `+0x48` | `u32[2]` | trans | animation descriptor, default `0x00915198` (`0x00246687`) |
| `+0x50` | `u32` | flags2 | bit 0 clip, bit 1 owns the array at `+0x60` |
| `+0x60` | `u32[2]` | arr | array freed by the release (`0x0024838A`) |
| `+0x68` | `u32[2]` | half | the descriptor half of the current run |
| `+0x70` | `u32` | frames | run length in frames |
| `+0x74` | `u32` | start | frame the run started (`0x0208F570`) |
| `+0x78` | `u32` | t78 | 0 forward, 1.0 backward |
| `+0x7C` | `u32` | state | low nibble: run state 0-4 |
| `+0x80` | `u32` | tween | bits 0-2: tween channels running |
| `+0x98` | `u16[2]` | pos | tween channel 0 output |
| `+0x9C` | `u16[2]` | ext | tween channel 1 output |
| `+0xA0` | `u8` | alpha | `0x80` when built |
| `+0xA1` | `u8` | rgb | `0x80` when built |
| `+0xA2` | `u8` | slot | pool slot marker; 0 frees it (`0x002483E9`) |
| `+0xB4` | `u32` | phase | half-rate phase counter |
| `+0xB8` | `f32` | rate | 1.0, or 1 / steps at game speed (`0x00246B49`) |

| `+0x40` bit | Meaning |
|---:|---|
| 0 | active (`0x002473F0`) |
| 1 | may be activated |
| 3 | can take the focus (`0x002481D8`) |
| 4 | has the focus (`0x00244865`) |
| 5 | passed to children on attach (`0x00248271`) |
| 6 | close requested (`0x00244F0A`) |
| 7 | the byte offsets at `+0xA4`-`+0xAD` move the draw box (`0x00246480`) |
| 9 | a run was started |
| 10 | release deferred to the next tick (`0x00245097`) |
| 13 | has had a child attached, or a child's priority changed: the children are re-sorted (`0x00244990`) |
| 14 | borrowed storage |
| 15 | use the default animation descriptor |
| 17 | generation parity |
| 18 | skip the per-tick update |
| 24 | drawn in the second draw pass (`0x00247730`) |
| 27 | `+0xAE`/`+0xAF` also widen the draw box |

### The tree

`0x00244960(parent, child)` attaches a child only when it has no parent yet, through `0x00248220`
(`0x00244960`-`0x00244965`), which appends it to the parent's children, links the siblings, counts it and stores the parent
(`0x00248230`-`0x00248267`). An active parent activates an attached child that may be activated (`0x002473F0`, which sends
message 6, `0x002482AE`-`0x002482C7`). A parent with bit 5 passes it to the child and to every descendant of the child
through the pre-order walker `0x002463F0(widget, callback, value)` with the bit setter `0x002418E0` (`0x00248271`-`0x002482A0`).

Two shortcuts use the main root `[0x0208EA28]`:

- `0x00246AC0(widget)` opens a widget under it (`0x00246AD0`).
- `0x00247950(widget, on)` attaches a widget that has no parent to it with bit 1 set to `on`. For a widget that has a
  parent it sets bit 1 to `on` through `0x00247870`, which also runs the activation `0x002473F0` when bit 5 is set
  (`0x0024795C`-`0x0024797A`).
- `0x00247980(parent, widget, on)` does the same under a parent the caller gives; `0x00228130` calls it.

Messages travel along the tree:

- `0x00275440(widget, message)` delivers to every ancestor in turn, up to the root (`0x00275452`-`0x00275477`).
- `0x002753F0(widget, message)` delivers to the widget and then every descendant (`0x002753FA`-`0x00275427`).

The message record and every id are in [Widget messages](widget-messages.md).

### Draw order and the two draw passes

`0x00247930(widget, priority)` stores a widget's draw priority at `+0x44` (100 when built) and sets bit 13 on its
parent. When the walker `0x00244980` reaches a widget with bit 13, it re-sorts that widget's children with `0x002479B0`
and clears the bit (`0x00244990`-`0x0024499F`):

1. Each child's priority, position in the list and pointer go into the scratch table `0x0208ED60`
   (`0x00247A0A`-`0x00247A2D`).
2. The sort `0x00249CE0` orders them with the comparator `0x00244610`: a larger priority first, equal priorities in
   their old order. `0x00249CE0` jumps to `0x00249680(scratch, base, size, n, compare)`, an insertion sort that
   takes each element in turn into `scratch` and moves larger ones up by `size` bytes.
3. The children are relinked in that order (`0x00247A51`-`0x00247AB1`).

The root draw passes `0x002450B0` and `0x00245110` set `0x0208F564` to 0 and to 1 and walk the tree with `0x00245E60`. A
widget's own content is drawn only in the pass equal to its `+0x40` bit 24, with bit 28 clear (`0x0024623A`-`0x0024624B`);
its box is drawn in that pass when `+0x40` bit 7 is also set (`0x002461BB`-`0x002461CE`).
`0x00247730(widget, pass)` sets that bit on a widget and every descendant.

`0x00245E60` takes each widget's box from `0x00246480(widget, box)` (`0x00245F50`):

- the position and size from `+0x98`, an inner rectangle the size of the widget, scale 1.0 at box `+0x1C` and
  `+0x20`, and the alpha `+0xA0`;
- with bit 7, the signed bytes `+0xAC`/`+0xAD` added to the position, the inner offset from `+0xA4`/`+0xA5`, and
  `+0xA6`/`+0xA7` added to the inner size, plus `+0xAE`/`+0xAF` with bit 27;
- then the running opening or closing run, through `0x00244A20`.

It returns 1 when a float at box `+0x10`-`+0x18` is not 0 or the scale is not 1.0. `0x00246450` returns the position
alone, with the same bit 7 offset.

The box itself is a nine-piece panel. `0x00245E60` sets up a draw record (`0x002D8530`) and calls `0x002455A0` when
`+0x40` bit 8 is set, otherwise `0x00245170` (`0x002461D9`-`0x002461F0`). `0x00245170(widget, record)` draws nothing while
`0x002DD4B0()` (the dword `0x0215E6D0`) is 0. Otherwise:

1. It takes the atlas `0x0208EAA0` (`cm_win_c`), or `0x0208EAB0` with `+0x40` bit 22, and nine consecutive 8-byte
   pieces from the index its header gives at `+0x44`: `i16` x and y, then 12-bit width and height.
2. The middle column is the widget width `+0x9C` less the two corner widths plus `+0xA6`; the middle row the height
   `+0x9E` less the two corner heights plus `+0xA7`. The panel starts at `+0xA4`, `+0xA5`.
3. Its colour is `0x80808080` for a style byte `+0xA3` below 2, else colour-table entry `+0xA3 + 0x92`
   (`0x002DD7E0`); its palette byte is the first piece's byte `+7` for a style below 10, else `0x002DD7B0(+0xA3 +
   0x92)`.
4. It draws the nine pieces row by row with `0x002DA7C0` between `0x002DAF30` and `0x002DAC70`, leaving out the
   middle row or column when its size is not above 0.

`0x00272310(widget, out)` gives a widget's place on screen: its own box position
(`0x00246480`) plus that of every ancestor up the `+0x10` chain, for `0x003EE420` (`0x003EE511`, `0x003EE51F`).
`0x003EE420` also steps four fades of its object with `0x003EEBD0(object, up)` (`0x003EE6A4`). Each moves by
`1 / ([0x01DFE0B4] x 9600 / 1000)` and is clamped to 0-1: `+0x1D0` up when `up` is non-zero, `+0x88` up with `+0x1D4`
bit 8, and `+0x188` and `+0x1B8` up with `+0x1D4` bit 9; each goes down otherwise.

`0x003EEA80(block, kind, flag, element, fade)` draws the sprite records of the two `0x30`-byte blocks at `+0x170` and
`+0x1A0` of that object (`0x003EE612`, `0x003EE637`, with the fade `+0x1D0`), while the block's `+0x18` is positive:

- it scales the element's width word `+0x58` by `+0x18 x fade`, and puts the width and `+0x5C` back afterwards;
- for the one or (with `+0x1C` set) two 8-byte records at `+0x08` it takes x and y from words 0 and 1, u and v as the
  two 12-bit fields of dword `+0x04`, and byte `+0x07`: its high nibble picks a row of the picture's palette table
  (`[[block] + 0x20] + 0x30`, row `+0x12`) and its low nibble is added, giving element `+0x5C`;
- each record is drawn with `0x002D8CB0(element, [block], rect, kind, flag)`.

`0x003EE8C0(object, text, a, b)` sets those fades up for a new text. The object holds two 0x1E0-byte
text entries at `+0xC0`, and the index `+0x4B0` toggles between them:

1. It clears bits 8 and 9 of the old entry's `+0x1D4`, moves the index and sets both bits on the new one.
2. It copies up to 0x80 bytes of `text` into the entry (`0x00254F30`); a null or empty text leaves it empty.
3. It clears bit 9 again when `a` and `b` are both 0, zeroes `+0x1D0`, `+0x88`, `+0x188` and `+0x1B8`,
   keeps `a` at `+0x18C` and `b` at `+0x1BC`, and runs `0x002B3400(entry + 0xA0, 0, 0)`.

The battle menu's title writer `0x0027D480` (`0x0027D52F`) and `0x00298250` (`0x002984C0`, on its `+0xC0`) call it.

Two helpers set those offset bytes:

- `0x002476E0(widget, d)` adds the low bytes of the four words at `d` to `+0xA4`-`+0xA7` when bit 7 is set and bit 8
  clear; `0x002A70B0` calls it.
- `0x00247810(widget)` reads the three bits 16-18 of `+0x44`. With bit 18 clear it sets `+0xAD` to -7 when bit 17 is
  set and to 6 otherwise, and `+0xAC` the same way from bit 16; with bit 18 set it writes only the -7 values.
  `0x00227EE0`, `0x002A6A80` and the confirmation window `0x0057C480` call it.
- `0x002478D0(widget, on)` sets or clears bit 18, the per-tick skip, on a widget and every descendant (first child
  `+0x18`, next sibling `+0x20`); `0x00285290` calls it.

`0x00247780(on)` sets bit 0 of `0x0208ED58`. While it is set, both passes also call `0x00245510` for a root whose `+0xC0`
is 1, which hands the root's position and alpha to `0x00367940` (`0x002450D7`-`0x002450F5`, `0x00245137`-`0x00245149`); the
first pass does so only while `0x0208F568` is 0. The script verbs `fsmenu_showcursor` and `fsmenu_hidecursor` set and
clear the bit (`0x00510964`, `0x005109A3`).

### The per-tick update and the input turn

Five UI tick functions (`0x00250540`, `0x002506D0`, `0x00250730`, `0x002507C0`, `0x002508E0`) each flip the parity `0x0208ED5C`
(`0x002481A0`) and run the drain `0x00248030` over the root widgets:

1. A widget with bit 10 set is released (`0x00248086`-`0x00248097`).
2. Every other widget gets message 2 unless bit 18 is set, and its generation bit is restamped (`0x002480DB`-`0x00248110`).

`0x002284F0` also runs the drain (`0x0022865C`). So message 2 reaches every live widget once per UI tick. The same ticks give the focus widget its input turn
(`0x002481C0`): message 10, or 11 when a widget up its parent chain has bit 9 set (`0x002481D0`-`0x0024820D`).

### The focus stack

| Cell | Holds |
|---|---|
| `0x0208EAC0` | 32 widget slots |
| `0x0208EBC8` | the count |
| `0x0208EBC0` | the widget with the focus |

- `0x002470D0(widget)` takes the focus: it pushes the widget (`0x00244640`) and switches to it (`0x00244830`).
- A full stack drops its oldest entry (`0x00244650`-`0x002446C2`).
- `0x00244830` clears the old widget's bit 4 and sends it message 9, then sets the new widget's bit 4 and sends it
  message 8.
- `0x002448D0(widget)` gives the focus up: when the widget has it, the stack pops and the new top takes it.
- `0x00244700(widget, all)` takes a widget out of the stack wherever it sits, every copy when `all` is set and the
  topmost one otherwise, then drops entries equal to their neighbour. `0x002446E0(widget)` gives the focus up and
  removes every copy.

### Opening and closing runs

`0x00246AD0(parent, widget)` opens a widget:

1. It attaches the widget under `parent` when it has none (`0x00246AF5`), and activates it.
2. It sets the rate: 1.0, or one over the game's speed steps in the field at game speed (`0x00246B1B`-`0x00246B49`).
3. From states 0 and 1 it starts a forward run: the descriptor's length in milliseconds becomes
   `ms x 60 / 1000` frames (`0x00246BDF`-`0x00246BEC`), started at the frame counter `0x0208F570`.
4. From state 4 it reverses a closing run in place (`0x00246B72`-`0x00246B90`).
5. It sets state 2 and sends message 14 (`0x00246BFF`).

`0x00247570(widget, descriptor)` installs a widget's descriptor at `+0x48`, or the default `0x00915198` for 0. HUD and menu
code takes most of theirs from the table of `0x28`-byte descriptors at `0x009158C0`, entry `i` through `0x002735E0(i)`
(for example `0x0029BEE8`, `0x0028B92A`).

`0x00244DD0(widget)` closes it, the mirror image: a backward run from descriptor `+0x14`, length 0 when `0x00181C90`
returns 1, state 4, then message 15 (`0x00244EF5`).

Every tick the walker `0x00244970` steps each active widget with `0x00246C20`, which sends message 25 first, steps one tween
channel (messages 22 and 17, 21, 23), and ends a run with message 19 (forward) or 20 (backward)
(`0x0024701E`-`0x0024706B`). When a closing run ends, a widget with bit 6 set is torn down (`0x002449C3`).

`0x0208F570` only advances: the five tick functions add to it, and `0x0022819C` resets it.

### Tweens

Besides its opening and closing runs, a widget has four animated values, one per bit of `+0x80`. Each starter
refuses while any of the other three bits is set, records the start value, the change and the length
`ms x 60 / 1000` frames, and stores a curve in bits 10-13:

| Bit | Starter | Animates | Message per step |
|---:|---|---|---|
| `0` | `0x002468A0(widget, x, y, curve, ms)` | the position `+0x98`/`+0x9A` | 22, and 17 at the end |
| `1` | `0x00247130(widget, w, h, anchor, ms)`, curve 1 | the size `+0x9C`/`+0x9E`; anchor bit 0 or 1 keeps the right or bottom edge in place (`0x00246EAE`-`0x00246EDE`) | 21 |
| `2` | `0x00247300(widget, from, to, curve, ms)` | the float `+0x8C` | 23 |
| `3` | `0x002472A0(widget, value, slot)` | nothing: the float `+0x84` is copied into the draw box's float at `+0x10`, `+0x14` or `+0x18` for slot 0, 1 or 2 (`0x00244D74`-`0x00244DC1`) | none |

`0x00247260` starts bit 1 like `0x00247130` and then replaces the curve with its sixth argument. `0x002468A0` sends 17
twice instead of starting when the widget is already at the target (`0x002468DE`-`0x00246922`).

Each tick `0x00246C20` steps the lowest running bit. The elapsed frames are multiplied by the rate `+0xB8` while the
game runs at speed (`0x00246C58`-`0x00246C7D`); `0x002418F0` sets that rate the way the opening run does: 1.0, or one over
the speed steps (`0x00229E70`) when `0x00229DF0` is set and `0x00229EA0` returns 2.

The curve function `0x00248F40(curve, length, t)` returns 1.0 once `t` reaches `length`; before that, with
`p = t / length`:

| Curve | Value |
|---:|---|
| 0, 6-15 | `p` |
| 1 | `sin(p x pi / 2)` |
| 2 | `1 - sin((p / 2 + 0.5) x pi)` |
| 3 | `0.5 - 0.5 x sin((p + 0.5) x pi)` |
| 4 | `0.6 + 0.4 x sqrt(p)` (`0x003A1D30`) |
| 5 | `0.4 + 0.3 x sin(p x pi / 2) + 0.3 x p` |

Many menu rows fade their alpha `+0xA0` or colour byte `+0xA1` with a pair of helpers that keep their state in the row
widget's own `+0xC0`-`+0xD3`:

- `0x002D04F0(widget, to, which, curve, ms)` starts the fade: bit 0 of `+0xC0` running, bits 2-5 the curve, bits 6-7
  `which` (above 0 for `+0xA1`), the start value at `+0xC4`, the change at `+0xC8`, the length `ms x 60 / 1000`
  frames at `+0xCC` and the start frame `0x0208F570` at `+0xD0`.
- `0x002D0410(widget)`, run each tick by the row, writes `start + change x 0x00248F40(curve, length, now - start)` to the
  byte and clears the running bits when the curve reaches 1.0.

The Party Menu's member rows, the Status and Equip rows and the license board use them (`0x00284D76`, `0x002C1D26`,
`0x00557EA1`, `0x0028453E`, `0x0055A761`).

### Teardown

1. `0x00244F00` asks for the close: with bits 0 and 5 set it starts a closing run, otherwise it sends message 15 and tears
   the widget down now (`0x00244F0A`-`0x00244F39`).
2. `0x00245020` gives up the focus, sends message 18 to the widget and every descendant (`0x002473B0`), and releases it. A
   widget with bit 5 is instead deactivated and marked for release on the next tick (`0x00245072`-`0x0024509B`).
3. The release `0x002482E0` releases the children, unlinks the widget, frees its array, sends message 24, clears the
   procedure, frees the storage and jumps to `+0x08` when set (`0x00248308`-`0x00248405`).

### The half-rate phase counter

`+0xB4` lets a widget work on every other tick. The constructor sets it to 1 when `0x001EDDA0` returns 0 and
`0x00314960` is non-zero (`0x0024674A`-`0x0024675C`); the drain clears it when `0x001EDDA0` returns non-zero and counts it up
otherwise (`0x00248044`-`0x00248059`). `0x001EDEC0(phase)` answers 1 always when `0x01DFE0C0` is set or `0x01F82E38` is clear,
and the phase's low bit inverted otherwise; 43 functions call it on their `+0xB4` (`0x0024218B`, `0x002521DD`,
`0x00580356` and others) before doing their gated work.

### The widget that registers itself once

`0x00565DD0` builds the `0x200`-byte widget `0x00565E00` only while `[0x0209AC30] + 0x168` is empty (`0x00565DD7`); its message 1
stores itself there and its message 18 clears it (`0x00565E50`, `0x0056622D`). So at most one exists at a time, always from
the heap.

### The title asset and its consumer

| Widget | Factory | Size | Procedure | Kept at |
|---|---|---|---|---|
| title asset | `0x00394460` | `0xD8` | `0x00394070` | `0x02AEE4C0` |
| its consumer | `0x00394530` | `0x1D0` | `0x003939B0` | `0x02AEE4C8` |

The script verbs `fsttl_initialize` (`0x00511EA0`) and `fsttl_opencommand` (`0x00511F90`) build them. The asset publishes
itself on message 1 and sets `+0xC0` bit 0 on message 16. The consumer refuses to be built before the asset exists
(`0x00394543`), and each tick it waits for that bit (`0x00393A88`-`0x00393A9F`) and passes the asset's `+0xD0` on to
`0x003946B0`.

The verbs read and set the pair's bits: `fsttl_initialize` answers the asset's `+0xC0` bit 0 (`0x00394500`),
`fsttl_opencommandsync` waits through `0x003944D0`, which answers 0 while `0x01EFAC12` is 2 and the consumer's `+0xC4`
bit 1 is clear, and `fsttl_closecommand` sets the consumer's `+0xC4` bit 2 (`0x00394350`). The consumer opens its
confirm through `0x00394380` and paints its rows with `0x00393950`, which, when `0x00264150`
answers non-zero, recolours row 0 with colour 1 and the others with colour 0 (`0x00393240`), and sets each row's picture cell.

## Modding notes

- A new widget needs a procedure that answers message 1 and returns 0 for the rest; `0x005C5230` is the shared default.
- Widgets of `0x120` bytes or less come from a 112-slot pool; more than 112 at once fall back to the heap.
- Animation lengths are milliseconds in the descriptor at `+0x48`; the run converts them to frames at 60 per second.

## Related

- [Widget messages](widget-messages.md) - every message id.
- [Menus](menus.md) - the router that opens screens.
- [Dialogs](dialogs.md) - the list and confirmation widgets.
