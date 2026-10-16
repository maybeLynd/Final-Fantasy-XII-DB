---
title: "Subsystem update flags: the enable word that switches the sixteen interface update groups on or off each frame"
kind: "system"
category: "Engine core"
addresses: "0028E290, 002507C0, 00289970, 001EDE80, 003F8B40, 002917E0, 0028C4C0, 0028D1C0, 003F6BB0, 003F7050, 003F9F40, 00291B90, 003F6100, 003F24D0, 003F24A0, 0030C300, 003F80D0, 00296860, 00290CF0, 00290EB0, 003F8EC0, 003F31B0, 003FA790, 002C6180, 0028C870, 002547C0, 00253970, 00184960, 00184950, 00226280, 0036D840"
---

## What the player sees

Nothing changes on screen because of this word: it ships with every bit set and nothing in the
game clears one. What it describes is the order in which the interface advances each frame: the
widgets, the menus, the battle display and the message boxes are sixteen update groups run one
after another by one pump, and every group first asks this word whether it may run. A build that
cleared a bit would freeze that part of the interface while the rest kept moving.

## How it works

### The word and its reader

`01E0C464` is a dword that holds `FFFFFFFF`<sub>h</sub> in the image. Its sixteen read sites are all inside
`0028E290`, the interface pump, and no instruction in the image writes it. The pump tests bits
0 to 3, 5, 6 and 7 as byte tests and bits 8 to 15 as dword tests; bit 4 (`0010`<sub>h</sub>) is tested
nowhere. Bit 1 is tested twice, so sixteen tests gate sixteen groups over fifteen distinct bits.

### Where the pump runs

`002507C0(first)` is the pump's only caller. The field frame calls it with 1 once per pass when
the `002878A0` predicate holds, `003583A0()` holds and the time accumulator is 0, and with the
first-step flag once per simulation step when `003583A0()` holds; the title and loading state
calls it with 0 ([frame update order](frame-update-order.md)). It runs:

1. `02092748` = 1 around `00184960(1 + (001D6B70() < 1))` ([startup constants](startup-constants.md)),
   then `02092748` = 0; everything below only unless `002287A0()` holds;
2. `0208F570 += 00184950()`, and `00254CC0` of that value when `first`;
3. `0035BC40`, `003C6000`, `002481A0`, `00248030` on the four objects `0208EA28`, `0208EA40`,
   `0208EA48` and `0208EA50`, `00248190`, `002481C0` when `first`, `00244980` on the same four;
4. `003BBA60` when the 60 fps predicate `001EDE80` holds;
5. the pump `0028E290([01E0C2B0])`;
6. `00367200` of `00184950()` when `first`, and `00228930`.

### The sixteen groups, in frame order

Every group works on the UI manager object at `[0209BE80]` ([UI request
router](../Menus-And-HUD/menus.md)); the table gives the handler, the extra
condition the pump adds, and the sub-object or field the handler receives.

| # | Mask | Width | Extra gate | Handler and argument |
|---|---|---|---|---|
| 1 | `0001`<sub>h</sub> | byte | | `00289970(manager + 5380h)` |
| 2 | `0002`<sub>h</sub> | byte | `001EDE80()` non-zero | `003F8B40(manager + 80h)` |
| 3 | `0004`<sub>h</sub> | byte | | `002917E0(manager, [+10F6Ch], [+10F70h], [+10F72h])` only with `+10F68`<sub>h</sub> bit 3; then, under the enable bit alone, with `[+10F00h]` set `0028C4C0` and `+10F00h = 0028D1C0([+10F00h])`, else `+10EF0`<sub>h</sub> = 0 |
| 4 | `0008`<sub>h</sub> | byte | `[+10F30h]` set | `003F6BB0`, then `+10F30h = 003F7050([+10F30h])` |
| 5 | `0020`<sub>h</sub> | byte | `[+10F78h]` set | `003F9F40(manager + 57E0h)` |
| 6 | `0002`<sub>h</sub> | byte | the pump argument's bit 0 | `00291B90(manager)`, `003F6100([+10F10h])`, and with `[+10F20h]` set `003F24D0()` rebuilds `+10F20`<sub>h</sub> and `003F24A0` runs on the new object |
| 7 | `1000`<sub>h</sub> | dword | | `+10F68`<sub>h</sub> bit 1 = bit 0 of `0030C300()` |
| 8 | `0040`<sub>h</sub> | byte | | `003F80D0(manager + A0D0h)` |
| 9 | `0080`<sub>h</sub> | byte | | `00296860(manager + 7FB0h, 6)` |
| 10 | `2000`<sub>h</sub> | dword | | `00290CF0(manager)` |
| 11 | `4000`<sub>h</sub> | dword | | `00290EB0(manager)` |
| 12 | `0100`<sub>h</sub> | dword | `+10F68`<sub>h</sub> bit 8 | `003F8EC0(manager + A0h)` |
| 13 | `0200`<sub>h</sub> | dword | `[+10F40h]` set | `+10F40h = 003F31B0([+10F40h], 00290DF0)` |
| 14 | `0400`<sub>h</sub> | dword | | `003FA790(manager + 57E0h)` |
| 15 | `8000`<sub>h</sub> | dword | `[+10F80h]` set | `002C6180()` |
| 16 | `0800`<sub>h</sub> | dword | | `0028C870(manager + 7EA0h)`, the pump's last act |

The order is not the bit order: bit 12 runs seventh, bits 13 and 14 before bit 8, and bit 11 last.
Bit 1 gates two groups at two points of the frame, the second only when the pump's argument has
bit 0.

The argument is the 16-bit word `01E0C2B0`. `00253970`, the interface start-up, stores
`F`<sub>h</sub>. `00226280`, the world-lock apply that runs at the end of every field frame, stores through
`002547C0` the value `F`<sub>h</sub> when the AND of the lock table's first words has bit 36, else `E`<sub>h</sub>,
with bits 2 and 3 cleared when that AND lacks bit 37; `0036D840(on)` sets or clears bits 2 and 3
through the same setter. So a lock record that clears bit 36 skips group 6 for every frame it is
held, while the other fifteen groups keep running.

## Layouts

```
01E0C464  u32  the enable word; 0xFFFFFFFF in the image; readers: the sixteen tests in 0028E290; writers: none
01E0C2B0  u16  the pump argument; bit 0 enables group 6; writers 00226280 and 0036D840 through 002547C0, and 00253970
0209BE80  ptr  the UI manager object
  +0x80    group 2 sub-object          +0x5380  group 1 sub-object       +0x57E0  groups 5 and 14 sub-object
  +0x7EA0  group 16 sub-object         +0x7FB0  group 9 sub-object       +0xA0    group 12 sub-object
  +0xA0D0  group 8 sub-object          +0x10EF0 / +0x10F00  group 3's list and its rebuilt head
  +0x10F10 / +0x10F20  group 6's two objects   +0x10F30  group 4's object   +0x10F40  group 13's object
  +0x10F68 u32 flags: bit 1 written by group 7, bit 3 gates group 3's 002917E0 call, bit 8 gates group 12
  +0x10F6C u32, +0x10F70 u16, +0x10F72 u16  group 3's arguments   +0x10F78  group 5's gate   +0x10F80  group 15's gate
02092748  u32  set to 1 around the 00184960 call in 002507C0
0208F570  u32  accumulates 00184950() per 002507C0 call
```

## Shipped data

| Fact | Value |
|---|---|
| the enable word | `FFFFFFFF`<sub>h</sub> in the image, no writer |
| groups, distinct bits | 16, 15 (bit 4 unused) |
| test widths | 8 byte tests (bits 0 to 7), 8 dword tests (bits 8 to 15) |
| `00296860`'s second argument | 6 |

## Operations

Per field-frame pass or simulation step in which `003583A0()` holds: `002507C0`, then the pump,
which runs each of the sixteen groups whose bit is set and whose extra gate holds, in the table's
order, ending in the tail jump to `0028C870`.

## State

The enable word; the pump argument word; the UI manager object's flag word `+10F68`<sub>h</sub> and the
object pointers the gates test.

## Modding notes

- The word is an authored switch board left fully on; clearing a bit at run time is the only way
  to use it, since nothing in the game writes it.
- A port that iterates bits 0 to 15 in order runs the groups in the wrong order; the frame order
  above is the one the handlers were written against.
- Bit 1 is one bit for two groups; a one-bit-per-subsystem design cannot express it.
- Group 6 is the only group the game switches off at run time, through the pump argument rather
  than the enable word: a world lock whose record clears bit 36 holds it for the lock's duration.
- Half the tests are byte-wide: a port that stores the word as a byte loses bits 8 to 15.

## Related

- [Frame update order](frame-update-order.md): where `002507C0` sits in the field frame.
- [UI request router](../Menus-And-HUD/menus.md): the UI manager object the
  groups update.
