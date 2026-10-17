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

The HUD is one `10FD0`<sub>h</sub>-byte object whose pointer is at `0209BE80`:

1. `0028F8B0` first tears down any old one with `0028F2F0`, then allocates the object through `00271420(10FD0h)`
   when the pointer is empty and initialises it with `00291750` (`0028F8CF`, `0028F8DE`).
2. `00291750` clears all `10FD0`<sub>h</sub> bytes, allocates the `8030`<sub>h</sub>-byte pool into `+10FC0`<sub>h</sub> and prepares it
   (`00272470`), builds the part at `+5380`<sub>h</sub> (`0028A080`), the selection marker `+7EA0`<sub>h</sub> (`0028CA30`), the help
   block `+8FA0`<sub>h</sub> (`002BE450`, `002BE0A0`) and the world-object part `+57E0`<sub>h</sub> (`003FA760`), and sets
   `+10F90`<sub>h</sub> to -1 and byte `+10FA2`<sub>h</sub> to 1.
3. `0028F8B0` then clears the two rolling-counter tables (`00296260`, `00296240`), resets the counter list `+80`<sub>h</sub>
   (`004FE3C0`), writes 1 to `+AA44`<sub>h</sub>, sets flag bit 5 and closes the widget kept at `+10F88`<sub>h</sub> (`0028F8E3`-`0028F952`).

`0028F8B0` runs from `0035C560` (`0035C57F`). `0028F2F0` releases every list in the pool, the two `+10F74`<sub>h</sub> and
`+10F78`<sub>h</sub> widgets through `00274840` (`002446E0`, `002473B0`, `002482E0`: focus, message 18 and release), the
level-up blink part (`00296670`), the pool and the object itself (`0028F2F0`-`0028F564`).

### Its parts

The interface pump `0028E290` updates the parts in a fixed order ([Subsystem update flags](../Engine-Core/subsystem-update-flags.md)).
What each offset holds:

| Offset | Part |
|---|---|
| `00000`<sub>h</sub> | four `20`<sub>h</sub>-byte member cells of the party list, `0028F830(i)` = object + `i` x `20`<sub>h</sub> ([Party list](party-list.md)) |
| `00080`<sub>h</sub> | the rolling-counter list the party list registers in; `0028F590` returns its address, or 0 with no HUD |
| `05380`<sub>h</sub> | the part EXP, LP and combo numbers go to ([Combos](../Battle-Actions/combos.md)) |
| `057E0`<sub>h</sub> | the world-object manager ([Loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)) |
| `07EA0`<sub>h</sub> | the selection marker, below |
| `07FB0`<sub>h</sub> | the level-up blink `00296860`; each blink widget `00299D10` follows its unit's screen position (`00299FC0`, `002E9A90`), fades in or out by `01DFE0BC` / 6 a frame and closes itself when its count `+C0`<sub>h</sub> runs out |
| `08FA0`<sub>h</sub> | the help block ([Battle menu](battle-menu.md)) |
| `+AA60`<sub>h</sub>, `+AB30`<sub>h</sub> | the battle menu's cursor block and the battle menu |
| `+10EF0`<sub>h</sub>, `+10F00`<sub>h</sub> | the current target ring and the ring list |
| `10F10`<sub>h</sub> | the target lines |
| `+10F20`<sub>h</sub>, `+10F30`<sub>h</sub>, `+10F40`<sub>h</sub> | three lists of line marks, below |
| `10F50`<sub>h</sub> | the `targetline_p` picture, loaded on first use by `0024A5A0` |
| `10F78`<sub>h</sub> | the party list widget ([Party list](party-list.md)) |
| `10FC0`<sub>h</sub> | the pool |

The `+5380`<sub>h</sub> part's draw `00289A10` queues each number through `0028A790(entry, list, buffer, alpha)`, unless
the entry's `+14`<sub>h</sub> is set: a sprite at the entry's position with w = -1, the picture of `0035D3D0` at its cell,
and a size and alpha from the 5-key track `00915F68` at the entry's time `+10`<sub>h</sub>; the alpha is scaled by
`00272DE0()` x `alpha` while `+0C`<sub>h</sub> is set and is 0 otherwise.

### The flag word

Bits of `+10F68`<sub>h</sub> that change what the HUD does:

| Bit | Set by | Effect |
|---:|---|---|
| `0` | `00290350(0)`, the handler `0050D1A0` of the debug verb `debug_settargetlinedispstatus` (`207F`<sub>h</sub>) | hides the lines and the `+10F20`<sub>h</sub> and `+10F40`<sub>h</sub> marks (`0028ECA5`) |
| `1` | the pump, from `0030C300` | group 7 of the pump |
| `3` | `00290370` | a target ring is waiting to be built (`0028E2EE`) |
| `4`, `10` | `0028E940(id)`, with the id at `+10F60`<sub>h</sub> | the battle menu is built on the next pump (`00290CF0`) |
| `8` | `0028FAF0`; cleared by `0028FA70` | group 12 runs (`003F8EC0(+A0h)`) |
| `11` | `00290960(1)`, the last step of the field set-up `003C5F00` (`003C5FA5`), run by `00253A30`; cleared by `002908C0` from the matching teardown `003C5E50` (`003C5EF2`) | the `+10F30`<sub>h</sub> marks are built only while it is set (`00291027`) |
| `13` | `002906D0`; cleared by `00290610` | `00290CF0` and `0028F970` do nothing |

### The pool

The pool is a first-fit allocator over the `8030`<sub>h</sub> bytes at `+10FC0`<sub>h</sub>, and every target object below comes from it.
`00272470(pool, size)` writes the `30`<sub>h</sub>-byte header, PoolHeader, at the start of the pool:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `PoolBlock*` | head | first block |
| `10`<sub>h</sub> | `PoolBlock*` | cursor | the last block allocated |
| `18`<sub>h</sub> | `u8*` | end | pool address + size, kept to 32 bits |
| `20`<sub>h</sub> | `u8*` | start | pool address + `30`<sub>h</sub>, rounded up to 16 |

Each allocation is a `20`<sub>h</sub>-byte block header, PoolBlock, followed by the data:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | data | the header's address + `20`<sub>h</sub>, the address returned |
| `08`<sub>h</sub> | `u32` | size | the data size, a multiple of 16 |
| `10`<sub>h</sub> | `PoolBlock*` | next | the next block in address order |
| `18`<sub>h</sub> | `PoolBlock*` | prev | the previous block |

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
3. Otherwise it takes `890`<sub>h</sub> bytes from the pool: state `+850`<sub>h</sub> = 1, the ends at `+810`<sub>h</sub> and `+814`<sub>h</sub>, the kind at
   `+840`<sub>h</sub>, the picture `+10F50`<sub>h</sub> with its two texture rectangles (`00271140`, `002711E0`), and `003F5370` sets the
   rest; `flag` sets `+842`<sub>h</sub> bit 0 and a hold of 20 x `01DFE0B8` at `+844`<sub>h</sub> (`002913B9`-`0029152D`).
4. The line is appended to the list at `+10F10`<sub>h</sub> (`+868`<sub>h</sub> next, `+860`<sub>h</sub> previous).

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
| `5` | dead; `00290BE0` gives every line state 5 and sets its `+83C`<sub>h</sub> to 0 |

Group 6 of the pump frees the dead lines (`00291B90`, through `00273B40`) and steps the rest (`003F6100`, which runs
`003F5CB0` per line).

The functions that keep and draw the lines:

| Function | Does |
|---|---|
| `003F5070(list)` | run by `00290C00`: gives state 5 to every line whose either end no longer resolves (`003588B0`), clearing `+842`<sub>h</sub> bit 1 and `+83C`<sub>h</sub> |
| `00270F50(out, points, n)` | the curve through a line's points, for the line set-up `003F6370`, which passes three points (the two ends and one raised between them) and stores the count, 33, at `+7E0`<sub>h</sub>. It runs `00270F60` with s = 16, which clears the work block `0209A770` and keeps s at `0209A76C`; `00275CA0` stores the points relative to the first and adds a mirrored point (2a - b) beyond each end; `00275570` samples a uniform cubic B-spline (weights / 6), s points a segment, ends pinned, and returns (n - 1) x s + 1 |
| `003F62D0(line)` | run by the line step `003F5CB0`: rebuilds the packet header for the `+7E0`<sub>h</sub> points (`003F65C0`) and the points' brightness and alpha (`003F6A10`), from the fractions `+824`<sub>h</sub> and `+828`<sub>h</sub> and the hold `+846`<sub>h</sub> against 15 x `01DFE0B4` |
| `003F5100(list, arg)` | draws the lines with `+842`<sub>h</sub> bit 1, sorted by the distance from the camera `02AED5F0` to their midpoint (`+888`<sub>h</sub>; tree links `+870`<sub>h</sub>, `+878`<sub>h</sub>, `+880`<sub>h</sub>), walking the tree with `003F6960` |
| `003F5430(line)` | draws one line: a ribbon of quads through its points, 0.15 to each side (`003F6130`, `003F6200`), with the `targetline_p` cell its kind `+840`<sub>h</sub> gives (`002713B0`); while `+824`<sub>h</sub> is below 1 it adds the six-vertex end piece from `01EFF3E0` (`003F6690`, `003F6850`) |
| `003F5390`, `003F67C0` | write the GS state records of the line pass (the template at `02064AB0`, then TEST_1 `53001`<sub>h</sub> and ALPHA_1) through `002712E0` |

`002713B0(kind)` turns a line or mark kind into its palette cell: 1 gives 1, 2 gives 5, 4 gives 3 and any
other 0.

### What is drawn

The HUD draw `0028EAB0`, run from the frame's UI step `00252A70` with the word `01E0C2AC`, draws the target rings
every time (`0028C590`, `0028EBA5`). The lines and the `+10F20`<sub>h</sub> and `+10F40`<sub>h</sub> marks are drawn only when all of
these hold (`0028EC7A`-`0028ED3B`):

- the options record exists (`002DE040`) and Target Lines is on (`002DDE00`, dword 1 bit 22,
  [Game settings](../Saving-Loading-And-Settings/game-settings.md));
- the word has bit 0;
- flag bit 0 is clear.

The selection marker is drawn after them (`0028C970`, `0028EDC9`).

### The draw pass

`0028EAB0` runs in this order:

1. `003F1220` points a packet record at a 32 KB stack buffer, and `003F12D0` empties two depth lists that
   collect sprites placed in the world; the second gets bit 0 of its `+18`<sub>h</sub>.
2. It draws the rings (`0028C590`), the part `003F8C70(+A0h)` unless `00236760` answers non-zero, the
   world-object part (`003FA570`, `003FA600`) when `+7C70`<sub>h</sub> is set, and the `+10F30`<sub>h</sub> marks (`003F7200`)
   when the word has bit 3.
3. With the conditions above it draws the lines (`003F5100`), the `+10F20`<sub>h</sub> marks (`003F2CF0`) and the
   `+10F40`<sub>h</sub> marks (`003F3260`).
4. After the "Gaussian Filter" and "display UI 2" markers it draws the part at `+10F80`<sub>h</sub> (`002C62B0`, the
   overhead gauges on [Battle menu](battle-menu.md)) when the word has bit 2, and the selection marker.
5. Last, `003F0170` draws both depth lists and `003F1530` the screen-space list.

| Function | Does |
|---|---|
| `003F0170(list)` | projects each sprite (`002720F0`, the view `02AEDDB0`) to its depth `+C8`<sub>h</sub>, keeps those in front with screen x and y inside (0, 4096), sorts them by depth (`003F19D0`; links `+B0`<sub>h</sub>, `+B8`<sub>h</sub>, `+C0`<sub>h</sub>) and draws them in order through `003F1A60`; the next sprite is at `+D0`<sub>h</sub>. The first list uses the depth test (TEST_1 `53001`<sub>h</sub>), the second does not (`1001`<sub>h</sub>) |
| `003F1A60(sprite, batch)` | draws one sprite at alpha `80`<sub>h</sub>; with `+EA`<sub>h</sub> bit 0 the alpha drops when the camera looks at it from behind the focus unit (`003590D0`, a dot product below -0.9, eased over distances 1 to 20). It starts a new batch after 24 sprites or a picture change, then runs `003F0610` |
| `003F0610(batch, sprite)` | computes the four corners and the texture rectangle; the kind `+F0`<sub>h</sub> picks the picture: -1 `chain_item` (1024 x 1024), -2 `targetline_p`, -3 `chainflash` (1024 x 512), any other the picture at `+E0`<sub>h</sub> |
| `003F1530(list)` | the screen-space list: projects each entry (from the list's `+40`<sub>h</sub>, next at `+F8`<sub>h</sub>) unless `+EC`<sub>h</sub> bit 0 is set, clips it (`00249EE0`), sorts by depth `+120`<sub>h</sub> (`003F1940`; links `+108`<sub>h</sub>, `+110`<sub>h</sub>, `+118`<sub>h</sub>) and draws each with `002B0280`; `003BBB60` also calls it |
| `003F12E0(sprite, picture, code, frame)` | binds a sprite to a picture cell found through the picture header's tables (`+40`<sub>h</sub>, `+42`<sub>h</sub>, `+44`<sub>h</sub>): the picture at `+E0`<sub>h</sub>, the texture rectangle (`00271140`) at `+30`<sub>h</sub>-`+3C`<sub>h</sub>. `003F1430` adds a frame offset; the selection marker's `0028D260` and `0028D460` use it |

`003F1530` (`003F15B4`) and the widget draw `00247AE0` (`00247B84`, `00247C32`) take their projection from
`008626C0(m, f, sx, sy, ox, oy, z0, z1, n, far)`. It multiplies (`00217150`) a perspective matrix of focal length `f`
(`m00 = m11 = f`, `m23 = 1`, `m33 = 0`) by a screen matrix with the scales `sx`, `sy`, the offsets `ox`, `oy` and the
depth terms below, then transposes the product:

```python
k = (z1 - z0) / (far - n)
m22 = n x far x k
m23 = (z0 x far - z1 x n) / (far - n)
```

### The target ring

`00290370(unit, other, style)` asks for the ring (`00290370`-`002903C8`):

- with `other` set it moves the selection marker to the unit instead (`0028CA40`);
- otherwise it stores the unit at `+10F6C`<sub>h</sub>, 0 at `+10F70`<sub>h</sub> and the style at `+10F72`<sub>h</sub>, and sets flag bit 3.

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
   the new colour and a faster spin, `+D44`<sub>h</sub> + 0.314 x `01DFE0BC`, capped at 0.419 x `01DFE0BC` (`0029188E`-`002918DD`).
2. Otherwise the old rings fade when there is at most one (`00291954`-`00291975`); with more, bit 3 is set again for
   the next frame.
3. It takes `D80`<sub>h</sub> bytes from the pool, or sets bit 3 again when the pool is full (`00291B5F`).
4. It sets state 1 and the unit, converts the picture's sprite into texture coordinates (`00291A8F`), writes the
   draw packets with the colour index (`0028C620`, `00291ADB`) and appends the ring (`+D70`<sub>h</sub> next, `+D68`<sub>h</sub> previous).

Each pump `0028C4C0` steps every ring (`0028BB50`) and `0028D1C0` frees the rings in state 5 (`0028FA50`).
`0028C4F0(list)` closes rings: those in states 0, 1 and 5 become 5, those in state 4 are left, and the others start
the fade, state 3. `0028C560` puts every ring in state 5 and `0028C850` counts them.

| Closer | Also |
|---|---|
| `00290990` | fades every ring, clears the current one and fades the selection marker (`0028C940`) |
| `002909F0` | the same, then kills and frees every ring (`0028C560`, `0028D1C0`) |
| `00290B10` | fades every ring and marks a fading current ring with `+D4C`<sub>h</sub> bit 3 |

A ring is two halves of six segments. `0028C590` draws each ring with `+D4C`<sub>h</sub> bit 0:

| Function | Does |
|---|---|
| `0028D030(ring)` | for a ring with `+D50`<sub>h</sub> = 1: copies the six 13-record segments of each half (`+000`<sub>h</sub>, `+5D0`<sub>h</sub>) through the VIF writer, after `003F3010` puts the view `02AEDDB0` and the camera `02AED5F0` into each half's matrix block (`+4E0`<sub>h</sub>, `+AB0`<sub>h</sub>) |
| `0028D980(ring)` | for other rings: the same with 10-record segments, through the sprite batcher too, binding `targetline_p` at the cell `+D7C`<sub>h</sub> + 2 x `+D78`<sub>h</sub>; `0028DC00` draws each segment |
| `003F26F0(segments, out, n, ...)`, `003F2A70(segments, out, n, ...)` | build `n` segments round the circle, 360 / `n` degrees each, as 13-record (`D0`<sub>h</sub>) or 10-record (`A0`<sub>h</sub>) packets, and copy them out (`00271290`); `0028C620` uses both |
| `0028CF80(ring, v)` | the pulse `0028BB50` runs: for `+D50`<sub>h</sub> = 1 it writes sin(2 pi / (2 x `+D48`<sub>h</sub>)) x v into `+A0`<sub>h</sub> of each `D0`<sub>h</sub> segment (`003F3050`), otherwise v into `+80`<sub>h</sub> of each `A0`<sub>h</sub> segment (`003F25D0`) |

### The selection marker

The `80`<sub>h</sub>-byte marker at `+7EA0`<sub>h</sub> keeps two slots. `0028CA40(marker, unit)` starts it on a unit's position
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
| `10F20`<sub>h</sub> | 2512 | `002915C0`, one per unit handle `+980`<sub>h</sub> or position `+960`<sub>h</sub> | `0028E9F0`, called by the line step `003F5CB0` (`003F5F7D`) |
| `10F40`<sub>h</sub> | 128 | `002911D0`, found by unit through `003F3580` | `0028EA20`, called by the battle menu's `0027DC10` |
| `10F30`<sub>h</sub> | 832 | `00291010`, only while flag bit 11 is set | `00290300`, called by `0035DAF0` |

`0027DC10(actor, unit, action, keep)` asks for a `+10F40`<sub>h</sub> mark when `0031AB80` reports kind 1, `keep` is 0 and
`00273710` passes the unit; it first drops the unit's old mark (`00290CD0`, `003F35A0`).

The `+10F20`<sub>h</sub> and `+10F40`<sub>h</sub> marks:

| Function | Does |
|---|---|
| `003F2580(list, mark)` | appends a `+10F20`<sub>h</sub> mark (next `+9B0`<sub>h</sub>, previous `+9B8`<sub>h</sub>); `002915C0` uses it and `003F2600` |
| `003F2600(mark, rect)` | sets a new `+10F20`<sub>h</sub> mark: six 10-record segments (`003F2A70`), the scale `+998`<sub>h</sub> = 1.0, two sprite blocks (`003F2F20`) and two label heights, y / 2 - y / 10 and y / 2 + h + y / 10, from the rectangle |
| `003F2CF0(list)` | draws each `+10F20`<sub>h</sub> mark with `+991`<sub>h</sub> bit 0: twelve segments with the picture `+988`<sub>h</sub> at the cell its kind `+990`<sub>h</sub> gives, the alpha scaled by `+998`<sub>h</sub> |
| `003F3080(mark, on)` | sets or clears `+991`<sub>h</sub> bit 3; `002907F0` calls it |
| `003F34D0(list, mark)` | appends a `+10F40`<sub>h</sub> mark (next `+70`<sub>h</sub>, previous `+78`<sub>h</sub>); `002911D0` uses it and `003F3510` |
| `003F3510(mark, picture, ...)` | sets a new `+10F40`<sub>h</sub> mark: the header `00275550(mark, 80h)`, `+60`<sub>h</sub> from `00272F30`, then `003F3660` binds the picture cell, sets the shown bit 0 of `+50`<sub>h</sub>, the colour (255, 255, 255, 127) and the scale 0.25 |
| `003F30D0(mark)` | the step `003F31B0` runs per `+10F40`<sub>h</sub> mark: it clears the shown bit when the unit no longer passes `002713E0`, fades `+4C`<sub>h</sub> in or out by 0.5 x `01DFE0BC`, advances the pulse `+68`<sub>h</sub> (reset at 0.99) and sets bit 1 once faded out |
| `003F3260(list)` | draws each `+10F40`<sub>h</sub> mark as two sprites 90 degrees apart (`003F3710`) at the angle `003F35C0` gives, first a pulsing copy and then the mark |
| `003F30A0(list, fn)` | walks a list linked at `+70`<sub>h</sub> and calls `fn` for each entry; the teardown `0028F2F0` uses it |

The `+10F30`<sub>h</sub> marks join two units, a at `+2D0`<sub>h</sub> and b at `+2D4`<sub>h</sub>:

| Function | Does |
|---|---|
| `003F73F0(mark, a, b, rect, picture)` | sets a new mark: the header `00275550(mark, 340h)`, `+2EC`<sub>h</sub> bits 1 and 2 with the units' positions (`002713E0` into `+280`<sub>h</sub> and `+290`<sub>h</sub>), the sprite blocks (`003F7CC0`) and state 1 at `+2F0`<sub>h</sub> |
| `003F7380(list, mark)`, `003F73D0(list, a)` | append a mark (next `+300`<sub>h</sub>, previous `+308`<sub>h</sub>), and find the mark whose unit a is `a` |
| `003F7490(list)` | run by `00290C00`: state 4 for every mark whose unit a or b no longer resolves (`003588B0`) |
| `003F6FD0(mark)` | closes a mark for `002908C0` and `00291010`: state 1 becomes 4, other states except 0 and 4 become 3 |
| `003F77F0(mark)` | when both units are set, a has a party record (`002732E0`) whose `+5C`<sub>h</sub> is not -1 and `002739D0` passes, binds the `targetline_p` cell 4 when `0030BEF0` answers above 0 and 1 otherwise (`00271650`); otherwise it closes the mark like `003F6FD0` |
| `003F7BC0(mark)` | eases `+2E0`<sub>h</sub> by 0.35 a step toward the gap between the two units, less both radii (`002645D0`, plus 1 for b), clamped to 10 and divided by 10 |
| `003F7760(mark)` | turns the orientation `+2A0`<sub>h</sub> by 0.35 toward the direction from a to b (`00270A10`, `00270CF0`) |
| `003F7610(mark)`, `003F74F0(...)` | build the two halves' matrices from the orientation (`00270720`), scaled by `+2E0`<sub>h</sub> and raised by a's radius x 1.3, or x 1.2 for the second half, at a's position |
| `003F7200(list)` | draws the marks with `+2EC`<sub>h</sub> bit 0, farthest from the camera first (distance `+328`<sub>h</sub>; links `+310`<sub>h</sub>, `+318`<sub>h</sub>, `+320`<sub>h</sub>), each with `003F70F0`, which binds `targetline_p` at the cell `+330`<sub>h</sub> + 2 x `+32C`<sub>h</sub> and draws both halves as the 35 sprites of the table `01EFF4E0` (`003F7930`) |

`003F7BC0`, `003F7760`, `003F7610` and `003F77F0` are run by group 4's step `003F6BB0`.

### The overhead display

The part at `+10F80`<sub>h</sub>, `1D90`<sub>h</sub> bytes, draws marks over units: a status mark for each unit it lists, a box at
`+1B80`<sub>h</sub> and two name boxes. `002C63D0`, run by `0028FF80` and `00290060`, clears it, links its 95 `40`<sub>h</sub>-byte unit
entries into the free list `+1D60`<sub>h</sub> and sets the fade distances `+1D7C`<sub>h</sub> = 5.0 and `+1D80`<sub>h</sub> = 17.0.

Group 15 of the pump, `002C6180`, steps it:

1. It clears every entry's shown bit (`+17`<sub>h</sub> bit 0) and sets the closing bit 1 of both name boxes (`+19B4`<sub>h</sub>).
2. With `+1D7A`<sub>h</sub> bit 9 it runs `002C8D60`, which calls `002C6F70` for each unit of the list `0035D500`
   (`0035D510` units), stopping when one returns 0.
3. It steps the box at `+1B80`<sub>h</sub> (`002C6BE0`) and the name boxes (`002C6B50`), and fades the whole part
   `+1D78`<sub>h</sub> toward `80`<sub>h</sub>, or toward 0 while `+1D7A`<sub>h</sub> bit 3 is set, by 32 / `[01DFE0B4]` a frame.
4. It keeps `0028F5B0()` at `+1D88`<sub>h</sub>, frees the entries left unshown (`002C8DF0`) and copies `02092730` to
   `+1D84`<sub>h</sub>.

| Function | Does |
|---|---|
| `002C8A20(list, entry)`, `002C7620(list, entry)` | append an entry to the list `+1D70`<sub>h</sub> (next `+18`<sub>h</sub>, previous `+20`<sub>h</sub>), and unlink one |
| `002C8DF0(part)` | returns every entry whose shown bit is clear to the free list, and clears the `+1B80`<sub>h</sub> box's entry `+1D30`<sub>h</sub> when it was one of them |
| `002C8A60(part, entry)` | gives an entry a name box: the box already showing its unit, else a free one, else the box after the last one used (`+1D7A`<sub>h</sub> bit 7 flips). A new box is cleared and filled by `002C8BC0`; the unit goes to `+1B0`<sub>h</sub> with bit 0 set and bit 1 clear in `+1B4`<sub>h</sub> |
| `002C6B50(part)` | fades each open name box in, or out while its bit 1 is set, by 32 / `[01DFE0B4]` a frame up to `80`<sub>h</sub>; a box faded out loses bit 0 |
| `002C6BE0(part, box)` | the same for the box at `+1B80`<sub>h</sub>, also moving its ramps `+1BC`<sub>h</sub>, `+1BE`<sub>h</sub> and `+1D0`<sub>h</sub>; a box faded out drops its entry |
| `002C62B0(part, ...)` | the draw: each entry through `002C7660`, with bit 10 of the script hold mask (`002E0FA0`) and the focus unit, then the `+1B80`<sub>h</sub> box (`002C7F90`) and each open name box at the part's alpha times the box's (`003F14D0`) |
| `002C7B10(entry, ...)` | the status mark over a unit: the cell `300`<sub>h</sub> sprite of the status `+16`<sub>h</sub> (`003F12E0`) at the alpha `+15`<sub>h</sub>. Statuses 4, 9 and 24 pulse in size along the track `00916E90`, status 12 turns along `00916ED0`; with `+17`<sub>h</sub> bit 2 it adds the status numbers (`002C84E0`) |
| `002C8920(unit, alpha, list, ...)` | queues the cell `E00`<sub>h</sub> sprite of the picture `0035D460` returns over a unit; `002C7660` asks for it for the unit `0035BAD0` names when `003135C0` and `00273460` answer non-zero |
| `002C69A0(pos, sprite, cell, alpha, rgba, picture)` | fills a sprite from a picture cell: the position with w = -1, the texture rectangle, the colour bytes with alpha x `rgba.a` / 128, and half the cell's size to each side; `002C7F90`, `002C8310` and `002C8820` use it |
| `002C6450(part)` | answers whether the focus unit's entry is drawn at full alpha (entry `+14`<sub>h</sub> x `+1D78`<sub>h</sub> at least `4000`<sub>h</sub>), or, with no entry, whether the part is at `80`<sub>h</sub>. A scan of the image for calls, jumps and `lea` to it finds none |

### Keyframe tracks

HUD animations read short tracks of keys. `00271AB0(out, keys, count, t)` uses 12-byte keys:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i16` | x | interpolated |
| `02`<sub>h</sub> | `i16` | y | interpolated |
| `04`<sub>h</sub> | `u16` | time | the key's time |
| `06`<sub>h</sub> | `u8` | a | interpolated |
| `07`<sub>h</sub> | `u8` | b | interpolated |
| `08`<sub>h</sub> | `u16` | curve | how the segment that ends at this key moves |
| `0A`<sub>h</sub> | `i16` | w | interpolated into a 32-bit result at `out + 8` |

It finds the segment whose times hold `t`, the last one past the end, and blends by `p`, the fraction of the
segment: curve 1 gives `sin(p x pi/2)`, curve 2 `1 - sin((1 - p) x pi/2)`, any other `p`. Past the last key it keeps
blending along the last segment.
`0028CB90` does the same over 8-byte keys `{i16 value, u8, u8, i16 curve, u16 time}` and blends through `002752E0`.
`002C6DC0(out, keys, n, t)` does it for the overhead display (`002C7F90`, `002C84E0`) over 8-byte keys
`{i8, i8, u8 curve, u8, i16 time, i16}`, blending through `002752E0`.

### Vector helpers

The HUD parts and the screens around them share a few small vector helpers:

| Function | Does |
|---|---|
| `00270550(v)` | the length of the x, y, z lanes; the ring step `0028BB50`, the overhead gauges (`002C6F70`), the world objects (`003F8FE0`) and `003F7BC0` among its ten callers |
| `00270880(out, v, s)`, `002708B0(out, v, s)` | scale all four lanes, or x, y and z keeping w |
| `00202DE0(out, v)`, `00202C50(out, m, p)` | normalise x, y, z through `00216660`, giving all four lanes 0 when the squared length is NaN, infinite or at most 1.1754944e-38; and transform a point through `00216FC0`, x · row 0 + y · row 1 + z · row 2 + row 3, with w = 0 |
| `00270230(out, rect, dx, dy)` | moves both corners of a rectangle by (dx, dy); the marker sprite `0028D460` uses it |
| `00270720(out, q)` | the rotation matrix of the quaternion (x, y, z, w) |
| `00270A10(out, dir)` | the orientation facing a direction: pitch -atan2(y, max(abs x, abs z)) and yaw atan2(x, z), each kept in (-pi, pi], as a quaternion (`00270B40`) |
| `00270CF0(out, a, b, t)` | spherical interpolation from a (t = 0) to b (t of 1 or more), the short way round |
| `00270420(out, points, n)`, `00270500(lengths, n, d)` | the n - 1 segment lengths of a chain of points; and the fractional segment index at which their running sum reaches d, or -1.0 past the end. `005621A0`, which draws the `w_line01` path, uses both |

### The active log

The active log, procedure `002BE4F0` built by `002BDCE0` under the field HUD root, shows one battle-log line at a time.
The root `00253780` reaches that builder through `0035C630` (`002537E6`), which runs `002BDCE0` (through `0028E220`),
`0028FF80`, the chocobo menu task builder `003CA280`, the HUD widget builder `003C98E0` and then `00290450(1)`.

`0028E110` posts a line through `002BDB00` ([Battle log](../Battle-Actions/battle-log.md)), and `002BE8D0` files it
as a `198`<sub>h</sub>-byte record: the text, `180`<sub>h</sub> bytes copied by `00254F30`, its colour at `+180`<sub>h</sub>, the hold time at
`+184`<sub>h</sub>, an in-use bit at `+186`<sub>h</sub> and half its width at `+187`<sub>h</sub> (`0029CD00`). Records move between three lists
linked through `+188`<sub>h</sub> and `+190`<sub>h</sub>:

| List | Offset | Holds |
|---|---|---|
| queued | `+4098`<sub>h</sub> | posted lines; `002BF480` takes the first |
| shown | `+40A0`<sub>h</sub> | the line on screen and the one sliding in |
| free | `+40A8`<sub>h</sub> | spent records; a new line takes the first, or the oldest queued line's record when the list is empty |

Each tick `002BEAC0` steps the log, with the frame base `01DFE0B4` as the unit:

1. With nothing shown, it shows the first queued line and fades the log in by 16 a tick up to `80`<sub>h</sub> (`+40B4`<sub>h</sub>).
2. A line slides in by `32 / [01DFE0B4]` a tick over `100`<sub>h</sub> (`+40B8`<sub>h</sub>); when it is in, `002BF010` retires the line
   it replaced.
3. Once the log is fully faded in and no time stop restricts anything (`00226BA0`), the timer `+40BA`<sub>h</sub> counts up to
   150 x `[01DFE0B4]`. A queued line replaces the shown one when the timer reaches the shown line's hold time.
4. With nothing queued, the log fades out once the timer is full, and `002BEE00` retires every shown line when the
   fade reaches 0.

Message 15 stops the steps (bit 0 of `+40B6`<sub>h</sub>), and the pane set-up `002BEF70` installs the layout record and the
descriptor `002735E0(1)` for the log and its pane `002C0BE0`.

### The HUD switch

`00251F40(n)` shows the HUD for `n` above 0 and hides it otherwise, and does nothing while bits 6 and 7 of `01E0C320`
are both set (`00251F51`). Among the parts it switches are the minimap (`003C5E00`, `003C58B0`), the map overlay page
(`002B61B0`, `002B6140`; [Map screens](map-screens.md)) and the message windows (`0035D1B0`, `0035D0E0`;
[Message windows](message-windows.md)).

On show it also sets bit 0 of the word `+1D7A`<sub>h</sub> of the part at `+10F80`<sub>h</sub>
through `00290280(0, v)`: `0035D560` gives v = 1 when bit 21 of the options word is set (`002DDDC0`) and bit 10 of
the script hold mask is clear (`002E0FA0`), and `0035D550` gives 0 otherwise.

Scripts reach it through a word of hide bits, one per verb family:

1. `maskopen`, `maskclose`, `sethpmenu` and their fast and `mesv` forms set or clear their bit of `0215F1AC` with
   `002E1C40`; the fast forms also set the same bit of `0215F1B4` with `002E1C70`
   ([verb table](../Scripts-And-Script-Commands/verb-table.md)).
2. Each tick `002E0940` compares the word with the last one seen (`0215F1B0`). On a change it calls
   `00254440(word != 0, b)`, with b = 1 when any bit of `0215F1B4` is set, and clears `0215F1B4`.
3. `00254440` sets bit 6 of `01E0C320` for a b of 0 or more, keeps the two values at `02092744` and `020927EC`, and
   runs `00255330`, which hides the HUD for 1 and
   otherwise runs the switch with the saved value `[020927E8]`.

`00254480(a, b)`, run by the menu handler `00280140` (`002801D5`), stores the same two words directly: a at
`02092744` and b without bit 7 at `020927EC`, clearing `01E0C320` when b has bit 7.

### Entry points

| Function | Does |
|---|---|
| `00254E70` | runs the HUD switch `00251F40` with the saved value `[020927E8]` |
| `002509A0` | `0035C880(Ch, 1)`, which clears bits 2 and 3 of the battle mode register `022C83EC` and sets bit 0 (`002509B6`), then `0028E5F0`; run by `002678C0` and `0026E0D0` while `02099DA7` is 0, which then set it to 1 |
| `0028E5F0` | sets or clears the battle mode register's bit 1 from the Escape Mode arming (`003669D0`), stops the arming sound (`00366990`) and closes the widget at `[0209C300]` (`002970C0`) |
| `0028E110(text, kind, colour, arg)` | posts a help message: colour `80808080`<sub>h</sub> when none is given, two times from `002BDB20` (kinds 1-5 from the bytes at `0209E610`, else 30 x `01DFE0B4`; and 150 x `01DFE0B4`), through `002BDB00`; called by `0035B990` |
| `0028E580` | run by `00250960`: builds the status display orders once (`0035D5C0`, which runs `00273BA0` and sets bit 9 of `022C83E8`), arms Escape Mode at once when the battle mode register (`0035C6F0`) has bit 1 and bit 10 of the script hold mask (`002E0FA0`) is clear (`00366960`), runs `00366950`, and resets the four member cells: `00296540(cell, i)` clears `20`<sub>h</sub> bytes and sets byte 0 to i, byte 1 and `+13`<sub>h</sub> to `FF`<sub>h</sub> and the word `+04`<sub>h</sub> to `FFFF`<sub>h</sub> |
| `0028E900` | resets the help block (`002BE050`), which also closes the rings (`00290990`) |
| `0028FEA0(text, arg)` | closes the help window (`002BE020`) and opens a new one (`002BE1A0`); called by `0027B880` |
| `00290C60`, `00290C80` | write the open help window's word `+298`<sub>h</sub>, or `+294`<sub>h</sub> with its `+280`<sub>h</sub> bit 5, and the block's pending `+1040`<sub>h</sub> or `+103C`<sub>h</sub> when no window is open; called by `0027B880` |
| `002E1BB0(v)` | the verb `setgaugehidestatus` (`3D4`<sub>h</sub>): `004087E0` sets bit 20 of `+40`<sub>h</sub> of the gauge window `[02B62D80] + C0h` for v = 2 and clears it for 0 and 1, unless bit 1 of the gauge's `+C8`<sub>h</sub> is set; it is the bit `setmeswinhidestatus` sets on a message window |
| `00473B30(actor)` | `00290840` of the actor's handle (`003589B0`): with the manager present and `+10F68`<sub>h</sub> bit 5 clear, copies bit 8 of `+842`<sub>h</sub> of the line that starts at the handle into bit 5, and returns bit 5 (1 without a manager); the poll `00352350` of `tutorial_sync_targetinfolinearrive` (`3A3`<sub>h</sub>, `3A4`<sub>h</sub>) is true while it returns 0 |
| `00290190` | forwards to the return stub `0016D6A0` and does nothing; the HUD switch calls it with 0 (`00251F8A`) |

The Escape Mode register and arming are on [Escape](../Controls-And-Input/escape.md).

## Modding notes

- Every target line, ring and mark shares one `8030`<sub>h</sub>-byte pool; when it is full a ring request waits a frame and a
  line is not made.
- Target Lines hides only the lines and the `+10F20`<sub>h</sub> and `+10F40`<sub>h</sub> marks; the target ring, the selection marker
  and the `+10F30`<sub>h</sub> marks stay.
- A ring's colour is a palette index from the four bytes at `00916010`.

## Related

- [Battle menu](battle-menu.md) - the menu, help line and gauges the HUD holds.
- [Party list](party-list.md) - the member rows the HUD holds.
- [Subsystem update flags](../Engine-Core/subsystem-update-flags.md) - the pump that steps each part.
- [Menu sprites](menu-sprites.md) - the `targetline_p` picture.
- [Widgets](widgets.md) - the widget model the parts use.
