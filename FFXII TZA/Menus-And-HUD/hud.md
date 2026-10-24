---
title: "HUD: the interface manager and its pool, the target lines, the target ring and the selection marker, and the calls other systems make into it"
kind: "system"
category: "Menus and HUD"
addresses: "0x0028F8B0, 0x00291750, 0x0028F2F0, 0x00273A30, 0x00273B40, 0x00291320, 0x002917E0, 0x0028EAB0, 0x00290370, 0x0028CA40, 0x00271AB0"
---

## What the player sees

- In battle a line joins each character to the target it is acting on; the Target Lines option in Config turns these
  lines off.
- The unit the menu or the cursor points at stands on a spinning ring whose colour depends on what it is.
- A second, rotating marker sits under a unit chosen outside the party list.
- The party's HP and MP list, the battle menu, the help line and the gauges all hang off the same HUD object.

## How it works

### The manager object

The HUD is one `0x10FD0`-byte object whose pointer is at `0x0209BE80`:

1. `0x0028F8B0` first tears down any old one with `0x0028F2F0`, then allocates the object through `0x00271420(0x10FD0)`
   when the pointer is empty and initialises it with `0x00291750` (`0x0028F8CF`, `0x0028F8DE`).
2. `0x00291750` clears all `0x10FD0` bytes, allocates the `0x8030`-byte pool into `+0x10FC0` and prepares it
   (`0x00272470`), builds the part at `+0x5380` (`0x0028A080`), the selection marker `+0x7EA0` (`0x0028CA30`), the help
   block `+0x8FA0` (`0x002BE450`, `0x002BE0A0`) and the world-object part `+0x57E0` (`0x003FA760`), and sets
   `+0x10F90` to -1 and byte `+0x10FA2` to 1.
3. `0x0028F8B0` then clears the two rolling-counter tables (`0x00296260`, `0x00296240`), resets the counter list `+0x80`
   (`0x004FE3C0`), writes 1 to `+0xAA44`, sets flag bit 5 and closes the widget kept at `+0x10F88` (`0x0028F8E3`-`0x0028F952`).

`0x0028F8B0` runs from `0x0035C560` (`0x0035C57F`). `0x0028F2F0` releases every list in the pool, the two `+0x10F74` and
`+0x10F78` widgets through `0x00274840` (`0x002446E0`, `0x002473B0`, `0x002482E0`: focus, message 18 and release), the
level-up blink part (`0x00296670`), the pool and the object itself (`0x0028F2F0`-`0x0028F564`).

### Its parts

The interface pump `0x0028E290` updates the parts in a fixed order ([Subsystem update flags](../Engine-Core/subsystem-update-flags.md)).
What each offset holds:

| Offset | Part |
|---|---|
| `+0x00000` | four `0x20`-byte member cells of the party list, `0x0028F830(i)` = object + `i` x `0x20` ([Party list](party-list.md)) |
| `+0x00080` | the rolling-counter list the party list registers in; `0x0028F590` returns its address, or 0 with no HUD |
| `+0x05380` | the part EXP, LP and combo numbers go to ([Combos](../Battle-Actions/combos.md)) |
| `+0x057E0` | the world-object manager ([Loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)) |
| `+0x07EA0` | the selection marker, below |
| `+0x07FB0` | the level-up blink `0x00296860`; each blink widget `0x00299D10` follows its unit's screen position (`0x00299FC0`, `0x002E9A90`), fades in or out by `0x01DFE0BC` / 6 a frame and closes itself when its count `+0xC0` runs out |
| `+0x08FA0` | the help block ([Battle menu](battle-menu.md)) |
| `+0xAA60`, `+0xAB30` | the battle menu's cursor block and the battle menu |
| `+0x10EF0`, `+0x10F00` | the current target ring and the ring list |
| `+0x10F10` | the target lines |
| `+0x10F20`, `+0x10F30`, `+0x10F40` | three lists of line marks, below |
| `+0x10F50` | the `targetline_p` picture, loaded on first use by `0x0024A5A0` |
| `+0x10F78` | the party list widget ([Party list](party-list.md)) |
| `+0x10FC0` | the pool |

The `+0x5380` part's draw `0x00289A10` queues each number through `0x0028A790(entry, list, buffer, alpha)`, unless
the entry's `+0x14` is set: a sprite at the entry's position with w = -1, the picture of `0x0035D3D0` at its cell,
and a size and alpha from the 5-key track `0x00915F68` at the entry's time `+0x10`; the alpha is scaled by
`0x00272DE0()` x `alpha` while `+0x0C` is set and is 0 otherwise.

### The flag word

Bits of `+0x10F68` that change what the HUD does:

| Bit | Set by | Effect |
|---:|---|---|
| `0` | `0x00290350(0)`, the handler `0x0050D1A0` of the debug verb `debug_settargetlinedispstatus` (`0x207F`) | hides the lines and the `+0x10F20` and `+0x10F40` marks (`0x0028ECA5`) |
| `1` | the pump, from `0x0030C300` | group 7 of the pump |
| `3` | `0x00290370` | a target ring is waiting to be built (`0x0028E2EE`) |
| `4`, `10` | `0x0028E940(id)`, with the id at `+0x10F60` | the battle menu is built on the next pump (`0x00290CF0`) |
| `8` | `0x0028FAF0`; cleared by `0x0028FA70` | group 12 runs (`0x003F8EC0(+0xA0)`) |
| `11` | `0x00290960(1)`, the last step of the field set-up `0x003C5F00` (`0x003C5FA5`), run by `0x00253A30`; cleared by `0x002908C0` from the matching teardown `0x003C5E50` (`0x003C5EF2`) | the `+0x10F30` marks are built only while it is set (`0x00291027`) |
| `13` | `0x002906D0`; cleared by `0x00290610` | `0x00290CF0` and `0x0028F970` do nothing |

### The pool

The pool is a first-fit allocator over the `0x8030` bytes at `+0x10FC0`, and every target object below comes from it.
`0x00272470(pool, size)` writes the `0x30`-byte header, PoolHeader, at the start of the pool:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `PoolBlock*` | head | first block |
| `+0x10` | `PoolBlock*` | cursor | the last block allocated |
| `+0x18` | `u8*` | end | pool address + size, kept to 32 bits |
| `+0x20` | `u8*` | start | pool address + `0x30`, rounded up to 16 |

Each allocation is a `0x20`-byte block header, PoolBlock, followed by the data:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | data | the header's address + `0x20`, the address returned |
| `+0x08` | `u32` | size | the data size, a multiple of 16 |
| `+0x10` | `PoolBlock*` | next | the next block in address order |
| `+0x18` | `PoolBlock*` | prev | the previous block |

### Allocating and freeing

`0x00273A30(mode, pool, size)` rounds the size up to 16 and returns 0 for size 0:

1. In an empty pool the block goes at `start` when it fits before `end`.
2. With mode 0 it tries the gaps after each block from the cursor forwards (`0x00276000`), then from the cursor's
   previous block backwards (`0x002760A0`), then the gap before the head (`0x00276120`).
3. With another mode it tries the gap before the head first, then forwards from the head.
4. A found block is linked in and becomes the cursor; when none fits it returns 0.

The gap tests compare the low 32 bits of the addresses (`0x00276000`, `0x00276120`). Every caller passes mode 0
(`0x002910AD`, `0x00291234`, `0x002913B9`, `0x00291624`, `0x00291997`).

`0x00273B40(pool, data)` unlinks a block: the head moves to the next block when the freed one had no previous, and a
freed cursor moves to its next block, or to its previous one at the end.

### Target lines

`0x00290320(from, to, kind, flag)` asks for a line from one unit to another through `0x00291320`:

1. It refuses kind 0, a unit that `0x00273780` does not resolve, and a line from a unit to itself (`0x0029134E`, `0x00291359`).
2. A line with the same ends and kind is returned as it is (`0x00291366`-`0x00291392`).
3. Otherwise it takes `0x890` bytes from the pool: state `+0x850` = 1, the ends at `+0x810` and `+0x814`, the kind at
   `+0x840`, the picture `+0x10F50` with its two texture rectangles (`0x00271140`, `0x002711E0`), and `0x003F5370` sets the
   rest; `flag` sets `+0x842` bit 0 and a hold of 20 x `0x01DFE0B8` at `+0x844` (`0x002913B9`-`0x0029152D`).
4. The line is appended to the list at `+0x10F10` (`+0x868` next, `+0x860` previous).

Two callers ask for lines:

- `0x00328530(unit, target)`, for each target of a unit (`0x00306010`), when `0x003126E0` passes the target and
  `0x0031AA30` gives a kind (`0x00328555`-`0x003285A0`);
- the battle menu's list `0x0027DE30(unit, row)`, for the target `0x00272E10` gives the row, with the kind from
  `0x00321060` (`0x0027DE99`); a row with no target closes the unit's lines (`0x00290B90`, `0x0027DE6F`).

### Line states

| State | Meaning |
|---:|---|
| `1`, `2` | shown; `0x0028F9E0` answers 1 for these two |
| `3` | closing; `0x00290B70` turns 2 into 3, and `0x00290B90(unit)` does so for every line from the unit |
| `5` | dead; `0x00290BE0` gives every line state 5 and sets its `+0x83C` to 0 |

Group 6 of the pump frees the dead lines (`0x00291B90`, through `0x00273B40`) and steps the rest (`0x003F6100`, which runs
`0x003F5CB0` per line).

The functions that keep and draw the lines:

| Function | Does |
|---|---|
| `0x003F5070(list)` | run by `0x00290C00`: gives state 5 to every line whose either end no longer resolves (`0x003588B0`), clearing `+0x842` bit 1 and `+0x83C` |
| `0x00270F50(out, points, n)` | the curve through a line's points, for the line set-up `0x003F6370`, which passes three points (the two ends and one raised between them) and stores the count, 33, at `+0x7E0`. It runs `0x00270F60` with s = 16, which clears the work block `0x0209A770` and keeps s at `0x0209A76C`; `0x00275CA0` stores the points relative to the first and adds a mirrored point (2a - b) beyond each end; `0x00275570` samples a uniform cubic B-spline (weights / 6), s points a segment, ends pinned, and returns (n - 1) x s + 1 |
| `0x003F62D0(line)` | run by the line step `0x003F5CB0`: rebuilds the packet header for the `+0x7E0` points (`0x003F65C0`) and the points' brightness and alpha (`0x003F6A10`), from the fractions `+0x824` and `+0x828` and the hold `+0x846` against 15 x `0x01DFE0B4` |
| `0x003F5100(list, arg)` | draws the lines with `+0x842` bit 1, sorted by the distance from the camera `0x02AED5F0` to their midpoint (`+0x888`; tree links `+0x870`, `+0x878`, `+0x880`), walking the tree with `0x003F6960` |
| `0x003F5430(line)` | draws one line: a ribbon of quads through its points, 0.15 to each side (`0x003F6130`, `0x003F6200`), with the `targetline_p` cell its kind `+0x840` gives (`0x002713B0`); while `+0x824` is below 1 it adds the six-vertex end piece from `0x01EFF3E0` (`0x003F6690`, `0x003F6850`) |
| `0x003F5390`, `0x003F67C0` | write the GS state records of the line pass (the template at `0x02064AB0`, then TEST_1 `0x53001` and ALPHA_1) through `0x002712E0` |

`0x002713B0(kind)` turns a line or mark kind into its palette cell: 1 gives 1, 2 gives 5, 4 gives 3 and any
other 0.

### What is drawn

The HUD draw `0x0028EAB0`, run from the frame's UI step `0x00252A70` with the word `0x01E0C2AC`, draws the target rings
every time (`0x0028C590`, `0x0028EBA5`). The lines and the `+0x10F20` and `+0x10F40` marks are drawn only when all of
these hold (`0x0028EC7A`-`0x0028ED3B`):

- the options record exists (`0x002DE040`) and Target Lines is on (`0x002DDE00`, dword 1 bit 22,
  [Game settings](../Saving-Loading-And-Settings/game-settings.md));
- the word has bit 0;
- flag bit 0 is clear.

The selection marker is drawn after them (`0x0028C970`, `0x0028EDC9`).

### The draw pass

`0x0028EAB0` runs in this order:

1. `0x003F1220` points a packet record at a 32 KB stack buffer, and `0x003F12D0` empties two depth lists that
   collect sprites placed in the world; the second gets bit 0 of its `+0x18`.
2. It draws the rings (`0x0028C590`), the part `0x003F8C70(+0xA0)` unless `0x00236760` answers non-zero, the
   world-object part (`0x003FA570`, `0x003FA600`) when `+0x7C70` is set, and the `+0x10F30` marks (`0x003F7200`)
   when the word has bit 3.
3. With the conditions above it draws the lines (`0x003F5100`), the `+0x10F20` marks (`0x003F2CF0`) and the
   `+0x10F40` marks (`0x003F3260`).
4. After the "Gaussian Filter" and "display UI 2" markers it draws the part at `+0x10F80` (`0x002C62B0`, the
   overhead gauges on [Battle menu](battle-menu.md)) when the word has bit 2, and the selection marker.
5. Last, `0x003F0170` draws both depth lists and `0x003F1530` the screen-space list.

| Function | Does |
|---|---|
| `0x003F0170(list)` | projects each sprite (`0x002720F0`, the view `0x02AEDDB0`) to its depth `+0xC8`, keeps those in front with screen x and y inside (0, 4096), sorts them by depth (`0x003F19D0`; links `+0xB0`, `+0xB8`, `+0xC0`) and draws them in order through `0x003F1A60`; the next sprite is at `+0xD0`. The first list uses the depth test (TEST_1 `0x53001`), the second does not (`0x1001`) |
| `0x003F1A60(sprite, batch)` | draws one sprite at alpha `0x80`; with `+0xEA` bit 0 the alpha drops when the camera looks at it from behind the focus unit (`0x003590D0`, a dot product below -0.9, eased over distances 1 to 20). It starts a new batch after 24 sprites or a picture change, then runs `0x003F0610` |
| `0x003F0610(batch, sprite)` | computes the four corners and the texture rectangle; the kind `+0xF0` picks the picture: -1 `chain_item` (1024 x 1024), -2 `targetline_p`, -3 `chainflash` (1024 x 512), any other the picture at `+0xE0` |
| `0x003F1530(list)` | the screen-space list: projects each entry (from the list's `+0x40`, next at `+0xF8`) unless `+0xEC` bit 0 is set, clips it (`0x00249EE0`), sorts by depth `+0x120` (`0x003F1940`; links `+0x108`, `+0x110`, `+0x118`) and draws each with `0x002B0280`; `0x003BBB60` also calls it |
| `0x003FAB60(..., list, picture, a, b, c, d, ..., type)` | makes one such sprite (`0x003F0040(list)`; none gives 0): `a` at `+0x00`, `c` at `+0x10` and `d` at `+0x40`. For a `type` below 4 the kind `+0xF0` is -1 and `+0x30` takes 16-byte entry `type` of `0x00D11EE0`; for 4 and 5 the kind is -3 with entry `type - 4` of `0x00D11F20`; otherwise the kind is 0 with `b` at `+0x30`. It writes the picture's TEX0 `+0x30` with a palette offset at `+0x20` and register 6 at `+0x28`, sets `+0xEA` bit 0, keeps the picture at `+0xE0` and links the sprite (`0x003F1290`). `0x003FB3E0` (`0x003FB648`), from `0x003FA570`, calls it |
| `0x003F12E0(sprite, picture, code, frame)` | binds a sprite to a picture cell found through the picture header's tables (`+0x40`, `+0x42`, `+0x44`): the picture at `+0xE0`, the texture rectangle (`0x00271140`) at `+0x30`-`+0x3C`. `0x003F1430` adds a frame offset; the selection marker's `0x0028D260` and `0x0028D460` use it |

`0x003F1530` (`0x003F15B4`) and the widget draw `0x00247AE0` (`0x00247B84`, `0x00247C32`) take their projection from
`0x008626C0(m, f, sx, sy, ox, oy, z0, z1, n, far)`. It multiplies (`0x00217150`) a perspective matrix of focal length `f`
(`m00 = m11 = f`, `m23 = 1`, `m33 = 0`) by a screen matrix with the scales `sx`, `sy`, the offsets `ox`, `oy` and the
depth terms below, then transposes the product:

```python
k = (z1 - z0) / (far - n)
m22 = n x far x k
m23 = (z0 x far - z1 x n) / (far - n)
```

### The target ring

`0x00290370(unit, other, style)` asks for the ring (`0x00290370`-`0x002903C8`):

- with `other` set it moves the selection marker to the unit instead (`0x0028CA40`);
- otherwise it stores the unit at `+0x10F6C`, 0 at `+0x10F70` and the style at `+0x10F72`, and sets flag bit 3.

Its caller `0x002BF0E0` (thunk `0x002BE080`) picks the style from what the unit is:

| Unit | Style | Colour index (`0x00916010`) |
|---|---:|---:|
| kind 2: a unit that `0x00273710` passes, not KO, Stone or status bit 31 | `3` | `0` |
| one of the four party members (`0x00273880`) | `1` | `0` |
| actor class 1, 2 or 7 (`0x00263C20`) | `2` | `1` |
| actor class 3 | `0` | `4` |
| anything else | `1` | `0` |

Kind 1 closes the rings; kind 6 sends the unit to the selection marker (`0x002BF15F`-`0x002BF167`); any other kind first
needs `0x00273710` to pass and closes the rings otherwise (`0x002BF19D`-`0x002BF1A6`).

### Building and closing rings

Group 3 of the pump calls `0x002917E0(manager, unit, 0, style)` while bit 3 is set:

1. It clears bit 3. A current ring below state 3 is kept for the same unit, or turned to the new unit with state 1,
   the new colour and a faster spin, `+0xD44` + 0.314 x `0x01DFE0BC`, capped at 0.419 x `0x01DFE0BC` (`0x0029188E`-`0x002918DD`).
2. Otherwise the old rings fade when there is at most one (`0x00291954`-`0x00291975`); with more, bit 3 is set again for
   the next frame.
3. It takes `0xD80` bytes from the pool, or sets bit 3 again when the pool is full (`0x00291B5F`).
4. It sets state 1 and the unit, converts the picture's sprite into texture coordinates (`0x00291A8F`), writes the
   draw packets with the colour index (`0x0028C620`, `0x00291ADB`) and appends the ring (`+0xD70` next, `+0xD68` previous).

Each pump `0x0028C4C0` steps every ring (`0x0028BB50`) and `0x0028D1C0` frees the rings in state 5 (`0x0028FA50`).
`0x0028C4F0(list)` closes rings: those in states 0, 1 and 5 become 5, those in state 4 are left, and the others start
the fade, state 3. `0x0028C560` puts every ring in state 5 and `0x0028C850` counts them.

| Closer | Also |
|---|---|
| `0x00290990` | fades every ring, clears the current one and fades the selection marker (`0x0028C940`) |
| `0x002909F0` | the same, then kills and frees every ring (`0x0028C560`, `0x0028D1C0`) |
| `0x00290B10` | fades every ring and marks a fading current ring with `+0xD4C` bit 3 |

A ring is two halves of six segments. `0x0028C590` draws each ring with `+0xD4C` bit 0:

| Function | Does |
|---|---|
| `0x0028D030(ring)` | for a ring with `+0xD50` = 1: copies the six 13-record segments of each half (`+0x000`, `+0x5D0`) through the VIF writer, after `0x003F3010` puts the view `0x02AEDDB0` and the camera `0x02AED5F0` into each half's matrix block (`+0x4E0`, `+0xAB0`) |
| `0x0028D980(ring)` | for other rings: the same with 10-record segments, through the sprite batcher too, binding `targetline_p` at the cell `+0xD7C` + 2 x `+0xD78`; `0x0028DC00` draws each segment |
| `0x003F26F0(segments, out, n, ...)`, `0x003F2A70(segments, out, n, ...)` | build `n` segments round the circle, 360 / `n` degrees each, as 13-record (`0xD0`) or 10-record (`0xA0`) packets, and copy them out (`0x00271290`); `0x0028C620` uses both |
| `0x003F5260(block)` | the same matrix copy for `0x003FBA80`'s block (`0x003FBDC2`): the 64-byte view `0x02AEDDB0` to `+0x10` (`0x00202C70`) and the 16-byte camera `0x02AED5F0` to `+0x50` (`0x00202C90`); `0x003F3010` writes them to `+0x50` and `+0x90` |
| `0x003F5BE0(block)` | writes the VU1 chunk around `0x003FBA80`'s block (`0x003FBD52`) for the record count `n` in `+0x5C`: three `0x10000000` and an UNPACK header for `n + 5` records, a GIF tag with A+D and two PRIM records (`0x5B`, `0x5C`), a GIF tag with end-of-packet, NLOOP `4n + 2` and the registers ST, RGBAQ, XYZF2 (`0x412`), and after the `n` records FLUSHA and MSCNT (`0x17000000`); it returns the chunk's length |
| `0x0028CF80(ring, v)` | the pulse `0x0028BB50` runs: for `+0xD50` = 1 it writes sin(2 pi / (2 x `+0xD48`)) x v into `+0xA0` of each `0xD0` segment (`0x003F3050`), otherwise v into `+0x80` of each `0xA0` segment (`0x003F25D0`) |

### The selection marker

The `0x80`-byte marker at `+0x7EA0` keeps two slots. `0x0028CA40(marker, unit)` starts it on a unit's position
(`0x002E7F70`), or on a new unit fades the old slot out and starts the other. Group 16 of the
pump (`0x0028C870`) turns it by 10 x `0x01DFE0BC` degrees a frame and fades it in or out by 32 / `0x01DFE0B4` a frame.

`0x0028C970` draws it with `0x0028D260` and, per slot, `0x0028D8A0`, whose `0x0028D460` draws three sprites 2.094 radians
apart. Both read a colour track at `0x00915FB0` (four keys, `0x0028CB90`) and scale it by `0x0028CD10(angle)`:

```python
0x0028CD10(a) = 0                                            a >= pi = 128 x sin((a / 0.785398) x pi/2)              a <= pi/4 = 128 x sin(pi/2 - ((a - pi/4) / 2.356194) x pi/2)   otherwise
```

### Line marks

| List offset | Size | Built by | From |
|---|---|---|---|
| `+0x10F20` | 2512 | `0x002915C0`, one per unit handle `+0x980` or position `+0x960` | `0x0028E9F0`, called by the line step `0x003F5CB0` (`0x003F5F7D`) |
| `+0x10F40` | 128 | `0x002911D0`, found by unit through `0x003F3580` | `0x0028EA20`, called by the battle menu's `0x0027DC10` |
| `+0x10F30` | 832 | `0x00291010`, only while flag bit 11 is set | `0x00290300`, called by `0x0035DAF0` |

`0x0027DC10(actor, unit, action, keep)` asks for a `+0x10F40` mark when `0x0031AB80` reports kind 1, `keep` is 0 and
`0x00273710` passes the unit; it first drops the unit's old mark (`0x00290CD0`, `0x003F35A0`).

The `+0x10F20` and `+0x10F40` marks:

| Function | Does |
|---|---|
| `0x003F2580(list, mark)` | appends a `+0x10F20` mark (next `+0x9B0`, previous `+0x9B8`); `0x002915C0` uses it and `0x003F2600` |
| `0x003F2600(mark, rect)` | sets a new `+0x10F20` mark: six 10-record segments (`0x003F2A70`), the scale `+0x998` = 1.0, two sprite blocks (`0x003F2F20`) and two label heights, y / 2 - y / 10 and y / 2 + h + y / 10, from the rectangle |
| `0x003F2CF0(list)` | draws each `+0x10F20` mark with `+0x991` bit 0: twelve segments with the picture `+0x988` at the cell its kind `+0x990` gives, the alpha scaled by `+0x998` |
| `0x003F3080(mark, on)` | sets or clears `+0x991` bit 3; `0x002907F0` calls it |
| `0x003F1E90(mark)` | the step of one `+0x10F20` mark, which `0x003F24A0(list)` runs down the `+0x9B0` chain. With `+0x991` bit `0x2` it asks `0x002713E0(+0x960, +0x980)`: on 0 it clears `+0x980` and moves state `+0x9C0` 0 to 5 and 1 or 2 to 3, otherwise `+0x964` grows by `(1 - +0x9AC) x 0.5 x 0x00271380(+0x980)` (doubled in state 2). With bit `0x8`, `+0x998` falls by a third per step and at 0 the state becomes 5. State 1 sets bit `0x1` and becomes 2; states 2 and 3 raise `+0x994` by `max(0.002, (1 - +0x994) / 6)` toward 1.0, set `+0x93C` to 100 x and `+0x84C` to 255 x `+0x994`, and raise `+0x9AC` by the same step; with bit `0x4` the pairs `+0x834`/`+0x83C` and `+0x924`/`+0x92C` ease toward `+0x974`/`+0x97C` by a twelfth, otherwise `+0x9AC x +0x9A8` goes to `+0x80` of the twelve `0xA0`-byte segments; when `+0x994` and `+0x9AC` both reach 1.0 the state becomes 4. State 4 eases the same pairs, lowers `+0x994` by `max(0.002, (1 - +0x994) / 5)` to 0, `+0x84C` by 25.4 and `+0x93C` by 25.4 / 1.5 (never above `+0x84C`), and raises `+0x9AC` to at most 2.0 (`0x003F3D80` below once it is there); at `+0x994` = 0 it clears bit `0x1` and sets state 5. It ends by rebuilding `+0x790` from `+0x960` and `+0x880` (`0x00203170`, `0x002030E0`, `0x00202C70`) |
| `0x003F3D80(block, n, s, t)` | builds the vector (t, s, t) (`0x00203170`) and transforms `+0x60` and `+0x70` of each of `n` `0xA0`-byte segments from `block + 0x70` with it (`0x00202B70`); the state-4 step calls it with (mark, 6, 1.0, 1.25) and (mark + 0x3C0, 6, 1.0, 1.25) (`0x003F21CC`, `0x003F21E8`) |
| `0x003F34D0(list, mark)` | appends a `+0x10F40` mark (next `+0x70`, previous `+0x78`); `0x002911D0` uses it and `0x003F3510` |
| `0x003F3510(mark, picture, ...)` | sets a new `+0x10F40` mark: the header `0x00275550(mark, 0x80)`, `+0x60` from `0x00272F30`, then `0x003F3660` binds the picture cell, sets the shown bit 0 of `+0x50`, the colour (255, 255, 255, 127) and the scale 0.25 |
| `0x003F30D0(mark)` | the step `0x003F31B0` runs per `+0x10F40` mark: it clears the shown bit when the unit no longer passes `0x002713E0`, fades `+0x4C` in or out by 0.5 x `0x01DFE0BC`, advances the pulse `+0x68` (reset at 0.99) and sets bit 1 once faded out |
| `0x003F3260(list)` | draws each `+0x10F40` mark as two sprites 90 degrees apart (`0x003F3710`) at the angle `0x003F35C0` gives, first a pulsing copy and then the mark |
| `0x003F30A0(list, fn)` | walks a list linked at `+0x70` and calls `fn` for each entry; the teardown `0x0028F2F0` uses it |

The `+0x10F30` marks join two units, a at `+0x2D0` and b at `+0x2D4`:

| Function | Does |
|---|---|
| `0x003F73F0(mark, a, b, rect, picture)` | sets a new mark: the header `0x00275550(mark, 0x340)`, `+0x2EC` bits 1 and 2 with the units' positions (`0x002713E0` into `+0x280` and `+0x290`), the sprite blocks (`0x003F7CC0`) and state 1 at `+0x2F0` |
| `0x003F7380(list, mark)`, `0x003F73D0(list, a)` | append a mark (next `+0x300`, previous `+0x308`), and find the mark whose unit a is `a` |
| `0x003F7490(list)` | run by `0x00290C00`: state 4 for every mark whose unit a or b no longer resolves (`0x003588B0`) |
| `0x003F6FD0(mark)` | closes a mark for `0x002908C0` and `0x00291010`: state 1 becomes 4, other states except 0 and 4 become 3 |
| `0x003F77F0(mark)` | when both units are set, a has a party record (`0x002732E0`) whose `+0x5C` is not -1 and `0x002739D0` passes, binds the `targetline_p` cell 4 when `0x0030BEF0` answers above 0 and 1 otherwise (`0x00271650`); otherwise it closes the mark like `0x003F6FD0` |
| `0x003F7BC0(mark)` | eases `+0x2E0` by 0.35 a step toward the gap between the two units, less both radii (`0x002645D0`, plus 1 for b), clamped to 10 and divided by 10: `g = length(+0x290 - +0x280) - (ra + rb + 1)`, `+0x2E0 += (min(max(g, 0), 10) / 10 - +0x2E0) x 0.35` (`0x003F7C52`-`0x003F7C8B`) |
| `0x003F7760(mark)` | turns the orientation `+0x2A0` by 0.35 toward the direction from a to b (`0x00270A10`, `0x00270CF0`) |
| `0x003F7610(mark)`, `0x003F74F0(...)` | build the two halves' matrices from the orientation (`0x00270720`), scaled by `+0x2E0` and raised by a's radius x 1.3, or x 1.2 for the second half, at a's position |
| `0x003F7200(list)` | draws the marks with `+0x2EC` bit 0, farthest from the camera first (distance `+0x328`; links `+0x310`, `+0x318`, `+0x320`), each with `0x003F70F0`, which binds `targetline_p` at the cell `+0x330` + 2 x `+0x32C` and draws both halves as the 35 sprites of the table `0x01EFF4E0` (`0x003F7930`) |

`0x003F7BC0`, `0x003F7760`, `0x003F7610` and `0x003F77F0` are run by group 4's step `0x003F6BB0`.

### The overhead display

The part at `+0x10F80`, `0x1D90` bytes, draws marks over units: a status mark for each unit it lists, a box at
`+0x1B80` and two name boxes. `0x002C63D0`, run by `0x0028FF80` and `0x00290060`, clears it, links its 95 `0x40`-byte unit
entries into the free list `+0x1D60` and sets the fade distances `+0x1D7C` = 5.0 and `+0x1D80` = 17.0.

Group 15 of the pump, `0x002C6180`, steps it:

1. It clears every entry's shown bit (`+0x17` bit 0) and sets the closing bit 1 of both name boxes (`+0x19B4`).
2. With `+0x1D7A` bit 9 it runs `0x002C8D60`, which calls `0x002C6F70` for each unit of the list `0x0035D500`
   (`0x0035D510` units), stopping when one returns 0.
3. It steps the box at `+0x1B80` (`0x002C6BE0`) and the name boxes (`0x002C6B50`), and fades the whole part
   `+0x1D78` toward `0x80`, or toward 0 while `+0x1D7A` bit 3 is set, by 32 / `[0x01DFE0B4]` a frame.
4. It keeps `0x0028F5B0()` at `+0x1D88`, frees the entries left unshown (`0x002C8DF0`) and copies `0x02092730` to
   `+0x1D84`.

| Function | Does |
|---|---|
| `0x002C8A20(list, entry)`, `0x002C7620(list, entry)` | append an entry to the list `+0x1D70` (next `+0x18`, previous `+0x20`), and unlink one |
| `0x002C8DF0(part)` | returns every entry whose shown bit is clear to the free list, and clears the `+0x1B80` box's entry `+0x1D30` when it was one of them |
| `0x002C8A60(part, entry)` | gives an entry a name box: the box already showing its unit, else a free one, else the box after the last one used (`+0x1D7A` bit 7 flips). A new box is cleared and filled by `0x002C8BC0`, which writes the menu text `0x46D8` (`0x002C8C07`), a `0F <` baseline shift ([Text codes](text-codes.md)) whose two parameter bytes come from the screen-layout value NAOverHeadTextOffsetY (`0x002C8C22`-`0x002C8C43`), and then the display name from `0x00272CE0` (`0x002C8C02`) when bits 4 and 5 of the entry's byte `+0x17` are both set (`0x002C8BEC`-`0x002C8BF7`), and the name alone otherwise (`0x002C8CB5`); the unit goes to `+0x1B0` with bit 0 set and bit 1 clear in `+0x1B4` |
| `0x002C6B50(part)` | fades each open name box in, or out while its bit 1 is set, by 32 / `[0x01DFE0B4]` a frame up to `0x80`; a box faded out loses bit 0 |
| `0x002C6BE0(part, box)` | the same for the box at `+0x1B80`, also moving its ramps `+0x1BC`, `+0x1BE` and `+0x1D0`; a box faded out drops its entry |
| `0x002C62B0(part, ...)` | the draw: each entry through `0x002C7660`, with bit 10 of the script hold mask (`0x002E0FA0`) and the focus unit, then the `+0x1B80` box (`0x002C7F90`) and each open name box at the part's alpha times the box's (`0x003F14D0`) |
| `0x002C7B10(entry, ...)` | the status mark over a unit: the cell `0x300` sprite of the status `+0x16` (`0x003F12E0`) at the alpha `+0x15`. Statuses 4, 9 and 24 pulse in size along the track `0x00916E90`, status 12 turns along `0x00916ED0`; with `+0x17` bit 2 it adds the status numbers (`0x002C84E0`) |
| `0x002C8920(unit, alpha, list, ...)` | queues the cell `0xE00` sprite of the picture `0x0035D460` returns over a unit; `0x002C7660` asks for it for the unit `0x0035BAD0` names when `0x003135C0` and `0x00273460` answer non-zero |
| `0x002C69A0(pos, sprite, cell, alpha, rgba, picture)` | fills a sprite from a picture cell: the position with w = -1, the texture rectangle, the colour bytes with alpha x `rgba.a` / 128, and half the cell's size to each side; `0x002C7F90`, `0x002C8310` and `0x002C8820` use it |
| `0x002C6450(part)` | answers whether the focus unit's entry is drawn at full alpha (entry `+0x14` x `+0x1D78` at least `0x4000`), or, with no entry, whether the part is at `0x80`. `0x0028FA00` jumps to it with the part `[0x0209BE80] + 0x10F80` when that part exists and bit 3 of its `+0x1D7A` is clear, and answers 0 otherwise (`0x0028FA00`-`0x0028FA25`); `0x00253C70` (`0x00254120`) and `0x002736B0` (`0x002736CC`) call `0x0028FA00` |

### Keyframe tracks

HUD animations read short tracks of keys. `0x00271AB0(out, keys, count, t)` uses 12-byte keys:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | x | interpolated |
| `+0x02` | `i16` | y | interpolated |
| `+0x04` | `u16` | time | the key's time |
| `+0x06` | `u8` | a | interpolated |
| `+0x07` | `u8` | b | interpolated |
| `+0x08` | `u16` | curve | how the segment that ends at this key moves |
| `+0x0A` | `i16` | w | interpolated into a 32-bit result at `out + 8` |

It finds the segment whose times hold `t`, the last one past the end, and blends by `p`, the fraction of the
segment: curve 1 gives `sin(p x pi/2)`, curve 2 `1 - sin((1 - p) x pi/2)`, any other `p`. Past the last key it keeps
blending along the last segment.
`0x0028CB90` does the same over 8-byte keys `{i16 value, u8, u8, i16 curve, u16 time}` and blends through `0x002752E0`.
`0x002C6DC0(out, keys, n, t)` does it for the overhead display (`0x002C7F90`, `0x002C84E0`) over 8-byte keys
`{i8, i8, u8 curve, u8, i16 time, i16}`, blending through `0x002752E0`.

`0x003FB8F0(out, keys, n, t)`, called twice by `0x003FAF10` (`0x003FAFE6`, `0x003FB004`), does it over 12-byte keys
`{i16, i16 time, i16, i16, i32 curve}`: the first pair of keys with start time <= `t` < end time, else the last
pair; the later key's curve picks the same blends as a 0-256 ratio, and `0x002752E0` blends the three `i16`
values into a word and two bytes at `out`.

### Vector helpers

The HUD parts and the screens around them share a few small vector helpers:

| Function | Does |
|---|---|
| `0x00270550(v)` | the length of the x, y, z lanes; the ring step `0x0028BB50`, the overhead gauges (`0x002C6F70`), the world objects (`0x003F8FE0`) and `0x003F7BC0` among its ten callers |
| `0x00270880(out, v, s)`, `0x002708B0(out, v, s)` | scale all four lanes, or x, y and z keeping w |
| `0x00202DE0(out, v)`, `0x00202C50(out, m, p)` | normalise x, y, z through `0x00216660`, giving all four lanes 0 when the squared length is NaN, infinite or at most 1.1754944e-38; and transform a point through `0x00216FC0`, x · row 0 + y · row 1 + z · row 2 + row 3, with w = 0 |
| `0x00270230(out, rect, dx, dy)` | moves both corners of a rectangle by (dx, dy); the marker sprite `0x0028D460` uses it |
| `0x00270720(out, q)` | the rotation matrix of the quaternion (x, y, z, w) |
| `0x00270A10(out, dir)` | the orientation facing a direction: pitch -atan2(y, max(abs x, abs z)) and yaw atan2(x, z), each kept in (-pi, pi], as a quaternion (`0x00270B40`) |
| `0x00270CF0(out, a, b, t)` | spherical interpolation from a (t = 0) to b (t of 1 or more), the short way round |
| `0x00270590(out, p, a, b)` | the point nearest `b` on the line through `p` and `a`: it takes the plane of `p`, `a`, `b` (normal `(a - p) x (b - p)`), a second plane through `p` and `a` at right angles to it, and moves `b` along the second plane's normal onto it (`0x002708E0`, a line and plane intersection); `out` is `b` with w = 1 when that line is parallel to the plane. The world objects call it (`0x003F9078`), and `0x003F9720` (`0x003F9C0F`) |
| `0x00270420(out, points, n)`, `0x00270500(lengths, n, d)` | the n - 1 segment lengths of a chain of points; and the fractional segment index at which their running sum reaches d, or -1.0 past the end. `0x005621A0`, which draws the `w_line01` path, uses both |
| `0x002754E0(out, a, b, t)` | `a + (b - a) x t` on four floats; the ring pulse `0x0028BB50` (`0x0028BE05`, `0x0028BE21`, `0x0028C1A5`, `0x0028C2D2`, `0x0028C31B`, `0x0028C356`), group 4's step `0x003F6BB0` (`0x003F6D4B`, `0x003F6EA4`) and the `w_line01` path `0x005621A0` (`0x005624B9`) use it |

### The active log

The active log, procedure `0x002BE4F0` built by `0x002BDCE0` under the field HUD root, shows one battle-log line at a time.
The root `0x00253780` reaches that builder through `0x0035C630` (`0x002537E6`), which runs `0x002BDCE0` (through `0x0028E220`),
`0x0028FF80`, the chocobo menu task builder `0x003CA280`, the HUD widget builder `0x003C98E0` and then `0x00290450(1)`.

`0x0028E110` posts a line through `0x002BDB00` ([Battle log](../Battle-Actions/battle-log.md)), and `0x002BE8D0` files it
as a `0x198`-byte record: the text, `0x180` bytes copied by `0x00254F30`, its colour at `+0x180`, the hold time at
`+0x184`, an in-use bit at `+0x186` and half its width at `+0x187` (`0x0029CD00`). Records move between three lists
linked through `+0x188` and `+0x190`:

| List | Offset | Holds |
|---|---|---|
| queued | `+0x4098` | posted lines; `0x002BF480` takes the first |
| shown | `+0x40A0` | the line on screen and the one sliding in |
| free | `+0x40A8` | spent records; a new line takes the first, or the oldest queued line's record when the list is empty |

Each tick `0x002BEAC0` steps the log, with the frame base `0x01DFE0B4` as the unit:

1. With nothing shown, it shows the first queued line and fades the log in by 16 a tick up to `0x80` (`+0x40B4`).
2. A line slides in by `32 / [0x01DFE0B4]` a tick over `0x100` (`+0x40B8`); when it is in, `0x002BF010` retires the line
   it replaced.
3. Once the log is fully faded in and no time stop restricts anything (`0x00226BA0`), the timer `+0x40BA` counts up to
   150 x `[0x01DFE0B4]`. A queued line replaces the shown one when the timer reaches the shown line's hold time.
4. With nothing queued, the log fades out once the timer is full, and `0x002BEE00` retires every shown line when the
   fade reaches 0.

Message 15 stops the steps (bit 0 of `+0x40B6`), and the pane set-up `0x002BEF70` installs the layout record and the
descriptor `0x002735E0(1)` for the log and its pane `0x002C0BE0`.

### The HUD switch

`0x00251F40(n)` shows the HUD for `n` above 0 and hides it otherwise, and does nothing while bits 6 and 7 of `0x01E0C320`
are both set (`0x00251F51`). Among the parts it switches are the minimap (`0x003C5E00`, `0x003C58B0`), the map overlay page
(`0x002B61B0`, `0x002B6140`; [Map screens](map-screens.md)) and the message windows (`0x0035D1B0`, `0x0035D0E0`;
[Message windows](message-windows.md)).

The switch (`0x00252011`), `0x00255330` (`0x00255371`) and `0x00254AC0` (`0x00254B05`) also close the widget at `[0x02B47740]`
with `0x003C9900`: when it exists, its `+0x40` bit 16 is set to whether `0x002544B0()` answers 1, then `0x00244DD0` runs.
The switch opens it with `0x003C9F80` (`0x00251FCD`): with the widget present it sets `+0x40` bit 15 to whether
`0x002544B0()` (`[0x020927EC]`) answers 1 and runs `0x00246AC0`; without it, `0x003C99D0` creates it (`0x00244F50(0xD8,
0x003C9A30, 0)`) and does the same.

That widget's procedure `0x003C9A30` stores the widget at `0x02B47740` when it is created (`0x003C9AE3`) and closes its
child `+0xC8` with `0x003C98A0` (`0x003C9BA8`, `0x003C9D37`): the child's `+0x7C` becomes `(v & 0x3FF7FF) | 0x4B000800`,
`0x00244DD0` closes it, and bit 1 of the widget's `+0xC4` is cleared. The same procedure places that child with
`0x003C9840` (`0x003C9B6D`, `0x003C9CB8`): it copies the words `+0x0C` and `+0x0E` of layout entry 2 (1 when `0x003C5FB0()`
answers 0) of the widget (`0x00394690`) to the child's `+0x98` and `+0x9A`.

On show it also sets bit 0 of the word `+0x1D7A` of the part at `+0x10F80`
through `0x00290280(0, v)`: `0x0035D560` gives v = 1 when bit 21 of the options word is set (`0x002DDDC0`) and bit 10 of
the script hold mask is clear (`0x002E0FA0`), and `0x0035D550` gives 0 otherwise.

Scripts reach it through a word of hide bits, one per verb family:

1. `maskopen`, `maskclose`, `sethpmenu` and their fast and `mesv` forms set or clear their bit of `0x0215F1AC` with
   `0x002E1C40`; the fast forms also set the same bit of `0x0215F1B4` with `0x002E1C70`
   ([verb table](../Scripts-And-Script-Commands/verb-table.md)).
2. Each tick `0x002E0940` compares the word with the last one seen (`0x0215F1B0`). On a change it calls
   `0x00254440(word != 0, b)`, with b = 1 when any bit of `0x0215F1B4` is set, and clears `0x0215F1B4`.
3. `0x00254440` sets bit 6 of `0x01E0C320` for a b of 0 or more, keeps the two values at `0x02092744` and `0x020927EC`, and
   runs `0x00255330`, which hides the HUD for 1 and
   otherwise runs the switch with the saved value `[0x020927E8]`.

`0x00254480(a, b)`, run by the menu handler `0x00280140` (`0x002801D5`), stores the same two words directly: a at
`0x02092744` and b without bit 7 at `0x020927EC`, clearing `0x01E0C320` when b has bit 7.

### Entry points

| Function | Does |
|---|---|
| `0x00254E70` | runs the HUD switch `0x00251F40` with the saved value `[0x020927E8]` |
| `0x00290EB0(hud)` | while `+0x10F90` holds a caption index (not -1): when the `0xE8`-byte widget at `+0x10D20` or `+0x10E08` (chosen by `+0x10F68` bit 7) still exists (`0x00273A20`) it only calls `0x00245020`; otherwise it opens it with the procedure `0x003F8250`, places it at `+0x10F94`/`+0x10F96`, sets its text with `0x003F8030`, sets `+0x10F90` back to -1 and flips bit 7 |
| `0x003F8030(widget, n)` | the text `0x002F9860([0x00D11E30 + 16n])` at `+0xC0`; the box is the measured text (`0x0029CD90`) plus 4 |
| `0x003F8790(widget, mode)` | run by `0x003F8250` (`0x003F8362`, `0x003F83F3`): matches the four children at `+0xC0`-`+0xD8` against the four ids at `[+0xE0] + 0x740`. A child whose id `+0xE0` is still listed moves to that id's slot, sliding to y = (3 - slot) x 0x12 (`0x002468A0`) when the slot changed; any other child is closed (`0x00244F00`); a listed id with no child gets one from `0x003F8640(widget, id, slot)`, opened with `0x00244960` for mode 0 or `0x00246AD0` otherwise. Every child then takes the widest `+0xD0`, and it returns the number of listed ids |
| `0x003F8490(widget)` | finds a free slot among the eight `0xE8`-byte child slots from `+0x000`: it steps the index `+0x750`, wrapping from 7 to 0, and returns the first slot for which `0x00273A20` answers 0, or 0 after eight; `0x003F8640` takes its slot this way (`0x003F8688`) |
| `0x003F8140(widget)` | run by `0x003F8250` on each message 2 (`0x003F83B0`): while `+0x100` is below 1.0 it adds 1/6 (to at most 1.0) and moves the four `i16` at `+0xE8`-`+0xEE` from `+0xF8`-`+0xFE` towards `+0xF0`-`+0xF6` by that fraction |
| `0x002509A0` | `0x0035C880(0xC, 1)`, which clears bits 2 and 3 of the battle mode register `0x022C83EC` and sets bit 0 (`0x002509B6`), then `0x0028E5F0`; run by `0x002678C0` and `0x0026E0D0` while `0x02099DA7` is 0, which then set it to 1 |
| `0x0028E5F0` | sets or clears the battle mode register's bit 1 from the Escape Mode arming (`0x003669D0`), stops the arming sound (`0x00366990`) and closes the widget at `[0x0209C300]` (`0x002970C0`) |
| `0x0028E110(text, kind, colour, arg)` | posts a help message: colour `0x80808080` when none is given, two times from `0x002BDB20` (kinds 1-5 from the bytes at `0x0209E610`, else 30 x `0x01DFE0B4`; and 150 x `0x01DFE0B4`), through `0x002BDB00`; called by `0x0035B990` |
| `0x0028E580` | run by `0x00250960`: builds the status display orders once (`0x0035D5C0`, which runs `0x00273BA0` and sets bit 9 of `0x022C83E8`), arms Escape Mode at once when the battle mode register (`0x0035C6F0`) has bit 1 and bit 10 of the script hold mask (`0x002E0FA0`) is clear (`0x00366960`), runs `0x00366950`, and resets the four member cells: `0x00296540(cell, i)` clears `0x20` bytes and sets byte 0 to i, byte 1 and `+0x13` to `0xFF` and the word `+0x04` to `0xFFFF` |
| `0x0028E900` | resets the help block (`0x002BE050`), which also closes the rings (`0x00290990`) |
| `0x0028FEA0(text, arg)` | closes the help window (`0x002BE020`) and opens a new one (`0x002BE1A0`); called by `0x0027B880` |
| `0x00290C60`, `0x00290C80` | write the open help window's word `+0x298`, or `+0x294` with its `+0x280` bit 5, and the block's pending `+0x1040` or `+0x103C` when no window is open; called by `0x0027B880` |
| `0x002E1BB0(v)` | the verb `setgaugehidestatus` (`0x3D4`): `0x004087E0` sets bit 20 of `+0x40` of the gauge window `[0x02B62D80] + 0xC0` for v = 2 and clears it for 0 and 1, unless bit 1 of the gauge's `+0xC8` is set; it is the bit `setmeswinhidestatus` sets on a message window |
| `0x00473B30(actor)` | `0x00290840` of the actor's handle (`0x003589B0`): with the manager present and `+0x10F68` bit 5 clear, copies bit 8 of `+0x842` of the line that starts at the handle into bit 5, and returns bit 5 (1 without a manager); the poll `0x00352350` of `tutorial_sync_targetinfolinearrive` (`0x3A3`, `0x3A4`) is true while it returns 0 |
| `0x00290190` | forwards to the return stub `0x0016D6A0` and does nothing; the HUD switch calls it with 0 (`0x00251F8A`) |

The Escape Mode register and arming are on [Escape](../Controls-And-Input/escape.md).

## Layouts

### The field marker

The field marker is the `0xF8`-byte widget at `0x022C83E0` with procedure `0x0035C160` (State below); every field past the header is set only by its construct message, so it draws nothing.

`FieldMarker` (`0xF8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0035C160` |
| `+0xC0` | `i16` | state | the marker's draw state: the draw message 4 runs only for states 2-5 (`0x0035C1BD`-`0x0035C1CA`); states 2, 4 and 5 set the colour bytes `+0x90`-`+0x92` of the draw record [`+0x38`] to the pulse 96 + 32 x sin(frame x pi / 30) (`0x0035C1D0`-`0x0035C22D`), state 3 holds `+0x90` at `0x80` (`0x0035C364`). The construct message 1 sets it to 0 (`0x0035C3AB`); no other instruction writes it |
| `+0xC2` | `u8[2]` | pad0C2 | read and written by no function; nothing fixes its width |
| `+0xC4` | `u32` | helpOpen | set while the marker holds the help block's rings open: `0x0035C080` closes them with `0x00290990` only when it is non-zero and then clears it (`0x0035C090`, `0x0035C0A5`); `0x0035C100` fades them with `0x00290B10` and clears it (`0x0035C11E`). The construct message 1 sets it to 0 (`0x0035C3B2`); no instruction sets it non-zero |
| `+0xC8` | `char[32]` | label | the label text the marker draws: the draw message passes its address to `0x002B3400` as the text of the draw context (`0x0035C2C4`) and `0x002D8650` draws it (`0x0035C34D`); the construct message 1 stores 0 in its first byte (`0x0035C397`), an empty label. The next field bounds it at 32 bytes |
| `+0xE8` | `i16` | labelWidth | the label's width: the draw message scales it by the depth factor 0.5 + 0.5 x (depth - `0x100000`) / 3145728 (depth clamped to `0x100000`-`0x400000`) and draws the label at x - width / 2 (`0x0035C2DC`-`0x0035C341`) |
| `+0xEA` | `i16` | labelHeight | the label's height: scaled by the same depth factor; the label is drawn at y - height, above the projected point (`0x0035C2F2`-`0x0035C330`) |
| `+0xEC` | `u32` | unit | the handle of the unit the label follows: the draw message skips when `0x002EA230`(handle) answers non-zero (`0x0035C233`), otherwise takes the unit's position (`0x002E9A90`, `0x0035C246`) and projects it through the view `0x02AEDDB0` (`0x00249110`, `0x0035C270`), and draws nothing when the projected depth is `0x1000000` or more (`0x0035C28C`). The construct message 1 sets it to 0 (`0x0035C3A5`) |
| `+0xF0` | `u64` | cleared0F0 | set to 0 by the command message 12 (`0x0035C1B1`); read by no instruction |

### The field-effect icon

The field-effect icon is the `0xD8`-byte widget at `0x02B47740` with procedure `0x003C9A30` that the HUD switch opens; it shows the icon of the first field effect in force.

`FieldEffectIcon` (`0xD8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x003C9A30` |
| `+0xC0` | `u8` | effect | the field effect in force: each tick (message 2) takes the first of bits `0x1`-`0x40` of the field-effect flags `0x022C314C` (`0x0031A8E0`) in the table `0x00D11710` as 0-6, or 7 for none, and stores it here (`0x003C9BD8`-`0x003C9C02`); the construct message sets it and `+0xC1` to 7 with one word store of `0x707` (`0x003C9AF1`). Read by no instruction: the tick uses the value it has just computed |
| `+0xC1` | `u8` | iconEffect | the field effect whose icon is loaded or being loaded: the tick stores the current effect here when it differs from the icon child's `+0xC0` and the child is idle (its `+0xC1` is 0) or in state 3-4 (`0x003C9D28`, `0x003C9D46`); `0x003C9950` requests the picture kind 7, id `0x0E` + this value (`0x003C997B`); once the picture has loaded the tick gives it to the child's `+0xC0` (`0x003C9C33`, `0x003C9C43`) |
| `+0xC2` | `u8[2]` | pad0C2 | read and written by no function; nothing fixes its width |
| `+0xC4` | `u32` | flags | bit 0: the widget is open, set by message 19 (forward run finished, `0x003C9BBF`), cleared by message 15 (closing begins, `0x003C9D75`); bit 1: the icon child is open, set by the tick (`0x003C9CAE`), cleared by `0x003C98A0` when it closes the child (`0x003C98D1`); bit 2: a new icon is wanted, set by the tick (`0x003C9D25`, `0x003C9D43`), cleared once the child is opened with it (`0x003C9CBD`); bit 3: the picture request is in flight, set by `0x003C9950` (`0x003C99AF`), cleared by message 16 (a resource batch has loaded, `0x003C9B2A`). The construct message sets it to 0 (`0x003C9AFF`) |
| `+0xC8` | `void*` | iconChild | the icon widget, `0xC8` bytes with procedure `0x003C95C0`, built by the construct message (`0x00244F50` at `0x003C9B0C`, stored at `0x003C9B11`); placed by `0x003C9840` (`0x003C9846`, `0x003C986E`), closed by `0x003C98A0` (`0x003C98A9`, `0x003C98C5`), opened by the tick (`0x00246AD0`, `0x003C9CA2`) and released by message 18 unless it is open (`0x003C9D8E`-`0x003C9DAA`) |
| `+0xD0` | `void*` | pictureBuffer | the loaded icon picture: `0x003C9950` frees the previous buffer (`0x003697F0`, `0x003C9967`) and keeps the new request's `+0x08` (`0x003C99C0`); `0x003C9E50` copies 2h rows of w bytes from it into the battle_4_c image and frees it (`0x003C9E58`, `0x003C9F52`, `0x003C9F6D`); message 18 frees it (`0x003C9DB1`, `0x003C9DC2`); the construct message sets it to 0 (`0x003C9B05`) |

### The manager part at +0xA0

These bytes sit in the part at `+0xA0` of the manager `[0x0209BE80]` (The manager object above); the offset is from the start of the part.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x52A8` | `u8[8]` | pad52A8 | between the pointer +0x52A0 and the pointer +0x52B0 (manager +0x5348-+0x534F); read and written by no function; nothing fixes its width |

### The manager part at +0x57E0

These bytes sit in the pickup part at `+0x57E0` of the manager; the offsets are from the start of the part.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x24A4` | `u8[12]` | pad24A4 | after the counter words +0x24A0/+0x24A2 and before the screen-label node at +0x24B0 (manager +0x7C84-+0x7C8F); read and written by no function; nothing fixes its width |
| `+0x26A0` | `u8[7]` | pad26A0 | after the two image handles +0x2690/+0x2698 and before the six low-nibble bytes +0x26A7 (manager +0x7E80-+0x7E86); read and written by no function; nothing fixes its width |

### The manager part at +0x8FA0

This field sits in the help-message part at `+0x8FA0` of the manager; the offset is from the start of the part.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xBC` | `u8[4]` | headerBC | the last four bytes of the help-message screen's widget header (manager +0x905C-+0x905F), past the header's rate +0xB8; read and written by no function; nothing fixes its width |

### The manager part at +0xA0D0

This field sits in the part at `+0xA0D0` of the manager, whose two `0x110`-byte elements start at its `+0x000`; the offset is from the start of the part.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x220` | `u8[8]` | boundBase | the start of the block the two 0x110 elements are bound to: 0x003F7E80 passes this + 0x220 as the second qword of each element's construct message (0x003F7EAA, 0x003F7EB1), the element keeps it as its bound object (0x003F83C6) and reads it at +0x740, which is this + 0x960 (0x003F8820), and +0x754, which is this + 0x974 (0x003F82BF). These eight bytes themselves are read and written by no function; nothing fixes their width |

### The selection marker's slots

The selection marker keeps two `0x20`-byte slots at its `+0x30` (The selection marker above). A new unit starts the slot that bit 1 of the marker's `+0x74` names and flips that bit, so the next unit takes the other slot (`0x0028CB1F`-`0x0028CB66`).

`SelectionMarkerSlot` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | position | the unit's position in the world, x, y, z and 1.0: `0x002E7F70` writes it from the unit's model (`0x003E5510`) when the slot starts (`0x0028CB70`-`0x0028CB77`) and on every update while the unit's handle still resolves and the slot is not fading out (`0x0028CEE3`-`0x0028CEFE`); each of the slot's three sprites copies it as its own position (`0x0028D665`-`0x0028D66B`) |
| `+0x10` | `i16` | growth | the slot's growth in 256ths: 0 when the slot starts (`0x0028CB52`), 16 more on every update up to 256 (`0x0028CF4D`-`0x0028CF67`). The draw reads it as the time into the colour track `0x00915FB0` and scales the sprites' brightness by it (`0x0028D4AD`, `0x0028D5D3`-`0x0028D610`), and scales the alpha of the second, widening pass by it (`0x0028D911`-`0x0028D94B`) |
| `+0x12` | `u8` | unobservedByte012 | set to `0x80` when the slot starts (`0x0028CB62`), as the marker's own byte `+0x2B` is when the marker starts (`0x0028CAA2`); read by no function |
| `+0x13` | `u8` | alpha | the slot's alpha, 0 to 128: 0 when the slot starts (`0x0028CB52`); each update adds 32 / [`0x01DFE0B4`] up to 128 while flag bit 1 is clear, and takes the same away while it is set, freeing the slot (flag bit 0 cleared) when it would fall below 0 (`0x0028CF03`-`0x0028CF4A`). The draw multiplies the marker's fade `+0x76` by it over 128 (`0x0028D488`-`0x0028D497`) |
| `+0x14` | `u16` | flags0014 | bit 0: the slot is in use (set at `0x0028CB5A`, cleared when the alpha runs out at `0x0028CF29`); bit 1: the slot fades out, set when the unit's handle no longer resolves (`0x00273780` at `0x0028CEAC`-`0x0028CEC4`) or when the marker moves to another unit (`0x0028C940`, `0x0028CB00`-`0x0028CB11`); bit 3: `0x00273750` answers that the unit's class nibble is 1 or 2 (`0x0028CECE`-`0x0028CEEA`), passed to the sprite binder `0x003F1430` (`0x0028D6CA`-`0x0028D6F0`) |
| `+0x16` | `i16` | lastGrowth | the growth `+0x10` before the last update (`0x0028CF56`). While it differs from `+0x10` the slot is still widening and the draw draws three rings of the three sprites at half alpha; once they are equal it draws one (`0x0028D513`-`0x0028D59B`) |
| `+0x18` | `u32` | unit | the handle of the unit the slot marks, from `0x0028CA40`'s second argument (`0x0028CB5F`); the update resolves it (`0x0028CEA9`, `0x0028CECE`, `0x0028CEE3`) and `0x0028CA40` compares it with a new request (`0x0028CAC9`) |
| `+0x1C` | `u8[4]` | pad01C | zeroed when the slot starts by the qword store `0x0028CB56`, which also covers `+0x18`; read and written by no other function; nothing fixes its width |

### The level-up popups

The part at `+0x7FB0` holds six `0x110`-byte records, one per unit whose level went up (`0x002905D0`, Its parts above). The first `0xF0` bytes of a record become the popup widget the pump `0x00296860` builds in place.

`LevelUpBlink` (`0x110` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header) when the pump `0x00296860` builds the record's `0xF0`-byte widget in place with procedure `0x00299D10` (`0x002968B5`-`0x002968DE`) |
| `+0x0C0` | `i32` | life | the frames the popup stays: 30 x [`0x01DFE0B4`] when built (`0x00299F3E`-`0x00299F52`); each update while the widget's state nibble `+0x7C` is 3 and flag bit 1 is clear takes one away, and at 0 or below sets flag bit 1 and asks for the close `0x00244F00` (`0x0029A063`-`0x0029A092`) |
| `+0x0C4` | `u32` | liveKey00C4 | the handle of the unit the popup is over: the construct message's second argument (`0x00299F35`-`0x00299F38`), which the pump passes from the record's key `+0xF4` (`0x002968CA`-`0x002968D9`); each update resolves it (`0x00299FC9`-`0x00299FCF`) and `0x00299A30` matches a live record by it (`0x00299A71`) |
| `+0x0C8` | `u32` | queuedValue | the construct message's first argument (`0x00299F2C`-`0x00299F2F`), the value the pump takes from the queue (`0x002968C5`); `0x002905D0` only ever queues 1 (`0x002905F6`); read by no function |
| `+0x0CC` | `f32` | fade | the popup's opacity, 0 to 1: 1.0 when built (`0x00299F22`); each update adds [`0x01DFE0BC`] / 6 up to 1.0 while flag bit 0 is set and takes it away down to 0 while it is clear (`0x0029A003`-`0x0029A059`); the draw scales the alpha `+0x58` of the widget's draw record `+0x38` by it (`0x00299D72`, `0x00299E65`, `0x00299ECE`-`0x00299EDD`) |
| `+0x0D0` | `f32[4]` | position | the unit's position, x, y, z and 1.0, which `0x002E9A90` writes from the unit's model (`0x003E5810`, 1.0 at `0x002E9AE2`) on each update while the handle resolves (`0x00299FE2`-`0x00299FEF`); the draw projects it through the view `0x02AEDDB0` (`0x00249080` at `0x00299D91`-`0x00299DBA`) and centres the popup on the screen point (`0x00299E35`-`0x00299E5D`) |
| `+0x0E0` | `void*` | layout | the popup's layout, record 0 of MRP unit 4 at [`0x0209AC30`] + `0x20` (`0x0035D3F0`) built by `0x002432B0` with the widget as parent (`0x00299F58`-`0x00299F6F`); its width `+0x08` and height `+0x0A` go to the header's `+0x9C` and `+0x9E` (`0x00299F76`-`0x00299F88`) and centre the drawn popup (`0x00299D8A`-`0x00299DB2`, `0x00299E35`-`0x00299E4B`) |
| `+0x0E8` | `u32` | flags | bit 0: the unit is present, set when built (`0x00299F1B`) and cleared when the handle no longer resolves (`0x00299FD9`), which turns the fade `+0xCC` downward; bit 1: finished, set by the close message 15 (`0x00299D5F`) or when `+0xC0` runs out (`0x0029A081`), and stops the count; bit 2: running, set when built, needed for the fade and the count (`0x00299FF4`-`0x00299FFD`) and for any draw (`0x00299D6B`-`0x00299D85`); bit 3: drawn once, set by the first draw on screen, which draws nothing (`0x00299E56`-`0x00299E78`), after which each draw pulses the brightness `+0x5A` as 128 + 64 sin(pi (frame mod [`0x01E0C550`]) / [`0x01E0C550`]) (`0x00299E7D`-`0x00299ECA`) |
| `+0x0EC` | `u8[4]` | unobservedSpan00EC | read and written by no function; nothing fixes its width |
| `+0x0F0` | `u32` | claimed00F0 | the record's claim flag, 0 when free: the producer `0x002966E0` sets it to 1 when it claims a free record (`0x002967D3`, `0x0029680F`) and the pump `0x00296860` clears it once the record's queue is empty (`0x00296903`-`0x00296909`); the pump builds the popup only while it is set (`0x00296897`) |
| `+0x0F4` | `u32` | key00F4 | the unit's handle, written when the record is claimed from the producer's argument (`0x002967DD`, `0x00296819`): `0x002905D0`'s caller passes the levelled unit's handle [unit + 8] (`0x0030C811` in `0x0030C650`); `0x00299A30` matches a claimed record by it (`0x00299A7B`) |
| `+0x0F8` | `u32[3]` | queue00F8 | three queued values, each 1 from `0x002905D0` (`0x002905F6`): the producer appends a value it does not already hold at `+0x106` (`0x00296712`-`0x0029675D`, `0x002967E4`); the pump builds one popup for the value at `+0x104` and clears that slot (`0x002968AC`-`0x002968EF`) |
| `+0x104` | `i16` | consumeCursor0104 | the pump's index into `+0xF8`, wrapping at 3 (`0x002968AC`, `0x002968F3`-`0x002968FC`) |
| `+0x106` | `i16` | produceCursor0106 | the producer's index into `+0xF8`, wrapping at 3 (`0x00296736`-`0x0029675D`, `0x002967CB`-`0x002967FD`, `0x00296807`-`0x00296839`) |
| `+0x108` | `u8[8]` | unobservedSpan0108 | read and written by no function; nothing fixes its width |

### The sprites of the part at +0xA0

The part at `+0xA0` keeps 64 sprites of `0x100` bytes at its `+0x20`. `0x003F9390` places them along the lines of the zone script's lists 0 and 1 (`0x003F9720`), and `0x003F8C70` hands them to the depth list on each draw (The draw pass above), so they have the layout every function of that table reads.

`HudLineSprite` (`0x100` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | position | x, y, z: the sprite's place on the line, which `0x00270260` sets at parameter t along the line's points (`0x003F954F`-`0x003F956E`); the fourth float is the size the draw multiplies the corner offsets by (`0x003F0903`-`0x003F0A15`), which the part sets to 0.5 after placing the sprite (`0x003F95B1`). The depth pass projects x, y, z through the view `0x02AEDDB0` (`0x002720F0` at `0x003F01DE`) |
| `+0x10` | `f32[4]` | offset | added to `+0x00` before the corners are projected (`0x00202B10` at `0x003F068F`-`0x003F069A`); (0, 0, 0, 1.0) from the reset `0x003F00F0` (`0x003F014B`-`0x003F0162`, the constant `0x01EF93F0`) |
| `+0x20` | `u64` | tex0 | the picture's TEX0 [picture + `0x30`] with the palette block (2 x [`+0x52C4`] + the point's style byte) added at bit 38 (`0x003F95BC`-`0x003F95E9`); part of the `0xB0` bytes the draw copies into the packet (`0x003F1E24`-`0x003F1E31`) |
| `+0x28` | `u64` | tex0Register | 6, the register number of the TEX0 value before it (`0x003F95F0`), copied into the packet with it |
| `+0x30` | `f32[4]` | texRect | the texture rectangle, u, v, width and height as fractions of the picture's size: the part's cell rectangle `+0x00` copied by `0x00202C90` (`0x003F95E1`, `0x003F961E`), which `0x003F8D20` takes from the picture's cell (`0x002711E0` at `0x003F8E09`); the draw scales it by the picture's width and height (`0x003F111C`-`0x003F117F`) |
| `+0x40` | `i32` | red | 255 (`0x003F9629`); the corners' red, 0 to 255 (`0x003F0E8F`-`0x003F0EBE`) |
| `+0x44` | `i32` | green | 255 (`0x003F9630`); the corners' green (`0x003F0E98`-`0x003F0EC4`) |
| `+0x48` | `i32` | blue | 255 (`0x003F9637`); the corners' blue (`0x003F0EA1`-`0x003F0ECA`) |
| `+0x4C` | `i32` | alpha | 128 x min(1, sin((6 - d) / 6 x pi/2)) x the point's alpha / 128, d being the sprite's distance from the line point the segment starts at; no sprite is placed farther than 6 (`0x003F957B`-`0x003F9623`); the draw scales it by its camera fade (`0x003F1E36`-`0x003F1E49`) |
| `+0x50` | `f32[4]` | corners | the corner offsets x0, y0, x1, y1: (-0.25, -0.25, 0.25, 0.25) (`0x003F963E`-`0x003F9653`), turned by `+0x60` and scaled by the size `+0x0C` (`0x003F0903`-`0x003F0A15`) |
| `+0x60` | `f32[4]` | cosSin060 | (cos a, sin a, -sin a, cos a) of the sprite's turn a: 0 from the reset `0x003F00F0` (`0x003F0101`-`0x003F012E`), then (frame mod 160) x 360 / 160 degrees, one turn every 160 frames (`0x003F93F4`-`0x003F9462`, `0x003F1230` at `0x003F954A`); the draw turns the corners `+0x50` by it (`0x003F0915`-`0x003F09C7`) |
| `+0x70` | `f32[4]` | screenShift | `+0x70` and `+0x74` are added to all four projected corners, divided by the frame scales `0x0024ABC0` and `0x0024ABA0` (`0x003F0C81`-`0x003F0D75`); (0, 0, 0, 1.0) from the reset (`0x003F0140`-`0x003F0147`), so the part's sprites stay in place; the draw reads neither `+0x78` nor `+0x7C` |
| `+0x80` | `u32` | twoColour | 0 from the reset (`0x003F013A`); when it is not 0 the draw gives two of the four corners the colour `+0x90`-`+0x9C` instead of `+0x40`-`+0x4C` (`0x003F0E04`-`0x003F0EAF`) |
| `+0x84` | `u8[12]` | pad084 | copied into the packet with the first `0xB0` bytes (`0x00271290` from `0x003F1E31`); read by no other instruction; nothing fixes its width |
| `+0x90` | `i32[4]` | colour2 | the second colour, red, green, blue and alpha, that the draw reads only while `+0x80` is not 0 (`0x003F0E57`-`0x003F0E89`); the part never sets `+0x80` or these words |
| `+0xA0` | `u8[16]` | pad0A0 | copied into the packet with the first `0xB0` bytes (`0x003F1E31`); read by no other instruction; nothing fixes its width |
| `+0xB0` | `void*` | sortLow | the depth tree's lower link: `0x003F19D0` clears it when it inserts the sprite and hangs a sprite of lower depth from it (`0x003F19D5`, `0x003F1A1E`-`0x003F1A41`); the draw walk follows it (`0x003F0532`) |
| `+0xB8` | `void*` | sortHigh | the depth tree's higher link (`0x003F19DC`, `0x003F1A0D`-`0x003F1A2F`); the draw walk follows it (`0x003F0543`-`0x003F0564`) |
| `+0xC0` | `void*` | sortParent | the depth tree's parent link (`0x003F19E3`, `0x003F1A36`, `0x003F1A48`); the draw walk climbs it (`0x003F0523`, `0x003F056E`) |
| `+0xC8` | `f32` | depth | 1 / w from the projection `0x002720F0`, stored for every sprite of the list (`0x003F01E6`) and, for a sprite in front with x and y inside 0 to 4096, stored negated (`0x003F020E`-`0x003F0219`); `0x003F19D0` sorts on it (`0x003F19F3`, `0x003F1A00`) |
| `+0xCC` | `u8[4]` | pad0CC | read and written by no function; nothing fixes its width |
| `+0xD0` | `void*` | listNext | the next sprite of the depth list: `0x003F1290` clears it when it appends the sprite (`0x003F1292`) and sets it on the old tail (`0x003F12B1`); `0x003F0170` walks it (`0x003F0229`) |
| `+0xD8` | `void*` | listPrev | the previous sprite of the depth list: cleared on append (`0x003F1299`), set to the old tail (`0x003F12BC`) |
| `+0xE0` | `void*` | picture | the part's picture partytop_8_c, [`+0x52B8`] (`0x003F965A`-`0x003F9661`), which `0x003F8D20` fetches by name with `0x0024A5A0` (`0x003F8D45`-`0x003F8D51`); the draw reads its size from the header `+0x20` (`0x003F0F02`-`0x003F0F44`) and hands it to the batcher (`0x003F11D1`-`0x003F11E8`) |
| `+0xE8` | `i16` | paletteOffset | 0 (`0x003F9668`); for a 4-bit picture the draw adds 4 x it at bit 37 of the bound TEX0 (`0x003F1CC3`-`0x003F1CFC`) and starts a new batch when it differs from the batch's (`0x003F1BF4`-`0x003F1BFE`) |
| `+0xEA` | `u16` | drawFlags | bit 0 dims the sprite while the camera looks at it from behind the focus unit (`0x003F1A87`-`0x003F1BC3`); `0x003FAB60` sets it on the world-object sprites (`0x003FAC9E`); nothing sets it on the part's sprites, so it stays 0 from the manager's clear |
| `+0xEC` | `i32` | palette | the palette the batcher binds with the picture (`0x003F1192`-`0x003F11E8`): -1 from the reset (`0x003F0152`), then [`+0x52C4`] plus the point's style byte (`0x003F95F8`-`0x003F9610`) |
| `+0xF0` | `i32` | kind | the picture kind the draw switches on: -1 chain_item, -2 targetline_p, -3 chainflash, any other the picture `+0xE0` (`0x003F0F55`-`0x003F111C`); 0 from the reset and the part (`0x003F015C`, `0x003F9606`) |
| `+0xF4` | `u8[12]` | unobservedTail0F4 | read and written by no function; nothing fixes its width |

## State

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B5F1F0` | `f32` | 0 | the horizontal scale of the depth-list sprites: the screen's aspect factor `0x00183280()` (height x 16/9, or `0x001DD110()`, over width) times 1.0, or 0.75 when `0x002DDC50()` answers non-zero and `0x00180150()` answers 0 (`0x00254A00`; `0x003F03C9`-`0x003F048D`). `0x003F0610` multiplies one offset of each of the four corners by it and divides it by the frame width over 512 (`0x0024ABC0`) | `0x003F0170` (`0x003F0499`) | `0x003F0610` (`0x003F0772`, `0x003F07AB`, `0x003F07E4`, `0x003F081D`) |
| `0x02B5F1F4` | `u32` | 0 | the palette of a `+0x10F40` mark's sprites: `0x003F3260` stores the mark's `+0x48` here before drawing it, and `0x003F3710` hands it to the sprite batcher's state as its palette `+0x3A38` (`0x00181930`, `0x001B2410`). `0x003F2CF0` also stores the cell of a `+0x10F20` mark's kind here (`0x002713B0(+0x990)`), which `0x003F3260` replaces before any read | `0x003F2CF0` (`0x003F2D5D`); `0x003F3260` (`0x003F3327`) | `0x003F3710` (`0x003F3851`), from `0x003F3260` (`0x003F339D`, `0x003F33CF`, `0x003F3420`, `0x003F3452`) |
| `0x022C83E0` | `void*` | 0 | the field marker widget: `0xF8` bytes with procedure `0x0035C160`, which on each draw (message 4) projects the unit of handle `+0xEC` through the view `0x02AEDDB0` (`0x00249110`) and draws a picture there whose brightness swings with the frame counter `0x0208F570` (`0x0035C1D0`-`0x0035C34D`); built once, nothing clears it | `0x0035C0D0` (`0x0035C0F2`), run by the field set-up `0x00253A10` (`0x00253A14`) | `0x0035C0D0`, which builds it only while it is 0 (`0x0035C0D4`); `0x0035C080` (`0x0035C084`, `0x0035C09E`) and `0x0035C100` (`0x0035C106`, `0x0035C117`), which close or fade the help block's rings (`0x00290990`, `0x00290B10`) when the widget's `+0xC4` is set and clear it; `0x0035C080` has 20 call sites in 12 functions and `0x0035C100` three in two, among them the leader choice (`0x0029C01B`, `0x0029C02C`) |
| `0x0209E610`-`0x0209E614` | `u8[5]` | 0 (zero-filled tail of `.data`) | the first of the two times `0x002BDB20` returns for help-message kinds 1-5, in frames: 12, 15, 20, 25 and 30 times the frame-rate multiplier `0x01DFE0B4` (1 in this build) | `0x002BDA90` (`0x002BDAA4`, `0x002BDAB3`, `0x002BDAC2`, `0x002BDACE`, `0x002BDAD7`), entered by the tail jump at `0x001EDE60` in `0x001EDDC0` | `0x002BDB20` (`0x002BDB3B`-`0x002BDB42`, index kind - 1), called by `0x0028E110` (`0x0028E136`) |

No other instruction reaches these four.

## Modding notes

- Every target line, ring and mark shares one `0x8030`-byte pool; when it is full a ring request waits a frame and a
  line is not made.
- Target Lines hides only the lines and the `+0x10F20` and `+0x10F40` marks; the target ring, the selection marker
  and the `+0x10F30` marks stay.
- A ring's colour is a palette index from the four bytes at `0x00916010`.

## Related

- [Battle menu](battle-menu.md) - the menu, help line and gauges the HUD holds.
- [Party list](party-list.md) - the member rows the HUD holds.
- [Subsystem update flags](../Engine-Core/subsystem-update-flags.md) - the pump that steps each part.
- [Menu sprites](menu-sprites.md) - the `targetline_p` picture.
- [Widgets](widgets.md) - the widget model the parts use.
