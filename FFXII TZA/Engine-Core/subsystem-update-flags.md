---
title: "Subsystem update flags: the enable word that switches the sixteen interface update groups on or off each frame"
kind: "system"
category: "Engine core"
addresses: "0x0028E290, 0x002507C0, 0x00289970, 0x001EDE80, 0x003F8B40, 0x002917E0, 0x0028C4C0, 0x0028D1C0, 0x003F6BB0, 0x003F7050, 0x003F9F40, 0x00291B90, 0x003F6100, 0x003F24D0, 0x003F24A0, 0x0030C300, 0x003F80D0, 0x00296860, 0x00290CF0, 0x00290EB0, 0x003F8EC0, 0x003F31B0, 0x003FA790, 0x002C6180, 0x0028C870, 0x002547C0, 0x00253970, 0x00184960, 0x00184950, 0x00226280, 0x0036D840"
---

## What the player sees

Nothing changes on screen because of this word: it ships with every bit set and nothing in the
game clears one. What it describes is the order in which the interface advances each frame: the
widgets, the menus, the battle display and the message boxes are sixteen update groups run one
after another by one pump, and every group first asks this word whether it may run. A build that
cleared a bit would freeze that part of the interface while the rest kept moving.

## How it works

### The word and its reader

`0x01E0C464` is a dword that holds `0xFFFFFFFF` in the image. Its sixteen read sites are all inside
`0x0028E290`, the interface pump, and no instruction in the image writes it. The pump tests bits
0 to 3, 5, 6 and 7 as byte tests and bits 8 to 15 as dword tests; bit 4 (`0x0010`) is tested
nowhere. Bit 1 is tested twice, so sixteen tests gate sixteen groups over fifteen distinct bits.

### Where the pump runs

`0x002507C0(first)` is the pump's only caller. The field frame calls it with 1 once per pass when
the `0x002878A0` predicate holds, `0x003583A0()` holds and the time accumulator is 0, and with the
first-step flag once per simulation step when `0x003583A0()` holds; the title and loading state
calls it with 0 ([frame update order](frame-update-order.md)). It runs:

1. `0x02092748` = 1 around `0x00184960(1 + (0x001D6B70() < 1))` ([startup constants](startup-constants.md)),
   then `0x02092748` = 0; everything below only unless `0x002287A0()` holds;
2. `0x0208F570 += 0x00184950()`, and `0x00254CC0` of that value when `first`;
3. `0x0035BC40`, `0x003C6000`, `0x002481A0`, `0x00248030` on the four objects `0x0208EA28`, `0x0208EA40`,
   `0x0208EA48` and `0x0208EA50`, `0x00248190`, `0x002481C0` when `first`, `0x00244980` on the same four;
4. `0x003BBA60` when the 60 fps predicate `0x001EDE80` holds;
5. the pump `0x0028E290([0x01E0C2B0])`;
6. `0x00367200` of `0x00184950()` when `first`, and `0x00228930`.

### The sixteen groups, in frame order

Every group works on the UI manager object at `[0x0209BE80]` ([UI request
router](../Menus-And-HUD/menus.md)); the table gives the handler, the extra
condition the pump adds, and the sub-object or field the handler receives.

| # | Mask | Width | Extra gate | Handler and argument |
|---|---|---|---|---|
| 1 | `0x0001` | byte | | `0x00289970(manager + 0x5380)` |
| 2 | `0x0002` | byte | `0x001EDE80()` non-zero | `0x003F8B40(manager + 0x80)` |
| 3 | `0x0004` | byte | | `0x002917E0(manager, [+0x10F6C], [+0x10F70], [+0x10F72])` only with `+0x10F68` bit 3; then, under the enable bit alone, with `[+0x10F00]` set `0x0028C4C0` and `+0x10F00 = 0x0028D1C0([+0x10F00])`, else `+0x10EF0` = 0 |
| 4 | `0x0008` | byte | `[+0x10F30]` set | `0x003F6BB0`, then `+0x10F30 = 0x003F7050([+0x10F30])` |
| 5 | `0x0020` | byte | `[+0x10F78]` set | `0x003F9F40(manager + 0x57E0)` |
| 6 | `0x0002` | byte | the pump argument's bit 0 | `0x00291B90(manager)`, `0x003F6100([+0x10F10])`, and with `[+0x10F20]` set `0x003F24D0()` rebuilds `+0x10F20` and `0x003F24A0` runs on the new object |
| 7 | `0x1000` | dword | | `+0x10F68` bit 1 = bit 0 of `0x0030C300()` |
| 8 | `0x0040` | byte | | `0x003F80D0(manager + 0xA0D0)` |
| 9 | `0x0080` | byte | | `0x00296860(manager + 0x7FB0, 6)` |
| 10 | `0x2000` | dword | | `0x00290CF0(manager)` |
| 11 | `0x4000` | dword | | `0x00290EB0(manager)` |
| 12 | `0x0100` | dword | `+0x10F68` bit 8 | `0x003F8EC0(manager + 0xA0)` |
| 13 | `0x0200` | dword | `[+0x10F40]` set | `+0x10F40 = 0x003F31B0([+0x10F40], 0x00290DF0)` |
| 14 | `0x0400` | dword | | `0x003FA790(manager + 0x57E0)` |
| 15 | `0x8000` | dword | `[+0x10F80]` set | `0x002C6180()` |
| 16 | `0x0800` | dword | | `0x0028C870(manager + 0x7EA0)`, the pump's last act |

The order is not the bit order: bit 12 runs seventh, bits 13 and 14 before bit 8, and bit 11 last.
Bit 1 gates two groups at two points of the frame, the second only when the pump's argument has
bit 0.

The argument is the 16-bit word `0x01E0C2B0`. `0x00253970`, the interface start-up, stores
`0xF`. `0x00226280`, the world-lock apply that runs at the end of every field frame, stores through
`0x002547C0` the value `0xF` when the AND of the lock table's first words has bit 36, else `0xE`,
with bits 2 and 3 cleared when that AND lacks bit 37. So a lock record that clears bit 36 skips group 6 for
every frame it is held, while the other fifteen groups keep running.

`0x0036D840(on)` sets or clears bits 2 and 3 of two remembered words, `0x02EC0B24` and `0x02EC0B28`, and stores the
first through the same setter and the second as the HUD draw word `0x01E0C2AC` (`0x00254840`, `0x0036D873`;
[HUD](../Menus-And-HUD/hud.md)).

Script verbs call `0x0036D840`: `setmenuhptargetshowstatus` (`0x2A7`, `0x0034D700`), and `0x003B7BB0`,
`0x003B7C60` and `0x003B7E20`, the bodies of `resumeposbattletarget` (`0x195`), `resumepartyinfo_spattack`
(`0x2A4`) and `setpossummonspace` (`0x191`, `0x003482E0`)
([party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md)).

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01E0C464` | `u32` | the enable word; 0xFFFFFFFF in the image; readers: the sixteen tests in 0x0028E290; writers: none |  |
| `0x01E0C2B0` | `u16` | the pump argument; bit 0 enables group 6; writers 0x00226280 and 0x0036D840 through 0x002547C0, and 0x00253970 |  |
| `0x0209BE80` | `void*` | the UI manager object |  |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00080` | `group 2 sub-object` | +0x5380 | group 1 sub-object       +`0x57E0`  groups 5 and 14 sub-object |
| `+0x07EA0` | `group 16 sub-object` | +0x7FB0 | group 9 sub-object       +`0xA0`    group 12 sub-object |
| `+0x0A0D0` | `group 8 sub-object` | +0x10EF0 / +0x10F00 | group 3's list and its rebuilt head |
| `+0x10F10` | `/ +0x10F20` | group 6's two objects | +`0x10F30`  group 4's object   +`0x10F40`  group 13's object |
| `+0x10F68` | `u32` | flags: | bit 1 written by group 7, bit 3 gates group 3's `0x002917E0` call, bit 8 gates group 12 |
| `+0x10F6C` | `u32, +0x10F70 u16, +0x10F72 u16` | group 3's arguments | +`0x10F78`  group 5's gate   +`0x10F80`  group 15's gate |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02092748` | `u32` | set to 1 around the 0x00184960 call in 0x002507C0 |  |
| `0x0208F570` | `u32` | accumulates 0x00184950() per 0x002507C0 call |  |

## Shipped data

| Fact | Value |
|---|---|
| the enable word | `0xFFFFFFFF` in the image, no writer |
| groups, distinct bits | 16, 15 (bit 4 unused) |
| test widths | 8 byte tests (bits 0 to 7), 8 dword tests (bits 8 to 15) |
| `0x00296860`'s second argument | 6 |

## Operations

Per field-frame pass or simulation step in which `0x003583A0()` holds: `0x002507C0`, then the pump,
which runs each of the sixteen groups whose bit is set and whose extra gate holds, in the table's
order, ending in the tail jump to `0x0028C870`.

## State

The enable word; the pump argument word; the UI manager object's flag word `+0x10F68` and the
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

- [Frame update order](frame-update-order.md): where `0x002507C0` sits in the field frame.
- [UI request router](../Menus-And-HUD/menus.md): the UI manager object the
  groups update.
