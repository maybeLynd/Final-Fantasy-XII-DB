---
title: "Widgets: how every menu element is built, sized, attached, focused, animated and torn down"
kind: "system"
category: "Menus and HUD"
summary: "The menu element object model: the one constructor and its three entry points, the 0x120-byte pool and the heap, what an object's size says about it, the 0xC0-byte header and its flag bits, parents that build children in their own memory, the tree links and posting up and down it, the per-tick update and input turn, the focus stack, opening and closing runs with the millisecond-to-frame conversion and the three tween channels, the half-rate phase counter, the widget that registers itself once, and the title asset and its consumer."
addresses: ["002465F0", "00244F50", "00245000", "00248220", "00248030", "00244640", "00246AD0", "00245020"]
---

# Widgets: how every menu element is built, sized, attached, focused, animated and torn down

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

```struct WidgetHeader base=record size=0xC0
+0x00  u32[2]  proc    procedure(self, message); 005C5230 when none
+0x08  u32[2]  cont    continuation the release jumps to after freeing (00248405)
+0x10  u32[2]  parent  set by the attach 00248220 (00248267)
+0x18  u32[2]  child   first child (00248239)
+0x20  u32[2]  next    next sibling (0024825C)
+0x28  u32[2]  prev    previous sibling (00248260)
+0x30  u32     nchild  number of children (00248264)
+0x38  u32[2]  draw    draw record while the draw pass is on this widget
+0x40  u32     flags   below; 0x80A plus the generation and borrowed bits when built (00246653)
+0x44  u16     w44     100 (002466FA)
+0x48  u32[2]  trans   animation descriptor, default 00915198 (00246687)
+0x50  u32     flags2  bit 0 clip, bit 1 owns the array at +0x60
+0x60  u32[2]  arr     array freed by the release (0024838A)
+0x68  u32[2]  half    the descriptor half of the current run
+0x70  u32     frames  run length in frames
+0x74  u32     start   frame the run started (0208F570)
+0x78  u32     t78     0 forward, 1.0 backward
+0x7C  u32     state   low nibble: run state 0-4
+0x80  u32     tween   bits 0-2: tween channels running
+0x98  u16[2]  pos     tween channel 0 output
+0x9C  u16[2]  ext     tween channel 1 output
+0xA0  u8      alpha   0x80 when built
+0xA1  u8      rgb     0x80 when built
+0xA2  u8      slot    pool slot marker; 0 frees it (002483E9)
+0xB4  u32     phase   half-rate phase counter
+0xB8  f32     rate    1.0, or 1 / steps at game speed (00246B49)
```

| `+0x40` bit | Meaning |
|---:|---|
| 0 | active (`002473F0`) |
| 1 | may be activated |
| 3 | can take the focus (`002481D8`) |
| 4 | has the focus (`00244865`) |
| 5 | passed to children on attach (`00248271`) |
| 6 | close requested (`00244F0A`) |
| 9 | a run was started |
| 10 | release deferred to the next tick (`00245097`) |
| 13 | has had a child attached |
| 14 | borrowed storage |
| 15 | use the default animation descriptor |
| 17 | generation parity |
| 18 | skip the per-tick update |

### The tree

`00244960(parent, child)` attaches a child only when it has no parent yet, through `00248220`
(`00244960`-`00244965`), which appends it to the parent's children, links the siblings, counts it and stores the parent
(`00248230`-`00248267`). An active parent activates an attached child that may be activated (`002473F0`, which sends
message 6, `002482AE`-`002482C7`).

Messages travel along the tree:

- `00275440(widget, message)` delivers to every ancestor in turn, up to the root (`00275452`-`00275477`).
- `002753F0(widget, message)` delivers to the widget and then every descendant (`002753FA`-`00275427`).

The message record and every id are in [Widget messages](widget-messages.md).

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

### Opening and closing runs

`00246AD0(parent, widget)` opens a widget:

1. It attaches the widget under `parent` when it has none (`00246AF5`), and activates it.
2. It sets the rate: 1.0, or one over the game's speed steps in the field at game speed (`00246B1B`-`00246B49`).
3. From states 0 and 1 it starts a forward run: the descriptor's length in milliseconds becomes
   `ms x 60 / 1000` frames (`00246BDF`-`00246BEC`), started at the frame counter `0208F570`.
4. From state 4 it reverses a closing run in place (`00246B72`-`00246B90`).
5. It sets state 2 and sends message 14 (`00246BFF`).

`00244DD0(widget)` closes it, the mirror image: a backward run from descriptor `+0x14`, length 0 when `00181C90`
returns 1, state 4, then message 15 (`00244EF5`).

Every tick the walker `00244970` steps each active widget with `00246C20`, which sends message 25 first, steps one tween
channel (messages 22 and 17, 21, 23), and ends a run with message 19 (forward) or 20 (backward)
(`0024701E`-`0024706B`). When a closing run ends, a widget with bit 6 set is torn down (`002449C3`).

`0208F570` only advances: the five tick functions add to it, and `0022819C` resets it.

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

## Modding notes

- A new widget needs a procedure that answers message 1 and returns 0 for the rest; `005C5230` is the shared default.
- Widgets of `0x120` bytes or less come from a 112-slot pool; more than 112 at once fall back to the heap.
- Animation lengths are milliseconds in the descriptor at `+0x48`; the run converts them to frames at 60 per second.

## Related

- [Widget messages](widget-messages.md) - every message id.
- [Menus](menus.md) - the router that opens screens.
- [Dialogs](dialogs.md) - the list and confirmation widgets.
