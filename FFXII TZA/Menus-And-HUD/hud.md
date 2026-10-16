---
title: "HUD: the interface manager and its pool, the target lines, the target ring and the selection marker, and the calls other systems make into it"
kind: "system"
category: "Menus and HUD"
addresses: "0028F8B0, 00291750, 0028F2F0, 00273A30, 00273B40, 00291320, 002917E0, 0028EAB0, 00290370, 0028CA40, 00271AB0"
---

## What the player sees

- In battle a line joins each character to the target it is acting on; the Target Lines option in Config turns these
  lines off.
- The unit the menu or the cursor points at stands on a spinning ring whose colour depends on what it is.
- A second, rotating marker sits under a unit chosen outside the party list.
- The party's HP and MP list, the battle menu, the help line and the gauges all hang off the same HUD object.

## How it works

### The manager object

The HUD is one `0x10FD0`-byte object whose pointer is at `0209BE80`:

1. `0028F8B0` first tears down any old one with `0028F2F0`, then allocates the object through `00271420(0x10FD0)`
   when the pointer is empty and initialises it with `00291750` (`0028F8CF`, `0028F8DE`).
2. `00291750` clears all `0x10FD0` bytes, allocates the `0x8030`-byte pool into `+0x10FC0` and prepares it
   (`00272470`), builds the part at `+0x5380` (`0028A080`), the selection marker `+0x7EA0` (`0028CA30`), the help
   block `+0x8FA0` (`002BE450`, `002BE0A0`) and the world-object part `+0x57E0` (`003FA760`), and sets
   `+0x10F90` to -1 and byte `+0x10FA2` to 1.
3. `0028F8B0` then clears the two rolling-counter tables (`00296260`, `00296240`), resets the counter list `+0x80`
   (`004FE3C0`), writes 1 to `+0xAA44`, sets flag bit 5 and closes the widget kept at `+0x10F88` (`0028F8E3`-`0028F952`).

`0028F8B0` runs from `0035C560` (`0035C57F`). `0028F2F0` releases every list in the pool, the two `+0x10F74` and
`+0x10F78` widgets through `00274840` (`002446E0`, `002473B0`, `002482E0`: focus, message 18 and release), the
level-up blink part (`00296670`), the pool and the object itself (`0028F2F0`-`0028F564`).

### Its parts

The interface pump `0028E290` updates the parts in a fixed order ([Subsystem update flags](../Engine-Core/subsystem-update-flags.md)).
What each offset holds:

| Offset | Part |
|---|---|
| `00000` | four `0x20`-byte member cells of the party list, `0028F830(i)` = object + `i` x `0x20` ([Party list](party-list.md)) |
| `00080` | the rolling-counter list the party list registers in; `0028F590` returns its address, or 0 with no HUD |
| `05380` | the part EXP, LP and combo numbers go to ([Combos](../Battle-Actions/combos.md)) |
| `057E0` | the world-object manager ([Loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)) |
| `07EA0` | the selection marker, below |
| `07FB0` | the level-up blink `00296860`; each blink widget `00299D10` follows its unit's screen position (`00299FC0`, `002E9A90`), fades in or out by `01DFE0BC` / 6 a frame and closes itself when its count `+0xC0` runs out |
| `08FA0` | the help block ([Battle menu](battle-menu.md)) |
| `+0xAA60`, `+0xAB30` | the battle menu's cursor block and the battle menu |
| `+0x10EF0`, `+0x10F00` | the current target ring and the ring list |
| `10F10` | the target lines |
| `+0x10F20`, `+0x10F30`, `+0x10F40` | three lists of line marks, below |
| `10F50` | the `targetline_p` picture, loaded on first use by `0024A5A0` |
| `10F78` | the party list widget ([Party list](party-list.md)) |
| `10FC0` | the pool |

### The flag word

Bits of `+0x10F68` that change what the HUD does:

| Bit | Set by | Effect |
|---:|---|---|
| `0` | `00290350(0)`, the handler `0050D1A0` of the debug verb `debug_settargetlinedispstatus` (`0x207F`) | hides the lines and the `+0x10F20` and `+0x10F40` marks (`0028ECA5`) |
| `1` | the pump, from `0030C300` | group 7 of the pump |
| `3` | `00290370` | a target ring is waiting to be built (`0028E2EE`) |
| `4`, `10` | `0028E940(id)`, with the id at `+0x10F60` | the battle menu is built on the next pump (`00290CF0`) |
| `8` | `0028FAF0`; cleared by `0028FA70` | group 12 runs (`003F8EC0(+0xA0)`) |
| `11` | `00290960(1)`, the last step of the field set-up `003C5F00` (`003C5FA5`), run by `00253A30`; cleared by `002908C0` from the matching teardown `003C5E50` (`003C5EF2`) | the `+0x10F30` marks are built only while it is set (`00291027`) |
| `13` | `002906D0`; cleared by `00290610` | `00290CF0` and `0028F970` do nothing |

### The pool

The pool is a first-fit allocator over the `0x8030` bytes at `+0x10FC0`, and every target object below comes from it.
`00272470(pool, size)` writes the `0x30`-byte header, PoolHeader, at the start of the pool:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `PoolBlock*` | head | first block |
| `10` | `PoolBlock*` | cursor | the last block allocated |
| `18` | `u8*` | end | pool address + size, kept to 32 bits |
| `20` | `u8*` | start | pool address + `0x30`, rounded up to 16 |

Each allocation is a `0x20`-byte block header, PoolBlock, followed by the data:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | data | the header's address + `0x20`, the address returned |
| `08` | `u32` | size | the data size, a multiple of 16 |
| `10` | `PoolBlock*` | next | the next block in address order |
| `18` | `PoolBlock*` | prev | the previous block |

### Allocating and freeing

`00273A30(mode, pool, size)` rounds the size up to 16 and returns 0 for size 0:

1. In an empty pool the block goes at `start` when it fits before `end`.
2. With mode 0 it tries the gaps after each block from the cursor forwards (`00276000`), then from the cursor's
   previous block backwards (`002760A0`), then the gap before the head (`00276120`).
3. With another mode it tries the gap before the head first, then forwards from the head.
4. A found block is linked in and becomes the cursor; when none fits it returns 0.

The gap tests compare the low 32 bits of the addresses (`00276000`, `00276120`). Every caller passes mode 0
(`002910AD`, `00291234`, `002913B9`, `00291624`, `00291997`).

`00273B40(pool, data)` unlinks a block: the head moves to the next block when the freed one had no previous, and a
freed cursor moves to its next block, or to its previous one at the end.

### Target lines

`00290320(from, to, kind, flag)` asks for a line from one unit to another through `00291320`:

1. It refuses kind 0, a unit that `00273780` does not resolve, and a line from a unit to itself (`0029134E`, `00291359`).
2. A line with the same ends and kind is returned as it is (`00291366`-`00291392`).
3. Otherwise it takes `0x890` bytes from the pool: state `+0x850` = 1, the ends at `+0x810` and `+0x814`, the kind at
   `+0x840`, the picture `+0x10F50` with its two texture rectangles (`00271140`, `002711E0`), and `003F5370` sets the
   rest; `flag` sets `+0x842` bit 0 and a hold of 20 x `01DFE0B8` at `+0x844` (`002913B9`-`0029152D`).
4. The line is appended to the list at `+0x10F10` (`+0x868` next, `+0x860` previous).

Two callers ask for lines:

- `00328530(unit, target)`, for each target of a unit (`00306010`), when `003126E0` passes the target and
  `0031AA30` gives a kind (`00328555`-`003285A0`);
- the battle menu's list `0027DE30(unit, row)`, for the target `00272E10` gives the row, with the kind from
  `00321060` (`0027DE99`); a row with no target closes the unit's lines (`00290B90`, `0027DE6F`).

### Line states

| State | Meaning |
|---:|---|
| `1`, `2` | shown; `0028F9E0` answers 1 for these two |
| `3` | closing; `00290B70` turns 2 into 3, and `00290B90(unit)` does so for every line from the unit |
| `5` | dead; `00290BE0` gives every line state 5 and sets its `+0x83C` to 0 |

Group 6 of the pump frees the dead lines (`00291B90`, through `00273B40`) and steps the rest (`003F6100`, which runs
`003F5CB0` per line).

### What is drawn

The HUD draw `0028EAB0`, run from the frame's UI step `00252A70` with the word `01E0C2AC`, draws the target rings
every time (`0028C590`, `0028EBA5`). The lines and the `+0x10F20` and `+0x10F40` marks are drawn only when all of
these hold (`0028EC7A`-`0028ED3B`):

- the options record exists (`002DE040`) and Target Lines is on (`002DDE00`, dword 1 bit 22,
  [Game settings](../Saving-Loading-And-Settings/game-settings.md));
- the word has bit 0;
- flag bit 0 is clear.

The selection marker is drawn after them (`0028C970`, `0028EDC9`).

### The target ring

`00290370(unit, other, style)` asks for the ring (`00290370`-`002903C5`):

- with `other` set it moves the selection marker to the unit instead (`0028CA40`);
- otherwise it stores the unit at `+0x10F6C`, 0 at `+0x10F70` and the style at `+0x10F72`, and sets flag bit 3.

Its caller `002BF0E0` (thunk `002BE080`) picks the style from what the unit is:

| Unit | Style | Colour index (`00916010`) |
|---|---:|---:|
| kind 2: a unit that `00273710` passes, not KO, Stone or status bit 31 | `3` | `0` |
| one of the four party members (`00273880`) | `1` | `0` |
| actor class 1, 2 or 7 (`00263C20`) | `2` | `1` |
| actor class 3 | `0` | `4` |
| anything else | `1` | `0` |

Kind 1 closes the rings; kind 6 sends the unit to the selection marker (`002BF15F`-`002BF167`); any other kind first
needs `00273710` to pass and closes the rings otherwise (`002BF19D`-`002BF1A6`).

### Building and closing rings

Group 3 of the pump calls `002917E0(manager, unit, 0, style)` while bit 3 is set:

1. It clears bit 3. A current ring below state 3 is kept for the same unit, or turned to the new unit with state 1,
   the new colour and a faster spin, `+0xD44` + 0.314 x `01DFE0BC`, capped at 0.419 x `01DFE0BC` (`0029188E`-`002918DD`).
2. Otherwise the old rings fade when there is at most one (`00291954`-`00291975`); with more, bit 3 is set again for
   the next frame.
3. It takes `0xD80` bytes from the pool, or sets bit 3 again when the pool is full (`00291B5F`).
4. It sets state 1 and the unit, converts the picture's sprite into texture coordinates (`00291A8F`), writes the
   draw packets with the colour index (`0028C620`, `00291ADB`) and appends the ring (`+0xD70` next, `+0xD68` previous).

Each pump `0028C4C0` steps every ring (`0028BB50`) and `0028D1C0` frees the rings in state 5 (`0028FA50`).
`0028C4F0(list)` closes rings: those in states 0, 1 and 5 become 5, those in state 4 are left, and the others start
the fade, state 3. `0028C560` puts every ring in state 5 and `0028C850` counts them.

| Closer | Also |
|---|---|
| `00290990` | fades every ring, clears the current one and fades the selection marker (`0028C940`) |
| `002909F0` | the same, then kills and frees every ring (`0028C560`, `0028D1C0`) |
| `00290B10` | fades every ring and marks a fading current ring with `+0xD4C` bit 3 |

### The selection marker

The `0x80`-byte marker at `+0x7EA0` keeps two slots. `0028CA40(marker, unit)` starts it on a unit's position
(`002E7F70`), or on a new unit fades the old slot out and starts the other. Group 16 of the
pump (`0028C870`) turns it by 10 x `01DFE0BC` degrees a frame and fades it in or out by 32 / `01DFE0B4` a frame.

`0028C970` draws it with `0028D260` and, per slot, `0028D8A0`, whose `0028D460` draws three sprites 2.094 radians
apart. Both read a colour track at `00915FB0` (four keys, `0028CB90`) and scale it by `0028CD10(angle)`:

```python
0028CD10(a) = 0                                            a >= pi = 128 x sin((a / 0.785398) x pi/2)              a <= pi/4 = 128 x sin(pi/2 - ((a - pi/4) / 2.356194) x pi/2)   otherwise
```

### Line marks

| List offset | Size | Built by | From |
|---|---|---|---|
| `10F20` | 2512 | `002915C0`, one per unit handle `+0x980` or position `+0x960` | `0028E9F0`, called by the line step `003F5CB0` (`003F5F7D`) |
| `10F40` | 128 | `002911D0`, found by unit through `003F3580` | `0028EA20`, called by the battle menu's `0027DC10` |
| `10F30` | 832 | `00291010`, only while flag bit 11 is set | `00290300`, called by `0035DAF0` |

`0027DC10(actor, unit, action, keep)` asks for a `+0x10F40` mark when `0031AB80` reports kind 1, `keep` is 0 and
`00273710` passes the unit; it first drops the unit's old mark (`00290CD0`, `003F35A0`).

### Keyframe tracks

HUD animations read short tracks of keys. `00271AB0(out, keys, count, t)` uses 12-byte keys:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i16` | x | interpolated |
| `02` | `i16` | y | interpolated |
| `04` | `u16` | time | the key's time |
| `06` | `u8` | a | interpolated |
| `07` | `u8` | b | interpolated |
| `08` | `u16` | curve | how the segment that ends at this key moves |
| `0A` | `i16` | w | interpolated into a 32-bit result at `out + 8` |

It finds the segment whose times hold `t`, the last one past the end, and blends by `p`, the fraction of the
segment: curve 1 gives `sin(p x pi/2)`, curve 2 `1 - sin((1 - p) x pi/2)`, any other `p`. Past the last key it keeps
blending along the last segment.
`0028CB90` does the same over 8-byte keys `{i16 value, u8, u8, i16 curve, u16 time}` and blends through `002752E0`.

### Entry points

| Function | Does |
|---|---|
| `00254E70` | runs the HUD switch `00251F40` with the saved value `[020927E8]` |
| `002509A0` | `0035C880(0xC, 1)`, which clears bits 2 and 3 of the battle mode register `022C83EC` and sets bit 0 (`002509B6`), then `0028E5F0`; run by `002678C0` and `0026E0D0` while `02099DA7` is 0, which then set it to 1 |
| `0028E5F0` | sets or clears the battle mode register's bit 1 from the Escape Mode arming (`003669D0`), stops the arming sound (`00366990`) and closes the widget at `[0209C300]` (`002970C0`) |
| `0028E110(text, kind, colour, arg)` | posts a help message: colour `0x80808080` when none is given, two times from `002BDB20` (kinds 1-5 from the bytes at `0209E610`, else 30 x `01DFE0B4`; and 150 x `01DFE0B4`), through `002BDB00`; called by `0035B990` |
| `0028E900` | resets the help block (`002BE050`), which also closes the rings (`00290990`) |
| `0028FEA0(text, arg)` | closes the help window (`002BE020`) and opens a new one (`002BE1A0`); called by `0027B880` |
| `00290C60`, `00290C80` | write the open help window's word `+0x298`, or `+0x294` with its `+0x280` bit 5, and the block's pending `+0x1040` or `+0x103C` when no window is open; called by `0027B880` |
| `00290190` | forwards to the return stub `0016D6A0` and does nothing; the HUD switch calls it with 0 (`00251F8A`) |

The Escape Mode register and arming are on [Escape](../Controls-And-Input/escape.md).

## Modding notes

- Every target line, ring and mark shares one `0x8030`-byte pool; when it is full a ring request waits a frame and a
  line is not made.
- Target Lines hides only the lines and the `+0x10F20` and `+0x10F40` marks; the target ring, the selection marker
  and the `+0x10F30` marks stay.
- A ring's colour is a palette index from the four bytes at `00916010`.

## Related

- [Battle menu](battle-menu.md) - the menu, help line and gauges the HUD holds.
- [Party list](party-list.md) - the member rows the HUD holds.
- [Subsystem update flags](../Engine-Core/subsystem-update-flags.md) - the pump that steps each part.
- [Menu sprites](menu-sprites.md) - the `targetline_p` picture.
- [Widgets](widgets.md) - the widget model the parts use.
</content>
</invoke>
