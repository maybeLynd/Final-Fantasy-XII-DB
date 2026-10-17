---
title: "Widgets: how every menu element is built, sized, attached, focused, animated and torn down"
kind: "system"
category: "Menus and HUD"
addresses: "002465F0, 00244F50, 00245000, 00248220, 00248030, 00244640, 00246AD0, 00245020"
---

## What the player sees

- Every menu, window, list and gauge is a widget: it opens with a short slide or fade, answers input while it has the
  focus, and closes with the reverse animation.
- Animations take the same time at any frame rate setting, because their durations are given in milliseconds.

## How it works

### Construction

Every widget is built by `002465F0(object, size, procedure, record, borrowed)`:

1. It clears the object (`00246612`-`00246626`).
2. It installs the procedure at `+0x00`, or `005C5230` (`xor eax, eax` / `ret`) when none is given
   (`0024662B`-`00246641`).
3. It writes the header (below).
4. It calls the procedure once with message 1 and the creator's two arguments (`00246721`-`00246748`).

There are three ways in:

| Entry | Does |
|---|---|
| `00244F50(size, procedure, record)` | the factory: size 0 becomes `0xC0`; up to `0x120` bytes it takes a free slot of the 112-slot pool at `*0208EA58` (`00244F7F`-`00244FAE`), otherwise or when the pool is full it allocates from the heap (`002497B0`) |
| `00245000(object, size, procedure, record)` | builds in memory the caller provides, usually inside the parent |
| `002465F0` directly | 7 sites, in `00241BF0`, `00241C90` and `00247AE0` |

A pool or in-place widget is marked borrowed (`+0x40` bit 14): the release then frees only the pool slot
(`002483E5`-`002483F0`), while a heap widget is freed (`002483DE`).

### Sizes

Over the image there are 296 construction sites in 235 functions, building 267 procedures at 83 sizes, from `0xC0` to
`0x179E0`. No procedure is built at two sizes, so a widget's size identifies its type.

| Size | Procedure | Widget |
|---|---|---|
| `0x61F0` | `00279E20` | the battle menu ([Battle menu](battle-menu.md)) |
| `0x179E0` | `002B7590`, `002BA700`, `003CB650` | the map containers ([Map screens](map-screens.md)) |
| `0xBC08` | `002B7B80`, `002BAF80` | the map pages |
| `0x640` | `0057C480` | the confirmation window ([Dialogs](dialogs.md)) |

A parent can hold its children inside itself: the battle menu builds two `0x3010` panels at `+0xC0` and `+0x30D0`, the
Dismiss confirmation in a panel slot, and the `0xD0` target tabs at `+0x60E0`, all with `00245000`
(`0027A12F`-`0027A42D`).

### The header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32[2]` | proc | procedure(self, message); `005C5230` when none |
| `+0x08` | `u32[2]` | cont | continuation the release jumps to after freeing (`00248405`) |
| `+0x10` | `u32[2]` | parent | set by the attach `00248220` (`00248267`) |
| `+0x18` | `u32[2]` | child | first child (`00248239`) |
| `+0x20` | `u32[2]` | next | next sibling (`0024825C`) |
| `+0x28` | `u32[2]` | prev | previous sibling (`00248260`) |
| `+0x30` | `u32` | nchild | number of children (`00248264`) |
| `+0x38` | `u32[2]` | draw | draw record while the draw pass is on this widget |
| `+0x40` | `u32` | flags | below; `0x80A` plus the generation and borrowed bits when built (`00246653`) |
| `+0x44` | `u16` | w44 | 100 (`002466FA`) |
| `+0x48` | `u32[2]` | trans | animation descriptor, default `00915198` (`00246687`) |
| `+0x50` | `u32` | flags2 | bit 0 clip, bit 1 owns the array at `+0x60` |
| `+0x60` | `u32[2]` | arr | array freed by the release (`0024838A`) |
| `+0x68` | `u32[2]` | half | the descriptor half of the current run |
| `+0x70` | `u32` | frames | run length in frames |
| `+0x74` | `u32` | start | frame the run started (`0208F570`) |
| `+0x78` | `u32` | t78 | 0 forward, 1.0 backward |
| `+0x7C` | `u32` | state | low nibble: run state 0-4 |
| `+0x80` | `u32` | tween | bits 0-2: tween channels running |
| `+0x98` | `u16[2]` | pos | tween channel 0 output |
| `+0x9C` | `u16[2]` | ext | tween channel 1 output |
| `+0xA0` | `u8` | alpha | `0x80` when built |
| `+0xA1` | `u8` | rgb | `0x80` when built |
| `+0xA2` | `u8` | slot | pool slot marker; 0 frees it (`002483E9`) |
| `+0xB4` | `u32` | phase | half-rate phase counter |
| `+0xB8` | `f32` | rate | 1.0, or 1 / steps at game speed (`00246B49`) |

| `+0x40` bit | Meaning |
|---:|---|
| 0 | active (`002473F0`) |
| 1 | may be activated |
| 3 | can take the focus (`002481D8`) |
| 4 | has the focus (`00244865`) |
| 5 | passed to children on attach (`00248271`) |
| 6 | close requested (`00244F0A`) |
| 7 | the byte offsets at `+0xA4`-`+0xAD` move the draw box (`00246480`) |
| 9 | a run was started |
| 10 | release deferred to the next tick (`00245097`) |
| 13 | has had a child attached, or a child's priority changed: the children are re-sorted (`00244990`) |
| 14 | borrowed storage |
| 15 | use the default animation descriptor |
| 17 | generation parity |
| 18 | skip the per-tick update |
| 24 | drawn in the second draw pass (`00247730`) |
| 27 | `+0xAE`/`+0xAF` also widen the draw box |

### The tree

`00244960(parent, child)` attaches a child only when it has no parent yet, through `00248220`
(`00244960`-`00244965`), which appends it to the parent's children, links the siblings, counts it and stores the parent
(`00248230`-`00248267`). An active parent activates an attached child that may be activated (`002473F0`, which sends
message 6, `002482AE`-`002482C7`). A parent with bit 5 passes it to the child and to every descendant of the child
through the pre-order walker `002463F0(widget, callback, value)` with the bit setter `002418E0` (`00248271`-`002482A0`).

Two shortcuts use the main root `[0208EA28]`:

- `00246AC0(widget)` opens a widget under it (`00246AD0`).
- `00247950(widget, on)` attaches a widget that has no parent to it with bit 1 set to `on`. For a widget that has a
  parent it sets bit 1 to `on` through `00247870`, which also runs the activation `002473F0` when bit 5 is set
  (`0024795C`-`0024797A`).
- `00247980(parent, widget, on)` does the same under a parent the caller gives; `00228130` calls it.

Messages travel along the tree:

- `00275440(widget, message)` delivers to every ancestor in turn, up to the root (`00275452`-`00275477`).
- `002753F0(widget, message)` delivers to the widget and then every descendant (`002753FA`-`00275427`).

The message record and every id are in [Widget messages](widget-messages.md).

### Draw order and the two draw passes

`00247930(widget, priority)` stores a widget's draw priority at `+0x44` (100 when built) and sets bit 13 on its
parent. When the walker `00244980` reaches a widget with bit 13, it re-sorts that widget's children with `002479B0`
and clears the bit (`00244990`-`0024499F`):

1. Each child's priority, position in the list and pointer go into the scratch table `0208ED60`
   (`00247A0A`-`00247A2D`).
2. The sort `00249CE0` orders them with the comparator `00244610`: a larger priority first, equal priorities in
   their old order. `00249CE0` jumps to `00249680(scratch, base, size, n, compare)`, an insertion sort that
   takes each element in turn into `scratch` and moves larger ones up by `size` bytes.
3. The children are relinked in that order (`00247A51`-`00247AB1`).

The root draw passes `002450B0` and `00245110` set `0208F564` to 0 and to 1 and walk the tree with `00245E60`. A
widget's own content is drawn only in the pass equal to its `+0x40` bit 24, with bit 28 clear (`0024623A`-`0024624B`);
its box is drawn in that pass when `+0x40` bit 7 is also set (`002461BB`-`002461CE`).
`00247730(widget, pass)` sets that bit on a widget and every descendant.

`00245E60` takes each widget's box from `00246480(widget, box)` (`00245F50`):

- the position and size from `+0x98`, an inner rectangle the size of the widget, scale 1.0 at box `+0x1C` and
  `+0x20`, and the alpha `+0xA0`;
- with bit 7, the signed bytes `+0xAC`/`+0xAD` added to the position, the inner offset from `+0xA4`/`+0xA5`, and
  `+0xA6`/`+0xA7` added to the inner size, plus `+0xAE`/`+0xAF` with bit 27;
- then the running opening or closing run, through `00244A20`.

It returns 1 when a float at box `+0x10`-`+0x18` is not 0 or the scale is not 1.0. `00246450` returns the position
alone, with the same bit 7 offset.

The box itself is a nine-piece panel. `00245E60` sets up a draw record (`002D8530`) and calls `002455A0` when
`+0x40` bit 8 is set, otherwise `00245170` (`002461D9`-`002461F0`). `00245170(widget, record)` draws nothing while
`002DD4B0()` (the dword `0215E6D0`) is 0. Otherwise:

1. It takes the atlas `0208EAA0` (`cm_win_c`), or `0208EAB0` with `+0x40` bit 22, and nine consecutive 8-byte
   pieces from the index its header gives at `+0x44`: `i16` x and y, then 12-bit width and height.
2. The middle column is the widget width `+0x9C` less the two corner widths plus `+0xA6`; the middle row the height
   `+0x9E` less the two corner heights plus `+0xA7`. The panel starts at `+0xA4`, `+0xA5`.
3. Its colour is `0x80808080` for a style byte `+0xA3` below 2, else colour-table entry `+0xA3 + 0x92`
   (`002DD7E0`); its palette byte is the first piece's byte `+7` for a style below 10, else `002DD7B0(+0xA3 +
   0x92)`.
4. It draws the nine pieces row by row with `002DA7C0` between `002DAF30` and `002DAC70`, leaving out the
   middle row or column when its size is not above 0.

`00272310(widget, out)` gives a widget's place on screen: its own box position
(`00246480`) plus that of every ancestor up the `+0x10` chain, for `003EE420` (`003EE511`, `003EE51F`).
`003EE420` also steps four fades of its object with `003EEBD0(object, up)` (`003EE6A4`). Each moves by
`1 / ([01DFE0B4] x 9600 / 1000)` and is clamped to 0-1: `+0x1D0` up when `up` is non-zero, `+0x88` up with `+0x1D4`
bit 8, and `+0x188` and `+0x1B8` up with `+0x1D4` bit 9; each goes down otherwise.

`003EE8C0(object, text, a, b)` sets those fades up for a new text. The object holds two 0x1E0-byte
text entries at `+0xC0`, and the index `+0x4B0` toggles between them:

1. It clears bits 8 and 9 of the old entry's `+0x1D4`, moves the index and sets both bits on the new one.
2. It copies up to 0x80 bytes of `text` into the entry (`00254F30`); a null or empty text leaves it empty.
3. It clears bit 9 again when `a` and `b` are both 0, zeroes `+0x1D0`, `+0x88`, `+0x188` and `+0x1B8`,
   keeps `a` at `+0x18C` and `b` at `+0x1BC`, and runs `002B3400(entry + 0xA0, 0, 0)`.

The battle menu's title writer `0027D480` (`0027D52F`) and `00298250` (`002984C0`, on its `+0xC0`) call it.

Two helpers set those offset bytes:

- `002476E0(widget, d)` adds the low bytes of the four words at `d` to `+0xA4`-`+0xA7` when bit 7 is set and bit 8
  clear; `002A70B0` calls it.
- `00247810(widget)` reads the three bits 16-18 of `+0x44`. With bit 18 clear it sets `+0xAD` to -7 when bit 17 is
  set and to 6 otherwise, and `+0xAC` the same way from bit 16; with bit 18 set it writes only the -7 values.
  `00227EE0`, `002A6A80` and the confirmation window `0057C480` call it.
- `002478D0(widget, on)` sets or clears bit 18, the per-tick skip, on a widget and every descendant (first child
  `+0x18`, next sibling `+0x20`); `00285290` calls it.

`00247780(on)` sets bit 0 of `0208ED58`. While it is set, both passes also call `00245510` for a root whose `+0xC0`
is 1, which hands the root's position and alpha to `00367940` (`002450D7`-`002450F5`, `00245137`-`00245149`); the
first pass does so only while `0208F568` is 0. The script verbs `fsmenu_showcursor` and `fsmenu_hidecursor` set and
clear the bit (`00510964`, `005109A3`).

### The per-tick update and the input turn

Five UI tick functions (`00250540`, `002506D0`, `00250730`, `002507C0`, `002508E0`) each flip the parity `0208ED5C`
(`002481A0`) and run the drain `00248030` over the root widgets:

1. A widget with bit 10 set is released (`00248086`-`00248097`).
2. Every other widget gets message 2 unless bit 18 is set, and its generation bit is restamped (`002480DB`-`00248110`).

`002284F0` also runs the drain (`0022865C`). So message 2 reaches every live widget once per UI tick. The same ticks give the focus widget its input turn
(`002481C0`): message 10, or 11 when a widget up its parent chain has bit 9 set (`002481D0`-`0024820D`).

### The focus stack

| Cell | Holds |
|---|---|
| `0208EAC0` | 32 widget slots |
| `0208EBC8` | the count |
| `0208EBC0` | the widget with the focus |

- `002470D0(widget)` takes the focus: it pushes the widget (`00244640`) and switches to it (`00244830`).
- A full stack drops its oldest entry (`00244650`-`002446C2`).
- `00244830` clears the old widget's bit 4 and sends it message 9, then sets the new widget's bit 4 and sends it
  message 8.
- `002448D0(widget)` gives the focus up: when the widget has it, the stack pops and the new top takes it.
- `00244700(widget, all)` takes a widget out of the stack wherever it sits, every copy when `all` is set and the
  topmost one otherwise, then drops entries equal to their neighbour. `002446E0(widget)` gives the focus up and
  removes every copy.

### Opening and closing runs

`00246AD0(parent, widget)` opens a widget:

1. It attaches the widget under `parent` when it has none (`00246AF5`), and activates it.
2. It sets the rate: 1.0, or one over the game's speed steps in the field at game speed (`00246B1B`-`00246B49`).
3. From states 0 and 1 it starts a forward run: the descriptor's length in milliseconds becomes
   `ms x 60 / 1000` frames (`00246BDF`-`00246BEC`), started at the frame counter `0208F570`.
4. From state 4 it reverses a closing run in place (`00246B72`-`00246B90`).
5. It sets state 2 and sends message 14 (`00246BFF`).

`00247570(widget, descriptor)` installs a widget's descriptor at `+0x48`, or the default `00915198` for 0. HUD and menu
code takes most of theirs from the table of `0x28`-byte descriptors at `009158C0`, entry `i` through `002735E0(i)`
(for example `0029BEE8`, `0028B92A`).

`00244DD0(widget)` closes it, the mirror image: a backward run from descriptor `+0x14`, length 0 when `00181C90`
returns 1, state 4, then message 15 (`00244EF5`).

Every tick the walker `00244970` steps each active widget with `00246C20`, which sends message 25 first, steps one tween
channel (messages 22 and 17, 21, 23), and ends a run with message 19 (forward) or 20 (backward)
(`0024701E`-`0024706B`). When a closing run ends, a widget with bit 6 set is torn down (`002449C3`).

`0208F570` only advances: the five tick functions add to it, and `0022819C` resets it.

### Tweens

Besides its opening and closing runs, a widget has four animated values, one per bit of `+0x80`. Each starter
refuses while any of the other three bits is set, records the start value, the change and the length
`ms x 60 / 1000` frames, and stores a curve in bits 10-13:

| Bit | Starter | Animates | Message per step |
|---:|---|---|---|
| `0` | `002468A0(widget, x, y, curve, ms)` | the position `+0x98`/`+0x9A` | 22, and 17 at the end |
| `1` | `00247130(widget, w, h, anchor, ms)`, curve 1 | the size `+0x9C`/`+0x9E`; anchor bit 0 or 1 keeps the right or bottom edge in place (`00246EAE`-`00246EDE`) | 21 |
| `2` | `00247300(widget, from, to, curve, ms)` | the float `+0x8C` | 23 |
| `3` | `002472A0(widget, value, slot)` | nothing: the float `+0x84` is copied into the draw box's float at `+0x10`, `+0x14` or `+0x18` for slot 0, 1 or 2 (`00244D74`-`00244DC1`) | none |

`00247260` starts bit 1 like `00247130` and then replaces the curve with its sixth argument. `002468A0` sends 17
twice instead of starting when the widget is already at the target (`002468DE`-`00246922`).

Each tick `00246C20` steps the lowest running bit. The elapsed frames are multiplied by the rate `+0xB8` while the
game runs at speed (`00246C58`-`00246C7D`); `002418F0` sets that rate the way the opening run does: 1.0, or one over
the speed steps (`00229E70`) when `00229DF0` is set and `00229EA0` returns 2.

The curve function `00248F40(curve, length, t)` returns 1.0 once `t` reaches `length`; before that, with
`p = t / length`:

| Curve | Value |
|---:|---|
| 0, 6-15 | `p` |
| 1 | `sin(p x pi / 2)` |
| 2 | `1 - sin((p / 2 + 0.5) x pi)` |
| 3 | `0.5 - 0.5 x sin((p + 0.5) x pi)` |
| 4 | `0.6 + 0.4 x sqrt(p)` (`003A1D30`) |
| 5 | `0.4 + 0.3 x sin(p x pi / 2) + 0.3 x p` |

Many menu rows fade their alpha `+0xA0` or colour byte `+0xA1` with a pair of helpers that keep their state in the row
widget's own `+0xC0`-`+0xD3`:

- `002D04F0(widget, to, which, curve, ms)` starts the fade: bit 0 of `+0xC0` running, bits 2-5 the curve, bits 6-7
  `which` (above 0 for `+0xA1`), the start value at `+0xC4`, the change at `+0xC8`, the length `ms x 60 / 1000`
  frames at `+0xCC` and the start frame `0208F570` at `+0xD0`.
- `002D0410(widget)`, run each tick by the row, writes `start + change x 00248F40(curve, length, now - start)` to the
  byte and clears the running bits when the curve reaches 1.0.

The Party Menu's member rows, the Status and Equip rows and the license board use them (`00284D76`, `002C1D26`,
`00557EA1`, `0028453E`, `0055A761`).

### Teardown

1. `00244F00` asks for the close: with bits 0 and 5 set it starts a closing run, otherwise it sends message 15 and tears
   the widget down now (`00244F0A`-`00244F39`).
2. `00245020` gives up the focus, sends message 18 to the widget and every descendant (`002473B0`), and releases it. A
   widget with bit 5 is instead deactivated and marked for release on the next tick (`00245072`-`0024509B`).
3. The release `002482E0` releases the children, unlinks the widget, frees its array, sends message 24, clears the
   procedure, frees the storage and jumps to `+0x08` when set (`00248308`-`00248405`).

### The half-rate phase counter

`+0xB4` lets a widget work on every other tick. The constructor sets it to 1 when `001EDDA0` returns 0 and
`00314960` is non-zero (`0024674A`-`0024675C`); the drain clears it when `001EDDA0` returns non-zero and counts it up
otherwise (`00248044`-`00248059`). `001EDEC0(phase)` answers 1 always when `01DFE0C0` is set or `01F82E38` is clear,
and the phase's low bit inverted otherwise; 43 functions call it on their `+0xB4` (`0024218B`, `002521DD`,
`00580356` and others) before doing their gated work.

### The widget that registers itself once

`00565DD0` builds the `0x200`-byte widget `00565E00` only while `[0209AC30] + 0x168` is empty (`00565DD7`); its message 1
stores itself there and its message 18 clears it (`00565E50`, `0056622D`). So at most one exists at a time, always from
the heap.

### The title asset and its consumer

| Widget | Factory | Size | Procedure | Kept at |
|---|---|---|---|---|
| title asset | `00394460` | `0xD8` | `00394070` | `02AEE4C0` |
| its consumer | `00394530` | `0x1D0` | `003939B0` | `02AEE4C8` |

The script verbs `fsttl_initialize` (`00511EA0`) and `fsttl_opencommand` (`00511F90`) build them. The asset publishes
itself on message 1 and sets `+0xC0` bit 0 on message 16. The consumer refuses to be built before the asset exists
(`00394543`), and each tick it waits for that bit (`00393A88`-`00393A9F`) and passes the asset's `+0xD0` on to
`003946B0`.

The verbs read and set the pair's bits: `fsttl_initialize` answers the asset's `+0xC0` bit 0 (`00394500`),
`fsttl_opencommandsync` waits through `003944D0`, which answers 0 while `01EFAC12` is 2 and the consumer's `+0xC4`
bit 1 is clear, and `fsttl_closecommand` sets the consumer's `+0xC4` bit 2 (`00394350`). The consumer opens its
confirm through `00394380` and paints its rows with `00393950`, which, when `00264150`
answers non-zero, recolours row 0 with colour 1 and the others with colour 0 (`00393240`), and sets each row's picture cell.

## Modding notes

- A new widget needs a procedure that answers message 1 and returns 0 for the rest; `005C5230` is the shared default.
- Widgets of `0x120` bytes or less come from a 112-slot pool; more than 112 at once fall back to the heap.
- Animation lengths are milliseconds in the descriptor at `+0x48`; the run converts them to frames at 60 per second.

## Related

- [Widget messages](widget-messages.md) - every message id.
- [Menus](menus.md) - the router that opens screens.
- [Dialogs](dialogs.md) - the list and confirmation widgets.
