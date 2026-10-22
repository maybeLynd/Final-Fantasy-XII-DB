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
| `0x002C8A60(part, entry)` | gives an entry a name box: the box already showing its unit, else a free one, else the box after the last one used (`+0x1D7A` bit 7 flips). A new box is cleared and filled by `0x002C8BC0`; the unit goes to `+0x1B0` with bit 0 set and bit 1 clear in `+0x1B4` |
| `0x002C6B50(part)` | fades each open name box in, or out while its bit 1 is set, by 32 / `[0x01DFE0B4]` a frame up to `0x80`; a box faded out loses bit 0 |
| `0x002C6BE0(part, box)` | the same for the box at `+0x1B80`, also moving its ramps `+0x1BC`, `+0x1BE` and `+0x1D0`; a box faded out drops its entry |
| `0x002C62B0(part, ...)` | the draw: each entry through `0x002C7660`, with bit 10 of the script hold mask (`0x002E0FA0`) and the focus unit, then the `+0x1B80` box (`0x002C7F90`) and each open name box at the part's alpha times the box's (`0x003F14D0`) |
| `0x002C7B10(entry, ...)` | the status mark over a unit: the cell `0x300` sprite of the status `+0x16` (`0x003F12E0`) at the alpha `+0x15`. Statuses 4, 9 and 24 pulse in size along the track `0x00916E90`, status 12 turns along `0x00916ED0`; with `+0x17` bit 2 it adds the status numbers (`0x002C84E0`) |
| `0x002C8920(unit, alpha, list, ...)` | queues the cell `0xE00` sprite of the picture `0x0035D460` returns over a unit; `0x002C7660` asks for it for the unit `0x0035BAD0` names when `0x003135C0` and `0x00273460` answer non-zero |
| `0x002C69A0(pos, sprite, cell, alpha, rgba, picture)` | fills a sprite from a picture cell: the position with w = -1, the texture rectangle, the colour bytes with alpha x `rgba.a` / 128, and half the cell's size to each side; `0x002C7F90`, `0x002C8310` and `0x002C8820` use it |
| `0x002C6450(part)` | answers whether the focus unit's entry is drawn at full alpha (entry `+0x14` x `+0x1D78` at least `0x4000`), or, with no entry, whether the part is at `0x80`. A scan of the image for calls, jumps and `lea` to it finds none |

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
